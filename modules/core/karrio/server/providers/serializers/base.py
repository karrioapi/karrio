import typing
import django.db.transaction as transaction
from rest_framework import status as http_status

import karrio.lib as lib
import karrio.references as references
import karrio.server.openapi as openapi
import karrio.server.core.utils as utils
import karrio.server.serializers as serializers
import karrio.server.core.dataunits as dataunits
import karrio.server.core.exceptions as exceptions
import karrio.server.providers.models as providers
from karrio.server.core.serializers import CARRIERS, Message


def generate_carrier_serializers() -> typing.Dict[str, serializers.Serializer]:

    def _create_serializer(carrier_name: str) -> serializers.Serializer:
        fields = dataunits.REFERENCE_MODELS["connection_fields"][carrier_name]
        return type(
            carrier_name,
            (serializers.Serializer,),
            {
                key: serializers.field_to_serializer(field)
                for key, field in fields.items()
            },
        )

    return {
        carrier_name: _create_serializer(carrier_name)
        for carrier_name in dataunits.REFERENCE_MODELS["carriers"].keys()
    }


CONNECTION_SERIALIZERS = generate_carrier_serializers()


@openapi.extend_schema_field(
    openapi.PolymorphicProxySerializer(
        component_name="ConnectionCredentialsField",
        serializers=CONNECTION_SERIALIZERS.values(),
        resource_type_field_name=None,
    )
)
class ConnectionCredentialsField(serializers.DictField):
    pass


class CarrierConnectionData(serializers.Serializer):

    carrier_name = serializers.ChoiceField(
        choices=CARRIERS,
        required=True,
        help_text="A carrier connection type.",
    )
    carrier_id = serializers.CharField(
        required=True,
        help_text="A carrier connection friendly name.",
    )
    credentials = ConnectionCredentialsField(
        required=True,
        help_text="Carrier connection credentials.",
    )
    capabilities = serializers.StringListField(
        required=False,
        allow_null=True,
        help_text="""The carrier enabled capabilities.""",
    )
    config = serializers.PlainDictField(
        required=False,
        default={},
        help_text="Carrier connection custom config.",
    )
    metadata = serializers.PlainDictField(
        required=False,
        default={},
        help_text="User metadata for the carrier.",
    )
    active = serializers.BooleanField(
        required=False,
        default=True,
        help_text="The active flag indicates whether the carrier account is active or not.",
    )


class CarrierConnectionUpdateData(serializers.Serializer):
    carrier_id = serializers.CharField(
        required=False, help_text="A carrier connection friendly name."
    )
    credentials = serializers.PlainDictField(
        required=False,
        help_text="Carrier connection credentials.",
    )
    capabilities = serializers.StringListField(
        required=False,
        allow_null=True,
        help_text="""The carrier enabled capabilities.""",
    )
    config = serializers.PlainDictField(
        required=False,
        default={},
        help_text="Carrier connection custom config.",
    )
    metadata = serializers.PlainDictField(
        required=False,
        default={},
        help_text="User metadata for the carrier.",
    )
    active = serializers.BooleanField(
        required=False,
        help_text="The active flag indicates whether the carrier account is active or not.",
    )


