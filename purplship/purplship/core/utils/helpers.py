import io
import asyncio
import logging
import base64
from PIL import Image
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from typing import List, TypeVar, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)
T = TypeVar("T")
S = TypeVar("S")


def gif_to_pdf(gif_str: str) -> str:
    content = base64.b64decode(gif_str)
    buffer = io.BytesIO()
    buffer.write(content)
    image = Image.open(buffer)
    new_buffer = io.BytesIO()
    image.save(new_buffer, format="PDF")
    return base64.b64encode(new_buffer.getvalue()).decode("utf-8")


def decode_bytes(byte):
    return byte.decode("utf-8")


def request(decoder: Callable = decode_bytes, on_error: Callable[[HTTPError], str] = None, **args) -> str:
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


def exec_parrallel(function: Callable, sequence: List[S], max_workers: int = None) -> List[T]:
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
