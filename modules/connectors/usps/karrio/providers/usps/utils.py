"""USPS connection settings."""

import re
import typing
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors

AccountType = lib.units.create_enum(
    "AccountType",
    ["EPS", "PERMIT", "METER"],
)


class Settings(core.Settings):
    """USPS connection settings."""

    # Add carrier specific api connection properties here
    client_id: str
    client_secret: str
    account_number: str = None
    account_type: AccountType = "EPS"  # type: ignore
    manifest_MID: str = None
    CRID: str = None
    MID: str = None

    @property
    def carrier_name(self):
        return "usps"

    @property
    def server_url(self):
        return "https://api-cat.usps.com" if self.test_mode else "https://apis.usps.com"

    @property
    def tracking_url(self):
        return "https://tools.usps.com/go/TrackConfirmAction?tLabels={}"

    @property
    def connection_config(self) -> lib.units.Options:
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def access_token(self):
        """Retrieve the access_token using the client_id|client_secret pair
        or collect it from the cache if an unexpired access_token exist.
        """
        cache_key = f"access|{self.carrier_name}|{self.client_id}|{self.client_secret}"
        now = datetime.datetime.now() + datetime.timedelta(minutes=30)

        auth = self.connection_cache.get(cache_key) or {}
        token = auth.get("access_token")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token

        self.connection_cache.set(cache_key, lambda: oauth2_login(self))
        new_auth = self.connection_cache.get(cache_key)

        return new_auth["access_token"]

    @property
    def payment_token(self):
        """Retrieve the paymentAuthorizationToken using the client_id|client_secret pair
        or collect it from the cache if an unexpired paymentAuthorizationToken exist.
        """
        cache_key = f"payment|{self.carrier_name}|{self.client_id}|{self.client_secret}"
        now = datetime.datetime.now() + datetime.timedelta(minutes=45)

        auth = self.connection_cache.get(cache_key) or {}
        token = auth.get("paymentAuthorizationToken")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token

        self.connection_cache.set(cache_key, lambda: payment_auth(self))
        new_auth = self.connection_cache.get(cache_key)

        return new_auth["paymentAuthorizationToken"]


class ConnectionConfig(lib.Enum):
    permit_ZIP = lib.OptionEnum("permit_ZIP")
    permit_number = lib.OptionEnum("permit_number")
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)


def oauth2_login(settings: Settings):
    import karrio.providers.usps.error as error

    API_SCOPES = [
        "addresses",
        "international-prices",
        "subscriptions",
        "payments",
        "pickup",
        "tracking",
        "labels",
        "scan-forms",
        "companies",
        "service-delivery-standards",
        "locations",
        "international-labels",
        "prices",
        "shipments",
    ]
    result = lib.request(
        url=f"{settings.server_url}/oauth2/v3/token",
        method="POST",
        headers={"content-Type": "application/x-www-form-urlencoded"},
        data=lib.to_query_string(
            dict(
                grant_type="client_credentials",
                client_id=settings.client_id,
                client_secret=settings.client_secret,
                scope=" ".join(API_SCOPES),
            )
        ),
    )

    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ParsedMessagesError(messages)

    expiry = datetime.datetime.now() + datetime.timedelta(
        seconds=float(response.get("expires_in", 0))
    )

    return {**response, "expiry": lib.fdatetime(expiry)}


def payment_auth(settings: Settings):
    import karrio.providers.usps.error as error

    result = lib.request(
        url=f"{settings.server_url}/payments/v3/payment-authorization",
        method="POST",
        headers={
            "content-Type": "application/json",
            "Authorization": f"Bearer {settings.access_token}",
        },
        data=lib.to_json(
            {
                "roles": [
                    {
                        "roleName": "LABEL_OWNER",
                        "CRID": settings.CRID,
                        "MID": settings.MID,
                        "accountType": settings.account_type or "EPS",
                        "accountNumber": settings.account_number,
                        "manifestMID": settings.manifest_MID,
                        # "permitNumber": settings.connection_config.permit_number.state,
                        # "permitZIP": settings.connection_config.permit_ZIP.state,
                    },
                    {
                        "roleName": "PAYER",
                        "CRID": settings.CRID,
                        "MID": settings.MID,
                        "accountType": settings.account_type or "EPS",
                        "accountNumber": settings.account_number,
                        # "permitNumber": settings.connection_config.permit_number.state,
                        # "permitZIP": settings.connection_config.permit_zip.state,
                    },
                ]
            }
        ),
    )

    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ParsedMessagesError(messages)

    expiry = datetime.datetime.now() + datetime.timedelta(minutes=50)

    return {**response, "expiry": lib.fdatetime(expiry)}


