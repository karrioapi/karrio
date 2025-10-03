# CarrierDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier_name** | **string** | Indicates a carrier (type) | [default to undefined]
**display_name** | **string** | The carrier verbose name. | [default to undefined]
**integration_status** | **string** | The carrier integration status. | [default to undefined]
**capabilities** | **Array&lt;string&gt;** | The carrier supported and enabled capabilities. | [optional] [default to undefined]
**connection_fields** | **{ [key: string]: any; }** | The carrier connection fields. | [optional] [default to undefined]
**config_fields** | **{ [key: string]: any; }** | The carrier connection config. | [optional] [default to undefined]
**shipping_services** | **{ [key: string]: any; }** | The carrier shipping services. | [optional] [default to undefined]
**shipping_options** | **{ [key: string]: any; }** | The carrier shipping options. | [optional] [default to undefined]

## Example

```typescript
import { CarrierDetails } from './api';

const instance: CarrierDetails = {
    carrier_name,
    display_name,
    integration_status,
    capabilities,
    connection_fields,
    config_fields,
    shipping_services,
    shipping_options,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
