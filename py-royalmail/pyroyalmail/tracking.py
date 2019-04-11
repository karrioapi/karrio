"""Royal Mail Tracking Service Datatypes definition module."""

import attr
from typing import List
from jstruct import JList, JStruct


@attr.s(auto_attribs=True)
class AllInternationalPostalProviderDef:
    url: str = None
    title: str = None
    description: str = None


@attr.s(auto_attribs=True)
class AllSummaryDef:
    unique_item_id: str = None
    one_d_barcode: str = None
    product_id: str = None
    product_name: str = None
    product_description: str = None
    product_category: str = None
    destination_country_code: str = None
    destination_country_name: str = None
    origin_country_code: str = None
    origin_country_name: str = None
    last_event_code: str = None
    last_event_name: str = None
    last_event_date_time: str = None
    last_event_location_name: str = None
    status_description: str = None
    status_category: str = None
    status_help_text: str = None
    summary_line: str = None
    international_postal_provider: str = None


@attr.s(auto_attribs=True)
class ErrorsDef:
    error_code: str = None
    error_description: str = None
    error_cause: str = None
    error_resolution: str = None


@attr.s(auto_attribs=True)
class ErrorResponse:
    http_code: str = None
    http_message: str = None
    more_information: str = None
    errors: List[ErrorsDef] = JList[ErrorsDef]


@attr.s(auto_attribs=True)
class EventsEstimatedDeliveryDef:
    _date: str = None
    start_of_estimated_window: str = None
    end_of_estimated_window: str = None


@attr.s(auto_attribs=True)
class EventsEventsDef:
    event_code: str = None
    event_name: str = None
    event_date_time: str = None
    location_name: str = None


@attr.s(auto_attribs=True)
class EventsLinksDef:
    recipient_name: str = None
    signature_date_time: str = None
    image_id: str = None


@attr.s(auto_attribs=True)
class EventsSignatureDef:
    recipient_name: str = None
    signature_date_time: str = None
    image_id: str = None


@attr.s(auto_attribs=True)
class EventsMailPiecesDef:
    mail_piece_id: str = None
    carrier_short_name: str = None
    carrier_full_name: str = None
    summary: AllSummaryDef = JStruct[AllSummaryDef]
    signature: EventsSignatureDef = JStruct[EventsSignatureDef]
    estimated_delivery: EventsEstimatedDeliveryDef = JStruct[EventsEstimatedDeliveryDef]
    events: List[EventsEventsDef] = JList[EventsEventsDef]
    links: EventsLinksDef = JStruct[EventsLinksDef]


@attr.s(auto_attribs=True)
class EventsSuccessResponse:
    mail_pieces: EventsMailPiecesDef = JStruct[EventsMailPiecesDef]


@attr.s(auto_attribs=True)
class IntegrationFooterDef:
    errors: List[ErrorsDef] = JStruct[ErrorsDef]


@attr.s(auto_attribs=True)
class EventsSuccessOutput:
    mail_pieces: EventsMailPiecesDef = JStruct[EventsMailPiecesDef]
    integration_footer: IntegrationFooterDef = JStruct[IntegrationFooterDef]


@attr.s(auto_attribs=True)
class MailPieceIdDef:
    mail_piece_id: str = None
    status: str = None


@attr.s(auto_attribs=True)
class SignatureSignatureDef:
    unique_item_id: str = None
    one_d_barcode: str = None
    recipient_name: str = None
    signature_date_time: str = None
    image_format: str = None
    image_id: str = None
    height: int = None
    width: int = None
    image: str = None


@attr.s(auto_attribs=True)
class SubLinksEventsDef:
    href: str = None
    title: str = None
    description: str = None


@attr.s(auto_attribs=True)
class SubLinksRedeliveryDef:
    href: str = None
    title: str = None
    description: str = None


@attr.s(auto_attribs=True)
class SubLinksSignatureDef:
    href: str = None
    title: str = None
    description: str = None


@attr.s(auto_attribs=True)
class SubLinksSummaryDef:
    href: str = None
    title: str = None
    description: str = None


@attr.s(auto_attribs=True)
class SummaryErrorResponse:
    mail_pieces: List[MailPieceIdDef] = JList[MailPieceIdDef]
    http_code: str = None
    http_message: str = None
    moreinformation: str = None
    errors: List[ErrorsDef] = JList[ErrorsDef]


@attr.s(auto_attribs=True)
class SummaryLinksDef:
    events: SubLinksEventsDef = JStruct[SubLinksEventsDef]


@attr.s(auto_attribs=True)
class SummaryMailPiecesDef:
    mail_piece_id: str = None
    status: str = None
    carrier_short_name: str = None
    carrier_full_name: str = None
    summary: AllSummaryDef = JStruct[AllSummaryDef]
    links: SummaryLinksDef = JStruct[SummaryLinksDef]
    error: ErrorsDef = JStruct[ErrorsDef]


@attr.s(auto_attribs=True)
class SummarySuccessOutput:
    mail_pieces: List[SummaryMailPiecesDef] = JList[SummaryMailPiecesDef]
    integration_footer: IntegrationFooterDef = JStruct[IntegrationFooterDef]


@attr.s(auto_attribs=True)
class SummarySuccessResponse:
    mail_pieces: List[SummaryMailPiecesDef] = JList[SummaryMailPiecesDef]


@attr.s(auto_attribs=True)
class SignatureLinksDef:
    events: SubLinksEventsDef = JStruct[SubLinksEventsDef]
    summary: SubLinksSummaryDef = JStruct[SubLinksSummaryDef]


@attr.s(auto_attribs=True)
class SignatureMailPiecesDef:
    mail_piece_id: str = None
    carrier_short_name: str = None
    carrier_full_name: str = None
    signature: SignatureSignatureDef = JStruct[SignatureSignatureDef]
    links: SignatureLinksDef = JStruct[SignatureLinksDef]


@attr.s(auto_attribs=True)
class SignatureSuccessOutput:
    mail_pieces: SignatureMailPiecesDef = JStruct[SignatureMailPiecesDef]
    integration_footer: IntegrationFooterDef = JStruct[IntegrationFooterDef]


@attr.s(auto_attribs=True)
class SignatureSuccessResponse:
    mail_pieces: SignatureMailPiecesDef = JStruct[SignatureMailPiecesDef]