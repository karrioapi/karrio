# DocumentData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**template_id** | **string** | The template name. **Required if template is not provided.** | [optional] [default to undefined]
**template** | **string** | The template content. **Required if template_id is not provided.** | [optional] [default to undefined]
**doc_format** | **string** | The format of the document | [optional] [default to undefined]
**doc_name** | **string** | The file name | [optional] [default to undefined]
**data** | **{ [key: string]: any; }** | The template data | [optional] [default to undefined]
**_options** | **{ [key: string]: any; }** | The template rendering options | [optional] [default to undefined]

## Example

```typescript
import { DocumentData } from './api';

const instance: DocumentData = {
    template_id,
    template,
    doc_format,
    doc_name,
    data,
    _options,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
