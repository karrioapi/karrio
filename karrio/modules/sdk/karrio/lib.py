import typing
import base64
import PyPDF2
import logging
import datetime
import functools
import urllib.parse
import urllib.error
import karrio.core.utils as utils
import karrio.core.units as units
import karrio.core.models as models

logger = logging.getLogger(__name__)
T = typing.TypeVar("T")
S = typing.TypeVar("S")
mutate_xml_object_type = utils.mutate_xml_object_type
apply_namespaceprefix = utils.apply_namespaceprefix
Deserializable = utils.Deserializable
Serializable = utils.Serializable
Pipeline = utils.Pipeline
Envelope = utils.Envelope
Header = utils.Header
Body = utils.Body
Element = utils.Element
Tracer = utils.Tracer
Trace = utils.Trace
Cache = utils.Cache
Job = utils.Job
OptionEnum = utils.OptionEnum
Enum = utils.Enum
Flag = utils.Flag
StrEnum = utils.StrEnum
identity = utils.identity


# -----------------------------------------------------------
# raw types utility functions.
# -----------------------------------------------------------
# region


def join(
    *values: typing.Union[str, None],
    join: bool = None,
    separator: str = None,
) -> typing.Optional[typing.Union[str, typing.List[str]]]:
    """Concatenate a set of string values into a list of string or a single joined text.

    Example:
        result1 = join("string text 1", "string text 2")
        print(result1) # ["string text 1", "string text 2"]

        result2 = join("string text 1", "string text 2", join=True)
        print(result2) # "string text 1 string text 2"

        result3 = join("string text 1", "string text 2", join=True, separator=", ")
        print(result3) # "string text 1, string text 2"

    :param values: a set of string values.
    :param join: indicate whether to join into a single string.
    :param separator: the text separator if joined into a single string.
    :return: a string, list of string or None.
    """
    return utils.SF.concat_str(
        *values, join=(join or False), separator=(separator or " ")
    )


def text(
    *values: typing.Union[str, None],
    max: int = None,
    separator: str = None,
    trim: bool = False,
) -> typing.Optional[str]:
    """Returns a joined text

    Example:
        result1 = text("string text 1", "string text 2")
        print(result1) # "string text 1 string text 2"

        result2 = text("string text 1", "string text 2", max=20)
        print(result2) # "string text 1 string"

        result3 = text("string text 1", "string text 2", separator=", ")
        print(result3) # "string text 1, string text 2"

        result4 = text("string text 1 ", trim=True)
        print(result4) # "string text 1"

    :param values: a set of string values.
    :param join: indicate whether to join into a single string.
    :param separator: the text separator if joined into a single string.
    :param trim: indicate whether to trim the string values.
    :return: a string, list of string or None.
    """
    _text = utils.SF.concat_str(
        *values,
        join=True,
        separator=(separator or " "),
        trim=trim,
    )

    if _text is None:
        return None

    return typing.cast(str, _text[0:max] if max else _text)


def to_snake_case(input_string: typing.Optional[str]) -> typing.Optional[str]:
    """Convert any string format to snake case."""
    return utils.SF.to_snake_case(input_string)


def to_slug(
    *values,
    separator: str = "_",
) -> typing.Optional[str]:
    """Convert a set of string values into a slug string, changing camel case to snake_case."""
    return utils.SF.to_slug(*values, separator=separator)


def to_int(
    value: typing.Union[str, int, bytes] = None,
    base: int = None,
) -> typing.Optional[int]:
    """Parse a value into a valid integer number.

    Example:
        result1 = to_int("15.0456")
        print(result1)  # 15

        result2 = to_int(12.05)
        print(result2)  # 12

        result3 = to_int(None)
        print(result3)  # None

    :param value: a value that can be parsed into integer.
    :param base: a rounding base value.
    :return: a valid integer number or None.
    """
    return utils.NF.integer(value, base)


