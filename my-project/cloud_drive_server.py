#!/usr/bin/env python3

from __future__ import annotations

import argparse
import cgi
import json
import mimetypes
import os
import shutil
import sys
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse


def build_root(path_value: str | None) -> Path:
    root_path = Path(path_value or os.environ.get("CLOUD_DRIVE_ROOT", "/home/azureuser/cloud-drive")).expanduser()
    root_path.mkdir(parents=True, exist_ok=True)
    return root_path.resolve()


ROOT = build_root(None)
UPLOAD_PASSWORD = os.environ.get("CLOUD_DRIVE_UPLOAD_PASSWORD", "sihan123")


def human_size(byte_count: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(byte_count)
    for unit in units:
        if value < 1024.0 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024.0
    return f"{byte_count} B"


def iso_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone().isoformat(timespec="seconds")


def relative_path(value: str) -> str:
    normalized = value.strip().lstrip("/")
    if not normalized or normalized == ".":
        return ""
    return Path(normalized).as_posix()


def resolve_inside_root(relative_value: str) -> Path:
    candidate = (ROOT / relative_path(relative_value)).resolve()
    if candidate == ROOT or ROOT in candidate.parents:
        return candidate
    raise ValueError("Path escapes storage root")


def safe_name(value: str) -> str:
    candidate = Path(value).name.strip()
    if not candidate or candidate in {".", ".."}:
        raise ValueError("Invalid name")
    return candidate


def parent_relative_path(value: str) -> str:
    cleaned = relative_path(value)
    if not cleaned:
        return ""
    parent = Path(cleaned).parent.as_posix()
    return "" if parent == "." else parent


def make_unique_path(base_path: Path) -> Path:
    if not base_path.exists():
        return base_path

    suffix = "".join(base_path.suffixes)
    stem = base_path.name[: -len(suffix)] if suffix else base_path.name

    for index in range(1, 10_000):
        candidate_name = f"{stem} ({index}){suffix}"
        candidate_path = base_path.with_name(candidate_name)
        if not candidate_path.exists():
            return candidate_path

    raise RuntimeError("Cannot allocate a unique filename")


def file_metadata(file_path: Path) -> dict[str, object]:
    stat_result = file_path.stat()
    kind = "directory" if file_path.is_dir() else "file"
    return {
        "name": file_path.name,
        "path": relative_path(file_path.relative_to(ROOT).as_posix()),
        "kind": kind,
        "size": stat_result.st_size if file_path.is_file() else 0,
        "modified": iso_timestamp(stat_result.st_mtime),
    }


def list_directory(folder_path: Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for child in sorted(folder_path.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower())):
        if child.is_symlink():
            continue
        entries.append(file_metadata(child))
    return entries


def request_json(handler: BaseHTTPRequestHandler) -> dict[str, object]:
    content_length = int(handler.headers.get("Content-Length", "0") or "0")
    if content_length <= 0:
        return {}
    raw_body = handler.rfile.read(content_length)
    if not raw_body:
        return {}
    return json.loads(raw_body.decode("utf-8"))


def write_response(handler: BaseHTTPRequestHandler, status: HTTPStatus, content_type: str, data: bytes) -> None:
    handler.send_response(status)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(data)))
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type, X-Upload-Password")
    handler.end_headers()
    handler.wfile.write(data)


def send_json(handler: BaseHTTPRequestHandler, status: HTTPStatus, payload: dict[str, object]) -> None:
    write_response(handler, status, "application/json; charset=utf-8", json.dumps(payload, ensure_ascii=False).encode("utf-8"))


def send_text(handler: BaseHTTPRequestHandler, status: HTTPStatus, content: str, content_type: str = "text/plain; charset=utf-8") -> None:
    write_response(handler, status, content_type, content.encode("utf-8"))


def send_html(handler: BaseHTTPRequestHandler, status: HTTPStatus, content: str) -> None:
    write_response(handler, status, "text/html; charset=utf-8", content.encode("utf-8"))


def parse_query(path: str) -> tuple[str, dict[str, list[str]]]:
    parsed = urlparse(path)
    return parsed.path, parse_qs(parsed.query)


def get_query_value(values: dict[str, list[str]], key: str, default: str = "") -> str:
    value_list = values.get(key)
    if not value_list:
        return default
    return value_list[0]


