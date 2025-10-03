# OrderUpdateData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**_options** | **{ [key: string]: any; }** | &lt;details&gt;         &lt;summary&gt;The options available for the order shipments.&lt;/summary&gt;          {             \&quot;currency\&quot;: \&quot;USD\&quot;,             \&quot;paid_by\&quot;: \&quot;third_party\&quot;,             \&quot;payment_account_number\&quot;: \&quot;123456789\&quot;,             \&quot;duty_paid_by\&quot;: \&quot;recipient\&quot;,             \&quot;duty_account_number\&quot;: \&quot;123456789\&quot;,             \&quot;invoice_number\&quot;: \&quot;123456789\&quot;,             \&quot;invoice_date\&quot;: \&quot;2020-01-01\&quot;,             \&quot;single_item_per_parcel\&quot;: true,             \&quot;carrier_ids\&quot;: [\&quot;canadapost-test\&quot;],         }         &lt;/details&gt;          | [optional] [default to undefined]
**metadata** | **{ [key: string]: any; }** | User metadata for the shipment | [optional] [default to undefined]

## Example

```typescript
import { OrderUpdateData } from './api';

const instance: OrderUpdateData = {
    _options,
    metadata,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
