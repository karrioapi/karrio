from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class LabelDetail:
    serviceLevel: Optional[str] = None
    outboundSortCode: Optional[int] = None
    sortingSetupVersion: Optional[int] = None
    inboundSortCode: Optional[str] = None
    serviceEndorsement: Optional[int] = None
    intendedReceivingFacility: Optional[str] = None
    mailBanner: Optional[str] = None
    customsDetailsProvided: Optional[bool] = None


@s(auto_attribs=True)
class Label:
    createdOn: Optional[str] = None
    packageId: Optional[str] = None
    dhlPackageId: Optional[str] = None
    trackingId: Optional[str] = None
    labelData: Optional[str] = None
    encodeType: Optional[str] = None
    format: Optional[str] = None
    link: Optional[str] = None
    labelDetail: Optional[LabelDetail] = JStruct[LabelDetail]


@s(auto_attribs=True)
class CreateLabelResponse:
    timestamp: Optional[str] = None
    pickup: Optional[int] = None
    distributionCenter: Optional[str] = None
    orderedProductId: Optional[str] = None
    labels: List[Label] = JList[Label]
