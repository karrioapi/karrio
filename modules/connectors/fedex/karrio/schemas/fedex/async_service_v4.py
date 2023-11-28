#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Thu May  6 11:00:02 2021 by generateDS.py version 2.38.6.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './fedex_lib/async_service_v4.py')
#
# Command line arguments:
#   /Users/danielkobina/Workspace/Carriers Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./fedex_lib/async_service_v4.py" /Users/danielkobina/Workspace/Carriers Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd
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


class ArtifactFormatType(str, Enum):
    """Identifies the format of the artifact."""
    BINARY='BINARY'
    DOC='DOC'
    EPL_2='EPL2'
    PDF='PDF'
    PNG='PNG'
    RTF='RTF'
    TEXT='TEXT'
    XML='XML'
    ZPLII='ZPLII'


class ArtifactType(str, Enum):
    """Identifies the type of artifact created."""
    AUXILIARY_LABEL='AUXILIARY_LABEL'
    CERTIFICATE_OF_ORIGIN='CERTIFICATE_OF_ORIGIN'
    COD_RETURN_LABEL='COD_RETURN_LABEL'
    COMMERCIAL_INVOICE='COMMERCIAL_INVOICE'
    COMMODITIES_BY_TRACKING_NUMBER_REPORT='COMMODITIES_BY_TRACKING_NUMBER_REPORT'
    CONDENSED_CRN_REPORT='CONDENSED_CRN_REPORT'
    CONSOLIDATED_COMMERCIAL_INVOICE='CONSOLIDATED_COMMERCIAL_INVOICE'
    CONSOLIDATED_CUSTOMS_LINEHAUL_REPORT='CONSOLIDATED_CUSTOMS_LINEHAUL_REPORT'
    CONSOLIDATED_SOLD_TO_SUMMARY_REPORT='CONSOLIDATED_SOLD_TO_SUMMARY_REPORT'
    CRN_REPORT='CRN_REPORT'
    CUSTOMS_PACKING_LIST='CUSTOMS_PACKING_LIST'
    CUSTOM_CONSOLIDATION_DOCUMENT='CUSTOM_CONSOLIDATION_DOCUMENT'
    CUSTOM_PACKAGE_DOCUMENT='CUSTOM_PACKAGE_DOCUMENT'
    CUSTOM_SHIPMENT_DOCUMENT='CUSTOM_SHIPMENT_DOCUMENT'
    DANGEROUS_GOODS_SHIPPERS_DECLARATION='DANGEROUS_GOODS_SHIPPERS_DECLARATION'
    DELIVERY_ON_INVOICE_ACCEPTANCE_RETURN_LABEL='DELIVERY_ON_INVOICE_ACCEPTANCE_RETURN_LABEL'
    FREIGHT_ADDRESS_LABEL='FREIGHT_ADDRESS_LABEL'
    GENERAL_AGENCY_AGREEMENT='GENERAL_AGENCY_AGREEMENT'
    LOW_CUSTOMS_VALUE_EXCEPTION_PARTY_REPORT='LOW_CUSTOMS_VALUE_EXCEPTION_PARTY_REPORT'
    NAFTA_CERTIFICATE_OF_ORIGIN='NAFTA_CERTIFICATE_OF_ORIGIN'
    OP__900='OP_900'
    OUTBOUND_LABEL='OUTBOUND_LABEL'
    PRO_FORMA_INVOICE='PRO_FORMA_INVOICE'
    RETURN_INSTRUCTIONS='RETURN_INSTRUCTIONS'
    SERVICE_REPLY='SERVICE_REPLY'
    SERVICE_REQUEST='SERVICE_REQUEST'
    STANDARD_BROKER_CLEARANCE_PARTY_REPORT='STANDARD_BROKER_CLEARANCE_PARTY_REPORT'
    TERMS_AND_CONDITIONS='TERMS_AND_CONDITIONS'


class ExpressRegionCode(str, Enum):
    """Indicates a FedEx Express operating region."""
    APAC='APAC'
    CA='CA'
    EMEA='EMEA'
    LAC='LAC'
    US='US'


