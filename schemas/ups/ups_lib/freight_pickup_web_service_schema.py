#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Mon Aug  1 09:54:46 2022 by generateDS.py version 2.40.13.
# Python 3.8.7 (v3.8.7:6503f05dd5, Dec 21 2020, 12:45:15)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './ups_lib/freight_pickup_web_service_schema.py')
#
# Command line arguments:
#   ./schemas/FreightPickupWebServiceSchema.xsd
#
# Command line:
#   /Users/danielk/Documents/karrio/karrio/.venv/karrio/bin/generateDS --no-namespace-defs -o "./ups_lib/freight_pickup_web_service_schema.py" ./schemas/FreightPickupWebServiceSchema.xsd
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


class FreightPickupRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Request=None, PickupRequestConfirmationNumber=None, DestinationPostalCode=None, DestinationCountryCode=None, Requester=None, ShipFrom=None, ShipTo=None, PickupDate=None, EarliestTimeReady=None, LatestTimeReady=None, ShipmentServiceOptions=None, ShipmentDetail=None, ExistingShipmentID=None, POM=None, PickupInstructions=None, AdditionalComments=None, HandlingInstructions=None, SpecialInstructions=None, DeliveryInstructions=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Request = Request
        self.Request_nsprefix_ = "common"
        self.PickupRequestConfirmationNumber = PickupRequestConfirmationNumber
        self.PickupRequestConfirmationNumber_nsprefix_ = None
        self.DestinationPostalCode = DestinationPostalCode
        self.DestinationPostalCode_nsprefix_ = None
        self.DestinationCountryCode = DestinationCountryCode
        self.DestinationCountryCode_nsprefix_ = None
        self.Requester = Requester
        self.Requester_nsprefix_ = "fpu"
        self.ShipFrom = ShipFrom
        self.ShipFrom_nsprefix_ = "fpu"
        self.ShipTo = ShipTo
        self.ShipTo_nsprefix_ = "fpu"
        self.PickupDate = PickupDate
        self.PickupDate_nsprefix_ = None
        self.EarliestTimeReady = EarliestTimeReady
        self.EarliestTimeReady_nsprefix_ = None
        self.LatestTimeReady = LatestTimeReady
        self.LatestTimeReady_nsprefix_ = None
        self.ShipmentServiceOptions = ShipmentServiceOptions
        self.ShipmentServiceOptions_nsprefix_ = "fpu"
        if ShipmentDetail is None:
            self.ShipmentDetail = []
        else:
            self.ShipmentDetail = ShipmentDetail
        self.ShipmentDetail_nsprefix_ = "fpu"
        self.ExistingShipmentID = ExistingShipmentID
        self.ExistingShipmentID_nsprefix_ = "fpu"
        self.POM = POM
        self.POM_nsprefix_ = "fpu"
        self.PickupInstructions = PickupInstructions
        self.PickupInstructions_nsprefix_ = None
        self.AdditionalComments = AdditionalComments
        self.AdditionalComments_nsprefix_ = None
        self.HandlingInstructions = HandlingInstructions
        self.HandlingInstructions_nsprefix_ = None
        self.SpecialInstructions = SpecialInstructions
        self.SpecialInstructions_nsprefix_ = None
        self.DeliveryInstructions = DeliveryInstructions
        self.DeliveryInstructions_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, FreightPickupRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if FreightPickupRequest.subclass:
            return FreightPickupRequest.subclass(*args_, **kwargs_)
        else:
            return FreightPickupRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Request(self):
        return self.Request
    def set_Request(self, Request):
        self.Request = Request
    def get_PickupRequestConfirmationNumber(self):
        return self.PickupRequestConfirmationNumber
    def set_PickupRequestConfirmationNumber(self, PickupRequestConfirmationNumber):
        self.PickupRequestConfirmationNumber = PickupRequestConfirmationNumber
    def get_DestinationPostalCode(self):
        return self.DestinationPostalCode
    def set_DestinationPostalCode(self, DestinationPostalCode):
        self.DestinationPostalCode = DestinationPostalCode
    def get_DestinationCountryCode(self):
        return self.DestinationCountryCode
    def set_DestinationCountryCode(self, DestinationCountryCode):
        self.DestinationCountryCode = DestinationCountryCode
    def get_Requester(self):
        return self.Requester
    def set_Requester(self, Requester):
        self.Requester = Requester
    def get_ShipFrom(self):
        return self.ShipFrom
    def set_ShipFrom(self, ShipFrom):
        self.ShipFrom = ShipFrom
    def get_ShipTo(self):
        return self.ShipTo
    def set_ShipTo(self, ShipTo):
        self.ShipTo = ShipTo
    def get_PickupDate(self):
        return self.PickupDate
    def set_PickupDate(self, PickupDate):
        self.PickupDate = PickupDate
    def get_EarliestTimeReady(self):
        return self.EarliestTimeReady
    def set_EarliestTimeReady(self, EarliestTimeReady):
        self.EarliestTimeReady = EarliestTimeReady
    def get_LatestTimeReady(self):
        return self.LatestTimeReady
    def set_LatestTimeReady(self, LatestTimeReady):
        self.LatestTimeReady = LatestTimeReady
    def get_ShipmentServiceOptions(self):
        return self.ShipmentServiceOptions
    def set_ShipmentServiceOptions(self, ShipmentServiceOptions):
        self.ShipmentServiceOptions = ShipmentServiceOptions
    def get_ShipmentDetail(self):
        return self.ShipmentDetail
    def set_ShipmentDetail(self, ShipmentDetail):
        self.ShipmentDetail = ShipmentDetail
    def add_ShipmentDetail(self, value):
        self.ShipmentDetail.append(value)
    def insert_ShipmentDetail_at(self, index, value):
        self.ShipmentDetail.insert(index, value)
    def replace_ShipmentDetail_at(self, index, value):
        self.ShipmentDetail[index] = value
    def get_ExistingShipmentID(self):
        return self.ExistingShipmentID
    def set_ExistingShipmentID(self, ExistingShipmentID):
        self.ExistingShipmentID = ExistingShipmentID
    def get_POM(self):
        return self.POM
    def set_POM(self, POM):
        self.POM = POM
    def get_PickupInstructions(self):
        return self.PickupInstructions
    def set_PickupInstructions(self, PickupInstructions):
        self.PickupInstructions = PickupInstructions
    def get_AdditionalComments(self):
        return self.AdditionalComments
    def set_AdditionalComments(self, AdditionalComments):
        self.AdditionalComments = AdditionalComments
    def get_HandlingInstructions(self):
        return self.HandlingInstructions
    def set_HandlingInstructions(self, HandlingInstructions):
        self.HandlingInstructions = HandlingInstructions
    def get_SpecialInstructions(self):
        return self.SpecialInstructions
    def set_SpecialInstructions(self, SpecialInstructions):
        self.SpecialInstructions = SpecialInstructions
    def get_DeliveryInstructions(self):
        return self.DeliveryInstructions
    def set_DeliveryInstructions(self, DeliveryInstructions):
        self.DeliveryInstructions = DeliveryInstructions
    def _hasContent(self):
        if (
            self.Request is not None or
            self.PickupRequestConfirmationNumber is not None or
            self.DestinationPostalCode is not None or
            self.DestinationCountryCode is not None or
            self.Requester is not None or
            self.ShipFrom is not None or
            self.ShipTo is not None or
            self.PickupDate is not None or
            self.EarliestTimeReady is not None or
            self.LatestTimeReady is not None or
            self.ShipmentServiceOptions is not None or
            self.ShipmentDetail or
            self.ExistingShipmentID is not None or
            self.POM is not None or
            self.PickupInstructions is not None or
            self.AdditionalComments is not None or
            self.HandlingInstructions is not None or
            self.SpecialInstructions is not None or
            self.DeliveryInstructions is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FreightPickupRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FreightPickupRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'FreightPickupRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='FreightPickupRequest')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='FreightPickupRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='FreightPickupRequest'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FreightPickupRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Request is not None:
            namespaceprefix_ = self.Request_nsprefix_ + ':' if (UseCapturedNS_ and self.Request_nsprefix_) else ''
            self.Request.export(outfile, level, namespaceprefix_='common:', namespacedef_='', name_='Request', pretty_print=pretty_print)
        if self.PickupRequestConfirmationNumber is not None:
            namespaceprefix_ = self.PickupRequestConfirmationNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupRequestConfirmationNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupRequestConfirmationNumber>%s</%sPickupRequestConfirmationNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupRequestConfirmationNumber), input_name='PickupRequestConfirmationNumber')), namespaceprefix_ , eol_))
        if self.DestinationPostalCode is not None:
            namespaceprefix_ = self.DestinationPostalCode_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationPostalCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDestinationPostalCode>%s</%sDestinationPostalCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DestinationPostalCode), input_name='DestinationPostalCode')), namespaceprefix_ , eol_))
        if self.DestinationCountryCode is not None:
            namespaceprefix_ = self.DestinationCountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationCountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDestinationCountryCode>%s</%sDestinationCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DestinationCountryCode), input_name='DestinationCountryCode')), namespaceprefix_ , eol_))
        if self.Requester is not None:
            namespaceprefix_ = self.Requester_nsprefix_ + ':' if (UseCapturedNS_ and self.Requester_nsprefix_) else ''
            self.Requester.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Requester', pretty_print=pretty_print)
        if self.ShipFrom is not None:
            namespaceprefix_ = self.ShipFrom_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipFrom_nsprefix_) else ''
            self.ShipFrom.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipFrom', pretty_print=pretty_print)
        if self.ShipTo is not None:
            namespaceprefix_ = self.ShipTo_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipTo_nsprefix_) else ''
            self.ShipTo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipTo', pretty_print=pretty_print)
        if self.PickupDate is not None:
            namespaceprefix_ = self.PickupDate_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupDate>%s</%sPickupDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupDate), input_name='PickupDate')), namespaceprefix_ , eol_))
        if self.EarliestTimeReady is not None:
            namespaceprefix_ = self.EarliestTimeReady_nsprefix_ + ':' if (UseCapturedNS_ and self.EarliestTimeReady_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEarliestTimeReady>%s</%sEarliestTimeReady>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EarliestTimeReady), input_name='EarliestTimeReady')), namespaceprefix_ , eol_))
        if self.LatestTimeReady is not None:
            namespaceprefix_ = self.LatestTimeReady_nsprefix_ + ':' if (UseCapturedNS_ and self.LatestTimeReady_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLatestTimeReady>%s</%sLatestTimeReady>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LatestTimeReady), input_name='LatestTimeReady')), namespaceprefix_ , eol_))
        if self.ShipmentServiceOptions is not None:
            namespaceprefix_ = self.ShipmentServiceOptions_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentServiceOptions_nsprefix_) else ''
            self.ShipmentServiceOptions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentServiceOptions', pretty_print=pretty_print)
        for ShipmentDetail_ in self.ShipmentDetail:
            namespaceprefix_ = self.ShipmentDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentDetail_nsprefix_) else ''
            ShipmentDetail_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentDetail', pretty_print=pretty_print)
        if self.ExistingShipmentID is not None:
            namespaceprefix_ = self.ExistingShipmentID_nsprefix_ + ':' if (UseCapturedNS_ and self.ExistingShipmentID_nsprefix_) else ''
            self.ExistingShipmentID.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ExistingShipmentID', pretty_print=pretty_print)
        if self.POM is not None:
            namespaceprefix_ = self.POM_nsprefix_ + ':' if (UseCapturedNS_ and self.POM_nsprefix_) else ''
            self.POM.export(outfile, level, namespaceprefix_, namespacedef_='', name_='POM', pretty_print=pretty_print)
        if self.PickupInstructions is not None:
            namespaceprefix_ = self.PickupInstructions_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupInstructions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupInstructions>%s</%sPickupInstructions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupInstructions), input_name='PickupInstructions')), namespaceprefix_ , eol_))
        if self.AdditionalComments is not None:
            namespaceprefix_ = self.AdditionalComments_nsprefix_ + ':' if (UseCapturedNS_ and self.AdditionalComments_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAdditionalComments>%s</%sAdditionalComments>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AdditionalComments), input_name='AdditionalComments')), namespaceprefix_ , eol_))
        if self.HandlingInstructions is not None:
            namespaceprefix_ = self.HandlingInstructions_nsprefix_ + ':' if (UseCapturedNS_ and self.HandlingInstructions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHandlingInstructions>%s</%sHandlingInstructions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HandlingInstructions), input_name='HandlingInstructions')), namespaceprefix_ , eol_))
        if self.SpecialInstructions is not None:
            namespaceprefix_ = self.SpecialInstructions_nsprefix_ + ':' if (UseCapturedNS_ and self.SpecialInstructions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSpecialInstructions>%s</%sSpecialInstructions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SpecialInstructions), input_name='SpecialInstructions')), namespaceprefix_ , eol_))
        if self.DeliveryInstructions is not None:
            namespaceprefix_ = self.DeliveryInstructions_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryInstructions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeliveryInstructions>%s</%sDeliveryInstructions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DeliveryInstructions), input_name='DeliveryInstructions')), namespaceprefix_ , eol_))
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
        elif nodeName_ == 'PickupRequestConfirmationNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupRequestConfirmationNumber')
            value_ = self.gds_validate_string(value_, node, 'PickupRequestConfirmationNumber')
            self.PickupRequestConfirmationNumber = value_
            self.PickupRequestConfirmationNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'DestinationPostalCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DestinationPostalCode')
            value_ = self.gds_validate_string(value_, node, 'DestinationPostalCode')
            self.DestinationPostalCode = value_
            self.DestinationPostalCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'DestinationCountryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DestinationCountryCode')
            value_ = self.gds_validate_string(value_, node, 'DestinationCountryCode')
            self.DestinationCountryCode = value_
            self.DestinationCountryCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'Requester':
            obj_ = RequesterType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Requester = obj_
            obj_.original_tagname_ = 'Requester'
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
        elif nodeName_ == 'PickupDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupDate')
            value_ = self.gds_validate_string(value_, node, 'PickupDate')
            self.PickupDate = value_
            self.PickupDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'EarliestTimeReady':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EarliestTimeReady')
            value_ = self.gds_validate_string(value_, node, 'EarliestTimeReady')
            self.EarliestTimeReady = value_
            self.EarliestTimeReady_nsprefix_ = child_.prefix
        elif nodeName_ == 'LatestTimeReady':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LatestTimeReady')
            value_ = self.gds_validate_string(value_, node, 'LatestTimeReady')
            self.LatestTimeReady = value_
            self.LatestTimeReady_nsprefix_ = child_.prefix
        elif nodeName_ == 'ShipmentServiceOptions':
            obj_ = ShipmentServiceOptionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentServiceOptions = obj_
            obj_.original_tagname_ = 'ShipmentServiceOptions'
        elif nodeName_ == 'ShipmentDetail':
            obj_ = ShipmentDetailType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentDetail.append(obj_)
            obj_.original_tagname_ = 'ShipmentDetail'
        elif nodeName_ == 'ExistingShipmentID':
            obj_ = ExistingShipmentIDType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ExistingShipmentID = obj_
            obj_.original_tagname_ = 'ExistingShipmentID'
        elif nodeName_ == 'POM':
            obj_ = POMType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.POM = obj_
            obj_.original_tagname_ = 'POM'
        elif nodeName_ == 'PickupInstructions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupInstructions')
            value_ = self.gds_validate_string(value_, node, 'PickupInstructions')
            self.PickupInstructions = value_
            self.PickupInstructions_nsprefix_ = child_.prefix
        elif nodeName_ == 'AdditionalComments':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AdditionalComments')
            value_ = self.gds_validate_string(value_, node, 'AdditionalComments')
            self.AdditionalComments = value_
            self.AdditionalComments_nsprefix_ = child_.prefix
        elif nodeName_ == 'HandlingInstructions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HandlingInstructions')
            value_ = self.gds_validate_string(value_, node, 'HandlingInstructions')
            self.HandlingInstructions = value_
            self.HandlingInstructions_nsprefix_ = child_.prefix
        elif nodeName_ == 'SpecialInstructions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SpecialInstructions')
            value_ = self.gds_validate_string(value_, node, 'SpecialInstructions')
            self.SpecialInstructions = value_
            self.SpecialInstructions_nsprefix_ = child_.prefix
        elif nodeName_ == 'DeliveryInstructions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DeliveryInstructions')
            value_ = self.gds_validate_string(value_, node, 'DeliveryInstructions')
            self.DeliveryInstructions = value_
            self.DeliveryInstructions_nsprefix_ = child_.prefix
