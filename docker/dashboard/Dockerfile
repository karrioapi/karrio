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
ARG VERSION
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1
ENV SENTRY_IGNORE_API_RESOLUTION_ERROR 1
ENV NEXTAUTH_SECRET "nasdlfij34l5kj5k6j5kl6lp+lsick5bi*90!mbk7rc3iy_op1r"
ENV NEXT_PUBLIC_KARRIO_PUBLIC_URL http://locahost:5002
ENV NEXT_PUBLIC_DASHBOARD_URL http://localhost:3000
ENV NEXT_PUBLIC_DASHBOARD_VERSION ${VERSION}

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
