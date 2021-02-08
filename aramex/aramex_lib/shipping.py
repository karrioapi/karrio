#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Sun Feb  7 20:26:58 2021 by generateDS.py version 2.37.15.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './aramex_lib/shipping.py')
#
# Command line arguments:
#   ./schemas/shipping.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./aramex_lib/shipping.py" ./schemas/shipping.xsd
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


class ShipmentCreationRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ClientInfo=None, Transaction=None, Shipments=None, LabelInfo=None, gds_collector_=None, **kwargs_):
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
        self.LabelInfo = LabelInfo
        self.LabelInfo_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentCreationRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentCreationRequest.subclass:
            return ShipmentCreationRequest.subclass(*args_, **kwargs_)
        else:
            return ShipmentCreationRequest(*args_, **kwargs_)
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
    def get_LabelInfo(self):
        return self.LabelInfo
    def set_LabelInfo(self, LabelInfo):
        self.LabelInfo = LabelInfo
    def hasContent_(self):
        if (
            self.ClientInfo is not None or
            self.Transaction is not None or
            self.Shipments is not None or
            self.LabelInfo is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentCreationRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentCreationRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentCreationRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentCreationRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentCreationRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentCreationRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentCreationRequest', fromsubclass_=False, pretty_print=True):
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
        if self.LabelInfo is not None:
            namespaceprefix_ = self.LabelInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.LabelInfo_nsprefix_) else ''
            self.LabelInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='LabelInfo', pretty_print=pretty_print)
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
            obj_ = ArrayOfShipment.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Shipments = obj_
            obj_.original_tagname_ = 'Shipments'
        elif nodeName_ == 'LabelInfo':
            obj_ = LabelInfo.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LabelInfo = obj_
            obj_.original_tagname_ = 'LabelInfo'
# end class ShipmentCreationRequest


class ClientInfo(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, UserName=None, Password=None, Version=None, AccountNumber=None, AccountPin=None, AccountEntity=None, AccountCountryCode=None, gds_collector_=None, **kwargs_):
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
    def hasContent_(self):
        if (
            self.UserName is not None or
            self.Password is not None or
            self.Version is not None or
            self.AccountNumber is not None or
            self.AccountPin is not None or
            self.AccountEntity is not None or
            self.AccountCountryCode is not None
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


class ArrayOfShipment(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Shipment=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Shipment is None:
            self.Shipment = []
        else:
            self.Shipment = Shipment
        self.Shipment_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfShipment)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfShipment.subclass:
            return ArrayOfShipment.subclass(*args_, **kwargs_)
        else:
            return ArrayOfShipment(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Shipment(self):
        return self.Shipment
    def set_Shipment(self, Shipment):
        self.Shipment = Shipment
    def add_Shipment(self, value):
        self.Shipment.append(value)
    def insert_Shipment_at(self, index, value):
        self.Shipment.insert(index, value)
    def replace_Shipment_at(self, index, value):
        self.Shipment[index] = value
    def hasContent_(self):
        if (
            self.Shipment
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfShipment', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfShipment')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfShipment':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfShipment')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfShipment', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfShipment'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfShipment', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Shipment_ in self.Shipment:
            namespaceprefix_ = self.Shipment_nsprefix_ + ':' if (UseCapturedNS_ and self.Shipment_nsprefix_) else ''
            Shipment_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Shipment', pretty_print=pretty_print)
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
        if nodeName_ == 'Shipment':
            obj_ = Shipment.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Shipment.append(obj_)
            obj_.original_tagname_ = 'Shipment'
# end class ArrayOfShipment


class Shipment(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Reference1=None, Reference2=None, Reference3=None, Shipper=None, Consignee=None, ThirdParty=None, ShippingDateTime=None, DueDate=None, Comments=None, PickupLocation=None, OperationsInstructions=None, AccountingInstrcutions=None, Details=None, Attachments=None, ForeignHAWB=None, TransportType_x0020_=None, PickupGUID=None, gds_collector_=None, **kwargs_):
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
        self.Shipper = Shipper
        self.Shipper_nsprefix_ = None
        self.Consignee = Consignee
        self.Consignee_nsprefix_ = None
        self.ThirdParty = ThirdParty
        self.ThirdParty_nsprefix_ = None
        if isinstance(ShippingDateTime, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ShippingDateTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = ShippingDateTime
        self.ShippingDateTime = initvalue_
        self.ShippingDateTime_nsprefix_ = None
        if isinstance(DueDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DueDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = DueDate
        self.DueDate = initvalue_
        self.DueDate_nsprefix_ = None
        self.Comments = Comments
        self.Comments_nsprefix_ = None
        self.PickupLocation = PickupLocation
        self.PickupLocation_nsprefix_ = None
        self.OperationsInstructions = OperationsInstructions
        self.OperationsInstructions_nsprefix_ = None
        self.AccountingInstrcutions = AccountingInstrcutions
        self.AccountingInstrcutions_nsprefix_ = None
        self.Details = Details
        self.Details_nsprefix_ = None
        self.Attachments = Attachments
        self.Attachments_nsprefix_ = None
        self.ForeignHAWB = ForeignHAWB
        self.ForeignHAWB_nsprefix_ = None
        self.TransportType_x0020_ = TransportType_x0020_
        self.TransportType_x0020__nsprefix_ = None
        self.PickupGUID = PickupGUID
        self.PickupGUID_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Shipment)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Shipment.subclass:
            return Shipment.subclass(*args_, **kwargs_)
        else:
            return Shipment(*args_, **kwargs_)
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
    def get_Shipper(self):
        return self.Shipper
    def set_Shipper(self, Shipper):
        self.Shipper = Shipper
    def get_Consignee(self):
        return self.Consignee
    def set_Consignee(self, Consignee):
        self.Consignee = Consignee
    def get_ThirdParty(self):
        return self.ThirdParty
    def set_ThirdParty(self, ThirdParty):
        self.ThirdParty = ThirdParty
    def get_ShippingDateTime(self):
        return self.ShippingDateTime
    def set_ShippingDateTime(self, ShippingDateTime):
        self.ShippingDateTime = ShippingDateTime
    def get_DueDate(self):
        return self.DueDate
    def set_DueDate(self, DueDate):
        self.DueDate = DueDate
    def get_Comments(self):
        return self.Comments
    def set_Comments(self, Comments):
        self.Comments = Comments
    def get_PickupLocation(self):
        return self.PickupLocation
    def set_PickupLocation(self, PickupLocation):
        self.PickupLocation = PickupLocation
    def get_OperationsInstructions(self):
        return self.OperationsInstructions
    def set_OperationsInstructions(self, OperationsInstructions):
        self.OperationsInstructions = OperationsInstructions
    def get_AccountingInstrcutions(self):
        return self.AccountingInstrcutions
    def set_AccountingInstrcutions(self, AccountingInstrcutions):
        self.AccountingInstrcutions = AccountingInstrcutions
    def get_Details(self):
        return self.Details
    def set_Details(self, Details):
        self.Details = Details
    def get_Attachments(self):
        return self.Attachments
    def set_Attachments(self, Attachments):
        self.Attachments = Attachments
    def get_ForeignHAWB(self):
        return self.ForeignHAWB
    def set_ForeignHAWB(self, ForeignHAWB):
        self.ForeignHAWB = ForeignHAWB
    def get_TransportType_x0020_(self):
        return self.TransportType_x0020_
    def set_TransportType_x0020_(self, TransportType_x0020_):
        self.TransportType_x0020_ = TransportType_x0020_
    def get_PickupGUID(self):
        return self.PickupGUID
    def set_PickupGUID(self, PickupGUID):
        self.PickupGUID = PickupGUID
    def hasContent_(self):
        if (
            self.Reference1 is not None or
            self.Reference2 is not None or
            self.Reference3 is not None or
            self.Shipper is not None or
            self.Consignee is not None or
            self.ThirdParty is not None or
            self.ShippingDateTime is not None or
            self.DueDate is not None or
            self.Comments is not None or
            self.PickupLocation is not None or
            self.OperationsInstructions is not None or
            self.AccountingInstrcutions is not None or
            self.Details is not None or
            self.Attachments is not None or
            self.ForeignHAWB is not None or
            self.TransportType_x0020_ is not None or
            self.PickupGUID is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Shipment', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Shipment')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Shipment':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Shipment')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Shipment', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Shipment'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Shipment', fromsubclass_=False, pretty_print=True):
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
        if self.Shipper is not None:
            namespaceprefix_ = self.Shipper_nsprefix_ + ':' if (UseCapturedNS_ and self.Shipper_nsprefix_) else ''
            self.Shipper.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Shipper', pretty_print=pretty_print)
        if self.Consignee is not None:
            namespaceprefix_ = self.Consignee_nsprefix_ + ':' if (UseCapturedNS_ and self.Consignee_nsprefix_) else ''
            self.Consignee.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Consignee', pretty_print=pretty_print)
        if self.ThirdParty is not None:
            namespaceprefix_ = self.ThirdParty_nsprefix_ + ':' if (UseCapturedNS_ and self.ThirdParty_nsprefix_) else ''
            self.ThirdParty.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ThirdParty', pretty_print=pretty_print)
        if self.ShippingDateTime is not None:
            namespaceprefix_ = self.ShippingDateTime_nsprefix_ + ':' if (UseCapturedNS_ and self.ShippingDateTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShippingDateTime>%s</%sShippingDateTime>%s' % (namespaceprefix_ , self.gds_format_datetime(self.ShippingDateTime, input_name='ShippingDateTime'), namespaceprefix_ , eol_))
        if self.DueDate is not None:
            namespaceprefix_ = self.DueDate_nsprefix_ + ':' if (UseCapturedNS_ and self.DueDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDueDate>%s</%sDueDate>%s' % (namespaceprefix_ , self.gds_format_datetime(self.DueDate, input_name='DueDate'), namespaceprefix_ , eol_))
        if self.Comments is not None:
            namespaceprefix_ = self.Comments_nsprefix_ + ':' if (UseCapturedNS_ and self.Comments_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sComments>%s</%sComments>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Comments), input_name='Comments')), namespaceprefix_ , eol_))
        if self.PickupLocation is not None:
            namespaceprefix_ = self.PickupLocation_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupLocation_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupLocation>%s</%sPickupLocation>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupLocation), input_name='PickupLocation')), namespaceprefix_ , eol_))
        if self.OperationsInstructions is not None:
            namespaceprefix_ = self.OperationsInstructions_nsprefix_ + ':' if (UseCapturedNS_ and self.OperationsInstructions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOperationsInstructions>%s</%sOperationsInstructions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OperationsInstructions), input_name='OperationsInstructions')), namespaceprefix_ , eol_))
        if self.AccountingInstrcutions is not None:
            namespaceprefix_ = self.AccountingInstrcutions_nsprefix_ + ':' if (UseCapturedNS_ and self.AccountingInstrcutions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccountingInstrcutions>%s</%sAccountingInstrcutions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AccountingInstrcutions), input_name='AccountingInstrcutions')), namespaceprefix_ , eol_))
        if self.Details is not None:
            namespaceprefix_ = self.Details_nsprefix_ + ':' if (UseCapturedNS_ and self.Details_nsprefix_) else ''
            self.Details.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Details', pretty_print=pretty_print)
        if self.Attachments is not None:
            namespaceprefix_ = self.Attachments_nsprefix_ + ':' if (UseCapturedNS_ and self.Attachments_nsprefix_) else ''
            self.Attachments.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Attachments', pretty_print=pretty_print)
        if self.ForeignHAWB is not None:
            namespaceprefix_ = self.ForeignHAWB_nsprefix_ + ':' if (UseCapturedNS_ and self.ForeignHAWB_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sForeignHAWB>%s</%sForeignHAWB>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ForeignHAWB), input_name='ForeignHAWB')), namespaceprefix_ , eol_))
        if self.TransportType_x0020_ is not None:
            namespaceprefix_ = self.TransportType_x0020__nsprefix_ + ':' if (UseCapturedNS_ and self.TransportType_x0020__nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTransportType_x0020_>%s</%sTransportType_x0020_>%s' % (namespaceprefix_ , self.gds_format_integer(self.TransportType_x0020_, input_name='TransportType_x0020_'), namespaceprefix_ , eol_))
        if self.PickupGUID is not None:
            namespaceprefix_ = self.PickupGUID_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupGUID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupGUID>%s</%sPickupGUID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupGUID), input_name='PickupGUID')), namespaceprefix_ , eol_))
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
        elif nodeName_ == 'Shipper':
            obj_ = Party.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Shipper = obj_
            obj_.original_tagname_ = 'Shipper'
        elif nodeName_ == 'Consignee':
            obj_ = Party.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Consignee = obj_
            obj_.original_tagname_ = 'Consignee'
        elif nodeName_ == 'ThirdParty':
            obj_ = Party.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ThirdParty = obj_
            obj_.original_tagname_ = 'ThirdParty'
        elif nodeName_ == 'ShippingDateTime':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.ShippingDateTime = dval_
            self.ShippingDateTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'DueDate':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.DueDate = dval_
            self.DueDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'Comments':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Comments')
            value_ = self.gds_validate_string(value_, node, 'Comments')
            self.Comments = value_
            self.Comments_nsprefix_ = child_.prefix
        elif nodeName_ == 'PickupLocation':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupLocation')
            value_ = self.gds_validate_string(value_, node, 'PickupLocation')
            self.PickupLocation = value_
            self.PickupLocation_nsprefix_ = child_.prefix
        elif nodeName_ == 'OperationsInstructions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OperationsInstructions')
            value_ = self.gds_validate_string(value_, node, 'OperationsInstructions')
            self.OperationsInstructions = value_
            self.OperationsInstructions_nsprefix_ = child_.prefix
        elif nodeName_ == 'AccountingInstrcutions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AccountingInstrcutions')
            value_ = self.gds_validate_string(value_, node, 'AccountingInstrcutions')
            self.AccountingInstrcutions = value_
            self.AccountingInstrcutions_nsprefix_ = child_.prefix
        elif nodeName_ == 'Details':
            obj_ = ShipmentDetails.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Details = obj_
            obj_.original_tagname_ = 'Details'
        elif nodeName_ == 'Attachments':
            obj_ = ArrayOfAttachment.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Attachments = obj_
            obj_.original_tagname_ = 'Attachments'
        elif nodeName_ == 'ForeignHAWB':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ForeignHAWB')
            value_ = self.gds_validate_string(value_, node, 'ForeignHAWB')
            self.ForeignHAWB = value_
            self.ForeignHAWB_nsprefix_ = child_.prefix
        elif nodeName_ == 'TransportType_x0020_' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'TransportType_x0020_')
            ival_ = self.gds_validate_integer(ival_, node, 'TransportType_x0020_')
            self.TransportType_x0020_ = ival_
            self.TransportType_x0020__nsprefix_ = child_.prefix
        elif nodeName_ == 'PickupGUID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupGUID')
            value_ = self.gds_validate_string(value_, node, 'PickupGUID')
            self.PickupGUID = value_
            self.PickupGUID_nsprefix_ = child_.prefix
