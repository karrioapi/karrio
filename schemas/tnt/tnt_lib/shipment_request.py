#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Wed Feb 24 19:49:29 2021 by generateDS.py version 2.37.16.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './tnt_lib/shipment_request.py')
#
# Command line arguments:
#   ./schemas/shipment_request.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./tnt_lib/shipment_request.py" ./schemas/shipment_request.xsd
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


class ESHIPPER(GeneratedsSuper):
    """Generated by XML Authority"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, LOGIN=None, CONSIGNMENTBATCH=None, ACTIVITY=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.LOGIN = LOGIN
        self.LOGIN_nsprefix_ = None
        self.CONSIGNMENTBATCH = CONSIGNMENTBATCH
        self.CONSIGNMENTBATCH_nsprefix_ = None
        self.ACTIVITY = ACTIVITY
        self.ACTIVITY_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ESHIPPER)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ESHIPPER.subclass:
            return ESHIPPER.subclass(*args_, **kwargs_)
        else:
            return ESHIPPER(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_LOGIN(self):
        return self.LOGIN
    def set_LOGIN(self, LOGIN):
        self.LOGIN = LOGIN
    def get_CONSIGNMENTBATCH(self):
        return self.CONSIGNMENTBATCH
    def set_CONSIGNMENTBATCH(self, CONSIGNMENTBATCH):
        self.CONSIGNMENTBATCH = CONSIGNMENTBATCH
    def get_ACTIVITY(self):
        return self.ACTIVITY
    def set_ACTIVITY(self, ACTIVITY):
        self.ACTIVITY = ACTIVITY
    def hasContent_(self):
        if (
            self.LOGIN is not None or
            self.CONSIGNMENTBATCH is not None or
            self.ACTIVITY is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ESHIPPER', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ESHIPPER')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ESHIPPER':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ESHIPPER')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ESHIPPER', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ESHIPPER'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ESHIPPER', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.LOGIN is not None:
            namespaceprefix_ = self.LOGIN_nsprefix_ + ':' if (UseCapturedNS_ and self.LOGIN_nsprefix_) else ''
            self.LOGIN.export(outfile, level, namespaceprefix_, namespacedef_='', name_='LOGIN', pretty_print=pretty_print)
        if self.CONSIGNMENTBATCH is not None:
            namespaceprefix_ = self.CONSIGNMENTBATCH_nsprefix_ + ':' if (UseCapturedNS_ and self.CONSIGNMENTBATCH_nsprefix_) else ''
            self.CONSIGNMENTBATCH.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CONSIGNMENTBATCH', pretty_print=pretty_print)
        if self.ACTIVITY is not None:
            namespaceprefix_ = self.ACTIVITY_nsprefix_ + ':' if (UseCapturedNS_ and self.ACTIVITY_nsprefix_) else ''
            self.ACTIVITY.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ACTIVITY', pretty_print=pretty_print)
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
        if nodeName_ == 'LOGIN':
            obj_ = LOGIN.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LOGIN = obj_
            obj_.original_tagname_ = 'LOGIN'
        elif nodeName_ == 'CONSIGNMENTBATCH':
            obj_ = CONSIGNMENTBATCH.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CONSIGNMENTBATCH = obj_
            obj_.original_tagname_ = 'CONSIGNMENTBATCH'
        elif nodeName_ == 'ACTIVITY':
            obj_ = ACTIVITY.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ACTIVITY = obj_
            obj_.original_tagname_ = 'ACTIVITY'
# end class ESHIPPER


class LOGIN(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, COMPANY=None, PASSWORD=None, APPID=None, APPVERSION=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.COMPANY = COMPANY
        self.COMPANY_nsprefix_ = None
        self.PASSWORD = PASSWORD
        self.PASSWORD_nsprefix_ = None
        self.APPID = APPID
        self.APPID_nsprefix_ = None
        self.APPVERSION = APPVERSION
        self.APPVERSION_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LOGIN)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LOGIN.subclass:
            return LOGIN.subclass(*args_, **kwargs_)
        else:
            return LOGIN(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_COMPANY(self):
        return self.COMPANY
    def set_COMPANY(self, COMPANY):
        self.COMPANY = COMPANY
    def get_PASSWORD(self):
        return self.PASSWORD
    def set_PASSWORD(self, PASSWORD):
        self.PASSWORD = PASSWORD
    def get_APPID(self):
        return self.APPID
    def set_APPID(self, APPID):
        self.APPID = APPID
    def get_APPVERSION(self):
        return self.APPVERSION
    def set_APPVERSION(self, APPVERSION):
        self.APPVERSION = APPVERSION
    def hasContent_(self):
        if (
            self.COMPANY is not None or
            self.PASSWORD is not None or
            self.APPID is not None or
            self.APPVERSION is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LOGIN', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LOGIN')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LOGIN':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LOGIN')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LOGIN', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LOGIN'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LOGIN', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.COMPANY is not None:
            namespaceprefix_ = self.COMPANY_nsprefix_ + ':' if (UseCapturedNS_ and self.COMPANY_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCOMPANY>%s</%sCOMPANY>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.COMPANY), input_name='COMPANY')), namespaceprefix_ , eol_))
        if self.PASSWORD is not None:
            namespaceprefix_ = self.PASSWORD_nsprefix_ + ':' if (UseCapturedNS_ and self.PASSWORD_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPASSWORD>%s</%sPASSWORD>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PASSWORD), input_name='PASSWORD')), namespaceprefix_ , eol_))
        if self.APPID is not None:
            namespaceprefix_ = self.APPID_nsprefix_ + ':' if (UseCapturedNS_ and self.APPID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAPPID>%s</%sAPPID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.APPID), input_name='APPID')), namespaceprefix_ , eol_))
        if self.APPVERSION is not None:
            namespaceprefix_ = self.APPVERSION_nsprefix_ + ':' if (UseCapturedNS_ and self.APPVERSION_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAPPVERSION>%s</%sAPPVERSION>%s' % (namespaceprefix_ , self.gds_format_decimal(self.APPVERSION, input_name='APPVERSION'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'COMPANY':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'COMPANY')
            value_ = self.gds_validate_string(value_, node, 'COMPANY')
            self.COMPANY = value_
            self.COMPANY_nsprefix_ = child_.prefix
        elif nodeName_ == 'PASSWORD':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PASSWORD')
            value_ = self.gds_validate_string(value_, node, 'PASSWORD')
            self.PASSWORD = value_
            self.PASSWORD_nsprefix_ = child_.prefix
        elif nodeName_ == 'APPID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'APPID')
            value_ = self.gds_validate_string(value_, node, 'APPID')
            self.APPID = value_
            self.APPID_nsprefix_ = child_.prefix
        elif nodeName_ == 'APPVERSION' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'APPVERSION')
            fval_ = self.gds_validate_decimal(fval_, node, 'APPVERSION')
            self.APPVERSION = fval_
            self.APPVERSION_nsprefix_ = child_.prefix
# end class LOGIN


class CONSIGNMENTBATCH(GeneratedsSuper):
    """SR 7855 CONSIGNMEN is now optional, as the input document may be used
    purely to print a summary manifest or book a whole group"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GROUPCODE=None, SENDER=None, CONSIGNMENT=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GROUPCODE = GROUPCODE
        self.GROUPCODE_nsprefix_ = None
        self.SENDER = SENDER
        self.SENDER_nsprefix_ = None
        if CONSIGNMENT is None:
            self.CONSIGNMENT = []
        else:
            self.CONSIGNMENT = CONSIGNMENT
        self.CONSIGNMENT_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CONSIGNMENTBATCH)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CONSIGNMENTBATCH.subclass:
            return CONSIGNMENTBATCH.subclass(*args_, **kwargs_)
        else:
            return CONSIGNMENTBATCH(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GROUPCODE(self):
        return self.GROUPCODE
    def set_GROUPCODE(self, GROUPCODE):
        self.GROUPCODE = GROUPCODE
    def get_SENDER(self):
        return self.SENDER
    def set_SENDER(self, SENDER):
        self.SENDER = SENDER
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
            self.GROUPCODE is not None or
            self.SENDER is not None or
            self.CONSIGNMENT
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CONSIGNMENTBATCH', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CONSIGNMENTBATCH')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CONSIGNMENTBATCH':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CONSIGNMENTBATCH')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CONSIGNMENTBATCH', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CONSIGNMENTBATCH'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CONSIGNMENTBATCH', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GROUPCODE is not None:
            namespaceprefix_ = self.GROUPCODE_nsprefix_ + ':' if (UseCapturedNS_ and self.GROUPCODE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGROUPCODE>%s</%sGROUPCODE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GROUPCODE), input_name='GROUPCODE')), namespaceprefix_ , eol_))
        if self.SENDER is not None:
            namespaceprefix_ = self.SENDER_nsprefix_ + ':' if (UseCapturedNS_ and self.SENDER_nsprefix_) else ''
            self.SENDER.export(outfile, level, namespaceprefix_, namespacedef_='', name_='SENDER', pretty_print=pretty_print)
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
        if nodeName_ == 'GROUPCODE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GROUPCODE')
            value_ = self.gds_validate_string(value_, node, 'GROUPCODE')
            self.GROUPCODE = value_
            self.GROUPCODE_nsprefix_ = child_.prefix
        elif nodeName_ == 'SENDER':
            obj_ = SENDER.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SENDER = obj_
            obj_.original_tagname_ = 'SENDER'
        elif nodeName_ == 'CONSIGNMENT':
            obj_ = CONSIGNMENT.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CONSIGNMENT.append(obj_)
            obj_.original_tagname_ = 'CONSIGNMENT'
# end class CONSIGNMENTBATCH


class SENDER(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, COMPANYNAME=None, STREETADDRESS1=None, STREETADDRESS2=None, STREETADDRESS3=None, CITY=None, PROVINCE=None, POSTCODE=None, COUNTRY=None, ACCOUNT=None, VAT=None, CONTACTNAME=None, CONTACTDIALCODE=None, CONTACTTELEPHONE=None, CONTACTEMAIL=None, COLLECTION=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.COMPANYNAME = COMPANYNAME
        self.COMPANYNAME_nsprefix_ = None
        self.STREETADDRESS1 = STREETADDRESS1
        self.STREETADDRESS1_nsprefix_ = None
        self.STREETADDRESS2 = STREETADDRESS2
        self.STREETADDRESS2_nsprefix_ = None
        self.STREETADDRESS3 = STREETADDRESS3
        self.STREETADDRESS3_nsprefix_ = None
        self.CITY = CITY
        self.CITY_nsprefix_ = None
        self.PROVINCE = PROVINCE
        self.PROVINCE_nsprefix_ = None
        self.POSTCODE = POSTCODE
        self.POSTCODE_nsprefix_ = None
        self.COUNTRY = COUNTRY
        self.COUNTRY_nsprefix_ = None
        self.ACCOUNT = ACCOUNT
        self.ACCOUNT_nsprefix_ = None
        self.VAT = VAT
        self.VAT_nsprefix_ = None
        self.CONTACTNAME = CONTACTNAME
        self.CONTACTNAME_nsprefix_ = None
        self.CONTACTDIALCODE = CONTACTDIALCODE
        self.CONTACTDIALCODE_nsprefix_ = None
        self.CONTACTTELEPHONE = CONTACTTELEPHONE
        self.CONTACTTELEPHONE_nsprefix_ = None
        self.CONTACTEMAIL = CONTACTEMAIL
        self.CONTACTEMAIL_nsprefix_ = None
        self.COLLECTION = COLLECTION
        self.COLLECTION_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SENDER)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SENDER.subclass:
            return SENDER.subclass(*args_, **kwargs_)
        else:
            return SENDER(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_COMPANYNAME(self):
        return self.COMPANYNAME
    def set_COMPANYNAME(self, COMPANYNAME):
        self.COMPANYNAME = COMPANYNAME
    def get_STREETADDRESS1(self):
        return self.STREETADDRESS1
    def set_STREETADDRESS1(self, STREETADDRESS1):
        self.STREETADDRESS1 = STREETADDRESS1
    def get_STREETADDRESS2(self):
        return self.STREETADDRESS2
    def set_STREETADDRESS2(self, STREETADDRESS2):
        self.STREETADDRESS2 = STREETADDRESS2
    def get_STREETADDRESS3(self):
        return self.STREETADDRESS3
    def set_STREETADDRESS3(self, STREETADDRESS3):
        self.STREETADDRESS3 = STREETADDRESS3
    def get_CITY(self):
        return self.CITY
    def set_CITY(self, CITY):
        self.CITY = CITY
    def get_PROVINCE(self):
        return self.PROVINCE
    def set_PROVINCE(self, PROVINCE):
        self.PROVINCE = PROVINCE
    def get_POSTCODE(self):
        return self.POSTCODE
    def set_POSTCODE(self, POSTCODE):
        self.POSTCODE = POSTCODE
    def get_COUNTRY(self):
        return self.COUNTRY
    def set_COUNTRY(self, COUNTRY):
        self.COUNTRY = COUNTRY
    def get_ACCOUNT(self):
        return self.ACCOUNT
    def set_ACCOUNT(self, ACCOUNT):
        self.ACCOUNT = ACCOUNT
    def get_VAT(self):
        return self.VAT
    def set_VAT(self, VAT):
        self.VAT = VAT
    def get_CONTACTNAME(self):
        return self.CONTACTNAME
    def set_CONTACTNAME(self, CONTACTNAME):
        self.CONTACTNAME = CONTACTNAME
    def get_CONTACTDIALCODE(self):
        return self.CONTACTDIALCODE
    def set_CONTACTDIALCODE(self, CONTACTDIALCODE):
        self.CONTACTDIALCODE = CONTACTDIALCODE
    def get_CONTACTTELEPHONE(self):
        return self.CONTACTTELEPHONE
    def set_CONTACTTELEPHONE(self, CONTACTTELEPHONE):
        self.CONTACTTELEPHONE = CONTACTTELEPHONE
    def get_CONTACTEMAIL(self):
        return self.CONTACTEMAIL
    def set_CONTACTEMAIL(self, CONTACTEMAIL):
        self.CONTACTEMAIL = CONTACTEMAIL
    def get_COLLECTION(self):
        return self.COLLECTION
    def set_COLLECTION(self, COLLECTION):
        self.COLLECTION = COLLECTION
    def hasContent_(self):
        if (
            self.COMPANYNAME is not None or
            self.STREETADDRESS1 is not None or
            self.STREETADDRESS2 is not None or
            self.STREETADDRESS3 is not None or
            self.CITY is not None or
            self.PROVINCE is not None or
            self.POSTCODE is not None or
            self.COUNTRY is not None or
            self.ACCOUNT is not None or
            self.VAT is not None or
            self.CONTACTNAME is not None or
            self.CONTACTDIALCODE is not None or
            self.CONTACTTELEPHONE is not None or
            self.CONTACTEMAIL is not None or
            self.COLLECTION is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SENDER', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SENDER')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SENDER':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SENDER')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SENDER', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SENDER'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SENDER', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.COMPANYNAME is not None:
            namespaceprefix_ = self.COMPANYNAME_nsprefix_ + ':' if (UseCapturedNS_ and self.COMPANYNAME_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCOMPANYNAME>%s</%sCOMPANYNAME>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.COMPANYNAME), input_name='COMPANYNAME')), namespaceprefix_ , eol_))
        if self.STREETADDRESS1 is not None:
            namespaceprefix_ = self.STREETADDRESS1_nsprefix_ + ':' if (UseCapturedNS_ and self.STREETADDRESS1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSTREETADDRESS1>%s</%sSTREETADDRESS1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.STREETADDRESS1), input_name='STREETADDRESS1')), namespaceprefix_ , eol_))
        if self.STREETADDRESS2 is not None:
            namespaceprefix_ = self.STREETADDRESS2_nsprefix_ + ':' if (UseCapturedNS_ and self.STREETADDRESS2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSTREETADDRESS2>%s</%sSTREETADDRESS2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.STREETADDRESS2), input_name='STREETADDRESS2')), namespaceprefix_ , eol_))
        if self.STREETADDRESS3 is not None:
            namespaceprefix_ = self.STREETADDRESS3_nsprefix_ + ':' if (UseCapturedNS_ and self.STREETADDRESS3_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSTREETADDRESS3>%s</%sSTREETADDRESS3>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.STREETADDRESS3), input_name='STREETADDRESS3')), namespaceprefix_ , eol_))
        if self.CITY is not None:
            namespaceprefix_ = self.CITY_nsprefix_ + ':' if (UseCapturedNS_ and self.CITY_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCITY>%s</%sCITY>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CITY), input_name='CITY')), namespaceprefix_ , eol_))
        if self.PROVINCE is not None:
            namespaceprefix_ = self.PROVINCE_nsprefix_ + ':' if (UseCapturedNS_ and self.PROVINCE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPROVINCE>%s</%sPROVINCE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PROVINCE), input_name='PROVINCE')), namespaceprefix_ , eol_))
        if self.POSTCODE is not None:
            namespaceprefix_ = self.POSTCODE_nsprefix_ + ':' if (UseCapturedNS_ and self.POSTCODE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPOSTCODE>%s</%sPOSTCODE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.POSTCODE), input_name='POSTCODE')), namespaceprefix_ , eol_))
        if self.COUNTRY is not None:
            namespaceprefix_ = self.COUNTRY_nsprefix_ + ':' if (UseCapturedNS_ and self.COUNTRY_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCOUNTRY>%s</%sCOUNTRY>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.COUNTRY), input_name='COUNTRY')), namespaceprefix_ , eol_))
        if self.ACCOUNT is not None:
            namespaceprefix_ = self.ACCOUNT_nsprefix_ + ':' if (UseCapturedNS_ and self.ACCOUNT_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sACCOUNT>%s</%sACCOUNT>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ACCOUNT), input_name='ACCOUNT')), namespaceprefix_ , eol_))
        if self.VAT is not None:
            namespaceprefix_ = self.VAT_nsprefix_ + ':' if (UseCapturedNS_ and self.VAT_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sVAT>%s</%sVAT>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.VAT), input_name='VAT')), namespaceprefix_ , eol_))
        if self.CONTACTNAME is not None:
            namespaceprefix_ = self.CONTACTNAME_nsprefix_ + ':' if (UseCapturedNS_ and self.CONTACTNAME_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONTACTNAME>%s</%sCONTACTNAME>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONTACTNAME), input_name='CONTACTNAME')), namespaceprefix_ , eol_))
        if self.CONTACTDIALCODE is not None:
            namespaceprefix_ = self.CONTACTDIALCODE_nsprefix_ + ':' if (UseCapturedNS_ and self.CONTACTDIALCODE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONTACTDIALCODE>%s</%sCONTACTDIALCODE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONTACTDIALCODE), input_name='CONTACTDIALCODE')), namespaceprefix_ , eol_))
        if self.CONTACTTELEPHONE is not None:
            namespaceprefix_ = self.CONTACTTELEPHONE_nsprefix_ + ':' if (UseCapturedNS_ and self.CONTACTTELEPHONE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONTACTTELEPHONE>%s</%sCONTACTTELEPHONE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONTACTTELEPHONE), input_name='CONTACTTELEPHONE')), namespaceprefix_ , eol_))
        if self.CONTACTEMAIL is not None:
            namespaceprefix_ = self.CONTACTEMAIL_nsprefix_ + ':' if (UseCapturedNS_ and self.CONTACTEMAIL_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONTACTEMAIL>%s</%sCONTACTEMAIL>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONTACTEMAIL), input_name='CONTACTEMAIL')), namespaceprefix_ , eol_))
        if self.COLLECTION is not None:
            namespaceprefix_ = self.COLLECTION_nsprefix_ + ':' if (UseCapturedNS_ and self.COLLECTION_nsprefix_) else ''
            self.COLLECTION.export(outfile, level, namespaceprefix_, namespacedef_='', name_='COLLECTION', pretty_print=pretty_print)
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
        if nodeName_ == 'COMPANYNAME':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'COMPANYNAME')
            value_ = self.gds_validate_string(value_, node, 'COMPANYNAME')
            self.COMPANYNAME = value_
            self.COMPANYNAME_nsprefix_ = child_.prefix
        elif nodeName_ == 'STREETADDRESS1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'STREETADDRESS1')
            value_ = self.gds_validate_string(value_, node, 'STREETADDRESS1')
            self.STREETADDRESS1 = value_
            self.STREETADDRESS1_nsprefix_ = child_.prefix
        elif nodeName_ == 'STREETADDRESS2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'STREETADDRESS2')
            value_ = self.gds_validate_string(value_, node, 'STREETADDRESS2')
            self.STREETADDRESS2 = value_
            self.STREETADDRESS2_nsprefix_ = child_.prefix
        elif nodeName_ == 'STREETADDRESS3':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'STREETADDRESS3')
            value_ = self.gds_validate_string(value_, node, 'STREETADDRESS3')
            self.STREETADDRESS3 = value_
            self.STREETADDRESS3_nsprefix_ = child_.prefix
        elif nodeName_ == 'CITY':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CITY')
            value_ = self.gds_validate_string(value_, node, 'CITY')
            self.CITY = value_
            self.CITY_nsprefix_ = child_.prefix
        elif nodeName_ == 'PROVINCE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PROVINCE')
            value_ = self.gds_validate_string(value_, node, 'PROVINCE')
            self.PROVINCE = value_
            self.PROVINCE_nsprefix_ = child_.prefix
        elif nodeName_ == 'POSTCODE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'POSTCODE')
            value_ = self.gds_validate_string(value_, node, 'POSTCODE')
            self.POSTCODE = value_
            self.POSTCODE_nsprefix_ = child_.prefix
        elif nodeName_ == 'COUNTRY':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'COUNTRY')
            value_ = self.gds_validate_string(value_, node, 'COUNTRY')
            self.COUNTRY = value_
            self.COUNTRY_nsprefix_ = child_.prefix
        elif nodeName_ == 'ACCOUNT':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ACCOUNT')
            value_ = self.gds_validate_string(value_, node, 'ACCOUNT')
            self.ACCOUNT = value_
            self.ACCOUNT_nsprefix_ = child_.prefix
        elif nodeName_ == 'VAT':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'VAT')
            value_ = self.gds_validate_string(value_, node, 'VAT')
            self.VAT = value_
            self.VAT_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONTACTNAME':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONTACTNAME')
            value_ = self.gds_validate_string(value_, node, 'CONTACTNAME')
            self.CONTACTNAME = value_
            self.CONTACTNAME_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONTACTDIALCODE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONTACTDIALCODE')
            value_ = self.gds_validate_string(value_, node, 'CONTACTDIALCODE')
            self.CONTACTDIALCODE = value_
            self.CONTACTDIALCODE_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONTACTTELEPHONE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONTACTTELEPHONE')
            value_ = self.gds_validate_string(value_, node, 'CONTACTTELEPHONE')
            self.CONTACTTELEPHONE = value_
            self.CONTACTTELEPHONE_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONTACTEMAIL':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONTACTEMAIL')
            value_ = self.gds_validate_string(value_, node, 'CONTACTEMAIL')
            self.CONTACTEMAIL = value_
            self.CONTACTEMAIL_nsprefix_ = child_.prefix
        elif nodeName_ == 'COLLECTION':
            obj_ = COLLECTION.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.COLLECTION = obj_
            obj_.original_tagname_ = 'COLLECTION'
