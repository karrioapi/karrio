# The base image compilation
FROM python:3.11-slim AS compile-image


RUN apt-get update -y && apt-get install -y gcc
RUN python -m venv /karrio/venv
ENV PATH="/karrio/venv/bin:$PATH"
COPY .build /temp/app/
RUN cd /temp/app && \
    pip install --upgrade pip && \
    pip install dumb-init && \
    pip install -r ./source.requirements.insiders.txt


# The runtime image
FROM python:3.11-slim AS build-image

LABEL maintainer=hello@karrio.io
LABEL org.opencontainers.image.title="karrio server"
LABEL org.opencontainers.image.description="karrio server runtime image"
LABEL org.opencontainers.image.url="https://karrio.io"
LABEL org.opencontainers.image.documentation="https://docs.karrio.io"
LABEL org.opencontainers.image.source="https://github.com/karrioapi/karrio-insiders"
LABEL org.opencontainers.image.vendor="team karrio"
LABEL org.opencontainers.image.authors="hello@karrio.io"

ENV DEBUG_MODE False
ENV USE_HTTPS False
ENV ALLOWED_HOSTS *
ENV KARRIO_WORKERS 2
ENV BACKGROUND_WORKERS 2
ENV DETACHED_WORKER False
ENV ADMIN_DASHBOARD False
ENV MULTI_ORGANIZATIONS True
ENV ALLOW_MULTI_ACCOUNT True
ENV ADMIN_EMAIL admin@example.com
ENV ADMIN_PASSWORD demo
ENV SECRET_KEY "w;l5kj65lk6j;lj56kl56jk5l656j5k6jl5"
ENV WORK_DIR /karrio/app
ENV LOG_DIR /karrio/log
ENV WORKER_DB_DIR /karrio/data
ENV STATIC_ROOT_DIR /karrio/static

RUN apt-get update -y && apt-get install -y libpango1.0-0 libpangoft2-1.0-0 gcc ghostscript curl

RUN useradd -m karrio -d /karrio
USER karrio

COPY --chown=karrio:karrio --from=compile-image /karrio/ /karrio/
RUN mkdir -p $WORK_DIR $LOG_DIR $WORKER_DB_DIR $STATIC_ROOT_DIR
COPY .build/api/gunicorn-cfg.py docker/insiders/entrypoint docker/insiders/worker $WORK_DIR/

WORKDIR $WORK_DIR

# Make sure we use the virtualenv:
ENV PATH="/karrio/venv/bin:$PATH"

ENTRYPOINT ["/karrio/venv/bin/dumb-init", "--"]
CMD ["./entrypoint"]
