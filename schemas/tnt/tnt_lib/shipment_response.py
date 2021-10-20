#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Wed Feb 24 19:49:29 2021 by generateDS.py version 2.37.16.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './tnt_lib/shipment_response.py')
#
# Command line arguments:
#   ./schemas/shipment_response.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./tnt_lib/shipment_response.py" ./schemas/shipment_response.xsd
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
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GROUPCODE=None, CREATE=None, RATE=None, BOOK=None, SHIP=None, PRINT=None, ERROR=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GROUPCODE = GROUPCODE
        self.GROUPCODE_nsprefix_ = None
        if CREATE is None:
            self.CREATE = []
        else:
            self.CREATE = CREATE
        self.CREATE_nsprefix_ = None
        self.RATE = RATE
        self.RATE_nsprefix_ = None
        self.BOOK = BOOK
        self.BOOK_nsprefix_ = None
        self.SHIP = SHIP
        self.SHIP_nsprefix_ = None
        self.PRINT = PRINT
        self.PRINT_nsprefix_ = None
        if ERROR is None:
            self.ERROR = []
        else:
            self.ERROR = ERROR
        self.ERROR_nsprefix_ = None
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
    def get_GROUPCODE(self):
        return self.GROUPCODE
    def set_GROUPCODE(self, GROUPCODE):
        self.GROUPCODE = GROUPCODE
    def get_CREATE(self):
        return self.CREATE
    def set_CREATE(self, CREATE):
        self.CREATE = CREATE
    def add_CREATE(self, value):
        self.CREATE.append(value)
    def insert_CREATE_at(self, index, value):
        self.CREATE.insert(index, value)
    def replace_CREATE_at(self, index, value):
        self.CREATE[index] = value
    def get_RATE(self):
        return self.RATE
    def set_RATE(self, RATE):
        self.RATE = RATE
    def get_BOOK(self):
        return self.BOOK
    def set_BOOK(self, BOOK):
        self.BOOK = BOOK
    def get_SHIP(self):
        return self.SHIP
    def set_SHIP(self, SHIP):
        self.SHIP = SHIP
    def get_PRINT(self):
        return self.PRINT
    def set_PRINT(self, PRINT):
        self.PRINT = PRINT
    def get_ERROR(self):
        return self.ERROR
    def set_ERROR(self, ERROR):
        self.ERROR = ERROR
    def add_ERROR(self, value):
        self.ERROR.append(value)
    def insert_ERROR_at(self, index, value):
        self.ERROR.insert(index, value)
    def replace_ERROR_at(self, index, value):
        self.ERROR[index] = value
    def hasContent_(self):
        if (
            self.GROUPCODE is not None or
            self.CREATE or
            self.RATE is not None or
            self.BOOK is not None or
            self.SHIP is not None or
            self.PRINT is not None or
            self.ERROR
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
        if self.GROUPCODE is not None:
            namespaceprefix_ = self.GROUPCODE_nsprefix_ + ':' if (UseCapturedNS_ and self.GROUPCODE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGROUPCODE>%s</%sGROUPCODE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GROUPCODE), input_name='GROUPCODE')), namespaceprefix_ , eol_))
        for CREATE_ in self.CREATE:
            namespaceprefix_ = self.CREATE_nsprefix_ + ':' if (UseCapturedNS_ and self.CREATE_nsprefix_) else ''
            CREATE_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CREATE', pretty_print=pretty_print)
        if self.RATE is not None:
            namespaceprefix_ = self.RATE_nsprefix_ + ':' if (UseCapturedNS_ and self.RATE_nsprefix_) else ''
            self.RATE.export(outfile, level, namespaceprefix_, namespacedef_='', name_='RATE', pretty_print=pretty_print)
        if self.BOOK is not None:
            namespaceprefix_ = self.BOOK_nsprefix_ + ':' if (UseCapturedNS_ and self.BOOK_nsprefix_) else ''
            self.BOOK.export(outfile, level, namespaceprefix_, namespacedef_='', name_='BOOK', pretty_print=pretty_print)
        if self.SHIP is not None:
            namespaceprefix_ = self.SHIP_nsprefix_ + ':' if (UseCapturedNS_ and self.SHIP_nsprefix_) else ''
            self.SHIP.export(outfile, level, namespaceprefix_, namespacedef_='', name_='SHIP', pretty_print=pretty_print)
        if self.PRINT is not None:
            namespaceprefix_ = self.PRINT_nsprefix_ + ':' if (UseCapturedNS_ and self.PRINT_nsprefix_) else ''
            self.PRINT.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PRINT', pretty_print=pretty_print)
        for ERROR_ in self.ERROR:
            namespaceprefix_ = self.ERROR_nsprefix_ + ':' if (UseCapturedNS_ and self.ERROR_nsprefix_) else ''
            ERROR_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ERROR', pretty_print=pretty_print)
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
        if nodeName_ == 'GROUPCODE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GROUPCODE')
            value_ = self.gds_validate_string(value_, node, 'GROUPCODE')
            self.GROUPCODE = value_
            self.GROUPCODE_nsprefix_ = child_.prefix
        elif nodeName_ == 'CREATE':
            obj_ = CREATE.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CREATE.append(obj_)
            obj_.original_tagname_ = 'CREATE'
        elif nodeName_ == 'RATE':
            obj_ = RATE.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.RATE = obj_
            obj_.original_tagname_ = 'RATE'
        elif nodeName_ == 'BOOK':
            obj_ = BOOK.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BOOK = obj_
            obj_.original_tagname_ = 'BOOK'
        elif nodeName_ == 'SHIP':
            obj_ = SHIP.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SHIP = obj_
            obj_.original_tagname_ = 'SHIP'
        elif nodeName_ == 'PRINT':
            obj_ = PRINT.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PRINT = obj_
            obj_.original_tagname_ = 'PRINT'
        elif nodeName_ == 'ERROR':
            obj_ = ERROR.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ERROR.append(obj_)
            obj_.original_tagname_ = 'ERROR'
# end class document


