#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Thu May  6 11:00:04 2021 by generateDS.py version 2.38.6.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './fedex_lib/location_service_v12.py')
#
# Command line arguments:
#   /Users/danielkobina/Workspace/Carriers Doc/Fedex/2020-09/schemas/LocationService_v12.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./fedex_lib/location_service_v12.py" /Users/danielkobina/Workspace/Carriers Doc/Fedex/2020-09/schemas/LocationService_v12.xsd
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


class AutoConfigurationType(str, Enum):
    ENTERPRISE='ENTERPRISE'
    SHIPPING_SERVICE_PROVIDER='SHIPPING_SERVICE_PROVIDER'
    SOFTWARE_ONLY='SOFTWARE_ONLY'
    TRADITIONAL='TRADITIONAL'


class AvailableLocationsRequestServiceLevel(str, Enum):
    CUSTOMER_APPROPRIATE_DATA='CUSTOMER_APPROPRIATE_DATA'
    INCLUDE_ACCOUNT_DATA='INCLUDE_ACCOUNT_DATA'
    NO_ACCOUNT_DATA='NO_ACCOUNT_DATA'


class CarrierCodeType(str, Enum):
    """Identification of a FedEx operating company (transportation)."""
    FDXC='FDXC'
    FDXE='FDXE'
    FDXG='FDXG'
    FDXO='FDXO'
    FXCC='FXCC'
    FXFR='FXFR'
    FXSP='FXSP'


class ConsolidationType(str, Enum):
    INTERNATIONAL_DISTRIBUTION_FREIGHT='INTERNATIONAL_DISTRIBUTION_FREIGHT'
    INTERNATIONAL_ECONOMY_DISTRIBUTION='INTERNATIONAL_ECONOMY_DISTRIBUTION'
    INTERNATIONAL_GROUND_DISTRIBUTION='INTERNATIONAL_GROUND_DISTRIBUTION'
    INTERNATIONAL_PRIORITY_DISTRIBUTION='INTERNATIONAL_PRIORITY_DISTRIBUTION'
    TRANSBORDER_DISTRIBUTION='TRANSBORDER_DISTRIBUTION'


class CountryRelationshipType(str, Enum):
    """Describes relationship between origin and destination countries."""
    DOMESTIC='DOMESTIC'
    INTERNATIONAL='INTERNATIONAL'


class DayOfWeekType(str, Enum):
    FRI='FRI'
    MON='MON'
    SAT='SAT'
    SUN='SUN'
    THU='THU'
    TUE='TUE'
    WED='WED'


class DistanceUnits(str, Enum):
    KM='KM'
    MI='MI'


class DistributionClearanceType(str, Enum):
    DESTINATION_COUNTRY_CLEARANCE='DESTINATION_COUNTRY_CLEARANCE'
    SINGLE_POINT_OF_CLEARANCE='SINGLE_POINT_OF_CLEARANCE'


class EnterprisePermissionType(str, Enum):
    ALLOWED='ALLOWED'
    ALLOWED_BY_EXCEPTION='ALLOWED_BY_EXCEPTION'
    DISALLOWED='DISALLOWED'


class ExpressRegionCode(str, Enum):
    """Indicates a FedEx Express operating region."""
    APAC='APAC'
    CA='CA'
    EMEA='EMEA'
    LAC='LAC'
    US='US'


class FedExLocationType(str, Enum):
    """Identifies a kind of FedEx facility."""
    FEDEX_AUTHORIZED_SHIP_CENTER='FEDEX_AUTHORIZED_SHIP_CENTER'
    FEDEX_EXPRESS_STATION='FEDEX_EXPRESS_STATION'
    FEDEX_FACILITY='FEDEX_FACILITY'
    FEDEX_FREIGHT_SERVICE_CENTER='FEDEX_FREIGHT_SERVICE_CENTER'
    FEDEX_GROUND_TERMINAL='FEDEX_GROUND_TERMINAL'
    FEDEX_HOME_DELIVERY_STATION='FEDEX_HOME_DELIVERY_STATION'
    FEDEX_OFFICE='FEDEX_OFFICE'
    FEDEX_ONSITE='FEDEX_ONSITE'
    FEDEX_SELF_SERVICE_LOCATION='FEDEX_SELF_SERVICE_LOCATION'
    FEDEX_SHIPSITE='FEDEX_SHIPSITE'
    FEDEX_SHIP_AND_GET='FEDEX_SHIP_AND_GET'
    FEDEX_SMART_POST_HUB='FEDEX_SMART_POST_HUB'


class IntermediateVersionType(str, Enum):
    _0='0'


class LatestDropOffOverlayType(str, Enum):
    """Specifies the reason for the overlay of the daily last drop off time for
    a carrier."""
    US_WEST_COAST='US_WEST_COAST'


class LinearUnits(str, Enum):
    CM='CM'
    IN='IN'


class LocationAccessibilityType(str, Enum):
    """Indicates how this can be accessed."""
    INSIDE='INSIDE'
    OUTSIDE='OUTSIDE'


class LocationAttributesForInternalFedexUseType(str, Enum):
    FAMIS_LOCATION='FAMIS_LOCATION'


class LocationAttributesType(str, Enum):
    ACCEPTS_CASH='ACCEPTS_CASH'
    ALREADY_OPEN='ALREADY_OPEN'
    CLEARANCE_SERVICES='CLEARANCE_SERVICES'
    COPY_AND_PRINT_SERVICES='COPY_AND_PRINT_SERVICES'
    DANGEROUS_GOODS_SERVICES='DANGEROUS_GOODS_SERVICES'
    DIRECT_MAIL_SERVICES='DIRECT_MAIL_SERVICES'
    DOMESTIC_SHIPPING_SERVICES='DOMESTIC_SHIPPING_SERVICES'
    DROP_BOX='DROP_BOX'
    INTERNATIONAL_SHIPPING_SERVICES='INTERNATIONAL_SHIPPING_SERVICES'
    LOCATION_IS_IN_AIRPORT='LOCATION_IS_IN_AIRPORT'
    NOTARY_SERVICES='NOTARY_SERVICES'
    OBSERVES_DAY_LIGHT_SAVING_TIMES='OBSERVES_DAY_LIGHT_SAVING_TIMES'
    OPEN_TWENTY_FOUR_HOURS='OPEN_TWENTY_FOUR_HOURS'
    PACKAGING_SUPPLIES='PACKAGING_SUPPLIES'
    PACK_AND_SHIP='PACK_AND_SHIP'
    PASSPORT_PHOTO_SERVICES='PASSPORT_PHOTO_SERVICES'
    RETURNS_SERVICES='RETURNS_SERVICES'
    SIGNS_AND_BANNERS_SERVICE='SIGNS_AND_BANNERS_SERVICE'
    SONY_PICTURE_STATION='SONY_PICTURE_STATION'


class LocationContentOptionType(str, Enum):
    HOLIDAYS='HOLIDAYS'
    LOCATION_DROPOFF_TIMES='LOCATION_DROPOFF_TIMES'
    MAP_URL='MAP_URL'
    TIMEZONE_OFFSET='TIMEZONE_OFFSET'


class LocationSearchFilterType(str, Enum):
    """Specifies the crieteria used to filter the location search results."""
    EXCLUDE_LOCATIONS_OUTSIDE_COUNTRY='EXCLUDE_LOCATIONS_OUTSIDE_COUNTRY'
    EXCLUDE_LOCATIONS_OUTSIDE_STATE_OR_PROVINCE='EXCLUDE_LOCATIONS_OUTSIDE_STATE_OR_PROVINCE'
    EXCLUDE_UNAVAILABLE_LOCATIONS='EXCLUDE_UNAVAILABLE_LOCATIONS'


class LocationSortCriteriaType(str, Enum):
    """Specifies the criterion to be used to sort the location details."""
    DISTANCE='DISTANCE'
    LATEST_EXPRESS_DROPOFF_TIME='LATEST_EXPRESS_DROPOFF_TIME'
    LATEST_GROUND_DROPOFF_TIME='LATEST_GROUND_DROPOFF_TIME'
    LOCATION_TYPE='LOCATION_TYPE'


class LocationSortOrderType(str, Enum):
    """Specifies sort order of the location details."""
    HIGHEST_TO_LOWEST='HIGHEST_TO_LOWEST'
    LOWEST_TO_HIGHEST='LOWEST_TO_HIGHEST'


class LocationTransferOfPossessionType(str, Enum):
    DROPOFF='DROPOFF'
    HOLD_AT_LOCATION='HOLD_AT_LOCATION'
    REDIRECT_TO_HOLD_AT_LOCATION='REDIRECT_TO_HOLD_AT_LOCATION'


class LocationsSearchCriteriaType(str, Enum):
    """Specifies the criteria types that may be used to search for FedEx
    locations."""
    ADDRESS='ADDRESS'
    GEOGRAPHIC_COORDINATES='GEOGRAPHIC_COORDINATES'
    MOBILE_PHONE_NUMBER='MOBILE_PHONE_NUMBER'
    PHONE_NUMBER='PHONE_NUMBER'


class MajorVersionType(str, Enum):
    _1_2='12'


class MinorVersionType(str, Enum):
    _0='0'


class MultipleMatchesActionType(str, Enum):
    RETURN_ALL='RETURN_ALL'
    RETURN_ERROR='RETURN_ERROR'
    RETURN_FIRST='RETURN_FIRST'


class NotificationSeverityType(str, Enum):
    ERROR='ERROR'
    FAILURE='FAILURE'
    NOTE='NOTE'
    SUCCESS='SUCCESS'
    WARNING='WARNING'


class OperationalHoursType(str, Enum):
    CLOSED_ALL_DAY='CLOSED_ALL_DAY'
    OPEN_ALL_DAY='OPEN_ALL_DAY'
    OPEN_BY_HOURS='OPEN_BY_HOURS'


class ReservationAttributesType(str, Enum):
    """Attributes about a reservation at a FedEx location."""
    RESERVATION_AVAILABLE='RESERVATION_AVAILABLE'


class RestrictionsAndPrivilegesPolicyExceptionType(str, Enum):
    POLICIES_NOT_FOUND='POLICIES_NOT_FOUND'
    SERVICE_UNAVAILABLE='SERVICE_UNAVAILABLE'


class SearchLocationsProcessingOptionType(str, Enum):
    ALLOW_RESTRICTIONS_WITH_EXCEPTIONS='ALLOW_RESTRICTIONS_WITH_EXCEPTIONS'


class SearchLocationsServiceLevelType(str, Enum):
    TRUSTED_PROXY='TRUSTED_PROXY'


class ServiceCategoryType(str, Enum):
    EXPRESS_FREIGHT='EXPRESS_FREIGHT'
    EXPRESS_PARCEL='EXPRESS_PARCEL'
    GROUND_HOME_DELIVERY='GROUND_HOME_DELIVERY'


class ServiceIdType(str, Enum):
    """Identifies the available set of callable FedEx services. This
    information deals with the service being called by the web service
    client, not the FedEx transportation service offerings. Set the value
    to "wsi" if you are using the FedEx web services interface."""
    LOCS='locs'


class ShippingActionType(str, Enum):
    DELIVERIES='DELIVERIES'
    PICKUPS='PICKUPS'


class SupportedRedirectToHoldServiceType(str, Enum):
    """DEPRECATED as of July 2017."""
    FEDEX_EXPRESS='FEDEX_EXPRESS'
    FEDEX_GROUND='FEDEX_GROUND'
    FEDEX_GROUND_HOME_DELIVERY='FEDEX_GROUND_HOME_DELIVERY'


class TransactionSourceFormat(str, Enum):
    API_CTS='API_CTS'
    API_XML='API_XML'
    DIRECT='DIRECT'
    DIRECT_XML='DIRECT_XML'
    FXRS_CTS='FXRS_CTS'
    UNKNOWN='UNKNOWN'
    WSI_XML='WSI_XML'


class WebServiceEnvironment(str, Enum):
    """Identifies the environment (level) for which an AuthenticationCredential
    is valid, and within which transactions are received."""
    PRODUCTION='PRODUCTION'
    TEST='TEST'


class WeightUnits(str, Enum):
    KG='KG'
    LB='LB'


class Address(GeneratedsSuper):
    """Descriptive data for a physical location. May be used as an actual
    physical address (place to which one could go), or as a container of
    "address parts" which should be handled as a unit (such as a city-
    state-ZIP combination within the US)."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, StreetLines=None, City=None, StateOrProvinceCode=None, PostalCode=None, UrbanizationCode=None, CountryCode=None, CountryName=None, Residential=None, GeographicCoordinates=None, gds_collector_=None, **kwargs_):
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
        self.GeographicCoordinates = GeographicCoordinates
        self.GeographicCoordinates_nsprefix_ = None
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
    def get_GeographicCoordinates(self):
        return self.GeographicCoordinates
    def set_GeographicCoordinates(self, GeographicCoordinates):
        self.GeographicCoordinates = GeographicCoordinates
    def hasContent_(self):
        if (
            self.StreetLines or
            self.City is not None or
            self.StateOrProvinceCode is not None or
            self.PostalCode is not None or
            self.UrbanizationCode is not None or
            self.CountryCode is not None or
            self.CountryName is not None or
            self.Residential is not None or
            self.GeographicCoordinates is not None
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
        if self.GeographicCoordinates is not None:
            namespaceprefix_ = self.GeographicCoordinates_nsprefix_ + ':' if (UseCapturedNS_ and self.GeographicCoordinates_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGeographicCoordinates>%s</%sGeographicCoordinates>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GeographicCoordinates), input_name='GeographicCoordinates')), namespaceprefix_ , eol_))
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
        elif nodeName_ == 'GeographicCoordinates':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GeographicCoordinates')
            value_ = self.gds_validate_string(value_, node, 'GeographicCoordinates')
            self.GeographicCoordinates = value_
            self.GeographicCoordinates_nsprefix_ = child_.prefix
# end class Address


class AddressAncillaryDetail(GeneratedsSuper):
    """Additional information about a physical location, such as suite number,
    cross street, floor number in a building. These details are not
    typically a part of a standard address definition; however, these
    details might help locate the address."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, LocationInCity=None, LocationInProperty=None, Accessibility=None, Building=None, Department=None, RoomFloor=None, Suite=None, Apartment=None, Room=None, CrossStreet=None, AdditionalDescriptions=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.LocationInCity = LocationInCity
        self.LocationInCity_nsprefix_ = None
        self.LocationInProperty = LocationInProperty
        self.LocationInProperty_nsprefix_ = None
        self.Accessibility = Accessibility
        self.validate_LocationAccessibilityType(self.Accessibility)
        self.Accessibility_nsprefix_ = "ns"
        self.Building = Building
        self.Building_nsprefix_ = None
        self.Department = Department
        self.Department_nsprefix_ = None
        self.RoomFloor = RoomFloor
        self.RoomFloor_nsprefix_ = None
        self.Suite = Suite
        self.Suite_nsprefix_ = None
        self.Apartment = Apartment
        self.Apartment_nsprefix_ = None
        self.Room = Room
        self.Room_nsprefix_ = None
        self.CrossStreet = CrossStreet
        self.CrossStreet_nsprefix_ = None
        if AdditionalDescriptions is None:
            self.AdditionalDescriptions = []
        else:
            self.AdditionalDescriptions = AdditionalDescriptions
        self.AdditionalDescriptions_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AddressAncillaryDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AddressAncillaryDetail.subclass:
            return AddressAncillaryDetail.subclass(*args_, **kwargs_)
        else:
            return AddressAncillaryDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_LocationInCity(self):
        return self.LocationInCity
    def set_LocationInCity(self, LocationInCity):
        self.LocationInCity = LocationInCity
    def get_LocationInProperty(self):
        return self.LocationInProperty
    def set_LocationInProperty(self, LocationInProperty):
        self.LocationInProperty = LocationInProperty
    def get_Accessibility(self):
        return self.Accessibility
    def set_Accessibility(self, Accessibility):
        self.Accessibility = Accessibility
    def get_Building(self):
        return self.Building
    def set_Building(self, Building):
        self.Building = Building
    def get_Department(self):
        return self.Department
    def set_Department(self, Department):
        self.Department = Department
    def get_RoomFloor(self):
        return self.RoomFloor
    def set_RoomFloor(self, RoomFloor):
        self.RoomFloor = RoomFloor
    def get_Suite(self):
        return self.Suite
    def set_Suite(self, Suite):
        self.Suite = Suite
    def get_Apartment(self):
        return self.Apartment
    def set_Apartment(self, Apartment):
        self.Apartment = Apartment
    def get_Room(self):
        return self.Room
    def set_Room(self, Room):
        self.Room = Room
    def get_CrossStreet(self):
        return self.CrossStreet
    def set_CrossStreet(self, CrossStreet):
        self.CrossStreet = CrossStreet
    def get_AdditionalDescriptions(self):
        return self.AdditionalDescriptions
    def set_AdditionalDescriptions(self, AdditionalDescriptions):
        self.AdditionalDescriptions = AdditionalDescriptions
    def add_AdditionalDescriptions(self, value):
        self.AdditionalDescriptions.append(value)
    def insert_AdditionalDescriptions_at(self, index, value):
        self.AdditionalDescriptions.insert(index, value)
    def replace_AdditionalDescriptions_at(self, index, value):
        self.AdditionalDescriptions[index] = value
    def validate_LocationAccessibilityType(self, value):
        result = True
        # Validate type LocationAccessibilityType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['INSIDE', 'OUTSIDE']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on LocationAccessibilityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.LocationInCity is not None or
            self.LocationInProperty is not None or
            self.Accessibility is not None or
            self.Building is not None or
            self.Department is not None or
            self.RoomFloor is not None or
            self.Suite is not None or
            self.Apartment is not None or
            self.Room is not None or
            self.CrossStreet is not None or
            self.AdditionalDescriptions
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressAncillaryDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AddressAncillaryDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AddressAncillaryDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AddressAncillaryDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AddressAncillaryDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AddressAncillaryDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressAncillaryDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.LocationInCity is not None:
            namespaceprefix_ = self.LocationInCity_nsprefix_ + ':' if (UseCapturedNS_ and self.LocationInCity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocationInCity>%s</%sLocationInCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocationInCity), input_name='LocationInCity')), namespaceprefix_ , eol_))
        if self.LocationInProperty is not None:
            namespaceprefix_ = self.LocationInProperty_nsprefix_ + ':' if (UseCapturedNS_ and self.LocationInProperty_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocationInProperty>%s</%sLocationInProperty>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocationInProperty), input_name='LocationInProperty')), namespaceprefix_ , eol_))
        if self.Accessibility is not None:
            namespaceprefix_ = self.Accessibility_nsprefix_ + ':' if (UseCapturedNS_ and self.Accessibility_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccessibility>%s</%sAccessibility>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Accessibility), input_name='Accessibility')), namespaceprefix_ , eol_))
        if self.Building is not None:
            namespaceprefix_ = self.Building_nsprefix_ + ':' if (UseCapturedNS_ and self.Building_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBuilding>%s</%sBuilding>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Building), input_name='Building')), namespaceprefix_ , eol_))
        if self.Department is not None:
            namespaceprefix_ = self.Department_nsprefix_ + ':' if (UseCapturedNS_ and self.Department_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDepartment>%s</%sDepartment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Department), input_name='Department')), namespaceprefix_ , eol_))
        if self.RoomFloor is not None:
            namespaceprefix_ = self.RoomFloor_nsprefix_ + ':' if (UseCapturedNS_ and self.RoomFloor_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRoomFloor>%s</%sRoomFloor>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.RoomFloor), input_name='RoomFloor')), namespaceprefix_ , eol_))
        if self.Suite is not None:
            namespaceprefix_ = self.Suite_nsprefix_ + ':' if (UseCapturedNS_ and self.Suite_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSuite>%s</%sSuite>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Suite), input_name='Suite')), namespaceprefix_ , eol_))
        if self.Apartment is not None:
            namespaceprefix_ = self.Apartment_nsprefix_ + ':' if (UseCapturedNS_ and self.Apartment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sApartment>%s</%sApartment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Apartment), input_name='Apartment')), namespaceprefix_ , eol_))
        if self.Room is not None:
            namespaceprefix_ = self.Room_nsprefix_ + ':' if (UseCapturedNS_ and self.Room_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRoom>%s</%sRoom>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Room), input_name='Room')), namespaceprefix_ , eol_))
        if self.CrossStreet is not None:
            namespaceprefix_ = self.CrossStreet_nsprefix_ + ':' if (UseCapturedNS_ and self.CrossStreet_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCrossStreet>%s</%sCrossStreet>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CrossStreet), input_name='CrossStreet')), namespaceprefix_ , eol_))
        for AdditionalDescriptions_ in self.AdditionalDescriptions:
            namespaceprefix_ = self.AdditionalDescriptions_nsprefix_ + ':' if (UseCapturedNS_ and self.AdditionalDescriptions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAdditionalDescriptions>%s</%sAdditionalDescriptions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(AdditionalDescriptions_), input_name='AdditionalDescriptions')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'LocationInCity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocationInCity')
            value_ = self.gds_validate_string(value_, node, 'LocationInCity')
            self.LocationInCity = value_
            self.LocationInCity_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocationInProperty':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocationInProperty')
            value_ = self.gds_validate_string(value_, node, 'LocationInProperty')
            self.LocationInProperty = value_
            self.LocationInProperty_nsprefix_ = child_.prefix
        elif nodeName_ == 'Accessibility':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Accessibility')
            value_ = self.gds_validate_string(value_, node, 'Accessibility')
            self.Accessibility = value_
            self.Accessibility_nsprefix_ = child_.prefix
            # validate type LocationAccessibilityType
            self.validate_LocationAccessibilityType(self.Accessibility)
        elif nodeName_ == 'Building':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Building')
            value_ = self.gds_validate_string(value_, node, 'Building')
            self.Building = value_
            self.Building_nsprefix_ = child_.prefix
        elif nodeName_ == 'Department':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Department')
            value_ = self.gds_validate_string(value_, node, 'Department')
            self.Department = value_
            self.Department_nsprefix_ = child_.prefix
        elif nodeName_ == 'RoomFloor':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RoomFloor')
            value_ = self.gds_validate_string(value_, node, 'RoomFloor')
            self.RoomFloor = value_
            self.RoomFloor_nsprefix_ = child_.prefix
        elif nodeName_ == 'Suite':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Suite')
            value_ = self.gds_validate_string(value_, node, 'Suite')
            self.Suite = value_
            self.Suite_nsprefix_ = child_.prefix
        elif nodeName_ == 'Apartment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Apartment')
            value_ = self.gds_validate_string(value_, node, 'Apartment')
            self.Apartment = value_
            self.Apartment_nsprefix_ = child_.prefix
        elif nodeName_ == 'Room':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Room')
            value_ = self.gds_validate_string(value_, node, 'Room')
            self.Room = value_
            self.Room_nsprefix_ = child_.prefix
        elif nodeName_ == 'CrossStreet':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CrossStreet')
            value_ = self.gds_validate_string(value_, node, 'CrossStreet')
            self.CrossStreet = value_
            self.CrossStreet_nsprefix_ = child_.prefix
        elif nodeName_ == 'AdditionalDescriptions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AdditionalDescriptions')
            value_ = self.gds_validate_string(value_, node, 'AdditionalDescriptions')
            self.AdditionalDescriptions.append(value_)
            self.AdditionalDescriptions_nsprefix_ = child_.prefix
# end class AddressAncillaryDetail