# end class SENDER


class COLLECTION(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, COLLECTIONADDRESS=None, SHIPDATE=None, PREFCOLLECTTIME=None, ALTCOLLECTTIME=None, COLLINSTRUCTIONS=None, CONFIRMATIONEMAILADDRESS=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.COLLECTIONADDRESS = COLLECTIONADDRESS
        self.COLLECTIONADDRESS_nsprefix_ = None
        self.SHIPDATE = SHIPDATE
        self.SHIPDATE_nsprefix_ = None
        self.PREFCOLLECTTIME = PREFCOLLECTTIME
        self.PREFCOLLECTTIME_nsprefix_ = None
        self.ALTCOLLECTTIME = ALTCOLLECTTIME
        self.ALTCOLLECTTIME_nsprefix_ = None
        self.COLLINSTRUCTIONS = COLLINSTRUCTIONS
        self.COLLINSTRUCTIONS_nsprefix_ = None
        self.CONFIRMATIONEMAILADDRESS = CONFIRMATIONEMAILADDRESS
        self.CONFIRMATIONEMAILADDRESS_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, COLLECTION)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if COLLECTION.subclass:
            return COLLECTION.subclass(*args_, **kwargs_)
        else:
            return COLLECTION(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_COLLECTIONADDRESS(self):
        return self.COLLECTIONADDRESS
    def set_COLLECTIONADDRESS(self, COLLECTIONADDRESS):
        self.COLLECTIONADDRESS = COLLECTIONADDRESS
    def get_SHIPDATE(self):
        return self.SHIPDATE
    def set_SHIPDATE(self, SHIPDATE):
        self.SHIPDATE = SHIPDATE
    def get_PREFCOLLECTTIME(self):
        return self.PREFCOLLECTTIME
    def set_PREFCOLLECTTIME(self, PREFCOLLECTTIME):
        self.PREFCOLLECTTIME = PREFCOLLECTTIME
    def get_ALTCOLLECTTIME(self):
        return self.ALTCOLLECTTIME
    def set_ALTCOLLECTTIME(self, ALTCOLLECTTIME):
        self.ALTCOLLECTTIME = ALTCOLLECTTIME
    def get_COLLINSTRUCTIONS(self):
        return self.COLLINSTRUCTIONS
    def set_COLLINSTRUCTIONS(self, COLLINSTRUCTIONS):
        self.COLLINSTRUCTIONS = COLLINSTRUCTIONS
    def get_CONFIRMATIONEMAILADDRESS(self):
        return self.CONFIRMATIONEMAILADDRESS
    def set_CONFIRMATIONEMAILADDRESS(self, CONFIRMATIONEMAILADDRESS):
        self.CONFIRMATIONEMAILADDRESS = CONFIRMATIONEMAILADDRESS
    def hasContent_(self):
        if (
            self.COLLECTIONADDRESS is not None or
            self.SHIPDATE is not None or
            self.PREFCOLLECTTIME is not None or
            self.ALTCOLLECTTIME is not None or
            self.COLLINSTRUCTIONS is not None or
            self.CONFIRMATIONEMAILADDRESS is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='COLLECTION', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('COLLECTION')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'COLLECTION':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='COLLECTION')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='COLLECTION', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='COLLECTION'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='COLLECTION', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.COLLECTIONADDRESS is not None:
            namespaceprefix_ = self.COLLECTIONADDRESS_nsprefix_ + ':' if (UseCapturedNS_ and self.COLLECTIONADDRESS_nsprefix_) else ''
            self.COLLECTIONADDRESS.export(outfile, level, namespaceprefix_, namespacedef_='', name_='COLLECTIONADDRESS', pretty_print=pretty_print)
        if self.SHIPDATE is not None:
            namespaceprefix_ = self.SHIPDATE_nsprefix_ + ':' if (UseCapturedNS_ and self.SHIPDATE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSHIPDATE>%s</%sSHIPDATE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SHIPDATE), input_name='SHIPDATE')), namespaceprefix_ , eol_))
        if self.PREFCOLLECTTIME is not None:
            namespaceprefix_ = self.PREFCOLLECTTIME_nsprefix_ + ':' if (UseCapturedNS_ and self.PREFCOLLECTTIME_nsprefix_) else ''
            self.PREFCOLLECTTIME.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PREFCOLLECTTIME', pretty_print=pretty_print)
        if self.ALTCOLLECTTIME is not None:
            namespaceprefix_ = self.ALTCOLLECTTIME_nsprefix_ + ':' if (UseCapturedNS_ and self.ALTCOLLECTTIME_nsprefix_) else ''
            self.ALTCOLLECTTIME.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ALTCOLLECTTIME', pretty_print=pretty_print)
        if self.COLLINSTRUCTIONS is not None:
            namespaceprefix_ = self.COLLINSTRUCTIONS_nsprefix_ + ':' if (UseCapturedNS_ and self.COLLINSTRUCTIONS_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCOLLINSTRUCTIONS>%s</%sCOLLINSTRUCTIONS>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.COLLINSTRUCTIONS), input_name='COLLINSTRUCTIONS')), namespaceprefix_ , eol_))
        if self.CONFIRMATIONEMAILADDRESS is not None:
            namespaceprefix_ = self.CONFIRMATIONEMAILADDRESS_nsprefix_ + ':' if (UseCapturedNS_ and self.CONFIRMATIONEMAILADDRESS_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONFIRMATIONEMAILADDRESS>%s</%sCONFIRMATIONEMAILADDRESS>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONFIRMATIONEMAILADDRESS), input_name='CONFIRMATIONEMAILADDRESS')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'COLLECTIONADDRESS':
            obj_ = COLLECTIONADDRESS.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.COLLECTIONADDRESS = obj_
            obj_.original_tagname_ = 'COLLECTIONADDRESS'
        elif nodeName_ == 'SHIPDATE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SHIPDATE')
            value_ = self.gds_validate_string(value_, node, 'SHIPDATE')
            self.SHIPDATE = value_
            self.SHIPDATE_nsprefix_ = child_.prefix
        elif nodeName_ == 'PREFCOLLECTTIME':
            obj_ = PREFCOLLECTTIME.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PREFCOLLECTTIME = obj_
            obj_.original_tagname_ = 'PREFCOLLECTTIME'
        elif nodeName_ == 'ALTCOLLECTTIME':
            obj_ = ALTCOLLECTTIME.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ALTCOLLECTTIME = obj_
            obj_.original_tagname_ = 'ALTCOLLECTTIME'
        elif nodeName_ == 'COLLINSTRUCTIONS':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'COLLINSTRUCTIONS')
            value_ = self.gds_validate_string(value_, node, 'COLLINSTRUCTIONS')
            self.COLLINSTRUCTIONS = value_
            self.COLLINSTRUCTIONS_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONFIRMATIONEMAILADDRESS':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONFIRMATIONEMAILADDRESS')
            value_ = self.gds_validate_string(value_, node, 'CONFIRMATIONEMAILADDRESS')
            self.CONFIRMATIONEMAILADDRESS = value_
            self.CONFIRMATIONEMAILADDRESS_nsprefix_ = child_.prefix
# end class COLLECTION


