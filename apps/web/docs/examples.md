---
sidebar_position: 5
---

# Code Examples

This page provides code examples for common Karrio API operations in various programming languages.

## Creating a Shipment

### JavaScript/TypeScript

```javascript
import { Karrio } from '@karrio/sdk';

const karrio = new Karrio({
  apiKey: 'YOUR_API_KEY',
});

async function createShipment() {
  try {
    const shipment = await karrio.shipments.create({
      shipper: {
        company_name: 'ACME Inc.',
        name: 'John Doe',
        phone_number: '1-555-555-5555',
        email: 'john@example.com',
        address_line1: '123 Main St',
        city: 'San Francisco',
        state_code: 'CA',
        postal_code: '94105',
        country_code: 'US',
      },
      recipient: {
        name: 'Jane Smith',
        phone_number: '1-555-123-4567',
        email: 'jane@example.com',
        address_line1: '456 Market St',
        city: 'New York',
        state_code: 'NY',
        postal_code: '10001',
        country_code: 'US',
      },
      parcels: [
        {
          weight: 1.5,
          weight_unit: 'kg',
          length: 10,
          width: 15,
          height: 5,
          dimension_unit: 'cm',
        },
      ],
      service: 'ups_express',
      options: {
        signature_confirmation: true,
      },
    });

    console.log('Shipment created:', shipment);
    return shipment;
  } catch (error) {
    console.error('Error creating shipment:', error);
    throw error;
  }
}

createShipment();
```

### Python

```python
from karrio import Karrio

karrio = Karrio(api_key='YOUR_API_KEY')

def create_shipment():
    try:
        shipment = karrio.shipments.create(
            shipper={
                'company_name': 'ACME Inc.',
                'name': 'John Doe',
                'phone_number': '1-555-555-5555',
                'email': 'john@example.com',
                'address_line1': '123 Main St',
                'city': 'San Francisco',
                'state_code': 'CA',
                'postal_code': '94105',
                'country_code': 'US',
            },
            recipient={
                'name': 'Jane Smith',
                'phone_number': '1-555-123-4567',
                'email': 'jane@example.com',
                'address_line1': '456 Market St',
                'city': 'New York',
                'state_code': 'NY',
                'postal_code': '10001',
                'country_code': 'US',
            },
            parcels=[
                {
                    'weight': 1.5,
                    'weight_unit': 'kg',
                    'length': 10,
                    'width': 15,
                    'height': 5,
                    'dimension_unit': 'cm',
                },
            ],
            service='ups_express',
            options={
                'signature_confirmation': True,
            },
        )

        print(f"Shipment created: {shipment}")
        return shipment
    except Exception as e:
        print(f"Error creating shipment: {e}")
        raise

if __name__ == "__main__":
    create_shipment()
```

### Ruby

```ruby
require 'karrio'

karrio = Karrio::Client.new(api_key: 'YOUR_API_KEY')

def create_shipment
  begin
    shipment = karrio.shipments.create(
      shipper: {
        company_name: 'ACME Inc.',
        name: 'John Doe',
        phone_number: '1-555-555-5555',
        email: 'john@example.com',
        address_line1: '123 Main St',
        city: 'San Francisco',
        state_code: 'CA',
        postal_code: '94105',
        country_code: 'US',
      },
      recipient: {
        name: 'Jane Smith',
        phone_number: '1-555-123-4567',
        email: 'jane@example.com',
        address_line1: '456 Market St',
        city: 'New York',
        state_code: 'NY',
        postal_code: '10001',
        country_code: 'US',
      },
      parcels: [
        {
          weight: 1.5,
          weight_unit: 'kg',
          length: 10,
          width: 15,
          height: 5,
          dimension_unit: 'cm',
        },
      ],
      service: 'ups_express',
      options: {
        signature_confirmation: true,
      },
    )

    puts "Shipment created: #{shipment}"
    return shipment
  rescue => e
    puts "Error creating shipment: #{e}"
    raise
  end
end

create_shipment
```

## Getting Shipping Rates

### JavaScript/TypeScript

```javascript
import { Karrio } from '@karrio/sdk';

const karrio = new Karrio({
  apiKey: 'YOUR_API_KEY',
});

async function getRates() {
  try {
    const rates = await karrio.rates.fetch({
      shipper: {
        postal_code: '94105',
        country_code: 'US',
      },
      recipient: {
        postal_code: '10001',
        country_code: 'US',
      },
      parcels: [
        {
          weight: 1.5,
          weight_unit: 'kg',
        },
      ],
      carriers: ['ups', 'fedex', 'usps'],
    });

    console.log('Available rates:', rates);
    return rates;
  } catch (error) {
    console.error('Error fetching rates:', error);
    throw error;
  }
}

getRates();
```

