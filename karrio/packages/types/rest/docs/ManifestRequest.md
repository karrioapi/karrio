# ManifestRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier_name** | **string** | The manifest\&#39;s carrier | [default to undefined]
**address** | [**AddressData**](AddressData.md) | The address of the warehouse or location where the shipments originate. | [default to undefined]
**_options** | **{ [key: string]: any; }** | &lt;details&gt;         &lt;summary&gt;The options available for the manifest.&lt;/summary&gt;          {             \&quot;shipments\&quot;: [                 {                     \&quot;tracking_number\&quot;: \&quot;123456789\&quot;,                     ...                     \&quot;meta\&quot;: {...}                 }             ]         }         &lt;/details&gt;          | [optional] [default to undefined]
**reference** | **string** | The manifest reference | [optional] [default to undefined]
**shipment_identifiers** | **Array&lt;string&gt;** | The list of shipment identifiers you want to add to your manifest.&lt;br/&gt;         shipment_identifier is often a tracking_number or shipment_id returned when you purchase a label.          | [default to undefined]

## Example

```typescript
import { ManifestRequest } from './api';

const instance: ManifestRequest = {
    carrier_name,
    address,
    _options,
    reference,
    shipment_identifiers,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
