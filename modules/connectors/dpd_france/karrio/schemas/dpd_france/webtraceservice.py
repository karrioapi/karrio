#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Fri Apr 17 19:24:10 2026 by generateDS.py version 2.44.3.
# Python 3.12.13 (main, Mar 21 2026, 20:40:49) [Clang 17.0.0 (clang-1700.6.3.2)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './karrio/schemas/dpd_france/webtraceservice.py')
#
# Command line arguments:
#   ./schemas/Webtrace_Service.xsd
#
# Command line:
#   /Users/anshdevnagar/Desktop/PROJECTS/shipping-platform/.venv/karrio/bin/generateDS --no-namespace-defs -o "./karrio/schemas/dpd_france/webtraceservice.py" ./schemas/Webtrace_Service.xsd
#
# Current working directory (os.getcwd()):
#   dpd_france
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
        tzoff_pattern = re_.compile('(\\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00)$')
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
        Tag_strip_pattern_ = re_.compile(r'{.*}')
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
class ExpandContainerModeType(str, Enum):
    MASTER_ONLY='MasterOnly'
    MASTER_AND_SLAVE='MasterAndSlave'


class ImageType(str, Enum):
    POD='POD'
    POA='POA'
    DELIVERY_SIGNATURE='DeliverySignature'
    DELIVERY_SHOP='DeliveryShop'
    PICKUP_SIGNATURE='PickupSignature'


class ReferenceSearchMode(str, Enum):
    EQUALS='Equals'
    LIKE='Like'


#
# Start data representation classes
#
class isAlive(GeneratedsSuper):
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
                CurrentSubclassModule_, isAlive)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if isAlive.subclass:
            return isAlive.subclass(*args_, **kwargs_)
        else:
            return isAlive(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='isAlive', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('isAlive')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'isAlive':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='isAlive')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='isAlive', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='isAlive'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='isAlive', fromsubclass_=False, pretty_print=True):
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
# end class isAlive


class isAliveResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, isAliveResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.isAliveResult = isAliveResult
        self.isAliveResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, isAliveResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if isAliveResponse.subclass:
            return isAliveResponse.subclass(*args_, **kwargs_)
        else:
            return isAliveResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_isAliveResult(self):
        return self.isAliveResult
    def set_isAliveResult(self, isAliveResult):
        self.isAliveResult = isAliveResult
    def has__content(self):
        if (
            self.isAliveResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='isAliveResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('isAliveResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'isAliveResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='isAliveResponse')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='isAliveResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='isAliveResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='isAliveResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.isAliveResult is not None:
            namespaceprefix_ = self.isAliveResult_nsprefix_ + ':' if (UseCapturedNS_ and self.isAliveResult_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sisAliveResult>%s</%sisAliveResult>%s' % (namespaceprefix_ , self.gds_format_boolean(self.isAliveResult, input_name='isAliveResult'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'isAliveResult':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'isAliveResult')
            ival_ = self.gds_validate_boolean(ival_, node, 'isAliveResult')
            self.isAliveResult = ival_
            self.isAliveResult_nsprefix_ = child_.prefix
# end class isAliveResponse


class setAlive(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, value=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.value = value
        self.value_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, setAlive)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if setAlive.subclass:
            return setAlive.subclass(*args_, **kwargs_)
        else:
            return setAlive(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_value(self):
        return self.value
    def set_value(self, value):
        self.value = value
    def has__content(self):
        if (
            self.value is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='setAlive', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('setAlive')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'setAlive':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='setAlive')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='setAlive', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='setAlive'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='setAlive', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.value is not None:
            namespaceprefix_ = self.value_nsprefix_ + ':' if (UseCapturedNS_ and self.value_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%svalue>%s</%svalue>%s' % (namespaceprefix_ , self.gds_format_boolean(self.value, input_name='value'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'value':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'value')
            ival_ = self.gds_validate_boolean(ival_, node, 'value')
            self.value = ival_
            self.value_nsprefix_ = child_.prefix
# end class setAlive


class setAliveResponse(GeneratedsSuper):
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
                CurrentSubclassModule_, setAliveResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if setAliveResponse.subclass:
            return setAliveResponse.subclass(*args_, **kwargs_)
        else:
            return setAliveResponse(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='setAliveResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('setAliveResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'setAliveResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='setAliveResponse')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='setAliveResponse', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='setAliveResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='setAliveResponse', fromsubclass_=False, pretty_print=True):
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
# end class setAliveResponse


class UserCredentials(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, userid=None, password=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.userid = userid
        self.userid_nsprefix_ = None
        self.password = password
        self.password_nsprefix_ = None
        self.anyAttributes_ = {}
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UserCredentials)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UserCredentials.subclass:
            return UserCredentials.subclass(*args_, **kwargs_)
        else:
            return UserCredentials(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_userid(self):
        return self.userid
    def set_userid(self, userid):
        self.userid = userid
    def get_password(self):
        return self.password
    def set_password(self, password):
        self.password = password
    def get_anyAttributes_(self): return self.anyAttributes_
    def set_anyAttributes_(self, anyAttributes_): self.anyAttributes_ = anyAttributes_
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def has__content(self):
        if (
            self.userid is not None or
            self.password is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UserCredentials', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UserCredentials')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UserCredentials':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UserCredentials')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UserCredentials', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UserCredentials'):
        unique_counter = 0
        for name, value in self.anyAttributes_.items():
            xsinamespaceprefix = 'xsi'
            xsinamespace1 = 'http://www.w3.org/2001/XMLSchema-instance'
            xsinamespace2 = '{%s}' % (xsinamespace1, )
            if name.startswith(xsinamespace2):
                name1 = name[len(xsinamespace2):]
                name2 = '%s:%s' % (xsinamespaceprefix, name1, )
                if name2 not in already_processed:
                    already_processed.add(name2)
                    outfile.write(' %s=%s' % (name2, quote_attrib(value), ))
            else:
                mo = re_.match(Namespace_extract_pat_, name)
                if mo is not None:
                    namespace, name = mo.group(1, 2)
                    if name not in already_processed:
                        already_processed.add(name)
                        if namespace == 'http://www.w3.org/XML/1998/namespace':
                            outfile.write(' %s=%s' % (
                                name, quote_attrib(value), ))
                        else:
                            unique_counter += 1
                            outfile.write(' xmlns:%d="%s"' % (
                                unique_counter, namespace, ))
                            outfile.write(' %d:%s=%s' % (
                                unique_counter, name, quote_attrib(value), ))
                else:
                    if name not in already_processed:
                        already_processed.add(name)
                        outfile.write(' %s=%s' % (
                            name, quote_attrib(value), ))
        if self.extensiontype_ is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self.extensiontype_:
                imported_ns_type_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.extensiontype_, '')
                outfile.write(' xsi:type="%s%s"' % (imported_ns_type_prefix_, self.extensiontype_))
            else:
                outfile.write(' xsi:type="%s"' % self.extensiontype_)
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UserCredentials', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.userid is not None:
            namespaceprefix_ = self.userid_nsprefix_ + ':' if (UseCapturedNS_ and self.userid_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%suserid>%s</%suserid>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.userid), input_name='userid')), namespaceprefix_ , eol_))
        if self.password is not None:
            namespaceprefix_ = self.password_nsprefix_ + ':' if (UseCapturedNS_ and self.password_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spassword>%s</%spassword>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.password), input_name='password')), namespaceprefix_ , eol_))
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
        self.anyAttributes_ = {}
        for name, value in attrs.items():
            if name not in already_processed:
                self.anyAttributes_[name] = value
        value = find_attr_value_('xsi:type', node)
        if value is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            self.extensiontype_ = value
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'userid':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'userid')
            value_ = self.gds_validate_string(value_, node, 'userid')
            self.userid = value_
            self.userid_nsprefix_ = child_.prefix
        elif nodeName_ == 'password':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'password')
            value_ = self.gds_validate_string(value_, node, 'password')
            self.password = value_
            self.password_nsprefix_ = child_.prefix
# end class UserCredentials


class VerifyConfiguration(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, request=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.request = request
        self.request_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, VerifyConfiguration)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if VerifyConfiguration.subclass:
            return VerifyConfiguration.subclass(*args_, **kwargs_)
        else:
            return VerifyConfiguration(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_request(self):
        return self.request
    def set_request(self, request):
        self.request = request
    def has__content(self):
        if (
            self.request is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='VerifyConfiguration', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('VerifyConfiguration')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'VerifyConfiguration':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='VerifyConfiguration')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='VerifyConfiguration', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='VerifyConfiguration'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='VerifyConfiguration', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.request is not None:
            namespaceprefix_ = self.request_nsprefix_ + ':' if (UseCapturedNS_ and self.request_nsprefix_) else ''
            self.request.export(outfile, level, namespaceprefix_, namespacedef_='', name_='request', pretty_print=pretty_print)
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
        if nodeName_ == 'request':
            obj_ = VerifyConfigurationRequest.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.request = obj_
            obj_.original_tagname_ = 'request'
# end class VerifyConfiguration


class VerifyConfigurationRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, customer=None, ip=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.customer = customer
        self.customer_nsprefix_ = "tns"
        self.ip = ip
        self.ip_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, VerifyConfigurationRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if VerifyConfigurationRequest.subclass:
            return VerifyConfigurationRequest.subclass(*args_, **kwargs_)
        else:
            return VerifyConfigurationRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_customer(self):
        return self.customer
    def set_customer(self, customer):
        self.customer = customer
    def get_ip(self):
        return self.ip
    def set_ip(self, ip):
        self.ip = ip
    def has__content(self):
        if (
            self.customer is not None or
            self.ip is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='VerifyConfigurationRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('VerifyConfigurationRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'VerifyConfigurationRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='VerifyConfigurationRequest')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='VerifyConfigurationRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='VerifyConfigurationRequest'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='VerifyConfigurationRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.customer is not None:
            namespaceprefix_ = self.customer_nsprefix_ + ':' if (UseCapturedNS_ and self.customer_nsprefix_) else ''
            self.customer.export(outfile, level, namespaceprefix_, namespacedef_='', name_='customer', pretty_print=pretty_print)
        if self.ip is not None:
            namespaceprefix_ = self.ip_nsprefix_ + ':' if (UseCapturedNS_ and self.ip_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sip>%s</%sip>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ip), input_name='ip')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'customer':
            obj_ = Customer.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.customer = obj_
            obj_.original_tagname_ = 'customer'
        elif nodeName_ == 'ip':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ip')
            value_ = self.gds_validate_string(value_, node, 'ip')
            self.ip = value_
            self.ip_nsprefix_ = child_.prefix
# end class VerifyConfigurationRequest


class CustomerSmall(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, centernumber=None, number=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.centernumber = centernumber
        self.centernumber_nsprefix_ = None
        self.number = number
        self.number_nsprefix_ = None
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CustomerSmall)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CustomerSmall.subclass:
            return CustomerSmall.subclass(*args_, **kwargs_)
        else:
            return CustomerSmall(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_centernumber(self):
        return self.centernumber
    def set_centernumber(self, centernumber):
        self.centernumber = centernumber
    def get_number(self):
        return self.number
    def set_number(self, number):
        self.number = number
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def has__content(self):
        if (
            self.centernumber is not None or
            self.number is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CustomerSmall', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CustomerSmall')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CustomerSmall':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CustomerSmall')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CustomerSmall', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CustomerSmall'):
        if self.extensiontype_ is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self.extensiontype_:
                imported_ns_type_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.extensiontype_, '')
                outfile.write(' xsi:type="%s%s"' % (imported_ns_type_prefix_, self.extensiontype_))
            else:
                outfile.write(' xsi:type="%s"' % self.extensiontype_)
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CustomerSmall', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.centernumber is not None:
            namespaceprefix_ = self.centernumber_nsprefix_ + ':' if (UseCapturedNS_ and self.centernumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scenternumber>%s</%scenternumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.centernumber, input_name='centernumber'), namespaceprefix_ , eol_))
        if self.number is not None:
            namespaceprefix_ = self.number_nsprefix_ + ':' if (UseCapturedNS_ and self.number_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snumber>%s</%snumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.number, input_name='number'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'centernumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'centernumber')
            ival_ = self.gds_validate_integer(ival_, node, 'centernumber')
            self.centernumber = ival_
            self.centernumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'number' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'number')
            ival_ = self.gds_validate_integer(ival_, node, 'number')
            self.number = ival_
            self.number_nsprefix_ = child_.prefix
# end class CustomerSmall


class VerifyConfigurationResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, VerifyConfigurationResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.VerifyConfigurationResult = VerifyConfigurationResult
        self.VerifyConfigurationResult_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, VerifyConfigurationResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if VerifyConfigurationResponse.subclass:
            return VerifyConfigurationResponse.subclass(*args_, **kwargs_)
        else:
            return VerifyConfigurationResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_VerifyConfigurationResult(self):
        return self.VerifyConfigurationResult
    def set_VerifyConfigurationResult(self, VerifyConfigurationResult):
        self.VerifyConfigurationResult = VerifyConfigurationResult
    def has__content(self):
        if (
            self.VerifyConfigurationResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='VerifyConfigurationResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('VerifyConfigurationResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'VerifyConfigurationResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='VerifyConfigurationResponse')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='VerifyConfigurationResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='VerifyConfigurationResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='VerifyConfigurationResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.VerifyConfigurationResult is not None:
            namespaceprefix_ = self.VerifyConfigurationResult_nsprefix_ + ':' if (UseCapturedNS_ and self.VerifyConfigurationResult_nsprefix_) else ''
            self.VerifyConfigurationResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='VerifyConfigurationResult', pretty_print=pretty_print)
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
        if nodeName_ == 'VerifyConfigurationResult':
            obj_ = VerifyConfigurationResponse.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.VerifyConfigurationResult = obj_
            obj_.original_tagname_ = 'VerifyConfigurationResult'
# end class VerifyConfigurationResponse


class VerifyUserCredentials(UserCredentials):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = UserCredentials
    def __init__(self, userid=None, password=None, Verify_userid=None, Verify_password=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("VerifyUserCredentials"), self).__init__(userid, password,  **kwargs_)
        self.Verify_userid = Verify_userid
        self.Verify_userid_nsprefix_ = None
        self.Verify_password = Verify_password
        self.Verify_password_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, VerifyUserCredentials)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if VerifyUserCredentials.subclass:
            return VerifyUserCredentials.subclass(*args_, **kwargs_)
        else:
            return VerifyUserCredentials(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Verify_userid(self):
        return self.Verify_userid
    def set_Verify_userid(self, Verify_userid):
        self.Verify_userid = Verify_userid
    def get_Verify_password(self):
        return self.Verify_password
    def set_Verify_password(self, Verify_password):
        self.Verify_password = Verify_password
    def has__content(self):
        if (
            self.Verify_userid is not None or
            self.Verify_password is not None or
            super(VerifyUserCredentials, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='VerifyUserCredentials', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('VerifyUserCredentials')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'VerifyUserCredentials':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='VerifyUserCredentials')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='VerifyUserCredentials', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='VerifyUserCredentials'):
        super(VerifyUserCredentials, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='VerifyUserCredentials')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='VerifyUserCredentials', fromsubclass_=False, pretty_print=True):
        super(VerifyUserCredentials, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Verify_userid is not None:
            namespaceprefix_ = self.Verify_userid_nsprefix_ + ':' if (UseCapturedNS_ and self.Verify_userid_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sVerify_userid>%s</%sVerify_userid>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Verify_userid), input_name='Verify_userid')), namespaceprefix_ , eol_))
        if self.Verify_password is not None:
            namespaceprefix_ = self.Verify_password_nsprefix_ + ':' if (UseCapturedNS_ and self.Verify_password_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sVerify_password>%s</%sVerify_password>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Verify_password), input_name='Verify_password')), namespaceprefix_ , eol_))
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
        super(VerifyUserCredentials, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Verify_userid':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Verify_userid')
            value_ = self.gds_validate_string(value_, node, 'Verify_userid')
            self.Verify_userid = value_
            self.Verify_userid_nsprefix_ = child_.prefix
        elif nodeName_ == 'Verify_password':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Verify_password')
            value_ = self.gds_validate_string(value_, node, 'Verify_password')
            self.Verify_password = value_
            self.Verify_password_nsprefix_ = child_.prefix
        super(VerifyUserCredentials, self)._buildChildren(child_, node, nodeName_, True)
# end class VerifyUserCredentials


class getInfo(GeneratedsSuper):
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
                CurrentSubclassModule_, getInfo)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if getInfo.subclass:
            return getInfo.subclass(*args_, **kwargs_)
        else:
            return getInfo(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='getInfo', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('getInfo')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'getInfo':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='getInfo')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='getInfo', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='getInfo'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='getInfo', fromsubclass_=False, pretty_print=True):
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
# end class getInfo


class getInfoResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, getInfoResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.getInfoResult = getInfoResult
        self.getInfoResult_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, getInfoResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if getInfoResponse.subclass:
            return getInfoResponse.subclass(*args_, **kwargs_)
        else:
            return getInfoResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_getInfoResult(self):
        return self.getInfoResult
    def set_getInfoResult(self, getInfoResult):
        self.getInfoResult = getInfoResult
    def has__content(self):
        if (
            self.getInfoResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='getInfoResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('getInfoResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'getInfoResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='getInfoResponse')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='getInfoResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='getInfoResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='getInfoResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.getInfoResult is not None:
            namespaceprefix_ = self.getInfoResult_nsprefix_ + ':' if (UseCapturedNS_ and self.getInfoResult_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sgetInfoResult>%s</%sgetInfoResult>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.getInfoResult), input_name='getInfoResult')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'getInfoResult':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'getInfoResult')
            value_ = self.gds_validate_string(value_, node, 'getInfoResult')
            self.getInfoResult = value_
            self.getInfoResult_nsprefix_ = child_.prefix
# end class getInfoResponse


class runAction(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, request=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.request = request
        self.request_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, runAction)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if runAction.subclass:
            return runAction.subclass(*args_, **kwargs_)
        else:
            return runAction(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_request(self):
        return self.request
    def set_request(self, request):
        self.request = request
    def has__content(self):
        if (
            self.request is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='runAction', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('runAction')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'runAction':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='runAction')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='runAction', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='runAction'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='runAction', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.request is not None:
            namespaceprefix_ = self.request_nsprefix_ + ':' if (UseCapturedNS_ and self.request_nsprefix_) else ''
            self.request.export(outfile, level, namespaceprefix_, namespacedef_='', name_='request', pretty_print=pretty_print)
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
        if nodeName_ == 'request':
            obj_ = RunActionRequest.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.request = obj_
            obj_.original_tagname_ = 'request'
# end class runAction


class RunActionRequest(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Action=None, Parameter=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Action = Action
        self.Action_nsprefix_ = None
        self.Parameter = Parameter
        self.Parameter_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RunActionRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RunActionRequest.subclass:
            return RunActionRequest.subclass(*args_, **kwargs_)
        else:
            return RunActionRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Action(self):
        return self.Action
    def set_Action(self, Action):
        self.Action = Action
    def get_Parameter(self):
        return self.Parameter
    def set_Parameter(self, Parameter):
        self.Parameter = Parameter
    def has__content(self):
        if (
            self.Action is not None or
            self.Parameter is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RunActionRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RunActionRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RunActionRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RunActionRequest')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RunActionRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RunActionRequest'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RunActionRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Action is not None:
            namespaceprefix_ = self.Action_nsprefix_ + ':' if (UseCapturedNS_ and self.Action_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAction>%s</%sAction>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Action), input_name='Action')), namespaceprefix_ , eol_))
        if self.Parameter is not None:
            namespaceprefix_ = self.Parameter_nsprefix_ + ':' if (UseCapturedNS_ and self.Parameter_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sParameter>%s</%sParameter>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Parameter), input_name='Parameter')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Action':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Action')
            value_ = self.gds_validate_string(value_, node, 'Action')
            self.Action = value_
            self.Action_nsprefix_ = child_.prefix
        elif nodeName_ == 'Parameter':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Parameter')
            value_ = self.gds_validate_string(value_, node, 'Parameter')
            self.Parameter = value_
            self.Parameter_nsprefix_ = child_.prefix
# end class RunActionRequest


class runActionResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, runActionResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.runActionResult = runActionResult
        self.runActionResult_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, runActionResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if runActionResponse.subclass:
            return runActionResponse.subclass(*args_, **kwargs_)
        else:
            return runActionResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_runActionResult(self):
        return self.runActionResult
    def set_runActionResult(self, runActionResult):
        self.runActionResult = runActionResult
    def has__content(self):
        if (
            self.runActionResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='runActionResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('runActionResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'runActionResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='runActionResponse')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='runActionResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='runActionResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='runActionResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.runActionResult is not None:
            namespaceprefix_ = self.runActionResult_nsprefix_ + ':' if (UseCapturedNS_ and self.runActionResult_nsprefix_) else ''
            self.runActionResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='runActionResult', pretty_print=pretty_print)
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
        if nodeName_ == 'runActionResult':
            obj_ = RunActionResponse.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.runActionResult = obj_
            obj_.original_tagname_ = 'runActionResult'
# end class runActionResponse


class RunActionResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Response=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Response = Response
        self.Response_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RunActionResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RunActionResponse.subclass:
            return RunActionResponse.subclass(*args_, **kwargs_)
        else:
            return RunActionResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Response(self):
        return self.Response
    def set_Response(self, Response):
        self.Response = Response
    def has__content(self):
        if (
            self.Response is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RunActionResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RunActionResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RunActionResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RunActionResponse')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RunActionResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RunActionResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RunActionResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
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
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Response':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Response')
            value_ = self.gds_validate_string(value_, node, 'Response')
            self.Response = value_
            self.Response_nsprefix_ = child_.prefix
# end class RunActionResponse


class GetShipmentTraceSingle(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, request=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.request = request
        self.request_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetShipmentTraceSingle)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetShipmentTraceSingle.subclass:
            return GetShipmentTraceSingle.subclass(*args_, **kwargs_)
        else:
            return GetShipmentTraceSingle(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_request(self):
        return self.request
    def set_request(self, request):
        self.request = request
    def has__content(self):
        if (
            self.request is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetShipmentTraceSingle', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetShipmentTraceSingle')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetShipmentTraceSingle':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetShipmentTraceSingle')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetShipmentTraceSingle', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetShipmentTraceSingle'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetShipmentTraceSingle', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.request is not None:
            namespaceprefix_ = self.request_nsprefix_ + ':' if (UseCapturedNS_ and self.request_nsprefix_) else ''
            self.request.export(outfile, level, namespaceprefix_, namespacedef_='', name_='request', pretty_print=pretty_print)
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
        if nodeName_ == 'request':
            obj_ = ShipmentDetailRequest.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.request = obj_
            obj_.original_tagname_ = 'request'
# end class GetShipmentTraceSingle


class RequestBase(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Customer=None, Language=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Customer = Customer
        self.Customer_nsprefix_ = "tns"
        self.Language = Language
        self.Language_nsprefix_ = None
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RequestBase)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RequestBase.subclass:
            return RequestBase.subclass(*args_, **kwargs_)
        else:
            return RequestBase(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Customer(self):
        return self.Customer
    def set_Customer(self, Customer):
        self.Customer = Customer
    def get_Language(self):
        return self.Language
    def set_Language(self, Language):
        self.Language = Language
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def has__content(self):
        if (
            self.Customer is not None or
            self.Language is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RequestBase', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RequestBase')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RequestBase':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RequestBase')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RequestBase', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RequestBase'):
        if self.extensiontype_ is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self.extensiontype_:
                imported_ns_type_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.extensiontype_, '')
                outfile.write(' xsi:type="%s%s"' % (imported_ns_type_prefix_, self.extensiontype_))
            else:
                outfile.write(' xsi:type="%s"' % self.extensiontype_)
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RequestBase', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Customer is not None:
            namespaceprefix_ = self.Customer_nsprefix_ + ':' if (UseCapturedNS_ and self.Customer_nsprefix_) else ''
            self.Customer.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Customer', pretty_print=pretty_print)
        if self.Language is not None:
            namespaceprefix_ = self.Language_nsprefix_ + ':' if (UseCapturedNS_ and self.Language_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLanguage>%s</%sLanguage>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Language), input_name='Language')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Customer':
            obj_ = Customer.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Customer = obj_
            obj_.original_tagname_ = 'Customer'
        elif nodeName_ == 'Language':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Language')
            value_ = self.gds_validate_string(value_, node, 'Language')
            self.Language = value_
            self.Language_nsprefix_ = child_.prefix
# end class RequestBase


class Options(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Type=None, CenterType=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Type = Type
        self.Type_nsprefix_ = None
        self.CenterType = CenterType
        self.CenterType_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Options)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Options.subclass:
            return Options.subclass(*args_, **kwargs_)
        else:
            return Options(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_CenterType(self):
        return self.CenterType
    def set_CenterType(self, CenterType):
        self.CenterType = CenterType
    def has__content(self):
        if (
            self.Type is not None or
            self.CenterType is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Options', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Options')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Options':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Options')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Options', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Options'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Options', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sType>%s</%sType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Type), input_name='Type')), namespaceprefix_ , eol_))
        if self.CenterType is not None:
            namespaceprefix_ = self.CenterType_nsprefix_ + ':' if (UseCapturedNS_ and self.CenterType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCenterType>%s</%sCenterType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CenterType), input_name='CenterType')), namespaceprefix_ , eol_))
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
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Type')
            value_ = self.gds_validate_string(value_, node, 'Type')
            self.Type = value_
            self.Type_nsprefix_ = child_.prefix
        elif nodeName_ == 'CenterType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CenterType')
            value_ = self.gds_validate_string(value_, node, 'CenterType')
            self.CenterType = value_
            self.CenterType_nsprefix_ = child_.prefix
# end class Options


class GetShipmentTraceSingleResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetShipmentTraceSingleResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetShipmentTraceSingleResult = GetShipmentTraceSingleResult
        self.GetShipmentTraceSingleResult_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetShipmentTraceSingleResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetShipmentTraceSingleResponse.subclass:
            return GetShipmentTraceSingleResponse.subclass(*args_, **kwargs_)
        else:
            return GetShipmentTraceSingleResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetShipmentTraceSingleResult(self):
        return self.GetShipmentTraceSingleResult
    def set_GetShipmentTraceSingleResult(self, GetShipmentTraceSingleResult):
        self.GetShipmentTraceSingleResult = GetShipmentTraceSingleResult
    def has__content(self):
        if (
            self.GetShipmentTraceSingleResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetShipmentTraceSingleResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetShipmentTraceSingleResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetShipmentTraceSingleResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetShipmentTraceSingleResponse')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetShipmentTraceSingleResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetShipmentTraceSingleResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetShipmentTraceSingleResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetShipmentTraceSingleResult is not None:
            namespaceprefix_ = self.GetShipmentTraceSingleResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetShipmentTraceSingleResult_nsprefix_) else ''
            self.GetShipmentTraceSingleResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetShipmentTraceSingleResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GetShipmentTraceSingleResult':
            obj_ = ShipmentTrace.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetShipmentTraceSingleResult = obj_
            obj_.original_tagname_ = 'GetShipmentTraceSingleResult'
# end class GetShipmentTraceSingleResponse


