#!/bin/bash

# MYTA Backend Start Script for Railway
echo "🚀 Starting MYTA Backend on Railway..."

# Set Python path
export PYTHONPATH=/app

# Set default port if not provided by Railway
export PORT=${PORT:-8888}

# Log environment info
echo "📊 Environment: ${ENVIRONMENT:-production}"
echo "🌐 Port: $PORT"
echo "🐍 Python Path: $PYTHONPATH"

# Check if we can import the main app
echo "🔍 Checking app import..."
python -c "
try:
    from App.main import app
    print('✅ App import successful')
except Exception as e:
    print(f'❌ App import failed: {e}')
    import traceback
    traceback.print_exc()
    exit(1)
"

# Start the FastAPI server
echo "🌐 Starting FastAPI server on port $PORT..."
exec uvicorn App.main:app \
    --host 0.0.0.0 \
    --port $PORT \
    --workers 1 \
    --log-level info \
    --access-log \
    --no-use-colors
