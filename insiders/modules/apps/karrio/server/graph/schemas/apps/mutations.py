import typing
import strawberry
from strawberry.types import Info
from django.db import models as django, transaction
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from oauth2_provider.models import Application

import karrio.server.graph.utils as utils
import karrio.server.graph.schemas.apps.types as types
import karrio.server.graph.schemas.apps.inputs as inputs
import karrio.server.apps.models as models
import karrio.server.graph.schemas.base.inputs as base_inputs
import karrio.server.graph.serializers as graph_serializers
import karrio.server.serializers as serializers


def validate_redirect_uris(redirect_uris_string):
    """Validate that all redirect URIs are valid URLs and use HTTPS in production."""
    url_validator = URLValidator()
    redirect_uris = redirect_uris_string.strip().split('\n')

    for uri in redirect_uris:
        uri = uri.strip()
        if not uri:
            continue

        try:
            url_validator(uri)
        except ValidationError:
            raise ValidationError(f"Invalid redirect URI: {uri}")

        # In production, require HTTPS redirect URIs for security
        from django.conf import settings
        if not settings.DEBUG and not uri.startswith('https://'):
            raise ValidationError(f"Redirect URI must use HTTPS: {uri}")


# OAuth App Mutations
@strawberry.type
class CreateOAuthAppMutation(utils.BaseMutation):
    oauth_app: typing.Optional[types.OAuthAppWithCredentialsType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["APPS_MANAGEMENT", "manage_apps"])
    @transaction.atomic
    def mutate(
        info: Info, **input: inputs.CreateOAuthAppMutationInput
    ) -> "CreateOAuthAppMutation":

        # Validate URLs
        url_validator = URLValidator()
        try:
            url_validator(input["launch_url"])
        except ValidationError:
            return CreateOAuthAppMutation(
                errors=[utils.ErrorType(
                    field="launch_url",
                    messages=["Enter a valid URL."]
                )]
            )

        # Validate redirect URIs
        try:
            validate_redirect_uris(input["redirect_uris"])
        except ValidationError as e:
            return CreateOAuthAppMutation(
                errors=[utils.ErrorType(
                    field="redirect_uris",
                    messages=[str(e)]
                )]
            )

        # Create OAuth2 application with Authorization Code Flow
        registration = Application(
            user=info.context.request.user,
            name=input["display_name"],
            redirect_uris=input["redirect_uris"],
            algorithm=Application.RS256_ALGORITHM,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,  # ✅ Changed to Authorization Code
            skip_authorization=False,  # Require user consent
        )

        # Capture the raw client secret before saving (Django hashes it during save)
        raw_client_secret = registration.client_secret
        registration.save()

        # Create OAuthApp record
        oauth_app = models.OAuthApp.objects.create(
            display_name=input["display_name"],
            description=input.get("description", ""),
            launch_url=input["launch_url"],
            redirect_uris=input["redirect_uris"],
            features=input.get("features", []),
            metadata=input.get("metadata", {}),
            registration=registration,
            created_by=info.context.request.user,
        )

        # Create the response with credentials
        oauth_app_with_credentials = types.OAuthAppWithCredentialsType(
            object_type=oauth_app.object_type,
            id=oauth_app.id,
            display_name=oauth_app.display_name,
            description=oauth_app.description,
            launch_url=oauth_app.launch_url,
            redirect_uris=oauth_app.redirect_uris,
            features=oauth_app.features,
            client_id=oauth_app.client_id,
            client_secret=raw_client_secret,
            created_at=oauth_app.created_at,
            updated_at=oauth_app.updated_at,
            created_by=oauth_app.created_by,
            metadata=oauth_app.metadata,
        )

        return CreateOAuthAppMutation(oauth_app=oauth_app_with_credentials)


