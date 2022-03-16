#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Thu Feb 11 08:51:15 2021 by generateDS.py version 2.37.15.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './aramex_lib/tracking.py')
#
# Command line arguments:
#   ./schemas/tracking.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/karrio-carriers/.venv/karrio-carriers/bin/generateDS --no-namespace-defs -o "./aramex_lib/tracking.py" ./schemas/tracking.xsd
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


class ClientInfo1(GeneratedsSuper):
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
                CurrentSubclassModule_, ClientInfo1)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ClientInfo1.subclass:
            return ClientInfo1.subclass(*args_, **kwargs_)
        else:
            return ClientInfo1(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ClientInfo1', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ClientInfo1')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ClientInfo1':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ClientInfo1')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ClientInfo1', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ClientInfo1'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ClientInfo1', fromsubclass_=False, pretty_print=True):
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
# end class ClientInfo1


class Transaction2(GeneratedsSuper):
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
                CurrentSubclassModule_, Transaction2)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Transaction2.subclass:
            return Transaction2.subclass(*args_, **kwargs_)
        else:
            return Transaction2(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Transaction2', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Transaction2')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Transaction2':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Transaction2')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Transaction2', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Transaction2'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Transaction2', fromsubclass_=False, pretty_print=True):
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
# end class Transaction2


class ArrayOfNotification3(GeneratedsSuper):
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
                CurrentSubclassModule_, ArrayOfNotification3)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfNotification3.subclass:
            return ArrayOfNotification3.subclass(*args_, **kwargs_)
        else:
            return ArrayOfNotification3(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfNotification3', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfNotification3')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfNotification3':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfNotification3')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfNotification3', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfNotification3'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfNotification3', fromsubclass_=False, pretty_print=True):
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
            obj_ = Notification4.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notification.append(obj_)
            obj_.original_tagname_ = 'Notification'
# end class ArrayOfNotification3


class Notification4(GeneratedsSuper):
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
                CurrentSubclassModule_, Notification4)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Notification4.subclass:
            return Notification4.subclass(*args_, **kwargs_)
        else:
            return Notification4(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Notification4', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Notification4')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Notification4':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Notification4')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Notification4', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Notification4'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Notification4', fromsubclass_=False, pretty_print=True):
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
# end class Notification4


class ArrayOfTrackingResult5(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TrackingResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if TrackingResult is None:
            self.TrackingResult = []
        else:
            self.TrackingResult = TrackingResult
        self.TrackingResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfTrackingResult5)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfTrackingResult5.subclass:
            return ArrayOfTrackingResult5.subclass(*args_, **kwargs_)
        else:
            return ArrayOfTrackingResult5(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_TrackingResult(self):
        return self.TrackingResult
    def set_TrackingResult(self, TrackingResult):
        self.TrackingResult = TrackingResult
    def add_TrackingResult(self, value):
        self.TrackingResult.append(value)
    def insert_TrackingResult_at(self, index, value):
        self.TrackingResult.insert(index, value)
    def replace_TrackingResult_at(self, index, value):
        self.TrackingResult[index] = value
    def hasContent_(self):
        if (
            self.TrackingResult
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfTrackingResult5', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfTrackingResult5')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfTrackingResult5':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfTrackingResult5')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfTrackingResult5', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfTrackingResult5'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfTrackingResult5', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for TrackingResult_ in self.TrackingResult:
            namespaceprefix_ = self.TrackingResult_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackingResult_nsprefix_) else ''
            TrackingResult_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TrackingResult', pretty_print=pretty_print)
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
        if nodeName_ == 'TrackingResult':
            obj_ = TrackingResult6.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TrackingResult.append(obj_)
            obj_.original_tagname_ = 'TrackingResult'
# end class ArrayOfTrackingResult5


