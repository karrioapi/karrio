#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Thu May  6 11:00:03 2021 by generateDS.py version 2.38.6.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './fedex_lib/close_service_v5.py')
#
# Command line arguments:
#   /Users/danielkobina/Workspace/Carriers Doc/Fedex/2020-09/schemas/CloseService_v5.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./fedex_lib/close_service_v5.py" /Users/danielkobina/Workspace/Carriers Doc/Fedex/2020-09/schemas/CloseService_v5.xsd
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


class CarrierCodeType(str, Enum):
    """Identification of a FedEx operating company (transportation)."""
    FDXC='FDXC'
    FDXE='FDXE'
    FDXG='FDXG'
    FXCC='FXCC'
    FXFR='FXFR'
    FXSP='FXSP'


class CloseActionType(str, Enum):
    CLOSE='CLOSE'
    PREVIEW_CLOSE_DOCUMENTS='PREVIEW_CLOSE_DOCUMENTS'
    REPRINT_CLOSE_DOCUMENTS='REPRINT_CLOSE_DOCUMENTS'


class CloseDocumentType(str, Enum):
    COD_REPORT='COD_REPORT'
    DETAILED_DELIVERY_MANIFEST='DETAILED_DELIVERY_MANIFEST'
    HAZARDOUS_MATERIALS_CERTIFICATION='HAZARDOUS_MATERIALS_CERTIFICATION'
    MANIFEST='MANIFEST'
    MULTIWEIGHT_REPORT='MULTIWEIGHT_REPORT'
    OP__950='OP_950'


class CloseGroupingType(str, Enum):
    """Specifies how the shipment close requests are grouped."""
    MANIFEST_REFERENCE='MANIFEST_REFERENCE'
    SHIPPING_CYCLE='SHIPPING_CYCLE'
    TIME='TIME'


class CloseReportType(str, Enum):
    ALL='ALL'
    COD='COD'
    HAZMAT='HAZMAT'
    MANIFEST='MANIFEST'
    MULTIWEIGHT='MULTIWEIGHT'


class CloseWithDocumentsProcessingOptionType(str, Enum):
    ERROR_IF_OPEN_SHIPMENTS_FOUND='ERROR_IF_OPEN_SHIPMENTS_FOUND'
    WARNING_IF_OPEN_SHIPMENTS_FOUND='WARNING_IF_OPEN_SHIPMENTS_FOUND'


class CustomerImageUsageType(str, Enum):
    LETTER_HEAD='LETTER_HEAD'
    SIGNATURE='SIGNATURE'


class CustomerReferenceType(str, Enum):
    BILL_OF_LADING='BILL_OF_LADING'
    CUSTOMER_REFERENCE='CUSTOMER_REFERENCE'
    DEPARTMENT_NUMBER='DEPARTMENT_NUMBER'
    ELECTRONIC_PRODUCT_CODE='ELECTRONIC_PRODUCT_CODE'
    INTRACOUNTRY_REGULATORY_REFERENCE='INTRACOUNTRY_REGULATORY_REFERENCE'
    INVOICE_NUMBER='INVOICE_NUMBER'
    PACKING_SLIP_NUMBER='PACKING_SLIP_NUMBER'
    P_O_NUMBER='P_O_NUMBER'
    RMA_ASSOCIATION='RMA_ASSOCIATION'
    SHIPMENT_INTEGRITY='SHIPMENT_INTEGRITY'
    STORE_NUMBER='STORE_NUMBER'


class EMailNotificationRecipientType(str, Enum):
    BROKER='BROKER'
    OTHER='OTHER'
    RECIPIENT='RECIPIENT'
    SHIPPER='SHIPPER'
    THIRD_PARTY='THIRD_PARTY'


class ImageId(str, Enum):
    IMAGE__1='IMAGE_1'
    IMAGE__2='IMAGE_2'
    IMAGE__3='IMAGE_3'
    IMAGE__4='IMAGE_4'
    IMAGE__5='IMAGE_5'


class InternalImageType(str, Enum):
    LETTER_HEAD='LETTER_HEAD'
    SIGNATURE='SIGNATURE'


class LinearUnits(str, Enum):
    CM='CM'
    IN='IN'


class NotificationSeverityType(str, Enum):
    ERROR='ERROR'
    FAILURE='FAILURE'
    NOTE='NOTE'
    SUCCESS='SUCCESS'
    WARNING='WARNING'


class ReprintGroundCloseDocumentsOptionType(str, Enum):
    """Identifies the requested options to reprinting Ground Close Documents"""
    BY_SHIP_DATE='BY_SHIP_DATE'
    BY_TRACKING_NUMBER='BY_TRACKING_NUMBER'


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


class ClientDetail(GeneratedsSuper):
    """Descriptive data for the client submitting a transaction."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AccountNumber=None, MeterNumber=None, IntegratorId=None, Localization=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.AccountNumber = AccountNumber
        self.AccountNumber_nsprefix_ = None
        self.MeterNumber = MeterNumber
        self.MeterNumber_nsprefix_ = None
        self.IntegratorId = IntegratorId
        self.IntegratorId_nsprefix_ = None
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
    def get_IntegratorId(self):
        return self.IntegratorId
    def set_IntegratorId(self, IntegratorId):
        self.IntegratorId = IntegratorId
    def get_Localization(self):
        return self.Localization
    def set_Localization(self, Localization):
        self.Localization = Localization
    def hasContent_(self):
        if (
            self.AccountNumber is not None or
            self.MeterNumber is not None or
            self.IntegratorId is not None or
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
        if self.IntegratorId is not None:
            namespaceprefix_ = self.IntegratorId_nsprefix_ + ':' if (UseCapturedNS_ and self.IntegratorId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIntegratorId>%s</%sIntegratorId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IntegratorId), input_name='IntegratorId')), namespaceprefix_ , eol_))
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
        elif nodeName_ == 'IntegratorId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IntegratorId')
            value_ = self.gds_validate_string(value_, node, 'IntegratorId')
            self.IntegratorId = value_
            self.IntegratorId_nsprefix_ = child_.prefix
        elif nodeName_ == 'Localization':
            obj_ = Localization.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Localization = obj_
            obj_.original_tagname_ = 'Localization'
# end class ClientDetail


class CloseDocument(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Type=None, ShippingCycle=None, ShippingDocumentDisposition=None, AccessReference=None, Resolution=None, CopiesToPrint=None, Parts=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Type = Type
        self.validate_CloseDocumentType(self.Type)
        self.Type_nsprefix_ = "ns"
        self.ShippingCycle = ShippingCycle
        self.ShippingCycle_nsprefix_ = None
        self.ShippingDocumentDisposition = ShippingDocumentDisposition
        self.validate_ShippingDocumentDispositionType(self.ShippingDocumentDisposition)
        self.ShippingDocumentDisposition_nsprefix_ = "ns"
        self.AccessReference = AccessReference
        self.AccessReference_nsprefix_ = None
        self.Resolution = Resolution
        self.Resolution_nsprefix_ = None
        self.CopiesToPrint = CopiesToPrint
        self.CopiesToPrint_nsprefix_ = None
        if Parts is None:
            self.Parts = []
        else:
            self.Parts = Parts
        self.Parts_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CloseDocument)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CloseDocument.subclass:
            return CloseDocument.subclass(*args_, **kwargs_)
        else:
            return CloseDocument(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_ShippingCycle(self):
        return self.ShippingCycle
    def set_ShippingCycle(self, ShippingCycle):
        self.ShippingCycle = ShippingCycle
    def get_ShippingDocumentDisposition(self):
        return self.ShippingDocumentDisposition
    def set_ShippingDocumentDisposition(self, ShippingDocumentDisposition):
        self.ShippingDocumentDisposition = ShippingDocumentDisposition
    def get_AccessReference(self):
        return self.AccessReference
    def set_AccessReference(self, AccessReference):
        self.AccessReference = AccessReference
    def get_Resolution(self):
        return self.Resolution
    def set_Resolution(self, Resolution):
        self.Resolution = Resolution
    def get_CopiesToPrint(self):
        return self.CopiesToPrint
    def set_CopiesToPrint(self, CopiesToPrint):
        self.CopiesToPrint = CopiesToPrint
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
    def validate_CloseDocumentType(self, value):
        result = True
        # Validate type CloseDocumentType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['COD_REPORT', 'DETAILED_DELIVERY_MANIFEST', 'HAZARDOUS_MATERIALS_CERTIFICATION', 'MANIFEST', 'MULTIWEIGHT_REPORT', 'OP_950']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CloseDocumentType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
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
    def hasContent_(self):
        if (
            self.Type is not None or
            self.ShippingCycle is not None or
            self.ShippingDocumentDisposition is not None or
            self.AccessReference is not None or
            self.Resolution is not None or
            self.CopiesToPrint is not None or
            self.Parts
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CloseDocument', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CloseDocument')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CloseDocument':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CloseDocument')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CloseDocument', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CloseDocument'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CloseDocument', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sType>%s</%sType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Type), input_name='Type')), namespaceprefix_ , eol_))
        if self.ShippingCycle is not None:
            namespaceprefix_ = self.ShippingCycle_nsprefix_ + ':' if (UseCapturedNS_ and self.ShippingCycle_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShippingCycle>%s</%sShippingCycle>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShippingCycle), input_name='ShippingCycle')), namespaceprefix_ , eol_))
        if self.ShippingDocumentDisposition is not None:
            namespaceprefix_ = self.ShippingDocumentDisposition_nsprefix_ + ':' if (UseCapturedNS_ and self.ShippingDocumentDisposition_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShippingDocumentDisposition>%s</%sShippingDocumentDisposition>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShippingDocumentDisposition), input_name='ShippingDocumentDisposition')), namespaceprefix_ , eol_))
        if self.AccessReference is not None:
            namespaceprefix_ = self.AccessReference_nsprefix_ + ':' if (UseCapturedNS_ and self.AccessReference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccessReference>%s</%sAccessReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AccessReference), input_name='AccessReference')), namespaceprefix_ , eol_))
        if self.Resolution is not None:
            namespaceprefix_ = self.Resolution_nsprefix_ + ':' if (UseCapturedNS_ and self.Resolution_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sResolution>%s</%sResolution>%s' % (namespaceprefix_ , self.gds_format_integer(self.Resolution, input_name='Resolution'), namespaceprefix_ , eol_))
        if self.CopiesToPrint is not None:
            namespaceprefix_ = self.CopiesToPrint_nsprefix_ + ':' if (UseCapturedNS_ and self.CopiesToPrint_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCopiesToPrint>%s</%sCopiesToPrint>%s' % (namespaceprefix_ , self.gds_format_integer(self.CopiesToPrint, input_name='CopiesToPrint'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Type':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Type')
            value_ = self.gds_validate_string(value_, node, 'Type')
            self.Type = value_
            self.Type_nsprefix_ = child_.prefix
            # validate type CloseDocumentType
            self.validate_CloseDocumentType(self.Type)
        elif nodeName_ == 'ShippingCycle':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShippingCycle')
            value_ = self.gds_validate_string(value_, node, 'ShippingCycle')
            self.ShippingCycle = value_
            self.ShippingCycle_nsprefix_ = child_.prefix
        elif nodeName_ == 'ShippingDocumentDisposition':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShippingDocumentDisposition')
            value_ = self.gds_validate_string(value_, node, 'ShippingDocumentDisposition')
            self.ShippingDocumentDisposition = value_
            self.ShippingDocumentDisposition_nsprefix_ = child_.prefix
            # validate type ShippingDocumentDispositionType
            self.validate_ShippingDocumentDispositionType(self.ShippingDocumentDisposition)
        elif nodeName_ == 'AccessReference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AccessReference')
            value_ = self.gds_validate_string(value_, node, 'AccessReference')
            self.AccessReference = value_
            self.AccessReference_nsprefix_ = child_.prefix
        elif nodeName_ == 'Resolution' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Resolution')
            if ival_ < 0:
                raise_parse_error(child_, 'requires nonNegativeInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'Resolution')
            self.Resolution = ival_
            self.Resolution_nsprefix_ = child_.prefix
        elif nodeName_ == 'CopiesToPrint' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'CopiesToPrint')
            if ival_ < 0:
                raise_parse_error(child_, 'requires nonNegativeInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'CopiesToPrint')
            self.CopiesToPrint = ival_
            self.CopiesToPrint_nsprefix_ = child_.prefix
        elif nodeName_ == 'Parts':
            obj_ = ShippingDocumentPart.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Parts.append(obj_)
            obj_.original_tagname_ = 'Parts'
# end class CloseDocument


class CloseDocumentFormat(GeneratedsSuper):
    """Specifies characteristics of a close document to be produced."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Dispositions=None, TopOfPageOffset=None, ImageType=None, StockType=None, ProvideInstructions=None, Localization=None, gds_collector_=None, **kwargs_):
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
        self.Localization = Localization
        self.Localization_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CloseDocumentFormat)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CloseDocumentFormat.subclass:
            return CloseDocumentFormat.subclass(*args_, **kwargs_)
        else:
            return CloseDocumentFormat(*args_, **kwargs_)
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
    def get_Localization(self):
        return self.Localization
    def set_Localization(self, Localization):
        self.Localization = Localization
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
            self.Localization is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CloseDocumentFormat', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CloseDocumentFormat')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CloseDocumentFormat':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CloseDocumentFormat')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CloseDocumentFormat', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CloseDocumentFormat'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CloseDocumentFormat', fromsubclass_=False, pretty_print=True):
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
        elif nodeName_ == 'Localization':
            obj_ = Localization.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Localization = obj_
            obj_.original_tagname_ = 'Localization'
