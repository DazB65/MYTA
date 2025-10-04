#!/bin/bash

# MYTA Backend Start Script for Railway
echo "🚀 Starting MYTA Backend..."

# Set Python path
export PYTHONPATH=/app

# Run database migrations if needed
echo "📊 Checking database..."
python -c "
try:
    from App.database import get_database_manager
    db_manager = get_database_manager()
    print('✅ Database connection verified')
except Exception as e:
    print(f'⚠️ Database warning: {e}')
"

# Start the FastAPI server
echo "🌐 Starting FastAPI server on port ${PORT:-8888}..."
exec uvicorn App.main:app \
    --host 0.0.0.0 \
    --port ${PORT:-8888} \
    --workers 1 \
    --log-level info \
    --access-log \
    --no-use-colors
