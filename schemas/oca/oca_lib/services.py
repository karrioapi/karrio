#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Thu Feb  4 18:28:32 2021 by generateDS.py version 2.37.15.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './oca_lib/services.py')
#
# Command line arguments:
#   ./schemas/services.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./oca_lib/services.py" ./schemas/services.xsd
#
# Current working directory (os.getcwd()):
#   oca
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


class List_Envios(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CUIT=None, FechaDesde=None, FechaHasta=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CUIT = CUIT
        self.CUIT_nsprefix_ = None
        self.FechaDesde = FechaDesde
        self.FechaDesde_nsprefix_ = None
        self.FechaHasta = FechaHasta
        self.FechaHasta_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, List_Envios)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if List_Envios.subclass:
            return List_Envios.subclass(*args_, **kwargs_)
        else:
            return List_Envios(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CUIT(self):
        return self.CUIT
    def set_CUIT(self, CUIT):
        self.CUIT = CUIT
    def get_FechaDesde(self):
        return self.FechaDesde
    def set_FechaDesde(self, FechaDesde):
        self.FechaDesde = FechaDesde
    def get_FechaHasta(self):
        return self.FechaHasta
    def set_FechaHasta(self, FechaHasta):
        self.FechaHasta = FechaHasta
    def hasContent_(self):
        if (
            self.CUIT is not None or
            self.FechaDesde is not None or
            self.FechaHasta is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='List_Envios', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('List_Envios')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'List_Envios':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='List_Envios')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='List_Envios', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='List_Envios'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='List_Envios', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CUIT is not None:
            namespaceprefix_ = self.CUIT_nsprefix_ + ':' if (UseCapturedNS_ and self.CUIT_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCUIT>%s</%sCUIT>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CUIT), input_name='CUIT')), namespaceprefix_ , eol_))
        if self.FechaDesde is not None:
            namespaceprefix_ = self.FechaDesde_nsprefix_ + ':' if (UseCapturedNS_ and self.FechaDesde_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFechaDesde>%s</%sFechaDesde>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FechaDesde), input_name='FechaDesde')), namespaceprefix_ , eol_))
        if self.FechaHasta is not None:
            namespaceprefix_ = self.FechaHasta_nsprefix_ + ':' if (UseCapturedNS_ and self.FechaHasta_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFechaHasta>%s</%sFechaHasta>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FechaHasta), input_name='FechaHasta')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'CUIT':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CUIT')
            value_ = self.gds_validate_string(value_, node, 'CUIT')
            self.CUIT = value_
            self.CUIT_nsprefix_ = child_.prefix
        elif nodeName_ == 'FechaDesde':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FechaDesde')
            value_ = self.gds_validate_string(value_, node, 'FechaDesde')
            self.FechaDesde = value_
            self.FechaDesde_nsprefix_ = child_.prefix
        elif nodeName_ == 'FechaHasta':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FechaHasta')
            value_ = self.gds_validate_string(value_, node, 'FechaHasta')
            self.FechaHasta = value_
            self.FechaHasta_nsprefix_ = child_.prefix
# end class List_Envios


class List_EnviosResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, List_EnviosResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.List_EnviosResult = List_EnviosResult
        self.List_EnviosResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, List_EnviosResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if List_EnviosResponse.subclass:
            return List_EnviosResponse.subclass(*args_, **kwargs_)
        else:
            return List_EnviosResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_List_EnviosResult(self):
        return self.List_EnviosResult
    def set_List_EnviosResult(self, List_EnviosResult):
        self.List_EnviosResult = List_EnviosResult
    def hasContent_(self):
        if (
            self.List_EnviosResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='List_EnviosResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('List_EnviosResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'List_EnviosResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='List_EnviosResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='List_EnviosResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='List_EnviosResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='List_EnviosResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.List_EnviosResult is not None:
            namespaceprefix_ = self.List_EnviosResult_nsprefix_ + ':' if (UseCapturedNS_ and self.List_EnviosResult_nsprefix_) else ''
            self.List_EnviosResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='List_EnviosResult', pretty_print=pretty_print)
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
        if nodeName_ == 'List_EnviosResult':
            obj_ = List_EnviosResultType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.List_EnviosResult = obj_
            obj_.original_tagname_ = 'List_EnviosResult'
# end class List_EnviosResponse


class Tracking_Pieza(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, NroDocumentoCliente=None, CUIT=None, Pieza=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.NroDocumentoCliente = NroDocumentoCliente
        self.NroDocumentoCliente_nsprefix_ = None
        self.CUIT = CUIT
        self.CUIT_nsprefix_ = None
        self.Pieza = Pieza
        self.Pieza_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Tracking_Pieza)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Tracking_Pieza.subclass:
            return Tracking_Pieza.subclass(*args_, **kwargs_)
        else:
            return Tracking_Pieza(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_NroDocumentoCliente(self):
        return self.NroDocumentoCliente
    def set_NroDocumentoCliente(self, NroDocumentoCliente):
        self.NroDocumentoCliente = NroDocumentoCliente
    def get_CUIT(self):
        return self.CUIT
    def set_CUIT(self, CUIT):
        self.CUIT = CUIT
    def get_Pieza(self):
        return self.Pieza
    def set_Pieza(self, Pieza):
        self.Pieza = Pieza
    def hasContent_(self):
        if (
            self.NroDocumentoCliente is not None or
            self.CUIT is not None or
            self.Pieza is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Tracking_Pieza', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Tracking_Pieza')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Tracking_Pieza':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Tracking_Pieza')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Tracking_Pieza', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Tracking_Pieza'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Tracking_Pieza', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.NroDocumentoCliente is not None:
            namespaceprefix_ = self.NroDocumentoCliente_nsprefix_ + ':' if (UseCapturedNS_ and self.NroDocumentoCliente_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNroDocumentoCliente>%s</%sNroDocumentoCliente>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NroDocumentoCliente), input_name='NroDocumentoCliente')), namespaceprefix_ , eol_))
        if self.CUIT is not None:
            namespaceprefix_ = self.CUIT_nsprefix_ + ':' if (UseCapturedNS_ and self.CUIT_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCUIT>%s</%sCUIT>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CUIT), input_name='CUIT')), namespaceprefix_ , eol_))
        if self.Pieza is not None:
            namespaceprefix_ = self.Pieza_nsprefix_ + ':' if (UseCapturedNS_ and self.Pieza_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPieza>%s</%sPieza>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Pieza), input_name='Pieza')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'NroDocumentoCliente':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NroDocumentoCliente')
            value_ = self.gds_validate_string(value_, node, 'NroDocumentoCliente')
            self.NroDocumentoCliente = value_
            self.NroDocumentoCliente_nsprefix_ = child_.prefix
        elif nodeName_ == 'CUIT':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CUIT')
            value_ = self.gds_validate_string(value_, node, 'CUIT')
            self.CUIT = value_
            self.CUIT_nsprefix_ = child_.prefix
        elif nodeName_ == 'Pieza':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Pieza')
            value_ = self.gds_validate_string(value_, node, 'Pieza')
            self.Pieza = value_
            self.Pieza_nsprefix_ = child_.prefix
# end class Tracking_Pieza


class Tracking_PiezaResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Tracking_PiezaResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Tracking_PiezaResult = Tracking_PiezaResult
        self.Tracking_PiezaResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Tracking_PiezaResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Tracking_PiezaResponse.subclass:
            return Tracking_PiezaResponse.subclass(*args_, **kwargs_)
        else:
            return Tracking_PiezaResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Tracking_PiezaResult(self):
        return self.Tracking_PiezaResult
    def set_Tracking_PiezaResult(self, Tracking_PiezaResult):
        self.Tracking_PiezaResult = Tracking_PiezaResult
    def hasContent_(self):
        if (
            self.Tracking_PiezaResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Tracking_PiezaResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Tracking_PiezaResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Tracking_PiezaResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Tracking_PiezaResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Tracking_PiezaResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Tracking_PiezaResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Tracking_PiezaResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Tracking_PiezaResult is not None:
            namespaceprefix_ = self.Tracking_PiezaResult_nsprefix_ + ':' if (UseCapturedNS_ and self.Tracking_PiezaResult_nsprefix_) else ''
            self.Tracking_PiezaResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Tracking_PiezaResult', pretty_print=pretty_print)
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
        if nodeName_ == 'Tracking_PiezaResult':
            obj_ = Tracking_PiezaResultType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Tracking_PiezaResult = obj_
            obj_.original_tagname_ = 'Tracking_PiezaResult'
# end class Tracking_PiezaResponse


class Tracking_OrdenRetiro(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CUIT=None, OrdenRetiro=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CUIT = CUIT
        self.CUIT_nsprefix_ = None
        self.OrdenRetiro = OrdenRetiro
        self.OrdenRetiro_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Tracking_OrdenRetiro)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Tracking_OrdenRetiro.subclass:
            return Tracking_OrdenRetiro.subclass(*args_, **kwargs_)
        else:
            return Tracking_OrdenRetiro(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CUIT(self):
        return self.CUIT
    def set_CUIT(self, CUIT):
        self.CUIT = CUIT
    def get_OrdenRetiro(self):
        return self.OrdenRetiro
    def set_OrdenRetiro(self, OrdenRetiro):
        self.OrdenRetiro = OrdenRetiro
    def hasContent_(self):
        if (
            self.CUIT is not None or
            self.OrdenRetiro is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Tracking_OrdenRetiro', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Tracking_OrdenRetiro')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Tracking_OrdenRetiro':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Tracking_OrdenRetiro')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Tracking_OrdenRetiro', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Tracking_OrdenRetiro'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Tracking_OrdenRetiro', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CUIT is not None:
            namespaceprefix_ = self.CUIT_nsprefix_ + ':' if (UseCapturedNS_ and self.CUIT_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCUIT>%s</%sCUIT>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CUIT), input_name='CUIT')), namespaceprefix_ , eol_))
        if self.OrdenRetiro is not None:
            namespaceprefix_ = self.OrdenRetiro_nsprefix_ + ':' if (UseCapturedNS_ and self.OrdenRetiro_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOrdenRetiro>%s</%sOrdenRetiro>%s' % (namespaceprefix_ , self.gds_format_integer(self.OrdenRetiro, input_name='OrdenRetiro'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'CUIT':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CUIT')
            value_ = self.gds_validate_string(value_, node, 'CUIT')
            self.CUIT = value_
            self.CUIT_nsprefix_ = child_.prefix
        elif nodeName_ == 'OrdenRetiro' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'OrdenRetiro')
            ival_ = self.gds_validate_integer(ival_, node, 'OrdenRetiro')
            self.OrdenRetiro = ival_
            self.OrdenRetiro_nsprefix_ = child_.prefix
# end class Tracking_OrdenRetiro


class Tracking_OrdenRetiroResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Tracking_OrdenRetiroResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Tracking_OrdenRetiroResult = Tracking_OrdenRetiroResult
        self.Tracking_OrdenRetiroResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Tracking_OrdenRetiroResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Tracking_OrdenRetiroResponse.subclass:
            return Tracking_OrdenRetiroResponse.subclass(*args_, **kwargs_)
        else:
            return Tracking_OrdenRetiroResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Tracking_OrdenRetiroResult(self):
        return self.Tracking_OrdenRetiroResult
    def set_Tracking_OrdenRetiroResult(self, Tracking_OrdenRetiroResult):
        self.Tracking_OrdenRetiroResult = Tracking_OrdenRetiroResult
    def hasContent_(self):
        if (
            self.Tracking_OrdenRetiroResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Tracking_OrdenRetiroResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Tracking_OrdenRetiroResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Tracking_OrdenRetiroResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Tracking_OrdenRetiroResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Tracking_OrdenRetiroResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Tracking_OrdenRetiroResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Tracking_OrdenRetiroResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Tracking_OrdenRetiroResult is not None:
            namespaceprefix_ = self.Tracking_OrdenRetiroResult_nsprefix_ + ':' if (UseCapturedNS_ and self.Tracking_OrdenRetiroResult_nsprefix_) else ''
            self.Tracking_OrdenRetiroResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Tracking_OrdenRetiroResult', pretty_print=pretty_print)
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
        if nodeName_ == 'Tracking_OrdenRetiroResult':
            obj_ = Tracking_OrdenRetiroResultType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Tracking_OrdenRetiroResult = obj_
            obj_.original_tagname_ = 'Tracking_OrdenRetiroResult'
# end class Tracking_OrdenRetiroResponse


class Tarifar_Envio_Corporativo(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PesoTotal=None, VolumenTotal=None, CodigoPostalOrigen=None, CodigoPostalDestino=None, CantidadPaquetes=None, Cuit=None, Operativa=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PesoTotal = PesoTotal
        self.PesoTotal_nsprefix_ = None
        self.VolumenTotal = VolumenTotal
        self.VolumenTotal_nsprefix_ = None
        self.CodigoPostalOrigen = CodigoPostalOrigen
        self.CodigoPostalOrigen_nsprefix_ = None
        self.CodigoPostalDestino = CodigoPostalDestino
        self.CodigoPostalDestino_nsprefix_ = None
        self.CantidadPaquetes = CantidadPaquetes
        self.CantidadPaquetes_nsprefix_ = None
        self.Cuit = Cuit
        self.Cuit_nsprefix_ = None
        self.Operativa = Operativa
        self.Operativa_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Tarifar_Envio_Corporativo)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Tarifar_Envio_Corporativo.subclass:
            return Tarifar_Envio_Corporativo.subclass(*args_, **kwargs_)
        else:
            return Tarifar_Envio_Corporativo(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PesoTotal(self):
        return self.PesoTotal
    def set_PesoTotal(self, PesoTotal):
        self.PesoTotal = PesoTotal
    def get_VolumenTotal(self):
        return self.VolumenTotal
    def set_VolumenTotal(self, VolumenTotal):
        self.VolumenTotal = VolumenTotal
    def get_CodigoPostalOrigen(self):
        return self.CodigoPostalOrigen
    def set_CodigoPostalOrigen(self, CodigoPostalOrigen):
        self.CodigoPostalOrigen = CodigoPostalOrigen
    def get_CodigoPostalDestino(self):
        return self.CodigoPostalDestino
    def set_CodigoPostalDestino(self, CodigoPostalDestino):
        self.CodigoPostalDestino = CodigoPostalDestino
    def get_CantidadPaquetes(self):
        return self.CantidadPaquetes
    def set_CantidadPaquetes(self, CantidadPaquetes):
        self.CantidadPaquetes = CantidadPaquetes
    def get_Cuit(self):
        return self.Cuit
    def set_Cuit(self, Cuit):
        self.Cuit = Cuit
    def get_Operativa(self):
        return self.Operativa
    def set_Operativa(self, Operativa):
        self.Operativa = Operativa
    def hasContent_(self):
        if (
            self.PesoTotal is not None or
            self.VolumenTotal is not None or
            self.CodigoPostalOrigen is not None or
            self.CodigoPostalDestino is not None or
            self.CantidadPaquetes is not None or
            self.Cuit is not None or
            self.Operativa is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Tarifar_Envio_Corporativo', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Tarifar_Envio_Corporativo')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Tarifar_Envio_Corporativo':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Tarifar_Envio_Corporativo')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Tarifar_Envio_Corporativo', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Tarifar_Envio_Corporativo'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Tarifar_Envio_Corporativo', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PesoTotal is not None:
            namespaceprefix_ = self.PesoTotal_nsprefix_ + ':' if (UseCapturedNS_ and self.PesoTotal_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPesoTotal>%s</%sPesoTotal>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PesoTotal), input_name='PesoTotal')), namespaceprefix_ , eol_))
        if self.VolumenTotal is not None:
            namespaceprefix_ = self.VolumenTotal_nsprefix_ + ':' if (UseCapturedNS_ and self.VolumenTotal_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sVolumenTotal>%s</%sVolumenTotal>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.VolumenTotal), input_name='VolumenTotal')), namespaceprefix_ , eol_))
        if self.CodigoPostalOrigen is not None:
            namespaceprefix_ = self.CodigoPostalOrigen_nsprefix_ + ':' if (UseCapturedNS_ and self.CodigoPostalOrigen_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodigoPostalOrigen>%s</%sCodigoPostalOrigen>%s' % (namespaceprefix_ , self.gds_format_integer(self.CodigoPostalOrigen, input_name='CodigoPostalOrigen'), namespaceprefix_ , eol_))
        if self.CodigoPostalDestino is not None:
            namespaceprefix_ = self.CodigoPostalDestino_nsprefix_ + ':' if (UseCapturedNS_ and self.CodigoPostalDestino_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodigoPostalDestino>%s</%sCodigoPostalDestino>%s' % (namespaceprefix_ , self.gds_format_integer(self.CodigoPostalDestino, input_name='CodigoPostalDestino'), namespaceprefix_ , eol_))
        if self.CantidadPaquetes is not None:
            namespaceprefix_ = self.CantidadPaquetes_nsprefix_ + ':' if (UseCapturedNS_ and self.CantidadPaquetes_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCantidadPaquetes>%s</%sCantidadPaquetes>%s' % (namespaceprefix_ , self.gds_format_integer(self.CantidadPaquetes, input_name='CantidadPaquetes'), namespaceprefix_ , eol_))
        if self.Cuit is not None:
            namespaceprefix_ = self.Cuit_nsprefix_ + ':' if (UseCapturedNS_ and self.Cuit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCuit>%s</%sCuit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Cuit), input_name='Cuit')), namespaceprefix_ , eol_))
        if self.Operativa is not None:
            namespaceprefix_ = self.Operativa_nsprefix_ + ':' if (UseCapturedNS_ and self.Operativa_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOperativa>%s</%sOperativa>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Operativa), input_name='Operativa')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'PesoTotal':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PesoTotal')
            value_ = self.gds_validate_string(value_, node, 'PesoTotal')
            self.PesoTotal = value_
            self.PesoTotal_nsprefix_ = child_.prefix
        elif nodeName_ == 'VolumenTotal':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'VolumenTotal')
            value_ = self.gds_validate_string(value_, node, 'VolumenTotal')
            self.VolumenTotal = value_
            self.VolumenTotal_nsprefix_ = child_.prefix
        elif nodeName_ == 'CodigoPostalOrigen' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'CodigoPostalOrigen')
            ival_ = self.gds_validate_integer(ival_, node, 'CodigoPostalOrigen')
            self.CodigoPostalOrigen = ival_
            self.CodigoPostalOrigen_nsprefix_ = child_.prefix
        elif nodeName_ == 'CodigoPostalDestino' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'CodigoPostalDestino')
            ival_ = self.gds_validate_integer(ival_, node, 'CodigoPostalDestino')
            self.CodigoPostalDestino = ival_
            self.CodigoPostalDestino_nsprefix_ = child_.prefix
        elif nodeName_ == 'CantidadPaquetes' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'CantidadPaquetes')
            ival_ = self.gds_validate_integer(ival_, node, 'CantidadPaquetes')
            self.CantidadPaquetes = ival_
            self.CantidadPaquetes_nsprefix_ = child_.prefix
        elif nodeName_ == 'Cuit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Cuit')
            value_ = self.gds_validate_string(value_, node, 'Cuit')
            self.Cuit = value_
            self.Cuit_nsprefix_ = child_.prefix
        elif nodeName_ == 'Operativa':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Operativa')
            value_ = self.gds_validate_string(value_, node, 'Operativa')
            self.Operativa = value_
            self.Operativa_nsprefix_ = child_.prefix
# end class Tarifar_Envio_Corporativo


class Tarifar_Envio_CorporativoResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Tarifar_Envio_CorporativoResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Tarifar_Envio_CorporativoResult = Tarifar_Envio_CorporativoResult
        self.Tarifar_Envio_CorporativoResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Tarifar_Envio_CorporativoResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Tarifar_Envio_CorporativoResponse.subclass:
            return Tarifar_Envio_CorporativoResponse.subclass(*args_, **kwargs_)
        else:
            return Tarifar_Envio_CorporativoResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Tarifar_Envio_CorporativoResult(self):
        return self.Tarifar_Envio_CorporativoResult
    def set_Tarifar_Envio_CorporativoResult(self, Tarifar_Envio_CorporativoResult):
        self.Tarifar_Envio_CorporativoResult = Tarifar_Envio_CorporativoResult
    def hasContent_(self):
        if (
            self.Tarifar_Envio_CorporativoResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Tarifar_Envio_CorporativoResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Tarifar_Envio_CorporativoResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Tarifar_Envio_CorporativoResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Tarifar_Envio_CorporativoResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Tarifar_Envio_CorporativoResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Tarifar_Envio_CorporativoResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Tarifar_Envio_CorporativoResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Tarifar_Envio_CorporativoResult is not None:
            namespaceprefix_ = self.Tarifar_Envio_CorporativoResult_nsprefix_ + ':' if (UseCapturedNS_ and self.Tarifar_Envio_CorporativoResult_nsprefix_) else ''
            self.Tarifar_Envio_CorporativoResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Tarifar_Envio_CorporativoResult', pretty_print=pretty_print)
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
        if nodeName_ == 'Tarifar_Envio_CorporativoResult':
            obj_ = Tarifar_Envio_CorporativoResultType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Tarifar_Envio_CorporativoResult = obj_
            obj_.original_tagname_ = 'Tarifar_Envio_CorporativoResult'
# end class Tarifar_Envio_CorporativoResponse


class AnularOrdenGenerada(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, usuario=None, password=None, nroOrden=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.usuario = usuario
        self.usuario_nsprefix_ = None
        self.password = password
        self.password_nsprefix_ = None
        self.nroOrden = nroOrden
        self.nroOrden_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AnularOrdenGenerada)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AnularOrdenGenerada.subclass:
            return AnularOrdenGenerada.subclass(*args_, **kwargs_)
        else:
            return AnularOrdenGenerada(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_usuario(self):
        return self.usuario
    def set_usuario(self, usuario):
        self.usuario = usuario
    def get_password(self):
        return self.password
    def set_password(self, password):
        self.password = password
    def get_nroOrden(self):
        return self.nroOrden
    def set_nroOrden(self, nroOrden):
        self.nroOrden = nroOrden
    def hasContent_(self):
        if (
            self.usuario is not None or
            self.password is not None or
            self.nroOrden is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AnularOrdenGenerada', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AnularOrdenGenerada')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AnularOrdenGenerada':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AnularOrdenGenerada')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AnularOrdenGenerada', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AnularOrdenGenerada'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AnularOrdenGenerada', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.usuario is not None:
            namespaceprefix_ = self.usuario_nsprefix_ + ':' if (UseCapturedNS_ and self.usuario_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%susuario>%s</%susuario>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.usuario), input_name='usuario')), namespaceprefix_ , eol_))
        if self.password is not None:
            namespaceprefix_ = self.password_nsprefix_ + ':' if (UseCapturedNS_ and self.password_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spassword>%s</%spassword>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.password), input_name='password')), namespaceprefix_ , eol_))
        if self.nroOrden is not None:
            namespaceprefix_ = self.nroOrden_nsprefix_ + ':' if (UseCapturedNS_ and self.nroOrden_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snroOrden>%s</%snroOrden>%s' % (namespaceprefix_ , self.gds_format_integer(self.nroOrden, input_name='nroOrden'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'usuario':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'usuario')
            value_ = self.gds_validate_string(value_, node, 'usuario')
            self.usuario = value_
            self.usuario_nsprefix_ = child_.prefix
        elif nodeName_ == 'password':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'password')
            value_ = self.gds_validate_string(value_, node, 'password')
            self.password = value_
            self.password_nsprefix_ = child_.prefix
        elif nodeName_ == 'nroOrden' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'nroOrden')
            ival_ = self.gds_validate_integer(ival_, node, 'nroOrden')
            self.nroOrden = ival_
            self.nroOrden_nsprefix_ = child_.prefix