# end class CloseDocumentFormat


class CloseDocumentSpecification(GeneratedsSuper):
    """Contains all data required for close-time documents to be produced in
    conjunction with a specific set of shipments. For January 2010, there
    are no applicable options for the COD report, the Manifest, or the
    Multiweight Report (they will only be available in TEXT format). Detail
    specifications will be added for those report types when customer-
    selectable options are implemented."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CloseDocumentTypes=None, DetailedDeliveryManifestDetail=None, HazardousMaterialsCertificationDetail=None, ManifestDetail=None, Op950Detail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if CloseDocumentTypes is None:
            self.CloseDocumentTypes = []
        else:
            self.CloseDocumentTypes = CloseDocumentTypes
        self.CloseDocumentTypes_nsprefix_ = "ns"
        self.DetailedDeliveryManifestDetail = DetailedDeliveryManifestDetail
        self.DetailedDeliveryManifestDetail_nsprefix_ = "ns"
        self.HazardousMaterialsCertificationDetail = HazardousMaterialsCertificationDetail
        self.HazardousMaterialsCertificationDetail_nsprefix_ = "ns"
        self.ManifestDetail = ManifestDetail
        self.ManifestDetail_nsprefix_ = "ns"
        self.Op950Detail = Op950Detail
        self.Op950Detail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CloseDocumentSpecification)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CloseDocumentSpecification.subclass:
            return CloseDocumentSpecification.subclass(*args_, **kwargs_)
        else:
            return CloseDocumentSpecification(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CloseDocumentTypes(self):
        return self.CloseDocumentTypes
    def set_CloseDocumentTypes(self, CloseDocumentTypes):
        self.CloseDocumentTypes = CloseDocumentTypes
    def add_CloseDocumentTypes(self, value):
        self.CloseDocumentTypes.append(value)
    def insert_CloseDocumentTypes_at(self, index, value):
        self.CloseDocumentTypes.insert(index, value)
    def replace_CloseDocumentTypes_at(self, index, value):
        self.CloseDocumentTypes[index] = value
    def get_DetailedDeliveryManifestDetail(self):
        return self.DetailedDeliveryManifestDetail
    def set_DetailedDeliveryManifestDetail(self, DetailedDeliveryManifestDetail):
        self.DetailedDeliveryManifestDetail = DetailedDeliveryManifestDetail
    def get_HazardousMaterialsCertificationDetail(self):
        return self.HazardousMaterialsCertificationDetail
    def set_HazardousMaterialsCertificationDetail(self, HazardousMaterialsCertificationDetail):
        self.HazardousMaterialsCertificationDetail = HazardousMaterialsCertificationDetail
    def get_ManifestDetail(self):
        return self.ManifestDetail
    def set_ManifestDetail(self, ManifestDetail):
        self.ManifestDetail = ManifestDetail
    def get_Op950Detail(self):
        return self.Op950Detail
    def set_Op950Detail(self, Op950Detail):
        self.Op950Detail = Op950Detail
    def validate_CloseDocumentType(self, value):
        result = True
        # Validate type CloseDocumentType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['COD_REPORT', 'DETAILED_DELIVERY_MANIFEST', 'HAZARDOUS_MATERIALS_CERTIFICATION', 'MANIFEST', 'MULTIWEIGHT_REPORT', 'OP_950']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CloseDocumentType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.CloseDocumentTypes or
            self.DetailedDeliveryManifestDetail is not None or
            self.HazardousMaterialsCertificationDetail is not None or
            self.ManifestDetail is not None or
            self.Op950Detail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CloseDocumentSpecification', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CloseDocumentSpecification')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CloseDocumentSpecification':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CloseDocumentSpecification')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CloseDocumentSpecification', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CloseDocumentSpecification'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CloseDocumentSpecification', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for CloseDocumentTypes_ in self.CloseDocumentTypes:
            namespaceprefix_ = self.CloseDocumentTypes_nsprefix_ + ':' if (UseCapturedNS_ and self.CloseDocumentTypes_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCloseDocumentTypes>%s</%sCloseDocumentTypes>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CloseDocumentTypes_), input_name='CloseDocumentTypes')), namespaceprefix_ , eol_))
        if self.DetailedDeliveryManifestDetail is not None:
            namespaceprefix_ = self.DetailedDeliveryManifestDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.DetailedDeliveryManifestDetail_nsprefix_) else ''
            self.DetailedDeliveryManifestDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DetailedDeliveryManifestDetail', pretty_print=pretty_print)
        if self.HazardousMaterialsCertificationDetail is not None:
            namespaceprefix_ = self.HazardousMaterialsCertificationDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.HazardousMaterialsCertificationDetail_nsprefix_) else ''
            self.HazardousMaterialsCertificationDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='HazardousMaterialsCertificationDetail', pretty_print=pretty_print)
        if self.ManifestDetail is not None:
            namespaceprefix_ = self.ManifestDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ManifestDetail_nsprefix_) else ''
            self.ManifestDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ManifestDetail', pretty_print=pretty_print)
        if self.Op950Detail is not None:
            namespaceprefix_ = self.Op950Detail_nsprefix_ + ':' if (UseCapturedNS_ and self.Op950Detail_nsprefix_) else ''
            self.Op950Detail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Op950Detail', pretty_print=pretty_print)
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
        if nodeName_ == 'CloseDocumentTypes':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CloseDocumentTypes')
            value_ = self.gds_validate_string(value_, node, 'CloseDocumentTypes')
            self.CloseDocumentTypes.append(value_)
            self.CloseDocumentTypes_nsprefix_ = child_.prefix
            # validate type CloseDocumentType
            self.validate_CloseDocumentType(self.CloseDocumentTypes[-1])
        elif nodeName_ == 'DetailedDeliveryManifestDetail':
            obj_ = DetailedDeliveryManifestDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DetailedDeliveryManifestDetail = obj_
            obj_.original_tagname_ = 'DetailedDeliveryManifestDetail'
        elif nodeName_ == 'HazardousMaterialsCertificationDetail':
            obj_ = HazardousMaterialsCertificationDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.HazardousMaterialsCertificationDetail = obj_
            obj_.original_tagname_ = 'HazardousMaterialsCertificationDetail'
        elif nodeName_ == 'ManifestDetail':
            obj_ = ManifestDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ManifestDetail = obj_
            obj_.original_tagname_ = 'ManifestDetail'
        elif nodeName_ == 'Op950Detail':
            obj_ = Op950Detail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Op950Detail = obj_
            obj_.original_tagname_ = 'Op950Detail'
# end class CloseDocumentSpecification


class CloseManifestReferenceDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Type=None, Value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Type = Type
        self.validate_CustomerReferenceType(self.Type)
        self.Type_nsprefix_ = "ns"
        self.Value = Value
        self.Value_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CloseManifestReferenceDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CloseManifestReferenceDetail.subclass:
            return CloseManifestReferenceDetail.subclass(*args_, **kwargs_)
        else:
            return CloseManifestReferenceDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def validate_CustomerReferenceType(self, value):
        result = True
        # Validate type CustomerReferenceType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['BILL_OF_LADING', 'CUSTOMER_REFERENCE', 'DEPARTMENT_NUMBER', 'ELECTRONIC_PRODUCT_CODE', 'INTRACOUNTRY_REGULATORY_REFERENCE', 'INVOICE_NUMBER', 'PACKING_SLIP_NUMBER', 'P_O_NUMBER', 'RMA_ASSOCIATION', 'SHIPMENT_INTEGRITY', 'STORE_NUMBER']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CustomerReferenceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Type is not None or
            self.Value is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CloseManifestReferenceDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CloseManifestReferenceDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CloseManifestReferenceDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CloseManifestReferenceDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CloseManifestReferenceDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CloseManifestReferenceDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CloseManifestReferenceDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sType>%s</%sType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Type), input_name='Type')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Type':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Type')
            value_ = self.gds_validate_string(value_, node, 'Type')
            self.Type = value_
            self.Type_nsprefix_ = child_.prefix
            # validate type CustomerReferenceType
            self.validate_CustomerReferenceType(self.Type)
        elif nodeName_ == 'Value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Value')
            value_ = self.gds_validate_string(value_, node, 'Value')
            self.Value = value_
            self.Value_nsprefix_ = child_.prefix
# end class CloseManifestReferenceDetail


class CloseSmartPostDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HubId=None, CustomerId=None, CustomerManifestId=None, DestinationCountryCode=None, PickupCarrier=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.HubId = HubId
        self.HubId_nsprefix_ = None
        self.CustomerId = CustomerId
        self.CustomerId_nsprefix_ = None
        self.CustomerManifestId = CustomerManifestId
        self.CustomerManifestId_nsprefix_ = None
        self.DestinationCountryCode = DestinationCountryCode
        self.DestinationCountryCode_nsprefix_ = None
        self.PickupCarrier = PickupCarrier
        self.validate_CarrierCodeType(self.PickupCarrier)
        self.PickupCarrier_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CloseSmartPostDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CloseSmartPostDetail.subclass:
            return CloseSmartPostDetail.subclass(*args_, **kwargs_)
        else:
            return CloseSmartPostDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_HubId(self):
        return self.HubId
    def set_HubId(self, HubId):
        self.HubId = HubId
    def get_CustomerId(self):
        return self.CustomerId
    def set_CustomerId(self, CustomerId):
        self.CustomerId = CustomerId
    def get_CustomerManifestId(self):
        return self.CustomerManifestId
    def set_CustomerManifestId(self, CustomerManifestId):
        self.CustomerManifestId = CustomerManifestId
    def get_DestinationCountryCode(self):
        return self.DestinationCountryCode
    def set_DestinationCountryCode(self, DestinationCountryCode):
        self.DestinationCountryCode = DestinationCountryCode
    def get_PickupCarrier(self):
        return self.PickupCarrier
    def set_PickupCarrier(self, PickupCarrier):
        self.PickupCarrier = PickupCarrier
    def validate_CarrierCodeType(self, value):
        result = True
        # Validate type CarrierCodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FDXC', 'FDXE', 'FDXG', 'FXCC', 'FXFR', 'FXSP']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CarrierCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.HubId is not None or
            self.CustomerId is not None or
            self.CustomerManifestId is not None or
            self.DestinationCountryCode is not None or
            self.PickupCarrier is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CloseSmartPostDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CloseSmartPostDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CloseSmartPostDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CloseSmartPostDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CloseSmartPostDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CloseSmartPostDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CloseSmartPostDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.HubId is not None:
            namespaceprefix_ = self.HubId_nsprefix_ + ':' if (UseCapturedNS_ and self.HubId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHubId>%s</%sHubId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HubId), input_name='HubId')), namespaceprefix_ , eol_))
        if self.CustomerId is not None:
            namespaceprefix_ = self.CustomerId_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomerId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustomerId>%s</%sCustomerId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CustomerId), input_name='CustomerId')), namespaceprefix_ , eol_))
        if self.CustomerManifestId is not None:
            namespaceprefix_ = self.CustomerManifestId_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomerManifestId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustomerManifestId>%s</%sCustomerManifestId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CustomerManifestId), input_name='CustomerManifestId')), namespaceprefix_ , eol_))
        if self.DestinationCountryCode is not None:
            namespaceprefix_ = self.DestinationCountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationCountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDestinationCountryCode>%s</%sDestinationCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DestinationCountryCode), input_name='DestinationCountryCode')), namespaceprefix_ , eol_))
        if self.PickupCarrier is not None:
            namespaceprefix_ = self.PickupCarrier_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupCarrier_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupCarrier>%s</%sPickupCarrier>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupCarrier), input_name='PickupCarrier')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'HubId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HubId')
            value_ = self.gds_validate_string(value_, node, 'HubId')
            self.HubId = value_
            self.HubId_nsprefix_ = child_.prefix
        elif nodeName_ == 'CustomerId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CustomerId')
            value_ = self.gds_validate_string(value_, node, 'CustomerId')
            self.CustomerId = value_
            self.CustomerId_nsprefix_ = child_.prefix
        elif nodeName_ == 'CustomerManifestId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CustomerManifestId')
            value_ = self.gds_validate_string(value_, node, 'CustomerManifestId')
            self.CustomerManifestId = value_
            self.CustomerManifestId_nsprefix_ = child_.prefix
        elif nodeName_ == 'DestinationCountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DestinationCountryCode')
            value_ = self.gds_validate_string(value_, node, 'DestinationCountryCode')
            self.DestinationCountryCode = value_
            self.DestinationCountryCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'PickupCarrier':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupCarrier')
            value_ = self.gds_validate_string(value_, node, 'PickupCarrier')
            self.PickupCarrier = value_
            self.PickupCarrier_nsprefix_ = child_.prefix
            # validate type CarrierCodeType
            self.validate_CarrierCodeType(self.PickupCarrier)
# end class CloseSmartPostDetail


class CloseWithDocumentsProcessingOptionsRequested(GeneratedsSuper):
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
                CurrentSubclassModule_, CloseWithDocumentsProcessingOptionsRequested)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CloseWithDocumentsProcessingOptionsRequested.subclass:
            return CloseWithDocumentsProcessingOptionsRequested.subclass(*args_, **kwargs_)
        else:
            return CloseWithDocumentsProcessingOptionsRequested(*args_, **kwargs_)
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
    def validate_CloseWithDocumentsProcessingOptionType(self, value):
        result = True
        # Validate type CloseWithDocumentsProcessingOptionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ERROR_IF_OPEN_SHIPMENTS_FOUND', 'WARNING_IF_OPEN_SHIPMENTS_FOUND']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CloseWithDocumentsProcessingOptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Options
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CloseWithDocumentsProcessingOptionsRequested', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CloseWithDocumentsProcessingOptionsRequested')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CloseWithDocumentsProcessingOptionsRequested':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CloseWithDocumentsProcessingOptionsRequested')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CloseWithDocumentsProcessingOptionsRequested', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CloseWithDocumentsProcessingOptionsRequested'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CloseWithDocumentsProcessingOptionsRequested', fromsubclass_=False, pretty_print=True):
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
            # validate type CloseWithDocumentsProcessingOptionType
            self.validate_CloseWithDocumentsProcessingOptionType(self.Options[-1])
# end class CloseWithDocumentsProcessingOptionsRequested


class CloseWithDocumentsReply(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, Documents=None, gds_collector_=None, **kwargs_):
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
        if Documents is None:
            self.Documents = []
        else:
            self.Documents = Documents
        self.Documents_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CloseWithDocumentsReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CloseWithDocumentsReply.subclass:
            return CloseWithDocumentsReply.subclass(*args_, **kwargs_)
        else:
            return CloseWithDocumentsReply(*args_, **kwargs_)
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
    def get_Documents(self):
        return self.Documents
    def set_Documents(self, Documents):
        self.Documents = Documents
    def add_Documents(self, value):
        self.Documents.append(value)
    def insert_Documents_at(self, index, value):
        self.Documents.insert(index, value)
    def replace_Documents_at(self, index, value):
        self.Documents[index] = value
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
            self.Documents
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CloseWithDocumentsReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CloseWithDocumentsReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CloseWithDocumentsReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CloseWithDocumentsReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CloseWithDocumentsReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CloseWithDocumentsReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CloseWithDocumentsReply', fromsubclass_=False, pretty_print=True):
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
        for Documents_ in self.Documents:
            namespaceprefix_ = self.Documents_nsprefix_ + ':' if (UseCapturedNS_ and self.Documents_nsprefix_) else ''
            Documents_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Documents', pretty_print=pretty_print)
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
        elif nodeName_ == 'Documents':
            obj_ = CloseDocument.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Documents.append(obj_)
            obj_.original_tagname_ = 'Documents'
# end class CloseWithDocumentsReply


class CloseWithDocumentsRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, TransactionDetail=None, Version=None, ActionType=None, ProcessingOptions=None, CarrierCode=None, ShippingCycle=None, ReprintCloseDate=None, ManifestReferenceDetail=None, SmartPostDetail=None, CloseDocumentSpecification=None, gds_collector_=None, **kwargs_):
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
        self.ActionType = ActionType
        self.validate_CloseActionType(self.ActionType)
        self.ActionType_nsprefix_ = "ns"
        self.ProcessingOptions = ProcessingOptions
        self.ProcessingOptions_nsprefix_ = "ns"
        self.CarrierCode = CarrierCode
        self.validate_CarrierCodeType(self.CarrierCode)
        self.CarrierCode_nsprefix_ = "ns"
        self.ShippingCycle = ShippingCycle
        self.ShippingCycle_nsprefix_ = None
        if isinstance(ReprintCloseDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ReprintCloseDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = ReprintCloseDate
        self.ReprintCloseDate = initvalue_
        self.ReprintCloseDate_nsprefix_ = None
        self.ManifestReferenceDetail = ManifestReferenceDetail
        self.ManifestReferenceDetail_nsprefix_ = "ns"
        self.SmartPostDetail = SmartPostDetail
        self.SmartPostDetail_nsprefix_ = "ns"
        self.CloseDocumentSpecification = CloseDocumentSpecification
        self.CloseDocumentSpecification_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CloseWithDocumentsRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CloseWithDocumentsRequest.subclass:
            return CloseWithDocumentsRequest.subclass(*args_, **kwargs_)
        else:
            return CloseWithDocumentsRequest(*args_, **kwargs_)
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
    def get_ActionType(self):
        return self.ActionType
    def set_ActionType(self, ActionType):
        self.ActionType = ActionType
    def get_ProcessingOptions(self):
        return self.ProcessingOptions
    def set_ProcessingOptions(self, ProcessingOptions):
        self.ProcessingOptions = ProcessingOptions
    def get_CarrierCode(self):
        return self.CarrierCode
    def set_CarrierCode(self, CarrierCode):
        self.CarrierCode = CarrierCode
    def get_ShippingCycle(self):
        return self.ShippingCycle
    def set_ShippingCycle(self, ShippingCycle):
        self.ShippingCycle = ShippingCycle
    def get_ReprintCloseDate(self):
        return self.ReprintCloseDate
    def set_ReprintCloseDate(self, ReprintCloseDate):
        self.ReprintCloseDate = ReprintCloseDate
    def get_ManifestReferenceDetail(self):
        return self.ManifestReferenceDetail
    def set_ManifestReferenceDetail(self, ManifestReferenceDetail):
        self.ManifestReferenceDetail = ManifestReferenceDetail
    def get_SmartPostDetail(self):
        return self.SmartPostDetail
    def set_SmartPostDetail(self, SmartPostDetail):
        self.SmartPostDetail = SmartPostDetail
    def get_CloseDocumentSpecification(self):
        return self.CloseDocumentSpecification
    def set_CloseDocumentSpecification(self, CloseDocumentSpecification):
        self.CloseDocumentSpecification = CloseDocumentSpecification
    def validate_CloseActionType(self, value):
        result = True
        # Validate type CloseActionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['CLOSE', 'PREVIEW_CLOSE_DOCUMENTS', 'REPRINT_CLOSE_DOCUMENTS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CloseActionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
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
            enumerations = ['FDXC', 'FDXE', 'FDXG', 'FXCC', 'FXFR', 'FXSP']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CarrierCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.ActionType is not None or
            self.ProcessingOptions is not None or
            self.CarrierCode is not None or
            self.ShippingCycle is not None or
            self.ReprintCloseDate is not None or
            self.ManifestReferenceDetail is not None or
            self.SmartPostDetail is not None or
            self.CloseDocumentSpecification is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CloseWithDocumentsRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CloseWithDocumentsRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CloseWithDocumentsRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CloseWithDocumentsRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CloseWithDocumentsRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CloseWithDocumentsRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CloseWithDocumentsRequest', fromsubclass_=False, pretty_print=True):
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
        if self.ActionType is not None:
            namespaceprefix_ = self.ActionType_nsprefix_ + ':' if (UseCapturedNS_ and self.ActionType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sActionType>%s</%sActionType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ActionType), input_name='ActionType')), namespaceprefix_ , eol_))
        if self.ProcessingOptions is not None:
            namespaceprefix_ = self.ProcessingOptions_nsprefix_ + ':' if (UseCapturedNS_ and self.ProcessingOptions_nsprefix_) else ''
            self.ProcessingOptions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ProcessingOptions', pretty_print=pretty_print)
        if self.CarrierCode is not None:
            namespaceprefix_ = self.CarrierCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CarrierCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCarrierCode>%s</%sCarrierCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CarrierCode), input_name='CarrierCode')), namespaceprefix_ , eol_))
        if self.ShippingCycle is not None:
            namespaceprefix_ = self.ShippingCycle_nsprefix_ + ':' if (UseCapturedNS_ and self.ShippingCycle_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShippingCycle>%s</%sShippingCycle>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShippingCycle), input_name='ShippingCycle')), namespaceprefix_ , eol_))
        if self.ReprintCloseDate is not None:
            namespaceprefix_ = self.ReprintCloseDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ReprintCloseDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReprintCloseDate>%s</%sReprintCloseDate>%s' % (namespaceprefix_ , self.gds_format_datetime(self.ReprintCloseDate, input_name='ReprintCloseDate'), namespaceprefix_ , eol_))
        if self.ManifestReferenceDetail is not None:
            namespaceprefix_ = self.ManifestReferenceDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ManifestReferenceDetail_nsprefix_) else ''
            self.ManifestReferenceDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ManifestReferenceDetail', pretty_print=pretty_print)
        if self.SmartPostDetail is not None:
            namespaceprefix_ = self.SmartPostDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.SmartPostDetail_nsprefix_) else ''
            self.SmartPostDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='SmartPostDetail', pretty_print=pretty_print)
        if self.CloseDocumentSpecification is not None:
            namespaceprefix_ = self.CloseDocumentSpecification_nsprefix_ + ':' if (UseCapturedNS_ and self.CloseDocumentSpecification_nsprefix_) else ''
            self.CloseDocumentSpecification.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CloseDocumentSpecification', pretty_print=pretty_print)
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
        elif nodeName_ == 'ActionType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ActionType')
            value_ = self.gds_validate_string(value_, node, 'ActionType')
            self.ActionType = value_
            self.ActionType_nsprefix_ = child_.prefix
            # validate type CloseActionType
            self.validate_CloseActionType(self.ActionType)
        elif nodeName_ == 'ProcessingOptions':
            obj_ = CloseWithDocumentsProcessingOptionsRequested.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ProcessingOptions = obj_
            obj_.original_tagname_ = 'ProcessingOptions'
        elif nodeName_ == 'CarrierCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CarrierCode')
            value_ = self.gds_validate_string(value_, node, 'CarrierCode')
            self.CarrierCode = value_
            self.CarrierCode_nsprefix_ = child_.prefix
            # validate type CarrierCodeType
            self.validate_CarrierCodeType(self.CarrierCode)
        elif nodeName_ == 'ShippingCycle':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShippingCycle')
            value_ = self.gds_validate_string(value_, node, 'ShippingCycle')
            self.ShippingCycle = value_
            self.ShippingCycle_nsprefix_ = child_.prefix
        elif nodeName_ == 'ReprintCloseDate':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.ReprintCloseDate = dval_
            self.ReprintCloseDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'ManifestReferenceDetail':
            obj_ = CloseManifestReferenceDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ManifestReferenceDetail = obj_
            obj_.original_tagname_ = 'ManifestReferenceDetail'
        elif nodeName_ == 'SmartPostDetail':
            obj_ = CloseSmartPostDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SmartPostDetail = obj_
            obj_.original_tagname_ = 'SmartPostDetail'
        elif nodeName_ == 'CloseDocumentSpecification':
            obj_ = CloseDocumentSpecification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CloseDocumentSpecification = obj_
            obj_.original_tagname_ = 'CloseDocumentSpecification'
# end class CloseWithDocumentsRequest


class CustomerImageUsage(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Type=None, Id=None, InternalId=None, InternalImageType=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Type = Type
        self.validate_CustomerImageUsageType(self.Type)
        self.Type_nsprefix_ = "ns"
        self.Id = Id
        self.validate_ImageId(self.Id)
        self.Id_nsprefix_ = "ns"
        self.InternalId = InternalId
        self.InternalId_nsprefix_ = None
        self.InternalImageType = InternalImageType
        self.validate_InternalImageType(self.InternalImageType)
        self.InternalImageType_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CustomerImageUsage)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CustomerImageUsage.subclass:
            return CustomerImageUsage.subclass(*args_, **kwargs_)
        else:
            return CustomerImageUsage(*args_, **kwargs_)
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
    def get_InternalId(self):
        return self.InternalId
    def set_InternalId(self, InternalId):
        self.InternalId = InternalId
    def get_InternalImageType(self):
        return self.InternalImageType
    def set_InternalImageType(self, InternalImageType):
        self.InternalImageType = InternalImageType
    def validate_CustomerImageUsageType(self, value):
        result = True
        # Validate type CustomerImageUsageType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['LETTER_HEAD', 'SIGNATURE']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CustomerImageUsageType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ImageId(self, value):
        result = True
        # Validate type ImageId, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['IMAGE_1', 'IMAGE_2', 'IMAGE_3', 'IMAGE_4', 'IMAGE_5']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ImageId' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_InternalImageType(self, value):
        result = True
        # Validate type InternalImageType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['LETTER_HEAD', 'SIGNATURE']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on InternalImageType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Type is not None or
            self.Id is not None or
            self.InternalId is not None or
            self.InternalImageType is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CustomerImageUsage', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CustomerImageUsage')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CustomerImageUsage':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CustomerImageUsage')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CustomerImageUsage', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CustomerImageUsage'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CustomerImageUsage', fromsubclass_=False, pretty_print=True):
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
        if self.InternalId is not None:
            namespaceprefix_ = self.InternalId_nsprefix_ + ':' if (UseCapturedNS_ and self.InternalId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sInternalId>%s</%sInternalId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.InternalId), input_name='InternalId')), namespaceprefix_ , eol_))
        if self.InternalImageType is not None:
            namespaceprefix_ = self.InternalImageType_nsprefix_ + ':' if (UseCapturedNS_ and self.InternalImageType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sInternalImageType>%s</%sInternalImageType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.InternalImageType), input_name='InternalImageType')), namespaceprefix_ , eol_))
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
            # validate type CustomerImageUsageType
            self.validate_CustomerImageUsageType(self.Type)
        elif nodeName_ == 'Id':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Id')
            value_ = self.gds_validate_string(value_, node, 'Id')
            self.Id = value_
            self.Id_nsprefix_ = child_.prefix
            # validate type ImageId
            self.validate_ImageId(self.Id)
        elif nodeName_ == 'InternalId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'InternalId')
            value_ = self.gds_validate_string(value_, node, 'InternalId')
            self.InternalId = value_
            self.InternalId_nsprefix_ = child_.prefix
        elif nodeName_ == 'InternalImageType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'InternalImageType')
            value_ = self.gds_validate_string(value_, node, 'InternalImageType')
            self.InternalImageType = value_
            self.InternalImageType_nsprefix_ = child_.prefix
            # validate type InternalImageType
            self.validate_InternalImageType(self.InternalImageType)
# end class CustomerImageUsage


class DetailedDeliveryManifestDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Format=None, ClientTimeZoneOffset=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Format = Format
        self.Format_nsprefix_ = "ns"
        self.ClientTimeZoneOffset = ClientTimeZoneOffset
        self.ClientTimeZoneOffset_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DetailedDeliveryManifestDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DetailedDeliveryManifestDetail.subclass:
            return DetailedDeliveryManifestDetail.subclass(*args_, **kwargs_)
        else:
            return DetailedDeliveryManifestDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Format(self):
        return self.Format
    def set_Format(self, Format):
        self.Format = Format
    def get_ClientTimeZoneOffset(self):
        return self.ClientTimeZoneOffset
    def set_ClientTimeZoneOffset(self, ClientTimeZoneOffset):
        self.ClientTimeZoneOffset = ClientTimeZoneOffset
    def hasContent_(self):
        if (
            self.Format is not None or
            self.ClientTimeZoneOffset is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DetailedDeliveryManifestDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DetailedDeliveryManifestDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DetailedDeliveryManifestDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DetailedDeliveryManifestDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DetailedDeliveryManifestDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DetailedDeliveryManifestDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DetailedDeliveryManifestDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Format is not None:
            namespaceprefix_ = self.Format_nsprefix_ + ':' if (UseCapturedNS_ and self.Format_nsprefix_) else ''
            self.Format.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Format', pretty_print=pretty_print)
        if self.ClientTimeZoneOffset is not None:
            namespaceprefix_ = self.ClientTimeZoneOffset_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientTimeZoneOffset_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sClientTimeZoneOffset>%s</%sClientTimeZoneOffset>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ClientTimeZoneOffset), input_name='ClientTimeZoneOffset')), namespaceprefix_ , eol_))
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
            obj_ = CloseDocumentFormat.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Format = obj_
            obj_.original_tagname_ = 'Format'
        elif nodeName_ == 'ClientTimeZoneOffset':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ClientTimeZoneOffset')
            value_ = self.gds_validate_string(value_, node, 'ClientTimeZoneOffset')
            self.ClientTimeZoneOffset = value_
            self.ClientTimeZoneOffset_nsprefix_ = child_.prefix
# end class DetailedDeliveryManifestDetail


class GroundCloseDocumentsReply(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, CloseDocuments=None, gds_collector_=None, **kwargs_):
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
        if CloseDocuments is None:
            self.CloseDocuments = []
        else:
            self.CloseDocuments = CloseDocuments
        self.CloseDocuments_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GroundCloseDocumentsReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GroundCloseDocumentsReply.subclass:
            return GroundCloseDocumentsReply.subclass(*args_, **kwargs_)
        else:
            return GroundCloseDocumentsReply(*args_, **kwargs_)
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
    def get_CloseDocuments(self):
        return self.CloseDocuments
    def set_CloseDocuments(self, CloseDocuments):
        self.CloseDocuments = CloseDocuments
    def add_CloseDocuments(self, value):
        self.CloseDocuments.append(value)
    def insert_CloseDocuments_at(self, index, value):
        self.CloseDocuments.insert(index, value)
    def replace_CloseDocuments_at(self, index, value):
        self.CloseDocuments[index] = value
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
            self.CloseDocuments
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GroundCloseDocumentsReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GroundCloseDocumentsReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GroundCloseDocumentsReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GroundCloseDocumentsReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GroundCloseDocumentsReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GroundCloseDocumentsReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GroundCloseDocumentsReply', fromsubclass_=False, pretty_print=True):
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
        for CloseDocuments_ in self.CloseDocuments:
            namespaceprefix_ = self.CloseDocuments_nsprefix_ + ':' if (UseCapturedNS_ and self.CloseDocuments_nsprefix_) else ''
            CloseDocuments_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CloseDocuments', pretty_print=pretty_print)
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
        elif nodeName_ == 'CloseDocuments':
            obj_ = CloseDocument.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CloseDocuments.append(obj_)
            obj_.original_tagname_ = 'CloseDocuments'
# end class GroundCloseDocumentsReply


class GroundCloseReply(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, CodReport=None, HazMatCertificate=None, Manifest=None, MultiweightReport=None, gds_collector_=None, **kwargs_):
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
        self.CodReport = CodReport
        self.CodReport_nsprefix_ = None
        self.HazMatCertificate = HazMatCertificate
        self.HazMatCertificate_nsprefix_ = None
        self.Manifest = Manifest
        self.Manifest_nsprefix_ = "ns"
        self.MultiweightReport = MultiweightReport
        self.MultiweightReport_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GroundCloseReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GroundCloseReply.subclass:
            return GroundCloseReply.subclass(*args_, **kwargs_)
        else:
            return GroundCloseReply(*args_, **kwargs_)
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
    def get_CodReport(self):
        return self.CodReport
    def set_CodReport(self, CodReport):
        self.CodReport = CodReport
    def get_HazMatCertificate(self):
        return self.HazMatCertificate
    def set_HazMatCertificate(self, HazMatCertificate):
        self.HazMatCertificate = HazMatCertificate
    def get_Manifest(self):
        return self.Manifest
    def set_Manifest(self, Manifest):
        self.Manifest = Manifest
    def get_MultiweightReport(self):
        return self.MultiweightReport
    def set_MultiweightReport(self, MultiweightReport):
        self.MultiweightReport = MultiweightReport
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
            self.CodReport is not None or
            self.HazMatCertificate is not None or
            self.Manifest is not None or
            self.MultiweightReport is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GroundCloseReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GroundCloseReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GroundCloseReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GroundCloseReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GroundCloseReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GroundCloseReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GroundCloseReply', fromsubclass_=False, pretty_print=True):
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
        if self.CodReport is not None:
            namespaceprefix_ = self.CodReport_nsprefix_ + ':' if (UseCapturedNS_ and self.CodReport_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodReport>%s</%sCodReport>%s' % (namespaceprefix_ , self.gds_format_base64(self.CodReport, input_name='CodReport'), namespaceprefix_ , eol_))
        if self.HazMatCertificate is not None:
            namespaceprefix_ = self.HazMatCertificate_nsprefix_ + ':' if (UseCapturedNS_ and self.HazMatCertificate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHazMatCertificate>%s</%sHazMatCertificate>%s' % (namespaceprefix_ , self.gds_format_base64(self.HazMatCertificate, input_name='HazMatCertificate'), namespaceprefix_ , eol_))
        if self.Manifest is not None:
            namespaceprefix_ = self.Manifest_nsprefix_ + ':' if (UseCapturedNS_ and self.Manifest_nsprefix_) else ''
            self.Manifest.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Manifest', pretty_print=pretty_print)
        if self.MultiweightReport is not None:
            namespaceprefix_ = self.MultiweightReport_nsprefix_ + ':' if (UseCapturedNS_ and self.MultiweightReport_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMultiweightReport>%s</%sMultiweightReport>%s' % (namespaceprefix_ , self.gds_format_base64(self.MultiweightReport, input_name='MultiweightReport'), namespaceprefix_ , eol_))
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
        elif nodeName_ == 'CodReport':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'CodReport')
            else:
                bval_ = None
            self.CodReport = bval_
            self.CodReport_nsprefix_ = child_.prefix
        elif nodeName_ == 'HazMatCertificate':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'HazMatCertificate')
            else:
                bval_ = None
            self.HazMatCertificate = bval_
            self.HazMatCertificate_nsprefix_ = child_.prefix
        elif nodeName_ == 'Manifest':
            obj_ = ManifestFile.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Manifest = obj_
            obj_.original_tagname_ = 'Manifest'
        elif nodeName_ == 'MultiweightReport':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'MultiweightReport')
            else:
                bval_ = None
            self.MultiweightReport = bval_
            self.MultiweightReport_nsprefix_ = child_.prefix
# end class GroundCloseReply


class GroundCloseReportsReprintReply(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, CodReport=None, HazMatCertificate=None, Manifests=None, gds_collector_=None, **kwargs_):
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
        self.CodReport = CodReport
        self.CodReport_nsprefix_ = None
        self.HazMatCertificate = HazMatCertificate
        self.HazMatCertificate_nsprefix_ = None
        if Manifests is None:
            self.Manifests = []
        else:
            self.Manifests = Manifests
        self.Manifests_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GroundCloseReportsReprintReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GroundCloseReportsReprintReply.subclass:
            return GroundCloseReportsReprintReply.subclass(*args_, **kwargs_)
        else:
            return GroundCloseReportsReprintReply(*args_, **kwargs_)
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
    def get_CodReport(self):
        return self.CodReport
    def set_CodReport(self, CodReport):
        self.CodReport = CodReport
    def get_HazMatCertificate(self):
        return self.HazMatCertificate
    def set_HazMatCertificate(self, HazMatCertificate):
        self.HazMatCertificate = HazMatCertificate
    def get_Manifests(self):
        return self.Manifests
    def set_Manifests(self, Manifests):
        self.Manifests = Manifests
    def add_Manifests(self, value):
        self.Manifests.append(value)
    def insert_Manifests_at(self, index, value):
        self.Manifests.insert(index, value)
    def replace_Manifests_at(self, index, value):
        self.Manifests[index] = value
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
            self.CodReport is not None or
            self.HazMatCertificate is not None or
            self.Manifests
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GroundCloseReportsReprintReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GroundCloseReportsReprintReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GroundCloseReportsReprintReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GroundCloseReportsReprintReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GroundCloseReportsReprintReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GroundCloseReportsReprintReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GroundCloseReportsReprintReply', fromsubclass_=False, pretty_print=True):
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
        if self.CodReport is not None:
            namespaceprefix_ = self.CodReport_nsprefix_ + ':' if (UseCapturedNS_ and self.CodReport_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodReport>%s</%sCodReport>%s' % (namespaceprefix_ , self.gds_format_base64(self.CodReport, input_name='CodReport'), namespaceprefix_ , eol_))
        if self.HazMatCertificate is not None:
            namespaceprefix_ = self.HazMatCertificate_nsprefix_ + ':' if (UseCapturedNS_ and self.HazMatCertificate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHazMatCertificate>%s</%sHazMatCertificate>%s' % (namespaceprefix_ , self.gds_format_base64(self.HazMatCertificate, input_name='HazMatCertificate'), namespaceprefix_ , eol_))
        for Manifests_ in self.Manifests:
            namespaceprefix_ = self.Manifests_nsprefix_ + ':' if (UseCapturedNS_ and self.Manifests_nsprefix_) else ''
            Manifests_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Manifests', pretty_print=pretty_print)
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
        elif nodeName_ == 'CodReport':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'CodReport')
            else:
                bval_ = None
            self.CodReport = bval_
            self.CodReport_nsprefix_ = child_.prefix
        elif nodeName_ == 'HazMatCertificate':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'HazMatCertificate')
            else:
                bval_ = None
            self.HazMatCertificate = bval_
            self.HazMatCertificate_nsprefix_ = child_.prefix
        elif nodeName_ == 'Manifests':
            obj_ = ManifestFile.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Manifests.append(obj_)
            obj_.original_tagname_ = 'Manifests'
# end class GroundCloseReportsReprintReply


class GroundCloseReportsReprintRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, TransactionDetail=None, Version=None, ReportDate=None, TrackingNumber=None, CloseReportType=None, gds_collector_=None, **kwargs_):
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
        if isinstance(ReportDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ReportDate, '%Y-%m-%d').date()
        else:
            initvalue_ = ReportDate
        self.ReportDate = initvalue_
        self.ReportDate_nsprefix_ = None
        self.TrackingNumber = TrackingNumber
        self.TrackingNumber_nsprefix_ = None
        self.CloseReportType = CloseReportType
        self.validate_CloseReportType(self.CloseReportType)
        self.CloseReportType_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GroundCloseReportsReprintRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GroundCloseReportsReprintRequest.subclass:
            return GroundCloseReportsReprintRequest.subclass(*args_, **kwargs_)
        else:
            return GroundCloseReportsReprintRequest(*args_, **kwargs_)
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
    def get_ReportDate(self):
        return self.ReportDate
    def set_ReportDate(self, ReportDate):
        self.ReportDate = ReportDate
    def get_TrackingNumber(self):
        return self.TrackingNumber
    def set_TrackingNumber(self, TrackingNumber):
        self.TrackingNumber = TrackingNumber
    def get_CloseReportType(self):
        return self.CloseReportType
    def set_CloseReportType(self, CloseReportType):
        self.CloseReportType = CloseReportType
    def validate_CloseReportType(self, value):
        result = True
        # Validate type CloseReportType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ALL', 'COD', 'HAZMAT', 'MANIFEST', 'MULTIWEIGHT']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CloseReportType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.ReportDate is not None or
            self.TrackingNumber is not None or
            self.CloseReportType is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GroundCloseReportsReprintRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GroundCloseReportsReprintRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GroundCloseReportsReprintRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GroundCloseReportsReprintRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GroundCloseReportsReprintRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GroundCloseReportsReprintRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GroundCloseReportsReprintRequest', fromsubclass_=False, pretty_print=True):
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
        if self.ReportDate is not None:
            namespaceprefix_ = self.ReportDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ReportDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReportDate>%s</%sReportDate>%s' % (namespaceprefix_ , self.gds_format_date(self.ReportDate, input_name='ReportDate'), namespaceprefix_ , eol_))
        if self.TrackingNumber is not None:
            namespaceprefix_ = self.TrackingNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackingNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTrackingNumber>%s</%sTrackingNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TrackingNumber), input_name='TrackingNumber')), namespaceprefix_ , eol_))
        if self.CloseReportType is not None:
            namespaceprefix_ = self.CloseReportType_nsprefix_ + ':' if (UseCapturedNS_ and self.CloseReportType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCloseReportType>%s</%sCloseReportType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CloseReportType), input_name='CloseReportType')), namespaceprefix_ , eol_))
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
        elif nodeName_ == 'ReportDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.ReportDate = dval_
            self.ReportDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'TrackingNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TrackingNumber')
            value_ = self.gds_validate_string(value_, node, 'TrackingNumber')
            self.TrackingNumber = value_
            self.TrackingNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'CloseReportType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CloseReportType')
            value_ = self.gds_validate_string(value_, node, 'CloseReportType')
            self.CloseReportType = value_
            self.CloseReportType_nsprefix_ = child_.prefix
            # validate type CloseReportType
            self.validate_CloseReportType(self.CloseReportType)
# end class GroundCloseReportsReprintRequest


class GroundCloseRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, TransactionDetail=None, Version=None, CloseGrouping=None, TimeUpToWhichShipmentsAreToBeClosed=None, ManifestReferenceDetail=None, gds_collector_=None, **kwargs_):
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
        self.CloseGrouping = CloseGrouping
        self.validate_CloseGroupingType(self.CloseGrouping)
        self.CloseGrouping_nsprefix_ = "ns"
        if isinstance(TimeUpToWhichShipmentsAreToBeClosed, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(TimeUpToWhichShipmentsAreToBeClosed, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = TimeUpToWhichShipmentsAreToBeClosed
        self.TimeUpToWhichShipmentsAreToBeClosed = initvalue_
        self.TimeUpToWhichShipmentsAreToBeClosed_nsprefix_ = None
        self.ManifestReferenceDetail = ManifestReferenceDetail
        self.ManifestReferenceDetail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GroundCloseRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GroundCloseRequest.subclass:
            return GroundCloseRequest.subclass(*args_, **kwargs_)
        else:
            return GroundCloseRequest(*args_, **kwargs_)
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
    def get_CloseGrouping(self):
        return self.CloseGrouping
    def set_CloseGrouping(self, CloseGrouping):
        self.CloseGrouping = CloseGrouping
    def get_TimeUpToWhichShipmentsAreToBeClosed(self):
        return self.TimeUpToWhichShipmentsAreToBeClosed
    def set_TimeUpToWhichShipmentsAreToBeClosed(self, TimeUpToWhichShipmentsAreToBeClosed):
        self.TimeUpToWhichShipmentsAreToBeClosed = TimeUpToWhichShipmentsAreToBeClosed
    def get_ManifestReferenceDetail(self):
        return self.ManifestReferenceDetail
    def set_ManifestReferenceDetail(self, ManifestReferenceDetail):
        self.ManifestReferenceDetail = ManifestReferenceDetail
    def validate_CloseGroupingType(self, value):
        result = True
        # Validate type CloseGroupingType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['MANIFEST_REFERENCE', 'SHIPPING_CYCLE', 'TIME']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CloseGroupingType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.CloseGrouping is not None or
            self.TimeUpToWhichShipmentsAreToBeClosed is not None or
            self.ManifestReferenceDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GroundCloseRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GroundCloseRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GroundCloseRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GroundCloseRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GroundCloseRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GroundCloseRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GroundCloseRequest', fromsubclass_=False, pretty_print=True):
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
        if self.CloseGrouping is not None:
            namespaceprefix_ = self.CloseGrouping_nsprefix_ + ':' if (UseCapturedNS_ and self.CloseGrouping_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCloseGrouping>%s</%sCloseGrouping>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CloseGrouping), input_name='CloseGrouping')), namespaceprefix_ , eol_))
        if self.TimeUpToWhichShipmentsAreToBeClosed is not None:
            namespaceprefix_ = self.TimeUpToWhichShipmentsAreToBeClosed_nsprefix_ + ':' if (UseCapturedNS_ and self.TimeUpToWhichShipmentsAreToBeClosed_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTimeUpToWhichShipmentsAreToBeClosed>%s</%sTimeUpToWhichShipmentsAreToBeClosed>%s' % (namespaceprefix_ , self.gds_format_datetime(self.TimeUpToWhichShipmentsAreToBeClosed, input_name='TimeUpToWhichShipmentsAreToBeClosed'), namespaceprefix_ , eol_))
        if self.ManifestReferenceDetail is not None:
            namespaceprefix_ = self.ManifestReferenceDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ManifestReferenceDetail_nsprefix_) else ''
            self.ManifestReferenceDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ManifestReferenceDetail', pretty_print=pretty_print)
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
        elif nodeName_ == 'CloseGrouping':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CloseGrouping')
            value_ = self.gds_validate_string(value_, node, 'CloseGrouping')
            self.CloseGrouping = value_
            self.CloseGrouping_nsprefix_ = child_.prefix
            # validate type CloseGroupingType
            self.validate_CloseGroupingType(self.CloseGrouping)
        elif nodeName_ == 'TimeUpToWhichShipmentsAreToBeClosed':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.TimeUpToWhichShipmentsAreToBeClosed = dval_
            self.TimeUpToWhichShipmentsAreToBeClosed_nsprefix_ = child_.prefix
        elif nodeName_ == 'ManifestReferenceDetail':
            obj_ = CloseManifestReferenceDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ManifestReferenceDetail = obj_
            obj_.original_tagname_ = 'ManifestReferenceDetail'
# end class GroundCloseRequest


class GroundCloseWithDocumentsRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, TransactionDetail=None, Version=None, CloseDate=None, CloseDocumentSpecification=None, gds_collector_=None, **kwargs_):
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
        if isinstance(CloseDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(CloseDate, '%Y-%m-%d').date()
        else:
            initvalue_ = CloseDate
        self.CloseDate = initvalue_
        self.CloseDate_nsprefix_ = None
        self.CloseDocumentSpecification = CloseDocumentSpecification
        self.CloseDocumentSpecification_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GroundCloseWithDocumentsRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GroundCloseWithDocumentsRequest.subclass:
            return GroundCloseWithDocumentsRequest.subclass(*args_, **kwargs_)
        else:
            return GroundCloseWithDocumentsRequest(*args_, **kwargs_)
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
    def get_CloseDate(self):
        return self.CloseDate
    def set_CloseDate(self, CloseDate):
        self.CloseDate = CloseDate
    def get_CloseDocumentSpecification(self):
        return self.CloseDocumentSpecification
    def set_CloseDocumentSpecification(self, CloseDocumentSpecification):
        self.CloseDocumentSpecification = CloseDocumentSpecification
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.CloseDate is not None or
            self.CloseDocumentSpecification is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GroundCloseWithDocumentsRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GroundCloseWithDocumentsRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GroundCloseWithDocumentsRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GroundCloseWithDocumentsRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GroundCloseWithDocumentsRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GroundCloseWithDocumentsRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GroundCloseWithDocumentsRequest', fromsubclass_=False, pretty_print=True):
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
        if self.CloseDate is not None:
            namespaceprefix_ = self.CloseDate_nsprefix_ + ':' if (UseCapturedNS_ and self.CloseDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCloseDate>%s</%sCloseDate>%s' % (namespaceprefix_ , self.gds_format_date(self.CloseDate, input_name='CloseDate'), namespaceprefix_ , eol_))
        if self.CloseDocumentSpecification is not None:
            namespaceprefix_ = self.CloseDocumentSpecification_nsprefix_ + ':' if (UseCapturedNS_ and self.CloseDocumentSpecification_nsprefix_) else ''
            self.CloseDocumentSpecification.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CloseDocumentSpecification', pretty_print=pretty_print)
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
        elif nodeName_ == 'CloseDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.CloseDate = dval_
            self.CloseDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'CloseDocumentSpecification':
            obj_ = CloseDocumentSpecification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CloseDocumentSpecification = obj_
            obj_.original_tagname_ = 'CloseDocumentSpecification'
# end class GroundCloseWithDocumentsRequest


class HazardousMaterialsCertificationDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Format=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Format = Format
        self.Format_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, HazardousMaterialsCertificationDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if HazardousMaterialsCertificationDetail.subclass:
            return HazardousMaterialsCertificationDetail.subclass(*args_, **kwargs_)
        else:
            return HazardousMaterialsCertificationDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Format(self):
        return self.Format
    def set_Format(self, Format):
        self.Format = Format
    def hasContent_(self):
        if (
            self.Format is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='HazardousMaterialsCertificationDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('HazardousMaterialsCertificationDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'HazardousMaterialsCertificationDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='HazardousMaterialsCertificationDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='HazardousMaterialsCertificationDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='HazardousMaterialsCertificationDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='HazardousMaterialsCertificationDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Format is not None:
            namespaceprefix_ = self.Format_nsprefix_ + ':' if (UseCapturedNS_ and self.Format_nsprefix_) else ''
            self.Format.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Format', pretty_print=pretty_print)
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
            obj_ = CloseDocumentFormat.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Format = obj_
            obj_.original_tagname_ = 'Format'
# end class HazardousMaterialsCertificationDetail


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


class ManifestDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Format=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Format = Format
        self.Format_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ManifestDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ManifestDetail.subclass:
            return ManifestDetail.subclass(*args_, **kwargs_)
        else:
            return ManifestDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Format(self):
        return self.Format
    def set_Format(self, Format):
        self.Format = Format
    def hasContent_(self):
        if (
            self.Format is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ManifestDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ManifestDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ManifestDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ManifestDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ManifestDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ManifestDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ManifestDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Format is not None:
            namespaceprefix_ = self.Format_nsprefix_ + ':' if (UseCapturedNS_ and self.Format_nsprefix_) else ''
            self.Format.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Format', pretty_print=pretty_print)
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
            obj_ = CloseDocumentFormat.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Format = obj_
            obj_.original_tagname_ = 'Format'
# end class ManifestDetail


class ManifestFile(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, FileName=None, File=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.FileName = FileName
        self.FileName_nsprefix_ = None
        self.File = File
        self.File_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ManifestFile)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ManifestFile.subclass:
            return ManifestFile.subclass(*args_, **kwargs_)
        else:
            return ManifestFile(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_FileName(self):
        return self.FileName
    def set_FileName(self, FileName):
        self.FileName = FileName
    def get_File(self):
        return self.File
    def set_File(self, File):
        self.File = File
    def hasContent_(self):
        if (
            self.FileName is not None or
            self.File is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ManifestFile', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ManifestFile')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ManifestFile':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ManifestFile')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ManifestFile', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ManifestFile'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ManifestFile', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.FileName is not None:
            namespaceprefix_ = self.FileName_nsprefix_ + ':' if (UseCapturedNS_ and self.FileName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFileName>%s</%sFileName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FileName), input_name='FileName')), namespaceprefix_ , eol_))
        if self.File is not None:
            namespaceprefix_ = self.File_nsprefix_ + ':' if (UseCapturedNS_ and self.File_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFile>%s</%sFile>%s' % (namespaceprefix_ , self.gds_format_base64(self.File, input_name='File'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'FileName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FileName')
            value_ = self.gds_validate_string(value_, node, 'FileName')
            self.FileName = value_
            self.FileName_nsprefix_ = child_.prefix
        elif nodeName_ == 'File':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'File')
            else:
                bval_ = None
            self.File = bval_
            self.File_nsprefix_ = child_.prefix
# end class ManifestFile


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


class Op950Detail(GeneratedsSuper):
    """The instructions indicating how to print the OP-950 form for hazardous
    materials."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Format=None, CustomerImageUsages=None, SignatureName=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Format = Format
        self.Format_nsprefix_ = "ns"
        if CustomerImageUsages is None:
            self.CustomerImageUsages = []
        else:
            self.CustomerImageUsages = CustomerImageUsages
        self.CustomerImageUsages_nsprefix_ = "ns"
        self.SignatureName = SignatureName
        self.SignatureName_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Op950Detail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Op950Detail.subclass:
            return Op950Detail.subclass(*args_, **kwargs_)
        else:
            return Op950Detail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Format(self):
        return self.Format
    def set_Format(self, Format):
        self.Format = Format
    def get_CustomerImageUsages(self):
        return self.CustomerImageUsages
    def set_CustomerImageUsages(self, CustomerImageUsages):
        self.CustomerImageUsages = CustomerImageUsages
    def add_CustomerImageUsages(self, value):
        self.CustomerImageUsages.append(value)
    def insert_CustomerImageUsages_at(self, index, value):
        self.CustomerImageUsages.insert(index, value)
    def replace_CustomerImageUsages_at(self, index, value):
        self.CustomerImageUsages[index] = value
    def get_SignatureName(self):
        return self.SignatureName
    def set_SignatureName(self, SignatureName):
        self.SignatureName = SignatureName
    def hasContent_(self):
        if (
            self.Format is not None or
            self.CustomerImageUsages or
            self.SignatureName is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Op950Detail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Op950Detail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Op950Detail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Op950Detail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Op950Detail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Op950Detail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Op950Detail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Format is not None:
            namespaceprefix_ = self.Format_nsprefix_ + ':' if (UseCapturedNS_ and self.Format_nsprefix_) else ''
            self.Format.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Format', pretty_print=pretty_print)
        for CustomerImageUsages_ in self.CustomerImageUsages:
            namespaceprefix_ = self.CustomerImageUsages_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomerImageUsages_nsprefix_) else ''
            CustomerImageUsages_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CustomerImageUsages', pretty_print=pretty_print)
        if self.SignatureName is not None:
            namespaceprefix_ = self.SignatureName_nsprefix_ + ':' if (UseCapturedNS_ and self.SignatureName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSignatureName>%s</%sSignatureName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SignatureName), input_name='SignatureName')), namespaceprefix_ , eol_))
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
            obj_ = CloseDocumentFormat.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Format = obj_
            obj_.original_tagname_ = 'Format'
        elif nodeName_ == 'CustomerImageUsages':
            obj_ = CustomerImageUsage.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CustomerImageUsages.append(obj_)
            obj_.original_tagname_ = 'CustomerImageUsages'
        elif nodeName_ == 'SignatureName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SignatureName')
            value_ = self.gds_validate_string(value_, node, 'SignatureName')
            self.SignatureName = value_
            self.SignatureName_nsprefix_ = child_.prefix
