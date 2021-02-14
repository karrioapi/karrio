from typing import List, Union, Any
from pysoap.envelope import Header, Body, Envelope, Fault
from purplship.core.utils.xml import GenerateDSAbstract, Element, XMLPARSER
from purplship.core.settings import Settings
from purplship.core.models import Message


def create_envelope(
    body_content: Union[GenerateDSAbstract, Any],
    header_content: Union[GenerateDSAbstract, Any] = None,
    header_prefix: str = None,
    body_prefix: str = None,
    header_tag_name: str = None,
    body_tag_name: str = None,
    envelope_prefix: str = "tns",
) -> Envelope:
    header = None
    if header_content is not None:
        header_content.ns_prefix_ = header_prefix or header_content.ns_prefix_
        header_content.original_tagname_ = (
            header_tag_name or header_content.original_tagname_
        )
        header = Header()
        header.add_anytypeobjs_(header_content)

    body_content.ns_prefix_ = body_prefix or body_content.ns_prefix_
    body_content.original_tagname_ = body_tag_name or body_content.original_tagname_
    body = Body()
    body.add_anytypeobjs_(body_content)

    envelope = Envelope(Header=header, Body=body)
    envelope.ns_prefix_ = envelope_prefix
    envelope.Body.ns_prefix_ = envelope.ns_prefix_
    if envelope.Header is not None:
        envelope.Header.ns_prefix_ = envelope.ns_prefix_
    return envelope


def clean_namespaces(
    envelope_str: str,
    envelope_prefix: str,
    body_child_name: str,
    header_child_name: str = "UnspecifiedTag",
    header_child_prefix: str = "",
    body_child_prefix: str = "",
):
    return (
        envelope_str.replace(
            "<%s%s" % (envelope_prefix, header_child_name),
            "<%s%s" % (header_child_prefix, header_child_name),
        )
        .replace(
            "</%s%s" % (envelope_prefix, header_child_name),
            "</%s%s" % (header_child_prefix, header_child_name),
        )
        .replace(
            "<%s%s" % (envelope_prefix, body_child_name),
            "<%s%s" % (body_child_prefix, body_child_name),
        )
        .replace(
            "</%s%s" % (envelope_prefix, body_child_name),
            "</%s%s" % (body_child_prefix, body_child_name),
        )
    )


def apply_namespaceprefix(item, prefix: str, special_prefixes: dict = None, item_name: str = None):
    if special_prefixes is None:
        special_prefixes = {}

    if isinstance(item, list):
        [apply_namespaceprefix(child, prefix, special_prefixes, item_name) for child in item]
    elif hasattr(item, "export"):
        item.ns_prefix_ = prefix
        children_prefix = special_prefixes.get(f'{item_name}_children', prefix)
        children = [
            (name, node) for name, node in item.__dict__.items()
            if name[-1:] != "_" and node is not None
        ]
        for name, node in children:
            special_prefix = special_prefixes.get(name, children_prefix)
            setattr(item, f"{name}_nsprefix_", special_prefix)
            apply_namespaceprefix(node, special_prefix, special_prefixes, name)


def extract_fault(response: Element, settings: Settings) -> List[Message]:
    faults = [
        XMLPARSER.build(Fault, node)
        for node in response.xpath(".//*[local-name() = $name]", name="Fault")
    ]
    return [
        Message(
            code=fault.faultcode,
            message=fault.faultstring,
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
        )
        for fault in faults
    ]