class runtime_error(GeneratedsSuper):
    """The runtime error messages returned by
    ExpressConnect e.g. login details not recognised"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, error_reason=None, error_srcText=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.error_reason = error_reason
        self.error_reason_nsprefix_ = None
        self.error_srcText = error_srcText
        self.error_srcText_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, runtime_error)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if runtime_error.subclass:
            return runtime_error.subclass(*args_, **kwargs_)
        else:
            return runtime_error(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_error_reason(self):
        return self.error_reason
    def set_error_reason(self, error_reason):
        self.error_reason = error_reason
    def get_error_srcText(self):
        return self.error_srcText
    def set_error_srcText(self, error_srcText):
        self.error_srcText = error_srcText
    def hasContent_(self):
        if (
            self.error_reason is not None or
            self.error_srcText is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='runtime_error', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('runtime_error')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'runtime_error':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='runtime_error')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='runtime_error', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='runtime_error'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='runtime_error', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.error_reason is not None:
            namespaceprefix_ = self.error_reason_nsprefix_ + ':' if (UseCapturedNS_ and self.error_reason_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%serror_reason>%s</%serror_reason>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.error_reason), input_name='error_reason')), namespaceprefix_ , eol_))
        if self.error_srcText is not None:
            namespaceprefix_ = self.error_srcText_nsprefix_ + ':' if (UseCapturedNS_ and self.error_srcText_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%serror_srcText>%s</%serror_srcText>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.error_srcText), input_name='error_srcText')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'error_reason':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'error_reason')
            value_ = self.gds_validate_string(value_, node, 'error_reason')
            self.error_reason = value_
            self.error_reason_nsprefix_ = child_.prefix
        elif nodeName_ == 'error_srcText':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'error_srcText')
            value_ = self.gds_validate_string(value_, node, 'error_srcText')
            self.error_srcText = value_
            self.error_srcText_nsprefix_ = child_.prefix
# end class runtime_error


class parse_error(GeneratedsSuper):
    """The XML parse error messages returned by
    ExpressConnect e.g. Element content is invalid according to the
    DTD/Schema."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, error_reason=None, error_line=None, error_linepos=None, error_srcText=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.error_reason = error_reason
        self.error_reason_nsprefix_ = None
        self.error_line = error_line
        self.error_line_nsprefix_ = None
        self.error_linepos = error_linepos
        self.error_linepos_nsprefix_ = None
        self.error_srcText = error_srcText
        self.error_srcText_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, parse_error)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if parse_error.subclass:
            return parse_error.subclass(*args_, **kwargs_)
        else:
            return parse_error(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_error_reason(self):
        return self.error_reason
    def set_error_reason(self, error_reason):
        self.error_reason = error_reason
    def get_error_line(self):
        return self.error_line
    def set_error_line(self, error_line):
        self.error_line = error_line
    def get_error_linepos(self):
        return self.error_linepos
    def set_error_linepos(self, error_linepos):
        self.error_linepos = error_linepos
    def get_error_srcText(self):
        return self.error_srcText
    def set_error_srcText(self, error_srcText):
        self.error_srcText = error_srcText
    def hasContent_(self):
        if (
            self.error_reason is not None or
            self.error_line is not None or
            self.error_linepos is not None or
            self.error_srcText is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='parse_error', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('parse_error')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'parse_error':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='parse_error')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='parse_error', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='parse_error'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='parse_error', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.error_reason is not None:
            namespaceprefix_ = self.error_reason_nsprefix_ + ':' if (UseCapturedNS_ and self.error_reason_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%serror_reason>%s</%serror_reason>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.error_reason), input_name='error_reason')), namespaceprefix_ , eol_))
        if self.error_line is not None:
            namespaceprefix_ = self.error_line_nsprefix_ + ':' if (UseCapturedNS_ and self.error_line_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%serror_line>%s</%serror_line>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.error_line), input_name='error_line')), namespaceprefix_ , eol_))
        if self.error_linepos is not None:
            namespaceprefix_ = self.error_linepos_nsprefix_ + ':' if (UseCapturedNS_ and self.error_linepos_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%serror_linepos>%s</%serror_linepos>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.error_linepos), input_name='error_linepos')), namespaceprefix_ , eol_))
        if self.error_srcText is not None:
            namespaceprefix_ = self.error_srcText_nsprefix_ + ':' if (UseCapturedNS_ and self.error_srcText_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%serror_srcText>%s</%serror_srcText>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.error_srcText), input_name='error_srcText')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'error_reason':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'error_reason')
            value_ = self.gds_validate_string(value_, node, 'error_reason')
            self.error_reason = value_
            self.error_reason_nsprefix_ = child_.prefix
        elif nodeName_ == 'error_line':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'error_line')
            value_ = self.gds_validate_string(value_, node, 'error_line')
            self.error_line = value_
            self.error_line_nsprefix_ = child_.prefix
        elif nodeName_ == 'error_linepos':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'error_linepos')
            value_ = self.gds_validate_string(value_, node, 'error_linepos')
            self.error_linepos = value_
            self.error_linepos_nsprefix_ = child_.prefix
        elif nodeName_ == 'error_srcText':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'error_srcText')
            value_ = self.gds_validate_string(value_, node, 'error_srcText')
            self.error_srcText = value_
            self.error_srcText_nsprefix_ = child_.prefix
# end class parse_error