class COLLECTIONADDRESS(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, COMPANYNAME=None, STREETADDRESS1=None, STREETADDRESS2=None, STREETADDRESS3=None, CITY=None, PROVINCE=None, POSTCODE=None, COUNTRY=None, VAT=None, CONTACTNAME=None, CONTACTDIALCODE=None, CONTACTTELEPHONE=None, CONTACTEMAIL=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.COMPANYNAME = COMPANYNAME
        self.COMPANYNAME_nsprefix_ = None
        self.STREETADDRESS1 = STREETADDRESS1
        self.STREETADDRESS1_nsprefix_ = None
        self.STREETADDRESS2 = STREETADDRESS2
        self.STREETADDRESS2_nsprefix_ = None
        self.STREETADDRESS3 = STREETADDRESS3
        self.STREETADDRESS3_nsprefix_ = None
        self.CITY = CITY
        self.CITY_nsprefix_ = None
        self.PROVINCE = PROVINCE
        self.PROVINCE_nsprefix_ = None
        self.POSTCODE = POSTCODE
        self.POSTCODE_nsprefix_ = None
        self.COUNTRY = COUNTRY
        self.COUNTRY_nsprefix_ = None
        self.VAT = VAT
        self.VAT_nsprefix_ = None
        self.CONTACTNAME = CONTACTNAME
        self.CONTACTNAME_nsprefix_ = None
        self.CONTACTDIALCODE = CONTACTDIALCODE
        self.CONTACTDIALCODE_nsprefix_ = None
        self.CONTACTTELEPHONE = CONTACTTELEPHONE
        self.CONTACTTELEPHONE_nsprefix_ = None
        self.CONTACTEMAIL = CONTACTEMAIL
        self.CONTACTEMAIL_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, COLLECTIONADDRESS)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if COLLECTIONADDRESS.subclass:
            return COLLECTIONADDRESS.subclass(*args_, **kwargs_)
        else:
            return COLLECTIONADDRESS(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_COMPANYNAME(self):
        return self.COMPANYNAME
    def set_COMPANYNAME(self, COMPANYNAME):
        self.COMPANYNAME = COMPANYNAME
    def get_STREETADDRESS1(self):
        return self.STREETADDRESS1
    def set_STREETADDRESS1(self, STREETADDRESS1):
        self.STREETADDRESS1 = STREETADDRESS1
    def get_STREETADDRESS2(self):
        return self.STREETADDRESS2
    def set_STREETADDRESS2(self, STREETADDRESS2):
        self.STREETADDRESS2 = STREETADDRESS2
    def get_STREETADDRESS3(self):
        return self.STREETADDRESS3
    def set_STREETADDRESS3(self, STREETADDRESS3):
        self.STREETADDRESS3 = STREETADDRESS3
    def get_CITY(self):
        return self.CITY
    def set_CITY(self, CITY):
        self.CITY = CITY
    def get_PROVINCE(self):
        return self.PROVINCE
    def set_PROVINCE(self, PROVINCE):
        self.PROVINCE = PROVINCE
    def get_POSTCODE(self):
        return self.POSTCODE
    def set_POSTCODE(self, POSTCODE):
        self.POSTCODE = POSTCODE
    def get_COUNTRY(self):
        return self.COUNTRY
    def set_COUNTRY(self, COUNTRY):
        self.COUNTRY = COUNTRY
    def get_VAT(self):
        return self.VAT
    def set_VAT(self, VAT):
        self.VAT = VAT
    def get_CONTACTNAME(self):
        return self.CONTACTNAME
    def set_CONTACTNAME(self, CONTACTNAME):
        self.CONTACTNAME = CONTACTNAME
    def get_CONTACTDIALCODE(self):
        return self.CONTACTDIALCODE
    def set_CONTACTDIALCODE(self, CONTACTDIALCODE):
        self.CONTACTDIALCODE = CONTACTDIALCODE
    def get_CONTACTTELEPHONE(self):
        return self.CONTACTTELEPHONE
    def set_CONTACTTELEPHONE(self, CONTACTTELEPHONE):
        self.CONTACTTELEPHONE = CONTACTTELEPHONE
    def get_CONTACTEMAIL(self):
        return self.CONTACTEMAIL
    def set_CONTACTEMAIL(self, CONTACTEMAIL):
        self.CONTACTEMAIL = CONTACTEMAIL
    def hasContent_(self):
        if (
            self.COMPANYNAME is not None or
            self.STREETADDRESS1 is not None or
            self.STREETADDRESS2 is not None or
            self.STREETADDRESS3 is not None or
            self.CITY is not None or
            self.PROVINCE is not None or
            self.POSTCODE is not None or
            self.COUNTRY is not None or
            self.VAT is not None or
            self.CONTACTNAME is not None or
            self.CONTACTDIALCODE is not None or
            self.CONTACTTELEPHONE is not None or
            self.CONTACTEMAIL is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='COLLECTIONADDRESS', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('COLLECTIONADDRESS')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'COLLECTIONADDRESS':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='COLLECTIONADDRESS')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='COLLECTIONADDRESS', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='COLLECTIONADDRESS'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='COLLECTIONADDRESS', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.COMPANYNAME is not None:
            namespaceprefix_ = self.COMPANYNAME_nsprefix_ + ':' if (UseCapturedNS_ and self.COMPANYNAME_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCOMPANYNAME>%s</%sCOMPANYNAME>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.COMPANYNAME), input_name='COMPANYNAME')), namespaceprefix_ , eol_))
        if self.STREETADDRESS1 is not None:
            namespaceprefix_ = self.STREETADDRESS1_nsprefix_ + ':' if (UseCapturedNS_ and self.STREETADDRESS1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSTREETADDRESS1>%s</%sSTREETADDRESS1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.STREETADDRESS1), input_name='STREETADDRESS1')), namespaceprefix_ , eol_))
        if self.STREETADDRESS2 is not None:
            namespaceprefix_ = self.STREETADDRESS2_nsprefix_ + ':' if (UseCapturedNS_ and self.STREETADDRESS2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSTREETADDRESS2>%s</%sSTREETADDRESS2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.STREETADDRESS2), input_name='STREETADDRESS2')), namespaceprefix_ , eol_))
        if self.STREETADDRESS3 is not None:
            namespaceprefix_ = self.STREETADDRESS3_nsprefix_ + ':' if (UseCapturedNS_ and self.STREETADDRESS3_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSTREETADDRESS3>%s</%sSTREETADDRESS3>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.STREETADDRESS3), input_name='STREETADDRESS3')), namespaceprefix_ , eol_))
        if self.CITY is not None:
            namespaceprefix_ = self.CITY_nsprefix_ + ':' if (UseCapturedNS_ and self.CITY_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCITY>%s</%sCITY>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CITY), input_name='CITY')), namespaceprefix_ , eol_))
        if self.PROVINCE is not None:
            namespaceprefix_ = self.PROVINCE_nsprefix_ + ':' if (UseCapturedNS_ and self.PROVINCE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPROVINCE>%s</%sPROVINCE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PROVINCE), input_name='PROVINCE')), namespaceprefix_ , eol_))
        if self.POSTCODE is not None:
            namespaceprefix_ = self.POSTCODE_nsprefix_ + ':' if (UseCapturedNS_ and self.POSTCODE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPOSTCODE>%s</%sPOSTCODE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.POSTCODE), input_name='POSTCODE')), namespaceprefix_ , eol_))
        if self.COUNTRY is not None:
            namespaceprefix_ = self.COUNTRY_nsprefix_ + ':' if (UseCapturedNS_ and self.COUNTRY_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCOUNTRY>%s</%sCOUNTRY>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.COUNTRY), input_name='COUNTRY')), namespaceprefix_ , eol_))
        if self.VAT is not None:
            namespaceprefix_ = self.VAT_nsprefix_ + ':' if (UseCapturedNS_ and self.VAT_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sVAT>%s</%sVAT>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.VAT), input_name='VAT')), namespaceprefix_ , eol_))
        if self.CONTACTNAME is not None:
            namespaceprefix_ = self.CONTACTNAME_nsprefix_ + ':' if (UseCapturedNS_ and self.CONTACTNAME_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONTACTNAME>%s</%sCONTACTNAME>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONTACTNAME), input_name='CONTACTNAME')), namespaceprefix_ , eol_))
        if self.CONTACTDIALCODE is not None:
            namespaceprefix_ = self.CONTACTDIALCODE_nsprefix_ + ':' if (UseCapturedNS_ and self.CONTACTDIALCODE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONTACTDIALCODE>%s</%sCONTACTDIALCODE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONTACTDIALCODE), input_name='CONTACTDIALCODE')), namespaceprefix_ , eol_))
        if self.CONTACTTELEPHONE is not None:
            namespaceprefix_ = self.CONTACTTELEPHONE_nsprefix_ + ':' if (UseCapturedNS_ and self.CONTACTTELEPHONE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONTACTTELEPHONE>%s</%sCONTACTTELEPHONE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONTACTTELEPHONE), input_name='CONTACTTELEPHONE')), namespaceprefix_ , eol_))
        if self.CONTACTEMAIL is not None:
            namespaceprefix_ = self.CONTACTEMAIL_nsprefix_ + ':' if (UseCapturedNS_ and self.CONTACTEMAIL_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONTACTEMAIL>%s</%sCONTACTEMAIL>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONTACTEMAIL), input_name='CONTACTEMAIL')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'COMPANYNAME':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'COMPANYNAME')
            value_ = self.gds_validate_string(value_, node, 'COMPANYNAME')
            self.COMPANYNAME = value_
            self.COMPANYNAME_nsprefix_ = child_.prefix
        elif nodeName_ == 'STREETADDRESS1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'STREETADDRESS1')
            value_ = self.gds_validate_string(value_, node, 'STREETADDRESS1')
            self.STREETADDRESS1 = value_
            self.STREETADDRESS1_nsprefix_ = child_.prefix
        elif nodeName_ == 'STREETADDRESS2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'STREETADDRESS2')
            value_ = self.gds_validate_string(value_, node, 'STREETADDRESS2')
            self.STREETADDRESS2 = value_
            self.STREETADDRESS2_nsprefix_ = child_.prefix
        elif nodeName_ == 'STREETADDRESS3':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'STREETADDRESS3')
            value_ = self.gds_validate_string(value_, node, 'STREETADDRESS3')
            self.STREETADDRESS3 = value_
            self.STREETADDRESS3_nsprefix_ = child_.prefix
        elif nodeName_ == 'CITY':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CITY')
            value_ = self.gds_validate_string(value_, node, 'CITY')
            self.CITY = value_
            self.CITY_nsprefix_ = child_.prefix
        elif nodeName_ == 'PROVINCE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PROVINCE')
            value_ = self.gds_validate_string(value_, node, 'PROVINCE')
            self.PROVINCE = value_
            self.PROVINCE_nsprefix_ = child_.prefix
        elif nodeName_ == 'POSTCODE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'POSTCODE')
            value_ = self.gds_validate_string(value_, node, 'POSTCODE')
            self.POSTCODE = value_
            self.POSTCODE_nsprefix_ = child_.prefix
        elif nodeName_ == 'COUNTRY':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'COUNTRY')
            value_ = self.gds_validate_string(value_, node, 'COUNTRY')
            self.COUNTRY = value_
            self.COUNTRY_nsprefix_ = child_.prefix
        elif nodeName_ == 'VAT':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'VAT')
            value_ = self.gds_validate_string(value_, node, 'VAT')
            self.VAT = value_
            self.VAT_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONTACTNAME':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONTACTNAME')
            value_ = self.gds_validate_string(value_, node, 'CONTACTNAME')
            self.CONTACTNAME = value_
            self.CONTACTNAME_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONTACTDIALCODE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONTACTDIALCODE')
            value_ = self.gds_validate_string(value_, node, 'CONTACTDIALCODE')
            self.CONTACTDIALCODE = value_
            self.CONTACTDIALCODE_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONTACTTELEPHONE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONTACTTELEPHONE')
            value_ = self.gds_validate_string(value_, node, 'CONTACTTELEPHONE')
            self.CONTACTTELEPHONE = value_
            self.CONTACTTELEPHONE_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONTACTEMAIL':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONTACTEMAIL')
            value_ = self.gds_validate_string(value_, node, 'CONTACTEMAIL')
            self.CONTACTEMAIL = value_
            self.CONTACTEMAIL_nsprefix_ = child_.prefix
# end class COLLECTIONADDRESS


class PREFCOLLECTTIME(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, FROM=None, TO=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.FROM = FROM
        self.FROM_nsprefix_ = None
        self.TO = TO
        self.TO_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PREFCOLLECTTIME)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PREFCOLLECTTIME.subclass:
            return PREFCOLLECTTIME.subclass(*args_, **kwargs_)
        else:
            return PREFCOLLECTTIME(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_FROM(self):
        return self.FROM
    def set_FROM(self, FROM):
        self.FROM = FROM
    def get_TO(self):
        return self.TO
    def set_TO(self, TO):
        self.TO = TO
    def hasContent_(self):
        if (
            self.FROM is not None or
            self.TO is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PREFCOLLECTTIME', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PREFCOLLECTTIME')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PREFCOLLECTTIME':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PREFCOLLECTTIME')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PREFCOLLECTTIME', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PREFCOLLECTTIME'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PREFCOLLECTTIME', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.FROM is not None:
            namespaceprefix_ = self.FROM_nsprefix_ + ':' if (UseCapturedNS_ and self.FROM_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFROM>%s</%sFROM>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FROM), input_name='FROM')), namespaceprefix_ , eol_))
        if self.TO is not None:
            namespaceprefix_ = self.TO_nsprefix_ + ':' if (UseCapturedNS_ and self.TO_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTO>%s</%sTO>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TO), input_name='TO')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'FROM':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FROM')
            value_ = self.gds_validate_string(value_, node, 'FROM')
            self.FROM = value_
            self.FROM_nsprefix_ = child_.prefix
        elif nodeName_ == 'TO':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TO')
            value_ = self.gds_validate_string(value_, node, 'TO')
            self.TO = value_
            self.TO_nsprefix_ = child_.prefix
# end class PREFCOLLECTTIME


class ALTCOLLECTTIME(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, FROM=None, TO=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.FROM = FROM
        self.FROM_nsprefix_ = None
        self.TO = TO
        self.TO_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ALTCOLLECTTIME)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ALTCOLLECTTIME.subclass:
            return ALTCOLLECTTIME.subclass(*args_, **kwargs_)
        else:
            return ALTCOLLECTTIME(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_FROM(self):
        return self.FROM
    def set_FROM(self, FROM):
        self.FROM = FROM
    def get_TO(self):
        return self.TO
    def set_TO(self, TO):
        self.TO = TO
    def hasContent_(self):
        if (
            self.FROM is not None or
            self.TO is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ALTCOLLECTTIME', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ALTCOLLECTTIME')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ALTCOLLECTTIME':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ALTCOLLECTTIME')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ALTCOLLECTTIME', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ALTCOLLECTTIME'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ALTCOLLECTTIME', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.FROM is not None:
            namespaceprefix_ = self.FROM_nsprefix_ + ':' if (UseCapturedNS_ and self.FROM_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFROM>%s</%sFROM>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FROM), input_name='FROM')), namespaceprefix_ , eol_))
        if self.TO is not None:
            namespaceprefix_ = self.TO_nsprefix_ + ':' if (UseCapturedNS_ and self.TO_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTO>%s</%sTO>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TO), input_name='TO')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'FROM':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FROM')
            value_ = self.gds_validate_string(value_, node, 'FROM')
            self.FROM = value_
            self.FROM_nsprefix_ = child_.prefix
        elif nodeName_ == 'TO':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TO')
            value_ = self.gds_validate_string(value_, node, 'TO')
            self.TO = value_
            self.TO_nsprefix_ = child_.prefix
# end class ALTCOLLECTTIME


class CONSIGNMENT(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CONREF=None, DETAILS=None, CONNUMBER=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CONREF = CONREF
        self.CONREF_nsprefix_ = None
        self.DETAILS = DETAILS
        self.DETAILS_nsprefix_ = None
        self.CONNUMBER = CONNUMBER
        self.CONNUMBER_nsprefix_ = None
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
    def get_DETAILS(self):
        return self.DETAILS
    def set_DETAILS(self, DETAILS):
        self.DETAILS = DETAILS
    def get_CONNUMBER(self):
        return self.CONNUMBER
    def set_CONNUMBER(self, CONNUMBER):
        self.CONNUMBER = CONNUMBER
    def hasContent_(self):
        if (
            self.CONREF is not None or
            self.DETAILS is not None or
            self.CONNUMBER is not None
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
        if self.DETAILS is not None:
            namespaceprefix_ = self.DETAILS_nsprefix_ + ':' if (UseCapturedNS_ and self.DETAILS_nsprefix_) else ''
            self.DETAILS.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DETAILS', pretty_print=pretty_print)
        if self.CONNUMBER is not None:
            namespaceprefix_ = self.CONNUMBER_nsprefix_ + ':' if (UseCapturedNS_ and self.CONNUMBER_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONNUMBER>%s</%sCONNUMBER>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONNUMBER), input_name='CONNUMBER')), namespaceprefix_ , eol_))
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
        elif nodeName_ == 'DETAILS':
            obj_ = DETAILS.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DETAILS = obj_
            obj_.original_tagname_ = 'DETAILS'
        elif nodeName_ == 'CONNUMBER':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONNUMBER')
            value_ = self.gds_validate_string(value_, node, 'CONNUMBER')
            self.CONNUMBER = value_
            self.CONNUMBER_nsprefix_ = child_.prefix
# end class CONSIGNMENT


