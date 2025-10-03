# Pickup


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** | A unique pickup identifier | [optional] [default to undefined]
**object_type** | **string** | Specifies the object type | [optional] [default to 'pickup']
**carrier_name** | **string** | The pickup carrier | [default to undefined]
**carrier_id** | **string** | The pickup carrier configured name | [default to undefined]
**confirmation_number** | **string** | The pickup confirmation identifier | [default to undefined]
**pickup_date** | **string** | The pickup date | [optional] [default to undefined]
**pickup_charge** | [**Charge**](Charge.md) | The pickup cost details | [optional] [default to undefined]
**ready_time** | **string** | The pickup expected ready time | [optional] [default to undefined]
**closing_time** | **string** | The pickup expected closing or late time | [optional] [default to undefined]
**metadata** | **{ [key: string]: any; }** | User metadata for the pickup | [optional] [default to undefined]
**meta** | **{ [key: string]: any; }** | provider specific metadata | [optional] [default to undefined]
**address** | [**Address**](Address.md) | The pickup address | [default to undefined]
**parcels** | [**Array&lt;Parcel&gt;**](Parcel.md) | The shipment parcels to pickup. | [default to undefined]
**instruction** | **string** | The pickup instruction.&lt;br/&gt;         eg: Handle with care.          | [optional] [default to undefined]
**package_location** | **string** | The package(s) location.&lt;br/&gt;         eg: Behind the entrance door.          | [optional] [default to undefined]
**_options** | **{ [key: string]: any; }** | Advanced carrier specific pickup options | [optional] [default to undefined]
**test_mode** | **boolean** | Specified whether it was created with a carrier in test mode | [default to undefined]

## Example

```typescript
import { Pickup } from './api';

const instance: Pickup = {
    id,
    object_type,
    carrier_name,
    carrier_id,
    confirmation_number,
    pickup_date,
    pickup_charge,
    ready_time,
    closing_time,
    metadata,
    meta,
    address,
    parcels,
    instruction,
    package_location,
    _options,
    test_mode,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
