# The base image compilation
FROM python:3.10-slim

WORKDIR /code

RUN apt-get update -y && apt-get install -y gcc libpango1.0-0 libpangoft2-1.0-0 ghostscript
RUN python -m venv /karrio/venv
ENV PATH="/karrio/venv/bin:$PATH"

COPY requirements.server.dev.txt /temp/requirements.txt
COPY . .
RUN pip install --upgrade pip && \
    pip install -r /temp/requirements.txt

EXPOSE 5002

CMD ["karrio", "runserver", "0.0.0.0:5002"]
