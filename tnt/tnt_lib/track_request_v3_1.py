#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Wed Feb 24 19:49:29 2021 by generateDS.py version 2.37.16.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './tnt_lib/track_request_v3_1.py')
#
# Command line arguments:
#   ./schemas/track_request_v3_1.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./tnt_lib/track_request_v3_1.py" ./schemas/track_request_v3_1.xsd
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


class MarketTypeType(str, Enum):
    DOMESTIC='Domestic'
    INTERNATIONAL='International'


class TrackRequest(GeneratedsSuper):
    """Specifies the request submitted to the Tracking Service"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, locale=None, version='3.0', SearchCriteria=None, LevelOfDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.locale = _cast(None, locale)
        self.locale_nsprefix_ = None
        self.version = _cast(float, version)
        self.version_nsprefix_ = None
        self.SearchCriteria = SearchCriteria
        self.SearchCriteria_nsprefix_ = None
        self.LevelOfDetail = LevelOfDetail
        self.LevelOfDetail_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TrackRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TrackRequest.subclass:
            return TrackRequest.subclass(*args_, **kwargs_)
        else:
            return TrackRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_SearchCriteria(self):
        return self.SearchCriteria
    def set_SearchCriteria(self, SearchCriteria):
        self.SearchCriteria = SearchCriteria
    def get_LevelOfDetail(self):
        return self.LevelOfDetail
    def set_LevelOfDetail(self, LevelOfDetail):
        self.LevelOfDetail = LevelOfDetail
    def get_locale(self):
        return self.locale
    def set_locale(self, locale):
        self.locale = locale
    def get_version(self):
        return self.version
    def set_version(self, version):
        self.version = version
    def validate_LocaleType(self, value):
        # Validate type LocaleType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_LocaleType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_LocaleType_patterns_, ))
    validate_LocaleType_patterns_ = [['^([a-z][a-z]_[A-Z][A-Z])$']]
    def validate_VersionType(self, value):
        # Validate type VersionType, a restriction on xs:float.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, float):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (float)' % {"value": value, "lineno": lineno, })
                return False
            pass
    def hasContent_(self):
        if (
            self.SearchCriteria is not None or
            self.LevelOfDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TrackRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TrackRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TrackRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TrackRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TrackRequest'):
        if self.locale is not None and 'locale' not in already_processed:
            already_processed.add('locale')
            outfile.write(' locale=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.locale), input_name='locale')), ))
        if self.version != 3.0 and 'version' not in already_processed:
            already_processed.add('version')
            outfile.write(' version="%s"' % self.gds_format_float(self.version, input_name='version'))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.SearchCriteria is not None:
            namespaceprefix_ = self.SearchCriteria_nsprefix_ + ':' if (UseCapturedNS_ and self.SearchCriteria_nsprefix_) else ''
            self.SearchCriteria.export(outfile, level, namespaceprefix_, namespacedef_='', name_='SearchCriteria', pretty_print=pretty_print)
        if self.LevelOfDetail is not None:
            namespaceprefix_ = self.LevelOfDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.LevelOfDetail_nsprefix_) else ''
            self.LevelOfDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='LevelOfDetail', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('locale', node)
        if value is not None and 'locale' not in already_processed:
            already_processed.add('locale')
            self.locale = value
            self.validate_LocaleType(self.locale)    # validate type LocaleType
        value = find_attr_value_('version', node)
        if value is not None and 'version' not in already_processed:
            already_processed.add('version')
            value = self.gds_parse_float(value, node, 'version')
            self.version = value
            self.validate_VersionType(self.version)    # validate type VersionType
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'SearchCriteria':
            obj_ = SearchCriteriaType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SearchCriteria = obj_
            obj_.original_tagname_ = 'SearchCriteria'
        elif nodeName_ == 'LevelOfDetail':
            obj_ = LevelOfDetailType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LevelOfDetail = obj_
            obj_.original_tagname_ = 'LevelOfDetail'
# end class TrackRequest


class NumberOfDays(GeneratedsSuper):
    """The number of days the search is to span including the DateFrom value as
    the first day"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, NumberOfDays)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if NumberOfDays.subclass:
            return NumberOfDays.subclass(*args_, **kwargs_)
        else:
            return NumberOfDays(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_NumberOfDays(self, value):
        result = True
        # Validate type NumberOfDays, a restriction on NonNegativeInteger.
        pass
        return result
    def hasContent_(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NumberOfDays', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('NumberOfDays')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'NumberOfDays':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='NumberOfDays')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='NumberOfDays', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='NumberOfDays'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NumberOfDays', fromsubclass_=False, pretty_print=True):
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
# end class NumberOfDays


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


class TimeFrameStructure(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DateFrom=None, DateTo=None, NumberOfDays=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DateFrom = DateFrom
        self.DateFrom_nsprefix_ = None
        self.DateTo = DateTo
        self.DateTo_nsprefix_ = None
        self.NumberOfDays = NumberOfDays
        self.validate_NumberOfDays(self.NumberOfDays)
        self.NumberOfDays_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TimeFrameStructure)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TimeFrameStructure.subclass:
            return TimeFrameStructure.subclass(*args_, **kwargs_)
        else:
            return TimeFrameStructure(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DateFrom(self):
        return self.DateFrom
    def set_DateFrom(self, DateFrom):
        self.DateFrom = DateFrom
    def get_DateTo(self):
        return self.DateTo
    def set_DateTo(self, DateTo):
        self.DateTo = DateTo
    def get_NumberOfDays(self):
        return self.NumberOfDays
    def set_NumberOfDays(self, NumberOfDays):
        self.NumberOfDays = NumberOfDays
    def validate_NumberOfDays(self, value):
        result = True
        # Validate type NumberOfDays, a restriction on NonNegativeInteger.
        pass
        return result
    def hasContent_(self):
        if (
            self.DateFrom is not None or
            self.DateTo is not None or
            self.NumberOfDays is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TimeFrameStructure', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TimeFrameStructure')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TimeFrameStructure':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TimeFrameStructure')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TimeFrameStructure', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TimeFrameStructure'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TimeFrameStructure', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DateFrom is not None:
            namespaceprefix_ = self.DateFrom_nsprefix_ + ':' if (UseCapturedNS_ and self.DateFrom_nsprefix_) else ''
            self.DateFrom.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DateFrom', pretty_print=pretty_print)
        if self.DateTo is not None:
            namespaceprefix_ = self.DateTo_nsprefix_ + ':' if (UseCapturedNS_ and self.DateTo_nsprefix_) else ''
            self.DateTo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DateTo', pretty_print=pretty_print)
        if self.NumberOfDays is not None:
            namespaceprefix_ = self.NumberOfDays_nsprefix_ + ':' if (UseCapturedNS_ and self.NumberOfDays_nsprefix_) else ''
            self.NumberOfDays.export(outfile, level, namespaceprefix_, namespacedef_='', name_='NumberOfDays', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DateFrom':
            obj_ = DateType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DateFrom = obj_
            obj_.original_tagname_ = 'DateFrom'
        elif nodeName_ == 'DateTo':
            obj_ = DateType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DateTo = obj_
            obj_.original_tagname_ = 'DateTo'
        elif nodeName_ == 'NumberOfDays':
            obj_ = None
            self.NumberOfDays = obj_
            obj_.original_tagname_ = 'NumberOfDays'
            # validate type NumberOfDays
            self.validate_NumberOfDays(self.NumberOfDays)
# end class TimeFrameStructure


class UsernameTokenStructure(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Username=None, Password=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Username = Username
        self.validate_NonZeroLengthString(self.Username)
        self.Username_nsprefix_ = None
        self.Password = Password
        self.Password_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UsernameTokenStructure)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UsernameTokenStructure.subclass:
            return UsernameTokenStructure.subclass(*args_, **kwargs_)
        else:
            return UsernameTokenStructure(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Username(self):
        return self.Username
    def set_Username(self, Username):
        self.Username = Username
    def get_Password(self):
        return self.Password
    def set_Password(self, Password):
        self.Password = Password
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
            self.Username is not None or
            self.Password is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UsernameTokenStructure', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UsernameTokenStructure')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UsernameTokenStructure':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UsernameTokenStructure')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UsernameTokenStructure', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UsernameTokenStructure'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UsernameTokenStructure', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Username is not None:
            namespaceprefix_ = self.Username_nsprefix_ + ':' if (UseCapturedNS_ and self.Username_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUsername>%s</%sUsername>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Username), input_name='Username')), namespaceprefix_ , eol_))
        if self.Password is not None:
            namespaceprefix_ = self.Password_nsprefix_ + ':' if (UseCapturedNS_ and self.Password_nsprefix_) else ''
            self.Password.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Password', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Username':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Username')
            value_ = self.gds_validate_string(value_, node, 'Username')
            self.Username = value_
            self.Username_nsprefix_ = child_.prefix
            # validate type NonZeroLengthString
            self.validate_NonZeroLengthString(self.Username)
        elif nodeName_ == 'Password':
            obj_ = PasswordType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Password = obj_
            obj_.original_tagname_ = 'Password'