class ERROR(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CODE=None, DESCRIPTION=None, SOURCE=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CODE = CODE
        self.CODE_nsprefix_ = None
        self.DESCRIPTION = DESCRIPTION
        self.DESCRIPTION_nsprefix_ = None
        self.SOURCE = SOURCE
        self.SOURCE_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ERROR)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ERROR.subclass:
            return ERROR.subclass(*args_, **kwargs_)
        else:
            return ERROR(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CODE(self):
        return self.CODE
    def set_CODE(self, CODE):
        self.CODE = CODE
    def get_DESCRIPTION(self):
        return self.DESCRIPTION
    def set_DESCRIPTION(self, DESCRIPTION):
        self.DESCRIPTION = DESCRIPTION
    def get_SOURCE(self):
        return self.SOURCE
    def set_SOURCE(self, SOURCE):
        self.SOURCE = SOURCE
    def hasContent_(self):
        if (
            self.CODE is not None or
            self.DESCRIPTION is not None or
            self.SOURCE is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ERROR', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ERROR')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ERROR':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ERROR')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ERROR', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ERROR'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ERROR', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CODE is not None:
            namespaceprefix_ = self.CODE_nsprefix_ + ':' if (UseCapturedNS_ and self.CODE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCODE>%s</%sCODE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CODE), input_name='CODE')), namespaceprefix_ , eol_))
        if self.DESCRIPTION is not None:
            namespaceprefix_ = self.DESCRIPTION_nsprefix_ + ':' if (UseCapturedNS_ and self.DESCRIPTION_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDESCRIPTION>%s</%sDESCRIPTION>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DESCRIPTION), input_name='DESCRIPTION')), namespaceprefix_ , eol_))
        if self.SOURCE is not None:
            namespaceprefix_ = self.SOURCE_nsprefix_ + ':' if (UseCapturedNS_ and self.SOURCE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSOURCE>%s</%sSOURCE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SOURCE), input_name='SOURCE')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'CODE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CODE')
            value_ = self.gds_validate_string(value_, node, 'CODE')
            self.CODE = value_
            self.CODE_nsprefix_ = child_.prefix
        elif nodeName_ == 'DESCRIPTION':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DESCRIPTION')
            value_ = self.gds_validate_string(value_, node, 'DESCRIPTION')
            self.DESCRIPTION = value_
            self.DESCRIPTION_nsprefix_ = child_.prefix
        elif nodeName_ == 'SOURCE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SOURCE')
            value_ = self.gds_validate_string(value_, node, 'SOURCE')
            self.SOURCE = value_
            self.SOURCE_nsprefix_ = child_.prefix
# end class ERROR


class PRINT(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ERROR=None, CONNOTE=None, LABEL=None, MANIFEST=None, INVOICE=None, EMAILTO=None, EMAILFROM=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if ERROR is None:
            self.ERROR = []
        else:
            self.ERROR = ERROR
        self.ERROR_nsprefix_ = None
        self.CONNOTE = CONNOTE
        self.CONNOTE_nsprefix_ = None
        self.LABEL = LABEL
        self.LABEL_nsprefix_ = None
        self.MANIFEST = MANIFEST
        self.MANIFEST_nsprefix_ = None
        self.INVOICE = INVOICE
        self.INVOICE_nsprefix_ = None
        self.EMAILTO = EMAILTO
        self.EMAILTO_nsprefix_ = None
        self.EMAILFROM = EMAILFROM
        self.EMAILFROM_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PRINT)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PRINT.subclass:
            return PRINT.subclass(*args_, **kwargs_)
        else:
            return PRINT(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ERROR(self):
        return self.ERROR
    def set_ERROR(self, ERROR):
        self.ERROR = ERROR
    def add_ERROR(self, value):
        self.ERROR.append(value)
    def insert_ERROR_at(self, index, value):
        self.ERROR.insert(index, value)
    def replace_ERROR_at(self, index, value):
        self.ERROR[index] = value
    def get_CONNOTE(self):
        return self.CONNOTE
    def set_CONNOTE(self, CONNOTE):
        self.CONNOTE = CONNOTE
    def get_LABEL(self):
        return self.LABEL
    def set_LABEL(self, LABEL):
        self.LABEL = LABEL
    def get_MANIFEST(self):
        return self.MANIFEST
    def set_MANIFEST(self, MANIFEST):
        self.MANIFEST = MANIFEST
    def get_INVOICE(self):
        return self.INVOICE
    def set_INVOICE(self, INVOICE):
        self.INVOICE = INVOICE
    def get_EMAILTO(self):
        return self.EMAILTO
    def set_EMAILTO(self, EMAILTO):
        self.EMAILTO = EMAILTO
    def get_EMAILFROM(self):
        return self.EMAILFROM
    def set_EMAILFROM(self, EMAILFROM):
        self.EMAILFROM = EMAILFROM
    def hasContent_(self):
        if (
            self.ERROR or
            self.CONNOTE is not None or
            self.LABEL is not None or
            self.MANIFEST is not None or
            self.INVOICE is not None or
            self.EMAILTO is not None or
            self.EMAILFROM is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PRINT', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PRINT')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PRINT':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PRINT')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PRINT', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PRINT'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PRINT', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for ERROR_ in self.ERROR:
            namespaceprefix_ = self.ERROR_nsprefix_ + ':' if (UseCapturedNS_ and self.ERROR_nsprefix_) else ''
            ERROR_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ERROR', pretty_print=pretty_print)
        if self.CONNOTE is not None:
            namespaceprefix_ = self.CONNOTE_nsprefix_ + ':' if (UseCapturedNS_ and self.CONNOTE_nsprefix_) else ''
            self.CONNOTE.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CONNOTE', pretty_print=pretty_print)
        if self.LABEL is not None:
            namespaceprefix_ = self.LABEL_nsprefix_ + ':' if (UseCapturedNS_ and self.LABEL_nsprefix_) else ''
            self.LABEL.export(outfile, level, namespaceprefix_, namespacedef_='', name_='LABEL', pretty_print=pretty_print)
        if self.MANIFEST is not None:
            namespaceprefix_ = self.MANIFEST_nsprefix_ + ':' if (UseCapturedNS_ and self.MANIFEST_nsprefix_) else ''
            self.MANIFEST.export(outfile, level, namespaceprefix_, namespacedef_='', name_='MANIFEST', pretty_print=pretty_print)
        if self.INVOICE is not None:
            namespaceprefix_ = self.INVOICE_nsprefix_ + ':' if (UseCapturedNS_ and self.INVOICE_nsprefix_) else ''
            self.INVOICE.export(outfile, level, namespaceprefix_, namespacedef_='', name_='INVOICE', pretty_print=pretty_print)
        if self.EMAILTO is not None:
            namespaceprefix_ = self.EMAILTO_nsprefix_ + ':' if (UseCapturedNS_ and self.EMAILTO_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEMAILTO>%s</%sEMAILTO>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EMAILTO), input_name='EMAILTO')), namespaceprefix_ , eol_))
        if self.EMAILFROM is not None:
            namespaceprefix_ = self.EMAILFROM_nsprefix_ + ':' if (UseCapturedNS_ and self.EMAILFROM_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEMAILFROM>%s</%sEMAILFROM>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EMAILFROM), input_name='EMAILFROM')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ERROR':
            obj_ = ERROR.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ERROR.append(obj_)
            obj_.original_tagname_ = 'ERROR'
        elif nodeName_ == 'CONNOTE':
            obj_ = CONNOTE.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CONNOTE = obj_
            obj_.original_tagname_ = 'CONNOTE'
        elif nodeName_ == 'LABEL':
            obj_ = LABEL.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LABEL = obj_
            obj_.original_tagname_ = 'LABEL'
        elif nodeName_ == 'MANIFEST':
            obj_ = MANIFEST.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.MANIFEST = obj_
            obj_.original_tagname_ = 'MANIFEST'
        elif nodeName_ == 'INVOICE':
            obj_ = INVOICE.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.INVOICE = obj_
            obj_.original_tagname_ = 'INVOICE'
        elif nodeName_ == 'EMAILTO':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EMAILTO')
            value_ = self.gds_validate_string(value_, node, 'EMAILTO')
            self.EMAILTO = value_
            self.EMAILTO_nsprefix_ = child_.prefix
        elif nodeName_ == 'EMAILFROM':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EMAILFROM')
            value_ = self.gds_validate_string(value_, node, 'EMAILFROM')
            self.EMAILFROM = value_
            self.EMAILFROM_nsprefix_ = child_.prefix
