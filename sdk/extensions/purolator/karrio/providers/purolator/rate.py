from typing import List, Tuple, cast
from pysoap.envelope import Envelope
from purolator_lib.estimate_service_2_1_2 import (
    GetFullEstimateRequest,
    Shipment,
    SenderInformation,
    Address,
    ReceiverInformation,
    PackageInformation,
    TrackingReferenceInformation,
    PickupInformation,
    ArrayOfPiece,
    Piece,
    Weight as PurolatorWeight,
    WeightUnit as PurolatorWeightUnit,
    RequestContext,
    Dimension as PurolatorDimension,
    DimensionUnit as PurolatorDimensionUnit,
    TotalWeight,
    ShipmentEstimate,
    Tax,
    Surcharge,
    OptionPrice,
    PickupType,
    PhoneNumber,
    PaymentInformation,
    PaymentType,
    InternationalInformation,
    DutyInformation,
    BusinessRelationship,
    ArrayOfOptionIDValuePair,
    OptionIDValuePair,
)
from karrio.core.units import Currency, Packages, Options, Phone, Services
from karrio.core.utils import Serializable, Element, SF, NF, XP, create_envelope
from karrio.core.models import RateRequest, RateDetails, Message, ChargeDetails
from karrio.providers.purolator.utils import Settings, standard_request_serializer
from karrio.providers.purolator.error import parse_error_response
from karrio.providers.purolator.units import (
    ShippingService,
    PackagePresets,
    DutyPaymentType,
    MeasurementOptions,
    ShippingOption,
    NON_OFFICIAL_SERVICES,
)


def parse_rate_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    estimates = XP.find("ShipmentEstimate", response)
    return (
        [_extract_rate(node, settings) for node in estimates],
        parse_error_response(response, settings),
    )


def _extract_rate(estimate_node: Element, settings: Settings) -> RateDetails:
    estimate = XP.to_object(ShipmentEstimate, estimate_node)
    currency = Currency.CAD.name
    service = ShippingService.map(estimate.ServiceID)
    charges = [
        ("Base charge", estimate.BasePrice),
        *(
            (s.Description, s.Amount)
            for s in (
                estimate.Taxes.Tax
                + estimate.Surcharges.Surcharge
                + estimate.OptionPrices.OptionPrice
            )
        ),
    ]

    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        service=service.name_or_key,
        currency=currency,
        transit_days=estimate.EstimatedTransitDays,
        total_charge=NF.decimal(estimate.TotalPrice),
        extra_charges=[
            ChargeDetails(
                name=name,
                amount=NF.decimal(amount),
                currency=currency,
            )
            for name, amount in charges
            if amount
        ],
        meta=dict(service_name=service.name_or_key),
    )


