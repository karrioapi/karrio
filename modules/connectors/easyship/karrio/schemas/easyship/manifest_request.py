import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ManifestRequestType:
    courier_account_id: typing.Optional[str] = None
    shipment_ids: typing.Optional[typing.List[str]] = None