# end class PRINT


class LABEL(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ERROR=None, valueOf_=None, mixedclass_=None, content_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if ERROR is None:
            self.ERROR = []
        else:
            self.ERROR = ERROR
        self.ERROR_nsprefix_ = None
        self.valueOf_ = valueOf_
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LABEL)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LABEL.subclass:
            return LABEL.subclass(*args_, **kwargs_)
        else:
            return LABEL(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ERROR(self):
        return self.ERROR
    def set_ERROR(self, ERROR):
        self.ERROR = ERROR
    def add_ERROR(self, value):
        self.ERROR.append(value)
    def insert_ERROR_at(self, index, value):
        self.ERROR.insert(index, value)
    def replace_ERROR_at(self, index, value):
        self.ERROR[index] = value
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def hasContent_(self):
        if (
            self.ERROR or
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_) or
            self.content_
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LABEL', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LABEL')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LABEL':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LABEL')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LABEL', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LABEL'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LABEL', fromsubclass_=False, pretty_print=True):
        if not fromsubclass_:
            for item_ in self.content_:
                item_.export(outfile, level, item_.name, namespaceprefix_, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for ERROR_ in self.ERROR:
            namespaceprefix_ = self.ERROR_nsprefix_ + ':' if (UseCapturedNS_ and self.ERROR_nsprefix_) else ''
            ERROR_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ERROR', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        if node.text is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', node.text)
            self.content_.append(obj_)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ERROR':
            obj_ = ERROR.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'ERROR', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_ERROR'):
              self.add_ERROR(obj_.value)
            elif hasattr(self, 'set_ERROR'):
              self.set_ERROR(obj_.value)
        if not fromsubclass_ and child_.tail is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.tail)
            self.content_.append(obj_)
# end class LABEL


class CONNOTE(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ERROR=None, valueOf_=None, mixedclass_=None, content_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if ERROR is None:
            self.ERROR = []
        else:
            self.ERROR = ERROR
        self.ERROR_nsprefix_ = None
        self.valueOf_ = valueOf_
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CONNOTE)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CONNOTE.subclass:
            return CONNOTE.subclass(*args_, **kwargs_)
        else:
            return CONNOTE(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ERROR(self):
        return self.ERROR
    def set_ERROR(self, ERROR):
        self.ERROR = ERROR
    def add_ERROR(self, value):
        self.ERROR.append(value)
    def insert_ERROR_at(self, index, value):
        self.ERROR.insert(index, value)
    def replace_ERROR_at(self, index, value):
        self.ERROR[index] = value
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def hasContent_(self):
        if (
            self.ERROR or
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_) or
            self.content_
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CONNOTE', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CONNOTE')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CONNOTE':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CONNOTE')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CONNOTE', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CONNOTE'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CONNOTE', fromsubclass_=False, pretty_print=True):
        if not fromsubclass_:
            for item_ in self.content_:
                item_.export(outfile, level, item_.name, namespaceprefix_, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for ERROR_ in self.ERROR:
            namespaceprefix_ = self.ERROR_nsprefix_ + ':' if (UseCapturedNS_ and self.ERROR_nsprefix_) else ''
            ERROR_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ERROR', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        if node.text is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', node.text)
            self.content_.append(obj_)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ERROR':
            obj_ = ERROR.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'ERROR', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_ERROR'):
              self.add_ERROR(obj_.value)
            elif hasattr(self, 'set_ERROR'):
              self.set_ERROR(obj_.value)
        if not fromsubclass_ and child_.tail is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.tail)
            self.content_.append(obj_)
# end class CONNOTE


