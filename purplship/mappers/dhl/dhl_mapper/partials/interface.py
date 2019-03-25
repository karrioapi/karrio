import time
from typing import Tuple, List
from functools import reduce
from lxml import etree
from purplship.mappers.dhl import DHLClient
from purplship.domain import Types as T
from pydhl.datatypes_global_v61 import ServiceHeader, Request
from pydhl import (
    DCT_req_global as Req,
    ship_val_global_req_61 as ShipReq,
    DCT_Response_global as Res,
    tracking_request_known as Track,
    book_pickup_global_req_20 as BookPUReq,
    modify_pickup_global_req_20 as ModifPUReq,
    cancel_pickup_global_req_20 as CancelPUReq,
)


class DHLCapabilities:
    """
        DHL native service request types
    """

    """ Requests """

    def create_dct_request(self, payload: T.RateRequest) -> Req.DCTRequest:
        pass

    def create_dhltracking_request(
        self, payload: T.TrackingRequest
    ) -> Track.KnownTrackingRequest:
        pass

    def create_dhlshipment_request(
        self, payload: T.ShipmentRequest
    ) -> ShipReq.ShipmentRequest:
        pass

    def create_book_purequest(
        self, payload: T.PickupRequest
    ) -> BookPUReq.BookPURequest:
        pass

    def create_modify_purequest(
        self, payload: T.PickupRequest
    ) -> ModifPUReq.ModifyPURequest:
        pass

    def create_cancel_purequest(
        self, payload: T.PickupCancellationRequest
    ) -> CancelPUReq.CancelPURequest:
        pass

    """ Response """

    def parse_dct_response(
        self, response: etree.ElementBase
    ) -> Tuple[List[T.QuoteDetails], List[T.Error]]:
        pass

    def parse_dhltracking_response(
        self, response: etree.ElementBase
    ) -> Tuple[List[T.TrackingDetails], List[T.Error]]:
        pass

    def parse_dhlshipment_respone(
        self, response: etree.ElementBase
    ) -> Tuple[T.ShipmentDetails, List[T.Error]]:
        pass

    def parse_book_puresponse(
        self, response: etree.ElementBase
    ) -> Tuple[T.PickupDetails, List[T.Error]]:
        pass

    def parse_cancel_puresponse(
        self, response: etree.ElementBase
    ) -> Tuple[dict, List[T.Error]]:
        pass


class DHLMapperBase(DHLCapabilities):
    """
        DHL mapper base class
    """

    def __init__(self, client: DHLClient):
        self.client = client

    def init_request(self, **kwargs) -> Request:
        return Request(
            ServiceHeader=ServiceHeader(
                MessageReference="1234567890123456789012345678901",
                MessageTime=time.strftime("%Y-%m-%dT%H:%M:%S"),
                SiteID=self.client.site_id,
                Password=self.client.password,
            ),
            **kwargs
        )

    def parse_error_response(self, response) -> List[T.Error]:
        conditions = response.xpath(".//*[local-name() = $name]", name="Condition")
        return reduce(self._extract_error, conditions, [])

    def _extract_error(
        self, errors: List[T.Error], conditionNode: etree.ElementBase
    ) -> List[T.Error]:
        condition = Res.ConditionType()
        condition.build(conditionNode)
        return errors + [
            T.Error(
                code=condition.ConditionCode,
                message=condition.ConditionData,
                carrier=self.client.carrier_name,
            )
        ]
