import graphene
from graphene_django.rest_framework.serializer_converter import (
    convert_serializer_to_input_type as serializer_to_input,
)

from purplship.server.core import serializers
from purplship.server.serializers import make_fields_optional, exclude_id_field
import purplship.server.graph.serializers as model_serializers
import purplship.server.graph.extension.base.types as types


def create_address_input(optional: bool = False) -> graphene.InputObjectType:
    _method = "Partial" if optional else ""
    _type = (
        model_serializers.AddressModelSerializer
        if optional
        else make_fields_optional(model_serializers.AddressModelSerializer)
    )

    return type(
        f"{_method}Address",
        (serializer_to_input(_type),),
        dict(
            country_code=types.CountryCodeEnum(required=False),
            validation=types.generic.GenericScalar(),
        ),
    )


def create_commodity_input(optional: bool = False) -> graphene.InputObjectType:
    _method = "Partial" if optional else ""
    _type = (
        make_fields_optional(model_serializers.CommodityModelSerializer)
        if optional
        else exclude_id_field(model_serializers.CommodityModelSerializer)
    )

    return type(
        f"{_method}Commodity",
        (serializer_to_input(_type),),
        dict(
            parent_id=graphene.String(required=False),
            weight_unit=types.WeightUnitEnum(required=False),
            origin_country=types.CountryCodeEnum(required=False),
            value_currency=types.CurrencyCodeEnum(required=False),
            metadata=types.generic.GenericScalar(),
        ),
    )


def create_customs_input(optional: bool = False) -> graphene.InputObjectType:
    _method = "Partial" if optional else ""
    _type = (
        make_fields_optional(model_serializers.CustomsModelSerializer)
        if optional
        else model_serializers.CustomsModelSerializer
    )

    return type(
        f"{_method}Customs",
        (serializer_to_input(_type),),
        dict(
            commodities=graphene.List(create_commodity_input(optional)),
            incoterm=types.IncotermCodeEnum(required=False),
            content_type=types.CustomsContentTypeEnum(required=False),
            duty=graphene.Field(serializer_to_input(serializers.Duty)),
            options=types.generic.GenericScalar(),
        ),
    )


def create_parcel_input(optional: bool = False) -> graphene.InputObjectType:
    _method = "Partial" if optional else ""
    _type = (
        model_serializers.ParcelModelSerializer
        if optional
        else make_fields_optional(model_serializers.ParcelModelSerializer)
    )

    return type(
        f"{_method}Parcel",
        (serializer_to_input(_type),),
        dict(
            weight_unit=types.WeightUnitEnum(required=False),
            dimension_unit=types.DimensionUnitEnum(required=False),
        ),
    )


CreateCommodityInput = create_commodity_input()
UpdateCommodityInput = create_commodity_input(optional=True)
CreateAddressInput = create_address_input()
UpdateAddressInput = create_address_input(optional=True)
CreateCustomsInput = create_customs_input()
UpdateCustomsInput = create_customs_input(optional=True)
CreateParcelInput = create_parcel_input()
UpdateParcelInput = create_parcel_input(optional=True)

CreateAddressTemplateInput = type("CreateAddressTemplate", (CreateAddressInput,), {})
UpdateAddressTemplateInput = type("UpdateAddressTemplate", (UpdateAddressInput,), {})
CreateCustomsTemplateInput = type("CreateCustomsTemplate", (CreateCustomsInput,), {})
UpdateCustomsTemplateInput = type("UpdateCustomsTemplate", (UpdateCustomsInput,), {})
CreateParcelTemplateInput = type("CreateParcelTemplate", (CreateParcelInput,), {})
UpdateParcelTemplateInput = type("UpdateParcelTemplate", (UpdateParcelInput,), {})
