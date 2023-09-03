#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Thu Feb 11 08:51:12 2021 by generateDS.py version 2.37.15.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './aramex_lib/rates.py')
#
# Command line arguments:
#   ./schemas/rates.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/karrio-carriers/.venv/karrio-carriers/bin/generateDS --no-namespace-defs -o "./aramex_lib/rates.py" ./schemas/rates.xsd
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


class RateCalculatorRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ClientInfo=None, Transaction=None, OriginAddress=None, DestinationAddress=None, ShipmentDetails=None, PreferredCurrencyCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ClientInfo = ClientInfo
        self.ClientInfo_nsprefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.OriginAddress = OriginAddress
        self.OriginAddress_nsprefix_ = None
        self.DestinationAddress = DestinationAddress
        self.DestinationAddress_nsprefix_ = None
        self.ShipmentDetails = ShipmentDetails
        self.ShipmentDetails_nsprefix_ = None
        self.PreferredCurrencyCode = PreferredCurrencyCode
        self.PreferredCurrencyCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RateCalculatorRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RateCalculatorRequest.subclass:
            return RateCalculatorRequest.subclass(*args_, **kwargs_)
        else:
            return RateCalculatorRequest(*args_, **kwargs_)
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
    def get_OriginAddress(self):
        return self.OriginAddress
    def set_OriginAddress(self, OriginAddress):
        self.OriginAddress = OriginAddress
    def get_DestinationAddress(self):
        return self.DestinationAddress
    def set_DestinationAddress(self, DestinationAddress):
        self.DestinationAddress = DestinationAddress
    def get_ShipmentDetails(self):
        return self.ShipmentDetails
    def set_ShipmentDetails(self, ShipmentDetails):
        self.ShipmentDetails = ShipmentDetails
    def get_PreferredCurrencyCode(self):
        return self.PreferredCurrencyCode
    def set_PreferredCurrencyCode(self, PreferredCurrencyCode):
        self.PreferredCurrencyCode = PreferredCurrencyCode
    def hasContent_(self):
        if (
            self.ClientInfo is not None or
            self.Transaction is not None or
            self.OriginAddress is not None or
            self.DestinationAddress is not None or
            self.ShipmentDetails is not None or
            self.PreferredCurrencyCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RateCalculatorRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RateCalculatorRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RateCalculatorRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RateCalculatorRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RateCalculatorRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RateCalculatorRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RateCalculatorRequest', fromsubclass_=False, pretty_print=True):
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
        if self.OriginAddress is not None:
            namespaceprefix_ = self.OriginAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.OriginAddress_nsprefix_) else ''
            self.OriginAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='OriginAddress', pretty_print=pretty_print)
        if self.DestinationAddress is not None:
            namespaceprefix_ = self.DestinationAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationAddress_nsprefix_) else ''
            self.DestinationAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DestinationAddress', pretty_print=pretty_print)
        if self.ShipmentDetails is not None:
            namespaceprefix_ = self.ShipmentDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentDetails_nsprefix_) else ''
            self.ShipmentDetails.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentDetails', pretty_print=pretty_print)
        if self.PreferredCurrencyCode is not None:
            namespaceprefix_ = self.PreferredCurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.PreferredCurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPreferredCurrencyCode>%s</%sPreferredCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PreferredCurrencyCode), input_name='PreferredCurrencyCode')), namespaceprefix_ , eol_))
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
        elif nodeName_ == 'OriginAddress':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.OriginAddress = obj_
            obj_.original_tagname_ = 'OriginAddress'
        elif nodeName_ == 'DestinationAddress':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DestinationAddress = obj_
            obj_.original_tagname_ = 'DestinationAddress'
        elif nodeName_ == 'ShipmentDetails':
            obj_ = ShipmentDetails.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentDetails = obj_
            obj_.original_tagname_ = 'ShipmentDetails'
        elif nodeName_ == 'PreferredCurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PreferredCurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'PreferredCurrencyCode')
            self.PreferredCurrencyCode = value_
            self.PreferredCurrencyCode_nsprefix_ = child_.prefix
# end class RateCalculatorRequest


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


