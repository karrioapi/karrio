
# Overview

## What's purplship server?

purplship server is a headless **shipping platform** for innovators who want to regain control over their logistics
processes and fulfilment automation.
The server is a self-hosted Multi-carrier Shipping API based on [Django](https://www.djangoproject.com/)
and [purplship SDK](https://sdk.purplship.com).

You can use any programming language to send API requests to our growing network of
shipping carriers from your app.

## Features

- **Headless shipping API**: Power up your application with access to a network of carrier services
- **Multi-carrier**: Integrate purplship once and connect to multiple shipping carrier APIs
- **Shipping**: Connect carrier accounts, get live rates and purchase shipping labels
- **Tracking**: Create package tracker, get real time tracking status and provide a branded tracking page
- **Address Validation**: Validate shipping addresses using the Google Geocoding API
- **Shipping Web App**: Use a single dashboard to orchestrate your logistics operation.
- **Cloud**: Optimized for deployments using Docker

## Quick Start

It takes less than 5 minutes to run and install purplship using Docker:

- Start a Postgres database

```bash
docker run -d \
  --name db --rm \
  -e POSTGRES_DB=db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  postgres
```

- Run your shipping server

!!! hint ""
    **Find a specific version of [purplship/purplship-server](https://hub.docker.com/r/purplship/purplship-server/tags?page=1&ordering=last_updated)**

```bash
docker run \
  --name pship --rm \
  -e DEBUG_MODE=True \
  -e ADMIN_EMAIL=admin@example.com \
  -e ADMIN_PASSWORD=demo \
  --link=db:db -p 5002:5002 \
  danh91.docker.scarf.sh/purplship/purplship-server:2021.7
```

Once the server is ready access your shipping dashboard at [http://0.0.0.0:5002](http://0.0.0.0:5002),
log in with the default admin account `admin@example.com` | `demo`


!!! info
    If you get stuck or need help, [file an issue](https://github.com/purplship/purplship-server/issues/new/choose),
    [post on the community board](https://github.com/purplship/purplship-server/discussions) or
    [email](mailto:hello@purplship.com?subject=Purplship Quick Start).


!!! warning ""
    **Check [install](developer-guides/installing/) for more details**

## Guides

  - [User Guides](user-guides/index.md)
  - [API Guides](api-guides/index.md)
  - [Developer Guides](developer-guides/architecture.md)

## Resources

- [Github Community](https://github.com/purplship/purplship-server/discussions)
- [Discord Chat](https://discord.gg/kXEa3UMRHd)
- [Issue trackers](https://github.com/purplship/purplship-server/issues)
- [News & Blogs](https://blog.purplship.com)
