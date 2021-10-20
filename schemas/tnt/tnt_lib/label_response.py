#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Wed Feb 24 19:49:28 2021 by generateDS.py version 2.37.16.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './tnt_lib/label_response.py')
#
# Command line arguments:
#   ./schemas/label_response.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./tnt_lib/label_response.py" ./schemas/label_response.xsd
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


class booleanEnum(str, Enum):
    N='N'
    Y='Y'


class cashTypeEnum(str, Enum):
    _0='0'
    _1='1'


class productTypeEnum(str, Enum):
    N='N'
    D='D'


class renderInstructionsType1(str, Enum):
    """This is the instruction to indicate if, and how,
    the field will be displayed."""
    YES='yes'
    NO='no'
    HIGHLIGHTED='highlighted'


class senderReceiverEnum(str, Enum):
    S='S'
    R='R'


class symbologyType(str, Enum):
    """This denotes the symbology to be used to render the barcode,
    e.g. '128C' French domestic labels use '2of5Int' and '128B' for the
    customer reference barcode."""
    _1_28_B='128B'
    _1_28_C='128C'
    _2_OF_5_INT='2of5Int'


class symbologyType2(str, Enum):
    """This denotes the symbology to be used to render the barcode,
    e.g. 'pdf417'."""
    PDF_417='pdf417'


class labelResponse(GeneratedsSuper):
    """The root XML tag for the data returned from ExpressLabel
    for the production of routing labels"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, consignment=None, brokenRules=None, fault=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if consignment is None:
            self.consignment = []
        else:
            self.consignment = consignment
        self.consignment_nsprefix_ = None
        if brokenRules is None:
            self.brokenRules = []
        else:
            self.brokenRules = brokenRules
        self.brokenRules_nsprefix_ = None
        if fault is None:
            self.fault = []
        else:
            self.fault = fault
        self.fault_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, labelResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if labelResponse.subclass:
            return labelResponse.subclass(*args_, **kwargs_)
        else:
            return labelResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_consignment(self):
        return self.consignment
    def set_consignment(self, consignment):
        self.consignment = consignment
    def add_consignment(self, value):
        self.consignment.append(value)
    def insert_consignment_at(self, index, value):
        self.consignment.insert(index, value)
    def replace_consignment_at(self, index, value):
        self.consignment[index] = value
    def get_brokenRules(self):
        return self.brokenRules
    def set_brokenRules(self, brokenRules):
        self.brokenRules = brokenRules
    def add_brokenRules(self, value):
        self.brokenRules.append(value)
    def insert_brokenRules_at(self, index, value):
        self.brokenRules.insert(index, value)
    def replace_brokenRules_at(self, index, value):
        self.brokenRules[index] = value
    def get_fault(self):
        return self.fault
    def set_fault(self, fault):
        self.fault = fault
    def add_fault(self, value):
        self.fault.append(value)
    def insert_fault_at(self, index, value):
        self.fault.insert(index, value)
    def replace_fault_at(self, index, value):
        self.fault[index] = value
    def hasContent_(self):
        if (
            self.consignment or
            self.brokenRules or
            self.fault
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='labelResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('labelResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'labelResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='labelResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='labelResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='labelResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='labelResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for consignment_ in self.consignment:
            namespaceprefix_ = self.consignment_nsprefix_ + ':' if (UseCapturedNS_ and self.consignment_nsprefix_) else ''
            consignment_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='consignment', pretty_print=pretty_print)
        for brokenRules_ in self.brokenRules:
            namespaceprefix_ = self.brokenRules_nsprefix_ + ':' if (UseCapturedNS_ and self.brokenRules_nsprefix_) else ''
            brokenRules_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='brokenRules', pretty_print=pretty_print)
        for fault_ in self.fault:
            namespaceprefix_ = self.fault_nsprefix_ + ':' if (UseCapturedNS_ and self.fault_nsprefix_) else ''
            fault_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='fault', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'consignment':
            obj_ = consignmentResponseType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.consignment.append(obj_)
            obj_.original_tagname_ = 'consignment'
        elif nodeName_ == 'brokenRules':
            obj_ = brokenRules.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.brokenRules.append(obj_)
            obj_.original_tagname_ = 'brokenRules'
        elif nodeName_ == 'fault':
            obj_ = fault.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.fault.append(obj_)
            obj_.original_tagname_ = 'fault'
# end class labelResponse


class consignmentResponseType(GeneratedsSuper):
    """There is one of these sections per unique consignment
    within the labels being printed."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, key=None, pieceLabelData=None, consignmentLabelData=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.key = _cast(None, key)
        self.key_nsprefix_ = None
        if pieceLabelData is None:
            self.pieceLabelData = []
        else:
            self.pieceLabelData = pieceLabelData
        self.pieceLabelData_nsprefix_ = None
        self.consignmentLabelData = consignmentLabelData
        self.consignmentLabelData_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, consignmentResponseType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if consignmentResponseType.subclass:
            return consignmentResponseType.subclass(*args_, **kwargs_)
        else:
            return consignmentResponseType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_pieceLabelData(self):
        return self.pieceLabelData
    def set_pieceLabelData(self, pieceLabelData):
        self.pieceLabelData = pieceLabelData
    def add_pieceLabelData(self, value):
        self.pieceLabelData.append(value)
    def insert_pieceLabelData_at(self, index, value):
        self.pieceLabelData.insert(index, value)
    def replace_pieceLabelData_at(self, index, value):
        self.pieceLabelData[index] = value
    def get_consignmentLabelData(self):
        return self.consignmentLabelData
    def set_consignmentLabelData(self, consignmentLabelData):
        self.consignmentLabelData = consignmentLabelData
    def get_key(self):
        return self.key
    def set_key(self, key):
        self.key = key
    def hasContent_(self):
        if (
            self.pieceLabelData or
            self.consignmentLabelData is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='consignmentResponseType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('consignmentResponseType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'consignmentResponseType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='consignmentResponseType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='consignmentResponseType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='consignmentResponseType'):
        if self.key is not None and 'key' not in already_processed:
            already_processed.add('key')
            outfile.write(' key=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.key), input_name='key')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='consignmentResponseType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for pieceLabelData_ in self.pieceLabelData:
            namespaceprefix_ = self.pieceLabelData_nsprefix_ + ':' if (UseCapturedNS_ and self.pieceLabelData_nsprefix_) else ''
            pieceLabelData_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='pieceLabelData', pretty_print=pretty_print)
        if self.consignmentLabelData is not None:
            namespaceprefix_ = self.consignmentLabelData_nsprefix_ + ':' if (UseCapturedNS_ and self.consignmentLabelData_nsprefix_) else ''
            self.consignmentLabelData.export(outfile, level, namespaceprefix_, namespacedef_='', name_='consignmentLabelData', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('key', node)
        if value is not None and 'key' not in already_processed:
            already_processed.add('key')
            self.key = value
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'pieceLabelData':
            obj_ = pieceRoutingLabelType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.pieceLabelData.append(obj_)
            obj_.original_tagname_ = 'pieceLabelData'
        elif nodeName_ == 'consignmentLabelData':
            obj_ = consignmentRoutingLabelType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.consignmentLabelData = obj_
            obj_.original_tagname_ = 'consignmentLabelData'
# end class consignmentResponseType


class pieceRoutingLabelType(GeneratedsSuper):
    """Contains information specific to the piece being that a
    routing label is being created for."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, pieceNumber=None, weightDisplay=None, pieceReference=None, barcode=None, barcodeForCustomer=None, twoDBarcode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.pieceNumber = pieceNumber
        self.pieceNumber_nsprefix_ = None
        self.weightDisplay = weightDisplay
        self.weightDisplay_nsprefix_ = None
        self.pieceReference = pieceReference
        self.pieceReference_nsprefix_ = None
        self.barcode = barcode
        self.barcode_nsprefix_ = None
        self.barcodeForCustomer = barcodeForCustomer
        self.barcodeForCustomer_nsprefix_ = None
        self.twoDBarcode = twoDBarcode
        self.twoDBarcode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, pieceRoutingLabelType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if pieceRoutingLabelType.subclass:
            return pieceRoutingLabelType.subclass(*args_, **kwargs_)
        else:
            return pieceRoutingLabelType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_pieceNumber(self):
        return self.pieceNumber
    def set_pieceNumber(self, pieceNumber):
        self.pieceNumber = pieceNumber
    def get_weightDisplay(self):
        return self.weightDisplay
    def set_weightDisplay(self, weightDisplay):
        self.weightDisplay = weightDisplay
    def get_pieceReference(self):
        return self.pieceReference
    def set_pieceReference(self, pieceReference):
        self.pieceReference = pieceReference
    def get_barcode(self):
        return self.barcode
    def set_barcode(self, barcode):
        self.barcode = barcode
    def get_barcodeForCustomer(self):
        return self.barcodeForCustomer
    def set_barcodeForCustomer(self, barcodeForCustomer):
        self.barcodeForCustomer = barcodeForCustomer
    def get_twoDBarcode(self):
        return self.twoDBarcode
    def set_twoDBarcode(self, twoDBarcode):
        self.twoDBarcode = twoDBarcode
    def hasContent_(self):
        if (
            self.pieceNumber is not None or
            self.weightDisplay is not None or
            self.pieceReference is not None or
            self.barcode is not None or
            self.barcodeForCustomer is not None or
            self.twoDBarcode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='pieceRoutingLabelType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('pieceRoutingLabelType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'pieceRoutingLabelType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='pieceRoutingLabelType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='pieceRoutingLabelType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='pieceRoutingLabelType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='pieceRoutingLabelType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.pieceNumber is not None:
            namespaceprefix_ = self.pieceNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.pieceNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spieceNumber>%s</%spieceNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.pieceNumber, input_name='pieceNumber'), namespaceprefix_ , eol_))
        if self.weightDisplay is not None:
            namespaceprefix_ = self.weightDisplay_nsprefix_ + ':' if (UseCapturedNS_ and self.weightDisplay_nsprefix_) else ''
            self.weightDisplay.export(outfile, level, namespaceprefix_, namespacedef_='', name_='weightDisplay', pretty_print=pretty_print)
        if self.pieceReference is not None:
            namespaceprefix_ = self.pieceReference_nsprefix_ + ':' if (UseCapturedNS_ and self.pieceReference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spieceReference>%s</%spieceReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.pieceReference), input_name='pieceReference')), namespaceprefix_ , eol_))
        if self.barcode is not None:
            namespaceprefix_ = self.barcode_nsprefix_ + ':' if (UseCapturedNS_ and self.barcode_nsprefix_) else ''
            self.barcode.export(outfile, level, namespaceprefix_, namespacedef_='', name_='barcode', pretty_print=pretty_print)
        if self.barcodeForCustomer is not None:
            namespaceprefix_ = self.barcodeForCustomer_nsprefix_ + ':' if (UseCapturedNS_ and self.barcodeForCustomer_nsprefix_) else ''
            self.barcodeForCustomer.export(outfile, level, namespaceprefix_, namespacedef_='', name_='barcodeForCustomer', pretty_print=pretty_print)
        if self.twoDBarcode is not None:
            namespaceprefix_ = self.twoDBarcode_nsprefix_ + ':' if (UseCapturedNS_ and self.twoDBarcode_nsprefix_) else ''
            self.twoDBarcode.export(outfile, level, namespaceprefix_, namespacedef_='', name_='twoDBarcode', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'pieceNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'pieceNumber')
            ival_ = self.gds_validate_integer(ival_, node, 'pieceNumber')
            self.pieceNumber = ival_
            self.pieceNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'weightDisplay':
            obj_ = renderInstructionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.weightDisplay = obj_
            obj_.original_tagname_ = 'weightDisplay'
        elif nodeName_ == 'pieceReference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'pieceReference')
            value_ = self.gds_validate_string(value_, node, 'pieceReference')
            self.pieceReference = value_
            self.pieceReference_nsprefix_ = child_.prefix
        elif nodeName_ == 'barcode':
            obj_ = barcodeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.barcode = obj_
            obj_.original_tagname_ = 'barcode'
        elif nodeName_ == 'barcodeForCustomer':
            obj_ = barcodeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.barcodeForCustomer = obj_
            obj_.original_tagname_ = 'barcodeForCustomer'
        elif nodeName_ == 'twoDBarcode':
            obj_ = twoDBarcodeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.twoDBarcode = obj_
            obj_.original_tagname_ = 'twoDBarcode'
# end class pieceRoutingLabelType


class destinationDepotType(GeneratedsSuper):
    """Details relevant to the destination TNT depot."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, depotCode=None, dueDayOfMonth=None, dueDate=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.depotCode = depotCode
        self.depotCode_nsprefix_ = None
        self.dueDayOfMonth = dueDayOfMonth
        self.dueDayOfMonth_nsprefix_ = None
        if isinstance(dueDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(dueDate, '%Y-%m-%d').date()
        else:
            initvalue_ = dueDate
        self.dueDate = initvalue_
        self.dueDate_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, destinationDepotType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if destinationDepotType.subclass:
            return destinationDepotType.subclass(*args_, **kwargs_)
        else:
            return destinationDepotType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_depotCode(self):
        return self.depotCode
    def set_depotCode(self, depotCode):
        self.depotCode = depotCode
    def get_dueDayOfMonth(self):
        return self.dueDayOfMonth
    def set_dueDayOfMonth(self, dueDayOfMonth):
        self.dueDayOfMonth = dueDayOfMonth
    def get_dueDate(self):
        return self.dueDate
    def set_dueDate(self, dueDate):
        self.dueDate = dueDate
    def hasContent_(self):
        if (
            self.depotCode is not None or
            self.dueDayOfMonth is not None or
            self.dueDate is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='destinationDepotType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('destinationDepotType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'destinationDepotType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='destinationDepotType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='destinationDepotType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='destinationDepotType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='destinationDepotType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.depotCode is not None:
            namespaceprefix_ = self.depotCode_nsprefix_ + ':' if (UseCapturedNS_ and self.depotCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdepotCode>%s</%sdepotCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.depotCode), input_name='depotCode')), namespaceprefix_ , eol_))
        if self.dueDayOfMonth is not None:
            namespaceprefix_ = self.dueDayOfMonth_nsprefix_ + ':' if (UseCapturedNS_ and self.dueDayOfMonth_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdueDayOfMonth>%s</%sdueDayOfMonth>%s' % (namespaceprefix_ , self.gds_format_integer(self.dueDayOfMonth, input_name='dueDayOfMonth'), namespaceprefix_ , eol_))
        if self.dueDate is not None:
            namespaceprefix_ = self.dueDate_nsprefix_ + ':' if (UseCapturedNS_ and self.dueDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdueDate>%s</%sdueDate>%s' % (namespaceprefix_ , self.gds_format_date(self.dueDate, input_name='dueDate'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'depotCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'depotCode')
            value_ = self.gds_validate_string(value_, node, 'depotCode')
            self.depotCode = value_
            self.depotCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'dueDayOfMonth' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'dueDayOfMonth')
            ival_ = self.gds_validate_integer(ival_, node, 'dueDayOfMonth')
            self.dueDayOfMonth = ival_
            self.dueDayOfMonth_nsprefix_ = child_.prefix
        elif nodeName_ == 'dueDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.dueDate = dval_
            self.dueDate_nsprefix_ = child_.prefix