def to_decimal(
    value: typing.Union[str, float, bytes] = None,
    quant: typing.Optional[float] = None,
) -> typing.Optional[float]:
    """Parse a value into a valid decimal number with 2 decimal places by default.

    Example:
        result1 = to_decimal(14.89998)
        print(result1)  # 14.90

        result2 = to_decimal("14.89998")
        print(result2)  # 14.90

        result3 = to_decimal(14)
        print(result3)  # 14.00

        result4 = to_decimal(None)
        print(result4)  # None

    :param value: a value that can be parsed to float.
    :param quant: decimal places for rounding (defaults to 2).
    :return: a valid decimal number or None.
    """
    # Default to 2 decimal places if not specified
    if quant is None:
        quant = 0.01  # This will round to 2 decimal places
    return utils.NF.decimal(value, quant)


def to_numeric_decimal(
    value: typing.Union[str, float, bytes] = None,
    total_digits: int = 6,
    decimal_digits: int = 3,
) -> str:
    """Convert a float to a zero-padded string with customizable total length and decimal places.

    Args:
    input_float (float): A floating point number to be formatted.
    total_digits (int): The total length of the output string (including both numeric and decimal parts).
    decimal_digits (int): The number of decimal digits (d) in the final output.

    Returns:
    str: A zero-padded string of total_digits length, with the last decimal_digits as decimals.

    Examples:
    >>> format_to_custom_numeric_decimal(1.0, 7, 3)  # NNNNddd
    '0001000'

    >>> format_to_custom_numeric_decimal(1.0, 8, 3)  # NNNNNddd
    '00001000'

    >>> format_to_custom_numeric_decimal(1.0, 6, 3)  # NNNddd
    '001000'
    """
    return utils.NF.numeric_decimal(value, total_digits, decimal_digits)


def to_money(
    value: typing.Union[str, float, bytes] = None,
) -> typing.Optional[float]:
    """Parse a value into a valid monetary decimal number.

    :param value: a value that can be parsed to float.
    :return: a valid monetary decimal number or None.
    """
    if isinstance(value, bool):
        return None

    try:
        return to_decimal(value)
    except:
        return None


def format_decimal(
    value: typing.Union[str, float, bytes] = None,
    decimal_places: int = 2,
) -> typing.Optional[float]:
    """Format a decimal number to a specific number of decimal places.

    Example:
        result1 = format_decimal(14.89998)
        print(result1)  # 14.90

        result2 = format_decimal(14.89998, 1)
        print(result2)  # 14.9

        result3 = format_decimal(14)
        print(result3)  # 14.00

    :param value: a value that can be parsed to float.
    :param decimal_places: number of decimal places (defaults to 2).
    :return: a formatted decimal number or None.
    """
    if value is None:
        return None

    try:
        # Convert to float first
        float_value = float(value)
        # Round to specified decimal places
        quant = 1.0 / (10 ** decimal_places)
        return utils.NF.decimal(float_value, quant)
    except (ValueError, TypeError):
        return None


def to_list(
    value: typing.Union[T, typing.List[T]] = None,
) -> typing.List[T]:
    """Ensures the input value is a list.

    Example:
        result1 = to_list("test")
        print(result1)  # ["test"]

        result2 = to_int(["test"])
        print(result2)  # ["test"]

    :param value: a value that can be parsed into integer.
    :return: a list of values.
    """

    if value is None:
        return []

    return value if isinstance(value, list) else [value]


# endregion

# -----------------------------------------------------------
# Date and Time utility functions.
# -----------------------------------------------------------
# region


def ftime(
    time_str: str,
    current_format: str = "%H:%M:%S",
    output_format: str = "%H:%M",
    try_formats: typing.List[str] = None,
) -> typing.Optional[str]:
    return utils.DF.ftime(
        time_str,
        current_format=current_format,
        output_format=output_format,
        try_formats=try_formats,
    )


def flocaltime(
    time_str: str,
    current_format: str = "%H:%M:%S",
    output_format: str = "%H:%M %p",
    try_formats: typing.List[str] = None,
) -> typing.Optional[str]:
    return utils.DF.ftime(
        time_str,
        current_format=current_format,
        output_format=output_format,
        try_formats=try_formats,
    )


