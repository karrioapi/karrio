import typing
import datetime
import strawberry
from strawberry.types import Info
from django.forms.models import model_to_dict

from karrio.server.serializers import SerializerDecorator, Context
from karrio.server.user.serializers import TokenSerializer
import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.base as base
import karrio.server.graph.schemas.orgs.inputs as inputs
import karrio.server.orgs.models as models
import karrio.server.orgs.utils as orgs


@strawberry.type
class OrganizationUserType:
    email: str
    is_admin: bool
    is_owner: bool
    is_staff: typing.Optional[bool] = None
    full_name: typing.Optional[str] = None
    last_login: typing.Optional[datetime.datetime] = None
    date_joined: typing.Optional[datetime.datetime] = None


@strawberry.type
class OrganizationInvitationType:
    object_type: str
    id: str
    guid: str
    invitee_identifier: str
    created: datetime.datetime
    modified: datetime.datetime
    invited_by: base.types.UserType
    invitee: typing.Optional[base.types.UserType] = None

    @strawberry.field
    def organization_name(self: models.Organization) -> str:
        return self.organization.name

    @staticmethod
    @utils.authentication_required
    def resolve(
        info,
        id: typing.Optional[str] = strawberry.UNSET,
        guid: typing.Optional[str] = strawberry.UNSET,
    ) -> typing.Optional["OrganizationType"]:
        _filter = dict(
            id=(id if id is not strawberry.UNSET else None),
            guid=(guid if guid is not strawberry.UNSET else None),
        )

        return (
            models.OrganizationInvitation
            .access_by(info.context.request)
            .filter(**_filter)
            .first()
        )


@strawberry.type
class OrganizationMemberType:
    email: str
    is_admin: bool
    roles: typing.List[orgs.OrganizationUserRole]
    is_owner: typing.Optional[bool] = None
    full_name: typing.Optional[str] = None
    last_login: typing.Optional[datetime.datetime] = None
    invitation: typing.Optional[OrganizationInvitationType] = None


@strawberry.type
class OrganizationType:
    id: str
    name: str
    slug: str
    is_active: bool
    created: datetime.datetime
    modified: datetime.datetime
    organization_invites: typing.List[OrganizationInvitationType]

    @strawberry.field
    def current_user(self: models.Organization, info: Info) -> OrganizationMemberType:
        user = info.context.request.user
        return OrganizationUserType( # type: ignore
            **{
                k: v
                for k, v in model_to_dict(user).items()
                if k in OrganizationUserType.__annotations__.keys()
            },
            is_admin=self.organization_users.get(user=user).is_admin,
            is_owner=self.is_owner(user),
        )

    @strawberry.field
    def members(self: models.Organization) -> typing.List[OrganizationMemberType]:
        users = [
            OrganizationMemberType( # type: ignore
                email=user.email,
                full_name=user.full_name,
                last_login=user.last_login,
                is_owner=self.is_owner(user),
                roles=self.organization_users.get(user=user).roles,
                is_admin=self.organization_users.get(user=user).is_admin,
            )
            for user in self.users.filter(is_active=True)
        ]
        invites = [
            OrganizationMemberType( # type: ignore
                email=getattr(invite.invitee, "email", invite.invitee_identifier),
                full_name=getattr(invite.invitee, "full_name", ""),
                is_admin=False,
                is_owner=False,
                invitation=invite,
                roles=[inputs.OrganizationUserRole.member],
            )
            for invite in self.organization_invites.all()
        ]

        return users + invites

    @strawberry.field
    def token(self: models.Organization, info: Info) -> str:
        context = Context(
            org=self,
            user=info.context.request.user,
            test_mode=info.context.request.test_mode,
        )

        return (
            SerializerDecorator[TokenSerializer](
                data=dict(user=info.context.request.user),
                context=context,
            )
            .save()
            .instance
        )

    @staticmethod
    @utils.authentication_required
    def resolve(info, id: str) -> typing.Optional["OrganizationType"]:
        return models.Organization.access_by(info.context.request).filter(id=id).first()

    @staticmethod
    @utils.authentication_required
    def resolve_list(info) -> typing.List["OrganizationType"]:
        return models.Organization.access_by(info.context.request).filter(
            users__id=info.context.request.user.id, is_active=True
        )


