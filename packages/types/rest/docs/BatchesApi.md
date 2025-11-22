# BatchesApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**createOrders**](#createorders) | **POST** /v1/batches/orders | Create order batch|
|[**createShipments**](#createshipments) | **POST** /v1/batches/shipments | Create shipment batch|
|[**createTrackers**](#createtrackers) | **POST** /v1/batches/trackers | Create tracker batch|
|[**exportFile**](#exportfile) | **GET** /v1/batches/data/export/{resource_type}.{export_format} | Export data files|
|[**importFile**](#importfile) | **POST** /v1/batches/data/import | Import data files|
|[**list**](#list) | **GET** /v1/batches/operations | List all batch operations|
|[**retrieve**](#retrieve) | **GET** /v1/batches/operations/{id} | Retrieve a batch operation|

# **createOrders**
> BatchOperation createOrders(batchOrderData)

Create order batch. `Beta`

### Example

```typescript
import {
    BatchesApi,
    Configuration,
    BatchOrderData
} from './api';

const configuration = new Configuration();
const apiInstance = new BatchesApi(configuration);

let batchOrderData: BatchOrderData; //

const { status, data } = await apiInstance.createOrders(
    batchOrderData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **batchOrderData** | **BatchOrderData**|  | |


### Return type

**BatchOperation**

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
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **createShipments**
> BatchOperation createShipments(batchShipmentData)

Create shipment batch. `Beta`

### Example

```typescript
import {
    BatchesApi,
    Configuration,
    BatchShipmentData
} from './api';

const configuration = new Configuration();
const apiInstance = new BatchesApi(configuration);

let batchShipmentData: BatchShipmentData; //

const { status, data } = await apiInstance.createShipments(
    batchShipmentData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **batchShipmentData** | **BatchShipmentData**|  | |


### Return type

**BatchOperation**

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
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **createTrackers**
> BatchOperation createTrackers(batchTrackerData)

Create tracker batch. `Beta`

### Example

```typescript
import {
    BatchesApi,
    Configuration,
    BatchTrackerData
} from './api';

const configuration = new Configuration();
const apiInstance = new BatchesApi(configuration);

let batchTrackerData: BatchTrackerData; //

const { status, data } = await apiInstance.createTrackers(
    batchTrackerData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **batchTrackerData** | **BatchTrackerData**|  | |


### Return type

**BatchOperation**

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
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **exportFile**
> File exportFile()


### Example

```typescript
import {
    BatchesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new BatchesApi(configuration);

let exportFormat: 'billing' | 'order' | 'shipment' | 'trackers'; // (default to undefined)
let resourceType: 'billing' | 'order' | 'shipment' | 'trackers'; // (default to undefined)
let dataTemplate: string; //A data template slug to use for the import.<br/>         **When nothing is specified, the system default headers are expected.**          (optional) (default to undefined)

const { status, data } = await apiInstance.exportFile(
    exportFormat,
    resourceType,
    dataTemplate
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **exportFormat** | [**&#39;billing&#39; | &#39;order&#39; | &#39;shipment&#39; | &#39;trackers&#39;**]**Array<&#39;billing&#39; &#124; &#39;order&#39; &#124; &#39;shipment&#39; &#124; &#39;trackers&#39;>** |  | defaults to undefined|
| **resourceType** | [**&#39;billing&#39; | &#39;order&#39; | &#39;shipment&#39; | &#39;trackers&#39;**]**Array<&#39;billing&#39; &#124; &#39;order&#39; &#124; &#39;shipment&#39; &#124; &#39;trackers&#39;>** |  | defaults to undefined|
| **dataTemplate** | [**string**] | A data template slug to use for the import.&lt;br/&gt;         **When nothing is specified, the system default headers are expected.**          | (optional) defaults to undefined|


### Return type

**File**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream, application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**409** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **importFile**
> BatchOperation importFile()

Import csv, xls and xlsx data files for: `Beta`<br/> - trackers data - orders data - shipments data - billing data (soon)<br/><br/> **This operation will return a batch operation that you can poll to follow the import progression.**

### Example

```typescript
import {
    BatchesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new BatchesApi(configuration);

let dataFile: File; // (optional) (default to undefined)
let dataTemplate: string; //A data template slug to use for the import.<br/>         **When nothing is specified, the system default headers are expected.**          (optional) (default to undefined)
let resourceType: 'billing' | 'order' | 'shipment' | 'trackers'; //The type of the resource to import (optional) (default to undefined)
let resourceType2: string; // (optional) (default to undefined)
let dataTemplate2: string; // (optional) (default to undefined)
let dataFile2: File; // (optional) (default to undefined)

const { status, data } = await apiInstance.importFile(
    dataFile,
    dataTemplate,
    resourceType,
    resourceType2,
    dataTemplate2,
    dataFile2
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **dataFile** | [**File**] |  | (optional) defaults to undefined|
| **dataTemplate** | [**string**] | A data template slug to use for the import.&lt;br/&gt;         **When nothing is specified, the system default headers are expected.**          | (optional) defaults to undefined|
| **resourceType** | [**&#39;billing&#39; | &#39;order&#39; | &#39;shipment&#39; | &#39;trackers&#39;**]**Array<&#39;billing&#39; &#124; &#39;order&#39; &#124; &#39;shipment&#39; &#124; &#39;trackers&#39;>** | The type of the resource to import | (optional) defaults to undefined|
| **resourceType2** | [**string**] |  | (optional) defaults to undefined|
| **dataTemplate2** | [**string**] |  | (optional) defaults to undefined|
| **dataFile2** | [**File**] |  | (optional) defaults to undefined|


### Return type

**BatchOperation**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**202** |  |  -  |
|**400** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list**
> BatchOperations list()

Retrieve all batch operations. `Beta`

### Example

```typescript
import {
    BatchesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new BatchesApi(configuration);

const { status, data } = await apiInstance.list();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**BatchOperations**

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
> BatchOperation retrieve()

Retrieve a batch operation. `Beta`

### Example

```typescript
import {
    BatchesApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new BatchesApi(configuration);

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

**BatchOperation**

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

