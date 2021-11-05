#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Wed Feb 24 19:49:29 2021 by generateDS.py version 2.37.16.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './tnt_lib/track_response_v3_1.py')
#
# Command line arguments:
#   ./schemas/track_response_v3_1.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./tnt_lib/track_response_v3_1.py" ./schemas/track_response_v3_1.xsd
#
# Current working directory (os.getcwd()):
#   tnt
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


class SummaryCodeType(str, Enum):
    """Has an enumerated value set, EXC represents Exception, INT respresents
    In Transit, DEL represents Delivered and CNF represents Consignment Not
    Found"""
    EXC='EXC'
    INT='INT'
    DEL='DEL'
    CNF='CNF'


class TermsOfPaymentType(str, Enum):
    """Enumerated values of Sender and Receiver"""
    SENDER='Sender'
    RECEIVER='Receiver'


class accessType(str, Enum):
    PUBLIC='public'
    FULL='full'


class addressPartyType(str, Enum):
    SENDER='Sender'
    RECEIVER='Receiver'
    COLLECTION='Collection'
    DELIVERY='Delivery'


class unitsType(str, Enum):
    KGS='kgs'
    LBS='lbs'


class TrackResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Consignment=None, ContinuationKey=None, Error=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Consignment is None:
            self.Consignment = []
        else:
            self.Consignment = Consignment
        self.Consignment_nsprefix_ = None
        self.ContinuationKey = ContinuationKey
        self.ContinuationKey_nsprefix_ = None
        self.Error = Error
        self.Error_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TrackResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TrackResponse.subclass:
            return TrackResponse.subclass(*args_, **kwargs_)
        else:
            return TrackResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Consignment(self):
        return self.Consignment
    def set_Consignment(self, Consignment):
        self.Consignment = Consignment
    def add_Consignment(self, value):
        self.Consignment.append(value)
    def insert_Consignment_at(self, index, value):
        self.Consignment.insert(index, value)
    def replace_Consignment_at(self, index, value):
        self.Consignment[index] = value
    def get_ContinuationKey(self):
        return self.ContinuationKey
    def set_ContinuationKey(self, ContinuationKey):
        self.ContinuationKey = ContinuationKey
    def get_Error(self):
        return self.Error
    def set_Error(self, Error):
        self.Error = Error
    def hasContent_(self):
        if (
            self.Consignment or
            self.ContinuationKey is not None or
            self.Error is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TrackResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TrackResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TrackResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TrackResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TrackResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Consignment_ in self.Consignment:
            namespaceprefix_ = self.Consignment_nsprefix_ + ':' if (UseCapturedNS_ and self.Consignment_nsprefix_) else ''
            Consignment_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Consignment', pretty_print=pretty_print)
        if self.ContinuationKey is not None:
            namespaceprefix_ = self.ContinuationKey_nsprefix_ + ':' if (UseCapturedNS_ and self.ContinuationKey_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sContinuationKey>%s</%sContinuationKey>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ContinuationKey), input_name='ContinuationKey')), namespaceprefix_ , eol_))
        if self.Error is not None:
            namespaceprefix_ = self.Error_nsprefix_ + ':' if (UseCapturedNS_ and self.Error_nsprefix_) else ''
            self.Error.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Error', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Consignment':
            obj_ = ConsignmentType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Consignment.append(obj_)
            obj_.original_tagname_ = 'Consignment'
        elif nodeName_ == 'ContinuationKey':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ContinuationKey')
            value_ = self.gds_validate_string(value_, node, 'ContinuationKey')
            self.ContinuationKey = value_
            self.ContinuationKey_nsprefix_ = child_.prefix
        elif nodeName_ == 'Error':
            obj_ = ErrorStructure.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Error = obj_
            obj_.original_tagname_ = 'Error'
# end class TrackResponse


class AccountStructure(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Number=None, CountryCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Number = Number
        self.validate_NumberType(self.Number)
        self.Number_nsprefix_ = None
        self.CountryCode = CountryCode
        self.validate_CountryCodeType(self.CountryCode)
        self.CountryCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AccountStructure)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AccountStructure.subclass:
            return AccountStructure.subclass(*args_, **kwargs_)
        else:
            return AccountStructure(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Number(self):
        return self.Number
    def set_Number(self, Number):
        self.Number = Number
    def get_CountryCode(self):
        return self.CountryCode
    def set_CountryCode(self, CountryCode):
        self.CountryCode = CountryCode
    def validate_NumberType(self, value):
        result = True
        # Validate type NumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_NumberType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_NumberType_patterns_, ))
                result = False
        return result
    validate_NumberType_patterns_ = [['^([A-Za-z0-9]+)$']]
    def validate_CountryCodeType(self, value):
        result = True
        # Validate type CountryCodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_CountryCodeType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_CountryCodeType_patterns_, ))
                result = False
        return result
    validate_CountryCodeType_patterns_ = [['^([A-Z][A-Z][A-Z0-9]?)$']]
    def hasContent_(self):
        if (
            self.Number is not None or
            self.CountryCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AccountStructure', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AccountStructure')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AccountStructure':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AccountStructure')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AccountStructure', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AccountStructure'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AccountStructure', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Number is not None:
            namespaceprefix_ = self.Number_nsprefix_ + ':' if (UseCapturedNS_ and self.Number_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumber>%s</%sNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Number), input_name='Number')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Number':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Number')
            value_ = self.gds_validate_string(value_, node, 'Number')
            self.Number = value_
            self.Number_nsprefix_ = child_.prefix
            # validate type NumberType
            self.validate_NumberType(self.Number)
        elif nodeName_ == 'CountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryCode')
            value_ = self.gds_validate_string(value_, node, 'CountryCode')
            self.CountryCode = value_
            self.CountryCode_nsprefix_ = child_.prefix
            # validate type CountryCodeType
            self.validate_CountryCodeType(self.CountryCode)
# end class AccountStructure


class DateType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, format='YYYYMMDD', valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.format = _cast(None, format)
        self.format_nsprefix_ = None
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DateType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DateType.subclass:
            return DateType.subclass(*args_, **kwargs_)
        else:
            return DateType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_format(self):
        return self.format
    def set_format(self, format):
        self.format = format
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def validate_NonZeroLengthString(self, value):
        result = True
        # Validate type NonZeroLengthString, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on NonZeroLengthString' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_)
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DateType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DateType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DateType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DateType')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DateType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DateType'):
        if self.format != "YYYYMMDD" and 'format' not in already_processed:
            already_processed.add('format')
            outfile.write(' format=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.format), input_name='format')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DateType', fromsubclass_=False, pretty_print=True):
        pass
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('format', node)
        if value is not None and 'format' not in already_processed:
            already_processed.add('format')
            self.format = value
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class DateType


