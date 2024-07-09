# karrio.hay_post

This package is a HayPost extension of the [karrio](https://pypi.org/project/karrio) multi carrier shipping SDK.

## Requirements

`Python 3.7+`

## Installation

```bash
pip install karrio.hay_post
```

## Usage

```python
import karrio
from karrio.mappers.hay_post.settings import Settings

# Initialize a carrier gateway
hay_post = karrio.gateway["hay_post"].create(
    Settings(
        ...
    )
)
```

For test mode, you need to add your proxy or use a static IP address that HayPost has whitelisted.
Additionally, you need to connect with HayPost managers to obtain test and production
accounts. [Haypost ContactUs](https://www.haypost.am/en/contact-us)

Check the [Karrio Mutli-carrier SDK docs](https://docs.karrio.io) for Shipping API requests

## Additional information

### Services

   * letter_ordered
   * letter_simple
   * letter_valued
   * package_ordered
   * package_simple
   * package_valued
   * parcel_simple
   * parcel_valued
   * postcard_ordered
   * postcard_simple
   * sekogram_simple
   * sprint_simple
   * yes_ordered_value

### Currencies

   * RUB
   * USD
   * EUR
   * AMD

### Additional Services as Option

   * notification
   * ordered_packaging
   * pick_up
   * postmen_delivery_value
   * delivery
   * international_notification
   * domestic_sms
   * international_sms

### Note
* To obtain rates, you first need to configure them in the Carrier Configurations section (Services and Options).