APP_HTML = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>云盘 / Cloud Drive</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #07111d;
      --panel: rgba(8, 15, 28, 0.88);
      --panel-soft: rgba(10, 18, 34, 0.72);
      --border: rgba(148, 163, 184, 0.16);
      --border-strong: rgba(96, 165, 250, 0.22);
      --text: #e5eefc;
      --muted: rgba(226, 232, 240, 0.72);
      --accent: #38bdf8;
      --accent-strong: #0ea5e9;
      --accent-soft: rgba(56, 189, 248, 0.12);
      --danger: #f87171;
      --success: #34d399;
      --shadow: 0 28px 70px rgba(0, 0, 0, 0.34);
      --radius-xl: 28px;
      --radius-lg: 20px;
      --radius-md: 14px;
      --radius-sm: 10px;
      --mono: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
      --sans: "Aptos", "Segoe UI Variable Display", "PingFang SC", "Microsoft YaHei", sans-serif;
    }

    * { box-sizing: border-box; }
    html, body { min-height: 100%; }
    body {
      margin: 0;
      font-family: var(--sans);
      color: var(--text);
      background:
        radial-gradient(circle at 12% 18%, rgba(56, 189, 248, 0.20), transparent 26%),
        radial-gradient(circle at 88% 16%, rgba(16, 185, 129, 0.12), transparent 22%),
        radial-gradient(circle at 82% 82%, rgba(245, 158, 11, 0.10), transparent 20%),
        linear-gradient(180deg, #07111d 0%, #08131f 52%, #050b14 100%);
    }

    body::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background-image:
        linear-gradient(rgba(148, 163, 184, 0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(148, 163, 184, 0.06) 1px, transparent 1px);
      background-size: 52px 52px;
      mask-image: linear-gradient(180deg, rgba(0, 0, 0, 0.8), transparent 90%);
      opacity: 0.55;
    }

    a { color: inherit; }

    .cloud-drive {
      position: relative;
      width: min(1280px, calc(100vw - 2rem));
      margin: 0 auto;
      padding: 1.2rem 0 2rem;
    }

    .hero {
      display: grid;
      gap: 1.25rem;
      grid-template-columns: 1.5fr 0.9fr;
      padding: 1.8rem;
      border: 1px solid var(--border);
      border-radius: var(--radius-xl);
      background: rgba(6, 12, 23, 0.78);
      backdrop-filter: blur(24px);
      box-shadow: var(--shadow);
    }

    .kicker {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.35rem 0.82rem;
      border-radius: 999px;
      border: 1px solid var(--border-strong);
      background: var(--accent-soft);
      color: #c0e7ff;
      font-size: 0.84rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .hero h1 {
      margin: 0.85rem 0 0.65rem;
      font-size: clamp(2.4rem, 5vw, 4.8rem);
      line-height: 0.95;
      letter-spacing: -0.05em;
    }

    .hero p {
      margin: 0;
      max-width: 62ch;
      color: var(--muted);
      line-height: 1.75;
      font-size: 1.01rem;
    }

    .pill-row {
      display: flex;
      flex-wrap: wrap;
      gap: 0.65rem;
      margin-top: 1rem;
    }

    .pill {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.4rem 0.76rem;
      border-radius: 999px;
      background: rgba(148, 163, 184, 0.08);
      border: 1px solid rgba(148, 163, 184, 0.15);
      color: rgba(226, 232, 240, 0.88);
      font-size: 0.88rem;
    }

    .stats {
      display: grid;
      gap: 0.8rem;
      align-content: start;
      padding: 1rem;
      border-radius: 22px;
      background: linear-gradient(180deg, rgba(12, 20, 35, 0.96), rgba(8, 15, 28, 0.94));
      border: 1px solid var(--border);
    }

    .stat {
      display: grid;
      gap: 0.15rem;
      padding: 0.95rem 1rem;
      border-radius: var(--radius-md);
      background: rgba(148, 163, 184, 0.05);
      border: 1px solid rgba(148, 163, 184, 0.08);
    }

    .stat strong {
      font-size: 1.3rem;
      letter-spacing: -0.03em;
    }

    .stat span {
      color: var(--muted);
      font-size: 0.88rem;
    }

    .layout {
      display: grid;
      gap: 1rem;
      grid-template-columns: 340px 1fr;
      margin-top: 1rem;
    }

    .panel {
      padding: 1.2rem;
      border-radius: var(--radius-xl);
      border: 1px solid var(--border);
      background: rgba(6, 12, 23, 0.78);
      backdrop-filter: blur(20px);
      box-shadow: var(--shadow);
    }

    .panel h2 {
      margin: 0 0 0.9rem;
      font-size: 1.05rem;
      letter-spacing: -0.02em;
    }

    .field {
      display: grid;
      gap: 0.45rem;
      margin-bottom: 0.9rem;
    }

    .field label {
      font-size: 0.9rem;
      color: rgba(226, 232, 240, 0.74);
    }

    .field input {
      width: 100%;
      padding: 0.85rem 0.95rem;
      border-radius: var(--radius-md);
      border: 1px solid rgba(148, 163, 184, 0.16);
      background: rgba(2, 6, 16, 0.86);
      color: var(--text);
      font: inherit;
      outline: none;
      transition: border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease;
    }

    .field input:focus {
      border-color: rgba(56, 189, 248, 0.55);
      box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.12);
    }

    .row {
      display: flex;
      gap: 0.6rem;
    }

    .row > * { flex: 1; }

    .button,
    .button-secondary,
    .button-danger {
      appearance: none;
      border: 0;
      border-radius: 14px;
      padding: 0.82rem 1rem;
      font: inherit;
      font-weight: 700;
      cursor: pointer;
      transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease, opacity 0.18s ease;
      text-align: center;
    }

    .button {
      color: white;
      background: linear-gradient(135deg, #38bdf8, #0ea5e9);
      box-shadow: 0 14px 28px rgba(14, 165, 233, 0.32);
    }

    .button-secondary {
      color: var(--text);
      background: rgba(148, 163, 184, 0.11);
      border: 1px solid rgba(148, 163, 184, 0.14);
    }

    .button-danger {
      color: #ffe4e6;
      background: rgba(248, 113, 113, 0.12);
      border: 1px solid rgba(248, 113, 113, 0.18);
    }

    .button:hover,
    .button-secondary:hover,
    .button-danger:hover,
    .file-actions button:hover {
      transform: translateY(-1px);
    }

    .dropzone {
      display: grid;
      place-items: center;
      min-height: 168px;
      padding: 1rem;
      margin: 0.4rem 0 0.9rem;
      border-radius: 20px;
      border: 1px dashed rgba(96, 165, 250, 0.34);
      background: linear-gradient(180deg, rgba(8, 17, 31, 0.92), rgba(7, 13, 23, 0.78));
      color: var(--muted);
      text-align: center;
      line-height: 1.6;
      cursor: pointer;
    }

    .dropzone.is-dragover {
      border-color: rgba(56, 189, 248, 0.8);
      color: #d6efff;
      background: rgba(14, 165, 233, 0.12);
    }

    .hint {
      margin: 0.9rem 0 0;
      color: var(--muted);
      font-size: 0.9rem;
      line-height: 1.7;
    }

    .toolbar {
      display: flex;
      flex-wrap: wrap;
      gap: 0.85rem;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 0.9rem;
    }

    .breadcrumbs {
      display: flex;
      flex-wrap: wrap;
      gap: 0.4rem;
      color: rgba(226, 232, 240, 0.82);
      min-height: 2rem;
      align-items: center;
    }

    .crumb {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.35rem 0.64rem;
      border-radius: 999px;
      border: 1px solid rgba(148, 163, 184, 0.12);
      background: rgba(148, 163, 184, 0.06);
      cursor: pointer;
      user-select: none;
    }

    .crumb.is-active {
      background: rgba(56, 189, 248, 0.14);
      border-color: rgba(56, 189, 248, 0.22);
      color: #d8f0ff;
    }

    .search {
      width: min(320px, 100%);
      padding: 0.78rem 0.92rem;
      border-radius: 14px;
      border: 1px solid rgba(148, 163, 184, 0.16);
      background: rgba(2, 6, 16, 0.84);
      color: var(--text);
      font: inherit;
      outline: none;
    }

    .status {
      display: flex;
      align-items: center;
      gap: 0.65rem;
      margin-bottom: 0.85rem;
      padding: 0.8rem 0.92rem;
      border-radius: 16px;
      background: rgba(148, 163, 184, 0.07);
      border: 1px solid rgba(148, 163, 184, 0.12);
      color: var(--muted);
      min-height: 3rem;
    }

    .status.is-error {
      color: #ffd7d7;
      background: rgba(248, 113, 113, 0.12);
      border-color: rgba(248, 113, 113, 0.18);
    }

    .status.is-success {
      color: #d1fae5;
      background: rgba(16, 185, 129, 0.12);
      border-color: rgba(16, 185, 129, 0.18);
    }

    .table-wrap {
      overflow: hidden;
      border-radius: 22px;
      border: 1px solid rgba(148, 163, 184, 0.12);
      background: linear-gradient(180deg, rgba(8, 15, 28, 0.92), rgba(5, 10, 18, 0.88));
    }

    table {
      width: 100%;
      border-collapse: collapse;
    }

    thead th {
      padding: 0.9rem 1rem;
      text-align: left;
      color: rgba(226, 232, 240, 0.72);
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      background: rgba(148, 163, 184, 0.05);
    }

    tbody td {
      padding: 0.95rem 1rem;
      border-top: 1px solid rgba(148, 163, 184, 0.08);
      vertical-align: middle;
    }

    tbody tr:hover {
      background: rgba(56, 189, 248, 0.05);
    }

    .file-name {
      display: grid;
      gap: 0.2rem;
    }

    .file-name strong {
      font-weight: 700;
      color: #f8fafc;
    }

    .file-name span,
    .file-meta {
      color: var(--muted);
      font-size: 0.9rem;
    }

    .file-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 0.45rem;
    }

    .file-actions button,
    .file-actions a {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 2.35rem;
      padding: 0.45rem 0.74rem;
      border-radius: 12px;
      border: 1px solid rgba(148, 163, 184, 0.12);
      background: rgba(148, 163, 184, 0.08);
      color: var(--text);
      text-decoration: none;
      cursor: pointer;
      font: inherit;
    }

    .empty {
      padding: 2.6rem 1.2rem;
      color: var(--muted);
      text-align: center;
      line-height: 1.75;
    }

    .loader {
      width: 1rem;
      height: 1rem;
      border-radius: 999px;
      border: 2px solid rgba(226, 232, 240, 0.28);
      border-top-color: #d5f5ff;
      animation: spin 0.8s linear infinite;
    }

    .mono {
      font-family: var(--mono);
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    @media (max-width: 1040px) {
      .hero,
      .layout {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 720px) {
      .cloud-drive {
        width: min(100vw - 1rem, 1280px);
        padding: 0.6rem 0 1.3rem;
      }

      .hero,
      .panel {
        padding: 1rem;
        border-radius: 20px;
      }

      .toolbar,
      .row {
        flex-direction: column;
      }

      .search {
        width: 100%;
      }

      thead {
        display: none;
      }

      table,
      tbody,
      tr,
      td {
        display: block;
        width: 100%;
      }

      tbody tr {
        padding: 0.9rem 0.85rem;
        border-top: 1px solid rgba(148, 163, 184, 0.08);
      }

      tbody td {
        padding: 0.25rem 0;
        border: 0;
      }

      tbody td[data-label]::before {
        content: attr(data-label) ": ";
        color: rgba(226, 232, 240, 0.66);
      }
    }
  </style>
</head>
<body>
  <div class="cloud-drive">
    <header class="hero">
      <div>
        <span class="kicker">Remote server backed storage</span>
        <h1>云盘 / Cloud Drive</h1>
        <p>这是一个直接运行在远程服务器上的文件管理界面。文件会存到 Azure VM 的磁盘里，适合大文件、备份和长期保存。上传和下载都走远程服务器，不占用你本地的存储空间。</p>
        <div class="pill-row">
          <span class="pill">大空间 / More space</span>
          <span class="pill">快速传输 / Fast transfers</span>
          <span class="pill">远程服务器 / Remote VM</span>
        </div>
      </div>
      <div class="stats">
        <div class="stat"><strong id="stat-used">--</strong><span>已用空间 / Used</span></div>
        <div class="stat"><strong id="stat-free">--</strong><span>可用空间 / Free</span></div>
        <div class="stat"><strong id="stat-count">--</strong><span>当前文件数 / Entries</span></div>
      </div>
    </header>

    <main class="layout">
      <section class="panel">
        <h2>操作区 / Actions</h2>

        <div class="field">
          <label for="folder-name">新建文件夹 / New folder</label>
          <div class="row">
            <input id="folder-name" type="text" placeholder="例如 backups / e.g. backups">
            <button id="create-folder" class="button-secondary" type="button">新建</button>
          </div>
        </div>

        <div class="field">
          <label>上传文件 / Upload</label>
          <div class="field" style="margin-bottom: 0.7rem;">
            <label for="upload-password">上传密码 / Upload password</label>
            <div class="row">
              <input id="upload-password" type="password" placeholder="请输入上传密码 / Enter upload password">
              <button id="save-upload-password" class="button-secondary" type="button">保存</button>
            </div>
          </div>
          <div id="dropzone" class="dropzone" tabindex="0" role="button" aria-label="上传文件区域">
            将文件拖到这里，或点击选择文件。支持批量上传。<br>
            Drop files here or click to select them.
          </div>
          <input id="file-input" type="file" multiple hidden>
          <p class="hint">只有上传需要密码，下载不需要。请使用你自己的上传密码后再开始上传。</p>
        </div>

        <div class="field">
          <label>导航 / Navigation</label>
          <div class="row">
            <button id="go-root" class="button-secondary" type="button">回到根目录</button>
            <button id="refresh-list" class="button" type="button">刷新</button>
          </div>
        </div>

        <p class="hint">文件会保存在远程服务器磁盘上。你可以把这里当成个人网盘、素材仓库或者备份盘。路径和删除操作都在服务器端处理。</p>
      </section>

      <section class="panel">
        <div class="toolbar">
          <div id="breadcrumbs" class="breadcrumbs"></div>
          <input id="search" class="search" type="search" placeholder="搜索当前目录 / Search this folder">
        </div>

        <div id="status" class="status">
          <span class="loader" aria-hidden="true"></span>
          <span>正在连接云盘后端 / Connecting to the cloud drive backend...</span>
        </div>

        <div class="table-wrap">
          <table aria-live="polite">
            <thead>
              <tr>
                <th>名称 / Name</th>
                <th>大小 / Size</th>
                <th>修改时间 / Modified</th>
                <th>操作 / Actions</th>
              </tr>
            </thead>
            <tbody id="file-list"></tbody>
          </table>
          <div id="empty-state" class="empty" hidden>
            当前目录还没有文件。<br>
            This folder is empty.
          </div>
        </div>
      </section>
    </main>
  </div>

  <script>
    const state = {
      path: "",
      entries: [],
      search: "",
      busy: false,
      health: null,
    };

    const elements = {};

    const formatBytes = (bytes) => {
      const units = ["B", "KB", "MB", "GB", "TB"];
      let value = Number(bytes) || 0;
      for (const unit of units) {
        if (value < 1024 || unit === units[units.length - 1]) {
          return unit === "B" ? `${value} ${unit}` : `${value.toFixed(1)} ${unit}`;
        }
        value /= 1024;
      }
      return `${bytes} B`;
    };

    const formatDate = (value) => {
      if (!value) return "--";
      const date = new Date(value);
      return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
    };

    const escapeHtml = (value) => String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");

    const normalizePath = (value) => {
      const cleaned = String(value || "").replace(/^\/+/, "").replace(/\/+$/, "");
      return cleaned === "." ? "" : cleaned;
    };

    const joinPath = (basePath, childName) => {
      const cleanBase = normalizePath(basePath);
      const cleanChild = normalizePath(childName);
      return cleanBase ? `${cleanBase}/${cleanChild}` : cleanChild;
    };

    const setStatus = (message, kind = "info") => {
      elements.status.classList.remove("is-error", "is-success");
      if (kind === "error") {
        elements.status.classList.add("is-error");
      } else if (kind === "success") {
        elements.status.classList.add("is-success");
      }
      elements.status.innerHTML = message;
    };

    const apiRequest = async (endpoint, options = {}) => {
      const response = await fetch(endpoint, {
        headers: {
          ...(options.headers || {}),
        },
        ...options,
      });
      if (!response.ok) {
        let detail = response.statusText;
        try {
          const payload = await response.json();
          detail = payload.error || payload.detail || detail;
        } catch (error) {
          try {
            detail = await response.text();
          } catch (ignored) {
            detail = response.statusText;
          }
        }
        throw new Error(detail || `HTTP ${response.status}`);
      }
      return response;
    };

    const refreshHealth = async () => {
      const response = await apiRequest("/health");
      const payload = await response.json();
      state.health = payload;

      const storage = payload.storage || {};
      elements.statUsed.textContent = formatBytes(storage.used_bytes || 0);
      elements.statFree.textContent = formatBytes(storage.free_bytes || 0);
      elements.statCount.textContent = String((state.entries || []).length);
    };

    const loadDirectory = async () => {
      if (state.busy) return;
      state.busy = true;
      elements.fileList.innerHTML = "";
      elements.emptyState.hidden = true;
      setStatus('<span class="loader" aria-hidden="true"></span><span>正在读取目录 / Loading directory...</span>');

      try {
        const response = await apiRequest(`/api/list?path=${encodeURIComponent(state.path)}`);
        const payload = await response.json();
        state.entries = payload.entries || [];
        state.path = payload.path || "";
        renderBreadcrumbs(payload.path || "");
        renderEntries();
        await refreshHealth();
        setStatus(`当前目录: <span class="mono">/${escapeHtml(state.path)}</span>`, "success");
      } catch (error) {
        state.entries = [];
        renderBreadcrumbs(state.path);
        elements.emptyState.hidden = false;
        setStatus(`连接失败: ${escapeHtml(error.message)}`, "error");
      } finally {
        state.busy = false;
      }
    };

    const renderBreadcrumbs = (pathValue) => {
      const cleanPath = normalizePath(pathValue);
      const parts = cleanPath ? cleanPath.split("/") : [];
      const crumbs = [
        { label: "/", path: "" },
        ...parts.map((part, index) => ({
          label: part,
          path: parts.slice(0, index + 1).join("/"),
        })),
      ];

      elements.breadcrumbs.innerHTML = crumbs.map((crumb, index) => {
        const active = index === crumbs.length - 1 ? " is-active" : "";
        return `<span class="crumb${active}" data-path="${escapeHtml(crumb.path)}">${escapeHtml(crumb.label)}</span>`;
      }).join("");

      elements.breadcrumbs.querySelectorAll(".crumb").forEach((crumb) => {
        crumb.addEventListener("click", () => {
          state.path = crumb.dataset.path || "";
          loadDirectory();
        });
      });
    };

    const renderEntries = () => {
      const searchValue = state.search.trim().toLowerCase();
      const visibleEntries = state.entries.filter((entry) => {
        if (!searchValue) return true;
        return String(entry.name || "").toLowerCase().includes(searchValue);
      });

      elements.statCount.textContent = String(visibleEntries.length);
      elements.fileList.innerHTML = "";
      elements.emptyState.hidden = visibleEntries.length > 0;

      visibleEntries.forEach((entry) => {
        const row = document.createElement("tr");

        const nameCell = document.createElement("td");
        nameCell.setAttribute("data-label", "名称 / Name");
        nameCell.innerHTML = `
          <div class="file-name">
            <strong>${escapeHtml(entry.name || "")}</strong>
            <span>${escapeHtml(entry.kind || "file")}</span>
          </div>
        `;

        const sizeCell = document.createElement("td");
        sizeCell.setAttribute("data-label", "大小 / Size");
        sizeCell.textContent = entry.kind === "directory" ? "—" : formatBytes(entry.size || 0);

        const modifiedCell = document.createElement("td");
        modifiedCell.setAttribute("data-label", "修改时间 / Modified");
        modifiedCell.textContent = formatDate(entry.modified);

        const actionsCell = document.createElement("td");
        actionsCell.setAttribute("data-label", "操作 / Actions");
        const actions = document.createElement("div");
        actions.className = "file-actions";

        if (entry.kind === "directory") {
          const openButton = document.createElement("button");
          openButton.type = "button";
          openButton.textContent = "打开";
          openButton.addEventListener("click", () => {
            state.path = joinPath(state.path, entry.name || "");
            loadDirectory();
          });
          actions.appendChild(openButton);
        } else {
          const downloadLink = document.createElement("a");
          downloadLink.textContent = "下载";
          downloadLink.href = `/api/download?path=${encodeURIComponent(joinPath(state.path, entry.name || ""))}`;
          downloadLink.target = "_blank";
          downloadLink.rel = "noreferrer noopener";
          actions.appendChild(downloadLink);
        }

        const deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.textContent = "删除";
        deleteButton.addEventListener("click", async () => {
          const fullPath = joinPath(state.path, entry.name || "");
          const confirmed = window.confirm(entry.kind === "directory"
            ? `确定删除文件夹「${entry.name}」及其全部内容吗？`
            : `确定删除文件「${entry.name}」吗？`);
          if (!confirmed) return;

          try {
            await apiRequest("/api/delete", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ path: fullPath }),
            });
            setStatus(`已删除: ${escapeHtml(entry.name || "")}`, "success");
            await loadDirectory();
          } catch (error) {
            setStatus(`删除失败: ${escapeHtml(error.message)}`, "error");
          }
        });
        actions.appendChild(deleteButton);

        actionsCell.appendChild(actions);

        row.append(nameCell, sizeCell, modifiedCell, actionsCell);
        elements.fileList.appendChild(row);
      });

      if (!visibleEntries.length) {
        elements.emptyState.hidden = false;
      }
    };

    const uploadFiles = async (fileList) => {
      const files = Array.from(fileList || []);
      if (!files.length) return;

      const uploadPassword = elements.uploadPassword.value.trim();
      if (!uploadPassword) {
        setStatus("请输入上传密码 / Please enter the upload password", "error");
        return;
      }

      setStatus(`<span class="loader" aria-hidden="true"></span><span>正在上传 ${files.length} 个文件 / Uploading ${files.length} files...</span>`);

      for (const file of files) {
        const formData = new FormData();
        formData.append("file", file, file.name);

        try {
          await apiRequest(`/api/upload?path=${encodeURIComponent(state.path)}`, {
            method: "POST",
            headers: {
              "X-Upload-Password": uploadPassword,
            },
            body: formData,
          });
        } catch (error) {
          setStatus(`上传失败: ${escapeHtml(file.name)} - ${escapeHtml(error.message)}`, "error");
          return;
        }
      }

      setStatus(`上传完成: ${files.length} 个文件`, "success");
      await loadDirectory();
    };

    const createFolder = async () => {
      const folderName = elements.folderName.value.trim();
      if (!folderName) {
        setStatus("请输入文件夹名称", "error");
        return;
      }

      try {
        await apiRequest("/api/mkdir", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            path: state.path,
            name: folderName,
          }),
        });
        elements.folderName.value = "";
        setStatus(`已创建文件夹: ${escapeHtml(folderName)}`, "success");
        await loadDirectory();
      } catch (error) {
        setStatus(`创建失败: ${escapeHtml(error.message)}`, "error");
      }
    };

    const wireEvents = () => {
      elements.fileInput.addEventListener("change", async (event) => {
        await uploadFiles(event.target.files);
        event.target.value = "";
      });

      elements.dropzone.addEventListener("click", () => elements.fileInput.click());
      elements.dropzone.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          elements.fileInput.click();
        }
      });

      elements.dropzone.addEventListener("dragover", (event) => {
        event.preventDefault();
        elements.dropzone.classList.add("is-dragover");
      });

      elements.dropzone.addEventListener("dragleave", () => {
        elements.dropzone.classList.remove("is-dragover");
      });

      elements.dropzone.addEventListener("drop", async (event) => {
        event.preventDefault();
        elements.dropzone.classList.remove("is-dragover");
        await uploadFiles(event.dataTransfer.files);
      });

      elements.refreshList.addEventListener("click", loadDirectory);
      elements.goRoot.addEventListener("click", () => {
        state.path = "";
        loadDirectory();
      });
      elements.createFolder.addEventListener("click", createFolder);

      elements.search.addEventListener("input", () => {
        state.search = elements.search.value;
        renderEntries();
      });
    };

    const init = async () => {
      elements.statUsed = document.getElementById("stat-used");
      elements.statFree = document.getElementById("stat-free");
      elements.statCount = document.getElementById("stat-count");
      elements.folderName = document.getElementById("folder-name");
      elements.uploadPassword = document.getElementById("upload-password");
      elements.saveUploadPassword = document.getElementById("save-upload-password");
      elements.createFolder = document.getElementById("create-folder");
      elements.dropzone = document.getElementById("dropzone");
      elements.fileInput = document.getElementById("file-input");
      elements.goRoot = document.getElementById("go-root");
      elements.refreshList = document.getElementById("refresh-list");
      elements.breadcrumbs = document.getElementById("breadcrumbs");
      elements.search = document.getElementById("search");
      elements.status = document.getElementById("status");
      elements.fileList = document.getElementById("file-list");
      elements.emptyState = document.getElementById("empty-state");

      wireEvents();
      elements.uploadPassword.value = sessionStorage.getItem("cloudDriveUploadPassword") || "";
      elements.saveUploadPassword.addEventListener("click", () => {
        sessionStorage.setItem("cloudDriveUploadPassword", elements.uploadPassword.value.trim());
        setStatus("上传密码已保存到当前浏览器会话", "success");
      });
      renderBreadcrumbs("");
      await loadDirectory();
    };

    document.addEventListener("DOMContentLoaded", () => {
      init().catch((error) => {
        setStatus(`初始化失败: ${escapeHtml(error.message)}`, "error");
      });
    });
  </script>