# end class Shipment


class Party(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Reference1=None, Reference2=None, AccountNumber=None, PartyAddress=None, Contact=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Reference1 = Reference1
        self.Reference1_nsprefix_ = None
        self.Reference2 = Reference2
        self.Reference2_nsprefix_ = None
        self.AccountNumber = AccountNumber
        self.AccountNumber_nsprefix_ = None
        self.PartyAddress = PartyAddress
        self.PartyAddress_nsprefix_ = None
        self.Contact = Contact
        self.Contact_nsprefix_ = None
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
    def get_Reference1(self):
        return self.Reference1
    def set_Reference1(self, Reference1):
        self.Reference1 = Reference1
    def get_Reference2(self):
        return self.Reference2
    def set_Reference2(self, Reference2):
        self.Reference2 = Reference2
    def get_AccountNumber(self):
        return self.AccountNumber
    def set_AccountNumber(self, AccountNumber):
        self.AccountNumber = AccountNumber
    def get_PartyAddress(self):
        return self.PartyAddress
    def set_PartyAddress(self, PartyAddress):
        self.PartyAddress = PartyAddress
    def get_Contact(self):
        return self.Contact
    def set_Contact(self, Contact):
        self.Contact = Contact
    def hasContent_(self):
        if (
            self.Reference1 is not None or
            self.Reference2 is not None or
            self.AccountNumber is not None or
            self.PartyAddress is not None or
            self.Contact is not None
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
        if self.Reference1 is not None:
            namespaceprefix_ = self.Reference1_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference1>%s</%sReference1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference1), input_name='Reference1')), namespaceprefix_ , eol_))
        if self.Reference2 is not None:
            namespaceprefix_ = self.Reference2_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference2>%s</%sReference2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference2), input_name='Reference2')), namespaceprefix_ , eol_))
        if self.AccountNumber is not None:
            namespaceprefix_ = self.AccountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.AccountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccountNumber>%s</%sAccountNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AccountNumber), input_name='AccountNumber')), namespaceprefix_ , eol_))
        if self.PartyAddress is not None:
            namespaceprefix_ = self.PartyAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.PartyAddress_nsprefix_) else ''
            self.PartyAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PartyAddress', pretty_print=pretty_print)
        if self.Contact is not None:
            namespaceprefix_ = self.Contact_nsprefix_ + ':' if (UseCapturedNS_ and self.Contact_nsprefix_) else ''
            self.Contact.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Contact', pretty_print=pretty_print)
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
        elif nodeName_ == 'AccountNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AccountNumber')
            value_ = self.gds_validate_string(value_, node, 'AccountNumber')
            self.AccountNumber = value_
            self.AccountNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'PartyAddress':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PartyAddress = obj_
            obj_.original_tagname_ = 'PartyAddress'
        elif nodeName_ == 'Contact':
            obj_ = Contact.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Contact = obj_
            obj_.original_tagname_ = 'Contact'
# end class Party