class DETAILS(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, RECEIVER=None, DELIVERY=None, CONNUMBER=None, CUSTOMERREF=None, CONTYPE=None, PAYMENTIND=None, ITEMS=None, TOTALWEIGHT=None, TOTALVOLUME=None, CURRENCY=None, GOODSVALUE=None, INSURANCEVALUE=None, INSURANCECURRENCY=None, DIVISION=None, SERVICE=None, OPTION=None, DESCRIPTION=None, DELIVERYINST=None, CUSTOMCONTROLIN=None, HAZARDOUS=None, UNNUMBER=None, PACKINGGROUP=None, PACKAGE=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.RECEIVER = RECEIVER
        self.RECEIVER_nsprefix_ = None
        self.DELIVERY = DELIVERY
        self.DELIVERY_nsprefix_ = None
        self.CONNUMBER = CONNUMBER
        self.CONNUMBER_nsprefix_ = None
        self.CUSTOMERREF = CUSTOMERREF
        self.CUSTOMERREF_nsprefix_ = None
        self.CONTYPE = CONTYPE
        self.CONTYPE_nsprefix_ = None
        self.PAYMENTIND = PAYMENTIND
        self.PAYMENTIND_nsprefix_ = None
        self.ITEMS = ITEMS
        self.ITEMS_nsprefix_ = None
        self.TOTALWEIGHT = TOTALWEIGHT
        self.TOTALWEIGHT_nsprefix_ = None
        self.TOTALVOLUME = TOTALVOLUME
        self.TOTALVOLUME_nsprefix_ = None
        self.CURRENCY = CURRENCY
        self.CURRENCY_nsprefix_ = None
        self.GOODSVALUE = GOODSVALUE
        self.GOODSVALUE_nsprefix_ = None
        self.INSURANCEVALUE = INSURANCEVALUE
        self.INSURANCEVALUE_nsprefix_ = None
        self.INSURANCECURRENCY = INSURANCECURRENCY
        self.INSURANCECURRENCY_nsprefix_ = None
        self.DIVISION = DIVISION
        self.DIVISION_nsprefix_ = None
        self.SERVICE = SERVICE
        self.SERVICE_nsprefix_ = None
        if OPTION is None:
            self.OPTION = []
        else:
            self.OPTION = OPTION
        self.OPTION_nsprefix_ = None
        self.DESCRIPTION = DESCRIPTION
        self.DESCRIPTION_nsprefix_ = None
        self.DELIVERYINST = DELIVERYINST
        self.DELIVERYINST_nsprefix_ = None
        self.CUSTOMCONTROLIN = CUSTOMCONTROLIN
        self.CUSTOMCONTROLIN_nsprefix_ = None
        self.HAZARDOUS = HAZARDOUS
        self.HAZARDOUS_nsprefix_ = None
        self.UNNUMBER = UNNUMBER
        self.UNNUMBER_nsprefix_ = None
        self.PACKINGGROUP = PACKINGGROUP
        self.PACKINGGROUP_nsprefix_ = None
        if PACKAGE is None:
            self.PACKAGE = []
        else:
            self.PACKAGE = PACKAGE
        self.PACKAGE_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DETAILS)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DETAILS.subclass:
            return DETAILS.subclass(*args_, **kwargs_)
        else:
            return DETAILS(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_RECEIVER(self):
        return self.RECEIVER
    def set_RECEIVER(self, RECEIVER):
        self.RECEIVER = RECEIVER
    def get_DELIVERY(self):
        return self.DELIVERY
    def set_DELIVERY(self, DELIVERY):
        self.DELIVERY = DELIVERY
    def get_CONNUMBER(self):
        return self.CONNUMBER
    def set_CONNUMBER(self, CONNUMBER):
        self.CONNUMBER = CONNUMBER
    def get_CUSTOMERREF(self):
        return self.CUSTOMERREF
    def set_CUSTOMERREF(self, CUSTOMERREF):
        self.CUSTOMERREF = CUSTOMERREF
    def get_CONTYPE(self):
        return self.CONTYPE
    def set_CONTYPE(self, CONTYPE):
        self.CONTYPE = CONTYPE
    def get_PAYMENTIND(self):
        return self.PAYMENTIND
    def set_PAYMENTIND(self, PAYMENTIND):
        self.PAYMENTIND = PAYMENTIND
    def get_ITEMS(self):
        return self.ITEMS
    def set_ITEMS(self, ITEMS):
        self.ITEMS = ITEMS
    def get_TOTALWEIGHT(self):
        return self.TOTALWEIGHT
    def set_TOTALWEIGHT(self, TOTALWEIGHT):
        self.TOTALWEIGHT = TOTALWEIGHT
    def get_TOTALVOLUME(self):
        return self.TOTALVOLUME
    def set_TOTALVOLUME(self, TOTALVOLUME):
        self.TOTALVOLUME = TOTALVOLUME
    def get_CURRENCY(self):
        return self.CURRENCY
    def set_CURRENCY(self, CURRENCY):
        self.CURRENCY = CURRENCY
    def get_GOODSVALUE(self):
        return self.GOODSVALUE
    def set_GOODSVALUE(self, GOODSVALUE):
        self.GOODSVALUE = GOODSVALUE
    def get_INSURANCEVALUE(self):
        return self.INSURANCEVALUE
    def set_INSURANCEVALUE(self, INSURANCEVALUE):
        self.INSURANCEVALUE = INSURANCEVALUE
    def get_INSURANCECURRENCY(self):
        return self.INSURANCECURRENCY
    def set_INSURANCECURRENCY(self, INSURANCECURRENCY):
        self.INSURANCECURRENCY = INSURANCECURRENCY
    def get_DIVISION(self):
        return self.DIVISION
    def set_DIVISION(self, DIVISION):
        self.DIVISION = DIVISION
    def get_SERVICE(self):
        return self.SERVICE
    def set_SERVICE(self, SERVICE):
        self.SERVICE = SERVICE
    def get_OPTION(self):
        return self.OPTION
    def set_OPTION(self, OPTION):
        self.OPTION = OPTION
    def add_OPTION(self, value):
        self.OPTION.append(value)
    def insert_OPTION_at(self, index, value):
        self.OPTION.insert(index, value)
    def replace_OPTION_at(self, index, value):
        self.OPTION[index] = value
    def get_DESCRIPTION(self):
        return self.DESCRIPTION
    def set_DESCRIPTION(self, DESCRIPTION):
        self.DESCRIPTION = DESCRIPTION
    def get_DELIVERYINST(self):
        return self.DELIVERYINST
    def set_DELIVERYINST(self, DELIVERYINST):
        self.DELIVERYINST = DELIVERYINST
    def get_CUSTOMCONTROLIN(self):
        return self.CUSTOMCONTROLIN
    def set_CUSTOMCONTROLIN(self, CUSTOMCONTROLIN):
        self.CUSTOMCONTROLIN = CUSTOMCONTROLIN
    def get_HAZARDOUS(self):
        return self.HAZARDOUS
    def set_HAZARDOUS(self, HAZARDOUS):
        self.HAZARDOUS = HAZARDOUS
    def get_UNNUMBER(self):
        return self.UNNUMBER
    def set_UNNUMBER(self, UNNUMBER):
        self.UNNUMBER = UNNUMBER
    def get_PACKINGGROUP(self):
        return self.PACKINGGROUP
    def set_PACKINGGROUP(self, PACKINGGROUP):
        self.PACKINGGROUP = PACKINGGROUP
    def get_PACKAGE(self):
        return self.PACKAGE
    def set_PACKAGE(self, PACKAGE):
        self.PACKAGE = PACKAGE
    def add_PACKAGE(self, value):
        self.PACKAGE.append(value)
    def insert_PACKAGE_at(self, index, value):
        self.PACKAGE.insert(index, value)
    def replace_PACKAGE_at(self, index, value):
        self.PACKAGE[index] = value
    def hasContent_(self):
        if (
            self.RECEIVER is not None or
            self.DELIVERY is not None or
            self.CONNUMBER is not None or
            self.CUSTOMERREF is not None or
            self.CONTYPE is not None or
            self.PAYMENTIND is not None or
            self.ITEMS is not None or
            self.TOTALWEIGHT is not None or
            self.TOTALVOLUME is not None or
            self.CURRENCY is not None or
            self.GOODSVALUE is not None or
            self.INSURANCEVALUE is not None or
            self.INSURANCECURRENCY is not None or
            self.DIVISION is not None or
            self.SERVICE is not None or
            self.OPTION or
            self.DESCRIPTION is not None or
            self.DELIVERYINST is not None or
            self.CUSTOMCONTROLIN is not None or
            self.HAZARDOUS is not None or
            self.UNNUMBER is not None or
            self.PACKINGGROUP is not None or
            self.PACKAGE
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DETAILS', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DETAILS')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DETAILS':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DETAILS')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DETAILS', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DETAILS'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DETAILS', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.RECEIVER is not None:
            namespaceprefix_ = self.RECEIVER_nsprefix_ + ':' if (UseCapturedNS_ and self.RECEIVER_nsprefix_) else ''
            self.RECEIVER.export(outfile, level, namespaceprefix_, namespacedef_='', name_='RECEIVER', pretty_print=pretty_print)
        if self.DELIVERY is not None:
            namespaceprefix_ = self.DELIVERY_nsprefix_ + ':' if (UseCapturedNS_ and self.DELIVERY_nsprefix_) else ''
            self.DELIVERY.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DELIVERY', pretty_print=pretty_print)
        if self.CONNUMBER is not None:
            namespaceprefix_ = self.CONNUMBER_nsprefix_ + ':' if (UseCapturedNS_ and self.CONNUMBER_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONNUMBER>%s</%sCONNUMBER>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONNUMBER), input_name='CONNUMBER')), namespaceprefix_ , eol_))
        if self.CUSTOMERREF is not None:
            namespaceprefix_ = self.CUSTOMERREF_nsprefix_ + ':' if (UseCapturedNS_ and self.CUSTOMERREF_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCUSTOMERREF>%s</%sCUSTOMERREF>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CUSTOMERREF), input_name='CUSTOMERREF')), namespaceprefix_ , eol_))
        if self.CONTYPE is not None:
            namespaceprefix_ = self.CONTYPE_nsprefix_ + ':' if (UseCapturedNS_ and self.CONTYPE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONTYPE>%s</%sCONTYPE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONTYPE), input_name='CONTYPE')), namespaceprefix_ , eol_))
        if self.PAYMENTIND is not None:
            namespaceprefix_ = self.PAYMENTIND_nsprefix_ + ':' if (UseCapturedNS_ and self.PAYMENTIND_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPAYMENTIND>%s</%sPAYMENTIND>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PAYMENTIND), input_name='PAYMENTIND')), namespaceprefix_ , eol_))
        if self.ITEMS is not None:
            namespaceprefix_ = self.ITEMS_nsprefix_ + ':' if (UseCapturedNS_ and self.ITEMS_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sITEMS>%s</%sITEMS>%s' % (namespaceprefix_ , self.gds_format_integer(self.ITEMS, input_name='ITEMS'), namespaceprefix_ , eol_))
        if self.TOTALWEIGHT is not None:
            namespaceprefix_ = self.TOTALWEIGHT_nsprefix_ + ':' if (UseCapturedNS_ and self.TOTALWEIGHT_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTOTALWEIGHT>%s</%sTOTALWEIGHT>%s' % (namespaceprefix_ , self.gds_format_decimal(self.TOTALWEIGHT, input_name='TOTALWEIGHT'), namespaceprefix_ , eol_))
        if self.TOTALVOLUME is not None:
            namespaceprefix_ = self.TOTALVOLUME_nsprefix_ + ':' if (UseCapturedNS_ and self.TOTALVOLUME_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTOTALVOLUME>%s</%sTOTALVOLUME>%s' % (namespaceprefix_ , self.gds_format_decimal(self.TOTALVOLUME, input_name='TOTALVOLUME'), namespaceprefix_ , eol_))
        if self.CURRENCY is not None:
            namespaceprefix_ = self.CURRENCY_nsprefix_ + ':' if (UseCapturedNS_ and self.CURRENCY_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCURRENCY>%s</%sCURRENCY>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CURRENCY), input_name='CURRENCY')), namespaceprefix_ , eol_))
        if self.GOODSVALUE is not None:
            namespaceprefix_ = self.GOODSVALUE_nsprefix_ + ':' if (UseCapturedNS_ and self.GOODSVALUE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGOODSVALUE>%s</%sGOODSVALUE>%s' % (namespaceprefix_ , self.gds_format_decimal(self.GOODSVALUE, input_name='GOODSVALUE'), namespaceprefix_ , eol_))
        if self.INSURANCEVALUE is not None:
            namespaceprefix_ = self.INSURANCEVALUE_nsprefix_ + ':' if (UseCapturedNS_ and self.INSURANCEVALUE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sINSURANCEVALUE>%s</%sINSURANCEVALUE>%s' % (namespaceprefix_ , self.gds_format_decimal(self.INSURANCEVALUE, input_name='INSURANCEVALUE'), namespaceprefix_ , eol_))
        if self.INSURANCECURRENCY is not None:
            namespaceprefix_ = self.INSURANCECURRENCY_nsprefix_ + ':' if (UseCapturedNS_ and self.INSURANCECURRENCY_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sINSURANCECURRENCY>%s</%sINSURANCECURRENCY>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.INSURANCECURRENCY), input_name='INSURANCECURRENCY')), namespaceprefix_ , eol_))
        if self.DIVISION is not None:
            namespaceprefix_ = self.DIVISION_nsprefix_ + ':' if (UseCapturedNS_ and self.DIVISION_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDIVISION>%s</%sDIVISION>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DIVISION), input_name='DIVISION')), namespaceprefix_ , eol_))
        if self.SERVICE is not None:
            namespaceprefix_ = self.SERVICE_nsprefix_ + ':' if (UseCapturedNS_ and self.SERVICE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSERVICE>%s</%sSERVICE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SERVICE), input_name='SERVICE')), namespaceprefix_ , eol_))
        for OPTION_ in self.OPTION:
            namespaceprefix_ = self.OPTION_nsprefix_ + ':' if (UseCapturedNS_ and self.OPTION_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOPTION>%s</%sOPTION>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(OPTION_), input_name='OPTION')), namespaceprefix_ , eol_))
        if self.DESCRIPTION is not None:
            namespaceprefix_ = self.DESCRIPTION_nsprefix_ + ':' if (UseCapturedNS_ and self.DESCRIPTION_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDESCRIPTION>%s</%sDESCRIPTION>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DESCRIPTION), input_name='DESCRIPTION')), namespaceprefix_ , eol_))
        if self.DELIVERYINST is not None:
            namespaceprefix_ = self.DELIVERYINST_nsprefix_ + ':' if (UseCapturedNS_ and self.DELIVERYINST_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDELIVERYINST>%s</%sDELIVERYINST>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DELIVERYINST), input_name='DELIVERYINST')), namespaceprefix_ , eol_))
        if self.CUSTOMCONTROLIN is not None:
            namespaceprefix_ = self.CUSTOMCONTROLIN_nsprefix_ + ':' if (UseCapturedNS_ and self.CUSTOMCONTROLIN_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCUSTOMCONTROLIN>%s</%sCUSTOMCONTROLIN>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CUSTOMCONTROLIN), input_name='CUSTOMCONTROLIN')), namespaceprefix_ , eol_))
        if self.HAZARDOUS is not None:
            namespaceprefix_ = self.HAZARDOUS_nsprefix_ + ':' if (UseCapturedNS_ and self.HAZARDOUS_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHAZARDOUS>%s</%sHAZARDOUS>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HAZARDOUS), input_name='HAZARDOUS')), namespaceprefix_ , eol_))
        if self.UNNUMBER is not None:
            namespaceprefix_ = self.UNNUMBER_nsprefix_ + ':' if (UseCapturedNS_ and self.UNNUMBER_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUNNUMBER>%s</%sUNNUMBER>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UNNUMBER), input_name='UNNUMBER')), namespaceprefix_ , eol_))
        if self.PACKINGGROUP is not None:
            namespaceprefix_ = self.PACKINGGROUP_nsprefix_ + ':' if (UseCapturedNS_ and self.PACKINGGROUP_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPACKINGGROUP>%s</%sPACKINGGROUP>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PACKINGGROUP), input_name='PACKINGGROUP')), namespaceprefix_ , eol_))
        for PACKAGE_ in self.PACKAGE:
            namespaceprefix_ = self.PACKAGE_nsprefix_ + ':' if (UseCapturedNS_ and self.PACKAGE_nsprefix_) else ''
            PACKAGE_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PACKAGE', pretty_print=pretty_print)
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
        if nodeName_ == 'RECEIVER':
            obj_ = RECEIVER.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.RECEIVER = obj_
            obj_.original_tagname_ = 'RECEIVER'
        elif nodeName_ == 'DELIVERY':
            obj_ = DELIVERY.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DELIVERY = obj_
            obj_.original_tagname_ = 'DELIVERY'
        elif nodeName_ == 'CONNUMBER':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONNUMBER')
            value_ = self.gds_validate_string(value_, node, 'CONNUMBER')
            self.CONNUMBER = value_
            self.CONNUMBER_nsprefix_ = child_.prefix
        elif nodeName_ == 'CUSTOMERREF':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CUSTOMERREF')
            value_ = self.gds_validate_string(value_, node, 'CUSTOMERREF')
            self.CUSTOMERREF = value_
            self.CUSTOMERREF_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONTYPE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONTYPE')
            value_ = self.gds_validate_string(value_, node, 'CONTYPE')
            self.CONTYPE = value_
            self.CONTYPE_nsprefix_ = child_.prefix
        elif nodeName_ == 'PAYMENTIND':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PAYMENTIND')
            value_ = self.gds_validate_string(value_, node, 'PAYMENTIND')
            self.PAYMENTIND = value_
            self.PAYMENTIND_nsprefix_ = child_.prefix
        elif nodeName_ == 'ITEMS' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'ITEMS')
            ival_ = self.gds_validate_integer(ival_, node, 'ITEMS')
            self.ITEMS = ival_
            self.ITEMS_nsprefix_ = child_.prefix
        elif nodeName_ == 'TOTALWEIGHT' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'TOTALWEIGHT')
            fval_ = self.gds_validate_decimal(fval_, node, 'TOTALWEIGHT')
            self.TOTALWEIGHT = fval_
            self.TOTALWEIGHT_nsprefix_ = child_.prefix
        elif nodeName_ == 'TOTALVOLUME' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'TOTALVOLUME')
            fval_ = self.gds_validate_decimal(fval_, node, 'TOTALVOLUME')
            self.TOTALVOLUME = fval_
            self.TOTALVOLUME_nsprefix_ = child_.prefix
        elif nodeName_ == 'CURRENCY':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CURRENCY')
            value_ = self.gds_validate_string(value_, node, 'CURRENCY')
            self.CURRENCY = value_
            self.CURRENCY_nsprefix_ = child_.prefix
        elif nodeName_ == 'GOODSVALUE' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'GOODSVALUE')
            fval_ = self.gds_validate_decimal(fval_, node, 'GOODSVALUE')
            self.GOODSVALUE = fval_
            self.GOODSVALUE_nsprefix_ = child_.prefix
        elif nodeName_ == 'INSURANCEVALUE' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'INSURANCEVALUE')
            fval_ = self.gds_validate_decimal(fval_, node, 'INSURANCEVALUE')
            self.INSURANCEVALUE = fval_
            self.INSURANCEVALUE_nsprefix_ = child_.prefix
        elif nodeName_ == 'INSURANCECURRENCY':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'INSURANCECURRENCY')
            value_ = self.gds_validate_string(value_, node, 'INSURANCECURRENCY')
            self.INSURANCECURRENCY = value_
            self.INSURANCECURRENCY_nsprefix_ = child_.prefix
        elif nodeName_ == 'DIVISION':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DIVISION')
            value_ = self.gds_validate_string(value_, node, 'DIVISION')
            self.DIVISION = value_
            self.DIVISION_nsprefix_ = child_.prefix
        elif nodeName_ == 'SERVICE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SERVICE')
            value_ = self.gds_validate_string(value_, node, 'SERVICE')
            self.SERVICE = value_
            self.SERVICE_nsprefix_ = child_.prefix
        elif nodeName_ == 'OPTION':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OPTION')
            value_ = self.gds_validate_string(value_, node, 'OPTION')
            self.OPTION.append(value_)
            self.OPTION_nsprefix_ = child_.prefix
        elif nodeName_ == 'DESCRIPTION':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DESCRIPTION')
            value_ = self.gds_validate_string(value_, node, 'DESCRIPTION')
            self.DESCRIPTION = value_
            self.DESCRIPTION_nsprefix_ = child_.prefix
        elif nodeName_ == 'DELIVERYINST':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DELIVERYINST')
            value_ = self.gds_validate_string(value_, node, 'DELIVERYINST')
            self.DELIVERYINST = value_
            self.DELIVERYINST_nsprefix_ = child_.prefix
        elif nodeName_ == 'CUSTOMCONTROLIN':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CUSTOMCONTROLIN')
            value_ = self.gds_validate_string(value_, node, 'CUSTOMCONTROLIN')
            self.CUSTOMCONTROLIN = value_
            self.CUSTOMCONTROLIN_nsprefix_ = child_.prefix
        elif nodeName_ == 'HAZARDOUS':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HAZARDOUS')
            value_ = self.gds_validate_string(value_, node, 'HAZARDOUS')
            self.HAZARDOUS = value_
            self.HAZARDOUS_nsprefix_ = child_.prefix
        elif nodeName_ == 'UNNUMBER':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UNNUMBER')
            value_ = self.gds_validate_string(value_, node, 'UNNUMBER')
            self.UNNUMBER = value_
            self.UNNUMBER_nsprefix_ = child_.prefix
        elif nodeName_ == 'PACKINGGROUP':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PACKINGGROUP')
            value_ = self.gds_validate_string(value_, node, 'PACKINGGROUP')
            self.PACKINGGROUP = value_
            self.PACKINGGROUP_nsprefix_ = child_.prefix
        elif nodeName_ == 'PACKAGE':
            obj_ = PACKAGE.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PACKAGE.append(obj_)
            obj_.original_tagname_ = 'PACKAGE'
# end class DETAILS


