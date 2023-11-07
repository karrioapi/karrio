#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Fri Oct 21 12:33:20 2022 by generateDS.py version 2.41.1.
# Python 3.10.8 (v3.10.8:aaaf517424, Oct 11 2022, 10:14:40) [Clang 13.0.0 (clang-1300.0.29.30)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './karrio.schemas.freightcom/shipping_reply.py')
#
# Command line arguments:
#   ./vendor/schemas/shipping_reply.xsd
#
# Command line:
#   /Users/danielk/Documents/karrio/karrio/.venv/karrio/bin/generateDS --no-namespace-defs -o "./karrio.schemas.freightcom/shipping_reply.py" ./vendor/schemas/shipping_reply.xsd
#
# Current working directory (os.getcwd()):
#   freightcom
#

import sys

try:
    ModulenotfoundExp_ = ModuleNotFoundError
except NameError:
    ModulenotfoundExp_ = ImportError
from six.moves import zip_longest
import os
import re as re_
import base64
import datetime as datetime_
import decimal as decimal_
from lxml import etree as etree_


Validate_simpletypes_ = True
SaveElementTreeNode = True
TagNamePrefix = ""
if sys.version_info.major == 2:
    BaseStrType_ = basestring
else:
    BaseStrType_ = str


def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    try:
        if isinstance(infile, os.PathLike):
            infile = os.path.join(infile)
    except AttributeError:
        pass
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc


