import typing
import karrio.lib as lib


FEDEX_PACKAGE_LOCATION_VALUES = {"FRONT", "NONE", "REAR", "SIDE"}
FEDEX_PICKUP_ADDRESS_TYPE_VALUES = {"ACCOUNT", "SHIPPER", "OTHER"}


def validate_package_location(value: typing.Optional[str]) -> typing.Optional[str]:
    if value is None:
        return None

    package_location = str(value).strip().upper()
    if package_location not in FEDEX_PACKAGE_LOCATION_VALUES:
        raise lib.exceptions.FieldError(
            {
                "package_location": (
                    f"Invalid FedEx package location '{value}'. "
                    f"Expected one of: {sorted(FEDEX_PACKAGE_LOCATION_VALUES)}"
                )
            }
        )

    return package_location


def validate_pickup_address_type(value: typing.Optional[str]) -> str:
    if value is None:
        return "OTHER"

    pickup_address_type = str(value).strip().upper()
    if pickup_address_type not in FEDEX_PICKUP_ADDRESS_TYPE_VALUES:
        raise lib.exceptions.FieldError(
            {
                "fedex_pickup_address_type": (
                    f"Invalid FedEx pickup address type '{value}'. "
                    f"Expected one of: {sorted(FEDEX_PICKUP_ADDRESS_TYPE_VALUES)}"
                )
            }
        )

    return pickup_address_type