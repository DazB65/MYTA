# Vidalytics Setup Guide

Complete setup instructions for the Vidalytics YouTube analytics platform.

## Prerequisites

- **Python 3.9+** (recommended: 3.11)
- **Node.js 18+** (recommended: 20.x)
- **Git**
- **YouTube API access** (Google Cloud Console)
- **OpenAI API key** (optional, for AI features)

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/DazB65/Vidalytics.git
cd Vidalytics
```

### 2. Backend Setup

```bash
# Create Python virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r backend/requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend-nuxt4

# Install Node.js dependencies
npm install

# Return to project root
cd ..
```

### 4. Environment Configuration

```bash
# Create environment file
cp .env.example .env

# Edit .env file with your API keys
nano .env  # or use your preferred editor
```

Required environment variables:

```env
# OpenAI API (optional - for AI features)
OPENAI_API_KEY=your_openai_api_key_here

# YouTube Data API v3 (required for analytics)
YOUTUBE_API_KEY=your_youtube_api_key_here

# Google OAuth (required for YouTube authentication)
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
```

### 5. Database Setup

The SQLite database is automatically created with optimized indexes:

```bash
# Verify database structure (optional)
sqlite3 Vidalytics.db ".tables"
sqlite3 Vidalytics.db ".indexes"
```

## Development

### Start Development Servers

**Terminal 1 - Backend (Port 8000):**

```bash
source venv/bin/activate
uvicorn backend.App.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend (Port 3000):**

```bash
cd frontend-nuxt4
npm run dev
```

### Access the Application

- **Frontend Dashboard**: http://localhost:3000
- **Main Dashboard**: http://localhost:3000/dashboard
- **Backend API**: http://localhost:8000
- **API Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs

## API Keys Setup

### YouTube Data API v3

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Add the API key to your `.env` file

### Google OAuth (for YouTube Authentication)

1. In Google Cloud Console, go to "Credentials"
2. Create OAuth 2.0 Client ID
3. Set authorized redirect URIs:
   - `http://localhost:8000/auth/google/callback`
   - `http://localhost:3000/auth/callback`
4. Add Client ID and Secret to `.env`

### OpenAI API (Optional)

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create API key
3. Add to `.env` file

## Troubleshooting

### Common Issues

**Backend won't start:**

- Check Python virtual environment is activated
- Verify all dependencies installed: `pip install -r backend/requirements.txt`
- Check port 8000 is not in use

**Frontend won't start:**

- Check Node.js version: `node --version` (should be 18+)
- Clear node_modules: `rm -rf node_modules && npm install`
- Check port 3000 is not in use

**Cannot connect to server:**

- Ensure backend is running on port 8000
- Check firewall settings
- Verify API base URL in frontend configuration

**Database issues:**

- Database is created automatically
- Check file permissions in project directory
- Verify SQLite is available: `sqlite3 --version`

### Development Tips

- Use `npm run dev` for frontend hot reload
- Backend auto-reloads with `--reload` flag
- Check browser console for frontend errors
- Check terminal output for backend errors
- Use `/health` endpoint to verify backend status

## Production Deployment

For production deployment, see:

- [Docker Guide](./DOCKER.md)
- [Security Implementation](./SECURITY_IMPLEMENTATION.md)
- [CI/CD Guide](./CI-CD.md)