class Address(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Line1=None, Line2=None, Line3=None, City=None, StateOrProvinceCode=None, PostCode=None, CountryCode=None, gds_collector_=None, **kwargs_):
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
    def hasContent_(self):
        if (
            self.Line1 is not None or
            self.Line2 is not None or
            self.Line3 is not None or
            self.City is not None or
            self.StateOrProvinceCode is not None or
            self.PostCode is not None or
            self.CountryCode is not None
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
# end class Address


class Contact(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Department=None, PersonName=None, Title=None, CompanyName=None, PhoneNumber1=None, PhoneNumber1Ext=None, PhoneNumber2=None, PhoneNumber2Ext=None, FaxNumber=None, CellPhone=None, EmailAddress=None, Type=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Department = Department
        self.Department_nsprefix_ = None
        self.PersonName = PersonName
        self.PersonName_nsprefix_ = None
        self.Title = Title
        self.Title_nsprefix_ = None
        self.CompanyName = CompanyName
        self.CompanyName_nsprefix_ = None
        self.PhoneNumber1 = PhoneNumber1
        self.PhoneNumber1_nsprefix_ = None
        self.PhoneNumber1Ext = PhoneNumber1Ext
        self.PhoneNumber1Ext_nsprefix_ = None
        self.PhoneNumber2 = PhoneNumber2
        self.PhoneNumber2_nsprefix_ = None
        self.PhoneNumber2Ext = PhoneNumber2Ext
        self.PhoneNumber2Ext_nsprefix_ = None
        self.FaxNumber = FaxNumber
        self.FaxNumber_nsprefix_ = None
        self.CellPhone = CellPhone
        self.CellPhone_nsprefix_ = None
        self.EmailAddress = EmailAddress
        self.EmailAddress_nsprefix_ = None
        self.Type = Type
        self.Type_nsprefix_ = None
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
    def get_Department(self):
        return self.Department
    def set_Department(self, Department):
        self.Department = Department
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
    def get_PhoneNumber1(self):
        return self.PhoneNumber1
    def set_PhoneNumber1(self, PhoneNumber1):
        self.PhoneNumber1 = PhoneNumber1
    def get_PhoneNumber1Ext(self):
        return self.PhoneNumber1Ext
    def set_PhoneNumber1Ext(self, PhoneNumber1Ext):
        self.PhoneNumber1Ext = PhoneNumber1Ext
    def get_PhoneNumber2(self):
        return self.PhoneNumber2
    def set_PhoneNumber2(self, PhoneNumber2):
        self.PhoneNumber2 = PhoneNumber2
    def get_PhoneNumber2Ext(self):
        return self.PhoneNumber2Ext
    def set_PhoneNumber2Ext(self, PhoneNumber2Ext):
        self.PhoneNumber2Ext = PhoneNumber2Ext
    def get_FaxNumber(self):
        return self.FaxNumber
    def set_FaxNumber(self, FaxNumber):
        self.FaxNumber = FaxNumber
    def get_CellPhone(self):
        return self.CellPhone
    def set_CellPhone(self, CellPhone):
        self.CellPhone = CellPhone
    def get_EmailAddress(self):
        return self.EmailAddress
    def set_EmailAddress(self, EmailAddress):
        self.EmailAddress = EmailAddress
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def hasContent_(self):
        if (
            self.Department is not None or
            self.PersonName is not None or
            self.Title is not None or
            self.CompanyName is not None or
            self.PhoneNumber1 is not None or
            self.PhoneNumber1Ext is not None or
            self.PhoneNumber2 is not None or
            self.PhoneNumber2Ext is not None or
            self.FaxNumber is not None or
            self.CellPhone is not None or
            self.EmailAddress is not None or
            self.Type is not None
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
        if self.Department is not None:
            namespaceprefix_ = self.Department_nsprefix_ + ':' if (UseCapturedNS_ and self.Department_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDepartment>%s</%sDepartment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Department), input_name='Department')), namespaceprefix_ , eol_))
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
        if self.PhoneNumber1 is not None:
            namespaceprefix_ = self.PhoneNumber1_nsprefix_ + ':' if (UseCapturedNS_ and self.PhoneNumber1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPhoneNumber1>%s</%sPhoneNumber1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PhoneNumber1), input_name='PhoneNumber1')), namespaceprefix_ , eol_))
        if self.PhoneNumber1Ext is not None:
            namespaceprefix_ = self.PhoneNumber1Ext_nsprefix_ + ':' if (UseCapturedNS_ and self.PhoneNumber1Ext_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPhoneNumber1Ext>%s</%sPhoneNumber1Ext>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PhoneNumber1Ext), input_name='PhoneNumber1Ext')), namespaceprefix_ , eol_))
        if self.PhoneNumber2 is not None:
            namespaceprefix_ = self.PhoneNumber2_nsprefix_ + ':' if (UseCapturedNS_ and self.PhoneNumber2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPhoneNumber2>%s</%sPhoneNumber2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PhoneNumber2), input_name='PhoneNumber2')), namespaceprefix_ , eol_))
        if self.PhoneNumber2Ext is not None:
            namespaceprefix_ = self.PhoneNumber2Ext_nsprefix_ + ':' if (UseCapturedNS_ and self.PhoneNumber2Ext_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPhoneNumber2Ext>%s</%sPhoneNumber2Ext>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PhoneNumber2Ext), input_name='PhoneNumber2Ext')), namespaceprefix_ , eol_))
        if self.FaxNumber is not None:
            namespaceprefix_ = self.FaxNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.FaxNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFaxNumber>%s</%sFaxNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FaxNumber), input_name='FaxNumber')), namespaceprefix_ , eol_))
        if self.CellPhone is not None:
            namespaceprefix_ = self.CellPhone_nsprefix_ + ':' if (UseCapturedNS_ and self.CellPhone_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCellPhone>%s</%sCellPhone>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CellPhone), input_name='CellPhone')), namespaceprefix_ , eol_))
        if self.EmailAddress is not None:
            namespaceprefix_ = self.EmailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.EmailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEmailAddress>%s</%sEmailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EmailAddress), input_name='EmailAddress')), namespaceprefix_ , eol_))
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sType>%s</%sType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Type), input_name='Type')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Department':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Department')
            value_ = self.gds_validate_string(value_, node, 'Department')
            self.Department = value_
            self.Department_nsprefix_ = child_.prefix
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
        elif nodeName_ == 'PhoneNumber1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PhoneNumber1')
            value_ = self.gds_validate_string(value_, node, 'PhoneNumber1')
            self.PhoneNumber1 = value_
            self.PhoneNumber1_nsprefix_ = child_.prefix
        elif nodeName_ == 'PhoneNumber1Ext':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PhoneNumber1Ext')
            value_ = self.gds_validate_string(value_, node, 'PhoneNumber1Ext')
            self.PhoneNumber1Ext = value_
            self.PhoneNumber1Ext_nsprefix_ = child_.prefix
        elif nodeName_ == 'PhoneNumber2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PhoneNumber2')
            value_ = self.gds_validate_string(value_, node, 'PhoneNumber2')
            self.PhoneNumber2 = value_
            self.PhoneNumber2_nsprefix_ = child_.prefix
        elif nodeName_ == 'PhoneNumber2Ext':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PhoneNumber2Ext')
            value_ = self.gds_validate_string(value_, node, 'PhoneNumber2Ext')
            self.PhoneNumber2Ext = value_
            self.PhoneNumber2Ext_nsprefix_ = child_.prefix
        elif nodeName_ == 'FaxNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FaxNumber')
            value_ = self.gds_validate_string(value_, node, 'FaxNumber')
            self.FaxNumber = value_
            self.FaxNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'CellPhone':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CellPhone')
            value_ = self.gds_validate_string(value_, node, 'CellPhone')
            self.CellPhone = value_
            self.CellPhone_nsprefix_ = child_.prefix
        elif nodeName_ == 'EmailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EmailAddress')
            value_ = self.gds_validate_string(value_, node, 'EmailAddress')
            self.EmailAddress = value_
            self.EmailAddress_nsprefix_ = child_.prefix
        elif nodeName_ == 'Type':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Type')
            value_ = self.gds_validate_string(value_, node, 'Type')
            self.Type = value_
            self.Type_nsprefix_ = child_.prefix
# end class Contact


class ShipmentDetails(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Dimensions=None, ActualWeight=None, ChargeableWeight=None, DescriptionOfGoods=None, GoodsOriginCountry=None, NumberOfPieces=None, ProductGroup=None, ProductType=None, PaymentType=None, PaymentOptions=None, CustomsValueAmount=None, CashOnDeliveryAmount=None, InsuranceAmount=None, CashAdditionalAmount=None, CashAdditionalAmountDescription=None, CollectAmount=None, Services=None, Items=None, gds_collector_=None, **kwargs_):
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
            self.Items is not None
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
    def __init__(self, PackageType=None, Quantity=None, Weight=None, Comments=None, Reference=None, gds_collector_=None, **kwargs_):
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
    def hasContent_(self):
        if (
            self.PackageType is not None or
            self.Quantity is not None or
            self.Weight is not None or
            self.Comments is not None or
            self.Reference is not None
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
# end class ShipmentItem


class ArrayOfAttachment(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Attachment=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Attachment is None:
            self.Attachment = []
        else:
            self.Attachment = Attachment
        self.Attachment_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfAttachment)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfAttachment.subclass:
            return ArrayOfAttachment.subclass(*args_, **kwargs_)
        else:
            return ArrayOfAttachment(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Attachment(self):
        return self.Attachment
    def set_Attachment(self, Attachment):
        self.Attachment = Attachment
    def add_Attachment(self, value):
        self.Attachment.append(value)
    def insert_Attachment_at(self, index, value):
        self.Attachment.insert(index, value)
    def replace_Attachment_at(self, index, value):
        self.Attachment[index] = value
    def hasContent_(self):
        if (
            self.Attachment
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfAttachment', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfAttachment')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfAttachment':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfAttachment')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfAttachment', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfAttachment'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfAttachment', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Attachment_ in self.Attachment:
            namespaceprefix_ = self.Attachment_nsprefix_ + ':' if (UseCapturedNS_ and self.Attachment_nsprefix_) else ''
            Attachment_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Attachment', pretty_print=pretty_print)
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
        if nodeName_ == 'Attachment':
            obj_ = Attachment.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Attachment.append(obj_)
            obj_.original_tagname_ = 'Attachment'
# end class ArrayOfAttachment


class Attachment(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, FileName=None, FileExtension=None, FileContents=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.FileName = FileName
        self.FileName_nsprefix_ = None
        self.FileExtension = FileExtension
        self.FileExtension_nsprefix_ = None
        self.FileContents = FileContents
        self.FileContents_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Attachment)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Attachment.subclass:
            return Attachment.subclass(*args_, **kwargs_)
        else:
            return Attachment(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_FileName(self):
        return self.FileName
    def set_FileName(self, FileName):
        self.FileName = FileName
    def get_FileExtension(self):
        return self.FileExtension
    def set_FileExtension(self, FileExtension):
        self.FileExtension = FileExtension
    def get_FileContents(self):
        return self.FileContents
    def set_FileContents(self, FileContents):
        self.FileContents = FileContents
    def hasContent_(self):
        if (
            self.FileName is not None or
            self.FileExtension is not None or
            self.FileContents is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Attachment', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Attachment')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Attachment':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Attachment')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Attachment', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Attachment'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Attachment', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.FileName is not None:
            namespaceprefix_ = self.FileName_nsprefix_ + ':' if (UseCapturedNS_ and self.FileName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFileName>%s</%sFileName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FileName), input_name='FileName')), namespaceprefix_ , eol_))
        if self.FileExtension is not None:
            namespaceprefix_ = self.FileExtension_nsprefix_ + ':' if (UseCapturedNS_ and self.FileExtension_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFileExtension>%s</%sFileExtension>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FileExtension), input_name='FileExtension')), namespaceprefix_ , eol_))
        if self.FileContents is not None:
            namespaceprefix_ = self.FileContents_nsprefix_ + ':' if (UseCapturedNS_ and self.FileContents_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFileContents>%s</%sFileContents>%s' % (namespaceprefix_ , self.gds_format_base64(self.FileContents, input_name='FileContents'), namespaceprefix_ , eol_))
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
        elif nodeName_ == 'FileExtension':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FileExtension')
            value_ = self.gds_validate_string(value_, node, 'FileExtension')
            self.FileExtension = value_
            self.FileExtension_nsprefix_ = child_.prefix
        elif nodeName_ == 'FileContents':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'FileContents')
            else:
                bval_ = None
            self.FileContents = bval_
            self.FileContents_nsprefix_ = child_.prefix
