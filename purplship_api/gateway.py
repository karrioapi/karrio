import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Tuple, Union, Callable, Type, TypeVar
from purplship.domain import Proxy
from purplship.domain.Types import (
    ShipmentRequest,
    RateRequest,
    TrackingRequest,
    PickupRequest,
    QuoteDetails,
    TrackingDetails,
    ShipmentDetails,
    PickupDetails,
    Error
)
from purplship.domain.Types.errors import OriginNotServicedError
from functools import reduce
from gds_helpers import export, to_dict
from lxml import etree
from purplship_core.settings import PURPLSHIP_SETTINGS

logger = logging.getLogger(__name__)

T = Type[Union[ShipmentRequest, TrackingRequest]]
ISerializable = TypeVar('ISerializable')
DEFAULTS = PURPLSHIP_SETTINGS.get('DEFAULTS')


class Gateway(Proxy):
    """Proxy interface methods."""

    @staticmethod
    def get_quotes(payload: RateRequest, proxies: List[Proxy] = []) -> Tuple[List[QuoteDetails], List[Error]]:
        return _parallellize(payload, _process_quotes, proxies)

    @staticmethod
    def get_tracking(payload: ShipmentRequest, proxies: List[Proxy] = []) -> Tuple[List[TrackingDetails], List[Error]]:
        return _parallellize(payload, _process_tracking, proxies)

    @staticmethod
    def create_shipment(payload: ShipmentRequest, proxy: Proxy) -> Tuple[ShipmentDetails, List[Error]]:
        return _process_shipment(payload, proxy)

    @staticmethod
    def request_pickup(payload: PickupRequest, proxy: Proxy) -> Tuple[PickupDetails, List[Error]]:
        return _process_pickup(payload, proxy)

    @staticmethod
    def modify_pickup(payload: PickupRequest, proxy: Proxy) -> Tuple[PickupDetails, List[Error]]:
        return _process_pickup(payload, proxy, update=True)


""" Helper functions """


def parse(entity: ISerializable):
    try:
        return export(entity)
    except:
        pass
    try:
        return etree.tostring(entity)
    except:
        pass
    try:
        return to_dict(entity)
    except:
        return None


def _parallellize(payload: T, processor: Callable, proxies: Dict[str, Proxy] = []) -> Tuple[List[T], List[Error]]:
    if len(proxies) <= 0:
        raise Exception('no valid carriers provided')

    async def process():
        with ThreadPoolExecutor(max_workers=len(proxies.items())) as executor:
            loop = asyncio.get_event_loop()
            requests = [
                loop.run_in_executor(
                    executor,
                    processor,
                    (payload, proxy)
                ) for _, proxy in proxies.items()
            ]
            result = [r for r in await asyncio.gather(*(requests))]
        return reduce(lambda c, r: (c[0] + r[0], c[1] + r[1]), result, ([], []))
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    summary = loop.run_until_complete(process())
    loop.close()
    return summary


def _process_quotes(args: Tuple[RateRequest, Proxy]) -> Tuple[List[QuoteDetails], List[Error]]:
    payload, proxy = args
    try:
        custom_payload = RateRequest(**to_dict(payload))
        if custom_payload.shipper.account_number is None:
            custom_payload.shipper.account_number = DEFAULTS.get(
                proxy.client.carrier_name, {}
            ).get("account_number", "")

        request = proxy.mapper.create_quote_request(custom_payload)
        response = proxy.get_quotes(request)
        logger.debug((proxy.client.carrier_name, parse(request), parse(response)))
        return proxy.mapper.parse_quote_response(response)

    except OriginNotServicedError as e:
        logger.error(('error', proxy.client.carrier_name, f"{e}"))
        return [[], [Error(
            carrier=proxy.client.carrier_name,
            code="400",
            message=f"{e}"
        )]]
    except Exception as e:
        logger.error(('error', e.args, proxy.client.carrier_name))
        return [[], [Error(
            carrier=proxy.client.carrier_name,
            code="500",
            message="An error occured while processing quotes"
        )]]


def _process_tracking(args: Tuple[TrackingRequest, Proxy]) -> Tuple[List[TrackingDetails], List[Error]]:
    payload, proxy = args
    try:
        request = proxy.mapper.create_tracking_request(payload)
        response = proxy.get_tracking(request)
        logger.debug((proxy.client.carrier_name, payload, parse(request), parse(response)))
        return proxy.mapper.parse_tracking_response(response)
    except Exception as e:
        logger.error((e.args, payload, proxy))
        return [[], [Error(
            carrier=proxy.client.carrier_name,
            code="500",
            message="An error occured while processing tracking"
        )]]


def _process_pickup(payload: PickupRequest, proxy: Proxy, update: bool = False) -> Tuple[PickupDetails, List[Error]]:
    logger.debug(("start processing pickup request", proxy.client.carrier_name))
    try:
        if payload.account_number is None:
            payload.account_number = DEFAULTS.get(
                proxy.client.carrier_name, {}
            ).get("account_number", "")

        request = proxy.mapper.modify_pickup_request(payload) if update else proxy.mapper.create_pickup_request(payload)
        response = proxy.modify_pickup(request) if update else proxy.request_pickup(request)
        logger.debug((proxy.client.carrier_name, parse(request), response))
        return proxy.mapper.parse_shipment_response(response)
    except Exception as e:
        logger.error(('error processing pickup request', e.args, payload, proxy))
        return [[], [Error(
            carrier=proxy.client.carrier_name,
            code="500",
            message=f"An error occured while processing pickup request: {e.args}"
        )]]


def _process_shipment(payload: ShipmentRequest, proxy: Proxy) -> Tuple[ShipmentDetails, List[Error]]:
    try:
        custom_payload = RateRequest(**to_dict(payload))
        if custom_payload.shipper.account_number is None:
            custom_payload.shipper.account_number = DEFAULTS.get(
                proxy.client.carrier_name, {}
            ).get("account_number", "")

        request = proxy.mapper.create_shipment_request(custom_payload)
        response = proxy.create_shipment(request)
        logger.debug((proxy.client.carrier_name, parse(request), response))
        return proxy.mapper.parse_shipment_response(response)
    except Exception as e:
        logger.error((e.args, payload, proxy))
        return [[], [Error(
            carrier=proxy.client.carrier_name,
            code="500",
            message=f"An error occured while processing shipping: {e.args}"
        )]]
