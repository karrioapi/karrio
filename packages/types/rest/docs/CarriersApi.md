# CarriersApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**getDetails**](#getdetails) | **GET** /v1/carriers/{carrier_name} | Get carrier details|
|[**getOptions**](#getoptions) | **GET** /v1/carriers/{carrier_name}/options | Get carrier options|
|[**getServices**](#getservices) | **GET** /v1/carriers/{carrier_name}/services | Get carrier services|
|[**list**](#list) | **GET** /v1/carriers | List all carriers|

# **getDetails**
> CarrierDetails getDetails()

Retrieve a carrier\'s details

### Example

```typescript
import {
    CarriersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CarriersApi(configuration);

let carrierName: string; //The unique carrier slug. <br/>Values: `aramex`, `asendia`, `asendia_us`, `australiapost`, `boxknight`, `bpost`, `canadapost`, `canpar`, `chronopost`, `colissimo`, `dhl_express`, `dhl_parcel_de`, `dhl_poland`, `dhl_universal`, `dicom`, `dpd`, `dpd_meta`, `dtdc`, `easypost`, `easyship`, `eshipper`, `fedex`, `freightcom`, `generic`, `geodis`, `gls`, `hay_post`, `hermes`, `landmark`, `laposte`, `locate2u`, `mydhl`, `nationex`, `parcelone`, `postat`, `purolator`, `roadie`, `royalmail`, `sapient`, `seko`, `sendle`, `shipengine`, `smartkargo`, `spring`, `teleship`, `tge`, `tnt`, `ups`, `usps`, `usps_international`, `veho`, `zoom2u` (default to undefined)

const { status, data } = await apiInstance.getDetails(
    carrierName
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **carrierName** | [**string**] | The unique carrier slug. &lt;br/&gt;Values: &#x60;aramex&#x60;, &#x60;asendia&#x60;, &#x60;asendia_us&#x60;, &#x60;australiapost&#x60;, &#x60;boxknight&#x60;, &#x60;bpost&#x60;, &#x60;canadapost&#x60;, &#x60;canpar&#x60;, &#x60;chronopost&#x60;, &#x60;colissimo&#x60;, &#x60;dhl_express&#x60;, &#x60;dhl_parcel_de&#x60;, &#x60;dhl_poland&#x60;, &#x60;dhl_universal&#x60;, &#x60;dicom&#x60;, &#x60;dpd&#x60;, &#x60;dpd_meta&#x60;, &#x60;dtdc&#x60;, &#x60;easypost&#x60;, &#x60;easyship&#x60;, &#x60;eshipper&#x60;, &#x60;fedex&#x60;, &#x60;freightcom&#x60;, &#x60;generic&#x60;, &#x60;geodis&#x60;, &#x60;gls&#x60;, &#x60;hay_post&#x60;, &#x60;hermes&#x60;, &#x60;landmark&#x60;, &#x60;laposte&#x60;, &#x60;locate2u&#x60;, &#x60;mydhl&#x60;, &#x60;nationex&#x60;, &#x60;parcelone&#x60;, &#x60;postat&#x60;, &#x60;purolator&#x60;, &#x60;roadie&#x60;, &#x60;royalmail&#x60;, &#x60;sapient&#x60;, &#x60;seko&#x60;, &#x60;sendle&#x60;, &#x60;shipengine&#x60;, &#x60;smartkargo&#x60;, &#x60;spring&#x60;, &#x60;teleship&#x60;, &#x60;tge&#x60;, &#x60;tnt&#x60;, &#x60;ups&#x60;, &#x60;usps&#x60;, &#x60;usps_international&#x60;, &#x60;veho&#x60;, &#x60;zoom2u&#x60; | defaults to undefined|


### Return type

**CarrierDetails**

### Authorization

No authorization required

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

# **getOptions**
> { [key: string]: any; } getOptions()

Retrieve a carrier\'s options

### Example

```typescript
import {
    CarriersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CarriersApi(configuration);

let carrierName: string; //The unique carrier slug. <br/>Values: `aramex`, `asendia`, `asendia_us`, `australiapost`, `boxknight`, `bpost`, `canadapost`, `canpar`, `chronopost`, `colissimo`, `dhl_express`, `dhl_parcel_de`, `dhl_poland`, `dhl_universal`, `dicom`, `dpd`, `dpd_meta`, `dtdc`, `easypost`, `easyship`, `eshipper`, `fedex`, `freightcom`, `generic`, `geodis`, `gls`, `hay_post`, `hermes`, `landmark`, `laposte`, `locate2u`, `mydhl`, `nationex`, `parcelone`, `postat`, `purolator`, `roadie`, `royalmail`, `sapient`, `seko`, `sendle`, `shipengine`, `smartkargo`, `spring`, `teleship`, `tge`, `tnt`, `ups`, `usps`, `usps_international`, `veho`, `zoom2u` (default to undefined)

const { status, data } = await apiInstance.getOptions(
    carrierName
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **carrierName** | [**string**] | The unique carrier slug. &lt;br/&gt;Values: &#x60;aramex&#x60;, &#x60;asendia&#x60;, &#x60;asendia_us&#x60;, &#x60;australiapost&#x60;, &#x60;boxknight&#x60;, &#x60;bpost&#x60;, &#x60;canadapost&#x60;, &#x60;canpar&#x60;, &#x60;chronopost&#x60;, &#x60;colissimo&#x60;, &#x60;dhl_express&#x60;, &#x60;dhl_parcel_de&#x60;, &#x60;dhl_poland&#x60;, &#x60;dhl_universal&#x60;, &#x60;dicom&#x60;, &#x60;dpd&#x60;, &#x60;dpd_meta&#x60;, &#x60;dtdc&#x60;, &#x60;easypost&#x60;, &#x60;easyship&#x60;, &#x60;eshipper&#x60;, &#x60;fedex&#x60;, &#x60;freightcom&#x60;, &#x60;generic&#x60;, &#x60;geodis&#x60;, &#x60;gls&#x60;, &#x60;hay_post&#x60;, &#x60;hermes&#x60;, &#x60;landmark&#x60;, &#x60;laposte&#x60;, &#x60;locate2u&#x60;, &#x60;mydhl&#x60;, &#x60;nationex&#x60;, &#x60;parcelone&#x60;, &#x60;postat&#x60;, &#x60;purolator&#x60;, &#x60;roadie&#x60;, &#x60;royalmail&#x60;, &#x60;sapient&#x60;, &#x60;seko&#x60;, &#x60;sendle&#x60;, &#x60;shipengine&#x60;, &#x60;smartkargo&#x60;, &#x60;spring&#x60;, &#x60;teleship&#x60;, &#x60;tge&#x60;, &#x60;tnt&#x60;, &#x60;ups&#x60;, &#x60;usps&#x60;, &#x60;usps_international&#x60;, &#x60;veho&#x60;, &#x60;zoom2u&#x60; | defaults to undefined|


### Return type

**{ [key: string]: any; }**

### Authorization

No authorization required

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

# **getServices**
> { [key: string]: any; } getServices()

Retrieve a carrier\'s services

### Example

```typescript
import {
    CarriersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CarriersApi(configuration);

let carrierName: string; //The unique carrier slug. <br/>Values: `aramex`, `asendia`, `asendia_us`, `australiapost`, `boxknight`, `bpost`, `canadapost`, `canpar`, `chronopost`, `colissimo`, `dhl_express`, `dhl_parcel_de`, `dhl_poland`, `dhl_universal`, `dicom`, `dpd`, `dpd_meta`, `dtdc`, `easypost`, `easyship`, `eshipper`, `fedex`, `freightcom`, `generic`, `geodis`, `gls`, `hay_post`, `hermes`, `landmark`, `laposte`, `locate2u`, `mydhl`, `nationex`, `parcelone`, `postat`, `purolator`, `roadie`, `royalmail`, `sapient`, `seko`, `sendle`, `shipengine`, `smartkargo`, `spring`, `teleship`, `tge`, `tnt`, `ups`, `usps`, `usps_international`, `veho`, `zoom2u` (default to undefined)

const { status, data } = await apiInstance.getServices(
    carrierName
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **carrierName** | [**string**] | The unique carrier slug. &lt;br/&gt;Values: &#x60;aramex&#x60;, &#x60;asendia&#x60;, &#x60;asendia_us&#x60;, &#x60;australiapost&#x60;, &#x60;boxknight&#x60;, &#x60;bpost&#x60;, &#x60;canadapost&#x60;, &#x60;canpar&#x60;, &#x60;chronopost&#x60;, &#x60;colissimo&#x60;, &#x60;dhl_express&#x60;, &#x60;dhl_parcel_de&#x60;, &#x60;dhl_poland&#x60;, &#x60;dhl_universal&#x60;, &#x60;dicom&#x60;, &#x60;dpd&#x60;, &#x60;dpd_meta&#x60;, &#x60;dtdc&#x60;, &#x60;easypost&#x60;, &#x60;easyship&#x60;, &#x60;eshipper&#x60;, &#x60;fedex&#x60;, &#x60;freightcom&#x60;, &#x60;generic&#x60;, &#x60;geodis&#x60;, &#x60;gls&#x60;, &#x60;hay_post&#x60;, &#x60;hermes&#x60;, &#x60;landmark&#x60;, &#x60;laposte&#x60;, &#x60;locate2u&#x60;, &#x60;mydhl&#x60;, &#x60;nationex&#x60;, &#x60;parcelone&#x60;, &#x60;postat&#x60;, &#x60;purolator&#x60;, &#x60;roadie&#x60;, &#x60;royalmail&#x60;, &#x60;sapient&#x60;, &#x60;seko&#x60;, &#x60;sendle&#x60;, &#x60;shipengine&#x60;, &#x60;smartkargo&#x60;, &#x60;spring&#x60;, &#x60;teleship&#x60;, &#x60;tge&#x60;, &#x60;tnt&#x60;, &#x60;ups&#x60;, &#x60;usps&#x60;, &#x60;usps_international&#x60;, &#x60;veho&#x60;, &#x60;zoom2u&#x60; | defaults to undefined|


### Return type

**{ [key: string]: any; }**

### Authorization

No authorization required

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

# **list**
> Array<CarrierDetails> list()

Returns the list of configured carriers

### Example

```typescript
import {
    CarriersApi,
    Configuration
} from './api';

const configuration = new Configuration();
const apiInstance = new CarriersApi(configuration);

const { status, data } = await apiInstance.list();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**Array<CarrierDetails>**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |
|**500** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

