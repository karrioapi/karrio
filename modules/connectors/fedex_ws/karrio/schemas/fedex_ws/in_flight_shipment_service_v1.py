#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Thu May  6 11:00:03 2021 by generateDS.py version 2.38.6.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './fedex_lib/in_flight_shipment_service_v1.py')
#
# Command line arguments:
#   /Users/danielkobina/Workspace/Carriers Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./fedex_lib/in_flight_shipment_service_v1.py" /Users/danielkobina/Workspace/Carriers Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd
#
# Current working directory (os.getcwd()):
#   fedex
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
try:
    from lxml import etree as etree_
except ModulenotfoundExp_ :
    from xml.etree import ElementTree as etree_


Validate_simpletypes_ = True
SaveElementTreeNode = True
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
# "xsi:type" attribute value.  See the exportAttributes method of
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
except ModulenotfoundExp_ :
    GenerateDSNamespaceDefs_ = {}
try:
    from generatedsnamespaces import GenerateDSNamespaceTypePrefixes as GenerateDSNamespaceTypePrefixes_
except ModulenotfoundExp_ :
    GenerateDSNamespaceTypePrefixes_ = {}

#
# You can replace the following class definition by defining an
# importable module named "generatedscollector" containing a class
# named "GdsCollector".  See the default class definition below for
# clues about the possible content of that class.
#
try:
    from generatedscollector import GdsCollector as GdsCollector_