# end class Op950Detail


class ReprintGroundCloseDocumentsRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, TransactionDetail=None, Version=None, ReprintOption=None, CloseDate=None, TrackingNumber=None, CloseDocumentSpecification=None, gds_collector_=None, **kwargs_):
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
        self.ReprintOption = ReprintOption
        self.validate_ReprintGroundCloseDocumentsOptionType(self.ReprintOption)
        self.ReprintOption_nsprefix_ = "ns"
        if isinstance(CloseDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(CloseDate, '%Y-%m-%d').date()
        else:
            initvalue_ = CloseDate
        self.CloseDate = initvalue_
        self.CloseDate_nsprefix_ = None
        self.TrackingNumber = TrackingNumber
        self.TrackingNumber_nsprefix_ = None
        self.CloseDocumentSpecification = CloseDocumentSpecification
        self.CloseDocumentSpecification_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ReprintGroundCloseDocumentsRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ReprintGroundCloseDocumentsRequest.subclass:
            return ReprintGroundCloseDocumentsRequest.subclass(*args_, **kwargs_)
        else:
            return ReprintGroundCloseDocumentsRequest(*args_, **kwargs_)
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
    def get_ReprintOption(self):
        return self.ReprintOption
    def set_ReprintOption(self, ReprintOption):
        self.ReprintOption = ReprintOption
    def get_CloseDate(self):
        return self.CloseDate
    def set_CloseDate(self, CloseDate):
        self.CloseDate = CloseDate
    def get_TrackingNumber(self):
        return self.TrackingNumber
    def set_TrackingNumber(self, TrackingNumber):
        self.TrackingNumber = TrackingNumber
    def get_CloseDocumentSpecification(self):
        return self.CloseDocumentSpecification
    def set_CloseDocumentSpecification(self, CloseDocumentSpecification):
        self.CloseDocumentSpecification = CloseDocumentSpecification
    def validate_ReprintGroundCloseDocumentsOptionType(self, value):
        result = True
        # Validate type ReprintGroundCloseDocumentsOptionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['BY_SHIP_DATE', 'BY_TRACKING_NUMBER']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ReprintGroundCloseDocumentsOptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.ReprintOption is not None or
            self.CloseDate is not None or
            self.TrackingNumber is not None or
            self.CloseDocumentSpecification is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReprintGroundCloseDocumentsRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ReprintGroundCloseDocumentsRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ReprintGroundCloseDocumentsRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ReprintGroundCloseDocumentsRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ReprintGroundCloseDocumentsRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ReprintGroundCloseDocumentsRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReprintGroundCloseDocumentsRequest', fromsubclass_=False, pretty_print=True):
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
        if self.ReprintOption is not None:
            namespaceprefix_ = self.ReprintOption_nsprefix_ + ':' if (UseCapturedNS_ and self.ReprintOption_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReprintOption>%s</%sReprintOption>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ReprintOption), input_name='ReprintOption')), namespaceprefix_ , eol_))
        if self.CloseDate is not None:
            namespaceprefix_ = self.CloseDate_nsprefix_ + ':' if (UseCapturedNS_ and self.CloseDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCloseDate>%s</%sCloseDate>%s' % (namespaceprefix_ , self.gds_format_date(self.CloseDate, input_name='CloseDate'), namespaceprefix_ , eol_))
        if self.TrackingNumber is not None:
            namespaceprefix_ = self.TrackingNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackingNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTrackingNumber>%s</%sTrackingNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TrackingNumber), input_name='TrackingNumber')), namespaceprefix_ , eol_))
        if self.CloseDocumentSpecification is not None:
            namespaceprefix_ = self.CloseDocumentSpecification_nsprefix_ + ':' if (UseCapturedNS_ and self.CloseDocumentSpecification_nsprefix_) else ''
            self.CloseDocumentSpecification.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CloseDocumentSpecification', pretty_print=pretty_print)
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
        elif nodeName_ == 'ReprintOption':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ReprintOption')
            value_ = self.gds_validate_string(value_, node, 'ReprintOption')
            self.ReprintOption = value_
            self.ReprintOption_nsprefix_ = child_.prefix
            # validate type ReprintGroundCloseDocumentsOptionType
            self.validate_ReprintGroundCloseDocumentsOptionType(self.ReprintOption)
        elif nodeName_ == 'CloseDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.CloseDate = dval_
            self.CloseDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'TrackingNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TrackingNumber')
            value_ = self.gds_validate_string(value_, node, 'TrackingNumber')
            self.TrackingNumber = value_
            self.TrackingNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'CloseDocumentSpecification':
            obj_ = CloseDocumentSpecification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CloseDocumentSpecification = obj_
            obj_.original_tagname_ = 'CloseDocumentSpecification'
