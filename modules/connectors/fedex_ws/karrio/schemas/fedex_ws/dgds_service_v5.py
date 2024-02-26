#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Thu May  6 11:00:03 2021 by generateDS.py version 2.38.6.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './fedex_lib/dgds_service_v5.py')
#
# Command line arguments:
#   /Users/danielkobina/Workspace/Carriers Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./fedex_lib/dgds_service_v5.py" /Users/danielkobina/Workspace/Carriers Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd
#
# Current working directory (os.getcwd()):
#   fedex
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
                value = self.gds_parse_boolean(value, node, input_name)
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


class CarrierCodeType(str, Enum):
    """Identification of a FedEx operating company (transportation)."""
    FDXC='FDXC'
    FDXE='FDXE'
    FDXG='FDXG'
    FXCC='FXCC'
    FXFR='FXFR'
    FXSP='FXSP'


class DangerousGoodsAccessibilityType(str, Enum):
    ACCESSIBLE='ACCESSIBLE'
    INACCESSIBLE='INACCESSIBLE'


class DangerousGoodsAircraftCategoryType(str, Enum):
    CARGO_AIRCRAFT_ONLY='CARGO_AIRCRAFT_ONLY'
    PASSENGER_AND_CARGO_AIRCRAFT='PASSENGER_AND_CARGO_AIRCRAFT'


class DangerousGoodsContainerAttributeType(str, Enum):
    ALL_PACKED_IN_ONE='ALL_PACKED_IN_ONE'


class DangerousGoodsDescriptorType(str, Enum):
    """FEDEX INTERNAL USE ONLY: Describes the characteristics of the dangerous
    goods inferred from the commodity data."""
    ALCOHOLIC_BEVERAGE='ALCOHOLIC_BEVERAGE'
    DRY_ICE='DRY_ICE'
    EMERGENCY_CONTACT_PHONE_REQUIRED='EMERGENCY_CONTACT_PHONE_REQUIRED'
    EXCEPTED_QUANTITIES='EXCEPTED_QUANTITIES'
    INFECTIOUS_SUBSTANCE='INFECTIOUS_SUBSTANCE'
    RADIOACTIVE='RADIOACTIVE'


class DangerousGoodsHandlingUnitAttributeType(str, Enum):
    OVERPACK='OVERPACK'


class DangerousGoodsPackingGroupType(str, Enum):
    I='I'
    II='II'
    III='III'
    UNDEFINED='UNDEFINED'


class DangerousGoodsRegulationAttributeType(str, Enum):
    """This attribute type identifies characteristics of a dangerous goods
    regulation that influence how FedEx systems process dangerous goods
    shipments."""
    DRY_ICE_DECLARATION_REQUIRED='DRY_ICE_DECLARATION_REQUIRED'


class ExpressRegionCode(str, Enum):
    """Indicates a FedEx Express operating region."""
    APAC='APAC'
    CA='CA'
    EMEA='EMEA'
    LAC='LAC'
    US='US'


class HazardousCommodityOptionType(str, Enum):
    """Indicates which kind of hazardous content is being reported."""
    BATTERY='BATTERY'
    HAZARDOUS_MATERIALS='HAZARDOUS_MATERIALS'
    LIMITED_QUANTITIES_COMMODITIES='LIMITED_QUANTITIES_COMMODITIES'
    ORM_D='ORM_D'
    REPORTABLE_QUANTITIES='REPORTABLE_QUANTITIES'
    SMALL_QUANTITY_EXCEPTION='SMALL_QUANTITY_EXCEPTION'


class HazardousCommodityRegulationType(str, Enum):
    """Identifies the source of regulation for hazardous commodity data."""
    ADR='ADR'
    DOT='DOT'
    IATA='IATA'
    ORMD='ORMD'


class NetExplosiveClassificationType(str, Enum):
    NET_EXPLOSIVE_CONTENT='NET_EXPLOSIVE_CONTENT'
    NET_EXPLOSIVE_MASS='NET_EXPLOSIVE_MASS'
    NET_EXPLOSIVE_QUANTITY='NET_EXPLOSIVE_QUANTITY'
    NET_EXPLOSIVE_WEIGHT='NET_EXPLOSIVE_WEIGHT'


class NotificationSeverityType(str, Enum):
    ERROR='ERROR'
    FAILURE='FAILURE'
    NOTE='NOTE'
    SUCCESS='SUCCESS'
    WARNING='WARNING'


class PhysicalFormType(str, Enum):
    GAS='GAS'
    LIQUID='LIQUID'
    SOLID='SOLID'
    SPECIAL='SPECIAL'


class RadioactiveLabelType(str, Enum):
    III_YELLOW='III_YELLOW'
    II_YELLOW='II_YELLOW'
    I_WHITE='I_WHITE'


class RadioactivityUnitOfMeasure(str, Enum):
    BQ='BQ'
    GBQ='GBQ'
    KBQ='KBQ'
    MBQ='MBQ'
    PBQ='PBQ'
    TBQ='TBQ'


class ShipmentDryIceProcessingOptionType(str, Enum):
    SHIPMENT_LEVEL_DRY_ICE_ONLY='SHIPMENT_LEVEL_DRY_ICE_ONLY'


class TrackingIdType(str, Enum):
    EXPRESS='EXPRESS'
    FEDEX='FEDEX'
    FREIGHT='FREIGHT'
    GROUND='GROUND'
    INTERNAL='INTERNAL'
    UNKNOWN='UNKNOWN'
    USPS='USPS'


class UploadDangerousGoodsProcessingOptionType(str, Enum):
    VALIDATION_ERRORS_AS_WARNINGS='VALIDATION_ERRORS_AS_WARNINGS'


class UploadedDangerousGoodsShipmentAttributeType(str, Enum):
    MANUAL_SHIPPING_LABEL='MANUAL_SHIPPING_LABEL'


class ValidateDangerousGoodsProcessingOptionType(str, Enum):
    BYPASS_PRODUCT_VALIDATION='BYPASS_PRODUCT_VALIDATION'
    BYPASS_TRACKING_NUMBER_VALIDATION='BYPASS_TRACKING_NUMBER_VALIDATION'


class WeightUnits(str, Enum):
    KG='KG'
    LB='LB'


class AddDangerousGoodsHandlingUnitReply(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, CompletedShipmentDetail=None, CompletedHandlingUnitGroup=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.HighestSeverity = HighestSeverity
        self.validate_NotificationSeverityType(self.HighestSeverity)
        self.HighestSeverity_nsprefix_ = "ns"
        if Notifications is None:
            self.Notifications = []
        else:
            self.Notifications = Notifications
        self.Notifications_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.CompletedShipmentDetail = CompletedShipmentDetail
        self.CompletedShipmentDetail_nsprefix_ = "ns"
        self.CompletedHandlingUnitGroup = CompletedHandlingUnitGroup
        self.CompletedHandlingUnitGroup_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AddDangerousGoodsHandlingUnitReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AddDangerousGoodsHandlingUnitReply.subclass:
            return AddDangerousGoodsHandlingUnitReply.subclass(*args_, **kwargs_)
        else:
            return AddDangerousGoodsHandlingUnitReply(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_HighestSeverity(self):
        return self.HighestSeverity
    def set_HighestSeverity(self, HighestSeverity):
        self.HighestSeverity = HighestSeverity
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def add_Notifications(self, value):
        self.Notifications.append(value)
    def insert_Notifications_at(self, index, value):
        self.Notifications.insert(index, value)
    def replace_Notifications_at(self, index, value):
        self.Notifications[index] = value
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_CompletedShipmentDetail(self):
        return self.CompletedShipmentDetail
    def set_CompletedShipmentDetail(self, CompletedShipmentDetail):
        self.CompletedShipmentDetail = CompletedShipmentDetail
    def get_CompletedHandlingUnitGroup(self):
        return self.CompletedHandlingUnitGroup
    def set_CompletedHandlingUnitGroup(self, CompletedHandlingUnitGroup):
        self.CompletedHandlingUnitGroup = CompletedHandlingUnitGroup
    def validate_NotificationSeverityType(self, value):
        result = True
        # Validate type NotificationSeverityType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ERROR', 'FAILURE', 'NOTE', 'SUCCESS', 'WARNING']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on NotificationSeverityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.HighestSeverity is not None or
            self.Notifications or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.CompletedShipmentDetail is not None or
            self.CompletedHandlingUnitGroup is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddDangerousGoodsHandlingUnitReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AddDangerousGoodsHandlingUnitReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AddDangerousGoodsHandlingUnitReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AddDangerousGoodsHandlingUnitReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AddDangerousGoodsHandlingUnitReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AddDangerousGoodsHandlingUnitReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddDangerousGoodsHandlingUnitReply', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.HighestSeverity is not None:
            namespaceprefix_ = self.HighestSeverity_nsprefix_ + ':' if (UseCapturedNS_ and self.HighestSeverity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHighestSeverity>%s</%sHighestSeverity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HighestSeverity), input_name='HighestSeverity')), namespaceprefix_ , eol_))
        for Notifications_ in self.Notifications:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            Notifications_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.CompletedShipmentDetail is not None:
            namespaceprefix_ = self.CompletedShipmentDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.CompletedShipmentDetail_nsprefix_) else ''
            self.CompletedShipmentDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CompletedShipmentDetail', pretty_print=pretty_print)
        if self.CompletedHandlingUnitGroup is not None:
            namespaceprefix_ = self.CompletedHandlingUnitGroup_nsprefix_ + ':' if (UseCapturedNS_ and self.CompletedHandlingUnitGroup_nsprefix_) else ''
            self.CompletedHandlingUnitGroup.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CompletedHandlingUnitGroup', pretty_print=pretty_print)
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
        if nodeName_ == 'HighestSeverity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HighestSeverity')
            value_ = self.gds_validate_string(value_, node, 'HighestSeverity')
            self.HighestSeverity = value_
            self.HighestSeverity_nsprefix_ = child_.prefix
            # validate type NotificationSeverityType
            self.validate_NotificationSeverityType(self.HighestSeverity)
        elif nodeName_ == 'Notifications':
            obj_ = Notification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications.append(obj_)
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'CompletedShipmentDetail':
            obj_ = CompletedDangerousGoodsShipmentDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CompletedShipmentDetail = obj_
            obj_.original_tagname_ = 'CompletedShipmentDetail'
        elif nodeName_ == 'CompletedHandlingUnitGroup':
            obj_ = CompletedDangerousGoodsHandlingUnitGroup.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CompletedHandlingUnitGroup = obj_
            obj_.original_tagname_ = 'CompletedHandlingUnitGroup'
# end class AddDangerousGoodsHandlingUnitReply


class AddDangerousGoodsHandlingUnitRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, TransactionDetail=None, Version=None, UploadId=None, HandlingUnitGroup=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.WebAuthenticationDetail = WebAuthenticationDetail
        self.WebAuthenticationDetail_nsprefix_ = "ns"
        self.ClientDetail = ClientDetail
        self.ClientDetail_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.UploadId = UploadId
        self.UploadId_nsprefix_ = None
        self.HandlingUnitGroup = HandlingUnitGroup
        self.HandlingUnitGroup_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AddDangerousGoodsHandlingUnitRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AddDangerousGoodsHandlingUnitRequest.subclass:
            return AddDangerousGoodsHandlingUnitRequest.subclass(*args_, **kwargs_)
        else:
            return AddDangerousGoodsHandlingUnitRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_WebAuthenticationDetail(self):
        return self.WebAuthenticationDetail
    def set_WebAuthenticationDetail(self, WebAuthenticationDetail):
        self.WebAuthenticationDetail = WebAuthenticationDetail
    def get_ClientDetail(self):
        return self.ClientDetail
    def set_ClientDetail(self, ClientDetail):
        self.ClientDetail = ClientDetail
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_UploadId(self):
        return self.UploadId
    def set_UploadId(self, UploadId):
        self.UploadId = UploadId
    def get_HandlingUnitGroup(self):
        return self.HandlingUnitGroup
    def set_HandlingUnitGroup(self, HandlingUnitGroup):
        self.HandlingUnitGroup = HandlingUnitGroup
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.UploadId is not None or
            self.HandlingUnitGroup is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddDangerousGoodsHandlingUnitRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AddDangerousGoodsHandlingUnitRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AddDangerousGoodsHandlingUnitRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AddDangerousGoodsHandlingUnitRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AddDangerousGoodsHandlingUnitRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AddDangerousGoodsHandlingUnitRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddDangerousGoodsHandlingUnitRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.WebAuthenticationDetail is not None:
            namespaceprefix_ = self.WebAuthenticationDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.WebAuthenticationDetail_nsprefix_) else ''
            self.WebAuthenticationDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='WebAuthenticationDetail', pretty_print=pretty_print)
        if self.ClientDetail is not None:
            namespaceprefix_ = self.ClientDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientDetail_nsprefix_) else ''
            self.ClientDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClientDetail', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.UploadId is not None:
            namespaceprefix_ = self.UploadId_nsprefix_ + ':' if (UseCapturedNS_ and self.UploadId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUploadId>%s</%sUploadId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UploadId), input_name='UploadId')), namespaceprefix_ , eol_))
        if self.HandlingUnitGroup is not None:
            namespaceprefix_ = self.HandlingUnitGroup_nsprefix_ + ':' if (UseCapturedNS_ and self.HandlingUnitGroup_nsprefix_) else ''
            self.HandlingUnitGroup.export(outfile, level, namespaceprefix_, namespacedef_='', name_='HandlingUnitGroup', pretty_print=pretty_print)
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
        if nodeName_ == 'WebAuthenticationDetail':
            obj_ = WebAuthenticationDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.WebAuthenticationDetail = obj_
            obj_.original_tagname_ = 'WebAuthenticationDetail'
        elif nodeName_ == 'ClientDetail':
            obj_ = ClientDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClientDetail = obj_
            obj_.original_tagname_ = 'ClientDetail'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'UploadId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UploadId')
            value_ = self.gds_validate_string(value_, node, 'UploadId')
            self.UploadId = value_
            self.UploadId_nsprefix_ = child_.prefix
        elif nodeName_ == 'HandlingUnitGroup':
            obj_ = UploadedDangerousGoodsHandlingUnitGroup.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.HandlingUnitGroup = obj_
            obj_.original_tagname_ = 'HandlingUnitGroup'
# end class AddDangerousGoodsHandlingUnitRequest


class Address(GeneratedsSuper):
    """Descriptive data for a physical location. May be used as an actual
    physical address (place to which one could go), or as a container of
    "address parts" which should be handled as a unit (such as a city-
    state-ZIP combination within the US)."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, StreetLines=None, City=None, StateOrProvinceCode=None, PostalCode=None, UrbanizationCode=None, CountryCode=None, CountryName=None, Residential=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if StreetLines is None:
            self.StreetLines = []
        else:
            self.StreetLines = StreetLines
        self.StreetLines_nsprefix_ = None
        self.City = City
        self.City_nsprefix_ = None
        self.StateOrProvinceCode = StateOrProvinceCode
        self.StateOrProvinceCode_nsprefix_ = None
        self.PostalCode = PostalCode
        self.PostalCode_nsprefix_ = None
        self.UrbanizationCode = UrbanizationCode
        self.UrbanizationCode_nsprefix_ = None
        self.CountryCode = CountryCode
        self.CountryCode_nsprefix_ = None
        self.CountryName = CountryName
        self.CountryName_nsprefix_ = None
        self.Residential = Residential
        self.Residential_nsprefix_ = None
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
    def get_StreetLines(self):
        return self.StreetLines
    def set_StreetLines(self, StreetLines):
        self.StreetLines = StreetLines
    def add_StreetLines(self, value):
        self.StreetLines.append(value)
    def insert_StreetLines_at(self, index, value):
        self.StreetLines.insert(index, value)
    def replace_StreetLines_at(self, index, value):
        self.StreetLines[index] = value
    def get_City(self):
        return self.City
    def set_City(self, City):
        self.City = City
    def get_StateOrProvinceCode(self):
        return self.StateOrProvinceCode
    def set_StateOrProvinceCode(self, StateOrProvinceCode):
        self.StateOrProvinceCode = StateOrProvinceCode
    def get_PostalCode(self):
        return self.PostalCode
    def set_PostalCode(self, PostalCode):
        self.PostalCode = PostalCode
    def get_UrbanizationCode(self):
        return self.UrbanizationCode
    def set_UrbanizationCode(self, UrbanizationCode):
        self.UrbanizationCode = UrbanizationCode
    def get_CountryCode(self):
        return self.CountryCode
    def set_CountryCode(self, CountryCode):
        self.CountryCode = CountryCode
    def get_CountryName(self):
        return self.CountryName
    def set_CountryName(self, CountryName):
        self.CountryName = CountryName
    def get_Residential(self):
        return self.Residential
    def set_Residential(self, Residential):
        self.Residential = Residential
    def hasContent_(self):
        if (
            self.StreetLines or
            self.City is not None or
            self.StateOrProvinceCode is not None or
            self.PostalCode is not None or
            self.UrbanizationCode is not None or
            self.CountryCode is not None or
            self.CountryName is not None or
            self.Residential is not None
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
        for StreetLines_ in self.StreetLines:
            namespaceprefix_ = self.StreetLines_nsprefix_ + ':' if (UseCapturedNS_ and self.StreetLines_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStreetLines>%s</%sStreetLines>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(StreetLines_), input_name='StreetLines')), namespaceprefix_ , eol_))
        if self.City is not None:
            namespaceprefix_ = self.City_nsprefix_ + ':' if (UseCapturedNS_ and self.City_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCity>%s</%sCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.City), input_name='City')), namespaceprefix_ , eol_))
        if self.StateOrProvinceCode is not None:
            namespaceprefix_ = self.StateOrProvinceCode_nsprefix_ + ':' if (UseCapturedNS_ and self.StateOrProvinceCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStateOrProvinceCode>%s</%sStateOrProvinceCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.StateOrProvinceCode), input_name='StateOrProvinceCode')), namespaceprefix_ , eol_))
        if self.PostalCode is not None:
            namespaceprefix_ = self.PostalCode_nsprefix_ + ':' if (UseCapturedNS_ and self.PostalCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPostalCode>%s</%sPostalCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PostalCode), input_name='PostalCode')), namespaceprefix_ , eol_))
        if self.UrbanizationCode is not None:
            namespaceprefix_ = self.UrbanizationCode_nsprefix_ + ':' if (UseCapturedNS_ and self.UrbanizationCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUrbanizationCode>%s</%sUrbanizationCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UrbanizationCode), input_name='UrbanizationCode')), namespaceprefix_ , eol_))
        if self.CountryCode is not None:
            namespaceprefix_ = self.CountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryCode>%s</%sCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryCode), input_name='CountryCode')), namespaceprefix_ , eol_))
        if self.CountryName is not None:
            namespaceprefix_ = self.CountryName_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryName>%s</%sCountryName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryName), input_name='CountryName')), namespaceprefix_ , eol_))
        if self.Residential is not None:
            namespaceprefix_ = self.Residential_nsprefix_ + ':' if (UseCapturedNS_ and self.Residential_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sResidential>%s</%sResidential>%s' % (namespaceprefix_ , self.gds_format_boolean(self.Residential, input_name='Residential'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'StreetLines':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'StreetLines')
            value_ = self.gds_validate_string(value_, node, 'StreetLines')
            self.StreetLines.append(value_)
            self.StreetLines_nsprefix_ = child_.prefix
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
        elif nodeName_ == 'PostalCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PostalCode')
            value_ = self.gds_validate_string(value_, node, 'PostalCode')
            self.PostalCode = value_
            self.PostalCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'UrbanizationCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UrbanizationCode')
            value_ = self.gds_validate_string(value_, node, 'UrbanizationCode')
            self.UrbanizationCode = value_
            self.UrbanizationCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'CountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryCode')
            value_ = self.gds_validate_string(value_, node, 'CountryCode')
            self.CountryCode = value_
            self.CountryCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'CountryName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryName')
            value_ = self.gds_validate_string(value_, node, 'CountryName')
            self.CountryName = value_
            self.CountryName_nsprefix_ = child_.prefix
        elif nodeName_ == 'Residential':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'Residential')
            ival_ = self.gds_validate_boolean(ival_, node, 'Residential')
            self.Residential = ival_
            self.Residential_nsprefix_ = child_.prefix
# end class Address


class AssociatedEnterpriseDocumentDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DocumentId=None, TrackingNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DocumentId = DocumentId
        self.DocumentId_nsprefix_ = None
        self.TrackingNumber = TrackingNumber
        self.TrackingNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AssociatedEnterpriseDocumentDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AssociatedEnterpriseDocumentDetail.subclass:
            return AssociatedEnterpriseDocumentDetail.subclass(*args_, **kwargs_)
        else:
            return AssociatedEnterpriseDocumentDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DocumentId(self):
        return self.DocumentId
    def set_DocumentId(self, DocumentId):
        self.DocumentId = DocumentId
    def get_TrackingNumber(self):
        return self.TrackingNumber
    def set_TrackingNumber(self, TrackingNumber):
        self.TrackingNumber = TrackingNumber
    def hasContent_(self):
        if (
            self.DocumentId is not None or
            self.TrackingNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AssociatedEnterpriseDocumentDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AssociatedEnterpriseDocumentDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AssociatedEnterpriseDocumentDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AssociatedEnterpriseDocumentDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AssociatedEnterpriseDocumentDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AssociatedEnterpriseDocumentDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AssociatedEnterpriseDocumentDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DocumentId is not None:
            namespaceprefix_ = self.DocumentId_nsprefix_ + ':' if (UseCapturedNS_ and self.DocumentId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDocumentId>%s</%sDocumentId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DocumentId), input_name='DocumentId')), namespaceprefix_ , eol_))
        if self.TrackingNumber is not None:
            namespaceprefix_ = self.TrackingNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackingNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTrackingNumber>%s</%sTrackingNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TrackingNumber), input_name='TrackingNumber')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'DocumentId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DocumentId')
            value_ = self.gds_validate_string(value_, node, 'DocumentId')
            self.DocumentId = value_
            self.DocumentId_nsprefix_ = child_.prefix
        elif nodeName_ == 'TrackingNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TrackingNumber')
            value_ = self.gds_validate_string(value_, node, 'TrackingNumber')
            self.TrackingNumber = value_
            self.TrackingNumber_nsprefix_ = child_.prefix
# end class AssociatedEnterpriseDocumentDetail


class ClientDetail(GeneratedsSuper):
    """Descriptive data for the client submitting a transaction."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AccountNumber=None, MeterNumber=None, MeterInstance=None, IntegratorId=None, Region=None, Localization=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.AccountNumber = AccountNumber
        self.AccountNumber_nsprefix_ = None
        self.MeterNumber = MeterNumber
        self.MeterNumber_nsprefix_ = None
        self.MeterInstance = MeterInstance
        self.MeterInstance_nsprefix_ = None
        self.IntegratorId = IntegratorId
        self.IntegratorId_nsprefix_ = None
        self.Region = Region
        self.validate_ExpressRegionCode(self.Region)
        self.Region_nsprefix_ = "ns"
        self.Localization = Localization
        self.Localization_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ClientDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ClientDetail.subclass:
            return ClientDetail.subclass(*args_, **kwargs_)
        else:
            return ClientDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AccountNumber(self):
        return self.AccountNumber
    def set_AccountNumber(self, AccountNumber):
        self.AccountNumber = AccountNumber
    def get_MeterNumber(self):
        return self.MeterNumber
    def set_MeterNumber(self, MeterNumber):
        self.MeterNumber = MeterNumber
    def get_MeterInstance(self):
        return self.MeterInstance
    def set_MeterInstance(self, MeterInstance):
        self.MeterInstance = MeterInstance
    def get_IntegratorId(self):
        return self.IntegratorId
    def set_IntegratorId(self, IntegratorId):
        self.IntegratorId = IntegratorId
    def get_Region(self):
        return self.Region
    def set_Region(self, Region):
        self.Region = Region
    def get_Localization(self):
        return self.Localization
    def set_Localization(self, Localization):
        self.Localization = Localization
    def validate_ExpressRegionCode(self, value):
        result = True
        # Validate type ExpressRegionCode, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['APAC', 'CA', 'EMEA', 'LAC', 'US']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ExpressRegionCode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.AccountNumber is not None or
            self.MeterNumber is not None or
            self.MeterInstance is not None or
            self.IntegratorId is not None or
            self.Region is not None or
            self.Localization is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ClientDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ClientDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ClientDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ClientDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ClientDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ClientDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ClientDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.AccountNumber is not None:
            namespaceprefix_ = self.AccountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.AccountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccountNumber>%s</%sAccountNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AccountNumber), input_name='AccountNumber')), namespaceprefix_ , eol_))
        if self.MeterNumber is not None:
            namespaceprefix_ = self.MeterNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.MeterNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMeterNumber>%s</%sMeterNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MeterNumber), input_name='MeterNumber')), namespaceprefix_ , eol_))
        if self.MeterInstance is not None:
            namespaceprefix_ = self.MeterInstance_nsprefix_ + ':' if (UseCapturedNS_ and self.MeterInstance_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMeterInstance>%s</%sMeterInstance>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MeterInstance), input_name='MeterInstance')), namespaceprefix_ , eol_))
        if self.IntegratorId is not None:
            namespaceprefix_ = self.IntegratorId_nsprefix_ + ':' if (UseCapturedNS_ and self.IntegratorId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIntegratorId>%s</%sIntegratorId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IntegratorId), input_name='IntegratorId')), namespaceprefix_ , eol_))
        if self.Region is not None:
            namespaceprefix_ = self.Region_nsprefix_ + ':' if (UseCapturedNS_ and self.Region_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRegion>%s</%sRegion>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Region), input_name='Region')), namespaceprefix_ , eol_))
        if self.Localization is not None:
            namespaceprefix_ = self.Localization_nsprefix_ + ':' if (UseCapturedNS_ and self.Localization_nsprefix_) else ''
            self.Localization.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Localization', pretty_print=pretty_print)
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
        if nodeName_ == 'AccountNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AccountNumber')
            value_ = self.gds_validate_string(value_, node, 'AccountNumber')
            self.AccountNumber = value_
            self.AccountNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'MeterNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MeterNumber')
            value_ = self.gds_validate_string(value_, node, 'MeterNumber')
            self.MeterNumber = value_
            self.MeterNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'MeterInstance':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MeterInstance')
            value_ = self.gds_validate_string(value_, node, 'MeterInstance')
            self.MeterInstance = value_
            self.MeterInstance_nsprefix_ = child_.prefix
        elif nodeName_ == 'IntegratorId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IntegratorId')
            value_ = self.gds_validate_string(value_, node, 'IntegratorId')
            self.IntegratorId = value_
            self.IntegratorId_nsprefix_ = child_.prefix
        elif nodeName_ == 'Region':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Region')
            value_ = self.gds_validate_string(value_, node, 'Region')
            self.Region = value_
            self.Region_nsprefix_ = child_.prefix
            # validate type ExpressRegionCode
            self.validate_ExpressRegionCode(self.Region)
        elif nodeName_ == 'Localization':
            obj_ = Localization.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Localization = obj_
            obj_.original_tagname_ = 'Localization'
# end class ClientDetail


