#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Thu Nov  9 10:01:53 2023 by generateDS.py version 2.43.3.
# Python 3.10.9 (main, Dec 15 2022, 18:18:30) [Clang 14.0.0 (clang-1400.0.29.202)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './karrio/schemas/bpost/announcement_common_v1.py')
#
# Command line arguments:
#   ./schemas/announcement_common_v1.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/karrio/.venv/karrio/bin/generateDS --no-namespace-defs -o "./karrio/schemas/bpost/announcement_common_v1.py" ./schemas/announcement_common_v1.xsd
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
class deliveryTimeFrame(str, Enum):
    AM='AM'
    PM='PM'
    PMPLUS='PMPLUS'
    OFFICE='OFFICE'


class deliveryTimeslotType(str, Enum):
    AM='AM'
    PM='PM'
    PMPLUS='PMPLUS'


class itemCategoryType(str, Enum):
    """itemCategoryType -- Indicates the category of the item
    
    """
    GIFT='GIFT'
    DOCUMENTS='DOCUMENTS'
    SAMPLE='SAMPLE'
    GOODS='GOODS'
    RETURNEDGOODS='RETURNED GOODS'
    OTHER='OTHER'


class languageType(str, Enum):
    EN='EN'
    NL='NL'
    FR='FR'
    DE='DE'


class maxAmountType(str, Enum):
    _1='1'
    _2='2'
    _3='3'
    _4='4'
    _5='5'
    _6='6'
    _7='7'
    _8='8'
    _9='9'
    _1_0='10'
    _1_1='11'


class messageTypeType(str, Enum):
    EMAIL='EMAIL'
    SMS='SMS'


class valueType(str, Enum):
    RTS='RTS'
    RTA='RTA'
    ABANDONED='ABANDONED'


#
# Start data representation classes
#
class addressType(GeneratedsSuper):
    """streetName -- Mandatory according to the LCI-in user manual???
    streetName2 -- Used for the second line of the street name.
    postalCode -- If the addressee is located in Belgium, the 4 digit postal code should be used.
    countryCode -- The country according to ISO alpha 2 (e.g. BE for Belgium)
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, streetName=None, streetName2=None, houseNumber=None, boxNumber=None, postalCode=None, city=None, geographicalSanction=None, pdpId=None, pdpSuffix=None, countryCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.streetName = streetName
        self.validate_streetNameType(self.streetName)
        self.streetName_nsprefix_ = None
        self.streetName2 = streetName2
        self.validate_streetName2Type(self.streetName2)
        self.streetName2_nsprefix_ = None
        self.houseNumber = houseNumber
        self.validate_houseNumberType(self.houseNumber)
        self.houseNumber_nsprefix_ = None
        self.boxNumber = boxNumber
        self.validate_boxNumberType(self.boxNumber)
        self.boxNumber_nsprefix_ = None
        self.postalCode = postalCode
        self.validate_postalCodeType(self.postalCode)
        self.postalCode_nsprefix_ = None
        self.city = city
        self.validate_cityType(self.city)
        self.city_nsprefix_ = None
        self.geographicalSanction = geographicalSanction
        self.validate_geographicalSanctionType(self.geographicalSanction)
        self.geographicalSanction_nsprefix_ = None
        self.pdpId = pdpId
        self.validate_pdpIdType(self.pdpId)
        self.pdpId_nsprefix_ = None
        self.pdpSuffix = pdpSuffix
        self.validate_pdpSuffixType(self.pdpSuffix)
        self.pdpSuffix_nsprefix_ = None
        self.countryCode = countryCode
        self.validate_countryCodeType(self.countryCode)
        self.countryCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, addressType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if addressType.subclass:
            return addressType.subclass(*args_, **kwargs_)
        else:
            return addressType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_streetName(self):
        return self.streetName
    def set_streetName(self, streetName):
        self.streetName = streetName
    def get_streetName2(self):
        return self.streetName2
    def set_streetName2(self, streetName2):
        self.streetName2 = streetName2
    def get_houseNumber(self):
        return self.houseNumber
    def set_houseNumber(self, houseNumber):
        self.houseNumber = houseNumber
    def get_boxNumber(self):
        return self.boxNumber
    def set_boxNumber(self, boxNumber):
        self.boxNumber = boxNumber
    def get_postalCode(self):
        return self.postalCode
    def set_postalCode(self, postalCode):
        self.postalCode = postalCode
    def get_city(self):
        return self.city
    def set_city(self, city):
        self.city = city
    def get_geographicalSanction(self):
        return self.geographicalSanction
    def set_geographicalSanction(self, geographicalSanction):
        self.geographicalSanction = geographicalSanction
    def get_pdpId(self):
        return self.pdpId
    def set_pdpId(self, pdpId):
        self.pdpId = pdpId
    def get_pdpSuffix(self):
        return self.pdpSuffix
    def set_pdpSuffix(self, pdpSuffix):
        self.pdpSuffix = pdpSuffix
    def get_countryCode(self):
        return self.countryCode
    def set_countryCode(self, countryCode):
        self.countryCode = countryCode
    def validate_streetNameType(self, value):
        result = True
        # Validate type streetNameType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_streetName2Type(self, value):
        result = True
        # Validate type streetName2Type, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetName2Type' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_houseNumberType(self, value):
        result = True
        # Validate type houseNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 8:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on houseNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_boxNumberType(self, value):
        result = True
        # Validate type boxNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 8:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on boxNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_postalCodeType(self, value):
        result = True
        # Validate type postalCodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 8:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on postalCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_cityType(self, value):
        result = True
        # Validate type cityType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on cityType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_geographicalSanctionType(self, value):
        result = True
        # Validate type geographicalSanctionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on geographicalSanctionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_pdpIdType(self, value):
        result = True
        # Validate type pdpIdType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on pdpIdType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_pdpSuffixType(self, value):
        result = True
        # Validate type pdpSuffixType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on pdpSuffixType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_countryCodeType(self, value):
        result = True
        # Validate type countryCodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on countryCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_countryCodeType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_countryCodeType_patterns_, ))
                result = False
        return result
    validate_countryCodeType_patterns_ = [['^([A-Za-z]{2})$']]
    def has__content(self):
        if (
            self.streetName is not None or
            self.streetName2 is not None or
            self.houseNumber is not None or
            self.boxNumber is not None or
            self.postalCode is not None or
            self.city is not None or
            self.geographicalSanction is not None or
            self.pdpId is not None or
            self.pdpSuffix is not None or
            self.countryCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='addressType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('addressType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'addressType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='addressType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='addressType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='addressType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='addressType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.streetName is not None:
            namespaceprefix_ = self.streetName_nsprefix_ + ':' if (UseCapturedNS_ and self.streetName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstreetName>%s</%sstreetName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.streetName), input_name='streetName')), namespaceprefix_ , eol_))
        if self.streetName2 is not None:
            namespaceprefix_ = self.streetName2_nsprefix_ + ':' if (UseCapturedNS_ and self.streetName2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstreetName2>%s</%sstreetName2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.streetName2), input_name='streetName2')), namespaceprefix_ , eol_))
        if self.houseNumber is not None:
            namespaceprefix_ = self.houseNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.houseNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%shouseNumber>%s</%shouseNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.houseNumber), input_name='houseNumber')), namespaceprefix_ , eol_))
        if self.boxNumber is not None:
            namespaceprefix_ = self.boxNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.boxNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sboxNumber>%s</%sboxNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.boxNumber), input_name='boxNumber')), namespaceprefix_ , eol_))
        if self.postalCode is not None:
            namespaceprefix_ = self.postalCode_nsprefix_ + ':' if (UseCapturedNS_ and self.postalCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spostalCode>%s</%spostalCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.postalCode), input_name='postalCode')), namespaceprefix_ , eol_))
        if self.city is not None:
            namespaceprefix_ = self.city_nsprefix_ + ':' if (UseCapturedNS_ and self.city_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scity>%s</%scity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.city), input_name='city')), namespaceprefix_ , eol_))
        if self.geographicalSanction is not None:
            namespaceprefix_ = self.geographicalSanction_nsprefix_ + ':' if (UseCapturedNS_ and self.geographicalSanction_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sgeographicalSanction>%s</%sgeographicalSanction>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.geographicalSanction), input_name='geographicalSanction')), namespaceprefix_ , eol_))
        if self.pdpId is not None:
            namespaceprefix_ = self.pdpId_nsprefix_ + ':' if (UseCapturedNS_ and self.pdpId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spdpId>%s</%spdpId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.pdpId), input_name='pdpId')), namespaceprefix_ , eol_))
        if self.pdpSuffix is not None:
            namespaceprefix_ = self.pdpSuffix_nsprefix_ + ':' if (UseCapturedNS_ and self.pdpSuffix_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spdpSuffix>%s</%spdpSuffix>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.pdpSuffix), input_name='pdpSuffix')), namespaceprefix_ , eol_))
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
            # validate type streetNameType
            self.validate_streetNameType(self.streetName)
        elif nodeName_ == 'streetName2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'streetName2')
            value_ = self.gds_validate_string(value_, node, 'streetName2')
            self.streetName2 = value_
            self.streetName2_nsprefix_ = child_.prefix
            # validate type streetName2Type
            self.validate_streetName2Type(self.streetName2)
        elif nodeName_ == 'houseNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'houseNumber')
            value_ = self.gds_validate_string(value_, node, 'houseNumber')
            self.houseNumber = value_
            self.houseNumber_nsprefix_ = child_.prefix
            # validate type houseNumberType
            self.validate_houseNumberType(self.houseNumber)
        elif nodeName_ == 'boxNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'boxNumber')
            value_ = self.gds_validate_string(value_, node, 'boxNumber')
            self.boxNumber = value_
            self.boxNumber_nsprefix_ = child_.prefix
            # validate type boxNumberType
            self.validate_boxNumberType(self.boxNumber)
        elif nodeName_ == 'postalCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'postalCode')
            value_ = self.gds_validate_string(value_, node, 'postalCode')
            self.postalCode = value_
            self.postalCode_nsprefix_ = child_.prefix
            # validate type postalCodeType
            self.validate_postalCodeType(self.postalCode)
        elif nodeName_ == 'city':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'city')
            value_ = self.gds_validate_string(value_, node, 'city')
            self.city = value_
            self.city_nsprefix_ = child_.prefix
            # validate type cityType
            self.validate_cityType(self.city)
        elif nodeName_ == 'geographicalSanction':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'geographicalSanction')
            value_ = self.gds_validate_string(value_, node, 'geographicalSanction')
            self.geographicalSanction = value_
            self.geographicalSanction_nsprefix_ = child_.prefix
            # validate type geographicalSanctionType
            self.validate_geographicalSanctionType(self.geographicalSanction)
        elif nodeName_ == 'pdpId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'pdpId')
            value_ = self.gds_validate_string(value_, node, 'pdpId')
            self.pdpId = value_
            self.pdpId_nsprefix_ = child_.prefix
            # validate type pdpIdType
            self.validate_pdpIdType(self.pdpId)
        elif nodeName_ == 'pdpSuffix':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'pdpSuffix')
            value_ = self.gds_validate_string(value_, node, 'pdpSuffix')
            self.pdpSuffix = value_
            self.pdpSuffix_nsprefix_ = child_.prefix
            # validate type pdpSuffixType
            self.validate_pdpSuffixType(self.pdpSuffix)
        elif nodeName_ == 'countryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'countryCode')
            value_ = self.gds_validate_string(value_, node, 'countryCode')
            self.countryCode = value_
            self.countryCode_nsprefix_ = child_.prefix
            # validate type countryCodeType
            self.validate_countryCodeType(self.countryCode)
# end class addressType


class contactDetailType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, emailAddress=None, telephoneNumber=None, mobilePhone=None, language=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.emailAddress = emailAddress
        self.validate_emailAddressType(self.emailAddress)
        self.emailAddress_nsprefix_ = None
        self.telephoneNumber = telephoneNumber
        self.validate_telephoneNumberType(self.telephoneNumber)
        self.telephoneNumber_nsprefix_ = None
        self.mobilePhone = mobilePhone
        self.validate_mobilePhoneType(self.mobilePhone)
        self.mobilePhone_nsprefix_ = None
        self.language = language
        self.validate_languageType(self.language)
        self.language_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, contactDetailType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if contactDetailType.subclass:
            return contactDetailType.subclass(*args_, **kwargs_)
        else:
            return contactDetailType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_emailAddress(self):
        return self.emailAddress
    def set_emailAddress(self, emailAddress):
        self.emailAddress = emailAddress
    def get_telephoneNumber(self):
        return self.telephoneNumber
    def set_telephoneNumber(self, telephoneNumber):
        self.telephoneNumber = telephoneNumber
    def get_mobilePhone(self):
        return self.mobilePhone
    def set_mobilePhone(self, mobilePhone):
        self.mobilePhone = mobilePhone
    def get_language(self):
        return self.language
    def set_language(self, language):
        self.language = language
    def validate_emailAddressType(self, value):
        result = True
        # Validate type emailAddressType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on emailAddressType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_telephoneNumberType(self, value):
        result = True
        # Validate type telephoneNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on telephoneNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_mobilePhoneType(self, value):
        result = True
        # Validate type mobilePhoneType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on mobilePhoneType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_languageType(self, value):
        result = True
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
        return result
    def has__content(self):
        if (
            self.emailAddress is not None or
            self.telephoneNumber is not None or
            self.mobilePhone is not None or
            self.language is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='contactDetailType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('contactDetailType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'contactDetailType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='contactDetailType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='contactDetailType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='contactDetailType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='contactDetailType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.emailAddress is not None:
            namespaceprefix_ = self.emailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.emailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%semailAddress>%s</%semailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.emailAddress), input_name='emailAddress')), namespaceprefix_ , eol_))
        if self.telephoneNumber is not None:
            namespaceprefix_ = self.telephoneNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.telephoneNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stelephoneNumber>%s</%stelephoneNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.telephoneNumber), input_name='telephoneNumber')), namespaceprefix_ , eol_))
        if self.mobilePhone is not None:
            namespaceprefix_ = self.mobilePhone_nsprefix_ + ':' if (UseCapturedNS_ and self.mobilePhone_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smobilePhone>%s</%smobilePhone>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.mobilePhone), input_name='mobilePhone')), namespaceprefix_ , eol_))
        if self.language is not None:
            namespaceprefix_ = self.language_nsprefix_ + ':' if (UseCapturedNS_ and self.language_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slanguage>%s</%slanguage>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.language), input_name='language')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'emailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'emailAddress')
            value_ = self.gds_validate_string(value_, node, 'emailAddress')
            self.emailAddress = value_
            self.emailAddress_nsprefix_ = child_.prefix
            # validate type emailAddressType
            self.validate_emailAddressType(self.emailAddress)
        elif nodeName_ == 'telephoneNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'telephoneNumber')
            value_ = self.gds_validate_string(value_, node, 'telephoneNumber')
            self.telephoneNumber = value_
            self.telephoneNumber_nsprefix_ = child_.prefix
            # validate type telephoneNumberType
            self.validate_telephoneNumberType(self.telephoneNumber)
        elif nodeName_ == 'mobilePhone':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'mobilePhone')
            value_ = self.gds_validate_string(value_, node, 'mobilePhone')
            self.mobilePhone = value_
            self.mobilePhone_nsprefix_ = child_.prefix
            # validate type mobilePhoneType
            self.validate_mobilePhoneType(self.mobilePhone)
        elif nodeName_ == 'language':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'language')
            value_ = self.gds_validate_string(value_, node, 'language')
            self.language = value_
            self.language_nsprefix_ = child_.prefix
            # validate type languageType
            self.validate_languageType(self.language)
# end class contactDetailType


class notificationType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, language=None, emailAddress=None, smsNumber=None, voiceNumber=None, messageType=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.language = _cast(None, language)
        self.language_nsprefix_ = None
        self.emailAddress = emailAddress
        self.validate_emailAddressType1(self.emailAddress)
        self.emailAddress_nsprefix_ = None
        self.smsNumber = smsNumber
        self.validate_smsNumberType(self.smsNumber)
        self.smsNumber_nsprefix_ = None
        self.voiceNumber = voiceNumber
        self.validate_voiceNumberType(self.voiceNumber)
        self.voiceNumber_nsprefix_ = None
        self.messageType = messageType
        self.validate_messageTypeType(self.messageType)
        self.messageType_nsprefix_ = None
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, notificationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if notificationType.subclass:
            return notificationType.subclass(*args_, **kwargs_)
        else:
            return notificationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_emailAddress(self):
        return self.emailAddress
    def set_emailAddress(self, emailAddress):
        self.emailAddress = emailAddress
    def get_smsNumber(self):
        return self.smsNumber
    def set_smsNumber(self, smsNumber):
        self.smsNumber = smsNumber
    def get_voiceNumber(self):
        return self.voiceNumber
    def set_voiceNumber(self, voiceNumber):
        self.voiceNumber = voiceNumber
    def get_messageType(self):
        return self.messageType
    def set_messageType(self, messageType):
        self.messageType = messageType
    def get_language(self):
        return self.language
    def set_language(self, language):
        self.language = language
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def validate_emailAddressType1(self, value):
        result = True
        # Validate type emailAddressType1, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on emailAddressType1' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on emailAddressType1' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_smsNumberType(self, value):
        result = True
        # Validate type smsNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on smsNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on smsNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_voiceNumberType(self, value):
        result = True
        # Validate type voiceNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on voiceNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_messageTypeType(self, value):
        result = True
        # Validate type messageTypeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['EMAIL', 'SMS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on messageTypeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
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
            self.smsNumber is not None or
            self.voiceNumber is not None or
            self.messageType is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='notificationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('notificationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'notificationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='notificationType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='notificationType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='notificationType'):
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
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='notificationType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.emailAddress is not None:
            namespaceprefix_ = self.emailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.emailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%semailAddress>%s</%semailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.emailAddress), input_name='emailAddress')), namespaceprefix_ , eol_))
        if self.smsNumber is not None:
            namespaceprefix_ = self.smsNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.smsNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssmsNumber>%s</%ssmsNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.smsNumber), input_name='smsNumber')), namespaceprefix_ , eol_))
        if self.voiceNumber is not None:
            namespaceprefix_ = self.voiceNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.voiceNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%svoiceNumber>%s</%svoiceNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.voiceNumber), input_name='voiceNumber')), namespaceprefix_ , eol_))
        if self.messageType is not None:
            namespaceprefix_ = self.messageType_nsprefix_ + ':' if (UseCapturedNS_ and self.messageType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smessageType>%s</%smessageType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.messageType), input_name='messageType')), namespaceprefix_ , eol_))
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
            # validate type emailAddressType1
            self.validate_emailAddressType1(self.emailAddress)
        elif nodeName_ == 'smsNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'smsNumber')
            value_ = self.gds_validate_string(value_, node, 'smsNumber')
            self.smsNumber = value_
            self.smsNumber_nsprefix_ = child_.prefix
            # validate type smsNumberType
            self.validate_smsNumberType(self.smsNumber)
        elif nodeName_ == 'voiceNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'voiceNumber')
            value_ = self.gds_validate_string(value_, node, 'voiceNumber')
            self.voiceNumber = value_
            self.voiceNumber_nsprefix_ = child_.prefix
            # validate type voiceNumberType
            self.validate_voiceNumberType(self.voiceNumber)
        elif nodeName_ == 'messageType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'messageType')
            value_ = self.gds_validate_string(value_, node, 'messageType')
            self.messageType = value_
            self.messageType_nsprefix_ = child_.prefix
            # validate type messageTypeType
            self.validate_messageTypeType(self.messageType)
# end class notificationType


class clientType(GeneratedsSuper):
    """name -- The Name, most often the company name
    addressPlace -- A specific place, e.g. 'desk 405'
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, name=None, addressDepartment=None, addressContactName=None, addressPlace=None, address=None, contactDetail=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name = name
        self.validate_nameType(self.name)
        self.name_nsprefix_ = None
        self.addressDepartment = addressDepartment
        self.validate_addressDepartmentType(self.addressDepartment)
        self.addressDepartment_nsprefix_ = None
        self.addressContactName = addressContactName
        self.validate_addressContactNameType(self.addressContactName)
        self.addressContactName_nsprefix_ = None
        self.addressPlace = addressPlace
        self.validate_addressPlaceType(self.addressPlace)
        self.addressPlace_nsprefix_ = None
        self.address = address
        self.address_nsprefix_ = None
        self.contactDetail = contactDetail
        self.contactDetail_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, clientType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if clientType.subclass:
            return clientType.subclass(*args_, **kwargs_)
        else:
            return clientType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_addressDepartment(self):
        return self.addressDepartment
    def set_addressDepartment(self, addressDepartment):
        self.addressDepartment = addressDepartment
    def get_addressContactName(self):
        return self.addressContactName
    def set_addressContactName(self, addressContactName):
        self.addressContactName = addressContactName
    def get_addressPlace(self):
        return self.addressPlace
    def set_addressPlace(self, addressPlace):
        self.addressPlace = addressPlace
    def get_address(self):
        return self.address
    def set_address(self, address):
        self.address = address
    def get_contactDetail(self):
        return self.contactDetail
    def set_contactDetail(self, contactDetail):
        self.contactDetail = contactDetail
    def validate_nameType(self, value):
        result = True
        # Validate type nameType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on nameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_addressDepartmentType(self, value):
        result = True
        # Validate type addressDepartmentType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on addressDepartmentType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_addressContactNameType(self, value):
        result = True
        # Validate type addressContactNameType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on addressContactNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_addressPlaceType(self, value):
        result = True
        # Validate type addressPlaceType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on addressPlaceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.name is not None or
            self.addressDepartment is not None or
            self.addressContactName is not None or
            self.addressPlace is not None or
            self.address is not None or
            self.contactDetail is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='clientType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('clientType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'clientType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='clientType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='clientType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='clientType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='clientType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.name is not None:
            namespaceprefix_ = self.name_nsprefix_ + ':' if (UseCapturedNS_ and self.name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sname>%s</%sname>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.name), input_name='name')), namespaceprefix_ , eol_))
        if self.addressDepartment is not None:
            namespaceprefix_ = self.addressDepartment_nsprefix_ + ':' if (UseCapturedNS_ and self.addressDepartment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saddressDepartment>%s</%saddressDepartment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.addressDepartment), input_name='addressDepartment')), namespaceprefix_ , eol_))
        if self.addressContactName is not None:
            namespaceprefix_ = self.addressContactName_nsprefix_ + ':' if (UseCapturedNS_ and self.addressContactName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saddressContactName>%s</%saddressContactName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.addressContactName), input_name='addressContactName')), namespaceprefix_ , eol_))
        if self.addressPlace is not None:
            namespaceprefix_ = self.addressPlace_nsprefix_ + ':' if (UseCapturedNS_ and self.addressPlace_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saddressPlace>%s</%saddressPlace>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.addressPlace), input_name='addressPlace')), namespaceprefix_ , eol_))
        if self.address is not None:
            namespaceprefix_ = self.address_nsprefix_ + ':' if (UseCapturedNS_ and self.address_nsprefix_) else ''
            self.address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='address', pretty_print=pretty_print)
        if self.contactDetail is not None:
            namespaceprefix_ = self.contactDetail_nsprefix_ + ':' if (UseCapturedNS_ and self.contactDetail_nsprefix_) else ''
            self.contactDetail.export(outfile, level, namespaceprefix_, namespacedef_='', name_='contactDetail', pretty_print=pretty_print)
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
            # validate type nameType
            self.validate_nameType(self.name)
        elif nodeName_ == 'addressDepartment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'addressDepartment')
            value_ = self.gds_validate_string(value_, node, 'addressDepartment')
            self.addressDepartment = value_
            self.addressDepartment_nsprefix_ = child_.prefix
            # validate type addressDepartmentType
            self.validate_addressDepartmentType(self.addressDepartment)
        elif nodeName_ == 'addressContactName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'addressContactName')
            value_ = self.gds_validate_string(value_, node, 'addressContactName')
            self.addressContactName = value_
            self.addressContactName_nsprefix_ = child_.prefix
            # validate type addressContactNameType
            self.validate_addressContactNameType(self.addressContactName)
        elif nodeName_ == 'addressPlace':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'addressPlace')
            value_ = self.gds_validate_string(value_, node, 'addressPlace')
            self.addressPlace = value_
            self.addressPlace_nsprefix_ = child_.prefix
            # validate type addressPlaceType
            self.validate_addressPlaceType(self.addressPlace)
        elif nodeName_ == 'address':
            obj_ = addressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.address = obj_
            obj_.original_tagname_ = 'address'
        elif nodeName_ == 'contactDetail':
            obj_ = contactDetailType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.contactDetail = obj_
            obj_.original_tagname_ = 'contactDetail'
