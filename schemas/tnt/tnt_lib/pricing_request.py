#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Wed Feb 24 19:49:29 2021 by generateDS.py version 2.37.16.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './tnt_lib/pricing_request.py')
#
# Command line arguments:
#   ./schemas/pricing_request.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./tnt_lib/pricing_request.py" ./schemas/pricing_request.xsd
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


class priceRequest(GeneratedsSuper):
    """PriceRequest input XSD. Version 3.0"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, appId=None, appVersion=None, priceCheck=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.appId = appId
        self.appId_nsprefix_ = None
        self.appVersion = appVersion
        self.appVersion_nsprefix_ = None
        if priceCheck is None:
            self.priceCheck = []
        else:
            self.priceCheck = priceCheck
        self.priceCheck_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, priceRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if priceRequest.subclass:
            return priceRequest.subclass(*args_, **kwargs_)
        else:
            return priceRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_appId(self):
        return self.appId
    def set_appId(self, appId):
        self.appId = appId
    def get_appVersion(self):
        return self.appVersion
    def set_appVersion(self, appVersion):
        self.appVersion = appVersion
    def get_priceCheck(self):
        return self.priceCheck
    def set_priceCheck(self, priceCheck):
        self.priceCheck = priceCheck
    def add_priceCheck(self, value):
        self.priceCheck.append(value)
    def insert_priceCheck_at(self, index, value):
        self.priceCheck.insert(index, value)
    def replace_priceCheck_at(self, index, value):
        self.priceCheck[index] = value
    def hasContent_(self):
        if (
            self.appId is not None or
            self.appVersion is not None or
            self.priceCheck
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='priceRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('priceRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'priceRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='priceRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='priceRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='priceRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='priceRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.appId is not None:
            namespaceprefix_ = self.appId_nsprefix_ + ':' if (UseCapturedNS_ and self.appId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sappId>%s</%sappId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.appId), input_name='appId')), namespaceprefix_ , eol_))
        if self.appVersion is not None:
            namespaceprefix_ = self.appVersion_nsprefix_ + ':' if (UseCapturedNS_ and self.appVersion_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sappVersion>%s</%sappVersion>%s' % (namespaceprefix_ , self.gds_format_decimal(self.appVersion, input_name='appVersion'), namespaceprefix_ , eol_))
        for priceCheck_ in self.priceCheck:
            namespaceprefix_ = self.priceCheck_nsprefix_ + ':' if (UseCapturedNS_ and self.priceCheck_nsprefix_) else ''
            priceCheck_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='priceCheck', pretty_print=pretty_print)
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
        if nodeName_ == 'appId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'appId')
            value_ = self.gds_validate_string(value_, node, 'appId')
            self.appId = value_
            self.appId_nsprefix_ = child_.prefix
        elif nodeName_ == 'appVersion' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'appVersion')
            fval_ = self.gds_validate_decimal(fval_, node, 'appVersion')
            self.appVersion = fval_
            self.appVersion_nsprefix_ = child_.prefix
        elif nodeName_ == 'priceCheck':
            obj_ = priceCheck.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.priceCheck.append(obj_)
            obj_.original_tagname_ = 'priceCheck'
# end class priceRequest


class priceCheck(GeneratedsSuper):
    """The priceCheck container element represents a single request for a price
    request. Multiple price
    requests,
    each one in a priceCheck element may be submitted. The
    information within this element will be used to
    validate
    the addresses, determine the services,
    and produce the estimate costs for the shipment."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, rateId=None, sender=None, delivery=None, collectionDateTime=None, product=None, account=None, insurance=None, termsOfPayment=None, currency=None, priceBreakDown=False, consignmentDetails=None, pieceLine=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.rateId = rateId
        self.rateId_nsprefix_ = None
        self.sender = sender
        self.sender_nsprefix_ = None
        self.delivery = delivery
        self.delivery_nsprefix_ = None
        if isinstance(collectionDateTime, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(collectionDateTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = collectionDateTime
        self.collectionDateTime = initvalue_
        self.collectionDateTime_nsprefix_ = None
        self.product = product
        self.product_nsprefix_ = None
        self.account = account
        self.account_nsprefix_ = None
        self.insurance = insurance
        self.insurance_nsprefix_ = None
        self.termsOfPayment = termsOfPayment
        self.termsOfPayment_nsprefix_ = None
        self.currency = currency
        self.currency_nsprefix_ = None
        self.priceBreakDown = priceBreakDown
        self.priceBreakDown_nsprefix_ = None
        self.consignmentDetails = consignmentDetails
        self.consignmentDetails_nsprefix_ = None
        if pieceLine is None:
            self.pieceLine = []
        else:
            self.pieceLine = pieceLine
        self.pieceLine_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, priceCheck)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if priceCheck.subclass:
            return priceCheck.subclass(*args_, **kwargs_)
        else:
            return priceCheck(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_rateId(self):
        return self.rateId
    def set_rateId(self, rateId):
        self.rateId = rateId
    def get_sender(self):
        return self.sender
    def set_sender(self, sender):
        self.sender = sender
    def get_delivery(self):
        return self.delivery
    def set_delivery(self, delivery):
        self.delivery = delivery
    def get_collectionDateTime(self):
        return self.collectionDateTime
    def set_collectionDateTime(self, collectionDateTime):
        self.collectionDateTime = collectionDateTime
    def get_product(self):
        return self.product
    def set_product(self, product):
        self.product = product
    def get_account(self):
        return self.account
    def set_account(self, account):
        self.account = account
    def get_insurance(self):
        return self.insurance
    def set_insurance(self, insurance):
        self.insurance = insurance
    def get_termsOfPayment(self):
        return self.termsOfPayment
    def set_termsOfPayment(self, termsOfPayment):
        self.termsOfPayment = termsOfPayment
    def get_currency(self):
        return self.currency
    def set_currency(self, currency):
        self.currency = currency
    def get_priceBreakDown(self):
        return self.priceBreakDown
    def set_priceBreakDown(self, priceBreakDown):
        self.priceBreakDown = priceBreakDown
    def get_consignmentDetails(self):
        return self.consignmentDetails
    def set_consignmentDetails(self, consignmentDetails):
        self.consignmentDetails = consignmentDetails
    def get_pieceLine(self):
        return self.pieceLine
    def set_pieceLine(self, pieceLine):
        self.pieceLine = pieceLine
    def add_pieceLine(self, value):
        self.pieceLine.append(value)
    def insert_pieceLine_at(self, index, value):
        self.pieceLine.insert(index, value)
    def replace_pieceLine_at(self, index, value):
        self.pieceLine[index] = value
    def hasContent_(self):
        if (
            self.rateId is not None or
            self.sender is not None or
            self.delivery is not None or
            self.collectionDateTime is not None or
            self.product is not None or
            self.account is not None or
            self.insurance is not None or
            self.termsOfPayment is not None or
            self.currency is not None or
            self.priceBreakDown or
            self.consignmentDetails is not None or
            self.pieceLine
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='priceCheck', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('priceCheck')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'priceCheck':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='priceCheck')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='priceCheck', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='priceCheck'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='priceCheck', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.rateId is not None:
            namespaceprefix_ = self.rateId_nsprefix_ + ':' if (UseCapturedNS_ and self.rateId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%srateId>%s</%srateId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.rateId), input_name='rateId')), namespaceprefix_ , eol_))
        if self.sender is not None:
            namespaceprefix_ = self.sender_nsprefix_ + ':' if (UseCapturedNS_ and self.sender_nsprefix_) else ''
            self.sender.export(outfile, level, namespaceprefix_, namespacedef_='', name_='sender', pretty_print=pretty_print)
        if self.delivery is not None:
            namespaceprefix_ = self.delivery_nsprefix_ + ':' if (UseCapturedNS_ and self.delivery_nsprefix_) else ''
            self.delivery.export(outfile, level, namespaceprefix_, namespacedef_='', name_='delivery', pretty_print=pretty_print)
        if self.collectionDateTime is not None:
            namespaceprefix_ = self.collectionDateTime_nsprefix_ + ':' if (UseCapturedNS_ and self.collectionDateTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scollectionDateTime>%s</%scollectionDateTime>%s' % (namespaceprefix_ , self.gds_format_datetime(self.collectionDateTime, input_name='collectionDateTime'), namespaceprefix_ , eol_))
        if self.product is not None:
            namespaceprefix_ = self.product_nsprefix_ + ':' if (UseCapturedNS_ and self.product_nsprefix_) else ''
            self.product.export(outfile, level, namespaceprefix_, namespacedef_='', name_='product', pretty_print=pretty_print)
        if self.account is not None:
            namespaceprefix_ = self.account_nsprefix_ + ':' if (UseCapturedNS_ and self.account_nsprefix_) else ''
            self.account.export(outfile, level, namespaceprefix_, namespacedef_='', name_='account', pretty_print=pretty_print)
        if self.insurance is not None:
            namespaceprefix_ = self.insurance_nsprefix_ + ':' if (UseCapturedNS_ and self.insurance_nsprefix_) else ''
            self.insurance.export(outfile, level, namespaceprefix_, namespacedef_='', name_='insurance', pretty_print=pretty_print)
        if self.termsOfPayment is not None:
            namespaceprefix_ = self.termsOfPayment_nsprefix_ + ':' if (UseCapturedNS_ and self.termsOfPayment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stermsOfPayment>%s</%stermsOfPayment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.termsOfPayment), input_name='termsOfPayment')), namespaceprefix_ , eol_))
        if self.currency is not None:
            namespaceprefix_ = self.currency_nsprefix_ + ':' if (UseCapturedNS_ and self.currency_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scurrency>%s</%scurrency>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.currency), input_name='currency')), namespaceprefix_ , eol_))
        if self.priceBreakDown:
            namespaceprefix_ = self.priceBreakDown_nsprefix_ + ':' if (UseCapturedNS_ and self.priceBreakDown_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spriceBreakDown>%s</%spriceBreakDown>%s' % (namespaceprefix_ , self.gds_format_boolean(self.priceBreakDown, input_name='priceBreakDown'), namespaceprefix_ , eol_))
        if self.consignmentDetails is not None:
            namespaceprefix_ = self.consignmentDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.consignmentDetails_nsprefix_) else ''
            self.consignmentDetails.export(outfile, level, namespaceprefix_, namespacedef_='', name_='consignmentDetails', pretty_print=pretty_print)
        for pieceLine_ in self.pieceLine:
            namespaceprefix_ = self.pieceLine_nsprefix_ + ':' if (UseCapturedNS_ and self.pieceLine_nsprefix_) else ''
            pieceLine_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='pieceLine', pretty_print=pretty_print)
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
        elif nodeName_ == 'sender':
            obj_ = address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.sender = obj_
            obj_.original_tagname_ = 'sender'
        elif nodeName_ == 'delivery':
            obj_ = address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.delivery = obj_
            obj_.original_tagname_ = 'delivery'
        elif nodeName_ == 'collectionDateTime':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.collectionDateTime = dval_
            self.collectionDateTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'product':
            obj_ = product.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.product = obj_
            obj_.original_tagname_ = 'product'
        elif nodeName_ == 'account':
            obj_ = account.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.account = obj_
            obj_.original_tagname_ = 'account'
        elif nodeName_ == 'insurance':
            obj_ = insurance.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.insurance = obj_
            obj_.original_tagname_ = 'insurance'
        elif nodeName_ == 'termsOfPayment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'termsOfPayment')
            value_ = self.gds_validate_string(value_, node, 'termsOfPayment')
            self.termsOfPayment = value_
            self.termsOfPayment_nsprefix_ = child_.prefix
        elif nodeName_ == 'currency':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'currency')
            value_ = self.gds_validate_string(value_, node, 'currency')
            self.currency = value_
            self.currency_nsprefix_ = child_.prefix
        elif nodeName_ == 'priceBreakDown':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'priceBreakDown')
            ival_ = self.gds_validate_boolean(ival_, node, 'priceBreakDown')
            self.priceBreakDown = ival_
            self.priceBreakDown_nsprefix_ = child_.prefix
        elif nodeName_ == 'consignmentDetails':
            obj_ = consignmentDetails.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.consignmentDetails = obj_
            obj_.original_tagname_ = 'consignmentDetails'
        elif nodeName_ == 'pieceLine':
            obj_ = pieceLine.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.pieceLine.append(obj_)
            obj_.original_tagname_ = 'pieceLine'
