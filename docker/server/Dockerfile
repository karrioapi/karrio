# The base image compilation
FROM python:3.12.10-slim AS compile-image

ARG REQUIREMENTS=./requirements.build.txt

RUN apt-get update -y && apt-get install -y gcc
RUN python -m venv /karrio/venv
ENV PATH="/karrio/venv/bin:$PATH"
COPY . /karrio/src/
RUN cd /karrio/src && \
    pip install --upgrade pip && \
    pip install dumb-init && \
    pip install -r ${REQUIREMENTS}


# The runtime image
FROM python:3.12.10-slim AS build-image

ARG VERSION
ARG EDITION="jtl"
ARG SOURCE="https://github.com/jtlshipping/shipping-platform"

LABEL maintainer=hello@jtl.io
LABEL org.opencontainers.image.title="JTL Shipping Platform Dashboard"
LABEL org.opencontainers.image.description="JTL shipping platform dashboard runtime image"
LABEL org.opencontainers.image.url="https://www.jtl-software.de/"
LABEL org.opencontainers.image.source=${SOURCE}
LABEL org.opencontainers.image.vendor="JTL"

ENV DEBUG_MODE=False
ENV USE_HTTPS=False
ENV ALLOWED_HOSTS=*
ENV KARRIO_WORKERS=2
ENV BACKGROUND_WORKERS=2
ENV DETACHED_WORKER=False
ENV ADMIN_DASHBOARD=False
ENV MULTI_ORGANIZATIONS=True
ENV ALLOW_MULTI_ACCOUNT=True
ENV ADMIN_EMAIL=admin@example.com
ENV ADMIN_PASSWORD=demo
ENV WORK_DIR=/karrio/app
ENV LOG_DIR=/karrio/log
ENV WORKER_DB_DIR=/karrio/data
ENV STATIC_ROOT_DIR=/karrio/static
ENV KARRIO_PLUGINS=/karrio/plugins
ENV ENABLE_ALL_PLUGINS_BY_DEFAULT=True

RUN apt-get update -y && apt-get install -y libpango1.0-0 libpangoft2-1.0-0 gcc zint curl netcat-openbsd

RUN useradd -m karrio -d /karrio
USER karrio

COPY --chown=karrio:karrio --from=compile-image /karrio/ /karrio/
RUN mkdir -p $WORK_DIR $LOG_DIR $WORKER_DB_DIR $STATIC_ROOT_DIR $KARRIO_PLUGINS
COPY --chown=karrio:karrio karrio/apps/api/gunicorn-cfg.py docker/server/entrypoint docker/server/worker $WORK_DIR/
COPY --chown=karrio:karrio karrio/plugins/ $KARRIO_PLUGINS/

# Copy source for editable installs to work
COPY --chown=karrio:karrio --from=compile-image /karrio/src /karrio/src

WORKDIR $WORK_DIR

# Make sure we use the virtualenv:
ENV PATH="/karrio/venv/bin:$PATH"

ENTRYPOINT ["/karrio/venv/bin/dumb-init", "--"]
CMD ["./entrypoint"]