class RECEIVER(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, COMPANYNAME=None, STREETADDRESS1=None, STREETADDRESS2=None, STREETADDRESS3=None, CITY=None, PROVINCE=None, POSTCODE=None, COUNTRY=None, VAT=None, CONTACTNAME=None, CONTACTDIALCODE=None, CONTACTTELEPHONE=None, CONTACTEMAIL=None, ACCOUNT=None, ACCOUNTCOUNTRY=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.COMPANYNAME = COMPANYNAME
        self.COMPANYNAME_nsprefix_ = None
        self.STREETADDRESS1 = STREETADDRESS1
        self.STREETADDRESS1_nsprefix_ = None
        self.STREETADDRESS2 = STREETADDRESS2
        self.STREETADDRESS2_nsprefix_ = None
        self.STREETADDRESS3 = STREETADDRESS3
        self.STREETADDRESS3_nsprefix_ = None
        self.CITY = CITY
        self.CITY_nsprefix_ = None
        self.PROVINCE = PROVINCE
        self.PROVINCE_nsprefix_ = None
        self.POSTCODE = POSTCODE
        self.POSTCODE_nsprefix_ = None
        self.COUNTRY = COUNTRY
        self.COUNTRY_nsprefix_ = None
        self.VAT = VAT
        self.VAT_nsprefix_ = None
        self.CONTACTNAME = CONTACTNAME
        self.CONTACTNAME_nsprefix_ = None
        self.CONTACTDIALCODE = CONTACTDIALCODE
        self.CONTACTDIALCODE_nsprefix_ = None
        self.CONTACTTELEPHONE = CONTACTTELEPHONE
        self.CONTACTTELEPHONE_nsprefix_ = None
        self.CONTACTEMAIL = CONTACTEMAIL
        self.CONTACTEMAIL_nsprefix_ = None
        self.ACCOUNT = ACCOUNT
        self.ACCOUNT_nsprefix_ = None
        self.ACCOUNTCOUNTRY = ACCOUNTCOUNTRY
        self.ACCOUNTCOUNTRY_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RECEIVER)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RECEIVER.subclass:
            return RECEIVER.subclass(*args_, **kwargs_)
        else:
            return RECEIVER(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_COMPANYNAME(self):
        return self.COMPANYNAME
    def set_COMPANYNAME(self, COMPANYNAME):
        self.COMPANYNAME = COMPANYNAME
    def get_STREETADDRESS1(self):
        return self.STREETADDRESS1
    def set_STREETADDRESS1(self, STREETADDRESS1):
        self.STREETADDRESS1 = STREETADDRESS1
    def get_STREETADDRESS2(self):
        return self.STREETADDRESS2
    def set_STREETADDRESS2(self, STREETADDRESS2):
        self.STREETADDRESS2 = STREETADDRESS2
    def get_STREETADDRESS3(self):
        return self.STREETADDRESS3
    def set_STREETADDRESS3(self, STREETADDRESS3):
        self.STREETADDRESS3 = STREETADDRESS3
    def get_CITY(self):
        return self.CITY
    def set_CITY(self, CITY):
        self.CITY = CITY
    def get_PROVINCE(self):
        return self.PROVINCE
    def set_PROVINCE(self, PROVINCE):
        self.PROVINCE = PROVINCE
    def get_POSTCODE(self):
        return self.POSTCODE
    def set_POSTCODE(self, POSTCODE):
        self.POSTCODE = POSTCODE
    def get_COUNTRY(self):
        return self.COUNTRY
    def set_COUNTRY(self, COUNTRY):
        self.COUNTRY = COUNTRY
    def get_VAT(self):
        return self.VAT
    def set_VAT(self, VAT):
        self.VAT = VAT
    def get_CONTACTNAME(self):
        return self.CONTACTNAME
    def set_CONTACTNAME(self, CONTACTNAME):
        self.CONTACTNAME = CONTACTNAME
    def get_CONTACTDIALCODE(self):
        return self.CONTACTDIALCODE
    def set_CONTACTDIALCODE(self, CONTACTDIALCODE):
        self.CONTACTDIALCODE = CONTACTDIALCODE
    def get_CONTACTTELEPHONE(self):
        return self.CONTACTTELEPHONE
    def set_CONTACTTELEPHONE(self, CONTACTTELEPHONE):
        self.CONTACTTELEPHONE = CONTACTTELEPHONE
    def get_CONTACTEMAIL(self):
        return self.CONTACTEMAIL
    def set_CONTACTEMAIL(self, CONTACTEMAIL):
        self.CONTACTEMAIL = CONTACTEMAIL
    def get_ACCOUNT(self):
        return self.ACCOUNT
    def set_ACCOUNT(self, ACCOUNT):
        self.ACCOUNT = ACCOUNT
    def get_ACCOUNTCOUNTRY(self):
        return self.ACCOUNTCOUNTRY
    def set_ACCOUNTCOUNTRY(self, ACCOUNTCOUNTRY):
        self.ACCOUNTCOUNTRY = ACCOUNTCOUNTRY
    def hasContent_(self):
        if (
            self.COMPANYNAME is not None or
            self.STREETADDRESS1 is not None or
            self.STREETADDRESS2 is not None or
            self.STREETADDRESS3 is not None or
            self.CITY is not None or
            self.PROVINCE is not None or
            self.POSTCODE is not None or
            self.COUNTRY is not None or
            self.VAT is not None or
            self.CONTACTNAME is not None or
            self.CONTACTDIALCODE is not None or
            self.CONTACTTELEPHONE is not None or
            self.CONTACTEMAIL is not None or
            self.ACCOUNT is not None or
            self.ACCOUNTCOUNTRY is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RECEIVER', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RECEIVER')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RECEIVER':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RECEIVER')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RECEIVER', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RECEIVER'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RECEIVER', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.COMPANYNAME is not None:
            namespaceprefix_ = self.COMPANYNAME_nsprefix_ + ':' if (UseCapturedNS_ and self.COMPANYNAME_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCOMPANYNAME>%s</%sCOMPANYNAME>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.COMPANYNAME), input_name='COMPANYNAME')), namespaceprefix_ , eol_))
        if self.STREETADDRESS1 is not None:
            namespaceprefix_ = self.STREETADDRESS1_nsprefix_ + ':' if (UseCapturedNS_ and self.STREETADDRESS1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSTREETADDRESS1>%s</%sSTREETADDRESS1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.STREETADDRESS1), input_name='STREETADDRESS1')), namespaceprefix_ , eol_))
        if self.STREETADDRESS2 is not None:
            namespaceprefix_ = self.STREETADDRESS2_nsprefix_ + ':' if (UseCapturedNS_ and self.STREETADDRESS2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSTREETADDRESS2>%s</%sSTREETADDRESS2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.STREETADDRESS2), input_name='STREETADDRESS2')), namespaceprefix_ , eol_))
        if self.STREETADDRESS3 is not None:
            namespaceprefix_ = self.STREETADDRESS3_nsprefix_ + ':' if (UseCapturedNS_ and self.STREETADDRESS3_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSTREETADDRESS3>%s</%sSTREETADDRESS3>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.STREETADDRESS3), input_name='STREETADDRESS3')), namespaceprefix_ , eol_))
        if self.CITY is not None:
            namespaceprefix_ = self.CITY_nsprefix_ + ':' if (UseCapturedNS_ and self.CITY_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCITY>%s</%sCITY>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CITY), input_name='CITY')), namespaceprefix_ , eol_))
        if self.PROVINCE is not None:
            namespaceprefix_ = self.PROVINCE_nsprefix_ + ':' if (UseCapturedNS_ and self.PROVINCE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPROVINCE>%s</%sPROVINCE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PROVINCE), input_name='PROVINCE')), namespaceprefix_ , eol_))
        if self.POSTCODE is not None:
            namespaceprefix_ = self.POSTCODE_nsprefix_ + ':' if (UseCapturedNS_ and self.POSTCODE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPOSTCODE>%s</%sPOSTCODE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.POSTCODE), input_name='POSTCODE')), namespaceprefix_ , eol_))
        if self.COUNTRY is not None:
            namespaceprefix_ = self.COUNTRY_nsprefix_ + ':' if (UseCapturedNS_ and self.COUNTRY_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCOUNTRY>%s</%sCOUNTRY>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.COUNTRY), input_name='COUNTRY')), namespaceprefix_ , eol_))
        if self.VAT is not None:
            namespaceprefix_ = self.VAT_nsprefix_ + ':' if (UseCapturedNS_ and self.VAT_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sVAT>%s</%sVAT>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.VAT), input_name='VAT')), namespaceprefix_ , eol_))
        if self.CONTACTNAME is not None:
            namespaceprefix_ = self.CONTACTNAME_nsprefix_ + ':' if (UseCapturedNS_ and self.CONTACTNAME_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONTACTNAME>%s</%sCONTACTNAME>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONTACTNAME), input_name='CONTACTNAME')), namespaceprefix_ , eol_))
        if self.CONTACTDIALCODE is not None:
            namespaceprefix_ = self.CONTACTDIALCODE_nsprefix_ + ':' if (UseCapturedNS_ and self.CONTACTDIALCODE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONTACTDIALCODE>%s</%sCONTACTDIALCODE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONTACTDIALCODE), input_name='CONTACTDIALCODE')), namespaceprefix_ , eol_))
        if self.CONTACTTELEPHONE is not None:
            namespaceprefix_ = self.CONTACTTELEPHONE_nsprefix_ + ':' if (UseCapturedNS_ and self.CONTACTTELEPHONE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONTACTTELEPHONE>%s</%sCONTACTTELEPHONE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONTACTTELEPHONE), input_name='CONTACTTELEPHONE')), namespaceprefix_ , eol_))
        if self.CONTACTEMAIL is not None:
            namespaceprefix_ = self.CONTACTEMAIL_nsprefix_ + ':' if (UseCapturedNS_ and self.CONTACTEMAIL_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONTACTEMAIL>%s</%sCONTACTEMAIL>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONTACTEMAIL), input_name='CONTACTEMAIL')), namespaceprefix_ , eol_))
        if self.ACCOUNT is not None:
            namespaceprefix_ = self.ACCOUNT_nsprefix_ + ':' if (UseCapturedNS_ and self.ACCOUNT_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sACCOUNT>%s</%sACCOUNT>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ACCOUNT), input_name='ACCOUNT')), namespaceprefix_ , eol_))
        if self.ACCOUNTCOUNTRY is not None:
            namespaceprefix_ = self.ACCOUNTCOUNTRY_nsprefix_ + ':' if (UseCapturedNS_ and self.ACCOUNTCOUNTRY_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sACCOUNTCOUNTRY>%s</%sACCOUNTCOUNTRY>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ACCOUNTCOUNTRY), input_name='ACCOUNTCOUNTRY')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'COMPANYNAME':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'COMPANYNAME')
            value_ = self.gds_validate_string(value_, node, 'COMPANYNAME')
            self.COMPANYNAME = value_
            self.COMPANYNAME_nsprefix_ = child_.prefix
        elif nodeName_ == 'STREETADDRESS1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'STREETADDRESS1')
            value_ = self.gds_validate_string(value_, node, 'STREETADDRESS1')
            self.STREETADDRESS1 = value_
            self.STREETADDRESS1_nsprefix_ = child_.prefix
        elif nodeName_ == 'STREETADDRESS2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'STREETADDRESS2')
            value_ = self.gds_validate_string(value_, node, 'STREETADDRESS2')
            self.STREETADDRESS2 = value_
            self.STREETADDRESS2_nsprefix_ = child_.prefix
        elif nodeName_ == 'STREETADDRESS3':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'STREETADDRESS3')
            value_ = self.gds_validate_string(value_, node, 'STREETADDRESS3')
            self.STREETADDRESS3 = value_
            self.STREETADDRESS3_nsprefix_ = child_.prefix
        elif nodeName_ == 'CITY':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CITY')
            value_ = self.gds_validate_string(value_, node, 'CITY')
            self.CITY = value_
            self.CITY_nsprefix_ = child_.prefix
        elif nodeName_ == 'PROVINCE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PROVINCE')
            value_ = self.gds_validate_string(value_, node, 'PROVINCE')
            self.PROVINCE = value_
            self.PROVINCE_nsprefix_ = child_.prefix
        elif nodeName_ == 'POSTCODE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'POSTCODE')
            value_ = self.gds_validate_string(value_, node, 'POSTCODE')
            self.POSTCODE = value_
            self.POSTCODE_nsprefix_ = child_.prefix
        elif nodeName_ == 'COUNTRY':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'COUNTRY')
            value_ = self.gds_validate_string(value_, node, 'COUNTRY')
            self.COUNTRY = value_
            self.COUNTRY_nsprefix_ = child_.prefix
        elif nodeName_ == 'VAT':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'VAT')
            value_ = self.gds_validate_string(value_, node, 'VAT')
            self.VAT = value_
            self.VAT_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONTACTNAME':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONTACTNAME')
            value_ = self.gds_validate_string(value_, node, 'CONTACTNAME')
            self.CONTACTNAME = value_
            self.CONTACTNAME_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONTACTDIALCODE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONTACTDIALCODE')
            value_ = self.gds_validate_string(value_, node, 'CONTACTDIALCODE')
            self.CONTACTDIALCODE = value_
            self.CONTACTDIALCODE_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONTACTTELEPHONE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONTACTTELEPHONE')
            value_ = self.gds_validate_string(value_, node, 'CONTACTTELEPHONE')
            self.CONTACTTELEPHONE = value_
            self.CONTACTTELEPHONE_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONTACTEMAIL':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONTACTEMAIL')
            value_ = self.gds_validate_string(value_, node, 'CONTACTEMAIL')
            self.CONTACTEMAIL = value_
            self.CONTACTEMAIL_nsprefix_ = child_.prefix
        elif nodeName_ == 'ACCOUNT':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ACCOUNT')
            value_ = self.gds_validate_string(value_, node, 'ACCOUNT')
            self.ACCOUNT = value_
            self.ACCOUNT_nsprefix_ = child_.prefix
        elif nodeName_ == 'ACCOUNTCOUNTRY':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ACCOUNTCOUNTRY')
            value_ = self.gds_validate_string(value_, node, 'ACCOUNTCOUNTRY')
            self.ACCOUNTCOUNTRY = value_
            self.ACCOUNTCOUNTRY_nsprefix_ = child_.prefix
# end class RECEIVER