# end class destinationDepotType


class consignmentRoutingLabelType(GeneratedsSuper):
    """There will be one of these sections per
    consignment, related to 1 or more piece
    label data sections as appropriate. This XML
    fragment stores all of the common
    consignment information for the pieces being
    labelled."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, consignmentNumber=None, sender=None, delivery=None, contact=None, account=None, totalNumberOfPieces=None, product=None, option=None, collectionDate=None, marketDisplay=None, transportDisplay=None, freeCirculationDisplay=None, sortSplitText=None, xrayDisplay=None, originDepot=None, transitDepots=None, destinationDepot=None, microzone=None, clusterCode=None, legalComments=None, cashAmount=None, specialInstructions=None, bulkShipment=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.consignmentNumber = consignmentNumber
        self.consignmentNumber_nsprefix_ = None
        self.sender = sender
        self.sender_nsprefix_ = None
        self.delivery = delivery
        self.delivery_nsprefix_ = None
        self.contact = contact
        self.contact_nsprefix_ = None
        self.account = account
        self.account_nsprefix_ = None
        self.totalNumberOfPieces = totalNumberOfPieces
        self.totalNumberOfPieces_nsprefix_ = None
        self.product = product
        self.product_nsprefix_ = None
        if option is None:
            self.option = []
        else:
            self.option = option
        self.option_nsprefix_ = None
        if isinstance(collectionDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(collectionDate, '%Y-%m-%d').date()
        else:
            initvalue_ = collectionDate
        self.collectionDate = initvalue_
        self.collectionDate_nsprefix_ = None
        self.marketDisplay = marketDisplay
        self.marketDisplay_nsprefix_ = None
        self.transportDisplay = transportDisplay
        self.transportDisplay_nsprefix_ = None
        self.freeCirculationDisplay = freeCirculationDisplay
        self.freeCirculationDisplay_nsprefix_ = None
        self.sortSplitText = sortSplitText
        self.sortSplitText_nsprefix_ = None
        self.xrayDisplay = xrayDisplay
        self.xrayDisplay_nsprefix_ = None
        self.originDepot = originDepot
        self.originDepot_nsprefix_ = None
        self.transitDepots = transitDepots
        self.transitDepots_nsprefix_ = None
        self.destinationDepot = destinationDepot
        self.destinationDepot_nsprefix_ = None
        self.microzone = microzone
        self.microzone_nsprefix_ = None
        self.clusterCode = clusterCode
        self.clusterCode_nsprefix_ = None
        self.legalComments = legalComments
        self.legalComments_nsprefix_ = None
        self.cashAmount = cashAmount
        self.cashAmount_nsprefix_ = None
        self.specialInstructions = specialInstructions
        self.specialInstructions_nsprefix_ = None
        self.bulkShipment = bulkShipment
        self.bulkShipment_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, consignmentRoutingLabelType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if consignmentRoutingLabelType.subclass:
            return consignmentRoutingLabelType.subclass(*args_, **kwargs_)
        else:
            return consignmentRoutingLabelType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_consignmentNumber(self):
        return self.consignmentNumber
    def set_consignmentNumber(self, consignmentNumber):
        self.consignmentNumber = consignmentNumber
    def get_sender(self):
        return self.sender
    def set_sender(self, sender):
        self.sender = sender
    def get_delivery(self):
        return self.delivery
    def set_delivery(self, delivery):
        self.delivery = delivery
    def get_contact(self):
        return self.contact
    def set_contact(self, contact):
        self.contact = contact
    def get_account(self):
        return self.account
    def set_account(self, account):
        self.account = account
    def get_totalNumberOfPieces(self):
        return self.totalNumberOfPieces
    def set_totalNumberOfPieces(self, totalNumberOfPieces):
        self.totalNumberOfPieces = totalNumberOfPieces
    def get_product(self):
        return self.product
    def set_product(self, product):
        self.product = product
    def get_option(self):
        return self.option
    def set_option(self, option):
        self.option = option
    def add_option(self, value):
        self.option.append(value)
    def insert_option_at(self, index, value):
        self.option.insert(index, value)
    def replace_option_at(self, index, value):
        self.option[index] = value
    def get_collectionDate(self):
        return self.collectionDate
    def set_collectionDate(self, collectionDate):
        self.collectionDate = collectionDate
    def get_marketDisplay(self):
        return self.marketDisplay
    def set_marketDisplay(self, marketDisplay):
        self.marketDisplay = marketDisplay
    def get_transportDisplay(self):
        return self.transportDisplay
    def set_transportDisplay(self, transportDisplay):
        self.transportDisplay = transportDisplay
    def get_freeCirculationDisplay(self):
        return self.freeCirculationDisplay
    def set_freeCirculationDisplay(self, freeCirculationDisplay):
        self.freeCirculationDisplay = freeCirculationDisplay
    def get_sortSplitText(self):
        return self.sortSplitText
    def set_sortSplitText(self, sortSplitText):
        self.sortSplitText = sortSplitText
    def get_xrayDisplay(self):
        return self.xrayDisplay
    def set_xrayDisplay(self, xrayDisplay):
        self.xrayDisplay = xrayDisplay
    def get_originDepot(self):
        return self.originDepot
    def set_originDepot(self, originDepot):
        self.originDepot = originDepot
    def get_transitDepots(self):
        return self.transitDepots
    def set_transitDepots(self, transitDepots):
        self.transitDepots = transitDepots
    def get_destinationDepot(self):
        return self.destinationDepot
    def set_destinationDepot(self, destinationDepot):
        self.destinationDepot = destinationDepot
    def get_microzone(self):
        return self.microzone
    def set_microzone(self, microzone):
        self.microzone = microzone
    def get_clusterCode(self):
        return self.clusterCode
    def set_clusterCode(self, clusterCode):
        self.clusterCode = clusterCode
    def get_legalComments(self):
        return self.legalComments
    def set_legalComments(self, legalComments):
        self.legalComments = legalComments
    def get_cashAmount(self):
        return self.cashAmount
    def set_cashAmount(self, cashAmount):
        self.cashAmount = cashAmount
    def get_specialInstructions(self):
        return self.specialInstructions
    def set_specialInstructions(self, specialInstructions):
        self.specialInstructions = specialInstructions
    def get_bulkShipment(self):
        return self.bulkShipment
    def set_bulkShipment(self, bulkShipment):
        self.bulkShipment = bulkShipment
    def hasContent_(self):
        if (
            self.consignmentNumber is not None or
            self.sender is not None or
            self.delivery is not None or
            self.contact is not None or
            self.account is not None or
            self.totalNumberOfPieces is not None or
            self.product is not None or
            self.option or
            self.collectionDate is not None or
            self.marketDisplay is not None or
            self.transportDisplay is not None or
            self.freeCirculationDisplay is not None or
            self.sortSplitText is not None or
            self.xrayDisplay is not None or
            self.originDepot is not None or
            self.transitDepots is not None or
            self.destinationDepot is not None or
            self.microzone is not None or
            self.clusterCode is not None or
            self.legalComments is not None or
            self.cashAmount is not None or
            self.specialInstructions is not None or
            self.bulkShipment is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='consignmentRoutingLabelType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('consignmentRoutingLabelType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'consignmentRoutingLabelType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='consignmentRoutingLabelType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='consignmentRoutingLabelType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='consignmentRoutingLabelType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='consignmentRoutingLabelType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.consignmentNumber is not None:
            namespaceprefix_ = self.consignmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.consignmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sconsignmentNumber>%s</%sconsignmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.consignmentNumber), input_name='consignmentNumber')), namespaceprefix_ , eol_))
        if self.sender is not None:
            namespaceprefix_ = self.sender_nsprefix_ + ':' if (UseCapturedNS_ and self.sender_nsprefix_) else ''
            self.sender.export(outfile, level, namespaceprefix_, namespacedef_='', name_='sender', pretty_print=pretty_print)
        if self.delivery is not None:
            namespaceprefix_ = self.delivery_nsprefix_ + ':' if (UseCapturedNS_ and self.delivery_nsprefix_) else ''
            self.delivery.export(outfile, level, namespaceprefix_, namespacedef_='', name_='delivery', pretty_print=pretty_print)
        if self.contact is not None:
            namespaceprefix_ = self.contact_nsprefix_ + ':' if (UseCapturedNS_ and self.contact_nsprefix_) else ''
            self.contact.export(outfile, level, namespaceprefix_, namespacedef_='', name_='contact', pretty_print=pretty_print)
        if self.account is not None:
            namespaceprefix_ = self.account_nsprefix_ + ':' if (UseCapturedNS_ and self.account_nsprefix_) else ''
            self.account.export(outfile, level, namespaceprefix_, namespacedef_='', name_='account', pretty_print=pretty_print)
        if self.totalNumberOfPieces is not None:
            namespaceprefix_ = self.totalNumberOfPieces_nsprefix_ + ':' if (UseCapturedNS_ and self.totalNumberOfPieces_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stotalNumberOfPieces>%s</%stotalNumberOfPieces>%s' % (namespaceprefix_ , self.gds_format_integer(self.totalNumberOfPieces, input_name='totalNumberOfPieces'), namespaceprefix_ , eol_))
        if self.product is not None:
            namespaceprefix_ = self.product_nsprefix_ + ':' if (UseCapturedNS_ and self.product_nsprefix_) else ''
            self.product.export(outfile, level, namespaceprefix_, namespacedef_='', name_='product', pretty_print=pretty_print)
        for option_ in self.option:
            namespaceprefix_ = self.option_nsprefix_ + ':' if (UseCapturedNS_ and self.option_nsprefix_) else ''
            option_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='option', pretty_print=pretty_print)
        if self.collectionDate is not None:
            namespaceprefix_ = self.collectionDate_nsprefix_ + ':' if (UseCapturedNS_ and self.collectionDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scollectionDate>%s</%scollectionDate>%s' % (namespaceprefix_ , self.gds_format_date(self.collectionDate, input_name='collectionDate'), namespaceprefix_ , eol_))
        if self.marketDisplay is not None:
            namespaceprefix_ = self.marketDisplay_nsprefix_ + ':' if (UseCapturedNS_ and self.marketDisplay_nsprefix_) else ''
            self.marketDisplay.export(outfile, level, namespaceprefix_, namespacedef_='', name_='marketDisplay', pretty_print=pretty_print)
        if self.transportDisplay is not None:
            namespaceprefix_ = self.transportDisplay_nsprefix_ + ':' if (UseCapturedNS_ and self.transportDisplay_nsprefix_) else ''
            self.transportDisplay.export(outfile, level, namespaceprefix_, namespacedef_='', name_='transportDisplay', pretty_print=pretty_print)
        if self.freeCirculationDisplay is not None:
            namespaceprefix_ = self.freeCirculationDisplay_nsprefix_ + ':' if (UseCapturedNS_ and self.freeCirculationDisplay_nsprefix_) else ''
            self.freeCirculationDisplay.export(outfile, level, namespaceprefix_, namespacedef_='', name_='freeCirculationDisplay', pretty_print=pretty_print)
        if self.sortSplitText is not None:
            namespaceprefix_ = self.sortSplitText_nsprefix_ + ':' if (UseCapturedNS_ and self.sortSplitText_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssortSplitText>%s</%ssortSplitText>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.sortSplitText), input_name='sortSplitText')), namespaceprefix_ , eol_))
        if self.xrayDisplay is not None:
            namespaceprefix_ = self.xrayDisplay_nsprefix_ + ':' if (UseCapturedNS_ and self.xrayDisplay_nsprefix_) else ''
            self.xrayDisplay.export(outfile, level, namespaceprefix_, namespacedef_='', name_='xrayDisplay', pretty_print=pretty_print)
        if self.originDepot is not None:
            namespaceprefix_ = self.originDepot_nsprefix_ + ':' if (UseCapturedNS_ and self.originDepot_nsprefix_) else ''
            self.originDepot.export(outfile, level, namespaceprefix_, namespacedef_='', name_='originDepot', pretty_print=pretty_print)
        if self.transitDepots is not None:
            namespaceprefix_ = self.transitDepots_nsprefix_ + ':' if (UseCapturedNS_ and self.transitDepots_nsprefix_) else ''
            self.transitDepots.export(outfile, level, namespaceprefix_, namespacedef_='', name_='transitDepots', pretty_print=pretty_print)
        if self.destinationDepot is not None:
            namespaceprefix_ = self.destinationDepot_nsprefix_ + ':' if (UseCapturedNS_ and self.destinationDepot_nsprefix_) else ''
            self.destinationDepot.export(outfile, level, namespaceprefix_, namespacedef_='', name_='destinationDepot', pretty_print=pretty_print)
        if self.microzone is not None:
            namespaceprefix_ = self.microzone_nsprefix_ + ':' if (UseCapturedNS_ and self.microzone_nsprefix_) else ''
            self.microzone.export(outfile, level, namespaceprefix_, namespacedef_='', name_='microzone', pretty_print=pretty_print)
        if self.clusterCode is not None:
            namespaceprefix_ = self.clusterCode_nsprefix_ + ':' if (UseCapturedNS_ and self.clusterCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sclusterCode>%s</%sclusterCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.clusterCode), input_name='clusterCode')), namespaceprefix_ , eol_))
        if self.legalComments is not None:
            namespaceprefix_ = self.legalComments_nsprefix_ + ':' if (UseCapturedNS_ and self.legalComments_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slegalComments>%s</%slegalComments>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.legalComments), input_name='legalComments')), namespaceprefix_ , eol_))
        if self.cashAmount is not None:
            namespaceprefix_ = self.cashAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.cashAmount_nsprefix_) else ''
            self.cashAmount.export(outfile, level, namespaceprefix_, namespacedef_='', name_='cashAmount', pretty_print=pretty_print)
        if self.specialInstructions is not None:
            namespaceprefix_ = self.specialInstructions_nsprefix_ + ':' if (UseCapturedNS_ and self.specialInstructions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sspecialInstructions>%s</%sspecialInstructions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.specialInstructions), input_name='specialInstructions')), namespaceprefix_ , eol_))
        if self.bulkShipment is not None:
            namespaceprefix_ = self.bulkShipment_nsprefix_ + ':' if (UseCapturedNS_ and self.bulkShipment_nsprefix_) else ''
            self.bulkShipment.export(outfile, level, namespaceprefix_, namespacedef_='', name_='bulkShipment', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'consignmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'consignmentNumber')
            value_ = self.gds_validate_string(value_, node, 'consignmentNumber')
            self.consignmentNumber = value_
            self.consignmentNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'sender':
            obj_ = nameAndAddressResponseType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.sender = obj_
            obj_.original_tagname_ = 'sender'
        elif nodeName_ == 'delivery':
            obj_ = nameAndAddressResponseType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.delivery = obj_
            obj_.original_tagname_ = 'delivery'
        elif nodeName_ == 'contact':
            obj_ = contactType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.contact = obj_
            obj_.original_tagname_ = 'contact'
        elif nodeName_ == 'account':
            obj_ = accountType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.account = obj_
            obj_.original_tagname_ = 'account'
        elif nodeName_ == 'totalNumberOfPieces' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'totalNumberOfPieces')
            ival_ = self.gds_validate_integer(ival_, node, 'totalNumberOfPieces')
            self.totalNumberOfPieces = ival_
            self.totalNumberOfPieces_nsprefix_ = child_.prefix
        elif nodeName_ == 'product':
            obj_ = productDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.product = obj_
            obj_.original_tagname_ = 'product'
        elif nodeName_ == 'option':
            obj_ = optionDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.option.append(obj_)
            obj_.original_tagname_ = 'option'
        elif nodeName_ == 'collectionDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.collectionDate = dval_
            self.collectionDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'marketDisplay':
            obj_ = renderInstructionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.marketDisplay = obj_
            obj_.original_tagname_ = 'marketDisplay'
        elif nodeName_ == 'transportDisplay':
            obj_ = renderInstructionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.transportDisplay = obj_
            obj_.original_tagname_ = 'transportDisplay'
        elif nodeName_ == 'freeCirculationDisplay':
            obj_ = renderInstructionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.freeCirculationDisplay = obj_
            obj_.original_tagname_ = 'freeCirculationDisplay'
        elif nodeName_ == 'sortSplitText':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'sortSplitText')
            value_ = self.gds_validate_string(value_, node, 'sortSplitText')
            self.sortSplitText = value_
            self.sortSplitText_nsprefix_ = child_.prefix
        elif nodeName_ == 'xrayDisplay':
            obj_ = renderInstructionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.xrayDisplay = obj_
            obj_.original_tagname_ = 'xrayDisplay'
        elif nodeName_ == 'originDepot':
            obj_ = depotType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.originDepot = obj_
            obj_.original_tagname_ = 'originDepot'
        elif nodeName_ == 'transitDepots':
            obj_ = transitDepotListType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.transitDepots = obj_
            obj_.original_tagname_ = 'transitDepots'
        elif nodeName_ == 'destinationDepot':
            obj_ = destinationDepotType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.destinationDepot = obj_
            obj_.original_tagname_ = 'destinationDepot'
        elif nodeName_ == 'microzone':
            obj_ = renderInstructionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.microzone = obj_
            obj_.original_tagname_ = 'microzone'
        elif nodeName_ == 'clusterCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'clusterCode')
            value_ = self.gds_validate_string(value_, node, 'clusterCode')
            self.clusterCode = value_
            self.clusterCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'legalComments':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'legalComments')
            value_ = self.gds_validate_string(value_, node, 'legalComments')
            self.legalComments = value_
            self.legalComments_nsprefix_ = child_.prefix
        elif nodeName_ == 'cashAmount':
            obj_ = renderInstructionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.cashAmount = obj_
            obj_.original_tagname_ = 'cashAmount'
        elif nodeName_ == 'specialInstructions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'specialInstructions')
            value_ = self.gds_validate_string(value_, node, 'specialInstructions')
            self.specialInstructions = value_
            self.specialInstructions_nsprefix_ = child_.prefix
        elif nodeName_ == 'bulkShipment':
            obj_ = renderInstructionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.bulkShipment = obj_
            obj_.original_tagname_ = 'bulkShipment'
# end class consignmentRoutingLabelType


class renderInstructionsType(GeneratedsSuper):
    """These are attributes used to determine how and what is
    displayed for certain fields on the routing Label. This
    type contains the display string for the attribute."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, code=None, renderInstructions=None, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.code = _cast(None, code)
        self.code_nsprefix_ = None
        self.renderInstructions = _cast(None, renderInstructions)
        self.renderInstructions_nsprefix_ = None
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, renderInstructionsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if renderInstructionsType.subclass:
            return renderInstructionsType.subclass(*args_, **kwargs_)
        else:
            return renderInstructionsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_code(self):
        return self.code
    def set_code(self, code):
        self.code = code
    def get_renderInstructions(self):
        return self.renderInstructions
    def set_renderInstructions(self, renderInstructions):
        self.renderInstructions = renderInstructions
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def validate_renderInstructionsType1(self, value):
        # Validate type renderInstructionsType1, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['yes', 'no', 'highlighted']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on renderInstructionsType1' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
    def hasContent_(self):
        if (
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_)
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='renderInstructionsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('renderInstructionsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'renderInstructionsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='renderInstructionsType')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='renderInstructionsType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='renderInstructionsType'):
        if self.code is not None and 'code' not in already_processed:
            already_processed.add('code')
            outfile.write(' code=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.code), input_name='code')), ))
        if self.renderInstructions is not None and 'renderInstructions' not in already_processed:
            already_processed.add('renderInstructions')
            outfile.write(' renderInstructions=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.renderInstructions), input_name='renderInstructions')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='renderInstructionsType', fromsubclass_=False, pretty_print=True):
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
        value = find_attr_value_('code', node)
        if value is not None and 'code' not in already_processed:
            already_processed.add('code')
            self.code = value
        value = find_attr_value_('renderInstructions', node)
        if value is not None and 'renderInstructions' not in already_processed:
            already_processed.add('renderInstructions')
            self.renderInstructions = value
            self.validate_renderInstructionsType1(self.renderInstructions)    # validate type renderInstructionsType1
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class renderInstructionsType


class numericRenderInstructionsType(GeneratedsSuper):
    """These are attributes used to determine how and what is
    displayed for certain fields on the routing Label. This
    type contains the display string for the attribute."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, code=None, renderInstructions=None, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.code = _cast(None, code)
        self.code_nsprefix_ = None
        self.renderInstructions = _cast(None, renderInstructions)
        self.renderInstructions_nsprefix_ = None
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, numericRenderInstructionsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if numericRenderInstructionsType.subclass:
            return numericRenderInstructionsType.subclass(*args_, **kwargs_)
        else:
            return numericRenderInstructionsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_code(self):
        return self.code
    def set_code(self, code):
        self.code = code
    def get_renderInstructions(self):
        return self.renderInstructions
    def set_renderInstructions(self, renderInstructions):
        self.renderInstructions = renderInstructions
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def validate_renderInstructionsType1(self, value):
        # Validate type renderInstructionsType1, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['yes', 'no', 'highlighted']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on renderInstructionsType1' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
    def hasContent_(self):
        if (
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_)
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='numericRenderInstructionsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('numericRenderInstructionsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'numericRenderInstructionsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='numericRenderInstructionsType')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='numericRenderInstructionsType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='numericRenderInstructionsType'):
        if self.code is not None and 'code' not in already_processed:
            already_processed.add('code')
            outfile.write(' code=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.code), input_name='code')), ))
        if self.renderInstructions is not None and 'renderInstructions' not in already_processed:
            already_processed.add('renderInstructions')
            outfile.write(' renderInstructions=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.renderInstructions), input_name='renderInstructions')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='numericRenderInstructionsType', fromsubclass_=False, pretty_print=True):
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
        value = find_attr_value_('code', node)
        if value is not None and 'code' not in already_processed:
            already_processed.add('code')
            self.code = value
        value = find_attr_value_('renderInstructions', node)
        if value is not None and 'renderInstructions' not in already_processed:
            already_processed.add('renderInstructions')
            self.renderInstructions = value
            self.validate_renderInstructionsType1(self.renderInstructions)    # validate type renderInstructionsType1
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class numericRenderInstructionsType


class transitDepotListType(GeneratedsSuper):
    """The list of TNT depots that will be handling the consignment between
    the origin and destination depots.The list of TNT depots that will be
    handling the consignment between
    the origin and destination depots."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, transitDepot=None, actionDepot=None, sortDepot=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if transitDepot is None:
            self.transitDepot = []
        else:
            self.transitDepot = transitDepot
        self.transitDepot_nsprefix_ = None
        if actionDepot is None:
            self.actionDepot = []
        else:
            self.actionDepot = actionDepot
        self.actionDepot_nsprefix_ = None
        if sortDepot is None:
            self.sortDepot = []
        else:
            self.sortDepot = sortDepot
        self.sortDepot_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, transitDepotListType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if transitDepotListType.subclass:
            return transitDepotListType.subclass(*args_, **kwargs_)
        else:
            return transitDepotListType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_transitDepot(self):
        return self.transitDepot
    def set_transitDepot(self, transitDepot):
        self.transitDepot = transitDepot
    def add_transitDepot(self, value):
        self.transitDepot.append(value)
    def insert_transitDepot_at(self, index, value):
        self.transitDepot.insert(index, value)
    def replace_transitDepot_at(self, index, value):
        self.transitDepot[index] = value
    def get_actionDepot(self):
        return self.actionDepot
    def set_actionDepot(self, actionDepot):
        self.actionDepot = actionDepot
    def add_actionDepot(self, value):
        self.actionDepot.append(value)
    def insert_actionDepot_at(self, index, value):
        self.actionDepot.insert(index, value)
    def replace_actionDepot_at(self, index, value):
        self.actionDepot[index] = value
    def get_sortDepot(self):
        return self.sortDepot
    def set_sortDepot(self, sortDepot):
        self.sortDepot = sortDepot
    def add_sortDepot(self, value):
        self.sortDepot.append(value)
    def insert_sortDepot_at(self, index, value):
        self.sortDepot.insert(index, value)
    def replace_sortDepot_at(self, index, value):
        self.sortDepot[index] = value
    def hasContent_(self):
        if (
            self.transitDepot or
            self.actionDepot or
            self.sortDepot
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='transitDepotListType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('transitDepotListType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'transitDepotListType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='transitDepotListType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='transitDepotListType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='transitDepotListType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='transitDepotListType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for transitDepot_ in self.transitDepot:
            namespaceprefix_ = self.transitDepot_nsprefix_ + ':' if (UseCapturedNS_ and self.transitDepot_nsprefix_) else ''
            transitDepot_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='transitDepot', pretty_print=pretty_print)
        for actionDepot_ in self.actionDepot:
            namespaceprefix_ = self.actionDepot_nsprefix_ + ':' if (UseCapturedNS_ and self.actionDepot_nsprefix_) else ''
            actionDepot_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='actionDepot', pretty_print=pretty_print)
        for sortDepot_ in self.sortDepot:
            namespaceprefix_ = self.sortDepot_nsprefix_ + ':' if (UseCapturedNS_ and self.sortDepot_nsprefix_) else ''
            sortDepot_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='sortDepot', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'transitDepot':
            obj_ = depotType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.transitDepot.append(obj_)
            obj_.original_tagname_ = 'transitDepot'
        elif nodeName_ == 'actionDepot':
            obj_ = actionDepotType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.actionDepot.append(obj_)
            obj_.original_tagname_ = 'actionDepot'
        elif nodeName_ == 'sortDepot':
            obj_ = sortDepotType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.sortDepot.append(obj_)
            obj_.original_tagname_ = 'sortDepot'
# end class transitDepotListType


class actionDepotType(GeneratedsSuper):
    """Details relevant to an action transit TNT depot."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, depotCode=None, actionDayOfWeek=None, actionDate=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.depotCode = depotCode
        self.depotCode_nsprefix_ = None
        self.actionDayOfWeek = actionDayOfWeek
        self.actionDayOfWeek_nsprefix_ = None
        if isinstance(actionDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(actionDate, '%Y-%m-%d').date()
        else:
            initvalue_ = actionDate
        self.actionDate = initvalue_
        self.actionDate_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, actionDepotType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if actionDepotType.subclass:
            return actionDepotType.subclass(*args_, **kwargs_)
        else:
            return actionDepotType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_depotCode(self):
        return self.depotCode
    def set_depotCode(self, depotCode):
        self.depotCode = depotCode
    def get_actionDayOfWeek(self):
        return self.actionDayOfWeek
    def set_actionDayOfWeek(self, actionDayOfWeek):
        self.actionDayOfWeek = actionDayOfWeek
    def get_actionDate(self):
        return self.actionDate
    def set_actionDate(self, actionDate):
        self.actionDate = actionDate
    def hasContent_(self):
        if (
            self.depotCode is not None or
            self.actionDayOfWeek is not None or
            self.actionDate is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='actionDepotType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('actionDepotType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'actionDepotType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='actionDepotType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='actionDepotType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='actionDepotType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='actionDepotType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.depotCode is not None:
            namespaceprefix_ = self.depotCode_nsprefix_ + ':' if (UseCapturedNS_ and self.depotCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdepotCode>%s</%sdepotCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.depotCode), input_name='depotCode')), namespaceprefix_ , eol_))
        if self.actionDayOfWeek is not None:
            namespaceprefix_ = self.actionDayOfWeek_nsprefix_ + ':' if (UseCapturedNS_ and self.actionDayOfWeek_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sactionDayOfWeek>%s</%sactionDayOfWeek>%s' % (namespaceprefix_ , self.gds_format_integer(self.actionDayOfWeek, input_name='actionDayOfWeek'), namespaceprefix_ , eol_))
        if self.actionDate is not None:
            namespaceprefix_ = self.actionDate_nsprefix_ + ':' if (UseCapturedNS_ and self.actionDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sactionDate>%s</%sactionDate>%s' % (namespaceprefix_ , self.gds_format_date(self.actionDate, input_name='actionDate'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'depotCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'depotCode')
            value_ = self.gds_validate_string(value_, node, 'depotCode')
            self.depotCode = value_
            self.depotCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'actionDayOfWeek' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'actionDayOfWeek')
            ival_ = self.gds_validate_integer(ival_, node, 'actionDayOfWeek')
            self.actionDayOfWeek = ival_
            self.actionDayOfWeek_nsprefix_ = child_.prefix
        elif nodeName_ == 'actionDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.actionDate = dval_
            self.actionDate_nsprefix_ = child_.prefix
# end class actionDepotType


class sortDepotType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, depotCode=None, sortCellIndicator=None, sortLocationCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.depotCode = depotCode
        self.depotCode_nsprefix_ = None
        self.sortCellIndicator = sortCellIndicator
        self.sortCellIndicator_nsprefix_ = None
        self.sortLocationCode = sortLocationCode
        self.sortLocationCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, sortDepotType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if sortDepotType.subclass:
            return sortDepotType.subclass(*args_, **kwargs_)
        else:
            return sortDepotType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_depotCode(self):
        return self.depotCode
    def set_depotCode(self, depotCode):
        self.depotCode = depotCode
    def get_sortCellIndicator(self):
        return self.sortCellIndicator
    def set_sortCellIndicator(self, sortCellIndicator):
        self.sortCellIndicator = sortCellIndicator
    def get_sortLocationCode(self):
        return self.sortLocationCode
    def set_sortLocationCode(self, sortLocationCode):
        self.sortLocationCode = sortLocationCode
    def hasContent_(self):
        if (
            self.depotCode is not None or
            self.sortCellIndicator is not None or
            self.sortLocationCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='sortDepotType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('sortDepotType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'sortDepotType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='sortDepotType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='sortDepotType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='sortDepotType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='sortDepotType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.depotCode is not None:
            namespaceprefix_ = self.depotCode_nsprefix_ + ':' if (UseCapturedNS_ and self.depotCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdepotCode>%s</%sdepotCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.depotCode), input_name='depotCode')), namespaceprefix_ , eol_))
        if self.sortCellIndicator is not None:
            namespaceprefix_ = self.sortCellIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.sortCellIndicator_nsprefix_) else ''
            self.sortCellIndicator.export(outfile, level, namespaceprefix_, namespacedef_='', name_='sortCellIndicator', pretty_print=pretty_print)
        if self.sortLocationCode is not None:
            namespaceprefix_ = self.sortLocationCode_nsprefix_ + ':' if (UseCapturedNS_ and self.sortLocationCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssortLocationCode>%s</%ssortLocationCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.sortLocationCode), input_name='sortLocationCode')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'depotCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'depotCode')
            value_ = self.gds_validate_string(value_, node, 'depotCode')
            self.depotCode = value_
            self.depotCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'sortCellIndicator':
            obj_ = renderInstructionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.sortCellIndicator = obj_
            obj_.original_tagname_ = 'sortCellIndicator'
        elif nodeName_ == 'sortLocationCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'sortLocationCode')
            value_ = self.gds_validate_string(value_, node, 'sortLocationCode')
            self.sortLocationCode = value_
            self.sortLocationCode_nsprefix_ = child_.prefix
# end class sortDepotType


class barcodeType(GeneratedsSuper):
    """This contains the information relating to the barcode to be printed on
    the
    label.This contains the data to be printed as a barcode on the label.This
    denotes the symbology to be used to render the barcode,
    e.g. '128C' French domestic labels use '2of5Int' and '128B' for the
    customer reference barcode."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, symbology=None, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.symbology = _cast(None, symbology)
        self.symbology_nsprefix_ = None
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, barcodeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if barcodeType.subclass:
            return barcodeType.subclass(*args_, **kwargs_)
        else:
            return barcodeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_symbology(self):
        return self.symbology
    def set_symbology(self, symbology):
        self.symbology = symbology
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def validate_symbologyType(self, value):
        # Validate type symbologyType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['128B', '128C', '2of5Int']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on symbologyType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
    def hasContent_(self):
        if (
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_)
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='barcodeType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('barcodeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'barcodeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='barcodeType')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='barcodeType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='barcodeType'):
        if self.symbology is not None and 'symbology' not in already_processed:
            already_processed.add('symbology')
            outfile.write(' symbology=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.symbology), input_name='symbology')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='barcodeType', fromsubclass_=False, pretty_print=True):
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
        value = find_attr_value_('symbology', node)
        if value is not None and 'symbology' not in already_processed:
            already_processed.add('symbology')
            self.symbology = value
            self.validate_symbologyType(self.symbology)    # validate type symbologyType
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class barcodeType


class twoDBarcodeType(GeneratedsSuper):
    """This contains the information relating to the 2D barcode to be printed
    on the
    label.This contains the data to be printed as a barcode on the label.This
    denotes the symbology to be used to render the barcode,
    e.g. 'pdf417'."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, symbology=None, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.symbology = _cast(None, symbology)
        self.symbology_nsprefix_ = None
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, twoDBarcodeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if twoDBarcodeType.subclass:
            return twoDBarcodeType.subclass(*args_, **kwargs_)
        else:
            return twoDBarcodeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_symbology(self):
        return self.symbology
    def set_symbology(self, symbology):
        self.symbology = symbology
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def validate_symbologyType2(self, value):
        # Validate type symbologyType2, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['pdf417']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on symbologyType2' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
    def hasContent_(self):
        if (
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_)
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='twoDBarcodeType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('twoDBarcodeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'twoDBarcodeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='twoDBarcodeType')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='twoDBarcodeType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='twoDBarcodeType'):
        if self.symbology is not None and 'symbology' not in already_processed:
            already_processed.add('symbology')
            outfile.write(' symbology=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.symbology), input_name='symbology')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='twoDBarcodeType', fromsubclass_=False, pretty_print=True):
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
        value = find_attr_value_('symbology', node)
        if value is not None and 'symbology' not in already_processed:
            already_processed.add('symbology')
            self.symbology = value
            self.validate_symbologyType2(self.symbology)    # validate type symbologyType2
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class twoDBarcodeType


class productDescriptionType(GeneratedsSuper):
    """This contains the information relating to the product to be printed on
    the
    label.This contains the description of the product to be printed on the
    label.This denotes the product id"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, id=None, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.id = _cast(None, id)
        self.id_nsprefix_ = None
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, productDescriptionType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if productDescriptionType.subclass:
            return productDescriptionType.subclass(*args_, **kwargs_)
        else:
            return productDescriptionType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_id(self):
        return self.id
    def set_id(self, id):
        self.id = id
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def hasContent_(self):
        if (
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_)
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='productDescriptionType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('productDescriptionType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'productDescriptionType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='productDescriptionType')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='productDescriptionType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='productDescriptionType'):
        if self.id is not None and 'id' not in already_processed:
            already_processed.add('id')
            outfile.write(' id=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.id), input_name='id')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='productDescriptionType', fromsubclass_=False, pretty_print=True):
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
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self.id = value
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class productDescriptionType


class optionDescriptionType(GeneratedsSuper):
    """This contains the information relating to the options to be printed on
    the
    label.This contains the description of the option to be printed on the
    label.This denotes the option id"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, id=None, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.id = _cast(None, id)
        self.id_nsprefix_ = None
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, optionDescriptionType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if optionDescriptionType.subclass:
            return optionDescriptionType.subclass(*args_, **kwargs_)
        else:
            return optionDescriptionType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_id(self):
        return self.id
    def set_id(self, id):
        self.id = id
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def hasContent_(self):
        if (
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_)
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='optionDescriptionType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('optionDescriptionType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'optionDescriptionType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='optionDescriptionType')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='optionDescriptionType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='optionDescriptionType'):
        if self.id is not None and 'id' not in already_processed:
            already_processed.add('id')
            outfile.write(' id=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.id), input_name='id')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='optionDescriptionType', fromsubclass_=False, pretty_print=True):
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
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self.id = value
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class optionDescriptionType


class consignmentIdentityType(GeneratedsSuper):
    """This element contains a consignment number and optional customer
    reference.
    These values are used to distinguish a consignment from any other
    consignment.
    This value appears on a routing label and is used as the key for a
    consignment."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, consignmentNumber=None, customerReference=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.consignmentNumber = consignmentNumber
        self.consignmentNumber_nsprefix_ = None
        self.customerReference = customerReference
        self.customerReference_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, consignmentIdentityType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if consignmentIdentityType.subclass:
            return consignmentIdentityType.subclass(*args_, **kwargs_)
        else:
            return consignmentIdentityType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_consignmentNumber(self):
        return self.consignmentNumber
    def set_consignmentNumber(self, consignmentNumber):
        self.consignmentNumber = consignmentNumber
    def get_customerReference(self):
        return self.customerReference
    def set_customerReference(self, customerReference):
        self.customerReference = customerReference
    def hasContent_(self):
        if (
            self.consignmentNumber is not None or
            self.customerReference is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='consignmentIdentityType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('consignmentIdentityType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'consignmentIdentityType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='consignmentIdentityType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='consignmentIdentityType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='consignmentIdentityType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='consignmentIdentityType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.consignmentNumber is not None:
            namespaceprefix_ = self.consignmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.consignmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sconsignmentNumber>%s</%sconsignmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.consignmentNumber), input_name='consignmentNumber')), namespaceprefix_ , eol_))
        if self.customerReference is not None:
            namespaceprefix_ = self.customerReference_nsprefix_ + ':' if (UseCapturedNS_ and self.customerReference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scustomerReference>%s</%scustomerReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.customerReference), input_name='customerReference')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'consignmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'consignmentNumber')
            value_ = self.gds_validate_string(value_, node, 'consignmentNumber')
            self.consignmentNumber = value_
            self.consignmentNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'customerReference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'customerReference')
            value_ = self.gds_validate_string(value_, node, 'customerReference')
            self.customerReference = value_
            self.customerReference_nsprefix_ = child_.prefix