# end class Attachment


class LabelInfo(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ReportID=None, ReportType=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ReportID = ReportID
        self.ReportID_nsprefix_ = None
        self.ReportType = ReportType
        self.ReportType_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LabelInfo)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LabelInfo.subclass:
            return LabelInfo.subclass(*args_, **kwargs_)
        else:
            return LabelInfo(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ReportID(self):
        return self.ReportID
    def set_ReportID(self, ReportID):
        self.ReportID = ReportID
    def get_ReportType(self):
        return self.ReportType
    def set_ReportType(self, ReportType):
        self.ReportType = ReportType
    def hasContent_(self):
        if (
            self.ReportID is not None or
            self.ReportType is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LabelInfo', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LabelInfo')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LabelInfo':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LabelInfo')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LabelInfo', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LabelInfo'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LabelInfo', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ReportID is not None:
            namespaceprefix_ = self.ReportID_nsprefix_ + ':' if (UseCapturedNS_ and self.ReportID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReportID>%s</%sReportID>%s' % (namespaceprefix_ , self.gds_format_integer(self.ReportID, input_name='ReportID'), namespaceprefix_ , eol_))
        if self.ReportType is not None:
            namespaceprefix_ = self.ReportType_nsprefix_ + ':' if (UseCapturedNS_ and self.ReportType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReportType>%s</%sReportType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ReportType), input_name='ReportType')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ReportID' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'ReportID')
            ival_ = self.gds_validate_integer(ival_, node, 'ReportID')
            self.ReportID = ival_
            self.ReportID_nsprefix_ = child_.prefix
        elif nodeName_ == 'ReportType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ReportType')
            value_ = self.gds_validate_string(value_, node, 'ReportType')
            self.ReportType = value_
            self.ReportType_nsprefix_ = child_.prefix
# end class LabelInfo


class ShipmentCreationResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Transaction=None, Notifications=None, HasErrors=None, Shipments=None, gds_collector_=None, **kwargs_):
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
        self.Shipments = Shipments
        self.Shipments_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentCreationResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentCreationResponse.subclass:
            return ShipmentCreationResponse.subclass(*args_, **kwargs_)
        else:
            return ShipmentCreationResponse(*args_, **kwargs_)
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
    def get_Shipments(self):
        return self.Shipments
    def set_Shipments(self, Shipments):
        self.Shipments = Shipments
    def hasContent_(self):
        if (
            self.Transaction is not None or
            self.Notifications is not None or
            self.HasErrors is not None or
            self.Shipments is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentCreationResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentCreationResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentCreationResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentCreationResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentCreationResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentCreationResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentCreationResponse', fromsubclass_=False, pretty_print=True):
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
        if self.Shipments is not None:
            namespaceprefix_ = self.Shipments_nsprefix_ + ':' if (UseCapturedNS_ and self.Shipments_nsprefix_) else ''
            self.Shipments.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Shipments', pretty_print=pretty_print)
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
        elif nodeName_ == 'Shipments':
            obj_ = ArrayOfProcessedShipment.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Shipments = obj_
            obj_.original_tagname_ = 'Shipments'
# end class ShipmentCreationResponse


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


class ArrayOfProcessedShipment(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ProcessedShipment=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if ProcessedShipment is None:
            self.ProcessedShipment = []
        else:
            self.ProcessedShipment = ProcessedShipment
        self.ProcessedShipment_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfProcessedShipment)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfProcessedShipment.subclass:
            return ArrayOfProcessedShipment.subclass(*args_, **kwargs_)
        else:
            return ArrayOfProcessedShipment(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ProcessedShipment(self):
        return self.ProcessedShipment
    def set_ProcessedShipment(self, ProcessedShipment):
        self.ProcessedShipment = ProcessedShipment
    def add_ProcessedShipment(self, value):
        self.ProcessedShipment.append(value)
    def insert_ProcessedShipment_at(self, index, value):
        self.ProcessedShipment.insert(index, value)
    def replace_ProcessedShipment_at(self, index, value):
        self.ProcessedShipment[index] = value
    def hasContent_(self):
        if (
            self.ProcessedShipment
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfProcessedShipment', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfProcessedShipment')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfProcessedShipment':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfProcessedShipment')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfProcessedShipment', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfProcessedShipment'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfProcessedShipment', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for ProcessedShipment_ in self.ProcessedShipment:
            namespaceprefix_ = self.ProcessedShipment_nsprefix_ + ':' if (UseCapturedNS_ and self.ProcessedShipment_nsprefix_) else ''
            ProcessedShipment_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ProcessedShipment', pretty_print=pretty_print)
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
        if nodeName_ == 'ProcessedShipment':
            obj_ = ProcessedShipment.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ProcessedShipment.append(obj_)
            obj_.original_tagname_ = 'ProcessedShipment'
# end class ArrayOfProcessedShipment


class ProcessedShipment(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ID=None, Reference1=None, Reference2=None, Reference3=None, ForeignHAWB=None, HasErrors=None, Notifications=None, ShipmentLabel=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ID = ID
        self.ID_nsprefix_ = None
        self.Reference1 = Reference1
        self.Reference1_nsprefix_ = None
        self.Reference2 = Reference2
        self.Reference2_nsprefix_ = None
        self.Reference3 = Reference3
        self.Reference3_nsprefix_ = None
        self.ForeignHAWB = ForeignHAWB
        self.ForeignHAWB_nsprefix_ = None
        self.HasErrors = HasErrors
        self.HasErrors_nsprefix_ = None
        self.Notifications = Notifications
        self.Notifications_nsprefix_ = None
        self.ShipmentLabel = ShipmentLabel
        self.ShipmentLabel_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ProcessedShipment)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ProcessedShipment.subclass:
            return ProcessedShipment.subclass(*args_, **kwargs_)
        else:
            return ProcessedShipment(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ID(self):
        return self.ID
    def set_ID(self, ID):
        self.ID = ID
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
    def get_ForeignHAWB(self):
        return self.ForeignHAWB
    def set_ForeignHAWB(self, ForeignHAWB):
        self.ForeignHAWB = ForeignHAWB
    def get_HasErrors(self):
        return self.HasErrors
    def set_HasErrors(self, HasErrors):
        self.HasErrors = HasErrors
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def get_ShipmentLabel(self):
        return self.ShipmentLabel
    def set_ShipmentLabel(self, ShipmentLabel):
        self.ShipmentLabel = ShipmentLabel
    def hasContent_(self):
        if (
            self.ID is not None or
            self.Reference1 is not None or
            self.Reference2 is not None or
            self.Reference3 is not None or
            self.ForeignHAWB is not None or
            self.HasErrors is not None or
            self.Notifications is not None or
            self.ShipmentLabel is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ProcessedShipment', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ProcessedShipment')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ProcessedShipment':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ProcessedShipment')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ProcessedShipment', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ProcessedShipment'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ProcessedShipment', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ID is not None:
            namespaceprefix_ = self.ID_nsprefix_ + ':' if (UseCapturedNS_ and self.ID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sID>%s</%sID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ID), input_name='ID')), namespaceprefix_ , eol_))
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
        if self.ForeignHAWB is not None:
            namespaceprefix_ = self.ForeignHAWB_nsprefix_ + ':' if (UseCapturedNS_ and self.ForeignHAWB_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sForeignHAWB>%s</%sForeignHAWB>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ForeignHAWB), input_name='ForeignHAWB')), namespaceprefix_ , eol_))
        if self.HasErrors is not None:
            namespaceprefix_ = self.HasErrors_nsprefix_ + ':' if (UseCapturedNS_ and self.HasErrors_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHasErrors>%s</%sHasErrors>%s' % (namespaceprefix_ , self.gds_format_boolean(self.HasErrors, input_name='HasErrors'), namespaceprefix_ , eol_))
        if self.Notifications is not None:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            self.Notifications.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.ShipmentLabel is not None:
            namespaceprefix_ = self.ShipmentLabel_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentLabel_nsprefix_) else ''
            self.ShipmentLabel.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentLabel', pretty_print=pretty_print)
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
        if nodeName_ == 'ID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ID')
            value_ = self.gds_validate_string(value_, node, 'ID')
            self.ID = value_
            self.ID_nsprefix_ = child_.prefix
        elif nodeName_ == 'Reference1':
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
        elif nodeName_ == 'ForeignHAWB':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ForeignHAWB')
            value_ = self.gds_validate_string(value_, node, 'ForeignHAWB')
            self.ForeignHAWB = value_
            self.ForeignHAWB_nsprefix_ = child_.prefix
        elif nodeName_ == 'HasErrors':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'HasErrors')
            ival_ = self.gds_validate_boolean(ival_, node, 'HasErrors')
            self.HasErrors = ival_
            self.HasErrors_nsprefix_ = child_.prefix
        elif nodeName_ == 'Notifications':
            obj_ = ArrayOfNotification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications = obj_
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'ShipmentLabel':
            obj_ = ShipmentLabel.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentLabel = obj_
            obj_.original_tagname_ = 'ShipmentLabel'
# end class ProcessedShipment


