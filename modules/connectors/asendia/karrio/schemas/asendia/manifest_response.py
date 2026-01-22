import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ManifestResponseType:
    id: typing.Optional[str] = None
    createdAt: typing.Optional[str] = None
    errorMessage: typing.Optional[str] = None
    errorParcelIds: typing.Optional[typing.List[str]] = None
    status: typing.Optional[str] = None
    manifestDocumentLocation: typing.Optional[str] = None
    parcelsLocation: typing.Optional[str] = None
    manifestLocation: typing.Optional[str] = None