except ModulenotfoundExp_ :

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
except ModulenotfoundExp_ :
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
    
    class GeneratedsSuper(object):
        __hash__ = object.__hash__
        tzoff_pattern = re_.compile(r'(\+|-)((0\d|1[0-3]):[0-5]\d|14:00)$')
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
        def gds_format_string(self, input_data, input_name=''):
            return input_data
        def gds_parse_string(self, input_data, node=None, input_name=''):
            return input_data
        def gds_validate_string(self, input_data, node=None, input_name=''):
            if not input_data:
                return ''
            else:
                return input_data
        def gds_format_base64(self, input_data, input_name=''):
            return base64.b64encode(input_data)
        def gds_validate_base64(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_integer(self, input_data, input_name=''):
            return '%d' % input_data
        def gds_parse_integer(self, input_data, node=None, input_name=''):
            try:
                ival = int(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires integer value: %s' % exp)
            return ival
        def gds_validate_integer(self, input_data, node=None, input_name=''):
            try:
                value = int(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires integer value')
            return value
        def gds_format_integer_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)
        def gds_validate_integer_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    int(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of integer values')
            return values
        def gds_format_float(self, input_data, input_name=''):
            return ('%.15f' % input_data).rstrip('0')
        def gds_parse_float(self, input_data, node=None, input_name=''):
            try:
                fval_ = float(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires float or double value: %s' % exp)
            return fval_
        def gds_validate_float(self, input_data, node=None, input_name=''):
            try:
                value = float(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires float value')
            return value
        def gds_format_float_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)
        def gds_validate_float_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of float values')
            return values
        def gds_format_decimal(self, input_data, input_name=''):
            return_value = '%s' % input_data
            if '.' in return_value:
                return_value = return_value.rstrip('0')
                if return_value.endswith('.'):
                    return_value = return_value.rstrip('.')
            return return_value
        def gds_parse_decimal(self, input_data, node=None, input_name=''):
            try:
                decimal_value = decimal_.Decimal(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires decimal value')
            return decimal_value
        def gds_validate_decimal(self, input_data, node=None, input_name=''):
            try:
                value = decimal_.Decimal(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires decimal value')
            return value
        def gds_format_decimal_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return ' '.join([self.gds_format_decimal(item) for item in input_data])
        def gds_validate_decimal_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    decimal_.Decimal(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of decimal values')
            return values
        def gds_format_double(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_parse_double(self, input_data, node=None, input_name=''):
            try:
                fval_ = float(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires double or float value: %s' % exp)
            return fval_
        def gds_validate_double(self, input_data, node=None, input_name=''):
            try:
                value = float(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires double or float value')
            return value
        def gds_format_double_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)
        def gds_validate_double_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise_parse_error(
                        node, 'Requires sequence of double or float values')
            return values
        def gds_format_boolean(self, input_data, input_name=''):
            return ('%s' % input_data).lower()
        def gds_parse_boolean(self, input_data, node=None, input_name=''):
            if input_data in ('true', '1'):
                bval = True
            elif input_data in ('false', '0'):
                bval = False
            else:
                raise_parse_error(node, 'Requires boolean value')
            return bval
        def gds_validate_boolean(self, input_data, node=None, input_name=''):
            if input_data not in (True, 1, False, 0, ):
                raise_parse_error(
                    node,
                    'Requires boolean value '
                    '(one of True, 1, False, 0)')
            return input_data
        def gds_format_boolean_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)
        def gds_validate_boolean_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                value = self.gds_parse_boolean(value, node, input_name)
                if value not in (True, 1, False, 0, ):
                    raise_parse_error(
                        node,
                        'Requires sequence of boolean values '
                        '(one of True, 1, False, 0)')
            return values
        def gds_validate_datetime(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_datetime(self, input_data, input_name=''):
            if input_data.microsecond == 0:
                _svalue = '%04d-%02d-%02dT%02d:%02d:%02d' % (
                    input_data.year,
                    input_data.month,
                    input_data.day,
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                )
            else:
                _svalue = '%04d-%02d-%02dT%02d:%02d:%02d.%s' % (
                    input_data.year,
                    input_data.month,
                    input_data.day,
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                    ('%f' % (float(input_data.microsecond) / 1000000))[2:],
                )
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)
                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)
                    if total_seconds == 0:
                        _svalue += 'Z'
                    else:
                        if total_seconds < 0:
                            _svalue += '-'
                            total_seconds *= -1
                        else:
                            _svalue += '+'
                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
            return _svalue
        @classmethod
        def gds_parse_datetime(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            time_parts = input_data.split('.')
            if len(time_parts) > 1:
                micro_seconds = int(float('0.' + time_parts[1]) * 1000000)
                input_data = '%s.%s' % (
                    time_parts[0], "{}".format(micro_seconds).rjust(6, "0"), )
                dt = datetime_.datetime.strptime(
                    input_data, '%Y-%m-%dT%H:%M:%S.%f')
            else:
                dt = datetime_.datetime.strptime(
                    input_data, '%Y-%m-%dT%H:%M:%S')
            dt = dt.replace(tzinfo=tz)
            return dt
        def gds_validate_date(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_date(self, input_data, input_name=''):
            _svalue = '%04d-%02d-%02d' % (
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
                            _svalue += 'Z'
                        else:
                            if total_seconds < 0:
                                _svalue += '-'
                                total_seconds *= -1
                            else:
                                _svalue += '+'
                            hours = total_seconds // 3600
                            minutes = (total_seconds - (hours * 3600)) // 60
                            _svalue += '{0:02d}:{1:02d}'.format(
                                hours, minutes)
            except AttributeError:
                pass
            return _svalue
        @classmethod
        def gds_parse_date(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            dt = datetime_.datetime.strptime(input_data, '%Y-%m-%d')
            dt = dt.replace(tzinfo=tz)
            return dt.date()
        def gds_validate_time(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_time(self, input_data, input_name=''):
            if input_data.microsecond == 0:
                _svalue = '%02d:%02d:%02d' % (
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                )
            else:
                _svalue = '%02d:%02d:%02d.%s' % (
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                    ('%f' % (float(input_data.microsecond) / 1000000))[2:],
                )
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)
                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)
                    if total_seconds == 0:
                        _svalue += 'Z'
                    else:
                        if total_seconds < 0:
                            _svalue += '-'
                            total_seconds *= -1
                        else:
                            _svalue += '+'
                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
            return _svalue
        def gds_validate_simple_patterns(self, patterns, target):
            # pat is a list of lists of strings/patterns.
            # The target value must match at least one of the patterns
            # in order for the test to succeed.
            found1 = True
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
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            if len(input_data.split('.')) > 1:
                dt = datetime_.datetime.strptime(input_data, '%H:%M:%S.%f')
            else:
                dt = datetime_.datetime.strptime(input_data, '%H:%M:%S')
            dt = dt.replace(tzinfo=tz)
            return dt.time()
        def gds_check_cardinality_(
                self, value, input_name,
                min_occurs=0, max_occurs=1, required=None):
            if value is None:
                length = 0
            elif isinstance(value, list):
                length = len(value)
            else:
                length = 1
            if required is not None :
                if required and length < 1:
                    self.gds_collector_.add_message(
                        "Required value {}{} is missing".format(
                            input_name, self.gds_get_node_lineno_()))
            if length < min_occurs:
                self.gds_collector_.add_message(
                    "Number of values for {}{} is below "
                    "the minimum allowed, "
                    "expected at least {}, found {}".format(
                        input_name, self.gds_get_node_lineno_(),
                        min_occurs, length))
            elif length > max_occurs:
                self.gds_collector_.add_message(
                    "Number of values for {}{} is above "
                    "the maximum allowed, "
                    "expected at most {}, found {}".format(
                        input_name, self.gds_get_node_lineno_(),
                        max_occurs, length))
        def gds_validate_builtin_ST_(
                self, validator, value, input_name,
                min_occurs=None, max_occurs=None, required=None):
            if value is not None:
                try:
                    validator(value, input_name=input_name)
                except GDSParseError as parse_error:
                    self.gds_collector_.add_message(str(parse_error))
        def gds_validate_defined_ST_(
                self, validator, value, input_name,
                min_occurs=None, max_occurs=None, required=None):
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
            path = '/'.join(path_list)
            return path
        Tag_strip_pattern_ = re_.compile(r'\{.*\}')
        def get_path_list_(self, node, path_list):
            if node is None:
                return
            tag = GeneratedsSuper.Tag_strip_pattern_.sub('', node.tag)
            if tag:
                path_list.append(tag)
            self.get_path_list_(node.getparent(), path_list)
        def get_class_obj_(self, node, default_class=None):
            class_obj1 = default_class
            if 'xsi' in node.nsmap:
                classname = node.get('{%s}type' % node.nsmap['xsi'])
                if classname is not None:
                    names = classname.split(':')
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
                    encoding = 'utf-8'
                return instring.encode(encoding)
            else:
                return instring
        @staticmethod
        def convert_unicode(instring):
            if isinstance(instring, str):
                result = quote_xml(instring)
            elif sys.version_info.major == 2 and isinstance(instring, unicode):
                result = quote_xml(instring).encode('utf8')
            else:
                result = GeneratedsSuper.gds_encode(str(instring))
            return result
        def __eq__(self, other):
            def excl_select_objs_(obj):
                return (obj[0] != 'parent_object_' and
                        obj[0] != 'gds_collector_')
            if type(self) != type(other):
                return False
            return all(x == y for x, y in zip_longest(
                filter(excl_select_objs_, self.__dict__.items()),
                filter(excl_select_objs_, other.__dict__.items())))
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
            if (hasattr(self, "gds_elementtree_node_") and
                    self.gds_elementtree_node_ is not None):
                return ' near line {}'.format(
                    self.gds_elementtree_node_.sourceline)
            else:
                return ""
    
    
    def getSubclassFromModule_(module, class_):
        '''Get the subclass of a class from a specific module.'''
        name = class_.__name__ + 'Sub'
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

ExternalEncoding = ''
# Set this to false in order to deactivate during export, the use of
# name space prefixes captured from the input document.
UseCapturedNS_ = True
CapturedNsmap_ = {}
Tag_pattern_ = re_.compile(r'({.*})?(.*)')
String_cleanup_pat_ = re_.compile(r"[\n\r\s]+")
Namespace_extract_pat_ = re_.compile(r'{(.*)}(.*)')
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
            outfile.write('    ')


def quote_xml(inStr):
    "Escape markup chars, but do not modify CDATA sections."
    if not inStr:
        return ''
    s1 = (isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr)
    s2 = ''
    pos = 0
    matchobjects = CDATA_pattern_.finditer(s1)
    for mo in matchobjects:
        s3 = s1[pos:mo.start()]
        s2 += quote_xml_aux(s3)
        s2 += s1[mo.start():mo.end()]
        pos = mo.end()
    s3 = s1[pos:]
    s2 += quote_xml_aux(s3)
    return s2


def quote_xml_aux(inStr):
    s1 = inStr.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1


def quote_attrib(inStr):
    s1 = (isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
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
        if s1.find('\n') == -1:
            return "'%s'" % s1
        else:
            return "'''%s'''" % s1
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find('\n') == -1:
            return '"%s"' % s1
        else:
            return '"""%s"""' % s1


def get_all_text_(node):
    if node.text is not None:
        text = node.text
    else:
        text = ''
    for child in node:
        if child.tail is not None:
            text += child.tail
    return text


def find_attr_value_(attr_name, node):
    attrs = node.attrib
    attr_parts = attr_name.split(':')
    value = None
    if len(attr_parts) == 1:
        value = attrs.get(attr_name)
    elif len(attr_parts) == 2:
        prefix, name = attr_parts
        if prefix == 'xml':
            namespace = 'http://www.w3.org/XML/1998/namespace'
        else:
            namespace = node.nsmap.get(prefix)
        if namespace is not None:
            value = attrs.get('{%s}%s' % (namespace, name, ))
    return value


def encode_str_2_3(instr):
    return instr


class GDSParseError(Exception):
    pass


def raise_parse_error(node, msg):
    if node is not None:
        msg = '%s (element %s/line %d)' % (msg, node.tag, node.sourceline, )
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
    def export(self, outfile, level, name, namespace,
               pretty_print=True):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip():
                outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:    # category == MixedContainer.CategoryComplex
            self.value.export(
                outfile, level, namespace, name_=name,
                pretty_print=pretty_print)
    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write('<%s>%s</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeInteger or \
                self.content_type == MixedContainer.TypeBoolean:
            outfile.write('<%s>%d</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeFloat or \
                self.content_type == MixedContainer.TypeDecimal:
            outfile.write('<%s>%f</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeDouble:
            outfile.write('<%s>%g</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeBase64:
            outfile.write('<%s>%s</%s>' % (
                self.name,
                base64.b64encode(self.value),
                self.name))
    def to_etree(self, element, mapping_=None, nsmap_=None):
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
            subelement = etree_.SubElement(
                element, '%s' % self.name)
            subelement.text = self.to_etree_simple()
        else:    # category == MixedContainer.CategoryComplex
            self.value.to_etree(element)
    def to_etree_simple(self, mapping_=None, nsmap_=None):
        if self.content_type == MixedContainer.TypeString:
            text = self.value
        elif (self.content_type == MixedContainer.TypeInteger or
                self.content_type == MixedContainer.TypeBoolean):
            text = '%d' % self.value
        elif (self.content_type == MixedContainer.TypeFloat or
                self.content_type == MixedContainer.TypeDecimal):
            text = '%f' % self.value
        elif self.content_type == MixedContainer.TypeDouble:
            text = '%g' % self.value
        elif self.content_type == MixedContainer.TypeBase64:
            text = '%s' % base64.b64encode(self.value)
        return text
    def exportLiteral(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s", "%s"),\n' % (
                    self.category, self.content_type,
                    self.name, self.value))
        elif self.category == MixedContainer.CategorySimple:
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s", "%s"),\n' % (
                    self.category, self.content_type,
                    self.name, self.value))
        else:    # category == MixedContainer.CategoryComplex
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s",\n' % (
                    self.category, self.content_type, self.name,))
            self.value.exportLiteral(outfile, level + 1)
            showIndent(outfile, level)
            outfile.write(')\n')


class MemberSpec_(object):
    def __init__(self, name='', data_type='', container=0,
            optional=0, child_attrs=None, choice=None):
        self.name = name
        self.data_type = data_type
        self.container = container
        self.child_attrs = child_attrs
        self.choice = choice
        self.optional = optional
    def set_name(self, name): self.name = name
    def get_name(self): return self.name
    def set_data_type(self, data_type): self.data_type = data_type
    def get_data_type_chain(self): return self.data_type
    def get_data_type(self):
        if isinstance(self.data_type, list):
            if len(self.data_type) > 0:
                return self.data_type[-1]
            else:
                return 'xs:string'
        else:
            return self.data_type
    def set_container(self, container): self.container = container
    def get_container(self): return self.container
    def set_child_attrs(self, child_attrs): self.child_attrs = child_attrs
    def get_child_attrs(self): return self.child_attrs
    def set_choice(self, choice): self.choice = choice
    def get_choice(self): return self.choice
    def set_optional(self, optional): self.optional = optional
    def get_optional(self): return self.optional


def _cast(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)

#
# Data representation classes.
#


class AppointmentWindowType(str, Enum):
    """The description that FedEx uses for a given appointment window."""
    AFTERNOON='AFTERNOON'
    LATE_AFTERNOON='LATE_AFTERNOON'
    MID_DAY='MID_DAY'
    MORNING='MORNING'


class AssociatedAccountNumberType(str, Enum):
    """This enumeration represents a kind of "legacy" account number from a
    FedEx operating entity."""
    FEDEX_EXPRESS='FEDEX_EXPRESS'
    FEDEX_FREIGHT='FEDEX_FREIGHT'
    FEDEX_GROUND='FEDEX_GROUND'
    FEDEX_OFFICE='FEDEX_OFFICE'


class AutoConfigurationType(str, Enum):
    ENTERPRISE='ENTERPRISE'
    SHIPPING_SERVICE_PROVIDER='SHIPPING_SERVICE_PROVIDER'
    SOFTWARE_ONLY='SOFTWARE_ONLY'
    TRADITIONAL='TRADITIONAL'


class CreditCardAuthorizationType(str, Enum):
    AUTHORIZE_NON_ACCOUNT='AUTHORIZE_NON_ACCOUNT'
    AUTHORIZE_WITH_ACCOUNT='AUTHORIZE_WITH_ACCOUNT'
    VERIFY_WITH_ACCOUNT='VERIFY_WITH_ACCOUNT'


class CreditCardSettlementScheduleType(str, Enum):
    SETTLE_IMMEDIATELY='SETTLE_IMMEDIATELY'
    SETTLE_NEXT_DAY='SETTLE_NEXT_DAY'
    SETTLE_ON_DELIVERY='SETTLE_ON_DELIVERY'


class CreditCardTransactionAttributeType(str, Enum):
    ORIGINATED_BY_AUTHORIZED_PERSONNEL='ORIGINATED_BY_AUTHORIZED_PERSONNEL'
    ORIGINATED_BY_UNAUTHORIZED_PERSONNEL='ORIGINATED_BY_UNAUTHORIZED_PERSONNEL'


class CreditCardType(str, Enum):
    AMEX='AMEX'
    DANKORT='DANKORT'
    DINERS='DINERS'
    DISCOVER='DISCOVER'
    JCB='JCB'
    MASTERCARD='MASTERCARD'
    VISA='VISA'


class DeliveryActionType(str, Enum):
    """Specifies the actions that can be taken on a delivery option."""
    ADD='ADD'


class DeliveryOptionType(str, Enum):
    """Specifies the different option types for delivery."""
    REDIRECT_TO_HOLD_AT_LOCATION='REDIRECT_TO_HOLD_AT_LOCATION'


class DocumentFormatOptionType(str, Enum):
    SUPPRESS_ADDITIONAL_LANGUAGES='SUPPRESS_ADDITIONAL_LANGUAGES'


class EMailNotificationRecipientType(str, Enum):
    BROKER='BROKER'
    OTHER='OTHER'
    RECIPIENT='RECIPIENT'
    SHIPPER='SHIPPER'
    THIRD_PARTY='THIRD_PARTY'


class ExpressRegionCode(str, Enum):
    """Indicates a FedEx Express operating region."""
    APAC='APAC'
    CA='CA'
    EMEA='EMEA'
    LAC='LAC'
    US='US'


class LinearUnits(str, Enum):
    CM='CM'
    IN='IN'


class NotificationSeverityType(str, Enum):
    ERROR='ERROR'
    FAILURE='FAILURE'
    NOTE='NOTE'
    SUCCESS='SUCCESS'
    WARNING='WARNING'


class OperationalDocumentType(str, Enum):
    SIGNATURE_RELEASE_DOCUMENT='SIGNATURE_RELEASE_DOCUMENT'


class PaymentType(str, Enum):
    ACCOUNT='ACCOUNT'
    CASH='CASH'
    COLLECT='COLLECT'
    CREDIT_CARD='CREDIT_CARD'
    RECIPIENT='RECIPIENT'
    SENDER='SENDER'
    THIRD_PARTY='THIRD_PARTY'


class RerouteDeliveryType(str, Enum):
    """Specifies the different ways to reroute a shipment."""
    CROSS_COUNTRY_DEFERRED='CROSS_COUNTRY_DEFERRED'
    CROSS_COUNTRY_EXPEDITED='CROSS_COUNTRY_EXPEDITED'
    LOCAL='LOCAL'
    UNDETERMINED='UNDETERMINED'


class RescheduleDeliveryType(str, Enum):
    """Specifies the ways to reschedule the delivery of a shipment."""
    APPOINTMENT='APPOINTMENT'
    DATE_CERTAIN='DATE_CERTAIN'
    EVENING='EVENING'


class ShippingDocumentDispositionType(str, Enum):
    """Specifies how to return a shipping document to the caller."""
    CONFIRMED='CONFIRMED'
    DEFERRED_QUEUED='DEFERRED_QUEUED'
    DEFERRED_RETURNED='DEFERRED_RETURNED'
    DEFERRED_STORED='DEFERRED_STORED'
    EMAILED='EMAILED'
    QUEUED='QUEUED'
    RETURNED='RETURNED'
    STORED='STORED'


class ShippingDocumentEMailGroupingType(str, Enum):
    BY_RECIPIENT='BY_RECIPIENT'
    NONE='NONE'


class ShippingDocumentGroupingType(str, Enum):
    """Specifies how to organize all shipping documents of the same type."""
    CONSOLIDATED_BY_DOCUMENT_TYPE='CONSOLIDATED_BY_DOCUMENT_TYPE'
    CONSOLIDATED_BY_IMAGE_TYPE='CONSOLIDATED_BY_IMAGE_TYPE'
    INDIVIDUAL='INDIVIDUAL'


class ShippingDocumentImageType(str, Enum):
    """Specifies the image format used for a shipping document."""
    DIB='DIB'
    DOC='DOC'
    DPL='DPL'
    EPL_2='EPL2'
    GIF='GIF'
    PDF='PDF'
    PNG='PNG'
    RTF='RTF'
    TEXT='TEXT'
    ZPLII='ZPLII'


class ShippingDocumentNamingType(str, Enum):
    """Identifies the convention by which file names are constructed for STORED
    or DEFERRED documents."""
    FAST='FAST'
    LEGACY_FXRS='LEGACY_FXRS'


class ShippingDocumentStockType(str, Enum):
    """Specifies the type of paper (stock) on which a document will be
    printed."""
    OP__900_LG='OP_900_LG'
    OP__900_LG_B='OP_900_LG_B'
    OP__900_LL='OP_900_LL'
    OP__900_LL_B='OP_900_LL_B'
    OP__950='OP_950'
    PAPER__4_X_6='PAPER_4X6'
    PAPER__4_PER_PAGE_PORTRAIT='PAPER_4_PER_PAGE_PORTRAIT'
    PAPER_LETTER='PAPER_LETTER'
    STOCK__4_X_6='STOCK_4X6'
    STOCK__4_X_6_75_LEADING_DOC_TAB='STOCK_4X6.75_LEADING_DOC_TAB'
    STOCK__4_X_6_75_TRAILING_DOC_TAB='STOCK_4X6.75_TRAILING_DOC_TAB'
    STOCK__4_X_8='STOCK_4X8'
    STOCK__4_X_9_LEADING_DOC_TAB='STOCK_4X9_LEADING_DOC_TAB'
    STOCK__4_X_9_TRAILING_DOC_TAB='STOCK_4X9_TRAILING_DOC_TAB'


class SurchargeLevelType(str, Enum):
    PACKAGE='PACKAGE'
    SHIPMENT='SHIPMENT'


class SurchargeType(str, Enum):
    ADDITIONAL_HANDLING='ADDITIONAL_HANDLING'
    ANCILLARY_FEE='ANCILLARY_FEE'
    APPOINTMENT_DELIVERY='APPOINTMENT_DELIVERY'
    BLIND_SHIPMENT='BLIND_SHIPMENT'
    BROKER_SELECT_OPTION='BROKER_SELECT_OPTION'
    CANADIAN_DESTINATION='CANADIAN_DESTINATION'
    CHARGEABLE_PALLET_WEIGHT='CHARGEABLE_PALLET_WEIGHT'
    CLEARANCE_ENTRY_FEE='CLEARANCE_ENTRY_FEE'
    COD='COD'
    CUT_FLOWERS='CUT_FLOWERS'
    DANGEROUS_GOODS='DANGEROUS_GOODS'
    DELIVERY_AREA='DELIVERY_AREA'
    DELIVERY_CONFIRMATION='DELIVERY_CONFIRMATION'
    DELIVERY_ON_INVOICE_ACCEPTANCE='DELIVERY_ON_INVOICE_ACCEPTANCE'
    DETENTION='DETENTION'
    DOCUMENTATION_FEE='DOCUMENTATION_FEE'
    DRY_ICE='DRY_ICE'
    EMAIL_LABEL='EMAIL_LABEL'
    EUROPE_FIRST='EUROPE_FIRST'
    EXCESS_VALUE='EXCESS_VALUE'
    EXCLUSIVE_USE='EXCLUSIVE_USE'
    EXHIBITION='EXHIBITION'
    EXPEDITED='EXPEDITED'
    EXPORT='EXPORT'
    EXTRA_LABOR='EXTRA_LABOR'
    EXTRA_SURFACE_HANDLING_CHARGE='EXTRA_SURFACE_HANDLING_CHARGE'
    EXTREME_LENGTH='EXTREME_LENGTH'
    FEDEX_INTRACOUNTRY_FEES='FEDEX_INTRACOUNTRY_FEES'
    FEDEX_TAG='FEDEX_TAG'
    FICE='FICE'
    FLATBED='FLATBED'
    FREIGHT_GUARANTEE='FREIGHT_GUARANTEE'
    FREIGHT_ON_VALUE='FREIGHT_ON_VALUE'
    FREIGHT_TO_COLLECT='FREIGHT_TO_COLLECT'
    FUEL='FUEL'
    HOLD_AT_LOCATION='HOLD_AT_LOCATION'
    HOLIDAY_DELIVERY='HOLIDAY_DELIVERY'
    HOLIDAY_GUARANTEE='HOLIDAY_GUARANTEE'
    HOME_DELIVERY_APPOINTMENT='HOME_DELIVERY_APPOINTMENT'
    HOME_DELIVERY_DATE_CERTAIN='HOME_DELIVERY_DATE_CERTAIN'
    HOME_DELIVERY_EVENING='HOME_DELIVERY_EVENING'
    INSIDE_DELIVERY='INSIDE_DELIVERY'
    INSIDE_PICKUP='INSIDE_PICKUP'
    INSURED_VALUE='INSURED_VALUE'
    INTERHAWAII='INTERHAWAII'
    LIFTGATE_DELIVERY='LIFTGATE_DELIVERY'
    LIFTGATE_PICKUP='LIFTGATE_PICKUP'
    LIMITED_ACCESS_DELIVERY='LIMITED_ACCESS_DELIVERY'
    LIMITED_ACCESS_PICKUP='LIMITED_ACCESS_PICKUP'
    MARKING_OR_TAGGING='MARKING_OR_TAGGING'
    METRO_DELIVERY='METRO_DELIVERY'
    METRO_PICKUP='METRO_PICKUP'
    NON_BUSINESS_TIME='NON_BUSINESS_TIME'
    NON_MACHINABLE='NON_MACHINABLE'
    OFFSHORE='OFFSHORE'
    ON_CALL_PICKUP='ON_CALL_PICKUP'
    OTHER='OTHER'
    OUT_OF_DELIVERY_AREA='OUT_OF_DELIVERY_AREA'
    OUT_OF_PICKUP_AREA='OUT_OF_PICKUP_AREA'
    OVERSIZE='OVERSIZE'
    OVER_DIMENSION='OVER_DIMENSION'
    PALLETS_PROVIDED='PALLETS_PROVIDED'
    PALLET_SHRINKWRAP='PALLET_SHRINKWRAP'
    PERMIT='PERMIT'
    PIECE_COUNT_VERIFICATION='PIECE_COUNT_VERIFICATION'
    PORT='PORT'
    PRE_DELIVERY_NOTIFICATION='PRE_DELIVERY_NOTIFICATION'
    PRIORITY_ALERT='PRIORITY_ALERT'
    PROTECTION_FROM_FREEZING='PROTECTION_FROM_FREEZING'
    REGIONAL_MALL_DELIVERY='REGIONAL_MALL_DELIVERY'
    REGIONAL_MALL_PICKUP='REGIONAL_MALL_PICKUP'
    REROUTE='REROUTE'
    RESCHEDULE='RESCHEDULE'
    RESIDENTIAL_DELIVERY='RESIDENTIAL_DELIVERY'
    RESIDENTIAL_PICKUP='RESIDENTIAL_PICKUP'
    RETURN_LABEL='RETURN_LABEL'
    SATURDAY_DELIVERY='SATURDAY_DELIVERY'
    SATURDAY_PICKUP='SATURDAY_PICKUP'
    SHIPMENT_ASSEMBLY='SHIPMENT_ASSEMBLY'
    SIGNATURE_OPTION='SIGNATURE_OPTION'
    SORT_AND_SEGREGATE='SORT_AND_SEGREGATE'
    SPECIAL_DELIVERY='SPECIAL_DELIVERY'
    SPECIAL_EQUIPMENT='SPECIAL_EQUIPMENT'
    STORAGE='STORAGE'
    SUNDAY_DELIVERY='SUNDAY_DELIVERY'
    TARP='TARP'
    THIRD_PARTY_CONSIGNEE='THIRD_PARTY_CONSIGNEE'
    TRANSMART_SERVICE_FEE='TRANSMART_SERVICE_FEE'
    USPS='USPS'
    WEIGHING='WEIGHING'


class TinType(str, Enum):
    BUSINESS_NATIONAL='BUSINESS_NATIONAL'
    BUSINESS_STATE='BUSINESS_STATE'
    BUSINESS_UNION='BUSINESS_UNION'
    PERSONAL_NATIONAL='PERSONAL_NATIONAL'
    PERSONAL_STATE='PERSONAL_STATE'


class TrackingIdType(str, Enum):
    EXPRESS='EXPRESS'
    FEDEX='FEDEX'
    FREIGHT='FREIGHT'
    GROUND='GROUND'
    INTERNAL='INTERNAL'
    UNKNOWN='UNKNOWN'
    USPS='USPS'


class TransactionSourceFormat(str, Enum):
    API_CTS='API_CTS'
    API_XML='API_XML'
    DIRECT='DIRECT'
    DIRECT_XML='DIRECT_XML'
    FXRS_CTS='FXRS_CTS'
    UNKNOWN='UNKNOWN'
    WSI_XML='WSI_XML'


class TransitTimeType(str, Enum):
    EIGHTEEN_DAYS='EIGHTEEN_DAYS'
    EIGHT_DAYS='EIGHT_DAYS'
    ELEVEN_DAYS='ELEVEN_DAYS'
    FIFTEEN_DAYS='FIFTEEN_DAYS'
    FIVE_DAYS='FIVE_DAYS'
    FOURTEEN_DAYS='FOURTEEN_DAYS'
    FOUR_DAYS='FOUR_DAYS'
    NINETEEN_DAYS='NINETEEN_DAYS'
    NINE_DAYS='NINE_DAYS'
    ONE_DAY='ONE_DAY'
    SEVENTEEN_DAYS='SEVENTEEN_DAYS'
    SEVEN_DAYS='SEVEN_DAYS'
    SIXTEEN_DAYS='SIXTEEN_DAYS'
    SIX_DAYS='SIX_DAYS'
    TEN_DAYS='TEN_DAYS'
    THIRTEEN_DAYS='THIRTEEN_DAYS'
    THREE_DAYS='THREE_DAYS'
    TWELVE_DAYS='TWELVE_DAYS'
    TWENTY_DAYS='TWENTY_DAYS'
    TWO_DAYS='TWO_DAYS'
    UNKNOWN='UNKNOWN'


class WebServiceEnvironment(str, Enum):
    """Identifies the environment (level) for which an AuthenticationCredential
    is valid, and within which transactions are received."""
    PRODUCTION='PRODUCTION'
    TEST='TEST'


class Address(GeneratedsSuper):
    """Descriptive data for a physical location. May be used as an actual
    physical address (place to which one could go), or as a container of
    "address parts" which should be handled as a unit (such as a city-
    state-ZIP combination within the US)."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, StreetLines=None, City=None, StateOrProvinceCode=None, PostalCode=None, UrbanizationCode=None, CountryCode=None, CountryName=None, Residential=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if StreetLines is None:
            self.StreetLines = []
        else:
            self.StreetLines = StreetLines
        self.StreetLines_nsprefix_ = None
        self.City = City
        self.City_nsprefix_ = None
        self.StateOrProvinceCode = StateOrProvinceCode
        self.StateOrProvinceCode_nsprefix_ = None
        self.PostalCode = PostalCode
        self.PostalCode_nsprefix_ = None
        self.UrbanizationCode = UrbanizationCode
        self.UrbanizationCode_nsprefix_ = None
        self.CountryCode = CountryCode
        self.CountryCode_nsprefix_ = None
        self.CountryName = CountryName
        self.CountryName_nsprefix_ = None
        self.Residential = Residential
        self.Residential_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Address)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Address.subclass:
            return Address.subclass(*args_, **kwargs_)
        else:
            return Address(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_StreetLines(self):
        return self.StreetLines
    def set_StreetLines(self, StreetLines):
        self.StreetLines = StreetLines
    def add_StreetLines(self, value):
        self.StreetLines.append(value)
    def insert_StreetLines_at(self, index, value):
        self.StreetLines.insert(index, value)
    def replace_StreetLines_at(self, index, value):
        self.StreetLines[index] = value
    def get_City(self):
        return self.City
    def set_City(self, City):
        self.City = City
    def get_StateOrProvinceCode(self):
        return self.StateOrProvinceCode
    def set_StateOrProvinceCode(self, StateOrProvinceCode):
        self.StateOrProvinceCode = StateOrProvinceCode
    def get_PostalCode(self):
        return self.PostalCode
    def set_PostalCode(self, PostalCode):
        self.PostalCode = PostalCode
    def get_UrbanizationCode(self):
        return self.UrbanizationCode
    def set_UrbanizationCode(self, UrbanizationCode):
        self.UrbanizationCode = UrbanizationCode
    def get_CountryCode(self):
        return self.CountryCode
    def set_CountryCode(self, CountryCode):
        self.CountryCode = CountryCode
    def get_CountryName(self):
        return self.CountryName
    def set_CountryName(self, CountryName):
        self.CountryName = CountryName
    def get_Residential(self):
        return self.Residential
    def set_Residential(self, Residential):
        self.Residential = Residential
    def hasContent_(self):
        if (
            self.StreetLines or
            self.City is not None or
            self.StateOrProvinceCode is not None or
            self.PostalCode is not None or
            self.UrbanizationCode is not None or
            self.CountryCode is not None or
            self.CountryName is not None or
            self.Residential is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Address', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Address')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Address':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Address')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Address', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Address'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Address', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for StreetLines_ in self.StreetLines:
            namespaceprefix_ = self.StreetLines_nsprefix_ + ':' if (UseCapturedNS_ and self.StreetLines_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStreetLines>%s</%sStreetLines>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(StreetLines_), input_name='StreetLines')), namespaceprefix_ , eol_))
        if self.City is not None:
            namespaceprefix_ = self.City_nsprefix_ + ':' if (UseCapturedNS_ and self.City_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCity>%s</%sCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.City), input_name='City')), namespaceprefix_ , eol_))
        if self.StateOrProvinceCode is not None:
            namespaceprefix_ = self.StateOrProvinceCode_nsprefix_ + ':' if (UseCapturedNS_ and self.StateOrProvinceCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStateOrProvinceCode>%s</%sStateOrProvinceCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.StateOrProvinceCode), input_name='StateOrProvinceCode')), namespaceprefix_ , eol_))
        if self.PostalCode is not None:
            namespaceprefix_ = self.PostalCode_nsprefix_ + ':' if (UseCapturedNS_ and self.PostalCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPostalCode>%s</%sPostalCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PostalCode), input_name='PostalCode')), namespaceprefix_ , eol_))
        if self.UrbanizationCode is not None:
            namespaceprefix_ = self.UrbanizationCode_nsprefix_ + ':' if (UseCapturedNS_ and self.UrbanizationCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUrbanizationCode>%s</%sUrbanizationCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UrbanizationCode), input_name='UrbanizationCode')), namespaceprefix_ , eol_))
        if self.CountryCode is not None:
            namespaceprefix_ = self.CountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryCode>%s</%sCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryCode), input_name='CountryCode')), namespaceprefix_ , eol_))
        if self.CountryName is not None:
            namespaceprefix_ = self.CountryName_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryName>%s</%sCountryName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryName), input_name='CountryName')), namespaceprefix_ , eol_))
        if self.Residential is not None:
            namespaceprefix_ = self.Residential_nsprefix_ + ':' if (UseCapturedNS_ and self.Residential_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sResidential>%s</%sResidential>%s' % (namespaceprefix_ , self.gds_format_boolean(self.Residential, input_name='Residential'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'StreetLines':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'StreetLines')
            value_ = self.gds_validate_string(value_, node, 'StreetLines')
            self.StreetLines.append(value_)
            self.StreetLines_nsprefix_ = child_.prefix
        elif nodeName_ == 'City':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'City')
            value_ = self.gds_validate_string(value_, node, 'City')
            self.City = value_
            self.City_nsprefix_ = child_.prefix
        elif nodeName_ == 'StateOrProvinceCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'StateOrProvinceCode')
            value_ = self.gds_validate_string(value_, node, 'StateOrProvinceCode')
            self.StateOrProvinceCode = value_
            self.StateOrProvinceCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'PostalCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PostalCode')
            value_ = self.gds_validate_string(value_, node, 'PostalCode')
            self.PostalCode = value_
            self.PostalCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'UrbanizationCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UrbanizationCode')
            value_ = self.gds_validate_string(value_, node, 'UrbanizationCode')
            self.UrbanizationCode = value_
            self.UrbanizationCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'CountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryCode')
            value_ = self.gds_validate_string(value_, node, 'CountryCode')
            self.CountryCode = value_
            self.CountryCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'CountryName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryName')
            value_ = self.gds_validate_string(value_, node, 'CountryName')
            self.CountryName = value_
            self.CountryName_nsprefix_ = child_.prefix
        elif nodeName_ == 'Residential':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'Residential')
            ival_ = self.gds_validate_boolean(ival_, node, 'Residential')
            self.Residential = ival_
            self.Residential_nsprefix_ = child_.prefix
# end class Address


class AppointmentDetail(GeneratedsSuper):
    """Specifies the different appointment times on a specific date."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Date=None, WindowDetails=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if isinstance(Date, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Date, '%Y-%m-%d').date()
        else:
            initvalue_ = Date
        self.Date = initvalue_
        self.Date_nsprefix_ = None
        if WindowDetails is None:
            self.WindowDetails = []
        else:
            self.WindowDetails = WindowDetails
        self.WindowDetails_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AppointmentDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AppointmentDetail.subclass:
            return AppointmentDetail.subclass(*args_, **kwargs_)
        else:
            return AppointmentDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Date(self):
        return self.Date
    def set_Date(self, Date):
        self.Date = Date
    def get_WindowDetails(self):
        return self.WindowDetails
    def set_WindowDetails(self, WindowDetails):
        self.WindowDetails = WindowDetails
    def add_WindowDetails(self, value):
        self.WindowDetails.append(value)
    def insert_WindowDetails_at(self, index, value):
        self.WindowDetails.insert(index, value)
    def replace_WindowDetails_at(self, index, value):
        self.WindowDetails[index] = value
    def hasContent_(self):
        if (
            self.Date is not None or
            self.WindowDetails
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AppointmentDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AppointmentDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AppointmentDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AppointmentDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AppointmentDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AppointmentDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AppointmentDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Date is not None:
            namespaceprefix_ = self.Date_nsprefix_ + ':' if (UseCapturedNS_ and self.Date_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDate>%s</%sDate>%s' % (namespaceprefix_ , self.gds_format_date(self.Date, input_name='Date'), namespaceprefix_ , eol_))
        for WindowDetails_ in self.WindowDetails:
            namespaceprefix_ = self.WindowDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.WindowDetails_nsprefix_) else ''
            WindowDetails_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='WindowDetails', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Date':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.Date = dval_
            self.Date_nsprefix_ = child_.prefix
        elif nodeName_ == 'WindowDetails':
            obj_ = AppointmentTimeDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.WindowDetails.append(obj_)
            obj_.original_tagname_ = 'WindowDetails'
# end class AppointmentDetail


class AppointmentTimeDetail(GeneratedsSuper):
    """Specifies the details about the appointment time window."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Type=None, Window=None, Description=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Type = Type
        self.validate_AppointmentWindowType(self.Type)
        self.Type_nsprefix_ = "ns"
        self.Window = Window
        self.Window_nsprefix_ = "ns"
        self.Description = Description
        self.Description_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AppointmentTimeDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AppointmentTimeDetail.subclass:
            return AppointmentTimeDetail.subclass(*args_, **kwargs_)
        else:
            return AppointmentTimeDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_Window(self):
        return self.Window
    def set_Window(self, Window):
        self.Window = Window
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def validate_AppointmentWindowType(self, value):
        result = True
        # Validate type AppointmentWindowType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['AFTERNOON', 'LATE_AFTERNOON', 'MID_DAY', 'MORNING']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on AppointmentWindowType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Type is not None or
            self.Window is not None or
            self.Description is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AppointmentTimeDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AppointmentTimeDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AppointmentTimeDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AppointmentTimeDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AppointmentTimeDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AppointmentTimeDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AppointmentTimeDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sType>%s</%sType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Type), input_name='Type')), namespaceprefix_ , eol_))
        if self.Window is not None:
            namespaceprefix_ = self.Window_nsprefix_ + ':' if (UseCapturedNS_ and self.Window_nsprefix_) else ''
            self.Window.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Window', pretty_print=pretty_print)
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Type':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Type')
            value_ = self.gds_validate_string(value_, node, 'Type')
            self.Type = value_
            self.Type_nsprefix_ = child_.prefix
            # validate type AppointmentWindowType
            self.validate_AppointmentWindowType(self.Type)
        elif nodeName_ == 'Window':
            obj_ = LocalTimeRange.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Window = obj_
            obj_.original_tagname_ = 'Window'
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
# end class AppointmentTimeDetail


class AssociatedAccount(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Type=None, AccountNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Type = Type
        self.validate_AssociatedAccountNumberType(self.Type)
        self.Type_nsprefix_ = "ns"
        self.AccountNumber = AccountNumber
        self.AccountNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AssociatedAccount)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AssociatedAccount.subclass:
            return AssociatedAccount.subclass(*args_, **kwargs_)
        else:
            return AssociatedAccount(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_AccountNumber(self):
        return self.AccountNumber
    def set_AccountNumber(self, AccountNumber):
        self.AccountNumber = AccountNumber
    def validate_AssociatedAccountNumberType(self, value):
        result = True
        # Validate type AssociatedAccountNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FEDEX_EXPRESS', 'FEDEX_FREIGHT', 'FEDEX_GROUND', 'FEDEX_OFFICE']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on AssociatedAccountNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Type is not None or
            self.AccountNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AssociatedAccount', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AssociatedAccount')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AssociatedAccount':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AssociatedAccount')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AssociatedAccount', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AssociatedAccount'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AssociatedAccount', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sType>%s</%sType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Type), input_name='Type')), namespaceprefix_ , eol_))
        if self.AccountNumber is not None:
            namespaceprefix_ = self.AccountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.AccountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccountNumber>%s</%sAccountNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AccountNumber), input_name='AccountNumber')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Type':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Type')
            value_ = self.gds_validate_string(value_, node, 'Type')
            self.Type = value_
            self.Type_nsprefix_ = child_.prefix
            # validate type AssociatedAccountNumberType
            self.validate_AssociatedAccountNumberType(self.Type)
        elif nodeName_ == 'AccountNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AccountNumber')
            value_ = self.gds_validate_string(value_, node, 'AccountNumber')
            self.AccountNumber = value_
            self.AccountNumber_nsprefix_ = child_.prefix
# end class AssociatedAccount


class ClientDetail(GeneratedsSuper):
    """Descriptive data for the client submitting a transaction."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AccountNumber=None, GroundShipperNumber=None, MeterNumber=None, MasterMeterNumber=None, MeterInstance=None, CompanyId=None, SoftwareId=None, SoftwareRelease=None, ClientProductId=None, ClientProductVersion=None, MiddlewareProductId=None, MiddlewareProductVersion=None, IntegratorId=None, Region=None, AutoConfigurationType=None, CspCredentialKey=None, UserCredentialKey=None, InitiativeManifest=None, Localization=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.AccountNumber = AccountNumber
        self.AccountNumber_nsprefix_ = None
        self.GroundShipperNumber = GroundShipperNumber
        self.GroundShipperNumber_nsprefix_ = None
        self.MeterNumber = MeterNumber
        self.MeterNumber_nsprefix_ = None
        self.MasterMeterNumber = MasterMeterNumber
        self.MasterMeterNumber_nsprefix_ = None
        self.MeterInstance = MeterInstance
        self.MeterInstance_nsprefix_ = None
        self.CompanyId = CompanyId
        self.CompanyId_nsprefix_ = None
        self.SoftwareId = SoftwareId
        self.SoftwareId_nsprefix_ = None
        self.SoftwareRelease = SoftwareRelease
        self.SoftwareRelease_nsprefix_ = None
        self.ClientProductId = ClientProductId
        self.ClientProductId_nsprefix_ = None
        self.ClientProductVersion = ClientProductVersion
        self.ClientProductVersion_nsprefix_ = None
        self.MiddlewareProductId = MiddlewareProductId
        self.MiddlewareProductId_nsprefix_ = None
        self.MiddlewareProductVersion = MiddlewareProductVersion
        self.MiddlewareProductVersion_nsprefix_ = None
        self.IntegratorId = IntegratorId
        self.IntegratorId_nsprefix_ = None
        self.Region = Region
        self.validate_ExpressRegionCode(self.Region)
        self.Region_nsprefix_ = "ns"
        self.AutoConfigurationType = AutoConfigurationType
        self.validate_AutoConfigurationType(self.AutoConfigurationType)
        self.AutoConfigurationType_nsprefix_ = "ns"
        self.CspCredentialKey = CspCredentialKey
        self.CspCredentialKey_nsprefix_ = None
        self.UserCredentialKey = UserCredentialKey
        self.UserCredentialKey_nsprefix_ = None
        self.InitiativeManifest = InitiativeManifest
        self.InitiativeManifest_nsprefix_ = "ns"
        self.Localization = Localization
        self.Localization_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ClientDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ClientDetail.subclass:
            return ClientDetail.subclass(*args_, **kwargs_)
        else:
            return ClientDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AccountNumber(self):
        return self.AccountNumber
    def set_AccountNumber(self, AccountNumber):
        self.AccountNumber = AccountNumber
    def get_GroundShipperNumber(self):
        return self.GroundShipperNumber
    def set_GroundShipperNumber(self, GroundShipperNumber):
        self.GroundShipperNumber = GroundShipperNumber
    def get_MeterNumber(self):
        return self.MeterNumber
    def set_MeterNumber(self, MeterNumber):
        self.MeterNumber = MeterNumber
    def get_MasterMeterNumber(self):
        return self.MasterMeterNumber
    def set_MasterMeterNumber(self, MasterMeterNumber):
        self.MasterMeterNumber = MasterMeterNumber
    def get_MeterInstance(self):
        return self.MeterInstance
    def set_MeterInstance(self, MeterInstance):
        self.MeterInstance = MeterInstance
    def get_CompanyId(self):
        return self.CompanyId
    def set_CompanyId(self, CompanyId):
        self.CompanyId = CompanyId
    def get_SoftwareId(self):
        return self.SoftwareId
    def set_SoftwareId(self, SoftwareId):
        self.SoftwareId = SoftwareId
    def get_SoftwareRelease(self):
        return self.SoftwareRelease
    def set_SoftwareRelease(self, SoftwareRelease):
        self.SoftwareRelease = SoftwareRelease
    def get_ClientProductId(self):
        return self.ClientProductId
    def set_ClientProductId(self, ClientProductId):
        self.ClientProductId = ClientProductId
    def get_ClientProductVersion(self):
        return self.ClientProductVersion
    def set_ClientProductVersion(self, ClientProductVersion):
        self.ClientProductVersion = ClientProductVersion
    def get_MiddlewareProductId(self):
        return self.MiddlewareProductId
    def set_MiddlewareProductId(self, MiddlewareProductId):
        self.MiddlewareProductId = MiddlewareProductId
    def get_MiddlewareProductVersion(self):
        return self.MiddlewareProductVersion
    def set_MiddlewareProductVersion(self, MiddlewareProductVersion):
        self.MiddlewareProductVersion = MiddlewareProductVersion
    def get_IntegratorId(self):
        return self.IntegratorId
    def set_IntegratorId(self, IntegratorId):
        self.IntegratorId = IntegratorId
    def get_Region(self):
        return self.Region
    def set_Region(self, Region):
        self.Region = Region
    def get_AutoConfigurationType(self):
        return self.AutoConfigurationType
    def set_AutoConfigurationType(self, AutoConfigurationType):
        self.AutoConfigurationType = AutoConfigurationType
    def get_CspCredentialKey(self):
        return self.CspCredentialKey
    def set_CspCredentialKey(self, CspCredentialKey):
        self.CspCredentialKey = CspCredentialKey
    def get_UserCredentialKey(self):
        return self.UserCredentialKey
    def set_UserCredentialKey(self, UserCredentialKey):
        self.UserCredentialKey = UserCredentialKey
    def get_InitiativeManifest(self):
        return self.InitiativeManifest
    def set_InitiativeManifest(self, InitiativeManifest):
        self.InitiativeManifest = InitiativeManifest
    def get_Localization(self):
        return self.Localization
    def set_Localization(self, Localization):
        self.Localization = Localization
    def validate_ExpressRegionCode(self, value):
        result = True
        # Validate type ExpressRegionCode, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['APAC', 'CA', 'EMEA', 'LAC', 'US']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ExpressRegionCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_AutoConfigurationType(self, value):
        result = True
        # Validate type AutoConfigurationType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ENTERPRISE', 'SHIPPING_SERVICE_PROVIDER', 'SOFTWARE_ONLY', 'TRADITIONAL']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on AutoConfigurationType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.AccountNumber is not None or
            self.GroundShipperNumber is not None or
            self.MeterNumber is not None or
            self.MasterMeterNumber is not None or
            self.MeterInstance is not None or
            self.CompanyId is not None or
            self.SoftwareId is not None or
            self.SoftwareRelease is not None or
            self.ClientProductId is not None or
            self.ClientProductVersion is not None or
            self.MiddlewareProductId is not None or
            self.MiddlewareProductVersion is not None or
            self.IntegratorId is not None or
            self.Region is not None or
            self.AutoConfigurationType is not None or
            self.CspCredentialKey is not None or
            self.UserCredentialKey is not None or
            self.InitiativeManifest is not None or
            self.Localization is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ClientDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ClientDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ClientDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ClientDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ClientDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ClientDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ClientDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.AccountNumber is not None:
            namespaceprefix_ = self.AccountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.AccountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccountNumber>%s</%sAccountNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AccountNumber), input_name='AccountNumber')), namespaceprefix_ , eol_))
        if self.GroundShipperNumber is not None:
            namespaceprefix_ = self.GroundShipperNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.GroundShipperNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGroundShipperNumber>%s</%sGroundShipperNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GroundShipperNumber), input_name='GroundShipperNumber')), namespaceprefix_ , eol_))
        if self.MeterNumber is not None:
            namespaceprefix_ = self.MeterNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.MeterNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMeterNumber>%s</%sMeterNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MeterNumber), input_name='MeterNumber')), namespaceprefix_ , eol_))
        if self.MasterMeterNumber is not None:
            namespaceprefix_ = self.MasterMeterNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.MasterMeterNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMasterMeterNumber>%s</%sMasterMeterNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MasterMeterNumber), input_name='MasterMeterNumber')), namespaceprefix_ , eol_))
        if self.MeterInstance is not None:
            namespaceprefix_ = self.MeterInstance_nsprefix_ + ':' if (UseCapturedNS_ and self.MeterInstance_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMeterInstance>%s</%sMeterInstance>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MeterInstance), input_name='MeterInstance')), namespaceprefix_ , eol_))
        if self.CompanyId is not None:
            namespaceprefix_ = self.CompanyId_nsprefix_ + ':' if (UseCapturedNS_ and self.CompanyId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCompanyId>%s</%sCompanyId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CompanyId), input_name='CompanyId')), namespaceprefix_ , eol_))
        if self.SoftwareId is not None:
            namespaceprefix_ = self.SoftwareId_nsprefix_ + ':' if (UseCapturedNS_ and self.SoftwareId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSoftwareId>%s</%sSoftwareId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SoftwareId), input_name='SoftwareId')), namespaceprefix_ , eol_))
        if self.SoftwareRelease is not None:
            namespaceprefix_ = self.SoftwareRelease_nsprefix_ + ':' if (UseCapturedNS_ and self.SoftwareRelease_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSoftwareRelease>%s</%sSoftwareRelease>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SoftwareRelease), input_name='SoftwareRelease')), namespaceprefix_ , eol_))
        if self.ClientProductId is not None:
            namespaceprefix_ = self.ClientProductId_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientProductId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sClientProductId>%s</%sClientProductId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ClientProductId), input_name='ClientProductId')), namespaceprefix_ , eol_))
        if self.ClientProductVersion is not None:
            namespaceprefix_ = self.ClientProductVersion_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientProductVersion_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sClientProductVersion>%s</%sClientProductVersion>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ClientProductVersion), input_name='ClientProductVersion')), namespaceprefix_ , eol_))
        if self.MiddlewareProductId is not None:
            namespaceprefix_ = self.MiddlewareProductId_nsprefix_ + ':' if (UseCapturedNS_ and self.MiddlewareProductId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMiddlewareProductId>%s</%sMiddlewareProductId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MiddlewareProductId), input_name='MiddlewareProductId')), namespaceprefix_ , eol_))
        if self.MiddlewareProductVersion is not None:
            namespaceprefix_ = self.MiddlewareProductVersion_nsprefix_ + ':' if (UseCapturedNS_ and self.MiddlewareProductVersion_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMiddlewareProductVersion>%s</%sMiddlewareProductVersion>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MiddlewareProductVersion), input_name='MiddlewareProductVersion')), namespaceprefix_ , eol_))
        if self.IntegratorId is not None:
            namespaceprefix_ = self.IntegratorId_nsprefix_ + ':' if (UseCapturedNS_ and self.IntegratorId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIntegratorId>%s</%sIntegratorId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IntegratorId), input_name='IntegratorId')), namespaceprefix_ , eol_))
        if self.Region is not None:
            namespaceprefix_ = self.Region_nsprefix_ + ':' if (UseCapturedNS_ and self.Region_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRegion>%s</%sRegion>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Region), input_name='Region')), namespaceprefix_ , eol_))
        if self.AutoConfigurationType is not None:
            namespaceprefix_ = self.AutoConfigurationType_nsprefix_ + ':' if (UseCapturedNS_ and self.AutoConfigurationType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAutoConfigurationType>%s</%sAutoConfigurationType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AutoConfigurationType), input_name='AutoConfigurationType')), namespaceprefix_ , eol_))
        if self.CspCredentialKey is not None:
            namespaceprefix_ = self.CspCredentialKey_nsprefix_ + ':' if (UseCapturedNS_ and self.CspCredentialKey_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCspCredentialKey>%s</%sCspCredentialKey>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CspCredentialKey), input_name='CspCredentialKey')), namespaceprefix_ , eol_))
        if self.UserCredentialKey is not None:
            namespaceprefix_ = self.UserCredentialKey_nsprefix_ + ':' if (UseCapturedNS_ and self.UserCredentialKey_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUserCredentialKey>%s</%sUserCredentialKey>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UserCredentialKey), input_name='UserCredentialKey')), namespaceprefix_ , eol_))
        if self.InitiativeManifest is not None:
            namespaceprefix_ = self.InitiativeManifest_nsprefix_ + ':' if (UseCapturedNS_ and self.InitiativeManifest_nsprefix_) else ''
            self.InitiativeManifest.export(outfile, level, namespaceprefix_, namespacedef_='', name_='InitiativeManifest', pretty_print=pretty_print)
        if self.Localization is not None:
            namespaceprefix_ = self.Localization_nsprefix_ + ':' if (UseCapturedNS_ and self.Localization_nsprefix_) else ''
            self.Localization.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Localization', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'AccountNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AccountNumber')
            value_ = self.gds_validate_string(value_, node, 'AccountNumber')
            self.AccountNumber = value_
            self.AccountNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'GroundShipperNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GroundShipperNumber')
            value_ = self.gds_validate_string(value_, node, 'GroundShipperNumber')
            self.GroundShipperNumber = value_
            self.GroundShipperNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'MeterNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MeterNumber')
            value_ = self.gds_validate_string(value_, node, 'MeterNumber')
            self.MeterNumber = value_
            self.MeterNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'MasterMeterNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MasterMeterNumber')
            value_ = self.gds_validate_string(value_, node, 'MasterMeterNumber')
            self.MasterMeterNumber = value_
            self.MasterMeterNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'MeterInstance':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MeterInstance')
            value_ = self.gds_validate_string(value_, node, 'MeterInstance')
            self.MeterInstance = value_
            self.MeterInstance_nsprefix_ = child_.prefix
        elif nodeName_ == 'CompanyId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CompanyId')
            value_ = self.gds_validate_string(value_, node, 'CompanyId')
            self.CompanyId = value_
            self.CompanyId_nsprefix_ = child_.prefix
        elif nodeName_ == 'SoftwareId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SoftwareId')
            value_ = self.gds_validate_string(value_, node, 'SoftwareId')
            self.SoftwareId = value_
            self.SoftwareId_nsprefix_ = child_.prefix
        elif nodeName_ == 'SoftwareRelease':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SoftwareRelease')
            value_ = self.gds_validate_string(value_, node, 'SoftwareRelease')
            self.SoftwareRelease = value_
            self.SoftwareRelease_nsprefix_ = child_.prefix
        elif nodeName_ == 'ClientProductId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ClientProductId')
            value_ = self.gds_validate_string(value_, node, 'ClientProductId')
            self.ClientProductId = value_
            self.ClientProductId_nsprefix_ = child_.prefix
        elif nodeName_ == 'ClientProductVersion':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ClientProductVersion')
            value_ = self.gds_validate_string(value_, node, 'ClientProductVersion')
            self.ClientProductVersion = value_
            self.ClientProductVersion_nsprefix_ = child_.prefix
        elif nodeName_ == 'MiddlewareProductId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MiddlewareProductId')
            value_ = self.gds_validate_string(value_, node, 'MiddlewareProductId')
            self.MiddlewareProductId = value_
            self.MiddlewareProductId_nsprefix_ = child_.prefix
        elif nodeName_ == 'MiddlewareProductVersion':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MiddlewareProductVersion')
            value_ = self.gds_validate_string(value_, node, 'MiddlewareProductVersion')
            self.MiddlewareProductVersion = value_
            self.MiddlewareProductVersion_nsprefix_ = child_.prefix
        elif nodeName_ == 'IntegratorId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IntegratorId')
            value_ = self.gds_validate_string(value_, node, 'IntegratorId')
            self.IntegratorId = value_
            self.IntegratorId_nsprefix_ = child_.prefix
        elif nodeName_ == 'Region':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Region')
            value_ = self.gds_validate_string(value_, node, 'Region')
            self.Region = value_
            self.Region_nsprefix_ = child_.prefix
            # validate type ExpressRegionCode
            self.validate_ExpressRegionCode(self.Region)
        elif nodeName_ == 'AutoConfigurationType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AutoConfigurationType')
            value_ = self.gds_validate_string(value_, node, 'AutoConfigurationType')
            self.AutoConfigurationType = value_
            self.AutoConfigurationType_nsprefix_ = child_.prefix
            # validate type AutoConfigurationType
            self.validate_AutoConfigurationType(self.AutoConfigurationType)
        elif nodeName_ == 'CspCredentialKey':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CspCredentialKey')
            value_ = self.gds_validate_string(value_, node, 'CspCredentialKey')
            self.CspCredentialKey = value_
            self.CspCredentialKey_nsprefix_ = child_.prefix
        elif nodeName_ == 'UserCredentialKey':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UserCredentialKey')
            value_ = self.gds_validate_string(value_, node, 'UserCredentialKey')
            self.UserCredentialKey = value_
            self.UserCredentialKey_nsprefix_ = child_.prefix
        elif nodeName_ == 'InitiativeManifest':
            obj_ = InitiativeManifest.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.InitiativeManifest = obj_
            obj_.original_tagname_ = 'InitiativeManifest'
        elif nodeName_ == 'Localization':
            obj_ = Localization.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Localization = obj_
            obj_.original_tagname_ = 'Localization'
