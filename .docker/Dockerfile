FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV DEBUG_MODE True
ENV DJANGO_ALLOWED_HOSTS *

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt