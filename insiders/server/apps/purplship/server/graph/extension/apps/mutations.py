import graphene
from graphene.types import generic
from graphene_django.types import ErrorType

import purplship.server.graph.utils as utils
import purplship.server.apps.models as models
import purplship.server.apps.serializers as serializers
import purplship.server.graph.extension.apps.types as types


class CreateApp(utils.ClientMutation):
    app = graphene.Field(types.AppType)

    class Input:
        display_name = graphene.String(required=True)
        developer_name = graphene.String(required=True)
        features = graphene.List(graphene.String)
        launch_url = graphene.String(required=True)
        is_embedded = graphene.Boolean(required=True)
        metadata = generic.GenericScalar()

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(cls, root, info, **data):
        serializer = serializers.AppModelSerializer(
            data=data,
            context=info.context,
        )

        if not serializer.is_valid():
            return cls(errors=ErrorType.from_errors(serializer.errors))

        return cls(app=serializer.save())


class UpdateApp(utils.ClientMutation):
    app = graphene.Field(types.AppType)

    class Input:
        id = graphene.String(required=True)
        display_name = graphene.String(required=True)
        developer_name = graphene.String(required=True)
        launch_url = graphene.String(required=True)
        is_embedded = graphene.Boolean(required=True)
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
        app = models.App.access_by(info.context).get(id=app_id)

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
    app = graphene.Field(types.AppType)

    class Input:
        app_id = graphene.String(required=True)

    @classmethod
    @utils.login_required
    def mutate_and_get_payload(cls, root, info, app_id, **inputs):
        app = models.App.access_by(info.context).get(id=app_id)

        app.installations.filter(org=info.context.org).delete()

        return cls(app=models.App.access_by(info.context).get(id=app_id))