# end class priceCheck


class address(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, country=None, town=None, postcode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.country = country
        self.country_nsprefix_ = None
        self.town = town
        self.town_nsprefix_ = None
        self.postcode = postcode
        self.postcode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, address)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if address.subclass:
            return address.subclass(*args_, **kwargs_)
        else:
            return address(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_country(self):
        return self.country
    def set_country(self, country):
        self.country = country
    def get_town(self):
        return self.town
    def set_town(self, town):
        self.town = town
    def get_postcode(self):
        return self.postcode
    def set_postcode(self, postcode):
        self.postcode = postcode
    def hasContent_(self):
        if (
            self.country is not None or
            self.town is not None or
            self.postcode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='address', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('address')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'address':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='address')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='address', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='address'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='address', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.country is not None:
            namespaceprefix_ = self.country_nsprefix_ + ':' if (UseCapturedNS_ and self.country_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scountry>%s</%scountry>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.country), input_name='country')), namespaceprefix_ , eol_))
        if self.town is not None:
            namespaceprefix_ = self.town_nsprefix_ + ':' if (UseCapturedNS_ and self.town_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stown>%s</%stown>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.town), input_name='town')), namespaceprefix_ , eol_))
        if self.postcode is not None:
            namespaceprefix_ = self.postcode_nsprefix_ + ':' if (UseCapturedNS_ and self.postcode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spostcode>%s</%spostcode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.postcode), input_name='postcode')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'country':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'country')
            value_ = self.gds_validate_string(value_, node, 'country')
            self.country = value_
            self.country_nsprefix_ = child_.prefix
        elif nodeName_ == 'town':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'town')
            value_ = self.gds_validate_string(value_, node, 'town')
            self.town = value_
            self.town_nsprefix_ = child_.prefix
        elif nodeName_ == 'postcode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'postcode')
            value_ = self.gds_validate_string(value_, node, 'postcode')
            self.postcode = value_
            self.postcode_nsprefix_ = child_.prefix
