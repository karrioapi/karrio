import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class CancelRequestType:
    listNosRecepisses: typing.Optional[typing.List[str]] = None
    listNosSuivis: typing.Optional[typing.List[str]] = None
    listReferences: typing.Optional[typing.List[str]] = None
