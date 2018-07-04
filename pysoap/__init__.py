from .envelope import Header, Body, Envelope

def create_envelope(body_content):
    body = Body()
    body.add_anytypeobjs_(body_content)
    return Envelope(Body=body)