class ShipmentLabel(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, LabelURL=None, LabelFileContents=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.LabelURL = LabelURL
        self.LabelURL_nsprefix_ = None
        self.LabelFileContents = LabelFileContents
        self.LabelFileContents_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentLabel)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentLabel.subclass:
            return ShipmentLabel.subclass(*args_, **kwargs_)
        else:
            return ShipmentLabel(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_LabelURL(self):
        return self.LabelURL
    def set_LabelURL(self, LabelURL):
        self.LabelURL = LabelURL
    def get_LabelFileContents(self):
        return self.LabelFileContents
    def set_LabelFileContents(self, LabelFileContents):
        self.LabelFileContents = LabelFileContents
    def hasContent_(self):
        if (
            self.LabelURL is not None or
            self.LabelFileContents is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentLabel', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentLabel')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentLabel':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentLabel')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentLabel', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentLabel'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentLabel', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.LabelURL is not None:
            namespaceprefix_ = self.LabelURL_nsprefix_ + ':' if (UseCapturedNS_ and self.LabelURL_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLabelURL>%s</%sLabelURL>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LabelURL), input_name='LabelURL')), namespaceprefix_ , eol_))
        if self.LabelFileContents is not None:
            namespaceprefix_ = self.LabelFileContents_nsprefix_ + ':' if (UseCapturedNS_ and self.LabelFileContents_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLabelFileContents>%s</%sLabelFileContents>%s' % (namespaceprefix_ , self.gds_format_base64(self.LabelFileContents, input_name='LabelFileContents'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'LabelURL':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LabelURL')
            value_ = self.gds_validate_string(value_, node, 'LabelURL')
            self.LabelURL = value_
            self.LabelURL_nsprefix_ = child_.prefix
        elif nodeName_ == 'LabelFileContents':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'LabelFileContents')
            else:
                bval_ = None
            self.LabelFileContents = bval_
            self.LabelFileContents_nsprefix_ = child_.prefix
# end class ShipmentLabel


class LabelPrintingRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ClientInfo=None, Transaction=None, ShipmentNumber=None, ProductGroup=None, OriginEntity=None, LabelInfo=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ClientInfo = ClientInfo
        self.ClientInfo_nsprefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.ShipmentNumber = ShipmentNumber
        self.ShipmentNumber_nsprefix_ = None
        self.ProductGroup = ProductGroup
        self.ProductGroup_nsprefix_ = None
        self.OriginEntity = OriginEntity
        self.OriginEntity_nsprefix_ = None
        self.LabelInfo = LabelInfo
        self.LabelInfo_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LabelPrintingRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LabelPrintingRequest.subclass:
            return LabelPrintingRequest.subclass(*args_, **kwargs_)
        else:
            return LabelPrintingRequest(*args_, **kwargs_)
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
    def get_ShipmentNumber(self):
        return self.ShipmentNumber
    def set_ShipmentNumber(self, ShipmentNumber):
        self.ShipmentNumber = ShipmentNumber
    def get_ProductGroup(self):
        return self.ProductGroup
    def set_ProductGroup(self, ProductGroup):
        self.ProductGroup = ProductGroup
    def get_OriginEntity(self):
        return self.OriginEntity
    def set_OriginEntity(self, OriginEntity):
        self.OriginEntity = OriginEntity
    def get_LabelInfo(self):
        return self.LabelInfo
    def set_LabelInfo(self, LabelInfo):
        self.LabelInfo = LabelInfo
    def hasContent_(self):
        if (
            self.ClientInfo is not None or
            self.Transaction is not None or
            self.ShipmentNumber is not None or
            self.ProductGroup is not None or
            self.OriginEntity is not None or
            self.LabelInfo is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LabelPrintingRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LabelPrintingRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LabelPrintingRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LabelPrintingRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LabelPrintingRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LabelPrintingRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LabelPrintingRequest', fromsubclass_=False, pretty_print=True):
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
        if self.ShipmentNumber is not None:
            namespaceprefix_ = self.ShipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipmentNumber>%s</%sShipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShipmentNumber), input_name='ShipmentNumber')), namespaceprefix_ , eol_))
        if self.ProductGroup is not None:
            namespaceprefix_ = self.ProductGroup_nsprefix_ + ':' if (UseCapturedNS_ and self.ProductGroup_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProductGroup>%s</%sProductGroup>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ProductGroup), input_name='ProductGroup')), namespaceprefix_ , eol_))
        if self.OriginEntity is not None:
            namespaceprefix_ = self.OriginEntity_nsprefix_ + ':' if (UseCapturedNS_ and self.OriginEntity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOriginEntity>%s</%sOriginEntity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OriginEntity), input_name='OriginEntity')), namespaceprefix_ , eol_))
        if self.LabelInfo is not None:
            namespaceprefix_ = self.LabelInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.LabelInfo_nsprefix_) else ''
            self.LabelInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='LabelInfo', pretty_print=pretty_print)
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
        elif nodeName_ == 'ShipmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShipmentNumber')
            value_ = self.gds_validate_string(value_, node, 'ShipmentNumber')
            self.ShipmentNumber = value_
            self.ShipmentNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'ProductGroup':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ProductGroup')
            value_ = self.gds_validate_string(value_, node, 'ProductGroup')
            self.ProductGroup = value_
            self.ProductGroup_nsprefix_ = child_.prefix
        elif nodeName_ == 'OriginEntity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OriginEntity')
            value_ = self.gds_validate_string(value_, node, 'OriginEntity')
            self.OriginEntity = value_
            self.OriginEntity_nsprefix_ = child_.prefix
        elif nodeName_ == 'LabelInfo':
            obj_ = LabelInfo.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LabelInfo = obj_
            obj_.original_tagname_ = 'LabelInfo'
# end class LabelPrintingRequest


class LabelPrintingResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Transaction=None, Notifications=None, HasErrors=None, ShipmentNumber=None, ShipmentLabel=None, gds_collector_=None, **kwargs_):
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
        self.ShipmentNumber = ShipmentNumber
        self.ShipmentNumber_nsprefix_ = None
        self.ShipmentLabel = ShipmentLabel
        self.ShipmentLabel_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LabelPrintingResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LabelPrintingResponse.subclass:
            return LabelPrintingResponse.subclass(*args_, **kwargs_)
        else:
            return LabelPrintingResponse(*args_, **kwargs_)
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
    def get_ShipmentNumber(self):
        return self.ShipmentNumber
    def set_ShipmentNumber(self, ShipmentNumber):
        self.ShipmentNumber = ShipmentNumber
    def get_ShipmentLabel(self):
        return self.ShipmentLabel
    def set_ShipmentLabel(self, ShipmentLabel):
        self.ShipmentLabel = ShipmentLabel
    def hasContent_(self):
        if (
            self.Transaction is not None or
            self.Notifications is not None or
            self.HasErrors is not None or
            self.ShipmentNumber is not None or
            self.ShipmentLabel is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LabelPrintingResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LabelPrintingResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LabelPrintingResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LabelPrintingResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LabelPrintingResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LabelPrintingResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LabelPrintingResponse', fromsubclass_=False, pretty_print=True):
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
        if self.ShipmentNumber is not None:
            namespaceprefix_ = self.ShipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipmentNumber>%s</%sShipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShipmentNumber), input_name='ShipmentNumber')), namespaceprefix_ , eol_))
        if self.ShipmentLabel is not None:
            namespaceprefix_ = self.ShipmentLabel_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentLabel_nsprefix_) else ''
            self.ShipmentLabel.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentLabel', pretty_print=pretty_print)
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
        elif nodeName_ == 'ShipmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShipmentNumber')
            value_ = self.gds_validate_string(value_, node, 'ShipmentNumber')
            self.ShipmentNumber = value_
            self.ShipmentNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'ShipmentLabel':
            obj_ = ShipmentLabel.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentLabel = obj_
            obj_.original_tagname_ = 'ShipmentLabel'
# end class LabelPrintingResponse


class PickupCreationRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ClientInfo=None, Transaction=None, Pickup=None, LabelInfo=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ClientInfo = ClientInfo
        self.ClientInfo_nsprefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.Pickup = Pickup
        self.Pickup_nsprefix_ = None
        self.LabelInfo = LabelInfo
        self.LabelInfo_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PickupCreationRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PickupCreationRequest.subclass:
            return PickupCreationRequest.subclass(*args_, **kwargs_)
        else:
            return PickupCreationRequest(*args_, **kwargs_)
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
    def get_Pickup(self):
        return self.Pickup
    def set_Pickup(self, Pickup):
        self.Pickup = Pickup
    def get_LabelInfo(self):
        return self.LabelInfo
    def set_LabelInfo(self, LabelInfo):
        self.LabelInfo = LabelInfo
    def hasContent_(self):
        if (
            self.ClientInfo is not None or
            self.Transaction is not None or
            self.Pickup is not None or
            self.LabelInfo is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupCreationRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PickupCreationRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PickupCreationRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PickupCreationRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PickupCreationRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PickupCreationRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupCreationRequest', fromsubclass_=False, pretty_print=True):
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
        if self.Pickup is not None:
            namespaceprefix_ = self.Pickup_nsprefix_ + ':' if (UseCapturedNS_ and self.Pickup_nsprefix_) else ''
            self.Pickup.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Pickup', pretty_print=pretty_print)
        if self.LabelInfo is not None:
            namespaceprefix_ = self.LabelInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.LabelInfo_nsprefix_) else ''
            self.LabelInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='LabelInfo', pretty_print=pretty_print)
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
        elif nodeName_ == 'Pickup':
            obj_ = Pickup.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Pickup = obj_
            obj_.original_tagname_ = 'Pickup'
        elif nodeName_ == 'LabelInfo':
            obj_ = LabelInfo.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LabelInfo = obj_
            obj_.original_tagname_ = 'LabelInfo'
# end class PickupCreationRequest


