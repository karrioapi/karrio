# OrderData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order_id** | **string** | The source\&#39; order id. | [default to undefined]
**order_date** | **string** | The order date. format: &#x60;YYYY-MM-DD&#x60; | [optional] [default to undefined]
**source** | **string** | The order\&#39;s source.&lt;br/&gt;         e.g. API, POS, ERP, Shopify, Woocommerce, etc.          | [optional] [default to 'API']
**shipping_to** | [**AddressData**](AddressData.md) | The customer or recipient address for the order. | [default to undefined]
**shipping_from** | [**AddressData**](AddressData.md) | The origin or warehouse address of the order items. | [optional] [default to undefined]
**billing_address** | [**AddressData**](AddressData.md) | The customer\&#39; or shipping billing address. | [optional] [default to undefined]
**line_items** | [**Array&lt;CommodityData&gt;**](CommodityData.md) | The order line items. | [default to undefined]
**_options** | **{ [key: string]: any; }** | &lt;details&gt;         &lt;summary&gt;The options available for the order shipments.&lt;/summary&gt;          {             \&quot;currency\&quot;: \&quot;USD\&quot;,             \&quot;paid_by\&quot;: \&quot;third_party\&quot;,             \&quot;payment_account_number\&quot;: \&quot;123456789\&quot;,             \&quot;duty_paid_by\&quot;: \&quot;third_party\&quot;,             \&quot;duty_account_number\&quot;: \&quot;123456789\&quot;,             \&quot;invoice_number\&quot;: \&quot;123456789\&quot;,             \&quot;invoice_date\&quot;: \&quot;2020-01-01\&quot;,             \&quot;single_item_per_parcel\&quot;: true,             \&quot;carrier_ids\&quot;: [\&quot;canadapost-test\&quot;],             \&quot;preferred_service\&quot;: \&quot;fedex_express_saver\&quot;,         }         &lt;/details&gt;          | [optional] [default to undefined]
**metadata** | **{ [key: string]: any; }** | User metadata for the order. | [optional] [default to undefined]

## Example

```typescript
import { OrderData } from './api';

const instance: OrderData = {
    order_id,
    order_date,
    source,
    shipping_to,
    shipping_from,
    billing_address,
    line_items,
    _options,
    metadata,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