class DELIVERY(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, COMPANYNAME=None, STREETADDRESS1=None, STREETADDRESS2=None, STREETADDRESS3=None, CITY=None, PROVINCE=None, POSTCODE=None, COUNTRY=None, VAT=None, CONTACTNAME=None, CONTACTDIALCODE=None, CONTACTTELEPHONE=None, CONTACTEMAIL=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.COMPANYNAME = COMPANYNAME
        self.COMPANYNAME_nsprefix_ = None
        self.STREETADDRESS1 = STREETADDRESS1
        self.STREETADDRESS1_nsprefix_ = None
        self.STREETADDRESS2 = STREETADDRESS2
        self.STREETADDRESS2_nsprefix_ = None
        self.STREETADDRESS3 = STREETADDRESS3
        self.STREETADDRESS3_nsprefix_ = None
        self.CITY = CITY
        self.CITY_nsprefix_ = None
        self.PROVINCE = PROVINCE
        self.PROVINCE_nsprefix_ = None
        self.POSTCODE = POSTCODE
        self.POSTCODE_nsprefix_ = None
        self.COUNTRY = COUNTRY
        self.COUNTRY_nsprefix_ = None
        self.VAT = VAT
        self.VAT_nsprefix_ = None
        self.CONTACTNAME = CONTACTNAME
        self.CONTACTNAME_nsprefix_ = None
        self.CONTACTDIALCODE = CONTACTDIALCODE
        self.CONTACTDIALCODE_nsprefix_ = None
        self.CONTACTTELEPHONE = CONTACTTELEPHONE
        self.CONTACTTELEPHONE_nsprefix_ = None
        self.CONTACTEMAIL = CONTACTEMAIL
        self.CONTACTEMAIL_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DELIVERY)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DELIVERY.subclass:
            return DELIVERY.subclass(*args_, **kwargs_)
        else:
            return DELIVERY(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_COMPANYNAME(self):
        return self.COMPANYNAME
    def set_COMPANYNAME(self, COMPANYNAME):
        self.COMPANYNAME = COMPANYNAME
    def get_STREETADDRESS1(self):
        return self.STREETADDRESS1
    def set_STREETADDRESS1(self, STREETADDRESS1):
        self.STREETADDRESS1 = STREETADDRESS1
    def get_STREETADDRESS2(self):
        return self.STREETADDRESS2
    def set_STREETADDRESS2(self, STREETADDRESS2):
        self.STREETADDRESS2 = STREETADDRESS2
    def get_STREETADDRESS3(self):
        return self.STREETADDRESS3
    def set_STREETADDRESS3(self, STREETADDRESS3):
        self.STREETADDRESS3 = STREETADDRESS3
    def get_CITY(self):
        return self.CITY
    def set_CITY(self, CITY):
        self.CITY = CITY
    def get_PROVINCE(self):
        return self.PROVINCE
    def set_PROVINCE(self, PROVINCE):
        self.PROVINCE = PROVINCE
    def get_POSTCODE(self):
        return self.POSTCODE
    def set_POSTCODE(self, POSTCODE):
        self.POSTCODE = POSTCODE
    def get_COUNTRY(self):
        return self.COUNTRY
    def set_COUNTRY(self, COUNTRY):
        self.COUNTRY = COUNTRY
    def get_VAT(self):
        return self.VAT
    def set_VAT(self, VAT):
        self.VAT = VAT
    def get_CONTACTNAME(self):
        return self.CONTACTNAME
    def set_CONTACTNAME(self, CONTACTNAME):
        self.CONTACTNAME = CONTACTNAME
    def get_CONTACTDIALCODE(self):
        return self.CONTACTDIALCODE
    def set_CONTACTDIALCODE(self, CONTACTDIALCODE):
        self.CONTACTDIALCODE = CONTACTDIALCODE
    def get_CONTACTTELEPHONE(self):
        return self.CONTACTTELEPHONE
    def set_CONTACTTELEPHONE(self, CONTACTTELEPHONE):
        self.CONTACTTELEPHONE = CONTACTTELEPHONE
    def get_CONTACTEMAIL(self):
        return self.CONTACTEMAIL
    def set_CONTACTEMAIL(self, CONTACTEMAIL):
        self.CONTACTEMAIL = CONTACTEMAIL
    def hasContent_(self):
        if (
            self.COMPANYNAME is not None or
            self.STREETADDRESS1 is not None or
            self.STREETADDRESS2 is not None or
            self.STREETADDRESS3 is not None or
            self.CITY is not None or
            self.PROVINCE is not None or
            self.POSTCODE is not None or
            self.COUNTRY is not None or
            self.VAT is not None or
            self.CONTACTNAME is not None or
            self.CONTACTDIALCODE is not None or
            self.CONTACTTELEPHONE is not None or
            self.CONTACTEMAIL is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DELIVERY', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DELIVERY')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DELIVERY':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DELIVERY')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DELIVERY', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DELIVERY'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DELIVERY', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.COMPANYNAME is not None:
            namespaceprefix_ = self.COMPANYNAME_nsprefix_ + ':' if (UseCapturedNS_ and self.COMPANYNAME_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCOMPANYNAME>%s</%sCOMPANYNAME>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.COMPANYNAME), input_name='COMPANYNAME')), namespaceprefix_ , eol_))
        if self.STREETADDRESS1 is not None:
            namespaceprefix_ = self.STREETADDRESS1_nsprefix_ + ':' if (UseCapturedNS_ and self.STREETADDRESS1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSTREETADDRESS1>%s</%sSTREETADDRESS1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.STREETADDRESS1), input_name='STREETADDRESS1')), namespaceprefix_ , eol_))
        if self.STREETADDRESS2 is not None:
            namespaceprefix_ = self.STREETADDRESS2_nsprefix_ + ':' if (UseCapturedNS_ and self.STREETADDRESS2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSTREETADDRESS2>%s</%sSTREETADDRESS2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.STREETADDRESS2), input_name='STREETADDRESS2')), namespaceprefix_ , eol_))
        if self.STREETADDRESS3 is not None:
            namespaceprefix_ = self.STREETADDRESS3_nsprefix_ + ':' if (UseCapturedNS_ and self.STREETADDRESS3_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSTREETADDRESS3>%s</%sSTREETADDRESS3>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.STREETADDRESS3), input_name='STREETADDRESS3')), namespaceprefix_ , eol_))
        if self.CITY is not None:
            namespaceprefix_ = self.CITY_nsprefix_ + ':' if (UseCapturedNS_ and self.CITY_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCITY>%s</%sCITY>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CITY), input_name='CITY')), namespaceprefix_ , eol_))
        if self.PROVINCE is not None:
            namespaceprefix_ = self.PROVINCE_nsprefix_ + ':' if (UseCapturedNS_ and self.PROVINCE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPROVINCE>%s</%sPROVINCE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PROVINCE), input_name='PROVINCE')), namespaceprefix_ , eol_))
        if self.POSTCODE is not None:
            namespaceprefix_ = self.POSTCODE_nsprefix_ + ':' if (UseCapturedNS_ and self.POSTCODE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPOSTCODE>%s</%sPOSTCODE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.POSTCODE), input_name='POSTCODE')), namespaceprefix_ , eol_))
        if self.COUNTRY is not None:
            namespaceprefix_ = self.COUNTRY_nsprefix_ + ':' if (UseCapturedNS_ and self.COUNTRY_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCOUNTRY>%s</%sCOUNTRY>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.COUNTRY), input_name='COUNTRY')), namespaceprefix_ , eol_))
        if self.VAT is not None:
            namespaceprefix_ = self.VAT_nsprefix_ + ':' if (UseCapturedNS_ and self.VAT_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sVAT>%s</%sVAT>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.VAT), input_name='VAT')), namespaceprefix_ , eol_))
        if self.CONTACTNAME is not None:
            namespaceprefix_ = self.CONTACTNAME_nsprefix_ + ':' if (UseCapturedNS_ and self.CONTACTNAME_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONTACTNAME>%s</%sCONTACTNAME>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONTACTNAME), input_name='CONTACTNAME')), namespaceprefix_ , eol_))
        if self.CONTACTDIALCODE is not None:
            namespaceprefix_ = self.CONTACTDIALCODE_nsprefix_ + ':' if (UseCapturedNS_ and self.CONTACTDIALCODE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONTACTDIALCODE>%s</%sCONTACTDIALCODE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONTACTDIALCODE), input_name='CONTACTDIALCODE')), namespaceprefix_ , eol_))
        if self.CONTACTTELEPHONE is not None:
            namespaceprefix_ = self.CONTACTTELEPHONE_nsprefix_ + ':' if (UseCapturedNS_ and self.CONTACTTELEPHONE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONTACTTELEPHONE>%s</%sCONTACTTELEPHONE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONTACTTELEPHONE), input_name='CONTACTTELEPHONE')), namespaceprefix_ , eol_))
        if self.CONTACTEMAIL is not None:
            namespaceprefix_ = self.CONTACTEMAIL_nsprefix_ + ':' if (UseCapturedNS_ and self.CONTACTEMAIL_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONTACTEMAIL>%s</%sCONTACTEMAIL>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CONTACTEMAIL), input_name='CONTACTEMAIL')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'COMPANYNAME':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'COMPANYNAME')
            value_ = self.gds_validate_string(value_, node, 'COMPANYNAME')
            self.COMPANYNAME = value_
            self.COMPANYNAME_nsprefix_ = child_.prefix
        elif nodeName_ == 'STREETADDRESS1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'STREETADDRESS1')
            value_ = self.gds_validate_string(value_, node, 'STREETADDRESS1')
            self.STREETADDRESS1 = value_
            self.STREETADDRESS1_nsprefix_ = child_.prefix
        elif nodeName_ == 'STREETADDRESS2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'STREETADDRESS2')
            value_ = self.gds_validate_string(value_, node, 'STREETADDRESS2')
            self.STREETADDRESS2 = value_
            self.STREETADDRESS2_nsprefix_ = child_.prefix
        elif nodeName_ == 'STREETADDRESS3':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'STREETADDRESS3')
            value_ = self.gds_validate_string(value_, node, 'STREETADDRESS3')
            self.STREETADDRESS3 = value_
            self.STREETADDRESS3_nsprefix_ = child_.prefix
        elif nodeName_ == 'CITY':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CITY')
            value_ = self.gds_validate_string(value_, node, 'CITY')
            self.CITY = value_
            self.CITY_nsprefix_ = child_.prefix
        elif nodeName_ == 'PROVINCE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PROVINCE')
            value_ = self.gds_validate_string(value_, node, 'PROVINCE')
            self.PROVINCE = value_
            self.PROVINCE_nsprefix_ = child_.prefix
        elif nodeName_ == 'POSTCODE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'POSTCODE')
            value_ = self.gds_validate_string(value_, node, 'POSTCODE')
            self.POSTCODE = value_
            self.POSTCODE_nsprefix_ = child_.prefix
        elif nodeName_ == 'COUNTRY':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'COUNTRY')
            value_ = self.gds_validate_string(value_, node, 'COUNTRY')
            self.COUNTRY = value_
            self.COUNTRY_nsprefix_ = child_.prefix
        elif nodeName_ == 'VAT':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'VAT')
            value_ = self.gds_validate_string(value_, node, 'VAT')
            self.VAT = value_
            self.VAT_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONTACTNAME':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONTACTNAME')
            value_ = self.gds_validate_string(value_, node, 'CONTACTNAME')
            self.CONTACTNAME = value_
            self.CONTACTNAME_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONTACTDIALCODE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONTACTDIALCODE')
            value_ = self.gds_validate_string(value_, node, 'CONTACTDIALCODE')
            self.CONTACTDIALCODE = value_
            self.CONTACTDIALCODE_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONTACTTELEPHONE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONTACTTELEPHONE')
            value_ = self.gds_validate_string(value_, node, 'CONTACTTELEPHONE')
            self.CONTACTTELEPHONE = value_
            self.CONTACTTELEPHONE_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONTACTEMAIL':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONTACTEMAIL')
            value_ = self.gds_validate_string(value_, node, 'CONTACTEMAIL')
            self.CONTACTEMAIL = value_
            self.CONTACTEMAIL_nsprefix_ = child_.prefix
# end class DELIVERY


class PACKAGE(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ITEMS=None, DESCRIPTION=None, LENGTH=None, HEIGHT=None, WIDTH=None, WEIGHT=None, ARTICLE=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ITEMS = ITEMS
        self.ITEMS_nsprefix_ = None
        self.DESCRIPTION = DESCRIPTION
        self.DESCRIPTION_nsprefix_ = None
        self.LENGTH = LENGTH
        self.LENGTH_nsprefix_ = None
        self.HEIGHT = HEIGHT
        self.HEIGHT_nsprefix_ = None
        self.WIDTH = WIDTH
        self.WIDTH_nsprefix_ = None
        self.WEIGHT = WEIGHT
        self.WEIGHT_nsprefix_ = None
        if ARTICLE is None:
            self.ARTICLE = []
        else:
            self.ARTICLE = ARTICLE
        self.ARTICLE_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PACKAGE)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PACKAGE.subclass:
            return PACKAGE.subclass(*args_, **kwargs_)
        else:
            return PACKAGE(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ITEMS(self):
        return self.ITEMS
    def set_ITEMS(self, ITEMS):
        self.ITEMS = ITEMS
    def get_DESCRIPTION(self):
        return self.DESCRIPTION
    def set_DESCRIPTION(self, DESCRIPTION):
        self.DESCRIPTION = DESCRIPTION
    def get_LENGTH(self):
        return self.LENGTH
    def set_LENGTH(self, LENGTH):
        self.LENGTH = LENGTH
    def get_HEIGHT(self):
        return self.HEIGHT
    def set_HEIGHT(self, HEIGHT):
        self.HEIGHT = HEIGHT
    def get_WIDTH(self):
        return self.WIDTH
    def set_WIDTH(self, WIDTH):
        self.WIDTH = WIDTH
    def get_WEIGHT(self):
        return self.WEIGHT
    def set_WEIGHT(self, WEIGHT):
        self.WEIGHT = WEIGHT
    def get_ARTICLE(self):
        return self.ARTICLE
    def set_ARTICLE(self, ARTICLE):
        self.ARTICLE = ARTICLE
    def add_ARTICLE(self, value):
        self.ARTICLE.append(value)
    def insert_ARTICLE_at(self, index, value):
        self.ARTICLE.insert(index, value)
    def replace_ARTICLE_at(self, index, value):
        self.ARTICLE[index] = value
    def hasContent_(self):
        if (
            self.ITEMS is not None or
            self.DESCRIPTION is not None or
            self.LENGTH is not None or
            self.HEIGHT is not None or
            self.WIDTH is not None or
            self.WEIGHT is not None or
            self.ARTICLE
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PACKAGE', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PACKAGE')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PACKAGE':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PACKAGE')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PACKAGE', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PACKAGE'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PACKAGE', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ITEMS is not None:
            namespaceprefix_ = self.ITEMS_nsprefix_ + ':' if (UseCapturedNS_ and self.ITEMS_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sITEMS>%s</%sITEMS>%s' % (namespaceprefix_ , self.gds_format_integer(self.ITEMS, input_name='ITEMS'), namespaceprefix_ , eol_))
        if self.DESCRIPTION is not None:
            namespaceprefix_ = self.DESCRIPTION_nsprefix_ + ':' if (UseCapturedNS_ and self.DESCRIPTION_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDESCRIPTION>%s</%sDESCRIPTION>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DESCRIPTION), input_name='DESCRIPTION')), namespaceprefix_ , eol_))
        if self.LENGTH is not None:
            namespaceprefix_ = self.LENGTH_nsprefix_ + ':' if (UseCapturedNS_ and self.LENGTH_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLENGTH>%s</%sLENGTH>%s' % (namespaceprefix_ , self.gds_format_decimal(self.LENGTH, input_name='LENGTH'), namespaceprefix_ , eol_))
        if self.HEIGHT is not None:
            namespaceprefix_ = self.HEIGHT_nsprefix_ + ':' if (UseCapturedNS_ and self.HEIGHT_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHEIGHT>%s</%sHEIGHT>%s' % (namespaceprefix_ , self.gds_format_decimal(self.HEIGHT, input_name='HEIGHT'), namespaceprefix_ , eol_))
        if self.WIDTH is not None:
            namespaceprefix_ = self.WIDTH_nsprefix_ + ':' if (UseCapturedNS_ and self.WIDTH_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWIDTH>%s</%sWIDTH>%s' % (namespaceprefix_ , self.gds_format_decimal(self.WIDTH, input_name='WIDTH'), namespaceprefix_ , eol_))
        if self.WEIGHT is not None:
            namespaceprefix_ = self.WEIGHT_nsprefix_ + ':' if (UseCapturedNS_ and self.WEIGHT_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWEIGHT>%s</%sWEIGHT>%s' % (namespaceprefix_ , self.gds_format_decimal(self.WEIGHT, input_name='WEIGHT'), namespaceprefix_ , eol_))
        for ARTICLE_ in self.ARTICLE:
            namespaceprefix_ = self.ARTICLE_nsprefix_ + ':' if (UseCapturedNS_ and self.ARTICLE_nsprefix_) else ''
            ARTICLE_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ARTICLE', pretty_print=pretty_print)
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
        if nodeName_ == 'ITEMS' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'ITEMS')
            ival_ = self.gds_validate_integer(ival_, node, 'ITEMS')
            self.ITEMS = ival_
            self.ITEMS_nsprefix_ = child_.prefix
        elif nodeName_ == 'DESCRIPTION':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DESCRIPTION')
            value_ = self.gds_validate_string(value_, node, 'DESCRIPTION')
            self.DESCRIPTION = value_
            self.DESCRIPTION_nsprefix_ = child_.prefix
        elif nodeName_ == 'LENGTH' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'LENGTH')
            fval_ = self.gds_validate_decimal(fval_, node, 'LENGTH')
            self.LENGTH = fval_
            self.LENGTH_nsprefix_ = child_.prefix
        elif nodeName_ == 'HEIGHT' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'HEIGHT')
            fval_ = self.gds_validate_decimal(fval_, node, 'HEIGHT')
            self.HEIGHT = fval_
            self.HEIGHT_nsprefix_ = child_.prefix
        elif nodeName_ == 'WIDTH' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'WIDTH')
            fval_ = self.gds_validate_decimal(fval_, node, 'WIDTH')
            self.WIDTH = fval_
            self.WIDTH_nsprefix_ = child_.prefix
        elif nodeName_ == 'WEIGHT' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'WEIGHT')
            fval_ = self.gds_validate_decimal(fval_, node, 'WEIGHT')
            self.WEIGHT = fval_
            self.WEIGHT_nsprefix_ = child_.prefix
        elif nodeName_ == 'ARTICLE':
            obj_ = ARTICLE.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ARTICLE.append(obj_)
            obj_.original_tagname_ = 'ARTICLE'
# end class PACKAGE


