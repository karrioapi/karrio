# <a href="https://purplship.com"><picture><source srcset="./server/main/purplship/server/static/extra/branding/logo-inverted.svg" media="(prefers-color-scheme: dark)"/><img alt="Sourcegraph" src="./server/main/purplship/server/static/extra/branding/logo.svg" height="48px" /></picture></a>

[![puprlship-tests](https://github.com/purplship/purplship/actions/workflows/tests.yml/badge.svg)](https://github.com/purplship/purplship/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![codecov](https://codecov.io/gh/purplship/purplship/branch/main/graph/badge.svg?token=D07fio4Dn6)](https://codecov.io/gh/purplship/purplship)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/cc2ac4fcb6004bca84e42a90d8acfe41)](https://www.codacy.com/gh/purplship/purplship/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=purplship/purplship&amp;utm_campaign=Badge_Grade)

purplship is a multi-carrier shipping integartion platform.

purplship makes shipping services simple and accessible.
Help us out… If you love open source and great software, give us a star! 🌟

**Features**

- **Multi-carrier SDK**: Integrate purplship once and connect to multiple shipping carrier APIs
- **Extendable**: Use the purplship SDK Framework to integrate with custom carrier APIs.
- **Headless shipping API**: Power up your application with access to a network of carrier services.
- **Shipping**: Connect carrier accounts, get live rates and purchase shipping labels.
- **Tracking**: Create package tracker, get real time tracking status and provide a branded tracking page.
- **Address Validation**: Validate shipping addresses using integrated 3rd party APIs.
- **Cloud**: Optimized for deployments using Docker.

## Try it now

There are several ways to use Purplship:

- [Purplship Cloud](https://cloud.purplship.com) let's you use the fullset of shipping features. you don't need to deploy anything. We will manage and scale your infrastructure.
- [Purplship OSS](#purplship-oss) is an open-source version of purplship that provides the core functionality of purplship (rating API, tracking API, shipping API), but lacks more advanced features (multi-tenant/orgs, shipping billing data, built-in address validation, etc.)
- [Purplship SDK](#purplship-sdk) is the core of the purplship abstraction layer. It can be installed as a simple set of python libraries to do the low level carrier integration yourself.

> Source code for all editions is contained in this repository. See the [License section](#license) for more details.

## Status

- [x] Alpha: We are testing purplship with a closed set of customers
- [x] Public Alpha: Anyone can sign up over at [cloud.purplship.com](cloud.purplship.com). But go easy on us, there are a few kinks
- [ ] Public Beta: Stable enough for most non-enterprise use-cases
- [ ] Public: Production-ready

We are currently in Public Alpha. Watch "releases" of this repo to get notified of major updates.

## Self-hosted installation

### Purplship OSS

> check the latest version tags of the purplship/server image on [Docker Hub](https://hub.docker.com/r/purplship/purplship-server/tags)

<details>
<summary>Using our Docker image</summary>

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
  danh91.docker.scarf.sh/purplship/server:2021.7
```

</details>

<details>
<summary>Or using docker-compose</summary>

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
    networks:
      - db_network

  pship:
    image: danh91.docker.scarf.sh/purplship/purplship-server:2021.7
    restart: unless-stopped
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
    networks:
      - db_network

volumes:
  pshipdb:
    driver: local

networks:
  db_network:
    driver: bridge
```

- Run the application

```terminal
docker-compose up
```

</details>

Purplship should now be running at http://0.0.0.0:5002

**Default Login**

| email             | Password |
| ----------------- | -------- |
| admin@example.com | demo     |

### Official Purplship Server Client Libraries

- [Node](https://github.com/purplship/purplship-node)
- [PHP](https://github.com/purplship/purplship-php-client)
- [Python](https://github.com/purplship/purplship-python-client)

Use the [swagger editor](https://editor.swagger.io/) to generate any additional client with
our [OpenAPI References](./server/schemas)

## Purplship SDK

### Installation

```bash
# install purplship core
pip install purplship

# eg: install the purplship canadapost extention
pip install purplship.canadapost
```

<details>
<summary>Additional carrier extensions</summary>

- `purplship.aramex`
- `purplship.australiapost`
- `purplship.canadapost`
- `purplship.canpar`
- `purplship.dhl-express`
- `purplship.dhl-universal`
- `purplship.dicom`
- `purplship.fedex`
- `purplship.purolator`
- `purplship.royalmail`
- `purplship.sendle`
- `purplship.sf-express`
- `purplship.tnt`
- `purplship.ups`
- `purplship.usps`
- `purplship.usps-international`
- `purplship.yanwen`
- `purplship.yunexpress`

</details>

### Usage

<details>
<summary>Rates Fetching</summary>

- Fetch shipping rates

```python
import purplship
from purplship.core.models import Address, Parcel, RateRequest
from purplship.mappers.canadapost.settings import Settings


# Initialize a carrier gateway
canadapost = purplship.gateway["canadapost"].create(
    Settings(
        username="6e93d53968881714",
        password="0bfa9fcb9853d1f51ee57a",
        customer_number="2004381",
        contract_id="42708517",
        test=True
    )
)

# Fetching shipment rates

# Provide the shipper's address
shipper = Address(
    postal_code="V6M2V9",
    city="Vancouver",
    country_code="CA",
    state_code="BC",
    address_line1="5840 Oak St"
)

# Provide the recipient's address
recipient = Address(
    postal_code="E1C4Z8",
    city="Moncton",
    country_code="CA",
    state_code="NB",
    residential=False,
    address_line1="125 Church St"
)

# Specify your package dimensions and weight
parcel = Parcel(
    height=3.0,
    length=6.0,
    width=3.0,
    weight=0.5,
    weight_unit='KG',
    dimension_unit='CM'
)

# Prepare a rate request
rate_request = RateRequest(
    shipper=shipper,
    recipient=recipient,
    parcels=[parcel],
    services=["canadapost_xpresspost"],
)

# Send a rate request using a carrier gateway
response = purplship.Rating.fetch(rate_request).from_(canadapost)

# Parse the returned response
rates, messages = response.parse()

print(rates)
# [
#     RateDetails(
#         carrier_name="canadapost",
#         carrier_id="canadapost",
#         currency="CAD",
#         transit_days=2,
#         service="canadapost_xpresspost",
#         discount=1.38,
#         base_charge=12.26,
#         total_charge=13.64,
#         duties_and_taxes=0.0,
#         extra_charges=[
#             ChargeDetails(name="Automation discount", amount=-0.37, currency="CAD"),
#             ChargeDetails(name="Fuel surcharge", amount=1.75, currency="CAD"),
#         ],
#         meta=None,
#         id=None,
#     )
# ]
```

</details>

## Resources

- [**Documentation**](https://docs.purplship.com)
- [**Community Discussions**](https://github.com/purplship/purplship/discussions)
- [**Issue Tracker**](https://github.com/purplship/purplship/issues)
- [**Blog**](https://blog.purplship.com)

> [Join us on Discord](https://discord.gg/gS88uE7sEx)

## License

This repository contains both OSS-licensed and non-OSS-licensed files. We maintain one repository rather than two separate repositories mainly for development convenience.

All files in the `/ee` fall under [Enterprise LICENSE](/ee/LICENSE).

The remaining files fall under the [Apache 2 license](LICENSE). Purplship OSS is built only from the Apache-licensed files in this repository.
