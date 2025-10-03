# Order


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** | A unique identifier | [optional] [default to undefined]
**object_type** | **string** | Specifies the object type | [optional] [default to 'order']
**order_id** | **string** | The source\&#39; order id. | [default to undefined]
**order_date** | **string** | The order date. format: &#x60;YYYY-MM-DD&#x60; | [optional] [default to undefined]
**source** | **string** | The order\&#39;s source. | [optional] [default to undefined]
**status** | **string** | The order status. | [optional] [default to StatusEnum_Unfulfilled]
**shipping_to** | [**Address**](Address.md) | The customer address for the order. | [default to undefined]
**shipping_from** | [**Address**](Address.md) | The origin or warehouse address of the order items. | [optional] [default to undefined]
**billing_address** | [**AddressData**](AddressData.md) | The customer\&#39; or shipping billing address. | [optional] [default to undefined]
**line_items** | [**Array&lt;LineItem&gt;**](LineItem.md) | The order line items. | [default to undefined]
**_options** | **{ [key: string]: any; }** | &lt;details&gt;         &lt;summary&gt;The options available for the order shipments.&lt;/summary&gt;          {             \&quot;currency\&quot;: \&quot;USD\&quot;,             \&quot;paid_by\&quot;: \&quot;third_party\&quot;,             \&quot;payment_account_number\&quot;: \&quot;123456789\&quot;,             \&quot;duty_paid_by\&quot;: \&quot;third_party\&quot;,             \&quot;duty_account_number\&quot;: \&quot;123456789\&quot;,             \&quot;invoice_number\&quot;: \&quot;123456789\&quot;,             \&quot;invoice_date\&quot;: \&quot;2020-01-01\&quot;,             \&quot;single_item_per_parcel\&quot;: true,             \&quot;carrier_ids\&quot;: [\&quot;canadapost-test\&quot;],             \&quot;preferred_service\&quot;: \&quot;fedex_express_saver\&quot;,         }         &lt;/details&gt;          | [optional] [default to undefined]
**meta** | **{ [key: string]: any; }** | system related metadata. | [optional] [default to undefined]
**metadata** | **{ [key: string]: any; }** | User metadata for the order. | [optional] [default to undefined]
**shipments** | [**Array&lt;Shipment&gt;**](Shipment.md) | The shipments associated with the order. | [optional] [default to undefined]
**test_mode** | **boolean** | Specify whether the order is in test mode or not. | [default to undefined]
**created_at** | **string** | The shipment creation datetime.&lt;br/&gt;         Date Format: &#x60;YYYY-MM-DD HH:MM:SS.mmmmmmz&#x60;          | [default to undefined]

## Example

```typescript
import { Order } from './api';

const instance: Order = {
    id,
    object_type,
    order_id,
    order_date,
    source,
    status,
    shipping_to,
    shipping_from,
    billing_address,
    line_items,
    _options,
    meta,
    metadata,
    shipments,
    test_mode,
    created_at,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
