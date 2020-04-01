"""Australia Post Domestic letter postage Datatype definition module."""

import attr
from typing import List, Union, Optional
from jstruct import JList, JStruct


@attr.s(auto_attribs=True)
class ServiceRequest:
    length: Optional[float]
    width: Optional[float]
    thickness: Optional[float]
    weight: Optional[float]


@attr.s(auto_attribs=True)
class SubOption:
    code: Optional[str] = None
    name: Optional[str] = None
    max_extra_cover: Optional[int] = None


@attr.s(auto_attribs=True)
class SubOptions:
    option: List[SubOption] = JList[SubOption]


@attr.s(auto_attribs=True)
class Option:
    code: Optional[str] = None
    name: Optional[str] = None
    suboptions: SubOptions = JStruct[SubOptions]


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