class CompletedDangerousGoodsHandlingUnitGroup(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Id=None, NumberOfHandlingUnits=None, HandlingUnitShippingDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Id = Id
        self.Id_nsprefix_ = None
        self.NumberOfHandlingUnits = NumberOfHandlingUnits
        self.NumberOfHandlingUnits_nsprefix_ = None
        self.HandlingUnitShippingDetail = HandlingUnitShippingDetail
        self.HandlingUnitShippingDetail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CompletedDangerousGoodsHandlingUnitGroup)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CompletedDangerousGoodsHandlingUnitGroup.subclass:
            return CompletedDangerousGoodsHandlingUnitGroup.subclass(*args_, **kwargs_)
        else:
            return CompletedDangerousGoodsHandlingUnitGroup(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def get_NumberOfHandlingUnits(self):
        return self.NumberOfHandlingUnits
    def set_NumberOfHandlingUnits(self, NumberOfHandlingUnits):
        self.NumberOfHandlingUnits = NumberOfHandlingUnits
    def get_HandlingUnitShippingDetail(self):
        return self.HandlingUnitShippingDetail
    def set_HandlingUnitShippingDetail(self, HandlingUnitShippingDetail):
        self.HandlingUnitShippingDetail = HandlingUnitShippingDetail
    def hasContent_(self):
        if (
            self.Id is not None or
            self.NumberOfHandlingUnits is not None or
            self.HandlingUnitShippingDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CompletedDangerousGoodsHandlingUnitGroup', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CompletedDangerousGoodsHandlingUnitGroup')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CompletedDangerousGoodsHandlingUnitGroup':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CompletedDangerousGoodsHandlingUnitGroup')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CompletedDangerousGoodsHandlingUnitGroup', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CompletedDangerousGoodsHandlingUnitGroup'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CompletedDangerousGoodsHandlingUnitGroup', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Id is not None:
            namespaceprefix_ = self.Id_nsprefix_ + ':' if (UseCapturedNS_ and self.Id_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sId>%s</%sId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Id), input_name='Id')), namespaceprefix_ , eol_))
        if self.NumberOfHandlingUnits is not None:
            namespaceprefix_ = self.NumberOfHandlingUnits_nsprefix_ + ':' if (UseCapturedNS_ and self.NumberOfHandlingUnits_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumberOfHandlingUnits>%s</%sNumberOfHandlingUnits>%s' % (namespaceprefix_ , self.gds_format_integer(self.NumberOfHandlingUnits, input_name='NumberOfHandlingUnits'), namespaceprefix_ , eol_))
        if self.HandlingUnitShippingDetail is not None:
            namespaceprefix_ = self.HandlingUnitShippingDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.HandlingUnitShippingDetail_nsprefix_) else ''
            self.HandlingUnitShippingDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='HandlingUnitShippingDetail', pretty_print=pretty_print)
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
        if nodeName_ == 'Id':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Id')
            value_ = self.gds_validate_string(value_, node, 'Id')
            self.Id = value_
            self.Id_nsprefix_ = child_.prefix
        elif nodeName_ == 'NumberOfHandlingUnits' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'NumberOfHandlingUnits')
            if ival_ < 0:
                raise_parse_error(child_, 'requires nonNegativeInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'NumberOfHandlingUnits')
            self.NumberOfHandlingUnits = ival_
            self.NumberOfHandlingUnits_nsprefix_ = child_.prefix
        elif nodeName_ == 'HandlingUnitShippingDetail':
            obj_ = DangerousGoodsHandlingUnitShippingDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.HandlingUnitShippingDetail = obj_
            obj_.original_tagname_ = 'HandlingUnitShippingDetail'
# end class CompletedDangerousGoodsHandlingUnitGroup


class CompletedDangerousGoodsShipmentDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Regulation=None, RegulationAttributes=None, TotalHandlingUnitCount=None, AircraftCategoryType=None, DangerousGoodsDescriptors=None, Accessibility=None, Options=None, ShipmentDryIceDetail=None, ExpirationDate=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Regulation = Regulation
        self.validate_HazardousCommodityRegulationType(self.Regulation)
        self.Regulation_nsprefix_ = "ns"
        if RegulationAttributes is None:
            self.RegulationAttributes = []
        else:
            self.RegulationAttributes = RegulationAttributes
        self.RegulationAttributes_nsprefix_ = "ns"
        self.TotalHandlingUnitCount = TotalHandlingUnitCount
        self.TotalHandlingUnitCount_nsprefix_ = None
        self.AircraftCategoryType = AircraftCategoryType
        self.validate_DangerousGoodsAircraftCategoryType(self.AircraftCategoryType)
        self.AircraftCategoryType_nsprefix_ = "ns"
        if DangerousGoodsDescriptors is None:
            self.DangerousGoodsDescriptors = []
        else:
            self.DangerousGoodsDescriptors = DangerousGoodsDescriptors
        self.DangerousGoodsDescriptors_nsprefix_ = "ns"
        self.Accessibility = Accessibility
        self.validate_DangerousGoodsAccessibilityType(self.Accessibility)
        self.Accessibility_nsprefix_ = "ns"
        if Options is None:
            self.Options = []
        else:
            self.Options = Options
        self.Options_nsprefix_ = "ns"
        self.ShipmentDryIceDetail = ShipmentDryIceDetail
        self.ShipmentDryIceDetail_nsprefix_ = "ns"
        if isinstance(ExpirationDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ExpirationDate, '%Y-%m-%d').date()
        else:
            initvalue_ = ExpirationDate
        self.ExpirationDate = initvalue_
        self.ExpirationDate_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CompletedDangerousGoodsShipmentDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CompletedDangerousGoodsShipmentDetail.subclass:
            return CompletedDangerousGoodsShipmentDetail.subclass(*args_, **kwargs_)
        else:
            return CompletedDangerousGoodsShipmentDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Regulation(self):
        return self.Regulation
    def set_Regulation(self, Regulation):
        self.Regulation = Regulation
    def get_RegulationAttributes(self):
        return self.RegulationAttributes
    def set_RegulationAttributes(self, RegulationAttributes):
        self.RegulationAttributes = RegulationAttributes
    def add_RegulationAttributes(self, value):
        self.RegulationAttributes.append(value)
    def insert_RegulationAttributes_at(self, index, value):
        self.RegulationAttributes.insert(index, value)
    def replace_RegulationAttributes_at(self, index, value):
        self.RegulationAttributes[index] = value
    def get_TotalHandlingUnitCount(self):
        return self.TotalHandlingUnitCount
    def set_TotalHandlingUnitCount(self, TotalHandlingUnitCount):
        self.TotalHandlingUnitCount = TotalHandlingUnitCount
    def get_AircraftCategoryType(self):
        return self.AircraftCategoryType
    def set_AircraftCategoryType(self, AircraftCategoryType):
        self.AircraftCategoryType = AircraftCategoryType
    def get_DangerousGoodsDescriptors(self):
        return self.DangerousGoodsDescriptors
    def set_DangerousGoodsDescriptors(self, DangerousGoodsDescriptors):
        self.DangerousGoodsDescriptors = DangerousGoodsDescriptors
    def add_DangerousGoodsDescriptors(self, value):
        self.DangerousGoodsDescriptors.append(value)
    def insert_DangerousGoodsDescriptors_at(self, index, value):
        self.DangerousGoodsDescriptors.insert(index, value)
    def replace_DangerousGoodsDescriptors_at(self, index, value):
        self.DangerousGoodsDescriptors[index] = value
    def get_Accessibility(self):
        return self.Accessibility
    def set_Accessibility(self, Accessibility):
        self.Accessibility = Accessibility
    def get_Options(self):
        return self.Options
    def set_Options(self, Options):
        self.Options = Options
    def add_Options(self, value):
        self.Options.append(value)
    def insert_Options_at(self, index, value):
        self.Options.insert(index, value)
    def replace_Options_at(self, index, value):
        self.Options[index] = value
    def get_ShipmentDryIceDetail(self):
        return self.ShipmentDryIceDetail
    def set_ShipmentDryIceDetail(self, ShipmentDryIceDetail):
        self.ShipmentDryIceDetail = ShipmentDryIceDetail
    def get_ExpirationDate(self):
        return self.ExpirationDate
    def set_ExpirationDate(self, ExpirationDate):
        self.ExpirationDate = ExpirationDate
    def validate_HazardousCommodityRegulationType(self, value):
        result = True
        # Validate type HazardousCommodityRegulationType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ADR', 'DOT', 'IATA', 'ORMD']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on HazardousCommodityRegulationType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DangerousGoodsRegulationAttributeType(self, value):
        result = True
        # Validate type DangerousGoodsRegulationAttributeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['DRY_ICE_DECLARATION_REQUIRED']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DangerousGoodsRegulationAttributeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DangerousGoodsAircraftCategoryType(self, value):
        result = True
        # Validate type DangerousGoodsAircraftCategoryType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['CARGO_AIRCRAFT_ONLY', 'PASSENGER_AND_CARGO_AIRCRAFT']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DangerousGoodsAircraftCategoryType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DangerousGoodsDescriptorType(self, value):
        result = True
        # Validate type DangerousGoodsDescriptorType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ALCOHOLIC_BEVERAGE', 'DRY_ICE', 'EMERGENCY_CONTACT_PHONE_REQUIRED', 'EXCEPTED_QUANTITIES', 'INFECTIOUS_SUBSTANCE', 'RADIOACTIVE']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DangerousGoodsDescriptorType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DangerousGoodsAccessibilityType(self, value):
        result = True
        # Validate type DangerousGoodsAccessibilityType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ACCESSIBLE', 'INACCESSIBLE']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DangerousGoodsAccessibilityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_HazardousCommodityOptionType(self, value):
        result = True
        # Validate type HazardousCommodityOptionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['BATTERY', 'HAZARDOUS_MATERIALS', 'LIMITED_QUANTITIES_COMMODITIES', 'ORM_D', 'REPORTABLE_QUANTITIES', 'SMALL_QUANTITY_EXCEPTION']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on HazardousCommodityOptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Regulation is not None or
            self.RegulationAttributes or
            self.TotalHandlingUnitCount is not None or
            self.AircraftCategoryType is not None or
            self.DangerousGoodsDescriptors or
            self.Accessibility is not None or
            self.Options or
            self.ShipmentDryIceDetail is not None or
            self.ExpirationDate is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CompletedDangerousGoodsShipmentDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CompletedDangerousGoodsShipmentDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CompletedDangerousGoodsShipmentDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CompletedDangerousGoodsShipmentDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CompletedDangerousGoodsShipmentDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CompletedDangerousGoodsShipmentDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CompletedDangerousGoodsShipmentDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Regulation is not None:
            namespaceprefix_ = self.Regulation_nsprefix_ + ':' if (UseCapturedNS_ and self.Regulation_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRegulation>%s</%sRegulation>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Regulation), input_name='Regulation')), namespaceprefix_ , eol_))
        for RegulationAttributes_ in self.RegulationAttributes:
            namespaceprefix_ = self.RegulationAttributes_nsprefix_ + ':' if (UseCapturedNS_ and self.RegulationAttributes_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRegulationAttributes>%s</%sRegulationAttributes>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(RegulationAttributes_), input_name='RegulationAttributes')), namespaceprefix_ , eol_))
        if self.TotalHandlingUnitCount is not None:
            namespaceprefix_ = self.TotalHandlingUnitCount_nsprefix_ + ':' if (UseCapturedNS_ and self.TotalHandlingUnitCount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTotalHandlingUnitCount>%s</%sTotalHandlingUnitCount>%s' % (namespaceprefix_ , self.gds_format_integer(self.TotalHandlingUnitCount, input_name='TotalHandlingUnitCount'), namespaceprefix_ , eol_))
        if self.AircraftCategoryType is not None:
            namespaceprefix_ = self.AircraftCategoryType_nsprefix_ + ':' if (UseCapturedNS_ and self.AircraftCategoryType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAircraftCategoryType>%s</%sAircraftCategoryType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AircraftCategoryType), input_name='AircraftCategoryType')), namespaceprefix_ , eol_))
        for DangerousGoodsDescriptors_ in self.DangerousGoodsDescriptors:
            namespaceprefix_ = self.DangerousGoodsDescriptors_nsprefix_ + ':' if (UseCapturedNS_ and self.DangerousGoodsDescriptors_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDangerousGoodsDescriptors>%s</%sDangerousGoodsDescriptors>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(DangerousGoodsDescriptors_), input_name='DangerousGoodsDescriptors')), namespaceprefix_ , eol_))
        if self.Accessibility is not None:
            namespaceprefix_ = self.Accessibility_nsprefix_ + ':' if (UseCapturedNS_ and self.Accessibility_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccessibility>%s</%sAccessibility>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Accessibility), input_name='Accessibility')), namespaceprefix_ , eol_))
        for Options_ in self.Options:
            namespaceprefix_ = self.Options_nsprefix_ + ':' if (UseCapturedNS_ and self.Options_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOptions>%s</%sOptions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Options_), input_name='Options')), namespaceprefix_ , eol_))
        if self.ShipmentDryIceDetail is not None:
            namespaceprefix_ = self.ShipmentDryIceDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentDryIceDetail_nsprefix_) else ''
            self.ShipmentDryIceDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentDryIceDetail', pretty_print=pretty_print)
        if self.ExpirationDate is not None:
            namespaceprefix_ = self.ExpirationDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ExpirationDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExpirationDate>%s</%sExpirationDate>%s' % (namespaceprefix_ , self.gds_format_date(self.ExpirationDate, input_name='ExpirationDate'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Regulation':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Regulation')
            value_ = self.gds_validate_string(value_, node, 'Regulation')
            self.Regulation = value_
            self.Regulation_nsprefix_ = child_.prefix
            # validate type HazardousCommodityRegulationType
            self.validate_HazardousCommodityRegulationType(self.Regulation)
        elif nodeName_ == 'RegulationAttributes':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RegulationAttributes')
            value_ = self.gds_validate_string(value_, node, 'RegulationAttributes')
            self.RegulationAttributes.append(value_)
            self.RegulationAttributes_nsprefix_ = child_.prefix
            # validate type DangerousGoodsRegulationAttributeType
            self.validate_DangerousGoodsRegulationAttributeType(self.RegulationAttributes[-1])
        elif nodeName_ == 'TotalHandlingUnitCount' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'TotalHandlingUnitCount')
            if ival_ < 0:
                raise_parse_error(child_, 'requires nonNegativeInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'TotalHandlingUnitCount')
            self.TotalHandlingUnitCount = ival_
            self.TotalHandlingUnitCount_nsprefix_ = child_.prefix
        elif nodeName_ == 'AircraftCategoryType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AircraftCategoryType')
            value_ = self.gds_validate_string(value_, node, 'AircraftCategoryType')
            self.AircraftCategoryType = value_
            self.AircraftCategoryType_nsprefix_ = child_.prefix
            # validate type DangerousGoodsAircraftCategoryType
            self.validate_DangerousGoodsAircraftCategoryType(self.AircraftCategoryType)
        elif nodeName_ == 'DangerousGoodsDescriptors':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DangerousGoodsDescriptors')
            value_ = self.gds_validate_string(value_, node, 'DangerousGoodsDescriptors')
            self.DangerousGoodsDescriptors.append(value_)
            self.DangerousGoodsDescriptors_nsprefix_ = child_.prefix
            # validate type DangerousGoodsDescriptorType
            self.validate_DangerousGoodsDescriptorType(self.DangerousGoodsDescriptors[-1])
        elif nodeName_ == 'Accessibility':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Accessibility')
            value_ = self.gds_validate_string(value_, node, 'Accessibility')
            self.Accessibility = value_
            self.Accessibility_nsprefix_ = child_.prefix
            # validate type DangerousGoodsAccessibilityType
            self.validate_DangerousGoodsAccessibilityType(self.Accessibility)
        elif nodeName_ == 'Options':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Options')
            value_ = self.gds_validate_string(value_, node, 'Options')
            self.Options.append(value_)
            self.Options_nsprefix_ = child_.prefix
            # validate type HazardousCommodityOptionType
            self.validate_HazardousCommodityOptionType(self.Options[-1])
        elif nodeName_ == 'ShipmentDryIceDetail':
            obj_ = ShipmentDryIceDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentDryIceDetail = obj_
            obj_.original_tagname_ = 'ShipmentDryIceDetail'
        elif nodeName_ == 'ExpirationDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.ExpirationDate = dval_
            self.ExpirationDate_nsprefix_ = child_.prefix
# end class CompletedDangerousGoodsShipmentDetail


class Contact(GeneratedsSuper):
    """The descriptive data for a point-of-contact person."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ContactId=None, PersonName=None, Title=None, CompanyName=None, PhoneNumber=None, PhoneExtension=None, TollFreePhoneNumber=None, PagerNumber=None, FaxNumber=None, EMailAddress=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ContactId = ContactId
        self.ContactId_nsprefix_ = None
        self.PersonName = PersonName
        self.PersonName_nsprefix_ = None
        self.Title = Title
        self.Title_nsprefix_ = None
        self.CompanyName = CompanyName
        self.CompanyName_nsprefix_ = None
        self.PhoneNumber = PhoneNumber
        self.PhoneNumber_nsprefix_ = None
        self.PhoneExtension = PhoneExtension
        self.PhoneExtension_nsprefix_ = None
        self.TollFreePhoneNumber = TollFreePhoneNumber
        self.TollFreePhoneNumber_nsprefix_ = None
        self.PagerNumber = PagerNumber
        self.PagerNumber_nsprefix_ = None
        self.FaxNumber = FaxNumber
        self.FaxNumber_nsprefix_ = None
        self.EMailAddress = EMailAddress
        self.EMailAddress_nsprefix_ = None
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
    def get_ContactId(self):
        return self.ContactId
    def set_ContactId(self, ContactId):
        self.ContactId = ContactId
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
    def get_PhoneNumber(self):
        return self.PhoneNumber
    def set_PhoneNumber(self, PhoneNumber):
        self.PhoneNumber = PhoneNumber
    def get_PhoneExtension(self):
        return self.PhoneExtension
    def set_PhoneExtension(self, PhoneExtension):
        self.PhoneExtension = PhoneExtension
    def get_TollFreePhoneNumber(self):
        return self.TollFreePhoneNumber
    def set_TollFreePhoneNumber(self, TollFreePhoneNumber):
        self.TollFreePhoneNumber = TollFreePhoneNumber
    def get_PagerNumber(self):
        return self.PagerNumber
    def set_PagerNumber(self, PagerNumber):
        self.PagerNumber = PagerNumber
    def get_FaxNumber(self):
        return self.FaxNumber
    def set_FaxNumber(self, FaxNumber):
        self.FaxNumber = FaxNumber
    def get_EMailAddress(self):
        return self.EMailAddress
    def set_EMailAddress(self, EMailAddress):
        self.EMailAddress = EMailAddress
    def hasContent_(self):
        if (
            self.ContactId is not None or
            self.PersonName is not None or
            self.Title is not None or
            self.CompanyName is not None or
            self.PhoneNumber is not None or
            self.PhoneExtension is not None or
            self.TollFreePhoneNumber is not None or
            self.PagerNumber is not None or
            self.FaxNumber is not None or
            self.EMailAddress is not None
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
        if self.ContactId is not None:
            namespaceprefix_ = self.ContactId_nsprefix_ + ':' if (UseCapturedNS_ and self.ContactId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sContactId>%s</%sContactId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ContactId), input_name='ContactId')), namespaceprefix_ , eol_))
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
        if self.PhoneNumber is not None:
            namespaceprefix_ = self.PhoneNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.PhoneNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPhoneNumber>%s</%sPhoneNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PhoneNumber), input_name='PhoneNumber')), namespaceprefix_ , eol_))
        if self.PhoneExtension is not None:
            namespaceprefix_ = self.PhoneExtension_nsprefix_ + ':' if (UseCapturedNS_ and self.PhoneExtension_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPhoneExtension>%s</%sPhoneExtension>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PhoneExtension), input_name='PhoneExtension')), namespaceprefix_ , eol_))
        if self.TollFreePhoneNumber is not None:
            namespaceprefix_ = self.TollFreePhoneNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.TollFreePhoneNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTollFreePhoneNumber>%s</%sTollFreePhoneNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TollFreePhoneNumber), input_name='TollFreePhoneNumber')), namespaceprefix_ , eol_))
        if self.PagerNumber is not None:
            namespaceprefix_ = self.PagerNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.PagerNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPagerNumber>%s</%sPagerNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PagerNumber), input_name='PagerNumber')), namespaceprefix_ , eol_))
        if self.FaxNumber is not None:
            namespaceprefix_ = self.FaxNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.FaxNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFaxNumber>%s</%sFaxNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FaxNumber), input_name='FaxNumber')), namespaceprefix_ , eol_))
        if self.EMailAddress is not None:
            namespaceprefix_ = self.EMailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.EMailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEMailAddress>%s</%sEMailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EMailAddress), input_name='EMailAddress')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ContactId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ContactId')
            value_ = self.gds_validate_string(value_, node, 'ContactId')
            self.ContactId = value_
            self.ContactId_nsprefix_ = child_.prefix
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
        elif nodeName_ == 'PhoneNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PhoneNumber')
            value_ = self.gds_validate_string(value_, node, 'PhoneNumber')
            self.PhoneNumber = value_
            self.PhoneNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'PhoneExtension':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PhoneExtension')
            value_ = self.gds_validate_string(value_, node, 'PhoneExtension')
            self.PhoneExtension = value_
            self.PhoneExtension_nsprefix_ = child_.prefix
        elif nodeName_ == 'TollFreePhoneNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TollFreePhoneNumber')
            value_ = self.gds_validate_string(value_, node, 'TollFreePhoneNumber')
            self.TollFreePhoneNumber = value_
            self.TollFreePhoneNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'PagerNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PagerNumber')
            value_ = self.gds_validate_string(value_, node, 'PagerNumber')
            self.PagerNumber = value_
            self.PagerNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'FaxNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FaxNumber')
            value_ = self.gds_validate_string(value_, node, 'FaxNumber')
            self.FaxNumber = value_
            self.FaxNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'EMailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EMailAddress')
            value_ = self.gds_validate_string(value_, node, 'EMailAddress')
            self.EMailAddress = value_
            self.EMailAddress_nsprefix_ = child_.prefix
# end class Contact


class DangerousGoodsHandlingUnitShippingDetail(GeneratedsSuper):
    """This provides the information needed for shipping, rating, validation,
    and label generation."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TrackingNumberUnits=None, Description=None, AircraftCategoryType=None, DangerousGoodsDescriptors=None, Accessibility=None, Options=None, DryIceWeight=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if TrackingNumberUnits is None:
            self.TrackingNumberUnits = []
        else:
            self.TrackingNumberUnits = TrackingNumberUnits
        self.TrackingNumberUnits_nsprefix_ = "ns"
        self.Description = Description
        self.Description_nsprefix_ = None
        self.AircraftCategoryType = AircraftCategoryType
        self.validate_DangerousGoodsAircraftCategoryType(self.AircraftCategoryType)
        self.AircraftCategoryType_nsprefix_ = "ns"
        if DangerousGoodsDescriptors is None:
            self.DangerousGoodsDescriptors = []
        else:
            self.DangerousGoodsDescriptors = DangerousGoodsDescriptors
        self.DangerousGoodsDescriptors_nsprefix_ = "ns"
        self.Accessibility = Accessibility
        self.validate_DangerousGoodsAccessibilityType(self.Accessibility)
        self.Accessibility_nsprefix_ = "ns"
        if Options is None:
            self.Options = []
        else:
            self.Options = Options
        self.Options_nsprefix_ = "ns"
        self.DryIceWeight = DryIceWeight
        self.DryIceWeight_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DangerousGoodsHandlingUnitShippingDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DangerousGoodsHandlingUnitShippingDetail.subclass:
            return DangerousGoodsHandlingUnitShippingDetail.subclass(*args_, **kwargs_)
        else:
            return DangerousGoodsHandlingUnitShippingDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_TrackingNumberUnits(self):
        return self.TrackingNumberUnits
    def set_TrackingNumberUnits(self, TrackingNumberUnits):
        self.TrackingNumberUnits = TrackingNumberUnits
    def add_TrackingNumberUnits(self, value):
        self.TrackingNumberUnits.append(value)
    def insert_TrackingNumberUnits_at(self, index, value):
        self.TrackingNumberUnits.insert(index, value)
    def replace_TrackingNumberUnits_at(self, index, value):
        self.TrackingNumberUnits[index] = value
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def get_AircraftCategoryType(self):
        return self.AircraftCategoryType
    def set_AircraftCategoryType(self, AircraftCategoryType):
        self.AircraftCategoryType = AircraftCategoryType
    def get_DangerousGoodsDescriptors(self):
        return self.DangerousGoodsDescriptors
    def set_DangerousGoodsDescriptors(self, DangerousGoodsDescriptors):
        self.DangerousGoodsDescriptors = DangerousGoodsDescriptors
    def add_DangerousGoodsDescriptors(self, value):
        self.DangerousGoodsDescriptors.append(value)
    def insert_DangerousGoodsDescriptors_at(self, index, value):
        self.DangerousGoodsDescriptors.insert(index, value)
    def replace_DangerousGoodsDescriptors_at(self, index, value):
        self.DangerousGoodsDescriptors[index] = value
    def get_Accessibility(self):
        return self.Accessibility
    def set_Accessibility(self, Accessibility):
        self.Accessibility = Accessibility
    def get_Options(self):
        return self.Options
    def set_Options(self, Options):
        self.Options = Options
    def add_Options(self, value):
        self.Options.append(value)
    def insert_Options_at(self, index, value):
        self.Options.insert(index, value)
    def replace_Options_at(self, index, value):
        self.Options[index] = value
    def get_DryIceWeight(self):
        return self.DryIceWeight
    def set_DryIceWeight(self, DryIceWeight):
        self.DryIceWeight = DryIceWeight
    def validate_DangerousGoodsAircraftCategoryType(self, value):
        result = True
        # Validate type DangerousGoodsAircraftCategoryType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['CARGO_AIRCRAFT_ONLY', 'PASSENGER_AND_CARGO_AIRCRAFT']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DangerousGoodsAircraftCategoryType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DangerousGoodsDescriptorType(self, value):
        result = True
        # Validate type DangerousGoodsDescriptorType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ALCOHOLIC_BEVERAGE', 'DRY_ICE', 'EMERGENCY_CONTACT_PHONE_REQUIRED', 'EXCEPTED_QUANTITIES', 'INFECTIOUS_SUBSTANCE', 'RADIOACTIVE']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DangerousGoodsDescriptorType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DangerousGoodsAccessibilityType(self, value):
        result = True
        # Validate type DangerousGoodsAccessibilityType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ACCESSIBLE', 'INACCESSIBLE']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DangerousGoodsAccessibilityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_HazardousCommodityOptionType(self, value):
        result = True
        # Validate type HazardousCommodityOptionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['BATTERY', 'HAZARDOUS_MATERIALS', 'LIMITED_QUANTITIES_COMMODITIES', 'ORM_D', 'REPORTABLE_QUANTITIES', 'SMALL_QUANTITY_EXCEPTION']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on HazardousCommodityOptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.TrackingNumberUnits or
            self.Description is not None or
            self.AircraftCategoryType is not None or
            self.DangerousGoodsDescriptors or
            self.Accessibility is not None or
            self.Options or
            self.DryIceWeight is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DangerousGoodsHandlingUnitShippingDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DangerousGoodsHandlingUnitShippingDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DangerousGoodsHandlingUnitShippingDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DangerousGoodsHandlingUnitShippingDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DangerousGoodsHandlingUnitShippingDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DangerousGoodsHandlingUnitShippingDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DangerousGoodsHandlingUnitShippingDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for TrackingNumberUnits_ in self.TrackingNumberUnits:
            namespaceprefix_ = self.TrackingNumberUnits_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackingNumberUnits_nsprefix_) else ''
            TrackingNumberUnits_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TrackingNumberUnits', pretty_print=pretty_print)
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
        if self.AircraftCategoryType is not None:
            namespaceprefix_ = self.AircraftCategoryType_nsprefix_ + ':' if (UseCapturedNS_ and self.AircraftCategoryType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAircraftCategoryType>%s</%sAircraftCategoryType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AircraftCategoryType), input_name='AircraftCategoryType')), namespaceprefix_ , eol_))
        for DangerousGoodsDescriptors_ in self.DangerousGoodsDescriptors:
            namespaceprefix_ = self.DangerousGoodsDescriptors_nsprefix_ + ':' if (UseCapturedNS_ and self.DangerousGoodsDescriptors_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDangerousGoodsDescriptors>%s</%sDangerousGoodsDescriptors>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(DangerousGoodsDescriptors_), input_name='DangerousGoodsDescriptors')), namespaceprefix_ , eol_))
        if self.Accessibility is not None:
            namespaceprefix_ = self.Accessibility_nsprefix_ + ':' if (UseCapturedNS_ and self.Accessibility_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccessibility>%s</%sAccessibility>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Accessibility), input_name='Accessibility')), namespaceprefix_ , eol_))
        for Options_ in self.Options:
            namespaceprefix_ = self.Options_nsprefix_ + ':' if (UseCapturedNS_ and self.Options_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOptions>%s</%sOptions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Options_), input_name='Options')), namespaceprefix_ , eol_))
        if self.DryIceWeight is not None:
            namespaceprefix_ = self.DryIceWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.DryIceWeight_nsprefix_) else ''
            self.DryIceWeight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DryIceWeight', pretty_print=pretty_print)
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
        if nodeName_ == 'TrackingNumberUnits':
            obj_ = TrackingNumberUnit.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TrackingNumberUnits.append(obj_)
            obj_.original_tagname_ = 'TrackingNumberUnits'
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
        elif nodeName_ == 'AircraftCategoryType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AircraftCategoryType')
            value_ = self.gds_validate_string(value_, node, 'AircraftCategoryType')
            self.AircraftCategoryType = value_
            self.AircraftCategoryType_nsprefix_ = child_.prefix
            # validate type DangerousGoodsAircraftCategoryType
            self.validate_DangerousGoodsAircraftCategoryType(self.AircraftCategoryType)
        elif nodeName_ == 'DangerousGoodsDescriptors':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DangerousGoodsDescriptors')
            value_ = self.gds_validate_string(value_, node, 'DangerousGoodsDescriptors')
            self.DangerousGoodsDescriptors.append(value_)
            self.DangerousGoodsDescriptors_nsprefix_ = child_.prefix
            # validate type DangerousGoodsDescriptorType
            self.validate_DangerousGoodsDescriptorType(self.DangerousGoodsDescriptors[-1])
        elif nodeName_ == 'Accessibility':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Accessibility')
            value_ = self.gds_validate_string(value_, node, 'Accessibility')
            self.Accessibility = value_
            self.Accessibility_nsprefix_ = child_.prefix
            # validate type DangerousGoodsAccessibilityType
            self.validate_DangerousGoodsAccessibilityType(self.Accessibility)
        elif nodeName_ == 'Options':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Options')
            value_ = self.gds_validate_string(value_, node, 'Options')
            self.Options.append(value_)
            self.Options_nsprefix_ = child_.prefix
            # validate type HazardousCommodityOptionType
            self.validate_HazardousCommodityOptionType(self.Options[-1])
        elif nodeName_ == 'DryIceWeight':
            obj_ = Weight.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DryIceWeight = obj_
            obj_.original_tagname_ = 'DryIceWeight'
