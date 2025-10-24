# Install dependencies only when needed
FROM node:22.5.1-alpine3.19 AS builder
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY . .
RUN npm ci -w apps/dashboard
RUN npm run build -w apps/dashboard && \
    rm -rf node_modules && \
    npm install --omit=dev --ignore-scripts --prefer-offline -w apps/dashboard

# Production image, copy all the files and run next
FROM node:22.5.1-alpine3.19 AS runner
RUN apk add curl

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
ENV NEXT_PUBLIC_KARRIO_PUBLIC_URL=http://locahost:5002

RUN addgroup -g 1001 -S nodejs
RUN adduser -S karrio -u 1001
USER karrio


COPY --from=builder /app/apps/dashboard/public ./public
COPY --from=builder /app/apps/dashboard/next.config.mjs ./
COPY --from=builder --chown=karrio:nodejs /app/apps/dashboard/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/apps/dashboard/package.json ./package.json
COPY --from=builder /app/docker/dashboard/entrypoint ./entrypoint


EXPOSE 3002

CMD ["/bin/sh", "./entrypoint"]
