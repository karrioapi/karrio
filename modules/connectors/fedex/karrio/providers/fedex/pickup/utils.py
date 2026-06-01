import typing
import karrio.lib as lib
import karrio.schemas.fedex.pickup_request as fedex


FEDEX_PACKAGE_LOCATION_VALUES = {"FRONT", "NONE", "REAR", "SIDE"}
FEDEX_PICKUP_ADDRESS_TYPE_VALUES = {"ACCOUNT", "SHIPPER", "OTHER"}
FEDEX_MAX_NOTIFICATION_EMAILS = 5


def _normalize_email_values(
    value: typing.Any,
) -> typing.List[str]:
    if value is None:
        return []

    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]

    return [
        _.strip()
        for _ in str(value).replace(";", ",").split(",")
        if _.strip()
    ]


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


def resolve_notification_emails(
    primary_email: typing.Optional[str], options: typing.Optional[dict]
) -> typing.List[str]:
    options = options or {}
    emails: typing.List[str] = []

    if primary_email:
        emails.append(str(primary_email).strip())

    emails.extend(_normalize_email_values(options.get("email_notification_to")))
    emails.extend(_normalize_email_values(options.get("fedex_notification_emails")))

    unique_emails: typing.List[str] = []
    seen = set()
    for email in emails:
        key = email.lower()
        if key not in seen:
            unique_emails.append(email)
            seen.add(key)

    if len(unique_emails) > FEDEX_MAX_NOTIFICATION_EMAILS:
        raise lib.exceptions.FieldError(
            {
                "fedex_notification_emails": (
                    f"FedEx pickup notification supports up to {FEDEX_MAX_NOTIFICATION_EMAILS} email addresses. "
                    f"Received: {len(unique_emails)}"
                )
            }
        )

    return unique_emails


def build_notification_email_details(
    emails: typing.List[str],
) -> typing.List[fedex.EmailDetailType]:
    return [
        fedex.EmailDetailType(
            address=email,
            locale="en_US",
        )
        for email in emails
    ]