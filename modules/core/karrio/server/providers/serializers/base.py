import typing
import django.db.transaction as transaction

import karrio.lib as lib
import karrio.references as references
import karrio.server.openapi as openapi
import karrio.server.core.utils as utils
import karrio.server.serializers as serializers
import karrio.server.core.dataunits as dataunits
import karrio.server.providers.models as providers
from karrio.server.core.serializers import CARRIERS


CarrierName = str
CarrierSerializerType = typing.Type[serializers.ModelSerializer]


def generate_provider_serializer() -> typing.Dict[CarrierName, CarrierSerializerType]:
    def _create_serializer(name) -> CarrierSerializerType:
        class _CarrierSerializer(serializers.ModelSerializer):
            class Meta:
                model = providers.MODELS[name]
                exclude = ["id", "created_at", "updated_at", "created_by"]

        return _CarrierSerializer

    return {name: _create_serializer(name) for name in providers.MODELS.keys()}


def generate_carrier_serializers() -> typing.Dict[CarrierName, serializers.Serializer]:

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


SERIALIZERS = generate_provider_serializer()
CONNECTION_SERIALIZERS = generate_carrier_serializers()


class CarrierSerializer(serializers.Serializer):
    carrier_name = serializers.ChoiceField(
        required=True, choices=CARRIERS, help_text="Indicates a carrier (type)"
    )
    carrier_config = serializers.PlainDictField(
        required=True,
        help_text="the logistics service provider connection configuration",
    )

    def __init__(self, *args, **kwargs):
        carrier_name: str = kwargs.get("data", {}).get("carrier_name")
        instance, *_ = args + (None,)

        if carrier_name in SERIALIZERS:
            carrier_config_data: dict = kwargs.get("data", {}).get("carrier_config", {})
            serializer = SERIALIZERS[carrier_name]
            _args = lib.identity(
                [
                    providers.MODELS[carrier_name].objects.get(
                        pk=carrier_config_data["id"]
                    )
                ]
                if "id" in carrier_config_data
                else []
            )
            carrier_config = serializer.map(*_args, data=carrier_config_data).data
            kwargs.update(
                data=dict(carrier_name=carrier_name, carrier_config=carrier_config)
            )

            if "id" in carrier_config_data:
                args = _args

        super().__init__(*args, **kwargs)

    def create(self, validated_data: dict, **kwargs) -> providers.Carrier:
        created_by = validated_data["created_by"]
        carrier_name = validated_data["carrier_name"]
        carrier_config = {**validated_data["carrier_config"], "created_by": created_by}

        return providers.MODELS[carrier_name].objects.create(**carrier_config)

    def update(
        self, instance: providers.Carrier, validated_data: dict, **kwargs
    ) -> providers.Carrier:
        carrier_config = validated_data["carrier_config"]

        for key, val in carrier_config.items():
            setattr(instance, key, val)

        instance.save()
        return instance


@openapi.extend_schema_field(
    openapi.PolymorphicProxySerializer(
        component_name="ConnectionCredentialsField",
        serializers=CONNECTION_SERIALIZERS.values(),
        resource_type_field_name=None,
    )
)
class ConnectionCredentialsField(serializers.DictField):
    pass


@serializers.owned_model_serializer
class CarrierConfigModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = providers.CarrierConfig
        exclude = ["created_at", "updated_at", "created_by"]
        extra_kwargs = {field: {"read_only": True} for field in ["id"]}


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
    carrier_id = serializers.CharField(
        required=True,
        help_text="A carrier connection friendly name.",
    )
    credentials = ConnectionCredentialsField(
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
    is_system = serializers.BooleanField(
        required=True,
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


@serializers.owned_model_serializer
class CarrierConnectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = providers.Carrier
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
        **kwargs,
    ) -> providers.Carrier:
        config = validated_data.pop("config")
        carrier_name = validated_data.pop("carrier_name")
        default_capabilities = references.get_carrier_capabilities(carrier_name)
        capabilities = lib.identity(
            validated_data.get("capabilities")
            if any(validated_data.get("capabilities") or [])
            else default_capabilities
        )

        validated_data.update(carrier_code=carrier_name)
        validated_data.update(
            capabilities=[_ for _ in capabilities if _ in default_capabilities]
        )
        validated_data.update(
            credentials=CONNECTION_SERIALIZERS[carrier_name]
            .map(data=validated_data["credentials"])
            .data
        )

        instance = super().create(validated_data, **kwargs)

        if config is not None:
            CarrierConfigModelSerializer.map(
                context=kwargs.get("context"),
                data={"carrier": instance.pk, "config": config},
            ).save()

        return providers.Carrier.objects.get(pk=instance.pk)

    @transaction.atomic
    @utils.error_wrapper
    def update(
        self,
        instance: providers.Carrier,
        validated_data: dict,
        **kwargs,
    ) -> providers.Carrier:
        if any(validated_data.get("capabilities") or []):
            default_capabilities = references.get_carrier_capabilities(
                instance.carrier_name
            )
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
                credentials=CONNECTION_SERIALIZERS[instance.carrier_name]
                .map(data=data["credentials"])
                .data
            )

        if "config" in validated_data:
            data = serializers.process_dictionaries_mutations(
                ["config"],
                dict(config=validated_data.pop("config")),
                instance,
            )
            lib.identity(
                CarrierConfigModelSerializer.map(
                    instance=instance.carrier_config,
                    context=kwargs.get("context"),
                    data={"carrier": instance.pk, **data},
                )
                .save()
                .instance
            )

        return super().update(instance, validated_data, **kwargs)
