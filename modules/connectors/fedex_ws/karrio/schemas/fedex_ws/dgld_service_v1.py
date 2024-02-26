#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Thu May  6 11:00:03 2021 by generateDS.py version 2.38.6.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './fedex_lib/dgld_service_v1.py')
#
# Command line arguments:
#   /Users/danielkobina/Workspace/Carriers Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./fedex_lib/dgld_service_v1.py" /Users/danielkobina/Workspace/Carriers Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd
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


class NotificationSeverityType(str, Enum):
    ERROR='ERROR'
    FAILURE='FAILURE'
    NOTE='NOTE'
    SUCCESS='SUCCESS'
    WARNING='WARNING'


class ServiceType(str, Enum):
    EUROPE_FIRST_INTERNATIONAL_PRIORITY='EUROPE_FIRST_INTERNATIONAL_PRIORITY'
    FEDEX__1_DAY_FREIGHT='FEDEX_1_DAY_FREIGHT'
    FEDEX__2_DAY='FEDEX_2_DAY'
    FEDEX__2_DAY_AM='FEDEX_2_DAY_AM'
    FEDEX__2_DAY_FREIGHT='FEDEX_2_DAY_FREIGHT'
    FEDEX__3_DAY_FREIGHT='FEDEX_3_DAY_FREIGHT'
    FEDEX_CARGO_AIRPORT_TO_AIRPORT='FEDEX_CARGO_AIRPORT_TO_AIRPORT'
    FEDEX_CARGO_FREIGHT_FORWARDING='FEDEX_CARGO_FREIGHT_FORWARDING'
    FEDEX_CARGO_INTERNATIONAL_EXPRESS_FREIGHT='FEDEX_CARGO_INTERNATIONAL_EXPRESS_FREIGHT'
    FEDEX_CARGO_INTERNATIONAL_PREMIUM='FEDEX_CARGO_INTERNATIONAL_PREMIUM'
    FEDEX_CARGO_MAIL='FEDEX_CARGO_MAIL'
    FEDEX_CARGO_REGISTERED_MAIL='FEDEX_CARGO_REGISTERED_MAIL'
    FEDEX_CARGO_SURFACE_MAIL='FEDEX_CARGO_SURFACE_MAIL'
    FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE='FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE'
    FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE_EXCLUSIVE_USE='FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE_EXCLUSIVE_USE'
    FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE_NETWORK='FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE_NETWORK'
    FEDEX_CUSTOM_CRITICAL_CHARTER_AIR='FEDEX_CUSTOM_CRITICAL_CHARTER_AIR'
    FEDEX_CUSTOM_CRITICAL_POINT_TO_POINT='FEDEX_CUSTOM_CRITICAL_POINT_TO_POINT'
    FEDEX_CUSTOM_CRITICAL_SURFACE_EXPEDITE='FEDEX_CUSTOM_CRITICAL_SURFACE_EXPEDITE'
    FEDEX_CUSTOM_CRITICAL_SURFACE_EXPEDITE_EXCLUSIVE_USE='FEDEX_CUSTOM_CRITICAL_SURFACE_EXPEDITE_EXCLUSIVE_USE'
    FEDEX_CUSTOM_CRITICAL_TEMP_ASSURE_AIR='FEDEX_CUSTOM_CRITICAL_TEMP_ASSURE_AIR'
    FEDEX_CUSTOM_CRITICAL_TEMP_ASSURE_VALIDATED_AIR='FEDEX_CUSTOM_CRITICAL_TEMP_ASSURE_VALIDATED_AIR'
    FEDEX_CUSTOM_CRITICAL_WHITE_GLOVE_SERVICES='FEDEX_CUSTOM_CRITICAL_WHITE_GLOVE_SERVICES'
    FEDEX_DISTANCE_DEFERRED='FEDEX_DISTANCE_DEFERRED'
    FEDEX_EXPRESS_SAVER='FEDEX_EXPRESS_SAVER'
    FEDEX_FIRST_FREIGHT='FEDEX_FIRST_FREIGHT'
    FEDEX_FREIGHT_ECONOMY='FEDEX_FREIGHT_ECONOMY'
    FEDEX_FREIGHT_PRIORITY='FEDEX_FREIGHT_PRIORITY'
    FEDEX_GROUND='FEDEX_GROUND'
    FEDEX_INTERNATIONAL_PRIORITY_PLUS='FEDEX_INTERNATIONAL_PRIORITY_PLUS'
    FEDEX_NEXT_DAY_AFTERNOON='FEDEX_NEXT_DAY_AFTERNOON'
    FEDEX_NEXT_DAY_EARLY_MORNING='FEDEX_NEXT_DAY_EARLY_MORNING'
    FEDEX_NEXT_DAY_END_OF_DAY='FEDEX_NEXT_DAY_END_OF_DAY'
    FEDEX_NEXT_DAY_FREIGHT='FEDEX_NEXT_DAY_FREIGHT'
    FEDEX_NEXT_DAY_MID_MORNING='FEDEX_NEXT_DAY_MID_MORNING'
    FIRST_OVERNIGHT='FIRST_OVERNIGHT'
    GROUND_HOME_DELIVERY='GROUND_HOME_DELIVERY'
    INTERNATIONAL_DISTRIBUTION_FREIGHT='INTERNATIONAL_DISTRIBUTION_FREIGHT'
    INTERNATIONAL_ECONOMY='INTERNATIONAL_ECONOMY'
    INTERNATIONAL_ECONOMY_DISTRIBUTION='INTERNATIONAL_ECONOMY_DISTRIBUTION'
    INTERNATIONAL_ECONOMY_FREIGHT='INTERNATIONAL_ECONOMY_FREIGHT'
    INTERNATIONAL_FIRST='INTERNATIONAL_FIRST'
    INTERNATIONAL_PRIORITY='INTERNATIONAL_PRIORITY'
    INTERNATIONAL_PRIORITY_DISTRIBUTION='INTERNATIONAL_PRIORITY_DISTRIBUTION'
    INTERNATIONAL_PRIORITY_FREIGHT='INTERNATIONAL_PRIORITY_FREIGHT'
    PRIORITY_OVERNIGHT='PRIORITY_OVERNIGHT'
    SAME_DAY='SAME_DAY'
    SAME_DAY_CITY='SAME_DAY_CITY'
    SAME_DAY_METRO_AFTERNOON='SAME_DAY_METRO_AFTERNOON'
    SAME_DAY_METRO_MORNING='SAME_DAY_METRO_MORNING'
    SAME_DAY_METRO_RUSH='SAME_DAY_METRO_RUSH'
    SMART_POST='SMART_POST'
    STANDARD_OVERNIGHT='STANDARD_OVERNIGHT'
    TRANSBORDER_DISTRIBUTION_CONSOLIDATION='TRANSBORDER_DISTRIBUTION_CONSOLIDATION'


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


