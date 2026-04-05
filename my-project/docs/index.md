<style>
.home-shell {
	position: relative;
	overflow: hidden;
	margin-top: 0.5rem;
	padding: 2rem;
	border-radius: 28px;
	border: 1px solid rgba(148, 163, 184, 0.18);
	background:
		radial-gradient(circle at top left, rgba(56, 189, 248, 0.18), transparent 28%),
		radial-gradient(circle at top right, rgba(34, 197, 94, 0.12), transparent 22%),
		linear-gradient(180deg, rgba(7, 14, 27, 0.96), rgba(5, 10, 18, 0.92));
	box-shadow: 0 28px 70px rgba(0, 0, 0, 0.24);
}

.home-shell::after {
	content: "";
	position: absolute;
	inset: 0;
	background-image:
		linear-gradient(rgba(148, 163, 184, 0.06) 1px, transparent 1px),
		linear-gradient(90deg, rgba(148, 163, 184, 0.06) 1px, transparent 1px);
	background-size: 52px 52px;
	mask-image: linear-gradient(180deg, rgba(0, 0, 0, 0.72), transparent 88%);
	pointer-events: none;
}

.home-hero {
	position: relative;
	display: grid;
	gap: 1rem;
	grid-template-columns: 1.45fr 0.95fr;
	align-items: start;
	z-index: 1;
}

.home-kicker {
	display: inline-flex;
	align-items: center;
	gap: 0.45rem;
	padding: 0.35rem 0.75rem;
	border-radius: 999px;
	border: 1px solid rgba(96, 165, 250, 0.28);
	background: rgba(96, 165, 250, 0.09);
	color: #b7d4ff;
	font-size: 0.84rem;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.home-title {
	margin: 0.85rem 0 0.55rem;
	font-size: clamp(2.3rem, 5vw, 4.7rem);
	line-height: 0.95;
	letter-spacing: -0.05em;
	color: #f8fafc;
}

.home-lead {
	margin: 0;
	max-width: 64ch;
	color: rgba(226, 232, 240, 0.78);
	line-height: 1.75;
	font-size: 1.02rem;
}

.home-actions {
	display: flex;
	flex-wrap: wrap;
	gap: 0.75rem;
	margin-top: 1.15rem;
}

.home-button,
.home-button-secondary {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	min-height: 3rem;
	padding: 0.8rem 1.1rem;
	border-radius: 14px;
	text-decoration: none !important;
	font-weight: 700;
}

.home-button {
	background: linear-gradient(135deg, #38bdf8, #0ea5e9);
	color: white !important;
	box-shadow: 0 16px 36px rgba(14, 165, 233, 0.32);
}

.home-button-secondary {
	background: rgba(148, 163, 184, 0.09);
	border: 1px solid rgba(148, 163, 184, 0.16);
	color: rgba(248, 250, 252, 0.92) !important;
}

.home-card-grid {
	position: relative;
	z-index: 1;
	display: grid;
	gap: 0.9rem;
}

.home-card {
	padding: 1rem;
	border-radius: 20px;
	border: 1px solid rgba(148, 163, 184, 0.14);
	background: rgba(8, 15, 28, 0.78);
}

.home-card strong {
	display: block;
	margin-bottom: 0.35rem;
	color: #f8fafc;
}

.home-card p {
	margin: 0;
	color: rgba(226, 232, 240, 0.74);
	line-height: 1.65;
}

.home-link-note {
	margin: 0.95rem 0 0;
	color: rgba(226, 232, 240, 0.82);
	line-height: 1.7;
}

.home-link-note a {
	color: #8fd3ff;
	font-weight: 700;
	text-decoration: none;
}

.home-link-note a:hover {
	text-decoration: underline;
}

.home-strip {
	position: relative;
	z-index: 1;
	display: grid;
	gap: 1rem;
	grid-template-columns: repeat(3, minmax(0, 1fr));
	margin-top: 1rem;
}

.home-strip-item {
	padding: 1rem;
	border-radius: 18px;
	border: 1px solid rgba(148, 163, 184, 0.14);
	background: rgba(8, 15, 28, 0.72);
	color: rgba(226, 232, 240, 0.78);
	line-height: 1.7;
}

@media (max-width: 860px) {
	.home-hero,
	.home-strip {
		grid-template-columns: 1fr;
	}

	.home-shell {
		padding: 1.2rem;
	}
}
</style>

<div class="home-shell">
	<div class="home-hero">
		<div>
			<span class="home-kicker">Remote access hub</span>
			<h1 class="home-title">LobeChat 入口 / Home</h1>
			<p class="home-lead">这是你的站点入口，同时接入了一个跑在远程服务器上的云盘。LobeChat 负责对话入口，云盘负责大文件上传、下载和长期保存，两者都可以直接从这个首页进入。</p>

			<div class="home-actions">
				<a class="home-button" href="https://raised-telling-ppm-notre.trycloudflare.com">打开 LobeChat / Open LobeChat</a>
				<a class="home-button-secondary" href="cloud-drive/">打开云盘 / Open Cloud Drive</a>
			</div>
			<p class="home-link-note">云盘直达链接：<a href="cloud-drive/">cloud-drive/</a>，也可以从顶部导航直接进入。</p>
		</div>
		<div class="home-card-grid">
			<div class="home-card">
				<strong>云盘状态 / Drive</strong>
				<p>云盘已经接到 Azure VM，上线后会自动使用远程存储。适合大空间、快速下载和持续备份。</p>
			</div>
			<div class="home-card">
				<strong>访问方式 / Access</strong>
				<p>如果云盘地址变化，只要更新 [cloud-drive.md](cloud-drive.md) 就能同步到首页和生成站点。</p>
			</div>
		</div>
	</div>

	<div class="home-strip">
		<div class="home-strip-item">远程服务器 / Remote VM：文件存储在 Azure VM，空间和读写都比本地浏览器更适合做网盘。</div>
		<div class="home-strip-item">快速入口 / Fast entry：主页只保留两个主动作，避免用户在一堆文本里找链接。</div>
		<div class="home-strip-item">可持续维护 / Maintainable：页面结构和实现说明分开，后续改隧道或后端不会影响首页布局。</div>
	</div>
</div>