# end class DangerousGoodsHandlingUnitShippingDetail


class DangerousGoodsInnerReceptacleDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Quantity=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Quantity = Quantity
        self.Quantity_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DangerousGoodsInnerReceptacleDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DangerousGoodsInnerReceptacleDetail.subclass:
            return DangerousGoodsInnerReceptacleDetail.subclass(*args_, **kwargs_)
        else:
            return DangerousGoodsInnerReceptacleDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Quantity(self):
        return self.Quantity
    def set_Quantity(self, Quantity):
        self.Quantity = Quantity
    def hasContent_(self):
        if (
            self.Quantity is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DangerousGoodsInnerReceptacleDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DangerousGoodsInnerReceptacleDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DangerousGoodsInnerReceptacleDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DangerousGoodsInnerReceptacleDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DangerousGoodsInnerReceptacleDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DangerousGoodsInnerReceptacleDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DangerousGoodsInnerReceptacleDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Quantity is not None:
            namespaceprefix_ = self.Quantity_nsprefix_ + ':' if (UseCapturedNS_ and self.Quantity_nsprefix_) else ''
            self.Quantity.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Quantity', pretty_print=pretty_print)
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
        if nodeName_ == 'Quantity':
            obj_ = PreciseQuantity.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Quantity = obj_
            obj_.original_tagname_ = 'Quantity'
# end class DangerousGoodsInnerReceptacleDetail


class DangerousGoodsRadionuclideActivity(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Value=None, UnitOfMeasure=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Value = Value
        self.Value_nsprefix_ = None
        self.UnitOfMeasure = UnitOfMeasure
        self.validate_RadioactivityUnitOfMeasure(self.UnitOfMeasure)
        self.UnitOfMeasure_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DangerousGoodsRadionuclideActivity)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DangerousGoodsRadionuclideActivity.subclass:
            return DangerousGoodsRadionuclideActivity.subclass(*args_, **kwargs_)
        else:
            return DangerousGoodsRadionuclideActivity(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def get_UnitOfMeasure(self):
        return self.UnitOfMeasure
    def set_UnitOfMeasure(self, UnitOfMeasure):
        self.UnitOfMeasure = UnitOfMeasure
    def validate_RadioactivityUnitOfMeasure(self, value):
        result = True
        # Validate type RadioactivityUnitOfMeasure, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['BQ', 'GBQ', 'KBQ', 'MBQ', 'PBQ', 'TBQ']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on RadioactivityUnitOfMeasure' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Value is not None or
            self.UnitOfMeasure is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DangerousGoodsRadionuclideActivity', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DangerousGoodsRadionuclideActivity')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DangerousGoodsRadionuclideActivity':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DangerousGoodsRadionuclideActivity')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DangerousGoodsRadionuclideActivity', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DangerousGoodsRadionuclideActivity'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DangerousGoodsRadionuclideActivity', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Value is not None:
            namespaceprefix_ = self.Value_nsprefix_ + ':' if (UseCapturedNS_ and self.Value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sValue>%s</%sValue>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Value, input_name='Value'), namespaceprefix_ , eol_))
        if self.UnitOfMeasure is not None:
            namespaceprefix_ = self.UnitOfMeasure_nsprefix_ + ':' if (UseCapturedNS_ and self.UnitOfMeasure_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUnitOfMeasure>%s</%sUnitOfMeasure>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UnitOfMeasure), input_name='UnitOfMeasure')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Value' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Value')
            fval_ = self.gds_validate_decimal(fval_, node, 'Value')
            self.Value = fval_
            self.Value_nsprefix_ = child_.prefix
        elif nodeName_ == 'UnitOfMeasure':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UnitOfMeasure')
            value_ = self.gds_validate_string(value_, node, 'UnitOfMeasure')
            self.UnitOfMeasure = value_
            self.UnitOfMeasure_nsprefix_ = child_.prefix
            # validate type RadioactivityUnitOfMeasure
            self.validate_RadioactivityUnitOfMeasure(self.UnitOfMeasure)
# end class DangerousGoodsRadionuclideActivity


class DangerousGoodsRadionuclideDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Radionuclides=None, Activity=None, PhysicalForm=None, ChemicalForm=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Radionuclides is None:
            self.Radionuclides = []
        else:
            self.Radionuclides = Radionuclides
        self.Radionuclides_nsprefix_ = None
        self.Activity = Activity
        self.Activity_nsprefix_ = "ns"
        self.PhysicalForm = PhysicalForm
        self.validate_PhysicalFormType(self.PhysicalForm)
        self.PhysicalForm_nsprefix_ = "ns"
        self.ChemicalForm = ChemicalForm
        self.ChemicalForm_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DangerousGoodsRadionuclideDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DangerousGoodsRadionuclideDetail.subclass:
            return DangerousGoodsRadionuclideDetail.subclass(*args_, **kwargs_)
        else:
            return DangerousGoodsRadionuclideDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Radionuclides(self):
        return self.Radionuclides
    def set_Radionuclides(self, Radionuclides):
        self.Radionuclides = Radionuclides
    def add_Radionuclides(self, value):
        self.Radionuclides.append(value)
    def insert_Radionuclides_at(self, index, value):
        self.Radionuclides.insert(index, value)
    def replace_Radionuclides_at(self, index, value):
        self.Radionuclides[index] = value
    def get_Activity(self):
        return self.Activity
    def set_Activity(self, Activity):
        self.Activity = Activity
    def get_PhysicalForm(self):
        return self.PhysicalForm
    def set_PhysicalForm(self, PhysicalForm):
        self.PhysicalForm = PhysicalForm
    def get_ChemicalForm(self):
        return self.ChemicalForm
    def set_ChemicalForm(self, ChemicalForm):
        self.ChemicalForm = ChemicalForm
    def validate_PhysicalFormType(self, value):
        result = True
        # Validate type PhysicalFormType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['GAS', 'LIQUID', 'SOLID', 'SPECIAL']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on PhysicalFormType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Radionuclides or
            self.Activity is not None or
            self.PhysicalForm is not None or
            self.ChemicalForm is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DangerousGoodsRadionuclideDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DangerousGoodsRadionuclideDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DangerousGoodsRadionuclideDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DangerousGoodsRadionuclideDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DangerousGoodsRadionuclideDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DangerousGoodsRadionuclideDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DangerousGoodsRadionuclideDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Radionuclides_ in self.Radionuclides:
            namespaceprefix_ = self.Radionuclides_nsprefix_ + ':' if (UseCapturedNS_ and self.Radionuclides_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRadionuclides>%s</%sRadionuclides>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Radionuclides_), input_name='Radionuclides')), namespaceprefix_ , eol_))
        if self.Activity is not None:
            namespaceprefix_ = self.Activity_nsprefix_ + ':' if (UseCapturedNS_ and self.Activity_nsprefix_) else ''
            self.Activity.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Activity', pretty_print=pretty_print)
        if self.PhysicalForm is not None:
            namespaceprefix_ = self.PhysicalForm_nsprefix_ + ':' if (UseCapturedNS_ and self.PhysicalForm_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPhysicalForm>%s</%sPhysicalForm>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PhysicalForm), input_name='PhysicalForm')), namespaceprefix_ , eol_))
        if self.ChemicalForm is not None:
            namespaceprefix_ = self.ChemicalForm_nsprefix_ + ':' if (UseCapturedNS_ and self.ChemicalForm_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChemicalForm>%s</%sChemicalForm>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChemicalForm), input_name='ChemicalForm')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Radionuclides':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Radionuclides')
            value_ = self.gds_validate_string(value_, node, 'Radionuclides')
            self.Radionuclides.append(value_)
            self.Radionuclides_nsprefix_ = child_.prefix
        elif nodeName_ == 'Activity':
            obj_ = DangerousGoodsRadionuclideActivity.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Activity = obj_
            obj_.original_tagname_ = 'Activity'
        elif nodeName_ == 'PhysicalForm':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PhysicalForm')
            value_ = self.gds_validate_string(value_, node, 'PhysicalForm')
            self.PhysicalForm = value_
            self.PhysicalForm_nsprefix_ = child_.prefix
            # validate type PhysicalFormType
            self.validate_PhysicalFormType(self.PhysicalForm)
        elif nodeName_ == 'ChemicalForm':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChemicalForm')
            value_ = self.gds_validate_string(value_, node, 'ChemicalForm')
            self.ChemicalForm = value_
            self.ChemicalForm_nsprefix_ = child_.prefix
# end class DangerousGoodsRadionuclideDetail


class DangerousGoodsSignatory(GeneratedsSuper):
    """Specifies that name, title and place of the signatory responsible for
    the dangerous goods shipment."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ContactName=None, Title=None, Place=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ContactName = ContactName
        self.ContactName_nsprefix_ = None
        self.Title = Title
        self.Title_nsprefix_ = None
        self.Place = Place
        self.Place_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DangerousGoodsSignatory)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DangerousGoodsSignatory.subclass:
            return DangerousGoodsSignatory.subclass(*args_, **kwargs_)
        else:
            return DangerousGoodsSignatory(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ContactName(self):
        return self.ContactName
    def set_ContactName(self, ContactName):
        self.ContactName = ContactName
    def get_Title(self):
        return self.Title
    def set_Title(self, Title):
        self.Title = Title
    def get_Place(self):
        return self.Place
    def set_Place(self, Place):
        self.Place = Place
    def hasContent_(self):
        if (
            self.ContactName is not None or
            self.Title is not None or
            self.Place is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DangerousGoodsSignatory', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DangerousGoodsSignatory')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DangerousGoodsSignatory':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DangerousGoodsSignatory')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DangerousGoodsSignatory', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DangerousGoodsSignatory'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DangerousGoodsSignatory', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ContactName is not None:
            namespaceprefix_ = self.ContactName_nsprefix_ + ':' if (UseCapturedNS_ and self.ContactName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sContactName>%s</%sContactName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ContactName), input_name='ContactName')), namespaceprefix_ , eol_))
        if self.Title is not None:
            namespaceprefix_ = self.Title_nsprefix_ + ':' if (UseCapturedNS_ and self.Title_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTitle>%s</%sTitle>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Title), input_name='Title')), namespaceprefix_ , eol_))
        if self.Place is not None:
            namespaceprefix_ = self.Place_nsprefix_ + ':' if (UseCapturedNS_ and self.Place_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPlace>%s</%sPlace>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Place), input_name='Place')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ContactName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ContactName')
            value_ = self.gds_validate_string(value_, node, 'ContactName')
            self.ContactName = value_
            self.ContactName_nsprefix_ = child_.prefix
        elif nodeName_ == 'Title':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Title')
            value_ = self.gds_validate_string(value_, node, 'Title')
            self.Title = value_
            self.Title_nsprefix_ = child_.prefix
        elif nodeName_ == 'Place':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Place')
            value_ = self.gds_validate_string(value_, node, 'Place')
            self.Place = value_
            self.Place_nsprefix_ = child_.prefix
# end class DangerousGoodsSignatory


class DeleteDangerousGoodsHandlingUnitReply(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, CompletedShipmentDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.HighestSeverity = HighestSeverity
        self.validate_NotificationSeverityType(self.HighestSeverity)
        self.HighestSeverity_nsprefix_ = "ns"
        if Notifications is None:
            self.Notifications = []
        else:
            self.Notifications = Notifications
        self.Notifications_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.CompletedShipmentDetail = CompletedShipmentDetail
        self.CompletedShipmentDetail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DeleteDangerousGoodsHandlingUnitReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DeleteDangerousGoodsHandlingUnitReply.subclass:
            return DeleteDangerousGoodsHandlingUnitReply.subclass(*args_, **kwargs_)
        else:
            return DeleteDangerousGoodsHandlingUnitReply(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_HighestSeverity(self):
        return self.HighestSeverity
    def set_HighestSeverity(self, HighestSeverity):
        self.HighestSeverity = HighestSeverity
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def add_Notifications(self, value):
        self.Notifications.append(value)
    def insert_Notifications_at(self, index, value):
        self.Notifications.insert(index, value)
    def replace_Notifications_at(self, index, value):
        self.Notifications[index] = value
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_CompletedShipmentDetail(self):
        return self.CompletedShipmentDetail
    def set_CompletedShipmentDetail(self, CompletedShipmentDetail):
        self.CompletedShipmentDetail = CompletedShipmentDetail
    def validate_NotificationSeverityType(self, value):
        result = True
        # Validate type NotificationSeverityType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ERROR', 'FAILURE', 'NOTE', 'SUCCESS', 'WARNING']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on NotificationSeverityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.HighestSeverity is not None or
            self.Notifications or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.CompletedShipmentDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeleteDangerousGoodsHandlingUnitReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DeleteDangerousGoodsHandlingUnitReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DeleteDangerousGoodsHandlingUnitReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DeleteDangerousGoodsHandlingUnitReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DeleteDangerousGoodsHandlingUnitReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DeleteDangerousGoodsHandlingUnitReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeleteDangerousGoodsHandlingUnitReply', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.HighestSeverity is not None:
            namespaceprefix_ = self.HighestSeverity_nsprefix_ + ':' if (UseCapturedNS_ and self.HighestSeverity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHighestSeverity>%s</%sHighestSeverity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HighestSeverity), input_name='HighestSeverity')), namespaceprefix_ , eol_))
        for Notifications_ in self.Notifications:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            Notifications_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.CompletedShipmentDetail is not None:
            namespaceprefix_ = self.CompletedShipmentDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.CompletedShipmentDetail_nsprefix_) else ''
            self.CompletedShipmentDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CompletedShipmentDetail', pretty_print=pretty_print)
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
        if nodeName_ == 'HighestSeverity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HighestSeverity')
            value_ = self.gds_validate_string(value_, node, 'HighestSeverity')
            self.HighestSeverity = value_
            self.HighestSeverity_nsprefix_ = child_.prefix
            # validate type NotificationSeverityType
            self.validate_NotificationSeverityType(self.HighestSeverity)
        elif nodeName_ == 'Notifications':
            obj_ = Notification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications.append(obj_)
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'CompletedShipmentDetail':
            obj_ = CompletedDangerousGoodsShipmentDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CompletedShipmentDetail = obj_
            obj_.original_tagname_ = 'CompletedShipmentDetail'
# end class DeleteDangerousGoodsHandlingUnitReply


class DeleteDangerousGoodsHandlingUnitRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, TransactionDetail=None, Version=None, UploadId=None, HandlingUnitGroupId=None, TrackingNumbers=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.WebAuthenticationDetail = WebAuthenticationDetail
        self.WebAuthenticationDetail_nsprefix_ = "ns"
        self.ClientDetail = ClientDetail
        self.ClientDetail_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.UploadId = UploadId
        self.UploadId_nsprefix_ = None
        self.HandlingUnitGroupId = HandlingUnitGroupId
        self.HandlingUnitGroupId_nsprefix_ = None
        if TrackingNumbers is None:
            self.TrackingNumbers = []
        else:
            self.TrackingNumbers = TrackingNumbers
        self.TrackingNumbers_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DeleteDangerousGoodsHandlingUnitRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DeleteDangerousGoodsHandlingUnitRequest.subclass:
            return DeleteDangerousGoodsHandlingUnitRequest.subclass(*args_, **kwargs_)
        else:
            return DeleteDangerousGoodsHandlingUnitRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_WebAuthenticationDetail(self):
        return self.WebAuthenticationDetail
    def set_WebAuthenticationDetail(self, WebAuthenticationDetail):
        self.WebAuthenticationDetail = WebAuthenticationDetail
    def get_ClientDetail(self):
        return self.ClientDetail
    def set_ClientDetail(self, ClientDetail):
        self.ClientDetail = ClientDetail
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_UploadId(self):
        return self.UploadId
    def set_UploadId(self, UploadId):
        self.UploadId = UploadId
    def get_HandlingUnitGroupId(self):
        return self.HandlingUnitGroupId
    def set_HandlingUnitGroupId(self, HandlingUnitGroupId):
        self.HandlingUnitGroupId = HandlingUnitGroupId
    def get_TrackingNumbers(self):
        return self.TrackingNumbers
    def set_TrackingNumbers(self, TrackingNumbers):
        self.TrackingNumbers = TrackingNumbers
    def add_TrackingNumbers(self, value):
        self.TrackingNumbers.append(value)
    def insert_TrackingNumbers_at(self, index, value):
        self.TrackingNumbers.insert(index, value)
    def replace_TrackingNumbers_at(self, index, value):
        self.TrackingNumbers[index] = value
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.UploadId is not None or
            self.HandlingUnitGroupId is not None or
            self.TrackingNumbers
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeleteDangerousGoodsHandlingUnitRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DeleteDangerousGoodsHandlingUnitRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DeleteDangerousGoodsHandlingUnitRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DeleteDangerousGoodsHandlingUnitRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DeleteDangerousGoodsHandlingUnitRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DeleteDangerousGoodsHandlingUnitRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeleteDangerousGoodsHandlingUnitRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.WebAuthenticationDetail is not None:
            namespaceprefix_ = self.WebAuthenticationDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.WebAuthenticationDetail_nsprefix_) else ''
            self.WebAuthenticationDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='WebAuthenticationDetail', pretty_print=pretty_print)
        if self.ClientDetail is not None:
            namespaceprefix_ = self.ClientDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientDetail_nsprefix_) else ''
            self.ClientDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClientDetail', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.UploadId is not None:
            namespaceprefix_ = self.UploadId_nsprefix_ + ':' if (UseCapturedNS_ and self.UploadId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUploadId>%s</%sUploadId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UploadId), input_name='UploadId')), namespaceprefix_ , eol_))
        if self.HandlingUnitGroupId is not None:
            namespaceprefix_ = self.HandlingUnitGroupId_nsprefix_ + ':' if (UseCapturedNS_ and self.HandlingUnitGroupId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHandlingUnitGroupId>%s</%sHandlingUnitGroupId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HandlingUnitGroupId), input_name='HandlingUnitGroupId')), namespaceprefix_ , eol_))
        for TrackingNumbers_ in self.TrackingNumbers:
            namespaceprefix_ = self.TrackingNumbers_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackingNumbers_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTrackingNumbers>%s</%sTrackingNumbers>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(TrackingNumbers_), input_name='TrackingNumbers')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'WebAuthenticationDetail':
            obj_ = WebAuthenticationDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.WebAuthenticationDetail = obj_
            obj_.original_tagname_ = 'WebAuthenticationDetail'
        elif nodeName_ == 'ClientDetail':
            obj_ = ClientDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClientDetail = obj_
            obj_.original_tagname_ = 'ClientDetail'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'UploadId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UploadId')
            value_ = self.gds_validate_string(value_, node, 'UploadId')
            self.UploadId = value_
            self.UploadId_nsprefix_ = child_.prefix
        elif nodeName_ == 'HandlingUnitGroupId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HandlingUnitGroupId')
            value_ = self.gds_validate_string(value_, node, 'HandlingUnitGroupId')
            self.HandlingUnitGroupId = value_
            self.HandlingUnitGroupId_nsprefix_ = child_.prefix
        elif nodeName_ == 'TrackingNumbers':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TrackingNumbers')
            value_ = self.gds_validate_string(value_, node, 'TrackingNumbers')
            self.TrackingNumbers.append(value_)
            self.TrackingNumbers_nsprefix_ = child_.prefix
# end class DeleteDangerousGoodsHandlingUnitRequest


class DeleteDangerousGoodsReply(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.HighestSeverity = HighestSeverity
        self.validate_NotificationSeverityType(self.HighestSeverity)
        self.HighestSeverity_nsprefix_ = "ns"
        if Notifications is None:
            self.Notifications = []
        else:
            self.Notifications = Notifications
        self.Notifications_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DeleteDangerousGoodsReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DeleteDangerousGoodsReply.subclass:
            return DeleteDangerousGoodsReply.subclass(*args_, **kwargs_)
        else:
            return DeleteDangerousGoodsReply(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_HighestSeverity(self):
        return self.HighestSeverity
    def set_HighestSeverity(self, HighestSeverity):
        self.HighestSeverity = HighestSeverity
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def add_Notifications(self, value):
        self.Notifications.append(value)
    def insert_Notifications_at(self, index, value):
        self.Notifications.insert(index, value)
    def replace_Notifications_at(self, index, value):
        self.Notifications[index] = value
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def validate_NotificationSeverityType(self, value):
        result = True
        # Validate type NotificationSeverityType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ERROR', 'FAILURE', 'NOTE', 'SUCCESS', 'WARNING']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on NotificationSeverityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.HighestSeverity is not None or
            self.Notifications or
            self.TransactionDetail is not None or
            self.Version is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeleteDangerousGoodsReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DeleteDangerousGoodsReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DeleteDangerousGoodsReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DeleteDangerousGoodsReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DeleteDangerousGoodsReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DeleteDangerousGoodsReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeleteDangerousGoodsReply', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.HighestSeverity is not None:
            namespaceprefix_ = self.HighestSeverity_nsprefix_ + ':' if (UseCapturedNS_ and self.HighestSeverity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHighestSeverity>%s</%sHighestSeverity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HighestSeverity), input_name='HighestSeverity')), namespaceprefix_ , eol_))
        for Notifications_ in self.Notifications:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            Notifications_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
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
        if nodeName_ == 'HighestSeverity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HighestSeverity')
            value_ = self.gds_validate_string(value_, node, 'HighestSeverity')
            self.HighestSeverity = value_
            self.HighestSeverity_nsprefix_ = child_.prefix
            # validate type NotificationSeverityType
            self.validate_NotificationSeverityType(self.HighestSeverity)
        elif nodeName_ == 'Notifications':
            obj_ = Notification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications.append(obj_)
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
# end class DeleteDangerousGoodsReply


class DeleteDangerousGoodsRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, TransactionDetail=None, Version=None, UploadId=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.WebAuthenticationDetail = WebAuthenticationDetail
        self.WebAuthenticationDetail_nsprefix_ = "ns"
        self.ClientDetail = ClientDetail
        self.ClientDetail_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.UploadId = UploadId
        self.UploadId_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DeleteDangerousGoodsRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DeleteDangerousGoodsRequest.subclass:
            return DeleteDangerousGoodsRequest.subclass(*args_, **kwargs_)
        else:
            return DeleteDangerousGoodsRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_WebAuthenticationDetail(self):
        return self.WebAuthenticationDetail
    def set_WebAuthenticationDetail(self, WebAuthenticationDetail):
        self.WebAuthenticationDetail = WebAuthenticationDetail
    def get_ClientDetail(self):
        return self.ClientDetail
    def set_ClientDetail(self, ClientDetail):
        self.ClientDetail = ClientDetail
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_UploadId(self):
        return self.UploadId
    def set_UploadId(self, UploadId):
        self.UploadId = UploadId
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.UploadId is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeleteDangerousGoodsRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DeleteDangerousGoodsRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DeleteDangerousGoodsRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DeleteDangerousGoodsRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DeleteDangerousGoodsRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DeleteDangerousGoodsRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeleteDangerousGoodsRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.WebAuthenticationDetail is not None:
            namespaceprefix_ = self.WebAuthenticationDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.WebAuthenticationDetail_nsprefix_) else ''
            self.WebAuthenticationDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='WebAuthenticationDetail', pretty_print=pretty_print)
        if self.ClientDetail is not None:
            namespaceprefix_ = self.ClientDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientDetail_nsprefix_) else ''
            self.ClientDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClientDetail', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.UploadId is not None:
            namespaceprefix_ = self.UploadId_nsprefix_ + ':' if (UseCapturedNS_ and self.UploadId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUploadId>%s</%sUploadId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UploadId), input_name='UploadId')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'WebAuthenticationDetail':
            obj_ = WebAuthenticationDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.WebAuthenticationDetail = obj_
            obj_.original_tagname_ = 'WebAuthenticationDetail'
        elif nodeName_ == 'ClientDetail':
            obj_ = ClientDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClientDetail = obj_
            obj_.original_tagname_ = 'ClientDetail'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'UploadId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UploadId')
            value_ = self.gds_validate_string(value_, node, 'UploadId')
            self.UploadId = value_
            self.UploadId_nsprefix_ = child_.prefix
# end class DeleteDangerousGoodsRequest


class Localization(GeneratedsSuper):
    """Identifies the representation of human-readable text."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, LanguageCode=None, LocaleCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.LanguageCode = LanguageCode
        self.LanguageCode_nsprefix_ = None
        self.LocaleCode = LocaleCode
        self.LocaleCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Localization)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Localization.subclass:
            return Localization.subclass(*args_, **kwargs_)
        else:
            return Localization(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_LanguageCode(self):
        return self.LanguageCode
    def set_LanguageCode(self, LanguageCode):
        self.LanguageCode = LanguageCode
    def get_LocaleCode(self):
        return self.LocaleCode
    def set_LocaleCode(self, LocaleCode):
        self.LocaleCode = LocaleCode
    def hasContent_(self):
        if (
            self.LanguageCode is not None or
            self.LocaleCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Localization', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Localization')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Localization':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Localization')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Localization', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Localization'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Localization', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.LanguageCode is not None:
            namespaceprefix_ = self.LanguageCode_nsprefix_ + ':' if (UseCapturedNS_ and self.LanguageCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLanguageCode>%s</%sLanguageCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LanguageCode), input_name='LanguageCode')), namespaceprefix_ , eol_))
        if self.LocaleCode is not None:
            namespaceprefix_ = self.LocaleCode_nsprefix_ + ':' if (UseCapturedNS_ and self.LocaleCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocaleCode>%s</%sLocaleCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocaleCode), input_name='LocaleCode')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'LanguageCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LanguageCode')
            value_ = self.gds_validate_string(value_, node, 'LanguageCode')
            self.LanguageCode = value_
            self.LanguageCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocaleCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocaleCode')
            value_ = self.gds_validate_string(value_, node, 'LocaleCode')
            self.LocaleCode = value_
            self.LocaleCode_nsprefix_ = child_.prefix
# end class Localization