def fdate(
    date_str: str = None,
    current_format: str = "%Y-%m-%d",
    try_formats: typing.List[str] = None,
) -> typing.Optional[str]:
    return utils.DF.fdate(
        date_str,
        current_format=current_format,
        try_formats=try_formats,
    )


def fdatetime(
    date_str: str = None,
    current_format: str = "%Y-%m-%d %H:%M:%S",
    output_format: str = "%Y-%m-%d %H:%M:%S",
    try_formats: typing.List[str] = None,
) -> typing.Optional[str]:
    return utils.DF.fdatetime(
        date_str,
        current_format=current_format,
        output_format=output_format,
        try_formats=try_formats,
    )


def ftimestamp(
    timestamp: str = None,
) -> typing.Optional[str]:
    return utils.DF.ftimestamp(timestamp)


def to_date(
    date_value: typing.Union[str, datetime.datetime] = None,
    current_format: str = "%Y-%m-%d",
    try_formats: typing.List[str] = None,
) -> datetime.datetime:
    return utils.DF.date(
        date_value,
        current_format=current_format,
        try_formats=try_formats,
    )


def to_next_business_datetime(
    date_value: typing.Union[str, datetime.datetime] = None,
    current_format: str = "%Y-%m-%d %H:%M:%S",
    try_formats: typing.List[str] = None,
) -> datetime.datetime:
    return utils.DF.next_business_datetime(
        date_value,
        current_format=current_format,
        try_formats=try_formats,
    )


# endregion

# -----------------------------------------------------------
# JSON, XML and object utility functions.
# -----------------------------------------------------------
# region


def to_object(
    object_type: typing.Type[T],
    data: typing.Any = None,
) -> typing.Optional[T]:
    """Create an instance of "object_type" from the "data".

    :param object_type: an object class.
    :param data: the data to pass for instantiation.
    :return: an object instance or None.
    """
    if utils.XP.isxmlelementtype(object_type):
        return utils.XP.to_object(object_type, data)

    return utils.DP.to_object(object_type, data)


def to_dict(
    value: typing.Any,
    clear_empty: bool = None,
) -> typing.Union[dict, list, typing.Any]:
    """Parse value into a Python dictionay.

    :param value: a value that can converted in dictionary.
    :return: a dictionary.
    """
    return utils.DP.to_dict(value, clear_empty=clear_empty)


def to_json(
    value: typing.Any,
) -> str:
    """Serialize value to JSON.

    :param value: a value that can be serialized to JSON.
    :return: a string.
    """
    return utils.DP.jsonify(value)


def to_xml(
    value: typing.Union[utils.Element, typing.Any],
    encoding: str = "utf-8",
    prefixes: dict = None,
    **kwargs,
) -> str:
    """Turn a XML typed object into a XML text.

    :param value: XML typed object or element.
    :param encoding: an optional encoding type.
    :return: a XML string.
    """

    if utils.XP.istypedxmlobject(value):
        if prefixes is not None:
            _prefix = prefixes.get(value.__class__.__name__) or ""
            apply_namespaceprefix(value, _prefix, prefixes)

        return utils.XP.export(value, **kwargs)

    return utils.XP.xml_tostring(value, encoding)


def to_element(
    *xml_texts,
    encoding: str = "utf-8",
) -> utils.Element:
    """Turn a XML text into an (lxml) XML Element.

    :param xml_str:
    :return: Node Element
    """
    xml_strings: typing.List[str] = functools.reduce(
        lambda acc, s: [*acc, *s] if isinstance(s, list) else [*acc, s],
        list(xml_texts),
        [],
    )

    xml_text = (
        utils.XP.bundle_xml(xml_strings)
        if len(xml_strings) > 1
        else next(iter(xml_strings), None)
    )

    if xml_text is None:
        raise Exception("Cannot parse empty XML text")

    return utils.XP.to_xml_or_html_element(xml_text, encoding=encoding)


