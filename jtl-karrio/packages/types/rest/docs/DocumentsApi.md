# DocumentsApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**create**](#create) | **POST** /v1/documents/templates | Create a template|
|[**discard**](#discard) | **DELETE** /v1/documents/templates/{id} | Delete a template|
|[**generateDocument**](#generatedocument) | **POST** /v1/documents/generate | Generate a document|
|[**list**](#list) | **GET** /v1/documents/templates | List all templates|
|[**retrieve**](#retrieve) | **GET** /v1/documents/templates/{id} | Retrieve a template|
|[**retrieveUpload**](#retrieveupload) | **GET** /v1/documents/uploads/{id} | Retrieve upload record|
|[**update**](#update) | **PATCH** /v1/documents/templates/{id} | Update a template|
|[**upload**](#upload) | **POST** /v1/documents/uploads | Upload documents|
|[**uploads**](#uploads) | **GET** /v1/documents/uploads | List all upload records|

# **create**
> DocumentTemplate create(documentTemplateData)

Create a new template.

### Example

```typescript
import {
    DocumentsApi,
    Configuration,
    DocumentTemplateData
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentsApi(configuration);

let documentTemplateData: DocumentTemplateData; //

const { status, data } = await apiInstance.create(
    documentTemplateData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **documentTemplateData** | **DocumentTemplateData**|  | |


### Return type

**DocumentTemplate**

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
> DocumentTemplate discard()

Delete a template.

### Example

```typescript
import {
    DocumentsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentsApi(configuration);

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

**DocumentTemplate**

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

# **generateDocument**
> GeneratedDocument generateDocument()

Generate any document. This API is designed to be used to generate GS1 labels, invoices and any document that requires external data.

### Example

```typescript
import {
    DocumentsApi,
    Configuration,
    DocumentData
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentsApi(configuration);

let documentData: DocumentData; // (optional)

const { status, data } = await apiInstance.generateDocument(
    documentData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **documentData** | **DocumentData**|  | |


### Return type

**GeneratedDocument**

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
|**404** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list**
> DocumentTemplateList list()

Retrieve all templates.

### Example

```typescript
import {
    DocumentsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentsApi(configuration);

const { status, data } = await apiInstance.list();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**DocumentTemplateList**

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
> DocumentTemplate retrieve()

Retrieve a template.

### Example

```typescript
import {
    DocumentsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentsApi(configuration);

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

**DocumentTemplate**

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

# **retrieveUpload**
> DocumentUploadRecord retrieveUpload()

Retrieve a shipping document upload record.

### Example

```typescript
import {
    DocumentsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentsApi(configuration);

let id: string; // (default to undefined)

const { status, data } = await apiInstance.retrieveUpload(
    id
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **id** | [**string**] |  | defaults to undefined|


### Return type

**DocumentUploadRecord**

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
> DocumentTemplate update()

update a template.

### Example

```typescript
import {
    DocumentsApi,
    Configuration,
    PatchedDocumentTemplateData
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentsApi(configuration);

let id: string; // (default to undefined)
let patchedDocumentTemplateData: PatchedDocumentTemplateData; // (optional)

const { status, data } = await apiInstance.update(
    id,
    patchedDocumentTemplateData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedDocumentTemplateData** | **PatchedDocumentTemplateData**|  | |
| **id** | [**string**] |  | defaults to undefined|


### Return type

**DocumentTemplate**

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

# **upload**
> DocumentUploadRecord upload(documentUploadData)

Upload a shipping document.

### Example

```typescript
import {
    DocumentsApi,
    Configuration,
    DocumentUploadData
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentsApi(configuration);

let documentUploadData: DocumentUploadData; //

const { status, data } = await apiInstance.upload(
    documentUploadData
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **documentUploadData** | **DocumentUploadData**|  | |


### Return type

**DocumentUploadRecord**

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

# **uploads**
> DocumentUploadRecords uploads()

Retrieve all shipping document upload records.

### Example

```typescript
import {
    DocumentsApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new DocumentsApi(configuration);

let createdAfter: string; // (optional) (default to undefined)
let createdBefore: string; // (optional) (default to undefined)
let shipmentId: string; // (optional) (default to undefined)

const { status, data } = await apiInstance.uploads(
    createdAfter,
    createdBefore,
    shipmentId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **createdAfter** | [**string**] |  | (optional) defaults to undefined|
| **createdBefore** | [**string**] |  | (optional) defaults to undefined|
| **shipmentId** | [**string**] |  | (optional) defaults to undefined|


### Return type

**DocumentUploadRecords**

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