# end class ClientDetail


class Contact(GeneratedsSuper):
    """The descriptive data for a point-of-contact person."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ContactId=None, PersonName=None, Title=None, CompanyName=None, PhoneNumber=None, PhoneExtension=None, TollFreePhoneNumber=None, PagerNumber=None, FaxNumber=None, EMailAddress=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ContactId = ContactId
        self.ContactId_nsprefix_ = None
        self.PersonName = PersonName
        self.PersonName_nsprefix_ = None
        self.Title = Title
        self.Title_nsprefix_ = None
        self.CompanyName = CompanyName
        self.CompanyName_nsprefix_ = None
        self.PhoneNumber = PhoneNumber
        self.PhoneNumber_nsprefix_ = None
        self.PhoneExtension = PhoneExtension
        self.PhoneExtension_nsprefix_ = None
        self.TollFreePhoneNumber = TollFreePhoneNumber
        self.TollFreePhoneNumber_nsprefix_ = None
        self.PagerNumber = PagerNumber
        self.PagerNumber_nsprefix_ = None
        self.FaxNumber = FaxNumber
        self.FaxNumber_nsprefix_ = None
        self.EMailAddress = EMailAddress
        self.EMailAddress_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Contact)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Contact.subclass:
            return Contact.subclass(*args_, **kwargs_)
        else:
            return Contact(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ContactId(self):
        return self.ContactId
    def set_ContactId(self, ContactId):
        self.ContactId = ContactId
    def get_PersonName(self):
        return self.PersonName
    def set_PersonName(self, PersonName):
        self.PersonName = PersonName
    def get_Title(self):
        return self.Title
    def set_Title(self, Title):
        self.Title = Title
    def get_CompanyName(self):
        return self.CompanyName
    def set_CompanyName(self, CompanyName):
        self.CompanyName = CompanyName
    def get_PhoneNumber(self):
        return self.PhoneNumber
    def set_PhoneNumber(self, PhoneNumber):
        self.PhoneNumber = PhoneNumber
    def get_PhoneExtension(self):
        return self.PhoneExtension
    def set_PhoneExtension(self, PhoneExtension):
        self.PhoneExtension = PhoneExtension
    def get_TollFreePhoneNumber(self):
        return self.TollFreePhoneNumber
    def set_TollFreePhoneNumber(self, TollFreePhoneNumber):
        self.TollFreePhoneNumber = TollFreePhoneNumber
    def get_PagerNumber(self):
        return self.PagerNumber
    def set_PagerNumber(self, PagerNumber):
        self.PagerNumber = PagerNumber
    def get_FaxNumber(self):
        return self.FaxNumber
    def set_FaxNumber(self, FaxNumber):
        self.FaxNumber = FaxNumber
    def get_EMailAddress(self):
        return self.EMailAddress
    def set_EMailAddress(self, EMailAddress):
        self.EMailAddress = EMailAddress
    def hasContent_(self):
        if (
            self.ContactId is not None or
            self.PersonName is not None or
            self.Title is not None or
            self.CompanyName is not None or
            self.PhoneNumber is not None or
            self.PhoneExtension is not None or
            self.TollFreePhoneNumber is not None or
            self.PagerNumber is not None or
            self.FaxNumber is not None or
            self.EMailAddress is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Contact', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Contact')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Contact':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Contact')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Contact', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Contact'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Contact', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ContactId is not None:
            namespaceprefix_ = self.ContactId_nsprefix_ + ':' if (UseCapturedNS_ and self.ContactId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sContactId>%s</%sContactId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ContactId), input_name='ContactId')), namespaceprefix_ , eol_))
        if self.PersonName is not None:
            namespaceprefix_ = self.PersonName_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPersonName>%s</%sPersonName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PersonName), input_name='PersonName')), namespaceprefix_ , eol_))
        if self.Title is not None:
            namespaceprefix_ = self.Title_nsprefix_ + ':' if (UseCapturedNS_ and self.Title_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTitle>%s</%sTitle>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Title), input_name='Title')), namespaceprefix_ , eol_))
        if self.CompanyName is not None:
            namespaceprefix_ = self.CompanyName_nsprefix_ + ':' if (UseCapturedNS_ and self.CompanyName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCompanyName>%s</%sCompanyName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CompanyName), input_name='CompanyName')), namespaceprefix_ , eol_))
        if self.PhoneNumber is not None:
            namespaceprefix_ = self.PhoneNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.PhoneNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPhoneNumber>%s</%sPhoneNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PhoneNumber), input_name='PhoneNumber')), namespaceprefix_ , eol_))
        if self.PhoneExtension is not None:
            namespaceprefix_ = self.PhoneExtension_nsprefix_ + ':' if (UseCapturedNS_ and self.PhoneExtension_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPhoneExtension>%s</%sPhoneExtension>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PhoneExtension), input_name='PhoneExtension')), namespaceprefix_ , eol_))
        if self.TollFreePhoneNumber is not None:
            namespaceprefix_ = self.TollFreePhoneNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.TollFreePhoneNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTollFreePhoneNumber>%s</%sTollFreePhoneNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TollFreePhoneNumber), input_name='TollFreePhoneNumber')), namespaceprefix_ , eol_))
        if self.PagerNumber is not None:
            namespaceprefix_ = self.PagerNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.PagerNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPagerNumber>%s</%sPagerNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PagerNumber), input_name='PagerNumber')), namespaceprefix_ , eol_))
        if self.FaxNumber is not None:
            namespaceprefix_ = self.FaxNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.FaxNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFaxNumber>%s</%sFaxNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FaxNumber), input_name='FaxNumber')), namespaceprefix_ , eol_))
        if self.EMailAddress is not None:
            namespaceprefix_ = self.EMailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.EMailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEMailAddress>%s</%sEMailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EMailAddress), input_name='EMailAddress')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ContactId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ContactId')
            value_ = self.gds_validate_string(value_, node, 'ContactId')
            self.ContactId = value_
            self.ContactId_nsprefix_ = child_.prefix
        elif nodeName_ == 'PersonName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PersonName')
            value_ = self.gds_validate_string(value_, node, 'PersonName')
            self.PersonName = value_
            self.PersonName_nsprefix_ = child_.prefix
        elif nodeName_ == 'Title':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Title')
            value_ = self.gds_validate_string(value_, node, 'Title')
            self.Title = value_
            self.Title_nsprefix_ = child_.prefix
        elif nodeName_ == 'CompanyName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CompanyName')
            value_ = self.gds_validate_string(value_, node, 'CompanyName')
            self.CompanyName = value_
            self.CompanyName_nsprefix_ = child_.prefix
        elif nodeName_ == 'PhoneNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PhoneNumber')
            value_ = self.gds_validate_string(value_, node, 'PhoneNumber')
            self.PhoneNumber = value_
            self.PhoneNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'PhoneExtension':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PhoneExtension')
            value_ = self.gds_validate_string(value_, node, 'PhoneExtension')
            self.PhoneExtension = value_
            self.PhoneExtension_nsprefix_ = child_.prefix
        elif nodeName_ == 'TollFreePhoneNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TollFreePhoneNumber')
            value_ = self.gds_validate_string(value_, node, 'TollFreePhoneNumber')
            self.TollFreePhoneNumber = value_
            self.TollFreePhoneNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'PagerNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PagerNumber')
            value_ = self.gds_validate_string(value_, node, 'PagerNumber')
            self.PagerNumber = value_
            self.PagerNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'FaxNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FaxNumber')
            value_ = self.gds_validate_string(value_, node, 'FaxNumber')
            self.FaxNumber = value_
            self.FaxNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'EMailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EMailAddress')
            value_ = self.gds_validate_string(value_, node, 'EMailAddress')
            self.EMailAddress = value_
            self.EMailAddress_nsprefix_ = child_.prefix
# end class Contact


class ContactAndAddress(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Contact=None, Address=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Contact = Contact
        self.Contact_nsprefix_ = "ns"
        self.Address = Address
        self.Address_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ContactAndAddress)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ContactAndAddress.subclass:
            return ContactAndAddress.subclass(*args_, **kwargs_)
        else:
            return ContactAndAddress(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Contact(self):
        return self.Contact
    def set_Contact(self, Contact):
        self.Contact = Contact
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def hasContent_(self):
        if (
            self.Contact is not None or
            self.Address is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ContactAndAddress', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ContactAndAddress')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ContactAndAddress':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ContactAndAddress')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ContactAndAddress', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ContactAndAddress'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ContactAndAddress', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Contact is not None:
            namespaceprefix_ = self.Contact_nsprefix_ + ':' if (UseCapturedNS_ and self.Contact_nsprefix_) else ''
            self.Contact.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Contact', pretty_print=pretty_print)
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Contact':
            obj_ = Contact.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Contact = obj_
            obj_.original_tagname_ = 'Contact'
        elif nodeName_ == 'Address':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
# end class ContactAndAddress


class CreditCard(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Number=None, CreditCardType=None, ExpirationDate=None, LastAuthenticationByFedexDate=None, VerificationCode=None, CreditCardHolder=None, TrackData=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Number = Number
        self.Number_nsprefix_ = None
        self.CreditCardType = CreditCardType
        self.validate_CreditCardType(self.CreditCardType)
        self.CreditCardType_nsprefix_ = "ns"
        self.ExpirationDate = ExpirationDate
        self.ExpirationDate_nsprefix_ = None
        if isinstance(LastAuthenticationByFedexDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(LastAuthenticationByFedexDate, '%Y-%m-%d').date()
        else:
            initvalue_ = LastAuthenticationByFedexDate
        self.LastAuthenticationByFedexDate = initvalue_
        self.LastAuthenticationByFedexDate_nsprefix_ = None
        self.VerificationCode = VerificationCode
        self.VerificationCode_nsprefix_ = None
        self.CreditCardHolder = CreditCardHolder
        self.CreditCardHolder_nsprefix_ = "ns"
        if TrackData is None:
            self.TrackData = []
        else:
            self.TrackData = TrackData
        self.TrackData_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CreditCard)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CreditCard.subclass:
            return CreditCard.subclass(*args_, **kwargs_)
        else:
            return CreditCard(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Number(self):
        return self.Number
    def set_Number(self, Number):
        self.Number = Number
    def get_CreditCardType(self):
        return self.CreditCardType
    def set_CreditCardType(self, CreditCardType):
        self.CreditCardType = CreditCardType
    def get_ExpirationDate(self):
        return self.ExpirationDate
    def set_ExpirationDate(self, ExpirationDate):
        self.ExpirationDate = ExpirationDate
    def get_LastAuthenticationByFedexDate(self):
        return self.LastAuthenticationByFedexDate
    def set_LastAuthenticationByFedexDate(self, LastAuthenticationByFedexDate):
        self.LastAuthenticationByFedexDate = LastAuthenticationByFedexDate
    def get_VerificationCode(self):
        return self.VerificationCode
    def set_VerificationCode(self, VerificationCode):
        self.VerificationCode = VerificationCode
    def get_CreditCardHolder(self):
        return self.CreditCardHolder
    def set_CreditCardHolder(self, CreditCardHolder):
        self.CreditCardHolder = CreditCardHolder
    def get_TrackData(self):
        return self.TrackData
    def set_TrackData(self, TrackData):
        self.TrackData = TrackData
    def add_TrackData(self, value):
        self.TrackData.append(value)
    def insert_TrackData_at(self, index, value):
        self.TrackData.insert(index, value)
    def replace_TrackData_at(self, index, value):
        self.TrackData[index] = value
    def validate_CreditCardType(self, value):
        result = True
        # Validate type CreditCardType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['AMEX', 'DANKORT', 'DINERS', 'DISCOVER', 'JCB', 'MASTERCARD', 'VISA']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CreditCardType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Number is not None or
            self.CreditCardType is not None or
            self.ExpirationDate is not None or
            self.LastAuthenticationByFedexDate is not None or
            self.VerificationCode is not None or
            self.CreditCardHolder is not None or
            self.TrackData
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CreditCard', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CreditCard')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CreditCard':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CreditCard')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CreditCard', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CreditCard'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CreditCard', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Number is not None:
            namespaceprefix_ = self.Number_nsprefix_ + ':' if (UseCapturedNS_ and self.Number_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumber>%s</%sNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Number), input_name='Number')), namespaceprefix_ , eol_))
        if self.CreditCardType is not None:
            namespaceprefix_ = self.CreditCardType_nsprefix_ + ':' if (UseCapturedNS_ and self.CreditCardType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCreditCardType>%s</%sCreditCardType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CreditCardType), input_name='CreditCardType')), namespaceprefix_ , eol_))
        if self.ExpirationDate is not None:
            namespaceprefix_ = self.ExpirationDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ExpirationDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExpirationDate>%s</%sExpirationDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ExpirationDate), input_name='ExpirationDate')), namespaceprefix_ , eol_))
        if self.LastAuthenticationByFedexDate is not None:
            namespaceprefix_ = self.LastAuthenticationByFedexDate_nsprefix_ + ':' if (UseCapturedNS_ and self.LastAuthenticationByFedexDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLastAuthenticationByFedexDate>%s</%sLastAuthenticationByFedexDate>%s' % (namespaceprefix_ , self.gds_format_date(self.LastAuthenticationByFedexDate, input_name='LastAuthenticationByFedexDate'), namespaceprefix_ , eol_))
        if self.VerificationCode is not None:
            namespaceprefix_ = self.VerificationCode_nsprefix_ + ':' if (UseCapturedNS_ and self.VerificationCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sVerificationCode>%s</%sVerificationCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.VerificationCode), input_name='VerificationCode')), namespaceprefix_ , eol_))
        if self.CreditCardHolder is not None:
            namespaceprefix_ = self.CreditCardHolder_nsprefix_ + ':' if (UseCapturedNS_ and self.CreditCardHolder_nsprefix_) else ''
            self.CreditCardHolder.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CreditCardHolder', pretty_print=pretty_print)
        for TrackData_ in self.TrackData:
            namespaceprefix_ = self.TrackData_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackData_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTrackData>%s</%sTrackData>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(TrackData_), input_name='TrackData')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Number':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Number')
            value_ = self.gds_validate_string(value_, node, 'Number')
            self.Number = value_
            self.Number_nsprefix_ = child_.prefix
        elif nodeName_ == 'CreditCardType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CreditCardType')
            value_ = self.gds_validate_string(value_, node, 'CreditCardType')
            self.CreditCardType = value_
            self.CreditCardType_nsprefix_ = child_.prefix
            # validate type CreditCardType
            self.validate_CreditCardType(self.CreditCardType)
        elif nodeName_ == 'ExpirationDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ExpirationDate')
            value_ = self.gds_validate_string(value_, node, 'ExpirationDate')
            self.ExpirationDate = value_
            self.ExpirationDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'LastAuthenticationByFedexDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.LastAuthenticationByFedexDate = dval_
            self.LastAuthenticationByFedexDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'VerificationCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'VerificationCode')
            value_ = self.gds_validate_string(value_, node, 'VerificationCode')
            self.VerificationCode = value_
            self.VerificationCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'CreditCardHolder':
            obj_ = ParsedContactAndAddress.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CreditCardHolder = obj_
            obj_.original_tagname_ = 'CreditCardHolder'
        elif nodeName_ == 'TrackData':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TrackData')
            value_ = self.gds_validate_string(value_, node, 'TrackData')
            self.TrackData.append(value_)
            self.TrackData_nsprefix_ = child_.prefix
# end class CreditCard


class CreditCardTransactionAttributesDetail(GeneratedsSuper):
    """Specifies details about the credit card transaction that drive decisions
    about credit card processing."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Types=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Types is None:
            self.Types = []
        else:
            self.Types = Types
        self.Types_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CreditCardTransactionAttributesDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CreditCardTransactionAttributesDetail.subclass:
            return CreditCardTransactionAttributesDetail.subclass(*args_, **kwargs_)
        else:
            return CreditCardTransactionAttributesDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Types(self):
        return self.Types
    def set_Types(self, Types):
        self.Types = Types
    def add_Types(self, value):
        self.Types.append(value)
    def insert_Types_at(self, index, value):
        self.Types.insert(index, value)
    def replace_Types_at(self, index, value):
        self.Types[index] = value
    def validate_CreditCardTransactionAttributeType(self, value):
        result = True
        # Validate type CreditCardTransactionAttributeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ORIGINATED_BY_AUTHORIZED_PERSONNEL', 'ORIGINATED_BY_UNAUTHORIZED_PERSONNEL']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CreditCardTransactionAttributeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Types
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CreditCardTransactionAttributesDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CreditCardTransactionAttributesDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CreditCardTransactionAttributesDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CreditCardTransactionAttributesDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CreditCardTransactionAttributesDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CreditCardTransactionAttributesDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CreditCardTransactionAttributesDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Types_ in self.Types:
            namespaceprefix_ = self.Types_nsprefix_ + ':' if (UseCapturedNS_ and self.Types_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTypes>%s</%sTypes>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Types_), input_name='Types')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Types':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Types')
            value_ = self.gds_validate_string(value_, node, 'Types')
            self.Types.append(value_)
            self.Types_nsprefix_ = child_.prefix
            # validate type CreditCardTransactionAttributeType
            self.validate_CreditCardTransactionAttributeType(self.Types[-1])
# end class CreditCardTransactionAttributesDetail


class CreditCardTransactionDetail(GeneratedsSuper):
    """This class represents data tied to the use of a credit card in a
    specific transaction."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AuthorizationId=None, AuthorizationType=None, SettlementScheduleType=None, FraudDetectionDetail=None, PayorAuthenticationCode=None, AttributesDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.AuthorizationId = AuthorizationId
        self.AuthorizationId_nsprefix_ = None
        self.AuthorizationType = AuthorizationType
        self.validate_CreditCardAuthorizationType(self.AuthorizationType)
        self.AuthorizationType_nsprefix_ = "ns"
        self.SettlementScheduleType = SettlementScheduleType
        self.validate_CreditCardSettlementScheduleType(self.SettlementScheduleType)
        self.SettlementScheduleType_nsprefix_ = "ns"
        self.FraudDetectionDetail = FraudDetectionDetail
        self.FraudDetectionDetail_nsprefix_ = "ns"
        self.PayorAuthenticationCode = PayorAuthenticationCode
        self.PayorAuthenticationCode_nsprefix_ = None
        self.AttributesDetail = AttributesDetail
        self.AttributesDetail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CreditCardTransactionDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CreditCardTransactionDetail.subclass:
            return CreditCardTransactionDetail.subclass(*args_, **kwargs_)
        else:
            return CreditCardTransactionDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AuthorizationId(self):
        return self.AuthorizationId
    def set_AuthorizationId(self, AuthorizationId):
        self.AuthorizationId = AuthorizationId
    def get_AuthorizationType(self):
        return self.AuthorizationType
    def set_AuthorizationType(self, AuthorizationType):
        self.AuthorizationType = AuthorizationType
    def get_SettlementScheduleType(self):
        return self.SettlementScheduleType
    def set_SettlementScheduleType(self, SettlementScheduleType):
        self.SettlementScheduleType = SettlementScheduleType
    def get_FraudDetectionDetail(self):
        return self.FraudDetectionDetail
    def set_FraudDetectionDetail(self, FraudDetectionDetail):
        self.FraudDetectionDetail = FraudDetectionDetail
    def get_PayorAuthenticationCode(self):
        return self.PayorAuthenticationCode
    def set_PayorAuthenticationCode(self, PayorAuthenticationCode):
        self.PayorAuthenticationCode = PayorAuthenticationCode
    def get_AttributesDetail(self):
        return self.AttributesDetail
    def set_AttributesDetail(self, AttributesDetail):
        self.AttributesDetail = AttributesDetail
    def validate_CreditCardAuthorizationType(self, value):
        result = True
        # Validate type CreditCardAuthorizationType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['AUTHORIZE_NON_ACCOUNT', 'AUTHORIZE_WITH_ACCOUNT', 'VERIFY_WITH_ACCOUNT']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CreditCardAuthorizationType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CreditCardSettlementScheduleType(self, value):
        result = True
        # Validate type CreditCardSettlementScheduleType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['SETTLE_IMMEDIATELY', 'SETTLE_NEXT_DAY', 'SETTLE_ON_DELIVERY']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CreditCardSettlementScheduleType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.AuthorizationId is not None or
            self.AuthorizationType is not None or
            self.SettlementScheduleType is not None or
            self.FraudDetectionDetail is not None or
            self.PayorAuthenticationCode is not None or
            self.AttributesDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CreditCardTransactionDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CreditCardTransactionDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CreditCardTransactionDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CreditCardTransactionDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CreditCardTransactionDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CreditCardTransactionDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CreditCardTransactionDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.AuthorizationId is not None:
            namespaceprefix_ = self.AuthorizationId_nsprefix_ + ':' if (UseCapturedNS_ and self.AuthorizationId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAuthorizationId>%s</%sAuthorizationId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AuthorizationId), input_name='AuthorizationId')), namespaceprefix_ , eol_))
        if self.AuthorizationType is not None:
            namespaceprefix_ = self.AuthorizationType_nsprefix_ + ':' if (UseCapturedNS_ and self.AuthorizationType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAuthorizationType>%s</%sAuthorizationType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AuthorizationType), input_name='AuthorizationType')), namespaceprefix_ , eol_))
        if self.SettlementScheduleType is not None:
            namespaceprefix_ = self.SettlementScheduleType_nsprefix_ + ':' if (UseCapturedNS_ and self.SettlementScheduleType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSettlementScheduleType>%s</%sSettlementScheduleType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SettlementScheduleType), input_name='SettlementScheduleType')), namespaceprefix_ , eol_))
        if self.FraudDetectionDetail is not None:
            namespaceprefix_ = self.FraudDetectionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.FraudDetectionDetail_nsprefix_) else ''
            self.FraudDetectionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='FraudDetectionDetail', pretty_print=pretty_print)
        if self.PayorAuthenticationCode is not None:
            namespaceprefix_ = self.PayorAuthenticationCode_nsprefix_ + ':' if (UseCapturedNS_ and self.PayorAuthenticationCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPayorAuthenticationCode>%s</%sPayorAuthenticationCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PayorAuthenticationCode), input_name='PayorAuthenticationCode')), namespaceprefix_ , eol_))
        if self.AttributesDetail is not None:
            namespaceprefix_ = self.AttributesDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.AttributesDetail_nsprefix_) else ''
            self.AttributesDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AttributesDetail', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'AuthorizationId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AuthorizationId')
            value_ = self.gds_validate_string(value_, node, 'AuthorizationId')
            self.AuthorizationId = value_
            self.AuthorizationId_nsprefix_ = child_.prefix
        elif nodeName_ == 'AuthorizationType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AuthorizationType')
            value_ = self.gds_validate_string(value_, node, 'AuthorizationType')
            self.AuthorizationType = value_
            self.AuthorizationType_nsprefix_ = child_.prefix
            # validate type CreditCardAuthorizationType
            self.validate_CreditCardAuthorizationType(self.AuthorizationType)
        elif nodeName_ == 'SettlementScheduleType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SettlementScheduleType')
            value_ = self.gds_validate_string(value_, node, 'SettlementScheduleType')
            self.SettlementScheduleType = value_
            self.SettlementScheduleType_nsprefix_ = child_.prefix
            # validate type CreditCardSettlementScheduleType
            self.validate_CreditCardSettlementScheduleType(self.SettlementScheduleType)
        elif nodeName_ == 'FraudDetectionDetail':
            obj_ = CreditFraudDetectionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.FraudDetectionDetail = obj_
            obj_.original_tagname_ = 'FraudDetectionDetail'
        elif nodeName_ == 'PayorAuthenticationCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PayorAuthenticationCode')
            value_ = self.gds_validate_string(value_, node, 'PayorAuthenticationCode')
            self.PayorAuthenticationCode = value_
            self.PayorAuthenticationCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'AttributesDetail':
            obj_ = CreditCardTransactionAttributesDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AttributesDetail = obj_
            obj_.original_tagname_ = 'AttributesDetail'
# end class CreditCardTransactionDetail


class CreditFraudDetectionDetail(GeneratedsSuper):
    """This class is a rename of the previous VerifyCreditFraudDetail; the name
    change reflects the fact that it is no longer tied to a "verify"
    usage."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, IpAddress=None, ClientCookiesEnabled=None, DevicePrint=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.IpAddress = IpAddress
        self.IpAddress_nsprefix_ = None
        self.ClientCookiesEnabled = ClientCookiesEnabled
        self.ClientCookiesEnabled_nsprefix_ = None
        self.DevicePrint = DevicePrint
        self.DevicePrint_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CreditFraudDetectionDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CreditFraudDetectionDetail.subclass:
            return CreditFraudDetectionDetail.subclass(*args_, **kwargs_)
        else:
            return CreditFraudDetectionDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_IpAddress(self):
        return self.IpAddress
    def set_IpAddress(self, IpAddress):
        self.IpAddress = IpAddress
    def get_ClientCookiesEnabled(self):
        return self.ClientCookiesEnabled
    def set_ClientCookiesEnabled(self, ClientCookiesEnabled):
        self.ClientCookiesEnabled = ClientCookiesEnabled
    def get_DevicePrint(self):
        return self.DevicePrint
    def set_DevicePrint(self, DevicePrint):
        self.DevicePrint = DevicePrint
    def hasContent_(self):
        if (
            self.IpAddress is not None or
            self.ClientCookiesEnabled is not None or
            self.DevicePrint is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CreditFraudDetectionDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CreditFraudDetectionDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CreditFraudDetectionDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CreditFraudDetectionDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CreditFraudDetectionDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CreditFraudDetectionDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CreditFraudDetectionDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.IpAddress is not None:
            namespaceprefix_ = self.IpAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.IpAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIpAddress>%s</%sIpAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IpAddress), input_name='IpAddress')), namespaceprefix_ , eol_))
        if self.ClientCookiesEnabled is not None:
            namespaceprefix_ = self.ClientCookiesEnabled_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientCookiesEnabled_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sClientCookiesEnabled>%s</%sClientCookiesEnabled>%s' % (namespaceprefix_ , self.gds_format_boolean(self.ClientCookiesEnabled, input_name='ClientCookiesEnabled'), namespaceprefix_ , eol_))
        if self.DevicePrint is not None:
            namespaceprefix_ = self.DevicePrint_nsprefix_ + ':' if (UseCapturedNS_ and self.DevicePrint_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDevicePrint>%s</%sDevicePrint>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DevicePrint), input_name='DevicePrint')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'IpAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IpAddress')
            value_ = self.gds_validate_string(value_, node, 'IpAddress')
            self.IpAddress = value_
            self.IpAddress_nsprefix_ = child_.prefix
        elif nodeName_ == 'ClientCookiesEnabled':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'ClientCookiesEnabled')
            ival_ = self.gds_validate_boolean(ival_, node, 'ClientCookiesEnabled')
            self.ClientCookiesEnabled = ival_
            self.ClientCookiesEnabled_nsprefix_ = child_.prefix
        elif nodeName_ == 'DevicePrint':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DevicePrint')
            value_ = self.gds_validate_string(value_, node, 'DevicePrint')
            self.DevicePrint = value_
            self.DevicePrint_nsprefix_ = child_.prefix
