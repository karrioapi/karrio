# ManifestData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier_name** | **string** | The manifest\&#39;s carrier | [default to undefined]
**address** | [**AddressData**](AddressData.md) | The address of the warehouse or location where the shipments originate. | [default to undefined]
**_options** | **{ [key: string]: any; }** | &lt;details&gt;         &lt;summary&gt;The options available for the manifest.&lt;/summary&gt;          {             \&quot;shipments\&quot;: [                 {                     \&quot;tracking_number\&quot;: \&quot;123456789\&quot;,                     ...                     \&quot;meta\&quot;: {...}                 }             ]         }         &lt;/details&gt;          | [optional] [default to undefined]
**reference** | **string** | The manifest reference | [optional] [default to undefined]
**shipment_ids** | **Array&lt;string&gt;** | The list of existing shipment object ids with label purchased. | [default to undefined]

## Example

```typescript
import { ManifestData } from './api';

const instance: ManifestData = {
    carrier_name,
    address,
    _options,
    reference,
    shipment_ids,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