class ShipmentDetails(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Dimensions=None, ActualWeight=None, ChargeableWeight=None, DescriptionOfGoods=None, GoodsOriginCountry=None, NumberOfPieces=None, ProductGroup=None, ProductType=None, PaymentType=None, PaymentOptions=None, CustomsValueAmount=None, CashOnDeliveryAmount=None, InsuranceAmount=None, CashAdditionalAmount=None, CashAdditionalAmountDescription=None, CollectAmount=None, Services=None, Items=None, DeliveryInstructions=None, AdditionalProperties=None, ContainsDangerousGoods=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Dimensions = Dimensions
        self.Dimensions_nsprefix_ = None
        self.ActualWeight = ActualWeight
        self.ActualWeight_nsprefix_ = None
        self.ChargeableWeight = ChargeableWeight
        self.ChargeableWeight_nsprefix_ = None
        self.DescriptionOfGoods = DescriptionOfGoods
        self.DescriptionOfGoods_nsprefix_ = None
        self.GoodsOriginCountry = GoodsOriginCountry
        self.GoodsOriginCountry_nsprefix_ = None
        self.NumberOfPieces = NumberOfPieces
        self.NumberOfPieces_nsprefix_ = None
        self.ProductGroup = ProductGroup
        self.ProductGroup_nsprefix_ = None
        self.ProductType = ProductType
        self.ProductType_nsprefix_ = None
        self.PaymentType = PaymentType
        self.PaymentType_nsprefix_ = None
        self.PaymentOptions = PaymentOptions
        self.PaymentOptions_nsprefix_ = None
        self.CustomsValueAmount = CustomsValueAmount
        self.CustomsValueAmount_nsprefix_ = None
        self.CashOnDeliveryAmount = CashOnDeliveryAmount
        self.CashOnDeliveryAmount_nsprefix_ = None
        self.InsuranceAmount = InsuranceAmount
        self.InsuranceAmount_nsprefix_ = None
        self.CashAdditionalAmount = CashAdditionalAmount
        self.CashAdditionalAmount_nsprefix_ = None
        self.CashAdditionalAmountDescription = CashAdditionalAmountDescription
        self.CashAdditionalAmountDescription_nsprefix_ = None
        self.CollectAmount = CollectAmount
        self.CollectAmount_nsprefix_ = None
        self.Services = Services
        self.Services_nsprefix_ = None
        self.Items = Items
        self.Items_nsprefix_ = None
        self.DeliveryInstructions = DeliveryInstructions
        self.DeliveryInstructions_nsprefix_ = None
        self.AdditionalProperties = AdditionalProperties
        self.AdditionalProperties_nsprefix_ = None
        self.ContainsDangerousGoods = ContainsDangerousGoods
        self.ContainsDangerousGoods_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentDetails)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentDetails.subclass:
            return ShipmentDetails.subclass(*args_, **kwargs_)
        else:
            return ShipmentDetails(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Dimensions(self):
        return self.Dimensions
    def set_Dimensions(self, Dimensions):
        self.Dimensions = Dimensions
    def get_ActualWeight(self):
        return self.ActualWeight
    def set_ActualWeight(self, ActualWeight):
        self.ActualWeight = ActualWeight
    def get_ChargeableWeight(self):
        return self.ChargeableWeight
    def set_ChargeableWeight(self, ChargeableWeight):
        self.ChargeableWeight = ChargeableWeight
    def get_DescriptionOfGoods(self):
        return self.DescriptionOfGoods
    def set_DescriptionOfGoods(self, DescriptionOfGoods):
        self.DescriptionOfGoods = DescriptionOfGoods
    def get_GoodsOriginCountry(self):
        return self.GoodsOriginCountry
    def set_GoodsOriginCountry(self, GoodsOriginCountry):
        self.GoodsOriginCountry = GoodsOriginCountry
    def get_NumberOfPieces(self):
        return self.NumberOfPieces
    def set_NumberOfPieces(self, NumberOfPieces):
        self.NumberOfPieces = NumberOfPieces
    def get_ProductGroup(self):
        return self.ProductGroup
    def set_ProductGroup(self, ProductGroup):
        self.ProductGroup = ProductGroup
    def get_ProductType(self):
        return self.ProductType
    def set_ProductType(self, ProductType):
        self.ProductType = ProductType
    def get_PaymentType(self):
        return self.PaymentType
    def set_PaymentType(self, PaymentType):
        self.PaymentType = PaymentType
    def get_PaymentOptions(self):
        return self.PaymentOptions
    def set_PaymentOptions(self, PaymentOptions):
        self.PaymentOptions = PaymentOptions
    def get_CustomsValueAmount(self):
        return self.CustomsValueAmount
    def set_CustomsValueAmount(self, CustomsValueAmount):
        self.CustomsValueAmount = CustomsValueAmount
    def get_CashOnDeliveryAmount(self):
        return self.CashOnDeliveryAmount
    def set_CashOnDeliveryAmount(self, CashOnDeliveryAmount):
        self.CashOnDeliveryAmount = CashOnDeliveryAmount
    def get_InsuranceAmount(self):
        return self.InsuranceAmount
    def set_InsuranceAmount(self, InsuranceAmount):
        self.InsuranceAmount = InsuranceAmount
    def get_CashAdditionalAmount(self):
        return self.CashAdditionalAmount
    def set_CashAdditionalAmount(self, CashAdditionalAmount):
        self.CashAdditionalAmount = CashAdditionalAmount
    def get_CashAdditionalAmountDescription(self):
        return self.CashAdditionalAmountDescription
    def set_CashAdditionalAmountDescription(self, CashAdditionalAmountDescription):
        self.CashAdditionalAmountDescription = CashAdditionalAmountDescription
    def get_CollectAmount(self):
        return self.CollectAmount
    def set_CollectAmount(self, CollectAmount):
        self.CollectAmount = CollectAmount
    def get_Services(self):
        return self.Services
    def set_Services(self, Services):
        self.Services = Services
    def get_Items(self):
        return self.Items
    def set_Items(self, Items):
        self.Items = Items
    def get_DeliveryInstructions(self):
        return self.DeliveryInstructions
    def set_DeliveryInstructions(self, DeliveryInstructions):
        self.DeliveryInstructions = DeliveryInstructions
    def get_AdditionalProperties(self):
        return self.AdditionalProperties
    def set_AdditionalProperties(self, AdditionalProperties):
        self.AdditionalProperties = AdditionalProperties
    def get_ContainsDangerousGoods(self):
        return self.ContainsDangerousGoods
    def set_ContainsDangerousGoods(self, ContainsDangerousGoods):
        self.ContainsDangerousGoods = ContainsDangerousGoods
    def hasContent_(self):
        if (
            self.Dimensions is not None or
            self.ActualWeight is not None or
            self.ChargeableWeight is not None or
            self.DescriptionOfGoods is not None or
            self.GoodsOriginCountry is not None or
            self.NumberOfPieces is not None or
            self.ProductGroup is not None or
            self.ProductType is not None or
            self.PaymentType is not None or
            self.PaymentOptions is not None or
            self.CustomsValueAmount is not None or
            self.CashOnDeliveryAmount is not None or
            self.InsuranceAmount is not None or
            self.CashAdditionalAmount is not None or
            self.CashAdditionalAmountDescription is not None or
            self.CollectAmount is not None or
            self.Services is not None or
            self.Items is not None or
            self.DeliveryInstructions is not None or
            self.AdditionalProperties is not None or
            self.ContainsDangerousGoods is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentDetails', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentDetails')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentDetails':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentDetails')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentDetails', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentDetails'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentDetails', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Dimensions is not None:
            namespaceprefix_ = self.Dimensions_nsprefix_ + ':' if (UseCapturedNS_ and self.Dimensions_nsprefix_) else ''
            self.Dimensions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Dimensions', pretty_print=pretty_print)
        if self.ActualWeight is not None:
            namespaceprefix_ = self.ActualWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.ActualWeight_nsprefix_) else ''
            self.ActualWeight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ActualWeight', pretty_print=pretty_print)
        if self.ChargeableWeight is not None:
            namespaceprefix_ = self.ChargeableWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.ChargeableWeight_nsprefix_) else ''
            self.ChargeableWeight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ChargeableWeight', pretty_print=pretty_print)
        if self.DescriptionOfGoods is not None:
            namespaceprefix_ = self.DescriptionOfGoods_nsprefix_ + ':' if (UseCapturedNS_ and self.DescriptionOfGoods_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescriptionOfGoods>%s</%sDescriptionOfGoods>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DescriptionOfGoods), input_name='DescriptionOfGoods')), namespaceprefix_ , eol_))
        if self.GoodsOriginCountry is not None:
            namespaceprefix_ = self.GoodsOriginCountry_nsprefix_ + ':' if (UseCapturedNS_ and self.GoodsOriginCountry_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGoodsOriginCountry>%s</%sGoodsOriginCountry>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GoodsOriginCountry), input_name='GoodsOriginCountry')), namespaceprefix_ , eol_))
        if self.NumberOfPieces is not None:
            namespaceprefix_ = self.NumberOfPieces_nsprefix_ + ':' if (UseCapturedNS_ and self.NumberOfPieces_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumberOfPieces>%s</%sNumberOfPieces>%s' % (namespaceprefix_ , self.gds_format_integer(self.NumberOfPieces, input_name='NumberOfPieces'), namespaceprefix_ , eol_))
        if self.ProductGroup is not None:
            namespaceprefix_ = self.ProductGroup_nsprefix_ + ':' if (UseCapturedNS_ and self.ProductGroup_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProductGroup>%s</%sProductGroup>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ProductGroup), input_name='ProductGroup')), namespaceprefix_ , eol_))
        if self.ProductType is not None:
            namespaceprefix_ = self.ProductType_nsprefix_ + ':' if (UseCapturedNS_ and self.ProductType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProductType>%s</%sProductType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ProductType), input_name='ProductType')), namespaceprefix_ , eol_))
        if self.PaymentType is not None:
            namespaceprefix_ = self.PaymentType_nsprefix_ + ':' if (UseCapturedNS_ and self.PaymentType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPaymentType>%s</%sPaymentType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PaymentType), input_name='PaymentType')), namespaceprefix_ , eol_))
        if self.PaymentOptions is not None:
            namespaceprefix_ = self.PaymentOptions_nsprefix_ + ':' if (UseCapturedNS_ and self.PaymentOptions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPaymentOptions>%s</%sPaymentOptions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PaymentOptions), input_name='PaymentOptions')), namespaceprefix_ , eol_))
        if self.CustomsValueAmount is not None:
            namespaceprefix_ = self.CustomsValueAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomsValueAmount_nsprefix_) else ''
            self.CustomsValueAmount.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CustomsValueAmount', pretty_print=pretty_print)
        if self.CashOnDeliveryAmount is not None:
            namespaceprefix_ = self.CashOnDeliveryAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.CashOnDeliveryAmount_nsprefix_) else ''
            self.CashOnDeliveryAmount.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CashOnDeliveryAmount', pretty_print=pretty_print)
        if self.InsuranceAmount is not None:
            namespaceprefix_ = self.InsuranceAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.InsuranceAmount_nsprefix_) else ''
            self.InsuranceAmount.export(outfile, level, namespaceprefix_, namespacedef_='', name_='InsuranceAmount', pretty_print=pretty_print)
        if self.CashAdditionalAmount is not None:
            namespaceprefix_ = self.CashAdditionalAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.CashAdditionalAmount_nsprefix_) else ''
            self.CashAdditionalAmount.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CashAdditionalAmount', pretty_print=pretty_print)
        if self.CashAdditionalAmountDescription is not None:
            namespaceprefix_ = self.CashAdditionalAmountDescription_nsprefix_ + ':' if (UseCapturedNS_ and self.CashAdditionalAmountDescription_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCashAdditionalAmountDescription>%s</%sCashAdditionalAmountDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CashAdditionalAmountDescription), input_name='CashAdditionalAmountDescription')), namespaceprefix_ , eol_))
        if self.CollectAmount is not None:
            namespaceprefix_ = self.CollectAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.CollectAmount_nsprefix_) else ''
            self.CollectAmount.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CollectAmount', pretty_print=pretty_print)
        if self.Services is not None:
            namespaceprefix_ = self.Services_nsprefix_ + ':' if (UseCapturedNS_ and self.Services_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServices>%s</%sServices>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Services), input_name='Services')), namespaceprefix_ , eol_))
        if self.Items is not None:
            namespaceprefix_ = self.Items_nsprefix_ + ':' if (UseCapturedNS_ and self.Items_nsprefix_) else ''
            self.Items.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Items', pretty_print=pretty_print)
        if self.DeliveryInstructions is not None:
            namespaceprefix_ = self.DeliveryInstructions_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryInstructions_nsprefix_) else ''
            self.DeliveryInstructions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DeliveryInstructions', pretty_print=pretty_print)
        if self.AdditionalProperties is not None:
            namespaceprefix_ = self.AdditionalProperties_nsprefix_ + ':' if (UseCapturedNS_ and self.AdditionalProperties_nsprefix_) else ''
            self.AdditionalProperties.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AdditionalProperties', pretty_print=pretty_print)
        if self.ContainsDangerousGoods is not None:
            namespaceprefix_ = self.ContainsDangerousGoods_nsprefix_ + ':' if (UseCapturedNS_ and self.ContainsDangerousGoods_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sContainsDangerousGoods>%s</%sContainsDangerousGoods>%s' % (namespaceprefix_ , self.gds_format_boolean(self.ContainsDangerousGoods, input_name='ContainsDangerousGoods'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Dimensions':
            obj_ = Dimensions.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Dimensions = obj_
            obj_.original_tagname_ = 'Dimensions'
        elif nodeName_ == 'ActualWeight':
            obj_ = Weight.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ActualWeight = obj_
            obj_.original_tagname_ = 'ActualWeight'
        elif nodeName_ == 'ChargeableWeight':
            obj_ = Weight.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ChargeableWeight = obj_
            obj_.original_tagname_ = 'ChargeableWeight'
        elif nodeName_ == 'DescriptionOfGoods':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DescriptionOfGoods')
            value_ = self.gds_validate_string(value_, node, 'DescriptionOfGoods')
            self.DescriptionOfGoods = value_
            self.DescriptionOfGoods_nsprefix_ = child_.prefix
        elif nodeName_ == 'GoodsOriginCountry':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GoodsOriginCountry')
            value_ = self.gds_validate_string(value_, node, 'GoodsOriginCountry')
            self.GoodsOriginCountry = value_
            self.GoodsOriginCountry_nsprefix_ = child_.prefix
        elif nodeName_ == 'NumberOfPieces' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'NumberOfPieces')
            ival_ = self.gds_validate_integer(ival_, node, 'NumberOfPieces')
            self.NumberOfPieces = ival_
            self.NumberOfPieces_nsprefix_ = child_.prefix
        elif nodeName_ == 'ProductGroup':
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
        elif nodeName_ == 'PaymentType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PaymentType')
            value_ = self.gds_validate_string(value_, node, 'PaymentType')
            self.PaymentType = value_
            self.PaymentType_nsprefix_ = child_.prefix
        elif nodeName_ == 'PaymentOptions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PaymentOptions')
            value_ = self.gds_validate_string(value_, node, 'PaymentOptions')
            self.PaymentOptions = value_
            self.PaymentOptions_nsprefix_ = child_.prefix
        elif nodeName_ == 'CustomsValueAmount':
            obj_ = Money.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CustomsValueAmount = obj_
            obj_.original_tagname_ = 'CustomsValueAmount'
        elif nodeName_ == 'CashOnDeliveryAmount':
            obj_ = Money.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CashOnDeliveryAmount = obj_
            obj_.original_tagname_ = 'CashOnDeliveryAmount'
        elif nodeName_ == 'InsuranceAmount':
            obj_ = Money.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.InsuranceAmount = obj_
            obj_.original_tagname_ = 'InsuranceAmount'
        elif nodeName_ == 'CashAdditionalAmount':
            obj_ = Money.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CashAdditionalAmount = obj_
            obj_.original_tagname_ = 'CashAdditionalAmount'
        elif nodeName_ == 'CashAdditionalAmountDescription':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CashAdditionalAmountDescription')
            value_ = self.gds_validate_string(value_, node, 'CashAdditionalAmountDescription')
            self.CashAdditionalAmountDescription = value_
            self.CashAdditionalAmountDescription_nsprefix_ = child_.prefix
        elif nodeName_ == 'CollectAmount':
            obj_ = Money.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CollectAmount = obj_
            obj_.original_tagname_ = 'CollectAmount'
        elif nodeName_ == 'Services':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Services')
            value_ = self.gds_validate_string(value_, node, 'Services')
            self.Services = value_
            self.Services_nsprefix_ = child_.prefix
        elif nodeName_ == 'Items':
            obj_ = ArrayOfShipmentItem.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Items = obj_
            obj_.original_tagname_ = 'Items'
        elif nodeName_ == 'DeliveryInstructions':
            obj_ = DeliveryInstructions.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DeliveryInstructions = obj_
            obj_.original_tagname_ = 'DeliveryInstructions'
        elif nodeName_ == 'AdditionalProperties':
            obj_ = ArrayOfAdditionalProperty.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdditionalProperties = obj_
            obj_.original_tagname_ = 'AdditionalProperties'
        elif nodeName_ == 'ContainsDangerousGoods':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'ContainsDangerousGoods')
            ival_ = self.gds_validate_boolean(ival_, node, 'ContainsDangerousGoods')
            self.ContainsDangerousGoods = ival_
            self.ContainsDangerousGoods_nsprefix_ = child_.prefix
