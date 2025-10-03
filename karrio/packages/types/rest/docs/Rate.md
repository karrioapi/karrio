# Rate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** | A unique identifier | [optional] [default to undefined]
**object_type** | **string** | Specifies the object type | [optional] [default to 'rate']
**carrier_name** | **string** | The rate\&#39;s carrier | [default to undefined]
**carrier_id** | **string** | The targeted carrier\&#39;s name (unique identifier) | [default to undefined]
**currency** | **string** | The rate monetary values currency code | [optional] [default to undefined]
**service** | **string** | The carrier\&#39;s rate (quote) service | [optional] [default to undefined]
**total_charge** | **number** | The rate\&#39;s monetary amount of the total charge.&lt;br/&gt;         This is the gross amount of the rate after adding the additional charges          | [optional] [default to 0.0]
**transit_days** | **number** | The estimated delivery transit days | [optional] [default to undefined]
**extra_charges** | [**Array&lt;Charge&gt;**](Charge.md) | list of the rate\&#39;s additional charges | [optional] [default to undefined]
**estimated_delivery** | **string** | The delivery estimated date | [optional] [default to undefined]
**meta** | **{ [key: string]: any; }** | provider specific metadata | [optional] [default to undefined]
**test_mode** | **boolean** | Specified whether it was created with a carrier in test mode | [default to undefined]

## Example

```typescript
import { Rate } from './api';

const instance: Rate = {
    id,
    object_type,
    carrier_name,
    carrier_id,
    currency,
    service,
    total_charge,
    transit_days,
    extra_charges,
    estimated_delivery,
    meta,
    test_mode,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
