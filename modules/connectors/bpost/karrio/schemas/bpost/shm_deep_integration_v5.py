#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Thu Nov  9 10:01:54 2023 by generateDS.py version 2.43.3.
# Python 3.10.9 (main, Dec 15 2022, 18:18:30) [Clang 14.0.0 (clang-1400.0.29.202)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './karrio/schemas/bpost/shm_deep_integration_v5.py')
#
# Command line arguments:
#   ./schemas/shm_deep_integration_v5.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/karrio/.venv/karrio/bin/generateDS --no-namespace-defs -o "./karrio/schemas/bpost/shm_deep_integration_v5.py" ./schemas/shm_deep_integration_v5.xsd
#
# Current working directory (os.getcwd()):
#   bpost
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
            value = ('%.15f' % float(input_data)).rstrip('0')
            if value.endswith('.'):
                value += '0'
            return value
    
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
# Start enum classes
#
class BoxStatusType(str, Enum):
    PENDING='PENDING'
    OPEN='OPEN'
    CANCELLED='CANCELLED'
    ONHOLD='ON-HOLD'
    PRINTED='PRINTED'
    ANNOUNCED='ANNOUNCED'
    IN_TRANSIT='IN_TRANSIT'
    AWAITING_PICKUP='AWAITING_PICKUP'
    DELIVERED='DELIVERED'
    BACK_TO_SENDER='BACK_TO_SENDER'


class ParcelReturnInstructionsType(str, Enum):
    ABANDONED='ABANDONED'
    RTA='RTA'
    RTS='RTS'


class SetBoxStatusType(str, Enum):
    OPEN='OPEN'
    CANCELLED='CANCELLED'
    ONHOLD='ON-HOLD'


class ShipmentType(str, Enum):
    SAMPLE='SAMPLE'
    GIFT='GIFT'
    GOODS='GOODS'
    OTHER='OTHER'
    DOCUMENTS='DOCUMENTS'


class languageType(str, Enum):
    EN='EN'
    NL='NL'
    FR='FR'
    DE='DE'


class languageType3(str, Enum):
    """languageType3 --  Element holding the language used for messaging
    (NL | FR | EN).
    
    """
    EN='EN'
    NL='NL'
    FR='FR'


class valueType(str, Enum):
    _1='1'
    _2='2'
    _3='3'


class valueType2(str, Enum):
    AM='AM'
    PM='PM'
    PMPLUS='PMPLUS'


#
# Start data representation classes
#
class OrderUpdateType(GeneratedsSuper):
    """status --  New status of an order.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, status=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.status = status
        self.validate_SetBoxStatusType(self.status)
        self.status_nsprefix_ = "common"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, OrderUpdateType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OrderUpdateType.subclass:
            return OrderUpdateType.subclass(*args_, **kwargs_)
        else:
            return OrderUpdateType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_status(self):
        return self.status
    def set_status(self, status):
        self.status = status
    def validate_SetBoxStatusType(self, value):
        result = True
        # Validate type SetBoxStatusType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['OPEN', 'CANCELLED', 'ON-HOLD']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on SetBoxStatusType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.status is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OrderUpdateType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OrderUpdateType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'OrderUpdateType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OrderUpdateType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='OrderUpdateType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='OrderUpdateType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OrderUpdateType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.status is not None:
            namespaceprefix_ = self.status_nsprefix_ + ':' if (UseCapturedNS_ and self.status_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstatus>%s</%sstatus>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.status), input_name='status')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'status':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'status')
            value_ = self.gds_validate_string(value_, node, 'status')
            self.status = value_
            self.status_nsprefix_ = child_.prefix
            # validate type SetBoxStatusType
            self.validate_SetBoxStatusType(self.status)
# end class OrderUpdateType


class BaseOrderType(GeneratedsSuper):
    """BaseOrderType --  Abstract type representing base structure of an order.
    accountId --  Element holding the account's id information.
    reference --  Element holding the reference of an order.
    costCenter --  Element holding the cost center information of
    an order.
    orderLine --  Element holding the order line information of
    an order.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, accountId=None, reference=None, costCenter=None, orderLine=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.accountId = accountId
        self.validate_AccountIdType(self.accountId)
        self.accountId_nsprefix_ = "common"
        self.reference = reference
        self.validate_OrderReferenceType(self.reference)
        self.reference_nsprefix_ = "tns"
        self.costCenter = costCenter
        self.validate_CostCenterType(self.costCenter)
        self.costCenter_nsprefix_ = "common"
        if orderLine is None:
            self.orderLine = []
        else:
            self.orderLine = orderLine
        self.orderLine_nsprefix_ = "tns"
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, BaseOrderType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BaseOrderType.subclass:
            return BaseOrderType.subclass(*args_, **kwargs_)
        else:
            return BaseOrderType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_accountId(self):
        return self.accountId
    def set_accountId(self, accountId):
        self.accountId = accountId
    def get_reference(self):
        return self.reference
    def set_reference(self, reference):
        self.reference = reference
    def get_costCenter(self):
        return self.costCenter
    def set_costCenter(self, costCenter):
        self.costCenter = costCenter
    def get_orderLine(self):
        return self.orderLine
    def set_orderLine(self, orderLine):
        self.orderLine = orderLine
    def add_orderLine(self, value):
        self.orderLine.append(value)
    def insert_orderLine_at(self, index, value):
        self.orderLine.insert(index, value)
    def replace_orderLine_at(self, index, value):
        self.orderLine[index] = value
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def validate_AccountIdType(self, value):
        result = True
        # Validate type AccountIdType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_AccountIdType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_AccountIdType_patterns_, ))
                result = False
        return result
    validate_AccountIdType_patterns_ = [['^([0-9]{6})$']]
    def validate_OrderReferenceType(self, value):
        result = True
        # Validate type OrderReferenceType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 100:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on OrderReferenceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on OrderReferenceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_OrderReferenceType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_OrderReferenceType_patterns_, ))
                result = False
        return result
    validate_OrderReferenceType_patterns_ = [['^(.*[^\\s].*)$']]
    def validate_CostCenterType(self, value):
        result = True
        # Validate type CostCenterType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CostCenterType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.accountId is not None or
            self.reference is not None or
            self.costCenter is not None or
            self.orderLine
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BaseOrderType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('BaseOrderType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'BaseOrderType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BaseOrderType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='BaseOrderType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='BaseOrderType'):
        if self.extensiontype_ is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self.extensiontype_:
                imported_ns_type_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.extensiontype_, '')
                outfile.write(' xsi:type="%s%s"' % (imported_ns_type_prefix_, self.extensiontype_))
            else:
                outfile.write(' xsi:type="%s"' % self.extensiontype_)
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BaseOrderType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.accountId is not None:
            namespaceprefix_ = self.accountId_nsprefix_ + ':' if (UseCapturedNS_ and self.accountId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saccountId>%s</%saccountId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.accountId), input_name='accountId')), namespaceprefix_ , eol_))
        if self.reference is not None:
            namespaceprefix_ = self.reference_nsprefix_ + ':' if (UseCapturedNS_ and self.reference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sreference>%s</%sreference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.reference), input_name='reference')), namespaceprefix_ , eol_))
        if self.costCenter is not None:
            namespaceprefix_ = self.costCenter_nsprefix_ + ':' if (UseCapturedNS_ and self.costCenter_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scostCenter>%s</%scostCenter>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.costCenter), input_name='costCenter')), namespaceprefix_ , eol_))
        for orderLine_ in self.orderLine:
            namespaceprefix_ = self.orderLine_nsprefix_ + ':' if (UseCapturedNS_ and self.orderLine_nsprefix_) else ''
            orderLine_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='orderLine', pretty_print=pretty_print)
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
        value = find_attr_value_('xsi:type', node)
        if value is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            self.extensiontype_ = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'accountId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'accountId')
            value_ = self.gds_validate_string(value_, node, 'accountId')
            self.accountId = value_
            self.accountId_nsprefix_ = child_.prefix
            # validate type AccountIdType
            self.validate_AccountIdType(self.accountId)
        elif nodeName_ == 'reference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'reference')
            value_ = self.gds_validate_string(value_, node, 'reference')
            self.reference = value_
            self.reference_nsprefix_ = child_.prefix
            # validate type OrderReferenceType
            self.validate_OrderReferenceType(self.reference)
        elif nodeName_ == 'costCenter':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'costCenter')
            value_ = self.gds_validate_string(value_, node, 'costCenter')
            self.costCenter = value_
            self.costCenter_nsprefix_ = child_.prefix
            # validate type CostCenterType
            self.validate_CostCenterType(self.costCenter)
        elif nodeName_ == 'orderLine':
            obj_ = OrderLineType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.orderLine.append(obj_)
            obj_.original_tagname_ = 'orderLine'
# end class BaseOrderType


class OrderType(BaseOrderType):
    """OrderType --  Type representing an order for creation. This type
    extends the base type and keeps additional information about boxes for the order.
    box --  Element holding the box information of
    an order when creating an order. Multiple boxes are allowed.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = BaseOrderType
    def __init__(self, accountId=None, reference=None, costCenter=None, orderLine=None, box=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("OrderType"), self).__init__(accountId, reference, costCenter, orderLine,  **kwargs_)
        if box is None:
            self.box = []
        else:
            self.box = box
        self.box_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, OrderType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OrderType.subclass:
            return OrderType.subclass(*args_, **kwargs_)
        else:
            return OrderType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_box(self):
        return self.box
    def set_box(self, box):
        self.box = box
    def add_box(self, value):
        self.box.append(value)
    def insert_box_at(self, index, value):
        self.box.insert(index, value)
    def replace_box_at(self, index, value):
        self.box[index] = value
    def has__content(self):
        if (
            self.box or
            super(OrderType, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OrderType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OrderType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'OrderType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OrderType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='OrderType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='OrderType'):
        super(OrderType, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OrderType')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OrderType', fromsubclass_=False, pretty_print=True):
        super(OrderType, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for box_ in self.box:
            namespaceprefix_ = self.box_nsprefix_ + ':' if (UseCapturedNS_ and self.box_nsprefix_) else ''
            box_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='box', pretty_print=pretty_print)
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
        super(OrderType, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'box':
            obj_ = CreateBoxType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.box.append(obj_)
            obj_.original_tagname_ = 'box'
        super(OrderType, self)._buildChildren(child_, node, nodeName_, True)
# end class OrderType


class OrderInfoType(BaseOrderType):
    """OrderInfoType --  Type representing an order when fetched. This type
    extends the base type and keeps additional information about boxes for the order.
    box --  Element holding the box information of
    an order when fetching an order. Multiple boxes are allowed.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = BaseOrderType
    def __init__(self, accountId=None, reference=None, costCenter=None, orderLine=None, box=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("OrderInfoType"), self).__init__(accountId, reference, costCenter, orderLine,  **kwargs_)
        if box is None:
            self.box = []
        else:
            self.box = box
        self.box_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, OrderInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OrderInfoType.subclass:
            return OrderInfoType.subclass(*args_, **kwargs_)
        else:
            return OrderInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_box(self):
        return self.box
    def set_box(self, box):
        self.box = box
    def add_box(self, value):
        self.box.append(value)
    def insert_box_at(self, index, value):
        self.box.insert(index, value)
    def replace_box_at(self, index, value):
        self.box[index] = value
    def has__content(self):
        if (
            self.box or
            super(OrderInfoType, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OrderInfoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OrderInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'OrderInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OrderInfoType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='OrderInfoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='OrderInfoType'):
        super(OrderInfoType, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OrderInfoType')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OrderInfoType', fromsubclass_=False, pretty_print=True):
        super(OrderInfoType, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for box_ in self.box:
            namespaceprefix_ = self.box_nsprefix_ + ':' if (UseCapturedNS_ and self.box_nsprefix_) else ''
            box_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='box', pretty_print=pretty_print)
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
        super(OrderInfoType, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'box':
            obj_ = BoxInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.box.append(obj_)
            obj_.original_tagname_ = 'box'
        super(OrderInfoType, self)._buildChildren(child_, node, nodeName_, True)
# end class OrderInfoType


class OrderLineType(GeneratedsSuper):
    """OrderLineType --  Type representing an order line.
    text --  Element holding the free text information about
    an order line.
    nbOfItems --  Element holding the amount of order lines.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, text=None, nbOfItems=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.text = text
        self.validate_OrderLineTextType(self.text)
        self.text_nsprefix_ = "tns"
        self.nbOfItems = nbOfItems
        self.nbOfItems_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, OrderLineType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OrderLineType.subclass:
            return OrderLineType.subclass(*args_, **kwargs_)
        else:
            return OrderLineType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_text(self):
        return self.text
    def set_text(self, text):
        self.text = text
    def get_nbOfItems(self):
        return self.nbOfItems
    def set_nbOfItems(self, nbOfItems):
        self.nbOfItems = nbOfItems
    def validate_OrderLineTextType(self, value):
        result = True
        # Validate type OrderLineTextType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 255:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on OrderLineTextType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on OrderLineTextType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_OrderLineTextType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_OrderLineTextType_patterns_, ))
                result = False
        return result
    validate_OrderLineTextType_patterns_ = [['^(.*[^\\s].*)$']]
    def has__content(self):
        if (
            self.text is not None or
            self.nbOfItems is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OrderLineType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OrderLineType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'OrderLineType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OrderLineType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='OrderLineType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='OrderLineType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OrderLineType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.text is not None:
            namespaceprefix_ = self.text_nsprefix_ + ':' if (UseCapturedNS_ and self.text_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stext>%s</%stext>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.text), input_name='text')), namespaceprefix_ , eol_))
        if self.nbOfItems is not None:
            namespaceprefix_ = self.nbOfItems_nsprefix_ + ':' if (UseCapturedNS_ and self.nbOfItems_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snbOfItems>%s</%snbOfItems>%s' % (namespaceprefix_ , self.gds_format_integer(self.nbOfItems, input_name='nbOfItems'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'text':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'text')
            value_ = self.gds_validate_string(value_, node, 'text')
            self.text = value_
            self.text_nsprefix_ = child_.prefix
            # validate type OrderLineTextType
            self.validate_OrderLineTextType(self.text)
        elif nodeName_ == 'nbOfItems' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'nbOfItems')
            ival_ = self.gds_validate_integer(ival_, node, 'nbOfItems')
            self.nbOfItems = ival_
            self.nbOfItems_nsprefix_ = child_.prefix
# end class OrderLineType


class BoxType(GeneratedsSuper):
    """BoxType --  Abstract type representing base structure of a box.
    sender --  Element holding information about the sender of
    a box.
    nationalBox --  Element for the national box information.
    internationalBox --  Element for the international box
    information.
    remark --  Element for the remark on a specific box (ref 4
    in lci).
    additionalCustomerReference --  Element holding additional customer reference
    information (ref 5 in lci).
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, sender=None, nationalBox=None, internationalBox=None, remark=None, additionalCustomerReference=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.sender = sender
        self.sender_nsprefix_ = "common"
        self.nationalBox = nationalBox
        self.nationalBox_nsprefix_ = "national"
        self.internationalBox = internationalBox
        self.internationalBox_nsprefix_ = "international"
        self.remark = remark
        self.validate_RemarkType(self.remark)
        self.remark_nsprefix_ = "tns"
        self.additionalCustomerReference = additionalCustomerReference
        self.validate_RemarkType(self.additionalCustomerReference)
        self.additionalCustomerReference_nsprefix_ = "tns"
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, BoxType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BoxType.subclass:
            return BoxType.subclass(*args_, **kwargs_)
        else:
            return BoxType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_sender(self):
        return self.sender
    def set_sender(self, sender):
        self.sender = sender
    def get_nationalBox(self):
        return self.nationalBox
    def set_nationalBox(self, nationalBox):
        self.nationalBox = nationalBox
    def get_internationalBox(self):
        return self.internationalBox
    def set_internationalBox(self, internationalBox):
        self.internationalBox = internationalBox
    def get_remark(self):
        return self.remark
    def set_remark(self, remark):
        self.remark = remark
    def get_additionalCustomerReference(self):
        return self.additionalCustomerReference
    def set_additionalCustomerReference(self, additionalCustomerReference):
        self.additionalCustomerReference = additionalCustomerReference
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def validate_RemarkType(self, value):
        result = True
        # Validate type RemarkType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on RemarkType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.sender is not None or
            self.nationalBox is not None or
            self.internationalBox is not None or
            self.remark is not None or
            self.additionalCustomerReference is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BoxType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('BoxType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'BoxType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BoxType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='BoxType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='BoxType'):
        if self.extensiontype_ is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self.extensiontype_:
                imported_ns_type_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.extensiontype_, '')
                outfile.write(' xsi:type="%s%s"' % (imported_ns_type_prefix_, self.extensiontype_))
            else:
                outfile.write(' xsi:type="%s"' % self.extensiontype_)
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BoxType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.sender is not None:
            namespaceprefix_ = self.sender_nsprefix_ + ':' if (UseCapturedNS_ and self.sender_nsprefix_) else ''
            self.sender.export(outfile, level, namespaceprefix_, namespacedef_='', name_='sender', pretty_print=pretty_print)
        if self.nationalBox is not None:
            namespaceprefix_ = self.nationalBox_nsprefix_ + ':' if (UseCapturedNS_ and self.nationalBox_nsprefix_) else ''
            self.nationalBox.export(outfile, level, namespaceprefix_, namespacedef_='', name_='nationalBox', pretty_print=pretty_print)
        if self.internationalBox is not None:
            namespaceprefix_ = self.internationalBox_nsprefix_ + ':' if (UseCapturedNS_ and self.internationalBox_nsprefix_) else ''
            self.internationalBox.export(outfile, level, namespaceprefix_, namespacedef_='', name_='internationalBox', pretty_print=pretty_print)
        if self.remark is not None:
            namespaceprefix_ = self.remark_nsprefix_ + ':' if (UseCapturedNS_ and self.remark_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sremark>%s</%sremark>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.remark), input_name='remark')), namespaceprefix_ , eol_))
        if self.additionalCustomerReference is not None:
            namespaceprefix_ = self.additionalCustomerReference_nsprefix_ + ':' if (UseCapturedNS_ and self.additionalCustomerReference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sadditionalCustomerReference>%s</%sadditionalCustomerReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.additionalCustomerReference), input_name='additionalCustomerReference')), namespaceprefix_ , eol_))
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
        value = find_attr_value_('xsi:type', node)
        if value is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            self.extensiontype_ = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'sender':
            obj_ = Party.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.sender = obj_
            obj_.original_tagname_ = 'sender'
        elif nodeName_ == 'nationalBox':
            obj_ = NationalBoxType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.nationalBox = obj_
            obj_.original_tagname_ = 'nationalBox'
        elif nodeName_ == 'internationalBox':
            obj_ = InternationalBoxType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.internationalBox = obj_
            obj_.original_tagname_ = 'internationalBox'
        elif nodeName_ == 'remark':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'remark')
            value_ = self.gds_validate_string(value_, node, 'remark')
            self.remark = value_
            self.remark_nsprefix_ = child_.prefix
            # validate type RemarkType
            self.validate_RemarkType(self.remark)
        elif nodeName_ == 'additionalCustomerReference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'additionalCustomerReference')
            value_ = self.gds_validate_string(value_, node, 'additionalCustomerReference')
            self.additionalCustomerReference = value_
            self.additionalCustomerReference_nsprefix_ = child_.prefix
            # validate type RemarkType
            self.validate_RemarkType(self.additionalCustomerReference)
# end class BoxType


class CreateBoxType(BoxType):
    """CreateBoxType --  Type representing a box for creation. This type
    extends the base type and keeps additional information about box status.
    status --  Element holding information about the
    status of a box.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = BoxType
    def __init__(self, sender=None, nationalBox=None, internationalBox=None, remark=None, additionalCustomerReference=None, status=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("CreateBoxType"), self).__init__(sender, nationalBox, internationalBox, remark, additionalCustomerReference,  **kwargs_)
        self.status = status
        self.validate_SetBoxStatusType(self.status)
        self.status_nsprefix_ = "common"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CreateBoxType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CreateBoxType.subclass:
            return CreateBoxType.subclass(*args_, **kwargs_)
        else:
            return CreateBoxType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_status(self):
        return self.status
    def set_status(self, status):
        self.status = status
    def validate_SetBoxStatusType(self, value):
        result = True
        # Validate type SetBoxStatusType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['OPEN', 'CANCELLED', 'ON-HOLD']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on SetBoxStatusType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.status is not None or
            super(CreateBoxType, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CreateBoxType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CreateBoxType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CreateBoxType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CreateBoxType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CreateBoxType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CreateBoxType'):
        super(CreateBoxType, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CreateBoxType')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CreateBoxType', fromsubclass_=False, pretty_print=True):
        super(CreateBoxType, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.status is not None:
            namespaceprefix_ = self.status_nsprefix_ + ':' if (UseCapturedNS_ and self.status_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstatus>%s</%sstatus>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.status), input_name='status')), namespaceprefix_ , eol_))
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
        super(CreateBoxType, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'status':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'status')
            value_ = self.gds_validate_string(value_, node, 'status')
            self.status = value_
            self.status_nsprefix_ = child_.prefix
            # validate type SetBoxStatusType
            self.validate_SetBoxStatusType(self.status)
        super(CreateBoxType, self)._buildChildren(child_, node, nodeName_, True)
# end class CreateBoxType


class BoxInfoType(BoxType):
    """BoxInfoType --  Type representing a box for fetching. This type extends
    the base type and keeps additional information about the box barcode and status.
    barcode --  Element holding the barcode of a box.
    additionalBarcode --  Element holding an additional barcode
    of a box. For example the barcode used by a another postal operator
    outside the bpost network.
    status --  Element holding the status of a box.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = BoxType
    def __init__(self, sender=None, nationalBox=None, internationalBox=None, remark=None, additionalCustomerReference=None, barcode=None, additionalBarcode=None, status=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("BoxInfoType"), self).__init__(sender, nationalBox, internationalBox, remark, additionalCustomerReference,  **kwargs_)
        self.barcode = barcode
        self.validate_BarcodeType(self.barcode)
        self.barcode_nsprefix_ = "tns"
        self.additionalBarcode = additionalBarcode
        self.validate_BarcodeType(self.additionalBarcode)
        self.additionalBarcode_nsprefix_ = "tns"
        self.status = status
        self.validate_BoxStatusType(self.status)
        self.status_nsprefix_ = "common"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, BoxInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BoxInfoType.subclass:
            return BoxInfoType.subclass(*args_, **kwargs_)
        else:
            return BoxInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_barcode(self):
        return self.barcode
    def set_barcode(self, barcode):
        self.barcode = barcode
    def get_additionalBarcode(self):
        return self.additionalBarcode
    def set_additionalBarcode(self, additionalBarcode):
        self.additionalBarcode = additionalBarcode
    def get_status(self):
        return self.status
    def set_status(self, status):
        self.status = status
    def validate_BarcodeType(self, value):
        result = True
        # Validate type BarcodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_BoxStatusType(self, value):
        result = True
        # Validate type BoxStatusType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['PENDING', 'OPEN', 'CANCELLED', 'ON-HOLD', 'PRINTED', 'ANNOUNCED', 'IN_TRANSIT', 'AWAITING_PICKUP', 'DELIVERED', 'BACK_TO_SENDER']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on BoxStatusType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.barcode is not None or
            self.additionalBarcode is not None or
            self.status is not None or
            super(BoxInfoType, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BoxInfoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('BoxInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'BoxInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BoxInfoType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='BoxInfoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='BoxInfoType'):
        super(BoxInfoType, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BoxInfoType')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BoxInfoType', fromsubclass_=False, pretty_print=True):
        super(BoxInfoType, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.barcode is not None:
            namespaceprefix_ = self.barcode_nsprefix_ + ':' if (UseCapturedNS_ and self.barcode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sbarcode>%s</%sbarcode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.barcode), input_name='barcode')), namespaceprefix_ , eol_))
        if self.additionalBarcode is not None:
            namespaceprefix_ = self.additionalBarcode_nsprefix_ + ':' if (UseCapturedNS_ and self.additionalBarcode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sadditionalBarcode>%s</%sadditionalBarcode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.additionalBarcode), input_name='additionalBarcode')), namespaceprefix_ , eol_))
        if self.status is not None:
            namespaceprefix_ = self.status_nsprefix_ + ':' if (UseCapturedNS_ and self.status_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstatus>%s</%sstatus>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.status), input_name='status')), namespaceprefix_ , eol_))
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
        super(BoxInfoType, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'barcode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'barcode')
            value_ = self.gds_validate_string(value_, node, 'barcode')
            self.barcode = value_
            self.barcode_nsprefix_ = child_.prefix
            # validate type BarcodeType
            self.validate_BarcodeType(self.barcode)
        elif nodeName_ == 'additionalBarcode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'additionalBarcode')
            value_ = self.gds_validate_string(value_, node, 'additionalBarcode')
            self.additionalBarcode = value_
            self.additionalBarcode_nsprefix_ = child_.prefix
            # validate type BarcodeType
            self.validate_BarcodeType(self.additionalBarcode)
        elif nodeName_ == 'status':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'status')
            value_ = self.gds_validate_string(value_, node, 'status')
            self.status = value_
            self.status_nsprefix_ = child_.prefix
            # validate type BoxStatusType
            self.validate_BoxStatusType(self.status)
        super(BoxInfoType, self)._buildChildren(child_, node, nodeName_, True)