# end class FreightPickupRequest


class FreightCancelPickupRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Request=None, PickupRequestConfirmationNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Request = Request
        self.Request_nsprefix_ = "common"
        self.PickupRequestConfirmationNumber = PickupRequestConfirmationNumber
        self.PickupRequestConfirmationNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, FreightCancelPickupRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if FreightCancelPickupRequest.subclass:
            return FreightCancelPickupRequest.subclass(*args_, **kwargs_)
        else:
            return FreightCancelPickupRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Request(self):
        return self.Request
    def set_Request(self, Request):
        self.Request = Request
    def get_PickupRequestConfirmationNumber(self):
        return self.PickupRequestConfirmationNumber
    def set_PickupRequestConfirmationNumber(self, PickupRequestConfirmationNumber):
        self.PickupRequestConfirmationNumber = PickupRequestConfirmationNumber
    def _hasContent(self):
        if (
            self.Request is not None or
            self.PickupRequestConfirmationNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FreightCancelPickupRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FreightCancelPickupRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'FreightCancelPickupRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='FreightCancelPickupRequest')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='FreightCancelPickupRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='FreightCancelPickupRequest'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FreightCancelPickupRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Request is not None:
            namespaceprefix_ = self.Request_nsprefix_ + ':' if (UseCapturedNS_ and self.Request_nsprefix_) else ''
            self.Request.export(outfile, level, namespaceprefix_='common:', namespacedef_='', name_='Request', pretty_print=pretty_print)
        if self.PickupRequestConfirmationNumber is not None:
            namespaceprefix_ = self.PickupRequestConfirmationNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupRequestConfirmationNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupRequestConfirmationNumber>%s</%sPickupRequestConfirmationNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupRequestConfirmationNumber), input_name='PickupRequestConfirmationNumber')), namespaceprefix_ , eol_))
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
        elif nodeName_ == 'PickupRequestConfirmationNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupRequestConfirmationNumber')
            value_ = self.gds_validate_string(value_, node, 'PickupRequestConfirmationNumber')
            self.PickupRequestConfirmationNumber = value_
            self.PickupRequestConfirmationNumber_nsprefix_ = child_.prefix
