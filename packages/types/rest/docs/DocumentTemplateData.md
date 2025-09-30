# DocumentTemplateData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **string** | The template name | [default to undefined]
**slug** | **string** | The template slug | [default to undefined]
**template** | **string** | The template content | [default to undefined]
**active** | **boolean** | disable template flag. | [optional] [default to true]
**description** | **string** | The template description | [optional] [default to undefined]
**metadata** | **{ [key: string]: any; }** | The template metadata | [optional] [default to undefined]
**_options** | **{ [key: string]: any; }** | The template rendering options | [optional] [default to undefined]
**related_object** | **string** | The template related object | [optional] [default to RelatedObjectEnum_Other]

## Example

```typescript
import { DocumentTemplateData } from './api';

const instance: DocumentTemplateData = {
    name,
    slug,
    template,
    active,
    description,
    metadata,
    _options,
    related_object,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
