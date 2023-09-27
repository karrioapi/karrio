# The base image compilation
FROM python:3.10-slim


RUN apt-get update -y && apt-get install -y gcc libpango1.0-0 libpangoft2-1.0-0 ghostscript

WORKDIR /karrio
ENV PATH="/karrio/.venv/karrio/bin:$PATH"
EXPOSE 5002

ENV PORT 5002