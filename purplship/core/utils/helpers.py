import io
import attr
import json
import asyncio
import logging
import base64
from PIL import Image
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from xmltodict import parse
from purplship.core.utils.xml import Element, fromstring, tostring
from typing import List, TypeVar, Callable, Any, Union
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)
T = TypeVar("T")
S = TypeVar("S")


def concat_str(*args, join: bool = False):
    strings = [s for s in args if s != ""]
    if len(strings) == 0:
        return None
    return strings if not join else " ".join(strings)


def export(xml_element: Element, **kwds) -> str:
    """Return a XML string.

    invoke the export method of generated type to return the subsequent XML represented
    """
    output = io.StringIO()
    xml_element.export(output, 0, **kwds)
    return output.getvalue()


def decode_bytes(byte):
    return byte.decode("utf-8")


def gif_to_pdf(gif_str: str) -> str:
    content = base64.b64decode(gif_str)
    buffer = io.BytesIO()
    buffer.write(content)
    image = Image.open(buffer)
    new_buffer = io.BytesIO()
    image.save(new_buffer, format="PDF")
    return base64.b64encode(new_buffer.getvalue()).decode("utf-8")


def request(decoder: Callable = decode_bytes, on_error: Callable[[HTTPError], str] = None, **args) -> str:
    """Return an HTTP response body.

    make a http request (wrapper around Request method from built in urllib)
    """
    logger.debug(f"sending request")
    try:
        req = Request(**args)
        with urlopen(req) as f:
            res = f.read()
            try:
                res = decoder(res)
            except Exception as e:
                logger.exception(e)

            logger.debug(f"response content {res}")
            return res
    except HTTPError as e:
        logger.exception(e)

        if on_error is not None:
            return on_error(e)

        error = e.read().decode("utf-8")
        logger.debug(f"error response content {error}")
        return error


def to_xml(xml_str: str) -> Element:
    """Return a XML element instance (from lxml library).

    parse xml string to node
    """
    return fromstring(bytes(bytearray(xml_str, encoding="utf-8")))


def xml_tostring(xml_element: Element, encoding: str = "utf-8") -> str:
    return str(tostring(xml_element), encoding)


def jsonify_xml(xml_str: str) -> dict:
    """Return a python dictionary.

    parse the given XML input and convert it into a dictionary.
    """
    return parse(xml_str)


@attr.s(auto_attribs=True)
class JWrapper:
    value: Any


def jsonify(entity: Union[dict, T]) -> str:
    """Return a JSON.

    recursively parse a data type using __dict__ into a JSON
    """
    return json.dumps(
        attr.asdict(JWrapper(value=entity)).get("value"),
        default=lambda o: o.__dict__ if hasattr(o, "__dict__") else o,
        sort_keys=True,
        indent=4,
    )


def to_dict(entity: Any) -> dict:
    """Return a python dictionary.

    recursively parse a data type using __dict__ into a JSON
    """
    return json.loads(
        jsonify(entity) if not isinstance(entity, str) else entity,
        object_hook=lambda d: {k: v for k, v in d.items() if v not in (None, [], "")},
    )


def bundle_xml(xml_strings: List[str]) -> str:
    """Return a XML string.

    <wrapper>{all the XML trees concatenated}</wrapper>
    """
    bundle = "".join([xml_tostring(to_xml(x)) for x in xml_strings if x is not None and x != ""])
    return f"<wrapper>{bundle}</wrapper>"


def exec_parrallel(
    function: Callable, sequence: List[S], max_workers: int = None
) -> List[T]:
    """Return a list of result for function execution on each element of the sequence."""
    with ThreadPoolExecutor(max_workers=max_workers or len(sequence)) as executor:
        requests = {executor.submit(function, item): item for item in sequence}
        return [response.result() for response in as_completed(requests)]


def exec_async(action: Callable[[S], T], sequence: List[S]) -> List[T]:
    async def async_action(args):
        return action(args)

    async def run_tasks():
        return await asyncio.gather(*[async_action(args) for args in sequence])

    return asyncio.run(run_tasks())