class TrackingResult6(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WaybillNumber=None, UpdateCode=None, UpdateDescription=None, UpdateDateTime=None, UpdateLocation=None, Comments=None, ProblemCode=None, GrossWeight=None, ChargeableWeight=None, WeightUnit=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.WaybillNumber = WaybillNumber
        self.WaybillNumber_nsprefix_ = None
        self.UpdateCode = UpdateCode
        self.UpdateCode_nsprefix_ = None
        self.UpdateDescription = UpdateDescription
        self.UpdateDescription_nsprefix_ = None
        if isinstance(UpdateDateTime, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(UpdateDateTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = UpdateDateTime
        self.UpdateDateTime = initvalue_
        self.UpdateDateTime_nsprefix_ = None
        self.UpdateLocation = UpdateLocation
        self.UpdateLocation_nsprefix_ = None
        self.Comments = Comments
        self.Comments_nsprefix_ = None
        self.ProblemCode = ProblemCode
        self.ProblemCode_nsprefix_ = None
        self.GrossWeight = GrossWeight
        self.GrossWeight_nsprefix_ = None
        self.ChargeableWeight = ChargeableWeight
        self.ChargeableWeight_nsprefix_ = None
        self.WeightUnit = WeightUnit
        self.WeightUnit_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TrackingResult6)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TrackingResult6.subclass:
            return TrackingResult6.subclass(*args_, **kwargs_)
        else:
            return TrackingResult6(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_WaybillNumber(self):
        return self.WaybillNumber
    def set_WaybillNumber(self, WaybillNumber):
        self.WaybillNumber = WaybillNumber
    def get_UpdateCode(self):
        return self.UpdateCode
    def set_UpdateCode(self, UpdateCode):
        self.UpdateCode = UpdateCode
    def get_UpdateDescription(self):
        return self.UpdateDescription
    def set_UpdateDescription(self, UpdateDescription):
        self.UpdateDescription = UpdateDescription
    def get_UpdateDateTime(self):
        return self.UpdateDateTime
    def set_UpdateDateTime(self, UpdateDateTime):
        self.UpdateDateTime = UpdateDateTime
    def get_UpdateLocation(self):
        return self.UpdateLocation
    def set_UpdateLocation(self, UpdateLocation):
        self.UpdateLocation = UpdateLocation
    def get_Comments(self):
        return self.Comments
    def set_Comments(self, Comments):
        self.Comments = Comments
    def get_ProblemCode(self):
        return self.ProblemCode
    def set_ProblemCode(self, ProblemCode):
        self.ProblemCode = ProblemCode
    def get_GrossWeight(self):
        return self.GrossWeight
    def set_GrossWeight(self, GrossWeight):
        self.GrossWeight = GrossWeight
    def get_ChargeableWeight(self):
        return self.ChargeableWeight
    def set_ChargeableWeight(self, ChargeableWeight):
        self.ChargeableWeight = ChargeableWeight
    def get_WeightUnit(self):
        return self.WeightUnit
    def set_WeightUnit(self, WeightUnit):
        self.WeightUnit = WeightUnit
    def hasContent_(self):
        if (
            self.WaybillNumber is not None or
            self.UpdateCode is not None or
            self.UpdateDescription is not None or
            self.UpdateDateTime is not None or
            self.UpdateLocation is not None or
            self.Comments is not None or
            self.ProblemCode is not None or
            self.GrossWeight is not None or
            self.ChargeableWeight is not None or
            self.WeightUnit is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackingResult6', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TrackingResult6')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TrackingResult6':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TrackingResult6')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TrackingResult6', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TrackingResult6'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackingResult6', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.WaybillNumber is not None:
            namespaceprefix_ = self.WaybillNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.WaybillNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWaybillNumber>%s</%sWaybillNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WaybillNumber), input_name='WaybillNumber')), namespaceprefix_ , eol_))
        if self.UpdateCode is not None:
            namespaceprefix_ = self.UpdateCode_nsprefix_ + ':' if (UseCapturedNS_ and self.UpdateCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUpdateCode>%s</%sUpdateCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UpdateCode), input_name='UpdateCode')), namespaceprefix_ , eol_))
        if self.UpdateDescription is not None:
            namespaceprefix_ = self.UpdateDescription_nsprefix_ + ':' if (UseCapturedNS_ and self.UpdateDescription_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUpdateDescription>%s</%sUpdateDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UpdateDescription), input_name='UpdateDescription')), namespaceprefix_ , eol_))
        if self.UpdateDateTime is not None:
            namespaceprefix_ = self.UpdateDateTime_nsprefix_ + ':' if (UseCapturedNS_ and self.UpdateDateTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUpdateDateTime>%s</%sUpdateDateTime>%s' % (namespaceprefix_ , self.gds_format_datetime(self.UpdateDateTime, input_name='UpdateDateTime'), namespaceprefix_ , eol_))
        if self.UpdateLocation is not None:
            namespaceprefix_ = self.UpdateLocation_nsprefix_ + ':' if (UseCapturedNS_ and self.UpdateLocation_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUpdateLocation>%s</%sUpdateLocation>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UpdateLocation), input_name='UpdateLocation')), namespaceprefix_ , eol_))
        if self.Comments is not None:
            namespaceprefix_ = self.Comments_nsprefix_ + ':' if (UseCapturedNS_ and self.Comments_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sComments>%s</%sComments>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Comments), input_name='Comments')), namespaceprefix_ , eol_))
        if self.ProblemCode is not None:
            namespaceprefix_ = self.ProblemCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ProblemCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProblemCode>%s</%sProblemCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ProblemCode), input_name='ProblemCode')), namespaceprefix_ , eol_))
        if self.GrossWeight is not None:
            namespaceprefix_ = self.GrossWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.GrossWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGrossWeight>%s</%sGrossWeight>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GrossWeight), input_name='GrossWeight')), namespaceprefix_ , eol_))
        if self.ChargeableWeight is not None:
            namespaceprefix_ = self.ChargeableWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.ChargeableWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChargeableWeight>%s</%sChargeableWeight>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChargeableWeight), input_name='ChargeableWeight')), namespaceprefix_ , eol_))
        if self.WeightUnit is not None:
            namespaceprefix_ = self.WeightUnit_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightUnit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeightUnit>%s</%sWeightUnit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WeightUnit), input_name='WeightUnit')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'WaybillNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WaybillNumber')
            value_ = self.gds_validate_string(value_, node, 'WaybillNumber')
            self.WaybillNumber = value_
            self.WaybillNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'UpdateCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UpdateCode')
            value_ = self.gds_validate_string(value_, node, 'UpdateCode')
            self.UpdateCode = value_
            self.UpdateCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'UpdateDescription':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UpdateDescription')
            value_ = self.gds_validate_string(value_, node, 'UpdateDescription')
            self.UpdateDescription = value_
            self.UpdateDescription_nsprefix_ = child_.prefix
        elif nodeName_ == 'UpdateDateTime':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.UpdateDateTime = dval_
            self.UpdateDateTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'UpdateLocation':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UpdateLocation')
            value_ = self.gds_validate_string(value_, node, 'UpdateLocation')
            self.UpdateLocation = value_
            self.UpdateLocation_nsprefix_ = child_.prefix
        elif nodeName_ == 'Comments':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Comments')
            value_ = self.gds_validate_string(value_, node, 'Comments')
            self.Comments = value_
            self.Comments_nsprefix_ = child_.prefix
        elif nodeName_ == 'ProblemCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ProblemCode')
            value_ = self.gds_validate_string(value_, node, 'ProblemCode')
            self.ProblemCode = value_
            self.ProblemCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'GrossWeight':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GrossWeight')
            value_ = self.gds_validate_string(value_, node, 'GrossWeight')
            self.GrossWeight = value_
            self.GrossWeight_nsprefix_ = child_.prefix
        elif nodeName_ == 'ChargeableWeight':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChargeableWeight')
            value_ = self.gds_validate_string(value_, node, 'ChargeableWeight')
            self.ChargeableWeight = value_
            self.ChargeableWeight_nsprefix_ = child_.prefix
        elif nodeName_ == 'WeightUnit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WeightUnit')
            value_ = self.gds_validate_string(value_, node, 'WeightUnit')
            self.WeightUnit = value_
            self.WeightUnit_nsprefix_ = child_.prefix
