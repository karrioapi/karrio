from attr import s
from typing import Optional


@s(auto_attribs=True)
class AuthResponseType:
    accessToken: Optional[str] = None
    expDate: Optional[int] = None
    refreshToken: Optional[str] = None
    navigation: Optional[int] = None
