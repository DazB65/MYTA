#!/bin/bash
# CreatorMate Development Docker Script
# Utility script for managing development environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.dev.yml"
PROJECT_NAME="creatormate-dev"

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
    log_info "Checking requirements..."
    
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
        log_warning ".env file not found. Creating from example..."
        if [ -f ".env.docker.example" ]; then
            cp .env.docker.example .env
            log_info "Please edit .env file with your configuration"
        else
            log_error ".env.docker.example not found. Please create .env file manually."
            exit 1
        fi
    fi
    
    log_success "Requirements check completed"
}

start_services() {
    log_info "Starting CreatorMate development services..."
    
    # Set build date and VCS ref
    export BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
    export VCS_REF=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
    
    # Start services
    docker compose -f $COMPOSE_FILE -p $PROJECT_NAME up -d
    
    log_success "Services started successfully!"
    log_info "Access points:"
    log_info "  Frontend (Vite dev server): http://localhost:5173"
    log_info "  Backend API: http://localhost:8888"
    log_info "  Redis: localhost:6379"
    log_info "  API Documentation: http://localhost:8888/docs"
}

stop_services() {
    log_info "Stopping CreatorMate development services..."
    docker compose -f $COMPOSE_FILE -p $PROJECT_NAME down
    log_success "Services stopped successfully!"
}

restart_services() {
    log_info "Restarting CreatorMate development services..."
    stop_services
    start_services
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
    log_info "Service status:"
    docker compose -f $COMPOSE_FILE -p $PROJECT_NAME ps
}

build_services() {
    log_info "Building CreatorMate development services..."
    
    # Set build variables
    export BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
    export VCS_REF=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
    
    docker compose -f $COMPOSE_FILE -p $PROJECT_NAME build --no-cache
    log_success "Services built successfully!"
}

clean_up() {
    log_info "Cleaning up CreatorMate development environment..."
    
    # Stop and remove containers
    docker compose -f $COMPOSE_FILE -p $PROJECT_NAME down -v --remove-orphans
    
    # Remove images
    log_info "Removing development images..."
    docker images --format "table {{.Repository}}:{{.Tag}}\t{{.ID}}" | grep creatormate | awk '{print $2}' | xargs -r docker rmi -f
    
    # Remove unused volumes (be careful with this)
    log_warning "Removing unused Docker volumes..."
    docker volume prune -f
    
    log_success "Cleanup completed!"
}

shell_access() {
    local service=${1:-backend}
    log_info "Opening shell in $service container..."
    docker compose -f $COMPOSE_FILE -p $PROJECT_NAME exec "$service" /bin/sh
}

run_tests() {
    log_info "Running tests in backend container..."
    docker compose -f $COMPOSE_FILE -p $PROJECT_NAME exec backend python -m pytest tests/ -v
}

show_help() {
    echo "CreatorMate Development Docker Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start         Start all development services"
    echo "  stop          Stop all development services"
    echo "  restart       Restart all development services"
    echo "  build         Build all development services"
    echo "  logs [SERVICE] Show logs (optionally for specific service)"
    echo "  status        Show service status"
    echo "  shell [SERVICE] Open shell in service container (default: backend)"
    echo "  test          Run tests"
    echo "  clean         Clean up containers, images, and volumes"
    echo "  help          Show this help message"
    echo ""
    echo "Services: backend, frontend, redis"
    echo ""
    echo "Examples:"
    echo "  $0 start                    # Start all services"
    echo "  $0 logs backend            # Show backend logs"
    echo "  $0 shell frontend          # Open shell in frontend container"
}

# Main script logic
case "${1:-help}" in
    start)
        check_requirements
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        check_requirements
        restart_services
        ;;
    build)
        check_requirements
        build_services
        ;;
    logs)
        show_logs "$2"
        ;;
    status)
        show_status
        ;;
    shell)
        shell_access "$2"
        ;;
    test)
        run_tests
        ;;
    clean)
        clean_up
        ;;
    help|*)
        show_help
        ;;
esac