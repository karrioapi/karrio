from io import StringIO
import urllib.request
from xmltodict import parse
from attr.exceptions import NotAnAttrsClassError
import attr
import ssl
import json
from json import JSONEncoder
import asyncio
from lxml import etree
from purplship.core.utils.xml import Element
from typing import List, TypeVar, Callable, Any, Union
from concurrent.futures import ThreadPoolExecutor, as_completed

ctx = ssl._create_unverified_context()
T = TypeVar("T")
S = TypeVar("S")


def export(xml_element: Element, **kwds) -> str:
    """Return a XML string.

    invoke the export method of generated type to return the subsequent XML represented
    """
    output = StringIO()
    xml_element.export(output, 0, **kwds)
    return output.getvalue()


def request(**args) -> str:
    """Return an HTTP response body.

    make a http request (wrapper around Request method from built in urllib)
    """
    try:
        req = urllib.request.Request(**args)
        with urllib.request.urlopen(req, context=ctx) as f:
            return f.read().decode("utf-8")
    except urllib.request.HTTPError as e:
        return e.read().decode("utf-8")


def to_xml(xml_str: str) -> Element:
    """Return a XML element instance (from lxml library).

    parse xml string to node
    """
    return etree.fromstring(bytes(bytearray(xml_str, encoding="utf-8")))


def xml_tostring(xml_element: Element, encoding: str = "utf-8") -> str:
    return str(etree.tostring(xml_element), encoding)


def jsonify_xml(xml_str: str) -> dict:
    """Return a python dictionary.

    parse the given XML input and convert it into a dictionary.
    """
    return parse(xml_str)


class Encoder(JSONEncoder):
    def default(self, o):
        try:
            return attr.asdict(o)
        except NotAnAttrsClassError:
            if hasattr(o, "__dict__"):
                return o.__dict__
            else:
                return o


def jsonify(entity: Union[dict, T]) -> str:
    """Return a JSON.

    recursively parse a data type using __dict__ into a JSON
    """
    return json.dumps(
        entity,
        cls=Encoder,
        sort_keys=True,
        indent=4,
    )


def to_dict(entity: Any) -> dict:
    """Return a python dictionary.

    recursively parse a data type using __dict__ into a JSON
    """
    return json.loads(
        jsonify(entity) if not isinstance(entity, str) else entity,
        object_hook=lambda d: {k: v for k, v in d.items() if v not in(None, [], "")}
    )


def bundle_xml(xml_strings: List[str]) -> str:
    """Return a XML string.

    <wrapper>{all the XML trees concatenated}</wrapper>
    """
    bundle = "".join([xml_tostring(to_xml(x)) for x in xml_strings])
    return f"<wrapper>{bundle}</wrapper>"


def exec_parrallel(function: Callable, sequence: List[S], max_workers: int = None) -> List[T]:
    """Return a list of result for function execution on each element of the sequence."""
    with ThreadPoolExecutor(max_workers=max_workers or len(sequence)) as executor:
        requests = {executor.submit(function, item): item for item in sequence}
        return [response.result() for response in as_completed(requests)]


def exec_async(function: Callable, sequence: List[tuple], max_workers: int = None) -> List[T]:
    def async_function(args):
        return function(*args)

    async def execute():
        with ThreadPoolExecutor(max_workers=max_workers or len(sequence)) as executor:
            event_loop = asyncio.get_event_loop()
            requests = [
                event_loop.run_in_executor(
                    executor,
                    async_function,
                    params
                ) for params in sequence
            ]
            return [r for r in await asyncio.gather(*requests)]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(execute())
    loop.close()
    return result
