#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Thu Feb 11 08:51:10 2021 by generateDS.py version 2.37.15.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './aramex_lib/location.py')
#
# Command line arguments:
#   ./schemas/location.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/karrio-carriers/.venv/karrio-carriers/bin/generateDS --no-namespace-defs -o "./aramex_lib/location.py" ./schemas/location.xsd
#
# Current working directory (os.getcwd()):
#   aramex
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


class AddressValidationRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ClientInfo=None, Transaction=None, Address=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ClientInfo = ClientInfo
        self.ClientInfo_nsprefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.Address = Address
        self.Address_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AddressValidationRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AddressValidationRequest.subclass:
            return AddressValidationRequest.subclass(*args_, **kwargs_)
        else:
            return AddressValidationRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ClientInfo(self):
        return self.ClientInfo
    def set_ClientInfo(self, ClientInfo):
        self.ClientInfo = ClientInfo
    def get_Transaction(self):
        return self.Transaction
    def set_Transaction(self, Transaction):
        self.Transaction = Transaction
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def hasContent_(self):
        if (
            self.ClientInfo is not None or
            self.Transaction is not None or
            self.Address is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressValidationRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AddressValidationRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AddressValidationRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AddressValidationRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AddressValidationRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AddressValidationRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressValidationRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ClientInfo is not None:
            namespaceprefix_ = self.ClientInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientInfo_nsprefix_) else ''
            self.ClientInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClientInfo', pretty_print=pretty_print)
        if self.Transaction is not None:
            namespaceprefix_ = self.Transaction_nsprefix_ + ':' if (UseCapturedNS_ and self.Transaction_nsprefix_) else ''
            self.Transaction.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Transaction', pretty_print=pretty_print)
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
        if nodeName_ == 'ClientInfo':
            obj_ = ClientInfo.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClientInfo = obj_
            obj_.original_tagname_ = 'ClientInfo'
        elif nodeName_ == 'Transaction':
            obj_ = Transaction.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transaction = obj_
            obj_.original_tagname_ = 'Transaction'
        elif nodeName_ == 'Address':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
# end class AddressValidationRequest


class ClientInfo(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, UserName=None, Password=None, Version=None, AccountNumber=None, AccountPin=None, AccountEntity=None, AccountCountryCode=None, Source=None, PreferredLanguageCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.UserName = UserName
        self.UserName_nsprefix_ = None
        self.Password = Password
        self.Password_nsprefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        self.AccountNumber = AccountNumber
        self.AccountNumber_nsprefix_ = None
        self.AccountPin = AccountPin
        self.AccountPin_nsprefix_ = None
        self.AccountEntity = AccountEntity
        self.AccountEntity_nsprefix_ = None
        self.AccountCountryCode = AccountCountryCode
        self.AccountCountryCode_nsprefix_ = None
        self.Source = Source
        self.Source_nsprefix_ = None
        self.PreferredLanguageCode = PreferredLanguageCode
        self.PreferredLanguageCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ClientInfo)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ClientInfo.subclass:
            return ClientInfo.subclass(*args_, **kwargs_)
        else:
            return ClientInfo(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_UserName(self):
        return self.UserName
    def set_UserName(self, UserName):
        self.UserName = UserName
    def get_Password(self):
        return self.Password
    def set_Password(self, Password):
        self.Password = Password
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_AccountNumber(self):
        return self.AccountNumber
    def set_AccountNumber(self, AccountNumber):
        self.AccountNumber = AccountNumber
    def get_AccountPin(self):
        return self.AccountPin
    def set_AccountPin(self, AccountPin):
        self.AccountPin = AccountPin
    def get_AccountEntity(self):
        return self.AccountEntity
    def set_AccountEntity(self, AccountEntity):
        self.AccountEntity = AccountEntity
    def get_AccountCountryCode(self):
        return self.AccountCountryCode
    def set_AccountCountryCode(self, AccountCountryCode):
        self.AccountCountryCode = AccountCountryCode
    def get_Source(self):
        return self.Source
    def set_Source(self, Source):
        self.Source = Source
    def get_PreferredLanguageCode(self):
        return self.PreferredLanguageCode
    def set_PreferredLanguageCode(self, PreferredLanguageCode):
        self.PreferredLanguageCode = PreferredLanguageCode
    def hasContent_(self):
        if (
            self.UserName is not None or
            self.Password is not None or
            self.Version is not None or
            self.AccountNumber is not None or
            self.AccountPin is not None or
            self.AccountEntity is not None or
            self.AccountCountryCode is not None or
            self.Source is not None or
            self.PreferredLanguageCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ClientInfo', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ClientInfo')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ClientInfo':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ClientInfo')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ClientInfo', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ClientInfo'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ClientInfo', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.UserName is not None:
            namespaceprefix_ = self.UserName_nsprefix_ + ':' if (UseCapturedNS_ and self.UserName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUserName>%s</%sUserName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UserName), input_name='UserName')), namespaceprefix_ , eol_))
        if self.Password is not None:
            namespaceprefix_ = self.Password_nsprefix_ + ':' if (UseCapturedNS_ and self.Password_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPassword>%s</%sPassword>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Password), input_name='Password')), namespaceprefix_ , eol_))
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sVersion>%s</%sVersion>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Version), input_name='Version')), namespaceprefix_ , eol_))
        if self.AccountNumber is not None:
            namespaceprefix_ = self.AccountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.AccountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccountNumber>%s</%sAccountNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AccountNumber), input_name='AccountNumber')), namespaceprefix_ , eol_))
        if self.AccountPin is not None:
            namespaceprefix_ = self.AccountPin_nsprefix_ + ':' if (UseCapturedNS_ and self.AccountPin_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccountPin>%s</%sAccountPin>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AccountPin), input_name='AccountPin')), namespaceprefix_ , eol_))
        if self.AccountEntity is not None:
            namespaceprefix_ = self.AccountEntity_nsprefix_ + ':' if (UseCapturedNS_ and self.AccountEntity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccountEntity>%s</%sAccountEntity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AccountEntity), input_name='AccountEntity')), namespaceprefix_ , eol_))
        if self.AccountCountryCode is not None:
            namespaceprefix_ = self.AccountCountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.AccountCountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccountCountryCode>%s</%sAccountCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AccountCountryCode), input_name='AccountCountryCode')), namespaceprefix_ , eol_))
        if self.Source is not None:
            namespaceprefix_ = self.Source_nsprefix_ + ':' if (UseCapturedNS_ and self.Source_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSource>%s</%sSource>%s' % (namespaceprefix_ , self.gds_format_integer(self.Source, input_name='Source'), namespaceprefix_ , eol_))
        if self.PreferredLanguageCode is not None:
            namespaceprefix_ = self.PreferredLanguageCode_nsprefix_ + ':' if (UseCapturedNS_ and self.PreferredLanguageCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPreferredLanguageCode>%s</%sPreferredLanguageCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PreferredLanguageCode), input_name='PreferredLanguageCode')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'UserName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UserName')
            value_ = self.gds_validate_string(value_, node, 'UserName')
            self.UserName = value_
            self.UserName_nsprefix_ = child_.prefix
        elif nodeName_ == 'Password':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Password')
            value_ = self.gds_validate_string(value_, node, 'Password')
            self.Password = value_
            self.Password_nsprefix_ = child_.prefix
        elif nodeName_ == 'Version':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Version')
            value_ = self.gds_validate_string(value_, node, 'Version')
            self.Version = value_
            self.Version_nsprefix_ = child_.prefix
        elif nodeName_ == 'AccountNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AccountNumber')
            value_ = self.gds_validate_string(value_, node, 'AccountNumber')
            self.AccountNumber = value_
            self.AccountNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'AccountPin':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AccountPin')
            value_ = self.gds_validate_string(value_, node, 'AccountPin')
            self.AccountPin = value_
            self.AccountPin_nsprefix_ = child_.prefix
        elif nodeName_ == 'AccountEntity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AccountEntity')
            value_ = self.gds_validate_string(value_, node, 'AccountEntity')
            self.AccountEntity = value_
            self.AccountEntity_nsprefix_ = child_.prefix
        elif nodeName_ == 'AccountCountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AccountCountryCode')
            value_ = self.gds_validate_string(value_, node, 'AccountCountryCode')
            self.AccountCountryCode = value_
            self.AccountCountryCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'Source' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Source')
            ival_ = self.gds_validate_integer(ival_, node, 'Source')
            self.Source = ival_
            self.Source_nsprefix_ = child_.prefix
        elif nodeName_ == 'PreferredLanguageCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PreferredLanguageCode')
            value_ = self.gds_validate_string(value_, node, 'PreferredLanguageCode')
            self.PreferredLanguageCode = value_
            self.PreferredLanguageCode_nsprefix_ = child_.prefix
# end class ClientInfo


class Transaction(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Reference1=None, Reference2=None, Reference3=None, Reference4=None, Reference5=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Reference1 = Reference1
        self.Reference1_nsprefix_ = None
        self.Reference2 = Reference2
        self.Reference2_nsprefix_ = None
        self.Reference3 = Reference3
        self.Reference3_nsprefix_ = None
        self.Reference4 = Reference4
        self.Reference4_nsprefix_ = None
        self.Reference5 = Reference5
        self.Reference5_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Transaction)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Transaction.subclass:
            return Transaction.subclass(*args_, **kwargs_)
        else:
            return Transaction(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Reference1(self):
        return self.Reference1
    def set_Reference1(self, Reference1):
        self.Reference1 = Reference1
    def get_Reference2(self):
        return self.Reference2
    def set_Reference2(self, Reference2):
        self.Reference2 = Reference2
    def get_Reference3(self):
        return self.Reference3
    def set_Reference3(self, Reference3):
        self.Reference3 = Reference3
    def get_Reference4(self):
        return self.Reference4
    def set_Reference4(self, Reference4):
        self.Reference4 = Reference4
    def get_Reference5(self):
        return self.Reference5
    def set_Reference5(self, Reference5):
        self.Reference5 = Reference5
    def hasContent_(self):
        if (
            self.Reference1 is not None or
            self.Reference2 is not None or
            self.Reference3 is not None or
            self.Reference4 is not None or
            self.Reference5 is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Transaction', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Transaction')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Transaction':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Transaction')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Transaction', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Transaction'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Transaction', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Reference1 is not None:
            namespaceprefix_ = self.Reference1_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference1>%s</%sReference1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference1), input_name='Reference1')), namespaceprefix_ , eol_))
        if self.Reference2 is not None:
            namespaceprefix_ = self.Reference2_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference2>%s</%sReference2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference2), input_name='Reference2')), namespaceprefix_ , eol_))
        if self.Reference3 is not None:
            namespaceprefix_ = self.Reference3_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference3_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference3>%s</%sReference3>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference3), input_name='Reference3')), namespaceprefix_ , eol_))
        if self.Reference4 is not None:
            namespaceprefix_ = self.Reference4_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference4_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference4>%s</%sReference4>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference4), input_name='Reference4')), namespaceprefix_ , eol_))
        if self.Reference5 is not None:
            namespaceprefix_ = self.Reference5_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference5_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference5>%s</%sReference5>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference5), input_name='Reference5')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Reference1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Reference1')
            value_ = self.gds_validate_string(value_, node, 'Reference1')
            self.Reference1 = value_
            self.Reference1_nsprefix_ = child_.prefix
        elif nodeName_ == 'Reference2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Reference2')
            value_ = self.gds_validate_string(value_, node, 'Reference2')
            self.Reference2 = value_
            self.Reference2_nsprefix_ = child_.prefix
        elif nodeName_ == 'Reference3':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Reference3')
            value_ = self.gds_validate_string(value_, node, 'Reference3')
            self.Reference3 = value_
            self.Reference3_nsprefix_ = child_.prefix
        elif nodeName_ == 'Reference4':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Reference4')
            value_ = self.gds_validate_string(value_, node, 'Reference4')
            self.Reference4 = value_
            self.Reference4_nsprefix_ = child_.prefix
        elif nodeName_ == 'Reference5':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Reference5')
            value_ = self.gds_validate_string(value_, node, 'Reference5')
            self.Reference5 = value_
            self.Reference5_nsprefix_ = child_.prefix