# end class CreditFraudDetectionDetail


class DeliveryRequestDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Type=None, RedirectToHoldAtLocationDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Type = Type
        self.validate_DeliveryOptionType(self.Type)
        self.Type_nsprefix_ = "ns"
        self.RedirectToHoldAtLocationDetail = RedirectToHoldAtLocationDetail
        self.RedirectToHoldAtLocationDetail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DeliveryRequestDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DeliveryRequestDetail.subclass:
            return DeliveryRequestDetail.subclass(*args_, **kwargs_)
        else:
            return DeliveryRequestDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_RedirectToHoldAtLocationDetail(self):
        return self.RedirectToHoldAtLocationDetail
    def set_RedirectToHoldAtLocationDetail(self, RedirectToHoldAtLocationDetail):
        self.RedirectToHoldAtLocationDetail = RedirectToHoldAtLocationDetail
    def validate_DeliveryOptionType(self, value):
        result = True
        # Validate type DeliveryOptionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['REDIRECT_TO_HOLD_AT_LOCATION']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DeliveryOptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Type is not None or
            self.RedirectToHoldAtLocationDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeliveryRequestDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DeliveryRequestDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DeliveryRequestDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DeliveryRequestDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DeliveryRequestDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DeliveryRequestDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeliveryRequestDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sType>%s</%sType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Type), input_name='Type')), namespaceprefix_ , eol_))
        if self.RedirectToHoldAtLocationDetail is not None:
            namespaceprefix_ = self.RedirectToHoldAtLocationDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.RedirectToHoldAtLocationDetail_nsprefix_) else ''
            self.RedirectToHoldAtLocationDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='RedirectToHoldAtLocationDetail', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Type':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Type')
            value_ = self.gds_validate_string(value_, node, 'Type')
            self.Type = value_
            self.Type_nsprefix_ = child_.prefix
            # validate type DeliveryOptionType
            self.validate_DeliveryOptionType(self.Type)
        elif nodeName_ == 'RedirectToHoldAtLocationDetail':
            obj_ = RedirectToHoldAtLocationRequestDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.RedirectToHoldAtLocationDetail = obj_
            obj_.original_tagname_ = 'RedirectToHoldAtLocationDetail'
# end class DeliveryRequestDetail


class DocumentFormatOptionsRequested(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Options=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Options is None:
            self.Options = []
        else:
            self.Options = Options
        self.Options_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DocumentFormatOptionsRequested)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DocumentFormatOptionsRequested.subclass:
            return DocumentFormatOptionsRequested.subclass(*args_, **kwargs_)
        else:
            return DocumentFormatOptionsRequested(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Options(self):
        return self.Options
    def set_Options(self, Options):
        self.Options = Options
    def add_Options(self, value):
        self.Options.append(value)
    def insert_Options_at(self, index, value):
        self.Options.insert(index, value)
    def replace_Options_at(self, index, value):
        self.Options[index] = value
    def validate_DocumentFormatOptionType(self, value):
        result = True
        # Validate type DocumentFormatOptionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['SUPPRESS_ADDITIONAL_LANGUAGES']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DocumentFormatOptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Options
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DocumentFormatOptionsRequested', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DocumentFormatOptionsRequested')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DocumentFormatOptionsRequested':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DocumentFormatOptionsRequested')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DocumentFormatOptionsRequested', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DocumentFormatOptionsRequested'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DocumentFormatOptionsRequested', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Options_ in self.Options:
            namespaceprefix_ = self.Options_nsprefix_ + ':' if (UseCapturedNS_ and self.Options_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOptions>%s</%sOptions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Options_), input_name='Options')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Options':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Options')
            value_ = self.gds_validate_string(value_, node, 'Options')
            self.Options.append(value_)
            self.Options_nsprefix_ = child_.prefix
            # validate type DocumentFormatOptionType
            self.validate_DocumentFormatOptionType(self.Options[-1])
# end class DocumentFormatOptionsRequested


class InitiativeManifest(GeneratedsSuper):
    """Represents a transaction-specific set of initiative control data for all
    services."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Content=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Content is None:
            self.Content = []
        else:
            self.Content = Content
        self.Content_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, InitiativeManifest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if InitiativeManifest.subclass:
            return InitiativeManifest.subclass(*args_, **kwargs_)
        else:
            return InitiativeManifest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Content(self):
        return self.Content
    def set_Content(self, Content):
        self.Content = Content
    def add_Content(self, value):
        self.Content.append(value)
    def insert_Content_at(self, index, value):
        self.Content.insert(index, value)
    def replace_Content_at(self, index, value):
        self.Content[index] = value
    def hasContent_(self):
        if (
            self.Content
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='InitiativeManifest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('InitiativeManifest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'InitiativeManifest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='InitiativeManifest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='InitiativeManifest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='InitiativeManifest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='InitiativeManifest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Content_ in self.Content:
            namespaceprefix_ = self.Content_nsprefix_ + ':' if (UseCapturedNS_ and self.Content_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sContent>%s</%sContent>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Content_), input_name='Content')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Content':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Content')
            value_ = self.gds_validate_string(value_, node, 'Content')
            self.Content.append(value_)
            self.Content_nsprefix_ = child_.prefix
# end class InitiativeManifest


class LinearMeasure(GeneratedsSuper):
    """Represents a one-dimensional measurement in small units (e.g. suitable
    for measuring a package or document), contrasted with Distance, which
    represents a large one-dimensional measurement (e.g. distance between
    cities)."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Value=None, Units=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Value = Value
        self.Value_nsprefix_ = None
        self.Units = Units
        self.validate_LinearUnits(self.Units)
        self.Units_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LinearMeasure)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LinearMeasure.subclass:
            return LinearMeasure.subclass(*args_, **kwargs_)
        else:
            return LinearMeasure(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def get_Units(self):
        return self.Units
    def set_Units(self, Units):
        self.Units = Units
    def validate_LinearUnits(self, value):
        result = True
        # Validate type LinearUnits, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['CM', 'IN']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on LinearUnits' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Value is not None or
            self.Units is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LinearMeasure', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LinearMeasure')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LinearMeasure':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LinearMeasure')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LinearMeasure', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LinearMeasure'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LinearMeasure', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Value is not None:
            namespaceprefix_ = self.Value_nsprefix_ + ':' if (UseCapturedNS_ and self.Value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sValue>%s</%sValue>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Value, input_name='Value'), namespaceprefix_ , eol_))
        if self.Units is not None:
            namespaceprefix_ = self.Units_nsprefix_ + ':' if (UseCapturedNS_ and self.Units_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUnits>%s</%sUnits>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Units), input_name='Units')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Value' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Value')
            fval_ = self.gds_validate_decimal(fval_, node, 'Value')
            self.Value = fval_
            self.Value_nsprefix_ = child_.prefix
        elif nodeName_ == 'Units':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Units')
            value_ = self.gds_validate_string(value_, node, 'Units')
            self.Units = value_
            self.Units_nsprefix_ = child_.prefix
            # validate type LinearUnits
            self.validate_LinearUnits(self.Units)
# end class LinearMeasure


class LocalTimeRange(GeneratedsSuper):
    """Time Range specified in local time."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Begins=None, Ends=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Begins = Begins
        self.Begins_nsprefix_ = None
        self.Ends = Ends
        self.Ends_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LocalTimeRange)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LocalTimeRange.subclass:
            return LocalTimeRange.subclass(*args_, **kwargs_)
        else:
            return LocalTimeRange(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Begins(self):
        return self.Begins
    def set_Begins(self, Begins):
        self.Begins = Begins
    def get_Ends(self):
        return self.Ends
    def set_Ends(self, Ends):
        self.Ends = Ends
    def hasContent_(self):
        if (
            self.Begins is not None or
            self.Ends is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocalTimeRange', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LocalTimeRange')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LocalTimeRange':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LocalTimeRange')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LocalTimeRange', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LocalTimeRange'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocalTimeRange', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Begins is not None:
            namespaceprefix_ = self.Begins_nsprefix_ + ':' if (UseCapturedNS_ and self.Begins_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBegins>%s</%sBegins>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Begins), input_name='Begins')), namespaceprefix_ , eol_))
        if self.Ends is not None:
            namespaceprefix_ = self.Ends_nsprefix_ + ':' if (UseCapturedNS_ and self.Ends_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEnds>%s</%sEnds>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Ends), input_name='Ends')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Begins':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Begins')
            value_ = self.gds_validate_string(value_, node, 'Begins')
            self.Begins = value_
            self.Begins_nsprefix_ = child_.prefix
        elif nodeName_ == 'Ends':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Ends')
            value_ = self.gds_validate_string(value_, node, 'Ends')
            self.Ends = value_
            self.Ends_nsprefix_ = child_.prefix
# end class LocalTimeRange


class Localization(GeneratedsSuper):
    """Identifies the representation of human-readable text."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, LanguageCode=None, LocaleCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.LanguageCode = LanguageCode
        self.LanguageCode_nsprefix_ = None
        self.LocaleCode = LocaleCode
        self.LocaleCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Localization)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Localization.subclass:
            return Localization.subclass(*args_, **kwargs_)
        else:
            return Localization(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_LanguageCode(self):
        return self.LanguageCode
    def set_LanguageCode(self, LanguageCode):
        self.LanguageCode = LanguageCode
    def get_LocaleCode(self):
        return self.LocaleCode
    def set_LocaleCode(self, LocaleCode):
        self.LocaleCode = LocaleCode
    def hasContent_(self):
        if (
            self.LanguageCode is not None or
            self.LocaleCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Localization', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Localization')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Localization':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Localization')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Localization', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Localization'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Localization', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.LanguageCode is not None:
            namespaceprefix_ = self.LanguageCode_nsprefix_ + ':' if (UseCapturedNS_ and self.LanguageCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLanguageCode>%s</%sLanguageCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LanguageCode), input_name='LanguageCode')), namespaceprefix_ , eol_))
        if self.LocaleCode is not None:
            namespaceprefix_ = self.LocaleCode_nsprefix_ + ':' if (UseCapturedNS_ and self.LocaleCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocaleCode>%s</%sLocaleCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocaleCode), input_name='LocaleCode')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'LanguageCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LanguageCode')
            value_ = self.gds_validate_string(value_, node, 'LanguageCode')
            self.LanguageCode = value_
            self.LanguageCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocaleCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocaleCode')
            value_ = self.gds_validate_string(value_, node, 'LocaleCode')
            self.LocaleCode = value_
            self.LocaleCode_nsprefix_ = child_.prefix
# end class Localization


class Money(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Currency=None, Amount=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Currency = Currency
        self.Currency_nsprefix_ = None
        self.Amount = Amount
        self.Amount_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Money)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Money.subclass:
            return Money.subclass(*args_, **kwargs_)
        else:
            return Money(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Currency(self):
        return self.Currency
    def set_Currency(self, Currency):
        self.Currency = Currency
    def get_Amount(self):
        return self.Amount
    def set_Amount(self, Amount):
        self.Amount = Amount
    def hasContent_(self):
        if (
            self.Currency is not None or
            self.Amount is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Money', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Money')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Money':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Money')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Money', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Money'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Money', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Currency is not None:
            namespaceprefix_ = self.Currency_nsprefix_ + ':' if (UseCapturedNS_ and self.Currency_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrency>%s</%sCurrency>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Currency), input_name='Currency')), namespaceprefix_ , eol_))
        if self.Amount is not None:
            namespaceprefix_ = self.Amount_nsprefix_ + ':' if (UseCapturedNS_ and self.Amount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAmount>%s</%sAmount>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Amount, input_name='Amount'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Currency':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Currency')
            value_ = self.gds_validate_string(value_, node, 'Currency')
            self.Currency = value_
            self.Currency_nsprefix_ = child_.prefix
        elif nodeName_ == 'Amount' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Amount')
            fval_ = self.gds_validate_decimal(fval_, node, 'Amount')
            self.Amount = fval_
            self.Amount_nsprefix_ = child_.prefix
# end class Money


class Notification(GeneratedsSuper):
    """The descriptive data regarding the result of the submitted
    transaction."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Severity=None, Source=None, Code=None, Message=None, LocalizedMessage=None, MessageParameters=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Severity = Severity
        self.validate_NotificationSeverityType(self.Severity)
        self.Severity_nsprefix_ = "ns"
        self.Source = Source
        self.Source_nsprefix_ = None
        self.Code = Code
        self.Code_nsprefix_ = None
        self.Message = Message
        self.Message_nsprefix_ = None
        self.LocalizedMessage = LocalizedMessage
        self.LocalizedMessage_nsprefix_ = None
        if MessageParameters is None:
            self.MessageParameters = []
        else:
            self.MessageParameters = MessageParameters
        self.MessageParameters_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Notification)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Notification.subclass:
            return Notification.subclass(*args_, **kwargs_)
        else:
            return Notification(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Severity(self):
        return self.Severity
    def set_Severity(self, Severity):
        self.Severity = Severity
    def get_Source(self):
        return self.Source
    def set_Source(self, Source):
        self.Source = Source
    def get_Code(self):
        return self.Code
    def set_Code(self, Code):
        self.Code = Code
    def get_Message(self):
        return self.Message
    def set_Message(self, Message):
        self.Message = Message
    def get_LocalizedMessage(self):
        return self.LocalizedMessage
    def set_LocalizedMessage(self, LocalizedMessage):
        self.LocalizedMessage = LocalizedMessage
    def get_MessageParameters(self):
        return self.MessageParameters
    def set_MessageParameters(self, MessageParameters):
        self.MessageParameters = MessageParameters
    def add_MessageParameters(self, value):
        self.MessageParameters.append(value)
    def insert_MessageParameters_at(self, index, value):
        self.MessageParameters.insert(index, value)
    def replace_MessageParameters_at(self, index, value):
        self.MessageParameters[index] = value
    def validate_NotificationSeverityType(self, value):
        result = True
        # Validate type NotificationSeverityType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ERROR', 'FAILURE', 'NOTE', 'SUCCESS', 'WARNING']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on NotificationSeverityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Severity is not None or
            self.Source is not None or
            self.Code is not None or
            self.Message is not None or
            self.LocalizedMessage is not None or
            self.MessageParameters
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Notification', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Notification')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Notification':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Notification')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Notification', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Notification'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Notification', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Severity is not None:
            namespaceprefix_ = self.Severity_nsprefix_ + ':' if (UseCapturedNS_ and self.Severity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSeverity>%s</%sSeverity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Severity), input_name='Severity')), namespaceprefix_ , eol_))
        if self.Source is not None:
            namespaceprefix_ = self.Source_nsprefix_ + ':' if (UseCapturedNS_ and self.Source_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSource>%s</%sSource>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Source), input_name='Source')), namespaceprefix_ , eol_))
        if self.Code is not None:
            namespaceprefix_ = self.Code_nsprefix_ + ':' if (UseCapturedNS_ and self.Code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCode>%s</%sCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Code), input_name='Code')), namespaceprefix_ , eol_))
        if self.Message is not None:
            namespaceprefix_ = self.Message_nsprefix_ + ':' if (UseCapturedNS_ and self.Message_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMessage>%s</%sMessage>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Message), input_name='Message')), namespaceprefix_ , eol_))
        if self.LocalizedMessage is not None:
            namespaceprefix_ = self.LocalizedMessage_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalizedMessage_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalizedMessage>%s</%sLocalizedMessage>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalizedMessage), input_name='LocalizedMessage')), namespaceprefix_ , eol_))
        for MessageParameters_ in self.MessageParameters:
            namespaceprefix_ = self.MessageParameters_nsprefix_ + ':' if (UseCapturedNS_ and self.MessageParameters_nsprefix_) else ''
            MessageParameters_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='MessageParameters', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Severity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Severity')
            value_ = self.gds_validate_string(value_, node, 'Severity')
            self.Severity = value_
            self.Severity_nsprefix_ = child_.prefix
            # validate type NotificationSeverityType
            self.validate_NotificationSeverityType(self.Severity)
        elif nodeName_ == 'Source':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Source')
            value_ = self.gds_validate_string(value_, node, 'Source')
            self.Source = value_
            self.Source_nsprefix_ = child_.prefix
        elif nodeName_ == 'Code':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Code')
            value_ = self.gds_validate_string(value_, node, 'Code')
            self.Code = value_
            self.Code_nsprefix_ = child_.prefix
        elif nodeName_ == 'Message':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Message')
            value_ = self.gds_validate_string(value_, node, 'Message')
            self.Message = value_
            self.Message_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocalizedMessage':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalizedMessage')
            value_ = self.gds_validate_string(value_, node, 'LocalizedMessage')
            self.LocalizedMessage = value_
            self.LocalizedMessage_nsprefix_ = child_.prefix
        elif nodeName_ == 'MessageParameters':
            obj_ = NotificationParameter.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.MessageParameters.append(obj_)
            obj_.original_tagname_ = 'MessageParameters'
# end class Notification


class NotificationParameter(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Id=None, Value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Id = Id
        self.Id_nsprefix_ = None
        self.Value = Value
        self.Value_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, NotificationParameter)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if NotificationParameter.subclass:
            return NotificationParameter.subclass(*args_, **kwargs_)
        else:
            return NotificationParameter(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def hasContent_(self):
        if (
            self.Id is not None or
            self.Value is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NotificationParameter', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('NotificationParameter')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'NotificationParameter':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='NotificationParameter')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='NotificationParameter', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='NotificationParameter'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NotificationParameter', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Id is not None:
            namespaceprefix_ = self.Id_nsprefix_ + ':' if (UseCapturedNS_ and self.Id_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sId>%s</%sId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Id), input_name='Id')), namespaceprefix_ , eol_))
        if self.Value is not None:
            namespaceprefix_ = self.Value_nsprefix_ + ':' if (UseCapturedNS_ and self.Value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sValue>%s</%sValue>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Value), input_name='Value')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Id':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Id')
            value_ = self.gds_validate_string(value_, node, 'Id')
            self.Id = value_
            self.Id_nsprefix_ = child_.prefix
        elif nodeName_ == 'Value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Value')
            value_ = self.gds_validate_string(value_, node, 'Value')
            self.Value = value_
            self.Value_nsprefix_ = child_.prefix
# end class NotificationParameter


class OperationalDocumentPart(GeneratedsSuper):
    """A single part of an operational document, such as one page of a
    multiple-page document whose format requires a separate image per
    page."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DocumentPartSequenceNumber=None, Image=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DocumentPartSequenceNumber = DocumentPartSequenceNumber
        self.DocumentPartSequenceNumber_nsprefix_ = None
        self.Image = Image
        self.Image_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, OperationalDocumentPart)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OperationalDocumentPart.subclass:
            return OperationalDocumentPart.subclass(*args_, **kwargs_)
        else:
            return OperationalDocumentPart(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DocumentPartSequenceNumber(self):
        return self.DocumentPartSequenceNumber
    def set_DocumentPartSequenceNumber(self, DocumentPartSequenceNumber):
        self.DocumentPartSequenceNumber = DocumentPartSequenceNumber
    def get_Image(self):
        return self.Image
    def set_Image(self, Image):
        self.Image = Image
    def hasContent_(self):
        if (
            self.DocumentPartSequenceNumber is not None or
            self.Image is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OperationalDocumentPart', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OperationalDocumentPart')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'OperationalDocumentPart':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OperationalDocumentPart')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='OperationalDocumentPart', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='OperationalDocumentPart'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OperationalDocumentPart', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DocumentPartSequenceNumber is not None:
            namespaceprefix_ = self.DocumentPartSequenceNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.DocumentPartSequenceNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDocumentPartSequenceNumber>%s</%sDocumentPartSequenceNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.DocumentPartSequenceNumber, input_name='DocumentPartSequenceNumber'), namespaceprefix_ , eol_))
        if self.Image is not None:
            namespaceprefix_ = self.Image_nsprefix_ + ':' if (UseCapturedNS_ and self.Image_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sImage>%s</%sImage>%s' % (namespaceprefix_ , self.gds_format_base64(self.Image, input_name='Image'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DocumentPartSequenceNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'DocumentPartSequenceNumber')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'DocumentPartSequenceNumber')
            self.DocumentPartSequenceNumber = ival_
            self.DocumentPartSequenceNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'Image':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'Image')
            else:
                bval_ = None
            self.Image = bval_
            self.Image_nsprefix_ = child_.prefix
# end class OperationalDocumentPart


class OperationalDocumentSpecification(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DocumentTypes=None, SignatureReleaseDocumentDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if DocumentTypes is None:
            self.DocumentTypes = []
        else:
            self.DocumentTypes = DocumentTypes
        self.DocumentTypes_nsprefix_ = "ns"
        self.SignatureReleaseDocumentDetail = SignatureReleaseDocumentDetail
        self.SignatureReleaseDocumentDetail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, OperationalDocumentSpecification)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OperationalDocumentSpecification.subclass:
            return OperationalDocumentSpecification.subclass(*args_, **kwargs_)
        else:
            return OperationalDocumentSpecification(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DocumentTypes(self):
        return self.DocumentTypes
    def set_DocumentTypes(self, DocumentTypes):
        self.DocumentTypes = DocumentTypes
    def add_DocumentTypes(self, value):
        self.DocumentTypes.append(value)
    def insert_DocumentTypes_at(self, index, value):
        self.DocumentTypes.insert(index, value)
    def replace_DocumentTypes_at(self, index, value):
        self.DocumentTypes[index] = value
    def get_SignatureReleaseDocumentDetail(self):
        return self.SignatureReleaseDocumentDetail
    def set_SignatureReleaseDocumentDetail(self, SignatureReleaseDocumentDetail):
        self.SignatureReleaseDocumentDetail = SignatureReleaseDocumentDetail
    def validate_OperationalDocumentType(self, value):
        result = True
        # Validate type OperationalDocumentType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['SIGNATURE_RELEASE_DOCUMENT']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on OperationalDocumentType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.DocumentTypes or
            self.SignatureReleaseDocumentDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OperationalDocumentSpecification', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OperationalDocumentSpecification')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'OperationalDocumentSpecification':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OperationalDocumentSpecification')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='OperationalDocumentSpecification', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='OperationalDocumentSpecification'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OperationalDocumentSpecification', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for DocumentTypes_ in self.DocumentTypes:
            namespaceprefix_ = self.DocumentTypes_nsprefix_ + ':' if (UseCapturedNS_ and self.DocumentTypes_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDocumentTypes>%s</%sDocumentTypes>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(DocumentTypes_), input_name='DocumentTypes')), namespaceprefix_ , eol_))
        if self.SignatureReleaseDocumentDetail is not None:
            namespaceprefix_ = self.SignatureReleaseDocumentDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.SignatureReleaseDocumentDetail_nsprefix_) else ''
            self.SignatureReleaseDocumentDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='SignatureReleaseDocumentDetail', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DocumentTypes':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DocumentTypes')
            value_ = self.gds_validate_string(value_, node, 'DocumentTypes')
            self.DocumentTypes.append(value_)
            self.DocumentTypes_nsprefix_ = child_.prefix
            # validate type OperationalDocumentType
            self.validate_OperationalDocumentType(self.DocumentTypes[-1])
        elif nodeName_ == 'SignatureReleaseDocumentDetail':
            obj_ = SignatureReleaseDocumentDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SignatureReleaseDocumentDetail = obj_
            obj_.original_tagname_ = 'SignatureReleaseDocumentDetail'
# end class OperationalDocumentSpecification


