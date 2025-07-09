# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CreatorMate is a web application for YouTube content creators with an AI-powered assistant. The application consists of a Python FastAPI backend and a modern React + TypeScript frontend.

## Architecture

### Backend (`/backend/`)
- **FastAPI framework** with Python 3.9+
- **main.py**: Core FastAPI application with API endpoints
- **ai_services.py**: OpenAI GPT-4o integration for AI responses with context management
- **Dependencies**: FastAPI, OpenAI, python-dotenv, pydantic

### Frontend (`/frontend-new/`)
- **React 18 + TypeScript + Vite** modern development stack
- **Component-based architecture** with full type safety
- **State management**: Zustand for user data and chat state
- **UI Framework**: Tailwind CSS with custom design system
- **Key Components**:
  - Layout: Main layout, Sidebar, AgentSidebar with responsive design
  - Chat: Real-time chat interface with thinking indicators
  - Pages: Onboarding, Channel, Pillars, Videos, Tools, Settings
  - Common: Reusable Button, Card, LoadingSpinner components
- **Build Output**: Production files served from `/frontend-dist/`

### Legacy Frontend (`/frontend/`)
- **Vanilla HTML/CSS/JavaScript** (deprecated, kept for reference)
- **Static files**: Original implementation now superseded by React app

## Development Commands

### Backend Development
```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source ../venv/bin/activate

# Install dependencies
pip install fastapi uvicorn openai python-dotenv

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8888
```

### Database Management
```bash
# Database is automatically created on first run
# Location: backend/creatormate.db (SQLite)
# Schema includes: users, channel_info, conversation_history, insights
```

### Frontend Development
```bash
# Navigate to React frontend directory
cd frontend-new

# Install dependencies
npm install

# Start development server (for development)
npm run dev

# Build for production
npm run build

# Type checking
npm run type-check
```

### Quick Start
```bash
# Use the convenience script to start everything
./start-dev.sh
```

## Environment Configuration

- **Environment variables**: Create `.env` file in project root
- **Required variables**: `OPENAI_API_KEY` for AI functionality
- **Backend serves frontend**: React build files served from `/frontend-dist/`

## API Endpoints

### Core Endpoints
- `POST /api/agent/chat`: Main chat interface with context-aware responses
- `POST /api/agent/set-channel-info`: Update user channel information
- `POST /api/agent/quick-action`: Execute quick actions (script generation, hooks, etc.)
- `GET /api/agent/insights/{user_id}`: Get dynamic insights for a user
- `POST /api/agent/generate-insights`: Generate fresh insights
- `GET /api/agent/status`: Check AI agent status
- `GET /health`: Health check endpoint

### Database-Driven Features
- **Persistent user context**: All user data stored in SQLite database
- **Channel information**: Comprehensive channel metrics and settings
- **Conversation history**: Last 20 messages per user with automatic cleanup
- **Dynamic insights**: AI-generated insights based on channel performance
- **Quick Actions**: Context-aware content generation tools

## Key Features

### AI Integration
- OpenAI GPT-4o model for content creator assistance
- Context-aware responses based on channel metrics
- Specialized system prompts for YouTube content optimization

### User Experience
- **Modern React UI** with TypeScript type safety
- **Responsive design** with Tailwind CSS and mobile-first approach
- **Real-time chat** with thinking indicators and error handling
- **Component-based architecture** with reusable UI elements
- **State management** with Zustand for persistent user data
- **Form validation** with React Hook Form and Zod schemas
- **Agent personalization** with avatar selection and personality settings

### Content Tools
- **Quick Actions**: Generate scripts, improve hooks, optimize titles, get ideas
- **Dynamic Insights**: Performance analysis, trending topics, growth recommendations
- **Personalized Recommendations**: Based on niche, subscriber count, and goals

### Data Management
- **SQLite Database**: Persistent user data storage
- **User Context**: Channel metrics, conversation history, insights
- **Data Validation**: Frontend and backend input validation
- **Error Handling**: Comprehensive error handling throughout the application

## Testing

To test the application:

1. **Quick Start**: Run `./start-dev.sh` from the project root
2. **Manual Start**: 
   - Build React frontend: `cd frontend-new && npm run build`
   - Start backend: `cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8888`
3. **Access the application**: Navigate to `http://localhost:8888`
4. **Test functionality**:
   - Complete onboarding flow with channel information
   - Use the AI chat interface with thinking indicators
   - Navigate between pages: Channel, Pillars, Videos, Tools, Settings
   - Try Quick Actions (Generate Script, Improve Hooks, etc.)
   - View dynamic insights in the agent sidebar
   - Test agent customization and avatar selection

## Development Notes

- **Database**: SQLite database auto-created on first run
- **Build process**: React frontend built to `/frontend-dist/` and served by FastAPI
- **Virtual environment**: Uses `venv/` directory for Python dependencies
- **CORS enabled**: Backend allows all origins for development
- **Persistent data**: All user context stored in database
- **TypeScript**: Full type safety with zero compilation errors
- **Hot reload**: Backend auto-reloads on changes, frontend requires rebuild
- **Modern stack**: React 18, TypeScript, Vite, Tailwind CSS, Zustand