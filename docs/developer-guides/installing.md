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
    volumes:
      - pshipdb:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: "db"
      POSTGRES_USER: "postgres"
      POSTGRES_PASSWORD: "postgres"

  pship:
    image: danh91.docker.scarf.sh/purplship/purplship-server:[version]
    restart: unless-stopped
    volumes:
      - pshipstatics:/pship/statics
    environment:
      - DEBUG_MODE=True
      - ALLOWED_HOSTS=*
      - ADMIN_EMAIL=admin@domain.com
      - ADMIN_PASSWORD=demo
      - DATABASE_NAME=db
      - DATABASE_HOST=db
      - DATABASE_PORT=5432
      - DATABASE_USERNAME=postgres
      - DATABASE_PASSWORD=postgres
    depends_on:
      - db
  
  worker:
    image: danh91.docker.scarf.sh/purplship/purplship-server:[version]
    restart: unless-stopped
    env_file: .env
    volumes:
      - pshipdata:/pship/data
    depends_on:
      - db
    networks:
      - db_network
    entrypoint: bash ./worker.sh

  nginx:
    container_name: nginx
    image: "nginx:latest"
    ports:
      - "80:80"
    volumes:
      - ./nginx:/etc/nginx/conf.d
      - pshipstatics:/static
    networks:
      - web_network
    depends_on:
      - pship


volumes:
  pshipdb:
  pshipdata:
  pshipstatics:

networks:
  db_network:
    driver: bridge
  web_network:
    driver: bridge
```

- Run the application

```terminal
docker-compose up
```

Access the application at http://0.0.0.0:80
