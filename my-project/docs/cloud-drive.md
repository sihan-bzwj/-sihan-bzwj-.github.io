# 云盘 / Cloud Drive

这个页面直接嵌入远程服务器上的云盘界面。文件会存到 Azure VM 的磁盘里，适合大文件上传、下载和长期保存。  
This page embeds the cloud drive running on the remote server. Files are stored on the Azure VM disk, which is suitable for large uploads, downloads, and long-term storage.

<style>
.drive-page {
  position: relative;
  margin: 1.5rem 0 0;
  padding: 0;
}

.drive-page::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: -2;
  background:
    radial-gradient(circle at 15% 15%, rgba(70, 140, 255, 0.24), transparent 32%),
    radial-gradient(circle at 85% 10%, rgba(39, 196, 180, 0.18), transparent 26%),
    radial-gradient(circle at 80% 86%, rgba(245, 158, 11, 0.12), transparent 24%),
    linear-gradient(180deg, #06111e 0%, #08131f 48%, #050b14 100%);
}

.drive-page::after {
  content: "";
  position: fixed;
  inset: 0;
  z-index: -1;
  background-image:
    linear-gradient(rgba(148, 163, 184, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(148, 163, 184, 0.06) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: linear-gradient(180deg, rgba(0, 0, 0, 0.8), transparent 85%);
}

.drive-hero {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: 1.4fr 0.9fr;
  align-items: start;
  margin-bottom: 1.25rem;
  padding: 1.8rem;
  border: 1px solid rgba(148, 163, 184, 0.18);
  border-radius: 28px;
  background: rgba(7, 14, 27, 0.78);
  backdrop-filter: blur(24px);
  box-shadow: 0 28px 70px rgba(0, 0, 0, 0.32);
}

.drive-kicker {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.8rem;
  border-radius: 999px;
  border: 1px solid rgba(96, 165, 250, 0.28);
  color: #b7d4ff;
  background: rgba(96, 165, 250, 0.09);
  font-size: 0.86rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.drive-hero h1 {
  margin: 0.85rem 0 0.7rem;
  font-size: clamp(2.2rem, 5vw, 4.8rem);
  line-height: 0.95;
  letter-spacing: -0.04em;
  color: #f5f7fb;
}

.drive-hero p {
  margin: 0;
  max-width: 66ch;
  color: rgba(226, 232, 240, 0.78);
  font-size: 1.02rem;
  line-height: 1.7;
}

.drive-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem;
  margin-top: 1rem;
}

.drive-tag {
  padding: 0.42rem 0.78rem;
  border-radius: 999px;
  background: rgba(148, 163, 184, 0.08);
  color: rgba(226, 232, 240, 0.88);
  border: 1px solid rgba(148, 163, 184, 0.15);
  font-size: 0.88rem;
}

.drive-note {
  display: grid;
  gap: 0.8rem;
  padding: 1.1rem;
  border-radius: 22px;
  background: linear-gradient(180deg, rgba(12, 20, 35, 0.96), rgba(8, 15, 28, 0.92));
  border: 1px solid rgba(148, 163, 184, 0.16);
}

.drive-note strong {
  display: block;
  font-size: 1rem;
  color: #f8fafc;
}

.drive-note span {
  color: rgba(226, 232, 240, 0.74);
  line-height: 1.65;
}

.drive-note a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: fit-content;
  margin-top: 0.3rem;
  padding: 0.8rem 1.1rem;
  border-radius: 14px;
  background: linear-gradient(135deg, #38bdf8, #0ea5e9);
  color: white !important;
  font-weight: 700;
  text-decoration: none !important;
  box-shadow: 0 16px 36px rgba(14, 165, 233, 0.35);
}

.drive-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr 1fr;
}

.drive-card {
  padding: 1.2rem;
  border-radius: 24px;
  background: rgba(8, 15, 28, 0.82);
  border: 1px solid rgba(148, 163, 184, 0.16);
  backdrop-filter: blur(16px);
  box-shadow: 0 20px 48px rgba(0, 0, 0, 0.22);
}

.drive-card h2 {
  margin: 0 0 0.8rem;
  font-size: 1.2rem;
  color: #f8fafc;
}

.drive-card ul {
  margin: 0;
  padding-left: 1.25rem;
  color: rgba(226, 232, 240, 0.76);
  line-height: 1.75;
}

.drive-frame {
  overflow: hidden;
  min-height: 78vh;
  border-radius: 20px;
  border: 1px solid rgba(148, 163, 184, 0.18);
  background: #08111d;
}

.drive-frame iframe {
  width: 100%;
  height: 78vh;
  border: 0;
  display: block;
  background: white;
}

.drive-card--wide {
  grid-column: 1 / -1;
}

@media (max-width: 960px) {
  .drive-hero,
  .drive-grid {
    grid-template-columns: 1fr;
  }

  .drive-frame,
  .drive-frame iframe {
    min-height: 68vh;
    height: 68vh;
  }
}
</style>

<div class="drive-page">
  <section class="drive-hero">
    <div>
      <span class="drive-kicker">Remote server backed storage</span>
      <h1>云盘 / Cloud Drive</h1>
      <p>上传、下载和文件管理都直接连接到你的远程服务器。这样空间更大，传输也更直接，适合备份、素材和大文件。</p>
      <div class="drive-tags">
        <span class="drive-tag">大空间 / More space</span>
        <span class="drive-tag">快速传输 / Fast transfers</span>
        <span class="drive-tag">远程服务器 / Remote VM</span>
      </div>
    </div>

    <aside class="drive-note">
      <strong>入口已就绪</strong>
      <span>下面的窗口会直接打开云盘界面。如果嵌入加载失败，可以用单独打开按钮进入。文件都保存在 Azure VM 上，不占用本地空间。</span>
      <a href="https://always-secrets-browsers-flights.trycloudflare.com" target="_blank" rel="noreferrer noopener">打开云盘 / Open Cloud Drive</a>
    </aside>
  </section>

  <section class="drive-grid">
    <article class="drive-card">
      <h2>使用方式 / How it works</h2>
      <ul>
        <li>云盘由远程服务器提供存储，适合更大的文件容量。</li>
        <li>上传和下载会直接走远程服务器，避免绕回本地。</li>
        <li>如果你需要更高安全性，后续可以再加登录口令。</li>
      </ul>
    </article>

    <article class="drive-card">
      <h2>访问提示 / Access tips</h2>
      <ul>
        <li>建议优先在桌面浏览器使用，拖拽上传更顺手。</li>
        <li>如果你更新了隧道地址，只需要替换这一页里的链接。</li>
        <li>这页是入口，真正的文件管理界面在远程服务器上运行。</li>
      </ul>
    </article>

    <article class="drive-card drive-card--wide">
      <div class="drive-frame">
        <iframe src="https://always-secrets-browsers-flights.trycloudflare.com" title="Cloud Drive" loading="lazy"></iframe>
      </div>
    </article>
  </section>
</div>