def parsexmlstring_(instring, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    element = etree_.fromstring(instring, parser=parser, **kwargs)
    return element


#
# Namespace prefix definition table (and other attributes, too)
#
# The module generatedsnamespaces, if it is importable, must contain
# a dictionary named GeneratedsNamespaceDefs.  This Python dictionary
# should map element type names (strings) to XML schema namespace prefix
# definitions.  The export method for any class for which there is
# a namespace prefix definition, will export that definition in the
# XML representation of that element.  See the export method of
# any generated element type class for an example of the use of this
# table.
# A sample table is:
#
#     # File: generatedsnamespaces.py
#
#     GenerateDSNamespaceDefs = {
#         "ElementtypeA": "http://www.xxx.com/namespaceA",
#         "ElementtypeB": "http://www.xxx.com/namespaceB",
#     }
#
# Additionally, the generatedsnamespaces module can contain a python
# dictionary named GenerateDSNamespaceTypePrefixes that associates element
# types with the namespace prefixes that are to be added to the
# "xsi:type" attribute value.  See the _exportAttributes method of
# any generated element type and the generation of "xsi:type" for an
# example of the use of this table.
# An example table:
#
#     # File: generatedsnamespaces.py
#
#     GenerateDSNamespaceTypePrefixes = {
#         "ElementtypeC": "aaa:",
#         "ElementtypeD": "bbb:",
#     }
#

try:
    from generatedsnamespaces import GenerateDSNamespaceDefs as GenerateDSNamespaceDefs_
except ModulenotfoundExp_:
    GenerateDSNamespaceDefs_ = {}
try:
    from generatedsnamespaces import (
        GenerateDSNamespaceTypePrefixes as GenerateDSNamespaceTypePrefixes_,
    )
except ModulenotfoundExp_:
    GenerateDSNamespaceTypePrefixes_ = {}

#
# You can replace the following class definition by defining an
# importable module named "generatedscollector" containing a class
# named "GdsCollector".  See the default class definition below for
# clues about the possible content of that class.
#
try:
    from generatedscollector import GdsCollector as GdsCollector_
except ModulenotfoundExp_:

    class GdsCollector_(object):
        def __init__(self, messages=None):
            if messages is None:
                self.messages = []
            else:
                self.messages = messages

        def add_message(self, msg):
            self.messages.append(msg)

        def get_messages(self):
            return self.messages

        def clear_messages(self):
            self.messages = []

        def print_messages(self):
            for msg in self.messages:
                print("Warning: {}".format(msg))

        def write_messages(self, outstream):
            for msg in self.messages:
                outstream.write("Warning: {}\n".format(msg))


#
# The super-class for enum types
#

try:
    from enum import Enum
except ModulenotfoundExp_:
    Enum = object

#
# The root super-class for element type classes
#
# Calls to the methods in these classes are generated by generateDS.py.
# You can replace these methods by re-implementing the following class
#   in a module named generatedssuper.py.

try:
    from generatedssuper import GeneratedsSuper
except ModulenotfoundExp_ as exp:
    try:
        from generatedssupersuper import GeneratedsSuperSuper
    except ModulenotfoundExp_ as exp:

        class GeneratedsSuperSuper(object):
            pass

    class GeneratedsSuper(GeneratedsSuperSuper):
        __hash__ = object.__hash__
        tzoff_pattern = re_.compile(r"(\+|-)((0\d|1[0-3]):[0-5]\d|14:00)$")

        class _FixedOffsetTZ(datetime_.tzinfo):
            def __init__(self, offset, name):
                self.__offset = datetime_.timedelta(minutes=offset)
                self.__name = name

            def utcoffset(self, dt):
                return self.__offset

            def tzname(self, dt):
                return self.__name

            def dst(self, dt):
                return None

        def __str__(self):
            settings = {
                "str_pretty_print": True,
                "str_indent_level": 0,
                "str_namespaceprefix": "",
                "str_name": self.__class__.__name__,
                "str_namespacedefs": "",
            }
            for n in settings:
                if hasattr(self, n):
                    settings[n] = getattr(self, n)
            if sys.version_info.major == 2:
                from StringIO import StringIO
            else:
                from io import StringIO
            output = StringIO()
            self.export(
                output,
                settings["str_indent_level"],
                pretty_print=settings["str_pretty_print"],
                namespaceprefix_=settings["str_namespaceprefix"],
                name_=settings["str_name"],
                namespacedef_=settings["str_namespacedefs"],
            )
            strval = output.getvalue()
            output.close()
            return strval

        def gds_format_string(self, input_data, input_name=""):
            return input_data

        def gds_parse_string(self, input_data, node=None, input_name=""):
            return input_data

        def gds_validate_string(self, input_data, node=None, input_name=""):
            if not input_data:
                return ""
            else:
                return input_data

        def gds_format_base64(self, input_data, input_name=""):
            return base64.b64encode(input_data).decode("ascii")

        def gds_validate_base64(self, input_data, node=None, input_name=""):
            return input_data

        def gds_format_integer(self, input_data, input_name=""):
            return "%d" % int(input_data)

        def gds_parse_integer(self, input_data, node=None, input_name=""):
            try:
                ival = int(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, "Requires integer value: %s" % exp)
            return ival

        def gds_validate_integer(self, input_data, node=None, input_name=""):
            try:
                value = int(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, "Requires integer value")
            return value

        def gds_format_integer_list(self, input_data, input_name=""):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return "%s" % " ".join(input_data)

        def gds_validate_integer_list(self, input_data, node=None, input_name=""):
            values = input_data.split()
            for value in values:
                try:
                    int(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, "Requires sequence of integer values")
            return values

        def gds_format_float(self, input_data, input_name=""):
            return ("%.15f" % float(input_data)).rstrip("0")

        def gds_parse_float(self, input_data, node=None, input_name=""):
            try:
                fval_ = float(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, "Requires float or double value: %s" % exp)
            return fval_

        def gds_validate_float(self, input_data, node=None, input_name=""):
            try:
                value = float(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, "Requires float value")
            return value

        def gds_format_float_list(self, input_data, input_name=""):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return "%s" % " ".join(input_data)

        def gds_validate_float_list(self, input_data, node=None, input_name=""):
            values = input_data.split()
            for value in values:
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, "Requires sequence of float values")
            return values

        def gds_format_decimal(self, input_data, input_name=""):
            return_value = "%s" % input_data
            if "." in return_value:
                return_value = return_value.rstrip("0")
                if return_value.endswith("."):
                    return_value = return_value.rstrip(".")
            return return_value

        def gds_parse_decimal(self, input_data, node=None, input_name=""):
            try:
                decimal_value = decimal_.Decimal(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, "Requires decimal value")
            return decimal_value

        def gds_validate_decimal(self, input_data, node=None, input_name=""):
            try:
                value = decimal_.Decimal(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, "Requires decimal value")
            return value

        def gds_format_decimal_list(self, input_data, input_name=""):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return " ".join([self.gds_format_decimal(item) for item in input_data])

        def gds_validate_decimal_list(self, input_data, node=None, input_name=""):
            values = input_data.split()
            for value in values:
                try:
                    decimal_.Decimal(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, "Requires sequence of decimal values")
            return values

        def gds_format_double(self, input_data, input_name=""):
            return "%s" % input_data

        def gds_parse_double(self, input_data, node=None, input_name=""):
            try:
                fval_ = float(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, "Requires double or float value: %s" % exp)
            return fval_

        def gds_validate_double(self, input_data, node=None, input_name=""):
            try:
                value = float(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, "Requires double or float value")
            return value

        def gds_format_double_list(self, input_data, input_name=""):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return "%s" % " ".join(input_data)

        def gds_validate_double_list(self, input_data, node=None, input_name=""):
            values = input_data.split()
            for value in values:
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise_parse_error(
                        node, "Requires sequence of double or float values"
                    )
            return values

        def gds_format_boolean(self, input_data, input_name=""):
            return ("%s" % input_data).lower()

        def gds_parse_boolean(self, input_data, node=None, input_name=""):
            input_data = input_data.strip()
            if input_data in ("true", "1"):
                bval = True
            elif input_data in ("false", "0"):
                bval = False
            else:
                raise_parse_error(node, "Requires boolean value")
            return bval

        def gds_validate_boolean(self, input_data, node=None, input_name=""):
            if input_data not in (
                True,
                1,
                False,
                0,
            ):
                raise_parse_error(
                    node, "Requires boolean value " "(one of True, 1, False, 0)"
                )
            return input_data

        def gds_format_boolean_list(self, input_data, input_name=""):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return "%s" % " ".join(input_data)

        def gds_validate_boolean_list(self, input_data, node=None, input_name=""):
            values = input_data.split()
            for value in values:
                value = self.gds_parse_boolean(value, node, input_name)
                if value not in (
                    True,
                    1,
                    False,
                    0,
                ):
                    raise_parse_error(
                        node,
                        "Requires sequence of boolean values "
                        "(one of True, 1, False, 0)",
                    )
            return values

        def gds_validate_datetime(self, input_data, node=None, input_name=""):
            return input_data

        def gds_format_datetime(self, input_data, input_name=""):
            if input_data.microsecond == 0:
                _svalue = "%04d-%02d-%02dT%02d:%02d:%02d" % (
                    input_data.year,
                    input_data.month,
                    input_data.day,
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                )
            else:
                _svalue = "%04d-%02d-%02dT%02d:%02d:%02d.%s" % (
                    input_data.year,
                    input_data.month,
                    input_data.day,
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                    ("%f" % (float(input_data.microsecond) / 1000000))[2:],
                )
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)
                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)
                    if total_seconds == 0:
                        _svalue += "Z"
                    else:
                        if total_seconds < 0:
                            _svalue += "-"
                            total_seconds *= -1
                        else:
                            _svalue += "+"
                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += "{0:02d}:{1:02d}".format(hours, minutes)
            return _svalue

        @classmethod
        def gds_parse_datetime(cls, input_data):
            tz = None
            if input_data[-1] == "Z":
                tz = GeneratedsSuper._FixedOffsetTZ(0, "UTC")
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(":")
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == "-":
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(tzoff, results.group(0))
                    input_data = input_data[:-6]
            time_parts = input_data.split(".")
            if len(time_parts) > 1:
                micro_seconds = int(float("0." + time_parts[1]) * 1000000)
                input_data = "%s.%s" % (
                    time_parts[0],
                    "{}".format(micro_seconds).rjust(6, "0"),
                )
                dt = datetime_.datetime.strptime(input_data, "%Y-%m-%dT%H:%M:%S.%f")
            else:
                dt = datetime_.datetime.strptime(input_data, "%Y-%m-%dT%H:%M:%S")
            dt = dt.replace(tzinfo=tz)
            return dt

        def gds_validate_date(self, input_data, node=None, input_name=""):
            return input_data

        def gds_format_date(self, input_data, input_name=""):
            _svalue = "%04d-%02d-%02d" % (
                input_data.year,
                input_data.month,
                input_data.day,
            )
            try:
                if input_data.tzinfo is not None:
                    tzoff = input_data.tzinfo.utcoffset(input_data)
                    if tzoff is not None:
                        total_seconds = tzoff.seconds + (86400 * tzoff.days)
                        if total_seconds == 0:
                            _svalue += "Z"
                        else:
                            if total_seconds < 0:
                                _svalue += "-"
                                total_seconds *= -1
                            else:
                                _svalue += "+"
                            hours = total_seconds // 3600
                            minutes = (total_seconds - (hours * 3600)) // 60
                            _svalue += "{0:02d}:{1:02d}".format(hours, minutes)
            except AttributeError:
                pass
            return _svalue

        @classmethod
        def gds_parse_date(cls, input_data):
            tz = None
            if input_data[-1] == "Z":
                tz = GeneratedsSuper._FixedOffsetTZ(0, "UTC")
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(":")
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == "-":
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(tzoff, results.group(0))
                    input_data = input_data[:-6]
            dt = datetime_.datetime.strptime(input_data, "%Y-%m-%d")
            dt = dt.replace(tzinfo=tz)
            return dt.date()

        def gds_validate_time(self, input_data, node=None, input_name=""):
            return input_data

        def gds_format_time(self, input_data, input_name=""):
            if input_data.microsecond == 0:
                _svalue = "%02d:%02d:%02d" % (
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                )
            else:
                _svalue = "%02d:%02d:%02d.%s" % (
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                    ("%f" % (float(input_data.microsecond) / 1000000))[2:],
                )
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)
                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)
                    if total_seconds == 0:
                        _svalue += "Z"
                    else:
                        if total_seconds < 0:
                            _svalue += "-"
                            total_seconds *= -1
                        else:
                            _svalue += "+"
                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += "{0:02d}:{1:02d}".format(hours, minutes)
            return _svalue

        def gds_validate_simple_patterns(self, patterns, target):
            # pat is a list of lists of strings/patterns.
            # The target value must match at least one of the patterns
            # in order for the test to succeed.
            found1 = True
            target = str(target)
            for patterns1 in patterns:
                found2 = False
                for patterns2 in patterns1:
                    mo = re_.search(patterns2, target)
                    if mo is not None and len(mo.group(0)) == len(target):
                        found2 = True
                        break
                if not found2:
                    found1 = False
                    break
            return found1

        @classmethod
        def gds_parse_time(cls, input_data):
            tz = None
            if input_data[-1] == "Z":
                tz = GeneratedsSuper._FixedOffsetTZ(0, "UTC")
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(":")
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == "-":
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(tzoff, results.group(0))
                    input_data = input_data[:-6]
            if len(input_data.split(".")) > 1:
                dt = datetime_.datetime.strptime(input_data, "%H:%M:%S.%f")
            else:
                dt = datetime_.datetime.strptime(input_data, "%H:%M:%S")
            dt = dt.replace(tzinfo=tz)
            return dt.time()

        def gds_check_cardinality_(
            self, value, input_name, min_occurs=0, max_occurs=1, required=None
        ):
            if value is None:
                length = 0
            elif isinstance(value, list):
                length = len(value)
            else:
                length = 1
            if required is not None:
                if required and length < 1:
                    self.gds_collector_.add_message(
                        "Required value {}{} is missing".format(
                            input_name, self.gds_get_node_lineno_()
                        )
                    )
            if length < min_occurs:
                self.gds_collector_.add_message(
                    "Number of values for {}{} is below "
                    "the minimum allowed, "
                    "expected at least {}, found {}".format(
                        input_name, self.gds_get_node_lineno_(), min_occurs, length
                    )
                )
            elif length > max_occurs:
                self.gds_collector_.add_message(
                    "Number of values for {}{} is above "
                    "the maximum allowed, "
                    "expected at most {}, found {}".format(
                        input_name, self.gds_get_node_lineno_(), max_occurs, length
                    )
                )

        def gds_validate_builtin_ST_(
            self,
            validator,
            value,
            input_name,
            min_occurs=None,
            max_occurs=None,
            required=None,
        ):
            if value is not None:
                try:
                    validator(value, input_name=input_name)
                except GDSParseError as parse_error:
                    self.gds_collector_.add_message(str(parse_error))

        def gds_validate_defined_ST_(
            self,
            validator,
            value,
            input_name,
            min_occurs=None,
            max_occurs=None,
            required=None,
        ):
            if value is not None:
                try:
                    validator(value)
                except GDSParseError as parse_error:
                    self.gds_collector_.add_message(str(parse_error))

        def gds_str_lower(self, instring):
            return instring.lower()

        def get_path_(self, node):
            path_list = []
            self.get_path_list_(node, path_list)
            path_list.reverse()
            path = "/".join(path_list)
            return path

        Tag_strip_pattern_ = re_.compile(r"\{.*\}")

        def get_path_list_(self, node, path_list):
            if node is None:
                return
            tag = GeneratedsSuper.Tag_strip_pattern_.sub("", node.tag)
            if tag:
                path_list.append(tag)
            self.get_path_list_(node.getparent(), path_list)

        def get_class_obj_(self, node, default_class=None):
            class_obj1 = default_class
            if "xsi" in node.nsmap:
                classname = node.get("{%s}type" % node.nsmap["xsi"])
                if classname is not None:
                    names = classname.split(":")
                    if len(names) == 2:
                        classname = names[1]
                    class_obj2 = globals().get(classname)
                    if class_obj2 is not None:
                        class_obj1 = class_obj2
            return class_obj1

        def gds_build_any(self, node, type_name=None):
            # provide default value in case option --disable-xml is used.
            content = ""
            content = etree_.tostring(node, encoding="unicode")
            return content

        @classmethod
        def gds_reverse_node_mapping(cls, mapping):
            return dict(((v, k) for k, v in mapping.items()))

        @staticmethod
        def gds_encode(instring):
            if sys.version_info.major == 2:
                if ExternalEncoding:
                    encoding = ExternalEncoding
                else:
                    encoding = "utf-8"
                return instring.encode(encoding)
            else:
                return instring

        @staticmethod
        def convert_unicode(instring):
            if isinstance(instring, str):
                result = quote_xml(instring)
            elif sys.version_info.major == 2 and isinstance(instring, unicode):
                result = quote_xml(instring).encode("utf8")
            else:
                result = GeneratedsSuper.gds_encode(str(instring))
            return result

        def __eq__(self, other):
            def excl_select_objs_(obj):
                return obj[0] != "parent_object_" and obj[0] != "gds_collector_"

            if type(self) != type(other):
                return False
            return all(
                x == y
                for x, y in zip_longest(
                    filter(excl_select_objs_, self.__dict__.items()),
                    filter(excl_select_objs_, other.__dict__.items()),
                )
            )

        def __ne__(self, other):
            return not self.__eq__(other)

        # Django ETL transform hooks.
        def gds_djo_etl_transform(self):
            pass

        def gds_djo_etl_transform_db_obj(self, dbobj):
            pass

        # SQLAlchemy ETL transform hooks.
        def gds_sqa_etl_transform(self):
            return 0, None

        def gds_sqa_etl_transform_db_obj(self, dbobj):
            pass

        def gds_get_node_lineno_(self):
            if (
                hasattr(self, "gds_elementtree_node_")
                and self.gds_elementtree_node_ is not None
            ):
                return " near line {}".format(self.gds_elementtree_node_.sourceline)
            else:
                return ""

    def getSubclassFromModule_(module, class_):
        """Get the subclass of a class from a specific module."""
        name = class_.__name__ + "Sub"
        if hasattr(module, name):
            return getattr(module, name)
        else:
            return None


#
# If you have installed IPython you can uncomment and use the following.
# IPython is available from http://ipython.scipy.org/.
#

## from IPython.Shell import IPShellEmbed
## args = ''
## ipshell = IPShellEmbed(args,
##     banner = 'Dropping into IPython',
##     exit_msg = 'Leaving Interpreter, back to program.')

# Then use the following line where and when you want to drop into the
# IPython shell:
#    ipshell('<some message> -- Entering ipshell.\nHit Ctrl-D to exit')