class ParsedContact(GeneratedsSuper):
    """This type contains equivalent data to Contact, but uses a form of person
    name with separate first and last names."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PersonName=None, Title=None, CompanyName=None, PhoneNumberCountryCode=None, PhoneNumberAreaCode=None, PhoneNumber=None, PhoneExtension=None, PagerNumber=None, FaxNumber=None, EMailAddress=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PersonName = PersonName
        self.PersonName_nsprefix_ = "ns"
        self.Title = Title
        self.Title_nsprefix_ = None
        self.CompanyName = CompanyName
        self.CompanyName_nsprefix_ = None
        self.PhoneNumberCountryCode = PhoneNumberCountryCode
        self.PhoneNumberCountryCode_nsprefix_ = None
        self.PhoneNumberAreaCode = PhoneNumberAreaCode
        self.PhoneNumberAreaCode_nsprefix_ = None
        self.PhoneNumber = PhoneNumber
        self.PhoneNumber_nsprefix_ = None
        self.PhoneExtension = PhoneExtension
        self.PhoneExtension_nsprefix_ = None
        self.PagerNumber = PagerNumber
        self.PagerNumber_nsprefix_ = None
        self.FaxNumber = FaxNumber
        self.FaxNumber_nsprefix_ = None
        self.EMailAddress = EMailAddress
        self.EMailAddress_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ParsedContact)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ParsedContact.subclass:
            return ParsedContact.subclass(*args_, **kwargs_)
        else:
            return ParsedContact(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PersonName(self):
        return self.PersonName
    def set_PersonName(self, PersonName):
        self.PersonName = PersonName
    def get_Title(self):
        return self.Title
    def set_Title(self, Title):
        self.Title = Title
    def get_CompanyName(self):
        return self.CompanyName
    def set_CompanyName(self, CompanyName):
        self.CompanyName = CompanyName
    def get_PhoneNumberCountryCode(self):
        return self.PhoneNumberCountryCode
    def set_PhoneNumberCountryCode(self, PhoneNumberCountryCode):
        self.PhoneNumberCountryCode = PhoneNumberCountryCode
    def get_PhoneNumberAreaCode(self):
        return self.PhoneNumberAreaCode
    def set_PhoneNumberAreaCode(self, PhoneNumberAreaCode):
        self.PhoneNumberAreaCode = PhoneNumberAreaCode
    def get_PhoneNumber(self):
        return self.PhoneNumber
    def set_PhoneNumber(self, PhoneNumber):
        self.PhoneNumber = PhoneNumber
    def get_PhoneExtension(self):
        return self.PhoneExtension
    def set_PhoneExtension(self, PhoneExtension):
        self.PhoneExtension = PhoneExtension
    def get_PagerNumber(self):
        return self.PagerNumber
    def set_PagerNumber(self, PagerNumber):
        self.PagerNumber = PagerNumber
    def get_FaxNumber(self):
        return self.FaxNumber
    def set_FaxNumber(self, FaxNumber):
        self.FaxNumber = FaxNumber
    def get_EMailAddress(self):
        return self.EMailAddress
    def set_EMailAddress(self, EMailAddress):
        self.EMailAddress = EMailAddress
    def hasContent_(self):
        if (
            self.PersonName is not None or
            self.Title is not None or
            self.CompanyName is not None or
            self.PhoneNumberCountryCode is not None or
            self.PhoneNumberAreaCode is not None or
            self.PhoneNumber is not None or
            self.PhoneExtension is not None or
            self.PagerNumber is not None or
            self.FaxNumber is not None or
            self.EMailAddress is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ParsedContact', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ParsedContact')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ParsedContact':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ParsedContact')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ParsedContact', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ParsedContact'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ParsedContact', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PersonName is not None:
            namespaceprefix_ = self.PersonName_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonName_nsprefix_) else ''
            self.PersonName.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PersonName', pretty_print=pretty_print)
        if self.Title is not None:
            namespaceprefix_ = self.Title_nsprefix_ + ':' if (UseCapturedNS_ and self.Title_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTitle>%s</%sTitle>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Title), input_name='Title')), namespaceprefix_ , eol_))
        if self.CompanyName is not None:
            namespaceprefix_ = self.CompanyName_nsprefix_ + ':' if (UseCapturedNS_ and self.CompanyName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCompanyName>%s</%sCompanyName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CompanyName), input_name='CompanyName')), namespaceprefix_ , eol_))
        if self.PhoneNumberCountryCode is not None:
            namespaceprefix_ = self.PhoneNumberCountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.PhoneNumberCountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPhoneNumberCountryCode>%s</%sPhoneNumberCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PhoneNumberCountryCode), input_name='PhoneNumberCountryCode')), namespaceprefix_ , eol_))
        if self.PhoneNumberAreaCode is not None:
            namespaceprefix_ = self.PhoneNumberAreaCode_nsprefix_ + ':' if (UseCapturedNS_ and self.PhoneNumberAreaCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPhoneNumberAreaCode>%s</%sPhoneNumberAreaCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PhoneNumberAreaCode), input_name='PhoneNumberAreaCode')), namespaceprefix_ , eol_))
        if self.PhoneNumber is not None:
            namespaceprefix_ = self.PhoneNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.PhoneNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPhoneNumber>%s</%sPhoneNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PhoneNumber), input_name='PhoneNumber')), namespaceprefix_ , eol_))
        if self.PhoneExtension is not None:
            namespaceprefix_ = self.PhoneExtension_nsprefix_ + ':' if (UseCapturedNS_ and self.PhoneExtension_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPhoneExtension>%s</%sPhoneExtension>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PhoneExtension), input_name='PhoneExtension')), namespaceprefix_ , eol_))
        if self.PagerNumber is not None:
            namespaceprefix_ = self.PagerNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.PagerNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPagerNumber>%s</%sPagerNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PagerNumber), input_name='PagerNumber')), namespaceprefix_ , eol_))
        if self.FaxNumber is not None:
            namespaceprefix_ = self.FaxNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.FaxNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFaxNumber>%s</%sFaxNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FaxNumber), input_name='FaxNumber')), namespaceprefix_ , eol_))
        if self.EMailAddress is not None:
            namespaceprefix_ = self.EMailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.EMailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEMailAddress>%s</%sEMailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EMailAddress), input_name='EMailAddress')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'PersonName':
            obj_ = ParsedPersonName.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PersonName = obj_
            obj_.original_tagname_ = 'PersonName'
        elif nodeName_ == 'Title':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Title')
            value_ = self.gds_validate_string(value_, node, 'Title')
            self.Title = value_
            self.Title_nsprefix_ = child_.prefix
        elif nodeName_ == 'CompanyName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CompanyName')
            value_ = self.gds_validate_string(value_, node, 'CompanyName')
            self.CompanyName = value_
            self.CompanyName_nsprefix_ = child_.prefix
        elif nodeName_ == 'PhoneNumberCountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PhoneNumberCountryCode')
            value_ = self.gds_validate_string(value_, node, 'PhoneNumberCountryCode')
            self.PhoneNumberCountryCode = value_
            self.PhoneNumberCountryCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'PhoneNumberAreaCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PhoneNumberAreaCode')
            value_ = self.gds_validate_string(value_, node, 'PhoneNumberAreaCode')
            self.PhoneNumberAreaCode = value_
            self.PhoneNumberAreaCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'PhoneNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PhoneNumber')
            value_ = self.gds_validate_string(value_, node, 'PhoneNumber')
            self.PhoneNumber = value_
            self.PhoneNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'PhoneExtension':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PhoneExtension')
            value_ = self.gds_validate_string(value_, node, 'PhoneExtension')
            self.PhoneExtension = value_
            self.PhoneExtension_nsprefix_ = child_.prefix
        elif nodeName_ == 'PagerNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PagerNumber')
            value_ = self.gds_validate_string(value_, node, 'PagerNumber')
            self.PagerNumber = value_
            self.PagerNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'FaxNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FaxNumber')
            value_ = self.gds_validate_string(value_, node, 'FaxNumber')
            self.FaxNumber = value_
            self.FaxNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'EMailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EMailAddress')
            value_ = self.gds_validate_string(value_, node, 'EMailAddress')
            self.EMailAddress = value_
            self.EMailAddress_nsprefix_ = child_.prefix
# end class ParsedContact


class ParsedContactAndAddress(GeneratedsSuper):
    """This type contains equivalent data to ContactAndAddress, but uses a form
    of person name with separate first, middle and last names."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Contact=None, Address=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Contact = Contact
        self.Contact_nsprefix_ = "ns"
        self.Address = Address
        self.Address_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ParsedContactAndAddress)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ParsedContactAndAddress.subclass:
            return ParsedContactAndAddress.subclass(*args_, **kwargs_)
        else:
            return ParsedContactAndAddress(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Contact(self):
        return self.Contact
    def set_Contact(self, Contact):
        self.Contact = Contact
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def hasContent_(self):
        if (
            self.Contact is not None or
            self.Address is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ParsedContactAndAddress', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ParsedContactAndAddress')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ParsedContactAndAddress':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ParsedContactAndAddress')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ParsedContactAndAddress', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ParsedContactAndAddress'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ParsedContactAndAddress', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Contact is not None:
            namespaceprefix_ = self.Contact_nsprefix_ + ':' if (UseCapturedNS_ and self.Contact_nsprefix_) else ''
            self.Contact.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Contact', pretty_print=pretty_print)
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Contact':
            obj_ = ParsedContact.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Contact = obj_
            obj_.original_tagname_ = 'Contact'
        elif nodeName_ == 'Address':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
# end class ParsedContactAndAddress


class ParsedPersonName(GeneratedsSuper):
    """The descriptive data for a person's name broken out into individual name
    elements such as first name, last name."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Prefix=None, Title=None, FirstName=None, MiddleName=None, LastName=None, Suffix=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Prefix = Prefix
        self.Prefix_nsprefix_ = None
        self.Title = Title
        self.Title_nsprefix_ = None
        self.FirstName = FirstName
        self.FirstName_nsprefix_ = None
        self.MiddleName = MiddleName
        self.MiddleName_nsprefix_ = None
        self.LastName = LastName
        self.LastName_nsprefix_ = None
        self.Suffix = Suffix
        self.Suffix_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ParsedPersonName)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ParsedPersonName.subclass:
            return ParsedPersonName.subclass(*args_, **kwargs_)
        else:
            return ParsedPersonName(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Prefix(self):
        return self.Prefix
    def set_Prefix(self, Prefix):
        self.Prefix = Prefix
    def get_Title(self):
        return self.Title
    def set_Title(self, Title):
        self.Title = Title
    def get_FirstName(self):
        return self.FirstName
    def set_FirstName(self, FirstName):
        self.FirstName = FirstName
    def get_MiddleName(self):
        return self.MiddleName
    def set_MiddleName(self, MiddleName):
        self.MiddleName = MiddleName
    def get_LastName(self):
        return self.LastName
    def set_LastName(self, LastName):
        self.LastName = LastName
    def get_Suffix(self):
        return self.Suffix
    def set_Suffix(self, Suffix):
        self.Suffix = Suffix
    def hasContent_(self):
        if (
            self.Prefix is not None or
            self.Title is not None or
            self.FirstName is not None or
            self.MiddleName is not None or
            self.LastName is not None or
            self.Suffix is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ParsedPersonName', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ParsedPersonName')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ParsedPersonName':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ParsedPersonName')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ParsedPersonName', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ParsedPersonName'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ParsedPersonName', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Prefix is not None:
            namespaceprefix_ = self.Prefix_nsprefix_ + ':' if (UseCapturedNS_ and self.Prefix_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPrefix>%s</%sPrefix>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Prefix), input_name='Prefix')), namespaceprefix_ , eol_))
        if self.Title is not None:
            namespaceprefix_ = self.Title_nsprefix_ + ':' if (UseCapturedNS_ and self.Title_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTitle>%s</%sTitle>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Title), input_name='Title')), namespaceprefix_ , eol_))
        if self.FirstName is not None:
            namespaceprefix_ = self.FirstName_nsprefix_ + ':' if (UseCapturedNS_ and self.FirstName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFirstName>%s</%sFirstName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FirstName), input_name='FirstName')), namespaceprefix_ , eol_))
        if self.MiddleName is not None:
            namespaceprefix_ = self.MiddleName_nsprefix_ + ':' if (UseCapturedNS_ and self.MiddleName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMiddleName>%s</%sMiddleName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MiddleName), input_name='MiddleName')), namespaceprefix_ , eol_))
        if self.LastName is not None:
            namespaceprefix_ = self.LastName_nsprefix_ + ':' if (UseCapturedNS_ and self.LastName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLastName>%s</%sLastName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LastName), input_name='LastName')), namespaceprefix_ , eol_))
        if self.Suffix is not None:
            namespaceprefix_ = self.Suffix_nsprefix_ + ':' if (UseCapturedNS_ and self.Suffix_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSuffix>%s</%sSuffix>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Suffix), input_name='Suffix')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Prefix':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Prefix')
            value_ = self.gds_validate_string(value_, node, 'Prefix')
            self.Prefix = value_
            self.Prefix_nsprefix_ = child_.prefix
        elif nodeName_ == 'Title':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Title')
            value_ = self.gds_validate_string(value_, node, 'Title')
            self.Title = value_
            self.Title_nsprefix_ = child_.prefix
        elif nodeName_ == 'FirstName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FirstName')
            value_ = self.gds_validate_string(value_, node, 'FirstName')
            self.FirstName = value_
            self.FirstName_nsprefix_ = child_.prefix
        elif nodeName_ == 'MiddleName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MiddleName')
            value_ = self.gds_validate_string(value_, node, 'MiddleName')
            self.MiddleName = value_
            self.MiddleName_nsprefix_ = child_.prefix
        elif nodeName_ == 'LastName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LastName')
            value_ = self.gds_validate_string(value_, node, 'LastName')
            self.LastName = value_
            self.LastName_nsprefix_ = child_.prefix
        elif nodeName_ == 'Suffix':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Suffix')
            value_ = self.gds_validate_string(value_, node, 'Suffix')
            self.Suffix = value_
            self.Suffix_nsprefix_ = child_.prefix
# end class ParsedPersonName


class Party(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AccountNumber=None, Tins=None, Contact=None, Address=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.AccountNumber = AccountNumber
        self.AccountNumber_nsprefix_ = None
        if Tins is None:
            self.Tins = []
        else:
            self.Tins = Tins
        self.Tins_nsprefix_ = "ns"
        self.Contact = Contact
        self.Contact_nsprefix_ = "ns"
        self.Address = Address
        self.Address_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Party)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Party.subclass:
            return Party.subclass(*args_, **kwargs_)
        else:
            return Party(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AccountNumber(self):
        return self.AccountNumber
    def set_AccountNumber(self, AccountNumber):
        self.AccountNumber = AccountNumber
    def get_Tins(self):
        return self.Tins
    def set_Tins(self, Tins):
        self.Tins = Tins
    def add_Tins(self, value):
        self.Tins.append(value)
    def insert_Tins_at(self, index, value):
        self.Tins.insert(index, value)
    def replace_Tins_at(self, index, value):
        self.Tins[index] = value
    def get_Contact(self):
        return self.Contact
    def set_Contact(self, Contact):
        self.Contact = Contact
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def hasContent_(self):
        if (
            self.AccountNumber is not None or
            self.Tins or
            self.Contact is not None or
            self.Address is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Party', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Party')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Party':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Party')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Party', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Party'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Party', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.AccountNumber is not None:
            namespaceprefix_ = self.AccountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.AccountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccountNumber>%s</%sAccountNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AccountNumber), input_name='AccountNumber')), namespaceprefix_ , eol_))
        for Tins_ in self.Tins:
            namespaceprefix_ = self.Tins_nsprefix_ + ':' if (UseCapturedNS_ and self.Tins_nsprefix_) else ''
            Tins_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Tins', pretty_print=pretty_print)
        if self.Contact is not None:
            namespaceprefix_ = self.Contact_nsprefix_ + ':' if (UseCapturedNS_ and self.Contact_nsprefix_) else ''
            self.Contact.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Contact', pretty_print=pretty_print)
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'AccountNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AccountNumber')
            value_ = self.gds_validate_string(value_, node, 'AccountNumber')
            self.AccountNumber = value_
            self.AccountNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'Tins':
            obj_ = TaxpayerIdentification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Tins.append(obj_)
            obj_.original_tagname_ = 'Tins'
        elif nodeName_ == 'Contact':
            obj_ = Contact.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Contact = obj_
            obj_.original_tagname_ = 'Contact'
        elif nodeName_ == 'Address':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
# end class Party


class Payor(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ResponsibleParty=None, AssociatedAccounts=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ResponsibleParty = ResponsibleParty
        self.ResponsibleParty_nsprefix_ = "ns"
        if AssociatedAccounts is None:
            self.AssociatedAccounts = []
        else:
            self.AssociatedAccounts = AssociatedAccounts
        self.AssociatedAccounts_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Payor)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Payor.subclass:
            return Payor.subclass(*args_, **kwargs_)
        else:
            return Payor(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ResponsibleParty(self):
        return self.ResponsibleParty
    def set_ResponsibleParty(self, ResponsibleParty):
        self.ResponsibleParty = ResponsibleParty
    def get_AssociatedAccounts(self):
        return self.AssociatedAccounts
    def set_AssociatedAccounts(self, AssociatedAccounts):
        self.AssociatedAccounts = AssociatedAccounts
    def add_AssociatedAccounts(self, value):
        self.AssociatedAccounts.append(value)
    def insert_AssociatedAccounts_at(self, index, value):
        self.AssociatedAccounts.insert(index, value)
    def replace_AssociatedAccounts_at(self, index, value):
        self.AssociatedAccounts[index] = value
    def hasContent_(self):
        if (
            self.ResponsibleParty is not None or
            self.AssociatedAccounts
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Payor', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Payor')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Payor':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Payor')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Payor', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Payor'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Payor', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ResponsibleParty is not None:
            namespaceprefix_ = self.ResponsibleParty_nsprefix_ + ':' if (UseCapturedNS_ and self.ResponsibleParty_nsprefix_) else ''
            self.ResponsibleParty.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ResponsibleParty', pretty_print=pretty_print)
        for AssociatedAccounts_ in self.AssociatedAccounts:
            namespaceprefix_ = self.AssociatedAccounts_nsprefix_ + ':' if (UseCapturedNS_ and self.AssociatedAccounts_nsprefix_) else ''
            AssociatedAccounts_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AssociatedAccounts', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ResponsibleParty':
            obj_ = Party.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ResponsibleParty = obj_
            obj_.original_tagname_ = 'ResponsibleParty'
        elif nodeName_ == 'AssociatedAccounts':
            obj_ = AssociatedAccount.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AssociatedAccounts.append(obj_)
            obj_.original_tagname_ = 'AssociatedAccounts'
# end class Payor


class ProcessDeliveryReply(GeneratedsSuper):
    """Reply parameter of IFSS method to process a specific delivery option"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, Confirmation=None, MasterTrackingNumber=None, PackageCount=None, EstimatedDeliveryTimestamp=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.HighestSeverity = HighestSeverity
        self.validate_NotificationSeverityType(self.HighestSeverity)
        self.HighestSeverity_nsprefix_ = "ns"
        if Notifications is None:
            self.Notifications = []
        else:
            self.Notifications = Notifications
        self.Notifications_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.Confirmation = Confirmation
        self.Confirmation_nsprefix_ = None
        self.MasterTrackingNumber = MasterTrackingNumber
        self.MasterTrackingNumber_nsprefix_ = "ns"
        self.PackageCount = PackageCount
        self.PackageCount_nsprefix_ = None
        if isinstance(EstimatedDeliveryTimestamp, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(EstimatedDeliveryTimestamp, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = EstimatedDeliveryTimestamp
        self.EstimatedDeliveryTimestamp = initvalue_
        self.EstimatedDeliveryTimestamp_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ProcessDeliveryReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ProcessDeliveryReply.subclass:
            return ProcessDeliveryReply.subclass(*args_, **kwargs_)
        else:
            return ProcessDeliveryReply(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_HighestSeverity(self):
        return self.HighestSeverity
    def set_HighestSeverity(self, HighestSeverity):
        self.HighestSeverity = HighestSeverity
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def add_Notifications(self, value):
        self.Notifications.append(value)
    def insert_Notifications_at(self, index, value):
        self.Notifications.insert(index, value)
    def replace_Notifications_at(self, index, value):
        self.Notifications[index] = value
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_Confirmation(self):
        return self.Confirmation
    def set_Confirmation(self, Confirmation):
        self.Confirmation = Confirmation
    def get_MasterTrackingNumber(self):
        return self.MasterTrackingNumber
    def set_MasterTrackingNumber(self, MasterTrackingNumber):
        self.MasterTrackingNumber = MasterTrackingNumber
    def get_PackageCount(self):
        return self.PackageCount
    def set_PackageCount(self, PackageCount):
        self.PackageCount = PackageCount
    def get_EstimatedDeliveryTimestamp(self):
        return self.EstimatedDeliveryTimestamp
    def set_EstimatedDeliveryTimestamp(self, EstimatedDeliveryTimestamp):
        self.EstimatedDeliveryTimestamp = EstimatedDeliveryTimestamp
    def validate_NotificationSeverityType(self, value):
        result = True
        # Validate type NotificationSeverityType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ERROR', 'FAILURE', 'NOTE', 'SUCCESS', 'WARNING']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on NotificationSeverityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.HighestSeverity is not None or
            self.Notifications or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.Confirmation is not None or
            self.MasterTrackingNumber is not None or
            self.PackageCount is not None or
            self.EstimatedDeliveryTimestamp is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ProcessDeliveryReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ProcessDeliveryReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ProcessDeliveryReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ProcessDeliveryReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ProcessDeliveryReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ProcessDeliveryReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ProcessDeliveryReply', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.HighestSeverity is not None:
            namespaceprefix_ = self.HighestSeverity_nsprefix_ + ':' if (UseCapturedNS_ and self.HighestSeverity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHighestSeverity>%s</%sHighestSeverity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HighestSeverity), input_name='HighestSeverity')), namespaceprefix_ , eol_))
        for Notifications_ in self.Notifications:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            Notifications_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.Confirmation is not None:
            namespaceprefix_ = self.Confirmation_nsprefix_ + ':' if (UseCapturedNS_ and self.Confirmation_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sConfirmation>%s</%sConfirmation>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Confirmation), input_name='Confirmation')), namespaceprefix_ , eol_))
        if self.MasterTrackingNumber is not None:
            namespaceprefix_ = self.MasterTrackingNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.MasterTrackingNumber_nsprefix_) else ''
            self.MasterTrackingNumber.export(outfile, level, namespaceprefix_, namespacedef_='', name_='MasterTrackingNumber', pretty_print=pretty_print)
        if self.PackageCount is not None:
            namespaceprefix_ = self.PackageCount_nsprefix_ + ':' if (UseCapturedNS_ and self.PackageCount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPackageCount>%s</%sPackageCount>%s' % (namespaceprefix_ , self.gds_format_integer(self.PackageCount, input_name='PackageCount'), namespaceprefix_ , eol_))
        if self.EstimatedDeliveryTimestamp is not None:
            namespaceprefix_ = self.EstimatedDeliveryTimestamp_nsprefix_ + ':' if (UseCapturedNS_ and self.EstimatedDeliveryTimestamp_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEstimatedDeliveryTimestamp>%s</%sEstimatedDeliveryTimestamp>%s' % (namespaceprefix_ , self.gds_format_datetime(self.EstimatedDeliveryTimestamp, input_name='EstimatedDeliveryTimestamp'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'HighestSeverity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HighestSeverity')
            value_ = self.gds_validate_string(value_, node, 'HighestSeverity')
            self.HighestSeverity = value_
            self.HighestSeverity_nsprefix_ = child_.prefix
            # validate type NotificationSeverityType
            self.validate_NotificationSeverityType(self.HighestSeverity)
        elif nodeName_ == 'Notifications':
            obj_ = Notification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications.append(obj_)
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'Confirmation':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Confirmation')
            value_ = self.gds_validate_string(value_, node, 'Confirmation')
            self.Confirmation = value_
            self.Confirmation_nsprefix_ = child_.prefix
        elif nodeName_ == 'MasterTrackingNumber':
            obj_ = TrackingId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.MasterTrackingNumber = obj_
            obj_.original_tagname_ = 'MasterTrackingNumber'
        elif nodeName_ == 'PackageCount' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'PackageCount')
            if ival_ < 0:
                raise_parse_error(child_, 'requires nonNegativeInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'PackageCount')
            self.PackageCount = ival_
            self.PackageCount_nsprefix_ = child_.prefix
        elif nodeName_ == 'EstimatedDeliveryTimestamp':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.EstimatedDeliveryTimestamp = dval_
            self.EstimatedDeliveryTimestamp_nsprefix_ = child_.prefix
# end class ProcessDeliveryReply


class ProcessDeliveryRequest(GeneratedsSuper):
    """Request parameter of IFSS method to process a specific delivery
    option."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, UserDetail=None, TransactionDetail=None, Version=None, ApplicationId=None, ActionRequested=None, UniqueTrackingNumber=None, RecipientContact=None, DestinationAddress=None, DeliveryRequestDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.WebAuthenticationDetail = WebAuthenticationDetail
        self.WebAuthenticationDetail_nsprefix_ = "ns"
        self.ClientDetail = ClientDetail
        self.ClientDetail_nsprefix_ = "ns"
        self.UserDetail = UserDetail
        self.UserDetail_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.ApplicationId = ApplicationId
        self.ApplicationId_nsprefix_ = None
        self.ActionRequested = ActionRequested
        self.validate_DeliveryActionType(self.ActionRequested)
        self.ActionRequested_nsprefix_ = "ns"
        self.UniqueTrackingNumber = UniqueTrackingNumber
        self.UniqueTrackingNumber_nsprefix_ = "ns"
        self.RecipientContact = RecipientContact
        self.RecipientContact_nsprefix_ = "ns"
        self.DestinationAddress = DestinationAddress
        self.DestinationAddress_nsprefix_ = "ns"
        self.DeliveryRequestDetail = DeliveryRequestDetail
        self.DeliveryRequestDetail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ProcessDeliveryRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ProcessDeliveryRequest.subclass:
            return ProcessDeliveryRequest.subclass(*args_, **kwargs_)
        else:
            return ProcessDeliveryRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_WebAuthenticationDetail(self):
        return self.WebAuthenticationDetail
    def set_WebAuthenticationDetail(self, WebAuthenticationDetail):
        self.WebAuthenticationDetail = WebAuthenticationDetail
    def get_ClientDetail(self):
        return self.ClientDetail
    def set_ClientDetail(self, ClientDetail):
        self.ClientDetail = ClientDetail
    def get_UserDetail(self):
        return self.UserDetail
    def set_UserDetail(self, UserDetail):
        self.UserDetail = UserDetail
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_ApplicationId(self):
        return self.ApplicationId
    def set_ApplicationId(self, ApplicationId):
        self.ApplicationId = ApplicationId
    def get_ActionRequested(self):
        return self.ActionRequested
    def set_ActionRequested(self, ActionRequested):
        self.ActionRequested = ActionRequested
    def get_UniqueTrackingNumber(self):
        return self.UniqueTrackingNumber
    def set_UniqueTrackingNumber(self, UniqueTrackingNumber):
        self.UniqueTrackingNumber = UniqueTrackingNumber
    def get_RecipientContact(self):
        return self.RecipientContact
    def set_RecipientContact(self, RecipientContact):
        self.RecipientContact = RecipientContact
    def get_DestinationAddress(self):
        return self.DestinationAddress
    def set_DestinationAddress(self, DestinationAddress):
        self.DestinationAddress = DestinationAddress
    def get_DeliveryRequestDetail(self):
        return self.DeliveryRequestDetail
    def set_DeliveryRequestDetail(self, DeliveryRequestDetail):
        self.DeliveryRequestDetail = DeliveryRequestDetail
    def validate_DeliveryActionType(self, value):
        result = True
        # Validate type DeliveryActionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ADD']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DeliveryActionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.UserDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.ApplicationId is not None or
            self.ActionRequested is not None or
            self.UniqueTrackingNumber is not None or
            self.RecipientContact is not None or
            self.DestinationAddress is not None or
            self.DeliveryRequestDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ProcessDeliveryRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ProcessDeliveryRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ProcessDeliveryRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ProcessDeliveryRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ProcessDeliveryRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ProcessDeliveryRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ProcessDeliveryRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.WebAuthenticationDetail is not None:
            namespaceprefix_ = self.WebAuthenticationDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.WebAuthenticationDetail_nsprefix_) else ''
            self.WebAuthenticationDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='WebAuthenticationDetail', pretty_print=pretty_print)
        if self.ClientDetail is not None:
            namespaceprefix_ = self.ClientDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientDetail_nsprefix_) else ''
            self.ClientDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClientDetail', pretty_print=pretty_print)
        if self.UserDetail is not None:
            namespaceprefix_ = self.UserDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.UserDetail_nsprefix_) else ''
            self.UserDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UserDetail', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.ApplicationId is not None:
            namespaceprefix_ = self.ApplicationId_nsprefix_ + ':' if (UseCapturedNS_ and self.ApplicationId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sApplicationId>%s</%sApplicationId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ApplicationId), input_name='ApplicationId')), namespaceprefix_ , eol_))
        if self.ActionRequested is not None:
            namespaceprefix_ = self.ActionRequested_nsprefix_ + ':' if (UseCapturedNS_ and self.ActionRequested_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sActionRequested>%s</%sActionRequested>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ActionRequested), input_name='ActionRequested')), namespaceprefix_ , eol_))
        if self.UniqueTrackingNumber is not None:
            namespaceprefix_ = self.UniqueTrackingNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.UniqueTrackingNumber_nsprefix_) else ''
            self.UniqueTrackingNumber.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UniqueTrackingNumber', pretty_print=pretty_print)
        if self.RecipientContact is not None:
            namespaceprefix_ = self.RecipientContact_nsprefix_ + ':' if (UseCapturedNS_ and self.RecipientContact_nsprefix_) else ''
            self.RecipientContact.export(outfile, level, namespaceprefix_, namespacedef_='', name_='RecipientContact', pretty_print=pretty_print)
        if self.DestinationAddress is not None:
            namespaceprefix_ = self.DestinationAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationAddress_nsprefix_) else ''
            self.DestinationAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DestinationAddress', pretty_print=pretty_print)
        if self.DeliveryRequestDetail is not None:
            namespaceprefix_ = self.DeliveryRequestDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryRequestDetail_nsprefix_) else ''
            self.DeliveryRequestDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DeliveryRequestDetail', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'WebAuthenticationDetail':
            obj_ = WebAuthenticationDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.WebAuthenticationDetail = obj_
            obj_.original_tagname_ = 'WebAuthenticationDetail'
        elif nodeName_ == 'ClientDetail':
            obj_ = ClientDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClientDetail = obj_
            obj_.original_tagname_ = 'ClientDetail'
        elif nodeName_ == 'UserDetail':
            obj_ = UserDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UserDetail = obj_
            obj_.original_tagname_ = 'UserDetail'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'ApplicationId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ApplicationId')
            value_ = self.gds_validate_string(value_, node, 'ApplicationId')
            self.ApplicationId = value_
            self.ApplicationId_nsprefix_ = child_.prefix
        elif nodeName_ == 'ActionRequested':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ActionRequested')
            value_ = self.gds_validate_string(value_, node, 'ActionRequested')
            self.ActionRequested = value_
            self.ActionRequested_nsprefix_ = child_.prefix
            # validate type DeliveryActionType
            self.validate_DeliveryActionType(self.ActionRequested)
        elif nodeName_ == 'UniqueTrackingNumber':
            obj_ = UniqueTrackingNumber.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UniqueTrackingNumber = obj_
            obj_.original_tagname_ = 'UniqueTrackingNumber'
        elif nodeName_ == 'RecipientContact':
            obj_ = Contact.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.RecipientContact = obj_
            obj_.original_tagname_ = 'RecipientContact'
        elif nodeName_ == 'DestinationAddress':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DestinationAddress = obj_
            obj_.original_tagname_ = 'DestinationAddress'
        elif nodeName_ == 'DeliveryRequestDetail':
            obj_ = DeliveryRequestDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DeliveryRequestDetail = obj_
            obj_.original_tagname_ = 'DeliveryRequestDetail'
# end class ProcessDeliveryRequest


class RatedDeliveryDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TotalPieces=None, TotalNetCharge=None, TotalSurcharges=None, Surcharges=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.TotalPieces = TotalPieces
        self.TotalPieces_nsprefix_ = None
        self.TotalNetCharge = TotalNetCharge
        self.TotalNetCharge_nsprefix_ = "ns"
        self.TotalSurcharges = TotalSurcharges
        self.TotalSurcharges_nsprefix_ = "ns"
        if Surcharges is None:
            self.Surcharges = []
        else:
            self.Surcharges = Surcharges
        self.Surcharges_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RatedDeliveryDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RatedDeliveryDetail.subclass:
            return RatedDeliveryDetail.subclass(*args_, **kwargs_)
        else:
            return RatedDeliveryDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_TotalPieces(self):
        return self.TotalPieces
    def set_TotalPieces(self, TotalPieces):
        self.TotalPieces = TotalPieces
    def get_TotalNetCharge(self):
        return self.TotalNetCharge
    def set_TotalNetCharge(self, TotalNetCharge):
        self.TotalNetCharge = TotalNetCharge
    def get_TotalSurcharges(self):
        return self.TotalSurcharges
    def set_TotalSurcharges(self, TotalSurcharges):
        self.TotalSurcharges = TotalSurcharges
    def get_Surcharges(self):
        return self.Surcharges
    def set_Surcharges(self, Surcharges):
        self.Surcharges = Surcharges
    def add_Surcharges(self, value):
        self.Surcharges.append(value)
    def insert_Surcharges_at(self, index, value):
        self.Surcharges.insert(index, value)
    def replace_Surcharges_at(self, index, value):
        self.Surcharges[index] = value
    def hasContent_(self):
        if (
            self.TotalPieces is not None or
            self.TotalNetCharge is not None or
            self.TotalSurcharges is not None or
            self.Surcharges
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RatedDeliveryDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RatedDeliveryDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RatedDeliveryDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RatedDeliveryDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RatedDeliveryDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RatedDeliveryDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RatedDeliveryDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.TotalPieces is not None:
            namespaceprefix_ = self.TotalPieces_nsprefix_ + ':' if (UseCapturedNS_ and self.TotalPieces_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTotalPieces>%s</%sTotalPieces>%s' % (namespaceprefix_ , self.gds_format_integer(self.TotalPieces, input_name='TotalPieces'), namespaceprefix_ , eol_))
        if self.TotalNetCharge is not None:
            namespaceprefix_ = self.TotalNetCharge_nsprefix_ + ':' if (UseCapturedNS_ and self.TotalNetCharge_nsprefix_) else ''
            self.TotalNetCharge.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TotalNetCharge', pretty_print=pretty_print)
        if self.TotalSurcharges is not None:
            namespaceprefix_ = self.TotalSurcharges_nsprefix_ + ':' if (UseCapturedNS_ and self.TotalSurcharges_nsprefix_) else ''
            self.TotalSurcharges.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TotalSurcharges', pretty_print=pretty_print)
        for Surcharges_ in self.Surcharges:
            namespaceprefix_ = self.Surcharges_nsprefix_ + ':' if (UseCapturedNS_ and self.Surcharges_nsprefix_) else ''
            Surcharges_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Surcharges', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'TotalPieces' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'TotalPieces')
            if ival_ < 0:
                raise_parse_error(child_, 'requires nonNegativeInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'TotalPieces')
            self.TotalPieces = ival_
            self.TotalPieces_nsprefix_ = child_.prefix
        elif nodeName_ == 'TotalNetCharge':
            obj_ = Money.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TotalNetCharge = obj_
            obj_.original_tagname_ = 'TotalNetCharge'
        elif nodeName_ == 'TotalSurcharges':
            obj_ = Money.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TotalSurcharges = obj_
            obj_.original_tagname_ = 'TotalSurcharges'
        elif nodeName_ == 'Surcharges':
            obj_ = Surcharge.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Surcharges.append(obj_)
            obj_.original_tagname_ = 'Surcharges'
# end class RatedDeliveryDetail


class RedirectToHoldAtLocationRequestDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HoldingLocationId=None, HoldingLocationNumber=None, HoldingLocationContactAndAddress=None, Comments=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.HoldingLocationId = HoldingLocationId
        self.HoldingLocationId_nsprefix_ = None
        self.HoldingLocationNumber = HoldingLocationNumber
        self.HoldingLocationNumber_nsprefix_ = None
        self.HoldingLocationContactAndAddress = HoldingLocationContactAndAddress
        self.HoldingLocationContactAndAddress_nsprefix_ = "ns"
        self.Comments = Comments
        self.Comments_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RedirectToHoldAtLocationRequestDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RedirectToHoldAtLocationRequestDetail.subclass:
            return RedirectToHoldAtLocationRequestDetail.subclass(*args_, **kwargs_)
        else:
            return RedirectToHoldAtLocationRequestDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_HoldingLocationId(self):
        return self.HoldingLocationId
    def set_HoldingLocationId(self, HoldingLocationId):
        self.HoldingLocationId = HoldingLocationId
    def get_HoldingLocationNumber(self):
        return self.HoldingLocationNumber
    def set_HoldingLocationNumber(self, HoldingLocationNumber):
        self.HoldingLocationNumber = HoldingLocationNumber
    def get_HoldingLocationContactAndAddress(self):
        return self.HoldingLocationContactAndAddress
    def set_HoldingLocationContactAndAddress(self, HoldingLocationContactAndAddress):
        self.HoldingLocationContactAndAddress = HoldingLocationContactAndAddress
    def get_Comments(self):
        return self.Comments
    def set_Comments(self, Comments):
        self.Comments = Comments
    def hasContent_(self):
        if (
            self.HoldingLocationId is not None or
            self.HoldingLocationNumber is not None or
            self.HoldingLocationContactAndAddress is not None or
            self.Comments is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RedirectToHoldAtLocationRequestDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RedirectToHoldAtLocationRequestDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RedirectToHoldAtLocationRequestDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RedirectToHoldAtLocationRequestDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RedirectToHoldAtLocationRequestDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RedirectToHoldAtLocationRequestDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RedirectToHoldAtLocationRequestDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.HoldingLocationId is not None:
            namespaceprefix_ = self.HoldingLocationId_nsprefix_ + ':' if (UseCapturedNS_ and self.HoldingLocationId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHoldingLocationId>%s</%sHoldingLocationId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HoldingLocationId), input_name='HoldingLocationId')), namespaceprefix_ , eol_))
        if self.HoldingLocationNumber is not None:
            namespaceprefix_ = self.HoldingLocationNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.HoldingLocationNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHoldingLocationNumber>%s</%sHoldingLocationNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.HoldingLocationNumber, input_name='HoldingLocationNumber'), namespaceprefix_ , eol_))
        if self.HoldingLocationContactAndAddress is not None:
            namespaceprefix_ = self.HoldingLocationContactAndAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.HoldingLocationContactAndAddress_nsprefix_) else ''
            self.HoldingLocationContactAndAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='HoldingLocationContactAndAddress', pretty_print=pretty_print)
        if self.Comments is not None:
            namespaceprefix_ = self.Comments_nsprefix_ + ':' if (UseCapturedNS_ and self.Comments_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sComments>%s</%sComments>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Comments), input_name='Comments')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'HoldingLocationId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HoldingLocationId')
            value_ = self.gds_validate_string(value_, node, 'HoldingLocationId')
            self.HoldingLocationId = value_
            self.HoldingLocationId_nsprefix_ = child_.prefix
        elif nodeName_ == 'HoldingLocationNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'HoldingLocationNumber')
            ival_ = self.gds_validate_integer(ival_, node, 'HoldingLocationNumber')
            self.HoldingLocationNumber = ival_
            self.HoldingLocationNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'HoldingLocationContactAndAddress':
            obj_ = ContactAndAddress.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.HoldingLocationContactAndAddress = obj_
            obj_.original_tagname_ = 'HoldingLocationContactAndAddress'
        elif nodeName_ == 'Comments':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Comments')
            value_ = self.gds_validate_string(value_, node, 'Comments')
            self.Comments = value_
            self.Comments_nsprefix_ = child_.prefix
# end class RedirectToHoldAtLocationRequestDetail


class RerouteDeliveryDetail(GeneratedsSuper):
    """Specifies the details about rerouting a shipment for delivery."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Type=None, TransitTime=None, CommitmentDate=None, CommitmentTime=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Type = Type
        self.validate_RerouteDeliveryType(self.Type)
        self.Type_nsprefix_ = "ns"
        self.TransitTime = TransitTime
        self.validate_TransitTimeType(self.TransitTime)
        self.TransitTime_nsprefix_ = "ns"
        if isinstance(CommitmentDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(CommitmentDate, '%Y-%m-%d').date()
        else:
            initvalue_ = CommitmentDate
        self.CommitmentDate = initvalue_
        self.CommitmentDate_nsprefix_ = None
        self.CommitmentTime = CommitmentTime
        self.CommitmentTime_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RerouteDeliveryDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RerouteDeliveryDetail.subclass:
            return RerouteDeliveryDetail.subclass(*args_, **kwargs_)
        else:
            return RerouteDeliveryDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_TransitTime(self):
        return self.TransitTime
    def set_TransitTime(self, TransitTime):
        self.TransitTime = TransitTime
    def get_CommitmentDate(self):
        return self.CommitmentDate
    def set_CommitmentDate(self, CommitmentDate):
        self.CommitmentDate = CommitmentDate
    def get_CommitmentTime(self):
        return self.CommitmentTime
    def set_CommitmentTime(self, CommitmentTime):
        self.CommitmentTime = CommitmentTime
    def validate_RerouteDeliveryType(self, value):
        result = True
        # Validate type RerouteDeliveryType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['CROSS_COUNTRY_DEFERRED', 'CROSS_COUNTRY_EXPEDITED', 'LOCAL', 'UNDETERMINED']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on RerouteDeliveryType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_TransitTimeType(self, value):
        result = True
        # Validate type TransitTimeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['EIGHTEEN_DAYS', 'EIGHT_DAYS', 'ELEVEN_DAYS', 'FIFTEEN_DAYS', 'FIVE_DAYS', 'FOURTEEN_DAYS', 'FOUR_DAYS', 'NINETEEN_DAYS', 'NINE_DAYS', 'ONE_DAY', 'SEVENTEEN_DAYS', 'SEVEN_DAYS', 'SIXTEEN_DAYS', 'SIX_DAYS', 'TEN_DAYS', 'THIRTEEN_DAYS', 'THREE_DAYS', 'TWELVE_DAYS', 'TWENTY_DAYS', 'TWO_DAYS', 'UNKNOWN']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on TransitTimeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Type is not None or
            self.TransitTime is not None or
            self.CommitmentDate is not None or
            self.CommitmentTime is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RerouteDeliveryDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RerouteDeliveryDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RerouteDeliveryDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RerouteDeliveryDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RerouteDeliveryDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RerouteDeliveryDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RerouteDeliveryDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sType>%s</%sType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Type), input_name='Type')), namespaceprefix_ , eol_))
        if self.TransitTime is not None:
            namespaceprefix_ = self.TransitTime_nsprefix_ + ':' if (UseCapturedNS_ and self.TransitTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTransitTime>%s</%sTransitTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TransitTime), input_name='TransitTime')), namespaceprefix_ , eol_))
        if self.CommitmentDate is not None:
            namespaceprefix_ = self.CommitmentDate_nsprefix_ + ':' if (UseCapturedNS_ and self.CommitmentDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCommitmentDate>%s</%sCommitmentDate>%s' % (namespaceprefix_ , self.gds_format_date(self.CommitmentDate, input_name='CommitmentDate'), namespaceprefix_ , eol_))
        if self.CommitmentTime is not None:
            namespaceprefix_ = self.CommitmentTime_nsprefix_ + ':' if (UseCapturedNS_ and self.CommitmentTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCommitmentTime>%s</%sCommitmentTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CommitmentTime), input_name='CommitmentTime')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Type':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Type')
            value_ = self.gds_validate_string(value_, node, 'Type')
            self.Type = value_
            self.Type_nsprefix_ = child_.prefix
            # validate type RerouteDeliveryType
            self.validate_RerouteDeliveryType(self.Type)
        elif nodeName_ == 'TransitTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TransitTime')
            value_ = self.gds_validate_string(value_, node, 'TransitTime')
            self.TransitTime = value_
            self.TransitTime_nsprefix_ = child_.prefix
            # validate type TransitTimeType
            self.validate_TransitTimeType(self.TransitTime)
        elif nodeName_ == 'CommitmentDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.CommitmentDate = dval_
            self.CommitmentDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'CommitmentTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CommitmentTime')
            value_ = self.gds_validate_string(value_, node, 'CommitmentTime')
            self.CommitmentTime = value_
            self.CommitmentTime_nsprefix_ = child_.prefix
