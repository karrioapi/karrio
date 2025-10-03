# TrackingStatus


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** | A unique identifier | [optional] [default to undefined]
**carrier_name** | **string** | The tracking carrier | [default to undefined]
**carrier_id** | **string** | The tracking carrier configured identifier | [default to undefined]
**tracking_number** | **string** | The shipment tracking number | [default to undefined]
**info** | [**TrackingInfo**](TrackingInfo.md) | The package and shipment tracking details | [optional] [default to undefined]
**events** | [**Array&lt;TrackingEvent&gt;**](TrackingEvent.md) | The tracking details events | [optional] [default to undefined]
**delivered** | **boolean** | Specified whether the related shipment was delivered | [optional] [default to undefined]
**test_mode** | **boolean** | Specified whether the object was created with a carrier in test mode | [default to undefined]
**status** | **string** | The current tracking status | [optional] [default to StatusEnum_Pending]
**estimated_delivery** | **string** | The delivery estimated date | [optional] [default to undefined]
**meta** | **{ [key: string]: any; }** | provider specific metadata | [optional] [default to undefined]
**object_type** | **string** | Specifies the object type | [optional] [default to 'tracker']
**metadata** | **{ [key: string]: any; }** | User metadata for the tracker | [optional] [default to undefined]
**messages** | [**Array&lt;Message&gt;**](Message.md) | The list of note or warning messages | [optional] [default to undefined]
**delivery_image_url** | **string** | The shipment invoice URL | [optional] [default to undefined]
**signature_image_url** | **string** | The shipment invoice URL | [optional] [default to undefined]

## Example

```typescript
import { TrackingStatus } from './api';

const instance: TrackingStatus = {
    id,
    carrier_name,
    carrier_id,
    tracking_number,
    info,
    events,
    delivered,
    test_mode,
    status,
    estimated_delivery,
    meta,
    object_type,
    metadata,
    messages,
    delivery_image_url,
    signature_image_url,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