# end class BoxInfoType


class BatchLabelsType(GeneratedsSuper):
    """BatchLabelsType --  Type used for the request of creating labels in bulk.
    box --  Element holding information about (a) box(es)
    for label creation.
    order --  Element holding information about (an) order(s)
    for label creation.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, box=None, order=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if box is None:
            self.box = []
        else:
            self.box = box
        self.box_nsprefix_ = "tns"
        if order is None:
            self.order = []
        else:
            self.order = order
        self.order_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, BatchLabelsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BatchLabelsType.subclass:
            return BatchLabelsType.subclass(*args_, **kwargs_)
        else:
            return BatchLabelsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_box(self):
        return self.box
    def set_box(self, box):
        self.box = box
    def add_box(self, value):
        self.box.append(value)
    def insert_box_at(self, index, value):
        self.box.insert(index, value)
    def replace_box_at(self, index, value):
        self.box[index] = value
    def get_order(self):
        return self.order
    def set_order(self, order):
        self.order = order
    def add_order(self, value):
        self.order.append(value)
    def insert_order_at(self, index, value):
        self.order.insert(index, value)
    def replace_order_at(self, index, value):
        self.order[index] = value
    def validate_BarcodeType(self, value):
        result = True
        # Validate type BarcodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_OrderReferenceType(self, value):
        result = True
        # Validate type OrderReferenceType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 100:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on OrderReferenceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on OrderReferenceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_OrderReferenceType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_OrderReferenceType_patterns_, ))
                result = False
        return result
    validate_OrderReferenceType_patterns_ = [['^(.*[^\\s].*)$']]
    def has__content(self):
        if (
            self.box or
            self.order
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BatchLabelsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('BatchLabelsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'BatchLabelsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BatchLabelsType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='BatchLabelsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='BatchLabelsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BatchLabelsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for box_ in self.box:
            namespaceprefix_ = self.box_nsprefix_ + ':' if (UseCapturedNS_ and self.box_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sbox>%s</%sbox>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(box_), input_name='box')), namespaceprefix_ , eol_))
        for order_ in self.order:
            namespaceprefix_ = self.order_nsprefix_ + ':' if (UseCapturedNS_ and self.order_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorder>%s</%sorder>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(order_), input_name='order')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'box':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'box')
            value_ = self.gds_validate_string(value_, node, 'box')
            self.box.append(value_)
            self.box_nsprefix_ = child_.prefix
            # validate type BarcodeType
            self.validate_BarcodeType(self.box[-1])
        elif nodeName_ == 'order':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'order')
            value_ = self.gds_validate_string(value_, node, 'order')
            self.order.append(value_)
            self.order_nsprefix_ = child_.prefix
            # validate type OrderReferenceType
            self.validate_OrderReferenceType(self.order[-1])
# end class BatchLabelsType


class UnknownItemsType(GeneratedsSuper):
    """UnknownItemsType --  Type representing an unknown item when printing labels
    in bulk.
    box --  Element holding information about a box.
    order --  Element holding information about an order.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, box=None, order=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if box is None:
            self.box = []
        else:
            self.box = box
        self.box_nsprefix_ = "tns"
        if order is None:
            self.order = []
        else:
            self.order = order
        self.order_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UnknownItemsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UnknownItemsType.subclass:
            return UnknownItemsType.subclass(*args_, **kwargs_)
        else:
            return UnknownItemsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_box(self):
        return self.box
    def set_box(self, box):
        self.box = box
    def add_box(self, value):
        self.box.append(value)
    def insert_box_at(self, index, value):
        self.box.insert(index, value)
    def replace_box_at(self, index, value):
        self.box[index] = value
    def get_order(self):
        return self.order
    def set_order(self, order):
        self.order = order
    def add_order(self, value):
        self.order.append(value)
    def insert_order_at(self, index, value):
        self.order.insert(index, value)
    def replace_order_at(self, index, value):
        self.order[index] = value
    def validate_BarcodeType(self, value):
        result = True
        # Validate type BarcodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_OrderReferenceType(self, value):
        result = True
        # Validate type OrderReferenceType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 100:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on OrderReferenceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on OrderReferenceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_OrderReferenceType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_OrderReferenceType_patterns_, ))
                result = False
        return result
    validate_OrderReferenceType_patterns_ = [['^(.*[^\\s].*)$']]
    def has__content(self):
        if (
            self.box or
            self.order
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UnknownItemsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UnknownItemsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UnknownItemsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UnknownItemsType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UnknownItemsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UnknownItemsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UnknownItemsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for box_ in self.box:
            namespaceprefix_ = self.box_nsprefix_ + ':' if (UseCapturedNS_ and self.box_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sbox>%s</%sbox>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(box_), input_name='box')), namespaceprefix_ , eol_))
        for order_ in self.order:
            namespaceprefix_ = self.order_nsprefix_ + ':' if (UseCapturedNS_ and self.order_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sorder>%s</%sorder>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(order_), input_name='order')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'box':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'box')
            value_ = self.gds_validate_string(value_, node, 'box')
            self.box.append(value_)
            self.box_nsprefix_ = child_.prefix
            # validate type BarcodeType
            self.validate_BarcodeType(self.box[-1])
        elif nodeName_ == 'order':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'order')
            value_ = self.gds_validate_string(value_, node, 'order')
            self.order.append(value_)
            self.order_nsprefix_ = child_.prefix
            # validate type OrderReferenceType
            self.validate_OrderReferenceType(self.order[-1])
# end class UnknownItemsType


class LabelsType(GeneratedsSuper):
    """LabelsType --  Type representing the type of a label.
    label --  Element holding information about a label.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, label=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if label is None:
            self.label = []
        else:
            self.label = label
        self.label_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LabelsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LabelsType.subclass:
            return LabelsType.subclass(*args_, **kwargs_)
        else:
            return LabelsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_label(self):
        return self.label
    def set_label(self, label):
        self.label = label
    def add_label(self, value):
        self.label.append(value)
    def insert_label_at(self, index, value):
        self.label.insert(index, value)
    def replace_label_at(self, index, value):
        self.label[index] = value
    def has__content(self):
        if (
            self.label
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LabelsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LabelsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LabelsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LabelsType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LabelsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LabelsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LabelsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for label_ in self.label:
            namespaceprefix_ = self.label_nsprefix_ + ':' if (UseCapturedNS_ and self.label_nsprefix_) else ''
            label_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='label', pretty_print=pretty_print)
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
        if nodeName_ == 'label':
            obj_ = labelType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.label.append(obj_)
            obj_.original_tagname_ = 'label'
# end class LabelsType


class ProductConfigurationType(GeneratedsSuper):
    """ProductConfigurationType --  Type representing the configuration of a product.
    deliveryMethod --  Element holding the information on how a parcel
    will be delivered.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, deliveryMethod=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if deliveryMethod is None:
            self.deliveryMethod = []
        else:
            self.deliveryMethod = deliveryMethod
        self.deliveryMethod_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ProductConfigurationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ProductConfigurationType.subclass:
            return ProductConfigurationType.subclass(*args_, **kwargs_)
        else:
            return ProductConfigurationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_deliveryMethod(self):
        return self.deliveryMethod
    def set_deliveryMethod(self, deliveryMethod):
        self.deliveryMethod = deliveryMethod
    def add_deliveryMethod(self, value):
        self.deliveryMethod.append(value)
    def insert_deliveryMethod_at(self, index, value):
        self.deliveryMethod.insert(index, value)
    def replace_deliveryMethod_at(self, index, value):
        self.deliveryMethod[index] = value
    def has__content(self):
        if (
            self.deliveryMethod
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ProductConfigurationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ProductConfigurationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ProductConfigurationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ProductConfigurationType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ProductConfigurationType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ProductConfigurationType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ProductConfigurationType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for deliveryMethod_ in self.deliveryMethod:
            namespaceprefix_ = self.deliveryMethod_nsprefix_ + ':' if (UseCapturedNS_ and self.deliveryMethod_nsprefix_) else ''
            deliveryMethod_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='deliveryMethod', pretty_print=pretty_print)
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
        if nodeName_ == 'deliveryMethod':
            obj_ = deliveryMethodType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.deliveryMethod.append(obj_)
            obj_.original_tagname_ = 'deliveryMethod'
# end class ProductConfigurationType


class InvalidSelectionType(GeneratedsSuper):
    """InvalidSelectionType --  Type representing an invalid selection when choosing
    options for a certain product.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, error=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if error is None:
            self.error = []
        else:
            self.error = error
        self.error_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, InvalidSelectionType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if InvalidSelectionType.subclass:
            return InvalidSelectionType.subclass(*args_, **kwargs_)
        else:
            return InvalidSelectionType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_error(self):
        return self.error
    def set_error(self, error):
        self.error = error
    def add_error(self, value):
        self.error.append(value)
    def insert_error_at(self, index, value):
        self.error.insert(index, value)
    def replace_error_at(self, index, value):
        self.error[index] = value
    def has__content(self):
        if (
            self.error
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='InvalidSelectionType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('InvalidSelectionType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'InvalidSelectionType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='InvalidSelectionType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='InvalidSelectionType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='InvalidSelectionType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='InvalidSelectionType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for error_ in self.error:
            namespaceprefix_ = self.error_nsprefix_ + ':' if (UseCapturedNS_ and self.error_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%serror>%s</%serror>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(error_), input_name='error')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'error':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'error')
            value_ = self.gds_validate_string(value_, node, 'error')
            self.error.append(value_)
            self.error_nsprefix_ = child_.prefix
# end class InvalidSelectionType


class BarcodeWithReferenceType(GeneratedsSuper):
    """BarcodeWithReferenceType --  Type representing a barcode with its corresponding
    order reference
    barcode --  Element holding information about a barcode of
    a label.
    crossReferenceBarcode --  Element holding the cross reference barcodee of
    a label.
    reference --  Element holding the order reference of a label.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, barcode=None, crossReferenceBarcode=None, reference=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.barcode = barcode
        self.validate_BarcodeType(self.barcode)
        self.barcode_nsprefix_ = "tns"
        self.crossReferenceBarcode = crossReferenceBarcode
        self.validate_CrossReferenceBarcodeType(self.crossReferenceBarcode)
        self.crossReferenceBarcode_nsprefix_ = "tns"
        self.reference = reference
        self.validate_OrderReferenceType(self.reference)
        self.reference_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, BarcodeWithReferenceType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BarcodeWithReferenceType.subclass:
            return BarcodeWithReferenceType.subclass(*args_, **kwargs_)
        else:
            return BarcodeWithReferenceType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_barcode(self):
        return self.barcode
    def set_barcode(self, barcode):
        self.barcode = barcode
    def get_crossReferenceBarcode(self):
        return self.crossReferenceBarcode
    def set_crossReferenceBarcode(self, crossReferenceBarcode):
        self.crossReferenceBarcode = crossReferenceBarcode
    def get_reference(self):
        return self.reference
    def set_reference(self, reference):
        self.reference = reference
    def validate_BarcodeType(self, value):
        result = True
        # Validate type BarcodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_CrossReferenceBarcodeType(self, value):
        result = True
        # Validate type CrossReferenceBarcodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_OrderReferenceType(self, value):
        result = True
        # Validate type OrderReferenceType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 100:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on OrderReferenceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on OrderReferenceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_OrderReferenceType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_OrderReferenceType_patterns_, ))
                result = False
        return result
    validate_OrderReferenceType_patterns_ = [['^(.*[^\\s].*)$']]
    def has__content(self):
        if (
            self.barcode is not None or
            self.crossReferenceBarcode is not None or
            self.reference is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BarcodeWithReferenceType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('BarcodeWithReferenceType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'BarcodeWithReferenceType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BarcodeWithReferenceType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='BarcodeWithReferenceType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='BarcodeWithReferenceType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BarcodeWithReferenceType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.barcode is not None:
            namespaceprefix_ = self.barcode_nsprefix_ + ':' if (UseCapturedNS_ and self.barcode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sbarcode>%s</%sbarcode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.barcode), input_name='barcode')), namespaceprefix_ , eol_))
        if self.crossReferenceBarcode is not None:
            namespaceprefix_ = self.crossReferenceBarcode_nsprefix_ + ':' if (UseCapturedNS_ and self.crossReferenceBarcode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scrossReferenceBarcode>%s</%scrossReferenceBarcode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.crossReferenceBarcode), input_name='crossReferenceBarcode')), namespaceprefix_ , eol_))
        if self.reference is not None:
            namespaceprefix_ = self.reference_nsprefix_ + ':' if (UseCapturedNS_ and self.reference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sreference>%s</%sreference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.reference), input_name='reference')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'barcode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'barcode')
            value_ = self.gds_validate_string(value_, node, 'barcode')
            self.barcode = value_
            self.barcode_nsprefix_ = child_.prefix
            # validate type BarcodeType
            self.validate_BarcodeType(self.barcode)
        elif nodeName_ == 'crossReferenceBarcode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'crossReferenceBarcode')
            value_ = self.gds_validate_string(value_, node, 'crossReferenceBarcode')
            self.crossReferenceBarcode = value_
            self.crossReferenceBarcode_nsprefix_ = child_.prefix
            # validate type CrossReferenceBarcodeType
            self.validate_CrossReferenceBarcodeType(self.crossReferenceBarcode)
        elif nodeName_ == 'reference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'reference')
            value_ = self.gds_validate_string(value_, node, 'reference')
            self.reference = value_
            self.reference_nsprefix_ = child_.prefix
            # validate type OrderReferenceType
            self.validate_OrderReferenceType(self.reference)
# end class BarcodeWithReferenceType


class Party(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, name=None, company=None, address=None, emailAddress=None, phoneNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name = name
        self.validate_ReceiverNameType(self.name)
        self.name_nsprefix_ = "tns"
        self.company = company
        self.validate_ReceiverCompany(self.company)
        self.company_nsprefix_ = "tns"
        self.address = address
        self.address_nsprefix_ = "tns"
        self.emailAddress = emailAddress
        self.validate_EmailAddressType(self.emailAddress)
        self.emailAddress_nsprefix_ = "tns"
        self.phoneNumber = phoneNumber
        self.validate_PhoneNumberType(self.phoneNumber)
        self.phoneNumber_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Party)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Party.subclass:
            return Party.subclass(*args_, **kwargs_)
        else:
            return Party(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_company(self):
        return self.company
    def set_company(self, company):
        self.company = company
    def get_address(self):
        return self.address
    def set_address(self, address):
        self.address = address
    def get_emailAddress(self):
        return self.emailAddress
    def set_emailAddress(self, emailAddress):
        self.emailAddress = emailAddress
    def get_phoneNumber(self):
        return self.phoneNumber
    def set_phoneNumber(self, phoneNumber):
        self.phoneNumber = phoneNumber
    def validate_ReceiverNameType(self, value):
        result = True
        # Validate type ReceiverNameType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ReceiverNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on ReceiverNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_ReceiverNameType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_ReceiverNameType_patterns_, ))
                result = False
        return result
    validate_ReceiverNameType_patterns_ = [['^(.*[^\\s].*)$']]
    def validate_ReceiverCompany(self, value):
        result = True
        # Validate type ReceiverCompany, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ReceiverCompany' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_EmailAddressType(self, value):
        result = True
        # Validate type EmailAddressType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on EmailAddressType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_EmailAddressType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_EmailAddressType_patterns_, ))
                result = False
        return result
    validate_EmailAddressType_patterns_ = [["^([-!#$%&'*+/0-9=?A-Z^_a-z{|}~](\\.?[-!#$%&'*+/0-9=?A-Z^_a-z`{|}~])*@[a-zA-Z0-9](-*\\.?[a-zA-Z0-9])*\\.[a-zA-Z](-?[a-zA-Z0-9])+)$"]]
    def validate_PhoneNumberType(self, value):
        result = True
        # Validate type PhoneNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on PhoneNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on PhoneNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_PhoneNumberType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_PhoneNumberType_patterns_, ))
                result = False
        return result
    validate_PhoneNumberType_patterns_ = [['^(.*[^\\s].*)$']]
    def has__content(self):
        if (
            self.name is not None or
            self.company is not None or
            self.address is not None or
            self.emailAddress is not None or
            self.phoneNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Party', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Party')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Party':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Party')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Party', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Party'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Party', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.name is not None:
            namespaceprefix_ = self.name_nsprefix_ + ':' if (UseCapturedNS_ and self.name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sname>%s</%sname>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.name), input_name='name')), namespaceprefix_ , eol_))
        if self.company is not None:
            namespaceprefix_ = self.company_nsprefix_ + ':' if (UseCapturedNS_ and self.company_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scompany>%s</%scompany>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.company), input_name='company')), namespaceprefix_ , eol_))
        if self.address is not None:
            namespaceprefix_ = self.address_nsprefix_ + ':' if (UseCapturedNS_ and self.address_nsprefix_) else ''
            self.address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='address', pretty_print=pretty_print)
        if self.emailAddress is not None:
            namespaceprefix_ = self.emailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.emailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%semailAddress>%s</%semailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.emailAddress), input_name='emailAddress')), namespaceprefix_ , eol_))
        if self.phoneNumber is not None:
            namespaceprefix_ = self.phoneNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.phoneNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sphoneNumber>%s</%sphoneNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.phoneNumber), input_name='phoneNumber')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'name')
            value_ = self.gds_validate_string(value_, node, 'name')
            self.name = value_
            self.name_nsprefix_ = child_.prefix
            # validate type ReceiverNameType
            self.validate_ReceiverNameType(self.name)
        elif nodeName_ == 'company':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'company')
            value_ = self.gds_validate_string(value_, node, 'company')
            self.company = value_
            self.company_nsprefix_ = child_.prefix
            # validate type ReceiverCompany
            self.validate_ReceiverCompany(self.company)
        elif nodeName_ == 'address':
            obj_ = AddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.address = obj_
            obj_.original_tagname_ = 'address'
        elif nodeName_ == 'emailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'emailAddress')
            value_ = self.gds_validate_string(value_, node, 'emailAddress')
            self.emailAddress = value_
            self.emailAddress_nsprefix_ = child_.prefix
            # validate type EmailAddressType
            self.validate_EmailAddressType(self.emailAddress)
        elif nodeName_ == 'phoneNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'phoneNumber')
            value_ = self.gds_validate_string(value_, node, 'phoneNumber')
            self.phoneNumber = value_
            self.phoneNumber_nsprefix_ = child_.prefix
            # validate type PhoneNumberType
            self.validate_PhoneNumberType(self.phoneNumber)
# end class Party


class AddressType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, streetName=None, addressLineTwo=None, number=None, box=None, postalCode=None, locality=None, countryCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.streetName = streetName
        self.validate_StreetNameType(self.streetName)
        self.streetName_nsprefix_ = "tns"
        self.addressLineTwo = addressLineTwo
        self.validate_StreetNameType(self.addressLineTwo)
        self.addressLineTwo_nsprefix_ = "tns"
        self.number = number
        self.validate_StreetNumberType(self.number)
        self.number_nsprefix_ = "tns"
        self.box = box
        self.validate_StreetBoxType(self.box)
        self.box_nsprefix_ = "tns"
        self.postalCode = postalCode
        self.validate_PostalCodeType(self.postalCode)
        self.postalCode_nsprefix_ = "tns"
        self.locality = locality
        self.validate_LocalityType(self.locality)
        self.locality_nsprefix_ = "tns"
        self.countryCode = countryCode
        self.validate_CountryCode(self.countryCode)
        self.countryCode_nsprefix_ = "tns"
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
    def get_streetName(self):
        return self.streetName
    def set_streetName(self, streetName):
        self.streetName = streetName
    def get_addressLineTwo(self):
        return self.addressLineTwo
    def set_addressLineTwo(self, addressLineTwo):
        self.addressLineTwo = addressLineTwo
    def get_number(self):
        return self.number
    def set_number(self, number):
        self.number = number
    def get_box(self):
        return self.box
    def set_box(self, box):
        self.box = box
    def get_postalCode(self):
        return self.postalCode
    def set_postalCode(self, postalCode):
        self.postalCode = postalCode
    def get_locality(self):
        return self.locality
    def set_locality(self, locality):
        self.locality = locality
    def get_countryCode(self):
        return self.countryCode
    def set_countryCode(self, countryCode):
        self.countryCode = countryCode
    def validate_StreetNameType(self, value):
        result = True
        # Validate type StreetNameType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on StreetNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on StreetNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_StreetNameType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_StreetNameType_patterns_, ))
                result = False
        return result
    validate_StreetNameType_patterns_ = [['^(.*[^\\s].*)$']]
    def validate_StreetNumberType(self, value):
        result = True
        # Validate type StreetNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 8:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on StreetNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on StreetNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_StreetNumberType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_StreetNumberType_patterns_, ))
                result = False
        return result
    validate_StreetNumberType_patterns_ = [['^(.*[^\\s].*)$']]
    def validate_StreetBoxType(self, value):
        result = True
        # Validate type StreetBoxType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 8:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on StreetBoxType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on StreetBoxType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_StreetBoxType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_StreetBoxType_patterns_, ))
                result = False
        return result
    validate_StreetBoxType_patterns_ = [['^(.*[^\\s].*)$']]
    def validate_PostalCodeType(self, value):
        result = True
        # Validate type PostalCodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 8:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on PostalCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on PostalCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_PostalCodeType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_PostalCodeType_patterns_, ))
                result = False
        return result
    validate_PostalCodeType_patterns_ = [['^(.*[^\\s].*)$']]
    def validate_LocalityType(self, value):
        result = True
        # Validate type LocalityType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on LocalityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on LocalityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_LocalityType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_LocalityType_patterns_, ))
                result = False
        return result
    validate_LocalityType_patterns_ = [['^(.*[^\\s].*)$']]
    def validate_CountryCode(self, value):
        result = True
        # Validate type CountryCode, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_CountryCode_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_CountryCode_patterns_, ))
                result = False
        return result
    validate_CountryCode_patterns_ = [['^([A-Z]{2})$']]
    def has__content(self):
        if (
            self.streetName is not None or
            self.addressLineTwo is not None or
            self.number is not None or
            self.box is not None or
            self.postalCode is not None or
            self.locality is not None or
            self.countryCode is not None
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
        if self.has__content():
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
        if self.streetName is not None:
            namespaceprefix_ = self.streetName_nsprefix_ + ':' if (UseCapturedNS_ and self.streetName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstreetName>%s</%sstreetName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.streetName), input_name='streetName')), namespaceprefix_ , eol_))
        if self.addressLineTwo is not None:
            namespaceprefix_ = self.addressLineTwo_nsprefix_ + ':' if (UseCapturedNS_ and self.addressLineTwo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saddressLineTwo>%s</%saddressLineTwo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.addressLineTwo), input_name='addressLineTwo')), namespaceprefix_ , eol_))
        if self.number is not None:
            namespaceprefix_ = self.number_nsprefix_ + ':' if (UseCapturedNS_ and self.number_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snumber>%s</%snumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.number), input_name='number')), namespaceprefix_ , eol_))
        if self.box is not None:
            namespaceprefix_ = self.box_nsprefix_ + ':' if (UseCapturedNS_ and self.box_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sbox>%s</%sbox>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.box), input_name='box')), namespaceprefix_ , eol_))
        if self.postalCode is not None:
            namespaceprefix_ = self.postalCode_nsprefix_ + ':' if (UseCapturedNS_ and self.postalCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spostalCode>%s</%spostalCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.postalCode), input_name='postalCode')), namespaceprefix_ , eol_))
        if self.locality is not None:
            namespaceprefix_ = self.locality_nsprefix_ + ':' if (UseCapturedNS_ and self.locality_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slocality>%s</%slocality>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.locality), input_name='locality')), namespaceprefix_ , eol_))
        if self.countryCode is not None:
            namespaceprefix_ = self.countryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.countryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scountryCode>%s</%scountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.countryCode), input_name='countryCode')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'streetName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'streetName')
            value_ = self.gds_validate_string(value_, node, 'streetName')
            self.streetName = value_
            self.streetName_nsprefix_ = child_.prefix
            # validate type StreetNameType
            self.validate_StreetNameType(self.streetName)
        elif nodeName_ == 'addressLineTwo':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'addressLineTwo')
            value_ = self.gds_validate_string(value_, node, 'addressLineTwo')
            self.addressLineTwo = value_
            self.addressLineTwo_nsprefix_ = child_.prefix
            # validate type StreetNameType
            self.validate_StreetNameType(self.addressLineTwo)
        elif nodeName_ == 'number':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'number')
            value_ = self.gds_validate_string(value_, node, 'number')
            self.number = value_
            self.number_nsprefix_ = child_.prefix
            # validate type StreetNumberType
            self.validate_StreetNumberType(self.number)
        elif nodeName_ == 'box':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'box')
            value_ = self.gds_validate_string(value_, node, 'box')
            self.box = value_
            self.box_nsprefix_ = child_.prefix
            # validate type StreetBoxType
            self.validate_StreetBoxType(self.box)
        elif nodeName_ == 'postalCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'postalCode')
            value_ = self.gds_validate_string(value_, node, 'postalCode')
            self.postalCode = value_
            self.postalCode_nsprefix_ = child_.prefix
            # validate type PostalCodeType
            self.validate_PostalCodeType(self.postalCode)
        elif nodeName_ == 'locality':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'locality')
            value_ = self.gds_validate_string(value_, node, 'locality')
            self.locality = value_
            self.locality_nsprefix_ = child_.prefix
            # validate type LocalityType
            self.validate_LocalityType(self.locality)
        elif nodeName_ == 'countryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'countryCode')
            value_ = self.gds_validate_string(value_, node, 'countryCode')
            self.countryCode = value_
            self.countryCode_nsprefix_ = child_.prefix
            # validate type CountryCode
            self.validate_CountryCode(self.countryCode)
# end class AddressType


class OptionsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, infoDistributed=None, infoNextDay=None, infoReminder=None, keepMeInformed=None, automaticSecondPresentation=None, fragile=None, insured=None, signed=None, timeSlotDelivery=None, saturdayDelivery=None, sundayDelivery=None, sameDayDelivery=None, cod=None, preferredDeliveryWindow=None, fullService=None, doorStepPlusService=None, ultraLateInEveningDelivery=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.infoDistributed = infoDistributed
        self.infoDistributed_nsprefix_ = None
        self.infoNextDay = infoNextDay
        self.infoNextDay_nsprefix_ = None
        self.infoReminder = infoReminder
        self.infoReminder_nsprefix_ = None
        self.keepMeInformed = keepMeInformed
        self.keepMeInformed_nsprefix_ = None
        self.automaticSecondPresentation = automaticSecondPresentation
        self.automaticSecondPresentation_nsprefix_ = None
        self.fragile = fragile
        self.fragile_nsprefix_ = None
        self.insured = insured
        self.insured_nsprefix_ = None
        self.signed = signed
        self.signed_nsprefix_ = None
        self.timeSlotDelivery = timeSlotDelivery
        self.timeSlotDelivery_nsprefix_ = None
        self.saturdayDelivery = saturdayDelivery
        self.saturdayDelivery_nsprefix_ = None
        self.sundayDelivery = sundayDelivery
        self.sundayDelivery_nsprefix_ = None
        self.sameDayDelivery = sameDayDelivery
        self.sameDayDelivery_nsprefix_ = None
        self.cod = cod
        self.cod_nsprefix_ = None
        self.preferredDeliveryWindow = preferredDeliveryWindow
        self.validate_PreferredDeliveryWindowType(self.preferredDeliveryWindow)
        self.preferredDeliveryWindow_nsprefix_ = None
        self.fullService = fullService
        self.fullService_nsprefix_ = None
        self.doorStepPlusService = doorStepPlusService
        self.doorStepPlusService_nsprefix_ = None
        self.ultraLateInEveningDelivery = ultraLateInEveningDelivery
        self.ultraLateInEveningDelivery_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, OptionsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OptionsType.subclass:
            return OptionsType.subclass(*args_, **kwargs_)
        else:
            return OptionsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_infoDistributed(self):
        return self.infoDistributed
    def set_infoDistributed(self, infoDistributed):
        self.infoDistributed = infoDistributed
    def get_infoNextDay(self):
        return self.infoNextDay
    def set_infoNextDay(self, infoNextDay):
        self.infoNextDay = infoNextDay
    def get_infoReminder(self):
        return self.infoReminder
    def set_infoReminder(self, infoReminder):
        self.infoReminder = infoReminder
    def get_keepMeInformed(self):
        return self.keepMeInformed
    def set_keepMeInformed(self, keepMeInformed):
        self.keepMeInformed = keepMeInformed
    def get_automaticSecondPresentation(self):
        return self.automaticSecondPresentation
    def set_automaticSecondPresentation(self, automaticSecondPresentation):
        self.automaticSecondPresentation = automaticSecondPresentation
    def get_fragile(self):
        return self.fragile
    def set_fragile(self, fragile):
        self.fragile = fragile
    def get_insured(self):
        return self.insured
    def set_insured(self, insured):
        self.insured = insured
    def get_signed(self):
        return self.signed
    def set_signed(self, signed):
        self.signed = signed
    def get_timeSlotDelivery(self):
        return self.timeSlotDelivery
    def set_timeSlotDelivery(self, timeSlotDelivery):
        self.timeSlotDelivery = timeSlotDelivery
    def get_saturdayDelivery(self):
        return self.saturdayDelivery
    def set_saturdayDelivery(self, saturdayDelivery):
        self.saturdayDelivery = saturdayDelivery
    def get_sundayDelivery(self):
        return self.sundayDelivery
    def set_sundayDelivery(self, sundayDelivery):
        self.sundayDelivery = sundayDelivery
    def get_sameDayDelivery(self):
        return self.sameDayDelivery
    def set_sameDayDelivery(self, sameDayDelivery):
        self.sameDayDelivery = sameDayDelivery
    def get_cod(self):
        return self.cod
    def set_cod(self, cod):
        self.cod = cod
    def get_preferredDeliveryWindow(self):
        return self.preferredDeliveryWindow
    def set_preferredDeliveryWindow(self, preferredDeliveryWindow):
        self.preferredDeliveryWindow = preferredDeliveryWindow
    def get_fullService(self):
        return self.fullService
    def set_fullService(self, fullService):
        self.fullService = fullService
    def get_doorStepPlusService(self):
        return self.doorStepPlusService
    def set_doorStepPlusService(self, doorStepPlusService):
        self.doorStepPlusService = doorStepPlusService
    def get_ultraLateInEveningDelivery(self):
        return self.ultraLateInEveningDelivery
    def set_ultraLateInEveningDelivery(self, ultraLateInEveningDelivery):
        self.ultraLateInEveningDelivery = ultraLateInEveningDelivery
    def validate_PreferredDeliveryWindowType(self, value):
        result = True
        # Validate type PreferredDeliveryWindowType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_PreferredDeliveryWindowType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_PreferredDeliveryWindowType_patterns_, ))
                result = False
        return result
    validate_PreferredDeliveryWindowType_patterns_ = [['^([Aa][Mm])$', '^([Pp][Mm])$', '^([Pp][Mm][Pp][Ll][Uu][Ss])$', '^([Oo][Ff][Ff][Ii][Cc][Ee])$']]
    def has__content(self):
        if (
            self.infoDistributed is not None or
            self.infoNextDay is not None or
            self.infoReminder is not None or
            self.keepMeInformed is not None or
            self.automaticSecondPresentation is not None or
            self.fragile is not None or
            self.insured is not None or
            self.signed is not None or
            self.timeSlotDelivery is not None or
            self.saturdayDelivery is not None or
            self.sundayDelivery is not None or
            self.sameDayDelivery is not None or
            self.cod is not None or
            self.preferredDeliveryWindow is not None or
            self.fullService is not None or
            self.doorStepPlusService is not None or
            self.ultraLateInEveningDelivery is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OptionsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OptionsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'OptionsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OptionsType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='OptionsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='OptionsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OptionsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.infoDistributed is not None:
            namespaceprefix_ = self.infoDistributed_nsprefix_ + ':' if (UseCapturedNS_ and self.infoDistributed_nsprefix_) else ''
            self.infoDistributed.export(outfile, level, namespaceprefix_, namespacedef_='', name_='infoDistributed', pretty_print=pretty_print)
        if self.infoNextDay is not None:
            namespaceprefix_ = self.infoNextDay_nsprefix_ + ':' if (UseCapturedNS_ and self.infoNextDay_nsprefix_) else ''
            self.infoNextDay.export(outfile, level, namespaceprefix_, namespacedef_='', name_='infoNextDay', pretty_print=pretty_print)
        if self.infoReminder is not None:
            namespaceprefix_ = self.infoReminder_nsprefix_ + ':' if (UseCapturedNS_ and self.infoReminder_nsprefix_) else ''
            self.infoReminder.export(outfile, level, namespaceprefix_, namespacedef_='', name_='infoReminder', pretty_print=pretty_print)
        if self.keepMeInformed is not None:
            namespaceprefix_ = self.keepMeInformed_nsprefix_ + ':' if (UseCapturedNS_ and self.keepMeInformed_nsprefix_) else ''
            self.keepMeInformed.export(outfile, level, namespaceprefix_, namespacedef_='', name_='keepMeInformed', pretty_print=pretty_print)
        if self.automaticSecondPresentation is not None:
            namespaceprefix_ = self.automaticSecondPresentation_nsprefix_ + ':' if (UseCapturedNS_ and self.automaticSecondPresentation_nsprefix_) else ''
            self.automaticSecondPresentation.export(outfile, level, namespaceprefix_, namespacedef_='', name_='automaticSecondPresentation', pretty_print=pretty_print)
        if self.fragile is not None:
            namespaceprefix_ = self.fragile_nsprefix_ + ':' if (UseCapturedNS_ and self.fragile_nsprefix_) else ''
            self.fragile.export(outfile, level, namespaceprefix_, namespacedef_='', name_='fragile', pretty_print=pretty_print)
        if self.insured is not None:
            namespaceprefix_ = self.insured_nsprefix_ + ':' if (UseCapturedNS_ and self.insured_nsprefix_) else ''
            self.insured.export(outfile, level, namespaceprefix_, namespacedef_='', name_='insured', pretty_print=pretty_print)
        if self.signed is not None:
            namespaceprefix_ = self.signed_nsprefix_ + ':' if (UseCapturedNS_ and self.signed_nsprefix_) else ''
            self.signed.export(outfile, level, namespaceprefix_, namespacedef_='', name_='signed', pretty_print=pretty_print)
        if self.timeSlotDelivery is not None:
            namespaceprefix_ = self.timeSlotDelivery_nsprefix_ + ':' if (UseCapturedNS_ and self.timeSlotDelivery_nsprefix_) else ''
            self.timeSlotDelivery.export(outfile, level, namespaceprefix_, namespacedef_='', name_='timeSlotDelivery', pretty_print=pretty_print)
        if self.saturdayDelivery is not None:
            namespaceprefix_ = self.saturdayDelivery_nsprefix_ + ':' if (UseCapturedNS_ and self.saturdayDelivery_nsprefix_) else ''
            self.saturdayDelivery.export(outfile, level, namespaceprefix_, namespacedef_='', name_='saturdayDelivery', pretty_print=pretty_print)
        if self.sundayDelivery is not None:
            namespaceprefix_ = self.sundayDelivery_nsprefix_ + ':' if (UseCapturedNS_ and self.sundayDelivery_nsprefix_) else ''
            self.sundayDelivery.export(outfile, level, namespaceprefix_, namespacedef_='', name_='sundayDelivery', pretty_print=pretty_print)
        if self.sameDayDelivery is not None:
            namespaceprefix_ = self.sameDayDelivery_nsprefix_ + ':' if (UseCapturedNS_ and self.sameDayDelivery_nsprefix_) else ''
            self.sameDayDelivery.export(outfile, level, namespaceprefix_, namespacedef_='', name_='sameDayDelivery', pretty_print=pretty_print)
        if self.cod is not None:
            namespaceprefix_ = self.cod_nsprefix_ + ':' if (UseCapturedNS_ and self.cod_nsprefix_) else ''
            self.cod.export(outfile, level, namespaceprefix_, namespacedef_='', name_='cod', pretty_print=pretty_print)
        if self.preferredDeliveryWindow is not None:
            namespaceprefix_ = self.preferredDeliveryWindow_nsprefix_ + ':' if (UseCapturedNS_ and self.preferredDeliveryWindow_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spreferredDeliveryWindow>%s</%spreferredDeliveryWindow>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.preferredDeliveryWindow), input_name='preferredDeliveryWindow')), namespaceprefix_ , eol_))
        if self.fullService is not None:
            namespaceprefix_ = self.fullService_nsprefix_ + ':' if (UseCapturedNS_ and self.fullService_nsprefix_) else ''
            self.fullService.export(outfile, level, namespaceprefix_, namespacedef_='', name_='fullService', pretty_print=pretty_print)
        if self.doorStepPlusService is not None:
            namespaceprefix_ = self.doorStepPlusService_nsprefix_ + ':' if (UseCapturedNS_ and self.doorStepPlusService_nsprefix_) else ''
            self.doorStepPlusService.export(outfile, level, namespaceprefix_, namespacedef_='', name_='doorStepPlusService', pretty_print=pretty_print)
        if self.ultraLateInEveningDelivery is not None:
            namespaceprefix_ = self.ultraLateInEveningDelivery_nsprefix_ + ':' if (UseCapturedNS_ and self.ultraLateInEveningDelivery_nsprefix_) else ''
            self.ultraLateInEveningDelivery.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ultraLateInEveningDelivery', pretty_print=pretty_print)
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
        if nodeName_ == 'infoDistributed':
            class_obj_ = self.get_class_obj_(child_, NotificationType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.infoDistributed = obj_
            obj_.original_tagname_ = 'infoDistributed'
        elif nodeName_ == 'infoNextDay':
            class_obj_ = self.get_class_obj_(child_, NotificationType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.infoNextDay = obj_
            obj_.original_tagname_ = 'infoNextDay'
        elif nodeName_ == 'infoReminder':
            class_obj_ = self.get_class_obj_(child_, NotificationType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.infoReminder = obj_
            obj_.original_tagname_ = 'infoReminder'
        elif nodeName_ == 'keepMeInformed':
            class_obj_ = self.get_class_obj_(child_, NotificationType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.keepMeInformed = obj_
            obj_.original_tagname_ = 'keepMeInformed'
        elif nodeName_ == 'automaticSecondPresentation':
            obj_ = automaticSecondPresentationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.automaticSecondPresentation = obj_
            obj_.original_tagname_ = 'automaticSecondPresentation'
        elif nodeName_ == 'fragile':
            obj_ = FragileType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.fragile = obj_
            obj_.original_tagname_ = 'fragile'
        elif nodeName_ == 'insured':
            obj_ = InsuranceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.insured = obj_
            obj_.original_tagname_ = 'insured'
        elif nodeName_ == 'signed':
            obj_ = SignatureType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.signed = obj_
            obj_.original_tagname_ = 'signed'
        elif nodeName_ == 'timeSlotDelivery':
            obj_ = TimeSlotDeliveryType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.timeSlotDelivery = obj_
            obj_.original_tagname_ = 'timeSlotDelivery'
        elif nodeName_ == 'saturdayDelivery':
            obj_ = SaturdayDeliveryType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.saturdayDelivery = obj_
            obj_.original_tagname_ = 'saturdayDelivery'
        elif nodeName_ == 'sundayDelivery':
            obj_ = SundayDeliveryType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.sundayDelivery = obj_
            obj_.original_tagname_ = 'sundayDelivery'
        elif nodeName_ == 'sameDayDelivery':
            class_obj_ = self.get_class_obj_(child_, NotificationType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.sameDayDelivery = obj_
            obj_.original_tagname_ = 'sameDayDelivery'
        elif nodeName_ == 'cod':
            obj_ = CodType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.cod = obj_
            obj_.original_tagname_ = 'cod'
        elif nodeName_ == 'preferredDeliveryWindow':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'preferredDeliveryWindow')
            value_ = self.gds_validate_string(value_, node, 'preferredDeliveryWindow')
            self.preferredDeliveryWindow = value_
            self.preferredDeliveryWindow_nsprefix_ = child_.prefix
            # validate type PreferredDeliveryWindowType
            self.validate_PreferredDeliveryWindowType(self.preferredDeliveryWindow)
        elif nodeName_ == 'fullService':
            obj_ = FullServiceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.fullService = obj_
            obj_.original_tagname_ = 'fullService'
        elif nodeName_ == 'doorStepPlusService':
            obj_ = DoorStepPlusServiceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.doorStepPlusService = obj_
            obj_.original_tagname_ = 'doorStepPlusService'
        elif nodeName_ == 'ultraLateInEveningDelivery':
            obj_ = UltraLateInEveningDelivery.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ultraLateInEveningDelivery = obj_
            obj_.original_tagname_ = 'ultraLateInEveningDelivery'
# end class OptionsType


class InsuranceType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, basicInsurance=None, additionalInsurance=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.basicInsurance = basicInsurance
        self.basicInsurance_nsprefix_ = None
        self.additionalInsurance = additionalInsurance
        self.additionalInsurance_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, InsuranceType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if InsuranceType.subclass:
            return InsuranceType.subclass(*args_, **kwargs_)
        else:
            return InsuranceType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_basicInsurance(self):
        return self.basicInsurance
    def set_basicInsurance(self, basicInsurance):
        self.basicInsurance = basicInsurance
    def get_additionalInsurance(self):
        return self.additionalInsurance
    def set_additionalInsurance(self, additionalInsurance):
        self.additionalInsurance = additionalInsurance
    def has__content(self):
        if (
            self.basicInsurance is not None or
            self.additionalInsurance is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='InsuranceType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('InsuranceType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'InsuranceType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='InsuranceType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='InsuranceType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='InsuranceType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='InsuranceType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.basicInsurance is not None:
            namespaceprefix_ = self.basicInsurance_nsprefix_ + ':' if (UseCapturedNS_ and self.basicInsurance_nsprefix_) else ''
            self.basicInsurance.export(outfile, level, namespaceprefix_, namespacedef_='', name_='basicInsurance', pretty_print=pretty_print)
        if self.additionalInsurance is not None:
            namespaceprefix_ = self.additionalInsurance_nsprefix_ + ':' if (UseCapturedNS_ and self.additionalInsurance_nsprefix_) else ''
            self.additionalInsurance.export(outfile, level, namespaceprefix_, namespacedef_='', name_='additionalInsurance', pretty_print=pretty_print)
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
        if nodeName_ == 'basicInsurance':
            obj_ = basicInsuranceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.basicInsurance = obj_
            obj_.original_tagname_ = 'basicInsurance'
        elif nodeName_ == 'additionalInsurance':
            obj_ = AdditionalInsuranceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.additionalInsurance = obj_
            obj_.original_tagname_ = 'additionalInsurance'
# end class InsuranceType


class AdditionalInsuranceType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.value = _cast(int, value)
        self.value_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AdditionalInsuranceType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AdditionalInsuranceType.subclass:
            return AdditionalInsuranceType.subclass(*args_, **kwargs_)
        else:
            return AdditionalInsuranceType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_value(self):
        return self.value
    def set_value(self, value):
        self.value = value
    def validate_valueType(self, value):
        # Validate type valueType, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = [1, 2, 3]
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on valueType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
    def has__content(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AdditionalInsuranceType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AdditionalInsuranceType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AdditionalInsuranceType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AdditionalInsuranceType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AdditionalInsuranceType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AdditionalInsuranceType'):
        if self.value is not None and 'value' not in already_processed:
            already_processed.add('value')
            outfile.write(' value="%s"' % self.gds_format_integer(self.value, input_name='value'))
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AdditionalInsuranceType', fromsubclass_=False, pretty_print=True):
        pass
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
        value = find_attr_value_('value', node)
        if value is not None and 'value' not in already_processed:
            already_processed.add('value')
            self.value = self.gds_parse_integer(value, node, 'value')
            self.validate_valueType(self.value)    # validate type valueType
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class AdditionalInsuranceType


class NotificationType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, language=None, emailAddress=None, mobilePhone=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.language = _cast(None, language)
        self.language_nsprefix_ = None
        self.emailAddress = emailAddress
        self.validate_EmailAddressType(self.emailAddress)
        self.emailAddress_nsprefix_ = "tns"
        self.mobilePhone = mobilePhone
        self.validate_PhoneNumberType(self.mobilePhone)
        self.mobilePhone_nsprefix_ = "tns"
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, NotificationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if NotificationType.subclass:
            return NotificationType.subclass(*args_, **kwargs_)
        else:
            return NotificationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_emailAddress(self):
        return self.emailAddress
    def set_emailAddress(self, emailAddress):
        self.emailAddress = emailAddress
    def get_mobilePhone(self):
        return self.mobilePhone
    def set_mobilePhone(self, mobilePhone):
        self.mobilePhone = mobilePhone
    def get_language(self):
        return self.language
    def set_language(self, language):
        self.language = language
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def validate_EmailAddressType(self, value):
        result = True
        # Validate type EmailAddressType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on EmailAddressType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_EmailAddressType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_EmailAddressType_patterns_, ))
                result = False
        return result
    validate_EmailAddressType_patterns_ = [["^([-!#$%&'*+/0-9=?A-Z^_a-z{|}~](\\.?[-!#$%&'*+/0-9=?A-Z^_a-z`{|}~])*@[a-zA-Z0-9](-*\\.?[a-zA-Z0-9])*\\.[a-zA-Z](-?[a-zA-Z0-9])+)$"]]
    def validate_PhoneNumberType(self, value):
        result = True
        # Validate type PhoneNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on PhoneNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on PhoneNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_PhoneNumberType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_PhoneNumberType_patterns_, ))
                result = False
        return result
    validate_PhoneNumberType_patterns_ = [['^(.*[^\\s].*)$']]
    def validate_languageType(self, value):
        # Validate type languageType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['EN', 'NL', 'FR', 'DE']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on languageType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
    def has__content(self):
        if (
            self.emailAddress is not None or
            self.mobilePhone is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NotificationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('NotificationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'NotificationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='NotificationType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='NotificationType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='NotificationType'):
        if self.language is not None and 'language' not in already_processed:
            already_processed.add('language')
            outfile.write(' language=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.language), input_name='language')), ))
        if self.extensiontype_ is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self.extensiontype_:
                imported_ns_type_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.extensiontype_, '')
                outfile.write(' xsi:type="%s%s"' % (imported_ns_type_prefix_, self.extensiontype_))
            else:
                outfile.write(' xsi:type="%s"' % self.extensiontype_)
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NotificationType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.emailAddress is not None:
            namespaceprefix_ = self.emailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.emailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%semailAddress>%s</%semailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.emailAddress), input_name='emailAddress')), namespaceprefix_ , eol_))
        if self.mobilePhone is not None:
            namespaceprefix_ = self.mobilePhone_nsprefix_ + ':' if (UseCapturedNS_ and self.mobilePhone_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smobilePhone>%s</%smobilePhone>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.mobilePhone), input_name='mobilePhone')), namespaceprefix_ , eol_))
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
        value = find_attr_value_('language', node)
        if value is not None and 'language' not in already_processed:
            already_processed.add('language')
            self.language = value
            self.validate_languageType(self.language)    # validate type languageType
        value = find_attr_value_('xsi:type', node)
        if value is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            self.extensiontype_ = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'emailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'emailAddress')
            value_ = self.gds_validate_string(value_, node, 'emailAddress')
            self.emailAddress = value_
            self.emailAddress_nsprefix_ = child_.prefix
            # validate type EmailAddressType
            self.validate_EmailAddressType(self.emailAddress)
        elif nodeName_ == 'mobilePhone':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'mobilePhone')
            value_ = self.gds_validate_string(value_, node, 'mobilePhone')
            self.mobilePhone = value_
            self.mobilePhone_nsprefix_ = child_.prefix
            # validate type PhoneNumberType
            self.validate_PhoneNumberType(self.mobilePhone)
# end class NotificationType


