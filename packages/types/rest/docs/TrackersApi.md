# TrackersApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**add**](#add) | **POST** /v1/trackers | Add a package tracker|
|[**create**](#create) | **GET** /v1/trackers/{carrier_name}/{tracking_number} | Create a package tracker|
|[**inject**](#inject) | **POST** /v1/trackers/{tracker_id}/inject-events | Inject tracking events|
|[**list**](#list) | **GET** /v1/trackers | List all package trackers|
|[**remove**](#remove) | **DELETE** /v1/trackers/{id_or_tracking_number} | Discard a package tracker|
|[**retrieve**](#retrieve) | **GET** /v1/trackers/{id_or_tracking_number} | Retrieves a package tracker|
|[**update**](#update) | **PUT** /v1/trackers/{id_or_tracking_number} | Update tracker data|

# **add**
> TrackingStatus add(trackingData)

This API creates or retrieves (if existent) a tracking status object containing the details and events of a shipping in progress.

### Example

```typescript
import {
    TrackersApi,
    Configuration,
    TrackingData
} from './api';

const configuration = new Configuration();
const apiInstance = new TrackersApi(configuration);

let trackingData: TrackingData; //
let hub: string; // (optional) (default to undefined)
let pendingPickup: boolean; //Add this flag to add the tracker whether the tracking info exist or not.When the package is eventually picked up, the tracker with capture real time updates. (optional) (default to undefined)

const { status, data } = await apiInstance.add(
    trackingData,
    hub,
    pendingPickup
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **trackingData** | **TrackingData**|  | |
| **hub** | [**string**] |  | (optional) defaults to undefined|
| **pendingPickup** | [**boolean**] | Add this flag to add the tracker whether the tracking info exist or not.When the package is eventually picked up, the tracker with capture real time updates. | (optional) defaults to undefined|


### Return type

**TrackingStatus**

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

# **create**
> TrackingStatus create()

This API creates or retrieves (if existent) a tracking status object containing the details and events of a shipping in progress.

### Example

```typescript
import {
    TrackersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new TrackersApi(configuration);

let carrierName: string; // (default to undefined)
let carrierName2: 'aramex' | 'asendia' | 'asendia_us' | 'australiapost' | 'boxknight' | 'bpost' | 'canadapost' | 'canpar' | 'chronopost' | 'colissimo' | 'dhl_express' | 'dhl_parcel_de' | 'dhl_poland' | 'dhl_universal' | 'dicom' | 'dpd' | 'dpd_meta' | 'dtdc' | 'fedex' | 'generic' | 'geodis' | 'gls' | 'hay_post' | 'hermes' | 'landmark' | 'laposte' | 'locate2u' | 'mydhl' | 'nationex' | 'postat' | 'purolator' | 'roadie' | 'royalmail' | 'seko' | 'sendle' | 'spring' | 'teleship' | 'tge' | 'tnt' | 'ups' | 'usps' | 'usps_international' | 'veho' | 'zoom2u'; // (default to undefined)
let trackingNumber: string; // (default to undefined)
let hub: string; // (optional) (default to undefined)

const { status, data } = await apiInstance.create(
    carrierName,
    carrierName2,
    trackingNumber,
    hub
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **carrierName** | [**string**] |  | defaults to undefined|
| **carrierName2** | [**&#39;aramex&#39; | &#39;asendia&#39; | &#39;asendia_us&#39; | &#39;australiapost&#39; | &#39;boxknight&#39; | &#39;bpost&#39; | &#39;canadapost&#39; | &#39;canpar&#39; | &#39;chronopost&#39; | &#39;colissimo&#39; | &#39;dhl_express&#39; | &#39;dhl_parcel_de&#39; | &#39;dhl_poland&#39; | &#39;dhl_universal&#39; | &#39;dicom&#39; | &#39;dpd&#39; | &#39;dpd_meta&#39; | &#39;dtdc&#39; | &#39;fedex&#39; | &#39;generic&#39; | &#39;geodis&#39; | &#39;gls&#39; | &#39;hay_post&#39; | &#39;hermes&#39; | &#39;landmark&#39; | &#39;laposte&#39; | &#39;locate2u&#39; | &#39;mydhl&#39; | &#39;nationex&#39; | &#39;postat&#39; | &#39;purolator&#39; | &#39;roadie&#39; | &#39;royalmail&#39; | &#39;seko&#39; | &#39;sendle&#39; | &#39;spring&#39; | &#39;teleship&#39; | &#39;tge&#39; | &#39;tnt&#39; | &#39;ups&#39; | &#39;usps&#39; | &#39;usps_international&#39; | &#39;veho&#39; | &#39;zoom2u&#39;**]**Array<&#39;aramex&#39; &#124; &#39;asendia&#39; &#124; &#39;asendia_us&#39; &#124; &#39;australiapost&#39; &#124; &#39;boxknight&#39; &#124; &#39;bpost&#39; &#124; &#39;canadapost&#39; &#124; &#39;canpar&#39; &#124; &#39;chronopost&#39; &#124; &#39;colissimo&#39; &#124; &#39;dhl_express&#39; &#124; &#39;dhl_parcel_de&#39; &#124; &#39;dhl_poland&#39; &#124; &#39;dhl_universal&#39; &#124; &#39;dicom&#39; &#124; &#39;dpd&#39; &#124; &#39;dpd_meta&#39; &#124; &#39;dtdc&#39; &#124; &#39;fedex&#39; &#124; &#39;generic&#39; &#124; &#39;geodis&#39; &#124; &#39;gls&#39; &#124; &#39;hay_post&#39; &#124; &#39;hermes&#39; &#124; &#39;landmark&#39; &#124; &#39;laposte&#39; &#124; &#39;locate2u&#39; &#124; &#39;mydhl&#39; &#124; &#39;nationex&#39; &#124; &#39;postat&#39; &#124; &#39;purolator&#39; &#124; &#39;roadie&#39; &#124; &#39;royalmail&#39; &#124; &#39;seko&#39; &#124; &#39;sendle&#39; &#124; &#39;spring&#39; &#124; &#39;teleship&#39; &#124; &#39;tge&#39; &#124; &#39;tnt&#39; &#124; &#39;ups&#39; &#124; &#39;usps&#39; &#124; &#39;usps_international&#39; &#124; &#39;veho&#39; &#124; &#39;zoom2u&#39;>** |  | defaults to undefined|
| **trackingNumber** | [**string**] |  | defaults to undefined|
| **hub** | [**string**] |  | (optional) defaults to undefined|


### Return type

**TrackingStatus**

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

# **inject**
> Operation inject(trackerEventInjectRequest)

Inject tracking events into an existing tracker for testing purposes.

### Example

```typescript
import {
    TrackersApi,
    Configuration,
    TrackerEventInjectRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new TrackersApi(configuration);

let trackerId: string; // (default to undefined)
let trackerEventInjectRequest: TrackerEventInjectRequest; //

const { status, data } = await apiInstance.inject(
    trackerId,
    trackerEventInjectRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **trackerEventInjectRequest** | **TrackerEventInjectRequest**|  | |
| **trackerId** | [**string**] |  | defaults to undefined|


### Return type

**Operation**

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
|**404** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list**
> TrackerList list()

Retrieve all shipment trackers.

### Example

```typescript
import {
    TrackersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new TrackersApi(configuration);

let carrierName: string; //The unique carrier slug. <br/>Values: `aramex`, `asendia`, `asendia_us`, `australiapost`, `boxknight`, `bpost`, `canadapost`, `canpar`, `chronopost`, `colissimo`, `dhl_express`, `dhl_parcel_de`, `dhl_poland`, `dhl_universal`, `dicom`, `dpd`, `dpd_meta`, `dtdc`, `easypost`, `easyship`, `eshipper`, `fedex`, `freightcom`, `generic`, `geodis`, `gls`, `hay_post`, `hermes`, `landmark`, `laposte`, `locate2u`, `mydhl`, `nationex`, `parcelone`, `postat`, `purolator`, `roadie`, `royalmail`, `sapient`, `seko`, `sendle`, `shipengine`, `spring`, `teleship`, `tge`, `tnt`, `ups`, `usps`, `usps_international`, `veho`, `zoom2u` (optional) (default to undefined)
let createdAfter: string; // (optional) (default to undefined)
let createdBefore: string; // (optional) (default to undefined)
let keyword: string; // (optional) (default to undefined)
let status: string; //Valid tracker status. <br/>Values: `pending`, `picked_up`, `unknown`, `on_hold`, `cancelled`, `delivered`, `in_transit`, `delivery_delayed`, `out_for_delivery`, `ready_for_pickup`, `delivery_failed`, `return_to_sender` (optional) (default to undefined)
let trackingNumber: string; // (optional) (default to undefined)

const { status, data } = await apiInstance.list(
    carrierName,
    createdAfter,
    createdBefore,
    keyword,
    status,
    trackingNumber
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **carrierName** | [**string**] | The unique carrier slug. &lt;br/&gt;Values: &#x60;aramex&#x60;, &#x60;asendia&#x60;, &#x60;asendia_us&#x60;, &#x60;australiapost&#x60;, &#x60;boxknight&#x60;, &#x60;bpost&#x60;, &#x60;canadapost&#x60;, &#x60;canpar&#x60;, &#x60;chronopost&#x60;, &#x60;colissimo&#x60;, &#x60;dhl_express&#x60;, &#x60;dhl_parcel_de&#x60;, &#x60;dhl_poland&#x60;, &#x60;dhl_universal&#x60;, &#x60;dicom&#x60;, &#x60;dpd&#x60;, &#x60;dpd_meta&#x60;, &#x60;dtdc&#x60;, &#x60;easypost&#x60;, &#x60;easyship&#x60;, &#x60;eshipper&#x60;, &#x60;fedex&#x60;, &#x60;freightcom&#x60;, &#x60;generic&#x60;, &#x60;geodis&#x60;, &#x60;gls&#x60;, &#x60;hay_post&#x60;, &#x60;hermes&#x60;, &#x60;landmark&#x60;, &#x60;laposte&#x60;, &#x60;locate2u&#x60;, &#x60;mydhl&#x60;, &#x60;nationex&#x60;, &#x60;parcelone&#x60;, &#x60;postat&#x60;, &#x60;purolator&#x60;, &#x60;roadie&#x60;, &#x60;royalmail&#x60;, &#x60;sapient&#x60;, &#x60;seko&#x60;, &#x60;sendle&#x60;, &#x60;shipengine&#x60;, &#x60;spring&#x60;, &#x60;teleship&#x60;, &#x60;tge&#x60;, &#x60;tnt&#x60;, &#x60;ups&#x60;, &#x60;usps&#x60;, &#x60;usps_international&#x60;, &#x60;veho&#x60;, &#x60;zoom2u&#x60; | (optional) defaults to undefined|
| **createdAfter** | [**string**] |  | (optional) defaults to undefined|
| **createdBefore** | [**string**] |  | (optional) defaults to undefined|
| **keyword** | [**string**] |  | (optional) defaults to undefined|
| **status** | [**string**] | Valid tracker status. &lt;br/&gt;Values: &#x60;pending&#x60;, &#x60;picked_up&#x60;, &#x60;unknown&#x60;, &#x60;on_hold&#x60;, &#x60;cancelled&#x60;, &#x60;delivered&#x60;, &#x60;in_transit&#x60;, &#x60;delivery_delayed&#x60;, &#x60;out_for_delivery&#x60;, &#x60;ready_for_pickup&#x60;, &#x60;delivery_failed&#x60;, &#x60;return_to_sender&#x60; | (optional) defaults to undefined|
| **trackingNumber** | [**string**] |  | (optional) defaults to undefined|


### Return type

**TrackerList**

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

# **remove**
> TrackingStatus remove()

Discard a package tracker.

### Example

```typescript
import {
    TrackersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new TrackersApi(configuration);

let idOrTrackingNumber: string; // (default to undefined)

const { status, data } = await apiInstance.remove(
    idOrTrackingNumber
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **idOrTrackingNumber** | [**string**] |  | defaults to undefined|


### Return type

**TrackingStatus**

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

# **retrieve**
> TrackingStatus retrieve()

Retrieve a package tracker

### Example

```typescript
import {
    TrackersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new TrackersApi(configuration);

let idOrTrackingNumber: string; // (default to undefined)

const { status, data } = await apiInstance.retrieve(
    idOrTrackingNumber
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **idOrTrackingNumber** | [**string**] |  | defaults to undefined|


### Return type

**TrackingStatus**

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
> TrackingStatus update()

Mixin to log requests

### Example

```typescript
import {
    TrackersApi,
    Configuration,
    TrackerUpdateData
} from './api';

const configuration = new Configuration();
const apiInstance = new TrackersApi(configuration);

let idOrTrackingNumber: string; // (default to undefined)
let trackerUpdateData: TrackerUpdateData; // (optional)

const { status, data } = await apiInstance.update(
    idOrTrackingNumber,
    trackerUpdateData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **trackerUpdateData** | **TrackerUpdateData**|  | |
| **idOrTrackingNumber** | [**string**] |  | defaults to undefined|


### Return type

**TrackingStatus**

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
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