# end class ShipmentDetails


class Dimensions(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Length=None, Width=None, Height=None, Unit=None, gds_collector_=None, **kwargs_):
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
        self.Unit = Unit
        self.Unit_nsprefix_ = None
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
    def get_Unit(self):
        return self.Unit
    def set_Unit(self, Unit):
        self.Unit = Unit
    def hasContent_(self):
        if (
            self.Length is not None or
            self.Width is not None or
            self.Height is not None or
            self.Unit is not None
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
            outfile.write('<%sLength>%s</%sLength>%s' % (namespaceprefix_ , self.gds_format_double(self.Length, input_name='Length'), namespaceprefix_ , eol_))
        if self.Width is not None:
            namespaceprefix_ = self.Width_nsprefix_ + ':' if (UseCapturedNS_ and self.Width_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWidth>%s</%sWidth>%s' % (namespaceprefix_ , self.gds_format_double(self.Width, input_name='Width'), namespaceprefix_ , eol_))
        if self.Height is not None:
            namespaceprefix_ = self.Height_nsprefix_ + ':' if (UseCapturedNS_ and self.Height_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHeight>%s</%sHeight>%s' % (namespaceprefix_ , self.gds_format_double(self.Height, input_name='Height'), namespaceprefix_ , eol_))
        if self.Unit is not None:
            namespaceprefix_ = self.Unit_nsprefix_ + ':' if (UseCapturedNS_ and self.Unit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUnit>%s</%sUnit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Unit), input_name='Unit')), namespaceprefix_ , eol_))
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
            fval_ = self.gds_parse_double(sval_, node, 'Length')
            fval_ = self.gds_validate_double(fval_, node, 'Length')
            self.Length = fval_
            self.Length_nsprefix_ = child_.prefix
        elif nodeName_ == 'Width' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'Width')
            fval_ = self.gds_validate_double(fval_, node, 'Width')
            self.Width = fval_
            self.Width_nsprefix_ = child_.prefix
        elif nodeName_ == 'Height' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'Height')
            fval_ = self.gds_validate_double(fval_, node, 'Height')
            self.Height = fval_
            self.Height_nsprefix_ = child_.prefix
        elif nodeName_ == 'Unit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Unit')
            value_ = self.gds_validate_string(value_, node, 'Unit')
            self.Unit = value_
            self.Unit_nsprefix_ = child_.prefix
# end class Dimensions


class Weight(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Unit=None, Value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Unit = Unit
        self.Unit_nsprefix_ = None
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
    def get_Unit(self):
        return self.Unit
    def set_Unit(self, Unit):
        self.Unit = Unit
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def hasContent_(self):
        if (
            self.Unit is not None or
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
        if self.Unit is not None:
            namespaceprefix_ = self.Unit_nsprefix_ + ':' if (UseCapturedNS_ and self.Unit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUnit>%s</%sUnit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Unit), input_name='Unit')), namespaceprefix_ , eol_))
        if self.Value is not None:
            namespaceprefix_ = self.Value_nsprefix_ + ':' if (UseCapturedNS_ and self.Value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sValue>%s</%sValue>%s' % (namespaceprefix_ , self.gds_format_double(self.Value, input_name='Value'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Unit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Unit')
            value_ = self.gds_validate_string(value_, node, 'Unit')
            self.Unit = value_
            self.Unit_nsprefix_ = child_.prefix
        elif nodeName_ == 'Value' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'Value')
            fval_ = self.gds_validate_double(fval_, node, 'Value')
            self.Value = fval_
            self.Value_nsprefix_ = child_.prefix
# end class Weight