# end class Transaction


class Address(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Line1=None, Line2=None, Line3=None, City=None, StateOrProvinceCode=None, PostCode=None, CountryCode=None, Longitude=None, Latitude=None, BuildingNumber=None, BuildingName=None, Floor=None, Apartment=None, POBox=None, Description=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Line1 = Line1
        self.Line1_nsprefix_ = None
        self.Line2 = Line2
        self.Line2_nsprefix_ = None
        self.Line3 = Line3
        self.Line3_nsprefix_ = None
        self.City = City
        self.City_nsprefix_ = None
        self.StateOrProvinceCode = StateOrProvinceCode
        self.StateOrProvinceCode_nsprefix_ = None
        self.PostCode = PostCode
        self.PostCode_nsprefix_ = None
        self.CountryCode = CountryCode
        self.CountryCode_nsprefix_ = None
        self.Longitude = Longitude
        self.Longitude_nsprefix_ = None
        self.Latitude = Latitude
        self.Latitude_nsprefix_ = None
        self.BuildingNumber = BuildingNumber
        self.BuildingNumber_nsprefix_ = None
        self.BuildingName = BuildingName
        self.BuildingName_nsprefix_ = None
        self.Floor = Floor
        self.Floor_nsprefix_ = None
        self.Apartment = Apartment
        self.Apartment_nsprefix_ = None
        self.POBox = POBox
        self.POBox_nsprefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = None
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
    def get_Line1(self):
        return self.Line1
    def set_Line1(self, Line1):
        self.Line1 = Line1
    def get_Line2(self):
        return self.Line2
    def set_Line2(self, Line2):
        self.Line2 = Line2
    def get_Line3(self):
        return self.Line3
    def set_Line3(self, Line3):
        self.Line3 = Line3
    def get_City(self):
        return self.City
    def set_City(self, City):
        self.City = City
    def get_StateOrProvinceCode(self):
        return self.StateOrProvinceCode
    def set_StateOrProvinceCode(self, StateOrProvinceCode):
        self.StateOrProvinceCode = StateOrProvinceCode
    def get_PostCode(self):
        return self.PostCode
    def set_PostCode(self, PostCode):
        self.PostCode = PostCode
    def get_CountryCode(self):
        return self.CountryCode
    def set_CountryCode(self, CountryCode):
        self.CountryCode = CountryCode
    def get_Longitude(self):
        return self.Longitude
    def set_Longitude(self, Longitude):
        self.Longitude = Longitude
    def get_Latitude(self):
        return self.Latitude
    def set_Latitude(self, Latitude):
        self.Latitude = Latitude
    def get_BuildingNumber(self):
        return self.BuildingNumber
    def set_BuildingNumber(self, BuildingNumber):
        self.BuildingNumber = BuildingNumber
    def get_BuildingName(self):
        return self.BuildingName
    def set_BuildingName(self, BuildingName):
        self.BuildingName = BuildingName
    def get_Floor(self):
        return self.Floor
    def set_Floor(self, Floor):
        self.Floor = Floor
    def get_Apartment(self):
        return self.Apartment
    def set_Apartment(self, Apartment):
        self.Apartment = Apartment
    def get_POBox(self):
        return self.POBox
    def set_POBox(self, POBox):
        self.POBox = POBox
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def hasContent_(self):
        if (
            self.Line1 is not None or
            self.Line2 is not None or
            self.Line3 is not None or
            self.City is not None or
            self.StateOrProvinceCode is not None or
            self.PostCode is not None or
            self.CountryCode is not None or
            self.Longitude is not None or
            self.Latitude is not None or
            self.BuildingNumber is not None or
            self.BuildingName is not None or
            self.Floor is not None or
            self.Apartment is not None or
            self.POBox is not None or
            self.Description is not None
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
        if self.Line1 is not None:
            namespaceprefix_ = self.Line1_nsprefix_ + ':' if (UseCapturedNS_ and self.Line1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLine1>%s</%sLine1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Line1), input_name='Line1')), namespaceprefix_ , eol_))
        if self.Line2 is not None:
            namespaceprefix_ = self.Line2_nsprefix_ + ':' if (UseCapturedNS_ and self.Line2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLine2>%s</%sLine2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Line2), input_name='Line2')), namespaceprefix_ , eol_))
        if self.Line3 is not None:
            namespaceprefix_ = self.Line3_nsprefix_ + ':' if (UseCapturedNS_ and self.Line3_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLine3>%s</%sLine3>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Line3), input_name='Line3')), namespaceprefix_ , eol_))
        if self.City is not None:
            namespaceprefix_ = self.City_nsprefix_ + ':' if (UseCapturedNS_ and self.City_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCity>%s</%sCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.City), input_name='City')), namespaceprefix_ , eol_))
        if self.StateOrProvinceCode is not None:
            namespaceprefix_ = self.StateOrProvinceCode_nsprefix_ + ':' if (UseCapturedNS_ and self.StateOrProvinceCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStateOrProvinceCode>%s</%sStateOrProvinceCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.StateOrProvinceCode), input_name='StateOrProvinceCode')), namespaceprefix_ , eol_))
        if self.PostCode is not None:
            namespaceprefix_ = self.PostCode_nsprefix_ + ':' if (UseCapturedNS_ and self.PostCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPostCode>%s</%sPostCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PostCode), input_name='PostCode')), namespaceprefix_ , eol_))
        if self.CountryCode is not None:
            namespaceprefix_ = self.CountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryCode>%s</%sCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryCode), input_name='CountryCode')), namespaceprefix_ , eol_))
        if self.Longitude is not None:
            namespaceprefix_ = self.Longitude_nsprefix_ + ':' if (UseCapturedNS_ and self.Longitude_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLongitude>%s</%sLongitude>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Longitude, input_name='Longitude'), namespaceprefix_ , eol_))
        if self.Latitude is not None:
            namespaceprefix_ = self.Latitude_nsprefix_ + ':' if (UseCapturedNS_ and self.Latitude_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLatitude>%s</%sLatitude>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Latitude, input_name='Latitude'), namespaceprefix_ , eol_))
        if self.BuildingNumber is not None:
            namespaceprefix_ = self.BuildingNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.BuildingNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBuildingNumber>%s</%sBuildingNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BuildingNumber), input_name='BuildingNumber')), namespaceprefix_ , eol_))
        if self.BuildingName is not None:
            namespaceprefix_ = self.BuildingName_nsprefix_ + ':' if (UseCapturedNS_ and self.BuildingName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBuildingName>%s</%sBuildingName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BuildingName), input_name='BuildingName')), namespaceprefix_ , eol_))
        if self.Floor is not None:
            namespaceprefix_ = self.Floor_nsprefix_ + ':' if (UseCapturedNS_ and self.Floor_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFloor>%s</%sFloor>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Floor), input_name='Floor')), namespaceprefix_ , eol_))
        if self.Apartment is not None:
            namespaceprefix_ = self.Apartment_nsprefix_ + ':' if (UseCapturedNS_ and self.Apartment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sApartment>%s</%sApartment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Apartment), input_name='Apartment')), namespaceprefix_ , eol_))
        if self.POBox is not None:
            namespaceprefix_ = self.POBox_nsprefix_ + ':' if (UseCapturedNS_ and self.POBox_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPOBox>%s</%sPOBox>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.POBox), input_name='POBox')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Line1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Line1')
            value_ = self.gds_validate_string(value_, node, 'Line1')
            self.Line1 = value_
            self.Line1_nsprefix_ = child_.prefix
        elif nodeName_ == 'Line2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Line2')
            value_ = self.gds_validate_string(value_, node, 'Line2')
            self.Line2 = value_
            self.Line2_nsprefix_ = child_.prefix
        elif nodeName_ == 'Line3':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Line3')
            value_ = self.gds_validate_string(value_, node, 'Line3')
            self.Line3 = value_
            self.Line3_nsprefix_ = child_.prefix
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
        elif nodeName_ == 'PostCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PostCode')
            value_ = self.gds_validate_string(value_, node, 'PostCode')
            self.PostCode = value_
            self.PostCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'CountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryCode')
            value_ = self.gds_validate_string(value_, node, 'CountryCode')
            self.CountryCode = value_
            self.CountryCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'Longitude' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Longitude')
            fval_ = self.gds_validate_decimal(fval_, node, 'Longitude')
            self.Longitude = fval_
            self.Longitude_nsprefix_ = child_.prefix
        elif nodeName_ == 'Latitude' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Latitude')
            fval_ = self.gds_validate_decimal(fval_, node, 'Latitude')
            self.Latitude = fval_
            self.Latitude_nsprefix_ = child_.prefix
        elif nodeName_ == 'BuildingNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BuildingNumber')
            value_ = self.gds_validate_string(value_, node, 'BuildingNumber')
            self.BuildingNumber = value_
            self.BuildingNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'BuildingName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BuildingName')
            value_ = self.gds_validate_string(value_, node, 'BuildingName')
            self.BuildingName = value_
            self.BuildingName_nsprefix_ = child_.prefix
        elif nodeName_ == 'Floor':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Floor')
            value_ = self.gds_validate_string(value_, node, 'Floor')
            self.Floor = value_
            self.Floor_nsprefix_ = child_.prefix
        elif nodeName_ == 'Apartment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Apartment')
            value_ = self.gds_validate_string(value_, node, 'Apartment')
            self.Apartment = value_
            self.Apartment_nsprefix_ = child_.prefix
        elif nodeName_ == 'POBox':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'POBox')
            value_ = self.gds_validate_string(value_, node, 'POBox')
            self.POBox = value_
            self.POBox_nsprefix_ = child_.prefix
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
# end class Address


class AddressValidationResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Transaction=None, Notifications=None, HasErrors=None, SuggestedAddresses=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.Notifications = Notifications
        self.Notifications_nsprefix_ = None
        self.HasErrors = HasErrors
        self.HasErrors_nsprefix_ = None
        self.SuggestedAddresses = SuggestedAddresses
        self.SuggestedAddresses_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AddressValidationResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AddressValidationResponse.subclass:
            return AddressValidationResponse.subclass(*args_, **kwargs_)
        else:
            return AddressValidationResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Transaction(self):
        return self.Transaction
    def set_Transaction(self, Transaction):
        self.Transaction = Transaction
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def get_HasErrors(self):
        return self.HasErrors
    def set_HasErrors(self, HasErrors):
        self.HasErrors = HasErrors
    def get_SuggestedAddresses(self):
        return self.SuggestedAddresses
    def set_SuggestedAddresses(self, SuggestedAddresses):
        self.SuggestedAddresses = SuggestedAddresses
    def hasContent_(self):
        if (
            self.Transaction is not None or
            self.Notifications is not None or
            self.HasErrors is not None or
            self.SuggestedAddresses is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressValidationResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AddressValidationResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AddressValidationResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AddressValidationResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AddressValidationResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AddressValidationResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressValidationResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Transaction is not None:
            namespaceprefix_ = self.Transaction_nsprefix_ + ':' if (UseCapturedNS_ and self.Transaction_nsprefix_) else ''
            self.Transaction.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Transaction', pretty_print=pretty_print)
        if self.Notifications is not None:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            self.Notifications.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.HasErrors is not None:
            namespaceprefix_ = self.HasErrors_nsprefix_ + ':' if (UseCapturedNS_ and self.HasErrors_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHasErrors>%s</%sHasErrors>%s' % (namespaceprefix_ , self.gds_format_boolean(self.HasErrors, input_name='HasErrors'), namespaceprefix_ , eol_))
        if self.SuggestedAddresses is not None:
            namespaceprefix_ = self.SuggestedAddresses_nsprefix_ + ':' if (UseCapturedNS_ and self.SuggestedAddresses_nsprefix_) else ''
            self.SuggestedAddresses.export(outfile, level, namespaceprefix_, namespacedef_='', name_='SuggestedAddresses', pretty_print=pretty_print)
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
        if nodeName_ == 'Transaction':
            obj_ = Transaction.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transaction = obj_
            obj_.original_tagname_ = 'Transaction'
        elif nodeName_ == 'Notifications':
            obj_ = ArrayOfNotification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications = obj_
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'HasErrors':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'HasErrors')
            ival_ = self.gds_validate_boolean(ival_, node, 'HasErrors')
            self.HasErrors = ival_
            self.HasErrors_nsprefix_ = child_.prefix
        elif nodeName_ == 'SuggestedAddresses':
            obj_ = ArrayOfAddress.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SuggestedAddresses = obj_
            obj_.original_tagname_ = 'SuggestedAddresses'
# end class AddressValidationResponse


class ArrayOfNotification(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Notification=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Notification is None:
            self.Notification = []
        else:
            self.Notification = Notification
        self.Notification_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfNotification)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfNotification.subclass:
            return ArrayOfNotification.subclass(*args_, **kwargs_)
        else:
            return ArrayOfNotification(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Notification(self):
        return self.Notification
    def set_Notification(self, Notification):
        self.Notification = Notification
    def add_Notification(self, value):
        self.Notification.append(value)
    def insert_Notification_at(self, index, value):
        self.Notification.insert(index, value)
    def replace_Notification_at(self, index, value):
        self.Notification[index] = value
    def hasContent_(self):
        if (
            self.Notification
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfNotification', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfNotification')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfNotification':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfNotification')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfNotification', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfNotification'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfNotification', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Notification_ in self.Notification:
            namespaceprefix_ = self.Notification_nsprefix_ + ':' if (UseCapturedNS_ and self.Notification_nsprefix_) else ''
            Notification_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notification', pretty_print=pretty_print)
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
        if nodeName_ == 'Notification':
            obj_ = Notification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notification.append(obj_)
            obj_.original_tagname_ = 'Notification'
# end class ArrayOfNotification


class Notification(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Code=None, Message=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Code = Code
        self.Code_nsprefix_ = None
        self.Message = Message
        self.Message_nsprefix_ = None
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
    def get_Code(self):
        return self.Code
    def set_Code(self, Code):
        self.Code = Code
    def get_Message(self):
        return self.Message
    def set_Message(self, Message):
        self.Message = Message
    def hasContent_(self):
        if (
            self.Code is not None or
            self.Message is not None
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
        if self.Code is not None:
            namespaceprefix_ = self.Code_nsprefix_ + ':' if (UseCapturedNS_ and self.Code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCode>%s</%sCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Code), input_name='Code')), namespaceprefix_ , eol_))
        if self.Message is not None:
            namespaceprefix_ = self.Message_nsprefix_ + ':' if (UseCapturedNS_ and self.Message_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMessage>%s</%sMessage>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Message), input_name='Message')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Code':
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
# end class Notification


class ArrayOfAddress(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Address=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Address is None:
            self.Address = []
        else:
            self.Address = Address
        self.Address_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfAddress)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfAddress.subclass:
            return ArrayOfAddress.subclass(*args_, **kwargs_)
        else:
            return ArrayOfAddress(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def add_Address(self, value):
        self.Address.append(value)
    def insert_Address_at(self, index, value):
        self.Address.insert(index, value)
    def replace_Address_at(self, index, value):
        self.Address[index] = value
    def hasContent_(self):
        if (
            self.Address
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfAddress', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfAddress')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfAddress':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfAddress')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfAddress', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfAddress'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfAddress', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Address_ in self.Address:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            Address_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
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
        if nodeName_ == 'Address':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address.append(obj_)
            obj_.original_tagname_ = 'Address'
# end class ArrayOfAddress


class CountriesFetchingRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ClientInfo=None, Transaction=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ClientInfo = ClientInfo
        self.ClientInfo_nsprefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CountriesFetchingRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CountriesFetchingRequest.subclass:
            return CountriesFetchingRequest.subclass(*args_, **kwargs_)
        else:
            return CountriesFetchingRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ClientInfo(self):
        return self.ClientInfo
    def set_ClientInfo(self, ClientInfo):
        self.ClientInfo = ClientInfo
    def get_Transaction(self):
        return self.Transaction
    def set_Transaction(self, Transaction):
        self.Transaction = Transaction
    def hasContent_(self):
        if (
            self.ClientInfo is not None or
            self.Transaction is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CountriesFetchingRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CountriesFetchingRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CountriesFetchingRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CountriesFetchingRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CountriesFetchingRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CountriesFetchingRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CountriesFetchingRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ClientInfo is not None:
            namespaceprefix_ = self.ClientInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientInfo_nsprefix_) else ''
            self.ClientInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClientInfo', pretty_print=pretty_print)
        if self.Transaction is not None:
            namespaceprefix_ = self.Transaction_nsprefix_ + ':' if (UseCapturedNS_ and self.Transaction_nsprefix_) else ''
            self.Transaction.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Transaction', pretty_print=pretty_print)
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
        if nodeName_ == 'ClientInfo':
            obj_ = ClientInfo.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClientInfo = obj_
            obj_.original_tagname_ = 'ClientInfo'
        elif nodeName_ == 'Transaction':
            obj_ = Transaction.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transaction = obj_
            obj_.original_tagname_ = 'Transaction'
# end class CountriesFetchingRequest


class CountriesFetchingResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Transaction=None, Notifications=None, HasErrors=None, Countries=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.Notifications = Notifications
        self.Notifications_nsprefix_ = None
        self.HasErrors = HasErrors
        self.HasErrors_nsprefix_ = None
        self.Countries = Countries
        self.Countries_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CountriesFetchingResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CountriesFetchingResponse.subclass:
            return CountriesFetchingResponse.subclass(*args_, **kwargs_)
        else:
            return CountriesFetchingResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Transaction(self):
        return self.Transaction
    def set_Transaction(self, Transaction):
        self.Transaction = Transaction
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def get_HasErrors(self):
        return self.HasErrors
    def set_HasErrors(self, HasErrors):
        self.HasErrors = HasErrors
    def get_Countries(self):
        return self.Countries
    def set_Countries(self, Countries):
        self.Countries = Countries
    def hasContent_(self):
        if (
            self.Transaction is not None or
            self.Notifications is not None or
            self.HasErrors is not None or
            self.Countries is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CountriesFetchingResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CountriesFetchingResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CountriesFetchingResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CountriesFetchingResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CountriesFetchingResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CountriesFetchingResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CountriesFetchingResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Transaction is not None:
            namespaceprefix_ = self.Transaction_nsprefix_ + ':' if (UseCapturedNS_ and self.Transaction_nsprefix_) else ''
            self.Transaction.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Transaction', pretty_print=pretty_print)
        if self.Notifications is not None:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            self.Notifications.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.HasErrors is not None:
            namespaceprefix_ = self.HasErrors_nsprefix_ + ':' if (UseCapturedNS_ and self.HasErrors_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHasErrors>%s</%sHasErrors>%s' % (namespaceprefix_ , self.gds_format_boolean(self.HasErrors, input_name='HasErrors'), namespaceprefix_ , eol_))
        if self.Countries is not None:
            namespaceprefix_ = self.Countries_nsprefix_ + ':' if (UseCapturedNS_ and self.Countries_nsprefix_) else ''
            self.Countries.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Countries', pretty_print=pretty_print)
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
        if nodeName_ == 'Transaction':
            obj_ = Transaction.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transaction = obj_
            obj_.original_tagname_ = 'Transaction'
        elif nodeName_ == 'Notifications':
            obj_ = ArrayOfNotification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications = obj_
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'HasErrors':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'HasErrors')
            ival_ = self.gds_validate_boolean(ival_, node, 'HasErrors')
            self.HasErrors = ival_
            self.HasErrors_nsprefix_ = child_.prefix
        elif nodeName_ == 'Countries':
            obj_ = ArrayOfCountry.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Countries = obj_
            obj_.original_tagname_ = 'Countries'
# end class CountriesFetchingResponse


class ArrayOfCountry(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Country=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Country is None:
            self.Country = []
        else:
            self.Country = Country
        self.Country_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfCountry)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfCountry.subclass:
            return ArrayOfCountry.subclass(*args_, **kwargs_)
        else:
            return ArrayOfCountry(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Country(self):
        return self.Country
    def set_Country(self, Country):
        self.Country = Country
    def add_Country(self, value):
        self.Country.append(value)
    def insert_Country_at(self, index, value):
        self.Country.insert(index, value)
    def replace_Country_at(self, index, value):
        self.Country[index] = value
    def hasContent_(self):
        if (
            self.Country
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfCountry', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfCountry')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfCountry':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfCountry')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfCountry', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfCountry'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfCountry', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Country_ in self.Country:
            namespaceprefix_ = self.Country_nsprefix_ + ':' if (UseCapturedNS_ and self.Country_nsprefix_) else ''
            Country_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Country', pretty_print=pretty_print)
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
        if nodeName_ == 'Country':
            obj_ = Country.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Country.append(obj_)
            obj_.original_tagname_ = 'Country'
# end class ArrayOfCountry


class Country(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Code=None, Name=None, IsoCode=None, StateRequired=None, PostCodeRequired=None, PostCodeRegex=None, InternationalCallingNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Code = Code
        self.Code_nsprefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = None
        self.IsoCode = IsoCode
        self.IsoCode_nsprefix_ = None
        self.StateRequired = StateRequired
        self.StateRequired_nsprefix_ = None
        self.PostCodeRequired = PostCodeRequired
        self.PostCodeRequired_nsprefix_ = None
        self.PostCodeRegex = PostCodeRegex
        self.PostCodeRegex_nsprefix_ = None
        self.InternationalCallingNumber = InternationalCallingNumber
        self.InternationalCallingNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Country)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Country.subclass:
            return Country.subclass(*args_, **kwargs_)
        else:
            return Country(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Code(self):
        return self.Code
    def set_Code(self, Code):
        self.Code = Code
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def get_IsoCode(self):
        return self.IsoCode
    def set_IsoCode(self, IsoCode):
        self.IsoCode = IsoCode
    def get_StateRequired(self):
        return self.StateRequired
    def set_StateRequired(self, StateRequired):
        self.StateRequired = StateRequired
    def get_PostCodeRequired(self):
        return self.PostCodeRequired
    def set_PostCodeRequired(self, PostCodeRequired):
        self.PostCodeRequired = PostCodeRequired
    def get_PostCodeRegex(self):
        return self.PostCodeRegex
    def set_PostCodeRegex(self, PostCodeRegex):
        self.PostCodeRegex = PostCodeRegex
    def get_InternationalCallingNumber(self):
        return self.InternationalCallingNumber
    def set_InternationalCallingNumber(self, InternationalCallingNumber):
        self.InternationalCallingNumber = InternationalCallingNumber
    def hasContent_(self):
        if (
            self.Code is not None or
            self.Name is not None or
            self.IsoCode is not None or
            self.StateRequired is not None or
            self.PostCodeRequired is not None or
            self.PostCodeRegex is not None or
            self.InternationalCallingNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Country', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Country')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Country':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Country')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Country', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Country'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Country', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Code is not None:
            namespaceprefix_ = self.Code_nsprefix_ + ':' if (UseCapturedNS_ and self.Code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCode>%s</%sCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Code), input_name='Code')), namespaceprefix_ , eol_))
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName>%s</%sName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name), input_name='Name')), namespaceprefix_ , eol_))
        if self.IsoCode is not None:
            namespaceprefix_ = self.IsoCode_nsprefix_ + ':' if (UseCapturedNS_ and self.IsoCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIsoCode>%s</%sIsoCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IsoCode), input_name='IsoCode')), namespaceprefix_ , eol_))
        if self.StateRequired is not None:
            namespaceprefix_ = self.StateRequired_nsprefix_ + ':' if (UseCapturedNS_ and self.StateRequired_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStateRequired>%s</%sStateRequired>%s' % (namespaceprefix_ , self.gds_format_boolean(self.StateRequired, input_name='StateRequired'), namespaceprefix_ , eol_))
        if self.PostCodeRequired is not None:
            namespaceprefix_ = self.PostCodeRequired_nsprefix_ + ':' if (UseCapturedNS_ and self.PostCodeRequired_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPostCodeRequired>%s</%sPostCodeRequired>%s' % (namespaceprefix_ , self.gds_format_boolean(self.PostCodeRequired, input_name='PostCodeRequired'), namespaceprefix_ , eol_))
        if self.PostCodeRegex is not None:
            namespaceprefix_ = self.PostCodeRegex_nsprefix_ + ':' if (UseCapturedNS_ and self.PostCodeRegex_nsprefix_) else ''
            self.PostCodeRegex.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PostCodeRegex', pretty_print=pretty_print)
        if self.InternationalCallingNumber is not None:
            namespaceprefix_ = self.InternationalCallingNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.InternationalCallingNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sInternationalCallingNumber>%s</%sInternationalCallingNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.InternationalCallingNumber), input_name='InternationalCallingNumber')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Code':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Code')
            value_ = self.gds_validate_string(value_, node, 'Code')
            self.Code = value_
            self.Code_nsprefix_ = child_.prefix
        elif nodeName_ == 'Name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Name')
            value_ = self.gds_validate_string(value_, node, 'Name')
            self.Name = value_
            self.Name_nsprefix_ = child_.prefix
        elif nodeName_ == 'IsoCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IsoCode')
            value_ = self.gds_validate_string(value_, node, 'IsoCode')
            self.IsoCode = value_
            self.IsoCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'StateRequired':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'StateRequired')
            ival_ = self.gds_validate_boolean(ival_, node, 'StateRequired')
            self.StateRequired = ival_
            self.StateRequired_nsprefix_ = child_.prefix
        elif nodeName_ == 'PostCodeRequired':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'PostCodeRequired')
            ival_ = self.gds_validate_boolean(ival_, node, 'PostCodeRequired')
            self.PostCodeRequired = ival_
            self.PostCodeRequired_nsprefix_ = child_.prefix
        elif nodeName_ == 'PostCodeRegex':
            obj_ = ArrayOfstring.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PostCodeRegex = obj_
            obj_.original_tagname_ = 'PostCodeRegex'
        elif nodeName_ == 'InternationalCallingNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'InternationalCallingNumber')
            value_ = self.gds_validate_string(value_, node, 'InternationalCallingNumber')
            self.InternationalCallingNumber = value_
            self.InternationalCallingNumber_nsprefix_ = child_.prefix
