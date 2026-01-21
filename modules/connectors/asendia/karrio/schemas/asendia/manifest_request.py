import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ManifestRequestType:
    parcelIds: typing.Optional[typing.List[str]] = None