class Money(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CurrencyCode=None, Value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CurrencyCode = CurrencyCode
        self.CurrencyCode_nsprefix_ = None
        self.Value = Value
        self.Value_nsprefix_ = None
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
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def hasContent_(self):
        if (
            self.CurrencyCode is not None or
            self.Value is not None
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
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.Value is not None:
            namespaceprefix_ = self.Value_nsprefix_ + ':' if (UseCapturedNS_ and self.Value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sValue>%s</%sValue>%s' % (namespaceprefix_ , self.gds_format_double(self.Value, input_name='Value'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'Value' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'Value')
            fval_ = self.gds_validate_double(fval_, node, 'Value')
            self.Value = fval_
            self.Value_nsprefix_ = child_.prefix
# end class Money


class ArrayOfShipmentItem(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ShipmentItem=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if ShipmentItem is None:
            self.ShipmentItem = []
        else:
            self.ShipmentItem = ShipmentItem
        self.ShipmentItem_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfShipmentItem)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfShipmentItem.subclass:
            return ArrayOfShipmentItem.subclass(*args_, **kwargs_)
        else:
            return ArrayOfShipmentItem(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ShipmentItem(self):
        return self.ShipmentItem
    def set_ShipmentItem(self, ShipmentItem):
        self.ShipmentItem = ShipmentItem
    def add_ShipmentItem(self, value):
        self.ShipmentItem.append(value)
    def insert_ShipmentItem_at(self, index, value):
        self.ShipmentItem.insert(index, value)
    def replace_ShipmentItem_at(self, index, value):
        self.ShipmentItem[index] = value
    def hasContent_(self):
        if (
            self.ShipmentItem
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfShipmentItem', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfShipmentItem')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfShipmentItem':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfShipmentItem')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfShipmentItem', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfShipmentItem'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfShipmentItem', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for ShipmentItem_ in self.ShipmentItem:
            namespaceprefix_ = self.ShipmentItem_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentItem_nsprefix_) else ''
            ShipmentItem_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentItem', pretty_print=pretty_print)
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
        if nodeName_ == 'ShipmentItem':
            obj_ = ShipmentItem.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentItem.append(obj_)
            obj_.original_tagname_ = 'ShipmentItem'
# end class ArrayOfShipmentItem


class ShipmentItem(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PackageType=None, Quantity=None, Weight=None, Comments=None, Reference=None, PiecesDimensions=None, CommodityCode=None, GoodsDescription=None, CountryOfOrigin=None, CustomsValue=None, ContainerNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PackageType = PackageType
        self.PackageType_nsprefix_ = None
        self.Quantity = Quantity
        self.Quantity_nsprefix_ = None
        self.Weight = Weight
        self.Weight_nsprefix_ = None
        self.Comments = Comments
        self.Comments_nsprefix_ = None
        self.Reference = Reference
        self.Reference_nsprefix_ = None
        self.PiecesDimensions = PiecesDimensions
        self.PiecesDimensions_nsprefix_ = None
        self.CommodityCode = CommodityCode
        self.CommodityCode_nsprefix_ = None
        self.GoodsDescription = GoodsDescription
        self.GoodsDescription_nsprefix_ = None
        self.CountryOfOrigin = CountryOfOrigin
        self.CountryOfOrigin_nsprefix_ = None
        self.CustomsValue = CustomsValue
        self.CustomsValue_nsprefix_ = None
        self.ContainerNumber = ContainerNumber
        self.ContainerNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentItem)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentItem.subclass:
            return ShipmentItem.subclass(*args_, **kwargs_)
        else:
            return ShipmentItem(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PackageType(self):
        return self.PackageType
    def set_PackageType(self, PackageType):
        self.PackageType = PackageType
    def get_Quantity(self):
        return self.Quantity
    def set_Quantity(self, Quantity):
        self.Quantity = Quantity
    def get_Weight(self):
        return self.Weight
    def set_Weight(self, Weight):
        self.Weight = Weight
    def get_Comments(self):
        return self.Comments
    def set_Comments(self, Comments):
        self.Comments = Comments
    def get_Reference(self):
        return self.Reference
    def set_Reference(self, Reference):
        self.Reference = Reference
    def get_PiecesDimensions(self):
        return self.PiecesDimensions
    def set_PiecesDimensions(self, PiecesDimensions):
        self.PiecesDimensions = PiecesDimensions
    def get_CommodityCode(self):
        return self.CommodityCode
    def set_CommodityCode(self, CommodityCode):
        self.CommodityCode = CommodityCode
    def get_GoodsDescription(self):
        return self.GoodsDescription
    def set_GoodsDescription(self, GoodsDescription):
        self.GoodsDescription = GoodsDescription
    def get_CountryOfOrigin(self):
        return self.CountryOfOrigin
    def set_CountryOfOrigin(self, CountryOfOrigin):
        self.CountryOfOrigin = CountryOfOrigin
    def get_CustomsValue(self):
        return self.CustomsValue
    def set_CustomsValue(self, CustomsValue):
        self.CustomsValue = CustomsValue
    def get_ContainerNumber(self):
        return self.ContainerNumber
    def set_ContainerNumber(self, ContainerNumber):
        self.ContainerNumber = ContainerNumber
    def hasContent_(self):
        if (
            self.PackageType is not None or
            self.Quantity is not None or
            self.Weight is not None or
            self.Comments is not None or
            self.Reference is not None or
            self.PiecesDimensions is not None or
            self.CommodityCode is not None or
            self.GoodsDescription is not None or
            self.CountryOfOrigin is not None or
            self.CustomsValue is not None or
            self.ContainerNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentItem', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentItem')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentItem':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentItem')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentItem', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentItem'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentItem', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PackageType is not None:
            namespaceprefix_ = self.PackageType_nsprefix_ + ':' if (UseCapturedNS_ and self.PackageType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPackageType>%s</%sPackageType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PackageType), input_name='PackageType')), namespaceprefix_ , eol_))
        if self.Quantity is not None:
            namespaceprefix_ = self.Quantity_nsprefix_ + ':' if (UseCapturedNS_ and self.Quantity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sQuantity>%s</%sQuantity>%s' % (namespaceprefix_ , self.gds_format_integer(self.Quantity, input_name='Quantity'), namespaceprefix_ , eol_))
        if self.Weight is not None:
            namespaceprefix_ = self.Weight_nsprefix_ + ':' if (UseCapturedNS_ and self.Weight_nsprefix_) else ''
            self.Weight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Weight', pretty_print=pretty_print)
        if self.Comments is not None:
            namespaceprefix_ = self.Comments_nsprefix_ + ':' if (UseCapturedNS_ and self.Comments_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sComments>%s</%sComments>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Comments), input_name='Comments')), namespaceprefix_ , eol_))
        if self.Reference is not None:
            namespaceprefix_ = self.Reference_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference>%s</%sReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference), input_name='Reference')), namespaceprefix_ , eol_))
        if self.PiecesDimensions is not None:
            namespaceprefix_ = self.PiecesDimensions_nsprefix_ + ':' if (UseCapturedNS_ and self.PiecesDimensions_nsprefix_) else ''
            self.PiecesDimensions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PiecesDimensions', pretty_print=pretty_print)
        if self.CommodityCode is not None:
            namespaceprefix_ = self.CommodityCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CommodityCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCommodityCode>%s</%sCommodityCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CommodityCode), input_name='CommodityCode')), namespaceprefix_ , eol_))
        if self.GoodsDescription is not None:
            namespaceprefix_ = self.GoodsDescription_nsprefix_ + ':' if (UseCapturedNS_ and self.GoodsDescription_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGoodsDescription>%s</%sGoodsDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GoodsDescription), input_name='GoodsDescription')), namespaceprefix_ , eol_))
        if self.CountryOfOrigin is not None:
            namespaceprefix_ = self.CountryOfOrigin_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryOfOrigin_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryOfOrigin>%s</%sCountryOfOrigin>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryOfOrigin), input_name='CountryOfOrigin')), namespaceprefix_ , eol_))
        if self.CustomsValue is not None:
            namespaceprefix_ = self.CustomsValue_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomsValue_nsprefix_) else ''
            self.CustomsValue.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CustomsValue', pretty_print=pretty_print)
        if self.ContainerNumber is not None:
            namespaceprefix_ = self.ContainerNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ContainerNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sContainerNumber>%s</%sContainerNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ContainerNumber), input_name='ContainerNumber')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'PackageType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PackageType')
            value_ = self.gds_validate_string(value_, node, 'PackageType')
            self.PackageType = value_
            self.PackageType_nsprefix_ = child_.prefix
        elif nodeName_ == 'Quantity' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Quantity')
            ival_ = self.gds_validate_integer(ival_, node, 'Quantity')
            self.Quantity = ival_
            self.Quantity_nsprefix_ = child_.prefix
        elif nodeName_ == 'Weight':
            obj_ = Weight.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Weight = obj_
            obj_.original_tagname_ = 'Weight'
        elif nodeName_ == 'Comments':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Comments')
            value_ = self.gds_validate_string(value_, node, 'Comments')
            self.Comments = value_
            self.Comments_nsprefix_ = child_.prefix
        elif nodeName_ == 'Reference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Reference')
            value_ = self.gds_validate_string(value_, node, 'Reference')
            self.Reference = value_
            self.Reference_nsprefix_ = child_.prefix
        elif nodeName_ == 'PiecesDimensions':
            obj_ = ArrayOfDimensions.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PiecesDimensions = obj_
            obj_.original_tagname_ = 'PiecesDimensions'
        elif nodeName_ == 'CommodityCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CommodityCode')
            value_ = self.gds_validate_string(value_, node, 'CommodityCode')
            self.CommodityCode = value_
            self.CommodityCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'GoodsDescription':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GoodsDescription')
            value_ = self.gds_validate_string(value_, node, 'GoodsDescription')
            self.GoodsDescription = value_
            self.GoodsDescription_nsprefix_ = child_.prefix
        elif nodeName_ == 'CountryOfOrigin':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryOfOrigin')
            value_ = self.gds_validate_string(value_, node, 'CountryOfOrigin')
            self.CountryOfOrigin = value_
            self.CountryOfOrigin_nsprefix_ = child_.prefix
        elif nodeName_ == 'CustomsValue':
            obj_ = Money.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CustomsValue = obj_
            obj_.original_tagname_ = 'CustomsValue'
        elif nodeName_ == 'ContainerNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ContainerNumber')
            value_ = self.gds_validate_string(value_, node, 'ContainerNumber')
            self.ContainerNumber = value_
            self.ContainerNumber_nsprefix_ = child_.prefix
# end class ShipmentItem


class ArrayOfDimensions(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Dimensions=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Dimensions is None:
            self.Dimensions = []
        else:
            self.Dimensions = Dimensions
        self.Dimensions_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfDimensions)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfDimensions.subclass:
            return ArrayOfDimensions.subclass(*args_, **kwargs_)
        else:
            return ArrayOfDimensions(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Dimensions(self):
        return self.Dimensions
    def set_Dimensions(self, Dimensions):
        self.Dimensions = Dimensions
    def add_Dimensions(self, value):
        self.Dimensions.append(value)
    def insert_Dimensions_at(self, index, value):
        self.Dimensions.insert(index, value)
    def replace_Dimensions_at(self, index, value):
        self.Dimensions[index] = value
    def hasContent_(self):
        if (
            self.Dimensions
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfDimensions', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfDimensions')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfDimensions':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfDimensions')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfDimensions', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfDimensions'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfDimensions', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Dimensions_ in self.Dimensions:
            namespaceprefix_ = self.Dimensions_nsprefix_ + ':' if (UseCapturedNS_ and self.Dimensions_nsprefix_) else ''
            Dimensions_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Dimensions', pretty_print=pretty_print)
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
        if nodeName_ == 'Dimensions':
            obj_ = Dimensions.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Dimensions.append(obj_)
            obj_.original_tagname_ = 'Dimensions'
# end class ArrayOfDimensions


class DeliveryInstructions(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Option=None, Reference=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Option = Option
        self.Option_nsprefix_ = None
        self.Reference = Reference
        self.Reference_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DeliveryInstructions)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DeliveryInstructions.subclass:
            return DeliveryInstructions.subclass(*args_, **kwargs_)
        else:
            return DeliveryInstructions(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Option(self):
        return self.Option
    def set_Option(self, Option):
        self.Option = Option
    def get_Reference(self):
        return self.Reference
    def set_Reference(self, Reference):
        self.Reference = Reference
    def hasContent_(self):
        if (
            self.Option is not None or
            self.Reference is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeliveryInstructions', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DeliveryInstructions')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DeliveryInstructions':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DeliveryInstructions')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DeliveryInstructions', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DeliveryInstructions'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeliveryInstructions', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Option is not None:
            namespaceprefix_ = self.Option_nsprefix_ + ':' if (UseCapturedNS_ and self.Option_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOption>%s</%sOption>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Option), input_name='Option')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Option':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Option')
            value_ = self.gds_validate_string(value_, node, 'Option')
            self.Option = value_
            self.Option_nsprefix_ = child_.prefix
        elif nodeName_ == 'Reference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Reference')
            value_ = self.gds_validate_string(value_, node, 'Reference')
            self.Reference = value_
            self.Reference_nsprefix_ = child_.prefix
# end class DeliveryInstructions


class ArrayOfAdditionalProperty(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AdditionalProperty=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if AdditionalProperty is None:
            self.AdditionalProperty = []
        else:
            self.AdditionalProperty = AdditionalProperty
        self.AdditionalProperty_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfAdditionalProperty)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfAdditionalProperty.subclass:
            return ArrayOfAdditionalProperty.subclass(*args_, **kwargs_)
        else:
            return ArrayOfAdditionalProperty(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AdditionalProperty(self):
        return self.AdditionalProperty
    def set_AdditionalProperty(self, AdditionalProperty):
        self.AdditionalProperty = AdditionalProperty
    def add_AdditionalProperty(self, value):
        self.AdditionalProperty.append(value)
    def insert_AdditionalProperty_at(self, index, value):
        self.AdditionalProperty.insert(index, value)
    def replace_AdditionalProperty_at(self, index, value):
        self.AdditionalProperty[index] = value
    def hasContent_(self):
        if (
            self.AdditionalProperty
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfAdditionalProperty', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfAdditionalProperty')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfAdditionalProperty':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfAdditionalProperty')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfAdditionalProperty', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfAdditionalProperty'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfAdditionalProperty', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for AdditionalProperty_ in self.AdditionalProperty:
            namespaceprefix_ = self.AdditionalProperty_nsprefix_ + ':' if (UseCapturedNS_ and self.AdditionalProperty_nsprefix_) else ''
            AdditionalProperty_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AdditionalProperty', pretty_print=pretty_print)
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
        if nodeName_ == 'AdditionalProperty':
            obj_ = AdditionalProperty.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdditionalProperty.append(obj_)
            obj_.original_tagname_ = 'AdditionalProperty'