@strawberry.type
class UpdateOAuthAppMutation(utils.BaseMutation):
    oauth_app: typing.Optional[types.OAuthAppType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["APPS_MANAGEMENT", "manage_apps"])
    @transaction.atomic
    def mutate(
        info: Info, **input: inputs.UpdateOAuthAppMutationInput
    ) -> "UpdateOAuthAppMutation":
        oauth_app = models.OAuthApp.access_by(info.context.request).get(id=input["id"])

        # Validate redirect URIs if being updated
        if "redirect_uris" in input:
            try:
                validate_redirect_uris(input["redirect_uris"])
            except ValidationError as e:
                return UpdateOAuthAppMutation(
                    errors=[utils.ErrorType(
                        field="redirect_uris",
                        messages=[str(e)]
                    )]
                )

        # Validate launch URL if being updated
        if "launch_url" in input:
            url_validator = URLValidator()
            try:
                url_validator(input["launch_url"])
            except ValidationError:
                return UpdateOAuthAppMutation(
                    errors=[utils.ErrorType(
                        field="launch_url",
                        messages=["Enter a valid URL."]
                    )]
                )

        # Update OAuth app fields
        if "display_name" in input:
            oauth_app.display_name = input["display_name"]
            oauth_app.registration.name = input["display_name"]
        if "description" in input:
            oauth_app.description = input["description"]
        if "launch_url" in input:
            oauth_app.launch_url = input["launch_url"]
        if "redirect_uris" in input:
            oauth_app.redirect_uris = input["redirect_uris"]
            oauth_app.registration.redirect_uris = input["redirect_uris"]
        if "features" in input:
            oauth_app.features = input["features"]
        if "metadata" in input:
            oauth_app.metadata = input["metadata"]

        oauth_app.save()
        oauth_app.registration.save()

        return UpdateOAuthAppMutation(oauth_app=oauth_app)


@strawberry.type
class DeleteOAuthAppMutation(utils.BaseMutation):
    success: bool = False

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["APPS_MANAGEMENT", "manage_apps"])
    @transaction.atomic
    def mutate(
        info: Info, **input: inputs.DeleteOAuthAppMutationInput
    ) -> "DeleteOAuthAppMutation":
        oauth_app = models.OAuthApp.access_by(info.context.request).get(id=input["id"])
        oauth_app.delete()  # This will also delete the OAuth2 application

        return DeleteOAuthAppMutation(success=True)


# App Installation Mutations
@strawberry.type
class InstallAppMutation(utils.BaseMutation):
    installation: typing.Optional[types.AppInstallationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["APPS_MANAGEMENT", "manage_apps"])
    @transaction.atomic
    def mutate(
        info: Info, **input: inputs.InstallAppMutationInput
    ) -> "InstallAppMutation":
        app_id = input["app_id"]
        app_type = input.get("app_type", "marketplace")

        # Check if already installed
        existing_installation = models.AppInstallation.access_by(info.context.request).filter(
            app_id=app_id, is_active=True
        ).first()

        if existing_installation:
            return InstallAppMutation(installation=existing_installation)

        oauth_app = None

        # Create OAuth app if required for private apps that need OAuth
        if app_type == "private" and input.get("requires_oauth") and input.get("oauth_app_data"):
            oauth_data = input["oauth_app_data"]

            # Validate OAuth app data
            try:
                validate_redirect_uris(oauth_data["redirect_uris"])
                url_validator = URLValidator()
                url_validator(oauth_data["launch_url"])
            except ValidationError as e:
                return InstallAppMutation(
                    errors=[utils.ErrorType(
                        field="oauth_app_data",
                        messages=[str(e)]
                    )]
                )

            # Create OAuth2 application with Authorization Code Flow
            registration = Application(
                user=info.context.request.user,
                name=f"{oauth_data['display_name']} (for {app_id})",
                redirect_uris=oauth_data["redirect_uris"],
                algorithm=Application.RS256_ALGORITHM,
                client_type=Application.CLIENT_CONFIDENTIAL,
                authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,  # ✅ Authorization Code Flow
                skip_authorization=False,  # Require user consent
            )

            # Capture the raw client secret before saving (Django hashes it during save)
            raw_client_secret = registration.client_secret
            registration.save()

            # Create OAuthApp record
            oauth_app = models.OAuthApp.objects.create(
                display_name=oauth_data["display_name"],
                description=oauth_data.get("description", ""),
                launch_url=oauth_data["launch_url"],
                redirect_uris=oauth_data["redirect_uris"],
                features=oauth_data.get("features", []),
                metadata=oauth_data.get("metadata", {}),
                registration=registration,
                created_by=info.context.request.user,
            )

        # Create installation record
        installation = models.AppInstallation.objects.create(
            app_id=app_id,
            app_type=app_type,
            access_scopes=input.get("access_scopes", []),
            metadata=input.get("metadata", {}),
            oauth_app=oauth_app,
            is_active=True,
            created_by=info.context.request.user,
        )

        # Handle metafields if provided
        metafields = input.get("metafields", [])
        if any(metafields or []):
            serializers.save_many_to_many_data(
                "metafields",
                graph_serializers.MetafieldModelSerializer,
                installation,
                payload=dict(metafields=metafields),
                context=info.context.request,
            )

        return InstallAppMutation(installation=installation)