class clsShipmentTraceBase(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ShipmentNumber=None, DestinationCountry=None, DestinationZipcode=None, ShippingDate=None, DeliveryDate=None, Weight=None, Receiver=None, Reference=None, Reference2=None, Reference3=None, Reference4=None, DeliveryScheduled=None, Traces=None, Reference_International=None, IsB2C=None, IsRetour=None, PointRelaisName=None, PointRelaisLink=None, ShipmentNumber_Retour=None, RetourType=None, Services=None, CustomerCenternumber=None, CustomerNumber=None, BarcodeSource=None, BarcodeId=None, ReceiverDepotNumber=None, ReceiverTourNumber=None, DeliveryRecordNumber=None, DeliveryRecordPosition=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ShipmentNumber = ShipmentNumber
        self.ShipmentNumber_nsprefix_ = None
        self.DestinationCountry = DestinationCountry
        self.DestinationCountry_nsprefix_ = None
        self.DestinationZipcode = DestinationZipcode
        self.DestinationZipcode_nsprefix_ = None
        self.ShippingDate = ShippingDate
        self.ShippingDate_nsprefix_ = None
        self.DeliveryDate = DeliveryDate
        self.DeliveryDate_nsprefix_ = None
        self.Weight = Weight
        self.Weight_nsprefix_ = None
        self.Receiver = Receiver
        self.Receiver_nsprefix_ = None
        self.Reference = Reference
        self.Reference_nsprefix_ = None
        self.Reference2 = Reference2
        self.Reference2_nsprefix_ = None
        self.Reference3 = Reference3
        self.Reference3_nsprefix_ = None
        self.Reference4 = Reference4
        self.Reference4_nsprefix_ = None
        self.DeliveryScheduled = DeliveryScheduled
        self.DeliveryScheduled_nsprefix_ = "tns"
        self.Traces = Traces
        self.Traces_nsprefix_ = "tns"
        self.Reference_International = Reference_International
        self.Reference_International_nsprefix_ = None
        self.IsB2C = IsB2C
        self.IsB2C_nsprefix_ = None
        self.IsRetour = IsRetour
        self.IsRetour_nsprefix_ = None
        self.PointRelaisName = PointRelaisName
        self.PointRelaisName_nsprefix_ = None
        self.PointRelaisLink = PointRelaisLink
        self.PointRelaisLink_nsprefix_ = None
        self.ShipmentNumber_Retour = ShipmentNumber_Retour
        self.ShipmentNumber_Retour_nsprefix_ = None
        self.RetourType = RetourType
        self.RetourType_nsprefix_ = None
        self.Services = Services
        self.Services_nsprefix_ = "tns"
        self.CustomerCenternumber = CustomerCenternumber
        self.CustomerCenternumber_nsprefix_ = None
        self.CustomerNumber = CustomerNumber
        self.CustomerNumber_nsprefix_ = None
        self.BarcodeSource = BarcodeSource
        self.BarcodeSource_nsprefix_ = None
        self.BarcodeId = BarcodeId
        self.BarcodeId_nsprefix_ = None
        self.ReceiverDepotNumber = ReceiverDepotNumber
        self.ReceiverDepotNumber_nsprefix_ = None
        self.ReceiverTourNumber = ReceiverTourNumber
        self.ReceiverTourNumber_nsprefix_ = None
        self.DeliveryRecordNumber = DeliveryRecordNumber
        self.DeliveryRecordNumber_nsprefix_ = None
        self.DeliveryRecordPosition = DeliveryRecordPosition
        self.DeliveryRecordPosition_nsprefix_ = None
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, clsShipmentTraceBase)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if clsShipmentTraceBase.subclass:
            return clsShipmentTraceBase.subclass(*args_, **kwargs_)
        else:
            return clsShipmentTraceBase(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ShipmentNumber(self):
        return self.ShipmentNumber
    def set_ShipmentNumber(self, ShipmentNumber):
        self.ShipmentNumber = ShipmentNumber
    def get_DestinationCountry(self):
        return self.DestinationCountry
    def set_DestinationCountry(self, DestinationCountry):
        self.DestinationCountry = DestinationCountry
    def get_DestinationZipcode(self):
        return self.DestinationZipcode
    def set_DestinationZipcode(self, DestinationZipcode):
        self.DestinationZipcode = DestinationZipcode
    def get_ShippingDate(self):
        return self.ShippingDate
    def set_ShippingDate(self, ShippingDate):
        self.ShippingDate = ShippingDate
    def get_DeliveryDate(self):
        return self.DeliveryDate
    def set_DeliveryDate(self, DeliveryDate):
        self.DeliveryDate = DeliveryDate
    def get_Weight(self):
        return self.Weight
    def set_Weight(self, Weight):
        self.Weight = Weight
    def get_Receiver(self):
        return self.Receiver
    def set_Receiver(self, Receiver):
        self.Receiver = Receiver
    def get_Reference(self):
        return self.Reference
    def set_Reference(self, Reference):
        self.Reference = Reference
    def get_Reference2(self):
        return self.Reference2
    def set_Reference2(self, Reference2):
        self.Reference2 = Reference2
    def get_Reference3(self):
        return self.Reference3
    def set_Reference3(self, Reference3):
        self.Reference3 = Reference3
    def get_Reference4(self):
        return self.Reference4
    def set_Reference4(self, Reference4):
        self.Reference4 = Reference4
    def get_DeliveryScheduled(self):
        return self.DeliveryScheduled
    def set_DeliveryScheduled(self, DeliveryScheduled):
        self.DeliveryScheduled = DeliveryScheduled
    def get_Traces(self):
        return self.Traces
    def set_Traces(self, Traces):
        self.Traces = Traces
    def get_Reference_International(self):
        return self.Reference_International
    def set_Reference_International(self, Reference_International):
        self.Reference_International = Reference_International
    def get_IsB2C(self):
        return self.IsB2C
    def set_IsB2C(self, IsB2C):
        self.IsB2C = IsB2C
    def get_IsRetour(self):
        return self.IsRetour
    def set_IsRetour(self, IsRetour):
        self.IsRetour = IsRetour
    def get_PointRelaisName(self):
        return self.PointRelaisName
    def set_PointRelaisName(self, PointRelaisName):
        self.PointRelaisName = PointRelaisName
    def get_PointRelaisLink(self):
        return self.PointRelaisLink
    def set_PointRelaisLink(self, PointRelaisLink):
        self.PointRelaisLink = PointRelaisLink
    def get_ShipmentNumber_Retour(self):
        return self.ShipmentNumber_Retour
    def set_ShipmentNumber_Retour(self, ShipmentNumber_Retour):
        self.ShipmentNumber_Retour = ShipmentNumber_Retour
    def get_RetourType(self):
        return self.RetourType
    def set_RetourType(self, RetourType):
        self.RetourType = RetourType
    def get_Services(self):
        return self.Services
    def set_Services(self, Services):
        self.Services = Services
    def get_CustomerCenternumber(self):
        return self.CustomerCenternumber
    def set_CustomerCenternumber(self, CustomerCenternumber):
        self.CustomerCenternumber = CustomerCenternumber
    def get_CustomerNumber(self):
        return self.CustomerNumber
    def set_CustomerNumber(self, CustomerNumber):
        self.CustomerNumber = CustomerNumber
    def get_BarcodeSource(self):
        return self.BarcodeSource
    def set_BarcodeSource(self, BarcodeSource):
        self.BarcodeSource = BarcodeSource
    def get_BarcodeId(self):
        return self.BarcodeId
    def set_BarcodeId(self, BarcodeId):
        self.BarcodeId = BarcodeId
    def get_ReceiverDepotNumber(self):
        return self.ReceiverDepotNumber
    def set_ReceiverDepotNumber(self, ReceiverDepotNumber):
        self.ReceiverDepotNumber = ReceiverDepotNumber
    def get_ReceiverTourNumber(self):
        return self.ReceiverTourNumber
    def set_ReceiverTourNumber(self, ReceiverTourNumber):
        self.ReceiverTourNumber = ReceiverTourNumber
    def get_DeliveryRecordNumber(self):
        return self.DeliveryRecordNumber
    def set_DeliveryRecordNumber(self, DeliveryRecordNumber):
        self.DeliveryRecordNumber = DeliveryRecordNumber
    def get_DeliveryRecordPosition(self):
        return self.DeliveryRecordPosition
    def set_DeliveryRecordPosition(self, DeliveryRecordPosition):
        self.DeliveryRecordPosition = DeliveryRecordPosition
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def has__content(self):
        if (
            self.ShipmentNumber is not None or
            self.DestinationCountry is not None or
            self.DestinationZipcode is not None or
            self.ShippingDate is not None or
            self.DeliveryDate is not None or
            self.Weight is not None or
            self.Receiver is not None or
            self.Reference is not None or
            self.Reference2 is not None or
            self.Reference3 is not None or
            self.Reference4 is not None or
            self.DeliveryScheduled is not None or
            self.Traces is not None or
            self.Reference_International is not None or
            self.IsB2C is not None or
            self.IsRetour is not None or
            self.PointRelaisName is not None or
            self.PointRelaisLink is not None or
            self.ShipmentNumber_Retour is not None or
            self.RetourType is not None or
            self.Services is not None or
            self.CustomerCenternumber is not None or
            self.CustomerNumber is not None or
            self.BarcodeSource is not None or
            self.BarcodeId is not None or
            self.ReceiverDepotNumber is not None or
            self.ReceiverTourNumber is not None or
            self.DeliveryRecordNumber is not None or
            self.DeliveryRecordPosition is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='clsShipmentTraceBase', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('clsShipmentTraceBase')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'clsShipmentTraceBase':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='clsShipmentTraceBase')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='clsShipmentTraceBase', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='clsShipmentTraceBase'):
        if self.extensiontype_ is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self.extensiontype_:
                imported_ns_type_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.extensiontype_, '')
                outfile.write(' xsi:type="%s%s"' % (imported_ns_type_prefix_, self.extensiontype_))
            else:
                outfile.write(' xsi:type="%s"' % self.extensiontype_)
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='clsShipmentTraceBase', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ShipmentNumber is not None:
            namespaceprefix_ = self.ShipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipmentNumber>%s</%sShipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShipmentNumber), input_name='ShipmentNumber')), namespaceprefix_ , eol_))
        if self.DestinationCountry is not None:
            namespaceprefix_ = self.DestinationCountry_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationCountry_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDestinationCountry>%s</%sDestinationCountry>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DestinationCountry), input_name='DestinationCountry')), namespaceprefix_ , eol_))
        if self.DestinationZipcode is not None:
            namespaceprefix_ = self.DestinationZipcode_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationZipcode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDestinationZipcode>%s</%sDestinationZipcode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DestinationZipcode), input_name='DestinationZipcode')), namespaceprefix_ , eol_))
        if self.ShippingDate is not None:
            namespaceprefix_ = self.ShippingDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ShippingDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShippingDate>%s</%sShippingDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShippingDate), input_name='ShippingDate')), namespaceprefix_ , eol_))
        if self.DeliveryDate is not None:
            namespaceprefix_ = self.DeliveryDate_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeliveryDate>%s</%sDeliveryDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DeliveryDate), input_name='DeliveryDate')), namespaceprefix_ , eol_))
        if self.Weight is not None:
            namespaceprefix_ = self.Weight_nsprefix_ + ':' if (UseCapturedNS_ and self.Weight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeight>%s</%sWeight>%s' % (namespaceprefix_ , self.gds_format_double(self.Weight, input_name='Weight'), namespaceprefix_ , eol_))
        if self.Receiver is not None:
            namespaceprefix_ = self.Receiver_nsprefix_ + ':' if (UseCapturedNS_ and self.Receiver_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReceiver>%s</%sReceiver>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Receiver), input_name='Receiver')), namespaceprefix_ , eol_))
        if self.Reference is not None:
            namespaceprefix_ = self.Reference_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference>%s</%sReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference), input_name='Reference')), namespaceprefix_ , eol_))
        if self.Reference2 is not None:
            namespaceprefix_ = self.Reference2_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference2>%s</%sReference2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference2), input_name='Reference2')), namespaceprefix_ , eol_))
        if self.Reference3 is not None:
            namespaceprefix_ = self.Reference3_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference3_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference3>%s</%sReference3>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference3), input_name='Reference3')), namespaceprefix_ , eol_))
        if self.Reference4 is not None:
            namespaceprefix_ = self.Reference4_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference4_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference4>%s</%sReference4>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference4), input_name='Reference4')), namespaceprefix_ , eol_))
        if self.DeliveryScheduled is not None:
            namespaceprefix_ = self.DeliveryScheduled_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryScheduled_nsprefix_) else ''
            self.DeliveryScheduled.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DeliveryScheduled', pretty_print=pretty_print)
        if self.Traces is not None:
            namespaceprefix_ = self.Traces_nsprefix_ + ':' if (UseCapturedNS_ and self.Traces_nsprefix_) else ''
            self.Traces.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Traces', pretty_print=pretty_print)
        if self.Reference_International is not None:
            namespaceprefix_ = self.Reference_International_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference_International_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference_International>%s</%sReference_International>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference_International), input_name='Reference_International')), namespaceprefix_ , eol_))
        if self.IsB2C is not None:
            namespaceprefix_ = self.IsB2C_nsprefix_ + ':' if (UseCapturedNS_ and self.IsB2C_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIsB2C>%s</%sIsB2C>%s' % (namespaceprefix_ , self.gds_format_boolean(self.IsB2C, input_name='IsB2C'), namespaceprefix_ , eol_))
        if self.IsRetour is not None:
            namespaceprefix_ = self.IsRetour_nsprefix_ + ':' if (UseCapturedNS_ and self.IsRetour_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIsRetour>%s</%sIsRetour>%s' % (namespaceprefix_ , self.gds_format_boolean(self.IsRetour, input_name='IsRetour'), namespaceprefix_ , eol_))
        if self.PointRelaisName is not None:
            namespaceprefix_ = self.PointRelaisName_nsprefix_ + ':' if (UseCapturedNS_ and self.PointRelaisName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPointRelaisName>%s</%sPointRelaisName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PointRelaisName), input_name='PointRelaisName')), namespaceprefix_ , eol_))
        if self.PointRelaisLink is not None:
            namespaceprefix_ = self.PointRelaisLink_nsprefix_ + ':' if (UseCapturedNS_ and self.PointRelaisLink_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPointRelaisLink>%s</%sPointRelaisLink>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PointRelaisLink), input_name='PointRelaisLink')), namespaceprefix_ , eol_))
        if self.ShipmentNumber_Retour is not None:
            namespaceprefix_ = self.ShipmentNumber_Retour_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentNumber_Retour_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipmentNumber_Retour>%s</%sShipmentNumber_Retour>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShipmentNumber_Retour), input_name='ShipmentNumber_Retour')), namespaceprefix_ , eol_))
        if self.RetourType is not None:
            namespaceprefix_ = self.RetourType_nsprefix_ + ':' if (UseCapturedNS_ and self.RetourType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRetourType>%s</%sRetourType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.RetourType), input_name='RetourType')), namespaceprefix_ , eol_))
        if self.Services is not None:
            namespaceprefix_ = self.Services_nsprefix_ + ':' if (UseCapturedNS_ and self.Services_nsprefix_) else ''
            self.Services.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Services', pretty_print=pretty_print)
        if self.CustomerCenternumber is not None:
            namespaceprefix_ = self.CustomerCenternumber_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomerCenternumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustomerCenternumber>%s</%sCustomerCenternumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.CustomerCenternumber, input_name='CustomerCenternumber'), namespaceprefix_ , eol_))
        if self.CustomerNumber is not None:
            namespaceprefix_ = self.CustomerNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomerNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustomerNumber>%s</%sCustomerNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.CustomerNumber, input_name='CustomerNumber'), namespaceprefix_ , eol_))
        if self.BarcodeSource is not None:
            namespaceprefix_ = self.BarcodeSource_nsprefix_ + ':' if (UseCapturedNS_ and self.BarcodeSource_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBarcodeSource>%s</%sBarcodeSource>%s' % (namespaceprefix_ , self.gds_format_integer(self.BarcodeSource, input_name='BarcodeSource'), namespaceprefix_ , eol_))
        if self.BarcodeId is not None:
            namespaceprefix_ = self.BarcodeId_nsprefix_ + ':' if (UseCapturedNS_ and self.BarcodeId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBarcodeId>%s</%sBarcodeId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BarcodeId), input_name='BarcodeId')), namespaceprefix_ , eol_))
        if self.ReceiverDepotNumber is not None:
            namespaceprefix_ = self.ReceiverDepotNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ReceiverDepotNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReceiverDepotNumber>%s</%sReceiverDepotNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.ReceiverDepotNumber, input_name='ReceiverDepotNumber'), namespaceprefix_ , eol_))
        if self.ReceiverTourNumber is not None:
            namespaceprefix_ = self.ReceiverTourNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ReceiverTourNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReceiverTourNumber>%s</%sReceiverTourNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.ReceiverTourNumber, input_name='ReceiverTourNumber'), namespaceprefix_ , eol_))
        if self.ReceiverTourNumber is None:
            namespaceprefix_ = self.ReceiverTourNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ReceiverTourNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReceiverTourNumber xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>%s' % (namespaceprefix_,eol_))
        if self.DeliveryRecordNumber is not None:
            namespaceprefix_ = self.DeliveryRecordNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryRecordNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeliveryRecordNumber>%s</%sDeliveryRecordNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.DeliveryRecordNumber, input_name='DeliveryRecordNumber'), namespaceprefix_ , eol_))
        if self.DeliveryRecordNumber is None:
            namespaceprefix_ = self.DeliveryRecordNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryRecordNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeliveryRecordNumber xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>%s' % (namespaceprefix_,eol_))
        if self.DeliveryRecordPosition is not None:
            namespaceprefix_ = self.DeliveryRecordPosition_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryRecordPosition_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeliveryRecordPosition>%s</%sDeliveryRecordPosition>%s' % (namespaceprefix_ , self.gds_format_integer(self.DeliveryRecordPosition, input_name='DeliveryRecordPosition'), namespaceprefix_ , eol_))
        if self.DeliveryRecordPosition is None:
            namespaceprefix_ = self.DeliveryRecordPosition_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryRecordPosition_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeliveryRecordPosition xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>%s' % (namespaceprefix_,eol_))
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
        if nodeName_ == 'ShipmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShipmentNumber')
            value_ = self.gds_validate_string(value_, node, 'ShipmentNumber')
            self.ShipmentNumber = value_
            self.ShipmentNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'DestinationCountry':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DestinationCountry')
            value_ = self.gds_validate_string(value_, node, 'DestinationCountry')
            self.DestinationCountry = value_
            self.DestinationCountry_nsprefix_ = child_.prefix
        elif nodeName_ == 'DestinationZipcode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DestinationZipcode')
            value_ = self.gds_validate_string(value_, node, 'DestinationZipcode')
            self.DestinationZipcode = value_
            self.DestinationZipcode_nsprefix_ = child_.prefix
        elif nodeName_ == 'ShippingDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShippingDate')
            value_ = self.gds_validate_string(value_, node, 'ShippingDate')
            self.ShippingDate = value_
            self.ShippingDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'DeliveryDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DeliveryDate')
            value_ = self.gds_validate_string(value_, node, 'DeliveryDate')
            self.DeliveryDate = value_
            self.DeliveryDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'Weight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_double(sval_, node, 'Weight')
            fval_ = self.gds_validate_double(fval_, node, 'Weight')
            self.Weight = fval_
            self.Weight_nsprefix_ = child_.prefix
        elif nodeName_ == 'Receiver':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Receiver')
            value_ = self.gds_validate_string(value_, node, 'Receiver')
            self.Receiver = value_
            self.Receiver_nsprefix_ = child_.prefix
        elif nodeName_ == 'Reference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Reference')
            value_ = self.gds_validate_string(value_, node, 'Reference')
            self.Reference = value_
            self.Reference_nsprefix_ = child_.prefix
        elif nodeName_ == 'Reference2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Reference2')
            value_ = self.gds_validate_string(value_, node, 'Reference2')
            self.Reference2 = value_
            self.Reference2_nsprefix_ = child_.prefix
        elif nodeName_ == 'Reference3':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Reference3')
            value_ = self.gds_validate_string(value_, node, 'Reference3')
            self.Reference3 = value_
            self.Reference3_nsprefix_ = child_.prefix
        elif nodeName_ == 'Reference4':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Reference4')
            value_ = self.gds_validate_string(value_, node, 'Reference4')
            self.Reference4 = value_
            self.Reference4_nsprefix_ = child_.prefix
        elif nodeName_ == 'DeliveryScheduled':
            obj_ = SdgiData.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DeliveryScheduled = obj_
            obj_.original_tagname_ = 'DeliveryScheduled'
        elif nodeName_ == 'Traces':
            obj_ = ArrayOfClsTrace.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Traces = obj_
            obj_.original_tagname_ = 'Traces'
        elif nodeName_ == 'Reference_International':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Reference_International')
            value_ = self.gds_validate_string(value_, node, 'Reference_International')
            self.Reference_International = value_
            self.Reference_International_nsprefix_ = child_.prefix
        elif nodeName_ == 'IsB2C':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'IsB2C')
            ival_ = self.gds_validate_boolean(ival_, node, 'IsB2C')
            self.IsB2C = ival_
            self.IsB2C_nsprefix_ = child_.prefix
        elif nodeName_ == 'IsRetour':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'IsRetour')
            ival_ = self.gds_validate_boolean(ival_, node, 'IsRetour')
            self.IsRetour = ival_
            self.IsRetour_nsprefix_ = child_.prefix
        elif nodeName_ == 'PointRelaisName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PointRelaisName')
            value_ = self.gds_validate_string(value_, node, 'PointRelaisName')
            self.PointRelaisName = value_
            self.PointRelaisName_nsprefix_ = child_.prefix
        elif nodeName_ == 'PointRelaisLink':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PointRelaisLink')
            value_ = self.gds_validate_string(value_, node, 'PointRelaisLink')
            self.PointRelaisLink = value_
            self.PointRelaisLink_nsprefix_ = child_.prefix
        elif nodeName_ == 'ShipmentNumber_Retour':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShipmentNumber_Retour')
            value_ = self.gds_validate_string(value_, node, 'ShipmentNumber_Retour')
            self.ShipmentNumber_Retour = value_
            self.ShipmentNumber_Retour_nsprefix_ = child_.prefix
        elif nodeName_ == 'RetourType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RetourType')
            value_ = self.gds_validate_string(value_, node, 'RetourType')
            self.RetourType = value_
            self.RetourType_nsprefix_ = child_.prefix
        elif nodeName_ == 'Services':
            obj_ = ArrayOfServiceInfo.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Services = obj_
            obj_.original_tagname_ = 'Services'
        elif nodeName_ == 'CustomerCenternumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'CustomerCenternumber')
            ival_ = self.gds_validate_integer(ival_, node, 'CustomerCenternumber')
            self.CustomerCenternumber = ival_
            self.CustomerCenternumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'CustomerNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'CustomerNumber')
            ival_ = self.gds_validate_integer(ival_, node, 'CustomerNumber')
            self.CustomerNumber = ival_
            self.CustomerNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'BarcodeSource' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'BarcodeSource')
            ival_ = self.gds_validate_integer(ival_, node, 'BarcodeSource')
            self.BarcodeSource = ival_
            self.BarcodeSource_nsprefix_ = child_.prefix
        elif nodeName_ == 'BarcodeId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BarcodeId')
            value_ = self.gds_validate_string(value_, node, 'BarcodeId')
            self.BarcodeId = value_
            self.BarcodeId_nsprefix_ = child_.prefix
        elif nodeName_ == 'ReceiverDepotNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'ReceiverDepotNumber')
            ival_ = self.gds_validate_integer(ival_, node, 'ReceiverDepotNumber')
            self.ReceiverDepotNumber = ival_
            self.ReceiverDepotNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'ReceiverTourNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'ReceiverTourNumber')
            ival_ = self.gds_validate_integer(ival_, node, 'ReceiverTourNumber')
            self.ReceiverTourNumber = ival_
            self.ReceiverTourNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'DeliveryRecordNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'DeliveryRecordNumber')
            ival_ = self.gds_validate_integer(ival_, node, 'DeliveryRecordNumber')
            self.DeliveryRecordNumber = ival_
            self.DeliveryRecordNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'DeliveryRecordPosition' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'DeliveryRecordPosition')
            ival_ = self.gds_validate_integer(ival_, node, 'DeliveryRecordPosition')
            self.DeliveryRecordPosition = ival_
            self.DeliveryRecordPosition_nsprefix_ = child_.prefix
