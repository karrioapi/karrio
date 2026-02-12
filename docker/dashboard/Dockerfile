# ── Stage 1: base ────────────────────────────────────────────────
FROM node:22.5.1-alpine3.19 AS base
RUN apk add --no-cache libc6-compat
RUN npm install -g turbo@^2

# ── Stage 2: prune ───────────────────────────────────────────────
FROM base AS prune
WORKDIR /app
COPY . .
RUN turbo prune @karrio/dashboard --docker

# ── Stage 3: builder ────────────────────────────────────────────
FROM base AS builder
WORKDIR /app

# Install dependencies first (cached layer)
COPY --from=prune /app/out/json/ .
RUN npm ci

# Copy source and build
COPY --from=prune /app/out/full/ .

ARG NEXT_PUBLIC_DASHBOARD_VERSION
ENV NEXT_PUBLIC_DASHBOARD_VERSION=${NEXT_PUBLIC_DASHBOARD_VERSION}
ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build -w apps/dashboard

# ── Stage 4: runner ──────────────────────────────────────────────
FROM node:22.5.1-alpine3.19 AS runner
RUN apk add --no-cache curl

ARG VERSION
ARG SOURCE="https://github.com/karrioapi/karrio"

LABEL maintainer=hello@karrio.io
LABEL org.opencontainers.image.title="karrio dashboard"
LABEL org.opencontainers.image.description="karrio dashboard runtime image"
LABEL org.opencontainers.image.url="https://karrio.io"
LABEL org.opencontainers.image.documentation="https://docs.karrio.io"
LABEL org.opencontainers.image.source=${SOURCE}
LABEL org.opencontainers.image.vendor="team karrio"
LABEL org.opencontainers.image.authors="hello@karrio.io"

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV SENTRY_IGNORE_API_RESOLUTION_ERROR=1
ENV NEXT_PUBLIC_DASHBOARD_VERSION=${VERSION}
ENV NEXT_PUBLIC_DASHBOARD_URL=http://localhost:3002
ENV NEXT_PUBLIC_KARRIO_PUBLIC_URL=http://localhost:5002

RUN addgroup -g 1001 -S nodejs
RUN adduser -S karrio -u 1001
USER karrio

# Standalone output: self-contained server + traced node_modules
COPY --from=builder --chown=karrio:nodejs /app/apps/dashboard/.next/standalone ./
# Static assets (CSS/JS chunks not included in standalone)
COPY --from=builder --chown=karrio:nodejs /app/apps/dashboard/.next/static ./apps/dashboard/.next/static
# Public assets (including CopyWebpackPlugin app-store assets)
COPY --from=builder --chown=karrio:nodejs /app/apps/dashboard/public ./apps/dashboard/public
# Entrypoint script
COPY --from=builder /app/docker/dashboard/entrypoint ./entrypoint

EXPOSE 3002

CMD ["/bin/sh", "./entrypoint"]
