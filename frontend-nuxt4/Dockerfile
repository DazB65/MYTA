# Nuxt 4 Dockerfile (Nitro)
# Multi-stage build to produce a self-contained server on port 80

# 1) Build Stage
FROM node:20-alpine AS build
WORKDIR /app

# Install dependencies (use package-lock for reproducible builds)
COPY package.json package-lock.json ./
RUN npm ci

# Copy source
COPY . .

# Build Nitro output
RUN npm run build

# 2) Runtime Stage
FROM node:20-alpine AS production
ENV NODE_ENV=production
WORKDIR /app

# Copy .output which contains server and public assets
COPY --from=build /app/.output ./.output

# Expose and run Nitro server
ENV NITRO_HOST=0.0.0.0
ENV NITRO_PORT=80
EXPOSE 80
CMD ["node", ".output/server/index.mjs"]

