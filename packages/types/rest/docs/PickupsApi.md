# PickupsApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**cancel**](#cancel) | **POST** /v1/pickups/{id}/cancel | Cancel a pickup|
|[**list**](#list) | **GET** /v1/pickups | List shipment pickups|
|[**retrieve**](#retrieve) | **GET** /v1/pickups/{id} | Retrieve a pickup|
|[**schedule**](#schedule) | **POST** /v1/pickups/{carrier_name}/schedule | Schedule a pickup|
|[**update**](#update) | **POST** /v1/pickups/{id} | Update a pickup|

# **cancel**
> Pickup cancel()

Cancel a pickup of one or more shipments.

### Example

```typescript
import {
    PickupsApi,
    Configuration,
    PickupCancelData
} from './api';

const configuration = new Configuration();
const apiInstance = new PickupsApi(configuration);

let id: string; // (default to undefined)
let pickupCancelData: PickupCancelData; // (optional)

const { status, data } = await apiInstance.cancel(
    id,
    pickupCancelData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **pickupCancelData** | **PickupCancelData**|  | |
| **id** | [**string**] |  | defaults to undefined|


### Return type

**Pickup**

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
|**409** |  |  -  |
|**424** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list**
> PickupList list()

Retrieve all scheduled pickups.

### Example

```typescript
import {
    PickupsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new PickupsApi(configuration);

let address: string; // (optional) (default to undefined)
let carrierName: string; //The unique carrier slug. <br/>Values: `aramex`, `asendia`, `asendia_us`, `australiapost`, `boxknight`, `bpost`, `canadapost`, `canpar`, `chronopost`, `colissimo`, `dhl_express`, `dhl_parcel_de`, `dhl_poland`, `dhl_universal`, `dicom`, `dpd`, `dpd_meta`, `dtdc`, `easypost`, `easyship`, `eshipper`, `fedex`, `freightcom`, `generic`, `geodis`, `gls`, `hay_post`, `hermes`, `landmark`, `laposte`, `locate2u`, `mydhl`, `nationex`, `parcelone`, `postat`, `purolator`, `roadie`, `royalmail`, `sapient`, `seko`, `sendle`, `shipengine`, `spring`, `teleship`, `tge`, `tnt`, `ups`, `usps`, `usps_international`, `veho`, `zoom2u` (optional) (default to undefined)
let confirmationNumber: string; // (optional) (default to undefined)
let createdAfter: string; // (optional) (default to undefined)
let createdBefore: string; // (optional) (default to undefined)
let keyword: string; // (optional) (default to undefined)
let pickupDateAfter: string; // (optional) (default to undefined)
let pickupDateBefore: string; // (optional) (default to undefined)

const { status, data } = await apiInstance.list(
    address,
    carrierName,
    confirmationNumber,
    createdAfter,
    createdBefore,
    keyword,
    pickupDateAfter,
    pickupDateBefore
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **address** | [**string**] |  | (optional) defaults to undefined|
| **carrierName** | [**string**] | The unique carrier slug. &lt;br/&gt;Values: &#x60;aramex&#x60;, &#x60;asendia&#x60;, &#x60;asendia_us&#x60;, &#x60;australiapost&#x60;, &#x60;boxknight&#x60;, &#x60;bpost&#x60;, &#x60;canadapost&#x60;, &#x60;canpar&#x60;, &#x60;chronopost&#x60;, &#x60;colissimo&#x60;, &#x60;dhl_express&#x60;, &#x60;dhl_parcel_de&#x60;, &#x60;dhl_poland&#x60;, &#x60;dhl_universal&#x60;, &#x60;dicom&#x60;, &#x60;dpd&#x60;, &#x60;dpd_meta&#x60;, &#x60;dtdc&#x60;, &#x60;easypost&#x60;, &#x60;easyship&#x60;, &#x60;eshipper&#x60;, &#x60;fedex&#x60;, &#x60;freightcom&#x60;, &#x60;generic&#x60;, &#x60;geodis&#x60;, &#x60;gls&#x60;, &#x60;hay_post&#x60;, &#x60;hermes&#x60;, &#x60;landmark&#x60;, &#x60;laposte&#x60;, &#x60;locate2u&#x60;, &#x60;mydhl&#x60;, &#x60;nationex&#x60;, &#x60;parcelone&#x60;, &#x60;postat&#x60;, &#x60;purolator&#x60;, &#x60;roadie&#x60;, &#x60;royalmail&#x60;, &#x60;sapient&#x60;, &#x60;seko&#x60;, &#x60;sendle&#x60;, &#x60;shipengine&#x60;, &#x60;spring&#x60;, &#x60;teleship&#x60;, &#x60;tge&#x60;, &#x60;tnt&#x60;, &#x60;ups&#x60;, &#x60;usps&#x60;, &#x60;usps_international&#x60;, &#x60;veho&#x60;, &#x60;zoom2u&#x60; | (optional) defaults to undefined|
| **confirmationNumber** | [**string**] |  | (optional) defaults to undefined|
| **createdAfter** | [**string**] |  | (optional) defaults to undefined|
| **createdBefore** | [**string**] |  | (optional) defaults to undefined|
| **keyword** | [**string**] |  | (optional) defaults to undefined|
| **pickupDateAfter** | [**string**] |  | (optional) defaults to undefined|
| **pickupDateBefore** | [**string**] |  | (optional) defaults to undefined|


### Return type

**PickupList**

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
> Pickup retrieve()

Retrieve a scheduled pickup.

### Example

```typescript
import {
    PickupsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new PickupsApi(configuration);

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

**Pickup**

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

# **schedule**
> Pickup schedule(pickupData)

Schedule a pickup for one or many shipments with labels already purchased.

### Example

```typescript
import {
    PickupsApi,
    Configuration,
    PickupData
} from './api';

const configuration = new Configuration();
const apiInstance = new PickupsApi(configuration);

let carrierName: string; // (default to undefined)
let pickupData: PickupData; //

const { status, data } = await apiInstance.schedule(
    carrierName,
    pickupData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **pickupData** | **PickupData**|  | |
| **carrierName** | [**string**] |  | defaults to undefined|


### Return type

**Pickup**

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

# **update**
> Pickup update(pickupUpdateData)

Modify a pickup for one or many shipments with labels already purchased.

### Example

```typescript
import {
    PickupsApi,
    Configuration,
    PickupUpdateData
} from './api';

const configuration = new Configuration();
const apiInstance = new PickupsApi(configuration);

let id: string; // (default to undefined)
let pickupUpdateData: PickupUpdateData; //

const { status, data } = await apiInstance.update(
    id,
    pickupUpdateData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **pickupUpdateData** | **PickupUpdateData**|  | |
| **id** | [**string**] |  | defaults to undefined|


### Return type

**Pickup**

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
|**424** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

