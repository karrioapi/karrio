import typing
import datetime
import strawberry
from django.urls import reverse

import karrio.server.graph.utils as utils
import karrio.server.tenants.models as models
import karrio.server.tenants.filters as filters
import karrio.server.admin.schemas.tenants.inputs as inputs


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
    app_domains: typing.Optional[typing.List[str]]
    created_at: typing.Optional[datetime.datetime]
    updated_at: typing.Optional[datetime.datetime]

    @strawberry.field
    def domains(self: models.Client, info) -> typing.List[DomainType]:
        return self.domains.all()

    @strawberry.field
    def api_domains(self: models.Client, info) -> typing.Optional[typing.List[str]]:
        _uri = info.context.request.build_absolute_uri("/")
        uri = _uri[:-1] if _uri[-1] == "/" else _uri
        host = info.context.request.get_host()
        domain = host.split(":")[0]

        return [
            (
                uri.replace(domain, d.domain)
                if domain in d.domain
                else uri.replace(host, d.domain)
            )
            for d in self.domains.all().order_by("is_primary")
        ]

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["TenantType"]:
        return models.Client.objects.filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(
        info,
        filter: typing.Optional[inputs.TenantFilter] = strawberry.UNSET,
    ) -> utils.Connection["TenantType"]:
        _filter = filter if not utils.is_unset(filter) else inputs.TenantFilter()
        queryset = filters.TenantFilter(
            _filter.to_dict(), models.Client.objects.all()
        ).qs

        return utils.paginated_connection(queryset, **_filter.pagination())
