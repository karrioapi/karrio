"""Karrio SAPIENT shipment API implementation."""

import karrio.schemas.sapient.shipment_requests as sapient
import karrio.schemas.sapient.shipment_response as shipping

import typing
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.sapient.error as error
import karrio.providers.sapient.utils as provider_utils
import karrio.providers.sapient.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    shipment = lib.identity(
        _extract_details(response, settings, _response.ctx)
        if "Packages" in response
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict = None,
) -> models.ShipmentDetails:
    details = lib.to_object(shipping.ShipmentResponseType, data)
    tracking_numbers = [_.TrackingNumber for _ in details.Packages]
    shipment_ids = [_.ShipmentId for _ in details.Packages]
    label = details.Labels

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_numbers[0],
        shipment_identifier=shipment_ids[0],
        label_type=details.LabelFormat,
        docs=models.Documents(label=label),
        meta=dict(
            carrier_tracking_link=lib.failsafe(lambda: details.Packages[0].TrackingUrl),
            shipment_ids=shipment_ids,
            tracking_numbers=tracking_numbers,
            sapient_shipment_id=shipment_ids[0],
            rate_provider=ctx.get("rate_provider"),
            sapient_carrier_code=ctx.get("carrier_code"),
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    return_address = lib.to_address(payload.return_address)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    carrier_code = lib.identity(
        provider_units.ShippingService.carrier_code(service)
        or settings.sapient_carrier_code
    )
    rate_provider = provider_units.ShippingCarrier.map(carrier_code).name_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    is_intl = payload.recipient.country_code != payload.shipper.country_code
    customs = lib.to_customs_info(
        payload.customs,
        weight_unit="KG",
        shipper=payload.shipper,
        recipient=payload.recipient,
    )
    commodities: units.Products = lib.identity(
        customs.commodities if payload.customs else packages.items
    )
    utc_shipping_date = lib.to_date(
        options.shipping_date.state or datetime.datetime.now(),
        current_format="%Y-%m-%dT%H:%M",
    ).astimezone(datetime.timezone.utc)
    shipping_date = lib.to_next_business_datetime(utc_shipping_date, "%Y-%m-%d")

    # map data to convert karrio model to sapient specific type
    request = sapient.ShipmentRequestType(
        ShipmentInformation=sapient.ShipmentInformationType(
            ContentType=lib.identity("DOX" if packages.is_document else "NDX"),
            Action="Process",
            LabelFormat=provider_units.LabelType.map(payload.label_type).value or "PDF",
            ServiceCode=service or "CRL1",
            DescriptionOfGoods=lib.text(
                packages.description or packages.items.description or "N/A", max=70
            ),
            ShipmentDate=lib.fdate(shipping_date, "%Y-%m-%d %H:%M:%S"),
            CurrencyCode=options.currency.state or "GBP",
            WeightUnitOfMeasure="KG",
            DimensionsUnitOfMeasure="CM",
            ContainerId=options.sapient_container_id.state,
            DeclaredWeight=packages.weight.KG,
            BusinessTransactionType=options.sapient_business_transaction_type.state,
        ),
        Shipper=sapient.ShipperType(
            Address=sapient.AddressType(
                ContactName=shipper.contact or "N/A",
                CompanyName=shipper.company_name,
                ContactEmail=shipper.email,
                ContactPhone=shipper.phone_number,
                Line1=shipper.address_line1,
                Line2=shipper.address_line2,
                Line3=None,
                Town=shipper.city,
                Postcode=shipper.postal_code,
                County=None,
                CountryCode=shipper.country_code,
            ),
            ShippingAccountId=lib.identity(
                settings.shipping_account_id
                or options.connection_config.mailer_id.state
            ),
            ShippingLocationId=None,
            Reference1=payload.reference,
            DepartmentNumber=None,
            EoriNumber=customs.options.eori_number.state,
            VatNumber=lib.identity(
                customs.options.vat_registration_number.state or shipper.tax_id
            ),
        ),
        Destination=sapient.DestinationType(
            Address=sapient.AddressType(
                ContactName=recipient.contact or "N/A",
                CompanyName=recipient.company_name,
                ContactEmail=recipient.email,
                ContactPhone=recipient.phone_number,
                Line1=recipient.address_line1,
                Line2=recipient.address_line2,
                Line3=None,
                Town=recipient.city,
                Postcode=recipient.postal_code,
                County=None,
                CountryCode=recipient.country_code,
            ),
            EoriNumber=None,
            VatNumber=recipient.tax_id,
        ),
        CarrierSpecifics=sapient.CarrierSpecificsType(
            ServiceLevel=settings.connection_config.service_level.state or "02",
            EbayVtn=options.sapient_ebay_vtn.state,
            ServiceEnhancements=[
                sapient.ServiceEnhancementType(
                    Code=option.code,
                    SafeplaceLocation=lib.identity(
                        option.state if option.code == "Safeplace" else None
                    ),
                )
                for _, option in options.items()
                if _ not in provider_units.CUSTOM_OPTIONS
            ],
        ),
        ReturnToSender=lib.identity(
            sapient.ReturnToSenderType(
                Address=sapient.AddressType(
                    ContactName=return_address.contact or "N/A",
                    CompanyName=return_address.company_name,
                    ContactEmail=return_address.email,
                    ContactPhone=return_address.phone_number,
                    Line1=return_address.address_line1,
                    Line2=return_address.address_line2,
                    Line3=None,
                    Town=return_address.city,
                    Postcode=return_address.postal_code,
                    County=None,
                    CountryCode=return_address.country_code,
                ),
            )
            if payload.return_address
            else None
        ),
        Packages=[
            sapient.PackageType(
                PackageType=lib.identity(
                    provider_units.PackagingType.map(package.packaging_type).value
                    or "Parcel"
                ),
                PackageOccurrence=(index if len(packages) > 1 else None),
                DeclaredWeight=package.weight.KG,
                Dimensions=sapient.DimensionsType(
                    Length=package.length.CM,
                    Width=package.width.CM,
                    Height=package.height.CM,
                ),
                DeclaredValue=package.total_value,
            )
            for index, package in typing.cast(
                typing.List[typing.Tuple[int, units.Package]],
                enumerate(packages, start=1),
            )
        ],
        Items=[
            sapient.ItemType(
                SkuCode=item.sku,
                PackageOccurrence=None,
                Quantity=item.quantity,
                Description=lib.text(item.title or item.description, max=35),
                Value=item.value_amount,
                Weight=item.weight,
                HSCode=item.hs_code,
                CountryOfOrigin=item.origin_country,
            )
            for index, item in enumerate(commodities, start=1)
        ],
        Customs=lib.identity(
            sapient.CustomsType(
                ReasonForExport=provider_units.CustomsContentType.map(
                    customs.content_type
                ).value,
                Incoterms=customs.incoterm,
                PreRegistrationNumber=customs.options.sapient_pre_registration_number.state,
                PreRegistrationType=customs.options.sapient_pre_registration_type.state,
                ShippingCharges=None,
                OtherCharges=options.insurance.state,
                QuotedLandedCost=None,
                InvoiceNumber=customs.invoice,
                InvoiceDate=lib.fdate(customs.invoice_date, "%Y-%m-%d"),
                ExportLicenceRequired=None,
                Airn=customs.options.sapient_airn.state,
            )
            if payload.customs and is_intl
            else None
        ),
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(carrier_code=carrier_code, rate_provider=rate_provider),
    )
