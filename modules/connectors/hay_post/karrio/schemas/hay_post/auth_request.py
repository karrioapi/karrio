from attr import s
from typing import Optional


@s(auto_attribs=True)
class AuthRequestType:
    username: Optional[str] = None
    password: Optional[str] = None
    customerType: Optional[int] = None
    deviceId: Optional[str] = None
    fcmToken: Optional[str] = None
