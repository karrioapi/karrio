# PickupRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pickup_date** | **string** | The expected pickup date.&lt;br/&gt;         Date Format: &#x60;YYYY-MM-DD&#x60;          | [default to undefined]
**address** | [**AddressData**](AddressData.md) | The pickup address | [optional] [default to undefined]
**parcels** | [**Array&lt;ParcelData&gt;**](ParcelData.md) | The shipment parcels to pickup. | [optional] [default to undefined]
**parcels_count** | **number** | The number of parcels to be picked up (alternative to providing parcels array) | [optional] [default to undefined]
**ready_time** | **string** | The ready time for pickup.&lt;br/&gt;         Time Format: &#x60;HH:MM&#x60;          | [default to undefined]
**closing_time** | **string** | The closing or late time of the pickup.&lt;br/&gt;         Time Format: &#x60;HH:MM&#x60;          | [default to undefined]
**instruction** | **string** | The pickup instruction.&lt;br/&gt;         eg: Handle with care.          | [optional] [default to undefined]
**package_location** | **string** | The package(s) location.&lt;br/&gt;         eg: Behind the entrance door.          | [optional] [default to undefined]
**pickup_type** | **string** | The pickup scheduling type.&lt;br/&gt;         - one_time: Single pickup on a specific date&lt;br/&gt;         - daily: Recurring pickup every business day&lt;br/&gt;         - recurring: Custom recurring schedule          | [optional] [default to PickupTypeEnum_OneTime]
**recurrence** | **{ [key: string]: any; }** | Recurrence configuration for recurring pickups.&lt;br/&gt;         Example: {\&quot;frequency\&quot;: \&quot;weekly\&quot;, \&quot;days_of_week\&quot;: [\&quot;monday\&quot;, \&quot;wednesday\&quot;, \&quot;friday\&quot;], \&quot;end_date\&quot;: \&quot;2024-12-31\&quot;}          | [optional] [default to undefined]
**_options** | **{ [key: string]: any; }** | Advanced carrier specific pickup options | [optional] [default to undefined]

## Example

```typescript
import { PickupRequest } from './api';

const instance: PickupRequest = {
    pickup_date,
    address,
    parcels,
    parcels_count,
    ready_time,
    closing_time,
    instruction,
    package_location,
    pickup_type,
    recurrence,
    _options,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