class AddressToLocationRelationshipDetail(GeneratedsSuper):
    """Specifies the relationship between the address specificed and the
    address of the FedEx Location in terms of distance."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, MatchedAddress=None, MatchedAddressGeographicCoordinates=None, DistanceAndLocationDetails=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.MatchedAddress = MatchedAddress
        self.MatchedAddress_nsprefix_ = "ns"
        self.MatchedAddressGeographicCoordinates = MatchedAddressGeographicCoordinates
        self.MatchedAddressGeographicCoordinates_nsprefix_ = None
        if DistanceAndLocationDetails is None:
            self.DistanceAndLocationDetails = []
        else:
            self.DistanceAndLocationDetails = DistanceAndLocationDetails
        self.DistanceAndLocationDetails_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AddressToLocationRelationshipDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AddressToLocationRelationshipDetail.subclass:
            return AddressToLocationRelationshipDetail.subclass(*args_, **kwargs_)
        else:
            return AddressToLocationRelationshipDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_MatchedAddress(self):
        return self.MatchedAddress
    def set_MatchedAddress(self, MatchedAddress):
        self.MatchedAddress = MatchedAddress
    def get_MatchedAddressGeographicCoordinates(self):
        return self.MatchedAddressGeographicCoordinates
    def set_MatchedAddressGeographicCoordinates(self, MatchedAddressGeographicCoordinates):
        self.MatchedAddressGeographicCoordinates = MatchedAddressGeographicCoordinates
    def get_DistanceAndLocationDetails(self):
        return self.DistanceAndLocationDetails
    def set_DistanceAndLocationDetails(self, DistanceAndLocationDetails):
        self.DistanceAndLocationDetails = DistanceAndLocationDetails
    def add_DistanceAndLocationDetails(self, value):
        self.DistanceAndLocationDetails.append(value)
    def insert_DistanceAndLocationDetails_at(self, index, value):
        self.DistanceAndLocationDetails.insert(index, value)
    def replace_DistanceAndLocationDetails_at(self, index, value):
        self.DistanceAndLocationDetails[index] = value
    def hasContent_(self):
        if (
            self.MatchedAddress is not None or
            self.MatchedAddressGeographicCoordinates is not None or
            self.DistanceAndLocationDetails
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressToLocationRelationshipDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AddressToLocationRelationshipDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AddressToLocationRelationshipDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AddressToLocationRelationshipDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AddressToLocationRelationshipDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AddressToLocationRelationshipDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressToLocationRelationshipDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.MatchedAddress is not None:
            namespaceprefix_ = self.MatchedAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.MatchedAddress_nsprefix_) else ''
            self.MatchedAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='MatchedAddress', pretty_print=pretty_print)
        if self.MatchedAddressGeographicCoordinates is not None:
            namespaceprefix_ = self.MatchedAddressGeographicCoordinates_nsprefix_ + ':' if (UseCapturedNS_ and self.MatchedAddressGeographicCoordinates_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMatchedAddressGeographicCoordinates>%s</%sMatchedAddressGeographicCoordinates>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MatchedAddressGeographicCoordinates), input_name='MatchedAddressGeographicCoordinates')), namespaceprefix_ , eol_))
        for DistanceAndLocationDetails_ in self.DistanceAndLocationDetails:
            namespaceprefix_ = self.DistanceAndLocationDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.DistanceAndLocationDetails_nsprefix_) else ''
            DistanceAndLocationDetails_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DistanceAndLocationDetails', pretty_print=pretty_print)
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
        if nodeName_ == 'MatchedAddress':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.MatchedAddress = obj_
            obj_.original_tagname_ = 'MatchedAddress'
        elif nodeName_ == 'MatchedAddressGeographicCoordinates':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MatchedAddressGeographicCoordinates')
            value_ = self.gds_validate_string(value_, node, 'MatchedAddressGeographicCoordinates')
            self.MatchedAddressGeographicCoordinates = value_
            self.MatchedAddressGeographicCoordinates_nsprefix_ = child_.prefix
        elif nodeName_ == 'DistanceAndLocationDetails':
            obj_ = DistanceAndLocationDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DistanceAndLocationDetails.append(obj_)
            obj_.original_tagname_ = 'DistanceAndLocationDetails'
# end class AddressToLocationRelationshipDetail


class CarrierDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Carrier=None, ServiceCategory=None, ServiceType=None, CountryRelationship=None, NormalLatestDropOffDetails=None, ExceptionalLatestDropOffDetails=None, EffectiveLatestDropOffDetails=None, ShippingHolidays=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Carrier = Carrier
        self.validate_CarrierCodeType(self.Carrier)
        self.Carrier_nsprefix_ = "ns"
        self.ServiceCategory = ServiceCategory
        self.validate_ServiceCategoryType(self.ServiceCategory)
        self.ServiceCategory_nsprefix_ = "ns"
        self.ServiceType = ServiceType
        self.ServiceType_nsprefix_ = None
        self.CountryRelationship = CountryRelationship
        self.validate_CountryRelationshipType(self.CountryRelationship)
        self.CountryRelationship_nsprefix_ = "ns"
        if NormalLatestDropOffDetails is None:
            self.NormalLatestDropOffDetails = []
        else:
            self.NormalLatestDropOffDetails = NormalLatestDropOffDetails
        self.NormalLatestDropOffDetails_nsprefix_ = "ns"
        if ExceptionalLatestDropOffDetails is None:
            self.ExceptionalLatestDropOffDetails = []
        else:
            self.ExceptionalLatestDropOffDetails = ExceptionalLatestDropOffDetails
        self.ExceptionalLatestDropOffDetails_nsprefix_ = "ns"
        self.EffectiveLatestDropOffDetails = EffectiveLatestDropOffDetails
        self.EffectiveLatestDropOffDetails_nsprefix_ = "ns"
        if ShippingHolidays is None:
            self.ShippingHolidays = []
        else:
            self.ShippingHolidays = ShippingHolidays
        self.ShippingHolidays_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CarrierDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CarrierDetail.subclass:
            return CarrierDetail.subclass(*args_, **kwargs_)
        else:
            return CarrierDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Carrier(self):
        return self.Carrier
    def set_Carrier(self, Carrier):
        self.Carrier = Carrier
    def get_ServiceCategory(self):
        return self.ServiceCategory
    def set_ServiceCategory(self, ServiceCategory):
        self.ServiceCategory = ServiceCategory
    def get_ServiceType(self):
        return self.ServiceType
    def set_ServiceType(self, ServiceType):
        self.ServiceType = ServiceType
    def get_CountryRelationship(self):
        return self.CountryRelationship
    def set_CountryRelationship(self, CountryRelationship):
        self.CountryRelationship = CountryRelationship
    def get_NormalLatestDropOffDetails(self):
        return self.NormalLatestDropOffDetails
    def set_NormalLatestDropOffDetails(self, NormalLatestDropOffDetails):
        self.NormalLatestDropOffDetails = NormalLatestDropOffDetails
    def add_NormalLatestDropOffDetails(self, value):
        self.NormalLatestDropOffDetails.append(value)
    def insert_NormalLatestDropOffDetails_at(self, index, value):
        self.NormalLatestDropOffDetails.insert(index, value)
    def replace_NormalLatestDropOffDetails_at(self, index, value):
        self.NormalLatestDropOffDetails[index] = value
    def get_ExceptionalLatestDropOffDetails(self):
        return self.ExceptionalLatestDropOffDetails
    def set_ExceptionalLatestDropOffDetails(self, ExceptionalLatestDropOffDetails):
        self.ExceptionalLatestDropOffDetails = ExceptionalLatestDropOffDetails
    def add_ExceptionalLatestDropOffDetails(self, value):
        self.ExceptionalLatestDropOffDetails.append(value)
    def insert_ExceptionalLatestDropOffDetails_at(self, index, value):
        self.ExceptionalLatestDropOffDetails.insert(index, value)
    def replace_ExceptionalLatestDropOffDetails_at(self, index, value):
        self.ExceptionalLatestDropOffDetails[index] = value
    def get_EffectiveLatestDropOffDetails(self):
        return self.EffectiveLatestDropOffDetails
    def set_EffectiveLatestDropOffDetails(self, EffectiveLatestDropOffDetails):
        self.EffectiveLatestDropOffDetails = EffectiveLatestDropOffDetails
    def get_ShippingHolidays(self):
        return self.ShippingHolidays
    def set_ShippingHolidays(self, ShippingHolidays):
        self.ShippingHolidays = ShippingHolidays
    def add_ShippingHolidays(self, value):
        self.ShippingHolidays.append(value)
    def insert_ShippingHolidays_at(self, index, value):
        self.ShippingHolidays.insert(index, value)
    def replace_ShippingHolidays_at(self, index, value):
        self.ShippingHolidays[index] = value
    def validate_CarrierCodeType(self, value):
        result = True
        # Validate type CarrierCodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FDXC', 'FDXE', 'FDXG', 'FDXO', 'FXCC', 'FXFR', 'FXSP']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CarrierCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ServiceCategoryType(self, value):
        result = True
        # Validate type ServiceCategoryType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['EXPRESS_FREIGHT', 'EXPRESS_PARCEL', 'GROUND_HOME_DELIVERY']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ServiceCategoryType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CountryRelationshipType(self, value):
        result = True
        # Validate type CountryRelationshipType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['DOMESTIC', 'INTERNATIONAL']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CountryRelationshipType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Carrier is not None or
            self.ServiceCategory is not None or
            self.ServiceType is not None or
            self.CountryRelationship is not None or
            self.NormalLatestDropOffDetails or
            self.ExceptionalLatestDropOffDetails or
            self.EffectiveLatestDropOffDetails is not None or
            self.ShippingHolidays
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CarrierDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CarrierDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CarrierDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CarrierDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CarrierDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CarrierDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CarrierDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Carrier is not None:
            namespaceprefix_ = self.Carrier_nsprefix_ + ':' if (UseCapturedNS_ and self.Carrier_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCarrier>%s</%sCarrier>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Carrier), input_name='Carrier')), namespaceprefix_ , eol_))
        if self.ServiceCategory is not None:
            namespaceprefix_ = self.ServiceCategory_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceCategory_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceCategory>%s</%sServiceCategory>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServiceCategory), input_name='ServiceCategory')), namespaceprefix_ , eol_))
        if self.ServiceType is not None:
            namespaceprefix_ = self.ServiceType_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceType>%s</%sServiceType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServiceType), input_name='ServiceType')), namespaceprefix_ , eol_))
        if self.CountryRelationship is not None:
            namespaceprefix_ = self.CountryRelationship_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryRelationship_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryRelationship>%s</%sCountryRelationship>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryRelationship), input_name='CountryRelationship')), namespaceprefix_ , eol_))
        for NormalLatestDropOffDetails_ in self.NormalLatestDropOffDetails:
            namespaceprefix_ = self.NormalLatestDropOffDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.NormalLatestDropOffDetails_nsprefix_) else ''
            NormalLatestDropOffDetails_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='NormalLatestDropOffDetails', pretty_print=pretty_print)
        for ExceptionalLatestDropOffDetails_ in self.ExceptionalLatestDropOffDetails:
            namespaceprefix_ = self.ExceptionalLatestDropOffDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.ExceptionalLatestDropOffDetails_nsprefix_) else ''
            ExceptionalLatestDropOffDetails_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ExceptionalLatestDropOffDetails', pretty_print=pretty_print)
        if self.EffectiveLatestDropOffDetails is not None:
            namespaceprefix_ = self.EffectiveLatestDropOffDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.EffectiveLatestDropOffDetails_nsprefix_) else ''
            self.EffectiveLatestDropOffDetails.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EffectiveLatestDropOffDetails', pretty_print=pretty_print)
        for ShippingHolidays_ in self.ShippingHolidays:
            namespaceprefix_ = self.ShippingHolidays_nsprefix_ + ':' if (UseCapturedNS_ and self.ShippingHolidays_nsprefix_) else ''
            ShippingHolidays_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShippingHolidays', pretty_print=pretty_print)
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
        if nodeName_ == 'Carrier':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Carrier')
            value_ = self.gds_validate_string(value_, node, 'Carrier')
            self.Carrier = value_
            self.Carrier_nsprefix_ = child_.prefix
            # validate type CarrierCodeType
            self.validate_CarrierCodeType(self.Carrier)
        elif nodeName_ == 'ServiceCategory':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServiceCategory')
            value_ = self.gds_validate_string(value_, node, 'ServiceCategory')
            self.ServiceCategory = value_
            self.ServiceCategory_nsprefix_ = child_.prefix
            # validate type ServiceCategoryType
            self.validate_ServiceCategoryType(self.ServiceCategory)
        elif nodeName_ == 'ServiceType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServiceType')
            value_ = self.gds_validate_string(value_, node, 'ServiceType')
            self.ServiceType = value_
            self.ServiceType_nsprefix_ = child_.prefix
        elif nodeName_ == 'CountryRelationship':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryRelationship')
            value_ = self.gds_validate_string(value_, node, 'CountryRelationship')
            self.CountryRelationship = value_
            self.CountryRelationship_nsprefix_ = child_.prefix
            # validate type CountryRelationshipType
            self.validate_CountryRelationshipType(self.CountryRelationship)
        elif nodeName_ == 'NormalLatestDropOffDetails':
            obj_ = LatestDropOffDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.NormalLatestDropOffDetails.append(obj_)
            obj_.original_tagname_ = 'NormalLatestDropOffDetails'
        elif nodeName_ == 'ExceptionalLatestDropOffDetails':
            obj_ = LatestDropOffDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ExceptionalLatestDropOffDetails.append(obj_)
            obj_.original_tagname_ = 'ExceptionalLatestDropOffDetails'
        elif nodeName_ == 'EffectiveLatestDropOffDetails':
            obj_ = LatestDropOffDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EffectiveLatestDropOffDetails = obj_
            obj_.original_tagname_ = 'EffectiveLatestDropOffDetails'
        elif nodeName_ == 'ShippingHolidays':
            obj_ = ShippingHoliday.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShippingHolidays.append(obj_)
            obj_.original_tagname_ = 'ShippingHolidays'
# end class CarrierDetail


class ClearanceCountryDetail(GeneratedsSuper):
    """Specifies the special services supported at the clearance location for
    an individual destination country."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ClearanceCountry=None, ServicesSupported=None, SpecialServicesSupported=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ClearanceCountry = ClearanceCountry
        self.ClearanceCountry_nsprefix_ = None
        if ServicesSupported is None:
            self.ServicesSupported = []
        else:
            self.ServicesSupported = ServicesSupported
        self.ServicesSupported_nsprefix_ = None
        if SpecialServicesSupported is None:
            self.SpecialServicesSupported = []
        else:
            self.SpecialServicesSupported = SpecialServicesSupported
        self.SpecialServicesSupported_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ClearanceCountryDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ClearanceCountryDetail.subclass:
            return ClearanceCountryDetail.subclass(*args_, **kwargs_)
        else:
            return ClearanceCountryDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ClearanceCountry(self):
        return self.ClearanceCountry
    def set_ClearanceCountry(self, ClearanceCountry):
        self.ClearanceCountry = ClearanceCountry
    def get_ServicesSupported(self):
        return self.ServicesSupported
    def set_ServicesSupported(self, ServicesSupported):
        self.ServicesSupported = ServicesSupported
    def add_ServicesSupported(self, value):
        self.ServicesSupported.append(value)
    def insert_ServicesSupported_at(self, index, value):
        self.ServicesSupported.insert(index, value)
    def replace_ServicesSupported_at(self, index, value):
        self.ServicesSupported[index] = value
    def get_SpecialServicesSupported(self):
        return self.SpecialServicesSupported
    def set_SpecialServicesSupported(self, SpecialServicesSupported):
        self.SpecialServicesSupported = SpecialServicesSupported
    def add_SpecialServicesSupported(self, value):
        self.SpecialServicesSupported.append(value)
    def insert_SpecialServicesSupported_at(self, index, value):
        self.SpecialServicesSupported.insert(index, value)
    def replace_SpecialServicesSupported_at(self, index, value):
        self.SpecialServicesSupported[index] = value
    def hasContent_(self):
        if (
            self.ClearanceCountry is not None or
            self.ServicesSupported or
            self.SpecialServicesSupported
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ClearanceCountryDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ClearanceCountryDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ClearanceCountryDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ClearanceCountryDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ClearanceCountryDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ClearanceCountryDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ClearanceCountryDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ClearanceCountry is not None:
            namespaceprefix_ = self.ClearanceCountry_nsprefix_ + ':' if (UseCapturedNS_ and self.ClearanceCountry_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sClearanceCountry>%s</%sClearanceCountry>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ClearanceCountry), input_name='ClearanceCountry')), namespaceprefix_ , eol_))
        for ServicesSupported_ in self.ServicesSupported:
            namespaceprefix_ = self.ServicesSupported_nsprefix_ + ':' if (UseCapturedNS_ and self.ServicesSupported_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServicesSupported>%s</%sServicesSupported>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(ServicesSupported_), input_name='ServicesSupported')), namespaceprefix_ , eol_))
        for SpecialServicesSupported_ in self.SpecialServicesSupported:
            namespaceprefix_ = self.SpecialServicesSupported_nsprefix_ + ':' if (UseCapturedNS_ and self.SpecialServicesSupported_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSpecialServicesSupported>%s</%sSpecialServicesSupported>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(SpecialServicesSupported_), input_name='SpecialServicesSupported')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ClearanceCountry':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ClearanceCountry')
            value_ = self.gds_validate_string(value_, node, 'ClearanceCountry')
            self.ClearanceCountry = value_
            self.ClearanceCountry_nsprefix_ = child_.prefix
        elif nodeName_ == 'ServicesSupported':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServicesSupported')
            value_ = self.gds_validate_string(value_, node, 'ServicesSupported')
            self.ServicesSupported.append(value_)
            self.ServicesSupported_nsprefix_ = child_.prefix
        elif nodeName_ == 'SpecialServicesSupported':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SpecialServicesSupported')
            value_ = self.gds_validate_string(value_, node, 'SpecialServicesSupported')
            self.SpecialServicesSupported.append(value_)
            self.SpecialServicesSupported_nsprefix_ = child_.prefix
# end class ClearanceCountryDetail


