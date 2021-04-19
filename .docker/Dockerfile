FROM python:3.8

ENV DEBUG_MODE False
ENV USE_HTTPS False
ENV ALLOWED_HOSTS *
ENV ADMIN_EMAIL admin@domain.com
ENV ADMIN_PASSWORD demo
ENV TENANT_ADMIN_EMAIL root@domain.com
ENV TENANT_ADMIN_PASSWORD demo
ENV PURPLSHIP_PORT 5002
ENV DATABASE_HOST db
ENV DATABASE_PORT 5432
ENV DATABASE_NAME postgres
ENV DATABASE_USERNAME postgres
ENV DATABASE_PASSWORD postgres
ENV WORK_DIR /app
ENV LOG_DIR /log

EXPOSE $PURPLSHIP_PORT

RUN mkdir /app /log
WORKDIR /app

COPY requirements.txt /temp/
COPY gunicorn-cfg.py .docker/go.sh .docker/entrypoint.sh licenses/APACHE-LICENSE-2.0 /app/

RUN pip install --upgrade pip \
    pip install -r /temp/requirements.txt

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]
CMD ["/bin/bash", "./go.sh"]


LABEL maintainer=hello@purplship.com
LABEL org.opencontainers.image.title="Purplship Server"
LABEL org.opencontainers.image.description="Purplship Server runtime image"
LABEL org.opencontainers.image.url="https://purplship.com"
LABEL org.opencontainers.image.documentation="https://docs.purplship.com"
LABEL org.opencontainers.image.source="https://github.com/purplship/purplship-server"
LABEL org.opencontainers.image.vendor="Purplship Team."
LABEL org.opencontainers.image.authors="hello@purplship.com"
