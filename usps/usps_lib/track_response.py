#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Wed Feb 17 05:44:56 2021 by generateDS.py version 2.37.15.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', 'usps_lib/track_response.py')
#
# Command line arguments:
#   schemas/TrackResponse.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "usps_lib/track_response.py" schemas/TrackResponse.xsd
#
# Current working directory (os.getcwd()):
#   usps
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


class TrackResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TrackInfo=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if TrackInfo is None:
            self.TrackInfo = []
        else:
            self.TrackInfo = TrackInfo
        self.TrackInfo_nsprefix_ = None
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
    def get_TrackInfo(self):
        return self.TrackInfo
    def set_TrackInfo(self, TrackInfo):
        self.TrackInfo = TrackInfo
    def add_TrackInfo(self, value):
        self.TrackInfo.append(value)
    def insert_TrackInfo_at(self, index, value):
        self.TrackInfo.insert(index, value)
    def replace_TrackInfo_at(self, index, value):
        self.TrackInfo[index] = value
    def hasContent_(self):
        if (
            self.TrackInfo
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
        for TrackInfo_ in self.TrackInfo:
            namespaceprefix_ = self.TrackInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackInfo_nsprefix_) else ''
            TrackInfo_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TrackInfo', pretty_print=pretty_print)
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
        if nodeName_ == 'TrackInfo':
            obj_ = TrackInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TrackInfo.append(obj_)
            obj_.original_tagname_ = 'TrackInfo'
# end class TrackResponse


