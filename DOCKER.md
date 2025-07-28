# CreatorMate Docker Setup

This document provides comprehensive instructions for running CreatorMate using Docker containers.

## Quick Start

### Development Environment

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd CreatorMate
   cp .env.docker.example .env
   # Edit .env with your API keys
   ```

2. **Start development environment**:
   ```bash
   ./docker-dev.sh start
   ```

3. **Access the application**:
   - Frontend: http://localhost:5173 (Vite dev server with hot reload)
   - Backend API: http://localhost:8888
   - API Documentation: http://localhost:8888/docs
   - Redis: localhost:6379

### Production Environment

1. **Setup production environment**:
   ```bash
   cp .env.docker.example .env
   # Edit .env with production values
   ```

2. **Deploy to production**:
   ```bash
   ./docker-prod.sh deploy
   ```

3. **Access the application**:
   - Application: http://localhost
   - Backend API: http://localhost:8888
   - Health Check: http://localhost/health

## Architecture

### Services

- **backend**: FastAPI application with AI agents
- **frontend**: React TypeScript application served by Nginx
- **redis**: Session management and caching
- **prometheus** (optional): Metrics collection
- **grafana** (optional): Monitoring dashboards

### Network Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Frontend     │    │     Backend     │    │      Redis      │
│   (React SPA)   │◄──►│   (FastAPI)     │◄──►│   (Session)     │
│   Port: 80      │    │   Port: 8888    │    │   Port: 6379    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌─────────────────────────────────────┐
         │          Docker Network             │
         │        (creatormate_network)        │
         └─────────────────────────────────────┘
```

## Configuration

### Environment Variables

Key environment variables that need to be configured:

```bash
# Required API Keys
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key  
YOUTUBE_API_KEY=your_youtube_key

# Security
BOSS_AGENT_SECRET_KEY=your_secret_key
SESSION_SECRET_KEY=your_session_key
REDIS_PASSWORD=your_redis_password

# Environment
ENVIRONMENT=production|development
LOG_LEVEL=INFO|DEBUG
DEBUG=false|true
```

### Volume Mounts

#### Production Volumes
- `backend_data`: Application database and user data
- `backend_logs`: Application logs
- `backend_backups`: Database backups
- `redis_data`: Redis persistence
- `prometheus_data`: Prometheus metrics (optional)
- `grafana_data`: Grafana dashboards (optional)

#### Development Volumes
- Source code is mounted for hot reloading
- Development-specific data volumes

## Management Scripts

### Development Script (`docker-dev.sh`)

```bash
# Start all services
./docker-dev.sh start

# View logs
./docker-dev.sh logs [service]

# Stop services
./docker-dev.sh stop

# Build services  
./docker-dev.sh build

# Access shell
./docker-dev.sh shell [service]

# Run tests
./docker-dev.sh test

# Clean up
./docker-dev.sh clean
```

### Production Script (`docker-prod.sh`)

```bash
# Deploy to production
./docker-prod.sh deploy

# Update deployment
./docker-prod.sh update

# View status and health
./docker-prod.sh status

# Create backup
./docker-prod.sh backup

# Start monitoring
./docker-prod.sh monitoring
```

## Development Workflow

### Hot Reloading

- **Backend**: Uvicorn auto-reload enabled, source code mounted
- **Frontend**: Vite dev server with HMR, source code mounted

### Debugging

- **Backend**: Debug port 5678 exposed for Python debugging
- **Logs**: Real-time log viewing with structured output
- **Database**: Development SQLite database persisted in volume

### Development Tools

Enable development tools profile:
```bash
docker compose -f docker-compose.dev.yml --profile tools up -d
```

Access points:
- **Adminer** (DB admin): http://localhost:8080
- **Redis Commander**: http://localhost:8081  
- **Mailhog** (Email testing): http://localhost:8025

## Production Deployment

### Security Features

