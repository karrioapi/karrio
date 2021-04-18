#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Wed Feb 24 19:49:29 2021 by generateDS.py version 2.37.16.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './tnt_lib/pricing_response.py')
#
# Command line arguments:
#   ./schemas/pricing_response.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./tnt_lib/pricing_response.py" ./schemas/pricing_response.xsd
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


class document(GeneratedsSuper):
    """The root element for a response from the ExpressConnect Pricing
    Service"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, requestId=None, errors=None, priceResponse=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.requestId = requestId
        self.requestId_nsprefix_ = None
        self.errors = errors
        self.errors_nsprefix_ = None
        if priceResponse is None:
            self.priceResponse = []
        else:
            self.priceResponse = priceResponse
        self.priceResponse_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, document)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if document.subclass:
            return document.subclass(*args_, **kwargs_)
        else:
            return document(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_requestId(self):
        return self.requestId
    def set_requestId(self, requestId):
        self.requestId = requestId
    def get_errors(self):
        return self.errors
    def set_errors(self, errors):
        self.errors = errors
    def get_priceResponse(self):
        return self.priceResponse
    def set_priceResponse(self, priceResponse):
        self.priceResponse = priceResponse
    def add_priceResponse(self, value):
        self.priceResponse.append(value)
    def insert_priceResponse_at(self, index, value):
        self.priceResponse.insert(index, value)
    def replace_priceResponse_at(self, index, value):
        self.priceResponse[index] = value
    def hasContent_(self):
        if (
            self.requestId is not None or
            self.errors is not None or
            self.priceResponse
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='document', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('document')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'document':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='document')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='document', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='document'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='document', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.requestId is not None:
            namespaceprefix_ = self.requestId_nsprefix_ + ':' if (UseCapturedNS_ and self.requestId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%srequestId>%s</%srequestId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.requestId), input_name='requestId')), namespaceprefix_ , eol_))
        if self.errors is not None:
            namespaceprefix_ = self.errors_nsprefix_ + ':' if (UseCapturedNS_ and self.errors_nsprefix_) else ''
            self.errors.export(outfile, level, namespaceprefix_, namespacedef_='', name_='errors', pretty_print=pretty_print)
        for priceResponse_ in self.priceResponse:
            namespaceprefix_ = self.priceResponse_nsprefix_ + ':' if (UseCapturedNS_ and self.priceResponse_nsprefix_) else ''
            priceResponse_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='priceResponse', pretty_print=pretty_print)
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
        if nodeName_ == 'requestId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'requestId')
            value_ = self.gds_validate_string(value_, node, 'requestId')
            self.requestId = value_
            self.requestId_nsprefix_ = child_.prefix
        elif nodeName_ == 'errors':
            obj_ = errors.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.errors = obj_
            obj_.original_tagname_ = 'errors'
        elif nodeName_ == 'priceResponse':
            obj_ = priceResponse.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.priceResponse.append(obj_)
            obj_.original_tagname_ = 'priceResponse'
# end class document


class priceResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ratedServices=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ratedServices = ratedServices
        self.ratedServices_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, priceResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if priceResponse.subclass:
            return priceResponse.subclass(*args_, **kwargs_)
        else:
            return priceResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ratedServices(self):
        return self.ratedServices
    def set_ratedServices(self, ratedServices):
        self.ratedServices = ratedServices
    def hasContent_(self):
        if (
            self.ratedServices is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='priceResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('priceResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'priceResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='priceResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='priceResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='priceResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='priceResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ratedServices is not None:
            namespaceprefix_ = self.ratedServices_nsprefix_ + ':' if (UseCapturedNS_ and self.ratedServices_nsprefix_) else ''
            self.ratedServices.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ratedServices', pretty_print=pretty_print)
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
        if nodeName_ == 'ratedServices':
            obj_ = ratedServices.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ratedServices = obj_
            obj_.original_tagname_ = 'ratedServices'
# end class priceResponse


class ratedServices(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, rateId=None, currency=None, ratedService=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.rateId = rateId
        self.rateId_nsprefix_ = None
        self.currency = currency
        self.currency_nsprefix_ = None
        if ratedService is None:
            self.ratedService = []
        else:
            self.ratedService = ratedService
        self.ratedService_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ratedServices)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ratedServices.subclass:
            return ratedServices.subclass(*args_, **kwargs_)
        else:
            return ratedServices(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_rateId(self):
        return self.rateId
    def set_rateId(self, rateId):
        self.rateId = rateId
    def get_currency(self):
        return self.currency
    def set_currency(self, currency):
        self.currency = currency
    def get_ratedService(self):
        return self.ratedService
    def set_ratedService(self, ratedService):
        self.ratedService = ratedService
    def add_ratedService(self, value):
        self.ratedService.append(value)
    def insert_ratedService_at(self, index, value):
        self.ratedService.insert(index, value)
    def replace_ratedService_at(self, index, value):
        self.ratedService[index] = value
    def hasContent_(self):
        if (
            self.rateId is not None or
            self.currency is not None or
            self.ratedService
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ratedServices', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ratedServices')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ratedServices':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ratedServices')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ratedServices', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ratedServices'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ratedServices', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.rateId is not None:
            namespaceprefix_ = self.rateId_nsprefix_ + ':' if (UseCapturedNS_ and self.rateId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%srateId>%s</%srateId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.rateId), input_name='rateId')), namespaceprefix_ , eol_))
        if self.currency is not None:
            namespaceprefix_ = self.currency_nsprefix_ + ':' if (UseCapturedNS_ and self.currency_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scurrency>%s</%scurrency>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.currency), input_name='currency')), namespaceprefix_ , eol_))
        for ratedService_ in self.ratedService:
            namespaceprefix_ = self.ratedService_nsprefix_ + ':' if (UseCapturedNS_ and self.ratedService_nsprefix_) else ''
            ratedService_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ratedService', pretty_print=pretty_print)
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
        if nodeName_ == 'rateId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'rateId')
            value_ = self.gds_validate_string(value_, node, 'rateId')
            self.rateId = value_
            self.rateId_nsprefix_ = child_.prefix
        elif nodeName_ == 'currency':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'currency')
            value_ = self.gds_validate_string(value_, node, 'currency')
            self.currency = value_
            self.currency_nsprefix_ = child_.prefix
        elif nodeName_ == 'ratedService':
            obj_ = ratedService.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ratedService.append(obj_)
            obj_.original_tagname_ = 'ratedService'
# end class ratedServices


class ratedService(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, product=None, totalPrice=None, totalPriceExclVat=None, vatAmount=None, chargeElements=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.product = product
        self.product_nsprefix_ = None
        self.totalPrice = totalPrice
        self.totalPrice_nsprefix_ = None
        self.totalPriceExclVat = totalPriceExclVat
        self.totalPriceExclVat_nsprefix_ = None
        self.vatAmount = vatAmount
        self.vatAmount_nsprefix_ = None
        self.chargeElements = chargeElements
        self.chargeElements_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ratedService)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ratedService.subclass:
            return ratedService.subclass(*args_, **kwargs_)
        else:
            return ratedService(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_product(self):
        return self.product
    def set_product(self, product):
        self.product = product
    def get_totalPrice(self):
        return self.totalPrice
    def set_totalPrice(self, totalPrice):
        self.totalPrice = totalPrice
    def get_totalPriceExclVat(self):
        return self.totalPriceExclVat
    def set_totalPriceExclVat(self, totalPriceExclVat):
        self.totalPriceExclVat = totalPriceExclVat
    def get_vatAmount(self):
        return self.vatAmount
    def set_vatAmount(self, vatAmount):
        self.vatAmount = vatAmount
    def get_chargeElements(self):
        return self.chargeElements
    def set_chargeElements(self, chargeElements):
        self.chargeElements = chargeElements
    def hasContent_(self):
        if (
            self.product is not None or
            self.totalPrice is not None or
            self.totalPriceExclVat is not None or
            self.vatAmount is not None or
            self.chargeElements is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ratedService', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ratedService')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ratedService':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ratedService')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ratedService', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ratedService'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ratedService', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.product is not None:
            namespaceprefix_ = self.product_nsprefix_ + ':' if (UseCapturedNS_ and self.product_nsprefix_) else ''
            self.product.export(outfile, level, namespaceprefix_, namespacedef_='', name_='product', pretty_print=pretty_print)
        if self.totalPrice is not None:
            namespaceprefix_ = self.totalPrice_nsprefix_ + ':' if (UseCapturedNS_ and self.totalPrice_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stotalPrice>%s</%stotalPrice>%s' % (namespaceprefix_ , self.gds_format_decimal(self.totalPrice, input_name='totalPrice'), namespaceprefix_ , eol_))
        if self.totalPriceExclVat is not None:
            namespaceprefix_ = self.totalPriceExclVat_nsprefix_ + ':' if (UseCapturedNS_ and self.totalPriceExclVat_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stotalPriceExclVat>%s</%stotalPriceExclVat>%s' % (namespaceprefix_ , self.gds_format_decimal(self.totalPriceExclVat, input_name='totalPriceExclVat'), namespaceprefix_ , eol_))
        if self.vatAmount is not None:
            namespaceprefix_ = self.vatAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.vatAmount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%svatAmount>%s</%svatAmount>%s' % (namespaceprefix_ , self.gds_format_decimal(self.vatAmount, input_name='vatAmount'), namespaceprefix_ , eol_))
        if self.chargeElements is not None:
            namespaceprefix_ = self.chargeElements_nsprefix_ + ':' if (UseCapturedNS_ and self.chargeElements_nsprefix_) else ''
            self.chargeElements.export(outfile, level, namespaceprefix_, namespacedef_='', name_='chargeElements', pretty_print=pretty_print)
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
        if nodeName_ == 'product':
            obj_ = product.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.product = obj_
            obj_.original_tagname_ = 'product'
        elif nodeName_ == 'totalPrice' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'totalPrice')
            fval_ = self.gds_validate_decimal(fval_, node, 'totalPrice')
            self.totalPrice = fval_
            self.totalPrice_nsprefix_ = child_.prefix
        elif nodeName_ == 'totalPriceExclVat' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'totalPriceExclVat')
            fval_ = self.gds_validate_decimal(fval_, node, 'totalPriceExclVat')
            self.totalPriceExclVat = fval_
            self.totalPriceExclVat_nsprefix_ = child_.prefix
        elif nodeName_ == 'vatAmount' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'vatAmount')
            fval_ = self.gds_validate_decimal(fval_, node, 'vatAmount')
            self.vatAmount = fval_
            self.vatAmount_nsprefix_ = child_.prefix
        elif nodeName_ == 'chargeElements':
            obj_ = chargeElements.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.chargeElements = obj_
            obj_.original_tagname_ = 'chargeElements'
# end class ratedService


class chargeElements(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, chargeElement=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if chargeElement is None:
            self.chargeElement = []
        else:
            self.chargeElement = chargeElement
        self.chargeElement_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, chargeElements)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if chargeElements.subclass:
            return chargeElements.subclass(*args_, **kwargs_)
        else:
            return chargeElements(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_chargeElement(self):
        return self.chargeElement
    def set_chargeElement(self, chargeElement):
        self.chargeElement = chargeElement
    def add_chargeElement(self, value):
        self.chargeElement.append(value)
    def insert_chargeElement_at(self, index, value):
        self.chargeElement.insert(index, value)
    def replace_chargeElement_at(self, index, value):
        self.chargeElement[index] = value
    def hasContent_(self):
        if (
            self.chargeElement
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='chargeElements', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('chargeElements')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'chargeElements':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='chargeElements')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='chargeElements', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='chargeElements'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='chargeElements', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for chargeElement_ in self.chargeElement:
            namespaceprefix_ = self.chargeElement_nsprefix_ + ':' if (UseCapturedNS_ and self.chargeElement_nsprefix_) else ''
            chargeElement_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='chargeElement', pretty_print=pretty_print)
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
        if nodeName_ == 'chargeElement':
            obj_ = chargeElement.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.chargeElement.append(obj_)
            obj_.original_tagname_ = 'chargeElement'
# end class chargeElements


class chargeElement(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, chargeItem=None, chargeCategory=None, chargeCode=None, description=None, chargeValue=None, vatIndicator=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.chargeItem = chargeItem
        self.chargeItem_nsprefix_ = None
        self.chargeCategory = chargeCategory
        self.chargeCategory_nsprefix_ = None
        self.chargeCode = chargeCode
        self.chargeCode_nsprefix_ = None
        self.description = description
        self.description_nsprefix_ = None
        self.chargeValue = chargeValue
        self.chargeValue_nsprefix_ = None
        self.vatIndicator = vatIndicator
        self.vatIndicator_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, chargeElement)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if chargeElement.subclass:
            return chargeElement.subclass(*args_, **kwargs_)
        else:
            return chargeElement(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_chargeItem(self):
        return self.chargeItem
    def set_chargeItem(self, chargeItem):
        self.chargeItem = chargeItem
    def get_chargeCategory(self):
        return self.chargeCategory
    def set_chargeCategory(self, chargeCategory):
        self.chargeCategory = chargeCategory
    def get_chargeCode(self):
        return self.chargeCode
    def set_chargeCode(self, chargeCode):
        self.chargeCode = chargeCode
    def get_description(self):
        return self.description
    def set_description(self, description):
        self.description = description
    def get_chargeValue(self):
        return self.chargeValue
    def set_chargeValue(self, chargeValue):
        self.chargeValue = chargeValue
    def get_vatIndicator(self):
        return self.vatIndicator
    def set_vatIndicator(self, vatIndicator):
        self.vatIndicator = vatIndicator
    def hasContent_(self):
        if (
            self.chargeItem is not None or
            self.chargeCategory is not None or
            self.chargeCode is not None or
            self.description is not None or
            self.chargeValue is not None or
            self.vatIndicator is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='chargeElement', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('chargeElement')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'chargeElement':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='chargeElement')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='chargeElement', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='chargeElement'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='chargeElement', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.chargeItem is not None:
            namespaceprefix_ = self.chargeItem_nsprefix_ + ':' if (UseCapturedNS_ and self.chargeItem_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%schargeItem>%s</%schargeItem>%s' % (namespaceprefix_ , self.gds_format_integer(self.chargeItem, input_name='chargeItem'), namespaceprefix_ , eol_))
        if self.chargeCategory is not None:
            namespaceprefix_ = self.chargeCategory_nsprefix_ + ':' if (UseCapturedNS_ and self.chargeCategory_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%schargeCategory>%s</%schargeCategory>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.chargeCategory), input_name='chargeCategory')), namespaceprefix_ , eol_))
        if self.chargeCode is not None:
            namespaceprefix_ = self.chargeCode_nsprefix_ + ':' if (UseCapturedNS_ and self.chargeCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%schargeCode>%s</%schargeCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.chargeCode), input_name='chargeCode')), namespaceprefix_ , eol_))
        if self.description is not None:
            namespaceprefix_ = self.description_nsprefix_ + ':' if (UseCapturedNS_ and self.description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdescription>%s</%sdescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.description), input_name='description')), namespaceprefix_ , eol_))
        if self.chargeValue is not None:
            namespaceprefix_ = self.chargeValue_nsprefix_ + ':' if (UseCapturedNS_ and self.chargeValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%schargeValue>%s</%schargeValue>%s' % (namespaceprefix_ , self.gds_format_decimal(self.chargeValue, input_name='chargeValue'), namespaceprefix_ , eol_))
        if self.vatIndicator is not None:
            namespaceprefix_ = self.vatIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.vatIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%svatIndicator>%s</%svatIndicator>%s' % (namespaceprefix_ , self.gds_format_boolean(self.vatIndicator, input_name='vatIndicator'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'chargeItem' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'chargeItem')
            ival_ = self.gds_validate_integer(ival_, node, 'chargeItem')
            self.chargeItem = ival_
            self.chargeItem_nsprefix_ = child_.prefix
        elif nodeName_ == 'chargeCategory':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'chargeCategory')
            value_ = self.gds_validate_string(value_, node, 'chargeCategory')
            self.chargeCategory = value_
            self.chargeCategory_nsprefix_ = child_.prefix
        elif nodeName_ == 'chargeCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'chargeCode')
            value_ = self.gds_validate_string(value_, node, 'chargeCode')
            self.chargeCode = value_
            self.chargeCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'description')
            value_ = self.gds_validate_string(value_, node, 'description')
            self.description = value_
            self.description_nsprefix_ = child_.prefix
        elif nodeName_ == 'chargeValue' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'chargeValue')
            fval_ = self.gds_validate_decimal(fval_, node, 'chargeValue')
            self.chargeValue = fval_
            self.chargeValue_nsprefix_ = child_.prefix
        elif nodeName_ == 'vatIndicator':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'vatIndicator')
            ival_ = self.gds_validate_boolean(ival_, node, 'vatIndicator')
            self.vatIndicator = ival_
            self.vatIndicator_nsprefix_ = child_.prefix
# end class chargeElement


class errors(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, runtimeError=None, parseError=None, brokenRule=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if runtimeError is None:
            self.runtimeError = []
        else:
            self.runtimeError = runtimeError
        self.runtimeError_nsprefix_ = None
        if parseError is None:
            self.parseError = []
        else:
            self.parseError = parseError
        self.parseError_nsprefix_ = None
        if brokenRule is None:
            self.brokenRule = []
        else:
            self.brokenRule = brokenRule
        self.brokenRule_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, errors)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if errors.subclass:
            return errors.subclass(*args_, **kwargs_)
        else:
            return errors(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_runtimeError(self):
        return self.runtimeError
    def set_runtimeError(self, runtimeError):
        self.runtimeError = runtimeError
    def add_runtimeError(self, value):
        self.runtimeError.append(value)
    def insert_runtimeError_at(self, index, value):
        self.runtimeError.insert(index, value)
    def replace_runtimeError_at(self, index, value):
        self.runtimeError[index] = value
    def get_parseError(self):
        return self.parseError
    def set_parseError(self, parseError):
        self.parseError = parseError
    def add_parseError(self, value):
        self.parseError.append(value)
    def insert_parseError_at(self, index, value):
        self.parseError.insert(index, value)
    def replace_parseError_at(self, index, value):
        self.parseError[index] = value
    def get_brokenRule(self):
        return self.brokenRule
    def set_brokenRule(self, brokenRule):
        self.brokenRule = brokenRule
    def add_brokenRule(self, value):
        self.brokenRule.append(value)
    def insert_brokenRule_at(self, index, value):
        self.brokenRule.insert(index, value)
    def replace_brokenRule_at(self, index, value):
        self.brokenRule[index] = value
    def hasContent_(self):
        if (
            self.runtimeError or
            self.parseError or
            self.brokenRule
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='errors', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('errors')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'errors':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='errors')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='errors', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='errors'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='errors', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for runtimeError_ in self.runtimeError:
            namespaceprefix_ = self.runtimeError_nsprefix_ + ':' if (UseCapturedNS_ and self.runtimeError_nsprefix_) else ''
            runtimeError_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='runtimeError', pretty_print=pretty_print)
        for parseError_ in self.parseError:
            namespaceprefix_ = self.parseError_nsprefix_ + ':' if (UseCapturedNS_ and self.parseError_nsprefix_) else ''
            parseError_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='parseError', pretty_print=pretty_print)
        for brokenRule_ in self.brokenRule:
            namespaceprefix_ = self.brokenRule_nsprefix_ + ':' if (UseCapturedNS_ and self.brokenRule_nsprefix_) else ''
            brokenRule_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='brokenRule', pretty_print=pretty_print)
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
        if nodeName_ == 'runtimeError':
            obj_ = runtimeError.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.runtimeError.append(obj_)
            obj_.original_tagname_ = 'runtimeError'
        elif nodeName_ == 'parseError':
            obj_ = parseError.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.parseError.append(obj_)
            obj_.original_tagname_ = 'parseError'
        elif nodeName_ == 'brokenRule':
            obj_ = brokenRule.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.brokenRule.append(obj_)
            obj_.original_tagname_ = 'brokenRule'
# end class errors


class runtimeError(GeneratedsSuper):
    """The runtime error messages returned by
    ExpressConnect e.g pricing service not available"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, errorReason=None, errorSrcText=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.errorReason = errorReason
        self.errorReason_nsprefix_ = None
        self.errorSrcText = errorSrcText
        self.errorSrcText_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, runtimeError)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if runtimeError.subclass:
            return runtimeError.subclass(*args_, **kwargs_)
        else:
            return runtimeError(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_errorReason(self):
        return self.errorReason
    def set_errorReason(self, errorReason):
        self.errorReason = errorReason
    def get_errorSrcText(self):
        return self.errorSrcText
    def set_errorSrcText(self, errorSrcText):
        self.errorSrcText = errorSrcText
    def hasContent_(self):
        if (
            self.errorReason is not None or
            self.errorSrcText is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='runtimeError', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('runtimeError')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'runtimeError':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='runtimeError')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='runtimeError', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='runtimeError'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='runtimeError', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.errorReason is not None:
            namespaceprefix_ = self.errorReason_nsprefix_ + ':' if (UseCapturedNS_ and self.errorReason_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%serrorReason>%s</%serrorReason>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.errorReason), input_name='errorReason')), namespaceprefix_ , eol_))
        if self.errorSrcText is not None:
            namespaceprefix_ = self.errorSrcText_nsprefix_ + ':' if (UseCapturedNS_ and self.errorSrcText_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%serrorSrcText>%s</%serrorSrcText>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.errorSrcText), input_name='errorSrcText')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'errorReason':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'errorReason')
            value_ = self.gds_validate_string(value_, node, 'errorReason')
            self.errorReason = value_
            self.errorReason_nsprefix_ = child_.prefix
        elif nodeName_ == 'errorSrcText':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'errorSrcText')
            value_ = self.gds_validate_string(value_, node, 'errorSrcText')
            self.errorSrcText = value_
            self.errorSrcText_nsprefix_ = child_.prefix