class TrackInfoType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ID=None, AdditionalInfo=None, ADPScripting=None, ARCHDATA=None, ArchiveRestoreInfo=None, AssociatedLabel=None, Class=None, ClassOfMailCode=None, DeliveryNotificationDate=None, DestinationCity=None, DestinationCountryCode=None, DestinationState=None, DestinationZip=None, EditedLabelID=None, EmailEnabled=None, ExpectedDeliveryDate=None, ExpectedDeliveryTime=None, GuaranteedDeliveryDate=None, GuaranteedDeliveryTime=None, GuaranteedDetails=None, KahalaIndicator=None, MailTypeCode=None, MPDATE=None, MPSUFFIX=None, OriginCity=None, OriginCountryCode=None, OriginState=None, OriginZip=None, PodEnabled=None, PredictedDeliveryDate=None, PredictedDeliveryTime=None, PDWStart=None, PDWEnd=None, RelatedRRID=None, RestoreEnabled=None, RRAMenabled=None, RreEnabled=None, Service=None, ServiceTypeCode=None, Status=None, StatusCategory=None, StatusSummary=None, TABLECODE=None, TpodEnabled=None, ValueofArticle=None, EnabledNotificationRequests=None, TrackSummary=None, TrackDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ID = _cast(None, ID)
        self.ID_nsprefix_ = None
        self.AdditionalInfo = AdditionalInfo
        self.AdditionalInfo_nsprefix_ = None
        self.ADPScripting = ADPScripting
        self.ADPScripting_nsprefix_ = None
        self.ARCHDATA = ARCHDATA
        self.ARCHDATA_nsprefix_ = None
        self.ArchiveRestoreInfo = ArchiveRestoreInfo
        self.ArchiveRestoreInfo_nsprefix_ = None
        self.AssociatedLabel = AssociatedLabel
        self.AssociatedLabel_nsprefix_ = None
        self.Class = Class
        self.Class_nsprefix_ = None
        self.ClassOfMailCode = ClassOfMailCode
        self.ClassOfMailCode_nsprefix_ = None
        self.DeliveryNotificationDate = DeliveryNotificationDate
        self.DeliveryNotificationDate_nsprefix_ = None
        self.DestinationCity = DestinationCity
        self.DestinationCity_nsprefix_ = None
        self.DestinationCountryCode = DestinationCountryCode
        self.DestinationCountryCode_nsprefix_ = None
        self.DestinationState = DestinationState
        self.DestinationState_nsprefix_ = None
        self.DestinationZip = DestinationZip
        self.DestinationZip_nsprefix_ = None
        self.EditedLabelID = EditedLabelID
        self.EditedLabelID_nsprefix_ = None
        self.EmailEnabled = EmailEnabled
        self.EmailEnabled_nsprefix_ = None
        self.ExpectedDeliveryDate = ExpectedDeliveryDate
        self.ExpectedDeliveryDate_nsprefix_ = None
        self.ExpectedDeliveryTime = ExpectedDeliveryTime
        self.ExpectedDeliveryTime_nsprefix_ = None
        self.GuaranteedDeliveryDate = GuaranteedDeliveryDate
        self.GuaranteedDeliveryDate_nsprefix_ = None
        self.GuaranteedDeliveryTime = GuaranteedDeliveryTime
        self.GuaranteedDeliveryTime_nsprefix_ = None
        self.GuaranteedDetails = GuaranteedDetails
        self.GuaranteedDetails_nsprefix_ = None
        self.KahalaIndicator = KahalaIndicator
        self.KahalaIndicator_nsprefix_ = None
        self.MailTypeCode = MailTypeCode
        self.MailTypeCode_nsprefix_ = None
        self.MPDATE = MPDATE
        self.MPDATE_nsprefix_ = None
        self.MPSUFFIX = MPSUFFIX
        self.MPSUFFIX_nsprefix_ = None
        self.OriginCity = OriginCity
        self.OriginCity_nsprefix_ = None
        self.OriginCountryCode = OriginCountryCode
        self.OriginCountryCode_nsprefix_ = None
        self.OriginState = OriginState
        self.OriginState_nsprefix_ = None
        self.OriginZip = OriginZip
        self.OriginZip_nsprefix_ = None
        self.PodEnabled = PodEnabled
        self.PodEnabled_nsprefix_ = None
        self.PredictedDeliveryDate = PredictedDeliveryDate
        self.PredictedDeliveryDate_nsprefix_ = None
        self.PredictedDeliveryTime = PredictedDeliveryTime
        self.PredictedDeliveryTime_nsprefix_ = None
        self.PDWStart = PDWStart
        self.PDWStart_nsprefix_ = None
        self.PDWEnd = PDWEnd
        self.PDWEnd_nsprefix_ = None
        self.RelatedRRID = RelatedRRID
        self.RelatedRRID_nsprefix_ = None
        self.RestoreEnabled = RestoreEnabled
        self.RestoreEnabled_nsprefix_ = None
        self.RRAMenabled = RRAMenabled
        self.RRAMenabled_nsprefix_ = None
        self.RreEnabled = RreEnabled
        self.RreEnabled_nsprefix_ = None
        self.Service = Service
        self.Service_nsprefix_ = None
        self.ServiceTypeCode = ServiceTypeCode
        self.ServiceTypeCode_nsprefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
        self.StatusCategory = StatusCategory
        self.StatusCategory_nsprefix_ = None
        self.StatusSummary = StatusSummary
        self.StatusSummary_nsprefix_ = None
        self.TABLECODE = TABLECODE
        self.TABLECODE_nsprefix_ = None
        self.TpodEnabled = TpodEnabled
        self.TpodEnabled_nsprefix_ = None
        self.ValueofArticle = ValueofArticle
        self.ValueofArticle_nsprefix_ = None
        self.EnabledNotificationRequests = EnabledNotificationRequests
        self.EnabledNotificationRequests_nsprefix_ = None
        self.TrackSummary = TrackSummary
        self.TrackSummary_nsprefix_ = None
        if TrackDetail is None:
            self.TrackDetail = []
        else:
            self.TrackDetail = TrackDetail
        self.TrackDetail_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TrackInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TrackInfoType.subclass:
            return TrackInfoType.subclass(*args_, **kwargs_)
        else:
            return TrackInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AdditionalInfo(self):
        return self.AdditionalInfo
    def set_AdditionalInfo(self, AdditionalInfo):
        self.AdditionalInfo = AdditionalInfo
    def get_ADPScripting(self):
        return self.ADPScripting
    def set_ADPScripting(self, ADPScripting):
        self.ADPScripting = ADPScripting
    def get_ARCHDATA(self):
        return self.ARCHDATA
    def set_ARCHDATA(self, ARCHDATA):
        self.ARCHDATA = ARCHDATA
    def get_ArchiveRestoreInfo(self):
        return self.ArchiveRestoreInfo
    def set_ArchiveRestoreInfo(self, ArchiveRestoreInfo):
        self.ArchiveRestoreInfo = ArchiveRestoreInfo
    def get_AssociatedLabel(self):
        return self.AssociatedLabel
    def set_AssociatedLabel(self, AssociatedLabel):
        self.AssociatedLabel = AssociatedLabel
    def get_Class(self):
        return self.Class
    def set_Class(self, Class):
        self.Class = Class
    def get_ClassOfMailCode(self):
        return self.ClassOfMailCode
    def set_ClassOfMailCode(self, ClassOfMailCode):
        self.ClassOfMailCode = ClassOfMailCode
    def get_DeliveryNotificationDate(self):
        return self.DeliveryNotificationDate
    def set_DeliveryNotificationDate(self, DeliveryNotificationDate):
        self.DeliveryNotificationDate = DeliveryNotificationDate
    def get_DestinationCity(self):
        return self.DestinationCity
    def set_DestinationCity(self, DestinationCity):
        self.DestinationCity = DestinationCity
    def get_DestinationCountryCode(self):
        return self.DestinationCountryCode
    def set_DestinationCountryCode(self, DestinationCountryCode):
        self.DestinationCountryCode = DestinationCountryCode
    def get_DestinationState(self):
        return self.DestinationState
    def set_DestinationState(self, DestinationState):
        self.DestinationState = DestinationState
    def get_DestinationZip(self):
        return self.DestinationZip
    def set_DestinationZip(self, DestinationZip):
        self.DestinationZip = DestinationZip
    def get_EditedLabelID(self):
        return self.EditedLabelID
    def set_EditedLabelID(self, EditedLabelID):
        self.EditedLabelID = EditedLabelID
    def get_EmailEnabled(self):
        return self.EmailEnabled
    def set_EmailEnabled(self, EmailEnabled):
        self.EmailEnabled = EmailEnabled
    def get_ExpectedDeliveryDate(self):
        return self.ExpectedDeliveryDate
    def set_ExpectedDeliveryDate(self, ExpectedDeliveryDate):
        self.ExpectedDeliveryDate = ExpectedDeliveryDate
    def get_ExpectedDeliveryTime(self):
        return self.ExpectedDeliveryTime
    def set_ExpectedDeliveryTime(self, ExpectedDeliveryTime):
        self.ExpectedDeliveryTime = ExpectedDeliveryTime
    def get_GuaranteedDeliveryDate(self):
        return self.GuaranteedDeliveryDate
    def set_GuaranteedDeliveryDate(self, GuaranteedDeliveryDate):
        self.GuaranteedDeliveryDate = GuaranteedDeliveryDate
    def get_GuaranteedDeliveryTime(self):
        return self.GuaranteedDeliveryTime
    def set_GuaranteedDeliveryTime(self, GuaranteedDeliveryTime):
        self.GuaranteedDeliveryTime = GuaranteedDeliveryTime
    def get_GuaranteedDetails(self):
        return self.GuaranteedDetails
    def set_GuaranteedDetails(self, GuaranteedDetails):
        self.GuaranteedDetails = GuaranteedDetails
    def get_KahalaIndicator(self):
        return self.KahalaIndicator
    def set_KahalaIndicator(self, KahalaIndicator):
        self.KahalaIndicator = KahalaIndicator
    def get_MailTypeCode(self):
        return self.MailTypeCode
    def set_MailTypeCode(self, MailTypeCode):
        self.MailTypeCode = MailTypeCode
    def get_MPDATE(self):
        return self.MPDATE
    def set_MPDATE(self, MPDATE):
        self.MPDATE = MPDATE
    def get_MPSUFFIX(self):
        return self.MPSUFFIX
    def set_MPSUFFIX(self, MPSUFFIX):
        self.MPSUFFIX = MPSUFFIX
    def get_OriginCity(self):
        return self.OriginCity
    def set_OriginCity(self, OriginCity):
        self.OriginCity = OriginCity
    def get_OriginCountryCode(self):
        return self.OriginCountryCode
    def set_OriginCountryCode(self, OriginCountryCode):
        self.OriginCountryCode = OriginCountryCode
    def get_OriginState(self):
        return self.OriginState
    def set_OriginState(self, OriginState):
        self.OriginState = OriginState
    def get_OriginZip(self):
        return self.OriginZip
    def set_OriginZip(self, OriginZip):
        self.OriginZip = OriginZip
    def get_PodEnabled(self):
        return self.PodEnabled
    def set_PodEnabled(self, PodEnabled):
        self.PodEnabled = PodEnabled
    def get_PredictedDeliveryDate(self):
        return self.PredictedDeliveryDate
    def set_PredictedDeliveryDate(self, PredictedDeliveryDate):
        self.PredictedDeliveryDate = PredictedDeliveryDate
    def get_PredictedDeliveryTime(self):
        return self.PredictedDeliveryTime
    def set_PredictedDeliveryTime(self, PredictedDeliveryTime):
        self.PredictedDeliveryTime = PredictedDeliveryTime
    def get_PDWStart(self):
        return self.PDWStart
    def set_PDWStart(self, PDWStart):
        self.PDWStart = PDWStart
    def get_PDWEnd(self):
        return self.PDWEnd
    def set_PDWEnd(self, PDWEnd):
        self.PDWEnd = PDWEnd
    def get_RelatedRRID(self):
        return self.RelatedRRID
    def set_RelatedRRID(self, RelatedRRID):
        self.RelatedRRID = RelatedRRID
    def get_RestoreEnabled(self):
        return self.RestoreEnabled
    def set_RestoreEnabled(self, RestoreEnabled):
        self.RestoreEnabled = RestoreEnabled
    def get_RRAMenabled(self):
        return self.RRAMenabled
    def set_RRAMenabled(self, RRAMenabled):
        self.RRAMenabled = RRAMenabled
    def get_RreEnabled(self):
        return self.RreEnabled
    def set_RreEnabled(self, RreEnabled):
        self.RreEnabled = RreEnabled
    def get_Service(self):
        return self.Service
    def set_Service(self, Service):
        self.Service = Service
    def get_ServiceTypeCode(self):
        return self.ServiceTypeCode
    def set_ServiceTypeCode(self, ServiceTypeCode):
        self.ServiceTypeCode = ServiceTypeCode
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def get_StatusCategory(self):
        return self.StatusCategory
    def set_StatusCategory(self, StatusCategory):
        self.StatusCategory = StatusCategory
    def get_StatusSummary(self):
        return self.StatusSummary
    def set_StatusSummary(self, StatusSummary):
        self.StatusSummary = StatusSummary
    def get_TABLECODE(self):
        return self.TABLECODE
    def set_TABLECODE(self, TABLECODE):
        self.TABLECODE = TABLECODE
    def get_TpodEnabled(self):
        return self.TpodEnabled
    def set_TpodEnabled(self, TpodEnabled):
        self.TpodEnabled = TpodEnabled
    def get_ValueofArticle(self):
        return self.ValueofArticle
    def set_ValueofArticle(self, ValueofArticle):
        self.ValueofArticle = ValueofArticle
    def get_EnabledNotificationRequests(self):
        return self.EnabledNotificationRequests
    def set_EnabledNotificationRequests(self, EnabledNotificationRequests):
        self.EnabledNotificationRequests = EnabledNotificationRequests
    def get_TrackSummary(self):
        return self.TrackSummary
    def set_TrackSummary(self, TrackSummary):
        self.TrackSummary = TrackSummary
    def get_TrackDetail(self):
        return self.TrackDetail
    def set_TrackDetail(self, TrackDetail):
        self.TrackDetail = TrackDetail
    def add_TrackDetail(self, value):
        self.TrackDetail.append(value)
    def insert_TrackDetail_at(self, index, value):
        self.TrackDetail.insert(index, value)
    def replace_TrackDetail_at(self, index, value):
        self.TrackDetail[index] = value
    def get_ID(self):
        return self.ID
    def set_ID(self, ID):
        self.ID = ID
    def hasContent_(self):
        if (
            self.AdditionalInfo is not None or
            self.ADPScripting is not None or
            self.ARCHDATA is not None or
            self.ArchiveRestoreInfo is not None or
            self.AssociatedLabel is not None or
            self.Class is not None or
            self.ClassOfMailCode is not None or
            self.DeliveryNotificationDate is not None or
            self.DestinationCity is not None or
            self.DestinationCountryCode is not None or
            self.DestinationState is not None or
            self.DestinationZip is not None or
            self.EditedLabelID is not None or
            self.EmailEnabled is not None or
            self.ExpectedDeliveryDate is not None or
            self.ExpectedDeliveryTime is not None or
            self.GuaranteedDeliveryDate is not None or
            self.GuaranteedDeliveryTime is not None or
            self.GuaranteedDetails is not None or
            self.KahalaIndicator is not None or
            self.MailTypeCode is not None or
            self.MPDATE is not None or
            self.MPSUFFIX is not None or
            self.OriginCity is not None or
            self.OriginCountryCode is not None or
            self.OriginState is not None or
            self.OriginZip is not None or
            self.PodEnabled is not None or
            self.PredictedDeliveryDate is not None or
            self.PredictedDeliveryTime is not None or
            self.PDWStart is not None or
            self.PDWEnd is not None or
            self.RelatedRRID is not None or
            self.RestoreEnabled is not None or
            self.RRAMenabled is not None or
            self.RreEnabled is not None or
            self.Service is not None or
            self.ServiceTypeCode is not None or
            self.Status is not None or
            self.StatusCategory is not None or
            self.StatusSummary is not None or
            self.TABLECODE is not None or
            self.TpodEnabled is not None or
            self.ValueofArticle is not None or
            self.EnabledNotificationRequests is not None or
            self.TrackSummary is not None or
            self.TrackDetail
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackInfoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TrackInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TrackInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TrackInfoType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TrackInfoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TrackInfoType'):
        if self.ID is not None and 'ID' not in already_processed:
            already_processed.add('ID')
            outfile.write(' ID=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.ID), input_name='ID')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackInfoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.AdditionalInfo is not None:
            namespaceprefix_ = self.AdditionalInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.AdditionalInfo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAdditionalInfo>%s</%sAdditionalInfo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AdditionalInfo), input_name='AdditionalInfo')), namespaceprefix_ , eol_))
        if self.ADPScripting is not None:
            namespaceprefix_ = self.ADPScripting_nsprefix_ + ':' if (UseCapturedNS_ and self.ADPScripting_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sADPScripting>%s</%sADPScripting>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ADPScripting), input_name='ADPScripting')), namespaceprefix_ , eol_))
        if self.ARCHDATA is not None:
            namespaceprefix_ = self.ARCHDATA_nsprefix_ + ':' if (UseCapturedNS_ and self.ARCHDATA_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sARCHDATA>%s</%sARCHDATA>%s' % (namespaceprefix_ , self.gds_format_boolean(self.ARCHDATA, input_name='ARCHDATA'), namespaceprefix_ , eol_))
        if self.ArchiveRestoreInfo is not None:
            namespaceprefix_ = self.ArchiveRestoreInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.ArchiveRestoreInfo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sArchiveRestoreInfo>%s</%sArchiveRestoreInfo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ArchiveRestoreInfo), input_name='ArchiveRestoreInfo')), namespaceprefix_ , eol_))
        if self.AssociatedLabel is not None:
            namespaceprefix_ = self.AssociatedLabel_nsprefix_ + ':' if (UseCapturedNS_ and self.AssociatedLabel_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAssociatedLabel>%s</%sAssociatedLabel>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AssociatedLabel), input_name='AssociatedLabel')), namespaceprefix_ , eol_))
        if self.Class is not None:
            namespaceprefix_ = self.Class_nsprefix_ + ':' if (UseCapturedNS_ and self.Class_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sClass>%s</%sClass>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Class), input_name='Class')), namespaceprefix_ , eol_))
        if self.ClassOfMailCode is not None:
            namespaceprefix_ = self.ClassOfMailCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ClassOfMailCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sClassOfMailCode>%s</%sClassOfMailCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ClassOfMailCode), input_name='ClassOfMailCode')), namespaceprefix_ , eol_))
        if self.DeliveryNotificationDate is not None:
            namespaceprefix_ = self.DeliveryNotificationDate_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryNotificationDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeliveryNotificationDate>%s</%sDeliveryNotificationDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DeliveryNotificationDate), input_name='DeliveryNotificationDate')), namespaceprefix_ , eol_))
        if self.DestinationCity is not None:
            namespaceprefix_ = self.DestinationCity_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationCity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDestinationCity>%s</%sDestinationCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DestinationCity), input_name='DestinationCity')), namespaceprefix_ , eol_))
        if self.DestinationCountryCode is not None:
            namespaceprefix_ = self.DestinationCountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationCountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDestinationCountryCode>%s</%sDestinationCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DestinationCountryCode), input_name='DestinationCountryCode')), namespaceprefix_ , eol_))
        if self.DestinationState is not None:
            namespaceprefix_ = self.DestinationState_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationState_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDestinationState>%s</%sDestinationState>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DestinationState), input_name='DestinationState')), namespaceprefix_ , eol_))
        if self.DestinationZip is not None:
            namespaceprefix_ = self.DestinationZip_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationZip_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDestinationZip>%s</%sDestinationZip>%s' % (namespaceprefix_ , self.gds_format_integer(self.DestinationZip, input_name='DestinationZip'), namespaceprefix_ , eol_))
        if self.EditedLabelID is not None:
            namespaceprefix_ = self.EditedLabelID_nsprefix_ + ':' if (UseCapturedNS_ and self.EditedLabelID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEditedLabelID>%s</%sEditedLabelID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EditedLabelID), input_name='EditedLabelID')), namespaceprefix_ , eol_))
        if self.EmailEnabled is not None:
            namespaceprefix_ = self.EmailEnabled_nsprefix_ + ':' if (UseCapturedNS_ and self.EmailEnabled_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEmailEnabled>%s</%sEmailEnabled>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EmailEnabled), input_name='EmailEnabled')), namespaceprefix_ , eol_))
        if self.ExpectedDeliveryDate is not None:
            namespaceprefix_ = self.ExpectedDeliveryDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ExpectedDeliveryDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExpectedDeliveryDate>%s</%sExpectedDeliveryDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ExpectedDeliveryDate), input_name='ExpectedDeliveryDate')), namespaceprefix_ , eol_))
        if self.ExpectedDeliveryTime is not None:
            namespaceprefix_ = self.ExpectedDeliveryTime_nsprefix_ + ':' if (UseCapturedNS_ and self.ExpectedDeliveryTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExpectedDeliveryTime>%s</%sExpectedDeliveryTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ExpectedDeliveryTime), input_name='ExpectedDeliveryTime')), namespaceprefix_ , eol_))
        if self.GuaranteedDeliveryDate is not None:
            namespaceprefix_ = self.GuaranteedDeliveryDate_nsprefix_ + ':' if (UseCapturedNS_ and self.GuaranteedDeliveryDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGuaranteedDeliveryDate>%s</%sGuaranteedDeliveryDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GuaranteedDeliveryDate), input_name='GuaranteedDeliveryDate')), namespaceprefix_ , eol_))
        if self.GuaranteedDeliveryTime is not None:
            namespaceprefix_ = self.GuaranteedDeliveryTime_nsprefix_ + ':' if (UseCapturedNS_ and self.GuaranteedDeliveryTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGuaranteedDeliveryTime>%s</%sGuaranteedDeliveryTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GuaranteedDeliveryTime), input_name='GuaranteedDeliveryTime')), namespaceprefix_ , eol_))
        if self.GuaranteedDetails is not None:
            namespaceprefix_ = self.GuaranteedDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.GuaranteedDetails_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGuaranteedDetails>%s</%sGuaranteedDetails>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GuaranteedDetails), input_name='GuaranteedDetails')), namespaceprefix_ , eol_))
        if self.KahalaIndicator is not None:
            namespaceprefix_ = self.KahalaIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.KahalaIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sKahalaIndicator>%s</%sKahalaIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.KahalaIndicator), input_name='KahalaIndicator')), namespaceprefix_ , eol_))
        if self.MailTypeCode is not None:
            namespaceprefix_ = self.MailTypeCode_nsprefix_ + ':' if (UseCapturedNS_ and self.MailTypeCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMailTypeCode>%s</%sMailTypeCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MailTypeCode), input_name='MailTypeCode')), namespaceprefix_ , eol_))
        if self.MPDATE is not None:
            namespaceprefix_ = self.MPDATE_nsprefix_ + ':' if (UseCapturedNS_ and self.MPDATE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMPDATE>%s</%sMPDATE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MPDATE), input_name='MPDATE')), namespaceprefix_ , eol_))
        if self.MPSUFFIX is not None:
            namespaceprefix_ = self.MPSUFFIX_nsprefix_ + ':' if (UseCapturedNS_ and self.MPSUFFIX_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMPSUFFIX>%s</%sMPSUFFIX>%s' % (namespaceprefix_ , self.gds_format_integer(self.MPSUFFIX, input_name='MPSUFFIX'), namespaceprefix_ , eol_))
        if self.OriginCity is not None:
            namespaceprefix_ = self.OriginCity_nsprefix_ + ':' if (UseCapturedNS_ and self.OriginCity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOriginCity>%s</%sOriginCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OriginCity), input_name='OriginCity')), namespaceprefix_ , eol_))
        if self.OriginCountryCode is not None:
            namespaceprefix_ = self.OriginCountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.OriginCountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOriginCountryCode>%s</%sOriginCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OriginCountryCode), input_name='OriginCountryCode')), namespaceprefix_ , eol_))
        if self.OriginState is not None:
            namespaceprefix_ = self.OriginState_nsprefix_ + ':' if (UseCapturedNS_ and self.OriginState_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOriginState>%s</%sOriginState>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OriginState), input_name='OriginState')), namespaceprefix_ , eol_))
        if self.OriginZip is not None:
            namespaceprefix_ = self.OriginZip_nsprefix_ + ':' if (UseCapturedNS_ and self.OriginZip_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOriginZip>%s</%sOriginZip>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OriginZip), input_name='OriginZip')), namespaceprefix_ , eol_))
        if self.PodEnabled is not None:
            namespaceprefix_ = self.PodEnabled_nsprefix_ + ':' if (UseCapturedNS_ and self.PodEnabled_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPodEnabled>%s</%sPodEnabled>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PodEnabled), input_name='PodEnabled')), namespaceprefix_ , eol_))
        if self.PredictedDeliveryDate is not None:
            namespaceprefix_ = self.PredictedDeliveryDate_nsprefix_ + ':' if (UseCapturedNS_ and self.PredictedDeliveryDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPredictedDeliveryDate>%s</%sPredictedDeliveryDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PredictedDeliveryDate), input_name='PredictedDeliveryDate')), namespaceprefix_ , eol_))
        if self.PredictedDeliveryTime is not None:
            namespaceprefix_ = self.PredictedDeliveryTime_nsprefix_ + ':' if (UseCapturedNS_ and self.PredictedDeliveryTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPredictedDeliveryTime>%s</%sPredictedDeliveryTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PredictedDeliveryTime), input_name='PredictedDeliveryTime')), namespaceprefix_ , eol_))
        if self.PDWStart is not None:
            namespaceprefix_ = self.PDWStart_nsprefix_ + ':' if (UseCapturedNS_ and self.PDWStart_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPDWStart>%s</%sPDWStart>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PDWStart), input_name='PDWStart')), namespaceprefix_ , eol_))
        if self.PDWEnd is not None:
            namespaceprefix_ = self.PDWEnd_nsprefix_ + ':' if (UseCapturedNS_ and self.PDWEnd_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPDWEnd>%s</%sPDWEnd>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PDWEnd), input_name='PDWEnd')), namespaceprefix_ , eol_))
        if self.RelatedRRID is not None:
            namespaceprefix_ = self.RelatedRRID_nsprefix_ + ':' if (UseCapturedNS_ and self.RelatedRRID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRelatedRRID>%s</%sRelatedRRID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.RelatedRRID), input_name='RelatedRRID')), namespaceprefix_ , eol_))
        if self.RestoreEnabled is not None:
            namespaceprefix_ = self.RestoreEnabled_nsprefix_ + ':' if (UseCapturedNS_ and self.RestoreEnabled_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRestoreEnabled>%s</%sRestoreEnabled>%s' % (namespaceprefix_ , self.gds_format_boolean(self.RestoreEnabled, input_name='RestoreEnabled'), namespaceprefix_ , eol_))
        if self.RRAMenabled is not None:
            namespaceprefix_ = self.RRAMenabled_nsprefix_ + ':' if (UseCapturedNS_ and self.RRAMenabled_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRRAMenabled>%s</%sRRAMenabled>%s' % (namespaceprefix_ , self.gds_format_boolean(self.RRAMenabled, input_name='RRAMenabled'), namespaceprefix_ , eol_))
        if self.RreEnabled is not None:
            namespaceprefix_ = self.RreEnabled_nsprefix_ + ':' if (UseCapturedNS_ and self.RreEnabled_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRreEnabled>%s</%sRreEnabled>%s' % (namespaceprefix_ , self.gds_format_boolean(self.RreEnabled, input_name='RreEnabled'), namespaceprefix_ , eol_))
        if self.Service is not None:
            namespaceprefix_ = self.Service_nsprefix_ + ':' if (UseCapturedNS_ and self.Service_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sService>%s</%sService>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Service), input_name='Service')), namespaceprefix_ , eol_))
        if self.ServiceTypeCode is not None:
            namespaceprefix_ = self.ServiceTypeCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceTypeCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceTypeCode>%s</%sServiceTypeCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServiceTypeCode), input_name='ServiceTypeCode')), namespaceprefix_ , eol_))
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStatus>%s</%sStatus>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Status), input_name='Status')), namespaceprefix_ , eol_))
        if self.StatusCategory is not None:
            namespaceprefix_ = self.StatusCategory_nsprefix_ + ':' if (UseCapturedNS_ and self.StatusCategory_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStatusCategory>%s</%sStatusCategory>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.StatusCategory), input_name='StatusCategory')), namespaceprefix_ , eol_))
        if self.StatusSummary is not None:
            namespaceprefix_ = self.StatusSummary_nsprefix_ + ':' if (UseCapturedNS_ and self.StatusSummary_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStatusSummary>%s</%sStatusSummary>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.StatusSummary), input_name='StatusSummary')), namespaceprefix_ , eol_))
        if self.TABLECODE is not None:
            namespaceprefix_ = self.TABLECODE_nsprefix_ + ':' if (UseCapturedNS_ and self.TABLECODE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTABLECODE>%s</%sTABLECODE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TABLECODE), input_name='TABLECODE')), namespaceprefix_ , eol_))
        if self.TpodEnabled is not None:
            namespaceprefix_ = self.TpodEnabled_nsprefix_ + ':' if (UseCapturedNS_ and self.TpodEnabled_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTpodEnabled>%s</%sTpodEnabled>%s' % (namespaceprefix_ , self.gds_format_boolean(self.TpodEnabled, input_name='TpodEnabled'), namespaceprefix_ , eol_))
        if self.ValueofArticle is not None:
            namespaceprefix_ = self.ValueofArticle_nsprefix_ + ':' if (UseCapturedNS_ and self.ValueofArticle_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sValueofArticle>%s</%sValueofArticle>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ValueofArticle), input_name='ValueofArticle')), namespaceprefix_ , eol_))
        if self.EnabledNotificationRequests is not None:
            namespaceprefix_ = self.EnabledNotificationRequests_nsprefix_ + ':' if (UseCapturedNS_ and self.EnabledNotificationRequests_nsprefix_) else ''
            self.EnabledNotificationRequests.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EnabledNotificationRequests', pretty_print=pretty_print)
        if self.TrackSummary is not None:
            namespaceprefix_ = self.TrackSummary_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackSummary_nsprefix_) else ''
            self.TrackSummary.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TrackSummary', pretty_print=pretty_print)
        for TrackDetail_ in self.TrackDetail:
            namespaceprefix_ = self.TrackDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackDetail_nsprefix_) else ''
            TrackDetail_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TrackDetail', pretty_print=pretty_print)
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
        value = find_attr_value_('ID', node)
        if value is not None and 'ID' not in already_processed:
            already_processed.add('ID')
            self.ID = value
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'AdditionalInfo':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AdditionalInfo')
            value_ = self.gds_validate_string(value_, node, 'AdditionalInfo')
            self.AdditionalInfo = value_
            self.AdditionalInfo_nsprefix_ = child_.prefix
        elif nodeName_ == 'ADPScripting':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ADPScripting')
            value_ = self.gds_validate_string(value_, node, 'ADPScripting')
            self.ADPScripting = value_
            self.ADPScripting_nsprefix_ = child_.prefix
        elif nodeName_ == 'ARCHDATA':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'ARCHDATA')
            ival_ = self.gds_validate_boolean(ival_, node, 'ARCHDATA')
            self.ARCHDATA = ival_
            self.ARCHDATA_nsprefix_ = child_.prefix
        elif nodeName_ == 'ArchiveRestoreInfo':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ArchiveRestoreInfo')
            value_ = self.gds_validate_string(value_, node, 'ArchiveRestoreInfo')
            self.ArchiveRestoreInfo = value_
            self.ArchiveRestoreInfo_nsprefix_ = child_.prefix
        elif nodeName_ == 'AssociatedLabel':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AssociatedLabel')
            value_ = self.gds_validate_string(value_, node, 'AssociatedLabel')
            self.AssociatedLabel = value_
            self.AssociatedLabel_nsprefix_ = child_.prefix
        elif nodeName_ == 'Class':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Class')
            value_ = self.gds_validate_string(value_, node, 'Class')
            self.Class = value_
            self.Class_nsprefix_ = child_.prefix
        elif nodeName_ == 'ClassOfMailCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ClassOfMailCode')
            value_ = self.gds_validate_string(value_, node, 'ClassOfMailCode')
            self.ClassOfMailCode = value_
            self.ClassOfMailCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'DeliveryNotificationDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DeliveryNotificationDate')
            value_ = self.gds_validate_string(value_, node, 'DeliveryNotificationDate')
            self.DeliveryNotificationDate = value_
            self.DeliveryNotificationDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'DestinationCity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DestinationCity')
            value_ = self.gds_validate_string(value_, node, 'DestinationCity')
            self.DestinationCity = value_
            self.DestinationCity_nsprefix_ = child_.prefix
        elif nodeName_ == 'DestinationCountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DestinationCountryCode')
            value_ = self.gds_validate_string(value_, node, 'DestinationCountryCode')
            self.DestinationCountryCode = value_
            self.DestinationCountryCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'DestinationState':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DestinationState')
            value_ = self.gds_validate_string(value_, node, 'DestinationState')
            self.DestinationState = value_
            self.DestinationState_nsprefix_ = child_.prefix
        elif nodeName_ == 'DestinationZip' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'DestinationZip')
            ival_ = self.gds_validate_integer(ival_, node, 'DestinationZip')
            self.DestinationZip = ival_
            self.DestinationZip_nsprefix_ = child_.prefix
        elif nodeName_ == 'EditedLabelID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EditedLabelID')
            value_ = self.gds_validate_string(value_, node, 'EditedLabelID')
            self.EditedLabelID = value_
            self.EditedLabelID_nsprefix_ = child_.prefix
        elif nodeName_ == 'EmailEnabled':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EmailEnabled')
            value_ = self.gds_validate_string(value_, node, 'EmailEnabled')
            self.EmailEnabled = value_
            self.EmailEnabled_nsprefix_ = child_.prefix
        elif nodeName_ == 'ExpectedDeliveryDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ExpectedDeliveryDate')
            value_ = self.gds_validate_string(value_, node, 'ExpectedDeliveryDate')
            self.ExpectedDeliveryDate = value_
            self.ExpectedDeliveryDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'ExpectedDeliveryTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ExpectedDeliveryTime')
            value_ = self.gds_validate_string(value_, node, 'ExpectedDeliveryTime')
            self.ExpectedDeliveryTime = value_
            self.ExpectedDeliveryTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'GuaranteedDeliveryDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GuaranteedDeliveryDate')
            value_ = self.gds_validate_string(value_, node, 'GuaranteedDeliveryDate')
            self.GuaranteedDeliveryDate = value_
            self.GuaranteedDeliveryDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'GuaranteedDeliveryTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GuaranteedDeliveryTime')
            value_ = self.gds_validate_string(value_, node, 'GuaranteedDeliveryTime')
            self.GuaranteedDeliveryTime = value_
            self.GuaranteedDeliveryTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'GuaranteedDetails':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GuaranteedDetails')
            value_ = self.gds_validate_string(value_, node, 'GuaranteedDetails')
            self.GuaranteedDetails = value_
            self.GuaranteedDetails_nsprefix_ = child_.prefix
        elif nodeName_ == 'KahalaIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'KahalaIndicator')
            value_ = self.gds_validate_string(value_, node, 'KahalaIndicator')
            self.KahalaIndicator = value_
            self.KahalaIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'MailTypeCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MailTypeCode')
            value_ = self.gds_validate_string(value_, node, 'MailTypeCode')
            self.MailTypeCode = value_
            self.MailTypeCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'MPDATE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MPDATE')
            value_ = self.gds_validate_string(value_, node, 'MPDATE')
            self.MPDATE = value_
            self.MPDATE_nsprefix_ = child_.prefix
        elif nodeName_ == 'MPSUFFIX' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'MPSUFFIX')
            ival_ = self.gds_validate_integer(ival_, node, 'MPSUFFIX')
            self.MPSUFFIX = ival_
            self.MPSUFFIX_nsprefix_ = child_.prefix
        elif nodeName_ == 'OriginCity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OriginCity')
            value_ = self.gds_validate_string(value_, node, 'OriginCity')
            self.OriginCity = value_
            self.OriginCity_nsprefix_ = child_.prefix
        elif nodeName_ == 'OriginCountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OriginCountryCode')
            value_ = self.gds_validate_string(value_, node, 'OriginCountryCode')
            self.OriginCountryCode = value_
            self.OriginCountryCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'OriginState':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OriginState')
            value_ = self.gds_validate_string(value_, node, 'OriginState')
            self.OriginState = value_
            self.OriginState_nsprefix_ = child_.prefix
        elif nodeName_ == 'OriginZip':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OriginZip')
            value_ = self.gds_validate_string(value_, node, 'OriginZip')
            self.OriginZip = value_
            self.OriginZip_nsprefix_ = child_.prefix
        elif nodeName_ == 'PodEnabled':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PodEnabled')
            value_ = self.gds_validate_string(value_, node, 'PodEnabled')
            self.PodEnabled = value_
            self.PodEnabled_nsprefix_ = child_.prefix
        elif nodeName_ == 'PredictedDeliveryDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PredictedDeliveryDate')
            value_ = self.gds_validate_string(value_, node, 'PredictedDeliveryDate')
            self.PredictedDeliveryDate = value_
            self.PredictedDeliveryDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'PredictedDeliveryTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PredictedDeliveryTime')
            value_ = self.gds_validate_string(value_, node, 'PredictedDeliveryTime')
            self.PredictedDeliveryTime = value_
            self.PredictedDeliveryTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'PDWStart':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PDWStart')
            value_ = self.gds_validate_string(value_, node, 'PDWStart')
            self.PDWStart = value_
            self.PDWStart_nsprefix_ = child_.prefix
        elif nodeName_ == 'PDWEnd':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PDWEnd')
            value_ = self.gds_validate_string(value_, node, 'PDWEnd')
            self.PDWEnd = value_
            self.PDWEnd_nsprefix_ = child_.prefix
        elif nodeName_ == 'RelatedRRID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RelatedRRID')
            value_ = self.gds_validate_string(value_, node, 'RelatedRRID')
            self.RelatedRRID = value_
            self.RelatedRRID_nsprefix_ = child_.prefix
        elif nodeName_ == 'RestoreEnabled':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'RestoreEnabled')
            ival_ = self.gds_validate_boolean(ival_, node, 'RestoreEnabled')
            self.RestoreEnabled = ival_
            self.RestoreEnabled_nsprefix_ = child_.prefix
        elif nodeName_ == 'RRAMenabled':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'RRAMenabled')
            ival_ = self.gds_validate_boolean(ival_, node, 'RRAMenabled')
            self.RRAMenabled = ival_
            self.RRAMenabled_nsprefix_ = child_.prefix
        elif nodeName_ == 'RreEnabled':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'RreEnabled')
            ival_ = self.gds_validate_boolean(ival_, node, 'RreEnabled')
            self.RreEnabled = ival_
            self.RreEnabled_nsprefix_ = child_.prefix
        elif nodeName_ == 'Service':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Service')
            value_ = self.gds_validate_string(value_, node, 'Service')
            self.Service = value_
            self.Service_nsprefix_ = child_.prefix
        elif nodeName_ == 'ServiceTypeCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServiceTypeCode')
            value_ = self.gds_validate_string(value_, node, 'ServiceTypeCode')
            self.ServiceTypeCode = value_
            self.ServiceTypeCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'Status':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Status')
            value_ = self.gds_validate_string(value_, node, 'Status')
            self.Status = value_
            self.Status_nsprefix_ = child_.prefix
        elif nodeName_ == 'StatusCategory':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'StatusCategory')
            value_ = self.gds_validate_string(value_, node, 'StatusCategory')
            self.StatusCategory = value_
            self.StatusCategory_nsprefix_ = child_.prefix
        elif nodeName_ == 'StatusSummary':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'StatusSummary')
            value_ = self.gds_validate_string(value_, node, 'StatusSummary')
            self.StatusSummary = value_
            self.StatusSummary_nsprefix_ = child_.prefix
        elif nodeName_ == 'TABLECODE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TABLECODE')
            value_ = self.gds_validate_string(value_, node, 'TABLECODE')
            self.TABLECODE = value_
            self.TABLECODE_nsprefix_ = child_.prefix
        elif nodeName_ == 'TpodEnabled':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'TpodEnabled')
            ival_ = self.gds_validate_boolean(ival_, node, 'TpodEnabled')
            self.TpodEnabled = ival_
            self.TpodEnabled_nsprefix_ = child_.prefix
        elif nodeName_ == 'ValueofArticle':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ValueofArticle')
            value_ = self.gds_validate_string(value_, node, 'ValueofArticle')
            self.ValueofArticle = value_
            self.ValueofArticle_nsprefix_ = child_.prefix
        elif nodeName_ == 'EnabledNotificationRequests':
            obj_ = EnabledNotificationRequestsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EnabledNotificationRequests = obj_
            obj_.original_tagname_ = 'EnabledNotificationRequests'
        elif nodeName_ == 'TrackSummary':
            obj_ = TrackSummaryType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TrackSummary = obj_
            obj_.original_tagname_ = 'TrackSummary'
        elif nodeName_ == 'TrackDetail':
            obj_ = TrackDetailType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TrackDetail.append(obj_)
            obj_.original_tagname_ = 'TrackDetail'