class ModifyDangerousGoodsHandlingUnitReply(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, CompletedShipmentDetail=None, CompletedHandlingUnitGroup=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.HighestSeverity = HighestSeverity
        self.validate_NotificationSeverityType(self.HighestSeverity)
        self.HighestSeverity_nsprefix_ = "ns"
        if Notifications is None:
            self.Notifications = []
        else:
            self.Notifications = Notifications
        self.Notifications_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.CompletedShipmentDetail = CompletedShipmentDetail
        self.CompletedShipmentDetail_nsprefix_ = "ns"
        self.CompletedHandlingUnitGroup = CompletedHandlingUnitGroup
        self.CompletedHandlingUnitGroup_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ModifyDangerousGoodsHandlingUnitReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ModifyDangerousGoodsHandlingUnitReply.subclass:
            return ModifyDangerousGoodsHandlingUnitReply.subclass(*args_, **kwargs_)
        else:
            return ModifyDangerousGoodsHandlingUnitReply(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_HighestSeverity(self):
        return self.HighestSeverity
    def set_HighestSeverity(self, HighestSeverity):
        self.HighestSeverity = HighestSeverity
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def add_Notifications(self, value):
        self.Notifications.append(value)
    def insert_Notifications_at(self, index, value):
        self.Notifications.insert(index, value)
    def replace_Notifications_at(self, index, value):
        self.Notifications[index] = value
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_CompletedShipmentDetail(self):
        return self.CompletedShipmentDetail
    def set_CompletedShipmentDetail(self, CompletedShipmentDetail):
        self.CompletedShipmentDetail = CompletedShipmentDetail
    def get_CompletedHandlingUnitGroup(self):
        return self.CompletedHandlingUnitGroup
    def set_CompletedHandlingUnitGroup(self, CompletedHandlingUnitGroup):
        self.CompletedHandlingUnitGroup = CompletedHandlingUnitGroup
    def validate_NotificationSeverityType(self, value):
        result = True
        # Validate type NotificationSeverityType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ERROR', 'FAILURE', 'NOTE', 'SUCCESS', 'WARNING']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on NotificationSeverityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.HighestSeverity is not None or
            self.Notifications or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.CompletedShipmentDetail is not None or
            self.CompletedHandlingUnitGroup is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ModifyDangerousGoodsHandlingUnitReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ModifyDangerousGoodsHandlingUnitReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ModifyDangerousGoodsHandlingUnitReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ModifyDangerousGoodsHandlingUnitReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ModifyDangerousGoodsHandlingUnitReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ModifyDangerousGoodsHandlingUnitReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ModifyDangerousGoodsHandlingUnitReply', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.HighestSeverity is not None:
            namespaceprefix_ = self.HighestSeverity_nsprefix_ + ':' if (UseCapturedNS_ and self.HighestSeverity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHighestSeverity>%s</%sHighestSeverity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HighestSeverity), input_name='HighestSeverity')), namespaceprefix_ , eol_))
        for Notifications_ in self.Notifications:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            Notifications_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.CompletedShipmentDetail is not None:
            namespaceprefix_ = self.CompletedShipmentDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.CompletedShipmentDetail_nsprefix_) else ''
            self.CompletedShipmentDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CompletedShipmentDetail', pretty_print=pretty_print)
        if self.CompletedHandlingUnitGroup is not None:
            namespaceprefix_ = self.CompletedHandlingUnitGroup_nsprefix_ + ':' if (UseCapturedNS_ and self.CompletedHandlingUnitGroup_nsprefix_) else ''
            self.CompletedHandlingUnitGroup.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CompletedHandlingUnitGroup', pretty_print=pretty_print)
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
        if nodeName_ == 'HighestSeverity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HighestSeverity')
            value_ = self.gds_validate_string(value_, node, 'HighestSeverity')
            self.HighestSeverity = value_
            self.HighestSeverity_nsprefix_ = child_.prefix
            # validate type NotificationSeverityType
            self.validate_NotificationSeverityType(self.HighestSeverity)
        elif nodeName_ == 'Notifications':
            obj_ = Notification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications.append(obj_)
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'CompletedShipmentDetail':
            obj_ = CompletedDangerousGoodsShipmentDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CompletedShipmentDetail = obj_
            obj_.original_tagname_ = 'CompletedShipmentDetail'
        elif nodeName_ == 'CompletedHandlingUnitGroup':
            obj_ = CompletedDangerousGoodsHandlingUnitGroup.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CompletedHandlingUnitGroup = obj_
            obj_.original_tagname_ = 'CompletedHandlingUnitGroup'
# end class ModifyDangerousGoodsHandlingUnitReply


class ModifyDangerousGoodsHandlingUnitRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, TransactionDetail=None, Version=None, UploadId=None, HandlingUnitGroup=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.WebAuthenticationDetail = WebAuthenticationDetail
        self.WebAuthenticationDetail_nsprefix_ = "ns"
        self.ClientDetail = ClientDetail
        self.ClientDetail_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.UploadId = UploadId
        self.UploadId_nsprefix_ = None
        self.HandlingUnitGroup = HandlingUnitGroup
        self.HandlingUnitGroup_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ModifyDangerousGoodsHandlingUnitRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ModifyDangerousGoodsHandlingUnitRequest.subclass:
            return ModifyDangerousGoodsHandlingUnitRequest.subclass(*args_, **kwargs_)
        else:
            return ModifyDangerousGoodsHandlingUnitRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_WebAuthenticationDetail(self):
        return self.WebAuthenticationDetail
    def set_WebAuthenticationDetail(self, WebAuthenticationDetail):
        self.WebAuthenticationDetail = WebAuthenticationDetail
    def get_ClientDetail(self):
        return self.ClientDetail
    def set_ClientDetail(self, ClientDetail):
        self.ClientDetail = ClientDetail
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_UploadId(self):
        return self.UploadId
    def set_UploadId(self, UploadId):
        self.UploadId = UploadId
    def get_HandlingUnitGroup(self):
        return self.HandlingUnitGroup
    def set_HandlingUnitGroup(self, HandlingUnitGroup):
        self.HandlingUnitGroup = HandlingUnitGroup
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.UploadId is not None or
            self.HandlingUnitGroup is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ModifyDangerousGoodsHandlingUnitRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ModifyDangerousGoodsHandlingUnitRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ModifyDangerousGoodsHandlingUnitRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ModifyDangerousGoodsHandlingUnitRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ModifyDangerousGoodsHandlingUnitRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ModifyDangerousGoodsHandlingUnitRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ModifyDangerousGoodsHandlingUnitRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.WebAuthenticationDetail is not None:
            namespaceprefix_ = self.WebAuthenticationDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.WebAuthenticationDetail_nsprefix_) else ''
            self.WebAuthenticationDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='WebAuthenticationDetail', pretty_print=pretty_print)
        if self.ClientDetail is not None:
            namespaceprefix_ = self.ClientDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientDetail_nsprefix_) else ''
            self.ClientDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClientDetail', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.UploadId is not None:
            namespaceprefix_ = self.UploadId_nsprefix_ + ':' if (UseCapturedNS_ and self.UploadId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUploadId>%s</%sUploadId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UploadId), input_name='UploadId')), namespaceprefix_ , eol_))
        if self.HandlingUnitGroup is not None:
            namespaceprefix_ = self.HandlingUnitGroup_nsprefix_ + ':' if (UseCapturedNS_ and self.HandlingUnitGroup_nsprefix_) else ''
            self.HandlingUnitGroup.export(outfile, level, namespaceprefix_, namespacedef_='', name_='HandlingUnitGroup', pretty_print=pretty_print)
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
        if nodeName_ == 'WebAuthenticationDetail':
            obj_ = WebAuthenticationDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.WebAuthenticationDetail = obj_
            obj_.original_tagname_ = 'WebAuthenticationDetail'
        elif nodeName_ == 'ClientDetail':
            obj_ = ClientDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClientDetail = obj_
            obj_.original_tagname_ = 'ClientDetail'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'UploadId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UploadId')
            value_ = self.gds_validate_string(value_, node, 'UploadId')
            self.UploadId = value_
            self.UploadId_nsprefix_ = child_.prefix
        elif nodeName_ == 'HandlingUnitGroup':
            obj_ = UploadedDangerousGoodsHandlingUnitGroup.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.HandlingUnitGroup = obj_
            obj_.original_tagname_ = 'HandlingUnitGroup'
# end class ModifyDangerousGoodsHandlingUnitRequest


class ModifyDangerousGoodsShipmentReply(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, CompletedShipmentDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.HighestSeverity = HighestSeverity
        self.validate_NotificationSeverityType(self.HighestSeverity)
        self.HighestSeverity_nsprefix_ = "ns"
        if Notifications is None:
            self.Notifications = []
        else:
            self.Notifications = Notifications
        self.Notifications_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.CompletedShipmentDetail = CompletedShipmentDetail
        self.CompletedShipmentDetail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ModifyDangerousGoodsShipmentReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ModifyDangerousGoodsShipmentReply.subclass:
            return ModifyDangerousGoodsShipmentReply.subclass(*args_, **kwargs_)
        else:
            return ModifyDangerousGoodsShipmentReply(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_HighestSeverity(self):
        return self.HighestSeverity
    def set_HighestSeverity(self, HighestSeverity):
        self.HighestSeverity = HighestSeverity
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def add_Notifications(self, value):
        self.Notifications.append(value)
    def insert_Notifications_at(self, index, value):
        self.Notifications.insert(index, value)
    def replace_Notifications_at(self, index, value):
        self.Notifications[index] = value
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_CompletedShipmentDetail(self):
        return self.CompletedShipmentDetail
    def set_CompletedShipmentDetail(self, CompletedShipmentDetail):
        self.CompletedShipmentDetail = CompletedShipmentDetail
    def validate_NotificationSeverityType(self, value):
        result = True
        # Validate type NotificationSeverityType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ERROR', 'FAILURE', 'NOTE', 'SUCCESS', 'WARNING']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on NotificationSeverityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.HighestSeverity is not None or
            self.Notifications or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.CompletedShipmentDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ModifyDangerousGoodsShipmentReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ModifyDangerousGoodsShipmentReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ModifyDangerousGoodsShipmentReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ModifyDangerousGoodsShipmentReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ModifyDangerousGoodsShipmentReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ModifyDangerousGoodsShipmentReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ModifyDangerousGoodsShipmentReply', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.HighestSeverity is not None:
            namespaceprefix_ = self.HighestSeverity_nsprefix_ + ':' if (UseCapturedNS_ and self.HighestSeverity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHighestSeverity>%s</%sHighestSeverity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HighestSeverity), input_name='HighestSeverity')), namespaceprefix_ , eol_))
        for Notifications_ in self.Notifications:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            Notifications_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.CompletedShipmentDetail is not None:
            namespaceprefix_ = self.CompletedShipmentDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.CompletedShipmentDetail_nsprefix_) else ''
            self.CompletedShipmentDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CompletedShipmentDetail', pretty_print=pretty_print)
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
        if nodeName_ == 'HighestSeverity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HighestSeverity')
            value_ = self.gds_validate_string(value_, node, 'HighestSeverity')
            self.HighestSeverity = value_
            self.HighestSeverity_nsprefix_ = child_.prefix
            # validate type NotificationSeverityType
            self.validate_NotificationSeverityType(self.HighestSeverity)
        elif nodeName_ == 'Notifications':
            obj_ = Notification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications.append(obj_)
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'CompletedShipmentDetail':
            obj_ = CompletedDangerousGoodsShipmentDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CompletedShipmentDetail = obj_
            obj_.original_tagname_ = 'CompletedShipmentDetail'
# end class ModifyDangerousGoodsShipmentReply


class ModifyDangerousGoodsShipmentRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, TransactionDetail=None, Version=None, UploadId=None, ShipmentDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.WebAuthenticationDetail = WebAuthenticationDetail
        self.WebAuthenticationDetail_nsprefix_ = "ns"
        self.ClientDetail = ClientDetail
        self.ClientDetail_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.UploadId = UploadId
        self.UploadId_nsprefix_ = None
        self.ShipmentDetail = ShipmentDetail
        self.ShipmentDetail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ModifyDangerousGoodsShipmentRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ModifyDangerousGoodsShipmentRequest.subclass:
            return ModifyDangerousGoodsShipmentRequest.subclass(*args_, **kwargs_)
        else:
            return ModifyDangerousGoodsShipmentRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_WebAuthenticationDetail(self):
        return self.WebAuthenticationDetail
    def set_WebAuthenticationDetail(self, WebAuthenticationDetail):
        self.WebAuthenticationDetail = WebAuthenticationDetail
    def get_ClientDetail(self):
        return self.ClientDetail
    def set_ClientDetail(self, ClientDetail):
        self.ClientDetail = ClientDetail
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_UploadId(self):
        return self.UploadId
    def set_UploadId(self, UploadId):
        self.UploadId = UploadId
    def get_ShipmentDetail(self):
        return self.ShipmentDetail
    def set_ShipmentDetail(self, ShipmentDetail):
        self.ShipmentDetail = ShipmentDetail
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.UploadId is not None or
            self.ShipmentDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ModifyDangerousGoodsShipmentRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ModifyDangerousGoodsShipmentRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ModifyDangerousGoodsShipmentRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ModifyDangerousGoodsShipmentRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ModifyDangerousGoodsShipmentRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ModifyDangerousGoodsShipmentRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ModifyDangerousGoodsShipmentRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.WebAuthenticationDetail is not None:
            namespaceprefix_ = self.WebAuthenticationDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.WebAuthenticationDetail_nsprefix_) else ''
            self.WebAuthenticationDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='WebAuthenticationDetail', pretty_print=pretty_print)
        if self.ClientDetail is not None:
            namespaceprefix_ = self.ClientDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientDetail_nsprefix_) else ''
            self.ClientDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClientDetail', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.UploadId is not None:
            namespaceprefix_ = self.UploadId_nsprefix_ + ':' if (UseCapturedNS_ and self.UploadId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUploadId>%s</%sUploadId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UploadId), input_name='UploadId')), namespaceprefix_ , eol_))
        if self.ShipmentDetail is not None:
            namespaceprefix_ = self.ShipmentDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentDetail_nsprefix_) else ''
            self.ShipmentDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentDetail', pretty_print=pretty_print)
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
        if nodeName_ == 'WebAuthenticationDetail':
            obj_ = WebAuthenticationDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.WebAuthenticationDetail = obj_
            obj_.original_tagname_ = 'WebAuthenticationDetail'
        elif nodeName_ == 'ClientDetail':
            obj_ = ClientDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClientDetail = obj_
            obj_.original_tagname_ = 'ClientDetail'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'UploadId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UploadId')
            value_ = self.gds_validate_string(value_, node, 'UploadId')
            self.UploadId = value_
            self.UploadId_nsprefix_ = child_.prefix
        elif nodeName_ == 'ShipmentDetail':
            obj_ = UploadedDangerousGoodsShipmentDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentDetail = obj_
            obj_.original_tagname_ = 'ShipmentDetail'
# end class ModifyDangerousGoodsShipmentRequest


class NetExplosiveDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Type=None, Amount=None, Units=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Type = Type
        self.validate_NetExplosiveClassificationType(self.Type)
        self.Type_nsprefix_ = "ns"
        self.Amount = Amount
        self.Amount_nsprefix_ = None
        self.Units = Units
        self.Units_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, NetExplosiveDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if NetExplosiveDetail.subclass:
            return NetExplosiveDetail.subclass(*args_, **kwargs_)
        else:
            return NetExplosiveDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_Amount(self):
        return self.Amount
    def set_Amount(self, Amount):
        self.Amount = Amount
    def get_Units(self):
        return self.Units
    def set_Units(self, Units):
        self.Units = Units
    def validate_NetExplosiveClassificationType(self, value):
        result = True
        # Validate type NetExplosiveClassificationType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['NET_EXPLOSIVE_CONTENT', 'NET_EXPLOSIVE_MASS', 'NET_EXPLOSIVE_QUANTITY', 'NET_EXPLOSIVE_WEIGHT']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on NetExplosiveClassificationType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Type is not None or
            self.Amount is not None or
            self.Units is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NetExplosiveDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('NetExplosiveDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'NetExplosiveDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='NetExplosiveDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='NetExplosiveDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='NetExplosiveDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NetExplosiveDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sType>%s</%sType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Type), input_name='Type')), namespaceprefix_ , eol_))
        if self.Amount is not None:
            namespaceprefix_ = self.Amount_nsprefix_ + ':' if (UseCapturedNS_ and self.Amount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAmount>%s</%sAmount>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Amount, input_name='Amount'), namespaceprefix_ , eol_))
        if self.Units is not None:
            namespaceprefix_ = self.Units_nsprefix_ + ':' if (UseCapturedNS_ and self.Units_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUnits>%s</%sUnits>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Units), input_name='Units')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Type':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Type')
            value_ = self.gds_validate_string(value_, node, 'Type')
            self.Type = value_
            self.Type_nsprefix_ = child_.prefix
            # validate type NetExplosiveClassificationType
            self.validate_NetExplosiveClassificationType(self.Type)
        elif nodeName_ == 'Amount' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Amount')
            fval_ = self.gds_validate_decimal(fval_, node, 'Amount')
            self.Amount = fval_
            self.Amount_nsprefix_ = child_.prefix
        elif nodeName_ == 'Units':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Units')
            value_ = self.gds_validate_string(value_, node, 'Units')
            self.Units = value_
            self.Units_nsprefix_ = child_.prefix
# end class NetExplosiveDetail