# end class TrackingResult6


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


class ArrayOfKeyValueOfstringArrayOfTrackingResultmFAkxlpY(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, KeyValueOfstringArrayOfTrackingResultmFAkxlpY=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if KeyValueOfstringArrayOfTrackingResultmFAkxlpY is None:
            self.KeyValueOfstringArrayOfTrackingResultmFAkxlpY = []
        else:
            self.KeyValueOfstringArrayOfTrackingResultmFAkxlpY = KeyValueOfstringArrayOfTrackingResultmFAkxlpY
        self.KeyValueOfstringArrayOfTrackingResultmFAkxlpY_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfKeyValueOfstringArrayOfTrackingResultmFAkxlpY)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfKeyValueOfstringArrayOfTrackingResultmFAkxlpY.subclass:
            return ArrayOfKeyValueOfstringArrayOfTrackingResultmFAkxlpY.subclass(*args_, **kwargs_)
        else:
            return ArrayOfKeyValueOfstringArrayOfTrackingResultmFAkxlpY(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_KeyValueOfstringArrayOfTrackingResultmFAkxlpY(self):
        return self.KeyValueOfstringArrayOfTrackingResultmFAkxlpY
    def set_KeyValueOfstringArrayOfTrackingResultmFAkxlpY(self, KeyValueOfstringArrayOfTrackingResultmFAkxlpY):
        self.KeyValueOfstringArrayOfTrackingResultmFAkxlpY = KeyValueOfstringArrayOfTrackingResultmFAkxlpY
    def add_KeyValueOfstringArrayOfTrackingResultmFAkxlpY(self, value):
        self.KeyValueOfstringArrayOfTrackingResultmFAkxlpY.append(value)
    def insert_KeyValueOfstringArrayOfTrackingResultmFAkxlpY_at(self, index, value):
        self.KeyValueOfstringArrayOfTrackingResultmFAkxlpY.insert(index, value)
    def replace_KeyValueOfstringArrayOfTrackingResultmFAkxlpY_at(self, index, value):
        self.KeyValueOfstringArrayOfTrackingResultmFAkxlpY[index] = value
    def hasContent_(self):
        if (
            self.KeyValueOfstringArrayOfTrackingResultmFAkxlpY
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='ArrayOfKeyValueOfstringArrayOfTrackingResultmFAkxlpY', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfKeyValueOfstringArrayOfTrackingResultmFAkxlpY')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfKeyValueOfstringArrayOfTrackingResultmFAkxlpY':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfKeyValueOfstringArrayOfTrackingResultmFAkxlpY')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfKeyValueOfstringArrayOfTrackingResultmFAkxlpY', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='tns:', name_='ArrayOfKeyValueOfstringArrayOfTrackingResultmFAkxlpY'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='ArrayOfKeyValueOfstringArrayOfTrackingResultmFAkxlpY', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for KeyValueOfstringArrayOfTrackingResultmFAkxlpY_ in self.KeyValueOfstringArrayOfTrackingResultmFAkxlpY:
            namespaceprefix_ = self.KeyValueOfstringArrayOfTrackingResultmFAkxlpY_nsprefix_ + ':' if (UseCapturedNS_ and self.KeyValueOfstringArrayOfTrackingResultmFAkxlpY_nsprefix_) else ''
            KeyValueOfstringArrayOfTrackingResultmFAkxlpY_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='KeyValueOfstringArrayOfTrackingResultmFAkxlpY', pretty_print=pretty_print)
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
        if nodeName_ == 'KeyValueOfstringArrayOfTrackingResultmFAkxlpY':
            obj_ = KeyValueOfstringArrayOfTrackingResultmFAkxlpYType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.KeyValueOfstringArrayOfTrackingResultmFAkxlpY.append(obj_)
            obj_.original_tagname_ = 'KeyValueOfstringArrayOfTrackingResultmFAkxlpY'
# end class ArrayOfKeyValueOfstringArrayOfTrackingResultmFAkxlpY


class ShipmentTrackingRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ClientInfo=None, Transaction=None, Shipments=None, GetLastTrackingUpdateOnly=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ClientInfo = ClientInfo
        self.ClientInfo_nsprefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.Shipments = Shipments
        self.Shipments_nsprefix_ = None
        self.GetLastTrackingUpdateOnly = GetLastTrackingUpdateOnly
        self.GetLastTrackingUpdateOnly_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentTrackingRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentTrackingRequest.subclass:
            return ShipmentTrackingRequest.subclass(*args_, **kwargs_)
        else:
            return ShipmentTrackingRequest(*args_, **kwargs_)
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
    def get_Shipments(self):
        return self.Shipments
    def set_Shipments(self, Shipments):
        self.Shipments = Shipments
    def get_GetLastTrackingUpdateOnly(self):
        return self.GetLastTrackingUpdateOnly
    def set_GetLastTrackingUpdateOnly(self, GetLastTrackingUpdateOnly):
        self.GetLastTrackingUpdateOnly = GetLastTrackingUpdateOnly
    def hasContent_(self):
        if (
            self.ClientInfo is not None or
            self.Transaction is not None or
            self.Shipments is not None or
            self.GetLastTrackingUpdateOnly is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='ShipmentTrackingRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentTrackingRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentTrackingRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentTrackingRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentTrackingRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='tns:', name_='ShipmentTrackingRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='ShipmentTrackingRequest', fromsubclass_=False, pretty_print=True):
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
        if self.Shipments is not None:
            namespaceprefix_ = self.Shipments_nsprefix_ + ':' if (UseCapturedNS_ and self.Shipments_nsprefix_) else ''
            self.Shipments.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Shipments', pretty_print=pretty_print)
        if self.GetLastTrackingUpdateOnly is not None:
            namespaceprefix_ = self.GetLastTrackingUpdateOnly_nsprefix_ + ':' if (UseCapturedNS_ and self.GetLastTrackingUpdateOnly_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetLastTrackingUpdateOnly>%s</%sGetLastTrackingUpdateOnly>%s' % (namespaceprefix_ , self.gds_format_boolean(self.GetLastTrackingUpdateOnly, input_name='GetLastTrackingUpdateOnly'), namespaceprefix_ , eol_))
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
        elif nodeName_ == 'Shipments':
            obj_ = ArrayOfstring.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Shipments = obj_
            obj_.original_tagname_ = 'Shipments'
        elif nodeName_ == 'GetLastTrackingUpdateOnly':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'GetLastTrackingUpdateOnly')
            ival_ = self.gds_validate_boolean(ival_, node, 'GetLastTrackingUpdateOnly')
            self.GetLastTrackingUpdateOnly = ival_
            self.GetLastTrackingUpdateOnly_nsprefix_ = child_.prefix
# end class ShipmentTrackingRequest


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
    def export(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='ClientInfo', pretty_print=True):
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
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='tns:', name_='ClientInfo'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='ClientInfo', fromsubclass_=False, pretty_print=True):
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
    def export(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='Transaction', pretty_print=True):
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
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='tns:', name_='Transaction'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='Transaction', fromsubclass_=False, pretty_print=True):
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


class ShipmentTrackingResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Transaction=None, Notifications=None, HasErrors=None, TrackingResults=None, NonExistingWaybills=None, gds_collector_=None, **kwargs_):
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
        self.TrackingResults = TrackingResults
        self.TrackingResults_nsprefix_ = None
        self.NonExistingWaybills = NonExistingWaybills
        self.NonExistingWaybills_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentTrackingResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentTrackingResponse.subclass:
            return ShipmentTrackingResponse.subclass(*args_, **kwargs_)
        else:
            return ShipmentTrackingResponse(*args_, **kwargs_)
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
    def get_TrackingResults(self):
        return self.TrackingResults
    def set_TrackingResults(self, TrackingResults):
        self.TrackingResults = TrackingResults
    def get_NonExistingWaybills(self):
        return self.NonExistingWaybills
    def set_NonExistingWaybills(self, NonExistingWaybills):
        self.NonExistingWaybills = NonExistingWaybills
    def hasContent_(self):
        if (
            self.Transaction is not None or
            self.Notifications is not None or
            self.HasErrors is not None or
            self.TrackingResults is not None or
            self.NonExistingWaybills is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='ShipmentTrackingResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentTrackingResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentTrackingResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentTrackingResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentTrackingResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='tns:', name_='ShipmentTrackingResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='ShipmentTrackingResponse', fromsubclass_=False, pretty_print=True):
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
        if self.TrackingResults is not None:
            namespaceprefix_ = self.TrackingResults_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackingResults_nsprefix_) else ''
            self.TrackingResults.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TrackingResults', pretty_print=pretty_print)
        if self.NonExistingWaybills is not None:
            namespaceprefix_ = self.NonExistingWaybills_nsprefix_ + ':' if (UseCapturedNS_ and self.NonExistingWaybills_nsprefix_) else ''
            self.NonExistingWaybills.export(outfile, level, namespaceprefix_, namespacedef_='', name_='NonExistingWaybills', pretty_print=pretty_print)
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
        elif nodeName_ == 'TrackingResults':
            obj_ = ArrayOfKeyValueOfstringArrayOfTrackingResultmFAkxlpY.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TrackingResults = obj_
            obj_.original_tagname_ = 'TrackingResults'
        elif nodeName_ == 'NonExistingWaybills':
            obj_ = ArrayOfstring.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.NonExistingWaybills = obj_
            obj_.original_tagname_ = 'NonExistingWaybills'
# end class ShipmentTrackingResponse


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
    def export(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='ArrayOfNotification', pretty_print=True):
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
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='tns:', name_='ArrayOfNotification'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='ArrayOfNotification', fromsubclass_=False, pretty_print=True):
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
            obj_ = Notification4.factory(parent_object_=self)
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
    def export(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='Notification', pretty_print=True):
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
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='tns:', name_='Notification'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='Notification', fromsubclass_=False, pretty_print=True):
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