class ClearanceLocationDetail(GeneratedsSuper):
    """Specifies the details about the countries supported by this location."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ServicesSupported=None, ConsolidationType=None, ClearanceLocationType=None, SpecialServicesSupported=None, ClearanceCountries=None, ClearanceRoutingCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if ServicesSupported is None:
            self.ServicesSupported = []
        else:
            self.ServicesSupported = ServicesSupported
        self.ServicesSupported_nsprefix_ = None
        self.ConsolidationType = ConsolidationType
        self.validate_ConsolidationType(self.ConsolidationType)
        self.ConsolidationType_nsprefix_ = "ns"
        self.ClearanceLocationType = ClearanceLocationType
        self.validate_DistributionClearanceType(self.ClearanceLocationType)
        self.ClearanceLocationType_nsprefix_ = "ns"
        if SpecialServicesSupported is None:
            self.SpecialServicesSupported = []
        else:
            self.SpecialServicesSupported = SpecialServicesSupported
        self.SpecialServicesSupported_nsprefix_ = None
        if ClearanceCountries is None:
            self.ClearanceCountries = []
        else:
            self.ClearanceCountries = ClearanceCountries
        self.ClearanceCountries_nsprefix_ = "ns"
        self.ClearanceRoutingCode = ClearanceRoutingCode
        self.ClearanceRoutingCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ClearanceLocationDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ClearanceLocationDetail.subclass:
            return ClearanceLocationDetail.subclass(*args_, **kwargs_)
        else:
            return ClearanceLocationDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ServicesSupported(self):
        return self.ServicesSupported
    def set_ServicesSupported(self, ServicesSupported):
        self.ServicesSupported = ServicesSupported
    def add_ServicesSupported(self, value):
        self.ServicesSupported.append(value)
    def insert_ServicesSupported_at(self, index, value):
        self.ServicesSupported.insert(index, value)
    def replace_ServicesSupported_at(self, index, value):
        self.ServicesSupported[index] = value
    def get_ConsolidationType(self):
        return self.ConsolidationType
    def set_ConsolidationType(self, ConsolidationType):
        self.ConsolidationType = ConsolidationType
    def get_ClearanceLocationType(self):
        return self.ClearanceLocationType
    def set_ClearanceLocationType(self, ClearanceLocationType):
        self.ClearanceLocationType = ClearanceLocationType
    def get_SpecialServicesSupported(self):
        return self.SpecialServicesSupported
    def set_SpecialServicesSupported(self, SpecialServicesSupported):
        self.SpecialServicesSupported = SpecialServicesSupported
    def add_SpecialServicesSupported(self, value):
        self.SpecialServicesSupported.append(value)
    def insert_SpecialServicesSupported_at(self, index, value):
        self.SpecialServicesSupported.insert(index, value)
    def replace_SpecialServicesSupported_at(self, index, value):
        self.SpecialServicesSupported[index] = value
    def get_ClearanceCountries(self):
        return self.ClearanceCountries
    def set_ClearanceCountries(self, ClearanceCountries):
        self.ClearanceCountries = ClearanceCountries
    def add_ClearanceCountries(self, value):
        self.ClearanceCountries.append(value)
    def insert_ClearanceCountries_at(self, index, value):
        self.ClearanceCountries.insert(index, value)
    def replace_ClearanceCountries_at(self, index, value):
        self.ClearanceCountries[index] = value
    def get_ClearanceRoutingCode(self):
        return self.ClearanceRoutingCode
    def set_ClearanceRoutingCode(self, ClearanceRoutingCode):
        self.ClearanceRoutingCode = ClearanceRoutingCode
    def validate_ConsolidationType(self, value):
        result = True
        # Validate type ConsolidationType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['INTERNATIONAL_DISTRIBUTION_FREIGHT', 'INTERNATIONAL_ECONOMY_DISTRIBUTION', 'INTERNATIONAL_GROUND_DISTRIBUTION', 'INTERNATIONAL_PRIORITY_DISTRIBUTION', 'TRANSBORDER_DISTRIBUTION']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ConsolidationType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DistributionClearanceType(self, value):
        result = True
        # Validate type DistributionClearanceType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['DESTINATION_COUNTRY_CLEARANCE', 'SINGLE_POINT_OF_CLEARANCE']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DistributionClearanceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.ServicesSupported or
            self.ConsolidationType is not None or
            self.ClearanceLocationType is not None or
            self.SpecialServicesSupported or
            self.ClearanceCountries or
            self.ClearanceRoutingCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ClearanceLocationDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ClearanceLocationDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ClearanceLocationDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ClearanceLocationDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ClearanceLocationDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ClearanceLocationDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ClearanceLocationDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for ServicesSupported_ in self.ServicesSupported:
            namespaceprefix_ = self.ServicesSupported_nsprefix_ + ':' if (UseCapturedNS_ and self.ServicesSupported_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServicesSupported>%s</%sServicesSupported>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(ServicesSupported_), input_name='ServicesSupported')), namespaceprefix_ , eol_))
        if self.ConsolidationType is not None:
            namespaceprefix_ = self.ConsolidationType_nsprefix_ + ':' if (UseCapturedNS_ and self.ConsolidationType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sConsolidationType>%s</%sConsolidationType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ConsolidationType), input_name='ConsolidationType')), namespaceprefix_ , eol_))
        if self.ClearanceLocationType is not None:
            namespaceprefix_ = self.ClearanceLocationType_nsprefix_ + ':' if (UseCapturedNS_ and self.ClearanceLocationType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sClearanceLocationType>%s</%sClearanceLocationType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ClearanceLocationType), input_name='ClearanceLocationType')), namespaceprefix_ , eol_))
        for SpecialServicesSupported_ in self.SpecialServicesSupported:
            namespaceprefix_ = self.SpecialServicesSupported_nsprefix_ + ':' if (UseCapturedNS_ and self.SpecialServicesSupported_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSpecialServicesSupported>%s</%sSpecialServicesSupported>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(SpecialServicesSupported_), input_name='SpecialServicesSupported')), namespaceprefix_ , eol_))
        for ClearanceCountries_ in self.ClearanceCountries:
            namespaceprefix_ = self.ClearanceCountries_nsprefix_ + ':' if (UseCapturedNS_ and self.ClearanceCountries_nsprefix_) else ''
            ClearanceCountries_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClearanceCountries', pretty_print=pretty_print)
        if self.ClearanceRoutingCode is not None:
            namespaceprefix_ = self.ClearanceRoutingCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ClearanceRoutingCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sClearanceRoutingCode>%s</%sClearanceRoutingCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ClearanceRoutingCode), input_name='ClearanceRoutingCode')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ServicesSupported':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServicesSupported')
            value_ = self.gds_validate_string(value_, node, 'ServicesSupported')
            self.ServicesSupported.append(value_)
            self.ServicesSupported_nsprefix_ = child_.prefix
        elif nodeName_ == 'ConsolidationType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ConsolidationType')
            value_ = self.gds_validate_string(value_, node, 'ConsolidationType')
            self.ConsolidationType = value_
            self.ConsolidationType_nsprefix_ = child_.prefix
            # validate type ConsolidationType
            self.validate_ConsolidationType(self.ConsolidationType)
        elif nodeName_ == 'ClearanceLocationType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ClearanceLocationType')
            value_ = self.gds_validate_string(value_, node, 'ClearanceLocationType')
            self.ClearanceLocationType = value_
            self.ClearanceLocationType_nsprefix_ = child_.prefix
            # validate type DistributionClearanceType
            self.validate_DistributionClearanceType(self.ClearanceLocationType)
        elif nodeName_ == 'SpecialServicesSupported':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SpecialServicesSupported')
            value_ = self.gds_validate_string(value_, node, 'SpecialServicesSupported')
            self.SpecialServicesSupported.append(value_)
            self.SpecialServicesSupported_nsprefix_ = child_.prefix
        elif nodeName_ == 'ClearanceCountries':
            obj_ = ClearanceCountryDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClearanceCountries.append(obj_)
            obj_.original_tagname_ = 'ClearanceCountries'
        elif nodeName_ == 'ClearanceRoutingCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ClearanceRoutingCode')
            value_ = self.gds_validate_string(value_, node, 'ClearanceRoutingCode')
            self.ClearanceRoutingCode = value_
            self.ClearanceRoutingCode_nsprefix_ = child_.prefix
# end class ClearanceLocationDetail


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


class DateRange(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Begins=None, Ends=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if isinstance(Begins, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Begins, '%Y-%m-%d').date()
        else:
            initvalue_ = Begins
        self.Begins = initvalue_
        self.Begins_nsprefix_ = None
        if isinstance(Ends, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Ends, '%Y-%m-%d').date()
        else:
            initvalue_ = Ends
        self.Ends = initvalue_
        self.Ends_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DateRange)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DateRange.subclass:
            return DateRange.subclass(*args_, **kwargs_)
        else:
            return DateRange(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DateRange', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DateRange')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DateRange':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DateRange')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DateRange', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DateRange'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DateRange', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Begins is not None:
            namespaceprefix_ = self.Begins_nsprefix_ + ':' if (UseCapturedNS_ and self.Begins_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBegins>%s</%sBegins>%s' % (namespaceprefix_ , self.gds_format_date(self.Begins, input_name='Begins'), namespaceprefix_ , eol_))
        if self.Ends is not None:
            namespaceprefix_ = self.Ends_nsprefix_ + ':' if (UseCapturedNS_ and self.Ends_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEnds>%s</%sEnds>%s' % (namespaceprefix_ , self.gds_format_date(self.Ends, input_name='Ends'), namespaceprefix_ , eol_))
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
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.Begins = dval_
            self.Begins_nsprefix_ = child_.prefix
        elif nodeName_ == 'Ends':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.Ends = dval_
            self.Ends_nsprefix_ = child_.prefix
# end class DateRange


class Dimensions(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Length=None, Width=None, Height=None, Units=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Length = Length
        self.Length_nsprefix_ = None
        self.Width = Width
        self.Width_nsprefix_ = None
        self.Height = Height
        self.Height_nsprefix_ = None
        self.Units = Units
        self.validate_LinearUnits(self.Units)
        self.Units_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Dimensions)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Dimensions.subclass:
            return Dimensions.subclass(*args_, **kwargs_)
        else:
            return Dimensions(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Length(self):
        return self.Length
    def set_Length(self, Length):
        self.Length = Length
    def get_Width(self):
        return self.Width
    def set_Width(self, Width):
        self.Width = Width
    def get_Height(self):
        return self.Height
    def set_Height(self, Height):
        self.Height = Height
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
            self.Length is not None or
            self.Width is not None or
            self.Height is not None or
            self.Units is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Dimensions', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Dimensions')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Dimensions':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Dimensions')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Dimensions', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Dimensions'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Dimensions', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Length is not None:
            namespaceprefix_ = self.Length_nsprefix_ + ':' if (UseCapturedNS_ and self.Length_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLength>%s</%sLength>%s' % (namespaceprefix_ , self.gds_format_integer(self.Length, input_name='Length'), namespaceprefix_ , eol_))
        if self.Width is not None:
            namespaceprefix_ = self.Width_nsprefix_ + ':' if (UseCapturedNS_ and self.Width_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWidth>%s</%sWidth>%s' % (namespaceprefix_ , self.gds_format_integer(self.Width, input_name='Width'), namespaceprefix_ , eol_))
        if self.Height is not None:
            namespaceprefix_ = self.Height_nsprefix_ + ':' if (UseCapturedNS_ and self.Height_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHeight>%s</%sHeight>%s' % (namespaceprefix_ , self.gds_format_integer(self.Height, input_name='Height'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Length' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Length')
            if ival_ < 0:
                raise_parse_error(child_, 'requires nonNegativeInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'Length')
            self.Length = ival_
            self.Length_nsprefix_ = child_.prefix
        elif nodeName_ == 'Width' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Width')
            if ival_ < 0:
                raise_parse_error(child_, 'requires nonNegativeInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'Width')
            self.Width = ival_
            self.Width_nsprefix_ = child_.prefix
        elif nodeName_ == 'Height' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Height')
            if ival_ < 0:
                raise_parse_error(child_, 'requires nonNegativeInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'Height')
            self.Height = ival_
            self.Height_nsprefix_ = child_.prefix
        elif nodeName_ == 'Units':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Units')
            value_ = self.gds_validate_string(value_, node, 'Units')
            self.Units = value_
            self.Units_nsprefix_ = child_.prefix
            # validate type LinearUnits
            self.validate_LinearUnits(self.Units)
# end class Dimensions


class Distance(GeneratedsSuper):
    """Driving or other transportation distances, distinct from dimension
    measurements."""
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
        self.validate_DistanceUnits(self.Units)
        self.Units_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Distance)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Distance.subclass:
            return Distance.subclass(*args_, **kwargs_)
        else:
            return Distance(*args_, **kwargs_)
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
    def validate_DistanceUnits(self, value):
        result = True
        # Validate type DistanceUnits, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['KM', 'MI']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DistanceUnits' % {"value" : encode_str_2_3(value), "lineno": lineno} )
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Distance', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Distance')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Distance':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Distance')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Distance', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Distance'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Distance', fromsubclass_=False, pretty_print=True):
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
            # validate type DistanceUnits
            self.validate_DistanceUnits(self.Units)
# end class Distance


class DistanceAndLocationDetail(GeneratedsSuper):
    """Specifies the location details and other information relevant to the
    location that is derived from the inputs provided in the request."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Distance=None, ReservationAvailabilityDetail=None, SupportedRedirectToHoldServices=None, LocationDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Distance = Distance
        self.Distance_nsprefix_ = "ns"
        self.ReservationAvailabilityDetail = ReservationAvailabilityDetail
        self.ReservationAvailabilityDetail_nsprefix_ = "ns"
        if SupportedRedirectToHoldServices is None:
            self.SupportedRedirectToHoldServices = []
        else:
            self.SupportedRedirectToHoldServices = SupportedRedirectToHoldServices
        self.SupportedRedirectToHoldServices_nsprefix_ = "ns"
        self.LocationDetail = LocationDetail
        self.LocationDetail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DistanceAndLocationDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DistanceAndLocationDetail.subclass:
            return DistanceAndLocationDetail.subclass(*args_, **kwargs_)
        else:
            return DistanceAndLocationDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Distance(self):
        return self.Distance
    def set_Distance(self, Distance):
        self.Distance = Distance
    def get_ReservationAvailabilityDetail(self):
        return self.ReservationAvailabilityDetail
    def set_ReservationAvailabilityDetail(self, ReservationAvailabilityDetail):
        self.ReservationAvailabilityDetail = ReservationAvailabilityDetail
    def get_SupportedRedirectToHoldServices(self):
        return self.SupportedRedirectToHoldServices
    def set_SupportedRedirectToHoldServices(self, SupportedRedirectToHoldServices):
        self.SupportedRedirectToHoldServices = SupportedRedirectToHoldServices
    def add_SupportedRedirectToHoldServices(self, value):
        self.SupportedRedirectToHoldServices.append(value)
    def insert_SupportedRedirectToHoldServices_at(self, index, value):
        self.SupportedRedirectToHoldServices.insert(index, value)
    def replace_SupportedRedirectToHoldServices_at(self, index, value):
        self.SupportedRedirectToHoldServices[index] = value
    def get_LocationDetail(self):
        return self.LocationDetail
    def set_LocationDetail(self, LocationDetail):
        self.LocationDetail = LocationDetail
    def validate_SupportedRedirectToHoldServiceType(self, value):
        result = True
        # Validate type SupportedRedirectToHoldServiceType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FEDEX_EXPRESS', 'FEDEX_GROUND', 'FEDEX_GROUND_HOME_DELIVERY']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on SupportedRedirectToHoldServiceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Distance is not None or
            self.ReservationAvailabilityDetail is not None or
            self.SupportedRedirectToHoldServices or
            self.LocationDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DistanceAndLocationDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DistanceAndLocationDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DistanceAndLocationDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DistanceAndLocationDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DistanceAndLocationDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DistanceAndLocationDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DistanceAndLocationDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Distance is not None:
            namespaceprefix_ = self.Distance_nsprefix_ + ':' if (UseCapturedNS_ and self.Distance_nsprefix_) else ''
            self.Distance.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Distance', pretty_print=pretty_print)
        if self.ReservationAvailabilityDetail is not None:
            namespaceprefix_ = self.ReservationAvailabilityDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ReservationAvailabilityDetail_nsprefix_) else ''
            self.ReservationAvailabilityDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ReservationAvailabilityDetail', pretty_print=pretty_print)
        for SupportedRedirectToHoldServices_ in self.SupportedRedirectToHoldServices:
            namespaceprefix_ = self.SupportedRedirectToHoldServices_nsprefix_ + ':' if (UseCapturedNS_ and self.SupportedRedirectToHoldServices_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSupportedRedirectToHoldServices>%s</%sSupportedRedirectToHoldServices>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(SupportedRedirectToHoldServices_), input_name='SupportedRedirectToHoldServices')), namespaceprefix_ , eol_))
        if self.LocationDetail is not None:
            namespaceprefix_ = self.LocationDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.LocationDetail_nsprefix_) else ''
            self.LocationDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='LocationDetail', pretty_print=pretty_print)
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
        if nodeName_ == 'Distance':
            obj_ = Distance.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Distance = obj_
            obj_.original_tagname_ = 'Distance'
        elif nodeName_ == 'ReservationAvailabilityDetail':
            obj_ = ReservationAvailabilityDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ReservationAvailabilityDetail = obj_
            obj_.original_tagname_ = 'ReservationAvailabilityDetail'
        elif nodeName_ == 'SupportedRedirectToHoldServices':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SupportedRedirectToHoldServices')
            value_ = self.gds_validate_string(value_, node, 'SupportedRedirectToHoldServices')
            self.SupportedRedirectToHoldServices.append(value_)
            self.SupportedRedirectToHoldServices_nsprefix_ = child_.prefix
            # validate type SupportedRedirectToHoldServiceType
            self.validate_SupportedRedirectToHoldServiceType(self.SupportedRedirectToHoldServices[-1])
        elif nodeName_ == 'LocationDetail':
            obj_ = LocationDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LocationDetail = obj_
            obj_.original_tagname_ = 'LocationDetail'
# end class DistanceAndLocationDetail


class EnterprisePrivilegeDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Id=None, Permission=None, CarrierCode=None, EffectiveDateRange=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Id = Id
        self.Id_nsprefix_ = None
        self.Permission = Permission
        self.validate_EnterprisePermissionType(self.Permission)
        self.Permission_nsprefix_ = "ns"
        self.CarrierCode = CarrierCode
        self.validate_CarrierCodeType(self.CarrierCode)
        self.CarrierCode_nsprefix_ = "ns"
        self.EffectiveDateRange = EffectiveDateRange
        self.EffectiveDateRange_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EnterprisePrivilegeDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EnterprisePrivilegeDetail.subclass:
            return EnterprisePrivilegeDetail.subclass(*args_, **kwargs_)
        else:
            return EnterprisePrivilegeDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def get_Permission(self):
        return self.Permission
    def set_Permission(self, Permission):
        self.Permission = Permission
    def get_CarrierCode(self):
        return self.CarrierCode
    def set_CarrierCode(self, CarrierCode):
        self.CarrierCode = CarrierCode
    def get_EffectiveDateRange(self):
        return self.EffectiveDateRange
    def set_EffectiveDateRange(self, EffectiveDateRange):
        self.EffectiveDateRange = EffectiveDateRange
    def validate_EnterprisePermissionType(self, value):
        result = True
        # Validate type EnterprisePermissionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ALLOWED', 'ALLOWED_BY_EXCEPTION', 'DISALLOWED']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on EnterprisePermissionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CarrierCodeType(self, value):
        result = True
        # Validate type CarrierCodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FDXC', 'FDXE', 'FDXG', 'FDXO', 'FXCC', 'FXFR', 'FXSP']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CarrierCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Id is not None or
            self.Permission is not None or
            self.CarrierCode is not None or
            self.EffectiveDateRange is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EnterprisePrivilegeDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EnterprisePrivilegeDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EnterprisePrivilegeDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EnterprisePrivilegeDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='EnterprisePrivilegeDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EnterprisePrivilegeDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EnterprisePrivilegeDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Id is not None:
            namespaceprefix_ = self.Id_nsprefix_ + ':' if (UseCapturedNS_ and self.Id_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sId>%s</%sId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Id), input_name='Id')), namespaceprefix_ , eol_))
        if self.Permission is not None:
            namespaceprefix_ = self.Permission_nsprefix_ + ':' if (UseCapturedNS_ and self.Permission_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPermission>%s</%sPermission>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Permission), input_name='Permission')), namespaceprefix_ , eol_))
        if self.CarrierCode is not None:
            namespaceprefix_ = self.CarrierCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CarrierCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCarrierCode>%s</%sCarrierCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CarrierCode), input_name='CarrierCode')), namespaceprefix_ , eol_))
        if self.EffectiveDateRange is not None:
            namespaceprefix_ = self.EffectiveDateRange_nsprefix_ + ':' if (UseCapturedNS_ and self.EffectiveDateRange_nsprefix_) else ''
            self.EffectiveDateRange.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EffectiveDateRange', pretty_print=pretty_print)
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
        elif nodeName_ == 'Permission':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Permission')
            value_ = self.gds_validate_string(value_, node, 'Permission')
            self.Permission = value_
            self.Permission_nsprefix_ = child_.prefix
            # validate type EnterprisePermissionType
            self.validate_EnterprisePermissionType(self.Permission)
        elif nodeName_ == 'CarrierCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CarrierCode')
            value_ = self.gds_validate_string(value_, node, 'CarrierCode')
            self.CarrierCode = value_
            self.CarrierCode_nsprefix_ = child_.prefix
            # validate type CarrierCodeType
            self.validate_CarrierCodeType(self.CarrierCode)
        elif nodeName_ == 'EffectiveDateRange':
            obj_ = DateRange.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EffectiveDateRange = obj_
            obj_.original_tagname_ = 'EffectiveDateRange'
# end class EnterprisePrivilegeDetail


class Holiday(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Name=None, Date=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = None
        if isinstance(Date, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Date, '%Y-%m-%d').date()
        else:
            initvalue_ = Date
        self.Date = initvalue_
        self.Date_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Holiday)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Holiday.subclass:
            return Holiday.subclass(*args_, **kwargs_)
        else:
            return Holiday(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def get_Date(self):
        return self.Date
    def set_Date(self, Date):
        self.Date = Date
    def hasContent_(self):
        if (
            self.Name is not None or
            self.Date is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Holiday', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Holiday')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Holiday':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Holiday')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Holiday', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Holiday'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Holiday', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName>%s</%sName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name), input_name='Name')), namespaceprefix_ , eol_))
        if self.Date is not None:
            namespaceprefix_ = self.Date_nsprefix_ + ':' if (UseCapturedNS_ and self.Date_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDate>%s</%sDate>%s' % (namespaceprefix_ , self.gds_format_date(self.Date, input_name='Date'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Name')
            value_ = self.gds_validate_string(value_, node, 'Name')
            self.Name = value_
            self.Name_nsprefix_ = child_.prefix
        elif nodeName_ == 'Date':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.Date = dval_
            self.Date_nsprefix_ = child_.prefix
# end class Holiday


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


class LatestDropOffDetail(GeneratedsSuper):
    """Specifies the latest time by which a package can be dropped off at a
    FedEx location."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DayOfWeek=None, Time=None, Overlays=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DayOfWeek = DayOfWeek
        self.validate_DayOfWeekType(self.DayOfWeek)
        self.DayOfWeek_nsprefix_ = "ns"
        if isinstance(Time, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Time, '%H:%M:%S').time()
        else:
            initvalue_ = Time
        self.Time = initvalue_
        self.Time_nsprefix_ = None
        if Overlays is None:
            self.Overlays = []
        else:
            self.Overlays = Overlays
        self.Overlays_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LatestDropOffDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LatestDropOffDetail.subclass:
            return LatestDropOffDetail.subclass(*args_, **kwargs_)
        else:
            return LatestDropOffDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DayOfWeek(self):
        return self.DayOfWeek
    def set_DayOfWeek(self, DayOfWeek):
        self.DayOfWeek = DayOfWeek
    def get_Time(self):
        return self.Time
    def set_Time(self, Time):
        self.Time = Time
    def get_Overlays(self):
        return self.Overlays
    def set_Overlays(self, Overlays):
        self.Overlays = Overlays
    def add_Overlays(self, value):
        self.Overlays.append(value)
    def insert_Overlays_at(self, index, value):
        self.Overlays.insert(index, value)
    def replace_Overlays_at(self, index, value):
        self.Overlays[index] = value
    def validate_DayOfWeekType(self, value):
        result = True
        # Validate type DayOfWeekType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FRI', 'MON', 'SAT', 'SUN', 'THU', 'TUE', 'WED']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DayOfWeekType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.DayOfWeek is not None or
            self.Time is not None or
            self.Overlays
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LatestDropOffDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LatestDropOffDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LatestDropOffDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LatestDropOffDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LatestDropOffDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LatestDropOffDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LatestDropOffDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DayOfWeek is not None:
            namespaceprefix_ = self.DayOfWeek_nsprefix_ + ':' if (UseCapturedNS_ and self.DayOfWeek_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDayOfWeek>%s</%sDayOfWeek>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DayOfWeek), input_name='DayOfWeek')), namespaceprefix_ , eol_))
        if self.Time is not None:
            namespaceprefix_ = self.Time_nsprefix_ + ':' if (UseCapturedNS_ and self.Time_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTime>%s</%sTime>%s' % (namespaceprefix_ , self.gds_format_time(self.Time, input_name='Time'), namespaceprefix_ , eol_))
        for Overlays_ in self.Overlays:
            namespaceprefix_ = self.Overlays_nsprefix_ + ':' if (UseCapturedNS_ and self.Overlays_nsprefix_) else ''
            Overlays_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Overlays', pretty_print=pretty_print)
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
        if nodeName_ == 'DayOfWeek':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DayOfWeek')
            value_ = self.gds_validate_string(value_, node, 'DayOfWeek')
            self.DayOfWeek = value_
            self.DayOfWeek_nsprefix_ = child_.prefix
            # validate type DayOfWeekType
            self.validate_DayOfWeekType(self.DayOfWeek)
        elif nodeName_ == 'Time':
            sval_ = child_.text
            dval_ = self.gds_parse_time(sval_)
            self.Time = dval_
            self.Time_nsprefix_ = child_.prefix
        elif nodeName_ == 'Overlays':
            obj_ = LatestDropoffOverlayDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Overlays.append(obj_)
            obj_.original_tagname_ = 'Overlays'
# end class LatestDropOffDetail


class LatestDropoffOverlayDetail(GeneratedsSuper):
    """Specifies the time and reason to overlay the last drop off time for a
    carrier at a FedEx location."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Type=None, Time=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Type = Type
        self.validate_LatestDropOffOverlayType(self.Type)
        self.Type_nsprefix_ = "ns"
        if isinstance(Time, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Time, '%H:%M:%S').time()
        else:
            initvalue_ = Time
        self.Time = initvalue_
        self.Time_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LatestDropoffOverlayDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LatestDropoffOverlayDetail.subclass:
            return LatestDropoffOverlayDetail.subclass(*args_, **kwargs_)
        else:
            return LatestDropoffOverlayDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_Time(self):
        return self.Time
    def set_Time(self, Time):
        self.Time = Time
    def validate_LatestDropOffOverlayType(self, value):
        result = True
        # Validate type LatestDropOffOverlayType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['US_WEST_COAST']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on LatestDropOffOverlayType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Type is not None or
            self.Time is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LatestDropoffOverlayDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LatestDropoffOverlayDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LatestDropoffOverlayDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LatestDropoffOverlayDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LatestDropoffOverlayDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LatestDropoffOverlayDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LatestDropoffOverlayDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sType>%s</%sType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Type), input_name='Type')), namespaceprefix_ , eol_))
        if self.Time is not None:
            namespaceprefix_ = self.Time_nsprefix_ + ':' if (UseCapturedNS_ and self.Time_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTime>%s</%sTime>%s' % (namespaceprefix_ , self.gds_format_time(self.Time, input_name='Time'), namespaceprefix_ , eol_))
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
            # validate type LatestDropOffOverlayType
            self.validate_LatestDropOffOverlayType(self.Type)
        elif nodeName_ == 'Time':
            sval_ = child_.text
            dval_ = self.gds_parse_time(sval_)
            self.Time = dval_
            self.Time_nsprefix_ = child_.prefix
# end class LatestDropoffOverlayDetail


class ListLocationsConstraints(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, RequiredLocationAttributes=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if RequiredLocationAttributes is None:
            self.RequiredLocationAttributes = []
        else:
            self.RequiredLocationAttributes = RequiredLocationAttributes
        self.RequiredLocationAttributes_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ListLocationsConstraints)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ListLocationsConstraints.subclass:
            return ListLocationsConstraints.subclass(*args_, **kwargs_)
        else:
            return ListLocationsConstraints(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_RequiredLocationAttributes(self):
        return self.RequiredLocationAttributes
    def set_RequiredLocationAttributes(self, RequiredLocationAttributes):
        self.RequiredLocationAttributes = RequiredLocationAttributes
    def add_RequiredLocationAttributes(self, value):
        self.RequiredLocationAttributes.append(value)
    def insert_RequiredLocationAttributes_at(self, index, value):
        self.RequiredLocationAttributes.insert(index, value)
    def replace_RequiredLocationAttributes_at(self, index, value):
        self.RequiredLocationAttributes[index] = value
    def validate_LocationAttributesType(self, value):
        result = True
        # Validate type LocationAttributesType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ACCEPTS_CASH', 'ALREADY_OPEN', 'CLEARANCE_SERVICES', 'COPY_AND_PRINT_SERVICES', 'DANGEROUS_GOODS_SERVICES', 'DIRECT_MAIL_SERVICES', 'DOMESTIC_SHIPPING_SERVICES', 'DROP_BOX', 'INTERNATIONAL_SHIPPING_SERVICES', 'LOCATION_IS_IN_AIRPORT', 'NOTARY_SERVICES', 'OBSERVES_DAY_LIGHT_SAVING_TIMES', 'OPEN_TWENTY_FOUR_HOURS', 'PACKAGING_SUPPLIES', 'PACK_AND_SHIP', 'PASSPORT_PHOTO_SERVICES', 'RETURNS_SERVICES', 'SIGNS_AND_BANNERS_SERVICE', 'SONY_PICTURE_STATION']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on LocationAttributesType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.RequiredLocationAttributes
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ListLocationsConstraints', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ListLocationsConstraints')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ListLocationsConstraints':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ListLocationsConstraints')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ListLocationsConstraints', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ListLocationsConstraints'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ListLocationsConstraints', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for RequiredLocationAttributes_ in self.RequiredLocationAttributes:
            namespaceprefix_ = self.RequiredLocationAttributes_nsprefix_ + ':' if (UseCapturedNS_ and self.RequiredLocationAttributes_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRequiredLocationAttributes>%s</%sRequiredLocationAttributes>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(RequiredLocationAttributes_), input_name='RequiredLocationAttributes')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'RequiredLocationAttributes':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RequiredLocationAttributes')
            value_ = self.gds_validate_string(value_, node, 'RequiredLocationAttributes')
            self.RequiredLocationAttributes.append(value_)
            self.RequiredLocationAttributes_nsprefix_ = child_.prefix
            # validate type LocationAttributesType
            self.validate_LocationAttributesType(self.RequiredLocationAttributes[-1])