class CarrierConnection(serializers.Serializer):
    """Response serializer for carrier connections.

    Note: Credentials are write-only and never returned in API responses.
    Use CarrierConnectionData for create and CarrierConnectionUpdateData for update.
    """

    id = serializers.CharField(
        required=True,
        help_text="A unique carrier connection identifier",
    )
    object_type = serializers.CharField(
        default="carrier-connection",
        help_text="Specifies the object type",
    )
    carrier_name = serializers.ChoiceField(
        choices=CARRIERS,
        required=True,
        help_text="A carrier connection type.",
    )
    display_name = serializers.CharField(
        required=False,
        help_text="The carrier connection type verbose name.",
    )
    carrier_id = serializers.SerializerMethodField(
        help_text="A carrier connection friendly name.",
    )
    # Note: credentials field removed - write-only (accepted on POST/PATCH, never returned)
    capabilities = serializers.StringListField(
        required=False,
        allow_null=True,
        help_text="""The carrier enabled capabilities.""",
    )
    config = serializers.PlainDictField(
        required=False,
        default={},
        help_text="Carrier connection custom config.",
    )
    metadata = serializers.PlainDictField(
        required=False,
        default={},
        help_text="User metadata for the carrier.",
    )
    is_system = serializers.SerializerMethodField(
        help_text="The carrier connection is provided by the system admin.",
    )
    active = serializers.BooleanField(
        required=True,
        help_text="The active flag indicates whether the carrier account is active or not.",
    )
    test_mode = serializers.BooleanField(
        required=True,
        help_text="The test flag indicates whether to use a carrier configured for test.",
    )

    def get_carrier_id(self, obj) -> str:
        """Get carrier_id, using effective_carrier_id for BrokeredConnection."""
        if isinstance(obj, providers.BrokeredConnection):
            return obj.effective_carrier_id
        return obj.carrier_id

    def get_is_system(self, obj) -> bool:
        """Return True for BrokeredConnection (system connections), False for Carrier (user-owned)."""
        return isinstance(obj, providers.BrokeredConnection)


@serializers.owned_model_serializer
class CarrierConnectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = providers.CarrierConnection
        exclude = ["created_at", "updated_at", "created_by"]

    carrier_name = serializers.ChoiceField(
        required=True, choices=CARRIERS, help_text="Indicates a carrier (type)"
    )
    capabilities = serializers.StringListField(
        required=False,
        allow_null=True,
        help_text="""The carrier enabled capabilities.""",
    )
    config = serializers.PlainDictField(
        required=False,
        allow_null=True,
        help_text="Carrier connection custom config.",
    )

    @transaction.atomic
    @utils.error_wrapper
    def create(
        self,
        validated_data: dict,
        context: serializers.Context,
        **kwargs,
    ) -> providers.CarrierConnection:
        carrier_name = validated_data.pop("carrier_name")
        default_capabilities = references.get_carrier_capabilities(carrier_name)
        capabilities = lib.identity(
            validated_data.get("capabilities")
            if any(validated_data.get("capabilities") or [])
            else default_capabilities
        )

        validated_data.update(test_mode=context.test_mode)
        validated_data.update(carrier_code=carrier_name)
        validated_data.update(
            capabilities=[_ for _ in capabilities if _ in default_capabilities]
        )
        validated_data.update(
            credentials=CONNECTION_SERIALIZERS[carrier_name]
            .map(data=validated_data["credentials"])
            .data
        )
        # Config is stored directly on Carrier model (no longer using CarrierConfig)
        validated_data.setdefault("config", {})

        instance = super().create(validated_data, context=context, **kwargs)

        return instance

    @transaction.atomic
    @utils.error_wrapper
    def update(
        self,
        instance: providers.CarrierConnection,
        validated_data: dict,
        **kwargs,
    ) -> providers.CarrierConnection:
        if any(validated_data.get("capabilities") or []):
            default_capabilities = references.get_carrier_capabilities(instance.ext)
            capabilities = validated_data.get("capabilities")
            instance.capabilities = [
                _ for _ in capabilities if _ in default_capabilities
            ]

        if "credentials" in validated_data:
            data = serializers.process_dictionaries_mutations(
                ["credentials"],
                validated_data,
                instance,
            )
            validated_data.update(
                credentials=CONNECTION_SERIALIZERS[instance.ext]
                .map(data=data["credentials"])
                .data
            )

        if "config" in validated_data:
            # Config is stored directly on Carrier model
            data = serializers.process_dictionaries_mutations(
                ["config"],
                dict(config=validated_data.pop("config")),
                instance,
            )
            validated_data["config"] = data["config"]

        return super().update(instance, validated_data, **kwargs)


