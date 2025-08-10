# Vidalytics

Vidalytics is an AI-powered YouTube analytics and content strategy platform, featuring a modern dashboard for content creators to analyze performance, track insights, and optimize their content strategy.

## Features

- **Analytics Dashboard**: Comprehensive YouTube analytics with interactive charts and metrics
- **Content Pillars**: Organize and track content themes and performance
- **AI-Powered Insights**: Intelligent analysis and recommendations for content optimization
- **Performance Tracking**: Monitor views, engagement, subscriber growth, and retention
- **Content Strategy**: Plan and optimize content based on data-driven insights
- **Modern UI/UX**: Clean, responsive interface built with Nuxt 4 and Tailwind CSS

## Quick Start

1. **Setup Environment**:

   ```bash
   # Clone the repository
   git clone https://github.com/DazB65/Vidalytics.git
   cd Vidalytics

   # Create Python virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install backend dependencies
   pip install -r backend/requirements.txt

   # Install frontend dependencies
   cd frontend-nuxt4
   npm install
   cd ..
   ```

2. **Configure Environment**:

   ```bash
   # Create environment file
   cp .env.example .env
   # Edit .env with your API keys:
   # OPENAI_API_KEY=your_openai_api_key
   # YOUTUBE_API_KEY=your_youtube_api_key
   ```

3. **Start Development Servers**:

   ```bash
   # Terminal 1: Start Backend (Port 8000)
   source venv/bin/activate
   uvicorn backend.App.main:app --reload --host 0.0.0.0 --port 8000

   # Terminal 2: Start Frontend (Port 3000)
   cd frontend-nuxt4
   npm run dev
   ```

4. **Access the Application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Dashboard: http://localhost:3000/dashboard

## Development

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
YOUTUBE_API_KEY=your_youtube_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

### Architecture

- **Backend**: FastAPI with Python, SQLite database with performance indexes
- **Frontend**: Nuxt 4 with Vue 3, TypeScript, and Tailwind CSS
- **Database**: SQLite for development (optimized with indexes)
- **State Management**: Nuxt composables and reactive state
- **Styling**: Tailwind CSS with custom components

### Development Commands

```bash
# Backend development
source venv/bin/activate
uvicorn backend.App.main:app --reload --host 0.0.0.0 --port 8000

# Frontend development
cd frontend-nuxt4
npm run dev

# Build for production
cd frontend-nuxt4
npm run build

# Database operations
sqlite3 Vidalytics.db ".tables"  # View tables
sqlite3 Vidalytics.db ".indexes"  # View indexes
```

### Project Structure

```
Vidalytics/
├── backend/
│   ├── App/                 # Main application modules
│   ├── requirements.txt     # Python dependencies
│   └── main.py             # FastAPI entry point
├── frontend-nuxt4/
│   ├── app/                # Nuxt 4 application
│   ├── components/         # Vue components
│   ├── composables/        # Nuxt composables
│   └── package.json        # Node dependencies
├── docs/                   # Documentation
├── Vidalytics.db          # SQLite database
└── .env                   # Environment variables
```

## Documentation

- [Setup Guide](./SetupGuide.md) - Detailed setup instructions
- [API Documentation](./API_DOCUMENTATION.md) - Backend API reference
- [Security Guide](../SECURITY.md) - Security implementation details

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test your changes locally
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