# end class ListLocationsConstraints


class ListLocationsReply(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, LocationDetails=None, gds_collector_=None, **kwargs_):
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
        if LocationDetails is None:
            self.LocationDetails = []
        else:
            self.LocationDetails = LocationDetails
        self.LocationDetails_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ListLocationsReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ListLocationsReply.subclass:
            return ListLocationsReply.subclass(*args_, **kwargs_)
        else:
            return ListLocationsReply(*args_, **kwargs_)
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
    def get_LocationDetails(self):
        return self.LocationDetails
    def set_LocationDetails(self, LocationDetails):
        self.LocationDetails = LocationDetails
    def add_LocationDetails(self, value):
        self.LocationDetails.append(value)
    def insert_LocationDetails_at(self, index, value):
        self.LocationDetails.insert(index, value)
    def replace_LocationDetails_at(self, index, value):
        self.LocationDetails[index] = value
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
            self.LocationDetails
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ListLocationsReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ListLocationsReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ListLocationsReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ListLocationsReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ListLocationsReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ListLocationsReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ListLocationsReply', fromsubclass_=False, pretty_print=True):
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
        for LocationDetails_ in self.LocationDetails:
            namespaceprefix_ = self.LocationDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.LocationDetails_nsprefix_) else ''
            LocationDetails_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='LocationDetails', pretty_print=pretty_print)
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
        elif nodeName_ == 'LocationDetails':
            obj_ = LocationDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LocationDetails.append(obj_)
            obj_.original_tagname_ = 'LocationDetails'
# end class ListLocationsReply


class ListLocationsRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, UserDetail=None, TransactionDetail=None, Version=None, ApplicationId=None, Constraints=None, gds_collector_=None, **kwargs_):
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
        self.Constraints = Constraints
        self.Constraints_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ListLocationsRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ListLocationsRequest.subclass:
            return ListLocationsRequest.subclass(*args_, **kwargs_)
        else:
            return ListLocationsRequest(*args_, **kwargs_)
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
    def get_Constraints(self):
        return self.Constraints
    def set_Constraints(self, Constraints):
        self.Constraints = Constraints
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.UserDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.ApplicationId is not None or
            self.Constraints is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ListLocationsRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ListLocationsRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ListLocationsRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ListLocationsRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ListLocationsRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ListLocationsRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ListLocationsRequest', fromsubclass_=False, pretty_print=True):
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
        if self.Constraints is not None:
            namespaceprefix_ = self.Constraints_nsprefix_ + ':' if (UseCapturedNS_ and self.Constraints_nsprefix_) else ''
            self.Constraints.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Constraints', pretty_print=pretty_print)
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
        elif nodeName_ == 'Constraints':
            obj_ = ListLocationsConstraints.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Constraints = obj_
            obj_.original_tagname_ = 'Constraints'
# end class ListLocationsRequest


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


class LocationCapabilityDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CarrierCode=None, ServiceType=None, ServiceCategory=None, TransferOfPossessionType=None, DaysOfWeek=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CarrierCode = CarrierCode
        self.validate_CarrierCodeType(self.CarrierCode)
        self.CarrierCode_nsprefix_ = "ns"
        self.ServiceType = ServiceType
        self.ServiceType_nsprefix_ = None
        self.ServiceCategory = ServiceCategory
        self.validate_ServiceCategoryType(self.ServiceCategory)
        self.ServiceCategory_nsprefix_ = "ns"
        self.TransferOfPossessionType = TransferOfPossessionType
        self.validate_LocationTransferOfPossessionType(self.TransferOfPossessionType)
        self.TransferOfPossessionType_nsprefix_ = "ns"
        if DaysOfWeek is None:
            self.DaysOfWeek = []
        else:
            self.DaysOfWeek = DaysOfWeek
        self.DaysOfWeek_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LocationCapabilityDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LocationCapabilityDetail.subclass:
            return LocationCapabilityDetail.subclass(*args_, **kwargs_)
        else:
            return LocationCapabilityDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CarrierCode(self):
        return self.CarrierCode
    def set_CarrierCode(self, CarrierCode):
        self.CarrierCode = CarrierCode
    def get_ServiceType(self):
        return self.ServiceType
    def set_ServiceType(self, ServiceType):
        self.ServiceType = ServiceType
    def get_ServiceCategory(self):
        return self.ServiceCategory
    def set_ServiceCategory(self, ServiceCategory):
        self.ServiceCategory = ServiceCategory
    def get_TransferOfPossessionType(self):
        return self.TransferOfPossessionType
    def set_TransferOfPossessionType(self, TransferOfPossessionType):
        self.TransferOfPossessionType = TransferOfPossessionType
    def get_DaysOfWeek(self):
        return self.DaysOfWeek
    def set_DaysOfWeek(self, DaysOfWeek):
        self.DaysOfWeek = DaysOfWeek
    def add_DaysOfWeek(self, value):
        self.DaysOfWeek.append(value)
    def insert_DaysOfWeek_at(self, index, value):
        self.DaysOfWeek.insert(index, value)
    def replace_DaysOfWeek_at(self, index, value):
        self.DaysOfWeek[index] = value
    def validate_CarrierCodeType(self, value):
        result = True
        # Validate type CarrierCodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FDXC', 'FDXE', 'FDXG', 'FDXO', 'FXCC', 'FXFR', 'FXSP']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CarrierCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ServiceCategoryType(self, value):
        result = True
        # Validate type ServiceCategoryType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['EXPRESS_FREIGHT', 'EXPRESS_PARCEL', 'GROUND_HOME_DELIVERY']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ServiceCategoryType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_LocationTransferOfPossessionType(self, value):
        result = True
        # Validate type LocationTransferOfPossessionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['DROPOFF', 'HOLD_AT_LOCATION', 'REDIRECT_TO_HOLD_AT_LOCATION']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on LocationTransferOfPossessionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DayOfWeekType(self, value):
        result = True
        # Validate type DayOfWeekType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FRI', 'MON', 'SAT', 'SUN', 'THU', 'TUE', 'WED']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DayOfWeekType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.CarrierCode is not None or
            self.ServiceType is not None or
            self.ServiceCategory is not None or
            self.TransferOfPossessionType is not None or
            self.DaysOfWeek
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationCapabilityDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LocationCapabilityDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LocationCapabilityDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LocationCapabilityDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LocationCapabilityDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LocationCapabilityDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationCapabilityDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CarrierCode is not None:
            namespaceprefix_ = self.CarrierCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CarrierCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCarrierCode>%s</%sCarrierCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CarrierCode), input_name='CarrierCode')), namespaceprefix_ , eol_))
        if self.ServiceType is not None:
            namespaceprefix_ = self.ServiceType_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceType>%s</%sServiceType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServiceType), input_name='ServiceType')), namespaceprefix_ , eol_))
        if self.ServiceCategory is not None:
            namespaceprefix_ = self.ServiceCategory_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceCategory_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceCategory>%s</%sServiceCategory>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServiceCategory), input_name='ServiceCategory')), namespaceprefix_ , eol_))
        if self.TransferOfPossessionType is not None:
            namespaceprefix_ = self.TransferOfPossessionType_nsprefix_ + ':' if (UseCapturedNS_ and self.TransferOfPossessionType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTransferOfPossessionType>%s</%sTransferOfPossessionType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TransferOfPossessionType), input_name='TransferOfPossessionType')), namespaceprefix_ , eol_))
        for DaysOfWeek_ in self.DaysOfWeek:
            namespaceprefix_ = self.DaysOfWeek_nsprefix_ + ':' if (UseCapturedNS_ and self.DaysOfWeek_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDaysOfWeek>%s</%sDaysOfWeek>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(DaysOfWeek_), input_name='DaysOfWeek')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'CarrierCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CarrierCode')
            value_ = self.gds_validate_string(value_, node, 'CarrierCode')
            self.CarrierCode = value_
            self.CarrierCode_nsprefix_ = child_.prefix
            # validate type CarrierCodeType
            self.validate_CarrierCodeType(self.CarrierCode)
        elif nodeName_ == 'ServiceType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServiceType')
            value_ = self.gds_validate_string(value_, node, 'ServiceType')
            self.ServiceType = value_
            self.ServiceType_nsprefix_ = child_.prefix
        elif nodeName_ == 'ServiceCategory':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServiceCategory')
            value_ = self.gds_validate_string(value_, node, 'ServiceCategory')
            self.ServiceCategory = value_
            self.ServiceCategory_nsprefix_ = child_.prefix
            # validate type ServiceCategoryType
            self.validate_ServiceCategoryType(self.ServiceCategory)
        elif nodeName_ == 'TransferOfPossessionType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TransferOfPossessionType')
            value_ = self.gds_validate_string(value_, node, 'TransferOfPossessionType')
            self.TransferOfPossessionType = value_
            self.TransferOfPossessionType_nsprefix_ = child_.prefix
            # validate type LocationTransferOfPossessionType
            self.validate_LocationTransferOfPossessionType(self.TransferOfPossessionType)
        elif nodeName_ == 'DaysOfWeek':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DaysOfWeek')
            value_ = self.gds_validate_string(value_, node, 'DaysOfWeek')
            self.DaysOfWeek.append(value_)
            self.DaysOfWeek_nsprefix_ = child_.prefix
            # validate type DayOfWeekType
            self.validate_DayOfWeekType(self.DaysOfWeek[-1])
# end class LocationCapabilityDetail


class LocationContactAndAddress(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Contact=None, Address=None, AddressAncillaryDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Contact = Contact
        self.Contact_nsprefix_ = "ns"
        self.Address = Address
        self.Address_nsprefix_ = "ns"
        self.AddressAncillaryDetail = AddressAncillaryDetail
        self.AddressAncillaryDetail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LocationContactAndAddress)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LocationContactAndAddress.subclass:
            return LocationContactAndAddress.subclass(*args_, **kwargs_)
        else:
            return LocationContactAndAddress(*args_, **kwargs_)
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
    def get_AddressAncillaryDetail(self):
        return self.AddressAncillaryDetail
    def set_AddressAncillaryDetail(self, AddressAncillaryDetail):
        self.AddressAncillaryDetail = AddressAncillaryDetail
    def hasContent_(self):
        if (
            self.Contact is not None or
            self.Address is not None or
            self.AddressAncillaryDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationContactAndAddress', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LocationContactAndAddress')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LocationContactAndAddress':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LocationContactAndAddress')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LocationContactAndAddress', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LocationContactAndAddress'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationContactAndAddress', fromsubclass_=False, pretty_print=True):
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
        if self.AddressAncillaryDetail is not None:
            namespaceprefix_ = self.AddressAncillaryDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.AddressAncillaryDetail_nsprefix_) else ''
            self.AddressAncillaryDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AddressAncillaryDetail', pretty_print=pretty_print)
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
        elif nodeName_ == 'AddressAncillaryDetail':
            obj_ = AddressAncillaryDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AddressAncillaryDetail = obj_
            obj_.original_tagname_ = 'AddressAncillaryDetail'
# end class LocationContactAndAddress


