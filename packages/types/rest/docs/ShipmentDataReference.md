# ShipmentDataReference


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**recipient** | [**AddressData**](AddressData.md) | The address of the party.&lt;br/&gt;         Origin address (ship from) for the **shipper**&lt;br/&gt;         Destination address (ship to) for the **recipient**          | [default to undefined]
**shipper** | [**AddressData**](AddressData.md) | The address of the party.&lt;br/&gt;         Origin address (ship from) for the **shipper**&lt;br/&gt;         Destination address (ship to) for the **recipient**          | [default to undefined]
**return_address** | [**AddressData**](AddressData.md) | The return address for this shipment. Defaults to the shipper address. | [optional] [default to undefined]
**billing_address** | [**AddressData**](AddressData.md) | The payor address. | [optional] [default to undefined]
**parcels** | [**Array&lt;ParcelData&gt;**](ParcelData.md) | The shipment\&#39;s parcels | [default to undefined]
**_options** | **{ [key: string]: any; }** | &lt;details&gt;         &lt;summary&gt;The options available for the shipment.&lt;/summary&gt;          {             \&quot;currency\&quot;: \&quot;USD\&quot;,             \&quot;insurance\&quot;: 100.00,             \&quot;cash_on_delivery\&quot;: 30.00,             \&quot;dangerous_good\&quot;: true,             \&quot;declared_value\&quot;: 150.00,             \&quot;sms_notification\&quot;: true,             \&quot;email_notification\&quot;: true,             \&quot;email_notification_to\&quot;: \&quot;shipper@mail.com\&quot;,             \&quot;hold_at_location\&quot;: true,             \&quot;paperless_trade\&quot;: true,             \&quot;preferred_service\&quot;: \&quot;fedex_express_saver\&quot;,             \&quot;shipment_date\&quot;: \&quot;2020-01-01\&quot;,  # TODO: deprecate             \&quot;shipping_date\&quot;: \&quot;2020-01-01T00:00\&quot;,             \&quot;shipment_note\&quot;: \&quot;This is a shipment note\&quot;,             \&quot;signature_confirmation\&quot;: true,             \&quot;saturday_delivery\&quot;: true,             \&quot;shipper_instructions\&quot;: \&quot;This is a shipper instruction\&quot;,             \&quot;recipient_instructions\&quot;: \&quot;This is a recipient instruction\&quot;,             \&quot;doc_files\&quot;: [                 {                     \&quot;doc_type\&quot;: \&quot;commercial_invoice\&quot;,                     \&quot;doc_file\&quot;: \&quot;base64 encoded file\&quot;,                     \&quot;doc_name\&quot;: \&quot;commercial_invoice.pdf\&quot;,                     \&quot;doc_format\&quot;: \&quot;pdf\&quot;,                 }             ],             \&quot;doc_references\&quot;: [                 {                     \&quot;doc_id\&quot;: \&quot;123456789\&quot;,                     \&quot;doc_type\&quot;: \&quot;commercial_invoice\&quot;,                 }             ],         }         &lt;/details&gt;          | [optional] [default to undefined]
**payment** | [**Payment**](Payment.md) | The payment details | [optional] [default to undefined]
**customs** | [**CustomsData**](CustomsData.md) | The customs details.&lt;br/&gt;         **Note that this is required for the shipment of an international Dutiable parcel.**          | [optional] [default to undefined]
**reference** | **string** | The shipment reference | [optional] [default to undefined]
**label_type** | **string** | The shipment label file type. | [optional] [default to LabelTypeEnum_Pdf]
**is_return** | **boolean** | Indicates whether this shipment is a return shipment. When true, addresses are auto-swapped and the request is routed to the carrier\&#39;s return shipment API. | [optional] [default to false]
**service** | **string** | **Specify a service to Buy a label in one call without rating.** | [optional] [default to undefined]
**services** | **Array&lt;string&gt;** | The requested carrier service for the shipment.&lt;br/&gt;         Please consult the reference for specific carriers services.&lt;br/&gt;         **Note that this is a list because on a Multi-carrier rate request         you could specify a service per carrier.**          | [optional] [default to undefined]
**carrier_ids** | **Array&lt;string&gt;** | The list of configured carriers you wish to get rates from.&lt;br/&gt;         **Note that the request will be sent to all carriers in nothing is specified**          | [optional] [default to undefined]
**metadata** | **{ [key: string]: any; }** | User metadata for the shipment | [optional] [default to undefined]
**id** | **string** | The shipment id. | [optional] [default to undefined]

## Example

```typescript
import { ShipmentDataReference } from './api';

const instance: ShipmentDataReference = {
    recipient,
    shipper,
    return_address,
    billing_address,
    parcels,
    _options,
    payment,
    customs,
    reference,
    label_type,
    is_return,
    service,
    services,
    carrier_ids,
    metadata,
    id,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