def normalize_multipart_response(response: str) -> str:
    """Normalize a multipart response string to have consistent formatting"""
    # Find boundary
    boundary_match = re.search(r"--[a-zA-Z0-9\+/=_-]+", response)
    if not boundary_match:
        return response

    boundary = boundary_match.group(0)

    # Split into parts using boundary
    parts = response.split(boundary)

    # Format each part
    formatted_parts = []
    for part in parts:
        if (
            not part.strip() or part.strip() == "--"
        ):  # Skip empty parts and end boundary
            continue

        # Remove excess whitespace and normalize line endings
        part = part.strip().replace("\r\n", "\n").replace("\n\n\n", "\n\n")

        # Extract headers and content
        if "Content-Type" in part:
            # Split headers and content
            headers = []
            content = ""

            # Process line by line
            lines = part.split("\n")
            in_headers = True

            for line in lines:
                if in_headers:
                    if line.startswith("Content-"):
                        headers.append(line)
                    elif not line.strip():
                        in_headers = False
                    continue
                content += line + "\n"

            # Reconstruct part with proper formatting
            formatted_part = "\n".join(headers) + "\n\n" + content.strip()
            formatted_parts.append(formatted_part)

    # Reconstruct full response
    formatted_response = f"\n{boundary}\n".join([""] + formatted_parts + ["--"])

    return formatted_response


def parse_response(response) -> dict:
    json_data = lib.failsafe(lambda: lib.to_dict(response))

    if json_data:
        return json_data

    # Normalize response format first
    normalized_response = normalize_multipart_response(response)

    # Extract boundary dynamically
    boundary_match = re.search(r"--[a-zA-Z0-9\-]+", normalized_response)
    if not boundary_match:
        return dict(
            error=dict(
                code="SHIPPING_SDK_ERROR",
                message="Failed to parse multipart response",
            )
        )

    boundary = boundary_match.group(0).strip()

    # Handle multipart form-data
    parts = normalized_response.split(boundary)
    data = {}

    for part in parts:
        if not part.strip() or part.strip() == "--":
            continue  # Skip empty parts and the final boundary marker

        part_data = {}
        headers_content, content = (
            part.split("\n\n", 1) if "\n\n" in part else (part, "")
        )
        headers: typing.List[str] = headers_content.strip().split("\n")

        # Extract Content-Disposition and Content-Type
        for header in headers:
            if "Content-Type" in header:
                part_data["content_type"] = header.split(":")[1].strip()
            elif "Content-Disposition" in header:
                disposition = header.split(":")[1].strip()
                if "filename=" in disposition:
                    filename = re.search(r'filename="([^"]+)"', disposition)
                    if filename:
                        part_data["filename"] = filename.group(1)
                if "name=" in disposition:
                    name = re.search(r' name="([^"]+)"', disposition)
                    if name:
                        part_data["name"] = name.group(1)

        # Parse content based on type
        if part_data.get("content_type") == "application/json":
            data[part_data["name"]] = {**lib.to_dict(content.strip())}
        elif part_data.get("filename"):
            data[part_data["name"]] = content.strip()  # type: ignore

    return data


def parse_error_response(response) -> dict:
    # Check if the response is JSON
    content = lib.failsafe(lambda: response.read())
    json_data = lib.failsafe(lambda: lib.to_dict(content))

    if json_data:
        return json_data

    # the response is plain text
    return dict(
        error=dict(
            code=response.code,
            message=response.strip(),
        )
    )

def parse_phone_number(number: str) -> typing.Optional[str]:
    if number is None:
        return None

    return number.replace(" ", "").replace("-", "").replace("+", "")[-10:]
