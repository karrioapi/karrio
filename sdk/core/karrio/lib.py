import string
import typing
import logging
import datetime
import functools
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
Job = utils.Job
OptionEnum = utils.OptionEnum
Enum = utils.Enum
Flag = utils.Flag


# -----------------------------------------------------------
# raw types utility functions.
# -----------------------------------------------------------


def join(
    *values: typing.Union[str, None],
    join: bool = None,
    separator: str = None,
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
    return utils.SF.concat_str(
        *values, join=(join or False), separator=(separator or " ")
    )


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
    if isinstance(value, bool):
        return None

    try:
        return to_decimal(value)
    except:
        return None


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
    clear_empty: bool = None,
) -> dict:
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

    return utils.XP.to_xml(xml_text, encoding=encoding)


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


# -----------------------------------------------------------
# Shipping request options utility functions.
# -----------------------------------------------------------


def to_shipping_options(
    options: dict,
    initializer: typing.Optional[typing.Callable[[dict], units.ShippingOptions]] = None,
    **kwargs,
) -> units.ShippingOptions:
    if initializer is not None:
        return initializer(options, **kwargs)

    return units.ShippingOptions(options)


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


def to_address(
    address: typing.Optional[models.Address],
) -> units.ComputedAddress:
    """Decorate address data with sensible default and None handling."""

    return units.ComputedAddress(address)


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


def to_packages(
    parcels: typing.List[models.Parcel],
    presets: typing.Type[utils.Enum] = None,
    required: typing.List[str] = None,
    max_weight: units.Weight = None,
    options: dict = None,
    package_option_type: typing.Type[utils.Enum] = utils.Enum,
) -> units.Packages:
    return units.Packages(
        parcels=parcels,
        presets=presets,
        required=required,
        max_weight=max_weight,
        options=units.ShippingOptions(options or {}, package_option_type),
        package_option_type=package_option_type,
    )


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
    return utils.request(decoder=decoder, on_error=on_error, trace=trace, **kwargs)


# -----------------------------------------------------------
# image and document processing utility functions.
# -----------------------------------------------------------


def image_to_pdf(
    image_str: str,
    rotate: int = None,
) -> str:
    return utils.image_to_pdf(image_str, rotate=rotate)


def bundle_pdfs(
    base64_strings: typing.List[str],
) -> utils.PdfMerger:
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


def to_buffer(
    base64_string: str,
    **kwargs,
):
    return utils.to_buffer(base64_string, **kwargs)


# -----------------------------------------------------------
# other utilities functions
# -----------------------------------------------------------


def failsafe(callable: typing.Callable[[], T], warning: str = None) -> T:
    """This higher order function wraps a callable in a try..except
    scope to capture any exception raised.
    Only use it when you are running something unstable that you
    don't mind if it fails.
    """
    try:
        return callable()
    except Exception as e:
        if warning:
            logger.warning(string.Template(warning).substitute(error=e))
        return None