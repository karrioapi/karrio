from pysoap.envelope import Header, Body, Envelope
from purplship.core.utils.xml import Element


def create_envelope(
    body_content: Element,
    header_content: Element = None,
    header_prefix: str = None,
    body_prefix: str = None,
    header_tag_name: str = None,
    body_tag_name: str = None,
    envelope_prefix: str = "tns"
) -> Envelope:
    header = None
    if header_content is not None:
        header_content.ns_prefix_ = header_prefix or header_content.ns_prefix_
        header_content.original_tagname_ = header_tag_name or header_content.original_tagname_
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