# end class runtimeError


class parseError(GeneratedsSuper):
    """The XML parse error messages returned by
    ExpressConnect e.g. Element content is invalid
    according
    to the
    XSD/Schema."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, errorReason=None, errorLine=None, errorLinepos=None, errorSrcText=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.errorReason = errorReason
        self.errorReason_nsprefix_ = None
        self.errorLine = errorLine
        self.errorLine_nsprefix_ = None
        self.errorLinepos = errorLinepos
        self.errorLinepos_nsprefix_ = None
        self.errorSrcText = errorSrcText
        self.errorSrcText_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, parseError)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if parseError.subclass:
            return parseError.subclass(*args_, **kwargs_)
        else:
            return parseError(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_errorReason(self):
        return self.errorReason
    def set_errorReason(self, errorReason):
        self.errorReason = errorReason
    def get_errorLine(self):
        return self.errorLine
    def set_errorLine(self, errorLine):
        self.errorLine = errorLine
    def get_errorLinepos(self):
        return self.errorLinepos
    def set_errorLinepos(self, errorLinepos):
        self.errorLinepos = errorLinepos
    def get_errorSrcText(self):
        return self.errorSrcText
    def set_errorSrcText(self, errorSrcText):
        self.errorSrcText = errorSrcText
    def hasContent_(self):
        if (
            self.errorReason is not None or
            self.errorLine is not None or
            self.errorLinepos is not None or
            self.errorSrcText is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='parseError', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('parseError')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'parseError':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='parseError')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='parseError', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='parseError'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='parseError', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.errorReason is not None:
            namespaceprefix_ = self.errorReason_nsprefix_ + ':' if (UseCapturedNS_ and self.errorReason_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%serrorReason>%s</%serrorReason>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.errorReason), input_name='errorReason')), namespaceprefix_ , eol_))
        if self.errorLine is not None:
            namespaceprefix_ = self.errorLine_nsprefix_ + ':' if (UseCapturedNS_ and self.errorLine_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%serrorLine>%s</%serrorLine>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.errorLine), input_name='errorLine')), namespaceprefix_ , eol_))
        if self.errorLinepos is not None:
            namespaceprefix_ = self.errorLinepos_nsprefix_ + ':' if (UseCapturedNS_ and self.errorLinepos_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%serrorLinepos>%s</%serrorLinepos>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.errorLinepos), input_name='errorLinepos')), namespaceprefix_ , eol_))
        if self.errorSrcText is not None:
            namespaceprefix_ = self.errorSrcText_nsprefix_ + ':' if (UseCapturedNS_ and self.errorSrcText_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%serrorSrcText>%s</%serrorSrcText>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.errorSrcText), input_name='errorSrcText')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'errorReason':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'errorReason')
            value_ = self.gds_validate_string(value_, node, 'errorReason')
            self.errorReason = value_
            self.errorReason_nsprefix_ = child_.prefix
        elif nodeName_ == 'errorLine':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'errorLine')
            value_ = self.gds_validate_string(value_, node, 'errorLine')
            self.errorLine = value_
            self.errorLine_nsprefix_ = child_.prefix
        elif nodeName_ == 'errorLinepos':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'errorLinepos')
            value_ = self.gds_validate_string(value_, node, 'errorLinepos')
            self.errorLinepos = value_
            self.errorLinepos_nsprefix_ = child_.prefix
        elif nodeName_ == 'errorSrcText':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'errorSrcText')
            value_ = self.gds_validate_string(value_, node, 'errorSrcText')
            self.errorSrcText = value_
            self.errorSrcText_nsprefix_ = child_.prefix
# end class parseError


class brokenRule(GeneratedsSuper):
    """The brokenRule section is for application errors which the customer can
    resolve such as invalid
    postcode, login credentials."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, rateId=None, messageType=None, code=None, description=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.rateId = rateId
        self.rateId_nsprefix_ = None
        self.messageType = messageType
        self.messageType_nsprefix_ = None
        self.code = code
        self.code_nsprefix_ = None
        self.description = description
        self.description_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, brokenRule)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if brokenRule.subclass:
            return brokenRule.subclass(*args_, **kwargs_)
        else:
            return brokenRule(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_rateId(self):
        return self.rateId
    def set_rateId(self, rateId):
        self.rateId = rateId
    def get_messageType(self):
        return self.messageType
    def set_messageType(self, messageType):
        self.messageType = messageType
    def get_code(self):
        return self.code
    def set_code(self, code):
        self.code = code
    def get_description(self):
        return self.description
    def set_description(self, description):
        self.description = description
    def hasContent_(self):
        if (
            self.rateId is not None or
            self.messageType is not None or
            self.code is not None or
            self.description is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='brokenRule', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('brokenRule')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'brokenRule':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='brokenRule')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='brokenRule', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='brokenRule'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='brokenRule', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.rateId is not None:
            namespaceprefix_ = self.rateId_nsprefix_ + ':' if (UseCapturedNS_ and self.rateId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%srateId>%s</%srateId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.rateId), input_name='rateId')), namespaceprefix_ , eol_))
        if self.messageType is not None:
            namespaceprefix_ = self.messageType_nsprefix_ + ':' if (UseCapturedNS_ and self.messageType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smessageType>%s</%smessageType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.messageType), input_name='messageType')), namespaceprefix_ , eol_))
        if self.code is not None:
            namespaceprefix_ = self.code_nsprefix_ + ':' if (UseCapturedNS_ and self.code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scode>%s</%scode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.code), input_name='code')), namespaceprefix_ , eol_))
        if self.description is not None:
            namespaceprefix_ = self.description_nsprefix_ + ':' if (UseCapturedNS_ and self.description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdescription>%s</%sdescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.description), input_name='description')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'rateId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'rateId')
            value_ = self.gds_validate_string(value_, node, 'rateId')
            self.rateId = value_
            self.rateId_nsprefix_ = child_.prefix
        elif nodeName_ == 'messageType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'messageType')
            value_ = self.gds_validate_string(value_, node, 'messageType')
            self.messageType = value_
            self.messageType_nsprefix_ = child_.prefix
        elif nodeName_ == 'code':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'code')
            value_ = self.gds_validate_string(value_, node, 'code')
            self.code = value_
            self.code_nsprefix_ = child_.prefix
        elif nodeName_ == 'description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'description')
            value_ = self.gds_validate_string(value_, node, 'description')
            self.description = value_
            self.description_nsprefix_ = child_.prefix