class TimeType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, format='HHMM', valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.format = _cast(None, format)
        self.format_nsprefix_ = None
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TimeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TimeType.subclass:
            return TimeType.subclass(*args_, **kwargs_)
        else:
            return TimeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_format(self):
        return self.format
    def set_format(self, format):
        self.format = format
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def validate_NonZeroLengthString(self, value):
        result = True
        # Validate type NonZeroLengthString, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on NonZeroLengthString' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_)
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TimeType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TimeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TimeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TimeType')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TimeType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TimeType'):
        if self.format != "HHMM" and 'format' not in already_processed:
            already_processed.add('format')
            outfile.write(' format=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.format), input_name='format')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TimeType', fromsubclass_=False, pretty_print=True):
        pass
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('format', node)
        if value is not None and 'format' not in already_processed:
            already_processed.add('format')
            self.format = value
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class TimeType


class StatusStructure(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, StatusCode=None, StatusDescription=None, LocalEventDate=None, LocalEventTime=None, Depot=None, DepotName=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.StatusCode = StatusCode
        self.StatusCode_nsprefix_ = None
        self.StatusDescription = StatusDescription
        self.StatusDescription_nsprefix_ = None
        self.LocalEventDate = LocalEventDate
        self.LocalEventDate_nsprefix_ = None
        self.LocalEventTime = LocalEventTime
        self.LocalEventTime_nsprefix_ = None
        self.Depot = Depot
        self.Depot_nsprefix_ = None
        self.DepotName = DepotName
        self.DepotName_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, StatusStructure)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if StatusStructure.subclass:
            return StatusStructure.subclass(*args_, **kwargs_)
        else:
            return StatusStructure(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_StatusCode(self):
        return self.StatusCode
    def set_StatusCode(self, StatusCode):
        self.StatusCode = StatusCode
    def get_StatusDescription(self):
        return self.StatusDescription
    def set_StatusDescription(self, StatusDescription):
        self.StatusDescription = StatusDescription
    def get_LocalEventDate(self):
        return self.LocalEventDate
    def set_LocalEventDate(self, LocalEventDate):
        self.LocalEventDate = LocalEventDate
    def get_LocalEventTime(self):
        return self.LocalEventTime
    def set_LocalEventTime(self, LocalEventTime):
        self.LocalEventTime = LocalEventTime
    def get_Depot(self):
        return self.Depot
    def set_Depot(self, Depot):
        self.Depot = Depot
    def get_DepotName(self):
        return self.DepotName
    def set_DepotName(self, DepotName):
        self.DepotName = DepotName
    def hasContent_(self):
        if (
            self.StatusCode is not None or
            self.StatusDescription is not None or
            self.LocalEventDate is not None or
            self.LocalEventTime is not None or
            self.Depot is not None or
            self.DepotName is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='StatusStructure', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('StatusStructure')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'StatusStructure':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='StatusStructure')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='StatusStructure', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='StatusStructure'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='StatusStructure', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.StatusCode is not None:
            namespaceprefix_ = self.StatusCode_nsprefix_ + ':' if (UseCapturedNS_ and self.StatusCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStatusCode>%s</%sStatusCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.StatusCode), input_name='StatusCode')), namespaceprefix_ , eol_))
        if self.StatusDescription is not None:
            namespaceprefix_ = self.StatusDescription_nsprefix_ + ':' if (UseCapturedNS_ and self.StatusDescription_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStatusDescription>%s</%sStatusDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.StatusDescription), input_name='StatusDescription')), namespaceprefix_ , eol_))
        if self.LocalEventDate is not None:
            namespaceprefix_ = self.LocalEventDate_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalEventDate_nsprefix_) else ''
            self.LocalEventDate.export(outfile, level, namespaceprefix_, namespacedef_='', name_='LocalEventDate', pretty_print=pretty_print)
        if self.LocalEventTime is not None:
            namespaceprefix_ = self.LocalEventTime_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalEventTime_nsprefix_) else ''
            self.LocalEventTime.export(outfile, level, namespaceprefix_, namespacedef_='', name_='LocalEventTime', pretty_print=pretty_print)
        if self.Depot is not None:
            namespaceprefix_ = self.Depot_nsprefix_ + ':' if (UseCapturedNS_ and self.Depot_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDepot>%s</%sDepot>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Depot), input_name='Depot')), namespaceprefix_ , eol_))
        if self.DepotName is not None:
            namespaceprefix_ = self.DepotName_nsprefix_ + ':' if (UseCapturedNS_ and self.DepotName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDepotName>%s</%sDepotName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DepotName), input_name='DepotName')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'StatusCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'StatusCode')
            value_ = self.gds_validate_string(value_, node, 'StatusCode')
            self.StatusCode = value_
            self.StatusCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'StatusDescription':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'StatusDescription')
            value_ = self.gds_validate_string(value_, node, 'StatusDescription')
            self.StatusDescription = value_
            self.StatusDescription_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocalEventDate':
            obj_ = DateType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LocalEventDate = obj_
            obj_.original_tagname_ = 'LocalEventDate'
        elif nodeName_ == 'LocalEventTime':
            obj_ = TimeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LocalEventTime = obj_
            obj_.original_tagname_ = 'LocalEventTime'
        elif nodeName_ == 'Depot':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Depot')
            value_ = self.gds_validate_string(value_, node, 'Depot')
            self.Depot = value_
            self.Depot_nsprefix_ = child_.prefix
        elif nodeName_ == 'DepotName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DepotName')
            value_ = self.gds_validate_string(value_, node, 'DepotName')
            self.DepotName = value_
            self.DepotName_nsprefix_ = child_.prefix
# end class StatusStructure


