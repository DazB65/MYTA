# CLAUDE.md

## Standard Workflow

1. First think through the problem, read the codebase for relevant files, and write a plan to tasks/todo.md.
2. The plan should have a list of todo items that you can check off as you complete them
3. Before you begin working, check in with me and I will verify the plan.
4. Then, begin working on the todo items, marking them as complete as you go.
5. Please every step of the way just give me a high level explanation of what changes you made
6. Make every task and code change you do as simple as possible. We want to avoid making any massive or complex changes. Every change should impact as little code as possible. Everything is about simplicity.
7. Finally, add a review section to the [todo.md](http://todo.md/) file with a summary of the changes you made and any other relevant information.
   This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CreatorMate is a web application for YouTube content creators with an AI-powered hierarchical multi-agent system. The application consists of a Python FastAPI backend with specialized AI agents and a modern React + TypeScript frontend.

### Multi-Agent Architecture

CreatorMate implements a sophisticated hierarchical agent system with strict communication protocols:

```
                    ┌─────────────────────────────────┐
                    │           USER INTERFACE       │
                    └─────────────┬───────────────────┘
                                  │
                    ┌─────────────▼───────────────────┐
                    │         BOSS AGENT             │
                    │    (Claude 3.5 Sonnet)        │
                    │   Central Orchestrator         │
                    └─────────────┬───────────────────┘
                                  │
            ┌─────────────────────┼─────────────────────┐
            │                     │                     │
    ┌───────▼──────┐    ┌────────▼────────┐   ┌────────▼──────────┐
    │   Content    │    │   Audience      │   │ SEO & Discover-   │
    │   Analysis   │    │   Insights      │   │ ability Agent     │
    │ (Gemini 2.5) │    │ (Claude Sonnet) │   │ (Claude Haiku)    │
    └──────────────┘    └─────────────────┘   └───────────────────┘
            │                     │                     │
    ┌───────▼──────┐    ┌────────▼────────────────────────────────┐
    │ Competitive  │    │      Monetization Strategy Agent       │
    │   Analysis   │    │         (Claude Haiku)                 │
    │ (Gemini 2.5) │    └─────────────────────────────────────────┘
    └──────────────┘
```

#### Agent Communication Rules (CRITICAL)

1. **HIERARCHY ENFORCEMENT**:

   - Boss Agent is the ONLY agent that communicates with users
   - Specialized agents NEVER communicate directly with users
   - Communication flow: User → Boss Agent → Specialized Agents → Boss Agent → User

2. **DOMAIN BOUNDARIES**:

   - Each specialized agent has strict domain restrictions
   - Agents must reject requests outside their domain expertise
   - All responses must include `for_boss_agent_only: true`

3. **AUTHENTICATION**:
   - All specialized agent requests require Boss Agent JWT authentication
   - Unauthorized requests must be rejected with proper error responses

## Architecture

### Backend (`/backend/`)

- **FastAPI framework** with Python 3.9+
- **Hierarchical Multi-Agent System**:
  - `boss_agent.py`: Central orchestrator (Claude 3.5 Sonnet)
  - `content_analysis_agent.py`: Video performance analysis (Gemini 2.5 Pro + Claude fallback)
  - `audience_insights_agent.py`: Demographics & sentiment analysis (Claude 3.5 Sonnet + Haiku fallback)
  - `seo_discoverability_agent.py`: Search optimization (Claude 3.5 Haiku)
  - `competitive_analysis_agent.py`: Market positioning (Gemini 2.5 Pro + Claude fallback)
  - `monetization_strategy_agent.py`: Revenue optimization (Claude 3.5 Haiku + Sonnet fallback)
  - `boss_agent_auth.py`: JWT authentication system for agent communication
- **main.py**: Core FastAPI application with API endpoints
- **ai_services.py**: Legacy AI integration (superseded by agent system)
- **Dependencies**: FastAPI, OpenAI, Google Generative AI, PyJWT, python-dotenv, pydantic

#### Agent Domain Definitions

**Boss Agent (boss_agent.py)**:

- **Model**: Claude 3.5 Sonnet (GPT-4o for intent classification)
- **Domain**: User communication, agent orchestration, response synthesis
- **Responsibilities**: Intent classification, agent delegation, multi-agent coordination

**Content Analysis Agent (content_analysis_agent.py)**:

- **Model**: Gemini 2.5 Pro (primary), Claude 3.5 Sonnet (fallback)
- **Domain**: Video performance, hooks, titles, thumbnails, retention metrics
- **Cache TTL**: 1-4 hours based on analysis depth

**Audience Insights Agent (audience_insights_agent.py)**:

- **Model**: Claude 3.5 Sonnet (primary), Claude 3.5 Haiku (fallback)
- **Domain**: Demographics, behavior patterns, sentiment analysis, community health
- **Cache TTL**: 30 minutes - 4 hours based on analysis depth

**SEO & Discoverability Agent (seo_discoverability_agent.py)**:

- **Model**: Claude 3.5 Haiku
- **Domain**: Keyword research, search optimization, algorithm favorability
- **Cache TTL**: 2-6 hours based on analysis depth

**Competitive Analysis Agent (competitive_analysis_agent.py)**:

- **Model**: Gemini 2.5 Pro (primary), Claude 3.5 Sonnet (fallback)
- **Domain**: Competitor benchmarking, market positioning, cross-channel analysis
- **Cache TTL**: 2-12 hours based on analysis depth

**Monetization Strategy Agent (monetization_strategy_agent.py)**:

- **Model**: Claude 3.5 Haiku (primary), Claude 3.5 Sonnet (fallback)
- **Domain**: Revenue optimization, sponsorship opportunities, RPM/CPM analysis
- **Cache TTL**: 2-8 hours based on analysis depth

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
- **Required variables**:
  - `OPENAI_API_KEY` for Claude models and Boss Agent
  - `GOOGLE_API_KEY` for Gemini models (Content Analysis, Competitive Analysis)
  - `YOUTUBE_API_KEY` for YouTube Data API integration
  - `BOSS_AGENT_SECRET_KEY` for JWT authentication (optional, auto-generated if not set)
- **Backend serves frontend**: React build files served from `/frontend-dist/`

## Agent Communication Protocols

### Standard Request Format (Boss Agent → Specialized Agents)

```json
{
  "request_id": "uuid4_string",
  "query_type": "content_analysis|audience_insights|seo_discoverability|competitive_analysis|monetization_strategy",
  "context": {
    "channel_id": "channel_identifier",
    "time_period": "last_7d|last_30d|last_90d",
    "specific_videos": ["video_id1", "video_id2"],
    "competitors": ["channel_id1", "channel_id2"]
  },
  "token_budget": {
    "input_tokens": 3000,
    "output_tokens": 1500
  },
  "analysis_depth": "quick|standard|deep",
  "boss_agent_token": "jwt_authentication_token",
  "timestamp": "2024-07-10T10:30:00Z"
}
```

### Standard Response Format (Specialized Agents → Boss Agent)

```json
{
  "agent_type": "content_analysis|audience_insights|seo_discoverability|competitive_analysis|monetization_strategy",
  "response_id": "unique_response_id",
  "request_id": "original_request_id",
  "timestamp": "2024-07-10T10:30:00Z",
  "confidence_score": 0.88,
  "domain_match": true,
  "analysis": {
    "summary": "Brief analysis summary",
    "metrics": { "key_metric": 8.7 },
    "key_insights": [
      {
        "insight": "Key finding",
        "evidence": "Supporting data",
        "impact": "High|Medium|Low",
        "confidence": 0.9
      }
    ],
    "recommendations": [
      {
        "recommendation": "Specific action",
        "expected_impact": "High|Medium|Low",
        "implementation_difficulty": "Easy|Medium|Hard",
        "reasoning": "Why this matters"
      }
    ]
  },
  "token_usage": {
    "input_tokens": 3200,
    "output_tokens": 1800,
    "model": "claude-3-5-sonnet-20241022"
  },
  "cache_info": {
    "cache_hit": false,
    "cache_key": "agent_cache_key",
    "ttl_remaining": 7200
  },
  "processing_time": 2.34,
  "for_boss_agent_only": true
}
```

### Error Response Format

```json
{
  "agent_type": "agent_name",
  "domain_match": false,
  "analysis": {
    "summary": "Error description",
    "error_type": "authentication_error|domain_mismatch|api_error|processing_error",
    "error_message": "Detailed error information"
  },
  "for_boss_agent_only": true,
  "authentication_required": true
}
```

## Cost Optimization Guidelines

### Model Selection Logic

1. **Primary Model Assignment**:

   - Use specialized models for domain expertise (Gemini for visual analysis, Haiku for cost-effective text)
   - Assign based on task complexity and cost considerations

2. **Fallback Strategy**:

   - Content Analysis: Gemini 2.5 Pro → Claude 3.5 Sonnet
   - Audience Insights: Claude 3.5 Sonnet → Claude 3.5 Haiku
   - Competitive Analysis: Gemini 2.5 Pro → Claude 3.5 Sonnet
   - Monetization Strategy: Claude 3.5 Haiku → Claude 3.5 Sonnet

3. **Token Budget Management**:
   - Quick Analysis: ~1500 tokens (basic insights, fast response)
   - Standard Analysis: ~3500 tokens (comprehensive analysis, balanced cost)
   - Deep Analysis: ~6000 tokens (advanced insights, maximum value)

### Caching Strategies

1. **TTL by Data Volatility**:

   - Content metrics: 1-4 hours (moderate change rate)
   - Audience data: 30 minutes - 4 hours (gradual evolution)
   - SEO data: 2-6 hours (slow change rate)
   - Competitive data: 2-12 hours (stable landscape)
   - Monetization data: 2-8 hours (infrequent updates)

2. **Cache Key Components**:

   - Agent type + Channel ID + Time period + Analysis depth + Parameters hash

3. **Invalidation Triggers**:
   - TTL expiration + Significant data changes + Manual clearing + Error conditions

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

- **Hierarchical Multi-Agent Architecture** with specialized domain expertise
- **Boss Agent**: Claude 3.5 Sonnet for orchestration and user communication
- **Specialized Agents**: Domain-specific models (Gemini 2.5 Pro, Claude variants)
- **Context-aware responses** based on channel metrics and multi-agent synthesis
- **JWT Authentication** ensuring secure inter-agent communication
- **Intelligent caching** with domain-appropriate TTLs for cost optimization

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

### Agent System Development

- **Hierarchical Architecture**: All agents must respect Boss Agent authority
- **Domain Validation**: Agents reject out-of-scope requests with proper error responses
- **Authentication**: JWT tokens required for all Boss Agent → Specialized Agent communication
- **Testing**: Use `demo_all_agents.py` and `test_hierarchy_validation.py` for comprehensive testing
- **Model Management**: Fallback strategies ensure system resilience
- **Caching**: Domain-specific TTLs optimize cost and performance
- **Security**: Strict communication protocols prevent unauthorized access

### Critical Development Rules

1. **NEVER allow specialized agents to communicate directly with users**
2. **ALWAYS include `for_boss_agent_only: true` in specialized agent responses**
3. **ALWAYS validate Boss Agent authentication in specialized agents**
4. **ALWAYS respect domain boundaries and reject out-of-scope requests**
5. **ALWAYS implement proper error handling and fallback mechanisms**
