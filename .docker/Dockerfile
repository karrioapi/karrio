# The base image compilation
FROM python:3.8-slim AS compile-image
RUN python -m venv /pship/venv
ENV PATH="/pship/venv/bin:$PATH"

COPY requirements.txt /temp/
RUN pip install --upgrade pip && \
    pip install -r /temp/requirements.txt


# The runtime image
FROM python:3.8-slim AS build-image

LABEL maintainer=hello@purplship.com
LABEL org.opencontainers.image.title="Purplship Server"
LABEL org.opencontainers.image.description="Purplship Server runtime image"
LABEL org.opencontainers.image.url="https://purplship.com"
LABEL org.opencontainers.image.documentation="https://docs.purplship.com"
LABEL org.opencontainers.image.source="https://github.com/purplship/purplship-server"
LABEL org.opencontainers.image.vendor="Purplship Team."
LABEL org.opencontainers.image.authors="hello@purplship.com"

ENV DEBUG_MODE False
ENV USE_HTTPS False
ENV ALLOWED_HOSTS *
ENV SECRET_KEY "w;l5kj65lk6j;lj56kl56jk5l656j5k6jl5"
ENV WORK_DIR /pship/app
ENV LOG_DIR /pship/log
ENV STATIC_ROOT_DIR /pship/static

RUN useradd -m pship -d /pship
USER pship
COPY --chown=pship:pship --from=compile-image /pship/venv /pship/venv
RUN mkdir $WORK_DIR $LOG_DIR $STATIC_ROOT_DIR
WORKDIR $WORK_DIR


# Make sure we use the virtualenv:
ENV PATH="/pship/venv/bin:$PATH"

COPY gunicorn-cfg.py .docker/entrypoint.sh $WORK_DIR/
ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]
