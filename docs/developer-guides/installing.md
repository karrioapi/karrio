# Installing

We recommend using Docker because it takes care of all of the necessary dependencies.


## Prerequisites 

You will need to install [Docker Desktop](https://www.docker.com/products/docker-desktop) and 
[Docker Compose](https://docs.docker.com/compose/install/) before following the instructions below.


## Installation using Docker Compose

- Create a `docker-compose.yml` file

```yaml
version: '3'

services:
  db:
    image: postgres
    restart: unless-stopped
    ports:
      - 5432:5432
    volumes:
      - purplship-db:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: "db"
      POSTGRES_USER: "postgres"
      POSTGRES_PASSWORD: "postgres"

  pship:
    image: danh91.docker.scarf.sh/purplship/purplship-server:[version]
    restart: unless-stopped
    ports:
      - "5002:5002"
    environment:
      - DEBUG_MODE=True
      - ALLOWED_HOSTS=*
      - DATABASE_NAME=db
      - DATABASE_HOST=db
      - DATABASE_PORT=5432
      - DATABASE_USERNAME=postgres
      - DATABASE_PASSWORD=postgres
    depends_on:
      - db
```

- Setup the database

```terminal
docker-compose run --rm --entrypoint="purplship migrate" pship
```

- Create an admin user

```terminal
docker-compose run --rm --entrypoint="purplship createsuperuser" pship
```

- Run the application

```terminal
docker-compose up
```

Access the application at http://0.0.0.0:5002
