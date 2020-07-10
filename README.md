# PurplShip (Multi-carrier private cloud shipping API)

[![Join the chat at https://gitter.im/PurplShip/purplship](https://badges.gitter.im/PurplShip/purplship.svg)](https://gitter.im/PurplShip/purplship?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

## Introduction

purplship-server is a private cloud Multi-carrier Shipping API.


## Documentation

PurplShip has usage and reference documentation at [docs.purplship.com](https://docs.purplship.com).


## Try out PurplShip

### Docker

- Docker Image

```shell script
docker run -p80:8000 purplship/purplship-server:2020.7.0 
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
    image: purplship/purplship-server:2020.7.0
    restart: always
    environment:
      - DEBUG_MODE=True
      - ALLOWED_HOSTS=*
      - DATABASE_HOST=db
      - DATABASE_PORT=5432
      - DATABASE_NAME=db
      - DATABASE_ENGINE=postgresql_psycopg2
      - DATABASE_USERNAME=postgres
      - DATABASE_PASSWORD=postgres
    ports:
      - "80:8000"
    depends_on:
      - db
```

```shell script
docker-compose up
```


### Using Pip (For development)

#### OS Requirements

Python >= 3.7 

#### Install

Create a python virtual environment using [python venv](https://docs.python.org/3/tutorial/venv.html)
```shell script
python -m venv env
```

Download the latest version freeze
```shell script
curl -L -O https://raw.githubusercontent.com/PurplShip/purplship-server/main/requirements.txt
```

```shell script
pip install -r requirements.txt
```

#### Initialize database (Demo)

```shell script
purplship makemigrations
purplship migrate
purplship collectstatic --noinput
purplship createsuperuser
# Enter your credentials in the prompt
```

#### Start the server (Demo)

```shell script
purplship runserver 0.0.0.0:8000
```