# end class ArrayOfAdditionalProperty


class AdditionalProperty(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CategoryName=None, Name=None, Value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CategoryName = CategoryName
        self.CategoryName_nsprefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = None
        self.Value = Value
        self.Value_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AdditionalProperty)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AdditionalProperty.subclass:
            return AdditionalProperty.subclass(*args_, **kwargs_)
        else:
            return AdditionalProperty(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CategoryName(self):
        return self.CategoryName
    def set_CategoryName(self, CategoryName):
        self.CategoryName = CategoryName
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def hasContent_(self):
        if (
            self.CategoryName is not None or
            self.Name is not None or
            self.Value is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AdditionalProperty', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AdditionalProperty')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AdditionalProperty':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AdditionalProperty')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AdditionalProperty', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AdditionalProperty'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AdditionalProperty', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CategoryName is not None:
            namespaceprefix_ = self.CategoryName_nsprefix_ + ':' if (UseCapturedNS_ and self.CategoryName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCategoryName>%s</%sCategoryName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CategoryName), input_name='CategoryName')), namespaceprefix_ , eol_))
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName>%s</%sName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name), input_name='Name')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'CategoryName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CategoryName')
            value_ = self.gds_validate_string(value_, node, 'CategoryName')
            self.CategoryName = value_
            self.CategoryName_nsprefix_ = child_.prefix
        elif nodeName_ == 'Name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Name')
            value_ = self.gds_validate_string(value_, node, 'Name')
            self.Name = value_
            self.Name_nsprefix_ = child_.prefix
        elif nodeName_ == 'Value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Value')
            value_ = self.gds_validate_string(value_, node, 'Value')
            self.Value = value_
            self.Value_nsprefix_ = child_.prefix
# end class AdditionalProperty


class RateCalculatorResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Transaction=None, Notifications=None, HasErrors=None, TotalAmount=None, RateDetails=None, gds_collector_=None, **kwargs_):
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
        self.TotalAmount = TotalAmount
        self.TotalAmount_nsprefix_ = None
        self.RateDetails = RateDetails
        self.RateDetails_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RateCalculatorResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RateCalculatorResponse.subclass:
            return RateCalculatorResponse.subclass(*args_, **kwargs_)
        else:
            return RateCalculatorResponse(*args_, **kwargs_)
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
    def get_TotalAmount(self):
        return self.TotalAmount
    def set_TotalAmount(self, TotalAmount):
        self.TotalAmount = TotalAmount
    def get_RateDetails(self):
        return self.RateDetails
    def set_RateDetails(self, RateDetails):
        self.RateDetails = RateDetails
    def hasContent_(self):
        if (
            self.Transaction is not None or
            self.Notifications is not None or
            self.HasErrors is not None or
            self.TotalAmount is not None or
            self.RateDetails is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RateCalculatorResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RateCalculatorResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RateCalculatorResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RateCalculatorResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RateCalculatorResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RateCalculatorResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RateCalculatorResponse', fromsubclass_=False, pretty_print=True):
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
        if self.TotalAmount is not None:
            namespaceprefix_ = self.TotalAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.TotalAmount_nsprefix_) else ''
            self.TotalAmount.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TotalAmount', pretty_print=pretty_print)
        if self.RateDetails is not None:
            namespaceprefix_ = self.RateDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.RateDetails_nsprefix_) else ''
            self.RateDetails.export(outfile, level, namespaceprefix_, namespacedef_='', name_='RateDetails', pretty_print=pretty_print)
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
        elif nodeName_ == 'TotalAmount':
            obj_ = Money.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TotalAmount = obj_
            obj_.original_tagname_ = 'TotalAmount'
        elif nodeName_ == 'RateDetails':
            obj_ = RateDetails.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.RateDetails = obj_
            obj_.original_tagname_ = 'RateDetails'
# end class RateCalculatorResponse


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


class RateDetails(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Amount=None, OtherAmount1=None, OtherAmount2=None, OtherAmount3=None, OtherAmount4=None, OtherAmount5=None, TotalAmountBeforeTax=None, TaxAmount=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Amount = Amount
        self.Amount_nsprefix_ = None
        self.OtherAmount1 = OtherAmount1
        self.OtherAmount1_nsprefix_ = None
        self.OtherAmount2 = OtherAmount2
        self.OtherAmount2_nsprefix_ = None
        self.OtherAmount3 = OtherAmount3
        self.OtherAmount3_nsprefix_ = None
        self.OtherAmount4 = OtherAmount4
        self.OtherAmount4_nsprefix_ = None
        self.OtherAmount5 = OtherAmount5
        self.OtherAmount5_nsprefix_ = None
        self.TotalAmountBeforeTax = TotalAmountBeforeTax
        self.TotalAmountBeforeTax_nsprefix_ = None
        self.TaxAmount = TaxAmount
        self.TaxAmount_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RateDetails)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RateDetails.subclass:
            return RateDetails.subclass(*args_, **kwargs_)
        else:
            return RateDetails(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Amount(self):
        return self.Amount
    def set_Amount(self, Amount):
        self.Amount = Amount
    def get_OtherAmount1(self):
        return self.OtherAmount1
    def set_OtherAmount1(self, OtherAmount1):
        self.OtherAmount1 = OtherAmount1
    def get_OtherAmount2(self):
        return self.OtherAmount2
    def set_OtherAmount2(self, OtherAmount2):
        self.OtherAmount2 = OtherAmount2
    def get_OtherAmount3(self):
        return self.OtherAmount3
    def set_OtherAmount3(self, OtherAmount3):
        self.OtherAmount3 = OtherAmount3
    def get_OtherAmount4(self):
        return self.OtherAmount4
    def set_OtherAmount4(self, OtherAmount4):
        self.OtherAmount4 = OtherAmount4
    def get_OtherAmount5(self):
        return self.OtherAmount5
    def set_OtherAmount5(self, OtherAmount5):
        self.OtherAmount5 = OtherAmount5
    def get_TotalAmountBeforeTax(self):
        return self.TotalAmountBeforeTax
    def set_TotalAmountBeforeTax(self, TotalAmountBeforeTax):
        self.TotalAmountBeforeTax = TotalAmountBeforeTax
    def get_TaxAmount(self):
        return self.TaxAmount
    def set_TaxAmount(self, TaxAmount):
        self.TaxAmount = TaxAmount
    def hasContent_(self):
        if (
            self.Amount is not None or
            self.OtherAmount1 is not None or
            self.OtherAmount2 is not None or
            self.OtherAmount3 is not None or
            self.OtherAmount4 is not None or
            self.OtherAmount5 is not None or
            self.TotalAmountBeforeTax is not None or
            self.TaxAmount is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RateDetails', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RateDetails')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RateDetails':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RateDetails')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RateDetails', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RateDetails'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RateDetails', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Amount is not None:
            namespaceprefix_ = self.Amount_nsprefix_ + ':' if (UseCapturedNS_ and self.Amount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAmount>%s</%sAmount>%s' % (namespaceprefix_ , self.gds_format_double(self.Amount, input_name='Amount'), namespaceprefix_ , eol_))
        if self.OtherAmount1 is not None:
            namespaceprefix_ = self.OtherAmount1_nsprefix_ + ':' if (UseCapturedNS_ and self.OtherAmount1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOtherAmount1>%s</%sOtherAmount1>%s' % (namespaceprefix_ , self.gds_format_double(self.OtherAmount1, input_name='OtherAmount1'), namespaceprefix_ , eol_))
        if self.OtherAmount2 is not None:
            namespaceprefix_ = self.OtherAmount2_nsprefix_ + ':' if (UseCapturedNS_ and self.OtherAmount2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOtherAmount2>%s</%sOtherAmount2>%s' % (namespaceprefix_ , self.gds_format_double(self.OtherAmount2, input_name='OtherAmount2'), namespaceprefix_ , eol_))
        if self.OtherAmount3 is not None:
            namespaceprefix_ = self.OtherAmount3_nsprefix_ + ':' if (UseCapturedNS_ and self.OtherAmount3_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOtherAmount3>%s</%sOtherAmount3>%s' % (namespaceprefix_ , self.gds_format_double(self.OtherAmount3, input_name='OtherAmount3'), namespaceprefix_ , eol_))
        if self.OtherAmount4 is not None:
            namespaceprefix_ = self.OtherAmount4_nsprefix_ + ':' if (UseCapturedNS_ and self.OtherAmount4_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOtherAmount4>%s</%sOtherAmount4>%s' % (namespaceprefix_ , self.gds_format_double(self.OtherAmount4, input_name='OtherAmount4'), namespaceprefix_ , eol_))
        if self.OtherAmount5 is not None:
            namespaceprefix_ = self.OtherAmount5_nsprefix_ + ':' if (UseCapturedNS_ and self.OtherAmount5_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOtherAmount5>%s</%sOtherAmount5>%s' % (namespaceprefix_ , self.gds_format_double(self.OtherAmount5, input_name='OtherAmount5'), namespaceprefix_ , eol_))
        if self.TotalAmountBeforeTax is not None:
            namespaceprefix_ = self.TotalAmountBeforeTax_nsprefix_ + ':' if (UseCapturedNS_ and self.TotalAmountBeforeTax_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTotalAmountBeforeTax>%s</%sTotalAmountBeforeTax>%s' % (namespaceprefix_ , self.gds_format_double(self.TotalAmountBeforeTax, input_name='TotalAmountBeforeTax'), namespaceprefix_ , eol_))
        if self.TaxAmount is not None:
            namespaceprefix_ = self.TaxAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.TaxAmount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTaxAmount>%s</%sTaxAmount>%s' % (namespaceprefix_ , self.gds_format_double(self.TaxAmount, input_name='TaxAmount'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Amount' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'Amount')
            fval_ = self.gds_validate_double(fval_, node, 'Amount')
            self.Amount = fval_
            self.Amount_nsprefix_ = child_.prefix
        elif nodeName_ == 'OtherAmount1' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'OtherAmount1')
            fval_ = self.gds_validate_double(fval_, node, 'OtherAmount1')
            self.OtherAmount1 = fval_
            self.OtherAmount1_nsprefix_ = child_.prefix
        elif nodeName_ == 'OtherAmount2' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'OtherAmount2')
            fval_ = self.gds_validate_double(fval_, node, 'OtherAmount2')
            self.OtherAmount2 = fval_
            self.OtherAmount2_nsprefix_ = child_.prefix
        elif nodeName_ == 'OtherAmount3' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'OtherAmount3')
            fval_ = self.gds_validate_double(fval_, node, 'OtherAmount3')
            self.OtherAmount3 = fval_
            self.OtherAmount3_nsprefix_ = child_.prefix
        elif nodeName_ == 'OtherAmount4' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'OtherAmount4')
            fval_ = self.gds_validate_double(fval_, node, 'OtherAmount4')
            self.OtherAmount4 = fval_
            self.OtherAmount4_nsprefix_ = child_.prefix
        elif nodeName_ == 'OtherAmount5' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'OtherAmount5')
            fval_ = self.gds_validate_double(fval_, node, 'OtherAmount5')
            self.OtherAmount5 = fval_
            self.OtherAmount5_nsprefix_ = child_.prefix
        elif nodeName_ == 'TotalAmountBeforeTax' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'TotalAmountBeforeTax')
            fval_ = self.gds_validate_double(fval_, node, 'TotalAmountBeforeTax')
            self.TotalAmountBeforeTax = fval_
            self.TotalAmountBeforeTax_nsprefix_ = child_.prefix
        elif nodeName_ == 'TaxAmount' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'TaxAmount')
            fval_ = self.gds_validate_double(fval_, node, 'TaxAmount')
            self.TaxAmount = fval_
            self.TaxAmount_nsprefix_ = child_.prefix