class Notification(GeneratedsSuper):
    """The descriptive data regarding the result of the submitted
    transaction."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Severity=None, Source=None, Code=None, Message=None, LocalizedMessage=None, MessageParameters=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Severity = Severity
        self.validate_NotificationSeverityType(self.Severity)
        self.Severity_nsprefix_ = "ns"
        self.Source = Source
        self.Source_nsprefix_ = None
        self.Code = Code
        self.Code_nsprefix_ = None
        self.Message = Message
        self.Message_nsprefix_ = None
        self.LocalizedMessage = LocalizedMessage
        self.LocalizedMessage_nsprefix_ = None
        if MessageParameters is None:
            self.MessageParameters = []
        else:
            self.MessageParameters = MessageParameters
        self.MessageParameters_nsprefix_ = "ns"
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
    def get_Severity(self):
        return self.Severity
    def set_Severity(self, Severity):
        self.Severity = Severity
    def get_Source(self):
        return self.Source
    def set_Source(self, Source):
        self.Source = Source
    def get_Code(self):
        return self.Code
    def set_Code(self, Code):
        self.Code = Code
    def get_Message(self):
        return self.Message
    def set_Message(self, Message):
        self.Message = Message
    def get_LocalizedMessage(self):
        return self.LocalizedMessage
    def set_LocalizedMessage(self, LocalizedMessage):
        self.LocalizedMessage = LocalizedMessage
    def get_MessageParameters(self):
        return self.MessageParameters
    def set_MessageParameters(self, MessageParameters):
        self.MessageParameters = MessageParameters
    def add_MessageParameters(self, value):
        self.MessageParameters.append(value)
    def insert_MessageParameters_at(self, index, value):
        self.MessageParameters.insert(index, value)
    def replace_MessageParameters_at(self, index, value):
        self.MessageParameters[index] = value
    def validate_NotificationSeverityType(self, value):
        result = True
        # Validate type NotificationSeverityType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ERROR', 'FAILURE', 'NOTE', 'SUCCESS', 'WARNING']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on NotificationSeverityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Severity is not None or
            self.Source is not None or
            self.Code is not None or
            self.Message is not None or
            self.LocalizedMessage is not None or
            self.MessageParameters
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
        if self.Severity is not None:
            namespaceprefix_ = self.Severity_nsprefix_ + ':' if (UseCapturedNS_ and self.Severity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSeverity>%s</%sSeverity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Severity), input_name='Severity')), namespaceprefix_ , eol_))
        if self.Source is not None:
            namespaceprefix_ = self.Source_nsprefix_ + ':' if (UseCapturedNS_ and self.Source_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSource>%s</%sSource>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Source), input_name='Source')), namespaceprefix_ , eol_))
        if self.Code is not None:
            namespaceprefix_ = self.Code_nsprefix_ + ':' if (UseCapturedNS_ and self.Code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCode>%s</%sCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Code), input_name='Code')), namespaceprefix_ , eol_))
        if self.Message is not None:
            namespaceprefix_ = self.Message_nsprefix_ + ':' if (UseCapturedNS_ and self.Message_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMessage>%s</%sMessage>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Message), input_name='Message')), namespaceprefix_ , eol_))
        if self.LocalizedMessage is not None:
            namespaceprefix_ = self.LocalizedMessage_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalizedMessage_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalizedMessage>%s</%sLocalizedMessage>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalizedMessage), input_name='LocalizedMessage')), namespaceprefix_ , eol_))
        for MessageParameters_ in self.MessageParameters:
            namespaceprefix_ = self.MessageParameters_nsprefix_ + ':' if (UseCapturedNS_ and self.MessageParameters_nsprefix_) else ''
            MessageParameters_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='MessageParameters', pretty_print=pretty_print)
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
        if nodeName_ == 'Severity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Severity')
            value_ = self.gds_validate_string(value_, node, 'Severity')
            self.Severity = value_
            self.Severity_nsprefix_ = child_.prefix
            # validate type NotificationSeverityType
            self.validate_NotificationSeverityType(self.Severity)
        elif nodeName_ == 'Source':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Source')
            value_ = self.gds_validate_string(value_, node, 'Source')
            self.Source = value_
            self.Source_nsprefix_ = child_.prefix
        elif nodeName_ == 'Code':
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
        elif nodeName_ == 'LocalizedMessage':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalizedMessage')
            value_ = self.gds_validate_string(value_, node, 'LocalizedMessage')
            self.LocalizedMessage = value_
            self.LocalizedMessage_nsprefix_ = child_.prefix
        elif nodeName_ == 'MessageParameters':
            obj_ = NotificationParameter.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.MessageParameters.append(obj_)
            obj_.original_tagname_ = 'MessageParameters'
# end class Notification


class NotificationParameter(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Id=None, Value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Id = Id
        self.Id_nsprefix_ = None
        self.Value = Value
        self.Value_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, NotificationParameter)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if NotificationParameter.subclass:
            return NotificationParameter.subclass(*args_, **kwargs_)
        else:
            return NotificationParameter(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def hasContent_(self):
        if (
            self.Id is not None or
            self.Value is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NotificationParameter', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('NotificationParameter')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'NotificationParameter':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='NotificationParameter')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='NotificationParameter', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='NotificationParameter'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NotificationParameter', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Id is not None:
            namespaceprefix_ = self.Id_nsprefix_ + ':' if (UseCapturedNS_ and self.Id_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sId>%s</%sId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Id), input_name='Id')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Id':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Id')
            value_ = self.gds_validate_string(value_, node, 'Id')
            self.Id = value_
            self.Id_nsprefix_ = child_.prefix
        elif nodeName_ == 'Value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Value')
            value_ = self.gds_validate_string(value_, node, 'Value')
            self.Value = value_
            self.Value_nsprefix_ = child_.prefix
# end class NotificationParameter


class PreciseQuantity(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Amount=None, Units=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Amount = Amount
        self.Amount_nsprefix_ = None
        self.Units = Units
        self.Units_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PreciseQuantity)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PreciseQuantity.subclass:
            return PreciseQuantity.subclass(*args_, **kwargs_)
        else:
            return PreciseQuantity(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Amount(self):
        return self.Amount
    def set_Amount(self, Amount):
        self.Amount = Amount
    def get_Units(self):
        return self.Units
    def set_Units(self, Units):
        self.Units = Units
    def hasContent_(self):
        if (
            self.Amount is not None or
            self.Units is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PreciseQuantity', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PreciseQuantity')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PreciseQuantity':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PreciseQuantity')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PreciseQuantity', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PreciseQuantity'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PreciseQuantity', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Amount is not None:
            namespaceprefix_ = self.Amount_nsprefix_ + ':' if (UseCapturedNS_ and self.Amount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAmount>%s</%sAmount>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Amount, input_name='Amount'), namespaceprefix_ , eol_))
        if self.Units is not None:
            namespaceprefix_ = self.Units_nsprefix_ + ':' if (UseCapturedNS_ and self.Units_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUnits>%s</%sUnits>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Units), input_name='Units')), namespaceprefix_ , eol_))
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
            fval_ = self.gds_parse_decimal(sval_, node, 'Amount')
            fval_ = self.gds_validate_decimal(fval_, node, 'Amount')
            self.Amount = fval_
            self.Amount_nsprefix_ = child_.prefix
        elif nodeName_ == 'Units':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Units')
            value_ = self.gds_validate_string(value_, node, 'Units')
            self.Units = value_
            self.Units_nsprefix_ = child_.prefix
# end class PreciseQuantity


class RadioactiveDangerousGoodsHandlingUnitDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TransportIndex=None, SurfaceReading=None, CriticalitySafetyIndex=None, LabelType=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.TransportIndex = TransportIndex
        self.TransportIndex_nsprefix_ = None
        self.SurfaceReading = SurfaceReading
        self.SurfaceReading_nsprefix_ = None
        self.CriticalitySafetyIndex = CriticalitySafetyIndex
        self.CriticalitySafetyIndex_nsprefix_ = None
        self.LabelType = LabelType
        self.validate_RadioactiveLabelType(self.LabelType)
        self.LabelType_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RadioactiveDangerousGoodsHandlingUnitDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RadioactiveDangerousGoodsHandlingUnitDetail.subclass:
            return RadioactiveDangerousGoodsHandlingUnitDetail.subclass(*args_, **kwargs_)
        else:
            return RadioactiveDangerousGoodsHandlingUnitDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_TransportIndex(self):
        return self.TransportIndex
    def set_TransportIndex(self, TransportIndex):
        self.TransportIndex = TransportIndex
    def get_SurfaceReading(self):
        return self.SurfaceReading
    def set_SurfaceReading(self, SurfaceReading):
        self.SurfaceReading = SurfaceReading
    def get_CriticalitySafetyIndex(self):
        return self.CriticalitySafetyIndex
    def set_CriticalitySafetyIndex(self, CriticalitySafetyIndex):
        self.CriticalitySafetyIndex = CriticalitySafetyIndex
    def get_LabelType(self):
        return self.LabelType
    def set_LabelType(self, LabelType):
        self.LabelType = LabelType
    def validate_RadioactiveLabelType(self, value):
        result = True
        # Validate type RadioactiveLabelType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['III_YELLOW', 'II_YELLOW', 'I_WHITE']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on RadioactiveLabelType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.TransportIndex is not None or
            self.SurfaceReading is not None or
            self.CriticalitySafetyIndex is not None or
            self.LabelType is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RadioactiveDangerousGoodsHandlingUnitDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RadioactiveDangerousGoodsHandlingUnitDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RadioactiveDangerousGoodsHandlingUnitDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RadioactiveDangerousGoodsHandlingUnitDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RadioactiveDangerousGoodsHandlingUnitDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RadioactiveDangerousGoodsHandlingUnitDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RadioactiveDangerousGoodsHandlingUnitDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.TransportIndex is not None:
            namespaceprefix_ = self.TransportIndex_nsprefix_ + ':' if (UseCapturedNS_ and self.TransportIndex_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTransportIndex>%s</%sTransportIndex>%s' % (namespaceprefix_ , self.gds_format_decimal(self.TransportIndex, input_name='TransportIndex'), namespaceprefix_ , eol_))
        if self.SurfaceReading is not None:
            namespaceprefix_ = self.SurfaceReading_nsprefix_ + ':' if (UseCapturedNS_ and self.SurfaceReading_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSurfaceReading>%s</%sSurfaceReading>%s' % (namespaceprefix_ , self.gds_format_decimal(self.SurfaceReading, input_name='SurfaceReading'), namespaceprefix_ , eol_))
        if self.CriticalitySafetyIndex is not None:
            namespaceprefix_ = self.CriticalitySafetyIndex_nsprefix_ + ':' if (UseCapturedNS_ and self.CriticalitySafetyIndex_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCriticalitySafetyIndex>%s</%sCriticalitySafetyIndex>%s' % (namespaceprefix_ , self.gds_format_decimal(self.CriticalitySafetyIndex, input_name='CriticalitySafetyIndex'), namespaceprefix_ , eol_))
        if self.LabelType is not None:
            namespaceprefix_ = self.LabelType_nsprefix_ + ':' if (UseCapturedNS_ and self.LabelType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLabelType>%s</%sLabelType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LabelType), input_name='LabelType')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'TransportIndex' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'TransportIndex')
            fval_ = self.gds_validate_decimal(fval_, node, 'TransportIndex')
            self.TransportIndex = fval_
            self.TransportIndex_nsprefix_ = child_.prefix
        elif nodeName_ == 'SurfaceReading' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'SurfaceReading')
            fval_ = self.gds_validate_decimal(fval_, node, 'SurfaceReading')
            self.SurfaceReading = fval_
            self.SurfaceReading_nsprefix_ = child_.prefix
        elif nodeName_ == 'CriticalitySafetyIndex' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'CriticalitySafetyIndex')
            fval_ = self.gds_validate_decimal(fval_, node, 'CriticalitySafetyIndex')
            self.CriticalitySafetyIndex = fval_
            self.CriticalitySafetyIndex_nsprefix_ = child_.prefix
        elif nodeName_ == 'LabelType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LabelType')
            value_ = self.gds_validate_string(value_, node, 'LabelType')
            self.LabelType = value_
            self.LabelType_nsprefix_ = child_.prefix
            # validate type RadioactiveLabelType
            self.validate_RadioactiveLabelType(self.LabelType)
# end class RadioactiveDangerousGoodsHandlingUnitDetail


class RecordedDangerousGoodsHandlingUnitGroup(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, UploadedHandlingUnitGroup=None, HandlingUnitShippingDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.UploadedHandlingUnitGroup = UploadedHandlingUnitGroup
        self.UploadedHandlingUnitGroup_nsprefix_ = "ns"
        self.HandlingUnitShippingDetail = HandlingUnitShippingDetail
        self.HandlingUnitShippingDetail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RecordedDangerousGoodsHandlingUnitGroup)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RecordedDangerousGoodsHandlingUnitGroup.subclass:
            return RecordedDangerousGoodsHandlingUnitGroup.subclass(*args_, **kwargs_)
        else:
            return RecordedDangerousGoodsHandlingUnitGroup(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_UploadedHandlingUnitGroup(self):
        return self.UploadedHandlingUnitGroup
    def set_UploadedHandlingUnitGroup(self, UploadedHandlingUnitGroup):
        self.UploadedHandlingUnitGroup = UploadedHandlingUnitGroup
    def get_HandlingUnitShippingDetail(self):
        return self.HandlingUnitShippingDetail
    def set_HandlingUnitShippingDetail(self, HandlingUnitShippingDetail):
        self.HandlingUnitShippingDetail = HandlingUnitShippingDetail
    def hasContent_(self):
        if (
            self.UploadedHandlingUnitGroup is not None or
            self.HandlingUnitShippingDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RecordedDangerousGoodsHandlingUnitGroup', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RecordedDangerousGoodsHandlingUnitGroup')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RecordedDangerousGoodsHandlingUnitGroup':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RecordedDangerousGoodsHandlingUnitGroup')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RecordedDangerousGoodsHandlingUnitGroup', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RecordedDangerousGoodsHandlingUnitGroup'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RecordedDangerousGoodsHandlingUnitGroup', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.UploadedHandlingUnitGroup is not None:
            namespaceprefix_ = self.UploadedHandlingUnitGroup_nsprefix_ + ':' if (UseCapturedNS_ and self.UploadedHandlingUnitGroup_nsprefix_) else ''
            self.UploadedHandlingUnitGroup.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UploadedHandlingUnitGroup', pretty_print=pretty_print)
        if self.HandlingUnitShippingDetail is not None:
            namespaceprefix_ = self.HandlingUnitShippingDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.HandlingUnitShippingDetail_nsprefix_) else ''
            self.HandlingUnitShippingDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='HandlingUnitShippingDetail', pretty_print=pretty_print)
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
        if nodeName_ == 'UploadedHandlingUnitGroup':
            obj_ = UploadedDangerousGoodsHandlingUnitGroup.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UploadedHandlingUnitGroup = obj_
            obj_.original_tagname_ = 'UploadedHandlingUnitGroup'
        elif nodeName_ == 'HandlingUnitShippingDetail':
            obj_ = DangerousGoodsHandlingUnitShippingDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.HandlingUnitShippingDetail = obj_
            obj_.original_tagname_ = 'HandlingUnitShippingDetail'
# end class RecordedDangerousGoodsHandlingUnitGroup


class RecordedDangerousGoodsShipmentDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, UploadedShipmentDetail=None, CompletedShipmentDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.UploadedShipmentDetail = UploadedShipmentDetail
        self.UploadedShipmentDetail_nsprefix_ = "ns"
        self.CompletedShipmentDetail = CompletedShipmentDetail
        self.CompletedShipmentDetail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RecordedDangerousGoodsShipmentDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RecordedDangerousGoodsShipmentDetail.subclass:
            return RecordedDangerousGoodsShipmentDetail.subclass(*args_, **kwargs_)
        else:
            return RecordedDangerousGoodsShipmentDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_UploadedShipmentDetail(self):
        return self.UploadedShipmentDetail
    def set_UploadedShipmentDetail(self, UploadedShipmentDetail):
        self.UploadedShipmentDetail = UploadedShipmentDetail
    def get_CompletedShipmentDetail(self):
        return self.CompletedShipmentDetail
    def set_CompletedShipmentDetail(self, CompletedShipmentDetail):
        self.CompletedShipmentDetail = CompletedShipmentDetail
    def hasContent_(self):
        if (
            self.UploadedShipmentDetail is not None or
            self.CompletedShipmentDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RecordedDangerousGoodsShipmentDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RecordedDangerousGoodsShipmentDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RecordedDangerousGoodsShipmentDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RecordedDangerousGoodsShipmentDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RecordedDangerousGoodsShipmentDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RecordedDangerousGoodsShipmentDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RecordedDangerousGoodsShipmentDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.UploadedShipmentDetail is not None:
            namespaceprefix_ = self.UploadedShipmentDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.UploadedShipmentDetail_nsprefix_) else ''
            self.UploadedShipmentDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UploadedShipmentDetail', pretty_print=pretty_print)
        if self.CompletedShipmentDetail is not None:
            namespaceprefix_ = self.CompletedShipmentDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.CompletedShipmentDetail_nsprefix_) else ''
            self.CompletedShipmentDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CompletedShipmentDetail', pretty_print=pretty_print)
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
        if nodeName_ == 'UploadedShipmentDetail':
            obj_ = UploadedDangerousGoodsShipmentDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UploadedShipmentDetail = obj_
            obj_.original_tagname_ = 'UploadedShipmentDetail'
        elif nodeName_ == 'CompletedShipmentDetail':
            obj_ = CompletedDangerousGoodsShipmentDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CompletedShipmentDetail = obj_
            obj_.original_tagname_ = 'CompletedShipmentDetail'
# end class RecordedDangerousGoodsShipmentDetail


class RetrieveDangerousGoodsReply(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, ShipmentDetail=None, HandlingUnitGroups=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.HighestSeverity = HighestSeverity
        self.validate_NotificationSeverityType(self.HighestSeverity)
        self.HighestSeverity_nsprefix_ = "ns"
        if Notifications is None:
            self.Notifications = []
        else:
            self.Notifications = Notifications
        self.Notifications_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.ShipmentDetail = ShipmentDetail
        self.ShipmentDetail_nsprefix_ = "ns"
        if HandlingUnitGroups is None:
            self.HandlingUnitGroups = []
        else:
            self.HandlingUnitGroups = HandlingUnitGroups
        self.HandlingUnitGroups_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RetrieveDangerousGoodsReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RetrieveDangerousGoodsReply.subclass:
            return RetrieveDangerousGoodsReply.subclass(*args_, **kwargs_)
        else:
            return RetrieveDangerousGoodsReply(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_HighestSeverity(self):
        return self.HighestSeverity
    def set_HighestSeverity(self, HighestSeverity):
        self.HighestSeverity = HighestSeverity
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def add_Notifications(self, value):
        self.Notifications.append(value)
    def insert_Notifications_at(self, index, value):
        self.Notifications.insert(index, value)
    def replace_Notifications_at(self, index, value):
        self.Notifications[index] = value
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_ShipmentDetail(self):
        return self.ShipmentDetail
    def set_ShipmentDetail(self, ShipmentDetail):
        self.ShipmentDetail = ShipmentDetail
    def get_HandlingUnitGroups(self):
        return self.HandlingUnitGroups
    def set_HandlingUnitGroups(self, HandlingUnitGroups):
        self.HandlingUnitGroups = HandlingUnitGroups
    def add_HandlingUnitGroups(self, value):
        self.HandlingUnitGroups.append(value)
    def insert_HandlingUnitGroups_at(self, index, value):
        self.HandlingUnitGroups.insert(index, value)
    def replace_HandlingUnitGroups_at(self, index, value):
        self.HandlingUnitGroups[index] = value
    def validate_NotificationSeverityType(self, value):
        result = True
        # Validate type NotificationSeverityType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ERROR', 'FAILURE', 'NOTE', 'SUCCESS', 'WARNING']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on NotificationSeverityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.HighestSeverity is not None or
            self.Notifications or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.ShipmentDetail is not None or
            self.HandlingUnitGroups
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RetrieveDangerousGoodsReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RetrieveDangerousGoodsReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RetrieveDangerousGoodsReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RetrieveDangerousGoodsReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RetrieveDangerousGoodsReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RetrieveDangerousGoodsReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RetrieveDangerousGoodsReply', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.HighestSeverity is not None:
            namespaceprefix_ = self.HighestSeverity_nsprefix_ + ':' if (UseCapturedNS_ and self.HighestSeverity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHighestSeverity>%s</%sHighestSeverity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HighestSeverity), input_name='HighestSeverity')), namespaceprefix_ , eol_))
        for Notifications_ in self.Notifications:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            Notifications_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.ShipmentDetail is not None:
            namespaceprefix_ = self.ShipmentDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentDetail_nsprefix_) else ''
            self.ShipmentDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentDetail', pretty_print=pretty_print)
        for HandlingUnitGroups_ in self.HandlingUnitGroups:
            namespaceprefix_ = self.HandlingUnitGroups_nsprefix_ + ':' if (UseCapturedNS_ and self.HandlingUnitGroups_nsprefix_) else ''
            HandlingUnitGroups_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='HandlingUnitGroups', pretty_print=pretty_print)
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
        if nodeName_ == 'HighestSeverity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HighestSeverity')
            value_ = self.gds_validate_string(value_, node, 'HighestSeverity')
            self.HighestSeverity = value_
            self.HighestSeverity_nsprefix_ = child_.prefix
            # validate type NotificationSeverityType
            self.validate_NotificationSeverityType(self.HighestSeverity)
        elif nodeName_ == 'Notifications':
            obj_ = Notification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications.append(obj_)
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'ShipmentDetail':
            obj_ = RecordedDangerousGoodsShipmentDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentDetail = obj_
            obj_.original_tagname_ = 'ShipmentDetail'
        elif nodeName_ == 'HandlingUnitGroups':
            obj_ = RecordedDangerousGoodsHandlingUnitGroup.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.HandlingUnitGroups.append(obj_)
            obj_.original_tagname_ = 'HandlingUnitGroups'
# end class RetrieveDangerousGoodsReply


class RetrieveDangerousGoodsRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, TransactionDetail=None, Version=None, UploadId=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.WebAuthenticationDetail = WebAuthenticationDetail
        self.WebAuthenticationDetail_nsprefix_ = "ns"
        self.ClientDetail = ClientDetail
        self.ClientDetail_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.UploadId = UploadId
        self.UploadId_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RetrieveDangerousGoodsRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RetrieveDangerousGoodsRequest.subclass:
            return RetrieveDangerousGoodsRequest.subclass(*args_, **kwargs_)
        else:
            return RetrieveDangerousGoodsRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_WebAuthenticationDetail(self):
        return self.WebAuthenticationDetail
    def set_WebAuthenticationDetail(self, WebAuthenticationDetail):
        self.WebAuthenticationDetail = WebAuthenticationDetail
    def get_ClientDetail(self):
        return self.ClientDetail
    def set_ClientDetail(self, ClientDetail):
        self.ClientDetail = ClientDetail
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_UploadId(self):
        return self.UploadId
    def set_UploadId(self, UploadId):
        self.UploadId = UploadId
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.UploadId is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RetrieveDangerousGoodsRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RetrieveDangerousGoodsRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RetrieveDangerousGoodsRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RetrieveDangerousGoodsRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RetrieveDangerousGoodsRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RetrieveDangerousGoodsRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RetrieveDangerousGoodsRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.WebAuthenticationDetail is not None:
            namespaceprefix_ = self.WebAuthenticationDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.WebAuthenticationDetail_nsprefix_) else ''
            self.WebAuthenticationDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='WebAuthenticationDetail', pretty_print=pretty_print)
        if self.ClientDetail is not None:
            namespaceprefix_ = self.ClientDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientDetail_nsprefix_) else ''
            self.ClientDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClientDetail', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.UploadId is not None:
            namespaceprefix_ = self.UploadId_nsprefix_ + ':' if (UseCapturedNS_ and self.UploadId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUploadId>%s</%sUploadId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UploadId), input_name='UploadId')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'WebAuthenticationDetail':
            obj_ = WebAuthenticationDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.WebAuthenticationDetail = obj_
            obj_.original_tagname_ = 'WebAuthenticationDetail'
        elif nodeName_ == 'ClientDetail':
            obj_ = ClientDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClientDetail = obj_
            obj_.original_tagname_ = 'ClientDetail'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'UploadId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UploadId')
            value_ = self.gds_validate_string(value_, node, 'UploadId')
            self.UploadId = value_
            self.UploadId_nsprefix_ = child_.prefix
# end class RetrieveDangerousGoodsRequest


class ShipmentDryIceDetail(GeneratedsSuper):
    """Shipment-level totals of dry ice data across all packages."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PackageCount=None, TotalWeight=None, ProcessingOptions=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PackageCount = PackageCount
        self.PackageCount_nsprefix_ = None
        self.TotalWeight = TotalWeight
        self.TotalWeight_nsprefix_ = "ns"
        self.ProcessingOptions = ProcessingOptions
        self.ProcessingOptions_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentDryIceDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentDryIceDetail.subclass:
            return ShipmentDryIceDetail.subclass(*args_, **kwargs_)
        else:
            return ShipmentDryIceDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PackageCount(self):
        return self.PackageCount
    def set_PackageCount(self, PackageCount):
        self.PackageCount = PackageCount
    def get_TotalWeight(self):
        return self.TotalWeight
    def set_TotalWeight(self, TotalWeight):
        self.TotalWeight = TotalWeight
    def get_ProcessingOptions(self):
        return self.ProcessingOptions
    def set_ProcessingOptions(self, ProcessingOptions):
        self.ProcessingOptions = ProcessingOptions
    def hasContent_(self):
        if (
            self.PackageCount is not None or
            self.TotalWeight is not None or
            self.ProcessingOptions is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentDryIceDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentDryIceDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentDryIceDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentDryIceDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentDryIceDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentDryIceDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentDryIceDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PackageCount is not None:
            namespaceprefix_ = self.PackageCount_nsprefix_ + ':' if (UseCapturedNS_ and self.PackageCount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPackageCount>%s</%sPackageCount>%s' % (namespaceprefix_ , self.gds_format_integer(self.PackageCount, input_name='PackageCount'), namespaceprefix_ , eol_))
        if self.TotalWeight is not None:
            namespaceprefix_ = self.TotalWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.TotalWeight_nsprefix_) else ''
            self.TotalWeight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TotalWeight', pretty_print=pretty_print)
        if self.ProcessingOptions is not None:
            namespaceprefix_ = self.ProcessingOptions_nsprefix_ + ':' if (UseCapturedNS_ and self.ProcessingOptions_nsprefix_) else ''
            self.ProcessingOptions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ProcessingOptions', pretty_print=pretty_print)
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
        if nodeName_ == 'PackageCount' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'PackageCount')
            if ival_ < 0:
                raise_parse_error(child_, 'requires nonNegativeInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'PackageCount')
            self.PackageCount = ival_
            self.PackageCount_nsprefix_ = child_.prefix
        elif nodeName_ == 'TotalWeight':
            obj_ = Weight.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TotalWeight = obj_
            obj_.original_tagname_ = 'TotalWeight'
        elif nodeName_ == 'ProcessingOptions':
            obj_ = ShipmentDryIceProcessingOptionsRequested.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ProcessingOptions = obj_
            obj_.original_tagname_ = 'ProcessingOptions'
# end class ShipmentDryIceDetail


class ShipmentDryIceProcessingOptionsRequested(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Options=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Options is None:
            self.Options = []
        else:
            self.Options = Options
        self.Options_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentDryIceProcessingOptionsRequested)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentDryIceProcessingOptionsRequested.subclass:
            return ShipmentDryIceProcessingOptionsRequested.subclass(*args_, **kwargs_)
        else:
            return ShipmentDryIceProcessingOptionsRequested(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Options(self):
        return self.Options
    def set_Options(self, Options):
        self.Options = Options
    def add_Options(self, value):
        self.Options.append(value)
    def insert_Options_at(self, index, value):
        self.Options.insert(index, value)
    def replace_Options_at(self, index, value):
        self.Options[index] = value
    def validate_ShipmentDryIceProcessingOptionType(self, value):
        result = True
        # Validate type ShipmentDryIceProcessingOptionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['SHIPMENT_LEVEL_DRY_ICE_ONLY']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ShipmentDryIceProcessingOptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Options
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentDryIceProcessingOptionsRequested', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentDryIceProcessingOptionsRequested')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentDryIceProcessingOptionsRequested':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentDryIceProcessingOptionsRequested')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentDryIceProcessingOptionsRequested', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentDryIceProcessingOptionsRequested'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentDryIceProcessingOptionsRequested', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Options_ in self.Options:
            namespaceprefix_ = self.Options_nsprefix_ + ':' if (UseCapturedNS_ and self.Options_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOptions>%s</%sOptions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Options_), input_name='Options')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Options':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Options')
            value_ = self.gds_validate_string(value_, node, 'Options')
            self.Options.append(value_)
            self.Options_nsprefix_ = child_.prefix
            # validate type ShipmentDryIceProcessingOptionType
            self.validate_ShipmentDryIceProcessingOptionType(self.Options[-1])
# end class ShipmentDryIceProcessingOptionsRequested


class TrackingId(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TrackingIdType=None, FormId=None, UspsApplicationId=None, TrackingNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.TrackingIdType = TrackingIdType
        self.validate_TrackingIdType(self.TrackingIdType)
        self.TrackingIdType_nsprefix_ = "ns"
        self.FormId = FormId
        self.FormId_nsprefix_ = None
        self.UspsApplicationId = UspsApplicationId
        self.UspsApplicationId_nsprefix_ = None
        self.TrackingNumber = TrackingNumber
        self.TrackingNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TrackingId)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TrackingId.subclass:
            return TrackingId.subclass(*args_, **kwargs_)
        else:
            return TrackingId(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_TrackingIdType(self):
        return self.TrackingIdType
    def set_TrackingIdType(self, TrackingIdType):
        self.TrackingIdType = TrackingIdType
    def get_FormId(self):
        return self.FormId
    def set_FormId(self, FormId):
        self.FormId = FormId
    def get_UspsApplicationId(self):
        return self.UspsApplicationId
    def set_UspsApplicationId(self, UspsApplicationId):
        self.UspsApplicationId = UspsApplicationId
    def get_TrackingNumber(self):
        return self.TrackingNumber
    def set_TrackingNumber(self, TrackingNumber):
        self.TrackingNumber = TrackingNumber
    def validate_TrackingIdType(self, value):
        result = True
        # Validate type TrackingIdType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['EXPRESS', 'FEDEX', 'FREIGHT', 'GROUND', 'INTERNAL', 'UNKNOWN', 'USPS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on TrackingIdType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.TrackingIdType is not None or
            self.FormId is not None or
            self.UspsApplicationId is not None or
            self.TrackingNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackingId', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TrackingId')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TrackingId':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TrackingId')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TrackingId', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TrackingId'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackingId', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.TrackingIdType is not None:
            namespaceprefix_ = self.TrackingIdType_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackingIdType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTrackingIdType>%s</%sTrackingIdType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TrackingIdType), input_name='TrackingIdType')), namespaceprefix_ , eol_))
        if self.FormId is not None:
            namespaceprefix_ = self.FormId_nsprefix_ + ':' if (UseCapturedNS_ and self.FormId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFormId>%s</%sFormId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FormId), input_name='FormId')), namespaceprefix_ , eol_))
        if self.UspsApplicationId is not None:
            namespaceprefix_ = self.UspsApplicationId_nsprefix_ + ':' if (UseCapturedNS_ and self.UspsApplicationId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUspsApplicationId>%s</%sUspsApplicationId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UspsApplicationId), input_name='UspsApplicationId')), namespaceprefix_ , eol_))
        if self.TrackingNumber is not None:
            namespaceprefix_ = self.TrackingNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackingNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTrackingNumber>%s</%sTrackingNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TrackingNumber), input_name='TrackingNumber')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'TrackingIdType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TrackingIdType')
            value_ = self.gds_validate_string(value_, node, 'TrackingIdType')
            self.TrackingIdType = value_
            self.TrackingIdType_nsprefix_ = child_.prefix
            # validate type TrackingIdType
            self.validate_TrackingIdType(self.TrackingIdType)
        elif nodeName_ == 'FormId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FormId')
            value_ = self.gds_validate_string(value_, node, 'FormId')
            self.FormId = value_
            self.FormId_nsprefix_ = child_.prefix
        elif nodeName_ == 'UspsApplicationId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UspsApplicationId')
            value_ = self.gds_validate_string(value_, node, 'UspsApplicationId')
            self.UspsApplicationId = value_
            self.UspsApplicationId_nsprefix_ = child_.prefix
        elif nodeName_ == 'TrackingNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TrackingNumber')
            value_ = self.gds_validate_string(value_, node, 'TrackingNumber')
            self.TrackingNumber = value_
            self.TrackingNumber_nsprefix_ = child_.prefix
# end class TrackingId


