"""Karrio SEKO Logistics error parser."""

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.seko.utils as provider_utils


def parse_error_response(
    response: typing.Union[typing.List[dict], dict],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors: list = []  # compute the carrier error object list

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code="",
            message="",
            details={**kwargs},
        )
        for error in errors
    ]