class NotificationSeverityType(str, Enum):
    ERROR='ERROR'
    FAILURE='FAILURE'
    NOTE='NOTE'
    SUCCESS='SUCCESS'
    WARNING='WARNING'


class ArtifactPart(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, SequenceNumber=None, Contents=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.SequenceNumber = SequenceNumber
        self.SequenceNumber_nsprefix_ = None
        self.Contents = Contents
        self.Contents_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArtifactPart)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArtifactPart.subclass:
            return ArtifactPart.subclass(*args_, **kwargs_)
        else:
            return ArtifactPart(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_SequenceNumber(self):
        return self.SequenceNumber
    def set_SequenceNumber(self, SequenceNumber):
        self.SequenceNumber = SequenceNumber
    def get_Contents(self):
        return self.Contents
    def set_Contents(self, Contents):
        self.Contents = Contents
    def hasContent_(self):
        if (
            self.SequenceNumber is not None or
            self.Contents is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArtifactPart', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArtifactPart')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArtifactPart':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArtifactPart')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArtifactPart', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArtifactPart'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArtifactPart', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.SequenceNumber is not None:
            namespaceprefix_ = self.SequenceNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.SequenceNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSequenceNumber>%s</%sSequenceNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.SequenceNumber, input_name='SequenceNumber'), namespaceprefix_ , eol_))
        if self.Contents is not None:
            namespaceprefix_ = self.Contents_nsprefix_ + ':' if (UseCapturedNS_ and self.Contents_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sContents>%s</%sContents>%s' % (namespaceprefix_ , self.gds_format_base64(self.Contents, input_name='Contents'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'SequenceNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'SequenceNumber')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'SequenceNumber')
            self.SequenceNumber = ival_
            self.SequenceNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'Contents':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'Contents')
            else:
                bval_ = None
            self.Contents = bval_
            self.Contents_nsprefix_ = child_.prefix
# end class ArtifactPart


