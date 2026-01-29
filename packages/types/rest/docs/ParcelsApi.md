# ParcelsApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**create**](#create) | **POST** /v1/parcels | Create a parcel|
|[**discard**](#discard) | **DELETE** /v1/parcels/{id} | Remove a parcel|
|[**list**](#list) | **GET** /v1/parcels | List all parcels|
|[**retrieve**](#retrieve) | **GET** /v1/parcels/{id} | Retrieve a parcel|
|[**update**](#update) | **PATCH** /v1/parcels/{id} | Update a parcel|

# **create**
> Parcel create(parcelData)

Create a new parcel.

### Example

```typescript
import {
    ParcelsApi,
    Configuration,
    ParcelData
} from './api';

const configuration = new Configuration();
const apiInstance = new ParcelsApi(configuration);

let parcelData: ParcelData; //

const { status, data } = await apiInstance.create(
    parcelData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **parcelData** | **ParcelData**|  | |


### Return type

**Parcel**

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
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **discard**
> Parcel discard()

Remove a parcel.

### Example

```typescript
import {
    ParcelsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ParcelsApi(configuration);

let id: string; // (default to undefined)

const { status, data } = await apiInstance.discard(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**string**] |  | defaults to undefined|


### Return type

**Parcel**

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

# **list**
> ParcelList list()

         Retrieve all stored parcels.          Query Parameters:         - label: Filter by meta.label (case-insensitive contains)         - keyword: Search by label         - usage: Filter by meta.usage (exact match in array)         

### Example

```typescript
import {
    ParcelsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ParcelsApi(configuration);

const { status, data } = await apiInstance.list();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**ParcelList**

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
> Parcel retrieve()

Retrieve a parcel.

### Example

```typescript
import {
    ParcelsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new ParcelsApi(configuration);

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

**Parcel**

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
> Parcel update()

modify an existing parcel\'s details.

### Example

```typescript
import {
    ParcelsApi,
    Configuration,
    PatchedParcelData
} from './api';

const configuration = new Configuration();
const apiInstance = new ParcelsApi(configuration);

let id: string; // (default to undefined)
let patchedParcelData: PatchedParcelData; // (optional)

const { status, data } = await apiInstance.update(
    id,
    patchedParcelData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedParcelData** | **PatchedParcelData**|  | |
| **id** | [**string**] |  | defaults to undefined|


### Return type

**Parcel**

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
|**409** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