class ArrayOfTrackingResult(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TrackingResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if TrackingResult is None:
            self.TrackingResult = []
        else:
            self.TrackingResult = TrackingResult
        self.TrackingResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfTrackingResult)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfTrackingResult.subclass:
            return ArrayOfTrackingResult.subclass(*args_, **kwargs_)
        else:
            return ArrayOfTrackingResult(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_TrackingResult(self):
        return self.TrackingResult
    def set_TrackingResult(self, TrackingResult):
        self.TrackingResult = TrackingResult
    def add_TrackingResult(self, value):
        self.TrackingResult.append(value)
    def insert_TrackingResult_at(self, index, value):
        self.TrackingResult.insert(index, value)
    def replace_TrackingResult_at(self, index, value):
        self.TrackingResult[index] = value
    def hasContent_(self):
        if (
            self.TrackingResult
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='ArrayOfTrackingResult', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfTrackingResult')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfTrackingResult':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfTrackingResult')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfTrackingResult', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='tns:', name_='ArrayOfTrackingResult'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='ArrayOfTrackingResult', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for TrackingResult_ in self.TrackingResult:
            namespaceprefix_ = self.TrackingResult_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackingResult_nsprefix_) else ''
            TrackingResult_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TrackingResult', pretty_print=pretty_print)
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
        if nodeName_ == 'TrackingResult':
            obj_ = TrackingResult6.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TrackingResult.append(obj_)
            obj_.original_tagname_ = 'TrackingResult'
# end class ArrayOfTrackingResult


class TrackingResult(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WaybillNumber=None, UpdateCode=None, UpdateDescription=None, UpdateDateTime=None, UpdateLocation=None, Comments=None, ProblemCode=None, GrossWeight=None, ChargeableWeight=None, WeightUnit=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.WaybillNumber = WaybillNumber
        self.WaybillNumber_nsprefix_ = None
        self.UpdateCode = UpdateCode
        self.UpdateCode_nsprefix_ = None
        self.UpdateDescription = UpdateDescription
        self.UpdateDescription_nsprefix_ = None
        if isinstance(UpdateDateTime, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(UpdateDateTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = UpdateDateTime
        self.UpdateDateTime = initvalue_
        self.UpdateDateTime_nsprefix_ = None
        self.UpdateLocation = UpdateLocation
        self.UpdateLocation_nsprefix_ = None
        self.Comments = Comments
        self.Comments_nsprefix_ = None
        self.ProblemCode = ProblemCode
        self.ProblemCode_nsprefix_ = None
        self.GrossWeight = GrossWeight
        self.GrossWeight_nsprefix_ = None
        self.ChargeableWeight = ChargeableWeight
        self.ChargeableWeight_nsprefix_ = None
        self.WeightUnit = WeightUnit
        self.WeightUnit_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TrackingResult)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TrackingResult.subclass:
            return TrackingResult.subclass(*args_, **kwargs_)
        else:
            return TrackingResult(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_WaybillNumber(self):
        return self.WaybillNumber
    def set_WaybillNumber(self, WaybillNumber):
        self.WaybillNumber = WaybillNumber
    def get_UpdateCode(self):
        return self.UpdateCode
    def set_UpdateCode(self, UpdateCode):
        self.UpdateCode = UpdateCode
    def get_UpdateDescription(self):
        return self.UpdateDescription
    def set_UpdateDescription(self, UpdateDescription):
        self.UpdateDescription = UpdateDescription
    def get_UpdateDateTime(self):
        return self.UpdateDateTime
    def set_UpdateDateTime(self, UpdateDateTime):
        self.UpdateDateTime = UpdateDateTime
    def get_UpdateLocation(self):
        return self.UpdateLocation
    def set_UpdateLocation(self, UpdateLocation):
        self.UpdateLocation = UpdateLocation
    def get_Comments(self):
        return self.Comments
    def set_Comments(self, Comments):
        self.Comments = Comments
    def get_ProblemCode(self):
        return self.ProblemCode
    def set_ProblemCode(self, ProblemCode):
        self.ProblemCode = ProblemCode
    def get_GrossWeight(self):
        return self.GrossWeight
    def set_GrossWeight(self, GrossWeight):
        self.GrossWeight = GrossWeight
    def get_ChargeableWeight(self):
        return self.ChargeableWeight
    def set_ChargeableWeight(self, ChargeableWeight):
        self.ChargeableWeight = ChargeableWeight
    def get_WeightUnit(self):
        return self.WeightUnit
    def set_WeightUnit(self, WeightUnit):
        self.WeightUnit = WeightUnit
    def hasContent_(self):
        if (
            self.WaybillNumber is not None or
            self.UpdateCode is not None or
            self.UpdateDescription is not None or
            self.UpdateDateTime is not None or
            self.UpdateLocation is not None or
            self.Comments is not None or
            self.ProblemCode is not None or
            self.GrossWeight is not None or
            self.ChargeableWeight is not None or
            self.WeightUnit is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='TrackingResult', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TrackingResult')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TrackingResult':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TrackingResult')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TrackingResult', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='tns:', name_='TrackingResult'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='TrackingResult', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.WaybillNumber is not None:
            namespaceprefix_ = self.WaybillNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.WaybillNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWaybillNumber>%s</%sWaybillNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WaybillNumber), input_name='WaybillNumber')), namespaceprefix_ , eol_))
        if self.UpdateCode is not None:
            namespaceprefix_ = self.UpdateCode_nsprefix_ + ':' if (UseCapturedNS_ and self.UpdateCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUpdateCode>%s</%sUpdateCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UpdateCode), input_name='UpdateCode')), namespaceprefix_ , eol_))
        if self.UpdateDescription is not None:
            namespaceprefix_ = self.UpdateDescription_nsprefix_ + ':' if (UseCapturedNS_ and self.UpdateDescription_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUpdateDescription>%s</%sUpdateDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UpdateDescription), input_name='UpdateDescription')), namespaceprefix_ , eol_))
        if self.UpdateDateTime is not None:
            namespaceprefix_ = self.UpdateDateTime_nsprefix_ + ':' if (UseCapturedNS_ and self.UpdateDateTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUpdateDateTime>%s</%sUpdateDateTime>%s' % (namespaceprefix_ , self.gds_format_datetime(self.UpdateDateTime, input_name='UpdateDateTime'), namespaceprefix_ , eol_))
        if self.UpdateLocation is not None:
            namespaceprefix_ = self.UpdateLocation_nsprefix_ + ':' if (UseCapturedNS_ and self.UpdateLocation_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUpdateLocation>%s</%sUpdateLocation>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UpdateLocation), input_name='UpdateLocation')), namespaceprefix_ , eol_))
        if self.Comments is not None:
            namespaceprefix_ = self.Comments_nsprefix_ + ':' if (UseCapturedNS_ and self.Comments_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sComments>%s</%sComments>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Comments), input_name='Comments')), namespaceprefix_ , eol_))
        if self.ProblemCode is not None:
            namespaceprefix_ = self.ProblemCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ProblemCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProblemCode>%s</%sProblemCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ProblemCode), input_name='ProblemCode')), namespaceprefix_ , eol_))
        if self.GrossWeight is not None:
            namespaceprefix_ = self.GrossWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.GrossWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGrossWeight>%s</%sGrossWeight>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GrossWeight), input_name='GrossWeight')), namespaceprefix_ , eol_))
        if self.ChargeableWeight is not None:
            namespaceprefix_ = self.ChargeableWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.ChargeableWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChargeableWeight>%s</%sChargeableWeight>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChargeableWeight), input_name='ChargeableWeight')), namespaceprefix_ , eol_))
        if self.WeightUnit is not None:
            namespaceprefix_ = self.WeightUnit_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightUnit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeightUnit>%s</%sWeightUnit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WeightUnit), input_name='WeightUnit')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'WaybillNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WaybillNumber')
            value_ = self.gds_validate_string(value_, node, 'WaybillNumber')
            self.WaybillNumber = value_
            self.WaybillNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'UpdateCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UpdateCode')
            value_ = self.gds_validate_string(value_, node, 'UpdateCode')
            self.UpdateCode = value_
            self.UpdateCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'UpdateDescription':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UpdateDescription')
            value_ = self.gds_validate_string(value_, node, 'UpdateDescription')
            self.UpdateDescription = value_
            self.UpdateDescription_nsprefix_ = child_.prefix
        elif nodeName_ == 'UpdateDateTime':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.UpdateDateTime = dval_
            self.UpdateDateTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'UpdateLocation':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UpdateLocation')
            value_ = self.gds_validate_string(value_, node, 'UpdateLocation')
            self.UpdateLocation = value_
            self.UpdateLocation_nsprefix_ = child_.prefix
        elif nodeName_ == 'Comments':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Comments')
            value_ = self.gds_validate_string(value_, node, 'Comments')
            self.Comments = value_
            self.Comments_nsprefix_ = child_.prefix
        elif nodeName_ == 'ProblemCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ProblemCode')
            value_ = self.gds_validate_string(value_, node, 'ProblemCode')
            self.ProblemCode = value_
            self.ProblemCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'GrossWeight':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GrossWeight')
            value_ = self.gds_validate_string(value_, node, 'GrossWeight')
            self.GrossWeight = value_
            self.GrossWeight_nsprefix_ = child_.prefix
        elif nodeName_ == 'ChargeableWeight':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChargeableWeight')
            value_ = self.gds_validate_string(value_, node, 'ChargeableWeight')
            self.ChargeableWeight = value_
            self.ChargeableWeight_nsprefix_ = child_.prefix
        elif nodeName_ == 'WeightUnit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WeightUnit')
            value_ = self.gds_validate_string(value_, node, 'WeightUnit')
            self.WeightUnit = value_
            self.WeightUnit_nsprefix_ = child_.prefix