# end class TrackInfoType


class EnabledNotificationRequestsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, SMS=None, EMAIL=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.SMS = SMS
        self.SMS_nsprefix_ = None
        self.EMAIL = EMAIL
        self.EMAIL_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EnabledNotificationRequestsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EnabledNotificationRequestsType.subclass:
            return EnabledNotificationRequestsType.subclass(*args_, **kwargs_)
        else:
            return EnabledNotificationRequestsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_SMS(self):
        return self.SMS
    def set_SMS(self, SMS):
        self.SMS = SMS
    def get_EMAIL(self):
        return self.EMAIL
    def set_EMAIL(self, EMAIL):
        self.EMAIL = EMAIL
    def hasContent_(self):
        if (
            self.SMS is not None or
            self.EMAIL is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EnabledNotificationRequestsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EnabledNotificationRequestsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EnabledNotificationRequestsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EnabledNotificationRequestsType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='EnabledNotificationRequestsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EnabledNotificationRequestsType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EnabledNotificationRequestsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.SMS is not None:
            namespaceprefix_ = self.SMS_nsprefix_ + ':' if (UseCapturedNS_ and self.SMS_nsprefix_) else ''
            self.SMS.export(outfile, level, namespaceprefix_, namespacedef_='', name_='SMS', pretty_print=pretty_print)
        if self.EMAIL is not None:
            namespaceprefix_ = self.EMAIL_nsprefix_ + ':' if (UseCapturedNS_ and self.EMAIL_nsprefix_) else ''
            self.EMAIL.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EMAIL', pretty_print=pretty_print)
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
        if nodeName_ == 'SMS':
            obj_ = SMSType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SMS = obj_
            obj_.original_tagname_ = 'SMS'
        elif nodeName_ == 'EMAIL':
            obj_ = EMAILType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EMAIL = obj_
            obj_.original_tagname_ = 'EMAIL'
# end class EnabledNotificationRequestsType


class SMSType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, FD=None, AL=None, TD=None, UP=None, DND=None, FS=None, OA=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.FD = FD
        self.FD_nsprefix_ = None
        self.AL = AL
        self.AL_nsprefix_ = None
        self.TD = TD
        self.TD_nsprefix_ = None
        self.UP = UP
        self.UP_nsprefix_ = None
        self.DND = DND
        self.DND_nsprefix_ = None
        self.FS = FS
        self.FS_nsprefix_ = None
        self.OA = OA
        self.OA_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SMSType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SMSType.subclass:
            return SMSType.subclass(*args_, **kwargs_)
        else:
            return SMSType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_FD(self):
        return self.FD
    def set_FD(self, FD):
        self.FD = FD
    def get_AL(self):
        return self.AL
    def set_AL(self, AL):
        self.AL = AL
    def get_TD(self):
        return self.TD
    def set_TD(self, TD):
        self.TD = TD
    def get_UP(self):
        return self.UP
    def set_UP(self, UP):
        self.UP = UP
    def get_DND(self):
        return self.DND
    def set_DND(self, DND):
        self.DND = DND
    def get_FS(self):
        return self.FS
    def set_FS(self, FS):
        self.FS = FS
    def get_OA(self):
        return self.OA
    def set_OA(self, OA):
        self.OA = OA
    def hasContent_(self):
        if (
            self.FD is not None or
            self.AL is not None or
            self.TD is not None or
            self.UP is not None or
            self.DND is not None or
            self.FS is not None or
            self.OA is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SMSType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SMSType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SMSType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SMSType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SMSType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SMSType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SMSType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.FD is not None:
            namespaceprefix_ = self.FD_nsprefix_ + ':' if (UseCapturedNS_ and self.FD_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFD>%s</%sFD>%s' % (namespaceprefix_ , self.gds_format_boolean(self.FD, input_name='FD'), namespaceprefix_ , eol_))
        if self.AL is not None:
            namespaceprefix_ = self.AL_nsprefix_ + ':' if (UseCapturedNS_ and self.AL_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAL>%s</%sAL>%s' % (namespaceprefix_ , self.gds_format_boolean(self.AL, input_name='AL'), namespaceprefix_ , eol_))
        if self.TD is not None:
            namespaceprefix_ = self.TD_nsprefix_ + ':' if (UseCapturedNS_ and self.TD_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTD>%s</%sTD>%s' % (namespaceprefix_ , self.gds_format_boolean(self.TD, input_name='TD'), namespaceprefix_ , eol_))
        if self.UP is not None:
            namespaceprefix_ = self.UP_nsprefix_ + ':' if (UseCapturedNS_ and self.UP_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUP>%s</%sUP>%s' % (namespaceprefix_ , self.gds_format_boolean(self.UP, input_name='UP'), namespaceprefix_ , eol_))
        if self.DND is not None:
            namespaceprefix_ = self.DND_nsprefix_ + ':' if (UseCapturedNS_ and self.DND_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDND>%s</%sDND>%s' % (namespaceprefix_ , self.gds_format_boolean(self.DND, input_name='DND'), namespaceprefix_ , eol_))
        if self.FS is not None:
            namespaceprefix_ = self.FS_nsprefix_ + ':' if (UseCapturedNS_ and self.FS_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFS>%s</%sFS>%s' % (namespaceprefix_ , self.gds_format_boolean(self.FS, input_name='FS'), namespaceprefix_ , eol_))
        if self.OA is not None:
            namespaceprefix_ = self.OA_nsprefix_ + ':' if (UseCapturedNS_ and self.OA_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOA>%s</%sOA>%s' % (namespaceprefix_ , self.gds_format_boolean(self.OA, input_name='OA'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'FD':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'FD')
            ival_ = self.gds_validate_boolean(ival_, node, 'FD')
            self.FD = ival_
            self.FD_nsprefix_ = child_.prefix
        elif nodeName_ == 'AL':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'AL')
            ival_ = self.gds_validate_boolean(ival_, node, 'AL')
            self.AL = ival_
            self.AL_nsprefix_ = child_.prefix
        elif nodeName_ == 'TD':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'TD')
            ival_ = self.gds_validate_boolean(ival_, node, 'TD')
            self.TD = ival_
            self.TD_nsprefix_ = child_.prefix
        elif nodeName_ == 'UP':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'UP')
            ival_ = self.gds_validate_boolean(ival_, node, 'UP')
            self.UP = ival_
            self.UP_nsprefix_ = child_.prefix
        elif nodeName_ == 'DND':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'DND')
            ival_ = self.gds_validate_boolean(ival_, node, 'DND')
            self.DND = ival_
            self.DND_nsprefix_ = child_.prefix
        elif nodeName_ == 'FS':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'FS')
            ival_ = self.gds_validate_boolean(ival_, node, 'FS')
            self.FS = ival_
            self.FS_nsprefix_ = child_.prefix
        elif nodeName_ == 'OA':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'OA')
            ival_ = self.gds_validate_boolean(ival_, node, 'OA')
            self.OA = ival_
            self.OA_nsprefix_ = child_.prefix
# end class SMSType


class EMAILType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, FD=None, AL=None, TD=None, UP=None, DND=None, FS=None, OA=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.FD = FD
        self.FD_nsprefix_ = None
        self.AL = AL
        self.AL_nsprefix_ = None
        self.TD = TD
        self.TD_nsprefix_ = None
        self.UP = UP
        self.UP_nsprefix_ = None
        self.DND = DND
        self.DND_nsprefix_ = None
        self.FS = FS
        self.FS_nsprefix_ = None
        self.OA = OA
        self.OA_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EMAILType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EMAILType.subclass:
            return EMAILType.subclass(*args_, **kwargs_)
        else:
            return EMAILType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_FD(self):
        return self.FD
    def set_FD(self, FD):
        self.FD = FD
    def get_AL(self):
        return self.AL
    def set_AL(self, AL):
        self.AL = AL
    def get_TD(self):
        return self.TD
    def set_TD(self, TD):
        self.TD = TD
    def get_UP(self):
        return self.UP
    def set_UP(self, UP):
        self.UP = UP
    def get_DND(self):
        return self.DND
    def set_DND(self, DND):
        self.DND = DND
    def get_FS(self):
        return self.FS
    def set_FS(self, FS):
        self.FS = FS
    def get_OA(self):
        return self.OA
    def set_OA(self, OA):
        self.OA = OA
    def hasContent_(self):
        if (
            self.FD is not None or
            self.AL is not None or
            self.TD is not None or
            self.UP is not None or
            self.DND is not None or
            self.FS is not None or
            self.OA is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EMAILType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EMAILType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EMAILType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EMAILType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='EMAILType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EMAILType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EMAILType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.FD is not None:
            namespaceprefix_ = self.FD_nsprefix_ + ':' if (UseCapturedNS_ and self.FD_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFD>%s</%sFD>%s' % (namespaceprefix_ , self.gds_format_boolean(self.FD, input_name='FD'), namespaceprefix_ , eol_))
        if self.AL is not None:
            namespaceprefix_ = self.AL_nsprefix_ + ':' if (UseCapturedNS_ and self.AL_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAL>%s</%sAL>%s' % (namespaceprefix_ , self.gds_format_boolean(self.AL, input_name='AL'), namespaceprefix_ , eol_))
        if self.TD is not None:
            namespaceprefix_ = self.TD_nsprefix_ + ':' if (UseCapturedNS_ and self.TD_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTD>%s</%sTD>%s' % (namespaceprefix_ , self.gds_format_boolean(self.TD, input_name='TD'), namespaceprefix_ , eol_))
        if self.UP is not None:
            namespaceprefix_ = self.UP_nsprefix_ + ':' if (UseCapturedNS_ and self.UP_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUP>%s</%sUP>%s' % (namespaceprefix_ , self.gds_format_boolean(self.UP, input_name='UP'), namespaceprefix_ , eol_))
        if self.DND is not None:
            namespaceprefix_ = self.DND_nsprefix_ + ':' if (UseCapturedNS_ and self.DND_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDND>%s</%sDND>%s' % (namespaceprefix_ , self.gds_format_boolean(self.DND, input_name='DND'), namespaceprefix_ , eol_))
        if self.FS is not None:
            namespaceprefix_ = self.FS_nsprefix_ + ':' if (UseCapturedNS_ and self.FS_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFS>%s</%sFS>%s' % (namespaceprefix_ , self.gds_format_boolean(self.FS, input_name='FS'), namespaceprefix_ , eol_))
        if self.OA is not None:
            namespaceprefix_ = self.OA_nsprefix_ + ':' if (UseCapturedNS_ and self.OA_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOA>%s</%sOA>%s' % (namespaceprefix_ , self.gds_format_boolean(self.OA, input_name='OA'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'FD':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'FD')
            ival_ = self.gds_validate_boolean(ival_, node, 'FD')
            self.FD = ival_
            self.FD_nsprefix_ = child_.prefix
        elif nodeName_ == 'AL':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'AL')
            ival_ = self.gds_validate_boolean(ival_, node, 'AL')
            self.AL = ival_
            self.AL_nsprefix_ = child_.prefix
        elif nodeName_ == 'TD':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'TD')
            ival_ = self.gds_validate_boolean(ival_, node, 'TD')
            self.TD = ival_
            self.TD_nsprefix_ = child_.prefix
        elif nodeName_ == 'UP':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'UP')
            ival_ = self.gds_validate_boolean(ival_, node, 'UP')
            self.UP = ival_
            self.UP_nsprefix_ = child_.prefix
        elif nodeName_ == 'DND':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'DND')
            ival_ = self.gds_validate_boolean(ival_, node, 'DND')
            self.DND = ival_
            self.DND_nsprefix_ = child_.prefix
        elif nodeName_ == 'FS':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'FS')
            ival_ = self.gds_validate_boolean(ival_, node, 'FS')
            self.FS = ival_
            self.FS_nsprefix_ = child_.prefix
        elif nodeName_ == 'OA':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'OA')
            ival_ = self.gds_validate_boolean(ival_, node, 'OA')
            self.OA = ival_
            self.OA_nsprefix_ = child_.prefix
# end class EMAILType


class TrackSummaryType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, EventTime=None, EventDate=None, Event=None, EventCity=None, EventState=None, EventZIPCode=None, EventCountry=None, FirmName=None, Name=None, AuthorizedAgent=None, EventCode=None, ActionCode=None, ReasonCode=None, GeoCertified=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.EventTime = EventTime
        self.EventTime_nsprefix_ = None
        self.EventDate = EventDate
        self.EventDate_nsprefix_ = None
        self.Event = Event
        self.Event_nsprefix_ = None
        self.EventCity = EventCity
        self.EventCity_nsprefix_ = None
        self.EventState = EventState
        self.EventState_nsprefix_ = None
        self.EventZIPCode = EventZIPCode
        self.EventZIPCode_nsprefix_ = None
        self.EventCountry = EventCountry
        self.EventCountry_nsprefix_ = None
        self.FirmName = FirmName
        self.FirmName_nsprefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = None
        self.AuthorizedAgent = AuthorizedAgent
        self.AuthorizedAgent_nsprefix_ = None
        self.EventCode = EventCode
        self.EventCode_nsprefix_ = None
        self.ActionCode = ActionCode
        self.ActionCode_nsprefix_ = None
        self.ReasonCode = ReasonCode
        self.ReasonCode_nsprefix_ = None
        self.GeoCertified = GeoCertified
        self.GeoCertified_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TrackSummaryType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TrackSummaryType.subclass:
            return TrackSummaryType.subclass(*args_, **kwargs_)
        else:
            return TrackSummaryType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_EventTime(self):
        return self.EventTime
    def set_EventTime(self, EventTime):
        self.EventTime = EventTime
    def get_EventDate(self):
        return self.EventDate
    def set_EventDate(self, EventDate):
        self.EventDate = EventDate
    def get_Event(self):
        return self.Event
    def set_Event(self, Event):
        self.Event = Event
    def get_EventCity(self):
        return self.EventCity
    def set_EventCity(self, EventCity):
        self.EventCity = EventCity
    def get_EventState(self):
        return self.EventState
    def set_EventState(self, EventState):
        self.EventState = EventState
    def get_EventZIPCode(self):
        return self.EventZIPCode
    def set_EventZIPCode(self, EventZIPCode):
        self.EventZIPCode = EventZIPCode
    def get_EventCountry(self):
        return self.EventCountry
    def set_EventCountry(self, EventCountry):
        self.EventCountry = EventCountry
    def get_FirmName(self):
        return self.FirmName
    def set_FirmName(self, FirmName):
        self.FirmName = FirmName
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def get_AuthorizedAgent(self):
        return self.AuthorizedAgent
    def set_AuthorizedAgent(self, AuthorizedAgent):
        self.AuthorizedAgent = AuthorizedAgent
    def get_EventCode(self):
        return self.EventCode
    def set_EventCode(self, EventCode):
        self.EventCode = EventCode
    def get_ActionCode(self):
        return self.ActionCode
    def set_ActionCode(self, ActionCode):
        self.ActionCode = ActionCode
    def get_ReasonCode(self):
        return self.ReasonCode
    def set_ReasonCode(self, ReasonCode):
        self.ReasonCode = ReasonCode
    def get_GeoCertified(self):
        return self.GeoCertified
    def set_GeoCertified(self, GeoCertified):
        self.GeoCertified = GeoCertified
    def hasContent_(self):
        if (
            self.EventTime is not None or
            self.EventDate is not None or
            self.Event is not None or
            self.EventCity is not None or
            self.EventState is not None or
            self.EventZIPCode is not None or
            self.EventCountry is not None or
            self.FirmName is not None or
            self.Name is not None or
            self.AuthorizedAgent is not None or
            self.EventCode is not None or
            self.ActionCode is not None or
            self.ReasonCode is not None or
            self.GeoCertified is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackSummaryType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TrackSummaryType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TrackSummaryType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TrackSummaryType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TrackSummaryType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TrackSummaryType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackSummaryType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.EventTime is not None:
            namespaceprefix_ = self.EventTime_nsprefix_ + ':' if (UseCapturedNS_ and self.EventTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEventTime>%s</%sEventTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EventTime), input_name='EventTime')), namespaceprefix_ , eol_))
        if self.EventDate is not None:
            namespaceprefix_ = self.EventDate_nsprefix_ + ':' if (UseCapturedNS_ and self.EventDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEventDate>%s</%sEventDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EventDate), input_name='EventDate')), namespaceprefix_ , eol_))
        if self.Event is not None:
            namespaceprefix_ = self.Event_nsprefix_ + ':' if (UseCapturedNS_ and self.Event_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEvent>%s</%sEvent>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Event), input_name='Event')), namespaceprefix_ , eol_))
        if self.EventCity is not None:
            namespaceprefix_ = self.EventCity_nsprefix_ + ':' if (UseCapturedNS_ and self.EventCity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEventCity>%s</%sEventCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EventCity), input_name='EventCity')), namespaceprefix_ , eol_))
        if self.EventState is not None:
            namespaceprefix_ = self.EventState_nsprefix_ + ':' if (UseCapturedNS_ and self.EventState_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEventState>%s</%sEventState>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EventState), input_name='EventState')), namespaceprefix_ , eol_))
        if self.EventZIPCode is not None:
            namespaceprefix_ = self.EventZIPCode_nsprefix_ + ':' if (UseCapturedNS_ and self.EventZIPCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEventZIPCode>%s</%sEventZIPCode>%s' % (namespaceprefix_ , self.gds_format_integer(self.EventZIPCode, input_name='EventZIPCode'), namespaceprefix_ , eol_))
        if self.EventCountry is not None:
            namespaceprefix_ = self.EventCountry_nsprefix_ + ':' if (UseCapturedNS_ and self.EventCountry_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEventCountry>%s</%sEventCountry>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EventCountry), input_name='EventCountry')), namespaceprefix_ , eol_))
        if self.FirmName is not None:
            namespaceprefix_ = self.FirmName_nsprefix_ + ':' if (UseCapturedNS_ and self.FirmName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFirmName>%s</%sFirmName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FirmName), input_name='FirmName')), namespaceprefix_ , eol_))
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName>%s</%sName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name), input_name='Name')), namespaceprefix_ , eol_))
        if self.AuthorizedAgent is not None:
            namespaceprefix_ = self.AuthorizedAgent_nsprefix_ + ':' if (UseCapturedNS_ and self.AuthorizedAgent_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAuthorizedAgent>%s</%sAuthorizedAgent>%s' % (namespaceprefix_ , self.gds_format_boolean(self.AuthorizedAgent, input_name='AuthorizedAgent'), namespaceprefix_ , eol_))
        if self.EventCode is not None:
            namespaceprefix_ = self.EventCode_nsprefix_ + ':' if (UseCapturedNS_ and self.EventCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEventCode>%s</%sEventCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EventCode), input_name='EventCode')), namespaceprefix_ , eol_))
        if self.ActionCode is not None:
            namespaceprefix_ = self.ActionCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ActionCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sActionCode>%s</%sActionCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ActionCode), input_name='ActionCode')), namespaceprefix_ , eol_))
        if self.ReasonCode is not None:
            namespaceprefix_ = self.ReasonCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ReasonCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReasonCode>%s</%sReasonCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ReasonCode), input_name='ReasonCode')), namespaceprefix_ , eol_))
        if self.GeoCertified is not None:
            namespaceprefix_ = self.GeoCertified_nsprefix_ + ':' if (UseCapturedNS_ and self.GeoCertified_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGeoCertified>%s</%sGeoCertified>%s' % (namespaceprefix_ , self.gds_format_boolean(self.GeoCertified, input_name='GeoCertified'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'EventTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EventTime')
            value_ = self.gds_validate_string(value_, node, 'EventTime')
            self.EventTime = value_
            self.EventTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'EventDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EventDate')
            value_ = self.gds_validate_string(value_, node, 'EventDate')
            self.EventDate = value_
            self.EventDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'Event':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Event')
            value_ = self.gds_validate_string(value_, node, 'Event')
            self.Event = value_
            self.Event_nsprefix_ = child_.prefix
        elif nodeName_ == 'EventCity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EventCity')
            value_ = self.gds_validate_string(value_, node, 'EventCity')
            self.EventCity = value_
            self.EventCity_nsprefix_ = child_.prefix
        elif nodeName_ == 'EventState':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EventState')
            value_ = self.gds_validate_string(value_, node, 'EventState')
            self.EventState = value_
            self.EventState_nsprefix_ = child_.prefix
        elif nodeName_ == 'EventZIPCode' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'EventZIPCode')
            ival_ = self.gds_validate_integer(ival_, node, 'EventZIPCode')
            self.EventZIPCode = ival_
            self.EventZIPCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'EventCountry':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EventCountry')
            value_ = self.gds_validate_string(value_, node, 'EventCountry')
            self.EventCountry = value_
            self.EventCountry_nsprefix_ = child_.prefix
        elif nodeName_ == 'FirmName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FirmName')
            value_ = self.gds_validate_string(value_, node, 'FirmName')
            self.FirmName = value_
            self.FirmName_nsprefix_ = child_.prefix
        elif nodeName_ == 'Name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Name')
            value_ = self.gds_validate_string(value_, node, 'Name')
            self.Name = value_
            self.Name_nsprefix_ = child_.prefix
        elif nodeName_ == 'AuthorizedAgent':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'AuthorizedAgent')
            ival_ = self.gds_validate_boolean(ival_, node, 'AuthorizedAgent')
            self.AuthorizedAgent = ival_
            self.AuthorizedAgent_nsprefix_ = child_.prefix
        elif nodeName_ == 'EventCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EventCode')
            value_ = self.gds_validate_string(value_, node, 'EventCode')
            self.EventCode = value_
            self.EventCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'ActionCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ActionCode')
            value_ = self.gds_validate_string(value_, node, 'ActionCode')
            self.ActionCode = value_
            self.ActionCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'ReasonCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ReasonCode')
            value_ = self.gds_validate_string(value_, node, 'ReasonCode')
            self.ReasonCode = value_
            self.ReasonCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'GeoCertified':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'GeoCertified')
            ival_ = self.gds_validate_boolean(ival_, node, 'GeoCertified')
            self.GeoCertified = ival_
            self.GeoCertified_nsprefix_ = child_.prefix