# end class brokenRule


class product(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, id=None, division=None, productDesc=None, type_=None, options=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.id = id
        self.id_nsprefix_ = None
        self.division = division
        self.division_nsprefix_ = None
        self.productDesc = productDesc
        self.productDesc_nsprefix_ = None
        self.type_ = type_
        self.type__nsprefix_ = None
        self.options = options
        self.options_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, product)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if product.subclass:
            return product.subclass(*args_, **kwargs_)
        else:
            return product(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_id(self):
        return self.id
    def set_id(self, id):
        self.id = id
    def get_division(self):
        return self.division
    def set_division(self, division):
        self.division = division
    def get_productDesc(self):
        return self.productDesc
    def set_productDesc(self, productDesc):
        self.productDesc = productDesc
    def get_type(self):
        return self.type_
    def set_type(self, type_):
        self.type_ = type_
    def get_options(self):
        return self.options
    def set_options(self, options):
        self.options = options
    def hasContent_(self):
        if (
            self.id is not None or
            self.division is not None or
            self.productDesc is not None or
            self.type_ is not None or
            self.options is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='product', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('product')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'product':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='product')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='product', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='product'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='product', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.id is not None:
            namespaceprefix_ = self.id_nsprefix_ + ':' if (UseCapturedNS_ and self.id_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sid>%s</%sid>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.id), input_name='id')), namespaceprefix_ , eol_))
        if self.division is not None:
            namespaceprefix_ = self.division_nsprefix_ + ':' if (UseCapturedNS_ and self.division_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdivision>%s</%sdivision>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.division), input_name='division')), namespaceprefix_ , eol_))
        if self.productDesc is not None:
            namespaceprefix_ = self.productDesc_nsprefix_ + ':' if (UseCapturedNS_ and self.productDesc_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sproductDesc>%s</%sproductDesc>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.productDesc), input_name='productDesc')), namespaceprefix_ , eol_))
        if self.type_ is not None:
            namespaceprefix_ = self.type__nsprefix_ + ':' if (UseCapturedNS_ and self.type__nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stype>%s</%stype>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.type_), input_name='type')), namespaceprefix_ , eol_))
        if self.options is not None:
            namespaceprefix_ = self.options_nsprefix_ + ':' if (UseCapturedNS_ and self.options_nsprefix_) else ''
            self.options.export(outfile, level, namespaceprefix_, namespacedef_='', name_='options', pretty_print=pretty_print)
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
        if nodeName_ == 'id':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'id')
            value_ = self.gds_validate_string(value_, node, 'id')
            self.id = value_
            self.id_nsprefix_ = child_.prefix
        elif nodeName_ == 'division':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'division')
            value_ = self.gds_validate_string(value_, node, 'division')
            self.division = value_
            self.division_nsprefix_ = child_.prefix
        elif nodeName_ == 'productDesc':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'productDesc')
            value_ = self.gds_validate_string(value_, node, 'productDesc')
            self.productDesc = value_
            self.productDesc_nsprefix_ = child_.prefix
        elif nodeName_ == 'type':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'type')
            value_ = self.gds_validate_string(value_, node, 'type')
            self.type_ = value_
            self.type_nsprefix_ = child_.prefix
        elif nodeName_ == 'options':
            obj_ = options.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.options = obj_
            obj_.original_tagname_ = 'options'
