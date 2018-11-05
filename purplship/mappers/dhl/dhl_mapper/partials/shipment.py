import time
from base64 import b64decode
from pydhl.datatypes_global_v61 import MetaData
from pydhl import (
    ship_val_global_req_61 as ShipReq,
    ship_val_global_res_61 as ShipRes
)
from .interface import (
    reduce, Tuple, List, Union, E, DHLMapperBase
)


class DHLMapperPartial(DHLMapperBase):

    def parse_dhlshipment_respone(self, response) -> Tuple[E.ShipmentDetails, List[E.Error]]:
        return (self._extract_shipment(response), self.parse_error_response(response))

    def _extract_shipment(self, shipmentResponseNode) -> E.ShipmentDetails:
        """
            Shipment extraction is implemented using lxml queries instead of generated ShipmentResponse type
            because the type construction fail during validation out of our control
        """
        get_value = lambda query: query[0].text if len(query) > 0 else None
        get = lambda key: get_value(shipmentResponseNode.xpath("//%s" % key))
        tracking_number = get("AirwayBillNumber")
        if tracking_number == None:
            return None
        plates = [p.text for p in shipmentResponseNode.xpath("//LicensePlateBarCode")]
        barcodes = [child.text for child in shipmentResponseNode.xpath("//Barcodes")[0].getchildren()]
        documents = reduce(lambda r,i: (r + [i] if i else r), [get("AWBBarCode")] + plates + barcodes, [])
        reference = E.ReferenceDetails(value=get("ReferenceID"), type=get("ReferenceType")) if len(shipmentResponseNode.xpath("//Reference")) > 0 else None
        currency_ = get("CurrencyCode")
        return E.ShipmentDetails(
            carrier=self.client.carrier_name,
            tracking_numbers=[tracking_number],
            shipment_date= get("ShipmentDate"),
            services=(
                [get("ProductShortName")] +
                [service.text for service in shipmentResponseNode.xpath("//SpecialServiceDesc")] +
                [service.text for service in shipmentResponseNode.xpath("//InternalServiceCode")]
            ),
            charges=[
                E.ChargeDetails(name="PackageCharge", amount=float(get("PackageCharge")), currency=currency_) 
            ],
            documents=documents,
            reference=reference,
            total_charge= E.ChargeDetails(name="Shipment charge", amount=get("ShippingCharge"), currency=currency_)
        )

    def create_dhlshipment_request(self, payload: E.shipment_request) -> ShipReq.ShipmentRequest:
        Request_ = self.init_request()
        Request_.MetaData = MetaData(SoftwareName="3PV", SoftwareVersion="1.0")

        Billing_ = ShipReq.Billing(
            ShipperAccountNumber=payload.shipper.account_number or self.client.account_number,
            BillingAccountNumber=payload.shipment.payment_account_number,
            ShippingPaymentType=payload.shipment.paid_by,
            DutyAccountNumber=payload.shipment.duty_payment_account,
            DutyPaymentType=payload.shipment.duty_paid_by
        )

        Consignee_ = ShipReq.Consignee(
            CompanyName=payload.recipient.company_name,
            PostalCode=payload.recipient.postal_code,
            CountryCode=payload.recipient.country_code,
            City=payload.recipient.city,
            CountryName=payload.recipient.country_name,
            Division=payload.recipient.state,
            DivisionCode=payload.recipient.state_code
        )

        if any([payload.recipient.person_name, payload.recipient.email_address]):
            Consignee_.Contact = ShipReq.Contact(
                PersonName=payload.recipient.person_name,
                PhoneNumber=payload.recipient.phone_number,
                Email=payload.recipient.email_address,
                FaxNumber=payload.recipient.extra.get('FaxNumber'),
                Telex=payload.recipient.extra.get('Telex'),
                PhoneExtension=payload.recipient.extra.get('PhoneExtension'),
                MobilePhoneNumber=payload.recipient.extra.get('MobilePhoneNumber')
            )

        [Consignee_.add_AddressLine(line)
         for line in payload.recipient.address_lines]

        Shipper_ = ShipReq.Shipper(
            ShipperID=payload.shipment.extra.get('ShipperID') or Billing_.ShipperAccountNumber,
            RegisteredAccount=payload.shipment.extra.get('ShipperID') or Billing_.ShipperAccountNumber,
            CompanyName=payload.shipper.company_name,
            PostalCode=payload.shipper.postal_code,
            CountryCode=payload.shipper.country_code,
            City=payload.shipper.city,
            CountryName=payload.shipper.country_name,
            Division=payload.shipper.state,
            DivisionCode=payload.shipper.state_code
        )

        if any([payload.shipper.person_name, payload.shipper.email_address]):
            Shipper_.Contact = ShipReq.Contact(
                PersonName=payload.shipper.person_name,
                PhoneNumber=payload.shipper.phone_number,
                Email=payload.shipper.email_address,
                FaxNumber=payload.shipper.extra.get('FaxNumber'),
                Telex=payload.shipper.extra.get('Telex'),
                PhoneExtension=payload.shipper.extra.get('PhoneExtension'),
                MobilePhoneNumber=payload.shipper.extra.get('MobilePhoneNumber')
            )

        [Shipper_.add_AddressLine(line)
         for line in payload.shipper.address_lines]

        Pieces_ = ShipReq.Pieces()
        for p in payload.shipment.items:
            Pieces_.add_Piece(ShipReq.Piece(
                PieceID=p.id,
                PackageType=p.packaging_type,
                Weight=p.weight,
                DimWeight=p.extra.get('DimWeight'),
                Height=p.height,
                Width=p.width,
                Depth=p.length,
                PieceContents=p.content
            ))

        """ 
            Get PackageType from extra when implementing multi carrier,
            Get weight from total_weight if specified otherwise calculated from items weight sum
        """
        ShipmentDetails_ = ShipReq.ShipmentDetails(
            NumberOfPieces=len(payload.shipment.items),
            Pieces=Pieces_,
            Weight=payload.shipment.total_weight or sum([p.weight for p in payload.shipment.items]),
            CurrencyCode=payload.shipment.currency or "USD",
            WeightUnit=(payload.shipment.weight_unit or "LB")[0],
            DimensionUnit=(payload.shipment.dimension_unit or "IN")[0],
            Date=payload.shipment.date or time.strftime('%Y-%m-%d'),
            PackageType=payload.shipment.packaging_type or payload.shipment.extra.get('PackageType'),
            IsDutiable= "N" if payload.shipment.is_document else "Y",
            InsuredAmount=payload.shipment.insured_amount,
            DoorTo=payload.shipment.extra.get('DoorTo'),
            GlobalProductCode=payload.shipment.extra.get('GlobalProductCode'),
            LocalProductCode=payload.shipment.extra.get('LocalProductCode'),
            Contents=payload.shipment.extra.get('Contents') or "..."
        )

        ShipmentRequest_ = ShipReq.ShipmentRequest(
            schemaVersion="6.1",
            Request=Request_,
            RegionCode=payload.shipment.extra.get('RegionCode') or "AM",
            RequestedPickupTime=payload.shipment.extra.get('RequestedPickupTime') or "Y",
            LanguageCode=payload.shipment.extra.get('LanguageCode') or "en",
            PiecesEnabled=payload.shipment.extra.get('PiecesEnabled') or "Y",
            NewShipper=payload.shipment.extra.get('NewShipper'),
            Billing=Billing_,
            Consignee=Consignee_,
            Shipper=Shipper_,
            ShipmentDetails=ShipmentDetails_,
            EProcShip=payload.shipment.extra.get('EProcShip')
        )

        if payload.shipment.label is not None:
            DocImages_ = ShipReq.DocImages()
            Image_ = None if 'Image' not in payload.shipment.label.extra else b64decode(
                payload.shipment.label.extra.get('Image') + '=' * (-len(payload.shipment.label.extra.get('Image')) % 4)
            )
            DocImages_.add_DocImage(ShipReq.DocImage(
                Type=payload.shipment.label.type,
                ImageFormat=payload.shipment.label.format,
                Image=Image_
            ))
            ShipmentRequest_.DocImages = DocImages_

        if ShipmentDetails_.IsDutiable == "Y":
            ShipmentRequest_.Dutiable = ShipReq.Dutiable(
                DeclaredCurrency=ShipmentDetails_.CurrencyCode,
                DeclaredValue=payload.shipment.declared_value,
                TermsOfTrade=payload.shipment.customs.terms_of_trade,
                ScheduleB=payload.shipment.customs.extra.get('ScheduleB'),
                ExportLicense=payload.shipment.customs.extra.get('ExportLicense'),
                ShipperEIN=payload.shipment.customs.extra.get('ShipperEIN'),
                ShipperIDType=payload.shipment.customs.extra.get('ShipperIDType'),
                ImportLicense=payload.shipment.customs.extra.get('ImportLicense'),
                ConsigneeEIN=payload.shipment.customs.extra.get('ConsigneeEIN')
            )

        [ShipmentRequest_.add_SpecialService(
            ShipReq.SpecialService(SpecialServiceType=service)
        ) for service in (payload.shipment.extra_services + [payload.shipment.service_type])]

        [ShipmentRequest_.add_Commodity(
            ShipReq.Commodity(CommodityCode=c.code, CommodityName=c.description)
        ) for c in payload.shipment.items]

        [ShipmentRequest_.add_Reference(
            ShipReq.Reference(ReferenceID=r)
        ) for r in payload.shipment.references]

        return ShipmentRequest_

