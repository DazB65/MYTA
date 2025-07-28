# CreatorMate CI/CD Pipeline Documentation

This document describes the comprehensive Continuous Integration and Continuous Deployment (CI/CD) pipeline for CreatorMate.

## Pipeline Overview

CreatorMate uses GitHub Actions for CI/CD with multiple automated workflows:

- **CI Pipeline** (`ci.yml`): Continuous Integration with testing and quality checks
- **CD Pipeline** (`cd.yml`): Continuous Deployment to staging and production
- **Security Scans** (`security.yml`): Security and vulnerability scanning
- **Performance Tests** (`performance.yml`): Performance monitoring and load testing

## Workflow Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Code Commit   │───▶│   CI Pipeline   │───▶│  Build & Test   │
│   (Push/PR)     │    │    Triggered    │    │    Complete     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌─────────────────┐             ▼
│   Production    │◄───│  CD Pipeline    │    ┌─────────────────┐
│   Deployment    │    │   Triggered     │◄───│  Security Pass  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## CI Pipeline (`ci.yml`)

### Triggers
- Push to `main`, `develop`, or `feature/*` branches
- Pull requests to `main` or `develop`

### Jobs

#### 1. Code Quality & Security
- **Python linting** with flake8
- **Code formatting** with black
- **Import sorting** with isort
- **Type checking** with mypy
- **Security scanning** with bandit

#### 2. Backend Tests
- **Unit tests** with pytest and coverage
- **Integration tests** with Redis service
- **Coverage reporting** to Codecov

#### 3. Frontend Tests & Build
- **Linting** with ESLint
- **Type checking** with TypeScript
- **Unit tests** with Vitest
- **Production build** verification

#### 4. Docker Build & Security
- **Multi-stage Docker builds** for both backend and frontend
- **Container registry** publishing to GitHub Container Registry
- **Vulnerability scanning** with Trivy
- **Dockerfile linting** with Hadolint

#### 5. End-to-End Tests
- **Full stack deployment** with Docker Compose
- **Health check validation** for all services
- **API endpoint testing**

#### 6. Performance Tests
- **Load testing** with Apache Bench
- **Basic performance benchmarks**

### Environment Variables Required
```bash
# GitHub Secrets needed for CI
GITHUB_TOKEN              # Automatic GitHub token
CODECOV_TOKEN             # Optional: Codecov integration
```

## CD Pipeline (`cd.yml`)

### Triggers
- Successful completion of CI pipeline on `main` branch
- Git tags matching `v*` pattern for production releases
- Manual workflow dispatch

### Deployment Stages

#### 1. Staging Deployment
- **Target**: `main` branch pushes
- **Environment**: `staging`
- **Process**:
  1. Deploy to staging server via SSH
  2. Update environment variables
  3. Run Docker Compose deployment
  4. Execute health checks
  5. Run smoke tests

#### 2. Production Deployment
- **Target**: Git tags (`v*`)
- **Environment**: `production`
- **Process**:
  1. Create pre-deployment backup
  2. Deploy with zero-downtime strategy
  3. Run database migrations
  4. Update services sequentially
  5. Comprehensive health checks
  6. Create GitHub release

#### 3. Rollback Capability
- **Automatic rollback** on deployment failure
- **Backup restoration** from pre-deployment state
- **Service health verification**

### Environment Variables Required
```bash
# Staging Environment
STAGING_HOST                    # Staging server hostname
STAGING_USER                    # SSH username
STAGING_SSH_KEY                 # SSH private key
STAGING_SSH_PORT               # SSH port (optional, default: 22)
STAGING_OPENAI_API_KEY         # Staging OpenAI API key
STAGING_GOOGLE_API_KEY         # Staging Google API key
STAGING_YOUTUBE_API_KEY        # Staging YouTube API key
STAGING_BOSS_AGENT_SECRET_KEY  # Staging boss agent secret
STAGING_SESSION_SECRET_KEY     # Staging session secret
STAGING_REDIS_PASSWORD         # Staging Redis password

# Production Environment  
PRODUCTION_HOST                    # Production server hostname
PRODUCTION_USER                    # SSH username
PRODUCTION_SSH_KEY                 # SSH private key
PRODUCTION_SSH_PORT               # SSH port (optional, default: 22)
PRODUCTION_OPENAI_API_KEY         # Production OpenAI API key
PRODUCTION_GOOGLE_API_KEY         # Production Google API key
PRODUCTION_YOUTUBE_API_KEY        # Production YouTube API key
PRODUCTION_BOSS_AGENT_SECRET_KEY  # Production boss agent secret
PRODUCTION_SESSION_SECRET_KEY     # Production session secret
PRODUCTION_REDIS_PASSWORD         # Production Redis password

# Optional Notifications
SLACK_WEBHOOK                  # Slack webhook for deployment notifications
```

## Security Pipeline (`security.yml`)

### Triggers
- Push to `main` or `develop` branches
- Pull requests
- Daily scheduled scans (2 AM UTC)

### Security Scans

#### 1. Dependency Vulnerability Scanning
- **Python**: Safety tool for Python dependencies
- **Node.js**: npm audit for JavaScript dependencies
- **Results**: JSON reports uploaded as artifacts

#### 2. Code Security Analysis
- **CodeQL**: GitHub's semantic code analysis
- **Languages**: Python and JavaScript
- **Queries**: Security-extended and quality queries

#### 3. Container Security Scanning
- **Trivy**: Container vulnerability scanner
- **Hadolint**: Dockerfile linting and best practices
- **Results**: SARIF format uploaded to GitHub Security tab

#### 4. Secrets Scanning
- **TruffleHog**: Git repository secrets detection
- **GitLeaks**: Additional secrets scanning
- **Scope**: Full repository history

