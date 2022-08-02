#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Mon Aug  1 09:54:50 2022 by generateDS.py version 2.40.13.
# Python 3.8.7 (v3.8.7:6503f05dd5, Dec 21 2020, 12:45:15)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './ups_lib/freight_rate_web_service_schema.py')
#
# Command line arguments:
#   ./schemas/FreightRateWebServiceSchema.xsd
#
# Command line:
#   /Users/danielk/Documents/karrio/karrio/.venv/karrio/bin/generateDS --no-namespace-defs -o "./ups_lib/freight_rate_web_service_schema.py" ./schemas/FreightRateWebServiceSchema.xsd
#
# Current working directory (os.getcwd()):
#   ups
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
from lxml import etree as etree_


Validate_simpletypes_ = True
SaveElementTreeNode = True
TagNamePrefix = ""
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
# "xsi:type" attribute value.  See the _exportAttributes method of
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
    try:
        from generatedssupersuper import GeneratedsSuperSuper
    except ModulenotfoundExp_ as exp:
        class GeneratedsSuperSuper(object):
            pass
    
    class GeneratedsSuper(GeneratedsSuperSuper):
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
        def __str__(self):
            settings = {
                'str_pretty_print': True,
                'str_indent_level': 0,
                'str_namespaceprefix': '',
                'str_name': self.__class__.__name__,
                'str_namespacedefs': '',
            }
            for n in settings:
                if hasattr(self, n):
                    settings[n] = getattr(self, n)
            if sys.version_info.major == 2:
                from StringIO import StringIO
            else:
                from io import StringIO
            output = StringIO()
            self.export(
                output,
                settings['str_indent_level'],
                pretty_print=settings['str_pretty_print'],
                namespaceprefix_=settings['str_namespaceprefix'],
                name_=settings['str_name'],
                namespacedef_=settings['str_namespacedefs']
            )
            strval = output.getvalue()
            output.close()
            return strval
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
            return base64.b64encode(input_data).decode('ascii')
        def gds_validate_base64(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_integer(self, input_data, input_name=''):
            return '%d' % int(input_data)
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
            return ('%.15f' % float(input_data)).rstrip('0')
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
            input_data = input_data.strip()
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
            target = str(target)
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
    s1 = s1.replace('\n', '&#10;')
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
    def to_etree(self, element, mapping_=None, reverse_mapping_=None, nsmap_=None):
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
    def to_etree_simple(self, mapping_=None, reverse_mapping_=None, nsmap_=None):
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


class FreightRateRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Request=None, ShipFrom=None, ShipTo=None, PaymentInformation=None, Service=None, HandlingUnitOne=None, HandlingUnitTwo=None, Commodity=None, ShipmentServiceOptions=None, PickupRequest=None, AlternateRateOptions=None, GFPOptions=None, AccountType=None, ShipmentTotalWeight=None, HandlingUnitWeight=None, AdjustedWeightIndicator=None, TimeInTransitIndicator=None, HandlingUnits=None, AdjustedHeightIndicator=None, DensityEligibleIndicator=None, QuoteNumberIndicator=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Request = Request
        self.Request_nsprefix_ = "common"
        self.ShipFrom = ShipFrom
        self.ShipFrom_nsprefix_ = "frt"
        self.ShipTo = ShipTo
        self.ShipTo_nsprefix_ = "frt"
        self.PaymentInformation = PaymentInformation
        self.PaymentInformation_nsprefix_ = "frt"
        self.Service = Service
        self.Service_nsprefix_ = "frt"
        self.HandlingUnitOne = HandlingUnitOne
        self.HandlingUnitOne_nsprefix_ = "frt"
        self.HandlingUnitTwo = HandlingUnitTwo
        self.HandlingUnitTwo_nsprefix_ = "frt"
        if Commodity is None:
            self.Commodity = []
        else:
            self.Commodity = Commodity
        self.Commodity_nsprefix_ = "frt"
        self.ShipmentServiceOptions = ShipmentServiceOptions
        self.ShipmentServiceOptions_nsprefix_ = "frt"
        self.PickupRequest = PickupRequest
        self.PickupRequest_nsprefix_ = "frt"
        self.AlternateRateOptions = AlternateRateOptions
        self.AlternateRateOptions_nsprefix_ = "frt"
        self.GFPOptions = GFPOptions
        self.GFPOptions_nsprefix_ = "frt"
        self.AccountType = AccountType
        self.AccountType_nsprefix_ = "frt"
        self.ShipmentTotalWeight = ShipmentTotalWeight
        self.ShipmentTotalWeight_nsprefix_ = "frt"
        self.HandlingUnitWeight = HandlingUnitWeight
        self.HandlingUnitWeight_nsprefix_ = "frt"
        self.AdjustedWeightIndicator = AdjustedWeightIndicator
        self.AdjustedWeightIndicator_nsprefix_ = None
        self.TimeInTransitIndicator = TimeInTransitIndicator
        self.TimeInTransitIndicator_nsprefix_ = None
        if HandlingUnits is None:
            self.HandlingUnits = []
        else:
            self.HandlingUnits = HandlingUnits
        self.HandlingUnits_nsprefix_ = "frt"
        self.AdjustedHeightIndicator = AdjustedHeightIndicator
        self.AdjustedHeightIndicator_nsprefix_ = None
        self.DensityEligibleIndicator = DensityEligibleIndicator
        self.DensityEligibleIndicator_nsprefix_ = None
        self.QuoteNumberIndicator = QuoteNumberIndicator
        self.QuoteNumberIndicator_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, FreightRateRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if FreightRateRequest.subclass:
            return FreightRateRequest.subclass(*args_, **kwargs_)
        else:
            return FreightRateRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Request(self):
        return self.Request
    def set_Request(self, Request):
        self.Request = Request
    def get_ShipFrom(self):
        return self.ShipFrom
    def set_ShipFrom(self, ShipFrom):
        self.ShipFrom = ShipFrom
    def get_ShipTo(self):
        return self.ShipTo
    def set_ShipTo(self, ShipTo):
        self.ShipTo = ShipTo
    def get_PaymentInformation(self):
        return self.PaymentInformation
    def set_PaymentInformation(self, PaymentInformation):
        self.PaymentInformation = PaymentInformation
    def get_Service(self):
        return self.Service
    def set_Service(self, Service):
        self.Service = Service
    def get_HandlingUnitOne(self):
        return self.HandlingUnitOne
    def set_HandlingUnitOne(self, HandlingUnitOne):
        self.HandlingUnitOne = HandlingUnitOne
    def get_HandlingUnitTwo(self):
        return self.HandlingUnitTwo
    def set_HandlingUnitTwo(self, HandlingUnitTwo):
        self.HandlingUnitTwo = HandlingUnitTwo
    def get_Commodity(self):
        return self.Commodity
    def set_Commodity(self, Commodity):
        self.Commodity = Commodity
    def add_Commodity(self, value):
        self.Commodity.append(value)
    def insert_Commodity_at(self, index, value):
        self.Commodity.insert(index, value)
    def replace_Commodity_at(self, index, value):
        self.Commodity[index] = value
    def get_ShipmentServiceOptions(self):
        return self.ShipmentServiceOptions
    def set_ShipmentServiceOptions(self, ShipmentServiceOptions):
        self.ShipmentServiceOptions = ShipmentServiceOptions
    def get_PickupRequest(self):
        return self.PickupRequest
    def set_PickupRequest(self, PickupRequest):
        self.PickupRequest = PickupRequest
    def get_AlternateRateOptions(self):
        return self.AlternateRateOptions
    def set_AlternateRateOptions(self, AlternateRateOptions):
        self.AlternateRateOptions = AlternateRateOptions
    def get_GFPOptions(self):
        return self.GFPOptions
    def set_GFPOptions(self, GFPOptions):
        self.GFPOptions = GFPOptions
    def get_AccountType(self):
        return self.AccountType
    def set_AccountType(self, AccountType):
        self.AccountType = AccountType
    def get_ShipmentTotalWeight(self):
        return self.ShipmentTotalWeight
    def set_ShipmentTotalWeight(self, ShipmentTotalWeight):
        self.ShipmentTotalWeight = ShipmentTotalWeight
    def get_HandlingUnitWeight(self):
        return self.HandlingUnitWeight
    def set_HandlingUnitWeight(self, HandlingUnitWeight):
        self.HandlingUnitWeight = HandlingUnitWeight
    def get_AdjustedWeightIndicator(self):
        return self.AdjustedWeightIndicator
    def set_AdjustedWeightIndicator(self, AdjustedWeightIndicator):
        self.AdjustedWeightIndicator = AdjustedWeightIndicator
    def get_TimeInTransitIndicator(self):
        return self.TimeInTransitIndicator
    def set_TimeInTransitIndicator(self, TimeInTransitIndicator):
        self.TimeInTransitIndicator = TimeInTransitIndicator
    def get_HandlingUnits(self):
        return self.HandlingUnits
    def set_HandlingUnits(self, HandlingUnits):
        self.HandlingUnits = HandlingUnits
    def add_HandlingUnits(self, value):
        self.HandlingUnits.append(value)
    def insert_HandlingUnits_at(self, index, value):
        self.HandlingUnits.insert(index, value)
    def replace_HandlingUnits_at(self, index, value):
        self.HandlingUnits[index] = value
    def get_AdjustedHeightIndicator(self):
        return self.AdjustedHeightIndicator
    def set_AdjustedHeightIndicator(self, AdjustedHeightIndicator):
        self.AdjustedHeightIndicator = AdjustedHeightIndicator
    def get_DensityEligibleIndicator(self):
        return self.DensityEligibleIndicator
    def set_DensityEligibleIndicator(self, DensityEligibleIndicator):
        self.DensityEligibleIndicator = DensityEligibleIndicator
    def get_QuoteNumberIndicator(self):
        return self.QuoteNumberIndicator
    def set_QuoteNumberIndicator(self, QuoteNumberIndicator):
        self.QuoteNumberIndicator = QuoteNumberIndicator
    def _hasContent(self):
        if (
            self.Request is not None or
            self.ShipFrom is not None or
            self.ShipTo is not None or
            self.PaymentInformation is not None or
            self.Service is not None or
            self.HandlingUnitOne is not None or
            self.HandlingUnitTwo is not None or
            self.Commodity or
            self.ShipmentServiceOptions is not None or
            self.PickupRequest is not None or
            self.AlternateRateOptions is not None or
            self.GFPOptions is not None or
            self.AccountType is not None or
            self.ShipmentTotalWeight is not None or
            self.HandlingUnitWeight is not None or
            self.AdjustedWeightIndicator is not None or
            self.TimeInTransitIndicator is not None or
            self.HandlingUnits or
            self.AdjustedHeightIndicator is not None or
            self.DensityEligibleIndicator is not None or
            self.QuoteNumberIndicator is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FreightRateRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FreightRateRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'FreightRateRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='FreightRateRequest')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='FreightRateRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='FreightRateRequest'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FreightRateRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Request is not None:
            namespaceprefix_ = self.Request_nsprefix_ + ':' if (UseCapturedNS_ and self.Request_nsprefix_) else ''
            self.Request.export(outfile, level, namespaceprefix_='common:', namespacedef_='', name_='Request', pretty_print=pretty_print)
        if self.ShipFrom is not None:
            namespaceprefix_ = self.ShipFrom_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipFrom_nsprefix_) else ''
            self.ShipFrom.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipFrom', pretty_print=pretty_print)
        if self.ShipTo is not None:
            namespaceprefix_ = self.ShipTo_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipTo_nsprefix_) else ''
            self.ShipTo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipTo', pretty_print=pretty_print)
        if self.PaymentInformation is not None:
            namespaceprefix_ = self.PaymentInformation_nsprefix_ + ':' if (UseCapturedNS_ and self.PaymentInformation_nsprefix_) else ''
            self.PaymentInformation.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PaymentInformation', pretty_print=pretty_print)
        if self.Service is not None:
            namespaceprefix_ = self.Service_nsprefix_ + ':' if (UseCapturedNS_ and self.Service_nsprefix_) else ''
            self.Service.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Service', pretty_print=pretty_print)
        if self.HandlingUnitOne is not None:
            namespaceprefix_ = self.HandlingUnitOne_nsprefix_ + ':' if (UseCapturedNS_ and self.HandlingUnitOne_nsprefix_) else ''
            self.HandlingUnitOne.export(outfile, level, namespaceprefix_, namespacedef_='', name_='HandlingUnitOne', pretty_print=pretty_print)
        if self.HandlingUnitTwo is not None:
            namespaceprefix_ = self.HandlingUnitTwo_nsprefix_ + ':' if (UseCapturedNS_ and self.HandlingUnitTwo_nsprefix_) else ''
            self.HandlingUnitTwo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='HandlingUnitTwo', pretty_print=pretty_print)
        for Commodity_ in self.Commodity:
            namespaceprefix_ = self.Commodity_nsprefix_ + ':' if (UseCapturedNS_ and self.Commodity_nsprefix_) else ''
            Commodity_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Commodity', pretty_print=pretty_print)
        if self.ShipmentServiceOptions is not None:
            namespaceprefix_ = self.ShipmentServiceOptions_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentServiceOptions_nsprefix_) else ''
            self.ShipmentServiceOptions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentServiceOptions', pretty_print=pretty_print)
        if self.PickupRequest is not None:
            namespaceprefix_ = self.PickupRequest_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupRequest_nsprefix_) else ''
            self.PickupRequest.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PickupRequest', pretty_print=pretty_print)
        if self.AlternateRateOptions is not None:
            namespaceprefix_ = self.AlternateRateOptions_nsprefix_ + ':' if (UseCapturedNS_ and self.AlternateRateOptions_nsprefix_) else ''
            self.AlternateRateOptions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AlternateRateOptions', pretty_print=pretty_print)
        if self.GFPOptions is not None:
            namespaceprefix_ = self.GFPOptions_nsprefix_ + ':' if (UseCapturedNS_ and self.GFPOptions_nsprefix_) else ''
            self.GFPOptions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GFPOptions', pretty_print=pretty_print)
        if self.AccountType is not None:
            namespaceprefix_ = self.AccountType_nsprefix_ + ':' if (UseCapturedNS_ and self.AccountType_nsprefix_) else ''
            self.AccountType.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AccountType', pretty_print=pretty_print)
        if self.ShipmentTotalWeight is not None:
            namespaceprefix_ = self.ShipmentTotalWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentTotalWeight_nsprefix_) else ''
            self.ShipmentTotalWeight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentTotalWeight', pretty_print=pretty_print)
        if self.HandlingUnitWeight is not None:
            namespaceprefix_ = self.HandlingUnitWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.HandlingUnitWeight_nsprefix_) else ''
            self.HandlingUnitWeight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='HandlingUnitWeight', pretty_print=pretty_print)
        if self.AdjustedWeightIndicator is not None:
            namespaceprefix_ = self.AdjustedWeightIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.AdjustedWeightIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAdjustedWeightIndicator>%s</%sAdjustedWeightIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AdjustedWeightIndicator), input_name='AdjustedWeightIndicator')), namespaceprefix_ , eol_))
        if self.TimeInTransitIndicator is not None:
            namespaceprefix_ = self.TimeInTransitIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.TimeInTransitIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTimeInTransitIndicator>%s</%sTimeInTransitIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TimeInTransitIndicator), input_name='TimeInTransitIndicator')), namespaceprefix_ , eol_))
        for HandlingUnits_ in self.HandlingUnits:
            namespaceprefix_ = self.HandlingUnits_nsprefix_ + ':' if (UseCapturedNS_ and self.HandlingUnits_nsprefix_) else ''
            HandlingUnits_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='HandlingUnits', pretty_print=pretty_print)
        if self.AdjustedHeightIndicator is not None:
            namespaceprefix_ = self.AdjustedHeightIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.AdjustedHeightIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAdjustedHeightIndicator>%s</%sAdjustedHeightIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AdjustedHeightIndicator), input_name='AdjustedHeightIndicator')), namespaceprefix_ , eol_))
        if self.DensityEligibleIndicator is not None:
            namespaceprefix_ = self.DensityEligibleIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.DensityEligibleIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDensityEligibleIndicator>%s</%sDensityEligibleIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DensityEligibleIndicator), input_name='DensityEligibleIndicator')), namespaceprefix_ , eol_))
        if self.QuoteNumberIndicator is not None:
            namespaceprefix_ = self.QuoteNumberIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.QuoteNumberIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sQuoteNumberIndicator>%s</%sQuoteNumberIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.QuoteNumberIndicator), input_name='QuoteNumberIndicator')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Request':
            obj_ = RequestType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Request = obj_
            obj_.original_tagname_ = 'Request'
        elif nodeName_ == 'ShipFrom':
            obj_ = ShipFromType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipFrom = obj_
            obj_.original_tagname_ = 'ShipFrom'
        elif nodeName_ == 'ShipTo':
            obj_ = ShipToType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipTo = obj_
            obj_.original_tagname_ = 'ShipTo'
        elif nodeName_ == 'PaymentInformation':
            obj_ = PaymentInformationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PaymentInformation = obj_
            obj_.original_tagname_ = 'PaymentInformation'
        elif nodeName_ == 'Service':
            obj_ = RateCodeDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Service = obj_
            obj_.original_tagname_ = 'Service'
        elif nodeName_ == 'HandlingUnitOne':
            obj_ = HandlingUnitType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.HandlingUnitOne = obj_
            obj_.original_tagname_ = 'HandlingUnitOne'
        elif nodeName_ == 'HandlingUnitTwo':
            obj_ = HandlingUnitType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.HandlingUnitTwo = obj_
            obj_.original_tagname_ = 'HandlingUnitTwo'
        elif nodeName_ == 'Commodity':
            obj_ = CommodityType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Commodity.append(obj_)
            obj_.original_tagname_ = 'Commodity'
        elif nodeName_ == 'ShipmentServiceOptions':
            obj_ = ShipmentServiceOptionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentServiceOptions = obj_
            obj_.original_tagname_ = 'ShipmentServiceOptions'
        elif nodeName_ == 'PickupRequest':
            obj_ = PickupRequestType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PickupRequest = obj_
            obj_.original_tagname_ = 'PickupRequest'
        elif nodeName_ == 'AlternateRateOptions':
            obj_ = RateCodeDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AlternateRateOptions = obj_
            obj_.original_tagname_ = 'AlternateRateOptions'
        elif nodeName_ == 'GFPOptions':
            obj_ = GFPOptionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GFPOptions = obj_
            obj_.original_tagname_ = 'GFPOptions'
        elif nodeName_ == 'AccountType':
            obj_ = AccountType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AccountType = obj_
            obj_.original_tagname_ = 'AccountType'
        elif nodeName_ == 'ShipmentTotalWeight':
            obj_ = ShipmentTotalWeightType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentTotalWeight = obj_
            obj_.original_tagname_ = 'ShipmentTotalWeight'
        elif nodeName_ == 'HandlingUnitWeight':
            obj_ = HandlingUnitWeightType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.HandlingUnitWeight = obj_
            obj_.original_tagname_ = 'HandlingUnitWeight'
        elif nodeName_ == 'AdjustedWeightIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AdjustedWeightIndicator')
            value_ = self.gds_validate_string(value_, node, 'AdjustedWeightIndicator')
            self.AdjustedWeightIndicator = value_
            self.AdjustedWeightIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'TimeInTransitIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TimeInTransitIndicator')
            value_ = self.gds_validate_string(value_, node, 'TimeInTransitIndicator')
            self.TimeInTransitIndicator = value_
            self.TimeInTransitIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'HandlingUnits':
            obj_ = HandlingUnitsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.HandlingUnits.append(obj_)
            obj_.original_tagname_ = 'HandlingUnits'
        elif nodeName_ == 'AdjustedHeightIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AdjustedHeightIndicator')
            value_ = self.gds_validate_string(value_, node, 'AdjustedHeightIndicator')
            self.AdjustedHeightIndicator = value_
            self.AdjustedHeightIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'DensityEligibleIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DensityEligibleIndicator')
            value_ = self.gds_validate_string(value_, node, 'DensityEligibleIndicator')
            self.DensityEligibleIndicator = value_
            self.DensityEligibleIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'QuoteNumberIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'QuoteNumberIndicator')
            value_ = self.gds_validate_string(value_, node, 'QuoteNumberIndicator')
            self.QuoteNumberIndicator = value_
            self.QuoteNumberIndicator_nsprefix_ = child_.prefix
# end class FreightRateRequest


class FreightRateResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Response=None, CustomerServiceCenterPhone=None, Rate=None, FreightDensityRate=None, Commodity=None, TotalShipmentCharge=None, BillableShipmentWeight=None, DimensionalWeight=None, Service=None, GuaranteedIndicator=None, MinimumChargeAppliedIndicator=None, AlternateRatesResponse=None, MinimumBillableWeightAppliedIndicator=None, RatingSchedule=None, HoldAtAirportPickupDate=None, NextAvailablePickupDate=None, TimeInTransit=None, HandlingUnits=None, QuoteNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Response = Response
        self.Response_nsprefix_ = "common"
        self.CustomerServiceCenterPhone = CustomerServiceCenterPhone
        self.CustomerServiceCenterPhone_nsprefix_ = "frt"
        if Rate is None:
            self.Rate = []
        else:
            self.Rate = Rate
        self.Rate_nsprefix_ = "frt"
        self.FreightDensityRate = FreightDensityRate
        self.FreightDensityRate_nsprefix_ = "frt"
        if Commodity is None:
            self.Commodity = []
        else:
            self.Commodity = Commodity
        self.Commodity_nsprefix_ = "frt"
        self.TotalShipmentCharge = TotalShipmentCharge
        self.TotalShipmentCharge_nsprefix_ = "frt"
        self.BillableShipmentWeight = BillableShipmentWeight
        self.BillableShipmentWeight_nsprefix_ = "frt"
        self.DimensionalWeight = DimensionalWeight
        self.DimensionalWeight_nsprefix_ = "frt"
        self.Service = Service
        self.Service_nsprefix_ = "frt"
        self.GuaranteedIndicator = GuaranteedIndicator
        self.GuaranteedIndicator_nsprefix_ = None
        self.MinimumChargeAppliedIndicator = MinimumChargeAppliedIndicator
        self.MinimumChargeAppliedIndicator_nsprefix_ = None
        if AlternateRatesResponse is None:
            self.AlternateRatesResponse = []
        else:
            self.AlternateRatesResponse = AlternateRatesResponse
        self.AlternateRatesResponse_nsprefix_ = "frt"
        self.MinimumBillableWeightAppliedIndicator = MinimumBillableWeightAppliedIndicator
        self.MinimumBillableWeightAppliedIndicator_nsprefix_ = None
        self.RatingSchedule = RatingSchedule
        self.RatingSchedule_nsprefix_ = "frt"
        self.HoldAtAirportPickupDate = HoldAtAirportPickupDate
        self.HoldAtAirportPickupDate_nsprefix_ = None
        self.NextAvailablePickupDate = NextAvailablePickupDate
        self.NextAvailablePickupDate_nsprefix_ = None
        self.TimeInTransit = TimeInTransit
        self.TimeInTransit_nsprefix_ = "frt"
        self.HandlingUnits = HandlingUnits
        self.HandlingUnits_nsprefix_ = "frt"
        self.QuoteNumber = QuoteNumber
        self.QuoteNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, FreightRateResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if FreightRateResponse.subclass:
            return FreightRateResponse.subclass(*args_, **kwargs_)
        else:
            return FreightRateResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Response(self):
        return self.Response
    def set_Response(self, Response):
        self.Response = Response
    def get_CustomerServiceCenterPhone(self):
        return self.CustomerServiceCenterPhone
    def set_CustomerServiceCenterPhone(self, CustomerServiceCenterPhone):
        self.CustomerServiceCenterPhone = CustomerServiceCenterPhone
    def get_Rate(self):
        return self.Rate
    def set_Rate(self, Rate):
        self.Rate = Rate
    def add_Rate(self, value):
        self.Rate.append(value)
    def insert_Rate_at(self, index, value):
        self.Rate.insert(index, value)
    def replace_Rate_at(self, index, value):
        self.Rate[index] = value
    def get_FreightDensityRate(self):
        return self.FreightDensityRate
    def set_FreightDensityRate(self, FreightDensityRate):
        self.FreightDensityRate = FreightDensityRate
    def get_Commodity(self):
        return self.Commodity
    def set_Commodity(self, Commodity):
        self.Commodity = Commodity
    def add_Commodity(self, value):
        self.Commodity.append(value)
    def insert_Commodity_at(self, index, value):
        self.Commodity.insert(index, value)
    def replace_Commodity_at(self, index, value):
        self.Commodity[index] = value
    def get_TotalShipmentCharge(self):
        return self.TotalShipmentCharge
    def set_TotalShipmentCharge(self, TotalShipmentCharge):
        self.TotalShipmentCharge = TotalShipmentCharge
    def get_BillableShipmentWeight(self):
        return self.BillableShipmentWeight
    def set_BillableShipmentWeight(self, BillableShipmentWeight):
        self.BillableShipmentWeight = BillableShipmentWeight
    def get_DimensionalWeight(self):
        return self.DimensionalWeight
    def set_DimensionalWeight(self, DimensionalWeight):
        self.DimensionalWeight = DimensionalWeight
    def get_Service(self):
        return self.Service
    def set_Service(self, Service):
        self.Service = Service
    def get_GuaranteedIndicator(self):
        return self.GuaranteedIndicator
    def set_GuaranteedIndicator(self, GuaranteedIndicator):
        self.GuaranteedIndicator = GuaranteedIndicator
    def get_MinimumChargeAppliedIndicator(self):
        return self.MinimumChargeAppliedIndicator
    def set_MinimumChargeAppliedIndicator(self, MinimumChargeAppliedIndicator):
        self.MinimumChargeAppliedIndicator = MinimumChargeAppliedIndicator
    def get_AlternateRatesResponse(self):
        return self.AlternateRatesResponse
    def set_AlternateRatesResponse(self, AlternateRatesResponse):
        self.AlternateRatesResponse = AlternateRatesResponse
    def add_AlternateRatesResponse(self, value):
        self.AlternateRatesResponse.append(value)
    def insert_AlternateRatesResponse_at(self, index, value):
        self.AlternateRatesResponse.insert(index, value)
    def replace_AlternateRatesResponse_at(self, index, value):
        self.AlternateRatesResponse[index] = value
    def get_MinimumBillableWeightAppliedIndicator(self):
        return self.MinimumBillableWeightAppliedIndicator
    def set_MinimumBillableWeightAppliedIndicator(self, MinimumBillableWeightAppliedIndicator):
        self.MinimumBillableWeightAppliedIndicator = MinimumBillableWeightAppliedIndicator
    def get_RatingSchedule(self):
        return self.RatingSchedule
    def set_RatingSchedule(self, RatingSchedule):
        self.RatingSchedule = RatingSchedule
    def get_HoldAtAirportPickupDate(self):
        return self.HoldAtAirportPickupDate
    def set_HoldAtAirportPickupDate(self, HoldAtAirportPickupDate):
        self.HoldAtAirportPickupDate = HoldAtAirportPickupDate
    def get_NextAvailablePickupDate(self):
        return self.NextAvailablePickupDate
    def set_NextAvailablePickupDate(self, NextAvailablePickupDate):
        self.NextAvailablePickupDate = NextAvailablePickupDate
    def get_TimeInTransit(self):
        return self.TimeInTransit
    def set_TimeInTransit(self, TimeInTransit):
        self.TimeInTransit = TimeInTransit
    def get_HandlingUnits(self):
        return self.HandlingUnits
    def set_HandlingUnits(self, HandlingUnits):
        self.HandlingUnits = HandlingUnits
    def get_QuoteNumber(self):
        return self.QuoteNumber
    def set_QuoteNumber(self, QuoteNumber):
        self.QuoteNumber = QuoteNumber
    def _hasContent(self):
        if (
            self.Response is not None or
            self.CustomerServiceCenterPhone is not None or
            self.Rate or
            self.FreightDensityRate is not None or
            self.Commodity or
            self.TotalShipmentCharge is not None or
            self.BillableShipmentWeight is not None or
            self.DimensionalWeight is not None or
            self.Service is not None or
            self.GuaranteedIndicator is not None or
            self.MinimumChargeAppliedIndicator is not None or
            self.AlternateRatesResponse or
            self.MinimumBillableWeightAppliedIndicator is not None or
            self.RatingSchedule is not None or
            self.HoldAtAirportPickupDate is not None or
            self.NextAvailablePickupDate is not None or
            self.TimeInTransit is not None or
            self.HandlingUnits is not None or
            self.QuoteNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FreightRateResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FreightRateResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'FreightRateResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='FreightRateResponse')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='FreightRateResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='FreightRateResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FreightRateResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Response is not None:
            namespaceprefix_ = self.Response_nsprefix_ + ':' if (UseCapturedNS_ and self.Response_nsprefix_) else ''
            self.Response.export(outfile, level, namespaceprefix_='common:', namespacedef_='', name_='Response', pretty_print=pretty_print)
        if self.CustomerServiceCenterPhone is not None:
            namespaceprefix_ = self.CustomerServiceCenterPhone_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomerServiceCenterPhone_nsprefix_) else ''
            self.CustomerServiceCenterPhone.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CustomerServiceCenterPhone', pretty_print=pretty_print)
        for Rate_ in self.Rate:
            namespaceprefix_ = self.Rate_nsprefix_ + ':' if (UseCapturedNS_ and self.Rate_nsprefix_) else ''
            Rate_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Rate', pretty_print=pretty_print)
        if self.FreightDensityRate is not None:
            namespaceprefix_ = self.FreightDensityRate_nsprefix_ + ':' if (UseCapturedNS_ and self.FreightDensityRate_nsprefix_) else ''
            self.FreightDensityRate.export(outfile, level, namespaceprefix_, namespacedef_='', name_='FreightDensityRate', pretty_print=pretty_print)
        for Commodity_ in self.Commodity:
            namespaceprefix_ = self.Commodity_nsprefix_ + ':' if (UseCapturedNS_ and self.Commodity_nsprefix_) else ''
            Commodity_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Commodity', pretty_print=pretty_print)
        if self.TotalShipmentCharge is not None:
            namespaceprefix_ = self.TotalShipmentCharge_nsprefix_ + ':' if (UseCapturedNS_ and self.TotalShipmentCharge_nsprefix_) else ''
            self.TotalShipmentCharge.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TotalShipmentCharge', pretty_print=pretty_print)
        if self.BillableShipmentWeight is not None:
            namespaceprefix_ = self.BillableShipmentWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.BillableShipmentWeight_nsprefix_) else ''
            self.BillableShipmentWeight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='BillableShipmentWeight', pretty_print=pretty_print)
        if self.DimensionalWeight is not None:
            namespaceprefix_ = self.DimensionalWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.DimensionalWeight_nsprefix_) else ''
            self.DimensionalWeight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DimensionalWeight', pretty_print=pretty_print)
        if self.Service is not None:
            namespaceprefix_ = self.Service_nsprefix_ + ':' if (UseCapturedNS_ and self.Service_nsprefix_) else ''
            self.Service.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Service', pretty_print=pretty_print)
        if self.GuaranteedIndicator is not None:
            namespaceprefix_ = self.GuaranteedIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.GuaranteedIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGuaranteedIndicator>%s</%sGuaranteedIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GuaranteedIndicator), input_name='GuaranteedIndicator')), namespaceprefix_ , eol_))
        if self.MinimumChargeAppliedIndicator is not None:
            namespaceprefix_ = self.MinimumChargeAppliedIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.MinimumChargeAppliedIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMinimumChargeAppliedIndicator>%s</%sMinimumChargeAppliedIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MinimumChargeAppliedIndicator), input_name='MinimumChargeAppliedIndicator')), namespaceprefix_ , eol_))
        for AlternateRatesResponse_ in self.AlternateRatesResponse:
            namespaceprefix_ = self.AlternateRatesResponse_nsprefix_ + ':' if (UseCapturedNS_ and self.AlternateRatesResponse_nsprefix_) else ''
            AlternateRatesResponse_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AlternateRatesResponse', pretty_print=pretty_print)
        if self.MinimumBillableWeightAppliedIndicator is not None:
            namespaceprefix_ = self.MinimumBillableWeightAppliedIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.MinimumBillableWeightAppliedIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMinimumBillableWeightAppliedIndicator>%s</%sMinimumBillableWeightAppliedIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MinimumBillableWeightAppliedIndicator), input_name='MinimumBillableWeightAppliedIndicator')), namespaceprefix_ , eol_))
        if self.RatingSchedule is not None:
            namespaceprefix_ = self.RatingSchedule_nsprefix_ + ':' if (UseCapturedNS_ and self.RatingSchedule_nsprefix_) else ''
            self.RatingSchedule.export(outfile, level, namespaceprefix_, namespacedef_='', name_='RatingSchedule', pretty_print=pretty_print)
        if self.HoldAtAirportPickupDate is not None:
            namespaceprefix_ = self.HoldAtAirportPickupDate_nsprefix_ + ':' if (UseCapturedNS_ and self.HoldAtAirportPickupDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHoldAtAirportPickupDate>%s</%sHoldAtAirportPickupDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HoldAtAirportPickupDate), input_name='HoldAtAirportPickupDate')), namespaceprefix_ , eol_))
        if self.NextAvailablePickupDate is not None:
            namespaceprefix_ = self.NextAvailablePickupDate_nsprefix_ + ':' if (UseCapturedNS_ and self.NextAvailablePickupDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNextAvailablePickupDate>%s</%sNextAvailablePickupDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NextAvailablePickupDate), input_name='NextAvailablePickupDate')), namespaceprefix_ , eol_))
        if self.TimeInTransit is not None:
            namespaceprefix_ = self.TimeInTransit_nsprefix_ + ':' if (UseCapturedNS_ and self.TimeInTransit_nsprefix_) else ''
            self.TimeInTransit.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TimeInTransit', pretty_print=pretty_print)
        if self.HandlingUnits is not None:
            namespaceprefix_ = self.HandlingUnits_nsprefix_ + ':' if (UseCapturedNS_ and self.HandlingUnits_nsprefix_) else ''
            self.HandlingUnits.export(outfile, level, namespaceprefix_, namespacedef_='', name_='HandlingUnits', pretty_print=pretty_print)
        if self.QuoteNumber is not None:
            namespaceprefix_ = self.QuoteNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.QuoteNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sQuoteNumber>%s</%sQuoteNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.QuoteNumber), input_name='QuoteNumber')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Response':
            obj_ = ResponseType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Response = obj_
            obj_.original_tagname_ = 'Response'
        elif nodeName_ == 'CustomerServiceCenterPhone':
            obj_ = PhoneType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CustomerServiceCenterPhone = obj_
            obj_.original_tagname_ = 'CustomerServiceCenterPhone'
        elif nodeName_ == 'Rate':
            obj_ = RateType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Rate.append(obj_)
            obj_.original_tagname_ = 'Rate'
        elif nodeName_ == 'FreightDensityRate':
            obj_ = FreightDensityRateType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.FreightDensityRate = obj_
            obj_.original_tagname_ = 'FreightDensityRate'
        elif nodeName_ == 'Commodity':
            obj_ = CommodityWeightType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Commodity.append(obj_)
            obj_.original_tagname_ = 'Commodity'
        elif nodeName_ == 'TotalShipmentCharge':
            obj_ = TotalShipmentChargeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TotalShipmentCharge = obj_
            obj_.original_tagname_ = 'TotalShipmentCharge'
        elif nodeName_ == 'BillableShipmentWeight':
            obj_ = WeightType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BillableShipmentWeight = obj_
            obj_.original_tagname_ = 'BillableShipmentWeight'
        elif nodeName_ == 'DimensionalWeight':
            obj_ = WeightType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DimensionalWeight = obj_
            obj_.original_tagname_ = 'DimensionalWeight'
        elif nodeName_ == 'Service':
            obj_ = RateCodeDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Service = obj_
            obj_.original_tagname_ = 'Service'
        elif nodeName_ == 'GuaranteedIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GuaranteedIndicator')
            value_ = self.gds_validate_string(value_, node, 'GuaranteedIndicator')
            self.GuaranteedIndicator = value_
            self.GuaranteedIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'MinimumChargeAppliedIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MinimumChargeAppliedIndicator')
            value_ = self.gds_validate_string(value_, node, 'MinimumChargeAppliedIndicator')
            self.MinimumChargeAppliedIndicator = value_
            self.MinimumChargeAppliedIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'AlternateRatesResponse':
            obj_ = AlternateRatesResponseType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AlternateRatesResponse.append(obj_)
            obj_.original_tagname_ = 'AlternateRatesResponse'
        elif nodeName_ == 'MinimumBillableWeightAppliedIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MinimumBillableWeightAppliedIndicator')
            value_ = self.gds_validate_string(value_, node, 'MinimumBillableWeightAppliedIndicator')
            self.MinimumBillableWeightAppliedIndicator = value_
            self.MinimumBillableWeightAppliedIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'RatingSchedule':
            obj_ = RatingScheduleType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.RatingSchedule = obj_
            obj_.original_tagname_ = 'RatingSchedule'
        elif nodeName_ == 'HoldAtAirportPickupDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HoldAtAirportPickupDate')
            value_ = self.gds_validate_string(value_, node, 'HoldAtAirportPickupDate')
            self.HoldAtAirportPickupDate = value_
            self.HoldAtAirportPickupDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'NextAvailablePickupDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NextAvailablePickupDate')
            value_ = self.gds_validate_string(value_, node, 'NextAvailablePickupDate')
            self.NextAvailablePickupDate = value_
            self.NextAvailablePickupDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'TimeInTransit':
            obj_ = TimeInTransitResponseType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TimeInTransit = obj_
            obj_.original_tagname_ = 'TimeInTransit'
        elif nodeName_ == 'HandlingUnits':
            obj_ = HandlingUnitsInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.HandlingUnits = obj_
            obj_.original_tagname_ = 'HandlingUnits'
        elif nodeName_ == 'QuoteNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'QuoteNumber')
            value_ = self.gds_validate_string(value_, node, 'QuoteNumber')
            self.QuoteNumber = value_
            self.QuoteNumber_nsprefix_ = child_.prefix
# end class FreightRateResponse


class AccountType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Code=None, Description=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Code = Code
        self.Code_nsprefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AccountType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AccountType.subclass:
            return AccountType.subclass(*args_, **kwargs_)
        else:
            return AccountType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Code(self):
        return self.Code
    def set_Code(self, Code):
        self.Code = Code
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def _hasContent(self):
        if (
            self.Code is not None or
            self.Description is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AccountType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AccountType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AccountType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AccountType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AccountType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AccountType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AccountType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Code is not None:
            namespaceprefix_ = self.Code_nsprefix_ + ':' if (UseCapturedNS_ and self.Code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCode>%s</%sCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Code), input_name='Code')), namespaceprefix_ , eol_))
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Code':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Code')
            value_ = self.gds_validate_string(value_, node, 'Code')
            self.Code = value_
            self.Code_nsprefix_ = child_.prefix
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
# end class AccountType


class ShipmentTotalWeightType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Value=None, UnitOfMeasurement=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Value = Value
        self.Value_nsprefix_ = None
        self.UnitOfMeasurement = UnitOfMeasurement
        self.UnitOfMeasurement_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentTotalWeightType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentTotalWeightType.subclass:
            return ShipmentTotalWeightType.subclass(*args_, **kwargs_)
        else:
            return ShipmentTotalWeightType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def get_UnitOfMeasurement(self):
        return self.UnitOfMeasurement
    def set_UnitOfMeasurement(self, UnitOfMeasurement):
        self.UnitOfMeasurement = UnitOfMeasurement
    def _hasContent(self):
        if (
            self.Value is not None or
            self.UnitOfMeasurement is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentTotalWeightType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentTotalWeightType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentTotalWeightType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentTotalWeightType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentTotalWeightType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentTotalWeightType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentTotalWeightType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Value is not None:
            namespaceprefix_ = self.Value_nsprefix_ + ':' if (UseCapturedNS_ and self.Value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sValue>%s</%sValue>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Value), input_name='Value')), namespaceprefix_ , eol_))
        if self.UnitOfMeasurement is not None:
            namespaceprefix_ = self.UnitOfMeasurement_nsprefix_ + ':' if (UseCapturedNS_ and self.UnitOfMeasurement_nsprefix_) else ''
            self.UnitOfMeasurement.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UnitOfMeasurement', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Value')
            value_ = self.gds_validate_string(value_, node, 'Value')
            self.Value = value_
            self.Value_nsprefix_ = child_.prefix
        elif nodeName_ == 'UnitOfMeasurement':
            obj_ = UnitOfMeasurementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UnitOfMeasurement = obj_
            obj_.original_tagname_ = 'UnitOfMeasurement'
# end class ShipmentTotalWeightType


class HandlingUnitWeightType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Value=None, UnitOfMeasurement=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Value = Value
        self.Value_nsprefix_ = None
        self.UnitOfMeasurement = UnitOfMeasurement
        self.UnitOfMeasurement_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, HandlingUnitWeightType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if HandlingUnitWeightType.subclass:
            return HandlingUnitWeightType.subclass(*args_, **kwargs_)
        else:
            return HandlingUnitWeightType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def get_UnitOfMeasurement(self):
        return self.UnitOfMeasurement
    def set_UnitOfMeasurement(self, UnitOfMeasurement):
        self.UnitOfMeasurement = UnitOfMeasurement
    def _hasContent(self):
        if (
            self.Value is not None or
            self.UnitOfMeasurement is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='HandlingUnitWeightType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('HandlingUnitWeightType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'HandlingUnitWeightType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='HandlingUnitWeightType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='HandlingUnitWeightType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='HandlingUnitWeightType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='HandlingUnitWeightType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Value is not None:
            namespaceprefix_ = self.Value_nsprefix_ + ':' if (UseCapturedNS_ and self.Value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sValue>%s</%sValue>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Value), input_name='Value')), namespaceprefix_ , eol_))
        if self.UnitOfMeasurement is not None:
            namespaceprefix_ = self.UnitOfMeasurement_nsprefix_ + ':' if (UseCapturedNS_ and self.UnitOfMeasurement_nsprefix_) else ''
            self.UnitOfMeasurement.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UnitOfMeasurement', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Value')
            value_ = self.gds_validate_string(value_, node, 'Value')
            self.Value = value_
            self.Value_nsprefix_ = child_.prefix
        elif nodeName_ == 'UnitOfMeasurement':
            obj_ = UnitOfMeasurementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UnitOfMeasurement = obj_
            obj_.original_tagname_ = 'UnitOfMeasurement'
# end class HandlingUnitWeightType


class AlternateRatesResponseType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AlternateRateType=None, Rate=None, FreightDensityRate=None, BillableShipmentWeight=None, TimeInTransit=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.AlternateRateType = AlternateRateType
        self.AlternateRateType_nsprefix_ = "frt"
        if Rate is None:
            self.Rate = []
        else:
            self.Rate = Rate
        self.Rate_nsprefix_ = "frt"
        self.FreightDensityRate = FreightDensityRate
        self.FreightDensityRate_nsprefix_ = "frt"
        self.BillableShipmentWeight = BillableShipmentWeight
        self.BillableShipmentWeight_nsprefix_ = "frt"
        self.TimeInTransit = TimeInTransit
        self.TimeInTransit_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AlternateRatesResponseType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AlternateRatesResponseType.subclass:
            return AlternateRatesResponseType.subclass(*args_, **kwargs_)
        else:
            return AlternateRatesResponseType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AlternateRateType(self):
        return self.AlternateRateType
    def set_AlternateRateType(self, AlternateRateType):
        self.AlternateRateType = AlternateRateType
    def get_Rate(self):
        return self.Rate
    def set_Rate(self, Rate):
        self.Rate = Rate
    def add_Rate(self, value):
        self.Rate.append(value)
    def insert_Rate_at(self, index, value):
        self.Rate.insert(index, value)
    def replace_Rate_at(self, index, value):
        self.Rate[index] = value
    def get_FreightDensityRate(self):
        return self.FreightDensityRate
    def set_FreightDensityRate(self, FreightDensityRate):
        self.FreightDensityRate = FreightDensityRate
    def get_BillableShipmentWeight(self):
        return self.BillableShipmentWeight
    def set_BillableShipmentWeight(self, BillableShipmentWeight):
        self.BillableShipmentWeight = BillableShipmentWeight
    def get_TimeInTransit(self):
        return self.TimeInTransit
    def set_TimeInTransit(self, TimeInTransit):
        self.TimeInTransit = TimeInTransit
    def _hasContent(self):
        if (
            self.AlternateRateType is not None or
            self.Rate or
            self.FreightDensityRate is not None or
            self.BillableShipmentWeight is not None or
            self.TimeInTransit is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AlternateRatesResponseType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AlternateRatesResponseType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AlternateRatesResponseType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AlternateRatesResponseType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AlternateRatesResponseType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AlternateRatesResponseType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AlternateRatesResponseType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.AlternateRateType is not None:
            namespaceprefix_ = self.AlternateRateType_nsprefix_ + ':' if (UseCapturedNS_ and self.AlternateRateType_nsprefix_) else ''
            self.AlternateRateType.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AlternateRateType', pretty_print=pretty_print)
        for Rate_ in self.Rate:
            namespaceprefix_ = self.Rate_nsprefix_ + ':' if (UseCapturedNS_ and self.Rate_nsprefix_) else ''
            Rate_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Rate', pretty_print=pretty_print)
        if self.FreightDensityRate is not None:
            namespaceprefix_ = self.FreightDensityRate_nsprefix_ + ':' if (UseCapturedNS_ and self.FreightDensityRate_nsprefix_) else ''
            self.FreightDensityRate.export(outfile, level, namespaceprefix_, namespacedef_='', name_='FreightDensityRate', pretty_print=pretty_print)
        if self.BillableShipmentWeight is not None:
            namespaceprefix_ = self.BillableShipmentWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.BillableShipmentWeight_nsprefix_) else ''
            self.BillableShipmentWeight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='BillableShipmentWeight', pretty_print=pretty_print)
        if self.TimeInTransit is not None:
            namespaceprefix_ = self.TimeInTransit_nsprefix_ + ':' if (UseCapturedNS_ and self.TimeInTransit_nsprefix_) else ''
            self.TimeInTransit.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TimeInTransit', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'AlternateRateType':
            obj_ = RateCodeDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AlternateRateType = obj_
            obj_.original_tagname_ = 'AlternateRateType'
        elif nodeName_ == 'Rate':
            obj_ = RateType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Rate.append(obj_)
            obj_.original_tagname_ = 'Rate'
        elif nodeName_ == 'FreightDensityRate':
            obj_ = FreightDensityRateType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.FreightDensityRate = obj_
            obj_.original_tagname_ = 'FreightDensityRate'
        elif nodeName_ == 'BillableShipmentWeight':
            obj_ = WeightType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BillableShipmentWeight = obj_
            obj_.original_tagname_ = 'BillableShipmentWeight'
        elif nodeName_ == 'TimeInTransit':
            obj_ = TimeInTransitResponseType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TimeInTransit = obj_
            obj_.original_tagname_ = 'TimeInTransit'
# end class AlternateRatesResponseType


class ShipFromType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Name=None, Address=None, AttentionName=None, TariffPoint=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = None
        self.Address = Address
        self.Address_nsprefix_ = "frt"
        self.AttentionName = AttentionName
        self.AttentionName_nsprefix_ = None
        self.TariffPoint = TariffPoint
        self.TariffPoint_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipFromType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipFromType.subclass:
            return ShipFromType.subclass(*args_, **kwargs_)
        else:
            return ShipFromType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_AttentionName(self):
        return self.AttentionName
    def set_AttentionName(self, AttentionName):
        self.AttentionName = AttentionName
    def get_TariffPoint(self):
        return self.TariffPoint
    def set_TariffPoint(self, TariffPoint):
        self.TariffPoint = TariffPoint
    def _hasContent(self):
        if (
            self.Name is not None or
            self.Address is not None or
            self.AttentionName is not None or
            self.TariffPoint is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipFromType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipFromType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipFromType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipFromType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipFromType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipFromType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipFromType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName>%s</%sName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name), input_name='Name')), namespaceprefix_ , eol_))
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.AttentionName is not None:
            namespaceprefix_ = self.AttentionName_nsprefix_ + ':' if (UseCapturedNS_ and self.AttentionName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAttentionName>%s</%sAttentionName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AttentionName), input_name='AttentionName')), namespaceprefix_ , eol_))
        if self.TariffPoint is not None:
            namespaceprefix_ = self.TariffPoint_nsprefix_ + ':' if (UseCapturedNS_ and self.TariffPoint_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTariffPoint>%s</%sTariffPoint>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TariffPoint), input_name='TariffPoint')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Name')
            value_ = self.gds_validate_string(value_, node, 'Name')
            self.Name = value_
            self.Name_nsprefix_ = child_.prefix
        elif nodeName_ == 'Address':
            obj_ = AddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'AttentionName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AttentionName')
            value_ = self.gds_validate_string(value_, node, 'AttentionName')
            self.AttentionName = value_
            self.AttentionName_nsprefix_ = child_.prefix
        elif nodeName_ == 'TariffPoint':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TariffPoint')
            value_ = self.gds_validate_string(value_, node, 'TariffPoint')
            self.TariffPoint = value_
            self.TariffPoint_nsprefix_ = child_.prefix
