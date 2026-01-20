# LineItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** | A unique identifier | [optional] [default to undefined]
**weight** | **number** | The commodity\&#39;s weight | [default to undefined]
**weight_unit** | **string** | The commodity\&#39;s weight unit | [default to undefined]
**title** | **string** | A description of the commodity | [optional] [default to undefined]
**description** | **string** | A description of the commodity | [optional] [default to undefined]
**quantity** | **number** | The commodity\&#39;s quantity (number or item) | [optional] [default to 1]
**sku** | **string** | The commodity\&#39;s sku number | [optional] [default to undefined]
**hs_code** | **string** | The commodity\&#39;s hs_code number | [optional] [default to undefined]
**value_amount** | **number** | The monetary value of the commodity | [optional] [default to undefined]
**value_currency** | **string** | The currency of the commodity value amount | [optional] [default to undefined]
**origin_country** | **string** | The origin or manufacture country | [optional] [default to undefined]
**product_url** | **string** | The product url | [optional] [default to undefined]
**image_url** | **string** | The image url | [optional] [default to undefined]
**product_id** | **string** | The product id | [optional] [default to undefined]
**variant_id** | **string** | The variant id | [optional] [default to undefined]
**parent_id** | **string** | The id of the related order line item. | [optional] [default to undefined]
**metadata** | **{ [key: string]: any; }** | &lt;details&gt;         &lt;summary&gt;Commodity user references metadata.&lt;/summary&gt;          {             \&quot;part_number\&quot;: \&quot;5218487281\&quot;,             \&quot;reference1\&quot;: \&quot;# ref 1\&quot;,             \&quot;reference2\&quot;: \&quot;# ref 2\&quot;,             \&quot;reference3\&quot;: \&quot;# ref 3\&quot;,             ...         }         &lt;/details&gt;          | [optional] [default to undefined]
**meta** | **{ [key: string]: any; }** | Template metadata for template identification.         Structure: {\&quot;label\&quot;: \&quot;Widget Pro\&quot;, \&quot;is_default\&quot;: false}          | [optional] [default to undefined]
**object_type** | **string** | Specifies the object type | [optional] [default to 'commodity']
**unfulfilled_quantity** | **number** |  | [optional] [default to 0]

## Example

```typescript
import { LineItem } from './api';

const instance: LineItem = {
    id,
    weight,
    weight_unit,
    title,
    description,
    quantity,
    sku,
    hs_code,
    value_amount,
    value_currency,
    origin_country,
    product_url,
    image_url,
    product_id,
    variant_id,
    parent_id,
    metadata,
    meta,
    object_type,
    unfulfilled_quantity,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