class PackageSummaryStructure(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, NumberOfPieces=None, Weight=None, PackageDescription=None, GoodsDescription=None, InvoiceAmount=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.NumberOfPieces = NumberOfPieces
        self.NumberOfPieces_nsprefix_ = None
        self.Weight = Weight
        self.Weight_nsprefix_ = None
        self.PackageDescription = PackageDescription
        self.PackageDescription_nsprefix_ = None
        self.GoodsDescription = GoodsDescription
        self.GoodsDescription_nsprefix_ = None
        self.InvoiceAmount = InvoiceAmount
        self.InvoiceAmount_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PackageSummaryStructure)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PackageSummaryStructure.subclass:
            return PackageSummaryStructure.subclass(*args_, **kwargs_)
        else:
            return PackageSummaryStructure(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_NumberOfPieces(self):
        return self.NumberOfPieces
    def set_NumberOfPieces(self, NumberOfPieces):
        self.NumberOfPieces = NumberOfPieces
    def get_Weight(self):
        return self.Weight
    def set_Weight(self, Weight):
        self.Weight = Weight
    def get_PackageDescription(self):
        return self.PackageDescription
    def set_PackageDescription(self, PackageDescription):
        self.PackageDescription = PackageDescription
    def get_GoodsDescription(self):
        return self.GoodsDescription
    def set_GoodsDescription(self, GoodsDescription):
        self.GoodsDescription = GoodsDescription
    def get_InvoiceAmount(self):
        return self.InvoiceAmount
    def set_InvoiceAmount(self, InvoiceAmount):
        self.InvoiceAmount = InvoiceAmount
    def hasContent_(self):
        if (
            self.NumberOfPieces is not None or
            self.Weight is not None or
            self.PackageDescription is not None or
            self.GoodsDescription is not None or
            self.InvoiceAmount is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PackageSummaryStructure', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PackageSummaryStructure')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PackageSummaryStructure':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PackageSummaryStructure')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PackageSummaryStructure', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PackageSummaryStructure'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PackageSummaryStructure', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.NumberOfPieces is not None:
            namespaceprefix_ = self.NumberOfPieces_nsprefix_ + ':' if (UseCapturedNS_ and self.NumberOfPieces_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumberOfPieces>%s</%sNumberOfPieces>%s' % (namespaceprefix_ , self.gds_format_integer(self.NumberOfPieces, input_name='NumberOfPieces'), namespaceprefix_ , eol_))
        if self.Weight is not None:
            namespaceprefix_ = self.Weight_nsprefix_ + ':' if (UseCapturedNS_ and self.Weight_nsprefix_) else ''
            self.Weight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Weight', pretty_print=pretty_print)
        if self.PackageDescription is not None:
            namespaceprefix_ = self.PackageDescription_nsprefix_ + ':' if (UseCapturedNS_ and self.PackageDescription_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPackageDescription>%s</%sPackageDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PackageDescription), input_name='PackageDescription')), namespaceprefix_ , eol_))
        if self.GoodsDescription is not None:
            namespaceprefix_ = self.GoodsDescription_nsprefix_ + ':' if (UseCapturedNS_ and self.GoodsDescription_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGoodsDescription>%s</%sGoodsDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GoodsDescription), input_name='GoodsDescription')), namespaceprefix_ , eol_))
        if self.InvoiceAmount is not None:
            namespaceprefix_ = self.InvoiceAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.InvoiceAmount_nsprefix_) else ''
            self.InvoiceAmount.export(outfile, level, namespaceprefix_, namespacedef_='', name_='InvoiceAmount', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'NumberOfPieces' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'NumberOfPieces')
            ival_ = self.gds_validate_integer(ival_, node, 'NumberOfPieces')
            self.NumberOfPieces = ival_
            self.NumberOfPieces_nsprefix_ = child_.prefix
        elif nodeName_ == 'Weight':
            obj_ = WeightType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Weight = obj_
            obj_.original_tagname_ = 'Weight'
        elif nodeName_ == 'PackageDescription':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PackageDescription')
            value_ = self.gds_validate_string(value_, node, 'PackageDescription')
            self.PackageDescription = value_
            self.PackageDescription_nsprefix_ = child_.prefix
        elif nodeName_ == 'GoodsDescription':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GoodsDescription')
            value_ = self.gds_validate_string(value_, node, 'GoodsDescription')
            self.GoodsDescription = value_
            self.GoodsDescription_nsprefix_ = child_.prefix
        elif nodeName_ == 'InvoiceAmount':
            obj_ = InvoiceAmountType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.InvoiceAmount = obj_
            obj_.original_tagname_ = 'InvoiceAmount'
# end class PackageSummaryStructure


class ShipmentSummaryStructure(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TermsOfPayment=None, DueDate=None, Service=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.TermsOfPayment = TermsOfPayment
        self.validate_TermsOfPaymentType(self.TermsOfPayment)
        self.TermsOfPayment_nsprefix_ = None
        self.DueDate = DueDate
        self.DueDate_nsprefix_ = None
        self.Service = Service
        self.Service_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentSummaryStructure)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentSummaryStructure.subclass:
            return ShipmentSummaryStructure.subclass(*args_, **kwargs_)
        else:
            return ShipmentSummaryStructure(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_TermsOfPayment(self):
        return self.TermsOfPayment
    def set_TermsOfPayment(self, TermsOfPayment):
        self.TermsOfPayment = TermsOfPayment
    def get_DueDate(self):
        return self.DueDate
    def set_DueDate(self, DueDate):
        self.DueDate = DueDate
    def get_Service(self):
        return self.Service
    def set_Service(self, Service):
        self.Service = Service
    def validate_TermsOfPaymentType(self, value):
        result = True
        # Validate type TermsOfPaymentType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['Sender', 'Receiver']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on TermsOfPaymentType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.TermsOfPayment is not None or
            self.DueDate is not None or
            self.Service is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentSummaryStructure', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentSummaryStructure')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentSummaryStructure':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentSummaryStructure')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentSummaryStructure', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentSummaryStructure'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentSummaryStructure', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.TermsOfPayment is not None:
            namespaceprefix_ = self.TermsOfPayment_nsprefix_ + ':' if (UseCapturedNS_ and self.TermsOfPayment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTermsOfPayment>%s</%sTermsOfPayment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TermsOfPayment), input_name='TermsOfPayment')), namespaceprefix_ , eol_))
        if self.DueDate is not None:
            namespaceprefix_ = self.DueDate_nsprefix_ + ':' if (UseCapturedNS_ and self.DueDate_nsprefix_) else ''
            self.DueDate.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DueDate', pretty_print=pretty_print)
        if self.Service is not None:
            namespaceprefix_ = self.Service_nsprefix_ + ':' if (UseCapturedNS_ and self.Service_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sService>%s</%sService>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Service), input_name='Service')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'TermsOfPayment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TermsOfPayment')
            value_ = self.gds_validate_string(value_, node, 'TermsOfPayment')
            self.TermsOfPayment = value_
            self.TermsOfPayment_nsprefix_ = child_.prefix
            # validate type TermsOfPaymentType
            self.validate_TermsOfPaymentType(self.TermsOfPayment)
        elif nodeName_ == 'DueDate':
            obj_ = DateType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DueDate = obj_
            obj_.original_tagname_ = 'DueDate'
        elif nodeName_ == 'Service':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Service')
            value_ = self.gds_validate_string(value_, node, 'Service')
            self.Service = value_
            self.Service_nsprefix_ = child_.prefix
# end class ShipmentSummaryStructure


