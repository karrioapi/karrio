"""Karrio Canada post client settings."""

import base64
import karrio.lib as lib
import karrio.core.settings as settings


LanguageEnum = lib.units.create_enum("LanguageEnum", ["en", "fr"])


class Settings(settings.Settings):
    """Canada post connection settings."""

    username: str
    password: str
    customer_number: str
    contract_id: str = None
    language: LanguageEnum = "en"  # type: ignore

    @property
    def carrier_name(self):
        return "canadapost"

    @property
    def server_url(self):
        return (
            "https://ct.soa-gw.canadapost.ca"
            if self.test_mode
            else "https://soa-gw.canadapost.ca"
        )

    @property
    def tracking_url(self):
        return (
            "https://www.canadapost-postescanada.ca/track-reperage/"
            + self.language
            + "#/resultList?searchFor={}"
        )

    @property
    def authorization(self):
        pair = "%s:%s" % (self.username, self.password)
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.canadapost.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


def format_ca_postal_code(code: str = None) -> str:
    """Format canadian postal code."""
    return (code or "").replace(" ", "").upper()


def parse_label_references(shipement_response: str) -> dict:
    response = lib.to_element(f"<wrapper>{shipement_response}</wrapper>")
    messages = lib.find_element("message", response)
    links = lib.find_element("link", response)

    href, media = next(
        (
            (link.get("href"), link.get("media-type"))
            for link in links
            if link.get("rel") == "label" and len(messages) == 0
        ),
        (None, None),
    )

    return dict(href=href, media=media)


def parse_submitted_shipment(shipment_response: str, ctx) -> str:
    import karrio.schemas.canadapost.shipment as canadapost

    shipment = lib.to_object(
        canadapost.ShipmentInfoType, lib.to_element(shipment_response)
    )

    return (
        lib.to_xml(
            canadapost.ShipmentRefundRequestType(email=ctx.get("email")),
            namespacedef_='xmlns="http://www.canadapost.ca/ws/shipment-v8"',
            name_="shipment-refund-request",
        )
        if shipment.shipment_status == "transmitted"
        else None
    )