# end class clsShipmentTraceBase


class SdgiData(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, StartDate=None, EndDate=None, StartTime=None, EndTime=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.StartDate = StartDate
        self.StartDate_nsprefix_ = None
        self.EndDate = EndDate
        self.EndDate_nsprefix_ = None
        self.StartTime = StartTime
        self.StartTime_nsprefix_ = None
        self.EndTime = EndTime
        self.EndTime_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SdgiData)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SdgiData.subclass:
            return SdgiData.subclass(*args_, **kwargs_)
        else:
            return SdgiData(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_StartDate(self):
        return self.StartDate
    def set_StartDate(self, StartDate):
        self.StartDate = StartDate
    def get_EndDate(self):
        return self.EndDate
    def set_EndDate(self, EndDate):
        self.EndDate = EndDate
    def get_StartTime(self):
        return self.StartTime
    def set_StartTime(self, StartTime):
        self.StartTime = StartTime
    def get_EndTime(self):
        return self.EndTime
    def set_EndTime(self, EndTime):
        self.EndTime = EndTime
    def has__content(self):
        if (
            self.StartDate is not None or
            self.EndDate is not None or
            self.StartTime is not None or
            self.EndTime is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SdgiData', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SdgiData')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SdgiData':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SdgiData')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SdgiData', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SdgiData'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SdgiData', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.StartDate is not None:
            namespaceprefix_ = self.StartDate_nsprefix_ + ':' if (UseCapturedNS_ and self.StartDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStartDate>%s</%sStartDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.StartDate), input_name='StartDate')), namespaceprefix_ , eol_))
        if self.EndDate is not None:
            namespaceprefix_ = self.EndDate_nsprefix_ + ':' if (UseCapturedNS_ and self.EndDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEndDate>%s</%sEndDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EndDate), input_name='EndDate')), namespaceprefix_ , eol_))
        if self.StartTime is not None:
            namespaceprefix_ = self.StartTime_nsprefix_ + ':' if (UseCapturedNS_ and self.StartTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStartTime>%s</%sStartTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.StartTime), input_name='StartTime')), namespaceprefix_ , eol_))
        if self.EndTime is not None:
            namespaceprefix_ = self.EndTime_nsprefix_ + ':' if (UseCapturedNS_ and self.EndTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEndTime>%s</%sEndTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EndTime), input_name='EndTime')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'StartDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'StartDate')
            value_ = self.gds_validate_string(value_, node, 'StartDate')
            self.StartDate = value_
            self.StartDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'EndDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EndDate')
            value_ = self.gds_validate_string(value_, node, 'EndDate')
            self.EndDate = value_
            self.EndDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'StartTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'StartTime')
            value_ = self.gds_validate_string(value_, node, 'StartTime')
            self.StartTime = value_
            self.StartTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'EndTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EndTime')
            value_ = self.gds_validate_string(value_, node, 'EndTime')
            self.EndTime = value_
            self.EndTime_nsprefix_ = child_.prefix
# end class SdgiData


class ArrayOfClsTrace(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, clsTrace=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if clsTrace is None:
            self.clsTrace = []
        else:
            self.clsTrace = clsTrace
        self.clsTrace_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfClsTrace)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfClsTrace.subclass:
            return ArrayOfClsTrace.subclass(*args_, **kwargs_)
        else:
            return ArrayOfClsTrace(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_clsTrace(self):
        return self.clsTrace
    def set_clsTrace(self, clsTrace):
        self.clsTrace = clsTrace
    def add_clsTrace(self, value):
        self.clsTrace.append(value)
    def insert_clsTrace_at(self, index, value):
        self.clsTrace.insert(index, value)
    def replace_clsTrace_at(self, index, value):
        self.clsTrace[index] = value
    def has__content(self):
        if (
            self.clsTrace
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfClsTrace', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfClsTrace')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfClsTrace':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfClsTrace')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfClsTrace', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfClsTrace'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfClsTrace', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for clsTrace_ in self.clsTrace:
            namespaceprefix_ = self.clsTrace_nsprefix_ + ':' if (UseCapturedNS_ and self.clsTrace_nsprefix_) else ''
            clsTrace_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='clsTrace', pretty_print=pretty_print)
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
        if nodeName_ == 'clsTrace':
            obj_ = clsTrace.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.clsTrace.append(obj_)
            obj_.original_tagname_ = 'clsTrace'
# end class ArrayOfClsTrace


class clsTrace(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ScanDate=None, ScanTime=None, StatusNumber=None, StatusDescription=None, CenterName=None, CenterNumber=None, User=None, Remark=None, Info=None, RelaisInfo=None, GeoX=None, GeoY=None, Photo=None, ParsedInfo=None, Details=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ScanDate = ScanDate
        self.ScanDate_nsprefix_ = None
        self.ScanTime = ScanTime
        self.ScanTime_nsprefix_ = None
        self.StatusNumber = StatusNumber
        self.StatusNumber_nsprefix_ = None
        self.StatusDescription = StatusDescription
        self.StatusDescription_nsprefix_ = None
        self.CenterName = CenterName
        self.CenterName_nsprefix_ = None
        self.CenterNumber = CenterNumber
        self.CenterNumber_nsprefix_ = None
        self.User = User
        self.User_nsprefix_ = None
        self.Remark = Remark
        self.Remark_nsprefix_ = None
        self.Info = Info
        self.Info_nsprefix_ = None
        self.RelaisInfo = RelaisInfo
        self.RelaisInfo_nsprefix_ = "tns"
        self.GeoX = GeoX
        self.GeoX_nsprefix_ = None
        self.GeoY = GeoY
        self.GeoY_nsprefix_ = None
        self.Photo = Photo
        self.Photo_nsprefix_ = "tns"
        self.ParsedInfo = ParsedInfo
        self.ParsedInfo_nsprefix_ = None
        self.Details = Details
        self.Details_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, clsTrace)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if clsTrace.subclass:
            return clsTrace.subclass(*args_, **kwargs_)
        else:
            return clsTrace(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ScanDate(self):
        return self.ScanDate
    def set_ScanDate(self, ScanDate):
        self.ScanDate = ScanDate
    def get_ScanTime(self):
        return self.ScanTime
    def set_ScanTime(self, ScanTime):
        self.ScanTime = ScanTime
    def get_StatusNumber(self):
        return self.StatusNumber
    def set_StatusNumber(self, StatusNumber):
        self.StatusNumber = StatusNumber
    def get_StatusDescription(self):
        return self.StatusDescription
    def set_StatusDescription(self, StatusDescription):
        self.StatusDescription = StatusDescription
    def get_CenterName(self):
        return self.CenterName
    def set_CenterName(self, CenterName):
        self.CenterName = CenterName
    def get_CenterNumber(self):
        return self.CenterNumber
    def set_CenterNumber(self, CenterNumber):
        self.CenterNumber = CenterNumber
    def get_User(self):
        return self.User
    def set_User(self, User):
        self.User = User
    def get_Remark(self):
        return self.Remark
    def set_Remark(self, Remark):
        self.Remark = Remark
    def get_Info(self):
        return self.Info
    def set_Info(self, Info):
        self.Info = Info
    def get_RelaisInfo(self):
        return self.RelaisInfo
    def set_RelaisInfo(self, RelaisInfo):
        self.RelaisInfo = RelaisInfo
    def get_GeoX(self):
        return self.GeoX
    def set_GeoX(self, GeoX):
        self.GeoX = GeoX
    def get_GeoY(self):
        return self.GeoY
    def set_GeoY(self, GeoY):
        self.GeoY = GeoY
    def get_Photo(self):
        return self.Photo
    def set_Photo(self, Photo):
        self.Photo = Photo
    def get_ParsedInfo(self):
        return self.ParsedInfo
    def set_ParsedInfo(self, ParsedInfo):
        self.ParsedInfo = ParsedInfo
    def get_Details(self):
        return self.Details
    def set_Details(self, Details):
        self.Details = Details
    def has__content(self):
        if (
            self.ScanDate is not None or
            self.ScanTime is not None or
            self.StatusNumber is not None or
            self.StatusDescription is not None or
            self.CenterName is not None or
            self.CenterNumber is not None or
            self.User is not None or
            self.Remark is not None or
            self.Info is not None or
            self.RelaisInfo is not None or
            self.GeoX is not None or
            self.GeoY is not None or
            self.Photo is not None or
            self.ParsedInfo is not None or
            self.Details is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='clsTrace', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('clsTrace')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'clsTrace':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='clsTrace')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='clsTrace', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='clsTrace'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='clsTrace', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ScanDate is not None:
            namespaceprefix_ = self.ScanDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ScanDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sScanDate>%s</%sScanDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ScanDate), input_name='ScanDate')), namespaceprefix_ , eol_))
        if self.ScanTime is not None:
            namespaceprefix_ = self.ScanTime_nsprefix_ + ':' if (UseCapturedNS_ and self.ScanTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sScanTime>%s</%sScanTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ScanTime), input_name='ScanTime')), namespaceprefix_ , eol_))
        if self.StatusNumber is not None:
            namespaceprefix_ = self.StatusNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.StatusNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStatusNumber>%s</%sStatusNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.StatusNumber, input_name='StatusNumber'), namespaceprefix_ , eol_))
        if self.StatusDescription is not None:
            namespaceprefix_ = self.StatusDescription_nsprefix_ + ':' if (UseCapturedNS_ and self.StatusDescription_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStatusDescription>%s</%sStatusDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.StatusDescription), input_name='StatusDescription')), namespaceprefix_ , eol_))
        if self.CenterName is not None:
            namespaceprefix_ = self.CenterName_nsprefix_ + ':' if (UseCapturedNS_ and self.CenterName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCenterName>%s</%sCenterName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CenterName), input_name='CenterName')), namespaceprefix_ , eol_))
        if self.CenterNumber is not None:
            namespaceprefix_ = self.CenterNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.CenterNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCenterNumber>%s</%sCenterNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CenterNumber), input_name='CenterNumber')), namespaceprefix_ , eol_))
        if self.User is not None:
            namespaceprefix_ = self.User_nsprefix_ + ':' if (UseCapturedNS_ and self.User_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUser>%s</%sUser>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.User), input_name='User')), namespaceprefix_ , eol_))
        if self.Remark is not None:
            namespaceprefix_ = self.Remark_nsprefix_ + ':' if (UseCapturedNS_ and self.Remark_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRemark>%s</%sRemark>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Remark), input_name='Remark')), namespaceprefix_ , eol_))
        if self.Info is not None:
            namespaceprefix_ = self.Info_nsprefix_ + ':' if (UseCapturedNS_ and self.Info_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sInfo>%s</%sInfo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Info), input_name='Info')), namespaceprefix_ , eol_))
        if self.RelaisInfo is not None:
            namespaceprefix_ = self.RelaisInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.RelaisInfo_nsprefix_) else ''
            self.RelaisInfo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='RelaisInfo', pretty_print=pretty_print)
        if self.GeoX is not None:
            namespaceprefix_ = self.GeoX_nsprefix_ + ':' if (UseCapturedNS_ and self.GeoX_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGeoX>%s</%sGeoX>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GeoX), input_name='GeoX')), namespaceprefix_ , eol_))
        if self.GeoY is not None:
            namespaceprefix_ = self.GeoY_nsprefix_ + ':' if (UseCapturedNS_ and self.GeoY_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGeoY>%s</%sGeoY>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GeoY), input_name='GeoY')), namespaceprefix_ , eol_))
        if self.Photo is not None:
            namespaceprefix_ = self.Photo_nsprefix_ + ':' if (UseCapturedNS_ and self.Photo_nsprefix_) else ''
            self.Photo.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Photo', pretty_print=pretty_print)
        if self.ParsedInfo is not None:
            namespaceprefix_ = self.ParsedInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.ParsedInfo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sParsedInfo>%s</%sParsedInfo>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ParsedInfo), input_name='ParsedInfo')), namespaceprefix_ , eol_))
        if self.Details is not None:
            namespaceprefix_ = self.Details_nsprefix_ + ':' if (UseCapturedNS_ and self.Details_nsprefix_) else ''
            self.Details.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Details', pretty_print=pretty_print)
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
        if nodeName_ == 'ScanDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ScanDate')
            value_ = self.gds_validate_string(value_, node, 'ScanDate')
            self.ScanDate = value_
            self.ScanDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'ScanTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ScanTime')
            value_ = self.gds_validate_string(value_, node, 'ScanTime')
            self.ScanTime = value_
            self.ScanTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'StatusNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'StatusNumber')
            ival_ = self.gds_validate_integer(ival_, node, 'StatusNumber')
            self.StatusNumber = ival_
            self.StatusNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'StatusDescription':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'StatusDescription')
            value_ = self.gds_validate_string(value_, node, 'StatusDescription')
            self.StatusDescription = value_
            self.StatusDescription_nsprefix_ = child_.prefix
        elif nodeName_ == 'CenterName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CenterName')
            value_ = self.gds_validate_string(value_, node, 'CenterName')
            self.CenterName = value_
            self.CenterName_nsprefix_ = child_.prefix
        elif nodeName_ == 'CenterNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CenterNumber')
            value_ = self.gds_validate_string(value_, node, 'CenterNumber')
            self.CenterNumber = value_
            self.CenterNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'User':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'User')
            value_ = self.gds_validate_string(value_, node, 'User')
            self.User = value_
            self.User_nsprefix_ = child_.prefix
        elif nodeName_ == 'Remark':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Remark')
            value_ = self.gds_validate_string(value_, node, 'Remark')
            self.Remark = value_
            self.Remark_nsprefix_ = child_.prefix
        elif nodeName_ == 'Info':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Info')
            value_ = self.gds_validate_string(value_, node, 'Info')
            self.Info = value_
            self.Info_nsprefix_ = child_.prefix
        elif nodeName_ == 'RelaisInfo':
            obj_ = RelaisInfo.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.RelaisInfo = obj_
            obj_.original_tagname_ = 'RelaisInfo'
        elif nodeName_ == 'GeoX':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GeoX')
            value_ = self.gds_validate_string(value_, node, 'GeoX')
            self.GeoX = value_
            self.GeoX_nsprefix_ = child_.prefix
        elif nodeName_ == 'GeoY':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GeoY')
            value_ = self.gds_validate_string(value_, node, 'GeoY')
            self.GeoY = value_
            self.GeoY_nsprefix_ = child_.prefix
        elif nodeName_ == 'Photo':
            obj_ = ArrayOfTracePhoto.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Photo = obj_
            obj_.original_tagname_ = 'Photo'
        elif nodeName_ == 'ParsedInfo':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ParsedInfo')
            value_ = self.gds_validate_string(value_, node, 'ParsedInfo')
            self.ParsedInfo = value_
            self.ParsedInfo_nsprefix_ = child_.prefix
        elif nodeName_ == 'Details':
            obj_ = ArrayOfClsTraceDetails.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Details = obj_
            obj_.original_tagname_ = 'Details'
# end class clsTrace


class RelaisInfo(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ID=None, CNSid=None, Name=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ID = ID
        self.ID_nsprefix_ = None
        self.CNSid = CNSid
        self.CNSid_nsprefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RelaisInfo)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RelaisInfo.subclass:
            return RelaisInfo.subclass(*args_, **kwargs_)
        else:
            return RelaisInfo(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ID(self):
        return self.ID
    def set_ID(self, ID):
        self.ID = ID
    def get_CNSid(self):
        return self.CNSid
    def set_CNSid(self, CNSid):
        self.CNSid = CNSid
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def has__content(self):
        if (
            self.ID is not None or
            self.CNSid is not None or
            self.Name is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RelaisInfo', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RelaisInfo')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RelaisInfo':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RelaisInfo')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RelaisInfo', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RelaisInfo'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RelaisInfo', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ID is not None:
            namespaceprefix_ = self.ID_nsprefix_ + ':' if (UseCapturedNS_ and self.ID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sID>%s</%sID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ID), input_name='ID')), namespaceprefix_ , eol_))
        if self.CNSid is not None:
            namespaceprefix_ = self.CNSid_nsprefix_ + ':' if (UseCapturedNS_ and self.CNSid_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCNSid>%s</%sCNSid>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CNSid), input_name='CNSid')), namespaceprefix_ , eol_))
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName>%s</%sName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name), input_name='Name')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ID')
            value_ = self.gds_validate_string(value_, node, 'ID')
            self.ID = value_
            self.ID_nsprefix_ = child_.prefix
        elif nodeName_ == 'CNSid':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CNSid')
            value_ = self.gds_validate_string(value_, node, 'CNSid')
            self.CNSid = value_
            self.CNSid_nsprefix_ = child_.prefix
        elif nodeName_ == 'Name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Name')
            value_ = self.gds_validate_string(value_, node, 'Name')
            self.Name = value_
            self.Name_nsprefix_ = child_.prefix
