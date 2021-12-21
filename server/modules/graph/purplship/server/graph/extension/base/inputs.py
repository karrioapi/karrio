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
        f"{_method}AddressTemplate",
        (serializer_to_input(_type),),
        dict(
            validation=types.generic.GenericScalar(),
        ),
    )


def create_customs_input(optional: bool = False) -> graphene.InputObjectType:
    _method = "Partial" if optional else ""
    _type = (
        make_fields_optional(model_serializers.CustomsModelSerializer)
        if optional
        else model_serializers.CustomsModelSerializer
    )
    _commodities = serializer_to_input(
        make_fields_optional(model_serializers.CommodityModelSerializer)
        if optional
        else exclude_id_field(model_serializers.CommodityModelSerializer)
    )

    return type(
        f"{_method}CustomsTemplate",
        (serializer_to_input(_type),),
        dict(
            commodities=graphene.List(_commodities),
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
        f"{_method}ParcelTemplate",
        (serializer_to_input(_type),),
        dict(),
    )


CreateAddressTemplateInput = create_address_input()
UpdateAddressTemplateInput = create_address_input(optional=True)
CreateCustomsTemplateInput = create_customs_input()
UpdateCustomsTemplateInput = create_customs_input(optional=True)
CreateParcelTemplateInput = create_parcel_input()
UpdateParcelTemplateInput = create_parcel_input(optional=True)