# end class ShipFromType


class ShipToType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Name=None, Address=None, AttentionName=None, TariffPoint=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = None
        self.Address = Address
        self.Address_nsprefix_ = "frt"
        self.AttentionName = AttentionName
        self.AttentionName_nsprefix_ = None
        self.TariffPoint = TariffPoint
        self.TariffPoint_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipToType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipToType.subclass:
            return ShipToType.subclass(*args_, **kwargs_)
        else:
            return ShipToType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_AttentionName(self):
        return self.AttentionName
    def set_AttentionName(self, AttentionName):
        self.AttentionName = AttentionName
    def get_TariffPoint(self):
        return self.TariffPoint
    def set_TariffPoint(self, TariffPoint):
        self.TariffPoint = TariffPoint
    def _hasContent(self):
        if (
            self.Name is not None or
            self.Address is not None or
            self.AttentionName is not None or
            self.TariffPoint is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipToType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipToType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipToType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipToType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipToType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipToType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipToType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName>%s</%sName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name), input_name='Name')), namespaceprefix_ , eol_))
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.AttentionName is not None:
            namespaceprefix_ = self.AttentionName_nsprefix_ + ':' if (UseCapturedNS_ and self.AttentionName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAttentionName>%s</%sAttentionName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AttentionName), input_name='AttentionName')), namespaceprefix_ , eol_))
        if self.TariffPoint is not None:
            namespaceprefix_ = self.TariffPoint_nsprefix_ + ':' if (UseCapturedNS_ and self.TariffPoint_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTariffPoint>%s</%sTariffPoint>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TariffPoint), input_name='TariffPoint')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Name')
            value_ = self.gds_validate_string(value_, node, 'Name')
            self.Name = value_
            self.Name_nsprefix_ = child_.prefix
        elif nodeName_ == 'Address':
            obj_ = AddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'AttentionName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AttentionName')
            value_ = self.gds_validate_string(value_, node, 'AttentionName')
            self.AttentionName = value_
            self.AttentionName_nsprefix_ = child_.prefix
        elif nodeName_ == 'TariffPoint':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TariffPoint')
            value_ = self.gds_validate_string(value_, node, 'TariffPoint')
            self.TariffPoint = value_
            self.TariffPoint_nsprefix_ = child_.prefix
# end class ShipToType


class PaymentInformationType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Payer=None, ShipmentBillingOption=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Payer = Payer
        self.Payer_nsprefix_ = "frt"
        self.ShipmentBillingOption = ShipmentBillingOption
        self.ShipmentBillingOption_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PaymentInformationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PaymentInformationType.subclass:
            return PaymentInformationType.subclass(*args_, **kwargs_)
        else:
            return PaymentInformationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Payer(self):
        return self.Payer
    def set_Payer(self, Payer):
        self.Payer = Payer
    def get_ShipmentBillingOption(self):
        return self.ShipmentBillingOption
    def set_ShipmentBillingOption(self, ShipmentBillingOption):
        self.ShipmentBillingOption = ShipmentBillingOption
    def _hasContent(self):
        if (
            self.Payer is not None or
            self.ShipmentBillingOption is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PaymentInformationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PaymentInformationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PaymentInformationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PaymentInformationType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PaymentInformationType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PaymentInformationType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PaymentInformationType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Payer is not None:
            namespaceprefix_ = self.Payer_nsprefix_ + ':' if (UseCapturedNS_ and self.Payer_nsprefix_) else ''
            self.Payer.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Payer', pretty_print=pretty_print)
        if self.ShipmentBillingOption is not None:
            namespaceprefix_ = self.ShipmentBillingOption_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentBillingOption_nsprefix_) else ''
            self.ShipmentBillingOption.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentBillingOption', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Payer':
            obj_ = PayerType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Payer = obj_
            obj_.original_tagname_ = 'Payer'
        elif nodeName_ == 'ShipmentBillingOption':
            obj_ = RateCodeDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentBillingOption = obj_
            obj_.original_tagname_ = 'ShipmentBillingOption'
# end class PaymentInformationType


class PayerType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Name=None, Address=None, ShipperNumber=None, AttentionName=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = None
        self.Address = Address
        self.Address_nsprefix_ = "frt"
        self.ShipperNumber = ShipperNumber
        self.ShipperNumber_nsprefix_ = None
        self.AttentionName = AttentionName
        self.AttentionName_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PayerType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PayerType.subclass:
            return PayerType.subclass(*args_, **kwargs_)
        else:
            return PayerType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_ShipperNumber(self):
        return self.ShipperNumber
    def set_ShipperNumber(self, ShipperNumber):
        self.ShipperNumber = ShipperNumber
    def get_AttentionName(self):
        return self.AttentionName
    def set_AttentionName(self, AttentionName):
        self.AttentionName = AttentionName
    def _hasContent(self):
        if (
            self.Name is not None or
            self.Address is not None or
            self.ShipperNumber is not None or
            self.AttentionName is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PayerType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PayerType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PayerType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PayerType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PayerType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PayerType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PayerType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName>%s</%sName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name), input_name='Name')), namespaceprefix_ , eol_))
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.ShipperNumber is not None:
            namespaceprefix_ = self.ShipperNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipperNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipperNumber>%s</%sShipperNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShipperNumber), input_name='ShipperNumber')), namespaceprefix_ , eol_))
        if self.AttentionName is not None:
            namespaceprefix_ = self.AttentionName_nsprefix_ + ':' if (UseCapturedNS_ and self.AttentionName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAttentionName>%s</%sAttentionName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AttentionName), input_name='AttentionName')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Name')
            value_ = self.gds_validate_string(value_, node, 'Name')
            self.Name = value_
            self.Name_nsprefix_ = child_.prefix
        elif nodeName_ == 'Address':
            obj_ = AddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'ShipperNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShipperNumber')
            value_ = self.gds_validate_string(value_, node, 'ShipperNumber')
            self.ShipperNumber = value_
            self.ShipperNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'AttentionName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AttentionName')
            value_ = self.gds_validate_string(value_, node, 'AttentionName')
            self.AttentionName = value_
            self.AttentionName_nsprefix_ = child_.prefix
# end class PayerType


class AddressType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AddressLine=None, City=None, StateProvinceCode=None, Town=None, PostalCode=None, CountryCode=None, ResidentialAddressIndicator=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if AddressLine is None:
            self.AddressLine = []
        else:
            self.AddressLine = AddressLine
        self.AddressLine_nsprefix_ = None
        self.City = City
        self.City_nsprefix_ = None
        self.StateProvinceCode = StateProvinceCode
        self.StateProvinceCode_nsprefix_ = None
        self.Town = Town
        self.Town_nsprefix_ = None
        self.PostalCode = PostalCode
        self.PostalCode_nsprefix_ = None
        self.CountryCode = CountryCode
        self.CountryCode_nsprefix_ = None
        self.ResidentialAddressIndicator = ResidentialAddressIndicator
        self.ResidentialAddressIndicator_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AddressType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AddressType.subclass:
            return AddressType.subclass(*args_, **kwargs_)
        else:
            return AddressType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AddressLine(self):
        return self.AddressLine
    def set_AddressLine(self, AddressLine):
        self.AddressLine = AddressLine
    def add_AddressLine(self, value):
        self.AddressLine.append(value)
    def insert_AddressLine_at(self, index, value):
        self.AddressLine.insert(index, value)
    def replace_AddressLine_at(self, index, value):
        self.AddressLine[index] = value
    def get_City(self):
        return self.City
    def set_City(self, City):
        self.City = City
    def get_StateProvinceCode(self):
        return self.StateProvinceCode
    def set_StateProvinceCode(self, StateProvinceCode):
        self.StateProvinceCode = StateProvinceCode
    def get_Town(self):
        return self.Town
    def set_Town(self, Town):
        self.Town = Town
    def get_PostalCode(self):
        return self.PostalCode
    def set_PostalCode(self, PostalCode):
        self.PostalCode = PostalCode
    def get_CountryCode(self):
        return self.CountryCode
    def set_CountryCode(self, CountryCode):
        self.CountryCode = CountryCode
    def get_ResidentialAddressIndicator(self):
        return self.ResidentialAddressIndicator
    def set_ResidentialAddressIndicator(self, ResidentialAddressIndicator):
        self.ResidentialAddressIndicator = ResidentialAddressIndicator
    def _hasContent(self):
        if (
            self.AddressLine or
            self.City is not None or
            self.StateProvinceCode is not None or
            self.Town is not None or
            self.PostalCode is not None or
            self.CountryCode is not None or
            self.ResidentialAddressIndicator is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AddressType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AddressType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AddressType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AddressType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AddressType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for AddressLine_ in self.AddressLine:
            namespaceprefix_ = self.AddressLine_nsprefix_ + ':' if (UseCapturedNS_ and self.AddressLine_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAddressLine>%s</%sAddressLine>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(AddressLine_), input_name='AddressLine')), namespaceprefix_ , eol_))
        if self.City is not None:
            namespaceprefix_ = self.City_nsprefix_ + ':' if (UseCapturedNS_ and self.City_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCity>%s</%sCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.City), input_name='City')), namespaceprefix_ , eol_))
        if self.StateProvinceCode is not None:
            namespaceprefix_ = self.StateProvinceCode_nsprefix_ + ':' if (UseCapturedNS_ and self.StateProvinceCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStateProvinceCode>%s</%sStateProvinceCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.StateProvinceCode), input_name='StateProvinceCode')), namespaceprefix_ , eol_))
        if self.Town is not None:
            namespaceprefix_ = self.Town_nsprefix_ + ':' if (UseCapturedNS_ and self.Town_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTown>%s</%sTown>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Town), input_name='Town')), namespaceprefix_ , eol_))
        if self.PostalCode is not None:
            namespaceprefix_ = self.PostalCode_nsprefix_ + ':' if (UseCapturedNS_ and self.PostalCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPostalCode>%s</%sPostalCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PostalCode), input_name='PostalCode')), namespaceprefix_ , eol_))
        if self.CountryCode is not None:
            namespaceprefix_ = self.CountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryCode>%s</%sCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryCode), input_name='CountryCode')), namespaceprefix_ , eol_))
        if self.ResidentialAddressIndicator is not None:
            namespaceprefix_ = self.ResidentialAddressIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.ResidentialAddressIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sResidentialAddressIndicator>%s</%sResidentialAddressIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ResidentialAddressIndicator), input_name='ResidentialAddressIndicator')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'AddressLine':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AddressLine')
            value_ = self.gds_validate_string(value_, node, 'AddressLine')
            self.AddressLine.append(value_)
            self.AddressLine_nsprefix_ = child_.prefix
        elif nodeName_ == 'City':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'City')
            value_ = self.gds_validate_string(value_, node, 'City')
            self.City = value_
            self.City_nsprefix_ = child_.prefix
        elif nodeName_ == 'StateProvinceCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'StateProvinceCode')
            value_ = self.gds_validate_string(value_, node, 'StateProvinceCode')
            self.StateProvinceCode = value_
            self.StateProvinceCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'Town':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Town')
            value_ = self.gds_validate_string(value_, node, 'Town')
            self.Town = value_
            self.Town_nsprefix_ = child_.prefix
        elif nodeName_ == 'PostalCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PostalCode')
            value_ = self.gds_validate_string(value_, node, 'PostalCode')
            self.PostalCode = value_
            self.PostalCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'CountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryCode')
            value_ = self.gds_validate_string(value_, node, 'CountryCode')
            self.CountryCode = value_
            self.CountryCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'ResidentialAddressIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ResidentialAddressIndicator')
            value_ = self.gds_validate_string(value_, node, 'ResidentialAddressIndicator')
            self.ResidentialAddressIndicator = value_
            self.ResidentialAddressIndicator_nsprefix_ = child_.prefix
# end class AddressType


class PhoneType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Number=None, Extension=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Number = Number
        self.Number_nsprefix_ = None
        self.Extension = Extension
        self.Extension_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PhoneType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PhoneType.subclass:
            return PhoneType.subclass(*args_, **kwargs_)
        else:
            return PhoneType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Number(self):
        return self.Number
    def set_Number(self, Number):
        self.Number = Number
    def get_Extension(self):
        return self.Extension
    def set_Extension(self, Extension):
        self.Extension = Extension
    def _hasContent(self):
        if (
            self.Number is not None or
            self.Extension is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PhoneType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PhoneType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PhoneType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PhoneType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PhoneType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PhoneType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PhoneType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Number is not None:
            namespaceprefix_ = self.Number_nsprefix_ + ':' if (UseCapturedNS_ and self.Number_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumber>%s</%sNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Number), input_name='Number')), namespaceprefix_ , eol_))
        if self.Extension is not None:
            namespaceprefix_ = self.Extension_nsprefix_ + ':' if (UseCapturedNS_ and self.Extension_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExtension>%s</%sExtension>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Extension), input_name='Extension')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Number':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Number')
            value_ = self.gds_validate_string(value_, node, 'Number')
            self.Number = value_
            self.Number_nsprefix_ = child_.prefix
        elif nodeName_ == 'Extension':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Extension')
            value_ = self.gds_validate_string(value_, node, 'Extension')
            self.Extension = value_
            self.Extension_nsprefix_ = child_.prefix
# end class PhoneType


class RateCodeDescriptionType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Code=None, Description=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Code = Code
        self.Code_nsprefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RateCodeDescriptionType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RateCodeDescriptionType.subclass:
            return RateCodeDescriptionType.subclass(*args_, **kwargs_)
        else:
            return RateCodeDescriptionType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Code(self):
        return self.Code
    def set_Code(self, Code):
        self.Code = Code
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def _hasContent(self):
        if (
            self.Code is not None or
            self.Description is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RateCodeDescriptionType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RateCodeDescriptionType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RateCodeDescriptionType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RateCodeDescriptionType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RateCodeDescriptionType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RateCodeDescriptionType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RateCodeDescriptionType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Code is not None:
            namespaceprefix_ = self.Code_nsprefix_ + ':' if (UseCapturedNS_ and self.Code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCode>%s</%sCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Code), input_name='Code')), namespaceprefix_ , eol_))
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Code':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Code')
            value_ = self.gds_validate_string(value_, node, 'Code')
            self.Code = value_
            self.Code_nsprefix_ = child_.prefix
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
# end class RateCodeDescriptionType


class HandlingUnitType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Quantity=None, Type=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Quantity = Quantity
        self.Quantity_nsprefix_ = None
        self.Type = Type
        self.Type_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, HandlingUnitType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if HandlingUnitType.subclass:
            return HandlingUnitType.subclass(*args_, **kwargs_)
        else:
            return HandlingUnitType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Quantity(self):
        return self.Quantity
    def set_Quantity(self, Quantity):
        self.Quantity = Quantity
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def _hasContent(self):
        if (
            self.Quantity is not None or
            self.Type is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='HandlingUnitType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('HandlingUnitType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'HandlingUnitType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='HandlingUnitType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='HandlingUnitType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='HandlingUnitType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='HandlingUnitType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Quantity is not None:
            namespaceprefix_ = self.Quantity_nsprefix_ + ':' if (UseCapturedNS_ and self.Quantity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sQuantity>%s</%sQuantity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Quantity), input_name='Quantity')), namespaceprefix_ , eol_))
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            self.Type.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Type', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Quantity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Quantity')
            value_ = self.gds_validate_string(value_, node, 'Quantity')
            self.Quantity = value_
            self.Quantity_nsprefix_ = child_.prefix
        elif nodeName_ == 'Type':
            obj_ = RateCodeDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Type = obj_
            obj_.original_tagname_ = 'Type'
# end class HandlingUnitType


class CommodityType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CommodityID=None, Description=None, Weight=None, AdjustedWeight=None, Dimensions=None, NumberOfPieces=None, PackagingType=None, DangerousGoodsIndicator=None, CommodityValue=None, FreightClass=None, NMFCCommodityCode=None, NMFCCommodity=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CommodityID = CommodityID
        self.CommodityID_nsprefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = None
        self.Weight = Weight
        self.Weight_nsprefix_ = "frt"
        self.AdjustedWeight = AdjustedWeight
        self.AdjustedWeight_nsprefix_ = "frt"
        self.Dimensions = Dimensions
        self.Dimensions_nsprefix_ = "frt"
        self.NumberOfPieces = NumberOfPieces
        self.NumberOfPieces_nsprefix_ = None
        self.PackagingType = PackagingType
        self.PackagingType_nsprefix_ = "frt"
        self.DangerousGoodsIndicator = DangerousGoodsIndicator
        self.DangerousGoodsIndicator_nsprefix_ = None
        self.CommodityValue = CommodityValue
        self.CommodityValue_nsprefix_ = "frt"
        self.FreightClass = FreightClass
        self.FreightClass_nsprefix_ = None
        self.NMFCCommodityCode = NMFCCommodityCode
        self.NMFCCommodityCode_nsprefix_ = None
        self.NMFCCommodity = NMFCCommodity
        self.NMFCCommodity_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CommodityType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CommodityType.subclass:
            return CommodityType.subclass(*args_, **kwargs_)
        else:
            return CommodityType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CommodityID(self):
        return self.CommodityID
    def set_CommodityID(self, CommodityID):
        self.CommodityID = CommodityID
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def get_Weight(self):
        return self.Weight
    def set_Weight(self, Weight):
        self.Weight = Weight
    def get_AdjustedWeight(self):
        return self.AdjustedWeight
    def set_AdjustedWeight(self, AdjustedWeight):
        self.AdjustedWeight = AdjustedWeight
    def get_Dimensions(self):
        return self.Dimensions
    def set_Dimensions(self, Dimensions):
        self.Dimensions = Dimensions
    def get_NumberOfPieces(self):
        return self.NumberOfPieces
    def set_NumberOfPieces(self, NumberOfPieces):
        self.NumberOfPieces = NumberOfPieces
    def get_PackagingType(self):
        return self.PackagingType
    def set_PackagingType(self, PackagingType):
        self.PackagingType = PackagingType
    def get_DangerousGoodsIndicator(self):
        return self.DangerousGoodsIndicator
    def set_DangerousGoodsIndicator(self, DangerousGoodsIndicator):
        self.DangerousGoodsIndicator = DangerousGoodsIndicator
    def get_CommodityValue(self):
        return self.CommodityValue
    def set_CommodityValue(self, CommodityValue):
        self.CommodityValue = CommodityValue
    def get_FreightClass(self):
        return self.FreightClass
    def set_FreightClass(self, FreightClass):
        self.FreightClass = FreightClass
    def get_NMFCCommodityCode(self):
        return self.NMFCCommodityCode
    def set_NMFCCommodityCode(self, NMFCCommodityCode):
        self.NMFCCommodityCode = NMFCCommodityCode
    def get_NMFCCommodity(self):
        return self.NMFCCommodity
    def set_NMFCCommodity(self, NMFCCommodity):
        self.NMFCCommodity = NMFCCommodity
    def _hasContent(self):
        if (
            self.CommodityID is not None or
            self.Description is not None or
            self.Weight is not None or
            self.AdjustedWeight is not None or
            self.Dimensions is not None or
            self.NumberOfPieces is not None or
            self.PackagingType is not None or
            self.DangerousGoodsIndicator is not None or
            self.CommodityValue is not None or
            self.FreightClass is not None or
            self.NMFCCommodityCode is not None or
            self.NMFCCommodity is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CommodityType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CommodityType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CommodityType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CommodityType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CommodityType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CommodityType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CommodityType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CommodityID is not None:
            namespaceprefix_ = self.CommodityID_nsprefix_ + ':' if (UseCapturedNS_ and self.CommodityID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCommodityID>%s</%sCommodityID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CommodityID), input_name='CommodityID')), namespaceprefix_ , eol_))
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
        if self.Weight is not None:
            namespaceprefix_ = self.Weight_nsprefix_ + ':' if (UseCapturedNS_ and self.Weight_nsprefix_) else ''
            self.Weight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Weight', pretty_print=pretty_print)
        if self.AdjustedWeight is not None:
            namespaceprefix_ = self.AdjustedWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.AdjustedWeight_nsprefix_) else ''
            self.AdjustedWeight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AdjustedWeight', pretty_print=pretty_print)
        if self.Dimensions is not None:
            namespaceprefix_ = self.Dimensions_nsprefix_ + ':' if (UseCapturedNS_ and self.Dimensions_nsprefix_) else ''
            self.Dimensions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Dimensions', pretty_print=pretty_print)
        if self.NumberOfPieces is not None:
            namespaceprefix_ = self.NumberOfPieces_nsprefix_ + ':' if (UseCapturedNS_ and self.NumberOfPieces_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumberOfPieces>%s</%sNumberOfPieces>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NumberOfPieces), input_name='NumberOfPieces')), namespaceprefix_ , eol_))
        if self.PackagingType is not None:
            namespaceprefix_ = self.PackagingType_nsprefix_ + ':' if (UseCapturedNS_ and self.PackagingType_nsprefix_) else ''
            self.PackagingType.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PackagingType', pretty_print=pretty_print)
        if self.DangerousGoodsIndicator is not None:
            namespaceprefix_ = self.DangerousGoodsIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.DangerousGoodsIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDangerousGoodsIndicator>%s</%sDangerousGoodsIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DangerousGoodsIndicator), input_name='DangerousGoodsIndicator')), namespaceprefix_ , eol_))
        if self.CommodityValue is not None:
            namespaceprefix_ = self.CommodityValue_nsprefix_ + ':' if (UseCapturedNS_ and self.CommodityValue_nsprefix_) else ''
            self.CommodityValue.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CommodityValue', pretty_print=pretty_print)
        if self.FreightClass is not None:
            namespaceprefix_ = self.FreightClass_nsprefix_ + ':' if (UseCapturedNS_ and self.FreightClass_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFreightClass>%s</%sFreightClass>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FreightClass), input_name='FreightClass')), namespaceprefix_ , eol_))
        if self.NMFCCommodityCode is not None:
            namespaceprefix_ = self.NMFCCommodityCode_nsprefix_ + ':' if (UseCapturedNS_ and self.NMFCCommodityCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNMFCCommodityCode>%s</%sNMFCCommodityCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NMFCCommodityCode), input_name='NMFCCommodityCode')), namespaceprefix_ , eol_))
        if self.NMFCCommodity is not None:
            namespaceprefix_ = self.NMFCCommodity_nsprefix_ + ':' if (UseCapturedNS_ and self.NMFCCommodity_nsprefix_) else ''
            self.NMFCCommodity.export(outfile, level, namespaceprefix_, namespacedef_='', name_='NMFCCommodity', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CommodityID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CommodityID')
            value_ = self.gds_validate_string(value_, node, 'CommodityID')
            self.CommodityID = value_
            self.CommodityID_nsprefix_ = child_.prefix
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
        elif nodeName_ == 'Weight':
            obj_ = WeightType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Weight = obj_
            obj_.original_tagname_ = 'Weight'
        elif nodeName_ == 'AdjustedWeight':
            obj_ = AdjustedWeightType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdjustedWeight = obj_
            obj_.original_tagname_ = 'AdjustedWeight'
        elif nodeName_ == 'Dimensions':
            obj_ = DimensionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Dimensions = obj_
            obj_.original_tagname_ = 'Dimensions'
        elif nodeName_ == 'NumberOfPieces':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NumberOfPieces')
            value_ = self.gds_validate_string(value_, node, 'NumberOfPieces')
            self.NumberOfPieces = value_
            self.NumberOfPieces_nsprefix_ = child_.prefix
        elif nodeName_ == 'PackagingType':
            obj_ = RateCodeDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PackagingType = obj_
            obj_.original_tagname_ = 'PackagingType'
        elif nodeName_ == 'DangerousGoodsIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DangerousGoodsIndicator')
            value_ = self.gds_validate_string(value_, node, 'DangerousGoodsIndicator')
            self.DangerousGoodsIndicator = value_
            self.DangerousGoodsIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'CommodityValue':
            obj_ = CommodityValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CommodityValue = obj_
            obj_.original_tagname_ = 'CommodityValue'
        elif nodeName_ == 'FreightClass':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FreightClass')
            value_ = self.gds_validate_string(value_, node, 'FreightClass')
            self.FreightClass = value_
            self.FreightClass_nsprefix_ = child_.prefix
        elif nodeName_ == 'NMFCCommodityCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NMFCCommodityCode')
            value_ = self.gds_validate_string(value_, node, 'NMFCCommodityCode')
            self.NMFCCommodityCode = value_
            self.NMFCCommodityCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'NMFCCommodity':
            obj_ = NMFCCommodityType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.NMFCCommodity = obj_
            obj_.original_tagname_ = 'NMFCCommodity'
# end class CommodityType