class TimeSlotDeliveryType(NotificationType):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = NotificationType
    def __init__(self, language=None, emailAddress=None, mobilePhone=None, value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("TimeSlotDeliveryType"), self).__init__(language, emailAddress, mobilePhone,  **kwargs_)
        self.value = _cast(None, value)
        self.value_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TimeSlotDeliveryType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TimeSlotDeliveryType.subclass:
            return TimeSlotDeliveryType.subclass(*args_, **kwargs_)
        else:
            return TimeSlotDeliveryType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_value(self):
        return self.value
    def set_value(self, value):
        self.value = value
    def validate_valueType2(self, value):
        # Validate type valueType2, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['AM', 'PM', 'PMPLUS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on valueType2' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
    def has__content(self):
        if (
            super(TimeSlotDeliveryType, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TimeSlotDeliveryType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TimeSlotDeliveryType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TimeSlotDeliveryType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TimeSlotDeliveryType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TimeSlotDeliveryType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TimeSlotDeliveryType'):
        super(TimeSlotDeliveryType, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TimeSlotDeliveryType')
        if self.value is not None and 'value' not in already_processed:
            already_processed.add('value')
            outfile.write(' value=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.value), input_name='value')), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TimeSlotDeliveryType', fromsubclass_=False, pretty_print=True):
        super(TimeSlotDeliveryType, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
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
        value = find_attr_value_('value', node)
        if value is not None and 'value' not in already_processed:
            already_processed.add('value')
            self.value = value
            self.validate_valueType2(self.value)    # validate type valueType2
        super(TimeSlotDeliveryType, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        super(TimeSlotDeliveryType, self)._buildChildren(child_, node, nodeName_, True)
        pass
# end class TimeSlotDeliveryType


class CodType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, codAmount=None, iban=None, bic=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.codAmount = codAmount
        self.validate_EuroCentAmount(self.codAmount)
        self.codAmount_nsprefix_ = "tns"
        self.iban = iban
        self.validate_IbanType(self.iban)
        self.iban_nsprefix_ = "tns"
        self.bic = bic
        self.validate_BicType(self.bic)
        self.bic_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CodType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CodType.subclass:
            return CodType.subclass(*args_, **kwargs_)
        else:
            return CodType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_codAmount(self):
        return self.codAmount
    def set_codAmount(self, codAmount):
        self.codAmount = codAmount
    def get_iban(self):
        return self.iban
    def set_iban(self, iban):
        self.iban = iban
    def get_bic(self):
        return self.bic
    def set_bic(self, bic):
        self.bic = bic
    def validate_EuroCentAmount(self, value):
        result = True
        # Validate type EuroCentAmount, a restriction on xs:int.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on EuroCentAmount' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_IbanType(self, value):
        result = True
        # Validate type IbanType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on IbanType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on IbanType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_BicType(self, value):
        result = True
        # Validate type BicType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_BicType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_BicType_patterns_, ))
                result = False
        return result
    validate_BicType_patterns_ = [['^(([A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?))$']]
    def has__content(self):
        if (
            self.codAmount is not None or
            self.iban is not None or
            self.bic is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CodType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CodType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CodType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CodType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CodType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CodType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CodType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.codAmount is not None:
            namespaceprefix_ = self.codAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.codAmount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scodAmount>%s</%scodAmount>%s' % (namespaceprefix_ , self.gds_format_integer(self.codAmount, input_name='codAmount'), namespaceprefix_ , eol_))
        if self.iban is not None:
            namespaceprefix_ = self.iban_nsprefix_ + ':' if (UseCapturedNS_ and self.iban_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%siban>%s</%siban>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.iban), input_name='iban')), namespaceprefix_ , eol_))
        if self.bic is not None:
            namespaceprefix_ = self.bic_nsprefix_ + ':' if (UseCapturedNS_ and self.bic_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sbic>%s</%sbic>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.bic), input_name='bic')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'codAmount' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'codAmount')
            ival_ = self.gds_validate_integer(ival_, node, 'codAmount')
            self.codAmount = ival_
            self.codAmount_nsprefix_ = child_.prefix
            # validate type EuroCentAmount
            self.validate_EuroCentAmount(self.codAmount)
        elif nodeName_ == 'iban':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'iban')
            value_ = self.gds_validate_string(value_, node, 'iban')
            self.iban = value_
            self.iban_nsprefix_ = child_.prefix
            # validate type IbanType
            self.validate_IbanType(self.iban)
        elif nodeName_ == 'bic':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'bic')
            value_ = self.gds_validate_string(value_, node, 'bic')
            self.bic = value_
            self.bic_nsprefix_ = child_.prefix
            # validate type BicType
            self.validate_BicType(self.bic)
# end class CodType


class SignatureType(GeneratedsSuper):
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
                CurrentSubclassModule_, SignatureType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SignatureType.subclass:
            return SignatureType.subclass(*args_, **kwargs_)
        else:
            return SignatureType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def has__content(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SignatureType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SignatureType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SignatureType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SignatureType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SignatureType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SignatureType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SignatureType', fromsubclass_=False, pretty_print=True):
        pass
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
        pass
# end class SignatureType


class SaturdayDeliveryType(GeneratedsSuper):
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
                CurrentSubclassModule_, SaturdayDeliveryType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SaturdayDeliveryType.subclass:
            return SaturdayDeliveryType.subclass(*args_, **kwargs_)
        else:
            return SaturdayDeliveryType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def has__content(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SaturdayDeliveryType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SaturdayDeliveryType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SaturdayDeliveryType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SaturdayDeliveryType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SaturdayDeliveryType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SaturdayDeliveryType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SaturdayDeliveryType', fromsubclass_=False, pretty_print=True):
        pass
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
        pass
# end class SaturdayDeliveryType


class SundayDeliveryType(GeneratedsSuper):
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
                CurrentSubclassModule_, SundayDeliveryType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SundayDeliveryType.subclass:
            return SundayDeliveryType.subclass(*args_, **kwargs_)
        else:
            return SundayDeliveryType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def has__content(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SundayDeliveryType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SundayDeliveryType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SundayDeliveryType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SundayDeliveryType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SundayDeliveryType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SundayDeliveryType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SundayDeliveryType', fromsubclass_=False, pretty_print=True):
        pass
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
        pass
# end class SundayDeliveryType


class FragileType(GeneratedsSuper):
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
                CurrentSubclassModule_, FragileType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if FragileType.subclass:
            return FragileType.subclass(*args_, **kwargs_)
        else:
            return FragileType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def has__content(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FragileType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FragileType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'FragileType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='FragileType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='FragileType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='FragileType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FragileType', fromsubclass_=False, pretty_print=True):
        pass
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
        pass
# end class FragileType


class FullServiceType(GeneratedsSuper):
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
                CurrentSubclassModule_, FullServiceType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if FullServiceType.subclass:
            return FullServiceType.subclass(*args_, **kwargs_)
        else:
            return FullServiceType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def has__content(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FullServiceType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FullServiceType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'FullServiceType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='FullServiceType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='FullServiceType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='FullServiceType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FullServiceType', fromsubclass_=False, pretty_print=True):
        pass
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
        pass
# end class FullServiceType


class DoorStepPlusServiceType(GeneratedsSuper):
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
                CurrentSubclassModule_, DoorStepPlusServiceType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DoorStepPlusServiceType.subclass:
            return DoorStepPlusServiceType.subclass(*args_, **kwargs_)
        else:
            return DoorStepPlusServiceType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def has__content(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DoorStepPlusServiceType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DoorStepPlusServiceType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DoorStepPlusServiceType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DoorStepPlusServiceType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DoorStepPlusServiceType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DoorStepPlusServiceType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DoorStepPlusServiceType', fromsubclass_=False, pretty_print=True):
        pass
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
        pass
# end class DoorStepPlusServiceType


class UltraLateInEveningDelivery(GeneratedsSuper):
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
                CurrentSubclassModule_, UltraLateInEveningDelivery)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UltraLateInEveningDelivery.subclass:
            return UltraLateInEveningDelivery.subclass(*args_, **kwargs_)
        else:
            return UltraLateInEveningDelivery(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def has__content(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UltraLateInEveningDelivery', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UltraLateInEveningDelivery')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UltraLateInEveningDelivery':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UltraLateInEveningDelivery')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UltraLateInEveningDelivery', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UltraLateInEveningDelivery'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UltraLateInEveningDelivery', fromsubclass_=False, pretty_print=True):
        pass
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
        pass
# end class UltraLateInEveningDelivery


class NationalBoxType(GeneratedsSuper):
    """NationalBoxType --  Type for a national box. This is a box send from a
    Belgian address to another Belgian address.
    atHome --  'Home or Office' delivery.
    atBpost --  'Pick-up point' delivery.
    at24-7 --  'Parcel Machine' delivery.
    bpostOnAppointment --  'bpost on appointment' delivery.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, atHome=None, atBpost=None, at24_7=None, bpostOnAppointment=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.atHome = atHome
        self.atHome_nsprefix_ = None
        self.atBpost = atBpost
        self.atBpost_nsprefix_ = None
        self.at24_7 = at24_7
        self.at24_7_nsprefix_ = None
        self.bpostOnAppointment = bpostOnAppointment
        self.bpostOnAppointment_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, NationalBoxType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if NationalBoxType.subclass:
            return NationalBoxType.subclass(*args_, **kwargs_)
        else:
            return NationalBoxType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_atHome(self):
        return self.atHome
    def set_atHome(self, atHome):
        self.atHome = atHome
    def get_atBpost(self):
        return self.atBpost
    def set_atBpost(self, atBpost):
        self.atBpost = atBpost
    def get_at24_7(self):
        return self.at24_7
    def set_at24_7(self, at24_7):
        self.at24_7 = at24_7
    def get_bpostOnAppointment(self):
        return self.bpostOnAppointment
    def set_bpostOnAppointment(self, bpostOnAppointment):
        self.bpostOnAppointment = bpostOnAppointment
    def has__content(self):
        if (
            self.atHome is not None or
            self.atBpost is not None or
            self.at24_7 is not None or
            self.bpostOnAppointment is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NationalBoxType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('NationalBoxType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'NationalBoxType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='NationalBoxType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='NationalBoxType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='NationalBoxType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NationalBoxType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.atHome is not None:
            namespaceprefix_ = self.atHome_nsprefix_ + ':' if (UseCapturedNS_ and self.atHome_nsprefix_) else ''
            self.atHome.export(outfile, level, namespaceprefix_, namespacedef_='', name_='atHome', pretty_print=pretty_print)
        if self.atBpost is not None:
            namespaceprefix_ = self.atBpost_nsprefix_ + ':' if (UseCapturedNS_ and self.atBpost_nsprefix_) else ''
            self.atBpost.export(outfile, level, namespaceprefix_, namespacedef_='', name_='atBpost', pretty_print=pretty_print)
        if self.at24_7 is not None:
            namespaceprefix_ = self.at24_7_nsprefix_ + ':' if (UseCapturedNS_ and self.at24_7_nsprefix_) else ''
            self.at24_7.export(outfile, level, namespaceprefix_, namespacedef_='', name_='at24-7', pretty_print=pretty_print)
        if self.bpostOnAppointment is not None:
            namespaceprefix_ = self.bpostOnAppointment_nsprefix_ + ':' if (UseCapturedNS_ and self.bpostOnAppointment_nsprefix_) else ''
            self.bpostOnAppointment.export(outfile, level, namespaceprefix_, namespacedef_='', name_='bpostOnAppointment', pretty_print=pretty_print)
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
        if nodeName_ == 'atHome':
            obj_ = atHome.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.atHome = obj_
            obj_.original_tagname_ = 'atHome'
        elif nodeName_ == 'atBpost':
            obj_ = atBpost.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.atBpost = obj_
            obj_.original_tagname_ = 'atBpost'
        elif nodeName_ == 'at24-7':
            obj_ = at24_7.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.at24_7 = obj_
            obj_.original_tagname_ = 'at24-7'
        elif nodeName_ == 'bpostOnAppointment':
            obj_ = bpostOnAppointment.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.bpostOnAppointment = obj_
            obj_.original_tagname_ = 'bpostOnAppointment'
# end class NationalBoxType


class NationalDeliveryMethodType(GeneratedsSuper):
    """NationalDeliveryMethodType --  Type for a national delivery method.
    product --  Element holding product information.
    options --  Element holding the options information.
    weight --  Element holding the the weight of the parcel.
    height --  Element holding the the height of the parcel.
    length --  Element holding the the length of the parcel.
    width --  Element holding the the width of the parcel.
    openingHours -- The opening hours of the receiver. Only applicable for B2B
    items.
    desiredDeliveryPlace -- The desired delivery place of the receiver. Only applicable
    for B2B items.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, product=None, options=None, weight=None, height=None, length=None, width=None, openingHours=None, desiredDeliveryPlace=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.product = product
        self.product_nsprefix_ = None
        self.options = options
        self.options_nsprefix_ = "common"
        self.weight = weight
        self.validate_WeightInGrams(self.weight)
        self.weight_nsprefix_ = "common"
        self.height = height
        self.validate_HeightInMm(self.height)
        self.height_nsprefix_ = "common"
        self.length = length
        self.validate_LegthInMm(self.length)
        self.length_nsprefix_ = "common"
        self.width = width
        self.validate_WidthInMm(self.width)
        self.width_nsprefix_ = "common"
        self.openingHours = openingHours
        self.openingHours_nsprefix_ = None
        self.desiredDeliveryPlace = desiredDeliveryPlace
        self.validate_DesiredDeliveryPlaceType(self.desiredDeliveryPlace)
        self.desiredDeliveryPlace_nsprefix_ = None
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, NationalDeliveryMethodType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if NationalDeliveryMethodType.subclass:
            return NationalDeliveryMethodType.subclass(*args_, **kwargs_)
        else:
            return NationalDeliveryMethodType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_product(self):
        return self.product
    def set_product(self, product):
        self.product = product
    def get_options(self):
        return self.options
    def set_options(self, options):
        self.options = options
    def get_weight(self):
        return self.weight
    def set_weight(self, weight):
        self.weight = weight
    def get_height(self):
        return self.height
    def set_height(self, height):
        self.height = height
    def get_length(self):
        return self.length
    def set_length(self, length):
        self.length = length
    def get_width(self):
        return self.width
    def set_width(self, width):
        self.width = width
    def get_openingHours(self):
        return self.openingHours
    def set_openingHours(self, openingHours):
        self.openingHours = openingHours
    def get_desiredDeliveryPlace(self):
        return self.desiredDeliveryPlace
    def set_desiredDeliveryPlace(self, desiredDeliveryPlace):
        self.desiredDeliveryPlace = desiredDeliveryPlace
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def validate_WeightInGrams(self, value):
        result = True
        # Validate type WeightInGrams, a restriction on xs:int.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on WeightInGrams' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_HeightInMm(self, value):
        result = True
        # Validate type HeightInMm, a restriction on xs:int.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on HeightInMm' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_LegthInMm(self, value):
        result = True
        # Validate type LegthInMm, a restriction on xs:int.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on LegthInMm' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_WidthInMm(self, value):
        result = True
        # Validate type WidthInMm, a restriction on xs:int.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on WidthInMm' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_DesiredDeliveryPlaceType(self, value):
        result = True
        # Validate type DesiredDeliveryPlaceType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on DesiredDeliveryPlaceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.product is not None or
            self.options is not None or
            self.weight is not None or
            self.height is not None or
            self.length is not None or
            self.width is not None or
            self.openingHours is not None or
            self.desiredDeliveryPlace is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NationalDeliveryMethodType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('NationalDeliveryMethodType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'NationalDeliveryMethodType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='NationalDeliveryMethodType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='NationalDeliveryMethodType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='NationalDeliveryMethodType'):
        if self.extensiontype_ is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self.extensiontype_:
                imported_ns_type_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.extensiontype_, '')
                outfile.write(' xsi:type="%s%s"' % (imported_ns_type_prefix_, self.extensiontype_))
            else:
                outfile.write(' xsi:type="%s"' % self.extensiontype_)
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NationalDeliveryMethodType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.product is not None:
            namespaceprefix_ = self.product_nsprefix_ + ':' if (UseCapturedNS_ and self.product_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sproduct>%s</%sproduct>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.product), input_name='product')), namespaceprefix_ , eol_))
        if self.options is not None:
            namespaceprefix_ = self.options_nsprefix_ + ':' if (UseCapturedNS_ and self.options_nsprefix_) else ''
            self.options.export(outfile, level, namespaceprefix_, namespacedef_='', name_='options', pretty_print=pretty_print)
        if self.weight is not None:
            namespaceprefix_ = self.weight_nsprefix_ + ':' if (UseCapturedNS_ and self.weight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sweight>%s</%sweight>%s' % (namespaceprefix_ , self.gds_format_integer(self.weight, input_name='weight'), namespaceprefix_ , eol_))
        if self.height is not None:
            namespaceprefix_ = self.height_nsprefix_ + ':' if (UseCapturedNS_ and self.height_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sheight>%s</%sheight>%s' % (namespaceprefix_ , self.gds_format_integer(self.height, input_name='height'), namespaceprefix_ , eol_))
        if self.length is not None:
            namespaceprefix_ = self.length_nsprefix_ + ':' if (UseCapturedNS_ and self.length_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slength>%s</%slength>%s' % (namespaceprefix_ , self.gds_format_integer(self.length, input_name='length'), namespaceprefix_ , eol_))
        if self.width is not None:
            namespaceprefix_ = self.width_nsprefix_ + ':' if (UseCapturedNS_ and self.width_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%swidth>%s</%swidth>%s' % (namespaceprefix_ , self.gds_format_integer(self.width, input_name='width'), namespaceprefix_ , eol_))
        if self.openingHours is not None:
            namespaceprefix_ = self.openingHours_nsprefix_ + ':' if (UseCapturedNS_ and self.openingHours_nsprefix_) else ''
            self.openingHours.export(outfile, level, namespaceprefix_, namespacedef_='', name_='openingHours', pretty_print=pretty_print)
        if self.desiredDeliveryPlace is not None:
            namespaceprefix_ = self.desiredDeliveryPlace_nsprefix_ + ':' if (UseCapturedNS_ and self.desiredDeliveryPlace_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdesiredDeliveryPlace>%s</%sdesiredDeliveryPlace>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.desiredDeliveryPlace), input_name='desiredDeliveryPlace')), namespaceprefix_ , eol_))
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
        value = find_attr_value_('xsi:type', node)
        if value is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            self.extensiontype_ = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'product':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'product')
            value_ = self.gds_validate_string(value_, node, 'product')
            self.product = value_
            self.product_nsprefix_ = child_.prefix
        elif nodeName_ == 'options':
            obj_ = OptionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.options = obj_
            obj_.original_tagname_ = 'options'
        elif nodeName_ == 'weight' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'weight')
            ival_ = self.gds_validate_integer(ival_, node, 'weight')
            self.weight = ival_
            self.weight_nsprefix_ = child_.prefix
            # validate type WeightInGrams
            self.validate_WeightInGrams(self.weight)
        elif nodeName_ == 'height' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'height')
            ival_ = self.gds_validate_integer(ival_, node, 'height')
            self.height = ival_
            self.height_nsprefix_ = child_.prefix
            # validate type HeightInMm
            self.validate_HeightInMm(self.height)
        elif nodeName_ == 'length' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'length')
            ival_ = self.gds_validate_integer(ival_, node, 'length')
            self.length = ival_
            self.length_nsprefix_ = child_.prefix
            # validate type LegthInMm
            self.validate_LegthInMm(self.length)
        elif nodeName_ == 'width' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'width')
            ival_ = self.gds_validate_integer(ival_, node, 'width')
            self.width = ival_
            self.width_nsprefix_ = child_.prefix
            # validate type WidthInMm
            self.validate_WidthInMm(self.width)
        elif nodeName_ == 'openingHours':
            obj_ = openingHoursType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.openingHours = obj_
            obj_.original_tagname_ = 'openingHours'
        elif nodeName_ == 'desiredDeliveryPlace':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'desiredDeliveryPlace')
            value_ = self.gds_validate_string(value_, node, 'desiredDeliveryPlace')
            self.desiredDeliveryPlace = value_
            self.desiredDeliveryPlace_nsprefix_ = child_.prefix
            # validate type DesiredDeliveryPlaceType
            self.validate_DesiredDeliveryPlaceType(self.desiredDeliveryPlace)
# end class NationalDeliveryMethodType