# end class RelaisInfo


class ArrayOfTracePhoto(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TracePhoto=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if TracePhoto is None:
            self.TracePhoto = []
        else:
            self.TracePhoto = TracePhoto
        self.TracePhoto_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfTracePhoto)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfTracePhoto.subclass:
            return ArrayOfTracePhoto.subclass(*args_, **kwargs_)
        else:
            return ArrayOfTracePhoto(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_TracePhoto(self):
        return self.TracePhoto
    def set_TracePhoto(self, TracePhoto):
        self.TracePhoto = TracePhoto
    def add_TracePhoto(self, value):
        self.TracePhoto.append(value)
    def insert_TracePhoto_at(self, index, value):
        self.TracePhoto.insert(index, value)
    def replace_TracePhoto_at(self, index, value):
        self.TracePhoto[index] = value
    def has__content(self):
        if (
            self.TracePhoto
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfTracePhoto', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfTracePhoto')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfTracePhoto':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfTracePhoto')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfTracePhoto', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfTracePhoto'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfTracePhoto', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for TracePhoto_ in self.TracePhoto:
            namespaceprefix_ = self.TracePhoto_nsprefix_ + ':' if (UseCapturedNS_ and self.TracePhoto_nsprefix_) else ''
            TracePhoto_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='TracePhoto', pretty_print=pretty_print)
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
        if nodeName_ == 'TracePhoto':
            obj_ = TracePhoto.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.TracePhoto.append(obj_)
            obj_.original_tagname_ = 'TracePhoto'
# end class ArrayOfTracePhoto


class TracePhoto(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Image=None, Type=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Image = Image
        self.Image_nsprefix_ = None
        self.Type = Type
        self.Type_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TracePhoto)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TracePhoto.subclass:
            return TracePhoto.subclass(*args_, **kwargs_)
        else:
            return TracePhoto(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Image(self):
        return self.Image
    def set_Image(self, Image):
        self.Image = Image
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def has__content(self):
        if (
            self.Image is not None or
            self.Type is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TracePhoto', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TracePhoto')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TracePhoto':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TracePhoto')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TracePhoto', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TracePhoto'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TracePhoto', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Image is not None:
            namespaceprefix_ = self.Image_nsprefix_ + ':' if (UseCapturedNS_ and self.Image_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sImage>%s</%sImage>%s' % (namespaceprefix_ , self.gds_format_base64(self.Image, input_name='Image'), namespaceprefix_ , eol_))
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sType>%s</%sType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Type), input_name='Type')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'Image':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'Image')
            else:
                bval_ = None
            self.Image = bval_
            self.Image_nsprefix_ = child_.prefix
        elif nodeName_ == 'Type':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Type')
            value_ = self.gds_validate_string(value_, node, 'Type')
            self.Type = value_
            self.Type_nsprefix_ = child_.prefix
# end class TracePhoto


class ArrayOfClsTraceDetails(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, clsTraceDetails=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if clsTraceDetails is None:
            self.clsTraceDetails = []
        else:
            self.clsTraceDetails = clsTraceDetails
        self.clsTraceDetails_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfClsTraceDetails)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfClsTraceDetails.subclass:
            return ArrayOfClsTraceDetails.subclass(*args_, **kwargs_)
        else:
            return ArrayOfClsTraceDetails(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_clsTraceDetails(self):
        return self.clsTraceDetails
    def set_clsTraceDetails(self, clsTraceDetails):
        self.clsTraceDetails = clsTraceDetails
    def add_clsTraceDetails(self, value):
        self.clsTraceDetails.append(value)
    def insert_clsTraceDetails_at(self, index, value):
        self.clsTraceDetails.insert(index, value)
    def replace_clsTraceDetails_at(self, index, value):
        self.clsTraceDetails[index] = value
    def has__content(self):
        if (
            self.clsTraceDetails
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfClsTraceDetails', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfClsTraceDetails')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfClsTraceDetails':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfClsTraceDetails')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfClsTraceDetails', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfClsTraceDetails'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfClsTraceDetails', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for clsTraceDetails_ in self.clsTraceDetails:
            namespaceprefix_ = self.clsTraceDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.clsTraceDetails_nsprefix_) else ''
            clsTraceDetails_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='clsTraceDetails', pretty_print=pretty_print)
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
        if nodeName_ == 'clsTraceDetails':
            obj_ = clsTraceDetails.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.clsTraceDetails.append(obj_)
            obj_.original_tagname_ = 'clsTraceDetails'
# end class ArrayOfClsTraceDetails


class clsTraceDetails(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ID=None, Text=None, Data=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ID = ID
        self.ID_nsprefix_ = None
        self.Text = Text
        self.Text_nsprefix_ = None
        self.Data = Data
        self.Data_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, clsTraceDetails)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if clsTraceDetails.subclass:
            return clsTraceDetails.subclass(*args_, **kwargs_)
        else:
            return clsTraceDetails(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ID(self):
        return self.ID
    def set_ID(self, ID):
        self.ID = ID
    def get_Text(self):
        return self.Text
    def set_Text(self, Text):
        self.Text = Text
    def get_Data(self):
        return self.Data
    def set_Data(self, Data):
        self.Data = Data
    def has__content(self):
        if (
            self.ID is not None or
            self.Text is not None or
            self.Data is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='clsTraceDetails', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('clsTraceDetails')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'clsTraceDetails':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='clsTraceDetails')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='clsTraceDetails', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='clsTraceDetails'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='clsTraceDetails', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ID is not None:
            namespaceprefix_ = self.ID_nsprefix_ + ':' if (UseCapturedNS_ and self.ID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sID>%s</%sID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ID), input_name='ID')), namespaceprefix_ , eol_))
        if self.Text is not None:
            namespaceprefix_ = self.Text_nsprefix_ + ':' if (UseCapturedNS_ and self.Text_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sText>%s</%sText>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Text), input_name='Text')), namespaceprefix_ , eol_))
        if self.Data is not None:
            namespaceprefix_ = self.Data_nsprefix_ + ':' if (UseCapturedNS_ and self.Data_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sData>%s</%sData>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Data), input_name='Data')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ID')
            value_ = self.gds_validate_string(value_, node, 'ID')
            self.ID = value_
            self.ID_nsprefix_ = child_.prefix
        elif nodeName_ == 'Text':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Text')
            value_ = self.gds_validate_string(value_, node, 'Text')
            self.Text = value_
            self.Text_nsprefix_ = child_.prefix
        elif nodeName_ == 'Data':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Data')
            value_ = self.gds_validate_string(value_, node, 'Data')
            self.Data = value_
            self.Data_nsprefix_ = child_.prefix
# end class clsTraceDetails


class ArrayOfServiceInfo(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ServiceInfo=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if ServiceInfo is None:
            self.ServiceInfo = []
        else:
            self.ServiceInfo = ServiceInfo
        self.ServiceInfo_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfServiceInfo)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfServiceInfo.subclass:
            return ArrayOfServiceInfo.subclass(*args_, **kwargs_)
        else:
            return ArrayOfServiceInfo(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ServiceInfo(self):
        return self.ServiceInfo
    def set_ServiceInfo(self, ServiceInfo):
        self.ServiceInfo = ServiceInfo
    def add_ServiceInfo(self, value):
        self.ServiceInfo.append(value)
    def insert_ServiceInfo_at(self, index, value):
        self.ServiceInfo.insert(index, value)
    def replace_ServiceInfo_at(self, index, value):
        self.ServiceInfo[index] = value
    def has__content(self):
        if (
            self.ServiceInfo
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfServiceInfo', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfServiceInfo')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfServiceInfo':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfServiceInfo')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfServiceInfo', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfServiceInfo'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfServiceInfo', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for ServiceInfo_ in self.ServiceInfo:
            namespaceprefix_ = self.ServiceInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceInfo_nsprefix_) else ''
            ServiceInfo_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ServiceInfo', pretty_print=pretty_print)
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
        if nodeName_ == 'ServiceInfo':
            obj_ = ServiceInfo.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ServiceInfo.append(obj_)
            obj_.original_tagname_ = 'ServiceInfo'
# end class ArrayOfServiceInfo


class ServiceInfo(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Name=None, Type=None, Attribute=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = None
        self.Type = Type
        self.Type_nsprefix_ = None
        self.Attribute = Attribute
        self.Attribute_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ServiceInfo)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ServiceInfo.subclass:
            return ServiceInfo.subclass(*args_, **kwargs_)
        else:
            return ServiceInfo(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_Attribute(self):
        return self.Attribute
    def set_Attribute(self, Attribute):
        self.Attribute = Attribute
    def has__content(self):
        if (
            self.Name is not None or
            self.Type is not None or
            self.Attribute is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ServiceInfo', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ServiceInfo')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ServiceInfo':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ServiceInfo')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ServiceInfo', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ServiceInfo'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ServiceInfo', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName>%s</%sName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name), input_name='Name')), namespaceprefix_ , eol_))
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sType>%s</%sType>%s' % (namespaceprefix_ , self.gds_format_integer(self.Type, input_name='Type'), namespaceprefix_ , eol_))
        if self.Attribute is not None:
            namespaceprefix_ = self.Attribute_nsprefix_ + ':' if (UseCapturedNS_ and self.Attribute_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAttribute>%s</%sAttribute>%s' % (namespaceprefix_ , self.gds_format_integer(self.Attribute, input_name='Attribute'), namespaceprefix_ , eol_))
        if self.Attribute is None:
            namespaceprefix_ = self.Attribute_nsprefix_ + ':' if (UseCapturedNS_ and self.Attribute_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAttribute xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>%s' % (namespaceprefix_,eol_))
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
        elif nodeName_ == 'Type' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Type')
            ival_ = self.gds_validate_integer(ival_, node, 'Type')
            self.Type = ival_
            self.Type_nsprefix_ = child_.prefix
        elif nodeName_ == 'Attribute' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Attribute')
            ival_ = self.gds_validate_integer(ival_, node, 'Attribute')
            self.Attribute = ival_
            self.Attribute_nsprefix_ = child_.prefix
# end class ServiceInfo


class ArrayOfImage(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Image=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Image is None:
            self.Image = []
        else:
            self.Image = Image
        self.Image_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfImage)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfImage.subclass:
            return ArrayOfImage.subclass(*args_, **kwargs_)
        else:
            return ArrayOfImage(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Image(self):
        return self.Image
    def set_Image(self, Image):
        self.Image = Image
    def add_Image(self, value):
        self.Image.append(value)
    def insert_Image_at(self, index, value):
        self.Image.insert(index, value)
    def replace_Image_at(self, index, value):
        self.Image[index] = value
    def has__content(self):
        if (
            self.Image
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfImage', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfImage')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfImage':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfImage')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfImage', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfImage'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfImage', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Image_ in self.Image:
            namespaceprefix_ = self.Image_nsprefix_ + ':' if (UseCapturedNS_ and self.Image_nsprefix_) else ''
            Image_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Image', pretty_print=pretty_print)
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
        if nodeName_ == 'Image':
            obj_ = Image.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Image.append(obj_)
            obj_.original_tagname_ = 'Image'
# end class ArrayOfImage


class Image(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, type_=None, image=None, date=None, time=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.type_ = type_
        self.validate_ImageType(self.type_)
        self.type__nsprefix_ = "tns"
        self.image = image
        self.image_nsprefix_ = None
        self.date = date
        self.date_nsprefix_ = None
        self.time = time
        self.time_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Image)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Image.subclass:
            return Image.subclass(*args_, **kwargs_)
        else:
            return Image(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_type(self):
        return self.type_
    def set_type(self, type_):
        self.type_ = type_
    def get_image(self):
        return self.image
    def set_image(self, image):
        self.image = image
    def get_date(self):
        return self.date
    def set_date(self, date):
        self.date = date
    def get_time(self):
        return self.time
    def set_time(self, time):
        self.time = time
    def validate_ImageType(self, value):
        result = True
        # Validate type ImageType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['POD', 'POA', 'DeliverySignature', 'DeliveryShop', 'PickupSignature']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ImageType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.type_ is not None or
            self.image is not None or
            self.date is not None or
            self.time is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Image', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Image')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Image':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Image')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Image', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Image'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Image', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.type_ is not None:
            namespaceprefix_ = self.type__nsprefix_ + ':' if (UseCapturedNS_ and self.type__nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stype>%s</%stype>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.type_), input_name='type')), namespaceprefix_ , eol_))
        if self.image is not None:
            namespaceprefix_ = self.image_nsprefix_ + ':' if (UseCapturedNS_ and self.image_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%simage>%s</%simage>%s' % (namespaceprefix_ , self.gds_format_base64(self.image, input_name='image'), namespaceprefix_ , eol_))
        if self.date is not None:
            namespaceprefix_ = self.date_nsprefix_ + ':' if (UseCapturedNS_ and self.date_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdate>%s</%sdate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.date), input_name='date')), namespaceprefix_ , eol_))
        if self.time is not None:
            namespaceprefix_ = self.time_nsprefix_ + ':' if (UseCapturedNS_ and self.time_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stime>%s</%stime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.time), input_name='time')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'type':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'type')
            value_ = self.gds_validate_string(value_, node, 'type')
            self.type_ = value_
            self.type_nsprefix_ = child_.prefix
            # validate type ImageType
            self.validate_ImageType(self.type_)
        elif nodeName_ == 'image':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'image')
            else:
                bval_ = None
            self.image = bval_
            self.image_nsprefix_ = child_.prefix
        elif nodeName_ == 'date':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'date')
            value_ = self.gds_validate_string(value_, node, 'date')
            self.date = value_
            self.date_nsprefix_ = child_.prefix
        elif nodeName_ == 'time':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'time')
            value_ = self.gds_validate_string(value_, node, 'time')
            self.time = value_
            self.time_nsprefix_ = child_.prefix
# end class Image


class GetShipmentTrace(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, request=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.request = request
        self.request_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetShipmentTrace)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetShipmentTrace.subclass:
            return GetShipmentTrace.subclass(*args_, **kwargs_)
        else:
            return GetShipmentTrace(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_request(self):
        return self.request
    def set_request(self, request):
        self.request = request
    def has__content(self):
        if (
            self.request is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetShipmentTrace', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetShipmentTrace')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetShipmentTrace':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetShipmentTrace')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetShipmentTrace', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetShipmentTrace'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetShipmentTrace', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.request is not None:
            namespaceprefix_ = self.request_nsprefix_ + ':' if (UseCapturedNS_ and self.request_nsprefix_) else ''
            self.request.export(outfile, level, namespaceprefix_, namespacedef_='', name_='request', pretty_print=pretty_print)
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
        if nodeName_ == 'request':
            obj_ = ShipmentDetailRequest.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.request = obj_
            obj_.original_tagname_ = 'request'
# end class GetShipmentTrace


class GetShipmentTraceResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetShipmentTraceResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetShipmentTraceResult = GetShipmentTraceResult
        self.GetShipmentTraceResult_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetShipmentTraceResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetShipmentTraceResponse.subclass:
            return GetShipmentTraceResponse.subclass(*args_, **kwargs_)
        else:
            return GetShipmentTraceResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetShipmentTraceResult(self):
        return self.GetShipmentTraceResult
    def set_GetShipmentTraceResult(self, GetShipmentTraceResult):
        self.GetShipmentTraceResult = GetShipmentTraceResult
    def has__content(self):
        if (
            self.GetShipmentTraceResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetShipmentTraceResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetShipmentTraceResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetShipmentTraceResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetShipmentTraceResponse')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetShipmentTraceResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetShipmentTraceResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetShipmentTraceResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetShipmentTraceResult is not None:
            namespaceprefix_ = self.GetShipmentTraceResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetShipmentTraceResult_nsprefix_) else ''
            self.GetShipmentTraceResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetShipmentTraceResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GetShipmentTraceResult':
            obj_ = ArrayOfShipmentTrace.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetShipmentTraceResult = obj_
            obj_.original_tagname_ = 'GetShipmentTraceResult'
# end class GetShipmentTraceResponse


