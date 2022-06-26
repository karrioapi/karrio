import io
import re
import asyncio
import logging
import base64
from PIL import Image, ImageFile
from PyPDF2 import PdfFileMerger
from simple_zpl2 import ZPLDocument
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from typing import List, TypeVar, Callable, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)
ImageFile.LOAD_TRUNCATED_IMAGES = True
T = TypeVar("T")
S = TypeVar("S")


def identity(value: Any) -> Any:
    return value


def image_to_pdf(image_str: str) -> str:
    content = base64.b64decode(image_str)
    buffer = io.BytesIO()
    buffer.write(content)
    image = Image.open(buffer)
    new_buffer = io.BytesIO()
    image.save(new_buffer, format="PDF")

    return base64.b64encode(new_buffer.getvalue()).decode("utf-8")


def bundle_pdfs(base64_strings: List[str]) -> PdfFileMerger:
    merger = PdfFileMerger(strict=False)

    for b64_str in base64_strings:
        content = base64.b64decode(b64_str)
        buffer = io.BytesIO()
        buffer.write(content)
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
    doc = ZPLDocument()
    for b64_str in base64_strings:
        doc.add_zpl_raw(base64.b64decode(b64_str).decode("utf-8"))

    return doc.zpl_text


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


def request(
    decoder: Callable = decode_bytes,
    on_error: Callable[[HTTPError], str] = None,
    **args,
) -> str:
    """Return an HTTP response body.

    make a http request (wrapper around Request method from built in urllib)
    """
    logger.debug(f"sending request")
    try:
        req = Request(**args)
        logger.info(f"Request URL:: {req.full_url}")
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


def exec_parrallel(
    function: Callable, sequence: List[S], max_workers: int = 2
) -> List[T]:
    """Return a list of result for function execution on each element of the sequence."""
    with ThreadPoolExecutor(max_workers=max_workers or len(sequence)) as executor:
        requests = {executor.submit(function, item): item for item in sequence}
        return [response.result() for response in as_completed(requests)]


def exec_async(action: Callable, sequence: List[S]) -> List[T]:
    async def async_action(args):
        return action(args)

    async def run_tasks():
        return await asyncio.gather(*[async_action(args) for args in sequence])

    return asyncio.run(run_tasks())


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