# end class AnularOrdenGenerada


class AnularOrdenGeneradaResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AnularOrdenGeneradaResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.AnularOrdenGeneradaResult = AnularOrdenGeneradaResult
        self.AnularOrdenGeneradaResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AnularOrdenGeneradaResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AnularOrdenGeneradaResponse.subclass:
            return AnularOrdenGeneradaResponse.subclass(*args_, **kwargs_)
        else:
            return AnularOrdenGeneradaResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AnularOrdenGeneradaResult(self):
        return self.AnularOrdenGeneradaResult
    def set_AnularOrdenGeneradaResult(self, AnularOrdenGeneradaResult):
        self.AnularOrdenGeneradaResult = AnularOrdenGeneradaResult
    def hasContent_(self):
        if (
            self.AnularOrdenGeneradaResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AnularOrdenGeneradaResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AnularOrdenGeneradaResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AnularOrdenGeneradaResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AnularOrdenGeneradaResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AnularOrdenGeneradaResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AnularOrdenGeneradaResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AnularOrdenGeneradaResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.AnularOrdenGeneradaResult is not None:
            namespaceprefix_ = self.AnularOrdenGeneradaResult_nsprefix_ + ':' if (UseCapturedNS_ and self.AnularOrdenGeneradaResult_nsprefix_) else ''
            self.AnularOrdenGeneradaResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AnularOrdenGeneradaResult', pretty_print=pretty_print)
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
        if nodeName_ == 'AnularOrdenGeneradaResult':
            obj_ = AnularOrdenGeneradaResultType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AnularOrdenGeneradaResult = obj_
            obj_.original_tagname_ = 'AnularOrdenGeneradaResult'
# end class AnularOrdenGeneradaResponse


class GenerarConsolidacionDeOrdenesDeRetiro(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, usr=None, psw=None, ordenesDeRetiro=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.usr = usr
        self.usr_nsprefix_ = None
        self.psw = psw
        self.psw_nsprefix_ = None
        self.ordenesDeRetiro = ordenesDeRetiro
        self.ordenesDeRetiro_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GenerarConsolidacionDeOrdenesDeRetiro)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GenerarConsolidacionDeOrdenesDeRetiro.subclass:
            return GenerarConsolidacionDeOrdenesDeRetiro.subclass(*args_, **kwargs_)
        else:
            return GenerarConsolidacionDeOrdenesDeRetiro(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_usr(self):
        return self.usr
    def set_usr(self, usr):
        self.usr = usr
    def get_psw(self):
        return self.psw
    def set_psw(self, psw):
        self.psw = psw
    def get_ordenesDeRetiro(self):
        return self.ordenesDeRetiro
    def set_ordenesDeRetiro(self, ordenesDeRetiro):
        self.ordenesDeRetiro = ordenesDeRetiro
    def hasContent_(self):
        if (
            self.usr is not None or
            self.psw is not None or
            self.ordenesDeRetiro is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GenerarConsolidacionDeOrdenesDeRetiro', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GenerarConsolidacionDeOrdenesDeRetiro')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GenerarConsolidacionDeOrdenesDeRetiro':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GenerarConsolidacionDeOrdenesDeRetiro')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GenerarConsolidacionDeOrdenesDeRetiro', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GenerarConsolidacionDeOrdenesDeRetiro'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GenerarConsolidacionDeOrdenesDeRetiro', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.usr is not None:
            namespaceprefix_ = self.usr_nsprefix_ + ':' if (UseCapturedNS_ and self.usr_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%susr>%s</%susr>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.usr), input_name='usr')), namespaceprefix_ , eol_))
        if self.psw is not None:
            namespaceprefix_ = self.psw_nsprefix_ + ':' if (UseCapturedNS_ and self.psw_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spsw>%s</%spsw>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.psw), input_name='psw')), namespaceprefix_ , eol_))
        if self.ordenesDeRetiro is not None:
            namespaceprefix_ = self.ordenesDeRetiro_nsprefix_ + ':' if (UseCapturedNS_ and self.ordenesDeRetiro_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sordenesDeRetiro>%s</%sordenesDeRetiro>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ordenesDeRetiro), input_name='ordenesDeRetiro')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'usr':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'usr')
            value_ = self.gds_validate_string(value_, node, 'usr')
            self.usr = value_
            self.usr_nsprefix_ = child_.prefix
        elif nodeName_ == 'psw':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'psw')
            value_ = self.gds_validate_string(value_, node, 'psw')
            self.psw = value_
            self.psw_nsprefix_ = child_.prefix
        elif nodeName_ == 'ordenesDeRetiro':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ordenesDeRetiro')
            value_ = self.gds_validate_string(value_, node, 'ordenesDeRetiro')
            self.ordenesDeRetiro = value_
            self.ordenesDeRetiro_nsprefix_ = child_.prefix
# end class GenerarConsolidacionDeOrdenesDeRetiro


class GenerarConsolidacionDeOrdenesDeRetiroResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GenerarConsolidacionDeOrdenesDeRetiroResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GenerarConsolidacionDeOrdenesDeRetiroResult = GenerarConsolidacionDeOrdenesDeRetiroResult
        self.GenerarConsolidacionDeOrdenesDeRetiroResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GenerarConsolidacionDeOrdenesDeRetiroResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GenerarConsolidacionDeOrdenesDeRetiroResponse.subclass:
            return GenerarConsolidacionDeOrdenesDeRetiroResponse.subclass(*args_, **kwargs_)
        else:
            return GenerarConsolidacionDeOrdenesDeRetiroResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GenerarConsolidacionDeOrdenesDeRetiroResult(self):
        return self.GenerarConsolidacionDeOrdenesDeRetiroResult
    def set_GenerarConsolidacionDeOrdenesDeRetiroResult(self, GenerarConsolidacionDeOrdenesDeRetiroResult):
        self.GenerarConsolidacionDeOrdenesDeRetiroResult = GenerarConsolidacionDeOrdenesDeRetiroResult
    def hasContent_(self):
        if (
            self.GenerarConsolidacionDeOrdenesDeRetiroResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GenerarConsolidacionDeOrdenesDeRetiroResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GenerarConsolidacionDeOrdenesDeRetiroResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GenerarConsolidacionDeOrdenesDeRetiroResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GenerarConsolidacionDeOrdenesDeRetiroResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GenerarConsolidacionDeOrdenesDeRetiroResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GenerarConsolidacionDeOrdenesDeRetiroResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GenerarConsolidacionDeOrdenesDeRetiroResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GenerarConsolidacionDeOrdenesDeRetiroResult is not None:
            namespaceprefix_ = self.GenerarConsolidacionDeOrdenesDeRetiroResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GenerarConsolidacionDeOrdenesDeRetiroResult_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGenerarConsolidacionDeOrdenesDeRetiroResult>%s</%sGenerarConsolidacionDeOrdenesDeRetiroResult>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GenerarConsolidacionDeOrdenesDeRetiroResult), input_name='GenerarConsolidacionDeOrdenesDeRetiroResult')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'GenerarConsolidacionDeOrdenesDeRetiroResult':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GenerarConsolidacionDeOrdenesDeRetiroResult')
            value_ = self.gds_validate_string(value_, node, 'GenerarConsolidacionDeOrdenesDeRetiroResult')
            self.GenerarConsolidacionDeOrdenesDeRetiroResult = value_
            self.GenerarConsolidacionDeOrdenesDeRetiroResult_nsprefix_ = child_.prefix
# end class GenerarConsolidacionDeOrdenesDeRetiroResponse


class GetEnviosUltimoEstado(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, cuit=None, operativas=None, fechaDesde=None, fechaHasta=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.cuit = cuit
        self.cuit_nsprefix_ = None
        self.operativas = operativas
        self.operativas_nsprefix_ = None
        if isinstance(fechaDesde, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(fechaDesde, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = fechaDesde
        self.fechaDesde = initvalue_
        self.fechaDesde_nsprefix_ = None
        if isinstance(fechaHasta, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(fechaHasta, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = fechaHasta
        self.fechaHasta = initvalue_
        self.fechaHasta_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetEnviosUltimoEstado)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetEnviosUltimoEstado.subclass:
            return GetEnviosUltimoEstado.subclass(*args_, **kwargs_)
        else:
            return GetEnviosUltimoEstado(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_cuit(self):
        return self.cuit
    def set_cuit(self, cuit):
        self.cuit = cuit
    def get_operativas(self):
        return self.operativas
    def set_operativas(self, operativas):
        self.operativas = operativas
    def get_fechaDesde(self):
        return self.fechaDesde
    def set_fechaDesde(self, fechaDesde):
        self.fechaDesde = fechaDesde
    def get_fechaHasta(self):
        return self.fechaHasta
    def set_fechaHasta(self, fechaHasta):
        self.fechaHasta = fechaHasta
    def hasContent_(self):
        if (
            self.cuit is not None or
            self.operativas is not None or
            self.fechaDesde is not None or
            self.fechaHasta is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetEnviosUltimoEstado', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetEnviosUltimoEstado')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetEnviosUltimoEstado':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetEnviosUltimoEstado')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetEnviosUltimoEstado', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetEnviosUltimoEstado'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetEnviosUltimoEstado', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.cuit is not None:
            namespaceprefix_ = self.cuit_nsprefix_ + ':' if (UseCapturedNS_ and self.cuit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scuit>%s</%scuit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.cuit), input_name='cuit')), namespaceprefix_ , eol_))
        if self.operativas is not None:
            namespaceprefix_ = self.operativas_nsprefix_ + ':' if (UseCapturedNS_ and self.operativas_nsprefix_) else ''
            self.operativas.export(outfile, level, namespaceprefix_, namespacedef_='', name_='operativas', pretty_print=pretty_print)
        if self.fechaDesde is not None:
            namespaceprefix_ = self.fechaDesde_nsprefix_ + ':' if (UseCapturedNS_ and self.fechaDesde_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sfechaDesde>%s</%sfechaDesde>%s' % (namespaceprefix_ , self.gds_format_datetime(self.fechaDesde, input_name='fechaDesde'), namespaceprefix_ , eol_))
        if self.fechaHasta is not None:
            namespaceprefix_ = self.fechaHasta_nsprefix_ + ':' if (UseCapturedNS_ and self.fechaHasta_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sfechaHasta>%s</%sfechaHasta>%s' % (namespaceprefix_ , self.gds_format_datetime(self.fechaHasta, input_name='fechaHasta'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'cuit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'cuit')
            value_ = self.gds_validate_string(value_, node, 'cuit')
            self.cuit = value_
            self.cuit_nsprefix_ = child_.prefix
        elif nodeName_ == 'operativas':
            obj_ = ArrayOfString.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.operativas = obj_
            obj_.original_tagname_ = 'operativas'
        elif nodeName_ == 'fechaDesde':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.fechaDesde = dval_
            self.fechaDesde_nsprefix_ = child_.prefix
        elif nodeName_ == 'fechaHasta':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.fechaHasta = dval_
            self.fechaHasta_nsprefix_ = child_.prefix
# end class GetEnviosUltimoEstado


class ArrayOfString(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, string=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if string is None:
            self.string = []
        else:
            self.string = string
        self.string_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfString)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfString.subclass:
            return ArrayOfString.subclass(*args_, **kwargs_)
        else:
            return ArrayOfString(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_string(self):
        return self.string
    def set_string(self, string):
        self.string = string
    def add_string(self, value):
        self.string.append(value)
    def insert_string_at(self, index, value):
        self.string.insert(index, value)
    def replace_string_at(self, index, value):
        self.string[index] = value
    def hasContent_(self):
        if (
            self.string
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfString', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfString')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfString':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfString')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfString', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfString'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfString', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for string_ in self.string:
            namespaceprefix_ = self.string_nsprefix_ + ':' if (UseCapturedNS_ and self.string_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstring>%s</%sstring>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(string_), input_name='string')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'string':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'string')
            value_ = self.gds_validate_string(value_, node, 'string')
            self.string.append(value_)
            self.string_nsprefix_ = child_.prefix
# end class ArrayOfString


class GetEnviosUltimoEstadoResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetEnviosUltimoEstadoResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetEnviosUltimoEstadoResult = GetEnviosUltimoEstadoResult
        self.GetEnviosUltimoEstadoResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetEnviosUltimoEstadoResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetEnviosUltimoEstadoResponse.subclass:
            return GetEnviosUltimoEstadoResponse.subclass(*args_, **kwargs_)
        else:
            return GetEnviosUltimoEstadoResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetEnviosUltimoEstadoResult(self):
        return self.GetEnviosUltimoEstadoResult
    def set_GetEnviosUltimoEstadoResult(self, GetEnviosUltimoEstadoResult):
        self.GetEnviosUltimoEstadoResult = GetEnviosUltimoEstadoResult
    def hasContent_(self):
        if (
            self.GetEnviosUltimoEstadoResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetEnviosUltimoEstadoResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetEnviosUltimoEstadoResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetEnviosUltimoEstadoResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetEnviosUltimoEstadoResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetEnviosUltimoEstadoResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetEnviosUltimoEstadoResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetEnviosUltimoEstadoResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetEnviosUltimoEstadoResult is not None:
            namespaceprefix_ = self.GetEnviosUltimoEstadoResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetEnviosUltimoEstadoResult_nsprefix_) else ''
            self.GetEnviosUltimoEstadoResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetEnviosUltimoEstadoResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GetEnviosUltimoEstadoResult':
            obj_ = GetEnviosUltimoEstadoResultType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetEnviosUltimoEstadoResult = obj_
            obj_.original_tagname_ = 'GetEnviosUltimoEstadoResult'
# end class GetEnviosUltimoEstadoResponse


class GenerateQrByOrdenDeRetiro(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, usr=None, psw=None, idOrdenDeRetiro=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.usr = usr
        self.usr_nsprefix_ = None
        self.psw = psw
        self.psw_nsprefix_ = None
        self.idOrdenDeRetiro = idOrdenDeRetiro
        self.idOrdenDeRetiro_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GenerateQrByOrdenDeRetiro)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GenerateQrByOrdenDeRetiro.subclass:
            return GenerateQrByOrdenDeRetiro.subclass(*args_, **kwargs_)
        else:
            return GenerateQrByOrdenDeRetiro(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_usr(self):
        return self.usr
    def set_usr(self, usr):
        self.usr = usr
    def get_psw(self):
        return self.psw
    def set_psw(self, psw):
        self.psw = psw
    def get_idOrdenDeRetiro(self):
        return self.idOrdenDeRetiro
    def set_idOrdenDeRetiro(self, idOrdenDeRetiro):
        self.idOrdenDeRetiro = idOrdenDeRetiro
    def hasContent_(self):
        if (
            self.usr is not None or
            self.psw is not None or
            self.idOrdenDeRetiro is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GenerateQrByOrdenDeRetiro', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GenerateQrByOrdenDeRetiro')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GenerateQrByOrdenDeRetiro':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GenerateQrByOrdenDeRetiro')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GenerateQrByOrdenDeRetiro', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GenerateQrByOrdenDeRetiro'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GenerateQrByOrdenDeRetiro', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.usr is not None:
            namespaceprefix_ = self.usr_nsprefix_ + ':' if (UseCapturedNS_ and self.usr_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%susr>%s</%susr>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.usr), input_name='usr')), namespaceprefix_ , eol_))
        if self.psw is not None:
            namespaceprefix_ = self.psw_nsprefix_ + ':' if (UseCapturedNS_ and self.psw_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spsw>%s</%spsw>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.psw), input_name='psw')), namespaceprefix_ , eol_))
        if self.idOrdenDeRetiro is not None:
            namespaceprefix_ = self.idOrdenDeRetiro_nsprefix_ + ':' if (UseCapturedNS_ and self.idOrdenDeRetiro_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sidOrdenDeRetiro>%s</%sidOrdenDeRetiro>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.idOrdenDeRetiro), input_name='idOrdenDeRetiro')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'usr':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'usr')
            value_ = self.gds_validate_string(value_, node, 'usr')
            self.usr = value_
            self.usr_nsprefix_ = child_.prefix
        elif nodeName_ == 'psw':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'psw')
            value_ = self.gds_validate_string(value_, node, 'psw')
            self.psw = value_
            self.psw_nsprefix_ = child_.prefix
        elif nodeName_ == 'idOrdenDeRetiro':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'idOrdenDeRetiro')
            value_ = self.gds_validate_string(value_, node, 'idOrdenDeRetiro')
            self.idOrdenDeRetiro = value_
            self.idOrdenDeRetiro_nsprefix_ = child_.prefix
# end class GenerateQrByOrdenDeRetiro


class GenerateQrByOrdenDeRetiroResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GenerateQrByOrdenDeRetiroResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GenerateQrByOrdenDeRetiroResult = GenerateQrByOrdenDeRetiroResult
        self.GenerateQrByOrdenDeRetiroResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GenerateQrByOrdenDeRetiroResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GenerateQrByOrdenDeRetiroResponse.subclass:
            return GenerateQrByOrdenDeRetiroResponse.subclass(*args_, **kwargs_)
        else:
            return GenerateQrByOrdenDeRetiroResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GenerateQrByOrdenDeRetiroResult(self):
        return self.GenerateQrByOrdenDeRetiroResult
    def set_GenerateQrByOrdenDeRetiroResult(self, GenerateQrByOrdenDeRetiroResult):
        self.GenerateQrByOrdenDeRetiroResult = GenerateQrByOrdenDeRetiroResult
    def hasContent_(self):
        if (
            self.GenerateQrByOrdenDeRetiroResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GenerateQrByOrdenDeRetiroResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GenerateQrByOrdenDeRetiroResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GenerateQrByOrdenDeRetiroResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GenerateQrByOrdenDeRetiroResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GenerateQrByOrdenDeRetiroResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GenerateQrByOrdenDeRetiroResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GenerateQrByOrdenDeRetiroResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GenerateQrByOrdenDeRetiroResult is not None:
            namespaceprefix_ = self.GenerateQrByOrdenDeRetiroResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GenerateQrByOrdenDeRetiroResult_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGenerateQrByOrdenDeRetiroResult>%s</%sGenerateQrByOrdenDeRetiroResult>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GenerateQrByOrdenDeRetiroResult), input_name='GenerateQrByOrdenDeRetiroResult')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'GenerateQrByOrdenDeRetiroResult':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GenerateQrByOrdenDeRetiroResult')
            value_ = self.gds_validate_string(value_, node, 'GenerateQrByOrdenDeRetiroResult')
            self.GenerateQrByOrdenDeRetiroResult = value_
            self.GenerateQrByOrdenDeRetiroResult_nsprefix_ = child_.prefix
# end class GenerateQrByOrdenDeRetiroResponse


