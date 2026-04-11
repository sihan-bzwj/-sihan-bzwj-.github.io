---
hide:
  - toc
---

<div class="editorial-page editorial-page--home">
  <header class="site-nav" data-reveal>
    <div class="brand-lockup">
      <strong class="brand-mark">Sihan's Cloud Notes</strong>
      <span class="brand-copy">暖色文档首页，集中保留仍在维护的公开入口。</span>
    </div>
    <nav class="nav-links" aria-label="Main navigation">
      <a class="nav-link" href="#entrypoints">入口</a>
      <a class="nav-link" href="#structure">结构</a>
      <a class="nav-link" href="cloud-drive/">云盘</a>
      <a class="secondary-link" href="https://github.com/sihan-bzwj/sihan-bzwj.github.io" target="_blank" rel="noreferrer noopener">GitHub</a>
    </nav>
  </header>

  <section class="section-card hero-grid" data-reveal>
    <div class="hero-copy">
      <p class="eyebrow">Editorial Home / 文档首页</p>
      <h1 class="hero-title">把公开入口整理成一页更适合阅读的纸感站点。</h1>
      <p class="hero-lead">
        这次重做只保留当前仍在运行的内容：云盘服务、部署文档和源码仓库。
        页面视觉遵循 <code>DESIGN.md</code> 的暖色编辑风，并将样式、页面和脚本按职责拆分。
      </p>
      <div class="cta-group">
        <a class="primary-link" href="cloud-drive/">打开云盘页面</a>
        <a class="secondary-link" href="#entrypoints">查看公开入口</a>
      </div>
      <div class="status-row" aria-label="Current status">
        <div class="status-pill">
          <strong>Cloud Drive</strong>
          <span>公开访问地址已上线</span>
        </div>
        <div class="status-pill">
          <strong>Docs Site</strong>
          <span>GitHub Pages 负责静态展示</span>
        </div>
        <div class="status-pill">
          <strong>Repository</strong>
          <span>源码与部署文件保持同步</span>
        </div>
      </div>
    </div>

    <aside class="hero-art" aria-hidden="true">
      <div class="hero-art__panel">
        <span class="hero-art__label">Now Maintained</span>
        <p class="hero-art__title">Docs, drive, and deployment notes.</p>
        <p class="hero-art__text">不再展示已经下线或无法维护的公共入口，信息层级也收缩为当前真实可用的服务。</p>
      </div>
      <div class="hero-art__note">
        <span class="hero-art__label">Design Direction</span>
        <p class="hero-art__text">暖纸色背景、衬线标题、低对比阴影和章节式深浅交替，全部直接对应设计说明。</p>
      </div>
      <svg class="hero-art__shape" viewBox="0 0 240 180" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M18 125C54 78 73 38 113 33C155 27 171 73 198 97C212 110 223 111 225 129C227 149 215 163 196 165C162 169 146 131 108 133C80 134 62 160 34 157C16 155 7 143 18 125Z" fill="currentColor" fill-opacity="0.16"/>
        <path d="M32 103C54 92 70 67 96 63C126 58 144 80 163 98C181 115 208 130 198 147C188 165 156 160 128 156C101 152 81 143 61 135C44 128 19 115 32 103Z" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
        <path d="M69 97C84 85 99 73 117 74C138 75 152 91 165 106" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
      </svg>
    </aside>
  </section>

  <section class="section-stack" id="entrypoints">
    <div class="section-card" data-reveal>
      <p class="eyebrow">Entry Points / 公开入口</p>
      <h2 class="section-heading">现在只保留真正需要被访问的三件事。</h2>
      <p class="section-summary">旧首页里偏“博客”和炫技的结构已经移除，当前页面只服务于导航、说明和运维信息的快速进入。</p>
      <div class="chapter-divider" aria-hidden="true"></div>
      <div class="three-column-grid">
        <article class="surface-card home-entry-card">
          <span class="surface-card__eyebrow">Cloud Drive</span>
          <h3 class="surface-card__title">文件入口</h3>
          <p class="surface-card__body">浏览、上传、下载、建目录和删除都由独立云盘服务承担，公共地址已固定。</p>
          <div class="chip-list">
            <span class="chip">storage</span>
            <span class="chip">upload</span>
            <span class="chip">download</span>
          </div>
          <a class="inline-link" href="cloud-drive/">进入云盘说明页面</a>
        </article>

        <article class="surface-card home-entry-card">
          <span class="surface-card__eyebrow">Documentation</span>
          <h3 class="surface-card__title">文档入口</h3>
          <p class="surface-card__body">GitHub Pages 负责静态说明页，内容集中展示现网结构、使用方式和后续维护指引。</p>
          <div class="chip-list">
            <span class="chip">mkdocs</span>
            <span class="chip">github pages</span>
          </div>
          <a class="inline-link" href="#structure">查看页面结构</a>
        </article>

        <article class="surface-card home-entry-card">
          <span class="surface-card__eyebrow">Source Repository</span>
          <h3 class="surface-card__title">源码入口</h3>
          <p class="surface-card__body">仓库里保留服务代码、systemd 文件、MkDocs 配置与本次重构后的站点资源模块。</p>
          <div class="chip-list">
            <span class="chip">python</span>
            <span class="chip">services</span>
            <span class="chip">docs</span>
          </div>
          <a class="inline-link" href="https://github.com/sihan-bzwj/sihan-bzwj.github.io" target="_blank" rel="noreferrer noopener">打开 GitHub 仓库</a>
        </article>
      </div>
    </div>

    <div class="section-card section-card--dark" data-reveal>
      <p class="eyebrow">Why Redesign / 重做原因</p>
      <h2 class="section-heading">从“深色科技感首页”收缩到“可长期维护的说明站”。</h2>
      <div class="timeline-grid">
        <article class="quote-card timeline-item">
          <span class="timeline-item__meta">Scope</span>
          <h3 class="timeline-item__title">删掉冗余展示</h3>
          <p class="timeline-item__body">移除了不再可靠的访客计数、iframe 预览和旧式博客入口，只留下清晰可验证的真实服务。</p>
        </article>
        <article class="quote-card timeline-item">
          <span class="timeline-item__meta">Design</span>
          <h3 class="timeline-item__title">统一暖色视觉</h3>
          <p class="timeline-item__body">整站改为纸张感背景、温暖中性色、衬线标题和低噪声卡片阴影，和 DESIGN.md 保持一致。</p>
        </article>
        <article class="quote-card timeline-item">
          <span class="timeline-item__meta">Code</span>
          <h3 class="timeline-item__title">拆分为独立模块</h3>
          <p class="timeline-item__body">配置、页面、字体、变量、基础样式、组件样式和动效脚本都按职责分开，方便继续维护。</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section-stack" id="structure">
    <div class="section-card" data-reveal>
      <p class="eyebrow">Structure / 结构说明</p>
      <h2 class="section-heading">前台页面更轻，后端职责没有被混进首页。</h2>
      <div class="two-column-grid">
        <article class="surface-card">
          <span class="surface-card__eyebrow">Site Modules</span>
          <h3 class="surface-card__title">文档站点资源</h3>
          <ul class="detail-list">
            <li><code>docs/index.md</code> 和 <code>docs/cloud-drive.md</code> 负责页面内容。</li>
            <li><code>stylesheets/*.css</code> 依次负责字体、变量、基础、组件和页面外观。</li>
            <li><code>javascripts/reveal.js</code> 只做滚动显现动画，不再绑定无效接口。</li>
          </ul>
        </article>

        <article class="surface-card">
          <span class="surface-card__eyebrow">Runtime Services</span>
          <h3 class="surface-card__title">实际运行中的服务</h3>
          <ul class="detail-list">
            <li><code>cloud_drive_server.py</code> 提供云盘 HTTP 服务。</li>
            <li><code>cloud_gateway.py</code> 保留网关和额外路由能力。</li>
            <li>GitHub Pages 只负责这套说明页，不直接承载文件服务。</li>
          </ul>
        </article>
      </div>
    </div>

    <div class="section-card" data-reveal>
      <p class="eyebrow">Quick Reference / 快速参考</p>
      <h2 class="section-heading">当前公开链接</h2>
      <div class="feature-grid">
        <article class="surface-card">
          <span class="surface-card__eyebrow">Drive URL</span>
          <h3 class="surface-card__title"><code>clouddrive.ccwu.cc</code></h3>
          <p class="surface-card__body">公共文件入口，适合直接访问、分享和下载。</p>
        </article>
        <article class="surface-card">
          <span class="surface-card__eyebrow">Docs URL</span>
          <h3 class="surface-card__title"><code>sihan-bzwj.github.io</code></h3>
          <p class="surface-card__body">文档站保留入口说明、部署结构和仓库导航。</p>
        </article>
      </div>
    </div>
  </section>
</div>