# end class FreightCancelPickupRequest


class FreightPickupResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Response=None, PickupRequestConfirmationNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Response = Response
        self.Response_nsprefix_ = "common"
        self.PickupRequestConfirmationNumber = PickupRequestConfirmationNumber
        self.PickupRequestConfirmationNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, FreightPickupResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if FreightPickupResponse.subclass:
            return FreightPickupResponse.subclass(*args_, **kwargs_)
        else:
            return FreightPickupResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Response(self):
        return self.Response
    def set_Response(self, Response):
        self.Response = Response
    def get_PickupRequestConfirmationNumber(self):
        return self.PickupRequestConfirmationNumber
    def set_PickupRequestConfirmationNumber(self, PickupRequestConfirmationNumber):
        self.PickupRequestConfirmationNumber = PickupRequestConfirmationNumber
    def _hasContent(self):
        if (
            self.Response is not None or
            self.PickupRequestConfirmationNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FreightPickupResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FreightPickupResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'FreightPickupResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='FreightPickupResponse')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='FreightPickupResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='FreightPickupResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FreightPickupResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Response is not None:
            namespaceprefix_ = self.Response_nsprefix_ + ':' if (UseCapturedNS_ and self.Response_nsprefix_) else ''
            self.Response.export(outfile, level, namespaceprefix_='common:', namespacedef_='', name_='Response', pretty_print=pretty_print)
        if self.PickupRequestConfirmationNumber is not None:
            namespaceprefix_ = self.PickupRequestConfirmationNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupRequestConfirmationNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupRequestConfirmationNumber>%s</%sPickupRequestConfirmationNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupRequestConfirmationNumber), input_name='PickupRequestConfirmationNumber')), namespaceprefix_ , eol_))
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
        elif nodeName_ == 'PickupRequestConfirmationNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupRequestConfirmationNumber')
            value_ = self.gds_validate_string(value_, node, 'PickupRequestConfirmationNumber')
            self.PickupRequestConfirmationNumber = value_
            self.PickupRequestConfirmationNumber_nsprefix_ = child_.prefix
# end class FreightPickupResponse


class FreightCancelPickupResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Response=None, FreightCancelStatus=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Response = Response
        self.Response_nsprefix_ = "common"
        self.FreightCancelStatus = FreightCancelStatus
        self.FreightCancelStatus_nsprefix_ = "fpu"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, FreightCancelPickupResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if FreightCancelPickupResponse.subclass:
            return FreightCancelPickupResponse.subclass(*args_, **kwargs_)
        else:
            return FreightCancelPickupResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Response(self):
        return self.Response
    def set_Response(self, Response):
        self.Response = Response
    def get_FreightCancelStatus(self):
        return self.FreightCancelStatus
    def set_FreightCancelStatus(self, FreightCancelStatus):
        self.FreightCancelStatus = FreightCancelStatus
    def _hasContent(self):
        if (
            self.Response is not None or
            self.FreightCancelStatus is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FreightCancelPickupResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FreightCancelPickupResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'FreightCancelPickupResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='FreightCancelPickupResponse')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='FreightCancelPickupResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='FreightCancelPickupResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FreightCancelPickupResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Response is not None:
            namespaceprefix_ = self.Response_nsprefix_ + ':' if (UseCapturedNS_ and self.Response_nsprefix_) else ''
            self.Response.export(outfile, level, namespaceprefix_='common:', namespacedef_='', name_='Response', pretty_print=pretty_print)
        if self.FreightCancelStatus is not None:
            namespaceprefix_ = self.FreightCancelStatus_nsprefix_ + ':' if (UseCapturedNS_ and self.FreightCancelStatus_nsprefix_) else ''
            self.FreightCancelStatus.export(outfile, level, namespaceprefix_, namespacedef_='', name_='FreightCancelStatus', pretty_print=pretty_print)
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
        elif nodeName_ == 'FreightCancelStatus':
            obj_ = CancelStatusCodeDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.FreightCancelStatus = obj_
            obj_.original_tagname_ = 'FreightCancelStatus'
# end class FreightCancelPickupResponse


class RequesterType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ThirdPartyIndicator=None, AttentionName=None, EMailAddress=None, Name=None, Phone=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ThirdPartyIndicator = ThirdPartyIndicator
        self.ThirdPartyIndicator_nsprefix_ = None
        self.AttentionName = AttentionName
        self.AttentionName_nsprefix_ = None
        self.EMailAddress = EMailAddress
        self.EMailAddress_nsprefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = None
        self.Phone = Phone
        self.Phone_nsprefix_ = "fpu"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RequesterType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RequesterType.subclass:
            return RequesterType.subclass(*args_, **kwargs_)
        else:
            return RequesterType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ThirdPartyIndicator(self):
        return self.ThirdPartyIndicator
    def set_ThirdPartyIndicator(self, ThirdPartyIndicator):
        self.ThirdPartyIndicator = ThirdPartyIndicator
    def get_AttentionName(self):
        return self.AttentionName
    def set_AttentionName(self, AttentionName):
        self.AttentionName = AttentionName
    def get_EMailAddress(self):
        return self.EMailAddress
    def set_EMailAddress(self, EMailAddress):
        self.EMailAddress = EMailAddress
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def get_Phone(self):
        return self.Phone
    def set_Phone(self, Phone):
        self.Phone = Phone
    def _hasContent(self):
        if (
            self.ThirdPartyIndicator is not None or
            self.AttentionName is not None or
            self.EMailAddress is not None or
            self.Name is not None or
            self.Phone is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RequesterType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RequesterType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RequesterType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RequesterType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RequesterType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RequesterType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RequesterType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ThirdPartyIndicator is not None:
            namespaceprefix_ = self.ThirdPartyIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.ThirdPartyIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sThirdPartyIndicator>%s</%sThirdPartyIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ThirdPartyIndicator), input_name='ThirdPartyIndicator')), namespaceprefix_ , eol_))
        if self.AttentionName is not None:
            namespaceprefix_ = self.AttentionName_nsprefix_ + ':' if (UseCapturedNS_ and self.AttentionName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAttentionName>%s</%sAttentionName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AttentionName), input_name='AttentionName')), namespaceprefix_ , eol_))
        if self.EMailAddress is not None:
            namespaceprefix_ = self.EMailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.EMailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEMailAddress>%s</%sEMailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EMailAddress), input_name='EMailAddress')), namespaceprefix_ , eol_))
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName>%s</%sName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name), input_name='Name')), namespaceprefix_ , eol_))
        if self.Phone is not None:
            namespaceprefix_ = self.Phone_nsprefix_ + ':' if (UseCapturedNS_ and self.Phone_nsprefix_) else ''
            self.Phone.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Phone', pretty_print=pretty_print)
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
        if nodeName_ == 'ThirdPartyIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ThirdPartyIndicator')
            value_ = self.gds_validate_string(value_, node, 'ThirdPartyIndicator')
            self.ThirdPartyIndicator = value_
            self.ThirdPartyIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'AttentionName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AttentionName')
            value_ = self.gds_validate_string(value_, node, 'AttentionName')
            self.AttentionName = value_
            self.AttentionName_nsprefix_ = child_.prefix
        elif nodeName_ == 'EMailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EMailAddress')
            value_ = self.gds_validate_string(value_, node, 'EMailAddress')
            self.EMailAddress = value_
            self.EMailAddress_nsprefix_ = child_.prefix
        elif nodeName_ == 'Name':
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
# end class RequesterType


class AddressType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AddressLine=None, City=None, StateProvinceCode=None, PostalCode=None, CountryCode=None, gds_collector_=None, **kwargs_):
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
        self.PostalCode = PostalCode
        self.PostalCode_nsprefix_ = None
        self.CountryCode = CountryCode
        self.CountryCode_nsprefix_ = None
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
    def get_PostalCode(self):
        return self.PostalCode
    def set_PostalCode(self, PostalCode):
        self.PostalCode = PostalCode
    def get_CountryCode(self):
        return self.CountryCode
    def set_CountryCode(self, CountryCode):
        self.CountryCode = CountryCode
    def _hasContent(self):
        if (
            self.AddressLine or
            self.City is not None or
            self.StateProvinceCode is not None or
            self.PostalCode is not None or
            self.CountryCode is not None
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
        if self.PostalCode is not None:
            namespaceprefix_ = self.PostalCode_nsprefix_ + ':' if (UseCapturedNS_ and self.PostalCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPostalCode>%s</%sPostalCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PostalCode), input_name='PostalCode')), namespaceprefix_ , eol_))
        if self.CountryCode is not None:
            namespaceprefix_ = self.CountryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryCode>%s</%sCountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryCode), input_name='CountryCode')), namespaceprefix_ , eol_))
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


