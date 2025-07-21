# CreatorMate

CreatorMate is an AI-powered content creation platform for YouTube creators, featuring a sophisticated hierarchical multi-agent system for content analysis, audience insights, and strategic guidance.

## Features

- **Multi-Agent AI System**: Specialized AI agents for different aspects of content creation
- **Content Analysis**: Performance analysis, optimization suggestions, and trend identification
- **Audience Insights**: Demographics analysis, engagement patterns, and community health
- **SEO & Discoverability**: Keyword research and search optimization
- **Competitive Analysis**: Market positioning and competitor benchmarking
- **Monetization Strategy**: Revenue optimization and sponsorship opportunities

## Quick Start

1. **Setup Environment**:
   ```bash
   # Clone the repository
   git clone https://github.com/MyContentHub-DB/CreatorMate.git
   cd CreatorMate
   
   # Create environment file
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Start Development Server**:
   ```bash
   ./start-dev.sh
   ```

3. **Access the Application**:
   - Open http://localhost:8888 in your browser
   - Complete the onboarding flow
   - Start chatting with your AI assistant

## Development

### Prerequisites

- Python 3.9+
- Node.js 16+
- Git

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
YOUTUBE_API_KEY=your_youtube_api_key
BOSS_AGENT_SECRET_KEY=your_secret_key_for_agent_auth
```

### Architecture

- **Backend**: FastAPI with Python, hierarchical multi-agent system
- **Frontend**: React + TypeScript with Vite build system
- **Database**: SQLite for development, extensible to PostgreSQL
- **State Management**: Zustand for React state management

### Development Commands

```bash
# Backend development
cd backend
source ../venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8888

# Frontend development
cd frontend-new
npm run dev

# Build for production
cd frontend-new
npm run build
```

### Git Workflow

- Work on feature branches: `feature/[task-name]`
- Create PRs to `development` branch
- Merge `development` to `main` for production releases

## Documentation

- [CLAUDE.md](./CLAUDE.md) - Development workflow for Claude Code
- [Architecture Documentation](./docs/) - Detailed system architecture
- [API Documentation](./backend/docs/) - Backend API reference

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.