# end class consignmentIdentityType


class nameAndAddressRequestType(GeneratedsSuper):
    """Information relating to name and address for a participant
    in the consignment.
    Examples of a participant are:
    The Sender - the company sending the consignment
    The Receiver - the company receiving the consignment
    The Collection Address - the address from which the consignment is picked
    up
    The Delivery Address - the address to which the consignment should be
    delivered"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, name=None, addressLine1=None, addressLine2=None, addressLine3=None, town=None, exactMatch='Y', province=None, postcode=None, country=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name = name
        self.validate_stringMaxLength40(self.name)
        self.name_nsprefix_ = None
        self.addressLine1 = addressLine1
        self.validate_stringMaxLength30(self.addressLine1)
        self.addressLine1_nsprefix_ = None
        self.addressLine2 = addressLine2
        self.validate_stringMaxLength30(self.addressLine2)
        self.addressLine2_nsprefix_ = None
        self.addressLine3 = addressLine3
        self.validate_stringMaxLength30(self.addressLine3)
        self.addressLine3_nsprefix_ = None
        self.town = town
        self.validate_stringMaxLength40(self.town)
        self.town_nsprefix_ = None
        self.exactMatch = exactMatch
        self.validate_booleanEnum(self.exactMatch)
        self.exactMatch_nsprefix_ = None
        self.province = province
        self.validate_stringMaxLength30(self.province)
        self.province_nsprefix_ = None
        self.postcode = postcode
        self.validate_stringMaxLength9(self.postcode)
        self.postcode_nsprefix_ = None
        self.country = country
        self.validate_stringMinLength2MaxLength2(self.country)
        self.country_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, nameAndAddressRequestType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if nameAndAddressRequestType.subclass:
            return nameAndAddressRequestType.subclass(*args_, **kwargs_)
        else:
            return nameAndAddressRequestType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_addressLine1(self):
        return self.addressLine1
    def set_addressLine1(self, addressLine1):
        self.addressLine1 = addressLine1
    def get_addressLine2(self):
        return self.addressLine2
    def set_addressLine2(self, addressLine2):
        self.addressLine2 = addressLine2
    def get_addressLine3(self):
        return self.addressLine3
    def set_addressLine3(self, addressLine3):
        self.addressLine3 = addressLine3
    def get_town(self):
        return self.town
    def set_town(self, town):
        self.town = town
    def get_exactMatch(self):
        return self.exactMatch
    def set_exactMatch(self, exactMatch):
        self.exactMatch = exactMatch
    def get_province(self):
        return self.province
    def set_province(self, province):
        self.province = province
    def get_postcode(self):
        return self.postcode
    def set_postcode(self, postcode):
        self.postcode = postcode
    def get_country(self):
        return self.country
    def set_country(self, country):
        self.country = country
    def validate_stringMaxLength40(self, value):
        result = True
        # Validate type stringMaxLength40, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stringMaxLength40' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_stringMaxLength30(self, value):
        result = True
        # Validate type stringMaxLength30, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 30:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stringMaxLength30' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_booleanEnum(self, value):
        result = True
        # Validate type booleanEnum, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['N', 'Y']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on booleanEnum' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_stringMaxLength9(self, value):
        result = True
        # Validate type stringMaxLength9, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 9:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stringMaxLength9' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_stringMinLength2MaxLength2(self, value):
        result = True
        # Validate type stringMinLength2MaxLength2, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stringMinLength2MaxLength2' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on stringMinLength2MaxLength2' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.name is not None or
            self.addressLine1 is not None or
            self.addressLine2 is not None or
            self.addressLine3 is not None or
            self.town is not None or
            self.exactMatch != "Y" or
            self.province is not None or
            self.postcode is not None or
            self.country is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='nameAndAddressRequestType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('nameAndAddressRequestType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'nameAndAddressRequestType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='nameAndAddressRequestType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='nameAndAddressRequestType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='nameAndAddressRequestType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='nameAndAddressRequestType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.name is not None:
            namespaceprefix_ = self.name_nsprefix_ + ':' if (UseCapturedNS_ and self.name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sname>%s</%sname>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.name), input_name='name')), namespaceprefix_ , eol_))
        if self.addressLine1 is not None:
            namespaceprefix_ = self.addressLine1_nsprefix_ + ':' if (UseCapturedNS_ and self.addressLine1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saddressLine1>%s</%saddressLine1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.addressLine1), input_name='addressLine1')), namespaceprefix_ , eol_))
        if self.addressLine2 is not None:
            namespaceprefix_ = self.addressLine2_nsprefix_ + ':' if (UseCapturedNS_ and self.addressLine2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saddressLine2>%s</%saddressLine2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.addressLine2), input_name='addressLine2')), namespaceprefix_ , eol_))
        if self.addressLine3 is not None:
            namespaceprefix_ = self.addressLine3_nsprefix_ + ':' if (UseCapturedNS_ and self.addressLine3_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saddressLine3>%s</%saddressLine3>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.addressLine3), input_name='addressLine3')), namespaceprefix_ , eol_))
        if self.town is not None:
            namespaceprefix_ = self.town_nsprefix_ + ':' if (UseCapturedNS_ and self.town_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stown>%s</%stown>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.town), input_name='town')), namespaceprefix_ , eol_))
        if self.exactMatch != "Y":
            namespaceprefix_ = self.exactMatch_nsprefix_ + ':' if (UseCapturedNS_ and self.exactMatch_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sexactMatch>%s</%sexactMatch>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.exactMatch), input_name='exactMatch')), namespaceprefix_ , eol_))
        if self.province is not None:
            namespaceprefix_ = self.province_nsprefix_ + ':' if (UseCapturedNS_ and self.province_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sprovince>%s</%sprovince>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.province), input_name='province')), namespaceprefix_ , eol_))
        if self.postcode is not None:
            namespaceprefix_ = self.postcode_nsprefix_ + ':' if (UseCapturedNS_ and self.postcode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spostcode>%s</%spostcode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.postcode), input_name='postcode')), namespaceprefix_ , eol_))
        if self.country is not None:
            namespaceprefix_ = self.country_nsprefix_ + ':' if (UseCapturedNS_ and self.country_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scountry>%s</%scountry>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.country), input_name='country')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'name')
            value_ = self.gds_validate_string(value_, node, 'name')
            self.name = value_
            self.name_nsprefix_ = child_.prefix
            # validate type stringMaxLength40
            self.validate_stringMaxLength40(self.name)
        elif nodeName_ == 'addressLine1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'addressLine1')
            value_ = self.gds_validate_string(value_, node, 'addressLine1')
            self.addressLine1 = value_
            self.addressLine1_nsprefix_ = child_.prefix
            # validate type stringMaxLength30
            self.validate_stringMaxLength30(self.addressLine1)
        elif nodeName_ == 'addressLine2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'addressLine2')
            value_ = self.gds_validate_string(value_, node, 'addressLine2')
            self.addressLine2 = value_
            self.addressLine2_nsprefix_ = child_.prefix
            # validate type stringMaxLength30
            self.validate_stringMaxLength30(self.addressLine2)
        elif nodeName_ == 'addressLine3':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'addressLine3')
            value_ = self.gds_validate_string(value_, node, 'addressLine3')
            self.addressLine3 = value_
            self.addressLine3_nsprefix_ = child_.prefix
            # validate type stringMaxLength30
            self.validate_stringMaxLength30(self.addressLine3)
        elif nodeName_ == 'town':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'town')
            value_ = self.gds_validate_string(value_, node, 'town')
            self.town = value_
            self.town_nsprefix_ = child_.prefix
            # validate type stringMaxLength40
            self.validate_stringMaxLength40(self.town)
        elif nodeName_ == 'exactMatch':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'exactMatch')
            value_ = self.gds_validate_string(value_, node, 'exactMatch')
            self.exactMatch = value_
            self.exactMatch_nsprefix_ = child_.prefix
            # validate type booleanEnum
            self.validate_booleanEnum(self.exactMatch)
        elif nodeName_ == 'province':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'province')
            value_ = self.gds_validate_string(value_, node, 'province')
            self.province = value_
            self.province_nsprefix_ = child_.prefix
            # validate type stringMaxLength30
            self.validate_stringMaxLength30(self.province)
        elif nodeName_ == 'postcode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'postcode')
            value_ = self.gds_validate_string(value_, node, 'postcode')
            self.postcode = value_
            self.postcode_nsprefix_ = child_.prefix
            # validate type stringMaxLength9
            self.validate_stringMaxLength9(self.postcode)
        elif nodeName_ == 'country':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'country')
            value_ = self.gds_validate_string(value_, node, 'country')
            self.country = value_
            self.country_nsprefix_ = child_.prefix
            # validate type stringMinLength2MaxLength2
            self.validate_stringMinLength2MaxLength2(self.country)
# end class nameAndAddressRequestType


class nameAndAddressResponseType(GeneratedsSuper):
    """Information relating to name and address for a participant
    in the consignment.
    Examples of a participant are:
    The Sender - the company sending the consignment
    The Receiver - the company receiving the consignment
    The Collection Address - the address from which the consignment is picked
    up
    The Delivery Address - the address to which the consignment should be
    delivered"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, name=None, addressLine1=None, addressLine2=None, addressLine3=None, town=None, province=None, postcode=None, country=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name = name
        self.validate_stringMaxLength40(self.name)
        self.name_nsprefix_ = None
        self.addressLine1 = addressLine1
        self.validate_stringMaxLength30(self.addressLine1)
        self.addressLine1_nsprefix_ = None
        self.addressLine2 = addressLine2
        self.validate_stringMaxLength30(self.addressLine2)
        self.addressLine2_nsprefix_ = None
        self.addressLine3 = addressLine3
        self.validate_stringMaxLength30(self.addressLine3)
        self.addressLine3_nsprefix_ = None
        self.town = town
        self.validate_stringMaxLength40(self.town)
        self.town_nsprefix_ = None
        self.province = province
        self.validate_stringMaxLength30(self.province)
        self.province_nsprefix_ = None
        self.postcode = postcode
        self.validate_stringMaxLength9(self.postcode)
        self.postcode_nsprefix_ = None
        self.country = country
        self.validate_stringMinLength2MaxLength2(self.country)
        self.country_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, nameAndAddressResponseType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if nameAndAddressResponseType.subclass:
            return nameAndAddressResponseType.subclass(*args_, **kwargs_)
        else:
            return nameAndAddressResponseType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_addressLine1(self):
        return self.addressLine1
    def set_addressLine1(self, addressLine1):
        self.addressLine1 = addressLine1
    def get_addressLine2(self):
        return self.addressLine2
    def set_addressLine2(self, addressLine2):
        self.addressLine2 = addressLine2
    def get_addressLine3(self):
        return self.addressLine3
    def set_addressLine3(self, addressLine3):
        self.addressLine3 = addressLine3
    def get_town(self):
        return self.town
    def set_town(self, town):
        self.town = town
    def get_province(self):
        return self.province
    def set_province(self, province):
        self.province = province
    def get_postcode(self):
        return self.postcode
    def set_postcode(self, postcode):
        self.postcode = postcode
    def get_country(self):
        return self.country
    def set_country(self, country):
        self.country = country
    def validate_stringMaxLength40(self, value):
        result = True
        # Validate type stringMaxLength40, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stringMaxLength40' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_stringMaxLength30(self, value):
        result = True
        # Validate type stringMaxLength30, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 30:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stringMaxLength30' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_stringMaxLength9(self, value):
        result = True
        # Validate type stringMaxLength9, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 9:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stringMaxLength9' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_stringMinLength2MaxLength2(self, value):
        result = True
        # Validate type stringMinLength2MaxLength2, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stringMinLength2MaxLength2' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on stringMinLength2MaxLength2' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.name is not None or
            self.addressLine1 is not None or
            self.addressLine2 is not None or
            self.addressLine3 is not None or
            self.town is not None or
            self.province is not None or
            self.postcode is not None or
            self.country is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='nameAndAddressResponseType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('nameAndAddressResponseType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'nameAndAddressResponseType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='nameAndAddressResponseType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='nameAndAddressResponseType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='nameAndAddressResponseType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='nameAndAddressResponseType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.name is not None:
            namespaceprefix_ = self.name_nsprefix_ + ':' if (UseCapturedNS_ and self.name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sname>%s</%sname>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.name), input_name='name')), namespaceprefix_ , eol_))
        if self.addressLine1 is not None:
            namespaceprefix_ = self.addressLine1_nsprefix_ + ':' if (UseCapturedNS_ and self.addressLine1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saddressLine1>%s</%saddressLine1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.addressLine1), input_name='addressLine1')), namespaceprefix_ , eol_))
        if self.addressLine2 is not None:
            namespaceprefix_ = self.addressLine2_nsprefix_ + ':' if (UseCapturedNS_ and self.addressLine2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saddressLine2>%s</%saddressLine2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.addressLine2), input_name='addressLine2')), namespaceprefix_ , eol_))
        if self.addressLine3 is not None:
            namespaceprefix_ = self.addressLine3_nsprefix_ + ':' if (UseCapturedNS_ and self.addressLine3_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saddressLine3>%s</%saddressLine3>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.addressLine3), input_name='addressLine3')), namespaceprefix_ , eol_))
        if self.town is not None:
            namespaceprefix_ = self.town_nsprefix_ + ':' if (UseCapturedNS_ and self.town_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stown>%s</%stown>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.town), input_name='town')), namespaceprefix_ , eol_))
        if self.province is not None:
            namespaceprefix_ = self.province_nsprefix_ + ':' if (UseCapturedNS_ and self.province_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sprovince>%s</%sprovince>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.province), input_name='province')), namespaceprefix_ , eol_))
        if self.postcode is not None:
            namespaceprefix_ = self.postcode_nsprefix_ + ':' if (UseCapturedNS_ and self.postcode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spostcode>%s</%spostcode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.postcode), input_name='postcode')), namespaceprefix_ , eol_))
        if self.country is not None:
            namespaceprefix_ = self.country_nsprefix_ + ':' if (UseCapturedNS_ and self.country_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scountry>%s</%scountry>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.country), input_name='country')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'name')
            value_ = self.gds_validate_string(value_, node, 'name')
            self.name = value_
            self.name_nsprefix_ = child_.prefix
            # validate type stringMaxLength40
            self.validate_stringMaxLength40(self.name)
        elif nodeName_ == 'addressLine1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'addressLine1')
            value_ = self.gds_validate_string(value_, node, 'addressLine1')
            self.addressLine1 = value_
            self.addressLine1_nsprefix_ = child_.prefix
            # validate type stringMaxLength30
            self.validate_stringMaxLength30(self.addressLine1)
        elif nodeName_ == 'addressLine2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'addressLine2')
            value_ = self.gds_validate_string(value_, node, 'addressLine2')
            self.addressLine2 = value_
            self.addressLine2_nsprefix_ = child_.prefix
            # validate type stringMaxLength30
            self.validate_stringMaxLength30(self.addressLine2)
        elif nodeName_ == 'addressLine3':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'addressLine3')
            value_ = self.gds_validate_string(value_, node, 'addressLine3')
            self.addressLine3 = value_
            self.addressLine3_nsprefix_ = child_.prefix
            # validate type stringMaxLength30
            self.validate_stringMaxLength30(self.addressLine3)
        elif nodeName_ == 'town':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'town')
            value_ = self.gds_validate_string(value_, node, 'town')
            self.town = value_
            self.town_nsprefix_ = child_.prefix
            # validate type stringMaxLength40
            self.validate_stringMaxLength40(self.town)
        elif nodeName_ == 'province':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'province')
            value_ = self.gds_validate_string(value_, node, 'province')
            self.province = value_
            self.province_nsprefix_ = child_.prefix
            # validate type stringMaxLength30
            self.validate_stringMaxLength30(self.province)
        elif nodeName_ == 'postcode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'postcode')
            value_ = self.gds_validate_string(value_, node, 'postcode')
            self.postcode = value_
            self.postcode_nsprefix_ = child_.prefix
            # validate type stringMaxLength9
            self.validate_stringMaxLength9(self.postcode)
        elif nodeName_ == 'country':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'country')
            value_ = self.gds_validate_string(value_, node, 'country')
            self.country = value_
            self.country_nsprefix_ = child_.prefix
            # validate type stringMinLength2MaxLength2
            self.validate_stringMinLength2MaxLength2(self.country)