# end class RateDetails


class MultiRateCalculatorRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ClientInfo=None, Transaction=None, OriginAddress=None, DestinationAddress=None, MultiRateDetails=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ClientInfo = ClientInfo
        self.ClientInfo_nsprefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.OriginAddress = OriginAddress
        self.OriginAddress_nsprefix_ = None
        self.DestinationAddress = DestinationAddress
        self.DestinationAddress_nsprefix_ = None
        self.MultiRateDetails = MultiRateDetails
        self.MultiRateDetails_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, MultiRateCalculatorRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if MultiRateCalculatorRequest.subclass:
            return MultiRateCalculatorRequest.subclass(*args_, **kwargs_)
        else:
            return MultiRateCalculatorRequest(*args_, **kwargs_)
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
    def get_OriginAddress(self):
        return self.OriginAddress
    def set_OriginAddress(self, OriginAddress):
        self.OriginAddress = OriginAddress
    def get_DestinationAddress(self):
        return self.DestinationAddress
    def set_DestinationAddress(self, DestinationAddress):
        self.DestinationAddress = DestinationAddress
    def get_MultiRateDetails(self):
        return self.MultiRateDetails
    def set_MultiRateDetails(self, MultiRateDetails):
        self.MultiRateDetails = MultiRateDetails
    def hasContent_(self):
        if (
            self.ClientInfo is not None or
            self.Transaction is not None or
            self.OriginAddress is not None or
            self.DestinationAddress is not None or
            self.MultiRateDetails is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='MultiRateCalculatorRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('MultiRateCalculatorRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'MultiRateCalculatorRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='MultiRateCalculatorRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='MultiRateCalculatorRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='MultiRateCalculatorRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='MultiRateCalculatorRequest', fromsubclass_=False, pretty_print=True):
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
        if self.OriginAddress is not None:
            namespaceprefix_ = self.OriginAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.OriginAddress_nsprefix_) else ''
            self.OriginAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='OriginAddress', pretty_print=pretty_print)
        if self.DestinationAddress is not None:
            namespaceprefix_ = self.DestinationAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationAddress_nsprefix_) else ''
            self.DestinationAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DestinationAddress', pretty_print=pretty_print)
        if self.MultiRateDetails is not None:
            namespaceprefix_ = self.MultiRateDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.MultiRateDetails_nsprefix_) else ''
            self.MultiRateDetails.export(outfile, level, namespaceprefix_, namespacedef_='', name_='MultiRateDetails', pretty_print=pretty_print)
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
        elif nodeName_ == 'OriginAddress':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.OriginAddress = obj_
            obj_.original_tagname_ = 'OriginAddress'
        elif nodeName_ == 'DestinationAddress':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DestinationAddress = obj_
            obj_.original_tagname_ = 'DestinationAddress'
        elif nodeName_ == 'MultiRateDetails':
            obj_ = MultiRateDetails.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.MultiRateDetails = obj_
            obj_.original_tagname_ = 'MultiRateDetails'
# end class MultiRateCalculatorRequest


class MultiRateDetails(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ProductGroup=None, ProductTypes=None, PaymentType=None, Services=None, ActualWeight=None, CashOnDeliveryAmount=None, InsuranceAmount=None, CustomsValueAmount=None, CollectAmount=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ProductGroup = ProductGroup
        self.ProductGroup_nsprefix_ = None
        self.ProductTypes = ProductTypes
        self.ProductTypes_nsprefix_ = None
        self.PaymentType = PaymentType
        self.PaymentType_nsprefix_ = None
        self.Services = Services
        self.Services_nsprefix_ = None
        self.ActualWeight = ActualWeight
        self.ActualWeight_nsprefix_ = None
        self.CashOnDeliveryAmount = CashOnDeliveryAmount
        self.CashOnDeliveryAmount_nsprefix_ = None
        self.InsuranceAmount = InsuranceAmount
        self.InsuranceAmount_nsprefix_ = None
        self.CustomsValueAmount = CustomsValueAmount
        self.CustomsValueAmount_nsprefix_ = None
        self.CollectAmount = CollectAmount
        self.CollectAmount_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, MultiRateDetails)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if MultiRateDetails.subclass:
            return MultiRateDetails.subclass(*args_, **kwargs_)
        else:
            return MultiRateDetails(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ProductGroup(self):
        return self.ProductGroup
    def set_ProductGroup(self, ProductGroup):
        self.ProductGroup = ProductGroup
    def get_ProductTypes(self):
        return self.ProductTypes
    def set_ProductTypes(self, ProductTypes):
        self.ProductTypes = ProductTypes
    def get_PaymentType(self):
        return self.PaymentType
    def set_PaymentType(self, PaymentType):
        self.PaymentType = PaymentType
    def get_Services(self):
        return self.Services
    def set_Services(self, Services):
        self.Services = Services
    def get_ActualWeight(self):
        return self.ActualWeight
    def set_ActualWeight(self, ActualWeight):
        self.ActualWeight = ActualWeight
    def get_CashOnDeliveryAmount(self):
        return self.CashOnDeliveryAmount
    def set_CashOnDeliveryAmount(self, CashOnDeliveryAmount):
        self.CashOnDeliveryAmount = CashOnDeliveryAmount
    def get_InsuranceAmount(self):
        return self.InsuranceAmount
    def set_InsuranceAmount(self, InsuranceAmount):
        self.InsuranceAmount = InsuranceAmount
    def get_CustomsValueAmount(self):
        return self.CustomsValueAmount
    def set_CustomsValueAmount(self, CustomsValueAmount):
        self.CustomsValueAmount = CustomsValueAmount
    def get_CollectAmount(self):
        return self.CollectAmount
    def set_CollectAmount(self, CollectAmount):
        self.CollectAmount = CollectAmount
    def hasContent_(self):
        if (
            self.ProductGroup is not None or
            self.ProductTypes is not None or
            self.PaymentType is not None or
            self.Services is not None or
            self.ActualWeight is not None or
            self.CashOnDeliveryAmount is not None or
            self.InsuranceAmount is not None or
            self.CustomsValueAmount is not None or
            self.CollectAmount is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='MultiRateDetails', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('MultiRateDetails')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'MultiRateDetails':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='MultiRateDetails')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='MultiRateDetails', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='MultiRateDetails'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='MultiRateDetails', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ProductGroup is not None:
            namespaceprefix_ = self.ProductGroup_nsprefix_ + ':' if (UseCapturedNS_ and self.ProductGroup_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProductGroup>%s</%sProductGroup>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ProductGroup), input_name='ProductGroup')), namespaceprefix_ , eol_))
        if self.ProductTypes is not None:
            namespaceprefix_ = self.ProductTypes_nsprefix_ + ':' if (UseCapturedNS_ and self.ProductTypes_nsprefix_) else ''
            self.ProductTypes.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ProductTypes', pretty_print=pretty_print)
        if self.PaymentType is not None:
            namespaceprefix_ = self.PaymentType_nsprefix_ + ':' if (UseCapturedNS_ and self.PaymentType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPaymentType>%s</%sPaymentType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PaymentType), input_name='PaymentType')), namespaceprefix_ , eol_))
        if self.Services is not None:
            namespaceprefix_ = self.Services_nsprefix_ + ':' if (UseCapturedNS_ and self.Services_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServices>%s</%sServices>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Services), input_name='Services')), namespaceprefix_ , eol_))
        if self.ActualWeight is not None:
            namespaceprefix_ = self.ActualWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.ActualWeight_nsprefix_) else ''
            self.ActualWeight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ActualWeight', pretty_print=pretty_print)
        if self.CashOnDeliveryAmount is not None:
            namespaceprefix_ = self.CashOnDeliveryAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.CashOnDeliveryAmount_nsprefix_) else ''
            self.CashOnDeliveryAmount.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CashOnDeliveryAmount', pretty_print=pretty_print)
        if self.InsuranceAmount is not None:
            namespaceprefix_ = self.InsuranceAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.InsuranceAmount_nsprefix_) else ''
            self.InsuranceAmount.export(outfile, level, namespaceprefix_, namespacedef_='', name_='InsuranceAmount', pretty_print=pretty_print)
        if self.CustomsValueAmount is not None:
            namespaceprefix_ = self.CustomsValueAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomsValueAmount_nsprefix_) else ''
            self.CustomsValueAmount.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CustomsValueAmount', pretty_print=pretty_print)
        if self.CollectAmount is not None:
            namespaceprefix_ = self.CollectAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.CollectAmount_nsprefix_) else ''
            self.CollectAmount.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CollectAmount', pretty_print=pretty_print)
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
        elif nodeName_ == 'ProductTypes':
            obj_ = ArrayOfstring.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ProductTypes = obj_
            obj_.original_tagname_ = 'ProductTypes'
        elif nodeName_ == 'PaymentType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PaymentType')
            value_ = self.gds_validate_string(value_, node, 'PaymentType')
            self.PaymentType = value_
            self.PaymentType_nsprefix_ = child_.prefix
        elif nodeName_ == 'Services':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Services')
            value_ = self.gds_validate_string(value_, node, 'Services')
            self.Services = value_
            self.Services_nsprefix_ = child_.prefix
        elif nodeName_ == 'ActualWeight':
            obj_ = Weight.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ActualWeight = obj_
            obj_.original_tagname_ = 'ActualWeight'
        elif nodeName_ == 'CashOnDeliveryAmount':
            obj_ = Money.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CashOnDeliveryAmount = obj_
            obj_.original_tagname_ = 'CashOnDeliveryAmount'
        elif nodeName_ == 'InsuranceAmount':
            obj_ = Money.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.InsuranceAmount = obj_
            obj_.original_tagname_ = 'InsuranceAmount'
        elif nodeName_ == 'CustomsValueAmount':
            obj_ = Money.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CustomsValueAmount = obj_
            obj_.original_tagname_ = 'CustomsValueAmount'
        elif nodeName_ == 'CollectAmount':
            obj_ = Money.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CollectAmount = obj_
            obj_.original_tagname_ = 'CollectAmount'