class ShipFromType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AttentionName=None, Name=None, Address=None, Phone=None, EMailAddress=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.AttentionName = AttentionName
        self.AttentionName_nsprefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = None
        self.Address = Address
        self.Address_nsprefix_ = "fpu"
        self.Phone = Phone
        self.Phone_nsprefix_ = "fpu"
        self.EMailAddress = EMailAddress
        self.EMailAddress_nsprefix_ = None
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
    def get_AttentionName(self):
        return self.AttentionName
    def set_AttentionName(self, AttentionName):
        self.AttentionName = AttentionName
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_Phone(self):
        return self.Phone
    def set_Phone(self, Phone):
        self.Phone = Phone
    def get_EMailAddress(self):
        return self.EMailAddress
    def set_EMailAddress(self, EMailAddress):
        self.EMailAddress = EMailAddress
    def _hasContent(self):
        if (
            self.AttentionName is not None or
            self.Name is not None or
            self.Address is not None or
            self.Phone is not None or
            self.EMailAddress is not None
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
        if self.AttentionName is not None:
            namespaceprefix_ = self.AttentionName_nsprefix_ + ':' if (UseCapturedNS_ and self.AttentionName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAttentionName>%s</%sAttentionName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AttentionName), input_name='AttentionName')), namespaceprefix_ , eol_))
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName>%s</%sName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name), input_name='Name')), namespaceprefix_ , eol_))
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.Phone is not None:
            namespaceprefix_ = self.Phone_nsprefix_ + ':' if (UseCapturedNS_ and self.Phone_nsprefix_) else ''
            self.Phone.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Phone', pretty_print=pretty_print)
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
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'AttentionName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AttentionName')
            value_ = self.gds_validate_string(value_, node, 'AttentionName')
            self.AttentionName = value_
            self.AttentionName_nsprefix_ = child_.prefix
        elif nodeName_ == 'Name':
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
        elif nodeName_ == 'Phone':
            obj_ = PhoneType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Phone = obj_
            obj_.original_tagname_ = 'Phone'
        elif nodeName_ == 'EMailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EMailAddress')
            value_ = self.gds_validate_string(value_, node, 'EMailAddress')
            self.EMailAddress = value_
            self.EMailAddress_nsprefix_ = child_.prefix
# end class ShipFromType


class ShipToType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AttentionName=None, Address=None, Phone=None, EMailAddress=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.AttentionName = AttentionName
        self.AttentionName_nsprefix_ = None
        self.Address = Address
        self.Address_nsprefix_ = "fpu"
        self.Phone = Phone
        self.Phone_nsprefix_ = "fpu"
        self.EMailAddress = EMailAddress
        self.EMailAddress_nsprefix_ = None
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
    def get_AttentionName(self):
        return self.AttentionName
    def set_AttentionName(self, AttentionName):
        self.AttentionName = AttentionName
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_Phone(self):
        return self.Phone
    def set_Phone(self, Phone):
        self.Phone = Phone
    def get_EMailAddress(self):
        return self.EMailAddress
    def set_EMailAddress(self, EMailAddress):
        self.EMailAddress = EMailAddress
    def _hasContent(self):
        if (
            self.AttentionName is not None or
            self.Address is not None or
            self.Phone is not None or
            self.EMailAddress is not None
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
        if self.AttentionName is not None:
            namespaceprefix_ = self.AttentionName_nsprefix_ + ':' if (UseCapturedNS_ and self.AttentionName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAttentionName>%s</%sAttentionName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AttentionName), input_name='AttentionName')), namespaceprefix_ , eol_))
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.Phone is not None:
            namespaceprefix_ = self.Phone_nsprefix_ + ':' if (UseCapturedNS_ and self.Phone_nsprefix_) else ''
            self.Phone.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Phone', pretty_print=pretty_print)
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
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'AttentionName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AttentionName')
            value_ = self.gds_validate_string(value_, node, 'AttentionName')
            self.AttentionName = value_
            self.AttentionName_nsprefix_ = child_.prefix
        elif nodeName_ == 'Address':
            obj_ = AddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'Phone':
            obj_ = PhoneType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Phone = obj_
            obj_.original_tagname_ = 'Phone'
        elif nodeName_ == 'EMailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EMailAddress')
            value_ = self.gds_validate_string(value_, node, 'EMailAddress')
            self.EMailAddress = value_
            self.EMailAddress_nsprefix_ = child_.prefix
# end class ShipToType


class ShipmentServiceOptionsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, FreezableProtectionIndicator=None, LimitedAccessPickupIndicator=None, LimitedAccessDeliveryIndicator=None, ExtremeLengthIndicator=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.FreezableProtectionIndicator = FreezableProtectionIndicator
        self.FreezableProtectionIndicator_nsprefix_ = None
        self.LimitedAccessPickupIndicator = LimitedAccessPickupIndicator
        self.LimitedAccessPickupIndicator_nsprefix_ = None
        self.LimitedAccessDeliveryIndicator = LimitedAccessDeliveryIndicator
        self.LimitedAccessDeliveryIndicator_nsprefix_ = None
        self.ExtremeLengthIndicator = ExtremeLengthIndicator
        self.ExtremeLengthIndicator_nsprefix_ = None
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
    def get_FreezableProtectionIndicator(self):
        return self.FreezableProtectionIndicator
    def set_FreezableProtectionIndicator(self, FreezableProtectionIndicator):
        self.FreezableProtectionIndicator = FreezableProtectionIndicator
    def get_LimitedAccessPickupIndicator(self):
        return self.LimitedAccessPickupIndicator
    def set_LimitedAccessPickupIndicator(self, LimitedAccessPickupIndicator):
        self.LimitedAccessPickupIndicator = LimitedAccessPickupIndicator
    def get_LimitedAccessDeliveryIndicator(self):
        return self.LimitedAccessDeliveryIndicator
    def set_LimitedAccessDeliveryIndicator(self, LimitedAccessDeliveryIndicator):
        self.LimitedAccessDeliveryIndicator = LimitedAccessDeliveryIndicator
    def get_ExtremeLengthIndicator(self):
        return self.ExtremeLengthIndicator
    def set_ExtremeLengthIndicator(self, ExtremeLengthIndicator):
        self.ExtremeLengthIndicator = ExtremeLengthIndicator
    def _hasContent(self):
        if (
            self.FreezableProtectionIndicator is not None or
            self.LimitedAccessPickupIndicator is not None or
            self.LimitedAccessDeliveryIndicator is not None or
            self.ExtremeLengthIndicator is not None
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
        if self.FreezableProtectionIndicator is not None:
            namespaceprefix_ = self.FreezableProtectionIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.FreezableProtectionIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFreezableProtectionIndicator>%s</%sFreezableProtectionIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FreezableProtectionIndicator), input_name='FreezableProtectionIndicator')), namespaceprefix_ , eol_))
        if self.LimitedAccessPickupIndicator is not None:
            namespaceprefix_ = self.LimitedAccessPickupIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.LimitedAccessPickupIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLimitedAccessPickupIndicator>%s</%sLimitedAccessPickupIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LimitedAccessPickupIndicator), input_name='LimitedAccessPickupIndicator')), namespaceprefix_ , eol_))
        if self.LimitedAccessDeliveryIndicator is not None:
            namespaceprefix_ = self.LimitedAccessDeliveryIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.LimitedAccessDeliveryIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLimitedAccessDeliveryIndicator>%s</%sLimitedAccessDeliveryIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LimitedAccessDeliveryIndicator), input_name='LimitedAccessDeliveryIndicator')), namespaceprefix_ , eol_))
        if self.ExtremeLengthIndicator is not None:
            namespaceprefix_ = self.ExtremeLengthIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.ExtremeLengthIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExtremeLengthIndicator>%s</%sExtremeLengthIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ExtremeLengthIndicator), input_name='ExtremeLengthIndicator')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'FreezableProtectionIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FreezableProtectionIndicator')
            value_ = self.gds_validate_string(value_, node, 'FreezableProtectionIndicator')
            self.FreezableProtectionIndicator = value_
            self.FreezableProtectionIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'LimitedAccessPickupIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LimitedAccessPickupIndicator')
            value_ = self.gds_validate_string(value_, node, 'LimitedAccessPickupIndicator')
            self.LimitedAccessPickupIndicator = value_
            self.LimitedAccessPickupIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'LimitedAccessDeliveryIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LimitedAccessDeliveryIndicator')
            value_ = self.gds_validate_string(value_, node, 'LimitedAccessDeliveryIndicator')
            self.LimitedAccessDeliveryIndicator = value_
            self.LimitedAccessDeliveryIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'ExtremeLengthIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ExtremeLengthIndicator')
            value_ = self.gds_validate_string(value_, node, 'ExtremeLengthIndicator')
            self.ExtremeLengthIndicator = value_
            self.ExtremeLengthIndicator_nsprefix_ = child_.prefix
