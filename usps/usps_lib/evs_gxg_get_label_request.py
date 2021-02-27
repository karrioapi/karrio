#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Fri Feb 26 09:55:19 2021 by generateDS.py version 2.37.16.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', 'usps_lib/evs_gxg_get_label_request.py')
#
# Command line arguments:
#   schemas/eVSGXGGetLabelRequest.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "usps_lib/evs_gxg_get_label_request.py" schemas/eVSGXGGetLabelRequest.xsd
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


class eVSGXGGetLabelRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, USERID=None, PASSWORD=None, Option=None, Revision=None, ImageParameters=None, FromFirstName=None, FromMiddleInitial=None, FromLastName=None, FromFirm=None, FromAddress1=None, FromAddress2=None, FromUrbanization=None, FromCity=None, FromState=None, FromZIP5=None, FromZIP4=None, FromPhone=None, ShipFromZIP=None, SenderEMail=None, ToFirstName=None, ToLastName=None, ToFirm=None, ToAddress1=None, ToAddress2=None, ToAddress3=None, ToPostalCode=None, ToPhone=None, RecipientEMail=None, ToDPID=None, ToProvince=None, ToTaxID=None, Container=None, ContentType=None, ShippingContents=None, PurposeOfShipment=None, PartiesToTransaction=None, Agreement=None, Postage=None, InsuredValue=None, GrossPounds=None, GrossOunces=None, Length=None, Width=None, Height=None, Girth=None, Shape=None, CIRequired=None, InvoiceDate=None, InvoiceNumber=None, CustomerOrderNumber=None, CustOrderNumber=None, TermsDelivery=None, TermsDeliveryOther=None, PackingCost=None, CountryUltDest=None, CIAgreement=None, ImageType=None, ImageLayout=None, CustomerRefNo=None, CustomerRefNo2=None, ShipDate=None, HoldForManifest=None, PriceOptions=None, CommercialShipment=None, BuyerFirstName=None, BuyerLastName=None, BuyerAddress1=None, BuyerAddress2=None, BuyerAddress3=None, BuyerCity=None, BuyerState=None, BuyerPostalCode=None, BuyerCountry=None, BuyerTaxID=None, BuyerRecipient=None, TermsPayment=None, ActionCode=None, OptOutOfSPE=None, PermitNumber=None, AccountZipCode=None, Machinable=None, DestinationRateIndicator=None, MID=None, LogisticsManagerMID=None, CRID=None, VendorCode=None, VendorProductVersionNumber=None, OverrideMID=None, ChargebackCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.USERID = _cast(None, USERID)
        self.USERID_nsprefix_ = None
        self.PASSWORD = _cast(None, PASSWORD)
        self.PASSWORD_nsprefix_ = None
        self.Option = Option
        self.Option_nsprefix_ = None
        self.Revision = Revision
        self.Revision_nsprefix_ = None
        self.ImageParameters = ImageParameters
        self.ImageParameters_nsprefix_ = None
        self.FromFirstName = FromFirstName
        self.FromFirstName_nsprefix_ = None
        self.FromMiddleInitial = FromMiddleInitial
        self.FromMiddleInitial_nsprefix_ = None
        self.FromLastName = FromLastName
        self.FromLastName_nsprefix_ = None
        self.FromFirm = FromFirm
        self.FromFirm_nsprefix_ = None
        self.FromAddress1 = FromAddress1
        self.FromAddress1_nsprefix_ = None
        self.FromAddress2 = FromAddress2
        self.FromAddress2_nsprefix_ = None
        self.FromUrbanization = FromUrbanization
        self.FromUrbanization_nsprefix_ = None
        self.FromCity = FromCity
        self.FromCity_nsprefix_ = None
        self.FromState = FromState
        self.FromState_nsprefix_ = None
        self.FromZIP5 = FromZIP5
        self.FromZIP5_nsprefix_ = None
        self.FromZIP4 = FromZIP4
        self.FromZIP4_nsprefix_ = None
        self.FromPhone = FromPhone
        self.FromPhone_nsprefix_ = None
        self.ShipFromZIP = ShipFromZIP
        self.ShipFromZIP_nsprefix_ = None
        self.SenderEMail = SenderEMail
        self.SenderEMail_nsprefix_ = None
        self.ToFirstName = ToFirstName
        self.ToFirstName_nsprefix_ = None
        self.ToLastName = ToLastName
        self.ToLastName_nsprefix_ = None
        self.ToFirm = ToFirm
        self.ToFirm_nsprefix_ = None
        self.ToAddress1 = ToAddress1
        self.ToAddress1_nsprefix_ = None
        self.ToAddress2 = ToAddress2
        self.ToAddress2_nsprefix_ = None
        self.ToAddress3 = ToAddress3
        self.ToAddress3_nsprefix_ = None
        self.ToPostalCode = ToPostalCode
        self.ToPostalCode_nsprefix_ = None
        self.ToPhone = ToPhone
        self.ToPhone_nsprefix_ = None
        self.RecipientEMail = RecipientEMail
        self.RecipientEMail_nsprefix_ = None
        self.ToDPID = ToDPID
        self.ToDPID_nsprefix_ = None
        self.ToProvince = ToProvince
        self.ToProvince_nsprefix_ = None
        self.ToTaxID = ToTaxID
        self.ToTaxID_nsprefix_ = None
        self.Container = Container
        self.Container_nsprefix_ = None
        self.ContentType = ContentType
        self.ContentType_nsprefix_ = None
        self.ShippingContents = ShippingContents
        self.ShippingContents_nsprefix_ = None
        self.PurposeOfShipment = PurposeOfShipment
        self.PurposeOfShipment_nsprefix_ = None
        self.PartiesToTransaction = PartiesToTransaction
        self.PartiesToTransaction_nsprefix_ = None
        self.Agreement = Agreement
        self.Agreement_nsprefix_ = None
        self.Postage = Postage
        self.Postage_nsprefix_ = None
        self.InsuredValue = InsuredValue
        self.InsuredValue_nsprefix_ = None
        self.GrossPounds = GrossPounds
        self.GrossPounds_nsprefix_ = None
        self.GrossOunces = GrossOunces
        self.GrossOunces_nsprefix_ = None
        self.Length = Length
        self.Length_nsprefix_ = None
        self.Width = Width
        self.Width_nsprefix_ = None
        self.Height = Height
        self.Height_nsprefix_ = None
        self.Girth = Girth
        self.Girth_nsprefix_ = None
        self.Shape = Shape
        self.Shape_nsprefix_ = None
        self.CIRequired = CIRequired
        self.CIRequired_nsprefix_ = None
        self.InvoiceDate = InvoiceDate
        self.InvoiceDate_nsprefix_ = None
        self.InvoiceNumber = InvoiceNumber
        self.InvoiceNumber_nsprefix_ = None
        self.CustomerOrderNumber = CustomerOrderNumber
        self.CustomerOrderNumber_nsprefix_ = None
        self.CustOrderNumber = CustOrderNumber
        self.CustOrderNumber_nsprefix_ = None
        self.TermsDelivery = TermsDelivery
        self.TermsDelivery_nsprefix_ = None
        self.TermsDeliveryOther = TermsDeliveryOther
        self.TermsDeliveryOther_nsprefix_ = None
        self.PackingCost = PackingCost
        self.PackingCost_nsprefix_ = None
        self.CountryUltDest = CountryUltDest
        self.CountryUltDest_nsprefix_ = None
        self.CIAgreement = CIAgreement
        self.CIAgreement_nsprefix_ = None
        self.ImageType = ImageType
        self.ImageType_nsprefix_ = None
        self.ImageLayout = ImageLayout
        self.ImageLayout_nsprefix_ = None
        self.CustomerRefNo = CustomerRefNo
        self.CustomerRefNo_nsprefix_ = None
        self.CustomerRefNo2 = CustomerRefNo2
        self.CustomerRefNo2_nsprefix_ = None
        self.ShipDate = ShipDate
        self.ShipDate_nsprefix_ = None
        self.HoldForManifest = HoldForManifest
        self.HoldForManifest_nsprefix_ = None
        self.PriceOptions = PriceOptions
        self.PriceOptions_nsprefix_ = None
        self.CommercialShipment = CommercialShipment
        self.CommercialShipment_nsprefix_ = None
        self.BuyerFirstName = BuyerFirstName
        self.BuyerFirstName_nsprefix_ = None
        self.BuyerLastName = BuyerLastName
        self.BuyerLastName_nsprefix_ = None
        self.BuyerAddress1 = BuyerAddress1
        self.BuyerAddress1_nsprefix_ = None
        self.BuyerAddress2 = BuyerAddress2
        self.BuyerAddress2_nsprefix_ = None
        self.BuyerAddress3 = BuyerAddress3
        self.BuyerAddress3_nsprefix_ = None
        self.BuyerCity = BuyerCity
        self.BuyerCity_nsprefix_ = None
        self.BuyerState = BuyerState
        self.BuyerState_nsprefix_ = None
        self.BuyerPostalCode = BuyerPostalCode
        self.BuyerPostalCode_nsprefix_ = None
        self.BuyerCountry = BuyerCountry
        self.BuyerCountry_nsprefix_ = None
        self.BuyerTaxID = BuyerTaxID
        self.BuyerTaxID_nsprefix_ = None
        self.BuyerRecipient = BuyerRecipient
        self.BuyerRecipient_nsprefix_ = None
        self.TermsPayment = TermsPayment
        self.TermsPayment_nsprefix_ = None
        self.ActionCode = ActionCode
        self.ActionCode_nsprefix_ = None
        self.OptOutOfSPE = OptOutOfSPE
        self.OptOutOfSPE_nsprefix_ = None
        self.PermitNumber = PermitNumber
        self.PermitNumber_nsprefix_ = None
        self.AccountZipCode = AccountZipCode
        self.AccountZipCode_nsprefix_ = None
        self.Machinable = Machinable
        self.Machinable_nsprefix_ = None
        self.DestinationRateIndicator = DestinationRateIndicator
        self.DestinationRateIndicator_nsprefix_ = None
        self.MID = MID
        self.MID_nsprefix_ = None
        self.LogisticsManagerMID = LogisticsManagerMID
        self.LogisticsManagerMID_nsprefix_ = None
        self.CRID = CRID
        self.CRID_nsprefix_ = None
        self.VendorCode = VendorCode
        self.VendorCode_nsprefix_ = None
        self.VendorProductVersionNumber = VendorProductVersionNumber
        self.VendorProductVersionNumber_nsprefix_ = None
        self.OverrideMID = OverrideMID
        self.OverrideMID_nsprefix_ = None
        self.ChargebackCode = ChargebackCode
        self.ChargebackCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, eVSGXGGetLabelRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if eVSGXGGetLabelRequest.subclass:
            return eVSGXGGetLabelRequest.subclass(*args_, **kwargs_)
        else:
            return eVSGXGGetLabelRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Option(self):
        return self.Option
    def set_Option(self, Option):
        self.Option = Option
    def get_Revision(self):
        return self.Revision
    def set_Revision(self, Revision):
        self.Revision = Revision
    def get_ImageParameters(self):
        return self.ImageParameters
    def set_ImageParameters(self, ImageParameters):
        self.ImageParameters = ImageParameters
    def get_FromFirstName(self):
        return self.FromFirstName
    def set_FromFirstName(self, FromFirstName):
        self.FromFirstName = FromFirstName
    def get_FromMiddleInitial(self):
        return self.FromMiddleInitial
    def set_FromMiddleInitial(self, FromMiddleInitial):
        self.FromMiddleInitial = FromMiddleInitial
    def get_FromLastName(self):
        return self.FromLastName
    def set_FromLastName(self, FromLastName):
        self.FromLastName = FromLastName
    def get_FromFirm(self):
        return self.FromFirm
    def set_FromFirm(self, FromFirm):
        self.FromFirm = FromFirm
    def get_FromAddress1(self):
        return self.FromAddress1
    def set_FromAddress1(self, FromAddress1):
        self.FromAddress1 = FromAddress1
    def get_FromAddress2(self):
        return self.FromAddress2
    def set_FromAddress2(self, FromAddress2):
        self.FromAddress2 = FromAddress2
    def get_FromUrbanization(self):
        return self.FromUrbanization
    def set_FromUrbanization(self, FromUrbanization):
        self.FromUrbanization = FromUrbanization
    def get_FromCity(self):
        return self.FromCity
    def set_FromCity(self, FromCity):
        self.FromCity = FromCity
    def get_FromState(self):
        return self.FromState
    def set_FromState(self, FromState):
        self.FromState = FromState
    def get_FromZIP5(self):
        return self.FromZIP5
    def set_FromZIP5(self, FromZIP5):
        self.FromZIP5 = FromZIP5
    def get_FromZIP4(self):
        return self.FromZIP4
    def set_FromZIP4(self, FromZIP4):
        self.FromZIP4 = FromZIP4
    def get_FromPhone(self):
        return self.FromPhone
    def set_FromPhone(self, FromPhone):
        self.FromPhone = FromPhone
    def get_ShipFromZIP(self):
        return self.ShipFromZIP
    def set_ShipFromZIP(self, ShipFromZIP):
        self.ShipFromZIP = ShipFromZIP
    def get_SenderEMail(self):
        return self.SenderEMail
    def set_SenderEMail(self, SenderEMail):
        self.SenderEMail = SenderEMail
    def get_ToFirstName(self):
        return self.ToFirstName
    def set_ToFirstName(self, ToFirstName):
        self.ToFirstName = ToFirstName
    def get_ToLastName(self):
        return self.ToLastName
    def set_ToLastName(self, ToLastName):
        self.ToLastName = ToLastName
    def get_ToFirm(self):
        return self.ToFirm
    def set_ToFirm(self, ToFirm):
        self.ToFirm = ToFirm
    def get_ToAddress1(self):
        return self.ToAddress1
    def set_ToAddress1(self, ToAddress1):
        self.ToAddress1 = ToAddress1
    def get_ToAddress2(self):
        return self.ToAddress2
    def set_ToAddress2(self, ToAddress2):
        self.ToAddress2 = ToAddress2
    def get_ToAddress3(self):
        return self.ToAddress3
    def set_ToAddress3(self, ToAddress3):
        self.ToAddress3 = ToAddress3
    def get_ToPostalCode(self):
        return self.ToPostalCode
    def set_ToPostalCode(self, ToPostalCode):
        self.ToPostalCode = ToPostalCode
    def get_ToPhone(self):
        return self.ToPhone
    def set_ToPhone(self, ToPhone):
        self.ToPhone = ToPhone
    def get_RecipientEMail(self):
        return self.RecipientEMail
    def set_RecipientEMail(self, RecipientEMail):
        self.RecipientEMail = RecipientEMail
    def get_ToDPID(self):
        return self.ToDPID
    def set_ToDPID(self, ToDPID):
        self.ToDPID = ToDPID
    def get_ToProvince(self):
        return self.ToProvince
    def set_ToProvince(self, ToProvince):
        self.ToProvince = ToProvince
    def get_ToTaxID(self):
        return self.ToTaxID
    def set_ToTaxID(self, ToTaxID):
        self.ToTaxID = ToTaxID
    def get_Container(self):
        return self.Container
    def set_Container(self, Container):
        self.Container = Container
    def get_ContentType(self):
        return self.ContentType
    def set_ContentType(self, ContentType):
        self.ContentType = ContentType
    def get_ShippingContents(self):
        return self.ShippingContents
    def set_ShippingContents(self, ShippingContents):
        self.ShippingContents = ShippingContents
    def get_PurposeOfShipment(self):
        return self.PurposeOfShipment
    def set_PurposeOfShipment(self, PurposeOfShipment):
        self.PurposeOfShipment = PurposeOfShipment
    def get_PartiesToTransaction(self):
        return self.PartiesToTransaction
    def set_PartiesToTransaction(self, PartiesToTransaction):
        self.PartiesToTransaction = PartiesToTransaction
    def get_Agreement(self):
        return self.Agreement
    def set_Agreement(self, Agreement):
        self.Agreement = Agreement
    def get_Postage(self):
        return self.Postage
    def set_Postage(self, Postage):
        self.Postage = Postage
    def get_InsuredValue(self):
        return self.InsuredValue
    def set_InsuredValue(self, InsuredValue):
        self.InsuredValue = InsuredValue
    def get_GrossPounds(self):
        return self.GrossPounds
    def set_GrossPounds(self, GrossPounds):
        self.GrossPounds = GrossPounds
    def get_GrossOunces(self):
        return self.GrossOunces
    def set_GrossOunces(self, GrossOunces):
        self.GrossOunces = GrossOunces
    def get_Length(self):
        return self.Length
    def set_Length(self, Length):
        self.Length = Length
    def get_Width(self):
        return self.Width
    def set_Width(self, Width):
        self.Width = Width
    def get_Height(self):
        return self.Height
    def set_Height(self, Height):
        self.Height = Height
    def get_Girth(self):
        return self.Girth
    def set_Girth(self, Girth):
        self.Girth = Girth
    def get_Shape(self):
        return self.Shape
    def set_Shape(self, Shape):
        self.Shape = Shape
    def get_CIRequired(self):
        return self.CIRequired
    def set_CIRequired(self, CIRequired):
        self.CIRequired = CIRequired
    def get_InvoiceDate(self):
        return self.InvoiceDate
    def set_InvoiceDate(self, InvoiceDate):
        self.InvoiceDate = InvoiceDate
    def get_InvoiceNumber(self):
        return self.InvoiceNumber
    def set_InvoiceNumber(self, InvoiceNumber):
        self.InvoiceNumber = InvoiceNumber
    def get_CustomerOrderNumber(self):
        return self.CustomerOrderNumber
    def set_CustomerOrderNumber(self, CustomerOrderNumber):
        self.CustomerOrderNumber = CustomerOrderNumber
    def get_CustOrderNumber(self):
        return self.CustOrderNumber
    def set_CustOrderNumber(self, CustOrderNumber):
        self.CustOrderNumber = CustOrderNumber
    def get_TermsDelivery(self):
        return self.TermsDelivery
    def set_TermsDelivery(self, TermsDelivery):
        self.TermsDelivery = TermsDelivery
    def get_TermsDeliveryOther(self):
        return self.TermsDeliveryOther
    def set_TermsDeliveryOther(self, TermsDeliveryOther):
        self.TermsDeliveryOther = TermsDeliveryOther
    def get_PackingCost(self):
        return self.PackingCost
    def set_PackingCost(self, PackingCost):
        self.PackingCost = PackingCost
    def get_CountryUltDest(self):
        return self.CountryUltDest
    def set_CountryUltDest(self, CountryUltDest):
        self.CountryUltDest = CountryUltDest
    def get_CIAgreement(self):
        return self.CIAgreement
    def set_CIAgreement(self, CIAgreement):
        self.CIAgreement = CIAgreement
    def get_ImageType(self):
        return self.ImageType
    def set_ImageType(self, ImageType):
        self.ImageType = ImageType
    def get_ImageLayout(self):
        return self.ImageLayout
    def set_ImageLayout(self, ImageLayout):
        self.ImageLayout = ImageLayout
    def get_CustomerRefNo(self):
        return self.CustomerRefNo
    def set_CustomerRefNo(self, CustomerRefNo):
        self.CustomerRefNo = CustomerRefNo
    def get_CustomerRefNo2(self):
        return self.CustomerRefNo2
    def set_CustomerRefNo2(self, CustomerRefNo2):
        self.CustomerRefNo2 = CustomerRefNo2
    def get_ShipDate(self):
        return self.ShipDate
    def set_ShipDate(self, ShipDate):
        self.ShipDate = ShipDate
    def get_HoldForManifest(self):
        return self.HoldForManifest
    def set_HoldForManifest(self, HoldForManifest):
        self.HoldForManifest = HoldForManifest
    def get_PriceOptions(self):
        return self.PriceOptions
    def set_PriceOptions(self, PriceOptions):
        self.PriceOptions = PriceOptions
    def get_CommercialShipment(self):
        return self.CommercialShipment
    def set_CommercialShipment(self, CommercialShipment):
        self.CommercialShipment = CommercialShipment
    def get_BuyerFirstName(self):
        return self.BuyerFirstName
    def set_BuyerFirstName(self, BuyerFirstName):
        self.BuyerFirstName = BuyerFirstName
    def get_BuyerLastName(self):
        return self.BuyerLastName
    def set_BuyerLastName(self, BuyerLastName):
        self.BuyerLastName = BuyerLastName
    def get_BuyerAddress1(self):
        return self.BuyerAddress1
    def set_BuyerAddress1(self, BuyerAddress1):
        self.BuyerAddress1 = BuyerAddress1
    def get_BuyerAddress2(self):
        return self.BuyerAddress2
    def set_BuyerAddress2(self, BuyerAddress2):
        self.BuyerAddress2 = BuyerAddress2
    def get_BuyerAddress3(self):
        return self.BuyerAddress3
    def set_BuyerAddress3(self, BuyerAddress3):
        self.BuyerAddress3 = BuyerAddress3
    def get_BuyerCity(self):
        return self.BuyerCity
    def set_BuyerCity(self, BuyerCity):
        self.BuyerCity = BuyerCity
    def get_BuyerState(self):
        return self.BuyerState
    def set_BuyerState(self, BuyerState):
        self.BuyerState = BuyerState
    def get_BuyerPostalCode(self):
        return self.BuyerPostalCode
    def set_BuyerPostalCode(self, BuyerPostalCode):
        self.BuyerPostalCode = BuyerPostalCode
    def get_BuyerCountry(self):
        return self.BuyerCountry
    def set_BuyerCountry(self, BuyerCountry):
        self.BuyerCountry = BuyerCountry
    def get_BuyerTaxID(self):
        return self.BuyerTaxID
    def set_BuyerTaxID(self, BuyerTaxID):
        self.BuyerTaxID = BuyerTaxID
    def get_BuyerRecipient(self):
        return self.BuyerRecipient
    def set_BuyerRecipient(self, BuyerRecipient):
        self.BuyerRecipient = BuyerRecipient
    def get_TermsPayment(self):
        return self.TermsPayment
    def set_TermsPayment(self, TermsPayment):
        self.TermsPayment = TermsPayment
    def get_ActionCode(self):
        return self.ActionCode
    def set_ActionCode(self, ActionCode):
        self.ActionCode = ActionCode
    def get_OptOutOfSPE(self):
        return self.OptOutOfSPE
    def set_OptOutOfSPE(self, OptOutOfSPE):
        self.OptOutOfSPE = OptOutOfSPE
    def get_PermitNumber(self):
        return self.PermitNumber
    def set_PermitNumber(self, PermitNumber):
        self.PermitNumber = PermitNumber
    def get_AccountZipCode(self):
        return self.AccountZipCode
    def set_AccountZipCode(self, AccountZipCode):
        self.AccountZipCode = AccountZipCode
    def get_Machinable(self):
        return self.Machinable
    def set_Machinable(self, Machinable):
        self.Machinable = Machinable
    def get_DestinationRateIndicator(self):
        return self.DestinationRateIndicator
    def set_DestinationRateIndicator(self, DestinationRateIndicator):
        self.DestinationRateIndicator = DestinationRateIndicator
    def get_MID(self):
        return self.MID
    def set_MID(self, MID):
        self.MID = MID
    def get_LogisticsManagerMID(self):
        return self.LogisticsManagerMID
    def set_LogisticsManagerMID(self, LogisticsManagerMID):
        self.LogisticsManagerMID = LogisticsManagerMID
    def get_CRID(self):
        return self.CRID
    def set_CRID(self, CRID):
        self.CRID = CRID
    def get_VendorCode(self):
        return self.VendorCode
    def set_VendorCode(self, VendorCode):
        self.VendorCode = VendorCode
    def get_VendorProductVersionNumber(self):
        return self.VendorProductVersionNumber
    def set_VendorProductVersionNumber(self, VendorProductVersionNumber):
        self.VendorProductVersionNumber = VendorProductVersionNumber
    def get_OverrideMID(self):
        return self.OverrideMID
    def set_OverrideMID(self, OverrideMID):
        self.OverrideMID = OverrideMID
    def get_ChargebackCode(self):
        return self.ChargebackCode
    def set_ChargebackCode(self, ChargebackCode):
        self.ChargebackCode = ChargebackCode
    def get_USERID(self):
        return self.USERID
    def set_USERID(self, USERID):
        self.USERID = USERID
    def get_PASSWORD(self):
        return self.PASSWORD
    def set_PASSWORD(self, PASSWORD):
        self.PASSWORD = PASSWORD
    def hasContent_(self):
        if (
            self.Option is not None or
            self.Revision is not None or
            self.ImageParameters is not None or
            self.FromFirstName is not None or
            self.FromMiddleInitial is not None or
            self.FromLastName is not None or
            self.FromFirm is not None or
            self.FromAddress1 is not None or
            self.FromAddress2 is not None or
            self.FromUrbanization is not None or
            self.FromCity is not None or
            self.FromState is not None or
            self.FromZIP5 is not None or
            self.FromZIP4 is not None or
            self.FromPhone is not None or
            self.ShipFromZIP is not None or
            self.SenderEMail is not None or
            self.ToFirstName is not None or
            self.ToLastName is not None or
            self.ToFirm is not None or
            self.ToAddress1 is not None or
            self.ToAddress2 is not None or
            self.ToAddress3 is not None or
            self.ToPostalCode is not None or
            self.ToPhone is not None or
            self.RecipientEMail is not None or
            self.ToDPID is not None or
            self.ToProvince is not None or
            self.ToTaxID is not None or
            self.Container is not None or
            self.ContentType is not None or
            self.ShippingContents is not None or
            self.PurposeOfShipment is not None or
            self.PartiesToTransaction is not None or
            self.Agreement is not None or
            self.Postage is not None or
            self.InsuredValue is not None or
            self.GrossPounds is not None or
            self.GrossOunces is not None or
            self.Length is not None or
            self.Width is not None or
            self.Height is not None or
            self.Girth is not None or
            self.Shape is not None or
            self.CIRequired is not None or
            self.InvoiceDate is not None or
            self.InvoiceNumber is not None or
            self.CustomerOrderNumber is not None or
            self.CustOrderNumber is not None or
            self.TermsDelivery is not None or
            self.TermsDeliveryOther is not None or
            self.PackingCost is not None or
            self.CountryUltDest is not None or
            self.CIAgreement is not None or
            self.ImageType is not None or
            self.ImageLayout is not None or
            self.CustomerRefNo is not None or
            self.CustomerRefNo2 is not None or
            self.ShipDate is not None or
            self.HoldForManifest is not None or
            self.PriceOptions is not None or
            self.CommercialShipment is not None or
            self.BuyerFirstName is not None or
            self.BuyerLastName is not None or
            self.BuyerAddress1 is not None or
            self.BuyerAddress2 is not None or
            self.BuyerAddress3 is not None or
            self.BuyerCity is not None or
            self.BuyerState is not None or
            self.BuyerPostalCode is not None or
            self.BuyerCountry is not None or
            self.BuyerTaxID is not None or
            self.BuyerRecipient is not None or
            self.TermsPayment is not None or
            self.ActionCode is not None or
            self.OptOutOfSPE is not None or
            self.PermitNumber is not None or
            self.AccountZipCode is not None or
            self.Machinable is not None or
            self.DestinationRateIndicator is not None or
            self.MID is not None or
            self.LogisticsManagerMID is not None or
            self.CRID is not None or
            self.VendorCode is not None or
            self.VendorProductVersionNumber is not None or
            self.OverrideMID is not None or
            self.ChargebackCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='eVSGXGGetLabelRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('eVSGXGGetLabelRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'eVSGXGGetLabelRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='eVSGXGGetLabelRequest')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='eVSGXGGetLabelRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='eVSGXGGetLabelRequest'):
        if self.USERID is not None and 'USERID' not in already_processed:
            already_processed.add('USERID')
            outfile.write(' USERID=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.USERID), input_name='USERID')), ))
        if self.PASSWORD is not None and 'PASSWORD' not in already_processed:
            already_processed.add('PASSWORD')
            outfile.write(' PASSWORD=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.PASSWORD), input_name='PASSWORD')), ))
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='eVSGXGGetLabelRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Option is not None:
            namespaceprefix_ = self.Option_nsprefix_ + ':' if (UseCapturedNS_ and self.Option_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOption>%s</%sOption>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Option), input_name='Option')), namespaceprefix_ , eol_))
        if self.Revision is not None:
            namespaceprefix_ = self.Revision_nsprefix_ + ':' if (UseCapturedNS_ and self.Revision_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRevision>%s</%sRevision>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Revision), input_name='Revision')), namespaceprefix_ , eol_))
        if self.ImageParameters is not None:
            namespaceprefix_ = self.ImageParameters_nsprefix_ + ':' if (UseCapturedNS_ and self.ImageParameters_nsprefix_) else ''
            self.ImageParameters.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ImageParameters', pretty_print=pretty_print)
        if self.FromFirstName is not None:
            namespaceprefix_ = self.FromFirstName_nsprefix_ + ':' if (UseCapturedNS_ and self.FromFirstName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFromFirstName>%s</%sFromFirstName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FromFirstName), input_name='FromFirstName')), namespaceprefix_ , eol_))
        if self.FromMiddleInitial is not None:
            namespaceprefix_ = self.FromMiddleInitial_nsprefix_ + ':' if (UseCapturedNS_ and self.FromMiddleInitial_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFromMiddleInitial>%s</%sFromMiddleInitial>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FromMiddleInitial), input_name='FromMiddleInitial')), namespaceprefix_ , eol_))
        if self.FromLastName is not None:
            namespaceprefix_ = self.FromLastName_nsprefix_ + ':' if (UseCapturedNS_ and self.FromLastName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFromLastName>%s</%sFromLastName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FromLastName), input_name='FromLastName')), namespaceprefix_ , eol_))
        if self.FromFirm is not None:
            namespaceprefix_ = self.FromFirm_nsprefix_ + ':' if (UseCapturedNS_ and self.FromFirm_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFromFirm>%s</%sFromFirm>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FromFirm), input_name='FromFirm')), namespaceprefix_ , eol_))
        if self.FromAddress1 is not None:
            namespaceprefix_ = self.FromAddress1_nsprefix_ + ':' if (UseCapturedNS_ and self.FromAddress1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFromAddress1>%s</%sFromAddress1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FromAddress1), input_name='FromAddress1')), namespaceprefix_ , eol_))
        if self.FromAddress2 is not None:
            namespaceprefix_ = self.FromAddress2_nsprefix_ + ':' if (UseCapturedNS_ and self.FromAddress2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFromAddress2>%s</%sFromAddress2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FromAddress2), input_name='FromAddress2')), namespaceprefix_ , eol_))
        if self.FromUrbanization is not None:
            namespaceprefix_ = self.FromUrbanization_nsprefix_ + ':' if (UseCapturedNS_ and self.FromUrbanization_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFromUrbanization>%s</%sFromUrbanization>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FromUrbanization), input_name='FromUrbanization')), namespaceprefix_ , eol_))
        if self.FromCity is not None:
            namespaceprefix_ = self.FromCity_nsprefix_ + ':' if (UseCapturedNS_ and self.FromCity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFromCity>%s</%sFromCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FromCity), input_name='FromCity')), namespaceprefix_ , eol_))
        if self.FromState is not None:
            namespaceprefix_ = self.FromState_nsprefix_ + ':' if (UseCapturedNS_ and self.FromState_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFromState>%s</%sFromState>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FromState), input_name='FromState')), namespaceprefix_ , eol_))
        if self.FromZIP5 is not None:
            namespaceprefix_ = self.FromZIP5_nsprefix_ + ':' if (UseCapturedNS_ and self.FromZIP5_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFromZIP5>%s</%sFromZIP5>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FromZIP5), input_name='FromZIP5')), namespaceprefix_ , eol_))
        if self.FromZIP4 is not None:
            namespaceprefix_ = self.FromZIP4_nsprefix_ + ':' if (UseCapturedNS_ and self.FromZIP4_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFromZIP4>%s</%sFromZIP4>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FromZIP4), input_name='FromZIP4')), namespaceprefix_ , eol_))
        if self.FromPhone is not None:
            namespaceprefix_ = self.FromPhone_nsprefix_ + ':' if (UseCapturedNS_ and self.FromPhone_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFromPhone>%s</%sFromPhone>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FromPhone), input_name='FromPhone')), namespaceprefix_ , eol_))
        if self.ShipFromZIP is not None:
            namespaceprefix_ = self.ShipFromZIP_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipFromZIP_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipFromZIP>%s</%sShipFromZIP>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShipFromZIP), input_name='ShipFromZIP')), namespaceprefix_ , eol_))
        if self.SenderEMail is not None:
            namespaceprefix_ = self.SenderEMail_nsprefix_ + ':' if (UseCapturedNS_ and self.SenderEMail_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSenderEMail>%s</%sSenderEMail>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SenderEMail), input_name='SenderEMail')), namespaceprefix_ , eol_))
        if self.ToFirstName is not None:
            namespaceprefix_ = self.ToFirstName_nsprefix_ + ':' if (UseCapturedNS_ and self.ToFirstName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sToFirstName>%s</%sToFirstName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ToFirstName), input_name='ToFirstName')), namespaceprefix_ , eol_))
        if self.ToLastName is not None:
            namespaceprefix_ = self.ToLastName_nsprefix_ + ':' if (UseCapturedNS_ and self.ToLastName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sToLastName>%s</%sToLastName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ToLastName), input_name='ToLastName')), namespaceprefix_ , eol_))
        if self.ToFirm is not None:
            namespaceprefix_ = self.ToFirm_nsprefix_ + ':' if (UseCapturedNS_ and self.ToFirm_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sToFirm>%s</%sToFirm>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ToFirm), input_name='ToFirm')), namespaceprefix_ , eol_))
        if self.ToAddress1 is not None:
            namespaceprefix_ = self.ToAddress1_nsprefix_ + ':' if (UseCapturedNS_ and self.ToAddress1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sToAddress1>%s</%sToAddress1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ToAddress1), input_name='ToAddress1')), namespaceprefix_ , eol_))
        if self.ToAddress2 is not None:
            namespaceprefix_ = self.ToAddress2_nsprefix_ + ':' if (UseCapturedNS_ and self.ToAddress2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sToAddress2>%s</%sToAddress2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ToAddress2), input_name='ToAddress2')), namespaceprefix_ , eol_))
        if self.ToAddress3 is not None:
            namespaceprefix_ = self.ToAddress3_nsprefix_ + ':' if (UseCapturedNS_ and self.ToAddress3_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sToAddress3>%s</%sToAddress3>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ToAddress3), input_name='ToAddress3')), namespaceprefix_ , eol_))
        if self.ToPostalCode is not None:
            namespaceprefix_ = self.ToPostalCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ToPostalCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sToPostalCode>%s</%sToPostalCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ToPostalCode), input_name='ToPostalCode')), namespaceprefix_ , eol_))
        if self.ToPhone is not None:
            namespaceprefix_ = self.ToPhone_nsprefix_ + ':' if (UseCapturedNS_ and self.ToPhone_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sToPhone>%s</%sToPhone>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ToPhone), input_name='ToPhone')), namespaceprefix_ , eol_))
        if self.RecipientEMail is not None:
            namespaceprefix_ = self.RecipientEMail_nsprefix_ + ':' if (UseCapturedNS_ and self.RecipientEMail_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRecipientEMail>%s</%sRecipientEMail>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.RecipientEMail), input_name='RecipientEMail')), namespaceprefix_ , eol_))
        if self.ToDPID is not None:
            namespaceprefix_ = self.ToDPID_nsprefix_ + ':' if (UseCapturedNS_ and self.ToDPID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sToDPID>%s</%sToDPID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ToDPID), input_name='ToDPID')), namespaceprefix_ , eol_))
        if self.ToProvince is not None:
            namespaceprefix_ = self.ToProvince_nsprefix_ + ':' if (UseCapturedNS_ and self.ToProvince_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sToProvince>%s</%sToProvince>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ToProvince), input_name='ToProvince')), namespaceprefix_ , eol_))
        if self.ToTaxID is not None:
            namespaceprefix_ = self.ToTaxID_nsprefix_ + ':' if (UseCapturedNS_ and self.ToTaxID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sToTaxID>%s</%sToTaxID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ToTaxID), input_name='ToTaxID')), namespaceprefix_ , eol_))
        if self.Container is not None:
            namespaceprefix_ = self.Container_nsprefix_ + ':' if (UseCapturedNS_ and self.Container_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sContainer>%s</%sContainer>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Container), input_name='Container')), namespaceprefix_ , eol_))
        if self.ContentType is not None:
            namespaceprefix_ = self.ContentType_nsprefix_ + ':' if (UseCapturedNS_ and self.ContentType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sContentType>%s</%sContentType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ContentType), input_name='ContentType')), namespaceprefix_ , eol_))
        if self.ShippingContents is not None:
            namespaceprefix_ = self.ShippingContents_nsprefix_ + ':' if (UseCapturedNS_ and self.ShippingContents_nsprefix_) else ''
            self.ShippingContents.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShippingContents', pretty_print=pretty_print)
        if self.PurposeOfShipment is not None:
            namespaceprefix_ = self.PurposeOfShipment_nsprefix_ + ':' if (UseCapturedNS_ and self.PurposeOfShipment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPurposeOfShipment>%s</%sPurposeOfShipment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PurposeOfShipment), input_name='PurposeOfShipment')), namespaceprefix_ , eol_))
        if self.PartiesToTransaction is not None:
            namespaceprefix_ = self.PartiesToTransaction_nsprefix_ + ':' if (UseCapturedNS_ and self.PartiesToTransaction_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPartiesToTransaction>%s</%sPartiesToTransaction>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PartiesToTransaction), input_name='PartiesToTransaction')), namespaceprefix_ , eol_))
        if self.Agreement is not None:
            namespaceprefix_ = self.Agreement_nsprefix_ + ':' if (UseCapturedNS_ and self.Agreement_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAgreement>%s</%sAgreement>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Agreement), input_name='Agreement')), namespaceprefix_ , eol_))
        if self.Postage is not None:
            namespaceprefix_ = self.Postage_nsprefix_ + ':' if (UseCapturedNS_ and self.Postage_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPostage>%s</%sPostage>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Postage), input_name='Postage')), namespaceprefix_ , eol_))
        if self.InsuredValue is not None:
            namespaceprefix_ = self.InsuredValue_nsprefix_ + ':' if (UseCapturedNS_ and self.InsuredValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sInsuredValue>%s</%sInsuredValue>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.InsuredValue), input_name='InsuredValue')), namespaceprefix_ , eol_))
        if self.GrossPounds is not None:
            namespaceprefix_ = self.GrossPounds_nsprefix_ + ':' if (UseCapturedNS_ and self.GrossPounds_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGrossPounds>%s</%sGrossPounds>%s' % (namespaceprefix_ , self.gds_format_integer(self.GrossPounds, input_name='GrossPounds'), namespaceprefix_ , eol_))
        if self.GrossOunces is not None:
            namespaceprefix_ = self.GrossOunces_nsprefix_ + ':' if (UseCapturedNS_ and self.GrossOunces_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGrossOunces>%s</%sGrossOunces>%s' % (namespaceprefix_ , self.gds_format_integer(self.GrossOunces, input_name='GrossOunces'), namespaceprefix_ , eol_))
        if self.Length is not None:
            namespaceprefix_ = self.Length_nsprefix_ + ':' if (UseCapturedNS_ and self.Length_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLength>%s</%sLength>%s' % (namespaceprefix_ , self.gds_format_float(self.Length, input_name='Length'), namespaceprefix_ , eol_))
        if self.Width is not None:
            namespaceprefix_ = self.Width_nsprefix_ + ':' if (UseCapturedNS_ and self.Width_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWidth>%s</%sWidth>%s' % (namespaceprefix_ , self.gds_format_float(self.Width, input_name='Width'), namespaceprefix_ , eol_))
        if self.Height is not None:
            namespaceprefix_ = self.Height_nsprefix_ + ':' if (UseCapturedNS_ and self.Height_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHeight>%s</%sHeight>%s' % (namespaceprefix_ , self.gds_format_float(self.Height, input_name='Height'), namespaceprefix_ , eol_))
        if self.Girth is not None:
            namespaceprefix_ = self.Girth_nsprefix_ + ':' if (UseCapturedNS_ and self.Girth_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGirth>%s</%sGirth>%s' % (namespaceprefix_ , self.gds_format_float(self.Girth, input_name='Girth'), namespaceprefix_ , eol_))
        if self.Shape is not None:
            namespaceprefix_ = self.Shape_nsprefix_ + ':' if (UseCapturedNS_ and self.Shape_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShape>%s</%sShape>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Shape), input_name='Shape')), namespaceprefix_ , eol_))
        if self.CIRequired is not None:
            namespaceprefix_ = self.CIRequired_nsprefix_ + ':' if (UseCapturedNS_ and self.CIRequired_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCIRequired>%s</%sCIRequired>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CIRequired), input_name='CIRequired')), namespaceprefix_ , eol_))
        if self.InvoiceDate is not None:
            namespaceprefix_ = self.InvoiceDate_nsprefix_ + ':' if (UseCapturedNS_ and self.InvoiceDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sInvoiceDate>%s</%sInvoiceDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.InvoiceDate), input_name='InvoiceDate')), namespaceprefix_ , eol_))
        if self.InvoiceNumber is not None:
            namespaceprefix_ = self.InvoiceNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.InvoiceNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sInvoiceNumber>%s</%sInvoiceNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.InvoiceNumber), input_name='InvoiceNumber')), namespaceprefix_ , eol_))
        if self.CustomerOrderNumber is not None:
            namespaceprefix_ = self.CustomerOrderNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomerOrderNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustomerOrderNumber>%s</%sCustomerOrderNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CustomerOrderNumber), input_name='CustomerOrderNumber')), namespaceprefix_ , eol_))
        if self.CustOrderNumber is not None:
            namespaceprefix_ = self.CustOrderNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.CustOrderNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustOrderNumber>%s</%sCustOrderNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CustOrderNumber), input_name='CustOrderNumber')), namespaceprefix_ , eol_))
        if self.TermsDelivery is not None:
            namespaceprefix_ = self.TermsDelivery_nsprefix_ + ':' if (UseCapturedNS_ and self.TermsDelivery_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTermsDelivery>%s</%sTermsDelivery>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TermsDelivery), input_name='TermsDelivery')), namespaceprefix_ , eol_))
        if self.TermsDeliveryOther is not None:
            namespaceprefix_ = self.TermsDeliveryOther_nsprefix_ + ':' if (UseCapturedNS_ and self.TermsDeliveryOther_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTermsDeliveryOther>%s</%sTermsDeliveryOther>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TermsDeliveryOther), input_name='TermsDeliveryOther')), namespaceprefix_ , eol_))
        if self.PackingCost is not None:
            namespaceprefix_ = self.PackingCost_nsprefix_ + ':' if (UseCapturedNS_ and self.PackingCost_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPackingCost>%s</%sPackingCost>%s' % (namespaceprefix_ , self.gds_format_decimal(self.PackingCost, input_name='PackingCost'), namespaceprefix_ , eol_))
        if self.CountryUltDest is not None:
            namespaceprefix_ = self.CountryUltDest_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryUltDest_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryUltDest>%s</%sCountryUltDest>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryUltDest), input_name='CountryUltDest')), namespaceprefix_ , eol_))
        if self.CIAgreement is not None:
            namespaceprefix_ = self.CIAgreement_nsprefix_ + ':' if (UseCapturedNS_ and self.CIAgreement_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCIAgreement>%s</%sCIAgreement>%s' % (namespaceprefix_ , self.gds_format_boolean(self.CIAgreement, input_name='CIAgreement'), namespaceprefix_ , eol_))
        if self.ImageType is not None:
            namespaceprefix_ = self.ImageType_nsprefix_ + ':' if (UseCapturedNS_ and self.ImageType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sImageType>%s</%sImageType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ImageType), input_name='ImageType')), namespaceprefix_ , eol_))
        if self.ImageLayout is not None:
            namespaceprefix_ = self.ImageLayout_nsprefix_ + ':' if (UseCapturedNS_ and self.ImageLayout_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sImageLayout>%s</%sImageLayout>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ImageLayout), input_name='ImageLayout')), namespaceprefix_ , eol_))
        if self.CustomerRefNo is not None:
            namespaceprefix_ = self.CustomerRefNo_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomerRefNo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustomerRefNo>%s</%sCustomerRefNo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CustomerRefNo), input_name='CustomerRefNo')), namespaceprefix_ , eol_))
        if self.CustomerRefNo2 is not None:
            namespaceprefix_ = self.CustomerRefNo2_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomerRefNo2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustomerRefNo2>%s</%sCustomerRefNo2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CustomerRefNo2), input_name='CustomerRefNo2')), namespaceprefix_ , eol_))
        if self.ShipDate is not None:
            namespaceprefix_ = self.ShipDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipDate>%s</%sShipDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShipDate), input_name='ShipDate')), namespaceprefix_ , eol_))
        if self.HoldForManifest is not None:
            namespaceprefix_ = self.HoldForManifest_nsprefix_ + ':' if (UseCapturedNS_ and self.HoldForManifest_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHoldForManifest>%s</%sHoldForManifest>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HoldForManifest), input_name='HoldForManifest')), namespaceprefix_ , eol_))
        if self.PriceOptions is not None:
            namespaceprefix_ = self.PriceOptions_nsprefix_ + ':' if (UseCapturedNS_ and self.PriceOptions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPriceOptions>%s</%sPriceOptions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PriceOptions), input_name='PriceOptions')), namespaceprefix_ , eol_))
        if self.CommercialShipment is not None:
            namespaceprefix_ = self.CommercialShipment_nsprefix_ + ':' if (UseCapturedNS_ and self.CommercialShipment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCommercialShipment>%s</%sCommercialShipment>%s' % (namespaceprefix_ , self.gds_format_boolean(self.CommercialShipment, input_name='CommercialShipment'), namespaceprefix_ , eol_))
        if self.BuyerFirstName is not None:
            namespaceprefix_ = self.BuyerFirstName_nsprefix_ + ':' if (UseCapturedNS_ and self.BuyerFirstName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBuyerFirstName>%s</%sBuyerFirstName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BuyerFirstName), input_name='BuyerFirstName')), namespaceprefix_ , eol_))
        if self.BuyerLastName is not None:
            namespaceprefix_ = self.BuyerLastName_nsprefix_ + ':' if (UseCapturedNS_ and self.BuyerLastName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBuyerLastName>%s</%sBuyerLastName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BuyerLastName), input_name='BuyerLastName')), namespaceprefix_ , eol_))
        if self.BuyerAddress1 is not None:
            namespaceprefix_ = self.BuyerAddress1_nsprefix_ + ':' if (UseCapturedNS_ and self.BuyerAddress1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBuyerAddress1>%s</%sBuyerAddress1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BuyerAddress1), input_name='BuyerAddress1')), namespaceprefix_ , eol_))
        if self.BuyerAddress2 is not None:
            namespaceprefix_ = self.BuyerAddress2_nsprefix_ + ':' if (UseCapturedNS_ and self.BuyerAddress2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBuyerAddress2>%s</%sBuyerAddress2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BuyerAddress2), input_name='BuyerAddress2')), namespaceprefix_ , eol_))
        if self.BuyerAddress3 is not None:
            namespaceprefix_ = self.BuyerAddress3_nsprefix_ + ':' if (UseCapturedNS_ and self.BuyerAddress3_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBuyerAddress3>%s</%sBuyerAddress3>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BuyerAddress3), input_name='BuyerAddress3')), namespaceprefix_ , eol_))
        if self.BuyerCity is not None:
            namespaceprefix_ = self.BuyerCity_nsprefix_ + ':' if (UseCapturedNS_ and self.BuyerCity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBuyerCity>%s</%sBuyerCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BuyerCity), input_name='BuyerCity')), namespaceprefix_ , eol_))
        if self.BuyerState is not None:
            namespaceprefix_ = self.BuyerState_nsprefix_ + ':' if (UseCapturedNS_ and self.BuyerState_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBuyerState>%s</%sBuyerState>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BuyerState), input_name='BuyerState')), namespaceprefix_ , eol_))
        if self.BuyerPostalCode is not None:
            namespaceprefix_ = self.BuyerPostalCode_nsprefix_ + ':' if (UseCapturedNS_ and self.BuyerPostalCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBuyerPostalCode>%s</%sBuyerPostalCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BuyerPostalCode), input_name='BuyerPostalCode')), namespaceprefix_ , eol_))
        if self.BuyerCountry is not None:
            namespaceprefix_ = self.BuyerCountry_nsprefix_ + ':' if (UseCapturedNS_ and self.BuyerCountry_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBuyerCountry>%s</%sBuyerCountry>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BuyerCountry), input_name='BuyerCountry')), namespaceprefix_ , eol_))
        if self.BuyerTaxID is not None:
            namespaceprefix_ = self.BuyerTaxID_nsprefix_ + ':' if (UseCapturedNS_ and self.BuyerTaxID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBuyerTaxID>%s</%sBuyerTaxID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BuyerTaxID), input_name='BuyerTaxID')), namespaceprefix_ , eol_))
        if self.BuyerRecipient is not None:
            namespaceprefix_ = self.BuyerRecipient_nsprefix_ + ':' if (UseCapturedNS_ and self.BuyerRecipient_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBuyerRecipient>%s</%sBuyerRecipient>%s' % (namespaceprefix_ , self.gds_format_boolean(self.BuyerRecipient, input_name='BuyerRecipient'), namespaceprefix_ , eol_))
        if self.TermsPayment is not None:
            namespaceprefix_ = self.TermsPayment_nsprefix_ + ':' if (UseCapturedNS_ and self.TermsPayment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTermsPayment>%s</%sTermsPayment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TermsPayment), input_name='TermsPayment')), namespaceprefix_ , eol_))
        if self.ActionCode is not None:
            namespaceprefix_ = self.ActionCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ActionCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sActionCode>%s</%sActionCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ActionCode), input_name='ActionCode')), namespaceprefix_ , eol_))
        if self.OptOutOfSPE is not None:
            namespaceprefix_ = self.OptOutOfSPE_nsprefix_ + ':' if (UseCapturedNS_ and self.OptOutOfSPE_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOptOutOfSPE>%s</%sOptOutOfSPE>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OptOutOfSPE), input_name='OptOutOfSPE')), namespaceprefix_ , eol_))
        if self.PermitNumber is not None:
            namespaceprefix_ = self.PermitNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.PermitNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPermitNumber>%s</%sPermitNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PermitNumber), input_name='PermitNumber')), namespaceprefix_ , eol_))
        if self.AccountZipCode is not None:
            namespaceprefix_ = self.AccountZipCode_nsprefix_ + ':' if (UseCapturedNS_ and self.AccountZipCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccountZipCode>%s</%sAccountZipCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AccountZipCode), input_name='AccountZipCode')), namespaceprefix_ , eol_))
        if self.Machinable is not None:
            namespaceprefix_ = self.Machinable_nsprefix_ + ':' if (UseCapturedNS_ and self.Machinable_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMachinable>%s</%sMachinable>%s' % (namespaceprefix_ , self.gds_format_boolean(self.Machinable, input_name='Machinable'), namespaceprefix_ , eol_))
        if self.DestinationRateIndicator is not None:
            namespaceprefix_ = self.DestinationRateIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationRateIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDestinationRateIndicator>%s</%sDestinationRateIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DestinationRateIndicator), input_name='DestinationRateIndicator')), namespaceprefix_ , eol_))
        if self.MID is not None:
            namespaceprefix_ = self.MID_nsprefix_ + ':' if (UseCapturedNS_ and self.MID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMID>%s</%sMID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MID), input_name='MID')), namespaceprefix_ , eol_))
        if self.LogisticsManagerMID is not None:
            namespaceprefix_ = self.LogisticsManagerMID_nsprefix_ + ':' if (UseCapturedNS_ and self.LogisticsManagerMID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLogisticsManagerMID>%s</%sLogisticsManagerMID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LogisticsManagerMID), input_name='LogisticsManagerMID')), namespaceprefix_ , eol_))
        if self.CRID is not None:
            namespaceprefix_ = self.CRID_nsprefix_ + ':' if (UseCapturedNS_ and self.CRID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCRID>%s</%sCRID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CRID), input_name='CRID')), namespaceprefix_ , eol_))
        if self.VendorCode is not None:
            namespaceprefix_ = self.VendorCode_nsprefix_ + ':' if (UseCapturedNS_ and self.VendorCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sVendorCode>%s</%sVendorCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.VendorCode), input_name='VendorCode')), namespaceprefix_ , eol_))
        if self.VendorProductVersionNumber is not None:
            namespaceprefix_ = self.VendorProductVersionNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.VendorProductVersionNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sVendorProductVersionNumber>%s</%sVendorProductVersionNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.VendorProductVersionNumber), input_name='VendorProductVersionNumber')), namespaceprefix_ , eol_))
        if self.OverrideMID is not None:
            namespaceprefix_ = self.OverrideMID_nsprefix_ + ':' if (UseCapturedNS_ and self.OverrideMID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOverrideMID>%s</%sOverrideMID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OverrideMID), input_name='OverrideMID')), namespaceprefix_ , eol_))
        if self.ChargebackCode is not None:
            namespaceprefix_ = self.ChargebackCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ChargebackCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChargebackCode>%s</%sChargebackCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChargebackCode), input_name='ChargebackCode')), namespaceprefix_ , eol_))
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
        value = find_attr_value_('USERID', node)
        if value is not None and 'USERID' not in already_processed:
            already_processed.add('USERID')
            self.USERID = value
        value = find_attr_value_('PASSWORD', node)
        if value is not None and 'PASSWORD' not in already_processed:
            already_processed.add('PASSWORD')
            self.PASSWORD = value
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Option':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Option')
            value_ = self.gds_validate_string(value_, node, 'Option')
            self.Option = value_
            self.Option_nsprefix_ = child_.prefix
        elif nodeName_ == 'Revision':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Revision')
            value_ = self.gds_validate_string(value_, node, 'Revision')
            self.Revision = value_
            self.Revision_nsprefix_ = child_.prefix
        elif nodeName_ == 'ImageParameters':
            obj_ = ImageParametersType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ImageParameters = obj_
            obj_.original_tagname_ = 'ImageParameters'
        elif nodeName_ == 'FromFirstName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FromFirstName')
            value_ = self.gds_validate_string(value_, node, 'FromFirstName')
            self.FromFirstName = value_
            self.FromFirstName_nsprefix_ = child_.prefix
        elif nodeName_ == 'FromMiddleInitial':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FromMiddleInitial')
            value_ = self.gds_validate_string(value_, node, 'FromMiddleInitial')
            self.FromMiddleInitial = value_
            self.FromMiddleInitial_nsprefix_ = child_.prefix
        elif nodeName_ == 'FromLastName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FromLastName')
            value_ = self.gds_validate_string(value_, node, 'FromLastName')
            self.FromLastName = value_
            self.FromLastName_nsprefix_ = child_.prefix
        elif nodeName_ == 'FromFirm':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FromFirm')
            value_ = self.gds_validate_string(value_, node, 'FromFirm')
            self.FromFirm = value_
            self.FromFirm_nsprefix_ = child_.prefix
        elif nodeName_ == 'FromAddress1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FromAddress1')
            value_ = self.gds_validate_string(value_, node, 'FromAddress1')
            self.FromAddress1 = value_
            self.FromAddress1_nsprefix_ = child_.prefix
        elif nodeName_ == 'FromAddress2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FromAddress2')
            value_ = self.gds_validate_string(value_, node, 'FromAddress2')
            self.FromAddress2 = value_
            self.FromAddress2_nsprefix_ = child_.prefix
        elif nodeName_ == 'FromUrbanization':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FromUrbanization')
            value_ = self.gds_validate_string(value_, node, 'FromUrbanization')
            self.FromUrbanization = value_
            self.FromUrbanization_nsprefix_ = child_.prefix
        elif nodeName_ == 'FromCity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FromCity')
            value_ = self.gds_validate_string(value_, node, 'FromCity')
            self.FromCity = value_
            self.FromCity_nsprefix_ = child_.prefix
        elif nodeName_ == 'FromState':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FromState')
            value_ = self.gds_validate_string(value_, node, 'FromState')
            self.FromState = value_
            self.FromState_nsprefix_ = child_.prefix
        elif nodeName_ == 'FromZIP5':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FromZIP5')
            value_ = self.gds_validate_string(value_, node, 'FromZIP5')
            self.FromZIP5 = value_
            self.FromZIP5_nsprefix_ = child_.prefix
        elif nodeName_ == 'FromZIP4':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FromZIP4')
            value_ = self.gds_validate_string(value_, node, 'FromZIP4')
            self.FromZIP4 = value_
            self.FromZIP4_nsprefix_ = child_.prefix
        elif nodeName_ == 'FromPhone':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FromPhone')
            value_ = self.gds_validate_string(value_, node, 'FromPhone')
            self.FromPhone = value_
            self.FromPhone_nsprefix_ = child_.prefix
        elif nodeName_ == 'ShipFromZIP':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShipFromZIP')
            value_ = self.gds_validate_string(value_, node, 'ShipFromZIP')
            self.ShipFromZIP = value_
            self.ShipFromZIP_nsprefix_ = child_.prefix
        elif nodeName_ == 'SenderEMail':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SenderEMail')
            value_ = self.gds_validate_string(value_, node, 'SenderEMail')
            self.SenderEMail = value_
            self.SenderEMail_nsprefix_ = child_.prefix
        elif nodeName_ == 'ToFirstName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ToFirstName')
            value_ = self.gds_validate_string(value_, node, 'ToFirstName')
            self.ToFirstName = value_
            self.ToFirstName_nsprefix_ = child_.prefix
        elif nodeName_ == 'ToLastName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ToLastName')
            value_ = self.gds_validate_string(value_, node, 'ToLastName')
            self.ToLastName = value_
            self.ToLastName_nsprefix_ = child_.prefix
        elif nodeName_ == 'ToFirm':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ToFirm')
            value_ = self.gds_validate_string(value_, node, 'ToFirm')
            self.ToFirm = value_
            self.ToFirm_nsprefix_ = child_.prefix
        elif nodeName_ == 'ToAddress1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ToAddress1')
            value_ = self.gds_validate_string(value_, node, 'ToAddress1')
            self.ToAddress1 = value_
            self.ToAddress1_nsprefix_ = child_.prefix
        elif nodeName_ == 'ToAddress2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ToAddress2')
            value_ = self.gds_validate_string(value_, node, 'ToAddress2')
            self.ToAddress2 = value_
            self.ToAddress2_nsprefix_ = child_.prefix
        elif nodeName_ == 'ToAddress3':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ToAddress3')
            value_ = self.gds_validate_string(value_, node, 'ToAddress3')
            self.ToAddress3 = value_
            self.ToAddress3_nsprefix_ = child_.prefix
        elif nodeName_ == 'ToPostalCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ToPostalCode')
            value_ = self.gds_validate_string(value_, node, 'ToPostalCode')
            self.ToPostalCode = value_
            self.ToPostalCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'ToPhone':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ToPhone')
            value_ = self.gds_validate_string(value_, node, 'ToPhone')
            self.ToPhone = value_
            self.ToPhone_nsprefix_ = child_.prefix
        elif nodeName_ == 'RecipientEMail':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RecipientEMail')
            value_ = self.gds_validate_string(value_, node, 'RecipientEMail')
            self.RecipientEMail = value_
            self.RecipientEMail_nsprefix_ = child_.prefix
        elif nodeName_ == 'ToDPID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ToDPID')
            value_ = self.gds_validate_string(value_, node, 'ToDPID')
            self.ToDPID = value_
            self.ToDPID_nsprefix_ = child_.prefix
        elif nodeName_ == 'ToProvince':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ToProvince')
            value_ = self.gds_validate_string(value_, node, 'ToProvince')
            self.ToProvince = value_
            self.ToProvince_nsprefix_ = child_.prefix
        elif nodeName_ == 'ToTaxID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ToTaxID')
            value_ = self.gds_validate_string(value_, node, 'ToTaxID')
            self.ToTaxID = value_
            self.ToTaxID_nsprefix_ = child_.prefix
        elif nodeName_ == 'Container':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Container')
            value_ = self.gds_validate_string(value_, node, 'Container')
            self.Container = value_
            self.Container_nsprefix_ = child_.prefix
        elif nodeName_ == 'ContentType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ContentType')
            value_ = self.gds_validate_string(value_, node, 'ContentType')
            self.ContentType = value_
            self.ContentType_nsprefix_ = child_.prefix
        elif nodeName_ == 'ShippingContents':
            obj_ = ShippingContentsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShippingContents = obj_
            obj_.original_tagname_ = 'ShippingContents'
        elif nodeName_ == 'PurposeOfShipment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PurposeOfShipment')
            value_ = self.gds_validate_string(value_, node, 'PurposeOfShipment')
            self.PurposeOfShipment = value_
            self.PurposeOfShipment_nsprefix_ = child_.prefix
        elif nodeName_ == 'PartiesToTransaction':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PartiesToTransaction')
            value_ = self.gds_validate_string(value_, node, 'PartiesToTransaction')
            self.PartiesToTransaction = value_
            self.PartiesToTransaction_nsprefix_ = child_.prefix
        elif nodeName_ == 'Agreement':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Agreement')
            value_ = self.gds_validate_string(value_, node, 'Agreement')
            self.Agreement = value_
            self.Agreement_nsprefix_ = child_.prefix
        elif nodeName_ == 'Postage':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Postage')
            value_ = self.gds_validate_string(value_, node, 'Postage')
            self.Postage = value_
            self.Postage_nsprefix_ = child_.prefix
        elif nodeName_ == 'InsuredValue':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'InsuredValue')
            value_ = self.gds_validate_string(value_, node, 'InsuredValue')
            self.InsuredValue = value_
            self.InsuredValue_nsprefix_ = child_.prefix
        elif nodeName_ == 'GrossPounds' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'GrossPounds')
            ival_ = self.gds_validate_integer(ival_, node, 'GrossPounds')
            self.GrossPounds = ival_
            self.GrossPounds_nsprefix_ = child_.prefix
        elif nodeName_ == 'GrossOunces' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'GrossOunces')
            ival_ = self.gds_validate_integer(ival_, node, 'GrossOunces')
            self.GrossOunces = ival_
            self.GrossOunces_nsprefix_ = child_.prefix
        elif nodeName_ == 'Length' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_float(sval_, node, 'Length')
            fval_ = self.gds_validate_float(fval_, node, 'Length')
            self.Length = fval_
            self.Length_nsprefix_ = child_.prefix
        elif nodeName_ == 'Width' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_float(sval_, node, 'Width')
            fval_ = self.gds_validate_float(fval_, node, 'Width')
            self.Width = fval_
            self.Width_nsprefix_ = child_.prefix
        elif nodeName_ == 'Height' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_float(sval_, node, 'Height')
            fval_ = self.gds_validate_float(fval_, node, 'Height')
            self.Height = fval_
            self.Height_nsprefix_ = child_.prefix
        elif nodeName_ == 'Girth' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_float(sval_, node, 'Girth')
            fval_ = self.gds_validate_float(fval_, node, 'Girth')
            self.Girth = fval_
            self.Girth_nsprefix_ = child_.prefix
        elif nodeName_ == 'Shape':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Shape')
            value_ = self.gds_validate_string(value_, node, 'Shape')
            self.Shape = value_
            self.Shape_nsprefix_ = child_.prefix
        elif nodeName_ == 'CIRequired':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CIRequired')
            value_ = self.gds_validate_string(value_, node, 'CIRequired')
            self.CIRequired = value_
            self.CIRequired_nsprefix_ = child_.prefix
        elif nodeName_ == 'InvoiceDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'InvoiceDate')
            value_ = self.gds_validate_string(value_, node, 'InvoiceDate')
            self.InvoiceDate = value_
            self.InvoiceDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'InvoiceNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'InvoiceNumber')
            value_ = self.gds_validate_string(value_, node, 'InvoiceNumber')
            self.InvoiceNumber = value_
            self.InvoiceNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'CustomerOrderNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CustomerOrderNumber')
            value_ = self.gds_validate_string(value_, node, 'CustomerOrderNumber')
            self.CustomerOrderNumber = value_
            self.CustomerOrderNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'CustOrderNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CustOrderNumber')
            value_ = self.gds_validate_string(value_, node, 'CustOrderNumber')
            self.CustOrderNumber = value_
            self.CustOrderNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'TermsDelivery':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TermsDelivery')
            value_ = self.gds_validate_string(value_, node, 'TermsDelivery')
            self.TermsDelivery = value_
            self.TermsDelivery_nsprefix_ = child_.prefix
        elif nodeName_ == 'TermsDeliveryOther':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TermsDeliveryOther')
            value_ = self.gds_validate_string(value_, node, 'TermsDeliveryOther')
            self.TermsDeliveryOther = value_
            self.TermsDeliveryOther_nsprefix_ = child_.prefix
        elif nodeName_ == 'PackingCost' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'PackingCost')
            fval_ = self.gds_validate_decimal(fval_, node, 'PackingCost')
            self.PackingCost = fval_
            self.PackingCost_nsprefix_ = child_.prefix
        elif nodeName_ == 'CountryUltDest':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryUltDest')
            value_ = self.gds_validate_string(value_, node, 'CountryUltDest')
            self.CountryUltDest = value_
            self.CountryUltDest_nsprefix_ = child_.prefix
        elif nodeName_ == 'CIAgreement':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'CIAgreement')
            ival_ = self.gds_validate_boolean(ival_, node, 'CIAgreement')
            self.CIAgreement = ival_
            self.CIAgreement_nsprefix_ = child_.prefix
        elif nodeName_ == 'ImageType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ImageType')
            value_ = self.gds_validate_string(value_, node, 'ImageType')
            self.ImageType = value_
            self.ImageType_nsprefix_ = child_.prefix
        elif nodeName_ == 'ImageLayout':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ImageLayout')
            value_ = self.gds_validate_string(value_, node, 'ImageLayout')
            self.ImageLayout = value_
            self.ImageLayout_nsprefix_ = child_.prefix
        elif nodeName_ == 'CustomerRefNo':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CustomerRefNo')
            value_ = self.gds_validate_string(value_, node, 'CustomerRefNo')
            self.CustomerRefNo = value_
            self.CustomerRefNo_nsprefix_ = child_.prefix
        elif nodeName_ == 'CustomerRefNo2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CustomerRefNo2')
            value_ = self.gds_validate_string(value_, node, 'CustomerRefNo2')
            self.CustomerRefNo2 = value_
            self.CustomerRefNo2_nsprefix_ = child_.prefix
        elif nodeName_ == 'ShipDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShipDate')
            value_ = self.gds_validate_string(value_, node, 'ShipDate')
            self.ShipDate = value_
            self.ShipDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'HoldForManifest':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HoldForManifest')
            value_ = self.gds_validate_string(value_, node, 'HoldForManifest')
            self.HoldForManifest = value_
            self.HoldForManifest_nsprefix_ = child_.prefix
        elif nodeName_ == 'PriceOptions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PriceOptions')
            value_ = self.gds_validate_string(value_, node, 'PriceOptions')
            self.PriceOptions = value_
            self.PriceOptions_nsprefix_ = child_.prefix
        elif nodeName_ == 'CommercialShipment':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'CommercialShipment')
            ival_ = self.gds_validate_boolean(ival_, node, 'CommercialShipment')
            self.CommercialShipment = ival_
            self.CommercialShipment_nsprefix_ = child_.prefix
        elif nodeName_ == 'BuyerFirstName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BuyerFirstName')
            value_ = self.gds_validate_string(value_, node, 'BuyerFirstName')
            self.BuyerFirstName = value_
            self.BuyerFirstName_nsprefix_ = child_.prefix
        elif nodeName_ == 'BuyerLastName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BuyerLastName')
            value_ = self.gds_validate_string(value_, node, 'BuyerLastName')
            self.BuyerLastName = value_
            self.BuyerLastName_nsprefix_ = child_.prefix
        elif nodeName_ == 'BuyerAddress1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BuyerAddress1')
            value_ = self.gds_validate_string(value_, node, 'BuyerAddress1')
            self.BuyerAddress1 = value_
            self.BuyerAddress1_nsprefix_ = child_.prefix
        elif nodeName_ == 'BuyerAddress2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BuyerAddress2')
            value_ = self.gds_validate_string(value_, node, 'BuyerAddress2')
            self.BuyerAddress2 = value_
            self.BuyerAddress2_nsprefix_ = child_.prefix
        elif nodeName_ == 'BuyerAddress3':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BuyerAddress3')
            value_ = self.gds_validate_string(value_, node, 'BuyerAddress3')
            self.BuyerAddress3 = value_
            self.BuyerAddress3_nsprefix_ = child_.prefix
        elif nodeName_ == 'BuyerCity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BuyerCity')
            value_ = self.gds_validate_string(value_, node, 'BuyerCity')
            self.BuyerCity = value_
            self.BuyerCity_nsprefix_ = child_.prefix
        elif nodeName_ == 'BuyerState':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BuyerState')
            value_ = self.gds_validate_string(value_, node, 'BuyerState')
            self.BuyerState = value_
            self.BuyerState_nsprefix_ = child_.prefix
        elif nodeName_ == 'BuyerPostalCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BuyerPostalCode')
            value_ = self.gds_validate_string(value_, node, 'BuyerPostalCode')
            self.BuyerPostalCode = value_
            self.BuyerPostalCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'BuyerCountry':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BuyerCountry')
            value_ = self.gds_validate_string(value_, node, 'BuyerCountry')
            self.BuyerCountry = value_
            self.BuyerCountry_nsprefix_ = child_.prefix
        elif nodeName_ == 'BuyerTaxID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BuyerTaxID')
            value_ = self.gds_validate_string(value_, node, 'BuyerTaxID')
            self.BuyerTaxID = value_
            self.BuyerTaxID_nsprefix_ = child_.prefix
        elif nodeName_ == 'BuyerRecipient':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'BuyerRecipient')
            ival_ = self.gds_validate_boolean(ival_, node, 'BuyerRecipient')
            self.BuyerRecipient = ival_
            self.BuyerRecipient_nsprefix_ = child_.prefix
        elif nodeName_ == 'TermsPayment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TermsPayment')
            value_ = self.gds_validate_string(value_, node, 'TermsPayment')
            self.TermsPayment = value_
            self.TermsPayment_nsprefix_ = child_.prefix
        elif nodeName_ == 'ActionCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ActionCode')
            value_ = self.gds_validate_string(value_, node, 'ActionCode')
            self.ActionCode = value_
            self.ActionCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'OptOutOfSPE':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OptOutOfSPE')
            value_ = self.gds_validate_string(value_, node, 'OptOutOfSPE')
            self.OptOutOfSPE = value_
            self.OptOutOfSPE_nsprefix_ = child_.prefix
        elif nodeName_ == 'PermitNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PermitNumber')
            value_ = self.gds_validate_string(value_, node, 'PermitNumber')
            self.PermitNumber = value_
            self.PermitNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'AccountZipCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AccountZipCode')
            value_ = self.gds_validate_string(value_, node, 'AccountZipCode')
            self.AccountZipCode = value_
            self.AccountZipCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'Machinable':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'Machinable')
            ival_ = self.gds_validate_boolean(ival_, node, 'Machinable')
            self.Machinable = ival_
            self.Machinable_nsprefix_ = child_.prefix
        elif nodeName_ == 'DestinationRateIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DestinationRateIndicator')
            value_ = self.gds_validate_string(value_, node, 'DestinationRateIndicator')
            self.DestinationRateIndicator = value_
            self.DestinationRateIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'MID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MID')
            value_ = self.gds_validate_string(value_, node, 'MID')
            self.MID = value_
            self.MID_nsprefix_ = child_.prefix
        elif nodeName_ == 'LogisticsManagerMID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LogisticsManagerMID')
            value_ = self.gds_validate_string(value_, node, 'LogisticsManagerMID')
            self.LogisticsManagerMID = value_
            self.LogisticsManagerMID_nsprefix_ = child_.prefix
        elif nodeName_ == 'CRID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CRID')
            value_ = self.gds_validate_string(value_, node, 'CRID')
            self.CRID = value_
            self.CRID_nsprefix_ = child_.prefix
        elif nodeName_ == 'VendorCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'VendorCode')
            value_ = self.gds_validate_string(value_, node, 'VendorCode')
            self.VendorCode = value_
            self.VendorCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'VendorProductVersionNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'VendorProductVersionNumber')
            value_ = self.gds_validate_string(value_, node, 'VendorProductVersionNumber')
            self.VendorProductVersionNumber = value_
            self.VendorProductVersionNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'OverrideMID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OverrideMID')
            value_ = self.gds_validate_string(value_, node, 'OverrideMID')
            self.OverrideMID = value_
            self.OverrideMID_nsprefix_ = child_.prefix
        elif nodeName_ == 'ChargebackCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChargebackCode')
            value_ = self.gds_validate_string(value_, node, 'ChargebackCode')
            self.ChargebackCode = value_
            self.ChargebackCode_nsprefix_ = child_.prefix