class ArtifactRetrievalFilter(GeneratedsSuper):
    """Specifies the details about the criteria used for artifact selection
    during retrieval."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AccessReference=None, Type=None, ReferenceId=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.AccessReference = AccessReference
        self.AccessReference_nsprefix_ = None
        self.Type = Type
        self.validate_ArtifactType(self.Type)
        self.Type_nsprefix_ = "ns"
        self.ReferenceId = ReferenceId
        self.ReferenceId_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArtifactRetrievalFilter)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArtifactRetrievalFilter.subclass:
            return ArtifactRetrievalFilter.subclass(*args_, **kwargs_)
        else:
            return ArtifactRetrievalFilter(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AccessReference(self):
        return self.AccessReference
    def set_AccessReference(self, AccessReference):
        self.AccessReference = AccessReference
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_ReferenceId(self):
        return self.ReferenceId
    def set_ReferenceId(self, ReferenceId):
        self.ReferenceId = ReferenceId
    def validate_ArtifactType(self, value):
        result = True
        # Validate type ArtifactType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['AUXILIARY_LABEL', 'CERTIFICATE_OF_ORIGIN', 'COD_RETURN_LABEL', 'COMMERCIAL_INVOICE', 'COMMODITIES_BY_TRACKING_NUMBER_REPORT', 'CONDENSED_CRN_REPORT', 'CONSOLIDATED_COMMERCIAL_INVOICE', 'CONSOLIDATED_CUSTOMS_LINEHAUL_REPORT', 'CONSOLIDATED_SOLD_TO_SUMMARY_REPORT', 'CRN_REPORT', 'CUSTOMS_PACKING_LIST', 'CUSTOM_CONSOLIDATION_DOCUMENT', 'CUSTOM_PACKAGE_DOCUMENT', 'CUSTOM_SHIPMENT_DOCUMENT', 'DANGEROUS_GOODS_SHIPPERS_DECLARATION', 'DELIVERY_ON_INVOICE_ACCEPTANCE_RETURN_LABEL', 'FREIGHT_ADDRESS_LABEL', 'GENERAL_AGENCY_AGREEMENT', 'LOW_CUSTOMS_VALUE_EXCEPTION_PARTY_REPORT', 'NAFTA_CERTIFICATE_OF_ORIGIN', 'OP_900', 'OUTBOUND_LABEL', 'PRO_FORMA_INVOICE', 'RETURN_INSTRUCTIONS', 'SERVICE_REPLY', 'SERVICE_REQUEST', 'STANDARD_BROKER_CLEARANCE_PARTY_REPORT', 'TERMS_AND_CONDITIONS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ArtifactType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.AccessReference is not None or
            self.Type is not None or
            self.ReferenceId is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArtifactRetrievalFilter', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArtifactRetrievalFilter')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArtifactRetrievalFilter':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArtifactRetrievalFilter')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArtifactRetrievalFilter', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArtifactRetrievalFilter'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArtifactRetrievalFilter', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.AccessReference is not None:
            namespaceprefix_ = self.AccessReference_nsprefix_ + ':' if (UseCapturedNS_ and self.AccessReference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccessReference>%s</%sAccessReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AccessReference), input_name='AccessReference')), namespaceprefix_ , eol_))
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sType>%s</%sType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Type), input_name='Type')), namespaceprefix_ , eol_))
        if self.ReferenceId is not None:
            namespaceprefix_ = self.ReferenceId_nsprefix_ + ':' if (UseCapturedNS_ and self.ReferenceId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReferenceId>%s</%sReferenceId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ReferenceId), input_name='ReferenceId')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'AccessReference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AccessReference')
            value_ = self.gds_validate_string(value_, node, 'AccessReference')
            self.AccessReference = value_
            self.AccessReference_nsprefix_ = child_.prefix
        elif nodeName_ == 'Type':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Type')
            value_ = self.gds_validate_string(value_, node, 'Type')
            self.Type = value_
            self.Type_nsprefix_ = child_.prefix
            # validate type ArtifactType
            self.validate_ArtifactType(self.Type)
        elif nodeName_ == 'ReferenceId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ReferenceId')
            value_ = self.gds_validate_string(value_, node, 'ReferenceId')
            self.ReferenceId = value_
            self.ReferenceId_nsprefix_ = child_.prefix
# end class ArtifactRetrievalFilter


class ClientDetail(GeneratedsSuper):
    """Descriptive data for the client submitting a transaction."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AccountNumber=None, MeterNumber=None, MeterInstance=None, IntegratorId=None, Region=None, Localization=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.AccountNumber = AccountNumber
        self.AccountNumber_nsprefix_ = None
        self.MeterNumber = MeterNumber
        self.MeterNumber_nsprefix_ = None
        self.MeterInstance = MeterInstance
        self.MeterInstance_nsprefix_ = None
        self.IntegratorId = IntegratorId
        self.IntegratorId_nsprefix_ = None
        self.Region = Region
        self.validate_ExpressRegionCode(self.Region)
        self.Region_nsprefix_ = "ns"
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
    def get_MeterNumber(self):
        return self.MeterNumber
    def set_MeterNumber(self, MeterNumber):
        self.MeterNumber = MeterNumber
    def get_MeterInstance(self):
        return self.MeterInstance
    def set_MeterInstance(self, MeterInstance):
        self.MeterInstance = MeterInstance
    def get_IntegratorId(self):
        return self.IntegratorId
    def set_IntegratorId(self, IntegratorId):
        self.IntegratorId = IntegratorId
    def get_Region(self):
        return self.Region
    def set_Region(self, Region):
        self.Region = Region
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
    def hasContent_(self):
        if (
            self.AccountNumber is not None or
            self.MeterNumber is not None or
            self.MeterInstance is not None or
            self.IntegratorId is not None or
            self.Region is not None or
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
        if self.MeterNumber is not None:
            namespaceprefix_ = self.MeterNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.MeterNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMeterNumber>%s</%sMeterNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MeterNumber), input_name='MeterNumber')), namespaceprefix_ , eol_))
        if self.MeterInstance is not None:
            namespaceprefix_ = self.MeterInstance_nsprefix_ + ':' if (UseCapturedNS_ and self.MeterInstance_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMeterInstance>%s</%sMeterInstance>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MeterInstance), input_name='MeterInstance')), namespaceprefix_ , eol_))
        if self.IntegratorId is not None:
            namespaceprefix_ = self.IntegratorId_nsprefix_ + ':' if (UseCapturedNS_ and self.IntegratorId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIntegratorId>%s</%sIntegratorId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IntegratorId), input_name='IntegratorId')), namespaceprefix_ , eol_))
        if self.Region is not None:
            namespaceprefix_ = self.Region_nsprefix_ + ':' if (UseCapturedNS_ and self.Region_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRegion>%s</%sRegion>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Region), input_name='Region')), namespaceprefix_ , eol_))
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
        elif nodeName_ == 'MeterNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MeterNumber')
            value_ = self.gds_validate_string(value_, node, 'MeterNumber')
            self.MeterNumber = value_
            self.MeterNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'MeterInstance':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MeterInstance')
            value_ = self.gds_validate_string(value_, node, 'MeterInstance')
            self.MeterInstance = value_
            self.MeterInstance_nsprefix_ = child_.prefix
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
        elif nodeName_ == 'Localization':
            obj_ = Localization.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Localization = obj_
            obj_.original_tagname_ = 'Localization'