class SystemConnectionModelSerializer(serializers.ModelSerializer):
    """Serializer for SystemConnection (admin-managed platform connections)."""

    class Meta:
        model = providers.SystemConnection
        exclude = ["created_at", "updated_at", "created_by", "carrier_code"]

    carrier_name = serializers.ChoiceField(
        required=True, choices=CARRIERS, help_text="Indicates a carrier (type)"
    )
    capabilities = serializers.StringListField(
        required=False,
        allow_null=True,
        help_text="""The carrier enabled capabilities.""",
    )
    config = serializers.PlainDictField(
        required=False,
        allow_null=True,
        help_text="Carrier connection custom config.",
    )

    @transaction.atomic
    @utils.error_wrapper
    def create(
        self,
        validated_data: dict,
    ) -> providers.SystemConnection:
        context = self.context
        carrier_name = validated_data.pop("carrier_name")
        default_capabilities = references.get_carrier_capabilities(carrier_name)
        capabilities = lib.identity(
            validated_data.get("capabilities")
            if any(validated_data.get("capabilities") or [])
            else default_capabilities
        )

        validated_data.update(test_mode=context.test_mode)
        validated_data.update(carrier_code=carrier_name)
        validated_data.update(
            capabilities=[_ for _ in capabilities if _ in default_capabilities]
        )
        validated_data.update(
            credentials=CONNECTION_SERIALIZERS[carrier_name]
            .map(data=validated_data["credentials"])
            .data
        )
        validated_data.setdefault("config", {})

        instance = super().create(validated_data)

        return instance

    @transaction.atomic
    @utils.error_wrapper
    def update(
        self,
        instance: providers.SystemConnection,
        validated_data: dict,
        **kwargs,
    ) -> providers.SystemConnection:
        if any(validated_data.get("capabilities") or []):
            default_capabilities = references.get_carrier_capabilities(instance.carrier_code)
            capabilities = validated_data.get("capabilities")
            instance.capabilities = [
                _ for _ in capabilities if _ in default_capabilities
            ]

        if "credentials" in validated_data:
            data = serializers.process_dictionaries_mutations(
                ["credentials"],
                validated_data,
                instance,
            )
            validated_data.update(
                credentials=CONNECTION_SERIALIZERS[instance.carrier_code]
                .map(data=data["credentials"])
                .data
            )

        if "config" in validated_data:
            data = serializers.process_dictionaries_mutations(
                ["config"],
                dict(config=validated_data.pop("config")),
                instance,
            )
            validated_data["config"] = data["config"]

        return super().update(instance, validated_data, **kwargs)


@serializers.owned_model_serializer
class BrokeredConnectionModelSerializer(serializers.ModelSerializer):
    """
    Serializer for BrokeredConnection (user's enabled instance of SystemConnection).

    Each org gets its own BrokeredConnection per SystemConnection. This is handled
    by the @owned_model_serializer decorator which calls link_org() after creation.

    Key behaviors:
    - Creates a new BrokeredConnection per org (not shared across orgs)
    - Links to org via BrokeredConnectionLink (handled by link_org)
    - Validates that system_connection exists and is active
    """

    class Meta:
        model = providers.BrokeredConnection
        exclude = ["created_at", "updated_at", "created_by", "system_connection"]

    system_connection_id = serializers.CharField(
        required=True,
        help_text="The SystemConnection ID to enable.",
    )
    carrier_id = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        help_text="Optional user-defined carrier identifier (overrides system).",
    )
    config_overrides = serializers.PlainDictField(
        required=False,
        allow_null=True,
        default={},
        help_text="User-specific config overrides (merged with system config).",
    )
    capabilities_overrides = serializers.StringListField(
        required=False,
        allow_null=True,
        default=[],
        help_text="Override capabilities (if empty, uses system capabilities).",
    )
    is_enabled = serializers.BooleanField(
        required=False,
        default=True,
        help_text="Whether this brokered connection is enabled.",
    )

    @transaction.atomic
    @utils.error_wrapper
    def create(
        self,
        validated_data: dict,
        context: serializers.Context,
        **kwargs,
    ) -> providers.BrokeredConnection:
        system_connection_id = validated_data.pop("system_connection_id")

        # Validate system connection exists and is active
        try:
            system_connection = providers.SystemConnection.objects.get(
                pk=system_connection_id,
                active=True,
            )
        except providers.SystemConnection.DoesNotExist:
            raise serializers.ValidationError(
                {"system_connection_id": "SystemConnection not found or not active."}
            )

        # Check if user/org already has a BrokeredConnection for this SystemConnection
        # In multi-org mode, check via link; in OSS mode, check via created_by
        from django.conf import settings as django_settings

        existing_filter = {"system_connection": system_connection}

        if django_settings.MULTI_ORGANIZATIONS and context.org:
            existing = providers.BrokeredConnection.objects.filter(
                **existing_filter,
                link__org=context.org,
            ).first()
        else:
            existing = providers.BrokeredConnection.objects.filter(
                **existing_filter,
                created_by=context.user,
            ).first()

        if existing:
            # Update existing instead of creating new
            return self.update(existing, validated_data)

        # Create new BrokeredConnection
        validated_data["system_connection"] = system_connection
        validated_data.setdefault("is_enabled", True)
        validated_data.setdefault("config_overrides", {})
        validated_data.setdefault("capabilities_overrides", [])
        # Copy carrier_id from SystemConnection as default
        validated_data.setdefault("carrier_id", system_connection.carrier_id)

        instance = super().create(validated_data, context=context, **kwargs)

        return instance

    @transaction.atomic
    @utils.error_wrapper
    def update(
        self,
        instance: providers.BrokeredConnection,
        validated_data: dict,
        **kwargs,
    ) -> providers.BrokeredConnection:
        # Handle config_overrides as dictionary mutation
        if "config_overrides" in validated_data:
            data = serializers.process_dictionaries_mutations(
                ["config_overrides"],
                dict(config_overrides=validated_data.pop("config_overrides")),
                instance,
            )
            validated_data["config_overrides"] = data["config_overrides"]

        # Remove system_connection_id if present (can't change after creation)
        validated_data.pop("system_connection_id", None)
        validated_data.pop("system_connection", None)

        return super().update(instance, validated_data, **kwargs)


