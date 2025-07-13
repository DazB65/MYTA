#!/bin/bash

# Auto-rebuild frontend when files change
echo "👀 Watching frontend files for changes..."

# Function to rebuild
rebuild() {
    echo "🔄 Changes detected, rebuilding frontend..."
    cd frontend-new
    npm run build
    cd ..
    echo "✅ Frontend rebuilt at $(date)"
}

# Initial build
rebuild

# Watch for changes in src directory
if command -v fswatch >/dev/null 2>&1; then
    echo "Using fswatch to monitor changes..."
    fswatch -o frontend-new/src | while read; do rebuild; done
elif command -v inotifywait >/dev/null 2>&1; then
    echo "Using inotifywait to monitor changes..."
    while inotifywait -r -e modify,create,delete frontend-new/src; do rebuild; done
else
    echo "⚠️  No file watcher available. Install fswatch: brew install fswatch"
    echo "   Or manually run: cd frontend-new && npm run build"
fi