# end class MultiRateDetails


class MultiRateCalculatorResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Transaction=None, Notifications=None, HasErrors=None, RateResults=None, gds_collector_=None, **kwargs_):
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
        self.RateResults = RateResults
        self.RateResults_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, MultiRateCalculatorResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if MultiRateCalculatorResponse.subclass:
            return MultiRateCalculatorResponse.subclass(*args_, **kwargs_)
        else:
            return MultiRateCalculatorResponse(*args_, **kwargs_)
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
    def get_RateResults(self):
        return self.RateResults
    def set_RateResults(self, RateResults):
        self.RateResults = RateResults
    def hasContent_(self):
        if (
            self.Transaction is not None or
            self.Notifications is not None or
            self.HasErrors is not None or
            self.RateResults is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='MultiRateCalculatorResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('MultiRateCalculatorResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'MultiRateCalculatorResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='MultiRateCalculatorResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='MultiRateCalculatorResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='MultiRateCalculatorResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='MultiRateCalculatorResponse', fromsubclass_=False, pretty_print=True):
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
        if self.RateResults is not None:
            namespaceprefix_ = self.RateResults_nsprefix_ + ':' if (UseCapturedNS_ and self.RateResults_nsprefix_) else ''
            self.RateResults.export(outfile, level, namespaceprefix_, namespacedef_='', name_='RateResults', pretty_print=pretty_print)
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
        elif nodeName_ == 'RateResults':
            obj_ = ArrayOfProductTypeRateResult.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.RateResults = obj_
            obj_.original_tagname_ = 'RateResults'
# end class MultiRateCalculatorResponse


class ArrayOfProductTypeRateResult(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ProductTypeRateResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if ProductTypeRateResult is None:
            self.ProductTypeRateResult = []
        else:
            self.ProductTypeRateResult = ProductTypeRateResult
        self.ProductTypeRateResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfProductTypeRateResult)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfProductTypeRateResult.subclass:
            return ArrayOfProductTypeRateResult.subclass(*args_, **kwargs_)
        else:
            return ArrayOfProductTypeRateResult(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ProductTypeRateResult(self):
        return self.ProductTypeRateResult
    def set_ProductTypeRateResult(self, ProductTypeRateResult):
        self.ProductTypeRateResult = ProductTypeRateResult
    def add_ProductTypeRateResult(self, value):
        self.ProductTypeRateResult.append(value)
    def insert_ProductTypeRateResult_at(self, index, value):
        self.ProductTypeRateResult.insert(index, value)
    def replace_ProductTypeRateResult_at(self, index, value):
        self.ProductTypeRateResult[index] = value
    def hasContent_(self):
        if (
            self.ProductTypeRateResult
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfProductTypeRateResult', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfProductTypeRateResult')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfProductTypeRateResult':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfProductTypeRateResult')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfProductTypeRateResult', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfProductTypeRateResult'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfProductTypeRateResult', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for ProductTypeRateResult_ in self.ProductTypeRateResult:
            namespaceprefix_ = self.ProductTypeRateResult_nsprefix_ + ':' if (UseCapturedNS_ and self.ProductTypeRateResult_nsprefix_) else ''
            ProductTypeRateResult_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ProductTypeRateResult', pretty_print=pretty_print)
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
        if nodeName_ == 'ProductTypeRateResult':
            obj_ = ProductTypeRateResult.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ProductTypeRateResult.append(obj_)
            obj_.original_tagname_ = 'ProductTypeRateResult'
# end class ArrayOfProductTypeRateResult


class ProductTypeRateResult(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ProductGroup=None, ProductType=None, AccountEntity=None, AccountNumber=None, Amount=None, Currency=None, AmountBeforeTax=None, TaxAmount=None, TaxRate=None, AdditionalCharges=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ProductGroup = ProductGroup
        self.ProductGroup_nsprefix_ = None
        self.ProductType = ProductType
        self.ProductType_nsprefix_ = None
        self.AccountEntity = AccountEntity
        self.AccountEntity_nsprefix_ = None
        self.AccountNumber = AccountNumber
        self.AccountNumber_nsprefix_ = None
        self.Amount = Amount
        self.Amount_nsprefix_ = None
        self.Currency = Currency
        self.Currency_nsprefix_ = None
        self.AmountBeforeTax = AmountBeforeTax
        self.AmountBeforeTax_nsprefix_ = None
        self.TaxAmount = TaxAmount
        self.TaxAmount_nsprefix_ = None
        self.TaxRate = TaxRate
        self.TaxRate_nsprefix_ = None
        self.AdditionalCharges = AdditionalCharges
        self.AdditionalCharges_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ProductTypeRateResult)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ProductTypeRateResult.subclass:
            return ProductTypeRateResult.subclass(*args_, **kwargs_)
        else:
            return ProductTypeRateResult(*args_, **kwargs_)
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
    def get_AccountEntity(self):
        return self.AccountEntity
    def set_AccountEntity(self, AccountEntity):
        self.AccountEntity = AccountEntity
    def get_AccountNumber(self):
        return self.AccountNumber
    def set_AccountNumber(self, AccountNumber):
        self.AccountNumber = AccountNumber
    def get_Amount(self):
        return self.Amount
    def set_Amount(self, Amount):
        self.Amount = Amount
    def get_Currency(self):
        return self.Currency
    def set_Currency(self, Currency):
        self.Currency = Currency
    def get_AmountBeforeTax(self):
        return self.AmountBeforeTax
    def set_AmountBeforeTax(self, AmountBeforeTax):
        self.AmountBeforeTax = AmountBeforeTax
    def get_TaxAmount(self):
        return self.TaxAmount
    def set_TaxAmount(self, TaxAmount):
        self.TaxAmount = TaxAmount
    def get_TaxRate(self):
        return self.TaxRate
    def set_TaxRate(self, TaxRate):
        self.TaxRate = TaxRate
    def get_AdditionalCharges(self):
        return self.AdditionalCharges
    def set_AdditionalCharges(self, AdditionalCharges):
        self.AdditionalCharges = AdditionalCharges
    def hasContent_(self):
        if (
            self.ProductGroup is not None or
            self.ProductType is not None or
            self.AccountEntity is not None or
            self.AccountNumber is not None or
            self.Amount is not None or
            self.Currency is not None or
            self.AmountBeforeTax is not None or
            self.TaxAmount is not None or
            self.TaxRate is not None or
            self.AdditionalCharges is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ProductTypeRateResult', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ProductTypeRateResult')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ProductTypeRateResult':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ProductTypeRateResult')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ProductTypeRateResult', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ProductTypeRateResult'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ProductTypeRateResult', fromsubclass_=False, pretty_print=True):
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
        if self.AccountEntity is not None:
            namespaceprefix_ = self.AccountEntity_nsprefix_ + ':' if (UseCapturedNS_ and self.AccountEntity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccountEntity>%s</%sAccountEntity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AccountEntity), input_name='AccountEntity')), namespaceprefix_ , eol_))
        if self.AccountNumber is not None:
            namespaceprefix_ = self.AccountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.AccountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccountNumber>%s</%sAccountNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AccountNumber), input_name='AccountNumber')), namespaceprefix_ , eol_))
        if self.Amount is not None:
            namespaceprefix_ = self.Amount_nsprefix_ + ':' if (UseCapturedNS_ and self.Amount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAmount>%s</%sAmount>%s' % (namespaceprefix_ , self.gds_format_double(self.Amount, input_name='Amount'), namespaceprefix_ , eol_))
        if self.Currency is not None:
            namespaceprefix_ = self.Currency_nsprefix_ + ':' if (UseCapturedNS_ and self.Currency_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrency>%s</%sCurrency>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Currency), input_name='Currency')), namespaceprefix_ , eol_))
        if self.AmountBeforeTax is not None:
            namespaceprefix_ = self.AmountBeforeTax_nsprefix_ + ':' if (UseCapturedNS_ and self.AmountBeforeTax_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAmountBeforeTax>%s</%sAmountBeforeTax>%s' % (namespaceprefix_ , self.gds_format_double(self.AmountBeforeTax, input_name='AmountBeforeTax'), namespaceprefix_ , eol_))
        if self.TaxAmount is not None:
            namespaceprefix_ = self.TaxAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.TaxAmount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTaxAmount>%s</%sTaxAmount>%s' % (namespaceprefix_ , self.gds_format_double(self.TaxAmount, input_name='TaxAmount'), namespaceprefix_ , eol_))
        if self.TaxRate is not None:
            namespaceprefix_ = self.TaxRate_nsprefix_ + ':' if (UseCapturedNS_ and self.TaxRate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTaxRate>%s</%sTaxRate>%s' % (namespaceprefix_ , self.gds_format_double(self.TaxRate, input_name='TaxRate'), namespaceprefix_ , eol_))
        if self.AdditionalCharges is not None:
            namespaceprefix_ = self.AdditionalCharges_nsprefix_ + ':' if (UseCapturedNS_ and self.AdditionalCharges_nsprefix_) else ''
            self.AdditionalCharges.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AdditionalCharges', pretty_print=pretty_print)
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
        elif nodeName_ == 'AccountEntity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AccountEntity')
            value_ = self.gds_validate_string(value_, node, 'AccountEntity')
            self.AccountEntity = value_
            self.AccountEntity_nsprefix_ = child_.prefix
        elif nodeName_ == 'AccountNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AccountNumber')
            value_ = self.gds_validate_string(value_, node, 'AccountNumber')
            self.AccountNumber = value_
            self.AccountNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'Amount' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'Amount')
            fval_ = self.gds_validate_double(fval_, node, 'Amount')
            self.Amount = fval_
            self.Amount_nsprefix_ = child_.prefix
        elif nodeName_ == 'Currency':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Currency')
            value_ = self.gds_validate_string(value_, node, 'Currency')
            self.Currency = value_
            self.Currency_nsprefix_ = child_.prefix
        elif nodeName_ == 'AmountBeforeTax' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'AmountBeforeTax')
            fval_ = self.gds_validate_double(fval_, node, 'AmountBeforeTax')
            self.AmountBeforeTax = fval_
            self.AmountBeforeTax_nsprefix_ = child_.prefix
        elif nodeName_ == 'TaxAmount' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'TaxAmount')
            fval_ = self.gds_validate_double(fval_, node, 'TaxAmount')
            self.TaxAmount = fval_
            self.TaxAmount_nsprefix_ = child_.prefix
        elif nodeName_ == 'TaxRate' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'TaxRate')
            fval_ = self.gds_validate_double(fval_, node, 'TaxRate')
            self.TaxRate = fval_
            self.TaxRate_nsprefix_ = child_.prefix
        elif nodeName_ == 'AdditionalCharges':
            obj_ = ArrayOfAdditionalCharge.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdditionalCharges = obj_
            obj_.original_tagname_ = 'AdditionalCharges'