class TrackingNumberUnit(GeneratedsSuper):
    """Each instance of this class groups together TrackingId instances that
    pertain to the same entity (e.g. package)."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, SequenceNumber=None, TrackingIds=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.SequenceNumber = SequenceNumber
        self.SequenceNumber_nsprefix_ = None
        if TrackingIds is None:
            self.TrackingIds = []
        else:
            self.TrackingIds = TrackingIds
        self.TrackingIds_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TrackingNumberUnit)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TrackingNumberUnit.subclass:
            return TrackingNumberUnit.subclass(*args_, **kwargs_)
        else:
            return TrackingNumberUnit(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_SequenceNumber(self):
        return self.SequenceNumber
    def set_SequenceNumber(self, SequenceNumber):
        self.SequenceNumber = SequenceNumber
    def get_TrackingIds(self):
        return self.TrackingIds
    def set_TrackingIds(self, TrackingIds):
        self.TrackingIds = TrackingIds
    def add_TrackingIds(self, value):
        self.TrackingIds.append(value)
    def insert_TrackingIds_at(self, index, value):
        self.TrackingIds.insert(index, value)
    def replace_TrackingIds_at(self, index, value):
        self.TrackingIds[index] = value
    def hasContent_(self):
        if (
            self.SequenceNumber is not None or
            self.TrackingIds
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackingNumberUnit', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TrackingNumberUnit')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TrackingNumberUnit':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TrackingNumberUnit')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TrackingNumberUnit', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TrackingNumberUnit'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackingNumberUnit', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.SequenceNumber is not None:
            namespaceprefix_ = self.SequenceNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.SequenceNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSequenceNumber>%s</%sSequenceNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.SequenceNumber, input_name='SequenceNumber'), namespaceprefix_ , eol_))
        for TrackingIds_ in self.TrackingIds:
            namespaceprefix_ = self.TrackingIds_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackingIds_nsprefix_) else ''
            TrackingIds_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TrackingIds', pretty_print=pretty_print)
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
        if nodeName_ == 'SequenceNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'SequenceNumber')
            if ival_ < 0:
                raise_parse_error(child_, 'requires nonNegativeInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'SequenceNumber')
            self.SequenceNumber = ival_
            self.SequenceNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'TrackingIds':
            obj_ = TrackingId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TrackingIds.append(obj_)
            obj_.original_tagname_ = 'TrackingIds'
# end class TrackingNumberUnit


class TransactionDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CustomerTransactionId=None, Localization=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CustomerTransactionId = CustomerTransactionId
        self.CustomerTransactionId_nsprefix_ = None
        self.Localization = Localization
        self.Localization_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TransactionDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TransactionDetail.subclass:
            return TransactionDetail.subclass(*args_, **kwargs_)
        else:
            return TransactionDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CustomerTransactionId(self):
        return self.CustomerTransactionId
    def set_CustomerTransactionId(self, CustomerTransactionId):
        self.CustomerTransactionId = CustomerTransactionId
    def get_Localization(self):
        return self.Localization
    def set_Localization(self, Localization):
        self.Localization = Localization
    def hasContent_(self):
        if (
            self.CustomerTransactionId is not None or
            self.Localization is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TransactionDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TransactionDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TransactionDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TransactionDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TransactionDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TransactionDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TransactionDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CustomerTransactionId is not None:
            namespaceprefix_ = self.CustomerTransactionId_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomerTransactionId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustomerTransactionId>%s</%sCustomerTransactionId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CustomerTransactionId), input_name='CustomerTransactionId')), namespaceprefix_ , eol_))
        if self.Localization is not None:
            namespaceprefix_ = self.Localization_nsprefix_ + ':' if (UseCapturedNS_ and self.Localization_nsprefix_) else ''
            self.Localization.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Localization', pretty_print=pretty_print)
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
        if nodeName_ == 'CustomerTransactionId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CustomerTransactionId')
            value_ = self.gds_validate_string(value_, node, 'CustomerTransactionId')
            self.CustomerTransactionId = value_
            self.CustomerTransactionId_nsprefix_ = child_.prefix
        elif nodeName_ == 'Localization':
            obj_ = Localization.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Localization = obj_
            obj_.original_tagname_ = 'Localization'
# end class TransactionDetail


class UploadDangerousGoodsProcessingOptionsRequested(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Options=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Options is None:
            self.Options = []
        else:
            self.Options = Options
        self.Options_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UploadDangerousGoodsProcessingOptionsRequested)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UploadDangerousGoodsProcessingOptionsRequested.subclass:
            return UploadDangerousGoodsProcessingOptionsRequested.subclass(*args_, **kwargs_)
        else:
            return UploadDangerousGoodsProcessingOptionsRequested(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Options(self):
        return self.Options
    def set_Options(self, Options):
        self.Options = Options
    def add_Options(self, value):
        self.Options.append(value)
    def insert_Options_at(self, index, value):
        self.Options.insert(index, value)
    def replace_Options_at(self, index, value):
        self.Options[index] = value
    def validate_UploadDangerousGoodsProcessingOptionType(self, value):
        result = True
        # Validate type UploadDangerousGoodsProcessingOptionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['VALIDATION_ERRORS_AS_WARNINGS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on UploadDangerousGoodsProcessingOptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Options
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadDangerousGoodsProcessingOptionsRequested', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UploadDangerousGoodsProcessingOptionsRequested')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UploadDangerousGoodsProcessingOptionsRequested':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UploadDangerousGoodsProcessingOptionsRequested')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UploadDangerousGoodsProcessingOptionsRequested', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UploadDangerousGoodsProcessingOptionsRequested'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadDangerousGoodsProcessingOptionsRequested', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Options_ in self.Options:
            namespaceprefix_ = self.Options_nsprefix_ + ':' if (UseCapturedNS_ and self.Options_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOptions>%s</%sOptions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Options_), input_name='Options')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Options':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Options')
            value_ = self.gds_validate_string(value_, node, 'Options')
            self.Options.append(value_)
            self.Options_nsprefix_ = child_.prefix
            # validate type UploadDangerousGoodsProcessingOptionType
            self.validate_UploadDangerousGoodsProcessingOptionType(self.Options[-1])
# end class UploadDangerousGoodsProcessingOptionsRequested


class UploadDangerousGoodsReply(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, UploadId=None, MasterTrackingId=None, CompletedShipmentDetail=None, CompletedHandlingUnitGroups=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.HighestSeverity = HighestSeverity
        self.validate_NotificationSeverityType(self.HighestSeverity)
        self.HighestSeverity_nsprefix_ = "ns"
        if Notifications is None:
            self.Notifications = []
        else:
            self.Notifications = Notifications
        self.Notifications_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.UploadId = UploadId
        self.UploadId_nsprefix_ = None
        self.MasterTrackingId = MasterTrackingId
        self.MasterTrackingId_nsprefix_ = "ns"
        self.CompletedShipmentDetail = CompletedShipmentDetail
        self.CompletedShipmentDetail_nsprefix_ = "ns"
        if CompletedHandlingUnitGroups is None:
            self.CompletedHandlingUnitGroups = []
        else:
            self.CompletedHandlingUnitGroups = CompletedHandlingUnitGroups
        self.CompletedHandlingUnitGroups_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UploadDangerousGoodsReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UploadDangerousGoodsReply.subclass:
            return UploadDangerousGoodsReply.subclass(*args_, **kwargs_)
        else:
            return UploadDangerousGoodsReply(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_HighestSeverity(self):
        return self.HighestSeverity
    def set_HighestSeverity(self, HighestSeverity):
        self.HighestSeverity = HighestSeverity
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def add_Notifications(self, value):
        self.Notifications.append(value)
    def insert_Notifications_at(self, index, value):
        self.Notifications.insert(index, value)
    def replace_Notifications_at(self, index, value):
        self.Notifications[index] = value
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_UploadId(self):
        return self.UploadId
    def set_UploadId(self, UploadId):
        self.UploadId = UploadId
    def get_MasterTrackingId(self):
        return self.MasterTrackingId
    def set_MasterTrackingId(self, MasterTrackingId):
        self.MasterTrackingId = MasterTrackingId
    def get_CompletedShipmentDetail(self):
        return self.CompletedShipmentDetail
    def set_CompletedShipmentDetail(self, CompletedShipmentDetail):
        self.CompletedShipmentDetail = CompletedShipmentDetail
    def get_CompletedHandlingUnitGroups(self):
        return self.CompletedHandlingUnitGroups
    def set_CompletedHandlingUnitGroups(self, CompletedHandlingUnitGroups):
        self.CompletedHandlingUnitGroups = CompletedHandlingUnitGroups
    def add_CompletedHandlingUnitGroups(self, value):
        self.CompletedHandlingUnitGroups.append(value)
    def insert_CompletedHandlingUnitGroups_at(self, index, value):
        self.CompletedHandlingUnitGroups.insert(index, value)
    def replace_CompletedHandlingUnitGroups_at(self, index, value):
        self.CompletedHandlingUnitGroups[index] = value
    def validate_NotificationSeverityType(self, value):
        result = True
        # Validate type NotificationSeverityType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ERROR', 'FAILURE', 'NOTE', 'SUCCESS', 'WARNING']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on NotificationSeverityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.HighestSeverity is not None or
            self.Notifications or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.UploadId is not None or
            self.MasterTrackingId is not None or
            self.CompletedShipmentDetail is not None or
            self.CompletedHandlingUnitGroups
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadDangerousGoodsReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UploadDangerousGoodsReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UploadDangerousGoodsReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UploadDangerousGoodsReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UploadDangerousGoodsReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UploadDangerousGoodsReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadDangerousGoodsReply', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.HighestSeverity is not None:
            namespaceprefix_ = self.HighestSeverity_nsprefix_ + ':' if (UseCapturedNS_ and self.HighestSeverity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHighestSeverity>%s</%sHighestSeverity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HighestSeverity), input_name='HighestSeverity')), namespaceprefix_ , eol_))
        for Notifications_ in self.Notifications:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            Notifications_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.UploadId is not None:
            namespaceprefix_ = self.UploadId_nsprefix_ + ':' if (UseCapturedNS_ and self.UploadId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUploadId>%s</%sUploadId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UploadId), input_name='UploadId')), namespaceprefix_ , eol_))
        if self.MasterTrackingId is not None:
            namespaceprefix_ = self.MasterTrackingId_nsprefix_ + ':' if (UseCapturedNS_ and self.MasterTrackingId_nsprefix_) else ''
            self.MasterTrackingId.export(outfile, level, namespaceprefix_, namespacedef_='', name_='MasterTrackingId', pretty_print=pretty_print)
        if self.CompletedShipmentDetail is not None:
            namespaceprefix_ = self.CompletedShipmentDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.CompletedShipmentDetail_nsprefix_) else ''
            self.CompletedShipmentDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CompletedShipmentDetail', pretty_print=pretty_print)
        for CompletedHandlingUnitGroups_ in self.CompletedHandlingUnitGroups:
            namespaceprefix_ = self.CompletedHandlingUnitGroups_nsprefix_ + ':' if (UseCapturedNS_ and self.CompletedHandlingUnitGroups_nsprefix_) else ''
            CompletedHandlingUnitGroups_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CompletedHandlingUnitGroups', pretty_print=pretty_print)
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
        if nodeName_ == 'HighestSeverity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HighestSeverity')
            value_ = self.gds_validate_string(value_, node, 'HighestSeverity')
            self.HighestSeverity = value_
            self.HighestSeverity_nsprefix_ = child_.prefix
            # validate type NotificationSeverityType
            self.validate_NotificationSeverityType(self.HighestSeverity)
        elif nodeName_ == 'Notifications':
            obj_ = Notification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications.append(obj_)
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'UploadId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UploadId')
            value_ = self.gds_validate_string(value_, node, 'UploadId')
            self.UploadId = value_
            self.UploadId_nsprefix_ = child_.prefix
        elif nodeName_ == 'MasterTrackingId':
            obj_ = TrackingId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.MasterTrackingId = obj_
            obj_.original_tagname_ = 'MasterTrackingId'
        elif nodeName_ == 'CompletedShipmentDetail':
            obj_ = CompletedDangerousGoodsShipmentDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CompletedShipmentDetail = obj_
            obj_.original_tagname_ = 'CompletedShipmentDetail'
        elif nodeName_ == 'CompletedHandlingUnitGroups':
            obj_ = CompletedDangerousGoodsHandlingUnitGroup.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CompletedHandlingUnitGroups.append(obj_)
            obj_.original_tagname_ = 'CompletedHandlingUnitGroups'
# end class UploadDangerousGoodsReply


class UploadDangerousGoodsRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, TransactionDetail=None, Version=None, ProcessingOptions=None, ShipmentDetail=None, HandlingUnitGroups=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.WebAuthenticationDetail = WebAuthenticationDetail
        self.WebAuthenticationDetail_nsprefix_ = "ns"
        self.ClientDetail = ClientDetail
        self.ClientDetail_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.ProcessingOptions = ProcessingOptions
        self.ProcessingOptions_nsprefix_ = "ns"
        self.ShipmentDetail = ShipmentDetail
        self.ShipmentDetail_nsprefix_ = "ns"
        if HandlingUnitGroups is None:
            self.HandlingUnitGroups = []
        else:
            self.HandlingUnitGroups = HandlingUnitGroups
        self.HandlingUnitGroups_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UploadDangerousGoodsRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UploadDangerousGoodsRequest.subclass:
            return UploadDangerousGoodsRequest.subclass(*args_, **kwargs_)
        else:
            return UploadDangerousGoodsRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_WebAuthenticationDetail(self):
        return self.WebAuthenticationDetail
    def set_WebAuthenticationDetail(self, WebAuthenticationDetail):
        self.WebAuthenticationDetail = WebAuthenticationDetail
    def get_ClientDetail(self):
        return self.ClientDetail
    def set_ClientDetail(self, ClientDetail):
        self.ClientDetail = ClientDetail
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_ProcessingOptions(self):
        return self.ProcessingOptions
    def set_ProcessingOptions(self, ProcessingOptions):
        self.ProcessingOptions = ProcessingOptions
    def get_ShipmentDetail(self):
        return self.ShipmentDetail
    def set_ShipmentDetail(self, ShipmentDetail):
        self.ShipmentDetail = ShipmentDetail
    def get_HandlingUnitGroups(self):
        return self.HandlingUnitGroups
    def set_HandlingUnitGroups(self, HandlingUnitGroups):
        self.HandlingUnitGroups = HandlingUnitGroups
    def add_HandlingUnitGroups(self, value):
        self.HandlingUnitGroups.append(value)
    def insert_HandlingUnitGroups_at(self, index, value):
        self.HandlingUnitGroups.insert(index, value)
    def replace_HandlingUnitGroups_at(self, index, value):
        self.HandlingUnitGroups[index] = value
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.ProcessingOptions is not None or
            self.ShipmentDetail is not None or
            self.HandlingUnitGroups
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadDangerousGoodsRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UploadDangerousGoodsRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UploadDangerousGoodsRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UploadDangerousGoodsRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UploadDangerousGoodsRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UploadDangerousGoodsRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadDangerousGoodsRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.WebAuthenticationDetail is not None:
            namespaceprefix_ = self.WebAuthenticationDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.WebAuthenticationDetail_nsprefix_) else ''
            self.WebAuthenticationDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='WebAuthenticationDetail', pretty_print=pretty_print)
        if self.ClientDetail is not None:
            namespaceprefix_ = self.ClientDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientDetail_nsprefix_) else ''
            self.ClientDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClientDetail', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.ProcessingOptions is not None:
            namespaceprefix_ = self.ProcessingOptions_nsprefix_ + ':' if (UseCapturedNS_ and self.ProcessingOptions_nsprefix_) else ''
            self.ProcessingOptions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ProcessingOptions', pretty_print=pretty_print)
        if self.ShipmentDetail is not None:
            namespaceprefix_ = self.ShipmentDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentDetail_nsprefix_) else ''
            self.ShipmentDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentDetail', pretty_print=pretty_print)
        for HandlingUnitGroups_ in self.HandlingUnitGroups:
            namespaceprefix_ = self.HandlingUnitGroups_nsprefix_ + ':' if (UseCapturedNS_ and self.HandlingUnitGroups_nsprefix_) else ''
            HandlingUnitGroups_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='HandlingUnitGroups', pretty_print=pretty_print)
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
        if nodeName_ == 'WebAuthenticationDetail':
            obj_ = WebAuthenticationDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.WebAuthenticationDetail = obj_
            obj_.original_tagname_ = 'WebAuthenticationDetail'
        elif nodeName_ == 'ClientDetail':
            obj_ = ClientDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClientDetail = obj_
            obj_.original_tagname_ = 'ClientDetail'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'ProcessingOptions':
            obj_ = UploadDangerousGoodsProcessingOptionsRequested.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ProcessingOptions = obj_
            obj_.original_tagname_ = 'ProcessingOptions'
        elif nodeName_ == 'ShipmentDetail':
            obj_ = UploadedDangerousGoodsShipmentDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentDetail = obj_
            obj_.original_tagname_ = 'ShipmentDetail'
        elif nodeName_ == 'HandlingUnitGroups':
            obj_ = UploadedDangerousGoodsHandlingUnitGroup.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.HandlingUnitGroups.append(obj_)
            obj_.original_tagname_ = 'HandlingUnitGroups'
# end class UploadDangerousGoodsRequest


class UploadedDangerousGoodsCommodityContent(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Description=None, Quantity=None, InnerReceptacles=None, RadionuclideDetail=None, NetExplosiveDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = "ns"
        self.Quantity = Quantity
        self.Quantity_nsprefix_ = "ns"
        if InnerReceptacles is None:
            self.InnerReceptacles = []
        else:
            self.InnerReceptacles = InnerReceptacles
        self.InnerReceptacles_nsprefix_ = "ns"
        self.RadionuclideDetail = RadionuclideDetail
        self.RadionuclideDetail_nsprefix_ = "ns"
        self.NetExplosiveDetail = NetExplosiveDetail
        self.NetExplosiveDetail_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UploadedDangerousGoodsCommodityContent)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UploadedDangerousGoodsCommodityContent.subclass:
            return UploadedDangerousGoodsCommodityContent.subclass(*args_, **kwargs_)
        else:
            return UploadedDangerousGoodsCommodityContent(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def get_Quantity(self):
        return self.Quantity
    def set_Quantity(self, Quantity):
        self.Quantity = Quantity
    def get_InnerReceptacles(self):
        return self.InnerReceptacles
    def set_InnerReceptacles(self, InnerReceptacles):
        self.InnerReceptacles = InnerReceptacles
    def add_InnerReceptacles(self, value):
        self.InnerReceptacles.append(value)
    def insert_InnerReceptacles_at(self, index, value):
        self.InnerReceptacles.insert(index, value)
    def replace_InnerReceptacles_at(self, index, value):
        self.InnerReceptacles[index] = value
    def get_RadionuclideDetail(self):
        return self.RadionuclideDetail
    def set_RadionuclideDetail(self, RadionuclideDetail):
        self.RadionuclideDetail = RadionuclideDetail
    def get_NetExplosiveDetail(self):
        return self.NetExplosiveDetail
    def set_NetExplosiveDetail(self, NetExplosiveDetail):
        self.NetExplosiveDetail = NetExplosiveDetail
    def hasContent_(self):
        if (
            self.Description is not None or
            self.Quantity is not None or
            self.InnerReceptacles or
            self.RadionuclideDetail is not None or
            self.NetExplosiveDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadedDangerousGoodsCommodityContent', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UploadedDangerousGoodsCommodityContent')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UploadedDangerousGoodsCommodityContent':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UploadedDangerousGoodsCommodityContent')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UploadedDangerousGoodsCommodityContent', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UploadedDangerousGoodsCommodityContent'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadedDangerousGoodsCommodityContent', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            self.Description.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Description', pretty_print=pretty_print)
        if self.Quantity is not None:
            namespaceprefix_ = self.Quantity_nsprefix_ + ':' if (UseCapturedNS_ and self.Quantity_nsprefix_) else ''
            self.Quantity.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Quantity', pretty_print=pretty_print)
        for InnerReceptacles_ in self.InnerReceptacles:
            namespaceprefix_ = self.InnerReceptacles_nsprefix_ + ':' if (UseCapturedNS_ and self.InnerReceptacles_nsprefix_) else ''
            InnerReceptacles_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='InnerReceptacles', pretty_print=pretty_print)
        if self.RadionuclideDetail is not None:
            namespaceprefix_ = self.RadionuclideDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.RadionuclideDetail_nsprefix_) else ''
            self.RadionuclideDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='RadionuclideDetail', pretty_print=pretty_print)
        if self.NetExplosiveDetail is not None:
            namespaceprefix_ = self.NetExplosiveDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.NetExplosiveDetail_nsprefix_) else ''
            self.NetExplosiveDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='NetExplosiveDetail', pretty_print=pretty_print)
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
        if nodeName_ == 'Description':
            obj_ = UploadedDangerousGoodsCommodityDescription.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Description = obj_
            obj_.original_tagname_ = 'Description'
        elif nodeName_ == 'Quantity':
            obj_ = PreciseQuantity.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Quantity = obj_
            obj_.original_tagname_ = 'Quantity'
        elif nodeName_ == 'InnerReceptacles':
            obj_ = DangerousGoodsInnerReceptacleDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.InnerReceptacles.append(obj_)
            obj_.original_tagname_ = 'InnerReceptacles'
        elif nodeName_ == 'RadionuclideDetail':
            obj_ = DangerousGoodsRadionuclideDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.RadionuclideDetail = obj_
            obj_.original_tagname_ = 'RadionuclideDetail'
        elif nodeName_ == 'NetExplosiveDetail':
            obj_ = NetExplosiveDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.NetExplosiveDetail = obj_
            obj_.original_tagname_ = 'NetExplosiveDetail'
# end class UploadedDangerousGoodsCommodityContent


class UploadedDangerousGoodsCommodityDescription(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, IdType=None, Id=None, SequenceNumber=None, PackingGroup=None, PackingInstructions=None, AircraftCategoryType=None, ProperShippingName=None, TechnicalName=None, PrimaryClass=None, SubsidiaryClasses=None, ReportableQuantity=None, Percentage=None, AuthorizationInformation=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.IdType = IdType
        self.IdType_nsprefix_ = None
        self.Id = Id
        self.Id_nsprefix_ = None
        self.SequenceNumber = SequenceNumber
        self.SequenceNumber_nsprefix_ = None
        self.PackingGroup = PackingGroup
        self.validate_DangerousGoodsPackingGroupType(self.PackingGroup)
        self.PackingGroup_nsprefix_ = "ns"
        self.PackingInstructions = PackingInstructions
        self.PackingInstructions_nsprefix_ = None
        self.AircraftCategoryType = AircraftCategoryType
        self.validate_DangerousGoodsAircraftCategoryType(self.AircraftCategoryType)
        self.AircraftCategoryType_nsprefix_ = "ns"
        self.ProperShippingName = ProperShippingName
        self.ProperShippingName_nsprefix_ = None
        self.TechnicalName = TechnicalName
        self.TechnicalName_nsprefix_ = None
        self.PrimaryClass = PrimaryClass
        self.PrimaryClass_nsprefix_ = None
        if SubsidiaryClasses is None:
            self.SubsidiaryClasses = []
        else:
            self.SubsidiaryClasses = SubsidiaryClasses
        self.SubsidiaryClasses_nsprefix_ = None
        self.ReportableQuantity = ReportableQuantity
        self.ReportableQuantity_nsprefix_ = None
        self.Percentage = Percentage
        self.Percentage_nsprefix_ = None
        self.AuthorizationInformation = AuthorizationInformation
        self.AuthorizationInformation_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UploadedDangerousGoodsCommodityDescription)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UploadedDangerousGoodsCommodityDescription.subclass:
            return UploadedDangerousGoodsCommodityDescription.subclass(*args_, **kwargs_)
        else:
            return UploadedDangerousGoodsCommodityDescription(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_IdType(self):
        return self.IdType
    def set_IdType(self, IdType):
        self.IdType = IdType
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def get_SequenceNumber(self):
        return self.SequenceNumber
    def set_SequenceNumber(self, SequenceNumber):
        self.SequenceNumber = SequenceNumber
    def get_PackingGroup(self):
        return self.PackingGroup
    def set_PackingGroup(self, PackingGroup):
        self.PackingGroup = PackingGroup
    def get_PackingInstructions(self):
        return self.PackingInstructions
    def set_PackingInstructions(self, PackingInstructions):
        self.PackingInstructions = PackingInstructions
    def get_AircraftCategoryType(self):
        return self.AircraftCategoryType
    def set_AircraftCategoryType(self, AircraftCategoryType):
        self.AircraftCategoryType = AircraftCategoryType
    def get_ProperShippingName(self):
        return self.ProperShippingName
    def set_ProperShippingName(self, ProperShippingName):
        self.ProperShippingName = ProperShippingName
    def get_TechnicalName(self):
        return self.TechnicalName
    def set_TechnicalName(self, TechnicalName):
        self.TechnicalName = TechnicalName
    def get_PrimaryClass(self):
        return self.PrimaryClass
    def set_PrimaryClass(self, PrimaryClass):
        self.PrimaryClass = PrimaryClass
    def get_SubsidiaryClasses(self):
        return self.SubsidiaryClasses
    def set_SubsidiaryClasses(self, SubsidiaryClasses):
        self.SubsidiaryClasses = SubsidiaryClasses
    def add_SubsidiaryClasses(self, value):
        self.SubsidiaryClasses.append(value)
    def insert_SubsidiaryClasses_at(self, index, value):
        self.SubsidiaryClasses.insert(index, value)
    def replace_SubsidiaryClasses_at(self, index, value):
        self.SubsidiaryClasses[index] = value
    def get_ReportableQuantity(self):
        return self.ReportableQuantity
    def set_ReportableQuantity(self, ReportableQuantity):
        self.ReportableQuantity = ReportableQuantity
    def get_Percentage(self):
        return self.Percentage
    def set_Percentage(self, Percentage):
        self.Percentage = Percentage
    def get_AuthorizationInformation(self):
        return self.AuthorizationInformation
    def set_AuthorizationInformation(self, AuthorizationInformation):
        self.AuthorizationInformation = AuthorizationInformation
    def validate_DangerousGoodsPackingGroupType(self, value):
        result = True
        # Validate type DangerousGoodsPackingGroupType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['I', 'II', 'III', 'UNDEFINED']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DangerousGoodsPackingGroupType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DangerousGoodsAircraftCategoryType(self, value):
        result = True
        # Validate type DangerousGoodsAircraftCategoryType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['CARGO_AIRCRAFT_ONLY', 'PASSENGER_AND_CARGO_AIRCRAFT']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DangerousGoodsAircraftCategoryType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.IdType is not None or
            self.Id is not None or
            self.SequenceNumber is not None or
            self.PackingGroup is not None or
            self.PackingInstructions is not None or
            self.AircraftCategoryType is not None or
            self.ProperShippingName is not None or
            self.TechnicalName is not None or
            self.PrimaryClass is not None or
            self.SubsidiaryClasses or
            self.ReportableQuantity is not None or
            self.Percentage is not None or
            self.AuthorizationInformation is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadedDangerousGoodsCommodityDescription', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UploadedDangerousGoodsCommodityDescription')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UploadedDangerousGoodsCommodityDescription':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UploadedDangerousGoodsCommodityDescription')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UploadedDangerousGoodsCommodityDescription', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UploadedDangerousGoodsCommodityDescription'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadedDangerousGoodsCommodityDescription', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.IdType is not None:
            namespaceprefix_ = self.IdType_nsprefix_ + ':' if (UseCapturedNS_ and self.IdType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIdType>%s</%sIdType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IdType), input_name='IdType')), namespaceprefix_ , eol_))
        if self.Id is not None:
            namespaceprefix_ = self.Id_nsprefix_ + ':' if (UseCapturedNS_ and self.Id_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sId>%s</%sId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Id), input_name='Id')), namespaceprefix_ , eol_))
        if self.SequenceNumber is not None:
            namespaceprefix_ = self.SequenceNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.SequenceNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSequenceNumber>%s</%sSequenceNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.SequenceNumber, input_name='SequenceNumber'), namespaceprefix_ , eol_))
        if self.PackingGroup is not None:
            namespaceprefix_ = self.PackingGroup_nsprefix_ + ':' if (UseCapturedNS_ and self.PackingGroup_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPackingGroup>%s</%sPackingGroup>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PackingGroup), input_name='PackingGroup')), namespaceprefix_ , eol_))
        if self.PackingInstructions is not None:
            namespaceprefix_ = self.PackingInstructions_nsprefix_ + ':' if (UseCapturedNS_ and self.PackingInstructions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPackingInstructions>%s</%sPackingInstructions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PackingInstructions), input_name='PackingInstructions')), namespaceprefix_ , eol_))
        if self.AircraftCategoryType is not None:
            namespaceprefix_ = self.AircraftCategoryType_nsprefix_ + ':' if (UseCapturedNS_ and self.AircraftCategoryType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAircraftCategoryType>%s</%sAircraftCategoryType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AircraftCategoryType), input_name='AircraftCategoryType')), namespaceprefix_ , eol_))
        if self.ProperShippingName is not None:
            namespaceprefix_ = self.ProperShippingName_nsprefix_ + ':' if (UseCapturedNS_ and self.ProperShippingName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProperShippingName>%s</%sProperShippingName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ProperShippingName), input_name='ProperShippingName')), namespaceprefix_ , eol_))
        if self.TechnicalName is not None:
            namespaceprefix_ = self.TechnicalName_nsprefix_ + ':' if (UseCapturedNS_ and self.TechnicalName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTechnicalName>%s</%sTechnicalName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TechnicalName), input_name='TechnicalName')), namespaceprefix_ , eol_))
        if self.PrimaryClass is not None:
            namespaceprefix_ = self.PrimaryClass_nsprefix_ + ':' if (UseCapturedNS_ and self.PrimaryClass_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPrimaryClass>%s</%sPrimaryClass>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PrimaryClass), input_name='PrimaryClass')), namespaceprefix_ , eol_))
        for SubsidiaryClasses_ in self.SubsidiaryClasses:
            namespaceprefix_ = self.SubsidiaryClasses_nsprefix_ + ':' if (UseCapturedNS_ and self.SubsidiaryClasses_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSubsidiaryClasses>%s</%sSubsidiaryClasses>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(SubsidiaryClasses_), input_name='SubsidiaryClasses')), namespaceprefix_ , eol_))
        if self.ReportableQuantity is not None:
            namespaceprefix_ = self.ReportableQuantity_nsprefix_ + ':' if (UseCapturedNS_ and self.ReportableQuantity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReportableQuantity>%s</%sReportableQuantity>%s' % (namespaceprefix_ , self.gds_format_boolean(self.ReportableQuantity, input_name='ReportableQuantity'), namespaceprefix_ , eol_))
        if self.Percentage is not None:
            namespaceprefix_ = self.Percentage_nsprefix_ + ':' if (UseCapturedNS_ and self.Percentage_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPercentage>%s</%sPercentage>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Percentage, input_name='Percentage'), namespaceprefix_ , eol_))
        if self.AuthorizationInformation is not None:
            namespaceprefix_ = self.AuthorizationInformation_nsprefix_ + ':' if (UseCapturedNS_ and self.AuthorizationInformation_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAuthorizationInformation>%s</%sAuthorizationInformation>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AuthorizationInformation), input_name='AuthorizationInformation')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'IdType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IdType')
            value_ = self.gds_validate_string(value_, node, 'IdType')
            self.IdType = value_
            self.IdType_nsprefix_ = child_.prefix
        elif nodeName_ == 'Id':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Id')
            value_ = self.gds_validate_string(value_, node, 'Id')
            self.Id = value_
            self.Id_nsprefix_ = child_.prefix
        elif nodeName_ == 'SequenceNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'SequenceNumber')
            if ival_ < 0:
                raise_parse_error(child_, 'requires nonNegativeInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'SequenceNumber')
            self.SequenceNumber = ival_
            self.SequenceNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'PackingGroup':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PackingGroup')
            value_ = self.gds_validate_string(value_, node, 'PackingGroup')
            self.PackingGroup = value_
            self.PackingGroup_nsprefix_ = child_.prefix
            # validate type DangerousGoodsPackingGroupType
            self.validate_DangerousGoodsPackingGroupType(self.PackingGroup)
        elif nodeName_ == 'PackingInstructions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PackingInstructions')
            value_ = self.gds_validate_string(value_, node, 'PackingInstructions')
            self.PackingInstructions = value_
            self.PackingInstructions_nsprefix_ = child_.prefix
        elif nodeName_ == 'AircraftCategoryType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AircraftCategoryType')
            value_ = self.gds_validate_string(value_, node, 'AircraftCategoryType')
            self.AircraftCategoryType = value_
            self.AircraftCategoryType_nsprefix_ = child_.prefix
            # validate type DangerousGoodsAircraftCategoryType
            self.validate_DangerousGoodsAircraftCategoryType(self.AircraftCategoryType)
        elif nodeName_ == 'ProperShippingName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ProperShippingName')
            value_ = self.gds_validate_string(value_, node, 'ProperShippingName')
            self.ProperShippingName = value_
            self.ProperShippingName_nsprefix_ = child_.prefix
        elif nodeName_ == 'TechnicalName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TechnicalName')
            value_ = self.gds_validate_string(value_, node, 'TechnicalName')
            self.TechnicalName = value_
            self.TechnicalName_nsprefix_ = child_.prefix
        elif nodeName_ == 'PrimaryClass':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PrimaryClass')
            value_ = self.gds_validate_string(value_, node, 'PrimaryClass')
            self.PrimaryClass = value_
            self.PrimaryClass_nsprefix_ = child_.prefix
        elif nodeName_ == 'SubsidiaryClasses':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SubsidiaryClasses')
            value_ = self.gds_validate_string(value_, node, 'SubsidiaryClasses')
            self.SubsidiaryClasses.append(value_)
            self.SubsidiaryClasses_nsprefix_ = child_.prefix
        elif nodeName_ == 'ReportableQuantity':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'ReportableQuantity')
            ival_ = self.gds_validate_boolean(ival_, node, 'ReportableQuantity')
            self.ReportableQuantity = ival_
            self.ReportableQuantity_nsprefix_ = child_.prefix
        elif nodeName_ == 'Percentage' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Percentage')
            fval_ = self.gds_validate_decimal(fval_, node, 'Percentage')
            self.Percentage = fval_
            self.Percentage_nsprefix_ = child_.prefix
        elif nodeName_ == 'AuthorizationInformation':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AuthorizationInformation')
            value_ = self.gds_validate_string(value_, node, 'AuthorizationInformation')
            self.AuthorizationInformation = value_
            self.AuthorizationInformation_nsprefix_ = child_.prefix
# end class UploadedDangerousGoodsCommodityDescription


class UploadedDangerousGoodsContainer(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Attributes=None, ContainerType=None, QValue=None, GrossWeight=None, Commodities=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Attributes is None:
            self.Attributes = []
        else:
            self.Attributes = Attributes
        self.Attributes_nsprefix_ = "ns"
        self.ContainerType = ContainerType
        self.ContainerType_nsprefix_ = None
        self.QValue = QValue
        self.QValue_nsprefix_ = None
        self.GrossWeight = GrossWeight
        self.GrossWeight_nsprefix_ = "ns"
        if Commodities is None:
            self.Commodities = []
        else:
            self.Commodities = Commodities
        self.Commodities_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UploadedDangerousGoodsContainer)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UploadedDangerousGoodsContainer.subclass:
            return UploadedDangerousGoodsContainer.subclass(*args_, **kwargs_)
        else:
            return UploadedDangerousGoodsContainer(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Attributes(self):
        return self.Attributes
    def set_Attributes(self, Attributes):
        self.Attributes = Attributes
    def add_Attributes(self, value):
        self.Attributes.append(value)
    def insert_Attributes_at(self, index, value):
        self.Attributes.insert(index, value)
    def replace_Attributes_at(self, index, value):
        self.Attributes[index] = value
    def get_ContainerType(self):
        return self.ContainerType
    def set_ContainerType(self, ContainerType):
        self.ContainerType = ContainerType
    def get_QValue(self):
        return self.QValue
    def set_QValue(self, QValue):
        self.QValue = QValue
    def get_GrossWeight(self):
        return self.GrossWeight
    def set_GrossWeight(self, GrossWeight):
        self.GrossWeight = GrossWeight
    def get_Commodities(self):
        return self.Commodities
    def set_Commodities(self, Commodities):
        self.Commodities = Commodities
    def add_Commodities(self, value):
        self.Commodities.append(value)
    def insert_Commodities_at(self, index, value):
        self.Commodities.insert(index, value)
    def replace_Commodities_at(self, index, value):
        self.Commodities[index] = value
    def validate_DangerousGoodsContainerAttributeType(self, value):
        result = True
        # Validate type DangerousGoodsContainerAttributeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ALL_PACKED_IN_ONE']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DangerousGoodsContainerAttributeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Attributes or
            self.ContainerType is not None or
            self.QValue is not None or
            self.GrossWeight is not None or
            self.Commodities
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadedDangerousGoodsContainer', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UploadedDangerousGoodsContainer')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UploadedDangerousGoodsContainer':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UploadedDangerousGoodsContainer')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UploadedDangerousGoodsContainer', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UploadedDangerousGoodsContainer'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadedDangerousGoodsContainer', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Attributes_ in self.Attributes:
            namespaceprefix_ = self.Attributes_nsprefix_ + ':' if (UseCapturedNS_ and self.Attributes_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAttributes>%s</%sAttributes>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Attributes_), input_name='Attributes')), namespaceprefix_ , eol_))
        if self.ContainerType is not None:
            namespaceprefix_ = self.ContainerType_nsprefix_ + ':' if (UseCapturedNS_ and self.ContainerType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sContainerType>%s</%sContainerType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ContainerType), input_name='ContainerType')), namespaceprefix_ , eol_))
        if self.QValue is not None:
            namespaceprefix_ = self.QValue_nsprefix_ + ':' if (UseCapturedNS_ and self.QValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sQValue>%s</%sQValue>%s' % (namespaceprefix_ , self.gds_format_decimal(self.QValue, input_name='QValue'), namespaceprefix_ , eol_))
        if self.GrossWeight is not None:
            namespaceprefix_ = self.GrossWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.GrossWeight_nsprefix_) else ''
            self.GrossWeight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GrossWeight', pretty_print=pretty_print)
        for Commodities_ in self.Commodities:
            namespaceprefix_ = self.Commodities_nsprefix_ + ':' if (UseCapturedNS_ and self.Commodities_nsprefix_) else ''
            Commodities_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Commodities', pretty_print=pretty_print)
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
        if nodeName_ == 'Attributes':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Attributes')
            value_ = self.gds_validate_string(value_, node, 'Attributes')
            self.Attributes.append(value_)
            self.Attributes_nsprefix_ = child_.prefix
            # validate type DangerousGoodsContainerAttributeType
            self.validate_DangerousGoodsContainerAttributeType(self.Attributes[-1])
        elif nodeName_ == 'ContainerType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ContainerType')
            value_ = self.gds_validate_string(value_, node, 'ContainerType')
            self.ContainerType = value_
            self.ContainerType_nsprefix_ = child_.prefix
        elif nodeName_ == 'QValue' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'QValue')
            fval_ = self.gds_validate_decimal(fval_, node, 'QValue')
            self.QValue = fval_
            self.QValue_nsprefix_ = child_.prefix
        elif nodeName_ == 'GrossWeight':
            obj_ = Weight.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GrossWeight = obj_
            obj_.original_tagname_ = 'GrossWeight'
        elif nodeName_ == 'Commodities':
            obj_ = UploadedDangerousGoodsCommodityContent.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Commodities.append(obj_)
            obj_.original_tagname_ = 'Commodities'
# end class UploadedDangerousGoodsContainer


class UploadedDangerousGoodsContainerGroup(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, NumberOfIdenticalContainers=None, Container=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.NumberOfIdenticalContainers = NumberOfIdenticalContainers
        self.NumberOfIdenticalContainers_nsprefix_ = None
        self.Container = Container
        self.Container_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UploadedDangerousGoodsContainerGroup)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UploadedDangerousGoodsContainerGroup.subclass:
            return UploadedDangerousGoodsContainerGroup.subclass(*args_, **kwargs_)
        else:
            return UploadedDangerousGoodsContainerGroup(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_NumberOfIdenticalContainers(self):
        return self.NumberOfIdenticalContainers
    def set_NumberOfIdenticalContainers(self, NumberOfIdenticalContainers):
        self.NumberOfIdenticalContainers = NumberOfIdenticalContainers
    def get_Container(self):
        return self.Container
    def set_Container(self, Container):
        self.Container = Container
    def hasContent_(self):
        if (
            self.NumberOfIdenticalContainers is not None or
            self.Container is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadedDangerousGoodsContainerGroup', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UploadedDangerousGoodsContainerGroup')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UploadedDangerousGoodsContainerGroup':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UploadedDangerousGoodsContainerGroup')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UploadedDangerousGoodsContainerGroup', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UploadedDangerousGoodsContainerGroup'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadedDangerousGoodsContainerGroup', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.NumberOfIdenticalContainers is not None:
            namespaceprefix_ = self.NumberOfIdenticalContainers_nsprefix_ + ':' if (UseCapturedNS_ and self.NumberOfIdenticalContainers_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumberOfIdenticalContainers>%s</%sNumberOfIdenticalContainers>%s' % (namespaceprefix_ , self.gds_format_integer(self.NumberOfIdenticalContainers, input_name='NumberOfIdenticalContainers'), namespaceprefix_ , eol_))
        if self.Container is not None:
            namespaceprefix_ = self.Container_nsprefix_ + ':' if (UseCapturedNS_ and self.Container_nsprefix_) else ''
            self.Container.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Container', pretty_print=pretty_print)
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
        if nodeName_ == 'NumberOfIdenticalContainers' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'NumberOfIdenticalContainers')
            if ival_ < 0:
                raise_parse_error(child_, 'requires nonNegativeInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'NumberOfIdenticalContainers')
            self.NumberOfIdenticalContainers = ival_
            self.NumberOfIdenticalContainers_nsprefix_ = child_.prefix
        elif nodeName_ == 'Container':
            obj_ = UploadedDangerousGoodsContainer.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Container = obj_
            obj_.original_tagname_ = 'Container'
# end class UploadedDangerousGoodsContainerGroup


class UploadedDangerousGoodsHandlingUnit(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Attributes=None, RadioactiveDetail=None, ContainerGroups=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Attributes is None:
            self.Attributes = []
        else:
            self.Attributes = Attributes
        self.Attributes_nsprefix_ = "ns"
        self.RadioactiveDetail = RadioactiveDetail
        self.RadioactiveDetail_nsprefix_ = "ns"
        if ContainerGroups is None:
            self.ContainerGroups = []
        else:
            self.ContainerGroups = ContainerGroups
        self.ContainerGroups_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UploadedDangerousGoodsHandlingUnit)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UploadedDangerousGoodsHandlingUnit.subclass:
            return UploadedDangerousGoodsHandlingUnit.subclass(*args_, **kwargs_)
        else:
            return UploadedDangerousGoodsHandlingUnit(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Attributes(self):
        return self.Attributes
    def set_Attributes(self, Attributes):
        self.Attributes = Attributes
    def add_Attributes(self, value):
        self.Attributes.append(value)
    def insert_Attributes_at(self, index, value):
        self.Attributes.insert(index, value)
    def replace_Attributes_at(self, index, value):
        self.Attributes[index] = value
    def get_RadioactiveDetail(self):
        return self.RadioactiveDetail
    def set_RadioactiveDetail(self, RadioactiveDetail):
        self.RadioactiveDetail = RadioactiveDetail
    def get_ContainerGroups(self):
        return self.ContainerGroups
    def set_ContainerGroups(self, ContainerGroups):
        self.ContainerGroups = ContainerGroups
    def add_ContainerGroups(self, value):
        self.ContainerGroups.append(value)
    def insert_ContainerGroups_at(self, index, value):
        self.ContainerGroups.insert(index, value)
    def replace_ContainerGroups_at(self, index, value):
        self.ContainerGroups[index] = value
    def validate_DangerousGoodsHandlingUnitAttributeType(self, value):
        result = True
        # Validate type DangerousGoodsHandlingUnitAttributeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['OVERPACK']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DangerousGoodsHandlingUnitAttributeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Attributes or
            self.RadioactiveDetail is not None or
            self.ContainerGroups
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadedDangerousGoodsHandlingUnit', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UploadedDangerousGoodsHandlingUnit')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UploadedDangerousGoodsHandlingUnit':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UploadedDangerousGoodsHandlingUnit')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UploadedDangerousGoodsHandlingUnit', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UploadedDangerousGoodsHandlingUnit'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadedDangerousGoodsHandlingUnit', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Attributes_ in self.Attributes:
            namespaceprefix_ = self.Attributes_nsprefix_ + ':' if (UseCapturedNS_ and self.Attributes_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAttributes>%s</%sAttributes>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Attributes_), input_name='Attributes')), namespaceprefix_ , eol_))
        if self.RadioactiveDetail is not None:
            namespaceprefix_ = self.RadioactiveDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.RadioactiveDetail_nsprefix_) else ''
            self.RadioactiveDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='RadioactiveDetail', pretty_print=pretty_print)
        for ContainerGroups_ in self.ContainerGroups:
            namespaceprefix_ = self.ContainerGroups_nsprefix_ + ':' if (UseCapturedNS_ and self.ContainerGroups_nsprefix_) else ''
            ContainerGroups_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ContainerGroups', pretty_print=pretty_print)
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
        if nodeName_ == 'Attributes':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Attributes')
            value_ = self.gds_validate_string(value_, node, 'Attributes')
            self.Attributes.append(value_)
            self.Attributes_nsprefix_ = child_.prefix
            # validate type DangerousGoodsHandlingUnitAttributeType
            self.validate_DangerousGoodsHandlingUnitAttributeType(self.Attributes[-1])
        elif nodeName_ == 'RadioactiveDetail':
            obj_ = RadioactiveDangerousGoodsHandlingUnitDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.RadioactiveDetail = obj_
            obj_.original_tagname_ = 'RadioactiveDetail'
        elif nodeName_ == 'ContainerGroups':
            obj_ = UploadedDangerousGoodsContainerGroup.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ContainerGroups.append(obj_)
            obj_.original_tagname_ = 'ContainerGroups'
# end class UploadedDangerousGoodsHandlingUnit


class UploadedDangerousGoodsHandlingUnitGroup(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Id=None, Description=None, NumberOfHandlingUnits=None, AssociatedDocumentDetails=None, TrackingNumberUnits=None, HandlingUnit=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Id = Id
        self.Id_nsprefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = None
        self.NumberOfHandlingUnits = NumberOfHandlingUnits
        self.NumberOfHandlingUnits_nsprefix_ = None
        if AssociatedDocumentDetails is None:
            self.AssociatedDocumentDetails = []
        else:
            self.AssociatedDocumentDetails = AssociatedDocumentDetails
        self.AssociatedDocumentDetails_nsprefix_ = "ns"
        if TrackingNumberUnits is None:
            self.TrackingNumberUnits = []
        else:
            self.TrackingNumberUnits = TrackingNumberUnits
        self.TrackingNumberUnits_nsprefix_ = "ns"
        self.HandlingUnit = HandlingUnit
        self.HandlingUnit_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UploadedDangerousGoodsHandlingUnitGroup)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UploadedDangerousGoodsHandlingUnitGroup.subclass:
            return UploadedDangerousGoodsHandlingUnitGroup.subclass(*args_, **kwargs_)
        else:
            return UploadedDangerousGoodsHandlingUnitGroup(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def get_NumberOfHandlingUnits(self):
        return self.NumberOfHandlingUnits
    def set_NumberOfHandlingUnits(self, NumberOfHandlingUnits):
        self.NumberOfHandlingUnits = NumberOfHandlingUnits
    def get_AssociatedDocumentDetails(self):
        return self.AssociatedDocumentDetails
    def set_AssociatedDocumentDetails(self, AssociatedDocumentDetails):
        self.AssociatedDocumentDetails = AssociatedDocumentDetails
    def add_AssociatedDocumentDetails(self, value):
        self.AssociatedDocumentDetails.append(value)
    def insert_AssociatedDocumentDetails_at(self, index, value):
        self.AssociatedDocumentDetails.insert(index, value)
    def replace_AssociatedDocumentDetails_at(self, index, value):
        self.AssociatedDocumentDetails[index] = value
    def get_TrackingNumberUnits(self):
        return self.TrackingNumberUnits
    def set_TrackingNumberUnits(self, TrackingNumberUnits):
        self.TrackingNumberUnits = TrackingNumberUnits
    def add_TrackingNumberUnits(self, value):
        self.TrackingNumberUnits.append(value)
    def insert_TrackingNumberUnits_at(self, index, value):
        self.TrackingNumberUnits.insert(index, value)
    def replace_TrackingNumberUnits_at(self, index, value):
        self.TrackingNumberUnits[index] = value
    def get_HandlingUnit(self):
        return self.HandlingUnit
    def set_HandlingUnit(self, HandlingUnit):
        self.HandlingUnit = HandlingUnit
    def hasContent_(self):
        if (
            self.Id is not None or
            self.Description is not None or
            self.NumberOfHandlingUnits is not None or
            self.AssociatedDocumentDetails or
            self.TrackingNumberUnits or
            self.HandlingUnit is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadedDangerousGoodsHandlingUnitGroup', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UploadedDangerousGoodsHandlingUnitGroup')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UploadedDangerousGoodsHandlingUnitGroup':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UploadedDangerousGoodsHandlingUnitGroup')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UploadedDangerousGoodsHandlingUnitGroup', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UploadedDangerousGoodsHandlingUnitGroup'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadedDangerousGoodsHandlingUnitGroup', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Id is not None:
            namespaceprefix_ = self.Id_nsprefix_ + ':' if (UseCapturedNS_ and self.Id_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sId>%s</%sId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Id), input_name='Id')), namespaceprefix_ , eol_))
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
        if self.NumberOfHandlingUnits is not None:
            namespaceprefix_ = self.NumberOfHandlingUnits_nsprefix_ + ':' if (UseCapturedNS_ and self.NumberOfHandlingUnits_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumberOfHandlingUnits>%s</%sNumberOfHandlingUnits>%s' % (namespaceprefix_ , self.gds_format_integer(self.NumberOfHandlingUnits, input_name='NumberOfHandlingUnits'), namespaceprefix_ , eol_))
        for AssociatedDocumentDetails_ in self.AssociatedDocumentDetails:
            namespaceprefix_ = self.AssociatedDocumentDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.AssociatedDocumentDetails_nsprefix_) else ''
            AssociatedDocumentDetails_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AssociatedDocumentDetails', pretty_print=pretty_print)
        for TrackingNumberUnits_ in self.TrackingNumberUnits:
            namespaceprefix_ = self.TrackingNumberUnits_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackingNumberUnits_nsprefix_) else ''
            TrackingNumberUnits_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TrackingNumberUnits', pretty_print=pretty_print)
        if self.HandlingUnit is not None:
            namespaceprefix_ = self.HandlingUnit_nsprefix_ + ':' if (UseCapturedNS_ and self.HandlingUnit_nsprefix_) else ''
            self.HandlingUnit.export(outfile, level, namespaceprefix_, namespacedef_='', name_='HandlingUnit', pretty_print=pretty_print)
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
        if nodeName_ == 'Id':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Id')
            value_ = self.gds_validate_string(value_, node, 'Id')
            self.Id = value_
            self.Id_nsprefix_ = child_.prefix
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
        elif nodeName_ == 'NumberOfHandlingUnits' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'NumberOfHandlingUnits')
            if ival_ < 0:
                raise_parse_error(child_, 'requires nonNegativeInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'NumberOfHandlingUnits')
            self.NumberOfHandlingUnits = ival_
            self.NumberOfHandlingUnits_nsprefix_ = child_.prefix
        elif nodeName_ == 'AssociatedDocumentDetails':
            obj_ = AssociatedEnterpriseDocumentDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AssociatedDocumentDetails.append(obj_)
            obj_.original_tagname_ = 'AssociatedDocumentDetails'
        elif nodeName_ == 'TrackingNumberUnits':
            obj_ = TrackingNumberUnit.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TrackingNumberUnits.append(obj_)
            obj_.original_tagname_ = 'TrackingNumberUnits'
        elif nodeName_ == 'HandlingUnit':
            obj_ = UploadedDangerousGoodsHandlingUnit.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.HandlingUnit = obj_
            obj_.original_tagname_ = 'HandlingUnit'
# end class UploadedDangerousGoodsHandlingUnitGroup


class UploadedDangerousGoodsShipmentDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Attributes=None, Origin=None, Destination=None, CarrierCode=None, ServiceType=None, ShipDate=None, Offeror=None, Signatory=None, InfectiousSubstanceResponsibleContact=None, EmergencyContactNumber=None, AircraftCategoryType=None, AdditionalHandling=None, MasterTrackingId=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Attributes is None:
            self.Attributes = []
        else:
            self.Attributes = Attributes
        self.Attributes_nsprefix_ = "ns"
        self.Origin = Origin
        self.Origin_nsprefix_ = "ns"
        self.Destination = Destination
        self.Destination_nsprefix_ = "ns"
        self.CarrierCode = CarrierCode
        self.validate_CarrierCodeType(self.CarrierCode)
        self.CarrierCode_nsprefix_ = "ns"
        self.ServiceType = ServiceType
        self.ServiceType_nsprefix_ = None
        if isinstance(ShipDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ShipDate, '%Y-%m-%d').date()
        else:
            initvalue_ = ShipDate
        self.ShipDate = initvalue_
        self.ShipDate_nsprefix_ = None
        self.Offeror = Offeror
        self.Offeror_nsprefix_ = None
        self.Signatory = Signatory
        self.Signatory_nsprefix_ = "ns"
        self.InfectiousSubstanceResponsibleContact = InfectiousSubstanceResponsibleContact
        self.InfectiousSubstanceResponsibleContact_nsprefix_ = "ns"
        self.EmergencyContactNumber = EmergencyContactNumber
        self.EmergencyContactNumber_nsprefix_ = None
        self.AircraftCategoryType = AircraftCategoryType
        self.validate_DangerousGoodsAircraftCategoryType(self.AircraftCategoryType)
        self.AircraftCategoryType_nsprefix_ = "ns"
        self.AdditionalHandling = AdditionalHandling
        self.AdditionalHandling_nsprefix_ = None
        self.MasterTrackingId = MasterTrackingId
        self.MasterTrackingId_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UploadedDangerousGoodsShipmentDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UploadedDangerousGoodsShipmentDetail.subclass:
            return UploadedDangerousGoodsShipmentDetail.subclass(*args_, **kwargs_)
        else:
            return UploadedDangerousGoodsShipmentDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Attributes(self):
        return self.Attributes
    def set_Attributes(self, Attributes):
        self.Attributes = Attributes
    def add_Attributes(self, value):
        self.Attributes.append(value)
    def insert_Attributes_at(self, index, value):
        self.Attributes.insert(index, value)
    def replace_Attributes_at(self, index, value):
        self.Attributes[index] = value
    def get_Origin(self):
        return self.Origin
    def set_Origin(self, Origin):
        self.Origin = Origin
    def get_Destination(self):
        return self.Destination
    def set_Destination(self, Destination):
        self.Destination = Destination
    def get_CarrierCode(self):
        return self.CarrierCode
    def set_CarrierCode(self, CarrierCode):
        self.CarrierCode = CarrierCode
    def get_ServiceType(self):
        return self.ServiceType
    def set_ServiceType(self, ServiceType):
        self.ServiceType = ServiceType
    def get_ShipDate(self):
        return self.ShipDate
    def set_ShipDate(self, ShipDate):
        self.ShipDate = ShipDate
    def get_Offeror(self):
        return self.Offeror
    def set_Offeror(self, Offeror):
        self.Offeror = Offeror
    def get_Signatory(self):
        return self.Signatory
    def set_Signatory(self, Signatory):
        self.Signatory = Signatory
    def get_InfectiousSubstanceResponsibleContact(self):
        return self.InfectiousSubstanceResponsibleContact
    def set_InfectiousSubstanceResponsibleContact(self, InfectiousSubstanceResponsibleContact):
        self.InfectiousSubstanceResponsibleContact = InfectiousSubstanceResponsibleContact
    def get_EmergencyContactNumber(self):
        return self.EmergencyContactNumber
    def set_EmergencyContactNumber(self, EmergencyContactNumber):
        self.EmergencyContactNumber = EmergencyContactNumber
    def get_AircraftCategoryType(self):
        return self.AircraftCategoryType
    def set_AircraftCategoryType(self, AircraftCategoryType):
        self.AircraftCategoryType = AircraftCategoryType
    def get_AdditionalHandling(self):
        return self.AdditionalHandling
    def set_AdditionalHandling(self, AdditionalHandling):
        self.AdditionalHandling = AdditionalHandling
    def get_MasterTrackingId(self):
        return self.MasterTrackingId
    def set_MasterTrackingId(self, MasterTrackingId):
        self.MasterTrackingId = MasterTrackingId
    def validate_UploadedDangerousGoodsShipmentAttributeType(self, value):
        result = True
        # Validate type UploadedDangerousGoodsShipmentAttributeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['MANUAL_SHIPPING_LABEL']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on UploadedDangerousGoodsShipmentAttributeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CarrierCodeType(self, value):
        result = True
        # Validate type CarrierCodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FDXC', 'FDXE', 'FDXG', 'FXCC', 'FXFR', 'FXSP']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on CarrierCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DangerousGoodsAircraftCategoryType(self, value):
        result = True
        # Validate type DangerousGoodsAircraftCategoryType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['CARGO_AIRCRAFT_ONLY', 'PASSENGER_AND_CARGO_AIRCRAFT']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on DangerousGoodsAircraftCategoryType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Attributes or
            self.Origin is not None or
            self.Destination is not None or
            self.CarrierCode is not None or
            self.ServiceType is not None or
            self.ShipDate is not None or
            self.Offeror is not None or
            self.Signatory is not None or
            self.InfectiousSubstanceResponsibleContact is not None or
            self.EmergencyContactNumber is not None or
            self.AircraftCategoryType is not None or
            self.AdditionalHandling is not None or
            self.MasterTrackingId is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadedDangerousGoodsShipmentDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UploadedDangerousGoodsShipmentDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UploadedDangerousGoodsShipmentDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UploadedDangerousGoodsShipmentDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UploadedDangerousGoodsShipmentDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UploadedDangerousGoodsShipmentDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UploadedDangerousGoodsShipmentDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Attributes_ in self.Attributes:
            namespaceprefix_ = self.Attributes_nsprefix_ + ':' if (UseCapturedNS_ and self.Attributes_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAttributes>%s</%sAttributes>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Attributes_), input_name='Attributes')), namespaceprefix_ , eol_))
        if self.Origin is not None:
            namespaceprefix_ = self.Origin_nsprefix_ + ':' if (UseCapturedNS_ and self.Origin_nsprefix_) else ''
            self.Origin.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Origin', pretty_print=pretty_print)
        if self.Destination is not None:
            namespaceprefix_ = self.Destination_nsprefix_ + ':' if (UseCapturedNS_ and self.Destination_nsprefix_) else ''
            self.Destination.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Destination', pretty_print=pretty_print)
        if self.CarrierCode is not None:
            namespaceprefix_ = self.CarrierCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CarrierCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCarrierCode>%s</%sCarrierCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CarrierCode), input_name='CarrierCode')), namespaceprefix_ , eol_))
        if self.ServiceType is not None:
            namespaceprefix_ = self.ServiceType_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceType>%s</%sServiceType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServiceType), input_name='ServiceType')), namespaceprefix_ , eol_))
        if self.ShipDate is not None:
            namespaceprefix_ = self.ShipDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipDate>%s</%sShipDate>%s' % (namespaceprefix_ , self.gds_format_date(self.ShipDate, input_name='ShipDate'), namespaceprefix_ , eol_))
        if self.Offeror is not None:
            namespaceprefix_ = self.Offeror_nsprefix_ + ':' if (UseCapturedNS_ and self.Offeror_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOfferor>%s</%sOfferor>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Offeror), input_name='Offeror')), namespaceprefix_ , eol_))
        if self.Signatory is not None:
            namespaceprefix_ = self.Signatory_nsprefix_ + ':' if (UseCapturedNS_ and self.Signatory_nsprefix_) else ''
            self.Signatory.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Signatory', pretty_print=pretty_print)
        if self.InfectiousSubstanceResponsibleContact is not None:
            namespaceprefix_ = self.InfectiousSubstanceResponsibleContact_nsprefix_ + ':' if (UseCapturedNS_ and self.InfectiousSubstanceResponsibleContact_nsprefix_) else ''
            self.InfectiousSubstanceResponsibleContact.export(outfile, level, namespaceprefix_, namespacedef_='', name_='InfectiousSubstanceResponsibleContact', pretty_print=pretty_print)
        if self.EmergencyContactNumber is not None:
            namespaceprefix_ = self.EmergencyContactNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.EmergencyContactNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEmergencyContactNumber>%s</%sEmergencyContactNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EmergencyContactNumber), input_name='EmergencyContactNumber')), namespaceprefix_ , eol_))
        if self.AircraftCategoryType is not None:
            namespaceprefix_ = self.AircraftCategoryType_nsprefix_ + ':' if (UseCapturedNS_ and self.AircraftCategoryType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAircraftCategoryType>%s</%sAircraftCategoryType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AircraftCategoryType), input_name='AircraftCategoryType')), namespaceprefix_ , eol_))
        if self.AdditionalHandling is not None:
            namespaceprefix_ = self.AdditionalHandling_nsprefix_ + ':' if (UseCapturedNS_ and self.AdditionalHandling_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAdditionalHandling>%s</%sAdditionalHandling>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AdditionalHandling), input_name='AdditionalHandling')), namespaceprefix_ , eol_))
        if self.MasterTrackingId is not None:
            namespaceprefix_ = self.MasterTrackingId_nsprefix_ + ':' if (UseCapturedNS_ and self.MasterTrackingId_nsprefix_) else ''
            self.MasterTrackingId.export(outfile, level, namespaceprefix_, namespacedef_='', name_='MasterTrackingId', pretty_print=pretty_print)
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
        if nodeName_ == 'Attributes':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Attributes')
            value_ = self.gds_validate_string(value_, node, 'Attributes')
            self.Attributes.append(value_)
            self.Attributes_nsprefix_ = child_.prefix
            # validate type UploadedDangerousGoodsShipmentAttributeType
            self.validate_UploadedDangerousGoodsShipmentAttributeType(self.Attributes[-1])
        elif nodeName_ == 'Origin':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Origin = obj_
            obj_.original_tagname_ = 'Origin'
        elif nodeName_ == 'Destination':
            obj_ = Address.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Destination = obj_
            obj_.original_tagname_ = 'Destination'
        elif nodeName_ == 'CarrierCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CarrierCode')
            value_ = self.gds_validate_string(value_, node, 'CarrierCode')
            self.CarrierCode = value_
            self.CarrierCode_nsprefix_ = child_.prefix
            # validate type CarrierCodeType
            self.validate_CarrierCodeType(self.CarrierCode)
        elif nodeName_ == 'ServiceType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServiceType')
            value_ = self.gds_validate_string(value_, node, 'ServiceType')
            self.ServiceType = value_
            self.ServiceType_nsprefix_ = child_.prefix
        elif nodeName_ == 'ShipDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.ShipDate = dval_
            self.ShipDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'Offeror':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Offeror')
            value_ = self.gds_validate_string(value_, node, 'Offeror')
            self.Offeror = value_
            self.Offeror_nsprefix_ = child_.prefix
        elif nodeName_ == 'Signatory':
            obj_ = DangerousGoodsSignatory.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Signatory = obj_
            obj_.original_tagname_ = 'Signatory'
        elif nodeName_ == 'InfectiousSubstanceResponsibleContact':
            obj_ = Contact.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.InfectiousSubstanceResponsibleContact = obj_
            obj_.original_tagname_ = 'InfectiousSubstanceResponsibleContact'
        elif nodeName_ == 'EmergencyContactNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EmergencyContactNumber')
            value_ = self.gds_validate_string(value_, node, 'EmergencyContactNumber')
            self.EmergencyContactNumber = value_
            self.EmergencyContactNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'AircraftCategoryType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AircraftCategoryType')
            value_ = self.gds_validate_string(value_, node, 'AircraftCategoryType')
            self.AircraftCategoryType = value_
            self.AircraftCategoryType_nsprefix_ = child_.prefix
            # validate type DangerousGoodsAircraftCategoryType
            self.validate_DangerousGoodsAircraftCategoryType(self.AircraftCategoryType)
        elif nodeName_ == 'AdditionalHandling':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AdditionalHandling')
            value_ = self.gds_validate_string(value_, node, 'AdditionalHandling')
            self.AdditionalHandling = value_
            self.AdditionalHandling_nsprefix_ = child_.prefix
        elif nodeName_ == 'MasterTrackingId':
            obj_ = TrackingId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.MasterTrackingId = obj_
            obj_.original_tagname_ = 'MasterTrackingId'
# end class UploadedDangerousGoodsShipmentDetail


class ValidateDangerousGoodsProcessingOptionsRequested(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Options=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Options is None:
            self.Options = []
        else:
            self.Options = Options
        self.Options_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ValidateDangerousGoodsProcessingOptionsRequested)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ValidateDangerousGoodsProcessingOptionsRequested.subclass:
            return ValidateDangerousGoodsProcessingOptionsRequested.subclass(*args_, **kwargs_)
        else:
            return ValidateDangerousGoodsProcessingOptionsRequested(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Options(self):
        return self.Options
    def set_Options(self, Options):
        self.Options = Options
    def add_Options(self, value):
        self.Options.append(value)
    def insert_Options_at(self, index, value):
        self.Options.insert(index, value)
    def replace_Options_at(self, index, value):
        self.Options[index] = value
    def validate_ValidateDangerousGoodsProcessingOptionType(self, value):
        result = True
        # Validate type ValidateDangerousGoodsProcessingOptionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['BYPASS_PRODUCT_VALIDATION', 'BYPASS_TRACKING_NUMBER_VALIDATION']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ValidateDangerousGoodsProcessingOptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Options
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ValidateDangerousGoodsProcessingOptionsRequested', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ValidateDangerousGoodsProcessingOptionsRequested')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ValidateDangerousGoodsProcessingOptionsRequested':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ValidateDangerousGoodsProcessingOptionsRequested')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ValidateDangerousGoodsProcessingOptionsRequested', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ValidateDangerousGoodsProcessingOptionsRequested'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ValidateDangerousGoodsProcessingOptionsRequested', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Options_ in self.Options:
            namespaceprefix_ = self.Options_nsprefix_ + ':' if (UseCapturedNS_ and self.Options_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOptions>%s</%sOptions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Options_), input_name='Options')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Options':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Options')
            value_ = self.gds_validate_string(value_, node, 'Options')
            self.Options.append(value_)
            self.Options_nsprefix_ = child_.prefix
            # validate type ValidateDangerousGoodsProcessingOptionType
            self.validate_ValidateDangerousGoodsProcessingOptionType(self.Options[-1])
# end class ValidateDangerousGoodsProcessingOptionsRequested


class ValidateDangerousGoodsReply(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, CompletedShipmentDetail=None, CompletedHandlingUnitGroups=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.HighestSeverity = HighestSeverity
        self.validate_NotificationSeverityType(self.HighestSeverity)
        self.HighestSeverity_nsprefix_ = "ns"
        if Notifications is None:
            self.Notifications = []
        else:
            self.Notifications = Notifications
        self.Notifications_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.CompletedShipmentDetail = CompletedShipmentDetail
        self.CompletedShipmentDetail_nsprefix_ = "ns"
        if CompletedHandlingUnitGroups is None:
            self.CompletedHandlingUnitGroups = []
        else:
            self.CompletedHandlingUnitGroups = CompletedHandlingUnitGroups
        self.CompletedHandlingUnitGroups_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ValidateDangerousGoodsReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ValidateDangerousGoodsReply.subclass:
            return ValidateDangerousGoodsReply.subclass(*args_, **kwargs_)
        else:
            return ValidateDangerousGoodsReply(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_HighestSeverity(self):
        return self.HighestSeverity
    def set_HighestSeverity(self, HighestSeverity):
        self.HighestSeverity = HighestSeverity
    def get_Notifications(self):
        return self.Notifications
    def set_Notifications(self, Notifications):
        self.Notifications = Notifications
    def add_Notifications(self, value):
        self.Notifications.append(value)
    def insert_Notifications_at(self, index, value):
        self.Notifications.insert(index, value)
    def replace_Notifications_at(self, index, value):
        self.Notifications[index] = value
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_CompletedShipmentDetail(self):
        return self.CompletedShipmentDetail
    def set_CompletedShipmentDetail(self, CompletedShipmentDetail):
        self.CompletedShipmentDetail = CompletedShipmentDetail
    def get_CompletedHandlingUnitGroups(self):
        return self.CompletedHandlingUnitGroups
    def set_CompletedHandlingUnitGroups(self, CompletedHandlingUnitGroups):
        self.CompletedHandlingUnitGroups = CompletedHandlingUnitGroups
    def add_CompletedHandlingUnitGroups(self, value):
        self.CompletedHandlingUnitGroups.append(value)
    def insert_CompletedHandlingUnitGroups_at(self, index, value):
        self.CompletedHandlingUnitGroups.insert(index, value)
    def replace_CompletedHandlingUnitGroups_at(self, index, value):
        self.CompletedHandlingUnitGroups[index] = value
    def validate_NotificationSeverityType(self, value):
        result = True
        # Validate type NotificationSeverityType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ERROR', 'FAILURE', 'NOTE', 'SUCCESS', 'WARNING']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on NotificationSeverityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.HighestSeverity is not None or
            self.Notifications or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.CompletedShipmentDetail is not None or
            self.CompletedHandlingUnitGroups
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ValidateDangerousGoodsReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ValidateDangerousGoodsReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ValidateDangerousGoodsReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ValidateDangerousGoodsReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ValidateDangerousGoodsReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ValidateDangerousGoodsReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ValidateDangerousGoodsReply', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.HighestSeverity is not None:
            namespaceprefix_ = self.HighestSeverity_nsprefix_ + ':' if (UseCapturedNS_ and self.HighestSeverity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHighestSeverity>%s</%sHighestSeverity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HighestSeverity), input_name='HighestSeverity')), namespaceprefix_ , eol_))
        for Notifications_ in self.Notifications:
            namespaceprefix_ = self.Notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.Notifications_nsprefix_) else ''
            Notifications_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notifications', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.CompletedShipmentDetail is not None:
            namespaceprefix_ = self.CompletedShipmentDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.CompletedShipmentDetail_nsprefix_) else ''
            self.CompletedShipmentDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CompletedShipmentDetail', pretty_print=pretty_print)
        for CompletedHandlingUnitGroups_ in self.CompletedHandlingUnitGroups:
            namespaceprefix_ = self.CompletedHandlingUnitGroups_nsprefix_ + ':' if (UseCapturedNS_ and self.CompletedHandlingUnitGroups_nsprefix_) else ''
            CompletedHandlingUnitGroups_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CompletedHandlingUnitGroups', pretty_print=pretty_print)
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
        if nodeName_ == 'HighestSeverity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HighestSeverity')
            value_ = self.gds_validate_string(value_, node, 'HighestSeverity')
            self.HighestSeverity = value_
            self.HighestSeverity_nsprefix_ = child_.prefix
            # validate type NotificationSeverityType
            self.validate_NotificationSeverityType(self.HighestSeverity)
        elif nodeName_ == 'Notifications':
            obj_ = Notification.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notifications.append(obj_)
            obj_.original_tagname_ = 'Notifications'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'CompletedShipmentDetail':
            obj_ = CompletedDangerousGoodsShipmentDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CompletedShipmentDetail = obj_
            obj_.original_tagname_ = 'CompletedShipmentDetail'
        elif nodeName_ == 'CompletedHandlingUnitGroups':
            obj_ = CompletedDangerousGoodsHandlingUnitGroup.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CompletedHandlingUnitGroups.append(obj_)
            obj_.original_tagname_ = 'CompletedHandlingUnitGroups'
# end class ValidateDangerousGoodsReply


class ValidateDangerousGoodsRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, TransactionDetail=None, Version=None, ProcessingOptions=None, ShipmentDetail=None, HandlingUnitGroups=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.WebAuthenticationDetail = WebAuthenticationDetail
        self.WebAuthenticationDetail_nsprefix_ = "ns"
        self.ClientDetail = ClientDetail
        self.ClientDetail_nsprefix_ = "ns"
        self.TransactionDetail = TransactionDetail
        self.TransactionDetail_nsprefix_ = "ns"
        self.Version = Version
        self.Version_nsprefix_ = "ns"
        self.ProcessingOptions = ProcessingOptions
        self.ProcessingOptions_nsprefix_ = "ns"
        self.ShipmentDetail = ShipmentDetail
        self.ShipmentDetail_nsprefix_ = "ns"
        if HandlingUnitGroups is None:
            self.HandlingUnitGroups = []
        else:
            self.HandlingUnitGroups = HandlingUnitGroups
        self.HandlingUnitGroups_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ValidateDangerousGoodsRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ValidateDangerousGoodsRequest.subclass:
            return ValidateDangerousGoodsRequest.subclass(*args_, **kwargs_)
        else:
            return ValidateDangerousGoodsRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_WebAuthenticationDetail(self):
        return self.WebAuthenticationDetail
    def set_WebAuthenticationDetail(self, WebAuthenticationDetail):
        self.WebAuthenticationDetail = WebAuthenticationDetail
    def get_ClientDetail(self):
        return self.ClientDetail
    def set_ClientDetail(self, ClientDetail):
        self.ClientDetail = ClientDetail
    def get_TransactionDetail(self):
        return self.TransactionDetail
    def set_TransactionDetail(self, TransactionDetail):
        self.TransactionDetail = TransactionDetail
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_ProcessingOptions(self):
        return self.ProcessingOptions
    def set_ProcessingOptions(self, ProcessingOptions):
        self.ProcessingOptions = ProcessingOptions
    def get_ShipmentDetail(self):
        return self.ShipmentDetail
    def set_ShipmentDetail(self, ShipmentDetail):
        self.ShipmentDetail = ShipmentDetail
    def get_HandlingUnitGroups(self):
        return self.HandlingUnitGroups
    def set_HandlingUnitGroups(self, HandlingUnitGroups):
        self.HandlingUnitGroups = HandlingUnitGroups
    def add_HandlingUnitGroups(self, value):
        self.HandlingUnitGroups.append(value)
    def insert_HandlingUnitGroups_at(self, index, value):
        self.HandlingUnitGroups.insert(index, value)
    def replace_HandlingUnitGroups_at(self, index, value):
        self.HandlingUnitGroups[index] = value
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.ProcessingOptions is not None or
            self.ShipmentDetail is not None or
            self.HandlingUnitGroups
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ValidateDangerousGoodsRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ValidateDangerousGoodsRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ValidateDangerousGoodsRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ValidateDangerousGoodsRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ValidateDangerousGoodsRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ValidateDangerousGoodsRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ValidateDangerousGoodsRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.WebAuthenticationDetail is not None:
            namespaceprefix_ = self.WebAuthenticationDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.WebAuthenticationDetail_nsprefix_) else ''
            self.WebAuthenticationDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='WebAuthenticationDetail', pretty_print=pretty_print)
        if self.ClientDetail is not None:
            namespaceprefix_ = self.ClientDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ClientDetail_nsprefix_) else ''
            self.ClientDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ClientDetail', pretty_print=pretty_print)
        if self.TransactionDetail is not None:
            namespaceprefix_ = self.TransactionDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionDetail_nsprefix_) else ''
            self.TransactionDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionDetail', pretty_print=pretty_print)
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.ProcessingOptions is not None:
            namespaceprefix_ = self.ProcessingOptions_nsprefix_ + ':' if (UseCapturedNS_ and self.ProcessingOptions_nsprefix_) else ''
            self.ProcessingOptions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ProcessingOptions', pretty_print=pretty_print)
        if self.ShipmentDetail is not None:
            namespaceprefix_ = self.ShipmentDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentDetail_nsprefix_) else ''
            self.ShipmentDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentDetail', pretty_print=pretty_print)
        for HandlingUnitGroups_ in self.HandlingUnitGroups:
            namespaceprefix_ = self.HandlingUnitGroups_nsprefix_ + ':' if (UseCapturedNS_ and self.HandlingUnitGroups_nsprefix_) else ''
            HandlingUnitGroups_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='HandlingUnitGroups', pretty_print=pretty_print)
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
        if nodeName_ == 'WebAuthenticationDetail':
            obj_ = WebAuthenticationDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.WebAuthenticationDetail = obj_
            obj_.original_tagname_ = 'WebAuthenticationDetail'
        elif nodeName_ == 'ClientDetail':
            obj_ = ClientDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ClientDetail = obj_
            obj_.original_tagname_ = 'ClientDetail'
        elif nodeName_ == 'TransactionDetail':
            obj_ = TransactionDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionDetail = obj_
            obj_.original_tagname_ = 'TransactionDetail'
        elif nodeName_ == 'Version':
            obj_ = VersionId.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'ProcessingOptions':
            obj_ = ValidateDangerousGoodsProcessingOptionsRequested.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ProcessingOptions = obj_
            obj_.original_tagname_ = 'ProcessingOptions'
        elif nodeName_ == 'ShipmentDetail':
            obj_ = UploadedDangerousGoodsShipmentDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentDetail = obj_
            obj_.original_tagname_ = 'ShipmentDetail'
        elif nodeName_ == 'HandlingUnitGroups':
            obj_ = UploadedDangerousGoodsHandlingUnitGroup.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.HandlingUnitGroups.append(obj_)
            obj_.original_tagname_ = 'HandlingUnitGroups'
# end class ValidateDangerousGoodsRequest


class Weight(GeneratedsSuper):
    """The descriptive data for the heaviness of an object."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Units=None, Value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Units = Units
        self.validate_WeightUnits(self.Units)
        self.Units_nsprefix_ = "ns"
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
    def get_Units(self):
        return self.Units
    def set_Units(self, Units):
        self.Units = Units
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def validate_WeightUnits(self, value):
        result = True
        # Validate type WeightUnits, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['KG', 'LB']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on WeightUnits' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.Units is not None or
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
        if self.Units is not None:
            namespaceprefix_ = self.Units_nsprefix_ + ':' if (UseCapturedNS_ and self.Units_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUnits>%s</%sUnits>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Units), input_name='Units')), namespaceprefix_ , eol_))
        if self.Value is not None:
            namespaceprefix_ = self.Value_nsprefix_ + ':' if (UseCapturedNS_ and self.Value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sValue>%s</%sValue>%s' % (namespaceprefix_ , self.gds_format_decimal(self.Value, input_name='Value'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Units':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Units')
            value_ = self.gds_validate_string(value_, node, 'Units')
            self.Units = value_
            self.Units_nsprefix_ = child_.prefix
            # validate type WeightUnits
            self.validate_WeightUnits(self.Units)
        elif nodeName_ == 'Value' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'Value')
            fval_ = self.gds_validate_decimal(fval_, node, 'Value')
            self.Value = fval_
            self.Value_nsprefix_ = child_.prefix
