import typing
import datetime
import strawberry

import karrio.server.graph.utils as utils
import karrio.server.tenants.models as models


@strawberry.type
class DomainType:
    object_type: str
    id: str
    domain: str
    is_primary: bool


@strawberry.type
class TenantType:
    object_type: str
    id: str
    name: str
    schema_name: str
    feature_flags: typing.Optional[utils.JSON]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]

    @strawberry.field
    def domains(self: models.Client) -> typing.List[DomainType]:
        return self.domains.all()

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["TenantType"]:
        return models.Client.objects.filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(info) -> typing.List["TenantType"]:
        return models.Client.objects.all()