class GenerateQRParaPaquetes(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, usr=None, psw=None, numeroDeEnvio=None, idpaquete=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.usr = usr
        self.usr_nsprefix_ = None
        self.psw = psw
        self.psw_nsprefix_ = None
        self.numeroDeEnvio = numeroDeEnvio
        self.numeroDeEnvio_nsprefix_ = None
        self.idpaquete = idpaquete
        self.idpaquete_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GenerateQRParaPaquetes)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GenerateQRParaPaquetes.subclass:
            return GenerateQRParaPaquetes.subclass(*args_, **kwargs_)
        else:
            return GenerateQRParaPaquetes(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_usr(self):
        return self.usr
    def set_usr(self, usr):
        self.usr = usr
    def get_psw(self):
        return self.psw
    def set_psw(self, psw):
        self.psw = psw
    def get_numeroDeEnvio(self):
        return self.numeroDeEnvio
    def set_numeroDeEnvio(self, numeroDeEnvio):
        self.numeroDeEnvio = numeroDeEnvio
    def get_idpaquete(self):
        return self.idpaquete
    def set_idpaquete(self, idpaquete):
        self.idpaquete = idpaquete
    def hasContent_(self):
        if (
            self.usr is not None or
            self.psw is not None or
            self.numeroDeEnvio is not None or
            self.idpaquete is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GenerateQRParaPaquetes', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GenerateQRParaPaquetes')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GenerateQRParaPaquetes':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GenerateQRParaPaquetes')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GenerateQRParaPaquetes', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GenerateQRParaPaquetes'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GenerateQRParaPaquetes', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.usr is not None:
            namespaceprefix_ = self.usr_nsprefix_ + ':' if (UseCapturedNS_ and self.usr_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%susr>%s</%susr>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.usr), input_name='usr')), namespaceprefix_ , eol_))
        if self.psw is not None:
            namespaceprefix_ = self.psw_nsprefix_ + ':' if (UseCapturedNS_ and self.psw_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spsw>%s</%spsw>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.psw), input_name='psw')), namespaceprefix_ , eol_))
        if self.numeroDeEnvio is not None:
            namespaceprefix_ = self.numeroDeEnvio_nsprefix_ + ':' if (UseCapturedNS_ and self.numeroDeEnvio_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snumeroDeEnvio>%s</%snumeroDeEnvio>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.numeroDeEnvio), input_name='numeroDeEnvio')), namespaceprefix_ , eol_))
        if self.idpaquete is not None:
            namespaceprefix_ = self.idpaquete_nsprefix_ + ':' if (UseCapturedNS_ and self.idpaquete_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sidpaquete>%s</%sidpaquete>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.idpaquete), input_name='idpaquete')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'usr':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'usr')
            value_ = self.gds_validate_string(value_, node, 'usr')
            self.usr = value_
            self.usr_nsprefix_ = child_.prefix
        elif nodeName_ == 'psw':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'psw')
            value_ = self.gds_validate_string(value_, node, 'psw')
            self.psw = value_
            self.psw_nsprefix_ = child_.prefix
        elif nodeName_ == 'numeroDeEnvio':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'numeroDeEnvio')
            value_ = self.gds_validate_string(value_, node, 'numeroDeEnvio')
            self.numeroDeEnvio = value_
            self.numeroDeEnvio_nsprefix_ = child_.prefix
        elif nodeName_ == 'idpaquete':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'idpaquete')
            value_ = self.gds_validate_string(value_, node, 'idpaquete')
            self.idpaquete = value_
            self.idpaquete_nsprefix_ = child_.prefix
# end class GenerateQRParaPaquetes


class GenerateQRParaPaquetesResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GenerateQRParaPaquetesResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GenerateQRParaPaquetesResult = GenerateQRParaPaquetesResult
        self.GenerateQRParaPaquetesResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GenerateQRParaPaquetesResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GenerateQRParaPaquetesResponse.subclass:
            return GenerateQRParaPaquetesResponse.subclass(*args_, **kwargs_)
        else:
            return GenerateQRParaPaquetesResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GenerateQRParaPaquetesResult(self):
        return self.GenerateQRParaPaquetesResult
    def set_GenerateQRParaPaquetesResult(self, GenerateQRParaPaquetesResult):
        self.GenerateQRParaPaquetesResult = GenerateQRParaPaquetesResult
    def hasContent_(self):
        if (
            self.GenerateQRParaPaquetesResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GenerateQRParaPaquetesResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GenerateQRParaPaquetesResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GenerateQRParaPaquetesResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GenerateQRParaPaquetesResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GenerateQRParaPaquetesResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GenerateQRParaPaquetesResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GenerateQRParaPaquetesResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GenerateQRParaPaquetesResult is not None:
            namespaceprefix_ = self.GenerateQRParaPaquetesResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GenerateQRParaPaquetesResult_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGenerateQRParaPaquetesResult>%s</%sGenerateQRParaPaquetesResult>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GenerateQRParaPaquetesResult), input_name='GenerateQRParaPaquetesResult')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'GenerateQRParaPaquetesResult':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GenerateQRParaPaquetesResult')
            value_ = self.gds_validate_string(value_, node, 'GenerateQRParaPaquetesResult')
            self.GenerateQRParaPaquetesResult = value_
            self.GenerateQRParaPaquetesResult_nsprefix_ = child_.prefix
# end class GenerateQRParaPaquetesResponse


class GenerateListQrPorEnvio(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, usr=None, psw=None, numeroDeEnvio=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.usr = usr
        self.usr_nsprefix_ = None
        self.psw = psw
        self.psw_nsprefix_ = None
        self.numeroDeEnvio = numeroDeEnvio
        self.numeroDeEnvio_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GenerateListQrPorEnvio)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GenerateListQrPorEnvio.subclass:
            return GenerateListQrPorEnvio.subclass(*args_, **kwargs_)
        else:
            return GenerateListQrPorEnvio(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_usr(self):
        return self.usr
    def set_usr(self, usr):
        self.usr = usr
    def get_psw(self):
        return self.psw
    def set_psw(self, psw):
        self.psw = psw
    def get_numeroDeEnvio(self):
        return self.numeroDeEnvio
    def set_numeroDeEnvio(self, numeroDeEnvio):
        self.numeroDeEnvio = numeroDeEnvio
    def hasContent_(self):
        if (
            self.usr is not None or
            self.psw is not None or
            self.numeroDeEnvio is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GenerateListQrPorEnvio', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GenerateListQrPorEnvio')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GenerateListQrPorEnvio':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GenerateListQrPorEnvio')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GenerateListQrPorEnvio', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GenerateListQrPorEnvio'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GenerateListQrPorEnvio', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.usr is not None:
            namespaceprefix_ = self.usr_nsprefix_ + ':' if (UseCapturedNS_ and self.usr_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%susr>%s</%susr>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.usr), input_name='usr')), namespaceprefix_ , eol_))
        if self.psw is not None:
            namespaceprefix_ = self.psw_nsprefix_ + ':' if (UseCapturedNS_ and self.psw_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spsw>%s</%spsw>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.psw), input_name='psw')), namespaceprefix_ , eol_))
        if self.numeroDeEnvio is not None:
            namespaceprefix_ = self.numeroDeEnvio_nsprefix_ + ':' if (UseCapturedNS_ and self.numeroDeEnvio_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snumeroDeEnvio>%s</%snumeroDeEnvio>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.numeroDeEnvio), input_name='numeroDeEnvio')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'usr':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'usr')
            value_ = self.gds_validate_string(value_, node, 'usr')
            self.usr = value_
            self.usr_nsprefix_ = child_.prefix
        elif nodeName_ == 'psw':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'psw')
            value_ = self.gds_validate_string(value_, node, 'psw')
            self.psw = value_
            self.psw_nsprefix_ = child_.prefix
        elif nodeName_ == 'numeroDeEnvio':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'numeroDeEnvio')
            value_ = self.gds_validate_string(value_, node, 'numeroDeEnvio')
            self.numeroDeEnvio = value_
            self.numeroDeEnvio_nsprefix_ = child_.prefix
# end class GenerateListQrPorEnvio


class GenerateListQrPorEnvioResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GenerateListQrPorEnvioResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GenerateListQrPorEnvioResult = GenerateListQrPorEnvioResult
        self.GenerateListQrPorEnvioResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GenerateListQrPorEnvioResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GenerateListQrPorEnvioResponse.subclass:
            return GenerateListQrPorEnvioResponse.subclass(*args_, **kwargs_)
        else:
            return GenerateListQrPorEnvioResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GenerateListQrPorEnvioResult(self):
        return self.GenerateListQrPorEnvioResult
    def set_GenerateListQrPorEnvioResult(self, GenerateListQrPorEnvioResult):
        self.GenerateListQrPorEnvioResult = GenerateListQrPorEnvioResult
    def hasContent_(self):
        if (
            self.GenerateListQrPorEnvioResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GenerateListQrPorEnvioResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GenerateListQrPorEnvioResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GenerateListQrPorEnvioResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GenerateListQrPorEnvioResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GenerateListQrPorEnvioResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GenerateListQrPorEnvioResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GenerateListQrPorEnvioResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GenerateListQrPorEnvioResult is not None:
            namespaceprefix_ = self.GenerateListQrPorEnvioResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GenerateListQrPorEnvioResult_nsprefix_) else ''
            self.GenerateListQrPorEnvioResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GenerateListQrPorEnvioResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GenerateListQrPorEnvioResult':
            obj_ = ArrayOfString.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GenerateListQrPorEnvioResult = obj_
            obj_.original_tagname_ = 'GenerateListQrPorEnvioResult'
# end class GenerateListQrPorEnvioResponse


class IngresoOR(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, usr=None, psw=None, XML_Retiro=None, ConfirmarRetiro=None, DiasRetiro=None, FranjaHoraria=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.usr = usr
        self.usr_nsprefix_ = None
        self.psw = psw
        self.psw_nsprefix_ = None
        self.XML_Retiro = XML_Retiro
        self.XML_Retiro_nsprefix_ = None
        self.ConfirmarRetiro = ConfirmarRetiro
        self.ConfirmarRetiro_nsprefix_ = None
        self.DiasRetiro = DiasRetiro
        self.DiasRetiro_nsprefix_ = None
        self.FranjaHoraria = FranjaHoraria
        self.FranjaHoraria_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, IngresoOR)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if IngresoOR.subclass:
            return IngresoOR.subclass(*args_, **kwargs_)
        else:
            return IngresoOR(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_usr(self):
        return self.usr
    def set_usr(self, usr):
        self.usr = usr
    def get_psw(self):
        return self.psw
    def set_psw(self, psw):
        self.psw = psw
    def get_XML_Retiro(self):
        return self.XML_Retiro
    def set_XML_Retiro(self, XML_Retiro):
        self.XML_Retiro = XML_Retiro
    def get_ConfirmarRetiro(self):
        return self.ConfirmarRetiro
    def set_ConfirmarRetiro(self, ConfirmarRetiro):
        self.ConfirmarRetiro = ConfirmarRetiro
    def get_DiasRetiro(self):
        return self.DiasRetiro
    def set_DiasRetiro(self, DiasRetiro):
        self.DiasRetiro = DiasRetiro
    def get_FranjaHoraria(self):
        return self.FranjaHoraria
    def set_FranjaHoraria(self, FranjaHoraria):
        self.FranjaHoraria = FranjaHoraria
    def hasContent_(self):
        if (
            self.usr is not None or
            self.psw is not None or
            self.XML_Retiro is not None or
            self.ConfirmarRetiro is not None or
            self.DiasRetiro is not None or
            self.FranjaHoraria is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='IngresoOR', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('IngresoOR')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'IngresoOR':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='IngresoOR')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='IngresoOR', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='IngresoOR'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='IngresoOR', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.usr is not None:
            namespaceprefix_ = self.usr_nsprefix_ + ':' if (UseCapturedNS_ and self.usr_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%susr>%s</%susr>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.usr), input_name='usr')), namespaceprefix_ , eol_))
        if self.psw is not None:
            namespaceprefix_ = self.psw_nsprefix_ + ':' if (UseCapturedNS_ and self.psw_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spsw>%s</%spsw>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.psw), input_name='psw')), namespaceprefix_ , eol_))
        if self.XML_Retiro is not None:
            namespaceprefix_ = self.XML_Retiro_nsprefix_ + ':' if (UseCapturedNS_ and self.XML_Retiro_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sXML_Retiro>%s</%sXML_Retiro>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.XML_Retiro), input_name='XML_Retiro')), namespaceprefix_ , eol_))
        if self.ConfirmarRetiro is not None:
            namespaceprefix_ = self.ConfirmarRetiro_nsprefix_ + ':' if (UseCapturedNS_ and self.ConfirmarRetiro_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sConfirmarRetiro>%s</%sConfirmarRetiro>%s' % (namespaceprefix_ , self.gds_format_boolean(self.ConfirmarRetiro, input_name='ConfirmarRetiro'), namespaceprefix_ , eol_))
        if self.DiasRetiro is not None:
            namespaceprefix_ = self.DiasRetiro_nsprefix_ + ':' if (UseCapturedNS_ and self.DiasRetiro_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDiasRetiro>%s</%sDiasRetiro>%s' % (namespaceprefix_ , self.gds_format_integer(self.DiasRetiro, input_name='DiasRetiro'), namespaceprefix_ , eol_))
        if self.FranjaHoraria is not None:
            namespaceprefix_ = self.FranjaHoraria_nsprefix_ + ':' if (UseCapturedNS_ and self.FranjaHoraria_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFranjaHoraria>%s</%sFranjaHoraria>%s' % (namespaceprefix_ , self.gds_format_integer(self.FranjaHoraria, input_name='FranjaHoraria'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'usr':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'usr')
            value_ = self.gds_validate_string(value_, node, 'usr')
            self.usr = value_
            self.usr_nsprefix_ = child_.prefix
        elif nodeName_ == 'psw':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'psw')
            value_ = self.gds_validate_string(value_, node, 'psw')
            self.psw = value_
            self.psw_nsprefix_ = child_.prefix
        elif nodeName_ == 'XML_Retiro':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'XML_Retiro')
            value_ = self.gds_validate_string(value_, node, 'XML_Retiro')
            self.XML_Retiro = value_
            self.XML_Retiro_nsprefix_ = child_.prefix
        elif nodeName_ == 'ConfirmarRetiro':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'ConfirmarRetiro')
            ival_ = self.gds_validate_boolean(ival_, node, 'ConfirmarRetiro')
            self.ConfirmarRetiro = ival_
            self.ConfirmarRetiro_nsprefix_ = child_.prefix
        elif nodeName_ == 'DiasRetiro' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'DiasRetiro')
            ival_ = self.gds_validate_integer(ival_, node, 'DiasRetiro')
            self.DiasRetiro = ival_
            self.DiasRetiro_nsprefix_ = child_.prefix
        elif nodeName_ == 'FranjaHoraria' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'FranjaHoraria')
            ival_ = self.gds_validate_integer(ival_, node, 'FranjaHoraria')
            self.FranjaHoraria = ival_
            self.FranjaHoraria_nsprefix_ = child_.prefix
# end class IngresoOR


class IngresoORResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, IngresoORResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.IngresoORResult = IngresoORResult
        self.IngresoORResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, IngresoORResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if IngresoORResponse.subclass:
            return IngresoORResponse.subclass(*args_, **kwargs_)
        else:
            return IngresoORResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_IngresoORResult(self):
        return self.IngresoORResult
    def set_IngresoORResult(self, IngresoORResult):
        self.IngresoORResult = IngresoORResult
    def hasContent_(self):
        if (
            self.IngresoORResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='IngresoORResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('IngresoORResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'IngresoORResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='IngresoORResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='IngresoORResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='IngresoORResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='IngresoORResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.IngresoORResult is not None:
            namespaceprefix_ = self.IngresoORResult_nsprefix_ + ':' if (UseCapturedNS_ and self.IngresoORResult_nsprefix_) else ''
            self.IngresoORResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='IngresoORResult', pretty_print=pretty_print)
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
        if nodeName_ == 'IngresoORResult':
            obj_ = IngresoORResultType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.IngresoORResult = obj_
            obj_.original_tagname_ = 'IngresoORResult'
# end class IngresoORResponse


class GetCentroCostoPorOperativa(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CUIT=None, Operativa=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CUIT = CUIT
        self.CUIT_nsprefix_ = None
        self.Operativa = Operativa
        self.Operativa_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetCentroCostoPorOperativa)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetCentroCostoPorOperativa.subclass:
            return GetCentroCostoPorOperativa.subclass(*args_, **kwargs_)
        else:
            return GetCentroCostoPorOperativa(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CUIT(self):
        return self.CUIT
    def set_CUIT(self, CUIT):
        self.CUIT = CUIT
    def get_Operativa(self):
        return self.Operativa
    def set_Operativa(self, Operativa):
        self.Operativa = Operativa
    def hasContent_(self):
        if (
            self.CUIT is not None or
            self.Operativa is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentroCostoPorOperativa', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetCentroCostoPorOperativa')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetCentroCostoPorOperativa':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetCentroCostoPorOperativa')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetCentroCostoPorOperativa', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetCentroCostoPorOperativa'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentroCostoPorOperativa', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CUIT is not None:
            namespaceprefix_ = self.CUIT_nsprefix_ + ':' if (UseCapturedNS_ and self.CUIT_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCUIT>%s</%sCUIT>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CUIT), input_name='CUIT')), namespaceprefix_ , eol_))
        if self.Operativa is not None:
            namespaceprefix_ = self.Operativa_nsprefix_ + ':' if (UseCapturedNS_ and self.Operativa_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOperativa>%s</%sOperativa>%s' % (namespaceprefix_ , self.gds_format_integer(self.Operativa, input_name='Operativa'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'CUIT':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CUIT')
            value_ = self.gds_validate_string(value_, node, 'CUIT')
            self.CUIT = value_
            self.CUIT_nsprefix_ = child_.prefix
        elif nodeName_ == 'Operativa' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Operativa')
            ival_ = self.gds_validate_integer(ival_, node, 'Operativa')
            self.Operativa = ival_
            self.Operativa_nsprefix_ = child_.prefix
# end class GetCentroCostoPorOperativa


class GetCentroCostoPorOperativaResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetCentroCostoPorOperativaResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetCentroCostoPorOperativaResult = GetCentroCostoPorOperativaResult
        self.GetCentroCostoPorOperativaResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetCentroCostoPorOperativaResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetCentroCostoPorOperativaResponse.subclass:
            return GetCentroCostoPorOperativaResponse.subclass(*args_, **kwargs_)
        else:
            return GetCentroCostoPorOperativaResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetCentroCostoPorOperativaResult(self):
        return self.GetCentroCostoPorOperativaResult
    def set_GetCentroCostoPorOperativaResult(self, GetCentroCostoPorOperativaResult):
        self.GetCentroCostoPorOperativaResult = GetCentroCostoPorOperativaResult
    def hasContent_(self):
        if (
            self.GetCentroCostoPorOperativaResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentroCostoPorOperativaResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetCentroCostoPorOperativaResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetCentroCostoPorOperativaResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetCentroCostoPorOperativaResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetCentroCostoPorOperativaResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetCentroCostoPorOperativaResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentroCostoPorOperativaResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetCentroCostoPorOperativaResult is not None:
            namespaceprefix_ = self.GetCentroCostoPorOperativaResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetCentroCostoPorOperativaResult_nsprefix_) else ''
            self.GetCentroCostoPorOperativaResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetCentroCostoPorOperativaResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GetCentroCostoPorOperativaResult':
            obj_ = GetCentroCostoPorOperativaResultType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetCentroCostoPorOperativaResult = obj_
            obj_.original_tagname_ = 'GetCentroCostoPorOperativaResult'
# end class GetCentroCostoPorOperativaResponse


class GetCentrosImposicion(GeneratedsSuper):
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
                CurrentSubclassModule_, GetCentrosImposicion)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetCentrosImposicion.subclass:
            return GetCentrosImposicion.subclass(*args_, **kwargs_)
        else:
            return GetCentrosImposicion(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicion', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetCentrosImposicion')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetCentrosImposicion':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetCentrosImposicion')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetCentrosImposicion', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetCentrosImposicion'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicion', fromsubclass_=False, pretty_print=True):
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
# end class GetCentrosImposicion


class GetCentrosImposicionResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetCentrosImposicionResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetCentrosImposicionResult = GetCentrosImposicionResult
        self.GetCentrosImposicionResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetCentrosImposicionResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetCentrosImposicionResponse.subclass:
            return GetCentrosImposicionResponse.subclass(*args_, **kwargs_)
        else:
            return GetCentrosImposicionResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetCentrosImposicionResult(self):
        return self.GetCentrosImposicionResult
    def set_GetCentrosImposicionResult(self, GetCentrosImposicionResult):
        self.GetCentrosImposicionResult = GetCentrosImposicionResult
    def hasContent_(self):
        if (
            self.GetCentrosImposicionResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetCentrosImposicionResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetCentrosImposicionResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetCentrosImposicionResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetCentrosImposicionResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetCentrosImposicionResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetCentrosImposicionResult is not None:
            namespaceprefix_ = self.GetCentrosImposicionResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetCentrosImposicionResult_nsprefix_) else ''
            self.GetCentrosImposicionResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetCentrosImposicionResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GetCentrosImposicionResult':
            obj_ = GetCentrosImposicionResultType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetCentrosImposicionResult = obj_
            obj_.original_tagname_ = 'GetCentrosImposicionResult'
# end class GetCentrosImposicionResponse


class GetELockerOCA(GeneratedsSuper):
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
                CurrentSubclassModule_, GetELockerOCA)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetELockerOCA.subclass:
            return GetELockerOCA.subclass(*args_, **kwargs_)
        else:
            return GetELockerOCA(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetELockerOCA', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetELockerOCA')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetELockerOCA':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetELockerOCA')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetELockerOCA', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetELockerOCA'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetELockerOCA', fromsubclass_=False, pretty_print=True):
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
# end class GetELockerOCA


class GetELockerOCAResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetELockerOCAResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetELockerOCAResult = GetELockerOCAResult
        self.GetELockerOCAResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetELockerOCAResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetELockerOCAResponse.subclass:
            return GetELockerOCAResponse.subclass(*args_, **kwargs_)
        else:
            return GetELockerOCAResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetELockerOCAResult(self):
        return self.GetELockerOCAResult
    def set_GetELockerOCAResult(self, GetELockerOCAResult):
        self.GetELockerOCAResult = GetELockerOCAResult
    def hasContent_(self):
        if (
            self.GetELockerOCAResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetELockerOCAResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetELockerOCAResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetELockerOCAResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetELockerOCAResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetELockerOCAResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetELockerOCAResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetELockerOCAResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetELockerOCAResult is not None:
            namespaceprefix_ = self.GetELockerOCAResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetELockerOCAResult_nsprefix_) else ''
            self.GetELockerOCAResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetELockerOCAResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GetELockerOCAResult':
            obj_ = GetELockerOCAResultType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetELockerOCAResult = obj_
            obj_.original_tagname_ = 'GetELockerOCAResult'
# end class GetELockerOCAResponse


