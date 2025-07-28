#!/bin/bash
# Test script for CreatorMate CI/CD setup validation

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

# Test GitHub Actions workflows exist
test_workflow_files() {
    log_info "Testing GitHub Actions workflow files..."
    
    required_workflows=(
        ".github/workflows/ci.yml"
        ".github/workflows/cd.yml"
        ".github/workflows/security.yml"
        ".github/workflows/performance.yml"
    )
    
    for workflow in "${required_workflows[@]}"; do
        if [ -f "$workflow" ]; then
            log_success "$workflow exists"
        else
            log_error "$workflow is missing"
            return 1
        fi
    done
}

# Test workflow syntax
test_workflow_syntax() {
    log_info "Testing GitHub Actions workflow syntax..."
    
    # Check if yq is available for YAML validation
    if command -v yq &> /dev/null; then
        for workflow in .github/workflows/*.yml; do
            if yq eval . "$workflow" > /dev/null 2>&1; then
                log_success "$(basename "$workflow") has valid YAML syntax"
            else
                log_error "$(basename "$workflow") has invalid YAML syntax"
                return 1
            fi
        done
    else
        log_warning "yq not found - skipping YAML syntax validation"
        log_info "Install yq with: brew install yq (macOS) or apt-get install yq (Ubuntu)"
    fi
}

# Test GitHub configuration files
test_github_config() {
    log_info "Testing GitHub configuration files..."
    
    required_configs=(
        ".github/dependabot.yml"
        ".github/pull_request_template.md"
        ".github/ISSUE_TEMPLATE/bug_report.md"
        ".github/ISSUE_TEMPLATE/feature_request.md"
    )
    
    for config in "${required_configs[@]}"; do
        if [ -f "$config" ]; then
            log_success "$config exists"
        else
            log_error "$config is missing"
            return 1
        fi
    done
}

# Test directory structure
test_directory_structure() {
    log_info "Testing CI/CD directory structure..."
    
    required_dirs=(
        ".github"
        ".github/workflows"
        ".github/ISSUE_TEMPLATE"
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

# Test documentation
test_documentation() {
    log_info "Testing CI/CD documentation..."
    
    if [ -f "CI-CD.md" ]; then
        log_success "CI-CD.md documentation exists"
        
        # Check for key sections
        required_sections=(
            "Pipeline Overview"
            "CI Pipeline"
            "CD Pipeline" 
            "Security Pipeline"
            "Performance Pipeline"
        )
        
        for section in "${required_sections[@]}"; do
            if grep -q "$section" CI-CD.md; then
                log_success "Documentation contains '$section' section"
            else
                log_warning "Documentation missing '$section' section"
            fi
        done
    else
        log_error "CI-CD.md documentation is missing"
        return 1
    fi
}

# Test workflow environment variables
test_workflow_env_vars() {
    log_info "Testing workflow environment variables..."
    
    # Check CI workflow
    if grep -q "PYTHON_VERSION" .github/workflows/ci.yml; then
        log_success "CI workflow has environment variables configured"
    else
        log_warning "CI workflow missing environment variables"
    fi
    
    # Check CD workflow  
    if grep -q "REGISTRY" .github/workflows/cd.yml; then
        log_success "CD workflow has registry configuration"
    else
        log_warning "CD workflow missing registry configuration"
    fi
}

# Test workflow triggers
test_workflow_triggers() {
    log_info "Testing workflow triggers..."
    
    # Check CI triggers
    if grep -q "push:" .github/workflows/ci.yml && grep -q "pull_request:" .github/workflows/ci.yml; then
        log_success "CI workflow has proper triggers (push/PR)"
    else
        log_error "CI workflow missing required triggers"
        return 1
    fi
    
    # Check security scheduled runs
    if grep -q "schedule:" .github/workflows/security.yml; then
        log_success "Security workflow has scheduled runs"
    else
        log_warning "Security workflow missing scheduled runs"
    fi
    
    # Check performance triggers
    if grep -q "workflow_dispatch:" .github/workflows/performance.yml; then
        log_success "Performance workflow has manual dispatch option"
    else
        log_warning "Performance workflow missing manual dispatch"
    fi
}

# Test workflow jobs structure
test_workflow_jobs() {
    log_info "Testing workflow jobs structure..."
    
    # Check CI jobs
    ci_jobs=(
        "code-quality"
        "backend-tests"
        "frontend-tests"
        "docker-build"
        "e2e-tests"
    )
    
    for job in "${ci_jobs[@]}"; do
        if grep -q "$job:" .github/workflows/ci.yml; then
            log_success "CI workflow has '$job' job"
        else
            log_error "CI workflow missing '$job' job"
            return 1
        fi
    done
    
    # Check CD jobs
    if grep -q "deploy-staging:" .github/workflows/cd.yml; then
        log_success "CD workflow has staging deployment job"
    else
        log_error "CD workflow missing staging deployment job"
        return 1
    fi
    
    if grep -q "deploy-production:" .github/workflows/cd.yml; then
        log_success "CD workflow has production deployment job"
    else
        log_error "CD workflow missing production deployment job"
        return 1
    fi
}

# Test security workflow completeness
test_security_workflow() {
    log_info "Testing security workflow completeness..."
    
    security_jobs=(
        "dependency-scan"
        "codeql-analysis"
        "container-security"
        "secrets-scan"
    )
    
    for job in "${security_jobs[@]}"; do
        if grep -q "$job:" .github/workflows/security.yml; then
            log_success "Security workflow has '$job' job"
        else
            log_error "Security workflow missing '$job' job"
            return 1
        fi
    done
}

# Test performance workflow completeness
test_performance_workflow() {
    log_info "Testing performance workflow completeness..."
    
    performance_jobs=(
        "frontend-performance"
        "backend-load-testing"
        "database-performance"
    )
    
    for job in "${performance_jobs[@]}"; do
        if grep -q "$job:" .github/workflows/performance.yml; then
            log_success "Performance workflow has '$job' job"
        else
            log_error "Performance workflow missing '$job' job"
            return 1
        fi
    done
}

# Test dependabot configuration
test_dependabot_config() {
    log_info "Testing Dependabot configuration..."
    
    if [ -f ".github/dependabot.yml" ]; then
        # Check for required package ecosystems
        ecosystems=("pip" "npm" "docker" "github-actions")
        
        for ecosystem in "${ecosystems[@]}"; do
            if grep -q "package-ecosystem: \"$ecosystem\"" .github/dependabot.yml; then
                log_success "Dependabot configured for $ecosystem"
            else
                log_error "Dependabot missing $ecosystem configuration"
                return 1
            fi
        done
    else
        log_error "Dependabot configuration file missing"
        return 1
    fi
}

# Test integration with existing Docker setup
test_docker_integration() {
    log_info "Testing CI/CD integration with Docker setup..."
    
    # Check if Docker files exist (should be from previous task)
    docker_files=(
        "docker-compose.yml"
        "docker-compose.dev.yml"
        "backend/Dockerfile"
        "frontend-new/Dockerfile"
    )
    
    for file in "${docker_files[@]}"; do
        if [ -f "$file" ]; then
            log_success "Docker file $file exists for CI/CD integration"
        else
            log_error "Docker file $file missing - CI/CD requires Docker containerization"
            return 1
        fi
    done
    
    # Check if workflows reference Docker files
    if grep -q "docker" .github/workflows/ci.yml; then
        log_success "CI workflow integrates with Docker"
    else
        log_error "CI workflow missing Docker integration"
        return 1
    fi
}

# Check for common CI/CD best practices
test_best_practices() {
    log_info "Testing CI/CD best practices..."
    
    # Check for caching in workflows
    if grep -q "cache" .github/workflows/ci.yml; then
        log_success "CI workflow uses caching for efficiency"
    else
        log_warning "CI workflow could benefit from dependency caching"
    fi
    
    # Check for security scanning
    if grep -q "security" .github/workflows/ci.yml || [ -f ".github/workflows/security.yml" ]; then
        log_success "Security scanning is integrated"
    else
        log_error "Security scanning is missing"
        return 1
    fi
    
    # Check for parallel job execution
    if grep -q "needs:" .github/workflows/ci.yml; then
        log_success "Workflows use job dependencies for optimization"
    else
        log_warning "Workflows could benefit from job dependencies"
    fi
    
    # Check for environment protection
    if grep -q "environment:" .github/workflows/cd.yml; then
        log_success "CD workflow uses environment protection"
    else
        log_warning "CD workflow could benefit from environment protection"
    fi
}

# Main test execution
main() {
    echo "🚀 CreatorMate CI/CD Setup Test"
    echo "================================"
    echo ""
    
    # Run all tests
    test_directory_structure || exit 1
    echo ""
    
    test_workflow_files || exit 1
    echo ""
    
    test_workflow_syntax
    echo ""
    
    test_github_config || exit 1
    echo ""
    
    test_documentation || exit 1
    echo ""
    
    test_workflow_env_vars
    echo ""
    
    test_workflow_triggers || exit 1
    echo ""
    
    test_workflow_jobs || exit 1
    echo ""
    
    test_security_workflow || exit 1
    echo ""
    
    test_performance_workflow || exit 1
    echo ""
    
    test_dependabot_config || exit 1
    echo ""
    
    test_docker_integration || exit 1
    echo ""
    
    test_best_practices
    echo ""
    
    echo "================================"
    echo -e "${GREEN}🎉 CI/CD setup test completed successfully!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Set up GitHub repository secrets for deployment"
    echo "2. Configure staging and production server access"
    echo "3. Test the CI pipeline with a sample commit"
    echo "4. Set up monitoring and alerting integrations"
    echo ""
    echo "For more information, see CI-CD.md"
}

# Run main function
main "$@"