# end class TrackingResult


class PickupTrackingRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ClientInfo=None, Transaction=None, Reference=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ClientInfo = ClientInfo
        self.ClientInfo_nsprefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.Reference = Reference
        self.Reference_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PickupTrackingRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PickupTrackingRequest.subclass:
            return PickupTrackingRequest.subclass(*args_, **kwargs_)
        else:
            return PickupTrackingRequest(*args_, **kwargs_)
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
    def get_Reference(self):
        return self.Reference
    def set_Reference(self, Reference):
        self.Reference = Reference
    def hasContent_(self):
        if (
            self.ClientInfo is not None or
            self.Transaction is not None or
            self.Reference is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='PickupTrackingRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PickupTrackingRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PickupTrackingRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PickupTrackingRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PickupTrackingRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='tns:', name_='PickupTrackingRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='PickupTrackingRequest', fromsubclass_=False, pretty_print=True):
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
        if self.Reference is not None:
            namespaceprefix_ = self.Reference_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference>%s</%sReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference), input_name='Reference')), namespaceprefix_ , eol_))
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
        elif nodeName_ == 'Reference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Reference')
            value_ = self.gds_validate_string(value_, node, 'Reference')
            self.Reference = value_
            self.Reference_nsprefix_ = child_.prefix
# end class PickupTrackingRequest


class PickupTrackingResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Transaction=None, Notifications=None, HasErrors=None, Entity=None, Reference=None, CollectionDate=None, PickupDate=None, LastStatus=None, LastStatusDescription=None, CollectedWaybills=None, gds_collector_=None, **kwargs_):
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
        self.Entity = Entity
        self.Entity_nsprefix_ = None
        self.Reference = Reference
        self.Reference_nsprefix_ = None
        if isinstance(CollectionDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(CollectionDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = CollectionDate
        self.CollectionDate = initvalue_
        self.CollectionDate_nsprefix_ = None
        if isinstance(PickupDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(PickupDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = PickupDate
        self.PickupDate = initvalue_
        self.PickupDate_nsprefix_ = None
        self.LastStatus = LastStatus
        self.LastStatus_nsprefix_ = None
        self.LastStatusDescription = LastStatusDescription
        self.LastStatusDescription_nsprefix_ = None
        self.CollectedWaybills = CollectedWaybills
        self.CollectedWaybills_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PickupTrackingResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PickupTrackingResponse.subclass:
            return PickupTrackingResponse.subclass(*args_, **kwargs_)
        else:
            return PickupTrackingResponse(*args_, **kwargs_)
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
    def get_Entity(self):
        return self.Entity
    def set_Entity(self, Entity):
        self.Entity = Entity
    def get_Reference(self):
        return self.Reference
    def set_Reference(self, Reference):
        self.Reference = Reference
    def get_CollectionDate(self):
        return self.CollectionDate
    def set_CollectionDate(self, CollectionDate):
        self.CollectionDate = CollectionDate
    def get_PickupDate(self):
        return self.PickupDate
    def set_PickupDate(self, PickupDate):
        self.PickupDate = PickupDate
    def get_LastStatus(self):
        return self.LastStatus
    def set_LastStatus(self, LastStatus):
        self.LastStatus = LastStatus
    def get_LastStatusDescription(self):
        return self.LastStatusDescription
    def set_LastStatusDescription(self, LastStatusDescription):
        self.LastStatusDescription = LastStatusDescription
    def get_CollectedWaybills(self):
        return self.CollectedWaybills
    def set_CollectedWaybills(self, CollectedWaybills):
        self.CollectedWaybills = CollectedWaybills
    def hasContent_(self):
        if (
            self.Transaction is not None or
            self.Notifications is not None or
            self.HasErrors is not None or
            self.Entity is not None or
            self.Reference is not None or
            self.CollectionDate is not None or
            self.PickupDate is not None or
            self.LastStatus is not None or
            self.LastStatusDescription is not None or
            self.CollectedWaybills is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='PickupTrackingResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PickupTrackingResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PickupTrackingResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PickupTrackingResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PickupTrackingResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='tns:', name_='PickupTrackingResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='tns:', namespacedef_='', name_='PickupTrackingResponse', fromsubclass_=False, pretty_print=True):
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
        if self.Entity is not None:
            namespaceprefix_ = self.Entity_nsprefix_ + ':' if (UseCapturedNS_ and self.Entity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEntity>%s</%sEntity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Entity), input_name='Entity')), namespaceprefix_ , eol_))
        if self.Reference is not None:
            namespaceprefix_ = self.Reference_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference>%s</%sReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference), input_name='Reference')), namespaceprefix_ , eol_))
        if self.CollectionDate is not None:
            namespaceprefix_ = self.CollectionDate_nsprefix_ + ':' if (UseCapturedNS_ and self.CollectionDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCollectionDate>%s</%sCollectionDate>%s' % (namespaceprefix_ , self.gds_format_datetime(self.CollectionDate, input_name='CollectionDate'), namespaceprefix_ , eol_))
        if self.PickupDate is not None:
            namespaceprefix_ = self.PickupDate_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupDate>%s</%sPickupDate>%s' % (namespaceprefix_ , self.gds_format_datetime(self.PickupDate, input_name='PickupDate'), namespaceprefix_ , eol_))
        if self.LastStatus is not None:
            namespaceprefix_ = self.LastStatus_nsprefix_ + ':' if (UseCapturedNS_ and self.LastStatus_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLastStatus>%s</%sLastStatus>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LastStatus), input_name='LastStatus')), namespaceprefix_ , eol_))
        if self.LastStatusDescription is not None:
            namespaceprefix_ = self.LastStatusDescription_nsprefix_ + ':' if (UseCapturedNS_ and self.LastStatusDescription_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLastStatusDescription>%s</%sLastStatusDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LastStatusDescription), input_name='LastStatusDescription')), namespaceprefix_ , eol_))
        if self.CollectedWaybills is not None:
            namespaceprefix_ = self.CollectedWaybills_nsprefix_ + ':' if (UseCapturedNS_ and self.CollectedWaybills_nsprefix_) else ''
            self.CollectedWaybills.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CollectedWaybills', pretty_print=pretty_print)
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
        elif nodeName_ == 'Entity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Entity')
            value_ = self.gds_validate_string(value_, node, 'Entity')
            self.Entity = value_
            self.Entity_nsprefix_ = child_.prefix
        elif nodeName_ == 'Reference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Reference')
            value_ = self.gds_validate_string(value_, node, 'Reference')
            self.Reference = value_
            self.Reference_nsprefix_ = child_.prefix
        elif nodeName_ == 'CollectionDate':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.CollectionDate = dval_
            self.CollectionDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'PickupDate':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.PickupDate = dval_
            self.PickupDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'LastStatus':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LastStatus')
            value_ = self.gds_validate_string(value_, node, 'LastStatus')
            self.LastStatus = value_
            self.LastStatus_nsprefix_ = child_.prefix
        elif nodeName_ == 'LastStatusDescription':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LastStatusDescription')
            value_ = self.gds_validate_string(value_, node, 'LastStatusDescription')
            self.LastStatusDescription = value_
            self.LastStatusDescription_nsprefix_ = child_.prefix
        elif nodeName_ == 'CollectedWaybills':
            obj_ = ArrayOfstring.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CollectedWaybills = obj_
            obj_.original_tagname_ = 'CollectedWaybills'
# end class PickupTrackingResponse


class KeyValueOfstringArrayOfTrackingResultmFAkxlpYType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Key=None, Value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Key = Key
        self.Key_nsprefix_ = None
        self.Value = Value
        self.Value_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, KeyValueOfstringArrayOfTrackingResultmFAkxlpYType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if KeyValueOfstringArrayOfTrackingResultmFAkxlpYType.subclass:
            return KeyValueOfstringArrayOfTrackingResultmFAkxlpYType.subclass(*args_, **kwargs_)
        else:
            return KeyValueOfstringArrayOfTrackingResultmFAkxlpYType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Key(self):
        return self.Key
    def set_Key(self, Key):
        self.Key = Key
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def hasContent_(self):
        if (
            self.Key is not None or
            self.Value is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='KeyValueOfstringArrayOfTrackingResultmFAkxlpYType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('KeyValueOfstringArrayOfTrackingResultmFAkxlpYType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'KeyValueOfstringArrayOfTrackingResultmFAkxlpYType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='KeyValueOfstringArrayOfTrackingResultmFAkxlpYType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='KeyValueOfstringArrayOfTrackingResultmFAkxlpYType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='KeyValueOfstringArrayOfTrackingResultmFAkxlpYType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='KeyValueOfstringArrayOfTrackingResultmFAkxlpYType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Key is not None:
            namespaceprefix_ = self.Key_nsprefix_ + ':' if (UseCapturedNS_ and self.Key_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sKey>%s</%sKey>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Key), input_name='Key')), namespaceprefix_ , eol_))
        if self.Value is not None:
            namespaceprefix_ = self.Value_nsprefix_ + ':' if (UseCapturedNS_ and self.Value_nsprefix_) else ''
            self.Value.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Value', pretty_print=pretty_print)
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
        elif nodeName_ == 'Value':
            obj_ = ArrayOfTrackingResult5.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Value = obj_
            obj_.original_tagname_ = 'Value'
