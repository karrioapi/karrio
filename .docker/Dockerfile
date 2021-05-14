FROM python:3.8

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

ENV WORK_DIR /app
ENV LOG_DIR /log
ENV STATIC_ROOT_DIR /static

EXPOSE $PURPLSHIP_PORT

RUN mkdir /app /log /static
WORKDIR /app

COPY requirements.txt /temp/
COPY gunicorn-cfg.py .docker/entrypoint.sh licenses/APACHE-LICENSE-2.0 /app/

RUN pip install --upgrade pip \
    pip install -r /temp/requirements.txt

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]
