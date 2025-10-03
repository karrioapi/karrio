# Customs


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** | A unique identifier | [optional] [default to undefined]
**commodities** | [**Array&lt;Commodity&gt;**](Commodity.md) | The parcel content items | [optional] [default to undefined]
**duty** | [**Duty**](Duty.md) | The payment details.&lt;br/&gt;         **Note that this is required for a Dutiable parcel shipped internationally.**          | [optional] [default to undefined]
**duty_billing_address** | [**Address**](Address.md) | The duty payor address. | [optional] [default to undefined]
**content_type** | **string** |  | [optional] [default to undefined]
**content_description** | **string** |  | [optional] [default to undefined]
**incoterm** | **string** | The customs \&#39;term of trade\&#39; also known as \&#39;incoterm\&#39; | [optional] [default to undefined]
**invoice** | **string** | The invoice reference number | [optional] [default to undefined]
**invoice_date** | **string** | The invoice date.&lt;br/&gt;         Date Format: &#x60;YYYY-MM-DD&#x60;          | [optional] [default to undefined]
**commercial_invoice** | **boolean** | Indicates if the shipment is commercial | [optional] [default to undefined]
**certify** | **boolean** | Indicate that signer certified confirmed all | [optional] [default to undefined]
**signer** | **string** |  | [optional] [default to undefined]
**_options** | **{ [key: string]: any; }** | &lt;details&gt;         &lt;summary&gt;Customs identification options.&lt;/summary&gt;          {             \&quot;aes\&quot;: \&quot;5218487281\&quot;,             \&quot;eel_pfc\&quot;: \&quot;5218487281\&quot;,             \&quot;license_number\&quot;: \&quot;5218487281\&quot;,             \&quot;certificate_number\&quot;: \&quot;5218487281\&quot;,             \&quot;nip_number\&quot;: \&quot;5218487281\&quot;,             \&quot;eori_number\&quot;: \&quot;5218487281\&quot;,             \&quot;vat_registration_number\&quot;: \&quot;5218487281\&quot;,         }         &lt;/details&gt;          | [optional] [default to undefined]
**object_type** | **string** | Specifies the object type | [optional] [default to 'customs_info']

## Example

```typescript
import { Customs } from './api';

const instance: Customs = {
    id,
    commodities,
    duty,
    duty_billing_address,
    content_type,
    content_description,
    incoterm,
    invoice,
    invoice_date,
    commercial_invoice,
    certify,
    signer,
    _options,
    object_type,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
