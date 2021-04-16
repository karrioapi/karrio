import time
from functools import reduce
from typing import List, Tuple, cast, Iterable
from dhl_express_lib.dct_req_global_2_0 import (
    DCTRequest,
    DCTTo,
    DCTFrom,
    GetQuoteType,
    BkgDetailsType,
    PiecesType,
    MetaData,
    PieceType,
    QtdShpType,
    QtdShpExChrgType,
)
from dhl_express_lib.dct_requestdatatypes_global import DCTDutiable
from dhl_express_lib.dct_response_global_2_0 import QtdShpType as ResponseQtdShpType

from purplship.core.errors import DestinationNotServicedError
from purplship.core.utils import Serializable, Element, NF, XP, DF
from purplship.core.units import Packages, Options, Package, WeightUnit, DimensionUnit, Services, CountryCurrency
from purplship.core.models import RateDetails, Message, ChargeDetails, RateRequest
from purplship.providers.dhl_express.units import (
    ProductCode,
    DCTPackageType,
    PackagePresets,
    SpecialServiceCode,
    NetworkType,
)
from purplship.providers.dhl_express.utils import Settings
from purplship.providers.dhl_express.error import parse_error_response


def parse_rate_response(
    response: Element, settings: Settings
) -> Tuple[List[RateDetails], List[Message]]:
    qtdshp_list = response.xpath(".//*[local-name() = $name]", name="QtdShp")
    quotes: List[RateDetails] = [
        _extract_quote(qtdshp_node, settings) for qtdshp_node in qtdshp_list
    ]
    return (
        [quote for quote in quotes if quote is not None],
        parse_error_response(response, settings),
    )


def _extract_quote(qtdshp_node: Element, settings: Settings) -> RateDetails:
    qtdshp = ResponseQtdShpType()
    qtdshp.build(qtdshp_node)
    if qtdshp.ShippingCharge is None or qtdshp.ShippingCharge == 0:
        return None

    ExtraCharges = list(
        map(
            lambda s: ChargeDetails(
                name=s.LocalServiceTypeName, amount=NF.decimal(s.ChargeValue or 0)
            ),
            qtdshp.QtdShpExChrg,
        )
    )
    Discount_ = reduce(
        lambda d, ec: d + ec.amount if "Discount" in ec.name else d, ExtraCharges, 0.0
    )
    DutiesAndTaxes_ = reduce(
        lambda d, ec: d + ec.amount if "TAXES PAID" in ec.name else d, ExtraCharges, 0.0
    )
    delivery_date = DF.date(qtdshp.DeliveryDate[0].DlvyDateTime, "%Y-%m-%d %H:%M:%S")
    pricing_date = DF.date(qtdshp.PricingDate)
    transit = (
        (delivery_date - pricing_date).days
        if all([delivery_date, pricing_date])
        else None
    )
    service_name = next(
        (p.name for p in ProductCode if p.value == qtdshp.GlobalProductCode),
        None,
    )
    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        currency=qtdshp.CurrencyCode,
        transit_days=transit,
        service=(service_name or qtdshp.GlobalProductCode),
        base_charge=NF.decimal(qtdshp.WeightCharge),
        total_charge=NF.decimal(qtdshp.ShippingCharge),
        duties_and_taxes=NF.decimal(DutiesAndTaxes_),
        discount=NF.decimal(Discount_),
        extra_charges=list(
            map(
                lambda s: ChargeDetails(
                    name=s.LocalServiceTypeName,
                    amount=NF.decimal(s.ChargeValue),
                    currency=qtdshp.CurrencyCode,
                ),
                qtdshp.QtdShpExChrg,
            )
        ),
        meta=(dict(
            service=qtdshp.GlobalProductCode,
            service_name=qtdshp.ProductShortName
        ) if service_name is None else None)
    )


