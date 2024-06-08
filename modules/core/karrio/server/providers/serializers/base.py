import typing

import karrio.server.serializers as serializers
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


SERIALIZERS = generate_provider_serializer()


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
            _args = (
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
    credentials = serializers.PlainDictField(
        required=True,
        help_text="Carrier connection credentials.",
    )
    config = serializers.PlainDictField(
        required=False,
        default={},
        help_text="Carrier connection custom config.",
    )
    capabilities = serializers.StringListField(
        required=False,
        allow_null=True,
        help_text="""The carrier enabled capabilities.""",
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
        required=True, help_text="A carrier connection friendly name."
    )
    credentials = serializers.PlainDictField(
        required=True,
        help_text="Carrier connection credentials.",
    )
    config = serializers.PlainDictField(
        required=False,
        default={},
        help_text="Carrier connection custom config.",
    )
    capabilities = serializers.StringListField(
        required=False,
        allow_null=True,
        help_text="""The carrier enabled capabilities.""",
    )
    metadata = serializers.PlainDictField(
        required=False,
        default={},
        help_text="User metadata for the carrier.",
    )
    active = serializers.BooleanField(
        required=True,
        help_text="The active flag indicates whether the carrier account is active or not.",
    )


class CarrierConnection(serializers.Serializer):
    id = serializers.CharField(
        required=True,
        help_text="A unique address identifier",
    )
    object_type = serializers.CharField(
        default="carrier-connection",
        help_text="Specifies the object type",
    )
    carrier_id = serializers.CharField(
        required=True,
        help_text="A carrier connection friendly name.",
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
    capabilities = serializers.StringListField(
        required=False,
        allow_null=True,
        help_text="""The carrier enabled capabilities.""",
    )
    credentials = serializers.PlainDictField(
        required=True,
        help_text="Carrier connection credentials.",
    )
    config = serializers.PlainDictField(
        required=False,
        default={},
        help_text="Carrier connection custom config.",
    )
    active = serializers.BooleanField(
        required=True,
        help_text="The active flag indicates whether the carrier account is active or not.",
    )
    test_mode = serializers.BooleanField(
        required=True,
        help_text="The test flag indicates whether to use a carrier configured for test.",
    )
    metadata = serializers.PlainDictField(
        required=False,
        default={},
        help_text="User metadata for the carrier.",
    )


@serializers.owned_model_serializer
class CarrierConnectionModelSerializer(serializers.Serializer):
    class Meta:
        model = providers.CarrierConnection
        exclude = ["created_at", "updated_at", "created_by"]