</body>
</html>
"""


class CloudDriveHandler(BaseHTTPRequestHandler):
    server_version = "CloudDrive/1.0"

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Upload-Password")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def do_GET(self) -> None:
        path, query = parse_query(self.path)

        if path in {"/", "/index.html"}:
            send_html(self, HTTPStatus.OK, APP_HTML)
            return

        if path == "/health":
            usage = shutil.disk_usage(ROOT)
            send_json(
                self,
                HTTPStatus.OK,
                {
                    "ok": True,
                    "storage": {
                        "root": str(ROOT),
                        "total_bytes": usage.total,
                        "used_bytes": usage.used,
                        "free_bytes": usage.free,
                    },
                },
            )
            return

        if path == "/api/list":
            try:
                folder = resolve_inside_root(get_query_value(query, "path"))
                if not folder.exists() or not folder.is_dir():
                    raise FileNotFoundError
                usage = shutil.disk_usage(ROOT)
                send_json(
                    self,
                    HTTPStatus.OK,
                    {
                        "ok": True,
                        "path": relative_path(folder.relative_to(ROOT).as_posix()),
                        "parent": parent_relative_path(folder.relative_to(ROOT).as_posix()),
                        "entries": list_directory(folder),
                        "storage": {
                            "root": str(ROOT),
                            "total_bytes": usage.total,
                            "used_bytes": usage.used,
                            "free_bytes": usage.free,
                        },
                    },
                )
            except FileNotFoundError:
                send_json(self, HTTPStatus.NOT_FOUND, {"ok": False, "error": "目录不存在"})
            except Exception as error:
                send_json(self, HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(error)})
            return

        if path == "/api/download":
            try:
                file_path = resolve_inside_root(get_query_value(query, "path"))
                if not file_path.is_file():
                    raise FileNotFoundError

                guessed_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
                encoded_name = quote(file_path.name)

                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", guessed_type)
                self.send_header("Content-Disposition", f"attachment; filename*=UTF-8''{encoded_name}")
                self.send_header("Content-Length", str(file_path.stat().st_size))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Cache-Control", "no-store")
                self.end_headers()

                with file_path.open("rb") as file_handle:
                    shutil.copyfileobj(file_handle, self.wfile, length=1024 * 1024)
            except FileNotFoundError:
                send_json(self, HTTPStatus.NOT_FOUND, {"ok": False, "error": "文件不存在"})
            except Exception as error:
                send_json(self, HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(error)})
            return

        send_json(self, HTTPStatus.NOT_FOUND, {"ok": False, "error": "未找到资源"})

    def do_POST(self) -> None:
        path, query = parse_query(self.path)

        if path == "/api/upload":
            try:
                provided_password = self.headers.get("X-Upload-Password", "")
                if provided_password != UPLOAD_PASSWORD:
                    send_json(self, HTTPStatus.UNAUTHORIZED, {"ok": False, "error": "上传密码错误"})
                    return

                folder = resolve_inside_root(get_query_value(query, "path"))
                if not folder.exists() or not folder.is_dir():
                    raise FileNotFoundError("目标目录不存在")

                content_type = self.headers.get_content_type()
                if not content_type.startswith("multipart/form-data"):
                    raise ValueError("上传接口只接受 multipart/form-data")

                environ = {
                    "REQUEST_METHOD": "POST",
                    "CONTENT_TYPE": self.headers.get("Content-Type", ""),
                    "CONTENT_LENGTH": self.headers.get("Content-Length", "0"),
                }
                form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ=environ, keep_blank_values=True)
                fields = form["file"] if "file" in form else []
                if not isinstance(fields, list):
                    fields = [fields]

                uploaded: list[dict[str, object]] = []
                for field in fields:
                    filename = safe_name(field.filename or "")
                    destination = make_unique_path(folder / filename)
                    with destination.open("wb") as destination_handle:
                        shutil.copyfileobj(field.file, destination_handle, length=1024 * 1024)
                    uploaded.append(file_metadata(destination))

                send_json(self, HTTPStatus.OK, {"ok": True, "uploaded": uploaded})
            except Exception as error:
                send_json(self, HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(error)})
            return

        if path == "/api/mkdir":
            try:
                payload = request_json(self)
                folder = resolve_inside_root(str(payload.get("path", "")))
                if not folder.exists() or not folder.is_dir():
                    raise FileNotFoundError("目标目录不存在")

                name = safe_name(str(payload.get("name", "")))
                new_folder = folder / name
                new_folder.mkdir(parents=True, exist_ok=False)

                send_json(self, HTTPStatus.OK, {"ok": True, "entry": file_metadata(new_folder)})
            except FileExistsError:
                send_json(self, HTTPStatus.CONFLICT, {"ok": False, "error": "文件夹已存在"})
            except Exception as error:
                send_json(self, HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(error)})
            return

        if path == "/api/delete":
            try:
                payload = request_json(self)
                target = resolve_inside_root(str(payload.get("path", "")))
                if target == ROOT:
                    raise ValueError("不允许删除根目录")

                if target.is_dir():
                    shutil.rmtree(target)
                elif target.exists():
                    target.unlink()
                else:
                    raise FileNotFoundError("目标不存在")

                send_json(self, HTTPStatus.OK, {"ok": True})
            except Exception as error:
                send_json(self, HTTPStatus.BAD_REQUEST, {"ok": False, "error": str(error)})
            return

        send_json(self, HTTPStatus.NOT_FOUND, {"ok": False, "error": "未找到资源"})

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        sys.stderr.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args))


def main() -> int:
    global ROOT

    parser = argparse.ArgumentParser(description="Cloud drive server")
    parser.add_argument("--host", default=os.environ.get("CLOUD_DRIVE_HOST", "127.0.0.1"))
    parser.add_argument("--port", default=int(os.environ.get("CLOUD_DRIVE_PORT", "8787")), type=int)
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args()
    ROOT = build_root(args.root)

    server = ThreadingHTTPServer((args.host, args.port), CloudDriveHandler)
    print(f"Cloud drive server listening on http://{args.host}:{args.port}")
    print(f"Storage root: {ROOT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())