# <a href="https://karrio.io" target="_blank"><img alt="Karrio" src="server/main/karrio/server/static/extra/branding/logo.svg" height="50px" /></a>

<img referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=86037d49-97aa-4091-ad2b-e9b221e64ed0" />

**The Universal Shipping API**

[![puprlship-tests](https://github.com/karrioapi/karrio/actions/workflows/tests.yml/badge.svg)](https://github.com/karrioapi/karrio/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/cc2ac4fcb6004bca84e42a90d8acfe41)](https://www.codacy.com/gh/karrioapi/karrio/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=karrioapi/karrio&amp;utm_campaign=Badge_Grade)

karrio makes shipping services simple and accessible.
Help us out… If you love open source and great software, give us a star! 🌟

**Features**

- **Headless Shipping**: Access a network of traditional and modern shipping carrier API-first
- **Multi-carrier SDK**: Integrate karrio once and connect to multiple shipping carrier APIs
- **Extensible**: Use the karrio SDK Framework to integrate with custom carrier APIs.
- **Shipping**: Connect carrier accounts, get live rates and purchase shipping labels.
- **Tracking**: Create package tracker, get real time tracking status and provide a branded tracking page.
- **Address Validation**: Validate shipping addresses using integrated 3rd party APIs.
- **Cloud**: Optimized for deployments using Docker.
- **Dashboard**: Use the [karrio dashboard](https://github.com/karrioapi/karrio-dashboard) to orchestrate your logistics operations.

<img alt="Karrio Dashboard" src="screenshots/dashboard.png" />

## Try it now

There are several ways to use Karrio:

- [Karrio Cloud](https://karrio.io) let's you use the fullset of shipping features.
you don't need to deploy anything. We will manage and scale your infrastructure.
- [Karrio OSS](#karrio-oss) is an open-source version of karrio that provides
the core functionality of karrio (rating API, tracking API, shipping API),
but lacks more advanced features (multi-tenant/orgs, shipping billing data, built-in address validation, etc.)
- [Karrio SDK](#karrio-sdk) is the core of the karrio abstraction layer.
It can be installed as a simple set of python libraries to do the low level carrier integration scripting yourself.

> Source code for all editions is contained in this repository.
See the [License section](#license) for more details.

## Status

- [x] Alpha: We are testing karrio with a closed set of customers
- [x] Private Beta: Stable enough for most non-enterprise use-cases
- [ ] Public: Production-ready

We are currently in Private Beta. Watch "releases" of this repo to get notified of major updates.

## Self-hosted installation

### Karrio OSS

> check the latest version tags of the karrio/server image on [Docker Hub](https://hub.docker.com/r/karrio/server/tags)

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
  --name karrio --rm \
  -e DEBUG_MODE=True \
  -e ADMIN_EMAIL=admin@example.com \
  -e ADMIN_PASSWORD=demo \
  --link=db:db -p 5002:5002 \
  danh91.docker.scarf.sh/karrio/server:2022.3.6
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
    environment:
      POSTGRES_DB: "db"
      POSTGRES_USER: "postgres"
      POSTGRES_PASSWORD: "postgres"
    networks:
      - db_network

  karrio:
    image: danh91.docker.scarf.sh/karrio/server:2022.3.6
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
  karriodb:
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

Karrio should now be running at <http://localhost:5002>

**Default Login**

| email             | Password |
| ----------------- | -------- |
| admin@example.com | demo     |

### Official Karrio Server Client Libraries

- [Node](https://github.com/karrioapi/karrio-node)
- [PHP](https://github.com/karrioapi/karrio-php)
- [Python](https://github.com/karrioapi/karrio-python)

## Karrio SDK

### Installation

```bash
# install karrio core
pip install karrio

# eg: install the karrio canadapost extention
pip install karrio.canadapost
```

<details>
<summary>Additional carrier extensions</summary>

- `karrio.aramex`
- `karrio.australiapost`
- `karrio.canadapost`
- `karrio.canpar`
- `karrio.dhl-express`
- `karrio.dhl-poland`
- `karrio.dhl-universal`
- `karrio.dicom`
- `karrio.fedex`
- `karrio.purolator`
- `karrio.royalmail`
- `karrio.sendle`
- `karrio.sf-express`
- `karrio.tnt`
- `karrio.ups`
- `karrio.usps`
- `karrio.usps-international`
- `karrio.yanwen`
- `karrio.yunexpress`

</details>

### Usage

<details>
<summary>Rates Fetching</summary>

- Fetch shipping rates

```python
import karrio
from karrio.core.models import Address, Parcel, RateRequest
from karrio.mappers.canadapost import Settings


# Initialize a carrier gateway
canadapost = karrio.gateway["canadapost"].create(
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
response = karrio.Rating.fetch(rate_request).from_(canadapost)

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
#     )
# ]
```

</details>

## Resources

- [**Documentation**](https://docs.karrio.io)
- [**Community Discussions**](https://github.com/karrioapi/karrio/discussions)
- [**Issue Tracker**](https://github.com/karrioapi/karrio/issues)
- [**Blog**](https://docs.karrio.io/blog)

> [Join us on Discord](https://discord.gg/gS88uE7sEx)

## License

This repository contains both OSS-licensed and non-OSS-licensed files.
We maintain one repository rather than two separate repositories mainly for development convenience.

All files in the `/insiders` fall under the [Karrio LICENSE](/insiders/LICENSE).

The remaining files fall under the [Apache 2 license](LICENSE).
Karrio OSS is built only from the Apache-licensed files in this repository.

Any other questions, mail us at hello@karrio.io We’d love to meet you!