# end class clientType


class insuranceType(GeneratedsSuper):
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
                CurrentSubclassModule_, insuranceType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if insuranceType.subclass:
            return insuranceType.subclass(*args_, **kwargs_)
        else:
            return insuranceType(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='insuranceType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('insuranceType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'insuranceType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='insuranceType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='insuranceType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='insuranceType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='insuranceType', fromsubclass_=False, pretty_print=True):
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
            obj_ = additionalInsuranceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.additionalInsurance = obj_
            obj_.original_tagname_ = 'additionalInsurance'
# end class insuranceType


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


class additionalInsuranceType(GeneratedsSuper):
    """additionalInsuranceType --
    The range in which the insurance amount is situated
    1 = basic insurance up to 500 EUR
    2 = additional up to 2.500EUR
    3 = additional up to 5.000 EUR
    4 = additional up to 7.500 EUR
    5 = additional up to 10.000 EUR
    6 = additional up to 12.500 EUR
    7 = additional up to 15.000 EUR
    8 = additional up to 17.500 EUR
    9 = additional up to 20.000 EUR
    10 = additional up to 22.500 EUR
    11 = additional up to 25.000 EUR
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, maxAmount=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.maxAmount = _cast(int, maxAmount)
        self.maxAmount_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, additionalInsuranceType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if additionalInsuranceType.subclass:
            return additionalInsuranceType.subclass(*args_, **kwargs_)
        else:
            return additionalInsuranceType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_maxAmount(self):
        return self.maxAmount
    def set_maxAmount(self, maxAmount):
        self.maxAmount = maxAmount
    def validate_maxAmountType(self, value):
        # Validate type maxAmountType, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on maxAmountType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
    def has__content(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='additionalInsuranceType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('additionalInsuranceType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'additionalInsuranceType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='additionalInsuranceType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='additionalInsuranceType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='additionalInsuranceType'):
        if self.maxAmount is not None and 'maxAmount' not in already_processed:
            already_processed.add('maxAmount')
            outfile.write(' maxAmount="%s"' % self.gds_format_integer(self.maxAmount, input_name='maxAmount'))
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='additionalInsuranceType', fromsubclass_=False, pretty_print=True):
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
        value = find_attr_value_('maxAmount', node)
        if value is not None and 'maxAmount' not in already_processed:
            already_processed.add('maxAmount')
            self.maxAmount = self.gds_parse_integer(value, node, 'maxAmount')
            self.validate_maxAmountType(self.maxAmount)    # validate type maxAmountType
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class additionalInsuranceType


class signatureType(GeneratedsSuper):
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
                CurrentSubclassModule_, signatureType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if signatureType.subclass:
            return signatureType.subclass(*args_, **kwargs_)
        else:
            return signatureType(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='signatureType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('signatureType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'signatureType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='signatureType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='signatureType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='signatureType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='signatureType', fromsubclass_=False, pretty_print=True):
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
# end class signatureType


class signaturePlusType(GeneratedsSuper):
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
                CurrentSubclassModule_, signaturePlusType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if signaturePlusType.subclass:
            return signaturePlusType.subclass(*args_, **kwargs_)
        else:
            return signaturePlusType(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='signaturePlusType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('signaturePlusType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'signaturePlusType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='signaturePlusType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='signaturePlusType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='signaturePlusType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='signaturePlusType', fromsubclass_=False, pretty_print=True):
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
# end class signaturePlusType


class nonDeliveryInstructionsType(GeneratedsSuper):
    """nonDeliveryInstructionsType -- Indication of what needs to be done with the parcel in case it could not be delivered.
    RTS = return to sender via road transport
    RTA = return to sender via air transport
    ABANDONED = destroyed
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.value = _cast(None, value)
        self.value_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, nonDeliveryInstructionsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if nonDeliveryInstructionsType.subclass:
            return nonDeliveryInstructionsType.subclass(*args_, **kwargs_)
        else:
            return nonDeliveryInstructionsType(*args_, **kwargs_)
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
        # Validate type valueType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['RTS', 'RTA', 'ABANDONED']
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='nonDeliveryInstructionsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('nonDeliveryInstructionsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'nonDeliveryInstructionsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='nonDeliveryInstructionsType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='nonDeliveryInstructionsType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='nonDeliveryInstructionsType'):
        if self.value is not None and 'value' not in already_processed:
            already_processed.add('value')
            outfile.write(' value=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.value), input_name='value')), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='nonDeliveryInstructionsType', fromsubclass_=False, pretty_print=True):
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
            self.value = value
            self.validate_valueType(self.value)    # validate type valueType
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class nonDeliveryInstructionsType


class cashOnDeliveryType(GeneratedsSuper):
    """amountTotalInEuroCents -- The value that the receiver must pay (in euro cents).
    bban -- National Bank account number (12 digits).
    iban --
    International Bank account number.
    Only Belgian IBANs can be used.
      
    * bic -- Bank identification code, 8 or 11 characters.
    * bankTransferMessage --
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, amountTotalInEuroCents=None, bban=None, iban=None, bic=None, bankTransferMessage=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.amountTotalInEuroCents = amountTotalInEuroCents
        self.amountTotalInEuroCents_nsprefix_ = None
        self.bban = bban
        self.validate_bbanType(self.bban)
        self.bban_nsprefix_ = None
        self.iban = iban
        self.validate_belgianIbanType(self.iban)
        self.iban_nsprefix_ = None
        self.bic = bic
        self.validate_bicType(self.bic)
        self.bic_nsprefix_ = None
        self.bankTransferMessage = bankTransferMessage
        self.validate_bankTransferMessageType(self.bankTransferMessage)
        self.bankTransferMessage_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, cashOnDeliveryType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if cashOnDeliveryType.subclass:
            return cashOnDeliveryType.subclass(*args_, **kwargs_)
        else:
            return cashOnDeliveryType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_amountTotalInEuroCents(self):
        return self.amountTotalInEuroCents
    def set_amountTotalInEuroCents(self, amountTotalInEuroCents):
        self.amountTotalInEuroCents = amountTotalInEuroCents
    def get_bban(self):
        return self.bban
    def set_bban(self, bban):
        self.bban = bban
    def get_iban(self):
        return self.iban
    def set_iban(self, iban):
        self.iban = iban
    def get_bic(self):
        return self.bic
    def set_bic(self, bic):
        self.bic = bic
    def get_bankTransferMessage(self):
        return self.bankTransferMessage
    def set_bankTransferMessage(self, bankTransferMessage):
        self.bankTransferMessage = bankTransferMessage
    def validate_bbanType(self, value):
        result = True
        # Validate type bbanType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 12:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on bbanType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_belgianIbanType(self, value):
        result = True
        # Validate type belgianIbanType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_belgianIbanType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_belgianIbanType_patterns_, ))
                result = False
        return result
    validate_belgianIbanType_patterns_ = [['^([A-Z]{2}[0-9]{14})$']]
    def validate_bicType(self, value):
        result = True
        # Validate type bicType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_bicType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_bicType_patterns_, ))
                result = False
        return result
    validate_bicType_patterns_ = [['^([A-Z0-9]{8}|[A-Z0-9]{11})$']]
    def validate_bankTransferMessageType(self, value):
        result = True
        # Validate type bankTransferMessageType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on bankTransferMessageType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.amountTotalInEuroCents is not None or
            self.bban is not None or
            self.iban is not None or
            self.bic is not None or
            self.bankTransferMessage is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='cashOnDeliveryType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('cashOnDeliveryType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'cashOnDeliveryType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='cashOnDeliveryType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='cashOnDeliveryType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='cashOnDeliveryType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='cashOnDeliveryType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.amountTotalInEuroCents is not None:
            namespaceprefix_ = self.amountTotalInEuroCents_nsprefix_ + ':' if (UseCapturedNS_ and self.amountTotalInEuroCents_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%samountTotalInEuroCents>%s</%samountTotalInEuroCents>%s' % (namespaceprefix_ , self.gds_format_integer(self.amountTotalInEuroCents, input_name='amountTotalInEuroCents'), namespaceprefix_ , eol_))
        if self.bban is not None:
            namespaceprefix_ = self.bban_nsprefix_ + ':' if (UseCapturedNS_ and self.bban_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sbban>%s</%sbban>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.bban), input_name='bban')), namespaceprefix_ , eol_))
        if self.iban is not None:
            namespaceprefix_ = self.iban_nsprefix_ + ':' if (UseCapturedNS_ and self.iban_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%siban>%s</%siban>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.iban), input_name='iban')), namespaceprefix_ , eol_))
        if self.bic is not None:
            namespaceprefix_ = self.bic_nsprefix_ + ':' if (UseCapturedNS_ and self.bic_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sbic>%s</%sbic>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.bic), input_name='bic')), namespaceprefix_ , eol_))
        if self.bankTransferMessage is not None:
            namespaceprefix_ = self.bankTransferMessage_nsprefix_ + ':' if (UseCapturedNS_ and self.bankTransferMessage_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sbankTransferMessage>%s</%sbankTransferMessage>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.bankTransferMessage), input_name='bankTransferMessage')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'amountTotalInEuroCents' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'amountTotalInEuroCents')
            if ival_ <= 0:
                raise_parse_error(child_, 'requires positiveInteger')
            ival_ = self.gds_validate_integer(ival_, node, 'amountTotalInEuroCents')
            self.amountTotalInEuroCents = ival_
            self.amountTotalInEuroCents_nsprefix_ = child_.prefix
        elif nodeName_ == 'bban':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'bban')
            value_ = self.gds_validate_string(value_, node, 'bban')
            self.bban = value_
            self.bban_nsprefix_ = child_.prefix
            # validate type bbanType
            self.validate_bbanType(self.bban)
        elif nodeName_ == 'iban':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'iban')
            value_ = self.gds_validate_string(value_, node, 'iban')
            self.iban = value_
            self.iban_nsprefix_ = child_.prefix
            # validate type belgianIbanType
            self.validate_belgianIbanType(self.iban)
        elif nodeName_ == 'bic':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'bic')
            value_ = self.gds_validate_string(value_, node, 'bic')
            self.bic = value_
            self.bic_nsprefix_ = child_.prefix
            # validate type bicType
            self.validate_bicType(self.bic)
        elif nodeName_ == 'bankTransferMessage':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'bankTransferMessage')
            value_ = self.gds_validate_string(value_, node, 'bankTransferMessage')
            self.bankTransferMessage = value_
            self.bankTransferMessage_nsprefix_ = child_.prefix
            # validate type bankTransferMessageType
            self.validate_bankTransferMessageType(self.bankTransferMessage)
# end class cashOnDeliveryType


class atHomeType(GeneratedsSuper):
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
                CurrentSubclassModule_, atHomeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if atHomeType.subclass:
            return atHomeType.subclass(*args_, **kwargs_)
        else:
            return atHomeType(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='atHomeType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('atHomeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'atHomeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='atHomeType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='atHomeType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='atHomeType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='atHomeType', fromsubclass_=False, pretty_print=True):
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
# end class atHomeType


class atShopType(notificationType):
    """pickupLocatorId -- The Taxipost Pick-up locator ID
    shopHandlingInstruction -- Free text message that will be shown in the shop point on the Mobile App
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = notificationType
    def __init__(self, language=None, emailAddress=None, smsNumber=None, voiceNumber=None, messageType=None, pickupLocatorId=None, shopHandlingInstruction=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("atShopType"), self).__init__(language, emailAddress, smsNumber, voiceNumber, messageType,  **kwargs_)
        self.pickupLocatorId = pickupLocatorId
        self.validate_pickupLocatorIdType(self.pickupLocatorId)
        self.pickupLocatorId_nsprefix_ = None
        self.shopHandlingInstruction = shopHandlingInstruction
        self.validate_shopHandlingInstructionType(self.shopHandlingInstruction)
        self.shopHandlingInstruction_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, atShopType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if atShopType.subclass:
            return atShopType.subclass(*args_, **kwargs_)
        else:
            return atShopType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_pickupLocatorId(self):
        return self.pickupLocatorId
    def set_pickupLocatorId(self, pickupLocatorId):
        self.pickupLocatorId = pickupLocatorId
    def get_shopHandlingInstruction(self):
        return self.shopHandlingInstruction
    def set_shopHandlingInstruction(self, shopHandlingInstruction):
        self.shopHandlingInstruction = shopHandlingInstruction
    def validate_pickupLocatorIdType(self, value):
        result = True
        # Validate type pickupLocatorIdType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on pickupLocatorIdType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on pickupLocatorIdType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_pickupLocatorIdType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_pickupLocatorIdType_patterns_, ))
                result = False
        return result
    validate_pickupLocatorIdType_patterns_ = [['^([A-Za-z0-9]*)$']]
    def validate_shopHandlingInstructionType(self, value):
        result = True
        # Validate type shopHandlingInstructionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on shopHandlingInstructionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on shopHandlingInstructionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.pickupLocatorId is not None or
            self.shopHandlingInstruction is not None or
            super(atShopType, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='atShopType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('atShopType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'atShopType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='atShopType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='atShopType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='atShopType'):
        super(atShopType, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='atShopType')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='atShopType', fromsubclass_=False, pretty_print=True):
        super(atShopType, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.pickupLocatorId is not None:
            namespaceprefix_ = self.pickupLocatorId_nsprefix_ + ':' if (UseCapturedNS_ and self.pickupLocatorId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spickupLocatorId>%s</%spickupLocatorId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.pickupLocatorId), input_name='pickupLocatorId')), namespaceprefix_ , eol_))
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
        super(atShopType, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'pickupLocatorId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'pickupLocatorId')
            value_ = self.gds_validate_string(value_, node, 'pickupLocatorId')
            self.pickupLocatorId = value_
            self.pickupLocatorId_nsprefix_ = child_.prefix
            # validate type pickupLocatorIdType
            self.validate_pickupLocatorIdType(self.pickupLocatorId)
        elif nodeName_ == 'shopHandlingInstruction':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'shopHandlingInstruction')
            value_ = self.gds_validate_string(value_, node, 'shopHandlingInstruction')
            self.shopHandlingInstruction = value_
            self.shopHandlingInstruction_nsprefix_ = child_.prefix
            # validate type shopHandlingInstructionType
            self.validate_shopHandlingInstructionType(self.shopHandlingInstruction)
        super(atShopType, self)._buildChildren(child_, node, nodeName_, True)