class ListDangerousGoodsDetail(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TrackingNumbers=None, Description=None, Accessibility=None, Options=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if TrackingNumbers is None:
            self.TrackingNumbers = []
        else:
            self.TrackingNumbers = TrackingNumbers
        self.TrackingNumbers_nsprefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = None
        self.Accessibility = Accessibility
        self.validate_DangerousGoodsAccessibilityType(self.Accessibility)
        self.Accessibility_nsprefix_ = "ns"
        if Options is None:
            self.Options = []
        else:
            self.Options = Options
        self.Options_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ListDangerousGoodsDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ListDangerousGoodsDetail.subclass:
            return ListDangerousGoodsDetail.subclass(*args_, **kwargs_)
        else:
            return ListDangerousGoodsDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
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
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
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
            self.TrackingNumbers or
            self.Description is not None or
            self.Accessibility is not None or
            self.Options
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ListDangerousGoodsDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ListDangerousGoodsDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ListDangerousGoodsDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ListDangerousGoodsDetail')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ListDangerousGoodsDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ListDangerousGoodsDetail'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ListDangerousGoodsDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for TrackingNumbers_ in self.TrackingNumbers:
            namespaceprefix_ = self.TrackingNumbers_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackingNumbers_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTrackingNumbers>%s</%sTrackingNumbers>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(TrackingNumbers_), input_name='TrackingNumbers')), namespaceprefix_ , eol_))
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
        if self.Accessibility is not None:
            namespaceprefix_ = self.Accessibility_nsprefix_ + ':' if (UseCapturedNS_ and self.Accessibility_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccessibility>%s</%sAccessibility>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Accessibility), input_name='Accessibility')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'TrackingNumbers':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TrackingNumbers')
            value_ = self.gds_validate_string(value_, node, 'TrackingNumbers')
            self.TrackingNumbers.append(value_)
            self.TrackingNumbers_nsprefix_ = child_.prefix
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
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
# end class ListDangerousGoodsDetail