# end class UsernameTokenStructure


class SearchCriteriaType(GeneratedsSuper):
    """The set of discriminators to be applied during a search."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, marketType=None, originCountry=None, AlternativeConsignmentNumber=None, ConsignmentNumber=None, CustomerReference=None, PieceReference=None, Account=None, Period=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.marketType = _cast(None, marketType)
        self.marketType_nsprefix_ = None
        self.originCountry = _cast(None, originCountry)
        self.originCountry_nsprefix_ = None
        if AlternativeConsignmentNumber is None:
            self.AlternativeConsignmentNumber = []
        else:
            self.AlternativeConsignmentNumber = AlternativeConsignmentNumber
        self.AlternativeConsignmentNumber_nsprefix_ = None
        if ConsignmentNumber is None:
            self.ConsignmentNumber = []
        else:
            self.ConsignmentNumber = ConsignmentNumber
        self.ConsignmentNumber_nsprefix_ = None
        if CustomerReference is None:
            self.CustomerReference = []
        else:
            self.CustomerReference = CustomerReference
        self.CustomerReference_nsprefix_ = None
        if PieceReference is None:
            self.PieceReference = []
        else:
            self.PieceReference = PieceReference
        self.PieceReference_nsprefix_ = None
        if Account is None:
            self.Account = []
        else:
            self.Account = Account
        self.Account_nsprefix_ = None
        self.Period = Period
        self.Period_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SearchCriteriaType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SearchCriteriaType.subclass:
            return SearchCriteriaType.subclass(*args_, **kwargs_)
        else:
            return SearchCriteriaType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AlternativeConsignmentNumber(self):
        return self.AlternativeConsignmentNumber
    def set_AlternativeConsignmentNumber(self, AlternativeConsignmentNumber):
        self.AlternativeConsignmentNumber = AlternativeConsignmentNumber
    def add_AlternativeConsignmentNumber(self, value):
        self.AlternativeConsignmentNumber.append(value)
    def insert_AlternativeConsignmentNumber_at(self, index, value):
        self.AlternativeConsignmentNumber.insert(index, value)
    def replace_AlternativeConsignmentNumber_at(self, index, value):
        self.AlternativeConsignmentNumber[index] = value
    def get_ConsignmentNumber(self):
        return self.ConsignmentNumber
    def set_ConsignmentNumber(self, ConsignmentNumber):
        self.ConsignmentNumber = ConsignmentNumber
    def add_ConsignmentNumber(self, value):
        self.ConsignmentNumber.append(value)
    def insert_ConsignmentNumber_at(self, index, value):
        self.ConsignmentNumber.insert(index, value)
    def replace_ConsignmentNumber_at(self, index, value):
        self.ConsignmentNumber[index] = value
    def get_CustomerReference(self):
        return self.CustomerReference
    def set_CustomerReference(self, CustomerReference):
        self.CustomerReference = CustomerReference
    def add_CustomerReference(self, value):
        self.CustomerReference.append(value)
    def insert_CustomerReference_at(self, index, value):
        self.CustomerReference.insert(index, value)
    def replace_CustomerReference_at(self, index, value):
        self.CustomerReference[index] = value
    def get_PieceReference(self):
        return self.PieceReference
    def set_PieceReference(self, PieceReference):
        self.PieceReference = PieceReference
    def add_PieceReference(self, value):
        self.PieceReference.append(value)
    def insert_PieceReference_at(self, index, value):
        self.PieceReference.insert(index, value)
    def replace_PieceReference_at(self, index, value):
        self.PieceReference[index] = value
    def get_Account(self):
        return self.Account
    def set_Account(self, Account):
        self.Account = Account
    def add_Account(self, value):
        self.Account.append(value)
    def insert_Account_at(self, index, value):
        self.Account.insert(index, value)
    def replace_Account_at(self, index, value):
        self.Account[index] = value
    def get_Period(self):
        return self.Period
    def set_Period(self, Period):
        self.Period = Period
    def get_marketType(self):
        return self.marketType
    def set_marketType(self, marketType):
        self.marketType = marketType
    def get_originCountry(self):
        return self.originCountry
    def set_originCountry(self, originCountry):
        self.originCountry = originCountry
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
    def validate_MarketTypeType(self, value):
        # Validate type MarketTypeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['Domestic', 'International']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on MarketTypeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
    def validate_CountryCodeType(self, value):
        # Validate type CountryCodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_CountryCodeType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_CountryCodeType_patterns_, ))
    validate_CountryCodeType_patterns_ = [['^([A-Z][A-Z][A-Z0-9]?)$']]
    def hasContent_(self):
        if (
            self.AlternativeConsignmentNumber or
            self.ConsignmentNumber or
            self.CustomerReference or
            self.PieceReference or
            self.Account or
            self.Period is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SearchCriteriaType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SearchCriteriaType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SearchCriteriaType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SearchCriteriaType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SearchCriteriaType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SearchCriteriaType'):
        if self.marketType is not None and 'marketType' not in already_processed:
            already_processed.add('marketType')
            outfile.write(' marketType=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.marketType), input_name='marketType')), ))
        if self.originCountry is not None and 'originCountry' not in already_processed:
            already_processed.add('originCountry')
            outfile.write(' originCountry=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.originCountry), input_name='originCountry')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SearchCriteriaType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for AlternativeConsignmentNumber_ in self.AlternativeConsignmentNumber:
            namespaceprefix_ = self.AlternativeConsignmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.AlternativeConsignmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAlternativeConsignmentNumber>%s</%sAlternativeConsignmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(AlternativeConsignmentNumber_), input_name='AlternativeConsignmentNumber')), namespaceprefix_ , eol_))
        for ConsignmentNumber_ in self.ConsignmentNumber:
            namespaceprefix_ = self.ConsignmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ConsignmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sConsignmentNumber>%s</%sConsignmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(ConsignmentNumber_), input_name='ConsignmentNumber')), namespaceprefix_ , eol_))
        for CustomerReference_ in self.CustomerReference:
            namespaceprefix_ = self.CustomerReference_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomerReference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustomerReference>%s</%sCustomerReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CustomerReference_), input_name='CustomerReference')), namespaceprefix_ , eol_))
        for PieceReference_ in self.PieceReference:
            namespaceprefix_ = self.PieceReference_nsprefix_ + ':' if (UseCapturedNS_ and self.PieceReference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPieceReference>%s</%sPieceReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(PieceReference_), input_name='PieceReference')), namespaceprefix_ , eol_))
        for Account_ in self.Account:
            namespaceprefix_ = self.Account_nsprefix_ + ':' if (UseCapturedNS_ and self.Account_nsprefix_) else ''
            Account_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Account', pretty_print=pretty_print)
        if self.Period is not None:
            namespaceprefix_ = self.Period_nsprefix_ + ':' if (UseCapturedNS_ and self.Period_nsprefix_) else ''
            self.Period.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Period', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('marketType', node)
        if value is not None and 'marketType' not in already_processed:
            already_processed.add('marketType')
            self.marketType = value
            self.validate_MarketTypeType(self.marketType)    # validate type MarketTypeType
        value = find_attr_value_('originCountry', node)
        if value is not None and 'originCountry' not in already_processed:
            already_processed.add('originCountry')
            self.originCountry = value
            self.validate_CountryCodeType(self.originCountry)    # validate type CountryCodeType
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'AlternativeConsignmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AlternativeConsignmentNumber')
            value_ = self.gds_validate_string(value_, node, 'AlternativeConsignmentNumber')
            self.AlternativeConsignmentNumber.append(value_)
            self.AlternativeConsignmentNumber_nsprefix_ = child_.prefix
            # validate type NonZeroLengthString
            self.validate_NonZeroLengthString(self.AlternativeConsignmentNumber[-1])
        elif nodeName_ == 'ConsignmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ConsignmentNumber')
            value_ = self.gds_validate_string(value_, node, 'ConsignmentNumber')
            self.ConsignmentNumber.append(value_)
            self.ConsignmentNumber_nsprefix_ = child_.prefix
            # validate type NonZeroLengthString
            self.validate_NonZeroLengthString(self.ConsignmentNumber[-1])
        elif nodeName_ == 'CustomerReference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CustomerReference')
            value_ = self.gds_validate_string(value_, node, 'CustomerReference')
            self.CustomerReference.append(value_)
            self.CustomerReference_nsprefix_ = child_.prefix
            # validate type NonZeroLengthString
            self.validate_NonZeroLengthString(self.CustomerReference[-1])
        elif nodeName_ == 'PieceReference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PieceReference')
            value_ = self.gds_validate_string(value_, node, 'PieceReference')
            self.PieceReference.append(value_)
            self.PieceReference_nsprefix_ = child_.prefix
            # validate type NonZeroLengthString
            self.validate_NonZeroLengthString(self.PieceReference[-1])
        elif nodeName_ == 'Account':
            obj_ = AccountStructure.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Account.append(obj_)
            obj_.original_tagname_ = 'Account'
        elif nodeName_ == 'Period':
            obj_ = TimeFrameStructure.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Period = obj_
            obj_.original_tagname_ = 'Period'
# end class SearchCriteriaType


class LevelOfDetailType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Complete=None, Summary=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Complete = Complete
        self.Complete_nsprefix_ = None
        self.Summary = Summary
        self.Summary_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LevelOfDetailType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LevelOfDetailType.subclass:
            return LevelOfDetailType.subclass(*args_, **kwargs_)
        else:
            return LevelOfDetailType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Complete(self):
        return self.Complete
    def set_Complete(self, Complete):
        self.Complete = Complete
    def get_Summary(self):
        return self.Summary
    def set_Summary(self, Summary):
        self.Summary = Summary
    def hasContent_(self):
        if (
            self.Complete is not None or
            self.Summary is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LevelOfDetailType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LevelOfDetailType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LevelOfDetailType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LevelOfDetailType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LevelOfDetailType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LevelOfDetailType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LevelOfDetailType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Complete is not None:
            namespaceprefix_ = self.Complete_nsprefix_ + ':' if (UseCapturedNS_ and self.Complete_nsprefix_) else ''
            self.Complete.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Complete', pretty_print=pretty_print)
        if self.Summary is not None:
            namespaceprefix_ = self.Summary_nsprefix_ + ':' if (UseCapturedNS_ and self.Summary_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSummary>%s</%sSummary>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Summary), input_name='Summary')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Complete':
            obj_ = CompleteType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Complete = obj_
            obj_.original_tagname_ = 'Complete'
        elif nodeName_ == 'Summary':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Summary')
            value_ = self.gds_validate_string(value_, node, 'Summary')
            self.Summary = value_
            self.Summary_nsprefix_ = child_.prefix
# end class LevelOfDetailType


class Summary(GeneratedsSuper):
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
                CurrentSubclassModule_, Summary)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Summary.subclass:
            return Summary.subclass(*args_, **kwargs_)
        else:
            return Summary(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Summary', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Summary')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Summary':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Summary')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Summary', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Summary'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Summary', fromsubclass_=False, pretty_print=True):
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
# end class Summary


class CompleteType(GeneratedsSuper):
    """By default summary results are returned. The presence of this element
    signifies that consignment details are to be populated along with the
    extra details specified by the associated attributes"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, originAddress=False, destinationAddress=False, shipment=False, package=False, podImage=False, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.originAddress = _cast(bool, originAddress)
        self.originAddress_nsprefix_ = None
        self.destinationAddress = _cast(bool, destinationAddress)
        self.destinationAddress_nsprefix_ = None
        self.shipment = _cast(bool, shipment)
        self.shipment_nsprefix_ = None
        self.package = _cast(bool, package)
        self.package_nsprefix_ = None
        self.podImage = _cast(bool, podImage)
        self.podImage_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CompleteType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CompleteType.subclass:
            return CompleteType.subclass(*args_, **kwargs_)
        else:
            return CompleteType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_originAddress(self):
        return self.originAddress
    def set_originAddress(self, originAddress):
        self.originAddress = originAddress
    def get_destinationAddress(self):
        return self.destinationAddress
    def set_destinationAddress(self, destinationAddress):
        self.destinationAddress = destinationAddress
    def get_shipment(self):
        return self.shipment
    def set_shipment(self, shipment):
        self.shipment = shipment
    def get_package(self):
        return self.package
    def set_package(self, package):
        self.package = package
    def get_podImage(self):
        return self.podImage
    def set_podImage(self, podImage):
        self.podImage = podImage
    def hasContent_(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CompleteType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CompleteType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CompleteType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CompleteType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CompleteType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CompleteType'):
        if self.originAddress and 'originAddress' not in already_processed:
            already_processed.add('originAddress')
            outfile.write(' originAddress="%s"' % self.gds_format_boolean(self.originAddress, input_name='originAddress'))
        if self.destinationAddress and 'destinationAddress' not in already_processed:
            already_processed.add('destinationAddress')
            outfile.write(' destinationAddress="%s"' % self.gds_format_boolean(self.destinationAddress, input_name='destinationAddress'))
        if self.shipment and 'shipment' not in already_processed:
            already_processed.add('shipment')
            outfile.write(' shipment="%s"' % self.gds_format_boolean(self.shipment, input_name='shipment'))
        if self.package and 'package' not in already_processed:
            already_processed.add('package')
            outfile.write(' package="%s"' % self.gds_format_boolean(self.package, input_name='package'))
        if self.podImage and 'podImage' not in already_processed:
            already_processed.add('podImage')
            outfile.write(' podImage="%s"' % self.gds_format_boolean(self.podImage, input_name='podImage'))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CompleteType', fromsubclass_=False, pretty_print=True):
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
        value = find_attr_value_('originAddress', node)
        if value is not None and 'originAddress' not in already_processed:
            already_processed.add('originAddress')
            if value in ('true', '1'):
                self.originAddress = True
            elif value in ('false', '0'):
                self.originAddress = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = find_attr_value_('destinationAddress', node)
        if value is not None and 'destinationAddress' not in already_processed:
            already_processed.add('destinationAddress')
            if value in ('true', '1'):
                self.destinationAddress = True
            elif value in ('false', '0'):
                self.destinationAddress = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = find_attr_value_('shipment', node)
        if value is not None and 'shipment' not in already_processed:
            already_processed.add('shipment')
            if value in ('true', '1'):
                self.shipment = True
            elif value in ('false', '0'):
                self.shipment = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = find_attr_value_('package', node)
        if value is not None and 'package' not in already_processed:
            already_processed.add('package')
            if value in ('true', '1'):
                self.package = True
            elif value in ('false', '0'):
                self.package = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
        value = find_attr_value_('podImage', node)
        if value is not None and 'podImage' not in already_processed:
            already_processed.add('podImage')
            if value in ('true', '1'):
                self.podImage = True
            elif value in ('false', '0'):
                self.podImage = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class CompleteType


class PasswordType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Type='PasswordText', valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Type = _cast(None, Type)
        self.Type_nsprefix_ = None
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PasswordType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PasswordType.subclass:
            return PasswordType.subclass(*args_, **kwargs_)
        else:
            return PasswordType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PasswordType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PasswordType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PasswordType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PasswordType')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PasswordType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PasswordType'):
        if self.Type != "PasswordText" and 'Type' not in already_processed:
            already_processed.add('Type')
            outfile.write(' Type=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.Type), input_name='Type')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PasswordType', fromsubclass_=False, pretty_print=True):
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
        value = find_attr_value_('Type', node)
        if value is not None and 'Type' not in already_processed:
            already_processed.add('Type')
            self.Type = value
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class PasswordType


GDSClassesMapping = {
    'Account': AccountStructure,
    'DateFrom': DateType,
    'DateTo': DateType,
    'Period': TimeFrameStructure,
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
        rootTag = 'TrackRequest'
        rootClass = TrackRequest
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
        rootTag = 'TrackRequest'
        rootClass = TrackRequest
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
        rootTag = 'TrackRequest'
        rootClass = TrackRequest
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
        rootTag = 'TrackRequest'
        rootClass = TrackRequest
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from track_request_v3_1 import *\n\n')
        sys.stdout.write('import track_request_v3_1 as model_\n\n')
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
    "AccountStructure",
    "CompleteType",
    "DateType",
    "LevelOfDetailType",
    "NumberOfDays",
    "PasswordType",
    "SearchCriteriaType",
    "Summary",
    "TimeFrameStructure",
    "TrackRequest",
    "UsernameTokenStructure"
]
