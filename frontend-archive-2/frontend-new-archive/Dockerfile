# Vidalytics Frontend Dockerfile
# Multi-stage build for React TypeScript application

# =============================================================================
# Build Stage
# =============================================================================
FROM node:18-alpine as builder

# Set build arguments
ARG BUILD_ENV=production
ARG BUILD_DATE
ARG VCS_REF
ARG VITE_API_BASE_URL=http://localhost:8888

# Set metadata labels
LABEL maintainer="Vidalytics Team" \
      org.opencontainers.image.title="Vidalytics Frontend" \
      org.opencontainers.image.description="React TypeScript frontend for Vidalytics" \
      org.opencontainers.image.version="2.0.0" \
      org.opencontainers.image.created=$BUILD_DATE \
      org.opencontainers.image.revision=$VCS_REF

# Install build dependencies
RUN apk add --no-cache git

# Set working directory
WORKDIR /app

# Copy package files first (for better layer caching)
COPY package*.json ./
COPY yarn.lock* ./

# Install dependencies
RUN if [ -f "yarn.lock" ]; then \
        yarn install --frozen-lockfile --production=false; \
    else \
        npm ci; \
    fi

# Copy source code
COPY . .

# Set build environment variables
ENV NODE_ENV=production \
    VITE_API_BASE_URL=$VITE_API_BASE_URL \
    GENERATE_SOURCEMAP=false

# Build the application
RUN if [ -f "yarn.lock" ]; then \
        yarn build; \
    else \
        npm run build; \
    fi

# =============================================================================
# Production Stage (Nginx)
# =============================================================================
FROM nginx:alpine as production

# Install curl for health checks
RUN apk add --no-cache curl

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf

# Copy built application from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy startup script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Create nginx user directories
RUN mkdir -p /var/cache/nginx /var/log/nginx /var/run && \
    chown -R nginx:nginx /var/cache/nginx /var/log/nginx /var/run /usr/share/nginx/html

# Set environment variables
ENV NGINX_PORT=80 \
    NGINX_HOST=localhost \
    API_BASE_URL=http://backend:8888

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:$NGINX_PORT/ || exit 1

# Switch to non-root user
USER nginx

# Expose port
EXPOSE 80

# Start nginx
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]

# =============================================================================
# Development Stage
# =============================================================================
FROM node:18-alpine as development

# Install development tools
RUN apk add --no-cache git curl vim

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY yarn.lock* ./

# Install all dependencies (including dev dependencies)
RUN if [ -f "yarn.lock" ]; then \
        yarn install --frozen-lockfile; \
    else \
        npm ci; \
    fi

# Copy source code
COPY . .

# Set development environment variables
ENV NODE_ENV=development \
    VITE_API_BASE_URL=http://localhost:8888 \
    CHOKIDAR_USEPOLLING=true

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 -G nodejs

# Change ownership of app directory
RUN chown -R nextjs:nodejs /app

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 5173

# Start development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]