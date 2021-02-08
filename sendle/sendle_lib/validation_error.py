import attr
from typing import Union


@attr.s(auto_attribs=True)
class ValidationError:
    messages: Union[dict, list] = None
    error: str = None
    error_description: str = None
