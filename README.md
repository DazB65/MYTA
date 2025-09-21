# 🤖 MYTA - My YouTube Agent

**Your AI team for YouTube growth** - A sophisticated multi-agent system for strategic channel development and content optimization.

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/DazB65/Vidalytics)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![Node](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org)

## 🚀 Overview

MYTA is an advanced AI-powered platform that provides YouTube creators with a team of specialized AI agents to optimize their content strategy, analyze performance, and accelerate channel growth.

### ✨ Key Features

- 🤖 **Multi-Agent AI System** - 5 specialized agents working together
- 📊 **YouTube Analytics Integration** - Deep insights from YouTube Data API
- 🎯 **Content Strategy Optimization** - AI-driven content planning
- 🔍 **Competitive Analysis** - Track and analyze competitor performance
- 💰 **Monetization Strategies** - Revenue optimization recommendations
- 🎨 **Content Studio** - Kanban-style content management
- 📈 **Real-time Performance Monitoring** - Live analytics and alerts

### 🤖 AI Agent Team

1. **Boss Agent** - Orchestrates and coordinates all agents
2. **Content Analysis Agent** - Analyzes video performance and optimization
3. **Audience Insights Agent** - Deep audience behavior analysis
4. **SEO & Discoverability Agent** - Search optimization and algorithm insights
5. **Competitive Analysis Agent** - Market positioning and competitor tracking
6. **Monetization Strategy Agent** - Revenue optimization and growth strategies

## 🏗️ Architecture

```
MYTA/
├── backend/                 # FastAPI backend with AI agents
│   ├── App/                # Main application code
│   ├── database/           # Database migrations and schema
│   └── requirements.txt    # Python dependencies
├── frontend-nuxt4/         # Nuxt 4 frontend application
│   ├── app/               # Nuxt 4 app directory
│   ├── components/        # Vue components
│   ├── stores/           # Pinia state management
│   └── package.json      # Node.js dependencies
├── waitlist-only/         # Standalone waitlist application
├── dashboard/            # Analytics dashboard
├── docs/                # Comprehensive documentation
└── docker-compose.yml   # Container orchestration
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Redis (for session management)
- Docker & Docker Compose (recommended)

### 1. Clone Repository

```bash
git clone https://github.com/DazB65/Vidalytics.git
cd MYTA
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
# Required: OPENAI_API_KEY, GOOGLE_API_KEY, YOUTUBE_API_KEY
# Optional: ANTHROPIC_API_KEY, GEMINI_API_KEY
```

### 3. Docker Deployment (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Manual Setup

#### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn App.main:app --host 0.0.0.0 --port 8888
```

#### Frontend Setup

```bash
cd frontend-nuxt4
npm install
npm run dev
```

## 🔧 Configuration

### API Keys Required

1. **OpenAI API Key** - For GPT models
2. **Google API Key** - For YouTube Data API
3. **YouTube API Key** - For analytics (can be same as Google)
4. **Google OAuth** - Client ID and Secret for authentication

### Optional Integrations

- **Anthropic API** - For Claude models
- **Gemini API** - For Google's Gemini models
- **Stripe** - For payment processing
- **Supabase** - For enhanced database features

## 📊 Usage

1. **Connect YouTube Channel** - OAuth authentication with Google
2. **Agent Analysis** - AI agents analyze your channel and content
3. **Strategic Insights** - Receive personalized recommendations
4. **Content Planning** - Use Content Studio for content management
5. **Performance Tracking** - Monitor growth and optimization results

## 🛠️ Development

### Backend Development

```bash
cd backend
pip install -r requirements-dev.txt
python -m pytest tests/
```

### Frontend Development

```bash
cd frontend-nuxt4
npm run dev
npm run lint
npm run typecheck
```

### Database Management

```bash
cd backend
python App/manage_db.py migrate
python App/manage_db.py backup create
```

## 📚 Documentation

- [API Documentation](docs/API_DOCUMENTATION.md)
- [Security Guide](docs/SECURITY_IMPLEMENTATION.md)
- [Deployment Guide](docs/DOCKER.md)
- [Agent System](docs/BOSS_AGENT_SYSTEM.md)
- [Setup Guide](docs/SetupGuide.md)

## 🔒 Security

MYTA implements enterprise-grade security:

- JWT authentication with refresh tokens
- Rate limiting and CSRF protection
- Secure session management with Redis
- API key rotation and encryption
- Comprehensive audit logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 Email: support@myytagent.app
- 📖 Documentation: [docs/](docs/)
- 🐛 Issues: [GitHub Issues](https://github.com/DazB65/Vidalytics/issues)

---

**Built with ❤️ for YouTube creators worldwide**