# =============================================================================
# Webhook Management Serializers
# =============================================================================


class WebhookOperationResponse(serializers.Serializer):
    """Response serializer for webhook operations."""

    operation = serializers.CharField(help_text="The operation performed")
    success = serializers.BooleanField(help_text="Whether the operation was successful")
    carrier_name = serializers.CharField(help_text="The carrier name")
    carrier_id = serializers.CharField(help_text="The carrier connection ID")
    messages = Message(
        required=False,
        many=True,
        help_text="Operation messages or errors",
    )


class WebhookRegisterData(serializers.Serializer):
    """Request serializer for webhook registration."""

    enabled_events = serializers.StringListField(
        required=False,
        default=["*"],
        help_text="Events to subscribe to. Defaults to all events.",
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Description for the webhook registration.",
    )


class WebhookRegisterSerializer(serializers.Serializer):
    """Handles webhook registration with carriers. Returns webhook details on success."""

    webhook_url = serializers.URLField(
        required=True,
        help_text="The URL to receive webhook events.",
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Description for the webhook registration.",
    )

    @utils.error_wrapper
    def update(self, connection: providers.CarrierConnection, validated_data: dict, **kwargs):
        import karrio.server.core.gateway as gateway

        webhook_url = validated_data["webhook_url"]
        description = validated_data.get(
            "description", f"Karrio webhook for {connection.carrier_id}"
        )

        webhook_details, messages = gateway.Webhooks.register(
            dict(url=webhook_url, description=description),
            carrier=connection,
            **kwargs,
        )

        if webhook_details is None:
            raise exceptions.APIException(
                detail=messages,
                status_code=http_status.HTTP_424_FAILED_DEPENDENCY,
            )

        return webhook_details


class WebhookDeregisterSerializer(serializers.Serializer):
    """Handles webhook deregistration from carriers. Returns confirmation on success."""

    webhook_id = serializers.CharField(
        required=True,
        help_text="The webhook ID to deregister.",
    )

    @utils.error_wrapper
    def update(self, connection: providers.CarrierConnection, validated_data: dict, **kwargs):
        import karrio.server.core.gateway as gateway

        confirmation, messages = gateway.Webhooks.unregister(
            payload=dict(webhook_id=validated_data["webhook_id"]),
            carrier=connection,
        )

        if not (confirmation and confirmation.success):
            raise exceptions.APIException(
                detail=messages,
                status_code=http_status.HTTP_424_FAILED_DEPENDENCY,
            )

        return confirmation