class LocationDetail(GeneratedsSuper):
    """Describes an individual location providing a set of customer service
    features."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, LocationId=None, StoreNumber=None, LocationContactAndAddress=None, SpecialInstructions=None, TimeZoneOffset=None, LocationType=None, LocationTypeForDisplay=None, InternalFieldsDetail=None, Attributes=None, LocationCapabilities=None, PackageMaximumLimits=None, ClearanceLocationDetail=None, ServicingLocationDetails=None, AcceptedCurrency=None, LocationHolidays=None, MapUrl=None, EntityId=None, NormalHours=None, ExceptionalHours=None, HoursForEffectiveDate=None, CarrierDetails=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.LocationId = LocationId
        self.LocationId_nsprefix_ = None
        self.StoreNumber = StoreNumber
        self.StoreNumber_nsprefix_ = None
        self.LocationContactAndAddress = LocationContactAndAddress
        self.LocationContactAndAddress_nsprefix_ = "ns"
        self.SpecialInstructions = SpecialInstructions
        self.SpecialInstructions_nsprefix_ = None
        self.TimeZoneOffset = TimeZoneOffset
        self.TimeZoneOffset_nsprefix_ = None
        self.LocationType = LocationType
        self.validate_FedExLocationType(self.LocationType)
        self.LocationType_nsprefix_ = "ns"
        self.LocationTypeForDisplay = LocationTypeForDisplay
        self.LocationTypeForDisplay_nsprefix_ = None
        self.InternalFieldsDetail = InternalFieldsDetail
        self.InternalFieldsDetail_nsprefix_ = "ns"
        if Attributes is None:
            self.Attributes = []
        else:
            self.Attributes = Attributes
        self.Attributes_nsprefix_ = "ns"
        if LocationCapabilities is None:
            self.LocationCapabilities = []
        else:
            self.LocationCapabilities = LocationCapabilities
        self.LocationCapabilities_nsprefix_ = "ns"
        self.PackageMaximumLimits = PackageMaximumLimits
        self.PackageMaximumLimits_nsprefix_ = "ns"
        self.ClearanceLocationDetail = ClearanceLocationDetail
        self.ClearanceLocationDetail_nsprefix_ = "ns"
        if ServicingLocationDetails is None:
            self.ServicingLocationDetails = []
        else:
            self.ServicingLocationDetails = ServicingLocationDetails
        self.ServicingLocationDetails_nsprefix_ = "ns"
        self.AcceptedCurrency = AcceptedCurrency
        self.AcceptedCurrency_nsprefix_ = None
        if LocationHolidays is None:
            self.LocationHolidays = []
        else:
            self.LocationHolidays = LocationHolidays
        self.LocationHolidays_nsprefix_ = "ns"
        self.MapUrl = MapUrl
        self.MapUrl_nsprefix_ = None
        self.EntityId = EntityId
        self.EntityId_nsprefix_ = None
        if NormalHours is None:
            self.NormalHours = []
        else:
            self.NormalHours = NormalHours
        self.NormalHours_nsprefix_ = "ns"
        if ExceptionalHours is None:
            self.ExceptionalHours = []
        else:
            self.ExceptionalHours = ExceptionalHours
        self.ExceptionalHours_nsprefix_ = "ns"
        if HoursForEffectiveDate is None:
            self.HoursForEffectiveDate = []
        else:
            self.HoursForEffectiveDate = HoursForEffectiveDate
        self.HoursForEffectiveDate_nsprefix_ = "ns"
        if CarrierDetails is None:
            self.CarrierDetails = []
        else:
            self.CarrierDetails = CarrierDetails
        self.CarrierDetails_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LocationDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LocationDetail.subclass:
            return LocationDetail.subclass(*args_, **kwargs_)
        else:
            return LocationDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_LocationId(self):
        return self.LocationId
    def set_LocationId(self, LocationId):
        self.LocationId = LocationId
    def get_StoreNumber(self):
        return self.StoreNumber
    def set_StoreNumber(self, StoreNumber):
        self.StoreNumber = StoreNumber
    def get_LocationContactAndAddress(self):
        return self.LocationContactAndAddress
    def set_LocationContactAndAddress(self, LocationContactAndAddress):
        self.LocationContactAndAddress = LocationContactAndAddress
    def get_SpecialInstructions(self):
        return self.SpecialInstructions
    def set_SpecialInstructions(self, SpecialInstructions):
        self.SpecialInstructions = SpecialInstructions
    def get_TimeZoneOffset(self):
        return self.TimeZoneOffset
    def set_TimeZoneOffset(self, TimeZoneOffset):
        self.TimeZoneOffset = TimeZoneOffset
    def get_LocationType(self):
        return self.LocationType
    def set_LocationType(self, LocationType):
        self.LocationType = LocationType
    def get_LocationTypeForDisplay(self):
        return self.LocationTypeForDisplay
    def set_LocationTypeForDisplay(self, LocationTypeForDisplay):
        self.LocationTypeForDisplay = LocationTypeForDisplay
    def get_InternalFieldsDetail(self):
        return self.InternalFieldsDetail
    def set_InternalFieldsDetail(self, InternalFieldsDetail):
        self.InternalFieldsDetail = InternalFieldsDetail
    def get_Attributes(self):
        return self.Attributes
    def set_Attributes(self, Attributes):
        self.Attributes = Attributes
    def add_Attributes(self, value):
        self.Attributes.append(value)
    def insert_Attributes_at(self, index, value):
        self.Attributes.insert(index, value)
    def replace_Attributes_at(self, index, value):
        self.Attributes[index] = value
    def get_LocationCapabilities(self):
        return self.LocationCapabilities
    def set_LocationCapabilities(self, LocationCapabilities):
        self.LocationCapabilities = LocationCapabilities
    def add_LocationCapabilities(self, value):
        self.LocationCapabilities.append(value)
    def insert_LocationCapabilities_at(self, index, value):
        self.LocationCapabilities.insert(index, value)
    def replace_LocationCapabilities_at(self, index, value):
        self.LocationCapabilities[index] = value
    def get_PackageMaximumLimits(self):
        return self.PackageMaximumLimits
    def set_PackageMaximumLimits(self, PackageMaximumLimits):
        self.PackageMaximumLimits = PackageMaximumLimits
    def get_ClearanceLocationDetail(self):
        return self.ClearanceLocationDetail
    def set_ClearanceLocationDetail(self, ClearanceLocationDetail):
        self.ClearanceLocationDetail = ClearanceLocationDetail
    def get_ServicingLocationDetails(self):
        return self.ServicingLocationDetails
    def set_ServicingLocationDetails(self, ServicingLocationDetails):
        self.ServicingLocationDetails = ServicingLocationDetails
    def add_ServicingLocationDetails(self, value):
        self.ServicingLocationDetails.append(value)
    def insert_ServicingLocationDetails_at(self, index, value):
        self.ServicingLocationDetails.insert(index, value)
    def replace_ServicingLocationDetails_at(self, index, value):
        self.ServicingLocationDetails[index] = value
    def get_AcceptedCurrency(self):
        return self.AcceptedCurrency
    def set_AcceptedCurrency(self, AcceptedCurrency):
        self.AcceptedCurrency = AcceptedCurrency
    def get_LocationHolidays(self):
        return self.LocationHolidays
    def set_LocationHolidays(self, LocationHolidays):
        self.LocationHolidays = LocationHolidays
    def add_LocationHolidays(self, value):
        self.LocationHolidays.append(value)
    def insert_LocationHolidays_at(self, index, value):
        self.LocationHolidays.insert(index, value)
    def replace_LocationHolidays_at(self, index, value):
        self.LocationHolidays[index] = value
    def get_MapUrl(self):
        return self.MapUrl
    def set_MapUrl(self, MapUrl):
        self.MapUrl = MapUrl
    def get_EntityId(self):
        return self.EntityId
    def set_EntityId(self, EntityId):
        self.EntityId = EntityId
    def get_NormalHours(self):
        return self.NormalHours
    def set_NormalHours(self, NormalHours):
        self.NormalHours = NormalHours
    def add_NormalHours(self, value):
        self.NormalHours.append(value)
    def insert_NormalHours_at(self, index, value):
        self.NormalHours.insert(index, value)
    def replace_NormalHours_at(self, index, value):
        self.NormalHours[index] = value
    def get_ExceptionalHours(self):
        return self.ExceptionalHours
    def set_ExceptionalHours(self, ExceptionalHours):
        self.ExceptionalHours = ExceptionalHours
    def add_ExceptionalHours(self, value):
        self.ExceptionalHours.append(value)
    def insert_ExceptionalHours_at(self, index, value):
        self.ExceptionalHours.insert(index, value)
    def replace_ExceptionalHours_at(self, index, value):
        self.ExceptionalHours[index] = value
    def get_HoursForEffectiveDate(self):
        return self.HoursForEffectiveDate
    def set_HoursForEffectiveDate(self, HoursForEffectiveDate):
        self.HoursForEffectiveDate = HoursForEffectiveDate
    def add_HoursForEffectiveDate(self, value):
        self.HoursForEffectiveDate.append(value)
    def insert_HoursForEffectiveDate_at(self, index, value):
        self.HoursForEffectiveDate.insert(index, value)
    def replace_HoursForEffectiveDate_at(self, index, value):
        self.HoursForEffectiveDate[index] = value
    def get_CarrierDetails(self):
        return self.CarrierDetails
    def set_CarrierDetails(self, CarrierDetails):
        self.CarrierDetails = CarrierDetails
    def add_CarrierDetails(self, value):
        self.CarrierDetails.append(value)
    def insert_CarrierDetails_at(self, index, value):
        self.CarrierDetails.insert(index, value)
    def replace_CarrierDetails_at(self, index, value):
        self.CarrierDetails[index] = value
    def validate_FedExLocationType(self, value):
        result = True
        # Validate type FedExLocationType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FEDEX_AUTHORIZED_SHIP_CENTER', 'FEDEX_EXPRESS_STATION', 'FEDEX_FACILITY', 'FEDEX_FREIGHT_SERVICE_CENTER', 'FEDEX_GROUND_TERMINAL', 'FEDEX_HOME_DELIVERY_STATION', 'FEDEX_OFFICE', 'FEDEX_ONSITE', 'FEDEX_SELF_SERVICE_LOCATION', 'FEDEX_SHIPSITE', 'FEDEX_SHIP_AND_GET', 'FEDEX_SMART_POST_HUB']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on FedExLocationType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_LocationAttributesType(self, value):
        result = True
        # Validate type LocationAttributesType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ACCEPTS_CASH', 'ALREADY_OPEN', 'CLEARANCE_SERVICES', 'COPY_AND_PRINT_SERVICES', 'DANGEROUS_GOODS_SERVICES', 'DIRECT_MAIL_SERVICES', 'DOMESTIC_SHIPPING_SERVICES', 'DROP_BOX', 'INTERNATIONAL_SHIPPING_SERVICES', 'LOCATION_IS_IN_AIRPORT', 'NOTARY_SERVICES', 'OBSERVES_DAY_LIGHT_SAVING_TIMES', 'OPEN_TWENTY_FOUR_HOURS', 'PACKAGING_SUPPLIES', 'PACK_AND_SHIP', 'PASSPORT_PHOTO_SERVICES', 'RETURNS_SERVICES', 'SIGNS_AND_BANNERS_SERVICE', 'SONY_PICTURE_STATION']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on LocationAttributesType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.LocationId is not None or
            self.StoreNumber is not None or
            self.LocationContactAndAddress is not None or
            self.SpecialInstructions is not None or
            self.TimeZoneOffset is not None or
            self.LocationType is not None or
            self.LocationTypeForDisplay is not None or
            self.InternalFieldsDetail is not None or
            self.Attributes or
            self.LocationCapabilities or
            self.PackageMaximumLimits is not None or
            self.ClearanceLocationDetail is not None or
            self.ServicingLocationDetails or
            self.AcceptedCurrency is not None or
            self.LocationHolidays or
            self.MapUrl is not None or
            self.EntityId is not None or
            self.NormalHours or
            self.ExceptionalHours or
            self.HoursForEffectiveDate or
            self.CarrierDetails
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LocationDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LocationDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LocationDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LocationDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LocationDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.LocationId is not None:
            namespaceprefix_ = self.LocationId_nsprefix_ + ':' if (UseCapturedNS_ and self.LocationId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocationId>%s</%sLocationId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocationId), input_name='LocationId')), namespaceprefix_ , eol_))
        if self.StoreNumber is not None:
            namespaceprefix_ = self.StoreNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.StoreNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStoreNumber>%s</%sStoreNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.StoreNumber), input_name='StoreNumber')), namespaceprefix_ , eol_))
        if self.LocationContactAndAddress is not None:
            namespaceprefix_ = self.LocationContactAndAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.LocationContactAndAddress_nsprefix_) else ''
            self.LocationContactAndAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='LocationContactAndAddress', pretty_print=pretty_print)
        if self.SpecialInstructions is not None:
            namespaceprefix_ = self.SpecialInstructions_nsprefix_ + ':' if (UseCapturedNS_ and self.SpecialInstructions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSpecialInstructions>%s</%sSpecialInstructions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SpecialInstructions), input_name='SpecialInstructions')), namespaceprefix_ , eol_))
        if self.TimeZoneOffset is not None:
            namespaceprefix_ = self.TimeZoneOffset_nsprefix_ + ':' if (UseCapturedNS_ and self.TimeZoneOffset_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTimeZoneOffset>%s</%sTimeZoneOffset>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TimeZoneOffset), input_name='TimeZoneOffset')), namespaceprefix_ , eol_))
        if self.LocationType is not None:
            namespaceprefix_ = self.LocationType_nsprefix_ + ':' if (UseCapturedNS_ and self.LocationType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocationType>%s</%sLocationType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocationType), input_name='LocationType')), namespaceprefix_ , eol_))
        if self.LocationTypeForDisplay is not None:
            namespaceprefix_ = self.LocationTypeForDisplay_nsprefix_ + ':' if (UseCapturedNS_ and self.LocationTypeForDisplay_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocationTypeForDisplay>%s</%sLocationTypeForDisplay>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocationTypeForDisplay), input_name='LocationTypeForDisplay')), namespaceprefix_ , eol_))
        if self.InternalFieldsDetail is not None:
            namespaceprefix_ = self.InternalFieldsDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.InternalFieldsDetail_nsprefix_) else ''
            self.InternalFieldsDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='InternalFieldsDetail', pretty_print=pretty_print)
        for Attributes_ in self.Attributes:
            namespaceprefix_ = self.Attributes_nsprefix_ + ':' if (UseCapturedNS_ and self.Attributes_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAttributes>%s</%sAttributes>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Attributes_), input_name='Attributes')), namespaceprefix_ , eol_))
        for LocationCapabilities_ in self.LocationCapabilities:
            namespaceprefix_ = self.LocationCapabilities_nsprefix_ + ':' if (UseCapturedNS_ and self.LocationCapabilities_nsprefix_) else ''
            LocationCapabilities_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='LocationCapabilities', pretty_print=pretty_print)
        if self.PackageMaximumLimits is not None:
            namespaceprefix_ = self.PackageMaximumLimits_nsprefix_ + ':' if (UseCapturedNS_ and self.PackageMaximumLimits_nsprefix_) else ''
            self.PackageMaximumLimits.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PackageMaximumLimits', pretty_print=pretty_print)
        if self.ClearanceLocationDetail is not None:
            namespaceprefix_ = self.ClearanceLocationDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ClearanceLocationDetail_nsprefix_) else ''
            self.ClearanceLocationDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClearanceLocationDetail', pretty_print=pretty_print)
        for ServicingLocationDetails_ in self.ServicingLocationDetails:
            namespaceprefix_ = self.ServicingLocationDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.ServicingLocationDetails_nsprefix_) else ''
            ServicingLocationDetails_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ServicingLocationDetails', pretty_print=pretty_print)
        if self.AcceptedCurrency is not None:
            namespaceprefix_ = self.AcceptedCurrency_nsprefix_ + ':' if (UseCapturedNS_ and self.AcceptedCurrency_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAcceptedCurrency>%s</%sAcceptedCurrency>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AcceptedCurrency), input_name='AcceptedCurrency')), namespaceprefix_ , eol_))
        for LocationHolidays_ in self.LocationHolidays:
            namespaceprefix_ = self.LocationHolidays_nsprefix_ + ':' if (UseCapturedNS_ and self.LocationHolidays_nsprefix_) else ''
            LocationHolidays_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='LocationHolidays', pretty_print=pretty_print)
        if self.MapUrl is not None:
            namespaceprefix_ = self.MapUrl_nsprefix_ + ':' if (UseCapturedNS_ and self.MapUrl_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMapUrl>%s</%sMapUrl>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MapUrl), input_name='MapUrl')), namespaceprefix_ , eol_))
        if self.EntityId is not None:
            namespaceprefix_ = self.EntityId_nsprefix_ + ':' if (UseCapturedNS_ and self.EntityId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEntityId>%s</%sEntityId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EntityId), input_name='EntityId')), namespaceprefix_ , eol_))
        for NormalHours_ in self.NormalHours:
            namespaceprefix_ = self.NormalHours_nsprefix_ + ':' if (UseCapturedNS_ and self.NormalHours_nsprefix_) else ''
            NormalHours_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='NormalHours', pretty_print=pretty_print)
        for ExceptionalHours_ in self.ExceptionalHours:
            namespaceprefix_ = self.ExceptionalHours_nsprefix_ + ':' if (UseCapturedNS_ and self.ExceptionalHours_nsprefix_) else ''
            ExceptionalHours_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ExceptionalHours', pretty_print=pretty_print)
        for HoursForEffectiveDate_ in self.HoursForEffectiveDate:
            namespaceprefix_ = self.HoursForEffectiveDate_nsprefix_ + ':' if (UseCapturedNS_ and self.HoursForEffectiveDate_nsprefix_) else ''
            HoursForEffectiveDate_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='HoursForEffectiveDate', pretty_print=pretty_print)
        for CarrierDetails_ in self.CarrierDetails:
            namespaceprefix_ = self.CarrierDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.CarrierDetails_nsprefix_) else ''
            CarrierDetails_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CarrierDetails', pretty_print=pretty_print)
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
        if nodeName_ == 'LocationId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocationId')
            value_ = self.gds_validate_string(value_, node, 'LocationId')
            self.LocationId = value_
            self.LocationId_nsprefix_ = child_.prefix
        elif nodeName_ == 'StoreNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'StoreNumber')
            value_ = self.gds_validate_string(value_, node, 'StoreNumber')
            self.StoreNumber = value_
            self.StoreNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocationContactAndAddress':
            obj_ = LocationContactAndAddress.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LocationContactAndAddress = obj_
            obj_.original_tagname_ = 'LocationContactAndAddress'
        elif nodeName_ == 'SpecialInstructions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SpecialInstructions')
            value_ = self.gds_validate_string(value_, node, 'SpecialInstructions')
            self.SpecialInstructions = value_
            self.SpecialInstructions_nsprefix_ = child_.prefix
        elif nodeName_ == 'TimeZoneOffset':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TimeZoneOffset')
            value_ = self.gds_validate_string(value_, node, 'TimeZoneOffset')
            self.TimeZoneOffset = value_
            self.TimeZoneOffset_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocationType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocationType')
            value_ = self.gds_validate_string(value_, node, 'LocationType')
            self.LocationType = value_
            self.LocationType_nsprefix_ = child_.prefix
            # validate type FedExLocationType
            self.validate_FedExLocationType(self.LocationType)
        elif nodeName_ == 'LocationTypeForDisplay':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocationTypeForDisplay')
            value_ = self.gds_validate_string(value_, node, 'LocationTypeForDisplay')
            self.LocationTypeForDisplay = value_
            self.LocationTypeForDisplay_nsprefix_ = child_.prefix
        elif nodeName_ == 'InternalFieldsDetail':
            obj_ = LocationFieldsForInternalFedexUseDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.InternalFieldsDetail = obj_
            obj_.original_tagname_ = 'InternalFieldsDetail'
        elif nodeName_ == 'Attributes':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Attributes')
            value_ = self.gds_validate_string(value_, node, 'Attributes')
            self.Attributes.append(value_)
            self.Attributes_nsprefix_ = child_.prefix
            # validate type LocationAttributesType
            self.validate_LocationAttributesType(self.Attributes[-1])
        elif nodeName_ == 'LocationCapabilities':
            obj_ = LocationCapabilityDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LocationCapabilities.append(obj_)
            obj_.original_tagname_ = 'LocationCapabilities'
        elif nodeName_ == 'PackageMaximumLimits':
            obj_ = LocationPackageLimitsDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PackageMaximumLimits = obj_
            obj_.original_tagname_ = 'PackageMaximumLimits'
        elif nodeName_ == 'ClearanceLocationDetail':
            obj_ = ClearanceLocationDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClearanceLocationDetail = obj_
            obj_.original_tagname_ = 'ClearanceLocationDetail'
        elif nodeName_ == 'ServicingLocationDetails':
            obj_ = LocationIdentificationDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ServicingLocationDetails.append(obj_)
            obj_.original_tagname_ = 'ServicingLocationDetails'
        elif nodeName_ == 'AcceptedCurrency':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AcceptedCurrency')
            value_ = self.gds_validate_string(value_, node, 'AcceptedCurrency')
            self.AcceptedCurrency = value_
            self.AcceptedCurrency_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocationHolidays':
            obj_ = Holiday.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LocationHolidays.append(obj_)
            obj_.original_tagname_ = 'LocationHolidays'
        elif nodeName_ == 'MapUrl':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MapUrl')
            value_ = self.gds_validate_string(value_, node, 'MapUrl')
            self.MapUrl = value_
            self.MapUrl_nsprefix_ = child_.prefix
        elif nodeName_ == 'EntityId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EntityId')
            value_ = self.gds_validate_string(value_, node, 'EntityId')
            self.EntityId = value_
            self.EntityId_nsprefix_ = child_.prefix
        elif nodeName_ == 'NormalHours':
            obj_ = LocationHours.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.NormalHours.append(obj_)
            obj_.original_tagname_ = 'NormalHours'
        elif nodeName_ == 'ExceptionalHours':
            obj_ = LocationHours.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ExceptionalHours.append(obj_)
            obj_.original_tagname_ = 'ExceptionalHours'
        elif nodeName_ == 'HoursForEffectiveDate':
            obj_ = LocationHours.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.HoursForEffectiveDate.append(obj_)
            obj_.original_tagname_ = 'HoursForEffectiveDate'
        elif nodeName_ == 'CarrierDetails':
            obj_ = CarrierDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CarrierDetails.append(obj_)
            obj_.original_tagname_ = 'CarrierDetails'
# end class LocationDetail


class LocationFieldsForInternalFedexUseDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, NonRevenueAccountNumber=None, CityCenterAccountNumber=None, CustomsLocationId=None, CostCenterCode=None, Attributes=None, OperationalContact=None, LocalAirportId=None, RegionalAirportId=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.NonRevenueAccountNumber = NonRevenueAccountNumber
        self.NonRevenueAccountNumber_nsprefix_ = None
        self.CityCenterAccountNumber = CityCenterAccountNumber
        self.CityCenterAccountNumber_nsprefix_ = None
        self.CustomsLocationId = CustomsLocationId
        self.CustomsLocationId_nsprefix_ = None
        self.CostCenterCode = CostCenterCode
        self.CostCenterCode_nsprefix_ = None
        if Attributes is None:
            self.Attributes = []
        else:
            self.Attributes = Attributes
        self.Attributes_nsprefix_ = "ns"
        self.OperationalContact = OperationalContact
        self.OperationalContact_nsprefix_ = "ns"
        self.LocalAirportId = LocalAirportId
        self.LocalAirportId_nsprefix_ = None
        self.RegionalAirportId = RegionalAirportId
        self.RegionalAirportId_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LocationFieldsForInternalFedexUseDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LocationFieldsForInternalFedexUseDetail.subclass:
            return LocationFieldsForInternalFedexUseDetail.subclass(*args_, **kwargs_)
        else:
            return LocationFieldsForInternalFedexUseDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_NonRevenueAccountNumber(self):
        return self.NonRevenueAccountNumber
    def set_NonRevenueAccountNumber(self, NonRevenueAccountNumber):
        self.NonRevenueAccountNumber = NonRevenueAccountNumber
    def get_CityCenterAccountNumber(self):
        return self.CityCenterAccountNumber
    def set_CityCenterAccountNumber(self, CityCenterAccountNumber):
        self.CityCenterAccountNumber = CityCenterAccountNumber
    def get_CustomsLocationId(self):
        return self.CustomsLocationId
    def set_CustomsLocationId(self, CustomsLocationId):
        self.CustomsLocationId = CustomsLocationId
    def get_CostCenterCode(self):
        return self.CostCenterCode
    def set_CostCenterCode(self, CostCenterCode):
        self.CostCenterCode = CostCenterCode
    def get_Attributes(self):
        return self.Attributes
    def set_Attributes(self, Attributes):
        self.Attributes = Attributes
    def add_Attributes(self, value):
        self.Attributes.append(value)
    def insert_Attributes_at(self, index, value):
        self.Attributes.insert(index, value)
    def replace_Attributes_at(self, index, value):
        self.Attributes[index] = value
    def get_OperationalContact(self):
        return self.OperationalContact
    def set_OperationalContact(self, OperationalContact):
        self.OperationalContact = OperationalContact
    def get_LocalAirportId(self):
        return self.LocalAirportId
    def set_LocalAirportId(self, LocalAirportId):
        self.LocalAirportId = LocalAirportId
    def get_RegionalAirportId(self):
        return self.RegionalAirportId
    def set_RegionalAirportId(self, RegionalAirportId):
        self.RegionalAirportId = RegionalAirportId
    def validate_LocationAttributesForInternalFedexUseType(self, value):
        result = True
        # Validate type LocationAttributesForInternalFedexUseType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FAMIS_LOCATION']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on LocationAttributesForInternalFedexUseType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.NonRevenueAccountNumber is not None or
            self.CityCenterAccountNumber is not None or
            self.CustomsLocationId is not None or
            self.CostCenterCode is not None or
            self.Attributes or
            self.OperationalContact is not None or
            self.LocalAirportId is not None or
            self.RegionalAirportId is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationFieldsForInternalFedexUseDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LocationFieldsForInternalFedexUseDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LocationFieldsForInternalFedexUseDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LocationFieldsForInternalFedexUseDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LocationFieldsForInternalFedexUseDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LocationFieldsForInternalFedexUseDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationFieldsForInternalFedexUseDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.NonRevenueAccountNumber is not None:
            namespaceprefix_ = self.NonRevenueAccountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.NonRevenueAccountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNonRevenueAccountNumber>%s</%sNonRevenueAccountNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NonRevenueAccountNumber), input_name='NonRevenueAccountNumber')), namespaceprefix_ , eol_))
        if self.CityCenterAccountNumber is not None:
            namespaceprefix_ = self.CityCenterAccountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.CityCenterAccountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCityCenterAccountNumber>%s</%sCityCenterAccountNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CityCenterAccountNumber), input_name='CityCenterAccountNumber')), namespaceprefix_ , eol_))
        if self.CustomsLocationId is not None:
            namespaceprefix_ = self.CustomsLocationId_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomsLocationId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustomsLocationId>%s</%sCustomsLocationId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CustomsLocationId), input_name='CustomsLocationId')), namespaceprefix_ , eol_))
        if self.CostCenterCode is not None:
            namespaceprefix_ = self.CostCenterCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CostCenterCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCostCenterCode>%s</%sCostCenterCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CostCenterCode), input_name='CostCenterCode')), namespaceprefix_ , eol_))
        for Attributes_ in self.Attributes:
            namespaceprefix_ = self.Attributes_nsprefix_ + ':' if (UseCapturedNS_ and self.Attributes_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAttributes>%s</%sAttributes>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Attributes_), input_name='Attributes')), namespaceprefix_ , eol_))
        if self.OperationalContact is not None:
            namespaceprefix_ = self.OperationalContact_nsprefix_ + ':' if (UseCapturedNS_ and self.OperationalContact_nsprefix_) else ''
            self.OperationalContact.export(outfile, level, namespaceprefix_, namespacedef_='', name_='OperationalContact', pretty_print=pretty_print)
        if self.LocalAirportId is not None:
            namespaceprefix_ = self.LocalAirportId_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalAirportId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalAirportId>%s</%sLocalAirportId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalAirportId), input_name='LocalAirportId')), namespaceprefix_ , eol_))
        if self.RegionalAirportId is not None:
            namespaceprefix_ = self.RegionalAirportId_nsprefix_ + ':' if (UseCapturedNS_ and self.RegionalAirportId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRegionalAirportId>%s</%sRegionalAirportId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.RegionalAirportId), input_name='RegionalAirportId')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'NonRevenueAccountNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NonRevenueAccountNumber')
            value_ = self.gds_validate_string(value_, node, 'NonRevenueAccountNumber')
            self.NonRevenueAccountNumber = value_
            self.NonRevenueAccountNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'CityCenterAccountNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CityCenterAccountNumber')
            value_ = self.gds_validate_string(value_, node, 'CityCenterAccountNumber')
            self.CityCenterAccountNumber = value_
            self.CityCenterAccountNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'CustomsLocationId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CustomsLocationId')
            value_ = self.gds_validate_string(value_, node, 'CustomsLocationId')
            self.CustomsLocationId = value_
            self.CustomsLocationId_nsprefix_ = child_.prefix
        elif nodeName_ == 'CostCenterCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CostCenterCode')
            value_ = self.gds_validate_string(value_, node, 'CostCenterCode')
            self.CostCenterCode = value_
            self.CostCenterCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'Attributes':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Attributes')
            value_ = self.gds_validate_string(value_, node, 'Attributes')
            self.Attributes.append(value_)
            self.Attributes_nsprefix_ = child_.prefix
            # validate type LocationAttributesForInternalFedexUseType
            self.validate_LocationAttributesForInternalFedexUseType(self.Attributes[-1])
        elif nodeName_ == 'OperationalContact':
            obj_ = Contact.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.OperationalContact = obj_
            obj_.original_tagname_ = 'OperationalContact'
        elif nodeName_ == 'LocalAirportId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalAirportId')
            value_ = self.gds_validate_string(value_, node, 'LocalAirportId')
            self.LocalAirportId = value_
            self.LocalAirportId_nsprefix_ = child_.prefix
        elif nodeName_ == 'RegionalAirportId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RegionalAirportId')
            value_ = self.gds_validate_string(value_, node, 'RegionalAirportId')
            self.RegionalAirportId = value_
            self.RegionalAirportId_nsprefix_ = child_.prefix
# end class LocationFieldsForInternalFedexUseDetail


class LocationHours(GeneratedsSuper):
    """Specifies the location hours for a location."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DayofWeek=None, OperationalHours=None, Hours=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DayofWeek = DayofWeek
        self.validate_DayOfWeekType(self.DayofWeek)
        self.DayofWeek_nsprefix_ = "ns"
        self.OperationalHours = OperationalHours
        self.validate_OperationalHoursType(self.OperationalHours)
        self.OperationalHours_nsprefix_ = "ns"
        if Hours is None:
            self.Hours = []
        else:
            self.Hours = Hours
        self.Hours_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LocationHours)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LocationHours.subclass:
            return LocationHours.subclass(*args_, **kwargs_)
        else:
            return LocationHours(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DayofWeek(self):
        return self.DayofWeek
    def set_DayofWeek(self, DayofWeek):
        self.DayofWeek = DayofWeek
    def get_OperationalHours(self):
        return self.OperationalHours
    def set_OperationalHours(self, OperationalHours):
        self.OperationalHours = OperationalHours
    def get_Hours(self):
        return self.Hours
    def set_Hours(self, Hours):
        self.Hours = Hours
    def add_Hours(self, value):
        self.Hours.append(value)
    def insert_Hours_at(self, index, value):
        self.Hours.insert(index, value)
    def replace_Hours_at(self, index, value):
        self.Hours[index] = value
    def validate_DayOfWeekType(self, value):
        result = True
        # Validate type DayOfWeekType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FRI', 'MON', 'SAT', 'SUN', 'THU', 'TUE', 'WED']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DayOfWeekType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_OperationalHoursType(self, value):
        result = True
        # Validate type OperationalHoursType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['CLOSED_ALL_DAY', 'OPEN_ALL_DAY', 'OPEN_BY_HOURS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on OperationalHoursType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.DayofWeek is not None or
            self.OperationalHours is not None or
            self.Hours
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationHours', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LocationHours')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LocationHours':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LocationHours')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LocationHours', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LocationHours'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationHours', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DayofWeek is not None:
            namespaceprefix_ = self.DayofWeek_nsprefix_ + ':' if (UseCapturedNS_ and self.DayofWeek_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDayofWeek>%s</%sDayofWeek>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DayofWeek), input_name='DayofWeek')), namespaceprefix_ , eol_))
        if self.OperationalHours is not None:
            namespaceprefix_ = self.OperationalHours_nsprefix_ + ':' if (UseCapturedNS_ and self.OperationalHours_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOperationalHours>%s</%sOperationalHours>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OperationalHours), input_name='OperationalHours')), namespaceprefix_ , eol_))
        for Hours_ in self.Hours:
            namespaceprefix_ = self.Hours_nsprefix_ + ':' if (UseCapturedNS_ and self.Hours_nsprefix_) else ''
            Hours_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Hours', pretty_print=pretty_print)
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
        if nodeName_ == 'DayofWeek':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DayofWeek')
            value_ = self.gds_validate_string(value_, node, 'DayofWeek')
            self.DayofWeek = value_
            self.DayofWeek_nsprefix_ = child_.prefix
            # validate type DayOfWeekType
            self.validate_DayOfWeekType(self.DayofWeek)
        elif nodeName_ == 'OperationalHours':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OperationalHours')
            value_ = self.gds_validate_string(value_, node, 'OperationalHours')
            self.OperationalHours = value_
            self.OperationalHours_nsprefix_ = child_.prefix
            # validate type OperationalHoursType
            self.validate_OperationalHoursType(self.OperationalHours)
        elif nodeName_ == 'Hours':
            obj_ = TimeRange.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Hours.append(obj_)
            obj_.original_tagname_ = 'Hours'
# end class LocationHours


class LocationIdentificationDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Type=None, Id=None, Number=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Type = Type
        self.validate_FedExLocationType(self.Type)
        self.Type_nsprefix_ = "ns"
        self.Id = Id
        self.Id_nsprefix_ = None
        self.Number = Number
        self.Number_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LocationIdentificationDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LocationIdentificationDetail.subclass:
            return LocationIdentificationDetail.subclass(*args_, **kwargs_)
        else:
            return LocationIdentificationDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def get_Number(self):
        return self.Number
    def set_Number(self, Number):
        self.Number = Number
    def validate_FedExLocationType(self, value):
        result = True
        # Validate type FedExLocationType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FEDEX_AUTHORIZED_SHIP_CENTER', 'FEDEX_EXPRESS_STATION', 'FEDEX_FACILITY', 'FEDEX_FREIGHT_SERVICE_CENTER', 'FEDEX_GROUND_TERMINAL', 'FEDEX_HOME_DELIVERY_STATION', 'FEDEX_OFFICE', 'FEDEX_ONSITE', 'FEDEX_SELF_SERVICE_LOCATION', 'FEDEX_SHIPSITE', 'FEDEX_SHIP_AND_GET', 'FEDEX_SMART_POST_HUB']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on FedExLocationType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Type is not None or
            self.Id is not None or
            self.Number is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationIdentificationDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LocationIdentificationDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LocationIdentificationDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LocationIdentificationDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LocationIdentificationDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LocationIdentificationDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationIdentificationDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sType>%s</%sType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Type), input_name='Type')), namespaceprefix_ , eol_))
        if self.Id is not None:
            namespaceprefix_ = self.Id_nsprefix_ + ':' if (UseCapturedNS_ and self.Id_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sId>%s</%sId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Id), input_name='Id')), namespaceprefix_ , eol_))
        if self.Number is not None:
            namespaceprefix_ = self.Number_nsprefix_ + ':' if (UseCapturedNS_ and self.Number_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumber>%s</%sNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.Number, input_name='Number'), namespaceprefix_ , eol_))
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
            # validate type FedExLocationType
            self.validate_FedExLocationType(self.Type)
        elif nodeName_ == 'Id':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Id')
            value_ = self.gds_validate_string(value_, node, 'Id')
            self.Id = value_
            self.Id_nsprefix_ = child_.prefix
        elif nodeName_ == 'Number' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Number')
            ival_ = self.gds_validate_integer(ival_, node, 'Number')
            self.Number = ival_
            self.Number_nsprefix_ = child_.prefix