# end class ReprintGroundCloseDocumentsRequest


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


class ShippingDocumentPart(GeneratedsSuper):
    """A single part of a shipping document, such as one page of a multiple-
    page document whose format requires a separate image per page."""
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
                CurrentSubclassModule_, ShippingDocumentPart)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShippingDocumentPart.subclass:
            return ShippingDocumentPart.subclass(*args_, **kwargs_)
        else:
            return ShippingDocumentPart(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShippingDocumentPart', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShippingDocumentPart')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShippingDocumentPart':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShippingDocumentPart')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShippingDocumentPart', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShippingDocumentPart'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShippingDocumentPart', fromsubclass_=False, pretty_print=True):
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
# end class ShippingDocumentPart


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


class SmartPostCloseReply(GeneratedsSuper):
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
                CurrentSubclassModule_, SmartPostCloseReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SmartPostCloseReply.subclass:
            return SmartPostCloseReply.subclass(*args_, **kwargs_)
        else:
            return SmartPostCloseReply(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SmartPostCloseReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SmartPostCloseReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SmartPostCloseReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SmartPostCloseReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SmartPostCloseReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SmartPostCloseReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SmartPostCloseReply', fromsubclass_=False, pretty_print=True):
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
# end class SmartPostCloseReply


class SmartPostCloseRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, TransactionDetail=None, Version=None, HubId=None, CustomerManifestId=None, DestinationCountryCode=None, PickUpCarrier=None, ManifestReferenceDetail=None, gds_collector_=None, **kwargs_):
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
        self.HubId = HubId
        self.HubId_nsprefix_ = None
        self.CustomerManifestId = CustomerManifestId
        self.CustomerManifestId_nsprefix_ = None
        self.DestinationCountryCode = DestinationCountryCode
        self.DestinationCountryCode_nsprefix_ = None
        self.PickUpCarrier = PickUpCarrier
        self.validate_CarrierCodeType(self.PickUpCarrier)
        self.PickUpCarrier_nsprefix_ = "ns"
        self.ManifestReferenceDetail = ManifestReferenceDetail
        self.ManifestReferenceDetail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SmartPostCloseRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SmartPostCloseRequest.subclass:
            return SmartPostCloseRequest.subclass(*args_, **kwargs_)
        else:
            return SmartPostCloseRequest(*args_, **kwargs_)
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
    def get_HubId(self):
        return self.HubId
    def set_HubId(self, HubId):
        self.HubId = HubId
    def get_CustomerManifestId(self):
        return self.CustomerManifestId
    def set_CustomerManifestId(self, CustomerManifestId):
        self.CustomerManifestId = CustomerManifestId
    def get_DestinationCountryCode(self):
        return self.DestinationCountryCode
    def set_DestinationCountryCode(self, DestinationCountryCode):
        self.DestinationCountryCode = DestinationCountryCode
    def get_PickUpCarrier(self):
        return self.PickUpCarrier
    def set_PickUpCarrier(self, PickUpCarrier):
        self.PickUpCarrier = PickUpCarrier
    def get_ManifestReferenceDetail(self):
        return self.ManifestReferenceDetail
    def set_ManifestReferenceDetail(self, ManifestReferenceDetail):
        self.ManifestReferenceDetail = ManifestReferenceDetail
    def validate_CarrierCodeType(self, value):
        result = True
        # Validate type CarrierCodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FDXC', 'FDXE', 'FDXG', 'FXCC', 'FXFR', 'FXSP']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CarrierCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.HubId is not None or
            self.CustomerManifestId is not None or
            self.DestinationCountryCode is not None or
            self.PickUpCarrier is not None or
            self.ManifestReferenceDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SmartPostCloseRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SmartPostCloseRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SmartPostCloseRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SmartPostCloseRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SmartPostCloseRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SmartPostCloseRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SmartPostCloseRequest', fromsubclass_=False, pretty_print=True):
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
        if self.HubId is not None:
            namespaceprefix_ = self.HubId_nsprefix_ + ':' if (UseCapturedNS_ and self.HubId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHubId>%s</%sHubId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HubId), input_name='HubId')), namespaceprefix_ , eol_))
        if self.CustomerManifestId is not None:
            namespaceprefix_ = self.CustomerManifestId_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomerManifestId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustomerManifestId>%s</%sCustomerManifestId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CustomerManifestId), input_name='CustomerManifestId')), namespaceprefix_ , eol_))
        if self.DestinationCountryCode is not None:
            namespaceprefix_ = self.DestinationCountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationCountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDestinationCountryCode>%s</%sDestinationCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DestinationCountryCode), input_name='DestinationCountryCode')), namespaceprefix_ , eol_))
        if self.PickUpCarrier is not None:
            namespaceprefix_ = self.PickUpCarrier_nsprefix_ + ':' if (UseCapturedNS_ and self.PickUpCarrier_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickUpCarrier>%s</%sPickUpCarrier>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickUpCarrier), input_name='PickUpCarrier')), namespaceprefix_ , eol_))
        if self.ManifestReferenceDetail is not None:
            namespaceprefix_ = self.ManifestReferenceDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ManifestReferenceDetail_nsprefix_) else ''
            self.ManifestReferenceDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ManifestReferenceDetail', pretty_print=pretty_print)
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
        elif nodeName_ == 'HubId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HubId')
            value_ = self.gds_validate_string(value_, node, 'HubId')
            self.HubId = value_
            self.HubId_nsprefix_ = child_.prefix
        elif nodeName_ == 'CustomerManifestId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CustomerManifestId')
            value_ = self.gds_validate_string(value_, node, 'CustomerManifestId')
            self.CustomerManifestId = value_
            self.CustomerManifestId_nsprefix_ = child_.prefix
        elif nodeName_ == 'DestinationCountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DestinationCountryCode')
            value_ = self.gds_validate_string(value_, node, 'DestinationCountryCode')
            self.DestinationCountryCode = value_
            self.DestinationCountryCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'PickUpCarrier':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickUpCarrier')
            value_ = self.gds_validate_string(value_, node, 'PickUpCarrier')
            self.PickUpCarrier = value_
            self.PickUpCarrier_nsprefix_ = child_.prefix
            # validate type CarrierCodeType
            self.validate_CarrierCodeType(self.PickUpCarrier)
        elif nodeName_ == 'ManifestReferenceDetail':
            obj_ = CloseManifestReferenceDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ManifestReferenceDetail = obj_
            obj_.original_tagname_ = 'ManifestReferenceDetail'
