# Purplship (Multi-carrier private cloud shipping API)

[![CI](https://github.com/PurplShip/purplship-server/workflows/PuprlShip-Server/badge.svg)](https://github.com/PurplShip/purplship-server/actions)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Join the chat at https://gitter.im/PurplShip/purplship](https://badges.gitter.im/PurplShip/purplship.svg)](https://gitter.im/PurplShip/purplship?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

## Introduction

purplship-server is a private cloud Multi-carrier Shipping API.


## Documentation

Purplship has usage and reference documentation at [docs.purplship.com](https://docs.purplship.com).


## Try out purplship

### Docker

#### Docker Image


<details>
<summary>Start a postgres SQL Database Instance</summary>

```bash
docker run -d --name db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres postgres
```

</details>

```shell script
docker run --name purplship --link=db:db -p5002:5002 purplship/purplship-server:2020.8.2
```

#### Docker Compose

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
    image: purplship/purplship-server:2020.8.2
    restart: always
    environment:
      - DEBUG_MODE=True
      - ALLOWED_HOSTS=*
      - DATABASE_HOST=db
      - DATABASE_PORT=5432
      - DATABASE_NAME=db
      - DATABASE_USERNAME=postgres
      - DATABASE_PASSWORD=postgres
    ports:
      - "5002:5002"
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

#### Initialize the data (Demo)

Make sure to have a running postgres SQL database instance running

- Set database connection environment variables

```bash
export DATABASE_HOST=database
export DATABASE_PORT=5432
export DATABASE_NAME=db
export DATABASE_USERNAME=postgres
export DATABASE_PASSWORD=postgres
```

- Initialize database and admin user

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