# end class Country


class CountryFetchingRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ClientInfo=None, Transaction=None, Code=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ClientInfo = ClientInfo
        self.ClientInfo_nsprefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.Code = Code
        self.Code_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CountryFetchingRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CountryFetchingRequest.subclass:
            return CountryFetchingRequest.subclass(*args_, **kwargs_)
        else:
            return CountryFetchingRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ClientInfo(self):
        return self.ClientInfo
    def set_ClientInfo(self, ClientInfo):
        self.ClientInfo = ClientInfo
    def get_Transaction(self):
        return self.Transaction
    def set_Transaction(self, Transaction):
        self.Transaction = Transaction
    def get_Code(self):
        return self.Code
    def set_Code(self, Code):
        self.Code = Code
    def hasContent_(self):
        if (
            self.ClientInfo is not None or
            self.Transaction is not None or
            self.Code is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CountryFetchingRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CountryFetchingRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CountryFetchingRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CountryFetchingRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CountryFetchingRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CountryFetchingRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CountryFetchingRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ClientInfo is not None:
            namespaceprefix_ = self.ClientInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientInfo_nsprefix_) else ''
            self.ClientInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClientInfo', pretty_print=pretty_print)
        if self.Transaction is not None:
            namespaceprefix_ = self.Transaction_nsprefix_ + ':' if (UseCapturedNS_ and self.Transaction_nsprefix_) else ''
            self.Transaction.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Transaction', pretty_print=pretty_print)
        if self.Code is not None:
            namespaceprefix_ = self.Code_nsprefix_ + ':' if (UseCapturedNS_ and self.Code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCode>%s</%sCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Code), input_name='Code')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ClientInfo':
            obj_ = ClientInfo.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClientInfo = obj_
            obj_.original_tagname_ = 'ClientInfo'
        elif nodeName_ == 'Transaction':
            obj_ = Transaction.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transaction = obj_
            obj_.original_tagname_ = 'Transaction'
        elif nodeName_ == 'Code':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Code')
            value_ = self.gds_validate_string(value_, node, 'Code')
            self.Code = value_
            self.Code_nsprefix_ = child_.prefix
# end class CountryFetchingRequest


class CountryFetchingResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Transaction=None, Notifications=None, HasErrors=None, Country=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.Notifications = Notifications
        self.Notifications_nsprefix_ = None
        self.HasErrors = HasErrors
        self.HasErrors_nsprefix_ = None
        self.Country = Country
        self.Country_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CountryFetchingResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CountryFetchingResponse.subclass:
            return CountryFetchingResponse.subclass(*args_, **kwargs_)
        else:
            return CountryFetchingResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Transaction(self):
        return self.Transaction
    def set_Transaction(self, Transaction):
        self.Transaction = Transaction
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def get_HasErrors(self):
        return self.HasErrors
    def set_HasErrors(self, HasErrors):
        self.HasErrors = HasErrors
    def get_Country(self):
        return self.Country
    def set_Country(self, Country):
        self.Country = Country
    def hasContent_(self):
        if (
            self.Transaction is not None or
            self.Notifications is not None or
            self.HasErrors is not None or
            self.Country is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CountryFetchingResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CountryFetchingResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CountryFetchingResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CountryFetchingResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CountryFetchingResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CountryFetchingResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CountryFetchingResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Transaction is not None:
            namespaceprefix_ = self.Transaction_nsprefix_ + ':' if (UseCapturedNS_ and self.Transaction_nsprefix_) else ''
            self.Transaction.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Transaction', pretty_print=pretty_print)
        if self.Notifications is not None:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            self.Notifications.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.HasErrors is not None:
            namespaceprefix_ = self.HasErrors_nsprefix_ + ':' if (UseCapturedNS_ and self.HasErrors_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHasErrors>%s</%sHasErrors>%s' % (namespaceprefix_ , self.gds_format_boolean(self.HasErrors, input_name='HasErrors'), namespaceprefix_ , eol_))
        if self.Country is not None:
            namespaceprefix_ = self.Country_nsprefix_ + ':' if (UseCapturedNS_ and self.Country_nsprefix_) else ''
            self.Country.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Country', pretty_print=pretty_print)
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
        if nodeName_ == 'Transaction':
            obj_ = Transaction.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transaction = obj_
            obj_.original_tagname_ = 'Transaction'
        elif nodeName_ == 'Notifications':
            obj_ = ArrayOfNotification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications = obj_
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'HasErrors':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'HasErrors')
            ival_ = self.gds_validate_boolean(ival_, node, 'HasErrors')
            self.HasErrors = ival_
            self.HasErrors_nsprefix_ = child_.prefix
        elif nodeName_ == 'Country':
            obj_ = Country.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Country = obj_
            obj_.original_tagname_ = 'Country'
# end class CountryFetchingResponse


class CitiesFetchingRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ClientInfo=None, Transaction=None, CountryCode=None, State=None, NameStartsWith=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ClientInfo = ClientInfo
        self.ClientInfo_nsprefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.CountryCode = CountryCode
        self.CountryCode_nsprefix_ = None
        self.State = State
        self.State_nsprefix_ = None
        self.NameStartsWith = NameStartsWith
        self.NameStartsWith_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CitiesFetchingRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CitiesFetchingRequest.subclass:
            return CitiesFetchingRequest.subclass(*args_, **kwargs_)
        else:
            return CitiesFetchingRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ClientInfo(self):
        return self.ClientInfo
    def set_ClientInfo(self, ClientInfo):
        self.ClientInfo = ClientInfo
    def get_Transaction(self):
        return self.Transaction
    def set_Transaction(self, Transaction):
        self.Transaction = Transaction
    def get_CountryCode(self):
        return self.CountryCode
    def set_CountryCode(self, CountryCode):
        self.CountryCode = CountryCode
    def get_State(self):
        return self.State
    def set_State(self, State):
        self.State = State
    def get_NameStartsWith(self):
        return self.NameStartsWith
    def set_NameStartsWith(self, NameStartsWith):
        self.NameStartsWith = NameStartsWith
    def hasContent_(self):
        if (
            self.ClientInfo is not None or
            self.Transaction is not None or
            self.CountryCode is not None or
            self.State is not None or
            self.NameStartsWith is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CitiesFetchingRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CitiesFetchingRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CitiesFetchingRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CitiesFetchingRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CitiesFetchingRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CitiesFetchingRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CitiesFetchingRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ClientInfo is not None:
            namespaceprefix_ = self.ClientInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientInfo_nsprefix_) else ''
            self.ClientInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClientInfo', pretty_print=pretty_print)
        if self.Transaction is not None:
            namespaceprefix_ = self.Transaction_nsprefix_ + ':' if (UseCapturedNS_ and self.Transaction_nsprefix_) else ''
            self.Transaction.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Transaction', pretty_print=pretty_print)
        if self.CountryCode is not None:
            namespaceprefix_ = self.CountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryCode>%s</%sCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryCode), input_name='CountryCode')), namespaceprefix_ , eol_))
        if self.State is not None:
            namespaceprefix_ = self.State_nsprefix_ + ':' if (UseCapturedNS_ and self.State_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sState>%s</%sState>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.State), input_name='State')), namespaceprefix_ , eol_))
        if self.NameStartsWith is not None:
            namespaceprefix_ = self.NameStartsWith_nsprefix_ + ':' if (UseCapturedNS_ and self.NameStartsWith_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNameStartsWith>%s</%sNameStartsWith>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NameStartsWith), input_name='NameStartsWith')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ClientInfo':
            obj_ = ClientInfo.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClientInfo = obj_
            obj_.original_tagname_ = 'ClientInfo'
        elif nodeName_ == 'Transaction':
            obj_ = Transaction.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transaction = obj_
            obj_.original_tagname_ = 'Transaction'
        elif nodeName_ == 'CountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryCode')
            value_ = self.gds_validate_string(value_, node, 'CountryCode')
            self.CountryCode = value_
            self.CountryCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'State':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'State')
            value_ = self.gds_validate_string(value_, node, 'State')
            self.State = value_
            self.State_nsprefix_ = child_.prefix
        elif nodeName_ == 'NameStartsWith':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NameStartsWith')
            value_ = self.gds_validate_string(value_, node, 'NameStartsWith')
            self.NameStartsWith = value_
            self.NameStartsWith_nsprefix_ = child_.prefix
