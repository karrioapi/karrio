# DocumentTemplate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** | A unique identifier | [optional] [default to undefined]
**name** | **string** | The template name | [default to undefined]
**slug** | **string** | The template slug | [default to undefined]
**template** | **string** | The template content | [default to undefined]
**active** | **boolean** | disable template flag. | [optional] [default to true]
**description** | **string** | The template description | [optional] [default to undefined]
**metadata** | **{ [key: string]: any; }** | The template metadata | [optional] [default to undefined]
**_options** | **{ [key: string]: any; }** | The template rendering options | [optional] [default to undefined]
**related_object** | **string** | The template related object | [optional] [default to RelatedObjectEnum_Other]
**object_type** | **string** | Specifies the object type | [optional] [default to 'document-template']
**preview_url** | **string** | The template preview URL | [optional] [default to undefined]

## Example

```typescript
import { DocumentTemplate } from './api';

const instance: DocumentTemplate = {
    id,
    name,
    slug,
    template,
    active,
    description,
    metadata,
    _options,
    related_object,
    object_type,
    preview_url,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