# end class TrackSummaryType


class TrackDetailType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, EventTime=None, EventDate=None, Event=None, EventCity=None, EventState=None, EventZIPCode=None, EventCountry=None, FirmName=None, Name=None, AuthorizedAgent=None, GeoCertified=None, EventCode=None, ActionCode=None, ReasonCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.EventTime = EventTime
        self.EventTime_nsprefix_ = None
        self.EventDate = EventDate
        self.EventDate_nsprefix_ = None
        self.Event = Event
        self.Event_nsprefix_ = None
        self.EventCity = EventCity
        self.EventCity_nsprefix_ = None
        self.EventState = EventState
        self.EventState_nsprefix_ = None
        self.EventZIPCode = EventZIPCode
        self.EventZIPCode_nsprefix_ = None
        self.EventCountry = EventCountry
        self.EventCountry_nsprefix_ = None
        self.FirmName = FirmName
        self.FirmName_nsprefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = None
        self.AuthorizedAgent = AuthorizedAgent
        self.AuthorizedAgent_nsprefix_ = None
        self.GeoCertified = GeoCertified
        self.GeoCertified_nsprefix_ = None
        self.EventCode = EventCode
        self.EventCode_nsprefix_ = None
        self.ActionCode = ActionCode
        self.ActionCode_nsprefix_ = None
        self.ReasonCode = ReasonCode
        self.ReasonCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TrackDetailType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TrackDetailType.subclass:
            return TrackDetailType.subclass(*args_, **kwargs_)
        else:
            return TrackDetailType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_EventTime(self):
        return self.EventTime
    def set_EventTime(self, EventTime):
        self.EventTime = EventTime
    def get_EventDate(self):
        return self.EventDate
    def set_EventDate(self, EventDate):
        self.EventDate = EventDate
    def get_Event(self):
        return self.Event
    def set_Event(self, Event):
        self.Event = Event
    def get_EventCity(self):
        return self.EventCity
    def set_EventCity(self, EventCity):
        self.EventCity = EventCity
    def get_EventState(self):
        return self.EventState
    def set_EventState(self, EventState):
        self.EventState = EventState
    def get_EventZIPCode(self):
        return self.EventZIPCode
    def set_EventZIPCode(self, EventZIPCode):
        self.EventZIPCode = EventZIPCode
    def get_EventCountry(self):
        return self.EventCountry
    def set_EventCountry(self, EventCountry):
        self.EventCountry = EventCountry
    def get_FirmName(self):
        return self.FirmName
    def set_FirmName(self, FirmName):
        self.FirmName = FirmName
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def get_AuthorizedAgent(self):
        return self.AuthorizedAgent
    def set_AuthorizedAgent(self, AuthorizedAgent):
        self.AuthorizedAgent = AuthorizedAgent
    def get_GeoCertified(self):
        return self.GeoCertified
    def set_GeoCertified(self, GeoCertified):
        self.GeoCertified = GeoCertified
    def get_EventCode(self):
        return self.EventCode
    def set_EventCode(self, EventCode):
        self.EventCode = EventCode
    def get_ActionCode(self):
        return self.ActionCode
    def set_ActionCode(self, ActionCode):
        self.ActionCode = ActionCode
    def get_ReasonCode(self):
        return self.ReasonCode
    def set_ReasonCode(self, ReasonCode):
        self.ReasonCode = ReasonCode
    def hasContent_(self):
        if (
            self.EventTime is not None or
            self.EventDate is not None or
            self.Event is not None or
            self.EventCity is not None or
            self.EventState is not None or
            self.EventZIPCode is not None or
            self.EventCountry is not None or
            self.FirmName is not None or
            self.Name is not None or
            self.AuthorizedAgent is not None or
            self.GeoCertified is not None or
            self.EventCode is not None or
            self.ActionCode is not None or
            self.ReasonCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackDetailType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TrackDetailType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TrackDetailType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TrackDetailType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TrackDetailType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TrackDetailType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackDetailType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.EventTime is not None:
            namespaceprefix_ = self.EventTime_nsprefix_ + ':' if (UseCapturedNS_ and self.EventTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEventTime>%s</%sEventTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EventTime), input_name='EventTime')), namespaceprefix_ , eol_))
        if self.EventDate is not None:
            namespaceprefix_ = self.EventDate_nsprefix_ + ':' if (UseCapturedNS_ and self.EventDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEventDate>%s</%sEventDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EventDate), input_name='EventDate')), namespaceprefix_ , eol_))
        if self.Event is not None:
            namespaceprefix_ = self.Event_nsprefix_ + ':' if (UseCapturedNS_ and self.Event_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEvent>%s</%sEvent>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Event), input_name='Event')), namespaceprefix_ , eol_))
        if self.EventCity is not None:
            namespaceprefix_ = self.EventCity_nsprefix_ + ':' if (UseCapturedNS_ and self.EventCity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEventCity>%s</%sEventCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EventCity), input_name='EventCity')), namespaceprefix_ , eol_))
        if self.EventState is not None:
            namespaceprefix_ = self.EventState_nsprefix_ + ':' if (UseCapturedNS_ and self.EventState_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEventState>%s</%sEventState>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EventState), input_name='EventState')), namespaceprefix_ , eol_))
        if self.EventZIPCode is not None:
            namespaceprefix_ = self.EventZIPCode_nsprefix_ + ':' if (UseCapturedNS_ and self.EventZIPCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEventZIPCode>%s</%sEventZIPCode>%s' % (namespaceprefix_ , self.gds_format_integer(self.EventZIPCode, input_name='EventZIPCode'), namespaceprefix_ , eol_))
        if self.EventCountry is not None:
            namespaceprefix_ = self.EventCountry_nsprefix_ + ':' if (UseCapturedNS_ and self.EventCountry_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEventCountry>%s</%sEventCountry>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EventCountry), input_name='EventCountry')), namespaceprefix_ , eol_))
        if self.FirmName is not None:
            namespaceprefix_ = self.FirmName_nsprefix_ + ':' if (UseCapturedNS_ and self.FirmName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFirmName>%s</%sFirmName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FirmName), input_name='FirmName')), namespaceprefix_ , eol_))
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName>%s</%sName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name), input_name='Name')), namespaceprefix_ , eol_))
        if self.AuthorizedAgent is not None:
            namespaceprefix_ = self.AuthorizedAgent_nsprefix_ + ':' if (UseCapturedNS_ and self.AuthorizedAgent_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAuthorizedAgent>%s</%sAuthorizedAgent>%s' % (namespaceprefix_ , self.gds_format_boolean(self.AuthorizedAgent, input_name='AuthorizedAgent'), namespaceprefix_ , eol_))
        if self.GeoCertified is not None:
            namespaceprefix_ = self.GeoCertified_nsprefix_ + ':' if (UseCapturedNS_ and self.GeoCertified_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGeoCertified>%s</%sGeoCertified>%s' % (namespaceprefix_ , self.gds_format_boolean(self.GeoCertified, input_name='GeoCertified'), namespaceprefix_ , eol_))
        if self.EventCode is not None:
            namespaceprefix_ = self.EventCode_nsprefix_ + ':' if (UseCapturedNS_ and self.EventCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEventCode>%s</%sEventCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EventCode), input_name='EventCode')), namespaceprefix_ , eol_))
        if self.ActionCode is not None:
            namespaceprefix_ = self.ActionCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ActionCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sActionCode>%s</%sActionCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ActionCode), input_name='ActionCode')), namespaceprefix_ , eol_))
        if self.ReasonCode is not None:
            namespaceprefix_ = self.ReasonCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ReasonCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReasonCode>%s</%sReasonCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ReasonCode), input_name='ReasonCode')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'EventTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EventTime')
            value_ = self.gds_validate_string(value_, node, 'EventTime')
            self.EventTime = value_
            self.EventTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'EventDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EventDate')
            value_ = self.gds_validate_string(value_, node, 'EventDate')
            self.EventDate = value_
            self.EventDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'Event':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Event')
            value_ = self.gds_validate_string(value_, node, 'Event')
            self.Event = value_
            self.Event_nsprefix_ = child_.prefix
        elif nodeName_ == 'EventCity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EventCity')
            value_ = self.gds_validate_string(value_, node, 'EventCity')
            self.EventCity = value_
            self.EventCity_nsprefix_ = child_.prefix
        elif nodeName_ == 'EventState':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EventState')
            value_ = self.gds_validate_string(value_, node, 'EventState')
            self.EventState = value_
            self.EventState_nsprefix_ = child_.prefix
        elif nodeName_ == 'EventZIPCode' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'EventZIPCode')
            ival_ = self.gds_validate_integer(ival_, node, 'EventZIPCode')
            self.EventZIPCode = ival_
            self.EventZIPCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'EventCountry':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EventCountry')
            value_ = self.gds_validate_string(value_, node, 'EventCountry')
            self.EventCountry = value_
            self.EventCountry_nsprefix_ = child_.prefix
        elif nodeName_ == 'FirmName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FirmName')
            value_ = self.gds_validate_string(value_, node, 'FirmName')
            self.FirmName = value_
            self.FirmName_nsprefix_ = child_.prefix
        elif nodeName_ == 'Name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Name')
            value_ = self.gds_validate_string(value_, node, 'Name')
            self.Name = value_
            self.Name_nsprefix_ = child_.prefix
        elif nodeName_ == 'AuthorizedAgent':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'AuthorizedAgent')
            ival_ = self.gds_validate_boolean(ival_, node, 'AuthorizedAgent')
            self.AuthorizedAgent = ival_
            self.AuthorizedAgent_nsprefix_ = child_.prefix
        elif nodeName_ == 'GeoCertified':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'GeoCertified')
            ival_ = self.gds_validate_boolean(ival_, node, 'GeoCertified')
            self.GeoCertified = ival_
            self.GeoCertified_nsprefix_ = child_.prefix
        elif nodeName_ == 'EventCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EventCode')
            value_ = self.gds_validate_string(value_, node, 'EventCode')
            self.EventCode = value_
            self.EventCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'ActionCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ActionCode')
            value_ = self.gds_validate_string(value_, node, 'ActionCode')
            self.ActionCode = value_
            self.ActionCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'ReasonCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ReasonCode')
            value_ = self.gds_validate_string(value_, node, 'ReasonCode')
            self.ReasonCode = value_
            self.ReasonCode_nsprefix_ = child_.prefix
# end class TrackDetailType


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
        sys.stdout.write('#from track_response import *\n\n')
        sys.stdout.write('import track_response as model_\n\n')
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
    "EMAILType",
    "EnabledNotificationRequestsType",
    "SMSType",
    "TrackDetailType",
    "TrackInfoType",
    "TrackResponse",
    "TrackSummaryType"
]