# end class KeyValueOfstringArrayOfTrackingResultmFAkxlpYType


GDSClassesMapping = {
    'ArrayOfKeyValueOfstringArrayOfTrackingResultmFAkxlpY': ArrayOfKeyValueOfstringArrayOfTrackingResultmFAkxlpY,
    'ArrayOfNotification': ArrayOfNotification,
    'ArrayOfNotification': ArrayOfNotification3,
    'ArrayOfTrackingResult': ArrayOfTrackingResult,
    'ArrayOfTrackingResult': ArrayOfTrackingResult5,
    'ArrayOfstring': ArrayOfstring,
    'ClientInfo': ClientInfo,
    'ClientInfo': ClientInfo1,
    'Notification': Notification,
    'Notification': Notification4,
    'TrackingResult': TrackingResult,
    'TrackingResult': TrackingResult6,
    'Transaction': Transaction,
    'Transaction': Transaction2,
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
        rootTag = 'ClientInfo1'
        rootClass = ClientInfo1
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
        rootTag = 'ClientInfo1'
        rootClass = ClientInfo1
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
        rootTag = 'ClientInfo1'
        rootClass = ClientInfo1
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
        rootTag = 'ClientInfo1'
        rootClass = ClientInfo1
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from tracking import *\n\n')
        sys.stdout.write('import tracking as model_\n\n')
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
    "{http://ws.aramex.net/ShippingAPI/v1/}ArrayOfNotification": "ArrayOfNotification3",
    "{http://ws.aramex.net/ShippingAPI/v1/}ArrayOfTrackingResult": "ArrayOfTrackingResult5",
    "{http://ws.aramex.net/ShippingAPI/v1/}ClientInfo": "ClientInfo1",
    "{http://ws.aramex.net/ShippingAPI/v1/}Notification": "Notification4",
    "{http://ws.aramex.net/ShippingAPI/v1/}TrackingResult": "TrackingResult6",
    "{http://ws.aramex.net/ShippingAPI/v1/}Transaction": "Transaction2",
}

#
# Mapping of namespaces to types defined in them
# and the file in which each is defined.
# simpleTypes are marked "ST" and complexTypes "CT".
NamespaceToDefMappings_ = {'http://schemas.microsoft.com/2003/10/Serialization/Arrays': [('ArrayOfstring',
                                                                'https://ws.aramex.net/ShippingAPI.V2/Tracking/Service_1_0.svc?xsd=xsd2',
                                                                'CT'),
                                                               ('ArrayOfKeyValueOfstringArrayOfTrackingResultmFAkxlpY',
                                                                'https://ws.aramex.net/ShippingAPI.V2/Tracking/Service_1_0.svc?xsd=xsd2',
                                                                'CT')],
 'http://ws.aramex.net/ShippingAPI/v1/': [('ClientInfo',
                                           'https://ws.aramex.net/ShippingAPI.V2/Tracking/Service_1_0.svc?xsd=xsd0',
                                           'CT'),
                                          ('Transaction',
                                           'https://ws.aramex.net/ShippingAPI.V2/Tracking/Service_1_0.svc?xsd=xsd0',
                                           'CT'),
                                          ('ArrayOfNotification',
                                           'https://ws.aramex.net/ShippingAPI.V2/Tracking/Service_1_0.svc?xsd=xsd0',
                                           'CT'),
                                          ('Notification',
                                           'https://ws.aramex.net/ShippingAPI.V2/Tracking/Service_1_0.svc?xsd=xsd0',
                                           'CT'),
                                          ('ArrayOfTrackingResult',
                                           'https://ws.aramex.net/ShippingAPI.V2/Tracking/Service_1_0.svc?xsd=xsd0',
                                           'CT'),
                                          ('TrackingResult',
                                           'https://ws.aramex.net/ShippingAPI.V2/Tracking/Service_1_0.svc?xsd=xsd0',
                                           'CT'),
                                          ('ClientInfo',
                                           './schemas/tracking.xsd',
                                           'CT'),
                                          ('Transaction',
                                           './schemas/tracking.xsd',
                                           'CT'),
                                          ('ArrayOfNotification',
                                           './schemas/tracking.xsd',
                                           'CT'),
                                          ('Notification',
                                           './schemas/tracking.xsd',
                                           'CT'),
                                          ('ArrayOfTrackingResult',
                                           './schemas/tracking.xsd',
                                           'CT'),
                                          ('TrackingResult',
                                           './schemas/tracking.xsd',
                                           'CT')]}

__all__ = [
    "ArrayOfKeyValueOfstringArrayOfTrackingResultmFAkxlpY",
    "ArrayOfNotification",
    "ArrayOfNotification3",
    "ArrayOfTrackingResult",
    "ArrayOfTrackingResult5",
    "ArrayOfstring",
    "ClientInfo",
    "ClientInfo1",
    "KeyValueOfstringArrayOfTrackingResultmFAkxlpYType",
    "Notification",
    "Notification4",
    "PickupTrackingRequest",
    "PickupTrackingResponse",
    "ShipmentTrackingRequest",
    "ShipmentTrackingResponse",
    "TrackingResult",
    "TrackingResult6",
    "Transaction",
    "Transaction2"
]