# end class ProductTypeRateResult


class ArrayOfAdditionalCharge(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AdditionalCharge=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if AdditionalCharge is None:
            self.AdditionalCharge = []
        else:
            self.AdditionalCharge = AdditionalCharge
        self.AdditionalCharge_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfAdditionalCharge)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfAdditionalCharge.subclass:
            return ArrayOfAdditionalCharge.subclass(*args_, **kwargs_)
        else:
            return ArrayOfAdditionalCharge(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AdditionalCharge(self):
        return self.AdditionalCharge
    def set_AdditionalCharge(self, AdditionalCharge):
        self.AdditionalCharge = AdditionalCharge
    def add_AdditionalCharge(self, value):
        self.AdditionalCharge.append(value)
    def insert_AdditionalCharge_at(self, index, value):
        self.AdditionalCharge.insert(index, value)
    def replace_AdditionalCharge_at(self, index, value):
        self.AdditionalCharge[index] = value
    def hasContent_(self):
        if (
            self.AdditionalCharge
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfAdditionalCharge', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfAdditionalCharge')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfAdditionalCharge':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfAdditionalCharge')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfAdditionalCharge', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfAdditionalCharge'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfAdditionalCharge', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for AdditionalCharge_ in self.AdditionalCharge:
            namespaceprefix_ = self.AdditionalCharge_nsprefix_ + ':' if (UseCapturedNS_ and self.AdditionalCharge_nsprefix_) else ''
            AdditionalCharge_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AdditionalCharge', pretty_print=pretty_print)
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
        if nodeName_ == 'AdditionalCharge':
            obj_ = AdditionalCharge.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdditionalCharge.append(obj_)
            obj_.original_tagname_ = 'AdditionalCharge'
# end class ArrayOfAdditionalCharge


class AdditionalCharge(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Amount=None, Code=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Amount = Amount
        self.Amount_nsprefix_ = None
        self.Code = Code
        self.Code_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AdditionalCharge)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AdditionalCharge.subclass:
            return AdditionalCharge.subclass(*args_, **kwargs_)
        else:
            return AdditionalCharge(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Amount(self):
        return self.Amount
    def set_Amount(self, Amount):
        self.Amount = Amount
    def get_Code(self):
        return self.Code
    def set_Code(self, Code):
        self.Code = Code
    def hasContent_(self):
        if (
            self.Amount is not None or
            self.Code is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AdditionalCharge', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AdditionalCharge')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AdditionalCharge':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AdditionalCharge')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AdditionalCharge', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AdditionalCharge'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AdditionalCharge', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Amount is not None:
            namespaceprefix_ = self.Amount_nsprefix_ + ':' if (UseCapturedNS_ and self.Amount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAmount>%s</%sAmount>%s' % (namespaceprefix_ , self.gds_format_double(self.Amount, input_name='Amount'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Amount' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'Amount')
            fval_ = self.gds_validate_double(fval_, node, 'Amount')
            self.Amount = fval_
            self.Amount_nsprefix_ = child_.prefix
        elif nodeName_ == 'Code':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Code')
            value_ = self.gds_validate_string(value_, node, 'Code')
            self.Code = value_
            self.Code_nsprefix_ = child_.prefix
# end class AdditionalCharge


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
    'AdditionalCharge': AdditionalCharge,
    'AdditionalProperty': AdditionalProperty,
    'Address': Address,
    'ArrayOfAdditionalCharge': ArrayOfAdditionalCharge,
    'ArrayOfAdditionalProperty': ArrayOfAdditionalProperty,
    'ArrayOfDimensions': ArrayOfDimensions,
    'ArrayOfNotification': ArrayOfNotification,
    'ArrayOfProductTypeRateResult': ArrayOfProductTypeRateResult,
    'ArrayOfShipmentItem': ArrayOfShipmentItem,
    'ArrayOfstring': ArrayOfstring,
    'ClientInfo': ClientInfo,
    'DeliveryInstructions': DeliveryInstructions,
    'Dimensions': Dimensions,
    'Money': Money,
    'MultiRateDetails': MultiRateDetails,
    'Notification': Notification,
    'ProductTypeRateResult': ProductTypeRateResult,
    'RateDetails': RateDetails,
    'ShipmentDetails': ShipmentDetails,
    'ShipmentItem': ShipmentItem,
    'Transaction': Transaction,
    'Weight': Weight,
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
        rootTag = 'RateCalculatorRequest'
        rootClass = RateCalculatorRequest
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
        rootTag = 'RateCalculatorRequest'
        rootClass = RateCalculatorRequest
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
        rootTag = 'RateCalculatorRequest'
        rootClass = RateCalculatorRequest
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
        rootTag = 'RateCalculatorRequest'
        rootClass = RateCalculatorRequest
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from rates import *\n\n')
        sys.stdout.write('import rates as model_\n\n')
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
                                                                'https://ws.aramex.net/ShippingAPI.V2/RateCalculator/Service_1_0.svc?xsd=xsd2',
                                                                'CT')],
 'http://ws.aramex.net/ShippingAPI/v1/': [('ClientInfo',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('Transaction',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('Address',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('ShipmentDetails',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('Dimensions',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('Weight',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('Money',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('ArrayOfShipmentItem',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('ShipmentItem',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('ArrayOfDimensions',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('DeliveryInstructions',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('ArrayOfAdditionalProperty',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('AdditionalProperty',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('ArrayOfNotification',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('Notification',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('RateDetails',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('MultiRateDetails',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('ArrayOfProductTypeRateResult',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('ProductTypeRateResult',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('ArrayOfAdditionalCharge',
                                           './schemas/rates.xsd',
                                           'CT'),
                                          ('AdditionalCharge',
                                           './schemas/rates.xsd',
                                           'CT')]}

__all__ = [
    "AdditionalCharge",
    "AdditionalProperty",
    "Address",
    "ArrayOfAdditionalCharge",
    "ArrayOfAdditionalProperty",
    "ArrayOfDimensions",
    "ArrayOfNotification",
    "ArrayOfProductTypeRateResult",
    "ArrayOfShipmentItem",
    "ArrayOfstring",
    "ClientInfo",
    "DeliveryInstructions",
    "Dimensions",
    "Money",
    "MultiRateCalculatorRequest",
    "MultiRateCalculatorResponse",
    "MultiRateDetails",
    "Notification",
    "ProductTypeRateResult",
    "RateCalculatorRequest",
    "RateCalculatorResponse",
    "RateDetails",
    "ShipmentDetails",
    "ShipmentItem",
    "Transaction",
    "Weight"
]
