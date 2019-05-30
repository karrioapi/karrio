"""PurplShip carriers proxies initialization module."""


from typing import Dict, Tuple, List
from purplship_core.settings import PURPLSHIP_SETTINGS

import purplship
from purplship.domain import Proxy


def register_carriers(carriers: List[dict]):
    """Create a record of registered carriers."""
    try:
        return {
            carrier['id']: purplship.gateway[carrier['key']].create({**carrier['settings']})
            for carrier in carriers
        }
    except Exception as e:
        raise Exception(f'Failed to register shipping carriers: {e}')


def prune_carrier(request_data: dict) -> Tuple[dict, Dict[str, Proxy]]:
    """Returns a Tuple of the request data without the extra 'carriers' keys
    and a dictionary of proxies specified in the request.
    """
    carriers = request_data['carriers'] if 'carriers' in request_data and len(request_data['carriers']) > 0 else list(Proxies.keys())
    return (
      remove_carriers_key(request_data),
      filter_proxies(carriers)
    )


def remove_carriers_key(request_data: dict) -> dict:
    return {k: v for k, v in request_data.items() if k != 'carriers'}


def filter_proxies(carriers: List[str]) -> Dict[str, Proxy]:
    return {k: v for k, v in Proxies.items() if k in carriers}


"""Shipping carriers registration."""
Proxies = register_carriers(PURPLSHIP_SETTINGS.get('CARRIERS'))