class UnregisteredParcelLockerMemberType(GeneratedsSuper):
    """language --  Element holding the language used for messaging
    (NL | FR | EN).
    mobilePhone --  Element holding the mobile phone number for
    sending messages.
    emailAddress --  Element holding the email address for sending
    messages.
    reducedMobilityZone --  Element holding info about the use of the
    reduced mobility zone. If the element is passed, reduced mobility zone will
    be set.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, language=None, mobilePhone=None, emailAddress=None, reducedMobilityZone=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.language = language
        self.validate_languageType3(self.language)
        self.language_nsprefix_ = None
        self.mobilePhone = mobilePhone
        self.validate_PhoneNumberType(self.mobilePhone)
        self.mobilePhone_nsprefix_ = "common"
        self.emailAddress = emailAddress
        self.validate_EmailAddressCharacteristicType(self.emailAddress)
        self.emailAddress_nsprefix_ = "common"
        self.reducedMobilityZone = reducedMobilityZone
        self.reducedMobilityZone_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UnregisteredParcelLockerMemberType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UnregisteredParcelLockerMemberType.subclass:
            return UnregisteredParcelLockerMemberType.subclass(*args_, **kwargs_)
        else:
            return UnregisteredParcelLockerMemberType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_language(self):
        return self.language
    def set_language(self, language):
        self.language = language
    def get_mobilePhone(self):
        return self.mobilePhone
    def set_mobilePhone(self, mobilePhone):
        self.mobilePhone = mobilePhone
    def get_emailAddress(self):
        return self.emailAddress
    def set_emailAddress(self, emailAddress):
        self.emailAddress = emailAddress
    def get_reducedMobilityZone(self):
        return self.reducedMobilityZone
    def set_reducedMobilityZone(self, reducedMobilityZone):
        self.reducedMobilityZone = reducedMobilityZone
    def validate_languageType3(self, value):
        result = True
        # Validate type languageType3, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['EN', 'NL', 'FR']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on languageType3' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PhoneNumberType(self, value):
        result = True
        # Validate type PhoneNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on PhoneNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on PhoneNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_PhoneNumberType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_PhoneNumberType_patterns_, ))
                result = False
        return result
    validate_PhoneNumberType_patterns_ = [['^(.*[^\\s].*)$']]
    def validate_EmailAddressCharacteristicType(self, value):
        result = True
        # Validate type EmailAddressCharacteristicType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on EmailAddressCharacteristicType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_EmailAddressCharacteristicType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_EmailAddressCharacteristicType_patterns_, ))
                result = False
        return result
    validate_EmailAddressCharacteristicType_patterns_ = [['^(.+@[a-zA-Z0-9-]+(\\.[a-zA-Z0-9-]+)+)$']]
    def has__content(self):
        if (
            self.language is not None or
            self.mobilePhone is not None or
            self.emailAddress is not None or
            self.reducedMobilityZone is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UnregisteredParcelLockerMemberType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UnregisteredParcelLockerMemberType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UnregisteredParcelLockerMemberType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UnregisteredParcelLockerMemberType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UnregisteredParcelLockerMemberType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UnregisteredParcelLockerMemberType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UnregisteredParcelLockerMemberType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.language is not None:
            namespaceprefix_ = self.language_nsprefix_ + ':' if (UseCapturedNS_ and self.language_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slanguage>%s</%slanguage>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.language), input_name='language')), namespaceprefix_ , eol_))
        if self.mobilePhone is not None:
            namespaceprefix_ = self.mobilePhone_nsprefix_ + ':' if (UseCapturedNS_ and self.mobilePhone_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smobilePhone>%s</%smobilePhone>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.mobilePhone), input_name='mobilePhone')), namespaceprefix_ , eol_))
        if self.emailAddress is not None:
            namespaceprefix_ = self.emailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.emailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%semailAddress>%s</%semailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.emailAddress), input_name='emailAddress')), namespaceprefix_ , eol_))
        if self.reducedMobilityZone is not None:
            namespaceprefix_ = self.reducedMobilityZone_nsprefix_ + ':' if (UseCapturedNS_ and self.reducedMobilityZone_nsprefix_) else ''
            self.reducedMobilityZone.export(outfile, level, namespaceprefix_, namespacedef_='', name_='reducedMobilityZone', pretty_print=pretty_print)
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
        if nodeName_ == 'language':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'language')
            value_ = self.gds_validate_string(value_, node, 'language')
            self.language = value_
            self.language_nsprefix_ = child_.prefix
            # validate type languageType3
            self.validate_languageType3(self.language)
        elif nodeName_ == 'mobilePhone':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'mobilePhone')
            value_ = self.gds_validate_string(value_, node, 'mobilePhone')
            self.mobilePhone = value_
            self.mobilePhone_nsprefix_ = child_.prefix
            # validate type PhoneNumberType
            self.validate_PhoneNumberType(self.mobilePhone)
        elif nodeName_ == 'emailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'emailAddress')
            value_ = self.gds_validate_string(value_, node, 'emailAddress')
            self.emailAddress = value_
            self.emailAddress_nsprefix_ = child_.prefix
            # validate type EmailAddressCharacteristicType
            self.validate_EmailAddressCharacteristicType(self.emailAddress)
        elif nodeName_ == 'reducedMobilityZone':
            obj_ = ParcelLockerReducedMobilityZoneType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.reducedMobilityZone = obj_
            obj_.original_tagname_ = 'reducedMobilityZone'
# end class UnregisteredParcelLockerMemberType


class ParcelLockerReducedMobilityZoneType(GeneratedsSuper):
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
                CurrentSubclassModule_, ParcelLockerReducedMobilityZoneType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ParcelLockerReducedMobilityZoneType.subclass:
            return ParcelLockerReducedMobilityZoneType.subclass(*args_, **kwargs_)
        else:
            return ParcelLockerReducedMobilityZoneType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def has__content(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ParcelLockerReducedMobilityZoneType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ParcelLockerReducedMobilityZoneType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ParcelLockerReducedMobilityZoneType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ParcelLockerReducedMobilityZoneType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ParcelLockerReducedMobilityZoneType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ParcelLockerReducedMobilityZoneType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ParcelLockerReducedMobilityZoneType', fromsubclass_=False, pretty_print=True):
        pass
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
        pass
# end class ParcelLockerReducedMobilityZoneType


class CustomsType(GeneratedsSuper):
    """currency -- Currency (iso code) of the value of the piece
    amtPostagePaidByAddresse -- Amount postage paid by Addresse
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, parcelValue=None, contentDescription=None, shipmentType=None, parcelReturnInstructions=None, privateAddress=None, currency=None, amtPostagePaidByAddresse=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.parcelValue = parcelValue
        self.validate_EuroCentAmount(self.parcelValue)
        self.parcelValue_nsprefix_ = "common"
        self.contentDescription = contentDescription
        self.validate_ContentDescriptionType(self.contentDescription)
        self.contentDescription_nsprefix_ = "tns"
        self.shipmentType = shipmentType
        self.validate_ShipmentType(self.shipmentType)
        self.shipmentType_nsprefix_ = "tns"
        self.parcelReturnInstructions = parcelReturnInstructions
        self.validate_ParcelReturnInstructionsType(self.parcelReturnInstructions)
        self.parcelReturnInstructions_nsprefix_ = "tns"
        self.privateAddress = privateAddress
        self.privateAddress_nsprefix_ = None
        self.currency = currency
        self.validate_currencyType(self.currency)
        self.currency_nsprefix_ = None
        self.amtPostagePaidByAddresse = amtPostagePaidByAddresse
        self.validate_amtPostagePaidByAddresseType(self.amtPostagePaidByAddresse)
        self.amtPostagePaidByAddresse_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CustomsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CustomsType.subclass:
            return CustomsType.subclass(*args_, **kwargs_)
        else:
            return CustomsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_parcelValue(self):
        return self.parcelValue
    def set_parcelValue(self, parcelValue):
        self.parcelValue = parcelValue
    def get_contentDescription(self):
        return self.contentDescription
    def set_contentDescription(self, contentDescription):
        self.contentDescription = contentDescription
    def get_shipmentType(self):
        return self.shipmentType
    def set_shipmentType(self, shipmentType):
        self.shipmentType = shipmentType
    def get_parcelReturnInstructions(self):
        return self.parcelReturnInstructions
    def set_parcelReturnInstructions(self, parcelReturnInstructions):
        self.parcelReturnInstructions = parcelReturnInstructions
    def get_privateAddress(self):
        return self.privateAddress
    def set_privateAddress(self, privateAddress):
        self.privateAddress = privateAddress
    def get_currency(self):
        return self.currency
    def set_currency(self, currency):
        self.currency = currency
    def get_amtPostagePaidByAddresse(self):
        return self.amtPostagePaidByAddresse
    def set_amtPostagePaidByAddresse(self, amtPostagePaidByAddresse):
        self.amtPostagePaidByAddresse = amtPostagePaidByAddresse
    def validate_EuroCentAmount(self, value):
        result = True
        # Validate type EuroCentAmount, a restriction on xs:int.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on EuroCentAmount' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_ContentDescriptionType(self, value):
        result = True
        # Validate type ContentDescriptionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ContentDescriptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on ContentDescriptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_ContentDescriptionType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_ContentDescriptionType_patterns_, ))
                result = False
        return result
    validate_ContentDescriptionType_patterns_ = [['^(.*[^\\s].*)$']]
    def validate_ShipmentType(self, value):
        result = True
        # Validate type ShipmentType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['SAMPLE', 'GIFT', 'GOODS', 'OTHER', 'DOCUMENTS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ShipmentType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ParcelReturnInstructionsType(self, value):
        result = True
        # Validate type ParcelReturnInstructionsType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['ABANDONED', 'RTA', 'RTS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ParcelReturnInstructionsType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_currencyType(self, value):
        result = True
        # Validate type currencyType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on currencyType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on currencyType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_amtPostagePaidByAddresseType(self, value):
        result = True
        # Validate type amtPostagePaidByAddresseType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if value > 999.99:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on amtPostagePaidByAddresseType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.parcelValue is not None or
            self.contentDescription is not None or
            self.shipmentType is not None or
            self.parcelReturnInstructions is not None or
            self.privateAddress is not None or
            self.currency is not None or
            self.amtPostagePaidByAddresse is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CustomsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CustomsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CustomsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CustomsType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CustomsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CustomsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CustomsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.parcelValue is not None:
            namespaceprefix_ = self.parcelValue_nsprefix_ + ':' if (UseCapturedNS_ and self.parcelValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sparcelValue>%s</%sparcelValue>%s' % (namespaceprefix_ , self.gds_format_integer(self.parcelValue, input_name='parcelValue'), namespaceprefix_ , eol_))
        if self.contentDescription is not None:
            namespaceprefix_ = self.contentDescription_nsprefix_ + ':' if (UseCapturedNS_ and self.contentDescription_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scontentDescription>%s</%scontentDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.contentDescription), input_name='contentDescription')), namespaceprefix_ , eol_))
        if self.shipmentType is not None:
            namespaceprefix_ = self.shipmentType_nsprefix_ + ':' if (UseCapturedNS_ and self.shipmentType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sshipmentType>%s</%sshipmentType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.shipmentType), input_name='shipmentType')), namespaceprefix_ , eol_))
        if self.parcelReturnInstructions is not None:
            namespaceprefix_ = self.parcelReturnInstructions_nsprefix_ + ':' if (UseCapturedNS_ and self.parcelReturnInstructions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sparcelReturnInstructions>%s</%sparcelReturnInstructions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.parcelReturnInstructions), input_name='parcelReturnInstructions')), namespaceprefix_ , eol_))
        if self.privateAddress is not None:
            namespaceprefix_ = self.privateAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.privateAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sprivateAddress>%s</%sprivateAddress>%s' % (namespaceprefix_ , self.gds_format_boolean(self.privateAddress, input_name='privateAddress'), namespaceprefix_ , eol_))
        if self.currency is not None:
            namespaceprefix_ = self.currency_nsprefix_ + ':' if (UseCapturedNS_ and self.currency_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scurrency>%s</%scurrency>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.currency), input_name='currency')), namespaceprefix_ , eol_))
        if self.amtPostagePaidByAddresse is not None:
            namespaceprefix_ = self.amtPostagePaidByAddresse_nsprefix_ + ':' if (UseCapturedNS_ and self.amtPostagePaidByAddresse_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%samtPostagePaidByAddresse>%s</%samtPostagePaidByAddresse>%s' % (namespaceprefix_ , self.gds_format_decimal(self.amtPostagePaidByAddresse, input_name='amtPostagePaidByAddresse'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'parcelValue' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'parcelValue')
            ival_ = self.gds_validate_integer(ival_, node, 'parcelValue')
            self.parcelValue = ival_
            self.parcelValue_nsprefix_ = child_.prefix
            # validate type EuroCentAmount
            self.validate_EuroCentAmount(self.parcelValue)
        elif nodeName_ == 'contentDescription':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'contentDescription')
            value_ = self.gds_validate_string(value_, node, 'contentDescription')
            self.contentDescription = value_
            self.contentDescription_nsprefix_ = child_.prefix
            # validate type ContentDescriptionType
            self.validate_ContentDescriptionType(self.contentDescription)
        elif nodeName_ == 'shipmentType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'shipmentType')
            value_ = self.gds_validate_string(value_, node, 'shipmentType')
            self.shipmentType = value_
            self.shipmentType_nsprefix_ = child_.prefix
            # validate type ShipmentType
            self.validate_ShipmentType(self.shipmentType)
        elif nodeName_ == 'parcelReturnInstructions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'parcelReturnInstructions')
            value_ = self.gds_validate_string(value_, node, 'parcelReturnInstructions')
            self.parcelReturnInstructions = value_
            self.parcelReturnInstructions_nsprefix_ = child_.prefix
            # validate type ParcelReturnInstructionsType
            self.validate_ParcelReturnInstructionsType(self.parcelReturnInstructions)
        elif nodeName_ == 'privateAddress':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'privateAddress')
            ival_ = self.gds_validate_boolean(ival_, node, 'privateAddress')
            self.privateAddress = ival_
            self.privateAddress_nsprefix_ = child_.prefix
        elif nodeName_ == 'currency':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'currency')
            value_ = self.gds_validate_string(value_, node, 'currency')
            self.currency = value_
            self.currency_nsprefix_ = child_.prefix
            # validate type currencyType
            self.validate_currencyType(self.currency)
        elif nodeName_ == 'amtPostagePaidByAddresse' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'amtPostagePaidByAddresse')
            fval_ = self.gds_validate_decimal(fval_, node, 'amtPostagePaidByAddresse')
            self.amtPostagePaidByAddresse = fval_
            self.amtPostagePaidByAddresse_nsprefix_ = child_.prefix
            # validate type amtPostagePaidByAddresseType
            self.validate_amtPostagePaidByAddresseType(self.amtPostagePaidByAddresse)
# end class CustomsType


class InternationalBoxType(GeneratedsSuper):
    """InternationalBoxType --  Type for an international box.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, international=None, atIntlHome=None, atIntlPugo=None, atIntlParcelDepot=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.international = international
        self.international_nsprefix_ = "tns"
        self.atIntlHome = atIntlHome
        self.atIntlHome_nsprefix_ = "tns"
        self.atIntlPugo = atIntlPugo
        self.atIntlPugo_nsprefix_ = None
        self.atIntlParcelDepot = atIntlParcelDepot
        self.atIntlParcelDepot_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, InternationalBoxType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if InternationalBoxType.subclass:
            return InternationalBoxType.subclass(*args_, **kwargs_)
        else:
            return InternationalBoxType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_international(self):
        return self.international
    def set_international(self, international):
        self.international = international
    def get_atIntlHome(self):
        return self.atIntlHome
    def set_atIntlHome(self, atIntlHome):
        self.atIntlHome = atIntlHome
    def get_atIntlPugo(self):
        return self.atIntlPugo
    def set_atIntlPugo(self, atIntlPugo):
        self.atIntlPugo = atIntlPugo
    def get_atIntlParcelDepot(self):
        return self.atIntlParcelDepot
    def set_atIntlParcelDepot(self, atIntlParcelDepot):
        self.atIntlParcelDepot = atIntlParcelDepot
    def has__content(self):
        if (
            self.international is not None or
            self.atIntlHome is not None or
            self.atIntlPugo is not None or
            self.atIntlParcelDepot is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='InternationalBoxType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('InternationalBoxType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'InternationalBoxType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='InternationalBoxType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='InternationalBoxType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='InternationalBoxType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='InternationalBoxType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.international is not None:
            namespaceprefix_ = self.international_nsprefix_ + ':' if (UseCapturedNS_ and self.international_nsprefix_) else ''
            self.international.export(outfile, level, namespaceprefix_, namespacedef_='', name_='international', pretty_print=pretty_print)
        if self.atIntlHome is not None:
            namespaceprefix_ = self.atIntlHome_nsprefix_ + ':' if (UseCapturedNS_ and self.atIntlHome_nsprefix_) else ''
            self.atIntlHome.export(outfile, level, namespaceprefix_, namespacedef_='', name_='atIntlHome', pretty_print=pretty_print)
        if self.atIntlPugo is not None:
            namespaceprefix_ = self.atIntlPugo_nsprefix_ + ':' if (UseCapturedNS_ and self.atIntlPugo_nsprefix_) else ''
            self.atIntlPugo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='atIntlPugo', pretty_print=pretty_print)
        if self.atIntlParcelDepot is not None:
            namespaceprefix_ = self.atIntlParcelDepot_nsprefix_ + ':' if (UseCapturedNS_ and self.atIntlParcelDepot_nsprefix_) else ''
            self.atIntlParcelDepot.export(outfile, level, namespaceprefix_, namespacedef_='', name_='atIntlParcelDepot', pretty_print=pretty_print)
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
        if nodeName_ == 'international':
            class_obj_ = self.get_class_obj_(child_, InternationalDeliveryMethodType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.international = obj_
            obj_.original_tagname_ = 'international'
        elif nodeName_ == 'atIntlHome':
            class_obj_ = self.get_class_obj_(child_, InternationalDeliveryMethodType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.atIntlHome = obj_
            obj_.original_tagname_ = 'atIntlHome'
        elif nodeName_ == 'atIntlPugo':
            obj_ = atIntlPugo.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.atIntlPugo = obj_
            obj_.original_tagname_ = 'atIntlPugo'
        elif nodeName_ == 'atIntlParcelDepot':
            obj_ = atIntlParcelDepot.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.atIntlParcelDepot = obj_
            obj_.original_tagname_ = 'atIntlParcelDepot'
# end class InternationalBoxType


class InternationalDeliveryMethodType(GeneratedsSuper):
    """InternationalDeliveryMethodType --  Type for an international delivery method.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, product=None, options=None, receiver=None, parcelWeight=None, parcelHeight=None, parcelLength=None, parcelWidth=None, customsInfo=None, parcelContents=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.product = product
        self.product_nsprefix_ = None
        self.options = options
        self.options_nsprefix_ = "common"
        self.receiver = receiver
        self.receiver_nsprefix_ = "common"
        self.parcelWeight = parcelWeight
        self.validate_WeightInGrams(self.parcelWeight)
        self.parcelWeight_nsprefix_ = "common"
        self.parcelHeight = parcelHeight
        self.validate_HeightInCm(self.parcelHeight)
        self.parcelHeight_nsprefix_ = "common"
        self.parcelLength = parcelLength
        self.validate_LengthInCm(self.parcelLength)
        self.parcelLength_nsprefix_ = "common"
        self.parcelWidth = parcelWidth
        self.validate_WidthInCm(self.parcelWidth)
        self.parcelWidth_nsprefix_ = "common"
        self.customsInfo = customsInfo
        self.customsInfo_nsprefix_ = "tns"
        self.parcelContents = parcelContents
        self.parcelContents_nsprefix_ = "tns"
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, InternationalDeliveryMethodType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if InternationalDeliveryMethodType.subclass:
            return InternationalDeliveryMethodType.subclass(*args_, **kwargs_)
        else:
            return InternationalDeliveryMethodType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_product(self):
        return self.product
    def set_product(self, product):
        self.product = product
    def get_options(self):
        return self.options
    def set_options(self, options):
        self.options = options
    def get_receiver(self):
        return self.receiver
    def set_receiver(self, receiver):
        self.receiver = receiver
    def get_parcelWeight(self):
        return self.parcelWeight
    def set_parcelWeight(self, parcelWeight):
        self.parcelWeight = parcelWeight
    def get_parcelHeight(self):
        return self.parcelHeight
    def set_parcelHeight(self, parcelHeight):
        self.parcelHeight = parcelHeight
    def get_parcelLength(self):
        return self.parcelLength
    def set_parcelLength(self, parcelLength):
        self.parcelLength = parcelLength
    def get_parcelWidth(self):
        return self.parcelWidth
    def set_parcelWidth(self, parcelWidth):
        self.parcelWidth = parcelWidth
    def get_customsInfo(self):
        return self.customsInfo
    def set_customsInfo(self, customsInfo):
        self.customsInfo = customsInfo
    def get_parcelContents(self):
        return self.parcelContents
    def set_parcelContents(self, parcelContents):
        self.parcelContents = parcelContents
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def validate_WeightInGrams(self, value):
        result = True
        # Validate type WeightInGrams, a restriction on xs:int.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on WeightInGrams' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_HeightInCm(self, value):
        result = True
        # Validate type HeightInCm, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on HeightInCm' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_LengthInCm(self, value):
        result = True
        # Validate type LengthInCm, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on LengthInCm' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_WidthInCm(self, value):
        result = True
        # Validate type WidthInCm, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on WidthInCm' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.product is not None or
            self.options is not None or
            self.receiver is not None or
            self.parcelWeight is not None or
            self.parcelHeight is not None or
            self.parcelLength is not None or
            self.parcelWidth is not None or
            self.customsInfo is not None or
            self.parcelContents is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='InternationalDeliveryMethodType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('InternationalDeliveryMethodType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'InternationalDeliveryMethodType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='InternationalDeliveryMethodType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='InternationalDeliveryMethodType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='InternationalDeliveryMethodType'):
        if self.extensiontype_ is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self.extensiontype_:
                imported_ns_type_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.extensiontype_, '')
                outfile.write(' xsi:type="%s%s"' % (imported_ns_type_prefix_, self.extensiontype_))
            else:
                outfile.write(' xsi:type="%s"' % self.extensiontype_)
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='InternationalDeliveryMethodType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.product is not None:
            namespaceprefix_ = self.product_nsprefix_ + ':' if (UseCapturedNS_ and self.product_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sproduct>%s</%sproduct>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.product), input_name='product')), namespaceprefix_ , eol_))
        if self.options is not None:
            namespaceprefix_ = self.options_nsprefix_ + ':' if (UseCapturedNS_ and self.options_nsprefix_) else ''
            self.options.export(outfile, level, namespaceprefix_, namespacedef_='', name_='options', pretty_print=pretty_print)
        if self.receiver is not None:
            namespaceprefix_ = self.receiver_nsprefix_ + ':' if (UseCapturedNS_ and self.receiver_nsprefix_) else ''
            self.receiver.export(outfile, level, namespaceprefix_, namespacedef_='', name_='receiver', pretty_print=pretty_print)
        if self.parcelWeight is not None:
            namespaceprefix_ = self.parcelWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.parcelWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sparcelWeight>%s</%sparcelWeight>%s' % (namespaceprefix_ , self.gds_format_integer(self.parcelWeight, input_name='parcelWeight'), namespaceprefix_ , eol_))
        if self.parcelHeight is not None:
            namespaceprefix_ = self.parcelHeight_nsprefix_ + ':' if (UseCapturedNS_ and self.parcelHeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sparcelHeight>%s</%sparcelHeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.parcelHeight, input_name='parcelHeight'), namespaceprefix_ , eol_))
        if self.parcelLength is not None:
            namespaceprefix_ = self.parcelLength_nsprefix_ + ':' if (UseCapturedNS_ and self.parcelLength_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sparcelLength>%s</%sparcelLength>%s' % (namespaceprefix_ , self.gds_format_decimal(self.parcelLength, input_name='parcelLength'), namespaceprefix_ , eol_))
        if self.parcelWidth is not None:
            namespaceprefix_ = self.parcelWidth_nsprefix_ + ':' if (UseCapturedNS_ and self.parcelWidth_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sparcelWidth>%s</%sparcelWidth>%s' % (namespaceprefix_ , self.gds_format_decimal(self.parcelWidth, input_name='parcelWidth'), namespaceprefix_ , eol_))
        if self.customsInfo is not None:
            namespaceprefix_ = self.customsInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.customsInfo_nsprefix_) else ''
            self.customsInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='customsInfo', pretty_print=pretty_print)
        if self.parcelContents is not None:
            namespaceprefix_ = self.parcelContents_nsprefix_ + ':' if (UseCapturedNS_ and self.parcelContents_nsprefix_) else ''
            self.parcelContents.export(outfile, level, namespaceprefix_, namespacedef_='', name_='parcelContents', pretty_print=pretty_print)
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
        value = find_attr_value_('xsi:type', node)
        if value is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            self.extensiontype_ = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'product':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'product')
            value_ = self.gds_validate_string(value_, node, 'product')
            self.product = value_
            self.product_nsprefix_ = child_.prefix
        elif nodeName_ == 'options':
            obj_ = OptionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.options = obj_
            obj_.original_tagname_ = 'options'
        elif nodeName_ == 'receiver':
            obj_ = Party.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.receiver = obj_
            obj_.original_tagname_ = 'receiver'
        elif nodeName_ == 'parcelWeight' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'parcelWeight')
            ival_ = self.gds_validate_integer(ival_, node, 'parcelWeight')
            self.parcelWeight = ival_
            self.parcelWeight_nsprefix_ = child_.prefix
            # validate type WeightInGrams
            self.validate_WeightInGrams(self.parcelWeight)
        elif nodeName_ == 'parcelHeight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'parcelHeight')
            fval_ = self.gds_validate_decimal(fval_, node, 'parcelHeight')
            self.parcelHeight = fval_
            self.parcelHeight_nsprefix_ = child_.prefix
            # validate type HeightInCm
            self.validate_HeightInCm(self.parcelHeight)
        elif nodeName_ == 'parcelLength' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'parcelLength')
            fval_ = self.gds_validate_decimal(fval_, node, 'parcelLength')
            self.parcelLength = fval_
            self.parcelLength_nsprefix_ = child_.prefix
            # validate type LengthInCm
            self.validate_LengthInCm(self.parcelLength)
        elif nodeName_ == 'parcelWidth' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'parcelWidth')
            fval_ = self.gds_validate_decimal(fval_, node, 'parcelWidth')
            self.parcelWidth = fval_
            self.parcelWidth_nsprefix_ = child_.prefix
            # validate type WidthInCm
            self.validate_WidthInCm(self.parcelWidth)
        elif nodeName_ == 'customsInfo':
            obj_ = CustomsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.customsInfo = obj_
            obj_.original_tagname_ = 'customsInfo'
        elif nodeName_ == 'parcelContents':
            obj_ = ParcelContentDetails.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.parcelContents = obj_
            obj_.original_tagname_ = 'parcelContents'
# end class InternationalDeliveryMethodType


