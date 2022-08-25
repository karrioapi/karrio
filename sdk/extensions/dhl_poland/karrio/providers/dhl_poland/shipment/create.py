from dhl_poland_lib.services import (
    Address,
    Addressat,
    ArrayOfCustomsitemdata,
    ArrayOfPackage,
    ArrayOfService,
    Billing,
    CreateShipmentRequest,
    CustomsAgreementData,
    CustomsData,
    CustomsItemData,
    Package,
    PreavisoContact,
    ReceiverAddress,
    ReceiverAddressat,
    Ship,
    ShipmentInfo,
    ShipmentTime,
    createShipment,
    Service as DhlService,
    CreateShipmentResponse,
)

import time
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dhl_poland.error as provider_error
import karrio.providers.dhl_poland.units as provider_units
import karrio.providers.dhl_poland.utils as provider_utils


def parse_shipment_response(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    errors = provider_error.parse_error_response(response, settings)
    shipment = (
        _extract_details(response, settings)
        if lib.find_element("createShipmentResult", response, first=True) is not None
        else None
    )

    return shipment, errors


def _extract_details(
    response: lib.Element,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipment = lib.find_element(
        "createShipmentResult", response, CreateShipmentResponse, first=True
    )

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.shipmentNotificationNumber,
        shipment_identifier=shipment.shipmentTrackingNumber,
        docs=models.Documents(
            label=shipment.label.labelContent,
            invoice=shipment.label.fvProformaContent,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable[str]:
    packages = lib.to_packages(
        payload.parcels,
        required=["weight"],
        package_option_type=provider_units.ShippingOption,
    )
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    customs = lib.to_customs_info(payload.customs, weight_unit=packages.weight_unit)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    is_international = shipper.country_code != recipient.country_code
    service_type = provider_units.Service.map(payload.service).value_or_key or (
        provider_units.Service.dhl_poland_polska.value
        if is_international
        else provider_units.Service.dhl_poland_09.value
    )
    label_type = provider_units.LabelType.map(payload.label_type or "PDF").value
    payment = payload.payment or models.Payment()
    quantity = len(customs.commodities or []) if customs.is_defined else 1

    request = lib.create_envelope(
        body_content=createShipment(
            authData=settings.auth_data,
            shipment=CreateShipmentRequest(
                shipmentInfo=ShipmentInfo(
                    wayBill=None,
                    dropOffType="REGULAR_PICKUP",
                    serviceType=service_type,
                    billing=Billing(
                        shippingPaymentType=provider_units.PaymentType[
                            payment.paid_by
                        ].value,
                        billingAccountNumber=(
                            payment.account_number or settings.account_number
                        ),
                        paymentType="BANK_TRANSFER",
                        costsCenter=None,
                    ),
                    specialServices=(
                        ArrayOfService(
                            item=[
                                DhlService(
                                    serviceType=option.code,
                                    serviceValue=lib.to_money(option.state),
                                    textInstruction=None,
                                    collectOnDeliveryForm=None,
                                )
                                for _, option in options.items()
                            ]
                        )
                        if any(options.items())
                        else None
                    ),
                    shipmentTime=(
                        ShipmentTime(
                            shipmentDate=(
                                options.shipment_date.state or time.strftime("%Y-%m-%d")
                            ),
                            shipmentStartHour="10:00",
                            shipmentEndHour="10:00",
                        )
                    ),
                    labelType=label_type,
                ),
                content=payload.parcels[0].content or "N/A",
                comment=None,
                reference=payload.reference,
                ship=Ship(
                    shipper=Addressat(
                        preaviso=(
                            PreavisoContact(
                                personName=shipper.person_name,
                                phoneNumber=shipper.phone_number,
                                emailAddress=shipper.email,
                            )
                            if any(
                                [
                                    shipper.person_name,
                                    shipper.phone_number,
                                    shipper.email,
                                ]
                            )
                            else None
                        ),
                        contact=(
                            PreavisoContact(
                                personName=shipper.person_name,
                                phoneNumber=shipper.phone_number,
                                emailAddress=shipper.email,
                            )
                            if any(
                                [
                                    shipper.person_name,
                                    shipper.phone_number,
                                    shipper.email,
                                ]
                            )
                            else None
                        ),
                        address=Address(
                            name=(shipper.company_name or shipper.person_name),
                            postalCode=(shipper.postal_code or "").replace("-", ""),
                            city=shipper.city,
                            street=shipper.address_line,
                            houseNumber=(shipper.street_number or "N/A"),
                            apartmentNumber=shipper.suite,
                        ),
                    ),
                    receiver=ReceiverAddressat(
                        preaviso=(
                            PreavisoContact(
                                personName=recipient.person_name,
                                phoneNumber=recipient.phone_number,
                                emailAddress=recipient.email,
                            )
                            if any(
                                [
                                    recipient.person_name,
                                    recipient.phone_number,
                                    recipient.email,
                                ]
                            )
                            else None
                        ),
                        contact=(
                            PreavisoContact(
                                personName=recipient.person_name,
                                phoneNumber=recipient.phone_number,
                                emailAddress=recipient.email,
                            )
                            if any(
                                [
                                    recipient.person_name,
                                    recipient.phone_number,
                                    recipient.email,
                                ]
                            )
                            else None
                        ),
                        address=ReceiverAddress(
                            country=recipient.country_code,
                            isPackstation=None,
                            isPostfiliale=None,
                            postnummer=None,
                            addressType=("C" if recipient.residential else "B"),
                            name=(recipient.company_name or recipient.person_name),
                            postalCode=(recipient.postal_code or "").replace("-", ""),
                            city=recipient.city,
                            street=recipient.address_line,
                            houseNumber=(shipper.street_number or "N/A"),
                            apartmentNumber=shipper.suite,
                        ),
                    ),
                    neighbour=None,
                ),
                pieceList=ArrayOfPackage(
                    item=[
                        Package(
                            type_=provider_units.PackagingType[
                                package.packaging_type or "your_packaging"
                            ].value,
                            euroReturn=None,
                            weight=package.weight.KG,
                            width=package.width.CM,
                            height=package.height.CM,
                            length=package.length.CM,
                            quantity=quantity,
                            nonStandard=None,
                            blpPieceId=None,
                        )
                        for package in packages
                    ]
                ),
                customs=(
                    CustomsData(
                        customsType="S",
                        firstName=getattr(
                            getattr(customs.duty, "bil_to", shipper.company_name),
                            "company_name",
                            "N/A",
                        ),
                        secondaryName=getattr(
                            getattr(customs.duty, "bil_to", shipper.person_name),
                            "person_name",
                            "N/A",
                        ),
                        costsOfShipment=(
                            getattr(customs.duty, "declared_value", None)
                            or options.declard_value.state
                        ),
                        currency=(
                            getattr(customs.duty, "currency", None)
                            or options.currency.state
                        ),
                        nipNr=customs.options.nip_number.state,
                        eoriNr=customs.options.eori_number.state,
                        vatRegistrationNumber=customs.options.vat_registration_number.state,
                        categoryOfItem=provider_units.CustomsContentType[
                            customs.content_type or "other"
                        ].value,
                        invoiceNr=customs.invoice,
                        invoice=None,
                        invoiceDate=customs.invoice_date,
                        countryOfOrigin=shipper.country_code,
                        additionalInfo=None,
                        grossWeight=packages.weight.KG,
                        customsItem=(
                            ArrayOfCustomsitemdata(
                                item=[
                                    CustomsItemData(
                                        nameEn=item.description or "N/A",
                                        namePl=item.description or "N/A",
                                        quantity=item.quantity,
                                        weight=units.Weight(
                                            item.weight,
                                            units.WeightUnit[item.weight_unit or "KG"],
                                        ).KG,
                                        value=item.value_amount,
                                        tariffCode=item.hs_code or item.sku,
                                    )
                                    for item in customs.commodities
                                ]
                            )
                            if any(customs.commodities)
                            else None
                        ),
                        customAgreements=CustomsAgreementData(
                            notExceedValue=True,
                            notProhibitedGoods=True,
                            notRestrictedGoods=True,
                        ),
                    )
                    if customs.is_defined
                    else None
                ),
            ),
        )
    )

    return lib.Serializable(
        request,
        lambda req: settings.serialize(req, "createShipment", settings.server_url),
    )