class GetCentrosImposicionAdmision(GeneratedsSuper):
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
                CurrentSubclassModule_, GetCentrosImposicionAdmision)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetCentrosImposicionAdmision.subclass:
            return GetCentrosImposicionAdmision.subclass(*args_, **kwargs_)
        else:
            return GetCentrosImposicionAdmision(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionAdmision', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetCentrosImposicionAdmision')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetCentrosImposicionAdmision':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetCentrosImposicionAdmision')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetCentrosImposicionAdmision', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetCentrosImposicionAdmision'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionAdmision', fromsubclass_=False, pretty_print=True):
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
# end class GetCentrosImposicionAdmision


class GetCentrosImposicionAdmisionResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetCentrosImposicionAdmisionResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetCentrosImposicionAdmisionResult = GetCentrosImposicionAdmisionResult
        self.GetCentrosImposicionAdmisionResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetCentrosImposicionAdmisionResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetCentrosImposicionAdmisionResponse.subclass:
            return GetCentrosImposicionAdmisionResponse.subclass(*args_, **kwargs_)
        else:
            return GetCentrosImposicionAdmisionResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetCentrosImposicionAdmisionResult(self):
        return self.GetCentrosImposicionAdmisionResult
    def set_GetCentrosImposicionAdmisionResult(self, GetCentrosImposicionAdmisionResult):
        self.GetCentrosImposicionAdmisionResult = GetCentrosImposicionAdmisionResult
    def hasContent_(self):
        if (
            self.GetCentrosImposicionAdmisionResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionAdmisionResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetCentrosImposicionAdmisionResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetCentrosImposicionAdmisionResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetCentrosImposicionAdmisionResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetCentrosImposicionAdmisionResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetCentrosImposicionAdmisionResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionAdmisionResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetCentrosImposicionAdmisionResult is not None:
            namespaceprefix_ = self.GetCentrosImposicionAdmisionResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetCentrosImposicionAdmisionResult_nsprefix_) else ''
            self.GetCentrosImposicionAdmisionResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetCentrosImposicionAdmisionResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GetCentrosImposicionAdmisionResult':
            obj_ = GetCentrosImposicionAdmisionResultType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetCentrosImposicionAdmisionResult = obj_
            obj_.original_tagname_ = 'GetCentrosImposicionAdmisionResult'
# end class GetCentrosImposicionAdmisionResponse


class GetServiciosDeCentrosImposicion(GeneratedsSuper):
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
                CurrentSubclassModule_, GetServiciosDeCentrosImposicion)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetServiciosDeCentrosImposicion.subclass:
            return GetServiciosDeCentrosImposicion.subclass(*args_, **kwargs_)
        else:
            return GetServiciosDeCentrosImposicion(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetServiciosDeCentrosImposicion', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetServiciosDeCentrosImposicion')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetServiciosDeCentrosImposicion':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetServiciosDeCentrosImposicion')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetServiciosDeCentrosImposicion', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetServiciosDeCentrosImposicion'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetServiciosDeCentrosImposicion', fromsubclass_=False, pretty_print=True):
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
# end class GetServiciosDeCentrosImposicion


class GetServiciosDeCentrosImposicionResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetServiciosDeCentrosImposicionResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetServiciosDeCentrosImposicionResult = GetServiciosDeCentrosImposicionResult
        self.GetServiciosDeCentrosImposicionResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetServiciosDeCentrosImposicionResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetServiciosDeCentrosImposicionResponse.subclass:
            return GetServiciosDeCentrosImposicionResponse.subclass(*args_, **kwargs_)
        else:
            return GetServiciosDeCentrosImposicionResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetServiciosDeCentrosImposicionResult(self):
        return self.GetServiciosDeCentrosImposicionResult
    def set_GetServiciosDeCentrosImposicionResult(self, GetServiciosDeCentrosImposicionResult):
        self.GetServiciosDeCentrosImposicionResult = GetServiciosDeCentrosImposicionResult
    def hasContent_(self):
        if (
            self.GetServiciosDeCentrosImposicionResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetServiciosDeCentrosImposicionResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetServiciosDeCentrosImposicionResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetServiciosDeCentrosImposicionResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetServiciosDeCentrosImposicionResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetServiciosDeCentrosImposicionResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetServiciosDeCentrosImposicionResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetServiciosDeCentrosImposicionResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetServiciosDeCentrosImposicionResult is not None:
            namespaceprefix_ = self.GetServiciosDeCentrosImposicionResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetServiciosDeCentrosImposicionResult_nsprefix_) else ''
            self.GetServiciosDeCentrosImposicionResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetServiciosDeCentrosImposicionResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GetServiciosDeCentrosImposicionResult':
            obj_ = GetServiciosDeCentrosImposicionResultType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetServiciosDeCentrosImposicionResult = obj_
            obj_.original_tagname_ = 'GetServiciosDeCentrosImposicionResult'
# end class GetServiciosDeCentrosImposicionResponse


class TrackingEnvio_EstadoActual(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, numeroEnvio=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.numeroEnvio = numeroEnvio
        self.numeroEnvio_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TrackingEnvio_EstadoActual)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TrackingEnvio_EstadoActual.subclass:
            return TrackingEnvio_EstadoActual.subclass(*args_, **kwargs_)
        else:
            return TrackingEnvio_EstadoActual(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_numeroEnvio(self):
        return self.numeroEnvio
    def set_numeroEnvio(self, numeroEnvio):
        self.numeroEnvio = numeroEnvio
    def hasContent_(self):
        if (
            self.numeroEnvio is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackingEnvio_EstadoActual', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TrackingEnvio_EstadoActual')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TrackingEnvio_EstadoActual':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TrackingEnvio_EstadoActual')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TrackingEnvio_EstadoActual', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TrackingEnvio_EstadoActual'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackingEnvio_EstadoActual', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.numeroEnvio is not None:
            namespaceprefix_ = self.numeroEnvio_nsprefix_ + ':' if (UseCapturedNS_ and self.numeroEnvio_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snumeroEnvio>%s</%snumeroEnvio>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.numeroEnvio), input_name='numeroEnvio')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'numeroEnvio':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'numeroEnvio')
            value_ = self.gds_validate_string(value_, node, 'numeroEnvio')
            self.numeroEnvio = value_
            self.numeroEnvio_nsprefix_ = child_.prefix
# end class TrackingEnvio_EstadoActual


class TrackingEnvio_EstadoActualResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TrackingEnvio_EstadoActualResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.TrackingEnvio_EstadoActualResult = TrackingEnvio_EstadoActualResult
        self.TrackingEnvio_EstadoActualResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TrackingEnvio_EstadoActualResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TrackingEnvio_EstadoActualResponse.subclass:
            return TrackingEnvio_EstadoActualResponse.subclass(*args_, **kwargs_)
        else:
            return TrackingEnvio_EstadoActualResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_TrackingEnvio_EstadoActualResult(self):
        return self.TrackingEnvio_EstadoActualResult
    def set_TrackingEnvio_EstadoActualResult(self, TrackingEnvio_EstadoActualResult):
        self.TrackingEnvio_EstadoActualResult = TrackingEnvio_EstadoActualResult
    def hasContent_(self):
        if (
            self.TrackingEnvio_EstadoActualResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackingEnvio_EstadoActualResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TrackingEnvio_EstadoActualResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TrackingEnvio_EstadoActualResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TrackingEnvio_EstadoActualResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TrackingEnvio_EstadoActualResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TrackingEnvio_EstadoActualResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackingEnvio_EstadoActualResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.TrackingEnvio_EstadoActualResult is not None:
            namespaceprefix_ = self.TrackingEnvio_EstadoActualResult_nsprefix_ + ':' if (UseCapturedNS_ and self.TrackingEnvio_EstadoActualResult_nsprefix_) else ''
            self.TrackingEnvio_EstadoActualResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TrackingEnvio_EstadoActualResult', pretty_print=pretty_print)
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
        if nodeName_ == 'TrackingEnvio_EstadoActualResult':
            obj_ = TrackingEnvio_EstadoActualResultType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TrackingEnvio_EstadoActualResult = obj_
            obj_.original_tagname_ = 'TrackingEnvio_EstadoActualResult'
# end class TrackingEnvio_EstadoActualResponse


class GetProvincias(GeneratedsSuper):
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
                CurrentSubclassModule_, GetProvincias)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetProvincias.subclass:
            return GetProvincias.subclass(*args_, **kwargs_)
        else:
            return GetProvincias(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetProvincias', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetProvincias')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetProvincias':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetProvincias')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetProvincias', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetProvincias'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetProvincias', fromsubclass_=False, pretty_print=True):
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
# end class GetProvincias


class GetProvinciasResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetProvinciasResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetProvinciasResult = GetProvinciasResult
        self.GetProvinciasResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetProvinciasResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetProvinciasResponse.subclass:
            return GetProvinciasResponse.subclass(*args_, **kwargs_)
        else:
            return GetProvinciasResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetProvinciasResult(self):
        return self.GetProvinciasResult
    def set_GetProvinciasResult(self, GetProvinciasResult):
        self.GetProvinciasResult = GetProvinciasResult
    def hasContent_(self):
        if (
            self.GetProvinciasResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetProvinciasResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetProvinciasResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetProvinciasResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetProvinciasResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetProvinciasResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetProvinciasResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetProvinciasResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetProvinciasResult is not None:
            namespaceprefix_ = self.GetProvinciasResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetProvinciasResult_nsprefix_) else ''
            self.GetProvinciasResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetProvinciasResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GetProvinciasResult':
            obj_ = GetProvinciasResultType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetProvinciasResult = obj_
            obj_.original_tagname_ = 'GetProvinciasResult'
# end class GetProvinciasResponse


class GetLocalidadesByProvincia(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, idProvincia=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.idProvincia = idProvincia
        self.idProvincia_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetLocalidadesByProvincia)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetLocalidadesByProvincia.subclass:
            return GetLocalidadesByProvincia.subclass(*args_, **kwargs_)
        else:
            return GetLocalidadesByProvincia(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_idProvincia(self):
        return self.idProvincia
    def set_idProvincia(self, idProvincia):
        self.idProvincia = idProvincia
    def hasContent_(self):
        if (
            self.idProvincia is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLocalidadesByProvincia', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetLocalidadesByProvincia')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetLocalidadesByProvincia':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetLocalidadesByProvincia')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetLocalidadesByProvincia', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetLocalidadesByProvincia'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLocalidadesByProvincia', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.idProvincia is not None:
            namespaceprefix_ = self.idProvincia_nsprefix_ + ':' if (UseCapturedNS_ and self.idProvincia_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sidProvincia>%s</%sidProvincia>%s' % (namespaceprefix_ , self.gds_format_integer(self.idProvincia, input_name='idProvincia'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'idProvincia' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'idProvincia')
            ival_ = self.gds_validate_integer(ival_, node, 'idProvincia')
            self.idProvincia = ival_
            self.idProvincia_nsprefix_ = child_.prefix
# end class GetLocalidadesByProvincia


class GetLocalidadesByProvinciaResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetLocalidadesByProvinciaResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetLocalidadesByProvinciaResult = GetLocalidadesByProvinciaResult
        self.GetLocalidadesByProvinciaResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetLocalidadesByProvinciaResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetLocalidadesByProvinciaResponse.subclass:
            return GetLocalidadesByProvinciaResponse.subclass(*args_, **kwargs_)
        else:
            return GetLocalidadesByProvinciaResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetLocalidadesByProvinciaResult(self):
        return self.GetLocalidadesByProvinciaResult
    def set_GetLocalidadesByProvinciaResult(self, GetLocalidadesByProvinciaResult):
        self.GetLocalidadesByProvinciaResult = GetLocalidadesByProvinciaResult
    def hasContent_(self):
        if (
            self.GetLocalidadesByProvinciaResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLocalidadesByProvinciaResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetLocalidadesByProvinciaResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetLocalidadesByProvinciaResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetLocalidadesByProvinciaResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetLocalidadesByProvinciaResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetLocalidadesByProvinciaResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLocalidadesByProvinciaResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetLocalidadesByProvinciaResult is not None:
            namespaceprefix_ = self.GetLocalidadesByProvinciaResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetLocalidadesByProvinciaResult_nsprefix_) else ''
            self.GetLocalidadesByProvinciaResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetLocalidadesByProvinciaResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GetLocalidadesByProvinciaResult':
            obj_ = GetLocalidadesByProvinciaResultType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetLocalidadesByProvinciaResult = obj_
            obj_.original_tagname_ = 'GetLocalidadesByProvinciaResult'
# end class GetLocalidadesByProvinciaResponse


class GetServiciosDeCentrosImposicion_xProvincia(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, provinciaID=None, localidad=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.provinciaID = provinciaID
        self.provinciaID_nsprefix_ = None
        self.localidad = localidad
        self.localidad_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetServiciosDeCentrosImposicion_xProvincia)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetServiciosDeCentrosImposicion_xProvincia.subclass:
            return GetServiciosDeCentrosImposicion_xProvincia.subclass(*args_, **kwargs_)
        else:
            return GetServiciosDeCentrosImposicion_xProvincia(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_provinciaID(self):
        return self.provinciaID
    def set_provinciaID(self, provinciaID):
        self.provinciaID = provinciaID
    def get_localidad(self):
        return self.localidad
    def set_localidad(self, localidad):
        self.localidad = localidad
    def hasContent_(self):
        if (
            self.provinciaID is not None or
            self.localidad is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetServiciosDeCentrosImposicion_xProvincia', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetServiciosDeCentrosImposicion_xProvincia')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetServiciosDeCentrosImposicion_xProvincia':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetServiciosDeCentrosImposicion_xProvincia')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetServiciosDeCentrosImposicion_xProvincia', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetServiciosDeCentrosImposicion_xProvincia'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetServiciosDeCentrosImposicion_xProvincia', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.provinciaID is not None:
            namespaceprefix_ = self.provinciaID_nsprefix_ + ':' if (UseCapturedNS_ and self.provinciaID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sprovinciaID>%s</%sprovinciaID>%s' % (namespaceprefix_ , self.gds_format_integer(self.provinciaID, input_name='provinciaID'), namespaceprefix_ , eol_))
        if self.localidad is not None:
            namespaceprefix_ = self.localidad_nsprefix_ + ':' if (UseCapturedNS_ and self.localidad_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slocalidad>%s</%slocalidad>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.localidad), input_name='localidad')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'provinciaID' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'provinciaID')
            ival_ = self.gds_validate_integer(ival_, node, 'provinciaID')
            self.provinciaID = ival_
            self.provinciaID_nsprefix_ = child_.prefix
        elif nodeName_ == 'localidad':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'localidad')
            value_ = self.gds_validate_string(value_, node, 'localidad')
            self.localidad = value_
            self.localidad_nsprefix_ = child_.prefix
# end class GetServiciosDeCentrosImposicion_xProvincia


class GetServiciosDeCentrosImposicion_xProvinciaResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetServiciosDeCentrosImposicion_xProvinciaResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetServiciosDeCentrosImposicion_xProvinciaResult = GetServiciosDeCentrosImposicion_xProvinciaResult
        self.GetServiciosDeCentrosImposicion_xProvinciaResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetServiciosDeCentrosImposicion_xProvinciaResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetServiciosDeCentrosImposicion_xProvinciaResponse.subclass:
            return GetServiciosDeCentrosImposicion_xProvinciaResponse.subclass(*args_, **kwargs_)
        else:
            return GetServiciosDeCentrosImposicion_xProvinciaResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetServiciosDeCentrosImposicion_xProvinciaResult(self):
        return self.GetServiciosDeCentrosImposicion_xProvinciaResult
    def set_GetServiciosDeCentrosImposicion_xProvinciaResult(self, GetServiciosDeCentrosImposicion_xProvinciaResult):
        self.GetServiciosDeCentrosImposicion_xProvinciaResult = GetServiciosDeCentrosImposicion_xProvinciaResult
    def hasContent_(self):
        if (
            self.GetServiciosDeCentrosImposicion_xProvinciaResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetServiciosDeCentrosImposicion_xProvinciaResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetServiciosDeCentrosImposicion_xProvinciaResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetServiciosDeCentrosImposicion_xProvinciaResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetServiciosDeCentrosImposicion_xProvinciaResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetServiciosDeCentrosImposicion_xProvinciaResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetServiciosDeCentrosImposicion_xProvinciaResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetServiciosDeCentrosImposicion_xProvinciaResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetServiciosDeCentrosImposicion_xProvinciaResult is not None:
            namespaceprefix_ = self.GetServiciosDeCentrosImposicion_xProvinciaResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetServiciosDeCentrosImposicion_xProvinciaResult_nsprefix_) else ''
            self.GetServiciosDeCentrosImposicion_xProvinciaResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetServiciosDeCentrosImposicion_xProvinciaResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GetServiciosDeCentrosImposicion_xProvinciaResult':
            obj_ = GetServiciosDeCentrosImposicion_xProvinciaResultType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetServiciosDeCentrosImposicion_xProvinciaResult = obj_
            obj_.original_tagname_ = 'GetServiciosDeCentrosImposicion_xProvinciaResult'
# end class GetServiciosDeCentrosImposicion_xProvinciaResponse


class GetCentrosImposicionPorCP(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CodigoPostal=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CodigoPostal = CodigoPostal
        self.CodigoPostal_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetCentrosImposicionPorCP)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetCentrosImposicionPorCP.subclass:
            return GetCentrosImposicionPorCP.subclass(*args_, **kwargs_)
        else:
            return GetCentrosImposicionPorCP(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CodigoPostal(self):
        return self.CodigoPostal
    def set_CodigoPostal(self, CodigoPostal):
        self.CodigoPostal = CodigoPostal
    def hasContent_(self):
        if (
            self.CodigoPostal is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionPorCP', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetCentrosImposicionPorCP')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetCentrosImposicionPorCP':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetCentrosImposicionPorCP')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetCentrosImposicionPorCP', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetCentrosImposicionPorCP'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionPorCP', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CodigoPostal is not None:
            namespaceprefix_ = self.CodigoPostal_nsprefix_ + ':' if (UseCapturedNS_ and self.CodigoPostal_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodigoPostal>%s</%sCodigoPostal>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodigoPostal), input_name='CodigoPostal')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'CodigoPostal':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodigoPostal')
            value_ = self.gds_validate_string(value_, node, 'CodigoPostal')
            self.CodigoPostal = value_
            self.CodigoPostal_nsprefix_ = child_.prefix
# end class GetCentrosImposicionPorCP


class GetCentrosImposicionPorCPResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetCentrosImposicionPorCPResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetCentrosImposicionPorCPResult = GetCentrosImposicionPorCPResult
        self.GetCentrosImposicionPorCPResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetCentrosImposicionPorCPResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetCentrosImposicionPorCPResponse.subclass:
            return GetCentrosImposicionPorCPResponse.subclass(*args_, **kwargs_)
        else:
            return GetCentrosImposicionPorCPResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetCentrosImposicionPorCPResult(self):
        return self.GetCentrosImposicionPorCPResult
    def set_GetCentrosImposicionPorCPResult(self, GetCentrosImposicionPorCPResult):
        self.GetCentrosImposicionPorCPResult = GetCentrosImposicionPorCPResult
    def hasContent_(self):
        if (
            self.GetCentrosImposicionPorCPResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionPorCPResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetCentrosImposicionPorCPResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetCentrosImposicionPorCPResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetCentrosImposicionPorCPResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetCentrosImposicionPorCPResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetCentrosImposicionPorCPResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionPorCPResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetCentrosImposicionPorCPResult is not None:
            namespaceprefix_ = self.GetCentrosImposicionPorCPResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetCentrosImposicionPorCPResult_nsprefix_) else ''
            self.GetCentrosImposicionPorCPResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetCentrosImposicionPorCPResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GetCentrosImposicionPorCPResult':
            obj_ = GetCentrosImposicionPorCPResultType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetCentrosImposicionPorCPResult = obj_
            obj_.original_tagname_ = 'GetCentrosImposicionPorCPResult'
# end class GetCentrosImposicionPorCPResponse


class GetCentrosImposicionAdmisionPorCP(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CodigoPostal=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CodigoPostal = CodigoPostal
        self.CodigoPostal_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetCentrosImposicionAdmisionPorCP)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetCentrosImposicionAdmisionPorCP.subclass:
            return GetCentrosImposicionAdmisionPorCP.subclass(*args_, **kwargs_)
        else:
            return GetCentrosImposicionAdmisionPorCP(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CodigoPostal(self):
        return self.CodigoPostal
    def set_CodigoPostal(self, CodigoPostal):
        self.CodigoPostal = CodigoPostal
    def hasContent_(self):
        if (
            self.CodigoPostal is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionAdmisionPorCP', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetCentrosImposicionAdmisionPorCP')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetCentrosImposicionAdmisionPorCP':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetCentrosImposicionAdmisionPorCP')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetCentrosImposicionAdmisionPorCP', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetCentrosImposicionAdmisionPorCP'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionAdmisionPorCP', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CodigoPostal is not None:
            namespaceprefix_ = self.CodigoPostal_nsprefix_ + ':' if (UseCapturedNS_ and self.CodigoPostal_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodigoPostal>%s</%sCodigoPostal>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodigoPostal), input_name='CodigoPostal')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'CodigoPostal':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodigoPostal')
            value_ = self.gds_validate_string(value_, node, 'CodigoPostal')
            self.CodigoPostal = value_
            self.CodigoPostal_nsprefix_ = child_.prefix
# end class GetCentrosImposicionAdmisionPorCP


class GetCentrosImposicionAdmisionPorCPResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetCentrosImposicionAdmisionPorCPResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetCentrosImposicionAdmisionPorCPResult = GetCentrosImposicionAdmisionPorCPResult
        self.GetCentrosImposicionAdmisionPorCPResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetCentrosImposicionAdmisionPorCPResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetCentrosImposicionAdmisionPorCPResponse.subclass:
            return GetCentrosImposicionAdmisionPorCPResponse.subclass(*args_, **kwargs_)
        else:
            return GetCentrosImposicionAdmisionPorCPResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetCentrosImposicionAdmisionPorCPResult(self):
        return self.GetCentrosImposicionAdmisionPorCPResult
    def set_GetCentrosImposicionAdmisionPorCPResult(self, GetCentrosImposicionAdmisionPorCPResult):
        self.GetCentrosImposicionAdmisionPorCPResult = GetCentrosImposicionAdmisionPorCPResult
    def hasContent_(self):
        if (
            self.GetCentrosImposicionAdmisionPorCPResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionAdmisionPorCPResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetCentrosImposicionAdmisionPorCPResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetCentrosImposicionAdmisionPorCPResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetCentrosImposicionAdmisionPorCPResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetCentrosImposicionAdmisionPorCPResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetCentrosImposicionAdmisionPorCPResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionAdmisionPorCPResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetCentrosImposicionAdmisionPorCPResult is not None:
            namespaceprefix_ = self.GetCentrosImposicionAdmisionPorCPResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetCentrosImposicionAdmisionPorCPResult_nsprefix_) else ''
            self.GetCentrosImposicionAdmisionPorCPResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetCentrosImposicionAdmisionPorCPResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GetCentrosImposicionAdmisionPorCPResult':
            obj_ = GetCentrosImposicionAdmisionPorCPResultType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetCentrosImposicionAdmisionPorCPResult = obj_
            obj_.original_tagname_ = 'GetCentrosImposicionAdmisionPorCPResult'
# end class GetCentrosImposicionAdmisionPorCPResponse


class GetHtmlDeEtiquetasPorOrdenOrNumeroEnvio(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, idOrdenRetiro=None, nroEnvio=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.idOrdenRetiro = idOrdenRetiro
        self.idOrdenRetiro_nsprefix_ = None
        self.nroEnvio = nroEnvio
        self.nroEnvio_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetHtmlDeEtiquetasPorOrdenOrNumeroEnvio)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetHtmlDeEtiquetasPorOrdenOrNumeroEnvio.subclass:
            return GetHtmlDeEtiquetasPorOrdenOrNumeroEnvio.subclass(*args_, **kwargs_)
        else:
            return GetHtmlDeEtiquetasPorOrdenOrNumeroEnvio(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_idOrdenRetiro(self):
        return self.idOrdenRetiro
    def set_idOrdenRetiro(self, idOrdenRetiro):
        self.idOrdenRetiro = idOrdenRetiro
    def get_nroEnvio(self):
        return self.nroEnvio
    def set_nroEnvio(self, nroEnvio):
        self.nroEnvio = nroEnvio
    def hasContent_(self):
        if (
            self.idOrdenRetiro is not None or
            self.nroEnvio is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvio', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetHtmlDeEtiquetasPorOrdenOrNumeroEnvio')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetHtmlDeEtiquetasPorOrdenOrNumeroEnvio':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvio')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvio', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvio'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvio', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.idOrdenRetiro is not None:
            namespaceprefix_ = self.idOrdenRetiro_nsprefix_ + ':' if (UseCapturedNS_ and self.idOrdenRetiro_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sidOrdenRetiro>%s</%sidOrdenRetiro>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.idOrdenRetiro), input_name='idOrdenRetiro')), namespaceprefix_ , eol_))
        if self.nroEnvio is not None:
            namespaceprefix_ = self.nroEnvio_nsprefix_ + ':' if (UseCapturedNS_ and self.nroEnvio_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snroEnvio>%s</%snroEnvio>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.nroEnvio), input_name='nroEnvio')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'idOrdenRetiro':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'idOrdenRetiro')
            value_ = self.gds_validate_string(value_, node, 'idOrdenRetiro')
            self.idOrdenRetiro = value_
            self.idOrdenRetiro_nsprefix_ = child_.prefix
        elif nodeName_ == 'nroEnvio':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'nroEnvio')
            value_ = self.gds_validate_string(value_, node, 'nroEnvio')
            self.nroEnvio = value_
            self.nroEnvio_nsprefix_ = child_.prefix
# end class GetHtmlDeEtiquetasPorOrdenOrNumeroEnvio


class GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult = GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult
        self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResponse.subclass:
            return GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResponse.subclass(*args_, **kwargs_)
        else:
            return GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult(self):
        return self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult
    def set_GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult(self, GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult):
        self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult = GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult
    def hasContent_(self):
        if (
            self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult is not None:
            namespaceprefix_ = self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult>%s</%sGetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult), input_name='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult')
            value_ = self.gds_validate_string(value_, node, 'GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult')
            self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult = value_
            self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_ = child_.prefix
# end class GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResponse


class GetHtmlDeEtiquetasPorOrdenes(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, idsOrdenRetiro=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.idsOrdenRetiro = idsOrdenRetiro
        self.idsOrdenRetiro_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetHtmlDeEtiquetasPorOrdenes)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetHtmlDeEtiquetasPorOrdenes.subclass:
            return GetHtmlDeEtiquetasPorOrdenes.subclass(*args_, **kwargs_)
        else:
            return GetHtmlDeEtiquetasPorOrdenes(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_idsOrdenRetiro(self):
        return self.idsOrdenRetiro
    def set_idsOrdenRetiro(self, idsOrdenRetiro):
        self.idsOrdenRetiro = idsOrdenRetiro
    def hasContent_(self):
        if (
            self.idsOrdenRetiro is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasPorOrdenes', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetHtmlDeEtiquetasPorOrdenes')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetHtmlDeEtiquetasPorOrdenes':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetHtmlDeEtiquetasPorOrdenes')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetHtmlDeEtiquetasPorOrdenes', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetHtmlDeEtiquetasPorOrdenes'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasPorOrdenes', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.idsOrdenRetiro is not None:
            namespaceprefix_ = self.idsOrdenRetiro_nsprefix_ + ':' if (UseCapturedNS_ and self.idsOrdenRetiro_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sidsOrdenRetiro>%s</%sidsOrdenRetiro>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.idsOrdenRetiro), input_name='idsOrdenRetiro')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'idsOrdenRetiro':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'idsOrdenRetiro')
            value_ = self.gds_validate_string(value_, node, 'idsOrdenRetiro')
            self.idsOrdenRetiro = value_
            self.idsOrdenRetiro_nsprefix_ = child_.prefix
# end class GetHtmlDeEtiquetasPorOrdenes


class GetHtmlDeEtiquetasPorOrdenesResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetHtmlDeEtiquetasPorOrdenesResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetHtmlDeEtiquetasPorOrdenesResult = GetHtmlDeEtiquetasPorOrdenesResult
        self.GetHtmlDeEtiquetasPorOrdenesResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetHtmlDeEtiquetasPorOrdenesResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetHtmlDeEtiquetasPorOrdenesResponse.subclass:
            return GetHtmlDeEtiquetasPorOrdenesResponse.subclass(*args_, **kwargs_)
        else:
            return GetHtmlDeEtiquetasPorOrdenesResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetHtmlDeEtiquetasPorOrdenesResult(self):
        return self.GetHtmlDeEtiquetasPorOrdenesResult
    def set_GetHtmlDeEtiquetasPorOrdenesResult(self, GetHtmlDeEtiquetasPorOrdenesResult):
        self.GetHtmlDeEtiquetasPorOrdenesResult = GetHtmlDeEtiquetasPorOrdenesResult
    def hasContent_(self):
        if (
            self.GetHtmlDeEtiquetasPorOrdenesResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasPorOrdenesResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetHtmlDeEtiquetasPorOrdenesResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetHtmlDeEtiquetasPorOrdenesResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetHtmlDeEtiquetasPorOrdenesResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetHtmlDeEtiquetasPorOrdenesResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetHtmlDeEtiquetasPorOrdenesResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasPorOrdenesResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetHtmlDeEtiquetasPorOrdenesResult is not None:
            namespaceprefix_ = self.GetHtmlDeEtiquetasPorOrdenesResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetHtmlDeEtiquetasPorOrdenesResult_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetHtmlDeEtiquetasPorOrdenesResult>%s</%sGetHtmlDeEtiquetasPorOrdenesResult>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GetHtmlDeEtiquetasPorOrdenesResult), input_name='GetHtmlDeEtiquetasPorOrdenesResult')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'GetHtmlDeEtiquetasPorOrdenesResult':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GetHtmlDeEtiquetasPorOrdenesResult')
            value_ = self.gds_validate_string(value_, node, 'GetHtmlDeEtiquetasPorOrdenesResult')
            self.GetHtmlDeEtiquetasPorOrdenesResult = value_
            self.GetHtmlDeEtiquetasPorOrdenesResult_nsprefix_ = child_.prefix
# end class GetHtmlDeEtiquetasPorOrdenesResponse


class GetDivDeEtiquetasPorOrdenOrNumeroEnvio(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, idOrdenRetiro=None, nroEnvio=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.idOrdenRetiro = idOrdenRetiro
        self.idOrdenRetiro_nsprefix_ = None
        self.nroEnvio = nroEnvio
        self.nroEnvio_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetDivDeEtiquetasPorOrdenOrNumeroEnvio)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetDivDeEtiquetasPorOrdenOrNumeroEnvio.subclass:
            return GetDivDeEtiquetasPorOrdenOrNumeroEnvio.subclass(*args_, **kwargs_)
        else:
            return GetDivDeEtiquetasPorOrdenOrNumeroEnvio(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_idOrdenRetiro(self):
        return self.idOrdenRetiro
    def set_idOrdenRetiro(self, idOrdenRetiro):
        self.idOrdenRetiro = idOrdenRetiro
    def get_nroEnvio(self):
        return self.nroEnvio
    def set_nroEnvio(self, nroEnvio):
        self.nroEnvio = nroEnvio
    def hasContent_(self):
        if (
            self.idOrdenRetiro is not None or
            self.nroEnvio is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetDivDeEtiquetasPorOrdenOrNumeroEnvio', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetDivDeEtiquetasPorOrdenOrNumeroEnvio')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetDivDeEtiquetasPorOrdenOrNumeroEnvio':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetDivDeEtiquetasPorOrdenOrNumeroEnvio')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetDivDeEtiquetasPorOrdenOrNumeroEnvio', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetDivDeEtiquetasPorOrdenOrNumeroEnvio'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetDivDeEtiquetasPorOrdenOrNumeroEnvio', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.idOrdenRetiro is not None:
            namespaceprefix_ = self.idOrdenRetiro_nsprefix_ + ':' if (UseCapturedNS_ and self.idOrdenRetiro_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sidOrdenRetiro>%s</%sidOrdenRetiro>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.idOrdenRetiro), input_name='idOrdenRetiro')), namespaceprefix_ , eol_))
        if self.nroEnvio is not None:
            namespaceprefix_ = self.nroEnvio_nsprefix_ + ':' if (UseCapturedNS_ and self.nroEnvio_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snroEnvio>%s</%snroEnvio>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.nroEnvio), input_name='nroEnvio')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'idOrdenRetiro':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'idOrdenRetiro')
            value_ = self.gds_validate_string(value_, node, 'idOrdenRetiro')
            self.idOrdenRetiro = value_
            self.idOrdenRetiro_nsprefix_ = child_.prefix
        elif nodeName_ == 'nroEnvio':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'nroEnvio')
            value_ = self.gds_validate_string(value_, node, 'nroEnvio')
            self.nroEnvio = value_
            self.nroEnvio_nsprefix_ = child_.prefix
# end class GetDivDeEtiquetasPorOrdenOrNumeroEnvio


class GetDivDeEtiquetasPorOrdenOrNumeroEnvioResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult = GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult
        self.GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetDivDeEtiquetasPorOrdenOrNumeroEnvioResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetDivDeEtiquetasPorOrdenOrNumeroEnvioResponse.subclass:
            return GetDivDeEtiquetasPorOrdenOrNumeroEnvioResponse.subclass(*args_, **kwargs_)
        else:
            return GetDivDeEtiquetasPorOrdenOrNumeroEnvioResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult(self):
        return self.GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult
    def set_GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult(self, GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult):
        self.GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult = GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult
    def hasContent_(self):
        if (
            self.GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetDivDeEtiquetasPorOrdenOrNumeroEnvioResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetDivDeEtiquetasPorOrdenOrNumeroEnvioResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetDivDeEtiquetasPorOrdenOrNumeroEnvioResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetDivDeEtiquetasPorOrdenOrNumeroEnvioResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetDivDeEtiquetasPorOrdenOrNumeroEnvioResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetDivDeEtiquetasPorOrdenOrNumeroEnvioResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetDivDeEtiquetasPorOrdenOrNumeroEnvioResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult is not None:
            namespaceprefix_ = self.GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetDivDeEtiquetasPorOrdenOrNumeroEnvioResult>%s</%sGetDivDeEtiquetasPorOrdenOrNumeroEnvioResult>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult), input_name='GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult')
            value_ = self.gds_validate_string(value_, node, 'GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult')
            self.GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult = value_
            self.GetDivDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_ = child_.prefix
# end class GetDivDeEtiquetasPorOrdenOrNumeroEnvioResponse


class GetDivDeEtiquetaByIdPieza(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, idPieza=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.idPieza = idPieza
        self.idPieza_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetDivDeEtiquetaByIdPieza)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetDivDeEtiquetaByIdPieza.subclass:
            return GetDivDeEtiquetaByIdPieza.subclass(*args_, **kwargs_)
        else:
            return GetDivDeEtiquetaByIdPieza(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_idPieza(self):
        return self.idPieza
    def set_idPieza(self, idPieza):
        self.idPieza = idPieza
    def hasContent_(self):
        if (
            self.idPieza is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetDivDeEtiquetaByIdPieza', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetDivDeEtiquetaByIdPieza')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetDivDeEtiquetaByIdPieza':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetDivDeEtiquetaByIdPieza')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetDivDeEtiquetaByIdPieza', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetDivDeEtiquetaByIdPieza'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetDivDeEtiquetaByIdPieza', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.idPieza is not None:
            namespaceprefix_ = self.idPieza_nsprefix_ + ':' if (UseCapturedNS_ and self.idPieza_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sidPieza>%s</%sidPieza>%s' % (namespaceprefix_ , self.gds_format_integer(self.idPieza, input_name='idPieza'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'idPieza' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'idPieza')
            ival_ = self.gds_validate_integer(ival_, node, 'idPieza')
            self.idPieza = ival_
            self.idPieza_nsprefix_ = child_.prefix
# end class GetDivDeEtiquetaByIdPieza


class GetDivDeEtiquetaByIdPiezaResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetDivDeEtiquetaByIdPiezaResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetDivDeEtiquetaByIdPiezaResult = GetDivDeEtiquetaByIdPiezaResult
        self.GetDivDeEtiquetaByIdPiezaResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetDivDeEtiquetaByIdPiezaResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetDivDeEtiquetaByIdPiezaResponse.subclass:
            return GetDivDeEtiquetaByIdPiezaResponse.subclass(*args_, **kwargs_)
        else:
            return GetDivDeEtiquetaByIdPiezaResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetDivDeEtiquetaByIdPiezaResult(self):
        return self.GetDivDeEtiquetaByIdPiezaResult
    def set_GetDivDeEtiquetaByIdPiezaResult(self, GetDivDeEtiquetaByIdPiezaResult):
        self.GetDivDeEtiquetaByIdPiezaResult = GetDivDeEtiquetaByIdPiezaResult
    def hasContent_(self):
        if (
            self.GetDivDeEtiquetaByIdPiezaResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetDivDeEtiquetaByIdPiezaResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetDivDeEtiquetaByIdPiezaResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetDivDeEtiquetaByIdPiezaResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetDivDeEtiquetaByIdPiezaResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetDivDeEtiquetaByIdPiezaResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetDivDeEtiquetaByIdPiezaResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetDivDeEtiquetaByIdPiezaResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetDivDeEtiquetaByIdPiezaResult is not None:
            namespaceprefix_ = self.GetDivDeEtiquetaByIdPiezaResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetDivDeEtiquetaByIdPiezaResult_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetDivDeEtiquetaByIdPiezaResult>%s</%sGetDivDeEtiquetaByIdPiezaResult>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GetDivDeEtiquetaByIdPiezaResult), input_name='GetDivDeEtiquetaByIdPiezaResult')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'GetDivDeEtiquetaByIdPiezaResult':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GetDivDeEtiquetaByIdPiezaResult')
            value_ = self.gds_validate_string(value_, node, 'GetDivDeEtiquetaByIdPiezaResult')
            self.GetDivDeEtiquetaByIdPiezaResult = value_
            self.GetDivDeEtiquetaByIdPiezaResult_nsprefix_ = child_.prefix
# end class GetDivDeEtiquetaByIdPiezaResponse


class GetCSSDeEtiquetasPorOrdenOrNumeroEnvio(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, paraEtiquetadora=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.paraEtiquetadora = paraEtiquetadora
        self.paraEtiquetadora_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetCSSDeEtiquetasPorOrdenOrNumeroEnvio)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetCSSDeEtiquetasPorOrdenOrNumeroEnvio.subclass:
            return GetCSSDeEtiquetasPorOrdenOrNumeroEnvio.subclass(*args_, **kwargs_)
        else:
            return GetCSSDeEtiquetasPorOrdenOrNumeroEnvio(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_paraEtiquetadora(self):
        return self.paraEtiquetadora
    def set_paraEtiquetadora(self, paraEtiquetadora):
        self.paraEtiquetadora = paraEtiquetadora
    def hasContent_(self):
        if (
            self.paraEtiquetadora is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCSSDeEtiquetasPorOrdenOrNumeroEnvio', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetCSSDeEtiquetasPorOrdenOrNumeroEnvio')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetCSSDeEtiquetasPorOrdenOrNumeroEnvio':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetCSSDeEtiquetasPorOrdenOrNumeroEnvio')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetCSSDeEtiquetasPorOrdenOrNumeroEnvio', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetCSSDeEtiquetasPorOrdenOrNumeroEnvio'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCSSDeEtiquetasPorOrdenOrNumeroEnvio', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.paraEtiquetadora is not None:
            namespaceprefix_ = self.paraEtiquetadora_nsprefix_ + ':' if (UseCapturedNS_ and self.paraEtiquetadora_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sparaEtiquetadora>%s</%sparaEtiquetadora>%s' % (namespaceprefix_ , self.gds_format_boolean(self.paraEtiquetadora, input_name='paraEtiquetadora'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'paraEtiquetadora':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'paraEtiquetadora')
            ival_ = self.gds_validate_boolean(ival_, node, 'paraEtiquetadora')
            self.paraEtiquetadora = ival_
            self.paraEtiquetadora_nsprefix_ = child_.prefix
# end class GetCSSDeEtiquetasPorOrdenOrNumeroEnvio


class GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult = GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult
        self.GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResponse.subclass:
            return GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResponse.subclass(*args_, **kwargs_)
        else:
            return GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult(self):
        return self.GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult
    def set_GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult(self, GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult):
        self.GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult = GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult
    def hasContent_(self):
        if (
            self.GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult is not None:
            namespaceprefix_ = self.GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult>%s</%sGetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult), input_name='GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult')
            value_ = self.gds_validate_string(value_, node, 'GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult')
            self.GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult = value_
            self.GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_ = child_.prefix
# end class GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResponse


class GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadora(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, idOrdenRetiro=None, nroEnvio=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.idOrdenRetiro = idOrdenRetiro
        self.idOrdenRetiro_nsprefix_ = None
        self.nroEnvio = nroEnvio
        self.nroEnvio_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadora)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadora.subclass:
            return GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadora.subclass(*args_, **kwargs_)
        else:
            return GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadora(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_idOrdenRetiro(self):
        return self.idOrdenRetiro
    def set_idOrdenRetiro(self, idOrdenRetiro):
        self.idOrdenRetiro = idOrdenRetiro
    def get_nroEnvio(self):
        return self.nroEnvio
    def set_nroEnvio(self, nroEnvio):
        self.nroEnvio = nroEnvio
    def hasContent_(self):
        if (
            self.idOrdenRetiro is not None or
            self.nroEnvio is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadora', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadora')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadora':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadora')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadora', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadora'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadora', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.idOrdenRetiro is not None:
            namespaceprefix_ = self.idOrdenRetiro_nsprefix_ + ':' if (UseCapturedNS_ and self.idOrdenRetiro_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sidOrdenRetiro>%s</%sidOrdenRetiro>%s' % (namespaceprefix_ , self.gds_format_integer(self.idOrdenRetiro, input_name='idOrdenRetiro'), namespaceprefix_ , eol_))
        if self.nroEnvio is not None:
            namespaceprefix_ = self.nroEnvio_nsprefix_ + ':' if (UseCapturedNS_ and self.nroEnvio_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snroEnvio>%s</%snroEnvio>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.nroEnvio), input_name='nroEnvio')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'idOrdenRetiro' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'idOrdenRetiro')
            ival_ = self.gds_validate_integer(ival_, node, 'idOrdenRetiro')
            self.idOrdenRetiro = ival_
            self.idOrdenRetiro_nsprefix_ = child_.prefix
        elif nodeName_ == 'nroEnvio':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'nroEnvio')
            value_ = self.gds_validate_string(value_, node, 'nroEnvio')
            self.nroEnvio = value_
            self.nroEnvio_nsprefix_ = child_.prefix
# end class GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadora


class GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult = GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult
        self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResponse.subclass:
            return GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResponse.subclass(*args_, **kwargs_)
        else:
            return GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult(self):
        return self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult
    def set_GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult(self, GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult):
        self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult = GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult
    def hasContent_(self):
        if (
            self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult is not None:
            namespaceprefix_ = self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult>%s</%sGetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult), input_name='GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult')
            value_ = self.gds_validate_string(value_, node, 'GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult')
            self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult = value_
            self.GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResult_nsprefix_ = child_.prefix
# end class GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResponse


class GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvio(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, idOrdenRetiro=None, nroEnvio=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.idOrdenRetiro = idOrdenRetiro
        self.idOrdenRetiro_nsprefix_ = None
        self.nroEnvio = nroEnvio
        self.nroEnvio_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvio)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvio.subclass:
            return GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvio.subclass(*args_, **kwargs_)
        else:
            return GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvio(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_idOrdenRetiro(self):
        return self.idOrdenRetiro
    def set_idOrdenRetiro(self, idOrdenRetiro):
        self.idOrdenRetiro = idOrdenRetiro
    def get_nroEnvio(self):
        return self.nroEnvio
    def set_nroEnvio(self, nroEnvio):
        self.nroEnvio = nroEnvio
    def hasContent_(self):
        if (
            self.idOrdenRetiro is not None or
            self.nroEnvio is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvio', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvio')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvio':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvio')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvio', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvio'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvio', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.idOrdenRetiro is not None:
            namespaceprefix_ = self.idOrdenRetiro_nsprefix_ + ':' if (UseCapturedNS_ and self.idOrdenRetiro_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sidOrdenRetiro>%s</%sidOrdenRetiro>%s' % (namespaceprefix_ , self.gds_format_integer(self.idOrdenRetiro, input_name='idOrdenRetiro'), namespaceprefix_ , eol_))
        if self.nroEnvio is not None:
            namespaceprefix_ = self.nroEnvio_nsprefix_ + ':' if (UseCapturedNS_ and self.nroEnvio_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snroEnvio>%s</%snroEnvio>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.nroEnvio), input_name='nroEnvio')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'idOrdenRetiro' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'idOrdenRetiro')
            ival_ = self.gds_validate_integer(ival_, node, 'idOrdenRetiro')
            self.idOrdenRetiro = ival_
            self.idOrdenRetiro_nsprefix_ = child_.prefix
        elif nodeName_ == 'nroEnvio':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'nroEnvio')
            value_ = self.gds_validate_string(value_, node, 'nroEnvio')
            self.nroEnvio = value_
            self.nroEnvio_nsprefix_ = child_.prefix
# end class GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvio


class GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult = GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult
        self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResponse.subclass:
            return GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResponse.subclass(*args_, **kwargs_)
        else:
            return GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult(self):
        return self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult
    def set_GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult(self, GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult):
        self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult = GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult
    def hasContent_(self):
        if (
            self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult is not None:
            namespaceprefix_ = self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult>%s</%sGetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult), input_name='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult')
            value_ = self.gds_validate_string(value_, node, 'GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult')
            self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult = value_
            self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResult_nsprefix_ = child_.prefix
# end class GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResponse


class GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadora(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, idOrdenRetiro=None, nroEnvio=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.idOrdenRetiro = idOrdenRetiro
        self.idOrdenRetiro_nsprefix_ = None
        self.nroEnvio = nroEnvio
        self.nroEnvio_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadora)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadora.subclass:
            return GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadora.subclass(*args_, **kwargs_)
        else:
            return GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadora(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_idOrdenRetiro(self):
        return self.idOrdenRetiro
    def set_idOrdenRetiro(self, idOrdenRetiro):
        self.idOrdenRetiro = idOrdenRetiro
    def get_nroEnvio(self):
        return self.nroEnvio
    def set_nroEnvio(self, nroEnvio):
        self.nroEnvio = nroEnvio
    def hasContent_(self):
        if (
            self.idOrdenRetiro is not None or
            self.nroEnvio is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadora', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadora')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadora':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadora')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadora', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadora'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadora', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.idOrdenRetiro is not None:
            namespaceprefix_ = self.idOrdenRetiro_nsprefix_ + ':' if (UseCapturedNS_ and self.idOrdenRetiro_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sidOrdenRetiro>%s</%sidOrdenRetiro>%s' % (namespaceprefix_ , self.gds_format_integer(self.idOrdenRetiro, input_name='idOrdenRetiro'), namespaceprefix_ , eol_))
        if self.nroEnvio is not None:
            namespaceprefix_ = self.nroEnvio_nsprefix_ + ':' if (UseCapturedNS_ and self.nroEnvio_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snroEnvio>%s</%snroEnvio>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.nroEnvio), input_name='nroEnvio')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'idOrdenRetiro' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'idOrdenRetiro')
            ival_ = self.gds_validate_integer(ival_, node, 'idOrdenRetiro')
            self.idOrdenRetiro = ival_
            self.idOrdenRetiro_nsprefix_ = child_.prefix
        elif nodeName_ == 'nroEnvio':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'nroEnvio')
            value_ = self.gds_validate_string(value_, node, 'nroEnvio')
            self.nroEnvio = value_
            self.nroEnvio_nsprefix_ = child_.prefix
# end class GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadora


class GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult = GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult
        self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResponse.subclass:
            return GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResponse.subclass(*args_, **kwargs_)
        else:
            return GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult(self):
        return self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult
    def set_GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult(self, GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult):
        self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult = GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult
    def hasContent_(self):
        if (
            self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult is not None:
            namespaceprefix_ = self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult>%s</%sGetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult), input_name='GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult')
            value_ = self.gds_validate_string(value_, node, 'GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult')
            self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult = value_
            self.GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResult_nsprefix_ = child_.prefix
# end class GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResponse


class GetPdfDeEtiquetasPorOrdenOrNumeroEnvio(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, idOrdenRetiro=None, nroEnvio=None, logisticaInversa=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.idOrdenRetiro = idOrdenRetiro
        self.idOrdenRetiro_nsprefix_ = None
        self.nroEnvio = nroEnvio
        self.nroEnvio_nsprefix_ = None
        self.logisticaInversa = logisticaInversa
        self.logisticaInversa_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetPdfDeEtiquetasPorOrdenOrNumeroEnvio)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetPdfDeEtiquetasPorOrdenOrNumeroEnvio.subclass:
            return GetPdfDeEtiquetasPorOrdenOrNumeroEnvio.subclass(*args_, **kwargs_)
        else:
            return GetPdfDeEtiquetasPorOrdenOrNumeroEnvio(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_idOrdenRetiro(self):
        return self.idOrdenRetiro
    def set_idOrdenRetiro(self, idOrdenRetiro):
        self.idOrdenRetiro = idOrdenRetiro
    def get_nroEnvio(self):
        return self.nroEnvio
    def set_nroEnvio(self, nroEnvio):
        self.nroEnvio = nroEnvio
    def get_logisticaInversa(self):
        return self.logisticaInversa
    def set_logisticaInversa(self, logisticaInversa):
        self.logisticaInversa = logisticaInversa
    def hasContent_(self):
        if (
            self.idOrdenRetiro is not None or
            self.nroEnvio is not None or
            self.logisticaInversa is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvio', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetPdfDeEtiquetasPorOrdenOrNumeroEnvio')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetPdfDeEtiquetasPorOrdenOrNumeroEnvio':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvio')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvio', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvio'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvio', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.idOrdenRetiro is not None:
            namespaceprefix_ = self.idOrdenRetiro_nsprefix_ + ':' if (UseCapturedNS_ and self.idOrdenRetiro_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sidOrdenRetiro>%s</%sidOrdenRetiro>%s' % (namespaceprefix_ , self.gds_format_integer(self.idOrdenRetiro, input_name='idOrdenRetiro'), namespaceprefix_ , eol_))
        if self.nroEnvio is not None:
            namespaceprefix_ = self.nroEnvio_nsprefix_ + ':' if (UseCapturedNS_ and self.nroEnvio_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snroEnvio>%s</%snroEnvio>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.nroEnvio), input_name='nroEnvio')), namespaceprefix_ , eol_))
        if self.logisticaInversa is not None:
            namespaceprefix_ = self.logisticaInversa_nsprefix_ + ':' if (UseCapturedNS_ and self.logisticaInversa_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slogisticaInversa>%s</%slogisticaInversa>%s' % (namespaceprefix_ , self.gds_format_boolean(self.logisticaInversa, input_name='logisticaInversa'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'idOrdenRetiro' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'idOrdenRetiro')
            ival_ = self.gds_validate_integer(ival_, node, 'idOrdenRetiro')
            self.idOrdenRetiro = ival_
            self.idOrdenRetiro_nsprefix_ = child_.prefix
        elif nodeName_ == 'nroEnvio':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'nroEnvio')
            value_ = self.gds_validate_string(value_, node, 'nroEnvio')
            self.nroEnvio = value_
            self.nroEnvio_nsprefix_ = child_.prefix
        elif nodeName_ == 'logisticaInversa':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'logisticaInversa')
            ival_ = self.gds_validate_boolean(ival_, node, 'logisticaInversa')
            self.logisticaInversa = ival_
            self.logisticaInversa_nsprefix_ = child_.prefix
# end class GetPdfDeEtiquetasPorOrdenOrNumeroEnvio


class GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult = GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult
        self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResponse.subclass:
            return GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResponse.subclass(*args_, **kwargs_)
        else:
            return GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult(self):
        return self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult
    def set_GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult(self, GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult):
        self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult = GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult
    def hasContent_(self):
        if (
            self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult is not None:
            namespaceprefix_ = self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult>%s</%sGetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult), input_name='GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult')
            value_ = self.gds_validate_string(value_, node, 'GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult')
            self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult = value_
            self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_ = child_.prefix
# end class GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResponse


class GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidas(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, idOrdenRetiro=None, nroEnvio=None, logisticaInversa=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.idOrdenRetiro = idOrdenRetiro
        self.idOrdenRetiro_nsprefix_ = None
        self.nroEnvio = nroEnvio
        self.nroEnvio_nsprefix_ = None
        self.logisticaInversa = logisticaInversa
        self.logisticaInversa_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidas)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidas.subclass:
            return GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidas.subclass(*args_, **kwargs_)
        else:
            return GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidas(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_idOrdenRetiro(self):
        return self.idOrdenRetiro
    def set_idOrdenRetiro(self, idOrdenRetiro):
        self.idOrdenRetiro = idOrdenRetiro
    def get_nroEnvio(self):
        return self.nroEnvio
    def set_nroEnvio(self, nroEnvio):
        self.nroEnvio = nroEnvio
    def get_logisticaInversa(self):
        return self.logisticaInversa
    def set_logisticaInversa(self, logisticaInversa):
        self.logisticaInversa = logisticaInversa
    def hasContent_(self):
        if (
            self.idOrdenRetiro is not None or
            self.nroEnvio is not None or
            self.logisticaInversa is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidas', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidas')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidas':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidas')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidas', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidas'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidas', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.idOrdenRetiro is not None:
            namespaceprefix_ = self.idOrdenRetiro_nsprefix_ + ':' if (UseCapturedNS_ and self.idOrdenRetiro_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sidOrdenRetiro>%s</%sidOrdenRetiro>%s' % (namespaceprefix_ , self.gds_format_integer(self.idOrdenRetiro, input_name='idOrdenRetiro'), namespaceprefix_ , eol_))
        if self.nroEnvio is not None:
            namespaceprefix_ = self.nroEnvio_nsprefix_ + ':' if (UseCapturedNS_ and self.nroEnvio_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snroEnvio>%s</%snroEnvio>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.nroEnvio), input_name='nroEnvio')), namespaceprefix_ , eol_))
        if self.logisticaInversa is not None:
            namespaceprefix_ = self.logisticaInversa_nsprefix_ + ':' if (UseCapturedNS_ and self.logisticaInversa_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slogisticaInversa>%s</%slogisticaInversa>%s' % (namespaceprefix_ , self.gds_format_boolean(self.logisticaInversa, input_name='logisticaInversa'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'idOrdenRetiro' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'idOrdenRetiro')
            ival_ = self.gds_validate_integer(ival_, node, 'idOrdenRetiro')
            self.idOrdenRetiro = ival_
            self.idOrdenRetiro_nsprefix_ = child_.prefix
        elif nodeName_ == 'nroEnvio':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'nroEnvio')
            value_ = self.gds_validate_string(value_, node, 'nroEnvio')
            self.nroEnvio = value_
            self.nroEnvio_nsprefix_ = child_.prefix
        elif nodeName_ == 'logisticaInversa':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'logisticaInversa')
            ival_ = self.gds_validate_boolean(ival_, node, 'logisticaInversa')
            self.logisticaInversa = ival_
            self.logisticaInversa_nsprefix_ = child_.prefix
# end class GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidas


class GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult = GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult
        self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResponse.subclass:
            return GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResponse.subclass(*args_, **kwargs_)
        else:
            return GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult(self):
        return self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult
    def set_GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult(self, GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult):
        self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult = GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult
    def hasContent_(self):
        if (
            self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult is not None:
            namespaceprefix_ = self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult_nsprefix_) else ''
            self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult':
            obj_ = EtiquetasPDFResponse.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult = obj_
            obj_.original_tagname_ = 'GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResult'
# end class GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResponse


class EtiquetasPDFResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, trackingNumber=None, pdf=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.trackingNumber = trackingNumber
        self.trackingNumber_nsprefix_ = None
        self.pdf = pdf
        self.pdf_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EtiquetasPDFResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EtiquetasPDFResponse.subclass:
            return EtiquetasPDFResponse.subclass(*args_, **kwargs_)
        else:
            return EtiquetasPDFResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_trackingNumber(self):
        return self.trackingNumber
    def set_trackingNumber(self, trackingNumber):
        self.trackingNumber = trackingNumber
    def get_pdf(self):
        return self.pdf
    def set_pdf(self, pdf):
        self.pdf = pdf
    def hasContent_(self):
        if (
            self.trackingNumber is not None or
            self.pdf is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EtiquetasPDFResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EtiquetasPDFResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EtiquetasPDFResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EtiquetasPDFResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='EtiquetasPDFResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EtiquetasPDFResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EtiquetasPDFResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.trackingNumber is not None:
            namespaceprefix_ = self.trackingNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.trackingNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%strackingNumber>%s</%strackingNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.trackingNumber), input_name='trackingNumber')), namespaceprefix_ , eol_))
        if self.pdf is not None:
            namespaceprefix_ = self.pdf_nsprefix_ + ':' if (UseCapturedNS_ and self.pdf_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spdf>%s</%spdf>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.pdf), input_name='pdf')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'trackingNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'trackingNumber')
            value_ = self.gds_validate_string(value_, node, 'trackingNumber')
            self.trackingNumber = value_
            self.trackingNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'pdf':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'pdf')
            value_ = self.gds_validate_string(value_, node, 'pdf')
            self.pdf = value_
            self.pdf_nsprefix_ = child_.prefix
# end class EtiquetasPDFResponse


class GetDatosDeEtiquetasPorOrdenOrNumeroEnvio(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, idOrdenRetiro=None, nroEnvio=None, isLocker=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.idOrdenRetiro = idOrdenRetiro
        self.idOrdenRetiro_nsprefix_ = None
        self.nroEnvio = nroEnvio
        self.nroEnvio_nsprefix_ = None
        self.isLocker = isLocker
        self.isLocker_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetDatosDeEtiquetasPorOrdenOrNumeroEnvio)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetDatosDeEtiquetasPorOrdenOrNumeroEnvio.subclass:
            return GetDatosDeEtiquetasPorOrdenOrNumeroEnvio.subclass(*args_, **kwargs_)
        else:
            return GetDatosDeEtiquetasPorOrdenOrNumeroEnvio(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_idOrdenRetiro(self):
        return self.idOrdenRetiro
    def set_idOrdenRetiro(self, idOrdenRetiro):
        self.idOrdenRetiro = idOrdenRetiro
    def get_nroEnvio(self):
        return self.nroEnvio
    def set_nroEnvio(self, nroEnvio):
        self.nroEnvio = nroEnvio
    def get_isLocker(self):
        return self.isLocker
    def set_isLocker(self, isLocker):
        self.isLocker = isLocker
    def hasContent_(self):
        if (
            self.idOrdenRetiro is not None or
            self.nroEnvio is not None or
            self.isLocker is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetDatosDeEtiquetasPorOrdenOrNumeroEnvio', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetDatosDeEtiquetasPorOrdenOrNumeroEnvio')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetDatosDeEtiquetasPorOrdenOrNumeroEnvio':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetDatosDeEtiquetasPorOrdenOrNumeroEnvio')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetDatosDeEtiquetasPorOrdenOrNumeroEnvio', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetDatosDeEtiquetasPorOrdenOrNumeroEnvio'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetDatosDeEtiquetasPorOrdenOrNumeroEnvio', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.idOrdenRetiro is not None:
            namespaceprefix_ = self.idOrdenRetiro_nsprefix_ + ':' if (UseCapturedNS_ and self.idOrdenRetiro_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sidOrdenRetiro>%s</%sidOrdenRetiro>%s' % (namespaceprefix_ , self.gds_format_integer(self.idOrdenRetiro, input_name='idOrdenRetiro'), namespaceprefix_ , eol_))
        if self.nroEnvio is not None:
            namespaceprefix_ = self.nroEnvio_nsprefix_ + ':' if (UseCapturedNS_ and self.nroEnvio_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snroEnvio>%s</%snroEnvio>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.nroEnvio), input_name='nroEnvio')), namespaceprefix_ , eol_))
        if self.isLocker is not None:
            namespaceprefix_ = self.isLocker_nsprefix_ + ':' if (UseCapturedNS_ and self.isLocker_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sisLocker>%s</%sisLocker>%s' % (namespaceprefix_ , self.gds_format_boolean(self.isLocker, input_name='isLocker'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'idOrdenRetiro' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'idOrdenRetiro')
            ival_ = self.gds_validate_integer(ival_, node, 'idOrdenRetiro')
            self.idOrdenRetiro = ival_
            self.idOrdenRetiro_nsprefix_ = child_.prefix
        elif nodeName_ == 'nroEnvio':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'nroEnvio')
            value_ = self.gds_validate_string(value_, node, 'nroEnvio')
            self.nroEnvio = value_
            self.nroEnvio_nsprefix_ = child_.prefix
        elif nodeName_ == 'isLocker':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'isLocker')
            ival_ = self.gds_validate_boolean(ival_, node, 'isLocker')
            self.isLocker = ival_
            self.isLocker_nsprefix_ = child_.prefix
# end class GetDatosDeEtiquetasPorOrdenOrNumeroEnvio


class GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult = GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult
        self.GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResponse.subclass:
            return GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResponse.subclass(*args_, **kwargs_)
        else:
            return GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult(self):
        return self.GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult
    def set_GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult(self, GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult):
        self.GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult = GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult
    def hasContent_(self):
        if (
            self.GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResponse')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResponse'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult is not None:
            namespaceprefix_ = self.GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult_nsprefix_) else ''
            self.GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult':
            obj_ = ArrayOfEtiqueta.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult = obj_
            obj_.original_tagname_ = 'GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResult'
# end class GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResponse


class ArrayOfEtiqueta(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Etiqueta=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Etiqueta is None:
            self.Etiqueta = []
        else:
            self.Etiqueta = Etiqueta
        self.Etiqueta_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfEtiqueta)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfEtiqueta.subclass:
            return ArrayOfEtiqueta.subclass(*args_, **kwargs_)
        else:
            return ArrayOfEtiqueta(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Etiqueta(self):
        return self.Etiqueta
    def set_Etiqueta(self, Etiqueta):
        self.Etiqueta = Etiqueta
    def add_Etiqueta(self, value):
        self.Etiqueta.append(value)
    def insert_Etiqueta_at(self, index, value):
        self.Etiqueta.insert(index, value)
    def replace_Etiqueta_at(self, index, value):
        self.Etiqueta[index] = value
    def hasContent_(self):
        if (
            self.Etiqueta
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfEtiqueta', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfEtiqueta')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfEtiqueta':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfEtiqueta')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfEtiqueta', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfEtiqueta'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfEtiqueta', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Etiqueta_ in self.Etiqueta:
            namespaceprefix_ = self.Etiqueta_nsprefix_ + ':' if (UseCapturedNS_ and self.Etiqueta_nsprefix_) else ''
            Etiqueta_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Etiqueta', pretty_print=pretty_print)
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
        if nodeName_ == 'Etiqueta':
            obj_ = Etiqueta.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Etiqueta.append(obj_)
            obj_.original_tagname_ = 'Etiqueta'
# end class ArrayOfEtiqueta