# end class atShopType


class atIntlHomeType(GeneratedsSuper):
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
                CurrentSubclassModule_, atIntlHomeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if atIntlHomeType.subclass:
            return atIntlHomeType.subclass(*args_, **kwargs_)
        else:
            return atIntlHomeType(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='atIntlHomeType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('atIntlHomeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'atIntlHomeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='atIntlHomeType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='atIntlHomeType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='atIntlHomeType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='atIntlHomeType', fromsubclass_=False, pretty_print=True):
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
# end class atIntlHomeType


class atIntlShopType(GeneratedsSuper):
    """pickupLocatorId -- The id of the partner pickup point
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, language=None, emailAddress=None, pickupLocatorId=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.language = _cast(None, language)
        self.language_nsprefix_ = None
        self.emailAddress = emailAddress
        self.validate_emailAddressType(self.emailAddress)
        self.emailAddress_nsprefix_ = None
        self.pickupLocatorId = pickupLocatorId
        self.validate_pickupLocatorIdType2(self.pickupLocatorId)
        self.pickupLocatorId_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, atIntlShopType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if atIntlShopType.subclass:
            return atIntlShopType.subclass(*args_, **kwargs_)
        else:
            return atIntlShopType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_emailAddress(self):
        return self.emailAddress
    def set_emailAddress(self, emailAddress):
        self.emailAddress = emailAddress
    def get_pickupLocatorId(self):
        return self.pickupLocatorId
    def set_pickupLocatorId(self, pickupLocatorId):
        self.pickupLocatorId = pickupLocatorId
    def get_language(self):
        return self.language
    def set_language(self, language):
        self.language = language
    def validate_emailAddressType(self, value):
        result = True
        # Validate type emailAddressType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on emailAddressType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_pickupLocatorIdType2(self, value):
        result = True
        # Validate type pickupLocatorIdType2, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on pickupLocatorIdType2' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on pickupLocatorIdType2' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
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
            self.pickupLocatorId is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='atIntlShopType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('atIntlShopType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'atIntlShopType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='atIntlShopType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='atIntlShopType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='atIntlShopType'):
        if self.language is not None and 'language' not in already_processed:
            already_processed.add('language')
            outfile.write(' language=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.language), input_name='language')), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='atIntlShopType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.emailAddress is not None:
            namespaceprefix_ = self.emailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.emailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%semailAddress>%s</%semailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.emailAddress), input_name='emailAddress')), namespaceprefix_ , eol_))
        if self.pickupLocatorId is not None:
            namespaceprefix_ = self.pickupLocatorId_nsprefix_ + ':' if (UseCapturedNS_ and self.pickupLocatorId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spickupLocatorId>%s</%spickupLocatorId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.pickupLocatorId), input_name='pickupLocatorId')), namespaceprefix_ , eol_))
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
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'emailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'emailAddress')
            value_ = self.gds_validate_string(value_, node, 'emailAddress')
            self.emailAddress = value_
            self.emailAddress_nsprefix_ = child_.prefix
            # validate type emailAddressType
            self.validate_emailAddressType(self.emailAddress)
        elif nodeName_ == 'pickupLocatorId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'pickupLocatorId')
            value_ = self.gds_validate_string(value_, node, 'pickupLocatorId')
            self.pickupLocatorId = value_
            self.pickupLocatorId_nsprefix_ = child_.prefix
            # validate type pickupLocatorIdType2
            self.validate_pickupLocatorIdType2(self.pickupLocatorId)
# end class atIntlShopType


class atIntlParcelDepotType(GeneratedsSuper):
    """parcelsDepotId -- The id of the partner parcel locker
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, language=None, emailAddress=None, smsNumber=None, parcelsDepotId=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.language = _cast(None, language)
        self.language_nsprefix_ = None
        self.emailAddress = emailAddress
        self.validate_emailAddressType(self.emailAddress)
        self.emailAddress_nsprefix_ = None
        self.smsNumber = smsNumber
        self.validate_smsNumberType3(self.smsNumber)
        self.smsNumber_nsprefix_ = None
        self.parcelsDepotId = parcelsDepotId
        self.validate_parcelsDepotIdType(self.parcelsDepotId)
        self.parcelsDepotId_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, atIntlParcelDepotType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if atIntlParcelDepotType.subclass:
            return atIntlParcelDepotType.subclass(*args_, **kwargs_)
        else:
            return atIntlParcelDepotType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_emailAddress(self):
        return self.emailAddress
    def set_emailAddress(self, emailAddress):
        self.emailAddress = emailAddress
    def get_smsNumber(self):
        return self.smsNumber
    def set_smsNumber(self, smsNumber):
        self.smsNumber = smsNumber
    def get_parcelsDepotId(self):
        return self.parcelsDepotId
    def set_parcelsDepotId(self, parcelsDepotId):
        self.parcelsDepotId = parcelsDepotId
    def get_language(self):
        return self.language
    def set_language(self, language):
        self.language = language
    def validate_emailAddressType(self, value):
        result = True
        # Validate type emailAddressType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on emailAddressType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_smsNumberType3(self, value):
        result = True
        # Validate type smsNumberType3, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on smsNumberType3' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on smsNumberType3' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_parcelsDepotIdType(self, value):
        result = True
        # Validate type parcelsDepotIdType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on parcelsDepotIdType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on parcelsDepotIdType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
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
            self.smsNumber is not None or
            self.parcelsDepotId is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='atIntlParcelDepotType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('atIntlParcelDepotType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'atIntlParcelDepotType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='atIntlParcelDepotType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='atIntlParcelDepotType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='atIntlParcelDepotType'):
        if self.language is not None and 'language' not in already_processed:
            already_processed.add('language')
            outfile.write(' language=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.language), input_name='language')), ))
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='atIntlParcelDepotType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.emailAddress is not None:
            namespaceprefix_ = self.emailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.emailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%semailAddress>%s</%semailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.emailAddress), input_name='emailAddress')), namespaceprefix_ , eol_))
        if self.smsNumber is not None:
            namespaceprefix_ = self.smsNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.smsNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssmsNumber>%s</%ssmsNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.smsNumber), input_name='smsNumber')), namespaceprefix_ , eol_))
        if self.parcelsDepotId is not None:
            namespaceprefix_ = self.parcelsDepotId_nsprefix_ + ':' if (UseCapturedNS_ and self.parcelsDepotId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sparcelsDepotId>%s</%sparcelsDepotId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.parcelsDepotId), input_name='parcelsDepotId')), namespaceprefix_ , eol_))
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
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'emailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'emailAddress')
            value_ = self.gds_validate_string(value_, node, 'emailAddress')
            self.emailAddress = value_
            self.emailAddress_nsprefix_ = child_.prefix
            # validate type emailAddressType
            self.validate_emailAddressType(self.emailAddress)
        elif nodeName_ == 'smsNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'smsNumber')
            value_ = self.gds_validate_string(value_, node, 'smsNumber')
            self.smsNumber = value_
            self.smsNumber_nsprefix_ = child_.prefix
            # validate type smsNumberType3
            self.validate_smsNumberType3(self.smsNumber)
        elif nodeName_ == 'parcelsDepotId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'parcelsDepotId')
            value_ = self.gds_validate_string(value_, node, 'parcelsDepotId')
            self.parcelsDepotId = value_
            self.parcelsDepotId_nsprefix_ = child_.prefix
            # validate type parcelsDepotIdType
            self.validate_parcelsDepotIdType(self.parcelsDepotId)
