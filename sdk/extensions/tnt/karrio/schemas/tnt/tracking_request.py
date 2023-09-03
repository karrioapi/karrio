from attr import s
from typing import Optional, List
from jstruct import JStruct


@s(auto_attribs=True)
class CompleteType:
    pass


@s(auto_attribs=True)
class PodType:
    format: Optional[str] = None


@s(auto_attribs=True)
class LevelOfDetailType:
    complete: Optional[CompleteType] = JStruct[CompleteType]
    pod: Optional[PodType] = JStruct[PodType]


@s(auto_attribs=True)
class SearchCriteriaType:
    customerReference: List[str] = []
    marketType: Optional[str] = None
    originCountry: Optional[str] = None


@s(auto_attribs=True)
class TrackRequestType:
    locale: Optional[str] = None
    version: Optional[str] = None
    searchCriteria: Optional[SearchCriteriaType] = JStruct[SearchCriteriaType]
    levelOfDetail: Optional[LevelOfDetailType] = JStruct[LevelOfDetailType]


@s(auto_attribs=True)
class TrackingRequestType:
    TrackRequest: Optional[TrackRequestType] = JStruct[TrackRequestType]
