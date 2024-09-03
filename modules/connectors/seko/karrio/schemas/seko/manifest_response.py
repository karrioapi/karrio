from attr import s
from typing import Optional, List, Any
from jstruct import JList


@s(auto_attribs=True)
class OutboundManifestType:
    ManifestNumber: Optional[str] = None
    ManifestedConnotes: List[str] = []
    ManifestContent: Optional[str] = None


@s(auto_attribs=True)
class ManifestResponseType:
    OutboundManifest: List[OutboundManifestType] = JList[OutboundManifestType]
    InboundManifest: List[Any] = []
    Error: List[Any] = []
    StatusCode: Optional[int] = None
    UnManifestedConnotes: List[Any] = []