@strawberry.type
class UninstallAppMutation(utils.BaseMutation):
    success: bool = False

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["APPS_MANAGEMENT", "manage_apps"])
    def mutate(
        info: Info, **input: inputs.UninstallAppMutationInput
    ) -> "UninstallAppMutation":
        app_id = input.get("app_id")
        installation_id = input.get("installation_id")

        # Validate input - need either app_id or installation_id
        if not (app_id or installation_id):
            return UninstallAppMutation(
                errors=[utils.ErrorType(
                    field="input",
                    messages=["Either app_id or installation_id must be provided"]
                )]
            )

        # Find and delete installation
        queryset = models.AppInstallation.access_by(info.context.request)

        if installation_id:
            queryset = queryset.filter(id=installation_id)
        else:  # app_id
            queryset = queryset.filter(app_id=app_id, is_active=True)

        installation = queryset.first()
        if installation:
            installation.delete()

        return UninstallAppMutation(success=True)


@strawberry.type
class UpdateAppInstallationMutation(utils.BaseMutation):
    installation: typing.Optional[types.AppInstallationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["APPS_MANAGEMENT", "manage_apps"])
    def mutate(
        info: Info, **input: inputs.UpdateAppInstallationMutationInput
    ) -> "UpdateAppInstallationMutation":
        installation = models.AppInstallation.access_by(info.context.request).get(id=input["id"])

        # Update installation fields
        if "access_scopes" in input:
            installation.access_scopes = input["access_scopes"]
        if "is_active" in input:
            installation.is_active = input["is_active"]
        if "metadata" in input:
            installation.metadata = input["metadata"]

        installation.save()

        # Handle metafields if provided
        metafields = input.get("metafields", [])
        if any(metafields or []):
            serializers.save_many_to_many_data(
                "metafields",
                graph_serializers.MetafieldModelSerializer,
                installation,
                payload=dict(metafields=metafields),
                context=info.context.request,
            )

        return UpdateAppInstallationMutation(installation=installation)


@strawberry.type
class RotateAppApiKeyMutation(utils.BaseMutation):
    installation: typing.Optional[types.AppInstallationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["APPS_MANAGEMENT", "manage_apps"])
    def mutate(
        info: Info, **input: inputs.RotateAppApiKeyMutationInput
    ) -> "RotateAppApiKeyMutation":
        installation = models.AppInstallation.access_by(info.context.request).get(id=input["id"])

        # Rotate the API key
        installation.rotate_api_key()

        return RotateAppApiKeyMutation(installation=installation)


@strawberry.type
class EnsureAppApiKeyMutation(utils.BaseMutation):
    installation: typing.Optional[types.AppInstallationType] = None

    @staticmethod
    @utils.authentication_required
    @utils.authorization_required(["APPS_MANAGEMENT", "manage_apps"])
    def mutate(
        info: Info, **input: inputs.EnsureAppApiKeyMutationInput
    ) -> "EnsureAppApiKeyMutation":
        installation = models.AppInstallation.access_by(info.context.request).get(id=input["id"])

        # Ensure API key exists (create if missing)
        installation.ensure_api_key()

        return EnsureAppApiKeyMutation(installation=installation)