#
# Globals
#

ExternalEncoding = ""
# Set this to false in order to deactivate during export, the use of
# name space prefixes captured from the input document.
UseCapturedNS_ = True
CapturedNsmap_ = {}
Tag_pattern_ = re_.compile(r"({.*})?(.*)")
String_cleanup_pat_ = re_.compile(r"[\n\r\s]+")
Namespace_extract_pat_ = re_.compile(r"{(.*)}(.*)")
CDATA_pattern_ = re_.compile(r"<!\[CDATA\[.*?\]\]>", re_.DOTALL)

# Change this to redirect the generated superclass module to use a
# specific subclass module.
CurrentSubclassModule_ = None

#
# Support/utility functions.
#


def showIndent(outfile, level, pretty_print=True):
    if pretty_print:
        for idx in range(level):
            outfile.write("    ")


def quote_xml(inStr):
    "Escape markup chars, but do not modify CDATA sections."
    if not inStr:
        return ""
    s1 = isinstance(inStr, BaseStrType_) and inStr or "%s" % inStr
    s2 = ""
    pos = 0
    matchobjects = CDATA_pattern_.finditer(s1)
    for mo in matchobjects:
        s3 = s1[pos : mo.start()]
        s2 += quote_xml_aux(s3)
        s2 += s1[mo.start() : mo.end()]
        pos = mo.end()
    s3 = s1[pos:]
    s2 += quote_xml_aux(s3)
    return s2


def quote_xml_aux(inStr):
    s1 = inStr.replace("&", "&amp;")
    s1 = s1.replace("<", "&lt;")
    s1 = s1.replace(">", "&gt;")
    return s1


def quote_attrib(inStr):
    s1 = isinstance(inStr, BaseStrType_) and inStr or "%s" % inStr
    s1 = s1.replace("&", "&amp;")
    s1 = s1.replace("<", "&lt;")
    s1 = s1.replace(">", "&gt;")
    s1 = s1.replace("\n", "&#10;")
    if '"' in s1:
        if "'" in s1:
            s1 = '"%s"' % s1.replace('"', "&quot;")
        else:
            s1 = "'%s'" % s1
    else:
        s1 = '"%s"' % s1
    return s1


def quote_python(inStr):
    s1 = inStr
    if s1.find("'") == -1:
        if s1.find("\n") == -1:
            return "'%s'" % s1
        else:
            return "'''%s'''" % s1
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find("\n") == -1:
            return '"%s"' % s1
        else:
            return '"""%s"""' % s1


def get_all_text_(node):
    if node.text is not None:
        text = node.text
    else:
        text = ""
    for child in node:
        if child.tail is not None:
            text += child.tail
    return text


def find_attr_value_(attr_name, node):
    attrs = node.attrib
    attr_parts = attr_name.split(":")
    value = None
    if len(attr_parts) == 1:
        value = attrs.get(attr_name)
    elif len(attr_parts) == 2:
        prefix, name = attr_parts
        if prefix == "xml":
            namespace = "http://www.w3.org/XML/1998/namespace"
        else:
            namespace = node.nsmap.get(prefix)
        if namespace is not None:
            value = attrs.get(
                "{%s}%s"
                % (
                    namespace,
                    name,
                )
            )
    return value


def encode_str_2_3(instr):
    return instr


class GDSParseError(Exception):
    pass


def raise_parse_error(node, msg):
    if node is not None:
        msg = "%s (element %s/line %d)" % (
            msg,
            node.tag,
            node.sourceline,
        )
    raise GDSParseError(msg)


class MixedContainer:
    # Constants for category:
    CategoryNone = 0
    CategoryText = 1
    CategorySimple = 2
    CategoryComplex = 3
    # Constants for content_type:
    TypeNone = 0
    TypeText = 1
    TypeString = 2
    TypeInteger = 3
    TypeFloat = 4
    TypeDecimal = 5
    TypeDouble = 6
    TypeBoolean = 7
    TypeBase64 = 8

    def __init__(self, category, content_type, name, value):
        self.category = category
        self.content_type = content_type
        self.name = name
        self.value = value

    def getCategory(self):
        return self.category

    def getContenttype(self, content_type):
        return self.content_type

    def getValue(self):
        return self.value

    def getName(self):
        return self.name

    def export(self, outfile, level, name, namespace, pretty_print=True):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip():
                outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:  # category == MixedContainer.CategoryComplex
            self.value.export(
                outfile, level, namespace, name_=name, pretty_print=pretty_print
            )

    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write("<%s>%s</%s>" % (self.name, self.value, self.name))
        elif (
            self.content_type == MixedContainer.TypeInteger
            or self.content_type == MixedContainer.TypeBoolean
        ):
            outfile.write("<%s>%d</%s>" % (self.name, self.value, self.name))
        elif (
            self.content_type == MixedContainer.TypeFloat
            or self.content_type == MixedContainer.TypeDecimal
        ):
            outfile.write("<%s>%f</%s>" % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeDouble:
            outfile.write("<%s>%g</%s>" % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeBase64:
            outfile.write(
                "<%s>%s</%s>" % (self.name, base64.b64encode(self.value), self.name)
            )

    def to_etree(self, element, mapping_=None, reverse_mapping_=None, nsmap_=None):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip():
                if len(element) > 0:
                    if element[-1].tail is None:
                        element[-1].tail = self.value
                    else:
                        element[-1].tail += self.value
                else:
                    if element.text is None:
                        element.text = self.value
                    else:
                        element.text += self.value
        elif self.category == MixedContainer.CategorySimple:
            subelement = etree_.SubElement(element, "%s" % self.name)
            subelement.text = self.to_etree_simple()
        else:  # category == MixedContainer.CategoryComplex
            self.value.to_etree(element)

    def to_etree_simple(self, mapping_=None, reverse_mapping_=None, nsmap_=None):
        if self.content_type == MixedContainer.TypeString:
            text = self.value
        elif (
            self.content_type == MixedContainer.TypeInteger
            or self.content_type == MixedContainer.TypeBoolean
        ):
            text = "%d" % self.value
        elif (
            self.content_type == MixedContainer.TypeFloat
            or self.content_type == MixedContainer.TypeDecimal
        ):
            text = "%f" % self.value
        elif self.content_type == MixedContainer.TypeDouble:
            text = "%g" % self.value
        elif self.content_type == MixedContainer.TypeBase64:
            text = "%s" % base64.b64encode(self.value)
        return text

    def exportLiteral(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s", "%s"),\n'
                % (self.category, self.content_type, self.name, self.value)
            )
        elif self.category == MixedContainer.CategorySimple:
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s", "%s"),\n'
                % (self.category, self.content_type, self.name, self.value)
            )
        else:  # category == MixedContainer.CategoryComplex
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s",\n'
                % (
                    self.category,
                    self.content_type,
                    self.name,
                )
            )
            self.value.exportLiteral(outfile, level + 1)
            showIndent(outfile, level)
            outfile.write(")\n")


class MemberSpec_(object):
    def __init__(
        self,
        name="",
        data_type="",
        container=0,
        optional=0,
        child_attrs=None,
        choice=None,
    ):
        self.name = name
        self.data_type = data_type
        self.container = container
        self.child_attrs = child_attrs
        self.choice = choice
        self.optional = optional

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_data_type(self, data_type):
        self.data_type = data_type

    def get_data_type_chain(self):
        return self.data_type

    def get_data_type(self):
        if isinstance(self.data_type, list):
            if len(self.data_type) > 0:
                return self.data_type[-1]
            else:
                return "xs:string"
        else:
            return self.data_type

    def set_container(self, container):
        self.container = container

    def get_container(self):
        return self.container

    def set_child_attrs(self, child_attrs):
        self.child_attrs = child_attrs

    def get_child_attrs(self):
        return self.child_attrs

    def set_choice(self, choice):
        self.choice = choice

    def get_choice(self):
        return self.choice

    def set_optional(self, optional):
        self.optional = optional

    def get_optional(self):
        return self.optional


def _cast(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)


#
# Data representation classes.
#


class Freightcom(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self, version=None, ShippingReply=None, gds_collector_=None, **kwargs_
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get("parent_object_")
        self.ns_prefix_ = None
        self.version = _cast(None, version)
        self.version_nsprefix_ = None
        self.ShippingReply = ShippingReply
        self.ShippingReply_nsprefix_ = None

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, Freightcom)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Freightcom.subclass:
            return Freightcom.subclass(*args_, **kwargs_)
        else:
            return Freightcom(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_ShippingReply(self):
        return self.ShippingReply

    def set_ShippingReply(self, ShippingReply):
        self.ShippingReply = ShippingReply

    def get_version(self):
        return self.version

    def set_version(self, version):
        self.version = version

    def _hasContent(self):
        if self.ShippingReply is not None:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="Freightcom",
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get("Freightcom")
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = "\n"
        else:
            eol_ = ""
        if self.original_tagname_ is not None and name_ == "Freightcom":
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ":"
        showIndent(outfile, level, pretty_print)
        outfile.write(
            "<%s%s%s"
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and " " + namespacedef_ or "",
            )
        )
        already_processed = set()
        self._exportAttributes(
            outfile, level, already_processed, namespaceprefix_, name_="Freightcom"
        )
        if self._hasContent():
            outfile.write(">%s" % (eol_,))
            self._exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_="Freightcom",
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write("</%s%s>%s" % (namespaceprefix_, name_, eol_))
        else:
            outfile.write("/>%s" % (eol_,))

    def _exportAttributes(
        self, outfile, level, already_processed, namespaceprefix_="", name_="Freightcom"
    ):
        if self.version is not None and "version" not in already_processed:
            already_processed.add("version")
            outfile.write(
                " version=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.version), input_name="version"
                        )
                    ),
                )
            )

    def _exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="Freightcom",
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = "\n"
        else:
            eol_ = ""
        if self.ShippingReply is not None:
            namespaceprefix_ = (
                self.ShippingReply_nsprefix_ + ":"
                if (UseCapturedNS_ and self.ShippingReply_nsprefix_)
                else ""
            )
            self.ShippingReply.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_="",
                name_="ShippingReply",
                pretty_print=pretty_print,
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_("version", node)
        if value is not None and "version" not in already_processed:
            already_processed.add("version")
            self.version = value

    def _buildChildren(
        self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None
    ):
        if nodeName_ == "ShippingReply":
            obj_ = ShippingReplyType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShippingReply = obj_
            obj_.original_tagname_ = "ShippingReply"