class MANIFEST(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ERROR=None, valueOf_=None, mixedclass_=None, content_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if ERROR is None:
            self.ERROR = []
        else:
            self.ERROR = ERROR
        self.ERROR_nsprefix_ = None
        self.valueOf_ = valueOf_
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, MANIFEST)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if MANIFEST.subclass:
            return MANIFEST.subclass(*args_, **kwargs_)
        else:
            return MANIFEST(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ERROR(self):
        return self.ERROR
    def set_ERROR(self, ERROR):
        self.ERROR = ERROR
    def add_ERROR(self, value):
        self.ERROR.append(value)
    def insert_ERROR_at(self, index, value):
        self.ERROR.insert(index, value)
    def replace_ERROR_at(self, index, value):
        self.ERROR[index] = value
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def hasContent_(self):
        if (
            self.ERROR or
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_) or
            self.content_
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='MANIFEST', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('MANIFEST')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'MANIFEST':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='MANIFEST')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='MANIFEST', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='MANIFEST'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='MANIFEST', fromsubclass_=False, pretty_print=True):
        if not fromsubclass_:
            for item_ in self.content_:
                item_.export(outfile, level, item_.name, namespaceprefix_, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for ERROR_ in self.ERROR:
            namespaceprefix_ = self.ERROR_nsprefix_ + ':' if (UseCapturedNS_ and self.ERROR_nsprefix_) else ''
            ERROR_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ERROR', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        if node.text is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', node.text)
            self.content_.append(obj_)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ERROR':
            obj_ = ERROR.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'ERROR', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_ERROR'):
              self.add_ERROR(obj_.value)
            elif hasattr(self, 'set_ERROR'):
              self.set_ERROR(obj_.value)
        if not fromsubclass_ and child_.tail is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.tail)
            self.content_.append(obj_)
# end class MANIFEST


class INVOICE(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ERROR=None, valueOf_=None, mixedclass_=None, content_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if ERROR is None:
            self.ERROR = []
        else:
            self.ERROR = ERROR
        self.ERROR_nsprefix_ = None
        self.valueOf_ = valueOf_
        if mixedclass_ is None:
            self.mixedclass_ = MixedContainer
        else:
            self.mixedclass_ = mixedclass_
        if content_ is None:
            self.content_ = []
        else:
            self.content_ = content_
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, INVOICE)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if INVOICE.subclass:
            return INVOICE.subclass(*args_, **kwargs_)
        else:
            return INVOICE(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ERROR(self):
        return self.ERROR
    def set_ERROR(self, ERROR):
        self.ERROR = ERROR
    def add_ERROR(self, value):
        self.ERROR.append(value)
    def insert_ERROR_at(self, index, value):
        self.ERROR.insert(index, value)
    def replace_ERROR_at(self, index, value):
        self.ERROR[index] = value
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def hasContent_(self):
        if (
            self.ERROR or
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_) or
            self.content_
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='INVOICE', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('INVOICE')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'INVOICE':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='INVOICE')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='INVOICE', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='INVOICE'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='INVOICE', fromsubclass_=False, pretty_print=True):
        if not fromsubclass_:
            for item_ in self.content_:
                item_.export(outfile, level, item_.name, namespaceprefix_, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for ERROR_ in self.ERROR:
            namespaceprefix_ = self.ERROR_nsprefix_ + ':' if (UseCapturedNS_ and self.ERROR_nsprefix_) else ''
            ERROR_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ERROR', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        if node.text is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', node.text)
            self.content_.append(obj_)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def buildAttributes(self, node, attrs, already_processed):
        pass
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ERROR':
            obj_ = ERROR.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, 'ERROR', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_ERROR'):
              self.add_ERROR(obj_.value)
            elif hasattr(self, 'set_ERROR'):
              self.set_ERROR(obj_.value)
        if not fromsubclass_ and child_.tail is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.tail)
            self.content_.append(obj_)
# end class INVOICE


class RATE(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ERROR=None, PRICE=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if ERROR is None:
            self.ERROR = []
        else:
            self.ERROR = ERROR
        self.ERROR_nsprefix_ = None
        if PRICE is None:
            self.PRICE = []
        else:
            self.PRICE = PRICE
        self.PRICE_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RATE)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RATE.subclass:
            return RATE.subclass(*args_, **kwargs_)
        else:
            return RATE(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ERROR(self):
        return self.ERROR
    def set_ERROR(self, ERROR):
        self.ERROR = ERROR
    def add_ERROR(self, value):
        self.ERROR.append(value)
    def insert_ERROR_at(self, index, value):
        self.ERROR.insert(index, value)
    def replace_ERROR_at(self, index, value):
        self.ERROR[index] = value
    def get_PRICE(self):
        return self.PRICE
    def set_PRICE(self, PRICE):
        self.PRICE = PRICE
    def add_PRICE(self, value):
        self.PRICE.append(value)
    def insert_PRICE_at(self, index, value):
        self.PRICE.insert(index, value)
    def replace_PRICE_at(self, index, value):
        self.PRICE[index] = value
    def hasContent_(self):
        if (
            self.ERROR or
            self.PRICE
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RATE', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RATE')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RATE':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RATE')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RATE', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RATE'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RATE', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for ERROR_ in self.ERROR:
            namespaceprefix_ = self.ERROR_nsprefix_ + ':' if (UseCapturedNS_ and self.ERROR_nsprefix_) else ''
            ERROR_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ERROR', pretty_print=pretty_print)
        for PRICE_ in self.PRICE:
            namespaceprefix_ = self.PRICE_nsprefix_ + ':' if (UseCapturedNS_ and self.PRICE_nsprefix_) else ''
            PRICE_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PRICE', pretty_print=pretty_print)
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
        if nodeName_ == 'ERROR':
            obj_ = ERROR.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ERROR.append(obj_)
            obj_.original_tagname_ = 'ERROR'
        elif nodeName_ == 'PRICE':
            obj_ = PRICE.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PRICE.append(obj_)
            obj_.original_tagname_ = 'PRICE'
# end class RATE


