<div align="center">

# Digital Nexus

### 个人网站 & 作品集

[![Vue 3](https://img.shields.io/badge/Vue-3-42b883?style=flat-square&logo=vue.js)](https://vuejs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat-square&logo=sqlite)](https://www.sqlite.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-38bdf8?style=flat-square&logo=tailwind-css)](https://tailwindcss.com/)

*一个全栈个人网站，具有赛博朋克美学、粒子动画和完整的内容管理系统。*

**[English](README.md)** | 中文

</div>

---

## 功能特性

| 功能 | 描述 |
|------|------|
| **首页** | 赛博朋克风格主页，包含粒子文字动画、打字机效果和角色轮播 |
| **照片墙** | 支持拖拽调整位置的照片画廊 |
| **作品集** | 项目展示，支持管理员管理 |
| **工具箱** | 内置开发者工具（JSON、Base64、正则表达式、哈希、二维码等） |
| **博客** | Markdown 博客系统，支持标签、点赞和搜索 |
| **简历** | 在线简历编辑器 |
| **代码活动** | GitHub & Gitee 贡献图和活动展示 |
| **主题** | 亮色/暗色模式切换，赛博朋克配色方案 |
| **管理后台** | 密码保护的管理面板，用于内容管理 |
| **响应式** | 全响应式设计，适配所有屏幕尺寸 |

## 快速开始

### 环境要求

- **Python 3.9+**
- **Node.js 16+** 和 npm
- **Git**

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/digital-nexus.git
cd digital-nexus
```

### 2. 后端配置

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建环境配置文件
cp .env.example .env
# 编辑 .env 文件，填入你的实际配置（参见下方配置说明）

# 初始化数据库（首次运行自动创建表）
python app.py
```

### 3. 前端配置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 4. 访问网站

- **前端**: http://localhost:5173
- **后端 API**: http://localhost:5000/api

## 配置说明

### 环境变量

将 `backend/.env.example` 复制为 `backend/.env` 并进行配置：

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `SECRET_KEY` | 是 | Flask 密钥。生成命令：`python -c "import secrets; print(secrets.token_hex(32))"` |
| `ADMIN_PASSWORD` | 是 | 管理面板密码，用于内容管理 |
| `GITHUB_USERNAME` | 否 | GitHub 用户名（用于代码活动展示） |
| `GITHUB_TOKEN` | 否 | GitHub 个人访问令牌 |
| `GITEE_USERNAME` | 否 | Gitee 用户名（用于代码活动展示） |
| `GITEE_TOKEN` | 否 | Gitee 个人访问令牌 |

> **安全提示**: 永远不要提交 `.env` 文件！它已被包含在 `.gitignore` 中。

### 可选：导入示例数据

```bash
cd backend

# 导入示例博客文章
python seed_blog.py

# 导入示例照片（需要在 uploads/images/ 中放置实际图片）
python seed_photos.py
```

## 项目结构

```
digital-nexus/
├── backend/
│   ├── app.py              # Flask 应用入口
│   ├── config.py           # 配置管理
│   ├── models.py           # SQLAlchemy 数据库模型
│   ├── requirements.txt    # Python 依赖
│   ├── resume.json         # 简历数据（编辑此文件填写你的信息）
│   ├── .env.example        # 环境变量模板
│   ├── seed_blog.py        # 示例博客数据脚本
│   ├── seed_photos.py      # 示例照片数据脚本
│   ├── instance/           # SQLite 数据库（自动创建，已忽略提交）
│   ├── routes/
│   │   ├── auth.py         # 管理员认证
│   │   ├── blog.py         # 博客 CRUD API
│   │   ├── github.py       # GitHub/Gitee API 代理
│   │   ├── logs.py         # 访问和活动日志
│   │   ├── photos.py       # 照片管理 API
│   │   ├── portfolio.py    # 作品集 API
│   │   ├── resume.py       # 简历 API
│   │   ├── stats.py        # 统计 API
│   │   └── tools.py        # 文件上传/下载 API
│   └── uploads/            # 用户上传文件（已忽略提交）
│       └── images/         # 照片存储
├── frontend/
│   ├── index.html          # HTML 入口文件
│   ├── package.json        # Node.js 依赖配置
│   ├── tailwind.config.js  # Tailwind CSS 配置
│   ├── vite.config.js      # Vite 构建配置
│   └── src/
│       ├── App.vue         # 根组件
│       ├── main.js         # Vue 应用初始化
│       ├── style.css       # 全局样式
│       ├── components/     # 可复用组件
│       ├── composables/    # Vue 组合式函数（API 客户端）
│       ├── router/         # Vue Router 路由配置
│       └── views/          # 页面组件
│           ├── HomeView.vue
│           ├── BlogView.vue
│           ├── PortfolioView.vue
│           ├── ToolsView.vue
│           ├── ResumeView.vue
│           ├── CodeActivityView.vue
│           └── ...
└── README.md
```

## 自定义指南

### 个人信息

1. **简历**: 编辑 `backend/resume.json` 填写你的实际信息
2. **首页**: 修改 `frontend/src/views/HomeView.vue` 更改欢迎文字和角色轮播
3. **博客**: 使用管理面板或修改 `seed_blog.py`
4. **作品集**: 通过管理面板添加项目

### 品牌名称

默认品牌名称为 "Digital Nexus"。如需修改，请在以下文件中搜索替换：
- `frontend/index.html`（页面标题）
- `frontend/src/components/Navbar.vue`（Logo 和品牌名）
- `frontend/src/components/Footer.vue`（版权信息）
- `frontend/src/views/HomeView.vue`（主视觉区域）

### 颜色主题

修改 `frontend/src/style.css` 中的 CSS 变量来自定义赛博朋克配色方案：

```css
:root {
  --neon: #0ea5e9;        /* 主色调 */
  --bg-primary: #0f172a;  /* 主背景色 */
  --text-primary: #e2e8f0; /* 主文字颜色 */
}
```

## 技术栈

| 层级 | 技术 |
|------|------|
| **前端** | Vue 3 (Composition API), Tailwind CSS, Vite, Vue Router, Axios |
| **后端** | Flask, SQLAlchemy, Flask-CORS |
| **数据库** | SQLite（自动创建，零配置） |
| **样式** | 赛博朋克主题，CSS 变量，粒子动画 |
| **API** | RESTful API，JSON 响应 |

## 生产环境构建

```bash
# 构建前端
cd frontend
npm run build

# 构建产物将输出到 frontend/dist/
# 可使用任意静态文件服务器部署，或配置 Flask 来托管这些文件
```

## 开源许可

本项目基于 [MIT 许可证](LICENSE) 开源。

---

<div align="center">

**如果喜欢这个项目，请给个 Star 支持一下！**

用爱和咖啡驱动

</div>
