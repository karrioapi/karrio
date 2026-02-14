# WebhooksApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**create**](#create) | **POST** /v1/webhooks | Create a webhook|
|[**list**](#list) | **GET** /v1/webhooks | List all webhooks|
|[**remove**](#remove) | **DELETE** /v1/webhooks/{id} | Remove a webhook|
|[**retrieve**](#retrieve) | **GET** /v1/webhooks/{id} | Retrieve a webhook|
|[**test**](#test) | **POST** /v1/webhooks/{id}/test | Test a webhook|
|[**update**](#update) | **PATCH** /v1/webhooks/{id} | Update a webhook|

# **create**
> Webhook create(webhookData)

Create a new webhook.

### Example

```typescript
import {
    WebhooksApi,
    Configuration,
    WebhookData
} from './api';

const configuration = new Configuration();
const apiInstance = new WebhooksApi(configuration);

let webhookData: WebhookData; //

const { status, data } = await apiInstance.create(
    webhookData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **webhookData** | **WebhookData**|  | |


### Return type

**Webhook**

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

# **list**
> WebhookList list()

Retrieve all webhooks.

### Example

```typescript
import {
    WebhooksApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new WebhooksApi(configuration);

const { status, data } = await apiInstance.list();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**WebhookList**

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
> Operation remove()

Remove a webhook.

### Example

```typescript
import {
    WebhooksApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new WebhooksApi(configuration);

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

**Operation**

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
> Webhook retrieve()

Retrieve a webhook.

### Example

```typescript
import {
    WebhooksApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new WebhooksApi(configuration);

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

**Webhook**

### Authorization

[OAuth2](../README.md#OAuth2), [JWT](../README.md#JWT), [TokenBasic](../README.md#TokenBasic), [Token](../README.md#Token)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** |  |  -  |
|**404** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test**
> Operation test()

test a webhook.

### Example

```typescript
import {
    WebhooksApi,
    Configuration,
    WebhookTestRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new WebhooksApi(configuration);

let id: string; // (default to undefined)
let webhookTestRequest: WebhookTestRequest; // (optional)

const { status, data } = await apiInstance.test(
    id,
    webhookTestRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **webhookTestRequest** | **WebhookTestRequest**|  | |
| **id** | [**string**] |  | defaults to undefined|


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
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update**
> Webhook update()

update a webhook.

### Example

```typescript
import {
    WebhooksApi,
    Configuration,
    PatchedWebhookData
} from './api';

const configuration = new Configuration();
const apiInstance = new WebhooksApi(configuration);

let id: string; // (default to undefined)
let patchedWebhookData: PatchedWebhookData; // (optional)

const { status, data } = await apiInstance.update(
    id,
    patchedWebhookData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedWebhookData** | **PatchedWebhookData**|  | |
| **id** | [**string**] |  | defaults to undefined|


### Return type

**Webhook**

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
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

