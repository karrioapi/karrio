#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Tue Apr  4 08:40:21 2023 by generateDS.py version 2.41.3.
# Python 3.10.6 (main, Mar 10 2023, 10:55:28) [GCC 11.3.0]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './dhl_express_lib/dct_responsedatatypes_global.py')
#
# Command line arguments:
#   ./schemas/DCTResponsedatatypes_global.xsd
#
# Command line:
#   /home/kserver/Workspace/karrio/.venv/karrio/bin/generateDS --no-namespace-defs -o "./dhl_express_lib/dct_responsedatatypes_global.py" ./schemas/DCTResponsedatatypes_global.xsd
#
# Current working directory (os.getcwd()):
#   dhl_express
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


class ChargeCodeTypeType(str, Enum):
    FEE='FEE'
    SCH='SCH'
    XCH='XCH'
    NRI='NRI'


class QuotedWeightUOM(str, Enum):
    """QuotedWeightUOM -- WeightUOM
    
    """
    KG='KG'
    LBS='Lbs'


class DCTResponseDataTypes(GeneratedsSuper):
    """DCTResponseDataTypes -- Comment describing your root element
    
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
                CurrentSubclassModule_, DCTResponseDataTypes)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DCTResponseDataTypes.subclass:
            return DCTResponseDataTypes.subclass(*args_, **kwargs_)
        else:
            return DCTResponseDataTypes(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DCTResponseDataTypes', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DCTResponseDataTypes')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DCTResponseDataTypes':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DCTResponseDataTypes')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DCTResponseDataTypes', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DCTResponseDataTypes'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DCTResponseDataTypes', fromsubclass_=False, pretty_print=True):
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
# end class DCTResponseDataTypes


class OrgnSvcAreaType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, FacilityCode=None, ServiceAreaCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.FacilityCode = FacilityCode
        self.validate_FacilityCodeType(self.FacilityCode)
        self.FacilityCode_nsprefix_ = None
        self.ServiceAreaCode = ServiceAreaCode
        self.validate_ServiceAreaCodeType(self.ServiceAreaCode)
        self.ServiceAreaCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, OrgnSvcAreaType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OrgnSvcAreaType.subclass:
            return OrgnSvcAreaType.subclass(*args_, **kwargs_)
        else:
            return OrgnSvcAreaType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_FacilityCode(self):
        return self.FacilityCode
    def set_FacilityCode(self, FacilityCode):
        self.FacilityCode = FacilityCode
    def get_ServiceAreaCode(self):
        return self.ServiceAreaCode
    def set_ServiceAreaCode(self, ServiceAreaCode):
        self.ServiceAreaCode = ServiceAreaCode
    def validate_FacilityCodeType(self, value):
        result = True
        # Validate type FacilityCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on FacilityCodeType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ServiceAreaCodeType(self, value):
        result = True
        # Validate type ServiceAreaCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on ServiceAreaCodeType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.FacilityCode is not None or
            self.ServiceAreaCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OrgnSvcAreaType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OrgnSvcAreaType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'OrgnSvcAreaType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OrgnSvcAreaType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='OrgnSvcAreaType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='OrgnSvcAreaType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='OrgnSvcAreaType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.FacilityCode is not None:
            namespaceprefix_ = self.FacilityCode_nsprefix_ + ':' if (UseCapturedNS_ and self.FacilityCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFacilityCode>%s</%sFacilityCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FacilityCode), input_name='FacilityCode')), namespaceprefix_ , eol_))
        if self.ServiceAreaCode is not None:
            namespaceprefix_ = self.ServiceAreaCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceAreaCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceAreaCode>%s</%sServiceAreaCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServiceAreaCode), input_name='ServiceAreaCode')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'FacilityCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FacilityCode')
            value_ = self.gds_validate_string(value_, node, 'FacilityCode')
            self.FacilityCode = value_
            self.FacilityCode_nsprefix_ = child_.prefix
            # validate type FacilityCodeType
            self.validate_FacilityCodeType(self.FacilityCode)
        elif nodeName_ == 'ServiceAreaCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServiceAreaCode')
            value_ = self.gds_validate_string(value_, node, 'ServiceAreaCode')
            self.ServiceAreaCode = value_
            self.ServiceAreaCode_nsprefix_ = child_.prefix
            # validate type ServiceAreaCodeType
            self.validate_ServiceAreaCodeType(self.ServiceAreaCode)
# end class OrgnSvcAreaType


class DestSvcAreaType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, FacilityCode=None, ServiceAreaCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.FacilityCode = FacilityCode
        self.validate_FacilityCodeType1(self.FacilityCode)
        self.FacilityCode_nsprefix_ = None
        self.ServiceAreaCode = ServiceAreaCode
        self.validate_ServiceAreaCodeType2(self.ServiceAreaCode)
        self.ServiceAreaCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DestSvcAreaType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DestSvcAreaType.subclass:
            return DestSvcAreaType.subclass(*args_, **kwargs_)
        else:
            return DestSvcAreaType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_FacilityCode(self):
        return self.FacilityCode
    def set_FacilityCode(self, FacilityCode):
        self.FacilityCode = FacilityCode
    def get_ServiceAreaCode(self):
        return self.ServiceAreaCode
    def set_ServiceAreaCode(self, ServiceAreaCode):
        self.ServiceAreaCode = ServiceAreaCode
    def validate_FacilityCodeType1(self, value):
        result = True
        # Validate type FacilityCodeType1, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on FacilityCodeType1' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ServiceAreaCodeType2(self, value):
        result = True
        # Validate type ServiceAreaCodeType2, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on ServiceAreaCodeType2' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.FacilityCode is not None or
            self.ServiceAreaCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DestSvcAreaType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DestSvcAreaType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DestSvcAreaType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DestSvcAreaType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DestSvcAreaType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DestSvcAreaType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DestSvcAreaType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.FacilityCode is not None:
            namespaceprefix_ = self.FacilityCode_nsprefix_ + ':' if (UseCapturedNS_ and self.FacilityCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFacilityCode>%s</%sFacilityCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FacilityCode), input_name='FacilityCode')), namespaceprefix_ , eol_))
        if self.ServiceAreaCode is not None:
            namespaceprefix_ = self.ServiceAreaCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceAreaCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceAreaCode>%s</%sServiceAreaCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServiceAreaCode), input_name='ServiceAreaCode')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'FacilityCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FacilityCode')
            value_ = self.gds_validate_string(value_, node, 'FacilityCode')
            self.FacilityCode = value_
            self.FacilityCode_nsprefix_ = child_.prefix
            # validate type FacilityCodeType1
            self.validate_FacilityCodeType1(self.FacilityCode)
        elif nodeName_ == 'ServiceAreaCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServiceAreaCode')
            value_ = self.gds_validate_string(value_, node, 'ServiceAreaCode')
            self.ServiceAreaCode = value_
            self.ServiceAreaCode_nsprefix_ = child_.prefix
            # validate type ServiceAreaCodeType2
            self.validate_ServiceAreaCodeType2(self.ServiceAreaCode)
# end class DestSvcAreaType


class BkgDetailsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, QtdShp=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if QtdShp is None:
            self.QtdShp = []
        else:
            self.QtdShp = QtdShp
        self.QtdShp_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, BkgDetailsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BkgDetailsType.subclass:
            return BkgDetailsType.subclass(*args_, **kwargs_)
        else:
            return BkgDetailsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_QtdShp(self):
        return self.QtdShp
    def set_QtdShp(self, QtdShp):
        self.QtdShp = QtdShp
    def add_QtdShp(self, value):
        self.QtdShp.append(value)
    def insert_QtdShp_at(self, index, value):
        self.QtdShp.insert(index, value)
    def replace_QtdShp_at(self, index, value):
        self.QtdShp[index] = value
    def _hasContent(self):
        if (
            self.QtdShp
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BkgDetailsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('BkgDetailsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'BkgDetailsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BkgDetailsType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='BkgDetailsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='BkgDetailsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BkgDetailsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for QtdShp_ in self.QtdShp:
            namespaceprefix_ = self.QtdShp_nsprefix_ + ':' if (UseCapturedNS_ and self.QtdShp_nsprefix_) else ''
            QtdShp_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='QtdShp', pretty_print=pretty_print)
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
        if nodeName_ == 'QtdShp':
            obj_ = QtdShpType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.QtdShp.append(obj_)
            obj_.original_tagname_ = 'QtdShp'
# end class BkgDetailsType


class SrvCombType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GlobalServiceName=None, GlobalServiceCode=None, LocalServiceCode=None, LocalServiceTypeName=None, ChargeCodeType=None, SOfferedCustAgreement=None, SrvComb=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GlobalServiceName = GlobalServiceName
        self.validate_GlobalServiceNameType(self.GlobalServiceName)
        self.GlobalServiceName_nsprefix_ = None
        self.GlobalServiceCode = GlobalServiceCode
        self.validate_GlobalServiceCodeType(self.GlobalServiceCode)
        self.GlobalServiceCode_nsprefix_ = None
        self.LocalServiceCode = LocalServiceCode
        self.validate_LocalServiceCodeType(self.LocalServiceCode)
        self.LocalServiceCode_nsprefix_ = None
        self.LocalServiceTypeName = LocalServiceTypeName
        self.validate_LocalServiceTypeNameType(self.LocalServiceTypeName)
        self.LocalServiceTypeName_nsprefix_ = None
        self.ChargeCodeType = ChargeCodeType
        self.validate_ChargeCodeTypeType(self.ChargeCodeType)
        self.ChargeCodeType_nsprefix_ = None
        self.SOfferedCustAgreement = SOfferedCustAgreement
        self.validate_SOfferedCustAgreementType(self.SOfferedCustAgreement)
        self.SOfferedCustAgreement_nsprefix_ = None
        self.SrvComb = SrvComb
        self.SrvComb_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SrvCombType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SrvCombType.subclass:
            return SrvCombType.subclass(*args_, **kwargs_)
        else:
            return SrvCombType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GlobalServiceName(self):
        return self.GlobalServiceName
    def set_GlobalServiceName(self, GlobalServiceName):
        self.GlobalServiceName = GlobalServiceName
    def get_GlobalServiceCode(self):
        return self.GlobalServiceCode
    def set_GlobalServiceCode(self, GlobalServiceCode):
        self.GlobalServiceCode = GlobalServiceCode
    def get_LocalServiceCode(self):
        return self.LocalServiceCode
    def set_LocalServiceCode(self, LocalServiceCode):
        self.LocalServiceCode = LocalServiceCode
    def get_LocalServiceTypeName(self):
        return self.LocalServiceTypeName
    def set_LocalServiceTypeName(self, LocalServiceTypeName):
        self.LocalServiceTypeName = LocalServiceTypeName
    def get_ChargeCodeType(self):
        return self.ChargeCodeType
    def set_ChargeCodeType(self, ChargeCodeType):
        self.ChargeCodeType = ChargeCodeType
    def get_SOfferedCustAgreement(self):
        return self.SOfferedCustAgreement
    def set_SOfferedCustAgreement(self, SOfferedCustAgreement):
        self.SOfferedCustAgreement = SOfferedCustAgreement
    def get_SrvComb(self):
        return self.SrvComb
    def set_SrvComb(self, SrvComb):
        self.SrvComb = SrvComb
    def validate_GlobalServiceNameType(self, value):
        result = True
        # Validate type GlobalServiceNameType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 45:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on GlobalServiceNameType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_GlobalServiceCodeType(self, value):
        result = True
        # Validate type GlobalServiceCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on GlobalServiceCodeType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_LocalServiceCodeType(self, value):
        result = True
        # Validate type LocalServiceCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on LocalServiceCodeType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_LocalServiceTypeNameType(self, value):
        result = True
        # Validate type LocalServiceTypeNameType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 45:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on LocalServiceTypeNameType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ChargeCodeTypeType(self, value):
        result = True
        # Validate type ChargeCodeTypeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['FEE', 'SCH', 'XCH', 'NRI']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ChargeCodeTypeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on ChargeCodeTypeType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_SOfferedCustAgreementType(self, value):
        result = True
        # Validate type SOfferedCustAgreementType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on SOfferedCustAgreementType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.GlobalServiceName is not None or
            self.GlobalServiceCode is not None or
            self.LocalServiceCode is not None or
            self.LocalServiceTypeName is not None or
            self.ChargeCodeType is not None or
            self.SOfferedCustAgreement is not None or
            self.SrvComb is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SrvCombType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SrvCombType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SrvCombType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SrvCombType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SrvCombType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SrvCombType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SrvCombType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GlobalServiceName is not None:
            namespaceprefix_ = self.GlobalServiceName_nsprefix_ + ':' if (UseCapturedNS_ and self.GlobalServiceName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGlobalServiceName>%s</%sGlobalServiceName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GlobalServiceName), input_name='GlobalServiceName')), namespaceprefix_ , eol_))
        if self.GlobalServiceCode is not None:
            namespaceprefix_ = self.GlobalServiceCode_nsprefix_ + ':' if (UseCapturedNS_ and self.GlobalServiceCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGlobalServiceCode>%s</%sGlobalServiceCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GlobalServiceCode), input_name='GlobalServiceCode')), namespaceprefix_ , eol_))
        if self.LocalServiceCode is not None:
            namespaceprefix_ = self.LocalServiceCode_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalServiceCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalServiceCode>%s</%sLocalServiceCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalServiceCode), input_name='LocalServiceCode')), namespaceprefix_ , eol_))
        if self.LocalServiceTypeName is not None:
            namespaceprefix_ = self.LocalServiceTypeName_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalServiceTypeName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalServiceTypeName>%s</%sLocalServiceTypeName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalServiceTypeName), input_name='LocalServiceTypeName')), namespaceprefix_ , eol_))
        if self.ChargeCodeType is not None:
            namespaceprefix_ = self.ChargeCodeType_nsprefix_ + ':' if (UseCapturedNS_ and self.ChargeCodeType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChargeCodeType>%s</%sChargeCodeType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChargeCodeType), input_name='ChargeCodeType')), namespaceprefix_ , eol_))
        if self.SOfferedCustAgreement is not None:
            namespaceprefix_ = self.SOfferedCustAgreement_nsprefix_ + ':' if (UseCapturedNS_ and self.SOfferedCustAgreement_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSOfferedCustAgreement>%s</%sSOfferedCustAgreement>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SOfferedCustAgreement), input_name='SOfferedCustAgreement')), namespaceprefix_ , eol_))
        if self.SrvComb is not None:
            namespaceprefix_ = self.SrvComb_nsprefix_ + ':' if (UseCapturedNS_ and self.SrvComb_nsprefix_) else ''
            self.SrvComb.export(outfile, level, namespaceprefix_, namespacedef_='', name_='SrvComb', pretty_print=pretty_print)
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
        if nodeName_ == 'GlobalServiceName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GlobalServiceName')
            value_ = self.gds_validate_string(value_, node, 'GlobalServiceName')
            self.GlobalServiceName = value_
            self.GlobalServiceName_nsprefix_ = child_.prefix
            # validate type GlobalServiceNameType
            self.validate_GlobalServiceNameType(self.GlobalServiceName)
        elif nodeName_ == 'GlobalServiceCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GlobalServiceCode')
            value_ = self.gds_validate_string(value_, node, 'GlobalServiceCode')
            self.GlobalServiceCode = value_
            self.GlobalServiceCode_nsprefix_ = child_.prefix
            # validate type GlobalServiceCodeType
            self.validate_GlobalServiceCodeType(self.GlobalServiceCode)
        elif nodeName_ == 'LocalServiceCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalServiceCode')
            value_ = self.gds_validate_string(value_, node, 'LocalServiceCode')
            self.LocalServiceCode = value_
            self.LocalServiceCode_nsprefix_ = child_.prefix
            # validate type LocalServiceCodeType
            self.validate_LocalServiceCodeType(self.LocalServiceCode)
        elif nodeName_ == 'LocalServiceTypeName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalServiceTypeName')
            value_ = self.gds_validate_string(value_, node, 'LocalServiceTypeName')
            self.LocalServiceTypeName = value_
            self.LocalServiceTypeName_nsprefix_ = child_.prefix
            # validate type LocalServiceTypeNameType
            self.validate_LocalServiceTypeNameType(self.LocalServiceTypeName)
        elif nodeName_ == 'ChargeCodeType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChargeCodeType')
            value_ = self.gds_validate_string(value_, node, 'ChargeCodeType')
            self.ChargeCodeType = value_
            self.ChargeCodeType_nsprefix_ = child_.prefix
            # validate type ChargeCodeTypeType
            self.validate_ChargeCodeTypeType(self.ChargeCodeType)
        elif nodeName_ == 'SOfferedCustAgreement':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SOfferedCustAgreement')
            value_ = self.gds_validate_string(value_, node, 'SOfferedCustAgreement')
            self.SOfferedCustAgreement = value_
            self.SOfferedCustAgreement_nsprefix_ = child_.prefix
            # validate type SOfferedCustAgreementType
            self.validate_SOfferedCustAgreementType(self.SOfferedCustAgreement)
        elif nodeName_ == 'SrvComb':
            obj_ = SrvCombType3.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SrvComb = obj_
            obj_.original_tagname_ = 'SrvComb'
# end class SrvCombType


class ProdType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, VldSrvComb=None, TotalDiscount=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if VldSrvComb is None:
            self.VldSrvComb = []
        else:
            self.VldSrvComb = VldSrvComb
        self.VldSrvComb_nsprefix_ = None
        self.TotalDiscount = TotalDiscount
        self.validate_TotalDiscountType(self.TotalDiscount)
        self.TotalDiscount_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ProdType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ProdType.subclass:
            return ProdType.subclass(*args_, **kwargs_)
        else:
            return ProdType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_VldSrvComb(self):
        return self.VldSrvComb
    def set_VldSrvComb(self, VldSrvComb):
        self.VldSrvComb = VldSrvComb
    def add_VldSrvComb(self, value):
        self.VldSrvComb.append(value)
    def insert_VldSrvComb_at(self, index, value):
        self.VldSrvComb.insert(index, value)
    def replace_VldSrvComb_at(self, index, value):
        self.VldSrvComb[index] = value
    def get_TotalDiscount(self):
        return self.TotalDiscount
    def set_TotalDiscount(self, TotalDiscount):
        self.TotalDiscount = TotalDiscount
    def validate_TotalDiscountType(self, value):
        result = True
        # Validate type TotalDiscountType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on TotalDiscountType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.VldSrvComb or
            self.TotalDiscount is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ProdType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ProdType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ProdType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ProdType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ProdType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ProdType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ProdType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for VldSrvComb_ in self.VldSrvComb:
            namespaceprefix_ = self.VldSrvComb_nsprefix_ + ':' if (UseCapturedNS_ and self.VldSrvComb_nsprefix_) else ''
            VldSrvComb_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='VldSrvComb', pretty_print=pretty_print)
        if self.TotalDiscount is not None:
            namespaceprefix_ = self.TotalDiscount_nsprefix_ + ':' if (UseCapturedNS_ and self.TotalDiscount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTotalDiscount>%s</%sTotalDiscount>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TotalDiscount), input_name='TotalDiscount')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'VldSrvComb':
            obj_ = VldSrvCombType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.VldSrvComb.append(obj_)
            obj_.original_tagname_ = 'VldSrvComb'
        elif nodeName_ == 'TotalDiscount':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TotalDiscount')
            value_ = self.gds_validate_string(value_, node, 'TotalDiscount')
            self.TotalDiscount = value_
            self.TotalDiscount_nsprefix_ = child_.prefix
            # validate type TotalDiscountType
            self.validate_TotalDiscountType(self.TotalDiscount)
# end class ProdType


class NoteType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ActionStatus=None, Condition=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ActionStatus = ActionStatus
        self.ActionStatus_nsprefix_ = None
        if Condition is None:
            self.Condition = []
        else:
            self.Condition = Condition
        self.Condition_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, NoteType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if NoteType.subclass:
            return NoteType.subclass(*args_, **kwargs_)
        else:
            return NoteType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ActionStatus(self):
        return self.ActionStatus
    def set_ActionStatus(self, ActionStatus):
        self.ActionStatus = ActionStatus
    def get_Condition(self):
        return self.Condition
    def set_Condition(self, Condition):
        self.Condition = Condition
    def add_Condition(self, value):
        self.Condition.append(value)
    def insert_Condition_at(self, index, value):
        self.Condition.insert(index, value)
    def replace_Condition_at(self, index, value):
        self.Condition[index] = value
    def _hasContent(self):
        if (
            self.ActionStatus is not None or
            self.Condition
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NoteType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('NoteType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'NoteType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='NoteType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='NoteType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='NoteType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NoteType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ActionStatus is not None:
            namespaceprefix_ = self.ActionStatus_nsprefix_ + ':' if (UseCapturedNS_ and self.ActionStatus_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sActionStatus>%s</%sActionStatus>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ActionStatus), input_name='ActionStatus')), namespaceprefix_ , eol_))
        for Condition_ in self.Condition:
            namespaceprefix_ = self.Condition_nsprefix_ + ':' if (UseCapturedNS_ and self.Condition_nsprefix_) else ''
            Condition_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Condition', pretty_print=pretty_print)
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
        if nodeName_ == 'ActionStatus':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ActionStatus')
            value_ = self.gds_validate_string(value_, node, 'ActionStatus')
            self.ActionStatus = value_
            self.ActionStatus_nsprefix_ = child_.prefix
        elif nodeName_ == 'Condition':
            obj_ = ConditionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Condition.append(obj_)
            obj_.original_tagname_ = 'Condition'
# end class NoteType


class QtdShpExChrgType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, SpecialServiceType=None, LocalServiceType=None, GlobalServiceName=None, LocalServiceTypeName=None, SOfferedCustAgreement=None, ChargeCodeType=None, InsPrmRateInPercentage=None, CurrencyCode=None, ChargeValue=None, ChargeTaxAmount=None, ChargeTaxRate=None, ChargeTaxAmountDet=None, QtdSExtrChrgInAdCur=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.SpecialServiceType = SpecialServiceType
        self.validate_SpecialServiceTypeType(self.SpecialServiceType)
        self.SpecialServiceType_nsprefix_ = None
        self.LocalServiceType = LocalServiceType
        self.validate_LocalServiceTypeType(self.LocalServiceType)
        self.LocalServiceType_nsprefix_ = None
        self.GlobalServiceName = GlobalServiceName
        self.GlobalServiceName_nsprefix_ = None
        self.LocalServiceTypeName = LocalServiceTypeName
        self.LocalServiceTypeName_nsprefix_ = None
        self.SOfferedCustAgreement = SOfferedCustAgreement
        self.SOfferedCustAgreement_nsprefix_ = None
        self.ChargeCodeType = ChargeCodeType
        self.ChargeCodeType_nsprefix_ = None
        self.InsPrmRateInPercentage = InsPrmRateInPercentage
        self.validate_InsPrmRateInPercentageType(self.InsPrmRateInPercentage)
        self.InsPrmRateInPercentage_nsprefix_ = None
        self.CurrencyCode = CurrencyCode
        self.validate_CurrencyCodeType(self.CurrencyCode)
        self.CurrencyCode_nsprefix_ = None
        self.ChargeValue = ChargeValue
        self.validate_ChargeValueType(self.ChargeValue)
        self.ChargeValue_nsprefix_ = None
        self.ChargeTaxAmount = ChargeTaxAmount
        self.validate_ChargeTaxAmountType(self.ChargeTaxAmount)
        self.ChargeTaxAmount_nsprefix_ = None
        if ChargeTaxRate is None:
            self.ChargeTaxRate = []
        else:
            self.ChargeTaxRate = ChargeTaxRate
        self.ChargeTaxRate_nsprefix_ = None
        if ChargeTaxAmountDet is None:
            self.ChargeTaxAmountDet = []
        else:
            self.ChargeTaxAmountDet = ChargeTaxAmountDet
        self.ChargeTaxAmountDet_nsprefix_ = None
        if QtdSExtrChrgInAdCur is None:
            self.QtdSExtrChrgInAdCur = []
        else:
            self.QtdSExtrChrgInAdCur = QtdSExtrChrgInAdCur
        self.QtdSExtrChrgInAdCur_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, QtdShpExChrgType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if QtdShpExChrgType.subclass:
            return QtdShpExChrgType.subclass(*args_, **kwargs_)
        else:
            return QtdShpExChrgType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_SpecialServiceType(self):
        return self.SpecialServiceType
    def set_SpecialServiceType(self, SpecialServiceType):
        self.SpecialServiceType = SpecialServiceType
    def get_LocalServiceType(self):
        return self.LocalServiceType
    def set_LocalServiceType(self, LocalServiceType):
        self.LocalServiceType = LocalServiceType
    def get_GlobalServiceName(self):
        return self.GlobalServiceName
    def set_GlobalServiceName(self, GlobalServiceName):
        self.GlobalServiceName = GlobalServiceName
    def get_LocalServiceTypeName(self):
        return self.LocalServiceTypeName
    def set_LocalServiceTypeName(self, LocalServiceTypeName):
        self.LocalServiceTypeName = LocalServiceTypeName
    def get_SOfferedCustAgreement(self):
        return self.SOfferedCustAgreement
    def set_SOfferedCustAgreement(self, SOfferedCustAgreement):
        self.SOfferedCustAgreement = SOfferedCustAgreement
    def get_ChargeCodeType(self):
        return self.ChargeCodeType
    def set_ChargeCodeType(self, ChargeCodeType):
        self.ChargeCodeType = ChargeCodeType
    def get_InsPrmRateInPercentage(self):
        return self.InsPrmRateInPercentage
    def set_InsPrmRateInPercentage(self, InsPrmRateInPercentage):
        self.InsPrmRateInPercentage = InsPrmRateInPercentage
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_ChargeValue(self):
        return self.ChargeValue
    def set_ChargeValue(self, ChargeValue):
        self.ChargeValue = ChargeValue
    def get_ChargeTaxAmount(self):
        return self.ChargeTaxAmount
    def set_ChargeTaxAmount(self, ChargeTaxAmount):
        self.ChargeTaxAmount = ChargeTaxAmount
    def get_ChargeTaxRate(self):
        return self.ChargeTaxRate
    def set_ChargeTaxRate(self, ChargeTaxRate):
        self.ChargeTaxRate = ChargeTaxRate
    def add_ChargeTaxRate(self, value):
        self.ChargeTaxRate.append(value)
    def insert_ChargeTaxRate_at(self, index, value):
        self.ChargeTaxRate.insert(index, value)
    def replace_ChargeTaxRate_at(self, index, value):
        self.ChargeTaxRate[index] = value
    def get_ChargeTaxAmountDet(self):
        return self.ChargeTaxAmountDet
    def set_ChargeTaxAmountDet(self, ChargeTaxAmountDet):
        self.ChargeTaxAmountDet = ChargeTaxAmountDet
    def add_ChargeTaxAmountDet(self, value):
        self.ChargeTaxAmountDet.append(value)
    def insert_ChargeTaxAmountDet_at(self, index, value):
        self.ChargeTaxAmountDet.insert(index, value)
    def replace_ChargeTaxAmountDet_at(self, index, value):
        self.ChargeTaxAmountDet[index] = value
    def get_QtdSExtrChrgInAdCur(self):
        return self.QtdSExtrChrgInAdCur
    def set_QtdSExtrChrgInAdCur(self, QtdSExtrChrgInAdCur):
        self.QtdSExtrChrgInAdCur = QtdSExtrChrgInAdCur
    def add_QtdSExtrChrgInAdCur(self, value):
        self.QtdSExtrChrgInAdCur.append(value)
    def insert_QtdSExtrChrgInAdCur_at(self, index, value):
        self.QtdSExtrChrgInAdCur.insert(index, value)
    def replace_QtdSExtrChrgInAdCur_at(self, index, value):
        self.QtdSExtrChrgInAdCur[index] = value
    def validate_SpecialServiceTypeType(self, value):
        result = True
        # Validate type SpecialServiceTypeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on SpecialServiceTypeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_LocalServiceTypeType(self, value):
        result = True
        # Validate type LocalServiceTypeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on LocalServiceTypeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_InsPrmRateInPercentageType(self, value):
        result = True
        # Validate type InsPrmRateInPercentageType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 8:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on InsPrmRateInPercentageType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_CurrencyCodeType(self, value):
        result = True
        # Validate type CurrencyCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CurrencyCodeType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ChargeValueType(self, value):
        result = True
        # Validate type ChargeValueType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on ChargeValueType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_ChargeTaxAmountType(self, value):
        result = True
        # Validate type ChargeTaxAmountType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on ChargeTaxAmountType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_ChargeTaxRateType(self, value):
        result = True
        # Validate type ChargeTaxRateType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on ChargeTaxRateType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.SpecialServiceType is not None or
            self.LocalServiceType is not None or
            self.GlobalServiceName is not None or
            self.LocalServiceTypeName is not None or
            self.SOfferedCustAgreement is not None or
            self.ChargeCodeType is not None or
            self.InsPrmRateInPercentage is not None or
            self.CurrencyCode is not None or
            self.ChargeValue is not None or
            self.ChargeTaxAmount is not None or
            self.ChargeTaxRate or
            self.ChargeTaxAmountDet or
            self.QtdSExtrChrgInAdCur
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='QtdShpExChrgType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('QtdShpExChrgType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'QtdShpExChrgType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='QtdShpExChrgType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='QtdShpExChrgType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='QtdShpExChrgType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='QtdShpExChrgType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.SpecialServiceType is not None:
            namespaceprefix_ = self.SpecialServiceType_nsprefix_ + ':' if (UseCapturedNS_ and self.SpecialServiceType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSpecialServiceType>%s</%sSpecialServiceType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SpecialServiceType), input_name='SpecialServiceType')), namespaceprefix_ , eol_))
        if self.LocalServiceType is not None:
            namespaceprefix_ = self.LocalServiceType_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalServiceType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalServiceType>%s</%sLocalServiceType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalServiceType), input_name='LocalServiceType')), namespaceprefix_ , eol_))
        if self.GlobalServiceName is not None:
            namespaceprefix_ = self.GlobalServiceName_nsprefix_ + ':' if (UseCapturedNS_ and self.GlobalServiceName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGlobalServiceName>%s</%sGlobalServiceName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GlobalServiceName), input_name='GlobalServiceName')), namespaceprefix_ , eol_))
        if self.LocalServiceTypeName is not None:
            namespaceprefix_ = self.LocalServiceTypeName_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalServiceTypeName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalServiceTypeName>%s</%sLocalServiceTypeName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalServiceTypeName), input_name='LocalServiceTypeName')), namespaceprefix_ , eol_))
        if self.SOfferedCustAgreement is not None:
            namespaceprefix_ = self.SOfferedCustAgreement_nsprefix_ + ':' if (UseCapturedNS_ and self.SOfferedCustAgreement_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSOfferedCustAgreement>%s</%sSOfferedCustAgreement>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SOfferedCustAgreement), input_name='SOfferedCustAgreement')), namespaceprefix_ , eol_))
        if self.ChargeCodeType is not None:
            namespaceprefix_ = self.ChargeCodeType_nsprefix_ + ':' if (UseCapturedNS_ and self.ChargeCodeType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChargeCodeType>%s</%sChargeCodeType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ChargeCodeType), input_name='ChargeCodeType')), namespaceprefix_ , eol_))
        if self.InsPrmRateInPercentage is not None:
            namespaceprefix_ = self.InsPrmRateInPercentage_nsprefix_ + ':' if (UseCapturedNS_ and self.InsPrmRateInPercentage_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sInsPrmRateInPercentage>%s</%sInsPrmRateInPercentage>%s' % (namespaceprefix_ , self.gds_format_decimal(self.InsPrmRateInPercentage, input_name='InsPrmRateInPercentage'), namespaceprefix_ , eol_))
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.ChargeValue is not None:
            namespaceprefix_ = self.ChargeValue_nsprefix_ + ':' if (UseCapturedNS_ and self.ChargeValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChargeValue>%s</%sChargeValue>%s' % (namespaceprefix_ , self.gds_format_decimal(self.ChargeValue, input_name='ChargeValue'), namespaceprefix_ , eol_))
        if self.ChargeTaxAmount is not None:
            namespaceprefix_ = self.ChargeTaxAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.ChargeTaxAmount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChargeTaxAmount>%s</%sChargeTaxAmount>%s' % (namespaceprefix_ , self.gds_format_decimal(self.ChargeTaxAmount, input_name='ChargeTaxAmount'), namespaceprefix_ , eol_))
        for ChargeTaxRate_ in self.ChargeTaxRate:
            namespaceprefix_ = self.ChargeTaxRate_nsprefix_ + ':' if (UseCapturedNS_ and self.ChargeTaxRate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChargeTaxRate>%s</%sChargeTaxRate>%s' % (namespaceprefix_ , self.gds_format_decimal(ChargeTaxRate_, input_name='ChargeTaxRate'), namespaceprefix_ , eol_))
        for ChargeTaxAmountDet_ in self.ChargeTaxAmountDet:
            namespaceprefix_ = self.ChargeTaxAmountDet_nsprefix_ + ':' if (UseCapturedNS_ and self.ChargeTaxAmountDet_nsprefix_) else ''
            ChargeTaxAmountDet_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ChargeTaxAmountDet', pretty_print=pretty_print)
        for QtdSExtrChrgInAdCur_ in self.QtdSExtrChrgInAdCur:
            namespaceprefix_ = self.QtdSExtrChrgInAdCur_nsprefix_ + ':' if (UseCapturedNS_ and self.QtdSExtrChrgInAdCur_nsprefix_) else ''
            QtdSExtrChrgInAdCur_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='QtdSExtrChrgInAdCur', pretty_print=pretty_print)
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
        if nodeName_ == 'SpecialServiceType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SpecialServiceType')
            value_ = self.gds_validate_string(value_, node, 'SpecialServiceType')
            self.SpecialServiceType = value_
            self.SpecialServiceType_nsprefix_ = child_.prefix
            # validate type SpecialServiceTypeType
            self.validate_SpecialServiceTypeType(self.SpecialServiceType)
        elif nodeName_ == 'LocalServiceType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalServiceType')
            value_ = self.gds_validate_string(value_, node, 'LocalServiceType')
            self.LocalServiceType = value_
            self.LocalServiceType_nsprefix_ = child_.prefix
            # validate type LocalServiceTypeType
            self.validate_LocalServiceTypeType(self.LocalServiceType)
        elif nodeName_ == 'GlobalServiceName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GlobalServiceName')
            value_ = self.gds_validate_string(value_, node, 'GlobalServiceName')
            self.GlobalServiceName = value_
            self.GlobalServiceName_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocalServiceTypeName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalServiceTypeName')
            value_ = self.gds_validate_string(value_, node, 'LocalServiceTypeName')
            self.LocalServiceTypeName = value_
            self.LocalServiceTypeName_nsprefix_ = child_.prefix
        elif nodeName_ == 'SOfferedCustAgreement':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SOfferedCustAgreement')
            value_ = self.gds_validate_string(value_, node, 'SOfferedCustAgreement')
            self.SOfferedCustAgreement = value_
            self.SOfferedCustAgreement_nsprefix_ = child_.prefix
        elif nodeName_ == 'ChargeCodeType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChargeCodeType')
            value_ = self.gds_validate_string(value_, node, 'ChargeCodeType')
            self.ChargeCodeType = value_
            self.ChargeCodeType_nsprefix_ = child_.prefix
        elif nodeName_ == 'InsPrmRateInPercentage' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'InsPrmRateInPercentage')
            fval_ = self.gds_validate_decimal(fval_, node, 'InsPrmRateInPercentage')
            self.InsPrmRateInPercentage = fval_
            self.InsPrmRateInPercentage_nsprefix_ = child_.prefix
            # validate type InsPrmRateInPercentageType
            self.validate_InsPrmRateInPercentageType(self.InsPrmRateInPercentage)
        elif nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
            # validate type CurrencyCodeType
            self.validate_CurrencyCodeType(self.CurrencyCode)
        elif nodeName_ == 'ChargeValue' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ChargeValue')
            fval_ = self.gds_validate_decimal(fval_, node, 'ChargeValue')
            self.ChargeValue = fval_
            self.ChargeValue_nsprefix_ = child_.prefix
            # validate type ChargeValueType
            self.validate_ChargeValueType(self.ChargeValue)
        elif nodeName_ == 'ChargeTaxAmount' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ChargeTaxAmount')
            fval_ = self.gds_validate_decimal(fval_, node, 'ChargeTaxAmount')
            self.ChargeTaxAmount = fval_
            self.ChargeTaxAmount_nsprefix_ = child_.prefix
            # validate type ChargeTaxAmountType
            self.validate_ChargeTaxAmountType(self.ChargeTaxAmount)
        elif nodeName_ == 'ChargeTaxRate' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ChargeTaxRate')
            fval_ = self.gds_validate_decimal(fval_, node, 'ChargeTaxRate')
            self.ChargeTaxRate.append(fval_)
            self.ChargeTaxRate_nsprefix_ = child_.prefix
            # validate type ChargeTaxRateType
            self.validate_ChargeTaxRateType(self.ChargeTaxRate[-1])
        elif nodeName_ == 'ChargeTaxAmountDet':
            obj_ = ChargeTaxAmountDetType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ChargeTaxAmountDet.append(obj_)
            obj_.original_tagname_ = 'ChargeTaxAmountDet'
        elif nodeName_ == 'QtdSExtrChrgInAdCur':
            obj_ = QtdSExtrChrgInAdCurType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.QtdSExtrChrgInAdCur.append(obj_)
            obj_.original_tagname_ = 'QtdSExtrChrgInAdCur'
# end class QtdShpExChrgType


class WeightChargeTaxDetType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TaxTypeRate=None, TaxTypeCode=None, WeightChargeTax=None, BaseAmt=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.TaxTypeRate = TaxTypeRate
        self.validate_TaxTypeRateType(self.TaxTypeRate)
        self.TaxTypeRate_nsprefix_ = None
        self.TaxTypeCode = TaxTypeCode
        self.validate_TaxTypeCodeType(self.TaxTypeCode)
        self.TaxTypeCode_nsprefix_ = None
        self.WeightChargeTax = WeightChargeTax
        self.validate_WeightChargeTaxType(self.WeightChargeTax)
        self.WeightChargeTax_nsprefix_ = None
        self.BaseAmt = BaseAmt
        self.validate_BaseAmtType(self.BaseAmt)
        self.BaseAmt_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, WeightChargeTaxDetType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if WeightChargeTaxDetType.subclass:
            return WeightChargeTaxDetType.subclass(*args_, **kwargs_)
        else:
            return WeightChargeTaxDetType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_TaxTypeRate(self):
        return self.TaxTypeRate
    def set_TaxTypeRate(self, TaxTypeRate):
        self.TaxTypeRate = TaxTypeRate
    def get_TaxTypeCode(self):
        return self.TaxTypeCode
    def set_TaxTypeCode(self, TaxTypeCode):
        self.TaxTypeCode = TaxTypeCode
    def get_WeightChargeTax(self):
        return self.WeightChargeTax
    def set_WeightChargeTax(self, WeightChargeTax):
        self.WeightChargeTax = WeightChargeTax
    def get_BaseAmt(self):
        return self.BaseAmt
    def set_BaseAmt(self, BaseAmt):
        self.BaseAmt = BaseAmt
    def validate_TaxTypeRateType(self, value):
        result = True
        # Validate type TaxTypeRateType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 8:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on TaxTypeRateType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_TaxTypeCodeType(self, value):
        result = True
        # Validate type TaxTypeCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on TaxTypeCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_WeightChargeTaxType(self, value):
        result = True
        # Validate type WeightChargeTaxType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on WeightChargeTaxType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_BaseAmtType(self, value):
        result = True
        # Validate type BaseAmtType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on BaseAmtType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.TaxTypeRate is not None or
            self.TaxTypeCode is not None or
            self.WeightChargeTax is not None or
            self.BaseAmt is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WeightChargeTaxDetType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('WeightChargeTaxDetType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'WeightChargeTaxDetType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='WeightChargeTaxDetType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='WeightChargeTaxDetType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='WeightChargeTaxDetType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WeightChargeTaxDetType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.TaxTypeRate is not None:
            namespaceprefix_ = self.TaxTypeRate_nsprefix_ + ':' if (UseCapturedNS_ and self.TaxTypeRate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTaxTypeRate>%s</%sTaxTypeRate>%s' % (namespaceprefix_ , self.gds_format_decimal(self.TaxTypeRate, input_name='TaxTypeRate'), namespaceprefix_ , eol_))
        if self.TaxTypeCode is not None:
            namespaceprefix_ = self.TaxTypeCode_nsprefix_ + ':' if (UseCapturedNS_ and self.TaxTypeCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTaxTypeCode>%s</%sTaxTypeCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TaxTypeCode), input_name='TaxTypeCode')), namespaceprefix_ , eol_))
        if self.WeightChargeTax is not None:
            namespaceprefix_ = self.WeightChargeTax_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightChargeTax_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeightChargeTax>%s</%sWeightChargeTax>%s' % (namespaceprefix_ , self.gds_format_decimal(self.WeightChargeTax, input_name='WeightChargeTax'), namespaceprefix_ , eol_))
        if self.BaseAmt is not None:
            namespaceprefix_ = self.BaseAmt_nsprefix_ + ':' if (UseCapturedNS_ and self.BaseAmt_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBaseAmt>%s</%sBaseAmt>%s' % (namespaceprefix_ , self.gds_format_decimal(self.BaseAmt, input_name='BaseAmt'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'TaxTypeRate' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'TaxTypeRate')
            fval_ = self.gds_validate_decimal(fval_, node, 'TaxTypeRate')
            self.TaxTypeRate = fval_
            self.TaxTypeRate_nsprefix_ = child_.prefix
            # validate type TaxTypeRateType
            self.validate_TaxTypeRateType(self.TaxTypeRate)
        elif nodeName_ == 'TaxTypeCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TaxTypeCode')
            value_ = self.gds_validate_string(value_, node, 'TaxTypeCode')
            self.TaxTypeCode = value_
            self.TaxTypeCode_nsprefix_ = child_.prefix
            # validate type TaxTypeCodeType
            self.validate_TaxTypeCodeType(self.TaxTypeCode)
        elif nodeName_ == 'WeightChargeTax' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'WeightChargeTax')
            fval_ = self.gds_validate_decimal(fval_, node, 'WeightChargeTax')
            self.WeightChargeTax = fval_
            self.WeightChargeTax_nsprefix_ = child_.prefix
            # validate type WeightChargeTaxType
            self.validate_WeightChargeTaxType(self.WeightChargeTax)
        elif nodeName_ == 'BaseAmt' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'BaseAmt')
            fval_ = self.gds_validate_decimal(fval_, node, 'BaseAmt')
            self.BaseAmt = fval_
            self.BaseAmt_nsprefix_ = child_.prefix
            # validate type BaseAmtType
            self.validate_BaseAmtType(self.BaseAmt)
# end class WeightChargeTaxDetType


class ChargeTaxAmountDetType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, TaxTypeRate=None, TaxTypeCode=None, TaxAmount=None, BaseAmount=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.TaxTypeRate = TaxTypeRate
        self.validate_TaxTypeRateType4(self.TaxTypeRate)
        self.TaxTypeRate_nsprefix_ = None
        self.TaxTypeCode = TaxTypeCode
        self.validate_TaxTypeCodeType5(self.TaxTypeCode)
        self.TaxTypeCode_nsprefix_ = None
        self.TaxAmount = TaxAmount
        self.validate_TaxAmountType(self.TaxAmount)
        self.TaxAmount_nsprefix_ = None
        self.BaseAmount = BaseAmount
        self.validate_BaseAmountType(self.BaseAmount)
        self.BaseAmount_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ChargeTaxAmountDetType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ChargeTaxAmountDetType.subclass:
            return ChargeTaxAmountDetType.subclass(*args_, **kwargs_)
        else:
            return ChargeTaxAmountDetType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_TaxTypeRate(self):
        return self.TaxTypeRate
    def set_TaxTypeRate(self, TaxTypeRate):
        self.TaxTypeRate = TaxTypeRate
    def get_TaxTypeCode(self):
        return self.TaxTypeCode
    def set_TaxTypeCode(self, TaxTypeCode):
        self.TaxTypeCode = TaxTypeCode
    def get_TaxAmount(self):
        return self.TaxAmount
    def set_TaxAmount(self, TaxAmount):
        self.TaxAmount = TaxAmount
    def get_BaseAmount(self):
        return self.BaseAmount
    def set_BaseAmount(self, BaseAmount):
        self.BaseAmount = BaseAmount
    def validate_TaxTypeRateType4(self, value):
        result = True
        # Validate type TaxTypeRateType4, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 8:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on TaxTypeRateType4' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_TaxTypeCodeType5(self, value):
        result = True
        # Validate type TaxTypeCodeType5, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on TaxTypeCodeType5' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_TaxAmountType(self, value):
        result = True
        # Validate type TaxAmountType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on TaxAmountType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_BaseAmountType(self, value):
        result = True
        # Validate type BaseAmountType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on BaseAmountType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.TaxTypeRate is not None or
            self.TaxTypeCode is not None or
            self.TaxAmount is not None or
            self.BaseAmount is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ChargeTaxAmountDetType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ChargeTaxAmountDetType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ChargeTaxAmountDetType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ChargeTaxAmountDetType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ChargeTaxAmountDetType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ChargeTaxAmountDetType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ChargeTaxAmountDetType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.TaxTypeRate is not None:
            namespaceprefix_ = self.TaxTypeRate_nsprefix_ + ':' if (UseCapturedNS_ and self.TaxTypeRate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTaxTypeRate>%s</%sTaxTypeRate>%s' % (namespaceprefix_ , self.gds_format_decimal(self.TaxTypeRate, input_name='TaxTypeRate'), namespaceprefix_ , eol_))
        if self.TaxTypeCode is not None:
            namespaceprefix_ = self.TaxTypeCode_nsprefix_ + ':' if (UseCapturedNS_ and self.TaxTypeCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTaxTypeCode>%s</%sTaxTypeCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TaxTypeCode), input_name='TaxTypeCode')), namespaceprefix_ , eol_))
        if self.TaxAmount is not None:
            namespaceprefix_ = self.TaxAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.TaxAmount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTaxAmount>%s</%sTaxAmount>%s' % (namespaceprefix_ , self.gds_format_decimal(self.TaxAmount, input_name='TaxAmount'), namespaceprefix_ , eol_))
        if self.BaseAmount is not None:
            namespaceprefix_ = self.BaseAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.BaseAmount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBaseAmount>%s</%sBaseAmount>%s' % (namespaceprefix_ , self.gds_format_decimal(self.BaseAmount, input_name='BaseAmount'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'TaxTypeRate' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'TaxTypeRate')
            fval_ = self.gds_validate_decimal(fval_, node, 'TaxTypeRate')
            self.TaxTypeRate = fval_
            self.TaxTypeRate_nsprefix_ = child_.prefix
            # validate type TaxTypeRateType4
            self.validate_TaxTypeRateType4(self.TaxTypeRate)
        elif nodeName_ == 'TaxTypeCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TaxTypeCode')
            value_ = self.gds_validate_string(value_, node, 'TaxTypeCode')
            self.TaxTypeCode = value_
            self.TaxTypeCode_nsprefix_ = child_.prefix
            # validate type TaxTypeCodeType5
            self.validate_TaxTypeCodeType5(self.TaxTypeCode)
        elif nodeName_ == 'TaxAmount' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'TaxAmount')
            fval_ = self.gds_validate_decimal(fval_, node, 'TaxAmount')
            self.TaxAmount = fval_
            self.TaxAmount_nsprefix_ = child_.prefix
            # validate type TaxAmountType
            self.validate_TaxAmountType(self.TaxAmount)
        elif nodeName_ == 'BaseAmount' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'BaseAmount')
            fval_ = self.gds_validate_decimal(fval_, node, 'BaseAmount')
            self.BaseAmount = fval_
            self.BaseAmount_nsprefix_ = child_.prefix
            # validate type BaseAmountType
            self.validate_BaseAmountType(self.BaseAmount)
# end class ChargeTaxAmountDetType


class QtdSInAdCurType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CustomsValue=None, ExchangeRate=None, CurrencyCode=None, CurrencyRoleTypeCode=None, WeightCharge=None, TotalAmount=None, TotalTaxAmount=None, WeightChargeTax=None, WeightChargeTaxDet=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CustomsValue = CustomsValue
        self.validate_CustomsValueType(self.CustomsValue)
        self.CustomsValue_nsprefix_ = None
        self.ExchangeRate = ExchangeRate
        self.validate_ExchangeRateType(self.ExchangeRate)
        self.ExchangeRate_nsprefix_ = None
        self.CurrencyCode = CurrencyCode
        self.validate_CurrencyCodeType6(self.CurrencyCode)
        self.CurrencyCode_nsprefix_ = None
        self.CurrencyRoleTypeCode = CurrencyRoleTypeCode
        self.validate_CurrencyRoleTypeCodeType(self.CurrencyRoleTypeCode)
        self.CurrencyRoleTypeCode_nsprefix_ = None
        self.WeightCharge = WeightCharge
        self.validate_WeightChargeType(self.WeightCharge)
        self.WeightCharge_nsprefix_ = None
        self.TotalAmount = TotalAmount
        self.validate_TotalAmountType(self.TotalAmount)
        self.TotalAmount_nsprefix_ = None
        self.TotalTaxAmount = TotalTaxAmount
        self.validate_TotalTaxAmountType(self.TotalTaxAmount)
        self.TotalTaxAmount_nsprefix_ = None
        self.WeightChargeTax = WeightChargeTax
        self.validate_WeightChargeTaxType7(self.WeightChargeTax)
        self.WeightChargeTax_nsprefix_ = None
        if WeightChargeTaxDet is None:
            self.WeightChargeTaxDet = []
        else:
            self.WeightChargeTaxDet = WeightChargeTaxDet
        self.WeightChargeTaxDet_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, QtdSInAdCurType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if QtdSInAdCurType.subclass:
            return QtdSInAdCurType.subclass(*args_, **kwargs_)
        else:
            return QtdSInAdCurType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CustomsValue(self):
        return self.CustomsValue
    def set_CustomsValue(self, CustomsValue):
        self.CustomsValue = CustomsValue
    def get_ExchangeRate(self):
        return self.ExchangeRate
    def set_ExchangeRate(self, ExchangeRate):
        self.ExchangeRate = ExchangeRate
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_CurrencyRoleTypeCode(self):
        return self.CurrencyRoleTypeCode
    def set_CurrencyRoleTypeCode(self, CurrencyRoleTypeCode):
        self.CurrencyRoleTypeCode = CurrencyRoleTypeCode
    def get_WeightCharge(self):
        return self.WeightCharge
    def set_WeightCharge(self, WeightCharge):
        self.WeightCharge = WeightCharge
    def get_TotalAmount(self):
        return self.TotalAmount
    def set_TotalAmount(self, TotalAmount):
        self.TotalAmount = TotalAmount
    def get_TotalTaxAmount(self):
        return self.TotalTaxAmount
    def set_TotalTaxAmount(self, TotalTaxAmount):
        self.TotalTaxAmount = TotalTaxAmount
    def get_WeightChargeTax(self):
        return self.WeightChargeTax
    def set_WeightChargeTax(self, WeightChargeTax):
        self.WeightChargeTax = WeightChargeTax
    def get_WeightChargeTaxDet(self):
        return self.WeightChargeTaxDet
    def set_WeightChargeTaxDet(self, WeightChargeTaxDet):
        self.WeightChargeTaxDet = WeightChargeTaxDet
    def add_WeightChargeTaxDet(self, value):
        self.WeightChargeTaxDet.append(value)
    def insert_WeightChargeTaxDet_at(self, index, value):
        self.WeightChargeTaxDet.insert(index, value)
    def replace_WeightChargeTaxDet_at(self, index, value):
        self.WeightChargeTaxDet[index] = value
    def validate_CustomsValueType(self, value):
        result = True
        # Validate type CustomsValueType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on CustomsValueType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_ExchangeRateType(self, value):
        result = True
        # Validate type ExchangeRateType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on ExchangeRateType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_CurrencyCodeType6(self, value):
        result = True
        # Validate type CurrencyCodeType6, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CurrencyCodeType6' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CurrencyRoleTypeCodeType(self, value):
        result = True
        # Validate type CurrencyRoleTypeCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CurrencyRoleTypeCodeType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_WeightChargeType(self, value):
        result = True
        # Validate type WeightChargeType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on WeightChargeType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_TotalAmountType(self, value):
        result = True
        # Validate type TotalAmountType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on TotalAmountType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_TotalTaxAmountType(self, value):
        result = True
        # Validate type TotalTaxAmountType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on TotalTaxAmountType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_WeightChargeTaxType7(self, value):
        result = True
        # Validate type WeightChargeTaxType7, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on WeightChargeTaxType7' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.CustomsValue is not None or
            self.ExchangeRate is not None or
            self.CurrencyCode is not None or
            self.CurrencyRoleTypeCode is not None or
            self.WeightCharge is not None or
            self.TotalAmount is not None or
            self.TotalTaxAmount is not None or
            self.WeightChargeTax is not None or
            self.WeightChargeTaxDet
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='QtdSInAdCurType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('QtdSInAdCurType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'QtdSInAdCurType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='QtdSInAdCurType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='QtdSInAdCurType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='QtdSInAdCurType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='QtdSInAdCurType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CustomsValue is not None:
            namespaceprefix_ = self.CustomsValue_nsprefix_ + ':' if (UseCapturedNS_ and self.CustomsValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCustomsValue>%s</%sCustomsValue>%s' % (namespaceprefix_ , self.gds_format_decimal(self.CustomsValue, input_name='CustomsValue'), namespaceprefix_ , eol_))
        if self.ExchangeRate is not None:
            namespaceprefix_ = self.ExchangeRate_nsprefix_ + ':' if (UseCapturedNS_ and self.ExchangeRate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExchangeRate>%s</%sExchangeRate>%s' % (namespaceprefix_ , self.gds_format_decimal(self.ExchangeRate, input_name='ExchangeRate'), namespaceprefix_ , eol_))
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.CurrencyRoleTypeCode is not None:
            namespaceprefix_ = self.CurrencyRoleTypeCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyRoleTypeCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyRoleTypeCode>%s</%sCurrencyRoleTypeCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyRoleTypeCode), input_name='CurrencyRoleTypeCode')), namespaceprefix_ , eol_))
        if self.WeightCharge is not None:
            namespaceprefix_ = self.WeightCharge_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightCharge_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeightCharge>%s</%sWeightCharge>%s' % (namespaceprefix_ , self.gds_format_decimal(self.WeightCharge, input_name='WeightCharge'), namespaceprefix_ , eol_))
        if self.TotalAmount is not None:
            namespaceprefix_ = self.TotalAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.TotalAmount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTotalAmount>%s</%sTotalAmount>%s' % (namespaceprefix_ , self.gds_format_decimal(self.TotalAmount, input_name='TotalAmount'), namespaceprefix_ , eol_))
        if self.TotalTaxAmount is not None:
            namespaceprefix_ = self.TotalTaxAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.TotalTaxAmount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTotalTaxAmount>%s</%sTotalTaxAmount>%s' % (namespaceprefix_ , self.gds_format_decimal(self.TotalTaxAmount, input_name='TotalTaxAmount'), namespaceprefix_ , eol_))
        if self.WeightChargeTax is not None:
            namespaceprefix_ = self.WeightChargeTax_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightChargeTax_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeightChargeTax>%s</%sWeightChargeTax>%s' % (namespaceprefix_ , self.gds_format_decimal(self.WeightChargeTax, input_name='WeightChargeTax'), namespaceprefix_ , eol_))
        for WeightChargeTaxDet_ in self.WeightChargeTaxDet:
            namespaceprefix_ = self.WeightChargeTaxDet_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightChargeTaxDet_nsprefix_) else ''
            WeightChargeTaxDet_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='WeightChargeTaxDet', pretty_print=pretty_print)
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
        if nodeName_ == 'CustomsValue' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'CustomsValue')
            fval_ = self.gds_validate_decimal(fval_, node, 'CustomsValue')
            self.CustomsValue = fval_
            self.CustomsValue_nsprefix_ = child_.prefix
            # validate type CustomsValueType
            self.validate_CustomsValueType(self.CustomsValue)
        elif nodeName_ == 'ExchangeRate' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ExchangeRate')
            fval_ = self.gds_validate_decimal(fval_, node, 'ExchangeRate')
            self.ExchangeRate = fval_
            self.ExchangeRate_nsprefix_ = child_.prefix
            # validate type ExchangeRateType
            self.validate_ExchangeRateType(self.ExchangeRate)
        elif nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
            # validate type CurrencyCodeType6
            self.validate_CurrencyCodeType6(self.CurrencyCode)
        elif nodeName_ == 'CurrencyRoleTypeCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyRoleTypeCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyRoleTypeCode')
            self.CurrencyRoleTypeCode = value_
            self.CurrencyRoleTypeCode_nsprefix_ = child_.prefix
            # validate type CurrencyRoleTypeCodeType
            self.validate_CurrencyRoleTypeCodeType(self.CurrencyRoleTypeCode)
        elif nodeName_ == 'WeightCharge' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'WeightCharge')
            fval_ = self.gds_validate_decimal(fval_, node, 'WeightCharge')
            self.WeightCharge = fval_
            self.WeightCharge_nsprefix_ = child_.prefix
            # validate type WeightChargeType
            self.validate_WeightChargeType(self.WeightCharge)
        elif nodeName_ == 'TotalAmount' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'TotalAmount')
            fval_ = self.gds_validate_decimal(fval_, node, 'TotalAmount')
            self.TotalAmount = fval_
            self.TotalAmount_nsprefix_ = child_.prefix
            # validate type TotalAmountType
            self.validate_TotalAmountType(self.TotalAmount)
        elif nodeName_ == 'TotalTaxAmount' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'TotalTaxAmount')
            fval_ = self.gds_validate_decimal(fval_, node, 'TotalTaxAmount')
            self.TotalTaxAmount = fval_
            self.TotalTaxAmount_nsprefix_ = child_.prefix
            # validate type TotalTaxAmountType
            self.validate_TotalTaxAmountType(self.TotalTaxAmount)
        elif nodeName_ == 'WeightChargeTax' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'WeightChargeTax')
            fval_ = self.gds_validate_decimal(fval_, node, 'WeightChargeTax')
            self.WeightChargeTax = fval_
            self.WeightChargeTax_nsprefix_ = child_.prefix
            # validate type WeightChargeTaxType7
            self.validate_WeightChargeTaxType7(self.WeightChargeTax)
        elif nodeName_ == 'WeightChargeTaxDet':
            obj_ = WeightChargeTaxDetType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.WeightChargeTaxDet.append(obj_)
            obj_.original_tagname_ = 'WeightChargeTaxDet'
# end class QtdSInAdCurType


class QtdSExtrChrgInAdCurType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ChargeValue=None, ChargeExchangeRate=None, ChargeTaxAmount=None, CurrencyCode=None, CurrencyRoleTypeCode=None, ChargeTaxAmountDet=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ChargeValue = ChargeValue
        self.validate_ChargeValueType8(self.ChargeValue)
        self.ChargeValue_nsprefix_ = None
        self.ChargeExchangeRate = ChargeExchangeRate
        self.validate_ChargeExchangeRateType(self.ChargeExchangeRate)
        self.ChargeExchangeRate_nsprefix_ = None
        self.ChargeTaxAmount = ChargeTaxAmount
        self.validate_ChargeTaxAmountType9(self.ChargeTaxAmount)
        self.ChargeTaxAmount_nsprefix_ = None
        self.CurrencyCode = CurrencyCode
        self.validate_CurrencyCodeType10(self.CurrencyCode)
        self.CurrencyCode_nsprefix_ = None
        self.CurrencyRoleTypeCode = CurrencyRoleTypeCode
        self.validate_CurrencyRoleTypeCodeType11(self.CurrencyRoleTypeCode)
        self.CurrencyRoleTypeCode_nsprefix_ = None
        if ChargeTaxAmountDet is None:
            self.ChargeTaxAmountDet = []
        else:
            self.ChargeTaxAmountDet = ChargeTaxAmountDet
        self.ChargeTaxAmountDet_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, QtdSExtrChrgInAdCurType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if QtdSExtrChrgInAdCurType.subclass:
            return QtdSExtrChrgInAdCurType.subclass(*args_, **kwargs_)
        else:
            return QtdSExtrChrgInAdCurType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ChargeValue(self):
        return self.ChargeValue
    def set_ChargeValue(self, ChargeValue):
        self.ChargeValue = ChargeValue
    def get_ChargeExchangeRate(self):
        return self.ChargeExchangeRate
    def set_ChargeExchangeRate(self, ChargeExchangeRate):
        self.ChargeExchangeRate = ChargeExchangeRate
    def get_ChargeTaxAmount(self):
        return self.ChargeTaxAmount
    def set_ChargeTaxAmount(self, ChargeTaxAmount):
        self.ChargeTaxAmount = ChargeTaxAmount
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_CurrencyRoleTypeCode(self):
        return self.CurrencyRoleTypeCode
    def set_CurrencyRoleTypeCode(self, CurrencyRoleTypeCode):
        self.CurrencyRoleTypeCode = CurrencyRoleTypeCode
    def get_ChargeTaxAmountDet(self):
        return self.ChargeTaxAmountDet
    def set_ChargeTaxAmountDet(self, ChargeTaxAmountDet):
        self.ChargeTaxAmountDet = ChargeTaxAmountDet
    def add_ChargeTaxAmountDet(self, value):
        self.ChargeTaxAmountDet.append(value)
    def insert_ChargeTaxAmountDet_at(self, index, value):
        self.ChargeTaxAmountDet.insert(index, value)
    def replace_ChargeTaxAmountDet_at(self, index, value):
        self.ChargeTaxAmountDet[index] = value
    def validate_ChargeValueType8(self, value):
        result = True
        # Validate type ChargeValueType8, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on ChargeValueType8' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_ChargeExchangeRateType(self, value):
        result = True
        # Validate type ChargeExchangeRateType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on ChargeExchangeRateType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_ChargeTaxAmountType9(self, value):
        result = True
        # Validate type ChargeTaxAmountType9, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on ChargeTaxAmountType9' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_CurrencyCodeType10(self, value):
        result = True
        # Validate type CurrencyCodeType10, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CurrencyCodeType10' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CurrencyRoleTypeCodeType11(self, value):
        result = True
        # Validate type CurrencyRoleTypeCodeType11, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CurrencyRoleTypeCodeType11' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.ChargeValue is not None or
            self.ChargeExchangeRate is not None or
            self.ChargeTaxAmount is not None or
            self.CurrencyCode is not None or
            self.CurrencyRoleTypeCode is not None or
            self.ChargeTaxAmountDet
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='QtdSExtrChrgInAdCurType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('QtdSExtrChrgInAdCurType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'QtdSExtrChrgInAdCurType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='QtdSExtrChrgInAdCurType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='QtdSExtrChrgInAdCurType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='QtdSExtrChrgInAdCurType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='QtdSExtrChrgInAdCurType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ChargeValue is not None:
            namespaceprefix_ = self.ChargeValue_nsprefix_ + ':' if (UseCapturedNS_ and self.ChargeValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChargeValue>%s</%sChargeValue>%s' % (namespaceprefix_ , self.gds_format_decimal(self.ChargeValue, input_name='ChargeValue'), namespaceprefix_ , eol_))
        if self.ChargeExchangeRate is not None:
            namespaceprefix_ = self.ChargeExchangeRate_nsprefix_ + ':' if (UseCapturedNS_ and self.ChargeExchangeRate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChargeExchangeRate>%s</%sChargeExchangeRate>%s' % (namespaceprefix_ , self.gds_format_decimal(self.ChargeExchangeRate, input_name='ChargeExchangeRate'), namespaceprefix_ , eol_))
        if self.ChargeTaxAmount is not None:
            namespaceprefix_ = self.ChargeTaxAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.ChargeTaxAmount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChargeTaxAmount>%s</%sChargeTaxAmount>%s' % (namespaceprefix_ , self.gds_format_decimal(self.ChargeTaxAmount, input_name='ChargeTaxAmount'), namespaceprefix_ , eol_))
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.CurrencyRoleTypeCode is not None:
            namespaceprefix_ = self.CurrencyRoleTypeCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyRoleTypeCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyRoleTypeCode>%s</%sCurrencyRoleTypeCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyRoleTypeCode), input_name='CurrencyRoleTypeCode')), namespaceprefix_ , eol_))
        for ChargeTaxAmountDet_ in self.ChargeTaxAmountDet:
            namespaceprefix_ = self.ChargeTaxAmountDet_nsprefix_ + ':' if (UseCapturedNS_ and self.ChargeTaxAmountDet_nsprefix_) else ''
            ChargeTaxAmountDet_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ChargeTaxAmountDet', pretty_print=pretty_print)
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
        if nodeName_ == 'ChargeValue' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ChargeValue')
            fval_ = self.gds_validate_decimal(fval_, node, 'ChargeValue')
            self.ChargeValue = fval_
            self.ChargeValue_nsprefix_ = child_.prefix
            # validate type ChargeValueType8
            self.validate_ChargeValueType8(self.ChargeValue)
        elif nodeName_ == 'ChargeExchangeRate' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ChargeExchangeRate')
            fval_ = self.gds_validate_decimal(fval_, node, 'ChargeExchangeRate')
            self.ChargeExchangeRate = fval_
            self.ChargeExchangeRate_nsprefix_ = child_.prefix
            # validate type ChargeExchangeRateType
            self.validate_ChargeExchangeRateType(self.ChargeExchangeRate)
        elif nodeName_ == 'ChargeTaxAmount' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ChargeTaxAmount')
            fval_ = self.gds_validate_decimal(fval_, node, 'ChargeTaxAmount')
            self.ChargeTaxAmount = fval_
            self.ChargeTaxAmount_nsprefix_ = child_.prefix
            # validate type ChargeTaxAmountType9
            self.validate_ChargeTaxAmountType9(self.ChargeTaxAmount)
        elif nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
            # validate type CurrencyCodeType10
            self.validate_CurrencyCodeType10(self.CurrencyCode)
        elif nodeName_ == 'CurrencyRoleTypeCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyRoleTypeCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyRoleTypeCode')
            self.CurrencyRoleTypeCode = value_
            self.CurrencyRoleTypeCode_nsprefix_ = child_.prefix
            # validate type CurrencyRoleTypeCodeType11
            self.validate_CurrencyRoleTypeCodeType11(self.CurrencyRoleTypeCode)
        elif nodeName_ == 'ChargeTaxAmountDet':
            obj_ = ChargeTaxAmountDetType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ChargeTaxAmountDet.append(obj_)
            obj_.original_tagname_ = 'ChargeTaxAmountDet'
# end class QtdSExtrChrgInAdCurType


class QtdShpType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, OriginServiceArea=None, DestinationServiceArea=None, GlobalProductCode=None, LocalProductCode=None, ProductShortName=None, LocalProductName=None, NetworkTypeCode=None, POfferedCustAgreement=None, TransInd=None, PickupDate=None, PickupCutoffTime=None, BookingTime=None, CurrencyCode=None, ExchangeRate=None, WeightCharge=None, WeightChargeTax=None, weightChargeTaxRate=None, TotalTransitDays=None, PickupPostalLocAddDays=None, DeliveryPostalLocAddDays=None, DeliveryDate=None, DeliveryTime=None, DeliveryTimeGMTOffset=None, DimensionalWeight=None, WeightUnit=None, PickupDayOfWeekNum=None, DestinationDayOfWeekNum=None, QuotedWeight=None, QuotedWeightUOM=None, QtdShpExChrg=None, PricingDate=None, ShippingCharge=None, TotalTaxAmount=None, TotalDiscount=None, WeightChargeTaxDet=None, PickupWindowEarliestTime=None, PickupWindowLatestTime=None, BookingCutoffOffset=None, PickupLeadTime=None, PickupCloseTime=None, WeightChargeDisc=None, QtdShpExChrgDisc=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.OriginServiceArea = OriginServiceArea
        self.OriginServiceArea_nsprefix_ = None
        self.DestinationServiceArea = DestinationServiceArea
        self.DestinationServiceArea_nsprefix_ = None
        self.GlobalProductCode = GlobalProductCode
        self.validate_GlobalProductCodeType(self.GlobalProductCode)
        self.GlobalProductCode_nsprefix_ = None
        self.LocalProductCode = LocalProductCode
        self.validate_LocalProductCodeType(self.LocalProductCode)
        self.LocalProductCode_nsprefix_ = None
        self.ProductShortName = ProductShortName
        self.ProductShortName_nsprefix_ = None
        self.LocalProductName = LocalProductName
        self.LocalProductName_nsprefix_ = None
        self.NetworkTypeCode = NetworkTypeCode
        self.NetworkTypeCode_nsprefix_ = None
        self.POfferedCustAgreement = POfferedCustAgreement
        self.POfferedCustAgreement_nsprefix_ = None
        self.TransInd = TransInd
        self.TransInd_nsprefix_ = None
        if isinstance(PickupDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(PickupDate, '%Y-%m-%d').date()
        else:
            initvalue_ = PickupDate
        self.PickupDate = initvalue_
        self.PickupDate_nsprefix_ = None
        self.PickupCutoffTime = PickupCutoffTime
        self.PickupCutoffTime_nsprefix_ = None
        self.BookingTime = BookingTime
        self.validate_BookingTimeType(self.BookingTime)
        self.BookingTime_nsprefix_ = None
        self.CurrencyCode = CurrencyCode
        self.validate_CurrencyCodeType12(self.CurrencyCode)
        self.CurrencyCode_nsprefix_ = None
        self.ExchangeRate = ExchangeRate
        self.validate_ExchangeRateType13(self.ExchangeRate)
        self.ExchangeRate_nsprefix_ = None
        self.WeightCharge = WeightCharge
        self.validate_WeightChargeType14(self.WeightCharge)
        self.WeightCharge_nsprefix_ = None
        self.WeightChargeTax = WeightChargeTax
        self.validate_WeightChargeTaxType15(self.WeightChargeTax)
        self.WeightChargeTax_nsprefix_ = None
        self.weightChargeTaxRate = weightChargeTaxRate
        self.validate_weightChargeTaxRateType(self.weightChargeTaxRate)
        self.weightChargeTaxRate_nsprefix_ = None
        self.TotalTransitDays = TotalTransitDays
        self.validate_TotalTransitDaysType(self.TotalTransitDays)
        self.TotalTransitDays_nsprefix_ = None
        self.PickupPostalLocAddDays = PickupPostalLocAddDays
        self.validate_PickupPostalLocAddDaysType(self.PickupPostalLocAddDays)
        self.PickupPostalLocAddDays_nsprefix_ = None
        self.DeliveryPostalLocAddDays = DeliveryPostalLocAddDays
        self.validate_DeliveryPostalLocAddDaysType(self.DeliveryPostalLocAddDays)
        self.DeliveryPostalLocAddDays_nsprefix_ = None
        if DeliveryDate is None:
            self.DeliveryDate = []
        else:
            self.DeliveryDate = DeliveryDate
        self.DeliveryDate_nsprefix_ = None
        self.DeliveryTime = DeliveryTime
        self.validate_DeliveryTimeType(self.DeliveryTime)
        self.DeliveryTime_nsprefix_ = None
        self.DeliveryTimeGMTOffset = DeliveryTimeGMTOffset
        self.validate_DeliveryTimeGMTOffsetType(self.DeliveryTimeGMTOffset)
        self.DeliveryTimeGMTOffset_nsprefix_ = None
        self.DimensionalWeight = DimensionalWeight
        self.validate_DimensionalWeightType(self.DimensionalWeight)
        self.DimensionalWeight_nsprefix_ = None
        self.WeightUnit = WeightUnit
        self.validate_WeightUnitType(self.WeightUnit)
        self.WeightUnit_nsprefix_ = None
        self.PickupDayOfWeekNum = PickupDayOfWeekNum
        self.validate_PickupDayOfWeekNumType(self.PickupDayOfWeekNum)
        self.PickupDayOfWeekNum_nsprefix_ = None
        self.DestinationDayOfWeekNum = DestinationDayOfWeekNum
        self.validate_DestinationDayOfWeekNumType(self.DestinationDayOfWeekNum)
        self.DestinationDayOfWeekNum_nsprefix_ = None
        self.QuotedWeight = QuotedWeight
        self.validate_QuotedWeight(self.QuotedWeight)
        self.QuotedWeight_nsprefix_ = None
        self.QuotedWeightUOM = QuotedWeightUOM
        self.validate_QuotedWeightUOM(self.QuotedWeightUOM)
        self.QuotedWeightUOM_nsprefix_ = None
        if QtdShpExChrg is None:
            self.QtdShpExChrg = []
        else:
            self.QtdShpExChrg = QtdShpExChrg
        self.QtdShpExChrg_nsprefix_ = None
        if isinstance(PricingDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(PricingDate, '%Y-%m-%d').date()
        else:
            initvalue_ = PricingDate
        self.PricingDate = initvalue_
        self.PricingDate_nsprefix_ = None
        self.ShippingCharge = ShippingCharge
        self.validate_ShippingChargeType(self.ShippingCharge)
        self.ShippingCharge_nsprefix_ = None
        self.TotalTaxAmount = TotalTaxAmount
        self.validate_TotalTaxAmountType16(self.TotalTaxAmount)
        self.TotalTaxAmount_nsprefix_ = None
        self.TotalDiscount = TotalDiscount
        self.validate_TotalDiscountType17(self.TotalDiscount)
        self.TotalDiscount_nsprefix_ = None
        if WeightChargeTaxDet is None:
            self.WeightChargeTaxDet = []
        else:
            self.WeightChargeTaxDet = WeightChargeTaxDet
        self.WeightChargeTaxDet_nsprefix_ = None
        self.PickupWindowEarliestTime = PickupWindowEarliestTime
        self.validate_PickupWindowEarliestTimeType(self.PickupWindowEarliestTime)
        self.PickupWindowEarliestTime_nsprefix_ = None
        self.PickupWindowLatestTime = PickupWindowLatestTime
        self.validate_PickupWindowLatestTimeType(self.PickupWindowLatestTime)
        self.PickupWindowLatestTime_nsprefix_ = None
        self.BookingCutoffOffset = BookingCutoffOffset
        self.validate_BookingCutoffOffsetType(self.BookingCutoffOffset)
        self.BookingCutoffOffset_nsprefix_ = None
        self.PickupLeadTime = PickupLeadTime
        self.validate_PickupLeadTimeType(self.PickupLeadTime)
        self.PickupLeadTime_nsprefix_ = None
        self.PickupCloseTime = PickupCloseTime
        self.validate_PickupCloseTimeType(self.PickupCloseTime)
        self.PickupCloseTime_nsprefix_ = None
        if WeightChargeDisc is None:
            self.WeightChargeDisc = []
        else:
            self.WeightChargeDisc = WeightChargeDisc
        self.WeightChargeDisc_nsprefix_ = None
        if QtdShpExChrgDisc is None:
            self.QtdShpExChrgDisc = []
        else:
            self.QtdShpExChrgDisc = QtdShpExChrgDisc
        self.QtdShpExChrgDisc_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, QtdShpType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if QtdShpType.subclass:
            return QtdShpType.subclass(*args_, **kwargs_)
        else:
            return QtdShpType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_OriginServiceArea(self):
        return self.OriginServiceArea
    def set_OriginServiceArea(self, OriginServiceArea):
        self.OriginServiceArea = OriginServiceArea
    def get_DestinationServiceArea(self):
        return self.DestinationServiceArea
    def set_DestinationServiceArea(self, DestinationServiceArea):
        self.DestinationServiceArea = DestinationServiceArea
    def get_GlobalProductCode(self):
        return self.GlobalProductCode
    def set_GlobalProductCode(self, GlobalProductCode):
        self.GlobalProductCode = GlobalProductCode
    def get_LocalProductCode(self):
        return self.LocalProductCode
    def set_LocalProductCode(self, LocalProductCode):
        self.LocalProductCode = LocalProductCode
    def get_ProductShortName(self):
        return self.ProductShortName
    def set_ProductShortName(self, ProductShortName):
        self.ProductShortName = ProductShortName
    def get_LocalProductName(self):
        return self.LocalProductName
    def set_LocalProductName(self, LocalProductName):
        self.LocalProductName = LocalProductName
    def get_NetworkTypeCode(self):
        return self.NetworkTypeCode
    def set_NetworkTypeCode(self, NetworkTypeCode):
        self.NetworkTypeCode = NetworkTypeCode
    def get_POfferedCustAgreement(self):
        return self.POfferedCustAgreement
    def set_POfferedCustAgreement(self, POfferedCustAgreement):
        self.POfferedCustAgreement = POfferedCustAgreement
    def get_TransInd(self):
        return self.TransInd
    def set_TransInd(self, TransInd):
        self.TransInd = TransInd
    def get_PickupDate(self):
        return self.PickupDate
    def set_PickupDate(self, PickupDate):
        self.PickupDate = PickupDate
    def get_PickupCutoffTime(self):
        return self.PickupCutoffTime
    def set_PickupCutoffTime(self, PickupCutoffTime):
        self.PickupCutoffTime = PickupCutoffTime
    def get_BookingTime(self):
        return self.BookingTime
    def set_BookingTime(self, BookingTime):
        self.BookingTime = BookingTime
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_ExchangeRate(self):
        return self.ExchangeRate
    def set_ExchangeRate(self, ExchangeRate):
        self.ExchangeRate = ExchangeRate
    def get_WeightCharge(self):
        return self.WeightCharge
    def set_WeightCharge(self, WeightCharge):
        self.WeightCharge = WeightCharge
    def get_WeightChargeTax(self):
        return self.WeightChargeTax
    def set_WeightChargeTax(self, WeightChargeTax):
        self.WeightChargeTax = WeightChargeTax
    def get_weightChargeTaxRate(self):
        return self.weightChargeTaxRate
    def set_weightChargeTaxRate(self, weightChargeTaxRate):
        self.weightChargeTaxRate = weightChargeTaxRate
    def get_TotalTransitDays(self):
        return self.TotalTransitDays
    def set_TotalTransitDays(self, TotalTransitDays):
        self.TotalTransitDays = TotalTransitDays
    def get_PickupPostalLocAddDays(self):
        return self.PickupPostalLocAddDays
    def set_PickupPostalLocAddDays(self, PickupPostalLocAddDays):
        self.PickupPostalLocAddDays = PickupPostalLocAddDays
    def get_DeliveryPostalLocAddDays(self):
        return self.DeliveryPostalLocAddDays
    def set_DeliveryPostalLocAddDays(self, DeliveryPostalLocAddDays):
        self.DeliveryPostalLocAddDays = DeliveryPostalLocAddDays
    def get_DeliveryDate(self):
        return self.DeliveryDate
    def set_DeliveryDate(self, DeliveryDate):
        self.DeliveryDate = DeliveryDate
    def add_DeliveryDate(self, value):
        self.DeliveryDate.append(value)
    def insert_DeliveryDate_at(self, index, value):
        self.DeliveryDate.insert(index, value)
    def replace_DeliveryDate_at(self, index, value):
        self.DeliveryDate[index] = value
    def get_DeliveryTime(self):
        return self.DeliveryTime
    def set_DeliveryTime(self, DeliveryTime):
        self.DeliveryTime = DeliveryTime
    def get_DeliveryTimeGMTOffset(self):
        return self.DeliveryTimeGMTOffset
    def set_DeliveryTimeGMTOffset(self, DeliveryTimeGMTOffset):
        self.DeliveryTimeGMTOffset = DeliveryTimeGMTOffset
    def get_DimensionalWeight(self):
        return self.DimensionalWeight
    def set_DimensionalWeight(self, DimensionalWeight):
        self.DimensionalWeight = DimensionalWeight
    def get_WeightUnit(self):
        return self.WeightUnit
    def set_WeightUnit(self, WeightUnit):
        self.WeightUnit = WeightUnit
    def get_PickupDayOfWeekNum(self):
        return self.PickupDayOfWeekNum
    def set_PickupDayOfWeekNum(self, PickupDayOfWeekNum):
        self.PickupDayOfWeekNum = PickupDayOfWeekNum
    def get_DestinationDayOfWeekNum(self):
        return self.DestinationDayOfWeekNum
    def set_DestinationDayOfWeekNum(self, DestinationDayOfWeekNum):
        self.DestinationDayOfWeekNum = DestinationDayOfWeekNum
    def get_QuotedWeight(self):
        return self.QuotedWeight
    def set_QuotedWeight(self, QuotedWeight):
        self.QuotedWeight = QuotedWeight
    def get_QuotedWeightUOM(self):
        return self.QuotedWeightUOM
    def set_QuotedWeightUOM(self, QuotedWeightUOM):
        self.QuotedWeightUOM = QuotedWeightUOM
    def get_QtdShpExChrg(self):
        return self.QtdShpExChrg
    def set_QtdShpExChrg(self, QtdShpExChrg):
        self.QtdShpExChrg = QtdShpExChrg
    def add_QtdShpExChrg(self, value):
        self.QtdShpExChrg.append(value)
    def insert_QtdShpExChrg_at(self, index, value):
        self.QtdShpExChrg.insert(index, value)
    def replace_QtdShpExChrg_at(self, index, value):
        self.QtdShpExChrg[index] = value
    def get_PricingDate(self):
        return self.PricingDate
    def set_PricingDate(self, PricingDate):
        self.PricingDate = PricingDate
    def get_ShippingCharge(self):
        return self.ShippingCharge
    def set_ShippingCharge(self, ShippingCharge):
        self.ShippingCharge = ShippingCharge
    def get_TotalTaxAmount(self):
        return self.TotalTaxAmount
    def set_TotalTaxAmount(self, TotalTaxAmount):
        self.TotalTaxAmount = TotalTaxAmount
    def get_TotalDiscount(self):
        return self.TotalDiscount
    def set_TotalDiscount(self, TotalDiscount):
        self.TotalDiscount = TotalDiscount
    def get_WeightChargeTaxDet(self):
        return self.WeightChargeTaxDet
    def set_WeightChargeTaxDet(self, WeightChargeTaxDet):
        self.WeightChargeTaxDet = WeightChargeTaxDet
    def add_WeightChargeTaxDet(self, value):
        self.WeightChargeTaxDet.append(value)
    def insert_WeightChargeTaxDet_at(self, index, value):
        self.WeightChargeTaxDet.insert(index, value)
    def replace_WeightChargeTaxDet_at(self, index, value):
        self.WeightChargeTaxDet[index] = value
    def get_PickupWindowEarliestTime(self):
        return self.PickupWindowEarliestTime
    def set_PickupWindowEarliestTime(self, PickupWindowEarliestTime):
        self.PickupWindowEarliestTime = PickupWindowEarliestTime
    def get_PickupWindowLatestTime(self):
        return self.PickupWindowLatestTime
    def set_PickupWindowLatestTime(self, PickupWindowLatestTime):
        self.PickupWindowLatestTime = PickupWindowLatestTime
    def get_BookingCutoffOffset(self):
        return self.BookingCutoffOffset
    def set_BookingCutoffOffset(self, BookingCutoffOffset):
        self.BookingCutoffOffset = BookingCutoffOffset
    def get_PickupLeadTime(self):
        return self.PickupLeadTime
    def set_PickupLeadTime(self, PickupLeadTime):
        self.PickupLeadTime = PickupLeadTime
    def get_PickupCloseTime(self):
        return self.PickupCloseTime
    def set_PickupCloseTime(self, PickupCloseTime):
        self.PickupCloseTime = PickupCloseTime
    def get_WeightChargeDisc(self):
        return self.WeightChargeDisc
    def set_WeightChargeDisc(self, WeightChargeDisc):
        self.WeightChargeDisc = WeightChargeDisc
    def add_WeightChargeDisc(self, value):
        self.WeightChargeDisc.append(value)
    def insert_WeightChargeDisc_at(self, index, value):
        self.WeightChargeDisc.insert(index, value)
    def replace_WeightChargeDisc_at(self, index, value):
        self.WeightChargeDisc[index] = value
    def get_QtdShpExChrgDisc(self):
        return self.QtdShpExChrgDisc
    def set_QtdShpExChrgDisc(self, QtdShpExChrgDisc):
        self.QtdShpExChrgDisc = QtdShpExChrgDisc
    def add_QtdShpExChrgDisc(self, value):
        self.QtdShpExChrgDisc.append(value)
    def insert_QtdShpExChrgDisc_at(self, index, value):
        self.QtdShpExChrgDisc.insert(index, value)
    def replace_QtdShpExChrgDisc_at(self, index, value):
        self.QtdShpExChrgDisc[index] = value
    def validate_GlobalProductCodeType(self, value):
        result = True
        # Validate type GlobalProductCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on GlobalProductCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_LocalProductCodeType(self, value):
        result = True
        # Validate type LocalProductCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on LocalProductCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PickupDateType(self, value):
        result = True
        # Validate type PickupDateType, a restriction on xsd:date.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.date):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.date)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_BookingTimeType(self, value):
        result = True
        # Validate type BookingTimeType, a restriction on xsd:duration.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_CurrencyCodeType12(self, value):
        result = True
        # Validate type CurrencyCodeType12, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CurrencyCodeType12' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ExchangeRateType13(self, value):
        result = True
        # Validate type ExchangeRateType13, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on ExchangeRateType13' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_WeightChargeType14(self, value):
        result = True
        # Validate type WeightChargeType14, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on WeightChargeType14' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_WeightChargeTaxType15(self, value):
        result = True
        # Validate type WeightChargeTaxType15, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on WeightChargeTaxType15' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_weightChargeTaxRateType(self, value):
        result = True
        # Validate type weightChargeTaxRateType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on weightChargeTaxRateType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_TotalTransitDaysType(self, value):
        result = True
        # Validate type TotalTransitDaysType, a restriction on xsd:int.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_PickupPostalLocAddDaysType(self, value):
        result = True
        # Validate type PickupPostalLocAddDaysType, a restriction on xsd:int.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_DeliveryPostalLocAddDaysType(self, value):
        result = True
        # Validate type DeliveryPostalLocAddDaysType, a restriction on xsd:int.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, int):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (int)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_DeliveryTimeType(self, value):
        result = True
        # Validate type DeliveryTimeType, a restriction on xsd:duration.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_DeliveryTimeGMTOffsetType(self, value):
        result = True
        # Validate type DeliveryTimeGMTOffsetType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on DeliveryTimeGMTOffsetType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DimensionalWeightType(self, value):
        result = True
        # Validate type DimensionalWeightType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 15:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on DimensionalWeightType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_WeightUnitType(self, value):
        result = True
        # Validate type WeightUnitType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on WeightUnitType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PickupDayOfWeekNumType(self, value):
        result = True
        # Validate type PickupDayOfWeekNumType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on PickupDayOfWeekNumType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DestinationDayOfWeekNumType(self, value):
        result = True
        # Validate type DestinationDayOfWeekNumType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on DestinationDayOfWeekNumType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_QuotedWeight(self, value):
        result = True
        # Validate type QuotedWeight, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if value < 0.000:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on QuotedWeight' % {"value": value, "lineno": lineno} )
                result = False
            if value > 999999.999:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on QuotedWeight' % {"value": value, "lineno": lineno} )
                result = False
            if len(str(value)) >= 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on QuotedWeight' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_QuotedWeightUOM(self, value):
        result = True
        # Validate type QuotedWeightUOM, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['KG', 'Lbs']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on QuotedWeightUOM' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on QuotedWeightUOM' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on QuotedWeightUOM' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PricingDateType(self, value):
        result = True
        # Validate type PricingDateType, a restriction on xsd:date.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, datetime_.date):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (datetime_.date)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_ShippingChargeType(self, value):
        result = True
        # Validate type ShippingChargeType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on ShippingChargeType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_TotalTaxAmountType16(self, value):
        result = True
        # Validate type TotalTaxAmountType16, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on TotalTaxAmountType16' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_TotalDiscountType17(self, value):
        result = True
        # Validate type TotalDiscountType17, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on TotalDiscountType17' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_PickupWindowEarliestTimeType(self, value):
        result = True
        # Validate type PickupWindowEarliestTimeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_PickupWindowLatestTimeType(self, value):
        result = True
        # Validate type PickupWindowLatestTimeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_BookingCutoffOffsetType(self, value):
        result = True
        # Validate type BookingCutoffOffsetType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_PickupLeadTimeType(self, value):
        result = True
        # Validate type PickupLeadTimeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on PickupLeadTimeType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PickupCloseTimeType(self, value):
        result = True
        # Validate type PickupCloseTimeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on PickupCloseTimeType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.OriginServiceArea is not None or
            self.DestinationServiceArea is not None or
            self.GlobalProductCode is not None or
            self.LocalProductCode is not None or
            self.ProductShortName is not None or
            self.LocalProductName is not None or
            self.NetworkTypeCode is not None or
            self.POfferedCustAgreement is not None or
            self.TransInd is not None or
            self.PickupDate is not None or
            self.PickupCutoffTime is not None or
            self.BookingTime is not None or
            self.CurrencyCode is not None or
            self.ExchangeRate is not None or
            self.WeightCharge is not None or
            self.WeightChargeTax is not None or
            self.weightChargeTaxRate is not None or
            self.TotalTransitDays is not None or
            self.PickupPostalLocAddDays is not None or
            self.DeliveryPostalLocAddDays is not None or
            self.DeliveryDate or
            self.DeliveryTime is not None or
            self.DeliveryTimeGMTOffset is not None or
            self.DimensionalWeight is not None or
            self.WeightUnit is not None or
            self.PickupDayOfWeekNum is not None or
            self.DestinationDayOfWeekNum is not None or
            self.QuotedWeight is not None or
            self.QuotedWeightUOM is not None or
            self.QtdShpExChrg or
            self.PricingDate is not None or
            self.ShippingCharge is not None or
            self.TotalTaxAmount is not None or
            self.TotalDiscount is not None or
            self.WeightChargeTaxDet or
            self.PickupWindowEarliestTime is not None or
            self.PickupWindowLatestTime is not None or
            self.BookingCutoffOffset is not None or
            self.PickupLeadTime is not None or
            self.PickupCloseTime is not None or
            self.WeightChargeDisc or
            self.QtdShpExChrgDisc
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='QtdShpType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('QtdShpType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'QtdShpType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='QtdShpType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='QtdShpType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='QtdShpType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='QtdShpType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.OriginServiceArea is not None:
            namespaceprefix_ = self.OriginServiceArea_nsprefix_ + ':' if (UseCapturedNS_ and self.OriginServiceArea_nsprefix_) else ''
            self.OriginServiceArea.export(outfile, level, namespaceprefix_, namespacedef_='', name_='OriginServiceArea', pretty_print=pretty_print)
        if self.DestinationServiceArea is not None:
            namespaceprefix_ = self.DestinationServiceArea_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationServiceArea_nsprefix_) else ''
            self.DestinationServiceArea.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DestinationServiceArea', pretty_print=pretty_print)
        if self.GlobalProductCode is not None:
            namespaceprefix_ = self.GlobalProductCode_nsprefix_ + ':' if (UseCapturedNS_ and self.GlobalProductCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGlobalProductCode>%s</%sGlobalProductCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GlobalProductCode), input_name='GlobalProductCode')), namespaceprefix_ , eol_))
        if self.LocalProductCode is not None:
            namespaceprefix_ = self.LocalProductCode_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalProductCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalProductCode>%s</%sLocalProductCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalProductCode), input_name='LocalProductCode')), namespaceprefix_ , eol_))
        if self.ProductShortName is not None:
            namespaceprefix_ = self.ProductShortName_nsprefix_ + ':' if (UseCapturedNS_ and self.ProductShortName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProductShortName>%s</%sProductShortName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ProductShortName), input_name='ProductShortName')), namespaceprefix_ , eol_))
        if self.LocalProductName is not None:
            namespaceprefix_ = self.LocalProductName_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalProductName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalProductName>%s</%sLocalProductName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalProductName), input_name='LocalProductName')), namespaceprefix_ , eol_))
        if self.NetworkTypeCode is not None:
            namespaceprefix_ = self.NetworkTypeCode_nsprefix_ + ':' if (UseCapturedNS_ and self.NetworkTypeCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNetworkTypeCode>%s</%sNetworkTypeCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NetworkTypeCode), input_name='NetworkTypeCode')), namespaceprefix_ , eol_))
        if self.POfferedCustAgreement is not None:
            namespaceprefix_ = self.POfferedCustAgreement_nsprefix_ + ':' if (UseCapturedNS_ and self.POfferedCustAgreement_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPOfferedCustAgreement>%s</%sPOfferedCustAgreement>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.POfferedCustAgreement), input_name='POfferedCustAgreement')), namespaceprefix_ , eol_))
        if self.TransInd is not None:
            namespaceprefix_ = self.TransInd_nsprefix_ + ':' if (UseCapturedNS_ and self.TransInd_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTransInd>%s</%sTransInd>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TransInd), input_name='TransInd')), namespaceprefix_ , eol_))
        if self.PickupDate is not None:
            namespaceprefix_ = self.PickupDate_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupDate>%s</%sPickupDate>%s' % (namespaceprefix_ , self.gds_format_date(self.PickupDate, input_name='PickupDate'), namespaceprefix_ , eol_))
        if self.PickupCutoffTime is not None:
            namespaceprefix_ = self.PickupCutoffTime_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupCutoffTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupCutoffTime>%s</%sPickupCutoffTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupCutoffTime), input_name='PickupCutoffTime')), namespaceprefix_ , eol_))
        if self.BookingTime is not None:
            namespaceprefix_ = self.BookingTime_nsprefix_ + ':' if (UseCapturedNS_ and self.BookingTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBookingTime>%s</%sBookingTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BookingTime), input_name='BookingTime')), namespaceprefix_ , eol_))
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.ExchangeRate is not None:
            namespaceprefix_ = self.ExchangeRate_nsprefix_ + ':' if (UseCapturedNS_ and self.ExchangeRate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExchangeRate>%s</%sExchangeRate>%s' % (namespaceprefix_ , self.gds_format_decimal(self.ExchangeRate, input_name='ExchangeRate'), namespaceprefix_ , eol_))
        if self.WeightCharge is not None:
            namespaceprefix_ = self.WeightCharge_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightCharge_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeightCharge>%s</%sWeightCharge>%s' % (namespaceprefix_ , self.gds_format_decimal(self.WeightCharge, input_name='WeightCharge'), namespaceprefix_ , eol_))
        if self.WeightChargeTax is not None:
            namespaceprefix_ = self.WeightChargeTax_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightChargeTax_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeightChargeTax>%s</%sWeightChargeTax>%s' % (namespaceprefix_ , self.gds_format_decimal(self.WeightChargeTax, input_name='WeightChargeTax'), namespaceprefix_ , eol_))
        if self.weightChargeTaxRate is not None:
            namespaceprefix_ = self.weightChargeTaxRate_nsprefix_ + ':' if (UseCapturedNS_ and self.weightChargeTaxRate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sweightChargeTaxRate>%s</%sweightChargeTaxRate>%s' % (namespaceprefix_ , self.gds_format_decimal(self.weightChargeTaxRate, input_name='weightChargeTaxRate'), namespaceprefix_ , eol_))
        if self.TotalTransitDays is not None:
            namespaceprefix_ = self.TotalTransitDays_nsprefix_ + ':' if (UseCapturedNS_ and self.TotalTransitDays_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTotalTransitDays>%s</%sTotalTransitDays>%s' % (namespaceprefix_ , self.gds_format_integer(self.TotalTransitDays, input_name='TotalTransitDays'), namespaceprefix_ , eol_))
        if self.PickupPostalLocAddDays is not None:
            namespaceprefix_ = self.PickupPostalLocAddDays_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupPostalLocAddDays_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupPostalLocAddDays>%s</%sPickupPostalLocAddDays>%s' % (namespaceprefix_ , self.gds_format_integer(self.PickupPostalLocAddDays, input_name='PickupPostalLocAddDays'), namespaceprefix_ , eol_))
        if self.DeliveryPostalLocAddDays is not None:
            namespaceprefix_ = self.DeliveryPostalLocAddDays_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryPostalLocAddDays_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeliveryPostalLocAddDays>%s</%sDeliveryPostalLocAddDays>%s' % (namespaceprefix_ , self.gds_format_integer(self.DeliveryPostalLocAddDays, input_name='DeliveryPostalLocAddDays'), namespaceprefix_ , eol_))
        for DeliveryDate_ in self.DeliveryDate:
            namespaceprefix_ = self.DeliveryDate_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryDate_nsprefix_) else ''
            DeliveryDate_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DeliveryDate', pretty_print=pretty_print)
        if self.DeliveryTime is not None:
            namespaceprefix_ = self.DeliveryTime_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeliveryTime>%s</%sDeliveryTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DeliveryTime), input_name='DeliveryTime')), namespaceprefix_ , eol_))
        if self.DeliveryTimeGMTOffset is not None:
            namespaceprefix_ = self.DeliveryTimeGMTOffset_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryTimeGMTOffset_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeliveryTimeGMTOffset>%s</%sDeliveryTimeGMTOffset>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DeliveryTimeGMTOffset), input_name='DeliveryTimeGMTOffset')), namespaceprefix_ , eol_))
        if self.DimensionalWeight is not None:
            namespaceprefix_ = self.DimensionalWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.DimensionalWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDimensionalWeight>%s</%sDimensionalWeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.DimensionalWeight, input_name='DimensionalWeight'), namespaceprefix_ , eol_))
        if self.WeightUnit is not None:
            namespaceprefix_ = self.WeightUnit_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightUnit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeightUnit>%s</%sWeightUnit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WeightUnit), input_name='WeightUnit')), namespaceprefix_ , eol_))
        if self.PickupDayOfWeekNum is not None:
            namespaceprefix_ = self.PickupDayOfWeekNum_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupDayOfWeekNum_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupDayOfWeekNum>%s</%sPickupDayOfWeekNum>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupDayOfWeekNum), input_name='PickupDayOfWeekNum')), namespaceprefix_ , eol_))
        if self.DestinationDayOfWeekNum is not None:
            namespaceprefix_ = self.DestinationDayOfWeekNum_nsprefix_ + ':' if (UseCapturedNS_ and self.DestinationDayOfWeekNum_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDestinationDayOfWeekNum>%s</%sDestinationDayOfWeekNum>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DestinationDayOfWeekNum), input_name='DestinationDayOfWeekNum')), namespaceprefix_ , eol_))
        if self.QuotedWeight is not None:
            namespaceprefix_ = self.QuotedWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.QuotedWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sQuotedWeight>%s</%sQuotedWeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.QuotedWeight, input_name='QuotedWeight'), namespaceprefix_ , eol_))
        if self.QuotedWeightUOM is not None:
            namespaceprefix_ = self.QuotedWeightUOM_nsprefix_ + ':' if (UseCapturedNS_ and self.QuotedWeightUOM_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sQuotedWeightUOM>%s</%sQuotedWeightUOM>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.QuotedWeightUOM), input_name='QuotedWeightUOM')), namespaceprefix_ , eol_))
        for QtdShpExChrg_ in self.QtdShpExChrg:
            namespaceprefix_ = self.QtdShpExChrg_nsprefix_ + ':' if (UseCapturedNS_ and self.QtdShpExChrg_nsprefix_) else ''
            QtdShpExChrg_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='QtdShpExChrg', pretty_print=pretty_print)
        if self.PricingDate is not None:
            namespaceprefix_ = self.PricingDate_nsprefix_ + ':' if (UseCapturedNS_ and self.PricingDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPricingDate>%s</%sPricingDate>%s' % (namespaceprefix_ , self.gds_format_date(self.PricingDate, input_name='PricingDate'), namespaceprefix_ , eol_))
        if self.ShippingCharge is not None:
            namespaceprefix_ = self.ShippingCharge_nsprefix_ + ':' if (UseCapturedNS_ and self.ShippingCharge_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShippingCharge>%s</%sShippingCharge>%s' % (namespaceprefix_ , self.gds_format_decimal(self.ShippingCharge, input_name='ShippingCharge'), namespaceprefix_ , eol_))
        if self.TotalTaxAmount is not None:
            namespaceprefix_ = self.TotalTaxAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.TotalTaxAmount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTotalTaxAmount>%s</%sTotalTaxAmount>%s' % (namespaceprefix_ , self.gds_format_decimal(self.TotalTaxAmount, input_name='TotalTaxAmount'), namespaceprefix_ , eol_))
        if self.TotalDiscount is not None:
            namespaceprefix_ = self.TotalDiscount_nsprefix_ + ':' if (UseCapturedNS_ and self.TotalDiscount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTotalDiscount>%s</%sTotalDiscount>%s' % (namespaceprefix_ , self.gds_format_decimal(self.TotalDiscount, input_name='TotalDiscount'), namespaceprefix_ , eol_))
        for WeightChargeTaxDet_ in self.WeightChargeTaxDet:
            namespaceprefix_ = self.WeightChargeTaxDet_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightChargeTaxDet_nsprefix_) else ''
            WeightChargeTaxDet_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='WeightChargeTaxDet', pretty_print=pretty_print)
        if self.PickupWindowEarliestTime is not None:
            namespaceprefix_ = self.PickupWindowEarliestTime_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupWindowEarliestTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupWindowEarliestTime>%s</%sPickupWindowEarliestTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupWindowEarliestTime), input_name='PickupWindowEarliestTime')), namespaceprefix_ , eol_))
        if self.PickupWindowLatestTime is not None:
            namespaceprefix_ = self.PickupWindowLatestTime_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupWindowLatestTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupWindowLatestTime>%s</%sPickupWindowLatestTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupWindowLatestTime), input_name='PickupWindowLatestTime')), namespaceprefix_ , eol_))
        if self.BookingCutoffOffset is not None:
            namespaceprefix_ = self.BookingCutoffOffset_nsprefix_ + ':' if (UseCapturedNS_ and self.BookingCutoffOffset_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBookingCutoffOffset>%s</%sBookingCutoffOffset>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BookingCutoffOffset), input_name='BookingCutoffOffset')), namespaceprefix_ , eol_))
        if self.PickupLeadTime is not None:
            namespaceprefix_ = self.PickupLeadTime_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupLeadTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupLeadTime>%s</%sPickupLeadTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupLeadTime), input_name='PickupLeadTime')), namespaceprefix_ , eol_))
        if self.PickupCloseTime is not None:
            namespaceprefix_ = self.PickupCloseTime_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupCloseTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupCloseTime>%s</%sPickupCloseTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupCloseTime), input_name='PickupCloseTime')), namespaceprefix_ , eol_))
        for WeightChargeDisc_ in self.WeightChargeDisc:
            namespaceprefix_ = self.WeightChargeDisc_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightChargeDisc_nsprefix_) else ''
            WeightChargeDisc_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='WeightChargeDisc', pretty_print=pretty_print)
        for QtdShpExChrgDisc_ in self.QtdShpExChrgDisc:
            namespaceprefix_ = self.QtdShpExChrgDisc_nsprefix_ + ':' if (UseCapturedNS_ and self.QtdShpExChrgDisc_nsprefix_) else ''
            QtdShpExChrgDisc_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='QtdShpExChrgDisc', pretty_print=pretty_print)
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
        if nodeName_ == 'OriginServiceArea':
            obj_ = OrgnSvcAreaType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.OriginServiceArea = obj_
            obj_.original_tagname_ = 'OriginServiceArea'
        elif nodeName_ == 'DestinationServiceArea':
            obj_ = DestSvcAreaType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DestinationServiceArea = obj_
            obj_.original_tagname_ = 'DestinationServiceArea'
        elif nodeName_ == 'GlobalProductCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GlobalProductCode')
            value_ = self.gds_validate_string(value_, node, 'GlobalProductCode')
            self.GlobalProductCode = value_
            self.GlobalProductCode_nsprefix_ = child_.prefix
            # validate type GlobalProductCodeType
            self.validate_GlobalProductCodeType(self.GlobalProductCode)
        elif nodeName_ == 'LocalProductCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalProductCode')
            value_ = self.gds_validate_string(value_, node, 'LocalProductCode')
            self.LocalProductCode = value_
            self.LocalProductCode_nsprefix_ = child_.prefix
            # validate type LocalProductCodeType
            self.validate_LocalProductCodeType(self.LocalProductCode)
        elif nodeName_ == 'ProductShortName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ProductShortName')
            value_ = self.gds_validate_string(value_, node, 'ProductShortName')
            self.ProductShortName = value_
            self.ProductShortName_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocalProductName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalProductName')
            value_ = self.gds_validate_string(value_, node, 'LocalProductName')
            self.LocalProductName = value_
            self.LocalProductName_nsprefix_ = child_.prefix
        elif nodeName_ == 'NetworkTypeCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NetworkTypeCode')
            value_ = self.gds_validate_string(value_, node, 'NetworkTypeCode')
            self.NetworkTypeCode = value_
            self.NetworkTypeCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'POfferedCustAgreement':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'POfferedCustAgreement')
            value_ = self.gds_validate_string(value_, node, 'POfferedCustAgreement')
            self.POfferedCustAgreement = value_
            self.POfferedCustAgreement_nsprefix_ = child_.prefix
        elif nodeName_ == 'TransInd':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TransInd')
            value_ = self.gds_validate_string(value_, node, 'TransInd')
            self.TransInd = value_
            self.TransInd_nsprefix_ = child_.prefix
        elif nodeName_ == 'PickupDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.PickupDate = dval_
            self.PickupDate_nsprefix_ = child_.prefix
            # validate type PickupDateType
            self.validate_PickupDateType(self.PickupDate)
        elif nodeName_ == 'PickupCutoffTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupCutoffTime')
            value_ = self.gds_validate_string(value_, node, 'PickupCutoffTime')
            self.PickupCutoffTime = value_
            self.PickupCutoffTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'BookingTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BookingTime')
            value_ = self.gds_validate_string(value_, node, 'BookingTime')
            self.BookingTime = value_
            self.BookingTime_nsprefix_ = child_.prefix
            # validate type BookingTimeType
            self.validate_BookingTimeType(self.BookingTime)
        elif nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
            # validate type CurrencyCodeType12
            self.validate_CurrencyCodeType12(self.CurrencyCode)
        elif nodeName_ == 'ExchangeRate' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ExchangeRate')
            fval_ = self.gds_validate_decimal(fval_, node, 'ExchangeRate')
            self.ExchangeRate = fval_
            self.ExchangeRate_nsprefix_ = child_.prefix
            # validate type ExchangeRateType13
            self.validate_ExchangeRateType13(self.ExchangeRate)
        elif nodeName_ == 'WeightCharge' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'WeightCharge')
            fval_ = self.gds_validate_decimal(fval_, node, 'WeightCharge')
            self.WeightCharge = fval_
            self.WeightCharge_nsprefix_ = child_.prefix
            # validate type WeightChargeType14
            self.validate_WeightChargeType14(self.WeightCharge)
        elif nodeName_ == 'WeightChargeTax' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'WeightChargeTax')
            fval_ = self.gds_validate_decimal(fval_, node, 'WeightChargeTax')
            self.WeightChargeTax = fval_
            self.WeightChargeTax_nsprefix_ = child_.prefix
            # validate type WeightChargeTaxType15
            self.validate_WeightChargeTaxType15(self.WeightChargeTax)
        elif nodeName_ == 'weightChargeTaxRate' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'weightChargeTaxRate')
            fval_ = self.gds_validate_decimal(fval_, node, 'weightChargeTaxRate')
            self.weightChargeTaxRate = fval_
            self.weightChargeTaxRate_nsprefix_ = child_.prefix
            # validate type weightChargeTaxRateType
            self.validate_weightChargeTaxRateType(self.weightChargeTaxRate)
        elif nodeName_ == 'TotalTransitDays' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'TotalTransitDays')
            ival_ = self.gds_validate_integer(ival_, node, 'TotalTransitDays')
            self.TotalTransitDays = ival_
            self.TotalTransitDays_nsprefix_ = child_.prefix
            # validate type TotalTransitDaysType
            self.validate_TotalTransitDaysType(self.TotalTransitDays)
        elif nodeName_ == 'PickupPostalLocAddDays' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'PickupPostalLocAddDays')
            ival_ = self.gds_validate_integer(ival_, node, 'PickupPostalLocAddDays')
            self.PickupPostalLocAddDays = ival_
            self.PickupPostalLocAddDays_nsprefix_ = child_.prefix
            # validate type PickupPostalLocAddDaysType
            self.validate_PickupPostalLocAddDaysType(self.PickupPostalLocAddDays)
        elif nodeName_ == 'DeliveryPostalLocAddDays' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'DeliveryPostalLocAddDays')
            ival_ = self.gds_validate_integer(ival_, node, 'DeliveryPostalLocAddDays')
            self.DeliveryPostalLocAddDays = ival_
            self.DeliveryPostalLocAddDays_nsprefix_ = child_.prefix
            # validate type DeliveryPostalLocAddDaysType
            self.validate_DeliveryPostalLocAddDaysType(self.DeliveryPostalLocAddDays)
        elif nodeName_ == 'DeliveryDate':
            obj_ = DeliveryDate.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DeliveryDate.append(obj_)
            obj_.original_tagname_ = 'DeliveryDate'
        elif nodeName_ == 'DeliveryTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DeliveryTime')
            value_ = self.gds_validate_string(value_, node, 'DeliveryTime')
            self.DeliveryTime = value_
            self.DeliveryTime_nsprefix_ = child_.prefix
            # validate type DeliveryTimeType
            self.validate_DeliveryTimeType(self.DeliveryTime)
        elif nodeName_ == 'DeliveryTimeGMTOffset':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DeliveryTimeGMTOffset')
            value_ = self.gds_validate_string(value_, node, 'DeliveryTimeGMTOffset')
            self.DeliveryTimeGMTOffset = value_
            self.DeliveryTimeGMTOffset_nsprefix_ = child_.prefix
            # validate type DeliveryTimeGMTOffsetType
            self.validate_DeliveryTimeGMTOffsetType(self.DeliveryTimeGMTOffset)
        elif nodeName_ == 'DimensionalWeight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'DimensionalWeight')
            fval_ = self.gds_validate_decimal(fval_, node, 'DimensionalWeight')
            self.DimensionalWeight = fval_
            self.DimensionalWeight_nsprefix_ = child_.prefix
            # validate type DimensionalWeightType
            self.validate_DimensionalWeightType(self.DimensionalWeight)
        elif nodeName_ == 'WeightUnit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WeightUnit')
            value_ = self.gds_validate_string(value_, node, 'WeightUnit')
            self.WeightUnit = value_
            self.WeightUnit_nsprefix_ = child_.prefix
            # validate type WeightUnitType
            self.validate_WeightUnitType(self.WeightUnit)
        elif nodeName_ == 'PickupDayOfWeekNum':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupDayOfWeekNum')
            value_ = self.gds_validate_string(value_, node, 'PickupDayOfWeekNum')
            self.PickupDayOfWeekNum = value_
            self.PickupDayOfWeekNum_nsprefix_ = child_.prefix
            # validate type PickupDayOfWeekNumType
            self.validate_PickupDayOfWeekNumType(self.PickupDayOfWeekNum)
        elif nodeName_ == 'DestinationDayOfWeekNum':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DestinationDayOfWeekNum')
            value_ = self.gds_validate_string(value_, node, 'DestinationDayOfWeekNum')
            self.DestinationDayOfWeekNum = value_
            self.DestinationDayOfWeekNum_nsprefix_ = child_.prefix
            # validate type DestinationDayOfWeekNumType
            self.validate_DestinationDayOfWeekNumType(self.DestinationDayOfWeekNum)
        elif nodeName_ == 'QuotedWeight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'QuotedWeight')
            fval_ = self.gds_validate_decimal(fval_, node, 'QuotedWeight')
            self.QuotedWeight = fval_
            self.QuotedWeight_nsprefix_ = child_.prefix
            # validate type QuotedWeight
            self.validate_QuotedWeight(self.QuotedWeight)
        elif nodeName_ == 'QuotedWeightUOM':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'QuotedWeightUOM')
            value_ = self.gds_validate_string(value_, node, 'QuotedWeightUOM')
            self.QuotedWeightUOM = value_
            self.QuotedWeightUOM_nsprefix_ = child_.prefix
            # validate type QuotedWeightUOM
            self.validate_QuotedWeightUOM(self.QuotedWeightUOM)
        elif nodeName_ == 'QtdShpExChrg':
            obj_ = QtdShpExChrgType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.QtdShpExChrg.append(obj_)
            obj_.original_tagname_ = 'QtdShpExChrg'
        elif nodeName_ == 'PricingDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.PricingDate = dval_
            self.PricingDate_nsprefix_ = child_.prefix
            # validate type PricingDateType
            self.validate_PricingDateType(self.PricingDate)
        elif nodeName_ == 'ShippingCharge' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'ShippingCharge')
            fval_ = self.gds_validate_decimal(fval_, node, 'ShippingCharge')
            self.ShippingCharge = fval_
            self.ShippingCharge_nsprefix_ = child_.prefix
            # validate type ShippingChargeType
            self.validate_ShippingChargeType(self.ShippingCharge)
        elif nodeName_ == 'TotalTaxAmount' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'TotalTaxAmount')
            fval_ = self.gds_validate_decimal(fval_, node, 'TotalTaxAmount')
            self.TotalTaxAmount = fval_
            self.TotalTaxAmount_nsprefix_ = child_.prefix
            # validate type TotalTaxAmountType16
            self.validate_TotalTaxAmountType16(self.TotalTaxAmount)
        elif nodeName_ == 'TotalDiscount' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'TotalDiscount')
            fval_ = self.gds_validate_decimal(fval_, node, 'TotalDiscount')
            self.TotalDiscount = fval_
            self.TotalDiscount_nsprefix_ = child_.prefix
            # validate type TotalDiscountType17
            self.validate_TotalDiscountType17(self.TotalDiscount)
        elif nodeName_ == 'WeightChargeTaxDet':
            obj_ = WeightChargeTaxDetType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.WeightChargeTaxDet.append(obj_)
            obj_.original_tagname_ = 'WeightChargeTaxDet'
        elif nodeName_ == 'PickupWindowEarliestTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupWindowEarliestTime')
            value_ = self.gds_validate_string(value_, node, 'PickupWindowEarliestTime')
            self.PickupWindowEarliestTime = value_
            self.PickupWindowEarliestTime_nsprefix_ = child_.prefix
            # validate type PickupWindowEarliestTimeType
            self.validate_PickupWindowEarliestTimeType(self.PickupWindowEarliestTime)
        elif nodeName_ == 'PickupWindowLatestTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupWindowLatestTime')
            value_ = self.gds_validate_string(value_, node, 'PickupWindowLatestTime')
            self.PickupWindowLatestTime = value_
            self.PickupWindowLatestTime_nsprefix_ = child_.prefix
            # validate type PickupWindowLatestTimeType
            self.validate_PickupWindowLatestTimeType(self.PickupWindowLatestTime)
        elif nodeName_ == 'BookingCutoffOffset':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BookingCutoffOffset')
            value_ = self.gds_validate_string(value_, node, 'BookingCutoffOffset')
            self.BookingCutoffOffset = value_
            self.BookingCutoffOffset_nsprefix_ = child_.prefix
            # validate type BookingCutoffOffsetType
            self.validate_BookingCutoffOffsetType(self.BookingCutoffOffset)
        elif nodeName_ == 'PickupLeadTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupLeadTime')
            value_ = self.gds_validate_string(value_, node, 'PickupLeadTime')
            self.PickupLeadTime = value_
            self.PickupLeadTime_nsprefix_ = child_.prefix
            # validate type PickupLeadTimeType
            self.validate_PickupLeadTimeType(self.PickupLeadTime)
        elif nodeName_ == 'PickupCloseTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupCloseTime')
            value_ = self.gds_validate_string(value_, node, 'PickupCloseTime')
            self.PickupCloseTime = value_
            self.PickupCloseTime_nsprefix_ = child_.prefix
            # validate type PickupCloseTimeType
            self.validate_PickupCloseTimeType(self.PickupCloseTime)
        elif nodeName_ == 'WeightChargeDisc':
            obj_ = WeightChargeDisc.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.WeightChargeDisc.append(obj_)
            obj_.original_tagname_ = 'WeightChargeDisc'
        elif nodeName_ == 'QtdShpExChrgDisc':
            obj_ = QtdShpExChrgDisc.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.QtdShpExChrgDisc.append(obj_)
            obj_.original_tagname_ = 'QtdShpExChrgDisc'
# end class QtdShpType


class MrkSrvType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, LocalProductCode=None, LocalServiceType=None, ProductShortName=None, GlobalServiceName=None, LocalProductName=None, LocalServiceTypeName=None, ProductDesc=None, ServiceDesc=None, NetworkTypeCode=None, POfferedCustAgreement=None, SOfferedCustAgreement=None, TransInd=None, ChargeCodeType=None, MrkSrvInd=None, LocalProductCtryCd=None, LocalProductDesc=None, GlobalProductDesc=None, GlobalServiceType=None, BillingServiceIndicator=None, LocalServiceName=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.LocalProductCode = LocalProductCode
        self.LocalProductCode_nsprefix_ = None
        self.LocalServiceType = LocalServiceType
        self.LocalServiceType_nsprefix_ = None
        self.ProductShortName = ProductShortName
        self.ProductShortName_nsprefix_ = None
        self.GlobalServiceName = GlobalServiceName
        self.GlobalServiceName_nsprefix_ = None
        self.LocalProductName = LocalProductName
        self.LocalProductName_nsprefix_ = None
        self.LocalServiceTypeName = LocalServiceTypeName
        self.LocalServiceTypeName_nsprefix_ = None
        self.ProductDesc = ProductDesc
        self.ProductDesc_nsprefix_ = None
        self.ServiceDesc = ServiceDesc
        self.ServiceDesc_nsprefix_ = None
        self.NetworkTypeCode = NetworkTypeCode
        self.NetworkTypeCode_nsprefix_ = None
        self.POfferedCustAgreement = POfferedCustAgreement
        self.POfferedCustAgreement_nsprefix_ = None
        self.SOfferedCustAgreement = SOfferedCustAgreement
        self.SOfferedCustAgreement_nsprefix_ = None
        self.TransInd = TransInd
        self.TransInd_nsprefix_ = None
        if ChargeCodeType is None:
            self.ChargeCodeType = []
        else:
            self.ChargeCodeType = ChargeCodeType
        self.ChargeCodeType_nsprefix_ = None
        self.MrkSrvInd = MrkSrvInd
        self.validate_MrkSrvIndType(self.MrkSrvInd)
        self.MrkSrvInd_nsprefix_ = None
        self.LocalProductCtryCd = LocalProductCtryCd
        self.validate_LocalProductCtryCdType(self.LocalProductCtryCd)
        self.LocalProductCtryCd_nsprefix_ = None
        self.LocalProductDesc = LocalProductDesc
        self.LocalProductDesc_nsprefix_ = None
        self.GlobalProductDesc = GlobalProductDesc
        self.GlobalProductDesc_nsprefix_ = None
        self.GlobalServiceType = GlobalServiceType
        self.GlobalServiceType_nsprefix_ = None
        self.BillingServiceIndicator = BillingServiceIndicator
        self.BillingServiceIndicator_nsprefix_ = None
        self.LocalServiceName = LocalServiceName
        self.LocalServiceName_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, MrkSrvType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if MrkSrvType.subclass:
            return MrkSrvType.subclass(*args_, **kwargs_)
        else:
            return MrkSrvType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_LocalProductCode(self):
        return self.LocalProductCode
    def set_LocalProductCode(self, LocalProductCode):
        self.LocalProductCode = LocalProductCode
    def get_LocalServiceType(self):
        return self.LocalServiceType
    def set_LocalServiceType(self, LocalServiceType):
        self.LocalServiceType = LocalServiceType
    def get_ProductShortName(self):
        return self.ProductShortName
    def set_ProductShortName(self, ProductShortName):
        self.ProductShortName = ProductShortName
    def get_GlobalServiceName(self):
        return self.GlobalServiceName
    def set_GlobalServiceName(self, GlobalServiceName):
        self.GlobalServiceName = GlobalServiceName
    def get_LocalProductName(self):
        return self.LocalProductName
    def set_LocalProductName(self, LocalProductName):
        self.LocalProductName = LocalProductName
    def get_LocalServiceTypeName(self):
        return self.LocalServiceTypeName
    def set_LocalServiceTypeName(self, LocalServiceTypeName):
        self.LocalServiceTypeName = LocalServiceTypeName
    def get_ProductDesc(self):
        return self.ProductDesc
    def set_ProductDesc(self, ProductDesc):
        self.ProductDesc = ProductDesc
    def get_ServiceDesc(self):
        return self.ServiceDesc
    def set_ServiceDesc(self, ServiceDesc):
        self.ServiceDesc = ServiceDesc
    def get_NetworkTypeCode(self):
        return self.NetworkTypeCode
    def set_NetworkTypeCode(self, NetworkTypeCode):
        self.NetworkTypeCode = NetworkTypeCode
    def get_POfferedCustAgreement(self):
        return self.POfferedCustAgreement
    def set_POfferedCustAgreement(self, POfferedCustAgreement):
        self.POfferedCustAgreement = POfferedCustAgreement
    def get_SOfferedCustAgreement(self):
        return self.SOfferedCustAgreement
    def set_SOfferedCustAgreement(self, SOfferedCustAgreement):
        self.SOfferedCustAgreement = SOfferedCustAgreement
    def get_TransInd(self):
        return self.TransInd
    def set_TransInd(self, TransInd):
        self.TransInd = TransInd
    def get_ChargeCodeType(self):
        return self.ChargeCodeType
    def set_ChargeCodeType(self, ChargeCodeType):
        self.ChargeCodeType = ChargeCodeType
    def add_ChargeCodeType(self, value):
        self.ChargeCodeType.append(value)
    def insert_ChargeCodeType_at(self, index, value):
        self.ChargeCodeType.insert(index, value)
    def replace_ChargeCodeType_at(self, index, value):
        self.ChargeCodeType[index] = value
    def get_MrkSrvInd(self):
        return self.MrkSrvInd
    def set_MrkSrvInd(self, MrkSrvInd):
        self.MrkSrvInd = MrkSrvInd
    def get_LocalProductCtryCd(self):
        return self.LocalProductCtryCd
    def set_LocalProductCtryCd(self, LocalProductCtryCd):
        self.LocalProductCtryCd = LocalProductCtryCd
    def get_LocalProductDesc(self):
        return self.LocalProductDesc
    def set_LocalProductDesc(self, LocalProductDesc):
        self.LocalProductDesc = LocalProductDesc
    def get_GlobalProductDesc(self):
        return self.GlobalProductDesc
    def set_GlobalProductDesc(self, GlobalProductDesc):
        self.GlobalProductDesc = GlobalProductDesc
    def get_GlobalServiceType(self):
        return self.GlobalServiceType
    def set_GlobalServiceType(self, GlobalServiceType):
        self.GlobalServiceType = GlobalServiceType
    def get_BillingServiceIndicator(self):
        return self.BillingServiceIndicator
    def set_BillingServiceIndicator(self, BillingServiceIndicator):
        self.BillingServiceIndicator = BillingServiceIndicator
    def get_LocalServiceName(self):
        return self.LocalServiceName
    def set_LocalServiceName(self, LocalServiceName):
        self.LocalServiceName = LocalServiceName
    def validate_MrkSrvIndType(self, value):
        result = True
        # Validate type MrkSrvIndType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on MrkSrvIndType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_LocalProductCtryCdType(self, value):
        result = True
        # Validate type LocalProductCtryCdType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on LocalProductCtryCdType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.LocalProductCode is not None or
            self.LocalServiceType is not None or
            self.ProductShortName is not None or
            self.GlobalServiceName is not None or
            self.LocalProductName is not None or
            self.LocalServiceTypeName is not None or
            self.ProductDesc is not None or
            self.ServiceDesc is not None or
            self.NetworkTypeCode is not None or
            self.POfferedCustAgreement is not None or
            self.SOfferedCustAgreement is not None or
            self.TransInd is not None or
            self.ChargeCodeType or
            self.MrkSrvInd is not None or
            self.LocalProductCtryCd is not None or
            self.LocalProductDesc is not None or
            self.GlobalProductDesc is not None or
            self.GlobalServiceType is not None or
            self.BillingServiceIndicator is not None or
            self.LocalServiceName is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='MrkSrvType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('MrkSrvType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'MrkSrvType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='MrkSrvType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='MrkSrvType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='MrkSrvType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='MrkSrvType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.LocalProductCode is not None:
            namespaceprefix_ = self.LocalProductCode_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalProductCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalProductCode>%s</%sLocalProductCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalProductCode), input_name='LocalProductCode')), namespaceprefix_ , eol_))
        if self.LocalServiceType is not None:
            namespaceprefix_ = self.LocalServiceType_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalServiceType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalServiceType>%s</%sLocalServiceType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalServiceType), input_name='LocalServiceType')), namespaceprefix_ , eol_))
        if self.ProductShortName is not None:
            namespaceprefix_ = self.ProductShortName_nsprefix_ + ':' if (UseCapturedNS_ and self.ProductShortName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProductShortName>%s</%sProductShortName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ProductShortName), input_name='ProductShortName')), namespaceprefix_ , eol_))
        if self.GlobalServiceName is not None:
            namespaceprefix_ = self.GlobalServiceName_nsprefix_ + ':' if (UseCapturedNS_ and self.GlobalServiceName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGlobalServiceName>%s</%sGlobalServiceName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GlobalServiceName), input_name='GlobalServiceName')), namespaceprefix_ , eol_))
        if self.LocalProductName is not None:
            namespaceprefix_ = self.LocalProductName_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalProductName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalProductName>%s</%sLocalProductName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalProductName), input_name='LocalProductName')), namespaceprefix_ , eol_))
        if self.LocalServiceTypeName is not None:
            namespaceprefix_ = self.LocalServiceTypeName_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalServiceTypeName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalServiceTypeName>%s</%sLocalServiceTypeName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalServiceTypeName), input_name='LocalServiceTypeName')), namespaceprefix_ , eol_))
        if self.ProductDesc is not None:
            namespaceprefix_ = self.ProductDesc_nsprefix_ + ':' if (UseCapturedNS_ and self.ProductDesc_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProductDesc>%s</%sProductDesc>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ProductDesc), input_name='ProductDesc')), namespaceprefix_ , eol_))
        if self.ServiceDesc is not None:
            namespaceprefix_ = self.ServiceDesc_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceDesc_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceDesc>%s</%sServiceDesc>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServiceDesc), input_name='ServiceDesc')), namespaceprefix_ , eol_))
        if self.NetworkTypeCode is not None:
            namespaceprefix_ = self.NetworkTypeCode_nsprefix_ + ':' if (UseCapturedNS_ and self.NetworkTypeCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNetworkTypeCode>%s</%sNetworkTypeCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NetworkTypeCode), input_name='NetworkTypeCode')), namespaceprefix_ , eol_))
        if self.POfferedCustAgreement is not None:
            namespaceprefix_ = self.POfferedCustAgreement_nsprefix_ + ':' if (UseCapturedNS_ and self.POfferedCustAgreement_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPOfferedCustAgreement>%s</%sPOfferedCustAgreement>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.POfferedCustAgreement), input_name='POfferedCustAgreement')), namespaceprefix_ , eol_))
        if self.SOfferedCustAgreement is not None:
            namespaceprefix_ = self.SOfferedCustAgreement_nsprefix_ + ':' if (UseCapturedNS_ and self.SOfferedCustAgreement_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSOfferedCustAgreement>%s</%sSOfferedCustAgreement>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SOfferedCustAgreement), input_name='SOfferedCustAgreement')), namespaceprefix_ , eol_))
        if self.TransInd is not None:
            namespaceprefix_ = self.TransInd_nsprefix_ + ':' if (UseCapturedNS_ and self.TransInd_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTransInd>%s</%sTransInd>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.TransInd), input_name='TransInd')), namespaceprefix_ , eol_))
        for ChargeCodeType_ in self.ChargeCodeType:
            namespaceprefix_ = self.ChargeCodeType_nsprefix_ + ':' if (UseCapturedNS_ and self.ChargeCodeType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sChargeCodeType>%s</%sChargeCodeType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(ChargeCodeType_), input_name='ChargeCodeType')), namespaceprefix_ , eol_))
        if self.MrkSrvInd is not None:
            namespaceprefix_ = self.MrkSrvInd_nsprefix_ + ':' if (UseCapturedNS_ and self.MrkSrvInd_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMrkSrvInd>%s</%sMrkSrvInd>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.MrkSrvInd), input_name='MrkSrvInd')), namespaceprefix_ , eol_))
        if self.LocalProductCtryCd is not None:
            namespaceprefix_ = self.LocalProductCtryCd_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalProductCtryCd_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalProductCtryCd>%s</%sLocalProductCtryCd>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalProductCtryCd), input_name='LocalProductCtryCd')), namespaceprefix_ , eol_))
        if self.LocalProductDesc is not None:
            namespaceprefix_ = self.LocalProductDesc_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalProductDesc_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalProductDesc>%s</%sLocalProductDesc>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalProductDesc), input_name='LocalProductDesc')), namespaceprefix_ , eol_))
        if self.GlobalProductDesc is not None:
            namespaceprefix_ = self.GlobalProductDesc_nsprefix_ + ':' if (UseCapturedNS_ and self.GlobalProductDesc_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGlobalProductDesc>%s</%sGlobalProductDesc>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GlobalProductDesc), input_name='GlobalProductDesc')), namespaceprefix_ , eol_))
        if self.GlobalServiceType is not None:
            namespaceprefix_ = self.GlobalServiceType_nsprefix_ + ':' if (UseCapturedNS_ and self.GlobalServiceType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGlobalServiceType>%s</%sGlobalServiceType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GlobalServiceType), input_name='GlobalServiceType')), namespaceprefix_ , eol_))
        if self.BillingServiceIndicator is not None:
            namespaceprefix_ = self.BillingServiceIndicator_nsprefix_ + ':' if (UseCapturedNS_ and self.BillingServiceIndicator_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBillingServiceIndicator>%s</%sBillingServiceIndicator>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BillingServiceIndicator), input_name='BillingServiceIndicator')), namespaceprefix_ , eol_))
        if self.LocalServiceName is not None:
            namespaceprefix_ = self.LocalServiceName_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalServiceName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalServiceName>%s</%sLocalServiceName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LocalServiceName), input_name='LocalServiceName')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'LocalProductCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalProductCode')
            value_ = self.gds_validate_string(value_, node, 'LocalProductCode')
            self.LocalProductCode = value_
            self.LocalProductCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocalServiceType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalServiceType')
            value_ = self.gds_validate_string(value_, node, 'LocalServiceType')
            self.LocalServiceType = value_
            self.LocalServiceType_nsprefix_ = child_.prefix
        elif nodeName_ == 'ProductShortName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ProductShortName')
            value_ = self.gds_validate_string(value_, node, 'ProductShortName')
            self.ProductShortName = value_
            self.ProductShortName_nsprefix_ = child_.prefix
        elif nodeName_ == 'GlobalServiceName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GlobalServiceName')
            value_ = self.gds_validate_string(value_, node, 'GlobalServiceName')
            self.GlobalServiceName = value_
            self.GlobalServiceName_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocalProductName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalProductName')
            value_ = self.gds_validate_string(value_, node, 'LocalProductName')
            self.LocalProductName = value_
            self.LocalProductName_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocalServiceTypeName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalServiceTypeName')
            value_ = self.gds_validate_string(value_, node, 'LocalServiceTypeName')
            self.LocalServiceTypeName = value_
            self.LocalServiceTypeName_nsprefix_ = child_.prefix
        elif nodeName_ == 'ProductDesc':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ProductDesc')
            value_ = self.gds_validate_string(value_, node, 'ProductDesc')
            self.ProductDesc = value_
            self.ProductDesc_nsprefix_ = child_.prefix
        elif nodeName_ == 'ServiceDesc':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServiceDesc')
            value_ = self.gds_validate_string(value_, node, 'ServiceDesc')
            self.ServiceDesc = value_
            self.ServiceDesc_nsprefix_ = child_.prefix
        elif nodeName_ == 'NetworkTypeCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NetworkTypeCode')
            value_ = self.gds_validate_string(value_, node, 'NetworkTypeCode')
            self.NetworkTypeCode = value_
            self.NetworkTypeCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'POfferedCustAgreement':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'POfferedCustAgreement')
            value_ = self.gds_validate_string(value_, node, 'POfferedCustAgreement')
            self.POfferedCustAgreement = value_
            self.POfferedCustAgreement_nsprefix_ = child_.prefix
        elif nodeName_ == 'SOfferedCustAgreement':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SOfferedCustAgreement')
            value_ = self.gds_validate_string(value_, node, 'SOfferedCustAgreement')
            self.SOfferedCustAgreement = value_
            self.SOfferedCustAgreement_nsprefix_ = child_.prefix
        elif nodeName_ == 'TransInd':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'TransInd')
            value_ = self.gds_validate_string(value_, node, 'TransInd')
            self.TransInd = value_
            self.TransInd_nsprefix_ = child_.prefix
        elif nodeName_ == 'ChargeCodeType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChargeCodeType')
            value_ = self.gds_validate_string(value_, node, 'ChargeCodeType')
            self.ChargeCodeType.append(value_)
            self.ChargeCodeType_nsprefix_ = child_.prefix
        elif nodeName_ == 'MrkSrvInd':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'MrkSrvInd')
            value_ = self.gds_validate_string(value_, node, 'MrkSrvInd')
            self.MrkSrvInd = value_
            self.MrkSrvInd_nsprefix_ = child_.prefix
            # validate type MrkSrvIndType
            self.validate_MrkSrvIndType(self.MrkSrvInd)
        elif nodeName_ == 'LocalProductCtryCd':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalProductCtryCd')
            value_ = self.gds_validate_string(value_, node, 'LocalProductCtryCd')
            self.LocalProductCtryCd = value_
            self.LocalProductCtryCd_nsprefix_ = child_.prefix
            # validate type LocalProductCtryCdType
            self.validate_LocalProductCtryCdType(self.LocalProductCtryCd)
        elif nodeName_ == 'LocalProductDesc':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalProductDesc')
            value_ = self.gds_validate_string(value_, node, 'LocalProductDesc')
            self.LocalProductDesc = value_
            self.LocalProductDesc_nsprefix_ = child_.prefix
        elif nodeName_ == 'GlobalProductDesc':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GlobalProductDesc')
            value_ = self.gds_validate_string(value_, node, 'GlobalProductDesc')
            self.GlobalProductDesc = value_
            self.GlobalProductDesc_nsprefix_ = child_.prefix
        elif nodeName_ == 'GlobalServiceType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GlobalServiceType')
            value_ = self.gds_validate_string(value_, node, 'GlobalServiceType')
            self.GlobalServiceType = value_
            self.GlobalServiceType_nsprefix_ = child_.prefix
        elif nodeName_ == 'BillingServiceIndicator':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BillingServiceIndicator')
            value_ = self.gds_validate_string(value_, node, 'BillingServiceIndicator')
            self.BillingServiceIndicator = value_
            self.BillingServiceIndicator_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocalServiceName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalServiceName')
            value_ = self.gds_validate_string(value_, node, 'LocalServiceName')
            self.LocalServiceName = value_
            self.LocalServiceName_nsprefix_ = child_.prefix
# end class MrkSrvType


class ProdNtwrkType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, NetworkTypeCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.NetworkTypeCode = NetworkTypeCode
        self.validate_NetworkTypeCodeType(self.NetworkTypeCode)
        self.NetworkTypeCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ProdNtwrkType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ProdNtwrkType.subclass:
            return ProdNtwrkType.subclass(*args_, **kwargs_)
        else:
            return ProdNtwrkType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_NetworkTypeCode(self):
        return self.NetworkTypeCode
    def set_NetworkTypeCode(self, NetworkTypeCode):
        self.NetworkTypeCode = NetworkTypeCode
    def validate_NetworkTypeCodeType(self, value):
        result = True
        # Validate type NetworkTypeCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on NetworkTypeCodeType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.NetworkTypeCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ProdNtwrkType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ProdNtwrkType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ProdNtwrkType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ProdNtwrkType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ProdNtwrkType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ProdNtwrkType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ProdNtwrkType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.NetworkTypeCode is not None:
            namespaceprefix_ = self.NetworkTypeCode_nsprefix_ + ':' if (UseCapturedNS_ and self.NetworkTypeCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNetworkTypeCode>%s</%sNetworkTypeCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NetworkTypeCode), input_name='NetworkTypeCode')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'NetworkTypeCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NetworkTypeCode')
            value_ = self.gds_validate_string(value_, node, 'NetworkTypeCode')
            self.NetworkTypeCode = value_
            self.NetworkTypeCode_nsprefix_ = child_.prefix
            # validate type NetworkTypeCodeType
            self.validate_NetworkTypeCodeType(self.NetworkTypeCode)
# end class ProdNtwrkType


class SrvType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, GlobalProductCode=None, MrkSrv=None, SBTP=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.GlobalProductCode = GlobalProductCode
        self.GlobalProductCode_nsprefix_ = None
        if MrkSrv is None:
            self.MrkSrv = []
        else:
            self.MrkSrv = MrkSrv
        self.MrkSrv_nsprefix_ = None
        self.SBTP = SBTP
        self.SBTP_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SrvType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SrvType.subclass:
            return SrvType.subclass(*args_, **kwargs_)
        else:
            return SrvType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_GlobalProductCode(self):
        return self.GlobalProductCode
    def set_GlobalProductCode(self, GlobalProductCode):
        self.GlobalProductCode = GlobalProductCode
    def get_MrkSrv(self):
        return self.MrkSrv
    def set_MrkSrv(self, MrkSrv):
        self.MrkSrv = MrkSrv
    def add_MrkSrv(self, value):
        self.MrkSrv.append(value)
    def insert_MrkSrv_at(self, index, value):
        self.MrkSrv.insert(index, value)
    def replace_MrkSrv_at(self, index, value):
        self.MrkSrv[index] = value
    def get_SBTP(self):
        return self.SBTP
    def set_SBTP(self, SBTP):
        self.SBTP = SBTP
    def _hasContent(self):
        if (
            self.GlobalProductCode is not None or
            self.MrkSrv or
            self.SBTP is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SrvType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SrvType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SrvType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SrvType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SrvType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SrvType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SrvType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.GlobalProductCode is not None:
            namespaceprefix_ = self.GlobalProductCode_nsprefix_ + ':' if (UseCapturedNS_ and self.GlobalProductCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sGlobalProductCode>%s</%sGlobalProductCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.GlobalProductCode), input_name='GlobalProductCode')), namespaceprefix_ , eol_))
        for MrkSrv_ in self.MrkSrv:
            namespaceprefix_ = self.MrkSrv_nsprefix_ + ':' if (UseCapturedNS_ and self.MrkSrv_nsprefix_) else ''
            MrkSrv_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='MrkSrv', pretty_print=pretty_print)
        if self.SBTP is not None:
            namespaceprefix_ = self.SBTP_nsprefix_ + ':' if (UseCapturedNS_ and self.SBTP_nsprefix_) else ''
            self.SBTP.export(outfile, level, namespaceprefix_, namespacedef_='', name_='SBTP', pretty_print=pretty_print)
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
        if nodeName_ == 'GlobalProductCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'GlobalProductCode')
            value_ = self.gds_validate_string(value_, node, 'GlobalProductCode')
            self.GlobalProductCode = value_
            self.GlobalProductCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'MrkSrv':
            obj_ = MrkSrvType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.MrkSrv.append(obj_)
            obj_.original_tagname_ = 'MrkSrv'
        elif nodeName_ == 'SBTP':
            obj_ = SBTPType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SBTP = obj_
            obj_.original_tagname_ = 'SBTP'
# end class SrvType


class SBTPType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Prod=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Prod = Prod
        self.Prod_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SBTPType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SBTPType.subclass:
            return SBTPType.subclass(*args_, **kwargs_)
        else:
            return SBTPType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Prod(self):
        return self.Prod
    def set_Prod(self, Prod):
        self.Prod = Prod
    def _hasContent(self):
        if (
            self.Prod is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SBTPType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SBTPType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SBTPType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SBTPType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SBTPType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SBTPType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SBTPType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Prod is not None:
            namespaceprefix_ = self.Prod_nsprefix_ + ':' if (UseCapturedNS_ and self.Prod_nsprefix_) else ''
            self.Prod.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Prod', pretty_print=pretty_print)
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
        if nodeName_ == 'Prod':
            obj_ = ProdType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Prod = obj_
            obj_.original_tagname_ = 'Prod'
# end class SBTPType


class DeliveryDate(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DeliveryType=None, DlvyDateTime=None, DeliveryDateTimeOffset=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DeliveryType = DeliveryType
        self.DeliveryType_nsprefix_ = None
        self.DlvyDateTime = DlvyDateTime
        self.DlvyDateTime_nsprefix_ = None
        self.DeliveryDateTimeOffset = DeliveryDateTimeOffset
        self.DeliveryDateTimeOffset_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DeliveryDate)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DeliveryDate.subclass:
            return DeliveryDate.subclass(*args_, **kwargs_)
        else:
            return DeliveryDate(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DeliveryType(self):
        return self.DeliveryType
    def set_DeliveryType(self, DeliveryType):
        self.DeliveryType = DeliveryType
    def get_DlvyDateTime(self):
        return self.DlvyDateTime
    def set_DlvyDateTime(self, DlvyDateTime):
        self.DlvyDateTime = DlvyDateTime
    def get_DeliveryDateTimeOffset(self):
        return self.DeliveryDateTimeOffset
    def set_DeliveryDateTimeOffset(self, DeliveryDateTimeOffset):
        self.DeliveryDateTimeOffset = DeliveryDateTimeOffset
    def _hasContent(self):
        if (
            self.DeliveryType is not None or
            self.DlvyDateTime is not None or
            self.DeliveryDateTimeOffset is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeliveryDate', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DeliveryDate')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DeliveryDate':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DeliveryDate')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DeliveryDate', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DeliveryDate'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeliveryDate', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DeliveryType is not None:
            namespaceprefix_ = self.DeliveryType_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeliveryType>%s</%sDeliveryType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DeliveryType), input_name='DeliveryType')), namespaceprefix_ , eol_))
        if self.DlvyDateTime is not None:
            namespaceprefix_ = self.DlvyDateTime_nsprefix_ + ':' if (UseCapturedNS_ and self.DlvyDateTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDlvyDateTime>%s</%sDlvyDateTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DlvyDateTime), input_name='DlvyDateTime')), namespaceprefix_ , eol_))
        if self.DeliveryDateTimeOffset is not None:
            namespaceprefix_ = self.DeliveryDateTimeOffset_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryDateTimeOffset_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDeliveryDateTimeOffset>%s</%sDeliveryDateTimeOffset>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DeliveryDateTimeOffset), input_name='DeliveryDateTimeOffset')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'DeliveryType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DeliveryType')
            value_ = self.gds_validate_string(value_, node, 'DeliveryType')
            self.DeliveryType = value_
            self.DeliveryType_nsprefix_ = child_.prefix
        elif nodeName_ == 'DlvyDateTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DlvyDateTime')
            value_ = self.gds_validate_string(value_, node, 'DlvyDateTime')
            self.DlvyDateTime = value_
            self.DlvyDateTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'DeliveryDateTimeOffset':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DeliveryDateTimeOffset')
            value_ = self.gds_validate_string(value_, node, 'DeliveryDateTimeOffset')
            self.DeliveryDateTimeOffset = value_
            self.DeliveryDateTimeOffset_nsprefix_ = child_.prefix
# end class DeliveryDate


class WeightChargeDisc(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DiscAmt=None, BaseAmount=None, CurrencyCode=None, DiscType=None, DiscPercentage=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DiscAmt = DiscAmt
        self.validate_DiscAmtType(self.DiscAmt)
        self.DiscAmt_nsprefix_ = None
        self.BaseAmount = BaseAmount
        self.validate_BaseAmountType18(self.BaseAmount)
        self.BaseAmount_nsprefix_ = None
        self.CurrencyCode = CurrencyCode
        self.validate_CurrencyCodeType19(self.CurrencyCode)
        self.CurrencyCode_nsprefix_ = None
        self.DiscType = DiscType
        self.validate_DiscTypeType(self.DiscType)
        self.DiscType_nsprefix_ = None
        self.DiscPercentage = DiscPercentage
        self.validate_DiscPercentageType(self.DiscPercentage)
        self.DiscPercentage_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, WeightChargeDisc)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if WeightChargeDisc.subclass:
            return WeightChargeDisc.subclass(*args_, **kwargs_)
        else:
            return WeightChargeDisc(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DiscAmt(self):
        return self.DiscAmt
    def set_DiscAmt(self, DiscAmt):
        self.DiscAmt = DiscAmt
    def get_BaseAmount(self):
        return self.BaseAmount
    def set_BaseAmount(self, BaseAmount):
        self.BaseAmount = BaseAmount
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_DiscType(self):
        return self.DiscType
    def set_DiscType(self, DiscType):
        self.DiscType = DiscType
    def get_DiscPercentage(self):
        return self.DiscPercentage
    def set_DiscPercentage(self, DiscPercentage):
        self.DiscPercentage = DiscPercentage
    def validate_DiscAmtType(self, value):
        result = True
        # Validate type DiscAmtType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on DiscAmtType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_BaseAmountType18(self, value):
        result = True
        # Validate type BaseAmountType18, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on BaseAmountType18' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_CurrencyCodeType19(self, value):
        result = True
        # Validate type CurrencyCodeType19, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CurrencyCodeType19' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DiscTypeType(self, value):
        result = True
        # Validate type DiscTypeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on DiscTypeType' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DiscPercentageType(self, value):
        result = True
        # Validate type DiscPercentageType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on DiscPercentageType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.DiscAmt is not None or
            self.BaseAmount is not None or
            self.CurrencyCode is not None or
            self.DiscType is not None or
            self.DiscPercentage is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WeightChargeDisc', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('WeightChargeDisc')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'WeightChargeDisc':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='WeightChargeDisc')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='WeightChargeDisc', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='WeightChargeDisc'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='WeightChargeDisc', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DiscAmt is not None:
            namespaceprefix_ = self.DiscAmt_nsprefix_ + ':' if (UseCapturedNS_ and self.DiscAmt_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDiscAmt>%s</%sDiscAmt>%s' % (namespaceprefix_ , self.gds_format_decimal(self.DiscAmt, input_name='DiscAmt'), namespaceprefix_ , eol_))
        if self.BaseAmount is not None:
            namespaceprefix_ = self.BaseAmount_nsprefix_ + ':' if (UseCapturedNS_ and self.BaseAmount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBaseAmount>%s</%sBaseAmount>%s' % (namespaceprefix_ , self.gds_format_decimal(self.BaseAmount, input_name='BaseAmount'), namespaceprefix_ , eol_))
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.DiscType is not None:
            namespaceprefix_ = self.DiscType_nsprefix_ + ':' if (UseCapturedNS_ and self.DiscType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDiscType>%s</%sDiscType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DiscType), input_name='DiscType')), namespaceprefix_ , eol_))
        if self.DiscPercentage is not None:
            namespaceprefix_ = self.DiscPercentage_nsprefix_ + ':' if (UseCapturedNS_ and self.DiscPercentage_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDiscPercentage>%s</%sDiscPercentage>%s' % (namespaceprefix_ , self.gds_format_decimal(self.DiscPercentage, input_name='DiscPercentage'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'DiscAmt' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'DiscAmt')
            fval_ = self.gds_validate_decimal(fval_, node, 'DiscAmt')
            self.DiscAmt = fval_
            self.DiscAmt_nsprefix_ = child_.prefix
            # validate type DiscAmtType
            self.validate_DiscAmtType(self.DiscAmt)
        elif nodeName_ == 'BaseAmount' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'BaseAmount')
            fval_ = self.gds_validate_decimal(fval_, node, 'BaseAmount')
            self.BaseAmount = fval_
            self.BaseAmount_nsprefix_ = child_.prefix
            # validate type BaseAmountType18
            self.validate_BaseAmountType18(self.BaseAmount)
        elif nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
            # validate type CurrencyCodeType19
            self.validate_CurrencyCodeType19(self.CurrencyCode)
        elif nodeName_ == 'DiscType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DiscType')
            value_ = self.gds_validate_string(value_, node, 'DiscType')
            self.DiscType = value_
            self.DiscType_nsprefix_ = child_.prefix
            # validate type DiscTypeType
            self.validate_DiscTypeType(self.DiscType)
        elif nodeName_ == 'DiscPercentage' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'DiscPercentage')
            fval_ = self.gds_validate_decimal(fval_, node, 'DiscPercentage')
            self.DiscPercentage = fval_
            self.DiscPercentage_nsprefix_ = child_.prefix
            # validate type DiscPercentageType
            self.validate_DiscPercentageType(self.DiscPercentage)
# end class WeightChargeDisc


class QtdShpExChrgDisc(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DiscAmt=None, BaseAmt=None, CurrencyCode=None, CurrencyRoleTypeCode=None, DiscPercentage=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DiscAmt = DiscAmt
        self.validate_DiscAmtType20(self.DiscAmt)
        self.DiscAmt_nsprefix_ = None
        self.BaseAmt = BaseAmt
        self.validate_BaseAmtType21(self.BaseAmt)
        self.BaseAmt_nsprefix_ = None
        self.CurrencyCode = CurrencyCode
        self.validate_CurrencyCodeType22(self.CurrencyCode)
        self.CurrencyCode_nsprefix_ = None
        self.CurrencyRoleTypeCode = CurrencyRoleTypeCode
        self.validate_CurrencyRoleTypeCodeType23(self.CurrencyRoleTypeCode)
        self.CurrencyRoleTypeCode_nsprefix_ = None
        self.DiscPercentage = DiscPercentage
        self.validate_DiscPercentageType24(self.DiscPercentage)
        self.DiscPercentage_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, QtdShpExChrgDisc)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if QtdShpExChrgDisc.subclass:
            return QtdShpExChrgDisc.subclass(*args_, **kwargs_)
        else:
            return QtdShpExChrgDisc(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DiscAmt(self):
        return self.DiscAmt
    def set_DiscAmt(self, DiscAmt):
        self.DiscAmt = DiscAmt
    def get_BaseAmt(self):
        return self.BaseAmt
    def set_BaseAmt(self, BaseAmt):
        self.BaseAmt = BaseAmt
    def get_CurrencyCode(self):
        return self.CurrencyCode
    def set_CurrencyCode(self, CurrencyCode):
        self.CurrencyCode = CurrencyCode
    def get_CurrencyRoleTypeCode(self):
        return self.CurrencyRoleTypeCode
    def set_CurrencyRoleTypeCode(self, CurrencyRoleTypeCode):
        self.CurrencyRoleTypeCode = CurrencyRoleTypeCode
    def get_DiscPercentage(self):
        return self.DiscPercentage
    def set_DiscPercentage(self, DiscPercentage):
        self.DiscPercentage = DiscPercentage
    def validate_DiscAmtType20(self, value):
        result = True
        # Validate type DiscAmtType20, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on DiscAmtType20' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_BaseAmtType21(self, value):
        result = True
        # Validate type BaseAmtType21, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on BaseAmtType21' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_CurrencyCodeType22(self, value):
        result = True
        # Validate type CurrencyCodeType22, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CurrencyCodeType22' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_CurrencyRoleTypeCodeType23(self, value):
        result = True
        # Validate type CurrencyRoleTypeCodeType23, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) != 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd length restriction on CurrencyRoleTypeCodeType23' % {"value": encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_DiscPercentageType24(self, value):
        result = True
        # Validate type DiscPercentageType24, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if len(str(value)) >= 18:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on DiscPercentageType24' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.DiscAmt is not None or
            self.BaseAmt is not None or
            self.CurrencyCode is not None or
            self.CurrencyRoleTypeCode is not None or
            self.DiscPercentage is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='QtdShpExChrgDisc', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('QtdShpExChrgDisc')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'QtdShpExChrgDisc':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='QtdShpExChrgDisc')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='QtdShpExChrgDisc', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='QtdShpExChrgDisc'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='QtdShpExChrgDisc', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DiscAmt is not None:
            namespaceprefix_ = self.DiscAmt_nsprefix_ + ':' if (UseCapturedNS_ and self.DiscAmt_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDiscAmt>%s</%sDiscAmt>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DiscAmt), input_name='DiscAmt')), namespaceprefix_ , eol_))
        if self.BaseAmt is not None:
            namespaceprefix_ = self.BaseAmt_nsprefix_ + ':' if (UseCapturedNS_ and self.BaseAmt_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBaseAmt>%s</%sBaseAmt>%s' % (namespaceprefix_ , self.gds_format_decimal(self.BaseAmt, input_name='BaseAmt'), namespaceprefix_ , eol_))
        if self.CurrencyCode is not None:
            namespaceprefix_ = self.CurrencyCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyCode>%s</%sCurrencyCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyCode), input_name='CurrencyCode')), namespaceprefix_ , eol_))
        if self.CurrencyRoleTypeCode is not None:
            namespaceprefix_ = self.CurrencyRoleTypeCode_nsprefix_ + ':' if (UseCapturedNS_ and self.CurrencyRoleTypeCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCurrencyRoleTypeCode>%s</%sCurrencyRoleTypeCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CurrencyRoleTypeCode), input_name='CurrencyRoleTypeCode')), namespaceprefix_ , eol_))
        if self.DiscPercentage is not None:
            namespaceprefix_ = self.DiscPercentage_nsprefix_ + ':' if (UseCapturedNS_ and self.DiscPercentage_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDiscPercentage>%s</%sDiscPercentage>%s' % (namespaceprefix_ , self.gds_format_decimal(self.DiscPercentage, input_name='DiscPercentage'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'DiscAmt':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DiscAmt')
            value_ = self.gds_validate_string(value_, node, 'DiscAmt')
            self.DiscAmt = value_
            self.DiscAmt_nsprefix_ = child_.prefix
            # validate type DiscAmtType20
            self.validate_DiscAmtType20(self.DiscAmt)
        elif nodeName_ == 'BaseAmt' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'BaseAmt')
            fval_ = self.gds_validate_decimal(fval_, node, 'BaseAmt')
            self.BaseAmt = fval_
            self.BaseAmt_nsprefix_ = child_.prefix
            # validate type BaseAmtType21
            self.validate_BaseAmtType21(self.BaseAmt)
        elif nodeName_ == 'CurrencyCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyCode')
            self.CurrencyCode = value_
            self.CurrencyCode_nsprefix_ = child_.prefix
            # validate type CurrencyCodeType22
            self.validate_CurrencyCodeType22(self.CurrencyCode)
        elif nodeName_ == 'CurrencyRoleTypeCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CurrencyRoleTypeCode')
            value_ = self.gds_validate_string(value_, node, 'CurrencyRoleTypeCode')
            self.CurrencyRoleTypeCode = value_
            self.CurrencyRoleTypeCode_nsprefix_ = child_.prefix
            # validate type CurrencyRoleTypeCodeType23
            self.validate_CurrencyRoleTypeCodeType23(self.CurrencyRoleTypeCode)
        elif nodeName_ == 'DiscPercentage' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'DiscPercentage')
            fval_ = self.gds_validate_decimal(fval_, node, 'DiscPercentage')
            self.DiscPercentage = fval_
            self.DiscPercentage_nsprefix_ = child_.prefix
            # validate type DiscPercentageType24
            self.validate_DiscPercentageType24(self.DiscPercentage)
# end class QtdShpExChrgDisc


class SrvCombType3(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Prod=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Prod = Prod
        self.Prod_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, SrvCombType3)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if SrvCombType3.subclass:
            return SrvCombType3.subclass(*args_, **kwargs_)
        else:
            return SrvCombType3(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Prod(self):
        return self.Prod
    def set_Prod(self, Prod):
        self.Prod = Prod
    def _hasContent(self):
        if (
            self.Prod is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SrvCombType3', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('SrvCombType3')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'SrvCombType3':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='SrvCombType3')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='SrvCombType3', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='SrvCombType3'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='SrvCombType3', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Prod is not None:
            namespaceprefix_ = self.Prod_nsprefix_ + ':' if (UseCapturedNS_ and self.Prod_nsprefix_) else ''
            self.Prod.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Prod', pretty_print=pretty_print)
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
        if nodeName_ == 'Prod':
            obj_ = ProdType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Prod = obj_
            obj_.original_tagname_ = 'Prod'
# end class SrvCombType3


class VldSrvCombType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, SpecialServiceType=None, LocalServiceType=None, CombRSrv=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.SpecialServiceType = SpecialServiceType
        self.SpecialServiceType_nsprefix_ = None
        if LocalServiceType is None:
            self.LocalServiceType = []
        else:
            self.LocalServiceType = LocalServiceType
        self.LocalServiceType_nsprefix_ = None
        if CombRSrv is None:
            self.CombRSrv = []
        else:
            self.CombRSrv = CombRSrv
        self.CombRSrv_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, VldSrvCombType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if VldSrvCombType.subclass:
            return VldSrvCombType.subclass(*args_, **kwargs_)
        else:
            return VldSrvCombType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_SpecialServiceType(self):
        return self.SpecialServiceType
    def set_SpecialServiceType(self, SpecialServiceType):
        self.SpecialServiceType = SpecialServiceType
    def get_LocalServiceType(self):
        return self.LocalServiceType
    def set_LocalServiceType(self, LocalServiceType):
        self.LocalServiceType = LocalServiceType
    def add_LocalServiceType(self, value):
        self.LocalServiceType.append(value)
    def insert_LocalServiceType_at(self, index, value):
        self.LocalServiceType.insert(index, value)
    def replace_LocalServiceType_at(self, index, value):
        self.LocalServiceType[index] = value
    def get_CombRSrv(self):
        return self.CombRSrv
    def set_CombRSrv(self, CombRSrv):
        self.CombRSrv = CombRSrv
    def add_CombRSrv(self, value):
        self.CombRSrv.append(value)
    def insert_CombRSrv_at(self, index, value):
        self.CombRSrv.insert(index, value)
    def replace_CombRSrv_at(self, index, value):
        self.CombRSrv[index] = value
    def _hasContent(self):
        if (
            self.SpecialServiceType is not None or
            self.LocalServiceType or
            self.CombRSrv
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='VldSrvCombType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('VldSrvCombType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'VldSrvCombType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='VldSrvCombType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='VldSrvCombType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='VldSrvCombType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='VldSrvCombType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.SpecialServiceType is not None:
            namespaceprefix_ = self.SpecialServiceType_nsprefix_ + ':' if (UseCapturedNS_ and self.SpecialServiceType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSpecialServiceType>%s</%sSpecialServiceType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SpecialServiceType), input_name='SpecialServiceType')), namespaceprefix_ , eol_))
        for LocalServiceType_ in self.LocalServiceType:
            namespaceprefix_ = self.LocalServiceType_nsprefix_ + ':' if (UseCapturedNS_ and self.LocalServiceType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLocalServiceType>%s</%sLocalServiceType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(LocalServiceType_), input_name='LocalServiceType')), namespaceprefix_ , eol_))
        for CombRSrv_ in self.CombRSrv:
            namespaceprefix_ = self.CombRSrv_nsprefix_ + ':' if (UseCapturedNS_ and self.CombRSrv_nsprefix_) else ''
            CombRSrv_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CombRSrv', pretty_print=pretty_print)
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
        if nodeName_ == 'SpecialServiceType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SpecialServiceType')
            value_ = self.gds_validate_string(value_, node, 'SpecialServiceType')
            self.SpecialServiceType = value_
            self.SpecialServiceType_nsprefix_ = child_.prefix
        elif nodeName_ == 'LocalServiceType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LocalServiceType')
            value_ = self.gds_validate_string(value_, node, 'LocalServiceType')
            self.LocalServiceType.append(value_)
            self.LocalServiceType_nsprefix_ = child_.prefix
        elif nodeName_ == 'CombRSrv':
            obj_ = CombRSrvType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CombRSrv.append(obj_)
            obj_.original_tagname_ = 'CombRSrv'
# end class VldSrvCombType


class CombRSrvType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, RestrictedSpecialServiceType=None, RestrictedLocalServiceType=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.RestrictedSpecialServiceType = RestrictedSpecialServiceType
        self.RestrictedSpecialServiceType_nsprefix_ = None
        if RestrictedLocalServiceType is None:
            self.RestrictedLocalServiceType = []
        else:
            self.RestrictedLocalServiceType = RestrictedLocalServiceType
        self.RestrictedLocalServiceType_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CombRSrvType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CombRSrvType.subclass:
            return CombRSrvType.subclass(*args_, **kwargs_)
        else:
            return CombRSrvType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_RestrictedSpecialServiceType(self):
        return self.RestrictedSpecialServiceType
    def set_RestrictedSpecialServiceType(self, RestrictedSpecialServiceType):
        self.RestrictedSpecialServiceType = RestrictedSpecialServiceType
    def get_RestrictedLocalServiceType(self):
        return self.RestrictedLocalServiceType
    def set_RestrictedLocalServiceType(self, RestrictedLocalServiceType):
        self.RestrictedLocalServiceType = RestrictedLocalServiceType
    def add_RestrictedLocalServiceType(self, value):
        self.RestrictedLocalServiceType.append(value)
    def insert_RestrictedLocalServiceType_at(self, index, value):
        self.RestrictedLocalServiceType.insert(index, value)
    def replace_RestrictedLocalServiceType_at(self, index, value):
        self.RestrictedLocalServiceType[index] = value
    def _hasContent(self):
        if (
            self.RestrictedSpecialServiceType is not None or
            self.RestrictedLocalServiceType
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CombRSrvType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CombRSrvType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CombRSrvType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CombRSrvType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CombRSrvType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CombRSrvType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CombRSrvType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.RestrictedSpecialServiceType is not None:
            namespaceprefix_ = self.RestrictedSpecialServiceType_nsprefix_ + ':' if (UseCapturedNS_ and self.RestrictedSpecialServiceType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRestrictedSpecialServiceType>%s</%sRestrictedSpecialServiceType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.RestrictedSpecialServiceType), input_name='RestrictedSpecialServiceType')), namespaceprefix_ , eol_))
        for RestrictedLocalServiceType_ in self.RestrictedLocalServiceType:
            namespaceprefix_ = self.RestrictedLocalServiceType_nsprefix_ + ':' if (UseCapturedNS_ and self.RestrictedLocalServiceType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRestrictedLocalServiceType>%s</%sRestrictedLocalServiceType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(RestrictedLocalServiceType_), input_name='RestrictedLocalServiceType')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'RestrictedSpecialServiceType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RestrictedSpecialServiceType')
            value_ = self.gds_validate_string(value_, node, 'RestrictedSpecialServiceType')
            self.RestrictedSpecialServiceType = value_
            self.RestrictedSpecialServiceType_nsprefix_ = child_.prefix
        elif nodeName_ == 'RestrictedLocalServiceType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'RestrictedLocalServiceType')
            value_ = self.gds_validate_string(value_, node, 'RestrictedLocalServiceType')
            self.RestrictedLocalServiceType.append(value_)
            self.RestrictedLocalServiceType_nsprefix_ = child_.prefix
# end class CombRSrvType


class ConditionType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ConditionCode=None, ConditionData=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ConditionCode = ConditionCode
        self.validate_ConditionCodeType(self.ConditionCode)
        self.ConditionCode_nsprefix_ = None
        self.ConditionData = ConditionData
        self.validate_ConditionDataType(self.ConditionData)
        self.ConditionData_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ConditionType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ConditionType.subclass:
            return ConditionType.subclass(*args_, **kwargs_)
        else:
            return ConditionType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ConditionCode(self):
        return self.ConditionCode
    def set_ConditionCode(self, ConditionCode):
        self.ConditionCode = ConditionCode
    def get_ConditionData(self):
        return self.ConditionData
    def set_ConditionData(self, ConditionData):
        self.ConditionData = ConditionData
    def validate_ConditionCodeType(self, value):
        result = True
        # Validate type ConditionCodeType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ConditionCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on ConditionCodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ConditionDataType(self, value):
        result = True
        # Validate type ConditionDataType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def _hasContent(self):
        if (
            self.ConditionCode is not None or
            self.ConditionData is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ConditionType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ConditionType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ConditionType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ConditionType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ConditionType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ConditionType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ConditionType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ConditionCode is not None:
            namespaceprefix_ = self.ConditionCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ConditionCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sConditionCode>%s</%sConditionCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ConditionCode), input_name='ConditionCode')), namespaceprefix_ , eol_))
        if self.ConditionData is not None:
            namespaceprefix_ = self.ConditionData_nsprefix_ + ':' if (UseCapturedNS_ and self.ConditionData_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sConditionData>%s</%sConditionData>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ConditionData), input_name='ConditionData')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'ConditionCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ConditionCode')
            value_ = self.gds_validate_string(value_, node, 'ConditionCode')
            self.ConditionCode = value_
            self.ConditionCode_nsprefix_ = child_.prefix
            # validate type ConditionCodeType
            self.validate_ConditionCodeType(self.ConditionCode)
        elif nodeName_ == 'ConditionData':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ConditionData')
            value_ = self.gds_validate_string(value_, node, 'ConditionData')
            self.ConditionData = value_
            self.ConditionData_nsprefix_ = child_.prefix
            # validate type ConditionDataType
            self.validate_ConditionDataType(self.ConditionData)
# end class ConditionType


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
        rootTag = 'DCTResponseDataTypes'
        rootClass = DCTResponseDataTypes
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
        rootTag = 'DCTResponseDataTypes'
        rootClass = DCTResponseDataTypes
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
        rootTag = 'DCTResponseDataTypes'
        rootClass = DCTResponseDataTypes
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
        rootTag = 'DCTResponseDataTypes'
        rootClass = DCTResponseDataTypes
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from dct_responsedatatypes_global import *\n\n')
        sys.stdout.write('import dct_responsedatatypes_global as model_\n\n')
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
NamespaceToDefMappings_ = {'http://www.dhl.com/DCTResponsedatatypes': [('QuotedWeight',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'ST'),
                                             ('QuotedWeightUOM',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'ST'),
                                             ('OrgnSvcAreaType',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT'),
                                             ('DestSvcAreaType',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT'),
                                             ('BkgDetailsType',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT'),
                                             ('SrvCombType',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT'),
                                             ('ProdType',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT'),
                                             ('NoteType',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT'),
                                             ('QtdShpExChrgType',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT'),
                                             ('WeightChargeTaxDetType',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT'),
                                             ('ChargeTaxAmountDetType',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT'),
                                             ('QtdSInAdCurType',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT'),
                                             ('QtdSExtrChrgInAdCurType',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT'),
                                             ('QtdShpType',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT'),
                                             ('MrkSrvType',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT'),
                                             ('ProdNtwrkType',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT'),
                                             ('SrvType',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT'),
                                             ('SBTPType',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT'),
                                             ('DeliveryDate',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT'),
                                             ('WeightChargeDisc',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT'),
                                             ('QtdShpExChrgDisc',
                                              './schemas/DCTResponsedatatypes_global.xsd',
                                              'CT')]}

__all__ = [
    "BkgDetailsType",
    "ChargeTaxAmountDetType",
    "CombRSrvType",
    "ConditionType",
    "DCTResponseDataTypes",
    "DeliveryDate",
    "DestSvcAreaType",
    "MrkSrvType",
    "NoteType",
    "OrgnSvcAreaType",
    "ProdNtwrkType",
    "ProdType",
    "QtdSExtrChrgInAdCurType",
    "QtdSInAdCurType",
    "QtdShpExChrgDisc",
    "QtdShpExChrgType",
    "QtdShpType",
    "SBTPType",
    "SrvCombType",
    "SrvCombType3",
    "SrvType",
    "VldSrvCombType",
    "WeightChargeDisc",
    "WeightChargeTaxDetType"
]