class CREATE(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CONREF=None, CONNUMBER=None, SUCCESS=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CONREF = CONREF
        self.CONREF_nsprefix_ = None
        self.CONNUMBER = CONNUMBER
        self.CONNUMBER_nsprefix_ = None
        self.SUCCESS = SUCCESS
        self.SUCCESS_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CREATE)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CREATE.subclass:
            return CREATE.subclass(*args_, **kwargs_)
        else:
            return CREATE(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CONREF(self):
        return self.CONREF
    def set_CONREF(self, CONREF):
        self.CONREF = CONREF
    def get_CONNUMBER(self):
        return self.CONNUMBER
    def set_CONNUMBER(self, CONNUMBER):
        self.CONNUMBER = CONNUMBER
    def get_SUCCESS(self):
        return self.SUCCESS
    def set_SUCCESS(self, SUCCESS):
        self.SUCCESS = SUCCESS
    def hasContent_(self):
        if (
            self.CONREF is not None or
            self.CONNUMBER is not None or
            self.SUCCESS is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CREATE', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CREATE')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CREATE':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CREATE')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CREATE', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CREATE'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CREATE', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CONREF is not None:
            namespaceprefix_ = self.CONREF_nsprefix_ + ':' if (UseCapturedNS_ and self.CONREF_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONREF>%s</%sCONREF>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONREF), input_name='CONREF')), namespaceprefix_ , eol_))
        if self.CONNUMBER is not None:
            namespaceprefix_ = self.CONNUMBER_nsprefix_ + ':' if (UseCapturedNS_ and self.CONNUMBER_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONNUMBER>%s</%sCONNUMBER>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONNUMBER), input_name='CONNUMBER')), namespaceprefix_ , eol_))
        if self.SUCCESS is not None:
            namespaceprefix_ = self.SUCCESS_nsprefix_ + ':' if (UseCapturedNS_ and self.SUCCESS_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSUCCESS>%s</%sSUCCESS>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SUCCESS), input_name='SUCCESS')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'CONREF':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONREF')
            value_ = self.gds_validate_string(value_, node, 'CONREF')
            self.CONREF = value_
            self.CONREF_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONNUMBER':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONNUMBER')
            value_ = self.gds_validate_string(value_, node, 'CONNUMBER')
            self.CONNUMBER = value_
            self.CONNUMBER_nsprefix_ = child_.prefix
        elif nodeName_ == 'SUCCESS':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SUCCESS')
            value_ = self.gds_validate_string(value_, node, 'SUCCESS')
            self.SUCCESS = value_
            self.SUCCESS_nsprefix_ = child_.prefix
# end class CREATE


