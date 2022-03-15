import graphene
from graphene.types import generic
from graphene_django.rest_framework.serializer_converter import (
    convert_serializer_to_input_type as serializer_to_input,
)

from karrio.server.core import serializers
from karrio.server.serializers import make_fields_optional, exclude_id_field
import karrio.server.graph.serializers as model_serializers
import karrio.server.graph.utils as utils


def create_address_input(partial: bool = False) -> graphene.InputObjectType:
    _method = "Partial" if partial else ""
    _type = (
        make_fields_optional(model_serializers.AddressModelSerializer)
        if partial
        else exclude_id_field(model_serializers.AddressModelSerializer)
    )

    return type(
        f"{_method}Address",
        (serializer_to_input(_type),),
        dict(
            country_code=utils.CountryCodeEnum(required=not partial),
        ),
    )


def create_commodity_input(partial: bool = False) -> graphene.InputObjectType:
    _method = "Partial" if partial else ""
    _type = (
        make_fields_optional(model_serializers.CommodityModelSerializer)
        if partial
        else exclude_id_field(model_serializers.CommodityModelSerializer)
    )

    return type(
        f"{_method}Commodity",
        (serializer_to_input(_type),),
        dict(
            parent_id=graphene.String(required=False),
            weight_unit=utils.WeightUnitEnum(required=False),
            origin_country=utils.CountryCodeEnum(required=False),
            value_currency=utils.CurrencyCodeEnum(required=False),
            metadata=generic.GenericScalar(),
        ),
    )


def create_payment_input() -> graphene.InputObjectType:
    return type(
        "PartialPayment",
        (serializer_to_input(serializers.Payment),),
        dict(
            paid_by=utils.PaidByEnum(required=False),
        ),
    )


def create_duty_input() -> graphene.InputObjectType:
    return type(
        "PartialDuty",
        (serializer_to_input(serializers.Duty),),
        dict(
            paid_by=utils.PaidByEnum(required=False),
            currency=utils.CurrencyCodeEnum(required=False),
            bill_to=graphene.Field(UpdateAddressInput, required=False),
        ),
    )


def create_customs_input(partial: bool = False) -> graphene.InputObjectType:
    _method = "Partial" if partial else ""
    _type = (
        make_fields_optional(model_serializers.CustomsModelSerializer)
        if partial
        else model_serializers.CustomsModelSerializer
    )

    return type(
        f"{_method}Customs",
        (serializer_to_input(_type),),
        dict(
            commodities=graphene.List(
                UpdateCommodityInput if partial else CreateCommodityInput
            ),
            incoterm=utils.IncotermCodeEnum(required=False),
            content_type=utils.CustomsContentTypeEnum(required=False),
            duty=graphene.Field(DutyInput, required=False),
            options=generic.GenericScalar(),
        ),
    )


def create_parcel_input(partial: bool = False) -> graphene.InputObjectType:
    _method = "Partial" if partial else ""
    _type = (
        make_fields_optional(model_serializers.ParcelModelSerializer)
        if partial
        else exclude_id_field(model_serializers.ParcelModelSerializer)
    )

    return type(
        f"{_method}Parcel",
        (serializer_to_input(_type),),
        dict(
            items=graphene.List(
                UpdateCommodityInput if partial else CreateCommodityInput
            ),
            weight_unit=utils.WeightUnitEnum(required=False),
            dimension_unit=utils.DimensionUnitEnum(required=False),
        ),
    )


def create_label_template_input(partial: bool = False) -> graphene.InputObjectType:
    _method = "Partial" if partial else ""
    _type = (
        make_fields_optional(model_serializers.LabelTemplateModelSerializer)
        if partial
        else exclude_id_field(model_serializers.LabelTemplateModelSerializer)
    )

    return type(
        f"{_method}LabelTemplate",
        (serializer_to_input(_type),),
        dict(
            template_type=utils.LabelTypeEnum(required=False),
        ),
    )


def create_service_level_input(partial: bool = False) -> graphene.InputObjectType:
    _method = "Partial" if partial else ""
    _type = (
        make_fields_optional(model_serializers.ServiceLevelModelSerializer)
        if partial
        else exclude_id_field(model_serializers.ServiceLevelModelSerializer)
    )

    return type(
        f"{_method}ServiceLevel",
        (serializer_to_input(_type),),
        dict(
            weight_unit=utils.WeightUnitEnum(required=False),
            dimension_unit=utils.DimensionUnitEnum(required=False),
        ),
    )


def create_connection_input(partial: bool = False) -> graphene.InputObjectType:
    _method = "Update" if partial else "Create"
    _fields = dict()

    for name, serializer in model_serializers.CARRIER_MODEL_SERIALIZERS.items():
        _extra_fields = dict()
        _serializer = make_fields_optional(serializer) if partial else serializer

        if hasattr(_serializer.Meta.model, "label_template"):
            _extra_fields["label_template"] = graphene.Field(
                UpdateLabelTemplateInput if partial else CreateLabelTemplateInput,
                required=False,
            )

        if hasattr(_serializer.Meta.model, "services"):
            _extra_fields["services"] = graphene.List(
                UpdateServiceLevelInput if partial else CreateServiceLevelInput,
                required=False,
            )

        _input = type(
            f"{_method}{_serializer.__name__}",
            (serializer_to_input(_serializer),),
            _extra_fields,
        )
        _field = type(
            f"{_method}{serializer.__name__}",
            (_input,),
            dict(
                carrier_id=graphene.String(required=not partial),
                metadata=generic.GenericScalar(),
            ),
        )
        _fields.update(
            {
                name: graphene.Field(_field, required=False),
            }
        )

    return type("Settings", (object,), _fields)


PaymentInput = create_payment_input()
CreateCommodityInput = create_commodity_input()
UpdateCommodityInput = create_commodity_input(partial=True)
CreateAddressInput = create_address_input()
UpdateAddressInput = create_address_input(partial=True)
DutyInput = create_duty_input()
CreateCustomsInput = create_customs_input()
UpdateCustomsInput = create_customs_input(partial=True)
CreateParcelInput = create_parcel_input()
UpdateParcelInput = create_parcel_input(partial=True)

CreateAddressTemplateInput = type("CreateAddressTemplate", (CreateAddressInput,), {})
UpdateAddressTemplateInput = type("UpdateAddressTemplate", (UpdateAddressInput,), {})
CreateCustomsTemplateInput = type("CreateCustomsTemplate", (CreateCustomsInput,), {})
UpdateCustomsTemplateInput = type("UpdateCustomsTemplate", (UpdateCustomsInput,), {})
CreateParcelTemplateInput = type("CreateParcelTemplate", (CreateParcelInput,), {})
UpdateParcelTemplateInput = type("UpdateParcelTemplate", (UpdateParcelInput,), {})

CreateLabelTemplateInput = create_label_template_input()
UpdateLabelTemplateInput = create_label_template_input(partial=True)
CreateServiceLevelInput = create_service_level_input()
UpdateServiceLevelInput = create_service_level_input(partial=True)

CreateConnectionInput = create_connection_input()
UpdateConnectionInput = create_connection_input(partial=True)
