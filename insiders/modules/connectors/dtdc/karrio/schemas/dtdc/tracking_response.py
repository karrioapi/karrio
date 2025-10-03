import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class TrackDetailType:
    strCode: typing.Optional[str] = None
    strAction: typing.Optional[str] = None
    strManifestNo: typing.Optional[str] = None
    strOrigin: typing.Optional[str] = None
    strDestination: typing.Optional[str] = None
    strActionDate: typing.Optional[int] = None
    strActionTime: typing.Optional[int] = None
    sTrRemarks: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackHeaderType:
    strShipmentNo: typing.Optional[str] = None
    strRefNo: typing.Optional[str] = None
    strCNType: typing.Optional[str] = None
    strCNTypeCode: typing.Optional[str] = None
    strCNTypeName: typing.Optional[str] = None
    strCNProduct: typing.Optional[str] = None
    strModeCode: typing.Optional[str] = None
    strMode: typing.Optional[str] = None
    strCNProdCODFOD: typing.Optional[str] = None
    strOrigin: typing.Optional[str] = None
    strOriginRemarks: typing.Optional[str] = None
    strBookedDate: typing.Optional[int] = None
    strBookedTime: typing.Optional[str] = None
    strPieces: typing.Optional[int] = None
    strWeightUnit: typing.Optional[str] = None
    strWeight: typing.Optional[str] = None
    strDestination: typing.Optional[str] = None
    strStatus: typing.Optional[str] = None
    strStatusTransOn: typing.Optional[int] = None
    strStatusTransTime: typing.Optional[int] = None
    strStatusRelCode: typing.Optional[str] = None
    strStatusRelName: typing.Optional[str] = None
    strRemarks: typing.Optional[str] = None
    strNoOfAttempts: typing.Optional[int] = None
    strRtoNumber: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    statusCode: typing.Optional[int] = None
    statusFlag: typing.Optional[bool] = None
    status: typing.Optional[str] = None
    errorDetails: typing.Any = None
    trackHeader: typing.Optional[TrackHeaderType] = jstruct.JStruct[TrackHeaderType]
    trackDetails: typing.Optional[typing.List[TrackDetailType]] = jstruct.JList[TrackDetailType]
