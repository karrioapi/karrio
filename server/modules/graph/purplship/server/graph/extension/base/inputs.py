import graphene
from graphene_django.rest_framework.serializer_converter import (
    convert_serializer_to_input_type as serializer_to_input,
)

from purplship.server.core import serializers
from purplship.server.serializers import make_fields_optional
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
        dict(),
    )


def create_customs_input(optional: bool = False) -> graphene.InputObjectType:
    _method = "Partial" if optional else ""
    _type = (
        model_serializers.CustomsModelSerializer
        if optional
        else make_fields_optional(model_serializers.CustomsModelSerializer)
    )

    return type(
        f"{_method}CustomsTemplate",
        (serializer_to_input(_type),),
        dict(
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