# end class ClientDetail


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


class RetrieveJobResultsReply(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, Artifacts=None, gds_collector_=None, **kwargs_):
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
        if Artifacts is None:
            self.Artifacts = []
        else:
            self.Artifacts = Artifacts
        self.Artifacts_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RetrieveJobResultsReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RetrieveJobResultsReply.subclass:
            return RetrieveJobResultsReply.subclass(*args_, **kwargs_)
        else:
            return RetrieveJobResultsReply(*args_, **kwargs_)
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
    def get_Artifacts(self):
        return self.Artifacts
    def set_Artifacts(self, Artifacts):
        self.Artifacts = Artifacts
    def add_Artifacts(self, value):
        self.Artifacts.append(value)
    def insert_Artifacts_at(self, index, value):
        self.Artifacts.insert(index, value)
    def replace_Artifacts_at(self, index, value):
        self.Artifacts[index] = value
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
            self.Artifacts
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RetrieveJobResultsReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RetrieveJobResultsReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RetrieveJobResultsReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RetrieveJobResultsReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RetrieveJobResultsReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RetrieveJobResultsReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RetrieveJobResultsReply', fromsubclass_=False, pretty_print=True):
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
        for Artifacts_ in self.Artifacts:
            namespaceprefix_ = self.Artifacts_nsprefix_ + ':' if (UseCapturedNS_ and self.Artifacts_nsprefix_) else ''
            Artifacts_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Artifacts', pretty_print=pretty_print)
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
        elif nodeName_ == 'Artifacts':
            obj_ = RetrievedArtifact.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Artifacts.append(obj_)
            obj_.original_tagname_ = 'Artifacts'
# end class RetrieveJobResultsReply


