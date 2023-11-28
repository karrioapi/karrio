import karrio.schemas.dhl_express.dct_response_global_3_0 as dhl
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dhl_express.utils as provider_utils


def parse_error_response(
    response: lib.Element,
    settings: provider_utils.Settings,
) -> typing.List[models.Message]:
    errors = lib.find_element("Condition", response, dhl.ConditionType)

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.ConditionCode,
            message=error.ConditionData,
        )
        for error in errors
    ]
