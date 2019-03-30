from lxml import etree
from functools import reduce
from typing import Tuple, List, Union, Any
from purplship.mappers.usps.usps_mapper.partials.interface import USPSMapperBase
from purplship.domain.Types import (
    QuoteDetails,
    Error,
    RateRequest,
    ChargeDetails,
    Option,
)
from purplship.domain.Types.units import (
    Weight,
    WeightUnit,
    Dimension,
    DimensionUnit,
    Country,
)
from purplship.mappers.usps.usps_units import (
    SpecialService,
    Container,
    Service,
    IntlContainer,
    ExtraService,
    IntlContentType,
    FirstClassMailType,
    IntlMailType,
)
from pyusps import (
    ratev4request as Rate,
    intlratev2request as IntlRate,
    ratev4response as RateRes,
    intlratev2response as IntlRateRes,
)


class USPSMapperPartial(USPSMapperBase):
    def parse_rate_response(
        self, response: etree.ElementBase
    ) -> Tuple[List[QuoteDetails], List[Error]]:
        is_intl = response.tag == "IntlRateV2Response"
        quotes: List[QuoteDetails] = [
            (
                self._extract_quote
                if not is_intl
                else self._extract_intl_quote
            )(package)
            for package in response.xpath(
                ".//*[local-name() = $name]",
                name="Postage" if not is_intl else "Service"
            )
        ]
        return quotes, self.parse_error_response(response)

    def _extract_quote(self, postage_node: etree.ElementBase) -> QuoteDetails:
        postage: RateRes.PostageType = RateRes.PostageType()
        postage.build(postage_node)
        currency = "USD"
        services: List[RateRes.SpecialServiceType] = [
            (lambda s: (s, s.build(svc)))(RateRes.SpecialServiceType())[0]
            for svc in postage_node.xpath(".//*[local-name() = $name]", name="SpecialService")
        ]

        def get(key: str) -> Any:
            return reduce(lambda r, v: v.text, postage_node.findall(key), None)
        return QuoteDetails(
            carrier=self.client.carrier_name,
            service_name=None,
            service_type=get("MailService"),
            base_charge=None,
            duties_and_taxes=None,
            total_charge=float(postage_node.find("Rate").text),
            currency=currency,
            delivery_date=postage.CommitmentDate,
            discount=None,
            extra_charges=[
                ChargeDetails(
                    name=SpecialService(str(svc.ServiceID)).name,
                    amount=svc.Price,
                    currency=currency,
                )
                for svc in services
            ],
        )

    def _extract_intl_quote(self, service_node: etree.ElementBase) -> QuoteDetails:
        service: IntlRateRes.ServiceType = IntlRateRes.ServiceType()
        service.build(service_node)
        currency = "USD"
        special_services: List[IntlRateRes.ExtraServiceType] = [
            (lambda s: (s, s.build(svc)))(IntlRateRes.ExtraServiceType())[0]
            for svc in service_node.xpath(".//*[local-name() = $name]", name="ExtraService")
        ]
        return QuoteDetails(
            carrier=self.client.carrier_name,
            service_name=None,
            service_type=service.MailType,
            base_charge=None,
            duties_and_taxes=None,
            total_charge=service.Postage,
            currency=currency,
            delivery_date=service.GuaranteeAvailability,
            discount=None,
            extra_charges=[
                ChargeDetails(
                    name=ExtraService(special.ServiceID).name,
                    amount=special.Price,
                    currency=currency,
                )
                for special in special_services
            ],
        )

    def create_rate_request(
        self, payload: RateRequest
    ) -> Union[Rate.RateV4Request, IntlRate.IntlRateV2Request]:
        return (
            self._create_rate_request
            if (
                payload.recipient.country_code is None
                or payload.recipient.country_code == "US"
            )
            else self._create_intl_rate_request
        )(payload)

    def _create_rate_request(self, payload: RateRequest) -> Rate.RateV4Request:
        weight_unit = WeightUnit[payload.shipment.weight_unit or "LB"]
        dimension_unit = DimensionUnit[payload.shipment.dimension_unit or "IN"]
        special_services: List[Option] = [
            svc
            for svc in payload.shipment.options
            if svc.code in SpecialService.__members__
        ]
        services: List[str] = [
            svc for svc in payload.shipment.services if svc in Service.__members__
        ]
        return Rate.RateV4Request(
            USERID=self.client.username,
            Revision="2",
            Package=[
                Rate.PackageType(
                    ID=item.id or str(index),
                    DestinationEntryFacilityType=None,
                    SortationLevel=None,
                    Service=(
                        lambda item_services: ", ".join(
                            [Service[svc].value for svc in item_services]
                        )
                        if len(item_services) > 0
                        else None
                    )(
                        services
                        + [
                            svc
                            for svc in item.extra.get("services", [])
                            if svc in Service.__members__
                        ]
                    ),
                    FirstClassMailType=FirstClassMailType[item.packaging_type].value
                    if (
                        item.packaging_type is not None
                        and any(
                            svc
                            for svc in (services + item.extra.get("services", []))
                            if Service[svc].value
                            in [
                                "First Class",
                                "First Class Commercial",
                                "First Class HFPCommercial",
                            ]
                        )
                    )
                    else None,
                    ZipOrigination=payload.shipper.postal_code,
                    ZipDestination=payload.recipient.postal_code,
                    Pounds=Weight(item.weight, weight_unit).LB,
                    Ounces=None,
                    Container=item.extra.get("Container")
                    or (
                        Container[item.packaging_type].value
                        if item.packaging_type
                        else None
                    ),
                    Size=item.extra.get("Size"),
                    Width=Dimension(item.width, dimension_unit).IN,
                    Length=Dimension(item.length, dimension_unit).IN,
                    Height=Dimension(item.height, dimension_unit).IN,
                    Girth=item.extra.get("Girth"),
                    Value=item.value_amount,
                    AmountToCollect=None,
                    SpecialServices=(
                        lambda item_special_services: Rate.SpecialServicesType(
                            SpecialService=[
                                SpecialService[svc.code].value
                                for svc in item_special_services
                            ]
                        )
                        if len(item_special_services) > 0
                        else None
                    )(
                        special_services
                        + [
                            Option(**svc)
                            for svc in item.extra.get("options", [])
                            if svc["code"] in SpecialService.__members__
                        ]
                    ),
                    Content=None,
                    GroundOnly=None,
                    SortBy=None,
                    Machinable=None,
                    ReturnLocations=None,
                    ReturnServiceInfo=None,
                    DropOffTime=None,
                    ShipDate=item.extra.get("ShipDate") or payload.shipment.date,
                )
                for index, item in enumerate(payload.shipment.items)
            ],
        )

    def _create_intl_rate_request(
        self, payload: RateRequest
    ) -> IntlRate.IntlRateV2Request:
        weight_unit = WeightUnit[payload.shipment.weight_unit or "LB"]
        dimension_unit = DimensionUnit[payload.shipment.dimension_unit or "IN"]
        extra_services = [
            ExtraService[svc.code].value
            for svc in payload.shipment.options
            if svc.code in ExtraService.__members__
        ]
        return IntlRate.IntlRateV2Request(
            USERID=self.client.username,
            Revision="2",
            Package=[
                IntlRate.PackageType(
                    ID=item.id or index,
                    Pounds=Weight(item.weight, weight_unit).LB,
                    Ounces=None,
                    Machinable=item.extra.get("Machinable"),
                    MailType=IntlMailType[item.packaging_type].value,
                    GXG=None,
                    ValueOfContents=item.value_amount
                    or payload.shipment.declared_value,
                    Country=Country[payload.recipient.country_code].value
                    if payload.recipient.country_code
                    else None,
                    Container=item.extra.get("Container")
                    or (
                        IntlContainer[item.packaging_type].value
                        if item.packaging_type
                        else None
                    ),
                    Size=item.extra.get("Size"),
                    Width=Dimension(item.width, dimension_unit).IN,
                    Length=Dimension(item.length, dimension_unit).IN,
                    Height=Dimension(item.height, dimension_unit).IN,
                    Girth=item.extra.get("Girth"),
                    OriginZip=payload.shipper.postal_code,
                    CommercialFlag=item.extra.get("CommercialFlag"),
                    CommercialPlusFlag=item.extra.get("CommercialPlusFlag"),
                    AcceptanceDateTime=payload.shipment.date,
                    DestinationPostalCode=payload.recipient.postal_code,
                    ExtraServices=(
                        lambda item_extra_services: IntlRate.ExtraServicesType(
                            ExtraService=[
                                ExtraService[svc.code].value
                                for svc in item_extra_services
                            ]
                        )
                        if len(item_extra_services) > 0
                        else None
                    )(
                        extra_services
                        + [
                            Option(**svc)
                            for svc in item.extra.get("options", [])
                            if svc["code"] in ExtraService.__members__
                        ]
                    ),
                    Content=IntlRate.ContentType(
                        ContentType=IntlContentType[item.content].value,
                        ContentDescription=item.content,
                    )
                    if item.content
                    else None,
                )
                for index, item in enumerate(payload.shipment.items)
            ],
        )