class ARTICLE(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ITEMS=None, DESCRIPTION=None, WEIGHT=None, INVOICEVALUE=None, INVOICEDESC=None, HTS=None, COUNTRY=None, EMRN=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ITEMS = ITEMS
        self.ITEMS_nsprefix_ = None
        self.DESCRIPTION = DESCRIPTION
        self.DESCRIPTION_nsprefix_ = None
        self.WEIGHT = WEIGHT
        self.WEIGHT_nsprefix_ = None
        self.INVOICEVALUE = INVOICEVALUE
        self.INVOICEVALUE_nsprefix_ = None
        self.INVOICEDESC = INVOICEDESC
        self.INVOICEDESC_nsprefix_ = None
        self.HTS = HTS
        self.HTS_nsprefix_ = None
        self.COUNTRY = COUNTRY
        self.COUNTRY_nsprefix_ = None
        self.EMRN = EMRN
        self.EMRN_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ARTICLE)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ARTICLE.subclass:
            return ARTICLE.subclass(*args_, **kwargs_)
        else:
            return ARTICLE(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ITEMS(self):
        return self.ITEMS
    def set_ITEMS(self, ITEMS):
        self.ITEMS = ITEMS
    def get_DESCRIPTION(self):
        return self.DESCRIPTION
    def set_DESCRIPTION(self, DESCRIPTION):
        self.DESCRIPTION = DESCRIPTION
    def get_WEIGHT(self):
        return self.WEIGHT
    def set_WEIGHT(self, WEIGHT):
        self.WEIGHT = WEIGHT
    def get_INVOICEVALUE(self):
        return self.INVOICEVALUE
    def set_INVOICEVALUE(self, INVOICEVALUE):
        self.INVOICEVALUE = INVOICEVALUE
    def get_INVOICEDESC(self):
        return self.INVOICEDESC
    def set_INVOICEDESC(self, INVOICEDESC):
        self.INVOICEDESC = INVOICEDESC
    def get_HTS(self):
        return self.HTS
    def set_HTS(self, HTS):
        self.HTS = HTS
    def get_COUNTRY(self):
        return self.COUNTRY
    def set_COUNTRY(self, COUNTRY):
        self.COUNTRY = COUNTRY
    def get_EMRN(self):
        return self.EMRN
    def set_EMRN(self, EMRN):
        self.EMRN = EMRN
    def hasContent_(self):
        if (
            self.ITEMS is not None or
            self.DESCRIPTION is not None or
            self.WEIGHT is not None or
            self.INVOICEVALUE is not None or
            self.INVOICEDESC is not None or
            self.HTS is not None or
            self.COUNTRY is not None or
            self.EMRN is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ARTICLE', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ARTICLE')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ARTICLE':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ARTICLE')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ARTICLE', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ARTICLE'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ARTICLE', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ITEMS is not None:
            namespaceprefix_ = self.ITEMS_nsprefix_ + ':' if (UseCapturedNS_ and self.ITEMS_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sITEMS>%s</%sITEMS>%s' % (namespaceprefix_ , self.gds_format_integer(self.ITEMS, input_name='ITEMS'), namespaceprefix_ , eol_))
        if self.DESCRIPTION is not None:
            namespaceprefix_ = self.DESCRIPTION_nsprefix_ + ':' if (UseCapturedNS_ and self.DESCRIPTION_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDESCRIPTION>%s</%sDESCRIPTION>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DESCRIPTION), input_name='DESCRIPTION')), namespaceprefix_ , eol_))
        if self.WEIGHT is not None:
            namespaceprefix_ = self.WEIGHT_nsprefix_ + ':' if (UseCapturedNS_ and self.WEIGHT_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWEIGHT>%s</%sWEIGHT>%s' % (namespaceprefix_ , self.gds_format_decimal(self.WEIGHT, input_name='WEIGHT'), namespaceprefix_ , eol_))
        if self.INVOICEVALUE is not None:
            namespaceprefix_ = self.INVOICEVALUE_nsprefix_ + ':' if (UseCapturedNS_ and self.INVOICEVALUE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sINVOICEVALUE>%s</%sINVOICEVALUE>%s' % (namespaceprefix_ , self.gds_format_decimal(self.INVOICEVALUE, input_name='INVOICEVALUE'), namespaceprefix_ , eol_))
        if self.INVOICEDESC is not None:
            namespaceprefix_ = self.INVOICEDESC_nsprefix_ + ':' if (UseCapturedNS_ and self.INVOICEDESC_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sINVOICEDESC>%s</%sINVOICEDESC>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.INVOICEDESC), input_name='INVOICEDESC')), namespaceprefix_ , eol_))
        if self.HTS is not None:
            namespaceprefix_ = self.HTS_nsprefix_ + ':' if (UseCapturedNS_ and self.HTS_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHTS>%s</%sHTS>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HTS), input_name='HTS')), namespaceprefix_ , eol_))
        if self.COUNTRY is not None:
            namespaceprefix_ = self.COUNTRY_nsprefix_ + ':' if (UseCapturedNS_ and self.COUNTRY_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCOUNTRY>%s</%sCOUNTRY>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.COUNTRY), input_name='COUNTRY')), namespaceprefix_ , eol_))
        if self.EMRN is not None:
            namespaceprefix_ = self.EMRN_nsprefix_ + ':' if (UseCapturedNS_ and self.EMRN_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEMRN>%s</%sEMRN>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EMRN), input_name='EMRN')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ITEMS' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'ITEMS')
            ival_ = self.gds_validate_integer(ival_, node, 'ITEMS')
            self.ITEMS = ival_
            self.ITEMS_nsprefix_ = child_.prefix
        elif nodeName_ == 'DESCRIPTION':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DESCRIPTION')
            value_ = self.gds_validate_string(value_, node, 'DESCRIPTION')
            self.DESCRIPTION = value_
            self.DESCRIPTION_nsprefix_ = child_.prefix
        elif nodeName_ == 'WEIGHT' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'WEIGHT')
            fval_ = self.gds_validate_decimal(fval_, node, 'WEIGHT')
            self.WEIGHT = fval_
            self.WEIGHT_nsprefix_ = child_.prefix
        elif nodeName_ == 'INVOICEVALUE' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'INVOICEVALUE')
            fval_ = self.gds_validate_decimal(fval_, node, 'INVOICEVALUE')
            self.INVOICEVALUE = fval_
            self.INVOICEVALUE_nsprefix_ = child_.prefix
        elif nodeName_ == 'INVOICEDESC':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'INVOICEDESC')
            value_ = self.gds_validate_string(value_, node, 'INVOICEDESC')
            self.INVOICEDESC = value_
            self.INVOICEDESC_nsprefix_ = child_.prefix
        elif nodeName_ == 'HTS':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HTS')
            value_ = self.gds_validate_string(value_, node, 'HTS')
            self.HTS = value_
            self.HTS_nsprefix_ = child_.prefix
        elif nodeName_ == 'COUNTRY':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'COUNTRY')
            value_ = self.gds_validate_string(value_, node, 'COUNTRY')
            self.COUNTRY = value_
            self.COUNTRY_nsprefix_ = child_.prefix
        elif nodeName_ == 'EMRN':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EMRN')
            value_ = self.gds_validate_string(value_, node, 'EMRN')
            self.EMRN = value_
            self.EMRN_nsprefix_ = child_.prefix
# end class ARTICLE


class ACTIVITY(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CREATE=None, RATE=None, BOOK=None, SHIP=None, PRINT=None, SHOW_GROUPCODE=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
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
        self.SHOW_GROUPCODE = SHOW_GROUPCODE
        self.SHOW_GROUPCODE_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ACTIVITY)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ACTIVITY.subclass:
            return ACTIVITY.subclass(*args_, **kwargs_)
        else:
            return ACTIVITY(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CREATE(self):
        return self.CREATE
    def set_CREATE(self, CREATE):
        self.CREATE = CREATE
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
    def get_SHOW_GROUPCODE(self):
        return self.SHOW_GROUPCODE
    def set_SHOW_GROUPCODE(self, SHOW_GROUPCODE):
        self.SHOW_GROUPCODE = SHOW_GROUPCODE
    def hasContent_(self):
        if (
            self.CREATE is not None or
            self.RATE is not None or
            self.BOOK is not None or
            self.SHIP is not None or
            self.PRINT is not None or
            self.SHOW_GROUPCODE is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ACTIVITY', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ACTIVITY')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ACTIVITY':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ACTIVITY')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ACTIVITY', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ACTIVITY'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ACTIVITY', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CREATE is not None:
            namespaceprefix_ = self.CREATE_nsprefix_ + ':' if (UseCapturedNS_ and self.CREATE_nsprefix_) else ''
            self.CREATE.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CREATE', pretty_print=pretty_print)
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
        if self.SHOW_GROUPCODE is not None:
            namespaceprefix_ = self.SHOW_GROUPCODE_nsprefix_ + ':' if (UseCapturedNS_ and self.SHOW_GROUPCODE_nsprefix_) else ''
            self.SHOW_GROUPCODE.export(outfile, level, namespaceprefix_, namespacedef_='', name_='SHOW_GROUPCODE', pretty_print=pretty_print)
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
        if nodeName_ == 'CREATE':
            obj_ = CREATE.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CREATE = obj_
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
        elif nodeName_ == 'SHOW_GROUPCODE':
            obj_ = SHOW_GROUPCODE.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SHOW_GROUPCODE = obj_
            obj_.original_tagname_ = 'SHOW_GROUPCODE'
# end class ACTIVITY


class CREATE(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CONREF=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if CONREF is None:
            self.CONREF = []
        else:
            self.CONREF = CONREF
        self.CONREF_nsprefix_ = None
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
    def add_CONREF(self, value):
        self.CONREF.append(value)
    def insert_CONREF_at(self, index, value):
        self.CONREF.insert(index, value)
    def replace_CONREF_at(self, index, value):
        self.CONREF[index] = value
    def hasContent_(self):
        if (
            self.CONREF
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
        for CONREF_ in self.CONREF:
            namespaceprefix_ = self.CONREF_nsprefix_ + ':' if (UseCapturedNS_ and self.CONREF_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONREF>%s</%sCONREF>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CONREF_), input_name='CONREF')), namespaceprefix_ , eol_))
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
            self.CONREF.append(value_)
            self.CONREF_nsprefix_ = child_.prefix
# end class CREATE


class RATE(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CONREF=None, CONNUMBER=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if CONREF is None:
            self.CONREF = []
        else:
            self.CONREF = CONREF
        self.CONREF_nsprefix_ = None
        if CONNUMBER is None:
            self.CONNUMBER = []
        else:
            self.CONNUMBER = CONNUMBER
        self.CONNUMBER_nsprefix_ = None
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
    def get_CONREF(self):
        return self.CONREF
    def set_CONREF(self, CONREF):
        self.CONREF = CONREF
    def add_CONREF(self, value):
        self.CONREF.append(value)
    def insert_CONREF_at(self, index, value):
        self.CONREF.insert(index, value)
    def replace_CONREF_at(self, index, value):
        self.CONREF[index] = value
    def get_CONNUMBER(self):
        return self.CONNUMBER
    def set_CONNUMBER(self, CONNUMBER):
        self.CONNUMBER = CONNUMBER
    def add_CONNUMBER(self, value):
        self.CONNUMBER.append(value)
    def insert_CONNUMBER_at(self, index, value):
        self.CONNUMBER.insert(index, value)
    def replace_CONNUMBER_at(self, index, value):
        self.CONNUMBER[index] = value
    def hasContent_(self):
        if (
            self.CONREF or
            self.CONNUMBER
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
        for CONREF_ in self.CONREF:
            namespaceprefix_ = self.CONREF_nsprefix_ + ':' if (UseCapturedNS_ and self.CONREF_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONREF>%s</%sCONREF>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CONREF_), input_name='CONREF')), namespaceprefix_ , eol_))
        for CONNUMBER_ in self.CONNUMBER:
            namespaceprefix_ = self.CONNUMBER_nsprefix_ + ':' if (UseCapturedNS_ and self.CONNUMBER_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONNUMBER>%s</%sCONNUMBER>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CONNUMBER_), input_name='CONNUMBER')), namespaceprefix_ , eol_))
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
            self.CONREF.append(value_)
            self.CONREF_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONNUMBER':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONNUMBER')
            value_ = self.gds_validate_string(value_, node, 'CONNUMBER')
            self.CONNUMBER.append(value_)
            self.CONNUMBER_nsprefix_ = child_.prefix
# end class RATE


class BOOK(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, EMAILREQD=None, ShowBookingRef=None, FaxNumber=None, LanguageId=None, PrintAtDepot=None, GROUPCODE=None, CONREF=None, CONNUMBER=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.EMAILREQD = _cast(None, EMAILREQD)
        self.EMAILREQD_nsprefix_ = None
        self.ShowBookingRef = _cast(None, ShowBookingRef)
        self.ShowBookingRef_nsprefix_ = None
        self.FaxNumber = _cast(None, FaxNumber)
        self.FaxNumber_nsprefix_ = None
        self.LanguageId = _cast(None, LanguageId)
        self.LanguageId_nsprefix_ = None
        self.PrintAtDepot = _cast(None, PrintAtDepot)
        self.PrintAtDepot_nsprefix_ = None
        self.GROUPCODE = GROUPCODE
        self.GROUPCODE_nsprefix_ = None
        if CONREF is None:
            self.CONREF = []
        else:
            self.CONREF = CONREF
        self.CONREF_nsprefix_ = None
        if CONNUMBER is None:
            self.CONNUMBER = []
        else:
            self.CONNUMBER = CONNUMBER
        self.CONNUMBER_nsprefix_ = None
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
    def get_GROUPCODE(self):
        return self.GROUPCODE
    def set_GROUPCODE(self, GROUPCODE):
        self.GROUPCODE = GROUPCODE
    def get_CONREF(self):
        return self.CONREF
    def set_CONREF(self, CONREF):
        self.CONREF = CONREF
    def add_CONREF(self, value):
        self.CONREF.append(value)
    def insert_CONREF_at(self, index, value):
        self.CONREF.insert(index, value)
    def replace_CONREF_at(self, index, value):
        self.CONREF[index] = value
    def get_CONNUMBER(self):
        return self.CONNUMBER
    def set_CONNUMBER(self, CONNUMBER):
        self.CONNUMBER = CONNUMBER
    def add_CONNUMBER(self, value):
        self.CONNUMBER.append(value)
    def insert_CONNUMBER_at(self, index, value):
        self.CONNUMBER.insert(index, value)
    def replace_CONNUMBER_at(self, index, value):
        self.CONNUMBER[index] = value
    def get_EMAILREQD(self):
        return self.EMAILREQD
    def set_EMAILREQD(self, EMAILREQD):
        self.EMAILREQD = EMAILREQD
    def get_ShowBookingRef(self):
        return self.ShowBookingRef
    def set_ShowBookingRef(self, ShowBookingRef):
        self.ShowBookingRef = ShowBookingRef
    def get_FaxNumber(self):
        return self.FaxNumber
    def set_FaxNumber(self, FaxNumber):
        self.FaxNumber = FaxNumber
    def get_LanguageId(self):
        return self.LanguageId
    def set_LanguageId(self, LanguageId):
        self.LanguageId = LanguageId
    def get_PrintAtDepot(self):
        return self.PrintAtDepot
    def set_PrintAtDepot(self, PrintAtDepot):
        self.PrintAtDepot = PrintAtDepot
    def hasContent_(self):
        if (
            self.GROUPCODE is not None or
            self.CONREF or
            self.CONNUMBER
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
        if self.EMAILREQD is not None and 'EMAILREQD' not in already_processed:
            already_processed.add('EMAILREQD')
            outfile.write(' EMAILREQD=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.EMAILREQD), input_name='EMAILREQD')), ))
        if self.ShowBookingRef is not None and 'ShowBookingRef' not in already_processed:
            already_processed.add('ShowBookingRef')
            outfile.write(' ShowBookingRef=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.ShowBookingRef), input_name='ShowBookingRef')), ))
        if self.FaxNumber is not None and 'FaxNumber' not in already_processed:
            already_processed.add('FaxNumber')
            outfile.write(' FaxNumber=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.FaxNumber), input_name='FaxNumber')), ))
        if self.LanguageId is not None and 'LanguageId' not in already_processed:
            already_processed.add('LanguageId')
            outfile.write(' LanguageId=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.LanguageId), input_name='LanguageId')), ))
        if self.PrintAtDepot is not None and 'PrintAtDepot' not in already_processed:
            already_processed.add('PrintAtDepot')
            outfile.write(' PrintAtDepot=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.PrintAtDepot), input_name='PrintAtDepot')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BOOK', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GROUPCODE is not None:
            namespaceprefix_ = self.GROUPCODE_nsprefix_ + ':' if (UseCapturedNS_ and self.GROUPCODE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGROUPCODE>%s</%sGROUPCODE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GROUPCODE), input_name='GROUPCODE')), namespaceprefix_ , eol_))
        for CONREF_ in self.CONREF:
            namespaceprefix_ = self.CONREF_nsprefix_ + ':' if (UseCapturedNS_ and self.CONREF_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONREF>%s</%sCONREF>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CONREF_), input_name='CONREF')), namespaceprefix_ , eol_))
        for CONNUMBER_ in self.CONNUMBER:
            namespaceprefix_ = self.CONNUMBER_nsprefix_ + ':' if (UseCapturedNS_ and self.CONNUMBER_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONNUMBER>%s</%sCONNUMBER>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CONNUMBER_), input_name='CONNUMBER')), namespaceprefix_ , eol_))
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
        value = find_attr_value_('EMAILREQD', node)
        if value is not None and 'EMAILREQD' not in already_processed:
            already_processed.add('EMAILREQD')
            self.EMAILREQD = value
        value = find_attr_value_('ShowBookingRef', node)
        if value is not None and 'ShowBookingRef' not in already_processed:
            already_processed.add('ShowBookingRef')
            self.ShowBookingRef = value
        value = find_attr_value_('FaxNumber', node)
        if value is not None and 'FaxNumber' not in already_processed:
            already_processed.add('FaxNumber')
            self.FaxNumber = value
        value = find_attr_value_('LanguageId', node)
        if value is not None and 'LanguageId' not in already_processed:
            already_processed.add('LanguageId')
            self.LanguageId = value
        value = find_attr_value_('PrintAtDepot', node)
        if value is not None and 'PrintAtDepot' not in already_processed:
            already_processed.add('PrintAtDepot')
            self.PrintAtDepot = value
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'GROUPCODE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GROUPCODE')
            value_ = self.gds_validate_string(value_, node, 'GROUPCODE')
            self.GROUPCODE = value_
            self.GROUPCODE_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONREF':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONREF')
            value_ = self.gds_validate_string(value_, node, 'CONREF')
            self.CONREF.append(value_)
            self.CONREF_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONNUMBER':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONNUMBER')
            value_ = self.gds_validate_string(value_, node, 'CONNUMBER')
            self.CONNUMBER.append(value_)
            self.CONNUMBER_nsprefix_ = child_.prefix
# end class BOOK


