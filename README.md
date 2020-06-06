# PurplShip (Multi-carrier private cloud shipping API)

## Introduction

purplship-server is a private cloud Multi-carrier Shipping API.


## Documentation

PurplShip has usage and reference documentation at [docs.purplship.com](https://docs.purplship.com).


## Try out PurplShip

### Docker

- Docker Image

```shell script
docker run \
  -p80:8000 \
  --name=pship --rm \
  --volume=$(pwd):/app \
  --interactive --tty purplship/purplship-server:2020.4.1 \
  /bin/bash -c "purplship makemigrations && purplship migrate && purplship createsuperuser ; purplship runserver 0.0.0.0:8000"
```

- Docker Compose

create a configuration file

```shell script
echo > docker-compose.yml
```

paste this configuration
```yaml
version: '3'

services:
  db:
    image: postgres
    restart: always
    environment:
      POSTGRES_DB: "db"
      POSTGRES_USER: "postgres"
      POSTGRES_PASSWORD: "postgres"
  web:
    image: purplship/purplship-server:2020.4.1
    restart: always
    entrypoint: |
      bash -c "bash -s <<EOF
      purplship makemigrations &&
      purplship migrate &&
      (echo \"from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'demo')\" | purplship shell) > /dev/null 2>&1;
      purplship runserver 0.0.0.0:8000
      EOF"
    environment:
      - DEBUG_MODE=True
      - DJANGO_ALLOWED_HOSTS=*
      - DATABASE_HOST=db
      - DATABASE_PORT=5432
      - DATABASE_NAME=db
      - DATABASE_ENGINE=postgresql_psycopg2
      - DATABASE_USERNAME=postgres
      - DATABASE_PASSWORD=postgres
    volumes:
      - .:/app
    ports:
      - "80:8000"
    depends_on:
      - db
```

```shell script
docker-compose up
```


### Using Pip (For development)

- OS Requirements

Python >= 3.7 

- Install

create a python virtual environment using [python venv](https://docs.python.org/3/tutorial/venv.html)

```shell script
pip install -f https://git.io/purplship purplship-server==2020.6.1
```

- Initialize database (Demo)

```shell script
purplship makemigrations
purplship migrate
purplship createsuperuser
# Enter your credentials in the prompt
```

- Start the server (Demo)

```shell script
purplship runserver 0.0.0.0:8000
```