class AddressStructure(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, addressParty=None, Name=None, AddressLine=None, City=None, Province=None, Postcode=None, Country=None, PhoneNumber=None, ContactName=None, ContactPhoneNumber=None, AccountNumber=None, VATNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.addressParty = _cast(None, addressParty)
        self.addressParty_nsprefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = None
        if AddressLine is None:
            self.AddressLine = []
        else:
            self.AddressLine = AddressLine
        self.AddressLine_nsprefix_ = None
        self.City = City
        self.City_nsprefix_ = None
        self.Province = Province
        self.Province_nsprefix_ = None
        self.Postcode = Postcode
        self.Postcode_nsprefix_ = None
        self.Country = Country
        self.Country_nsprefix_ = None
        self.PhoneNumber = PhoneNumber
        self.PhoneNumber_nsprefix_ = None
        self.ContactName = ContactName
        self.ContactName_nsprefix_ = None
        self.ContactPhoneNumber = ContactPhoneNumber
        self.ContactPhoneNumber_nsprefix_ = None
        self.AccountNumber = AccountNumber
        self.AccountNumber_nsprefix_ = None
        self.VATNumber = VATNumber
        self.VATNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AddressStructure)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AddressStructure.subclass:
            return AddressStructure.subclass(*args_, **kwargs_)
        else:
            return AddressStructure(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def get_AddressLine(self):
        return self.AddressLine
    def set_AddressLine(self, AddressLine):
        self.AddressLine = AddressLine
    def add_AddressLine(self, value):
        self.AddressLine.append(value)
    def insert_AddressLine_at(self, index, value):
        self.AddressLine.insert(index, value)
    def replace_AddressLine_at(self, index, value):
        self.AddressLine[index] = value
    def get_City(self):
        return self.City
    def set_City(self, City):
        self.City = City
    def get_Province(self):
        return self.Province
    def set_Province(self, Province):
        self.Province = Province
    def get_Postcode(self):
        return self.Postcode
    def set_Postcode(self, Postcode):
        self.Postcode = Postcode
    def get_Country(self):
        return self.Country
    def set_Country(self, Country):
        self.Country = Country
    def get_PhoneNumber(self):
        return self.PhoneNumber
    def set_PhoneNumber(self, PhoneNumber):
        self.PhoneNumber = PhoneNumber
    def get_ContactName(self):
        return self.ContactName
    def set_ContactName(self, ContactName):
        self.ContactName = ContactName
    def get_ContactPhoneNumber(self):
        return self.ContactPhoneNumber
    def set_ContactPhoneNumber(self, ContactPhoneNumber):
        self.ContactPhoneNumber = ContactPhoneNumber
    def get_AccountNumber(self):
        return self.AccountNumber
    def set_AccountNumber(self, AccountNumber):
        self.AccountNumber = AccountNumber
    def get_VATNumber(self):
        return self.VATNumber
    def set_VATNumber(self, VATNumber):
        self.VATNumber = VATNumber
    def get_addressParty(self):
        return self.addressParty
    def set_addressParty(self, addressParty):
        self.addressParty = addressParty
    def validate_addressPartyType(self, value):
        # Validate type addressPartyType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['Sender', 'Receiver', 'Collection', 'Delivery']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on addressPartyType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
    def hasContent_(self):
        if (
            self.Name is not None or
            self.AddressLine or
            self.City is not None or
            self.Province is not None or
            self.Postcode is not None or
            self.Country is not None or
            self.PhoneNumber is not None or
            self.ContactName is not None or
            self.ContactPhoneNumber is not None or
            self.AccountNumber is not None or
            self.VATNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressStructure', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AddressStructure')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AddressStructure':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AddressStructure')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AddressStructure', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AddressStructure'):
        if self.addressParty is not None and 'addressParty' not in already_processed:
            already_processed.add('addressParty')
            outfile.write(' addressParty=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.addressParty), input_name='addressParty')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressStructure', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName>%s</%sName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name), input_name='Name')), namespaceprefix_ , eol_))
        for AddressLine_ in self.AddressLine:
            namespaceprefix_ = self.AddressLine_nsprefix_ + ':' if (UseCapturedNS_ and self.AddressLine_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAddressLine>%s</%sAddressLine>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(AddressLine_), input_name='AddressLine')), namespaceprefix_ , eol_))
        if self.City is not None:
            namespaceprefix_ = self.City_nsprefix_ + ':' if (UseCapturedNS_ and self.City_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCity>%s</%sCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.City), input_name='City')), namespaceprefix_ , eol_))
        if self.Province is not None:
            namespaceprefix_ = self.Province_nsprefix_ + ':' if (UseCapturedNS_ and self.Province_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProvince>%s</%sProvince>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Province), input_name='Province')), namespaceprefix_ , eol_))
        if self.Postcode is not None:
            namespaceprefix_ = self.Postcode_nsprefix_ + ':' if (UseCapturedNS_ and self.Postcode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPostcode>%s</%sPostcode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Postcode), input_name='Postcode')), namespaceprefix_ , eol_))
        if self.Country is not None:
            namespaceprefix_ = self.Country_nsprefix_ + ':' if (UseCapturedNS_ and self.Country_nsprefix_) else ''
            self.Country.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Country', pretty_print=pretty_print)
        if self.PhoneNumber is not None:
            namespaceprefix_ = self.PhoneNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.PhoneNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPhoneNumber>%s</%sPhoneNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PhoneNumber), input_name='PhoneNumber')), namespaceprefix_ , eol_))
        if self.ContactName is not None:
            namespaceprefix_ = self.ContactName_nsprefix_ + ':' if (UseCapturedNS_ and self.ContactName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sContactName>%s</%sContactName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ContactName), input_name='ContactName')), namespaceprefix_ , eol_))
        if self.ContactPhoneNumber is not None:
            namespaceprefix_ = self.ContactPhoneNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ContactPhoneNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sContactPhoneNumber>%s</%sContactPhoneNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ContactPhoneNumber), input_name='ContactPhoneNumber')), namespaceprefix_ , eol_))
        if self.AccountNumber is not None:
            namespaceprefix_ = self.AccountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.AccountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccountNumber>%s</%sAccountNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AccountNumber), input_name='AccountNumber')), namespaceprefix_ , eol_))
        if self.VATNumber is not None:
            namespaceprefix_ = self.VATNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.VATNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sVATNumber>%s</%sVATNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.VATNumber), input_name='VATNumber')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('addressParty', node)
        if value is not None and 'addressParty' not in already_processed:
            already_processed.add('addressParty')
            self.addressParty = value
            self.validate_addressPartyType(self.addressParty)    # validate type addressPartyType
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Name')
            value_ = self.gds_validate_string(value_, node, 'Name')
            self.Name = value_
            self.Name_nsprefix_ = child_.prefix
        elif nodeName_ == 'AddressLine':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AddressLine')
            value_ = self.gds_validate_string(value_, node, 'AddressLine')
            self.AddressLine.append(value_)
            self.AddressLine_nsprefix_ = child_.prefix
        elif nodeName_ == 'City':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'City')
            value_ = self.gds_validate_string(value_, node, 'City')
            self.City = value_
            self.City_nsprefix_ = child_.prefix
        elif nodeName_ == 'Province':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Province')
            value_ = self.gds_validate_string(value_, node, 'Province')
            self.Province = value_
            self.Province_nsprefix_ = child_.prefix
        elif nodeName_ == 'Postcode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Postcode')
            value_ = self.gds_validate_string(value_, node, 'Postcode')
            self.Postcode = value_
            self.Postcode_nsprefix_ = child_.prefix
        elif nodeName_ == 'Country':
            obj_ = CountryStructure.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Country = obj_
            obj_.original_tagname_ = 'Country'
        elif nodeName_ == 'PhoneNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PhoneNumber')
            value_ = self.gds_validate_string(value_, node, 'PhoneNumber')
            self.PhoneNumber = value_
            self.PhoneNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'ContactName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ContactName')
            value_ = self.gds_validate_string(value_, node, 'ContactName')
            self.ContactName = value_
            self.ContactName_nsprefix_ = child_.prefix
        elif nodeName_ == 'ContactPhoneNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ContactPhoneNumber')
            value_ = self.gds_validate_string(value_, node, 'ContactPhoneNumber')
            self.ContactPhoneNumber = value_
            self.ContactPhoneNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'AccountNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AccountNumber')
            value_ = self.gds_validate_string(value_, node, 'AccountNumber')
            self.AccountNumber = value_
            self.AccountNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'VATNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'VATNumber')
            value_ = self.gds_validate_string(value_, node, 'VATNumber')
            self.VATNumber = value_
            self.VATNumber_nsprefix_ = child_.prefix