# end class LocationIdentificationDetail


class LocationPackageLimitsDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Weight=None, Dimensions=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Weight = Weight
        self.Weight_nsprefix_ = "ns"
        self.Dimensions = Dimensions
        self.Dimensions_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LocationPackageLimitsDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LocationPackageLimitsDetail.subclass:
            return LocationPackageLimitsDetail.subclass(*args_, **kwargs_)
        else:
            return LocationPackageLimitsDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Weight(self):
        return self.Weight
    def set_Weight(self, Weight):
        self.Weight = Weight
    def get_Dimensions(self):
        return self.Dimensions
    def set_Dimensions(self, Dimensions):
        self.Dimensions = Dimensions
    def hasContent_(self):
        if (
            self.Weight is not None or
            self.Dimensions is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationPackageLimitsDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LocationPackageLimitsDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LocationPackageLimitsDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LocationPackageLimitsDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LocationPackageLimitsDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LocationPackageLimitsDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationPackageLimitsDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Weight is not None:
            namespaceprefix_ = self.Weight_nsprefix_ + ':' if (UseCapturedNS_ and self.Weight_nsprefix_) else ''
            self.Weight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Weight', pretty_print=pretty_print)
        if self.Dimensions is not None:
            namespaceprefix_ = self.Dimensions_nsprefix_ + ':' if (UseCapturedNS_ and self.Dimensions_nsprefix_) else ''
            self.Dimensions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Dimensions', pretty_print=pretty_print)
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
        if nodeName_ == 'Weight':
            obj_ = Weight.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Weight = obj_
            obj_.original_tagname_ = 'Weight'
        elif nodeName_ == 'Dimensions':
            obj_ = Dimensions.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Dimensions = obj_
            obj_.original_tagname_ = 'Dimensions'
# end class LocationPackageLimitsDetail


class LocationSortDetail(GeneratedsSuper):
    """Specifies the criterion and order to be used to sort the location
    details."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Criterion=None, Order=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Criterion = Criterion
        self.validate_LocationSortCriteriaType(self.Criterion)
        self.Criterion_nsprefix_ = "ns"
        self.Order = Order
        self.validate_LocationSortOrderType(self.Order)
        self.Order_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LocationSortDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LocationSortDetail.subclass:
            return LocationSortDetail.subclass(*args_, **kwargs_)
        else:
            return LocationSortDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Criterion(self):
        return self.Criterion
    def set_Criterion(self, Criterion):
        self.Criterion = Criterion
    def get_Order(self):
        return self.Order
    def set_Order(self, Order):
        self.Order = Order
    def validate_LocationSortCriteriaType(self, value):
        result = True
        # Validate type LocationSortCriteriaType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['DISTANCE', 'LATEST_EXPRESS_DROPOFF_TIME', 'LATEST_GROUND_DROPOFF_TIME', 'LOCATION_TYPE']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on LocationSortCriteriaType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_LocationSortOrderType(self, value):
        result = True
        # Validate type LocationSortOrderType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['HIGHEST_TO_LOWEST', 'LOWEST_TO_HIGHEST']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on LocationSortOrderType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Criterion is not None or
            self.Order is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationSortDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LocationSortDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LocationSortDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LocationSortDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LocationSortDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LocationSortDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationSortDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Criterion is not None:
            namespaceprefix_ = self.Criterion_nsprefix_ + ':' if (UseCapturedNS_ and self.Criterion_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCriterion>%s</%sCriterion>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Criterion), input_name='Criterion')), namespaceprefix_ , eol_))
        if self.Order is not None:
            namespaceprefix_ = self.Order_nsprefix_ + ':' if (UseCapturedNS_ and self.Order_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOrder>%s</%sOrder>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Order), input_name='Order')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Criterion':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Criterion')
            value_ = self.gds_validate_string(value_, node, 'Criterion')
            self.Criterion = value_
            self.Criterion_nsprefix_ = child_.prefix
            # validate type LocationSortCriteriaType
            self.validate_LocationSortCriteriaType(self.Criterion)
        elif nodeName_ == 'Order':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Order')
            value_ = self.gds_validate_string(value_, node, 'Order')
            self.Order = value_
            self.Order_nsprefix_ = child_.prefix
            # validate type LocationSortOrderType
            self.validate_LocationSortOrderType(self.Order)
# end class LocationSortDetail


class LocationSupportedPackageDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Weight=None, Dimensions=None, ServiceOptions=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Weight = Weight
        self.Weight_nsprefix_ = "ns"
        self.Dimensions = Dimensions
        self.Dimensions_nsprefix_ = "ns"
        if ServiceOptions is None:
            self.ServiceOptions = []
        else:
            self.ServiceOptions = ServiceOptions
        self.ServiceOptions_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LocationSupportedPackageDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LocationSupportedPackageDetail.subclass:
            return LocationSupportedPackageDetail.subclass(*args_, **kwargs_)
        else:
            return LocationSupportedPackageDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Weight(self):
        return self.Weight
    def set_Weight(self, Weight):
        self.Weight = Weight
    def get_Dimensions(self):
        return self.Dimensions
    def set_Dimensions(self, Dimensions):
        self.Dimensions = Dimensions
    def get_ServiceOptions(self):
        return self.ServiceOptions
    def set_ServiceOptions(self, ServiceOptions):
        self.ServiceOptions = ServiceOptions
    def add_ServiceOptions(self, value):
        self.ServiceOptions.append(value)
    def insert_ServiceOptions_at(self, index, value):
        self.ServiceOptions.insert(index, value)
    def replace_ServiceOptions_at(self, index, value):
        self.ServiceOptions[index] = value
    def hasContent_(self):
        if (
            self.Weight is not None or
            self.Dimensions is not None or
            self.ServiceOptions
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationSupportedPackageDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LocationSupportedPackageDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LocationSupportedPackageDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LocationSupportedPackageDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LocationSupportedPackageDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LocationSupportedPackageDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationSupportedPackageDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Weight is not None:
            namespaceprefix_ = self.Weight_nsprefix_ + ':' if (UseCapturedNS_ and self.Weight_nsprefix_) else ''
            self.Weight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Weight', pretty_print=pretty_print)
        if self.Dimensions is not None:
            namespaceprefix_ = self.Dimensions_nsprefix_ + ':' if (UseCapturedNS_ and self.Dimensions_nsprefix_) else ''
            self.Dimensions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Dimensions', pretty_print=pretty_print)
        for ServiceOptions_ in self.ServiceOptions:
            namespaceprefix_ = self.ServiceOptions_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceOptions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceOptions>%s</%sServiceOptions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(ServiceOptions_), input_name='ServiceOptions')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Weight':
            obj_ = Weight.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Weight = obj_
            obj_.original_tagname_ = 'Weight'
        elif nodeName_ == 'Dimensions':
            obj_ = Dimensions.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Dimensions = obj_
            obj_.original_tagname_ = 'Dimensions'
        elif nodeName_ == 'ServiceOptions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServiceOptions')
            value_ = self.gds_validate_string(value_, node, 'ServiceOptions')
            self.ServiceOptions.append(value_)
            self.ServiceOptions_nsprefix_ = child_.prefix
# end class LocationSupportedPackageDetail


class LocationSupportedShipmentDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PackageDetails=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if PackageDetails is None:
            self.PackageDetails = []
        else:
            self.PackageDetails = PackageDetails
        self.PackageDetails_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LocationSupportedShipmentDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LocationSupportedShipmentDetail.subclass:
            return LocationSupportedShipmentDetail.subclass(*args_, **kwargs_)
        else:
            return LocationSupportedShipmentDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PackageDetails(self):
        return self.PackageDetails
    def set_PackageDetails(self, PackageDetails):
        self.PackageDetails = PackageDetails
    def add_PackageDetails(self, value):
        self.PackageDetails.append(value)
    def insert_PackageDetails_at(self, index, value):
        self.PackageDetails.insert(index, value)
    def replace_PackageDetails_at(self, index, value):
        self.PackageDetails[index] = value
    def hasContent_(self):
        if (
            self.PackageDetails
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationSupportedShipmentDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LocationSupportedShipmentDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LocationSupportedShipmentDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LocationSupportedShipmentDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LocationSupportedShipmentDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LocationSupportedShipmentDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LocationSupportedShipmentDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for PackageDetails_ in self.PackageDetails:
            namespaceprefix_ = self.PackageDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.PackageDetails_nsprefix_) else ''
            PackageDetails_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PackageDetails', pretty_print=pretty_print)
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
        if nodeName_ == 'PackageDetails':
            obj_ = LocationSupportedPackageDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PackageDetails.append(obj_)
            obj_.original_tagname_ = 'PackageDetails'
# end class LocationSupportedShipmentDetail


class LookupLocationReply(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, LocationDetail=None, gds_collector_=None, **kwargs_):
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
        self.LocationDetail = LocationDetail
        self.LocationDetail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LookupLocationReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LookupLocationReply.subclass:
            return LookupLocationReply.subclass(*args_, **kwargs_)
        else:
            return LookupLocationReply(*args_, **kwargs_)
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
    def get_LocationDetail(self):
        return self.LocationDetail
    def set_LocationDetail(self, LocationDetail):
        self.LocationDetail = LocationDetail
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
            self.LocationDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LookupLocationReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LookupLocationReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LookupLocationReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LookupLocationReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LookupLocationReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LookupLocationReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LookupLocationReply', fromsubclass_=False, pretty_print=True):
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
        if self.LocationDetail is not None:
            namespaceprefix_ = self.LocationDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.LocationDetail_nsprefix_) else ''
            self.LocationDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='LocationDetail', pretty_print=pretty_print)
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
        elif nodeName_ == 'LocationDetail':
            obj_ = LocationDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LocationDetail = obj_
            obj_.original_tagname_ = 'LocationDetail'
# end class LookupLocationReply


class LookupLocationRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, UserDetail=None, TransactionDetail=None, Version=None, ApplicationId=None, ServiceLevel=None, EffectiveDate=None, LocationId=None, LocationContentOptions=None, gds_collector_=None, **kwargs_):
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
        self.ServiceLevel = ServiceLevel
        self.validate_AvailableLocationsRequestServiceLevel(self.ServiceLevel)
        self.ServiceLevel_nsprefix_ = "ns"
        if isinstance(EffectiveDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(EffectiveDate, '%Y-%m-%d').date()
        else:
            initvalue_ = EffectiveDate
        self.EffectiveDate = initvalue_
        self.EffectiveDate_nsprefix_ = None
        self.LocationId = LocationId
        self.LocationId_nsprefix_ = None
        if LocationContentOptions is None:
            self.LocationContentOptions = []
        else:
            self.LocationContentOptions = LocationContentOptions
        self.LocationContentOptions_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LookupLocationRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LookupLocationRequest.subclass:
            return LookupLocationRequest.subclass(*args_, **kwargs_)
        else:
            return LookupLocationRequest(*args_, **kwargs_)
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
    def get_ServiceLevel(self):
        return self.ServiceLevel
    def set_ServiceLevel(self, ServiceLevel):
        self.ServiceLevel = ServiceLevel
    def get_EffectiveDate(self):
        return self.EffectiveDate
    def set_EffectiveDate(self, EffectiveDate):
        self.EffectiveDate = EffectiveDate
    def get_LocationId(self):
        return self.LocationId
    def set_LocationId(self, LocationId):
        self.LocationId = LocationId
    def get_LocationContentOptions(self):
        return self.LocationContentOptions
    def set_LocationContentOptions(self, LocationContentOptions):
        self.LocationContentOptions = LocationContentOptions
    def add_LocationContentOptions(self, value):
        self.LocationContentOptions.append(value)
    def insert_LocationContentOptions_at(self, index, value):
        self.LocationContentOptions.insert(index, value)
    def replace_LocationContentOptions_at(self, index, value):
        self.LocationContentOptions[index] = value
    def validate_AvailableLocationsRequestServiceLevel(self, value):
        result = True
        # Validate type AvailableLocationsRequestServiceLevel, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['CUSTOMER_APPROPRIATE_DATA', 'INCLUDE_ACCOUNT_DATA', 'NO_ACCOUNT_DATA']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on AvailableLocationsRequestServiceLevel' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_LocationContentOptionType(self, value):
        result = True
        # Validate type LocationContentOptionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['HOLIDAYS', 'LOCATION_DROPOFF_TIMES', 'MAP_URL', 'TIMEZONE_OFFSET']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on LocationContentOptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
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
            self.ServiceLevel is not None or
            self.EffectiveDate is not None or
            self.LocationId is not None or
            self.LocationContentOptions
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LookupLocationRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LookupLocationRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LookupLocationRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LookupLocationRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LookupLocationRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LookupLocationRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LookupLocationRequest', fromsubclass_=False, pretty_print=True):
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
        if self.ServiceLevel is not None:
            namespaceprefix_ = self.ServiceLevel_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceLevel_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceLevel>%s</%sServiceLevel>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServiceLevel), input_name='ServiceLevel')), namespaceprefix_ , eol_))
        if self.EffectiveDate is not None:
            namespaceprefix_ = self.EffectiveDate_nsprefix_ + ':' if (UseCapturedNS_ and self.EffectiveDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEffectiveDate>%s</%sEffectiveDate>%s' % (namespaceprefix_ , self.gds_format_date(self.EffectiveDate, input_name='EffectiveDate'), namespaceprefix_ , eol_))
        if self.LocationId is not None:
            namespaceprefix_ = self.LocationId_nsprefix_ + ':' if (UseCapturedNS_ and self.LocationId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocationId>%s</%sLocationId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocationId), input_name='LocationId')), namespaceprefix_ , eol_))
        for LocationContentOptions_ in self.LocationContentOptions:
            namespaceprefix_ = self.LocationContentOptions_nsprefix_ + ':' if (UseCapturedNS_ and self.LocationContentOptions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocationContentOptions>%s</%sLocationContentOptions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(LocationContentOptions_), input_name='LocationContentOptions')), namespaceprefix_ , eol_))
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
        elif nodeName_ == 'ServiceLevel':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServiceLevel')
            value_ = self.gds_validate_string(value_, node, 'ServiceLevel')
            self.ServiceLevel = value_
            self.ServiceLevel_nsprefix_ = child_.prefix
            # validate type AvailableLocationsRequestServiceLevel
            self.validate_AvailableLocationsRequestServiceLevel(self.ServiceLevel)
        elif nodeName_ == 'EffectiveDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.EffectiveDate = dval_
            self.EffectiveDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocationId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocationId')
            value_ = self.gds_validate_string(value_, node, 'LocationId')
            self.LocationId = value_
            self.LocationId_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocationContentOptions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocationContentOptions')
            value_ = self.gds_validate_string(value_, node, 'LocationContentOptions')
            self.LocationContentOptions.append(value_)
            self.LocationContentOptions_nsprefix_ = child_.prefix
            # validate type LocationContentOptionType
            self.validate_LocationContentOptionType(self.LocationContentOptions[-1])
# end class LookupLocationRequest


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
        self.validate_ServiceIdType(self.Source)
        self.Source_nsprefix_ = "ns"
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
    def validate_ServiceIdType(self, value):
        result = True
        # Validate type ServiceIdType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['locs']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ServiceIdType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
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
            # validate type ServiceIdType
            self.validate_ServiceIdType(self.Source)
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


class PolicyGridManifest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GridId=None, Contents=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GridId = GridId
        self.GridId_nsprefix_ = None
        if Contents is None:
            self.Contents = []
        else:
            self.Contents = Contents
        self.Contents_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PolicyGridManifest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PolicyGridManifest.subclass:
            return PolicyGridManifest.subclass(*args_, **kwargs_)
        else:
            return PolicyGridManifest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GridId(self):
        return self.GridId
    def set_GridId(self, GridId):
        self.GridId = GridId
    def get_Contents(self):
        return self.Contents
    def set_Contents(self, Contents):
        self.Contents = Contents
    def add_Contents(self, value):
        self.Contents.append(value)
    def insert_Contents_at(self, index, value):
        self.Contents.insert(index, value)
    def replace_Contents_at(self, index, value):
        self.Contents[index] = value
    def hasContent_(self):
        if (
            self.GridId is not None or
            self.Contents
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PolicyGridManifest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PolicyGridManifest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PolicyGridManifest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PolicyGridManifest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PolicyGridManifest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PolicyGridManifest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PolicyGridManifest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GridId is not None:
            namespaceprefix_ = self.GridId_nsprefix_ + ':' if (UseCapturedNS_ and self.GridId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGridId>%s</%sGridId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GridId), input_name='GridId')), namespaceprefix_ , eol_))
        for Contents_ in self.Contents:
            namespaceprefix_ = self.Contents_nsprefix_ + ':' if (UseCapturedNS_ and self.Contents_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sContents>%s</%sContents>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Contents_), input_name='Contents')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'GridId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GridId')
            value_ = self.gds_validate_string(value_, node, 'GridId')
            self.GridId = value_
            self.GridId_nsprefix_ = child_.prefix
        elif nodeName_ == 'Contents':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Contents')
            value_ = self.gds_validate_string(value_, node, 'Contents')
            self.Contents.append(value_)
            self.Contents_nsprefix_ = child_.prefix
# end class PolicyGridManifest


class ReservationAvailabilityDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Attributes=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Attributes is None:
            self.Attributes = []
        else:
            self.Attributes = Attributes
        self.Attributes_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ReservationAvailabilityDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ReservationAvailabilityDetail.subclass:
            return ReservationAvailabilityDetail.subclass(*args_, **kwargs_)
        else:
            return ReservationAvailabilityDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Attributes(self):
        return self.Attributes
    def set_Attributes(self, Attributes):
        self.Attributes = Attributes
    def add_Attributes(self, value):
        self.Attributes.append(value)
    def insert_Attributes_at(self, index, value):
        self.Attributes.insert(index, value)
    def replace_Attributes_at(self, index, value):
        self.Attributes[index] = value
    def validate_ReservationAttributesType(self, value):
        result = True
        # Validate type ReservationAttributesType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['RESERVATION_AVAILABLE']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ReservationAttributesType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Attributes
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReservationAvailabilityDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ReservationAvailabilityDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ReservationAvailabilityDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ReservationAvailabilityDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ReservationAvailabilityDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ReservationAvailabilityDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReservationAvailabilityDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Attributes_ in self.Attributes:
            namespaceprefix_ = self.Attributes_nsprefix_ + ':' if (UseCapturedNS_ and self.Attributes_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAttributes>%s</%sAttributes>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Attributes_), input_name='Attributes')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Attributes':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Attributes')
            value_ = self.gds_validate_string(value_, node, 'Attributes')
            self.Attributes.append(value_)
            self.Attributes_nsprefix_ = child_.prefix
            # validate type ReservationAttributesType
            self.validate_ReservationAttributesType(self.Attributes[-1])
# end class ReservationAvailabilityDetail


class RestrictionsAndPrivilegesPolicyDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ExceptionType=None, PolicyGridManifests=None, PrivilegeDetails=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ExceptionType = ExceptionType
        self.validate_RestrictionsAndPrivilegesPolicyExceptionType(self.ExceptionType)
        self.ExceptionType_nsprefix_ = "ns"
        if PolicyGridManifests is None:
            self.PolicyGridManifests = []
        else:
            self.PolicyGridManifests = PolicyGridManifests
        self.PolicyGridManifests_nsprefix_ = "ns"
        if PrivilegeDetails is None:
            self.PrivilegeDetails = []
        else:
            self.PrivilegeDetails = PrivilegeDetails
        self.PrivilegeDetails_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RestrictionsAndPrivilegesPolicyDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RestrictionsAndPrivilegesPolicyDetail.subclass:
            return RestrictionsAndPrivilegesPolicyDetail.subclass(*args_, **kwargs_)
        else:
            return RestrictionsAndPrivilegesPolicyDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ExceptionType(self):
        return self.ExceptionType
    def set_ExceptionType(self, ExceptionType):
        self.ExceptionType = ExceptionType
    def get_PolicyGridManifests(self):
        return self.PolicyGridManifests
    def set_PolicyGridManifests(self, PolicyGridManifests):
        self.PolicyGridManifests = PolicyGridManifests
    def add_PolicyGridManifests(self, value):
        self.PolicyGridManifests.append(value)
    def insert_PolicyGridManifests_at(self, index, value):
        self.PolicyGridManifests.insert(index, value)
    def replace_PolicyGridManifests_at(self, index, value):
        self.PolicyGridManifests[index] = value
    def get_PrivilegeDetails(self):
        return self.PrivilegeDetails
    def set_PrivilegeDetails(self, PrivilegeDetails):
        self.PrivilegeDetails = PrivilegeDetails
    def add_PrivilegeDetails(self, value):
        self.PrivilegeDetails.append(value)
    def insert_PrivilegeDetails_at(self, index, value):
        self.PrivilegeDetails.insert(index, value)
    def replace_PrivilegeDetails_at(self, index, value):
        self.PrivilegeDetails[index] = value
    def validate_RestrictionsAndPrivilegesPolicyExceptionType(self, value):
        result = True
        # Validate type RestrictionsAndPrivilegesPolicyExceptionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['POLICIES_NOT_FOUND', 'SERVICE_UNAVAILABLE']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on RestrictionsAndPrivilegesPolicyExceptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.ExceptionType is not None or
            self.PolicyGridManifests or
            self.PrivilegeDetails
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RestrictionsAndPrivilegesPolicyDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RestrictionsAndPrivilegesPolicyDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RestrictionsAndPrivilegesPolicyDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RestrictionsAndPrivilegesPolicyDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RestrictionsAndPrivilegesPolicyDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RestrictionsAndPrivilegesPolicyDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RestrictionsAndPrivilegesPolicyDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ExceptionType is not None:
            namespaceprefix_ = self.ExceptionType_nsprefix_ + ':' if (UseCapturedNS_ and self.ExceptionType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExceptionType>%s</%sExceptionType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ExceptionType), input_name='ExceptionType')), namespaceprefix_ , eol_))
        for PolicyGridManifests_ in self.PolicyGridManifests:
            namespaceprefix_ = self.PolicyGridManifests_nsprefix_ + ':' if (UseCapturedNS_ and self.PolicyGridManifests_nsprefix_) else ''
            PolicyGridManifests_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PolicyGridManifests', pretty_print=pretty_print)
        for PrivilegeDetails_ in self.PrivilegeDetails:
            namespaceprefix_ = self.PrivilegeDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.PrivilegeDetails_nsprefix_) else ''
            PrivilegeDetails_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PrivilegeDetails', pretty_print=pretty_print)
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
        if nodeName_ == 'ExceptionType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ExceptionType')
            value_ = self.gds_validate_string(value_, node, 'ExceptionType')
            self.ExceptionType = value_
            self.ExceptionType_nsprefix_ = child_.prefix
            # validate type RestrictionsAndPrivilegesPolicyExceptionType
            self.validate_RestrictionsAndPrivilegesPolicyExceptionType(self.ExceptionType)
        elif nodeName_ == 'PolicyGridManifests':
            obj_ = PolicyGridManifest.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PolicyGridManifests.append(obj_)
            obj_.original_tagname_ = 'PolicyGridManifests'
        elif nodeName_ == 'PrivilegeDetails':
            obj_ = EnterprisePrivilegeDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PrivilegeDetails.append(obj_)
            obj_.original_tagname_ = 'PrivilegeDetails'
# end class RestrictionsAndPrivilegesPolicyDetail


class SearchLocationConstraints(GeneratedsSuper):
    """Specifies additional constraints on the attributes of the locations
    being searched."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, RadiusDistance=None, DropOffTimeNeeded=None, ResultsFilters=None, SupportedRedirectToHoldServices=None, RequiredLocationAttributes=None, RequiredLocationCapabilities=None, ShipmentDetail=None, ResultsToSkip=None, ResultsRequested=None, LocationContentOptions=None, LocationTypesToInclude=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.RadiusDistance = RadiusDistance
        self.RadiusDistance_nsprefix_ = "ns"
        if isinstance(DropOffTimeNeeded, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DropOffTimeNeeded, '%H:%M:%S').time()
        else:
            initvalue_ = DropOffTimeNeeded
        self.DropOffTimeNeeded = initvalue_
        self.DropOffTimeNeeded_nsprefix_ = None
        if ResultsFilters is None:
            self.ResultsFilters = []
        else:
            self.ResultsFilters = ResultsFilters
        self.ResultsFilters_nsprefix_ = "ns"
        if SupportedRedirectToHoldServices is None:
            self.SupportedRedirectToHoldServices = []
        else:
            self.SupportedRedirectToHoldServices = SupportedRedirectToHoldServices
        self.SupportedRedirectToHoldServices_nsprefix_ = "ns"
        if RequiredLocationAttributes is None:
            self.RequiredLocationAttributes = []
        else:
            self.RequiredLocationAttributes = RequiredLocationAttributes
        self.RequiredLocationAttributes_nsprefix_ = "ns"
        if RequiredLocationCapabilities is None:
            self.RequiredLocationCapabilities = []
        else:
            self.RequiredLocationCapabilities = RequiredLocationCapabilities
        self.RequiredLocationCapabilities_nsprefix_ = "ns"
        self.ShipmentDetail = ShipmentDetail
        self.ShipmentDetail_nsprefix_ = "ns"
        self.ResultsToSkip = ResultsToSkip
        self.ResultsToSkip_nsprefix_ = None
        self.ResultsRequested = ResultsRequested
        self.ResultsRequested_nsprefix_ = None
        if LocationContentOptions is None:
            self.LocationContentOptions = []
        else:
            self.LocationContentOptions = LocationContentOptions
        self.LocationContentOptions_nsprefix_ = "ns"
        if LocationTypesToInclude is None:
            self.LocationTypesToInclude = []
        else:
            self.LocationTypesToInclude = LocationTypesToInclude
        self.LocationTypesToInclude_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SearchLocationConstraints)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SearchLocationConstraints.subclass:
            return SearchLocationConstraints.subclass(*args_, **kwargs_)
        else:
            return SearchLocationConstraints(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_RadiusDistance(self):
        return self.RadiusDistance
    def set_RadiusDistance(self, RadiusDistance):
        self.RadiusDistance = RadiusDistance
    def get_DropOffTimeNeeded(self):
        return self.DropOffTimeNeeded
    def set_DropOffTimeNeeded(self, DropOffTimeNeeded):
        self.DropOffTimeNeeded = DropOffTimeNeeded
    def get_ResultsFilters(self):
        return self.ResultsFilters
    def set_ResultsFilters(self, ResultsFilters):
        self.ResultsFilters = ResultsFilters
    def add_ResultsFilters(self, value):
        self.ResultsFilters.append(value)
    def insert_ResultsFilters_at(self, index, value):
        self.ResultsFilters.insert(index, value)
    def replace_ResultsFilters_at(self, index, value):
        self.ResultsFilters[index] = value
    def get_SupportedRedirectToHoldServices(self):
        return self.SupportedRedirectToHoldServices
    def set_SupportedRedirectToHoldServices(self, SupportedRedirectToHoldServices):
        self.SupportedRedirectToHoldServices = SupportedRedirectToHoldServices
    def add_SupportedRedirectToHoldServices(self, value):
        self.SupportedRedirectToHoldServices.append(value)
    def insert_SupportedRedirectToHoldServices_at(self, index, value):
        self.SupportedRedirectToHoldServices.insert(index, value)
    def replace_SupportedRedirectToHoldServices_at(self, index, value):
        self.SupportedRedirectToHoldServices[index] = value
    def get_RequiredLocationAttributes(self):
        return self.RequiredLocationAttributes
    def set_RequiredLocationAttributes(self, RequiredLocationAttributes):
        self.RequiredLocationAttributes = RequiredLocationAttributes
    def add_RequiredLocationAttributes(self, value):
        self.RequiredLocationAttributes.append(value)
    def insert_RequiredLocationAttributes_at(self, index, value):
        self.RequiredLocationAttributes.insert(index, value)
    def replace_RequiredLocationAttributes_at(self, index, value):
        self.RequiredLocationAttributes[index] = value
    def get_RequiredLocationCapabilities(self):
        return self.RequiredLocationCapabilities
    def set_RequiredLocationCapabilities(self, RequiredLocationCapabilities):
        self.RequiredLocationCapabilities = RequiredLocationCapabilities
    def add_RequiredLocationCapabilities(self, value):
        self.RequiredLocationCapabilities.append(value)
    def insert_RequiredLocationCapabilities_at(self, index, value):
        self.RequiredLocationCapabilities.insert(index, value)
    def replace_RequiredLocationCapabilities_at(self, index, value):
        self.RequiredLocationCapabilities[index] = value
    def get_ShipmentDetail(self):
        return self.ShipmentDetail
    def set_ShipmentDetail(self, ShipmentDetail):
        self.ShipmentDetail = ShipmentDetail
    def get_ResultsToSkip(self):
        return self.ResultsToSkip
    def set_ResultsToSkip(self, ResultsToSkip):
        self.ResultsToSkip = ResultsToSkip
    def get_ResultsRequested(self):
        return self.ResultsRequested
    def set_ResultsRequested(self, ResultsRequested):
        self.ResultsRequested = ResultsRequested
    def get_LocationContentOptions(self):
        return self.LocationContentOptions
    def set_LocationContentOptions(self, LocationContentOptions):
        self.LocationContentOptions = LocationContentOptions
    def add_LocationContentOptions(self, value):
        self.LocationContentOptions.append(value)
    def insert_LocationContentOptions_at(self, index, value):
        self.LocationContentOptions.insert(index, value)
    def replace_LocationContentOptions_at(self, index, value):
        self.LocationContentOptions[index] = value
    def get_LocationTypesToInclude(self):
        return self.LocationTypesToInclude
    def set_LocationTypesToInclude(self, LocationTypesToInclude):
        self.LocationTypesToInclude = LocationTypesToInclude
    def add_LocationTypesToInclude(self, value):
        self.LocationTypesToInclude.append(value)
    def insert_LocationTypesToInclude_at(self, index, value):
        self.LocationTypesToInclude.insert(index, value)
    def replace_LocationTypesToInclude_at(self, index, value):
        self.LocationTypesToInclude[index] = value
    def validate_LocationSearchFilterType(self, value):
        result = True
        # Validate type LocationSearchFilterType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['EXCLUDE_LOCATIONS_OUTSIDE_COUNTRY', 'EXCLUDE_LOCATIONS_OUTSIDE_STATE_OR_PROVINCE', 'EXCLUDE_UNAVAILABLE_LOCATIONS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on LocationSearchFilterType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_SupportedRedirectToHoldServiceType(self, value):
        result = True
        # Validate type SupportedRedirectToHoldServiceType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FEDEX_EXPRESS', 'FEDEX_GROUND', 'FEDEX_GROUND_HOME_DELIVERY']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on SupportedRedirectToHoldServiceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_LocationAttributesType(self, value):
        result = True
        # Validate type LocationAttributesType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ACCEPTS_CASH', 'ALREADY_OPEN', 'CLEARANCE_SERVICES', 'COPY_AND_PRINT_SERVICES', 'DANGEROUS_GOODS_SERVICES', 'DIRECT_MAIL_SERVICES', 'DOMESTIC_SHIPPING_SERVICES', 'DROP_BOX', 'INTERNATIONAL_SHIPPING_SERVICES', 'LOCATION_IS_IN_AIRPORT', 'NOTARY_SERVICES', 'OBSERVES_DAY_LIGHT_SAVING_TIMES', 'OPEN_TWENTY_FOUR_HOURS', 'PACKAGING_SUPPLIES', 'PACK_AND_SHIP', 'PASSPORT_PHOTO_SERVICES', 'RETURNS_SERVICES', 'SIGNS_AND_BANNERS_SERVICE', 'SONY_PICTURE_STATION']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on LocationAttributesType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_LocationContentOptionType(self, value):
        result = True
        # Validate type LocationContentOptionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['HOLIDAYS', 'LOCATION_DROPOFF_TIMES', 'MAP_URL', 'TIMEZONE_OFFSET']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on LocationContentOptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_FedExLocationType(self, value):
        result = True
        # Validate type FedExLocationType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FEDEX_AUTHORIZED_SHIP_CENTER', 'FEDEX_EXPRESS_STATION', 'FEDEX_FACILITY', 'FEDEX_FREIGHT_SERVICE_CENTER', 'FEDEX_GROUND_TERMINAL', 'FEDEX_HOME_DELIVERY_STATION', 'FEDEX_OFFICE', 'FEDEX_ONSITE', 'FEDEX_SELF_SERVICE_LOCATION', 'FEDEX_SHIPSITE', 'FEDEX_SHIP_AND_GET', 'FEDEX_SMART_POST_HUB']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on FedExLocationType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.RadiusDistance is not None or
            self.DropOffTimeNeeded is not None or
            self.ResultsFilters or
            self.SupportedRedirectToHoldServices or
            self.RequiredLocationAttributes or
            self.RequiredLocationCapabilities or
            self.ShipmentDetail is not None or
            self.ResultsToSkip is not None or
            self.ResultsRequested is not None or
            self.LocationContentOptions or
            self.LocationTypesToInclude
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SearchLocationConstraints', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SearchLocationConstraints')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SearchLocationConstraints':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SearchLocationConstraints')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SearchLocationConstraints', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SearchLocationConstraints'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SearchLocationConstraints', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.RadiusDistance is not None:
            namespaceprefix_ = self.RadiusDistance_nsprefix_ + ':' if (UseCapturedNS_ and self.RadiusDistance_nsprefix_) else ''
            self.RadiusDistance.export(outfile, level, namespaceprefix_, namespacedef_='', name_='RadiusDistance', pretty_print=pretty_print)
        if self.DropOffTimeNeeded is not None:
            namespaceprefix_ = self.DropOffTimeNeeded_nsprefix_ + ':' if (UseCapturedNS_ and self.DropOffTimeNeeded_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDropOffTimeNeeded>%s</%sDropOffTimeNeeded>%s' % (namespaceprefix_ , self.gds_format_time(self.DropOffTimeNeeded, input_name='DropOffTimeNeeded'), namespaceprefix_ , eol_))
        for ResultsFilters_ in self.ResultsFilters:
            namespaceprefix_ = self.ResultsFilters_nsprefix_ + ':' if (UseCapturedNS_ and self.ResultsFilters_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sResultsFilters>%s</%sResultsFilters>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(ResultsFilters_), input_name='ResultsFilters')), namespaceprefix_ , eol_))
        for SupportedRedirectToHoldServices_ in self.SupportedRedirectToHoldServices:
            namespaceprefix_ = self.SupportedRedirectToHoldServices_nsprefix_ + ':' if (UseCapturedNS_ and self.SupportedRedirectToHoldServices_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSupportedRedirectToHoldServices>%s</%sSupportedRedirectToHoldServices>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(SupportedRedirectToHoldServices_), input_name='SupportedRedirectToHoldServices')), namespaceprefix_ , eol_))
        for RequiredLocationAttributes_ in self.RequiredLocationAttributes:
            namespaceprefix_ = self.RequiredLocationAttributes_nsprefix_ + ':' if (UseCapturedNS_ and self.RequiredLocationAttributes_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRequiredLocationAttributes>%s</%sRequiredLocationAttributes>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(RequiredLocationAttributes_), input_name='RequiredLocationAttributes')), namespaceprefix_ , eol_))
        for RequiredLocationCapabilities_ in self.RequiredLocationCapabilities:
            namespaceprefix_ = self.RequiredLocationCapabilities_nsprefix_ + ':' if (UseCapturedNS_ and self.RequiredLocationCapabilities_nsprefix_) else ''
            RequiredLocationCapabilities_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='RequiredLocationCapabilities', pretty_print=pretty_print)
        if self.ShipmentDetail is not None:
            namespaceprefix_ = self.ShipmentDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentDetail_nsprefix_) else ''
            self.ShipmentDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentDetail', pretty_print=pretty_print)
        if self.ResultsToSkip is not None:
            namespaceprefix_ = self.ResultsToSkip_nsprefix_ + ':' if (UseCapturedNS_ and self.ResultsToSkip_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sResultsToSkip>%s</%sResultsToSkip>%s' % (namespaceprefix_ , self.gds_format_integer(self.ResultsToSkip, input_name='ResultsToSkip'), namespaceprefix_ , eol_))
        if self.ResultsRequested is not None:
            namespaceprefix_ = self.ResultsRequested_nsprefix_ + ':' if (UseCapturedNS_ and self.ResultsRequested_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sResultsRequested>%s</%sResultsRequested>%s' % (namespaceprefix_ , self.gds_format_integer(self.ResultsRequested, input_name='ResultsRequested'), namespaceprefix_ , eol_))
        for LocationContentOptions_ in self.LocationContentOptions:
            namespaceprefix_ = self.LocationContentOptions_nsprefix_ + ':' if (UseCapturedNS_ and self.LocationContentOptions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocationContentOptions>%s</%sLocationContentOptions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(LocationContentOptions_), input_name='LocationContentOptions')), namespaceprefix_ , eol_))
        for LocationTypesToInclude_ in self.LocationTypesToInclude:
            namespaceprefix_ = self.LocationTypesToInclude_nsprefix_ + ':' if (UseCapturedNS_ and self.LocationTypesToInclude_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocationTypesToInclude>%s</%sLocationTypesToInclude>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(LocationTypesToInclude_), input_name='LocationTypesToInclude')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'RadiusDistance':
            obj_ = Distance.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.RadiusDistance = obj_
            obj_.original_tagname_ = 'RadiusDistance'
        elif nodeName_ == 'DropOffTimeNeeded':
            sval_ = child_.text
            dval_ = self.gds_parse_time(sval_)
            self.DropOffTimeNeeded = dval_
            self.DropOffTimeNeeded_nsprefix_ = child_.prefix
        elif nodeName_ == 'ResultsFilters':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ResultsFilters')
            value_ = self.gds_validate_string(value_, node, 'ResultsFilters')
            self.ResultsFilters.append(value_)
            self.ResultsFilters_nsprefix_ = child_.prefix
            # validate type LocationSearchFilterType
            self.validate_LocationSearchFilterType(self.ResultsFilters[-1])
        elif nodeName_ == 'SupportedRedirectToHoldServices':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SupportedRedirectToHoldServices')
            value_ = self.gds_validate_string(value_, node, 'SupportedRedirectToHoldServices')
            self.SupportedRedirectToHoldServices.append(value_)
            self.SupportedRedirectToHoldServices_nsprefix_ = child_.prefix
            # validate type SupportedRedirectToHoldServiceType
            self.validate_SupportedRedirectToHoldServiceType(self.SupportedRedirectToHoldServices[-1])
        elif nodeName_ == 'RequiredLocationAttributes':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RequiredLocationAttributes')
            value_ = self.gds_validate_string(value_, node, 'RequiredLocationAttributes')
            self.RequiredLocationAttributes.append(value_)
            self.RequiredLocationAttributes_nsprefix_ = child_.prefix
            # validate type LocationAttributesType
            self.validate_LocationAttributesType(self.RequiredLocationAttributes[-1])
        elif nodeName_ == 'RequiredLocationCapabilities':
            obj_ = LocationCapabilityDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.RequiredLocationCapabilities.append(obj_)
            obj_.original_tagname_ = 'RequiredLocationCapabilities'
        elif nodeName_ == 'ShipmentDetail':
            obj_ = LocationSupportedShipmentDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentDetail = obj_
            obj_.original_tagname_ = 'ShipmentDetail'
        elif nodeName_ == 'ResultsToSkip' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'ResultsToSkip')
            if ival_ < 0:
                raise_parse_error(child_, 'requires nonNegativeInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'ResultsToSkip')
            self.ResultsToSkip = ival_
            self.ResultsToSkip_nsprefix_ = child_.prefix
        elif nodeName_ == 'ResultsRequested' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'ResultsRequested')
            if ival_ < 0:
                raise_parse_error(child_, 'requires nonNegativeInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'ResultsRequested')
            self.ResultsRequested = ival_
            self.ResultsRequested_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocationContentOptions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocationContentOptions')
            value_ = self.gds_validate_string(value_, node, 'LocationContentOptions')
            self.LocationContentOptions.append(value_)
            self.LocationContentOptions_nsprefix_ = child_.prefix
            # validate type LocationContentOptionType
            self.validate_LocationContentOptionType(self.LocationContentOptions[-1])
        elif nodeName_ == 'LocationTypesToInclude':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocationTypesToInclude')
            value_ = self.gds_validate_string(value_, node, 'LocationTypesToInclude')
            self.LocationTypesToInclude.append(value_)
            self.LocationTypesToInclude_nsprefix_ = child_.prefix
            # validate type FedExLocationType
            self.validate_FedExLocationType(self.LocationTypesToInclude[-1])
# end class SearchLocationConstraints


class SearchLocationsProcessingOptionsRequested(GeneratedsSuper):
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
                CurrentSubclassModule_, SearchLocationsProcessingOptionsRequested)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SearchLocationsProcessingOptionsRequested.subclass:
            return SearchLocationsProcessingOptionsRequested.subclass(*args_, **kwargs_)
        else:
            return SearchLocationsProcessingOptionsRequested(*args_, **kwargs_)
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
    def validate_SearchLocationsProcessingOptionType(self, value):
        result = True
        # Validate type SearchLocationsProcessingOptionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ALLOW_RESTRICTIONS_WITH_EXCEPTIONS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on SearchLocationsProcessingOptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Options
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SearchLocationsProcessingOptionsRequested', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SearchLocationsProcessingOptionsRequested')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SearchLocationsProcessingOptionsRequested':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SearchLocationsProcessingOptionsRequested')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SearchLocationsProcessingOptionsRequested', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SearchLocationsProcessingOptionsRequested'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SearchLocationsProcessingOptionsRequested', fromsubclass_=False, pretty_print=True):
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
            # validate type SearchLocationsProcessingOptionType
            self.validate_SearchLocationsProcessingOptionType(self.Options[-1])
