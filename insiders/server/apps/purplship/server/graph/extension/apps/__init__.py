import graphene
import graphene_django.filter as django_filter

import purplship.server.graph.utils as utils
import purplship.server.graph.extension.apps.mutations as mutations
import purplship.server.graph.extension.apps.types as types
import purplship.server.apps.models as models


class Query:
    app = graphene.Field(types.AppType, id=graphene.String(required=True))
    apps = django_filter.DjangoFilterConnectionField(
        types.AppType,
        required=True,
        filterset_class=types.AppFilter,
        default_value=[],
    )
    installations = django_filter.DjangoFilterConnectionField(
        types.AppInstallationType,
        required=True,
        filterset_class=types.AppInstallationFilter,
        default_value=[],
    )

    @utils.login_required
    def resolve_app(self, info, **kwargs):
        return models.App.access_by(info.context).filter(**kwargs).first()

    @utils.login_required
    def resolve_apps(self, info, **kwargs):
        return models.App.access_by(info.context)

    @utils.login_required
    def resolve_installations(self, info, **kwargs):
        return models.AppInstallation.access_by(info.context)


class Mutation:
    create_app = mutations.CreateApp.Field()
    update_app = mutations.UpdateApp.Field()
    delete_app = mutations.DeleteApp.Field()

    install_app = mutations.InstallApp.Field()
    uninstall_app = mutations.UninstallApp.Field()
