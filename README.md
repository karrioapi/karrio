<p align="center">
  <p align="center">
    <a href="https://purplship.com" target="_blank">
      <img src="https://github.com/PurplShip/purplship-server/raw/main/src/purpleserver/purpleserver/static/purpleserver/img/icon.png" alt="Purplship" height="100">
    </a>
  </p>
  <h2 align="center">
    The Open Source Multi-carrier Shipping API
  </h2>
  <p align="center">
    <a href="https://github.com/PurplShip/purplship-server/actions"><img src="https://github.com/PurplShip/purplship-server/workflows/PuprlShip-Server/badge.svg" alt="CI" style="max-width:100%;"></a>
    <a href="https://www.gnu.org/licenses/agpl-3.0" rel="nofollow"><img src="https://camo.githubusercontent.com/cb1d26ec555a33e9f09fe279b5edc49996a3bb3b/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4147504c25323076332d626c75652e737667" alt="License: AGPL v3" data-canonical-src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg" style="max-width:100%;"></a>
    <a href="https://gitter.im/PurplShip/purplship?utm_source=badge&amp;utm_medium=badge&amp;utm_campaign=pr-badge" rel="nofollow"><img src="https://camo.githubusercontent.com/01e8eacc7691f9db65721966fd30df70567aa1dc/68747470733a2f2f6261646765732e6769747465722e696d2f507572706c536869702f707572706c736869702e737667" alt="Join the chat at https://gitter.im/PurplShip/purplship" data-canonical-src="https://badges.gitter.im/PurplShip/purplship.svg" style="max-width:100%;"></a>
  </p>
</p>


## What's Purplship?

Purplship server is an On-prem or private cloud Multi-carrier Shipping API.
The server is in Python, but you can use any programming language to send API request to 
any supported shipping carriers (Canada Post, DHL, FedEx, UPS, Purolator...), in your application.

<p align="center">
  <img src="https://raw.githubusercontent.com/PurplShip/purplship-server/main/screenshots/api.png" width="200">
  <img src="https://raw.githubusercontent.com/PurplShip/purplship-server/main/screenshots/shipments.png" width="200">
  <img src="https://raw.githubusercontent.com/PurplShip/purplship-server/main/screenshots/create_label.png" width="200">
  <img src="https://raw.githubusercontent.com/PurplShip/purplship-server/main/screenshots/connections.png" width="200">
</p>


## Documentation

Purplship has usage and reference documentation at [docs.purplship.com](https://docs.purplship.com).


## Try out Purplship

### Docker

#### Docker Image


<details>
<summary>Start a postgres SQL Database Instance</summary>

```bash
docker run -d --name db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres postgres
```

</details>

```shell script
docker run --name purplship --link=db:db -p5002:5002 purplship/purplship-server:[version]
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
    image: purplship/purplship-server:[version]
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

Make sure to have a running postgres SQL database instance

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
purplship runserver 0.0.0.0:5002
```


## Official Purplship client libraries

- [Python](https://github.com/PurplShip/purplship-python-client)
- [PHP](https://github.com/PurplShip/purplship-php-client)
- [Typescript](https://github.com/PurplShip/purplship-typescript-client)

Use the [swagger editor](https://editor.swagger.io/) to generate any additional client with our [OpenAPI References](https://github.com/PurplShip/purplship-server/tree/main/openapi)

## Get the Latest News

- **Blog** - Get the latest updates from the [Puprlship blog](https://blog.purplship.com).
- **Twitter** - Follow [Purplship](https://twitter.com/purplship).

Any other questions, mail us at hello@purplship.com. We’d love to meet you!