# end class nameAndAddressResponseType


class optionType(GeneratedsSuper):
    """The type of option chosen for this consignment.
    Examples include insurance, priority."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, optionId=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if optionId is None:
            self.optionId = []
        else:
            self.optionId = optionId
        self.optionId_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, optionType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if optionType.subclass:
            return optionType.subclass(*args_, **kwargs_)
        else:
            return optionType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_optionId(self):
        return self.optionId
    def set_optionId(self, optionId):
        self.optionId = optionId
    def add_optionId(self, value):
        self.optionId.append(value)
    def insert_optionId_at(self, index, value):
        self.optionId.insert(index, value)
    def replace_optionId_at(self, index, value):
        self.optionId[index] = value
    def hasContent_(self):
        if (
            self.optionId
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='optionType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('optionType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'optionType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='optionType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='optionType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='optionType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='optionType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for optionId_ in self.optionId:
            namespaceprefix_ = self.optionId_nsprefix_ + ':' if (UseCapturedNS_ and self.optionId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%soptionId>%s</%soptionId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(optionId_), input_name='optionId')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'optionId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'optionId')
            value_ = self.gds_validate_string(value_, node, 'optionId')
            self.optionId.append(value_)
            self.optionId_nsprefix_ = child_.prefix
# end class optionType


class measurementsType(GeneratedsSuper):
    """The dimensions (height, width, length) and weight of the consignment,
    piece or article. Data must be provided in metres for dimensions,
    kilograms for weight."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, length=None, width=None, height=None, weight=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.length = length
        self.validate_doubleMaxExclusive100MinInclusive0_01(self.length)
        self.length_nsprefix_ = None
        self.width = width
        self.validate_doubleMaxExclusive100MinInclusive0_01(self.width)
        self.width_nsprefix_ = None
        self.height = height
        self.validate_doubleMaxExclusive100MinInclusive0_01(self.height)
        self.height_nsprefix_ = None
        self.weight = weight
        self.validate_doubleMaxExclusive100000MinInclusive0_01(self.weight)
        self.weight_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, measurementsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if measurementsType.subclass:
            return measurementsType.subclass(*args_, **kwargs_)
        else:
            return measurementsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_length(self):
        return self.length
    def set_length(self, length):
        self.length = length
    def get_width(self):
        return self.width
    def set_width(self, width):
        self.width = width
    def get_height(self):
        return self.height
    def set_height(self, height):
        self.height = height
    def get_weight(self):
        return self.weight
    def set_weight(self, weight):
        self.weight = weight
    def validate_doubleMaxExclusive100MinInclusive0_01(self, value):
        result = True
        # Validate type doubleMaxExclusive100MinInclusive0.01, a restriction on xsd:double.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, float):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (float)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0.01:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on doubleMaxExclusive100MinInclusive0.01' % {"value": value, "lineno": lineno} )
                result = False
            if value >= 100:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxExclusive restriction on doubleMaxExclusive100MinInclusive0.01' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_doubleMaxExclusive100000MinInclusive0_01(self, value):
        result = True
        # Validate type doubleMaxExclusive100000MinInclusive0.01, a restriction on xsd:double.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, float):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (float)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0.01:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on doubleMaxExclusive100000MinInclusive0.01' % {"value": value, "lineno": lineno} )
                result = False
            if value >= 100000:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxExclusive restriction on doubleMaxExclusive100000MinInclusive0.01' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.length is not None or
            self.width is not None or
            self.height is not None or
            self.weight is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='measurementsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('measurementsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'measurementsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='measurementsType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='measurementsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='measurementsType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='measurementsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.length is not None:
            namespaceprefix_ = self.length_nsprefix_ + ':' if (UseCapturedNS_ and self.length_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slength>%s</%slength>%s' % (namespaceprefix_ , self.gds_format_double(self.length, input_name='length'), namespaceprefix_ , eol_))
        if self.width is not None:
            namespaceprefix_ = self.width_nsprefix_ + ':' if (UseCapturedNS_ and self.width_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%swidth>%s</%swidth>%s' % (namespaceprefix_ , self.gds_format_double(self.width, input_name='width'), namespaceprefix_ , eol_))
        if self.height is not None:
            namespaceprefix_ = self.height_nsprefix_ + ':' if (UseCapturedNS_ and self.height_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sheight>%s</%sheight>%s' % (namespaceprefix_ , self.gds_format_double(self.height, input_name='height'), namespaceprefix_ , eol_))
        if self.weight is not None:
            namespaceprefix_ = self.weight_nsprefix_ + ':' if (UseCapturedNS_ and self.weight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sweight>%s</%sweight>%s' % (namespaceprefix_ , self.gds_format_double(self.weight, input_name='weight'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'length' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'length')
            fval_ = self.gds_validate_double(fval_, node, 'length')
            self.length = fval_
            self.length_nsprefix_ = child_.prefix
            # validate type doubleMaxExclusive100MinInclusive0.01
            self.validate_doubleMaxExclusive100MinInclusive0_01(self.length)
        elif nodeName_ == 'width' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'width')
            fval_ = self.gds_validate_double(fval_, node, 'width')
            self.width = fval_
            self.width_nsprefix_ = child_.prefix
            # validate type doubleMaxExclusive100MinInclusive0.01
            self.validate_doubleMaxExclusive100MinInclusive0_01(self.width)
        elif nodeName_ == 'height' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'height')
            fval_ = self.gds_validate_double(fval_, node, 'height')
            self.height = fval_
            self.height_nsprefix_ = child_.prefix
            # validate type doubleMaxExclusive100MinInclusive0.01
            self.validate_doubleMaxExclusive100MinInclusive0_01(self.height)
        elif nodeName_ == 'weight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'weight')
            fval_ = self.gds_validate_double(fval_, node, 'weight')
            self.weight = fval_
            self.weight_nsprefix_ = child_.prefix
            # validate type doubleMaxExclusive100000MinInclusive0.01
            self.validate_doubleMaxExclusive100000MinInclusive0_01(self.weight)
# end class measurementsType


class pieceLineType(GeneratedsSuper):
    """A piece line describes a kind of piece sharing the same physical
    attributes.
    (A piece is a package, box, envelope or shippable unit. All pieces which
    are
    identical are defined for convenience as a piece line with a number of
    units.)
    For example if there are 5 boxes of 0.1m x 0.2m x 0.3m of weight 0.1kg and
    1 box of 0.4m x 0.4m x 0.4 of weight 0.5kg this equates to two piece lines
    as
    follows:
    PieceLine1: 0.1m x 0.2m x 0.3m, weight 0.1kg, number of units=5
    PieceLine2: 0.4m x 0.4m x 0.4m, weight 0.5kg, number of units=1"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, identifier=None, goodsDescription=None, barcodeForCustomer=None, pieceMeasurements=None, pieces=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.identifier = identifier
        self.identifier_nsprefix_ = None
        self.goodsDescription = goodsDescription
        self.validate_stringMaxLength30(self.goodsDescription)
        self.goodsDescription_nsprefix_ = None
        self.barcodeForCustomer = barcodeForCustomer
        self.validate_booleanEnum(self.barcodeForCustomer)
        self.barcodeForCustomer_nsprefix_ = None
        self.pieceMeasurements = pieceMeasurements
        self.pieceMeasurements_nsprefix_ = None
        if pieces is None:
            self.pieces = []
        else:
            self.pieces = pieces
        self.pieces_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, pieceLineType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if pieceLineType.subclass:
            return pieceLineType.subclass(*args_, **kwargs_)
        else:
            return pieceLineType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_identifier(self):
        return self.identifier
    def set_identifier(self, identifier):
        self.identifier = identifier
    def get_goodsDescription(self):
        return self.goodsDescription
    def set_goodsDescription(self, goodsDescription):
        self.goodsDescription = goodsDescription
    def get_barcodeForCustomer(self):
        return self.barcodeForCustomer
    def set_barcodeForCustomer(self, barcodeForCustomer):
        self.barcodeForCustomer = barcodeForCustomer
    def get_pieceMeasurements(self):
        return self.pieceMeasurements
    def set_pieceMeasurements(self, pieceMeasurements):
        self.pieceMeasurements = pieceMeasurements
    def get_pieces(self):
        return self.pieces
    def set_pieces(self, pieces):
        self.pieces = pieces
    def add_pieces(self, value):
        self.pieces.append(value)
    def insert_pieces_at(self, index, value):
        self.pieces.insert(index, value)
    def replace_pieces_at(self, index, value):
        self.pieces[index] = value
    def validate_stringMaxLength30(self, value):
        result = True
        # Validate type stringMaxLength30, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 30:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stringMaxLength30' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_booleanEnum(self, value):
        result = True
        # Validate type booleanEnum, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['N', 'Y']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on booleanEnum' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.identifier is not None or
            self.goodsDescription is not None or
            self.barcodeForCustomer is not None or
            self.pieceMeasurements is not None or
            self.pieces
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='pieceLineType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('pieceLineType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'pieceLineType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='pieceLineType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='pieceLineType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='pieceLineType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='pieceLineType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.identifier is not None:
            namespaceprefix_ = self.identifier_nsprefix_ + ':' if (UseCapturedNS_ and self.identifier_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sidentifier>%s</%sidentifier>%s' % (namespaceprefix_ , self.gds_format_integer(self.identifier, input_name='identifier'), namespaceprefix_ , eol_))
        if self.goodsDescription is not None:
            namespaceprefix_ = self.goodsDescription_nsprefix_ + ':' if (UseCapturedNS_ and self.goodsDescription_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sgoodsDescription>%s</%sgoodsDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.goodsDescription), input_name='goodsDescription')), namespaceprefix_ , eol_))
        if self.barcodeForCustomer is not None:
            namespaceprefix_ = self.barcodeForCustomer_nsprefix_ + ':' if (UseCapturedNS_ and self.barcodeForCustomer_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sbarcodeForCustomer>%s</%sbarcodeForCustomer>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.barcodeForCustomer), input_name='barcodeForCustomer')), namespaceprefix_ , eol_))
        if self.pieceMeasurements is not None:
            namespaceprefix_ = self.pieceMeasurements_nsprefix_ + ':' if (UseCapturedNS_ and self.pieceMeasurements_nsprefix_) else ''
            self.pieceMeasurements.export(outfile, level, namespaceprefix_, namespacedef_='', name_='pieceMeasurements', pretty_print=pretty_print)
        for pieces_ in self.pieces:
            namespaceprefix_ = self.pieces_nsprefix_ + ':' if (UseCapturedNS_ and self.pieces_nsprefix_) else ''
            pieces_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='pieces', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'identifier' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'identifier')
            ival_ = self.gds_validate_integer(ival_, node, 'identifier')
            self.identifier = ival_
            self.identifier_nsprefix_ = child_.prefix
        elif nodeName_ == 'goodsDescription':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'goodsDescription')
            value_ = self.gds_validate_string(value_, node, 'goodsDescription')
            self.goodsDescription = value_
            self.goodsDescription_nsprefix_ = child_.prefix
            # validate type stringMaxLength30
            self.validate_stringMaxLength30(self.goodsDescription)
        elif nodeName_ == 'barcodeForCustomer':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'barcodeForCustomer')
            value_ = self.gds_validate_string(value_, node, 'barcodeForCustomer')
            self.barcodeForCustomer = value_
            self.barcodeForCustomer_nsprefix_ = child_.prefix
            # validate type booleanEnum
            self.validate_booleanEnum(self.barcodeForCustomer)
        elif nodeName_ == 'pieceMeasurements':
            obj_ = measurementsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.pieceMeasurements = obj_
            obj_.original_tagname_ = 'pieceMeasurements'
        elif nodeName_ == 'pieces':
            obj_ = pieceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.pieces.append(obj_)
            obj_.original_tagname_ = 'pieces'
# end class pieceLineType


class pieceType(GeneratedsSuper):
    """This element is used to identify all the pieces that should be grouped
    together by the given reference. The list of sequence numbers is included
    (one sequenceNumber element per piece) with a single pieceReference
    element."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, sequenceNumbers=None, pieceReference=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.sequenceNumbers = sequenceNumbers
        self.sequenceNumbers_nsprefix_ = None
        self.pieceReference = pieceReference
        self.pieceReference_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, pieceType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if pieceType.subclass:
            return pieceType.subclass(*args_, **kwargs_)
        else:
            return pieceType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_sequenceNumbers(self):
        return self.sequenceNumbers
    def set_sequenceNumbers(self, sequenceNumbers):
        self.sequenceNumbers = sequenceNumbers
    def get_pieceReference(self):
        return self.pieceReference
    def set_pieceReference(self, pieceReference):
        self.pieceReference = pieceReference
    def hasContent_(self):
        if (
            self.sequenceNumbers is not None or
            self.pieceReference is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='pieceType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('pieceType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'pieceType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='pieceType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='pieceType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='pieceType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='pieceType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.sequenceNumbers is not None:
            namespaceprefix_ = self.sequenceNumbers_nsprefix_ + ':' if (UseCapturedNS_ and self.sequenceNumbers_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssequenceNumbers>%s</%ssequenceNumbers>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.sequenceNumbers), input_name='sequenceNumbers')), namespaceprefix_ , eol_))
        if self.pieceReference is not None:
            namespaceprefix_ = self.pieceReference_nsprefix_ + ':' if (UseCapturedNS_ and self.pieceReference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spieceReference>%s</%spieceReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.pieceReference), input_name='pieceReference')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'sequenceNumbers':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'sequenceNumbers')
            value_ = self.gds_validate_string(value_, node, 'sequenceNumbers')
            self.sequenceNumbers = value_
            self.sequenceNumbers_nsprefix_ = child_.prefix
        elif nodeName_ == 'pieceReference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'pieceReference')
            value_ = self.gds_validate_string(value_, node, 'pieceReference')
            self.pieceReference = value_
            self.pieceReference_nsprefix_ = child_.prefix