class NMFCCommodityType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PrimeCode=None, SubCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PrimeCode = PrimeCode
        self.PrimeCode_nsprefix_ = None
        self.SubCode = SubCode
        self.SubCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, NMFCCommodityType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if NMFCCommodityType.subclass:
            return NMFCCommodityType.subclass(*args_, **kwargs_)
        else:
            return NMFCCommodityType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PrimeCode(self):
        return self.PrimeCode
    def set_PrimeCode(self, PrimeCode):
        self.PrimeCode = PrimeCode
    def get_SubCode(self):
        return self.SubCode
    def set_SubCode(self, SubCode):
        self.SubCode = SubCode
    def _hasContent(self):
        if (
            self.PrimeCode is not None or
            self.SubCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NMFCCommodityType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('NMFCCommodityType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'NMFCCommodityType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='NMFCCommodityType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='NMFCCommodityType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='NMFCCommodityType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NMFCCommodityType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PrimeCode is not None:
            namespaceprefix_ = self.PrimeCode_nsprefix_ + ':' if (UseCapturedNS_ and self.PrimeCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPrimeCode>%s</%sPrimeCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PrimeCode), input_name='PrimeCode')), namespaceprefix_ , eol_))
        if self.SubCode is not None:
            namespaceprefix_ = self.SubCode_nsprefix_ + ':' if (UseCapturedNS_ and self.SubCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSubCode>%s</%sSubCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SubCode), input_name='SubCode')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'PrimeCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PrimeCode')
            value_ = self.gds_validate_string(value_, node, 'PrimeCode')
            self.PrimeCode = value_
            self.PrimeCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'SubCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SubCode')
            value_ = self.gds_validate_string(value_, node, 'SubCode')
            self.SubCode = value_
            self.SubCode_nsprefix_ = child_.prefix
# end class NMFCCommodityType


class WeightType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Value=None, UnitOfMeasurement=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Value = Value
        self.Value_nsprefix_ = None
        self.UnitOfMeasurement = UnitOfMeasurement
        self.UnitOfMeasurement_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, WeightType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if WeightType.subclass:
            return WeightType.subclass(*args_, **kwargs_)
        else:
            return WeightType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def get_UnitOfMeasurement(self):
        return self.UnitOfMeasurement
    def set_UnitOfMeasurement(self, UnitOfMeasurement):
        self.UnitOfMeasurement = UnitOfMeasurement
    def _hasContent(self):
        if (
            self.Value is not None or
            self.UnitOfMeasurement is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WeightType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('WeightType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'WeightType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='WeightType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='WeightType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='WeightType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WeightType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Value is not None:
            namespaceprefix_ = self.Value_nsprefix_ + ':' if (UseCapturedNS_ and self.Value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sValue>%s</%sValue>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Value), input_name='Value')), namespaceprefix_ , eol_))
        if self.UnitOfMeasurement is not None:
            namespaceprefix_ = self.UnitOfMeasurement_nsprefix_ + ':' if (UseCapturedNS_ and self.UnitOfMeasurement_nsprefix_) else ''
            self.UnitOfMeasurement.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UnitOfMeasurement', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Value')
            value_ = self.gds_validate_string(value_, node, 'Value')
            self.Value = value_
            self.Value_nsprefix_ = child_.prefix
        elif nodeName_ == 'UnitOfMeasurement':
            obj_ = UnitOfMeasurementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UnitOfMeasurement = obj_
            obj_.original_tagname_ = 'UnitOfMeasurement'
# end class WeightType


class AdjustedWeightType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Value=None, UnitOfMeasurement=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Value = Value
        self.Value_nsprefix_ = None
        self.UnitOfMeasurement = UnitOfMeasurement
        self.UnitOfMeasurement_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AdjustedWeightType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AdjustedWeightType.subclass:
            return AdjustedWeightType.subclass(*args_, **kwargs_)
        else:
            return AdjustedWeightType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def get_UnitOfMeasurement(self):
        return self.UnitOfMeasurement
    def set_UnitOfMeasurement(self, UnitOfMeasurement):
        self.UnitOfMeasurement = UnitOfMeasurement
    def _hasContent(self):
        if (
            self.Value is not None or
            self.UnitOfMeasurement is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AdjustedWeightType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AdjustedWeightType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AdjustedWeightType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AdjustedWeightType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AdjustedWeightType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AdjustedWeightType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AdjustedWeightType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Value is not None:
            namespaceprefix_ = self.Value_nsprefix_ + ':' if (UseCapturedNS_ and self.Value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sValue>%s</%sValue>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Value), input_name='Value')), namespaceprefix_ , eol_))
        if self.UnitOfMeasurement is not None:
            namespaceprefix_ = self.UnitOfMeasurement_nsprefix_ + ':' if (UseCapturedNS_ and self.UnitOfMeasurement_nsprefix_) else ''
            self.UnitOfMeasurement.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UnitOfMeasurement', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Value')
            value_ = self.gds_validate_string(value_, node, 'Value')
            self.Value = value_
            self.Value_nsprefix_ = child_.prefix
        elif nodeName_ == 'UnitOfMeasurement':
            obj_ = UnitOfMeasurementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UnitOfMeasurement = obj_
            obj_.original_tagname_ = 'UnitOfMeasurement'
# end class AdjustedWeightType


class UnitOfMeasurementType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Code=None, Description=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Code = Code
        self.Code_nsprefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UnitOfMeasurementType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UnitOfMeasurementType.subclass:
            return UnitOfMeasurementType.subclass(*args_, **kwargs_)
        else:
            return UnitOfMeasurementType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Code(self):
        return self.Code
    def set_Code(self, Code):
        self.Code = Code
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def _hasContent(self):
        if (
            self.Code is not None or
            self.Description is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UnitOfMeasurementType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UnitOfMeasurementType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UnitOfMeasurementType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UnitOfMeasurementType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UnitOfMeasurementType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UnitOfMeasurementType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UnitOfMeasurementType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Code is not None:
            namespaceprefix_ = self.Code_nsprefix_ + ':' if (UseCapturedNS_ and self.Code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCode>%s</%sCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Code), input_name='Code')), namespaceprefix_ , eol_))
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Code':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Code')
            value_ = self.gds_validate_string(value_, node, 'Code')
            self.Code = value_
            self.Code_nsprefix_ = child_.prefix
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
# end class UnitOfMeasurementType


class DimensionsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, UnitOfMeasurement=None, Length=None, Width=None, Height=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.UnitOfMeasurement = UnitOfMeasurement
        self.UnitOfMeasurement_nsprefix_ = "frt"
        self.Length = Length
        self.Length_nsprefix_ = None
        self.Width = Width
        self.Width_nsprefix_ = None
        self.Height = Height
        self.Height_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DimensionsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DimensionsType.subclass:
            return DimensionsType.subclass(*args_, **kwargs_)
        else:
            return DimensionsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_UnitOfMeasurement(self):
        return self.UnitOfMeasurement
    def set_UnitOfMeasurement(self, UnitOfMeasurement):
        self.UnitOfMeasurement = UnitOfMeasurement
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
    def _hasContent(self):
        if (
            self.UnitOfMeasurement is not None or
            self.Length is not None or
            self.Width is not None or
            self.Height is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DimensionsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DimensionsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DimensionsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DimensionsType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DimensionsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DimensionsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DimensionsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.UnitOfMeasurement is not None:
            namespaceprefix_ = self.UnitOfMeasurement_nsprefix_ + ':' if (UseCapturedNS_ and self.UnitOfMeasurement_nsprefix_) else ''
            self.UnitOfMeasurement.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UnitOfMeasurement', pretty_print=pretty_print)
        if self.Length is not None:
            namespaceprefix_ = self.Length_nsprefix_ + ':' if (UseCapturedNS_ and self.Length_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLength>%s</%sLength>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Length), input_name='Length')), namespaceprefix_ , eol_))
        if self.Width is not None:
            namespaceprefix_ = self.Width_nsprefix_ + ':' if (UseCapturedNS_ and self.Width_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWidth>%s</%sWidth>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Width), input_name='Width')), namespaceprefix_ , eol_))
        if self.Height is not None:
            namespaceprefix_ = self.Height_nsprefix_ + ':' if (UseCapturedNS_ and self.Height_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHeight>%s</%sHeight>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Height), input_name='Height')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'UnitOfMeasurement':
            obj_ = UnitOfMeasurementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UnitOfMeasurement = obj_
            obj_.original_tagname_ = 'UnitOfMeasurement'
        elif nodeName_ == 'Length':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Length')
            value_ = self.gds_validate_string(value_, node, 'Length')
            self.Length = value_
            self.Length_nsprefix_ = child_.prefix
        elif nodeName_ == 'Width':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Width')
            value_ = self.gds_validate_string(value_, node, 'Width')
            self.Width = value_
            self.Width_nsprefix_ = child_.prefix
        elif nodeName_ == 'Height':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Height')
            value_ = self.gds_validate_string(value_, node, 'Height')
            self.Height = value_
            self.Height_nsprefix_ = child_.prefix
# end class DimensionsType


class CommodityValueType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CurrencyCode=None, MonetaryValue=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CurrencyCode = CurrencyCode
        self.CurrencyCode_nsprefix_ = None
        self.MonetaryValue = MonetaryValue
        self.MonetaryValue_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CommodityValueType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CommodityValueType.subclass:
            return CommodityValueType.subclass(*args_, **kwargs_)
        else:
            return CommodityValueType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_MonetaryValue(self):
        return self.MonetaryValue
    def set_MonetaryValue(self, MonetaryValue):
        self.MonetaryValue = MonetaryValue
    def _hasContent(self):
        if (
            self.CurrencyCode is not None or
            self.MonetaryValue is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CommodityValueType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CommodityValueType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CommodityValueType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CommodityValueType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CommodityValueType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CommodityValueType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CommodityValueType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.MonetaryValue is not None:
            namespaceprefix_ = self.MonetaryValue_nsprefix_ + ':' if (UseCapturedNS_ and self.MonetaryValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMonetaryValue>%s</%sMonetaryValue>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MonetaryValue), input_name='MonetaryValue')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'MonetaryValue':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MonetaryValue')
            value_ = self.gds_validate_string(value_, node, 'MonetaryValue')
            self.MonetaryValue = value_
            self.MonetaryValue_nsprefix_ = child_.prefix
# end class CommodityValueType


class ShipmentServiceOptionsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PickupOptions=None, DeliveryOptions=None, OverSeasLeg=None, COD=None, DangerousGoods=None, SortingAndSegregating=None, DeclaredValue=None, ExcessDeclaredValue=None, CustomsValue=None, DeliveryDutiesPaidIndicator=None, DeliveryDutiesUnpaidIndicator=None, HandlingCharge=None, CustomsClearanceIndicator=None, FreezableProtectionIndicator=None, ExtremeLengthIndicator=None, LinearFeet=None, AdjustedHeight=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PickupOptions = PickupOptions
        self.PickupOptions_nsprefix_ = "frt"
        self.DeliveryOptions = DeliveryOptions
        self.DeliveryOptions_nsprefix_ = "frt"
        self.OverSeasLeg = OverSeasLeg
        self.OverSeasLeg_nsprefix_ = "frt"
        self.COD = COD
        self.COD_nsprefix_ = "frt"
        self.DangerousGoods = DangerousGoods
        self.DangerousGoods_nsprefix_ = "frt"
        self.SortingAndSegregating = SortingAndSegregating
        self.SortingAndSegregating_nsprefix_ = "frt"
        self.DeclaredValue = DeclaredValue
        self.DeclaredValue_nsprefix_ = "frt"
        self.ExcessDeclaredValue = ExcessDeclaredValue
        self.ExcessDeclaredValue_nsprefix_ = "frt"
        self.CustomsValue = CustomsValue
        self.CustomsValue_nsprefix_ = "frt"
        self.DeliveryDutiesPaidIndicator = DeliveryDutiesPaidIndicator
        self.DeliveryDutiesPaidIndicator_nsprefix_ = None
        self.DeliveryDutiesUnpaidIndicator = DeliveryDutiesUnpaidIndicator
        self.DeliveryDutiesUnpaidIndicator_nsprefix_ = None
        self.HandlingCharge = HandlingCharge
        self.HandlingCharge_nsprefix_ = "frt"
        self.CustomsClearanceIndicator = CustomsClearanceIndicator
        self.CustomsClearanceIndicator_nsprefix_ = None
        self.FreezableProtectionIndicator = FreezableProtectionIndicator
        self.FreezableProtectionIndicator_nsprefix_ = None
        self.ExtremeLengthIndicator = ExtremeLengthIndicator
        self.ExtremeLengthIndicator_nsprefix_ = None
        self.LinearFeet = LinearFeet
        self.LinearFeet_nsprefix_ = None
        self.AdjustedHeight = AdjustedHeight
        self.AdjustedHeight_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentServiceOptionsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentServiceOptionsType.subclass:
            return ShipmentServiceOptionsType.subclass(*args_, **kwargs_)
        else:
            return ShipmentServiceOptionsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PickupOptions(self):
        return self.PickupOptions
    def set_PickupOptions(self, PickupOptions):
        self.PickupOptions = PickupOptions
    def get_DeliveryOptions(self):
        return self.DeliveryOptions
    def set_DeliveryOptions(self, DeliveryOptions):
        self.DeliveryOptions = DeliveryOptions
    def get_OverSeasLeg(self):
        return self.OverSeasLeg
    def set_OverSeasLeg(self, OverSeasLeg):
        self.OverSeasLeg = OverSeasLeg
    def get_COD(self):
        return self.COD
    def set_COD(self, COD):
        self.COD = COD
    def get_DangerousGoods(self):
        return self.DangerousGoods
    def set_DangerousGoods(self, DangerousGoods):
        self.DangerousGoods = DangerousGoods
    def get_SortingAndSegregating(self):
        return self.SortingAndSegregating
    def set_SortingAndSegregating(self, SortingAndSegregating):
        self.SortingAndSegregating = SortingAndSegregating
    def get_DeclaredValue(self):
        return self.DeclaredValue
    def set_DeclaredValue(self, DeclaredValue):
        self.DeclaredValue = DeclaredValue
    def get_ExcessDeclaredValue(self):
        return self.ExcessDeclaredValue
    def set_ExcessDeclaredValue(self, ExcessDeclaredValue):
        self.ExcessDeclaredValue = ExcessDeclaredValue
    def get_CustomsValue(self):
        return self.CustomsValue
    def set_CustomsValue(self, CustomsValue):
        self.CustomsValue = CustomsValue
    def get_DeliveryDutiesPaidIndicator(self):
        return self.DeliveryDutiesPaidIndicator
    def set_DeliveryDutiesPaidIndicator(self, DeliveryDutiesPaidIndicator):
        self.DeliveryDutiesPaidIndicator = DeliveryDutiesPaidIndicator
    def get_DeliveryDutiesUnpaidIndicator(self):
        return self.DeliveryDutiesUnpaidIndicator
    def set_DeliveryDutiesUnpaidIndicator(self, DeliveryDutiesUnpaidIndicator):
        self.DeliveryDutiesUnpaidIndicator = DeliveryDutiesUnpaidIndicator
    def get_HandlingCharge(self):
        return self.HandlingCharge
    def set_HandlingCharge(self, HandlingCharge):
        self.HandlingCharge = HandlingCharge
    def get_CustomsClearanceIndicator(self):
        return self.CustomsClearanceIndicator
    def set_CustomsClearanceIndicator(self, CustomsClearanceIndicator):
        self.CustomsClearanceIndicator = CustomsClearanceIndicator
    def get_FreezableProtectionIndicator(self):
        return self.FreezableProtectionIndicator
    def set_FreezableProtectionIndicator(self, FreezableProtectionIndicator):
        self.FreezableProtectionIndicator = FreezableProtectionIndicator
    def get_ExtremeLengthIndicator(self):
        return self.ExtremeLengthIndicator
    def set_ExtremeLengthIndicator(self, ExtremeLengthIndicator):
        self.ExtremeLengthIndicator = ExtremeLengthIndicator
    def get_LinearFeet(self):
        return self.LinearFeet
    def set_LinearFeet(self, LinearFeet):
        self.LinearFeet = LinearFeet
    def get_AdjustedHeight(self):
        return self.AdjustedHeight
    def set_AdjustedHeight(self, AdjustedHeight):
        self.AdjustedHeight = AdjustedHeight
    def _hasContent(self):
        if (
            self.PickupOptions is not None or
            self.DeliveryOptions is not None or
            self.OverSeasLeg is not None or
            self.COD is not None or
            self.DangerousGoods is not None or
            self.SortingAndSegregating is not None or
            self.DeclaredValue is not None or
            self.ExcessDeclaredValue is not None or
            self.CustomsValue is not None or
            self.DeliveryDutiesPaidIndicator is not None or
            self.DeliveryDutiesUnpaidIndicator is not None or
            self.HandlingCharge is not None or
            self.CustomsClearanceIndicator is not None or
            self.FreezableProtectionIndicator is not None or
            self.ExtremeLengthIndicator is not None or
            self.LinearFeet is not None or
            self.AdjustedHeight is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentServiceOptionsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentServiceOptionsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentServiceOptionsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentServiceOptionsType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentServiceOptionsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentServiceOptionsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentServiceOptionsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PickupOptions is not None:
            namespaceprefix_ = self.PickupOptions_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupOptions_nsprefix_) else ''
            self.PickupOptions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PickupOptions', pretty_print=pretty_print)
        if self.DeliveryOptions is not None:
            namespaceprefix_ = self.DeliveryOptions_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryOptions_nsprefix_) else ''
            self.DeliveryOptions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DeliveryOptions', pretty_print=pretty_print)
        if self.OverSeasLeg is not None:
            namespaceprefix_ = self.OverSeasLeg_nsprefix_ + ':' if (UseCapturedNS_ and self.OverSeasLeg_nsprefix_) else ''
            self.OverSeasLeg.export(outfile, level, namespaceprefix_, namespacedef_='', name_='OverSeasLeg', pretty_print=pretty_print)
        if self.COD is not None:
            namespaceprefix_ = self.COD_nsprefix_ + ':' if (UseCapturedNS_ and self.COD_nsprefix_) else ''
            self.COD.export(outfile, level, namespaceprefix_, namespacedef_='', name_='COD', pretty_print=pretty_print)
        if self.DangerousGoods is not None:
            namespaceprefix_ = self.DangerousGoods_nsprefix_ + ':' if (UseCapturedNS_ and self.DangerousGoods_nsprefix_) else ''
            self.DangerousGoods.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DangerousGoods', pretty_print=pretty_print)
        if self.SortingAndSegregating is not None:
            namespaceprefix_ = self.SortingAndSegregating_nsprefix_ + ':' if (UseCapturedNS_ and self.SortingAndSegregating_nsprefix_) else ''
            self.SortingAndSegregating.export(outfile, level, namespaceprefix_, namespacedef_='', name_='SortingAndSegregating', pretty_print=pretty_print)
        if self.DeclaredValue is not None:
            namespaceprefix_ = self.DeclaredValue_nsprefix_ + ':' if (UseCapturedNS_ and self.DeclaredValue_nsprefix_) else ''
            self.DeclaredValue.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DeclaredValue', pretty_print=pretty_print)
        if self.ExcessDeclaredValue is not None:
            namespaceprefix_ = self.ExcessDeclaredValue_nsprefix_ + ':' if (UseCapturedNS_ and self.ExcessDeclaredValue_nsprefix_) else ''
            self.ExcessDeclaredValue.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ExcessDeclaredValue', pretty_print=pretty_print)
        if self.CustomsValue is not None:
            namespaceprefix_ = self.CustomsValue_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomsValue_nsprefix_) else ''
            self.CustomsValue.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CustomsValue', pretty_print=pretty_print)
        if self.DeliveryDutiesPaidIndicator is not None:
            namespaceprefix_ = self.DeliveryDutiesPaidIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryDutiesPaidIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeliveryDutiesPaidIndicator>%s</%sDeliveryDutiesPaidIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DeliveryDutiesPaidIndicator), input_name='DeliveryDutiesPaidIndicator')), namespaceprefix_ , eol_))
        if self.DeliveryDutiesUnpaidIndicator is not None:
            namespaceprefix_ = self.DeliveryDutiesUnpaidIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryDutiesUnpaidIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeliveryDutiesUnpaidIndicator>%s</%sDeliveryDutiesUnpaidIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DeliveryDutiesUnpaidIndicator), input_name='DeliveryDutiesUnpaidIndicator')), namespaceprefix_ , eol_))
        if self.HandlingCharge is not None:
            namespaceprefix_ = self.HandlingCharge_nsprefix_ + ':' if (UseCapturedNS_ and self.HandlingCharge_nsprefix_) else ''
            self.HandlingCharge.export(outfile, level, namespaceprefix_, namespacedef_='', name_='HandlingCharge', pretty_print=pretty_print)
        if self.CustomsClearanceIndicator is not None:
            namespaceprefix_ = self.CustomsClearanceIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomsClearanceIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustomsClearanceIndicator>%s</%sCustomsClearanceIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CustomsClearanceIndicator), input_name='CustomsClearanceIndicator')), namespaceprefix_ , eol_))
        if self.FreezableProtectionIndicator is not None:
            namespaceprefix_ = self.FreezableProtectionIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.FreezableProtectionIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFreezableProtectionIndicator>%s</%sFreezableProtectionIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FreezableProtectionIndicator), input_name='FreezableProtectionIndicator')), namespaceprefix_ , eol_))
        if self.ExtremeLengthIndicator is not None:
            namespaceprefix_ = self.ExtremeLengthIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.ExtremeLengthIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExtremeLengthIndicator>%s</%sExtremeLengthIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ExtremeLengthIndicator), input_name='ExtremeLengthIndicator')), namespaceprefix_ , eol_))
        if self.LinearFeet is not None:
            namespaceprefix_ = self.LinearFeet_nsprefix_ + ':' if (UseCapturedNS_ and self.LinearFeet_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLinearFeet>%s</%sLinearFeet>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LinearFeet), input_name='LinearFeet')), namespaceprefix_ , eol_))
        if self.AdjustedHeight is not None:
            namespaceprefix_ = self.AdjustedHeight_nsprefix_ + ':' if (UseCapturedNS_ and self.AdjustedHeight_nsprefix_) else ''
            self.AdjustedHeight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AdjustedHeight', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'PickupOptions':
            obj_ = PickupOptionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PickupOptions = obj_
            obj_.original_tagname_ = 'PickupOptions'
        elif nodeName_ == 'DeliveryOptions':
            obj_ = DeliveryOptionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DeliveryOptions = obj_
            obj_.original_tagname_ = 'DeliveryOptions'
        elif nodeName_ == 'OverSeasLeg':
            obj_ = OverSeasLegType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.OverSeasLeg = obj_
            obj_.original_tagname_ = 'OverSeasLeg'
        elif nodeName_ == 'COD':
            obj_ = CODType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.COD = obj_
            obj_.original_tagname_ = 'COD'
        elif nodeName_ == 'DangerousGoods':
            obj_ = DangerousGoodsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DangerousGoods = obj_
            obj_.original_tagname_ = 'DangerousGoods'
        elif nodeName_ == 'SortingAndSegregating':
            obj_ = SortingAndSegregatingType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SortingAndSegregating = obj_
            obj_.original_tagname_ = 'SortingAndSegregating'
        elif nodeName_ == 'DeclaredValue':
            obj_ = DeclaredValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DeclaredValue = obj_
            obj_.original_tagname_ = 'DeclaredValue'
        elif nodeName_ == 'ExcessDeclaredValue':
            obj_ = DeclaredValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ExcessDeclaredValue = obj_
            obj_.original_tagname_ = 'ExcessDeclaredValue'
        elif nodeName_ == 'CustomsValue':
            obj_ = CustomsValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CustomsValue = obj_
            obj_.original_tagname_ = 'CustomsValue'
        elif nodeName_ == 'DeliveryDutiesPaidIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DeliveryDutiesPaidIndicator')
            value_ = self.gds_validate_string(value_, node, 'DeliveryDutiesPaidIndicator')
            self.DeliveryDutiesPaidIndicator = value_
            self.DeliveryDutiesPaidIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'DeliveryDutiesUnpaidIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DeliveryDutiesUnpaidIndicator')
            value_ = self.gds_validate_string(value_, node, 'DeliveryDutiesUnpaidIndicator')
            self.DeliveryDutiesUnpaidIndicator = value_
            self.DeliveryDutiesUnpaidIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'HandlingCharge':
            obj_ = HandlingChargeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.HandlingCharge = obj_
            obj_.original_tagname_ = 'HandlingCharge'
        elif nodeName_ == 'CustomsClearanceIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CustomsClearanceIndicator')
            value_ = self.gds_validate_string(value_, node, 'CustomsClearanceIndicator')
            self.CustomsClearanceIndicator = value_
            self.CustomsClearanceIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'FreezableProtectionIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FreezableProtectionIndicator')
            value_ = self.gds_validate_string(value_, node, 'FreezableProtectionIndicator')
            self.FreezableProtectionIndicator = value_
            self.FreezableProtectionIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'ExtremeLengthIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ExtremeLengthIndicator')
            value_ = self.gds_validate_string(value_, node, 'ExtremeLengthIndicator')
            self.ExtremeLengthIndicator = value_
            self.ExtremeLengthIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'LinearFeet':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LinearFeet')
            value_ = self.gds_validate_string(value_, node, 'LinearFeet')
            self.LinearFeet = value_
            self.LinearFeet_nsprefix_ = child_.prefix
        elif nodeName_ == 'AdjustedHeight':
            obj_ = AdjustedHeightType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdjustedHeight = obj_
            obj_.original_tagname_ = 'AdjustedHeight'
