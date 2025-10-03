# BatchObject


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** | A unique identifier | [optional] [default to undefined]
**status** | **string** | The batch operation resource status | [default to undefined]
**errors** | **{ [key: string]: any; }** | Resource processing errors | [optional] [default to undefined]

## Example

```typescript
import { BatchObject } from './api';

const instance: BatchObject = {
    id,
    status,
    errors,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