# end class Freightcom


class ShippingReplyType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self,
        Order=None,
        Carrier=None,
        Reference=None,
        Package=None,
        Pickup=None,
        TrackingURL=None,
        Labels=None,
        CustomsInvoice=None,
        LabelData=None,
        Quote=None,
        BillingAddress=None,
        gds_collector_=None,
        **kwargs_
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get("parent_object_")
        self.ns_prefix_ = None
        self.Order = Order
        self.Order_nsprefix_ = None
        self.Carrier = Carrier
        self.Carrier_nsprefix_ = None
        self.Reference = Reference
        self.Reference_nsprefix_ = None
        if Package is None:
            self.Package = []
        else:
            self.Package = Package
        self.Package_nsprefix_ = None
        self.Pickup = Pickup
        self.Pickup_nsprefix_ = None
        self.TrackingURL = TrackingURL
        self.TrackingURL_nsprefix_ = None
        self.Labels = Labels
        self.Labels_nsprefix_ = None
        self.CustomsInvoice = CustomsInvoice
        self.CustomsInvoice_nsprefix_ = None
        self.LabelData = LabelData
        self.LabelData_nsprefix_ = None
        self.Quote = Quote
        self.Quote_nsprefix_ = None
        self.BillingAddress = BillingAddress
        self.BillingAddress_nsprefix_ = None

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, ShippingReplyType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShippingReplyType.subclass:
            return ShippingReplyType.subclass(*args_, **kwargs_)
        else:
            return ShippingReplyType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_Order(self):
        return self.Order

    def set_Order(self, Order):
        self.Order = Order

    def get_Carrier(self):
        return self.Carrier

    def set_Carrier(self, Carrier):
        self.Carrier = Carrier

    def get_Reference(self):
        return self.Reference

    def set_Reference(self, Reference):
        self.Reference = Reference

    def get_Package(self):
        return self.Package

    def set_Package(self, Package):
        self.Package = Package

    def add_Package(self, value):
        self.Package.append(value)

    def insert_Package_at(self, index, value):
        self.Package.insert(index, value)

    def replace_Package_at(self, index, value):
        self.Package[index] = value

    def get_Pickup(self):
        return self.Pickup

    def set_Pickup(self, Pickup):
        self.Pickup = Pickup

    def get_TrackingURL(self):
        return self.TrackingURL

    def set_TrackingURL(self, TrackingURL):
        self.TrackingURL = TrackingURL

    def get_Labels(self):
        return self.Labels

    def set_Labels(self, Labels):
        self.Labels = Labels

    def get_CustomsInvoice(self):
        return self.CustomsInvoice

    def set_CustomsInvoice(self, CustomsInvoice):
        self.CustomsInvoice = CustomsInvoice

    def get_LabelData(self):
        return self.LabelData

    def set_LabelData(self, LabelData):
        self.LabelData = LabelData

    def get_Quote(self):
        return self.Quote

    def set_Quote(self, Quote):
        self.Quote = Quote

    def get_BillingAddress(self):
        return self.BillingAddress

    def set_BillingAddress(self, BillingAddress):
        self.BillingAddress = BillingAddress

    def _hasContent(self):
        if (
            self.Order is not None
            or self.Carrier is not None
            or self.Reference is not None
            or self.Package
            or self.Pickup is not None
            or self.TrackingURL is not None
            or self.Labels is not None
            or self.CustomsInvoice is not None
            or self.LabelData is not None
            or self.Quote is not None
            or self.BillingAddress is not None
        ):
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="ShippingReplyType",
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get("ShippingReplyType")
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = "\n"
        else:
            eol_ = ""
        if self.original_tagname_ is not None and name_ == "ShippingReplyType":
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ":"
        showIndent(outfile, level, pretty_print)
        outfile.write(
            "<%s%s%s"
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and " " + namespacedef_ or "",
            )
        )
        already_processed = set()
        self._exportAttributes(
            outfile,
            level,
            already_processed,
            namespaceprefix_,
            name_="ShippingReplyType",
        )
        if self._hasContent():
            outfile.write(">%s" % (eol_,))
            self._exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_="ShippingReplyType",
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write("</%s%s>%s" % (namespaceprefix_, name_, eol_))
        else:
            outfile.write("/>%s" % (eol_,))

    def _exportAttributes(
        self,
        outfile,
        level,
        already_processed,
        namespaceprefix_="",
        name_="ShippingReplyType",
    ):
        pass

    def _exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="ShippingReplyType",
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = "\n"
        else:
            eol_ = ""
        if self.Order is not None:
            namespaceprefix_ = (
                self.Order_nsprefix_ + ":"
                if (UseCapturedNS_ and self.Order_nsprefix_)
                else ""
            )
            self.Order.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_="",
                name_="Order",
                pretty_print=pretty_print,
            )
        if self.Carrier is not None:
            namespaceprefix_ = (
                self.Carrier_nsprefix_ + ":"
                if (UseCapturedNS_ and self.Carrier_nsprefix_)
                else ""
            )
            self.Carrier.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_="",
                name_="Carrier",
                pretty_print=pretty_print,
            )
        if self.Reference is not None:
            namespaceprefix_ = (
                self.Reference_nsprefix_ + ":"
                if (UseCapturedNS_ and self.Reference_nsprefix_)
                else ""
            )
            self.Reference.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_="",
                name_="Reference",
                pretty_print=pretty_print,
            )
        for Package_ in self.Package:
            namespaceprefix_ = (
                self.Package_nsprefix_ + ":"
                if (UseCapturedNS_ and self.Package_nsprefix_)
                else ""
            )
            Package_.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_="",
                name_="Package",
                pretty_print=pretty_print,
            )
        if self.Pickup is not None:
            namespaceprefix_ = (
                self.Pickup_nsprefix_ + ":"
                if (UseCapturedNS_ and self.Pickup_nsprefix_)
                else ""
            )
            self.Pickup.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_="",
                name_="Pickup",
                pretty_print=pretty_print,
            )
        if self.TrackingURL is not None:
            namespaceprefix_ = (
                self.TrackingURL_nsprefix_ + ":"
                if (UseCapturedNS_ and self.TrackingURL_nsprefix_)
                else ""
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                "<%sTrackingURL>%s</%sTrackingURL>%s"
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(
                            quote_xml(self.TrackingURL), input_name="TrackingURL"
                        )
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.Labels is not None:
            namespaceprefix_ = (
                self.Labels_nsprefix_ + ":"
                if (UseCapturedNS_ and self.Labels_nsprefix_)
                else ""
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                "<%sLabels>%s</%sLabels>%s"
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(
                            quote_xml(self.Labels), input_name="Labels"
                        )
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.CustomsInvoice is not None:
            namespaceprefix_ = (
                self.CustomsInvoice_nsprefix_ + ":"
                if (UseCapturedNS_ and self.CustomsInvoice_nsprefix_)
                else ""
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                "<%sCustomsInvoice>%s</%sCustomsInvoice>%s"
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(
                            quote_xml(self.CustomsInvoice), input_name="CustomsInvoice"
                        )
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.LabelData is not None:
            namespaceprefix_ = (
                self.LabelData_nsprefix_ + ":"
                if (UseCapturedNS_ and self.LabelData_nsprefix_)
                else ""
            )
            self.LabelData.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_="",
                name_="LabelData",
                pretty_print=pretty_print,
            )
        if self.Quote is not None:
            namespaceprefix_ = (
                self.Quote_nsprefix_ + ":"
                if (UseCapturedNS_ and self.Quote_nsprefix_)
                else ""
            )
            self.Quote.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_="",
                name_="Quote",
                pretty_print=pretty_print,
            )
        if self.BillingAddress is not None:
            namespaceprefix_ = (
                self.BillingAddress_nsprefix_ + ":"
                if (UseCapturedNS_ and self.BillingAddress_nsprefix_)
                else ""
            )
            self.BillingAddress.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_="",
                name_="BillingAddress",
                pretty_print=pretty_print,
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def _buildAttributes(self, node, attrs, already_processed):
        pass

    def _buildChildren(
        self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None
    ):
        if nodeName_ == "Order":
            obj_ = OrderType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Order = obj_
            obj_.original_tagname_ = "Order"
        elif nodeName_ == "Carrier":
            obj_ = CarrierType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Carrier = obj_
            obj_.original_tagname_ = "Carrier"
        elif nodeName_ == "Reference":
            obj_ = ReferenceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Reference = obj_
            obj_.original_tagname_ = "Reference"
        elif nodeName_ == "Package":
            obj_ = PackageType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Package.append(obj_)
            obj_.original_tagname_ = "Package"
        elif nodeName_ == "Pickup":
            obj_ = PickupType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Pickup = obj_
            obj_.original_tagname_ = "Pickup"
        elif nodeName_ == "TrackingURL":
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, "TrackingURL")
            value_ = self.gds_validate_string(value_, node, "TrackingURL")
            self.TrackingURL = value_
            self.TrackingURL_nsprefix_ = child_.prefix
        elif nodeName_ == "Labels":
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, "Labels")
            value_ = self.gds_validate_string(value_, node, "Labels")
            self.Labels = value_
            self.Labels_nsprefix_ = child_.prefix
        elif nodeName_ == "CustomsInvoice":
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, "CustomsInvoice")
            value_ = self.gds_validate_string(value_, node, "CustomsInvoice")
            self.CustomsInvoice = value_
            self.CustomsInvoice_nsprefix_ = child_.prefix
        elif nodeName_ == "LabelData":
            obj_ = LabelDataType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LabelData = obj_
            obj_.original_tagname_ = "LabelData"
        elif nodeName_ == "Quote":
            obj_ = QuoteType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Quote = obj_
            obj_.original_tagname_ = "Quote"
        elif nodeName_ == "BillingAddress":
            obj_ = BillingAddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BillingAddress = obj_
            obj_.original_tagname_ = "BillingAddress"


# end class ShippingReplyType


