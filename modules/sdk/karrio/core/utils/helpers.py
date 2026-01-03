import io
import re
import ssl
import uuid
import string
import base64
import PyPDF2
import asyncio
import datetime
import urllib.parse
import PIL.Image
import PIL.ImageFile
from functools import reduce
from urllib.error import HTTPError
from urllib.request import urlopen, Request, ProxyHandler, build_opener, install_opener
from typing import List, TypeVar, Callable, Optional, Any, Union, cast
from concurrent.futures import ThreadPoolExecutor, as_completed
from karrio.core.utils.logger import logger
ssl._create_default_https_context = ssl._create_unverified_context  # type: ignore
PIL.ImageFile.LOAD_TRUNCATED_IMAGES = True
T = TypeVar("T")
S = TypeVar("S")
NEW_LINE = """
"""


def identity(value: Any) -> Any:
    return value


def failsafe(callable: Callable[[], T], warning: str = None) -> T:
    try:
        return callable()
    except Exception as e:
        if warning:
            logger.warning(string.Template(warning).substitute(error=e))
        return None


def to_buffer(encoded_file: str, **kwargs) -> io.BytesIO:
    content = base64.b64decode(encoded_file, **kwargs)
    buffer = io.BytesIO()
    buffer.write(content)

    return buffer


def image_to_pdf(image_str: str, rotate: int = None, resize: dict = None) -> str:
    buffer = to_buffer(image_str)
    _image = PIL.Image.open(buffer)

    image = (
        _image.rotate(rotate, PIL.Image.Resampling.NEAREST, expand=True)
        if rotate is not None
        else _image
    )

    if resize is not None:
        img = image.copy()
        wpercent = resize["width"] / float(img.size[0])
        hsize = int((float(img.size[1]) * float(wpercent)))
        image = img.resize((resize["width"], hsize), PIL.Image.Resampling.LANCZOS)

    if resize is not None:
        img = image.copy()
        image = img.resize(
            (resize["width"], resize["height"]), PIL.Image.Resampling.LANCZOS
        )

    new_buffer = io.BytesIO()
    image.save(new_buffer, format="PDF", dpi=(300, 300))

    return base64.b64encode(new_buffer.getvalue()).decode("utf-8")


def bundle_pdfs(base64_strings: List[str]) -> PyPDF2.PdfMerger:
    merger = PyPDF2.PdfMerger(strict=False)

    for b64_str in base64_strings:
        buffer = to_buffer(b64_str)
        merger.append(buffer)

    return merger


def bundle_imgs(base64_strings: List[str]):
    image_buffers = [
        io.BytesIO(base64.b64decode(b64_str)) for b64_str in base64_strings
    ]
    images = [PIL.Image.open(buffer) for buffer in image_buffers]
    widths, heights = zip(*(i.size for i in images))

    max_width = max(widths)
    total_height = sum(heights)

    image = PIL.Image.new("RGB", (max_width, total_height))

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


def zpl_to_pdf(zpl_str: str, width: int, height: int, dpmm: int = 12) -> str:
    """Return a PDF base64 string from a ZPL string."""
    import karrio.lib as lib

    data = lib.to_json(dict(file=base64.b64decode(zpl_str).decode("utf-8")))
    doc = request(
        url=f"http://api.labelary.com/v1/printers/{dpmm}dpmm/labels/{width}x{height}/",
        data=data,
        headers={"Accept": "application/pdf"},
        decoder=lambda b: base64.encodebytes(b).decode("utf-8"),
    )

    return doc


def binary_to_base64(binary_str: str) -> str:
    buffer = to_buffer(binary_str)

    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def decode_bytes(byte):
    return (
        failsafe(lambda: byte.decode("utf-8"))
        or failsafe(lambda: byte.decode("ISO-8859-1"))
        or byte.decode("utf-8")
    )


