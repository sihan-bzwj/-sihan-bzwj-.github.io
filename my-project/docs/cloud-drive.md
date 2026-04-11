---
hide:
  - toc
---

<div class="editorial-page editorial-page--drive">
  <header class="site-nav" data-reveal>
    <div class="brand-lockup">
      <strong class="brand-mark">Sihan's Blog</strong>
    </div>
    <nav class="nav-links" aria-label="Cloud drive navigation">
      <a class="nav-link" href="../">Home</a>
      <a class="nav-link" href="#use">Use</a>
      <button class="theme-toggle" type="button" data-theme-toggle aria-label="Toggle theme">
        <span data-theme-label>Dark</span>
      </button>
      <a class="secondary-link" href="https://clouddrive.ccwu.cc/" target="_blank" rel="noreferrer noopener">Open Drive</a>
    </nav>
  </header>

  <section class="section-card hero-grid" data-reveal>
    <div class="hero-copy">
      <p class="eyebrow">Cloud Drive</p>
      <h1 class="hero-title">云盘</h1>
      <p class="hero-lead">
        这是一个长期在线的文件入口。它不复杂，也不打算变复杂：
        能浏览、能上传、能下载，偶尔也用来整理一些需要长期保留的内容。
      </p>
      <div class="cta-group">
        <a class="primary-link" href="https://clouddrive.ccwu.cc/" target="_blank" rel="noreferrer noopener">打开云盘</a>
        <a class="secondary-link" href="#use">查看说明</a>
      </div>
      <div class="status-row" aria-label="Drive status">
        <div class="status-pill">
          <strong>URL</strong>
          <span>clouddrive.ccwu.cc</span>
        </div>
        <div class="status-pill">
          <strong>Read</strong>
          <span>公开访问</span>
        </div>
        <div class="status-pill">
          <strong>Write</strong>
          <span>需要密码</span>
        </div>
      </div>
    </div>

    <aside class="surface-card" data-reveal>
      <span class="surface-card__eyebrow">Short Note</span>
      <h2 class="surface-card__title">给第一次使用的人</h2>
      <p class="surface-card__body">
        如果你只是来下载文件，直接进去就可以。上传和删除之所以需要密码，
        只是为了把它维持在一个足够稳定、也足够克制的状态。
      </p>
    </aside>
  </section>

  <section class="section-stack" id="use">
    <div class="section-card" data-reveal>
      <p class="eyebrow">What It Does</p>
      <h2 class="section-heading">现在能做的事</h2>
      <div class="chapter-divider" aria-hidden="true"></div>
      <div class="feature-grid">
        <article class="surface-card drive-feature-card">
          <span class="surface-card__eyebrow">Browse</span>
          <h3 class="surface-card__title">目录浏览</h3>
          <p class="surface-card__body">按层级查看文件和目录，适合直接找东西。</p>
        </article>

        <article class="surface-card drive-feature-card">
          <span class="surface-card__eyebrow">Upload</span>
          <h3 class="surface-card__title">文件上传</h3>
          <p class="surface-card__body">通过浏览器上传文件，服务端会避免重名覆盖。</p>
        </article>

        <article class="surface-card drive-feature-card">
          <span class="surface-card__eyebrow">Organize</span>
          <h3 class="surface-card__title">创建与删除</h3>
          <p class="surface-card__body">支持创建目录，也能删除文件或文件夹。</p>
        </article>

        <article class="surface-card drive-feature-card">
          <span class="surface-card__eyebrow">Download</span>
          <h3 class="surface-card__title">直接下载</h3>
          <p class="surface-card__body">下载链接始终被限制在存储根目录内。</p>
        </article>
      </div>
    </div>

    <div class="section-card section-card--dark" data-reveal>
      <p class="eyebrow">Access Rules</p>
      <h2 class="section-heading">一些必要的边界</h2>
      <div class="two-column-grid">
        <article class="surface-card">
          <span class="surface-card__eyebrow">Usage</span>
          <h3 class="surface-card__title">公开读取，谨慎写入</h3>
          <ul class="detail-list">
            <li>浏览和下载不需要密码。</li>
            <li>上传和删除需要服务端密码。</li>
            <li>文档页不再嵌入 iframe 预览，直接访问独立域名会更快。</li>
          </ul>
        </article>

        <article class="code-card">
          <span class="surface-card__eyebrow">Checks</span>
          <pre><code>sudo systemctl status cloud-drive.service --no-pager
sudo systemctl status caddy.service --no-pager
curl -I https://clouddrive.ccwu.cc/
curl https://clouddrive.ccwu.cc/health</code></pre>
        </article>
      </div>
    </div>
  </section>
</div>
