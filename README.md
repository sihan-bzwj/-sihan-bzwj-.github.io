# 浜戠 AI 瀵硅瘽骞冲彴 + 涓汉浜戠洏 | Cloud AI Chat + Cloud Drive

> 涓€涓畬鏁寸殑 LobeChat 浜戦儴缃叉柟妗?+ Python 浜戠洏鏈嶅姟锛屾敮鎸佸涓?LLM 渚涘簲鍟嗗拰鏂囦欢瀛樺偍锛岄€氳繃 Cloudflare 闅ч亾 24/7 鍏綉璁块棶銆?>
> A complete LobeChat cloud deployment + Python cloud drive service supporting multiple LLM providers and file storage, with 24/7 public access via Cloudflare tunnel.

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Platform](https://img.shields.io/badge/Platform-Azure%20VM%20%2B%20Docker-blue)
![Tunnel](https://img.shields.io/badge/Tunnel-Cloudflare%20Quick-orange)        
![License](https://img.shields.io/badge/License-MIT-green)

---

## 馃幆 椤圭洰姒傝 | Project Overview

杩欐槸涓€涓?*瀹屾暣鐨勪簯绔湇鍔″钩鍙?*锛屾彁渚涗袱澶ф牳蹇冩湇鍔★細

A **complete cloud service platform** with two core services:

### 馃 AI 瀵硅瘽骞冲彴 (LobeChat)

- 鉁?**LobeChat** - 澶氭ā鍨?AI 瀵硅瘽骞冲彴锛圢ext.js + Node.js锛?| Multi-model AI chat platform (Next.js + Node.js)
- 鉁?**56+ LLM 渚涘簲鍟?* - OpenRouter銆丱penAI銆丄nthropic銆丏eepSeek 绛?| 56+ LLM providers including OpenRouter, OpenAI, Anthropic, DeepSeek, etc.
- 鉁?**鍔ㄦ€佹ā鍨嬭幏鍙?* - 鑷姩鍚屾鏈€鏂版ā鍨嬪垪琛?| Dynamic model fetching with automatic sync
- 鉁?**API 瀵嗛挜浠ｇ悊** - 瀹夊叏鐨勫悗绔唬鐞嗘灦鏋?| Secure backend API key proxy

### 馃捑 涓汉浜戠洏 (Cloud Drive)

- 鉁?**鏂囦欢绠＄悊** - 涓婁紶銆佷笅杞姐€佸垹闄ゃ€侀噸鍛藉悕鏂囦欢 | Upload, download, delete, rename files
- 鉁?**鐩綍鏍戠粨鏋?* - 瀹屾暣鐨勬枃浠跺す绠＄悊 | Complete directory tree management
- 鉁?**瀵嗙爜淇濇姢** - 鏀寔涓婁紶瀵嗙爜楠岃瘉 | Password-protected uploads
- 鉁?**Web 鍓嶇** - 缇庤鐨勫搷搴斿紡鐣岄潰 | Beautiful responsive web interface

### 馃寪 鏁翠綋鐗规€?| Overall Features

- 鉁?**24/7 鍏綉璁块棶** - Cloudflare 闅ч亾鑷姩鍖栭儴缃?| 24/7 public access via automated Cloudflare tunnel
- 鉁?**Landing Page** - GitHub Pages + MkDocs 椤圭洰浠嬬粛 | GitHub Pages + MkDocs project documentation
- 鉁?**瀹屽叏鑷姩鍖?* - systemd 鏈嶅姟鑷鐞嗐€丏ocker 鑷姩閲嶅惎 | Fully automated with systemd services and auto-restart
- 鉁?**鍙屾湇鍔￠儴缃?* - LobeChat + Cloud Drive 鍗忎綔杩愯 | Dual service deployment with collaboration

---

## 馃彈锔?绯荤粺鏋舵瀯 | System Architecture

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?        鐢ㄦ埛娴忚鍣?(Web 瀹㈡埛绔?                           鈹?鈹?        User Browser (Web Client)                       鈹?鈹?        鍥介檯鐢ㄦ埛 / 鍥藉唴鐢ㄦ埛 (International/CN Users)    鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                   鈹?HTTPS 璇锋眰 / HTTPS Requests
                   鈻?    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹?  Cloudflare Quick Tunnel        鈹?    鈹?  (鍥介檯闅ч亾 / Free, 24/7)        鈹?    鈹?raised-telling-ppm-notre...      鈹?    鈹?   trycloudflare.com             鈹?    鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                   鈹?HTTP 杞彂 / HTTP Forward
                   鈻?    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹?        Azure VM (Ubuntu 20.04)              鈹?    鈹?        杩愯 Docker 瀹瑰櫒 / Docker Containers  鈹?    鈹?                                             鈹?    鈹?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?     鈹?    鈹?  鈹? LobeChat    鈹?   鈹?Cloud Drive  鈹?     鈹?    鈹?  鈹? (3210 绔彛) 鈹?   鈹? (8787 绔彛) 鈹?     鈹?    鈹?  鈹?             鈹?   鈹?             鈹?     鈹?    鈹?  鈹?- Next.js    鈹?   鈹?- Python     鈹?     鈹?    鈹?  鈹?  鍓嶇       鈹?   鈹?  Backend    鈹?     鈹?    鈹?  鈹?- Node.js    鈹?   鈹?- Flask      鈹?     鈹?    鈹?  鈹?  鍚庣       鈹?   鈹?- Web UI     鈹?     鈹?    鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?     鈹?    鈹?        鈻?                   鈻?             鈹?    鈹?        鈹?API 璋冪敤            鈹?鏂囦欢 I/O    鈹?    鈹?        鈹?API Calls           鈹?File I/O    鈹?    鈹?        鈻?                   鈻?             鈹?    鈹?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?     鈹?    鈹?  鈹?    Persistent Storage Layer     鈹?     鈹?    鈹?  鈹?                                 鈹?     鈹?    鈹?  鈹? - /data/lobe-chat (LobeChat)    鈹?     鈹?    鈹?  鈹? - /data/cloud-drive (Files)     鈹?     鈹?    鈹?  鈹? - /etc/systemd (Services)       鈹?     鈹?    鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?     鈹?    鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                   鈹?                   鈹?缃戠粶璇锋眰 / Network Requests
                   鈻?    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹?  澶栭儴 LLM API 鏈嶅姟                   鈹?    鈹?  External LLM API Services          鈹?    鈹?                                     鈹?    鈹?- OpenAI (GPT-4, GPT-3.5)           鈹?    鈹?- Anthropic (Claude)                鈹?    鈹?- DeepSeek                          鈹?    鈹?- OpenRouter (Multi-providers)      鈹?    鈹?- 鍏朵粬 56+ 渚涘簲鍟?/ 56+ Providers  鈹?    鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

---

## 馃殌 蹇€熷紑濮?| Quick Start

### 璁块棶鍦板潃 | Access Addresses

| 鏈嶅姟 / Service | 鍦板潃 / URL | 璇存槑 / Description |
|---|---|---|
| **AI 瀵硅瘽骞冲彴** | https://raised-telling-ppm-notre.trycloudflare.com | LobeChat 涓荤晫闈?/ Main Interface |
| **涓汉浜戠洏** | https://raised-telling-ppm-notre.trycloudflare.com/cloud-drive | 鏂囦欢绠＄悊 / File Management |
| **椤圭洰鏂囨。** | https://github.com/sihan-bzwj/-sihan-bzwj-.github.io | GitHub 浠撳簱 / Repository |
| **椤圭洰涓婚〉** | https://sihan-bzwj.github.io | MkDocs 绔欑偣 / Documentation Site |

### AI 骞冲彴浣跨敤娴佺▼ | AI Chat Usage

1. **鎵撳紑 AI 绔欑偣** - 璁块棶涓婇潰鐨?URL | Open AI link above
2. **閫夋嫨妯″瀷渚涘簲鍟?* - 鍦ㄨ缃腑閫夋嫨 LLM 婧?| Select LLM provider in settings
3. **閰嶇疆 API 瀵嗛挜** - 杈撳叆瀵瑰簲渚涘簲鍟嗙殑 API 瀵嗛挜 | Enter API key for selected provider
4. **寮€濮嬪璇?* - 杈撳叆鎻愮ず璇嶅紑濮嬩笌 AI 浜掑姩 | Start chatting with AI

### 浜戠洏浣跨敤娴佺▼ | Cloud Drive Usage

1. **鎵撳紑浜戠洏** - 璁块棶 `/cloud-drive` 璺敱 | Access `/cloud-drive` route
2. **娴忚鏂囦欢** - 鏌ョ湅宸蹭笂浼犵殑鏂囦欢鍜岀洰褰?| Browse uploaded files and directories
3. **涓婁紶鏂囦欢** - 杈撳叆瀵嗙爜鍚庝笂浼犳柊鏂囦欢锛堥渶瑕佸瘑鐮侊級 | Upload files with password
4. **涓嬭浇鏂囦欢** - 閫夋嫨鏂囦欢鐩存帴涓嬭浇锛堟棤闇€瀵嗙爜锛?| Download files without password

---

## 馃挕 宸ヤ綔鍘熺悊 | How It Works

### AI 瀵硅瘽娴佺▼ | AI Chat Flow

```
鐢ㄦ埛杈撳叆 / User Input
       鈫?娴忚鍣ㄥ墠绔?/ Browser Frontend
       鈫?LobeChat 鍚庣 / LobeChat Backend
       鈫?API 瀵嗛挜楠岃瘉 / API Key Validation
       鈫?杞彂鍒?LLM API / Forward to LLM API
       鈫?鑾峰彇 AI 鍝嶅簲 / Get AI Response
       鈫?娴佸紡杩斿洖缁欏墠绔?/ Stream back to Frontend
       鈫?鐢ㄦ埛鐪嬪埌缁撴灉 / User sees result
```

**鍏抽敭鐗圭偣 | Key Points:**
- API 瀵嗛挜瀛樺偍鍦ㄥ悗绔紝娴忚鍣ㄧ鎺ユ敹涓嶅埌瀵嗛挜锛屾彁楂樺畨鍏ㄦ€?| API keys stored on backend, not exposed to browser - more secure
- 鏀寔娴佸紡鍝嶅簲锛屾彁鍗囩敤鎴蜂綋楠?| Streaming responses for better UX
- 鑷姩妯″瀷鍚屾湡锛屽缁堟敮鎸佹渶鏂版ā鍨?| Auto model sync with latest models

### 浜戠洏宸ヤ綔娴?| Cloud Drive Workflow

```
鐢ㄦ埛涓婁紶鏂囦欢 / User uploads file
       鈫?杈撳叆涓婁紶瀵嗙爜 / Enter upload password
       鈫?瀵嗙爜楠岃瘉 / Password verification
       鈫?鏂囦欢淇濆瓨鍒版湇鍔″櫒 / Save to server
       鈫?鍒楄〃鏇存柊 / Update file list
       
鐢ㄦ埛涓嬭浇鏂囦欢 / User downloads file
       鈫?鐩存帴涓嬭浇锛堟棤闇€瀵嗙爜锛?/ Direct download (no password)
       鈫?杩斿洖鏂囦欢鍐呭 / Return file content
```

**鐗规€?| Features:**
- 涓婁紶闇€瑕佸瘑鐮佷繚鎶わ紝涓嬭浇鏃犻檺鍒?| Uploads password-protected, downloads unrestricted
- 瀹屾暣鐨勭洰褰曟爲缁撴瀯鏀寔 | Full directory tree support
- 鏂囦欢鍏冩暟鎹鐞嗭紙澶у皬銆佹棩鏈熴€丮IME 绫诲瀷锛?| File metadata management

---

## 馃洜锔?鎶€鏈爤 | Tech Stack

### 鍓嶇 | Frontend

| 鎶€鏈?/ Technology | 鐢ㄩ€?/ Purpose | 鐗堟湰 / Version |
|---|---|---|
| **Next.js** | LobeChat 妗嗘灦 / Framework | v14+ |
| **React** | UI 缁勪欢 / UI Framework | v18+ |
| **TailwindCSS** | 鏍峰紡绯荤粺 / Styling | v3+ |
| **HTML5/CSS3** | 浜戠洏鍓嶇 / Cloud Drive UI | Latest |

### 鍚庣 | Backend

| 鎶€鏈?/ Technology | 鐢ㄩ€?/ Purpose | 鐗堟湰 / Version |
|---|---|---|
| **Node.js** | LobeChat 鍚庣 / Runtime | v18+ |
| **Python 3** | 浜戠洏鏈嶅姟 / Cloud Drive Server | 3.9+ |
| **Flask** | Web 妗嗘灦 / Web Framework | 2.0+ |
| **Docker** | 瀹瑰櫒鍖栭儴缃?/ Containerization | Latest |

### 閮ㄧ讲 | Deployment

| 鎶€鏈?/ Technology | 鐢ㄩ€?/ Purpose | 璇存槑 / Description |
|---|---|---|
| **Azure VM** | 浜戞湇鍔″櫒 / Cloud Server | Ubuntu 20.04 |
| **Cloudflare** | 缃戠粶闅ч亾 / Network Tunnel | Quick Tunnel (鍏嶈垂 / Free) |
| **systemd** | 鏈嶅姟绠＄悊 / Service Manager | Auto-restart & monitoring |
| **GitHub Actions** | CI/CD | 鏂囨。鑷姩閮ㄧ讲 / Auto-deploy docs |

---

## 鈿欙笍 閰嶇疆绀轰緥 | Configuration Examples

### LobeChat 鐜閰嶇疆 | LobeChat Env

```bash
# API 瀵嗛挜浠ｇ悊
OPENAI_API_KEY=sk-xxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxx
OPENROUTER_API_KEY=sk-or-xxxxxxx

# 鏈嶅姟閰嶇疆
NEXT_PUBLIC_BASE_PATH=/
NEXT_PUBLIC_API_BASE_URL=http://localhost:3210

# 瀛樺偍閰嶇疆
STORAGE_PATH=/data/lobe-chat
```

### Cloud Drive 鐜閰嶇疆 | Cloud Drive Env

```bash
# 鏈嶅姟閰嶇疆
UPLOAD_PASSWORD=your-secure-password
FILE_STORAGE_PATH=/data/cloud-drive
MAX_FILE_SIZE=10737418240  # 10GB

# 缃戠粶閰嶇疆
FLASK_HOST=0.0.0.0
FLASK_PORT=8787
FLASK_ENV=production
```

### Cloudflare 闅ч亾閰嶇疆 | Cloudflare Tunnel

```bash
# 浣跨敤 cloudflared CLI 鍒涘缓闅ч亾
cloudflared tunnel create sihan-blog
cloudflared tunnel route dns sihan-blog raised-telling-ppm-notre.trycloudflare.com
cloudflared tunnel config
```

---

## 馃搵 閮ㄧ讲宸ヤ綔娴?| Deployment Workflow

### 5 闃舵閰嶇疆娓呯偣 | 5-Stage Checklist

| 闃舵 / Stage | 浠诲姟 / Task | 瀹屾垚鐘舵€?/ Status |
|---|---|---|
| **1. 鐜鍑嗗** | Azure VM + Docker + systemd | 鉁?Ready |
| **2. 鏈嶅姟閮ㄧ讲** | LobeChat + Cloud Drive | 鉁?Running |
| **3. 闅ч亾閰嶇疆** | Cloudflare Quick Tunnel | 鉁?Active |
| **4. 鏂囨。绔欑偣** | GitHub Pages + MkDocs | 鉁?Deployed |
| **5. 鐩戞帶缁存姢** | systemd 鑷鐞?+ 鏃ュ織璁板綍 | 鉁?Monitored |

### 鍏抽敭杩愮淮鍛戒护 | Key Operations

```bash
# 閲嶅惎 LobeChat 鏈嶅姟
sudo systemctl restart lobe-chat.service

# 閲嶅惎 Cloud Drive 鏈嶅姟
sudo systemctl restart cloud-drive.service

# 鏌ョ湅 Cloudflare 闅ч亾鏃ュ織
cloudflared tunnel run sihan-blog

# 鏌ョ湅鏈嶅姟鐘舵€?sudo systemctl status lobe-chat.service
sudo systemctl status cloud-drive.service

# 鏌ョ湅 Docker 瀹瑰櫒鏃ュ織
docker logs lobe-chat -f
docker logs cloud-drive -f

# 閲嶅缓闈欐€佹枃妗?cd my-project && mkdocs build

# 鎺ㄩ€佹枃妗ｅ埌 GitHub
git add docs && git commit -m "docs: update" && git push
```

---

## 馃 鏀寔鐨?LLM 渚涘簲鍟?| Supported LLM Providers

### 涓绘祦渚涘簲鍟?| Major Providers

1. **OpenAI** - GPT-4, GPT-3.5 Turbo
2. **Anthropic** - Claude (Opus, Sonnet, Haiku)
3. **DeepSeek** - DeepSeek Chat, DeepSeek Code
4. **OpenRouter** - 澶氫釜妯″瀷鑱氬悎 / Model aggregation
5. **Google** - Gemini Pro
6. **Meta** - Llama 2
7. **Mistral** - Mistral 7B, Mixtral 8x7B

### 鍏朵粬鏀寔锛?6+锛墊 Other Providers (56+)

鍖呮嫭浣嗕笉闄愪簬 / Including but not limited to:
- Azure OpenAI
- Cohere
- Together AI
- Replicate
- Hugging Face
- 鏇村... / And more...

瀹屾暣鍒楄〃瑙?LobeChat 瀹樻柟鏂囨。 / See LobeChat official docs for complete list

---

## 馃摑 宸茬煡闄愬埗鍜屾敼杩涙柟鍚?| Known Limitations & Improvements

### 褰撳墠闄愬埗 | Current Limitations

- 鈿狅笍 **Cloudflare 鍏嶈垂闅ч亾** - 鍏嶈垂鐗堟湰姣忓ぉ鏈夋祦閲忛檺鍒讹紝鐢熶骇鐜寤鸿鍗囩骇 | Free tier has rate limits, upgrade for production
- 鈿狅笍 **鍗曟満閮ㄧ讲** - 褰撳墠鍙湁涓€涓?VM锛屾棤楂樺彲鐢ㄦ€ч厤缃?| Single VM deployment, no HA setup
- 鈿狅笍 **瀛樺偍瀹归噺** - 浜戠洏瀛樺偍渚濊禆 VM 纾佺洏澶у皬锛屾棤鍒嗗竷寮忓瓨鍌?| Storage limited by VM disk size
- 鈿狅笍 **API 瀵嗛挜绠＄悊** - 瀵嗛挜鐩墠瀛樺偍鍦ㄧ幆澧冨彉閲忎腑锛屽彲鑰冭檻瀵嗛挜绠＄悊绯荤粺 | Keys in env vars, could use secrets management

### 鏀硅繘鏂瑰悜 | Future Improvements

- 馃攧 **澶氬尯鍩熼儴缃?* - 鍦ㄥ涓湴鍖洪儴缃插壇鏈紝闄嶄綆寤惰繜 | Multi-region deployment for lower latency
- 馃攧 **鍒嗗竷寮忓瓨鍌?* - 浣跨敤 S3銆丱SS 绛夊璞″瓨鍌ㄦ浛浠ｆ湰鍦板瓨鍌?| Use S3/OSS for distributed storage
- 馃攧 **瀵嗛挜绠＄悊** - 闆嗘垚 HashiCorp Vault 鎴?AWS Secrets Manager | Integrate proper secrets management
- 馃攧 **鐩戞帶鍛婅** - 閮ㄧ讲 Prometheus + Grafana 鐩戞帶绯荤粺 | Add monitoring with Prometheus + Grafana
- 馃攧 **鑷姩鎵╁睍** - Kubernetes 缂栨帓鍜岃嚜鍔ㄦ墿灞?| Kubernetes orchestration with autoscaling
- 馃攧 **鏁版嵁澶囦唤** - 鑷姩澶囦唤绯荤粺锛屾敮鎸佺伨闅炬仮澶?| Automated backups and disaster recovery

---

## 馃敆 鐩稿叧閾炬帴 | Related Links

### 椤圭洰璧勬簮 | Project Resources

- 馃彔 **椤圭洰涓婚〉** | Project Homepage: https://github.com/sihan-bzwj/-sihan-bzwj-.github.io
- 馃摉 **鏂囨。绔欑偣** | Documentation: https://sihan-bzwj.github.io
- 馃 **AI 骞冲彴** | AI Chat: https://raised-telling-ppm-notre.trycloudflare.com
- 馃捑 **浜戠洏** | Cloud Drive: https://raised-telling-ppm-notre.trycloudflare.com/cloud-drive

### 鐩稿叧椤圭洰 | Related Projects

- **LobeChat** - https://github.com/lobehub/lobe-chat (AI 瀵硅瘽骞冲彴 / AI Chat Platform)
- **Cloudflare Tunnel** - https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/ (闅ч亾鏂囨。 / Tunnel Docs)
- **MkDocs Material** - https://squidfunk.github.io/mkdocs-material/ (鏂囨。涓婚 / Doc Theme)

### 瀛︿範璧勬簮 | Learning Resources

- 馃摎 LobeChat 鏂囨。: https://docs.lobehub.com/
- 馃摎 Cloudflare 鏂囨。: https://developers.cloudflare.com/
- 馃摎 Python Flask 鏂囨。: https://flask.palletsprojects.com/
- 馃摎 Docker 鏂囨。: https://docs.docker.com/

---

## 馃搫 璁稿彲璇?| License

鏈」鐩噰鐢?**MIT 璁稿彲璇?*銆傝瑙?[LICENSE](LICENSE) 鏂囦欢銆?
This project is licensed under the **MIT License**. See [LICENSE](LICENSE) file for details.

---

## 馃懁 浣滆€?| Author

**鎬濇兜 (Sihan)** - 椤圭洰缁存姢鑰?| Project Maintainer

- GitHub: https://github.com/sihan-bzwj
- Email: [Your Email]

---

## 馃挰 鍙嶉涓庢敮鎸?| Feedback & Support

濡傛湁闂銆佸缓璁垨鏀硅繘鎰忚锛屾杩庯細

Feel free to:

- 馃摑 鎻愪氦 Issue: https://github.com/sihan-bzwj/-sihan-bzwj-.github.io/issues
- 馃攢 鎻愪氦 Pull Request
- 馃拰 鍙戦€侀偖浠跺弽棣?
---

**鏈€鍚庢洿鏂?/ Last Updated**: 2026-04-05 | **鍒朵綔鑰?/ Made by**: Sihan 鉂わ笍