class RetrieveJobResultsRequest(GeneratedsSuper):
    """This request object is used by the client to retrieve artifacts stored
    by the ASYNC service."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, TransactionDetail=None, Version=None, JobId=None, Filters=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.WebAuthenticationDetail = WebAuthenticationDetail
        self.WebAuthenticationDetail_nsprefix_ = "ns"
        self.ClientDetail = ClientDetail
        self.ClientDetail_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.JobId = JobId
        self.JobId_nsprefix_ = None
        if Filters is None:
            self.Filters = []
        else:
            self.Filters = Filters
        self.Filters_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RetrieveJobResultsRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RetrieveJobResultsRequest.subclass:
            return RetrieveJobResultsRequest.subclass(*args_, **kwargs_)
        else:
            return RetrieveJobResultsRequest(*args_, **kwargs_)
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
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_JobId(self):
        return self.JobId
    def set_JobId(self, JobId):
        self.JobId = JobId
    def get_Filters(self):
        return self.Filters
    def set_Filters(self, Filters):
        self.Filters = Filters
    def add_Filters(self, value):
        self.Filters.append(value)
    def insert_Filters_at(self, index, value):
        self.Filters.insert(index, value)
    def replace_Filters_at(self, index, value):
        self.Filters[index] = value
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.JobId is not None or
            self.Filters
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RetrieveJobResultsRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RetrieveJobResultsRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RetrieveJobResultsRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RetrieveJobResultsRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RetrieveJobResultsRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RetrieveJobResultsRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RetrieveJobResultsRequest', fromsubclass_=False, pretty_print=True):
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
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.JobId is not None:
            namespaceprefix_ = self.JobId_nsprefix_ + ':' if (UseCapturedNS_ and self.JobId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sJobId>%s</%sJobId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.JobId), input_name='JobId')), namespaceprefix_ , eol_))
        for Filters_ in self.Filters:
            namespaceprefix_ = self.Filters_nsprefix_ + ':' if (UseCapturedNS_ and self.Filters_nsprefix_) else ''
            Filters_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Filters', pretty_print=pretty_print)
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
        elif nodeName_ == 'JobId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'JobId')
            value_ = self.gds_validate_string(value_, node, 'JobId')
            self.JobId = value_
            self.JobId_nsprefix_ = child_.prefix
        elif nodeName_ == 'Filters':
            obj_ = ArtifactRetrievalFilter.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Filters.append(obj_)
            obj_.original_tagname_ = 'Filters'
# end class RetrieveJobResultsRequest


class RetrievedArtifact(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AccessReference=None, HighestSeverity=None, Notifications=None, Type=None, Format=None, FormatSpecification=None, ReferenceId=None, Parts=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.AccessReference = AccessReference
        self.AccessReference_nsprefix_ = None
        self.HighestSeverity = HighestSeverity
        self.validate_NotificationSeverityType(self.HighestSeverity)
        self.HighestSeverity_nsprefix_ = "ns"
        if Notifications is None:
            self.Notifications = []
        else:
            self.Notifications = Notifications
        self.Notifications_nsprefix_ = "ns"
        self.Type = Type
        self.validate_ArtifactType(self.Type)
        self.Type_nsprefix_ = "ns"
        self.Format = Format
        self.validate_ArtifactFormatType(self.Format)
        self.Format_nsprefix_ = "ns"
        self.FormatSpecification = FormatSpecification
        self.FormatSpecification_nsprefix_ = None
        self.ReferenceId = ReferenceId
        self.ReferenceId_nsprefix_ = None
        if Parts is None:
            self.Parts = []
        else:
            self.Parts = Parts
        self.Parts_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RetrievedArtifact)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RetrievedArtifact.subclass:
            return RetrievedArtifact.subclass(*args_, **kwargs_)
        else:
            return RetrievedArtifact(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AccessReference(self):
        return self.AccessReference
    def set_AccessReference(self, AccessReference):
        self.AccessReference = AccessReference
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
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_Format(self):
        return self.Format
    def set_Format(self, Format):
        self.Format = Format
    def get_FormatSpecification(self):
        return self.FormatSpecification
    def set_FormatSpecification(self, FormatSpecification):
        self.FormatSpecification = FormatSpecification
    def get_ReferenceId(self):
        return self.ReferenceId
    def set_ReferenceId(self, ReferenceId):
        self.ReferenceId = ReferenceId
    def get_Parts(self):
        return self.Parts
    def set_Parts(self, Parts):
        self.Parts = Parts
    def add_Parts(self, value):
        self.Parts.append(value)
    def insert_Parts_at(self, index, value):
        self.Parts.insert(index, value)
    def replace_Parts_at(self, index, value):
        self.Parts[index] = value
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
    def validate_ArtifactType(self, value):
        result = True
        # Validate type ArtifactType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['AUXILIARY_LABEL', 'CERTIFICATE_OF_ORIGIN', 'COD_RETURN_LABEL', 'COMMERCIAL_INVOICE', 'COMMODITIES_BY_TRACKING_NUMBER_REPORT', 'CONDENSED_CRN_REPORT', 'CONSOLIDATED_COMMERCIAL_INVOICE', 'CONSOLIDATED_CUSTOMS_LINEHAUL_REPORT', 'CONSOLIDATED_SOLD_TO_SUMMARY_REPORT', 'CRN_REPORT', 'CUSTOMS_PACKING_LIST', 'CUSTOM_CONSOLIDATION_DOCUMENT', 'CUSTOM_PACKAGE_DOCUMENT', 'CUSTOM_SHIPMENT_DOCUMENT', 'DANGEROUS_GOODS_SHIPPERS_DECLARATION', 'DELIVERY_ON_INVOICE_ACCEPTANCE_RETURN_LABEL', 'FREIGHT_ADDRESS_LABEL', 'GENERAL_AGENCY_AGREEMENT', 'LOW_CUSTOMS_VALUE_EXCEPTION_PARTY_REPORT', 'NAFTA_CERTIFICATE_OF_ORIGIN', 'OP_900', 'OUTBOUND_LABEL', 'PRO_FORMA_INVOICE', 'RETURN_INSTRUCTIONS', 'SERVICE_REPLY', 'SERVICE_REQUEST', 'STANDARD_BROKER_CLEARANCE_PARTY_REPORT', 'TERMS_AND_CONDITIONS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ArtifactType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ArtifactFormatType(self, value):
        result = True
        # Validate type ArtifactFormatType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['BINARY', 'DOC', 'EPL2', 'PDF', 'PNG', 'RTF', 'TEXT', 'XML', 'ZPLII']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ArtifactFormatType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.AccessReference is not None or
            self.HighestSeverity is not None or
            self.Notifications or
            self.Type is not None or
            self.Format is not None or
            self.FormatSpecification is not None or
            self.ReferenceId is not None or
            self.Parts
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RetrievedArtifact', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RetrievedArtifact')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RetrievedArtifact':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RetrievedArtifact')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RetrievedArtifact', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RetrievedArtifact'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RetrievedArtifact', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.AccessReference is not None:
            namespaceprefix_ = self.AccessReference_nsprefix_ + ':' if (UseCapturedNS_ and self.AccessReference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccessReference>%s</%sAccessReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AccessReference), input_name='AccessReference')), namespaceprefix_ , eol_))
        if self.HighestSeverity is not None:
            namespaceprefix_ = self.HighestSeverity_nsprefix_ + ':' if (UseCapturedNS_ and self.HighestSeverity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHighestSeverity>%s</%sHighestSeverity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HighestSeverity), input_name='HighestSeverity')), namespaceprefix_ , eol_))
        for Notifications_ in self.Notifications:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            Notifications_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sType>%s</%sType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Type), input_name='Type')), namespaceprefix_ , eol_))
        if self.Format is not None:
            namespaceprefix_ = self.Format_nsprefix_ + ':' if (UseCapturedNS_ and self.Format_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFormat>%s</%sFormat>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Format), input_name='Format')), namespaceprefix_ , eol_))
        if self.FormatSpecification is not None:
            namespaceprefix_ = self.FormatSpecification_nsprefix_ + ':' if (UseCapturedNS_ and self.FormatSpecification_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFormatSpecification>%s</%sFormatSpecification>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FormatSpecification), input_name='FormatSpecification')), namespaceprefix_ , eol_))
        if self.ReferenceId is not None:
            namespaceprefix_ = self.ReferenceId_nsprefix_ + ':' if (UseCapturedNS_ and self.ReferenceId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReferenceId>%s</%sReferenceId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ReferenceId), input_name='ReferenceId')), namespaceprefix_ , eol_))
        for Parts_ in self.Parts:
            namespaceprefix_ = self.Parts_nsprefix_ + ':' if (UseCapturedNS_ and self.Parts_nsprefix_) else ''
            Parts_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Parts', pretty_print=pretty_print)
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
        if nodeName_ == 'AccessReference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AccessReference')
            value_ = self.gds_validate_string(value_, node, 'AccessReference')
            self.AccessReference = value_
            self.AccessReference_nsprefix_ = child_.prefix
        elif nodeName_ == 'HighestSeverity':
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
        elif nodeName_ == 'Type':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Type')
            value_ = self.gds_validate_string(value_, node, 'Type')
            self.Type = value_
            self.Type_nsprefix_ = child_.prefix
            # validate type ArtifactType
            self.validate_ArtifactType(self.Type)
        elif nodeName_ == 'Format':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Format')
            value_ = self.gds_validate_string(value_, node, 'Format')
            self.Format = value_
            self.Format_nsprefix_ = child_.prefix
            # validate type ArtifactFormatType
            self.validate_ArtifactFormatType(self.Format)
        elif nodeName_ == 'FormatSpecification':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FormatSpecification')
            value_ = self.gds_validate_string(value_, node, 'FormatSpecification')
            self.FormatSpecification = value_
            self.FormatSpecification_nsprefix_ = child_.prefix
        elif nodeName_ == 'ReferenceId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ReferenceId')
            value_ = self.gds_validate_string(value_, node, 'ReferenceId')
            self.ReferenceId = value_
            self.ReferenceId_nsprefix_ = child_.prefix
        elif nodeName_ == 'Parts':
            obj_ = ArtifactPart.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Parts.append(obj_)
            obj_.original_tagname_ = 'Parts'
# end class RetrievedArtifact


class TransactionDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CustomerTransactionId=None, Localization=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CustomerTransactionId = CustomerTransactionId
        self.CustomerTransactionId_nsprefix_ = None
        self.Localization = Localization
        self.Localization_nsprefix_ = "ns"
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
    def hasContent_(self):
        if (
            self.CustomerTransactionId is not None or
            self.Localization is not None
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
# end class TransactionDetail


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
    'RetrieveJobResultsReply': RetrieveJobResultsReply,
    'RetrieveJobResultsRequest': RetrieveJobResultsRequest,
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
        rootTag = 'RetrieveJobResultsReply'
        rootClass = RetrieveJobResultsReply
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
        rootTag = 'RetrieveJobResultsReply'
        rootClass = RetrieveJobResultsReply
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
        rootTag = 'RetrieveJobResultsReply'
        rootClass = RetrieveJobResultsReply
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:ns="http://fedex.com/ws/async/v4"')
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
        rootTag = 'RetrieveJobResultsReply'
        rootClass = RetrieveJobResultsReply
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from async_service_v4 import *\n\n')
        sys.stdout.write('import async_service_v4 as model_\n\n')
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
NamespaceToDefMappings_ = {'http://fedex.com/ws/async/v4': [('ArtifactFormatType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd',
                                   'ST'),
                                  ('ArtifactType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd',
                                   'ST'),
                                  ('ExpressRegionCode',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd',
                                   'ST'),
                                  ('NotificationSeverityType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd',
                                   'ST'),
                                  ('ArtifactPart',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd',
                                   'CT'),
                                  ('ArtifactRetrievalFilter',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd',
                                   'CT'),
                                  ('ClientDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd',
                                   'CT'),
                                  ('Localization',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd',
                                   'CT'),
                                  ('Notification',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd',
                                   'CT'),
                                  ('NotificationParameter',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd',
                                   'CT'),
                                  ('RetrieveJobResultsReply',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd',
                                   'CT'),
                                  ('RetrieveJobResultsRequest',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd',
                                   'CT'),
                                  ('RetrievedArtifact',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd',
                                   'CT'),
                                  ('TransactionDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd',
                                   'CT'),
                                  ('WebAuthenticationDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd',
                                   'CT'),
                                  ('WebAuthenticationCredential',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd',
                                   'CT'),
                                  ('VersionId',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/ASYNCService_v4.xsd',
                                   'CT')]}

__all__ = [
    "ArtifactPart",
    "ArtifactRetrievalFilter",
    "ClientDetail",
    "Localization",
    "Notification",
    "NotificationParameter",
    "RetrieveJobResultsReply",
    "RetrieveJobResultsRequest",
    "RetrievedArtifact",
    "TransactionDetail",
    "VersionId",
    "WebAuthenticationCredential",
    "WebAuthenticationDetail"
]