# end class ShipmentServiceOptionsType


class EmailInformationType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, EMailType=None, EMail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.EMailType = EMailType
        self.EMailType_nsprefix_ = "frt"
        self.EMail = EMail
        self.EMail_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EmailInformationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EmailInformationType.subclass:
            return EmailInformationType.subclass(*args_, **kwargs_)
        else:
            return EmailInformationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_EMailType(self):
        return self.EMailType
    def set_EMailType(self, EMailType):
        self.EMailType = EMailType
    def get_EMail(self):
        return self.EMail
    def set_EMail(self, EMail):
        self.EMail = EMail
    def _hasContent(self):
        if (
            self.EMailType is not None or
            self.EMail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EmailInformationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EmailInformationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EmailInformationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EmailInformationType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='EmailInformationType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EmailInformationType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EmailInformationType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.EMailType is not None:
            namespaceprefix_ = self.EMailType_nsprefix_ + ':' if (UseCapturedNS_ and self.EMailType_nsprefix_) else ''
            self.EMailType.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EMailType', pretty_print=pretty_print)
        if self.EMail is not None:
            namespaceprefix_ = self.EMail_nsprefix_ + ':' if (UseCapturedNS_ and self.EMail_nsprefix_) else ''
            self.EMail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EMail', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'EMailType':
            obj_ = RateCodeDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EMailType = obj_
            obj_.original_tagname_ = 'EMailType'
        elif nodeName_ == 'EMail':
            obj_ = EMailType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EMail = obj_
            obj_.original_tagname_ = 'EMail'
# end class EmailInformationType


class EMailType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, EMailAddress=None, EMailText=None, UndeliverableEMailAddress=None, Subject=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if EMailAddress is None:
            self.EMailAddress = []
        else:
            self.EMailAddress = EMailAddress
        self.EMailAddress_nsprefix_ = None
        self.EMailText = EMailText
        self.EMailText_nsprefix_ = None
        self.UndeliverableEMailAddress = UndeliverableEMailAddress
        self.UndeliverableEMailAddress_nsprefix_ = None
        self.Subject = Subject
        self.Subject_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EMailType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EMailType.subclass:
            return EMailType.subclass(*args_, **kwargs_)
        else:
            return EMailType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_EMailAddress(self):
        return self.EMailAddress
    def set_EMailAddress(self, EMailAddress):
        self.EMailAddress = EMailAddress
    def add_EMailAddress(self, value):
        self.EMailAddress.append(value)
    def insert_EMailAddress_at(self, index, value):
        self.EMailAddress.insert(index, value)
    def replace_EMailAddress_at(self, index, value):
        self.EMailAddress[index] = value
    def get_EMailText(self):
        return self.EMailText
    def set_EMailText(self, EMailText):
        self.EMailText = EMailText
    def get_UndeliverableEMailAddress(self):
        return self.UndeliverableEMailAddress
    def set_UndeliverableEMailAddress(self, UndeliverableEMailAddress):
        self.UndeliverableEMailAddress = UndeliverableEMailAddress
    def get_Subject(self):
        return self.Subject
    def set_Subject(self, Subject):
        self.Subject = Subject
    def _hasContent(self):
        if (
            self.EMailAddress or
            self.EMailText is not None or
            self.UndeliverableEMailAddress is not None or
            self.Subject is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EMailType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EMailType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EMailType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EMailType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='EMailType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EMailType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EMailType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for EMailAddress_ in self.EMailAddress:
            namespaceprefix_ = self.EMailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.EMailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEMailAddress>%s</%sEMailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(EMailAddress_), input_name='EMailAddress')), namespaceprefix_ , eol_))
        if self.EMailText is not None:
            namespaceprefix_ = self.EMailText_nsprefix_ + ':' if (UseCapturedNS_ and self.EMailText_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEMailText>%s</%sEMailText>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EMailText), input_name='EMailText')), namespaceprefix_ , eol_))
        if self.UndeliverableEMailAddress is not None:
            namespaceprefix_ = self.UndeliverableEMailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.UndeliverableEMailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUndeliverableEMailAddress>%s</%sUndeliverableEMailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.UndeliverableEMailAddress), input_name='UndeliverableEMailAddress')), namespaceprefix_ , eol_))
        if self.Subject is not None:
            namespaceprefix_ = self.Subject_nsprefix_ + ':' if (UseCapturedNS_ and self.Subject_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSubject>%s</%sSubject>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Subject), input_name='Subject')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'EMailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EMailAddress')
            value_ = self.gds_validate_string(value_, node, 'EMailAddress')
            self.EMailAddress.append(value_)
            self.EMailAddress_nsprefix_ = child_.prefix
        elif nodeName_ == 'EMailText':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EMailText')
            value_ = self.gds_validate_string(value_, node, 'EMailText')
            self.EMailText = value_
            self.EMailText_nsprefix_ = child_.prefix
        elif nodeName_ == 'UndeliverableEMailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'UndeliverableEMailAddress')
            value_ = self.gds_validate_string(value_, node, 'UndeliverableEMailAddress')
            self.UndeliverableEMailAddress = value_
            self.UndeliverableEMailAddress_nsprefix_ = child_.prefix
        elif nodeName_ == 'Subject':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Subject')
            value_ = self.gds_validate_string(value_, node, 'Subject')
            self.Subject = value_
            self.Subject_nsprefix_ = child_.prefix
# end class EMailType


class PickupOptionsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HolidayPickupIndicator=None, InsidePickupIndicator=None, ResidentialPickupIndicator=None, WeekendPickupIndicator=None, LiftGateRequiredIndicator=None, HoldAtAirportForPickupIndicator=None, PickupFromDoorIndicator=None, LimitedAccessPickupIndicator=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.HolidayPickupIndicator = HolidayPickupIndicator
        self.HolidayPickupIndicator_nsprefix_ = None
        self.InsidePickupIndicator = InsidePickupIndicator
        self.InsidePickupIndicator_nsprefix_ = None
        self.ResidentialPickupIndicator = ResidentialPickupIndicator
        self.ResidentialPickupIndicator_nsprefix_ = None
        self.WeekendPickupIndicator = WeekendPickupIndicator
        self.WeekendPickupIndicator_nsprefix_ = None
        self.LiftGateRequiredIndicator = LiftGateRequiredIndicator
        self.LiftGateRequiredIndicator_nsprefix_ = None
        self.HoldAtAirportForPickupIndicator = HoldAtAirportForPickupIndicator
        self.HoldAtAirportForPickupIndicator_nsprefix_ = None
        self.PickupFromDoorIndicator = PickupFromDoorIndicator
        self.PickupFromDoorIndicator_nsprefix_ = None
        self.LimitedAccessPickupIndicator = LimitedAccessPickupIndicator
        self.LimitedAccessPickupIndicator_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PickupOptionsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PickupOptionsType.subclass:
            return PickupOptionsType.subclass(*args_, **kwargs_)
        else:
            return PickupOptionsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_HolidayPickupIndicator(self):
        return self.HolidayPickupIndicator
    def set_HolidayPickupIndicator(self, HolidayPickupIndicator):
        self.HolidayPickupIndicator = HolidayPickupIndicator
    def get_InsidePickupIndicator(self):
        return self.InsidePickupIndicator
    def set_InsidePickupIndicator(self, InsidePickupIndicator):
        self.InsidePickupIndicator = InsidePickupIndicator
    def get_ResidentialPickupIndicator(self):
        return self.ResidentialPickupIndicator
    def set_ResidentialPickupIndicator(self, ResidentialPickupIndicator):
        self.ResidentialPickupIndicator = ResidentialPickupIndicator
    def get_WeekendPickupIndicator(self):
        return self.WeekendPickupIndicator
    def set_WeekendPickupIndicator(self, WeekendPickupIndicator):
        self.WeekendPickupIndicator = WeekendPickupIndicator
    def get_LiftGateRequiredIndicator(self):
        return self.LiftGateRequiredIndicator
    def set_LiftGateRequiredIndicator(self, LiftGateRequiredIndicator):
        self.LiftGateRequiredIndicator = LiftGateRequiredIndicator
    def get_HoldAtAirportForPickupIndicator(self):
        return self.HoldAtAirportForPickupIndicator
    def set_HoldAtAirportForPickupIndicator(self, HoldAtAirportForPickupIndicator):
        self.HoldAtAirportForPickupIndicator = HoldAtAirportForPickupIndicator
    def get_PickupFromDoorIndicator(self):
        return self.PickupFromDoorIndicator
    def set_PickupFromDoorIndicator(self, PickupFromDoorIndicator):
        self.PickupFromDoorIndicator = PickupFromDoorIndicator
    def get_LimitedAccessPickupIndicator(self):
        return self.LimitedAccessPickupIndicator
    def set_LimitedAccessPickupIndicator(self, LimitedAccessPickupIndicator):
        self.LimitedAccessPickupIndicator = LimitedAccessPickupIndicator
    def _hasContent(self):
        if (
            self.HolidayPickupIndicator is not None or
            self.InsidePickupIndicator is not None or
            self.ResidentialPickupIndicator is not None or
            self.WeekendPickupIndicator is not None or
            self.LiftGateRequiredIndicator is not None or
            self.HoldAtAirportForPickupIndicator is not None or
            self.PickupFromDoorIndicator is not None or
            self.LimitedAccessPickupIndicator is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupOptionsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PickupOptionsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PickupOptionsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PickupOptionsType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PickupOptionsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PickupOptionsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupOptionsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.HolidayPickupIndicator is not None:
            namespaceprefix_ = self.HolidayPickupIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.HolidayPickupIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHolidayPickupIndicator>%s</%sHolidayPickupIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HolidayPickupIndicator), input_name='HolidayPickupIndicator')), namespaceprefix_ , eol_))
        if self.InsidePickupIndicator is not None:
            namespaceprefix_ = self.InsidePickupIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.InsidePickupIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sInsidePickupIndicator>%s</%sInsidePickupIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.InsidePickupIndicator), input_name='InsidePickupIndicator')), namespaceprefix_ , eol_))
        if self.ResidentialPickupIndicator is not None:
            namespaceprefix_ = self.ResidentialPickupIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.ResidentialPickupIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sResidentialPickupIndicator>%s</%sResidentialPickupIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ResidentialPickupIndicator), input_name='ResidentialPickupIndicator')), namespaceprefix_ , eol_))
        if self.WeekendPickupIndicator is not None:
            namespaceprefix_ = self.WeekendPickupIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.WeekendPickupIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeekendPickupIndicator>%s</%sWeekendPickupIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WeekendPickupIndicator), input_name='WeekendPickupIndicator')), namespaceprefix_ , eol_))
        if self.LiftGateRequiredIndicator is not None:
            namespaceprefix_ = self.LiftGateRequiredIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.LiftGateRequiredIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLiftGateRequiredIndicator>%s</%sLiftGateRequiredIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LiftGateRequiredIndicator), input_name='LiftGateRequiredIndicator')), namespaceprefix_ , eol_))
        if self.HoldAtAirportForPickupIndicator is not None:
            namespaceprefix_ = self.HoldAtAirportForPickupIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.HoldAtAirportForPickupIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHoldAtAirportForPickupIndicator>%s</%sHoldAtAirportForPickupIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HoldAtAirportForPickupIndicator), input_name='HoldAtAirportForPickupIndicator')), namespaceprefix_ , eol_))
        if self.PickupFromDoorIndicator is not None:
            namespaceprefix_ = self.PickupFromDoorIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupFromDoorIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupFromDoorIndicator>%s</%sPickupFromDoorIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupFromDoorIndicator), input_name='PickupFromDoorIndicator')), namespaceprefix_ , eol_))
        if self.LimitedAccessPickupIndicator is not None:
            namespaceprefix_ = self.LimitedAccessPickupIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.LimitedAccessPickupIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLimitedAccessPickupIndicator>%s</%sLimitedAccessPickupIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LimitedAccessPickupIndicator), input_name='LimitedAccessPickupIndicator')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'HolidayPickupIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HolidayPickupIndicator')
            value_ = self.gds_validate_string(value_, node, 'HolidayPickupIndicator')
            self.HolidayPickupIndicator = value_
            self.HolidayPickupIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'InsidePickupIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'InsidePickupIndicator')
            value_ = self.gds_validate_string(value_, node, 'InsidePickupIndicator')
            self.InsidePickupIndicator = value_
            self.InsidePickupIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'ResidentialPickupIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ResidentialPickupIndicator')
            value_ = self.gds_validate_string(value_, node, 'ResidentialPickupIndicator')
            self.ResidentialPickupIndicator = value_
            self.ResidentialPickupIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'WeekendPickupIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WeekendPickupIndicator')
            value_ = self.gds_validate_string(value_, node, 'WeekendPickupIndicator')
            self.WeekendPickupIndicator = value_
            self.WeekendPickupIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'LiftGateRequiredIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LiftGateRequiredIndicator')
            value_ = self.gds_validate_string(value_, node, 'LiftGateRequiredIndicator')
            self.LiftGateRequiredIndicator = value_
            self.LiftGateRequiredIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'HoldAtAirportForPickupIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HoldAtAirportForPickupIndicator')
            value_ = self.gds_validate_string(value_, node, 'HoldAtAirportForPickupIndicator')
            self.HoldAtAirportForPickupIndicator = value_
            self.HoldAtAirportForPickupIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'PickupFromDoorIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupFromDoorIndicator')
            value_ = self.gds_validate_string(value_, node, 'PickupFromDoorIndicator')
            self.PickupFromDoorIndicator = value_
            self.PickupFromDoorIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'LimitedAccessPickupIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LimitedAccessPickupIndicator')
            value_ = self.gds_validate_string(value_, node, 'LimitedAccessPickupIndicator')
            self.LimitedAccessPickupIndicator = value_
            self.LimitedAccessPickupIndicator_nsprefix_ = child_.prefix
# end class PickupOptionsType


class DeliveryOptionsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CallBeforeDeliveryIndicator=None, HolidayDeliveryIndicator=None, InsideDeliveryIndicator=None, ResidentialDeliveryIndicator=None, WeekendDeliveryIndicator=None, LiftGateRequiredIndicator=None, SaturdayDeliveryIndicator=None, DeliveryToDoorIndicator=None, LimitedAccessDeliveryIndicator=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CallBeforeDeliveryIndicator = CallBeforeDeliveryIndicator
        self.CallBeforeDeliveryIndicator_nsprefix_ = None
        self.HolidayDeliveryIndicator = HolidayDeliveryIndicator
        self.HolidayDeliveryIndicator_nsprefix_ = None
        self.InsideDeliveryIndicator = InsideDeliveryIndicator
        self.InsideDeliveryIndicator_nsprefix_ = None
        self.ResidentialDeliveryIndicator = ResidentialDeliveryIndicator
        self.ResidentialDeliveryIndicator_nsprefix_ = None
        self.WeekendDeliveryIndicator = WeekendDeliveryIndicator
        self.WeekendDeliveryIndicator_nsprefix_ = None
        self.LiftGateRequiredIndicator = LiftGateRequiredIndicator
        self.LiftGateRequiredIndicator_nsprefix_ = None
        self.SaturdayDeliveryIndicator = SaturdayDeliveryIndicator
        self.SaturdayDeliveryIndicator_nsprefix_ = None
        self.DeliveryToDoorIndicator = DeliveryToDoorIndicator
        self.DeliveryToDoorIndicator_nsprefix_ = None
        self.LimitedAccessDeliveryIndicator = LimitedAccessDeliveryIndicator
        self.LimitedAccessDeliveryIndicator_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DeliveryOptionsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DeliveryOptionsType.subclass:
            return DeliveryOptionsType.subclass(*args_, **kwargs_)
        else:
            return DeliveryOptionsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CallBeforeDeliveryIndicator(self):
        return self.CallBeforeDeliveryIndicator
    def set_CallBeforeDeliveryIndicator(self, CallBeforeDeliveryIndicator):
        self.CallBeforeDeliveryIndicator = CallBeforeDeliveryIndicator
    def get_HolidayDeliveryIndicator(self):
        return self.HolidayDeliveryIndicator
    def set_HolidayDeliveryIndicator(self, HolidayDeliveryIndicator):
        self.HolidayDeliveryIndicator = HolidayDeliveryIndicator
    def get_InsideDeliveryIndicator(self):
        return self.InsideDeliveryIndicator
    def set_InsideDeliveryIndicator(self, InsideDeliveryIndicator):
        self.InsideDeliveryIndicator = InsideDeliveryIndicator
    def get_ResidentialDeliveryIndicator(self):
        return self.ResidentialDeliveryIndicator
    def set_ResidentialDeliveryIndicator(self, ResidentialDeliveryIndicator):
        self.ResidentialDeliveryIndicator = ResidentialDeliveryIndicator
    def get_WeekendDeliveryIndicator(self):
        return self.WeekendDeliveryIndicator
    def set_WeekendDeliveryIndicator(self, WeekendDeliveryIndicator):
        self.WeekendDeliveryIndicator = WeekendDeliveryIndicator
    def get_LiftGateRequiredIndicator(self):
        return self.LiftGateRequiredIndicator
    def set_LiftGateRequiredIndicator(self, LiftGateRequiredIndicator):
        self.LiftGateRequiredIndicator = LiftGateRequiredIndicator
    def get_SaturdayDeliveryIndicator(self):
        return self.SaturdayDeliveryIndicator
    def set_SaturdayDeliveryIndicator(self, SaturdayDeliveryIndicator):
        self.SaturdayDeliveryIndicator = SaturdayDeliveryIndicator
    def get_DeliveryToDoorIndicator(self):
        return self.DeliveryToDoorIndicator
    def set_DeliveryToDoorIndicator(self, DeliveryToDoorIndicator):
        self.DeliveryToDoorIndicator = DeliveryToDoorIndicator
    def get_LimitedAccessDeliveryIndicator(self):
        return self.LimitedAccessDeliveryIndicator
    def set_LimitedAccessDeliveryIndicator(self, LimitedAccessDeliveryIndicator):
        self.LimitedAccessDeliveryIndicator = LimitedAccessDeliveryIndicator
    def _hasContent(self):
        if (
            self.CallBeforeDeliveryIndicator is not None or
            self.HolidayDeliveryIndicator is not None or
            self.InsideDeliveryIndicator is not None or
            self.ResidentialDeliveryIndicator is not None or
            self.WeekendDeliveryIndicator is not None or
            self.LiftGateRequiredIndicator is not None or
            self.SaturdayDeliveryIndicator is not None or
            self.DeliveryToDoorIndicator is not None or
            self.LimitedAccessDeliveryIndicator is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeliveryOptionsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DeliveryOptionsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DeliveryOptionsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DeliveryOptionsType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DeliveryOptionsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DeliveryOptionsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeliveryOptionsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CallBeforeDeliveryIndicator is not None:
            namespaceprefix_ = self.CallBeforeDeliveryIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.CallBeforeDeliveryIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCallBeforeDeliveryIndicator>%s</%sCallBeforeDeliveryIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CallBeforeDeliveryIndicator), input_name='CallBeforeDeliveryIndicator')), namespaceprefix_ , eol_))
        if self.HolidayDeliveryIndicator is not None:
            namespaceprefix_ = self.HolidayDeliveryIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.HolidayDeliveryIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHolidayDeliveryIndicator>%s</%sHolidayDeliveryIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HolidayDeliveryIndicator), input_name='HolidayDeliveryIndicator')), namespaceprefix_ , eol_))
        if self.InsideDeliveryIndicator is not None:
            namespaceprefix_ = self.InsideDeliveryIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.InsideDeliveryIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sInsideDeliveryIndicator>%s</%sInsideDeliveryIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.InsideDeliveryIndicator), input_name='InsideDeliveryIndicator')), namespaceprefix_ , eol_))
        if self.ResidentialDeliveryIndicator is not None:
            namespaceprefix_ = self.ResidentialDeliveryIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.ResidentialDeliveryIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sResidentialDeliveryIndicator>%s</%sResidentialDeliveryIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ResidentialDeliveryIndicator), input_name='ResidentialDeliveryIndicator')), namespaceprefix_ , eol_))
        if self.WeekendDeliveryIndicator is not None:
            namespaceprefix_ = self.WeekendDeliveryIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.WeekendDeliveryIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeekendDeliveryIndicator>%s</%sWeekendDeliveryIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WeekendDeliveryIndicator), input_name='WeekendDeliveryIndicator')), namespaceprefix_ , eol_))
        if self.LiftGateRequiredIndicator is not None:
            namespaceprefix_ = self.LiftGateRequiredIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.LiftGateRequiredIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLiftGateRequiredIndicator>%s</%sLiftGateRequiredIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LiftGateRequiredIndicator), input_name='LiftGateRequiredIndicator')), namespaceprefix_ , eol_))
        if self.SaturdayDeliveryIndicator is not None:
            namespaceprefix_ = self.SaturdayDeliveryIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.SaturdayDeliveryIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSaturdayDeliveryIndicator>%s</%sSaturdayDeliveryIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SaturdayDeliveryIndicator), input_name='SaturdayDeliveryIndicator')), namespaceprefix_ , eol_))
        if self.DeliveryToDoorIndicator is not None:
            namespaceprefix_ = self.DeliveryToDoorIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryToDoorIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeliveryToDoorIndicator>%s</%sDeliveryToDoorIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DeliveryToDoorIndicator), input_name='DeliveryToDoorIndicator')), namespaceprefix_ , eol_))
        if self.LimitedAccessDeliveryIndicator is not None:
            namespaceprefix_ = self.LimitedAccessDeliveryIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.LimitedAccessDeliveryIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLimitedAccessDeliveryIndicator>%s</%sLimitedAccessDeliveryIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LimitedAccessDeliveryIndicator), input_name='LimitedAccessDeliveryIndicator')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CallBeforeDeliveryIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CallBeforeDeliveryIndicator')
            value_ = self.gds_validate_string(value_, node, 'CallBeforeDeliveryIndicator')
            self.CallBeforeDeliveryIndicator = value_
            self.CallBeforeDeliveryIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'HolidayDeliveryIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HolidayDeliveryIndicator')
            value_ = self.gds_validate_string(value_, node, 'HolidayDeliveryIndicator')
            self.HolidayDeliveryIndicator = value_
            self.HolidayDeliveryIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'InsideDeliveryIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'InsideDeliveryIndicator')
            value_ = self.gds_validate_string(value_, node, 'InsideDeliveryIndicator')
            self.InsideDeliveryIndicator = value_
            self.InsideDeliveryIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'ResidentialDeliveryIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ResidentialDeliveryIndicator')
            value_ = self.gds_validate_string(value_, node, 'ResidentialDeliveryIndicator')
            self.ResidentialDeliveryIndicator = value_
            self.ResidentialDeliveryIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'WeekendDeliveryIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WeekendDeliveryIndicator')
            value_ = self.gds_validate_string(value_, node, 'WeekendDeliveryIndicator')
            self.WeekendDeliveryIndicator = value_
            self.WeekendDeliveryIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'LiftGateRequiredIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LiftGateRequiredIndicator')
            value_ = self.gds_validate_string(value_, node, 'LiftGateRequiredIndicator')
            self.LiftGateRequiredIndicator = value_
            self.LiftGateRequiredIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'SaturdayDeliveryIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SaturdayDeliveryIndicator')
            value_ = self.gds_validate_string(value_, node, 'SaturdayDeliveryIndicator')
            self.SaturdayDeliveryIndicator = value_
            self.SaturdayDeliveryIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'DeliveryToDoorIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DeliveryToDoorIndicator')
            value_ = self.gds_validate_string(value_, node, 'DeliveryToDoorIndicator')
            self.DeliveryToDoorIndicator = value_
            self.DeliveryToDoorIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'LimitedAccessDeliveryIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LimitedAccessDeliveryIndicator')
            value_ = self.gds_validate_string(value_, node, 'LimitedAccessDeliveryIndicator')
            self.LimitedAccessDeliveryIndicator = value_
            self.LimitedAccessDeliveryIndicator_nsprefix_ = child_.prefix
# end class DeliveryOptionsType


