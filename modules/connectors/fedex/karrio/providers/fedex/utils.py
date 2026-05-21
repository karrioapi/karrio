import karrio.schemas.fedex.shipping_request as shipping_request
import karrio.schemas.fedex.tracking_document_request as fedex
import gzip
import typing
import karrio.lib as lib
import karrio.core as core
import karrio.core.models as models
import karrio.core.units as units


class Settings(core.Settings):
    """FedEx connection settings."""

    api_key: str = None
    secret_key: str = None
    account_number: str = None
    track_api_key: str = None
    track_secret_key: str = None

    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
    id: str = None

    @property
    def carrier_name(self):
        return "fedex"

    @property
    def server_url(self):
        return (
            "https://apis-sandbox.fedex.com"
            if self.test_mode
            else "https://apis.fedex.com"
        )

    @property
    def tracking_url(self):
        return "https://www.fedex.com/fedextrack/?trknbr={}"

    @property
    def default_currency(self) -> typing.Optional[str]:
        return lib.units.CountryCurrency.map(self.account_country_code).value

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.fedex.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


def get_proof_of_delivery(tracking_number: str, settings: Settings):
    import karrio.providers.fedex.error as error

    request = fedex.TrackingDocumentRequestType(
        trackDocumentSpecification=[
            fedex.TrackDocumentSpecificationType(
                trackingNumberInfo=fedex.TrackingNumberInfoType(
                    trackingNumber=tracking_number
                )
            )
        ],
        trackDocumentDetail=fedex.TrackDocumentDetailType(
            documentType="SIGNATURE_PROOF_OF_DELIVERY",
            documentFormat="PNG",
        ),
    )
    response = lib.to_dict(
        lib.request(
            url=f"{settings.server_url}/track/v1/trackingdocuments",
            trace=settings.trace_as("json"),
            data=lib.to_json(request),
            method="POST",
            decoder=parse_response,
            on_error=lambda b: parse_response(b.read()),
        )
    )

    messages = error.parse_error_response(response, settings)

    if any(messages):
        return None

    return lib.failsafe(
        lambda: lib.bundle_base64(response["output"]["documents"], format="PNG")
    )


def parse_response(binary_string):
    content = lib.failsafe(lambda: gzip.decompress(binary_string)) or binary_string
    return lib.decode(content)


def state_code(address: lib.units.ComputedAddress) -> str:
    if address.state_code is None:
        return None

    return (
        "PQ"
        if address.state_code.lower() == "qc" and address.country_code == "CA"
        else address.state_code
    )


# Max lengths sourced from FedEx API spec (vendor/ship-api.json, CustomerReference schema).
# Note: CUSTOMER_REFERENCE allows 40 chars for Express but only 30 for Ground.
# We use the conservative Ground limit (30) to ensure all service types work correctly.
CUSTOMER_REFERENCE_MAX_LENGTH = {
    "CUSTOMER_REFERENCE": 30,
    "DEPARTMENT_NUMBER": 30,
    "INVOICE_NUMBER": 30,
    "P_O_NUMBER": 30,
    "RMA_ASSOCIATION": 20,
}


def build_customer_reference(
    reference_type: str,
    value: typing.Optional[str],
) -> typing.Optional[shipping_request.CustomerReferenceType]:
    parsed_value = lib.text(
        value,
        max=CUSTOMER_REFERENCE_MAX_LENGTH.get(reference_type, 30),
    )

    if not any(parsed_value or ""):
        return None

    return shipping_request.CustomerReferenceType(
        customerReferenceType=reference_type,
        value=parsed_value,
    )


def collect_customer_references(
    payload: models.ShipmentRequest,
    customs: models.Customs,
    options: units.ShippingOptions,
    package: typing.Optional[units.Package] = None,
) -> typing.Dict[str, typing.List[shipping_request.CustomerReferenceType]]:
    raw_options = payload.options or {}
    invoice_number = lib.text(customs.invoice) or lib.text(options.invoice_number.state)

    references = {
        "CUSTOMER_REFERENCE": build_customer_reference(
            "CUSTOMER_REFERENCE",
            payload.reference,
        ),
        "DEPARTMENT_NUMBER": build_customer_reference(
            "DEPARTMENT_NUMBER",
            lib.text(
                raw_options.get("fedex_department_number")
                or raw_options.get("department_number")
            ),
        ),
        "INVOICE_NUMBER": build_customer_reference("INVOICE_NUMBER", invoice_number),
        "P_O_NUMBER": build_customer_reference(
            "P_O_NUMBER",
            lib.text(
                package.reference_number if package is not None else None
            )
            or lib.text(raw_options.get("fedex_po_number") or raw_options.get("po_number")),
        ),
        "RMA_ASSOCIATION": build_customer_reference(
            "RMA_ASSOCIATION",
            lib.text(
                raw_options.get("fedex_rma_association")
                or raw_options.get("rma_association")
            ),
        ),
    }

    return {
        "commercial_invoice": [
            reference
            for key in ["INVOICE_NUMBER", "CUSTOMER_REFERENCE", "DEPARTMENT_NUMBER"]
            for reference in [references[key]]
            if reference is not None
        ],
        "package": [
            reference
            for key in [
                "CUSTOMER_REFERENCE",
                "DEPARTMENT_NUMBER",
                "P_O_NUMBER",
                "RMA_ASSOCIATION",
            ]
            for reference in [references[key]]
            if reference is not None
        ],
    }