class atIntlPugo(InternationalDeliveryMethodType):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = InternationalDeliveryMethodType
    def __init__(self, product=None, options=None, receiver=None, parcelWeight=None, parcelHeight=None, parcelLength=None, parcelWidth=None, customsInfo=None, parcelContents=None, pugoId=None, pugoName=None, pugoAddress=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("atIntlPugo"), self).__init__(product, options, receiver, parcelWeight, parcelHeight, parcelLength, parcelWidth, customsInfo, parcelContents,  **kwargs_)
        self.pugoId = pugoId
        self.validate_RcCode(self.pugoId)
        self.pugoId_nsprefix_ = "common"
        self.pugoName = pugoName
        self.validate_ReceiverNameType(self.pugoName)
        self.pugoName_nsprefix_ = "common"
        self.pugoAddress = pugoAddress
        self.pugoAddress_nsprefix_ = "common"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, atIntlPugo)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if atIntlPugo.subclass:
            return atIntlPugo.subclass(*args_, **kwargs_)
        else:
            return atIntlPugo(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_pugoId(self):
        return self.pugoId
    def set_pugoId(self, pugoId):
        self.pugoId = pugoId
    def get_pugoName(self):
        return self.pugoName
    def set_pugoName(self, pugoName):
        self.pugoName = pugoName
    def get_pugoAddress(self):
        return self.pugoAddress
    def set_pugoAddress(self, pugoAddress):
        self.pugoAddress = pugoAddress
    def validate_RcCode(self, value):
        result = True
        # Validate type RcCode, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_RcCode_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_RcCode_patterns_, ))
                result = False
        return result
    validate_RcCode_patterns_ = [['^([0-9A-Z_]{1,20})$']]
    def validate_ReceiverNameType(self, value):
        result = True
        # Validate type ReceiverNameType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ReceiverNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on ReceiverNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_ReceiverNameType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_ReceiverNameType_patterns_, ))
                result = False
        return result
    validate_ReceiverNameType_patterns_ = [['^(.*[^\\s].*)$']]
    def has__content(self):
        if (
            self.pugoId is not None or
            self.pugoName is not None or
            self.pugoAddress is not None or
            super(atIntlPugo, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='atIntlPugo', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('atIntlPugo')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'atIntlPugo':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='atIntlPugo')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='atIntlPugo', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='atIntlPugo'):
        super(atIntlPugo, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='atIntlPugo')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='atIntlPugo', fromsubclass_=False, pretty_print=True):
        super(atIntlPugo, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.pugoId is not None:
            namespaceprefix_ = self.pugoId_nsprefix_ + ':' if (UseCapturedNS_ and self.pugoId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spugoId>%s</%spugoId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.pugoId), input_name='pugoId')), namespaceprefix_ , eol_))
        if self.pugoName is not None:
            namespaceprefix_ = self.pugoName_nsprefix_ + ':' if (UseCapturedNS_ and self.pugoName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spugoName>%s</%spugoName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.pugoName), input_name='pugoName')), namespaceprefix_ , eol_))
        if self.pugoAddress is not None:
            namespaceprefix_ = self.pugoAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.pugoAddress_nsprefix_) else ''
            self.pugoAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='pugoAddress', pretty_print=pretty_print)
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
        super(atIntlPugo, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'pugoId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'pugoId')
            value_ = self.gds_validate_string(value_, node, 'pugoId')
            self.pugoId = value_
            self.pugoId_nsprefix_ = child_.prefix
            # validate type RcCode
            self.validate_RcCode(self.pugoId)
        elif nodeName_ == 'pugoName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'pugoName')
            value_ = self.gds_validate_string(value_, node, 'pugoName')
            self.pugoName = value_
            self.pugoName_nsprefix_ = child_.prefix
            # validate type ReceiverNameType
            self.validate_ReceiverNameType(self.pugoName)
        elif nodeName_ == 'pugoAddress':
            obj_ = AddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.pugoAddress = obj_
            obj_.original_tagname_ = 'pugoAddress'
        super(atIntlPugo, self)._buildChildren(child_, node, nodeName_, True)
# end class atIntlPugo


class atIntlParcelDepot(InternationalDeliveryMethodType):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = InternationalDeliveryMethodType
    def __init__(self, product=None, options=None, receiver=None, parcelWeight=None, parcelHeight=None, parcelLength=None, parcelWidth=None, customsInfo=None, parcelContents=None, parcelsDepotId=None, parcelsDepotName=None, parcelsDepotAddress=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("atIntlParcelDepot"), self).__init__(product, options, receiver, parcelWeight, parcelHeight, parcelLength, parcelWidth, customsInfo, parcelContents,  **kwargs_)
        self.parcelsDepotId = parcelsDepotId
        self.validate_RcCode(self.parcelsDepotId)
        self.parcelsDepotId_nsprefix_ = "common"
        self.parcelsDepotName = parcelsDepotName
        self.validate_ReceiverNameType(self.parcelsDepotName)
        self.parcelsDepotName_nsprefix_ = "common"
        self.parcelsDepotAddress = parcelsDepotAddress
        self.parcelsDepotAddress_nsprefix_ = "common"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, atIntlParcelDepot)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if atIntlParcelDepot.subclass:
            return atIntlParcelDepot.subclass(*args_, **kwargs_)
        else:
            return atIntlParcelDepot(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_parcelsDepotId(self):
        return self.parcelsDepotId
    def set_parcelsDepotId(self, parcelsDepotId):
        self.parcelsDepotId = parcelsDepotId
    def get_parcelsDepotName(self):
        return self.parcelsDepotName
    def set_parcelsDepotName(self, parcelsDepotName):
        self.parcelsDepotName = parcelsDepotName
    def get_parcelsDepotAddress(self):
        return self.parcelsDepotAddress
    def set_parcelsDepotAddress(self, parcelsDepotAddress):
        self.parcelsDepotAddress = parcelsDepotAddress
    def validate_RcCode(self, value):
        result = True
        # Validate type RcCode, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_RcCode_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_RcCode_patterns_, ))
                result = False
        return result
    validate_RcCode_patterns_ = [['^([0-9A-Z_]{1,20})$']]
    def validate_ReceiverNameType(self, value):
        result = True
        # Validate type ReceiverNameType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ReceiverNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on ReceiverNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_ReceiverNameType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_ReceiverNameType_patterns_, ))
                result = False
        return result
    validate_ReceiverNameType_patterns_ = [['^(.*[^\\s].*)$']]
    def has__content(self):
        if (
            self.parcelsDepotId is not None or
            self.parcelsDepotName is not None or
            self.parcelsDepotAddress is not None or
            super(atIntlParcelDepot, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='atIntlParcelDepot', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('atIntlParcelDepot')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'atIntlParcelDepot':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='atIntlParcelDepot')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='atIntlParcelDepot', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='atIntlParcelDepot'):
        super(atIntlParcelDepot, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='atIntlParcelDepot')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='atIntlParcelDepot', fromsubclass_=False, pretty_print=True):
        super(atIntlParcelDepot, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.parcelsDepotId is not None:
            namespaceprefix_ = self.parcelsDepotId_nsprefix_ + ':' if (UseCapturedNS_ and self.parcelsDepotId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sparcelsDepotId>%s</%sparcelsDepotId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.parcelsDepotId), input_name='parcelsDepotId')), namespaceprefix_ , eol_))
        if self.parcelsDepotName is not None:
            namespaceprefix_ = self.parcelsDepotName_nsprefix_ + ':' if (UseCapturedNS_ and self.parcelsDepotName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sparcelsDepotName>%s</%sparcelsDepotName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.parcelsDepotName), input_name='parcelsDepotName')), namespaceprefix_ , eol_))
        if self.parcelsDepotAddress is not None:
            namespaceprefix_ = self.parcelsDepotAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.parcelsDepotAddress_nsprefix_) else ''
            self.parcelsDepotAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='parcelsDepotAddress', pretty_print=pretty_print)
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
        super(atIntlParcelDepot, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'parcelsDepotId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'parcelsDepotId')
            value_ = self.gds_validate_string(value_, node, 'parcelsDepotId')
            self.parcelsDepotId = value_
            self.parcelsDepotId_nsprefix_ = child_.prefix
            # validate type RcCode
            self.validate_RcCode(self.parcelsDepotId)
        elif nodeName_ == 'parcelsDepotName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'parcelsDepotName')
            value_ = self.gds_validate_string(value_, node, 'parcelsDepotName')
            self.parcelsDepotName = value_
            self.parcelsDepotName_nsprefix_ = child_.prefix
            # validate type ReceiverNameType
            self.validate_ReceiverNameType(self.parcelsDepotName)
        elif nodeName_ == 'parcelsDepotAddress':
            obj_ = AddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.parcelsDepotAddress = obj_
            obj_.original_tagname_ = 'parcelsDepotAddress'
        super(atIntlParcelDepot, self)._buildChildren(child_, node, nodeName_, True)
# end class atIntlParcelDepot


class ParcelContentDetails(GeneratedsSuper):
    """ParcelContentDetails -- Parcel Content Detail list
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, parcelContent=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if parcelContent is None:
            self.parcelContent = []
        else:
            self.parcelContent = parcelContent
        self.parcelContent_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ParcelContentDetails)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ParcelContentDetails.subclass:
            return ParcelContentDetails.subclass(*args_, **kwargs_)
        else:
            return ParcelContentDetails(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_parcelContent(self):
        return self.parcelContent
    def set_parcelContent(self, parcelContent):
        self.parcelContent = parcelContent
    def add_parcelContent(self, value):
        self.parcelContent.append(value)
    def insert_parcelContent_at(self, index, value):
        self.parcelContent.insert(index, value)
    def replace_parcelContent_at(self, index, value):
        self.parcelContent[index] = value
    def has__content(self):
        if (
            self.parcelContent
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ParcelContentDetails', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ParcelContentDetails')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ParcelContentDetails':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ParcelContentDetails')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ParcelContentDetails', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ParcelContentDetails'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ParcelContentDetails', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for parcelContent_ in self.parcelContent:
            namespaceprefix_ = self.parcelContent_nsprefix_ + ':' if (UseCapturedNS_ and self.parcelContent_nsprefix_) else ''
            parcelContent_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='parcelContent', pretty_print=pretty_print)
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
        if nodeName_ == 'parcelContent':
            obj_ = ParcelContentDetail.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.parcelContent.append(obj_)
            obj_.original_tagname_ = 'parcelContent'
# end class ParcelContentDetails


class ParcelContentDetail(GeneratedsSuper):
    """numberOfItemType -- Number of pieces of the same type
    valueOfItem -- Value of all pieces of the same type
    itemDescription -- Description of the pieces
    nettoWeight -- The weight of all pieces of the same type
    hsTariffCode -- Harmonized System Tariff code indicating the type of goods for this
    piece. It should be a text field instead of select option
    originOfGoods -- Country of origin of the goods (iso code)
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, numberOfItemType=None, valueOfItem=None, itemDescription=None, nettoWeight=None, hsTariffCode=None, originOfGoods=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.numberOfItemType = numberOfItemType
        self.numberOfItemType_nsprefix_ = None
        self.valueOfItem = valueOfItem
        self.valueOfItem_nsprefix_ = None
        self.itemDescription = itemDescription
        self.itemDescription_nsprefix_ = None
        self.nettoWeight = nettoWeight
        self.nettoWeight_nsprefix_ = None
        self.hsTariffCode = hsTariffCode
        self.validate_hsTariffCodeType(self.hsTariffCode)
        self.hsTariffCode_nsprefix_ = None
        self.originOfGoods = originOfGoods
        self.validate_originOfGoodsType(self.originOfGoods)
        self.originOfGoods_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ParcelContentDetail)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ParcelContentDetail.subclass:
            return ParcelContentDetail.subclass(*args_, **kwargs_)
        else:
            return ParcelContentDetail(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_numberOfItemType(self):
        return self.numberOfItemType
    def set_numberOfItemType(self, numberOfItemType):
        self.numberOfItemType = numberOfItemType
    def get_valueOfItem(self):
        return self.valueOfItem
    def set_valueOfItem(self, valueOfItem):
        self.valueOfItem = valueOfItem
    def get_itemDescription(self):
        return self.itemDescription
    def set_itemDescription(self, itemDescription):
        self.itemDescription = itemDescription
    def get_nettoWeight(self):
        return self.nettoWeight
    def set_nettoWeight(self, nettoWeight):
        self.nettoWeight = nettoWeight
    def get_hsTariffCode(self):
        return self.hsTariffCode
    def set_hsTariffCode(self, hsTariffCode):
        self.hsTariffCode = hsTariffCode
    def get_originOfGoods(self):
        return self.originOfGoods
    def set_originOfGoods(self, originOfGoods):
        self.originOfGoods = originOfGoods
    def validate_hsTariffCodeType(self, value):
        result = True
        # Validate type hsTariffCodeType, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on hsTariffCodeType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 999999999:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on hsTariffCodeType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_originOfGoodsType(self, value):
        result = True
        # Validate type originOfGoodsType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on originOfGoodsType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on originOfGoodsType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.numberOfItemType is not None or
            self.valueOfItem is not None or
            self.itemDescription is not None or
            self.nettoWeight is not None or
            self.hsTariffCode is not None or
            self.originOfGoods is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ParcelContentDetail', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ParcelContentDetail')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ParcelContentDetail':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ParcelContentDetail')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ParcelContentDetail', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ParcelContentDetail'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ParcelContentDetail', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.numberOfItemType is not None:
            namespaceprefix_ = self.numberOfItemType_nsprefix_ + ':' if (UseCapturedNS_ and self.numberOfItemType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snumberOfItemType>%s</%snumberOfItemType>%s' % (namespaceprefix_ , self.gds_format_integer(self.numberOfItemType, input_name='numberOfItemType'), namespaceprefix_ , eol_))
        if self.valueOfItem is not None:
            namespaceprefix_ = self.valueOfItem_nsprefix_ + ':' if (UseCapturedNS_ and self.valueOfItem_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%svalueOfItem>%s</%svalueOfItem>%s' % (namespaceprefix_ , self.gds_format_decimal(self.valueOfItem, input_name='valueOfItem'), namespaceprefix_ , eol_))
        if self.itemDescription is not None:
            namespaceprefix_ = self.itemDescription_nsprefix_ + ':' if (UseCapturedNS_ and self.itemDescription_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sitemDescription>%s</%sitemDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.itemDescription), input_name='itemDescription')), namespaceprefix_ , eol_))
        if self.nettoWeight is not None:
            namespaceprefix_ = self.nettoWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.nettoWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snettoWeight>%s</%snettoWeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.nettoWeight, input_name='nettoWeight'), namespaceprefix_ , eol_))
        if self.hsTariffCode is not None:
            namespaceprefix_ = self.hsTariffCode_nsprefix_ + ':' if (UseCapturedNS_ and self.hsTariffCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%shsTariffCode>%s</%shsTariffCode>%s' % (namespaceprefix_ , self.gds_format_integer(self.hsTariffCode, input_name='hsTariffCode'), namespaceprefix_ , eol_))
        if self.originOfGoods is not None:
            namespaceprefix_ = self.originOfGoods_nsprefix_ + ':' if (UseCapturedNS_ and self.originOfGoods_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%soriginOfGoods>%s</%soriginOfGoods>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.originOfGoods), input_name='originOfGoods')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'numberOfItemType' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'numberOfItemType')
            ival_ = self.gds_validate_integer(ival_, node, 'numberOfItemType')
            self.numberOfItemType = ival_
            self.numberOfItemType_nsprefix_ = child_.prefix
        elif nodeName_ == 'valueOfItem' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'valueOfItem')
            fval_ = self.gds_validate_decimal(fval_, node, 'valueOfItem')
            self.valueOfItem = fval_
            self.valueOfItem_nsprefix_ = child_.prefix
        elif nodeName_ == 'itemDescription':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'itemDescription')
            value_ = self.gds_validate_string(value_, node, 'itemDescription')
            self.itemDescription = value_
            self.itemDescription_nsprefix_ = child_.prefix
        elif nodeName_ == 'nettoWeight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'nettoWeight')
            fval_ = self.gds_validate_decimal(fval_, node, 'nettoWeight')
            self.nettoWeight = fval_
            self.nettoWeight_nsprefix_ = child_.prefix
        elif nodeName_ == 'hsTariffCode' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'hsTariffCode')
            ival_ = self.gds_validate_integer(ival_, node, 'hsTariffCode')
            self.hsTariffCode = ival_
            self.hsTariffCode_nsprefix_ = child_.prefix
            # validate type hsTariffCodeType
            self.validate_hsTariffCodeType(self.hsTariffCode)
        elif nodeName_ == 'originOfGoods':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'originOfGoods')
            value_ = self.gds_validate_string(value_, node, 'originOfGoods')
            self.originOfGoods = value_
            self.originOfGoods_nsprefix_ = child_.prefix
            # validate type originOfGoodsType
            self.validate_originOfGoodsType(self.originOfGoods)
# end class ParcelContentDetail


