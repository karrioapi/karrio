from pysoap.envelope import Header, Body, Envelope


def create_envelope(body_content, header_content=None) -> Envelope:
    header = None
    if header_content is not None:
        header = Header()
        header.add_anytypeobjs_(header_content)

    body = Body()
    body.add_anytypeobjs_(body_content)

    return Envelope(Header=header, Body=body)


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
