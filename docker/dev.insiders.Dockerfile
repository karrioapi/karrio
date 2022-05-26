# The base image compilation
FROM python:3.8-slim AS compile-image
RUN python -m venv /karrio/venv
ENV PATH="/karrio/venv/bin:$PATH"
COPY . /karrio/app/
RUN cd /karrio/app && \
    pip install -r requirements.dev.txt --upgrade && \
    pip install -r requirements.server.insiders.dev.txt


# The runtime image
FROM python:3.8-slim AS build-image

RUN apt-get update -y && apt-get install -y libpango1.0-0 libpangoft2-1.0-0
RUN useradd -m karrio -d /karrio
USER karrio
COPY --chown=karrio:karrio --from=compile-image /karrio/ /karrio/
RUN mkdir -p /karrio/.karrio

WORKDIR /karrio/app

# Make sure we use the virtualenv:
ENV PATH="/karrio/venv/bin:$PATH"
EXPOSE 5002
ENV PORT 5002