### Python

```python
from karrio import Karrio

karrio = Karrio(api_key='YOUR_API_KEY')

def get_rates():
    try:
        rates = karrio.rates.fetch(
            shipper={
                'postal_code': '94105',
                'country_code': 'US',
            },
            recipient={
                'postal_code': '10001',
                'country_code': 'US',
            },
            parcels=[
                {
                    'weight': 1.5,
                    'weight_unit': 'kg',
                },
            ],
            carriers=['ups', 'fedex', 'usps'],
        )

        print(f"Available rates: {rates}")
        return rates
    except Exception as e:
        print(f"Error fetching rates: {e}")
        raise

if __name__ == "__main__":
    get_rates()
```

## Tracking a Package

### JavaScript/TypeScript

```javascript
import { Karrio } from '@karrio/sdk';

const karrio = new Karrio({
  apiKey: 'YOUR_API_KEY',
});

async function trackPackage(trackingNumber, carrier) {
  try {
    const tracker = await karrio.trackers.create({
      tracking_number: trackingNumber,
      carrier: carrier,
    });

    console.log('Tracker created:', tracker);
    return tracker;
  } catch (error) {
    console.error('Error tracking package:', error);
    throw error;
  }
}

trackPackage('1Z999AA10123456784', 'ups');
```

### Python

```python
from karrio import Karrio

karrio = Karrio(api_key='YOUR_API_KEY')

def track_package(tracking_number, carrier):
    try:
        tracker = karrio.trackers.create(
            tracking_number=tracking_number,
            carrier=carrier,
        )

        print(f"Tracker created: {tracker}")
        return tracker
    except Exception as e:
        print(f"Error tracking package: {e}")
        raise

if __name__ == "__main__":
    track_package('1Z999AA10123456784', 'ups')
```

## Validating an Address

### JavaScript/TypeScript

```javascript
import { Karrio } from '@karrio/sdk';

const karrio = new Karrio({
  apiKey: 'YOUR_API_KEY',
});

async function validateAddress() {
  try {
    const validation = await karrio.addresses.validate({
      address_line1: '123 Main St',
      city: 'San Francisco',
      state_code: 'CA',
      postal_code: '94105',
      country_code: 'US',
    });

    console.log('Address validation:', validation);
    return validation;
  } catch (error) {
    console.error('Error validating address:', error);
    throw error;
  }
}

validateAddress();
```

### Python

```python
from karrio import Karrio

karrio = Karrio(api_key='YOUR_API_KEY')

def validate_address():
    try:
        validation = karrio.addresses.validate(
            address_line1='123 Main St',
            city='San Francisco',
            state_code='CA',
            postal_code='94105',
            country_code='US',
        )

        print(f"Address validation: {validation}")
        return validation
    except Exception as e:
        print(f"Error validating address: {e}")
        raise

if __name__ == "__main__":
    validate_address()
```

## Creating a Return Label

### JavaScript/TypeScript

```javascript
import { Karrio } from '@karrio/sdk';

const karrio = new Karrio({
  apiKey: 'YOUR_API_KEY',
});

async function createReturnLabel() {
  try {
    const shipment = await karrio.shipments.create({
      shipper: {
        name: 'Jane Smith',
        phone_number: '1-555-123-4567',
        email: 'jane@example.com',
        address_line1: '456 Market St',
        city: 'New York',
        state_code: 'NY',
        postal_code: '10001',
        country_code: 'US',
      },
      recipient: {
        company_name: 'ACME Inc.',
        name: 'Returns Department',
        phone_number: '1-555-555-5555',
        email: 'returns@example.com',
        address_line1: '123 Main St',
        city: 'San Francisco',
        state_code: 'CA',
        postal_code: '94105',
        country_code: 'US',
      },
      parcels: [
        {
          weight: 1.5,
          weight_unit: 'kg',
          length: 10,
          width: 15,
          height: 5,
          dimension_unit: 'cm',
        },
      ],
      service: 'ups_ground',
      options: {
        is_return: true,
      },
    });

    console.log('Return label created:', shipment);
    return shipment;
  } catch (error) {
    console.error('Error creating return label:', error);
    throw error;
  }
}

createReturnLabel();
```

### Python