class Etiqueta(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, NroOrden=None, NroGuia=None, DocCliente=None, Servicio=None, Bulto=None, Operativa=None, PesoTotal=None, SucursalDestino=None, SucursalOrigen=None, SucursalGuarda=None, Entrega=None, Destinatario=None, Domicilio=None, Telefono=None, Remitente=None, Observaciones=None, CodigoApertura=None, QR=None, CodeBar=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.NroOrden = NroOrden
        self.NroOrden_nsprefix_ = None
        self.NroGuia = NroGuia
        self.NroGuia_nsprefix_ = None
        self.DocCliente = DocCliente
        self.DocCliente_nsprefix_ = None
        self.Servicio = Servicio
        self.Servicio_nsprefix_ = None
        self.Bulto = Bulto
        self.Bulto_nsprefix_ = None
        self.Operativa = Operativa
        self.Operativa_nsprefix_ = None
        self.PesoTotal = PesoTotal
        self.PesoTotal_nsprefix_ = None
        self.SucursalDestino = SucursalDestino
        self.SucursalDestino_nsprefix_ = None
        self.SucursalOrigen = SucursalOrigen
        self.SucursalOrigen_nsprefix_ = None
        self.SucursalGuarda = SucursalGuarda
        self.SucursalGuarda_nsprefix_ = None
        self.Entrega = Entrega
        self.Entrega_nsprefix_ = None
        self.Destinatario = Destinatario
        self.Destinatario_nsprefix_ = None
        self.Domicilio = Domicilio
        self.Domicilio_nsprefix_ = None
        self.Telefono = Telefono
        self.Telefono_nsprefix_ = None
        self.Remitente = Remitente
        self.Remitente_nsprefix_ = None
        self.Observaciones = Observaciones
        self.Observaciones_nsprefix_ = None
        self.CodigoApertura = CodigoApertura
        self.CodigoApertura_nsprefix_ = None
        self.QR = QR
        self.QR_nsprefix_ = None
        self.CodeBar = CodeBar
        self.CodeBar_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Etiqueta)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Etiqueta.subclass:
            return Etiqueta.subclass(*args_, **kwargs_)
        else:
            return Etiqueta(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_NroOrden(self):
        return self.NroOrden
    def set_NroOrden(self, NroOrden):
        self.NroOrden = NroOrden
    def get_NroGuia(self):
        return self.NroGuia
    def set_NroGuia(self, NroGuia):
        self.NroGuia = NroGuia
    def get_DocCliente(self):
        return self.DocCliente
    def set_DocCliente(self, DocCliente):
        self.DocCliente = DocCliente
    def get_Servicio(self):
        return self.Servicio
    def set_Servicio(self, Servicio):
        self.Servicio = Servicio
    def get_Bulto(self):
        return self.Bulto
    def set_Bulto(self, Bulto):
        self.Bulto = Bulto
    def get_Operativa(self):
        return self.Operativa
    def set_Operativa(self, Operativa):
        self.Operativa = Operativa
    def get_PesoTotal(self):
        return self.PesoTotal
    def set_PesoTotal(self, PesoTotal):
        self.PesoTotal = PesoTotal
    def get_SucursalDestino(self):
        return self.SucursalDestino
    def set_SucursalDestino(self, SucursalDestino):
        self.SucursalDestino = SucursalDestino
    def get_SucursalOrigen(self):
        return self.SucursalOrigen
    def set_SucursalOrigen(self, SucursalOrigen):
        self.SucursalOrigen = SucursalOrigen
    def get_SucursalGuarda(self):
        return self.SucursalGuarda
    def set_SucursalGuarda(self, SucursalGuarda):
        self.SucursalGuarda = SucursalGuarda
    def get_Entrega(self):
        return self.Entrega
    def set_Entrega(self, Entrega):
        self.Entrega = Entrega
    def get_Destinatario(self):
        return self.Destinatario
    def set_Destinatario(self, Destinatario):
        self.Destinatario = Destinatario
    def get_Domicilio(self):
        return self.Domicilio
    def set_Domicilio(self, Domicilio):
        self.Domicilio = Domicilio
    def get_Telefono(self):
        return self.Telefono
    def set_Telefono(self, Telefono):
        self.Telefono = Telefono
    def get_Remitente(self):
        return self.Remitente
    def set_Remitente(self, Remitente):
        self.Remitente = Remitente
    def get_Observaciones(self):
        return self.Observaciones
    def set_Observaciones(self, Observaciones):
        self.Observaciones = Observaciones
    def get_CodigoApertura(self):
        return self.CodigoApertura
    def set_CodigoApertura(self, CodigoApertura):
        self.CodigoApertura = CodigoApertura
    def get_QR(self):
        return self.QR
    def set_QR(self, QR):
        self.QR = QR
    def get_CodeBar(self):
        return self.CodeBar
    def set_CodeBar(self, CodeBar):
        self.CodeBar = CodeBar
    def hasContent_(self):
        if (
            self.NroOrden is not None or
            self.NroGuia is not None or
            self.DocCliente is not None or
            self.Servicio is not None or
            self.Bulto is not None or
            self.Operativa is not None or
            self.PesoTotal is not None or
            self.SucursalDestino is not None or
            self.SucursalOrigen is not None or
            self.SucursalGuarda is not None or
            self.Entrega is not None or
            self.Destinatario is not None or
            self.Domicilio is not None or
            self.Telefono is not None or
            self.Remitente is not None or
            self.Observaciones is not None or
            self.CodigoApertura is not None or
            self.QR is not None or
            self.CodeBar is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Etiqueta', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Etiqueta')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Etiqueta':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Etiqueta')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Etiqueta', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Etiqueta'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Etiqueta', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.NroOrden is not None:
            namespaceprefix_ = self.NroOrden_nsprefix_ + ':' if (UseCapturedNS_ and self.NroOrden_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNroOrden>%s</%sNroOrden>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NroOrden), input_name='NroOrden')), namespaceprefix_ , eol_))
        if self.NroGuia is not None:
            namespaceprefix_ = self.NroGuia_nsprefix_ + ':' if (UseCapturedNS_ and self.NroGuia_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNroGuia>%s</%sNroGuia>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NroGuia), input_name='NroGuia')), namespaceprefix_ , eol_))
        if self.DocCliente is not None:
            namespaceprefix_ = self.DocCliente_nsprefix_ + ':' if (UseCapturedNS_ and self.DocCliente_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDocCliente>%s</%sDocCliente>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DocCliente), input_name='DocCliente')), namespaceprefix_ , eol_))
        if self.Servicio is not None:
            namespaceprefix_ = self.Servicio_nsprefix_ + ':' if (UseCapturedNS_ and self.Servicio_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServicio>%s</%sServicio>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Servicio), input_name='Servicio')), namespaceprefix_ , eol_))
        if self.Bulto is not None:
            namespaceprefix_ = self.Bulto_nsprefix_ + ':' if (UseCapturedNS_ and self.Bulto_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBulto>%s</%sBulto>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Bulto), input_name='Bulto')), namespaceprefix_ , eol_))
        if self.Operativa is not None:
            namespaceprefix_ = self.Operativa_nsprefix_ + ':' if (UseCapturedNS_ and self.Operativa_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOperativa>%s</%sOperativa>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Operativa), input_name='Operativa')), namespaceprefix_ , eol_))
        if self.PesoTotal is not None:
            namespaceprefix_ = self.PesoTotal_nsprefix_ + ':' if (UseCapturedNS_ and self.PesoTotal_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPesoTotal>%s</%sPesoTotal>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PesoTotal), input_name='PesoTotal')), namespaceprefix_ , eol_))
        if self.SucursalDestino is not None:
            namespaceprefix_ = self.SucursalDestino_nsprefix_ + ':' if (UseCapturedNS_ and self.SucursalDestino_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSucursalDestino>%s</%sSucursalDestino>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SucursalDestino), input_name='SucursalDestino')), namespaceprefix_ , eol_))
        if self.SucursalOrigen is not None:
            namespaceprefix_ = self.SucursalOrigen_nsprefix_ + ':' if (UseCapturedNS_ and self.SucursalOrigen_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSucursalOrigen>%s</%sSucursalOrigen>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SucursalOrigen), input_name='SucursalOrigen')), namespaceprefix_ , eol_))
        if self.SucursalGuarda is not None:
            namespaceprefix_ = self.SucursalGuarda_nsprefix_ + ':' if (UseCapturedNS_ and self.SucursalGuarda_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSucursalGuarda>%s</%sSucursalGuarda>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SucursalGuarda), input_name='SucursalGuarda')), namespaceprefix_ , eol_))
        if self.Entrega is not None:
            namespaceprefix_ = self.Entrega_nsprefix_ + ':' if (UseCapturedNS_ and self.Entrega_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEntrega>%s</%sEntrega>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Entrega), input_name='Entrega')), namespaceprefix_ , eol_))
        if self.Destinatario is not None:
            namespaceprefix_ = self.Destinatario_nsprefix_ + ':' if (UseCapturedNS_ and self.Destinatario_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDestinatario>%s</%sDestinatario>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Destinatario), input_name='Destinatario')), namespaceprefix_ , eol_))
        if self.Domicilio is not None:
            namespaceprefix_ = self.Domicilio_nsprefix_ + ':' if (UseCapturedNS_ and self.Domicilio_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDomicilio>%s</%sDomicilio>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Domicilio), input_name='Domicilio')), namespaceprefix_ , eol_))
        if self.Telefono is not None:
            namespaceprefix_ = self.Telefono_nsprefix_ + ':' if (UseCapturedNS_ and self.Telefono_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTelefono>%s</%sTelefono>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Telefono), input_name='Telefono')), namespaceprefix_ , eol_))
        if self.Remitente is not None:
            namespaceprefix_ = self.Remitente_nsprefix_ + ':' if (UseCapturedNS_ and self.Remitente_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRemitente>%s</%sRemitente>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Remitente), input_name='Remitente')), namespaceprefix_ , eol_))
        if self.Observaciones is not None:
            namespaceprefix_ = self.Observaciones_nsprefix_ + ':' if (UseCapturedNS_ and self.Observaciones_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sObservaciones>%s</%sObservaciones>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Observaciones), input_name='Observaciones')), namespaceprefix_ , eol_))
        if self.CodigoApertura is not None:
            namespaceprefix_ = self.CodigoApertura_nsprefix_ + ':' if (UseCapturedNS_ and self.CodigoApertura_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodigoApertura>%s</%sCodigoApertura>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodigoApertura), input_name='CodigoApertura')), namespaceprefix_ , eol_))
        if self.QR is not None:
            namespaceprefix_ = self.QR_nsprefix_ + ':' if (UseCapturedNS_ and self.QR_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sQR>%s</%sQR>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.QR), input_name='QR')), namespaceprefix_ , eol_))
        if self.CodeBar is not None:
            namespaceprefix_ = self.CodeBar_nsprefix_ + ':' if (UseCapturedNS_ and self.CodeBar_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCodeBar>%s</%sCodeBar>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CodeBar), input_name='CodeBar')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'NroOrden':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NroOrden')
            value_ = self.gds_validate_string(value_, node, 'NroOrden')
            self.NroOrden = value_
            self.NroOrden_nsprefix_ = child_.prefix
        elif nodeName_ == 'NroGuia':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NroGuia')
            value_ = self.gds_validate_string(value_, node, 'NroGuia')
            self.NroGuia = value_
            self.NroGuia_nsprefix_ = child_.prefix
        elif nodeName_ == 'DocCliente':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DocCliente')
            value_ = self.gds_validate_string(value_, node, 'DocCliente')
            self.DocCliente = value_
            self.DocCliente_nsprefix_ = child_.prefix
        elif nodeName_ == 'Servicio':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Servicio')
            value_ = self.gds_validate_string(value_, node, 'Servicio')
            self.Servicio = value_
            self.Servicio_nsprefix_ = child_.prefix
        elif nodeName_ == 'Bulto':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Bulto')
            value_ = self.gds_validate_string(value_, node, 'Bulto')
            self.Bulto = value_
            self.Bulto_nsprefix_ = child_.prefix
        elif nodeName_ == 'Operativa':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Operativa')
            value_ = self.gds_validate_string(value_, node, 'Operativa')
            self.Operativa = value_
            self.Operativa_nsprefix_ = child_.prefix
        elif nodeName_ == 'PesoTotal':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PesoTotal')
            value_ = self.gds_validate_string(value_, node, 'PesoTotal')
            self.PesoTotal = value_
            self.PesoTotal_nsprefix_ = child_.prefix
        elif nodeName_ == 'SucursalDestino':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SucursalDestino')
            value_ = self.gds_validate_string(value_, node, 'SucursalDestino')
            self.SucursalDestino = value_
            self.SucursalDestino_nsprefix_ = child_.prefix
        elif nodeName_ == 'SucursalOrigen':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SucursalOrigen')
            value_ = self.gds_validate_string(value_, node, 'SucursalOrigen')
            self.SucursalOrigen = value_
            self.SucursalOrigen_nsprefix_ = child_.prefix
        elif nodeName_ == 'SucursalGuarda':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SucursalGuarda')
            value_ = self.gds_validate_string(value_, node, 'SucursalGuarda')
            self.SucursalGuarda = value_
            self.SucursalGuarda_nsprefix_ = child_.prefix
        elif nodeName_ == 'Entrega':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Entrega')
            value_ = self.gds_validate_string(value_, node, 'Entrega')
            self.Entrega = value_
            self.Entrega_nsprefix_ = child_.prefix
        elif nodeName_ == 'Destinatario':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Destinatario')
            value_ = self.gds_validate_string(value_, node, 'Destinatario')
            self.Destinatario = value_
            self.Destinatario_nsprefix_ = child_.prefix
        elif nodeName_ == 'Domicilio':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Domicilio')
            value_ = self.gds_validate_string(value_, node, 'Domicilio')
            self.Domicilio = value_
            self.Domicilio_nsprefix_ = child_.prefix
        elif nodeName_ == 'Telefono':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Telefono')
            value_ = self.gds_validate_string(value_, node, 'Telefono')
            self.Telefono = value_
            self.Telefono_nsprefix_ = child_.prefix
        elif nodeName_ == 'Remitente':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Remitente')
            value_ = self.gds_validate_string(value_, node, 'Remitente')
            self.Remitente = value_
            self.Remitente_nsprefix_ = child_.prefix
        elif nodeName_ == 'Observaciones':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Observaciones')
            value_ = self.gds_validate_string(value_, node, 'Observaciones')
            self.Observaciones = value_
            self.Observaciones_nsprefix_ = child_.prefix
        elif nodeName_ == 'CodigoApertura':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodigoApertura')
            value_ = self.gds_validate_string(value_, node, 'CodigoApertura')
            self.CodigoApertura = value_
            self.CodigoApertura_nsprefix_ = child_.prefix
        elif nodeName_ == 'QR':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'QR')
            value_ = self.gds_validate_string(value_, node, 'QR')
            self.QR = value_
            self.QR_nsprefix_ = child_.prefix
        elif nodeName_ == 'CodeBar':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CodeBar')
            value_ = self.gds_validate_string(value_, node, 'CodeBar')
            self.CodeBar = value_
            self.CodeBar_nsprefix_ = child_.prefix
# end class Etiqueta


class DataSet(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, schema=None, anytypeobjs_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.schema = schema
        self.schema_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DataSet)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DataSet.subclass:
            return DataSet.subclass(*args_, **kwargs_)
        else:
            return DataSet(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_schema(self):
        return self.schema
    def set_schema(self, schema):
        self.schema = schema
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def hasContent_(self):
        if (
            self.schema is not None or
            self.anytypeobjs_ is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DataSet', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DataSet')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DataSet':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DataSet')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DataSet', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DataSet'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DataSet', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.schema is not None:
            namespaceprefix_ = self.schema_nsprefix_ + ':' if (UseCapturedNS_ and self.schema_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sschema>%s</%sschema>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.schema), input_name='schema')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == 'schema':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'schema')
            value_ = self.gds_validate_string(value_, node, 'schema')
            self.schema = value_
            self.schema_nsprefix_ = child_.prefix
        else:
            content_ = self.gds_build_any(child_, 'DataSet')
            self.set_anytypeobjs_(content_)
# end class DataSet


class List_EnviosResultType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, schema=None, anytypeobjs_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.schema = schema
        self.schema_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, List_EnviosResultType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if List_EnviosResultType.subclass:
            return List_EnviosResultType.subclass(*args_, **kwargs_)
        else:
            return List_EnviosResultType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_schema(self):
        return self.schema
    def set_schema(self, schema):
        self.schema = schema
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def hasContent_(self):
        if (
            self.schema is not None or
            self.anytypeobjs_ is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='List_EnviosResultType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('List_EnviosResultType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'List_EnviosResultType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='List_EnviosResultType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='List_EnviosResultType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='List_EnviosResultType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='List_EnviosResultType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.schema is not None:
            namespaceprefix_ = self.schema_nsprefix_ + ':' if (UseCapturedNS_ and self.schema_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sschema>%s</%sschema>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.schema), input_name='schema')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == 'schema':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'schema')
            value_ = self.gds_validate_string(value_, node, 'schema')
            self.schema = value_
            self.schema_nsprefix_ = child_.prefix
        else:
            content_ = self.gds_build_any(child_, 'List_EnviosResultType')
            self.set_anytypeobjs_(content_)
# end class List_EnviosResultType


class Tracking_PiezaResultType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, schema=None, anytypeobjs_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.schema = schema
        self.schema_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Tracking_PiezaResultType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Tracking_PiezaResultType.subclass:
            return Tracking_PiezaResultType.subclass(*args_, **kwargs_)
        else:
            return Tracking_PiezaResultType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_schema(self):
        return self.schema
    def set_schema(self, schema):
        self.schema = schema
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def hasContent_(self):
        if (
            self.schema is not None or
            self.anytypeobjs_ is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Tracking_PiezaResultType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Tracking_PiezaResultType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Tracking_PiezaResultType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Tracking_PiezaResultType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Tracking_PiezaResultType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Tracking_PiezaResultType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Tracking_PiezaResultType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.schema is not None:
            namespaceprefix_ = self.schema_nsprefix_ + ':' if (UseCapturedNS_ and self.schema_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sschema>%s</%sschema>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.schema), input_name='schema')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == 'schema':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'schema')
            value_ = self.gds_validate_string(value_, node, 'schema')
            self.schema = value_
            self.schema_nsprefix_ = child_.prefix
        else:
            content_ = self.gds_build_any(child_, 'Tracking_PiezaResultType')
            self.set_anytypeobjs_(content_)
# end class Tracking_PiezaResultType


class Tracking_OrdenRetiroResultType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, schema=None, anytypeobjs_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.schema = schema
        self.schema_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Tracking_OrdenRetiroResultType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Tracking_OrdenRetiroResultType.subclass:
            return Tracking_OrdenRetiroResultType.subclass(*args_, **kwargs_)
        else:
            return Tracking_OrdenRetiroResultType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_schema(self):
        return self.schema
    def set_schema(self, schema):
        self.schema = schema
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def hasContent_(self):
        if (
            self.schema is not None or
            self.anytypeobjs_ is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Tracking_OrdenRetiroResultType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Tracking_OrdenRetiroResultType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Tracking_OrdenRetiroResultType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Tracking_OrdenRetiroResultType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Tracking_OrdenRetiroResultType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Tracking_OrdenRetiroResultType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Tracking_OrdenRetiroResultType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.schema is not None:
            namespaceprefix_ = self.schema_nsprefix_ + ':' if (UseCapturedNS_ and self.schema_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sschema>%s</%sschema>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.schema), input_name='schema')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == 'schema':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'schema')
            value_ = self.gds_validate_string(value_, node, 'schema')
            self.schema = value_
            self.schema_nsprefix_ = child_.prefix
        else:
            content_ = self.gds_build_any(child_, 'Tracking_OrdenRetiroResultType')
            self.set_anytypeobjs_(content_)
# end class Tracking_OrdenRetiroResultType


class Tarifar_Envio_CorporativoResultType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, schema=None, anytypeobjs_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.schema = schema
        self.schema_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Tarifar_Envio_CorporativoResultType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Tarifar_Envio_CorporativoResultType.subclass:
            return Tarifar_Envio_CorporativoResultType.subclass(*args_, **kwargs_)
        else:
            return Tarifar_Envio_CorporativoResultType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_schema(self):
        return self.schema
    def set_schema(self, schema):
        self.schema = schema
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def hasContent_(self):
        if (
            self.schema is not None or
            self.anytypeobjs_ is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Tarifar_Envio_CorporativoResultType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Tarifar_Envio_CorporativoResultType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Tarifar_Envio_CorporativoResultType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Tarifar_Envio_CorporativoResultType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Tarifar_Envio_CorporativoResultType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Tarifar_Envio_CorporativoResultType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Tarifar_Envio_CorporativoResultType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.schema is not None:
            namespaceprefix_ = self.schema_nsprefix_ + ':' if (UseCapturedNS_ and self.schema_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sschema>%s</%sschema>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.schema), input_name='schema')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == 'schema':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'schema')
            value_ = self.gds_validate_string(value_, node, 'schema')
            self.schema = value_
            self.schema_nsprefix_ = child_.prefix
        else:
            content_ = self.gds_build_any(child_, 'Tarifar_Envio_CorporativoResultType')
            self.set_anytypeobjs_(content_)
# end class Tarifar_Envio_CorporativoResultType


class AnularOrdenGeneradaResultType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, schema=None, anytypeobjs_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.schema = schema
        self.schema_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AnularOrdenGeneradaResultType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AnularOrdenGeneradaResultType.subclass:
            return AnularOrdenGeneradaResultType.subclass(*args_, **kwargs_)
        else:
            return AnularOrdenGeneradaResultType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_schema(self):
        return self.schema
    def set_schema(self, schema):
        self.schema = schema
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def hasContent_(self):
        if (
            self.schema is not None or
            self.anytypeobjs_ is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AnularOrdenGeneradaResultType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AnularOrdenGeneradaResultType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AnularOrdenGeneradaResultType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AnularOrdenGeneradaResultType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AnularOrdenGeneradaResultType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AnularOrdenGeneradaResultType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AnularOrdenGeneradaResultType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.schema is not None:
            namespaceprefix_ = self.schema_nsprefix_ + ':' if (UseCapturedNS_ and self.schema_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sschema>%s</%sschema>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.schema), input_name='schema')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == 'schema':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'schema')
            value_ = self.gds_validate_string(value_, node, 'schema')
            self.schema = value_
            self.schema_nsprefix_ = child_.prefix
        else:
            content_ = self.gds_build_any(child_, 'AnularOrdenGeneradaResultType')
            self.set_anytypeobjs_(content_)
# end class AnularOrdenGeneradaResultType


class GetEnviosUltimoEstadoResultType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, schema=None, anytypeobjs_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.schema = schema
        self.schema_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetEnviosUltimoEstadoResultType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetEnviosUltimoEstadoResultType.subclass:
            return GetEnviosUltimoEstadoResultType.subclass(*args_, **kwargs_)
        else:
            return GetEnviosUltimoEstadoResultType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_schema(self):
        return self.schema
    def set_schema(self, schema):
        self.schema = schema
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def hasContent_(self):
        if (
            self.schema is not None or
            self.anytypeobjs_ is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetEnviosUltimoEstadoResultType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetEnviosUltimoEstadoResultType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetEnviosUltimoEstadoResultType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetEnviosUltimoEstadoResultType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetEnviosUltimoEstadoResultType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetEnviosUltimoEstadoResultType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetEnviosUltimoEstadoResultType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.schema is not None:
            namespaceprefix_ = self.schema_nsprefix_ + ':' if (UseCapturedNS_ and self.schema_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sschema>%s</%sschema>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.schema), input_name='schema')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == 'schema':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'schema')
            value_ = self.gds_validate_string(value_, node, 'schema')
            self.schema = value_
            self.schema_nsprefix_ = child_.prefix
        else:
            content_ = self.gds_build_any(child_, 'GetEnviosUltimoEstadoResultType')
            self.set_anytypeobjs_(content_)