class ArrayOfShipmentTrace(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ShipmentTrace=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if ShipmentTrace is None:
            self.ShipmentTrace = []
        else:
            self.ShipmentTrace = ShipmentTrace
        self.ShipmentTrace_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfShipmentTrace)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfShipmentTrace.subclass:
            return ArrayOfShipmentTrace.subclass(*args_, **kwargs_)
        else:
            return ArrayOfShipmentTrace(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ShipmentTrace(self):
        return self.ShipmentTrace
    def set_ShipmentTrace(self, ShipmentTrace):
        self.ShipmentTrace = ShipmentTrace
    def add_ShipmentTrace(self, value):
        self.ShipmentTrace.append(value)
    def insert_ShipmentTrace_at(self, index, value):
        self.ShipmentTrace.insert(index, value)
    def replace_ShipmentTrace_at(self, index, value):
        self.ShipmentTrace[index] = value
    def has__content(self):
        if (
            self.ShipmentTrace
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfShipmentTrace', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfShipmentTrace')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfShipmentTrace':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfShipmentTrace')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfShipmentTrace', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfShipmentTrace'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfShipmentTrace', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for ShipmentTrace_ in self.ShipmentTrace:
            namespaceprefix_ = self.ShipmentTrace_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentTrace_nsprefix_) else ''
            ShipmentTrace_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentTrace', pretty_print=pretty_print)
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
        if nodeName_ == 'ShipmentTrace':
            obj_ = ShipmentTrace.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentTrace.append(obj_)
            obj_.original_tagname_ = 'ShipmentTrace'
# end class ArrayOfShipmentTrace


class GetShipmentTraceByReference(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, request=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.request = request
        self.request_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetShipmentTraceByReference)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetShipmentTraceByReference.subclass:
            return GetShipmentTraceByReference.subclass(*args_, **kwargs_)
        else:
            return GetShipmentTraceByReference(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_request(self):
        return self.request
    def set_request(self, request):
        self.request = request
    def has__content(self):
        if (
            self.request is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetShipmentTraceByReference', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetShipmentTraceByReference')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetShipmentTraceByReference':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetShipmentTraceByReference')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetShipmentTraceByReference', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetShipmentTraceByReference'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetShipmentTraceByReference', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.request is not None:
            namespaceprefix_ = self.request_nsprefix_ + ':' if (UseCapturedNS_ and self.request_nsprefix_) else ''
            self.request.export(outfile, level, namespaceprefix_, namespacedef_='', name_='request', pretty_print=pretty_print)
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
        if nodeName_ == 'request':
            obj_ = ReferenceDetailRequest.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.request = obj_
            obj_.original_tagname_ = 'request'
# end class GetShipmentTraceByReference


class ReferenceBaseRequest(RequestBase):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = RequestBase
    def __init__(self, Customer=None, Language=None, Reference=None, ShippingDate=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("ReferenceBaseRequest"), self).__init__(Customer, Language, extensiontype_,  **kwargs_)
        self.Reference = Reference
        self.Reference_nsprefix_ = None
        self.ShippingDate = ShippingDate
        self.ShippingDate_nsprefix_ = None
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ReferenceBaseRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ReferenceBaseRequest.subclass:
            return ReferenceBaseRequest.subclass(*args_, **kwargs_)
        else:
            return ReferenceBaseRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Reference(self):
        return self.Reference
    def set_Reference(self, Reference):
        self.Reference = Reference
    def get_ShippingDate(self):
        return self.ShippingDate
    def set_ShippingDate(self, ShippingDate):
        self.ShippingDate = ShippingDate
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def has__content(self):
        if (
            self.Reference is not None or
            self.ShippingDate is not None or
            super(ReferenceBaseRequest, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReferenceBaseRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ReferenceBaseRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ReferenceBaseRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ReferenceBaseRequest')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ReferenceBaseRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ReferenceBaseRequest'):
        super(ReferenceBaseRequest, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ReferenceBaseRequest')
        if self.extensiontype_ is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self.extensiontype_:
                imported_ns_type_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.extensiontype_, '')
                outfile.write(' xsi:type="%s%s"' % (imported_ns_type_prefix_, self.extensiontype_))
            else:
                outfile.write(' xsi:type="%s"' % self.extensiontype_)
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReferenceBaseRequest', fromsubclass_=False, pretty_print=True):
        super(ReferenceBaseRequest, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Reference is not None:
            namespaceprefix_ = self.Reference_nsprefix_ + ':' if (UseCapturedNS_ and self.Reference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReference>%s</%sReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Reference), input_name='Reference')), namespaceprefix_ , eol_))
        if self.ShippingDate is not None:
            namespaceprefix_ = self.ShippingDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ShippingDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShippingDate>%s</%sShippingDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShippingDate), input_name='ShippingDate')), namespaceprefix_ , eol_))
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
        super(ReferenceBaseRequest, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Reference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Reference')
            value_ = self.gds_validate_string(value_, node, 'Reference')
            self.Reference = value_
            self.Reference_nsprefix_ = child_.prefix
        elif nodeName_ == 'ShippingDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShippingDate')
            value_ = self.gds_validate_string(value_, node, 'ShippingDate')
            self.ShippingDate = value_
            self.ShippingDate_nsprefix_ = child_.prefix
        super(ReferenceBaseRequest, self)._buildChildren(child_, node, nodeName_, True)
# end class ReferenceBaseRequest


class GetShipmentTraceByReferenceResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetShipmentTraceByReferenceResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetShipmentTraceByReferenceResult = GetShipmentTraceByReferenceResult
        self.GetShipmentTraceByReferenceResult_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetShipmentTraceByReferenceResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetShipmentTraceByReferenceResponse.subclass:
            return GetShipmentTraceByReferenceResponse.subclass(*args_, **kwargs_)
        else:
            return GetShipmentTraceByReferenceResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetShipmentTraceByReferenceResult(self):
        return self.GetShipmentTraceByReferenceResult
    def set_GetShipmentTraceByReferenceResult(self, GetShipmentTraceByReferenceResult):
        self.GetShipmentTraceByReferenceResult = GetShipmentTraceByReferenceResult
    def has__content(self):
        if (
            self.GetShipmentTraceByReferenceResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetShipmentTraceByReferenceResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetShipmentTraceByReferenceResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetShipmentTraceByReferenceResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetShipmentTraceByReferenceResponse')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetShipmentTraceByReferenceResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetShipmentTraceByReferenceResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetShipmentTraceByReferenceResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetShipmentTraceByReferenceResult is not None:
            namespaceprefix_ = self.GetShipmentTraceByReferenceResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetShipmentTraceByReferenceResult_nsprefix_) else ''
            self.GetShipmentTraceByReferenceResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetShipmentTraceByReferenceResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GetShipmentTraceByReferenceResult':
            obj_ = ArrayOfShipmentTrace.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetShipmentTraceByReferenceResult = obj_
            obj_.original_tagname_ = 'GetShipmentTraceByReferenceResult'
# end class GetShipmentTraceByReferenceResponse


class GetLastTrace(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, request=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.request = request
        self.request_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetLastTrace)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetLastTrace.subclass:
            return GetLastTrace.subclass(*args_, **kwargs_)
        else:
            return GetLastTrace(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_request(self):
        return self.request
    def set_request(self, request):
        self.request = request
    def has__content(self):
        if (
            self.request is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLastTrace', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetLastTrace')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetLastTrace':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetLastTrace')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetLastTrace', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetLastTrace'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLastTrace', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.request is not None:
            namespaceprefix_ = self.request_nsprefix_ + ':' if (UseCapturedNS_ and self.request_nsprefix_) else ''
            self.request.export(outfile, level, namespaceprefix_, namespacedef_='', name_='request', pretty_print=pretty_print)
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
        if nodeName_ == 'request':
            obj_ = GetLastTraceRequest.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.request = obj_
            obj_.original_tagname_ = 'request'
# end class GetLastTrace


