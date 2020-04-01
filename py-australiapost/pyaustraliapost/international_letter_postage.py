"""Australia Post International letter postage Datatype definition module."""

import attr
from typing import List, Union, Optional
from jstruct import JList, JStruct


@attr.s(auto_attribs=True)
class ServiceRequest:
    country_code: str
    weight: Optional[float] = None


@attr.s(auto_attribs=True)
class Option:
    code: Optional[str] = None
    name: Optional[str] = None


@attr.s(auto_attribs=True)
class Options:
    option: List[Option] = JList[Option]


@attr.s(auto_attribs=True)
class Service:
    code: Optional[str] = None
    name: Optional[str] = None
    price: Optional[Union[float, str]] = None
    max_extra_cover: Optional[int] = None
    options: Options = JStruct[Options]


@attr.s(auto_attribs=True)
class Services:
    service: List[Service] = JList[Service]


@attr.s(auto_attribs=True)
class ServiceResponse:
    services: Services = JStruct[Services]


@attr.s(auto_attribs=True)
class PostageRequest:
    country_code: str
    service_code: str
    weight: Optional[float] = None
    option_code: Optional[str] = None
    suboption_code: Optional[str] = None
    extra_cover: Optional[str] = None


@attr.s(auto_attribs=True)
class Cost:
    cost: Optional[str] = None
    item: Optional[str] = None


@attr.s(auto_attribs=True)
class Costs:
    cost: List[Cost] = JList[Cost]


@attr.s(auto_attribs=True)
class PostageResult:
    service: Optional[str] = None
    total_cost: Optional[str] = None
    costs: Costs = JStruct[Costs]


@attr.s(auto_attribs=True)
class PostageResponse:
    postage_result: PostageResult = JStruct[PostageResult]
