import typing
import strawberry
from strawberry.types import Info
from django.db import models as django, transaction

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.apps.types as types
import karrio.server.graph.schemas.apps.inputs as inputs
import karrio.server.apps.serializers as serializers
import karrio.server.apps.models as models


@strawberry.type
class CreateAppMutation(utils.BaseMutation):
    app: typing.Optional[types.AppType] = None
    client_secret: typing.Optional[str] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["APPS_MANAGEMENT", "manage_apps"])
    @transaction.atomic
    def mutate(
        info: Info, **input: inputs.CreateAppMutationInput
    ) -> "CreateAppMutation":
        registration = models.Application(
            user=info.context.request.user,
            name=input["display_name"],
            redirect_uris=input["redirect_uris"],
            algorithm=models.Application.RS256_ALGORITHM,
            client_type=models.Application.CLIENT_PUBLIC,
            authorization_grant_type=models.Application.GRANT_AUTHORIZATION_CODE,
        )
        client_secret = registration.client_secret
        registration.save()

        serializer = serializers.AppModelSerializer(
            data={**input, "registration": registration.pk},
            context=info.context,
        )
        serializer.is_valid(raise_exception=True)

        return CreateAppMutation(  # type:ignore
            app=serializer.save(),
            client_secret=client_secret
        )


@strawberry.type
class UpdateAppMutation(utils.BaseMutation):
    app: typing.Optional[types.AppType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["APPS_MANAGEMENT", "manage_apps"])
    @transaction.atomic
    def mutate(
        info: Info, **input: inputs.UpdateAppMutationInput
    ) -> "UpdateAppMutation":
        instance = models.App.access_by(info.context.request).get(id=id)

        serializer = serializers.AppModelSerializer(
            instance,
            data=input,
            partial=True,
            context=info.context,
        )
        serializer.is_valid(raise_exception=True)

        instance.registration.name = input.get("display_name") or instance.display_name
        instance.registration.redirect_uris = (
            input.get("redirect_uris") or instance.registration.redirect_uris
        )
        instance.registration.save()

        return UpdateAppMutation(app=serializer.save())  # type:ignore


@strawberry.type
class InstallAppMutation(utils.BaseMutation):
    installation: typing.Optional[types.AppInstallationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["APPS_MANAGEMENT", "manage_apps"])
    def mutate(
        info: Info, **input: inputs.InstallAppMutationInput
    ) -> "InstallAppMutation":
        app = models.App.objects.get(
            django.Q(id=input["app_id"], link__org=info.context.request.org)
            | django.Q(id=input["app_id"], is_public=True, is_published=True)
        )

        if app.installations.filter(org=info.context.request.org).exists():
            return InstallAppMutation(
                installation=app.installations.filter(org=info.context.request.org).first()
            )

        serializer = serializers.AppInstallationModelSerializer(
            data={"app": app, **input},
            context=info.context,
        )
        serializer.is_valid(raise_exception=True)

        return InstallAppMutation(installation=serializer.save())  # type:ignore


@strawberry.type
class UninstallAppMutation(utils.BaseMutation):
    app: typing.Optional[types.AppType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["APPS_MANAGEMENT", "manage_apps"])
    def mutate(
        info: Info, **input: inputs.UninstallAppMutationInput
    ) -> "UninstallAppMutation":
        app = models.App.objects.get(id=input["app_id"])

        app.installations.filter(org=info.context.request.org).delete()

        return UninstallAppMutation(  # type:ignore
            app=models.App.access_by(info.context.request).get(id=input["app_id"])
        )