# end class GetEnviosUltimoEstadoResultType


class IngresoORResultType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, schema=None, anytypeobjs_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.schema = schema
        self.schema_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, IngresoORResultType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if IngresoORResultType.subclass:
            return IngresoORResultType.subclass(*args_, **kwargs_)
        else:
            return IngresoORResultType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_schema(self):
        return self.schema
    def set_schema(self, schema):
        self.schema = schema
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def hasContent_(self):
        if (
            self.schema is not None or
            self.anytypeobjs_ is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='IngresoORResultType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('IngresoORResultType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'IngresoORResultType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='IngresoORResultType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='IngresoORResultType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='IngresoORResultType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='IngresoORResultType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.schema is not None:
            namespaceprefix_ = self.schema_nsprefix_ + ':' if (UseCapturedNS_ and self.schema_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sschema>%s</%sschema>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.schema), input_name='schema')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == 'schema':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'schema')
            value_ = self.gds_validate_string(value_, node, 'schema')
            self.schema = value_
            self.schema_nsprefix_ = child_.prefix
        else:
            content_ = self.gds_build_any(child_, 'IngresoORResultType')
            self.set_anytypeobjs_(content_)
# end class IngresoORResultType


class GetCentroCostoPorOperativaResultType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, schema=None, anytypeobjs_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.schema = schema
        self.schema_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetCentroCostoPorOperativaResultType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetCentroCostoPorOperativaResultType.subclass:
            return GetCentroCostoPorOperativaResultType.subclass(*args_, **kwargs_)
        else:
            return GetCentroCostoPorOperativaResultType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_schema(self):
        return self.schema
    def set_schema(self, schema):
        self.schema = schema
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def hasContent_(self):
        if (
            self.schema is not None or
            self.anytypeobjs_ is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentroCostoPorOperativaResultType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetCentroCostoPorOperativaResultType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetCentroCostoPorOperativaResultType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetCentroCostoPorOperativaResultType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetCentroCostoPorOperativaResultType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetCentroCostoPorOperativaResultType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentroCostoPorOperativaResultType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.schema is not None:
            namespaceprefix_ = self.schema_nsprefix_ + ':' if (UseCapturedNS_ and self.schema_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sschema>%s</%sschema>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.schema), input_name='schema')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == 'schema':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'schema')
            value_ = self.gds_validate_string(value_, node, 'schema')
            self.schema = value_
            self.schema_nsprefix_ = child_.prefix
        else:
            content_ = self.gds_build_any(child_, 'GetCentroCostoPorOperativaResultType')
            self.set_anytypeobjs_(content_)
# end class GetCentroCostoPorOperativaResultType


class GetCentrosImposicionResultType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, schema=None, anytypeobjs_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.schema = schema
        self.schema_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetCentrosImposicionResultType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetCentrosImposicionResultType.subclass:
            return GetCentrosImposicionResultType.subclass(*args_, **kwargs_)
        else:
            return GetCentrosImposicionResultType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_schema(self):
        return self.schema
    def set_schema(self, schema):
        self.schema = schema
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def hasContent_(self):
        if (
            self.schema is not None or
            self.anytypeobjs_ is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionResultType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetCentrosImposicionResultType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetCentrosImposicionResultType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetCentrosImposicionResultType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetCentrosImposicionResultType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetCentrosImposicionResultType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionResultType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.schema is not None:
            namespaceprefix_ = self.schema_nsprefix_ + ':' if (UseCapturedNS_ and self.schema_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sschema>%s</%sschema>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.schema), input_name='schema')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == 'schema':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'schema')
            value_ = self.gds_validate_string(value_, node, 'schema')
            self.schema = value_
            self.schema_nsprefix_ = child_.prefix
        else:
            content_ = self.gds_build_any(child_, 'GetCentrosImposicionResultType')
            self.set_anytypeobjs_(content_)
# end class GetCentrosImposicionResultType


class GetELockerOCAResultType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, schema=None, anytypeobjs_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.schema = schema
        self.schema_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetELockerOCAResultType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetELockerOCAResultType.subclass:
            return GetELockerOCAResultType.subclass(*args_, **kwargs_)
        else:
            return GetELockerOCAResultType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_schema(self):
        return self.schema
    def set_schema(self, schema):
        self.schema = schema
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def hasContent_(self):
        if (
            self.schema is not None or
            self.anytypeobjs_ is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetELockerOCAResultType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetELockerOCAResultType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetELockerOCAResultType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetELockerOCAResultType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetELockerOCAResultType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetELockerOCAResultType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetELockerOCAResultType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.schema is not None:
            namespaceprefix_ = self.schema_nsprefix_ + ':' if (UseCapturedNS_ and self.schema_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sschema>%s</%sschema>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.schema), input_name='schema')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == 'schema':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'schema')
            value_ = self.gds_validate_string(value_, node, 'schema')
            self.schema = value_
            self.schema_nsprefix_ = child_.prefix
        else:
            content_ = self.gds_build_any(child_, 'GetELockerOCAResultType')
            self.set_anytypeobjs_(content_)
# end class GetELockerOCAResultType


class GetCentrosImposicionAdmisionResultType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, schema=None, anytypeobjs_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.schema = schema
        self.schema_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetCentrosImposicionAdmisionResultType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetCentrosImposicionAdmisionResultType.subclass:
            return GetCentrosImposicionAdmisionResultType.subclass(*args_, **kwargs_)
        else:
            return GetCentrosImposicionAdmisionResultType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_schema(self):
        return self.schema
    def set_schema(self, schema):
        self.schema = schema
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def hasContent_(self):
        if (
            self.schema is not None or
            self.anytypeobjs_ is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionAdmisionResultType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetCentrosImposicionAdmisionResultType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetCentrosImposicionAdmisionResultType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetCentrosImposicionAdmisionResultType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetCentrosImposicionAdmisionResultType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetCentrosImposicionAdmisionResultType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionAdmisionResultType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.schema is not None:
            namespaceprefix_ = self.schema_nsprefix_ + ':' if (UseCapturedNS_ and self.schema_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sschema>%s</%sschema>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.schema), input_name='schema')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == 'schema':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'schema')
            value_ = self.gds_validate_string(value_, node, 'schema')
            self.schema = value_
            self.schema_nsprefix_ = child_.prefix
        else:
            content_ = self.gds_build_any(child_, 'GetCentrosImposicionAdmisionResultType')
            self.set_anytypeobjs_(content_)
# end class GetCentrosImposicionAdmisionResultType


class GetServiciosDeCentrosImposicionResultType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.anytypeobjs_ = anytypeobjs_
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
                CurrentSubclassModule_, GetServiciosDeCentrosImposicionResultType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetServiciosDeCentrosImposicionResultType.subclass:
            return GetServiciosDeCentrosImposicionResultType.subclass(*args_, **kwargs_)
        else:
            return GetServiciosDeCentrosImposicionResultType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def hasContent_(self):
        if (
            self.anytypeobjs_ is not None or
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_) or
            self.content_
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetServiciosDeCentrosImposicionResultType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetServiciosDeCentrosImposicionResultType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetServiciosDeCentrosImposicionResultType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetServiciosDeCentrosImposicionResultType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetServiciosDeCentrosImposicionResultType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetServiciosDeCentrosImposicionResultType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetServiciosDeCentrosImposicionResultType', fromsubclass_=False, pretty_print=True):
        if not fromsubclass_:
            for item_ in self.content_:
                item_.export(outfile, level, item_.name, namespaceprefix_, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == '':
            obj_ = __ANY__.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, '', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_'):
              self.add_(obj_.value)
            elif hasattr(self, 'set_'):
              self.set_(obj_.value)
        if not fromsubclass_ and child_.tail is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.tail)
            self.content_.append(obj_)
# end class GetServiciosDeCentrosImposicionResultType


class TrackingEnvio_EstadoActualResultType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.anytypeobjs_ = anytypeobjs_
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
                CurrentSubclassModule_, TrackingEnvio_EstadoActualResultType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TrackingEnvio_EstadoActualResultType.subclass:
            return TrackingEnvio_EstadoActualResultType.subclass(*args_, **kwargs_)
        else:
            return TrackingEnvio_EstadoActualResultType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def hasContent_(self):
        if (
            self.anytypeobjs_ is not None or
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_) or
            self.content_
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackingEnvio_EstadoActualResultType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TrackingEnvio_EstadoActualResultType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TrackingEnvio_EstadoActualResultType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TrackingEnvio_EstadoActualResultType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TrackingEnvio_EstadoActualResultType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TrackingEnvio_EstadoActualResultType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TrackingEnvio_EstadoActualResultType', fromsubclass_=False, pretty_print=True):
        if not fromsubclass_:
            for item_ in self.content_:
                item_.export(outfile, level, item_.name, namespaceprefix_, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == '':
            obj_ = __ANY__.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, '', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_'):
              self.add_(obj_.value)
            elif hasattr(self, 'set_'):
              self.set_(obj_.value)
        if not fromsubclass_ and child_.tail is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.tail)
            self.content_.append(obj_)
# end class TrackingEnvio_EstadoActualResultType


class GetProvinciasResultType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.anytypeobjs_ = anytypeobjs_
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
                CurrentSubclassModule_, GetProvinciasResultType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetProvinciasResultType.subclass:
            return GetProvinciasResultType.subclass(*args_, **kwargs_)
        else:
            return GetProvinciasResultType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def hasContent_(self):
        if (
            self.anytypeobjs_ is not None or
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_) or
            self.content_
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetProvinciasResultType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetProvinciasResultType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetProvinciasResultType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetProvinciasResultType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetProvinciasResultType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetProvinciasResultType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetProvinciasResultType', fromsubclass_=False, pretty_print=True):
        if not fromsubclass_:
            for item_ in self.content_:
                item_.export(outfile, level, item_.name, namespaceprefix_, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == '':
            obj_ = __ANY__.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, '', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_'):
              self.add_(obj_.value)
            elif hasattr(self, 'set_'):
              self.set_(obj_.value)
        if not fromsubclass_ and child_.tail is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.tail)
            self.content_.append(obj_)
# end class GetProvinciasResultType


class GetLocalidadesByProvinciaResultType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.anytypeobjs_ = anytypeobjs_
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
                CurrentSubclassModule_, GetLocalidadesByProvinciaResultType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetLocalidadesByProvinciaResultType.subclass:
            return GetLocalidadesByProvinciaResultType.subclass(*args_, **kwargs_)
        else:
            return GetLocalidadesByProvinciaResultType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def hasContent_(self):
        if (
            self.anytypeobjs_ is not None or
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_) or
            self.content_
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLocalidadesByProvinciaResultType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetLocalidadesByProvinciaResultType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetLocalidadesByProvinciaResultType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetLocalidadesByProvinciaResultType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetLocalidadesByProvinciaResultType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetLocalidadesByProvinciaResultType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLocalidadesByProvinciaResultType', fromsubclass_=False, pretty_print=True):
        if not fromsubclass_:
            for item_ in self.content_:
                item_.export(outfile, level, item_.name, namespaceprefix_, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == '':
            obj_ = __ANY__.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, '', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_'):
              self.add_(obj_.value)
            elif hasattr(self, 'set_'):
              self.set_(obj_.value)
        if not fromsubclass_ and child_.tail is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.tail)
            self.content_.append(obj_)
# end class GetLocalidadesByProvinciaResultType


class GetServiciosDeCentrosImposicion_xProvinciaResultType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, anytypeobjs_=None, valueOf_=None, mixedclass_=None, content_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.anytypeobjs_ = anytypeobjs_
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
                CurrentSubclassModule_, GetServiciosDeCentrosImposicion_xProvinciaResultType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetServiciosDeCentrosImposicion_xProvinciaResultType.subclass:
            return GetServiciosDeCentrosImposicion_xProvinciaResultType.subclass(*args_, **kwargs_)
        else:
            return GetServiciosDeCentrosImposicion_xProvinciaResultType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def hasContent_(self):
        if (
            self.anytypeobjs_ is not None or
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_) or
            self.content_
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetServiciosDeCentrosImposicion_xProvinciaResultType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetServiciosDeCentrosImposicion_xProvinciaResultType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetServiciosDeCentrosImposicion_xProvinciaResultType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetServiciosDeCentrosImposicion_xProvinciaResultType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetServiciosDeCentrosImposicion_xProvinciaResultType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetServiciosDeCentrosImposicion_xProvinciaResultType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetServiciosDeCentrosImposicion_xProvinciaResultType', fromsubclass_=False, pretty_print=True):
        if not fromsubclass_:
            for item_ in self.content_:
                item_.export(outfile, level, item_.name, namespaceprefix_, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == '':
            obj_ = __ANY__.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            obj_ = self.mixedclass_(MixedContainer.CategoryComplex,
                MixedContainer.TypeNone, '', obj_)
            self.content_.append(obj_)
            if hasattr(self, 'add_'):
              self.add_(obj_.value)
            elif hasattr(self, 'set_'):
              self.set_(obj_.value)
        if not fromsubclass_ and child_.tail is not None:
            obj_ = self.mixedclass_(MixedContainer.CategoryText,
                MixedContainer.TypeNone, '', child_.tail)
            self.content_.append(obj_)
# end class GetServiciosDeCentrosImposicion_xProvinciaResultType


class GetCentrosImposicionPorCPResultType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, schema=None, anytypeobjs_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.schema = schema
        self.schema_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetCentrosImposicionPorCPResultType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetCentrosImposicionPorCPResultType.subclass:
            return GetCentrosImposicionPorCPResultType.subclass(*args_, **kwargs_)
        else:
            return GetCentrosImposicionPorCPResultType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_schema(self):
        return self.schema
    def set_schema(self, schema):
        self.schema = schema
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def hasContent_(self):
        if (
            self.schema is not None or
            self.anytypeobjs_ is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionPorCPResultType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetCentrosImposicionPorCPResultType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetCentrosImposicionPorCPResultType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetCentrosImposicionPorCPResultType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetCentrosImposicionPorCPResultType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetCentrosImposicionPorCPResultType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionPorCPResultType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.schema is not None:
            namespaceprefix_ = self.schema_nsprefix_ + ':' if (UseCapturedNS_ and self.schema_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sschema>%s</%sschema>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.schema), input_name='schema')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == 'schema':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'schema')
            value_ = self.gds_validate_string(value_, node, 'schema')
            self.schema = value_
            self.schema_nsprefix_ = child_.prefix
        else:
            content_ = self.gds_build_any(child_, 'GetCentrosImposicionPorCPResultType')
            self.set_anytypeobjs_(content_)
# end class GetCentrosImposicionPorCPResultType


class GetCentrosImposicionAdmisionPorCPResultType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, schema=None, anytypeobjs_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.schema = schema
        self.schema_nsprefix_ = None
        self.anytypeobjs_ = anytypeobjs_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetCentrosImposicionAdmisionPorCPResultType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetCentrosImposicionAdmisionPorCPResultType.subclass:
            return GetCentrosImposicionAdmisionPorCPResultType.subclass(*args_, **kwargs_)
        else:
            return GetCentrosImposicionAdmisionPorCPResultType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_schema(self):
        return self.schema
    def set_schema(self, schema):
        self.schema = schema
    def get_anytypeobjs_(self): return self.anytypeobjs_
    def set_anytypeobjs_(self, anytypeobjs_): self.anytypeobjs_ = anytypeobjs_
    def hasContent_(self):
        if (
            self.schema is not None or
            self.anytypeobjs_ is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionAdmisionPorCPResultType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetCentrosImposicionAdmisionPorCPResultType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetCentrosImposicionAdmisionPorCPResultType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetCentrosImposicionAdmisionPorCPResultType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_, ))
            self.exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetCentrosImposicionAdmisionPorCPResultType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetCentrosImposicionAdmisionPorCPResultType'):
        pass
    def exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetCentrosImposicionAdmisionPorCPResultType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.schema is not None:
            namespaceprefix_ = self.schema_nsprefix_ + ':' if (UseCapturedNS_ and self.schema_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sschema>%s</%sschema>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.schema), input_name='schema')), namespaceprefix_ , eol_))
        if not fromsubclass_:
            if self.anytypeobjs_ is not None:
                content_ = self.anytypeobjs_
                outfile.write(content_)
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
        if nodeName_ == 'schema':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'schema')
            value_ = self.gds_validate_string(value_, node, 'schema')
            self.schema = value_
            self.schema_nsprefix_ = child_.prefix
        else:
            content_ = self.gds_build_any(child_, 'GetCentrosImposicionAdmisionPorCPResultType')
            self.set_anytypeobjs_(content_)
# end class GetCentrosImposicionAdmisionPorCPResultType


GDSClassesMapping = {
    'ArrayOfEtiqueta': ArrayOfEtiqueta,
    'ArrayOfString': ArrayOfString,
    'EtiquetasPDFResponse': EtiquetasPDFResponse,
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
        rootTag = 'List_Envios'
        rootClass = List_Envios
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
        rootTag = 'List_Envios'
        rootClass = List_Envios
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
        rootTag = 'List_Envios'
        rootClass = List_Envios
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:tns="#Oca_Express_Pak"')
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
        rootTag = 'List_Envios'
        rootClass = List_Envios
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from services import *\n\n')
        sys.stdout.write('import services as model_\n\n')
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
NamespaceToDefMappings_ = {'#Oca_Express_Pak': [('ArrayOfString', './schemas/services.xsd', 'CT'),
                      ('EtiquetasPDFResponse', './schemas/services.xsd', 'CT'),
                      ('ArrayOfEtiqueta', './schemas/services.xsd', 'CT'),
                      ('Etiqueta', './schemas/services.xsd', 'CT')]}

__all__ = [
    "AnularOrdenGenerada",
    "AnularOrdenGeneradaResponse",
    "AnularOrdenGeneradaResultType",
    "ArrayOfEtiqueta",
    "ArrayOfString",
    "DataSet",
    "Etiqueta",
    "EtiquetasPDFResponse",
    "GenerarConsolidacionDeOrdenesDeRetiro",
    "GenerarConsolidacionDeOrdenesDeRetiroResponse",
    "GenerateListQrPorEnvio",
    "GenerateListQrPorEnvioResponse",
    "GenerateQRParaPaquetes",
    "GenerateQRParaPaquetesResponse",
    "GenerateQrByOrdenDeRetiro",
    "GenerateQrByOrdenDeRetiroResponse",
    "GetCSSDeEtiquetasPorOrdenOrNumeroEnvio",
    "GetCSSDeEtiquetasPorOrdenOrNumeroEnvioResponse",
    "GetCentroCostoPorOperativa",
    "GetCentroCostoPorOperativaResponse",
    "GetCentroCostoPorOperativaResultType",
    "GetCentrosImposicion",
    "GetCentrosImposicionAdmision",
    "GetCentrosImposicionAdmisionPorCP",
    "GetCentrosImposicionAdmisionPorCPResponse",
    "GetCentrosImposicionAdmisionPorCPResultType",
    "GetCentrosImposicionAdmisionResponse",
    "GetCentrosImposicionAdmisionResultType",
    "GetCentrosImposicionPorCP",
    "GetCentrosImposicionPorCPResponse",
    "GetCentrosImposicionPorCPResultType",
    "GetCentrosImposicionResponse",
    "GetCentrosImposicionResultType",
    "GetDatosDeEtiquetasPorOrdenOrNumeroEnvio",
    "GetDatosDeEtiquetasPorOrdenOrNumeroEnvioResponse",
    "GetDivDeEtiquetaByIdPieza",
    "GetDivDeEtiquetaByIdPiezaResponse",
    "GetDivDeEtiquetasPorOrdenOrNumeroEnvio",
    "GetDivDeEtiquetasPorOrdenOrNumeroEnvioResponse",
    "GetELockerOCA",
    "GetELockerOCAResponse",
    "GetELockerOCAResultType",
    "GetEnviosUltimoEstado",
    "GetEnviosUltimoEstadoResponse",
    "GetEnviosUltimoEstadoResultType",
    "GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvio",
    "GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadora",
    "GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioParaEtiquetadoraResponse",
    "GetHtmlDeEtiquetasLockersPorOrdenOrNumeroEnvioResponse",
    "GetHtmlDeEtiquetasPorOrdenOrNumeroEnvio",
    "GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadora",
    "GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioParaEtiquetadoraResponse",
    "GetHtmlDeEtiquetasPorOrdenOrNumeroEnvioResponse",
    "GetHtmlDeEtiquetasPorOrdenes",
    "GetHtmlDeEtiquetasPorOrdenesResponse",
    "GetLocalidadesByProvincia",
    "GetLocalidadesByProvinciaResponse",
    "GetLocalidadesByProvinciaResultType",
    "GetPdfDeEtiquetasPorOrdenOrNumeroEnvio",
    "GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidas",
    "GetPdfDeEtiquetasPorOrdenOrNumeroEnvioAdidasResponse",
    "GetPdfDeEtiquetasPorOrdenOrNumeroEnvioResponse",
    "GetProvincias",
    "GetProvinciasResponse",
    "GetProvinciasResultType",
    "GetServiciosDeCentrosImposicion",
    "GetServiciosDeCentrosImposicionResponse",
    "GetServiciosDeCentrosImposicionResultType",
    "GetServiciosDeCentrosImposicion_xProvincia",
    "GetServiciosDeCentrosImposicion_xProvinciaResponse",
    "GetServiciosDeCentrosImposicion_xProvinciaResultType",
    "IngresoOR",
    "IngresoORResponse",
    "IngresoORResultType",
    "List_Envios",
    "List_EnviosResponse",
    "List_EnviosResultType",
    "Tarifar_Envio_Corporativo",
    "Tarifar_Envio_CorporativoResponse",
    "Tarifar_Envio_CorporativoResultType",
    "TrackingEnvio_EstadoActual",
    "TrackingEnvio_EstadoActualResponse",
    "TrackingEnvio_EstadoActualResultType",
    "Tracking_OrdenRetiro",
    "Tracking_OrdenRetiroResponse",
    "Tracking_OrdenRetiroResultType",
    "Tracking_Pieza",
    "Tracking_PiezaResponse",
    "Tracking_PiezaResultType"
]