class labelType(GeneratedsSuper):
    """labelType --  Element holding information about a label.
    barcode --  Element holding information
    about a barcode of a label.
    crossReferenceBarcode --  Element holding the cross
    reference barcodee of a label.
    barcodeWithReference --  Element holding information
    about a barcode of a label with its order reference.
    mimeType --  Element holding information about
    the mime type of a label.
    bytes --  Element holding the bytes of a
    label.
    zplCode --  Element holding the zpl code of a
    label.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, barcode=None, crossReferenceBarcode=None, barcodeWithReference=None, mimeType=None, bytes=None, zplCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if barcode is None:
            self.barcode = []
        else:
            self.barcode = barcode
        self.barcode_nsprefix_ = None
        self.crossReferenceBarcode = crossReferenceBarcode
        self.validate_CrossReferenceBarcodeType(self.crossReferenceBarcode)
        self.crossReferenceBarcode_nsprefix_ = None
        if barcodeWithReference is None:
            self.barcodeWithReference = []
        else:
            self.barcodeWithReference = barcodeWithReference
        self.barcodeWithReference_nsprefix_ = None
        self.mimeType = mimeType
        self.mimeType_nsprefix_ = None
        self.bytes = bytes
        self.bytes_nsprefix_ = None
        self.zplCode = zplCode
        self.zplCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, labelType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if labelType.subclass:
            return labelType.subclass(*args_, **kwargs_)
        else:
            return labelType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_barcode(self):
        return self.barcode
    def set_barcode(self, barcode):
        self.barcode = barcode
    def add_barcode(self, value):
        self.barcode.append(value)
    def insert_barcode_at(self, index, value):
        self.barcode.insert(index, value)
    def replace_barcode_at(self, index, value):
        self.barcode[index] = value
    def get_crossReferenceBarcode(self):
        return self.crossReferenceBarcode
    def set_crossReferenceBarcode(self, crossReferenceBarcode):
        self.crossReferenceBarcode = crossReferenceBarcode
    def get_barcodeWithReference(self):
        return self.barcodeWithReference
    def set_barcodeWithReference(self, barcodeWithReference):
        self.barcodeWithReference = barcodeWithReference
    def add_barcodeWithReference(self, value):
        self.barcodeWithReference.append(value)
    def insert_barcodeWithReference_at(self, index, value):
        self.barcodeWithReference.insert(index, value)
    def replace_barcodeWithReference_at(self, index, value):
        self.barcodeWithReference[index] = value
    def get_mimeType(self):
        return self.mimeType
    def set_mimeType(self, mimeType):
        self.mimeType = mimeType
    def get_bytes(self):
        return self.bytes
    def set_bytes(self, bytes):
        self.bytes = bytes
    def get_zplCode(self):
        return self.zplCode
    def set_zplCode(self, zplCode):
        self.zplCode = zplCode
    def validate_BarcodeType(self, value):
        result = True
        # Validate type BarcodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_CrossReferenceBarcodeType(self, value):
        result = True
        # Validate type CrossReferenceBarcodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def has__content(self):
        if (
            self.barcode or
            self.crossReferenceBarcode is not None or
            self.barcodeWithReference or
            self.mimeType is not None or
            self.bytes is not None or
            self.zplCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='labelType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('labelType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'labelType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='labelType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='labelType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='labelType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='labelType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for barcode_ in self.barcode:
            namespaceprefix_ = self.barcode_nsprefix_ + ':' if (UseCapturedNS_ and self.barcode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sbarcode>%s</%sbarcode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(barcode_), input_name='barcode')), namespaceprefix_ , eol_))
        if self.crossReferenceBarcode is not None:
            namespaceprefix_ = self.crossReferenceBarcode_nsprefix_ + ':' if (UseCapturedNS_ and self.crossReferenceBarcode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scrossReferenceBarcode>%s</%scrossReferenceBarcode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.crossReferenceBarcode), input_name='crossReferenceBarcode')), namespaceprefix_ , eol_))
        for barcodeWithReference_ in self.barcodeWithReference:
            namespaceprefix_ = self.barcodeWithReference_nsprefix_ + ':' if (UseCapturedNS_ and self.barcodeWithReference_nsprefix_) else ''
            barcodeWithReference_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='barcodeWithReference', pretty_print=pretty_print)
        if self.mimeType is not None:
            namespaceprefix_ = self.mimeType_nsprefix_ + ':' if (UseCapturedNS_ and self.mimeType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smimeType>%s</%smimeType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.mimeType), input_name='mimeType')), namespaceprefix_ , eol_))
        if self.bytes is not None:
            namespaceprefix_ = self.bytes_nsprefix_ + ':' if (UseCapturedNS_ and self.bytes_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sbytes>%s</%sbytes>%s' % (namespaceprefix_ , self.gds_format_base64(self.bytes, input_name='bytes'), namespaceprefix_ , eol_))
        if self.zplCode is not None:
            namespaceprefix_ = self.zplCode_nsprefix_ + ':' if (UseCapturedNS_ and self.zplCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%szplCode>%s</%szplCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.zplCode), input_name='zplCode')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'barcode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'barcode')
            value_ = self.gds_validate_string(value_, node, 'barcode')
            self.barcode.append(value_)
            self.barcode_nsprefix_ = child_.prefix
            # validate type BarcodeType
            self.validate_BarcodeType(self.barcode[-1])
        elif nodeName_ == 'crossReferenceBarcode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'crossReferenceBarcode')
            value_ = self.gds_validate_string(value_, node, 'crossReferenceBarcode')
            self.crossReferenceBarcode = value_
            self.crossReferenceBarcode_nsprefix_ = child_.prefix
            # validate type CrossReferenceBarcodeType
            self.validate_CrossReferenceBarcodeType(self.crossReferenceBarcode)
        elif nodeName_ == 'barcodeWithReference':
            obj_ = BarcodeWithReferenceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.barcodeWithReference.append(obj_)
            obj_.original_tagname_ = 'barcodeWithReference'
        elif nodeName_ == 'mimeType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'mimeType')
            value_ = self.gds_validate_string(value_, node, 'mimeType')
            self.mimeType = value_
            self.mimeType_nsprefix_ = child_.prefix
        elif nodeName_ == 'bytes':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'bytes')
            else:
                bval_ = None
            self.bytes = bval_
            self.bytes_nsprefix_ = child_.prefix
        elif nodeName_ == 'zplCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'zplCode')
            value_ = self.gds_validate_string(value_, node, 'zplCode')
            self.zplCode = value_
            self.zplCode_nsprefix_ = child_.prefix
# end class labelType


class deliveryMethodType(GeneratedsSuper):
    """deliveryMethodType --  Element holding the information on how a parcel
    will be delivered.
    product --  Element holding the information of
    a product.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, name=None, visiblity=None, product=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name = _cast(None, name)
        self.name_nsprefix_ = None
        self.visiblity = _cast(None, visiblity)
        self.visiblity_nsprefix_ = None
        if product is None:
            self.product = []
        else:
            self.product = product
        self.product_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, deliveryMethodType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if deliveryMethodType.subclass:
            return deliveryMethodType.subclass(*args_, **kwargs_)
        else:
            return deliveryMethodType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_product(self):
        return self.product
    def set_product(self, product):
        self.product = product
    def add_product(self, value):
        self.product.append(value)
    def insert_product_at(self, index, value):
        self.product.insert(index, value)
    def replace_product_at(self, index, value):
        self.product[index] = value
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_visiblity(self):
        return self.visiblity
    def set_visiblity(self, visiblity):
        self.visiblity = visiblity
    def has__content(self):
        if (
            self.product
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='deliveryMethodType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('deliveryMethodType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'deliveryMethodType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='deliveryMethodType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='deliveryMethodType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='deliveryMethodType'):
        if self.name is not None and 'name' not in already_processed:
            already_processed.add('name')
            outfile.write(' name=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.name), input_name='name')), ))
        if self.visiblity is not None and 'visiblity' not in already_processed:
            already_processed.add('visiblity')
            outfile.write(' visiblity=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.visiblity), input_name='visiblity')), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='deliveryMethodType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for product_ in self.product:
            namespaceprefix_ = self.product_nsprefix_ + ':' if (UseCapturedNS_ and self.product_nsprefix_) else ''
            product_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='product', pretty_print=pretty_print)
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
        value = find_attr_value_('name', node)
        if value is not None and 'name' not in already_processed:
            already_processed.add('name')
            self.name = value
        value = find_attr_value_('visiblity', node)
        if value is not None and 'visiblity' not in already_processed:
            already_processed.add('visiblity')
            self.visiblity = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'product':
            obj_ = productType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.product.append(obj_)
            obj_.original_tagname_ = 'product'
# end class deliveryMethodType


class productType(GeneratedsSuper):
    """productType --  Element holding the information of
    a product.
    price --  The price of the
    product.
    option --  Options which can be
    chosen for a certain product.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, name=None, default=None, price=None, option=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name = _cast(None, name)
        self.name_nsprefix_ = None
        self.default = _cast(bool, default)
        self.default_nsprefix_ = None
        if price is None:
            self.price = []
        else:
            self.price = price
        self.price_nsprefix_ = None
        if option is None:
            self.option = []
        else:
            self.option = option
        self.option_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, productType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if productType.subclass:
            return productType.subclass(*args_, **kwargs_)
        else:
            return productType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_price(self):
        return self.price
    def set_price(self, price):
        self.price = price
    def add_price(self, value):
        self.price.append(value)
    def insert_price_at(self, index, value):
        self.price.insert(index, value)
    def replace_price_at(self, index, value):
        self.price[index] = value
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
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_default(self):
        return self.default
    def set_default(self, default):
        self.default = default
    def has__content(self):
        if (
            self.price or
            self.option
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='productType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('productType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'productType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='productType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='productType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='productType'):
        if self.name is not None and 'name' not in already_processed:
            already_processed.add('name')
            outfile.write(' name=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.name), input_name='name')), ))
        if self.default is not None and 'default' not in already_processed:
            already_processed.add('default')
            outfile.write(' default="%s"' % self.gds_format_boolean(self.default, input_name='default'))
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='productType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for price_ in self.price:
            namespaceprefix_ = self.price_nsprefix_ + ':' if (UseCapturedNS_ and self.price_nsprefix_) else ''
            price_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='price', pretty_print=pretty_print)
        for option_ in self.option:
            namespaceprefix_ = self.option_nsprefix_ + ':' if (UseCapturedNS_ and self.option_nsprefix_) else ''
            option_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='option', pretty_print=pretty_print)
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
        value = find_attr_value_('name', node)
        if value is not None and 'name' not in already_processed:
            already_processed.add('name')
            self.name = value
        value = find_attr_value_('default', node)
        if value is not None and 'default' not in already_processed:
            already_processed.add('default')
            if value in ('true', '1'):
                self.default = True
            elif value in ('false', '0'):
                self.default = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'price':
            obj_ = priceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.price.append(obj_)
            obj_.original_tagname_ = 'price'
        elif nodeName_ == 'option':
            obj_ = optionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.option.append(obj_)
            obj_.original_tagname_ = 'option'
# end class productType


class priceType(GeneratedsSuper):
    """priceType --  The price of the
    product.
    Iso code of the
    country and their price zones.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, countryIso2Code=None, priceLessThan2=None, price2To5=None, price5To10=None, price10To20=None, price20To30=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.countryIso2Code = _cast(None, countryIso2Code)
        self.countryIso2Code_nsprefix_ = None
        self.priceLessThan2 = _cast(None, priceLessThan2)
        self.priceLessThan2_nsprefix_ = None
        self.price2To5 = _cast(None, price2To5)
        self.price2To5_nsprefix_ = None
        self.price5To10 = _cast(None, price5To10)
        self.price5To10_nsprefix_ = None
        self.price10To20 = _cast(None, price10To20)
        self.price10To20_nsprefix_ = None
        self.price20To30 = _cast(None, price20To30)
        self.price20To30_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, priceType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if priceType.subclass:
            return priceType.subclass(*args_, **kwargs_)
        else:
            return priceType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_countryIso2Code(self):
        return self.countryIso2Code
    def set_countryIso2Code(self, countryIso2Code):
        self.countryIso2Code = countryIso2Code
    def get_priceLessThan2(self):
        return self.priceLessThan2
    def set_priceLessThan2(self, priceLessThan2):
        self.priceLessThan2 = priceLessThan2
    def get_price2To5(self):
        return self.price2To5
    def set_price2To5(self, price2To5):
        self.price2To5 = price2To5
    def get_price5To10(self):
        return self.price5To10
    def set_price5To10(self, price5To10):
        self.price5To10 = price5To10
    def get_price10To20(self):
        return self.price10To20
    def set_price10To20(self, price10To20):
        self.price10To20 = price10To20
    def get_price20To30(self):
        return self.price20To30
    def set_price20To30(self, price20To30):
        self.price20To30 = price20To30
    def validate_CountryCode(self, value):
        # Validate type common:CountryCode, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_CountryCode_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_CountryCode_patterns_, ))
    validate_CountryCode_patterns_ = [['^([A-Z]{2})$']]
    def validate_EuroCentAmount(self, value):
        # Validate type common:EuroCentAmount, a restriction on xs:int.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on EuroCentAmount' % {"value": value, "lineno": lineno} )
                result = False
    def has__content(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='priceType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('priceType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'priceType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='priceType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='priceType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='priceType'):
        if self.countryIso2Code is not None and 'countryIso2Code' not in already_processed:
            already_processed.add('countryIso2Code')
            outfile.write(' countryIso2Code=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.countryIso2Code), input_name='countryIso2Code')), ))
        if self.priceLessThan2 is not None and 'priceLessThan2' not in already_processed:
            already_processed.add('priceLessThan2')
            outfile.write(' priceLessThan2="%s"' % self.gds_format_integer(self.priceLessThan2, input_name='priceLessThan2'))
        if self.price2To5 is not None and 'price2To5' not in already_processed:
            already_processed.add('price2To5')
            outfile.write(' price2To5="%s"' % self.gds_format_integer(self.price2To5, input_name='price2To5'))
        if self.price5To10 is not None and 'price5To10' not in already_processed:
            already_processed.add('price5To10')
            outfile.write(' price5To10="%s"' % self.gds_format_integer(self.price5To10, input_name='price5To10'))
        if self.price10To20 is not None and 'price10To20' not in already_processed:
            already_processed.add('price10To20')
            outfile.write(' price10To20="%s"' % self.gds_format_integer(self.price10To20, input_name='price10To20'))
        if self.price20To30 is not None and 'price20To30' not in already_processed:
            already_processed.add('price20To30')
            outfile.write(' price20To30="%s"' % self.gds_format_integer(self.price20To30, input_name='price20To30'))
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='priceType', fromsubclass_=False, pretty_print=True):
        pass
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
        value = find_attr_value_('countryIso2Code', node)
        if value is not None and 'countryIso2Code' not in already_processed:
            already_processed.add('countryIso2Code')
            self.countryIso2Code = value
            self.validate_CountryCode(self.countryIso2Code)    # validate type CountryCode
        value = find_attr_value_('priceLessThan2', node)
        if value is not None and 'priceLessThan2' not in already_processed:
            already_processed.add('priceLessThan2')
            self.priceLessThan2 = self.gds_parse_integer(value, node, 'priceLessThan2')
            self.validate_EuroCentAmount(self.priceLessThan2)    # validate type EuroCentAmount
        value = find_attr_value_('price2To5', node)
        if value is not None and 'price2To5' not in already_processed:
            already_processed.add('price2To5')
            self.price2To5 = self.gds_parse_integer(value, node, 'price2To5')
            self.validate_EuroCentAmount(self.price2To5)    # validate type EuroCentAmount
        value = find_attr_value_('price5To10', node)
        if value is not None and 'price5To10' not in already_processed:
            already_processed.add('price5To10')
            self.price5To10 = self.gds_parse_integer(value, node, 'price5To10')
            self.validate_EuroCentAmount(self.price5To10)    # validate type EuroCentAmount
        value = find_attr_value_('price10To20', node)
        if value is not None and 'price10To20' not in already_processed:
            already_processed.add('price10To20')
            self.price10To20 = self.gds_parse_integer(value, node, 'price10To20')
            self.validate_EuroCentAmount(self.price10To20)    # validate type EuroCentAmount
        value = find_attr_value_('price20To30', node)
        if value is not None and 'price20To30' not in already_processed:
            already_processed.add('price20To30')
            self.price20To30 = self.gds_parse_integer(value, node, 'price20To30')
            self.validate_EuroCentAmount(self.price20To30)    # validate type EuroCentAmount
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class priceType


class optionType(GeneratedsSuper):
    """optionType --  Options which can be
    chosen for a certain product.
    Name and the price
    of a certain option.
    characteristic --
    Characteristics defined for the option.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, name=None, price=None, visiblity=None, characteristic=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name = _cast(None, name)
        self.name_nsprefix_ = None
        self.price = _cast(None, price)
        self.price_nsprefix_ = None
        self.visiblity = _cast(None, visiblity)
        self.visiblity_nsprefix_ = None
        if characteristic is None:
            self.characteristic = []
        else:
            self.characteristic = characteristic
        self.characteristic_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, optionType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if optionType.subclass:
            return optionType.subclass(*args_, **kwargs_)
        else:
            return optionType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_characteristic(self):
        return self.characteristic
    def set_characteristic(self, characteristic):
        self.characteristic = characteristic
    def add_characteristic(self, value):
        self.characteristic.append(value)
    def insert_characteristic_at(self, index, value):
        self.characteristic.insert(index, value)
    def replace_characteristic_at(self, index, value):
        self.characteristic[index] = value
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_price(self):
        return self.price
    def set_price(self, price):
        self.price = price
    def get_visiblity(self):
        return self.visiblity
    def set_visiblity(self, visiblity):
        self.visiblity = visiblity
    def validate_EuroCentAmount(self, value):
        # Validate type common:EuroCentAmount, a restriction on xs:int.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on EuroCentAmount' % {"value": value, "lineno": lineno} )
                result = False
    def has__content(self):
        if (
            self.characteristic
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='optionType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('optionType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'optionType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='optionType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='optionType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='optionType'):
        if self.name is not None and 'name' not in already_processed:
            already_processed.add('name')
            outfile.write(' name=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.name), input_name='name')), ))
        if self.price is not None and 'price' not in already_processed:
            already_processed.add('price')
            outfile.write(' price="%s"' % self.gds_format_integer(self.price, input_name='price'))
        if self.visiblity is not None and 'visiblity' not in already_processed:
            already_processed.add('visiblity')
            outfile.write(' visiblity=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.visiblity), input_name='visiblity')), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='optionType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for characteristic_ in self.characteristic:
            namespaceprefix_ = self.characteristic_nsprefix_ + ':' if (UseCapturedNS_ and self.characteristic_nsprefix_) else ''
            characteristic_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='characteristic', pretty_print=pretty_print)
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
        value = find_attr_value_('name', node)
        if value is not None and 'name' not in already_processed:
            already_processed.add('name')
            self.name = value
        value = find_attr_value_('price', node)
        if value is not None and 'price' not in already_processed:
            already_processed.add('price')
            self.price = self.gds_parse_integer(value, node, 'price')
            self.validate_EuroCentAmount(self.price)    # validate type EuroCentAmount
        value = find_attr_value_('visiblity', node)
        if value is not None and 'visiblity' not in already_processed:
            already_processed.add('visiblity')
            self.visiblity = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'characteristic':
            obj_ = characteristicType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.characteristic.append(obj_)
            obj_.original_tagname_ = 'characteristic'
# end class optionType


class characteristicType(GeneratedsSuper):
    """characteristicType --
    Characteristics defined for the option.
    Name
    and the value of a certain
    characteristic.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, name=None, value=None, displayValue=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name = _cast(None, name)
        self.name_nsprefix_ = None
        self.value = _cast(None, value)
        self.value_nsprefix_ = None
        self.displayValue = _cast(None, displayValue)
        self.displayValue_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, characteristicType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if characteristicType.subclass:
            return characteristicType.subclass(*args_, **kwargs_)
        else:
            return characteristicType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_value(self):
        return self.value
    def set_value(self, value):
        self.value = value
    def get_displayValue(self):
        return self.displayValue
    def set_displayValue(self, displayValue):
        self.displayValue = displayValue
    def has__content(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='characteristicType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('characteristicType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'characteristicType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='characteristicType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='characteristicType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='characteristicType'):
        if self.name is not None and 'name' not in already_processed:
            already_processed.add('name')
            outfile.write(' name=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.name), input_name='name')), ))
        if self.value is not None and 'value' not in already_processed:
            already_processed.add('value')
            outfile.write(' value=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.value), input_name='value')), ))
        if self.displayValue is not None and 'displayValue' not in already_processed:
            already_processed.add('displayValue')
            outfile.write(' displayValue=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.displayValue), input_name='displayValue')), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='characteristicType', fromsubclass_=False, pretty_print=True):
        pass
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
        value = find_attr_value_('name', node)
        if value is not None and 'name' not in already_processed:
            already_processed.add('name')
            self.name = value
        value = find_attr_value_('value', node)
        if value is not None and 'value' not in already_processed:
            already_processed.add('value')
            self.value = value
        value = find_attr_value_('displayValue', node)
        if value is not None and 'displayValue' not in already_processed:
            already_processed.add('displayValue')
            self.displayValue = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class characteristicType


class automaticSecondPresentationType(GeneratedsSuper):
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
                CurrentSubclassModule_, automaticSecondPresentationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if automaticSecondPresentationType.subclass:
            return automaticSecondPresentationType.subclass(*args_, **kwargs_)
        else:
            return automaticSecondPresentationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def has__content(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='automaticSecondPresentationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('automaticSecondPresentationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'automaticSecondPresentationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='automaticSecondPresentationType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='automaticSecondPresentationType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='automaticSecondPresentationType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='automaticSecondPresentationType', fromsubclass_=False, pretty_print=True):
        pass
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
        pass
# end class automaticSecondPresentationType


class basicInsuranceType(GeneratedsSuper):
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
                CurrentSubclassModule_, basicInsuranceType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if basicInsuranceType.subclass:
            return basicInsuranceType.subclass(*args_, **kwargs_)
        else:
            return basicInsuranceType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def has__content(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='basicInsuranceType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('basicInsuranceType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'basicInsuranceType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='basicInsuranceType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='basicInsuranceType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='basicInsuranceType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='basicInsuranceType', fromsubclass_=False, pretty_print=True):
        pass
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
        pass
# end class basicInsuranceType


class openingHoursType(GeneratedsSuper):
    """openingHoursType -- The opening hours of the receiver. Only applicable for B2B
    items.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Monday=None, Tuesday=None, Wednesday=None, Thursday=None, Friday=None, Saturday=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Monday = Monday
        self.validate_OpeningHoursType(self.Monday)
        self.Monday_nsprefix_ = None
        self.Tuesday = Tuesday
        self.validate_OpeningHoursType(self.Tuesday)
        self.Tuesday_nsprefix_ = None
        self.Wednesday = Wednesday
        self.validate_OpeningHoursType(self.Wednesday)
        self.Wednesday_nsprefix_ = None
        self.Thursday = Thursday
        self.validate_OpeningHoursType(self.Thursday)
        self.Thursday_nsprefix_ = None
        self.Friday = Friday
        self.validate_OpeningHoursType(self.Friday)
        self.Friday_nsprefix_ = None
        self.Saturday = Saturday
        self.validate_OpeningHoursType(self.Saturday)
        self.Saturday_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, openingHoursType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if openingHoursType.subclass:
            return openingHoursType.subclass(*args_, **kwargs_)
        else:
            return openingHoursType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Monday(self):
        return self.Monday
    def set_Monday(self, Monday):
        self.Monday = Monday
    def get_Tuesday(self):
        return self.Tuesday
    def set_Tuesday(self, Tuesday):
        self.Tuesday = Tuesday
    def get_Wednesday(self):
        return self.Wednesday
    def set_Wednesday(self, Wednesday):
        self.Wednesday = Wednesday
    def get_Thursday(self):
        return self.Thursday
    def set_Thursday(self, Thursday):
        self.Thursday = Thursday
    def get_Friday(self):
        return self.Friday
    def set_Friday(self, Friday):
        self.Friday = Friday
    def get_Saturday(self):
        return self.Saturday
    def set_Saturday(self, Saturday):
        self.Saturday = Saturday
    def validate_OpeningHoursType(self, value):
        result = True
        # Validate type OpeningHoursType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 23:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on OpeningHoursType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.Monday is not None or
            self.Tuesday is not None or
            self.Wednesday is not None or
            self.Thursday is not None or
            self.Friday is not None or
            self.Saturday is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='openingHoursType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('openingHoursType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'openingHoursType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='openingHoursType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='openingHoursType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='openingHoursType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='openingHoursType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Monday is not None:
            namespaceprefix_ = self.Monday_nsprefix_ + ':' if (UseCapturedNS_ and self.Monday_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMonday>%s</%sMonday>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Monday), input_name='Monday')), namespaceprefix_ , eol_))
        if self.Tuesday is not None:
            namespaceprefix_ = self.Tuesday_nsprefix_ + ':' if (UseCapturedNS_ and self.Tuesday_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTuesday>%s</%sTuesday>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Tuesday), input_name='Tuesday')), namespaceprefix_ , eol_))
        if self.Wednesday is not None:
            namespaceprefix_ = self.Wednesday_nsprefix_ + ':' if (UseCapturedNS_ and self.Wednesday_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWednesday>%s</%sWednesday>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Wednesday), input_name='Wednesday')), namespaceprefix_ , eol_))
        if self.Thursday is not None:
            namespaceprefix_ = self.Thursday_nsprefix_ + ':' if (UseCapturedNS_ and self.Thursday_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sThursday>%s</%sThursday>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Thursday), input_name='Thursday')), namespaceprefix_ , eol_))
        if self.Friday is not None:
            namespaceprefix_ = self.Friday_nsprefix_ + ':' if (UseCapturedNS_ and self.Friday_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFriday>%s</%sFriday>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Friday), input_name='Friday')), namespaceprefix_ , eol_))
        if self.Saturday is not None:
            namespaceprefix_ = self.Saturday_nsprefix_ + ':' if (UseCapturedNS_ and self.Saturday_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSaturday>%s</%sSaturday>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Saturday), input_name='Saturday')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Monday':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Monday')
            value_ = self.gds_validate_string(value_, node, 'Monday')
            self.Monday = value_
            self.Monday_nsprefix_ = child_.prefix
            # validate type OpeningHoursType
            self.validate_OpeningHoursType(self.Monday)
        elif nodeName_ == 'Tuesday':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Tuesday')
            value_ = self.gds_validate_string(value_, node, 'Tuesday')
            self.Tuesday = value_
            self.Tuesday_nsprefix_ = child_.prefix
            # validate type OpeningHoursType
            self.validate_OpeningHoursType(self.Tuesday)
        elif nodeName_ == 'Wednesday':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Wednesday')
            value_ = self.gds_validate_string(value_, node, 'Wednesday')
            self.Wednesday = value_
            self.Wednesday_nsprefix_ = child_.prefix
            # validate type OpeningHoursType
            self.validate_OpeningHoursType(self.Wednesday)
        elif nodeName_ == 'Thursday':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Thursday')
            value_ = self.gds_validate_string(value_, node, 'Thursday')
            self.Thursday = value_
            self.Thursday_nsprefix_ = child_.prefix
            # validate type OpeningHoursType
            self.validate_OpeningHoursType(self.Thursday)
        elif nodeName_ == 'Friday':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Friday')
            value_ = self.gds_validate_string(value_, node, 'Friday')
            self.Friday = value_
            self.Friday_nsprefix_ = child_.prefix
            # validate type OpeningHoursType
            self.validate_OpeningHoursType(self.Friday)
        elif nodeName_ == 'Saturday':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Saturday')
            value_ = self.gds_validate_string(value_, node, 'Saturday')
            self.Saturday = value_
            self.Saturday_nsprefix_ = child_.prefix
            # validate type OpeningHoursType
            self.validate_OpeningHoursType(self.Saturday)
# end class openingHoursType


class bpostOnAppointment(NationalDeliveryMethodType):
    """bpostOnAppointment --  'bpost on appointment' delivery.
    receiver --  Element holding information about
    the receiver of the parcel.
    inNetworkCutOff --  Latest time at which the parcel
    should be ready to enter the bpost network.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = NationalDeliveryMethodType
    def __init__(self, product=None, options=None, weight=None, height=None, length=None, width=None, openingHours=None, desiredDeliveryPlace=None, receiver=None, inNetworkCutOff=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("bpostOnAppointment"), self).__init__(product, options, weight, height, length, width, openingHours, desiredDeliveryPlace,  **kwargs_)
        self.receiver = receiver
        self.receiver_nsprefix_ = "common"
        if isinstance(inNetworkCutOff, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(inNetworkCutOff, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = inNetworkCutOff
        self.inNetworkCutOff = initvalue_
        self.inNetworkCutOff_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, bpostOnAppointment)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if bpostOnAppointment.subclass:
            return bpostOnAppointment.subclass(*args_, **kwargs_)
        else:
            return bpostOnAppointment(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_receiver(self):
        return self.receiver
    def set_receiver(self, receiver):
        self.receiver = receiver
    def get_inNetworkCutOff(self):
        return self.inNetworkCutOff
    def set_inNetworkCutOff(self, inNetworkCutOff):
        self.inNetworkCutOff = inNetworkCutOff
    def has__content(self):
        if (
            self.receiver is not None or
            self.inNetworkCutOff is not None or
            super(bpostOnAppointment, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='bpostOnAppointment', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('bpostOnAppointment')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'bpostOnAppointment':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='bpostOnAppointment')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='bpostOnAppointment', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='bpostOnAppointment'):
        super(bpostOnAppointment, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='bpostOnAppointment')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='bpostOnAppointment', fromsubclass_=False, pretty_print=True):
        super(bpostOnAppointment, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.receiver is not None:
            namespaceprefix_ = self.receiver_nsprefix_ + ':' if (UseCapturedNS_ and self.receiver_nsprefix_) else ''
            self.receiver.export(outfile, level, namespaceprefix_, namespacedef_='', name_='receiver', pretty_print=pretty_print)
        if self.inNetworkCutOff is not None:
            namespaceprefix_ = self.inNetworkCutOff_nsprefix_ + ':' if (UseCapturedNS_ and self.inNetworkCutOff_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sinNetworkCutOff>%s</%sinNetworkCutOff>%s' % (namespaceprefix_ , self.gds_format_datetime(self.inNetworkCutOff, input_name='inNetworkCutOff'), namespaceprefix_ , eol_))
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
        super(bpostOnAppointment, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'receiver':
            obj_ = Party.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.receiver = obj_
            obj_.original_tagname_ = 'receiver'
        elif nodeName_ == 'inNetworkCutOff':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.inNetworkCutOff = dval_
            self.inNetworkCutOff_nsprefix_ = child_.prefix
        super(bpostOnAppointment, self)._buildChildren(child_, node, nodeName_, True)
# end class bpostOnAppointment


class at24_7(NationalDeliveryMethodType):
    """at24-7 --  'Parcel Machine' delivery.
    parcelsDepotId --  Element holding the unique
    identifier of the parcel machine.
    parcelsDepotName --  Element holding the name of the
    parcel machine.
    parcelsDepotAddress --  Element holding the address of the
    parcel machine.
    memberId --  Element holding the member id
    of the receiver of the parcel.
    unregistered --  Element holding the member id
    of the receiver of the parcel.
    receiverName --  Element holding the name of the
    receiver of the parcel.
    receiverCompany --  Element holding the name of the
    company of the receiver of the parcel.
    requestedDeliveryDate -- See type definition.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = NationalDeliveryMethodType
    def __init__(self, product=None, options=None, weight=None, height=None, length=None, width=None, openingHours=None, desiredDeliveryPlace=None, parcelsDepotId=None, parcelsDepotName=None, parcelsDepotAddress=None, memberId=None, unregistered=None, receiverName=None, receiverCompany=None, requestedDeliveryDate=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("at24_7"), self).__init__(product, options, weight, height, length, width, openingHours, desiredDeliveryPlace,  **kwargs_)
        self.parcelsDepotId = parcelsDepotId
        self.validate_RcCode(self.parcelsDepotId)
        self.parcelsDepotId_nsprefix_ = "common"
        self.parcelsDepotName = parcelsDepotName
        self.validate_ReceiverNameType(self.parcelsDepotName)
        self.parcelsDepotName_nsprefix_ = "common"
        self.parcelsDepotAddress = parcelsDepotAddress
        self.parcelsDepotAddress_nsprefix_ = "common"
        self.memberId = memberId
        self.validate_BpackMemberId(self.memberId)
        self.memberId_nsprefix_ = "common"
        self.unregistered = unregistered
        self.unregistered_nsprefix_ = None
        self.receiverName = receiverName
        self.validate_ReceiverNameType(self.receiverName)
        self.receiverName_nsprefix_ = "common"
        self.receiverCompany = receiverCompany
        self.validate_ReceiverCompany(self.receiverCompany)
        self.receiverCompany_nsprefix_ = "common"
        if isinstance(requestedDeliveryDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(requestedDeliveryDate, '%Y-%m-%d').date()
        else:
            initvalue_ = requestedDeliveryDate
        self.requestedDeliveryDate = initvalue_
        self.requestedDeliveryDate_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, at24_7)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if at24_7.subclass:
            return at24_7.subclass(*args_, **kwargs_)
        else:
            return at24_7(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_parcelsDepotId(self):
        return self.parcelsDepotId
    def set_parcelsDepotId(self, parcelsDepotId):
        self.parcelsDepotId = parcelsDepotId
    def get_parcelsDepotName(self):
        return self.parcelsDepotName
    def set_parcelsDepotName(self, parcelsDepotName):
        self.parcelsDepotName = parcelsDepotName
    def get_parcelsDepotAddress(self):
        return self.parcelsDepotAddress
    def set_parcelsDepotAddress(self, parcelsDepotAddress):
        self.parcelsDepotAddress = parcelsDepotAddress
    def get_memberId(self):
        return self.memberId
    def set_memberId(self, memberId):
        self.memberId = memberId
    def get_unregistered(self):
        return self.unregistered
    def set_unregistered(self, unregistered):
        self.unregistered = unregistered
    def get_receiverName(self):
        return self.receiverName
    def set_receiverName(self, receiverName):
        self.receiverName = receiverName
    def get_receiverCompany(self):
        return self.receiverCompany
    def set_receiverCompany(self, receiverCompany):
        self.receiverCompany = receiverCompany
    def get_requestedDeliveryDate(self):
        return self.requestedDeliveryDate
    def set_requestedDeliveryDate(self, requestedDeliveryDate):
        self.requestedDeliveryDate = requestedDeliveryDate
    def validate_RcCode(self, value):
        result = True
        # Validate type RcCode, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_RcCode_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_RcCode_patterns_, ))
                result = False
        return result
    validate_RcCode_patterns_ = [['^([0-9A-Z_]{1,20})$']]
    def validate_ReceiverNameType(self, value):
        result = True
        # Validate type ReceiverNameType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ReceiverNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on ReceiverNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_ReceiverNameType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_ReceiverNameType_patterns_, ))
                result = False
        return result
    validate_ReceiverNameType_patterns_ = [['^(.*[^\\s].*)$']]
    def validate_BpackMemberId(self, value):
        result = True
        # Validate type BpackMemberId, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_BpackMemberId_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_BpackMemberId_patterns_, ))
                result = False
        return result
    validate_BpackMemberId_patterns_ = [['^([0-9]{9})$']]
    def validate_ReceiverCompany(self, value):
        result = True
        # Validate type ReceiverCompany, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ReceiverCompany' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_RequestedDeliveryDateType(self, value):
        result = True
        # Validate type RequestedDeliveryDateType, a restriction on xs:date.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.date):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.date)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def has__content(self):
        if (
            self.parcelsDepotId is not None or
            self.parcelsDepotName is not None or
            self.parcelsDepotAddress is not None or
            self.memberId is not None or
            self.unregistered is not None or
            self.receiverName is not None or
            self.receiverCompany is not None or
            self.requestedDeliveryDate is not None or
            super(at24_7, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='at24-7', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('at24-7')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'at24-7':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='at24-7')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='at24-7', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='at24-7'):
        super(at24_7, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='at24-7')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='at24-7', fromsubclass_=False, pretty_print=True):
        super(at24_7, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.parcelsDepotId is not None:
            namespaceprefix_ = self.parcelsDepotId_nsprefix_ + ':' if (UseCapturedNS_ and self.parcelsDepotId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sparcelsDepotId>%s</%sparcelsDepotId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.parcelsDepotId), input_name='parcelsDepotId')), namespaceprefix_ , eol_))
        if self.parcelsDepotName is not None:
            namespaceprefix_ = self.parcelsDepotName_nsprefix_ + ':' if (UseCapturedNS_ and self.parcelsDepotName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sparcelsDepotName>%s</%sparcelsDepotName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.parcelsDepotName), input_name='parcelsDepotName')), namespaceprefix_ , eol_))
        if self.parcelsDepotAddress is not None:
            namespaceprefix_ = self.parcelsDepotAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.parcelsDepotAddress_nsprefix_) else ''
            self.parcelsDepotAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='parcelsDepotAddress', pretty_print=pretty_print)
        if self.memberId is not None:
            namespaceprefix_ = self.memberId_nsprefix_ + ':' if (UseCapturedNS_ and self.memberId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smemberId>%s</%smemberId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.memberId), input_name='memberId')), namespaceprefix_ , eol_))
        if self.unregistered is not None:
            namespaceprefix_ = self.unregistered_nsprefix_ + ':' if (UseCapturedNS_ and self.unregistered_nsprefix_) else ''
            self.unregistered.export(outfile, level, namespaceprefix_, namespacedef_='', name_='unregistered', pretty_print=pretty_print)
        if self.receiverName is not None:
            namespaceprefix_ = self.receiverName_nsprefix_ + ':' if (UseCapturedNS_ and self.receiverName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sreceiverName>%s</%sreceiverName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.receiverName), input_name='receiverName')), namespaceprefix_ , eol_))
        if self.receiverCompany is not None:
            namespaceprefix_ = self.receiverCompany_nsprefix_ + ':' if (UseCapturedNS_ and self.receiverCompany_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sreceiverCompany>%s</%sreceiverCompany>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.receiverCompany), input_name='receiverCompany')), namespaceprefix_ , eol_))
        if self.requestedDeliveryDate is not None:
            namespaceprefix_ = self.requestedDeliveryDate_nsprefix_ + ':' if (UseCapturedNS_ and self.requestedDeliveryDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%srequestedDeliveryDate>%s</%srequestedDeliveryDate>%s' % (namespaceprefix_ , self.gds_format_date(self.requestedDeliveryDate, input_name='requestedDeliveryDate'), namespaceprefix_ , eol_))
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
        super(at24_7, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'parcelsDepotId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'parcelsDepotId')
            value_ = self.gds_validate_string(value_, node, 'parcelsDepotId')
            self.parcelsDepotId = value_
            self.parcelsDepotId_nsprefix_ = child_.prefix
            # validate type RcCode
            self.validate_RcCode(self.parcelsDepotId)
        elif nodeName_ == 'parcelsDepotName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'parcelsDepotName')
            value_ = self.gds_validate_string(value_, node, 'parcelsDepotName')
            self.parcelsDepotName = value_
            self.parcelsDepotName_nsprefix_ = child_.prefix
            # validate type ReceiverNameType
            self.validate_ReceiverNameType(self.parcelsDepotName)
        elif nodeName_ == 'parcelsDepotAddress':
            obj_ = AddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.parcelsDepotAddress = obj_
            obj_.original_tagname_ = 'parcelsDepotAddress'
        elif nodeName_ == 'memberId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'memberId')
            value_ = self.gds_validate_string(value_, node, 'memberId')
            self.memberId = value_
            self.memberId_nsprefix_ = child_.prefix
            # validate type BpackMemberId
            self.validate_BpackMemberId(self.memberId)
        elif nodeName_ == 'unregistered':
            obj_ = UnregisteredParcelLockerMemberType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.unregistered = obj_
            obj_.original_tagname_ = 'unregistered'
        elif nodeName_ == 'receiverName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'receiverName')
            value_ = self.gds_validate_string(value_, node, 'receiverName')
            self.receiverName = value_
            self.receiverName_nsprefix_ = child_.prefix
            # validate type ReceiverNameType
            self.validate_ReceiverNameType(self.receiverName)
        elif nodeName_ == 'receiverCompany':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'receiverCompany')
            value_ = self.gds_validate_string(value_, node, 'receiverCompany')
            self.receiverCompany = value_
            self.receiverCompany_nsprefix_ = child_.prefix
            # validate type ReceiverCompany
            self.validate_ReceiverCompany(self.receiverCompany)
        elif nodeName_ == 'requestedDeliveryDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.requestedDeliveryDate = dval_
            self.requestedDeliveryDate_nsprefix_ = child_.prefix
            # validate type RequestedDeliveryDateType
            self.validate_RequestedDeliveryDateType(self.requestedDeliveryDate)
        super(at24_7, self)._buildChildren(child_, node, nodeName_, True)
# end class at24_7


class atBpost(NationalDeliveryMethodType):
    """atBpost --  'Pick-up point' delivery.
    pugoId --  Element holding the unique
    identifier of the pick-up point.
    pugoName --  Element holding the name of the
    pick-up point.
    pugoAddress --  Element holding the address of
    the pick-up point.
    receiverName --  Element holding the name of the
    receiver of the parcel.
    receiverCompany --  Element holding the company
    name of the receiver of the parcel.
    requestedDeliveryDate -- See type definition.
    shopHandlingInstruction -- See type definition.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = NationalDeliveryMethodType
    def __init__(self, product=None, options=None, weight=None, height=None, length=None, width=None, openingHours=None, desiredDeliveryPlace=None, pugoId=None, pugoName=None, pugoAddress=None, receiverName=None, receiverCompany=None, requestedDeliveryDate=None, shopHandlingInstruction=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("atBpost"), self).__init__(product, options, weight, height, length, width, openingHours, desiredDeliveryPlace,  **kwargs_)
        self.pugoId = pugoId
        self.validate_RcCode(self.pugoId)
        self.pugoId_nsprefix_ = "common"
        self.pugoName = pugoName
        self.validate_ReceiverNameType(self.pugoName)
        self.pugoName_nsprefix_ = "common"
        self.pugoAddress = pugoAddress
        self.pugoAddress_nsprefix_ = "common"
        self.receiverName = receiverName
        self.validate_ReceiverNameType(self.receiverName)
        self.receiverName_nsprefix_ = "common"
        self.receiverCompany = receiverCompany
        self.validate_ReceiverCompany(self.receiverCompany)
        self.receiverCompany_nsprefix_ = "common"
        if isinstance(requestedDeliveryDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(requestedDeliveryDate, '%Y-%m-%d').date()
        else:
            initvalue_ = requestedDeliveryDate
        self.requestedDeliveryDate = initvalue_
        self.requestedDeliveryDate_nsprefix_ = None
        self.shopHandlingInstruction = shopHandlingInstruction
        self.validate_ShopHandlingInstructionType(self.shopHandlingInstruction)
        self.shopHandlingInstruction_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, atBpost)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if atBpost.subclass:
            return atBpost.subclass(*args_, **kwargs_)
        else:
            return atBpost(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_pugoId(self):
        return self.pugoId
    def set_pugoId(self, pugoId):
        self.pugoId = pugoId
    def get_pugoName(self):
        return self.pugoName
    def set_pugoName(self, pugoName):
        self.pugoName = pugoName
    def get_pugoAddress(self):
        return self.pugoAddress
    def set_pugoAddress(self, pugoAddress):
        self.pugoAddress = pugoAddress
    def get_receiverName(self):
        return self.receiverName
    def set_receiverName(self, receiverName):
        self.receiverName = receiverName
    def get_receiverCompany(self):
        return self.receiverCompany
    def set_receiverCompany(self, receiverCompany):
        self.receiverCompany = receiverCompany
    def get_requestedDeliveryDate(self):
        return self.requestedDeliveryDate
    def set_requestedDeliveryDate(self, requestedDeliveryDate):
        self.requestedDeliveryDate = requestedDeliveryDate
    def get_shopHandlingInstruction(self):
        return self.shopHandlingInstruction
    def set_shopHandlingInstruction(self, shopHandlingInstruction):
        self.shopHandlingInstruction = shopHandlingInstruction
    def validate_RcCode(self, value):
        result = True
        # Validate type RcCode, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_RcCode_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_RcCode_patterns_, ))
                result = False
        return result
    validate_RcCode_patterns_ = [['^([0-9A-Z_]{1,20})$']]
    def validate_ReceiverNameType(self, value):
        result = True
        # Validate type ReceiverNameType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ReceiverNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on ReceiverNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_ReceiverNameType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_ReceiverNameType_patterns_, ))
                result = False
        return result
    validate_ReceiverNameType_patterns_ = [['^(.*[^\\s].*)$']]
    def validate_ReceiverCompany(self, value):
        result = True
        # Validate type ReceiverCompany, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ReceiverCompany' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_RequestedDeliveryDateType(self, value):
        result = True
        # Validate type RequestedDeliveryDateType, a restriction on xs:date.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.date):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.date)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_ShopHandlingInstructionType(self, value):
        result = True
        # Validate type ShopHandlingInstructionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ShopHandlingInstructionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.pugoId is not None or
            self.pugoName is not None or
            self.pugoAddress is not None or
            self.receiverName is not None or
            self.receiverCompany is not None or
            self.requestedDeliveryDate is not None or
            self.shopHandlingInstruction is not None or
            super(atBpost, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='atBpost', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('atBpost')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'atBpost':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='atBpost')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='atBpost', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='atBpost'):
        super(atBpost, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='atBpost')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='atBpost', fromsubclass_=False, pretty_print=True):
        super(atBpost, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.pugoId is not None:
            namespaceprefix_ = self.pugoId_nsprefix_ + ':' if (UseCapturedNS_ and self.pugoId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spugoId>%s</%spugoId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.pugoId), input_name='pugoId')), namespaceprefix_ , eol_))
        if self.pugoName is not None:
            namespaceprefix_ = self.pugoName_nsprefix_ + ':' if (UseCapturedNS_ and self.pugoName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spugoName>%s</%spugoName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.pugoName), input_name='pugoName')), namespaceprefix_ , eol_))
        if self.pugoAddress is not None:
            namespaceprefix_ = self.pugoAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.pugoAddress_nsprefix_) else ''
            self.pugoAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='pugoAddress', pretty_print=pretty_print)
        if self.receiverName is not None:
            namespaceprefix_ = self.receiverName_nsprefix_ + ':' if (UseCapturedNS_ and self.receiverName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sreceiverName>%s</%sreceiverName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.receiverName), input_name='receiverName')), namespaceprefix_ , eol_))
        if self.receiverCompany is not None:
            namespaceprefix_ = self.receiverCompany_nsprefix_ + ':' if (UseCapturedNS_ and self.receiverCompany_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sreceiverCompany>%s</%sreceiverCompany>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.receiverCompany), input_name='receiverCompany')), namespaceprefix_ , eol_))
        if self.requestedDeliveryDate is not None:
            namespaceprefix_ = self.requestedDeliveryDate_nsprefix_ + ':' if (UseCapturedNS_ and self.requestedDeliveryDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%srequestedDeliveryDate>%s</%srequestedDeliveryDate>%s' % (namespaceprefix_ , self.gds_format_date(self.requestedDeliveryDate, input_name='requestedDeliveryDate'), namespaceprefix_ , eol_))
        if self.shopHandlingInstruction is not None:
            namespaceprefix_ = self.shopHandlingInstruction_nsprefix_ + ':' if (UseCapturedNS_ and self.shopHandlingInstruction_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sshopHandlingInstruction>%s</%sshopHandlingInstruction>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.shopHandlingInstruction), input_name='shopHandlingInstruction')), namespaceprefix_ , eol_))
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
        super(atBpost, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'pugoId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'pugoId')
            value_ = self.gds_validate_string(value_, node, 'pugoId')
            self.pugoId = value_
            self.pugoId_nsprefix_ = child_.prefix
            # validate type RcCode
            self.validate_RcCode(self.pugoId)
        elif nodeName_ == 'pugoName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'pugoName')
            value_ = self.gds_validate_string(value_, node, 'pugoName')
            self.pugoName = value_
            self.pugoName_nsprefix_ = child_.prefix
            # validate type ReceiverNameType
            self.validate_ReceiverNameType(self.pugoName)
        elif nodeName_ == 'pugoAddress':
            obj_ = AddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.pugoAddress = obj_
            obj_.original_tagname_ = 'pugoAddress'
        elif nodeName_ == 'receiverName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'receiverName')
            value_ = self.gds_validate_string(value_, node, 'receiverName')
            self.receiverName = value_
            self.receiverName_nsprefix_ = child_.prefix
            # validate type ReceiverNameType
            self.validate_ReceiverNameType(self.receiverName)
        elif nodeName_ == 'receiverCompany':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'receiverCompany')
            value_ = self.gds_validate_string(value_, node, 'receiverCompany')
            self.receiverCompany = value_
            self.receiverCompany_nsprefix_ = child_.prefix
            # validate type ReceiverCompany
            self.validate_ReceiverCompany(self.receiverCompany)
        elif nodeName_ == 'requestedDeliveryDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.requestedDeliveryDate = dval_
            self.requestedDeliveryDate_nsprefix_ = child_.prefix
            # validate type RequestedDeliveryDateType
            self.validate_RequestedDeliveryDateType(self.requestedDeliveryDate)
        elif nodeName_ == 'shopHandlingInstruction':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'shopHandlingInstruction')
            value_ = self.gds_validate_string(value_, node, 'shopHandlingInstruction')
            self.shopHandlingInstruction = value_
            self.shopHandlingInstruction_nsprefix_ = child_.prefix
            # validate type ShopHandlingInstructionType
            self.validate_ShopHandlingInstructionType(self.shopHandlingInstruction)
        super(atBpost, self)._buildChildren(child_, node, nodeName_, True)