# end class SmartPostCloseRequest


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
    'CloseWithDocumentsReply': CloseWithDocumentsReply,
    'CloseWithDocumentsRequest': CloseWithDocumentsRequest,
    'GroundCloseDocumentsReply': GroundCloseDocumentsReply,
    'GroundCloseReply': GroundCloseReply,
    'GroundCloseReportsReprintReply': GroundCloseReportsReprintReply,
    'GroundCloseReportsReprintRequest': GroundCloseReportsReprintRequest,
    'GroundCloseRequest': GroundCloseRequest,
    'GroundCloseWithDocumentsRequest': GroundCloseWithDocumentsRequest,
    'ReprintGroundCloseDocumentsRequest': ReprintGroundCloseDocumentsRequest,
    'SmartPostCloseReply': SmartPostCloseReply,
    'SmartPostCloseRequest': SmartPostCloseRequest,
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
        rootTag = 'CloseWithDocumentsReply'
        rootClass = CloseWithDocumentsReply
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
        rootTag = 'CloseWithDocumentsReply'
        rootClass = CloseWithDocumentsReply
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
        rootTag = 'CloseWithDocumentsReply'
        rootClass = CloseWithDocumentsReply
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:ns="http://fedex.com/ws/close/v5"')
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
        rootTag = 'CloseWithDocumentsReply'
        rootClass = CloseWithDocumentsReply
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from close_service_v5 import *\n\n')
        sys.stdout.write('import close_service_v5 as model_\n\n')
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
NamespaceToDefMappings_ = {'http://fedex.com/ws/close/v5': [('CarrierCodeType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('CloseActionType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('CloseDocumentType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('CloseGroupingType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('CloseReportType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('CloseWithDocumentsProcessingOptionType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('CustomerImageUsageType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('CustomerReferenceType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('EMailNotificationRecipientType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('ImageId',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('InternalImageType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('LinearUnits',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('NotificationSeverityType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('ReprintGroundCloseDocumentsOptionType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('ShippingDocumentDispositionType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('ShippingDocumentEMailGroupingType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('ShippingDocumentGroupingType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('ShippingDocumentImageType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('ShippingDocumentNamingType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('ShippingDocumentStockType',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'ST'),
                                  ('ClientDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('CloseDocument',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('CloseDocumentFormat',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('CloseDocumentSpecification',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('CloseManifestReferenceDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('CloseSmartPostDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('CloseWithDocumentsProcessingOptionsRequested',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('CloseWithDocumentsReply',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('CloseWithDocumentsRequest',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('CustomerImageUsage',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('DetailedDeliveryManifestDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('GroundCloseDocumentsReply',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('GroundCloseReply',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('GroundCloseReportsReprintReply',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('GroundCloseReportsReprintRequest',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('GroundCloseRequest',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('GroundCloseWithDocumentsRequest',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('HazardousMaterialsCertificationDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('LinearMeasure',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('Localization',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('ManifestDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('ManifestFile',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('Notification',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('NotificationParameter',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('Op950Detail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('ReprintGroundCloseDocumentsRequest',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('ShippingDocumentDispositionDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('ShippingDocumentEMailDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('ShippingDocumentEMailRecipient',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('ShippingDocumentPart',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('ShippingDocumentPrintDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('ShippingDocumentStorageDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('SmartPostCloseReply',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('SmartPostCloseRequest',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('TransactionDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('WebAuthenticationDetail',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('WebAuthenticationCredential',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT'),
                                  ('VersionId',
                                   '../../../Carriers '
                                   'Doc/Fedex/2020-09/schemas/CloseService_v5.xsd',
                                   'CT')]}

__all__ = [
    "ClientDetail",
    "CloseDocument",
    "CloseDocumentFormat",
    "CloseDocumentSpecification",
    "CloseManifestReferenceDetail",
    "CloseSmartPostDetail",
    "CloseWithDocumentsProcessingOptionsRequested",
    "CloseWithDocumentsReply",
    "CloseWithDocumentsRequest",
    "CustomerImageUsage",
    "DetailedDeliveryManifestDetail",
    "GroundCloseDocumentsReply",
    "GroundCloseReply",
    "GroundCloseReportsReprintReply",
    "GroundCloseReportsReprintRequest",
    "GroundCloseRequest",
    "GroundCloseWithDocumentsRequest",
    "HazardousMaterialsCertificationDetail",
    "LinearMeasure",
    "Localization",
    "ManifestDetail",
    "ManifestFile",
    "Notification",
    "NotificationParameter",
    "Op950Detail",
    "ReprintGroundCloseDocumentsRequest",
    "ShippingDocumentDispositionDetail",
    "ShippingDocumentEMailDetail",
    "ShippingDocumentEMailRecipient",
    "ShippingDocumentPart",
    "ShippingDocumentPrintDetail",
    "ShippingDocumentStorageDetail",
    "SmartPostCloseReply",
    "SmartPostCloseRequest",
    "TransactionDetail",
    "VersionId",
    "WebAuthenticationCredential",
    "WebAuthenticationDetail"
]
