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

const { status, data } = await apiInstance.list();
```

### Parameters
This endpoint does not have any parameters.


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