# end class RerouteDeliveryDetail


class ShippingDocumentDispositionDetail(GeneratedsSuper):
    """Each occurrence of this class specifies a particular way in which a kind
    of shipping document is to be produced and provided."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DispositionType=None, Grouping=None, StorageDetail=None, EMailDetail=None, PrintDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DispositionType = DispositionType
        self.validate_ShippingDocumentDispositionType(self.DispositionType)
        self.DispositionType_nsprefix_ = "ns"
        self.Grouping = Grouping
        self.validate_ShippingDocumentGroupingType(self.Grouping)
        self.Grouping_nsprefix_ = "ns"
        self.StorageDetail = StorageDetail
        self.StorageDetail_nsprefix_ = "ns"
        self.EMailDetail = EMailDetail
        self.EMailDetail_nsprefix_ = "ns"
        self.PrintDetail = PrintDetail
        self.PrintDetail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShippingDocumentDispositionDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShippingDocumentDispositionDetail.subclass:
            return ShippingDocumentDispositionDetail.subclass(*args_, **kwargs_)
        else:
            return ShippingDocumentDispositionDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DispositionType(self):
        return self.DispositionType
    def set_DispositionType(self, DispositionType):
        self.DispositionType = DispositionType
    def get_Grouping(self):
        return self.Grouping
    def set_Grouping(self, Grouping):
        self.Grouping = Grouping
    def get_StorageDetail(self):
        return self.StorageDetail
    def set_StorageDetail(self, StorageDetail):
        self.StorageDetail = StorageDetail
    def get_EMailDetail(self):
        return self.EMailDetail
    def set_EMailDetail(self, EMailDetail):
        self.EMailDetail = EMailDetail
    def get_PrintDetail(self):
        return self.PrintDetail
    def set_PrintDetail(self, PrintDetail):
        self.PrintDetail = PrintDetail
    def validate_ShippingDocumentDispositionType(self, value):
        result = True
        # Validate type ShippingDocumentDispositionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['CONFIRMED', 'DEFERRED_QUEUED', 'DEFERRED_RETURNED', 'DEFERRED_STORED', 'EMAILED', 'QUEUED', 'RETURNED', 'STORED']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ShippingDocumentDispositionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ShippingDocumentGroupingType(self, value):
        result = True
        # Validate type ShippingDocumentGroupingType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['CONSOLIDATED_BY_DOCUMENT_TYPE', 'CONSOLIDATED_BY_IMAGE_TYPE', 'INDIVIDUAL']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ShippingDocumentGroupingType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.DispositionType is not None or
            self.Grouping is not None or
            self.StorageDetail is not None or
            self.EMailDetail is not None or
            self.PrintDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShippingDocumentDispositionDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShippingDocumentDispositionDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShippingDocumentDispositionDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShippingDocumentDispositionDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShippingDocumentDispositionDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShippingDocumentDispositionDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShippingDocumentDispositionDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DispositionType is not None:
            namespaceprefix_ = self.DispositionType_nsprefix_ + ':' if (UseCapturedNS_ and self.DispositionType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDispositionType>%s</%sDispositionType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DispositionType), input_name='DispositionType')), namespaceprefix_ , eol_))
        if self.Grouping is not None:
            namespaceprefix_ = self.Grouping_nsprefix_ + ':' if (UseCapturedNS_ and self.Grouping_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGrouping>%s</%sGrouping>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Grouping), input_name='Grouping')), namespaceprefix_ , eol_))
        if self.StorageDetail is not None:
            namespaceprefix_ = self.StorageDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.StorageDetail_nsprefix_) else ''
            self.StorageDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='StorageDetail', pretty_print=pretty_print)
        if self.EMailDetail is not None:
            namespaceprefix_ = self.EMailDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.EMailDetail_nsprefix_) else ''
            self.EMailDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EMailDetail', pretty_print=pretty_print)
        if self.PrintDetail is not None:
            namespaceprefix_ = self.PrintDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.PrintDetail_nsprefix_) else ''
            self.PrintDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PrintDetail', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DispositionType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DispositionType')
            value_ = self.gds_validate_string(value_, node, 'DispositionType')
            self.DispositionType = value_
            self.DispositionType_nsprefix_ = child_.prefix
            # validate type ShippingDocumentDispositionType
            self.validate_ShippingDocumentDispositionType(self.DispositionType)
        elif nodeName_ == 'Grouping':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Grouping')
            value_ = self.gds_validate_string(value_, node, 'Grouping')
            self.Grouping = value_
            self.Grouping_nsprefix_ = child_.prefix
            # validate type ShippingDocumentGroupingType
            self.validate_ShippingDocumentGroupingType(self.Grouping)
        elif nodeName_ == 'StorageDetail':
            obj_ = ShippingDocumentStorageDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.StorageDetail = obj_
            obj_.original_tagname_ = 'StorageDetail'
        elif nodeName_ == 'EMailDetail':
            obj_ = ShippingDocumentEMailDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EMailDetail = obj_
            obj_.original_tagname_ = 'EMailDetail'
        elif nodeName_ == 'PrintDetail':
            obj_ = ShippingDocumentPrintDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PrintDetail = obj_
            obj_.original_tagname_ = 'PrintDetail'
# end class ShippingDocumentDispositionDetail


class ShippingDocumentEMailDetail(GeneratedsSuper):
    """Specifies how to e-mail shipping documents."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, EMailRecipients=None, Grouping=None, Localization=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if EMailRecipients is None:
            self.EMailRecipients = []
        else:
            self.EMailRecipients = EMailRecipients
        self.EMailRecipients_nsprefix_ = "ns"
        self.Grouping = Grouping
        self.validate_ShippingDocumentEMailGroupingType(self.Grouping)
        self.Grouping_nsprefix_ = "ns"
        self.Localization = Localization
        self.Localization_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShippingDocumentEMailDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShippingDocumentEMailDetail.subclass:
            return ShippingDocumentEMailDetail.subclass(*args_, **kwargs_)
        else:
            return ShippingDocumentEMailDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_EMailRecipients(self):
        return self.EMailRecipients
    def set_EMailRecipients(self, EMailRecipients):
        self.EMailRecipients = EMailRecipients
    def add_EMailRecipients(self, value):
        self.EMailRecipients.append(value)
    def insert_EMailRecipients_at(self, index, value):
        self.EMailRecipients.insert(index, value)
    def replace_EMailRecipients_at(self, index, value):
        self.EMailRecipients[index] = value
    def get_Grouping(self):
        return self.Grouping
    def set_Grouping(self, Grouping):
        self.Grouping = Grouping
    def get_Localization(self):
        return self.Localization
    def set_Localization(self, Localization):
        self.Localization = Localization
    def validate_ShippingDocumentEMailGroupingType(self, value):
        result = True
        # Validate type ShippingDocumentEMailGroupingType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['BY_RECIPIENT', 'NONE']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ShippingDocumentEMailGroupingType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.EMailRecipients or
            self.Grouping is not None or
            self.Localization is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShippingDocumentEMailDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShippingDocumentEMailDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShippingDocumentEMailDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShippingDocumentEMailDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShippingDocumentEMailDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShippingDocumentEMailDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShippingDocumentEMailDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for EMailRecipients_ in self.EMailRecipients:
            namespaceprefix_ = self.EMailRecipients_nsprefix_ + ':' if (UseCapturedNS_ and self.EMailRecipients_nsprefix_) else ''
            EMailRecipients_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EMailRecipients', pretty_print=pretty_print)
        if self.Grouping is not None:
            namespaceprefix_ = self.Grouping_nsprefix_ + ':' if (UseCapturedNS_ and self.Grouping_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGrouping>%s</%sGrouping>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Grouping), input_name='Grouping')), namespaceprefix_ , eol_))
        if self.Localization is not None:
            namespaceprefix_ = self.Localization_nsprefix_ + ':' if (UseCapturedNS_ and self.Localization_nsprefix_) else ''
            self.Localization.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Localization', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'EMailRecipients':
            obj_ = ShippingDocumentEMailRecipient.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EMailRecipients.append(obj_)
            obj_.original_tagname_ = 'EMailRecipients'
        elif nodeName_ == 'Grouping':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Grouping')
            value_ = self.gds_validate_string(value_, node, 'Grouping')
            self.Grouping = value_
            self.Grouping_nsprefix_ = child_.prefix
            # validate type ShippingDocumentEMailGroupingType
            self.validate_ShippingDocumentEMailGroupingType(self.Grouping)
        elif nodeName_ == 'Localization':
            obj_ = Localization.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Localization = obj_
            obj_.original_tagname_ = 'Localization'
# end class ShippingDocumentEMailDetail


class ShippingDocumentEMailRecipient(GeneratedsSuper):
    """Specifies an individual recipient of e-mailed shipping document(s)."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, RecipientType=None, Address=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.RecipientType = RecipientType
        self.validate_EMailNotificationRecipientType(self.RecipientType)
        self.RecipientType_nsprefix_ = "ns"
        self.Address = Address
        self.Address_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShippingDocumentEMailRecipient)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShippingDocumentEMailRecipient.subclass:
            return ShippingDocumentEMailRecipient.subclass(*args_, **kwargs_)
        else:
            return ShippingDocumentEMailRecipient(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_RecipientType(self):
        return self.RecipientType
    def set_RecipientType(self, RecipientType):
        self.RecipientType = RecipientType
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def validate_EMailNotificationRecipientType(self, value):
        result = True
        # Validate type EMailNotificationRecipientType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['BROKER', 'OTHER', 'RECIPIENT', 'SHIPPER', 'THIRD_PARTY']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on EMailNotificationRecipientType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.RecipientType is not None or
            self.Address is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShippingDocumentEMailRecipient', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShippingDocumentEMailRecipient')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShippingDocumentEMailRecipient':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShippingDocumentEMailRecipient')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShippingDocumentEMailRecipient', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShippingDocumentEMailRecipient'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShippingDocumentEMailRecipient', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.RecipientType is not None:
            namespaceprefix_ = self.RecipientType_nsprefix_ + ':' if (UseCapturedNS_ and self.RecipientType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRecipientType>%s</%sRecipientType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.RecipientType), input_name='RecipientType')), namespaceprefix_ , eol_))
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAddress>%s</%sAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Address), input_name='Address')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'RecipientType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RecipientType')
            value_ = self.gds_validate_string(value_, node, 'RecipientType')
            self.RecipientType = value_
            self.RecipientType_nsprefix_ = child_.prefix
            # validate type EMailNotificationRecipientType
            self.validate_EMailNotificationRecipientType(self.RecipientType)
        elif nodeName_ == 'Address':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Address')
            value_ = self.gds_validate_string(value_, node, 'Address')
            self.Address = value_
            self.Address_nsprefix_ = child_.prefix
# end class ShippingDocumentEMailRecipient


class ShippingDocumentFormat(GeneratedsSuper):
    """Specifies characteristics of a shipping document to be produced."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Dispositions=None, TopOfPageOffset=None, ImageType=None, StockType=None, ProvideInstructions=None, OptionsRequested=None, Localization=None, CustomDocumentIdentifier=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Dispositions is None:
            self.Dispositions = []
        else:
            self.Dispositions = Dispositions
        self.Dispositions_nsprefix_ = "ns"
        self.TopOfPageOffset = TopOfPageOffset
        self.TopOfPageOffset_nsprefix_ = "ns"
        self.ImageType = ImageType
        self.validate_ShippingDocumentImageType(self.ImageType)
        self.ImageType_nsprefix_ = "ns"
        self.StockType = StockType
        self.validate_ShippingDocumentStockType(self.StockType)
        self.StockType_nsprefix_ = "ns"
        self.ProvideInstructions = ProvideInstructions
        self.ProvideInstructions_nsprefix_ = None
        self.OptionsRequested = OptionsRequested
        self.OptionsRequested_nsprefix_ = "ns"
        self.Localization = Localization
        self.Localization_nsprefix_ = "ns"
        self.CustomDocumentIdentifier = CustomDocumentIdentifier
        self.CustomDocumentIdentifier_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShippingDocumentFormat)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShippingDocumentFormat.subclass:
            return ShippingDocumentFormat.subclass(*args_, **kwargs_)
        else:
            return ShippingDocumentFormat(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Dispositions(self):
        return self.Dispositions
    def set_Dispositions(self, Dispositions):
        self.Dispositions = Dispositions
    def add_Dispositions(self, value):
        self.Dispositions.append(value)
    def insert_Dispositions_at(self, index, value):
        self.Dispositions.insert(index, value)
    def replace_Dispositions_at(self, index, value):
        self.Dispositions[index] = value
    def get_TopOfPageOffset(self):
        return self.TopOfPageOffset
    def set_TopOfPageOffset(self, TopOfPageOffset):
        self.TopOfPageOffset = TopOfPageOffset
    def get_ImageType(self):
        return self.ImageType
    def set_ImageType(self, ImageType):
        self.ImageType = ImageType
    def get_StockType(self):
        return self.StockType
    def set_StockType(self, StockType):
        self.StockType = StockType
    def get_ProvideInstructions(self):
        return self.ProvideInstructions
    def set_ProvideInstructions(self, ProvideInstructions):
        self.ProvideInstructions = ProvideInstructions
    def get_OptionsRequested(self):
        return self.OptionsRequested
    def set_OptionsRequested(self, OptionsRequested):
        self.OptionsRequested = OptionsRequested
    def get_Localization(self):
        return self.Localization
    def set_Localization(self, Localization):
        self.Localization = Localization
    def get_CustomDocumentIdentifier(self):
        return self.CustomDocumentIdentifier
    def set_CustomDocumentIdentifier(self, CustomDocumentIdentifier):
        self.CustomDocumentIdentifier = CustomDocumentIdentifier
    def validate_ShippingDocumentImageType(self, value):
        result = True
        # Validate type ShippingDocumentImageType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['DIB', 'DOC', 'DPL', 'EPL2', 'GIF', 'PDF', 'PNG', 'RTF', 'TEXT', 'ZPLII']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ShippingDocumentImageType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ShippingDocumentStockType(self, value):
        result = True
        # Validate type ShippingDocumentStockType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['OP_900_LG', 'OP_900_LG_B', 'OP_900_LL', 'OP_900_LL_B', 'OP_950', 'PAPER_4X6', 'PAPER_4_PER_PAGE_PORTRAIT', 'PAPER_LETTER', 'STOCK_4X6', 'STOCK_4X6.75_LEADING_DOC_TAB', 'STOCK_4X6.75_TRAILING_DOC_TAB', 'STOCK_4X8', 'STOCK_4X9_LEADING_DOC_TAB', 'STOCK_4X9_TRAILING_DOC_TAB']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ShippingDocumentStockType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Dispositions or
            self.TopOfPageOffset is not None or
            self.ImageType is not None or
            self.StockType is not None or
            self.ProvideInstructions is not None or
            self.OptionsRequested is not None or
            self.Localization is not None or
            self.CustomDocumentIdentifier is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShippingDocumentFormat', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShippingDocumentFormat')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShippingDocumentFormat':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShippingDocumentFormat')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShippingDocumentFormat', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShippingDocumentFormat'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShippingDocumentFormat', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Dispositions_ in self.Dispositions:
            namespaceprefix_ = self.Dispositions_nsprefix_ + ':' if (UseCapturedNS_ and self.Dispositions_nsprefix_) else ''
            Dispositions_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Dispositions', pretty_print=pretty_print)
        if self.TopOfPageOffset is not None:
            namespaceprefix_ = self.TopOfPageOffset_nsprefix_ + ':' if (UseCapturedNS_ and self.TopOfPageOffset_nsprefix_) else ''
            self.TopOfPageOffset.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TopOfPageOffset', pretty_print=pretty_print)
        if self.ImageType is not None:
            namespaceprefix_ = self.ImageType_nsprefix_ + ':' if (UseCapturedNS_ and self.ImageType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sImageType>%s</%sImageType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ImageType), input_name='ImageType')), namespaceprefix_ , eol_))
        if self.StockType is not None:
            namespaceprefix_ = self.StockType_nsprefix_ + ':' if (UseCapturedNS_ and self.StockType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStockType>%s</%sStockType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.StockType), input_name='StockType')), namespaceprefix_ , eol_))
        if self.ProvideInstructions is not None:
            namespaceprefix_ = self.ProvideInstructions_nsprefix_ + ':' if (UseCapturedNS_ and self.ProvideInstructions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProvideInstructions>%s</%sProvideInstructions>%s' % (namespaceprefix_ , self.gds_format_boolean(self.ProvideInstructions, input_name='ProvideInstructions'), namespaceprefix_ , eol_))
        if self.OptionsRequested is not None:
            namespaceprefix_ = self.OptionsRequested_nsprefix_ + ':' if (UseCapturedNS_ and self.OptionsRequested_nsprefix_) else ''
            self.OptionsRequested.export(outfile, level, namespaceprefix_, namespacedef_='', name_='OptionsRequested', pretty_print=pretty_print)
        if self.Localization is not None:
            namespaceprefix_ = self.Localization_nsprefix_ + ':' if (UseCapturedNS_ and self.Localization_nsprefix_) else ''
            self.Localization.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Localization', pretty_print=pretty_print)
        if self.CustomDocumentIdentifier is not None:
            namespaceprefix_ = self.CustomDocumentIdentifier_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomDocumentIdentifier_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustomDocumentIdentifier>%s</%sCustomDocumentIdentifier>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CustomDocumentIdentifier), input_name='CustomDocumentIdentifier')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Dispositions':
            obj_ = ShippingDocumentDispositionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Dispositions.append(obj_)
            obj_.original_tagname_ = 'Dispositions'
        elif nodeName_ == 'TopOfPageOffset':
            obj_ = LinearMeasure.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TopOfPageOffset = obj_
            obj_.original_tagname_ = 'TopOfPageOffset'
        elif nodeName_ == 'ImageType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ImageType')
            value_ = self.gds_validate_string(value_, node, 'ImageType')
            self.ImageType = value_
            self.ImageType_nsprefix_ = child_.prefix
            # validate type ShippingDocumentImageType
            self.validate_ShippingDocumentImageType(self.ImageType)
        elif nodeName_ == 'StockType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'StockType')
            value_ = self.gds_validate_string(value_, node, 'StockType')
            self.StockType = value_
            self.StockType_nsprefix_ = child_.prefix
            # validate type ShippingDocumentStockType
            self.validate_ShippingDocumentStockType(self.StockType)
        elif nodeName_ == 'ProvideInstructions':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'ProvideInstructions')
            ival_ = self.gds_validate_boolean(ival_, node, 'ProvideInstructions')
            self.ProvideInstructions = ival_
            self.ProvideInstructions_nsprefix_ = child_.prefix
        elif nodeName_ == 'OptionsRequested':
            obj_ = DocumentFormatOptionsRequested.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.OptionsRequested = obj_
            obj_.original_tagname_ = 'OptionsRequested'
        elif nodeName_ == 'Localization':
            obj_ = Localization.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Localization = obj_
            obj_.original_tagname_ = 'Localization'
        elif nodeName_ == 'CustomDocumentIdentifier':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CustomDocumentIdentifier')
            value_ = self.gds_validate_string(value_, node, 'CustomDocumentIdentifier')
            self.CustomDocumentIdentifier = value_
            self.CustomDocumentIdentifier_nsprefix_ = child_.prefix