class OverSeasLegType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Dimensions=None, Value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Dimensions = Dimensions
        self.Dimensions_nsprefix_ = "frt"
        self.Value = Value
        self.Value_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, OverSeasLegType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OverSeasLegType.subclass:
            return OverSeasLegType.subclass(*args_, **kwargs_)
        else:
            return OverSeasLegType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Dimensions(self):
        return self.Dimensions
    def set_Dimensions(self, Dimensions):
        self.Dimensions = Dimensions
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def _hasContent(self):
        if (
            self.Dimensions is not None or
            self.Value is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OverSeasLegType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OverSeasLegType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'OverSeasLegType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OverSeasLegType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='OverSeasLegType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='OverSeasLegType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OverSeasLegType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Dimensions is not None:
            namespaceprefix_ = self.Dimensions_nsprefix_ + ':' if (UseCapturedNS_ and self.Dimensions_nsprefix_) else ''
            self.Dimensions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Dimensions', pretty_print=pretty_print)
        if self.Value is not None:
            namespaceprefix_ = self.Value_nsprefix_ + ':' if (UseCapturedNS_ and self.Value_nsprefix_) else ''
            self.Value.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Value', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Dimensions':
            obj_ = DimensionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Dimensions = obj_
            obj_.original_tagname_ = 'Dimensions'
        elif nodeName_ == 'Value':
            obj_ = DimensionValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Value = obj_
            obj_.original_tagname_ = 'Value'
# end class OverSeasLegType


class DimensionType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Volume=None, Height=None, Length=None, Width=None, UnitOfMeasurement=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Volume = Volume
        self.Volume_nsprefix_ = None
        self.Height = Height
        self.Height_nsprefix_ = None
        self.Length = Length
        self.Length_nsprefix_ = None
        self.Width = Width
        self.Width_nsprefix_ = None
        self.UnitOfMeasurement = UnitOfMeasurement
        self.UnitOfMeasurement_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DimensionType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DimensionType.subclass:
            return DimensionType.subclass(*args_, **kwargs_)
        else:
            return DimensionType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Volume(self):
        return self.Volume
    def set_Volume(self, Volume):
        self.Volume = Volume
    def get_Height(self):
        return self.Height
    def set_Height(self, Height):
        self.Height = Height
    def get_Length(self):
        return self.Length
    def set_Length(self, Length):
        self.Length = Length
    def get_Width(self):
        return self.Width
    def set_Width(self, Width):
        self.Width = Width
    def get_UnitOfMeasurement(self):
        return self.UnitOfMeasurement
    def set_UnitOfMeasurement(self, UnitOfMeasurement):
        self.UnitOfMeasurement = UnitOfMeasurement
    def _hasContent(self):
        if (
            self.Volume is not None or
            self.Height is not None or
            self.Length is not None or
            self.Width is not None or
            self.UnitOfMeasurement is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DimensionType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DimensionType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DimensionType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DimensionType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DimensionType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DimensionType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DimensionType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Volume is not None:
            namespaceprefix_ = self.Volume_nsprefix_ + ':' if (UseCapturedNS_ and self.Volume_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sVolume>%s</%sVolume>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Volume), input_name='Volume')), namespaceprefix_ , eol_))
        if self.Height is not None:
            namespaceprefix_ = self.Height_nsprefix_ + ':' if (UseCapturedNS_ and self.Height_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHeight>%s</%sHeight>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Height), input_name='Height')), namespaceprefix_ , eol_))
        if self.Length is not None:
            namespaceprefix_ = self.Length_nsprefix_ + ':' if (UseCapturedNS_ and self.Length_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLength>%s</%sLength>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Length), input_name='Length')), namespaceprefix_ , eol_))
        if self.Width is not None:
            namespaceprefix_ = self.Width_nsprefix_ + ':' if (UseCapturedNS_ and self.Width_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWidth>%s</%sWidth>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Width), input_name='Width')), namespaceprefix_ , eol_))
        if self.UnitOfMeasurement is not None:
            namespaceprefix_ = self.UnitOfMeasurement_nsprefix_ + ':' if (UseCapturedNS_ and self.UnitOfMeasurement_nsprefix_) else ''
            self.UnitOfMeasurement.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UnitOfMeasurement', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Volume':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Volume')
            value_ = self.gds_validate_string(value_, node, 'Volume')
            self.Volume = value_
            self.Volume_nsprefix_ = child_.prefix
        elif nodeName_ == 'Height':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Height')
            value_ = self.gds_validate_string(value_, node, 'Height')
            self.Height = value_
            self.Height_nsprefix_ = child_.prefix
        elif nodeName_ == 'Length':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Length')
            value_ = self.gds_validate_string(value_, node, 'Length')
            self.Length = value_
            self.Length_nsprefix_ = child_.prefix
        elif nodeName_ == 'Width':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Width')
            value_ = self.gds_validate_string(value_, node, 'Width')
            self.Width = value_
            self.Width_nsprefix_ = child_.prefix
        elif nodeName_ == 'UnitOfMeasurement':
            obj_ = UnitOfMeasurementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UnitOfMeasurement = obj_
            obj_.original_tagname_ = 'UnitOfMeasurement'
# end class DimensionType


class DimensionValueType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Cube=None, CWT=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Cube = Cube
        self.Cube_nsprefix_ = "frt"
        self.CWT = CWT
        self.CWT_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DimensionValueType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DimensionValueType.subclass:
            return DimensionValueType.subclass(*args_, **kwargs_)
        else:
            return DimensionValueType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Cube(self):
        return self.Cube
    def set_Cube(self, Cube):
        self.Cube = Cube
    def get_CWT(self):
        return self.CWT
    def set_CWT(self, CWT):
        self.CWT = CWT
    def _hasContent(self):
        if (
            self.Cube is not None or
            self.CWT is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DimensionValueType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DimensionValueType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DimensionValueType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DimensionValueType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DimensionValueType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DimensionValueType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DimensionValueType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Cube is not None:
            namespaceprefix_ = self.Cube_nsprefix_ + ':' if (UseCapturedNS_ and self.Cube_nsprefix_) else ''
            self.Cube.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Cube', pretty_print=pretty_print)
        if self.CWT is not None:
            namespaceprefix_ = self.CWT_nsprefix_ + ':' if (UseCapturedNS_ and self.CWT_nsprefix_) else ''
            self.CWT.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CWT', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Cube':
            obj_ = CubeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Cube = obj_
            obj_.original_tagname_ = 'Cube'
        elif nodeName_ == 'CWT':
            obj_ = CWTType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CWT = obj_
            obj_.original_tagname_ = 'CWT'
# end class DimensionValueType


class CubeType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CurrencyCode=None, MonetaryValue=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CurrencyCode = CurrencyCode
        self.CurrencyCode_nsprefix_ = None
        self.MonetaryValue = MonetaryValue
        self.MonetaryValue_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CubeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CubeType.subclass:
            return CubeType.subclass(*args_, **kwargs_)
        else:
            return CubeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_MonetaryValue(self):
        return self.MonetaryValue
    def set_MonetaryValue(self, MonetaryValue):
        self.MonetaryValue = MonetaryValue
    def _hasContent(self):
        if (
            self.CurrencyCode is not None or
            self.MonetaryValue is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CubeType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CubeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CubeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CubeType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CubeType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CubeType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CubeType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.MonetaryValue is not None:
            namespaceprefix_ = self.MonetaryValue_nsprefix_ + ':' if (UseCapturedNS_ and self.MonetaryValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMonetaryValue>%s</%sMonetaryValue>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MonetaryValue), input_name='MonetaryValue')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'MonetaryValue':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MonetaryValue')
            value_ = self.gds_validate_string(value_, node, 'MonetaryValue')
            self.MonetaryValue = value_
            self.MonetaryValue_nsprefix_ = child_.prefix
# end class CubeType


class CWTType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CurrencyCode=None, MonetaryValue=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CurrencyCode = CurrencyCode
        self.CurrencyCode_nsprefix_ = None
        self.MonetaryValue = MonetaryValue
        self.MonetaryValue_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CWTType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CWTType.subclass:
            return CWTType.subclass(*args_, **kwargs_)
        else:
            return CWTType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_MonetaryValue(self):
        return self.MonetaryValue
    def set_MonetaryValue(self, MonetaryValue):
        self.MonetaryValue = MonetaryValue
    def _hasContent(self):
        if (
            self.CurrencyCode is not None or
            self.MonetaryValue is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CWTType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CWTType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CWTType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CWTType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CWTType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CWTType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CWTType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.MonetaryValue is not None:
            namespaceprefix_ = self.MonetaryValue_nsprefix_ + ':' if (UseCapturedNS_ and self.MonetaryValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMonetaryValue>%s</%sMonetaryValue>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MonetaryValue), input_name='MonetaryValue')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'MonetaryValue':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MonetaryValue')
            value_ = self.gds_validate_string(value_, node, 'MonetaryValue')
            self.MonetaryValue = value_
            self.MonetaryValue_nsprefix_ = child_.prefix
# end class CWTType


class CODType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CODValue=None, CODPaymentMethod=None, CODBillingOption=None, RemitTo=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CODValue = CODValue
        self.CODValue_nsprefix_ = "frt"
        self.CODPaymentMethod = CODPaymentMethod
        self.CODPaymentMethod_nsprefix_ = "frt"
        self.CODBillingOption = CODBillingOption
        self.CODBillingOption_nsprefix_ = "frt"
        self.RemitTo = RemitTo
        self.RemitTo_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CODType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CODType.subclass:
            return CODType.subclass(*args_, **kwargs_)
        else:
            return CODType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CODValue(self):
        return self.CODValue
    def set_CODValue(self, CODValue):
        self.CODValue = CODValue
    def get_CODPaymentMethod(self):
        return self.CODPaymentMethod
    def set_CODPaymentMethod(self, CODPaymentMethod):
        self.CODPaymentMethod = CODPaymentMethod
    def get_CODBillingOption(self):
        return self.CODBillingOption
    def set_CODBillingOption(self, CODBillingOption):
        self.CODBillingOption = CODBillingOption
    def get_RemitTo(self):
        return self.RemitTo
    def set_RemitTo(self, RemitTo):
        self.RemitTo = RemitTo
    def _hasContent(self):
        if (
            self.CODValue is not None or
            self.CODPaymentMethod is not None or
            self.CODBillingOption is not None or
            self.RemitTo is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CODType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CODType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CODType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CODType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CODType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CODType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CODType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CODValue is not None:
            namespaceprefix_ = self.CODValue_nsprefix_ + ':' if (UseCapturedNS_ and self.CODValue_nsprefix_) else ''
            self.CODValue.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CODValue', pretty_print=pretty_print)
        if self.CODPaymentMethod is not None:
            namespaceprefix_ = self.CODPaymentMethod_nsprefix_ + ':' if (UseCapturedNS_ and self.CODPaymentMethod_nsprefix_) else ''
            self.CODPaymentMethod.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CODPaymentMethod', pretty_print=pretty_print)
        if self.CODBillingOption is not None:
            namespaceprefix_ = self.CODBillingOption_nsprefix_ + ':' if (UseCapturedNS_ and self.CODBillingOption_nsprefix_) else ''
            self.CODBillingOption.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CODBillingOption', pretty_print=pretty_print)
        if self.RemitTo is not None:
            namespaceprefix_ = self.RemitTo_nsprefix_ + ':' if (UseCapturedNS_ and self.RemitTo_nsprefix_) else ''
            self.RemitTo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='RemitTo', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CODValue':
            obj_ = CODValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CODValue = obj_
            obj_.original_tagname_ = 'CODValue'
        elif nodeName_ == 'CODPaymentMethod':
            obj_ = RateCodeDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CODPaymentMethod = obj_
            obj_.original_tagname_ = 'CODPaymentMethod'
        elif nodeName_ == 'CODBillingOption':
            obj_ = RateCodeDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CODBillingOption = obj_
            obj_.original_tagname_ = 'CODBillingOption'
        elif nodeName_ == 'RemitTo':
            obj_ = RemitToType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.RemitTo = obj_
            obj_.original_tagname_ = 'RemitTo'
# end class CODType


class CODValueType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CurrencyCode=None, MonetaryValue=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CurrencyCode = CurrencyCode
        self.CurrencyCode_nsprefix_ = None
        self.MonetaryValue = MonetaryValue
        self.MonetaryValue_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CODValueType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CODValueType.subclass:
            return CODValueType.subclass(*args_, **kwargs_)
        else:
            return CODValueType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_MonetaryValue(self):
        return self.MonetaryValue
    def set_MonetaryValue(self, MonetaryValue):
        self.MonetaryValue = MonetaryValue
    def _hasContent(self):
        if (
            self.CurrencyCode is not None or
            self.MonetaryValue is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CODValueType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CODValueType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CODValueType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CODValueType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CODValueType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CODValueType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CODValueType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.MonetaryValue is not None:
            namespaceprefix_ = self.MonetaryValue_nsprefix_ + ':' if (UseCapturedNS_ and self.MonetaryValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMonetaryValue>%s</%sMonetaryValue>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MonetaryValue), input_name='MonetaryValue')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'MonetaryValue':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MonetaryValue')
            value_ = self.gds_validate_string(value_, node, 'MonetaryValue')
            self.MonetaryValue = value_
            self.MonetaryValue_nsprefix_ = child_.prefix
# end class CODValueType


class RemitToType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Name=None, Address=None, AttentionName=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = None
        self.Address = Address
        self.Address_nsprefix_ = "frt"
        self.AttentionName = AttentionName
        self.AttentionName_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RemitToType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RemitToType.subclass:
            return RemitToType.subclass(*args_, **kwargs_)
        else:
            return RemitToType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_AttentionName(self):
        return self.AttentionName
    def set_AttentionName(self, AttentionName):
        self.AttentionName = AttentionName
    def _hasContent(self):
        if (
            self.Name is not None or
            self.Address is not None or
            self.AttentionName is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RemitToType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RemitToType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RemitToType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RemitToType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RemitToType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RemitToType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RemitToType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName>%s</%sName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name), input_name='Name')), namespaceprefix_ , eol_))
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.AttentionName is not None:
            namespaceprefix_ = self.AttentionName_nsprefix_ + ':' if (UseCapturedNS_ and self.AttentionName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAttentionName>%s</%sAttentionName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AttentionName), input_name='AttentionName')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Name')
            value_ = self.gds_validate_string(value_, node, 'Name')
            self.Name = value_
            self.Name_nsprefix_ = child_.prefix
        elif nodeName_ == 'Address':
            obj_ = AddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'AttentionName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AttentionName')
            value_ = self.gds_validate_string(value_, node, 'AttentionName')
            self.AttentionName = value_
            self.AttentionName_nsprefix_ = child_.prefix
# end class RemitToType


class DangerousGoodsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Name=None, Phone=None, TransportationMode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = None
        self.Phone = Phone
        self.Phone_nsprefix_ = "frt"
        self.TransportationMode = TransportationMode
        self.TransportationMode_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DangerousGoodsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DangerousGoodsType.subclass:
            return DangerousGoodsType.subclass(*args_, **kwargs_)
        else:
            return DangerousGoodsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def get_Phone(self):
        return self.Phone
    def set_Phone(self, Phone):
        self.Phone = Phone
    def get_TransportationMode(self):
        return self.TransportationMode
    def set_TransportationMode(self, TransportationMode):
        self.TransportationMode = TransportationMode
    def _hasContent(self):
        if (
            self.Name is not None or
            self.Phone is not None or
            self.TransportationMode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DangerousGoodsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DangerousGoodsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DangerousGoodsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DangerousGoodsType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DangerousGoodsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DangerousGoodsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DangerousGoodsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName>%s</%sName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name), input_name='Name')), namespaceprefix_ , eol_))
        if self.Phone is not None:
            namespaceprefix_ = self.Phone_nsprefix_ + ':' if (UseCapturedNS_ and self.Phone_nsprefix_) else ''
            self.Phone.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Phone', pretty_print=pretty_print)
        if self.TransportationMode is not None:
            namespaceprefix_ = self.TransportationMode_nsprefix_ + ':' if (UseCapturedNS_ and self.TransportationMode_nsprefix_) else ''
            self.TransportationMode.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransportationMode', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Name')
            value_ = self.gds_validate_string(value_, node, 'Name')
            self.Name = value_
            self.Name_nsprefix_ = child_.prefix
        elif nodeName_ == 'Phone':
            obj_ = PhoneType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Phone = obj_
            obj_.original_tagname_ = 'Phone'
        elif nodeName_ == 'TransportationMode':
            obj_ = RateCodeDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransportationMode = obj_
            obj_.original_tagname_ = 'TransportationMode'
# end class DangerousGoodsType


class SortingAndSegregatingType(GeneratedsSuper):
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
        self.Quantity_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SortingAndSegregatingType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SortingAndSegregatingType.subclass:
            return SortingAndSegregatingType.subclass(*args_, **kwargs_)
        else:
            return SortingAndSegregatingType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Quantity(self):
        return self.Quantity
    def set_Quantity(self, Quantity):
        self.Quantity = Quantity
    def _hasContent(self):
        if (
            self.Quantity is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SortingAndSegregatingType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SortingAndSegregatingType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SortingAndSegregatingType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SortingAndSegregatingType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SortingAndSegregatingType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SortingAndSegregatingType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SortingAndSegregatingType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Quantity is not None:
            namespaceprefix_ = self.Quantity_nsprefix_ + ':' if (UseCapturedNS_ and self.Quantity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sQuantity>%s</%sQuantity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Quantity), input_name='Quantity')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Quantity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Quantity')
            value_ = self.gds_validate_string(value_, node, 'Quantity')
            self.Quantity = value_
            self.Quantity_nsprefix_ = child_.prefix
# end class SortingAndSegregatingType


class DeclaredValueType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CurrencyCode=None, MonetaryValue=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CurrencyCode = CurrencyCode
        self.CurrencyCode_nsprefix_ = None
        self.MonetaryValue = MonetaryValue
        self.MonetaryValue_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DeclaredValueType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DeclaredValueType.subclass:
            return DeclaredValueType.subclass(*args_, **kwargs_)
        else:
            return DeclaredValueType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_MonetaryValue(self):
        return self.MonetaryValue
    def set_MonetaryValue(self, MonetaryValue):
        self.MonetaryValue = MonetaryValue
    def _hasContent(self):
        if (
            self.CurrencyCode is not None or
            self.MonetaryValue is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeclaredValueType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DeclaredValueType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DeclaredValueType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DeclaredValueType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DeclaredValueType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DeclaredValueType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeclaredValueType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.MonetaryValue is not None:
            namespaceprefix_ = self.MonetaryValue_nsprefix_ + ':' if (UseCapturedNS_ and self.MonetaryValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMonetaryValue>%s</%sMonetaryValue>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MonetaryValue), input_name='MonetaryValue')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'MonetaryValue':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MonetaryValue')
            value_ = self.gds_validate_string(value_, node, 'MonetaryValue')
            self.MonetaryValue = value_
            self.MonetaryValue_nsprefix_ = child_.prefix
# end class DeclaredValueType


class CustomsValueType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CurrencyCode=None, MonetaryValue=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CurrencyCode = CurrencyCode
        self.CurrencyCode_nsprefix_ = None
        self.MonetaryValue = MonetaryValue
        self.MonetaryValue_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CustomsValueType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CustomsValueType.subclass:
            return CustomsValueType.subclass(*args_, **kwargs_)
        else:
            return CustomsValueType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_MonetaryValue(self):
        return self.MonetaryValue
    def set_MonetaryValue(self, MonetaryValue):
        self.MonetaryValue = MonetaryValue
    def _hasContent(self):
        if (
            self.CurrencyCode is not None or
            self.MonetaryValue is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CustomsValueType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CustomsValueType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CustomsValueType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CustomsValueType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CustomsValueType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CustomsValueType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CustomsValueType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.MonetaryValue is not None:
            namespaceprefix_ = self.MonetaryValue_nsprefix_ + ':' if (UseCapturedNS_ and self.MonetaryValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMonetaryValue>%s</%sMonetaryValue>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MonetaryValue), input_name='MonetaryValue')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'MonetaryValue':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MonetaryValue')
            value_ = self.gds_validate_string(value_, node, 'MonetaryValue')
            self.MonetaryValue = value_
            self.MonetaryValue_nsprefix_ = child_.prefix
# end class CustomsValueType


class HandlingChargeType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Percentage=None, Amount=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Percentage = Percentage
        self.Percentage_nsprefix_ = None
        self.Amount = Amount
        self.Amount_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, HandlingChargeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if HandlingChargeType.subclass:
            return HandlingChargeType.subclass(*args_, **kwargs_)
        else:
            return HandlingChargeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Percentage(self):
        return self.Percentage
    def set_Percentage(self, Percentage):
        self.Percentage = Percentage
    def get_Amount(self):
        return self.Amount
    def set_Amount(self, Amount):
        self.Amount = Amount
    def _hasContent(self):
        if (
            self.Percentage is not None or
            self.Amount is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='HandlingChargeType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('HandlingChargeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'HandlingChargeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='HandlingChargeType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='HandlingChargeType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='HandlingChargeType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='HandlingChargeType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Percentage is not None:
            namespaceprefix_ = self.Percentage_nsprefix_ + ':' if (UseCapturedNS_ and self.Percentage_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPercentage>%s</%sPercentage>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Percentage), input_name='Percentage')), namespaceprefix_ , eol_))
        if self.Amount is not None:
            namespaceprefix_ = self.Amount_nsprefix_ + ':' if (UseCapturedNS_ and self.Amount_nsprefix_) else ''
            self.Amount.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Amount', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Percentage':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Percentage')
            value_ = self.gds_validate_string(value_, node, 'Percentage')
            self.Percentage = value_
            self.Percentage_nsprefix_ = child_.prefix
        elif nodeName_ == 'Amount':
            obj_ = HandlingChargeAmountType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Amount = obj_
            obj_.original_tagname_ = 'Amount'
# end class HandlingChargeType


class HandlingChargeAmountType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CurrencyCode=None, MonetaryValue=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CurrencyCode = CurrencyCode
        self.CurrencyCode_nsprefix_ = None
        self.MonetaryValue = MonetaryValue
        self.MonetaryValue_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, HandlingChargeAmountType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if HandlingChargeAmountType.subclass:
            return HandlingChargeAmountType.subclass(*args_, **kwargs_)
        else:
            return HandlingChargeAmountType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_MonetaryValue(self):
        return self.MonetaryValue
    def set_MonetaryValue(self, MonetaryValue):
        self.MonetaryValue = MonetaryValue
    def _hasContent(self):
        if (
            self.CurrencyCode is not None or
            self.MonetaryValue is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='HandlingChargeAmountType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('HandlingChargeAmountType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'HandlingChargeAmountType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='HandlingChargeAmountType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='HandlingChargeAmountType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='HandlingChargeAmountType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='HandlingChargeAmountType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.MonetaryValue is not None:
            namespaceprefix_ = self.MonetaryValue_nsprefix_ + ':' if (UseCapturedNS_ and self.MonetaryValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMonetaryValue>%s</%sMonetaryValue>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MonetaryValue), input_name='MonetaryValue')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'MonetaryValue':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MonetaryValue')
            value_ = self.gds_validate_string(value_, node, 'MonetaryValue')
            self.MonetaryValue = value_
            self.MonetaryValue_nsprefix_ = child_.prefix
# end class HandlingChargeAmountType


class PickupRequestType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PickupDate=None, AdditionalComments=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PickupDate = PickupDate
        self.PickupDate_nsprefix_ = None
        self.AdditionalComments = AdditionalComments
        self.AdditionalComments_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PickupRequestType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PickupRequestType.subclass:
            return PickupRequestType.subclass(*args_, **kwargs_)
        else:
            return PickupRequestType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PickupDate(self):
        return self.PickupDate
    def set_PickupDate(self, PickupDate):
        self.PickupDate = PickupDate
    def get_AdditionalComments(self):
        return self.AdditionalComments
    def set_AdditionalComments(self, AdditionalComments):
        self.AdditionalComments = AdditionalComments
    def _hasContent(self):
        if (
            self.PickupDate is not None or
            self.AdditionalComments is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupRequestType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PickupRequestType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PickupRequestType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PickupRequestType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PickupRequestType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PickupRequestType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupRequestType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PickupDate is not None:
            namespaceprefix_ = self.PickupDate_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupDate>%s</%sPickupDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupDate), input_name='PickupDate')), namespaceprefix_ , eol_))
        if self.AdditionalComments is not None:
            namespaceprefix_ = self.AdditionalComments_nsprefix_ + ':' if (UseCapturedNS_ and self.AdditionalComments_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAdditionalComments>%s</%sAdditionalComments>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AdditionalComments), input_name='AdditionalComments')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'PickupDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupDate')
            value_ = self.gds_validate_string(value_, node, 'PickupDate')
            self.PickupDate = value_
            self.PickupDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'AdditionalComments':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AdditionalComments')
            value_ = self.gds_validate_string(value_, node, 'AdditionalComments')
            self.AdditionalComments = value_
            self.AdditionalComments_nsprefix_ = child_.prefix