```python
from karrio import Karrio

karrio = Karrio(api_key='YOUR_API_KEY')

def create_return_label():
    try:
        shipment = karrio.shipments.create(
            shipper={
                'name': 'Jane Smith',
                'phone_number': '1-555-123-4567',
                'email': 'jane@example.com',
                'address_line1': '456 Market St',
                'city': 'New York',
                'state_code': 'NY',
                'postal_code': '10001',
                'country_code': 'US',
            },
            recipient={
                'company_name': 'ACME Inc.',
                'name': 'Returns Department',
                'phone_number': '1-555-555-5555',
                'email': 'returns@example.com',
                'address_line1': '123 Main St',
                'city': 'San Francisco',
                'state_code': 'CA',
                'postal_code': '94105',
                'country_code': 'US',
            },
            parcels=[
                {
                    'weight': 1.5,
                    'weight_unit': 'kg',
                    'length': 10,
                    'width': 15,
                    'height': 5,
                    'dimension_unit': 'cm',
                },
            ],
            service='ups_ground',
            options={
                'is_return': True,
            },
        )

        print(f"Return label created: {shipment}")
        return shipment
    except Exception as e:
        print(f"Error creating return label: {e}")
        raise

if __name__ == "__main__":
    create_return_label()
```

## Creating an International Shipment

### JavaScript/TypeScript

```javascript
import { Karrio } from '@karrio/sdk';

const karrio = new Karrio({
  apiKey: 'YOUR_API_KEY',
});

async function createInternationalShipment() {
  try {
    const shipment = await karrio.shipments.create({
      shipper: {
        company_name: 'ACME Inc.',
        name: 'John Doe',
        phone_number: '1-555-555-5555',
        email: 'john@example.com',
        address_line1: '123 Main St',
        city: 'San Francisco',
        state_code: 'CA',
        postal_code: '94105',
        country_code: 'US',
      },
      recipient: {
        name: 'Marie Dupont',
        phone_number: '33-1-23-45-67-89',
        email: 'marie@example.fr',
        address_line1: '1 Rue de Rivoli',
        city: 'Paris',
        postal_code: '75001',
        country_code: 'FR',
      },
      parcels: [
        {
          weight: 1.5,
          weight_unit: 'kg',
          length: 10,
          width: 15,
          height: 5,
          dimension_unit: 'cm',
        },
      ],
      service: 'fedex_international_priority',
      options: {
        signature_confirmation: true,
      },
      customs: {
        content_type: 'merchandise',
        invoice: '123456789',
        duty: {
          paid_by: 'sender',
        },
        commodities: [
          {
            description: 'T-shirt',
            quantity: 2,
            weight: 0.5,
            weight_unit: 'kg',
            value_amount: 20,
            value_currency: 'USD',
            origin_country: 'US',
            hs_code: '610910',
          },
          {
            description: 'Jeans',
            quantity: 1,
            weight: 1,
            weight_unit: 'kg',
            value_amount: 50,
            value_currency: 'USD',
            origin_country: 'US',
            hs_code: '620342',
          },
        ],
      },
    });

    console.log('International shipment created:', shipment);
    return shipment;
  } catch (error) {
    console.error('Error creating international shipment:', error);
    throw error;
  }
}

createInternationalShipment();
```

### Python

```python
from karrio import Karrio

karrio = Karrio(api_key='YOUR_API_KEY')

def create_international_shipment():
    try:
        shipment = karrio.shipments.create(
            shipper={
                'company_name': 'ACME Inc.',
                'name': 'John Doe',
                'phone_number': '1-555-555-5555',
                'email': 'john@example.com',
                'address_line1': '123 Main St',
                'city': 'San Francisco',
                'state_code': 'CA',
                'postal_code': '94105',
                'country_code': 'US',
            },
            recipient={
                'name': 'Marie Dupont',
                'phone_number': '33-1-23-45-67-89',
                'email': 'marie@example.fr',
                'address_line1': '1 Rue de Rivoli',
                'city': 'Paris',
                'postal_code': '75001',
                'country_code': 'FR',
            },
            parcels=[
                {
                    'weight': 1.5,
                    'weight_unit': 'kg',
                    'length': 10,
                    'width': 15,
                    'height': 5,
                    'dimension_unit': 'cm',
                },
            ],
            service='fedex_international_priority',
            options={
                'signature_confirmation': True,
            },
            customs={
                'content_type': 'merchandise',
                'invoice': '123456789',
                'duty': {
                    'paid_by': 'sender',
                },
                'commodities': [
                    {
                        'description': 'T-shirt',
                        'quantity': 2,
                        'weight': 0.5,
                        'weight_unit': 'kg',
                        'value_amount': 20,
                        'value_currency': 'USD',
                        'origin_country': 'US',
                        'hs_code': '610910',
                    },
                    {
                        'description': 'Jeans',
                        'quantity': 1,
                        'weight': 1,
                        'weight_unit': 'kg',
                        'value_amount': 50,
                        'value_currency': 'USD',
                        'origin_country': 'US',
                        'hs_code': '620342',
                    },
                ],
            },
        )

        print(f"International shipment created: {shipment}")
        return shipment
    except Exception as e:
        print(f"Error creating international shipment: {e}")
        raise

if __name__ == "__main__":
    create_international_shipment()
```