# end class eVSGXGGetLabelRequest


class ImageParametersType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ImageParameter=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ImageParameter = ImageParameter
        self.ImageParameter_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ImageParametersType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ImageParametersType.subclass:
            return ImageParametersType.subclass(*args_, **kwargs_)
        else:
            return ImageParametersType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ImageParameter(self):
        return self.ImageParameter
    def set_ImageParameter(self, ImageParameter):
        self.ImageParameter = ImageParameter
    def hasContent_(self):
        if (
            self.ImageParameter is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ImageParametersType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ImageParametersType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ImageParametersType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ImageParametersType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ImageParametersType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ImageParametersType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ImageParametersType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ImageParameter is not None:
            namespaceprefix_ = self.ImageParameter_nsprefix_ + ':' if (UseCapturedNS_ and self.ImageParameter_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sImageParameter>%s</%sImageParameter>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ImageParameter), input_name='ImageParameter')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ImageParameter':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ImageParameter')
            value_ = self.gds_validate_string(value_, node, 'ImageParameter')
            self.ImageParameter = value_
            self.ImageParameter_nsprefix_ = child_.prefix
# end class ImageParametersType


class ShippingContentsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ItemDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if ItemDetail is None:
            self.ItemDetail = []
        else:
            self.ItemDetail = ItemDetail
        self.ItemDetail_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShippingContentsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShippingContentsType.subclass:
            return ShippingContentsType.subclass(*args_, **kwargs_)
        else:
            return ShippingContentsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ItemDetail(self):
        return self.ItemDetail
    def set_ItemDetail(self, ItemDetail):
        self.ItemDetail = ItemDetail
    def add_ItemDetail(self, value):
        self.ItemDetail.append(value)
    def insert_ItemDetail_at(self, index, value):
        self.ItemDetail.insert(index, value)
    def replace_ItemDetail_at(self, index, value):
        self.ItemDetail[index] = value
    def hasContent_(self):
        if (
            self.ItemDetail
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShippingContentsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShippingContentsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShippingContentsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShippingContentsType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShippingContentsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShippingContentsType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShippingContentsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for ItemDetail_ in self.ItemDetail:
            namespaceprefix_ = self.ItemDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ItemDetail_nsprefix_) else ''
            ItemDetail_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ItemDetail', pretty_print=pretty_print)
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
        if nodeName_ == 'ItemDetail':
            obj_ = ItemDetailType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ItemDetail.append(obj_)
            obj_.original_tagname_ = 'ItemDetail'
