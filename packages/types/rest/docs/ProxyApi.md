# ProxyApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**buyLabel**](#buylabel) | **POST** /v1/proxy/shipping | Buy a shipment label|
|[**cancelPickup**](#cancelpickup) | **POST** /v1/proxy/pickups/{carrier_name}/cancel | Cancel a pickup|
|[**fetchRates**](#fetchrates) | **POST** /v1/proxy/rates | Fetch shipment rates|
|[**generateManifest**](#generatemanifest) | **POST** /v1/proxy/manifest | Create a manifest|
|[**getTracking**](#gettracking) | **POST** /v1/proxy/tracking | Get tracking details|
|[**schedulePickup**](#schedulepickup) | **POST** /v1/proxy/pickups/{carrier_name} | Schedule a pickup|
|[**trackShipment**](#trackshipment) | **GET** /v1/proxy/tracking/{carrier_name}/{tracking_number} | Track a shipment|
|[**updatePickup**](#updatepickup) | **POST** /v1/proxy/pickups/{carrier_name}/update | Update a pickup|
|[**voidLabel**](#voidlabel) | **POST** /v1/proxy/shipping/{carrier_name}/cancel | Void a shipment label|

# **buyLabel**
> ShippingResponse buyLabel(shippingRequest)

Once the shipping rates are retrieved, provide the required info to submit the shipment by specifying your preferred rate.

### Example

```typescript
import {
    ProxyApi,
    Configuration,
    ShippingRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ProxyApi(configuration);

let shippingRequest: ShippingRequest; //

const { status, data } = await apiInstance.buyLabel(
    shippingRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **shippingRequest** | **ShippingRequest**|  | |


### Return type

**ShippingResponse**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**400** |  |  -  |
|**424** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **cancelPickup**
> OperationResponse cancelPickup(pickupCancelRequest)

Cancel a pickup previously scheduled

### Example

```typescript
import {
    ProxyApi,
    Configuration,
    PickupCancelRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ProxyApi(configuration);

let carrierName: 'aramex' | 'asendia' | 'asendia_us' | 'australiapost' | 'boxknight' | 'bpost' | 'canadapost' | 'canpar' | 'chronopost' | 'colissimo' | 'dhl_express' | 'dhl_parcel_de' | 'dhl_poland' | 'dhl_universal' | 'dicom' | 'dpd' | 'dpd_meta' | 'dtdc' | 'easypost' | 'easyship' | 'eshipper' | 'fedex' | 'freightcom' | 'generic' | 'geodis' | 'gls' | 'hay_post' | 'hermes' | 'landmark' | 'laposte' | 'locate2u' | 'mydhl' | 'nationex' | 'parcelone' | 'postat' | 'purolator' | 'roadie' | 'royalmail' | 'sapient' | 'seko' | 'sendle' | 'shipengine' | 'smartkargo' | 'spring' | 'teleship' | 'tge' | 'tnt' | 'ups' | 'usps' | 'usps_international' | 'veho' | 'zoom2u'; // (default to undefined)
let pickupCancelRequest: PickupCancelRequest; //

const { status, data } = await apiInstance.cancelPickup(
    carrierName,
    pickupCancelRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **pickupCancelRequest** | **PickupCancelRequest**|  | |
| **carrierName** | [**&#39;aramex&#39; | &#39;asendia&#39; | &#39;asendia_us&#39; | &#39;australiapost&#39; | &#39;boxknight&#39; | &#39;bpost&#39; | &#39;canadapost&#39; | &#39;canpar&#39; | &#39;chronopost&#39; | &#39;colissimo&#39; | &#39;dhl_express&#39; | &#39;dhl_parcel_de&#39; | &#39;dhl_poland&#39; | &#39;dhl_universal&#39; | &#39;dicom&#39; | &#39;dpd&#39; | &#39;dpd_meta&#39; | &#39;dtdc&#39; | &#39;easypost&#39; | &#39;easyship&#39; | &#39;eshipper&#39; | &#39;fedex&#39; | &#39;freightcom&#39; | &#39;generic&#39; | &#39;geodis&#39; | &#39;gls&#39; | &#39;hay_post&#39; | &#39;hermes&#39; | &#39;landmark&#39; | &#39;laposte&#39; | &#39;locate2u&#39; | &#39;mydhl&#39; | &#39;nationex&#39; | &#39;parcelone&#39; | &#39;postat&#39; | &#39;purolator&#39; | &#39;roadie&#39; | &#39;royalmail&#39; | &#39;sapient&#39; | &#39;seko&#39; | &#39;sendle&#39; | &#39;shipengine&#39; | &#39;smartkargo&#39; | &#39;spring&#39; | &#39;teleship&#39; | &#39;tge&#39; | &#39;tnt&#39; | &#39;ups&#39; | &#39;usps&#39; | &#39;usps_international&#39; | &#39;veho&#39; | &#39;zoom2u&#39;**]**Array<&#39;aramex&#39; &#124; &#39;asendia&#39; &#124; &#39;asendia_us&#39; &#124; &#39;australiapost&#39; &#124; &#39;boxknight&#39; &#124; &#39;bpost&#39; &#124; &#39;canadapost&#39; &#124; &#39;canpar&#39; &#124; &#39;chronopost&#39; &#124; &#39;colissimo&#39; &#124; &#39;dhl_express&#39; &#124; &#39;dhl_parcel_de&#39; &#124; &#39;dhl_poland&#39; &#124; &#39;dhl_universal&#39; &#124; &#39;dicom&#39; &#124; &#39;dpd&#39; &#124; &#39;dpd_meta&#39; &#124; &#39;dtdc&#39; &#124; &#39;easypost&#39; &#124; &#39;easyship&#39; &#124; &#39;eshipper&#39; &#124; &#39;fedex&#39; &#124; &#39;freightcom&#39; &#124; &#39;generic&#39; &#124; &#39;geodis&#39; &#124; &#39;gls&#39; &#124; &#39;hay_post&#39; &#124; &#39;hermes&#39; &#124; &#39;landmark&#39; &#124; &#39;laposte&#39; &#124; &#39;locate2u&#39; &#124; &#39;mydhl&#39; &#124; &#39;nationex&#39; &#124; &#39;parcelone&#39; &#124; &#39;postat&#39; &#124; &#39;purolator&#39; &#124; &#39;roadie&#39; &#124; &#39;royalmail&#39; &#124; &#39;sapient&#39; &#124; &#39;seko&#39; &#124; &#39;sendle&#39; &#124; &#39;shipengine&#39; &#124; &#39;smartkargo&#39; &#124; &#39;spring&#39; &#124; &#39;teleship&#39; &#124; &#39;tge&#39; &#124; &#39;tnt&#39; &#124; &#39;ups&#39; &#124; &#39;usps&#39; &#124; &#39;usps_international&#39; &#124; &#39;veho&#39; &#124; &#39;zoom2u&#39;>** |  | defaults to undefined|


### Return type

**OperationResponse**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**400** |  |  -  |
|**424** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **fetchRates**
> RateResponse fetchRates(rateRequest)

 The Shipping process begins by fetching rates for your shipment. Use this service to fetch a shipping rates available. 

### Example

```typescript
import {
    ProxyApi,
    Configuration,
    RateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ProxyApi(configuration);

let rateRequest: RateRequest; //

const { status, data } = await apiInstance.fetchRates(
    rateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **rateRequest** | **RateRequest**|  | |


### Return type

**RateResponse**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**400** |  |  -  |
|**424** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generateManifest**
> ManifestResponse generateManifest(manifestRequest)

 Some carriers require shipment manifests to be created for pickups and dropoff. Creating a manifest for a shipment also kicks off billing as a commitment or confirmation of the shipment. 

### Example

```typescript
import {
    ProxyApi,
    Configuration,
    ManifestRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ProxyApi(configuration);

let manifestRequest: ManifestRequest; //

const { status, data } = await apiInstance.generateManifest(
    manifestRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **manifestRequest** | **ManifestRequest**|  | |


### Return type

**ManifestResponse**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**400** |  |  -  |
|**424** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getTracking**
> TrackingResponse getTracking(trackingData)

You can track a shipment by specifying the carrier and the shipment tracking number.

### Example

```typescript
import {
    ProxyApi,
    Configuration,
    TrackingData
} from './api';

const configuration = new Configuration();
const apiInstance = new ProxyApi(configuration);

let trackingData: TrackingData; //
let hub: string; // (optional) (default to undefined)

const { status, data } = await apiInstance.getTracking(
    trackingData,
    hub
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **trackingData** | **TrackingData**|  | |
| **hub** | [**string**] |  | (optional) defaults to undefined|


### Return type

**TrackingResponse**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**400** |  |  -  |
|**424** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **schedulePickup**
> PickupResponse schedulePickup(pickupRequest)

Schedule one or many parcels pickup

### Example

```typescript
import {
    ProxyApi,
    Configuration,
    PickupRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ProxyApi(configuration);

let carrierName: 'aramex' | 'asendia' | 'asendia_us' | 'australiapost' | 'boxknight' | 'bpost' | 'canadapost' | 'canpar' | 'chronopost' | 'colissimo' | 'dhl_express' | 'dhl_parcel_de' | 'dhl_poland' | 'dhl_universal' | 'dicom' | 'dpd' | 'dpd_meta' | 'dtdc' | 'easypost' | 'easyship' | 'eshipper' | 'fedex' | 'freightcom' | 'generic' | 'geodis' | 'gls' | 'hay_post' | 'hermes' | 'landmark' | 'laposte' | 'locate2u' | 'mydhl' | 'nationex' | 'parcelone' | 'postat' | 'purolator' | 'roadie' | 'royalmail' | 'sapient' | 'seko' | 'sendle' | 'shipengine' | 'smartkargo' | 'spring' | 'teleship' | 'tge' | 'tnt' | 'ups' | 'usps' | 'usps_international' | 'veho' | 'zoom2u'; // (default to undefined)
let pickupRequest: PickupRequest; //

const { status, data } = await apiInstance.schedulePickup(
    carrierName,
    pickupRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **pickupRequest** | **PickupRequest**|  | |
| **carrierName** | [**&#39;aramex&#39; | &#39;asendia&#39; | &#39;asendia_us&#39; | &#39;australiapost&#39; | &#39;boxknight&#39; | &#39;bpost&#39; | &#39;canadapost&#39; | &#39;canpar&#39; | &#39;chronopost&#39; | &#39;colissimo&#39; | &#39;dhl_express&#39; | &#39;dhl_parcel_de&#39; | &#39;dhl_poland&#39; | &#39;dhl_universal&#39; | &#39;dicom&#39; | &#39;dpd&#39; | &#39;dpd_meta&#39; | &#39;dtdc&#39; | &#39;easypost&#39; | &#39;easyship&#39; | &#39;eshipper&#39; | &#39;fedex&#39; | &#39;freightcom&#39; | &#39;generic&#39; | &#39;geodis&#39; | &#39;gls&#39; | &#39;hay_post&#39; | &#39;hermes&#39; | &#39;landmark&#39; | &#39;laposte&#39; | &#39;locate2u&#39; | &#39;mydhl&#39; | &#39;nationex&#39; | &#39;parcelone&#39; | &#39;postat&#39; | &#39;purolator&#39; | &#39;roadie&#39; | &#39;royalmail&#39; | &#39;sapient&#39; | &#39;seko&#39; | &#39;sendle&#39; | &#39;shipengine&#39; | &#39;smartkargo&#39; | &#39;spring&#39; | &#39;teleship&#39; | &#39;tge&#39; | &#39;tnt&#39; | &#39;ups&#39; | &#39;usps&#39; | &#39;usps_international&#39; | &#39;veho&#39; | &#39;zoom2u&#39;**]**Array<&#39;aramex&#39; &#124; &#39;asendia&#39; &#124; &#39;asendia_us&#39; &#124; &#39;australiapost&#39; &#124; &#39;boxknight&#39; &#124; &#39;bpost&#39; &#124; &#39;canadapost&#39; &#124; &#39;canpar&#39; &#124; &#39;chronopost&#39; &#124; &#39;colissimo&#39; &#124; &#39;dhl_express&#39; &#124; &#39;dhl_parcel_de&#39; &#124; &#39;dhl_poland&#39; &#124; &#39;dhl_universal&#39; &#124; &#39;dicom&#39; &#124; &#39;dpd&#39; &#124; &#39;dpd_meta&#39; &#124; &#39;dtdc&#39; &#124; &#39;easypost&#39; &#124; &#39;easyship&#39; &#124; &#39;eshipper&#39; &#124; &#39;fedex&#39; &#124; &#39;freightcom&#39; &#124; &#39;generic&#39; &#124; &#39;geodis&#39; &#124; &#39;gls&#39; &#124; &#39;hay_post&#39; &#124; &#39;hermes&#39; &#124; &#39;landmark&#39; &#124; &#39;laposte&#39; &#124; &#39;locate2u&#39; &#124; &#39;mydhl&#39; &#124; &#39;nationex&#39; &#124; &#39;parcelone&#39; &#124; &#39;postat&#39; &#124; &#39;purolator&#39; &#124; &#39;roadie&#39; &#124; &#39;royalmail&#39; &#124; &#39;sapient&#39; &#124; &#39;seko&#39; &#124; &#39;sendle&#39; &#124; &#39;shipengine&#39; &#124; &#39;smartkargo&#39; &#124; &#39;spring&#39; &#124; &#39;teleship&#39; &#124; &#39;tge&#39; &#124; &#39;tnt&#39; &#124; &#39;ups&#39; &#124; &#39;usps&#39; &#124; &#39;usps_international&#39; &#124; &#39;veho&#39; &#124; &#39;zoom2u&#39;>** |  | defaults to undefined|


### Return type

**PickupResponse**

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

# **trackShipment**
> TrackingResponse trackShipment()

You can track a shipment by specifying the carrier and the shipment tracking number.

### Example

```typescript
import {
    ProxyApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ProxyApi(configuration);

let carrierName: 'aramex' | 'asendia' | 'asendia_us' | 'australiapost' | 'boxknight' | 'bpost' | 'canadapost' | 'canpar' | 'chronopost' | 'colissimo' | 'dhl_express' | 'dhl_parcel_de' | 'dhl_poland' | 'dhl_universal' | 'dicom' | 'dpd' | 'dpd_meta' | 'dtdc' | 'fedex' | 'generic' | 'geodis' | 'gls' | 'hay_post' | 'hermes' | 'landmark' | 'laposte' | 'locate2u' | 'mydhl' | 'nationex' | 'postat' | 'purolator' | 'roadie' | 'royalmail' | 'seko' | 'sendle' | 'smartkargo' | 'spring' | 'teleship' | 'tge' | 'tnt' | 'ups' | 'usps' | 'usps_international' | 'veho' | 'zoom2u'; // (default to undefined)
let trackingNumber: string; // (default to undefined)
let hub: string; // (optional) (default to undefined)

const { status, data } = await apiInstance.trackShipment(
    carrierName,
    trackingNumber,
    hub
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **carrierName** | [**&#39;aramex&#39; | &#39;asendia&#39; | &#39;asendia_us&#39; | &#39;australiapost&#39; | &#39;boxknight&#39; | &#39;bpost&#39; | &#39;canadapost&#39; | &#39;canpar&#39; | &#39;chronopost&#39; | &#39;colissimo&#39; | &#39;dhl_express&#39; | &#39;dhl_parcel_de&#39; | &#39;dhl_poland&#39; | &#39;dhl_universal&#39; | &#39;dicom&#39; | &#39;dpd&#39; | &#39;dpd_meta&#39; | &#39;dtdc&#39; | &#39;fedex&#39; | &#39;generic&#39; | &#39;geodis&#39; | &#39;gls&#39; | &#39;hay_post&#39; | &#39;hermes&#39; | &#39;landmark&#39; | &#39;laposte&#39; | &#39;locate2u&#39; | &#39;mydhl&#39; | &#39;nationex&#39; | &#39;postat&#39; | &#39;purolator&#39; | &#39;roadie&#39; | &#39;royalmail&#39; | &#39;seko&#39; | &#39;sendle&#39; | &#39;smartkargo&#39; | &#39;spring&#39; | &#39;teleship&#39; | &#39;tge&#39; | &#39;tnt&#39; | &#39;ups&#39; | &#39;usps&#39; | &#39;usps_international&#39; | &#39;veho&#39; | &#39;zoom2u&#39;**]**Array<&#39;aramex&#39; &#124; &#39;asendia&#39; &#124; &#39;asendia_us&#39; &#124; &#39;australiapost&#39; &#124; &#39;boxknight&#39; &#124; &#39;bpost&#39; &#124; &#39;canadapost&#39; &#124; &#39;canpar&#39; &#124; &#39;chronopost&#39; &#124; &#39;colissimo&#39; &#124; &#39;dhl_express&#39; &#124; &#39;dhl_parcel_de&#39; &#124; &#39;dhl_poland&#39; &#124; &#39;dhl_universal&#39; &#124; &#39;dicom&#39; &#124; &#39;dpd&#39; &#124; &#39;dpd_meta&#39; &#124; &#39;dtdc&#39; &#124; &#39;fedex&#39; &#124; &#39;generic&#39; &#124; &#39;geodis&#39; &#124; &#39;gls&#39; &#124; &#39;hay_post&#39; &#124; &#39;hermes&#39; &#124; &#39;landmark&#39; &#124; &#39;laposte&#39; &#124; &#39;locate2u&#39; &#124; &#39;mydhl&#39; &#124; &#39;nationex&#39; &#124; &#39;postat&#39; &#124; &#39;purolator&#39; &#124; &#39;roadie&#39; &#124; &#39;royalmail&#39; &#124; &#39;seko&#39; &#124; &#39;sendle&#39; &#124; &#39;smartkargo&#39; &#124; &#39;spring&#39; &#124; &#39;teleship&#39; &#124; &#39;tge&#39; &#124; &#39;tnt&#39; &#124; &#39;ups&#39; &#124; &#39;usps&#39; &#124; &#39;usps_international&#39; &#124; &#39;veho&#39; &#124; &#39;zoom2u&#39;>** |  | defaults to undefined|
| **trackingNumber** | [**string**] |  | defaults to undefined|
| **hub** | [**string**] |  | (optional) defaults to undefined|


### Return type

**TrackingResponse**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**400** |  |  -  |
|**424** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **updatePickup**
> PickupResponse updatePickup(pickupUpdateRequest)

Modify a scheduled pickup

### Example

```typescript
import {
    ProxyApi,
    Configuration,
    PickupUpdateRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ProxyApi(configuration);

let carrierName: 'aramex' | 'asendia' | 'asendia_us' | 'australiapost' | 'boxknight' | 'bpost' | 'canadapost' | 'canpar' | 'chronopost' | 'colissimo' | 'dhl_express' | 'dhl_parcel_de' | 'dhl_poland' | 'dhl_universal' | 'dicom' | 'dpd' | 'dpd_meta' | 'dtdc' | 'easypost' | 'easyship' | 'eshipper' | 'fedex' | 'freightcom' | 'generic' | 'geodis' | 'gls' | 'hay_post' | 'hermes' | 'landmark' | 'laposte' | 'locate2u' | 'mydhl' | 'nationex' | 'parcelone' | 'postat' | 'purolator' | 'roadie' | 'royalmail' | 'sapient' | 'seko' | 'sendle' | 'shipengine' | 'smartkargo' | 'spring' | 'teleship' | 'tge' | 'tnt' | 'ups' | 'usps' | 'usps_international' | 'veho' | 'zoom2u'; // (default to undefined)
let pickupUpdateRequest: PickupUpdateRequest; //

const { status, data } = await apiInstance.updatePickup(
    carrierName,
    pickupUpdateRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **pickupUpdateRequest** | **PickupUpdateRequest**|  | |
| **carrierName** | [**&#39;aramex&#39; | &#39;asendia&#39; | &#39;asendia_us&#39; | &#39;australiapost&#39; | &#39;boxknight&#39; | &#39;bpost&#39; | &#39;canadapost&#39; | &#39;canpar&#39; | &#39;chronopost&#39; | &#39;colissimo&#39; | &#39;dhl_express&#39; | &#39;dhl_parcel_de&#39; | &#39;dhl_poland&#39; | &#39;dhl_universal&#39; | &#39;dicom&#39; | &#39;dpd&#39; | &#39;dpd_meta&#39; | &#39;dtdc&#39; | &#39;easypost&#39; | &#39;easyship&#39; | &#39;eshipper&#39; | &#39;fedex&#39; | &#39;freightcom&#39; | &#39;generic&#39; | &#39;geodis&#39; | &#39;gls&#39; | &#39;hay_post&#39; | &#39;hermes&#39; | &#39;landmark&#39; | &#39;laposte&#39; | &#39;locate2u&#39; | &#39;mydhl&#39; | &#39;nationex&#39; | &#39;parcelone&#39; | &#39;postat&#39; | &#39;purolator&#39; | &#39;roadie&#39; | &#39;royalmail&#39; | &#39;sapient&#39; | &#39;seko&#39; | &#39;sendle&#39; | &#39;shipengine&#39; | &#39;smartkargo&#39; | &#39;spring&#39; | &#39;teleship&#39; | &#39;tge&#39; | &#39;tnt&#39; | &#39;ups&#39; | &#39;usps&#39; | &#39;usps_international&#39; | &#39;veho&#39; | &#39;zoom2u&#39;**]**Array<&#39;aramex&#39; &#124; &#39;asendia&#39; &#124; &#39;asendia_us&#39; &#124; &#39;australiapost&#39; &#124; &#39;boxknight&#39; &#124; &#39;bpost&#39; &#124; &#39;canadapost&#39; &#124; &#39;canpar&#39; &#124; &#39;chronopost&#39; &#124; &#39;colissimo&#39; &#124; &#39;dhl_express&#39; &#124; &#39;dhl_parcel_de&#39; &#124; &#39;dhl_poland&#39; &#124; &#39;dhl_universal&#39; &#124; &#39;dicom&#39; &#124; &#39;dpd&#39; &#124; &#39;dpd_meta&#39; &#124; &#39;dtdc&#39; &#124; &#39;easypost&#39; &#124; &#39;easyship&#39; &#124; &#39;eshipper&#39; &#124; &#39;fedex&#39; &#124; &#39;freightcom&#39; &#124; &#39;generic&#39; &#124; &#39;geodis&#39; &#124; &#39;gls&#39; &#124; &#39;hay_post&#39; &#124; &#39;hermes&#39; &#124; &#39;landmark&#39; &#124; &#39;laposte&#39; &#124; &#39;locate2u&#39; &#124; &#39;mydhl&#39; &#124; &#39;nationex&#39; &#124; &#39;parcelone&#39; &#124; &#39;postat&#39; &#124; &#39;purolator&#39; &#124; &#39;roadie&#39; &#124; &#39;royalmail&#39; &#124; &#39;sapient&#39; &#124; &#39;seko&#39; &#124; &#39;sendle&#39; &#124; &#39;shipengine&#39; &#124; &#39;smartkargo&#39; &#124; &#39;spring&#39; &#124; &#39;teleship&#39; &#124; &#39;tge&#39; &#124; &#39;tnt&#39; &#124; &#39;ups&#39; &#124; &#39;usps&#39; &#124; &#39;usps_international&#39; &#124; &#39;veho&#39; &#124; &#39;zoom2u&#39;>** |  | defaults to undefined|


### Return type

**PickupResponse**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**400** |  |  -  |
|**424** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **voidLabel**
> OperationResponse voidLabel(shipmentCancelRequest)

Cancel a shipment and the label previously created

### Example

```typescript
import {
    ProxyApi,
    Configuration,
    ShipmentCancelRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new ProxyApi(configuration);

let carrierName: 'aramex' | 'asendia' | 'asendia_us' | 'australiapost' | 'boxknight' | 'bpost' | 'canadapost' | 'canpar' | 'chronopost' | 'colissimo' | 'dhl_express' | 'dhl_parcel_de' | 'dhl_poland' | 'dhl_universal' | 'dicom' | 'dpd' | 'dpd_meta' | 'dtdc' | 'easypost' | 'easyship' | 'eshipper' | 'fedex' | 'freightcom' | 'generic' | 'geodis' | 'gls' | 'hay_post' | 'hermes' | 'landmark' | 'laposte' | 'locate2u' | 'mydhl' | 'nationex' | 'parcelone' | 'postat' | 'purolator' | 'roadie' | 'royalmail' | 'sapient' | 'seko' | 'sendle' | 'shipengine' | 'smartkargo' | 'spring' | 'teleship' | 'tge' | 'tnt' | 'ups' | 'usps' | 'usps_international' | 'veho' | 'zoom2u'; // (default to undefined)
let shipmentCancelRequest: ShipmentCancelRequest; //

const { status, data } = await apiInstance.voidLabel(
    carrierName,
    shipmentCancelRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **shipmentCancelRequest** | **ShipmentCancelRequest**|  | |
| **carrierName** | [**&#39;aramex&#39; | &#39;asendia&#39; | &#39;asendia_us&#39; | &#39;australiapost&#39; | &#39;boxknight&#39; | &#39;bpost&#39; | &#39;canadapost&#39; | &#39;canpar&#39; | &#39;chronopost&#39; | &#39;colissimo&#39; | &#39;dhl_express&#39; | &#39;dhl_parcel_de&#39; | &#39;dhl_poland&#39; | &#39;dhl_universal&#39; | &#39;dicom&#39; | &#39;dpd&#39; | &#39;dpd_meta&#39; | &#39;dtdc&#39; | &#39;easypost&#39; | &#39;easyship&#39; | &#39;eshipper&#39; | &#39;fedex&#39; | &#39;freightcom&#39; | &#39;generic&#39; | &#39;geodis&#39; | &#39;gls&#39; | &#39;hay_post&#39; | &#39;hermes&#39; | &#39;landmark&#39; | &#39;laposte&#39; | &#39;locate2u&#39; | &#39;mydhl&#39; | &#39;nationex&#39; | &#39;parcelone&#39; | &#39;postat&#39; | &#39;purolator&#39; | &#39;roadie&#39; | &#39;royalmail&#39; | &#39;sapient&#39; | &#39;seko&#39; | &#39;sendle&#39; | &#39;shipengine&#39; | &#39;smartkargo&#39; | &#39;spring&#39; | &#39;teleship&#39; | &#39;tge&#39; | &#39;tnt&#39; | &#39;ups&#39; | &#39;usps&#39; | &#39;usps_international&#39; | &#39;veho&#39; | &#39;zoom2u&#39;**]**Array<&#39;aramex&#39; &#124; &#39;asendia&#39; &#124; &#39;asendia_us&#39; &#124; &#39;australiapost&#39; &#124; &#39;boxknight&#39; &#124; &#39;bpost&#39; &#124; &#39;canadapost&#39; &#124; &#39;canpar&#39; &#124; &#39;chronopost&#39; &#124; &#39;colissimo&#39; &#124; &#39;dhl_express&#39; &#124; &#39;dhl_parcel_de&#39; &#124; &#39;dhl_poland&#39; &#124; &#39;dhl_universal&#39; &#124; &#39;dicom&#39; &#124; &#39;dpd&#39; &#124; &#39;dpd_meta&#39; &#124; &#39;dtdc&#39; &#124; &#39;easypost&#39; &#124; &#39;easyship&#39; &#124; &#39;eshipper&#39; &#124; &#39;fedex&#39; &#124; &#39;freightcom&#39; &#124; &#39;generic&#39; &#124; &#39;geodis&#39; &#124; &#39;gls&#39; &#124; &#39;hay_post&#39; &#124; &#39;hermes&#39; &#124; &#39;landmark&#39; &#124; &#39;laposte&#39; &#124; &#39;locate2u&#39; &#124; &#39;mydhl&#39; &#124; &#39;nationex&#39; &#124; &#39;parcelone&#39; &#124; &#39;postat&#39; &#124; &#39;purolator&#39; &#124; &#39;roadie&#39; &#124; &#39;royalmail&#39; &#124; &#39;sapient&#39; &#124; &#39;seko&#39; &#124; &#39;sendle&#39; &#124; &#39;shipengine&#39; &#124; &#39;smartkargo&#39; &#124; &#39;spring&#39; &#124; &#39;teleship&#39; &#124; &#39;tge&#39; &#124; &#39;tnt&#39; &#124; &#39;ups&#39; &#124; &#39;usps&#39; &#124; &#39;usps_international&#39; &#124; &#39;veho&#39; &#124; &#39;zoom2u&#39;>** |  | defaults to undefined|


### Return type

**OperationResponse**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**202** |  |  -  |
|**400** |  |  -  |
|**424** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