# end class SearchLocationsProcessingOptionsRequested


class SearchLocationsReply(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, TotalResultsAvailable=None, ResultsReturned=None, FormattedAddress=None, AddressToLocationRelationships=None, gds_collector_=None, **kwargs_):
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
        self.TotalResultsAvailable = TotalResultsAvailable
        self.TotalResultsAvailable_nsprefix_ = None
        self.ResultsReturned = ResultsReturned
        self.ResultsReturned_nsprefix_ = None
        self.FormattedAddress = FormattedAddress
        self.FormattedAddress_nsprefix_ = "ns"
        if AddressToLocationRelationships is None:
            self.AddressToLocationRelationships = []
        else:
            self.AddressToLocationRelationships = AddressToLocationRelationships
        self.AddressToLocationRelationships_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SearchLocationsReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SearchLocationsReply.subclass:
            return SearchLocationsReply.subclass(*args_, **kwargs_)
        else:
            return SearchLocationsReply(*args_, **kwargs_)
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
    def get_TotalResultsAvailable(self):
        return self.TotalResultsAvailable
    def set_TotalResultsAvailable(self, TotalResultsAvailable):
        self.TotalResultsAvailable = TotalResultsAvailable
    def get_ResultsReturned(self):
        return self.ResultsReturned
    def set_ResultsReturned(self, ResultsReturned):
        self.ResultsReturned = ResultsReturned
    def get_FormattedAddress(self):
        return self.FormattedAddress
    def set_FormattedAddress(self, FormattedAddress):
        self.FormattedAddress = FormattedAddress
    def get_AddressToLocationRelationships(self):
        return self.AddressToLocationRelationships
    def set_AddressToLocationRelationships(self, AddressToLocationRelationships):
        self.AddressToLocationRelationships = AddressToLocationRelationships
    def add_AddressToLocationRelationships(self, value):
        self.AddressToLocationRelationships.append(value)
    def insert_AddressToLocationRelationships_at(self, index, value):
        self.AddressToLocationRelationships.insert(index, value)
    def replace_AddressToLocationRelationships_at(self, index, value):
        self.AddressToLocationRelationships[index] = value
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
            self.TotalResultsAvailable is not None or
            self.ResultsReturned is not None or
            self.FormattedAddress is not None or
            self.AddressToLocationRelationships
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SearchLocationsReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SearchLocationsReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SearchLocationsReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SearchLocationsReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SearchLocationsReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SearchLocationsReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SearchLocationsReply', fromsubclass_=False, pretty_print=True):
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
        if self.TotalResultsAvailable is not None:
            namespaceprefix_ = self.TotalResultsAvailable_nsprefix_ + ':' if (UseCapturedNS_ and self.TotalResultsAvailable_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTotalResultsAvailable>%s</%sTotalResultsAvailable>%s' % (namespaceprefix_ , self.gds_format_integer(self.TotalResultsAvailable, input_name='TotalResultsAvailable'), namespaceprefix_ , eol_))
        if self.ResultsReturned is not None:
            namespaceprefix_ = self.ResultsReturned_nsprefix_ + ':' if (UseCapturedNS_ and self.ResultsReturned_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sResultsReturned>%s</%sResultsReturned>%s' % (namespaceprefix_ , self.gds_format_integer(self.ResultsReturned, input_name='ResultsReturned'), namespaceprefix_ , eol_))
        if self.FormattedAddress is not None:
            namespaceprefix_ = self.FormattedAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.FormattedAddress_nsprefix_) else ''
            self.FormattedAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='FormattedAddress', pretty_print=pretty_print)
        for AddressToLocationRelationships_ in self.AddressToLocationRelationships:
            namespaceprefix_ = self.AddressToLocationRelationships_nsprefix_ + ':' if (UseCapturedNS_ and self.AddressToLocationRelationships_nsprefix_) else ''
            AddressToLocationRelationships_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AddressToLocationRelationships', pretty_print=pretty_print)
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
        elif nodeName_ == 'TotalResultsAvailable' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'TotalResultsAvailable')
            if ival_ < 0:
                raise_parse_error(child_, 'requires nonNegativeInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'TotalResultsAvailable')
            self.TotalResultsAvailable = ival_
            self.TotalResultsAvailable_nsprefix_ = child_.prefix
        elif nodeName_ == 'ResultsReturned' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'ResultsReturned')
            if ival_ < 0:
                raise_parse_error(child_, 'requires nonNegativeInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'ResultsReturned')
            self.ResultsReturned = ival_
            self.ResultsReturned_nsprefix_ = child_.prefix
        elif nodeName_ == 'FormattedAddress':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.FormattedAddress = obj_
            obj_.original_tagname_ = 'FormattedAddress'
        elif nodeName_ == 'AddressToLocationRelationships':
            obj_ = AddressToLocationRelationshipDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AddressToLocationRelationships.append(obj_)
            obj_.original_tagname_ = 'AddressToLocationRelationships'
# end class SearchLocationsReply


class SearchLocationsRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, UserDetail=None, TransactionDetail=None, Version=None, ServiceLevel=None, ProcessingOptions=None, EffectiveDate=None, LocationsSearchCriterion=None, ShipperAccountNumber=None, RestrictionsAndPrivileges=None, UniqueTrackingNumber=None, Address=None, PhoneNumber=None, GeographicCoordinates=None, MultipleMatchesAction=None, SortDetail=None, Constraints=None, gds_collector_=None, **kwargs_):
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
        self.ServiceLevel = ServiceLevel
        self.validate_SearchLocationsServiceLevelType(self.ServiceLevel)
        self.ServiceLevel_nsprefix_ = "ns"
        self.ProcessingOptions = ProcessingOptions
        self.ProcessingOptions_nsprefix_ = "ns"
        if isinstance(EffectiveDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(EffectiveDate, '%Y-%m-%d').date()
        else:
            initvalue_ = EffectiveDate
        self.EffectiveDate = initvalue_
        self.EffectiveDate_nsprefix_ = None
        self.LocationsSearchCriterion = LocationsSearchCriterion
        self.validate_LocationsSearchCriteriaType(self.LocationsSearchCriterion)
        self.LocationsSearchCriterion_nsprefix_ = "ns"
        self.ShipperAccountNumber = ShipperAccountNumber
        self.ShipperAccountNumber_nsprefix_ = None
        self.RestrictionsAndPrivileges = RestrictionsAndPrivileges
        self.RestrictionsAndPrivileges_nsprefix_ = "ns"
        self.UniqueTrackingNumber = UniqueTrackingNumber
        self.UniqueTrackingNumber_nsprefix_ = "ns"
        self.Address = Address
        self.Address_nsprefix_ = "ns"
        self.PhoneNumber = PhoneNumber
        self.PhoneNumber_nsprefix_ = None
        self.GeographicCoordinates = GeographicCoordinates
        self.GeographicCoordinates_nsprefix_ = None
        self.MultipleMatchesAction = MultipleMatchesAction
        self.validate_MultipleMatchesActionType(self.MultipleMatchesAction)
        self.MultipleMatchesAction_nsprefix_ = "ns"
        self.SortDetail = SortDetail
        self.SortDetail_nsprefix_ = "ns"
        self.Constraints = Constraints
        self.Constraints_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SearchLocationsRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SearchLocationsRequest.subclass:
            return SearchLocationsRequest.subclass(*args_, **kwargs_)
        else:
            return SearchLocationsRequest(*args_, **kwargs_)
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
    def get_ServiceLevel(self):
        return self.ServiceLevel
    def set_ServiceLevel(self, ServiceLevel):
        self.ServiceLevel = ServiceLevel
    def get_ProcessingOptions(self):
        return self.ProcessingOptions
    def set_ProcessingOptions(self, ProcessingOptions):
        self.ProcessingOptions = ProcessingOptions
    def get_EffectiveDate(self):
        return self.EffectiveDate
    def set_EffectiveDate(self, EffectiveDate):
        self.EffectiveDate = EffectiveDate
    def get_LocationsSearchCriterion(self):
        return self.LocationsSearchCriterion
    def set_LocationsSearchCriterion(self, LocationsSearchCriterion):
        self.LocationsSearchCriterion = LocationsSearchCriterion
    def get_ShipperAccountNumber(self):
        return self.ShipperAccountNumber
    def set_ShipperAccountNumber(self, ShipperAccountNumber):
        self.ShipperAccountNumber = ShipperAccountNumber
    def get_RestrictionsAndPrivileges(self):
        return self.RestrictionsAndPrivileges
    def set_RestrictionsAndPrivileges(self, RestrictionsAndPrivileges):
        self.RestrictionsAndPrivileges = RestrictionsAndPrivileges
    def get_UniqueTrackingNumber(self):
        return self.UniqueTrackingNumber
    def set_UniqueTrackingNumber(self, UniqueTrackingNumber):
        self.UniqueTrackingNumber = UniqueTrackingNumber
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_PhoneNumber(self):
        return self.PhoneNumber
    def set_PhoneNumber(self, PhoneNumber):
        self.PhoneNumber = PhoneNumber
    def get_GeographicCoordinates(self):
        return self.GeographicCoordinates
    def set_GeographicCoordinates(self, GeographicCoordinates):
        self.GeographicCoordinates = GeographicCoordinates
    def get_MultipleMatchesAction(self):
        return self.MultipleMatchesAction
    def set_MultipleMatchesAction(self, MultipleMatchesAction):
        self.MultipleMatchesAction = MultipleMatchesAction
    def get_SortDetail(self):
        return self.SortDetail
    def set_SortDetail(self, SortDetail):
        self.SortDetail = SortDetail
    def get_Constraints(self):
        return self.Constraints
    def set_Constraints(self, Constraints):
        self.Constraints = Constraints
    def validate_SearchLocationsServiceLevelType(self, value):
        result = True
        # Validate type SearchLocationsServiceLevelType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['TRUSTED_PROXY']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on SearchLocationsServiceLevelType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_LocationsSearchCriteriaType(self, value):
        result = True
        # Validate type LocationsSearchCriteriaType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ADDRESS', 'GEOGRAPHIC_COORDINATES', 'MOBILE_PHONE_NUMBER', 'PHONE_NUMBER']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on LocationsSearchCriteriaType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_MultipleMatchesActionType(self, value):
        result = True
        # Validate type MultipleMatchesActionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['RETURN_ALL', 'RETURN_ERROR', 'RETURN_FIRST']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on MultipleMatchesActionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.UserDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.ServiceLevel is not None or
            self.ProcessingOptions is not None or
            self.EffectiveDate is not None or
            self.LocationsSearchCriterion is not None or
            self.ShipperAccountNumber is not None or
            self.RestrictionsAndPrivileges is not None or
            self.UniqueTrackingNumber is not None or
            self.Address is not None or
            self.PhoneNumber is not None or
            self.GeographicCoordinates is not None or
            self.MultipleMatchesAction is not None or
            self.SortDetail is not None or
            self.Constraints is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SearchLocationsRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SearchLocationsRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SearchLocationsRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SearchLocationsRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SearchLocationsRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SearchLocationsRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SearchLocationsRequest', fromsubclass_=False, pretty_print=True):
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
        if self.ServiceLevel is not None:
            namespaceprefix_ = self.ServiceLevel_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceLevel_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceLevel>%s</%sServiceLevel>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServiceLevel), input_name='ServiceLevel')), namespaceprefix_ , eol_))
        if self.ProcessingOptions is not None:
            namespaceprefix_ = self.ProcessingOptions_nsprefix_ + ':' if (UseCapturedNS_ and self.ProcessingOptions_nsprefix_) else ''
            self.ProcessingOptions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ProcessingOptions', pretty_print=pretty_print)
        if self.EffectiveDate is not None:
            namespaceprefix_ = self.EffectiveDate_nsprefix_ + ':' if (UseCapturedNS_ and self.EffectiveDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEffectiveDate>%s</%sEffectiveDate>%s' % (namespaceprefix_ , self.gds_format_date(self.EffectiveDate, input_name='EffectiveDate'), namespaceprefix_ , eol_))
        if self.LocationsSearchCriterion is not None:
            namespaceprefix_ = self.LocationsSearchCriterion_nsprefix_ + ':' if (UseCapturedNS_ and self.LocationsSearchCriterion_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocationsSearchCriterion>%s</%sLocationsSearchCriterion>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocationsSearchCriterion), input_name='LocationsSearchCriterion')), namespaceprefix_ , eol_))
        if self.ShipperAccountNumber is not None:
            namespaceprefix_ = self.ShipperAccountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipperAccountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipperAccountNumber>%s</%sShipperAccountNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShipperAccountNumber), input_name='ShipperAccountNumber')), namespaceprefix_ , eol_))
        if self.RestrictionsAndPrivileges is not None:
            namespaceprefix_ = self.RestrictionsAndPrivileges_nsprefix_ + ':' if (UseCapturedNS_ and self.RestrictionsAndPrivileges_nsprefix_) else ''
            self.RestrictionsAndPrivileges.export(outfile, level, namespaceprefix_, namespacedef_='', name_='RestrictionsAndPrivileges', pretty_print=pretty_print)
        if self.UniqueTrackingNumber is not None:
            namespaceprefix_ = self.UniqueTrackingNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.UniqueTrackingNumber_nsprefix_) else ''
            self.UniqueTrackingNumber.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UniqueTrackingNumber', pretty_print=pretty_print)
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.PhoneNumber is not None:
            namespaceprefix_ = self.PhoneNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.PhoneNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPhoneNumber>%s</%sPhoneNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PhoneNumber), input_name='PhoneNumber')), namespaceprefix_ , eol_))
        if self.GeographicCoordinates is not None:
            namespaceprefix_ = self.GeographicCoordinates_nsprefix_ + ':' if (UseCapturedNS_ and self.GeographicCoordinates_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGeographicCoordinates>%s</%sGeographicCoordinates>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GeographicCoordinates), input_name='GeographicCoordinates')), namespaceprefix_ , eol_))
        if self.MultipleMatchesAction is not None:
            namespaceprefix_ = self.MultipleMatchesAction_nsprefix_ + ':' if (UseCapturedNS_ and self.MultipleMatchesAction_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMultipleMatchesAction>%s</%sMultipleMatchesAction>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MultipleMatchesAction), input_name='MultipleMatchesAction')), namespaceprefix_ , eol_))
        if self.SortDetail is not None:
            namespaceprefix_ = self.SortDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.SortDetail_nsprefix_) else ''
            self.SortDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='SortDetail', pretty_print=pretty_print)
        if self.Constraints is not None:
            namespaceprefix_ = self.Constraints_nsprefix_ + ':' if (UseCapturedNS_ and self.Constraints_nsprefix_) else ''
            self.Constraints.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Constraints', pretty_print=pretty_print)
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
        elif nodeName_ == 'ServiceLevel':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServiceLevel')
            value_ = self.gds_validate_string(value_, node, 'ServiceLevel')
            self.ServiceLevel = value_
            self.ServiceLevel_nsprefix_ = child_.prefix
            # validate type SearchLocationsServiceLevelType
            self.validate_SearchLocationsServiceLevelType(self.ServiceLevel)
        elif nodeName_ == 'ProcessingOptions':
            obj_ = SearchLocationsProcessingOptionsRequested.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ProcessingOptions = obj_
            obj_.original_tagname_ = 'ProcessingOptions'
        elif nodeName_ == 'EffectiveDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.EffectiveDate = dval_
            self.EffectiveDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocationsSearchCriterion':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocationsSearchCriterion')
            value_ = self.gds_validate_string(value_, node, 'LocationsSearchCriterion')
            self.LocationsSearchCriterion = value_
            self.LocationsSearchCriterion_nsprefix_ = child_.prefix
            # validate type LocationsSearchCriteriaType
            self.validate_LocationsSearchCriteriaType(self.LocationsSearchCriterion)
        elif nodeName_ == 'ShipperAccountNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShipperAccountNumber')
            value_ = self.gds_validate_string(value_, node, 'ShipperAccountNumber')
            self.ShipperAccountNumber = value_
            self.ShipperAccountNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'RestrictionsAndPrivileges':
            obj_ = RestrictionsAndPrivilegesPolicyDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.RestrictionsAndPrivileges = obj_
            obj_.original_tagname_ = 'RestrictionsAndPrivileges'
        elif nodeName_ == 'UniqueTrackingNumber':
            obj_ = UniqueTrackingNumber.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UniqueTrackingNumber = obj_
            obj_.original_tagname_ = 'UniqueTrackingNumber'
        elif nodeName_ == 'Address':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'PhoneNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PhoneNumber')
            value_ = self.gds_validate_string(value_, node, 'PhoneNumber')
            self.PhoneNumber = value_
            self.PhoneNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'GeographicCoordinates':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GeographicCoordinates')
            value_ = self.gds_validate_string(value_, node, 'GeographicCoordinates')
            self.GeographicCoordinates = value_
            self.GeographicCoordinates_nsprefix_ = child_.prefix
        elif nodeName_ == 'MultipleMatchesAction':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MultipleMatchesAction')
            value_ = self.gds_validate_string(value_, node, 'MultipleMatchesAction')
            self.MultipleMatchesAction = value_
            self.MultipleMatchesAction_nsprefix_ = child_.prefix
            # validate type MultipleMatchesActionType
            self.validate_MultipleMatchesActionType(self.MultipleMatchesAction)
        elif nodeName_ == 'SortDetail':
            obj_ = LocationSortDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SortDetail = obj_
            obj_.original_tagname_ = 'SortDetail'
        elif nodeName_ == 'Constraints':
            obj_ = SearchLocationConstraints.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Constraints = obj_
            obj_.original_tagname_ = 'Constraints'
