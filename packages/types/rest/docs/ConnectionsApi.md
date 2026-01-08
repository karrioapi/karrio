# ConnectionsApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**add**](#add) | **POST** /v1/connections | Add a carrier connection|
|[**list**](#list) | **GET** /v1/connections | List carrier connections|
|[**remove**](#remove) | **DELETE** /v1/connections/{id} | Remove a carrier connection|
|[**retrieve**](#retrieve) | **GET** /v1/connections/{id} | Retrieve a connection|
|[**update**](#update) | **PATCH** /v1/connections/{id} | Update a connection|

# **add**
> CarrierConnection add(carrierConnectionData)

Add a new carrier connection.

### Example

```typescript
import {
    ConnectionsApi,
    Configuration,
    CarrierConnectionData
} from './api';

const configuration = new Configuration();
const apiInstance = new ConnectionsApi(configuration);

let carrierConnectionData: CarrierConnectionData; //

const { status, data } = await apiInstance.add(
    carrierConnectionData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **carrierConnectionData** | **CarrierConnectionData**|  | |


### Return type

**CarrierConnection**

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

# **list**
> CarrierConnectionList list()

Retrieve all carrier connections

### Example

```typescript
import {
    ConnectionsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ConnectionsApi(configuration);

let active: boolean; // (optional) (default to undefined)
let carrierName: string; //The unique carrier slug. <br/>Values: `aramex`, `asendia_us`, `australiapost`, `boxknight`, `bpost`, `canadapost`, `canpar`, `chronopost`, `colissimo`, `dhl_express`, `dhl_parcel_de`, `dhl_poland`, `dhl_universal`, `dicom`, `dpd`, `dpd_meta`, `dtdc`, `easypost`, `easyship`, `eshipper`, `fedex`, `freightcom`, `generic`, `geodis`, `gls`, `hay_post`, `hermes`, `landmark`, `laposte`, `locate2u`, `mydhl`, `nationex`, `parcelone`, `postat`, `purolator`, `roadie`, `royalmail`, `sapient`, `seko`, `sendle`, `shipengine`, `teleship`, `tge`, `tnt`, `ups`, `usps`, `usps_international`, `veho`, `zoom2u` (optional) (default to undefined)
let metadataKey: string; // (optional) (default to undefined)
let metadataValue: string; // (optional) (default to undefined)
let systemOnly: boolean; // (optional) (default to undefined)

const { status, data } = await apiInstance.list(
    active,
    carrierName,
    metadataKey,
    metadataValue,
    systemOnly
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **active** | [**boolean**] |  | (optional) defaults to undefined|
| **carrierName** | [**string**] | The unique carrier slug. &lt;br/&gt;Values: &#x60;aramex&#x60;, &#x60;asendia_us&#x60;, &#x60;australiapost&#x60;, &#x60;boxknight&#x60;, &#x60;bpost&#x60;, &#x60;canadapost&#x60;, &#x60;canpar&#x60;, &#x60;chronopost&#x60;, &#x60;colissimo&#x60;, &#x60;dhl_express&#x60;, &#x60;dhl_parcel_de&#x60;, &#x60;dhl_poland&#x60;, &#x60;dhl_universal&#x60;, &#x60;dicom&#x60;, &#x60;dpd&#x60;, &#x60;dpd_meta&#x60;, &#x60;dtdc&#x60;, &#x60;easypost&#x60;, &#x60;easyship&#x60;, &#x60;eshipper&#x60;, &#x60;fedex&#x60;, &#x60;freightcom&#x60;, &#x60;generic&#x60;, &#x60;geodis&#x60;, &#x60;gls&#x60;, &#x60;hay_post&#x60;, &#x60;hermes&#x60;, &#x60;landmark&#x60;, &#x60;laposte&#x60;, &#x60;locate2u&#x60;, &#x60;mydhl&#x60;, &#x60;nationex&#x60;, &#x60;parcelone&#x60;, &#x60;postat&#x60;, &#x60;purolator&#x60;, &#x60;roadie&#x60;, &#x60;royalmail&#x60;, &#x60;sapient&#x60;, &#x60;seko&#x60;, &#x60;sendle&#x60;, &#x60;shipengine&#x60;, &#x60;teleship&#x60;, &#x60;tge&#x60;, &#x60;tnt&#x60;, &#x60;ups&#x60;, &#x60;usps&#x60;, &#x60;usps_international&#x60;, &#x60;veho&#x60;, &#x60;zoom2u&#x60; | (optional) defaults to undefined|
| **metadataKey** | [**string**] |  | (optional) defaults to undefined|
| **metadataValue** | [**string**] |  | (optional) defaults to undefined|
| **systemOnly** | [**boolean**] |  | (optional) defaults to undefined|


### Return type

**CarrierConnectionList**

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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove**
> CarrierConnection remove()

Remove a carrier connection.

### Example

```typescript
import {
    ConnectionsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ConnectionsApi(configuration);

let id: string; // (default to undefined)

const { status, data } = await apiInstance.remove(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**string**] |  | defaults to undefined|


### Return type

**CarrierConnection**

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
|**409** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve**
> CarrierConnection retrieve()

Retrieve carrier connection.

### Example

```typescript
import {
    ConnectionsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ConnectionsApi(configuration);

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

**CarrierConnection**

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
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update**
> CarrierConnection update()

Update a carrier connection.

### Example

```typescript
import {
    ConnectionsApi,
    Configuration,
    PatchedCarrierConnectionData
} from './api';

const configuration = new Configuration();
const apiInstance = new ConnectionsApi(configuration);

let id: string; // (default to undefined)
let patchedCarrierConnectionData: PatchedCarrierConnectionData; // (optional)

const { status, data } = await apiInstance.update(
    id,
    patchedCarrierConnectionData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedCarrierConnectionData** | **PatchedCarrierConnectionData**|  | |
| **id** | [**string**] |  | defaults to undefined|


### Return type

**CarrierConnection**

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

