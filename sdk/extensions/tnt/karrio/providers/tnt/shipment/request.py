from uuid import uuid4
from tnt_lib.shipment_request import (
    ESHIPPER,
    CONSIGNMENTBATCH,
    LOGIN,
    SENDER,
    CONSIGNMENT,
    ACTIVITY,
    CREATE,
    BOOK,
    SHIP,
    PRINT,
    LABEL,
    CONNOTE,
    MANIFEST,
    INVOICE,
    DETAILS,
    RECEIVER,
    PACKAGE,
    ARTICLE,
    RATE,
    REQUIRED,
)

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.tnt.error as provider_error
import karrio.providers.tnt.units as provider_units
import karrio.providers.tnt.utils as provider_utils


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable[ESHIPPER]:
    ref = f"ref_{uuid4()}"
    package = lib.to_packages(payload.parcels).single
    service = provider_units.ShipmentService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=package.options,
        initializer=provider_units.shipping_options_initializer,
    )

    payment = payload.payment or models.Payment(paid_by="sender")
    insurance = options.tnt_insurance.state

    request = ESHIPPER(
        LOGIN=LOGIN(
            COMPANY=settings.username,
            PASSWORD=settings.password,
            APPID="EC",
            APPVERSION=3.1,
        ),
        CONSIGNMENTBATCH=CONSIGNMENTBATCH(
            GROUPCODE=None,
            SENDER=SENDER(
                COMPANYNAME=payload.shipper.company_name,
                STREETADDRESS1=payload.shipper.address_line1,
                STREETADDRESS2=payload.shipper.address_line2,
                STREETADDRESS3=None,
                CITY=payload.shipper.city,
                PROVINCE=payload.shipper.state_code,
                POSTCODE=payload.shipper.postal_code,
                COUNTRY=payload.shipper.country_code,
                ACCOUNT=settings.account_number,
                VAT=(payload.shipper.state_tax_id or payload.shipper.federal_tax_id),
                CONTACTNAME=payload.shipper.person_name,
                CONTACTDIALCODE=None,
                CONTACTTELEPHONE=payload.shipper.phone_number,
                CONTACTEMAIL=payload.shipper.email,
                COLLECTION=None,
            ),
            CONSIGNMENT=CONSIGNMENT(
                CONREF=ref,
                DETAILS=DETAILS(
                    RECEIVER=RECEIVER(
                        COMPANYNAME=payload.recipient.company_name,
                        STREETADDRESS1=payload.recipient.address_line1,
                        STREETADDRESS2=payload.recipient.address_line2,
                        STREETADDRESS3=None,
                        CITY=payload.recipient.city,
                        PROVINCE=payload.recipient.state_code,
                        POSTCODE=payload.recipient.postal_code,
                        COUNTRY=payload.recipient.country_code,
                        VAT=(
                            payload.recipient.state_tax_id
                            or payload.recipient.federal_tax_id
                        ),
                        CONTACTNAME=payload.recipient.person_name,
                        CONTACTDIALCODE=None,
                        CONTACTTELEPHONE=payload.recipient.phone_number,
                        CONTACTEMAIL=payload.recipient.email,
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
                    PACKAGE=PACKAGE(
                        ITEMS=1,
                        DESCRIPTION=package.parcel.description,
                        LENGTH=package.length.M,
                        HEIGHT=package.height.M,
                        WIDTH=package.width.M,
                        WEIGHT=package.weight.KG,
                        ARTICLE=(
                            [
                                ARTICLE(
                                    ITEMS=article.quantity,
                                    DESCRIPTION=article.description,
                                    WEIGHT=units.Weight(
                                        article.weight,
                                        units.WeightUnit[article.weight_unit],
                                    ).KG,
                                    INVOICEVALUE=article.value_amount,
                                    INVOICEDESC=article.description,
                                    HTS=article.hs_code or article.sku,
                                    COUNTRY=article.origin_country,
                                )
                                for article in payload.customs.commodities
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
        ACTIVITY=ACTIVITY(
            CREATE=CREATE(CONREF=ref),
            RATE=RATE(CONREF=ref),
            BOOK=BOOK(CONREF=ref),
            SHIP=SHIP(CONREF=ref),
            PRINT=PRINT(
                REQUIRED=REQUIRED(CONREF=ref),
                CONNOTE=CONNOTE(CONREF=ref),
                LABEL=LABEL(CONREF=ref),
                MANIFEST=MANIFEST(CONREF=ref),
                INVOICE=INVOICE(CONREF=ref),
                EMAILTO=payload.recipient.email,
                EMAILFROM=payload.shipper.email,
            ),
            SHOW_GROUPCODE=None,
        ),
    )

    return lib.Serializable(request, lib.to_xml)