# end class ShipmentServiceOptionsType


class ShipmentDetailType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, HazmatIndicator=None, PackagingType=None, NumberOfPieces=None, DescriptionOfCommodity=None, Weight=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.HazmatIndicator = HazmatIndicator
        self.HazmatIndicator_nsprefix_ = None
        self.PackagingType = PackagingType
        self.PackagingType_nsprefix_ = "fpu"
        self.NumberOfPieces = NumberOfPieces
        self.NumberOfPieces_nsprefix_ = None
        self.DescriptionOfCommodity = DescriptionOfCommodity
        self.DescriptionOfCommodity_nsprefix_ = None
        self.Weight = Weight
        self.Weight_nsprefix_ = "fpu"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentDetailType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentDetailType.subclass:
            return ShipmentDetailType.subclass(*args_, **kwargs_)
        else:
            return ShipmentDetailType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_HazmatIndicator(self):
        return self.HazmatIndicator
    def set_HazmatIndicator(self, HazmatIndicator):
        self.HazmatIndicator = HazmatIndicator
    def get_PackagingType(self):
        return self.PackagingType
    def set_PackagingType(self, PackagingType):
        self.PackagingType = PackagingType
    def get_NumberOfPieces(self):
        return self.NumberOfPieces
    def set_NumberOfPieces(self, NumberOfPieces):
        self.NumberOfPieces = NumberOfPieces
    def get_DescriptionOfCommodity(self):
        return self.DescriptionOfCommodity
    def set_DescriptionOfCommodity(self, DescriptionOfCommodity):
        self.DescriptionOfCommodity = DescriptionOfCommodity
    def get_Weight(self):
        return self.Weight
    def set_Weight(self, Weight):
        self.Weight = Weight
    def _hasContent(self):
        if (
            self.HazmatIndicator is not None or
            self.PackagingType is not None or
            self.NumberOfPieces is not None or
            self.DescriptionOfCommodity is not None or
            self.Weight is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentDetailType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentDetailType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentDetailType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentDetailType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentDetailType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentDetailType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentDetailType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.HazmatIndicator is not None:
            namespaceprefix_ = self.HazmatIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.HazmatIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHazmatIndicator>%s</%sHazmatIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HazmatIndicator), input_name='HazmatIndicator')), namespaceprefix_ , eol_))
        if self.PackagingType is not None:
            namespaceprefix_ = self.PackagingType_nsprefix_ + ':' if (UseCapturedNS_ and self.PackagingType_nsprefix_) else ''
            self.PackagingType.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PackagingType', pretty_print=pretty_print)
        if self.NumberOfPieces is not None:
            namespaceprefix_ = self.NumberOfPieces_nsprefix_ + ':' if (UseCapturedNS_ and self.NumberOfPieces_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNumberOfPieces>%s</%sNumberOfPieces>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NumberOfPieces), input_name='NumberOfPieces')), namespaceprefix_ , eol_))
        if self.DescriptionOfCommodity is not None:
            namespaceprefix_ = self.DescriptionOfCommodity_nsprefix_ + ':' if (UseCapturedNS_ and self.DescriptionOfCommodity_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDescriptionOfCommodity>%s</%sDescriptionOfCommodity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DescriptionOfCommodity), input_name='DescriptionOfCommodity')), namespaceprefix_ , eol_))
        if self.Weight is not None:
            namespaceprefix_ = self.Weight_nsprefix_ + ':' if (UseCapturedNS_ and self.Weight_nsprefix_) else ''
            self.Weight.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Weight', pretty_print=pretty_print)
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
        if nodeName_ == 'HazmatIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HazmatIndicator')
            value_ = self.gds_validate_string(value_, node, 'HazmatIndicator')
            self.HazmatIndicator = value_
            self.HazmatIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'PackagingType':
            obj_ = PickupCodeDescriptionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PackagingType = obj_
            obj_.original_tagname_ = 'PackagingType'
        elif nodeName_ == 'NumberOfPieces':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NumberOfPieces')
            value_ = self.gds_validate_string(value_, node, 'NumberOfPieces')
            self.NumberOfPieces = value_
            self.NumberOfPieces_nsprefix_ = child_.prefix
        elif nodeName_ == 'DescriptionOfCommodity':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DescriptionOfCommodity')
            value_ = self.gds_validate_string(value_, node, 'DescriptionOfCommodity')
            self.DescriptionOfCommodity = value_
            self.DescriptionOfCommodity_nsprefix_ = child_.prefix
        elif nodeName_ == 'Weight':
            obj_ = WeightType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Weight = obj_
            obj_.original_tagname_ = 'Weight'
# end class ShipmentDetailType