# end class PickupRequestType


class RateType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Type=None, SubTypeCode=None, Factor=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Type = Type
        self.Type_nsprefix_ = "frt"
        self.SubTypeCode = SubTypeCode
        self.SubTypeCode_nsprefix_ = None
        self.Factor = Factor
        self.Factor_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RateType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RateType.subclass:
            return RateType.subclass(*args_, **kwargs_)
        else:
            return RateType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_SubTypeCode(self):
        return self.SubTypeCode
    def set_SubTypeCode(self, SubTypeCode):
        self.SubTypeCode = SubTypeCode
    def get_Factor(self):
        return self.Factor
    def set_Factor(self, Factor):
        self.Factor = Factor
    def _hasContent(self):
        if (
            self.Type is not None or
            self.SubTypeCode is not None or
            self.Factor is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RateType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RateType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RateType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RateType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RateType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RateType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RateType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            self.Type.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Type', pretty_print=pretty_print)
        if self.SubTypeCode is not None:
            namespaceprefix_ = self.SubTypeCode_nsprefix_ + ':' if (UseCapturedNS_ and self.SubTypeCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSubTypeCode>%s</%sSubTypeCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SubTypeCode), input_name='SubTypeCode')), namespaceprefix_ , eol_))
        if self.Factor is not None:
            namespaceprefix_ = self.Factor_nsprefix_ + ':' if (UseCapturedNS_ and self.Factor_nsprefix_) else ''
            self.Factor.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Factor', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Type':
            obj_ = RateCodeDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Type = obj_
            obj_.original_tagname_ = 'Type'
        elif nodeName_ == 'SubTypeCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SubTypeCode')
            value_ = self.gds_validate_string(value_, node, 'SubTypeCode')
            self.SubTypeCode = value_
            self.SubTypeCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'Factor':
            obj_ = FactorType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Factor = obj_
            obj_.original_tagname_ = 'Factor'
# end class RateType


class CommodityWeightType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CommodityID=None, Description=None, Weight=None, AdjustedWeight=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CommodityID = CommodityID
        self.CommodityID_nsprefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = None
        self.Weight = Weight
        self.Weight_nsprefix_ = "frt"
        self.AdjustedWeight = AdjustedWeight
        self.AdjustedWeight_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CommodityWeightType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CommodityWeightType.subclass:
            return CommodityWeightType.subclass(*args_, **kwargs_)
        else:
            return CommodityWeightType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CommodityID(self):
        return self.CommodityID
    def set_CommodityID(self, CommodityID):
        self.CommodityID = CommodityID
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def get_Weight(self):
        return self.Weight
    def set_Weight(self, Weight):
        self.Weight = Weight
    def get_AdjustedWeight(self):
        return self.AdjustedWeight
    def set_AdjustedWeight(self, AdjustedWeight):
        self.AdjustedWeight = AdjustedWeight
    def _hasContent(self):
        if (
            self.CommodityID is not None or
            self.Description is not None or
            self.Weight is not None or
            self.AdjustedWeight is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CommodityWeightType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CommodityWeightType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CommodityWeightType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CommodityWeightType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CommodityWeightType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CommodityWeightType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CommodityWeightType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CommodityID is not None:
            namespaceprefix_ = self.CommodityID_nsprefix_ + ':' if (UseCapturedNS_ and self.CommodityID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCommodityID>%s</%sCommodityID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CommodityID), input_name='CommodityID')), namespaceprefix_ , eol_))
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
        if self.Weight is not None:
            namespaceprefix_ = self.Weight_nsprefix_ + ':' if (UseCapturedNS_ and self.Weight_nsprefix_) else ''
            self.Weight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Weight', pretty_print=pretty_print)
        if self.AdjustedWeight is not None:
            namespaceprefix_ = self.AdjustedWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.AdjustedWeight_nsprefix_) else ''
            self.AdjustedWeight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AdjustedWeight', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CommodityID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CommodityID')
            value_ = self.gds_validate_string(value_, node, 'CommodityID')
            self.CommodityID = value_
            self.CommodityID_nsprefix_ = child_.prefix
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
        elif nodeName_ == 'Weight':
            obj_ = WeightType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Weight = obj_
            obj_.original_tagname_ = 'Weight'
        elif nodeName_ == 'AdjustedWeight':
            obj_ = AdjustedWeightType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdjustedWeight = obj_
            obj_.original_tagname_ = 'AdjustedWeight'
# end class CommodityWeightType


class FactorType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Value=None, UnitOfMeasurement=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Value = Value
        self.Value_nsprefix_ = None
        self.UnitOfMeasurement = UnitOfMeasurement
        self.UnitOfMeasurement_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, FactorType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if FactorType.subclass:
            return FactorType.subclass(*args_, **kwargs_)
        else:
            return FactorType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def get_UnitOfMeasurement(self):
        return self.UnitOfMeasurement
    def set_UnitOfMeasurement(self, UnitOfMeasurement):
        self.UnitOfMeasurement = UnitOfMeasurement
    def _hasContent(self):
        if (
            self.Value is not None or
            self.UnitOfMeasurement is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FactorType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FactorType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'FactorType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='FactorType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='FactorType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='FactorType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FactorType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Value is not None:
            namespaceprefix_ = self.Value_nsprefix_ + ':' if (UseCapturedNS_ and self.Value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sValue>%s</%sValue>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Value), input_name='Value')), namespaceprefix_ , eol_))
        if self.UnitOfMeasurement is not None:
            namespaceprefix_ = self.UnitOfMeasurement_nsprefix_ + ':' if (UseCapturedNS_ and self.UnitOfMeasurement_nsprefix_) else ''
            self.UnitOfMeasurement.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UnitOfMeasurement', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Value')
            value_ = self.gds_validate_string(value_, node, 'Value')
            self.Value = value_
            self.Value_nsprefix_ = child_.prefix
        elif nodeName_ == 'UnitOfMeasurement':
            obj_ = UnitOfMeasurementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UnitOfMeasurement = obj_
            obj_.original_tagname_ = 'UnitOfMeasurement'
# end class FactorType


class AmountType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CurrencyCode=None, MonetaryValue=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CurrencyCode = CurrencyCode
        self.CurrencyCode_nsprefix_ = None
        self.MonetaryValue = MonetaryValue
        self.MonetaryValue_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AmountType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AmountType.subclass:
            return AmountType.subclass(*args_, **kwargs_)
        else:
            return AmountType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_MonetaryValue(self):
        return self.MonetaryValue
    def set_MonetaryValue(self, MonetaryValue):
        self.MonetaryValue = MonetaryValue
    def _hasContent(self):
        if (
            self.CurrencyCode is not None or
            self.MonetaryValue is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AmountType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AmountType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AmountType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AmountType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AmountType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AmountType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AmountType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.MonetaryValue is not None:
            namespaceprefix_ = self.MonetaryValue_nsprefix_ + ':' if (UseCapturedNS_ and self.MonetaryValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMonetaryValue>%s</%sMonetaryValue>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MonetaryValue), input_name='MonetaryValue')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'MonetaryValue':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MonetaryValue')
            value_ = self.gds_validate_string(value_, node, 'MonetaryValue')
            self.MonetaryValue = value_
            self.MonetaryValue_nsprefix_ = child_.prefix
# end class AmountType


class TotalShipmentChargeType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CurrencyCode=None, MonetaryValue=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CurrencyCode = CurrencyCode
        self.CurrencyCode_nsprefix_ = None
        self.MonetaryValue = MonetaryValue
        self.MonetaryValue_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TotalShipmentChargeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TotalShipmentChargeType.subclass:
            return TotalShipmentChargeType.subclass(*args_, **kwargs_)
        else:
            return TotalShipmentChargeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_MonetaryValue(self):
        return self.MonetaryValue
    def set_MonetaryValue(self, MonetaryValue):
        self.MonetaryValue = MonetaryValue
    def _hasContent(self):
        if (
            self.CurrencyCode is not None or
            self.MonetaryValue is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TotalShipmentChargeType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TotalShipmentChargeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TotalShipmentChargeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TotalShipmentChargeType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TotalShipmentChargeType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TotalShipmentChargeType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TotalShipmentChargeType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.MonetaryValue is not None:
            namespaceprefix_ = self.MonetaryValue_nsprefix_ + ':' if (UseCapturedNS_ and self.MonetaryValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMonetaryValue>%s</%sMonetaryValue>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MonetaryValue), input_name='MonetaryValue')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'MonetaryValue':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MonetaryValue')
            value_ = self.gds_validate_string(value_, node, 'MonetaryValue')
            self.MonetaryValue = value_
            self.MonetaryValue_nsprefix_ = child_.prefix
# end class TotalShipmentChargeType


class RatingScheduleType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Code=None, Description=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Code = Code
        self.Code_nsprefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RatingScheduleType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RatingScheduleType.subclass:
            return RatingScheduleType.subclass(*args_, **kwargs_)
        else:
            return RatingScheduleType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Code(self):
        return self.Code
    def set_Code(self, Code):
        self.Code = Code
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def _hasContent(self):
        if (
            self.Code is not None or
            self.Description is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RatingScheduleType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RatingScheduleType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RatingScheduleType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RatingScheduleType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RatingScheduleType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RatingScheduleType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RatingScheduleType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Code is not None:
            namespaceprefix_ = self.Code_nsprefix_ + ':' if (UseCapturedNS_ and self.Code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCode>%s</%sCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Code), input_name='Code')), namespaceprefix_ , eol_))
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Code':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Code')
            value_ = self.gds_validate_string(value_, node, 'Code')
            self.Code = value_
            self.Code_nsprefix_ = child_.prefix
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
# end class RatingScheduleType


class TimeInTransitResponseType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DaysInTransit=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DaysInTransit = DaysInTransit
        self.DaysInTransit_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TimeInTransitResponseType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TimeInTransitResponseType.subclass:
            return TimeInTransitResponseType.subclass(*args_, **kwargs_)
        else:
            return TimeInTransitResponseType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DaysInTransit(self):
        return self.DaysInTransit
    def set_DaysInTransit(self, DaysInTransit):
        self.DaysInTransit = DaysInTransit
    def _hasContent(self):
        if (
            self.DaysInTransit is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TimeInTransitResponseType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TimeInTransitResponseType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TimeInTransitResponseType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TimeInTransitResponseType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TimeInTransitResponseType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TimeInTransitResponseType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TimeInTransitResponseType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DaysInTransit is not None:
            namespaceprefix_ = self.DaysInTransit_nsprefix_ + ':' if (UseCapturedNS_ and self.DaysInTransit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDaysInTransit>%s</%sDaysInTransit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DaysInTransit), input_name='DaysInTransit')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DaysInTransit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DaysInTransit')
            value_ = self.gds_validate_string(value_, node, 'DaysInTransit')
            self.DaysInTransit = value_
            self.DaysInTransit_nsprefix_ = child_.prefix
# end class TimeInTransitResponseType


class GFPOptionsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GPFAccesorialRateIndicator=None, OnCallInformation=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GPFAccesorialRateIndicator = GPFAccesorialRateIndicator
        self.GPFAccesorialRateIndicator_nsprefix_ = None
        self.OnCallInformation = OnCallInformation
        self.OnCallInformation_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GFPOptionsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GFPOptionsType.subclass:
            return GFPOptionsType.subclass(*args_, **kwargs_)
        else:
            return GFPOptionsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GPFAccesorialRateIndicator(self):
        return self.GPFAccesorialRateIndicator
    def set_GPFAccesorialRateIndicator(self, GPFAccesorialRateIndicator):
        self.GPFAccesorialRateIndicator = GPFAccesorialRateIndicator
    def get_OnCallInformation(self):
        return self.OnCallInformation
    def set_OnCallInformation(self, OnCallInformation):
        self.OnCallInformation = OnCallInformation
    def _hasContent(self):
        if (
            self.GPFAccesorialRateIndicator is not None or
            self.OnCallInformation is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GFPOptionsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GFPOptionsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GFPOptionsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GFPOptionsType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GFPOptionsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GFPOptionsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GFPOptionsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GPFAccesorialRateIndicator is not None:
            namespaceprefix_ = self.GPFAccesorialRateIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.GPFAccesorialRateIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGPFAccesorialRateIndicator>%s</%sGPFAccesorialRateIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GPFAccesorialRateIndicator), input_name='GPFAccesorialRateIndicator')), namespaceprefix_ , eol_))
        if self.OnCallInformation is not None:
            namespaceprefix_ = self.OnCallInformation_nsprefix_ + ':' if (UseCapturedNS_ and self.OnCallInformation_nsprefix_) else ''
            self.OnCallInformation.export(outfile, level, namespaceprefix_, namespacedef_='', name_='OnCallInformation', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'GPFAccesorialRateIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GPFAccesorialRateIndicator')
            value_ = self.gds_validate_string(value_, node, 'GPFAccesorialRateIndicator')
            self.GPFAccesorialRateIndicator = value_
            self.GPFAccesorialRateIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'OnCallInformation':
            obj_ = OnCallInformationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.OnCallInformation = obj_
            obj_.original_tagname_ = 'OnCallInformation'
# end class GFPOptionsType


class OnCallInformationType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, OnCallPickupIndicator=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.OnCallPickupIndicator = OnCallPickupIndicator
        self.OnCallPickupIndicator_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, OnCallInformationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OnCallInformationType.subclass:
            return OnCallInformationType.subclass(*args_, **kwargs_)
        else:
            return OnCallInformationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_OnCallPickupIndicator(self):
        return self.OnCallPickupIndicator
    def set_OnCallPickupIndicator(self, OnCallPickupIndicator):
        self.OnCallPickupIndicator = OnCallPickupIndicator
    def _hasContent(self):
        if (
            self.OnCallPickupIndicator is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OnCallInformationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OnCallInformationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'OnCallInformationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OnCallInformationType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='OnCallInformationType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='OnCallInformationType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OnCallInformationType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.OnCallPickupIndicator is not None:
            namespaceprefix_ = self.OnCallPickupIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.OnCallPickupIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sOnCallPickupIndicator>%s</%sOnCallPickupIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.OnCallPickupIndicator), input_name='OnCallPickupIndicator')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'OnCallPickupIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OnCallPickupIndicator')
            value_ = self.gds_validate_string(value_, node, 'OnCallPickupIndicator')
            self.OnCallPickupIndicator = value_
            self.OnCallPickupIndicator_nsprefix_ = child_.prefix
# end class OnCallInformationType


class HandlingUnitsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Quantity=None, Type=None, Dimensions=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Quantity = Quantity
        self.Quantity_nsprefix_ = None
        self.Type = Type
        self.Type_nsprefix_ = "frt"
        self.Dimensions = Dimensions
        self.Dimensions_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, HandlingUnitsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if HandlingUnitsType.subclass:
            return HandlingUnitsType.subclass(*args_, **kwargs_)
        else:
            return HandlingUnitsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Quantity(self):
        return self.Quantity
    def set_Quantity(self, Quantity):
        self.Quantity = Quantity
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_Dimensions(self):
        return self.Dimensions
    def set_Dimensions(self, Dimensions):
        self.Dimensions = Dimensions
    def _hasContent(self):
        if (
            self.Quantity is not None or
            self.Type is not None or
            self.Dimensions is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='HandlingUnitsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('HandlingUnitsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'HandlingUnitsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='HandlingUnitsType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='HandlingUnitsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='HandlingUnitsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='HandlingUnitsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Quantity is not None:
            namespaceprefix_ = self.Quantity_nsprefix_ + ':' if (UseCapturedNS_ and self.Quantity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sQuantity>%s</%sQuantity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Quantity), input_name='Quantity')), namespaceprefix_ , eol_))
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            self.Type.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Type', pretty_print=pretty_print)
        if self.Dimensions is not None:
            namespaceprefix_ = self.Dimensions_nsprefix_ + ':' if (UseCapturedNS_ and self.Dimensions_nsprefix_) else ''
            self.Dimensions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Dimensions', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Quantity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Quantity')
            value_ = self.gds_validate_string(value_, node, 'Quantity')
            self.Quantity = value_
            self.Quantity_nsprefix_ = child_.prefix
        elif nodeName_ == 'Type':
            obj_ = RateCodeDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Type = obj_
            obj_.original_tagname_ = 'Type'
        elif nodeName_ == 'Dimensions':
            obj_ = HandlingUnitsDimensionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Dimensions = obj_
            obj_.original_tagname_ = 'Dimensions'
# end class HandlingUnitsType


class HandlingUnitsDimensionsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, UnitOfMeasurement=None, Length=None, Width=None, Height=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.UnitOfMeasurement = UnitOfMeasurement
        self.UnitOfMeasurement_nsprefix_ = "frt"
        self.Length = Length
        self.Length_nsprefix_ = None
        self.Width = Width
        self.Width_nsprefix_ = None
        self.Height = Height
        self.Height_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, HandlingUnitsDimensionsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if HandlingUnitsDimensionsType.subclass:
            return HandlingUnitsDimensionsType.subclass(*args_, **kwargs_)
        else:
            return HandlingUnitsDimensionsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_UnitOfMeasurement(self):
        return self.UnitOfMeasurement
    def set_UnitOfMeasurement(self, UnitOfMeasurement):
        self.UnitOfMeasurement = UnitOfMeasurement
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
    def _hasContent(self):
        if (
            self.UnitOfMeasurement is not None or
            self.Length is not None or
            self.Width is not None or
            self.Height is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='HandlingUnitsDimensionsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('HandlingUnitsDimensionsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'HandlingUnitsDimensionsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='HandlingUnitsDimensionsType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='HandlingUnitsDimensionsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='HandlingUnitsDimensionsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='HandlingUnitsDimensionsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.UnitOfMeasurement is not None:
            namespaceprefix_ = self.UnitOfMeasurement_nsprefix_ + ':' if (UseCapturedNS_ and self.UnitOfMeasurement_nsprefix_) else ''
            self.UnitOfMeasurement.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UnitOfMeasurement', pretty_print=pretty_print)
        if self.Length is not None:
            namespaceprefix_ = self.Length_nsprefix_ + ':' if (UseCapturedNS_ and self.Length_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLength>%s</%sLength>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Length), input_name='Length')), namespaceprefix_ , eol_))
        if self.Width is not None:
            namespaceprefix_ = self.Width_nsprefix_ + ':' if (UseCapturedNS_ and self.Width_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWidth>%s</%sWidth>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Width), input_name='Width')), namespaceprefix_ , eol_))
        if self.Height is not None:
            namespaceprefix_ = self.Height_nsprefix_ + ':' if (UseCapturedNS_ and self.Height_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHeight>%s</%sHeight>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Height), input_name='Height')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'UnitOfMeasurement':
            obj_ = UnitOfMeasurementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UnitOfMeasurement = obj_
            obj_.original_tagname_ = 'UnitOfMeasurement'
        elif nodeName_ == 'Length':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Length')
            value_ = self.gds_validate_string(value_, node, 'Length')
            self.Length = value_
            self.Length_nsprefix_ = child_.prefix
        elif nodeName_ == 'Width':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Width')
            value_ = self.gds_validate_string(value_, node, 'Width')
            self.Width = value_
            self.Width_nsprefix_ = child_.prefix
        elif nodeName_ == 'Height':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Height')
            value_ = self.gds_validate_string(value_, node, 'Height')
            self.Height = value_
            self.Height_nsprefix_ = child_.prefix
# end class HandlingUnitsDimensionsType


class FreightDensityRateType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Density=None, TotalCubicFeet=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Density = Density
        self.Density_nsprefix_ = None
        self.TotalCubicFeet = TotalCubicFeet
        self.TotalCubicFeet_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, FreightDensityRateType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if FreightDensityRateType.subclass:
            return FreightDensityRateType.subclass(*args_, **kwargs_)
        else:
            return FreightDensityRateType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Density(self):
        return self.Density
    def set_Density(self, Density):
        self.Density = Density
    def get_TotalCubicFeet(self):
        return self.TotalCubicFeet
    def set_TotalCubicFeet(self, TotalCubicFeet):
        self.TotalCubicFeet = TotalCubicFeet
    def _hasContent(self):
        if (
            self.Density is not None or
            self.TotalCubicFeet is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FreightDensityRateType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FreightDensityRateType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'FreightDensityRateType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='FreightDensityRateType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='FreightDensityRateType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='FreightDensityRateType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FreightDensityRateType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Density is not None:
            namespaceprefix_ = self.Density_nsprefix_ + ':' if (UseCapturedNS_ and self.Density_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDensity>%s</%sDensity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Density), input_name='Density')), namespaceprefix_ , eol_))
        if self.TotalCubicFeet is not None:
            namespaceprefix_ = self.TotalCubicFeet_nsprefix_ + ':' if (UseCapturedNS_ and self.TotalCubicFeet_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTotalCubicFeet>%s</%sTotalCubicFeet>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TotalCubicFeet), input_name='TotalCubicFeet')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Density':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Density')
            value_ = self.gds_validate_string(value_, node, 'Density')
            self.Density = value_
            self.Density_nsprefix_ = child_.prefix
        elif nodeName_ == 'TotalCubicFeet':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TotalCubicFeet')
            value_ = self.gds_validate_string(value_, node, 'TotalCubicFeet')
            self.TotalCubicFeet = value_
            self.TotalCubicFeet_nsprefix_ = child_.prefix
# end class FreightDensityRateType


class AdjustedHeightType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Value=None, UnitOfMeasurement=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Value = Value
        self.Value_nsprefix_ = None
        self.UnitOfMeasurement = UnitOfMeasurement
        self.UnitOfMeasurement_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AdjustedHeightType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AdjustedHeightType.subclass:
            return AdjustedHeightType.subclass(*args_, **kwargs_)
        else:
            return AdjustedHeightType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def get_UnitOfMeasurement(self):
        return self.UnitOfMeasurement
    def set_UnitOfMeasurement(self, UnitOfMeasurement):
        self.UnitOfMeasurement = UnitOfMeasurement
    def _hasContent(self):
        if (
            self.Value is not None or
            self.UnitOfMeasurement is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AdjustedHeightType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AdjustedHeightType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AdjustedHeightType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AdjustedHeightType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AdjustedHeightType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AdjustedHeightType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AdjustedHeightType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Value is not None:
            namespaceprefix_ = self.Value_nsprefix_ + ':' if (UseCapturedNS_ and self.Value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sValue>%s</%sValue>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Value), input_name='Value')), namespaceprefix_ , eol_))
        if self.UnitOfMeasurement is not None:
            namespaceprefix_ = self.UnitOfMeasurement_nsprefix_ + ':' if (UseCapturedNS_ and self.UnitOfMeasurement_nsprefix_) else ''
            self.UnitOfMeasurement.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UnitOfMeasurement', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Value')
            value_ = self.gds_validate_string(value_, node, 'Value')
            self.Value = value_
            self.Value_nsprefix_ = child_.prefix
        elif nodeName_ == 'UnitOfMeasurement':
            obj_ = UnitOfMeasurementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UnitOfMeasurement = obj_
            obj_.original_tagname_ = 'UnitOfMeasurement'
# end class AdjustedHeightType


class HandlingUnitsInfoType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Quantity=None, Type=None, Dimensions=None, AdjustedHeight=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Quantity = Quantity
        self.Quantity_nsprefix_ = None
        self.Type = Type
        self.Type_nsprefix_ = "frt"
        self.Dimensions = Dimensions
        self.Dimensions_nsprefix_ = "frt"
        self.AdjustedHeight = AdjustedHeight
        self.AdjustedHeight_nsprefix_ = "frt"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, HandlingUnitsInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if HandlingUnitsInfoType.subclass:
            return HandlingUnitsInfoType.subclass(*args_, **kwargs_)
        else:
            return HandlingUnitsInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Quantity(self):
        return self.Quantity
    def set_Quantity(self, Quantity):
        self.Quantity = Quantity
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_Dimensions(self):
        return self.Dimensions
    def set_Dimensions(self, Dimensions):
        self.Dimensions = Dimensions
    def get_AdjustedHeight(self):
        return self.AdjustedHeight
    def set_AdjustedHeight(self, AdjustedHeight):
        self.AdjustedHeight = AdjustedHeight
    def _hasContent(self):
        if (
            self.Quantity is not None or
            self.Type is not None or
            self.Dimensions is not None or
            self.AdjustedHeight is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='HandlingUnitsInfoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('HandlingUnitsInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'HandlingUnitsInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='HandlingUnitsInfoType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='HandlingUnitsInfoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='HandlingUnitsInfoType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='HandlingUnitsInfoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Quantity is not None:
            namespaceprefix_ = self.Quantity_nsprefix_ + ':' if (UseCapturedNS_ and self.Quantity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sQuantity>%s</%sQuantity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Quantity), input_name='Quantity')), namespaceprefix_ , eol_))
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            self.Type.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Type', pretty_print=pretty_print)
        if self.Dimensions is not None:
            namespaceprefix_ = self.Dimensions_nsprefix_ + ':' if (UseCapturedNS_ and self.Dimensions_nsprefix_) else ''
            self.Dimensions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Dimensions', pretty_print=pretty_print)
        if self.AdjustedHeight is not None:
            namespaceprefix_ = self.AdjustedHeight_nsprefix_ + ':' if (UseCapturedNS_ and self.AdjustedHeight_nsprefix_) else ''
            self.AdjustedHeight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AdjustedHeight', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Quantity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Quantity')
            value_ = self.gds_validate_string(value_, node, 'Quantity')
            self.Quantity = value_
            self.Quantity_nsprefix_ = child_.prefix
        elif nodeName_ == 'Type':
            obj_ = RateCodeDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Type = obj_
            obj_.original_tagname_ = 'Type'
        elif nodeName_ == 'Dimensions':
            obj_ = HandlingUnitsDimensionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Dimensions = obj_
            obj_.original_tagname_ = 'Dimensions'
        elif nodeName_ == 'AdjustedHeight':
            obj_ = AdjustedHeightType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdjustedHeight = obj_
            obj_.original_tagname_ = 'AdjustedHeight'
