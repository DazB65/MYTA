#!/bin/bash

# Vidalytics Development with Hot Reload
echo "🚀 Starting Vidalytics Development Environment (Hot Reload)"

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

echo "⚡ Starting Nuxt 4 dev server with hot reload..."
cd frontend-nuxt4
API_BASE_URL=http://localhost:8888 npm run dev &
FRONTEND_PID=$!
cd ..

echo "🐍 Starting Python backend on http://localhost:8888"
# Activate virtualenv from repo root
if [ -d ".venv" ]; then
  source .venv/bin/activate
elif [ -d "venv" ]; then
  source venv/bin/activate
fi
uvicorn backend.App.main:app --reload --host 0.0.0.0 --port 8888 &
BACKEND_PID=$!

echo "⏳ Waiting for servers to start..."
sleep 5

echo "✅ Development environment ready!"
echo "🌐 Frontend: http://localhost:3000 (Nuxt dev)"
echo "🌐 Backend: http://localhost:8888"
echo "📡 API available at http://localhost:8888/api/"
echo ""
echo "⚡ Frontend changes will auto-reload"
echo "🔄 Backend changes will auto-reload"
echo "Press Ctrl+C to stop all services"

# Wait for both processes
wait $FRONTEND_PID $BACKEND_PID