def process_request(
    request_id: str,
    trace: Callable[[Any, str], Any] = None,
    proxy: str = None,
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

    # Apply proxy settings if provided: Proxy Example` 'username:password@IP_Address:Port'
    if proxy:
        proxy_info = proxy.split("@")
        auth_info, host_port = proxy_info[0], proxy_info[1]
        auth_info = urllib.parse.unquote(auth_info)
        auth_encoded = base64.b64encode(auth_info.encode()).decode()
        proxy_url = f"http://{host_port}"

        # Create a ProxyHandler
        proxy_handler = ProxyHandler({"http": proxy_url, "https": proxy_url})
        opener = build_opener(proxy_handler)
        opener.addheaders = [("Proxy-Authorization", f"Basic {auth_encoded}")]
        install_opener(opener)
        logger.info("Proxy configured", proxy_url=proxy_url)

    logger.info("HTTP request prepared", url=_request.full_url)

    return _request


def process_response(
    request_id: str,
    response: Any,
    decoder: Callable,
    on_ok: Callable[[Any], str] = None,
    trace: Callable[[Any, str], Any] = None,
) -> str:
    if on_ok is not None:
        _response = on_ok(response)
    else:
        _data = response.read()
        _response = failsafe(lambda: decoder(_data)) or _data

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
    logger.error("HTTP request failed", request_id=request_id, error_code=error.code, error_msg=str(error))

    if on_error is not None:
        _error = on_error(error)
    else:
        _error = decode_bytes(error.read())

    if trace:
        trace({"request_id": request_id, "error": _error}, "error")

    logger.debug("HTTP error details", request_id=request_id, error=str(error))

    return _error


# Default HTTP status codes that should trigger a retry
RETRYABLE_STATUS_CODES = {500, 502, 503, 504, 522, 524}


class HttpResponse:
    """HTTP response wrapper that provides access to both content and headers."""

    def __init__(
        self,
        content: str,
        status_code: int = 200,
        headers: Optional[dict] = None,
        is_error: bool = False,
    ):
        self.content = content
        self.status_code = status_code
        self.headers = headers or {}
        self.is_error = is_error

    def __str__(self) -> str:
        return self.content

    def get_header(self, name: str, default: str = None) -> Optional[str]:
        """Get a header value (case-insensitive)."""
        for key, value in self.headers.items():
            if key.lower() == name.lower():
                return value
        return default


def request_with_response(
    decoder: Callable = decode_bytes,
    on_ok: Callable[[Any], str] = None,
    on_error: Callable[[HTTPError], str] = None,
    trace: Callable[[Any, str], Any] = None,
    proxy: str = None,
    timeout: Optional[int] = None,
    max_retries: int = 0,
    retry_delay: float = 1.0,
    retry_on_status: List[int] = None,
    **kwargs,
) -> HttpResponse:
    """Return an HTTP response object with content, headers, and status.

    This is similar to request() but returns an HttpResponse object
    that provides access to response headers in addition to the body.

    Args:
        decoder: Function to decode the response bytes (default: decode_bytes)
        on_ok: Optional callback to process successful responses
        on_error: Optional callback to process error responses
        trace: Trace function for logging
        proxy: Proxy configuration string (format: 'Username:Password@IP_Address:Port')
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts for transient failures (default: 0)
        retry_delay: Initial delay between retries in seconds, doubles each attempt (default: 1.0)
        retry_on_status: List of HTTP status codes to retry on (default: 500, 502, 503, 504, 522, 524)
        **kwargs: Additional arguments passed to urllib.request.Request

    Returns:
        HttpResponse object with content, status_code, headers, and is_error flag
    """
    import time

    _retry_statuses = set(retry_on_status or RETRYABLE_STATUS_CODES)
    _request_id = str(uuid.uuid4())
    _last_error: Optional[Union[HTTPError, TimeoutError, ConnectionError, OSError]] = None
    _last_response = None

    for attempt in range(max_retries + 1):
        try:
            if attempt > 0:
                delay = retry_delay * (2 ** (attempt - 1))
                logger.warning(
                    "Retrying HTTP request",
                    request_id=_request_id,
                    attempt=attempt,
                    max_retries=max_retries,
                    delay=delay,
                )
                time.sleep(delay)

            logger.debug(
                "Sending HTTP request",
                request_id=_request_id,
                attempt=attempt if max_retries > 0 else None,
            )

            _request = process_request(_request_id, trace if attempt == 0 else None, proxy, **kwargs)

            with urlopen(_request, timeout=timeout) as f:
                _content = process_response(
                    _request_id, f, decoder, on_ok=on_ok, trace=trace if attempt == 0 else None
                )
                return HttpResponse(
                    content=_content,
                    status_code=f.status,
                    headers=dict(f.headers),
                    is_error=False,
                )

        except HTTPError as e:
            _last_error = e

            # Check if we should retry this error
            if e.code in _retry_statuses and attempt < max_retries:
                logger.warning(
                    "HTTP request failed with retryable status",
                    request_id=_request_id,
                    status_code=e.code,
                    attempt=attempt,
                    max_retries=max_retries,
                )
                continue

            # No more retries, process the error
            _content = process_error(_request_id, e, on_error=on_error, trace=trace)
            return HttpResponse(
                content=_content,
                status_code=e.code,
                headers=dict(e.headers) if e.headers else {},
                is_error=True,
            )

        except (TimeoutError, ConnectionError, OSError) as e:
            _last_error = e

            # Retry on connection/timeout errors
            if attempt < max_retries:
                logger.warning(
                    "HTTP request failed with connection error, retrying",
                    request_id=_request_id,
                    error=str(e),
                    attempt=attempt,
                    max_retries=max_retries,
                )
                continue

            # No more retries, raise the error
            raise

    # Should not reach here, but just in case
    if _last_error is not None:
        raise _last_error

    return HttpResponse(content="", status_code=0, headers={}, is_error=True)


def request(
    decoder: Callable = decode_bytes,
    on_ok: Callable[[Any], str] = None,
    on_error: Callable[[HTTPError], str] = None,
    trace: Callable[[Any, str], Any] = None,
    proxy: str = None,
    timeout: Optional[int] = None,
    max_retries: int = 0,
    retry_delay: float = 1.0,
    retry_on_status: List[int] = None,
    **kwargs,
) -> str:
    """Return an HTTP response body.

    Make an HTTP request (wrapper around Request method from built-in urllib).

    Args:
        decoder: Function to decode the response bytes (default: decode_bytes)
        on_ok: Optional callback to process successful responses
        on_error: Optional callback to process error responses
        trace: Trace function for logging
        proxy: Proxy configuration string (format: 'Username:Password@IP_Address:Port')
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts for transient failures (default: 0)
        retry_delay: Initial delay between retries in seconds, doubles each attempt (default: 1.0)
        retry_on_status: List of HTTP status codes to retry on (default: 500, 502, 503, 504, 522, 524)
        **kwargs: Additional arguments passed to urllib.request.Request

    Returns:
        The decoded response body string
    """
    import time

    _retry_statuses = set(retry_on_status or RETRYABLE_STATUS_CODES)
    _request_id = str(uuid.uuid4())
    _last_error: Optional[Union[HTTPError, TimeoutError, ConnectionError, OSError]] = None
    _last_response = None

    for attempt in range(max_retries + 1):
        try:
            if attempt > 0:
                delay = retry_delay * (2 ** (attempt - 1))
                logger.warning(
                    "Retrying HTTP request",
                    request_id=_request_id,
                    attempt=attempt,
                    max_retries=max_retries,
                    delay=delay,
                )
                time.sleep(delay)

            logger.debug(
                "Sending HTTP request",
                request_id=_request_id,
                attempt=attempt if max_retries > 0 else None,
            )

            _request = process_request(_request_id, trace if attempt == 0 else None, proxy, **kwargs)

            with urlopen(_request, timeout=timeout) as f:
                _response = process_response(
                    _request_id, f, decoder, on_ok=on_ok, trace=trace if attempt == 0 else None
                )

            return _response

        except HTTPError as e:
            _last_error = e

            # Check if we should retry this error
            if e.code in _retry_statuses and attempt < max_retries:
                logger.warning(
                    "HTTP request failed with retryable status",
                    request_id=_request_id,
                    status_code=e.code,
                    attempt=attempt,
                    max_retries=max_retries,
                )
                continue

            # No more retries, process the error
            _last_response = process_error(_request_id, e, on_error=on_error, trace=trace)
            return _last_response

        except (TimeoutError, ConnectionError, OSError) as e:
            _last_error = e

            # Retry on connection/timeout errors
            if attempt < max_retries:
                logger.warning(
                    "HTTP request failed with connection error, retrying",
                    request_id=_request_id,
                    error=str(e),
                    attempt=attempt,
                    max_retries=max_retries,
                )
                continue

            # No more retries, raise the error
            raise

    # Should not reach here, but just in case
    if _last_response is not None:
        return _last_response

    if _last_error is not None:
        raise _last_error

    return ""


def exec_parrallel(
    function: Callable, sequence: List[S], max_workers: int = None
) -> List[T]:
    """Return a list of result for function execution on each element of the sequence."""
    if not sequence:
        return []  # No work to do

    workers = min(len(sequence), max_workers or len(sequence))

    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Submit tasks
        futures = [executor.submit(function, item) for item in sequence]

        # Collect results as tasks complete
        results = []
        for future in as_completed(futures):
            try:
                results.append(future.result())  # Append result of the completed task
            except Exception as e:
                results.append(e)  # Optionally handle or log exceptions here

        return results


def exec_async(action: Callable, sequence: List[S]) -> List[T]:
    async def run_tasks():
        # Use asyncio.to_thread instead of loop.run_in_executor
        # This ensures proper task scheduling and prevents potential task dropping
        return await asyncio.gather(
            *[asyncio.to_thread(action, args) for args in sequence]
        )

    async def run_loop():
        # Simplified to just return the result of run_tasks
        # No need for manual loop creation and closing
        return await run_tasks()

    # Use asyncio.run instead of ThreadPoolExecutor
    # This properly sets up and tears down the event loop
    # Preventing issues with loop closure and task cleanup
    result = asyncio.run(run_loop())

    # Cast the result to the expected type
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
        if not self.value:
            return None

        # Try to extract exactly 5 digits
        if match := re.search(r"\d{5}", self.value):
            return match.group(0)

        # If 4 digits, pad with 0
        if match := re.search(r"\d{4}", self.value):
            return f"{match.group(0)}0"

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


def sort_events_chronologically(events: List[Any]) -> List[Any]:
    """
    Sort tracking events chronologically with the most recent event first.

    This function parses date and time from events and sorts them by their
    combined datetime value. Events with valid dates are sorted first (most recent
    to oldest), followed by events without dates in their original order.

    Args:
        events: List of tracking events to sort

    Returns:
        Sorted list with most recent event first
    """
    # Early return for trivial cases
    if not events or len(events) < 2:
        return events

    def try_parse_with_format(value: str, fmt: str) -> Optional[Any]:
        """Safely attempt to parse a value with a format"""
        return failsafe(lambda: datetime.datetime.strptime(value, fmt))

    def parse_date(event) -> Optional[datetime.datetime]:
        """Parse date from event using multiple format attempts"""
        date_formats = ["%Y-%m-%d", "%m/%d/%Y", "%-m/%d/%Y"]
        return (
            reduce(
                lambda acc, fmt: acc or try_parse_with_format(event.date, fmt),
                date_formats,
                None,
            )
            if hasattr(event, "date") and event.date
            else None
        )

    def parse_time(event) -> Optional[datetime.time]:
        """Parse time from event using multiple format attempts"""
        time_formats = ["%I:%M %p", "%H:%M:%S", "%H:%M"]
        parsed = (
            reduce(
                lambda acc, fmt: acc or try_parse_with_format(event.time, fmt),
                time_formats,
                None,
            )
            if hasattr(event, "time") and event.time
            else None
        )
        return parsed.time() if parsed else None

    def parse_event_datetime(event) -> Optional[datetime.datetime]:
        """Parse complete datetime from event date and time"""
        parsed_date = parse_date(event)
        parsed_time = parse_time(event) if parsed_date else None
        return (
            datetime.datetime.combine(parsed_date.date(), parsed_time)
            if parsed_date and parsed_time
            else parsed_date
        )

    # Create mapping of event index to parsed datetime
    indexed_events = list(enumerate(events))
    datetime_map = dict(
        filter(
            lambda x: x[1] is not None,
            [(idx, parse_event_datetime(event)) for idx, event in indexed_events],
        )
    )

    # Sort events: dated events first (by datetime desc), undated last (by original index)
    def create_sort_key(item: tuple) -> tuple:
        idx, _ = item
        return (
            (0, datetime_map.get(idx, datetime.datetime.min))
            if idx in datetime_map
            else (1, idx)
        )

    sorted_indexed = sorted(indexed_events, key=create_sort_key, reverse=True)
    return [event for _, event in sorted_indexed]