class Pickup(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PickupAddress=None, PickupContact=None, PickupLocation=None, PickupDate=None, ReadyTime=None, LastPickupTime=None, ClosingTime=None, Comments=None, Reference1=None, Reference2=None, Vehicle=None, Shipments=None, PickupItems=None, Status=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PickupAddress = PickupAddress
        self.PickupAddress_nsprefix_ = None
        self.PickupContact = PickupContact
        self.PickupContact_nsprefix_ = None
        self.PickupLocation = PickupLocation
        self.PickupLocation_nsprefix_ = None
        if isinstance(PickupDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(PickupDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = PickupDate
        self.PickupDate = initvalue_
        self.PickupDate_nsprefix_ = None
        if isinstance(ReadyTime, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ReadyTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = ReadyTime
        self.ReadyTime = initvalue_
        self.ReadyTime_nsprefix_ = None
        if isinstance(LastPickupTime, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(LastPickupTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = LastPickupTime
        self.LastPickupTime = initvalue_
        self.LastPickupTime_nsprefix_ = None
        if isinstance(ClosingTime, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ClosingTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = ClosingTime
        self.ClosingTime = initvalue_
        self.ClosingTime_nsprefix_ = None
        self.Comments = Comments
        self.Comments_nsprefix_ = None
        self.Reference1 = Reference1
        self.Reference1_nsprefix_ = None
        self.Reference2 = Reference2
        self.Reference2_nsprefix_ = None
        self.Vehicle = Vehicle
        self.Vehicle_nsprefix_ = None
        self.Shipments = Shipments
        self.Shipments_nsprefix_ = None
        self.PickupItems = PickupItems
        self.PickupItems_nsprefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Pickup)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Pickup.subclass:
            return Pickup.subclass(*args_, **kwargs_)
        else:
            return Pickup(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PickupAddress(self):
        return self.PickupAddress
    def set_PickupAddress(self, PickupAddress):
        self.PickupAddress = PickupAddress
    def get_PickupContact(self):
        return self.PickupContact
    def set_PickupContact(self, PickupContact):
        self.PickupContact = PickupContact
    def get_PickupLocation(self):
        return self.PickupLocation
    def set_PickupLocation(self, PickupLocation):
        self.PickupLocation = PickupLocation
    def get_PickupDate(self):
        return self.PickupDate
    def set_PickupDate(self, PickupDate):
        self.PickupDate = PickupDate
    def get_ReadyTime(self):
        return self.ReadyTime
    def set_ReadyTime(self, ReadyTime):
        self.ReadyTime = ReadyTime
    def get_LastPickupTime(self):
        return self.LastPickupTime
    def set_LastPickupTime(self, LastPickupTime):
        self.LastPickupTime = LastPickupTime
    def get_ClosingTime(self):
        return self.ClosingTime
    def set_ClosingTime(self, ClosingTime):
        self.ClosingTime = ClosingTime
    def get_Comments(self):
        return self.Comments
    def set_Comments(self, Comments):
        self.Comments = Comments
    def get_Reference1(self):
        return self.Reference1
    def set_Reference1(self, Reference1):
        self.Reference1 = Reference1
    def get_Reference2(self):
        return self.Reference2
    def set_Reference2(self, Reference2):
        self.Reference2 = Reference2
    def get_Vehicle(self):
        return self.Vehicle
    def set_Vehicle(self, Vehicle):
        self.Vehicle = Vehicle
    def get_Shipments(self):
        return self.Shipments
    def set_Shipments(self, Shipments):
        self.Shipments = Shipments
    def get_PickupItems(self):
        return self.PickupItems
    def set_PickupItems(self, PickupItems):
        self.PickupItems = PickupItems
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def hasContent_(self):
        if (
            self.PickupAddress is not None or
            self.PickupContact is not None or
            self.PickupLocation is not None or
            self.PickupDate is not None or
            self.ReadyTime is not None or
            self.LastPickupTime is not None or
            self.ClosingTime is not None or
            self.Comments is not None or
            self.Reference1 is not None or
            self.Reference2 is not None or
            self.Vehicle is not None or
            self.Shipments is not None or
            self.PickupItems is not None or
            self.Status is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Pickup', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Pickup')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Pickup':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Pickup')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Pickup', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Pickup'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Pickup', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PickupAddress is not None:
            namespaceprefix_ = self.PickupAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupAddress_nsprefix_) else ''
            self.PickupAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PickupAddress', pretty_print=pretty_print)
        if self.PickupContact is not None:
            namespaceprefix_ = self.PickupContact_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupContact_nsprefix_) else ''
            self.PickupContact.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PickupContact', pretty_print=pretty_print)
        if self.PickupLocation is not None:
            namespaceprefix_ = self.PickupLocation_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupLocation_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupLocation>%s</%sPickupLocation>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupLocation), input_name='PickupLocation')), namespaceprefix_ , eol_))
        if self.PickupDate is not None:
            namespaceprefix_ = self.PickupDate_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupDate>%s</%sPickupDate>%s' % (namespaceprefix_ , self.gds_format_datetime(self.PickupDate, input_name='PickupDate'), namespaceprefix_ , eol_))
        if self.ReadyTime is not None:
            namespaceprefix_ = self.ReadyTime_nsprefix_ + ':' if (UseCapturedNS_ and self.ReadyTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReadyTime>%s</%sReadyTime>%s' % (namespaceprefix_ , self.gds_format_datetime(self.ReadyTime, input_name='ReadyTime'), namespaceprefix_ , eol_))
        if self.LastPickupTime is not None:
            namespaceprefix_ = self.LastPickupTime_nsprefix_ + ':' if (UseCapturedNS_ and self.LastPickupTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLastPickupTime>%s</%sLastPickupTime>%s' % (namespaceprefix_ , self.gds_format_datetime(self.LastPickupTime, input_name='LastPickupTime'), namespaceprefix_ , eol_))
        if self.ClosingTime is not None:
            namespaceprefix_ = self.ClosingTime_nsprefix_ + ':' if (UseCapturedNS_ and self.ClosingTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sClosingTime>%s</%sClosingTime>%s' % (namespaceprefix_ , self.gds_format_datetime(self.ClosingTime, input_name='ClosingTime'), namespaceprefix_ , eol_))
        if self.Comments is not None:
            namespaceprefix_ = self.Comments_nsprefix_ + ':' if (UseCapturedNS_ and self.Comments_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sComments>%s</%sComments>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Comments), input_name='Comments')), namespaceprefix_ , eol_))
        if self.Reference1 is not None:
            namespaceprefix_ = self.Reference1_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference1>%s</%sReference1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference1), input_name='Reference1')), namespaceprefix_ , eol_))
        if self.Reference2 is not None:
            namespaceprefix_ = self.Reference2_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference2>%s</%sReference2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference2), input_name='Reference2')), namespaceprefix_ , eol_))
        if self.Vehicle is not None:
            namespaceprefix_ = self.Vehicle_nsprefix_ + ':' if (UseCapturedNS_ and self.Vehicle_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sVehicle>%s</%sVehicle>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Vehicle), input_name='Vehicle')), namespaceprefix_ , eol_))
        if self.Shipments is not None:
            namespaceprefix_ = self.Shipments_nsprefix_ + ':' if (UseCapturedNS_ and self.Shipments_nsprefix_) else ''
            self.Shipments.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Shipments', pretty_print=pretty_print)
        if self.PickupItems is not None:
            namespaceprefix_ = self.PickupItems_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupItems_nsprefix_) else ''
            self.PickupItems.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PickupItems', pretty_print=pretty_print)
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStatus>%s</%sStatus>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Status), input_name='Status')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'PickupAddress':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PickupAddress = obj_
            obj_.original_tagname_ = 'PickupAddress'
        elif nodeName_ == 'PickupContact':
            obj_ = Contact.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PickupContact = obj_
            obj_.original_tagname_ = 'PickupContact'
        elif nodeName_ == 'PickupLocation':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupLocation')
            value_ = self.gds_validate_string(value_, node, 'PickupLocation')
            self.PickupLocation = value_
            self.PickupLocation_nsprefix_ = child_.prefix
        elif nodeName_ == 'PickupDate':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.PickupDate = dval_
            self.PickupDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'ReadyTime':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.ReadyTime = dval_
            self.ReadyTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'LastPickupTime':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.LastPickupTime = dval_
            self.LastPickupTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'ClosingTime':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.ClosingTime = dval_
            self.ClosingTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'Comments':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Comments')
            value_ = self.gds_validate_string(value_, node, 'Comments')
            self.Comments = value_
            self.Comments_nsprefix_ = child_.prefix
        elif nodeName_ == 'Reference1':
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
        elif nodeName_ == 'Vehicle':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Vehicle')
            value_ = self.gds_validate_string(value_, node, 'Vehicle')
            self.Vehicle = value_
            self.Vehicle_nsprefix_ = child_.prefix
        elif nodeName_ == 'Shipments':
            obj_ = ArrayOfShipment.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Shipments = obj_
            obj_.original_tagname_ = 'Shipments'
        elif nodeName_ == 'PickupItems':
            obj_ = ArrayOfPickupItemDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PickupItems = obj_
            obj_.original_tagname_ = 'PickupItems'
        elif nodeName_ == 'Status':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Status')
            value_ = self.gds_validate_string(value_, node, 'Status')
            self.Status = value_
            self.Status_nsprefix_ = child_.prefix
# end class Pickup


class ArrayOfPickupItemDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PickupItemDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if PickupItemDetail is None:
            self.PickupItemDetail = []
        else:
            self.PickupItemDetail = PickupItemDetail
        self.PickupItemDetail_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfPickupItemDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfPickupItemDetail.subclass:
            return ArrayOfPickupItemDetail.subclass(*args_, **kwargs_)
        else:
            return ArrayOfPickupItemDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PickupItemDetail(self):
        return self.PickupItemDetail
    def set_PickupItemDetail(self, PickupItemDetail):
        self.PickupItemDetail = PickupItemDetail
    def add_PickupItemDetail(self, value):
        self.PickupItemDetail.append(value)
    def insert_PickupItemDetail_at(self, index, value):
        self.PickupItemDetail.insert(index, value)
    def replace_PickupItemDetail_at(self, index, value):
        self.PickupItemDetail[index] = value
    def hasContent_(self):
        if (
            self.PickupItemDetail
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfPickupItemDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfPickupItemDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfPickupItemDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfPickupItemDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfPickupItemDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfPickupItemDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfPickupItemDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for PickupItemDetail_ in self.PickupItemDetail:
            namespaceprefix_ = self.PickupItemDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupItemDetail_nsprefix_) else ''
            PickupItemDetail_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PickupItemDetail', pretty_print=pretty_print)
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
        if nodeName_ == 'PickupItemDetail':
            obj_ = PickupItemDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PickupItemDetail.append(obj_)
            obj_.original_tagname_ = 'PickupItemDetail'
