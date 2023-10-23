import karrio.schemas.tnt.rating_response as tnt
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.tnt.utils as provider_utils


def parse_error_response(
    response,
    settings: provider_utils.Settings,
) -> typing.List[models.Message]:
    structure_errors = lib.find_element("ErrorStructure", response)
    broken_rules_nodes = lib.find_element("brokenRules", response)
    broken_rule_nodes = lib.find_element("brokenRule", response)
    runtime_errors = lib.find_element("runtime_error", response)
    parse_errors = lib.find_element("parse_error", response)
    ERRORS = lib.find_element("ERROR", response)
    errors = lib.find_element("Error", response)
    faults = lib.find_element("fault", response)

    return [
        *[_extract_structure_error(node, settings) for node in structure_errors],
        *[_extract_broken_rules(node, settings) for node in broken_rules_nodes],
        *[_extract_broken_rule(node, settings) for node in broken_rule_nodes],
        *[_extract_runtime_error(node, settings) for node in runtime_errors],
        *[_extract_parse_error(node, settings) for node in parse_errors],
        *[_extract_structure_error(node, settings) for node in errors],
        *[_extract_error(node, settings) for node in ERRORS],
        *[_extract_faut(node, settings) for node in faults],
    ]


def _extract_structure_error(
    node: lib.Element, settings: provider_utils.Settings
) -> models.Message:
    return models.Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        # carrier error info
        code=lib.find_element("Code", node, first=True).text,
        message=lib.find_element("Message", node, first=True).text,
    )


def _extract_broken_rules(
    node: lib.Element, settings: provider_utils.Settings
) -> models.Message:
    return models.Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        # carrier error info
        code=lib.find_element("errorCode", node, first=True).text,
        message=lib.find_element("errorMessage", node, first=True).text,
    )


def _extract_broken_rule(
    node: lib.Element, settings: provider_utils.Settings
) -> models.Message:
    error = lib.to_object(tnt.brokenRule, node)

    return models.Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        # carrier error info
        code=getattr(error, "code", None),
        message=getattr(error, "description", None),
        details=dict(messageType=getattr(error, "messageType", None)),
    )


def _extract_runtime_error(
    node: lib.Element, settings: provider_utils.Settings
) -> models.Message:
    error = lib.to_object(tnt.runtimeError, node)

    return models.Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        # carrier error info
        code="runtime",
        message=getattr(error, "errorReason", None),
        details=dict(srcTxt=getattr(error, "errorSrcText", None)),
    )


def _extract_parse_error(
    node: lib.Element, settings: provider_utils.Settings
) -> models.Message:
    error = lib.to_object(tnt.parseError, node)

    return models.Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        # carrier error info
        code="parsing",
        message=getattr(error, "errorReason", None),
        details=dict(srcText=getattr(error, "errorSrcText", None)),
    )


def _extract_error(
    node: lib.Element, settings: provider_utils.Settings
) -> models.Message:
    return models.Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        # carrier error info
        code=lib.find_element("CODE", node, first=True).text,
        message=lib.find_element("DESCRIPTION", node, first=True).text,
    )


def _extract_faut(
    node: lib.Element, settings: provider_utils.Settings
) -> models.Message:
    return models.Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        # carrier error info
        code=lib.find_element("key", node, first=True).text,
    )
