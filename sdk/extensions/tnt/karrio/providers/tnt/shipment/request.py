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

import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.tnt.units as provider_units
import karrio.providers.tnt.utils as provider_utils


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    ref = f"ref_{uuid4()}"
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
            CONSIGNMENT=CONSIGNMENT(
                CONREF=ref,
                DETAILS=DETAILS(
                    RECEIVER=RECEIVER(
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
                EMAILTO=recipient.email,
                EMAILFROM=shipper.email,
            ),
            SHOW_GROUPCODE=None,
        ),
    )

    return lib.Serializable(request, lib.to_xml)