# end class atIntlParcelDepotType


class at24_7Type(GeneratedsSuper):
    """parcelsDepotId -- ID of the pack station
    memberId -- type, length ???
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, parcelsDepotId=None, memberId=None, messageLanguage=None, mobilePhone=None, email=None, reducedMobilityZone=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.parcelsDepotId = parcelsDepotId
        self.validate_parcelsDepotIdType4(self.parcelsDepotId)
        self.parcelsDepotId_nsprefix_ = None
        self.memberId = memberId
        self.validate_memberIdType(self.memberId)
        self.memberId_nsprefix_ = None
        self.messageLanguage = messageLanguage
        self.validate_languageType(self.messageLanguage)
        self.messageLanguage_nsprefix_ = None
        self.mobilePhone = mobilePhone
        self.validate_mobilePhoneType(self.mobilePhone)
        self.mobilePhone_nsprefix_ = None
        self.email = email
        self.validate_emailAddressType(self.email)
        self.email_nsprefix_ = None
        self.reducedMobilityZone = reducedMobilityZone
        self.reducedMobilityZone_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, at24_7Type)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if at24_7Type.subclass:
            return at24_7Type.subclass(*args_, **kwargs_)
        else:
            return at24_7Type(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_parcelsDepotId(self):
        return self.parcelsDepotId
    def set_parcelsDepotId(self, parcelsDepotId):
        self.parcelsDepotId = parcelsDepotId
    def get_memberId(self):
        return self.memberId
    def set_memberId(self, memberId):
        self.memberId = memberId
    def get_messageLanguage(self):
        return self.messageLanguage
    def set_messageLanguage(self, messageLanguage):
        self.messageLanguage = messageLanguage
    def get_mobilePhone(self):
        return self.mobilePhone
    def set_mobilePhone(self, mobilePhone):
        self.mobilePhone = mobilePhone
    def get_email(self):
        return self.email
    def set_email(self, email):
        self.email = email
    def get_reducedMobilityZone(self):
        return self.reducedMobilityZone
    def set_reducedMobilityZone(self, reducedMobilityZone):
        self.reducedMobilityZone = reducedMobilityZone
    def validate_parcelsDepotIdType4(self, value):
        result = True
        # Validate type parcelsDepotIdType4, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on parcelsDepotIdType4' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_memberIdType(self, value):
        result = True
        # Validate type memberIdType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on memberIdType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_languageType(self, value):
        result = True
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
        return result
    def validate_mobilePhoneType(self, value):
        result = True
        # Validate type mobilePhoneType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on mobilePhoneType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_emailAddressType(self, value):
        result = True
        # Validate type emailAddressType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on emailAddressType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.parcelsDepotId is not None or
            self.memberId is not None or
            self.messageLanguage is not None or
            self.mobilePhone is not None or
            self.email is not None or
            self.reducedMobilityZone is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='at24-7Type', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('at24-7Type')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'at24-7Type':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='at24-7Type')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='at24-7Type', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='at24-7Type'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='at24-7Type', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.parcelsDepotId is not None:
            namespaceprefix_ = self.parcelsDepotId_nsprefix_ + ':' if (UseCapturedNS_ and self.parcelsDepotId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sparcelsDepotId>%s</%sparcelsDepotId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.parcelsDepotId), input_name='parcelsDepotId')), namespaceprefix_ , eol_))
        if self.memberId is not None:
            namespaceprefix_ = self.memberId_nsprefix_ + ':' if (UseCapturedNS_ and self.memberId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smemberId>%s</%smemberId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.memberId), input_name='memberId')), namespaceprefix_ , eol_))
        if self.messageLanguage is not None:
            namespaceprefix_ = self.messageLanguage_nsprefix_ + ':' if (UseCapturedNS_ and self.messageLanguage_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smessageLanguage>%s</%smessageLanguage>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.messageLanguage), input_name='messageLanguage')), namespaceprefix_ , eol_))
        if self.mobilePhone is not None:
            namespaceprefix_ = self.mobilePhone_nsprefix_ + ':' if (UseCapturedNS_ and self.mobilePhone_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smobilePhone>%s</%smobilePhone>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.mobilePhone), input_name='mobilePhone')), namespaceprefix_ , eol_))
        if self.email is not None:
            namespaceprefix_ = self.email_nsprefix_ + ':' if (UseCapturedNS_ and self.email_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%semail>%s</%semail>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.email), input_name='email')), namespaceprefix_ , eol_))
        if self.reducedMobilityZone is not None:
            namespaceprefix_ = self.reducedMobilityZone_nsprefix_ + ':' if (UseCapturedNS_ and self.reducedMobilityZone_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sreducedMobilityZone>%s</%sreducedMobilityZone>%s' % (namespaceprefix_ , self.gds_format_boolean(self.reducedMobilityZone, input_name='reducedMobilityZone'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'parcelsDepotId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'parcelsDepotId')
            value_ = self.gds_validate_string(value_, node, 'parcelsDepotId')
            self.parcelsDepotId = value_
            self.parcelsDepotId_nsprefix_ = child_.prefix
            # validate type parcelsDepotIdType4
            self.validate_parcelsDepotIdType4(self.parcelsDepotId)
        elif nodeName_ == 'memberId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'memberId')
            value_ = self.gds_validate_string(value_, node, 'memberId')
            self.memberId = value_
            self.memberId_nsprefix_ = child_.prefix
            # validate type memberIdType
            self.validate_memberIdType(self.memberId)
        elif nodeName_ == 'messageLanguage':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'messageLanguage')
            value_ = self.gds_validate_string(value_, node, 'messageLanguage')
            self.messageLanguage = value_
            self.messageLanguage_nsprefix_ = child_.prefix
            # validate type languageType
            self.validate_languageType(self.messageLanguage)
        elif nodeName_ == 'mobilePhone':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'mobilePhone')
            value_ = self.gds_validate_string(value_, node, 'mobilePhone')
            self.mobilePhone = value_
            self.mobilePhone_nsprefix_ = child_.prefix
            # validate type mobilePhoneType
            self.validate_mobilePhoneType(self.mobilePhone)
        elif nodeName_ == 'email':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'email')
            value_ = self.gds_validate_string(value_, node, 'email')
            self.email = value_
            self.email_nsprefix_ = child_.prefix
            # validate type emailAddressType
            self.validate_emailAddressType(self.email)
        elif nodeName_ == 'reducedMobilityZone':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'reducedMobilityZone')
            ival_ = self.gds_validate_boolean(ival_, node, 'reducedMobilityZone')
            self.reducedMobilityZone = ival_
            self.reducedMobilityZone_nsprefix_ = child_.prefix
# end class at24_7Type


class deliveryMethodType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, atHome=None, atShop=None, at24_7=None, atIntlHome=None, atIntlShop=None, atIntlParcelDepot=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.atHome = atHome
        self.atHome_nsprefix_ = None
        self.atShop = atShop
        self.atShop_nsprefix_ = None
        self.at24_7 = at24_7
        self.at24_7_nsprefix_ = None
        self.atIntlHome = atIntlHome
        self.atIntlHome_nsprefix_ = None
        self.atIntlShop = atIntlShop
        self.atIntlShop_nsprefix_ = None
        self.atIntlParcelDepot = atIntlParcelDepot
        self.atIntlParcelDepot_nsprefix_ = None
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
    def get_atHome(self):
        return self.atHome
    def set_atHome(self, atHome):
        self.atHome = atHome
    def get_atShop(self):
        return self.atShop
    def set_atShop(self, atShop):
        self.atShop = atShop
    def get_at24_7(self):
        return self.at24_7
    def set_at24_7(self, at24_7):
        self.at24_7 = at24_7
    def get_atIntlHome(self):
        return self.atIntlHome
    def set_atIntlHome(self, atIntlHome):
        self.atIntlHome = atIntlHome
    def get_atIntlShop(self):
        return self.atIntlShop
    def set_atIntlShop(self, atIntlShop):
        self.atIntlShop = atIntlShop
    def get_atIntlParcelDepot(self):
        return self.atIntlParcelDepot
    def set_atIntlParcelDepot(self, atIntlParcelDepot):
        self.atIntlParcelDepot = atIntlParcelDepot
    def has__content(self):
        if (
            self.atHome is not None or
            self.atShop is not None or
            self.at24_7 is not None or
            self.atIntlHome is not None or
            self.atIntlShop is not None or
            self.atIntlParcelDepot is not None
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
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='deliveryMethodType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.atHome is not None:
            namespaceprefix_ = self.atHome_nsprefix_ + ':' if (UseCapturedNS_ and self.atHome_nsprefix_) else ''
            self.atHome.export(outfile, level, namespaceprefix_, namespacedef_='', name_='atHome', pretty_print=pretty_print)
        if self.atShop is not None:
            namespaceprefix_ = self.atShop_nsprefix_ + ':' if (UseCapturedNS_ and self.atShop_nsprefix_) else ''
            self.atShop.export(outfile, level, namespaceprefix_, namespacedef_='', name_='atShop', pretty_print=pretty_print)
        if self.at24_7 is not None:
            namespaceprefix_ = self.at24_7_nsprefix_ + ':' if (UseCapturedNS_ and self.at24_7_nsprefix_) else ''
            self.at24_7.export(outfile, level, namespaceprefix_, namespacedef_='', name_='at24-7', pretty_print=pretty_print)
        if self.atIntlHome is not None:
            namespaceprefix_ = self.atIntlHome_nsprefix_ + ':' if (UseCapturedNS_ and self.atIntlHome_nsprefix_) else ''
            self.atIntlHome.export(outfile, level, namespaceprefix_, namespacedef_='', name_='atIntlHome', pretty_print=pretty_print)
        if self.atIntlShop is not None:
            namespaceprefix_ = self.atIntlShop_nsprefix_ + ':' if (UseCapturedNS_ and self.atIntlShop_nsprefix_) else ''
            self.atIntlShop.export(outfile, level, namespaceprefix_, namespacedef_='', name_='atIntlShop', pretty_print=pretty_print)
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
        if nodeName_ == 'atHome':
            obj_ = atHomeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.atHome = obj_
            obj_.original_tagname_ = 'atHome'
        elif nodeName_ == 'atShop':
            obj_ = atShopType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.atShop = obj_
            obj_.original_tagname_ = 'atShop'
        elif nodeName_ == 'at24-7':
            obj_ = at24_7Type.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.at24_7 = obj_
            obj_.original_tagname_ = 'at24-7'
        elif nodeName_ == 'atIntlHome':
            obj_ = atIntlHomeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.atIntlHome = obj_
            obj_.original_tagname_ = 'atIntlHome'
        elif nodeName_ == 'atIntlShop':
            obj_ = atIntlShopType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.atIntlShop = obj_
            obj_.original_tagname_ = 'atIntlShop'
        elif nodeName_ == 'atIntlParcelDepot':
            obj_ = atIntlParcelDepotType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.atIntlParcelDepot = obj_
            obj_.original_tagname_ = 'atIntlParcelDepot'
# end class deliveryMethodType


class multicolliType(GeneratedsSuper):
    """multicolliId -- Multicolli ID sent from senders for deliverying the items in group
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, multicolliId=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.multicolliId = multicolliId
        self.validate_multicolliIdType(self.multicolliId)
        self.multicolliId_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, multicolliType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if multicolliType.subclass:
            return multicolliType.subclass(*args_, **kwargs_)
        else:
            return multicolliType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_multicolliId(self):
        return self.multicolliId
    def set_multicolliId(self, multicolliId):
        self.multicolliId = multicolliId
    def validate_multicolliIdType(self, value):
        result = True
        # Validate type multicolliIdType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on multicolliIdType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on multicolliIdType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.multicolliId is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='multicolliType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('multicolliType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'multicolliType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='multicolliType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='multicolliType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='multicolliType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='multicolliType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.multicolliId is not None:
            namespaceprefix_ = self.multicolliId_nsprefix_ + ':' if (UseCapturedNS_ and self.multicolliId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smulticolliId>%s</%smulticolliId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.multicolliId), input_name='multicolliId')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'multicolliId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'multicolliId')
            value_ = self.gds_validate_string(value_, node, 'multicolliId')
            self.multicolliId = value_
            self.multicolliId_nsprefix_ = child_.prefix
            # validate type multicolliIdType
            self.validate_multicolliIdType(self.multicolliId)
# end class multicolliType


class automaticSecondPresentationType(GeneratedsSuper):
    """automaticSecondPresentationType -- The item will be presented
    
    """
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


class desktopDeliveryType(GeneratedsSuper):
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
                CurrentSubclassModule_, desktopDeliveryType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if desktopDeliveryType.subclass:
            return desktopDeliveryType.subclass(*args_, **kwargs_)
        else:
            return desktopDeliveryType(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='desktopDeliveryType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('desktopDeliveryType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'desktopDeliveryType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='desktopDeliveryType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='desktopDeliveryType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='desktopDeliveryType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='desktopDeliveryType', fromsubclass_=False, pretty_print=True):
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
# end class desktopDeliveryType


class repairLogisticsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, labelPrintedBybPost=False, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.labelPrintedBybPost = _cast(bool, labelPrintedBybPost)
        self.labelPrintedBybPost_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, repairLogisticsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if repairLogisticsType.subclass:
            return repairLogisticsType.subclass(*args_, **kwargs_)
        else:
            return repairLogisticsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_labelPrintedBybPost(self):
        return self.labelPrintedBybPost
    def set_labelPrintedBybPost(self, labelPrintedBybPost):
        self.labelPrintedBybPost = labelPrintedBybPost
    def has__content(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='repairLogisticsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('repairLogisticsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'repairLogisticsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='repairLogisticsType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='repairLogisticsType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='repairLogisticsType'):
        if self.labelPrintedBybPost and 'labelPrintedBybPost' not in already_processed:
            already_processed.add('labelPrintedBybPost')
            outfile.write(' labelPrintedBybPost="%s"' % self.gds_format_boolean(self.labelPrintedBybPost, input_name='labelPrintedBybPost'))
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='repairLogisticsType', fromsubclass_=False, pretty_print=True):
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
        value = find_attr_value_('labelPrintedBybPost', node)
        if value is not None and 'labelPrintedBybPost' not in already_processed:
            already_processed.add('labelPrintedBybPost')
            if value in ('true', '1'):
                self.labelPrintedBybPost = True
            elif value in ('false', '0'):
                self.labelPrintedBybPost = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class repairLogisticsType


