import karrio.schemas.tnt.shipping_request as tnt
import karrio.schemas.tnt.shipping_response as shipping
import uuid
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.tnt.error as provider_error
import karrio.providers.tnt.utils as provider_utils
import karrio.providers.tnt.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()

    messages = provider_error.parse_error_response(response, settings)
    create: shipping.CREATE = lib.find_element(
        "CREATE", response, element_type=shipping.CREATE, first=True
    )
    shipment = (
        _extract_detail(create, settings, ctx=_response.ctx)
        if getattr(create, "SUCCESS", None) == "Y"
        else None
    )

    return shipment, messages


def _extract_detail(
    detail: shipping.CREATE,
    settings: provider_utils.Settings,
    ctx: dict,
) -> typing.Optional[models.ShipmentDetails]:
    label = ctx.get("label")

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=detail.CONNUMBER,
        shipment_identifier=detail.CONREF,
        docs=models.Documents(label=label),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    payment = payload.payment or models.Payment(paid_by="sender")
    is_document = all([parcel.is_document for parcel in payload.parcels])
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        shipper_country_code=payload.shipper.country_code,
        recipient_country_code=payload.recipient.country_code,
        is_international=(
            payload.shipper.country_code != payload.recipient.country_code
        ),
        initializer=provider_units.shipping_options_initializer,
    )
    ref = payload.parcels[0].reference_number or f"ref_{uuid.uuid4()}"
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
                COLLECTION=tnt.COLLECTION(
                    COLLECTIONADDRESS=None,
                    SHIPDATE=lib.fdatetime(
                        options.shipment_date.state,
                        current_format="%Y-%m-%d",
                        output_format="%d/%m/%Y",
                    ),
                    PREFCOLLECTTIME=None,
                    ALTCOLLECTTIME=None,
                    COLLINSTRUCTIONS=None,
                    CONFIRMATIONEMAILADDRESS=None,
                ),
            ),
            CONSIGNMENT=[
                tnt.CONSIGNMENT(
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
                        CONTYPE=("D" if is_document else "N"),
                        PAYMENTIND=provider_units.PaymentType.map(
                            payment.paid_by
                        ).value,
                        ITEMS=len(packages),
                        TOTALWEIGHT=packages.weight.KG,
                        TOTALVOLUME=packages.volume.m3,
                        CURRENCY=options.currency.state,
                        GOODSVALUE=options.declared_value.state,
                        INSURANCEVALUE=insurance,
                        INSURANCECURRENCY=options.currency.state,
                        DIVISION=None,
                        SERVICE=service,
                        OPTION=[
                            option.code
                            for _, option in options.items()
                            if "division" not in _
                        ],
                        DESCRIPTION=None,
                        DELIVERYINST=None,
                        CUSTOMCONTROLIN=None,
                        HAZARDOUS=None,
                        UNNUMBER=None,
                        PACKINGGROUP=None,
                        PACKAGE=[
                            tnt.PACKAGE(
                                ITEMS=package.items.quantity,
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
                                                item.title or item.description or "N/A",
                                                max=35,
                                            ),
                                            WEIGHT=units.Weight(
                                                item.weight,
                                                units.WeightUnit[item.weight_unit],
                                            ).KG,
                                            INVOICEVALUE=item.value_amount,
                                            INVOICEDESC=lib.text(
                                                item.description or item.title,
                                                max=35,
                                            ),
                                            HTS=item.hs_code or item.sku,
                                            COUNTRY=item.origin_country,
                                        )
                                        for item in package.items
                                    ]
                                    if len(package.items) > 0
                                    else None
                                ),
                            )
                            for package in packages
                        ],
                    ),
                )
            ],
        ),
        ACTIVITY=tnt.ACTIVITY(
            CREATE=tnt.CREATE(CONREF=[ref]),
            RATE=tnt.RATE(CONREF=[ref]),
            BOOK=tnt.BOOK(CONREF=[ref]),
            SHIP=tnt.SHIP(CONREF=[ref]),
            PRINT=tnt.PRINT(
                REQUIRED=tnt.REQUIRED(CONREF=[ref]),
                CONNOTE=tnt.CONNOTE(CONREF=[ref]),
                LABEL=tnt.LABEL(CONREF=[ref]),
                MANIFEST=tnt.MANIFEST(CONREF=[ref]),
                INVOICE=tnt.INVOICE(CONREF=[ref]),
                EMAILTO=(
                    tnt.EMAILTO(
                        type_=None,
                        valueOf_=(
                            options.email_notification_to.state or recipient.email
                        ),
                    )
                    if (
                        options.email_notification.state
                        and any([options.email_notification_to.state, recipient.email])
                    )
                    else None
                ),
                EMAILFROM=settings.connection_config.email_from.state,
            ),
            SHOW_GROUPCODE=tnt.SHOW_GROUPCODE(),
        ),
    )

    return lib.Serializable(request, lib.to_xml, dict(payload=payload))
