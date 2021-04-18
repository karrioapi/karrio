from typing import List, Tuple
from datetime import datetime
from usps_lib.rate_v4_response import PostageType, SpecialServiceType
from usps_lib.rate_v4_request import (
    RateV4Request,
    PackageType,
    SpecialServicesType,
    ShipDateType,
)
from purplship.core.errors import OriginNotServicedError, DestinationNotServicedError
from purplship.core.utils import Serializable, Element, NF, XP, DF
from purplship.core.models import RateDetails, RateRequest, Message, ChargeDetails
from purplship.core.units import Packages, Currency, Options, Services, Country

from purplship.providers.usps.units import (
    ShipmentService, ShipmentOption, PackagingType, ServiceClassID, FirstClassMailType, SortLevelType
)
from purplship.providers.usps.error import parse_error_response
from purplship.providers.usps.utils import Settings


def parse_rate_response(response: Element, settings: Settings) -> Tuple[List[RateDetails], List[Message]]:
    rates: List[RateDetails] = [
        _extract_details(package, settings)
        for package in response.xpath(".//*[local-name() = $name]", name="Postage")
    ]
    return rates, parse_error_response(response, settings)


def _extract_details(postage_node: Element, settings: Settings) -> RateDetails:
    postage: PostageType = XP.build(PostageType, postage_node)
    charges: List[SpecialServiceType] = postage.SpecialServices.SpecialService
    estimated_date = DF.date(postage.CommitmentDate)
    transit = (
        (estimated_date - datetime.now()).days
        if estimated_date is not None else None
    )

    return RateDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        service=ServiceClassID(str(postage.CLASSID)),
        total_charge=NF.decimal(postage.Rate),
        currency=Currency.USD.name,
        transit_days=transit,
        extra_charges=[
            ChargeDetails(
                name=charge.ServiceName,
                amount=NF.decimal(charge.Price),
                currency=Currency.USD.name,
            )
            for charge in charges
        ]
    )


def rate_request(payload: RateRequest, settings: Settings) -> Serializable[RateV4Request]:
    """Create the appropriate USPS rate request depending on the destination

    :param payload: Purplship unified API rate request data
    :param settings: USPS connection and auth settings
    :return: a domestic or international USPS compatible request
    :raises: an OriginNotServicedError when origin country is not serviced by the carrier
    """

    if payload.shipper.country_code is not None and payload.shipper.country_code != Country.US.name:
        raise OriginNotServicedError(payload.shipper.country_code)

    if payload.recipient.country_code is not None and payload.recipient.country_code == Country.US.name:
        raise DestinationNotServicedError(payload.recipient.country_code)

    package = Packages(payload.parcels).single
    options = Options(payload.options, ShipmentOption)
    service = (Services(payload.services, ShipmentService).first or ShipmentService.usps_all).value
    special_services = [getattr(option, 'value', option) for key, option in options if 'usps_option' not in key]
    insurance = next(
        (option.value for key, option in options if 'usps_insurance' in key),
        options.insurance
    )

    container = PackagingType[package.packaging_type or "your_packaging"]
    sort_level = SortLevelType[container.name]
    mail_type = (FirstClassMailType[container.name].value if 'first_class' in service else None)

    request = RateV4Request(
        USERID=settings.username,
        Revision="2",
        Package=[
            PackageType(
                ID=0,
                Service=(service or ShipmentService.usps_all).value,
                FirstClassMailType=mail_type,
                ZipOrigination=payload.shipper.postal_code,
                ZipDestination=payload.recipient.postal_code,
                Pounds=package.weight.LB,
                Ounces=package.weight.OZ,
                Container=container.value,
                Width=package.width.IN,
                Length=package.length.IN,
                Height=package.height.IN,
                Girth=package.girth.value,
                Value=insurance,
                AmountToCollect=options.cash_on_delivery,
                SpecialServices=(
                    SpecialServicesType(SpecialService=[s.value for s in special_services])
                    if any(special_services) else None
                ),
                Content=None,
                GroundOnly=options["usps_option_ground_only"],
                SortBy=sort_level.value,
                Machinable=options["usps_option_machinable_item"],
                ReturnLocations=options["usps_option_return_service_info"],
                ReturnServiceInfo=options["usps_option_return_service_info"],
                DropOffTime=('13:30' if options.shipment_date is not None else None),
                ShipDate=ShipDateType(valueOf_=DF.fdate(options.shipment_date)),
            )
        ],
    )

    return Serializable(request, XP.export)
