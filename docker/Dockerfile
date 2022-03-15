# The base image compilation
FROM python:3.8-slim AS compile-image

ARG REQUIREMENTS="requirements.txt"
ARG REGISTRY_TOKEN
ARG REGISTRY_TOKEN_NAME

RUN python -m venv /pship/venv
ENV PATH="/pship/venv/bin:$PATH"
COPY "${REQUIREMENTS}" /temp/
RUN pip install --upgrade pip && \
    pip install dumb-init && \
    pip install -r "/temp/${REQUIREMENTS}"


# The runtime image
FROM python:3.8-slim AS build-image

LABEL maintainer=hello@karrio.io
LABEL org.opencontainers.image.title="karrio server"
LABEL org.opencontainers.image.description="karrio server runtime image"
LABEL org.opencontainers.image.url="https://karrio.io"
LABEL org.opencontainers.image.documentation="https://docs.karrio.io"
LABEL org.opencontainers.image.source="https://github.com/karrio-inc/karrio-server"
LABEL org.opencontainers.image.vendor="team karrio"
LABEL org.opencontainers.image.authors="hello@karrio.io"

ENV DEBUG_MODE False
ENV USE_HTTPS False
ENV ALLOWED_HOSTS *
ENV KARRIO_WORKERS 2
ENV BACKGROUND_WORKERS 2
ENV DETACHED_WORKER False
ENV ADMIN_EMAIL admin@example.com
ENV ADMIN_PASSWORD demo
ENV SECRET_KEY "w;l5kj65lk6j;lj56kl56jk5l656j5k6jl5"
ENV WORK_DIR /pship/app
ENV LOG_DIR /pship/log
ENV WORKER_DB_DIR /pship/data
ENV STATIC_ROOT_DIR /pship/static

RUN useradd -m pship -d /pship
USER pship
COPY --chown=pship:pship --from=compile-image /pship/ /pship/
RUN mkdir -p $WORK_DIR $LOG_DIR $WORKER_DB_DIR $STATIC_ROOT_DIR
COPY server/gunicorn-cfg.py docker/entrypoint.sh docker/worker.sh $WORK_DIR/

WORKDIR $WORK_DIR

# Make sure we use the virtualenv:
ENV PATH="/pship/venv/bin:$PATH"

ENTRYPOINT ["/pship/venv/bin/dumb-init", "--"]
CMD ["./entrypoint.sh"]