class ListDangerousGoodsReply(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HighestSeverity=None, Notifications=None, TransactionDetail=None, Version=None, Regulation=None, Accessibility=None, Options=None, Details=None, gds_collector_=None, **kwargs_):
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
        self.Regulation = Regulation
        self.validate_HazardousCommodityRegulationType(self.Regulation)
        self.Regulation_nsprefix_ = "ns"
        self.Accessibility = Accessibility
        self.validate_DangerousGoodsAccessibilityType(self.Accessibility)
        self.Accessibility_nsprefix_ = "ns"
        if Options is None:
            self.Options = []
        else:
            self.Options = Options
        self.Options_nsprefix_ = "ns"
        if Details is None:
            self.Details = []
        else:
            self.Details = Details
        self.Details_nsprefix_ = "ns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ListDangerousGoodsReply)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ListDangerousGoodsReply.subclass:
            return ListDangerousGoodsReply.subclass(*args_, **kwargs_)
        else:
            return ListDangerousGoodsReply(*args_, **kwargs_)
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
    def get_Regulation(self):
        return self.Regulation
    def set_Regulation(self, Regulation):
        self.Regulation = Regulation
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
    def get_Details(self):
        return self.Details
    def set_Details(self, Details):
        self.Details = Details
    def add_Details(self, value):
        self.Details.append(value)
    def insert_Details_at(self, index, value):
        self.Details.insert(index, value)
    def replace_Details_at(self, index, value):
        self.Details[index] = value
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
            self.HighestSeverity is not None or
            self.Notifications or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.Regulation is not None or
            self.Accessibility is not None or
            self.Options or
            self.Details
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ListDangerousGoodsReply', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ListDangerousGoodsReply')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ListDangerousGoodsReply':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ListDangerousGoodsReply')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ListDangerousGoodsReply', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ListDangerousGoodsReply'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ListDangerousGoodsReply', fromsubclass_=False, pretty_print=True):
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
        if self.Regulation is not None:
            namespaceprefix_ = self.Regulation_nsprefix_ + ':' if (UseCapturedNS_ and self.Regulation_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRegulation>%s</%sRegulation>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Regulation), input_name='Regulation')), namespaceprefix_ , eol_))
        if self.Accessibility is not None:
            namespaceprefix_ = self.Accessibility_nsprefix_ + ':' if (UseCapturedNS_ and self.Accessibility_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccessibility>%s</%sAccessibility>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Accessibility), input_name='Accessibility')), namespaceprefix_ , eol_))
        for Options_ in self.Options:
            namespaceprefix_ = self.Options_nsprefix_ + ':' if (UseCapturedNS_ and self.Options_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOptions>%s</%sOptions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(Options_), input_name='Options')), namespaceprefix_ , eol_))
        for Details_ in self.Details:
            namespaceprefix_ = self.Details_nsprefix_ + ':' if (UseCapturedNS_ and self.Details_nsprefix_) else ''
            Details_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Details', pretty_print=pretty_print)
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
        elif nodeName_ == 'Regulation':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Regulation')
            value_ = self.gds_validate_string(value_, node, 'Regulation')
            self.Regulation = value_
            self.Regulation_nsprefix_ = child_.prefix
            # validate type HazardousCommodityRegulationType
            self.validate_HazardousCommodityRegulationType(self.Regulation)
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
        elif nodeName_ == 'Details':
            obj_ = ListDangerousGoodsDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Details.append(obj_)
            obj_.original_tagname_ = 'Details'