class optionsType(GeneratedsSuper):
    """startRoundNotification -- Send a message to the receiver with an estimated delivery time when the round starts
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, signature=None, signaturePlus=None, insurance=None, cashOnDelivery=None, infoDistributed=None, infoNextDay=None, infoReminder=None, startRoundNotification=None, multicolli=None, automaticSecondPresentation=None, desktopDelivery=None, repairLogistics=None, morningDelivery=None, saturdayDelivery=None, sundayDelivery=None, timeslotDelivery=None, sameDayEveningDelivery=None, ultraLateInEveningDelivery=None, pickupDate=None, timeWindow=None, fragile=None, eveningPickup=None, printLabelAtOffice=None, preferredDelivery=None, deliveryWindow=None, deliveryService=None, proofOfDelivery=None, RP=None, shippingCost=None, dayPickup=None, estimatedDropOff=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.signature = signature
        self.signature_nsprefix_ = None
        self.signaturePlus = signaturePlus
        self.signaturePlus_nsprefix_ = None
        self.insurance = insurance
        self.insurance_nsprefix_ = None
        self.cashOnDelivery = cashOnDelivery
        self.cashOnDelivery_nsprefix_ = None
        self.infoDistributed = infoDistributed
        self.infoDistributed_nsprefix_ = None
        self.infoNextDay = infoNextDay
        self.infoNextDay_nsprefix_ = None
        self.infoReminder = infoReminder
        self.infoReminder_nsprefix_ = None
        self.startRoundNotification = startRoundNotification
        self.startRoundNotification_nsprefix_ = None
        self.multicolli = multicolli
        self.multicolli_nsprefix_ = None
        self.automaticSecondPresentation = automaticSecondPresentation
        self.automaticSecondPresentation_nsprefix_ = None
        self.desktopDelivery = desktopDelivery
        self.desktopDelivery_nsprefix_ = None
        self.repairLogistics = repairLogistics
        self.repairLogistics_nsprefix_ = None
        self.morningDelivery = morningDelivery
        self.morningDelivery_nsprefix_ = None
        self.saturdayDelivery = saturdayDelivery
        self.saturdayDelivery_nsprefix_ = None
        self.sundayDelivery = sundayDelivery
        self.sundayDelivery_nsprefix_ = None
        self.timeslotDelivery = timeslotDelivery
        self.timeslotDelivery_nsprefix_ = None
        self.sameDayEveningDelivery = sameDayEveningDelivery
        self.sameDayEveningDelivery_nsprefix_ = None
        self.ultraLateInEveningDelivery = ultraLateInEveningDelivery
        self.ultraLateInEveningDelivery_nsprefix_ = None
        if isinstance(pickupDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(pickupDate, '%Y-%m-%d').date()
        else:
            initvalue_ = pickupDate
        self.pickupDate = initvalue_
        self.pickupDate_nsprefix_ = None
        self.timeWindow = timeWindow
        self.validate_timeWindowType(self.timeWindow)
        self.timeWindow_nsprefix_ = None
        self.fragile = fragile
        self.fragile_nsprefix_ = None
        self.eveningPickup = eveningPickup
        self.eveningPickup_nsprefix_ = None
        self.printLabelAtOffice = printLabelAtOffice
        self.printLabelAtOffice_nsprefix_ = None
        self.preferredDelivery = preferredDelivery
        self.preferredDelivery_nsprefix_ = None
        self.deliveryWindow = deliveryWindow
        self.validate_deliveryTimeFrame(self.deliveryWindow)
        self.deliveryWindow_nsprefix_ = None
        self.deliveryService = deliveryService
        self.deliveryService_nsprefix_ = None
        self.proofOfDelivery = proofOfDelivery
        self.proofOfDelivery_nsprefix_ = None
        self.RP = RP
        self.RP_nsprefix_ = None
        self.shippingCost = shippingCost
        self.shippingCost_nsprefix_ = None
        self.dayPickup = dayPickup
        self.dayPickup_nsprefix_ = None
        self.estimatedDropOff = estimatedDropOff
        self.estimatedDropOff_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, optionsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if optionsType.subclass:
            return optionsType.subclass(*args_, **kwargs_)
        else:
            return optionsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_signature(self):
        return self.signature
    def set_signature(self, signature):
        self.signature = signature
    def get_signaturePlus(self):
        return self.signaturePlus
    def set_signaturePlus(self, signaturePlus):
        self.signaturePlus = signaturePlus
    def get_insurance(self):
        return self.insurance
    def set_insurance(self, insurance):
        self.insurance = insurance
    def get_cashOnDelivery(self):
        return self.cashOnDelivery
    def set_cashOnDelivery(self, cashOnDelivery):
        self.cashOnDelivery = cashOnDelivery
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
    def get_startRoundNotification(self):
        return self.startRoundNotification
    def set_startRoundNotification(self, startRoundNotification):
        self.startRoundNotification = startRoundNotification
    def get_multicolli(self):
        return self.multicolli
    def set_multicolli(self, multicolli):
        self.multicolli = multicolli
    def get_automaticSecondPresentation(self):
        return self.automaticSecondPresentation
    def set_automaticSecondPresentation(self, automaticSecondPresentation):
        self.automaticSecondPresentation = automaticSecondPresentation
    def get_desktopDelivery(self):
        return self.desktopDelivery
    def set_desktopDelivery(self, desktopDelivery):
        self.desktopDelivery = desktopDelivery
    def get_repairLogistics(self):
        return self.repairLogistics
    def set_repairLogistics(self, repairLogistics):
        self.repairLogistics = repairLogistics
    def get_morningDelivery(self):
        return self.morningDelivery
    def set_morningDelivery(self, morningDelivery):
        self.morningDelivery = morningDelivery
    def get_saturdayDelivery(self):
        return self.saturdayDelivery
    def set_saturdayDelivery(self, saturdayDelivery):
        self.saturdayDelivery = saturdayDelivery
    def get_sundayDelivery(self):
        return self.sundayDelivery
    def set_sundayDelivery(self, sundayDelivery):
        self.sundayDelivery = sundayDelivery
    def get_timeslotDelivery(self):
        return self.timeslotDelivery
    def set_timeslotDelivery(self, timeslotDelivery):
        self.timeslotDelivery = timeslotDelivery
    def get_sameDayEveningDelivery(self):
        return self.sameDayEveningDelivery
    def set_sameDayEveningDelivery(self, sameDayEveningDelivery):
        self.sameDayEveningDelivery = sameDayEveningDelivery
    def get_ultraLateInEveningDelivery(self):
        return self.ultraLateInEveningDelivery
    def set_ultraLateInEveningDelivery(self, ultraLateInEveningDelivery):
        self.ultraLateInEveningDelivery = ultraLateInEveningDelivery
    def get_pickupDate(self):
        return self.pickupDate
    def set_pickupDate(self, pickupDate):
        self.pickupDate = pickupDate
    def get_timeWindow(self):
        return self.timeWindow
    def set_timeWindow(self, timeWindow):
        self.timeWindow = timeWindow
    def get_fragile(self):
        return self.fragile
    def set_fragile(self, fragile):
        self.fragile = fragile
    def get_eveningPickup(self):
        return self.eveningPickup
    def set_eveningPickup(self, eveningPickup):
        self.eveningPickup = eveningPickup
    def get_printLabelAtOffice(self):
        return self.printLabelAtOffice
    def set_printLabelAtOffice(self, printLabelAtOffice):
        self.printLabelAtOffice = printLabelAtOffice
    def get_preferredDelivery(self):
        return self.preferredDelivery
    def set_preferredDelivery(self, preferredDelivery):
        self.preferredDelivery = preferredDelivery
    def get_deliveryWindow(self):
        return self.deliveryWindow
    def set_deliveryWindow(self, deliveryWindow):
        self.deliveryWindow = deliveryWindow
    def get_deliveryService(self):
        return self.deliveryService
    def set_deliveryService(self, deliveryService):
        self.deliveryService = deliveryService
    def get_proofOfDelivery(self):
        return self.proofOfDelivery
    def set_proofOfDelivery(self, proofOfDelivery):
        self.proofOfDelivery = proofOfDelivery
    def get_RP(self):
        return self.RP
    def set_RP(self, RP):
        self.RP = RP
    def get_shippingCost(self):
        return self.shippingCost
    def set_shippingCost(self, shippingCost):
        self.shippingCost = shippingCost
    def get_dayPickup(self):
        return self.dayPickup
    def set_dayPickup(self, dayPickup):
        self.dayPickup = dayPickup
    def get_estimatedDropOff(self):
        return self.estimatedDropOff
    def set_estimatedDropOff(self, estimatedDropOff):
        self.estimatedDropOff = estimatedDropOff
    def validate_timeWindowType(self, value):
        result = True
        # Validate type timeWindowType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 11:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on timeWindowType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_deliveryTimeFrame(self, value):
        result = True
        # Validate type deliveryTimeFrame, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['AM', 'PM', 'PMPLUS', 'OFFICE']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on deliveryTimeFrame' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.signature is not None or
            self.signaturePlus is not None or
            self.insurance is not None or
            self.cashOnDelivery is not None or
            self.infoDistributed is not None or
            self.infoNextDay is not None or
            self.infoReminder is not None or
            self.startRoundNotification is not None or
            self.multicolli is not None or
            self.automaticSecondPresentation is not None or
            self.desktopDelivery is not None or
            self.repairLogistics is not None or
            self.morningDelivery is not None or
            self.saturdayDelivery is not None or
            self.sundayDelivery is not None or
            self.timeslotDelivery is not None or
            self.sameDayEveningDelivery is not None or
            self.ultraLateInEveningDelivery is not None or
            self.pickupDate is not None or
            self.timeWindow is not None or
            self.fragile is not None or
            self.eveningPickup is not None or
            self.printLabelAtOffice is not None or
            self.preferredDelivery is not None or
            self.deliveryWindow is not None or
            self.deliveryService is not None or
            self.proofOfDelivery is not None or
            self.RP is not None or
            self.shippingCost is not None or
            self.dayPickup is not None or
            self.estimatedDropOff is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='optionsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('optionsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'optionsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='optionsType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='optionsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='optionsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='optionsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.signature is not None:
            namespaceprefix_ = self.signature_nsprefix_ + ':' if (UseCapturedNS_ and self.signature_nsprefix_) else ''
            self.signature.export(outfile, level, namespaceprefix_, namespacedef_='', name_='signature', pretty_print=pretty_print)
        if self.signaturePlus is not None:
            namespaceprefix_ = self.signaturePlus_nsprefix_ + ':' if (UseCapturedNS_ and self.signaturePlus_nsprefix_) else ''
            self.signaturePlus.export(outfile, level, namespaceprefix_, namespacedef_='', name_='signaturePlus', pretty_print=pretty_print)
        if self.insurance is not None:
            namespaceprefix_ = self.insurance_nsprefix_ + ':' if (UseCapturedNS_ and self.insurance_nsprefix_) else ''
            self.insurance.export(outfile, level, namespaceprefix_, namespacedef_='', name_='insurance', pretty_print=pretty_print)
        if self.cashOnDelivery is not None:
            namespaceprefix_ = self.cashOnDelivery_nsprefix_ + ':' if (UseCapturedNS_ and self.cashOnDelivery_nsprefix_) else ''
            self.cashOnDelivery.export(outfile, level, namespaceprefix_, namespacedef_='', name_='cashOnDelivery', pretty_print=pretty_print)
        if self.infoDistributed is not None:
            namespaceprefix_ = self.infoDistributed_nsprefix_ + ':' if (UseCapturedNS_ and self.infoDistributed_nsprefix_) else ''
            self.infoDistributed.export(outfile, level, namespaceprefix_, namespacedef_='', name_='infoDistributed', pretty_print=pretty_print)
        if self.infoNextDay is not None:
            namespaceprefix_ = self.infoNextDay_nsprefix_ + ':' if (UseCapturedNS_ and self.infoNextDay_nsprefix_) else ''
            self.infoNextDay.export(outfile, level, namespaceprefix_, namespacedef_='', name_='infoNextDay', pretty_print=pretty_print)
        if self.infoReminder is not None:
            namespaceprefix_ = self.infoReminder_nsprefix_ + ':' if (UseCapturedNS_ and self.infoReminder_nsprefix_) else ''
            self.infoReminder.export(outfile, level, namespaceprefix_, namespacedef_='', name_='infoReminder', pretty_print=pretty_print)
        if self.startRoundNotification is not None:
            namespaceprefix_ = self.startRoundNotification_nsprefix_ + ':' if (UseCapturedNS_ and self.startRoundNotification_nsprefix_) else ''
            self.startRoundNotification.export(outfile, level, namespaceprefix_, namespacedef_='', name_='startRoundNotification', pretty_print=pretty_print)
        if self.multicolli is not None:
            namespaceprefix_ = self.multicolli_nsprefix_ + ':' if (UseCapturedNS_ and self.multicolli_nsprefix_) else ''
            self.multicolli.export(outfile, level, namespaceprefix_, namespacedef_='', name_='multicolli', pretty_print=pretty_print)
        if self.automaticSecondPresentation is not None:
            namespaceprefix_ = self.automaticSecondPresentation_nsprefix_ + ':' if (UseCapturedNS_ and self.automaticSecondPresentation_nsprefix_) else ''
            self.automaticSecondPresentation.export(outfile, level, namespaceprefix_, namespacedef_='', name_='automaticSecondPresentation', pretty_print=pretty_print)
        if self.desktopDelivery is not None:
            namespaceprefix_ = self.desktopDelivery_nsprefix_ + ':' if (UseCapturedNS_ and self.desktopDelivery_nsprefix_) else ''
            self.desktopDelivery.export(outfile, level, namespaceprefix_, namespacedef_='', name_='desktopDelivery', pretty_print=pretty_print)
        if self.repairLogistics is not None:
            namespaceprefix_ = self.repairLogistics_nsprefix_ + ':' if (UseCapturedNS_ and self.repairLogistics_nsprefix_) else ''
            self.repairLogistics.export(outfile, level, namespaceprefix_, namespacedef_='', name_='repairLogistics', pretty_print=pretty_print)
        if self.morningDelivery is not None:
            namespaceprefix_ = self.morningDelivery_nsprefix_ + ':' if (UseCapturedNS_ and self.morningDelivery_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smorningDelivery>%s</%smorningDelivery>%s' % (namespaceprefix_ , self.gds_format_boolean(self.morningDelivery, input_name='morningDelivery'), namespaceprefix_ , eol_))
        if self.saturdayDelivery is not None:
            namespaceprefix_ = self.saturdayDelivery_nsprefix_ + ':' if (UseCapturedNS_ and self.saturdayDelivery_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssaturdayDelivery>%s</%ssaturdayDelivery>%s' % (namespaceprefix_ , self.gds_format_boolean(self.saturdayDelivery, input_name='saturdayDelivery'), namespaceprefix_ , eol_))
        if self.sundayDelivery is not None:
            namespaceprefix_ = self.sundayDelivery_nsprefix_ + ':' if (UseCapturedNS_ and self.sundayDelivery_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssundayDelivery>%s</%ssundayDelivery>%s' % (namespaceprefix_ , self.gds_format_boolean(self.sundayDelivery, input_name='sundayDelivery'), namespaceprefix_ , eol_))
        if self.timeslotDelivery is not None:
            namespaceprefix_ = self.timeslotDelivery_nsprefix_ + ':' if (UseCapturedNS_ and self.timeslotDelivery_nsprefix_) else ''
            self.timeslotDelivery.export(outfile, level, namespaceprefix_, namespacedef_='', name_='timeslotDelivery', pretty_print=pretty_print)
        if self.sameDayEveningDelivery is not None:
            namespaceprefix_ = self.sameDayEveningDelivery_nsprefix_ + ':' if (UseCapturedNS_ and self.sameDayEveningDelivery_nsprefix_) else ''
            self.sameDayEveningDelivery.export(outfile, level, namespaceprefix_, namespacedef_='', name_='sameDayEveningDelivery', pretty_print=pretty_print)
        if self.ultraLateInEveningDelivery is not None:
            namespaceprefix_ = self.ultraLateInEveningDelivery_nsprefix_ + ':' if (UseCapturedNS_ and self.ultraLateInEveningDelivery_nsprefix_) else ''
            self.ultraLateInEveningDelivery.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ultraLateInEveningDelivery', pretty_print=pretty_print)
        if self.pickupDate is not None:
            namespaceprefix_ = self.pickupDate_nsprefix_ + ':' if (UseCapturedNS_ and self.pickupDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spickupDate>%s</%spickupDate>%s' % (namespaceprefix_ , self.gds_format_date(self.pickupDate, input_name='pickupDate'), namespaceprefix_ , eol_))
        if self.timeWindow is not None:
            namespaceprefix_ = self.timeWindow_nsprefix_ + ':' if (UseCapturedNS_ and self.timeWindow_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stimeWindow>%s</%stimeWindow>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.timeWindow), input_name='timeWindow')), namespaceprefix_ , eol_))
        if self.fragile is not None:
            namespaceprefix_ = self.fragile_nsprefix_ + ':' if (UseCapturedNS_ and self.fragile_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sfragile>%s</%sfragile>%s' % (namespaceprefix_ , self.gds_format_boolean(self.fragile, input_name='fragile'), namespaceprefix_ , eol_))
        if self.eveningPickup is not None:
            namespaceprefix_ = self.eveningPickup_nsprefix_ + ':' if (UseCapturedNS_ and self.eveningPickup_nsprefix_) else ''
            self.eveningPickup.export(outfile, level, namespaceprefix_, namespacedef_='', name_='eveningPickup', pretty_print=pretty_print)
        if self.printLabelAtOffice is not None:
            namespaceprefix_ = self.printLabelAtOffice_nsprefix_ + ':' if (UseCapturedNS_ and self.printLabelAtOffice_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sprintLabelAtOffice>%s</%sprintLabelAtOffice>%s' % (namespaceprefix_ , self.gds_format_boolean(self.printLabelAtOffice, input_name='printLabelAtOffice'), namespaceprefix_ , eol_))
        if self.preferredDelivery is not None:
            namespaceprefix_ = self.preferredDelivery_nsprefix_ + ':' if (UseCapturedNS_ and self.preferredDelivery_nsprefix_) else ''
            self.preferredDelivery.export(outfile, level, namespaceprefix_, namespacedef_='', name_='preferredDelivery', pretty_print=pretty_print)
        if self.deliveryWindow is not None:
            namespaceprefix_ = self.deliveryWindow_nsprefix_ + ':' if (UseCapturedNS_ and self.deliveryWindow_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdeliveryWindow>%s</%sdeliveryWindow>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.deliveryWindow), input_name='deliveryWindow')), namespaceprefix_ , eol_))
        if self.deliveryService is not None:
            namespaceprefix_ = self.deliveryService_nsprefix_ + ':' if (UseCapturedNS_ and self.deliveryService_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdeliveryService>%s</%sdeliveryService>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.deliveryService), input_name='deliveryService')), namespaceprefix_ , eol_))
        if self.proofOfDelivery is not None:
            namespaceprefix_ = self.proofOfDelivery_nsprefix_ + ':' if (UseCapturedNS_ and self.proofOfDelivery_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sproofOfDelivery>%s</%sproofOfDelivery>%s' % (namespaceprefix_ , self.gds_format_boolean(self.proofOfDelivery, input_name='proofOfDelivery'), namespaceprefix_ , eol_))
        if self.RP is not None:
            namespaceprefix_ = self.RP_nsprefix_ + ':' if (UseCapturedNS_ and self.RP_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRP>%s</%sRP>%s' % (namespaceprefix_ , self.gds_format_boolean(self.RP, input_name='RP'), namespaceprefix_ , eol_))
        if self.shippingCost is not None:
            namespaceprefix_ = self.shippingCost_nsprefix_ + ':' if (UseCapturedNS_ and self.shippingCost_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sshippingCost>%s</%sshippingCost>%s' % (namespaceprefix_ , self.gds_format_decimal(self.shippingCost, input_name='shippingCost'), namespaceprefix_ , eol_))
        if self.dayPickup is not None:
            namespaceprefix_ = self.dayPickup_nsprefix_ + ':' if (UseCapturedNS_ and self.dayPickup_nsprefix_) else ''
            self.dayPickup.export(outfile, level, namespaceprefix_, namespacedef_='', name_='dayPickup', pretty_print=pretty_print)
        if self.estimatedDropOff is not None:
            namespaceprefix_ = self.estimatedDropOff_nsprefix_ + ':' if (UseCapturedNS_ and self.estimatedDropOff_nsprefix_) else ''
            self.estimatedDropOff.export(outfile, level, namespaceprefix_, namespacedef_='', name_='estimatedDropOff', pretty_print=pretty_print)
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
        if nodeName_ == 'signature':
            obj_ = signatureType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.signature = obj_
            obj_.original_tagname_ = 'signature'
        elif nodeName_ == 'signaturePlus':
            obj_ = signaturePlusType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.signaturePlus = obj_
            obj_.original_tagname_ = 'signaturePlus'
        elif nodeName_ == 'insurance':
            obj_ = insuranceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.insurance = obj_
            obj_.original_tagname_ = 'insurance'
        elif nodeName_ == 'cashOnDelivery':
            obj_ = cashOnDeliveryType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.cashOnDelivery = obj_
            obj_.original_tagname_ = 'cashOnDelivery'
        elif nodeName_ == 'infoDistributed':
            class_obj_ = self.get_class_obj_(child_, notificationType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.infoDistributed = obj_
            obj_.original_tagname_ = 'infoDistributed'
        elif nodeName_ == 'infoNextDay':
            class_obj_ = self.get_class_obj_(child_, notificationType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.infoNextDay = obj_
            obj_.original_tagname_ = 'infoNextDay'
        elif nodeName_ == 'infoReminder':
            class_obj_ = self.get_class_obj_(child_, notificationType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.infoReminder = obj_
            obj_.original_tagname_ = 'infoReminder'
        elif nodeName_ == 'startRoundNotification':
            class_obj_ = self.get_class_obj_(child_, notificationType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.startRoundNotification = obj_
            obj_.original_tagname_ = 'startRoundNotification'
        elif nodeName_ == 'multicolli':
            obj_ = multicolliType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.multicolli = obj_
            obj_.original_tagname_ = 'multicolli'
        elif nodeName_ == 'automaticSecondPresentation':
            obj_ = automaticSecondPresentationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.automaticSecondPresentation = obj_
            obj_.original_tagname_ = 'automaticSecondPresentation'
        elif nodeName_ == 'desktopDelivery':
            obj_ = desktopDeliveryType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.desktopDelivery = obj_
            obj_.original_tagname_ = 'desktopDelivery'
        elif nodeName_ == 'repairLogistics':
            obj_ = repairLogisticsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.repairLogistics = obj_
            obj_.original_tagname_ = 'repairLogistics'
        elif nodeName_ == 'morningDelivery':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'morningDelivery')
            ival_ = self.gds_validate_boolean(ival_, node, 'morningDelivery')
            self.morningDelivery = ival_
            self.morningDelivery_nsprefix_ = child_.prefix
        elif nodeName_ == 'saturdayDelivery':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'saturdayDelivery')
            ival_ = self.gds_validate_boolean(ival_, node, 'saturdayDelivery')
            self.saturdayDelivery = ival_
            self.saturdayDelivery_nsprefix_ = child_.prefix
        elif nodeName_ == 'sundayDelivery':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'sundayDelivery')
            ival_ = self.gds_validate_boolean(ival_, node, 'sundayDelivery')
            self.sundayDelivery = ival_
            self.sundayDelivery_nsprefix_ = child_.prefix
        elif nodeName_ == 'timeslotDelivery':
            obj_ = timeslotDeliveryType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.timeslotDelivery = obj_
            obj_.original_tagname_ = 'timeslotDelivery'
        elif nodeName_ == 'sameDayEveningDelivery':
            obj_ = samedayEveningDeliveryType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.sameDayEveningDelivery = obj_
            obj_.original_tagname_ = 'sameDayEveningDelivery'
        elif nodeName_ == 'ultraLateInEveningDelivery':
            obj_ = ultraLateInEveningDeliveryType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ultraLateInEveningDelivery = obj_
            obj_.original_tagname_ = 'ultraLateInEveningDelivery'
        elif nodeName_ == 'pickupDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.pickupDate = dval_
            self.pickupDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'timeWindow':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'timeWindow')
            value_ = self.gds_validate_string(value_, node, 'timeWindow')
            self.timeWindow = value_
            self.timeWindow_nsprefix_ = child_.prefix
            # validate type timeWindowType
            self.validate_timeWindowType(self.timeWindow)
        elif nodeName_ == 'fragile':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'fragile')
            ival_ = self.gds_validate_boolean(ival_, node, 'fragile')
            self.fragile = ival_
            self.fragile_nsprefix_ = child_.prefix
        elif nodeName_ == 'eveningPickup':
            obj_ = eveningPickupType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.eveningPickup = obj_
            obj_.original_tagname_ = 'eveningPickup'
        elif nodeName_ == 'printLabelAtOffice':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'printLabelAtOffice')
            ival_ = self.gds_validate_boolean(ival_, node, 'printLabelAtOffice')
            self.printLabelAtOffice = ival_
            self.printLabelAtOffice_nsprefix_ = child_.prefix
        elif nodeName_ == 'preferredDelivery':
            obj_ = preferredDeliveryType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.preferredDelivery = obj_
            obj_.original_tagname_ = 'preferredDelivery'
        elif nodeName_ == 'deliveryWindow':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'deliveryWindow')
            value_ = self.gds_validate_string(value_, node, 'deliveryWindow')
            self.deliveryWindow = value_
            self.deliveryWindow_nsprefix_ = child_.prefix
            # validate type deliveryTimeFrame
            self.validate_deliveryTimeFrame(self.deliveryWindow)
        elif nodeName_ == 'deliveryService':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'deliveryService')
            value_ = self.gds_validate_string(value_, node, 'deliveryService')
            self.deliveryService = value_
            self.deliveryService_nsprefix_ = child_.prefix
        elif nodeName_ == 'proofOfDelivery':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'proofOfDelivery')
            ival_ = self.gds_validate_boolean(ival_, node, 'proofOfDelivery')
            self.proofOfDelivery = ival_
            self.proofOfDelivery_nsprefix_ = child_.prefix
        elif nodeName_ == 'RP':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'RP')
            ival_ = self.gds_validate_boolean(ival_, node, 'RP')
            self.RP = ival_
            self.RP_nsprefix_ = child_.prefix
        elif nodeName_ == 'shippingCost' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'shippingCost')
            fval_ = self.gds_validate_decimal(fval_, node, 'shippingCost')
            self.shippingCost = fval_
            self.shippingCost_nsprefix_ = child_.prefix
        elif nodeName_ == 'dayPickup':
            obj_ = dayPickupType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.dayPickup = obj_
            obj_.original_tagname_ = 'dayPickup'
        elif nodeName_ == 'estimatedDropOff':
            obj_ = estimatedDropOffType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.estimatedDropOff = obj_
            obj_.original_tagname_ = 'estimatedDropOff'
# end class optionsType


class eveningPickupType(GeneratedsSuper):
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
                CurrentSubclassModule_, eveningPickupType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if eveningPickupType.subclass:
            return eveningPickupType.subclass(*args_, **kwargs_)
        else:
            return eveningPickupType(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='eveningPickupType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('eveningPickupType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'eveningPickupType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='eveningPickupType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='eveningPickupType', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='eveningPickupType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='eveningPickupType', fromsubclass_=False, pretty_print=True):
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
# end class eveningPickupType


class ultraLateInEveningDeliveryType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, notificationOptions=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.notificationOptions = notificationOptions
        self.notificationOptions_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ultraLateInEveningDeliveryType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ultraLateInEveningDeliveryType.subclass:
            return ultraLateInEveningDeliveryType.subclass(*args_, **kwargs_)
        else:
            return ultraLateInEveningDeliveryType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_notificationOptions(self):
        return self.notificationOptions
    def set_notificationOptions(self, notificationOptions):
        self.notificationOptions = notificationOptions
    def has__content(self):
        if (
            self.notificationOptions is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ultraLateInEveningDeliveryType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ultraLateInEveningDeliveryType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ultraLateInEveningDeliveryType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ultraLateInEveningDeliveryType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ultraLateInEveningDeliveryType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ultraLateInEveningDeliveryType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ultraLateInEveningDeliveryType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.notificationOptions is not None:
            namespaceprefix_ = self.notificationOptions_nsprefix_ + ':' if (UseCapturedNS_ and self.notificationOptions_nsprefix_) else ''
            self.notificationOptions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='notificationOptions', pretty_print=pretty_print)
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
        if nodeName_ == 'notificationOptions':
            class_obj_ = self.get_class_obj_(child_, notificationType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.notificationOptions = obj_
            obj_.original_tagname_ = 'notificationOptions'
# end class ultraLateInEveningDeliveryType


class timeslotDeliveryType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, deliveryTimeslot=None, notificationOptions=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.deliveryTimeslot = deliveryTimeslot
        self.validate_deliveryTimeslotType(self.deliveryTimeslot)
        self.deliveryTimeslot_nsprefix_ = None
        self.notificationOptions = notificationOptions
        self.notificationOptions_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, timeslotDeliveryType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if timeslotDeliveryType.subclass:
            return timeslotDeliveryType.subclass(*args_, **kwargs_)
        else:
            return timeslotDeliveryType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_deliveryTimeslot(self):
        return self.deliveryTimeslot
    def set_deliveryTimeslot(self, deliveryTimeslot):
        self.deliveryTimeslot = deliveryTimeslot
    def get_notificationOptions(self):
        return self.notificationOptions
    def set_notificationOptions(self, notificationOptions):
        self.notificationOptions = notificationOptions
    def validate_deliveryTimeslotType(self, value):
        result = True
        # Validate type deliveryTimeslotType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['AM', 'PM', 'PMPLUS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on deliveryTimeslotType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.deliveryTimeslot is not None or
            self.notificationOptions is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='timeslotDeliveryType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('timeslotDeliveryType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'timeslotDeliveryType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='timeslotDeliveryType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='timeslotDeliveryType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='timeslotDeliveryType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='timeslotDeliveryType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.deliveryTimeslot is not None:
            namespaceprefix_ = self.deliveryTimeslot_nsprefix_ + ':' if (UseCapturedNS_ and self.deliveryTimeslot_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdeliveryTimeslot>%s</%sdeliveryTimeslot>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.deliveryTimeslot), input_name='deliveryTimeslot')), namespaceprefix_ , eol_))
        if self.notificationOptions is not None:
            namespaceprefix_ = self.notificationOptions_nsprefix_ + ':' if (UseCapturedNS_ and self.notificationOptions_nsprefix_) else ''
            self.notificationOptions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='notificationOptions', pretty_print=pretty_print)
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
        if nodeName_ == 'deliveryTimeslot':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'deliveryTimeslot')
            value_ = self.gds_validate_string(value_, node, 'deliveryTimeslot')
            self.deliveryTimeslot = value_
            self.deliveryTimeslot_nsprefix_ = child_.prefix
            # validate type deliveryTimeslotType
            self.validate_deliveryTimeslotType(self.deliveryTimeslot)
        elif nodeName_ == 'notificationOptions':
            class_obj_ = self.get_class_obj_(child_, notificationType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.notificationOptions = obj_
            obj_.original_tagname_ = 'notificationOptions'
# end class timeslotDeliveryType


class samedayEveningDeliveryType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, requestedDeliveryDate=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if isinstance(requestedDeliveryDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(requestedDeliveryDate, '%Y-%m-%d').date()
        else:
            initvalue_ = requestedDeliveryDate
        self.requestedDeliveryDate = initvalue_
        self.requestedDeliveryDate_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, samedayEveningDeliveryType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if samedayEveningDeliveryType.subclass:
            return samedayEveningDeliveryType.subclass(*args_, **kwargs_)
        else:
            return samedayEveningDeliveryType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_requestedDeliveryDate(self):
        return self.requestedDeliveryDate
    def set_requestedDeliveryDate(self, requestedDeliveryDate):
        self.requestedDeliveryDate = requestedDeliveryDate
    def has__content(self):
        if (
            self.requestedDeliveryDate is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='samedayEveningDeliveryType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('samedayEveningDeliveryType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'samedayEveningDeliveryType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='samedayEveningDeliveryType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='samedayEveningDeliveryType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='samedayEveningDeliveryType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='samedayEveningDeliveryType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
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
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'requestedDeliveryDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.requestedDeliveryDate = dval_
            self.requestedDeliveryDate_nsprefix_ = child_.prefix
# end class samedayEveningDeliveryType


class preferredDeliveryType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, preferredDeliveryDate=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if isinstance(preferredDeliveryDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(preferredDeliveryDate, '%Y-%m-%d').date()
        else:
            initvalue_ = preferredDeliveryDate
        self.preferredDeliveryDate = initvalue_
        self.preferredDeliveryDate_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, preferredDeliveryType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if preferredDeliveryType.subclass:
            return preferredDeliveryType.subclass(*args_, **kwargs_)
        else:
            return preferredDeliveryType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_preferredDeliveryDate(self):
        return self.preferredDeliveryDate
    def set_preferredDeliveryDate(self, preferredDeliveryDate):
        self.preferredDeliveryDate = preferredDeliveryDate
    def has__content(self):
        if (
            self.preferredDeliveryDate is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='preferredDeliveryType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('preferredDeliveryType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'preferredDeliveryType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='preferredDeliveryType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='preferredDeliveryType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='preferredDeliveryType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='preferredDeliveryType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.preferredDeliveryDate is not None:
            namespaceprefix_ = self.preferredDeliveryDate_nsprefix_ + ':' if (UseCapturedNS_ and self.preferredDeliveryDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spreferredDeliveryDate>%s</%spreferredDeliveryDate>%s' % (namespaceprefix_ , self.gds_format_date(self.preferredDeliveryDate, input_name='preferredDeliveryDate'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'preferredDeliveryDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.preferredDeliveryDate = dval_
            self.preferredDeliveryDate_nsprefix_ = child_.prefix
# end class preferredDeliveryType


class estimatedDropOffType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, estimatedDropOffStartDate=None, estimatedDropOffEndDate=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if isinstance(estimatedDropOffStartDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(estimatedDropOffStartDate, '%Y-%m-%d').date()
        else:
            initvalue_ = estimatedDropOffStartDate
        self.estimatedDropOffStartDate = initvalue_
        self.estimatedDropOffStartDate_nsprefix_ = None
        if isinstance(estimatedDropOffEndDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(estimatedDropOffEndDate, '%Y-%m-%d').date()
        else:
            initvalue_ = estimatedDropOffEndDate
        self.estimatedDropOffEndDate = initvalue_
        self.estimatedDropOffEndDate_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, estimatedDropOffType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if estimatedDropOffType.subclass:
            return estimatedDropOffType.subclass(*args_, **kwargs_)
        else:
            return estimatedDropOffType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_estimatedDropOffStartDate(self):
        return self.estimatedDropOffStartDate
    def set_estimatedDropOffStartDate(self, estimatedDropOffStartDate):
        self.estimatedDropOffStartDate = estimatedDropOffStartDate
    def get_estimatedDropOffEndDate(self):
        return self.estimatedDropOffEndDate
    def set_estimatedDropOffEndDate(self, estimatedDropOffEndDate):
        self.estimatedDropOffEndDate = estimatedDropOffEndDate
    def has__content(self):
        if (
            self.estimatedDropOffStartDate is not None or
            self.estimatedDropOffEndDate is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='estimatedDropOffType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('estimatedDropOffType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'estimatedDropOffType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='estimatedDropOffType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='estimatedDropOffType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='estimatedDropOffType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='estimatedDropOffType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.estimatedDropOffStartDate is not None:
            namespaceprefix_ = self.estimatedDropOffStartDate_nsprefix_ + ':' if (UseCapturedNS_ and self.estimatedDropOffStartDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sestimatedDropOffStartDate>%s</%sestimatedDropOffStartDate>%s' % (namespaceprefix_ , self.gds_format_date(self.estimatedDropOffStartDate, input_name='estimatedDropOffStartDate'), namespaceprefix_ , eol_))
        if self.estimatedDropOffEndDate is not None:
            namespaceprefix_ = self.estimatedDropOffEndDate_nsprefix_ + ':' if (UseCapturedNS_ and self.estimatedDropOffEndDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sestimatedDropOffEndDate>%s</%sestimatedDropOffEndDate>%s' % (namespaceprefix_ , self.gds_format_date(self.estimatedDropOffEndDate, input_name='estimatedDropOffEndDate'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'estimatedDropOffStartDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.estimatedDropOffStartDate = dval_
            self.estimatedDropOffStartDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'estimatedDropOffEndDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.estimatedDropOffEndDate = dval_
            self.estimatedDropOffEndDate_nsprefix_ = child_.prefix
# end class estimatedDropOffType


class prepaidCharacteristicsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ogonePaymentReference=None, totalItemsPriceInEuroCent=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ogonePaymentReference = ogonePaymentReference
        self.ogonePaymentReference_nsprefix_ = None
        self.totalItemsPriceInEuroCent = totalItemsPriceInEuroCent
        self.totalItemsPriceInEuroCent_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, prepaidCharacteristicsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if prepaidCharacteristicsType.subclass:
            return prepaidCharacteristicsType.subclass(*args_, **kwargs_)
        else:
            return prepaidCharacteristicsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ogonePaymentReference(self):
        return self.ogonePaymentReference
    def set_ogonePaymentReference(self, ogonePaymentReference):
        self.ogonePaymentReference = ogonePaymentReference
    def get_totalItemsPriceInEuroCent(self):
        return self.totalItemsPriceInEuroCent
    def set_totalItemsPriceInEuroCent(self, totalItemsPriceInEuroCent):
        self.totalItemsPriceInEuroCent = totalItemsPriceInEuroCent
    def has__content(self):
        if (
            self.ogonePaymentReference is not None or
            self.totalItemsPriceInEuroCent is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='prepaidCharacteristicsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('prepaidCharacteristicsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'prepaidCharacteristicsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='prepaidCharacteristicsType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='prepaidCharacteristicsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='prepaidCharacteristicsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='prepaidCharacteristicsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ogonePaymentReference is not None:
            namespaceprefix_ = self.ogonePaymentReference_nsprefix_ + ':' if (UseCapturedNS_ and self.ogonePaymentReference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sogonePaymentReference>%s</%sogonePaymentReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ogonePaymentReference), input_name='ogonePaymentReference')), namespaceprefix_ , eol_))
        if self.totalItemsPriceInEuroCent is not None:
            namespaceprefix_ = self.totalItemsPriceInEuroCent_nsprefix_ + ':' if (UseCapturedNS_ and self.totalItemsPriceInEuroCent_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stotalItemsPriceInEuroCent>%s</%stotalItemsPriceInEuroCent>%s' % (namespaceprefix_ , self.gds_format_integer(self.totalItemsPriceInEuroCent, input_name='totalItemsPriceInEuroCent'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ogonePaymentReference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ogonePaymentReference')
            value_ = self.gds_validate_string(value_, node, 'ogonePaymentReference')
            self.ogonePaymentReference = value_
            self.ogonePaymentReference_nsprefix_ = child_.prefix
        elif nodeName_ == 'totalItemsPriceInEuroCent' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'totalItemsPriceInEuroCent')
            ival_ = self.gds_validate_integer(ival_, node, 'totalItemsPriceInEuroCent')
            self.totalItemsPriceInEuroCent = ival_
            self.totalItemsPriceInEuroCent_nsprefix_ = child_.prefix
# end class prepaidCharacteristicsType


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
        self.parcelContent_nsprefix_ = None
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
    valueOfItems -- Value of all pieces of the same type
    itemDescription -- Description of the pieces
    nettoWeight -- The weight of all pieces of the same type
    hsTariffCode -- Harmonized System Tariff code indicating the type of goods for this piece. It should be a text
    field instead of select option
    originOfGoods -- Country of origin of the goods (iso code)
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, numberOfItemType=None, valueOfItems=None, itemDescription=None, nettoWeight=None, hsTariffCode=999999999, originOfGoods=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.numberOfItemType = numberOfItemType
        self.numberOfItemType_nsprefix_ = None
        self.valueOfItems = valueOfItems
        self.valueOfItems_nsprefix_ = None
        self.itemDescription = itemDescription
        self.itemDescription_nsprefix_ = None
        self.nettoWeight = nettoWeight
        self.nettoWeight_nsprefix_ = None
        self.hsTariffCode = hsTariffCode
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
    def get_valueOfItems(self):
        return self.valueOfItems
    def set_valueOfItems(self, valueOfItems):
        self.valueOfItems = valueOfItems
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
            self.valueOfItems is not None or
            self.itemDescription is not None or
            self.nettoWeight is not None or
            self.hsTariffCode != 999999999 or
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
        if self.valueOfItems is not None:
            namespaceprefix_ = self.valueOfItems_nsprefix_ + ':' if (UseCapturedNS_ and self.valueOfItems_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%svalueOfItems>%s</%svalueOfItems>%s' % (namespaceprefix_ , self.gds_format_decimal(self.valueOfItems, input_name='valueOfItems'), namespaceprefix_ , eol_))
        if self.itemDescription is not None:
            namespaceprefix_ = self.itemDescription_nsprefix_ + ':' if (UseCapturedNS_ and self.itemDescription_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sitemDescription>%s</%sitemDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.itemDescription), input_name='itemDescription')), namespaceprefix_ , eol_))
        if self.nettoWeight is not None:
            namespaceprefix_ = self.nettoWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.nettoWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snettoWeight>%s</%snettoWeight>%s' % (namespaceprefix_ , self.gds_format_integer(self.nettoWeight, input_name='nettoWeight'), namespaceprefix_ , eol_))
        if self.hsTariffCode != 999999999:
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
        elif nodeName_ == 'valueOfItems' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'valueOfItems')
            fval_ = self.gds_validate_decimal(fval_, node, 'valueOfItems')
            self.valueOfItems = fval_
            self.valueOfItems_nsprefix_ = child_.prefix
        elif nodeName_ == 'itemDescription':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'itemDescription')
            value_ = self.gds_validate_string(value_, node, 'itemDescription')
            self.itemDescription = value_
            self.itemDescription_nsprefix_ = child_.prefix
        elif nodeName_ == 'nettoWeight' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'nettoWeight')
            ival_ = self.gds_validate_integer(ival_, node, 'nettoWeight')
            self.nettoWeight = ival_
            self.nettoWeight_nsprefix_ = child_.prefix
        elif nodeName_ == 'hsTariffCode' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'hsTariffCode')
            ival_ = self.gds_validate_integer(ival_, node, 'hsTariffCode')
            self.hsTariffCode = ival_
            self.hsTariffCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'originOfGoods':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'originOfGoods')
            value_ = self.gds_validate_string(value_, node, 'originOfGoods')
            self.originOfGoods = value_
            self.originOfGoods_nsprefix_ = child_.prefix
            # validate type originOfGoodsType
            self.validate_originOfGoodsType(self.originOfGoods)
# end class ParcelContentDetail


class dimensionsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, widthInMm=None, heightInMm=None, lengthInMm=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.widthInMm = widthInMm
        self.validate_dimensionType(self.widthInMm)
        self.widthInMm_nsprefix_ = None
        self.heightInMm = heightInMm
        self.validate_dimensionType(self.heightInMm)
        self.heightInMm_nsprefix_ = None
        self.lengthInMm = lengthInMm
        self.validate_dimensionType(self.lengthInMm)
        self.lengthInMm_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, dimensionsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if dimensionsType.subclass:
            return dimensionsType.subclass(*args_, **kwargs_)
        else:
            return dimensionsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_widthInMm(self):
        return self.widthInMm
    def set_widthInMm(self, widthInMm):
        self.widthInMm = widthInMm
    def get_heightInMm(self):
        return self.heightInMm
    def set_heightInMm(self, heightInMm):
        self.heightInMm = heightInMm
    def get_lengthInMm(self):
        return self.lengthInMm
    def set_lengthInMm(self, lengthInMm):
        self.lengthInMm = lengthInMm
    def validate_dimensionType(self, value):
        result = True
        # Validate type dimensionType, a restriction on xs:int.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            if value < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on dimensionType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on dimensionType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.widthInMm is not None or
            self.heightInMm is not None or
            self.lengthInMm is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='dimensionsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('dimensionsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'dimensionsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='dimensionsType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='dimensionsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='dimensionsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='dimensionsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.widthInMm is not None:
            namespaceprefix_ = self.widthInMm_nsprefix_ + ':' if (UseCapturedNS_ and self.widthInMm_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%swidthInMm>%s</%swidthInMm>%s' % (namespaceprefix_ , self.gds_format_integer(self.widthInMm, input_name='widthInMm'), namespaceprefix_ , eol_))
        if self.heightInMm is not None:
            namespaceprefix_ = self.heightInMm_nsprefix_ + ':' if (UseCapturedNS_ and self.heightInMm_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sheightInMm>%s</%sheightInMm>%s' % (namespaceprefix_ , self.gds_format_integer(self.heightInMm, input_name='heightInMm'), namespaceprefix_ , eol_))
        if self.lengthInMm is not None:
            namespaceprefix_ = self.lengthInMm_nsprefix_ + ':' if (UseCapturedNS_ and self.lengthInMm_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slengthInMm>%s</%slengthInMm>%s' % (namespaceprefix_ , self.gds_format_integer(self.lengthInMm, input_name='lengthInMm'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'widthInMm' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'widthInMm')
            ival_ = self.gds_validate_integer(ival_, node, 'widthInMm')
            self.widthInMm = ival_
            self.widthInMm_nsprefix_ = child_.prefix
            # validate type dimensionType
            self.validate_dimensionType(self.widthInMm)
        elif nodeName_ == 'heightInMm' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'heightInMm')
            ival_ = self.gds_validate_integer(ival_, node, 'heightInMm')
            self.heightInMm = ival_
            self.heightInMm_nsprefix_ = child_.prefix
            # validate type dimensionType
            self.validate_dimensionType(self.heightInMm)
        elif nodeName_ == 'lengthInMm' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'lengthInMm')
            ival_ = self.gds_validate_integer(ival_, node, 'lengthInMm')
            self.lengthInMm = ival_
            self.lengthInMm_nsprefix_ = child_.prefix
            # validate type dimensionType
            self.validate_dimensionType(self.lengthInMm)
# end class dimensionsType


class dayPickupType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, pickupDate=None, timeWindow=None, pickupLocation=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if isinstance(pickupDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(pickupDate, '%Y-%m-%d').date()
        else:
            initvalue_ = pickupDate
        self.pickupDate = initvalue_
        self.pickupDate_nsprefix_ = None
        self.timeWindow = timeWindow
        self.validate_timeWindowType(self.timeWindow)
        self.timeWindow_nsprefix_ = None
        self.pickupLocation = pickupLocation
        self.pickupLocation_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, dayPickupType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if dayPickupType.subclass:
            return dayPickupType.subclass(*args_, **kwargs_)
        else:
            return dayPickupType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_pickupDate(self):
        return self.pickupDate
    def set_pickupDate(self, pickupDate):
        self.pickupDate = pickupDate
    def get_timeWindow(self):
        return self.timeWindow
    def set_timeWindow(self, timeWindow):
        self.timeWindow = timeWindow
    def get_pickupLocation(self):
        return self.pickupLocation
    def set_pickupLocation(self, pickupLocation):
        self.pickupLocation = pickupLocation
    def validate_timeWindowType(self, value):
        result = True
        # Validate type timeWindowType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 11:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on timeWindowType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.pickupDate is not None or
            self.timeWindow is not None or
            self.pickupLocation is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='dayPickupType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('dayPickupType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'dayPickupType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='dayPickupType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='dayPickupType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='dayPickupType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='dayPickupType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.pickupDate is not None:
            namespaceprefix_ = self.pickupDate_nsprefix_ + ':' if (UseCapturedNS_ and self.pickupDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spickupDate>%s</%spickupDate>%s' % (namespaceprefix_ , self.gds_format_date(self.pickupDate, input_name='pickupDate'), namespaceprefix_ , eol_))
        if self.timeWindow is not None:
            namespaceprefix_ = self.timeWindow_nsprefix_ + ':' if (UseCapturedNS_ and self.timeWindow_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stimeWindow>%s</%stimeWindow>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.timeWindow), input_name='timeWindow')), namespaceprefix_ , eol_))
        if self.pickupLocation is not None:
            namespaceprefix_ = self.pickupLocation_nsprefix_ + ':' if (UseCapturedNS_ and self.pickupLocation_nsprefix_) else ''
            self.pickupLocation.export(outfile, level, namespaceprefix_, namespacedef_='', name_='pickupLocation', pretty_print=pretty_print)
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
        if nodeName_ == 'pickupDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.pickupDate = dval_
            self.pickupDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'timeWindow':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'timeWindow')
            value_ = self.gds_validate_string(value_, node, 'timeWindow')
            self.timeWindow = value_
            self.timeWindow_nsprefix_ = child_.prefix
            # validate type timeWindowType
            self.validate_timeWindowType(self.timeWindow)
        elif nodeName_ == 'pickupLocation':
            obj_ = pickupLocationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.pickupLocation = obj_
            obj_.original_tagname_ = 'pickupLocation'
# end class dayPickupType


class pickupLocationType(GeneratedsSuper):
    """streetName -- Mandatory according to the LCI-in user manual???
    postalCode -- If the addressee is located in Belgium, the 4 digit postal code should be used.
    countryCode -- The country according to ISO alpha 2 (e.g. BE for Belgium)
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, pickUpName=None, streetName=None, houseNumber=None, boxNumber=None, postalCode=None, city=None, countryCode=None, emailAddress=None, mobileNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.pickUpName = pickUpName
        self.validate_pickUpNameType(self.pickUpName)
        self.pickUpName_nsprefix_ = None
        self.streetName = streetName
        self.validate_streetNameType5(self.streetName)
        self.streetName_nsprefix_ = None
        self.houseNumber = houseNumber
        self.validate_houseNumberType6(self.houseNumber)
        self.houseNumber_nsprefix_ = None
        self.boxNumber = boxNumber
        self.validate_boxNumberType7(self.boxNumber)
        self.boxNumber_nsprefix_ = None
        self.postalCode = postalCode
        self.validate_postalCodeType8(self.postalCode)
        self.postalCode_nsprefix_ = None
        self.city = city
        self.validate_cityType9(self.city)
        self.city_nsprefix_ = None
        self.countryCode = countryCode
        self.validate_countryCodeType10(self.countryCode)
        self.countryCode_nsprefix_ = None
        self.emailAddress = emailAddress
        self.validate_emailAddressType(self.emailAddress)
        self.emailAddress_nsprefix_ = None
        self.mobileNumber = mobileNumber
        self.validate_mobilePhoneType(self.mobileNumber)
        self.mobileNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, pickupLocationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if pickupLocationType.subclass:
            return pickupLocationType.subclass(*args_, **kwargs_)
        else:
            return pickupLocationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_pickUpName(self):
        return self.pickUpName
    def set_pickUpName(self, pickUpName):
        self.pickUpName = pickUpName
    def get_streetName(self):
        return self.streetName
    def set_streetName(self, streetName):
        self.streetName = streetName
    def get_houseNumber(self):
        return self.houseNumber
    def set_houseNumber(self, houseNumber):
        self.houseNumber = houseNumber
    def get_boxNumber(self):
        return self.boxNumber
    def set_boxNumber(self, boxNumber):
        self.boxNumber = boxNumber
    def get_postalCode(self):
        return self.postalCode
    def set_postalCode(self, postalCode):
        self.postalCode = postalCode
    def get_city(self):
        return self.city
    def set_city(self, city):
        self.city = city
    def get_countryCode(self):
        return self.countryCode
    def set_countryCode(self, countryCode):
        self.countryCode = countryCode
    def get_emailAddress(self):
        return self.emailAddress
    def set_emailAddress(self, emailAddress):
        self.emailAddress = emailAddress
    def get_mobileNumber(self):
        return self.mobileNumber
    def set_mobileNumber(self, mobileNumber):
        self.mobileNumber = mobileNumber
    def validate_pickUpNameType(self, value):
        result = True
        # Validate type pickUpNameType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on pickUpNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_streetNameType5(self, value):
        result = True
        # Validate type streetNameType5, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetNameType5' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_houseNumberType6(self, value):
        result = True
        # Validate type houseNumberType6, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 8:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on houseNumberType6' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_boxNumberType7(self, value):
        result = True
        # Validate type boxNumberType7, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 8:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on boxNumberType7' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_postalCodeType8(self, value):
        result = True
        # Validate type postalCodeType8, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 8:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on postalCodeType8' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_cityType9(self, value):
        result = True
        # Validate type cityType9, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on cityType9' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_countryCodeType10(self, value):
        result = True
        # Validate type countryCodeType10, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on countryCodeType10' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_countryCodeType10_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_countryCodeType10_patterns_, ))
                result = False
        return result
    validate_countryCodeType10_patterns_ = [['^([A-Za-z]{2})$']]
    def validate_emailAddressType(self, value):
        result = True
        # Validate type emailAddressType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on emailAddressType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_mobilePhoneType(self, value):
        result = True
        # Validate type mobilePhoneType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on mobilePhoneType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.pickUpName is not None or
            self.streetName is not None or
            self.houseNumber is not None or
            self.boxNumber is not None or
            self.postalCode is not None or
            self.city is not None or
            self.countryCode is not None or
            self.emailAddress is not None or
            self.mobileNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='pickupLocationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('pickupLocationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'pickupLocationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='pickupLocationType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='pickupLocationType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='pickupLocationType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='pickupLocationType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.pickUpName is not None:
            namespaceprefix_ = self.pickUpName_nsprefix_ + ':' if (UseCapturedNS_ and self.pickUpName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spickUpName>%s</%spickUpName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.pickUpName), input_name='pickUpName')), namespaceprefix_ , eol_))
        if self.streetName is not None:
            namespaceprefix_ = self.streetName_nsprefix_ + ':' if (UseCapturedNS_ and self.streetName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstreetName>%s</%sstreetName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.streetName), input_name='streetName')), namespaceprefix_ , eol_))
        if self.houseNumber is not None:
            namespaceprefix_ = self.houseNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.houseNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%shouseNumber>%s</%shouseNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.houseNumber), input_name='houseNumber')), namespaceprefix_ , eol_))
        if self.boxNumber is not None:
            namespaceprefix_ = self.boxNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.boxNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sboxNumber>%s</%sboxNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.boxNumber), input_name='boxNumber')), namespaceprefix_ , eol_))
        if self.postalCode is not None:
            namespaceprefix_ = self.postalCode_nsprefix_ + ':' if (UseCapturedNS_ and self.postalCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spostalCode>%s</%spostalCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.postalCode), input_name='postalCode')), namespaceprefix_ , eol_))
        if self.city is not None:
            namespaceprefix_ = self.city_nsprefix_ + ':' if (UseCapturedNS_ and self.city_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scity>%s</%scity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.city), input_name='city')), namespaceprefix_ , eol_))
        if self.countryCode is not None:
            namespaceprefix_ = self.countryCode_nsprefix_ + ':' if (UseCapturedNS_ and self.countryCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scountryCode>%s</%scountryCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.countryCode), input_name='countryCode')), namespaceprefix_ , eol_))
        if self.emailAddress is not None:
            namespaceprefix_ = self.emailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.emailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%semailAddress>%s</%semailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.emailAddress), input_name='emailAddress')), namespaceprefix_ , eol_))
        if self.mobileNumber is not None:
            namespaceprefix_ = self.mobileNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.mobileNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smobileNumber>%s</%smobileNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.mobileNumber), input_name='mobileNumber')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'pickUpName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'pickUpName')
            value_ = self.gds_validate_string(value_, node, 'pickUpName')
            self.pickUpName = value_
            self.pickUpName_nsprefix_ = child_.prefix
            # validate type pickUpNameType
            self.validate_pickUpNameType(self.pickUpName)
        elif nodeName_ == 'streetName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'streetName')
            value_ = self.gds_validate_string(value_, node, 'streetName')
            self.streetName = value_
            self.streetName_nsprefix_ = child_.prefix
            # validate type streetNameType5
            self.validate_streetNameType5(self.streetName)
        elif nodeName_ == 'houseNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'houseNumber')
            value_ = self.gds_validate_string(value_, node, 'houseNumber')
            self.houseNumber = value_
            self.houseNumber_nsprefix_ = child_.prefix
            # validate type houseNumberType6
            self.validate_houseNumberType6(self.houseNumber)
        elif nodeName_ == 'boxNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'boxNumber')
            value_ = self.gds_validate_string(value_, node, 'boxNumber')
            self.boxNumber = value_
            self.boxNumber_nsprefix_ = child_.prefix
            # validate type boxNumberType7
            self.validate_boxNumberType7(self.boxNumber)
        elif nodeName_ == 'postalCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'postalCode')
            value_ = self.gds_validate_string(value_, node, 'postalCode')
            self.postalCode = value_
            self.postalCode_nsprefix_ = child_.prefix
            # validate type postalCodeType8
            self.validate_postalCodeType8(self.postalCode)
        elif nodeName_ == 'city':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'city')
            value_ = self.gds_validate_string(value_, node, 'city')
            self.city = value_
            self.city_nsprefix_ = child_.prefix
            # validate type cityType9
            self.validate_cityType9(self.city)
        elif nodeName_ == 'countryCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'countryCode')
            value_ = self.gds_validate_string(value_, node, 'countryCode')
            self.countryCode = value_
            self.countryCode_nsprefix_ = child_.prefix
            # validate type countryCodeType10
            self.validate_countryCodeType10(self.countryCode)
        elif nodeName_ == 'emailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'emailAddress')
            value_ = self.gds_validate_string(value_, node, 'emailAddress')
            self.emailAddress = value_
            self.emailAddress_nsprefix_ = child_.prefix
            # validate type emailAddressType
            self.validate_emailAddressType(self.emailAddress)
        elif nodeName_ == 'mobileNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'mobileNumber')
            value_ = self.gds_validate_string(value_, node, 'mobileNumber')
            self.mobileNumber = value_
            self.mobileNumber_nsprefix_ = child_.prefix
            # validate type mobilePhoneType
            self.validate_mobilePhoneType(self.mobileNumber)
