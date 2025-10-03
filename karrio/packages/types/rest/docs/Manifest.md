# Manifest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** | A unique manifest identifier | [optional] [default to undefined]
**object_type** | **string** | Specifies the object type | [optional] [default to 'manifest']
**carrier_name** | **string** | The manifest carrier | [default to undefined]
**carrier_id** | **string** | The manifest carrier configured name | [default to undefined]
**meta** | **{ [key: string]: any; }** | provider specific metadata | [optional] [default to undefined]
**test_mode** | **boolean** | Specified whether it was created with a carrier in test mode | [default to undefined]
**address** | [**AddressData**](AddressData.md) | The address of the warehouse or location where the shipments originate. | [default to undefined]
**_options** | **{ [key: string]: any; }** | &lt;details&gt;         &lt;summary&gt;The options available for the manifest.&lt;/summary&gt;          {             \&quot;shipments\&quot;: [                 {                     \&quot;tracking_number\&quot;: \&quot;123456789\&quot;,                     ...                     \&quot;meta\&quot;: {...}                 }             ]         }         &lt;/details&gt;          | [optional] [default to undefined]
**reference** | **string** | The manifest reference | [optional] [default to undefined]
**shipment_identifiers** | **Array&lt;string&gt;** | The list of shipment identifiers you want to add to your manifest.&lt;br/&gt;         shipment_identifier is often a tracking_number or shipment_id returned when you purchase a label.          | [default to undefined]
**metadata** | **{ [key: string]: any; }** | User metadata for the pickup | [optional] [default to undefined]
**manifest_url** | **string** | The Manifest file URL | [optional] [default to undefined]
**messages** | [**Array&lt;Message&gt;**](Message.md) | The list of note or warning messages | [optional] [default to undefined]

## Example

```typescript
import { Manifest } from './api';

const instance: Manifest = {
    id,
    object_type,
    carrier_name,
    carrier_id,
    meta,
    test_mode,
    address,
    _options,
    reference,
    shipment_identifiers,
    metadata,
    manifest_url,
    messages,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