class OrderType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(self, id=None, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get("parent_object_")
        self.ns_prefix_ = None
        self.id = _cast(None, id)
        self.id_nsprefix_ = None
        self.valueOf_ = valueOf_

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, OrderType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OrderType.subclass:
            return OrderType.subclass(*args_, **kwargs_)
        else:
            return OrderType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_valueOf_(self):
        return self.valueOf_

    def set_valueOf_(self, valueOf_):
        self.valueOf_ = valueOf_

    def _hasContent(self):
        if 1 if type(self.valueOf_) in [int, float] else self.valueOf_:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="OrderType",
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get("OrderType")
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = "\n"
        else:
            eol_ = ""
        if self.original_tagname_ is not None and name_ == "OrderType":
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ":"
        showIndent(outfile, level, pretty_print)
        outfile.write(
            "<%s%s%s"
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and " " + namespacedef_ or "",
            )
        )
        already_processed = set()
        self._exportAttributes(
            outfile, level, already_processed, namespaceprefix_, name_="OrderType"
        )
        if self._hasContent():
            outfile.write(">")
            outfile.write(self.convert_unicode(self.valueOf_))
            self._exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_="OrderType",
                pretty_print=pretty_print,
            )
            outfile.write("</%s%s>%s" % (namespaceprefix_, name_, eol_))
        else:
            outfile.write("/>%s" % (eol_,))

    def _exportAttributes(
        self, outfile, level, already_processed, namespaceprefix_="", name_="OrderType"
    ):
        if self.id is not None and "id" not in already_processed:
            already_processed.add("id")
            outfile.write(
                " id=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(quote_attrib(self.id), input_name="id")
                    ),
                )
            )

    def _exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="OrderType",
        fromsubclass_=False,
        pretty_print=True,
    ):
        pass

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_("id", node)
        if value is not None and "id" not in already_processed:
            already_processed.add("id")
            self.id = value

    def _buildChildren(
        self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None
    ):
        pass


# end class OrderType


class CarrierType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self,
        carrierName=None,
        serviceName=None,
        SCAC=None,
        valueOf_=None,
        gds_collector_=None,
        **kwargs_
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get("parent_object_")
        self.ns_prefix_ = None
        self.carrierName = _cast(None, carrierName)
        self.carrierName_nsprefix_ = None
        self.serviceName = _cast(None, serviceName)
        self.serviceName_nsprefix_ = None
        self.SCAC = _cast(None, SCAC)
        self.SCAC_nsprefix_ = None
        self.valueOf_ = valueOf_

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, CarrierType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CarrierType.subclass:
            return CarrierType.subclass(*args_, **kwargs_)
        else:
            return CarrierType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_carrierName(self):
        return self.carrierName

    def set_carrierName(self, carrierName):
        self.carrierName = carrierName

    def get_serviceName(self):
        return self.serviceName

    def set_serviceName(self, serviceName):
        self.serviceName = serviceName

    def get_SCAC(self):
        return self.SCAC

    def set_SCAC(self, SCAC):
        self.SCAC = SCAC

    def get_valueOf_(self):
        return self.valueOf_

    def set_valueOf_(self, valueOf_):
        self.valueOf_ = valueOf_

    def _hasContent(self):
        if 1 if type(self.valueOf_) in [int, float] else self.valueOf_:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="CarrierType",
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get("CarrierType")
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = "\n"
        else:
            eol_ = ""
        if self.original_tagname_ is not None and name_ == "CarrierType":
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ":"
        showIndent(outfile, level, pretty_print)
        outfile.write(
            "<%s%s%s"
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and " " + namespacedef_ or "",
            )
        )
        already_processed = set()
        self._exportAttributes(
            outfile, level, already_processed, namespaceprefix_, name_="CarrierType"
        )
        if self._hasContent():
            outfile.write(">")
            outfile.write(self.convert_unicode(self.valueOf_))
            self._exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_="CarrierType",
                pretty_print=pretty_print,
            )
            outfile.write("</%s%s>%s" % (namespaceprefix_, name_, eol_))
        else:
            outfile.write("/>%s" % (eol_,))

    def _exportAttributes(
        self,
        outfile,
        level,
        already_processed,
        namespaceprefix_="",
        name_="CarrierType",
    ):
        if self.carrierName is not None and "carrierName" not in already_processed:
            already_processed.add("carrierName")
            outfile.write(
                " carrierName=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.carrierName), input_name="carrierName"
                        )
                    ),
                )
            )
        if self.serviceName is not None and "serviceName" not in already_processed:
            already_processed.add("serviceName")
            outfile.write(
                " serviceName=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.serviceName), input_name="serviceName"
                        )
                    ),
                )
            )
        if self.SCAC is not None and "SCAC" not in already_processed:
            already_processed.add("SCAC")
            outfile.write(
                " SCAC=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.SCAC), input_name="SCAC"
                        )
                    ),
                )
            )

    def _exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="CarrierType",
        fromsubclass_=False,
        pretty_print=True,
    ):
        pass

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_("carrierName", node)
        if value is not None and "carrierName" not in already_processed:
            already_processed.add("carrierName")
            self.carrierName = value
        value = find_attr_value_("serviceName", node)
        if value is not None and "serviceName" not in already_processed:
            already_processed.add("serviceName")
            self.serviceName = value
        value = find_attr_value_("SCAC", node)
        if value is not None and "SCAC" not in already_processed:
            already_processed.add("SCAC")
            self.SCAC = value

    def _buildChildren(
        self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None
    ):
        pass


# end class CarrierType


class ReferenceType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self, code=None, name=None, valueOf_=None, gds_collector_=None, **kwargs_
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get("parent_object_")
        self.ns_prefix_ = None
        self.code = _cast(None, code)
        self.code_nsprefix_ = None
        self.name = _cast(None, name)
        self.name_nsprefix_ = None
        self.valueOf_ = valueOf_

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, ReferenceType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ReferenceType.subclass:
            return ReferenceType.subclass(*args_, **kwargs_)
        else:
            return ReferenceType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_code(self):
        return self.code

    def set_code(self, code):
        self.code = code

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_valueOf_(self):
        return self.valueOf_

    def set_valueOf_(self, valueOf_):
        self.valueOf_ = valueOf_

    def _hasContent(self):
        if 1 if type(self.valueOf_) in [int, float] else self.valueOf_:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="ReferenceType",
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get("ReferenceType")
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = "\n"
        else:
            eol_ = ""
        if self.original_tagname_ is not None and name_ == "ReferenceType":
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ":"
        showIndent(outfile, level, pretty_print)
        outfile.write(
            "<%s%s%s"
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and " " + namespacedef_ or "",
            )
        )
        already_processed = set()
        self._exportAttributes(
            outfile, level, already_processed, namespaceprefix_, name_="ReferenceType"
        )
        if self._hasContent():
            outfile.write(">")
            outfile.write(self.convert_unicode(self.valueOf_))
            self._exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_="ReferenceType",
                pretty_print=pretty_print,
            )
            outfile.write("</%s%s>%s" % (namespaceprefix_, name_, eol_))
        else:
            outfile.write("/>%s" % (eol_,))

    def _exportAttributes(
        self,
        outfile,
        level,
        already_processed,
        namespaceprefix_="",
        name_="ReferenceType",
    ):
        if self.code is not None and "code" not in already_processed:
            already_processed.add("code")
            outfile.write(
                " code=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.code), input_name="code"
                        )
                    ),
                )
            )
        if self.name is not None and "name" not in already_processed:
            already_processed.add("name")
            outfile.write(
                " name=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.name), input_name="name"
                        )
                    ),
                )
            )

    def _exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="ReferenceType",
        fromsubclass_=False,
        pretty_print=True,
    ):
        pass

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_("code", node)
        if value is not None and "code" not in already_processed:
            already_processed.add("code")
            self.code = value
        value = find_attr_value_("name", node)
        if value is not None and "name" not in already_processed:
            already_processed.add("name")
            self.name = value

    def _buildChildren(
        self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None
    ):
        pass


# end class ReferenceType


class PackageType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self, trackingNumber=None, valueOf_=None, gds_collector_=None, **kwargs_
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get("parent_object_")
        self.ns_prefix_ = None
        self.trackingNumber = _cast(None, trackingNumber)
        self.trackingNumber_nsprefix_ = None
        self.valueOf_ = valueOf_

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, PackageType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PackageType.subclass:
            return PackageType.subclass(*args_, **kwargs_)
        else:
            return PackageType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_trackingNumber(self):
        return self.trackingNumber

    def set_trackingNumber(self, trackingNumber):
        self.trackingNumber = trackingNumber

    def get_valueOf_(self):
        return self.valueOf_

    def set_valueOf_(self, valueOf_):
        self.valueOf_ = valueOf_

    def _hasContent(self):
        if 1 if type(self.valueOf_) in [int, float] else self.valueOf_:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="PackageType",
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get("PackageType")
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = "\n"
        else:
            eol_ = ""
        if self.original_tagname_ is not None and name_ == "PackageType":
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ":"
        showIndent(outfile, level, pretty_print)
        outfile.write(
            "<%s%s%s"
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and " " + namespacedef_ or "",
            )
        )
        already_processed = set()
        self._exportAttributes(
            outfile, level, already_processed, namespaceprefix_, name_="PackageType"
        )
        if self._hasContent():
            outfile.write(">")
            outfile.write(self.convert_unicode(self.valueOf_))
            self._exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_="PackageType",
                pretty_print=pretty_print,
            )
            outfile.write("</%s%s>%s" % (namespaceprefix_, name_, eol_))
        else:
            outfile.write("/>%s" % (eol_,))

    def _exportAttributes(
        self,
        outfile,
        level,
        already_processed,
        namespaceprefix_="",
        name_="PackageType",
    ):
        if (
            self.trackingNumber is not None
            and "trackingNumber" not in already_processed
        ):
            already_processed.add("trackingNumber")
            outfile.write(
                " trackingNumber=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.trackingNumber),
                            input_name="trackingNumber",
                        )
                    ),
                )
            )

    def _exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="PackageType",
        fromsubclass_=False,
        pretty_print=True,
    ):
        pass

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_("trackingNumber", node)
        if value is not None and "trackingNumber" not in already_processed:
            already_processed.add("trackingNumber")
            self.trackingNumber = value

    def _buildChildren(
        self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None
    ):
        pass