#### 5. Infrastructure Security
- **Checkov**: Docker Compose configuration scanning
- **Results**: Infrastructure security issues identification

#### 6. License Compliance
- **Python**: pip-licenses for license analysis
- **Node.js**: license-checker for dependency licenses
- **Results**: License compliance reports

## Performance Pipeline (`performance.yml`)

### Triggers
- Push to `main` branch
- Pull requests to `main`
- Weekly scheduled runs (Sunday 3 AM UTC)
- Manual workflow dispatch with parameters

### Performance Tests

#### 1. Frontend Performance
- **Bundle size analysis** and optimization
- **Lighthouse CI** for web performance metrics
- **Performance budget** enforcement

#### 2. Backend Load Testing
- **Apache Bench** for basic load testing
- **Artillery** for advanced load testing scenarios
- **Resource usage** monitoring during tests

#### 3. Database Performance
- **Database operation benchmarks**
- **Query performance analysis**
- **Connection pooling optimization**

### Performance Metrics
- **Response times** for API endpoints
- **Throughput** measurements
- **Resource utilization** (CPU, memory)
- **Bundle size** tracking
- **Lighthouse scores** (Performance, Accessibility, SEO)

## Branch Strategy

### Branch Types
- `main`: Production-ready code
- `develop`: Integration branch for ongoing development
- `feature/*`: Feature development branches
- `fix/*`: Bug fix branches

### Release Process
1. **Feature Development**: Work in `feature/*` branches
2. **Integration**: Merge to `develop` for testing
3. **Release Preparation**: Merge `develop` to `main`
4. **Production Release**: Create git tag (`v1.0.0`) on `main`
5. **Hotfixes**: Create `fix/*` branches from `main`

## Automated Dependency Management

### Dependabot Configuration
- **Weekly updates** for all package ecosystems
- **Security updates** prioritized and grouped
- **Automated PR creation** with proper labeling
- **Review assignment** to appropriate team members

### Supported Ecosystems
- **Python pip** packages (backend)
- **Node.js npm** packages (frontend)
- **Docker** base images
- **GitHub Actions** workflow dependencies

## Monitoring and Notifications

### Deployment Notifications
- **Slack integration** for deployment status
- **Success/failure** notifications with details
- **Rollback alerts** for failed deployments

### Security Alerts
- **GitHub Security Advisories** integration
- **Dependabot alerts** for vulnerable dependencies
- **CodeQL findings** in Security tab

### Performance Monitoring
- **Performance regression** detection
- **Bundle size** tracking and alerts
- **Load test results** comparison

## Best Practices

### Code Quality
- **Automated formatting** enforcement
- **Linting rules** for consistency
- **Type checking** for JavaScript and Python
- **Test coverage** requirements

### Security
- **Secrets scanning** on every commit
- **Dependency vulnerability** monitoring
- **Container security** scanning
- **Infrastructure as Code** security validation

### Performance
- **Performance budgets** for frontend
- **Load testing** for backend APIs
- **Database performance** benchmarking
- **Resource usage** monitoring

### Deployment
- **Zero-downtime deployments** for production
- **Database migration** automation
- **Health check** validation
- **Rollback procedures** for failures

## Troubleshooting

### Common CI/CD Issues

#### 1. Test Failures
```bash
# Check test logs
gh run view [run-id] --log

# Run tests locally
./docker-dev.sh test
```

#### 2. Docker Build Issues
```bash
# Check Dockerfile syntax
docker build --dry-run -f backend/Dockerfile backend/

# Test build locally
./docker-dev.sh build
```

#### 3. Deployment Failures
```bash
# Check deployment logs
ssh user@server 'cd /opt/creatormate && docker compose logs'

# Manual rollback
ssh user@server 'cd /opt/creatormate && git checkout [previous-tag] && docker compose up -d'
```

#### 4. Security Scan Issues
```bash
# Run security scans locally
pip install safety bandit
safety check
bandit -r .

# Update vulnerable dependencies
pip install --upgrade [package-name]
```

### Performance Issues
```bash
# Run performance tests locally
ab -n 100 -c 10 http://localhost:8888/health

# Check resource usage
docker stats --no-stream
```

## Development Workflow

### Feature Development
1. Create feature branch: `git checkout -b feature/new-feature`
2. Develop and test locally
3. Create pull request to `develop`
4. CI pipeline runs automatically
5. Code review and merge
6. Feature deployed to staging

### Hotfix Process
1. Create hotfix branch: `git checkout -b fix/critical-issue`
2. Fix issue and test
3. Create pull request to `main`
4. Expedited review and merge
5. Emergency deployment to production

### Release Process
1. Merge `develop` to `main`
2. Create release tag: `git tag v1.0.0`
3. Push tag: `git push origin v1.0.0`
4. CD pipeline deploys to production
5. Monitor deployment and health checks

## Metrics and Reporting

### CI/CD Metrics
- **Build success rate**: Target >95%
- **Deployment frequency**: Multiple times per day
- **Lead time**: <24 hours from commit to production
- **Mean time to recovery**: <1 hour

### Quality Metrics  
- **Test coverage**: Target >80%
- **Security scan pass rate**: Target 100%
- **Performance regression**: <5% acceptable
- **Dependency freshness**: <30 days behind latest

### Security Metrics
- **Critical vulnerabilities**: 0 tolerance
- **Time to patch**: <24 hours for high severity
- **Secrets exposure**: 0 tolerance
- **Container scan score**: Target >8/10

This CI/CD pipeline ensures high code quality, security, and reliable deployments for CreatorMate while maintaining developer productivity and system reliability.