# end class address


class account(GeneratedsSuper):
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
        self.accountNumber_nsprefix_ = None
        self.accountCountry = accountCountry
        self.accountCountry_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, account)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if account.subclass:
            return account.subclass(*args_, **kwargs_)
        else:
            return account(*args_, **kwargs_)
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
    def hasContent_(self):
        if (
            self.accountNumber is not None or
            self.accountCountry is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='account', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('account')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'account':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='account')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='account', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='account'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='account', fromsubclass_=False, pretty_print=True):
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
        elif nodeName_ == 'accountCountry':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'accountCountry')
            value_ = self.gds_validate_string(value_, node, 'accountCountry')
            self.accountCountry = value_
            self.accountCountry_nsprefix_ = child_.prefix
# end class account


class insurance(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, insuranceValue=None, goodsValue=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.insuranceValue = insuranceValue
        self.insuranceValue_nsprefix_ = None
        self.goodsValue = goodsValue
        self.goodsValue_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, insurance)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if insurance.subclass:
            return insurance.subclass(*args_, **kwargs_)
        else:
            return insurance(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_insuranceValue(self):
        return self.insuranceValue
    def set_insuranceValue(self, insuranceValue):
        self.insuranceValue = insuranceValue
    def get_goodsValue(self):
        return self.goodsValue
    def set_goodsValue(self, goodsValue):
        self.goodsValue = goodsValue
    def hasContent_(self):
        if (
            self.insuranceValue is not None or
            self.goodsValue is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='insurance', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('insurance')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'insurance':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='insurance')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='insurance', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='insurance'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='insurance', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.insuranceValue is not None:
            namespaceprefix_ = self.insuranceValue_nsprefix_ + ':' if (UseCapturedNS_ and self.insuranceValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sinsuranceValue>%s</%sinsuranceValue>%s' % (namespaceprefix_ , self.gds_format_decimal(self.insuranceValue, input_name='insuranceValue'), namespaceprefix_ , eol_))
        if self.goodsValue is not None:
            namespaceprefix_ = self.goodsValue_nsprefix_ + ':' if (UseCapturedNS_ and self.goodsValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sgoodsValue>%s</%sgoodsValue>%s' % (namespaceprefix_ , self.gds_format_decimal(self.goodsValue, input_name='goodsValue'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'insuranceValue' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'insuranceValue')
            fval_ = self.gds_validate_decimal(fval_, node, 'insuranceValue')
            self.insuranceValue = fval_
            self.insuranceValue_nsprefix_ = child_.prefix
        elif nodeName_ == 'goodsValue' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'goodsValue')
            fval_ = self.gds_validate_decimal(fval_, node, 'goodsValue')
            self.goodsValue = fval_
            self.goodsValue_nsprefix_ = child_.prefix
# end class insurance


class consignmentDetails(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, totalWeight=None, totalVolume=None, totalNumberOfPieces=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.totalWeight = totalWeight
        self.totalWeight_nsprefix_ = None
        self.totalVolume = totalVolume
        self.totalVolume_nsprefix_ = None
        self.totalNumberOfPieces = totalNumberOfPieces
        self.totalNumberOfPieces_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, consignmentDetails)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if consignmentDetails.subclass:
            return consignmentDetails.subclass(*args_, **kwargs_)
        else:
            return consignmentDetails(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_totalWeight(self):
        return self.totalWeight
    def set_totalWeight(self, totalWeight):
        self.totalWeight = totalWeight
    def get_totalVolume(self):
        return self.totalVolume
    def set_totalVolume(self, totalVolume):
        self.totalVolume = totalVolume
    def get_totalNumberOfPieces(self):
        return self.totalNumberOfPieces
    def set_totalNumberOfPieces(self, totalNumberOfPieces):
        self.totalNumberOfPieces = totalNumberOfPieces
    def hasContent_(self):
        if (
            self.totalWeight is not None or
            self.totalVolume is not None or
            self.totalNumberOfPieces is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='consignmentDetails', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('consignmentDetails')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'consignmentDetails':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='consignmentDetails')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='consignmentDetails', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='consignmentDetails'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='consignmentDetails', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.totalWeight is not None:
            namespaceprefix_ = self.totalWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.totalWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stotalWeight>%s</%stotalWeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.totalWeight, input_name='totalWeight'), namespaceprefix_ , eol_))
        if self.totalVolume is not None:
            namespaceprefix_ = self.totalVolume_nsprefix_ + ':' if (UseCapturedNS_ and self.totalVolume_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stotalVolume>%s</%stotalVolume>%s' % (namespaceprefix_ , self.gds_format_decimal(self.totalVolume, input_name='totalVolume'), namespaceprefix_ , eol_))
        if self.totalNumberOfPieces is not None:
            namespaceprefix_ = self.totalNumberOfPieces_nsprefix_ + ':' if (UseCapturedNS_ and self.totalNumberOfPieces_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stotalNumberOfPieces>%s</%stotalNumberOfPieces>%s' % (namespaceprefix_ , self.gds_format_integer(self.totalNumberOfPieces, input_name='totalNumberOfPieces'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'totalWeight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'totalWeight')
            fval_ = self.gds_validate_decimal(fval_, node, 'totalWeight')
            self.totalWeight = fval_
            self.totalWeight_nsprefix_ = child_.prefix
        elif nodeName_ == 'totalVolume' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'totalVolume')
            fval_ = self.gds_validate_decimal(fval_, node, 'totalVolume')
            self.totalVolume = fval_
            self.totalVolume_nsprefix_ = child_.prefix
        elif nodeName_ == 'totalNumberOfPieces' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'totalNumberOfPieces')
            ival_ = self.gds_validate_integer(ival_, node, 'totalNumberOfPieces')
            self.totalNumberOfPieces = ival_
            self.totalNumberOfPieces_nsprefix_ = child_.prefix