# end class AddressStructure


class AccountNumber(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AccountNumber)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AccountNumber.subclass:
            return AccountNumber.subclass(*args_, **kwargs_)
        else:
            return AccountNumber(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def hasContent_(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AccountNumber', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AccountNumber')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AccountNumber':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AccountNumber')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AccountNumber', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AccountNumber'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AccountNumber', fromsubclass_=False, pretty_print=True):
        pass
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class AccountNumber


class CountryStructure(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CountryCode=None, CountryName=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CountryCode = CountryCode
        self.validate_CountryCodeType(self.CountryCode)
        self.CountryCode_nsprefix_ = None
        self.CountryName = CountryName
        self.CountryName_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CountryStructure)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CountryStructure.subclass:
            return CountryStructure.subclass(*args_, **kwargs_)
        else:
            return CountryStructure(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CountryCode(self):
        return self.CountryCode
    def set_CountryCode(self, CountryCode):
        self.CountryCode = CountryCode
    def get_CountryName(self):
        return self.CountryName
    def set_CountryName(self, CountryName):
        self.CountryName = CountryName
    def validate_CountryCodeType(self, value):
        result = True
        # Validate type CountryCodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_CountryCodeType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_CountryCodeType_patterns_, ))
                result = False
        return result
    validate_CountryCodeType_patterns_ = [['^([A-Z][A-Z][A-Z0-9]?)$']]
    def hasContent_(self):
        if (
            self.CountryCode is not None or
            self.CountryName is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CountryStructure', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CountryStructure')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CountryStructure':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CountryStructure')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CountryStructure', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CountryStructure'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CountryStructure', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CountryCode is not None:
            namespaceprefix_ = self.CountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryCode>%s</%sCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryCode), input_name='CountryCode')), namespaceprefix_ , eol_))
        if self.CountryName is not None:
            namespaceprefix_ = self.CountryName_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryName>%s</%sCountryName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryName), input_name='CountryName')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryCode')
            value_ = self.gds_validate_string(value_, node, 'CountryCode')
            self.CountryCode = value_
            self.CountryCode_nsprefix_ = child_.prefix
            # validate type CountryCodeType
            self.validate_CountryCodeType(self.CountryCode)
        elif nodeName_ == 'CountryName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryName')
            value_ = self.gds_validate_string(value_, node, 'CountryName')
            self.CountryName = value_
            self.CountryName_nsprefix_ = child_.prefix
# end class CountryStructure


class ErrorStructure(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Code=None, Message=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Code is None:
            self.Code = []
        else:
            self.Code = Code
        self.Code_nsprefix_ = None
        if Message is None:
            self.Message = []
        else:
            self.Message = Message
        self.Message_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ErrorStructure)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ErrorStructure.subclass:
            return ErrorStructure.subclass(*args_, **kwargs_)
        else:
            return ErrorStructure(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Code(self):
        return self.Code
    def set_Code(self, Code):
        self.Code = Code
    def add_Code(self, value):
        self.Code.append(value)
    def insert_Code_at(self, index, value):
        self.Code.insert(index, value)
    def replace_Code_at(self, index, value):
        self.Code[index] = value
    def get_Message(self):
        return self.Message
    def set_Message(self, Message):
        self.Message = Message
    def add_Message(self, value):
        self.Message.append(value)
    def insert_Message_at(self, index, value):
        self.Message.insert(index, value)
    def replace_Message_at(self, index, value):
        self.Message[index] = value
    def hasContent_(self):
        if (
            self.Code or
            self.Message
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ErrorStructure', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ErrorStructure')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ErrorStructure':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ErrorStructure')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ErrorStructure', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ErrorStructure'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ErrorStructure', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Code_ in self.Code:
            namespaceprefix_ = self.Code_nsprefix_ + ':' if (UseCapturedNS_ and self.Code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCode>%s</%sCode>%s' % (namespaceprefix_ , self.gds_format_integer(Code_, input_name='Code'), namespaceprefix_ , eol_))
        for Message_ in self.Message:
            namespaceprefix_ = self.Message_nsprefix_ + ':' if (UseCapturedNS_ and self.Message_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMessage>%s</%sMessage>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Message_), input_name='Message')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Code' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Code')
            ival_ = self.gds_validate_integer(ival_, node, 'Code')
            self.Code.append(ival_)
            self.Code_nsprefix_ = child_.prefix
        elif nodeName_ == 'Message':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Message')
            value_ = self.gds_validate_string(value_, node, 'Message')
            self.Message.append(value_)
            self.Message_nsprefix_ = child_.prefix
# end class ErrorStructure


