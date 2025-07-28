#!/bin/bash
# CreatorMate Production Docker Script
# Utility script for managing production environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.yml"
PROJECT_NAME="creatormate"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_requirements() {
    log_info "Checking production requirements..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if Docker Compose is available
    if ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not available. Please install Docker Compose."
        exit 1
    fi
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        log_error ".env file not found. Please create it from .env.docker.example"
        exit 1
    fi
    
    # Check critical environment variables
    source .env
    if [ -z "$OPENAI_API_KEY" ] || [ -z "$GOOGLE_API_KEY" ] || [ -z "$YOUTUBE_API_KEY" ]; then
        log_error "Critical API keys missing in .env file"
        exit 1
    fi
    
    log_success "Production requirements check completed"
}

deploy() {
    log_info "Deploying CreatorMate to production..."
    
    # Set build date and VCS ref
    export BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
    export VCS_REF=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
    
    # Build and start services
    docker compose -f $COMPOSE_FILE -p $PROJECT_NAME up -d --build
    
    log_success "Production deployment completed!"
    log_info "Access points:"
    log_info "  Application: http://localhost"
    log_info "  Backend API: http://localhost:8888"
    log_info "  Health Check: http://localhost/health"
}

start() {
    log_info "Starting CreatorMate production services..."
    
    export BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
    export VCS_REF=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
    
    docker compose -f $COMPOSE_FILE -p $PROJECT_NAME up -d
    
    log_success "Services started successfully!"
}

stop() {
    log_info "Stopping CreatorMate production services..."
    docker compose -f $COMPOSE_FILE -p $PROJECT_NAME down
    log_success "Services stopped successfully!"
}

restart() {
    log_info "Restarting CreatorMate production services..."
    stop
    start
}

update() {
    log_info "Updating CreatorMate production deployment..."
    
    # Pull latest changes
    git pull origin main
    
    # Set build variables
    export BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
    export VCS_REF=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
    
    # Rebuild and restart services
    docker compose -f $COMPOSE_FILE -p $PROJECT_NAME up -d --build
    
    log_success "Production update completed!"
}

show_logs() {
    local service=${1:-}
    if [ -n "$service" ]; then
        log_info "Showing logs for $service..."
        docker compose -f $COMPOSE_FILE -p $PROJECT_NAME logs -f "$service"
    else
        log_info "Showing logs for all services..."
        docker compose -f $COMPOSE_FILE -p $PROJECT_NAME logs -f
    fi
}

show_status() {
    log_info "Production service status:"
    docker compose -f $COMPOSE_FILE -p $PROJECT_NAME ps
    
    log_info "Health check results:"
    curl -s http://localhost/health | jq . 2>/dev/null || curl -s http://localhost/health
}

backup() {
    log_info "Creating production backup..."
    
    local backup_dir="backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # Backup database
    docker compose -f $COMPOSE_FILE -p $PROJECT_NAME exec -T backend python -c "
from backup_service import get_backup_service
service = get_backup_service('/app/data/creatormate.db')
backup_id = service.create_manual_backup({'type': 'scheduled', 'reason': 'manual_backup'})
print(f'Backup created: {backup_id}')
"
    
    # Backup environment configuration (without secrets)
    grep -v -E "(API_KEY|SECRET|PASSWORD)" .env > "$backup_dir/env_template"
    
    log_success "Backup created in $backup_dir"
}

monitoring_start() {
    log_info "Starting monitoring services..."
    docker compose -f $COMPOSE_FILE -p $PROJECT_NAME --profile monitoring up -d prometheus grafana
    
    log_success "Monitoring services started!"
    log_info "Access points:"
    log_info "  Prometheus: http://localhost:9090"
    log_info "  Grafana: http://localhost:3000 (admin/admin)"
}

monitoring_stop() {
    log_info "Stopping monitoring services..."
    docker compose -f $COMPOSE_FILE -p $PROJECT_NAME stop prometheus grafana
    log_success "Monitoring services stopped!"
}

show_help() {
    echo "CreatorMate Production Docker Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy        Deploy to production (build and start)"
    echo "  start         Start production services"
    echo "  stop          Stop production services"
    echo "  restart       Restart production services"
    echo "  update        Update production deployment"
    echo "  logs [SERVICE] Show logs (optionally for specific service)"
    echo "  status        Show service status and health"
    echo "  backup        Create production backup"
    echo "  monitoring    Start monitoring services"
    echo "  monitoring-stop Stop monitoring services"
    echo "  help          Show this help message"
    echo ""
    echo "Services: backend, frontend, redis, prometheus, grafana"
    echo ""
    echo "Examples:"
    echo "  $0 deploy                  # Full production deployment"
    echo "  $0 logs backend           # Show backend logs"
    echo "  $0 monitoring             # Start monitoring stack"
}

# Main script logic
case "${1:-help}" in
    deploy)
        check_requirements
        deploy
        ;;
    start)
        check_requirements
        start
        ;;
    stop)
        stop
        ;;
    restart)
        check_requirements
        restart
        ;;
    update)
        check_requirements
        update
        ;;
    logs)
        show_logs "$2"
        ;;
    status)
        show_status
        ;;
    backup)
        backup
        ;;
    monitoring)
        monitoring_start
        ;;
    monitoring-stop)
        monitoring_stop
        ;;
    help|*)
        show_help
        ;;
esac