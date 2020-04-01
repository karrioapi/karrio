# py-caps

Canada Post Python Data Structure generated from .xsd files with [generateDS](http://www.davekuhlman.org/generateDS.html) library

## Installation

```bash
pip install -f https://git.io/purplship py-caps
```

## Usage

### Rating

- [Types Documentation](https://doc.purplship.com/api/pycaps.html)
- [Official API Documentation](https://www.canadapost.ca/cpo/mc/business/productsservices/developers/services/rating/getrates/default.jsf)

#### Create a rating request (mailing-scenario)

```python
from pycaps import rating as Rating

mailing = Rating.mailing_scenario(
  customer_number="1234567",
  contract_id="3409857495",
  expected_mailing_date="2025-10-03",
  parcel_characteristics=Rating.parcel_characteristicsType(
    weight=0.3,
    dimensions=Rating.dimensionsType(
      length=5.0,
      width=4.0,
      height=5.0
    )
  ),
  services=Rating.servicesType(
    service_code=["DOM.EP"]
  ),
  origin_postal_code="H8Z2Z3",
  destination=Rating.destinationType(
    domestic=Rating.domesticType(postal_code="H8Z2V4")
  )
)
```

#### Export the request as XML string

```python
# Install generateDs-helpers to benefit from utilities functions used below
# pip install -f https://git.io/purplship gds-helpers
from gds_helpers import export

requestXML = export(
  mailing,
  namespacedef_='xmlns="http://www.canadapost.ca/ws/ship/rate-v3"'
)

print(requestXML)
"""
<mailing-scenario xmlns="http://www.canadapost.ca/ws/ship/rate-v3">
    <customer-number>1234567</customer-number>
    <contract-id>3409857495</contract-id>
    <expected-mailing-date>2025-10-03</expected-mailing-date>
    <parcel-characteristics>
        <weight>0.3</weight>
        <dimensions>
            <length>5.</length>
            <width>4.</width>
            <height>5.</height>
        </dimensions>
    </parcel-characteristics>
    <services>
        <service-code>DOM.EP</service-code>
    </services>
    <origin-postal-code>H8Z2Z3</origin-postal-code>
    <destination>
        <domestic>
            <postal-code>H8Z2V4</postal-code>
        </domestic>
    </destination>
</mailing-scenario>
"""
```

#### Send a http request to get the rate pricing from Canada Post

```python
from gds_helpers import request
from base64 import b64encode
auth = b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")

response = request(
  url="https://soagw.canadapost.ca/rs/ship/price",
  data=bytearray(requestXML, "utf-8"),
  headers={
    "Content-Type": "application/vnd.cpc.ship.rate-v3+xml",
    "Accept": "application/vnd.cpc.ship.rate-v3+xml",
    "Authorization": f"Basic {auth}",
    "Accept-language": "en-CA",
  },
  method="POST",
)
```