# end class ShippingContentsType


class ItemDetailType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Description=None, Commodity=None, Restriction=None, Quantity=None, UnitValue=None, NetPounds=None, NetOunces=None, UnitOfMeasure=None, HSTariffNumber=None, CountryofManufacture=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = None
        self.Commodity = Commodity
        self.Commodity_nsprefix_ = None
        self.Restriction = Restriction
        self.Restriction_nsprefix_ = None
        self.Quantity = Quantity
        self.Quantity_nsprefix_ = None
        self.UnitValue = UnitValue
        self.UnitValue_nsprefix_ = None
        self.NetPounds = NetPounds
        self.NetPounds_nsprefix_ = None
        self.NetOunces = NetOunces
        self.NetOunces_nsprefix_ = None
        self.UnitOfMeasure = UnitOfMeasure
        self.UnitOfMeasure_nsprefix_ = None
        self.HSTariffNumber = HSTariffNumber
        self.HSTariffNumber_nsprefix_ = None
        self.CountryofManufacture = CountryofManufacture
        self.CountryofManufacture_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ItemDetailType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ItemDetailType.subclass:
            return ItemDetailType.subclass(*args_, **kwargs_)
        else:
            return ItemDetailType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def get_Commodity(self):
        return self.Commodity
    def set_Commodity(self, Commodity):
        self.Commodity = Commodity
    def get_Restriction(self):
        return self.Restriction
    def set_Restriction(self, Restriction):
        self.Restriction = Restriction
    def get_Quantity(self):
        return self.Quantity
    def set_Quantity(self, Quantity):
        self.Quantity = Quantity
    def get_UnitValue(self):
        return self.UnitValue
    def set_UnitValue(self, UnitValue):
        self.UnitValue = UnitValue
    def get_NetPounds(self):
        return self.NetPounds
    def set_NetPounds(self, NetPounds):
        self.NetPounds = NetPounds
    def get_NetOunces(self):
        return self.NetOunces
    def set_NetOunces(self, NetOunces):
        self.NetOunces = NetOunces
    def get_UnitOfMeasure(self):
        return self.UnitOfMeasure
    def set_UnitOfMeasure(self, UnitOfMeasure):
        self.UnitOfMeasure = UnitOfMeasure
    def get_HSTariffNumber(self):
        return self.HSTariffNumber
    def set_HSTariffNumber(self, HSTariffNumber):
        self.HSTariffNumber = HSTariffNumber
    def get_CountryofManufacture(self):
        return self.CountryofManufacture
    def set_CountryofManufacture(self, CountryofManufacture):
        self.CountryofManufacture = CountryofManufacture
    def hasContent_(self):
        if (
            self.Description is not None or
            self.Commodity is not None or
            self.Restriction is not None or
            self.Quantity is not None or
            self.UnitValue is not None or
            self.NetPounds is not None or
            self.NetOunces is not None or
            self.UnitOfMeasure is not None or
            self.HSTariffNumber is not None or
            self.CountryofManufacture is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ItemDetailType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ItemDetailType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ItemDetailType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ItemDetailType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ItemDetailType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ItemDetailType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ItemDetailType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
        if self.Commodity is not None:
            namespaceprefix_ = self.Commodity_nsprefix_ + ':' if (UseCapturedNS_ and self.Commodity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCommodity>%s</%sCommodity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Commodity), input_name='Commodity')), namespaceprefix_ , eol_))
        if self.Restriction is not None:
            namespaceprefix_ = self.Restriction_nsprefix_ + ':' if (UseCapturedNS_ and self.Restriction_nsprefix_) else ''
            self.Restriction.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Restriction', pretty_print=pretty_print)
        if self.Quantity is not None:
            namespaceprefix_ = self.Quantity_nsprefix_ + ':' if (UseCapturedNS_ and self.Quantity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sQuantity>%s</%sQuantity>%s' % (namespaceprefix_ , self.gds_format_integer(self.Quantity, input_name='Quantity'), namespaceprefix_ , eol_))
        if self.UnitValue is not None:
            namespaceprefix_ = self.UnitValue_nsprefix_ + ':' if (UseCapturedNS_ and self.UnitValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUnitValue>%s</%sUnitValue>%s' % (namespaceprefix_ , self.gds_format_float(self.UnitValue, input_name='UnitValue'), namespaceprefix_ , eol_))
        if self.NetPounds is not None:
            namespaceprefix_ = self.NetPounds_nsprefix_ + ':' if (UseCapturedNS_ and self.NetPounds_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNetPounds>%s</%sNetPounds>%s' % (namespaceprefix_ , self.gds_format_float(self.NetPounds, input_name='NetPounds'), namespaceprefix_ , eol_))
        if self.NetOunces is not None:
            namespaceprefix_ = self.NetOunces_nsprefix_ + ':' if (UseCapturedNS_ and self.NetOunces_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNetOunces>%s</%sNetOunces>%s' % (namespaceprefix_ , self.gds_format_float(self.NetOunces, input_name='NetOunces'), namespaceprefix_ , eol_))
        if self.UnitOfMeasure is not None:
            namespaceprefix_ = self.UnitOfMeasure_nsprefix_ + ':' if (UseCapturedNS_ and self.UnitOfMeasure_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUnitOfMeasure>%s</%sUnitOfMeasure>%s' % (namespaceprefix_ , self.gds_format_float(self.UnitOfMeasure, input_name='UnitOfMeasure'), namespaceprefix_ , eol_))
        if self.HSTariffNumber is not None:
            namespaceprefix_ = self.HSTariffNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.HSTariffNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHSTariffNumber>%s</%sHSTariffNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.HSTariffNumber, input_name='HSTariffNumber'), namespaceprefix_ , eol_))
        if self.CountryofManufacture is not None:
            namespaceprefix_ = self.CountryofManufacture_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryofManufacture_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryofManufacture>%s</%sCountryofManufacture>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryofManufacture), input_name='CountryofManufacture')), namespaceprefix_ , eol_))
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
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
        elif nodeName_ == 'Commodity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Commodity')
            value_ = self.gds_validate_string(value_, node, 'Commodity')
            self.Commodity = value_
            self.Commodity_nsprefix_ = child_.prefix
        elif nodeName_ == 'Restriction':
            obj_ = RestrictionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Restriction = obj_
            obj_.original_tagname_ = 'Restriction'
        elif nodeName_ == 'Quantity' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Quantity')
            ival_ = self.gds_validate_integer(ival_, node, 'Quantity')
            self.Quantity = ival_
            self.Quantity_nsprefix_ = child_.prefix
        elif nodeName_ == 'UnitValue' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_float(sval_, node, 'UnitValue')
            fval_ = self.gds_validate_float(fval_, node, 'UnitValue')
            self.UnitValue = fval_
            self.UnitValue_nsprefix_ = child_.prefix
        elif nodeName_ == 'NetPounds' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_float(sval_, node, 'NetPounds')
            fval_ = self.gds_validate_float(fval_, node, 'NetPounds')
            self.NetPounds = fval_
            self.NetPounds_nsprefix_ = child_.prefix
        elif nodeName_ == 'NetOunces' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_float(sval_, node, 'NetOunces')
            fval_ = self.gds_validate_float(fval_, node, 'NetOunces')
            self.NetOunces = fval_
            self.NetOunces_nsprefix_ = child_.prefix
        elif nodeName_ == 'UnitOfMeasure' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_float(sval_, node, 'UnitOfMeasure')
            fval_ = self.gds_validate_float(fval_, node, 'UnitOfMeasure')
            self.UnitOfMeasure = fval_
            self.UnitOfMeasure_nsprefix_ = child_.prefix
        elif nodeName_ == 'HSTariffNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'HSTariffNumber')
            ival_ = self.gds_validate_integer(ival_, node, 'HSTariffNumber')
            self.HSTariffNumber = ival_
            self.HSTariffNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'CountryofManufacture':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryofManufacture')
            value_ = self.gds_validate_string(value_, node, 'CountryofManufacture')
            self.CountryofManufacture = value_
            self.CountryofManufacture_nsprefix_ = child_.prefix
