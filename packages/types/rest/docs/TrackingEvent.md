# TrackingEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**date** | **string** | The tracking event\&#39;s date. Format: &#x60;YYYY-MM-DD&#x60; | [optional] [default to undefined]
**time** | **string** | The tracking event\&#39;s time. Format: &#x60;HH:MM AM/PM&#x60; | [optional] [default to undefined]
**timestamp** | **string** | The tracking event\&#39;s timestamp. Format: &#x60;YYYY-MM-DDTHH:MM:SS.sssZ&#x60; (ISO 8601) | [optional] [default to undefined]
**status** | **string** | The normalized status of this specific event | [optional] [default to undefined]
**code** | **string** | The tracking event\&#39;s code | [optional] [default to undefined]
**reason** | **string** | The normalized incident reason (for exception events only) | [optional] [default to undefined]
**description** | **string** | The tracking event\&#39;s description | [optional] [default to undefined]
**location** | **string** | The tracking event\&#39;s location | [optional] [default to undefined]
**latitude** | **number** | The tracking event\&#39;s latitude. | [optional] [default to undefined]
**longitude** | **number** | The tracking event\&#39;s longitude. | [optional] [default to undefined]

## Example

```typescript
import { TrackingEvent } from './api';

const instance: TrackingEvent = {
    date,
    time,
    timestamp,
    status,
    code,
    reason,
    description,
    location,
    latitude,
    longitude,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