# =============================================================================
# OAuth Callback Serializers
# =============================================================================


class OAuthAuthorizeData(serializers.Serializer):
    """Request serializer for OAuth authorization."""

    frontend_url = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Frontend URL to redirect to after OAuth callback.",
    )


class OAuthCallbackData(serializers.Serializer):
    """Request serializer for OAuth callback data."""

    query = serializers.PlainDictField(
        required=False,
        default={},
        help_text="Query parameters from the OAuth callback.",
    )
    body = serializers.PlainDictField(
        required=False,
        default={},
        help_text="Body data from the OAuth callback.",
    )
    headers = serializers.PlainDictField(
        required=False,
        default={},
        help_text="Headers from the OAuth callback.",
    )
    url = serializers.CharField(
        required=False,
        help_text="The full callback URL.",
    )


class OAuthCallbackSerializer(serializers.Serializer):
    """Handles OAuth callback processing logic."""

    @staticmethod
    def process_callback(
        request,
        carrier_name: str,
    ) -> dict:
        """Process OAuth callback and return result dict."""
        import json
        import base64
        import karrio.lib as lib
        import karrio.server.core.gateway as gateway

        payload = OAuthCallbackData.map(
            data=dict(
                query=request.query_params.dict(),
                body=(
                    request.data.dict()
                    if hasattr(request.data, "dict")
                    else dict(request.data or {})
                ),
                headers=dict(request.headers),
                url=request.build_absolute_uri(),
            )
        ).data

        [output, messages] = gateway.Hooks.on_oauth_callback(
            payload=payload,
            carrier_name=carrier_name,
            test_mode=request.test_mode,
            context=request,
        )

        result = dict(
            type="oauth_callback",
            success=output is not None,
            carrier_name=carrier_name,
            credentials=lib.to_dict(output) if output else None,
            messages=lib.to_dict(messages),
            state=request.query_params.get("state"),
        )

        frontend_url = None
        state = request.query_params.get("state")
        if state:
            try:
                state_data = json.loads(base64.b64decode(state).decode("utf-8"))
                frontend_url = state_data.get("frontend_url")
            except Exception:
                pass

        return result, frontend_url


# =============================================================================
# Webhook Event Serializers
# =============================================================================


class WebhookEventSerializer(serializers.Serializer):
    """Handles webhook event processing logic."""

    @staticmethod
    def process_event(request, pk: str) -> tuple:
        """
        Process webhook event and return response data and status code.

        Returns:
            tuple: (response_data, http_status_code)
        """
        import django.db.models as django
        import karrio.lib as lib
        import karrio.server.core.gateway as gateway

        try:
            connection = providers.CarrierConnection.objects.get(pk=pk)
        except providers.CarrierConnection.DoesNotExist:
            return (
                dict(
                    operation="Webhook event",
                    success=False,
                    messages=[{"message": f"Connection not found: {pk}"}],
                ),
                http_status.HTTP_404_NOT_FOUND,
            )

        event, messages = gateway.Hooks.on_webhook_event(
            payload=dict(
                url=request.build_absolute_uri(),
                body=request.data,
                query=dict(request.query_params),
                headers=dict(request.headers),
            ),
            carrier=connection,
        )

        if event and event.tracking:
            import karrio.server.manager.models as manager_models
            import karrio.server.manager.serializers.tracking as tracking_serializers

            tracker = manager_models.Tracking.objects.filter(
                django.Q(tracking_number=event.tracking.tracking_number)
                | django.Q(carrier__connection_id=str(connection.id))
            ).first()

            if tracker:
                tracking_serializers.update_tracker(
                    tracker, lib.to_dict(event.tracking)
                )

        return (
            dict(
                operation="Webhook event",
                success=len(messages) == 0,
                carrier_name=connection.carrier_name,
                carrier_id=connection.carrier_id,
                messages=lib.to_dict(messages),
            ),
            http_status.HTTP_200_OK,
        )
