import fedex_lib.shipping_request as fedex
import typing
import base64
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.fedex.error as provider_error
import karrio.providers.fedex.units as provider_units
import karrio.providers.fedex.utils as provider_utils


NOTIFICATION_EVENTS = [
    "ON_DELIVERY",
    "ON_ESTIMATED_DELIVERY",
    "ON_EXCEPTION",
    "ON_SHIPMENT",
    "ON_TENDER",
]


def parse_shipment_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    details = lib.find_element("CompletedPackageDetails", response)
    documents = lib.find_element("ShipmentDocuments", response)

    shipment = (
        _extract_details((details, documents), settings) if len(details) > 0 else None
    )
    return shipment, provider_error.parse_error_response(response, settings)


def _extract_details(
    details: typing.Tuple[typing.List[lib.Element], typing.List[lib.Element]],
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    pieces, docs = details
    tracking_numbers = [
        getattr(lib.find_element("TrackingNumber", piece, first=True), "text", None)
        for piece in pieces
    ]
    [master_id, *_] = tracking_numbers

    labels = [
        getattr(lib.find_element("Image", piece, first=True), "text", None)
        for piece in pieces
    ]
    label_type = getattr(
        lib.find_element("ImageType", pieces[0], first=True), "text", None
    )

    invoices = [
        getattr(lib.find_element("Image", doc, first=True), "text", None)
        for doc in docs
    ]
    doc_type = (
        getattr(lib.find_element("ImageType", docs[0], first=True), "text", None)
        if len(docs) > 0
        else "PDF"
    )

    label = labels[0] if len(labels) == 1 else lib.bundle_base64(labels, label_type)
    invoice = (
        invoices[0] if len(invoices) == 1 else lib.bundle_base64(invoices, doc_type)
    )

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=master_id,
        shipment_identifier=master_id,
        docs=models.Documents(
            label=label,
            **({"invoice": invoice} if invoice else {}),
        ),
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(master_id),
            tracking_numbers=tracking_numbers,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(
        payload.parcels,
        provider_units.PackagePresets,
        required=["weight"],
        package_option_type=provider_units.ShippingOption,
    )
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    weight_unit, dim_unit = (
        provider_units.COUNTRY_PREFERED_UNITS.get(payload.shipper.country_code)
        or packages.compatible_units
    )
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=weight_unit.value,
    )

    payment = payload.payment or models.Payment()
    service = provider_units.ServiceType.map(payload.service).value_or_key
    label_type, label_format = provider_units.LabelType.map(
        payload.label_type or "PDF_4x6"
    ).value

    requests = [
        fedex.ShippingRequestType(
            mergeLabelDocOption="LABELS_AND_DOCS",
            requestedShipment=fedex.RequestedShipmentType(
                shipDatestamp=None,
                totalDeclaredValue=None,
                shipper=None,
                soldTo=None,
                recipients=None,
                recipientLocationNumber=None,
                pickupType=None,
                serviceType=None,
                packagingType=None,
                totalWeight=None,
                origin=None,
                shippingChargesPayment=None,
                shipmentSpecialServices=None,
                emailNotificationDetail=None,
                expressFreightDetail=None,
                variableHandlingChargeDetail=None,
                customsClearanceDetail=None,
                smartPostInfoDetail=None,
                blockInsightVisibility=None,
                labelSpecification=None,
                shippingDocumentSpecification=None,
                rateRequestType=None,
                preferredCurrency=None,
                totalPackageCount=None,
                masterTrackingId=None,
                requestedPackageLineItems=None,
            ),
            labelResponseOptions="LABEL",
            accountNumber=fedex.AccountNumberType(value=settings.account_number),
            shipAction="CONFIRM",
            processingOptionType="SYNCHRONOUS_ONLY",
            oneLabelAtATime=None,
        )
        for package_index, package in enumerate(packages, 1)
    ]

    return lib.Serializable(requests, lib.to_dict)
