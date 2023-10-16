import karrio.schemas.tnt.shipping_request as tnt
import karrio.schemas.tnt.shipping_response as shipping
import uuid
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.core.units as units
import karrio.providers.tnt.error as provider_error
import karrio.providers.tnt.utils as provider_utils
import karrio.providers.tnt.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[lib.Message]]:
    response = _response.deserialize()

    messages = provider_error.parse_error_response(response, settings)
    activity: shipping.document = lib.find_element(
        "document", response, element_type=shipping.document, first=True
    )
    shipment = (
        _extract_detail(activity, settings)
        if activity is None or activity.CREATE.SUCCESS != "Y"
        else None
    )

    return shipment, messages


def _extract_detail(
    activity: shipping.document,
    settings: provider_utils.Settings,
    ctx: dict,
) -> typing.Optional[models.ShipmentDetails]:
    label = lib.failsafe(lambda: provider_utils.generate_label(activity, settings, ctx))

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=activity.CREATE.CONNUMBER,
        shipment_identifier=activity.CREATE.CONREF,
        docs=models.Documents(label=label),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    ref = f"ref_{uuid.uuid4()}"
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    package = lib.to_packages(payload.parcels).single
    service = provider_units.ShipmentService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=package.options,
        initializer=provider_units.shipping_options_initializer,
    )

    payment = payload.payment or models.Payment(paid_by="sender")
    insurance = options.tnt_insurance.state

    request = tnt.ESHIPPER(
        LOGIN=tnt.LOGIN(
            COMPANY=settings.username,
            PASSWORD=settings.password,
            APPID=settings.connection_config.app_id.state or "EC",
            APPVERSION="3.1",
        ),
        CONSIGNMENTBATCH=tnt.CONSIGNMENTBATCH(
            GROUPCODE=None,
            SENDER=tnt.SENDER(
                COMPANYNAME=shipper.company_name,
                STREETADDRESS1=shipper.address_line1,
                STREETADDRESS2=shipper.address_line2,
                STREETADDRESS3=None,
                CITY=shipper.city,
                PROVINCE=shipper.state_code,
                POSTCODE=shipper.postal_code,
                COUNTRY=shipper.country_code,
                ACCOUNT=settings.account_number,
                VAT=shipper.tax_id,
                CONTACTNAME=shipper.person_name,
                CONTACTDIALCODE=None,
                CONTACTTELEPHONE=shipper.phone_number,
                CONTACTEMAIL=shipper.email,
                COLLECTION=None,
            ),
            CONSIGNMENT=tnt.CONSIGNMENT(
                CONREF=ref,
                DETAILS=tnt.DETAILS(
                    RECEIVER=tnt.RECEIVER(
                        COMPANYNAME=recipient.company_name,
                        STREETADDRESS1=recipient.address_line1,
                        STREETADDRESS2=recipient.address_line2,
                        STREETADDRESS3=None,
                        CITY=recipient.city,
                        PROVINCE=recipient.state_code,
                        POSTCODE=recipient.postal_code,
                        COUNTRY=recipient.country_code,
                        VAT=recipient.tax_id,
                        CONTACTNAME=recipient.person_name,
                        CONTACTDIALCODE=None,
                        CONTACTTELEPHONE=recipient.phone_number,
                        CONTACTEMAIL=recipient.email,
                        ACCOUNT=None,
                        ACCOUNTCOUNTRY=None,
                    ),
                    DELIVERY=None,
                    CONNUMBER=None,
                    CUSTOMERREF=payload.reference,
                    CONTYPE=("D" if package.parcel.is_document else "N"),
                    PAYMENTIND=provider_units.PaymentType[
                        payment.paid_by or "sender"
                    ].value,
                    ITEMS=1,
                    TOTALWEIGHT=package.weight.KG,
                    TOTALVOLUME=package.volume,
                    CURRENCY=options.currency.state,
                    GOODSVALUE=insurance,
                    INSURANCEVALUE=insurance,
                    INSURANCECURRENCY=options.currency.state,
                    DIVISION=None,
                    SERVICE=service,
                    OPTION=[getattr(option, "key", option) for _, option in options],
                    DESCRIPTION=package.parcel.content,
                    DELIVERYINST=None,
                    CUSTOMCONTROLIN=None,
                    HAZARDOUS=None,
                    UNNUMBER=None,
                    PACKINGGROUP=None,
                    PACKAGE=tnt.PACKAGE(
                        ITEMS=1,
                        DESCRIPTION=package.parcel.description,
                        LENGTH=package.length.M,
                        HEIGHT=package.height.M,
                        WIDTH=package.width.M,
                        WEIGHT=package.weight.KG,
                        ARTICLE=(
                            [
                                tnt.ARTICLE(
                                    ITEMS=item.quantity,
                                    DESCRIPTION=lib.text(
                                        item.title or item.description or "N/A", max=35
                                    ),
                                    WEIGHT=units.Weight(
                                        item.weight,
                                        units.WeightUnit[item.weight_unit],
                                    ).KG,
                                    INVOICEVALUE=item.value_amount,
                                    INVOICEDESC=lib.text(
                                        item.title or item.description, max=35
                                    ),
                                    HTS=item.hs_code or item.sku,
                                    COUNTRY=item.origin_country,
                                )
                                for item in payload.customs.commodities
                            ]
                            if payload.customs is not None
                            and any(payload.customs.commodities)
                            else None
                        ),
                    ),
                ),
                CONNUMBER=None,
            ),
        ),
        ACTIVITY=tnt.ACTIVITY(
            CREATE=tnt.CREATE(CONREF=ref),
            RATE=tnt.RATE(CONREF=ref),
            BOOK=tnt.BOOK(CONREF=ref),
            SHIP=tnt.SHIP(CONREF=ref),
            PRINT=tnt.PRINT(
                REQUIRED=tnt.REQUIRED(CONREF=ref),
                CONNOTE=tnt.CONNOTE(CONREF=ref),
                LABEL=tnt.LABEL(CONREF=ref),
                MANIFEST=tnt.MANIFEST(CONREF=ref),
                INVOICE=tnt.INVOICE(CONREF=ref),
                EMAILTO=recipient.email,
                EMAILFROM=shipper.email,
            ),
            SHOW_GROUPCODE=None,
        ),
    )

    return lib.Serializable(
        request,
        lib.to_xml,
        dict(payload=payload),
    )
