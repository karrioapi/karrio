FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV DEBUG_MODE False
ENV USE_HTTPS False
ENV ALLOWED_HOSTS *
ENV ADMIN_USERNAME "admin"
ENV ADMIN_PASSWORD "demo"
ENV PURPLSHIP_PORT 8000
ENV WORK_DIR "/app"

RUN mkdir /app
WORKDIR /app
VOLUME /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt && \
    pip freeze

COPY docker-entrypoint.sh /app/
RUN chmod +x docker-entrypoint.sh

EXPOSE $PURPLSHIP_PORT
ENTRYPOINT ["/bin/bash", "./docker-entrypoint.sh"]

CMD ["purplship runserver 0.0.0.0:$PURPLSHIP_PORT"]