class GetLastTraceBaseRequest(RequestBase):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = RequestBase
    def __init__(self, Customer=None, Language=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("GetLastTraceBaseRequest"), self).__init__(Customer, Language, extensiontype_,  **kwargs_)
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetLastTraceBaseRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetLastTraceBaseRequest.subclass:
            return GetLastTraceBaseRequest.subclass(*args_, **kwargs_)
        else:
            return GetLastTraceBaseRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def has__content(self):
        if (
            super(GetLastTraceBaseRequest, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLastTraceBaseRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetLastTraceBaseRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetLastTraceBaseRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetLastTraceBaseRequest')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetLastTraceBaseRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetLastTraceBaseRequest'):
        super(GetLastTraceBaseRequest, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetLastTraceBaseRequest')
        if self.extensiontype_ is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self.extensiontype_:
                imported_ns_type_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.extensiontype_, '')
                outfile.write(' xsi:type="%s%s"' % (imported_ns_type_prefix_, self.extensiontype_))
            else:
                outfile.write(' xsi:type="%s"' % self.extensiontype_)
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLastTraceBaseRequest', fromsubclass_=False, pretty_print=True):
        super(GetLastTraceBaseRequest, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
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
        super(GetLastTraceBaseRequest, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        super(GetLastTraceBaseRequest, self)._buildChildren(child_, node, nodeName_, True)
        pass
# end class GetLastTraceBaseRequest


class ArrayOfParcel(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Parcel=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Parcel is None:
            self.Parcel = []
        else:
            self.Parcel = Parcel
        self.Parcel_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfParcel)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfParcel.subclass:
            return ArrayOfParcel.subclass(*args_, **kwargs_)
        else:
            return ArrayOfParcel(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Parcel(self):
        return self.Parcel
    def set_Parcel(self, Parcel):
        self.Parcel = Parcel
    def add_Parcel(self, value):
        self.Parcel.append(value)
    def insert_Parcel_at(self, index, value):
        self.Parcel.insert(index, value)
    def replace_Parcel_at(self, index, value):
        self.Parcel[index] = value
    def has__content(self):
        if (
            self.Parcel
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfParcel', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfParcel')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfParcel':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfParcel')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfParcel', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfParcel'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfParcel', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Parcel_ in self.Parcel:
            namespaceprefix_ = self.Parcel_nsprefix_ + ':' if (UseCapturedNS_ and self.Parcel_nsprefix_) else ''
            Parcel_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Parcel', pretty_print=pretty_print)
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
        if nodeName_ == 'Parcel':
            obj_ = Parcel.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Parcel.append(obj_)
            obj_.original_tagname_ = 'Parcel'
# end class ArrayOfParcel


class Parcel(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, countrycode=None, centernumber=None, parcelnumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.countrycode = countrycode
        self.countrycode_nsprefix_ = None
        self.centernumber = centernumber
        self.centernumber_nsprefix_ = None
        self.parcelnumber = parcelnumber
        self.parcelnumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Parcel)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Parcel.subclass:
            return Parcel.subclass(*args_, **kwargs_)
        else:
            return Parcel(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_countrycode(self):
        return self.countrycode
    def set_countrycode(self, countrycode):
        self.countrycode = countrycode
    def get_centernumber(self):
        return self.centernumber
    def set_centernumber(self, centernumber):
        self.centernumber = centernumber
    def get_parcelnumber(self):
        return self.parcelnumber
    def set_parcelnumber(self, parcelnumber):
        self.parcelnumber = parcelnumber
    def has__content(self):
        if (
            self.countrycode is not None or
            self.centernumber is not None or
            self.parcelnumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Parcel', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Parcel')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Parcel':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Parcel')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Parcel', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Parcel'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Parcel', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.countrycode is not None:
            namespaceprefix_ = self.countrycode_nsprefix_ + ':' if (UseCapturedNS_ and self.countrycode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scountrycode>%s</%scountrycode>%s' % (namespaceprefix_ , self.gds_format_integer(self.countrycode, input_name='countrycode'), namespaceprefix_ , eol_))
        if self.centernumber is not None:
            namespaceprefix_ = self.centernumber_nsprefix_ + ':' if (UseCapturedNS_ and self.centernumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scenternumber>%s</%scenternumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.centernumber, input_name='centernumber'), namespaceprefix_ , eol_))
        if self.parcelnumber is not None:
            namespaceprefix_ = self.parcelnumber_nsprefix_ + ':' if (UseCapturedNS_ and self.parcelnumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sparcelnumber>%s</%sparcelnumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.parcelnumber, input_name='parcelnumber'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'countrycode' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'countrycode')
            ival_ = self.gds_validate_integer(ival_, node, 'countrycode')
            self.countrycode = ival_
            self.countrycode_nsprefix_ = child_.prefix
        elif nodeName_ == 'centernumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'centernumber')
            ival_ = self.gds_validate_integer(ival_, node, 'centernumber')
            self.centernumber = ival_
            self.centernumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'parcelnumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'parcelnumber')
            ival_ = self.gds_validate_integer(ival_, node, 'parcelnumber')
            self.parcelnumber = ival_
            self.parcelnumber_nsprefix_ = child_.prefix
# end class Parcel


class GetLastTraceResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetLastTraceResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetLastTraceResult = GetLastTraceResult
        self.GetLastTraceResult_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetLastTraceResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetLastTraceResponse.subclass:
            return GetLastTraceResponse.subclass(*args_, **kwargs_)
        else:
            return GetLastTraceResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetLastTraceResult(self):
        return self.GetLastTraceResult
    def set_GetLastTraceResult(self, GetLastTraceResult):
        self.GetLastTraceResult = GetLastTraceResult
    def has__content(self):
        if (
            self.GetLastTraceResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLastTraceResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetLastTraceResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetLastTraceResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetLastTraceResponse')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetLastTraceResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetLastTraceResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLastTraceResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetLastTraceResult is not None:
            namespaceprefix_ = self.GetLastTraceResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetLastTraceResult_nsprefix_) else ''
            self.GetLastTraceResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetLastTraceResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GetLastTraceResult':
            obj_ = ArrayOfGetLastTraceResponse.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetLastTraceResult = obj_
            obj_.original_tagname_ = 'GetLastTraceResult'
# end class GetLastTraceResponse


class ArrayOfGetLastTraceResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetLastTraceResponse=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if GetLastTraceResponse is None:
            self.GetLastTraceResponse = []
        else:
            self.GetLastTraceResponse = GetLastTraceResponse
        self.GetLastTraceResponse_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfGetLastTraceResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfGetLastTraceResponse.subclass:
            return ArrayOfGetLastTraceResponse.subclass(*args_, **kwargs_)
        else:
            return ArrayOfGetLastTraceResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetLastTraceResponse(self):
        return self.GetLastTraceResponse
    def set_GetLastTraceResponse(self, GetLastTraceResponse):
        self.GetLastTraceResponse = GetLastTraceResponse
    def add_GetLastTraceResponse(self, value):
        self.GetLastTraceResponse.append(value)
    def insert_GetLastTraceResponse_at(self, index, value):
        self.GetLastTraceResponse.insert(index, value)
    def replace_GetLastTraceResponse_at(self, index, value):
        self.GetLastTraceResponse[index] = value
    def has__content(self):
        if (
            self.GetLastTraceResponse
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfGetLastTraceResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfGetLastTraceResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfGetLastTraceResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfGetLastTraceResponse')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfGetLastTraceResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfGetLastTraceResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfGetLastTraceResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for GetLastTraceResponse_ in self.GetLastTraceResponse:
            namespaceprefix_ = self.GetLastTraceResponse_nsprefix_ + ':' if (UseCapturedNS_ and self.GetLastTraceResponse_nsprefix_) else ''
            GetLastTraceResponse_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetLastTraceResponse', pretty_print=pretty_print)
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
        if nodeName_ == 'GetLastTraceResponse':
            obj_ = GetLastTraceResponse.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetLastTraceResponse.append(obj_)
            obj_.original_tagname_ = 'GetLastTraceResponse'
# end class ArrayOfGetLastTraceResponse


class GetLastTraceBaseResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Trace=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Trace = Trace
        self.Trace_nsprefix_ = "tns"
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetLastTraceBaseResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetLastTraceBaseResponse.subclass:
            return GetLastTraceBaseResponse.subclass(*args_, **kwargs_)
        else:
            return GetLastTraceBaseResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Trace(self):
        return self.Trace
    def set_Trace(self, Trace):
        self.Trace = Trace
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def has__content(self):
        if (
            self.Trace is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLastTraceBaseResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetLastTraceBaseResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetLastTraceBaseResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetLastTraceBaseResponse')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetLastTraceBaseResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetLastTraceBaseResponse'):
        if self.extensiontype_ is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self.extensiontype_:
                imported_ns_type_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.extensiontype_, '')
                outfile.write(' xsi:type="%s%s"' % (imported_ns_type_prefix_, self.extensiontype_))
            else:
                outfile.write(' xsi:type="%s"' % self.extensiontype_)
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLastTraceBaseResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Trace is not None:
            namespaceprefix_ = self.Trace_nsprefix_ + ':' if (UseCapturedNS_ and self.Trace_nsprefix_) else ''
            self.Trace.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Trace', pretty_print=pretty_print)
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
        if nodeName_ == 'Trace':
            obj_ = clsTrace.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Trace = obj_
            obj_.original_tagname_ = 'Trace'
# end class GetLastTraceBaseResponse


class GetLastTraceBc(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, request=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.request = request
        self.request_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetLastTraceBc)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetLastTraceBc.subclass:
            return GetLastTraceBc.subclass(*args_, **kwargs_)
        else:
            return GetLastTraceBc(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_request(self):
        return self.request
    def set_request(self, request):
        self.request = request
    def has__content(self):
        if (
            self.request is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLastTraceBc', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetLastTraceBc')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetLastTraceBc':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetLastTraceBc')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetLastTraceBc', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetLastTraceBc'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLastTraceBc', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.request is not None:
            namespaceprefix_ = self.request_nsprefix_ + ':' if (UseCapturedNS_ and self.request_nsprefix_) else ''
            self.request.export(outfile, level, namespaceprefix_, namespacedef_='', name_='request', pretty_print=pretty_print)
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
        if nodeName_ == 'request':
            obj_ = GetLastTraceBcRequest.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.request = obj_
            obj_.original_tagname_ = 'request'
# end class GetLastTraceBc


class GetLastTraceBcRequest(GetLastTraceBaseRequest):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = GetLastTraceBaseRequest
    def __init__(self, Customer=None, Language=None, Parcels=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("GetLastTraceBcRequest"), self).__init__(Customer, Language,  **kwargs_)
        self.Parcels = Parcels
        self.Parcels_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetLastTraceBcRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetLastTraceBcRequest.subclass:
            return GetLastTraceBcRequest.subclass(*args_, **kwargs_)
        else:
            return GetLastTraceBcRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Parcels(self):
        return self.Parcels
    def set_Parcels(self, Parcels):
        self.Parcels = Parcels
    def has__content(self):
        if (
            self.Parcels is not None or
            super(GetLastTraceBcRequest, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLastTraceBcRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetLastTraceBcRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetLastTraceBcRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetLastTraceBcRequest')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetLastTraceBcRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetLastTraceBcRequest'):
        super(GetLastTraceBcRequest, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetLastTraceBcRequest')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLastTraceBcRequest', fromsubclass_=False, pretty_print=True):
        super(GetLastTraceBcRequest, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Parcels is not None:
            namespaceprefix_ = self.Parcels_nsprefix_ + ':' if (UseCapturedNS_ and self.Parcels_nsprefix_) else ''
            self.Parcels.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Parcels', pretty_print=pretty_print)
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
        super(GetLastTraceBcRequest, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Parcels':
            obj_ = ArrayOfString.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Parcels = obj_
            obj_.original_tagname_ = 'Parcels'
        super(GetLastTraceBcRequest, self)._buildChildren(child_, node, nodeName_, True)
# end class GetLastTraceBcRequest


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
    def has__content(self):
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
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfString')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfString', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfString'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfString', fromsubclass_=False, pretty_print=True):
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
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'string':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'string')
            value_ = self.gds_validate_string(value_, node, 'string')
            self.string.append(value_)
            self.string_nsprefix_ = child_.prefix
# end class ArrayOfString


class GetLastTraceBcResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetLastTraceBcResult=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GetLastTraceBcResult = GetLastTraceBcResult
        self.GetLastTraceBcResult_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetLastTraceBcResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetLastTraceBcResponse.subclass:
            return GetLastTraceBcResponse.subclass(*args_, **kwargs_)
        else:
            return GetLastTraceBcResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetLastTraceBcResult(self):
        return self.GetLastTraceBcResult
    def set_GetLastTraceBcResult(self, GetLastTraceBcResult):
        self.GetLastTraceBcResult = GetLastTraceBcResult
    def has__content(self):
        if (
            self.GetLastTraceBcResult is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLastTraceBcResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetLastTraceBcResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetLastTraceBcResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetLastTraceBcResponse')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetLastTraceBcResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetLastTraceBcResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLastTraceBcResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GetLastTraceBcResult is not None:
            namespaceprefix_ = self.GetLastTraceBcResult_nsprefix_ + ':' if (UseCapturedNS_ and self.GetLastTraceBcResult_nsprefix_) else ''
            self.GetLastTraceBcResult.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetLastTraceBcResult', pretty_print=pretty_print)
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
        if nodeName_ == 'GetLastTraceBcResult':
            obj_ = ArrayOfGetLastTraceBcResponse.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetLastTraceBcResult = obj_
            obj_.original_tagname_ = 'GetLastTraceBcResult'
# end class GetLastTraceBcResponse


class ArrayOfGetLastTraceBcResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GetLastTraceBcResponse=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if GetLastTraceBcResponse is None:
            self.GetLastTraceBcResponse = []
        else:
            self.GetLastTraceBcResponse = GetLastTraceBcResponse
        self.GetLastTraceBcResponse_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ArrayOfGetLastTraceBcResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ArrayOfGetLastTraceBcResponse.subclass:
            return ArrayOfGetLastTraceBcResponse.subclass(*args_, **kwargs_)
        else:
            return ArrayOfGetLastTraceBcResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GetLastTraceBcResponse(self):
        return self.GetLastTraceBcResponse
    def set_GetLastTraceBcResponse(self, GetLastTraceBcResponse):
        self.GetLastTraceBcResponse = GetLastTraceBcResponse
    def add_GetLastTraceBcResponse(self, value):
        self.GetLastTraceBcResponse.append(value)
    def insert_GetLastTraceBcResponse_at(self, index, value):
        self.GetLastTraceBcResponse.insert(index, value)
    def replace_GetLastTraceBcResponse_at(self, index, value):
        self.GetLastTraceBcResponse[index] = value
    def has__content(self):
        if (
            self.GetLastTraceBcResponse
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfGetLastTraceBcResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ArrayOfGetLastTraceBcResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ArrayOfGetLastTraceBcResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ArrayOfGetLastTraceBcResponse')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ArrayOfGetLastTraceBcResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ArrayOfGetLastTraceBcResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ArrayOfGetLastTraceBcResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for GetLastTraceBcResponse_ in self.GetLastTraceBcResponse:
            namespaceprefix_ = self.GetLastTraceBcResponse_nsprefix_ + ':' if (UseCapturedNS_ and self.GetLastTraceBcResponse_nsprefix_) else ''
            GetLastTraceBcResponse_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='GetLastTraceBcResponse', pretty_print=pretty_print)
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
        if nodeName_ == 'GetLastTraceBcResponse':
            obj_ = GetLastTraceBcResponse.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GetLastTraceBcResponse.append(obj_)
            obj_.original_tagname_ = 'GetLastTraceBcResponse'
# end class ArrayOfGetLastTraceBcResponse


class GetLastTraceRequest(GetLastTraceBaseRequest):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = GetLastTraceBaseRequest
    def __init__(self, Customer=None, Language=None, Parcels=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("GetLastTraceRequest"), self).__init__(Customer, Language,  **kwargs_)
        self.Parcels = Parcels
        self.Parcels_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetLastTraceRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetLastTraceRequest.subclass:
            return GetLastTraceRequest.subclass(*args_, **kwargs_)
        else:
            return GetLastTraceRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Parcels(self):
        return self.Parcels
    def set_Parcels(self, Parcels):
        self.Parcels = Parcels
    def has__content(self):
        if (
            self.Parcels is not None or
            super(GetLastTraceRequest, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLastTraceRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetLastTraceRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetLastTraceRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetLastTraceRequest')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetLastTraceRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetLastTraceRequest'):
        super(GetLastTraceRequest, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetLastTraceRequest')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLastTraceRequest', fromsubclass_=False, pretty_print=True):
        super(GetLastTraceRequest, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Parcels is not None:
            namespaceprefix_ = self.Parcels_nsprefix_ + ':' if (UseCapturedNS_ and self.Parcels_nsprefix_) else ''
            self.Parcels.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Parcels', pretty_print=pretty_print)
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
        super(GetLastTraceRequest, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Parcels':
            obj_ = ArrayOfParcel.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Parcels = obj_
            obj_.original_tagname_ = 'Parcels'
        super(GetLastTraceRequest, self)._buildChildren(child_, node, nodeName_, True)
# end class GetLastTraceRequest


class ReferenceDetailRequest(ReferenceBaseRequest):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = ReferenceBaseRequest
    def __init__(self, Customer=None, Language=None, Reference=None, ShippingDate=None, Searchmode=None, GetImages=None, GetPhotos=None, GetParsedInfo=None, GetServices=None, GetLastTrace=None, Options=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("ReferenceDetailRequest"), self).__init__(Customer, Language, Reference, ShippingDate,  **kwargs_)
        self.Searchmode = Searchmode
        self.validate_ReferenceSearchMode(self.Searchmode)
        self.Searchmode_nsprefix_ = "tns"
        self.GetImages = GetImages
        self.GetImages_nsprefix_ = None
        self.GetPhotos = GetPhotos
        self.GetPhotos_nsprefix_ = None
        self.GetParsedInfo = GetParsedInfo
        self.GetParsedInfo_nsprefix_ = None
        self.GetServices = GetServices
        self.GetServices_nsprefix_ = None
        self.GetLastTrace = GetLastTrace
        self.GetLastTrace_nsprefix_ = None
        self.Options = Options
        self.Options_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ReferenceDetailRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ReferenceDetailRequest.subclass:
            return ReferenceDetailRequest.subclass(*args_, **kwargs_)
        else:
            return ReferenceDetailRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Searchmode(self):
        return self.Searchmode
    def set_Searchmode(self, Searchmode):
        self.Searchmode = Searchmode
    def get_GetImages(self):
        return self.GetImages
    def set_GetImages(self, GetImages):
        self.GetImages = GetImages
    def get_GetPhotos(self):
        return self.GetPhotos
    def set_GetPhotos(self, GetPhotos):
        self.GetPhotos = GetPhotos
    def get_GetParsedInfo(self):
        return self.GetParsedInfo
    def set_GetParsedInfo(self, GetParsedInfo):
        self.GetParsedInfo = GetParsedInfo
    def get_GetServices(self):
        return self.GetServices
    def set_GetServices(self, GetServices):
        self.GetServices = GetServices
    def get_GetLastTrace(self):
        return self.GetLastTrace
    def set_GetLastTrace(self, GetLastTrace):
        self.GetLastTrace = GetLastTrace
    def get_Options(self):
        return self.Options
    def set_Options(self, Options):
        self.Options = Options
    def validate_ReferenceSearchMode(self, value):
        result = True
        # Validate type ReferenceSearchMode, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['Equals', 'Like']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ReferenceSearchMode' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.Searchmode is not None or
            self.GetImages is not None or
            self.GetPhotos is not None or
            self.GetParsedInfo is not None or
            self.GetServices is not None or
            self.GetLastTrace is not None or
            self.Options is not None or
            super(ReferenceDetailRequest, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReferenceDetailRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ReferenceDetailRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ReferenceDetailRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ReferenceDetailRequest')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ReferenceDetailRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ReferenceDetailRequest'):
        super(ReferenceDetailRequest, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ReferenceDetailRequest')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReferenceDetailRequest', fromsubclass_=False, pretty_print=True):
        super(ReferenceDetailRequest, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Searchmode is not None:
            namespaceprefix_ = self.Searchmode_nsprefix_ + ':' if (UseCapturedNS_ and self.Searchmode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSearchmode>%s</%sSearchmode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Searchmode), input_name='Searchmode')), namespaceprefix_ , eol_))
        if self.GetImages is not None:
            namespaceprefix_ = self.GetImages_nsprefix_ + ':' if (UseCapturedNS_ and self.GetImages_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetImages>%s</%sGetImages>%s' % (namespaceprefix_ , self.gds_format_boolean(self.GetImages, input_name='GetImages'), namespaceprefix_ , eol_))
        if self.GetPhotos is not None:
            namespaceprefix_ = self.GetPhotos_nsprefix_ + ':' if (UseCapturedNS_ and self.GetPhotos_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetPhotos>%s</%sGetPhotos>%s' % (namespaceprefix_ , self.gds_format_boolean(self.GetPhotos, input_name='GetPhotos'), namespaceprefix_ , eol_))
        if self.GetPhotos is None:
            namespaceprefix_ = self.GetPhotos_nsprefix_ + ':' if (UseCapturedNS_ and self.GetPhotos_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetPhotos xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>%s' % (namespaceprefix_,eol_))
        if self.GetParsedInfo is not None:
            namespaceprefix_ = self.GetParsedInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.GetParsedInfo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetParsedInfo>%s</%sGetParsedInfo>%s' % (namespaceprefix_ , self.gds_format_boolean(self.GetParsedInfo, input_name='GetParsedInfo'), namespaceprefix_ , eol_))
        if self.GetParsedInfo is None:
            namespaceprefix_ = self.GetParsedInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.GetParsedInfo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetParsedInfo xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>%s' % (namespaceprefix_,eol_))
        if self.GetServices is not None:
            namespaceprefix_ = self.GetServices_nsprefix_ + ':' if (UseCapturedNS_ and self.GetServices_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetServices>%s</%sGetServices>%s' % (namespaceprefix_ , self.gds_format_boolean(self.GetServices, input_name='GetServices'), namespaceprefix_ , eol_))
        if self.GetServices is None:
            namespaceprefix_ = self.GetServices_nsprefix_ + ':' if (UseCapturedNS_ and self.GetServices_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetServices xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>%s' % (namespaceprefix_,eol_))
        if self.GetLastTrace is not None:
            namespaceprefix_ = self.GetLastTrace_nsprefix_ + ':' if (UseCapturedNS_ and self.GetLastTrace_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetLastTrace>%s</%sGetLastTrace>%s' % (namespaceprefix_ , self.gds_format_boolean(self.GetLastTrace, input_name='GetLastTrace'), namespaceprefix_ , eol_))
        if self.GetLastTrace is None:
            namespaceprefix_ = self.GetLastTrace_nsprefix_ + ':' if (UseCapturedNS_ and self.GetLastTrace_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetLastTrace xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>%s' % (namespaceprefix_,eol_))
        if self.Options is not None:
            namespaceprefix_ = self.Options_nsprefix_ + ':' if (UseCapturedNS_ and self.Options_nsprefix_) else ''
            self.Options.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Options', pretty_print=pretty_print)
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
        super(ReferenceDetailRequest, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Searchmode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Searchmode')
            value_ = self.gds_validate_string(value_, node, 'Searchmode')
            self.Searchmode = value_
            self.Searchmode_nsprefix_ = child_.prefix
            # validate type ReferenceSearchMode
            self.validate_ReferenceSearchMode(self.Searchmode)
        elif nodeName_ == 'GetImages':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'GetImages')
            ival_ = self.gds_validate_boolean(ival_, node, 'GetImages')
            self.GetImages = ival_
            self.GetImages_nsprefix_ = child_.prefix
        elif nodeName_ == 'GetPhotos':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'GetPhotos')
            ival_ = self.gds_validate_boolean(ival_, node, 'GetPhotos')
            self.GetPhotos = ival_
            self.GetPhotos_nsprefix_ = child_.prefix
        elif nodeName_ == 'GetParsedInfo':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'GetParsedInfo')
            ival_ = self.gds_validate_boolean(ival_, node, 'GetParsedInfo')
            self.GetParsedInfo = ival_
            self.GetParsedInfo_nsprefix_ = child_.prefix
        elif nodeName_ == 'GetServices':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'GetServices')
            ival_ = self.gds_validate_boolean(ival_, node, 'GetServices')
            self.GetServices = ival_
            self.GetServices_nsprefix_ = child_.prefix
        elif nodeName_ == 'GetLastTrace':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'GetLastTrace')
            ival_ = self.gds_validate_boolean(ival_, node, 'GetLastTrace')
            self.GetLastTrace = ival_
            self.GetLastTrace_nsprefix_ = child_.prefix
        elif nodeName_ == 'Options':
            obj_ = Options.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Options = obj_
            obj_.original_tagname_ = 'Options'
        super(ReferenceDetailRequest, self)._buildChildren(child_, node, nodeName_, True)
# end class ReferenceDetailRequest


class ShipmentTrace(clsShipmentTraceBase):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = clsShipmentTraceBase
    def __init__(self, ShipmentNumber=None, DestinationCountry=None, DestinationZipcode=None, ShippingDate=None, DeliveryDate=None, Weight=None, Receiver=None, Reference=None, Reference2=None, Reference3=None, Reference4=None, DeliveryScheduled=None, Traces=None, Reference_International=None, IsB2C=None, IsRetour=None, PointRelaisName=None, PointRelaisLink=None, ShipmentNumber_Retour=None, RetourType=None, Services=None, CustomerCenternumber=None, CustomerNumber=None, BarcodeSource=None, BarcodeId=None, ReceiverDepotNumber=None, ReceiverTourNumber=None, DeliveryRecordNumber=None, DeliveryRecordPosition=None, images=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("ShipmentTrace"), self).__init__(ShipmentNumber, DestinationCountry, DestinationZipcode, ShippingDate, DeliveryDate, Weight, Receiver, Reference, Reference2, Reference3, Reference4, DeliveryScheduled, Traces, Reference_International, IsB2C, IsRetour, PointRelaisName, PointRelaisLink, ShipmentNumber_Retour, RetourType, Services, CustomerCenternumber, CustomerNumber, BarcodeSource, BarcodeId, ReceiverDepotNumber, ReceiverTourNumber, DeliveryRecordNumber, DeliveryRecordPosition,  **kwargs_)
        self.images = images
        self.images_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentTrace)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentTrace.subclass:
            return ShipmentTrace.subclass(*args_, **kwargs_)
        else:
            return ShipmentTrace(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_images(self):
        return self.images
    def set_images(self, images):
        self.images = images
    def has__content(self):
        if (
            self.images is not None or
            super(ShipmentTrace, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentTrace', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentTrace')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentTrace':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentTrace')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentTrace', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentTrace'):
        super(ShipmentTrace, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentTrace')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentTrace', fromsubclass_=False, pretty_print=True):
        super(ShipmentTrace, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.images is not None:
            namespaceprefix_ = self.images_nsprefix_ + ':' if (UseCapturedNS_ and self.images_nsprefix_) else ''
            self.images.export(outfile, level, namespaceprefix_, namespacedef_='', name_='images', pretty_print=pretty_print)
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
        super(ShipmentTrace, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'images':
            obj_ = ArrayOfImage.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.images = obj_
            obj_.original_tagname_ = 'images'
        super(ShipmentTrace, self)._buildChildren(child_, node, nodeName_, True)
# end class ShipmentTrace


class RequestShipmentBase(RequestBase):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = RequestBase
    def __init__(self, Customer=None, Language=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("RequestShipmentBase"), self).__init__(Customer, Language, extensiontype_,  **kwargs_)
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, RequestShipmentBase)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if RequestShipmentBase.subclass:
            return RequestShipmentBase.subclass(*args_, **kwargs_)
        else:
            return RequestShipmentBase(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def has__content(self):
        if (
            super(RequestShipmentBase, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RequestShipmentBase', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('RequestShipmentBase')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'RequestShipmentBase':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RequestShipmentBase')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='RequestShipmentBase', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='RequestShipmentBase'):
        super(RequestShipmentBase, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='RequestShipmentBase')
        if self.extensiontype_ is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self.extensiontype_:
                imported_ns_type_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.extensiontype_, '')
                outfile.write(' xsi:type="%s%s"' % (imported_ns_type_prefix_, self.extensiontype_))
            else:
                outfile.write(' xsi:type="%s"' % self.extensiontype_)
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='RequestShipmentBase', fromsubclass_=False, pretty_print=True):
        super(RequestShipmentBase, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
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
        super(RequestShipmentBase, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        super(RequestShipmentBase, self)._buildChildren(child_, node, nodeName_, True)
        pass
# end class RequestShipmentBase


class ShipmentBaseRequest(RequestShipmentBase):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = RequestShipmentBase
    def __init__(self, Customer=None, Language=None, ShipmentNumber=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("ShipmentBaseRequest"), self).__init__(Customer, Language, extensiontype_,  **kwargs_)
        self.ShipmentNumber = ShipmentNumber
        self.ShipmentNumber_nsprefix_ = None
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentBaseRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentBaseRequest.subclass:
            return ShipmentBaseRequest.subclass(*args_, **kwargs_)
        else:
            return ShipmentBaseRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ShipmentNumber(self):
        return self.ShipmentNumber
    def set_ShipmentNumber(self, ShipmentNumber):
        self.ShipmentNumber = ShipmentNumber
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def has__content(self):
        if (
            self.ShipmentNumber is not None or
            super(ShipmentBaseRequest, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentBaseRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentBaseRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentBaseRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentBaseRequest')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentBaseRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentBaseRequest'):
        super(ShipmentBaseRequest, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentBaseRequest')
        if self.extensiontype_ is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self.extensiontype_:
                imported_ns_type_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.extensiontype_, '')
                outfile.write(' xsi:type="%s%s"' % (imported_ns_type_prefix_, self.extensiontype_))
            else:
                outfile.write(' xsi:type="%s"' % self.extensiontype_)
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentBaseRequest', fromsubclass_=False, pretty_print=True):
        super(ShipmentBaseRequest, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ShipmentNumber is not None:
            namespaceprefix_ = self.ShipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipmentNumber>%s</%sShipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShipmentNumber), input_name='ShipmentNumber')), namespaceprefix_ , eol_))
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
        super(ShipmentBaseRequest, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ShipmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShipmentNumber')
            value_ = self.gds_validate_string(value_, node, 'ShipmentNumber')
            self.ShipmentNumber = value_
            self.ShipmentNumber_nsprefix_ = child_.prefix
        super(ShipmentBaseRequest, self)._buildChildren(child_, node, nodeName_, True)
# end class ShipmentBaseRequest


class ShipmentDetailRequest(ShipmentBaseRequest):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = ShipmentBaseRequest
    def __init__(self, Customer=None, Language=None, ShipmentNumber=None, ExpandContainerMode=None, GetImages=None, GetPhotos=None, GetParsedInfo=None, GetServices=None, Options=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("ShipmentDetailRequest"), self).__init__(Customer, Language, ShipmentNumber,  **kwargs_)
        self.ExpandContainerMode = ExpandContainerMode
        self.validate_ExpandContainerModeType(self.ExpandContainerMode)
        self.ExpandContainerMode_nsprefix_ = "tns"
        self.GetImages = GetImages
        self.GetImages_nsprefix_ = None
        self.GetPhotos = GetPhotos
        self.GetPhotos_nsprefix_ = None
        self.GetParsedInfo = GetParsedInfo
        self.GetParsedInfo_nsprefix_ = None
        self.GetServices = GetServices
        self.GetServices_nsprefix_ = None
        self.Options = Options
        self.Options_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentDetailRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentDetailRequest.subclass:
            return ShipmentDetailRequest.subclass(*args_, **kwargs_)
        else:
            return ShipmentDetailRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ExpandContainerMode(self):
        return self.ExpandContainerMode
    def set_ExpandContainerMode(self, ExpandContainerMode):
        self.ExpandContainerMode = ExpandContainerMode
    def get_GetImages(self):
        return self.GetImages
    def set_GetImages(self, GetImages):
        self.GetImages = GetImages
    def get_GetPhotos(self):
        return self.GetPhotos
    def set_GetPhotos(self, GetPhotos):
        self.GetPhotos = GetPhotos
    def get_GetParsedInfo(self):
        return self.GetParsedInfo
    def set_GetParsedInfo(self, GetParsedInfo):
        self.GetParsedInfo = GetParsedInfo
    def get_GetServices(self):
        return self.GetServices
    def set_GetServices(self, GetServices):
        self.GetServices = GetServices
    def get_Options(self):
        return self.Options
    def set_Options(self, Options):
        self.Options = Options
    def validate_ExpandContainerModeType(self, value):
        result = True
        # Validate type ExpandContainerModeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['MasterOnly', 'MasterAndSlave']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ExpandContainerModeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def has__content(self):
        if (
            self.ExpandContainerMode is not None or
            self.GetImages is not None or
            self.GetPhotos is not None or
            self.GetParsedInfo is not None or
            self.GetServices is not None or
            self.Options is not None or
            super(ShipmentDetailRequest, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentDetailRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentDetailRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentDetailRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentDetailRequest')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentDetailRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentDetailRequest'):
        super(ShipmentDetailRequest, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentDetailRequest')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentDetailRequest', fromsubclass_=False, pretty_print=True):
        super(ShipmentDetailRequest, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ExpandContainerMode is not None:
            namespaceprefix_ = self.ExpandContainerMode_nsprefix_ + ':' if (UseCapturedNS_ and self.ExpandContainerMode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExpandContainerMode>%s</%sExpandContainerMode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ExpandContainerMode), input_name='ExpandContainerMode')), namespaceprefix_ , eol_))
        if self.ExpandContainerMode is None:
            namespaceprefix_ = self.ExpandContainerMode_nsprefix_ + ':' if (UseCapturedNS_ and self.ExpandContainerMode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExpandContainerMode xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>%s' % (namespaceprefix_,eol_))
        if self.GetImages is not None:
            namespaceprefix_ = self.GetImages_nsprefix_ + ':' if (UseCapturedNS_ and self.GetImages_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetImages>%s</%sGetImages>%s' % (namespaceprefix_ , self.gds_format_boolean(self.GetImages, input_name='GetImages'), namespaceprefix_ , eol_))
        if self.GetPhotos is not None:
            namespaceprefix_ = self.GetPhotos_nsprefix_ + ':' if (UseCapturedNS_ and self.GetPhotos_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetPhotos>%s</%sGetPhotos>%s' % (namespaceprefix_ , self.gds_format_boolean(self.GetPhotos, input_name='GetPhotos'), namespaceprefix_ , eol_))
        if self.GetPhotos is None:
            namespaceprefix_ = self.GetPhotos_nsprefix_ + ':' if (UseCapturedNS_ and self.GetPhotos_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetPhotos xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>%s' % (namespaceprefix_,eol_))
        if self.GetParsedInfo is not None:
            namespaceprefix_ = self.GetParsedInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.GetParsedInfo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetParsedInfo>%s</%sGetParsedInfo>%s' % (namespaceprefix_ , self.gds_format_boolean(self.GetParsedInfo, input_name='GetParsedInfo'), namespaceprefix_ , eol_))
        if self.GetParsedInfo is None:
            namespaceprefix_ = self.GetParsedInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.GetParsedInfo_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetParsedInfo xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>%s' % (namespaceprefix_,eol_))
        if self.GetServices is not None:
            namespaceprefix_ = self.GetServices_nsprefix_ + ':' if (UseCapturedNS_ and self.GetServices_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetServices>%s</%sGetServices>%s' % (namespaceprefix_ , self.gds_format_boolean(self.GetServices, input_name='GetServices'), namespaceprefix_ , eol_))
        if self.GetServices is None:
            namespaceprefix_ = self.GetServices_nsprefix_ + ':' if (UseCapturedNS_ and self.GetServices_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGetServices xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>%s' % (namespaceprefix_,eol_))
        if self.Options is not None:
            namespaceprefix_ = self.Options_nsprefix_ + ':' if (UseCapturedNS_ and self.Options_nsprefix_) else ''
            self.Options.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Options', pretty_print=pretty_print)
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
        super(ShipmentDetailRequest, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ExpandContainerMode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ExpandContainerMode')
            value_ = self.gds_validate_string(value_, node, 'ExpandContainerMode')
            self.ExpandContainerMode = value_
            self.ExpandContainerMode_nsprefix_ = child_.prefix
            # validate type ExpandContainerModeType
            self.validate_ExpandContainerModeType(self.ExpandContainerMode)
        elif nodeName_ == 'GetImages':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'GetImages')
            ival_ = self.gds_validate_boolean(ival_, node, 'GetImages')
            self.GetImages = ival_
            self.GetImages_nsprefix_ = child_.prefix
        elif nodeName_ == 'GetPhotos':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'GetPhotos')
            ival_ = self.gds_validate_boolean(ival_, node, 'GetPhotos')
            self.GetPhotos = ival_
            self.GetPhotos_nsprefix_ = child_.prefix
        elif nodeName_ == 'GetParsedInfo':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'GetParsedInfo')
            ival_ = self.gds_validate_boolean(ival_, node, 'GetParsedInfo')
            self.GetParsedInfo = ival_
            self.GetParsedInfo_nsprefix_ = child_.prefix
        elif nodeName_ == 'GetServices':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'GetServices')
            ival_ = self.gds_validate_boolean(ival_, node, 'GetServices')
            self.GetServices = ival_
            self.GetServices_nsprefix_ = child_.prefix
        elif nodeName_ == 'Options':
            obj_ = Options.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Options = obj_
            obj_.original_tagname_ = 'Options'
        super(ShipmentDetailRequest, self)._buildChildren(child_, node, nodeName_, True)
# end class ShipmentDetailRequest


class Customer(CustomerSmall):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = CustomerSmall
    def __init__(self, centernumber=None, number=None, countrycode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("Customer"), self).__init__(centernumber, number,  **kwargs_)
        self.countrycode = countrycode
        self.countrycode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Customer)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Customer.subclass:
            return Customer.subclass(*args_, **kwargs_)
        else:
            return Customer(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_countrycode(self):
        return self.countrycode
    def set_countrycode(self, countrycode):
        self.countrycode = countrycode
    def has__content(self):
        if (
            self.countrycode is not None or
            super(Customer, self).has__content()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Customer', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Customer')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Customer':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Customer')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Customer', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Customer'):
        super(Customer, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Customer')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Customer', fromsubclass_=False, pretty_print=True):
        super(Customer, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.countrycode is not None:
            namespaceprefix_ = self.countrycode_nsprefix_ + ':' if (UseCapturedNS_ and self.countrycode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scountrycode>%s</%scountrycode>%s' % (namespaceprefix_ , self.gds_format_integer(self.countrycode, input_name='countrycode'), namespaceprefix_ , eol_))
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
        super(Customer, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'countrycode' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'countrycode')
            ival_ = self.gds_validate_integer(ival_, node, 'countrycode')
            self.countrycode = ival_
            self.countrycode_nsprefix_ = child_.prefix
        super(Customer, self)._buildChildren(child_, node, nodeName_, True)
# end class Customer


#
# End data representation classes.
#


GDSClassesMapping = {
    'UserCredentials': UserCredentials,
    'VerifyUserCredentials': VerifyUserCredentials,
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
        rootTag = 'isAlive'
        rootClass = isAlive
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
        rootTag = 'isAlive'
        rootClass = isAlive
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
        rootTag = 'isAlive'
        rootClass = isAlive
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:tns="http://www.cargonet.software/"')
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
        rootTag = 'isAlive'
        rootClass = isAlive
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from webtraceservice import *\n\n')
        sys.stdout.write('import webtraceservice as model_\n\n')
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
NamespaceToDefMappings_ = {'http://www.cargonet.software/': [('ExpandContainerModeType',
                                    './schemas/Webtrace_Service.xsd',
                                    'ST'),
                                   ('ImageType',
                                    './schemas/Webtrace_Service.xsd',
                                    'ST'),
                                   ('ReferenceSearchMode',
                                    './schemas/Webtrace_Service.xsd',
                                    'ST'),
                                   ('UserCredentials',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('VerifyConfigurationRequest',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('Customer',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('CustomerSmall',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('VerifyConfigurationResponse',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('VerifyUserCredentials',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('RunActionRequest',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('RunActionResponse',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('ShipmentDetailRequest',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('ShipmentBaseRequest',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('RequestShipmentBase',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('RequestBase',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('Options',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('ShipmentTrace',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('clsShipmentTraceBase',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('SdgiData',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('ArrayOfClsTrace',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('clsTrace',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('RelaisInfo',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('ArrayOfTracePhoto',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('TracePhoto',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('ArrayOfClsTraceDetails',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('clsTraceDetails',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('ArrayOfServiceInfo',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('ServiceInfo',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('ArrayOfImage',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('Image',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('ArrayOfShipmentTrace',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('ReferenceDetailRequest',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('ReferenceBaseRequest',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('GetLastTraceRequest',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('GetLastTraceBaseRequest',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('ArrayOfParcel',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('Parcel',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('ArrayOfGetLastTraceResponse',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('GetLastTraceResponse',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('GetLastTraceBaseResponse',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('GetLastTraceBcRequest',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('ArrayOfString',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('ArrayOfGetLastTraceBcResponse',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT'),
                                   ('GetLastTraceBcResponse',
                                    './schemas/Webtrace_Service.xsd',
                                    'CT')]}

__all__ = [
    "ArrayOfClsTrace",
    "ArrayOfClsTraceDetails",
    "ArrayOfGetLastTraceBcResponse",
    "ArrayOfGetLastTraceResponse",
    "ArrayOfImage",
    "ArrayOfParcel",
    "ArrayOfServiceInfo",
    "ArrayOfShipmentTrace",
    "ArrayOfString",
    "ArrayOfTracePhoto",
    "Customer",
    "CustomerSmall",
    "GetLastTrace",
    "GetLastTraceBaseRequest",
    "GetLastTraceBaseResponse",
    "GetLastTraceBc",
    "GetLastTraceBcRequest",
    "GetLastTraceBcResponse",
    "GetLastTraceRequest",
    "GetLastTraceResponse",
    "GetShipmentTrace",
    "GetShipmentTraceByReference",
    "GetShipmentTraceByReferenceResponse",
    "GetShipmentTraceResponse",
    "GetShipmentTraceSingle",
    "GetShipmentTraceSingleResponse",
    "Image",
    "Options",
    "Parcel",
    "ReferenceBaseRequest",
    "ReferenceDetailRequest",
    "RelaisInfo",
    "RequestBase",
    "RequestShipmentBase",
    "RunActionRequest",
    "RunActionResponse",
    "SdgiData",
    "ServiceInfo",
    "ShipmentBaseRequest",
    "ShipmentDetailRequest",
    "ShipmentTrace",
    "TracePhoto",
    "UserCredentials",
    "VerifyConfiguration",
    "VerifyConfigurationRequest",
    "VerifyConfigurationResponse",
    "VerifyUserCredentials",
    "clsShipmentTraceBase",
    "clsTrace",
    "clsTraceDetails",
    "getInfo",
    "getInfoResponse",
    "isAlive",
    "isAliveResponse",
    "runAction",
    "runActionResponse",
    "setAlive",
    "setAliveResponse"
]
