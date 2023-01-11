from ups_lib.rate_web_service_schema import (
    RateRequest as UPSRateRequest,
    RatedShipmentType,
    ShipmentRatingOptionsType,
    ShipToType,
    ShipmentType,
    ShipperType,
    ShipAddressType,
    ShipToAddressType,
    PackageType,
    PackageWeightType,
    UOMCodeDescriptionType,
    DimensionsType,
    RequestType,
    TransactionReferenceType,
    TimeInTransitRequestType,
    EstimatedArrivalType,
)

import typing
import functools
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.ups.error as provider_error
import karrio.providers.ups.units as provider_units
import karrio.providers.ups.utils as provider_utils


def parse_rate_response(
    response: lib.Element,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    rate_reply = lib.find_element("RatedShipment", response)
    rates: typing.List[models.RateDetails] = functools.reduce(
        _extract_package_rate(settings), rate_reply, []
    )
    return rates, provider_error.parse_error_response(response, settings)


def _extract_package_rate(
    settings: provider_utils.Settings,
) -> typing.Callable[
    [typing.List[models.RateDetails], lib.Element], typing.List[models.RateDetails]
]:
    def extract(
        rates: typing.List[models.RateDetails], detail_node: lib.Element
    ) -> typing.List[models.RateDetails]:
        rate = lib.to_object(RatedShipmentType, detail_node)

        if rate.NegotiatedRateCharges is not None:
            total_charges = (
                rate.NegotiatedRateCharges.TotalChargesWithTaxes
                or rate.NegotiatedRateCharges.TotalCharge
            )
            taxes = rate.NegotiatedRateCharges.TaxCharges
            itemized_charges = rate.NegotiatedRateCharges.ItemizedCharges + taxes
        else:
            total_charges = rate.TotalChargesWithTaxes or rate.TotalCharges
            taxes = rate.TaxCharges
            itemized_charges = rate.ItemizedCharges + taxes

        charges = [
            ("Base charge", rate.TransportationCharges.MonetaryValue),
            ("Taxes", sum(c.MonetaryValue for c in taxes)),
            (rate.ServiceOptionsCharges.Code, rate.ServiceOptionsCharges.MonetaryValue),
            *((c.Code, c.MonetaryValue) for c in itemized_charges),
        ]
        estimated_arrival = (
            lib.find_element(
                "EstimatedArrival", detail_node, EstimatedArrivalType, first=True
            )
            or EstimatedArrivalType()
        )
        transit_days = (
            rate.GuaranteedDelivery.BusinessDaysInTransit
            if rate.GuaranteedDelivery is not None
            else estimated_arrival.BusinessDaysInTransit
        )
        currency = lib.find_element("CurrencyCode", detail_node, first=True).text
        service = provider_units.ShippingService.map(rate.Service.Code)

        return rates + [
            models.RateDetails(
                carrier_name=settings.carrier_name,
                carrier_id=settings.carrier_id,
                currency=currency,
                service=service.name_or_key,
                total_charge=lib.to_decimal(total_charges.MonetaryValue),
                extra_charges=[
                    models.ChargeDetails(
                        name=name,
                        amount=lib.to_decimal(amount),
                        currency=currency,
                    )
                    for name, amount in charges
                    if name is not None or not amount
                ],
                transit_days=lib.to_int(transit_days),
                meta=dict(service_name=service.name_or_key),
            )
        ]

    return extract


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable[UPSRateRequest]:
    packages = lib.to_packages(payload.parcels, provider_units.PackagePresets)
    is_document = all([parcel.is_document for parcel in payload.parcels])
    service = lib.to_services(payload.services, provider_units.ShippingService).first
    mps_packaging = (
        provider_units.PackagingType.ups_unknown.value if len(packages) > 1 else None
    )

    request = UPSRateRequest(
        Request=RequestType(
            RequestOption=["Shop", "Rate"],
            SubVersion=None,
            TransactionReference=TransactionReferenceType(
                CustomerContext=payload.reference,
                TransactionIdentifier=getattr(payload, "id", None),
            ),
        ),
        PickupType=None,
        CustomerClassification=None,
        Shipment=ShipmentType(
            OriginRecordTransactionTimestamp=None,
            Shipper=ShipperType(
                Name=payload.shipper.company_name,
                ShipperNumber=settings.account_number,
                Address=ShipAddressType(
                    AddressLine=lib.join(
                        payload.recipient.address_line1,
                        payload.recipient.address_line2,
                    ),
                    City=payload.shipper.city,
                    StateProvinceCode=payload.shipper.state_code,
                    PostalCode=payload.shipper.postal_code,
                    CountryCode=payload.shipper.country_code,
                ),
            ),
            ShipTo=ShipToType(
                Name=payload.recipient.company_name,
                Address=ShipToAddressType(
                    AddressLine=lib.join(
                        payload.recipient.address_line1,
                        payload.recipient.address_line2,
                    ),
                    City=payload.recipient.city,
                    StateProvinceCode=payload.recipient.state_code,
                    PostalCode=payload.recipient.postal_code,
                    CountryCode=payload.recipient.country_code,
                    ResidentialAddressIndicator=None,
                ),
            ),
            ShipFrom=None,
            AlternateDeliveryAddress=None,
            ShipmentIndicationType=None,
            PaymentDetails=None,
            FRSPaymentInformation=None,
            FreightShipmentInformation=None,
            GoodsNotInFreeCirculationIndicator=None,
            Service=(
                UOMCodeDescriptionType(Code=service.value, Description=None)
                if service is not None
                else None
            ),
            NumOfPieces=None,  # Only required for Freight
            ShipmentTotalWeight=None,  # Only required for "timeintransit" requests
            DocumentsOnlyIndicator=("" if is_document else None),
            Package=[
                PackageType(
                    PackagingType=UOMCodeDescriptionType(
                        Code=(
                            mps_packaging
                            or provider_units.PackagingType.map(package.packaging_type).value
                            or provider_units.PackagingType.ups_customer_supplied_package.value
                        ),
                        Description=None,
                    ),
                    Dimensions=(
                        DimensionsType(
                            UnitOfMeasurement=UOMCodeDescriptionType(
                                Code=package.dimension_unit.value, Description=None
                            ),
                            Length=package.length.value,
                            Width=package.width.value,
                            Height=package.height.value,
                        )
                        if any(
                            [
                                package.length.value,
                                package.height.value,
                                package.width.value,
                            ]
                        )
                        else None
                    ),
                    DimWeight=None,
                    PackageWeight=PackageWeightType(
                        UnitOfMeasurement=UOMCodeDescriptionType(
                            Code=provider_units.WeightUnit[
                                package.weight_unit.name
                            ].value,
                            Description=None,
                        ),
                        Weight=package.weight.value,
                    )
                    if package.weight.value
                    else None,
                    Commodity=None,
                    PackageServiceOptions=None,
                    AdditionalHandlingIndicator=None,
                )
                for package in packages
            ],
            ShipmentServiceOptions=None,
            ShipmentRatingOptions=ShipmentRatingOptionsType(
                NegotiatedRatesIndicator=""
            ),
            InvoiceLineTotal=None,
            RatingMethodRequestedIndicator=None,
            TaxInformationIndicator=None,
            PromotionalDiscountInformation=None,
            DeliveryTimeInformation=TimeInTransitRequestType(
                PackageBillType="02" if is_document else "03"
            ),
        ),
    )
    return lib.Serializable(
        lib.create_envelope(header_content=settings.Security, body_content=request),
        _request_serializer,
    )


def _request_serializer(envelope: lib.Envelope) -> str:
    namespace_ = """
        xmlns:tns="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
        xmlns:upss="http://www.ups.com/XMLSchema/XOLTWS/UPSS/v1.0"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:common="http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0"
        xmlns:rate="http://www.ups.com/XMLSchema/XOLTWS/Rate/v1.1"
    """.replace(
        " ", ""
    ).replace(
        "\n", " "
    )
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    envelope.Header.ns_prefix_ = envelope.ns_prefix_
    lib.apply_namespaceprefix(envelope.Body.anytypeobjs_[0], "rate")
    lib.apply_namespaceprefix(envelope.Header.anytypeobjs_[0], "upss")
    lib.apply_namespaceprefix(envelope.Body.anytypeobjs_[0].Request, "common")

    return lib.to_xml(envelope, namespacedef_=namespace_)
