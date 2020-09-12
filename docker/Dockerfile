FROM python:3.8

LABEL maintainer="hello@purplship.com"
LABEL org.opencontainers.image.title="PurplShip Server"
LABEL org.opencontainers.image.description="PurplShip Server runtime image"
LABEL org.opencontainers.image.url="https://purplship.com"
LABEL org.opencontainers.image.documentation="https://docs.purplship.com"
LABEL org.opencontainers.image.source="https://github.com/purplship/purplship-server"
LABEL org.opencontainers.image.vendor="PurplShip Software, Inc."
LABEL org.opencontainers.image.authors="hello@purplship.com"

ENV DEBUG_MODE False
ENV USE_HTTPS False
ENV ALLOWED_HOSTS *
ENV ADMIN_USERNAME "admin"
ENV ADMIN_PASSWORD "demo"
ENV PURPLSHIP_PORT 8000
ENV WORK_DIR "/app"

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /temp/
COPY gunicorn-cfg.py docker/docker-entrypoint.sh /app/

RUN pip install --upgrade pip \
    pip install -r /temp/requirements.txt \
    pip freeze

RUN chmod +x docker-entrypoint.sh

EXPOSE $PURPLSHIP_PORT
ENTRYPOINT ["/bin/bash", "./docker-entrypoint.sh"]
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "purpleserver.wsgi"]