def to_query_string(data: dict) -> str:
    param_list: list = functools.reduce(
        lambda acc, item: [
            *acc,
            *(
                [(item[0], _) for _ in item[1]]
                if isinstance(item[1], list)
                else [(item[0], item[1])]
            ),
        ],
        data.items(),
        [],
    )

    return urllib.parse.urlencode(param_list)


def to_query_unquote(query_string: str) -> str:
    return urllib.parse.unquote(query_string)


def find_element(
    tag: str,
    in_element: utils.Element,
    element_type: typing.Type[typing.Union[T, utils.Element]] = None,
    first: bool = None,
):
    return utils.XP.find(tag, in_element, element_type, first=first)


def create_envelope(
    body_content: typing.Any,
    header_content: typing.Any = None,
    header_prefix: str = None,
    body_prefix: str = None,
    header_tag_name: str = None,
    body_tag_name: str = None,
    envelope_prefix: str = "tns",
) -> utils.Envelope:
    return utils.create_envelope(
        body_content=body_content,
        header_content=header_content,
        header_prefix=header_prefix,
        body_prefix=body_prefix,
        header_tag_name=header_tag_name,
        body_tag_name=body_tag_name,
        envelope_prefix=envelope_prefix,
    )


def envelope_serializer(
    envelope: utils.Envelope,
    namespace: str = "",
    prefixes: dict = None,
):
    ns_prefixes = {"Envelope": "soap-env", **(prefixes or {})}

    envelope.ns_prefix_ = ns_prefixes.get("Envelope") or "soap-env"
    envelope.Body.ns_prefix_ = envelope.ns_prefix_

    if envelope.Header is not None:
        envelope.Header.ns_prefix_ = envelope.ns_prefix_

    for node in envelope.Body.anytypeobjs_ + getattr(
        envelope.Header, "anytypeobjs_", []
    ):
        _prefix = ns_prefixes.get(node.__class__.__name__) or ""
        apply_namespaceprefix(node, _prefix, ns_prefixes)

    return to_xml(envelope, namespacedef_=namespace)


def load_json(path: str):
    """Load and parse a JSON file from the given path.

    Args:
        path (str): The path to the JSON file to be loaded.

    Returns:
        dict: The parsed JSON content as a Python dictionary.

    Raises:
        FileNotFoundError: If the specified file is not found.
        JSONDecodeError: If the file content is not valid JSON.
        IOError: If there's an error reading the file.
    """
    return to_dict(load_file_content(path))


