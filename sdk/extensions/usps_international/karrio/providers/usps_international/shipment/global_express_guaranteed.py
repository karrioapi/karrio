from usps_lib.evs_gxg_get_label_response import eVSGXGGetLabelResponse
from usps_lib.evs_gxg_get_label_request import (
    eVSGXGGetLabelRequest,
    ShippingContentsType,
    ItemDetailType,
)

import time
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.usps_international.error as provider_error
import karrio.providers.usps_international.units as provider_units
import karrio.providers.usps_international.utils as provider_utils


def parse_shipment_response(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    errors = provider_error.parse_error_response(response, settings)
    details = _extract_details(response, settings)

    return details, errors


def _extract_details(
    response: lib.Element, settings: provider_utils.Settings
) -> models.ShipmentDetails:
    shipment = lib.to_object(eVSGXGGetLabelResponse, response)
    tracking_number = shipment.USPSBarcodeNumber or shipment.FedExBarcodeNumber

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=tracking_number,
        shipment_identifier=tracking_number,
        docs=models.Documents(label=shipment.LabelImage),
    )


def shipment_request(
    payload: models.ShipmentRequest, settings: provider_utils.Settings
) -> lib.Serializable[eVSGXGGetLabelRequest]:
    package = lib.to_packages(
        payload.parcels,
        package_option_type=provider_units.ShippingOption,
        max_weight=units.Weight(70, units.WeightUnit.LB),
    ).single
    options = lib.to_shipping_options(
        payload.options,
        package_options=package.options,
        initializer=provider_units.shipping_options_initializer,
    )

    customs = lib.to_customs_info(payload.customs or models.Customs(commodities=[]))
    incoterm = provider_units.Incoterm[customs.incoterm or "OTHER"].value

    request = eVSGXGGetLabelRequest(
        USERID=settings.username,
        PASSWORD=settings.password,
        Option=None,
        Revision=2,
        ImageParameters=None,
        FromFirstName=(customs.signer or payload.shipper.person_name or "N/A"),
        FromMiddleInitial=None,
        FromLastName=payload.shipper.person_name,
        FromFirm=payload.shipper.company_name or "N/A",
        FromAddress1=payload.shipper.address_line1,
        FromAddress2=payload.shipper.address_line2,
        FromUrbanization=None,
        FromCity=payload.shipper.city,
        FromState=lib.to_state_name(payload.shipper.state_code, country="US"),
        FromZIP5=lib.to_zip5(payload.shipper.postal_code),
        FromZIP4=lib.to_zip4(payload.shipper.postal_code),
        FromPhone=payload.shipper.phone_number,
        ShipFromZIP=None,
        ToFirstName=None,
        ToLastName=payload.recipient.person_name,
        ToFirm=payload.recipient.company_name or "N/A",
        ToAddress1=payload.recipient.address_line1,
        ToAddress2=payload.recipient.address_line2,
        ToAddress3=None,
        ToPostalCode=payload.recipient.postal_code,
        ToPhone=payload.recipient.phone_number,
        RecipientEMail=payload.recipient.email,
        ToDPID="000",  # supposedly required test and find a solution
        ToProvince=payload.recipient.state_code,
        ToTaxID=(payload.recipient.federal_tax_id or payload.recipient.state_tax_id),
        Container=provider_units.PackagingType[
            package.packaging_type or "package"
        ].value,
        ContentType=("DOCUMENTS" if package.parcel.is_document else "NON-DOC"),
        ShippingContents=ShippingContentsType(
            ItemDetail=[
                ItemDetailType(
                    Description=item.description,
                    Commodity=item.description or "N/A",
                    Quantity=item.quantity,
                    UnitValue=item.value_amount,
                    NetPounds=units.Weight(
                        item.weight, units.WeightUnit[item.weight_unit or "LB"]
                    ).LB,
                    NetOunces=units.Weight(
                        item.weight, units.WeightUnit[item.weight_unit or "LB"]
                    ).OZ,
                    UnitOfMeasure=None,
                    HSTariffNumber=item.hs_code or item.sku,
                    CountryofManufacture=lib.to_country_name(item.origin_country),
                )
                for item in customs.commodities
            ]
        ),
        PurposeOfShipment=provider_units.ContentType[
            customs.content_type or "other"
        ].value,
        PartiesToTransaction=None,
        Agreement=("N" if customs.certify else "Y"),
        Postage=None,
        InsuredValue=provider_units.ShippingOption.insurance_from(
            options, "global_express"
        ),
        GrossPounds=package.weight.LB,
        GrossOunces=package.weight.OZ,
        Length=package.length.IN,
        Width=package.width.IN,
        Height=package.height.IN,
        Girth=(package.girth.value if package.packaging_type == "tube" else None),
        Shape=None,
        CIRequired=customs.commercial_invoice or None,
        InvoiceDate=lib.fdatetime(customs.invoice_date, output_format="%m/%d/%Y"),
        InvoiceNumber=customs.invoice,
        CustomerOrderNumber=None,
        CustOrderNumber=None,
        TermsDelivery=incoterm,
        TermsDeliveryOther=(
            (customs.incoterm or incoterm) if incoterm == "OTHER" else None
        ),
        PackingCost=None,
        CountryUltDest=lib.to_country_name(payload.recipient.country_code),
        CIAgreement=customs.commercial_invoice or None,
        ImageType="PDF",
        ImageLayout=None,
        CustomerRefNo=None,
        CustomerRefNo2=None,
        ShipDate=lib.fdatetime(
            (options.shipment_date.state or time.strftime("%Y-%m-%d")),
            current_format="%Y-%m-%d",
            output_format="%m/%d/%Y",
        ),
        HoldForManifest=None,
        PriceOptions=None,
        CommercialShipment=customs.commercial_invoice or None,
        BuyerRecipient=(
            customs.commercial_invoice or None
        ),  # Consider recipient as buyer for commercial shipment
        TermsPayment=("Net 50" if customs.commercial_invoice else None),
        ActionCode=None,
        OptOutOfSPE=None,
        PermitNumber=None,
        AccountZipCode=None,
        Machinable=(options.usps_option_machinable_item.state or False),
        DestinationRateIndicator="I",
        MID=settings.mailer_id,
        LogisticsManagerMID=settings.logistics_manager_mailer_id,
        CRID=settings.customer_registration_id,
        VendorCode=None,
        VendorProductVersionNumber=None,
        OverrideMID=None,
        ChargebackCode=None,
    )

    return lib.Serializable(request, lib.to_xml)