# end class product


class options(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, option=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if option is None:
            self.option = []
        else:
            self.option = option
        self.option_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, options)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if options.subclass:
            return options.subclass(*args_, **kwargs_)
        else:
            return options(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
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
    def hasContent_(self):
        if (
            self.option
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='options', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('options')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'options':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='options')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='options', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='options'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='options', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for option_ in self.option:
            namespaceprefix_ = self.option_nsprefix_ + ':' if (UseCapturedNS_ and self.option_nsprefix_) else ''
            option_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='option', pretty_print=pretty_print)
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
        if nodeName_ == 'option':
            obj_ = option.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.option.append(obj_)
            obj_.original_tagname_ = 'option'
# end class options


class option(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, optionCode=None, optionDesc=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.optionCode = optionCode
        self.optionCode_nsprefix_ = None
        self.optionDesc = optionDesc
        self.optionDesc_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, option)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if option.subclass:
            return option.subclass(*args_, **kwargs_)
        else:
            return option(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_optionCode(self):
        return self.optionCode
    def set_optionCode(self, optionCode):
        self.optionCode = optionCode
    def get_optionDesc(self):
        return self.optionDesc
    def set_optionDesc(self, optionDesc):
        self.optionDesc = optionDesc
    def hasContent_(self):
        if (
            self.optionCode is not None or
            self.optionDesc is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='option', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('option')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'option':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='option')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='option', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='option'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='option', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.optionCode is not None:
            namespaceprefix_ = self.optionCode_nsprefix_ + ':' if (UseCapturedNS_ and self.optionCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%soptionCode>%s</%soptionCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.optionCode), input_name='optionCode')), namespaceprefix_ , eol_))
        if self.optionDesc is not None:
            namespaceprefix_ = self.optionDesc_nsprefix_ + ':' if (UseCapturedNS_ and self.optionDesc_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%soptionDesc>%s</%soptionDesc>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.optionDesc), input_name='optionDesc')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'optionCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'optionCode')
            value_ = self.gds_validate_string(value_, node, 'optionCode')
            self.optionCode = value_
            self.optionCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'optionDesc':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'optionDesc')
            value_ = self.gds_validate_string(value_, node, 'optionDesc')
            self.optionDesc = value_
            self.optionDesc_nsprefix_ = child_.prefix
# end class option


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
        rootTag = 'document'
        rootClass = document
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
        rootTag = 'document'
        rootClass = document
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
        rootTag = 'document'
        rootClass = document
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
        rootTag = 'document'
        rootClass = document
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from pricing_response import *\n\n')
        sys.stdout.write('import pricing_response as model_\n\n')
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
    "brokenRule",
    "chargeElement",
    "chargeElements",
    "document",
    "errors",
    "option",
    "options",
    "parseError",
    "priceResponse",
    "product",
    "ratedService",
    "ratedServices",
    "runtimeError"
]
