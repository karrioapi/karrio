# ShipmentsApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**cancel**](#cancel) | **POST** /v1/shipments/{id}/cancel | Cancel a shipment|
|[**create**](#create) | **POST** /v1/shipments | Create a shipment|
|[**document**](#document) | **POST** /v1/shipments/{id}/documents/{doc} | Retrieve a shipment document|
|[**list**](#list) | **GET** /v1/shipments | List all shipments|
|[**purchase**](#purchase) | **POST** /v1/shipments/{id}/purchase | Buy a shipment label|
|[**rates**](#rates) | **POST** /v1/shipments/{id}/rates | Fetch new shipment rates|
|[**retrieve**](#retrieve) | **GET** /v1/shipments/{id} | Retrieve a shipment|
|[**update**](#update) | **PUT** /v1/shipments/{id} | Update a shipment|

# **cancel**
> Shipment cancel()

Void a shipment with the associated label.

### Example

```typescript
import {
    ShipmentsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ShipmentsApi(configuration);

let id: string; // (default to undefined)

const { status, data } = await apiInstance.cancel(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**string**] |  | defaults to undefined|


### Return type

**Shipment**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**304** |  |  -  |
|**404** |  |  -  |
|**400** |  |  -  |
|**409** |  |  -  |
|**424** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create**
> Shipment create(shipmentData)

Create a new shipment instance.

### Example

```typescript
import {
    ShipmentsApi,
    Configuration,
    ShipmentData
} from './api';

const configuration = new Configuration();
const apiInstance = new ShipmentsApi(configuration);

let shipmentData: ShipmentData; //

const { status, data } = await apiInstance.create(
    shipmentData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **shipmentData** | **ShipmentData**|  | |


### Return type

**Shipment**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** |  |  -  |
|**400** |  |  -  |
|**424** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **document**
> ShippingDocument document()

Retrieve a shipment document (label or invoice) as base64 encoded content.

### Example

```typescript
import {
    ShipmentsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ShipmentsApi(configuration);

let doc: string; // (default to undefined)
let id: string; // (default to undefined)

const { status, data } = await apiInstance.document(
    doc,
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **doc** | [**string**] |  | defaults to undefined|
| **id** | [**string**] |  | defaults to undefined|


### Return type

**ShippingDocument**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**404** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list**
> Shipment list()

Retrieve all shipments.

### Example

```typescript
import {
    ShipmentsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ShipmentsApi(configuration);

let address: string; // (optional) (default to undefined)
let carrierName: string; //The unique carrier slug. <br/>Values: `aramex`, `asendia_us`, `australiapost`, `boxknight`, `bpost`, `canadapost`, `canpar`, `chronopost`, `colissimo`, `dhl_express`, `dhl_parcel_de`, `dhl_poland`, `dhl_universal`, `dicom`, `dpd`, `dpd_meta`, `dtdc`, `easypost`, `easyship`, `eshipper`, `fedex`, `freightcom`, `generic`, `geodis`, `gls`, `hay_post`, `hermes`, `landmark`, `laposte`, `locate2u`, `mydhl`, `nationex`, `parcelone`, `postat`, `purolator`, `roadie`, `royalmail`, `sapient`, `seko`, `sendle`, `shipengine`, `teleship`, `tge`, `tnt`, `ups`, `usps`, `usps_international`, `veho`, `zoom2u` (optional) (default to undefined)
let createdAfter: string; // (optional) (default to undefined)
let createdBefore: string; // (optional) (default to undefined)
let hasManifest: boolean; // (optional) (default to undefined)
let hasTracker: boolean; // (optional) (default to undefined)
let id: string; // (optional) (default to undefined)
let keyword: string; // (optional) (default to undefined)
let metaKey: string; // (optional) (default to undefined)
let metaValue: string; // (optional) (default to undefined)
let metadataKey: string; // (optional) (default to undefined)
let metadataValue: string; // (optional) (default to undefined)
let optionKey: string; // (optional) (default to undefined)
let optionValue: string; // (optional) (default to undefined)
let reference: string; // (optional) (default to undefined)
let service: string; // (optional) (default to undefined)
let status: string; //Valid shipment status. <br/>Values: `draft`, `purchased`, `cancelled`, `shipped`, `in_transit`, `delivered`, `needs_attention`, `out_for_delivery`, `delivery_failed` (optional) (default to undefined)
let trackingNumber: string; // (optional) (default to undefined)

const { status, data } = await apiInstance.list(
    address,
    carrierName,
    createdAfter,
    createdBefore,
    hasManifest,
    hasTracker,
    id,
    keyword,
    metaKey,
    metaValue,
    metadataKey,
    metadataValue,
    optionKey,
    optionValue,
    reference,
    service,
    status,
    trackingNumber
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **address** | [**string**] |  | (optional) defaults to undefined|
| **carrierName** | [**string**] | The unique carrier slug. &lt;br/&gt;Values: &#x60;aramex&#x60;, &#x60;asendia_us&#x60;, &#x60;australiapost&#x60;, &#x60;boxknight&#x60;, &#x60;bpost&#x60;, &#x60;canadapost&#x60;, &#x60;canpar&#x60;, &#x60;chronopost&#x60;, &#x60;colissimo&#x60;, &#x60;dhl_express&#x60;, &#x60;dhl_parcel_de&#x60;, &#x60;dhl_poland&#x60;, &#x60;dhl_universal&#x60;, &#x60;dicom&#x60;, &#x60;dpd&#x60;, &#x60;dpd_meta&#x60;, &#x60;dtdc&#x60;, &#x60;easypost&#x60;, &#x60;easyship&#x60;, &#x60;eshipper&#x60;, &#x60;fedex&#x60;, &#x60;freightcom&#x60;, &#x60;generic&#x60;, &#x60;geodis&#x60;, &#x60;gls&#x60;, &#x60;hay_post&#x60;, &#x60;hermes&#x60;, &#x60;landmark&#x60;, &#x60;laposte&#x60;, &#x60;locate2u&#x60;, &#x60;mydhl&#x60;, &#x60;nationex&#x60;, &#x60;parcelone&#x60;, &#x60;postat&#x60;, &#x60;purolator&#x60;, &#x60;roadie&#x60;, &#x60;royalmail&#x60;, &#x60;sapient&#x60;, &#x60;seko&#x60;, &#x60;sendle&#x60;, &#x60;shipengine&#x60;, &#x60;teleship&#x60;, &#x60;tge&#x60;, &#x60;tnt&#x60;, &#x60;ups&#x60;, &#x60;usps&#x60;, &#x60;usps_international&#x60;, &#x60;veho&#x60;, &#x60;zoom2u&#x60; | (optional) defaults to undefined|
| **createdAfter** | [**string**] |  | (optional) defaults to undefined|
| **createdBefore** | [**string**] |  | (optional) defaults to undefined|
| **hasManifest** | [**boolean**] |  | (optional) defaults to undefined|
| **hasTracker** | [**boolean**] |  | (optional) defaults to undefined|
| **id** | [**string**] |  | (optional) defaults to undefined|
| **keyword** | [**string**] |  | (optional) defaults to undefined|
| **metaKey** | [**string**] |  | (optional) defaults to undefined|
| **metaValue** | [**string**] |  | (optional) defaults to undefined|
| **metadataKey** | [**string**] |  | (optional) defaults to undefined|
| **metadataValue** | [**string**] |  | (optional) defaults to undefined|
| **optionKey** | [**string**] |  | (optional) defaults to undefined|
| **optionValue** | [**string**] |  | (optional) defaults to undefined|
| **reference** | [**string**] |  | (optional) defaults to undefined|
| **service** | [**string**] |  | (optional) defaults to undefined|
| **status** | [**string**] | Valid shipment status. &lt;br/&gt;Values: &#x60;draft&#x60;, &#x60;purchased&#x60;, &#x60;cancelled&#x60;, &#x60;shipped&#x60;, &#x60;in_transit&#x60;, &#x60;delivered&#x60;, &#x60;needs_attention&#x60;, &#x60;out_for_delivery&#x60;, &#x60;delivery_failed&#x60; | (optional) defaults to undefined|
| **trackingNumber** | [**string**] |  | (optional) defaults to undefined|


### Return type

**Shipment**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**404** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **purchase**
> Shipment purchase()

Select your preferred rates to buy a shipment label.

### Example

```typescript
import {
    ShipmentsApi,
    Configuration,
    ShipmentPurchaseData
} from './api';

const configuration = new Configuration();
const apiInstance = new ShipmentsApi(configuration);

let id: string; // (default to undefined)
let shipmentPurchaseData: ShipmentPurchaseData; // (optional)

const { status, data } = await apiInstance.purchase(
    id,
    shipmentPurchaseData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **shipmentPurchaseData** | **ShipmentPurchaseData**|  | |
| **id** | [**string**] |  | defaults to undefined|


### Return type

**Shipment**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**404** |  |  -  |
|**400** |  |  -  |
|**409** |  |  -  |
|**424** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **rates**
> Shipment rates()

Refresh the list of the shipment rates

### Example

```typescript
import {
    ShipmentsApi,
    Configuration,
    ShipmentRateData
} from './api';

const configuration = new Configuration();
const apiInstance = new ShipmentsApi(configuration);

let id: string; // (default to undefined)
let shipmentRateData: ShipmentRateData; // (optional)

const { status, data } = await apiInstance.rates(
    id,
    shipmentRateData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **shipmentRateData** | **ShipmentRateData**|  | |
| **id** | [**string**] |  | defaults to undefined|


### Return type

**Shipment**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**404** |  |  -  |
|**400** |  |  -  |
|**409** |  |  -  |
|**424** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve**
> Shipment retrieve()

Retrieve a shipment.

### Example

```typescript
import {
    ShipmentsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ShipmentsApi(configuration);

let id: string; // (default to undefined)

const { status, data } = await apiInstance.retrieve(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**string**] |  | defaults to undefined|


### Return type

**Shipment**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**404** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update**
> Shipment update()

This operation allows for updating properties of a shipment including `label_type`, `reference`, `payment`, `options` and `metadata`. It is not for editing the parcels of a shipment.

### Example

```typescript
import {
    ShipmentsApi,
    Configuration,
    ShipmentUpdateData
} from './api';

const configuration = new Configuration();
const apiInstance = new ShipmentsApi(configuration);

let id: string; // (default to undefined)
let shipmentUpdateData: ShipmentUpdateData; // (optional)

const { status, data } = await apiInstance.update(
    id,
    shipmentUpdateData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **shipmentUpdateData** | **ShipmentUpdateData**|  | |
| **id** | [**string**] |  | defaults to undefined|


### Return type

**Shipment**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**404** |  |  -  |
|**400** |  |  -  |
|**409** |  |  -  |
|**424** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

