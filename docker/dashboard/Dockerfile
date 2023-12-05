# Install dependencies only when needed
FROM node:21.2.0-alpine3.17 AS deps
# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine to understand why libc6-compat might be needed.
RUN apk add --no-cache libc6-compat

# Rebuild the source code only when needed
FROM node:21.2.0-alpine3.17 AS builder
WORKDIR /app
COPY . .
RUN npm ci -w apps/dashboard 
RUN npm run build -w apps/dashboard && \
  rm -rf node_modules && \
  npm install --omit=dev --ignore-scripts --prefer-offline -w apps/dashboard

# Production image, copy all the files and run next
FROM node:21.2.0-alpine3.17 AS runner
ARG VERSION
WORKDIR /app

ENV NEXT_TELEMETRY_DISABLED 1
ENV SENTRY_IGNORE_API_RESOLUTION_ERROR 1
ENV NODE_ENV production
ENV JWT_SECRET "nasdlfij34l5kj5k6j5kl6lp+lsick5bi*90!mbk7rc3iy_op1r"
ENV KARRIO_PUBLIC_URL https://api.karrio.io
ENV DASHBOARD_URL http://localhost:3000
ENV DASHBOARD_VERSION ${VERSION}

RUN addgroup -g 1001 -S nodejs
RUN adduser -S karrio -u 1001


COPY --from=builder /app/apps/dashboard/public ./public
COPY --from=builder /app/apps/dashboard/next.config.js ./
COPY --from=builder --chown=karrio:nodejs /app/apps/dashboard/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/apps/dashboard/package.json ./package.json
COPY --from=builder /app/docker/dashboard/entrypoint ./entrypoint

USER karrio

EXPOSE 3000

CMD ["/bin/sh", "./entrypoint"]
