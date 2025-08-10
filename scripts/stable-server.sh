#!/bin/bash

# Stable Server Script for Vidalytics
# This script ensures the server stays running reliably

echo "🚀 Starting Vidalytics Stable Server..."

# Kill any existing processes
pkill -f uvicorn 2>/dev/null || true
pkill -f "start-dev" 2>/dev/null || true

# Wait a moment for processes to clean up
sleep 2

# Navigate to project directory
cd /Users/darrenberich/Vidalytics

# Build frontend once (Nuxt 4)
echo "📦 Building frontend (Nuxt 4)..."
cd frontend-nuxt4
API_BASE_URL=http://localhost:8888 npm run build
cd ..

# Start backend with proper environment
echo "🐍 Starting backend on http://localhost:8888..."
cd backend

# Activate virtual environment and start server
source ../venv/bin/activate

# Start server in background with nohup for stability
nohup python -m uvicorn main:app --host 0.0.0.0 --port 8888 --reload > ../server.log 2>&1 &

# Wait for server to start
sleep 5

# Check if server is running
if curl -s http://localhost:8888/health > /dev/null 2>&1; then
    echo "✅ Server started successfully!"
    echo "🌐 Access at: http://localhost:8888"
    echo "📋 Logs: tail -f /Users/darrenberich/Vidalytics/server.log"
else
    echo "❌ Server failed to start. Check logs:"
    tail -20 ../server.log
fi