"""USPS connection settings."""

import re
import typing
import karrio.lib as lib
import karrio.core as core

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


class ConnectionConfig(lib.Enum):
    permit_ZIP = lib.OptionEnum("permit_ZIP")
    permit_number = lib.OptionEnum("permit_number")
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)


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
