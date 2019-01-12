from lxml import etree
from typing import Tuple, List, Union
from purplship.mappers.usps.usps_mapper.partials.interface import USPSMapperBase
from purplship.domain.Types import (
    QuoteDetails,
    Error,
    RateRequest,
    ChargeDetails
)
from purplship.domain.Types.units import (
    Weight,
    WeightUnit,
    Dimension,
    DimensionUnit
)
from purplship.mappers.usps.usps_units import (
    SpecialService,
    Container,
    Service,
    IntlContainer,
    IntlSpecialService,
    IntlContentType,
    FirstClassMailType,
    IntlMailType
)
from pyusps import (
    ratev4request as Rate,
    intlratev2request as IntlRate,
    ratev4response as RateRes,
    intlratev2response as IntlRateRes
)


class USPSMapperPartial(USPSMapperBase):
    
    def parse_rate_response(self, response: etree.ElementBase) -> Tuple[List[QuoteDetails], List[Error]]:
        quotes: List[QuoteDetails] = [
            (self._extract_quote if response.tag == "" else self._extract_intl_quote)
            (package) for package in
            response.xpath(".//*[local-name() = $name]", name="Postage")
        ]
        return (
            quotes, self.parse_error_response(response)
        )

    def _extract_quote(self, postage_node: etree.ElementBase) -> QuoteDetails:
        postage: RateRes.PostageType = RateRes.PostageType()
        postage.build(postage_node)
        currency = "USD"
        special_services: List[RateRes.SpecialServiceType] = [
            svc for svc in postage.SpecialServices
        ]
        return QuoteDetails(
            carrier=self.client.carrier_name,
            service_name=postage.MailService,
            service_type=postage.CommitmentName,
            base_charge=None,
            duties_and_taxes=None,
            total_charge=postage.Rate,
            currency=currency,
            delivery_date=postage.CommitmentDate,
            discount=None,
            extra_charges=[
                ChargeDetails(
                    name=SpecialService(svc.ServiceID).name,
                    amount=svc.Price,
                    currency=currency
                ) for svc in special_services
            ]
        )

    def _extract_intl_quote(self, service_node: etree.ElementBase) -> QuoteDetails:
        service: IntlRateRes.ServiceType = IntlRateRes.ServiceType()
        service.build(service_node)
        currency = "USD"
        special_services: List[IntlRateRes.ExtraServiceType] = [
            svc for svc in service.ExtraServices
        ]
        return QuoteDetails(
            carrier=self.client.carrier_name,
            service_name=service.ID,
            service_type=service.MailType,
            base_charge=None,
            duties_and_taxes=None,
            total_charge=service.Postage,
            currency=currency,
            delivery_date=service.GuaranteeAvailability,
            discount=None,
            extra_charges=[
                ChargeDetails(
                    name=IntlSpecialService(special.ServiceID).name,
                    amount=special.Price,
                    currency=currency
                ) for special in special_services
            ]
        )

    def create_rate_request(self, payload: RateRequest) -> Union[Rate.RateV4Request, IntlRate.IntlRateV2Request]:
        return (
            self._create_rate_request
            if (
                payload.recipient.country_code is None or
                payload.recipient.country_code == 'US'
            ) else
            self._create_intl_rate_request
        )(payload)

    def _create_rate_request(self, payload: RateRequest) -> Rate.RateV4Request:
        weight_unit = WeightUnit[payload.shipment.weight_unit or "LB"]
        dimension_unit = DimensionUnit[payload.shipment.dimension_unit or "IN"]
        special_services = [
            SpecialService[svc.code].value
            for svc in payload.shipment.options
            if svc.code in SpecialService.__members__
        ]
        services = [
            Service[svc].value for svc
            in payload.shipment.services
            if svc in Service.__members__
        ]
        return Rate.RateV4Request(
            USERID=self.client.username,
            Revision="2",
            Package=[
               Rate.PackageType(
                   ID=item.id or str(index),
                   DestinationEntryFacilityType=None,
                   SortationLevel=None,
                   Service=", ".join(services) if len(services) else None,
                   FirstClassMailType=(
                       FirstClassMailType[item.packaging_type]
                   ) if any(
                       svc for svc in services if Service[svc].value
                       in ['First Class', 'First Class Commercial', 'First Class HFPCommercial']
                   ) else None,
                   ZipOrigination=payload.shipper.postal_code,
                   ZipDestination=payload.recipient.postal_code,
                   Pounds=Weight(item.weight, weight_unit).LB,
                   Ounces=None,
                   Container=Container[item.packaging_type].value,
                   Size=None,
                   Width=Dimension(item.width, dimension_unit).IN,
                   Length=Dimension(item.length, dimension_unit).IN,
                   Height=Dimension(item.height, dimension_unit).IN,
                   Girth=None,
                   Value=None,
                   AmountToCollect=None,
                   SpecialServices=Rate.SpecialServicesType(
                       SpecialService=special_services
                   ) if len(special_services) else None,
                   Content=None,
                   GroundOnly=None,
                   SortBy=None,
                   Machinable=None,
                   ReturnLocations=None,
                   ReturnServiceInfo=None,
                   DropOffTime=None,
                   ShipDate=payload.shipment.date,
                ) for index, item in enumerate(payload.shipment.items)
            ]
        )

    def _create_intl_rate_request(self, payload: RateRequest) -> IntlRate.IntlRateV2Request:
        weight_unit = WeightUnit[payload.shipment.weight_unit or "LB"]
        dimension_unit = DimensionUnit[payload.shipment.dimension_unit or "IN"]
        special_services = [
            IntlSpecialService[svc.code].value
            for svc in payload.shipment.options
            if svc.code in IntlSpecialService.__members__
        ]
        return IntlRate.IntlRateV2Request(
            USERID=self.client.username,
            Revision="2",
            Package=[
                IntlRate.PackageType(
                    ID=None,
                    Pounds=Weight(item.weight, weight_unit).LB,
                    Ounces=None,
                    MailType=IntlMailType[item.packaging_type].value,
                    GXG=None,
                    ValueOfContents=item.value_amount or payload.shipment.declared_value,
                    Country=payload.recipient.country_code,
                    Container=IntlContainer[item.packaging_type].value,
                    Size=None,
                    Width=Dimension(item.width, dimension_unit).IN,
                    Length=Dimension(item.length, dimension_unit).IN,
                    Height=Dimension(item.height, dimension_unit).IN,
                    Girth=None,
                    OriginZip=payload.shipper.postal_code,
                    CommercialFlag=None,
                    CommercialPlusFlag=None,
                    AcceptanceDateTime=payload.shipment.date,
                    DestinationPostalCode=payload.recipient.postal_code,
                    ExtraServices=Rate.SpecialServicesType(
                       SpecialService=special_services
                    ) if len(special_services) else None,
                    Content=IntlRate.ContentType(
                        ContentType=IntlContentType[item.content].value,
                        ContentDescription=item.content
                    ) if item.content else None
                ) for item in payload.shipment.items
            ]
        )
