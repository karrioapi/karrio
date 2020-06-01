# PurplShip (Multi-carrier Shipping API SDK)

[![CI](https://github.com/PurplShip/purplship/workflows/PuprlShip/badge.svg)](https://github.com/PurplShip/purplship/actions)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![codecov](https://codecov.io/gh/PurplShip/purplship/branch/master/graph/badge.svg)](https://codecov.io/gh/PurplShip/purplship)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a57baa23a1ca4403a37a8b7134609709)](https://app.codacy.com/manual/DanH91/purplship?utm_source=github.com&utm_medium=referral&utm_content=PurplShip/purplship&utm_campaign=Badge_Grade_Dashboard)

## Introduction

PurplShip is a system for connecting multiple supply chain carriers API.

In addition to providing a unified and simplified interface across logistics carriers APIs, PurplShip offers a framework to facilitate the full access of advanced and specific carriers capabilities while simplifying the addition of new carrier APIs.

With PurplShip you can:

- Integrate multiple carriers web services: DHL, FedEx, UPS, USPS, Canada Post and more with ease
- Use a modern and intuitive, unified API across carriers


## License

Please see [LICENSE.md](https://github.com/PurplShip/purplship/blob/master/LICENSE) for licensing details.


## Authors

- **Daniel K.** - [@DanHK91](https://twitter.com/DanHK91) | [https://danielk.xyz](https://danielk.xyz/) | [PurplShip](https://purplship.com)


___


## Documentation


### Overview

This SDK is the foundation of a framework that intend to streamline the integration for any shipping carrier service.


| PurplShip packages | |
| --- | --- |
| `purplship.package` | Dedicated to carriers Courier and Package services integration. |
| `purplship.freight` *(in development)* | Dedicated to carriers Freight (LTL, FTL...) services integration. |
| `purplship.document` *(on roadmap)* | Dedicated to carriers document services (BOL, Procurements...) integration. |


Table of content

- [Installation](#Installation)
    - [Create a dependencies file requirements.txt with the content below](#create-a-dependencies-file-requirementstxt-with-the-content-below)
    - [Install PurplShip using pip](#install-purplship-using-pip)
- [PurplShip Package Usage](#purplship-package-usage)
    - [Initialize a carrier gateway]()
    - [Fetching a Shipment rates (or quotes)]()
- [API Reference](#api-reference)
    - [Fluent API]()
    - [Gateway](#Gateway)
    - [Models](#Models)
    - [Options](#Options)
    - [Packaging Types]()
    - [Package Presets]()
    - [Services]()
    - [Create a dependencies file requirements.txt with the content below](#Create a dependencies file requirements.txt with the content below)
- [PurplShip Package Usage](#purplship-package-usage)
- [API Reference](#API Reference)


### Installation

This instruction will get you started with `purplship.package` and the support for `canadapost` services extension.

#### Create a dependencies file `requirements.txt` with the content below

```text
# package repository index
-f https://git.io/purplship

# core packages
purplship==2020.5.1
purplship.package==2020.5.1

# carriers
purplship.canadapost==2020.5.1
```

<details>
<summary>Additional carriers</summary>

You can add additional carriers you desire to work with

```text
purplship.dhl==2020.5.1
purplship.fedex==2020.5.1
purplship.purolator==2020.5.1
purplship.ups==2020.5.1
```

</details>

#### Install PurplShip using `pip`

<details>
<summary>Create a Python virtual environment</summary>

```shell script
# create a clean evironment
python -m venv .venv

# activate it
. ./.venv/bin/activate
# on Windows .\.venv\Scripts\activate
```

</details>

```shell script
pip install -r requirements.txt
```

### PurplShip Package Usage

#### Initialize a carrier gateway

```python
import purplship.package as purplship
from purplship.package.mappers.canadapost import Settings

canadapost = purplship.gateway["canadapost"].create(
    Settings(
        username="username",
        password="password",
        customer_number="123456789",
        test=True
    )
)
```

*Check the [reference](#Gateway) of further details on the specific carrier gateways parameters*


#### Fetching a Shipment rates (or quotes)

Using the fluent API with the gateway previously initialized, you can fetch the price for a shipment.

```python
import purplship.package as purplship
from purplship.core.models import Address, Parcel, RateRequest

shipper = Address(
    postal_code="V6M2V9",
    city="Vancouver",
    country_code="CA",
    state_code="BC",
    address_line1="5840 Oak St"
)

recipient = Address(
    postal_code="E1C4Z8",
    city="Moncton",
    country_code="CA",
    state_code="NB",
    residential=False,
    address_line1="125 Church St"
)
parcel = Parcel(
    height=3.0,
    length=6.0,
    width=3.0,
    weight=0.5
)

request = purplship.Rating.fetch(
    RateRequest(
        shipper=shipper,
        recipient=recipient,
        parcel=parcel,
        services=["canadapost_priority"]
    )
)

rates = request.from_(canadapost).parse()
```

*Check the [reference](#Models) for further details on the model parameters*

<details>
<summary>Rating Response</summary>

```shell script
from purplship.core.utils import to_dict

print(to_dict(rates))
```

**output**

```json
[
  [],
  [
      {
        "base_charge": 101.83,
        "carrier": "canadapost",
        "carrier_name": "CanadaPost",
        "currency": "CAD",
        "discount": -3.63,
        "duties_and_taxes": 14.73,
        "estimated_delivery": "2020-05-06",
        "extra_charges": [
          {
            "amount": 8.11,
            "currency": "CAD",
            "name": "Fuel surcharge"
          },
          {
            "amount": -11.74,
            "currency": "CAD",
            "name": "SMB Savings"
          }
        ],
        "id": "da75bd1d-caf6-4e1a-8362-7e6e3e7e75d8",
        "service": "canadapost_priority",
        "total_charge": 112.93
      }
    ]
]
```

</details>


### API Reference


#### Fluent API

##### Pickup

- Booking

```python
import purplship.package as purplship
from purplship.core.models import PickupRequest

carrier = purplship.gateway['carrier'].create(...)

request = purplship.Pickup.book(
    PickupRequest(...)
)

rates = request.with_(carrier).parse()
```

- Update

```python
import purplship.package as purplship
from purplship.core.models import PickupUpdateRequest

carrier = purplship.gateway['carrier'].create(...)

request = purplship.Pickup.update(
    PickupUpdateRequest(...)
)

rates = request.from_(carrier).parse()
```

- Cancel

```python
import purplship.package as purplship
from purplship.core.models import PickupCancellationRequest

carrier = purplship.gateway['carrier'].create(...)

request = purplship.Pickup.cancel(
    PickupCancellationRequest(...)
)

rates = request.from_(carrier).parse()
```

##### Rating

- Fetch

```python
import purplship.package as purplship
from purplship.core.models import RateRequest

carrier = purplship.gateway['carrier'].create(...)

request = purplship.Rating.fetch(
    RateRequest(...)
)

rates = request.from_(carrier).parse()
```

##### Shipment

- Create

```python
import purplship.package as purplship
from purplship.core.models import ShipmentRequest

carrier = purplship.gateway['carrier'].create(...)

request = purplship.Shipment.create(
    ShipmentRequest(...)
)

rates = request.with_(carrier).parse()
```

##### Tracking

- Fetch

```python
import purplship.package as purplship
from purplship.core.models import TrackingRequest

carrier = purplship.gateway['carrier'].create(...)

request = purplship.Tracking.fetch(
    TrackingRequest(...)
)

rates = request.from_(carrier).parse()
```


#### Gateway

*Note that all carrier gateway defined bellow have these additional parameters*

    | Name | Type | Description
    | --- | --- | --- |
    | `carrier_name` | `str` | default: carrier name (eg: CanadaPost, Purolator...)
    | `id` | `str` | 
    | `test` | `boolean` |

- CanadaPost

    | Name | Type | Description 
    | --- | --- | --- | 
    | `username` | `str` | **required**
    | `password` | `str` | **required**
    | `custumer_number` | `str` |


- DHL

    | Name | Type | Description
    | --- | --- | --- |
    | `site_id` | `str` | **required**
    | `password` | `str` | **required**
    | `account_number` | `str` |

- FedEx

    | Name | Type | Description
    | --- | --- | --- |
    | `user_key` | `str` | **required**
    | `password` | `str` | **required**
    | `meter_number` | `str` | **required**
    | `account_number` | `str` | **required**

- Purolator

    | Name | Type | Description
    | --- | --- | --- |
    | `username` | `str` | **required**
    | `password` | `str` | **required**
    | `account_number` | `str` | **required**
    | `user_token` | `str` |
    | `language` | `str` | default: `en`

- UPS

    | Name | Type | Description
    | --- | --- | --- |
    | `username` | `str` | **required**
    | `password` | `str` | **required**
    | `access_license_number` | `str` | **required**
    | `account_number` | `str` |


#### Models

- <a name="Address"></a> Address

    | Name | Type | Description
    | --- | --- | --- |
    | `id` | `str` |
    | `postal_code` | `str` |
    | `city` | `str` |
    | `federal_tax_id` | `str` |
    | `state_tax_id` | `str` |
    | `person_name` | `str` |
    | `company_name` | `str` |
    | `country_code` | `str` |
    | `email` | `str` |
    | `phone_number` | `str` |
    | `state_code` | `str` |
    | `suburb` | `str` |
    | `residential` | `bool` |
    | `address_line1` | `str` |
    | `address_line2` | `str` |



- <a name="COD"></a> COD

    | Name | Type | Description
    | --- | --- | --- |
    | `amount` | `float` |



- <a name="Card"></a> Card

    | Name | Type | Description
    | --- | --- | --- |
    | `type` | `str` |
    | `number` | `str` |
    | `expiry_month` | `str` |
    | `expiry_year` | `str` |
    | `security_code` | `str` |
    | `name` | `str` |
    | `postal_code` | `str` |



- <a name="ChargeDetails"></a> ChargeDetails

    | Name | Type | Description
    | --- | --- | --- |
    | `name` | `str` |
    | `amount` | `float` |
    | `currency` | `str` |



- <a name="Commodity"></a> Commodity

    | Name | Type | Description
    | --- | --- | --- |
    | `id` | `str` |
    | `weight` | `float` |
    | `width` | `float` |
    | `height` | `float` |
    | `length` | `float` |
    | `description` | `str` |
    | `quantity` | `int` |
    | `sku` | `str` |
    | `value_amount` | `float` |
    | `value_currency` | `str` |
    | `origin_country` | `str` |



- <a name="Customs"></a> Customs

    | Name | Type | Description
    | --- | --- | --- |
    | `no_eei` | `str` |
    | `aes` | `str` |
    | `description` | `str` |
    | `terms_of_trade` | `str` |
    | `commodities` | List[[Commodity](#Commodity)] |
    | `duty` | [Payment](#Payment) |
    | `invoice` | [Invoice](#Invoice) |
    | `commercial_invoice` | `bool` |



- <a name="Doc"></a> Doc

    | Name | Type | Description
    | --- | --- | --- |
    | `type` | `str` |
    | `format` | `str` |
    | `image` | `str` |



- <a name="Insurance"></a> Insurance

    | Name | Type | Description
    | --- | --- | --- |
    | `amount` | `float` |



- <a name="Invoice"></a> Invoice

    | Name | Type | Description
    | --- | --- | --- |
    | `date` | `str` |
    | `identifier` | `str` |
    | `type` | `str` |
    | `copies` | `int` |



- <a name="Message"></a> Message

    | Name | Type | Description
    | --- | --- | --- |
    | `carrier` | `str` |
    | `carrier_name` | `str` |
    | `message` | `str` |
    | `code` | `str` |
    | `details` | `dict` |



- <a name="Notification"></a> Notification

    | Name | Type | Description
    | --- | --- | --- |
    | `email` | `str` |
    | `locale` | `str` |



- <a name="Parcel"></a> Parcel

    | Name | Type | Description
    | --- | --- | --- |
    | `id` | `str` |
    | `weight` | `float` |
    | `width` | `float` |
    | `height` | `float` |
    | `length` | `float` |
    | `packaging_type` | `str` |
    | `package_preset` | `str` |
    | `description` | `str` |
    | `content` | `str` |
    | `is_document` | `bool` |
    | `weight_unit` | `str` |
    | `dimension_unit` | `str` |



- <a name="Payment"></a> Payment

    | Name | Type | Description
    | --- | --- | --- |
    | `paid_by` | `str` |
    | `amount` | `float` |
    | `currency` | `str` |
    | `account_number` | `str` |
    | `credit_card` | [Card](#Card) |
    | `contact` | [Address](#Address) |



- <a name="PickupCancellationRequest"></a> PickupCancellationRequest

    | Name | Type | Description
    | --- | --- | --- |
    | `pickup_date` | `str` |
    | `confirmation_number` | `str` |
    | `person_name` | `str` |
    | `country_code` | `str` |



- <a name="PickupDetails"></a> PickupDetails

    | Name | Type | Description
    | --- | --- | --- |
    | `carrier` | `str` |
    | `carrier_name` | `str` |
    | `confirmation_number` | `str` |
    | `pickup_date` | `str` |
    | `pickup_charge` | [ChargeDetails](#ChargeDetails) |
    | `ready_time` | `str` |
    | `closing_time` | `str` |
    | `id` | `str` |



- <a name="PickupRequest"></a> PickupRequest

    | Name | Type | Description
    | --- | --- | --- |
    | `date` | `str` |
    | `address` | [Address](#Address) |
    | `parcels` | List[[Parcel](#Parcel)] |
    | `ready_time` | `str` |
    | `closing_time` | `str` |
    | `instruction` | `str` |
    | `package_location` | `str` |



- <a name="PickupUpdateRequest"></a> PickupUpdateRequest

    | Name | Type | Description
    | --- | --- | --- |
    | `date` | `str` |
    | `address` | [Address](#Address) |
    | `parcels` | List[[Parcel](#Parcel)] |
    | `confirmation_number` | `str` |
    | `ready_time` | `str` |
    | `closing_time` | `str` |
    | `instruction` | `str` |
    | `package_location` | `str` |



- <a name="RateDetails"></a> RateDetails

    | Name | Type | Description
    | --- | --- | --- |
    | `carrier` | `str` |
    | `carrier_name` | `str` |
    | `currency` | `str` |
    | `service` | `str` |
    | `discount` | `float` |
    | `base_charge` | `float` |
    | `total_charge` | `float` |
    | `duties_and_taxes` | `float` |
    | `estimated_delivery` | `str` |
    | `extra_charges` | List[[ChargeDetails](#ChargeDetails)] |
    | `id` | `str` |



- <a name="RateRequest"></a> RateRequest

    | Name | Type | Description
    | --- | --- | --- |
    | `shipper` | [Address](#Address) |
    | `recipient` | [Address](#Address) |
    | `parcel` | [Parcel](#Parcel) |
    | `services` | List[str] |
    | `options` | `dict` |
    | `reference` | `str` |



- <a name="ShipmentDetails"></a> ShipmentDetails

    | Name | Type | Description
    | --- | --- | --- |
    | `carrier` | `str` |
    | `carrier_name` | `str` |
    | `label` | `str` |
    | `tracking_number` | `str` |
    | `selected_rate` | [RateDetails](#RateDetails) |
    | `id` | `str` |



- <a name="ShipmentRequest"></a> ShipmentRequest

    | Name | Type | Description
    | --- | --- | --- |
    | `service` | `str` |
    | `shipper` | [Address](#Address) |
    | `recipient` | [Address](#Address) |
    | `parcel` | [Parcel](#Parcel) |
    | `payment` | [Payment](#Payment) |
    | `customs` | [Customs](#Customs) |
    | `doc_images` | List[[Doc](#Doc)] |
    | `options` | `dict` |
    | `reference` | `str` |



- <a name="TrackingDetails"></a> TrackingDetails

    | Name | Type | Description
    | --- | --- | --- |
    | `carrier` | `str` |
    | `carrier_name` | `str` |
    | `tracking_number` | `str` |
    | `events` | List[[TrackingEvent](#TrackingEvent)] |



- <a name="TrackingEvent"></a> TrackingEvent

    | Name | Type | Description
    | --- | --- | --- |
    | `date` | `str` |
    | `description` | `str` |
    | `location` | `str` |
    | `code` | `str` |
    | `time` | `str` |
    | `signatory` | `str` |



- <a name="TrackingRequest"></a> TrackingRequest

    | Name | Type | Description
    | --- | --- | --- |
    | `tracking_numbers` | List[str] |
    | `language_code` | `str` |
    | `level_of_details` | `str` |


#### Options


#### Packaging Types


#### Package Presets


#### Services