def rate_request(payload: RateRequest, settings: Settings) -> Serializable[Envelope]:
    packages = Packages(payload.parcels, PackagePresets, required=["weight"])
    service = Services(payload.services, ShippingService).first
    options = ShippingOption.to_options(
        payload.options,
        package_options=packages.options,
        service_is_defined=(getattr(service, "value", None) in payload.services),
    )

    shipper_phone = Phone(
        payload.shipper.phone_number, payload.shipper.country_code or "CA"
    )
    recipient_phone = Phone(
        payload.recipient.phone_number, payload.recipient.country_code
    )
    is_international = payload.shipper.country_code != payload.recipient.country_code

    # When no specific service is requested, set a default one.
    if service is None:
        service = ShippingService[
            "purolator_express_international"
            if is_international
            else "purolator_express"
        ]

    request = create_envelope(
        header_content=RequestContext(
            Version="2.1",
            Language=settings.language,
            GroupID="",
            RequestReference=getattr(payload, "id", ""),
            UserToken=settings.user_token,
        ),
        body_content=GetFullEstimateRequest(
            Shipment=Shipment(
                SenderInformation=SenderInformation(
                    Address=Address(
                        Name=payload.shipper.person_name or "",
                        Company=payload.shipper.company_name,
                        Department=None,
                        StreetNumber="",
                        StreetSuffix=None,
                        StreetName=SF.concat_str(
                            payload.shipper.address_line1, join=True
                        ),
                        StreetType=None,
                        StreetDirection=None,
                        Suite=None,
                        Floor=None,
                        StreetAddress2=SF.concat_str(
                            payload.shipper.address_line2, join=True
                        ),
                        StreetAddress3=None,
                        City=payload.shipper.city or "",
                        Province=payload.shipper.state_code or "",
                        Country=payload.shipper.country_code or "",
                        PostalCode=payload.shipper.postal_code or "",
                        PhoneNumber=PhoneNumber(
                            CountryCode=shipper_phone.country_code or "0",
                            AreaCode=shipper_phone.area_code or "0",
                            Phone=shipper_phone.phone or "0",
                            Extension=None,
                        ),
                        FaxNumber=None,
                    ),
                    TaxNumber=(
                        payload.shipper.federal_tax_id or payload.shipper.state_tax_id
                    ),
                ),
                ReceiverInformation=ReceiverInformation(
                    Address=Address(
                        Name=payload.recipient.person_name or "",
                        Company=payload.recipient.company_name,
                        Department=None,
                        StreetNumber="",
                        StreetSuffix=None,
                        StreetName=SF.concat_str(
                            payload.recipient.address_line1, join=True
                        ),
                        StreetType=None,
                        StreetDirection=None,
                        Suite=None,
                        Floor=None,
                        StreetAddress2=SF.concat_str(
                            payload.recipient.address_line2, join=True
                        ),
                        StreetAddress3=None,
                        City=payload.recipient.city or "",
                        Province=payload.recipient.state_code or "",
                        Country=payload.recipient.country_code or "",
                        PostalCode=payload.recipient.postal_code or "",
                        PhoneNumber=PhoneNumber(
                            CountryCode=recipient_phone.country_code or "0",
                            AreaCode=recipient_phone.area_code or "0",
                            Phone=recipient_phone.phone or "0",
                            Extension=None,
                        ),
                        FaxNumber=None,
                    ),
                    TaxNumber=(
                        payload.recipient.federal_tax_id
                        or payload.recipient.state_tax_id
                    ),
                ),
                FromOnLabelIndicator=None,
                FromOnLabelInformation=None,
                ShipmentDate=options.shipment_date,
                PackageInformation=PackageInformation(
                    ServiceID=service.value,
                    Description=packages.description,
                    TotalWeight=(
                        TotalWeight(
                            Value=packages.weight.map(MeasurementOptions).LB,
                            WeightUnit=PurolatorWeightUnit.LB.value,
                        )
                        if packages.weight.value is not None
                        else None
                    ),
                    TotalPieces=1,
                    PiecesInformation=ArrayOfPiece(
                        Piece=[
                            Piece(
                                Weight=(
                                    PurolatorWeight(
                                        Value=package.weight.map(
                                            MeasurementOptions
                                        ).value,
                                        WeightUnit=PurolatorWeightUnit[
                                            package.weight_unit.value
                                        ].value,
                                    )
                                    if package.weight.value
                                    else None
                                ),
                                Length=(
                                    PurolatorDimension(
                                        Value=package.length.value,
                                        DimensionUnit=PurolatorDimensionUnit[
                                            package.dimension_unit.value
                                        ].value,
                                    )
                                    if package.length.value
                                    else None
                                ),
                                Width=(
                                    PurolatorDimension(
                                        Value=package.width.value,
                                        DimensionUnit=PurolatorDimensionUnit[
                                            package.dimension_unit.value
                                        ].value,
                                    )
                                    if package.width.value
                                    else None
                                ),
                                Height=(
                                    PurolatorDimension(
                                        Value=package.height.value,
                                        DimensionUnit=PurolatorDimensionUnit[
                                            package.dimension_unit.value
                                        ].value,
                                    )
                                    if package.height.value
                                    else None
                                ),
                                Options=ArrayOfOptionIDValuePair(
                                    OptionIDValuePair=[
                                        OptionIDValuePair(ID=code, Value=value)
                                        for _, code, value in options.as_list()
                                    ]
                                )
                                if any(options.as_list())
                                else None,
                            )
                            for package in packages
                        ]
                    ),
                    DangerousGoodsDeclarationDocumentIndicator=None,
                    OptionsInformation=None,
                ),
                InternationalInformation=(
                    InternationalInformation(
                        DocumentsOnlyIndicator=packages.is_document,
                        ContentDetails=None,
                        BuyerInformation=None,
                        PreferredCustomsBroker=None,
                        DutyInformation=DutyInformation(
                            BillDutiesToParty=DutyPaymentType.recipient.value,
                            BusinessRelationship=BusinessRelationship.NOT_RELATED.value,
                            Currency=options.currency,
                        ),
                        ImportExportType=None,
                        CustomsInvoiceDocumentIndicator=None,
                    )
                    if is_international
                    else None
                ),
                ReturnShipmentInformation=None,
                PaymentInformation=PaymentInformation(
                    PaymentType=PaymentType.SENDER.value,
                    RegisteredAccountNumber=settings.account_number,
                ),
                PickupInformation=PickupInformation(
                    PickupType=PickupType.DROP_OFF.value
                ),
                NotificationInformation=None,
                TrackingReferenceInformation=(
                    TrackingReferenceInformation(Reference1=payload.reference)
                    if payload.reference != ""
                    else None
                ),
                OtherInformation=None,
                ProactiveNotification=None,
            ),
            ShowAlternativeServicesIndicator=options.purolator_show_alternative_services,
        ),
    )

    return Serializable(request, standard_request_serializer)