# end class atBpost


class atHome(NationalDeliveryMethodType):
    """atHome --  'Home or Office' delivery.
    receiver --  Element holding information about
    the receiver of the parcel.
    requestedDeliveryDate -- See type definition.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = NationalDeliveryMethodType
    def __init__(self, product=None, options=None, weight=None, height=None, length=None, width=None, openingHours=None, desiredDeliveryPlace=None, receiver=None, requestedDeliveryDate=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("atHome"), self).__init__(product, options, weight, height, length, width, openingHours, desiredDeliveryPlace,  **kwargs_)
        self.receiver = receiver
        self.receiver_nsprefix_ = "common"
        if isinstance(requestedDeliveryDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(requestedDeliveryDate, '%Y-%m-%d').date()
        else:
            initvalue_ = requestedDeliveryDate
        self.requestedDeliveryDate = initvalue_
        self.requestedDeliveryDate_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, atHome)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if atHome.subclass:
            return atHome.subclass(*args_, **kwargs_)
        else:
            return atHome(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_receiver(self):
        return self.receiver
    def set_receiver(self, receiver):
        self.receiver = receiver
    def get_requestedDeliveryDate(self):
        return self.requestedDeliveryDate
    def set_requestedDeliveryDate(self, requestedDeliveryDate):
        self.requestedDeliveryDate = requestedDeliveryDate
    def validate_RequestedDeliveryDateType(self, value):
        result = True
        # Validate type RequestedDeliveryDateType, a restriction on xs:date.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.date):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.date)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def has__content(self):
        if (
            self.receiver is not None or
            self.requestedDeliveryDate is not None or
            super(atHome, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='atHome', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('atHome')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'atHome':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='atHome')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='atHome', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='atHome'):
        super(atHome, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='atHome')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='atHome', fromsubclass_=False, pretty_print=True):
        super(atHome, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.receiver is not None:
            namespaceprefix_ = self.receiver_nsprefix_ + ':' if (UseCapturedNS_ and self.receiver_nsprefix_) else ''
            self.receiver.export(outfile, level, namespaceprefix_, namespacedef_='', name_='receiver', pretty_print=pretty_print)
        if self.requestedDeliveryDate is not None:
            namespaceprefix_ = self.requestedDeliveryDate_nsprefix_ + ':' if (UseCapturedNS_ and self.requestedDeliveryDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%srequestedDeliveryDate>%s</%srequestedDeliveryDate>%s' % (namespaceprefix_ , self.gds_format_date(self.requestedDeliveryDate, input_name='requestedDeliveryDate'), namespaceprefix_ , eol_))
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
        super(atHome, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'receiver':
            obj_ = Party.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.receiver = obj_
            obj_.original_tagname_ = 'receiver'
        elif nodeName_ == 'requestedDeliveryDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.requestedDeliveryDate = dval_
            self.requestedDeliveryDate_nsprefix_ = child_.prefix
            # validate type RequestedDeliveryDateType
            self.validate_RequestedDeliveryDateType(self.requestedDeliveryDate)
        super(atHome, self)._buildChildren(child_, node, nodeName_, True)
# end class atHome


#
# End data representation classes.
#


GDSClassesMapping = {
    'batchLabels': BatchLabelsType,
    'invalidSelection': InvalidSelectionType,
    'labels': LabelsType,
    'order': OrderType,
    'orderInfo': OrderInfoType,
    'orderUpdate': OrderUpdateType,
    'productConfiguration': ProductConfigurationType,
    'unknownItems': UnknownItemsType,
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
        rootTag = 'OrderType'
        rootClass = OrderType
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
        rootTag = 'OrderType'
        rootClass = OrderType
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
        rootTag = 'OrderType'
        rootClass = OrderType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:tns="http://schema.post.be/shm/deepintegration/v5/"')
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
        rootTag = 'OrderType'
        rootClass = OrderType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from shm_deep_integration_v5 import *\n\n')
        sys.stdout.write('import shm_deep_integration_v5 as model_\n\n')
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
    "{http://schema.post.be/shm/deepintegration/v5/international}RequestedDeliveryDateType": "RequestedDeliveryDateType1",
}

#
# Mapping of namespaces to types defined in them
# and the file in which each is defined.
# simpleTypes are marked "ST" and complexTypes "CT".
NamespaceToDefMappings_ = {'http://schema.post.be/shm/deepintegration/v5/': [('OrderReferenceType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'ST'),
                                                   ('BarcodeType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'ST'),
                                                   ('CrossReferenceBarcodeType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'ST'),
                                                   ('OrderLineTextType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'ST'),
                                                   ('RemarkType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'ST'),
                                                   ('OrderUpdateType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'CT'),
                                                   ('BaseOrderType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'CT'),
                                                   ('OrderType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'CT'),
                                                   ('OrderInfoType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'CT'),
                                                   ('OrderLineType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'CT'),
                                                   ('BoxType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'CT'),
                                                   ('CreateBoxType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'CT'),
                                                   ('BoxInfoType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'CT'),
                                                   ('BatchLabelsType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'CT'),
                                                   ('UnknownItemsType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'CT'),
                                                   ('LabelsType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'CT'),
                                                   ('ProductConfigurationType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'CT'),
                                                   ('InvalidSelectionType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'CT'),
                                                   ('BarcodeWithReferenceType',
                                                    './schemas/shm_deep_integration_v5.xsd',
                                                    'CT')],
 'http://schema.post.be/shm/deepintegration/v5/common': [('AccountIdType',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('CostCenterType',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('WeightInGrams',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('HeightInMm',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('LegthInMm',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('WidthInMm',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('HeightInCm',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('LengthInCm',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('WidthInCm',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('EuroCentAmount',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('IbanType',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('BicType',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('EmailAddressType',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('EmailAddressCharacteristicType',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('PhoneNumberType',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('ReceiverNameType',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('ReceiverCompany',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('StreetNameType',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('StreetNumberType',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('StreetBoxType',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('PostalCodeType',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('LocalityType',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('CountryCode',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('RcCode',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('BpackMemberId',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('BoxStatusType',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('SetBoxStatusType',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('PreferredDeliveryWindowType',
                                                          './schemas/common_v5.xsd',
                                                          'ST'),
                                                         ('Party',
                                                          './schemas/common_v5.xsd',
                                                          'CT'),
                                                         ('AddressType',
                                                          './schemas/common_v5.xsd',
                                                          'CT'),
                                                         ('OptionsType',
                                                          './schemas/common_v5.xsd',
                                                          'CT'),
                                                         ('InsuranceType',
                                                          './schemas/common_v5.xsd',
                                                          'CT'),
                                                         ('AdditionalInsuranceType',
                                                          './schemas/common_v5.xsd',
                                                          'CT'),
                                                         ('NotificationType',
                                                          './schemas/common_v5.xsd',
                                                          'CT'),
                                                         ('TimeSlotDeliveryType',
                                                          './schemas/common_v5.xsd',
                                                          'CT'),
                                                         ('CodType',
                                                          './schemas/common_v5.xsd',
                                                          'CT'),
                                                         ('SignatureType',
                                                          './schemas/common_v5.xsd',
                                                          'CT'),
                                                         ('SaturdayDeliveryType',
                                                          './schemas/common_v5.xsd',
                                                          'CT'),
                                                         ('SundayDeliveryType',
                                                          './schemas/common_v5.xsd',
                                                          'CT'),
                                                         ('FragileType',
                                                          './schemas/common_v5.xsd',
                                                          'CT'),
                                                         ('FullServiceType',
                                                          './schemas/common_v5.xsd',
                                                          'CT'),
                                                         ('DoorStepPlusServiceType',
                                                          './schemas/common_v5.xsd',
                                                          'CT'),
                                                         ('UltraLateInEveningDelivery',
                                                          './schemas/common_v5.xsd',
                                                          'CT')],
 'http://schema.post.be/shm/deepintegration/v5/international': [('ShipmentType',
                                                                 './schemas/international_v5.xsd',
                                                                 'ST'),
                                                                ('ParcelReturnInstructionsType',
                                                                 './schemas/international_v5.xsd',
                                                                 'ST'),
                                                                ('ContentDescriptionType',
                                                                 './schemas/international_v5.xsd',
                                                                 'ST'),
                                                                ('RequestedDeliveryDateType',
                                                                 './schemas/international_v5.xsd',
                                                                 'ST'),
                                                                ('CustomsType',
                                                                 './schemas/international_v5.xsd',
                                                                 'CT'),
                                                                ('InternationalBoxType',
                                                                 './schemas/international_v5.xsd',
                                                                 'CT'),
                                                                ('InternationalDeliveryMethodType',
                                                                 './schemas/international_v5.xsd',
                                                                 'CT'),
                                                                ('ParcelContentDetails',
                                                                 './schemas/international_v5.xsd',
                                                                 'CT'),
                                                                ('ParcelContentDetail',
                                                                 './schemas/international_v5.xsd',
                                                                 'CT')],
 'http://schema.post.be/shm/deepintegration/v5/national': [('RequestedDeliveryDateType',
                                                            './schemas/national_v5.xsd',
                                                            'ST'),
                                                           ('ShopHandlingInstructionType',
                                                            './schemas/national_v5.xsd',
                                                            'ST'),
                                                           ('OpeningHoursType',
                                                            './schemas/national_v5.xsd',
                                                            'ST'),
                                                           ('DesiredDeliveryPlaceType',
                                                            './schemas/national_v5.xsd',
                                                            'ST'),
                                                           ('NationalBoxType',
                                                            './schemas/national_v5.xsd',
                                                            'CT'),
                                                           ('NationalDeliveryMethodType',
                                                            './schemas/national_v5.xsd',
                                                            'CT'),
                                                           ('UnregisteredParcelLockerMemberType',
                                                            './schemas/national_v5.xsd',
                                                            'CT'),
                                                           ('ParcelLockerReducedMobilityZoneType',
                                                            './schemas/national_v5.xsd',
                                                            'CT')]}

__all__ = [
    "AdditionalInsuranceType",
    "AddressType",
    "BarcodeWithReferenceType",
    "BaseOrderType",
    "BatchLabelsType",
    "BoxInfoType",
    "BoxType",
    "CodType",
    "CreateBoxType",
    "CustomsType",
    "DoorStepPlusServiceType",
    "FragileType",
    "FullServiceType",
    "InsuranceType",
    "InternationalBoxType",
    "InternationalDeliveryMethodType",
    "InvalidSelectionType",
    "LabelsType",
    "NationalBoxType",
    "NationalDeliveryMethodType",
    "NotificationType",
    "OptionsType",
    "OrderInfoType",
    "OrderLineType",
    "OrderType",
    "OrderUpdateType",
    "ParcelContentDetail",
    "ParcelContentDetails",
    "ParcelLockerReducedMobilityZoneType",
    "Party",
    "ProductConfigurationType",
    "SaturdayDeliveryType",
    "SignatureType",
    "SundayDeliveryType",
    "TimeSlotDeliveryType",
    "UltraLateInEveningDelivery",
    "UnknownItemsType",
    "UnregisteredParcelLockerMemberType",
    "at24_7",
    "atBpost",
    "atHome",
    "atIntlParcelDepot",
    "atIntlPugo",
    "automaticSecondPresentationType",
    "basicInsuranceType",
    "bpostOnAppointment",
    "characteristicType",
    "deliveryMethodType",
    "labelType",
    "openingHoursType",
    "optionType",
    "priceType",
    "productType"
]
