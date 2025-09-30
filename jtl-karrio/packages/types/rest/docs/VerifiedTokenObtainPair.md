# VerifiedTokenObtainPair


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**refresh** | **string** |  | [default to undefined]
**access** | **string** |  | [readonly] [default to undefined]
**otp_token** | **string** | The OTP (One Time Password) token received by the user from the         configured Two Factor Authentication method.          | [default to undefined]

## Example

```typescript
import { VerifiedTokenObtainPair } from './api';

const instance: VerifiedTokenObtainPair = {
    refresh,
    access,
    otp_token,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