# end class pieceType


class contactType(GeneratedsSuper):
    """Information about the contact person at the relevant address."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, name=None, telephoneNumber=None, emailAddress=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name = name
        self.validate_stringMaxLength30(self.name)
        self.name_nsprefix_ = None
        self.telephoneNumber = telephoneNumber
        self.validate_stringMaxLength30(self.telephoneNumber)
        self.telephoneNumber_nsprefix_ = None
        self.emailAddress = emailAddress
        self.emailAddress_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, contactType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if contactType.subclass:
            return contactType.subclass(*args_, **kwargs_)
        else:
            return contactType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_telephoneNumber(self):
        return self.telephoneNumber
    def set_telephoneNumber(self, telephoneNumber):
        self.telephoneNumber = telephoneNumber
    def get_emailAddress(self):
        return self.emailAddress
    def set_emailAddress(self, emailAddress):
        self.emailAddress = emailAddress
    def validate_stringMaxLength30(self, value):
        result = True
        # Validate type stringMaxLength30, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 30:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stringMaxLength30' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.name is not None or
            self.telephoneNumber is not None or
            self.emailAddress is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='contactType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('contactType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'contactType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='contactType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='contactType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='contactType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='contactType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.name is not None:
            namespaceprefix_ = self.name_nsprefix_ + ':' if (UseCapturedNS_ and self.name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sname>%s</%sname>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.name), input_name='name')), namespaceprefix_ , eol_))
        if self.telephoneNumber is not None:
            namespaceprefix_ = self.telephoneNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.telephoneNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stelephoneNumber>%s</%stelephoneNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.telephoneNumber), input_name='telephoneNumber')), namespaceprefix_ , eol_))
        if self.emailAddress is not None:
            namespaceprefix_ = self.emailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.emailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%semailAddress>%s</%semailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.emailAddress), input_name='emailAddress')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'name')
            value_ = self.gds_validate_string(value_, node, 'name')
            self.name = value_
            self.name_nsprefix_ = child_.prefix
            # validate type stringMaxLength30
            self.validate_stringMaxLength30(self.name)
        elif nodeName_ == 'telephoneNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'telephoneNumber')
            value_ = self.gds_validate_string(value_, node, 'telephoneNumber')
            self.telephoneNumber = value_
            self.telephoneNumber_nsprefix_ = child_.prefix
            # validate type stringMaxLength30
            self.validate_stringMaxLength30(self.telephoneNumber)
        elif nodeName_ == 'emailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'emailAddress')
            value_ = self.gds_validate_string(value_, node, 'emailAddress')
            self.emailAddress = value_
            self.emailAddress_nsprefix_ = child_.prefix
# end class contactType


class accountType(GeneratedsSuper):
    """Information about a TNT account which includes the account number
    and country code."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, accountNumber=None, accountCountry=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.accountNumber = accountNumber
        self.validate_stringMaxLength10(self.accountNumber)
        self.accountNumber_nsprefix_ = None
        self.accountCountry = accountCountry
        self.validate_stringMinLength2MaxLength2(self.accountCountry)
        self.accountCountry_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, accountType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if accountType.subclass:
            return accountType.subclass(*args_, **kwargs_)
        else:
            return accountType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_accountNumber(self):
        return self.accountNumber
    def set_accountNumber(self, accountNumber):
        self.accountNumber = accountNumber
    def get_accountCountry(self):
        return self.accountCountry
    def set_accountCountry(self, accountCountry):
        self.accountCountry = accountCountry
    def validate_stringMaxLength10(self, value):
        result = True
        # Validate type stringMaxLength10, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stringMaxLength10' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_stringMinLength2MaxLength2(self, value):
        result = True
        # Validate type stringMinLength2MaxLength2, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stringMinLength2MaxLength2' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on stringMinLength2MaxLength2' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.accountNumber is not None or
            self.accountCountry is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='accountType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('accountType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'accountType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='accountType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='accountType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='accountType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='accountType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.accountNumber is not None:
            namespaceprefix_ = self.accountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.accountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saccountNumber>%s</%saccountNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.accountNumber), input_name='accountNumber')), namespaceprefix_ , eol_))
        if self.accountCountry is not None:
            namespaceprefix_ = self.accountCountry_nsprefix_ + ':' if (UseCapturedNS_ and self.accountCountry_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saccountCountry>%s</%saccountCountry>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.accountCountry), input_name='accountCountry')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'accountNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'accountNumber')
            value_ = self.gds_validate_string(value_, node, 'accountNumber')
            self.accountNumber = value_
            self.accountNumber_nsprefix_ = child_.prefix
            # validate type stringMaxLength10
            self.validate_stringMaxLength10(self.accountNumber)
        elif nodeName_ == 'accountCountry':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'accountCountry')
            value_ = self.gds_validate_string(value_, node, 'accountCountry')
            self.accountCountry = value_
            self.accountCountry_nsprefix_ = child_.prefix
            # validate type stringMinLength2MaxLength2
            self.validate_stringMinLength2MaxLength2(self.accountCountry)
