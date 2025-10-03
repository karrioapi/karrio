# Webhook


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** | A unique identifier | [optional] [default to undefined]
**url** | **string** | The URL of the webhook endpoint. | [default to undefined]
**description** | **string** | An optional description of what the webhook is used for. | [optional] [default to undefined]
**enabled_events** | **Array&lt;string&gt;** | The list of events to enable for this endpoint. | [default to undefined]
**disabled** | **boolean** | Indicates that the webhook is disabled | [optional] [default to undefined]
**object_type** | **string** | Specifies the object type | [optional] [default to 'webhook']
**last_event_at** | **string** | The datetime of the last event sent. | [optional] [default to undefined]
**secret** | **string** | Header signature secret | [default to undefined]
**test_mode** | **boolean** | Specified whether it was created with a carrier in test mode | [default to undefined]

## Example

```typescript
import { Webhook } from './api';

const instance: Webhook = {
    id,
    url,
    description,
    enabled_events,
    disabled,
    object_type,
    last_event_at,
    secret,
    test_mode,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