# end class PackageType


class PickupType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self, confirmationNumber=None, valueOf_=None, gds_collector_=None, **kwargs_
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get("parent_object_")
        self.ns_prefix_ = None
        self.confirmationNumber = _cast(None, confirmationNumber)
        self.confirmationNumber_nsprefix_ = None
        self.valueOf_ = valueOf_

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, PickupType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PickupType.subclass:
            return PickupType.subclass(*args_, **kwargs_)
        else:
            return PickupType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_confirmationNumber(self):
        return self.confirmationNumber

    def set_confirmationNumber(self, confirmationNumber):
        self.confirmationNumber = confirmationNumber

    def get_valueOf_(self):
        return self.valueOf_

    def set_valueOf_(self, valueOf_):
        self.valueOf_ = valueOf_

    def _hasContent(self):
        if 1 if type(self.valueOf_) in [int, float] else self.valueOf_:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="PickupType",
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get("PickupType")
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = "\n"
        else:
            eol_ = ""
        if self.original_tagname_ is not None and name_ == "PickupType":
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ":"
        showIndent(outfile, level, pretty_print)
        outfile.write(
            "<%s%s%s"
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and " " + namespacedef_ or "",
            )
        )
        already_processed = set()
        self._exportAttributes(
            outfile, level, already_processed, namespaceprefix_, name_="PickupType"
        )
        if self._hasContent():
            outfile.write(">")
            outfile.write(self.convert_unicode(self.valueOf_))
            self._exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_="PickupType",
                pretty_print=pretty_print,
            )
            outfile.write("</%s%s>%s" % (namespaceprefix_, name_, eol_))
        else:
            outfile.write("/>%s" % (eol_,))

    def _exportAttributes(
        self, outfile, level, already_processed, namespaceprefix_="", name_="PickupType"
    ):
        if (
            self.confirmationNumber is not None
            and "confirmationNumber" not in already_processed
        ):
            already_processed.add("confirmationNumber")
            outfile.write(
                " confirmationNumber=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.confirmationNumber),
                            input_name="confirmationNumber",
                        )
                    ),
                )
            )

    def _exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="PickupType",
        fromsubclass_=False,
        pretty_print=True,
    ):
        pass

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_("confirmationNumber", node)
        if value is not None and "confirmationNumber" not in already_processed:
            already_processed.add("confirmationNumber")
            self.confirmationNumber = value

    def _buildChildren(
        self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None
    ):
        pass


# end class PickupType


class LabelDataType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(self, Label=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get("parent_object_")
        self.ns_prefix_ = None
        if Label is None:
            self.Label = []
        else:
            self.Label = Label
        self.Label_nsprefix_ = None

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, LabelDataType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LabelDataType.subclass:
            return LabelDataType.subclass(*args_, **kwargs_)
        else:
            return LabelDataType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_Label(self):
        return self.Label

    def set_Label(self, Label):
        self.Label = Label

    def add_Label(self, value):
        self.Label.append(value)

    def insert_Label_at(self, index, value):
        self.Label.insert(index, value)

    def replace_Label_at(self, index, value):
        self.Label[index] = value

    def _hasContent(self):
        if self.Label:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="LabelDataType",
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get("LabelDataType")
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = "\n"
        else:
            eol_ = ""
        if self.original_tagname_ is not None and name_ == "LabelDataType":
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ":"
        showIndent(outfile, level, pretty_print)
        outfile.write(
            "<%s%s%s"
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and " " + namespacedef_ or "",
            )
        )
        already_processed = set()
        self._exportAttributes(
            outfile, level, already_processed, namespaceprefix_, name_="LabelDataType"
        )
        if self._hasContent():
            outfile.write(">%s" % (eol_,))
            self._exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_="LabelDataType",
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write("</%s%s>%s" % (namespaceprefix_, name_, eol_))
        else:
            outfile.write("/>%s" % (eol_,))

    def _exportAttributes(
        self,
        outfile,
        level,
        already_processed,
        namespaceprefix_="",
        name_="LabelDataType",
    ):
        pass

    def _exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="LabelDataType",
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = "\n"
        else:
            eol_ = ""
        for Label_ in self.Label:
            namespaceprefix_ = (
                self.Label_nsprefix_ + ":"
                if (UseCapturedNS_ and self.Label_nsprefix_)
                else ""
            )
            Label_.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_="",
                name_="Label",
                pretty_print=pretty_print,
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def _buildAttributes(self, node, attrs, already_processed):
        pass

    def _buildChildren(
        self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None
    ):
        if nodeName_ == "Label":
            obj_ = LabelType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Label.append(obj_)
            obj_.original_tagname_ = "Label"


# end class LabelDataType


class LabelType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(self, Type=None, Data=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get("parent_object_")
        self.ns_prefix_ = None
        self.Type = Type
        self.Type_nsprefix_ = None
        self.Data = Data
        self.Data_nsprefix_ = None

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, LabelType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LabelType.subclass:
            return LabelType.subclass(*args_, **kwargs_)
        else:
            return LabelType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_Type(self):
        return self.Type

    def set_Type(self, Type):
        self.Type = Type

    def get_Data(self):
        return self.Data

    def set_Data(self, Data):
        self.Data = Data

    def _hasContent(self):
        if self.Type is not None or self.Data is not None:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="LabelType",
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get("LabelType")
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = "\n"
        else:
            eol_ = ""
        if self.original_tagname_ is not None and name_ == "LabelType":
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ":"
        showIndent(outfile, level, pretty_print)
        outfile.write(
            "<%s%s%s"
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and " " + namespacedef_ or "",
            )
        )
        already_processed = set()
        self._exportAttributes(
            outfile, level, already_processed, namespaceprefix_, name_="LabelType"
        )
        if self._hasContent():
            outfile.write(">%s" % (eol_,))
            self._exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_="LabelType",
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write("</%s%s>%s" % (namespaceprefix_, name_, eol_))
        else:
            outfile.write("/>%s" % (eol_,))

    def _exportAttributes(
        self, outfile, level, already_processed, namespaceprefix_="", name_="LabelType"
    ):
        pass

    def _exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="LabelType",
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = "\n"
        else:
            eol_ = ""
        if self.Type is not None:
            namespaceprefix_ = (
                self.Type_nsprefix_ + ":"
                if (UseCapturedNS_ and self.Type_nsprefix_)
                else ""
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                "<%sType>%s</%sType>%s"
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(quote_xml(self.Type), input_name="Type")
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.Data is not None:
            namespaceprefix_ = (
                self.Data_nsprefix_ + ":"
                if (UseCapturedNS_ and self.Data_nsprefix_)
                else ""
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                "<%sData>%s</%sData>%s"
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(quote_xml(self.Data), input_name="Data")
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def _buildAttributes(self, node, attrs, already_processed):
        pass

    def _buildChildren(
        self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None
    ):
        if nodeName_ == "Type":
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, "Type")
            value_ = self.gds_validate_string(value_, node, "Type")
            self.Type = value_
            self.Type_nsprefix_ = child_.prefix
        elif nodeName_ == "Data":
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, "Data")
            value_ = self.gds_validate_string(value_, node, "Data")
            self.Data = value_
            self.Data_nsprefix_ = child_.prefix


# end class LabelType


