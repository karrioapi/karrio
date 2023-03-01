import io
import re
import ssl
import uuid
import asyncio
import logging
import base64
import urllib.parse
from PyPDF2 import PdfMerger
from PIL import Image, ImageFile
from urllib.error import HTTPError
from urllib.request import urlopen, Request
from typing import List, TypeVar, Callable, Optional, Any, cast
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)
ssl._create_default_https_context = ssl._create_unverified_context
ImageFile.LOAD_TRUNCATED_IMAGES = True
T = TypeVar("T")
S = TypeVar("S")
NEW_LINE = """
"""


def identity(value: Any) -> Any:
    return value


def to_buffer(encoded_file: str, **kwargs) -> io.BytesIO:
    content = base64.b64decode(encoded_file, **kwargs)
    buffer = io.BytesIO()
    buffer.write(content)

    return buffer


def image_to_pdf(image_str: str, rotate: int = None) -> str:
    buffer = to_buffer(image_str)
    _image = Image.open(buffer)
    image = (
        _image.rotate(rotate, Image.NEAREST, expand = True)
        if rotate is not None
        else _image
    )

    new_buffer = io.BytesIO()
    image.save(new_buffer, format="PDF")

    return base64.b64encode(new_buffer.getvalue()).decode("utf-8")


def bundle_pdfs(base64_strings: List[str]) -> PdfMerger:
    merger = PdfMerger(strict=False)

    for b64_str in base64_strings:
        buffer = to_buffer(b64_str)
        merger.append(buffer)

    return merger


def bundle_imgs(base64_strings: List[str]) -> Image:
    image_buffers = [
        io.BytesIO(base64.b64decode(b64_str)) for b64_str in base64_strings
    ]
    images = [Image.open(buffer) for buffer in image_buffers]
    widths, heights = zip(*(i.size for i in images))

    max_width = max(widths)
    total_height = sum(heights)

    image = Image.new("RGB", (max_width, total_height))

    x_offset = 0
    for im in images:
        image.paste(im, (0, x_offset))
        x_offset += im.size[1]

    return image


def bundle_zpls(base64_strings: List[str]) -> str:
    doc = ""
    for b64_str in base64_strings:
        doc += f'{base64.b64decode(b64_str).decode("utf-8")}{NEW_LINE}'

    return doc


def bundle_base64(base64_strings: List[str], format: str = "PDF") -> str:
    """Return a base64 string from a list of base64 strings."""
    result = io.BytesIO()

    if format == "PDF":
        pdf_buffer = bundle_pdfs(base64_strings)
        pdf_buffer.write(result)

    elif "ZPL" in format:
        content = bundle_zpls(base64_strings)
        result.write(content.encode("utf-8"))

    else:
        image = bundle_imgs(base64_strings)
        image.save(result, format)

    return base64.b64encode(result.getvalue()).decode("utf-8")


def decode_bytes(byte):
    return byte.decode("utf-8")


def process_request(
    request_id: str,
    trace: Callable[[Any, str], Any] = None,
    **kwargs,
) -> Request:
    payload = (
        dict(data=bytearray(kwargs["data"], encoding="utf-8"))
        if "data" in kwargs
        else {}
    )

    if trace:
        trace(
            {
                "request_id": request_id,
                "url": urllib.parse.unquote(kwargs.get("url")),
                **({"data": kwargs.get("data")} if "data" in kwargs else {}),
            },
            "request",
        )

    _request = Request(**{**kwargs, **payload})

    logger.info(f"Request URL:: {_request.full_url}")

    return _request


def process_response(
    request_id: str,
    response,
    decoder: Callable,
    trace: Callable[[Any, str], Any] = None,
) -> str:
    try:
        _response = decoder(response)
    except Exception as e:
        logger.error(e)
        _response = response

    if trace:
        _content = _response if isinstance(_response, str) else "undecoded bytes..."
        trace({"request_id": request_id, "response": _content}, "response")

    # logger.debug(f"Response content:: {_response}")

    return _response


def process_error(
    request_id: str,
    error: HTTPError,
    on_error: Callable[[HTTPError], str] = None,
    trace: Callable[[Any, str], Any] = None,
) -> str:
    logger.error(error, exc_info=False)

    if on_error is not None:
        _error = on_error(error)
    else:
        _error = error.read().decode("utf-8")

    if trace:
        trace({"request_id": request_id, "error": _error}, "error")

    logger.debug(f"Error content:: {error}")

    return _error


def request(
    decoder: Callable = decode_bytes,
    on_error: Callable[[HTTPError], str] = None,
    trace: Callable[[Any, str], Any] = None,
    **kwargs,
) -> str:
    """Return an HTTP response body.

    make a http request (wrapper around Request method from built in urllib)
    """

    _request_id = str(uuid.uuid4())
    logger.debug(f"sending request ({_request_id})...")

    try:
        _request = process_request(_request_id, trace, **kwargs)

        with urlopen(_request) as f:
            _response = process_response(_request_id, f.read(), decoder, trace=trace)

    except HTTPError as e:
        _response = process_error(_request_id, e, on_error=on_error, trace=trace)

    return _response


def exec_parrallel(
    function: Callable, sequence: List[S], max_workers: int = None
) -> List[T]:
    """Return a list of result for function execution on each element of the sequence."""
    workers = len(sequence) or max_workers or 2
    with ThreadPoolExecutor(max_workers=workers) as executor:
        requests = {executor.submit(function, item): item for item in sequence}
        return [response.result() for response in as_completed(requests)]


def exec_async(action: Callable, sequence: List[S]) -> List[T]:
    async def run_tasks(loop):
        return await asyncio.gather(
            *[loop.run_in_executor(None, lambda: action(args)) for args in sequence]
        )

    def run_loop():
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(run_tasks(loop))
        loop.close()

        return result

    result = ThreadPoolExecutor().submit(run_loop).result()
    return cast(List[T], result)


class Location:
    def __init__(self, value: Optional[str], **kwargs):
        self.value = value
        self.extra = kwargs

    @property
    def as_zip4(self) -> Optional[str]:
        if re.match(r"/^SW\d{4}$/", self.value or ""):
            return self.value

        return None

    @property
    def as_zip5(self) -> Optional[str]:
        if not re.match(r"/^SW\d{5}$/", self.value or ""):
            return self.value

        return None

    @property
    def as_country_name(self) -> str:
        from karrio.core.units import Country

        if self.value in Country:
            return Country[self.value].value

        return self.value

    @property
    def as_state_name(self) -> str:
        from karrio.core.units import CountryState

        try:
            country: Any = CountryState.__members__.get(self.extra["country"])
            if self.value in getattr(country, "value", []):
                return country.value[self.value].value

            return self.value
        except KeyError as e:
            raise Exception(
                'Missing country code. e.g: Location(state_code, country="US").as_state_name'
            ) from e