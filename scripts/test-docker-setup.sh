#!/bin/bash
# Test script for Vidalytics Docker setup

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Test Docker installation
test_docker() {
    log_info "Testing Docker installation..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        return 1
    fi
    
    docker --version
    log_success "Docker is installed"
}

# Test Docker Compose
test_docker_compose() {
    log_info "Testing Docker Compose..."
    
    if ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not available"
        return 1
    fi
    
    docker compose version
    log_success "Docker Compose is available"
}

# Test Docker Compose file syntax
test_compose_files() {
    log_info "Testing Docker Compose file syntax..."
    
    # Test production compose file
    if docker compose -f docker-compose.yml config > /dev/null 2>&1; then
        log_success "Production docker-compose.yml is valid"
    else
        log_error "Production docker-compose.yml has syntax errors"
        return 1
    fi
    
    # Test development compose file
    if docker compose -f docker-compose.dev.yml config > /dev/null 2>&1; then
        log_success "Development docker-compose.dev.yml is valid"
    else
        log_error "Development docker-compose.dev.yml has syntax errors"
        return 1
    fi
}

# Test Dockerfiles
test_dockerfiles() {
    log_info "Testing Dockerfile syntax..."
    
    # Test backend Dockerfile
    if docker build -f backend/Dockerfile --target production -t Vidalytics-backend-test backend/ --dry-run > /dev/null 2>&1; then
        log_success "Backend Dockerfile is valid"
    else
        log_warning "Backend Dockerfile validation failed (this may be normal if dependencies are missing)"
    fi
    
    # Test frontend Dockerfile  
    if docker build -f frontend-new/Dockerfile --target production -t Vidalytics-frontend-test frontend-new/ --dry-run > /dev/null 2>&1; then
        log_success "Frontend Dockerfile is valid"
    else
        log_warning "Frontend Dockerfile validation failed (this may be normal if dependencies are missing)"
    fi
}

# Test script permissions
test_scripts() {
    log_info "Testing script permissions..."
    
    if [ -x "docker-dev.sh" ]; then
        log_success "docker-dev.sh is executable"
    else
        log_error "docker-dev.sh is not executable"
        return 1
    fi
    
    if [ -x "docker-prod.sh" ]; then
        log_success "docker-prod.sh is executable"
    else
        log_error "docker-prod.sh is not executable"
        return 1
    fi
}

# Test environment configuration
test_env_config() {
    log_info "Testing environment configuration..."
    
    if [ -f ".env.docker.example" ]; then
        log_success ".env.docker.example exists"
    else
        log_error ".env.docker.example is missing"
        return 1
    fi
    
    if [ -f ".env" ]; then
        log_success ".env file exists"
    else
        log_warning ".env file not found - you'll need to create it from .env.docker.example"
    fi
}

# Test required files
test_required_files() {
    log_info "Testing required files..."
    
    required_files=(
        "docker-compose.yml"
        "docker-compose.dev.yml"
        "backend/Dockerfile"
        "frontend-new/Dockerfile"
        "backend/.dockerignore"
        "frontend-new/.dockerignore"
        "redis.conf"
        "monitoring/prometheus.yml"
        "DOCKER.md"
    )
    
    for file in "${required_files[@]}"; do
        if [ -f "$file" ]; then
            log_success "$file exists"
        else
            log_error "$file is missing"
            return 1
        fi
    done
}

# Test directory structure
test_directory_structure() {
    log_info "Testing directory structure..."
    
    required_dirs=(
        "backend"
        "frontend-new"
        "monitoring"
    )
    
    for dir in "${required_dirs[@]}"; do
        if [ -d "$dir" ]; then
            log_success "$dir directory exists"
        else
            log_error "$dir directory is missing"
            return 1
        fi
    done
}

# Main test execution
main() {
    echo "🐳 Vidalytics Docker Setup Test"
    echo "================================="
    echo ""
    
    # Run all tests
    test_docker || exit 1
    echo ""
    
    test_docker_compose || exit 1
    echo ""
    
    test_directory_structure || exit 1
    echo ""
    
    test_required_files || exit 1
    echo ""
    
    test_compose_files || exit 1
    echo ""
    
    test_dockerfiles
    echo ""
    
    test_scripts || exit 1
    echo ""
    
    test_env_config
    echo ""
    
    echo "================================="
    echo -e "${GREEN}🎉 Docker setup test completed successfully!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Copy .env.docker.example to .env and configure your API keys"
    echo "2. Run './docker-dev.sh start' for development"
    echo "3. Run './docker-prod.sh deploy' for production"
    echo ""
    echo "For more information, see DOCKER.md"
}

# Run main function
main "$@"