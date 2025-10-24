# CarrierConnectionData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier_name** | **string** | A carrier connection type. | [default to undefined]
**carrier_id** | **string** | A carrier connection friendly name. | [default to undefined]
**credentials** | [**ConnectionCredentialsField**](ConnectionCredentialsField.md) | Carrier connection credentials. | [default to undefined]
**capabilities** | **Array&lt;string&gt;** | The carrier enabled capabilities. | [optional] [default to undefined]
**config** | **{ [key: string]: any; }** | Carrier connection custom config. | [optional] [default to undefined]
**metadata** | **{ [key: string]: any; }** | User metadata for the carrier. | [optional] [default to undefined]
**active** | **boolean** | The active flag indicates whether the carrier account is active or not. | [optional] [default to true]

## Example

```typescript
import { CarrierConnectionData } from './api';

const instance: CarrierConnectionData = {
    carrier_name,
    carrier_id,
    credentials,
    capabilities,
    config,
    metadata,
    active,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