# end class ListDangerousGoodsReply


class ListDangerousGoodsRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, WebAuthenticationDetail=None, ClientDetail=None, TransactionDetail=None, Version=None, Origin=None, Destination=None, CarrierCode=None, ServiceType=None, ShipDate=None, TrackingNumber=None, gds_collector_=None, **kwargs_):
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
        self.Origin = Origin
        self.Origin_nsprefix_ = "ns"
        self.Destination = Destination
        self.Destination_nsprefix_ = "ns"
        self.CarrierCode = CarrierCode
        self.validate_CarrierCodeType(self.CarrierCode)
        self.CarrierCode_nsprefix_ = "ns"
        self.ServiceType = ServiceType
        self.validate_ServiceType(self.ServiceType)
        self.ServiceType_nsprefix_ = "ns"
        if isinstance(ShipDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ShipDate, '%Y-%m-%d').date()
        else:
            initvalue_ = ShipDate
        self.ShipDate = initvalue_
        self.ShipDate_nsprefix_ = None
        self.TrackingNumber = TrackingNumber
        self.TrackingNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ListDangerousGoodsRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ListDangerousGoodsRequest.subclass:
            return ListDangerousGoodsRequest.subclass(*args_, **kwargs_)
        else:
            return ListDangerousGoodsRequest(*args_, **kwargs_)
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
    def get_TrackingNumber(self):
        return self.TrackingNumber
    def set_TrackingNumber(self, TrackingNumber):
        self.TrackingNumber = TrackingNumber
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
    def validate_ServiceType(self, value):
        result = True
        # Validate type ServiceType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['EUROPE_FIRST_INTERNATIONAL_PRIORITY', 'FEDEX_1_DAY_FREIGHT', 'FEDEX_2_DAY', 'FEDEX_2_DAY_AM', 'FEDEX_2_DAY_FREIGHT', 'FEDEX_3_DAY_FREIGHT', 'FEDEX_CARGO_AIRPORT_TO_AIRPORT', 'FEDEX_CARGO_FREIGHT_FORWARDING', 'FEDEX_CARGO_INTERNATIONAL_EXPRESS_FREIGHT', 'FEDEX_CARGO_INTERNATIONAL_PREMIUM', 'FEDEX_CARGO_MAIL', 'FEDEX_CARGO_REGISTERED_MAIL', 'FEDEX_CARGO_SURFACE_MAIL', 'FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE', 'FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE_EXCLUSIVE_USE', 'FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE_NETWORK', 'FEDEX_CUSTOM_CRITICAL_CHARTER_AIR', 'FEDEX_CUSTOM_CRITICAL_POINT_TO_POINT', 'FEDEX_CUSTOM_CRITICAL_SURFACE_EXPEDITE', 'FEDEX_CUSTOM_CRITICAL_SURFACE_EXPEDITE_EXCLUSIVE_USE', 'FEDEX_CUSTOM_CRITICAL_TEMP_ASSURE_AIR', 'FEDEX_CUSTOM_CRITICAL_TEMP_ASSURE_VALIDATED_AIR', 'FEDEX_CUSTOM_CRITICAL_WHITE_GLOVE_SERVICES', 'FEDEX_DISTANCE_DEFERRED', 'FEDEX_EXPRESS_SAVER', 'FEDEX_FIRST_FREIGHT', 'FEDEX_FREIGHT_ECONOMY', 'FEDEX_FREIGHT_PRIORITY', 'FEDEX_GROUND', 'FEDEX_INTERNATIONAL_PRIORITY_PLUS', 'FEDEX_NEXT_DAY_AFTERNOON', 'FEDEX_NEXT_DAY_EARLY_MORNING', 'FEDEX_NEXT_DAY_END_OF_DAY', 'FEDEX_NEXT_DAY_FREIGHT', 'FEDEX_NEXT_DAY_MID_MORNING', 'FIRST_OVERNIGHT', 'GROUND_HOME_DELIVERY', 'INTERNATIONAL_DISTRIBUTION_FREIGHT', 'INTERNATIONAL_ECONOMY', 'INTERNATIONAL_ECONOMY_DISTRIBUTION', 'INTERNATIONAL_ECONOMY_FREIGHT', 'INTERNATIONAL_FIRST', 'INTERNATIONAL_PRIORITY', 'INTERNATIONAL_PRIORITY_DISTRIBUTION', 'INTERNATIONAL_PRIORITY_FREIGHT', 'PRIORITY_OVERNIGHT', 'SAME_DAY', 'SAME_DAY_CITY', 'SAME_DAY_METRO_AFTERNOON', 'SAME_DAY_METRO_MORNING', 'SAME_DAY_METRO_RUSH', 'SMART_POST', 'STANDARD_OVERNIGHT', 'TRANSBORDER_DISTRIBUTION_CONSOLIDATION']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ServiceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def hasContent_(self):
        if (
            self.WebAuthenticationDetail is not None or
            self.ClientDetail is not None or
            self.TransactionDetail is not None or
            self.Version is not None or
            self.Origin is not None or
            self.Destination is not None or
            self.CarrierCode is not None or
            self.ServiceType is not None or
            self.ShipDate is not None or
            self.TrackingNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ListDangerousGoodsRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ListDangerousGoodsRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ListDangerousGoodsRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ListDangerousGoodsRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ListDangerousGoodsRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ListDangerousGoodsRequest'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ListDangerousGoodsRequest', fromsubclass_=False, pretty_print=True):
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
            # validate type ServiceType
            self.validate_ServiceType(self.ServiceType)
        elif nodeName_ == 'ShipDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.ShipDate = dval_
            self.ShipDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'TrackingNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TrackingNumber')
            value_ = self.gds_validate_string(value_, node, 'TrackingNumber')
            self.TrackingNumber = value_
            self.TrackingNumber_nsprefix_ = child_.prefix
