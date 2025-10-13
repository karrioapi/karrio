# Build stage
FROM node:22-alpine AS builder

RUN apk add --no-cache libc6-compat

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./
COPY apps/dashboard/package.json ./apps/dashboard/

# Install dependencies
RUN npm ci --force

# Copy application source
COPY apps/dashboard ./apps/dashboard

# Build the dashboard
WORKDIR /app/apps/dashboard
RUN npm run build

# Production stage
FROM node:22-alpine AS runner

RUN apk add --no-cache curl

ARG VERSION
ARG SOURCE="https://github.com/jtlshipping/shipping-platform"

LABEL maintainer=hello@jtl.io
LABEL org.opencontainers.image.title="JTL Shipping Platform Dashboard"
LABEL org.opencontainers.image.description="JTL shipping platform dashboard runtime image"
LABEL org.opencontainers.image.url="https://www.jtl-software.de/"
LABEL org.opencontainers.image.source=${SOURCE}
LABEL org.opencontainers.image.vendor="JTL"

WORKDIR /app

ENV NODE_ENV=production
ENV DASHBOARD_PORT=3102

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S jtl -u 1001

# Copy built application and dependencies
COPY --from=builder --chown=jtl:nodejs /app/apps/dashboard/dist ./dist
COPY --from=builder --chown=jtl:nodejs /app/apps/dashboard/package.json ./package.json
COPY --from=builder --chown=jtl:nodejs /app/node_modules ./node_modules

# Ensure jtl user owns everything
RUN chown -R jtl:nodejs /app

# Copy runtime server entry point
COPY docker/dashboard/server-entry.mjs ./server-entry.mjs

# Copy entrypoint script
COPY docker/dashboard/entrypoint ./entrypoint
RUN chmod +x ./entrypoint

USER jtl

EXPOSE 3102

CMD ["/bin/sh", "./entrypoint"]
