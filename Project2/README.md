<div align="center">

# Digital Nexus

### A Cyberpunk-Style Personal Website & Portfolio

[![Vue 3](https://img.shields.io/badge/Vue-3-42b883?style=flat-square&logo=vue.js)](https://vuejs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat-square&logo=sqlite)](https://www.sqlite.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-38bdf8?style=flat-square&logo=tailwind-css)](https://tailwindcss.com/)

*A full-stack personal website featuring cyberpunk aesthetics, particle animations, and a complete content management system.*

**English** | [中文](README_CN.md)

</div>

---

## Features

| Feature | Description |
|---------|-------------|
| **Homepage** | Cyberpunk-themed hero with particle text animation, typewriter effect, and role carousel |
| **Photo Wall** | Photo gallery with drag-to-adjust positioning |
| **Portfolio** | Project showcase with admin management |
| **Toolbox** | Built-in developer tools (JSON, Base64, Regex, Hash, QR Code, etc.) |
| **Blog** | Markdown blog system with tags, likes, and search |
| **Resume** | Online resume editor |
| **Code Activity** | GitHub & Gitee contribution graphs and activity display |
| **Theme** | Dark/Light mode toggle with cyberpunk color scheme |
| **Admin** | Password-protected admin panel for content management |
| **Responsive** | Fully responsive design for all screen sizes |

## Quick Start

### Prerequisites

- **Python 3.9+**
- **Node.js 16+** and npm
- **Git**

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/digital-nexus.git
cd digital-nexus
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment configuration
cp .env.example .env
# Edit .env with your actual values (see Configuration section below)

# Initialize database (first run creates tables automatically)
python app.py
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Access the Website

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000/api

## Configuration

### Environment Variables

Copy `backend/.env.example` to `backend/.env` and configure:

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Flask secret key. Generate with: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `ADMIN_PASSWORD` | Yes | Admin panel password for managing content |
| `GITHUB_USERNAME` | No | Your GitHub username (for code activity display) |
| `GITHUB_TOKEN` | No | GitHub personal access token |
| `GITEE_USERNAME` | No | Your Gitee username (for code activity display) |
| `GITEE_TOKEN` | No | Gitee personal access token |

> **Security**: Never commit your `.env` file! It is already included in `.gitignore`.

### Optional: Seed Sample Data

```bash
cd backend

# Seed sample blog posts
python seed_blog.py

# Seed sample photos (requires actual images in uploads/images/)
python seed_photos.py
```

## Project Structure

```
digital-nexus/
├── backend/
│   ├── app.py              # Flask application entry point
│   ├── config.py           # Configuration management
│   ├── models.py           # SQLAlchemy database models
│   ├── requirements.txt    # Python dependencies
│   ├── resume.json         # Resume data (edit this for your info)
│   ├── .env.example        # Environment variable template
│   ├── seed_blog.py        # Sample blog data seeder
│   ├── seed_photos.py      # Sample photo data seeder
│   ├── instance/           # SQLite database (auto-created, git-ignored)
│   ├── routes/
│   │   ├── auth.py         # Admin authentication
│   │   ├── blog.py         # Blog CRUD API
│   │   ├── github.py       # GitHub/Gitee API proxy
│   │   ├── logs.py         # Visit & activity logs
│   │   ├── photos.py       # Photo management API
│   │   ├── portfolio.py    # Portfolio API
│   │   ├── resume.py       # Resume API
│   │   ├── stats.py        # Statistics API
│   │   └── tools.py        # File upload/download API
│   └── uploads/            # User uploads (git-ignored)
│       └── images/         # Photo storage
├── frontend/
│   ├── index.html          # HTML entry point
│   ├── package.json        # Node.js dependencies
│   ├── tailwind.config.js  # Tailwind CSS configuration
│   ├── vite.config.js      # Vite build configuration
│   └── src/
│       ├── App.vue         # Root component
│       ├── main.js         # Vue app initialization
│       ├── style.css       # Global styles
│       ├── components/     # Reusable components
│       ├── composables/    # Vue composables (API client)
│       ├── router/         # Vue Router configuration
│       └── views/          # Page components
│           ├── HomeView.vue
│           ├── BlogView.vue
│           ├── PortfolioView.vue
│           ├── ToolsView.vue
│           ├── ResumeView.vue
│           ├── CodeActivityView.vue
│           └── ...
└── README.md
```

## Customization

### Personal Information

1. **Resume**: Edit `backend/resume.json` with your actual information
2. **Homepage**: Modify `frontend/src/views/HomeView.vue` to change welcome text and role carousel
3. **Blog**: Use the admin panel or modify `seed_blog.py`
4. **Portfolio**: Add projects through the admin panel

### Branding

The default brand name is "Digital Nexus". To change it, search and replace in:
- `frontend/index.html` (page title)
- `frontend/src/components/Navbar.vue` (logo & brand)
- `frontend/src/components/Footer.vue` (copyright)
- `frontend/src/views/HomeView.vue` (hero section)

### Color Theme

Modify CSS variables in `frontend/src/style.css` to customize the cyberpunk color scheme:

```css
:root {
  --neon: #0ea5e9;        /* Primary accent color */
  --bg-primary: #0f172a;  /* Main background */
  --text-primary: #e2e8f0; /* Main text color */
}
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Vue 3 (Composition API), Tailwind CSS, Vite, Vue Router, Axios |
| **Backend** | Flask, SQLAlchemy, Flask-CORS |
| **Database** | SQLite (auto-created, zero config) |
| **Styling** | Cyberpunk theme with CSS variables, particle animations |
| **API** | RESTful API with JSON responses |

## Build for Production

```bash
# Build frontend
cd frontend
npm run build

# The built files will be in frontend/dist/
# Serve with any static file server or configure Flask to serve them
```

## License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**If you like this project, please give it a star!**

Made with love and lots of coffee

</div>
