# The base image compilation
FROM python:3.8-slim AS compile-image
RUN python -m venv /pship/venv
ENV PATH="/pship/venv/bin:$PATH"
COPY . /pship/app/
RUN cd /pship/app && \
     pip install --upgrade pip && \
    pip install -r requirements.ee.dev.txt


# The runtime image
FROM python:3.8-slim AS build-image

RUN useradd -m pship -d /pship
USER pship
COPY --chown=pship:pship --from=compile-image /pship/ /pship/

WORKDIR /pship

# Make sure we use the virtualenv:
ENV PATH="/pship/venv/bin:$PATH"
