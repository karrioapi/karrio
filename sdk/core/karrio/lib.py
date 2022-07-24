import typing
import datetime
import karrio.core.utils as utils
import karrio.core.models as models

T = typing.TypeVar("T")
S = typing.TypeVar("S")
Deserializable = utils.Deserializable
Serializable = utils.Serializable
Pipeline = utils.Pipeline
Envelope = utils.Envelope
Element = utils.Element
Trace = utils.Trace
Job = utils.Job


# -----------------------------------------------------------
# raw types utility functions.
# -----------------------------------------------------------


def to_text(
    *values: typing.Union[str, None],
    join: bool = False,
    separator: str = " ",
) -> typing.Optional[typing.Union[str, typing.List[str]]]:
    """Concatenate a set of string values into a list of string or a single joined text.

    Example:
        result1 = to_text("string text 1", "string text 2")
        print(result1) # ["string text 1", "string text 2"]

        result2 = to_text("string text 1", "string text 2", join=True)
        print(result2) # "string text 1 string text 2"

        result3 = to_text("string text 1", "string text 2", join=True, separator=", ")
        print(result3) # "string text 1, string text 2"

    :param values: a set of string values.
    :param join: indicate whether to join into a single string.
    :param separator: the text separator if joined into a single string.
    :return: a string, list of string or None.
    """
    return utils.SF.concat_str(*values, join, separator)


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
    """Parse a value into a valid decimal number.

    Example:
        result1 = to_decimal(14.89998)
        print(result1)  # 14.89

        result2 = to_decimal("14.89998")
        print(result2)  # 14.89

        result3 = to_decimal(14)
        print(result3)  # 14.00

        result4 = to_decimal(None)
        print(result4)  # None

    :param value: a value that can be parsed to float.
    :param quant: decimal places for rounding.
    :return: a valid decimal number or None.
    """
    return utils.NF.decimal(value, quant)


def to_money(
    value: typing.Union[str, float, bytes] = None,
) -> typing.Optional[float]:
    """Parse a value into a valid monetary decimal number.

    :param value: a value that can be parsed to float.
    :return: a valid monetary decimal number or None.
    """
    return to_decimal(value)


# -----------------------------------------------------------
# Date and Time utility functions.
# -----------------------------------------------------------


def ftime(
    time_str: str,
    current_format: str = "%H:%M:%S",
    output_format: str = "%H:%M",
    try_formats: typing.List[str] = None,
) -> typing.Optional[str]:

    return utils.DF.ftime(
        time_str,
        current_format,
        output_format,
        try_formats,
    )


def fdate(
    date_str: str = None,
    current_format: str = "%Y-%m-%d",
    try_formats: typing.List[str] = None,
) -> typing.Optional[str]:
    return utils.DF.fdate(
        date_str,
        current_format,
        try_formats,
    )


def fdatetime(
    date_str: str = None,
    current_format: str = "%Y-%m-%d %H:%M:%S",
    output_format: str = "%Y-%m-%d %H:%M:%S",
    try_formats: typing.List[str] = None,
) -> typing.Optional[str]:
    return utils.DF.fdatetime(
        date_str,
        current_format,
        output_format,
        try_formats,
    )


def to_date(
    date_value: typing.Union[str, datetime.datetime] = None,
    current_format: str = "%Y-%m-%d",
    try_formats: typing.List[str] = None,
) -> datetime.datetime:
    return utils.DF.date(
        date_value,
        current_format,
        try_formats,
    )


# -----------------------------------------------------------
# JSON, XML and object utility functions.
# -----------------------------------------------------------


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
) -> dict:
    """Parse value into a Python dictionay.

    :param value: a value that can converted in dictionary.
    :return: a dictionary.
    """
    return utils.DP.to_dict(value)


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
    **kwargs,
) -> str:
    """Turn a XML typed object into a XML text.

    :param value: XML typed object or element.
    :param encoding: an optional encoding type.
    :return: a XML string.
    """
    if utils.XP.istypedxmlobject(value):
        return utils.XP.export(value, **kwargs)

    return utils.XP.xml_tostring(value, encoding)


