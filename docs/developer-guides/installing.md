# Installing

- Start a Postgres database

```bash
docker run -d \
  --name db --rm \
  -e POSTGRES_DB=db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  postgres
```

- Run your shipping API

```bash
docker run -d \
  --name pship --rm \
  -e DEBUG_MODE=True \
  --link=db:db -p 5002:5002 \
  purplship/purplship-server:[version]
```

- Create an admin user

```terminal
docker exec -it purplship bash -c "purplship createsuperuser"
```

Access the application at [http://0.0.0.0:5002](http://0.0.0.0:5002)

## Updating Purplship

All you need to do to upgrade Purplship is to restart your Docker server with a new image tag.

We actively maintain the two most recent monthly releases of Purplship.

> The Docker server image tags follow CalVer semantics, so version 2021.4.2 can be found at purplship/purplship-server:2021.4.2.
> You can see the full list of tags on our [Docker Hub page](https://hub.docker.com/r/purplship/purplship-server/tags).