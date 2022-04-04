import graphene
from django.db.models import Q
from graphene.types import generic
from graphene_django.types import ErrorType

import karrio.server.graph.utils as utils
import karrio.server.apps.models as models
import karrio.server.apps.serializers as serializers
import karrio.server.graph.extension.apps.types as types


class CreateApp(utils.ClientMutation):
    app = graphene.Field(types.PrivateAppType)

    class Input:
        display_name = graphene.String(required=True)
        developer_name = graphene.String(required=True)
        features = graphene.List(graphene.String)
        launch_url = graphene.String(required=True)
        is_embedded = graphene.Boolean(required=True)
        redirect_uris = graphene.String(required=True)
        is_public = graphene.Boolean(default_value=False)
        metadata = generic.GenericScalar()

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(cls, root, info, **data):
        registration = models.Application.objects.create(
            user=info.context.user,
            name=data["display_name"],
            redirect_uris=data["redirect_uris"],
            algorithm=models.Application.RS256_ALGORITHM,
            client_type=models.Application.CLIENT_PUBLIC,
            authorization_grant_type=models.Application.GRANT_AUTHORIZATION_CODE,
        )
        serializer = serializers.AppModelSerializer(
            data={**data, "registration": registration.pk},
            context=info.context,
        )

        if not serializer.is_valid():
            return cls(errors=ErrorType.from_errors(serializer.errors))

        return cls(app=serializer.save())


class UpdateApp(utils.ClientMutation):
    app = graphene.Field(types.PrivateAppType)

    class Input:
        id = graphene.String(required=True)
        display_name = graphene.String()
        developer_name = graphene.String()
        features = graphene.List(graphene.String)
        launch_url = graphene.String()
        is_embedded = graphene.Boolean()
        redirect_uris = graphene.String()
        is_public = graphene.Boolean()
        metadata = generic.GenericScalar()

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(cls, root, info, id, **data):
        instance = models.App.access_by(info.context).get(id=id)

        serializer = serializers.AppModelSerializer(
            instance,
            data=data,
            partial=True,
            context=info.context,
        )

        if not serializer.is_valid():
            return cls(errors=ErrorType.from_errors(serializer.errors))

        instance.registration.name = data.get("display_name") or instance.display_name
        instance.registration.redirect_uris = (
            data.get("redirect_uris") or instance.registration.redirect_uris
        )
        instance.registration.save()

        return cls(app=serializer.save())


class DeleteApp(utils.ClientMutation):
    id = graphene.String()

    class Input:
        id = graphene.String(required=True)

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(cls, root, info, id, **kwargs):
        app = models.App.access_by(info.context).get(id=id)

        app.delete(keep_parents=True)

        return cls(id=id)


class InstallApp(utils.ClientMutation):
    installation = graphene.Field(types.AppInstallationType)

    class Input:
        app_id = graphene.String(required=True)
        access_scopes = graphene.List(graphene.String, required=True)
        metadata = generic.GenericScalar()

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(cls, root, info, app_id, **inputs):
        app = models.App.objects.get(
            Q(id=app_id, link__org=info.context.org)
            | Q(id=app_id, is_public=True, is_published=True)
        )

        if app.installations.filter(org=info.context.org).exists():
            return cls(
                installation=app.installations.filter(org=info.context.org).first()
            )

        serializer = serializers.AppInstallationModelSerializer(
            data={"app": app, **inputs},
            context=info.context,
        )

        if not serializer.is_valid():
            return cls(errors=ErrorType.from_errors(serializer.errors))

        return cls(installation=serializer.save())


class UninstallApp(utils.ClientMutation):
    app = graphene.Field(types.PrivateAppType)

    class Input:
        app_id = graphene.String(required=True)

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(cls, root, info, app_id, **inputs):
        app = models.App.objects.get(id=app_id)

        app.installations.filter(org=info.context.org).delete()

        return cls(app=models.App.access_by(info.context).get(id=app_id))
