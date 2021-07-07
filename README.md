<p align="center">
  <p align="center">
    <a href="https://purplship.com" target="_blank">
      <img src="https://github.com/purplship/purplship-server/raw/main/purpleserver/purpleserver/static/extra/branding/icon.png" alt="purplship" height="100">
    </a>
  </p>
  <h2 align="center">
    The Open Source Multi-carrier Shipping API
  </h2>
  <p align="center">
    <a href="https://github.com/purplship/purplship-server/actions"><img src="https://github.com/purplship/purplship-server/workflows/puprlship-server/badge.svg" alt="CI" style="max-width:100%;"></a>
    <a href="https://www.gnu.org/licenses/agpl-3.0" rel="nofollow"><img src="https://camo.githubusercontent.com/cb1d26ec555a33e9f09fe279b5edc49996a3bb3b/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4147504c25323076332d626c75652e737667" alt="License: AGPL v3" data-canonical-src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg" style="max-width:100%;"></a>
  </p>
</p>


## What's purplship server?

purplship server is a headless **shipping platform** for innovators who want to regain control over their logistics
processes and fulfilment automation.
The server is in Python, but you can use any programming language to send API requests to our growing network of 
shipping carriers from your app.

- [Join us on Discord](https://discord.gg/gS88uE7sEx)
- [Want to partner up? Reach Out](https://purplship.com/#contact)

purplship makes shipping services simple and accessible.
Help us out… If you love Open standard and great software, give us a star! 🌟


## Features

- **Headless shipping API**: Power up your application with access to a network of carrier services
- **Multi-carrier**: Integrate purplship once and connect to multiple shipping carrier APIs
- **Shipping**: Connect carrier accounts, get live rates and purchase shipping labels
- **Tracking**: Create package tracker, get real time tracking status and provide a branded tracking page
- **Address Validation**: Validate shipping addresses using the Google Geocoding API
- **Shipping Web App**: Use a single dashboard to orchestrate your logistics operation.
- **Cloud**: Optimized for deployments using Docker


<img src="https://github.com/purplship/purplship-server/raw/main/artifacts/shipping-dashboard.jpeg">
<img src="https://github.com/purplship/purplship-server/raw/main/artifacts/tracking-dashboard.jpeg">


## Deployment

### `Docker`
  
> [check the latest version tags of the purplship/purplship-server](https://hub.docker.com/r/purplship/purplship-server/tags)

<details>
<summary>Use our image</summary>

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
  -e ADMIN_EMAIL=admin@example.com \
  -e ADMIN_PASSWORD=demo \
  --link=db:db -p 5002:5002 \
  danh91.docker.scarf.sh/purplship/purplship-server:2021.6.2
```

</details>

<details>
<summary>Or use docker-compose</summary>

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
    image: danh91.docker.scarf.sh/purplship/purplship-server:2021.6.2
    restart: unless-stopped
    ports:
      - "5002:5002"
    environment:
      - DEBUG_MODE=True
      - ALLOWED_HOSTS=*
      - ADMIN_EMAIL=admin@example.com
      - ADMIN_PASSWORD=demo
      - DATABASE_NAME=db
      - DATABASE_HOST=db
      - DATABASE_PORT=5432
      - DATABASE_USERNAME=postgres
      - DATABASE_PASSWORD=postgres
    depends_on:
      - db
```

- Run the application

```terminal
docker-compose up
```

</details>

Access the application at http://0.0.0.0:5002

**Default Login**

| email             | Password |
| ----------------- | -------- |
| admin@example.com | demo     |


### `Heroku`

Host your own purplship server for FREE with One-Click Deploy.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/purplship/purplship-heroku/tree/main/)


## Editions

purplship is available in two editions - **OSS** and **Enterprise**.
Here you can find the Open Source Edition released under the `Apache 2` License.

- [Become a backer or sponsor on Patreon](https://www.patreon.com/danh91)

To get the quotation of our Enterprise Edition, please visit [purplship.com](https://purplship.com) and contact us.

- [Book a Live Demo at purplship.com](https://purplship.com/schedule-demo/)


|                                          | OSS         | Bronze Sponsor | Enterprise   |
| ---------------------------------------- | ----------- | -------------- | ------------ |
| Multi-carrier shipping APIs              | Yes         | Yes            | Yes          |
| Carrier accounts                         | Unlimited   | Unlimited      | Unlimited    |
| Hosting                                  | Self-hosted | Self-hosted    | Self-hosted  |
| Maintenance & support                    | Community   | Priority Ticket| Dedicated    |
| Whitelabel                               | No          | Yes            | Yes          |
| Multi-tenant & Multi-org                 | No          | No             | Yes          |
| Reporting & Analytics (soon)             | No          | No             | Yes          |
| Shipping billing data (soon)             | No          | No             | Yes          |


## Official Client Libraries

- [Node](https://github.com/purplship/purplship-node)
- [PHP](https://github.com/purplship/purplship-php-client)
- [Python](https://github.com/purplship/purplship-python-client)

Use the [swagger editor](https://editor.swagger.io/) to generate any additional client with 
our [OpenAPI References](https://github.com/purplship/purplship-server/tree/main/shemas)


## Resources

- [**Documentation**](https://docs.purplship.com)
- [**Community**](https://github.com/purplship/purplship-server/discussions)
- [**Bug Tracker**](https://github.com/purplship/purplship/issues)
- [**Blog**](https://blog.purplship.com)
- [**@PurplShip on Twitter**](https://twitter.com/PurplShip)

## License

This project codebase is licensed under the terms of the `AGPL v3` license.

See the [LICENSE file](/LICENSE) for license rights and limitations.

Any other questions, mail us at hello@purplship.com. We’d love to meet you!
