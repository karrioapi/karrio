import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class AlertType:
    code: typing.Optional[str] = None
    message: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class LocalizationType:
    localeCode: typing.Optional[str] = None
    languageCode: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class OutputType:
    alerts: typing.Optional[typing.List[AlertType]] = jstruct.JList[AlertType]
    localization: typing.Optional[LocalizationType] = jstruct.JStruct[LocalizationType]
    documentType: typing.Optional[str] = None
    documentFormat: typing.Optional[str] = None
    documents: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class TrackingDocumentResponseType:
    transactionId: typing.Optional[str] = None
    output: typing.Optional[OutputType] = jstruct.JStruct[OutputType]
