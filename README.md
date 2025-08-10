# Vidalytics

> AI-powered YouTube analytics and content strategy platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)

Vidalytics is a modern YouTube analytics dashboard that helps content creators analyze performance, track insights, and optimize their content strategy with AI-powered recommendations.

## ✨ Features

- 📊 **Analytics Dashboard** - Comprehensive YouTube metrics with interactive charts
- 🎯 **Content Pillars** - Organize and track content themes and performance  
- 🤖 **AI Insights** - Intelligent analysis and optimization recommendations
- 📈 **Performance Tracking** - Monitor views, engagement, and subscriber growth
- 🎨 **Modern UI/UX** - Clean, responsive interface built with Nuxt 4
- 🔒 **Secure** - OAuth authentication and secure API handling

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ 
- Node.js 18+
- YouTube Data API key
- Google OAuth credentials

### Installation

```bash
# Clone repository
git clone https://github.com/DazB65/Vidalytics.git
cd Vidalytics

# Setup backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt

# Setup frontend
cd frontend-nuxt4
npm install
cd ..

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Development

```bash
# Terminal 1: Backend (Port 8000)
source venv/bin/activate
uvicorn backend.App.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend (Port 3000)  
cd frontend-nuxt4
npm run dev
```

**Access:** http://localhost:3000/dashboard

## 📖 Documentation

- **[Setup Guide](./docs/SetupGuide.md)** - Complete installation instructions
- **[API Documentation](./docs/API_DOCUMENTATION.md)** - Backend API reference
- **[Security Guide](./SECURITY.md)** - Security implementation details

## 🏗️ Architecture

```
├── backend/App/           # FastAPI backend application
├── frontend-nuxt4/        # Nuxt 4 frontend application  
├── docs/                  # Documentation
├── Vidalytics.db         # SQLite database (auto-created)
└── .env                  # Environment configuration
```

**Tech Stack:**
- **Backend:** FastAPI + Python + SQLite
- **Frontend:** Nuxt 4 + Vue 3 + TypeScript + Tailwind CSS
- **Database:** SQLite with performance indexes
- **APIs:** YouTube Data API v3, OpenAI API

## 🔧 Environment Variables

```env
# Required
YOUTUBE_API_KEY=your_youtube_api_key
GOOGLE_CLIENT_ID=your_google_client_id  
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Optional
OPENAI_API_KEY=your_openai_api_key
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- YouTube Data API for analytics data
- OpenAI for AI-powered insights
- Nuxt.js team for the amazing framework
- Tailwind CSS for beautiful styling

---

**Made with ❤️ for YouTube creators**