# end class SearchLocationsRequest


class ShippingHoliday(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Holiday=None, UnavailableActions=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Holiday = Holiday
        self.Holiday_nsprefix_ = "ns"
        if UnavailableActions is None:
            self.UnavailableActions = []
        else:
            self.UnavailableActions = UnavailableActions
        self.UnavailableActions_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShippingHoliday)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShippingHoliday.subclass:
            return ShippingHoliday.subclass(*args_, **kwargs_)
        else:
            return ShippingHoliday(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Holiday(self):
        return self.Holiday
    def set_Holiday(self, Holiday):
        self.Holiday = Holiday
    def get_UnavailableActions(self):
        return self.UnavailableActions
    def set_UnavailableActions(self, UnavailableActions):
        self.UnavailableActions = UnavailableActions
    def add_UnavailableActions(self, value):
        self.UnavailableActions.append(value)
    def insert_UnavailableActions_at(self, index, value):
        self.UnavailableActions.insert(index, value)
    def replace_UnavailableActions_at(self, index, value):
        self.UnavailableActions[index] = value
    def validate_ShippingActionType(self, value):
        result = True
        # Validate type ShippingActionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['DELIVERIES', 'PICKUPS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ShippingActionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Holiday is not None or
            self.UnavailableActions
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShippingHoliday', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShippingHoliday')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShippingHoliday':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShippingHoliday')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShippingHoliday', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShippingHoliday'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShippingHoliday', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Holiday is not None:
            namespaceprefix_ = self.Holiday_nsprefix_ + ':' if (UseCapturedNS_ and self.Holiday_nsprefix_) else ''
            self.Holiday.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Holiday', pretty_print=pretty_print)
        for UnavailableActions_ in self.UnavailableActions:
            namespaceprefix_ = self.UnavailableActions_nsprefix_ + ':' if (UseCapturedNS_ and self.UnavailableActions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUnavailableActions>%s</%sUnavailableActions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(UnavailableActions_), input_name='UnavailableActions')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Holiday':
            obj_ = Holiday.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Holiday = obj_
            obj_.original_tagname_ = 'Holiday'
        elif nodeName_ == 'UnavailableActions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UnavailableActions')
            value_ = self.gds_validate_string(value_, node, 'UnavailableActions')
            self.UnavailableActions.append(value_)
            self.UnavailableActions_nsprefix_ = child_.prefix
            # validate type ShippingActionType
            self.validate_ShippingActionType(self.UnavailableActions[-1])
# end class ShippingHoliday


class TimeRange(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Begins=None, Ends=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if isinstance(Begins, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Begins, '%H:%M:%S').time()
        else:
            initvalue_ = Begins
        self.Begins = initvalue_
        self.Begins_nsprefix_ = None
        if isinstance(Ends, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Ends, '%H:%M:%S').time()
        else:
            initvalue_ = Ends
        self.Ends = initvalue_
        self.Ends_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TimeRange)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TimeRange.subclass:
            return TimeRange.subclass(*args_, **kwargs_)
        else:
            return TimeRange(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TimeRange', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TimeRange')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TimeRange':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TimeRange')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TimeRange', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TimeRange'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TimeRange', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Begins is not None:
            namespaceprefix_ = self.Begins_nsprefix_ + ':' if (UseCapturedNS_ and self.Begins_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBegins>%s</%sBegins>%s' % (namespaceprefix_ , self.gds_format_time(self.Begins, input_name='Begins'), namespaceprefix_ , eol_))
        if self.Ends is not None:
            namespaceprefix_ = self.Ends_nsprefix_ + ':' if (UseCapturedNS_ and self.Ends_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEnds>%s</%sEnds>%s' % (namespaceprefix_ , self.gds_format_time(self.Ends, input_name='Ends'), namespaceprefix_ , eol_))
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
            sval_ = child_.text
            dval_ = self.gds_parse_time(sval_)
            self.Begins = dval_
            self.Begins_nsprefix_ = child_.prefix
        elif nodeName_ == 'Ends':
            sval_ = child_.text
            dval_ = self.gds_parse_time(sval_)
            self.Ends = dval_
            self.Ends_nsprefix_ = child_.prefix
# end class TimeRange


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


class Weight(GeneratedsSuper):
    """The descriptive data for the heaviness of an object."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Units=None, Value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Units = Units
        self.validate_WeightUnits(self.Units)
        self.Units_nsprefix_ = "ns"
        self.Value = Value
        self.Value_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Weight)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Weight.subclass:
            return Weight.subclass(*args_, **kwargs_)
        else:
            return Weight(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Units(self):
        return self.Units
    def set_Units(self, Units):
        self.Units = Units
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def validate_WeightUnits(self, value):
        result = True
        # Validate type WeightUnits, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['KG', 'LB']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on WeightUnits' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Units is not None or
            self.Value is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Weight', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Weight')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Weight':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Weight')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Weight', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Weight'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Weight', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Units is not None:
            namespaceprefix_ = self.Units_nsprefix_ + ':' if (UseCapturedNS_ and self.Units_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUnits>%s</%sUnits>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Units), input_name='Units')), namespaceprefix_ , eol_))
        if self.Value is not None:
            namespaceprefix_ = self.Value_nsprefix_ + ':' if (UseCapturedNS_ and self.Value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sValue>%s</%sValue>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Value, input_name='Value'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Units':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Units')
            value_ = self.gds_validate_string(value_, node, 'Units')
            self.Units = value_
            self.Units_nsprefix_ = child_.prefix
            # validate type WeightUnits
            self.validate_WeightUnits(self.Units)
        elif nodeName_ == 'Value' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Value')
            fval_ = self.gds_validate_decimal(fval_, node, 'Value')
            self.Value = fval_
            self.Value_nsprefix_ = child_.prefix
# end class Weight


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
        self.validate_ServiceIdType(self.ServiceId)
        self.ServiceId_nsprefix_ = "ns"
        self.Major = Major
        self.validate_MajorVersionType(self.Major)
        self.Major_nsprefix_ = "ns"
        self.Intermediate = Intermediate
        self.validate_IntermediateVersionType(self.Intermediate)
        self.Intermediate_nsprefix_ = "ns"
        self.Minor = Minor
        self.validate_MinorVersionType(self.Minor)
        self.Minor_nsprefix_ = "ns"
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
    def validate_ServiceIdType(self, value):
        result = True
        # Validate type ServiceIdType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['locs']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ServiceIdType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_MajorVersionType(self, value):
        result = True
        # Validate type MajorVersionType, a restriction on xs:int.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = [12]
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on MajorVersionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_IntermediateVersionType(self, value):
        result = True
        # Validate type IntermediateVersionType, a restriction on xs:int.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = [0]
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on IntermediateVersionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_MinorVersionType(self, value):
        result = True
        # Validate type MinorVersionType, a restriction on xs:int.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = [0]
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on MinorVersionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
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
            # validate type ServiceIdType
            self.validate_ServiceIdType(self.ServiceId)
        elif nodeName_ == 'Major' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Major')
            ival_ = self.gds_validate_integer(ival_, node, 'Major')
            self.Major = ival_
            self.Major_nsprefix_ = child_.prefix
            # validate type MajorVersionType
            self.validate_MajorVersionType(self.Major)
        elif nodeName_ == 'Intermediate' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Intermediate')
            ival_ = self.gds_validate_integer(ival_, node, 'Intermediate')
            self.Intermediate = ival_
            self.Intermediate_nsprefix_ = child_.prefix
            # validate type IntermediateVersionType
            self.validate_IntermediateVersionType(self.Intermediate)
        elif nodeName_ == 'Minor' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Minor')
            ival_ = self.gds_validate_integer(ival_, node, 'Minor')
            self.Minor = ival_
            self.Minor_nsprefix_ = child_.prefix
            # validate type MinorVersionType
            self.validate_MinorVersionType(self.Minor)
# end class VersionId


GDSClassesMapping = {
    'ListLocationsReply': ListLocationsReply,
    'ListLocationsRequest': ListLocationsRequest,
    'LookupLocationReply': LookupLocationReply,
    'LookupLocationRequest': LookupLocationRequest,
    'SearchLocationsReply': SearchLocationsReply,
    'SearchLocationsRequest': SearchLocationsRequest,
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
        rootTag = 'ListLocationsReply'
        rootClass = ListLocationsReply
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
        rootTag = 'ListLocationsReply'
        rootClass = ListLocationsReply
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
        rootTag = 'ListLocationsReply'
        rootClass = ListLocationsReply
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:ns="http://fedex.com/ws/locs/v12"')
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
        rootTag = 'ListLocationsReply'
        rootClass = ListLocationsReply
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from location_service_v12 import *\n\n')
        sys.stdout.write('import location_service_v12 as model_\n\n')
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
NamespaceToDefMappings_ = {'http://fedex.com/ws/locs/v12': [('AutoConfigurationType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('AvailableLocationsRequestServiceLevel',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('CarrierCodeType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('ConsolidationType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('CountryRelationshipType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('DayOfWeekType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('DistanceUnits',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('DistributionClearanceType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('EnterprisePermissionType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('ExpressRegionCode',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('FedExLocationType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('LatestDropOffOverlayType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('LinearUnits',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('LocationAccessibilityType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('LocationAttributesForInternalFedexUseType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('LocationAttributesType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('LocationContentOptionType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('LocationSearchFilterType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('LocationSortCriteriaType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('LocationSortOrderType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('LocationTransferOfPossessionType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('LocationsSearchCriteriaType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('MultipleMatchesActionType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('NotificationSeverityType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('OperationalHoursType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('ReservationAttributesType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('RestrictionsAndPrivilegesPolicyExceptionType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('SearchLocationsProcessingOptionType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('SearchLocationsServiceLevelType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('ServiceCategoryType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('ShippingActionType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('SupportedRedirectToHoldServiceType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('TransactionSourceFormat',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('WebServiceEnvironment',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('WeightUnits',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('MajorVersionType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('IntermediateVersionType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('MinorVersionType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('ServiceIdType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'ST'),
                                  ('Address',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('AddressAncillaryDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('AddressToLocationRelationshipDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('CarrierDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('ClearanceCountryDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('ClearanceLocationDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('ClientDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('Contact',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('DateRange',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('Dimensions',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('Distance',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('DistanceAndLocationDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('EnterprisePrivilegeDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('Holiday',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('InitiativeManifest',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('LatestDropOffDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('LatestDropoffOverlayDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('ListLocationsConstraints',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('ListLocationsReply',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('ListLocationsRequest',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('Localization',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('LocationCapabilityDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('LocationContactAndAddress',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('LocationDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('LocationFieldsForInternalFedexUseDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('LocationHours',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('LocationIdentificationDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('LocationPackageLimitsDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('LocationSortDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('LocationSupportedPackageDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('LocationSupportedShipmentDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('LookupLocationReply',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('LookupLocationRequest',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('Notification',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('NotificationParameter',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('PolicyGridManifest',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('ReservationAvailabilityDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('RestrictionsAndPrivilegesPolicyDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('SearchLocationConstraints',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('SearchLocationsProcessingOptionsRequested',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('SearchLocationsReply',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('SearchLocationsRequest',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('ShippingHoliday',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('TimeRange',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('TransactionDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('UniqueTrackingNumber',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('UserDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('Weight',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('WebAuthenticationDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('WebAuthenticationCredential',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT'),
                                  ('VersionId',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/LocationService_v12.xsd',
                                   'CT')]}

__all__ = [
    "Address",
    "AddressAncillaryDetail",
    "AddressToLocationRelationshipDetail",
    "CarrierDetail",
    "ClearanceCountryDetail",
    "ClearanceLocationDetail",
    "ClientDetail",
    "Contact",
    "DateRange",
    "Dimensions",
    "Distance",
    "DistanceAndLocationDetail",
    "EnterprisePrivilegeDetail",
    "Holiday",
    "InitiativeManifest",
    "LatestDropOffDetail",
    "LatestDropoffOverlayDetail",
    "ListLocationsConstraints",
    "ListLocationsReply",
    "ListLocationsRequest",
    "Localization",
    "LocationCapabilityDetail",
    "LocationContactAndAddress",
    "LocationDetail",
    "LocationFieldsForInternalFedexUseDetail",
    "LocationHours",
    "LocationIdentificationDetail",
    "LocationPackageLimitsDetail",
    "LocationSortDetail",
    "LocationSupportedPackageDetail",
    "LocationSupportedShipmentDetail",
    "LookupLocationReply",
    "LookupLocationRequest",
    "Notification",
    "NotificationParameter",
    "PolicyGridManifest",
    "ReservationAvailabilityDetail",
    "RestrictionsAndPrivilegesPolicyDetail",
    "SearchLocationConstraints",
    "SearchLocationsProcessingOptionsRequested",
    "SearchLocationsReply",
    "SearchLocationsRequest",
    "ShippingHoliday",
    "TimeRange",
    "TransactionDetail",
    "UniqueTrackingNumber",
    "UserDetail",
    "VersionId",
    "WebAuthenticationCredential",
    "WebAuthenticationDetail",
    "Weight"
]