# end class ShippingDocumentFormat


class ShippingDocumentPrintDetail(GeneratedsSuper):
    """Specifies printing options for a shipping document."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PrinterId=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PrinterId = PrinterId
        self.PrinterId_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShippingDocumentPrintDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShippingDocumentPrintDetail.subclass:
            return ShippingDocumentPrintDetail.subclass(*args_, **kwargs_)
        else:
            return ShippingDocumentPrintDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PrinterId(self):
        return self.PrinterId
    def set_PrinterId(self, PrinterId):
        self.PrinterId = PrinterId
    def hasContent_(self):
        if (
            self.PrinterId is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShippingDocumentPrintDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShippingDocumentPrintDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShippingDocumentPrintDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShippingDocumentPrintDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShippingDocumentPrintDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShippingDocumentPrintDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShippingDocumentPrintDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PrinterId is not None:
            namespaceprefix_ = self.PrinterId_nsprefix_ + ':' if (UseCapturedNS_ and self.PrinterId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPrinterId>%s</%sPrinterId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PrinterId), input_name='PrinterId')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'PrinterId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PrinterId')
            value_ = self.gds_validate_string(value_, node, 'PrinterId')
            self.PrinterId = value_
            self.PrinterId_nsprefix_ = child_.prefix
# end class ShippingDocumentPrintDetail


class ShippingDocumentStorageDetail(GeneratedsSuper):
    """Specifies how to store shipping documents."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, FilePath=None, FileNaming=None, FileSuffix=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.FilePath = FilePath
        self.FilePath_nsprefix_ = None
        self.FileNaming = FileNaming
        self.validate_ShippingDocumentNamingType(self.FileNaming)
        self.FileNaming_nsprefix_ = "ns"
        self.FileSuffix = FileSuffix
        self.FileSuffix_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShippingDocumentStorageDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShippingDocumentStorageDetail.subclass:
            return ShippingDocumentStorageDetail.subclass(*args_, **kwargs_)
        else:
            return ShippingDocumentStorageDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_FilePath(self):
        return self.FilePath
    def set_FilePath(self, FilePath):
        self.FilePath = FilePath
    def get_FileNaming(self):
        return self.FileNaming
    def set_FileNaming(self, FileNaming):
        self.FileNaming = FileNaming
    def get_FileSuffix(self):
        return self.FileSuffix
    def set_FileSuffix(self, FileSuffix):
        self.FileSuffix = FileSuffix
    def validate_ShippingDocumentNamingType(self, value):
        result = True
        # Validate type ShippingDocumentNamingType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FAST', 'LEGACY_FXRS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ShippingDocumentNamingType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.FilePath is not None or
            self.FileNaming is not None or
            self.FileSuffix is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShippingDocumentStorageDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShippingDocumentStorageDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShippingDocumentStorageDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShippingDocumentStorageDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShippingDocumentStorageDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShippingDocumentStorageDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShippingDocumentStorageDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.FilePath is not None:
            namespaceprefix_ = self.FilePath_nsprefix_ + ':' if (UseCapturedNS_ and self.FilePath_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFilePath>%s</%sFilePath>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FilePath), input_name='FilePath')), namespaceprefix_ , eol_))
        if self.FileNaming is not None:
            namespaceprefix_ = self.FileNaming_nsprefix_ + ':' if (UseCapturedNS_ and self.FileNaming_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFileNaming>%s</%sFileNaming>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FileNaming), input_name='FileNaming')), namespaceprefix_ , eol_))
        if self.FileSuffix is not None:
            namespaceprefix_ = self.FileSuffix_nsprefix_ + ':' if (UseCapturedNS_ and self.FileSuffix_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFileSuffix>%s</%sFileSuffix>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FileSuffix), input_name='FileSuffix')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'FilePath':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FilePath')
            value_ = self.gds_validate_string(value_, node, 'FilePath')
            self.FilePath = value_
            self.FilePath_nsprefix_ = child_.prefix
        elif nodeName_ == 'FileNaming':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FileNaming')
            value_ = self.gds_validate_string(value_, node, 'FileNaming')
            self.FileNaming = value_
            self.FileNaming_nsprefix_ = child_.prefix
            # validate type ShippingDocumentNamingType
            self.validate_ShippingDocumentNamingType(self.FileNaming)
        elif nodeName_ == 'FileSuffix':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FileSuffix')
            value_ = self.gds_validate_string(value_, node, 'FileSuffix')
            self.FileSuffix = value_
            self.FileSuffix_nsprefix_ = child_.prefix
# end class ShippingDocumentStorageDetail


class SignatureReleaseDocumentDetail(GeneratedsSuper):
    """Specifies the details needed to produce a door tag."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Format=None, Id=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Format = Format
        self.Format_nsprefix_ = "ns"
        self.Id = Id
        self.Id_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SignatureReleaseDocumentDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SignatureReleaseDocumentDetail.subclass:
            return SignatureReleaseDocumentDetail.subclass(*args_, **kwargs_)
        else:
            return SignatureReleaseDocumentDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Format(self):
        return self.Format
    def set_Format(self, Format):
        self.Format = Format
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def hasContent_(self):
        if (
            self.Format is not None or
            self.Id is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SignatureReleaseDocumentDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SignatureReleaseDocumentDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SignatureReleaseDocumentDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SignatureReleaseDocumentDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SignatureReleaseDocumentDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SignatureReleaseDocumentDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SignatureReleaseDocumentDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Format is not None:
            namespaceprefix_ = self.Format_nsprefix_ + ':' if (UseCapturedNS_ and self.Format_nsprefix_) else ''
            self.Format.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Format', pretty_print=pretty_print)
        if self.Id is not None:
            namespaceprefix_ = self.Id_nsprefix_ + ':' if (UseCapturedNS_ and self.Id_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sId>%s</%sId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Id), input_name='Id')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Format':
            obj_ = ShippingDocumentFormat.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Format = obj_
            obj_.original_tagname_ = 'Format'
        elif nodeName_ == 'Id':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Id')
            value_ = self.gds_validate_string(value_, node, 'Id')
            self.Id = value_
            self.Id_nsprefix_ = child_.prefix
# end class SignatureReleaseDocumentDetail


class Surcharge(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, SurchargeType=None, Level=None, Description=None, Amount=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.SurchargeType = SurchargeType
        self.validate_SurchargeType(self.SurchargeType)
        self.SurchargeType_nsprefix_ = "ns"
        self.Level = Level
        self.validate_SurchargeLevelType(self.Level)
        self.Level_nsprefix_ = "ns"
        self.Description = Description
        self.Description_nsprefix_ = None
        self.Amount = Amount
        self.Amount_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Surcharge)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Surcharge.subclass:
            return Surcharge.subclass(*args_, **kwargs_)
        else:
            return Surcharge(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_SurchargeType(self):
        return self.SurchargeType
    def set_SurchargeType(self, SurchargeType):
        self.SurchargeType = SurchargeType
    def get_Level(self):
        return self.Level
    def set_Level(self, Level):
        self.Level = Level
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def get_Amount(self):
        return self.Amount
    def set_Amount(self, Amount):
        self.Amount = Amount
    def validate_SurchargeType(self, value):
        result = True
        # Validate type SurchargeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ADDITIONAL_HANDLING', 'ANCILLARY_FEE', 'APPOINTMENT_DELIVERY', 'BLIND_SHIPMENT', 'BROKER_SELECT_OPTION', 'CANADIAN_DESTINATION', 'CHARGEABLE_PALLET_WEIGHT', 'CLEARANCE_ENTRY_FEE', 'COD', 'CUT_FLOWERS', 'DANGEROUS_GOODS', 'DELIVERY_AREA', 'DELIVERY_CONFIRMATION', 'DELIVERY_ON_INVOICE_ACCEPTANCE', 'DETENTION', 'DOCUMENTATION_FEE', 'DRY_ICE', 'EMAIL_LABEL', 'EUROPE_FIRST', 'EXCESS_VALUE', 'EXCLUSIVE_USE', 'EXHIBITION', 'EXPEDITED', 'EXPORT', 'EXTRA_LABOR', 'EXTRA_SURFACE_HANDLING_CHARGE', 'EXTREME_LENGTH', 'FEDEX_INTRACOUNTRY_FEES', 'FEDEX_TAG', 'FICE', 'FLATBED', 'FREIGHT_GUARANTEE', 'FREIGHT_ON_VALUE', 'FREIGHT_TO_COLLECT', 'FUEL', 'HOLD_AT_LOCATION', 'HOLIDAY_DELIVERY', 'HOLIDAY_GUARANTEE', 'HOME_DELIVERY_APPOINTMENT', 'HOME_DELIVERY_DATE_CERTAIN', 'HOME_DELIVERY_EVENING', 'INSIDE_DELIVERY', 'INSIDE_PICKUP', 'INSURED_VALUE', 'INTERHAWAII', 'LIFTGATE_DELIVERY', 'LIFTGATE_PICKUP', 'LIMITED_ACCESS_DELIVERY', 'LIMITED_ACCESS_PICKUP', 'MARKING_OR_TAGGING', 'METRO_DELIVERY', 'METRO_PICKUP', 'NON_BUSINESS_TIME', 'NON_MACHINABLE', 'OFFSHORE', 'ON_CALL_PICKUP', 'OTHER', 'OUT_OF_DELIVERY_AREA', 'OUT_OF_PICKUP_AREA', 'OVERSIZE', 'OVER_DIMENSION', 'PALLETS_PROVIDED', 'PALLET_SHRINKWRAP', 'PERMIT', 'PIECE_COUNT_VERIFICATION', 'PORT', 'PRE_DELIVERY_NOTIFICATION', 'PRIORITY_ALERT', 'PROTECTION_FROM_FREEZING', 'REGIONAL_MALL_DELIVERY', 'REGIONAL_MALL_PICKUP', 'REROUTE', 'RESCHEDULE', 'RESIDENTIAL_DELIVERY', 'RESIDENTIAL_PICKUP', 'RETURN_LABEL', 'SATURDAY_DELIVERY', 'SATURDAY_PICKUP', 'SHIPMENT_ASSEMBLY', 'SIGNATURE_OPTION', 'SORT_AND_SEGREGATE', 'SPECIAL_DELIVERY', 'SPECIAL_EQUIPMENT', 'STORAGE', 'SUNDAY_DELIVERY', 'TARP', 'THIRD_PARTY_CONSIGNEE', 'TRANSMART_SERVICE_FEE', 'USPS', 'WEIGHING']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on SurchargeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_SurchargeLevelType(self, value):
        result = True
        # Validate type SurchargeLevelType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['PACKAGE', 'SHIPMENT']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on SurchargeLevelType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.SurchargeType is not None or
            self.Level is not None or
            self.Description is not None or
            self.Amount is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Surcharge', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Surcharge')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Surcharge':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Surcharge')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Surcharge', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Surcharge'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Surcharge', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.SurchargeType is not None:
            namespaceprefix_ = self.SurchargeType_nsprefix_ + ':' if (UseCapturedNS_ and self.SurchargeType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSurchargeType>%s</%sSurchargeType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SurchargeType), input_name='SurchargeType')), namespaceprefix_ , eol_))
        if self.Level is not None:
            namespaceprefix_ = self.Level_nsprefix_ + ':' if (UseCapturedNS_ and self.Level_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLevel>%s</%sLevel>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Level), input_name='Level')), namespaceprefix_ , eol_))
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
        if self.Amount is not None:
            namespaceprefix_ = self.Amount_nsprefix_ + ':' if (UseCapturedNS_ and self.Amount_nsprefix_) else ''
            self.Amount.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Amount', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'SurchargeType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SurchargeType')
            value_ = self.gds_validate_string(value_, node, 'SurchargeType')
            self.SurchargeType = value_
            self.SurchargeType_nsprefix_ = child_.prefix
            # validate type SurchargeType
            self.validate_SurchargeType(self.SurchargeType)
        elif nodeName_ == 'Level':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Level')
            value_ = self.gds_validate_string(value_, node, 'Level')
            self.Level = value_
            self.Level_nsprefix_ = child_.prefix
            # validate type SurchargeLevelType
            self.validate_SurchargeLevelType(self.Level)
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
        elif nodeName_ == 'Amount':
            obj_ = Money.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Amount = obj_
            obj_.original_tagname_ = 'Amount'
# end class Surcharge


class TaxpayerIdentification(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TinType=None, Number=None, Usage=None, EffectiveDate=None, ExpirationDate=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.TinType = TinType
        self.validate_TinType(self.TinType)
        self.TinType_nsprefix_ = "ns"
        self.Number = Number
        self.Number_nsprefix_ = None
        self.Usage = Usage
        self.Usage_nsprefix_ = None
        if isinstance(EffectiveDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(EffectiveDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = EffectiveDate
        self.EffectiveDate = initvalue_
        self.EffectiveDate_nsprefix_ = None
        if isinstance(ExpirationDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ExpirationDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = ExpirationDate
        self.ExpirationDate = initvalue_
        self.ExpirationDate_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TaxpayerIdentification)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TaxpayerIdentification.subclass:
            return TaxpayerIdentification.subclass(*args_, **kwargs_)
        else:
            return TaxpayerIdentification(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_TinType(self):
        return self.TinType
    def set_TinType(self, TinType):
        self.TinType = TinType
    def get_Number(self):
        return self.Number
    def set_Number(self, Number):
        self.Number = Number
    def get_Usage(self):
        return self.Usage
    def set_Usage(self, Usage):
        self.Usage = Usage
    def get_EffectiveDate(self):
        return self.EffectiveDate
    def set_EffectiveDate(self, EffectiveDate):
        self.EffectiveDate = EffectiveDate
    def get_ExpirationDate(self):
        return self.ExpirationDate
    def set_ExpirationDate(self, ExpirationDate):
        self.ExpirationDate = ExpirationDate
    def validate_TinType(self, value):
        result = True
        # Validate type TinType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['BUSINESS_NATIONAL', 'BUSINESS_STATE', 'BUSINESS_UNION', 'PERSONAL_NATIONAL', 'PERSONAL_STATE']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on TinType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.TinType is not None or
            self.Number is not None or
            self.Usage is not None or
            self.EffectiveDate is not None or
            self.ExpirationDate is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TaxpayerIdentification', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TaxpayerIdentification')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TaxpayerIdentification':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TaxpayerIdentification')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TaxpayerIdentification', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TaxpayerIdentification'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TaxpayerIdentification', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.TinType is not None:
            namespaceprefix_ = self.TinType_nsprefix_ + ':' if (UseCapturedNS_ and self.TinType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTinType>%s</%sTinType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TinType), input_name='TinType')), namespaceprefix_ , eol_))
        if self.Number is not None:
            namespaceprefix_ = self.Number_nsprefix_ + ':' if (UseCapturedNS_ and self.Number_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumber>%s</%sNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Number), input_name='Number')), namespaceprefix_ , eol_))
        if self.Usage is not None:
            namespaceprefix_ = self.Usage_nsprefix_ + ':' if (UseCapturedNS_ and self.Usage_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUsage>%s</%sUsage>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Usage), input_name='Usage')), namespaceprefix_ , eol_))
        if self.EffectiveDate is not None:
            namespaceprefix_ = self.EffectiveDate_nsprefix_ + ':' if (UseCapturedNS_ and self.EffectiveDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEffectiveDate>%s</%sEffectiveDate>%s' % (namespaceprefix_ , self.gds_format_datetime(self.EffectiveDate, input_name='EffectiveDate'), namespaceprefix_ , eol_))
        if self.ExpirationDate is not None:
            namespaceprefix_ = self.ExpirationDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ExpirationDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExpirationDate>%s</%sExpirationDate>%s' % (namespaceprefix_ , self.gds_format_datetime(self.ExpirationDate, input_name='ExpirationDate'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'TinType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TinType')
            value_ = self.gds_validate_string(value_, node, 'TinType')
            self.TinType = value_
            self.TinType_nsprefix_ = child_.prefix
            # validate type TinType
            self.validate_TinType(self.TinType)
        elif nodeName_ == 'Number':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Number')
            value_ = self.gds_validate_string(value_, node, 'Number')
            self.Number = value_
            self.Number_nsprefix_ = child_.prefix
        elif nodeName_ == 'Usage':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Usage')
            value_ = self.gds_validate_string(value_, node, 'Usage')
            self.Usage = value_
            self.Usage_nsprefix_ = child_.prefix
        elif nodeName_ == 'EffectiveDate':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.EffectiveDate = dval_
            self.EffectiveDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'ExpirationDate':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.ExpirationDate = dval_
            self.ExpirationDate_nsprefix_ = child_.prefix
# end class TaxpayerIdentification


class TrackingId(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TrackingIdType=None, FormId=None, UspsApplicationId=None, TrackingNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.TrackingIdType = TrackingIdType
        self.validate_TrackingIdType(self.TrackingIdType)
        self.TrackingIdType_nsprefix_ = "ns"
        self.FormId = FormId
        self.FormId_nsprefix_ = None
        self.UspsApplicationId = UspsApplicationId
        self.UspsApplicationId_nsprefix_ = None
        self.TrackingNumber = TrackingNumber
        self.TrackingNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TrackingId)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TrackingId.subclass:
            return TrackingId.subclass(*args_, **kwargs_)
        else:
            return TrackingId(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_TrackingIdType(self):
        return self.TrackingIdType
    def set_TrackingIdType(self, TrackingIdType):
        self.TrackingIdType = TrackingIdType
    def get_FormId(self):
        return self.FormId
    def set_FormId(self, FormId):
        self.FormId = FormId
    def get_UspsApplicationId(self):
        return self.UspsApplicationId
    def set_UspsApplicationId(self, UspsApplicationId):
        self.UspsApplicationId = UspsApplicationId
    def get_TrackingNumber(self):
        return self.TrackingNumber
    def set_TrackingNumber(self, TrackingNumber):
        self.TrackingNumber = TrackingNumber
    def validate_TrackingIdType(self, value):
        result = True
        # Validate type TrackingIdType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['EXPRESS', 'FEDEX', 'FREIGHT', 'GROUND', 'INTERNAL', 'UNKNOWN', 'USPS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on TrackingIdType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.TrackingIdType is not None or
            self.FormId is not None or
            self.UspsApplicationId is not None or
            self.TrackingNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackingId', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TrackingId')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TrackingId':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TrackingId')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TrackingId', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TrackingId'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackingId', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.TrackingIdType is not None:
            namespaceprefix_ = self.TrackingIdType_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackingIdType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTrackingIdType>%s</%sTrackingIdType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TrackingIdType), input_name='TrackingIdType')), namespaceprefix_ , eol_))
        if self.FormId is not None:
            namespaceprefix_ = self.FormId_nsprefix_ + ':' if (UseCapturedNS_ and self.FormId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFormId>%s</%sFormId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FormId), input_name='FormId')), namespaceprefix_ , eol_))
        if self.UspsApplicationId is not None:
            namespaceprefix_ = self.UspsApplicationId_nsprefix_ + ':' if (UseCapturedNS_ and self.UspsApplicationId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUspsApplicationId>%s</%sUspsApplicationId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UspsApplicationId), input_name='UspsApplicationId')), namespaceprefix_ , eol_))
        if self.TrackingNumber is not None:
            namespaceprefix_ = self.TrackingNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackingNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTrackingNumber>%s</%sTrackingNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TrackingNumber), input_name='TrackingNumber')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'TrackingIdType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TrackingIdType')
            value_ = self.gds_validate_string(value_, node, 'TrackingIdType')
            self.TrackingIdType = value_
            self.TrackingIdType_nsprefix_ = child_.prefix
            # validate type TrackingIdType
            self.validate_TrackingIdType(self.TrackingIdType)
        elif nodeName_ == 'FormId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FormId')
            value_ = self.gds_validate_string(value_, node, 'FormId')
            self.FormId = value_
            self.FormId_nsprefix_ = child_.prefix
        elif nodeName_ == 'UspsApplicationId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UspsApplicationId')
            value_ = self.gds_validate_string(value_, node, 'UspsApplicationId')
            self.UspsApplicationId = value_
            self.UspsApplicationId_nsprefix_ = child_.prefix
        elif nodeName_ == 'TrackingNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TrackingNumber')
            value_ = self.gds_validate_string(value_, node, 'TrackingNumber')
            self.TrackingNumber = value_
            self.TrackingNumber_nsprefix_ = child_.prefix
# end class TrackingId


class TransactionDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CustomerTransactionId=None, Localization=None, InternalTransactionId=None, Tracing=None, SourceFormat=None, Environment=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CustomerTransactionId = CustomerTransactionId
        self.CustomerTransactionId_nsprefix_ = None
        self.Localization = Localization
        self.Localization_nsprefix_ = "ns"
        self.InternalTransactionId = InternalTransactionId
        self.InternalTransactionId_nsprefix_ = None
        self.Tracing = Tracing
        self.Tracing_nsprefix_ = None
        self.SourceFormat = SourceFormat
        self.validate_TransactionSourceFormat(self.SourceFormat)
        self.SourceFormat_nsprefix_ = "ns"
        self.Environment = Environment
        self.validate_WebServiceEnvironment(self.Environment)
        self.Environment_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TransactionDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TransactionDetail.subclass:
            return TransactionDetail.subclass(*args_, **kwargs_)
        else:
            return TransactionDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CustomerTransactionId(self):
        return self.CustomerTransactionId
    def set_CustomerTransactionId(self, CustomerTransactionId):
        self.CustomerTransactionId = CustomerTransactionId
    def get_Localization(self):
        return self.Localization
    def set_Localization(self, Localization):
        self.Localization = Localization
    def get_InternalTransactionId(self):
        return self.InternalTransactionId
    def set_InternalTransactionId(self, InternalTransactionId):
        self.InternalTransactionId = InternalTransactionId
    def get_Tracing(self):
        return self.Tracing
    def set_Tracing(self, Tracing):
        self.Tracing = Tracing
    def get_SourceFormat(self):
        return self.SourceFormat
    def set_SourceFormat(self, SourceFormat):
        self.SourceFormat = SourceFormat
    def get_Environment(self):
        return self.Environment
    def set_Environment(self, Environment):
        self.Environment = Environment
    def validate_TransactionSourceFormat(self, value):
        result = True
        # Validate type TransactionSourceFormat, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['API_CTS', 'API_XML', 'DIRECT', 'DIRECT_XML', 'FXRS_CTS', 'UNKNOWN', 'WSI_XML']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on TransactionSourceFormat' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_WebServiceEnvironment(self, value):
        result = True
        # Validate type WebServiceEnvironment, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['PRODUCTION', 'TEST']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on WebServiceEnvironment' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.CustomerTransactionId is not None or
            self.Localization is not None or
            self.InternalTransactionId is not None or
            self.Tracing is not None or
            self.SourceFormat is not None or
            self.Environment is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TransactionDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TransactionDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TransactionDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TransactionDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TransactionDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TransactionDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TransactionDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CustomerTransactionId is not None:
            namespaceprefix_ = self.CustomerTransactionId_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomerTransactionId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustomerTransactionId>%s</%sCustomerTransactionId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CustomerTransactionId), input_name='CustomerTransactionId')), namespaceprefix_ , eol_))
        if self.Localization is not None:
            namespaceprefix_ = self.Localization_nsprefix_ + ':' if (UseCapturedNS_ and self.Localization_nsprefix_) else ''
            self.Localization.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Localization', pretty_print=pretty_print)
        if self.InternalTransactionId is not None:
            namespaceprefix_ = self.InternalTransactionId_nsprefix_ + ':' if (UseCapturedNS_ and self.InternalTransactionId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sInternalTransactionId>%s</%sInternalTransactionId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.InternalTransactionId), input_name='InternalTransactionId')), namespaceprefix_ , eol_))
        if self.Tracing is not None:
            namespaceprefix_ = self.Tracing_nsprefix_ + ':' if (UseCapturedNS_ and self.Tracing_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTracing>%s</%sTracing>%s' % (namespaceprefix_ , self.gds_format_boolean(self.Tracing, input_name='Tracing'), namespaceprefix_ , eol_))
        if self.SourceFormat is not None:
            namespaceprefix_ = self.SourceFormat_nsprefix_ + ':' if (UseCapturedNS_ and self.SourceFormat_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSourceFormat>%s</%sSourceFormat>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SourceFormat), input_name='SourceFormat')), namespaceprefix_ , eol_))
        if self.Environment is not None:
            namespaceprefix_ = self.Environment_nsprefix_ + ':' if (UseCapturedNS_ and self.Environment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEnvironment>%s</%sEnvironment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Environment), input_name='Environment')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CustomerTransactionId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CustomerTransactionId')
            value_ = self.gds_validate_string(value_, node, 'CustomerTransactionId')
            self.CustomerTransactionId = value_
            self.CustomerTransactionId_nsprefix_ = child_.prefix
        elif nodeName_ == 'Localization':
            obj_ = Localization.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Localization = obj_
            obj_.original_tagname_ = 'Localization'
        elif nodeName_ == 'InternalTransactionId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'InternalTransactionId')
            value_ = self.gds_validate_string(value_, node, 'InternalTransactionId')
            self.InternalTransactionId = value_
            self.InternalTransactionId_nsprefix_ = child_.prefix
        elif nodeName_ == 'Tracing':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'Tracing')
            ival_ = self.gds_validate_boolean(ival_, node, 'Tracing')
            self.Tracing = ival_
            self.Tracing_nsprefix_ = child_.prefix
        elif nodeName_ == 'SourceFormat':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SourceFormat')
            value_ = self.gds_validate_string(value_, node, 'SourceFormat')
            self.SourceFormat = value_
            self.SourceFormat_nsprefix_ = child_.prefix
            # validate type TransactionSourceFormat
            self.validate_TransactionSourceFormat(self.SourceFormat)
        elif nodeName_ == 'Environment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Environment')
            value_ = self.gds_validate_string(value_, node, 'Environment')
            self.Environment = value_
            self.Environment_nsprefix_ = child_.prefix
            # validate type WebServiceEnvironment
            self.validate_WebServiceEnvironment(self.Environment)
# end class TransactionDetail


class UniqueTrackingNumber(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TrackingNumber=None, TrackingNumberUniqueIdentifier=None, ShipDate=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.TrackingNumber = TrackingNumber
        self.TrackingNumber_nsprefix_ = None
        self.TrackingNumberUniqueIdentifier = TrackingNumberUniqueIdentifier
        self.TrackingNumberUniqueIdentifier_nsprefix_ = None
        if isinstance(ShipDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ShipDate, '%Y-%m-%d').date()
        else:
            initvalue_ = ShipDate
        self.ShipDate = initvalue_
        self.ShipDate_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UniqueTrackingNumber)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UniqueTrackingNumber.subclass:
            return UniqueTrackingNumber.subclass(*args_, **kwargs_)
        else:
            return UniqueTrackingNumber(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_TrackingNumber(self):
        return self.TrackingNumber
    def set_TrackingNumber(self, TrackingNumber):
        self.TrackingNumber = TrackingNumber
    def get_TrackingNumberUniqueIdentifier(self):
        return self.TrackingNumberUniqueIdentifier
    def set_TrackingNumberUniqueIdentifier(self, TrackingNumberUniqueIdentifier):
        self.TrackingNumberUniqueIdentifier = TrackingNumberUniqueIdentifier
    def get_ShipDate(self):
        return self.ShipDate
    def set_ShipDate(self, ShipDate):
        self.ShipDate = ShipDate
    def hasContent_(self):
        if (
            self.TrackingNumber is not None or
            self.TrackingNumberUniqueIdentifier is not None or
            self.ShipDate is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UniqueTrackingNumber', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UniqueTrackingNumber')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UniqueTrackingNumber':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UniqueTrackingNumber')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UniqueTrackingNumber', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UniqueTrackingNumber'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UniqueTrackingNumber', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.TrackingNumber is not None:
            namespaceprefix_ = self.TrackingNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackingNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTrackingNumber>%s</%sTrackingNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TrackingNumber), input_name='TrackingNumber')), namespaceprefix_ , eol_))
        if self.TrackingNumberUniqueIdentifier is not None:
            namespaceprefix_ = self.TrackingNumberUniqueIdentifier_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackingNumberUniqueIdentifier_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTrackingNumberUniqueIdentifier>%s</%sTrackingNumberUniqueIdentifier>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TrackingNumberUniqueIdentifier), input_name='TrackingNumberUniqueIdentifier')), namespaceprefix_ , eol_))
        if self.ShipDate is not None:
            namespaceprefix_ = self.ShipDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipDate>%s</%sShipDate>%s' % (namespaceprefix_ , self.gds_format_date(self.ShipDate, input_name='ShipDate'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'TrackingNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TrackingNumber')
            value_ = self.gds_validate_string(value_, node, 'TrackingNumber')
            self.TrackingNumber = value_
            self.TrackingNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'TrackingNumberUniqueIdentifier':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TrackingNumberUniqueIdentifier')
            value_ = self.gds_validate_string(value_, node, 'TrackingNumberUniqueIdentifier')
            self.TrackingNumberUniqueIdentifier = value_
            self.TrackingNumberUniqueIdentifier_nsprefix_ = child_.prefix
        elif nodeName_ == 'ShipDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.ShipDate = dval_
            self.ShipDate_nsprefix_ = child_.prefix
# end class UniqueTrackingNumber


class UserDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, UserId=None, Password=None, UniqueUserId=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.UserId = UserId
        self.UserId_nsprefix_ = None
        self.Password = Password
        self.Password_nsprefix_ = None
        self.UniqueUserId = UniqueUserId
        self.UniqueUserId_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UserDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UserDetail.subclass:
            return UserDetail.subclass(*args_, **kwargs_)
        else:
            return UserDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_UserId(self):
        return self.UserId
    def set_UserId(self, UserId):
        self.UserId = UserId
    def get_Password(self):
        return self.Password
    def set_Password(self, Password):
        self.Password = Password
    def get_UniqueUserId(self):
        return self.UniqueUserId
    def set_UniqueUserId(self, UniqueUserId):
        self.UniqueUserId = UniqueUserId
    def hasContent_(self):
        if (
            self.UserId is not None or
            self.Password is not None or
            self.UniqueUserId is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UserDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UserDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UserDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UserDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UserDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UserDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UserDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.UserId is not None:
            namespaceprefix_ = self.UserId_nsprefix_ + ':' if (UseCapturedNS_ and self.UserId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUserId>%s</%sUserId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UserId), input_name='UserId')), namespaceprefix_ , eol_))
        if self.Password is not None:
            namespaceprefix_ = self.Password_nsprefix_ + ':' if (UseCapturedNS_ and self.Password_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPassword>%s</%sPassword>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Password), input_name='Password')), namespaceprefix_ , eol_))
        if self.UniqueUserId is not None:
            namespaceprefix_ = self.UniqueUserId_nsprefix_ + ':' if (UseCapturedNS_ and self.UniqueUserId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUniqueUserId>%s</%sUniqueUserId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UniqueUserId), input_name='UniqueUserId')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'UserId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UserId')
            value_ = self.gds_validate_string(value_, node, 'UserId')
            self.UserId = value_
            self.UserId_nsprefix_ = child_.prefix
        elif nodeName_ == 'Password':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Password')
            value_ = self.gds_validate_string(value_, node, 'Password')
            self.Password = value_
            self.Password_nsprefix_ = child_.prefix
        elif nodeName_ == 'UniqueUserId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UniqueUserId')
            value_ = self.gds_validate_string(value_, node, 'UniqueUserId')
            self.UniqueUserId = value_
            self.UniqueUserId_nsprefix_ = child_.prefix
# end class UserDetail


class ValidateDeliveryReply(GeneratedsSuper):
    """Reply parameter of IFSS method to validate a delivry option."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.HighestSeverity = HighestSeverity
        self.validate_NotificationSeverityType(self.HighestSeverity)
        self.HighestSeverity_nsprefix_ = "ns"
        if Notifications is None:
            self.Notifications = []
        else:
            self.Notifications = Notifications
        self.Notifications_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ValidateDeliveryReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ValidateDeliveryReply.subclass:
            return ValidateDeliveryReply.subclass(*args_, **kwargs_)
        else:
            return ValidateDeliveryReply(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_HighestSeverity(self):
        return self.HighestSeverity
    def set_HighestSeverity(self, HighestSeverity):
        self.HighestSeverity = HighestSeverity
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def add_Notifications(self, value):
        self.Notifications.append(value)
    def insert_Notifications_at(self, index, value):
        self.Notifications.insert(index, value)
    def replace_Notifications_at(self, index, value):
        self.Notifications[index] = value
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def validate_NotificationSeverityType(self, value):
        result = True
        # Validate type NotificationSeverityType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ERROR', 'FAILURE', 'NOTE', 'SUCCESS', 'WARNING']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on NotificationSeverityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.HighestSeverity is not None or
            self.Notifications or
            self.TransactionDetail is not None or
            self.Version is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ValidateDeliveryReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ValidateDeliveryReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ValidateDeliveryReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ValidateDeliveryReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ValidateDeliveryReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ValidateDeliveryReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ValidateDeliveryReply', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.HighestSeverity is not None:
            namespaceprefix_ = self.HighestSeverity_nsprefix_ + ':' if (UseCapturedNS_ and self.HighestSeverity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHighestSeverity>%s</%sHighestSeverity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HighestSeverity), input_name='HighestSeverity')), namespaceprefix_ , eol_))
        for Notifications_ in self.Notifications:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            Notifications_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'HighestSeverity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HighestSeverity')
            value_ = self.gds_validate_string(value_, node, 'HighestSeverity')
            self.HighestSeverity = value_
            self.HighestSeverity_nsprefix_ = child_.prefix
            # validate type NotificationSeverityType
            self.validate_NotificationSeverityType(self.HighestSeverity)
        elif nodeName_ == 'Notifications':
            obj_ = Notification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications.append(obj_)
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
# end class ValidateDeliveryReply