class PickupCodeDescriptionType(GeneratedsSuper):
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
                CurrentSubclassModule_, PickupCodeDescriptionType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PickupCodeDescriptionType.subclass:
            return PickupCodeDescriptionType.subclass(*args_, **kwargs_)
        else:
            return PickupCodeDescriptionType(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupCodeDescriptionType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PickupCodeDescriptionType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PickupCodeDescriptionType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PickupCodeDescriptionType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PickupCodeDescriptionType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PickupCodeDescriptionType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupCodeDescriptionType', fromsubclass_=False, pretty_print=True):
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
# end class PickupCodeDescriptionType


class POMType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, POMNumber=None, POMNumberType=None, PickupNotifications=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.POMNumber = POMNumber
        self.POMNumber_nsprefix_ = None
        self.POMNumberType = POMNumberType
        self.POMNumberType_nsprefix_ = None
        self.PickupNotifications = PickupNotifications
        self.PickupNotifications_nsprefix_ = "fpu"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, POMType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if POMType.subclass:
            return POMType.subclass(*args_, **kwargs_)
        else:
            return POMType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_POMNumber(self):
        return self.POMNumber
    def set_POMNumber(self, POMNumber):
        self.POMNumber = POMNumber
    def get_POMNumberType(self):
        return self.POMNumberType
    def set_POMNumberType(self, POMNumberType):
        self.POMNumberType = POMNumberType
    def get_PickupNotifications(self):
        return self.PickupNotifications
    def set_PickupNotifications(self, PickupNotifications):
        self.PickupNotifications = PickupNotifications
    def _hasContent(self):
        if (
            self.POMNumber is not None or
            self.POMNumberType is not None or
            self.PickupNotifications is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='POMType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('POMType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'POMType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='POMType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='POMType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='POMType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='POMType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.POMNumber is not None:
            namespaceprefix_ = self.POMNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.POMNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPOMNumber>%s</%sPOMNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.POMNumber), input_name='POMNumber')), namespaceprefix_ , eol_))
        if self.POMNumberType is not None:
            namespaceprefix_ = self.POMNumberType_nsprefix_ + ':' if (UseCapturedNS_ and self.POMNumberType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPOMNumberType>%s</%sPOMNumberType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.POMNumberType), input_name='POMNumberType')), namespaceprefix_ , eol_))
        if self.PickupNotifications is not None:
            namespaceprefix_ = self.PickupNotifications_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupNotifications_nsprefix_) else ''
            self.PickupNotifications.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PickupNotifications', pretty_print=pretty_print)
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
        if nodeName_ == 'POMNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'POMNumber')
            value_ = self.gds_validate_string(value_, node, 'POMNumber')
            self.POMNumber = value_
            self.POMNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'POMNumberType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'POMNumberType')
            value_ = self.gds_validate_string(value_, node, 'POMNumberType')
            self.POMNumberType = value_
            self.POMNumberType_nsprefix_ = child_.prefix
        elif nodeName_ == 'PickupNotifications':
            obj_ = PickupNotificationsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PickupNotifications = obj_
            obj_.original_tagname_ = 'PickupNotifications'
# end class POMType


class PickupNotificationsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CompanyName=None, EMailNotification=None, FailedEMail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CompanyName = CompanyName
        self.CompanyName_nsprefix_ = None
        if EMailNotification is None:
            self.EMailNotification = []
        else:
            self.EMailNotification = EMailNotification
        self.EMailNotification_nsprefix_ = "fpu"
        self.FailedEMail = FailedEMail
        self.FailedEMail_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PickupNotificationsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PickupNotificationsType.subclass:
            return PickupNotificationsType.subclass(*args_, **kwargs_)
        else:
            return PickupNotificationsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CompanyName(self):
        return self.CompanyName
    def set_CompanyName(self, CompanyName):
        self.CompanyName = CompanyName
    def get_EMailNotification(self):
        return self.EMailNotification
    def set_EMailNotification(self, EMailNotification):
        self.EMailNotification = EMailNotification
    def add_EMailNotification(self, value):
        self.EMailNotification.append(value)
    def insert_EMailNotification_at(self, index, value):
        self.EMailNotification.insert(index, value)
    def replace_EMailNotification_at(self, index, value):
        self.EMailNotification[index] = value
    def get_FailedEMail(self):
        return self.FailedEMail
    def set_FailedEMail(self, FailedEMail):
        self.FailedEMail = FailedEMail
    def _hasContent(self):
        if (
            self.CompanyName is not None or
            self.EMailNotification or
            self.FailedEMail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupNotificationsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PickupNotificationsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PickupNotificationsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PickupNotificationsType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PickupNotificationsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PickupNotificationsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupNotificationsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CompanyName is not None:
            namespaceprefix_ = self.CompanyName_nsprefix_ + ':' if (UseCapturedNS_ and self.CompanyName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCompanyName>%s</%sCompanyName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CompanyName), input_name='CompanyName')), namespaceprefix_ , eol_))
        for EMailNotification_ in self.EMailNotification:
            namespaceprefix_ = self.EMailNotification_nsprefix_ + ':' if (UseCapturedNS_ and self.EMailNotification_nsprefix_) else ''
            EMailNotification_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='EMailNotification', pretty_print=pretty_print)
        if self.FailedEMail is not None:
            namespaceprefix_ = self.FailedEMail_nsprefix_ + ':' if (UseCapturedNS_ and self.FailedEMail_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFailedEMail>%s</%sFailedEMail>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FailedEMail), input_name='FailedEMail')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'CompanyName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CompanyName')
            value_ = self.gds_validate_string(value_, node, 'CompanyName')
            self.CompanyName = value_
            self.CompanyName_nsprefix_ = child_.prefix
        elif nodeName_ == 'EMailNotification':
            obj_ = EMailNotificationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EMailNotification.append(obj_)
            obj_.original_tagname_ = 'EMailNotification'
        elif nodeName_ == 'FailedEMail':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FailedEMail')
            value_ = self.gds_validate_string(value_, node, 'FailedEMail')
            self.FailedEMail = value_
            self.FailedEMail_nsprefix_ = child_.prefix
# end class PickupNotificationsType


class WeightType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, UnitOfMeasurement=None, Value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.UnitOfMeasurement = UnitOfMeasurement
        self.UnitOfMeasurement_nsprefix_ = "fpu"
        self.Value = Value
        self.Value_nsprefix_ = None
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
    def get_UnitOfMeasurement(self):
        return self.UnitOfMeasurement
    def set_UnitOfMeasurement(self, UnitOfMeasurement):
        self.UnitOfMeasurement = UnitOfMeasurement
    def get_Value(self):
        return self.Value
    def set_Value(self, Value):
        self.Value = Value
    def _hasContent(self):
        if (
            self.UnitOfMeasurement is not None or
            self.Value is not None
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
        if self.UnitOfMeasurement is not None:
            namespaceprefix_ = self.UnitOfMeasurement_nsprefix_ + ':' if (UseCapturedNS_ and self.UnitOfMeasurement_nsprefix_) else ''
            self.UnitOfMeasurement.export(outfile, level, namespaceprefix_, namespacedef_='', name_='UnitOfMeasurement', pretty_print=pretty_print)
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
        if nodeName_ == 'UnitOfMeasurement':
            obj_ = UnitOfMeasurementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UnitOfMeasurement = obj_
            obj_.original_tagname_ = 'UnitOfMeasurement'
        elif nodeName_ == 'Value':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Value')
            value_ = self.gds_validate_string(value_, node, 'Value')
            self.Value = value_
            self.Value_nsprefix_ = child_.prefix
# end class WeightType


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


class ExistingShipmentIDType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ShipmentNumber=None, BOLID=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ShipmentNumber = ShipmentNumber
        self.ShipmentNumber_nsprefix_ = None
        self.BOLID = BOLID
        self.BOLID_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ExistingShipmentIDType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ExistingShipmentIDType.subclass:
            return ExistingShipmentIDType.subclass(*args_, **kwargs_)
        else:
            return ExistingShipmentIDType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ShipmentNumber(self):
        return self.ShipmentNumber
    def set_ShipmentNumber(self, ShipmentNumber):
        self.ShipmentNumber = ShipmentNumber
    def get_BOLID(self):
        return self.BOLID
    def set_BOLID(self, BOLID):
        self.BOLID = BOLID
    def _hasContent(self):
        if (
            self.ShipmentNumber is not None or
            self.BOLID is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ExistingShipmentIDType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ExistingShipmentIDType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ExistingShipmentIDType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ExistingShipmentIDType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ExistingShipmentIDType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ExistingShipmentIDType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ExistingShipmentIDType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ShipmentNumber is not None:
            namespaceprefix_ = self.ShipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipmentNumber>%s</%sShipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShipmentNumber), input_name='ShipmentNumber')), namespaceprefix_ , eol_))
        if self.BOLID is not None:
            namespaceprefix_ = self.BOLID_nsprefix_ + ':' if (UseCapturedNS_ and self.BOLID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBOLID>%s</%sBOLID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BOLID), input_name='BOLID')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ShipmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShipmentNumber')
            value_ = self.gds_validate_string(value_, node, 'ShipmentNumber')
            self.ShipmentNumber = value_
            self.ShipmentNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'BOLID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BOLID')
            value_ = self.gds_validate_string(value_, node, 'BOLID')
            self.BOLID = value_
            self.BOLID_nsprefix_ = child_.prefix