class BOOK(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CONSIGNMENT=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if CONSIGNMENT is None:
            self.CONSIGNMENT = []
        else:
            self.CONSIGNMENT = CONSIGNMENT
        self.CONSIGNMENT_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, BOOK)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BOOK.subclass:
            return BOOK.subclass(*args_, **kwargs_)
        else:
            return BOOK(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CONSIGNMENT(self):
        return self.CONSIGNMENT
    def set_CONSIGNMENT(self, CONSIGNMENT):
        self.CONSIGNMENT = CONSIGNMENT
    def add_CONSIGNMENT(self, value):
        self.CONSIGNMENT.append(value)
    def insert_CONSIGNMENT_at(self, index, value):
        self.CONSIGNMENT.insert(index, value)
    def replace_CONSIGNMENT_at(self, index, value):
        self.CONSIGNMENT[index] = value
    def hasContent_(self):
        if (
            self.CONSIGNMENT
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BOOK', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('BOOK')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'BOOK':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BOOK')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='BOOK', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='BOOK'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BOOK', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for CONSIGNMENT_ in self.CONSIGNMENT:
            namespaceprefix_ = self.CONSIGNMENT_nsprefix_ + ':' if (UseCapturedNS_ and self.CONSIGNMENT_nsprefix_) else ''
            CONSIGNMENT_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CONSIGNMENT', pretty_print=pretty_print)
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
        if nodeName_ == 'CONSIGNMENT':
            obj_ = CONSIGNMENT.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CONSIGNMENT.append(obj_)
            obj_.original_tagname_ = 'CONSIGNMENT'
# end class BOOK


class SHIP(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ERROR=None, CONSIGNMENT=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if ERROR is None:
            self.ERROR = []
        else:
            self.ERROR = ERROR
        self.ERROR_nsprefix_ = None
        if CONSIGNMENT is None:
            self.CONSIGNMENT = []
        else:
            self.CONSIGNMENT = CONSIGNMENT
        self.CONSIGNMENT_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SHIP)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SHIP.subclass:
            return SHIP.subclass(*args_, **kwargs_)
        else:
            return SHIP(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ERROR(self):
        return self.ERROR
    def set_ERROR(self, ERROR):
        self.ERROR = ERROR
    def add_ERROR(self, value):
        self.ERROR.append(value)
    def insert_ERROR_at(self, index, value):
        self.ERROR.insert(index, value)
    def replace_ERROR_at(self, index, value):
        self.ERROR[index] = value
    def get_CONSIGNMENT(self):
        return self.CONSIGNMENT
    def set_CONSIGNMENT(self, CONSIGNMENT):
        self.CONSIGNMENT = CONSIGNMENT
    def add_CONSIGNMENT(self, value):
        self.CONSIGNMENT.append(value)
    def insert_CONSIGNMENT_at(self, index, value):
        self.CONSIGNMENT.insert(index, value)
    def replace_CONSIGNMENT_at(self, index, value):
        self.CONSIGNMENT[index] = value
    def hasContent_(self):
        if (
            self.ERROR or
            self.CONSIGNMENT
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SHIP', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SHIP')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SHIP':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SHIP')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SHIP', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SHIP'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SHIP', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for ERROR_ in self.ERROR:
            namespaceprefix_ = self.ERROR_nsprefix_ + ':' if (UseCapturedNS_ and self.ERROR_nsprefix_) else ''
            ERROR_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ERROR', pretty_print=pretty_print)
        for CONSIGNMENT_ in self.CONSIGNMENT:
            namespaceprefix_ = self.CONSIGNMENT_nsprefix_ + ':' if (UseCapturedNS_ and self.CONSIGNMENT_nsprefix_) else ''
            CONSIGNMENT_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CONSIGNMENT', pretty_print=pretty_print)
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
        if nodeName_ == 'ERROR':
            obj_ = ERROR.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ERROR.append(obj_)
            obj_.original_tagname_ = 'ERROR'
        elif nodeName_ == 'CONSIGNMENT':
            obj_ = CONSIGNMENT.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CONSIGNMENT.append(obj_)
            obj_.original_tagname_ = 'CONSIGNMENT'
# end class SHIP


class CONSIGNMENT(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CONREF=None, CONNUMBER=None, SUCCESS=None, FIRSTTIMETRADER=None, BOOKINGREF=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CONREF = CONREF
        self.CONREF_nsprefix_ = None
        self.CONNUMBER = CONNUMBER
        self.CONNUMBER_nsprefix_ = None
        self.SUCCESS = SUCCESS
        self.SUCCESS_nsprefix_ = None
        self.FIRSTTIMETRADER = FIRSTTIMETRADER
        self.FIRSTTIMETRADER_nsprefix_ = None
        self.BOOKINGREF = BOOKINGREF
        self.BOOKINGREF_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CONSIGNMENT)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CONSIGNMENT.subclass:
            return CONSIGNMENT.subclass(*args_, **kwargs_)
        else:
            return CONSIGNMENT(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CONREF(self):
        return self.CONREF
    def set_CONREF(self, CONREF):
        self.CONREF = CONREF
    def get_CONNUMBER(self):
        return self.CONNUMBER
    def set_CONNUMBER(self, CONNUMBER):
        self.CONNUMBER = CONNUMBER
    def get_SUCCESS(self):
        return self.SUCCESS
    def set_SUCCESS(self, SUCCESS):
        self.SUCCESS = SUCCESS
    def get_FIRSTTIMETRADER(self):
        return self.FIRSTTIMETRADER
    def set_FIRSTTIMETRADER(self, FIRSTTIMETRADER):
        self.FIRSTTIMETRADER = FIRSTTIMETRADER
    def get_BOOKINGREF(self):
        return self.BOOKINGREF
    def set_BOOKINGREF(self, BOOKINGREF):
        self.BOOKINGREF = BOOKINGREF
    def hasContent_(self):
        if (
            self.CONREF is not None or
            self.CONNUMBER is not None or
            self.SUCCESS is not None or
            self.FIRSTTIMETRADER is not None or
            self.BOOKINGREF is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CONSIGNMENT', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CONSIGNMENT')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CONSIGNMENT':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CONSIGNMENT')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CONSIGNMENT', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CONSIGNMENT'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CONSIGNMENT', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CONREF is not None:
            namespaceprefix_ = self.CONREF_nsprefix_ + ':' if (UseCapturedNS_ and self.CONREF_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONREF>%s</%sCONREF>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONREF), input_name='CONREF')), namespaceprefix_ , eol_))
        if self.CONNUMBER is not None:
            namespaceprefix_ = self.CONNUMBER_nsprefix_ + ':' if (UseCapturedNS_ and self.CONNUMBER_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONNUMBER>%s</%sCONNUMBER>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONNUMBER), input_name='CONNUMBER')), namespaceprefix_ , eol_))
        if self.SUCCESS is not None:
            namespaceprefix_ = self.SUCCESS_nsprefix_ + ':' if (UseCapturedNS_ and self.SUCCESS_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSUCCESS>%s</%sSUCCESS>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SUCCESS), input_name='SUCCESS')), namespaceprefix_ , eol_))
        if self.FIRSTTIMETRADER is not None:
            namespaceprefix_ = self.FIRSTTIMETRADER_nsprefix_ + ':' if (UseCapturedNS_ and self.FIRSTTIMETRADER_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFIRSTTIMETRADER>%s</%sFIRSTTIMETRADER>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FIRSTTIMETRADER), input_name='FIRSTTIMETRADER')), namespaceprefix_ , eol_))
        if self.BOOKINGREF is not None:
            namespaceprefix_ = self.BOOKINGREF_nsprefix_ + ':' if (UseCapturedNS_ and self.BOOKINGREF_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBOOKINGREF>%s</%sBOOKINGREF>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BOOKINGREF), input_name='BOOKINGREF')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'CONREF':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONREF')
            value_ = self.gds_validate_string(value_, node, 'CONREF')
            self.CONREF = value_
            self.CONREF_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONNUMBER':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONNUMBER')
            value_ = self.gds_validate_string(value_, node, 'CONNUMBER')
            self.CONNUMBER = value_
            self.CONNUMBER_nsprefix_ = child_.prefix
        elif nodeName_ == 'SUCCESS':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SUCCESS')
            value_ = self.gds_validate_string(value_, node, 'SUCCESS')
            self.SUCCESS = value_
            self.SUCCESS_nsprefix_ = child_.prefix
        elif nodeName_ == 'FIRSTTIMETRADER':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FIRSTTIMETRADER')
            value_ = self.gds_validate_string(value_, node, 'FIRSTTIMETRADER')
            self.FIRSTTIMETRADER = value_
            self.FIRSTTIMETRADER_nsprefix_ = child_.prefix
        elif nodeName_ == 'BOOKINGREF':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BOOKINGREF')
            value_ = self.gds_validate_string(value_, node, 'BOOKINGREF')
            self.BOOKINGREF = value_
            self.BOOKINGREF_nsprefix_ = child_.prefix
# end class CONSIGNMENT