class ConsignmentType(GeneratedsSuper):
    """A response to a request for summary details will only contain mandatory
    child elements of Consignment"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, access=None, ConsignmentNumber=None, AlternativeConsignmentNumber=None, OriginDepot=None, OriginDepotName=None, CustomerReference=None, CollectionDate=None, DeliveryTown=None, DeliveryDate=None, DeliveryTime=None, Signatory=None, SummaryCode=None, DestinationCountry=None, OriginCountry=None, TermsOfPaymentAccount=None, SenderAccount=None, PieceQuantity=None, StatusData=None, PackageSummary=None, ShipmentSummary=None, Addresses=None, POD=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.access = _cast(None, access)
        self.access_nsprefix_ = None
        self.ConsignmentNumber = ConsignmentNumber
        self.ConsignmentNumber_nsprefix_ = None
        self.AlternativeConsignmentNumber = AlternativeConsignmentNumber
        self.AlternativeConsignmentNumber_nsprefix_ = None
        self.OriginDepot = OriginDepot
        self.OriginDepot_nsprefix_ = None
        self.OriginDepotName = OriginDepotName
        self.OriginDepotName_nsprefix_ = None
        self.CustomerReference = CustomerReference
        self.CustomerReference_nsprefix_ = None
        self.CollectionDate = CollectionDate
        self.CollectionDate_nsprefix_ = None
        self.DeliveryTown = DeliveryTown
        self.DeliveryTown_nsprefix_ = None
        self.DeliveryDate = DeliveryDate
        self.DeliveryDate_nsprefix_ = None
        self.DeliveryTime = DeliveryTime
        self.DeliveryTime_nsprefix_ = None
        self.Signatory = Signatory
        self.Signatory_nsprefix_ = None
        self.SummaryCode = SummaryCode
        self.validate_SummaryCodeType(self.SummaryCode)
        self.SummaryCode_nsprefix_ = None
        self.DestinationCountry = DestinationCountry
        self.DestinationCountry_nsprefix_ = None
        self.OriginCountry = OriginCountry
        self.OriginCountry_nsprefix_ = None
        self.TermsOfPaymentAccount = TermsOfPaymentAccount
        self.TermsOfPaymentAccount_nsprefix_ = None
        self.SenderAccount = SenderAccount
        self.SenderAccount_nsprefix_ = None
        self.PieceQuantity = PieceQuantity
        self.PieceQuantity_nsprefix_ = None
        if StatusData is None:
            self.StatusData = []
        else:
            self.StatusData = StatusData
        self.StatusData_nsprefix_ = None
        self.PackageSummary = PackageSummary
        self.PackageSummary_nsprefix_ = None
        self.ShipmentSummary = ShipmentSummary
        self.ShipmentSummary_nsprefix_ = None
        self.Addresses = Addresses
        self.Addresses_nsprefix_ = None
        self.POD = POD
        self.POD_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ConsignmentType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ConsignmentType.subclass:
            return ConsignmentType.subclass(*args_, **kwargs_)
        else:
            return ConsignmentType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ConsignmentNumber(self):
        return self.ConsignmentNumber
    def set_ConsignmentNumber(self, ConsignmentNumber):
        self.ConsignmentNumber = ConsignmentNumber
    def get_AlternativeConsignmentNumber(self):
        return self.AlternativeConsignmentNumber
    def set_AlternativeConsignmentNumber(self, AlternativeConsignmentNumber):
        self.AlternativeConsignmentNumber = AlternativeConsignmentNumber
    def get_OriginDepot(self):
        return self.OriginDepot
    def set_OriginDepot(self, OriginDepot):
        self.OriginDepot = OriginDepot
    def get_OriginDepotName(self):
        return self.OriginDepotName
    def set_OriginDepotName(self, OriginDepotName):
        self.OriginDepotName = OriginDepotName
    def get_CustomerReference(self):
        return self.CustomerReference
    def set_CustomerReference(self, CustomerReference):
        self.CustomerReference = CustomerReference
    def get_CollectionDate(self):
        return self.CollectionDate
    def set_CollectionDate(self, CollectionDate):
        self.CollectionDate = CollectionDate
    def get_DeliveryTown(self):
        return self.DeliveryTown
    def set_DeliveryTown(self, DeliveryTown):
        self.DeliveryTown = DeliveryTown
    def get_DeliveryDate(self):
        return self.DeliveryDate
    def set_DeliveryDate(self, DeliveryDate):
        self.DeliveryDate = DeliveryDate
    def get_DeliveryTime(self):
        return self.DeliveryTime
    def set_DeliveryTime(self, DeliveryTime):
        self.DeliveryTime = DeliveryTime
    def get_Signatory(self):
        return self.Signatory
    def set_Signatory(self, Signatory):
        self.Signatory = Signatory
    def get_SummaryCode(self):
        return self.SummaryCode
    def set_SummaryCode(self, SummaryCode):
        self.SummaryCode = SummaryCode
    def get_DestinationCountry(self):
        return self.DestinationCountry
    def set_DestinationCountry(self, DestinationCountry):
        self.DestinationCountry = DestinationCountry
    def get_OriginCountry(self):
        return self.OriginCountry
    def set_OriginCountry(self, OriginCountry):
        self.OriginCountry = OriginCountry
    def get_TermsOfPaymentAccount(self):
        return self.TermsOfPaymentAccount
    def set_TermsOfPaymentAccount(self, TermsOfPaymentAccount):
        self.TermsOfPaymentAccount = TermsOfPaymentAccount
    def get_SenderAccount(self):
        return self.SenderAccount
    def set_SenderAccount(self, SenderAccount):
        self.SenderAccount = SenderAccount
    def get_PieceQuantity(self):
        return self.PieceQuantity
    def set_PieceQuantity(self, PieceQuantity):
        self.PieceQuantity = PieceQuantity
    def get_StatusData(self):
        return self.StatusData
    def set_StatusData(self, StatusData):
        self.StatusData = StatusData
    def add_StatusData(self, value):
        self.StatusData.append(value)
    def insert_StatusData_at(self, index, value):
        self.StatusData.insert(index, value)
    def replace_StatusData_at(self, index, value):
        self.StatusData[index] = value
    def get_PackageSummary(self):
        return self.PackageSummary
    def set_PackageSummary(self, PackageSummary):
        self.PackageSummary = PackageSummary
    def get_ShipmentSummary(self):
        return self.ShipmentSummary
    def set_ShipmentSummary(self, ShipmentSummary):
        self.ShipmentSummary = ShipmentSummary
    def get_Addresses(self):
        return self.Addresses
    def set_Addresses(self, Addresses):
        self.Addresses = Addresses
    def get_POD(self):
        return self.POD
    def set_POD(self, POD):
        self.POD = POD
    def get_access(self):
        return self.access
    def set_access(self, access):
        self.access = access
    def validate_SummaryCodeType(self, value):
        result = True
        # Validate type SummaryCodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['EXC', 'INT', 'DEL', 'CNF']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on SummaryCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_accessType(self, value):
        # Validate type accessType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['public', 'full']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on accessType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
    def hasContent_(self):
        if (
            self.ConsignmentNumber is not None or
            self.AlternativeConsignmentNumber is not None or
            self.OriginDepot is not None or
            self.OriginDepotName is not None or
            self.CustomerReference is not None or
            self.CollectionDate is not None or
            self.DeliveryTown is not None or
            self.DeliveryDate is not None or
            self.DeliveryTime is not None or
            self.Signatory is not None or
            self.SummaryCode is not None or
            self.DestinationCountry is not None or
            self.OriginCountry is not None or
            self.TermsOfPaymentAccount is not None or
            self.SenderAccount is not None or
            self.PieceQuantity is not None or
            self.StatusData or
            self.PackageSummary is not None or
            self.ShipmentSummary is not None or
            self.Addresses is not None or
            self.POD is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ConsignmentType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ConsignmentType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ConsignmentType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ConsignmentType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ConsignmentType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ConsignmentType'):
        if self.access is not None and 'access' not in already_processed:
            already_processed.add('access')
            outfile.write(' access=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.access), input_name='access')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ConsignmentType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ConsignmentNumber is not None:
            namespaceprefix_ = self.ConsignmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ConsignmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sConsignmentNumber>%s</%sConsignmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ConsignmentNumber), input_name='ConsignmentNumber')), namespaceprefix_ , eol_))
        if self.AlternativeConsignmentNumber is not None:
            namespaceprefix_ = self.AlternativeConsignmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.AlternativeConsignmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAlternativeConsignmentNumber>%s</%sAlternativeConsignmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AlternativeConsignmentNumber), input_name='AlternativeConsignmentNumber')), namespaceprefix_ , eol_))
        if self.OriginDepot is not None:
            namespaceprefix_ = self.OriginDepot_nsprefix_ + ':' if (UseCapturedNS_ and self.OriginDepot_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOriginDepot>%s</%sOriginDepot>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OriginDepot), input_name='OriginDepot')), namespaceprefix_ , eol_))
        if self.OriginDepotName is not None:
            namespaceprefix_ = self.OriginDepotName_nsprefix_ + ':' if (UseCapturedNS_ and self.OriginDepotName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOriginDepotName>%s</%sOriginDepotName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OriginDepotName), input_name='OriginDepotName')), namespaceprefix_ , eol_))
        if self.CustomerReference is not None:
            namespaceprefix_ = self.CustomerReference_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomerReference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustomerReference>%s</%sCustomerReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CustomerReference), input_name='CustomerReference')), namespaceprefix_ , eol_))
        if self.CollectionDate is not None:
            namespaceprefix_ = self.CollectionDate_nsprefix_ + ':' if (UseCapturedNS_ and self.CollectionDate_nsprefix_) else ''
            self.CollectionDate.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CollectionDate', pretty_print=pretty_print)
        if self.DeliveryTown is not None:
            namespaceprefix_ = self.DeliveryTown_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryTown_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeliveryTown>%s</%sDeliveryTown>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DeliveryTown), input_name='DeliveryTown')), namespaceprefix_ , eol_))
        if self.DeliveryDate is not None:
            namespaceprefix_ = self.DeliveryDate_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryDate_nsprefix_) else ''
            self.DeliveryDate.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DeliveryDate', pretty_print=pretty_print)
        if self.DeliveryTime is not None:
            namespaceprefix_ = self.DeliveryTime_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryTime_nsprefix_) else ''
            self.DeliveryTime.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DeliveryTime', pretty_print=pretty_print)
        if self.Signatory is not None:
            namespaceprefix_ = self.Signatory_nsprefix_ + ':' if (UseCapturedNS_ and self.Signatory_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSignatory>%s</%sSignatory>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Signatory), input_name='Signatory')), namespaceprefix_ , eol_))
        if self.SummaryCode is not None:
            namespaceprefix_ = self.SummaryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.SummaryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSummaryCode>%s</%sSummaryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SummaryCode), input_name='SummaryCode')), namespaceprefix_ , eol_))
        if self.DestinationCountry is not None:
            namespaceprefix_ = self.DestinationCountry_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationCountry_nsprefix_) else ''
            self.DestinationCountry.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DestinationCountry', pretty_print=pretty_print)
        if self.OriginCountry is not None:
            namespaceprefix_ = self.OriginCountry_nsprefix_ + ':' if (UseCapturedNS_ and self.OriginCountry_nsprefix_) else ''
            self.OriginCountry.export(outfile, level, namespaceprefix_, namespacedef_='', name_='OriginCountry', pretty_print=pretty_print)
        if self.TermsOfPaymentAccount is not None:
            namespaceprefix_ = self.TermsOfPaymentAccount_nsprefix_ + ':' if (UseCapturedNS_ and self.TermsOfPaymentAccount_nsprefix_) else ''
            self.TermsOfPaymentAccount.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TermsOfPaymentAccount', pretty_print=pretty_print)
        if self.SenderAccount is not None:
            namespaceprefix_ = self.SenderAccount_nsprefix_ + ':' if (UseCapturedNS_ and self.SenderAccount_nsprefix_) else ''
            self.SenderAccount.export(outfile, level, namespaceprefix_, namespacedef_='', name_='SenderAccount', pretty_print=pretty_print)
        if self.PieceQuantity is not None:
            namespaceprefix_ = self.PieceQuantity_nsprefix_ + ':' if (UseCapturedNS_ and self.PieceQuantity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPieceQuantity>%s</%sPieceQuantity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PieceQuantity), input_name='PieceQuantity')), namespaceprefix_ , eol_))
        for StatusData_ in self.StatusData:
            namespaceprefix_ = self.StatusData_nsprefix_ + ':' if (UseCapturedNS_ and self.StatusData_nsprefix_) else ''
            StatusData_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='StatusData', pretty_print=pretty_print)
        if self.PackageSummary is not None:
            namespaceprefix_ = self.PackageSummary_nsprefix_ + ':' if (UseCapturedNS_ and self.PackageSummary_nsprefix_) else ''
            self.PackageSummary.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PackageSummary', pretty_print=pretty_print)
        if self.ShipmentSummary is not None:
            namespaceprefix_ = self.ShipmentSummary_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentSummary_nsprefix_) else ''
            self.ShipmentSummary.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentSummary', pretty_print=pretty_print)
        if self.Addresses is not None:
            namespaceprefix_ = self.Addresses_nsprefix_ + ':' if (UseCapturedNS_ and self.Addresses_nsprefix_) else ''
            self.Addresses.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Addresses', pretty_print=pretty_print)
        if self.POD is not None:
            namespaceprefix_ = self.POD_nsprefix_ + ':' if (UseCapturedNS_ and self.POD_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPOD>%s</%sPOD>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.POD), input_name='POD')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('access', node)
        if value is not None and 'access' not in already_processed:
            already_processed.add('access')
            self.access = value
            self.validate_accessType(self.access)    # validate type accessType
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ConsignmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ConsignmentNumber')
            value_ = self.gds_validate_string(value_, node, 'ConsignmentNumber')
            self.ConsignmentNumber = value_
            self.ConsignmentNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'AlternativeConsignmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AlternativeConsignmentNumber')
            value_ = self.gds_validate_string(value_, node, 'AlternativeConsignmentNumber')
            self.AlternativeConsignmentNumber = value_
            self.AlternativeConsignmentNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'OriginDepot':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OriginDepot')
            value_ = self.gds_validate_string(value_, node, 'OriginDepot')
            self.OriginDepot = value_
            self.OriginDepot_nsprefix_ = child_.prefix
        elif nodeName_ == 'OriginDepotName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OriginDepotName')
            value_ = self.gds_validate_string(value_, node, 'OriginDepotName')
            self.OriginDepotName = value_
            self.OriginDepotName_nsprefix_ = child_.prefix
        elif nodeName_ == 'CustomerReference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CustomerReference')
            value_ = self.gds_validate_string(value_, node, 'CustomerReference')
            self.CustomerReference = value_
            self.CustomerReference_nsprefix_ = child_.prefix
        elif nodeName_ == 'CollectionDate':
            obj_ = DateType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CollectionDate = obj_
            obj_.original_tagname_ = 'CollectionDate'
        elif nodeName_ == 'DeliveryTown':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DeliveryTown')
            value_ = self.gds_validate_string(value_, node, 'DeliveryTown')
            self.DeliveryTown = value_
            self.DeliveryTown_nsprefix_ = child_.prefix
        elif nodeName_ == 'DeliveryDate':
            obj_ = DateType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DeliveryDate = obj_
            obj_.original_tagname_ = 'DeliveryDate'
        elif nodeName_ == 'DeliveryTime':
            obj_ = TimeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DeliveryTime = obj_
            obj_.original_tagname_ = 'DeliveryTime'
        elif nodeName_ == 'Signatory':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Signatory')
            value_ = self.gds_validate_string(value_, node, 'Signatory')
            self.Signatory = value_
            self.Signatory_nsprefix_ = child_.prefix
        elif nodeName_ == 'SummaryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SummaryCode')
            value_ = self.gds_validate_string(value_, node, 'SummaryCode')
            self.SummaryCode = value_
            self.SummaryCode_nsprefix_ = child_.prefix
            # validate type SummaryCodeType
            self.validate_SummaryCodeType(self.SummaryCode)
        elif nodeName_ == 'DestinationCountry':
            obj_ = CountryStructure.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DestinationCountry = obj_
            obj_.original_tagname_ = 'DestinationCountry'
        elif nodeName_ == 'OriginCountry':
            obj_ = CountryStructure.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.OriginCountry = obj_
            obj_.original_tagname_ = 'OriginCountry'
        elif nodeName_ == 'TermsOfPaymentAccount':
            obj_ = AccountStructure.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TermsOfPaymentAccount = obj_
            obj_.original_tagname_ = 'TermsOfPaymentAccount'
        elif nodeName_ == 'SenderAccount':
            obj_ = AccountStructure.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SenderAccount = obj_
            obj_.original_tagname_ = 'SenderAccount'
        elif nodeName_ == 'PieceQuantity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PieceQuantity')
            value_ = self.gds_validate_string(value_, node, 'PieceQuantity')
            self.PieceQuantity = value_
            self.PieceQuantity_nsprefix_ = child_.prefix
        elif nodeName_ == 'StatusData':
            obj_ = StatusStructure.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.StatusData.append(obj_)
            obj_.original_tagname_ = 'StatusData'
        elif nodeName_ == 'PackageSummary':
            obj_ = PackageSummaryStructure.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PackageSummary = obj_
            obj_.original_tagname_ = 'PackageSummary'
        elif nodeName_ == 'ShipmentSummary':
            obj_ = ShipmentSummaryStructure.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentSummary = obj_
            obj_.original_tagname_ = 'ShipmentSummary'
        elif nodeName_ == 'Addresses':
            obj_ = AddressesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Addresses = obj_
            obj_.original_tagname_ = 'Addresses'
        elif nodeName_ == 'POD':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'POD')
            value_ = self.gds_validate_string(value_, node, 'POD')
            self.POD = value_
            self.POD_nsprefix_ = child_.prefix
# end class ConsignmentType


class PieceQuantity(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PieceQuantity)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PieceQuantity.subclass:
            return PieceQuantity.subclass(*args_, **kwargs_)
        else:
            return PieceQuantity(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def hasContent_(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PieceQuantity', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PieceQuantity')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PieceQuantity':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PieceQuantity')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PieceQuantity', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PieceQuantity'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PieceQuantity', fromsubclass_=False, pretty_print=True):
        pass
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class PieceQuantity


class AddressesType(GeneratedsSuper):
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
                CurrentSubclassModule_, AddressesType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AddressesType.subclass:
            return AddressesType.subclass(*args_, **kwargs_)
        else:
            return AddressesType(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressesType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AddressesType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AddressesType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AddressesType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AddressesType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AddressesType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressesType', fromsubclass_=False, pretty_print=True):
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
            obj_ = AddressStructure.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address.append(obj_)
            obj_.original_tagname_ = 'Address'
# end class AddressesType


class WeightType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, units='kgs', valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.units = _cast(None, units)
        self.units_nsprefix_ = None
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, WeightType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if WeightType.subclass:
            return WeightType.subclass(*args_, **kwargs_)
        else:
            return WeightType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_units(self):
        return self.units
    def set_units(self, units):
        self.units = units
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def validate_unitsType(self, value):
        # Validate type unitsType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['kgs', 'lbs']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on unitsType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
    def hasContent_(self):
        if (
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_)
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WeightType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('WeightType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'WeightType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='WeightType')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='WeightType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='WeightType'):
        if self.units != "kgs" and 'units' not in already_processed:
            already_processed.add('units')
            outfile.write(' units=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.units), input_name='units')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WeightType', fromsubclass_=False, pretty_print=True):
        pass
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('units', node)
        if value is not None and 'units' not in already_processed:
            already_processed.add('units')
            self.units = value
            self.validate_unitsType(self.units)    # validate type unitsType
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class WeightType


class InvoiceAmountType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, currency=None, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.currency = _cast(None, currency)
        self.currency_nsprefix_ = None
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, InvoiceAmountType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if InvoiceAmountType.subclass:
            return InvoiceAmountType.subclass(*args_, **kwargs_)
        else:
            return InvoiceAmountType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_currency(self):
        return self.currency
    def set_currency(self, currency):
        self.currency = currency
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def hasContent_(self):
        if (
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_)
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='InvoiceAmountType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('InvoiceAmountType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'InvoiceAmountType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='InvoiceAmountType')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='InvoiceAmountType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='InvoiceAmountType'):
        if self.currency is not None and 'currency' not in already_processed:
            already_processed.add('currency')
            outfile.write(' currency=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.currency), input_name='currency')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='InvoiceAmountType', fromsubclass_=False, pretty_print=True):
        pass
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('currency', node)
        if value is not None and 'currency' not in already_processed:
            already_processed.add('currency')
            self.currency = value
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class InvoiceAmountType


GDSClassesMapping = {
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
        rootTag = 'TrackResponse'
        rootClass = TrackResponse
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
        rootTag = 'TrackResponse'
        rootClass = TrackResponse
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
        rootTag = 'TrackResponse'
        rootClass = TrackResponse
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
        rootTag = 'TrackResponse'
        rootClass = TrackResponse
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from track_response_v3_1 import *\n\n')
        sys.stdout.write('import track_response_v3_1 as model_\n\n')
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
NamespaceToDefMappings_ = {}

__all__ = [
    "AccountNumber",
    "AccountStructure",
    "AddressStructure",
    "AddressesType",
    "ConsignmentType",
    "CountryStructure",
    "DateType",
    "ErrorStructure",
    "InvoiceAmountType",
    "PackageSummaryStructure",
    "PieceQuantity",
    "ShipmentSummaryStructure",
    "StatusStructure",
    "TimeType",
    "TrackResponse",
    "WeightType"
]
