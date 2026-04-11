<div class="site-shell">
	<header class="topbar">
		<div class="brand">Sihan's Blog | 思涵的个人网站</div>
		<nav class="nav-pills" aria-label="Top navigation">
			<a class="pill" href="../">Home | 首页</a>
			<a class="pill" href="#drive">Drive | 云盘</a>
			<a class="pill" href="#features">Features | 功能</a>
			<a class="social-link" href="https://github.com/sihan-bzwj/sihan-bzwj.github.io" target="_blank" rel="noreferrer noopener">GitHub</a>
		</nav>
	</header>

	<section class="hero">
		<div class="hero-panel">
			<span class="kicker">Project / Service | 项目 / 服务</span>
			<h1 class="hero-title">云盘服务 | Cloud Drive</h1>
			<p class="hero-lead">浏览、上传、下载和整理文件的轻量云盘入口。| A lightweight browser-based drive for browsing, uploading, downloading, and organizing files.</p>
			<div class="hero-meta">
				<span class="meta-chip">storage</span>
				<span class="meta-chip">upload</span>
				<span class="meta-chip">download</span>
				<span class="meta-chip">folders</span>
			</div>
			<div class="hero-actions">
				<a class="button" href="https://clouddrive.ccwu.cc/" target="_blank" rel="noreferrer noopener">打开云盘 | Open Drive</a>
				<a class="button-secondary" href="../">回到首页 | Back Home</a>
			</div>
		</div>

		<aside class="side-panel">
			<h2>当前能力 | Current Scope</h2>
			<p>当前版本聚焦基础文件管理：目录浏览、上传、下载、建目录和删除。上传与删除都需要服务端密码。公开 AI 入口已移除，不再从这里跳转。| The current version focuses on core file management: browsing, upload, download, folder creation, and deletion. Upload and delete actions require the server-side password. The public AI entry has been removed and is no longer linked from here.</p>
			<div class="card-actions">
				<a class="button" href="https://clouddrive.ccwu.cc/" target="_blank" rel="noreferrer noopener">打开云盘 | Open</a>
				<a class="button-secondary" href="https://github.com/sihan-bzwj/sihan-bzwj.github.io" target="_blank" rel="noreferrer noopener">GitHub 源码 | Code</a>
			</div>
		</aside>
	</section>

	<section class="section" id="drive">
		<div class="section-header">
			<div>
				<h2>界面预览 | Interface Preview</h2>
				<p>下面直接嵌入当前云盘页面；如果 iframe 不稳定，使用上面的按钮直接打开即可。| The current cloud drive page is embedded below. If the iframe is unstable, open it directly with the button above.</p>
			</div>
		</div>

		<div class="frame-panel">
			<div class="frame-box">
				<iframe src="https://clouddrive.ccwu.cc/" title="Cloud Drive | 云盘" loading="lazy"></iframe>
			</div>
			<p class="frame-note">上传和删除需要输入密码，普通浏览和下载无需密码。| Upload and delete require a password, while browsing and downloading do not.</p>
		</div>
	</section>

	<section class="section" id="features">
		<div class="section-header">
			<div>
				<h2>功能特性 | Features</h2>
				<p>这里只展示当前已经在代码里实现的能力。| Only features that are implemented in the current codebase are listed here.</p>
			</div>
		</div>

		<div class="cards">
			<div class="card info-panel">
				<div class="card-header">
					<span class="kicker">Browse | 浏览</span>
					<h3>目录浏览 | Directory Browser</h3>
				</div>
				<p>支持按目录层级浏览文件，目录优先显示，并实时显示当前磁盘使用情况。| Browse files by folder hierarchy with directories listed first, plus live storage usage information.</p>
				<div class="tag-list">
					<span class="tag">tree view</span>
					<span class="tag">storage stats</span>
				</div>
			</div>

			<div class="card info-panel">
				<div class="card-header">
					<span class="kicker">Upload | 上传</span>
					<h3>文件上传 | File Upload</h3>
				</div>
				<p>支持拖拽或选择文件上传，服务端会自动避免重名覆盖。| Upload files by drag-and-drop or file picker, with automatic duplicate filename protection on the server.</p>
				<div class="tag-list">
					<span class="tag">password protected</span>
					<span class="tag">safe overwrite avoidance</span>
				</div>
			</div>

			<div class="card info-panel">
				<div class="card-header">
					<span class="kicker">Organize | 整理</span>
					<h3>目录创建与删除 | Create and Delete</h3>
				</div>
				<p>支持创建目录，删除文件或整个目录；删除操作同样需要密码确认。| Create folders and delete files or directories, with password protection for destructive actions.</p>
				<div class="tag-list">
					<span class="tag">folders</span>
					<span class="tag">protected delete</span>
				</div>
			</div>

			<div class="card info-panel">
				<div class="card-header">
					<span class="kicker">Download | 下载</span>
					<h3>直链下载 | Direct Download</h3>
				</div>
				<p>文件可直接下载，下载路径会被限制在云盘根目录内。| Files can be downloaded directly, and download paths are constrained to the storage root.</p>
				<div class="tag-list">
					<span class="tag">direct link</span>
					<span class="tag">path safety</span>
				</div>
			</div>
		</div>

		<footer class="site-footer" aria-label="网站统计">
			<div class="site-footer__item">
				<span class="site-footer__label">浏览人数统计 | Visitors</span>
				<strong class="site-footer__value" data-visitor-count>加载中</strong>
			</div>
			<div class="site-footer__item">
				<span class="site-footer__label">更新时间 | Updated</span>
				<strong class="site-footer__value">2026-04-11</strong>
			</div>
		</footer>
	</section>
</div>