def to_element(
    *xml_texts,
) -> utils.Element:
    """Turn a XML text into an (lxml) XML Element.

    :param xml_str:
    :return: Node Element
    """
    xml_strings: typing.List[str] = list(xml_texts)
    xml_text = (
        utils.XP.bundle_xml(xml_strings)
        if len(xml_strings) > 1
        else next(iter(xml_strings), None)
    )

    if xml_text is None:
        raise Exception("Cannot parse empty XML text")

    return utils.XP.to_xml(xml_text)


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


# -----------------------------------------------------------
# Shipping request options utility functions.
# -----------------------------------------------------------


def optionFlag(
    key: str,
) -> utils.Spec:
    """Create a wrapper for an option flag.
    This will return True or False if the value is provided.

    Example:
        option = optionFlag("LAD")
        option_value = option.apply(True)

        print(option.key)  # "LAD"
        print(option.value)  # None
        print(option_value)  # True


    :param key: the option code name.
    :return: an option wrapper object.
    """
    return utils.Spec.asFlag(key)


def optionKey(
    key: str,
) -> utils.Spec:
    """Create a wrapper for an option code.
    This will return True or False if the value is accessed.

    Example:
        option = optionKey("LAD")
        option_value = option.apply(True)

        print(option.key)  # "LAD"
        print(option.value)  # None
        print(option_value)  # "LAD"


    :param key: the option code name.
    :return: an option wrapper object.
    """
    return utils.Spec.asKey(key)


def optionValue(
    key: str,
) -> utils.Spec:
    """Create a wrapper for an option value.

    example:
        option = optionValue("LAD")
        option_value = option.apply('always')

        print(option.key)  # "LAD"
        print(option.value)  # None
        print(option_value)  # "always"


    :param key: the option key name.
    :return: an option wrapper object.
    """
    return utils.Spec.asValue(key)


def optionKeyVal(
    code: str,
    type: typing.Type = str,
) -> utils.Spec:
    """Create a wrapper for an option key pair.
    This will return the value of the provided type.

    example:
        option = optionKeyVal("cash_on_delivery", to_money)
        option_value = option.apply(39.99)

        print(option.key)  # "cash_on_delivery"
        print(option.value)  # 39.99
        print(option_value)  # 39.99


    :param key: the option code name.
    :return: an option wrapper object.
    """
    return utils.Spec.asKeyVal(code, type)


# -----------------------------------------------------------
# Address utility functions.
# -----------------------------------------------------------


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


# -----------------------------------------------------------
# Multi-piece shipment utility functions.
# -----------------------------------------------------------


def to_multi_piece_rates(
    package_rates: typing.List[typing.Tuple[str, typing.List[models.RateDetails]]]
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
    package_shipments: typing.List[typing.Tuple[str, models.ShipmentDetails]]
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


# -----------------------------------------------------------
# async and backgroung code execution utility functions.
# -----------------------------------------------------------


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


# -----------------------------------------------------------
# HTTP requests utility functions.
# -----------------------------------------------------------


def request(
    decoder: typing.Callable = utils.decode_bytes,
    on_error: typing.Callable = None,
    trace: typing.Callable[[typing.Any, str], typing.Any] = None,
    **kwargs,
) -> str:
    return utils.request(decoder, on_error=on_error, trace=trace, **kwargs)


# -----------------------------------------------------------
# image and document processing utility functions.
# -----------------------------------------------------------


def image_to_pdf(
    image_str: str,
) -> str:
    return utils.image_to_pdf(image_str)


def bundle_pdfs(
    base64_strings: typing.List[str],
) -> utils.PdfFileMerger:
    return utils.bundle_pdfs(base64_strings)


def bundle_imgs(
    base64_strings: typing.List[str],
) -> utils.Image:
    return utils.bundle_imgs(base64_strings)


def bundle_zpls(
    base64_strings: typing.List[str],
) -> str:
    return utils.bundle_zpls(base64_strings)


def bundle_base64(
    base64_strings: typing.List[str],
    format: str = "PDF",
) -> str:
    return utils.bundle_base64(base64_strings, format=format)
