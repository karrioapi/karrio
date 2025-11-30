# AuthApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**authenticate**](#authenticate) | **POST** /api/token | Obtain auth token pair|
|[**generateResourceToken**](#generateresourcetoken) | **POST** /api/tokens | Generate resource access token|
|[**getVerifiedToken**](#getverifiedtoken) | **POST** /api/token/verified | Get verified JWT token|
|[**refreshToken**](#refreshtoken) | **POST** /api/token/refresh | Refresh auth token|
|[**verifyToken**](#verifytoken) | **POST** /api/token/verify | Verify token|

# **authenticate**
> TokenPair authenticate(tokenObtainPair)

Authenticate the user and return a token pair

### Example

```typescript
import {
    AuthApi,
    Configuration,
    TokenObtainPair
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let tokenObtainPair: TokenObtainPair; //

const { status, data } = await apiInstance.authenticate(
    tokenObtainPair
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **tokenObtainPair** | **TokenObtainPair**|  | |


### Return type

**TokenPair**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generateResourceToken**
> ResourceTokenResponse generateResourceToken(resourceTokenRequest)

 Generate a short-lived JWT token for accessing specific resources.  This endpoint is used to create secure, time-limited access tokens for resources like shipment labels, manifests, and document templates.  **Use cases:** - Generate a token to allow document preview in a new browser window - Create shareable links for documents with automatic expiration - Enable secure document downloads without exposing API keys  **Token lifetime:** Default 5 minutes, configurable up to 1 hour.         

### Example

```typescript
import {
    AuthApi,
    Configuration,
    ResourceTokenRequest
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let resourceTokenRequest: ResourceTokenRequest; //

const { status, data } = await apiInstance.generateResourceToken(
    resourceTokenRequest
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **resourceTokenRequest** | **ResourceTokenRequest**|  | |


### Return type

**ResourceTokenResponse**

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
|**401** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **getVerifiedToken**
> TokenPair getVerifiedToken(verifiedTokenObtainPair)

Get a verified JWT token pair by submitting a Two-Factor authentication code.

### Example

```typescript
import {
    AuthApi,
    Configuration,
    VerifiedTokenObtainPair
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let verifiedTokenObtainPair: VerifiedTokenObtainPair; //

const { status, data } = await apiInstance.getVerifiedToken(
    verifiedTokenObtainPair
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **verifiedTokenObtainPair** | **VerifiedTokenObtainPair**|  | |


### Return type

**TokenPair**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **refreshToken**
> TokenPair refreshToken(tokenRefresh)

Authenticate the user and return a token pair

### Example

```typescript
import {
    AuthApi,
    Configuration,
    TokenRefresh
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let tokenRefresh: TokenRefresh; //

const { status, data } = await apiInstance.refreshToken(
    tokenRefresh
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **tokenRefresh** | **TokenRefresh**|  | |


### Return type

**TokenPair**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **verifyToken**
> { [key: string]: any; } verifyToken(tokenVerify)

Verify an existent authentication token

### Example

```typescript
import {
    AuthApi,
    Configuration,
    TokenVerify
} from './api';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let tokenVerify: TokenVerify; //

const { status, data } = await apiInstance.verifyToken(
    tokenVerify
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **tokenVerify** | **TokenVerify**|  | |


### Return type

**{ [key: string]: any; }**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

