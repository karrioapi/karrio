import time
from typing import Tuple, List, Union
from functools import reduce
from purplship.mappers.dhl import DHLClient
from purplship.domain import entities as E
from pydhl.datatypes_global_v61 import ServiceHeader, MetaData, Request
from pydhl import (
    DCT_req_global as Req,
    ship_val_global_req_61 as ShipReq,
    DCT_Response_global as Res,
    tracking_request_known as Track,
    tracking_response as TrackRes,
    book_pickup_global_req_20 as BookPUReq,
    modify_pickup_global_req_20 as ModifPUReq,
    cancel_pickup_global_req_20 as CancelPUReq,
    book_pickup_global_res_20 as BookPURes,
    modify_pickup_global_res_20 as ModifPURes,
    pickupdatatypes_global_20 as PickpuDataTypes
)


class DHLCapabilities: 
    """
        DHL native service request types
    """      

    """ Requests """

    def create_dct_request(self, payload: E.shipment_request) -> Req.DCTRequest:
        pass

    def create_dhltracking_request(self, payload: E.tracking_request) -> Track.KnownTrackingRequest:
        pass

    def create_dhlshipment_request(self, payload: E.shipment_request) -> ShipReq.ShipmentRequest:
        pass    

    def create_book_purequest(self, payload: E.pickup_request) -> BookPUReq.BookPURequest:
        pass
        
    def create_modify_purequest(self, payload: E.pickup_request) -> ModifPUReq.ModifyPURequest:
        pass

    def create_cancel_purequest(self, payload: E.pickup_cancellation_request) -> CancelPUReq.CancelPURequest:
        pass

    """ Response """ 
    
    def parse_dct_response(self, response: 'XMLElement') -> Tuple[List[E.QuoteDetails], List[E.Error]]:
        pass

    def parse_dhltracking_response(self, response: 'XMLElement') -> Tuple[List[E.TrackingDetails], List[E.Error]]:
        pass

    def parse_dhlshipment_respone(self, response: 'XMLElement') -> Tuple[E.ShipmentDetails, List[E.Error]]:
        pass

    def parse_book_puresponse(self, response: 'XMLElement') -> Tuple[E.PickupDetails, List[E.Error]]:
        pass

    def parse_cancel_puresponse(self, response: 'XMLElement') -> Tuple[dict, List[E.Error]]:
        pass


class DHLMapperBase(DHLCapabilities):
    """
        DHL mapper base class
    """       
    def __init__(self, client: DHLClient):
        self.client = client  

    def init_request(self) -> Request:
        ServiceHeader_ = ServiceHeader(
            MessageReference="1234567890123456789012345678901",
            MessageTime=time.strftime('%Y-%m-%dT%H:%M:%S'),
            SiteID=self.client.site_id,
            Password=self.client.password
        )
        return Request(ServiceHeader=ServiceHeader_)

    def parse_error_response(self, response) -> List[E.Error]:
        conditions = response.xpath(
            './/*[local-name() = $name]', name="Condition")
        return reduce(self._extract_error, conditions, [])

    def _extract_error(self, errors: List[E.Error], conditionNode: 'XMLElement') -> List[E.Error]:
        condition = Res.ConditionType()
        condition.build(conditionNode)
        return errors + [
            E.Error(code=condition.ConditionCode,
                    message=condition.ConditionData, carrier=self.client.carrier_name)
        ]