# end class ItemDetailType


class RestrictionType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, FootnoteNumber=None, Response=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.FootnoteNumber = FootnoteNumber
        self.FootnoteNumber_nsprefix_ = None
        self.Response = Response
        self.Response_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RestrictionType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RestrictionType.subclass:
            return RestrictionType.subclass(*args_, **kwargs_)
        else:
            return RestrictionType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_FootnoteNumber(self):
        return self.FootnoteNumber
    def set_FootnoteNumber(self, FootnoteNumber):
        self.FootnoteNumber = FootnoteNumber
    def get_Response(self):
        return self.Response
    def set_Response(self, Response):
        self.Response = Response
    def hasContent_(self):
        if (
            self.FootnoteNumber is not None or
            self.Response is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RestrictionType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RestrictionType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RestrictionType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RestrictionType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RestrictionType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RestrictionType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RestrictionType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.FootnoteNumber is not None:
            namespaceprefix_ = self.FootnoteNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.FootnoteNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFootnoteNumber>%s</%sFootnoteNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FootnoteNumber), input_name='FootnoteNumber')), namespaceprefix_ , eol_))
        if self.Response is not None:
            namespaceprefix_ = self.Response_nsprefix_ + ':' if (UseCapturedNS_ and self.Response_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sResponse>%s</%sResponse>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Response), input_name='Response')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'FootnoteNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FootnoteNumber')
            value_ = self.gds_validate_string(value_, node, 'FootnoteNumber')
            self.FootnoteNumber = value_
            self.FootnoteNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'Response':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Response')
            value_ = self.gds_validate_string(value_, node, 'Response')
            self.Response = value_
            self.Response_nsprefix_ = child_.prefix
# end class RestrictionType


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
        rootTag = 'eVSGXGGetLabelRequest'
        rootClass = eVSGXGGetLabelRequest
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
        rootTag = 'eVSGXGGetLabelRequest'
        rootClass = eVSGXGGetLabelRequest
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
        rootTag = 'eVSGXGGetLabelRequest'
        rootClass = eVSGXGGetLabelRequest
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
        rootTag = 'eVSGXGGetLabelRequest'
        rootClass = eVSGXGGetLabelRequest
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from evs_gxg_get_label_request import *\n\n')
        sys.stdout.write('import evs_gxg_get_label_request as model_\n\n')
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
    "ImageParametersType",
    "ItemDetailType",
    "RestrictionType",
    "ShippingContentsType",
    "eVSGXGGetLabelRequest"
]
