# AddressesApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**create**](#create) | **POST** /v1/addresses | Create an address|
|[**discard**](#discard) | **DELETE** /v1/addresses/{id} | Discard an address|
|[**list**](#list) | **GET** /v1/addresses | List all addresses|
|[**retrieve**](#retrieve) | **GET** /v1/addresses/{id} | Retrieve an address|
|[**update**](#update) | **PATCH** /v1/addresses/{id} | Update an address|

# **create**
> Address create(addressData)

Create a new address.

### Example

```typescript
import {
    AddressesApi,
    Configuration,
    AddressData
} from './api';

const configuration = new Configuration();
const apiInstance = new AddressesApi(configuration);

let addressData: AddressData; //

const { status, data } = await apiInstance.create(
    addressData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **addressData** | **AddressData**|  | |


### Return type

**Address**

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
> Address discard()

Discard an address.

### Example

```typescript
import {
    AddressesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AddressesApi(configuration);

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

**Address**

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
> AddressList list()

         Retrieve all addresses.          Query Parameters:         - label: Filter by meta.label (case-insensitive contains)         - keyword: Search across label, address fields, contact info         - usage: Filter by meta.usage (exact match in array)         

### Example

```typescript
import {
    AddressesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AddressesApi(configuration);

const { status, data } = await apiInstance.list();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**AddressList**

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
> Address retrieve()

Retrieve an address.

### Example

```typescript
import {
    AddressesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new AddressesApi(configuration);

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

**Address**

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
> Address update()

update an address.

### Example

```typescript
import {
    AddressesApi,
    Configuration,
    PatchedAddressData
} from './api';

const configuration = new Configuration();
const apiInstance = new AddressesApi(configuration);

let id: string; // (default to undefined)
let patchedAddressData: PatchedAddressData; // (optional)

const { status, data } = await apiInstance.update(
    id,
    patchedAddressData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedAddressData** | **PatchedAddressData**|  | |
| **id** | [**string**] |  | defaults to undefined|


### Return type

**Address**

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

