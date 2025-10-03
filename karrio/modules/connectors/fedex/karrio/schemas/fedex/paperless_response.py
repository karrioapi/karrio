import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class MetaType:
    documentType: typing.Optional[str] = None
    docId: typing.Optional[str] = None
    folderId: typing.Optional[typing.List[str]] = None


@attr.s(auto_attribs=True)
class OutputType:
    meta: typing.Optional[MetaType] = jstruct.JStruct[MetaType]


@attr.s(auto_attribs=True)
class PaperlessResponseType:
    output: typing.Optional[OutputType] = jstruct.JStruct[OutputType]
    customerTransactionId: typing.Optional[str] = None