# end class ListDangerousGoodsRequest


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
    'ListDangerousGoodsReply': ListDangerousGoodsReply,
    'ListDangerousGoodsRequest': ListDangerousGoodsRequest,
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
        rootTag = 'ListDangerousGoodsReply'
        rootClass = ListDangerousGoodsReply
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
        rootTag = 'ListDangerousGoodsReply'
        rootClass = ListDangerousGoodsReply
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
        rootTag = 'ListDangerousGoodsReply'
        rootClass = ListDangerousGoodsReply
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:ns="http://fedex.com/ws/dgld/v1"')
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
        rootTag = 'ListDangerousGoodsReply'
        rootClass = ListDangerousGoodsReply
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from dgld_service_v1 import *\n\n')
        sys.stdout.write('import dgld_service_v1 as model_\n\n')
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
NamespaceToDefMappings_ = {'http://fedex.com/ws/dgld/v1': [('CarrierCodeType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'ST'),
                                 ('DangerousGoodsAccessibilityType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'ST'),
                                 ('ExpressRegionCode',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'ST'),
                                 ('HazardousCommodityOptionType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'ST'),
                                 ('HazardousCommodityRegulationType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'ST'),
                                 ('NotificationSeverityType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'ST'),
                                 ('ServiceType',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'ST'),
                                 ('Address',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'CT'),
                                 ('ClientDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'CT'),
                                 ('ListDangerousGoodsDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'CT'),
                                 ('ListDangerousGoodsReply',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'CT'),
                                 ('ListDangerousGoodsRequest',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'CT'),
                                 ('Localization',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'CT'),
                                 ('Notification',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'CT'),
                                 ('NotificationParameter',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'CT'),
                                 ('TransactionDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'CT'),
                                 ('WebAuthenticationDetail',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'CT'),
                                 ('WebAuthenticationCredential',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'CT'),
                                 ('VersionId',
                                  '../../../Carriers '
                                  'Doc/Fedex/2020-09/schemas/DGLDService_v1.xsd',
                                  'CT')]}

__all__ = [
    "Address",
    "ClientDetail",
    "ListDangerousGoodsDetail",
    "ListDangerousGoodsReply",
    "ListDangerousGoodsRequest",
    "Localization",
    "Notification",
    "NotificationParameter",
    "TransactionDetail",
    "VersionId",
    "WebAuthenticationCredential",
    "WebAuthenticationDetail"
]