class ValidateDeliveryRequest(GeneratedsSuper):
    """Request parameter of IFSS method to validate a delivery option."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, UserDetail=None, TransactionDetail=None, Version=None, ApplicationId=None, ActionRequested=None, UniqueTrackingNumber=None, RecipientContact=None, DestinationAddress=None, DeliveryRequestDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.WebAuthenticationDetail = WebAuthenticationDetail
        self.WebAuthenticationDetail_nsprefix_ = "ns"
        self.ClientDetail = ClientDetail
        self.ClientDetail_nsprefix_ = "ns"
        self.UserDetail = UserDetail
        self.UserDetail_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.ApplicationId = ApplicationId
        self.ApplicationId_nsprefix_ = None
        self.ActionRequested = ActionRequested
        self.validate_DeliveryActionType(self.ActionRequested)
        self.ActionRequested_nsprefix_ = "ns"
        self.UniqueTrackingNumber = UniqueTrackingNumber
        self.UniqueTrackingNumber_nsprefix_ = "ns"
        self.RecipientContact = RecipientContact
        self.RecipientContact_nsprefix_ = "ns"
        self.DestinationAddress = DestinationAddress
        self.DestinationAddress_nsprefix_ = "ns"
        self.DeliveryRequestDetail = DeliveryRequestDetail
        self.DeliveryRequestDetail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ValidateDeliveryRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ValidateDeliveryRequest.subclass:
            return ValidateDeliveryRequest.subclass(*args_, **kwargs_)
        else:
            return ValidateDeliveryRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_WebAuthenticationDetail(self):
        return self.WebAuthenticationDetail
    def set_WebAuthenticationDetail(self, WebAuthenticationDetail):
        self.WebAuthenticationDetail = WebAuthenticationDetail
    def get_ClientDetail(self):
        return self.ClientDetail
    def set_ClientDetail(self, ClientDetail):
        self.ClientDetail = ClientDetail
    def get_UserDetail(self):
        return self.UserDetail
    def set_UserDetail(self, UserDetail):
        self.UserDetail = UserDetail
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_ApplicationId(self):
        return self.ApplicationId
    def set_ApplicationId(self, ApplicationId):
        self.ApplicationId = ApplicationId
    def get_ActionRequested(self):
        return self.ActionRequested
    def set_ActionRequested(self, ActionRequested):
        self.ActionRequested = ActionRequested
    def get_UniqueTrackingNumber(self):
        return self.UniqueTrackingNumber
    def set_UniqueTrackingNumber(self, UniqueTrackingNumber):
        self.UniqueTrackingNumber = UniqueTrackingNumber
    def get_RecipientContact(self):
        return self.RecipientContact
    def set_RecipientContact(self, RecipientContact):
        self.RecipientContact = RecipientContact
    def get_DestinationAddress(self):
        return self.DestinationAddress
    def set_DestinationAddress(self, DestinationAddress):
        self.DestinationAddress = DestinationAddress
    def get_DeliveryRequestDetail(self):
        return self.DeliveryRequestDetail
    def set_DeliveryRequestDetail(self, DeliveryRequestDetail):
        self.DeliveryRequestDetail = DeliveryRequestDetail
    def validate_DeliveryActionType(self, value):
        result = True
        # Validate type DeliveryActionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ADD']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DeliveryActionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.UserDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.ApplicationId is not None or
            self.ActionRequested is not None or
            self.UniqueTrackingNumber is not None or
            self.RecipientContact is not None or
            self.DestinationAddress is not None or
            self.DeliveryRequestDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ValidateDeliveryRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ValidateDeliveryRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ValidateDeliveryRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ValidateDeliveryRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ValidateDeliveryRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ValidateDeliveryRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ValidateDeliveryRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.WebAuthenticationDetail is not None:
            namespaceprefix_ = self.WebAuthenticationDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.WebAuthenticationDetail_nsprefix_) else ''
            self.WebAuthenticationDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='WebAuthenticationDetail', pretty_print=pretty_print)
        if self.ClientDetail is not None:
            namespaceprefix_ = self.ClientDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientDetail_nsprefix_) else ''
            self.ClientDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClientDetail', pretty_print=pretty_print)
        if self.UserDetail is not None:
            namespaceprefix_ = self.UserDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.UserDetail_nsprefix_) else ''
            self.UserDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UserDetail', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.ApplicationId is not None:
            namespaceprefix_ = self.ApplicationId_nsprefix_ + ':' if (UseCapturedNS_ and self.ApplicationId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sApplicationId>%s</%sApplicationId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ApplicationId), input_name='ApplicationId')), namespaceprefix_ , eol_))
        if self.ActionRequested is not None:
            namespaceprefix_ = self.ActionRequested_nsprefix_ + ':' if (UseCapturedNS_ and self.ActionRequested_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sActionRequested>%s</%sActionRequested>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ActionRequested), input_name='ActionRequested')), namespaceprefix_ , eol_))
        if self.UniqueTrackingNumber is not None:
            namespaceprefix_ = self.UniqueTrackingNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.UniqueTrackingNumber_nsprefix_) else ''
            self.UniqueTrackingNumber.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UniqueTrackingNumber', pretty_print=pretty_print)
        if self.RecipientContact is not None:
            namespaceprefix_ = self.RecipientContact_nsprefix_ + ':' if (UseCapturedNS_ and self.RecipientContact_nsprefix_) else ''
            self.RecipientContact.export(outfile, level, namespaceprefix_, namespacedef_='', name_='RecipientContact', pretty_print=pretty_print)
        if self.DestinationAddress is not None:
            namespaceprefix_ = self.DestinationAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationAddress_nsprefix_) else ''
            self.DestinationAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DestinationAddress', pretty_print=pretty_print)
        if self.DeliveryRequestDetail is not None:
            namespaceprefix_ = self.DeliveryRequestDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryRequestDetail_nsprefix_) else ''
            self.DeliveryRequestDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DeliveryRequestDetail', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'WebAuthenticationDetail':
            obj_ = WebAuthenticationDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.WebAuthenticationDetail = obj_
            obj_.original_tagname_ = 'WebAuthenticationDetail'
        elif nodeName_ == 'ClientDetail':
            obj_ = ClientDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClientDetail = obj_
            obj_.original_tagname_ = 'ClientDetail'
        elif nodeName_ == 'UserDetail':
            obj_ = UserDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UserDetail = obj_
            obj_.original_tagname_ = 'UserDetail'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'ApplicationId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ApplicationId')
            value_ = self.gds_validate_string(value_, node, 'ApplicationId')
            self.ApplicationId = value_
            self.ApplicationId_nsprefix_ = child_.prefix
        elif nodeName_ == 'ActionRequested':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ActionRequested')
            value_ = self.gds_validate_string(value_, node, 'ActionRequested')
            self.ActionRequested = value_
            self.ActionRequested_nsprefix_ = child_.prefix
            # validate type DeliveryActionType
            self.validate_DeliveryActionType(self.ActionRequested)
        elif nodeName_ == 'UniqueTrackingNumber':
            obj_ = UniqueTrackingNumber.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UniqueTrackingNumber = obj_
            obj_.original_tagname_ = 'UniqueTrackingNumber'
        elif nodeName_ == 'RecipientContact':
            obj_ = Contact.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.RecipientContact = obj_
            obj_.original_tagname_ = 'RecipientContact'
        elif nodeName_ == 'DestinationAddress':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DestinationAddress = obj_
            obj_.original_tagname_ = 'DestinationAddress'
        elif nodeName_ == 'DeliveryRequestDetail':
            obj_ = DeliveryRequestDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DeliveryRequestDetail = obj_
            obj_.original_tagname_ = 'DeliveryRequestDetail'
# end class ValidateDeliveryRequest


class WebAuthenticationDetail(GeneratedsSuper):
    """Used in authentication of the sender's identity."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ParentCredential=None, UserCredential=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ParentCredential = ParentCredential
        self.ParentCredential_nsprefix_ = "ns"
        self.UserCredential = UserCredential
        self.UserCredential_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, WebAuthenticationDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if WebAuthenticationDetail.subclass:
            return WebAuthenticationDetail.subclass(*args_, **kwargs_)
        else:
            return WebAuthenticationDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ParentCredential(self):
        return self.ParentCredential
    def set_ParentCredential(self, ParentCredential):
        self.ParentCredential = ParentCredential
    def get_UserCredential(self):
        return self.UserCredential
    def set_UserCredential(self, UserCredential):
        self.UserCredential = UserCredential
    def hasContent_(self):
        if (
            self.ParentCredential is not None or
            self.UserCredential is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WebAuthenticationDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('WebAuthenticationDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'WebAuthenticationDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='WebAuthenticationDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='WebAuthenticationDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='WebAuthenticationDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WebAuthenticationDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ParentCredential is not None:
            namespaceprefix_ = self.ParentCredential_nsprefix_ + ':' if (UseCapturedNS_ and self.ParentCredential_nsprefix_) else ''
            self.ParentCredential.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ParentCredential', pretty_print=pretty_print)
        if self.UserCredential is not None:
            namespaceprefix_ = self.UserCredential_nsprefix_ + ':' if (UseCapturedNS_ and self.UserCredential_nsprefix_) else ''
            self.UserCredential.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UserCredential', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ParentCredential':
            obj_ = WebAuthenticationCredential.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ParentCredential = obj_
            obj_.original_tagname_ = 'ParentCredential'
        elif nodeName_ == 'UserCredential':
            obj_ = WebAuthenticationCredential.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UserCredential = obj_
            obj_.original_tagname_ = 'UserCredential'
# end class WebAuthenticationDetail


class WebAuthenticationCredential(GeneratedsSuper):
    """Two part authentication string used for the sender's identity"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Key=None, Password=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Key = Key
        self.Key_nsprefix_ = None
        self.Password = Password
        self.Password_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, WebAuthenticationCredential)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if WebAuthenticationCredential.subclass:
            return WebAuthenticationCredential.subclass(*args_, **kwargs_)
        else:
            return WebAuthenticationCredential(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Key(self):
        return self.Key
    def set_Key(self, Key):
        self.Key = Key
    def get_Password(self):
        return self.Password
    def set_Password(self, Password):
        self.Password = Password
    def hasContent_(self):
        if (
            self.Key is not None or
            self.Password is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WebAuthenticationCredential', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('WebAuthenticationCredential')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'WebAuthenticationCredential':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='WebAuthenticationCredential')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='WebAuthenticationCredential', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='WebAuthenticationCredential'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WebAuthenticationCredential', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Key is not None:
            namespaceprefix_ = self.Key_nsprefix_ + ':' if (UseCapturedNS_ and self.Key_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sKey>%s</%sKey>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Key), input_name='Key')), namespaceprefix_ , eol_))
        if self.Password is not None:
            namespaceprefix_ = self.Password_nsprefix_ + ':' if (UseCapturedNS_ and self.Password_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPassword>%s</%sPassword>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Password), input_name='Password')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Key':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Key')
            value_ = self.gds_validate_string(value_, node, 'Key')
            self.Key = value_
            self.Key_nsprefix_ = child_.prefix
        elif nodeName_ == 'Password':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Password')
            value_ = self.gds_validate_string(value_, node, 'Password')
            self.Password = value_
            self.Password_nsprefix_ = child_.prefix
# end class WebAuthenticationCredential


class VersionId(GeneratedsSuper):
    """Identifies the version/level of a service operation expected by a caller
    (in each request) and performed by the callee (in each reply)."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ServiceId=None, Major=None, Intermediate=None, Minor=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ServiceId = ServiceId
        self.ServiceId_nsprefix_ = None
        self.Major = Major
        self.Major_nsprefix_ = None
        self.Intermediate = Intermediate
        self.Intermediate_nsprefix_ = None
        self.Minor = Minor
        self.Minor_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, VersionId)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if VersionId.subclass:
            return VersionId.subclass(*args_, **kwargs_)
        else:
            return VersionId(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ServiceId(self):
        return self.ServiceId
    def set_ServiceId(self, ServiceId):
        self.ServiceId = ServiceId
    def get_Major(self):
        return self.Major
    def set_Major(self, Major):
        self.Major = Major
    def get_Intermediate(self):
        return self.Intermediate
    def set_Intermediate(self, Intermediate):
        self.Intermediate = Intermediate
    def get_Minor(self):
        return self.Minor
    def set_Minor(self, Minor):
        self.Minor = Minor
    def hasContent_(self):
        if (
            self.ServiceId is not None or
            self.Major is not None or
            self.Intermediate is not None or
            self.Minor is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='VersionId', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('VersionId')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'VersionId':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='VersionId')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='VersionId', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='VersionId'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='VersionId', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ServiceId is not None:
            namespaceprefix_ = self.ServiceId_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceId>%s</%sServiceId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServiceId), input_name='ServiceId')), namespaceprefix_ , eol_))
        if self.Major is not None:
            namespaceprefix_ = self.Major_nsprefix_ + ':' if (UseCapturedNS_ and self.Major_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMajor>%s</%sMajor>%s' % (namespaceprefix_ , self.gds_format_integer(self.Major, input_name='Major'), namespaceprefix_ , eol_))
        if self.Intermediate is not None:
            namespaceprefix_ = self.Intermediate_nsprefix_ + ':' if (UseCapturedNS_ and self.Intermediate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIntermediate>%s</%sIntermediate>%s' % (namespaceprefix_ , self.gds_format_integer(self.Intermediate, input_name='Intermediate'), namespaceprefix_ , eol_))
        if self.Minor is not None:
            namespaceprefix_ = self.Minor_nsprefix_ + ':' if (UseCapturedNS_ and self.Minor_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMinor>%s</%sMinor>%s' % (namespaceprefix_ , self.gds_format_integer(self.Minor, input_name='Minor'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ServiceId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServiceId')
            value_ = self.gds_validate_string(value_, node, 'ServiceId')
            self.ServiceId = value_
            self.ServiceId_nsprefix_ = child_.prefix
        elif nodeName_ == 'Major' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Major')
            ival_ = self.gds_validate_integer(ival_, node, 'Major')
            self.Major = ival_
            self.Major_nsprefix_ = child_.prefix
        elif nodeName_ == 'Intermediate' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Intermediate')
            ival_ = self.gds_validate_integer(ival_, node, 'Intermediate')
            self.Intermediate = ival_
            self.Intermediate_nsprefix_ = child_.prefix
        elif nodeName_ == 'Minor' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Minor')
            ival_ = self.gds_validate_integer(ival_, node, 'Minor')
            self.Minor = ival_
            self.Minor_nsprefix_ = child_.prefix
# end class VersionId


GDSClassesMapping = {
    'ProcessDeliveryReply': ProcessDeliveryReply,
    'ProcessDeliveryRequest': ProcessDeliveryRequest,
    'ValidateDeliveryReply': ValidateDeliveryReply,
    'ValidateDeliveryRequest': ValidateDeliveryRequest,
}


USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def get_root_tag(node):
    tag = Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = GDSClassesMapping.get(tag)
    if rootClass is None:
        rootClass = globals().get(tag)
    return tag, rootClass


def get_required_ns_prefix_defs(rootNode):
    '''Get all name space prefix definitions required in this XML doc.
    Return a dictionary of definitions and a char string of definitions.
    '''
    nsmap = {
        prefix: uri
        for node in rootNode.iter()
        for (prefix, uri) in node.nsmap.items()
        if prefix is not None
    }
    namespacedefs = ' '.join([
        'xmlns:{}="{}"'.format(prefix, uri)
        for prefix, uri in nsmap.items()
    ])
    return nsmap, namespacedefs


def parse(inFileName, silence=False, print_warnings=True):
    global CapturedNsmap_
    gds_collector = GdsCollector_()
    parser = None
    doc = parsexml_(inFileName, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'ProcessDeliveryReply'
        rootClass = ProcessDeliveryReply
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    CapturedNsmap_, namespacedefs = get_required_ns_prefix_defs(rootNode)
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_=namespacedefs,
            pretty_print=True)
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def parseEtree(inFileName, silence=False, print_warnings=True,
               mapping=None, nsmap=None):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'ProcessDeliveryReply'
        rootClass = ProcessDeliveryReply
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if mapping is None:
        mapping = {}
    rootElement = rootObj.to_etree(
        None, name_=rootTag, mapping_=mapping, nsmap_=nsmap)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(str(content))
        sys.stdout.write('\n')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False, print_warnings=True):
    '''Parse a string, create the object tree, and export it.

    Arguments:
    - inString -- A string.  This XML fragment should not start
      with an XML declaration containing an encoding.
    - silence -- A boolean.  If False, export the object.
    Returns -- The root object in the tree.
    '''
    parser = None
    rootNode= parsexmlstring_(inString, parser)
    gds_collector = GdsCollector_()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'ProcessDeliveryReply'
        rootClass = ProcessDeliveryReply
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:ns="http://fedex.com/ws/ifss/v1"')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
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
        rootTag = 'ProcessDeliveryReply'
        rootClass = ProcessDeliveryReply
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from in_flight_shipment_service_v1 import *\n\n')
        sys.stdout.write('import in_flight_shipment_service_v1 as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        parse(args[0])
    else:
        usage()


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()

RenameMappings_ = {
}

#
# Mapping of namespaces to types defined in them
# and the file in which each is defined.
# simpleTypes are marked "ST" and complexTypes "CT".
NamespaceToDefMappings_ = {'http://fedex.com/ws/ifss/v1': [('AppointmentWindowType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('AssociatedAccountNumberType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('AutoConfigurationType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('CreditCardAuthorizationType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('CreditCardSettlementScheduleType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('CreditCardTransactionAttributeType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('CreditCardType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('DeliveryActionType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('DeliveryOptionType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('DocumentFormatOptionType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('EMailNotificationRecipientType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('ExpressRegionCode',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('LinearUnits',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('NotificationSeverityType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('OperationalDocumentType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('PaymentType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('RerouteDeliveryType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('RescheduleDeliveryType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('ShippingDocumentDispositionType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('ShippingDocumentEMailGroupingType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('ShippingDocumentGroupingType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('ShippingDocumentImageType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('ShippingDocumentNamingType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('ShippingDocumentStockType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('SurchargeLevelType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('SurchargeType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('TinType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('TrackingIdType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('TransactionSourceFormat',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('TransitTimeType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('WebServiceEnvironment',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'ST'),
                                 ('Address',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('AppointmentDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('AppointmentTimeDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('AssociatedAccount',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('ClientDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('Contact',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('ContactAndAddress',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('CreditCard',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('CreditCardTransactionAttributesDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('CreditCardTransactionDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('CreditFraudDetectionDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('DeliveryRequestDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('DocumentFormatOptionsRequested',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('InitiativeManifest',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('LinearMeasure',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('LocalTimeRange',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('Localization',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('Money',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('Notification',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('NotificationParameter',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('OperationalDocumentPart',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('OperationalDocumentSpecification',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('ParsedContact',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('ParsedContactAndAddress',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('ParsedPersonName',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('Party',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('Payor',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('ProcessDeliveryReply',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('ProcessDeliveryRequest',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('RatedDeliveryDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('RedirectToHoldAtLocationRequestDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('RerouteDeliveryDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('ShippingDocumentDispositionDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('ShippingDocumentEMailDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('ShippingDocumentEMailRecipient',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('ShippingDocumentFormat',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('ShippingDocumentPrintDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('ShippingDocumentStorageDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('SignatureReleaseDocumentDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('Surcharge',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('TaxpayerIdentification',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('TrackingId',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('TransactionDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('UniqueTrackingNumber',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('UserDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('ValidateDeliveryReply',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('ValidateDeliveryRequest',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('WebAuthenticationDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('WebAuthenticationCredential',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT'),
                                 ('VersionId',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/InFlightShipmentService_v1.xsd',
                                  'CT')]}

__all__ = [
    "Address",
    "AppointmentDetail",
    "AppointmentTimeDetail",
    "AssociatedAccount",
    "ClientDetail",
    "Contact",
    "ContactAndAddress",
    "CreditCard",
    "CreditCardTransactionAttributesDetail",
    "CreditCardTransactionDetail",
    "CreditFraudDetectionDetail",
    "DeliveryRequestDetail",
    "DocumentFormatOptionsRequested",
    "InitiativeManifest",
    "LinearMeasure",
    "LocalTimeRange",
    "Localization",
    "Money",
    "Notification",
    "NotificationParameter",
    "OperationalDocumentPart",
    "OperationalDocumentSpecification",
    "ParsedContact",
    "ParsedContactAndAddress",
    "ParsedPersonName",
    "Party",
    "Payor",
    "ProcessDeliveryReply",
    "ProcessDeliveryRequest",
    "RatedDeliveryDetail",
    "RedirectToHoldAtLocationRequestDetail",
    "RerouteDeliveryDetail",
    "ShippingDocumentDispositionDetail",
    "ShippingDocumentEMailDetail",
    "ShippingDocumentEMailRecipient",
    "ShippingDocumentFormat",
    "ShippingDocumentPrintDetail",
    "ShippingDocumentStorageDetail",
    "SignatureReleaseDocumentDetail",
    "Surcharge",
    "TaxpayerIdentification",
    "TrackingId",
    "TransactionDetail",
    "UniqueTrackingNumber",
    "UserDetail",
    "ValidateDeliveryReply",
    "ValidateDeliveryRequest",
    "VersionId",
    "WebAuthenticationCredential",
    "WebAuthenticationDetail"
]
