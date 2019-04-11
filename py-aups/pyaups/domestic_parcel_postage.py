"""Australia Post Domestic parcel postage Datatype definition module."""

import attr
from typing import List, Union
from jstruct import JList, JStruct


@attr.s(auto_attribs=True)
class ServiceRequest:
    from_postcode: str
    to_postcode: str
    length: float
    width: float
    height: float
    weight: float


@attr.s(auto_attribs=True)
class SubOption:
    code: str = None
    name: str = None
    max_extra_cover: int = None


@attr.s(auto_attribs=True)
class SubOptions:
    option: List[SubOption] = JList[SubOption]


@attr.s(auto_attribs=True)
class Option:
    code: str = None
    name: str = None
    suboptions: SubOptions = JStruct[SubOptions]


@attr.s(auto_attribs=True)
class Options:
    option: List[Option] = JList[Option]


@attr.s(auto_attribs=True)
class Service:
    code: str = None
    name: str = None
    price: Union[float, str] = None
    max_extra_cover: int = None
    options: Options = JStruct[Options]


@attr.s(auto_attribs=True)
class Services:
    service: List[Service] = JList[Service]


@attr.s(auto_attribs=True)
class ServiceResponse:
    services: Services = JStruct[Services]


@attr.s(auto_attribs=True)
class PostageRequest:
    from_postcode: str
    to_postcode: str
    length: float
    width: float
    height: float
    weight: float
    service_code: str
    option_code: str = None
    suboption_code: str = None
    extra_cover: str = None


@attr.s(auto_attribs=True)
class Cost:
    cost: str = None
    item: str = None


@attr.s(auto_attribs=True)
class PostageResult:
    service: str = None
    total_cost: str = None
    costs: Cost = JStruct[Cost]


@attr.s(auto_attribs=True)
class PostageResponse:
    postage_result: PostageResult = JStruct[PostageResult]