# end class pickupLocationType


#
# End data representation classes.
#


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
        rootTag = 'addressType'
        rootClass = addressType
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
        rootTag = 'addressType'
        rootClass = addressType
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
        rootTag = 'addressType'
        rootClass = addressType
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
        rootTag = 'addressType'
        rootClass = addressType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from announcement_common_v1 import *\n\n')
        sys.stdout.write('import announcement_common_v1 as model_\n\n')
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
NamespaceToDefMappings_ = {'http://schema.post.be/announcement/common/v1/': [('mobilePhoneType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('emailAddressType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('desiredDeliveryPlaceType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('itemCodeType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('pickupCodeType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('announcementTypeType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('bbanType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('belgianIbanType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('bicType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('bankTransferMessageType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('productCodeType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('weightInGramsType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('customerReferenceType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('crossReferenceBarcodeType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('freeTextCustomerReference',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('costCenterType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('languageType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('accountIdType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('itemCategoryType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('parcelContentType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('valueCurrencySenderType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('multicolliId',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('openingHoursType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('unitCepType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('deliveryTimeslotType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('dimensionType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('deliveryTimeFrame',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('timeWindowType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'ST'),
                                                   ('addressType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('contactDetailType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('notificationType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('clientType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('insuranceType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('basicInsuranceType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('additionalInsuranceType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('signatureType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('signaturePlusType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('nonDeliveryInstructionsType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('cashOnDeliveryType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('atHomeType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('atShopType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('atIntlHomeType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('atIntlShopType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('atIntlParcelDepotType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('at24_7Type',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('deliveryMethodType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('multicolliType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('automaticSecondPresentationType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('desktopDeliveryType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('repairLogisticsType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('optionsType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('eveningPickupType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('ultraLateInEveningDeliveryType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('timeslotDeliveryType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('samedayEveningDeliveryType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('preferredDeliveryType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('estimatedDropOffType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('prepaidCharacteristicsType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('ParcelContentDetails',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('ParcelContentDetail',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('dimensionsType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('dayPickupType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT'),
                                                   ('pickupLocationType',
                                                    './schemas/announcement_common_v1.xsd',
                                                    'CT')]}

__all__ = [
    "ParcelContentDetail",
    "ParcelContentDetails",
    "additionalInsuranceType",
    "addressType",
    "at24_7Type",
    "atHomeType",
    "atIntlHomeType",
    "atIntlParcelDepotType",
    "atIntlShopType",
    "atShopType",
    "automaticSecondPresentationType",
    "basicInsuranceType",
    "cashOnDeliveryType",
    "clientType",
    "contactDetailType",
    "dayPickupType",
    "deliveryMethodType",
    "desktopDeliveryType",
    "dimensionsType",
    "estimatedDropOffType",
    "eveningPickupType",
    "insuranceType",
    "multicolliType",
    "nonDeliveryInstructionsType",
    "notificationType",
    "optionsType",
    "pickupLocationType",
    "preferredDeliveryType",
    "prepaidCharacteristicsType",
    "repairLogisticsType",
    "samedayEveningDeliveryType",
    "signaturePlusType",
    "signatureType",
    "timeslotDeliveryType",
    "ultraLateInEveningDeliveryType"
]
