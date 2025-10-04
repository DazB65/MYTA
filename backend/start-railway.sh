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

# Check if we can import the railway app
echo "🔍 Checking railway app import..."
python -c "
try:
    import railway_main
    print('✅ Railway app import successful')
except Exception as e:
    print(f'❌ Railway app import failed: {e}')
    print('Trying full app...')
    try:
        from App.main import app
        print('✅ Full app import successful')
    except Exception as e2:
        print(f'❌ Full app import failed: {e2}')
        import traceback
        traceback.print_exc()
        exit(1)
"

# Start the FastAPI server (try railway_main first, fallback to full app)
echo "🌐 Starting FastAPI server on port $PORT..."
if python -c "import railway_main" 2>/dev/null; then
    echo "Using minimal railway_main app"
    exec uvicorn railway_main:app \
        --host 0.0.0.0 \
        --port $PORT \
        --workers 1 \
        --log-level info \
        --access-log \
        --no-use-colors
else
    echo "Using full App.main app"
    exec uvicorn App.main:app \
        --host 0.0.0.0 \
        --port $PORT \
        --workers 1 \
        --log-level info \
        --access-log \
        --no-use-colors
fi
