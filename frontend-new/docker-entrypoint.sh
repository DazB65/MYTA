#!/bin/sh
# Docker entrypoint script for CreatorMate Frontend

set -e

# Function to log messages
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting CreatorMate Frontend container..."

# Replace environment variables in nginx configuration
if [ -n "$API_BASE_URL" ]; then
    log "Setting API_BASE_URL to: $API_BASE_URL"
    sed -i "s|http://backend:8888|$API_BASE_URL|g" /etc/nginx/conf.d/default.conf
fi

if [ -n "$NGINX_PORT" ]; then
    log "Setting Nginx port to: $NGINX_PORT"
    sed -i "s|listen 80|listen $NGINX_PORT|g" /etc/nginx/conf.d/default.conf
fi

if [ -n "$NGINX_HOST" ]; then
    log "Setting server name to: $NGINX_HOST"
    sed -i "s|server_name localhost|server_name $NGINX_HOST|g" /etc/nginx/conf.d/default.conf
fi

# Test nginx configuration
log "Testing Nginx configuration..."
nginx -t

if [ $? -eq 0 ]; then
    log "Nginx configuration is valid"
else
    log "ERROR: Nginx configuration is invalid"
    exit 1
fi

log "Starting Nginx..."

# Execute the main command
exec "$@"