# end class consignmentDetails


class pieceLine(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, numberOfPieces=None, pieceMeasurements=None, pallet=False, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.numberOfPieces = numberOfPieces
        self.numberOfPieces_nsprefix_ = None
        self.pieceMeasurements = pieceMeasurements
        self.pieceMeasurements_nsprefix_ = None
        self.pallet = pallet
        self.pallet_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, pieceLine)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if pieceLine.subclass:
            return pieceLine.subclass(*args_, **kwargs_)
        else:
            return pieceLine(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_numberOfPieces(self):
        return self.numberOfPieces
    def set_numberOfPieces(self, numberOfPieces):
        self.numberOfPieces = numberOfPieces
    def get_pieceMeasurements(self):
        return self.pieceMeasurements
    def set_pieceMeasurements(self, pieceMeasurements):
        self.pieceMeasurements = pieceMeasurements
    def get_pallet(self):
        return self.pallet
    def set_pallet(self, pallet):
        self.pallet = pallet
    def hasContent_(self):
        if (
            self.numberOfPieces is not None or
            self.pieceMeasurements is not None or
            self.pallet
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='pieceLine', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('pieceLine')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'pieceLine':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='pieceLine')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='pieceLine', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='pieceLine'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='pieceLine', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.numberOfPieces is not None:
            namespaceprefix_ = self.numberOfPieces_nsprefix_ + ':' if (UseCapturedNS_ and self.numberOfPieces_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snumberOfPieces>%s</%snumberOfPieces>%s' % (namespaceprefix_ , self.gds_format_integer(self.numberOfPieces, input_name='numberOfPieces'), namespaceprefix_ , eol_))
        if self.pieceMeasurements is not None:
            namespaceprefix_ = self.pieceMeasurements_nsprefix_ + ':' if (UseCapturedNS_ and self.pieceMeasurements_nsprefix_) else ''
            self.pieceMeasurements.export(outfile, level, namespaceprefix_, namespacedef_='', name_='pieceMeasurements', pretty_print=pretty_print)
        if self.pallet is not None:
            namespaceprefix_ = self.pallet_nsprefix_ + ':' if (UseCapturedNS_ and self.pallet_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spallet>%s</%spallet>%s' % (namespaceprefix_ , self.gds_format_boolean(self.pallet, input_name='pallet'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'numberOfPieces' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'numberOfPieces')
            ival_ = self.gds_validate_integer(ival_, node, 'numberOfPieces')
            self.numberOfPieces = ival_
            self.numberOfPieces_nsprefix_ = child_.prefix
        elif nodeName_ == 'pieceMeasurements':
            obj_ = pieceMeasurements.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.pieceMeasurements = obj_
            obj_.original_tagname_ = 'pieceMeasurements'
        elif nodeName_ == 'pallet':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'pallet')
            ival_ = self.gds_validate_boolean(ival_, node, 'pallet')
            self.pallet = ival_
            self.pallet_nsprefix_ = child_.prefix
# end class pieceLine


class pieceMeasurements(GeneratedsSuper):
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
        self.length_nsprefix_ = None
        self.width = width
        self.width_nsprefix_ = None
        self.height = height
        self.height_nsprefix_ = None
        self.weight = weight
        self.weight_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, pieceMeasurements)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if pieceMeasurements.subclass:
            return pieceMeasurements.subclass(*args_, **kwargs_)
        else:
            return pieceMeasurements(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='pieceMeasurements', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('pieceMeasurements')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'pieceMeasurements':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='pieceMeasurements')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='pieceMeasurements', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='pieceMeasurements'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='pieceMeasurements', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.length is not None:
            namespaceprefix_ = self.length_nsprefix_ + ':' if (UseCapturedNS_ and self.length_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slength>%s</%slength>%s' % (namespaceprefix_ , self.gds_format_decimal(self.length, input_name='length'), namespaceprefix_ , eol_))
        if self.width is not None:
            namespaceprefix_ = self.width_nsprefix_ + ':' if (UseCapturedNS_ and self.width_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%swidth>%s</%swidth>%s' % (namespaceprefix_ , self.gds_format_decimal(self.width, input_name='width'), namespaceprefix_ , eol_))
        if self.height is not None:
            namespaceprefix_ = self.height_nsprefix_ + ':' if (UseCapturedNS_ and self.height_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sheight>%s</%sheight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.height, input_name='height'), namespaceprefix_ , eol_))
        if self.weight is not None:
            namespaceprefix_ = self.weight_nsprefix_ + ':' if (UseCapturedNS_ and self.weight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sweight>%s</%sweight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.weight, input_name='weight'), namespaceprefix_ , eol_))
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
            fval_ = self.gds_parse_decimal(sval_, node, 'length')
            fval_ = self.gds_validate_decimal(fval_, node, 'length')
            self.length = fval_
            self.length_nsprefix_ = child_.prefix
        elif nodeName_ == 'width' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'width')
            fval_ = self.gds_validate_decimal(fval_, node, 'width')
            self.width = fval_
            self.width_nsprefix_ = child_.prefix
        elif nodeName_ == 'height' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'height')
            fval_ = self.gds_validate_decimal(fval_, node, 'height')
            self.height = fval_
            self.height_nsprefix_ = child_.prefix
        elif nodeName_ == 'weight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'weight')
            fval_ = self.gds_validate_decimal(fval_, node, 'weight')
            self.weight = fval_
            self.weight_nsprefix_ = child_.prefix
# end class pieceMeasurements


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
        rootTag = 'priceRequest'
        rootClass = priceRequest
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
        rootTag = 'priceRequest'
        rootClass = priceRequest
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
        rootTag = 'priceRequest'
        rootClass = priceRequest
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
        rootTag = 'priceRequest'
        rootClass = priceRequest
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from pricing_request import *\n\n')
        sys.stdout.write('import pricing_request as model_\n\n')
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
    "account",
    "address",
    "consignmentDetails",
    "insurance",
    "option",
    "options",
    "pieceLine",
    "pieceMeasurements",
    "priceCheck",
    "priceRequest",
    "product"
]