# end class CitiesFetchingRequest


class CitiesFetchingResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Transaction=None, Notifications=None, HasErrors=None, Cities=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.Notifications = Notifications
        self.Notifications_nsprefix_ = None
        self.HasErrors = HasErrors
        self.HasErrors_nsprefix_ = None
        self.Cities = Cities
        self.Cities_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CitiesFetchingResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CitiesFetchingResponse.subclass:
            return CitiesFetchingResponse.subclass(*args_, **kwargs_)
        else:
            return CitiesFetchingResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Transaction(self):
        return self.Transaction
    def set_Transaction(self, Transaction):
        self.Transaction = Transaction
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def get_HasErrors(self):
        return self.HasErrors
    def set_HasErrors(self, HasErrors):
        self.HasErrors = HasErrors
    def get_Cities(self):
        return self.Cities
    def set_Cities(self, Cities):
        self.Cities = Cities
    def hasContent_(self):
        if (
            self.Transaction is not None or
            self.Notifications is not None or
            self.HasErrors is not None or
            self.Cities is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CitiesFetchingResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CitiesFetchingResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CitiesFetchingResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CitiesFetchingResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CitiesFetchingResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CitiesFetchingResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CitiesFetchingResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Transaction is not None:
            namespaceprefix_ = self.Transaction_nsprefix_ + ':' if (UseCapturedNS_ and self.Transaction_nsprefix_) else ''
            self.Transaction.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Transaction', pretty_print=pretty_print)
        if self.Notifications is not None:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            self.Notifications.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.HasErrors is not None:
            namespaceprefix_ = self.HasErrors_nsprefix_ + ':' if (UseCapturedNS_ and self.HasErrors_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHasErrors>%s</%sHasErrors>%s' % (namespaceprefix_ , self.gds_format_boolean(self.HasErrors, input_name='HasErrors'), namespaceprefix_ , eol_))
        if self.Cities is not None:
            namespaceprefix_ = self.Cities_nsprefix_ + ':' if (UseCapturedNS_ and self.Cities_nsprefix_) else ''
            self.Cities.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Cities', pretty_print=pretty_print)
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
        if nodeName_ == 'Transaction':
            obj_ = Transaction.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transaction = obj_
            obj_.original_tagname_ = 'Transaction'
        elif nodeName_ == 'Notifications':
            obj_ = ArrayOfNotification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications = obj_
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'HasErrors':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'HasErrors')
            ival_ = self.gds_validate_boolean(ival_, node, 'HasErrors')
            self.HasErrors = ival_
            self.HasErrors_nsprefix_ = child_.prefix
        elif nodeName_ == 'Cities':
            obj_ = ArrayOfstring.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Cities = obj_
            obj_.original_tagname_ = 'Cities'
# end class CitiesFetchingResponse


class OfficesFetchingRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ClientInfo=None, Transaction=None, CountryCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ClientInfo = ClientInfo
        self.ClientInfo_nsprefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.CountryCode = CountryCode
        self.CountryCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, OfficesFetchingRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OfficesFetchingRequest.subclass:
            return OfficesFetchingRequest.subclass(*args_, **kwargs_)
        else:
            return OfficesFetchingRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ClientInfo(self):
        return self.ClientInfo
    def set_ClientInfo(self, ClientInfo):
        self.ClientInfo = ClientInfo
    def get_Transaction(self):
        return self.Transaction
    def set_Transaction(self, Transaction):
        self.Transaction = Transaction
    def get_CountryCode(self):
        return self.CountryCode
    def set_CountryCode(self, CountryCode):
        self.CountryCode = CountryCode
    def hasContent_(self):
        if (
            self.ClientInfo is not None or
            self.Transaction is not None or
            self.CountryCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OfficesFetchingRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OfficesFetchingRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'OfficesFetchingRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OfficesFetchingRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='OfficesFetchingRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='OfficesFetchingRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OfficesFetchingRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ClientInfo is not None:
            namespaceprefix_ = self.ClientInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientInfo_nsprefix_) else ''
            self.ClientInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClientInfo', pretty_print=pretty_print)
        if self.Transaction is not None:
            namespaceprefix_ = self.Transaction_nsprefix_ + ':' if (UseCapturedNS_ and self.Transaction_nsprefix_) else ''
            self.Transaction.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Transaction', pretty_print=pretty_print)
        if self.CountryCode is not None:
            namespaceprefix_ = self.CountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryCode>%s</%sCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryCode), input_name='CountryCode')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ClientInfo':
            obj_ = ClientInfo.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClientInfo = obj_
            obj_.original_tagname_ = 'ClientInfo'
        elif nodeName_ == 'Transaction':
            obj_ = Transaction.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transaction = obj_
            obj_.original_tagname_ = 'Transaction'
        elif nodeName_ == 'CountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryCode')
            value_ = self.gds_validate_string(value_, node, 'CountryCode')
            self.CountryCode = value_
            self.CountryCode_nsprefix_ = child_.prefix
# end class OfficesFetchingRequest


class OfficesFetchingResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Transaction=None, Notifications=None, HasErrors=None, Offices=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.Notifications = Notifications
        self.Notifications_nsprefix_ = None
        self.HasErrors = HasErrors
        self.HasErrors_nsprefix_ = None
        self.Offices = Offices
        self.Offices_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, OfficesFetchingResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OfficesFetchingResponse.subclass:
            return OfficesFetchingResponse.subclass(*args_, **kwargs_)
        else:
            return OfficesFetchingResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Transaction(self):
        return self.Transaction
    def set_Transaction(self, Transaction):
        self.Transaction = Transaction
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def get_HasErrors(self):
        return self.HasErrors
    def set_HasErrors(self, HasErrors):
        self.HasErrors = HasErrors
    def get_Offices(self):
        return self.Offices
    def set_Offices(self, Offices):
        self.Offices = Offices
    def hasContent_(self):
        if (
            self.Transaction is not None or
            self.Notifications is not None or
            self.HasErrors is not None or
            self.Offices is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OfficesFetchingResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OfficesFetchingResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'OfficesFetchingResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OfficesFetchingResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='OfficesFetchingResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='OfficesFetchingResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OfficesFetchingResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Transaction is not None:
            namespaceprefix_ = self.Transaction_nsprefix_ + ':' if (UseCapturedNS_ and self.Transaction_nsprefix_) else ''
            self.Transaction.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Transaction', pretty_print=pretty_print)
        if self.Notifications is not None:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            self.Notifications.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.HasErrors is not None:
            namespaceprefix_ = self.HasErrors_nsprefix_ + ':' if (UseCapturedNS_ and self.HasErrors_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHasErrors>%s</%sHasErrors>%s' % (namespaceprefix_ , self.gds_format_boolean(self.HasErrors, input_name='HasErrors'), namespaceprefix_ , eol_))
        if self.Offices is not None:
            namespaceprefix_ = self.Offices_nsprefix_ + ':' if (UseCapturedNS_ and self.Offices_nsprefix_) else ''
            self.Offices.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Offices', pretty_print=pretty_print)
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
        if nodeName_ == 'Transaction':
            obj_ = Transaction.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transaction = obj_
            obj_.original_tagname_ = 'Transaction'
        elif nodeName_ == 'Notifications':
            obj_ = ArrayOfNotification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications = obj_
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'HasErrors':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'HasErrors')
            ival_ = self.gds_validate_boolean(ival_, node, 'HasErrors')
            self.HasErrors = ival_
            self.HasErrors_nsprefix_ = child_.prefix
        elif nodeName_ == 'Offices':
            obj_ = ArrayOfOffice.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Offices = obj_
            obj_.original_tagname_ = 'Offices'
# end class OfficesFetchingResponse


class ArrayOfOffice(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Office=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Office is None:
            self.Office = []
        else:
            self.Office = Office
        self.Office_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfOffice)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfOffice.subclass:
            return ArrayOfOffice.subclass(*args_, **kwargs_)
        else:
            return ArrayOfOffice(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Office(self):
        return self.Office
    def set_Office(self, Office):
        self.Office = Office
    def add_Office(self, value):
        self.Office.append(value)
    def insert_Office_at(self, index, value):
        self.Office.insert(index, value)
    def replace_Office_at(self, index, value):
        self.Office[index] = value
    def hasContent_(self):
        if (
            self.Office
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfOffice', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfOffice')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfOffice':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfOffice')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfOffice', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfOffice'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfOffice', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Office_ in self.Office:
            namespaceprefix_ = self.Office_nsprefix_ + ':' if (UseCapturedNS_ and self.Office_nsprefix_) else ''
            Office_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Office', pretty_print=pretty_print)
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
        if nodeName_ == 'Office':
            obj_ = Office.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Office.append(obj_)
            obj_.original_tagname_ = 'Office'
# end class ArrayOfOffice


class Office(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Entity=None, EntityDescription=None, OfficeType=None, Address=None, Telephone=None, WorkingDays=None, WorkingHours=None, Longtitude=None, Latitude=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Entity = Entity
        self.Entity_nsprefix_ = None
        self.EntityDescription = EntityDescription
        self.EntityDescription_nsprefix_ = None
        self.OfficeType = OfficeType
        self.OfficeType_nsprefix_ = None
        self.Address = Address
        self.Address_nsprefix_ = None
        self.Telephone = Telephone
        self.Telephone_nsprefix_ = None
        self.WorkingDays = WorkingDays
        self.WorkingDays_nsprefix_ = None
        self.WorkingHours = WorkingHours
        self.WorkingHours_nsprefix_ = None
        self.Longtitude = Longtitude
        self.Longtitude_nsprefix_ = None
        self.Latitude = Latitude
        self.Latitude_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Office)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Office.subclass:
            return Office.subclass(*args_, **kwargs_)
        else:
            return Office(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Entity(self):
        return self.Entity
    def set_Entity(self, Entity):
        self.Entity = Entity
    def get_EntityDescription(self):
        return self.EntityDescription
    def set_EntityDescription(self, EntityDescription):
        self.EntityDescription = EntityDescription
    def get_OfficeType(self):
        return self.OfficeType
    def set_OfficeType(self, OfficeType):
        self.OfficeType = OfficeType
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_Telephone(self):
        return self.Telephone
    def set_Telephone(self, Telephone):
        self.Telephone = Telephone
    def get_WorkingDays(self):
        return self.WorkingDays
    def set_WorkingDays(self, WorkingDays):
        self.WorkingDays = WorkingDays
    def get_WorkingHours(self):
        return self.WorkingHours
    def set_WorkingHours(self, WorkingHours):
        self.WorkingHours = WorkingHours
    def get_Longtitude(self):
        return self.Longtitude
    def set_Longtitude(self, Longtitude):
        self.Longtitude = Longtitude
    def get_Latitude(self):
        return self.Latitude
    def set_Latitude(self, Latitude):
        self.Latitude = Latitude
    def hasContent_(self):
        if (
            self.Entity is not None or
            self.EntityDescription is not None or
            self.OfficeType is not None or
            self.Address is not None or
            self.Telephone is not None or
            self.WorkingDays is not None or
            self.WorkingHours is not None or
            self.Longtitude is not None or
            self.Latitude is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Office', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Office')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Office':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Office')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Office', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Office'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Office', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Entity is not None:
            namespaceprefix_ = self.Entity_nsprefix_ + ':' if (UseCapturedNS_ and self.Entity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEntity>%s</%sEntity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Entity), input_name='Entity')), namespaceprefix_ , eol_))
        if self.EntityDescription is not None:
            namespaceprefix_ = self.EntityDescription_nsprefix_ + ':' if (UseCapturedNS_ and self.EntityDescription_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEntityDescription>%s</%sEntityDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EntityDescription), input_name='EntityDescription')), namespaceprefix_ , eol_))
        if self.OfficeType is not None:
            namespaceprefix_ = self.OfficeType_nsprefix_ + ':' if (UseCapturedNS_ and self.OfficeType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOfficeType>%s</%sOfficeType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OfficeType), input_name='OfficeType')), namespaceprefix_ , eol_))
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.Telephone is not None:
            namespaceprefix_ = self.Telephone_nsprefix_ + ':' if (UseCapturedNS_ and self.Telephone_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTelephone>%s</%sTelephone>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Telephone), input_name='Telephone')), namespaceprefix_ , eol_))
        if self.WorkingDays is not None:
            namespaceprefix_ = self.WorkingDays_nsprefix_ + ':' if (UseCapturedNS_ and self.WorkingDays_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWorkingDays>%s</%sWorkingDays>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WorkingDays), input_name='WorkingDays')), namespaceprefix_ , eol_))
        if self.WorkingHours is not None:
            namespaceprefix_ = self.WorkingHours_nsprefix_ + ':' if (UseCapturedNS_ and self.WorkingHours_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWorkingHours>%s</%sWorkingHours>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WorkingHours), input_name='WorkingHours')), namespaceprefix_ , eol_))
        if self.Longtitude is not None:
            namespaceprefix_ = self.Longtitude_nsprefix_ + ':' if (UseCapturedNS_ and self.Longtitude_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLongtitude>%s</%sLongtitude>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Longtitude, input_name='Longtitude'), namespaceprefix_ , eol_))
        if self.Latitude is not None:
            namespaceprefix_ = self.Latitude_nsprefix_ + ':' if (UseCapturedNS_ and self.Latitude_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLatitude>%s</%sLatitude>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Latitude, input_name='Latitude'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Entity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Entity')
            value_ = self.gds_validate_string(value_, node, 'Entity')
            self.Entity = value_
            self.Entity_nsprefix_ = child_.prefix
        elif nodeName_ == 'EntityDescription':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EntityDescription')
            value_ = self.gds_validate_string(value_, node, 'EntityDescription')
            self.EntityDescription = value_
            self.EntityDescription_nsprefix_ = child_.prefix
        elif nodeName_ == 'OfficeType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OfficeType')
            value_ = self.gds_validate_string(value_, node, 'OfficeType')
            self.OfficeType = value_
            self.OfficeType_nsprefix_ = child_.prefix
        elif nodeName_ == 'Address':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'Telephone':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Telephone')
            value_ = self.gds_validate_string(value_, node, 'Telephone')
            self.Telephone = value_
            self.Telephone_nsprefix_ = child_.prefix
        elif nodeName_ == 'WorkingDays':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WorkingDays')
            value_ = self.gds_validate_string(value_, node, 'WorkingDays')
            self.WorkingDays = value_
            self.WorkingDays_nsprefix_ = child_.prefix
        elif nodeName_ == 'WorkingHours':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WorkingHours')
            value_ = self.gds_validate_string(value_, node, 'WorkingHours')
            self.WorkingHours = value_
            self.WorkingHours_nsprefix_ = child_.prefix
        elif nodeName_ == 'Longtitude' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Longtitude')
            fval_ = self.gds_validate_decimal(fval_, node, 'Longtitude')
            self.Longtitude = fval_
            self.Longtitude_nsprefix_ = child_.prefix
        elif nodeName_ == 'Latitude' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Latitude')
            fval_ = self.gds_validate_decimal(fval_, node, 'Latitude')
            self.Latitude = fval_
            self.Latitude_nsprefix_ = child_.prefix
