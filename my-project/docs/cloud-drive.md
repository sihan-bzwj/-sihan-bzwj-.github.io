---
hide:
  - toc
---

<div class="editorial-page editorial-page--drive">
  <header class="site-nav" data-reveal>
    <div class="brand-lockup">
      <strong class="brand-mark">Cloud Drive</strong>
      <span class="brand-copy">轻量文件服务的公开说明页，保留真实能力和访问方式。</span>
    </div>
    <nav class="nav-links" aria-label="Cloud drive navigation">
      <a class="nav-link" href="../">首页</a>
      <a class="nav-link" href="#features">功能</a>
      <a class="nav-link" href="#operations">维护</a>
      <a class="secondary-link" href="https://clouddrive.ccwu.cc/" target="_blank" rel="noreferrer noopener">Open Drive</a>
    </nav>
  </header>

  <section class="section-card hero-grid" data-reveal>
    <div class="hero-copy">
      <p class="eyebrow">Cloud Drive / 云盘服务</p>
      <h1 class="hero-title">一个专注文件管理的公开入口，不再夹带额外页面噪声。</h1>
      <p class="hero-lead">
        当前云盘页面只描述已经实装的能力：目录浏览、上传、下载、建目录和删除。
        页面也明确说明了权限边界，不再使用跨站 iframe 预览。
      </p>
      <div class="cta-group">
        <a class="primary-link" href="https://clouddrive.ccwu.cc/" target="_blank" rel="noreferrer noopener">直接打开云盘</a>
        <a class="secondary-link" href="../">返回首页</a>
      </div>
      <div class="status-row" aria-label="Drive status">
        <div class="status-pill">
          <strong>Public URL</strong>
          <span><code>https://clouddrive.ccwu.cc/</code></span>
        </div>
        <div class="status-pill">
          <strong>Upload & Delete</strong>
          <span>需要服务端密码</span>
        </div>
        <div class="status-pill">
          <strong>Browse & Download</strong>
          <span>公开访问即可使用</span>
        </div>
      </div>
    </div>

    <aside class="hero-art" aria-hidden="true">
      <div class="hero-art__panel">
        <span class="hero-art__label">Service Scope</span>
        <p class="hero-art__title">Only implemented features are listed.</p>
        <p class="hero-art__text">这里不再放“未来也许会做”的内容，页面说明与当前代码能力保持一一对应。</p>
      </div>
      <div class="hero-art__note">
        <span class="hero-art__label">Deployment</span>
        <p class="hero-art__text">云盘服务运行在 Azure VM，本页只是静态说明，访问时会直接跳转到独立域名。</p>
      </div>
      <svg class="hero-art__shape hero-art__shape--drive" viewBox="0 0 240 180" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M31 50C47 32 77 26 110 33C145 40 161 65 186 86C205 102 231 118 227 139C223 160 192 166 161 160C135 155 116 140 90 133C60 124 15 122 11 95C8 77 19 64 31 50Z" fill="currentColor" fill-opacity="0.15"/>
        <path d="M49 57C67 49 88 47 110 54C132 62 145 80 161 95C175 108 197 119 194 137C190 157 165 160 143 155C123 150 109 139 89 132C70 126 41 123 36 103C32 88 35 64 49 57Z" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
        <path d="M72 76H158" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
        <path d="M72 98H170" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
        <path d="M72 120H144" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
      </svg>
    </aside>
  </section>

  <section class="section-stack" id="features">
    <div class="section-card" data-reveal>
      <p class="eyebrow">Features / 当前能力</p>
      <h2 class="section-heading">页面只展示已在代码里完成的四类操作。</h2>
      <p class="section-summary">每项能力都对应现有后端逻辑，没有再用营销式文案去扩写未上线功能。</p>
      <div class="chapter-divider" aria-hidden="true"></div>
      <div class="feature-grid">
        <article class="surface-card drive-feature-card">
          <span class="surface-card__eyebrow">Browse</span>
          <h3 class="surface-card__title">目录浏览</h3>
          <p class="surface-card__body">按层级浏览文件和目录，目录优先显示，并可看到当前存储占用。</p>
          <div class="chip-list">
            <span class="chip">tree view</span>
            <span class="chip">storage stats</span>
          </div>
        </article>

        <article class="surface-card drive-feature-card">
          <span class="surface-card__eyebrow">Upload</span>
          <h3 class="surface-card__title">文件上传</h3>
          <p class="surface-card__body">支持通过浏览器上传文件，服务端会避免直接覆盖重名文件。</p>
          <div class="chip-list">
            <span class="chip">password protected</span>
            <span class="chip">duplicate-safe</span>
          </div>
        </article>

        <article class="surface-card drive-feature-card">
          <span class="surface-card__eyebrow">Organize</span>
          <h3 class="surface-card__title">建目录与删除</h3>
          <p class="surface-card__body">可创建目录并删除文件或文件夹，所有破坏性操作都需要密码确认。</p>
          <div class="chip-list">
            <span class="chip">folders</span>
            <span class="chip">protected delete</span>
          </div>
        </article>

        <article class="surface-card drive-feature-card">
          <span class="surface-card__eyebrow">Download</span>
          <h3 class="surface-card__title">直接下载</h3>
          <p class="surface-card__body">文件可直接下载，路径会被限制在云盘根目录之内，避免越界访问。</p>
          <div class="chip-list">
            <span class="chip">direct link</span>
            <span class="chip">path safety</span>
          </div>
        </article>
      </div>
    </div>

    <div class="section-card section-card--dark" data-reveal>
      <p class="eyebrow">Access & Safety / 访问与边界</p>
      <h2 class="section-heading">访问方式更直接，权限说明也更明确。</h2>
      <div class="three-column-grid">
        <article class="quote-card">
          <span class="surface-card__eyebrow">Direct Access</span>
          <h3 class="surface-card__title">不再嵌 iframe</h3>
          <p class="quote-card__body">跨站 iframe 容易引入慢加载和失败状态，所以文档页只保留按钮和域名说明，实际操作直接去独立站点。</p>
        </article>

        <article class="quote-card">
          <span class="surface-card__eyebrow">Password Rules</span>
          <h3 class="surface-card__title">只给危险操作加门槛</h3>
          <p class="quote-card__body">浏览和下载保持公开可用；上传和删除因为会改变存储内容，所以继续要求服务端密码。</p>
        </article>

        <article class="quote-card">
          <span class="surface-card__eyebrow">Deployment Path</span>
          <h3 class="surface-card__title">页面和服务分层部署</h3>
          <p class="quote-card__body">GitHub Pages 负责静态文档，Azure VM 上的 Python 服务负责真正的文件处理，两者职责不再混在一起。</p>
        </article>
      </div>
    </div>

    <div class="section-card" id="operations" data-reveal>
      <p class="eyebrow">Operations / 维护参考</p>
      <h2 class="section-heading">需要排查时，先看服务状态和健康检查。</h2>
      <div class="two-column-grid">
        <article class="surface-card">
          <span class="surface-card__eyebrow">Useful Checks</span>
          <h3 class="surface-card__title">优先确认的事实</h3>
          <ul class="detail-list">
            <li><code>cloud-drive.service</code> 是否处于 <code>active</code>。</li>
            <li><code>caddy.service</code> 是否仍在负责 <code>443</code> HTTPS。</li>
            <li><code>/health</code> 是否能正常返回。</li>
          </ul>
        </article>

        <article class="code-card">
          <span class="surface-card__eyebrow">Commands</span>
          <pre><code>sudo systemctl status cloud-drive.service --no-pager
sudo systemctl status caddy.service --no-pager
curl -I https://clouddrive.ccwu.cc/
curl https://clouddrive.ccwu.cc/health</code></pre>
        </article>
      </div>
    </div>
  </section>
</div>
