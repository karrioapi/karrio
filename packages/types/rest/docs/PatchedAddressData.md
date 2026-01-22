# PatchedAddressData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** | A unique identifier for the address (used in JSON embedded data) | [optional] [default to undefined]
**postal_code** | **string** | The address postal code         **(required for shipment purchase)**          | [optional] [default to undefined]
**city** | **string** | The address city.         **(required for shipment purchase)**          | [optional] [default to undefined]
**federal_tax_id** | **string** | The party frederal tax id | [optional] [default to undefined]
**state_tax_id** | **string** | The party state id | [optional] [default to undefined]
**person_name** | **string** | Attention to         **(required for shipment purchase)**          | [optional] [default to undefined]
**company_name** | **string** | The company name if the party is a company | [optional] [default to undefined]
**country_code** | **string** | The address country code | [optional] [default to undefined]
**email** | **string** | The party email | [optional] [default to undefined]
**phone_number** | **string** | The party phone number. | [optional] [default to undefined]
**state_code** | **string** | The address state code | [optional] [default to undefined]
**residential** | **boolean** | Indicate if the address is residential or commercial (enterprise) | [optional] [default to false]
**street_number** | **string** | The address street number | [optional] [default to undefined]
**address_line1** | **string** | The address line with street number &lt;br/&gt;         **(required for shipment purchase)**          | [optional] [default to undefined]
**address_line2** | **string** | The address line with suite number | [optional] [default to undefined]
**validate_location** | **boolean** | Indicate if the address should be validated | [optional] [default to false]
**meta** | **{ [key: string]: any; }** | Template metadata for template identification.         Structure: {\&quot;label\&quot;: \&quot;Warehouse A\&quot;, \&quot;is_default\&quot;: true, \&quot;usage\&quot;: [\&quot;sender\&quot;, \&quot;return\&quot;]}          | [optional] [default to undefined]

## Example

```typescript
import { PatchedAddressData } from './api';

const instance: PatchedAddressData = {
    id,
    postal_code,
    city,
    federal_tax_id,
    state_tax_id,
    person_name,
    company_name,
    country_code,
    email,
    phone_number,
    state_code,
    residential,
    street_number,
    address_line1,
    address_line2,
    validate_location,
    meta,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
