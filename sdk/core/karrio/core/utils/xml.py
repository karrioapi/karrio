"""Karrio lxml typing and utilities wrappers"""

import io
import warnings
from lxml import etree
from xmltodict import parse
from typing import Any, List, TypeVar, Type, Optional, cast, Union
from pysoap.envelope import Envelope
from lxml.etree import _Element

T = TypeVar("T")


class Element(_Element):
    def xpath(self, *args, **kwargs) -> List["Element"]:  # type: ignore
        pass


class GenerateDSAbstract(Envelope):
    pass


class XMLPARSER:
    @staticmethod
    def iselement(element: Any):
        """Return True if *element* appears to be an Element."""
        return isinstance(element, _Element)

    @staticmethod
    def isxmlelementtype(element_type: Type[T]):
        """Return True if *element_type* appears to be an GenerateDS generated Type."""

        return hasattr(element_type, "build") and hasattr(element_type, "export")

    @staticmethod
    def istypedxmlobject(xml_typed_object: T):
        """Return True if *xml_typed_object* appears to be an GenerateDS generated Type instance."""
        return XMLPARSER.isxmlelementtype(xml_typed_object.__class__)

    @staticmethod
    def build(element_type: Type[T], xml_node: Element = None) -> Optional[T]:
        warnings.warn(
            "build is deprecated. Use to_object instead", category=DeprecationWarning
        )
        return XMLPARSER.to_object(element_type, xml_node)

    @staticmethod
    def to_object(element_type: Type[T], xml_node: Element = None) -> Optional[T]:
        """Build xml element node into type class

        :param element_type: The xml node corresponding type (class)
        :param xml_node: the xml node source
        :return: None if the node is None else an instance of GenerateDS XML Element class
        """
        if xml_node is None:
            return None

        instance = element_type()
        cast(GenerateDSAbstract, instance).build(xml_node)
        return instance

    @staticmethod
    def find(
        tag: str,
        in_element: Element,
        element_type: Type[Union[T, Element]] = None,
        first: bool = None,
    ):
        children = [
            (
                child
                if element_type is None
                else XMLPARSER.to_object(element_type, child)
            )
            for child in list(in_element.xpath(".//*[local-name() = $name]", name=tag))
        ]

        if first is True:
            return next((c for c in children), None)

        return children

    @staticmethod
    def export(typed_xml_element: Union[Type[GenerateDSAbstract], Any], **kwds) -> str:
        """Serialize a class instance into XML string.
        => Invoke the export method of generated type to return the subsequent XML represented

        :param typed_xml_element: a GeneratedDS XML Element instance
        :param kwds: exporting method arguments
        :return: an XML text
        """
        output = io.StringIO()
        cast(GenerateDSAbstract, typed_xml_element).export(output, 0, **kwds)
        return output.getvalue()

    @staticmethod
    def bundle_xml(xml_strings: List[str]) -> str:
        """Bundle a list of XML string into a single one.
        => <wrapper>{all the XML trees concatenated}</wrapper>

        :param xml_strings:
        :return: a bundled XML text containing all the micro XML string
        """
        from karrio.core.utils.string import STRINGFORMAT

        bundle = "".join(
            [
                XMLPARSER.xml_tostring(XMLPARSER.to_xml(x))
                for x in xml_strings
                if x is not None and x != ""
            ]
        )
        return f"<wrapper>{bundle}</wrapper>"

    @staticmethod
    def jsonify_xml(xml_str: str) -> dict:
        """Turn a XML string into a Python Dictionary

        :param xml_str:
        :return: a dictionary
        """
        return parse(xml_str)

    @staticmethod
    def to_xml(xml_str: Union[str, bytes], encoding: str = "utf-8") -> Element:
        """Turn a XML text into an (lxml) XML Element.

        :param xml_str:
        :return: Node Element
        """
        text = xml_str if isinstance(xml_str, bytes) else xml_str.encode(encoding)
        element = etree.fromstring(text, parser=etree.XMLParser(encoding=encoding))

        return cast(Element, element)

    @staticmethod
    def xml_tostring(xml_element: Element, encoding: str = "utf-8") -> str:
        """Turn a XML Element into a XML text.

        :param xml_element: XML ELement
        :param encoding: the string format encoding
        :return: Node Element
        """
        return str(cast(bytes, etree.tostring(xml_element)), encoding)