def rate_request(payload: RateRequest, settings: Settings) -> Serializable[DCTRequest]:
    packages = Packages(payload.parcels, PackagePresets, required=["weight"])
    products = [*Services(payload.services, ProductCode)]
    options = Options(payload.options, SpecialServiceCode)

    is_international = payload.shipper.country_code != payload.recipient.country_code
    is_document = all([parcel.is_document for parcel in payload.parcels])
    is_dutiable = not is_document

    if not is_international and payload.shipper.country_code in ["CA"]:
        raise DestinationNotServicedError(payload.shipper.country_code)

    paperless = (SpecialServiceCode.dhl_paperless_trade if (is_international and is_dutiable) else None)
    special_services = [*options, *([(paperless.name, None)] if paperless is not None else [])]
    insurance = options['dhl_shipment_insurance'].value if 'dhl_shipment_insurance' in options else None

    if len(products) == 0:
        if is_international and is_document:
            product = 'dhl_express_worldwide_doc'
        elif is_international:
            product = 'dhl_express_worldwide_nondoc'
        elif is_document and 'envelope' in packages[0].packaging_type:
            product = 'dhl_express_envelope_doc'
        elif is_document:
            product = 'dhl_domestic_express_doc'
        else:
            product = 'dhl_express_12_00_nondoc'

        products = [ProductCode[product]]

    request = DCTRequest(
        GetQuote=GetQuoteType(
            Request=settings.Request(
                MetaData=MetaData(SoftwareName="3PV", SoftwareVersion=1.0)
            ),
            From=DCTFrom(
                CountryCode=payload.shipper.country_code,
                Postalcode=payload.shipper.postal_code,
                City=payload.shipper.city,
                Suburb=payload.shipper.state_code,
            ),
            To=DCTTo(
                CountryCode=payload.recipient.country_code,
                Postalcode=payload.recipient.postal_code,
                City=payload.recipient.city,
                Suburb=payload.recipient.state_code,
            ),
            BkgDetails=BkgDetailsType(
                PaymentCountryCode=payload.shipper.country_code,
                NetworkTypeCode=NetworkType.both_time_and_day_definite.value,
                WeightUnit=WeightUnit.LB.value,
                DimensionUnit=DimensionUnit.IN.value,
                ReadyTime=time.strftime("PT%HH%MM"),
                Date=time.strftime("%Y-%m-%d"),
                IsDutiable=("Y" if is_dutiable else "N"),
                Pieces=PiecesType(
                    Piece=[
                        PieceType(
                            PieceID=package.parcel.id or f"{index}",
                            PackageTypeCode=DCTPackageType[
                                package.packaging_type or "your_packaging"
                            ].value,
                            Depth=package.length.IN,
                            Width=package.width.IN,
                            Height=package.height.IN,
                            Weight=package.weight.LB,
                        )
                        for index, package in enumerate(
                            cast(Iterable[Package], packages), 1
                        )
                    ]
                ),
                NumberOfPieces=len(packages),
                ShipmentWeight=packages.weight.LB,
                Volume=None,
                PaymentAccountNumber=settings.account_number,
                InsuredCurrency=(options.currency if insurance is not None else None),
                InsuredValue=insurance,
                PaymentType=None,
                AcctPickupCloseTime=None,
                QtdShp=[
                    QtdShpType(
                        GlobalProductCode=product.value,
                        LocalProductCode=product.value,
                        QtdShpExChrg=[
                            QtdShpExChrgType(SpecialServiceType=SpecialServiceCode[key].value.key)
                            for key, _ in special_services if key in SpecialServiceCode
                        ],
                    )
                    for product in products
                ],
            ),
            Dutiable=(
                DCTDutiable(
                    DeclaredValue=insurance or 1.0,
                    DeclaredCurrency=options.currency or CountryCurrency[payload.shipper.country_code].value
                )
                if is_dutiable else None
            ),
        ),
    )

    return Serializable(request, _request_serializer)


def _request_serializer(request: DCTRequest) -> str:
    namespacedef_ = (
        'xmlns:p="http://www.dhl.com" '
        'xmlns:p1="http://www.dhl.com/datatypes" '
        'xmlns:p2="http://www.dhl.com/DCTRequestdatatypes" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.dhl.com DCT-req.xsd "'
    )
    return XP.export(
        request,
        name_="p:DCTRequest",
        namespacedef_=namespacedef_,
    ).replace('schemaVersion="2."', 'schemaVersion="2.0"')