class PRICE(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, RATEID=None, SERVICE=None, SERVICEDESC=None, OPTION=None, OPTIONDESC=None, CURRENCY=None, RATE=None, RESULT=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.RATEID = RATEID
        self.RATEID_nsprefix_ = None
        self.SERVICE = SERVICE
        self.SERVICE_nsprefix_ = None
        self.SERVICEDESC = SERVICEDESC
        self.SERVICEDESC_nsprefix_ = None
        self.OPTION = OPTION
        self.OPTION_nsprefix_ = None
        self.OPTIONDESC = OPTIONDESC
        self.OPTIONDESC_nsprefix_ = None
        self.CURRENCY = CURRENCY
        self.CURRENCY_nsprefix_ = None
        self.RATE = RATE
        self.RATE_nsprefix_ = None
        self.RESULT = RESULT
        self.RESULT_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PRICE)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PRICE.subclass:
            return PRICE.subclass(*args_, **kwargs_)
        else:
            return PRICE(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_RATEID(self):
        return self.RATEID
    def set_RATEID(self, RATEID):
        self.RATEID = RATEID
    def get_SERVICE(self):
        return self.SERVICE
    def set_SERVICE(self, SERVICE):
        self.SERVICE = SERVICE
    def get_SERVICEDESC(self):
        return self.SERVICEDESC
    def set_SERVICEDESC(self, SERVICEDESC):
        self.SERVICEDESC = SERVICEDESC
    def get_OPTION(self):
        return self.OPTION
    def set_OPTION(self, OPTION):
        self.OPTION = OPTION
    def get_OPTIONDESC(self):
        return self.OPTIONDESC
    def set_OPTIONDESC(self, OPTIONDESC):
        self.OPTIONDESC = OPTIONDESC
    def get_CURRENCY(self):
        return self.CURRENCY
    def set_CURRENCY(self, CURRENCY):
        self.CURRENCY = CURRENCY
    def get_RATE(self):
        return self.RATE
    def set_RATE(self, RATE):
        self.RATE = RATE
    def get_RESULT(self):
        return self.RESULT
    def set_RESULT(self, RESULT):
        self.RESULT = RESULT
    def hasContent_(self):
        if (
            self.RATEID is not None or
            self.SERVICE is not None or
            self.SERVICEDESC is not None or
            self.OPTION is not None or
            self.OPTIONDESC is not None or
            self.CURRENCY is not None or
            self.RATE is not None or
            self.RESULT is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PRICE', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PRICE')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PRICE':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PRICE')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PRICE', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PRICE'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PRICE', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.RATEID is not None:
            namespaceprefix_ = self.RATEID_nsprefix_ + ':' if (UseCapturedNS_ and self.RATEID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRATEID>%s</%sRATEID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.RATEID), input_name='RATEID')), namespaceprefix_ , eol_))
        if self.SERVICE is not None:
            namespaceprefix_ = self.SERVICE_nsprefix_ + ':' if (UseCapturedNS_ and self.SERVICE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSERVICE>%s</%sSERVICE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SERVICE), input_name='SERVICE')), namespaceprefix_ , eol_))
        if self.SERVICEDESC is not None:
            namespaceprefix_ = self.SERVICEDESC_nsprefix_ + ':' if (UseCapturedNS_ and self.SERVICEDESC_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSERVICEDESC>%s</%sSERVICEDESC>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SERVICEDESC), input_name='SERVICEDESC')), namespaceprefix_ , eol_))
        if self.OPTION is not None:
            namespaceprefix_ = self.OPTION_nsprefix_ + ':' if (UseCapturedNS_ and self.OPTION_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOPTION>%s</%sOPTION>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OPTION), input_name='OPTION')), namespaceprefix_ , eol_))
        if self.OPTIONDESC is not None:
            namespaceprefix_ = self.OPTIONDESC_nsprefix_ + ':' if (UseCapturedNS_ and self.OPTIONDESC_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOPTIONDESC>%s</%sOPTIONDESC>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OPTIONDESC), input_name='OPTIONDESC')), namespaceprefix_ , eol_))
        if self.CURRENCY is not None:
            namespaceprefix_ = self.CURRENCY_nsprefix_ + ':' if (UseCapturedNS_ and self.CURRENCY_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCURRENCY>%s</%sCURRENCY>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CURRENCY), input_name='CURRENCY')), namespaceprefix_ , eol_))
        if self.RATE is not None:
            namespaceprefix_ = self.RATE_nsprefix_ + ':' if (UseCapturedNS_ and self.RATE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRATE>%s</%sRATE>%s' % (namespaceprefix_ , self.gds_format_decimal(self.RATE, input_name='RATE'), namespaceprefix_ , eol_))
        if self.RESULT is not None:
            namespaceprefix_ = self.RESULT_nsprefix_ + ':' if (UseCapturedNS_ and self.RESULT_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRESULT>%s</%sRESULT>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.RESULT), input_name='RESULT')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'RATEID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RATEID')
            value_ = self.gds_validate_string(value_, node, 'RATEID')
            self.RATEID = value_
            self.RATEID_nsprefix_ = child_.prefix
        elif nodeName_ == 'SERVICE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SERVICE')
            value_ = self.gds_validate_string(value_, node, 'SERVICE')
            self.SERVICE = value_
            self.SERVICE_nsprefix_ = child_.prefix
        elif nodeName_ == 'SERVICEDESC':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SERVICEDESC')
            value_ = self.gds_validate_string(value_, node, 'SERVICEDESC')
            self.SERVICEDESC = value_
            self.SERVICEDESC_nsprefix_ = child_.prefix
        elif nodeName_ == 'OPTION':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OPTION')
            value_ = self.gds_validate_string(value_, node, 'OPTION')
            self.OPTION = value_
            self.OPTION_nsprefix_ = child_.prefix
        elif nodeName_ == 'OPTIONDESC':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OPTIONDESC')
            value_ = self.gds_validate_string(value_, node, 'OPTIONDESC')
            self.OPTIONDESC = value_
            self.OPTIONDESC_nsprefix_ = child_.prefix
        elif nodeName_ == 'CURRENCY':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CURRENCY')
            value_ = self.gds_validate_string(value_, node, 'CURRENCY')
            self.CURRENCY = value_
            self.CURRENCY_nsprefix_ = child_.prefix
        elif nodeName_ == 'RATE' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'RATE')
            fval_ = self.gds_validate_decimal(fval_, node, 'RATE')
            self.RATE = fval_
            self.RATE_nsprefix_ = child_.prefix
        elif nodeName_ == 'RESULT':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RESULT')
            value_ = self.gds_validate_string(value_, node, 'RESULT')
            self.RESULT = value_
            self.RESULT_nsprefix_ = child_.prefix
# end class PRICE


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
        sys.stdout.write('#from shipment_response import *\n\n')
        sys.stdout.write('import shipment_response as model_\n\n')
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
    "BOOK",
    "CONNOTE",
    "CONSIGNMENT",
    "CREATE",
    "ERROR",
    "INVOICE",
    "LABEL",
    "MANIFEST",
    "PRICE",
    "PRINT",
    "RATE",
    "SHIP",
    "document",
    "parse_error",
    "runtime_error"
]