- **Non-root containers**: All services run as non-root users
- **Secrets management**: Sensitive data via environment variables
- **Network isolation**: Services communicate via internal network
- **Health checks**: Built-in health monitoring
- **Security headers**: Nginx configured with security headers

### Performance Optimizations

- **Multi-stage builds**: Minimal production images
- **Nginx caching**: Static asset caching and compression
- **Redis caching**: Session and application caching
- **Resource limits**: Memory and CPU limits configured

### Monitoring

Start monitoring stack:
```bash
./docker-prod.sh monitoring
```

Access monitoring:
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

## Troubleshooting

### Common Issues

1. **Port conflicts**:
   ```bash
   # Check which process is using port
   lsof -i :8888
   # Kill process or change port in .env
   ```

2. **Permission issues**:
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

3. **Environment variables not loaded**:
   ```bash
   # Verify .env file exists and has correct values
   cat .env | grep API_KEY
   ```

4. **Database connection issues**:
   ```bash
   # Check database volume
   docker volume inspect creatormate_backend_data
   ```

### Logs and Debugging

View service logs:
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend

# With timestamps
docker compose logs -f -t backend
```

Access container shell:
```bash
# Backend container
docker compose exec backend /bin/sh

# Frontend container  
docker compose exec frontend /bin/sh
```

### Performance Monitoring

Monitor resource usage:
```bash
# Container stats
docker stats

# Service-specific stats
docker compose top backend
```

## Backup and Recovery

### Automated Backups

The backend service includes automated backup functionality:

```bash
# Create manual backup
./docker-prod.sh backup

# List backups (from container)
docker compose exec backend python -c "
from backup_service import get_backup_service
service = get_backup_service('/app/data/creatormate.db')
for backup in service.migration_manager.list_backups():
    print(f'{backup.backup_id}: {backup.created_at}')
"
```

### Data Recovery

1. **Stop services**:
   ```bash
   ./docker-prod.sh stop
   ```

2. **Restore from backup**:
   ```bash
   # Copy backup file to volume
   docker run --rm -v creatormate_backend_data:/data -v $(pwd)/backups:/backups alpine cp /backups/backup_file.db /data/creatormate.db
   ```

3. **Restart services**:
   ```bash
   ./docker-prod.sh start
   ```

## Scaling and Performance

### Horizontal Scaling

To scale backend services:
```bash
docker compose up -d --scale backend=3
```

Add load balancer configuration for multiple backend instances.

### Performance Tuning

1. **Adjust worker processes**:
   ```bash
   # In Dockerfile, modify CMD
   CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker"]
   ```

2. **Redis memory optimization**:
   ```bash
   # In redis.conf
   maxmemory 512mb
   maxmemory-policy allkeys-lru
   ```

3. **Nginx optimization**:
   ```bash
   # In nginx.conf
   worker_processes auto;
   worker_connections 2048;
   ```

## Security Considerations

### Production Security Checklist

- [ ] All API keys properly configured
- [ ] Redis password set
- [ ] Session secrets configured  
- [ ] Non-root containers used
- [ ] Security headers enabled
- [ ] Network isolation configured
- [ ] Volume permissions secured
- [ ] Log access restricted
- [ ] Regular security updates

### Network Security

- Services communicate via internal Docker network
- Only necessary ports exposed to host
- Nginx acts as reverse proxy for backend
- Redis not directly accessible from outside

## Maintenance

### Regular Tasks

1. **Update containers**:
   ```bash
   ./docker-prod.sh update
   ```

2. **Clean up unused resources**:
   ```bash
   docker system prune -a --volumes
   ```

3. **Monitor disk usage**:
   ```bash
   docker system df
   ```

4. **Backup database**:
   ```bash
   ./docker-prod.sh backup
   ```

### Health Monitoring

The application includes built-in health checks:
- Backend: http://localhost:8888/health
- Frontend: http://localhost/
- Detailed health: http://localhost:8888/api/health/system

Monitor these endpoints for service health.