import typing
import karrio.lib as lib


FEDEX_PACKAGE_LOCATION_VALUES = {"FRONT", "NONE", "REAR", "SIDE"}


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