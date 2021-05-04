## Overview

Purplship proposes a set of unified APIs accepting all required data to send requests to the supported carrier services.

The typical data flows for all requests processed by Purplship is illustrated bellow.

<figure>
  <img src="/images/purplship-sequence-diagram.svg" height="300" />
  <figcaption>Purplship - Sequence</figcaption>
</figure>

To accomplish this, the overall abstraction proposed by Purplship come down to the implementation these abstract classes.

<figure>
  <img src="/images/purplship-class-diagram.svg" height="300" />
  <figcaption>Purplship - Class Diagram</figcaption>
</figure>

### The `Settings`

!!! abstract ""
    The `Settings` class defines all the carrier specific credential required to authenticate connections
    and additionally
    
    - a unique `carrier_name` (a readonly name. e.g: canadapost)
    - a unique `carrier_id` (a nickname provided for each instance. e.g: canadapost_test_account)
    - optionally a unique `id` reference in your system or a database


### The `Mapper`

!!! abstract ""
    The `Mapper` class translates the unified Purplship API data into carrier specific data to send requests
    and also takes care or parsing the response returned back into a unified data model 
    
    Learn more about the Mapper pattern from [Martin Fowler Enterprise Pattern](https://martinfowler.com/eaaCatalog/dataMapper.html)


### The `Proxy`

!!! abstract ""
    The `Proxy` class defines one or many HTTP requests required to communicate with a carrier service
    
    [Learn more about the Proxy pattern](https://en.wikipedia.org/wiki/Proxy_pattern)
    

## In practice

This is how these classes come together to make a request to a carrier service

```python
from purplship.mappers.canadapost import Settings, Mapper, Proxy

# Instantiate a connection settings
canadapost_settings = Settings(
    username="username",
    password="password",
    customer_number="2004381",
    contract_id="42708517",
)

# Instantiate the carrier corresponding translator
canadapost_mapper = Mapper(canadapost_settings)

# And finally the carrier corresponding communication proxy
canadapost_proxy = Proxy(canadapost_settings)


# e.g: a Pickup scheduling request
from purplship.core.models import PickupRequest, Address


# A Purplship unified Pickup request type
pickup_request: PickupRequest = PickupRequest(
    pickup_date="2021-12-15",
    ready_time="10:00",
    closing_time="17:00",
    address=Address(
        postal_code="V6M2V9",
        city="Vancouver",
        country_code="CA",
        state_code="BC",
        address_line1="5840 Oak St"  
    )
)

# Convert into a carrier specific pickup request
canadapost_pickup_request = canadapost_mapper.create_pickup_request(pickup_request)

# Send the request the carrier
canadapost_pickup_response = canadapost_proxy.schedule_pickup(canadapost_pickup_request)

# Parse the response into a Purplship unified Pickup response type
pickup_response = canadapost_mapper.parse_pickup_response(canadapost_pickup_response)

print(pickup_response)
```
```shell
(
    PickupDetails(
        carrier_name='canadapost',
        carrier_id='canadapost',
        confirmation_number='0074698052',
        pickup_charge=ChargeDetails(
            name='Pickup fees',
            amount=4.42,
            currency='CAD'
        )
    ),
    [] # message and error list here 
)
```

!!! info
    The example above illustrates a Pickup scheduling but the idea is that all requests made by Purplship follow the same lifecycle:
    
    - convert unified Purplship API data into a carrier specific request using the `Mapper`
    - send the request to the carrier using the `Proxy`
    - and parse back the response into a unified Purplship data using the `Mapper`

!!! caution
    Note that Purplship does not raise exceptions when there is a failure during requests but rather always return 
    a tuple of a `response` if `successful` with a list of `messages` if any **notes**, **messages** or **errors** 
    in case of `failures` are returned.

## Fluent API

Once you understand the lifecycle above, you can send any requests supported by Purplship with the same mental model.
However, this looks a little verbose. That's why we introduced a Fluent interface to handle this process with fewer lines.

```python
import purplship

# Create a carrier connection gateway
# This will instantiate the corresponding Settings, Mapper and Proxy
canadapost_gateway = purplship.gateway['canadapost'].create({
    'contract_id': '42708517',
    'customer_number': '2004381',
    'password': 'password',
    'username': 'username'
})

pickup_request = purplship.Pickup.schedule({
    'pickup_date': '2021-12-15',
    'closing_time': '17:00',
    'ready_time': '10:00',
    'address': {
        'address_line1': '5840 Oak St',
        'city': 'Vancouver',
        'country_code': 'CA',
        'postal_code': 'V6M2V9',
        'residential': False,
        'state_code': 'BC'
    }
})

pickup_response = pickup_request.with_(canadapost_gateway).parse()
```

!!! info
    Note the concept of Gateway introduced here to encapsulate the access to the external system that are carrier servers
    in our case.
    
    Learn more about the Gateway pattern from [Martin Fowler Enterprise Pattern](https://martinfowler.com/eaaCatalog/gateway.html)