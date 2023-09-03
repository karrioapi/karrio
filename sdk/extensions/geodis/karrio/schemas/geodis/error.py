from attr import s
from typing import Optional


@s(auto_attribs=True)
class Error:
    ok: Optional[bool] = None
    codeErreur: Optional[str] = None
    texteErreur: Optional[str] = None
