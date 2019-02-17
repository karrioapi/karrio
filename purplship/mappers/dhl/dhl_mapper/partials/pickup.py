import time
from pydhl.book_pickup_global_req_20 import BookPURequest
from pydhl.modify_pickup_global_req_20 import ModifyPURequest
from pydhl.cancel_pickup_global_req_20 import CancelPURequest
from pydhl.book_pickup_global_res_20 import BookPUResponse
from pydhl.modify_pickup_global_res_20 import ModifyPUResponse
from pydhl import pickupdatatypes_global_20 as PickpuDataTypes

from .interface import reduce, Union, Tuple, List, T, DHLMapperBase


class DHLMapperPartial(DHLMapperBase):
    def parse_book_puresponse(self, response) -> Tuple[T.PickupDetails, List[T.Error]]:
        ConfirmationNumbers = response.xpath(
            ".//*[local-name() = $name]", name="ConfirmationNumber"
        )
        success = len(ConfirmationNumbers) > 0
        if success:
            pickup = (
                BookPUResponse()
                if "BookPUResponse" in response.tag
                else ModifyPUResponse()
            )
            pickup.build(response)
        return (
            self._extract_pickup(pickup) if success else None,
            self.parse_error_response(response) if not success else [],
        )

    def parse_cancel_puresponse(self, response) -> Tuple[dict, List[T.Error]]:
        ConfirmationNumbers = response.xpath(
            ".//*[local-name() = $name]", name="ConfirmationNumber"
        )
        success = len(ConfirmationNumbers) > 0
        if success:
            cancellation = dict(
                confirmation_number=response.xpath(
                    ".//*[local-name() = $name]", name="ConfirmationNumber"
                )[0].text
            )
        return (
            cancellation if success else None,
            self.parse_error_response(response) if not success else [],
        )

    def create_tracking_pins(self, payload: T.tracking_request) -> List[str]:
        return payload.tracking_numbers

    def create_book_purequest(self, payload: T.pickup_request) -> BookPURequest:
        Requestor_, Place_, PickupContact_, Pickup_ = self._create_pickup_request(
            payload
        )

        return BookPURequest(
            Request=self.init_request(),
            schemaVersion="1.0",
            RegionCode=payload.extra.get("RegionCode") or "AM",
            Requestor=Requestor_,
            Place=Place_,
            PickupContact=PickupContact_,
            Pickup=Pickup_,
        )

    def create_modify_purequest(self, payload: T.pickup_request) -> ModifyPURequest:
        Requestor_, Place_, PickupContact_, Pickup_ = self._create_pickup_request(
            payload
        )

        return ModifyPURequest(
            Request=self.init_request(),
            schemaVersion="1.0",
            RegionCode=payload.extra.get("RegionCode") or "AM",
            ConfirmationNumber=payload.confirmation_number,
            Requestor=Requestor_,
            Place=Place_,
            PickupContact=PickupContact_,
            Pickup=Pickup_,
            OriginSvcArea=payload.extra.get("OriginSvcArea"),
        )

    def create_cancel_purequest(
        self, payload: T.pickup_cancellation_request
    ) -> CancelPURequest:
        return CancelPURequest(
            Request=self.init_request(),
            schemaVersion="2.0",
            RegionCode=payload.extra.get("RegionCode") or "AM",
            ConfirmationNumber=payload.confirmation_number,
            RequestorName=payload.person_name,
            CountryCode=payload.country_code,
            Reason=payload.extra.get("Reason") or "006",
            PickupDate=payload.pickup_date,
            CancelTime=time.strftime("%H:%M"),
        )

    """ Private functions """

    def _extract_pickup(
        self, pickup: Union[BookPUResponse, ModifyPURequest]
    ) -> T.PickupDetails:
        pickup_charge = (
            None
            if pickup.PickupCharge is None
            else T.ChargeDetails(
                name="Pickup Charge",
                amount=pickup.PickupCharge,
                currency=pickup.CurrencyCode,
            )
        )
        ref_times = (
            []
            if pickup.ReadyByTime is None
            else [T.TimeDetails(name="ReadyByTime", value=pickup.ReadyByTime)]
        ) + (
            []
            if pickup.CallInTime is None
            else [T.TimeDetails(name="CallInTime", value=pickup.CallInTime)]
        )
        return T.PickupDetails(
            carrier=self.client.carrier_name,
            confirmation_number=pickup.ConfirmationNumber,
            pickup_date=pickup.NextPickupDate,
            pickup_charge=pickup_charge,
            ref_times=ref_times,
        )

    def _create_pickup_request(
        self, payload: T.pickup_request
    ) -> Tuple[
        PickpuDataTypes.Requestor,
        PickpuDataTypes.Place,
        PickpuDataTypes.Contact,
        PickpuDataTypes.Pickup,
    ]:
        RequestorContact_ = (
            None
            if "RequestorContact" not in payload.extra
            else PickpuDataTypes.RequestorContact(
                PersonName=payload.extra.get("RequestorContact").get("PersonName"),
                Phone=payload.extra.get("RequestorContact").get("Phone"),
                PhoneExtension=payload.extra.get("RequestorContact").get(
                    "PhoneExtension"
                ),
            )
        )

        Requestor_ = PickpuDataTypes.Requestor(
            AccountNumber=payload.account_number,
            AccountType=payload.extra.get("AccountType") or "D",
            RequestorContact=RequestorContact_,
            CompanyName=payload.extra.get("CompanyName"),
        )

        Place_ = PickpuDataTypes.Place(
            City=payload.city,
            StateCode=payload.state_code,
            PostalCode=payload.postal_code,
            CompanyName=payload.company_name,
            CountryCode=payload.country_code,
            PackageLocation=payload.package_location or "...",
            LocationType="B" if payload.is_business else "R",
            Address1=payload.address_lines[0]
            if len(payload.address_lines) > 0
            else None,
            Address2=payload.address_lines[1]
            if len(payload.address_lines) > 1
            else None,
        )

        PickupContact_ = PickpuDataTypes.Contact(
            PersonName=payload.person_name, Phone=payload.phone_number
        )

        weight_ = (
            PickpuDataTypes.WeightSeg(
                Weight=payload.weight, WeightUnit=payload.weight_unit
            )
            if any([payload.weight, payload.weight_unit])
            else None
        )

        Pickup_ = PickpuDataTypes.Pickup(
            Pieces=payload.pieces,
            PickupDate=payload.date,
            ReadyByTime=payload.ready_time,
            CloseTime=payload.closing_time,
            SpecialInstructions=payload.instruction,
            RemotePickupFlag=payload.extra.get("RemotePickupFlag"),
            weight=weight_,
        )

        return Requestor_, Place_, PickupContact_, Pickup_