# end class accountType


class depotType(GeneratedsSuper):
    """Details relating to a TNT depot which could be the origin,
    destination or transit depot on the route calculated by TNT to deliver
    a consignment."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, depotCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.depotCode = depotCode
        self.validate_stringMinLength3MaxLength3(self.depotCode)
        self.depotCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, depotType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if depotType.subclass:
            return depotType.subclass(*args_, **kwargs_)
        else:
            return depotType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_depotCode(self):
        return self.depotCode
    def set_depotCode(self, depotCode):
        self.depotCode = depotCode
    def validate_stringMinLength3MaxLength3(self, value):
        result = True
        # Validate type stringMinLength3MaxLength3, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stringMinLength3MaxLength3' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on stringMinLength3MaxLength3' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.depotCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='depotType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('depotType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'depotType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='depotType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='depotType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='depotType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='depotType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.depotCode is not None:
            namespaceprefix_ = self.depotCode_nsprefix_ + ':' if (UseCapturedNS_ and self.depotCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdepotCode>%s</%sdepotCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.depotCode), input_name='depotCode')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'depotCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'depotCode')
            value_ = self.gds_validate_string(value_, node, 'depotCode')
            self.depotCode = value_
            self.depotCode_nsprefix_ = child_.prefix
            # validate type stringMinLength3MaxLength3
            self.validate_stringMinLength3MaxLength3(self.depotCode)
# end class depotType


class marketType(GeneratedsSuper):
    """This identifies the market type for the consignment comprising the
    origin
    country and whether the consignment is being shipped domestically or
    internationally and within which international trading block, e.g. 'EU'."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, originCountryCode=None, marketSpecification=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.originCountryCode = originCountryCode
        self.validate_stringMinLength2MaxLength2(self.originCountryCode)
        self.originCountryCode_nsprefix_ = None
        self.marketSpecification = marketSpecification
        self.marketSpecification_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, marketType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if marketType.subclass:
            return marketType.subclass(*args_, **kwargs_)
        else:
            return marketType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_originCountryCode(self):
        return self.originCountryCode
    def set_originCountryCode(self, originCountryCode):
        self.originCountryCode = originCountryCode
    def get_marketSpecification(self):
        return self.marketSpecification
    def set_marketSpecification(self, marketSpecification):
        self.marketSpecification = marketSpecification
    def validate_stringMinLength2MaxLength2(self, value):
        result = True
        # Validate type stringMinLength2MaxLength2, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stringMinLength2MaxLength2' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on stringMinLength2MaxLength2' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.originCountryCode is not None or
            self.marketSpecification is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='marketType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('marketType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'marketType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='marketType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='marketType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='marketType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='marketType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.originCountryCode is not None:
            namespaceprefix_ = self.originCountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.originCountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%soriginCountryCode>%s</%soriginCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.originCountryCode), input_name='originCountryCode')), namespaceprefix_ , eol_))
        if self.marketSpecification is not None:
            namespaceprefix_ = self.marketSpecification_nsprefix_ + ':' if (UseCapturedNS_ and self.marketSpecification_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smarketSpecification>%s</%smarketSpecification>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.marketSpecification), input_name='marketSpecification')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'originCountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'originCountryCode')
            value_ = self.gds_validate_string(value_, node, 'originCountryCode')
            self.originCountryCode = value_
            self.originCountryCode_nsprefix_ = child_.prefix
            # validate type stringMinLength2MaxLength2
            self.validate_stringMinLength2MaxLength2(self.originCountryCode)
        elif nodeName_ == 'marketSpecification':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'marketSpecification')
            value_ = self.gds_validate_string(value_, node, 'marketSpecification')
            self.marketSpecification = value_
            self.marketSpecification_nsprefix_ = child_.prefix