# end class HandlingUnitsInfoType


class ClientInformationType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Property=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Property is None:
            self.Property = []
        else:
            self.Property = Property
        self.Property_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ClientInformationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ClientInformationType.subclass:
            return ClientInformationType.subclass(*args_, **kwargs_)
        else:
            return ClientInformationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Property(self):
        return self.Property
    def set_Property(self, Property):
        self.Property = Property
    def add_Property(self, value):
        self.Property.append(value)
    def insert_Property_at(self, index, value):
        self.Property.insert(index, value)
    def replace_Property_at(self, index, value):
        self.Property[index] = value
    def _hasContent(self):
        if (
            self.Property
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='common:', namespacedef_='', name_='ClientInformationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ClientInformationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ClientInformationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ClientInformationType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ClientInformationType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='common:', name_='ClientInformationType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='common:', namespacedef_='', name_='ClientInformationType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Property_ in self.Property:
            namespaceprefix_ = self.Property_nsprefix_ + ':' if (UseCapturedNS_ and self.Property_nsprefix_) else ''
            Property_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Property', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Property':
            obj_ = PropertyType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Property.append(obj_)
            obj_.original_tagname_ = 'Property'
# end class ClientInformationType


class RequestType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, RequestOption=None, SubVersion=None, TransactionReference=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if RequestOption is None:
            self.RequestOption = []
        else:
            self.RequestOption = RequestOption
        self.RequestOption_nsprefix_ = None
        self.SubVersion = SubVersion
        self.SubVersion_nsprefix_ = None
        self.TransactionReference = TransactionReference
        self.TransactionReference_nsprefix_ = "common"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RequestType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RequestType.subclass:
            return RequestType.subclass(*args_, **kwargs_)
        else:
            return RequestType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_RequestOption(self):
        return self.RequestOption
    def set_RequestOption(self, RequestOption):
        self.RequestOption = RequestOption
    def add_RequestOption(self, value):
        self.RequestOption.append(value)
    def insert_RequestOption_at(self, index, value):
        self.RequestOption.insert(index, value)
    def replace_RequestOption_at(self, index, value):
        self.RequestOption[index] = value
    def get_SubVersion(self):
        return self.SubVersion
    def set_SubVersion(self, SubVersion):
        self.SubVersion = SubVersion
    def get_TransactionReference(self):
        return self.TransactionReference
    def set_TransactionReference(self, TransactionReference):
        self.TransactionReference = TransactionReference
    def _hasContent(self):
        if (
            self.RequestOption or
            self.SubVersion is not None or
            self.TransactionReference is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='common:', namespacedef_='', name_='RequestType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RequestType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RequestType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RequestType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RequestType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='common:', name_='RequestType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='common:', namespacedef_='', name_='RequestType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for RequestOption_ in self.RequestOption:
            namespaceprefix_ = self.RequestOption_nsprefix_ + ':' if (UseCapturedNS_ and self.RequestOption_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRequestOption>%s</%sRequestOption>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(RequestOption_), input_name='RequestOption')), namespaceprefix_ , eol_))
        if self.SubVersion is not None:
            namespaceprefix_ = self.SubVersion_nsprefix_ + ':' if (UseCapturedNS_ and self.SubVersion_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSubVersion>%s</%sSubVersion>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SubVersion), input_name='SubVersion')), namespaceprefix_ , eol_))
        if self.TransactionReference is not None:
            namespaceprefix_ = self.TransactionReference_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionReference_nsprefix_) else ''
            self.TransactionReference.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionReference', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'RequestOption':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RequestOption')
            value_ = self.gds_validate_string(value_, node, 'RequestOption')
            self.RequestOption.append(value_)
            self.RequestOption_nsprefix_ = child_.prefix
        elif nodeName_ == 'SubVersion':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SubVersion')
            value_ = self.gds_validate_string(value_, node, 'SubVersion')
            self.SubVersion = value_
            self.SubVersion_nsprefix_ = child_.prefix
        elif nodeName_ == 'TransactionReference':
            obj_ = TransactionReferenceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionReference = obj_
            obj_.original_tagname_ = 'TransactionReference'
# end class RequestType


class TransactionReferenceType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CustomerContext=None, TransactionIdentifier=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CustomerContext = CustomerContext
        self.CustomerContext_nsprefix_ = None
        self.TransactionIdentifier = TransactionIdentifier
        self.TransactionIdentifier_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TransactionReferenceType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TransactionReferenceType.subclass:
            return TransactionReferenceType.subclass(*args_, **kwargs_)
        else:
            return TransactionReferenceType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CustomerContext(self):
        return self.CustomerContext
    def set_CustomerContext(self, CustomerContext):
        self.CustomerContext = CustomerContext
    def get_TransactionIdentifier(self):
        return self.TransactionIdentifier
    def set_TransactionIdentifier(self, TransactionIdentifier):
        self.TransactionIdentifier = TransactionIdentifier
    def _hasContent(self):
        if (
            self.CustomerContext is not None or
            self.TransactionIdentifier is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='common:', namespacedef_='', name_='TransactionReferenceType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TransactionReferenceType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TransactionReferenceType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TransactionReferenceType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TransactionReferenceType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='common:', name_='TransactionReferenceType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='common:', namespacedef_='', name_='TransactionReferenceType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CustomerContext is not None:
            namespaceprefix_ = self.CustomerContext_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomerContext_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustomerContext>%s</%sCustomerContext>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CustomerContext), input_name='CustomerContext')), namespaceprefix_ , eol_))
        if self.TransactionIdentifier is not None:
            namespaceprefix_ = self.TransactionIdentifier_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionIdentifier_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTransactionIdentifier>%s</%sTransactionIdentifier>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TransactionIdentifier), input_name='TransactionIdentifier')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CustomerContext':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CustomerContext')
            value_ = self.gds_validate_string(value_, node, 'CustomerContext')
            self.CustomerContext = value_
            self.CustomerContext_nsprefix_ = child_.prefix
        elif nodeName_ == 'TransactionIdentifier':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TransactionIdentifier')
            value_ = self.gds_validate_string(value_, node, 'TransactionIdentifier')
            self.TransactionIdentifier = value_
            self.TransactionIdentifier_nsprefix_ = child_.prefix
# end class TransactionReferenceType


class ResponseType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ResponseStatus=None, Alert=None, AlertDetail=None, TransactionReference=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ResponseStatus = ResponseStatus
        self.ResponseStatus_nsprefix_ = "common"
        if Alert is None:
            self.Alert = []
        else:
            self.Alert = Alert
        self.Alert_nsprefix_ = "common"
        if AlertDetail is None:
            self.AlertDetail = []
        else:
            self.AlertDetail = AlertDetail
        self.AlertDetail_nsprefix_ = "common"
        self.TransactionReference = TransactionReference
        self.TransactionReference_nsprefix_ = "common"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ResponseType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ResponseType.subclass:
            return ResponseType.subclass(*args_, **kwargs_)
        else:
            return ResponseType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ResponseStatus(self):
        return self.ResponseStatus
    def set_ResponseStatus(self, ResponseStatus):
        self.ResponseStatus = ResponseStatus
    def get_Alert(self):
        return self.Alert
    def set_Alert(self, Alert):
        self.Alert = Alert
    def add_Alert(self, value):
        self.Alert.append(value)
    def insert_Alert_at(self, index, value):
        self.Alert.insert(index, value)
    def replace_Alert_at(self, index, value):
        self.Alert[index] = value
    def get_AlertDetail(self):
        return self.AlertDetail
    def set_AlertDetail(self, AlertDetail):
        self.AlertDetail = AlertDetail
    def add_AlertDetail(self, value):
        self.AlertDetail.append(value)
    def insert_AlertDetail_at(self, index, value):
        self.AlertDetail.insert(index, value)
    def replace_AlertDetail_at(self, index, value):
        self.AlertDetail[index] = value
    def get_TransactionReference(self):
        return self.TransactionReference
    def set_TransactionReference(self, TransactionReference):
        self.TransactionReference = TransactionReference
    def _hasContent(self):
        if (
            self.ResponseStatus is not None or
            self.Alert or
            self.AlertDetail or
            self.TransactionReference is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='common:', namespacedef_='', name_='ResponseType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ResponseType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ResponseType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ResponseType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ResponseType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='common:', name_='ResponseType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='common:', namespacedef_='', name_='ResponseType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ResponseStatus is not None:
            namespaceprefix_ = self.ResponseStatus_nsprefix_ + ':' if (UseCapturedNS_ and self.ResponseStatus_nsprefix_) else ''
            self.ResponseStatus.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ResponseStatus', pretty_print=pretty_print)
        for Alert_ in self.Alert:
            namespaceprefix_ = self.Alert_nsprefix_ + ':' if (UseCapturedNS_ and self.Alert_nsprefix_) else ''
            Alert_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Alert', pretty_print=pretty_print)
        for AlertDetail_ in self.AlertDetail:
            namespaceprefix_ = self.AlertDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.AlertDetail_nsprefix_) else ''
            AlertDetail_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AlertDetail', pretty_print=pretty_print)
        if self.TransactionReference is not None:
            namespaceprefix_ = self.TransactionReference_nsprefix_ + ':' if (UseCapturedNS_ and self.TransactionReference_nsprefix_) else ''
            self.TransactionReference.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TransactionReference', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ResponseStatus':
            obj_ = CodeDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ResponseStatus = obj_
            obj_.original_tagname_ = 'ResponseStatus'
        elif nodeName_ == 'Alert':
            obj_ = CodeDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Alert.append(obj_)
            obj_.original_tagname_ = 'Alert'
        elif nodeName_ == 'AlertDetail':
            obj_ = DetailType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AlertDetail.append(obj_)
            obj_.original_tagname_ = 'AlertDetail'
        elif nodeName_ == 'TransactionReference':
            obj_ = TransactionReferenceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TransactionReference = obj_
            obj_.original_tagname_ = 'TransactionReference'
# end class ResponseType


class CodeDescriptionType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Code=None, Description=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Code = Code
        self.Code_nsprefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CodeDescriptionType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CodeDescriptionType.subclass:
            return CodeDescriptionType.subclass(*args_, **kwargs_)
        else:
            return CodeDescriptionType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Code(self):
        return self.Code
    def set_Code(self, Code):
        self.Code = Code
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def _hasContent(self):
        if (
            self.Code is not None or
            self.Description is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='common:', namespacedef_='', name_='CodeDescriptionType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CodeDescriptionType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CodeDescriptionType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CodeDescriptionType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CodeDescriptionType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='common:', name_='CodeDescriptionType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='common:', namespacedef_='', name_='CodeDescriptionType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Code is not None:
            namespaceprefix_ = self.Code_nsprefix_ + ':' if (UseCapturedNS_ and self.Code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCode>%s</%sCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Code), input_name='Code')), namespaceprefix_ , eol_))
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Code':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Code')
            value_ = self.gds_validate_string(value_, node, 'Code')
            self.Code = value_
            self.Code_nsprefix_ = child_.prefix
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
# end class CodeDescriptionType


class DetailType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Code=None, Description=None, ElementLevelInformation=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Code = Code
        self.Code_nsprefix_ = None
        self.Description = Description
        self.Description_nsprefix_ = None
        self.ElementLevelInformation = ElementLevelInformation
        self.ElementLevelInformation_nsprefix_ = "common"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DetailType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DetailType.subclass:
            return DetailType.subclass(*args_, **kwargs_)
        else:
            return DetailType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Code(self):
        return self.Code
    def set_Code(self, Code):
        self.Code = Code
    def get_Description(self):
        return self.Description
    def set_Description(self, Description):
        self.Description = Description
    def get_ElementLevelInformation(self):
        return self.ElementLevelInformation
    def set_ElementLevelInformation(self, ElementLevelInformation):
        self.ElementLevelInformation = ElementLevelInformation
    def _hasContent(self):
        if (
            self.Code is not None or
            self.Description is not None or
            self.ElementLevelInformation is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='common:', namespacedef_='', name_='DetailType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DetailType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DetailType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DetailType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DetailType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='common:', name_='DetailType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='common:', namespacedef_='', name_='DetailType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Code is not None:
            namespaceprefix_ = self.Code_nsprefix_ + ':' if (UseCapturedNS_ and self.Code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCode>%s</%sCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Code), input_name='Code')), namespaceprefix_ , eol_))
        if self.Description is not None:
            namespaceprefix_ = self.Description_nsprefix_ + ':' if (UseCapturedNS_ and self.Description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescription>%s</%sDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Description), input_name='Description')), namespaceprefix_ , eol_))
        if self.ElementLevelInformation is not None:
            namespaceprefix_ = self.ElementLevelInformation_nsprefix_ + ':' if (UseCapturedNS_ and self.ElementLevelInformation_nsprefix_) else ''
            self.ElementLevelInformation.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ElementLevelInformation', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Code':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Code')
            value_ = self.gds_validate_string(value_, node, 'Code')
            self.Code = value_
            self.Code_nsprefix_ = child_.prefix
        elif nodeName_ == 'Description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Description')
            value_ = self.gds_validate_string(value_, node, 'Description')
            self.Description = value_
            self.Description_nsprefix_ = child_.prefix
        elif nodeName_ == 'ElementLevelInformation':
            obj_ = ElementLevelInformationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ElementLevelInformation = obj_
            obj_.original_tagname_ = 'ElementLevelInformation'
# end class DetailType


class ElementLevelInformationType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Level=None, ElementIdentifier=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Level = Level
        self.Level_nsprefix_ = None
        if ElementIdentifier is None:
            self.ElementIdentifier = []
        else:
            self.ElementIdentifier = ElementIdentifier
        self.ElementIdentifier_nsprefix_ = "common"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ElementLevelInformationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ElementLevelInformationType.subclass:
            return ElementLevelInformationType.subclass(*args_, **kwargs_)
        else:
            return ElementLevelInformationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Level(self):
        return self.Level
    def set_Level(self, Level):
        self.Level = Level
    def get_ElementIdentifier(self):
        return self.ElementIdentifier
    def set_ElementIdentifier(self, ElementIdentifier):
        self.ElementIdentifier = ElementIdentifier
    def add_ElementIdentifier(self, value):
        self.ElementIdentifier.append(value)
    def insert_ElementIdentifier_at(self, index, value):
        self.ElementIdentifier.insert(index, value)
    def replace_ElementIdentifier_at(self, index, value):
        self.ElementIdentifier[index] = value
    def _hasContent(self):
        if (
            self.Level is not None or
            self.ElementIdentifier
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='common:', namespacedef_='', name_='ElementLevelInformationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ElementLevelInformationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ElementLevelInformationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ElementLevelInformationType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ElementLevelInformationType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='common:', name_='ElementLevelInformationType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='common:', namespacedef_='', name_='ElementLevelInformationType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Level is not None:
            namespaceprefix_ = self.Level_nsprefix_ + ':' if (UseCapturedNS_ and self.Level_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLevel>%s</%sLevel>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Level), input_name='Level')), namespaceprefix_ , eol_))
        for ElementIdentifier_ in self.ElementIdentifier:
            namespaceprefix_ = self.ElementIdentifier_nsprefix_ + ':' if (UseCapturedNS_ and self.ElementIdentifier_nsprefix_) else ''
            ElementIdentifier_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ElementIdentifier', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Level':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Level')
            value_ = self.gds_validate_string(value_, node, 'Level')
            self.Level = value_
            self.Level_nsprefix_ = child_.prefix
        elif nodeName_ == 'ElementIdentifier':
            obj_ = ElementIdentifierType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ElementIdentifier.append(obj_)
            obj_.original_tagname_ = 'ElementIdentifier'
# end class ElementLevelInformationType


class ElementIdentifierType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Code=None, Value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Code = Code
        self.Code_nsprefix_ = None
        self.Value = Value
        self.Value_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ElementIdentifierType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ElementIdentifierType.subclass:
            return ElementIdentifierType.subclass(*args_, **kwargs_)
        else:
            return ElementIdentifierType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Code(self):
        return self.Code
    def set_Code(self, Code):
        self.Code = Code
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def _hasContent(self):
        if (
            self.Code is not None or
            self.Value is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='common:', namespacedef_='', name_='ElementIdentifierType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ElementIdentifierType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ElementIdentifierType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ElementIdentifierType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ElementIdentifierType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='common:', name_='ElementIdentifierType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='common:', namespacedef_='', name_='ElementIdentifierType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Code is not None:
            namespaceprefix_ = self.Code_nsprefix_ + ':' if (UseCapturedNS_ and self.Code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCode>%s</%sCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Code), input_name='Code')), namespaceprefix_ , eol_))
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
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Code':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Code')
            value_ = self.gds_validate_string(value_, node, 'Code')
            self.Code = value_
            self.Code_nsprefix_ = child_.prefix
        elif nodeName_ == 'Value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Value')
            value_ = self.gds_validate_string(value_, node, 'Value')
            self.Value = value_
            self.Value_nsprefix_ = child_.prefix
# end class ElementIdentifierType


class PropertyType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Key=None, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Key = _cast(None, Key)
        self.Key_nsprefix_ = None
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PropertyType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PropertyType.subclass:
            return PropertyType.subclass(*args_, **kwargs_)
        else:
            return PropertyType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Key(self):
        return self.Key
    def set_Key(self, Key):
        self.Key = Key
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def _hasContent(self):
        if (
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_)
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PropertyType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PropertyType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PropertyType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PropertyType')
        if self._hasContent():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PropertyType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PropertyType'):
        if self.Key is not None and 'Key' not in already_processed:
            already_processed.add('Key')
            outfile.write(' Key=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.Key), input_name='Key')), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PropertyType', fromsubclass_=False, pretty_print=True):
        pass
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('Key', node)
        if value is not None and 'Key' not in already_processed:
            already_processed.add('Key')
            self.Key = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class PropertyType


GDSClassesMapping = {
    'ClientInformation': ClientInformationType,
    'Request': RequestType,
    'Response': ResponseType,
}


USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def get_root_tag(node):
    tag = Tag_pattern_.match(node.tag).groups()[-1]
    prefix_tag = TagNamePrefix + tag
    rootClass = GDSClassesMapping.get(prefix_tag)
    if rootClass is None:
        rootClass = globals().get(prefix_tag)
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
        rootTag = 'FreightRateRequest'
        rootClass = FreightRateRequest
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
               mapping=None, reverse_mapping=None, nsmap=None):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'FreightRateRequest'
        rootClass = FreightRateRequest
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if mapping is None:
        mapping = {}
    if reverse_mapping is None:
        reverse_mapping = {}
    rootElement = rootObj.to_etree(
        None, name_=rootTag, mapping_=mapping,
        reverse_mapping_=reverse_mapping, nsmap_=nsmap)
    reverse_node_mapping = rootObj.gds_reverse_node_mapping(mapping)
    # Enable Python to collect the space used by the DOM.
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
    return rootObj, rootElement, mapping, reverse_node_mapping


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
        rootTag = 'FreightRateRequest'
        rootClass = FreightRateRequest
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:frt="http://www.ups.com/XMLSchema/XOLTWS/FreightRate/v1.0"')
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
        rootTag = 'FreightRateRequest'
        rootClass = FreightRateRequest
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from freight_rate_web_service_schema import *\n\n')
        sys.stdout.write('import freight_rate_web_service_schema as model_\n\n')
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
NamespaceToDefMappings_ = {'http://www.ups.com/XMLSchema/XOLTWS/Common/v1.0': [('ClientInformationType',
                                                      './schemas/common.xsd',
                                                      'CT'),
                                                     ('RequestType',
                                                      './schemas/common.xsd',
                                                      'CT'),
                                                     ('TransactionReferenceType',
                                                      './schemas/common.xsd',
                                                      'CT'),
                                                     ('ResponseType',
                                                      './schemas/common.xsd',
                                                      'CT'),
                                                     ('CodeDescriptionType',
                                                      './schemas/common.xsd',
                                                      'CT'),
                                                     ('DetailType',
                                                      './schemas/common.xsd',
                                                      'CT'),
                                                     ('ElementLevelInformationType',
                                                      './schemas/common.xsd',
                                                      'CT'),
                                                     ('ElementIdentifierType',
                                                      './schemas/common.xsd',
                                                      'CT')],
 'http://www.ups.com/XMLSchema/XOLTWS/FreightRate/v1.0': [('AccountType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('ShipmentTotalWeightType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('HandlingUnitWeightType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('AlternateRatesResponseType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('ShipFromType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('ShipToType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('PaymentInformationType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('PayerType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('AddressType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('PhoneType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('RateCodeDescriptionType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('HandlingUnitType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('CommodityType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('NMFCCommodityType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('WeightType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('AdjustedWeightType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('UnitOfMeasurementType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('DimensionsType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('CommodityValueType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('ShipmentServiceOptionsType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('EmailInformationType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('EMailType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('PickupOptionsType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('DeliveryOptionsType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('OverSeasLegType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('DimensionType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('DimensionValueType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('CubeType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('CWTType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('CODType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('CODValueType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('RemitToType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('DangerousGoodsType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('SortingAndSegregatingType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('DeclaredValueType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('CustomsValueType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('HandlingChargeType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('HandlingChargeAmountType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('PickupRequestType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('RateType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('CommodityWeightType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('FactorType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('AmountType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('TotalShipmentChargeType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('RatingScheduleType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('TimeInTransitResponseType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('GFPOptionsType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('OnCallInformationType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('HandlingUnitsType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('HandlingUnitsDimensionsType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('FreightDensityRateType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('AdjustedHeightType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT'),
                                                          ('HandlingUnitsInfoType',
                                                           './schemas/FreightRateWebServiceSchema.xsd',
                                                           'CT')]}

__all__ = [
    "AccountType",
    "AddressType",
    "AdjustedHeightType",
    "AdjustedWeightType",
    "AlternateRatesResponseType",
    "AmountType",
    "CODType",
    "CODValueType",
    "CWTType",
    "ClientInformationType",
    "CodeDescriptionType",
    "CommodityType",
    "CommodityValueType",
    "CommodityWeightType",
    "CubeType",
    "CustomsValueType",
    "DangerousGoodsType",
    "DeclaredValueType",
    "DeliveryOptionsType",
    "DetailType",
    "DimensionType",
    "DimensionValueType",
    "DimensionsType",
    "EMailType",
    "ElementIdentifierType",
    "ElementLevelInformationType",
    "EmailInformationType",
    "FactorType",
    "FreightDensityRateType",
    "FreightRateRequest",
    "FreightRateResponse",
    "GFPOptionsType",
    "HandlingChargeAmountType",
    "HandlingChargeType",
    "HandlingUnitType",
    "HandlingUnitWeightType",
    "HandlingUnitsDimensionsType",
    "HandlingUnitsInfoType",
    "HandlingUnitsType",
    "NMFCCommodityType",
    "OnCallInformationType",
    "OverSeasLegType",
    "PayerType",
    "PaymentInformationType",
    "PhoneType",
    "PickupOptionsType",
    "PickupRequestType",
    "PropertyType",
    "RateCodeDescriptionType",
    "RateType",
    "RatingScheduleType",
    "RemitToType",
    "RequestType",
    "ResponseType",
    "ShipFromType",
    "ShipToType",
    "ShipmentServiceOptionsType",
    "ShipmentTotalWeightType",
    "SortingAndSegregatingType",
    "TimeInTransitResponseType",
    "TotalShipmentChargeType",
    "TransactionReferenceType",
    "UnitOfMeasurementType",
    "WeightType"
]
