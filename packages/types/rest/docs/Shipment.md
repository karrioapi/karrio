# Shipment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** | A unique identifier | [optional] [default to undefined]
**object_type** | **string** | Specifies the object type | [optional] [default to 'shipment']
**tracking_url** | **string** | The shipment tracking url | [optional] [default to undefined]
**shipper** | [**Address**](Address.md) | The address of the party.&lt;br/&gt;         Origin address (ship from) for the **shipper**&lt;br/&gt;         Destination address (ship to) for the **recipient**          | [default to undefined]
**recipient** | [**Address**](Address.md) | The address of the party.&lt;br/&gt;         Origin address (ship from) for the **shipper**&lt;br/&gt;         Destination address (ship to) for the **recipient**          | [default to undefined]
**return_address** | [**Address**](Address.md) | The return address for this shipment. Defaults to the shipper address. | [optional] [default to undefined]
**billing_address** | [**Address**](Address.md) | The payor address. | [optional] [default to undefined]
**parcels** | [**Array&lt;Parcel&gt;**](Parcel.md) | The shipment\&#39;s parcels | [default to undefined]
**services** | **Array&lt;string&gt;** | The carriers services requested for the shipment.&lt;br/&gt;         Please consult the reference for specific carriers services.&lt;br/&gt;         **Note that this is a list because on a Multi-carrier rate request you could specify a service per carrier.**          | [optional] [default to undefined]
**_options** | **{ [key: string]: any; }** | &lt;details&gt;         &lt;summary&gt;The options available for the shipment.&lt;/summary&gt;          {             \&quot;currency\&quot;: \&quot;USD\&quot;,             \&quot;insurance\&quot;: 100.00,             \&quot;cash_on_delivery\&quot;: 30.00,             \&quot;dangerous_good\&quot;: true,             \&quot;declared_value\&quot;: 150.00,             \&quot;sms_notification\&quot;: true,             \&quot;email_notification\&quot;: true,             \&quot;email_notification_to\&quot;: \&quot;shipper@mail.com\&quot;,             \&quot;hold_at_location\&quot;: true,             \&quot;paperless_trade\&quot;: true,             \&quot;preferred_service\&quot;: \&quot;fedex_express_saver\&quot;,             \&quot;shipment_date\&quot;: \&quot;2020-01-01\&quot;,  # TODO: deprecate             \&quot;shipping_date\&quot;: \&quot;2020-01-01T00:00\&quot;,             \&quot;shipment_note\&quot;: \&quot;This is a shipment note\&quot;,             \&quot;signature_confirmation\&quot;: true,             \&quot;saturday_delivery\&quot;: true,             \&quot;shipper_instructions\&quot;: \&quot;This is a shipper instruction\&quot;,             \&quot;recipient_instructions\&quot;: \&quot;This is a recipient instruction\&quot;,             \&quot;doc_files\&quot;: [                 {                     \&quot;doc_type\&quot;: \&quot;commercial_invoice\&quot;,                     \&quot;doc_file\&quot;: \&quot;base64 encoded file\&quot;,                     \&quot;doc_name\&quot;: \&quot;commercial_invoice.pdf\&quot;,                     \&quot;doc_format\&quot;: \&quot;pdf\&quot;,                 }             ],             \&quot;doc_references\&quot;: [                 {                     \&quot;doc_id\&quot;: \&quot;123456789\&quot;,                     \&quot;doc_type\&quot;: \&quot;commercial_invoice\&quot;,                 }             ],         }         &lt;/details&gt;          | [optional] [default to undefined]
**payment** | [**Payment**](Payment.md) | The payment details | [optional] [default to undefined]
**customs** | [**CustomsData**](CustomsData.md) | The customs details.&lt;br/&gt;         **Note that this is required for the shipment of an international Dutiable parcel.**          | [optional] [default to undefined]
**rates** | [**Array&lt;Rate&gt;**](Rate.md) | The list for shipment rates fetched previously | [optional] [default to undefined]
**reference** | **string** | The shipment reference | [optional] [default to undefined]
**label_type** | **string** | The shipment label file type. | [optional] [default to undefined]
**carrier_ids** | **Array&lt;string&gt;** | The list of configured carriers you wish to get rates from.&lt;br/&gt;         **Note that the request will be sent to all carriers in nothing is specified**          | [optional] [default to undefined]
**tracker_id** | **string** | The attached tracker id | [optional] [default to undefined]
**created_at** | **string** | The shipment creation datetime.&lt;br/&gt;         Date Format: &#x60;YYYY-MM-DD HH:MM:SS.mmmmmmz&#x60;          | [default to undefined]
**metadata** | **{ [key: string]: any; }** | User metadata for the shipment | [optional] [default to undefined]
**messages** | [**Array&lt;Message&gt;**](Message.md) | The list of note or warning messages | [optional] [default to undefined]
**status** | **string** | The current Shipment status | [optional] [default to StatusEnum_Draft]
**carrier_name** | **string** | The shipment carrier | [optional] [default to undefined]
**carrier_id** | **string** | The shipment carrier configured identifier | [optional] [default to undefined]
**tracking_number** | **string** | The shipment tracking number | [optional] [default to undefined]
**shipment_identifier** | **string** | The shipment carrier system identifier | [optional] [default to undefined]
**selected_rate** | [**Rate**](Rate.md) | The shipment selected rate | [optional] [default to undefined]
**meta** | **{ [key: string]: any; }** | provider specific metadata | [optional] [default to undefined]
**return_shipment** | **{ [key: string]: any; }** | Return shipment details when a return label is provided with outbound shipment | [optional] [default to undefined]
**service** | **string** | The selected service | [optional] [default to undefined]
**selected_rate_id** | **string** | The shipment selected rate. | [optional] [default to undefined]
**test_mode** | **boolean** | Specified whether it was created with a carrier in test mode | [default to undefined]
**is_return** | **boolean** | Indicates whether this shipment is a return shipment. | [optional] [default to false]
**label_url** | **string** | The shipment label URL | [optional] [default to undefined]
**invoice_url** | **string** | The shipment invoice URL | [optional] [default to undefined]
**shipping_documents** | [**Array&lt;ShippingDocument&gt;**](ShippingDocument.md) | The list of shipping documents | [optional] [default to undefined]

## Example

```typescript
import { Shipment } from './api';

const instance: Shipment = {
    id,
    object_type,
    tracking_url,
    shipper,
    recipient,
    return_address,
    billing_address,
    parcels,
    services,
    _options,
    payment,
    customs,
    rates,
    reference,
    label_type,
    carrier_ids,
    tracker_id,
    created_at,
    metadata,
    messages,
    status,
    carrier_name,
    carrier_id,
    tracking_number,
    shipment_identifier,
    selected_rate,
    meta,
    return_shipment,
    service,
    selected_rate_id,
    test_mode,
    is_return,
    label_url,
    invoice_url,
    shipping_documents,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