# end class marketType


class brokenRules(GeneratedsSuper):
    """List of business rules that have been breached by the input and that
    will
    require the user to correct in order to print labels on resubmission of
    XML input file.RequestId number to which the error relates."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, key=None, errorCode=None, errorDescription=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.key = _cast(None, key)
        self.key_nsprefix_ = None
        self.errorCode = errorCode
        self.errorCode_nsprefix_ = None
        self.errorDescription = errorDescription
        self.errorDescription_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, brokenRules)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if brokenRules.subclass:
            return brokenRules.subclass(*args_, **kwargs_)
        else:
            return brokenRules(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_errorCode(self):
        return self.errorCode
    def set_errorCode(self, errorCode):
        self.errorCode = errorCode
    def get_errorDescription(self):
        return self.errorDescription
    def set_errorDescription(self, errorDescription):
        self.errorDescription = errorDescription
    def get_key(self):
        return self.key
    def set_key(self, key):
        self.key = key
    def hasContent_(self):
        if (
            self.errorCode is not None or
            self.errorDescription is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='brokenRules', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('brokenRules')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'brokenRules':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='brokenRules')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='brokenRules', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='brokenRules'):
        if self.key is not None and 'key' not in already_processed:
            already_processed.add('key')
            outfile.write(' key=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.key), input_name='key')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='brokenRules', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.errorCode is not None:
            namespaceprefix_ = self.errorCode_nsprefix_ + ':' if (UseCapturedNS_ and self.errorCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%serrorCode>%s</%serrorCode>%s' % (namespaceprefix_ , self.gds_format_integer(self.errorCode, input_name='errorCode'), namespaceprefix_ , eol_))
        if self.errorDescription is not None:
            namespaceprefix_ = self.errorDescription_nsprefix_ + ':' if (UseCapturedNS_ and self.errorDescription_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%serrorDescription>%s</%serrorDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.errorDescription), input_name='errorDescription')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('key', node)
        if value is not None and 'key' not in already_processed:
            already_processed.add('key')
            self.key = value
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'errorCode' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'errorCode')
            ival_ = self.gds_validate_integer(ival_, node, 'errorCode')
            self.errorCode = ival_
            self.errorCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'errorDescription':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'errorDescription')
            value_ = self.gds_validate_string(value_, node, 'errorDescription')
            self.errorDescription = value_
            self.errorDescription_nsprefix_ = child_.prefix
# end class brokenRules


class fault(GeneratedsSuper):
    """List of faults that have occured during teh processign of multiple
    requestsRequestId number to which the fault relates."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, key=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.key = _cast(None, key)
        self.key_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, fault)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if fault.subclass:
            return fault.subclass(*args_, **kwargs_)
        else:
            return fault(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_key(self):
        return self.key
    def set_key(self, key):
        self.key = key
    def hasContent_(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='fault', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('fault')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'fault':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='fault')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='fault', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='fault'):
        if self.key is not None and 'key' not in already_processed:
            already_processed.add('key')
            outfile.write(' key=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.key), input_name='key')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='fault', fromsubclass_=False, pretty_print=True):
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
        value = find_attr_value_('key', node)
        if value is not None and 'key' not in already_processed:
            already_processed.add('key')
            self.key = value
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class fault


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
        rootTag = 'labelResponse'
        rootClass = labelResponse
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
        rootTag = 'labelResponse'
        rootClass = labelResponse
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
        rootTag = 'labelResponse'
        rootClass = labelResponse
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
        rootTag = 'labelResponse'
        rootClass = labelResponse
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from label_response import *\n\n')
        sys.stdout.write('import label_response as model_\n\n')
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
    "accountType",
    "actionDepotType",
    "barcodeType",
    "brokenRules",
    "consignmentIdentityType",
    "consignmentResponseType",
    "consignmentRoutingLabelType",
    "contactType",
    "depotType",
    "destinationDepotType",
    "fault",
    "labelResponse",
    "marketType",
    "measurementsType",
    "nameAndAddressRequestType",
    "nameAndAddressResponseType",
    "numericRenderInstructionsType",
    "optionDescriptionType",
    "optionType",
    "pieceLineType",
    "pieceRoutingLabelType",
    "pieceType",
    "productDescriptionType",
    "renderInstructionsType",
    "sortDepotType",
    "transitDepotListType",
    "twoDBarcodeType"
]
