# ParcelData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**weight** | **number** | The parcel\&#39;s weight | [default to undefined]
**width** | **number** | The parcel\&#39;s width | [optional] [default to undefined]
**height** | **number** | The parcel\&#39;s height | [optional] [default to undefined]
**length** | **number** | The parcel\&#39;s length | [optional] [default to undefined]
**packaging_type** | **string** | The parcel\&#39;s packaging type.&lt;br/&gt;         **Note that the packaging is optional when using a package preset.**&lt;br/&gt;         values: &lt;br/&gt;         &#x60;envelope&#x60; &#x60;pak&#x60; &#x60;tube&#x60; &#x60;pallet&#x60; &#x60;small_box&#x60; &#x60;medium_box&#x60; &#x60;your_packaging&#x60;&lt;br/&gt;         For carrier specific packaging types, please consult the reference.          | [optional] [default to undefined]
**package_preset** | **string** | The parcel\&#39;s package preset.&lt;br/&gt;         For carrier specific package presets, please consult the reference.          | [optional] [default to undefined]
**description** | **string** | The parcel\&#39;s description | [optional] [default to undefined]
**content** | **string** | The parcel\&#39;s content description | [optional] [default to undefined]
**is_document** | **boolean** | Indicates if the parcel is composed of documents only | [optional] [default to false]
**weight_unit** | **string** | The parcel\&#39;s weight unit | [default to undefined]
**dimension_unit** | **string** | The parcel\&#39;s dimension unit | [optional] [default to undefined]
**items** | [**Array&lt;CommodityData&gt;**](CommodityData.md) | The parcel items. | [optional] [default to undefined]
**reference_number** | **string** | The parcel reference number.&lt;br/&gt;         (can be used as tracking number for custom carriers)          | [optional] [default to undefined]
**freight_class** | **string** | The parcel\&#39;s freight class for pallet and freight shipments. | [optional] [default to undefined]
**_options** | **{ [key: string]: any; }** | &lt;details&gt;         &lt;summary&gt;Parcel specific options.&lt;/summary&gt;          {             \&quot;insurance\&quot;: \&quot;100.00\&quot;,             \&quot;insured_by\&quot;: \&quot;carrier\&quot;,         }         &lt;/details&gt;          | [optional] [default to undefined]
**meta** | **{ [key: string]: any; }** | Template metadata for template identification.         Structure: {\&quot;label\&quot;: \&quot;Standard Box\&quot;, \&quot;is_default\&quot;: true}          | [optional] [default to undefined]

## Example

```typescript
import { ParcelData } from './api';

const instance: ParcelData = {
    weight,
    width,
    height,
    length,
    packaging_type,
    package_preset,
    description,
    content,
    is_document,
    weight_unit,
    dimension_unit,
    items,
    reference_number,
    freight_class,
    _options,
    meta,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
