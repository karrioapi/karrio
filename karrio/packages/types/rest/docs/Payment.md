# Payment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**paid_by** | **string** | The payor type | [optional] [default to PaidByEnum_Sender]
**currency** | **string** | The payment amount currency | [optional] [default to undefined]
**account_number** | **string** | The payor account number | [optional] [default to undefined]

## Example

```typescript
import { Payment } from './api';

const instance: Payment = {
    paid_by,
    currency,
    account_number,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