class QuoteType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self,
        carrierId=None,
        carrierName=None,
        serviceId=None,
        serviceName=None,
        modeTransport=None,
        transitDays=None,
        baseCharge=None,
        fuelSurcharge=None,
        totalCharge=None,
        currency=None,
        Surcharge=None,
        gds_collector_=None,
        **kwargs_
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get("parent_object_")
        self.ns_prefix_ = None
        self.carrierId = _cast(int, carrierId)
        self.carrierId_nsprefix_ = None
        self.carrierName = _cast(None, carrierName)
        self.carrierName_nsprefix_ = None
        self.serviceId = _cast(int, serviceId)
        self.serviceId_nsprefix_ = None
        self.serviceName = _cast(None, serviceName)
        self.serviceName_nsprefix_ = None
        self.modeTransport = _cast(None, modeTransport)
        self.modeTransport_nsprefix_ = None
        self.transitDays = _cast(int, transitDays)
        self.transitDays_nsprefix_ = None
        self.baseCharge = _cast(float, baseCharge)
        self.baseCharge_nsprefix_ = None
        self.fuelSurcharge = _cast(float, fuelSurcharge)
        self.fuelSurcharge_nsprefix_ = None
        self.totalCharge = _cast(float, totalCharge)
        self.totalCharge_nsprefix_ = None
        self.currency = _cast(None, currency)
        self.currency_nsprefix_ = None
        if Surcharge is None:
            self.Surcharge = []
        else:
            self.Surcharge = Surcharge
        self.Surcharge_nsprefix_ = None

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, QuoteType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if QuoteType.subclass:
            return QuoteType.subclass(*args_, **kwargs_)
        else:
            return QuoteType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_Surcharge(self):
        return self.Surcharge

    def set_Surcharge(self, Surcharge):
        self.Surcharge = Surcharge

    def add_Surcharge(self, value):
        self.Surcharge.append(value)

    def insert_Surcharge_at(self, index, value):
        self.Surcharge.insert(index, value)

    def replace_Surcharge_at(self, index, value):
        self.Surcharge[index] = value

    def get_carrierId(self):
        return self.carrierId

    def set_carrierId(self, carrierId):
        self.carrierId = carrierId

    def get_carrierName(self):
        return self.carrierName

    def set_carrierName(self, carrierName):
        self.carrierName = carrierName

    def get_serviceId(self):
        return self.serviceId

    def set_serviceId(self, serviceId):
        self.serviceId = serviceId

    def get_serviceName(self):
        return self.serviceName

    def set_serviceName(self, serviceName):
        self.serviceName = serviceName

    def get_modeTransport(self):
        return self.modeTransport

    def set_modeTransport(self, modeTransport):
        self.modeTransport = modeTransport

    def get_transitDays(self):
        return self.transitDays

    def set_transitDays(self, transitDays):
        self.transitDays = transitDays

    def get_baseCharge(self):
        return self.baseCharge

    def set_baseCharge(self, baseCharge):
        self.baseCharge = baseCharge

    def get_fuelSurcharge(self):
        return self.fuelSurcharge

    def set_fuelSurcharge(self, fuelSurcharge):
        self.fuelSurcharge = fuelSurcharge

    def get_totalCharge(self):
        return self.totalCharge

    def set_totalCharge(self, totalCharge):
        self.totalCharge = totalCharge

    def get_currency(self):
        return self.currency

    def set_currency(self, currency):
        self.currency = currency

    def _hasContent(self):
        if self.Surcharge:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="QuoteType",
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get("QuoteType")
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = "\n"
        else:
            eol_ = ""
        if self.original_tagname_ is not None and name_ == "QuoteType":
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ":"
        showIndent(outfile, level, pretty_print)
        outfile.write(
            "<%s%s%s"
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and " " + namespacedef_ or "",
            )
        )
        already_processed = set()
        self._exportAttributes(
            outfile, level, already_processed, namespaceprefix_, name_="QuoteType"
        )
        if self._hasContent():
            outfile.write(">%s" % (eol_,))
            self._exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_="QuoteType",
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write("</%s%s>%s" % (namespaceprefix_, name_, eol_))
        else:
            outfile.write("/>%s" % (eol_,))

    def _exportAttributes(
        self, outfile, level, already_processed, namespaceprefix_="", name_="QuoteType"
    ):
        if self.carrierId is not None and "carrierId" not in already_processed:
            already_processed.add("carrierId")
            outfile.write(
                ' carrierId="%s"'
                % self.gds_format_integer(self.carrierId, input_name="carrierId")
            )
        if self.carrierName is not None and "carrierName" not in already_processed:
            already_processed.add("carrierName")
            outfile.write(
                " carrierName=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.carrierName), input_name="carrierName"
                        )
                    ),
                )
            )
        if self.serviceId is not None and "serviceId" not in already_processed:
            already_processed.add("serviceId")
            outfile.write(
                ' serviceId="%s"'
                % self.gds_format_integer(self.serviceId, input_name="serviceId")
            )
        if self.serviceName is not None and "serviceName" not in already_processed:
            already_processed.add("serviceName")
            outfile.write(
                " serviceName=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.serviceName), input_name="serviceName"
                        )
                    ),
                )
            )
        if self.modeTransport is not None and "modeTransport" not in already_processed:
            already_processed.add("modeTransport")
            outfile.write(
                " modeTransport=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.modeTransport), input_name="modeTransport"
                        )
                    ),
                )
            )
        if self.transitDays is not None and "transitDays" not in already_processed:
            already_processed.add("transitDays")
            outfile.write(
                ' transitDays="%s"'
                % self.gds_format_integer(self.transitDays, input_name="transitDays")
            )
        if self.baseCharge is not None and "baseCharge" not in already_processed:
            already_processed.add("baseCharge")
            outfile.write(
                ' baseCharge="%s"'
                % self.gds_format_float(self.baseCharge, input_name="baseCharge")
            )
        if self.fuelSurcharge is not None and "fuelSurcharge" not in already_processed:
            already_processed.add("fuelSurcharge")
            outfile.write(
                ' fuelSurcharge="%s"'
                % self.gds_format_float(self.fuelSurcharge, input_name="fuelSurcharge")
            )
        if self.totalCharge is not None and "totalCharge" not in already_processed:
            already_processed.add("totalCharge")
            outfile.write(
                ' totalCharge="%s"'
                % self.gds_format_float(self.totalCharge, input_name="totalCharge")
            )
        if self.currency is not None and "currency" not in already_processed:
            already_processed.add("currency")
            outfile.write(
                " currency=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.currency), input_name="currency"
                        )
                    ),
                )
            )

    def _exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="QuoteType",
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = "\n"
        else:
            eol_ = ""
        for Surcharge_ in self.Surcharge:
            namespaceprefix_ = (
                self.Surcharge_nsprefix_ + ":"
                if (UseCapturedNS_ and self.Surcharge_nsprefix_)
                else ""
            )
            Surcharge_.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_="",
                name_="Surcharge",
                pretty_print=pretty_print,
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_("carrierId", node)
        if value is not None and "carrierId" not in already_processed:
            already_processed.add("carrierId")
            self.carrierId = self.gds_parse_integer(value, node, "carrierId")
        value = find_attr_value_("carrierName", node)
        if value is not None and "carrierName" not in already_processed:
            already_processed.add("carrierName")
            self.carrierName = value
        value = find_attr_value_("serviceId", node)
        if value is not None and "serviceId" not in already_processed:
            already_processed.add("serviceId")
            self.serviceId = self.gds_parse_integer(value, node, "serviceId")
        value = find_attr_value_("serviceName", node)
        if value is not None and "serviceName" not in already_processed:
            already_processed.add("serviceName")
            self.serviceName = value
        value = find_attr_value_("modeTransport", node)
        if value is not None and "modeTransport" not in already_processed:
            already_processed.add("modeTransport")
            self.modeTransport = value
        value = find_attr_value_("transitDays", node)
        if value is not None and "transitDays" not in already_processed:
            already_processed.add("transitDays")
            self.transitDays = self.gds_parse_integer(value, node, "transitDays")
        value = find_attr_value_("baseCharge", node)
        if value is not None and "baseCharge" not in already_processed:
            already_processed.add("baseCharge")
            value = self.gds_parse_float(value, node, "baseCharge")
            self.baseCharge = value
        value = find_attr_value_("fuelSurcharge", node)
        if value is not None and "fuelSurcharge" not in already_processed:
            already_processed.add("fuelSurcharge")
            value = self.gds_parse_float(value, node, "fuelSurcharge")
            self.fuelSurcharge = value
        value = find_attr_value_("totalCharge", node)
        if value is not None and "totalCharge" not in already_processed:
            already_processed.add("totalCharge")
            value = self.gds_parse_float(value, node, "totalCharge")
            self.totalCharge = value
        value = find_attr_value_("currency", node)
        if value is not None and "currency" not in already_processed:
            already_processed.add("currency")
            self.currency = value

    def _buildChildren(
        self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None
    ):
        if nodeName_ == "Surcharge":
            obj_ = SurchargeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Surcharge.append(obj_)
            obj_.original_tagname_ = "Surcharge"


# end class QuoteType


class SurchargeType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self,
        id=None,
        name=None,
        amount=None,
        valueOf_=None,
        gds_collector_=None,
        **kwargs_
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get("parent_object_")
        self.ns_prefix_ = None
        self.id = _cast(None, id)
        self.id_nsprefix_ = None
        self.name = _cast(None, name)
        self.name_nsprefix_ = None
        self.amount = _cast(float, amount)
        self.amount_nsprefix_ = None
        self.valueOf_ = valueOf_

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, SurchargeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SurchargeType.subclass:
            return SurchargeType.subclass(*args_, **kwargs_)
        else:
            return SurchargeType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_amount(self):
        return self.amount

    def set_amount(self, amount):
        self.amount = amount

    def get_valueOf_(self):
        return self.valueOf_

    def set_valueOf_(self, valueOf_):
        self.valueOf_ = valueOf_

    def _hasContent(self):
        if 1 if type(self.valueOf_) in [int, float] else self.valueOf_:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="SurchargeType",
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get("SurchargeType")
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = "\n"
        else:
            eol_ = ""
        if self.original_tagname_ is not None and name_ == "SurchargeType":
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ":"
        showIndent(outfile, level, pretty_print)
        outfile.write(
            "<%s%s%s"
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and " " + namespacedef_ or "",
            )
        )
        already_processed = set()
        self._exportAttributes(
            outfile, level, already_processed, namespaceprefix_, name_="SurchargeType"
        )
        if self._hasContent():
            outfile.write(">")
            outfile.write(self.convert_unicode(self.valueOf_))
            self._exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_="SurchargeType",
                pretty_print=pretty_print,
            )
            outfile.write("</%s%s>%s" % (namespaceprefix_, name_, eol_))
        else:
            outfile.write("/>%s" % (eol_,))

    def _exportAttributes(
        self,
        outfile,
        level,
        already_processed,
        namespaceprefix_="",
        name_="SurchargeType",
    ):
        if self.id is not None and "id" not in already_processed:
            already_processed.add("id")
            outfile.write(
                " id=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(quote_attrib(self.id), input_name="id")
                    ),
                )
            )
        if self.name is not None and "name" not in already_processed:
            already_processed.add("name")
            outfile.write(
                " name=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.name), input_name="name"
                        )
                    ),
                )
            )
        if self.amount is not None and "amount" not in already_processed:
            already_processed.add("amount")
            outfile.write(
                ' amount="%s"' % self.gds_format_float(self.amount, input_name="amount")
            )

    def _exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="SurchargeType",
        fromsubclass_=False,
        pretty_print=True,
    ):
        pass

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_("id", node)
        if value is not None and "id" not in already_processed:
            already_processed.add("id")
            self.id = value
        value = find_attr_value_("name", node)
        if value is not None and "name" not in already_processed:
            already_processed.add("name")
            self.name = value
        value = find_attr_value_("amount", node)
        if value is not None and "amount" not in already_processed:
            already_processed.add("amount")
            value = self.gds_parse_float(value, node, "amount")
            self.amount = value

    def _buildChildren(
        self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None
    ):
        pass


# end class SurchargeType