# end class ArrayOfPickupItemDetail


class PickupItemDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ProductGroup=None, ProductType=None, NumberOfShipments=None, PackageType=None, Payment=None, ShipmentWeight=None, ShipmentVolume=None, NumberOfPieces=None, CashAmount=None, ExtraCharges=None, ShipmentDimensions=None, Comments=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ProductGroup = ProductGroup
        self.ProductGroup_nsprefix_ = None
        self.ProductType = ProductType
        self.ProductType_nsprefix_ = None
        self.NumberOfShipments = NumberOfShipments
        self.NumberOfShipments_nsprefix_ = None
        self.PackageType = PackageType
        self.PackageType_nsprefix_ = None
        self.Payment = Payment
        self.Payment_nsprefix_ = None
        self.ShipmentWeight = ShipmentWeight
        self.ShipmentWeight_nsprefix_ = None
        self.ShipmentVolume = ShipmentVolume
        self.ShipmentVolume_nsprefix_ = None
        self.NumberOfPieces = NumberOfPieces
        self.NumberOfPieces_nsprefix_ = None
        self.CashAmount = CashAmount
        self.CashAmount_nsprefix_ = None
        self.ExtraCharges = ExtraCharges
        self.ExtraCharges_nsprefix_ = None
        self.ShipmentDimensions = ShipmentDimensions
        self.ShipmentDimensions_nsprefix_ = None
        self.Comments = Comments
        self.Comments_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PickupItemDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PickupItemDetail.subclass:
            return PickupItemDetail.subclass(*args_, **kwargs_)
        else:
            return PickupItemDetail(*args_, **kwargs_)
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
    def get_NumberOfShipments(self):
        return self.NumberOfShipments
    def set_NumberOfShipments(self, NumberOfShipments):
        self.NumberOfShipments = NumberOfShipments
    def get_PackageType(self):
        return self.PackageType
    def set_PackageType(self, PackageType):
        self.PackageType = PackageType
    def get_Payment(self):
        return self.Payment
    def set_Payment(self, Payment):
        self.Payment = Payment
    def get_ShipmentWeight(self):
        return self.ShipmentWeight
    def set_ShipmentWeight(self, ShipmentWeight):
        self.ShipmentWeight = ShipmentWeight
    def get_ShipmentVolume(self):
        return self.ShipmentVolume
    def set_ShipmentVolume(self, ShipmentVolume):
        self.ShipmentVolume = ShipmentVolume
    def get_NumberOfPieces(self):
        return self.NumberOfPieces
    def set_NumberOfPieces(self, NumberOfPieces):
        self.NumberOfPieces = NumberOfPieces
    def get_CashAmount(self):
        return self.CashAmount
    def set_CashAmount(self, CashAmount):
        self.CashAmount = CashAmount
    def get_ExtraCharges(self):
        return self.ExtraCharges
    def set_ExtraCharges(self, ExtraCharges):
        self.ExtraCharges = ExtraCharges
    def get_ShipmentDimensions(self):
        return self.ShipmentDimensions
    def set_ShipmentDimensions(self, ShipmentDimensions):
        self.ShipmentDimensions = ShipmentDimensions
    def get_Comments(self):
        return self.Comments
    def set_Comments(self, Comments):
        self.Comments = Comments
    def hasContent_(self):
        if (
            self.ProductGroup is not None or
            self.ProductType is not None or
            self.NumberOfShipments is not None or
            self.PackageType is not None or
            self.Payment is not None or
            self.ShipmentWeight is not None or
            self.ShipmentVolume is not None or
            self.NumberOfPieces is not None or
            self.CashAmount is not None or
            self.ExtraCharges is not None or
            self.ShipmentDimensions is not None or
            self.Comments is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupItemDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PickupItemDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PickupItemDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PickupItemDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PickupItemDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PickupItemDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupItemDetail', fromsubclass_=False, pretty_print=True):
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
        if self.NumberOfShipments is not None:
            namespaceprefix_ = self.NumberOfShipments_nsprefix_ + ':' if (UseCapturedNS_ and self.NumberOfShipments_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumberOfShipments>%s</%sNumberOfShipments>%s' % (namespaceprefix_ , self.gds_format_integer(self.NumberOfShipments, input_name='NumberOfShipments'), namespaceprefix_ , eol_))
        if self.PackageType is not None:
            namespaceprefix_ = self.PackageType_nsprefix_ + ':' if (UseCapturedNS_ and self.PackageType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPackageType>%s</%sPackageType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PackageType), input_name='PackageType')), namespaceprefix_ , eol_))
        if self.Payment is not None:
            namespaceprefix_ = self.Payment_nsprefix_ + ':' if (UseCapturedNS_ and self.Payment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPayment>%s</%sPayment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Payment), input_name='Payment')), namespaceprefix_ , eol_))
        if self.ShipmentWeight is not None:
            namespaceprefix_ = self.ShipmentWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentWeight_nsprefix_) else ''
            self.ShipmentWeight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentWeight', pretty_print=pretty_print)
        if self.ShipmentVolume is not None:
            namespaceprefix_ = self.ShipmentVolume_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentVolume_nsprefix_) else ''
            self.ShipmentVolume.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentVolume', pretty_print=pretty_print)
        if self.NumberOfPieces is not None:
            namespaceprefix_ = self.NumberOfPieces_nsprefix_ + ':' if (UseCapturedNS_ and self.NumberOfPieces_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumberOfPieces>%s</%sNumberOfPieces>%s' % (namespaceprefix_ , self.gds_format_integer(self.NumberOfPieces, input_name='NumberOfPieces'), namespaceprefix_ , eol_))
        if self.CashAmount is not None:
            namespaceprefix_ = self.CashAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.CashAmount_nsprefix_) else ''
            self.CashAmount.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CashAmount', pretty_print=pretty_print)
        if self.ExtraCharges is not None:
            namespaceprefix_ = self.ExtraCharges_nsprefix_ + ':' if (UseCapturedNS_ and self.ExtraCharges_nsprefix_) else ''
            self.ExtraCharges.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ExtraCharges', pretty_print=pretty_print)
        if self.ShipmentDimensions is not None:
            namespaceprefix_ = self.ShipmentDimensions_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentDimensions_nsprefix_) else ''
            self.ShipmentDimensions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentDimensions', pretty_print=pretty_print)
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
        elif nodeName_ == 'NumberOfShipments' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'NumberOfShipments')
            ival_ = self.gds_validate_integer(ival_, node, 'NumberOfShipments')
            self.NumberOfShipments = ival_
            self.NumberOfShipments_nsprefix_ = child_.prefix
        elif nodeName_ == 'PackageType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PackageType')
            value_ = self.gds_validate_string(value_, node, 'PackageType')
            self.PackageType = value_
            self.PackageType_nsprefix_ = child_.prefix
        elif nodeName_ == 'Payment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Payment')
            value_ = self.gds_validate_string(value_, node, 'Payment')
            self.Payment = value_
            self.Payment_nsprefix_ = child_.prefix
        elif nodeName_ == 'ShipmentWeight':
            obj_ = Weight.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentWeight = obj_
            obj_.original_tagname_ = 'ShipmentWeight'
        elif nodeName_ == 'ShipmentVolume':
            obj_ = Volume.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentVolume = obj_
            obj_.original_tagname_ = 'ShipmentVolume'
        elif nodeName_ == 'NumberOfPieces' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'NumberOfPieces')
            ival_ = self.gds_validate_integer(ival_, node, 'NumberOfPieces')
            self.NumberOfPieces = ival_
            self.NumberOfPieces_nsprefix_ = child_.prefix
        elif nodeName_ == 'CashAmount':
            obj_ = Money.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CashAmount = obj_
            obj_.original_tagname_ = 'CashAmount'
        elif nodeName_ == 'ExtraCharges':
            obj_ = Money.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ExtraCharges = obj_
            obj_.original_tagname_ = 'ExtraCharges'
        elif nodeName_ == 'ShipmentDimensions':
            obj_ = Dimensions.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentDimensions = obj_
            obj_.original_tagname_ = 'ShipmentDimensions'
        elif nodeName_ == 'Comments':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Comments')
            value_ = self.gds_validate_string(value_, node, 'Comments')
            self.Comments = value_
            self.Comments_nsprefix_ = child_.prefix
# end class PickupItemDetail


class Volume(GeneratedsSuper):
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
                CurrentSubclassModule_, Volume)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Volume.subclass:
            return Volume.subclass(*args_, **kwargs_)
        else:
            return Volume(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Volume', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Volume')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Volume':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Volume')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Volume', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Volume'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Volume', fromsubclass_=False, pretty_print=True):
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
# end class Volume


class PickupCreationResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Transaction=None, Notifications=None, HasErrors=None, ProcessedPickup=None, gds_collector_=None, **kwargs_):
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
        self.ProcessedPickup = ProcessedPickup
        self.ProcessedPickup_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PickupCreationResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PickupCreationResponse.subclass:
            return PickupCreationResponse.subclass(*args_, **kwargs_)
        else:
            return PickupCreationResponse(*args_, **kwargs_)
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
    def get_ProcessedPickup(self):
        return self.ProcessedPickup
    def set_ProcessedPickup(self, ProcessedPickup):
        self.ProcessedPickup = ProcessedPickup
    def hasContent_(self):
        if (
            self.Transaction is not None or
            self.Notifications is not None or
            self.HasErrors is not None or
            self.ProcessedPickup is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupCreationResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PickupCreationResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PickupCreationResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PickupCreationResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PickupCreationResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PickupCreationResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupCreationResponse', fromsubclass_=False, pretty_print=True):
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
        if self.ProcessedPickup is not None:
            namespaceprefix_ = self.ProcessedPickup_nsprefix_ + ':' if (UseCapturedNS_ and self.ProcessedPickup_nsprefix_) else ''
            self.ProcessedPickup.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ProcessedPickup', pretty_print=pretty_print)
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
        elif nodeName_ == 'ProcessedPickup':
            obj_ = ProcessedPickup.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ProcessedPickup = obj_
            obj_.original_tagname_ = 'ProcessedPickup'
# end class PickupCreationResponse


class ProcessedPickup(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ID=None, GUID=None, Reference1=None, Reference2=None, ProcessedShipments=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ID = ID
        self.ID_nsprefix_ = None
        self.GUID = GUID
        self.GUID_nsprefix_ = None
        self.Reference1 = Reference1
        self.Reference1_nsprefix_ = None
        self.Reference2 = Reference2
        self.Reference2_nsprefix_ = None
        self.ProcessedShipments = ProcessedShipments
        self.ProcessedShipments_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ProcessedPickup)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ProcessedPickup.subclass:
            return ProcessedPickup.subclass(*args_, **kwargs_)
        else:
            return ProcessedPickup(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ID(self):
        return self.ID
    def set_ID(self, ID):
        self.ID = ID
    def get_GUID(self):
        return self.GUID
    def set_GUID(self, GUID):
        self.GUID = GUID
    def get_Reference1(self):
        return self.Reference1
    def set_Reference1(self, Reference1):
        self.Reference1 = Reference1
    def get_Reference2(self):
        return self.Reference2
    def set_Reference2(self, Reference2):
        self.Reference2 = Reference2
    def get_ProcessedShipments(self):
        return self.ProcessedShipments
    def set_ProcessedShipments(self, ProcessedShipments):
        self.ProcessedShipments = ProcessedShipments
    def hasContent_(self):
        if (
            self.ID is not None or
            self.GUID is not None or
            self.Reference1 is not None or
            self.Reference2 is not None or
            self.ProcessedShipments is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ProcessedPickup', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ProcessedPickup')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ProcessedPickup':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ProcessedPickup')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ProcessedPickup', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ProcessedPickup'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ProcessedPickup', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ID is not None:
            namespaceprefix_ = self.ID_nsprefix_ + ':' if (UseCapturedNS_ and self.ID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sID>%s</%sID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ID), input_name='ID')), namespaceprefix_ , eol_))
        if self.GUID is not None:
            namespaceprefix_ = self.GUID_nsprefix_ + ':' if (UseCapturedNS_ and self.GUID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGUID>%s</%sGUID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GUID), input_name='GUID')), namespaceprefix_ , eol_))
        if self.Reference1 is not None:
            namespaceprefix_ = self.Reference1_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference1>%s</%sReference1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference1), input_name='Reference1')), namespaceprefix_ , eol_))
        if self.Reference2 is not None:
            namespaceprefix_ = self.Reference2_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference2>%s</%sReference2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference2), input_name='Reference2')), namespaceprefix_ , eol_))
        if self.ProcessedShipments is not None:
            namespaceprefix_ = self.ProcessedShipments_nsprefix_ + ':' if (UseCapturedNS_ and self.ProcessedShipments_nsprefix_) else ''
            self.ProcessedShipments.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ProcessedShipments', pretty_print=pretty_print)
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
        if nodeName_ == 'ID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ID')
            value_ = self.gds_validate_string(value_, node, 'ID')
            self.ID = value_
            self.ID_nsprefix_ = child_.prefix
        elif nodeName_ == 'GUID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GUID')
            value_ = self.gds_validate_string(value_, node, 'GUID')
            self.GUID = value_
            self.GUID_nsprefix_ = child_.prefix
        elif nodeName_ == 'Reference1':
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
        elif nodeName_ == 'ProcessedShipments':
            obj_ = ArrayOfProcessedShipment.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ProcessedShipments = obj_
            obj_.original_tagname_ = 'ProcessedShipments'
# end class ProcessedPickup


class PickupCancelationRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ClientInfo=None, Transaction=None, PickupGUID=None, Comments=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ClientInfo = ClientInfo
        self.ClientInfo_nsprefix_ = None
        self.Transaction = Transaction
        self.Transaction_nsprefix_ = None
        self.PickupGUID = PickupGUID
        self.PickupGUID_nsprefix_ = None
        self.Comments = Comments
        self.Comments_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PickupCancelationRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PickupCancelationRequest.subclass:
            return PickupCancelationRequest.subclass(*args_, **kwargs_)
        else:
            return PickupCancelationRequest(*args_, **kwargs_)
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
    def get_PickupGUID(self):
        return self.PickupGUID
    def set_PickupGUID(self, PickupGUID):
        self.PickupGUID = PickupGUID
    def get_Comments(self):
        return self.Comments
    def set_Comments(self, Comments):
        self.Comments = Comments
    def hasContent_(self):
        if (
            self.ClientInfo is not None or
            self.Transaction is not None or
            self.PickupGUID is not None or
            self.Comments is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupCancelationRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PickupCancelationRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PickupCancelationRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PickupCancelationRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PickupCancelationRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PickupCancelationRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupCancelationRequest', fromsubclass_=False, pretty_print=True):
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
        if self.PickupGUID is not None:
            namespaceprefix_ = self.PickupGUID_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupGUID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupGUID>%s</%sPickupGUID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupGUID), input_name='PickupGUID')), namespaceprefix_ , eol_))
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
        elif nodeName_ == 'PickupGUID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupGUID')
            value_ = self.gds_validate_string(value_, node, 'PickupGUID')
            self.PickupGUID = value_
            self.PickupGUID_nsprefix_ = child_.prefix
        elif nodeName_ == 'Comments':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Comments')
            value_ = self.gds_validate_string(value_, node, 'Comments')
            self.Comments = value_
            self.Comments_nsprefix_ = child_.prefix
# end class PickupCancelationRequest


class PickupCancelationResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Transaction=None, Notifications=None, HasErrors=None, gds_collector_=None, **kwargs_):
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
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PickupCancelationResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PickupCancelationResponse.subclass:
            return PickupCancelationResponse.subclass(*args_, **kwargs_)
        else:
            return PickupCancelationResponse(*args_, **kwargs_)
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
    def hasContent_(self):
        if (
            self.Transaction is not None or
            self.Notifications is not None or
            self.HasErrors is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupCancelationResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PickupCancelationResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PickupCancelationResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PickupCancelationResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PickupCancelationResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PickupCancelationResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupCancelationResponse', fromsubclass_=False, pretty_print=True):
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
# end class PickupCancelationResponse


GDSClassesMapping = {
    'Address': Address,
    'ArrayOfAttachment': ArrayOfAttachment,
    'ArrayOfNotification': ArrayOfNotification,
    'ArrayOfPickupItemDetail': ArrayOfPickupItemDetail,
    'ArrayOfProcessedShipment': ArrayOfProcessedShipment,
    'ArrayOfShipment': ArrayOfShipment,
    'ArrayOfShipmentItem': ArrayOfShipmentItem,
    'Attachment': Attachment,
    'ClientInfo': ClientInfo,
    'Contact': Contact,
    'Dimensions': Dimensions,
    'LabelInfo': LabelInfo,
    'Money': Money,
    'Notification': Notification,
    'Party': Party,
    'Pickup': Pickup,
    'PickupItemDetail': PickupItemDetail,
    'ProcessedPickup': ProcessedPickup,
    'ProcessedShipment': ProcessedShipment,
    'Shipment': Shipment,
    'ShipmentDetails': ShipmentDetails,
    'ShipmentItem': ShipmentItem,
    'ShipmentLabel': ShipmentLabel,
    'Transaction': Transaction,
    'Volume': Volume,
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
        rootTag = 'ShipmentCreationRequest'
        rootClass = ShipmentCreationRequest
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
        rootTag = 'ShipmentCreationRequest'
        rootClass = ShipmentCreationRequest
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
        rootTag = 'ShipmentCreationRequest'
        rootClass = ShipmentCreationRequest
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='')
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
        rootTag = 'ShipmentCreationRequest'
        rootClass = ShipmentCreationRequest
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from shipping import *\n\n')
        sys.stdout.write('import shipping as model_\n\n')
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
NamespaceToDefMappings_ = {'http://ws.aramex.net/ShippingAPI/v1/': [('ClientInfo',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('Transaction',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('ArrayOfShipment',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('Shipment',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('Party',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('Address',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('Contact',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('ShipmentDetails',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('Dimensions',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('Weight',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('Money',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('ArrayOfShipmentItem',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('ShipmentItem',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('ArrayOfAttachment',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('Attachment',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('LabelInfo',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('ArrayOfNotification',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('Notification',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('ArrayOfProcessedShipment',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('ProcessedShipment',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('ShipmentLabel',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('Pickup',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('ArrayOfPickupItemDetail',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('PickupItemDetail',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('Volume',
                                           './schemas/shipping.xsd',
                                           'CT'),
                                          ('ProcessedPickup',
                                           './schemas/shipping.xsd',
                                           'CT')]}

__all__ = [
    "Address",
    "ArrayOfAttachment",
    "ArrayOfNotification",
    "ArrayOfPickupItemDetail",
    "ArrayOfProcessedShipment",
    "ArrayOfShipment",
    "ArrayOfShipmentItem",
    "Attachment",
    "ClientInfo",
    "Contact",
    "Dimensions",
    "LabelInfo",
    "LabelPrintingRequest",
    "LabelPrintingResponse",
    "Money",
    "Notification",
    "Party",
    "Pickup",
    "PickupCancelationRequest",
    "PickupCancelationResponse",
    "PickupCreationRequest",
    "PickupCreationResponse",
    "PickupItemDetail",
    "ProcessedPickup",
    "ProcessedShipment",
    "Shipment",
    "ShipmentCreationRequest",
    "ShipmentCreationResponse",
    "ShipmentDetails",
    "ShipmentItem",
    "ShipmentLabel",
    "Transaction",
    "Volume",
    "Weight"
]