# end class ExistingShipmentIDType


class EMailNotificationType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, EMailAddress=None, EventType=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.EMailAddress = EMailAddress
        self.EMailAddress_nsprefix_ = None
        if EventType is None:
            self.EventType = []
        else:
            self.EventType = EventType
        self.EventType_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, EMailNotificationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EMailNotificationType.subclass:
            return EMailNotificationType.subclass(*args_, **kwargs_)
        else:
            return EMailNotificationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_EMailAddress(self):
        return self.EMailAddress
    def set_EMailAddress(self, EMailAddress):
        self.EMailAddress = EMailAddress
    def get_EventType(self):
        return self.EventType
    def set_EventType(self, EventType):
        self.EventType = EventType
    def add_EventType(self, value):
        self.EventType.append(value)
    def insert_EventType_at(self, index, value):
        self.EventType.insert(index, value)
    def replace_EventType_at(self, index, value):
        self.EventType[index] = value
    def _hasContent(self):
        if (
            self.EMailAddress is not None or
            self.EventType
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EMailNotificationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EMailNotificationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EMailNotificationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EMailNotificationType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='EMailNotificationType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EMailNotificationType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EMailNotificationType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.EMailAddress is not None:
            namespaceprefix_ = self.EMailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.EMailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEMailAddress>%s</%sEMailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EMailAddress), input_name='EMailAddress')), namespaceprefix_ , eol_))
        for EventType_ in self.EventType:
            namespaceprefix_ = self.EventType_nsprefix_ + ':' if (UseCapturedNS_ and self.EventType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEventType>%s</%sEventType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(EventType_), input_name='EventType')), namespaceprefix_ , eol_))
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
            self.EMailAddress = value_
            self.EMailAddress_nsprefix_ = child_.prefix
        elif nodeName_ == 'EventType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EventType')
            value_ = self.gds_validate_string(value_, node, 'EventType')
            self.EventType.append(value_)
            self.EventType_nsprefix_ = child_.prefix
# end class EMailNotificationType


class CancelStatusCodeDescriptionType(GeneratedsSuper):
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
                CurrentSubclassModule_, CancelStatusCodeDescriptionType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CancelStatusCodeDescriptionType.subclass:
            return CancelStatusCodeDescriptionType.subclass(*args_, **kwargs_)
        else:
            return CancelStatusCodeDescriptionType(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CancelStatusCodeDescriptionType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CancelStatusCodeDescriptionType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CancelStatusCodeDescriptionType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CancelStatusCodeDescriptionType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CancelStatusCodeDescriptionType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CancelStatusCodeDescriptionType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CancelStatusCodeDescriptionType', fromsubclass_=False, pretty_print=True):
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
# end class CancelStatusCodeDescriptionType


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
        rootTag = 'FreightPickupRequest'
        rootClass = FreightPickupRequest
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
        rootTag = 'FreightPickupRequest'
        rootClass = FreightPickupRequest
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
        rootTag = 'FreightPickupRequest'
        rootClass = FreightPickupRequest
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:fpu="http://www.ups.com/XMLSchema/XOLTWS/FreightPickup/v1.0"')
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
        rootTag = 'FreightPickupRequest'
        rootClass = FreightPickupRequest
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from freight_pickup_web_service_schema import *\n\n')
        sys.stdout.write('import freight_pickup_web_service_schema as model_\n\n')
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
 'http://www.ups.com/XMLSchema/XOLTWS/FreightPickup/v1.0': [('RequesterType',
                                                             './schemas/FreightPickupWebServiceSchema.xsd',
                                                             'CT'),
                                                            ('AddressType',
                                                             './schemas/FreightPickupWebServiceSchema.xsd',
                                                             'CT'),
                                                            ('PhoneType',
                                                             './schemas/FreightPickupWebServiceSchema.xsd',
                                                             'CT'),
                                                            ('ShipFromType',
                                                             './schemas/FreightPickupWebServiceSchema.xsd',
                                                             'CT'),
                                                            ('ShipToType',
                                                             './schemas/FreightPickupWebServiceSchema.xsd',
                                                             'CT'),
                                                            ('ShipmentServiceOptionsType',
                                                             './schemas/FreightPickupWebServiceSchema.xsd',
                                                             'CT'),
                                                            ('ShipmentDetailType',
                                                             './schemas/FreightPickupWebServiceSchema.xsd',
                                                             'CT'),
                                                            ('PickupCodeDescriptionType',
                                                             './schemas/FreightPickupWebServiceSchema.xsd',
                                                             'CT'),
                                                            ('POMType',
                                                             './schemas/FreightPickupWebServiceSchema.xsd',
                                                             'CT'),
                                                            ('PickupNotificationsType',
                                                             './schemas/FreightPickupWebServiceSchema.xsd',
                                                             'CT'),
                                                            ('WeightType',
                                                             './schemas/FreightPickupWebServiceSchema.xsd',
                                                             'CT'),
                                                            ('UnitOfMeasurementType',
                                                             './schemas/FreightPickupWebServiceSchema.xsd',
                                                             'CT'),
                                                            ('ExistingShipmentIDType',
                                                             './schemas/FreightPickupWebServiceSchema.xsd',
                                                             'CT'),
                                                            ('EMailNotificationType',
                                                             './schemas/FreightPickupWebServiceSchema.xsd',
                                                             'CT'),
                                                            ('CancelStatusCodeDescriptionType',
                                                             './schemas/FreightPickupWebServiceSchema.xsd',
                                                             'CT')]}

__all__ = [
    "AddressType",
    "CancelStatusCodeDescriptionType",
    "ClientInformationType",
    "CodeDescriptionType",
    "DetailType",
    "EMailNotificationType",
    "ElementIdentifierType",
    "ElementLevelInformationType",
    "ExistingShipmentIDType",
    "FreightCancelPickupRequest",
    "FreightCancelPickupResponse",
    "FreightPickupRequest",
    "FreightPickupResponse",
    "POMType",
    "PhoneType",
    "PickupCodeDescriptionType",
    "PickupNotificationsType",
    "PropertyType",
    "RequestType",
    "RequesterType",
    "ResponseType",
    "ShipFromType",
    "ShipToType",
    "ShipmentDetailType",
    "ShipmentServiceOptionsType",
    "TransactionReferenceType",
    "UnitOfMeasurementType",
    "WeightType"
]