# end class Weight


class WebAuthenticationDetail(GeneratedsSuper):
    """Used in authentication of the sender's identity."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ParentCredential=None, UserCredential=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ParentCredential = ParentCredential
        self.ParentCredential_nsprefix_ = "ns"
        self.UserCredential = UserCredential
        self.UserCredential_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, WebAuthenticationDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if WebAuthenticationDetail.subclass:
            return WebAuthenticationDetail.subclass(*args_, **kwargs_)
        else:
            return WebAuthenticationDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ParentCredential(self):
        return self.ParentCredential
    def set_ParentCredential(self, ParentCredential):
        self.ParentCredential = ParentCredential
    def get_UserCredential(self):
        return self.UserCredential
    def set_UserCredential(self, UserCredential):
        self.UserCredential = UserCredential
    def hasContent_(self):
        if (
            self.ParentCredential is not None or
            self.UserCredential is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WebAuthenticationDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('WebAuthenticationDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'WebAuthenticationDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='WebAuthenticationDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='WebAuthenticationDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='WebAuthenticationDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WebAuthenticationDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ParentCredential is not None:
            namespaceprefix_ = self.ParentCredential_nsprefix_ + ':' if (UseCapturedNS_ and self.ParentCredential_nsprefix_) else ''
            self.ParentCredential.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ParentCredential', pretty_print=pretty_print)
        if self.UserCredential is not None:
            namespaceprefix_ = self.UserCredential_nsprefix_ + ':' if (UseCapturedNS_ and self.UserCredential_nsprefix_) else ''
            self.UserCredential.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UserCredential', pretty_print=pretty_print)
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
        if nodeName_ == 'ParentCredential':
            obj_ = WebAuthenticationCredential.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ParentCredential = obj_
            obj_.original_tagname_ = 'ParentCredential'
        elif nodeName_ == 'UserCredential':
            obj_ = WebAuthenticationCredential.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UserCredential = obj_
            obj_.original_tagname_ = 'UserCredential'
# end class WebAuthenticationDetail


class WebAuthenticationCredential(GeneratedsSuper):
    """Two part authentication string used for the sender's identity"""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Key=None, Password=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Key = Key
        self.Key_nsprefix_ = None
        self.Password = Password
        self.Password_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, WebAuthenticationCredential)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if WebAuthenticationCredential.subclass:
            return WebAuthenticationCredential.subclass(*args_, **kwargs_)
        else:
            return WebAuthenticationCredential(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Key(self):
        return self.Key
    def set_Key(self, Key):
        self.Key = Key
    def get_Password(self):
        return self.Password
    def set_Password(self, Password):
        self.Password = Password
    def hasContent_(self):
        if (
            self.Key is not None or
            self.Password is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WebAuthenticationCredential', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('WebAuthenticationCredential')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'WebAuthenticationCredential':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='WebAuthenticationCredential')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='WebAuthenticationCredential', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='WebAuthenticationCredential'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WebAuthenticationCredential', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Key is not None:
            namespaceprefix_ = self.Key_nsprefix_ + ':' if (UseCapturedNS_ and self.Key_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sKey>%s</%sKey>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Key), input_name='Key')), namespaceprefix_ , eol_))
        if self.Password is not None:
            namespaceprefix_ = self.Password_nsprefix_ + ':' if (UseCapturedNS_ and self.Password_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPassword>%s</%sPassword>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Password), input_name='Password')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Key':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Key')
            value_ = self.gds_validate_string(value_, node, 'Key')
            self.Key = value_
            self.Key_nsprefix_ = child_.prefix
        elif nodeName_ == 'Password':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Password')
            value_ = self.gds_validate_string(value_, node, 'Password')
            self.Password = value_
            self.Password_nsprefix_ = child_.prefix