class BillingAddressType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self,
        CompanyName=None,
        Address1=None,
        Address2=None,
        City=None,
        ProvinceCode=None,
        CountryCode=None,
        zip=None,
        PhoneNo=None,
        valueOf_=None,
        gds_collector_=None,
        **kwargs_
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get("parent_object_")
        self.ns_prefix_ = None
        self.CompanyName = _cast(None, CompanyName)
        self.CompanyName_nsprefix_ = None
        self.Address1 = _cast(None, Address1)
        self.Address1_nsprefix_ = None
        self.Address2 = _cast(None, Address2)
        self.Address2_nsprefix_ = None
        self.City = _cast(None, City)
        self.City_nsprefix_ = None
        self.ProvinceCode = _cast(None, ProvinceCode)
        self.ProvinceCode_nsprefix_ = None
        self.CountryCode = _cast(None, CountryCode)
        self.CountryCode_nsprefix_ = None
        self.zip = _cast(None, zip)
        self.zip_nsprefix_ = None
        self.PhoneNo = _cast(None, PhoneNo)
        self.PhoneNo_nsprefix_ = None
        self.valueOf_ = valueOf_

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, BillingAddressType
            )
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BillingAddressType.subclass:
            return BillingAddressType.subclass(*args_, **kwargs_)
        else:
            return BillingAddressType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_CompanyName(self):
        return self.CompanyName

    def set_CompanyName(self, CompanyName):
        self.CompanyName = CompanyName

    def get_Address1(self):
        return self.Address1

    def set_Address1(self, Address1):
        self.Address1 = Address1

    def get_Address2(self):
        return self.Address2

    def set_Address2(self, Address2):
        self.Address2 = Address2

    def get_City(self):
        return self.City

    def set_City(self, City):
        self.City = City

    def get_ProvinceCode(self):
        return self.ProvinceCode

    def set_ProvinceCode(self, ProvinceCode):
        self.ProvinceCode = ProvinceCode

    def get_CountryCode(self):
        return self.CountryCode

    def set_CountryCode(self, CountryCode):
        self.CountryCode = CountryCode

    def get_zip(self):
        return self.zip

    def set_zip(self, zip):
        self.zip = zip

    def get_PhoneNo(self):
        return self.PhoneNo

    def set_PhoneNo(self, PhoneNo):
        self.PhoneNo = PhoneNo

    def get_valueOf_(self):
        return self.valueOf_

    def set_valueOf_(self, valueOf_):
        self.valueOf_ = valueOf_

    def _hasContent(self):
        if 1 if type(self.valueOf_) in [int, float] else self.valueOf_:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="BillingAddressType",
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get("BillingAddressType")
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = "\n"
        else:
            eol_ = ""
        if self.original_tagname_ is not None and name_ == "BillingAddressType":
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ":"
        showIndent(outfile, level, pretty_print)
        outfile.write(
            "<%s%s%s"
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and " " + namespacedef_ or "",
            )
        )
        already_processed = set()
        self._exportAttributes(
            outfile,
            level,
            already_processed,
            namespaceprefix_,
            name_="BillingAddressType",
        )
        if self._hasContent():
            outfile.write(">")
            outfile.write(self.convert_unicode(self.valueOf_))
            self._exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_="BillingAddressType",
                pretty_print=pretty_print,
            )
            outfile.write("</%s%s>%s" % (namespaceprefix_, name_, eol_))
        else:
            outfile.write("/>%s" % (eol_,))

    def _exportAttributes(
        self,
        outfile,
        level,
        already_processed,
        namespaceprefix_="",
        name_="BillingAddressType",
    ):
        if self.CompanyName is not None and "CompanyName" not in already_processed:
            already_processed.add("CompanyName")
            outfile.write(
                " CompanyName=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.CompanyName), input_name="CompanyName"
                        )
                    ),
                )
            )
        if self.Address1 is not None and "Address1" not in already_processed:
            already_processed.add("Address1")
            outfile.write(
                " Address1=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.Address1), input_name="Address1"
                        )
                    ),
                )
            )
        if self.Address2 is not None and "Address2" not in already_processed:
            already_processed.add("Address2")
            outfile.write(
                " Address2=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.Address2), input_name="Address2"
                        )
                    ),
                )
            )
        if self.City is not None and "City" not in already_processed:
            already_processed.add("City")
            outfile.write(
                " City=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.City), input_name="City"
                        )
                    ),
                )
            )
        if self.ProvinceCode is not None and "ProvinceCode" not in already_processed:
            already_processed.add("ProvinceCode")
            outfile.write(
                " ProvinceCode=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.ProvinceCode), input_name="ProvinceCode"
                        )
                    ),
                )
            )
        if self.CountryCode is not None and "CountryCode" not in already_processed:
            already_processed.add("CountryCode")
            outfile.write(
                " CountryCode=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.CountryCode), input_name="CountryCode"
                        )
                    ),
                )
            )
        if self.zip is not None and "zip" not in already_processed:
            already_processed.add("zip")
            outfile.write(
                " zip=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(quote_attrib(self.zip), input_name="zip")
                    ),
                )
            )
        if self.PhoneNo is not None and "PhoneNo" not in already_processed:
            already_processed.add("PhoneNo")
            outfile.write(
                " PhoneNo=%s"
                % (
                    self.gds_encode(
                        self.gds_format_string(
                            quote_attrib(self.PhoneNo), input_name="PhoneNo"
                        )
                    ),
                )
            )

    def _exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_="",
        namespacedef_="",
        name_="BillingAddressType",
        fromsubclass_=False,
        pretty_print=True,
    ):
        pass

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_("CompanyName", node)
        if value is not None and "CompanyName" not in already_processed:
            already_processed.add("CompanyName")
            self.CompanyName = value
        value = find_attr_value_("Address1", node)
        if value is not None and "Address1" not in already_processed:
            already_processed.add("Address1")
            self.Address1 = value
        value = find_attr_value_("Address2", node)
        if value is not None and "Address2" not in already_processed:
            already_processed.add("Address2")
            self.Address2 = value
        value = find_attr_value_("City", node)
        if value is not None and "City" not in already_processed:
            already_processed.add("City")
            self.City = value
        value = find_attr_value_("ProvinceCode", node)
        if value is not None and "ProvinceCode" not in already_processed:
            already_processed.add("ProvinceCode")
            self.ProvinceCode = value
        value = find_attr_value_("CountryCode", node)
        if value is not None and "CountryCode" not in already_processed:
            already_processed.add("CountryCode")
            self.CountryCode = value
        value = find_attr_value_("zip", node)
        if value is not None and "zip" not in already_processed:
            already_processed.add("zip")
            self.zip = value
        value = find_attr_value_("PhoneNo", node)
        if value is not None and "PhoneNo" not in already_processed:
            already_processed.add("PhoneNo")
            self.PhoneNo = value

    def _buildChildren(
        self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None
    ):
        pass


# end class BillingAddressType


GDSClassesMapping = {}


USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def get_root_tag(node):
    tag = Tag_pattern_.match(node.tag).groups()[-1]
    prefix_tag = TagNamePrefix + tag
    rootClass = GDSClassesMapping.get(prefix_tag)
    if rootClass is None:
        rootClass = globals().get(prefix_tag)
    return tag, rootClass


def get_required_ns_prefix_defs(rootNode):
    """Get all name space prefix definitions required in this XML doc.
    Return a dictionary of definitions and a char string of definitions.
    """
    nsmap = {
        prefix: uri
        for node in rootNode.iter()
        for (prefix, uri) in node.nsmap.items()
        if prefix is not None
    }
    namespacedefs = " ".join(
        ['xmlns:{}="{}"'.format(prefix, uri) for prefix, uri in nsmap.items()]
    )
    return nsmap, namespacedefs


def parse(inFileName, silence=False, print_warnings=True):
    global CapturedNsmap_
    gds_collector = GdsCollector_()
    parser = None
    doc = parsexml_(inFileName, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = "Freightcom"
        rootClass = Freightcom
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    CapturedNsmap_, namespacedefs = get_required_ns_prefix_defs(rootNode)
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag, namespacedef_=namespacedefs, pretty_print=True
        )
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ("-" * 50) + "\n"
        sys.stderr.write(separator)
        sys.stderr.write(
            "----- Warnings -- count: {} -----\n".format(
                len(gds_collector.get_messages()),
            )
        )
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def parseEtree(
    inFileName,
    silence=False,
    print_warnings=True,
    mapping=None,
    reverse_mapping=None,
    nsmap=None,
):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = "Freightcom"
        rootClass = Freightcom
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if mapping is None:
        mapping = {}
    if reverse_mapping is None:
        reverse_mapping = {}
    rootElement = rootObj.to_etree(
        None,
        name_=rootTag,
        mapping_=mapping,
        reverse_mapping_=reverse_mapping,
        nsmap_=nsmap,
    )
    reverse_node_mapping = rootObj.gds_reverse_node_mapping(mapping)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True, xml_declaration=True, encoding="utf-8"
        )
        sys.stdout.write(str(content))
        sys.stdout.write("\n")
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ("-" * 50) + "\n"
        sys.stderr.write(separator)
        sys.stderr.write(
            "----- Warnings -- count: {} -----\n".format(
                len(gds_collector.get_messages()),
            )
        )
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj, rootElement, mapping, reverse_node_mapping


def parseString(inString, silence=False, print_warnings=True):
    """Parse a string, create the object tree, and export it.

    Arguments:
    - inString -- A string.  This XML fragment should not start
      with an XML declaration containing an encoding.
    - silence -- A boolean.  If False, export the object.
    Returns -- The root object in the tree.
    """
    parser = None
    rootNode = parsexmlstring_(inString, parser)
    gds_collector = GdsCollector_()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = "Freightcom"
        rootClass = Freightcom
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(sys.stdout, 0, name_=rootTag, namespacedef_="")
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ("-" * 50) + "\n"
        sys.stderr.write(separator)
        sys.stderr.write(
            "----- Warnings -- count: {} -----\n".format(
                len(gds_collector.get_messages()),
            )
        )
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def parseLiteral(inFileName, silence=False, print_warnings=True):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = "Freightcom"
        rootClass = Freightcom
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write("#from shipping_reply import *\n\n")
        sys.stdout.write("import shipping_reply as model_\n\n")
        sys.stdout.write("rootObj = model_.rootClass(\n")
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(")\n")
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ("-" * 50) + "\n"
        sys.stderr.write(separator)
        sys.stderr.write(
            "----- Warnings -- count: {} -----\n".format(
                len(gds_collector.get_messages()),
            )
        )
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        parse(args[0])
    else:
        usage()


if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    main()

RenameMappings_ = {}

#
# Mapping of namespaces to types defined in them
# and the file in which each is defined.
# simpleTypes are marked "ST" and complexTypes "CT".
NamespaceToDefMappings_ = {"http://www.freightcom.net/XMLSchema": []}

__all__ = [
    "BillingAddressType",
    "CarrierType",
    "Freightcom",
    "LabelDataType",
    "LabelType",
    "OrderType",
    "PackageType",
    "PickupType",
    "QuoteType",
    "ReferenceType",
    "ShippingReplyType",
    "SurchargeType",
]