def load_file_content(path: str) -> str:
    """Load the content of a file from the given path.

    Args:
        path (str): The path to the file to be read.

    Returns:
        str: The content of the file as a string.

    Raises:
        FileNotFoundError: If the specified file is not found.
        IOError: If there's an error reading the file.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except IOError as e:
        raise IOError(f"Error reading file {path}: {str(e)}")


# endregion

# -----------------------------------------------------------
# Shipping request options utility functions.
# -----------------------------------------------------------
# region


def to_shipping_options(
    options: dict,
    initializer: typing.Optional[typing.Callable[[dict], units.ShippingOptions]] = None,
    **kwargs,
) -> units.ShippingOptions:
    if initializer is not None:
        return initializer(options, **kwargs)

    return units.ShippingOptions(
        options,
        option_type=kwargs.get("option_type"),
        items_filter=kwargs.get("items_filter"),
    )


def to_services(
    services: typing.List[str],
    service_type: typing.Type[utils.Enum] = None,
    initializer: typing.Optional[
        typing.Callable[[typing.List[str]], units.Services]
    ] = None,
    **kwargs,
) -> units.Services:
    if initializer is not None:
        return initializer(services, **kwargs)

    return units.Services(services, service_type=service_type)


def to_customs_info(
    customs: models.Customs,
    option_type: typing.Type[utils.Enum] = None,
    weight_unit: str = None,
    default_to: typing.Optional[models.Customs] = None,
    shipper: typing.Optional[models.Address] = None,
    recipient: typing.Optional[models.Address] = None,
):
    return units.CustomsInfo(
        customs,
        option_type=option_type or utils.Enum,
        weight_unit=weight_unit,
        default_to=default_to,
        shipper=shipper,
        recipient=recipient,
    )


def to_document_files(
    document_files: typing.List[models.DocumentFile],
) -> typing.List[units.ComputedDocumentFile]:
    return [
        units.ComputedDocumentFile(document_file) for document_file in document_files
    ]


def to_upload_options(
    options: dict,
    option_type: typing.Optional[typing.Type[utils.Enum]] = None,
):
    return units.Options(
        options,
        option_type=option_type,
        base_option_type=units.DocumentUploadOption,
    )


def to_connection_config(
    options: dict,
    option_type: typing.Optional[typing.Type[utils.Enum]] = None,
) -> units.ConnectionConfigOptions:
    return units.ConnectionConfigOptions(
        options,
        option_type=option_type,
    )


# endregion

# -----------------------------------------------------------
# Address utility functions.
# -----------------------------------------------------------
# region


def to_zip4(
    value: typing.Optional[str],
    **kwargs,
) -> typing.Optional[str]:
    return utils.Location(value, **kwargs).as_zip4


def to_zip5(
    value: typing.Optional[str],
    **kwargs,
) -> typing.Optional[str]:
    return utils.Location(value, **kwargs).as_zip5


def to_country_name(
    value: typing.Optional[str],
    **kwargs,
) -> typing.Optional[str]:
    return utils.Location(value, **kwargs).as_country_name


def to_state_name(
    value: typing.Optional[str],
    country: str,
    **kwargs,
) -> typing.Optional[str]:
    return utils.Location(value, **{**kwargs, "country": country}).as_state_name


def to_address(
    address: typing.Optional[models.Address],
) -> units.ComputedAddress:
    """Decorate address data with sensible default and None handling."""

    return units.ComputedAddress(address)


# endregion

# -----------------------------------------------------------
# Multi-piece shipment utility functions.
# -----------------------------------------------------------
# region


def to_multi_piece_rates(
    package_rates: typing.List[typing.Tuple[str, typing.List[models.RateDetails]]],
) -> typing.List[models.RateDetails]:
    """Combine rates received separately per package into a single rate list.

    Example:
        package_rates = [
            ("pkg_1_id", { "service": "standard", "total_charge": 10, ... }),
            ("pkg_2_id", { "service": "standard", "total_charge": 15, ... })
        ]
        result = to_multi_piece_rates(package_rates)

        print(result) # [{ "service": "standard", "total_charge": 25, ... }]


    :param package_rates: a tuple of a package identifier and the list of rates returned for that package.
    :return: a unified list of combined rates of same services.
    """
    return utils.to_multi_piece_rates(package_rates)


def to_multi_piece_shipment(
    package_shipments: typing.List[typing.Tuple[str, models.ShipmentDetails]],
) -> models.ShipmentDetails:
    """Combine shipment received separately per package into a single master shipment.

    Example:
        package_shipments = [
            { "tracking_number": "123", "shipment_identifier": "id_123", "docs": { "label": "label1_base64==" }, ... },
            { "tracking_number": "124", "shipment_identifier": "id_123", "docs": { "label": "label2_base64==" }, ... }
        ]
        result = to_multi_piece_shipment(package_shipments)

        print(result)
        # {
        #   "tracking_number": "123",
        #   "docs": { "label": "label1_base64label2_base64==" },
        #   "meta": { "tracking_numbers": ["123", "124"], "shipment_identifiers": ["id_123", "id_124"] },
        #   ...
        # }


    :param package_shipments: a tuple of a package identifier and the shipment returned for that package.
    :return: a unified master shipment object.
    """
    return utils.to_multi_piece_shipment(package_shipments)


def to_packages(
    parcels: typing.List[models.Parcel],
    presets: typing.Type[utils.Enum] = None,
    required: typing.List[str] = None,
    max_weight: units.Weight = None,
    options: dict = None,
    package_option_type: typing.Type[utils.Enum] = utils.Enum,
    shipping_options_initializer: typing.Callable = None,
) -> units.Packages:
    return units.Packages(
        parcels=parcels,
        presets=presets,
        required=required,
        max_weight=max_weight,
        options=(
            units.ShippingOptions(options or {}, package_option_type)
            if (isinstance(options, dict) or options is None)
            else options
        ),
        package_option_type=package_option_type,
        shipping_options_initializer=shipping_options_initializer,
    )


# endregion

# -----------------------------------------------------------
# async and backgroung code execution utility functions.
# -----------------------------------------------------------
# region


def run_concurently(
    predicate: typing.Callable,
    sequence: typing.List[S],
    max_workers: int = 2,
) -> typing.List[T]:
    return utils.exec_parrallel(predicate, sequence, max_workers=max_workers)


def run_asynchronously(
    predicate: typing.Callable,
    sequence: typing.List[S],
) -> typing.List[T]:
    return utils.exec_async(predicate, sequence)


# endregion

# -----------------------------------------------------------
# HTTP requests utility functions.
# -----------------------------------------------------------
# region


def request(
    decoder: typing.Callable = utils.decode_bytes,
    on_ok: typing.Callable = None,
    on_error: typing.Callable = None,
    trace: typing.Callable[[typing.Any, str], typing.Any] = None,
    proxy: str = None,
    timeout: typing.Optional[int] = None,
    **kwargs,
) -> str:
    return utils.request(
        decoder=decoder,
        on_ok=on_ok,
        on_error=on_error,
        trace=trace,
        proxy=proxy,
        timeout=timeout,
        **kwargs,
    )


def parse_http_response(response: urllib.error.HTTPError) -> str:
    return to_json(dict(code=str(response.code), error=response.reason))


# endregion

# -----------------------------------------------------------
# image and document processing utility functions.
# -----------------------------------------------------------
# region


def image_to_pdf(
    image_str: str,
    rotate: int = None,
    resize: dict = None,
) -> str:
    return utils.image_to_pdf(image_str, rotate=rotate, resize=resize)


def bundle_pdfs(
    base64_strings: typing.List[str],
) -> PyPDF2.PdfMerger:
    return utils.bundle_pdfs(base64_strings)


def bundle_imgs(
    base64_strings: typing.List[str],
):
    return utils.bundle_imgs(base64_strings)


def bundle_zpls(
    base64_strings: typing.List[str],
) -> str:
    return utils.bundle_zpls(base64_strings)


def zpl_to_pdf(
    zpl_str: str,
    width: int,
    height: int,
    dpmm: int = 12,
) -> str:
    """Return a PDF base64 string from a ZPL string."""
    return utils.zpl_to_pdf(zpl_str, width, height, dpmm=dpmm)


def bundle_base64(
    base64_strings: typing.List[str],
    format: str = "PDF",
) -> str:
    return utils.bundle_base64(base64_strings, format=format)


def to_buffer(
    base64_string: str,
    **kwargs,
):
    return utils.to_buffer(base64_string, **kwargs)


def decode(byte: bytes):
    return (
        failsafe(lambda: byte.decode("utf-8"))
        or failsafe(lambda: byte.decode("ISO-8859-1"))
        or byte.decode("utf-8")
    )


def encode_base64(byte: bytes):
    return (
        failsafe(lambda: base64.encodebytes(byte).decode("utf-8"))
        or failsafe(lambda: base64.encodebytes(byte).decode("ISO-8859-1"))
        or base64.encodebytes(byte).decode("utf-8")
    )


def binary_to_base64(binary_string: str):
    return utils.binary_to_base64(binary_string)


# endregion

# -----------------------------------------------------------
# other utilities functions
# -----------------------------------------------------------
# region


def failsafe(callable: typing.Callable[[], T], warning: str = None) -> T:
    """This higher order function wraps a callable in a try..except
    scope to capture any exception raised.
    Only use it when you are running something unstable that you
    don't mind if it fails.
    """
    return utils.failsafe(callable, warning=warning)


# endregion
