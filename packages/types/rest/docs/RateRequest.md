# RateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipper** | [**AddressData**](AddressData.md) | The address of the party&lt;br/&gt;         Origin address (ship from) for the **shipper**&lt;br/&gt;         Destination address (ship to) for the **recipient**          | [default to undefined]
**recipient** | [**AddressData**](AddressData.md) | The address of the party&lt;br/&gt;         Origin address (ship from) for the **shipper**&lt;br/&gt;         Destination address (ship to) for the **recipient**          | [default to undefined]
**parcels** | [**Array&lt;ParcelData&gt;**](ParcelData.md) | The shipment\&#39;s parcels | [default to undefined]
**services** | **Array&lt;string&gt;** | The requested carrier service for the shipment.&lt;br/&gt;         Please consult the reference for specific carriers services.&lt;br/&gt;         Note that this is a list because on a Multi-carrier rate request you could specify a service per carrier.          | [optional] [default to undefined]
**_options** | **{ [key: string]: any; }** | &lt;details&gt;         &lt;summary&gt;The options available for the shipment.&lt;/summary&gt;          {             \&quot;currency\&quot;: \&quot;USD\&quot;,             \&quot;insurance\&quot;: 100.00,             \&quot;insured_by\&quot;: \&quot;carrier\&quot;,             \&quot;cash_on_delivery\&quot;: 30.00,             \&quot;dangerous_good\&quot;: true,             \&quot;declared_value\&quot;: 150.00,             \&quot;sms_notification\&quot;: true,             \&quot;email_notification\&quot;: true,             \&quot;email_notification_to\&quot;: \&quot;shipper@mail.com\&quot;,             \&quot;hold_at_location\&quot;: true,             \&quot;paperless_trade\&quot;: true,             \&quot;preferred_service\&quot;: \&quot;fedex_express_saver\&quot;,             \&quot;shipment_date\&quot;: \&quot;2020-01-01\&quot;,  # TODO: deprecate             \&quot;shipping_date\&quot;: \&quot;2020-01-01T00:00\&quot;,             \&quot;shipment_note\&quot;: \&quot;This is a shipment note\&quot;,             \&quot;signature_confirmation\&quot;: true,             \&quot;saturday_delivery\&quot;: true,             \&quot;is_return\&quot;: true,             \&quot;shipper_instructions\&quot;: \&quot;This is a shipper instruction\&quot;,             \&quot;recipient_instructions\&quot;: \&quot;This is a recipient instruction\&quot;,             \&quot;doc_files\&quot;: [                 {                     \&quot;doc_type\&quot;: \&quot;commercial_invoice\&quot;,                     \&quot;doc_file\&quot;: \&quot;base64 encoded file\&quot;,                     \&quot;doc_name\&quot;: \&quot;commercial_invoice.pdf\&quot;,                     \&quot;doc_format\&quot;: \&quot;pdf\&quot;,                 }             ],             \&quot;doc_references\&quot;: [                 {                     \&quot;doc_id\&quot;: \&quot;123456789\&quot;,                     \&quot;doc_type\&quot;: \&quot;commercial_invoice\&quot;,                 }             ],         }         &lt;/details&gt;          | [optional] [default to undefined]
**reference** | **string** | The shipment reference | [optional] [default to undefined]
**payment** | [**Payment**](Payment.md) | The payment details | [optional] [default to undefined]
**customs** | [**CustomsData**](CustomsData.md) | The customs details.&lt;br/&gt;         **Note that this is required for international shipments.**          | [optional] [default to undefined]
**carrier_ids** | **Array&lt;string&gt;** | The list of configured carriers you wish to get rates from. | [optional] [default to undefined]

## Example

```typescript
import { RateRequest } from './api';

const instance: RateRequest = {
    shipper,
    recipient,
    parcels,
    services,
    _options,
    reference,
    payment,
    customs,
    carrier_ids,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
