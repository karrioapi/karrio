# CarrierConnection

Response serializer for carrier connections.  Note: Credentials are write-only and never returned in API responses. Use CarrierConnectionData for create and CarrierConnectionUpdateData for update.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** | A unique carrier connection identifier | [default to undefined]
**object_type** | **string** | Specifies the object type | [optional] [default to 'carrier-connection']
**carrier_name** | **string** | A carrier connection type. | [default to undefined]
**display_name** | **string** | The carrier connection type verbose name. | [optional] [default to undefined]
**carrier_id** | **string** | A carrier connection friendly name. | [readonly] [default to undefined]
**capabilities** | **Array&lt;string&gt;** | The carrier enabled capabilities. | [optional] [default to undefined]
**config** | **{ [key: string]: any; }** | Carrier connection custom config. | [optional] [default to undefined]
**metadata** | **{ [key: string]: any; }** | User metadata for the carrier. | [optional] [default to undefined]
**is_system** | **boolean** | The carrier connection is provided by the system admin. | [readonly] [default to undefined]
**active** | **boolean** | The active flag indicates whether the carrier account is active or not. | [default to undefined]
**test_mode** | **boolean** | The test flag indicates whether to use a carrier configured for test. | [default to undefined]

## Example

```typescript
import { CarrierConnection } from './api';

const instance: CarrierConnection = {
    id,
    object_type,
    carrier_name,
    display_name,
    carrier_id,
    capabilities,
    config,
    metadata,
    is_system,
    active,
    test_mode,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