class SHIP(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GROUPCODE=None, CONREF=None, CONNUMBER=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GROUPCODE = GROUPCODE
        self.GROUPCODE_nsprefix_ = None
        if CONREF is None:
            self.CONREF = []
        else:
            self.CONREF = CONREF
        self.CONREF_nsprefix_ = None
        if CONNUMBER is None:
            self.CONNUMBER = []
        else:
            self.CONNUMBER = CONNUMBER
        self.CONNUMBER_nsprefix_ = None
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
    def get_GROUPCODE(self):
        return self.GROUPCODE
    def set_GROUPCODE(self, GROUPCODE):
        self.GROUPCODE = GROUPCODE
    def get_CONREF(self):
        return self.CONREF
    def set_CONREF(self, CONREF):
        self.CONREF = CONREF
    def add_CONREF(self, value):
        self.CONREF.append(value)
    def insert_CONREF_at(self, index, value):
        self.CONREF.insert(index, value)
    def replace_CONREF_at(self, index, value):
        self.CONREF[index] = value
    def get_CONNUMBER(self):
        return self.CONNUMBER
    def set_CONNUMBER(self, CONNUMBER):
        self.CONNUMBER = CONNUMBER
    def add_CONNUMBER(self, value):
        self.CONNUMBER.append(value)
    def insert_CONNUMBER_at(self, index, value):
        self.CONNUMBER.insert(index, value)
    def replace_CONNUMBER_at(self, index, value):
        self.CONNUMBER[index] = value
    def hasContent_(self):
        if (
            self.GROUPCODE is not None or
            self.CONREF or
            self.CONNUMBER
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
        if self.GROUPCODE is not None:
            namespaceprefix_ = self.GROUPCODE_nsprefix_ + ':' if (UseCapturedNS_ and self.GROUPCODE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGROUPCODE>%s</%sGROUPCODE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GROUPCODE), input_name='GROUPCODE')), namespaceprefix_ , eol_))
        for CONREF_ in self.CONREF:
            namespaceprefix_ = self.CONREF_nsprefix_ + ':' if (UseCapturedNS_ and self.CONREF_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONREF>%s</%sCONREF>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CONREF_), input_name='CONREF')), namespaceprefix_ , eol_))
        for CONNUMBER_ in self.CONNUMBER:
            namespaceprefix_ = self.CONNUMBER_nsprefix_ + ':' if (UseCapturedNS_ and self.CONNUMBER_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONNUMBER>%s</%sCONNUMBER>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CONNUMBER_), input_name='CONNUMBER')), namespaceprefix_ , eol_))
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
        elif nodeName_ == 'CONREF':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONREF')
            value_ = self.gds_validate_string(value_, node, 'CONREF')
            self.CONREF.append(value_)
            self.CONREF_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONNUMBER':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONNUMBER')
            value_ = self.gds_validate_string(value_, node, 'CONNUMBER')
            self.CONNUMBER.append(value_)
            self.CONNUMBER_nsprefix_ = child_.prefix
# end class SHIP


class PRINT(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, REQUIRED=None, CONNOTE=None, LABEL=None, MANIFEST=None, INVOICE=None, EMAILTO=None, EMAILFROM=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.REQUIRED = REQUIRED
        self.REQUIRED_nsprefix_ = None
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
    def get_REQUIRED(self):
        return self.REQUIRED
    def set_REQUIRED(self, REQUIRED):
        self.REQUIRED = REQUIRED
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
            self.REQUIRED is not None or
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
        if self.REQUIRED is not None:
            namespaceprefix_ = self.REQUIRED_nsprefix_ + ':' if (UseCapturedNS_ and self.REQUIRED_nsprefix_) else ''
            self.REQUIRED.export(outfile, level, namespaceprefix_, namespacedef_='', name_='REQUIRED', pretty_print=pretty_print)
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
            self.EMAILTO.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EMAILTO', pretty_print=pretty_print)
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
        if nodeName_ == 'REQUIRED':
            obj_ = REQUIRED.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.REQUIRED = obj_
            obj_.original_tagname_ = 'REQUIRED'
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
            obj_ = EMAILTO.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EMAILTO = obj_
            obj_.original_tagname_ = 'EMAILTO'
        elif nodeName_ == 'EMAILFROM':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EMAILFROM')
            value_ = self.gds_validate_string(value_, node, 'EMAILFROM')
            self.EMAILFROM = value_
            self.EMAILFROM_nsprefix_ = child_.prefix
# end class PRINT


class SHOW_GROUPCODE(GeneratedsSuper):
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
                CurrentSubclassModule_, SHOW_GROUPCODE)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SHOW_GROUPCODE.subclass:
            return SHOW_GROUPCODE.subclass(*args_, **kwargs_)
        else:
            return SHOW_GROUPCODE(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SHOW_GROUPCODE', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SHOW_GROUPCODE')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SHOW_GROUPCODE':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SHOW_GROUPCODE')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SHOW_GROUPCODE', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SHOW_GROUPCODE'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SHOW_GROUPCODE', fromsubclass_=False, pretty_print=True):
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
# end class SHOW_GROUPCODE


class REQUIRED(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CONREF=None, CONNUMBER=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if CONREF is None:
            self.CONREF = []
        else:
            self.CONREF = CONREF
        self.CONREF_nsprefix_ = None
        if CONNUMBER is None:
            self.CONNUMBER = []
        else:
            self.CONNUMBER = CONNUMBER
        self.CONNUMBER_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, REQUIRED)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if REQUIRED.subclass:
            return REQUIRED.subclass(*args_, **kwargs_)
        else:
            return REQUIRED(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CONREF(self):
        return self.CONREF
    def set_CONREF(self, CONREF):
        self.CONREF = CONREF
    def add_CONREF(self, value):
        self.CONREF.append(value)
    def insert_CONREF_at(self, index, value):
        self.CONREF.insert(index, value)
    def replace_CONREF_at(self, index, value):
        self.CONREF[index] = value
    def get_CONNUMBER(self):
        return self.CONNUMBER
    def set_CONNUMBER(self, CONNUMBER):
        self.CONNUMBER = CONNUMBER
    def add_CONNUMBER(self, value):
        self.CONNUMBER.append(value)
    def insert_CONNUMBER_at(self, index, value):
        self.CONNUMBER.insert(index, value)
    def replace_CONNUMBER_at(self, index, value):
        self.CONNUMBER[index] = value
    def hasContent_(self):
        if (
            self.CONREF or
            self.CONNUMBER
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='REQUIRED', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('REQUIRED')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'REQUIRED':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='REQUIRED')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='REQUIRED', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='REQUIRED'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='REQUIRED', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for CONREF_ in self.CONREF:
            namespaceprefix_ = self.CONREF_nsprefix_ + ':' if (UseCapturedNS_ and self.CONREF_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONREF>%s</%sCONREF>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CONREF_), input_name='CONREF')), namespaceprefix_ , eol_))
        for CONNUMBER_ in self.CONNUMBER:
            namespaceprefix_ = self.CONNUMBER_nsprefix_ + ':' if (UseCapturedNS_ and self.CONNUMBER_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONNUMBER>%s</%sCONNUMBER>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CONNUMBER_), input_name='CONNUMBER')), namespaceprefix_ , eol_))
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
            self.CONREF.append(value_)
            self.CONREF_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONNUMBER':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONNUMBER')
            value_ = self.gds_validate_string(value_, node, 'CONNUMBER')
            self.CONNUMBER.append(value_)
            self.CONNUMBER_nsprefix_ = child_.prefix
# end class REQUIRED


class CONNOTE(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CONREF=None, CONNUMBER=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if CONREF is None:
            self.CONREF = []
        else:
            self.CONREF = CONREF
        self.CONREF_nsprefix_ = None
        if CONNUMBER is None:
            self.CONNUMBER = []
        else:
            self.CONNUMBER = CONNUMBER
        self.CONNUMBER_nsprefix_ = None
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
    def get_CONREF(self):
        return self.CONREF
    def set_CONREF(self, CONREF):
        self.CONREF = CONREF
    def add_CONREF(self, value):
        self.CONREF.append(value)
    def insert_CONREF_at(self, index, value):
        self.CONREF.insert(index, value)
    def replace_CONREF_at(self, index, value):
        self.CONREF[index] = value
    def get_CONNUMBER(self):
        return self.CONNUMBER
    def set_CONNUMBER(self, CONNUMBER):
        self.CONNUMBER = CONNUMBER
    def add_CONNUMBER(self, value):
        self.CONNUMBER.append(value)
    def insert_CONNUMBER_at(self, index, value):
        self.CONNUMBER.insert(index, value)
    def replace_CONNUMBER_at(self, index, value):
        self.CONNUMBER[index] = value
    def hasContent_(self):
        if (
            self.CONREF or
            self.CONNUMBER
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
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for CONREF_ in self.CONREF:
            namespaceprefix_ = self.CONREF_nsprefix_ + ':' if (UseCapturedNS_ and self.CONREF_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONREF>%s</%sCONREF>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CONREF_), input_name='CONREF')), namespaceprefix_ , eol_))
        for CONNUMBER_ in self.CONNUMBER:
            namespaceprefix_ = self.CONNUMBER_nsprefix_ + ':' if (UseCapturedNS_ and self.CONNUMBER_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONNUMBER>%s</%sCONNUMBER>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CONNUMBER_), input_name='CONNUMBER')), namespaceprefix_ , eol_))
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
            self.CONREF.append(value_)
            self.CONREF_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONNUMBER':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONNUMBER')
            value_ = self.gds_validate_string(value_, node, 'CONNUMBER')
            self.CONNUMBER.append(value_)
            self.CONNUMBER_nsprefix_ = child_.prefix
# end class CONNOTE


class LABEL(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CONREF=None, CONNUMBER=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if CONREF is None:
            self.CONREF = []
        else:
            self.CONREF = CONREF
        self.CONREF_nsprefix_ = None
        if CONNUMBER is None:
            self.CONNUMBER = []
        else:
            self.CONNUMBER = CONNUMBER
        self.CONNUMBER_nsprefix_ = None
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
    def get_CONREF(self):
        return self.CONREF
    def set_CONREF(self, CONREF):
        self.CONREF = CONREF
    def add_CONREF(self, value):
        self.CONREF.append(value)
    def insert_CONREF_at(self, index, value):
        self.CONREF.insert(index, value)
    def replace_CONREF_at(self, index, value):
        self.CONREF[index] = value
    def get_CONNUMBER(self):
        return self.CONNUMBER
    def set_CONNUMBER(self, CONNUMBER):
        self.CONNUMBER = CONNUMBER
    def add_CONNUMBER(self, value):
        self.CONNUMBER.append(value)
    def insert_CONNUMBER_at(self, index, value):
        self.CONNUMBER.insert(index, value)
    def replace_CONNUMBER_at(self, index, value):
        self.CONNUMBER[index] = value
    def hasContent_(self):
        if (
            self.CONREF or
            self.CONNUMBER
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
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for CONREF_ in self.CONREF:
            namespaceprefix_ = self.CONREF_nsprefix_ + ':' if (UseCapturedNS_ and self.CONREF_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONREF>%s</%sCONREF>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CONREF_), input_name='CONREF')), namespaceprefix_ , eol_))
        for CONNUMBER_ in self.CONNUMBER:
            namespaceprefix_ = self.CONNUMBER_nsprefix_ + ':' if (UseCapturedNS_ and self.CONNUMBER_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONNUMBER>%s</%sCONNUMBER>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CONNUMBER_), input_name='CONNUMBER')), namespaceprefix_ , eol_))
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
            self.CONREF.append(value_)
            self.CONREF_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONNUMBER':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONNUMBER')
            value_ = self.gds_validate_string(value_, node, 'CONNUMBER')
            self.CONNUMBER.append(value_)
            self.CONNUMBER_nsprefix_ = child_.prefix
# end class LABEL


class MANIFEST(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GROUPCODE=None, CONREF=None, CONNUMBER=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GROUPCODE = GROUPCODE
        self.GROUPCODE_nsprefix_ = None
        if CONREF is None:
            self.CONREF = []
        else:
            self.CONREF = CONREF
        self.CONREF_nsprefix_ = None
        if CONNUMBER is None:
            self.CONNUMBER = []
        else:
            self.CONNUMBER = CONNUMBER
        self.CONNUMBER_nsprefix_ = None
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
    def get_GROUPCODE(self):
        return self.GROUPCODE
    def set_GROUPCODE(self, GROUPCODE):
        self.GROUPCODE = GROUPCODE
    def get_CONREF(self):
        return self.CONREF
    def set_CONREF(self, CONREF):
        self.CONREF = CONREF
    def add_CONREF(self, value):
        self.CONREF.append(value)
    def insert_CONREF_at(self, index, value):
        self.CONREF.insert(index, value)
    def replace_CONREF_at(self, index, value):
        self.CONREF[index] = value
    def get_CONNUMBER(self):
        return self.CONNUMBER
    def set_CONNUMBER(self, CONNUMBER):
        self.CONNUMBER = CONNUMBER
    def add_CONNUMBER(self, value):
        self.CONNUMBER.append(value)
    def insert_CONNUMBER_at(self, index, value):
        self.CONNUMBER.insert(index, value)
    def replace_CONNUMBER_at(self, index, value):
        self.CONNUMBER[index] = value
    def hasContent_(self):
        if (
            self.GROUPCODE is not None or
            self.CONREF or
            self.CONNUMBER
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
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GROUPCODE is not None:
            namespaceprefix_ = self.GROUPCODE_nsprefix_ + ':' if (UseCapturedNS_ and self.GROUPCODE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGROUPCODE>%s</%sGROUPCODE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GROUPCODE), input_name='GROUPCODE')), namespaceprefix_ , eol_))
        for CONREF_ in self.CONREF:
            namespaceprefix_ = self.CONREF_nsprefix_ + ':' if (UseCapturedNS_ and self.CONREF_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONREF>%s</%sCONREF>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CONREF_), input_name='CONREF')), namespaceprefix_ , eol_))
        for CONNUMBER_ in self.CONNUMBER:
            namespaceprefix_ = self.CONNUMBER_nsprefix_ + ':' if (UseCapturedNS_ and self.CONNUMBER_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONNUMBER>%s</%sCONNUMBER>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CONNUMBER_), input_name='CONNUMBER')), namespaceprefix_ , eol_))
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
        elif nodeName_ == 'CONREF':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONREF')
            value_ = self.gds_validate_string(value_, node, 'CONREF')
            self.CONREF.append(value_)
            self.CONREF_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONNUMBER':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONNUMBER')
            value_ = self.gds_validate_string(value_, node, 'CONNUMBER')
            self.CONNUMBER.append(value_)
            self.CONNUMBER_nsprefix_ = child_.prefix
# end class MANIFEST


class INVOICE(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CONREF=None, CONNUMBER=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if CONREF is None:
            self.CONREF = []
        else:
            self.CONREF = CONREF
        self.CONREF_nsprefix_ = None
        if CONNUMBER is None:
            self.CONNUMBER = []
        else:
            self.CONNUMBER = CONNUMBER
        self.CONNUMBER_nsprefix_ = None
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
    def get_CONREF(self):
        return self.CONREF
    def set_CONREF(self, CONREF):
        self.CONREF = CONREF
    def add_CONREF(self, value):
        self.CONREF.append(value)
    def insert_CONREF_at(self, index, value):
        self.CONREF.insert(index, value)
    def replace_CONREF_at(self, index, value):
        self.CONREF[index] = value
    def get_CONNUMBER(self):
        return self.CONNUMBER
    def set_CONNUMBER(self, CONNUMBER):
        self.CONNUMBER = CONNUMBER
    def add_CONNUMBER(self, value):
        self.CONNUMBER.append(value)
    def insert_CONNUMBER_at(self, index, value):
        self.CONNUMBER.insert(index, value)
    def replace_CONNUMBER_at(self, index, value):
        self.CONNUMBER[index] = value
    def hasContent_(self):
        if (
            self.CONREF or
            self.CONNUMBER
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
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for CONREF_ in self.CONREF:
            namespaceprefix_ = self.CONREF_nsprefix_ + ':' if (UseCapturedNS_ and self.CONREF_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONREF>%s</%sCONREF>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CONREF_), input_name='CONREF')), namespaceprefix_ , eol_))
        for CONNUMBER_ in self.CONNUMBER:
            namespaceprefix_ = self.CONNUMBER_nsprefix_ + ':' if (UseCapturedNS_ and self.CONNUMBER_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCONNUMBER>%s</%sCONNUMBER>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(CONNUMBER_), input_name='CONNUMBER')), namespaceprefix_ , eol_))
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
            self.CONREF.append(value_)
            self.CONREF_nsprefix_ = child_.prefix
        elif nodeName_ == 'CONNUMBER':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CONNUMBER')
            value_ = self.gds_validate_string(value_, node, 'CONNUMBER')
            self.CONNUMBER.append(value_)
            self.CONNUMBER_nsprefix_ = child_.prefix
# end class INVOICE


class EMAILTO(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, type_=None, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.type_ = _cast(None, type_)
        self.type__nsprefix_ = None
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EMAILTO)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EMAILTO.subclass:
            return EMAILTO.subclass(*args_, **kwargs_)
        else:
            return EMAILTO(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_type(self):
        return self.type_
    def set_type(self, type_):
        self.type_ = type_
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def hasContent_(self):
        if (
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_)
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EMAILTO', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EMAILTO')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EMAILTO':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EMAILTO')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='EMAILTO', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EMAILTO'):
        if self.type_ is not None and 'type_' not in already_processed:
            already_processed.add('type_')
            outfile.write(' type=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.type_), input_name='type')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EMAILTO', fromsubclass_=False, pretty_print=True):
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
        value = find_attr_value_('type', node)
        if value is not None and 'type' not in already_processed:
            already_processed.add('type')
            self.type_ = value
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class EMAILTO


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
        rootTag = 'ESHIPPER'
        rootClass = ESHIPPER
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
        rootTag = 'ESHIPPER'
        rootClass = ESHIPPER
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
        rootTag = 'ESHIPPER'
        rootClass = ESHIPPER
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
        rootTag = 'ESHIPPER'
        rootClass = ESHIPPER
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from shipment_request import *\n\n')
        sys.stdout.write('import shipment_request as model_\n\n')
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
    "ACTIVITY",
    "ALTCOLLECTTIME",
    "ARTICLE",
    "BOOK",
    "COLLECTION",
    "COLLECTIONADDRESS",
    "CONNOTE",
    "CONSIGNMENT",
    "CONSIGNMENTBATCH",
    "CREATE",
    "DELIVERY",
    "DETAILS",
    "EMAILTO",
    "ESHIPPER",
    "INVOICE",
    "LABEL",
    "LOGIN",
    "MANIFEST",
    "PACKAGE",
    "PREFCOLLECTTIME",
    "PRINT",
    "RATE",
    "RECEIVER",
    "REQUIRED",
    "SENDER",
    "SHIP",
    "SHOW_GROUPCODE"
]