# end class WebAuthenticationCredential


class VersionId(GeneratedsSuper):
    """Identifies the version/level of a service operation expected by a caller
    (in each request) and performed by the callee (in each reply)."""
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ServiceId=None, Major=None, Intermediate=None, Minor=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ServiceId = ServiceId
        self.ServiceId_nsprefix_ = None
        self.Major = Major
        self.Major_nsprefix_ = None
        self.Intermediate = Intermediate
        self.Intermediate_nsprefix_ = None
        self.Minor = Minor
        self.Minor_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, VersionId)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if VersionId.subclass:
            return VersionId.subclass(*args_, **kwargs_)
        else:
            return VersionId(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ServiceId(self):
        return self.ServiceId
    def set_ServiceId(self, ServiceId):
        self.ServiceId = ServiceId
    def get_Major(self):
        return self.Major
    def set_Major(self, Major):
        self.Major = Major
    def get_Intermediate(self):
        return self.Intermediate
    def set_Intermediate(self, Intermediate):
        self.Intermediate = Intermediate
    def get_Minor(self):
        return self.Minor
    def set_Minor(self, Minor):
        self.Minor = Minor
    def hasContent_(self):
        if (
            self.ServiceId is not None or
            self.Major is not None or
            self.Intermediate is not None or
            self.Minor is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='VersionId', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('VersionId')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'VersionId':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='VersionId')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='VersionId', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='VersionId'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='VersionId', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ServiceId is not None:
            namespaceprefix_ = self.ServiceId_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceId>%s</%sServiceId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServiceId), input_name='ServiceId')), namespaceprefix_ , eol_))
        if self.Major is not None:
            namespaceprefix_ = self.Major_nsprefix_ + ':' if (UseCapturedNS_ and self.Major_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMajor>%s</%sMajor>%s' % (namespaceprefix_ , self.gds_format_integer(self.Major, input_name='Major'), namespaceprefix_ , eol_))
        if self.Intermediate is not None:
            namespaceprefix_ = self.Intermediate_nsprefix_ + ':' if (UseCapturedNS_ and self.Intermediate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIntermediate>%s</%sIntermediate>%s' % (namespaceprefix_ , self.gds_format_integer(self.Intermediate, input_name='Intermediate'), namespaceprefix_ , eol_))
        if self.Minor is not None:
            namespaceprefix_ = self.Minor_nsprefix_ + ':' if (UseCapturedNS_ and self.Minor_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMinor>%s</%sMinor>%s' % (namespaceprefix_ , self.gds_format_integer(self.Minor, input_name='Minor'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ServiceId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServiceId')
            value_ = self.gds_validate_string(value_, node, 'ServiceId')
            self.ServiceId = value_
            self.ServiceId_nsprefix_ = child_.prefix
        elif nodeName_ == 'Major' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Major')
            ival_ = self.gds_validate_integer(ival_, node, 'Major')
            self.Major = ival_
            self.Major_nsprefix_ = child_.prefix
        elif nodeName_ == 'Intermediate' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Intermediate')
            ival_ = self.gds_validate_integer(ival_, node, 'Intermediate')
            self.Intermediate = ival_
            self.Intermediate_nsprefix_ = child_.prefix
        elif nodeName_ == 'Minor' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Minor')
            ival_ = self.gds_validate_integer(ival_, node, 'Minor')
            self.Minor = ival_
            self.Minor_nsprefix_ = child_.prefix
# end class VersionId


GDSClassesMapping = {
    'AddDangerousGoodsHandlingUnitReply': AddDangerousGoodsHandlingUnitReply,
    'AddDangerousGoodsHandlingUnitRequest': AddDangerousGoodsHandlingUnitRequest,
    'DeleteDangerousGoodsHandlingUnitReply': DeleteDangerousGoodsHandlingUnitReply,
    'DeleteDangerousGoodsHandlingUnitRequest': DeleteDangerousGoodsHandlingUnitRequest,
    'DeleteDangerousGoodsReply': DeleteDangerousGoodsReply,
    'DeleteDangerousGoodsRequest': DeleteDangerousGoodsRequest,
    'ModifyDangerousGoodsHandlingUnitReply': ModifyDangerousGoodsHandlingUnitReply,
    'ModifyDangerousGoodsHandlingUnitRequest': ModifyDangerousGoodsHandlingUnitRequest,
    'ModifyDangerousGoodsShipmentReply': ModifyDangerousGoodsShipmentReply,
    'ModifyDangerousGoodsShipmentRequest': ModifyDangerousGoodsShipmentRequest,
    'RetrieveDangerousGoodsReply': RetrieveDangerousGoodsReply,
    'RetrieveDangerousGoodsRequest': RetrieveDangerousGoodsRequest,
    'UploadDangerousGoodsReply': UploadDangerousGoodsReply,
    'UploadDangerousGoodsRequest': UploadDangerousGoodsRequest,
    'ValidateDangerousGoodsReply': ValidateDangerousGoodsReply,
    'ValidateDangerousGoodsRequest': ValidateDangerousGoodsRequest,
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
        rootTag = 'AddDangerousGoodsHandlingUnitReply'
        rootClass = AddDangerousGoodsHandlingUnitReply
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
        rootTag = 'AddDangerousGoodsHandlingUnitReply'
        rootClass = AddDangerousGoodsHandlingUnitReply
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
        rootTag = 'AddDangerousGoodsHandlingUnitReply'
        rootClass = AddDangerousGoodsHandlingUnitReply
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:ns="http://fedex.com/ws/dgds/v5"')
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
        rootTag = 'AddDangerousGoodsHandlingUnitReply'
        rootClass = AddDangerousGoodsHandlingUnitReply
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from dgds_service_v5 import *\n\n')
        sys.stdout.write('import dgds_service_v5 as model_\n\n')
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
NamespaceToDefMappings_ = {'http://fedex.com/ws/dgds/v5': [('CarrierCodeType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('DangerousGoodsAccessibilityType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('DangerousGoodsAircraftCategoryType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('DangerousGoodsContainerAttributeType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('DangerousGoodsDescriptorType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('DangerousGoodsHandlingUnitAttributeType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('DangerousGoodsPackingGroupType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('DangerousGoodsRegulationAttributeType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('ExpressRegionCode',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('HazardousCommodityOptionType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('HazardousCommodityRegulationType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('NetExplosiveClassificationType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('NotificationSeverityType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('PhysicalFormType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('RadioactiveLabelType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('RadioactivityUnitOfMeasure',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('ShipmentDryIceProcessingOptionType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('TrackingIdType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('UploadDangerousGoodsProcessingOptionType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('UploadedDangerousGoodsShipmentAttributeType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('ValidateDangerousGoodsProcessingOptionType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('WeightUnits',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'ST'),
                                 ('AddDangerousGoodsHandlingUnitReply',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('AddDangerousGoodsHandlingUnitRequest',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('Address',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('AssociatedEnterpriseDocumentDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('ClientDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('CompletedDangerousGoodsHandlingUnitGroup',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('CompletedDangerousGoodsShipmentDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('Contact',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('DangerousGoodsHandlingUnitShippingDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('DangerousGoodsInnerReceptacleDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('DangerousGoodsRadionuclideActivity',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('DangerousGoodsRadionuclideDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('DangerousGoodsSignatory',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('DeleteDangerousGoodsHandlingUnitReply',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('DeleteDangerousGoodsHandlingUnitRequest',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('DeleteDangerousGoodsReply',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('DeleteDangerousGoodsRequest',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('Localization',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('ModifyDangerousGoodsHandlingUnitReply',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('ModifyDangerousGoodsHandlingUnitRequest',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('ModifyDangerousGoodsShipmentReply',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('ModifyDangerousGoodsShipmentRequest',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('NetExplosiveDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('Notification',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('NotificationParameter',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('PreciseQuantity',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('RadioactiveDangerousGoodsHandlingUnitDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('RecordedDangerousGoodsHandlingUnitGroup',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('RecordedDangerousGoodsShipmentDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('RetrieveDangerousGoodsReply',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('RetrieveDangerousGoodsRequest',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('ShipmentDryIceDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('ShipmentDryIceProcessingOptionsRequested',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('TrackingId',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('TrackingNumberUnit',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('TransactionDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('UploadDangerousGoodsProcessingOptionsRequested',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('UploadDangerousGoodsReply',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('UploadDangerousGoodsRequest',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('UploadedDangerousGoodsCommodityContent',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('UploadedDangerousGoodsCommodityDescription',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('UploadedDangerousGoodsContainer',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('UploadedDangerousGoodsContainerGroup',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('UploadedDangerousGoodsHandlingUnit',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('UploadedDangerousGoodsHandlingUnitGroup',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('UploadedDangerousGoodsShipmentDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('ValidateDangerousGoodsProcessingOptionsRequested',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('ValidateDangerousGoodsReply',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('ValidateDangerousGoodsRequest',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('Weight',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('WebAuthenticationDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('WebAuthenticationCredential',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT'),
                                 ('VersionId',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGDSService_v5.xsd',
                                  'CT')]}

__all__ = [
    "AddDangerousGoodsHandlingUnitReply",
    "AddDangerousGoodsHandlingUnitRequest",
    "Address",
    "AssociatedEnterpriseDocumentDetail",
    "ClientDetail",
    "CompletedDangerousGoodsHandlingUnitGroup",
    "CompletedDangerousGoodsShipmentDetail",
    "Contact",
    "DangerousGoodsHandlingUnitShippingDetail",
    "DangerousGoodsInnerReceptacleDetail",
    "DangerousGoodsRadionuclideActivity",
    "DangerousGoodsRadionuclideDetail",
    "DangerousGoodsSignatory",
    "DeleteDangerousGoodsHandlingUnitReply",
    "DeleteDangerousGoodsHandlingUnitRequest",
    "DeleteDangerousGoodsReply",
    "DeleteDangerousGoodsRequest",
    "Localization",
    "ModifyDangerousGoodsHandlingUnitReply",
    "ModifyDangerousGoodsHandlingUnitRequest",
    "ModifyDangerousGoodsShipmentReply",
    "ModifyDangerousGoodsShipmentRequest",
    "NetExplosiveDetail",
    "Notification",
    "NotificationParameter",
    "PreciseQuantity",
    "RadioactiveDangerousGoodsHandlingUnitDetail",
    "RecordedDangerousGoodsHandlingUnitGroup",
    "RecordedDangerousGoodsShipmentDetail",
    "RetrieveDangerousGoodsReply",
    "RetrieveDangerousGoodsRequest",
    "ShipmentDryIceDetail",
    "ShipmentDryIceProcessingOptionsRequested",
    "TrackingId",
    "TrackingNumberUnit",
    "TransactionDetail",
    "UploadDangerousGoodsProcessingOptionsRequested",
    "UploadDangerousGoodsReply",
    "UploadDangerousGoodsRequest",
    "UploadedDangerousGoodsCommodityContent",
    "UploadedDangerousGoodsCommodityDescription",
    "UploadedDangerousGoodsContainer",
    "UploadedDangerousGoodsContainerGroup",
    "UploadedDangerousGoodsHandlingUnit",
    "UploadedDangerousGoodsHandlingUnitGroup",
    "UploadedDangerousGoodsShipmentDetail",
    "ValidateDangerousGoodsProcessingOptionsRequested",
    "ValidateDangerousGoodsReply",
    "ValidateDangerousGoodsRequest",
    "VersionId",
    "WebAuthenticationCredential",
    "WebAuthenticationDetail",
    "Weight"
]