# end class Office


class StatesFetchingRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ClientInfo=None, Transaction=None, CountryCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ClientInfo = ClientInfo
        self.ClientInfo_nsprefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.CountryCode = CountryCode
        self.CountryCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, StatesFetchingRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if StatesFetchingRequest.subclass:
            return StatesFetchingRequest.subclass(*args_, **kwargs_)
        else:
            return StatesFetchingRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ClientInfo(self):
        return self.ClientInfo
    def set_ClientInfo(self, ClientInfo):
        self.ClientInfo = ClientInfo
    def get_Transaction(self):
        return self.Transaction
    def set_Transaction(self, Transaction):
        self.Transaction = Transaction
    def get_CountryCode(self):
        return self.CountryCode
    def set_CountryCode(self, CountryCode):
        self.CountryCode = CountryCode
    def hasContent_(self):
        if (
            self.ClientInfo is not None or
            self.Transaction is not None or
            self.CountryCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='StatesFetchingRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('StatesFetchingRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'StatesFetchingRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='StatesFetchingRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='StatesFetchingRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='StatesFetchingRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='StatesFetchingRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ClientInfo is not None:
            namespaceprefix_ = self.ClientInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientInfo_nsprefix_) else ''
            self.ClientInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClientInfo', pretty_print=pretty_print)
        if self.Transaction is not None:
            namespaceprefix_ = self.Transaction_nsprefix_ + ':' if (UseCapturedNS_ and self.Transaction_nsprefix_) else ''
            self.Transaction.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Transaction', pretty_print=pretty_print)
        if self.CountryCode is not None:
            namespaceprefix_ = self.CountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryCode>%s</%sCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryCode), input_name='CountryCode')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ClientInfo':
            obj_ = ClientInfo.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClientInfo = obj_
            obj_.original_tagname_ = 'ClientInfo'
        elif nodeName_ == 'Transaction':
            obj_ = Transaction.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transaction = obj_
            obj_.original_tagname_ = 'Transaction'
        elif nodeName_ == 'CountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryCode')
            value_ = self.gds_validate_string(value_, node, 'CountryCode')
            self.CountryCode = value_
            self.CountryCode_nsprefix_ = child_.prefix
# end class StatesFetchingRequest


class StatesFetchingResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Transaction=None, Notifications=None, HasErrors=None, States=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.Notifications = Notifications
        self.Notifications_nsprefix_ = None
        self.HasErrors = HasErrors
        self.HasErrors_nsprefix_ = None
        self.States = States
        self.States_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, StatesFetchingResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if StatesFetchingResponse.subclass:
            return StatesFetchingResponse.subclass(*args_, **kwargs_)
        else:
            return StatesFetchingResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Transaction(self):
        return self.Transaction
    def set_Transaction(self, Transaction):
        self.Transaction = Transaction
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def get_HasErrors(self):
        return self.HasErrors
    def set_HasErrors(self, HasErrors):
        self.HasErrors = HasErrors
    def get_States(self):
        return self.States
    def set_States(self, States):
        self.States = States
    def hasContent_(self):
        if (
            self.Transaction is not None or
            self.Notifications is not None or
            self.HasErrors is not None or
            self.States is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='StatesFetchingResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('StatesFetchingResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'StatesFetchingResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='StatesFetchingResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='StatesFetchingResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='StatesFetchingResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='StatesFetchingResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Transaction is not None:
            namespaceprefix_ = self.Transaction_nsprefix_ + ':' if (UseCapturedNS_ and self.Transaction_nsprefix_) else ''
            self.Transaction.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Transaction', pretty_print=pretty_print)
        if self.Notifications is not None:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            self.Notifications.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.HasErrors is not None:
            namespaceprefix_ = self.HasErrors_nsprefix_ + ':' if (UseCapturedNS_ and self.HasErrors_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHasErrors>%s</%sHasErrors>%s' % (namespaceprefix_ , self.gds_format_boolean(self.HasErrors, input_name='HasErrors'), namespaceprefix_ , eol_))
        if self.States is not None:
            namespaceprefix_ = self.States_nsprefix_ + ':' if (UseCapturedNS_ and self.States_nsprefix_) else ''
            self.States.export(outfile, level, namespaceprefix_, namespacedef_='', name_='States', pretty_print=pretty_print)
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
        if nodeName_ == 'Transaction':
            obj_ = Transaction.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transaction = obj_
            obj_.original_tagname_ = 'Transaction'
        elif nodeName_ == 'Notifications':
            obj_ = ArrayOfNotification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications = obj_
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'HasErrors':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'HasErrors')
            ival_ = self.gds_validate_boolean(ival_, node, 'HasErrors')
            self.HasErrors = ival_
            self.HasErrors_nsprefix_ = child_.prefix
        elif nodeName_ == 'States':
            obj_ = ArrayOfState.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.States = obj_
            obj_.original_tagname_ = 'States'
# end class StatesFetchingResponse


class ArrayOfState(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, State=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if State is None:
            self.State = []
        else:
            self.State = State
        self.State_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfState)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfState.subclass:
            return ArrayOfState.subclass(*args_, **kwargs_)
        else:
            return ArrayOfState(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_State(self):
        return self.State
    def set_State(self, State):
        self.State = State
    def add_State(self, value):
        self.State.append(value)
    def insert_State_at(self, index, value):
        self.State.insert(index, value)
    def replace_State_at(self, index, value):
        self.State[index] = value
    def hasContent_(self):
        if (
            self.State
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfState', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfState')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfState':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfState')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfState', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfState'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfState', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for State_ in self.State:
            namespaceprefix_ = self.State_nsprefix_ + ':' if (UseCapturedNS_ and self.State_nsprefix_) else ''
            State_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='State', pretty_print=pretty_print)
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
        if nodeName_ == 'State':
            obj_ = State.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.State.append(obj_)
            obj_.original_tagname_ = 'State'
# end class ArrayOfState


class State(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Code=None, Name=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Code = Code
        self.Code_nsprefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, State)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if State.subclass:
            return State.subclass(*args_, **kwargs_)
        else:
            return State(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Code(self):
        return self.Code
    def set_Code(self, Code):
        self.Code = Code
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def hasContent_(self):
        if (
            self.Code is not None or
            self.Name is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='State', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('State')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'State':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='State')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='State', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='State'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='State', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Code is not None:
            namespaceprefix_ = self.Code_nsprefix_ + ':' if (UseCapturedNS_ and self.Code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCode>%s</%sCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Code), input_name='Code')), namespaceprefix_ , eol_))
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName>%s</%sName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name), input_name='Name')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Code':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Code')
            value_ = self.gds_validate_string(value_, node, 'Code')
            self.Code = value_
            self.Code_nsprefix_ = child_.prefix
        elif nodeName_ == 'Name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Name')
            value_ = self.gds_validate_string(value_, node, 'Name')
            self.Name = value_
            self.Name_nsprefix_ = child_.prefix
# end class State


class AddressServiceabilityRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ClientInfo=None, Transaction=None, Address=None, ServiceDetails=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ClientInfo = ClientInfo
        self.ClientInfo_nsprefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.Address = Address
        self.Address_nsprefix_ = None
        self.ServiceDetails = ServiceDetails
        self.ServiceDetails_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AddressServiceabilityRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AddressServiceabilityRequest.subclass:
            return AddressServiceabilityRequest.subclass(*args_, **kwargs_)
        else:
            return AddressServiceabilityRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ClientInfo(self):
        return self.ClientInfo
    def set_ClientInfo(self, ClientInfo):
        self.ClientInfo = ClientInfo
    def get_Transaction(self):
        return self.Transaction
    def set_Transaction(self, Transaction):
        self.Transaction = Transaction
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_ServiceDetails(self):
        return self.ServiceDetails
    def set_ServiceDetails(self, ServiceDetails):
        self.ServiceDetails = ServiceDetails
    def hasContent_(self):
        if (
            self.ClientInfo is not None or
            self.Transaction is not None or
            self.Address is not None or
            self.ServiceDetails is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressServiceabilityRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AddressServiceabilityRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AddressServiceabilityRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AddressServiceabilityRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AddressServiceabilityRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AddressServiceabilityRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressServiceabilityRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ClientInfo is not None:
            namespaceprefix_ = self.ClientInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientInfo_nsprefix_) else ''
            self.ClientInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClientInfo', pretty_print=pretty_print)
        if self.Transaction is not None:
            namespaceprefix_ = self.Transaction_nsprefix_ + ':' if (UseCapturedNS_ and self.Transaction_nsprefix_) else ''
            self.Transaction.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Transaction', pretty_print=pretty_print)
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.ServiceDetails is not None:
            namespaceprefix_ = self.ServiceDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceDetails_nsprefix_) else ''
            self.ServiceDetails.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ServiceDetails', pretty_print=pretty_print)
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
        if nodeName_ == 'ClientInfo':
            obj_ = ClientInfo.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClientInfo = obj_
            obj_.original_tagname_ = 'ClientInfo'
        elif nodeName_ == 'Transaction':
            obj_ = Transaction.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transaction = obj_
            obj_.original_tagname_ = 'Transaction'
        elif nodeName_ == 'Address':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'ServiceDetails':
            obj_ = AddressServiceDetails.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ServiceDetails = obj_
            obj_.original_tagname_ = 'ServiceDetails'
# end class AddressServiceabilityRequest


class AddressServiceDetails(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ProductGroup=None, ProductType=None, ServiceMode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ProductGroup = ProductGroup
        self.ProductGroup_nsprefix_ = None
        self.ProductType = ProductType
        self.ProductType_nsprefix_ = None
        self.ServiceMode = ServiceMode
        self.ServiceMode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AddressServiceDetails)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AddressServiceDetails.subclass:
            return AddressServiceDetails.subclass(*args_, **kwargs_)
        else:
            return AddressServiceDetails(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ProductGroup(self):
        return self.ProductGroup
    def set_ProductGroup(self, ProductGroup):
        self.ProductGroup = ProductGroup
    def get_ProductType(self):
        return self.ProductType
    def set_ProductType(self, ProductType):
        self.ProductType = ProductType
    def get_ServiceMode(self):
        return self.ServiceMode
    def set_ServiceMode(self, ServiceMode):
        self.ServiceMode = ServiceMode
    def hasContent_(self):
        if (
            self.ProductGroup is not None or
            self.ProductType is not None or
            self.ServiceMode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressServiceDetails', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AddressServiceDetails')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AddressServiceDetails':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AddressServiceDetails')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AddressServiceDetails', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AddressServiceDetails'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressServiceDetails', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ProductGroup is not None:
            namespaceprefix_ = self.ProductGroup_nsprefix_ + ':' if (UseCapturedNS_ and self.ProductGroup_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProductGroup>%s</%sProductGroup>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ProductGroup), input_name='ProductGroup')), namespaceprefix_ , eol_))
        if self.ProductType is not None:
            namespaceprefix_ = self.ProductType_nsprefix_ + ':' if (UseCapturedNS_ and self.ProductType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProductType>%s</%sProductType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ProductType), input_name='ProductType')), namespaceprefix_ , eol_))
        if self.ServiceMode is not None:
            namespaceprefix_ = self.ServiceMode_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceMode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceMode>%s</%sServiceMode>%s' % (namespaceprefix_ , self.gds_format_integer(self.ServiceMode, input_name='ServiceMode'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ProductGroup':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ProductGroup')
            value_ = self.gds_validate_string(value_, node, 'ProductGroup')
            self.ProductGroup = value_
            self.ProductGroup_nsprefix_ = child_.prefix
        elif nodeName_ == 'ProductType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ProductType')
            value_ = self.gds_validate_string(value_, node, 'ProductType')
            self.ProductType = value_
            self.ProductType_nsprefix_ = child_.prefix
        elif nodeName_ == 'ServiceMode' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'ServiceMode')
            ival_ = self.gds_validate_integer(ival_, node, 'ServiceMode')
            self.ServiceMode = ival_
            self.ServiceMode_nsprefix_ = child_.prefix
# end class AddressServiceDetails


class AddressServiceabilityResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Transaction=None, Notifications=None, HasErrors=None, IsServiced=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.Notifications = Notifications
        self.Notifications_nsprefix_ = None
        self.HasErrors = HasErrors
        self.HasErrors_nsprefix_ = None
        self.IsServiced = IsServiced
        self.IsServiced_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AddressServiceabilityResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AddressServiceabilityResponse.subclass:
            return AddressServiceabilityResponse.subclass(*args_, **kwargs_)
        else:
            return AddressServiceabilityResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Transaction(self):
        return self.Transaction
    def set_Transaction(self, Transaction):
        self.Transaction = Transaction
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def get_HasErrors(self):
        return self.HasErrors
    def set_HasErrors(self, HasErrors):
        self.HasErrors = HasErrors
    def get_IsServiced(self):
        return self.IsServiced
    def set_IsServiced(self, IsServiced):
        self.IsServiced = IsServiced
    def hasContent_(self):
        if (
            self.Transaction is not None or
            self.Notifications is not None or
            self.HasErrors is not None or
            self.IsServiced is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressServiceabilityResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AddressServiceabilityResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AddressServiceabilityResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AddressServiceabilityResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AddressServiceabilityResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AddressServiceabilityResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressServiceabilityResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Transaction is not None:
            namespaceprefix_ = self.Transaction_nsprefix_ + ':' if (UseCapturedNS_ and self.Transaction_nsprefix_) else ''
            self.Transaction.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Transaction', pretty_print=pretty_print)
        if self.Notifications is not None:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            self.Notifications.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.HasErrors is not None:
            namespaceprefix_ = self.HasErrors_nsprefix_ + ':' if (UseCapturedNS_ and self.HasErrors_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHasErrors>%s</%sHasErrors>%s' % (namespaceprefix_ , self.gds_format_boolean(self.HasErrors, input_name='HasErrors'), namespaceprefix_ , eol_))
        if self.IsServiced is not None:
            namespaceprefix_ = self.IsServiced_nsprefix_ + ':' if (UseCapturedNS_ and self.IsServiced_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIsServiced>%s</%sIsServiced>%s' % (namespaceprefix_ , self.gds_format_boolean(self.IsServiced, input_name='IsServiced'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Transaction':
            obj_ = Transaction.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transaction = obj_
            obj_.original_tagname_ = 'Transaction'
        elif nodeName_ == 'Notifications':
            obj_ = ArrayOfNotification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications = obj_
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'HasErrors':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'HasErrors')
            ival_ = self.gds_validate_boolean(ival_, node, 'HasErrors')
            self.HasErrors = ival_
            self.HasErrors_nsprefix_ = child_.prefix
        elif nodeName_ == 'IsServiced':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'IsServiced')
            ival_ = self.gds_validate_boolean(ival_, node, 'IsServiced')
            self.IsServiced = ival_
            self.IsServiced_nsprefix_ = child_.prefix
# end class AddressServiceabilityResponse


class DropOffLocationsFetchingRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ClientInfo=None, Transaction=None, CountryCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ClientInfo = ClientInfo
        self.ClientInfo_nsprefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.CountryCode = CountryCode
        self.CountryCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DropOffLocationsFetchingRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DropOffLocationsFetchingRequest.subclass:
            return DropOffLocationsFetchingRequest.subclass(*args_, **kwargs_)
        else:
            return DropOffLocationsFetchingRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ClientInfo(self):
        return self.ClientInfo
    def set_ClientInfo(self, ClientInfo):
        self.ClientInfo = ClientInfo
    def get_Transaction(self):
        return self.Transaction
    def set_Transaction(self, Transaction):
        self.Transaction = Transaction
    def get_CountryCode(self):
        return self.CountryCode
    def set_CountryCode(self, CountryCode):
        self.CountryCode = CountryCode
    def hasContent_(self):
        if (
            self.ClientInfo is not None or
            self.Transaction is not None or
            self.CountryCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DropOffLocationsFetchingRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DropOffLocationsFetchingRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DropOffLocationsFetchingRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DropOffLocationsFetchingRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DropOffLocationsFetchingRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DropOffLocationsFetchingRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DropOffLocationsFetchingRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ClientInfo is not None:
            namespaceprefix_ = self.ClientInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientInfo_nsprefix_) else ''
            self.ClientInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClientInfo', pretty_print=pretty_print)
        if self.Transaction is not None:
            namespaceprefix_ = self.Transaction_nsprefix_ + ':' if (UseCapturedNS_ and self.Transaction_nsprefix_) else ''
            self.Transaction.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Transaction', pretty_print=pretty_print)
        if self.CountryCode is not None:
            namespaceprefix_ = self.CountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryCode>%s</%sCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryCode), input_name='CountryCode')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ClientInfo':
            obj_ = ClientInfo.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClientInfo = obj_
            obj_.original_tagname_ = 'ClientInfo'
        elif nodeName_ == 'Transaction':
            obj_ = Transaction.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transaction = obj_
            obj_.original_tagname_ = 'Transaction'
        elif nodeName_ == 'CountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryCode')
            value_ = self.gds_validate_string(value_, node, 'CountryCode')
            self.CountryCode = value_
            self.CountryCode_nsprefix_ = child_.prefix
# end class DropOffLocationsFetchingRequest


class DropOffLocationsFetchingResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Transaction=None, Notifications=None, HasErrors=None, Locations=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.Notifications = Notifications
        self.Notifications_nsprefix_ = None
        self.HasErrors = HasErrors
        self.HasErrors_nsprefix_ = None
        self.Locations = Locations
        self.Locations_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DropOffLocationsFetchingResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DropOffLocationsFetchingResponse.subclass:
            return DropOffLocationsFetchingResponse.subclass(*args_, **kwargs_)
        else:
            return DropOffLocationsFetchingResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Transaction(self):
        return self.Transaction
    def set_Transaction(self, Transaction):
        self.Transaction = Transaction
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def get_HasErrors(self):
        return self.HasErrors
    def set_HasErrors(self, HasErrors):
        self.HasErrors = HasErrors
    def get_Locations(self):
        return self.Locations
    def set_Locations(self, Locations):
        self.Locations = Locations
    def hasContent_(self):
        if (
            self.Transaction is not None or
            self.Notifications is not None or
            self.HasErrors is not None or
            self.Locations is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DropOffLocationsFetchingResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DropOffLocationsFetchingResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DropOffLocationsFetchingResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DropOffLocationsFetchingResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DropOffLocationsFetchingResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DropOffLocationsFetchingResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DropOffLocationsFetchingResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Transaction is not None:
            namespaceprefix_ = self.Transaction_nsprefix_ + ':' if (UseCapturedNS_ and self.Transaction_nsprefix_) else ''
            self.Transaction.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Transaction', pretty_print=pretty_print)
        if self.Notifications is not None:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            self.Notifications.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.HasErrors is not None:
            namespaceprefix_ = self.HasErrors_nsprefix_ + ':' if (UseCapturedNS_ and self.HasErrors_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHasErrors>%s</%sHasErrors>%s' % (namespaceprefix_ , self.gds_format_boolean(self.HasErrors, input_name='HasErrors'), namespaceprefix_ , eol_))
        if self.Locations is not None:
            namespaceprefix_ = self.Locations_nsprefix_ + ':' if (UseCapturedNS_ and self.Locations_nsprefix_) else ''
            self.Locations.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Locations', pretty_print=pretty_print)
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
        if nodeName_ == 'Transaction':
            obj_ = Transaction.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Transaction = obj_
            obj_.original_tagname_ = 'Transaction'
        elif nodeName_ == 'Notifications':
            obj_ = ArrayOfNotification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications = obj_
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'HasErrors':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'HasErrors')
            ival_ = self.gds_validate_boolean(ival_, node, 'HasErrors')
            self.HasErrors = ival_
            self.HasErrors_nsprefix_ = child_.prefix
        elif nodeName_ == 'Locations':
            obj_ = ArrayOfDropOffLocation.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Locations = obj_
            obj_.original_tagname_ = 'Locations'
# end class DropOffLocationsFetchingResponse


class ArrayOfDropOffLocation(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DropOffLocation=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if DropOffLocation is None:
            self.DropOffLocation = []
        else:
            self.DropOffLocation = DropOffLocation
        self.DropOffLocation_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfDropOffLocation)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfDropOffLocation.subclass:
            return ArrayOfDropOffLocation.subclass(*args_, **kwargs_)
        else:
            return ArrayOfDropOffLocation(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DropOffLocation(self):
        return self.DropOffLocation
    def set_DropOffLocation(self, DropOffLocation):
        self.DropOffLocation = DropOffLocation
    def add_DropOffLocation(self, value):
        self.DropOffLocation.append(value)
    def insert_DropOffLocation_at(self, index, value):
        self.DropOffLocation.insert(index, value)
    def replace_DropOffLocation_at(self, index, value):
        self.DropOffLocation[index] = value
    def hasContent_(self):
        if (
            self.DropOffLocation
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfDropOffLocation', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfDropOffLocation')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfDropOffLocation':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfDropOffLocation')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfDropOffLocation', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfDropOffLocation'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfDropOffLocation', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for DropOffLocation_ in self.DropOffLocation:
            namespaceprefix_ = self.DropOffLocation_nsprefix_ + ':' if (UseCapturedNS_ and self.DropOffLocation_nsprefix_) else ''
            DropOffLocation_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DropOffLocation', pretty_print=pretty_print)
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
        if nodeName_ == 'DropOffLocation':
            obj_ = DropOffLocation.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DropOffLocation.append(obj_)
            obj_.original_tagname_ = 'DropOffLocation'
# end class ArrayOfDropOffLocation


class DropOffLocation(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ID=None, Description=None, Address=None, Telephone=None, WorkingDays=None, WorkingHours=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ID = ID
        self.ID_nsprefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = None
        self.Address = Address
        self.Address_nsprefix_ = None
        self.Telephone = Telephone
        self.Telephone_nsprefix_ = None
        self.WorkingDays = WorkingDays
        self.WorkingDays_nsprefix_ = None
        self.WorkingHours = WorkingHours
        self.WorkingHours_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DropOffLocation)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DropOffLocation.subclass:
            return DropOffLocation.subclass(*args_, **kwargs_)
        else:
            return DropOffLocation(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ID(self):
        return self.ID
    def set_ID(self, ID):
        self.ID = ID
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_Telephone(self):
        return self.Telephone
    def set_Telephone(self, Telephone):
        self.Telephone = Telephone
    def get_WorkingDays(self):
        return self.WorkingDays
    def set_WorkingDays(self, WorkingDays):
        self.WorkingDays = WorkingDays
    def get_WorkingHours(self):
        return self.WorkingHours
    def set_WorkingHours(self, WorkingHours):
        self.WorkingHours = WorkingHours
    def hasContent_(self):
        if (
            self.ID is not None or
            self.Description is not None or
            self.Address is not None or
            self.Telephone is not None or
            self.WorkingDays is not None or
            self.WorkingHours is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DropOffLocation', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DropOffLocation')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DropOffLocation':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DropOffLocation')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DropOffLocation', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DropOffLocation'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DropOffLocation', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ID is not None:
            namespaceprefix_ = self.ID_nsprefix_ + ':' if (UseCapturedNS_ and self.ID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sID>%s</%sID>%s' % (namespaceprefix_ , self.gds_format_integer(self.ID, input_name='ID'), namespaceprefix_ , eol_))
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.Telephone is not None:
            namespaceprefix_ = self.Telephone_nsprefix_ + ':' if (UseCapturedNS_ and self.Telephone_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTelephone>%s</%sTelephone>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Telephone), input_name='Telephone')), namespaceprefix_ , eol_))
        if self.WorkingDays is not None:
            namespaceprefix_ = self.WorkingDays_nsprefix_ + ':' if (UseCapturedNS_ and self.WorkingDays_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWorkingDays>%s</%sWorkingDays>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WorkingDays), input_name='WorkingDays')), namespaceprefix_ , eol_))
        if self.WorkingHours is not None:
            namespaceprefix_ = self.WorkingHours_nsprefix_ + ':' if (UseCapturedNS_ and self.WorkingHours_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWorkingHours>%s</%sWorkingHours>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WorkingHours), input_name='WorkingHours')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ID' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'ID')
            ival_ = self.gds_validate_integer(ival_, node, 'ID')
            self.ID = ival_
            self.ID_nsprefix_ = child_.prefix
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
        elif nodeName_ == 'Address':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'Telephone':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Telephone')
            value_ = self.gds_validate_string(value_, node, 'Telephone')
            self.Telephone = value_
            self.Telephone_nsprefix_ = child_.prefix
        elif nodeName_ == 'WorkingDays':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WorkingDays')
            value_ = self.gds_validate_string(value_, node, 'WorkingDays')
            self.WorkingDays = value_
            self.WorkingDays_nsprefix_ = child_.prefix
        elif nodeName_ == 'WorkingHours':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WorkingHours')
            value_ = self.gds_validate_string(value_, node, 'WorkingHours')
            self.WorkingHours = value_
            self.WorkingHours_nsprefix_ = child_.prefix
# end class DropOffLocation


class ArrayOfstring(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, string=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if string is None:
            self.string = []
        else:
            self.string = string
        self.string_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfstring)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfstring.subclass:
            return ArrayOfstring.subclass(*args_, **kwargs_)
        else:
            return ArrayOfstring(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_string(self):
        return self.string
    def set_string(self, string):
        self.string = string
    def add_string(self, value):
        self.string.append(value)
    def insert_string_at(self, index, value):
        self.string.insert(index, value)
    def replace_string_at(self, index, value):
        self.string[index] = value
    def hasContent_(self):
        if (
            self.string
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='ArrayOfstring', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfstring')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfstring':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfstring')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfstring', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='tns:', name_='ArrayOfstring'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='ArrayOfstring', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for string_ in self.string:
            namespaceprefix_ = self.string_nsprefix_ + ':' if (UseCapturedNS_ and self.string_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstring>%s</%sstring>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(string_), input_name='string')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'string':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'string')
            value_ = self.gds_validate_string(value_, node, 'string')
            self.string.append(value_)
            self.string_nsprefix_ = child_.prefix
# end class ArrayOfstring


GDSClassesMapping = {
    'Address': Address,
    'AddressServiceDetails': AddressServiceDetails,
    'ArrayOfAddress': ArrayOfAddress,
    'ArrayOfCountry': ArrayOfCountry,
    'ArrayOfDropOffLocation': ArrayOfDropOffLocation,
    'ArrayOfNotification': ArrayOfNotification,
    'ArrayOfOffice': ArrayOfOffice,
    'ArrayOfState': ArrayOfState,
    'ArrayOfstring': ArrayOfstring,
    'ClientInfo': ClientInfo,
    'Country': Country,
    'DropOffLocation': DropOffLocation,
    'Notification': Notification,
    'Office': Office,
    'State': State,
    'Transaction': Transaction,
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
        rootTag = 'AddressValidationRequest'
        rootClass = AddressValidationRequest
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
        rootTag = 'AddressValidationRequest'
        rootClass = AddressValidationRequest
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
        rootTag = 'AddressValidationRequest'
        rootClass = AddressValidationRequest
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:tns="http://ws.aramex.net/ShippingAPI/v1/"')
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
        rootTag = 'AddressValidationRequest'
        rootClass = AddressValidationRequest
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from location import *\n\n')
        sys.stdout.write('import location as model_\n\n')
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
NamespaceToDefMappings_ = {'http://schemas.microsoft.com/2003/10/Serialization/Arrays': [('ArrayOfstring',
                                                                'https://ws.aramex.net/ShippingAPI.V2/Location/Service_1_0.svc?xsd=xsd2',
                                                                'CT')],
 'http://ws.aramex.net/ShippingAPI/v1/': [('ClientInfo',
                                           './schemas/location.xsd',
                                           'CT'),
                                          ('Transaction',
                                           './schemas/location.xsd',
                                           'CT'),
                                          ('Address',
                                           './schemas/location.xsd',
                                           'CT'),
                                          ('ArrayOfNotification',
                                           './schemas/location.xsd',
                                           'CT'),
                                          ('Notification',
                                           './schemas/location.xsd',
                                           'CT'),
                                          ('ArrayOfAddress',
                                           './schemas/location.xsd',
                                           'CT'),
                                          ('ArrayOfCountry',
                                           './schemas/location.xsd',
                                           'CT'),
                                          ('Country',
                                           './schemas/location.xsd',
                                           'CT'),
                                          ('ArrayOfOffice',
                                           './schemas/location.xsd',
                                           'CT'),
                                          ('Office',
                                           './schemas/location.xsd',
                                           'CT'),
                                          ('ArrayOfState',
                                           './schemas/location.xsd',
                                           'CT'),
                                          ('State',
                                           './schemas/location.xsd',
                                           'CT'),
                                          ('AddressServiceDetails',
                                           './schemas/location.xsd',
                                           'CT'),
                                          ('ArrayOfDropOffLocation',
                                           './schemas/location.xsd',
                                           'CT'),
                                          ('DropOffLocation',
                                           './schemas/location.xsd',
                                           'CT')]}

__all__ = [
    "Address",
    "AddressServiceDetails",
    "AddressServiceabilityRequest",
    "AddressServiceabilityResponse",
    "AddressValidationRequest",
    "AddressValidationResponse",
    "ArrayOfAddress",
    "ArrayOfCountry",
    "ArrayOfDropOffLocation",
    "ArrayOfNotification",
    "ArrayOfOffice",
    "ArrayOfState",
    "ArrayOfstring",
    "CitiesFetchingRequest",
    "CitiesFetchingResponse",
    "ClientInfo",
    "CountriesFetchingRequest",
    "CountriesFetchingResponse",
    "Country",
    "CountryFetchingRequest",
    "CountryFetchingResponse",
    "DropOffLocation",
    "DropOffLocationsFetchingRequest",
    "DropOffLocationsFetchingResponse",
    "Notification",
    "Office",
    "OfficesFetchingRequest",
    "OfficesFetchingResponse",
    "State",
    "StatesFetchingRequest",
    "StatesFetchingResponse",
    "Transaction"
]
