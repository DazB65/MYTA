#!/bin/bash

# Vidalytics Development Startup Script
echo "🚀 Starting Vidalytics Development Environment"

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY not found in environment"
    echo "   Make sure your .env file is properly configured"
fi

# Function to cleanup background processes
cleanup() {
    echo "🛑 Stopping development servers..."
    jobs -p | xargs -I {} kill {} 2>/dev/null
    exit 0
}

# Set trap for cleanup on script exit
trap cleanup SIGINT SIGTERM EXIT

echo "📦 Building React frontend..."
cd frontend-vidalytics
npm run build
cd ..

echo "🐍 Starting Python backend on http://localhost:8888"
cd backend
source ../venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8888 &
BACKEND_PID=$!

echo "⏳ Waiting for backend to start..."
sleep 3

echo "✅ Development environment ready!"
echo "🌐 Open http://localhost:8888 in your browser"
echo "📡 API available at http://localhost:8888/api/"
echo "💬 Health check: http://localhost:8888/health"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for backend process
wait $BACKEND_PID