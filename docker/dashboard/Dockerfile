# Build stage
FROM node:22-alpine AS builder

RUN apk add --no-cache libc6-compat

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./
COPY apps/dashboard/package.json ./apps/dashboard/

# Install dependencies
# First remove package-lock.json and reinstall to get correct platform binaries
RUN rm -f package-lock.json && npm install --no-package-lock

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

# Copy built application and source (needed for vite preview with TanStack Start)
COPY --from=builder --chown=jtl:nodejs /app/apps/dashboard ./
COPY --from=builder --chown=jtl:nodejs /app/node_modules ../node_modules
COPY --from=builder --chown=jtl:nodejs /app/package.json ../package.json

# Update start script to use vite dev (TanStack Start SSR needs dev server)
RUN sed -i 's|node .output/server/index.mjs|vite dev --host 0.0.0.0 --port ${DASHBOARD_PORT:-3102}|g' ./package.json

# Ensure jtl user owns everything
RUN chown -R jtl:nodejs /app

# Copy entrypoint script
COPY docker/dashboard/entrypoint ./entrypoint
RUN chmod +x ./entrypoint

USER jtl

EXPOSE 3102

CMD ["/bin/sh", "./entrypoint"]
