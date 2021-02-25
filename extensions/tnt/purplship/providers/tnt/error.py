from typing import List
from tnt_lib.track_response_v3_1 import ErrorStructure
from tnt_lib.label_response import brokenRules, fault
from tnt_lib.pricing_response import brokenRule, parseError, runtimeError
from tnt_lib.shipment_response import ERROR
from purplship.core.models import Message
from purplship.core.utils import Element, XP
from purplship.providers.tnt import Settings


def parse_error_response(response, settings: Settings) -> List[Message]:
    structure_errors = response.xpath(".//*[local-name() = $name]", name="ErrorStructure")
    broken_rules_nodes = response.xpath(".//*[local-name() = $name]", name="brokenRules")
    broken_rule_nodes = response.xpath(".//*[local-name() = $name]", name="brokenRule")
    runtime_errors = response.xpath(".//*[local-name() = $name]", name="runtime_error")
    parse_errors = response.xpath(".//*[local-name() = $name]", name="parse_error")
    errors = response.xpath(".//*[local-name() = $name]", name="ERROR")
    faults = response.xpath(".//*[local-name() = $name]", name="fault")

    return [
        *[_extract_structure_error(node, settings) for node in structure_errors],
        *[_extract_broken_rules(node, settings) for node in broken_rules_nodes],
        *[_extract_broken_rule(node, settings) for node in broken_rule_nodes],
        *[_extract_runtime_error(node, settings) for node in runtime_errors],
        *[_extract_parse_error(node, settings) for node in parse_errors],
        *[_extract_error(node, settings) for node in errors],
        *[_extract_faut(node, settings) for node in faults],
    ]


def _extract_structure_error(node: Element, settings: Settings) -> Message:
    error = XP.build(ErrorStructure, node)

    return Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        # carrier error info
        code=error.Code,
        message=error.Message,
    )


def _extract_broken_rules(node: Element, settings: Settings) -> Message:
    error = XP.build(brokenRules, node)

    return Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        # carrier error info
        code=error.errorCode,
        message=error.errorDescription,
    )


def _extract_broken_rule(node: Element, settings: Settings) -> Message:
    error = XP.build(brokenRule, node)

    return Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        # carrier error info
        code=error.code,
        message=error.description,
        details=dict(messageType=error.messageType)
    )


def _extract_runtime_error(node: Element, settings: Settings) -> Message:
    error = XP.build(runtimeError, node)

    return Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        # carrier error info
        code='runtime',
        message=error.errorReason,
        details=dict(srcTxt=error.errorSrcText)
    )


def _extract_parse_error(node: Element, settings: Settings) -> Message:
    error = XP.build(parseError, node)

    return Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        # carrier error info
        code='parsing',
        message=error.errorReason,
        details=dict(srcText=error.errorSrcText)
    )


def _extract_error(node: Element, settings: Settings) -> Message:
    error = XP.build(ERROR, node)

    return Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        # carrier error info
        code=error.CODE,
        message=error.DESCRIPTION,
    )


def _extract_faut(node: Element, settings: Settings) -> Message:
    error = XP.build(fault, node)

    return Message(
        # context info
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,

        # carrier error info
        code=error.key
    )
