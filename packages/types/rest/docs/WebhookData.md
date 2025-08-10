# WebhookData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **string** | The URL of the webhook endpoint. | [default to undefined]
**description** | **string** | An optional description of what the webhook is used for. | [optional] [default to undefined]
**enabled_events** | **Array&lt;string&gt;** | The list of events to enable for this endpoint. | [default to undefined]
**disabled** | **boolean** | Indicates that the webhook is disabled | [optional] [default to undefined]

## Example

```typescript
import { WebhookData } from './api';

const instance: WebhookData = {
    url,
    description,
    enabled_events,
    disabled,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
