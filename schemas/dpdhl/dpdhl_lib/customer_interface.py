#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Sat Apr 22 21:02:04 2023 by generateDS.py version 2.41.3.
# Python 3.10.6 (main, Mar 10 2023, 10:55:28) [GCC 11.3.0]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './dpdhl_lib/customer_interface.py')
#
# Command line arguments:
#   ./schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd
#
# Command line:
#   /home/kserver/Workspace/karrio/.venv/karrio/bin/generateDS --no-namespace-defs -o "./dpdhl_lib/customer_interface.py" ./schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd
#
# Current working directory (os.getcwd()):
#   dpdhl
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


class unitType(str, Enum):
    """unitType -- unit for all measures
    
    """
    MM='mm'
    INCH='inch'


class EKP(GeneratedsSuper):
    """EKP -- First 10 digit number extract from the 14 digit DHL Account Number.
    E.g. if DHL Account Number is "5000000008 72 01" then EKP is equal to 5000000008.
    
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
                CurrentSubclassModule_, EKP)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EKP.subclass:
            return EKP.subclass(*args_, **kwargs_)
        else:
            return EKP(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_EKP(self, value):
        result = True
        # Validate type EKP, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EKP', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EKP')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EKP':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EKP')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='EKP', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EKP'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='EKP', fromsubclass_=False, pretty_print=True):
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
# end class EKP


class partnerID(GeneratedsSuper):
    """partnerID -- Field has the partner id. I.e. the last 2 digit number extract from
    the 14 digit DHL Account Number. E.g. if DHL Account Number is "5000000008 72 01"
    then Attendance is 01.
    
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
                CurrentSubclassModule_, partnerID)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if partnerID.subclass:
            return partnerID.subclass(*args_, **kwargs_)
        else:
            return partnerID(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_partnerID(self, value):
        result = True
        # Validate type partnerID, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='partnerID', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('partnerID')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'partnerID':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='partnerID')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='partnerID', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='partnerID'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='partnerID', fromsubclass_=False, pretty_print=True):
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
# end class partnerID


class procedureID(GeneratedsSuper):
    """procedureID -- Procedure ID (part of account number).
    
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
                CurrentSubclassModule_, procedureID)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if procedureID.subclass:
            return procedureID.subclass(*args_, **kwargs_)
        else:
            return procedureID(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_procedureID(self, value):
        result = True
        # Validate type procedureID, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='procedureID', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('procedureID')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'procedureID':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='procedureID')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='procedureID', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='procedureID'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='procedureID', fromsubclass_=False, pretty_print=True):
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
# end class procedureID


class accountNumber(GeneratedsSuper):
    """accountNumber -- DHL account number (14 digits).
    
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
                CurrentSubclassModule_, accountNumber)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if accountNumber.subclass:
            return accountNumber.subclass(*args_, **kwargs_)
        else:
            return accountNumber(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_accountNumber(self, value):
        result = True
        # Validate type accountNumber, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='accountNumber', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('accountNumber')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'accountNumber':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='accountNumber')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='accountNumber', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='accountNumber'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='accountNumber', fromsubclass_=False, pretty_print=True):
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
# end class accountNumber


class accountNumberExpress(GeneratedsSuper):
    """accountNumberExpress -- Express AccountNumber (9 digits).
    
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
                CurrentSubclassModule_, accountNumberExpress)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if accountNumberExpress.subclass:
            return accountNumberExpress.subclass(*args_, **kwargs_)
        else:
            return accountNumberExpress(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_accountNumberExpress(self, value):
        result = True
        # Validate type accountNumberExpress, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='accountNumberExpress', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('accountNumberExpress')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'accountNumberExpress':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='accountNumberExpress')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='accountNumberExpress', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='accountNumberExpress'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='accountNumberExpress', fromsubclass_=False, pretty_print=True):
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
# end class accountNumberExpress


class identCode(GeneratedsSuper):
    """identCode -- Ident code number.
    
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
                CurrentSubclassModule_, identCode)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if identCode.subclass:
            return identCode.subclass(*args_, **kwargs_)
        else:
            return identCode(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_identCode(self, value):
        result = True
        # Validate type identCode, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='identCode', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('identCode')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'identCode':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='identCode')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='identCode', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='identCode'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='identCode', fromsubclass_=False, pretty_print=True):
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
# end class identCode


class licensePlate(GeneratedsSuper):
    """licensePlate -- License plate number.
    
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
                CurrentSubclassModule_, licensePlate)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if licensePlate.subclass:
            return licensePlate.subclass(*args_, **kwargs_)
        else:
            return licensePlate(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_licensePlate(self, value):
        result = True
        # Validate type licensePlate, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='licensePlate', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('licensePlate')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'licensePlate':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='licensePlate')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='licensePlate', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='licensePlate'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='licensePlate', fromsubclass_=False, pretty_print=True):
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
# end class licensePlate


class airwayBill(GeneratedsSuper):
    """airwayBill -- Airway bill number.
    
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
                CurrentSubclassModule_, airwayBill)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if airwayBill.subclass:
            return airwayBill.subclass(*args_, **kwargs_)
        else:
            return airwayBill(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_airwayBill(self, value):
        result = True
        # Validate type airwayBill, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='airwayBill', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('airwayBill')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'airwayBill':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='airwayBill')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='airwayBill', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='airwayBill'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='airwayBill', fromsubclass_=False, pretty_print=True):
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
# end class airwayBill


class routeCode(GeneratedsSuper):
    """routeCode -- route code (default).
    
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
                CurrentSubclassModule_, routeCode)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if routeCode.subclass:
            return routeCode.subclass(*args_, **kwargs_)
        else:
            return routeCode(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_routeCode(self, value):
        result = True
        # Validate type routeCode, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='routeCode', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('routeCode')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'routeCode':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='routeCode')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='routeCode', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='routeCode'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='routeCode', fromsubclass_=False, pretty_print=True):
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
# end class routeCode


class routingCode(GeneratedsSuper):
    """routingCode --  The following barcode types are: 1. GS1 Barcode 2. ASC MH10 Barcode
    3. 2/5 Interleaved 4. Code 128 ( UPU )
    
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
                CurrentSubclassModule_, routingCode)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if routingCode.subclass:
            return routingCode.subclass(*args_, **kwargs_)
        else:
            return routingCode(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_routingCode(self, value):
        result = True
        # Validate type routingCode, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='routingCode', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('routingCode')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'routingCode':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='routingCode')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='routingCode', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='routingCode'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='routingCode', fromsubclass_=False, pretty_print=True):
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
# end class routingCode


class city(GeneratedsSuper):
    """city -- City name.
    
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
                CurrentSubclassModule_, city)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if city.subclass:
            return city.subclass(*args_, **kwargs_)
        else:
            return city(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_city(self, value):
        result = True
        # Validate type city, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='city', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('city')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'city':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='city')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='city', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='city'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='city', fromsubclass_=False, pretty_print=True):
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
# end class city


class province(GeneratedsSuper):
    """province -- Province name.
    
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
                CurrentSubclassModule_, province)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if province.subclass:
            return province.subclass(*args_, **kwargs_)
        else:
            return province(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_province(self, value):
        result = True
        # Validate type province, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='province', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('province')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'province':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='province')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='province', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='province'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='province', fromsubclass_=False, pretty_print=True):
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
# end class province


class streetNameCode(GeneratedsSuper):
    """streetNameCode -- Code for street name (part of routecode).
    
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
                CurrentSubclassModule_, streetNameCode)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if streetNameCode.subclass:
            return streetNameCode.subclass(*args_, **kwargs_)
        else:
            return streetNameCode(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_streetNameCode(self, value):
        result = True
        # Validate type streetNameCode, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='streetNameCode', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('streetNameCode')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'streetNameCode':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='streetNameCode')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='streetNameCode', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='streetNameCode'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='streetNameCode', fromsubclass_=False, pretty_print=True):
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
# end class streetNameCode


class streetNumberCode(GeneratedsSuper):
    """streetNumberCode -- Code for street number (part of routecode).
    
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
                CurrentSubclassModule_, streetNumberCode)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if streetNumberCode.subclass:
            return streetNumberCode.subclass(*args_, **kwargs_)
        else:
            return streetNumberCode(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_streetNumberCode(self, value):
        result = True
        # Validate type streetNumberCode, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='streetNumberCode', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('streetNumberCode')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'streetNumberCode':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='streetNumberCode')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='streetNumberCode', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='streetNumberCode'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='streetNumberCode', fromsubclass_=False, pretty_print=True):
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
# end class streetNumberCode


class Version(GeneratedsSuper):
    """Version -- The version of the webservice implementation for which the requesting
    client is developed.
    includes
    majorRelease -- The number of the major release. E.g. the '3' in version
    "3.2.".
    minorRelease -- The number of the minor release. E.g. the '3' in version
    "3.2.".
    build -- Optional build id to be addressed.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, majorRelease=None, minorRelease=None, build_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.majorRelease = majorRelease
        self.validate_majorReleaseType(self.majorRelease)
        self.majorRelease_nsprefix_ = None
        self.minorRelease = minorRelease
        self.validate_minorReleaseType(self.minorRelease)
        self.minorRelease_nsprefix_ = None
        self.build_ = build_
        self.validate_buildType(self.build_)
        self.build__nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Version)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Version.subclass:
            return Version.subclass(*args_, **kwargs_)
        else:
            return Version(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_majorRelease(self):
        return self.majorRelease
    def set_majorRelease(self, majorRelease):
        self.majorRelease = majorRelease
    def get_minorRelease(self):
        return self.minorRelease
    def set_minorRelease(self, minorRelease):
        self.minorRelease = minorRelease
    def get_build(self):
        return self.build_
    def set_build(self, build_):
        self.build_ = build_
    def validate_majorReleaseType(self, value):
        result = True
        # Validate type majorReleaseType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on majorReleaseType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_minorReleaseType(self, value):
        result = True
        # Validate type minorReleaseType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on minorReleaseType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_buildType(self, value):
        result = True
        # Validate type buildType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on buildType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.majorRelease is not None or
            self.minorRelease is not None or
            self.build_ is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Version', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Version')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Version':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Version')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Version', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Version'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Version', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.majorRelease is not None:
            namespaceprefix_ = self.majorRelease_nsprefix_ + ':' if (UseCapturedNS_ and self.majorRelease_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smajorRelease>%s</%smajorRelease>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.majorRelease), input_name='majorRelease')), namespaceprefix_ , eol_))
        if self.minorRelease is not None:
            namespaceprefix_ = self.minorRelease_nsprefix_ + ':' if (UseCapturedNS_ and self.minorRelease_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sminorRelease>%s</%sminorRelease>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.minorRelease), input_name='minorRelease')), namespaceprefix_ , eol_))
        if self.build_ is not None:
            namespaceprefix_ = self.build__nsprefix_ + ':' if (UseCapturedNS_ and self.build__nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sbuild>%s</%sbuild>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.build_), input_name='build')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'majorRelease':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'majorRelease')
            value_ = self.gds_validate_string(value_, node, 'majorRelease')
            self.majorRelease = value_
            self.majorRelease_nsprefix_ = child_.prefix
            # validate type majorReleaseType
            self.validate_majorReleaseType(self.majorRelease)
        elif nodeName_ == 'minorRelease':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'minorRelease')
            value_ = self.gds_validate_string(value_, node, 'minorRelease')
            self.minorRelease = value_
            self.minorRelease_nsprefix_ = child_.prefix
            # validate type minorReleaseType
            self.validate_minorReleaseType(self.minorRelease)
        elif nodeName_ == 'build':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'build')
            value_ = self.gds_validate_string(value_, node, 'build')
            self.build_ = value_
            self.build_nsprefix_ = child_.prefix
            # validate type buildType
            self.validate_buildType(self.build_)
# end class Version


class AuthentificationType(GeneratedsSuper):
    """AuthentificationType -- Type of authentification
    includes
    user -- username for the business customer portal (only lower case)
    signature -- password for the business customer portal
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, user=None, signature=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.user = user
        self.validate_userType(self.user)
        self.user_nsprefix_ = None
        self.signature = signature
        self.validate_signatureType(self.signature)
        self.signature_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AuthentificationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AuthentificationType.subclass:
            return AuthentificationType.subclass(*args_, **kwargs_)
        else:
            return AuthentificationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_user(self):
        return self.user
    def set_user(self, user):
        self.user = user
    def get_signature(self):
        return self.signature
    def set_signature(self, signature):
        self.signature = signature
    def validate_userType(self, value):
        result = True
        # Validate type userType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            pass
        return result
    def validate_signatureType(self, value):
        result = True
        # Validate type signatureType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 32:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on signatureType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.user is not None or
            self.signature is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AuthentificationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AuthentificationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AuthentificationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AuthentificationType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AuthentificationType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AuthentificationType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AuthentificationType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.user is not None:
            namespaceprefix_ = self.user_nsprefix_ + ':' if (UseCapturedNS_ and self.user_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%suser>%s</%suser>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.user), input_name='user')), namespaceprefix_ , eol_))
        if self.signature is not None:
            namespaceprefix_ = self.signature_nsprefix_ + ':' if (UseCapturedNS_ and self.signature_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssignature>%s</%ssignature>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.signature), input_name='signature')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'user':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'user')
            value_ = self.gds_validate_string(value_, node, 'user')
            self.user = value_
            self.user_nsprefix_ = child_.prefix
            # validate type userType
            self.validate_userType(self.user)
        elif nodeName_ == 'signature':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'signature')
            value_ = self.gds_validate_string(value_, node, 'signature')
            self.signature = value_
            self.signature_nsprefix_ = child_.prefix
            # validate type signatureType
            self.validate_signatureType(self.signature)
# end class AuthentificationType


class NativeAddressType(GeneratedsSuper):
    """NativeAddressType -- Type of native address
    includes
    streetName -- The name of the street. Optionally the house number can be
    passed in this field too. In this case the field "streetNumber" must not be
    present.
    streetNumber -- The house number. This field is only optional when the house
    number is passed with the field streetName.
    addressAddition -- Address addon, is only printed in the international area
    (V53WPAK)
    dispatchingInformation -- DispatchingInformation, is only printed in the international
    area (V53WPAK)
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, streetName=None, streetNumber=None, addressAddition=None, dispatchingInformation=None, zip=None, city=None, province=None, Origin=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.streetName = streetName
        self.validate_streetNameType(self.streetName)
        self.streetName_nsprefix_ = None
        self.streetNumber = streetNumber
        self.validate_streetNumberType(self.streetNumber)
        self.streetNumber_nsprefix_ = None
        if addressAddition is None:
            self.addressAddition = []
        else:
            self.addressAddition = addressAddition
        self.addressAddition_nsprefix_ = None
        self.dispatchingInformation = dispatchingInformation
        self.validate_dispatchingInformationType(self.dispatchingInformation)
        self.dispatchingInformation_nsprefix_ = None
        self.zip = zip
        self.zip_nsprefix_ = "cis"
        self.city = city
        self.validate_city(self.city)
        self.city_nsprefix_ = "cis"
        self.province = province
        self.validate_province(self.province)
        self.province_nsprefix_ = "cis"
        self.Origin = Origin
        self.Origin_nsprefix_ = "cis"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, NativeAddressType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if NativeAddressType.subclass:
            return NativeAddressType.subclass(*args_, **kwargs_)
        else:
            return NativeAddressType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_streetName(self):
        return self.streetName
    def set_streetName(self, streetName):
        self.streetName = streetName
    def get_streetNumber(self):
        return self.streetNumber
    def set_streetNumber(self, streetNumber):
        self.streetNumber = streetNumber
    def get_addressAddition(self):
        return self.addressAddition
    def set_addressAddition(self, addressAddition):
        self.addressAddition = addressAddition
    def add_addressAddition(self, value):
        self.addressAddition.append(value)
    def insert_addressAddition_at(self, index, value):
        self.addressAddition.insert(index, value)
    def replace_addressAddition_at(self, index, value):
        self.addressAddition[index] = value
    def get_dispatchingInformation(self):
        return self.dispatchingInformation
    def set_dispatchingInformation(self, dispatchingInformation):
        self.dispatchingInformation = dispatchingInformation
    def get_zip(self):
        return self.zip
    def set_zip(self, zip):
        self.zip = zip
    def get_city(self):
        return self.city
    def set_city(self, city):
        self.city = city
    def get_province(self):
        return self.province
    def set_province(self, province):
        self.province = province
    def get_Origin(self):
        return self.Origin
    def set_Origin(self, Origin):
        self.Origin = Origin
    def validate_streetNameType(self, value):
        result = True
        # Validate type streetNameType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_streetNumberType(self, value):
        result = True
        # Validate type streetNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_addressAdditionType(self, value):
        result = True
        # Validate type addressAdditionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on addressAdditionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_dispatchingInformationType(self, value):
        result = True
        # Validate type dispatchingInformationType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on dispatchingInformationType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_city(self, value):
        result = True
        # Validate type city, a restriction on xs:string.
        pass
        return result
    def validate_province(self, value):
        result = True
        # Validate type province, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.streetName is not None or
            self.streetNumber is not None or
            self.addressAddition or
            self.dispatchingInformation is not None or
            self.zip is not None or
            self.city is not None or
            self.province is not None or
            self.Origin is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NativeAddressType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('NativeAddressType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'NativeAddressType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='NativeAddressType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='NativeAddressType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='NativeAddressType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NativeAddressType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.streetName is not None:
            namespaceprefix_ = self.streetName_nsprefix_ + ':' if (UseCapturedNS_ and self.streetName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstreetName>%s</%sstreetName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.streetName), input_name='streetName')), namespaceprefix_ , eol_))
        if self.streetNumber is not None:
            namespaceprefix_ = self.streetNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.streetNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstreetNumber>%s</%sstreetNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.streetNumber), input_name='streetNumber')), namespaceprefix_ , eol_))
        for addressAddition_ in self.addressAddition:
            namespaceprefix_ = self.addressAddition_nsprefix_ + ':' if (UseCapturedNS_ and self.addressAddition_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saddressAddition>%s</%saddressAddition>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(addressAddition_), input_name='addressAddition')), namespaceprefix_ , eol_))
        if self.dispatchingInformation is not None:
            namespaceprefix_ = self.dispatchingInformation_nsprefix_ + ':' if (UseCapturedNS_ and self.dispatchingInformation_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdispatchingInformation>%s</%sdispatchingInformation>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.dispatchingInformation), input_name='dispatchingInformation')), namespaceprefix_ , eol_))
        if self.zip is not None:
            namespaceprefix_ = self.zip_nsprefix_ + ':' if (UseCapturedNS_ and self.zip_nsprefix_) else ''
            self.zip.export(outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='zip', pretty_print=pretty_print)
        if self.city is not None:
            namespaceprefix_ = self.city_nsprefix_ + ':' if (UseCapturedNS_ and self.city_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scity>%s</%scity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.city), input_name='city')), namespaceprefix_ , eol_))
        if self.province is not None:
            namespaceprefix_ = self.province_nsprefix_ + ':' if (UseCapturedNS_ and self.province_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sprovince>%s</%sprovince>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.province), input_name='province')), namespaceprefix_ , eol_))
        if self.Origin is not None:
            namespaceprefix_ = self.Origin_nsprefix_ + ':' if (UseCapturedNS_ and self.Origin_nsprefix_) else ''
            self.Origin.export(outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='Origin', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        elif nodeName_ == 'streetNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'streetNumber')
            value_ = self.gds_validate_string(value_, node, 'streetNumber')
            self.streetNumber = value_
            self.streetNumber_nsprefix_ = child_.prefix
            # validate type streetNumberType
            self.validate_streetNumberType(self.streetNumber)
        elif nodeName_ == 'addressAddition':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'addressAddition')
            value_ = self.gds_validate_string(value_, node, 'addressAddition')
            self.addressAddition.append(value_)
            self.addressAddition_nsprefix_ = child_.prefix
            # validate type addressAdditionType
            self.validate_addressAdditionType(self.addressAddition[-1])
        elif nodeName_ == 'dispatchingInformation':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'dispatchingInformation')
            value_ = self.gds_validate_string(value_, node, 'dispatchingInformation')
            self.dispatchingInformation = value_
            self.dispatchingInformation_nsprefix_ = child_.prefix
            # validate type dispatchingInformationType
            self.validate_dispatchingInformationType(self.dispatchingInformation)
        elif nodeName_ == 'zip':
            obj_ = ZipType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.zip = obj_
            obj_.original_tagname_ = 'zip'
        elif nodeName_ == 'city':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'city')
            value_ = self.gds_validate_string(value_, node, 'city')
            self.city = value_
            self.city_nsprefix_ = child_.prefix
            # validate type city
            self.validate_city(self.city)
        elif nodeName_ == 'province':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'province')
            value_ = self.gds_validate_string(value_, node, 'province')
            self.province = value_
            self.province_nsprefix_ = child_.prefix
            # validate type province
            self.validate_province(self.province)
        elif nodeName_ == 'Origin':
            obj_ = CountryType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Origin = obj_
            obj_.original_tagname_ = 'Origin'
# end class NativeAddressType


class NativeAddressTypeNew(GeneratedsSuper):
    """NativeAddressTypeNew -- Type of native address
    includes
    streetName -- The name of the street. Optionally the house number can be
    passed in this field too. In this case the field "streetNumber" must not be
    present.
    streetNumber -- The house number. This field is only optional when the house
    number is passed with the field streetName.
    Origin -- Country.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, streetName=None, streetNumber=None, zip=None, city=None, Origin=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.streetName = streetName
        self.validate_streetNameType1(self.streetName)
        self.streetName_nsprefix_ = None
        self.streetNumber = streetNumber
        self.validate_streetNumberType2(self.streetNumber)
        self.streetNumber_nsprefix_ = None
        self.zip = zip
        self.zip_nsprefix_ = "cis"
        self.city = city
        self.validate_city(self.city)
        self.city_nsprefix_ = "cis"
        self.Origin = Origin
        self.Origin_nsprefix_ = "cis"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, NativeAddressTypeNew)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if NativeAddressTypeNew.subclass:
            return NativeAddressTypeNew.subclass(*args_, **kwargs_)
        else:
            return NativeAddressTypeNew(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_streetName(self):
        return self.streetName
    def set_streetName(self, streetName):
        self.streetName = streetName
    def get_streetNumber(self):
        return self.streetNumber
    def set_streetNumber(self, streetNumber):
        self.streetNumber = streetNumber
    def get_zip(self):
        return self.zip
    def set_zip(self, zip):
        self.zip = zip
    def get_city(self):
        return self.city
    def set_city(self, city):
        self.city = city
    def get_Origin(self):
        return self.Origin
    def set_Origin(self, Origin):
        self.Origin = Origin
    def validate_streetNameType1(self, value):
        result = True
        # Validate type streetNameType1, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetNameType1' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_streetNumberType2(self, value):
        result = True
        # Validate type streetNumberType2, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetNumberType2' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_city(self, value):
        result = True
        # Validate type city, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.streetName is not None or
            self.streetNumber is not None or
            self.zip is not None or
            self.city is not None or
            self.Origin is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NativeAddressTypeNew', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('NativeAddressTypeNew')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'NativeAddressTypeNew':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='NativeAddressTypeNew')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='NativeAddressTypeNew', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='NativeAddressTypeNew'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NativeAddressTypeNew', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.streetName is not None:
            namespaceprefix_ = self.streetName_nsprefix_ + ':' if (UseCapturedNS_ and self.streetName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstreetName>%s</%sstreetName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.streetName), input_name='streetName')), namespaceprefix_ , eol_))
        if self.streetNumber is not None:
            namespaceprefix_ = self.streetNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.streetNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstreetNumber>%s</%sstreetNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.streetNumber), input_name='streetNumber')), namespaceprefix_ , eol_))
        if self.zip is not None:
            namespaceprefix_ = self.zip_nsprefix_ + ':' if (UseCapturedNS_ and self.zip_nsprefix_) else ''
            self.zip.export(outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='zip', pretty_print=pretty_print)
        if self.city is not None:
            namespaceprefix_ = self.city_nsprefix_ + ':' if (UseCapturedNS_ and self.city_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scity>%s</%scity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.city), input_name='city')), namespaceprefix_ , eol_))
        if self.Origin is not None:
            namespaceprefix_ = self.Origin_nsprefix_ + ':' if (UseCapturedNS_ and self.Origin_nsprefix_) else ''
            self.Origin.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Origin', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
            # validate type streetNameType1
            self.validate_streetNameType1(self.streetName)
        elif nodeName_ == 'streetNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'streetNumber')
            value_ = self.gds_validate_string(value_, node, 'streetNumber')
            self.streetNumber = value_
            self.streetNumber_nsprefix_ = child_.prefix
            # validate type streetNumberType2
            self.validate_streetNumberType2(self.streetNumber)
        elif nodeName_ == 'zip':
            obj_ = ZipType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.zip = obj_
            obj_.original_tagname_ = 'zip'
        elif nodeName_ == 'city':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'city')
            value_ = self.gds_validate_string(value_, node, 'city')
            self.city = value_
            self.city_nsprefix_ = child_.prefix
            # validate type city
            self.validate_city(self.city)
        elif nodeName_ == 'Origin':
            obj_ = CountryType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Origin = obj_
            obj_.original_tagname_ = 'Origin'
# end class NativeAddressTypeNew


class ReceiverNativeAddressType(GeneratedsSuper):
    """streetName -- The name of the street. Optionally the house number can be
    passed in this field too. In this case the field "streetNumber" must not be
    present.
    streetNumber -- The house number. This field is only optional when the house
    number is passed with the field streetName.
    addressAddition -- Address addon, is only printed in the international area
    (V53WPAK)
    dispatchingInformation -- DispatchingInformation, is only printed in the international
    area (V53WPAK)
    Origin -- Country.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, name2=None, name3=None, streetName=None, streetNumber=None, addressAddition=None, dispatchingInformation=None, zip=None, city=None, province=None, Origin=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name2 = name2
        self.validate_name2(self.name2)
        self.name2_nsprefix_ = "cis"
        self.name3 = name3
        self.validate_name3(self.name3)
        self.name3_nsprefix_ = "cis"
        self.streetName = streetName
        self.validate_streetNameType3(self.streetName)
        self.streetName_nsprefix_ = None
        self.streetNumber = streetNumber
        self.validate_streetNumberType4(self.streetNumber)
        self.streetNumber_nsprefix_ = None
        if addressAddition is None:
            self.addressAddition = []
        else:
            self.addressAddition = addressAddition
        self.addressAddition_nsprefix_ = None
        self.dispatchingInformation = dispatchingInformation
        self.validate_dispatchingInformationType6(self.dispatchingInformation)
        self.dispatchingInformation_nsprefix_ = None
        self.zip = zip
        self.zip_nsprefix_ = "cis"
        self.city = city
        self.validate_city(self.city)
        self.city_nsprefix_ = "cis"
        self.province = province
        self.validate_province(self.province)
        self.province_nsprefix_ = "cis"
        self.Origin = Origin
        self.Origin_nsprefix_ = "cis"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ReceiverNativeAddressType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ReceiverNativeAddressType.subclass:
            return ReceiverNativeAddressType.subclass(*args_, **kwargs_)
        else:
            return ReceiverNativeAddressType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_name2(self):
        return self.name2
    def set_name2(self, name2):
        self.name2 = name2
    def get_name3(self):
        return self.name3
    def set_name3(self, name3):
        self.name3 = name3
    def get_streetName(self):
        return self.streetName
    def set_streetName(self, streetName):
        self.streetName = streetName
    def get_streetNumber(self):
        return self.streetNumber
    def set_streetNumber(self, streetNumber):
        self.streetNumber = streetNumber
    def get_addressAddition(self):
        return self.addressAddition
    def set_addressAddition(self, addressAddition):
        self.addressAddition = addressAddition
    def add_addressAddition(self, value):
        self.addressAddition.append(value)
    def insert_addressAddition_at(self, index, value):
        self.addressAddition.insert(index, value)
    def replace_addressAddition_at(self, index, value):
        self.addressAddition[index] = value
    def get_dispatchingInformation(self):
        return self.dispatchingInformation
    def set_dispatchingInformation(self, dispatchingInformation):
        self.dispatchingInformation = dispatchingInformation
    def get_zip(self):
        return self.zip
    def set_zip(self, zip):
        self.zip = zip
    def get_city(self):
        return self.city
    def set_city(self, city):
        self.city = city
    def get_province(self):
        return self.province
    def set_province(self, province):
        self.province = province
    def get_Origin(self):
        return self.Origin
    def set_Origin(self, Origin):
        self.Origin = Origin
    def validate_name2(self, value):
        result = True
        # Validate type name2, a restriction on xs:string.
        pass
        return result
    def validate_name3(self, value):
        result = True
        # Validate type name3, a restriction on xs:string.
        pass
        return result
    def validate_streetNameType3(self, value):
        result = True
        # Validate type streetNameType3, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetNameType3' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_streetNumberType4(self, value):
        result = True
        # Validate type streetNumberType4, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetNumberType4' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_addressAdditionType5(self, value):
        result = True
        # Validate type addressAdditionType5, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on addressAdditionType5' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_dispatchingInformationType6(self, value):
        result = True
        # Validate type dispatchingInformationType6, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on dispatchingInformationType6' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_city(self, value):
        result = True
        # Validate type city, a restriction on xs:string.
        pass
        return result
    def validate_province(self, value):
        result = True
        # Validate type province, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.name2 is not None or
            self.name3 is not None or
            self.streetName is not None or
            self.streetNumber is not None or
            self.addressAddition or
            self.dispatchingInformation is not None or
            self.zip is not None or
            self.city is not None or
            self.province is not None or
            self.Origin is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReceiverNativeAddressType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ReceiverNativeAddressType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ReceiverNativeAddressType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ReceiverNativeAddressType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ReceiverNativeAddressType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ReceiverNativeAddressType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReceiverNativeAddressType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.name2 is not None:
            namespaceprefix_ = self.name2_nsprefix_ + ':' if (UseCapturedNS_ and self.name2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sname2>%s</%sname2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.name2), input_name='name2')), namespaceprefix_ , eol_))
        if self.name3 is not None:
            namespaceprefix_ = self.name3_nsprefix_ + ':' if (UseCapturedNS_ and self.name3_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sname3>%s</%sname3>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.name3), input_name='name3')), namespaceprefix_ , eol_))
        if self.streetName is not None:
            namespaceprefix_ = self.streetName_nsprefix_ + ':' if (UseCapturedNS_ and self.streetName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstreetName>%s</%sstreetName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.streetName), input_name='streetName')), namespaceprefix_ , eol_))
        if self.streetNumber is not None:
            namespaceprefix_ = self.streetNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.streetNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstreetNumber>%s</%sstreetNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.streetNumber), input_name='streetNumber')), namespaceprefix_ , eol_))
        for addressAddition_ in self.addressAddition:
            namespaceprefix_ = self.addressAddition_nsprefix_ + ':' if (UseCapturedNS_ and self.addressAddition_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saddressAddition>%s</%saddressAddition>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(addressAddition_), input_name='addressAddition')), namespaceprefix_ , eol_))
        if self.dispatchingInformation is not None:
            namespaceprefix_ = self.dispatchingInformation_nsprefix_ + ':' if (UseCapturedNS_ and self.dispatchingInformation_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdispatchingInformation>%s</%sdispatchingInformation>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.dispatchingInformation), input_name='dispatchingInformation')), namespaceprefix_ , eol_))
        if self.zip is not None:
            namespaceprefix_ = self.zip_nsprefix_ + ':' if (UseCapturedNS_ and self.zip_nsprefix_) else ''
            self.zip.export(outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='zip', pretty_print=pretty_print)
        if self.city is not None:
            namespaceprefix_ = self.city_nsprefix_ + ':' if (UseCapturedNS_ and self.city_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scity>%s</%scity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.city), input_name='city')), namespaceprefix_ , eol_))
        if self.province is not None:
            namespaceprefix_ = self.province_nsprefix_ + ':' if (UseCapturedNS_ and self.province_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sprovince>%s</%sprovince>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.province), input_name='province')), namespaceprefix_ , eol_))
        if self.Origin is not None:
            namespaceprefix_ = self.Origin_nsprefix_ + ':' if (UseCapturedNS_ and self.Origin_nsprefix_) else ''
            self.Origin.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Origin', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'name2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'name2')
            value_ = self.gds_validate_string(value_, node, 'name2')
            self.name2 = value_
            self.name2_nsprefix_ = child_.prefix
            # validate type name2
            self.validate_name2(self.name2)
        elif nodeName_ == 'name3':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'name3')
            value_ = self.gds_validate_string(value_, node, 'name3')
            self.name3 = value_
            self.name3_nsprefix_ = child_.prefix
            # validate type name3
            self.validate_name3(self.name3)
        elif nodeName_ == 'streetName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'streetName')
            value_ = self.gds_validate_string(value_, node, 'streetName')
            self.streetName = value_
            self.streetName_nsprefix_ = child_.prefix
            # validate type streetNameType3
            self.validate_streetNameType3(self.streetName)
        elif nodeName_ == 'streetNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'streetNumber')
            value_ = self.gds_validate_string(value_, node, 'streetNumber')
            self.streetNumber = value_
            self.streetNumber_nsprefix_ = child_.prefix
            # validate type streetNumberType4
            self.validate_streetNumberType4(self.streetNumber)
        elif nodeName_ == 'addressAddition':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'addressAddition')
            value_ = self.gds_validate_string(value_, node, 'addressAddition')
            self.addressAddition.append(value_)
            self.addressAddition_nsprefix_ = child_.prefix
            # validate type addressAdditionType5
            self.validate_addressAdditionType5(self.addressAddition[-1])
        elif nodeName_ == 'dispatchingInformation':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'dispatchingInformation')
            value_ = self.gds_validate_string(value_, node, 'dispatchingInformation')
            self.dispatchingInformation = value_
            self.dispatchingInformation_nsprefix_ = child_.prefix
            # validate type dispatchingInformationType6
            self.validate_dispatchingInformationType6(self.dispatchingInformation)
        elif nodeName_ == 'zip':
            obj_ = ZipType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.zip = obj_
            obj_.original_tagname_ = 'zip'
        elif nodeName_ == 'city':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'city')
            value_ = self.gds_validate_string(value_, node, 'city')
            self.city = value_
            self.city_nsprefix_ = child_.prefix
            # validate type city
            self.validate_city(self.city)
        elif nodeName_ == 'province':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'province')
            value_ = self.gds_validate_string(value_, node, 'province')
            self.province = value_
            self.province_nsprefix_ = child_.prefix
            # validate type province
            self.validate_province(self.province)
        elif nodeName_ == 'Origin':
            obj_ = CountryType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Origin = obj_
            obj_.original_tagname_ = 'Origin'
# end class ReceiverNativeAddressType


class PickupAddressType(GeneratedsSuper):
    """PickupAddressType -- Type of pickup address
    includes
    can be
    NativeAddress -- Default address
    PackStation -- Packstation address
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, NativeAddress=None, PackStation=None, streetNameCode=None, streetNumberCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.NativeAddress = NativeAddress
        self.NativeAddress_nsprefix_ = "cis"
        self.PackStation = PackStation
        self.PackStation_nsprefix_ = "cis"
        self.streetNameCode = streetNameCode
        self.validate_streetNameCode(self.streetNameCode)
        self.streetNameCode_nsprefix_ = "cis"
        self.streetNumberCode = streetNumberCode
        self.validate_streetNumberCode(self.streetNumberCode)
        self.streetNumberCode_nsprefix_ = "cis"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PickupAddressType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PickupAddressType.subclass:
            return PickupAddressType.subclass(*args_, **kwargs_)
        else:
            return PickupAddressType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_NativeAddress(self):
        return self.NativeAddress
    def set_NativeAddress(self, NativeAddress):
        self.NativeAddress = NativeAddress
    def get_PackStation(self):
        return self.PackStation
    def set_PackStation(self, PackStation):
        self.PackStation = PackStation
    def get_streetNameCode(self):
        return self.streetNameCode
    def set_streetNameCode(self, streetNameCode):
        self.streetNameCode = streetNameCode
    def get_streetNumberCode(self):
        return self.streetNumberCode
    def set_streetNumberCode(self, streetNumberCode):
        self.streetNumberCode = streetNumberCode
    def validate_streetNameCode(self, value):
        result = True
        # Validate type streetNameCode, a restriction on xs:string.
        pass
        return result
    def validate_streetNumberCode(self, value):
        result = True
        # Validate type streetNumberCode, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.NativeAddress is not None or
            self.PackStation is not None or
            self.streetNameCode is not None or
            self.streetNumberCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupAddressType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PickupAddressType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PickupAddressType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PickupAddressType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PickupAddressType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PickupAddressType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupAddressType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.NativeAddress is not None:
            namespaceprefix_ = self.NativeAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.NativeAddress_nsprefix_) else ''
            self.NativeAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='NativeAddress', pretty_print=pretty_print)
        if self.PackStation is not None:
            namespaceprefix_ = self.PackStation_nsprefix_ + ':' if (UseCapturedNS_ and self.PackStation_nsprefix_) else ''
            self.PackStation.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PackStation', pretty_print=pretty_print)
        if self.streetNameCode is not None:
            namespaceprefix_ = self.streetNameCode_nsprefix_ + ':' if (UseCapturedNS_ and self.streetNameCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstreetNameCode>%s</%sstreetNameCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.streetNameCode), input_name='streetNameCode')), namespaceprefix_ , eol_))
        if self.streetNumberCode is not None:
            namespaceprefix_ = self.streetNumberCode_nsprefix_ + ':' if (UseCapturedNS_ and self.streetNumberCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstreetNumberCode>%s</%sstreetNumberCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.streetNumberCode), input_name='streetNumberCode')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'NativeAddress':
            obj_ = NativeAddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.NativeAddress = obj_
            obj_.original_tagname_ = 'NativeAddress'
        elif nodeName_ == 'PackStation':
            obj_ = PackStationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PackStation = obj_
            obj_.original_tagname_ = 'PackStation'
        elif nodeName_ == 'streetNameCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'streetNameCode')
            value_ = self.gds_validate_string(value_, node, 'streetNameCode')
            self.streetNameCode = value_
            self.streetNameCode_nsprefix_ = child_.prefix
            # validate type streetNameCode
            self.validate_streetNameCode(self.streetNameCode)
        elif nodeName_ == 'streetNumberCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'streetNumberCode')
            value_ = self.gds_validate_string(value_, node, 'streetNumberCode')
            self.streetNumberCode = value_
            self.streetNumberCode_nsprefix_ = child_.prefix
            # validate type streetNumberCode
            self.validate_streetNumberCode(self.streetNumberCode)
# end class PickupAddressType


class DeliveryAddressType(GeneratedsSuper):
    """DeliveryAddressType -- Type of delivery address
    includes
    can be
    NativeAddress -- Default address
    PostOffice -- Postoffice address
    PackStation -- Packstation address
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, NativeAddress=None, PostOffice=None, PackStation=None, streetNameCode=None, streetNumberCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.NativeAddress = NativeAddress
        self.NativeAddress_nsprefix_ = "cis"
        self.PostOffice = PostOffice
        self.PostOffice_nsprefix_ = "cis"
        self.PackStation = PackStation
        self.PackStation_nsprefix_ = "cis"
        self.streetNameCode = streetNameCode
        self.validate_streetNameCode(self.streetNameCode)
        self.streetNameCode_nsprefix_ = "cis"
        self.streetNumberCode = streetNumberCode
        self.validate_streetNumberCode(self.streetNumberCode)
        self.streetNumberCode_nsprefix_ = "cis"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DeliveryAddressType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DeliveryAddressType.subclass:
            return DeliveryAddressType.subclass(*args_, **kwargs_)
        else:
            return DeliveryAddressType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_NativeAddress(self):
        return self.NativeAddress
    def set_NativeAddress(self, NativeAddress):
        self.NativeAddress = NativeAddress
    def get_PostOffice(self):
        return self.PostOffice
    def set_PostOffice(self, PostOffice):
        self.PostOffice = PostOffice
    def get_PackStation(self):
        return self.PackStation
    def set_PackStation(self, PackStation):
        self.PackStation = PackStation
    def get_streetNameCode(self):
        return self.streetNameCode
    def set_streetNameCode(self, streetNameCode):
        self.streetNameCode = streetNameCode
    def get_streetNumberCode(self):
        return self.streetNumberCode
    def set_streetNumberCode(self, streetNumberCode):
        self.streetNumberCode = streetNumberCode
    def validate_streetNameCode(self, value):
        result = True
        # Validate type streetNameCode, a restriction on xs:string.
        pass
        return result
    def validate_streetNumberCode(self, value):
        result = True
        # Validate type streetNumberCode, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.NativeAddress is not None or
            self.PostOffice is not None or
            self.PackStation is not None or
            self.streetNameCode is not None or
            self.streetNumberCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeliveryAddressType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DeliveryAddressType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DeliveryAddressType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DeliveryAddressType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DeliveryAddressType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DeliveryAddressType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeliveryAddressType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.NativeAddress is not None:
            namespaceprefix_ = self.NativeAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.NativeAddress_nsprefix_) else ''
            self.NativeAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='NativeAddress', pretty_print=pretty_print)
        if self.PostOffice is not None:
            namespaceprefix_ = self.PostOffice_nsprefix_ + ':' if (UseCapturedNS_ and self.PostOffice_nsprefix_) else ''
            self.PostOffice.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PostOffice', pretty_print=pretty_print)
        if self.PackStation is not None:
            namespaceprefix_ = self.PackStation_nsprefix_ + ':' if (UseCapturedNS_ and self.PackStation_nsprefix_) else ''
            self.PackStation.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PackStation', pretty_print=pretty_print)
        if self.streetNameCode is not None:
            namespaceprefix_ = self.streetNameCode_nsprefix_ + ':' if (UseCapturedNS_ and self.streetNameCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstreetNameCode>%s</%sstreetNameCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.streetNameCode), input_name='streetNameCode')), namespaceprefix_ , eol_))
        if self.streetNumberCode is not None:
            namespaceprefix_ = self.streetNumberCode_nsprefix_ + ':' if (UseCapturedNS_ and self.streetNumberCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstreetNumberCode>%s</%sstreetNumberCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.streetNumberCode), input_name='streetNumberCode')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'NativeAddress':
            obj_ = NativeAddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.NativeAddress = obj_
            obj_.original_tagname_ = 'NativeAddress'
        elif nodeName_ == 'PostOffice':
            obj_ = PostfilialeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PostOffice = obj_
            obj_.original_tagname_ = 'PostOffice'
        elif nodeName_ == 'PackStation':
            obj_ = PackStationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PackStation = obj_
            obj_.original_tagname_ = 'PackStation'
        elif nodeName_ == 'streetNameCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'streetNameCode')
            value_ = self.gds_validate_string(value_, node, 'streetNameCode')
            self.streetNameCode = value_
            self.streetNameCode_nsprefix_ = child_.prefix
            # validate type streetNameCode
            self.validate_streetNameCode(self.streetNameCode)
        elif nodeName_ == 'streetNumberCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'streetNumberCode')
            value_ = self.gds_validate_string(value_, node, 'streetNumberCode')
            self.streetNumberCode = value_
            self.streetNumberCode_nsprefix_ = child_.prefix
            # validate type streetNumberCode
            self.validate_streetNumberCode(self.streetNumberCode)
# end class DeliveryAddressType


class BankType(GeneratedsSuper):
    """BankType -- Type of bank information
    includes
    accountOwner -- Name of bank account owner.
    bankName -- Name of bank.
    iban -- IBAN code of bank account.
    note1 -- Purpose of bank information.
    note2 -- Purpose of bank information.
    bic -- Bank-Information-Code (BankCCL) of bank account.
    accountreference -- Accountreferece to customer profile
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, accountOwner=None, bankName=None, iban=None, note1=None, note2=None, bic=None, accountreference=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.accountOwner = accountOwner
        self.validate_accountOwnerType(self.accountOwner)
        self.accountOwner_nsprefix_ = None
        self.bankName = bankName
        self.validate_bankNameType(self.bankName)
        self.bankName_nsprefix_ = None
        self.iban = iban
        self.validate_ibanType(self.iban)
        self.iban_nsprefix_ = None
        self.note1 = note1
        self.validate_note1Type(self.note1)
        self.note1_nsprefix_ = None
        self.note2 = note2
        self.validate_note2Type(self.note2)
        self.note2_nsprefix_ = None
        self.bic = bic
        self.validate_bicType(self.bic)
        self.bic_nsprefix_ = None
        self.accountreference = accountreference
        self.validate_accountreferenceType(self.accountreference)
        self.accountreference_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, BankType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BankType.subclass:
            return BankType.subclass(*args_, **kwargs_)
        else:
            return BankType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_accountOwner(self):
        return self.accountOwner
    def set_accountOwner(self, accountOwner):
        self.accountOwner = accountOwner
    def get_bankName(self):
        return self.bankName
    def set_bankName(self, bankName):
        self.bankName = bankName
    def get_iban(self):
        return self.iban
    def set_iban(self, iban):
        self.iban = iban
    def get_note1(self):
        return self.note1
    def set_note1(self, note1):
        self.note1 = note1
    def get_note2(self):
        return self.note2
    def set_note2(self, note2):
        self.note2 = note2
    def get_bic(self):
        return self.bic
    def set_bic(self, bic):
        self.bic = bic
    def get_accountreference(self):
        return self.accountreference
    def set_accountreference(self, accountreference):
        self.accountreference = accountreference
    def validate_accountOwnerType(self, value):
        result = True
        # Validate type accountOwnerType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 80:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on accountOwnerType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_bankNameType(self, value):
        result = True
        # Validate type bankNameType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 80:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on bankNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ibanType(self, value):
        result = True
        # Validate type ibanType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 22:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ibanType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_note1Type(self, value):
        result = True
        # Validate type note1Type, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on note1Type' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_note2Type(self, value):
        result = True
        # Validate type note2Type, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on note2Type' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_bicType(self, value):
        result = True
        # Validate type bicType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 11:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on bicType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_accountreferenceType(self, value):
        result = True
        # Validate type accountreferenceType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on accountreferenceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.accountOwner is not None or
            self.bankName is not None or
            self.iban is not None or
            self.note1 is not None or
            self.note2 is not None or
            self.bic is not None or
            self.accountreference is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BankType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('BankType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'BankType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BankType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='BankType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='BankType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BankType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.accountOwner is not None:
            namespaceprefix_ = self.accountOwner_nsprefix_ + ':' if (UseCapturedNS_ and self.accountOwner_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saccountOwner>%s</%saccountOwner>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.accountOwner), input_name='accountOwner')), namespaceprefix_ , eol_))
        if self.bankName is not None:
            namespaceprefix_ = self.bankName_nsprefix_ + ':' if (UseCapturedNS_ and self.bankName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sbankName>%s</%sbankName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.bankName), input_name='bankName')), namespaceprefix_ , eol_))
        if self.iban is not None:
            namespaceprefix_ = self.iban_nsprefix_ + ':' if (UseCapturedNS_ and self.iban_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%siban>%s</%siban>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.iban), input_name='iban')), namespaceprefix_ , eol_))
        if self.note1 is not None:
            namespaceprefix_ = self.note1_nsprefix_ + ':' if (UseCapturedNS_ and self.note1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snote1>%s</%snote1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.note1), input_name='note1')), namespaceprefix_ , eol_))
        if self.note2 is not None:
            namespaceprefix_ = self.note2_nsprefix_ + ':' if (UseCapturedNS_ and self.note2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snote2>%s</%snote2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.note2), input_name='note2')), namespaceprefix_ , eol_))
        if self.bic is not None:
            namespaceprefix_ = self.bic_nsprefix_ + ':' if (UseCapturedNS_ and self.bic_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sbic>%s</%sbic>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.bic), input_name='bic')), namespaceprefix_ , eol_))
        if self.accountreference is not None:
            namespaceprefix_ = self.accountreference_nsprefix_ + ':' if (UseCapturedNS_ and self.accountreference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saccountreference>%s</%saccountreference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.accountreference), input_name='accountreference')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'accountOwner':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'accountOwner')
            value_ = self.gds_validate_string(value_, node, 'accountOwner')
            self.accountOwner = value_
            self.accountOwner_nsprefix_ = child_.prefix
            # validate type accountOwnerType
            self.validate_accountOwnerType(self.accountOwner)
        elif nodeName_ == 'bankName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'bankName')
            value_ = self.gds_validate_string(value_, node, 'bankName')
            self.bankName = value_
            self.bankName_nsprefix_ = child_.prefix
            # validate type bankNameType
            self.validate_bankNameType(self.bankName)
        elif nodeName_ == 'iban':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'iban')
            value_ = self.gds_validate_string(value_, node, 'iban')
            self.iban = value_
            self.iban_nsprefix_ = child_.prefix
            # validate type ibanType
            self.validate_ibanType(self.iban)
        elif nodeName_ == 'note1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'note1')
            value_ = self.gds_validate_string(value_, node, 'note1')
            self.note1 = value_
            self.note1_nsprefix_ = child_.prefix
            # validate type note1Type
            self.validate_note1Type(self.note1)
        elif nodeName_ == 'note2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'note2')
            value_ = self.gds_validate_string(value_, node, 'note2')
            self.note2 = value_
            self.note2_nsprefix_ = child_.prefix
            # validate type note2Type
            self.validate_note2Type(self.note2)
        elif nodeName_ == 'bic':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'bic')
            value_ = self.gds_validate_string(value_, node, 'bic')
            self.bic = value_
            self.bic_nsprefix_ = child_.prefix
            # validate type bicType
            self.validate_bicType(self.bic)
        elif nodeName_ == 'accountreference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'accountreference')
            value_ = self.gds_validate_string(value_, node, 'accountreference')
            self.accountreference = value_
            self.accountreference_nsprefix_ = child_.prefix
            # validate type accountreferenceType
            self.validate_accountreferenceType(self.accountreference)
# end class BankType


class NameType(GeneratedsSuper):
    """NameType -- Type of name
    includes
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, name1=None, name2=None, name3=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name1 = name1
        self.validate_name1(self.name1)
        self.name1_nsprefix_ = "cis"
        self.name2 = name2
        self.validate_name2(self.name2)
        self.name2_nsprefix_ = "cis"
        self.name3 = name3
        self.validate_name3(self.name3)
        self.name3_nsprefix_ = "cis"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, NameType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if NameType.subclass:
            return NameType.subclass(*args_, **kwargs_)
        else:
            return NameType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_name1(self):
        return self.name1
    def set_name1(self, name1):
        self.name1 = name1
    def get_name2(self):
        return self.name2
    def set_name2(self, name2):
        self.name2 = name2
    def get_name3(self):
        return self.name3
    def set_name3(self, name3):
        self.name3 = name3
    def validate_name1(self, value):
        result = True
        # Validate type name1, a restriction on xs:string.
        pass
        return result
    def validate_name2(self, value):
        result = True
        # Validate type name2, a restriction on xs:string.
        pass
        return result
    def validate_name3(self, value):
        result = True
        # Validate type name3, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.name1 is not None or
            self.name2 is not None or
            self.name3 is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NameType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('NameType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'NameType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='NameType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='NameType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='NameType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NameType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.name1 is not None:
            namespaceprefix_ = self.name1_nsprefix_ + ':' if (UseCapturedNS_ and self.name1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sname1>%s</%sname1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.name1), input_name='name1')), namespaceprefix_ , eol_))
        if self.name2 is not None:
            namespaceprefix_ = self.name2_nsprefix_ + ':' if (UseCapturedNS_ and self.name2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sname2>%s</%sname2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.name2), input_name='name2')), namespaceprefix_ , eol_))
        if self.name3 is not None:
            namespaceprefix_ = self.name3_nsprefix_ + ':' if (UseCapturedNS_ and self.name3_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sname3>%s</%sname3>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.name3), input_name='name3')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'name1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'name1')
            value_ = self.gds_validate_string(value_, node, 'name1')
            self.name1 = value_
            self.name1_nsprefix_ = child_.prefix
            # validate type name1
            self.validate_name1(self.name1)
        elif nodeName_ == 'name2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'name2')
            value_ = self.gds_validate_string(value_, node, 'name2')
            self.name2 = value_
            self.name2_nsprefix_ = child_.prefix
            # validate type name2
            self.validate_name2(self.name2)
        elif nodeName_ == 'name3':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'name3')
            value_ = self.gds_validate_string(value_, node, 'name3')
            self.name3 = value_
            self.name3_nsprefix_ = child_.prefix
            # validate type name3
            self.validate_name3(self.name3)
# end class NameType


class ReceiverNameType(GeneratedsSuper):
    """ReceiverNameType -- Type of name
    includes
    name -- Name of receiver (first part)
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, name=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name = name
        self.validate_nameType(self.name)
        self.name_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ReceiverNameType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ReceiverNameType.subclass:
            return ReceiverNameType.subclass(*args_, **kwargs_)
        else:
            return ReceiverNameType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def validate_nameType(self, value):
        result = True
        # Validate type nameType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on nameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.name is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReceiverNameType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ReceiverNameType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ReceiverNameType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ReceiverNameType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ReceiverNameType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ReceiverNameType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReceiverNameType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.name is not None:
            namespaceprefix_ = self.name_nsprefix_ + ':' if (UseCapturedNS_ and self.name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sname>%s</%sname>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.name), input_name='name')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
# end class ReceiverNameType


class name1(GeneratedsSuper):
    """name1 -- Name of receiver (first part)
    
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
                CurrentSubclassModule_, name1)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if name1.subclass:
            return name1.subclass(*args_, **kwargs_)
        else:
            return name1(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_name1(self, value):
        result = True
        # Validate type name1, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='name1', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('name1')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'name1':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='name1')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='name1', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='name1'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='name1', fromsubclass_=False, pretty_print=True):
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
# end class name1


class name2(GeneratedsSuper):
    """name2 -- Name of company (second part).
    
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
                CurrentSubclassModule_, name2)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if name2.subclass:
            return name2.subclass(*args_, **kwargs_)
        else:
            return name2(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_name2(self, value):
        result = True
        # Validate type name2, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='name2', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('name2')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'name2':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='name2')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='name2', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='name2'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='name2', fromsubclass_=False, pretty_print=True):
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
# end class name2


class name3(GeneratedsSuper):
    """name3 -- Name of company (third part).
    
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
                CurrentSubclassModule_, name3)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if name3.subclass:
            return name3.subclass(*args_, **kwargs_)
        else:
            return name3(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_name3(self, value):
        result = True
        # Validate type name3, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='name3', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('name3')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'name3':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='name3')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='name3', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='name3'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='name3', fromsubclass_=False, pretty_print=True):
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
# end class name3


class CommunicationType(GeneratedsSuper):
    """CommunicationType -- Type of communication.
    includes
    phone -- Phone number. If you are using delivery type CDP, the phone
    number and/or e-mail address are mandatory
    email -- Emailaddress. If you are using delivery type CDP, the phone
    number and/or e-mail address are mandatory
    contactPerson -- First name and last name of contact person.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, phone=None, email=None, contactPerson=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.phone = phone
        self.validate_phoneType(self.phone)
        self.phone_nsprefix_ = None
        self.email = email
        self.validate_emailType(self.email)
        self.email_nsprefix_ = None
        self.contactPerson = contactPerson
        self.validate_contactPersonType(self.contactPerson)
        self.contactPerson_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CommunicationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CommunicationType.subclass:
            return CommunicationType.subclass(*args_, **kwargs_)
        else:
            return CommunicationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_phone(self):
        return self.phone
    def set_phone(self, phone):
        self.phone = phone
    def get_email(self):
        return self.email
    def set_email(self, email):
        self.email = email
    def get_contactPerson(self):
        return self.contactPerson
    def set_contactPerson(self, contactPerson):
        self.contactPerson = contactPerson
    def validate_phoneType(self, value):
        result = True
        # Validate type phoneType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on phoneType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_emailType(self, value):
        result = True
        # Validate type emailType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 70:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on emailType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_contactPersonType(self, value):
        result = True
        # Validate type contactPersonType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on contactPersonType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.phone is not None or
            self.email is not None or
            self.contactPerson is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CommunicationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CommunicationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CommunicationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CommunicationType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CommunicationType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CommunicationType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CommunicationType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.phone is not None:
            namespaceprefix_ = self.phone_nsprefix_ + ':' if (UseCapturedNS_ and self.phone_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sphone>%s</%sphone>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.phone), input_name='phone')), namespaceprefix_ , eol_))
        if self.email is not None:
            namespaceprefix_ = self.email_nsprefix_ + ':' if (UseCapturedNS_ and self.email_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%semail>%s</%semail>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.email), input_name='email')), namespaceprefix_ , eol_))
        if self.contactPerson is not None:
            namespaceprefix_ = self.contactPerson_nsprefix_ + ':' if (UseCapturedNS_ and self.contactPerson_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scontactPerson>%s</%scontactPerson>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.contactPerson), input_name='contactPerson')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'phone':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'phone')
            value_ = self.gds_validate_string(value_, node, 'phone')
            self.phone = value_
            self.phone_nsprefix_ = child_.prefix
            # validate type phoneType
            self.validate_phoneType(self.phone)
        elif nodeName_ == 'email':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'email')
            value_ = self.gds_validate_string(value_, node, 'email')
            self.email = value_
            self.email_nsprefix_ = child_.prefix
            # validate type emailType
            self.validate_emailType(self.email)
        elif nodeName_ == 'contactPerson':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'contactPerson')
            value_ = self.gds_validate_string(value_, node, 'contactPerson')
            self.contactPerson = value_
            self.contactPerson_nsprefix_ = child_.prefix
            # validate type contactPersonType
            self.validate_contactPersonType(self.contactPerson)
# end class CommunicationType


class ContactType(GeneratedsSuper):
    """ContactType -- Type of contact.
    includes
    Communication -- Contact communication information.
    Address -- Contact address.
    Name -- Contact name.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Communication=None, Address=None, Name=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Communication = Communication
        self.Communication_nsprefix_ = "cis"
        self.Address = Address
        self.Address_nsprefix_ = "cis"
        self.Name = Name
        self.Name_nsprefix_ = "cis"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ContactType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ContactType.subclass:
            return ContactType.subclass(*args_, **kwargs_)
        else:
            return ContactType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Communication(self):
        return self.Communication
    def set_Communication(self, Communication):
        self.Communication = Communication
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def _hasContent(self):
        if (
            self.Communication is not None or
            self.Address is not None or
            self.Name is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ContactType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ContactType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ContactType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ContactType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ContactType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ContactType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ContactType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Communication is not None:
            namespaceprefix_ = self.Communication_nsprefix_ + ':' if (UseCapturedNS_ and self.Communication_nsprefix_) else ''
            self.Communication.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Communication', pretty_print=pretty_print)
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            self.Name.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Name', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'Communication':
            obj_ = CommunicationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Communication = obj_
            obj_.original_tagname_ = 'Communication'
        elif nodeName_ == 'Address':
            obj_ = NativeAddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'Name':
            obj_ = NameType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Name = obj_
            obj_.original_tagname_ = 'Name'
# end class ContactType


class PackStationType(GeneratedsSuper):
    """PackStationType -- Type of packstation.
    includes
    postNumber -- Post Nummer of the receiver, if not set receiver e-mail and/or
    mobilephone number needs to be set. When sending to a packstation with "DHL
    Paket" (V01PAK), the postnumber must always be entered.
    packstationNumber -- Number of the Packstation.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, postNumber=None, packstationNumber=None, zip=None, city=None, province=None, Origin=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.postNumber = postNumber
        self.validate_postNumberType(self.postNumber)
        self.postNumber_nsprefix_ = None
        self.packstationNumber = packstationNumber
        self.validate_packstationNumberType(self.packstationNumber)
        self.packstationNumber_nsprefix_ = None
        self.zip = zip
        self.zip_nsprefix_ = "cis"
        self.city = city
        self.validate_city(self.city)
        self.city_nsprefix_ = "cis"
        self.province = province
        self.validate_province(self.province)
        self.province_nsprefix_ = "cis"
        self.Origin = Origin
        self.Origin_nsprefix_ = "cis"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PackStationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PackStationType.subclass:
            return PackStationType.subclass(*args_, **kwargs_)
        else:
            return PackStationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_postNumber(self):
        return self.postNumber
    def set_postNumber(self, postNumber):
        self.postNumber = postNumber
    def get_packstationNumber(self):
        return self.packstationNumber
    def set_packstationNumber(self, packstationNumber):
        self.packstationNumber = packstationNumber
    def get_zip(self):
        return self.zip
    def set_zip(self, zip):
        self.zip = zip
    def get_city(self):
        return self.city
    def set_city(self, city):
        self.city = city
    def get_province(self):
        return self.province
    def set_province(self, province):
        self.province = province
    def get_Origin(self):
        return self.Origin
    def set_Origin(self, Origin):
        self.Origin = Origin
    def validate_postNumberType(self, value):
        result = True
        # Validate type postNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on postNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on postNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_packstationNumberType(self, value):
        result = True
        # Validate type packstationNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on packstationNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on packstationNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_city(self, value):
        result = True
        # Validate type city, a restriction on xs:string.
        pass
        return result
    def validate_province(self, value):
        result = True
        # Validate type province, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.postNumber is not None or
            self.packstationNumber is not None or
            self.zip is not None or
            self.city is not None or
            self.province is not None or
            self.Origin is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PackStationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PackStationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PackStationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PackStationType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PackStationType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PackStationType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PackStationType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.postNumber is not None:
            namespaceprefix_ = self.postNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.postNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spostNumber>%s</%spostNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.postNumber), input_name='postNumber')), namespaceprefix_ , eol_))
        if self.packstationNumber is not None:
            namespaceprefix_ = self.packstationNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.packstationNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spackstationNumber>%s</%spackstationNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.packstationNumber), input_name='packstationNumber')), namespaceprefix_ , eol_))
        if self.zip is not None:
            namespaceprefix_ = self.zip_nsprefix_ + ':' if (UseCapturedNS_ and self.zip_nsprefix_) else ''
            self.zip.export(outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='zip', pretty_print=pretty_print)
        if self.city is not None:
            namespaceprefix_ = self.city_nsprefix_ + ':' if (UseCapturedNS_ and self.city_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scity>%s</%scity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.city), input_name='city')), namespaceprefix_ , eol_))
        if self.province is not None:
            namespaceprefix_ = self.province_nsprefix_ + ':' if (UseCapturedNS_ and self.province_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sprovince>%s</%sprovince>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.province), input_name='province')), namespaceprefix_ , eol_))
        if self.Origin is not None:
            namespaceprefix_ = self.Origin_nsprefix_ + ':' if (UseCapturedNS_ and self.Origin_nsprefix_) else ''
            self.Origin.export(outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='Origin', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'postNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'postNumber')
            value_ = self.gds_validate_string(value_, node, 'postNumber')
            self.postNumber = value_
            self.postNumber_nsprefix_ = child_.prefix
            # validate type postNumberType
            self.validate_postNumberType(self.postNumber)
        elif nodeName_ == 'packstationNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'packstationNumber')
            value_ = self.gds_validate_string(value_, node, 'packstationNumber')
            self.packstationNumber = value_
            self.packstationNumber_nsprefix_ = child_.prefix
            # validate type packstationNumberType
            self.validate_packstationNumberType(self.packstationNumber)
        elif nodeName_ == 'zip':
            obj_ = ZipType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.zip = obj_
            obj_.original_tagname_ = 'zip'
        elif nodeName_ == 'city':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'city')
            value_ = self.gds_validate_string(value_, node, 'city')
            self.city = value_
            self.city_nsprefix_ = child_.prefix
            # validate type city
            self.validate_city(self.city)
        elif nodeName_ == 'province':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'province')
            value_ = self.gds_validate_string(value_, node, 'province')
            self.province = value_
            self.province_nsprefix_ = child_.prefix
            # validate type province
            self.validate_province(self.province)
        elif nodeName_ == 'Origin':
            obj_ = CountryType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Origin = obj_
            obj_.original_tagname_ = 'Origin'
# end class PackStationType


class PostfilialeType(GeneratedsSuper):
    """PostfilialeType -- Type of Postfiliale
    includes
    postfilialNumber -- Number of the postfiliale
    postNumber -- Post Nummer of the receiver
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, postfilialNumber=None, postNumber=None, zip=None, city=None, Origin=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.postfilialNumber = postfilialNumber
        self.validate_postfilialNumberType(self.postfilialNumber)
        self.postfilialNumber_nsprefix_ = None
        self.postNumber = postNumber
        self.validate_postNumberType7(self.postNumber)
        self.postNumber_nsprefix_ = None
        self.zip = zip
        self.zip_nsprefix_ = "cis"
        self.city = city
        self.validate_city(self.city)
        self.city_nsprefix_ = "cis"
        self.Origin = Origin
        self.Origin_nsprefix_ = "cis"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PostfilialeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PostfilialeType.subclass:
            return PostfilialeType.subclass(*args_, **kwargs_)
        else:
            return PostfilialeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_postfilialNumber(self):
        return self.postfilialNumber
    def set_postfilialNumber(self, postfilialNumber):
        self.postfilialNumber = postfilialNumber
    def get_postNumber(self):
        return self.postNumber
    def set_postNumber(self, postNumber):
        self.postNumber = postNumber
    def get_zip(self):
        return self.zip
    def set_zip(self, zip):
        self.zip = zip
    def get_city(self):
        return self.city
    def set_city(self, city):
        self.city = city
    def get_Origin(self):
        return self.Origin
    def set_Origin(self, Origin):
        self.Origin = Origin
    def validate_postfilialNumberType(self, value):
        result = True
        # Validate type postfilialNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on postfilialNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on postfilialNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_postNumberType7(self, value):
        result = True
        # Validate type postNumberType7, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on postNumberType7' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on postNumberType7' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_city(self, value):
        result = True
        # Validate type city, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.postfilialNumber is not None or
            self.postNumber is not None or
            self.zip is not None or
            self.city is not None or
            self.Origin is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PostfilialeType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PostfilialeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PostfilialeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PostfilialeType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PostfilialeType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PostfilialeType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PostfilialeType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.postfilialNumber is not None:
            namespaceprefix_ = self.postfilialNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.postfilialNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spostfilialNumber>%s</%spostfilialNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.postfilialNumber), input_name='postfilialNumber')), namespaceprefix_ , eol_))
        if self.postNumber is not None:
            namespaceprefix_ = self.postNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.postNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spostNumber>%s</%spostNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.postNumber), input_name='postNumber')), namespaceprefix_ , eol_))
        if self.zip is not None:
            namespaceprefix_ = self.zip_nsprefix_ + ':' if (UseCapturedNS_ and self.zip_nsprefix_) else ''
            self.zip.export(outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='zip', pretty_print=pretty_print)
        if self.city is not None:
            namespaceprefix_ = self.city_nsprefix_ + ':' if (UseCapturedNS_ and self.city_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scity>%s</%scity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.city), input_name='city')), namespaceprefix_ , eol_))
        if self.Origin is not None:
            namespaceprefix_ = self.Origin_nsprefix_ + ':' if (UseCapturedNS_ and self.Origin_nsprefix_) else ''
            self.Origin.export(outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='Origin', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'postfilialNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'postfilialNumber')
            value_ = self.gds_validate_string(value_, node, 'postfilialNumber')
            self.postfilialNumber = value_
            self.postfilialNumber_nsprefix_ = child_.prefix
            # validate type postfilialNumberType
            self.validate_postfilialNumberType(self.postfilialNumber)
        elif nodeName_ == 'postNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'postNumber')
            value_ = self.gds_validate_string(value_, node, 'postNumber')
            self.postNumber = value_
            self.postNumber_nsprefix_ = child_.prefix
            # validate type postNumberType7
            self.validate_postNumberType7(self.postNumber)
        elif nodeName_ == 'zip':
            obj_ = ZipType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.zip = obj_
            obj_.original_tagname_ = 'zip'
        elif nodeName_ == 'city':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'city')
            value_ = self.gds_validate_string(value_, node, 'city')
            self.city = value_
            self.city_nsprefix_ = child_.prefix
            # validate type city
            self.validate_city(self.city)
        elif nodeName_ == 'Origin':
            obj_ = CountryType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Origin = obj_
            obj_.original_tagname_ = 'Origin'
# end class PostfilialeType


class PostfilialeTypeNoCountry(GeneratedsSuper):
    """PostfilialeTypeNoCountry -- Type of Postfiliale
    includes
    postfilialNumber -- Number of the postfiliale
    postNumber -- Post Nummer of the receiver or receiver e-mail-adress.
    Origin -- Country.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, postfilialNumber=None, postNumber=None, zip=None, city=None, Origin=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.postfilialNumber = postfilialNumber
        self.validate_postfilialNumberType8(self.postfilialNumber)
        self.postfilialNumber_nsprefix_ = None
        self.postNumber = postNumber
        self.validate_postNumberType9(self.postNumber)
        self.postNumber_nsprefix_ = None
        self.zip = zip
        self.zip_nsprefix_ = "cis"
        self.city = city
        self.validate_city(self.city)
        self.city_nsprefix_ = "cis"
        self.Origin = Origin
        self.Origin_nsprefix_ = "cis"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PostfilialeTypeNoCountry)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PostfilialeTypeNoCountry.subclass:
            return PostfilialeTypeNoCountry.subclass(*args_, **kwargs_)
        else:
            return PostfilialeTypeNoCountry(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_postfilialNumber(self):
        return self.postfilialNumber
    def set_postfilialNumber(self, postfilialNumber):
        self.postfilialNumber = postfilialNumber
    def get_postNumber(self):
        return self.postNumber
    def set_postNumber(self, postNumber):
        self.postNumber = postNumber
    def get_zip(self):
        return self.zip
    def set_zip(self, zip):
        self.zip = zip
    def get_city(self):
        return self.city
    def set_city(self, city):
        self.city = city
    def get_Origin(self):
        return self.Origin
    def set_Origin(self, Origin):
        self.Origin = Origin
    def validate_postfilialNumberType8(self, value):
        result = True
        # Validate type postfilialNumberType8, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on postfilialNumberType8' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on postfilialNumberType8' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_postNumberType9(self, value):
        result = True
        # Validate type postNumberType9, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on postNumberType9' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on postNumberType9' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_city(self, value):
        result = True
        # Validate type city, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.postfilialNumber is not None or
            self.postNumber is not None or
            self.zip is not None or
            self.city is not None or
            self.Origin is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PostfilialeTypeNoCountry', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PostfilialeTypeNoCountry')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PostfilialeTypeNoCountry':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PostfilialeTypeNoCountry')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PostfilialeTypeNoCountry', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PostfilialeTypeNoCountry'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PostfilialeTypeNoCountry', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.postfilialNumber is not None:
            namespaceprefix_ = self.postfilialNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.postfilialNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spostfilialNumber>%s</%spostfilialNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.postfilialNumber), input_name='postfilialNumber')), namespaceprefix_ , eol_))
        if self.postNumber is not None:
            namespaceprefix_ = self.postNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.postNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spostNumber>%s</%spostNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.postNumber), input_name='postNumber')), namespaceprefix_ , eol_))
        if self.zip is not None:
            namespaceprefix_ = self.zip_nsprefix_ + ':' if (UseCapturedNS_ and self.zip_nsprefix_) else ''
            self.zip.export(outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='zip', pretty_print=pretty_print)
        if self.city is not None:
            namespaceprefix_ = self.city_nsprefix_ + ':' if (UseCapturedNS_ and self.city_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scity>%s</%scity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.city), input_name='city')), namespaceprefix_ , eol_))
        if self.Origin is not None:
            namespaceprefix_ = self.Origin_nsprefix_ + ':' if (UseCapturedNS_ and self.Origin_nsprefix_) else ''
            self.Origin.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Origin', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'postfilialNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'postfilialNumber')
            value_ = self.gds_validate_string(value_, node, 'postfilialNumber')
            self.postfilialNumber = value_
            self.postfilialNumber_nsprefix_ = child_.prefix
            # validate type postfilialNumberType8
            self.validate_postfilialNumberType8(self.postfilialNumber)
        elif nodeName_ == 'postNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'postNumber')
            value_ = self.gds_validate_string(value_, node, 'postNumber')
            self.postNumber = value_
            self.postNumber_nsprefix_ = child_.prefix
            # validate type postNumberType9
            self.validate_postNumberType9(self.postNumber)
        elif nodeName_ == 'zip':
            obj_ = ZipType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.zip = obj_
            obj_.original_tagname_ = 'zip'
        elif nodeName_ == 'city':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'city')
            value_ = self.gds_validate_string(value_, node, 'city')
            self.city = value_
            self.city_nsprefix_ = child_.prefix
            # validate type city
            self.validate_city(self.city)
        elif nodeName_ == 'Origin':
            obj_ = CountryType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Origin = obj_
            obj_.original_tagname_ = 'Origin'
# end class PostfilialeTypeNoCountry


class ParcelShopType(GeneratedsSuper):
    """ParcelShopType -- Type of ParcelShop (Receiver is in Europe)
    includes
    parcelShopNumber -- Number of the ParcelShop
    streetName -- Name of street of the ParcelShop
    streetNumber -- House number of the ParcelShop
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, parcelShopNumber=None, streetName=None, streetNumber=None, zip=None, city=None, Origin=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.parcelShopNumber = parcelShopNumber
        self.validate_parcelShopNumberType(self.parcelShopNumber)
        self.parcelShopNumber_nsprefix_ = None
        self.streetName = streetName
        self.validate_streetNameType10(self.streetName)
        self.streetName_nsprefix_ = None
        self.streetNumber = streetNumber
        self.validate_streetNumberType11(self.streetNumber)
        self.streetNumber_nsprefix_ = None
        self.zip = zip
        self.zip_nsprefix_ = "cis"
        self.city = city
        self.validate_city(self.city)
        self.city_nsprefix_ = "cis"
        self.Origin = Origin
        self.Origin_nsprefix_ = "cis"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ParcelShopType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ParcelShopType.subclass:
            return ParcelShopType.subclass(*args_, **kwargs_)
        else:
            return ParcelShopType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_parcelShopNumber(self):
        return self.parcelShopNumber
    def set_parcelShopNumber(self, parcelShopNumber):
        self.parcelShopNumber = parcelShopNumber
    def get_streetName(self):
        return self.streetName
    def set_streetName(self, streetName):
        self.streetName = streetName
    def get_streetNumber(self):
        return self.streetNumber
    def set_streetNumber(self, streetNumber):
        self.streetNumber = streetNumber
    def get_zip(self):
        return self.zip
    def set_zip(self, zip):
        self.zip = zip
    def get_city(self):
        return self.city
    def set_city(self, city):
        self.city = city
    def get_Origin(self):
        return self.Origin
    def set_Origin(self, Origin):
        self.Origin = Origin
    def validate_parcelShopNumberType(self, value):
        result = True
        # Validate type parcelShopNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on parcelShopNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on parcelShopNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_streetNameType10(self, value):
        result = True
        # Validate type streetNameType10, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetNameType10' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_streetNumberType11(self, value):
        result = True
        # Validate type streetNumberType11, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetNumberType11' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_city(self, value):
        result = True
        # Validate type city, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.parcelShopNumber is not None or
            self.streetName is not None or
            self.streetNumber is not None or
            self.zip is not None or
            self.city is not None or
            self.Origin is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ParcelShopType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ParcelShopType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ParcelShopType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ParcelShopType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ParcelShopType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ParcelShopType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ParcelShopType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.parcelShopNumber is not None:
            namespaceprefix_ = self.parcelShopNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.parcelShopNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sparcelShopNumber>%s</%sparcelShopNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.parcelShopNumber), input_name='parcelShopNumber')), namespaceprefix_ , eol_))
        if self.streetName is not None:
            namespaceprefix_ = self.streetName_nsprefix_ + ':' if (UseCapturedNS_ and self.streetName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstreetName>%s</%sstreetName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.streetName), input_name='streetName')), namespaceprefix_ , eol_))
        if self.streetNumber is not None:
            namespaceprefix_ = self.streetNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.streetNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstreetNumber>%s</%sstreetNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.streetNumber), input_name='streetNumber')), namespaceprefix_ , eol_))
        if self.zip is not None:
            namespaceprefix_ = self.zip_nsprefix_ + ':' if (UseCapturedNS_ and self.zip_nsprefix_) else ''
            self.zip.export(outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='zip', pretty_print=pretty_print)
        if self.city is not None:
            namespaceprefix_ = self.city_nsprefix_ + ':' if (UseCapturedNS_ and self.city_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scity>%s</%scity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.city), input_name='city')), namespaceprefix_ , eol_))
        if self.Origin is not None:
            namespaceprefix_ = self.Origin_nsprefix_ + ':' if (UseCapturedNS_ and self.Origin_nsprefix_) else ''
            self.Origin.export(outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='Origin', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'parcelShopNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'parcelShopNumber')
            value_ = self.gds_validate_string(value_, node, 'parcelShopNumber')
            self.parcelShopNumber = value_
            self.parcelShopNumber_nsprefix_ = child_.prefix
            # validate type parcelShopNumberType
            self.validate_parcelShopNumberType(self.parcelShopNumber)
        elif nodeName_ == 'streetName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'streetName')
            value_ = self.gds_validate_string(value_, node, 'streetName')
            self.streetName = value_
            self.streetName_nsprefix_ = child_.prefix
            # validate type streetNameType10
            self.validate_streetNameType10(self.streetName)
        elif nodeName_ == 'streetNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'streetNumber')
            value_ = self.gds_validate_string(value_, node, 'streetNumber')
            self.streetNumber = value_
            self.streetNumber_nsprefix_ = child_.prefix
            # validate type streetNumberType11
            self.validate_streetNumberType11(self.streetNumber)
        elif nodeName_ == 'zip':
            obj_ = ZipType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.zip = obj_
            obj_.original_tagname_ = 'zip'
        elif nodeName_ == 'city':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'city')
            value_ = self.gds_validate_string(value_, node, 'city')
            self.city = value_
            self.city_nsprefix_ = child_.prefix
            # validate type city
            self.validate_city(self.city)
        elif nodeName_ == 'Origin':
            obj_ = CountryType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Origin = obj_
            obj_.original_tagname_ = 'Origin'
# end class ParcelShopType


class CustomerType(GeneratedsSuper):
    """CustomerType -- Type of customer
    includes
    Name -- Name of customer.
    vatID -- VAT id.
    Address -- Address of customer
    Contact -- Contact information
    Bank -- Bank information
    note -- Additional notes
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Name=None, vatID=None, EKP=None, Address=None, Contact=None, Bank=None, note=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = "cis"
        self.vatID = vatID
        self.vatID_nsprefix_ = None
        self.EKP = EKP
        self.validate_EKP(self.EKP)
        self.EKP_nsprefix_ = "cis"
        self.Address = Address
        self.Address_nsprefix_ = "cis"
        self.Contact = Contact
        self.Contact_nsprefix_ = "cis"
        self.Bank = Bank
        self.Bank_nsprefix_ = "cis"
        self.note = note
        self.note_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CustomerType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CustomerType.subclass:
            return CustomerType.subclass(*args_, **kwargs_)
        else:
            return CustomerType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Name(self):
        return self.Name
    def set_Name(self, Name):
        self.Name = Name
    def get_vatID(self):
        return self.vatID
    def set_vatID(self, vatID):
        self.vatID = vatID
    def get_EKP(self):
        return self.EKP
    def set_EKP(self, EKP):
        self.EKP = EKP
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_Contact(self):
        return self.Contact
    def set_Contact(self, Contact):
        self.Contact = Contact
    def get_Bank(self):
        return self.Bank
    def set_Bank(self, Bank):
        self.Bank = Bank
    def get_note(self):
        return self.note
    def set_note(self, note):
        self.note = note
    def validate_EKP(self, value):
        result = True
        # Validate type EKP, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.Name is not None or
            self.vatID is not None or
            self.EKP is not None or
            self.Address is not None or
            self.Contact is not None or
            self.Bank is not None or
            self.note is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CustomerType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CustomerType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CustomerType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CustomerType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CustomerType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CustomerType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CustomerType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            self.Name.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Name', pretty_print=pretty_print)
        if self.vatID is not None:
            namespaceprefix_ = self.vatID_nsprefix_ + ':' if (UseCapturedNS_ and self.vatID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%svatID>%s</%svatID>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.vatID), input_name='vatID')), namespaceprefix_ , eol_))
        if self.EKP is not None:
            namespaceprefix_ = self.EKP_nsprefix_ + ':' if (UseCapturedNS_ and self.EKP_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEKP>%s</%sEKP>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EKP), input_name='EKP')), namespaceprefix_ , eol_))
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.Contact is not None:
            namespaceprefix_ = self.Contact_nsprefix_ + ':' if (UseCapturedNS_ and self.Contact_nsprefix_) else ''
            self.Contact.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Contact', pretty_print=pretty_print)
        if self.Bank is not None:
            namespaceprefix_ = self.Bank_nsprefix_ + ':' if (UseCapturedNS_ and self.Bank_nsprefix_) else ''
            self.Bank.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Bank', pretty_print=pretty_print)
        if self.note is not None:
            namespaceprefix_ = self.note_nsprefix_ + ':' if (UseCapturedNS_ and self.note_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snote>%s</%snote>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.note), input_name='note')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
            obj_ = NameType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Name = obj_
            obj_.original_tagname_ = 'Name'
        elif nodeName_ == 'vatID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'vatID')
            value_ = self.gds_validate_string(value_, node, 'vatID')
            self.vatID = value_
            self.vatID_nsprefix_ = child_.prefix
        elif nodeName_ == 'EKP':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EKP')
            value_ = self.gds_validate_string(value_, node, 'EKP')
            self.EKP = value_
            self.EKP_nsprefix_ = child_.prefix
            # validate type EKP
            self.validate_EKP(self.EKP)
        elif nodeName_ == 'Address':
            obj_ = NativeAddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'Contact':
            obj_ = ContactType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Contact = obj_
            obj_.original_tagname_ = 'Contact'
        elif nodeName_ == 'Bank':
            obj_ = BankType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Bank = obj_
            obj_.original_tagname_ = 'Bank'
        elif nodeName_ == 'note':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'note')
            value_ = self.gds_validate_string(value_, node, 'note')
            self.note = value_
            self.note_nsprefix_ = child_.prefix
# end class CustomerType


class note(GeneratedsSuper):
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
                CurrentSubclassModule_, note)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if note.subclass:
            return note.subclass(*args_, **kwargs_)
        else:
            return note(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='note', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('note')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'note':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='note')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='note', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='note'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='note', fromsubclass_=False, pretty_print=True):
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
# end class note


class ErrorType(GeneratedsSuper):
    """ErrorType -- Type of error
    includes
    priority -- Priority (e.g. error, warnung, .....)
    code -- Code
    dateTime -- Occurence
    description -- Short description
    descriptionLong -- Detailed description
    solution -- Suggested solution
    application -- Name of application
    module -- Module name
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, priority=None, code=None, dateTime=None, description=None, descriptionLong=None, solution=None, application=None, module=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.priority = priority
        self.priority_nsprefix_ = None
        self.code = code
        self.code_nsprefix_ = None
        if isinstance(dateTime, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(dateTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = dateTime
        self.dateTime = initvalue_
        self.dateTime_nsprefix_ = None
        self.description = description
        self.description_nsprefix_ = None
        self.descriptionLong = descriptionLong
        self.descriptionLong_nsprefix_ = None
        self.solution = solution
        self.solution_nsprefix_ = None
        self.application = application
        self.application_nsprefix_ = None
        self.module = module
        self.module_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ErrorType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ErrorType.subclass:
            return ErrorType.subclass(*args_, **kwargs_)
        else:
            return ErrorType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_priority(self):
        return self.priority
    def set_priority(self, priority):
        self.priority = priority
    def get_code(self):
        return self.code
    def set_code(self, code):
        self.code = code
    def get_dateTime(self):
        return self.dateTime
    def set_dateTime(self, dateTime):
        self.dateTime = dateTime
    def get_description(self):
        return self.description
    def set_description(self, description):
        self.description = description
    def get_descriptionLong(self):
        return self.descriptionLong
    def set_descriptionLong(self, descriptionLong):
        self.descriptionLong = descriptionLong
    def get_solution(self):
        return self.solution
    def set_solution(self, solution):
        self.solution = solution
    def get_application(self):
        return self.application
    def set_application(self, application):
        self.application = application
    def get_module(self):
        return self.module
    def set_module(self, module):
        self.module = module
    def _hasContent(self):
        if (
            self.priority is not None or
            self.code is not None or
            self.dateTime is not None or
            self.description is not None or
            self.descriptionLong is not None or
            self.solution is not None or
            self.application is not None or
            self.module is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ErrorType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ErrorType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ErrorType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ErrorType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ErrorType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ErrorType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ErrorType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.priority is not None:
            namespaceprefix_ = self.priority_nsprefix_ + ':' if (UseCapturedNS_ and self.priority_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spriority>%s</%spriority>%s' % (namespaceprefix_ , self.gds_format_integer(self.priority, input_name='priority'), namespaceprefix_ , eol_))
        if self.code is not None:
            namespaceprefix_ = self.code_nsprefix_ + ':' if (UseCapturedNS_ and self.code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scode>%s</%scode>%s' % (namespaceprefix_ , self.gds_format_integer(self.code, input_name='code'), namespaceprefix_ , eol_))
        if self.dateTime is not None:
            namespaceprefix_ = self.dateTime_nsprefix_ + ':' if (UseCapturedNS_ and self.dateTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdateTime>%s</%sdateTime>%s' % (namespaceprefix_ , self.gds_format_datetime(self.dateTime, input_name='dateTime'), namespaceprefix_ , eol_))
        if self.description is not None:
            namespaceprefix_ = self.description_nsprefix_ + ':' if (UseCapturedNS_ and self.description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdescription>%s</%sdescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.description), input_name='description')), namespaceprefix_ , eol_))
        if self.descriptionLong is not None:
            namespaceprefix_ = self.descriptionLong_nsprefix_ + ':' if (UseCapturedNS_ and self.descriptionLong_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdescriptionLong>%s</%sdescriptionLong>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.descriptionLong), input_name='descriptionLong')), namespaceprefix_ , eol_))
        if self.solution is not None:
            namespaceprefix_ = self.solution_nsprefix_ + ':' if (UseCapturedNS_ and self.solution_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssolution>%s</%ssolution>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.solution), input_name='solution')), namespaceprefix_ , eol_))
        if self.application is not None:
            namespaceprefix_ = self.application_nsprefix_ + ':' if (UseCapturedNS_ and self.application_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sapplication>%s</%sapplication>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.application), input_name='application')), namespaceprefix_ , eol_))
        if self.module is not None:
            namespaceprefix_ = self.module_nsprefix_ + ':' if (UseCapturedNS_ and self.module_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smodule>%s</%smodule>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.module), input_name='module')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'priority' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'priority')
            ival_ = self.gds_validate_integer(ival_, node, 'priority')
            self.priority = ival_
            self.priority_nsprefix_ = child_.prefix
        elif nodeName_ == 'code' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'code')
            ival_ = self.gds_validate_integer(ival_, node, 'code')
            self.code = ival_
            self.code_nsprefix_ = child_.prefix
        elif nodeName_ == 'dateTime':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.dateTime = dval_
            self.dateTime_nsprefix_ = child_.prefix
        elif nodeName_ == 'description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'description')
            value_ = self.gds_validate_string(value_, node, 'description')
            self.description = value_
            self.description_nsprefix_ = child_.prefix
        elif nodeName_ == 'descriptionLong':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'descriptionLong')
            value_ = self.gds_validate_string(value_, node, 'descriptionLong')
            self.descriptionLong = value_
            self.descriptionLong_nsprefix_ = child_.prefix
        elif nodeName_ == 'solution':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'solution')
            value_ = self.gds_validate_string(value_, node, 'solution')
            self.solution = value_
            self.solution_nsprefix_ = child_.prefix
        elif nodeName_ == 'application':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'application')
            value_ = self.gds_validate_string(value_, node, 'application')
            self.application = value_
            self.application_nsprefix_ = child_.prefix
        elif nodeName_ == 'module':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'module')
            value_ = self.gds_validate_string(value_, node, 'module')
            self.module = value_
            self.module_nsprefix_ = child_.prefix
# end class ErrorType


class CountryType(GeneratedsSuper):
    """CountryType -- Type of country
    includes
    country -- Name of country.
    countryISOCode -- Country's ISO-Code (ISO-2-Alpha).
    state -- Name of state.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, country=None, countryISOCode=None, state=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.country = country
        self.validate_countryType(self.country)
        self.country_nsprefix_ = None
        self.countryISOCode = countryISOCode
        self.validate_countryISOType(self.countryISOCode)
        self.countryISOCode_nsprefix_ = "cis"
        self.state = state
        self.validate_stateType(self.state)
        self.state_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CountryType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CountryType.subclass:
            return CountryType.subclass(*args_, **kwargs_)
        else:
            return CountryType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_country(self):
        return self.country
    def set_country(self, country):
        self.country = country
    def get_countryISOCode(self):
        return self.countryISOCode
    def set_countryISOCode(self, countryISOCode):
        self.countryISOCode = countryISOCode
    def get_state(self):
        return self.state
    def set_state(self, state):
        self.state = state
    def validate_countryType(self, value):
        result = True
        # Validate type countryType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 30:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on countryType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_countryISOType(self, value):
        result = True
        # Validate type countryISOType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on countryISOType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on countryISOType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_stateType(self, value):
        result = True
        # Validate type stateType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on stateType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.country is not None or
            self.countryISOCode is not None or
            self.state is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CountryType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CountryType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CountryType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CountryType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CountryType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CountryType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CountryType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.country is not None:
            namespaceprefix_ = self.country_nsprefix_ + ':' if (UseCapturedNS_ and self.country_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scountry>%s</%scountry>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.country), input_name='country')), namespaceprefix_ , eol_))
        if self.countryISOCode is not None:
            namespaceprefix_ = self.countryISOCode_nsprefix_ + ':' if (UseCapturedNS_ and self.countryISOCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scountryISOCode>%s</%scountryISOCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.countryISOCode), input_name='countryISOCode')), namespaceprefix_ , eol_))
        if self.state is not None:
            namespaceprefix_ = self.state_nsprefix_ + ':' if (UseCapturedNS_ and self.state_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstate>%s</%sstate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.state), input_name='state')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'country':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'country')
            value_ = self.gds_validate_string(value_, node, 'country')
            self.country = value_
            self.country_nsprefix_ = child_.prefix
            # validate type countryType
            self.validate_countryType(self.country)
        elif nodeName_ == 'countryISOCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'countryISOCode')
            value_ = self.gds_validate_string(value_, node, 'countryISOCode')
            self.countryISOCode = value_
            self.countryISOCode_nsprefix_ = child_.prefix
            # validate type countryISOType
            self.validate_countryISOType(self.countryISOCode)
        elif nodeName_ == 'state':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'state')
            value_ = self.gds_validate_string(value_, node, 'state')
            self.state = value_
            self.state_nsprefix_ = child_.prefix
            # validate type stateType
            self.validate_stateType(self.state)
# end class CountryType


class ShipmentNumberType(GeneratedsSuper):
    """ShipmentNumberType -- Type of shipment number
    can be
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, shipmentNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.shipmentNumber = shipmentNumber
        self.validate_shipmentNumber(self.shipmentNumber)
        self.shipmentNumber_nsprefix_ = "cis"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentNumberType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentNumberType.subclass:
            return ShipmentNumberType.subclass(*args_, **kwargs_)
        else:
            return ShipmentNumberType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_shipmentNumber(self):
        return self.shipmentNumber
    def set_shipmentNumber(self, shipmentNumber):
        self.shipmentNumber = shipmentNumber
    def validate_shipmentNumber(self, value):
        result = True
        # Validate type shipmentNumber, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.shipmentNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentNumberType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentNumberType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentNumberType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentNumberType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentNumberType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentNumberType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentNumberType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.shipmentNumber is not None:
            namespaceprefix_ = self.shipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.shipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sshipmentNumber>%s</%sshipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.shipmentNumber), input_name='shipmentNumber')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'shipmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'shipmentNumber')
            value_ = self.gds_validate_string(value_, node, 'shipmentNumber')
            self.shipmentNumber = value_
            self.shipmentNumber_nsprefix_ = child_.prefix
            # validate type shipmentNumber
            self.validate_shipmentNumber(self.shipmentNumber)
# end class ShipmentNumberType


class Status(GeneratedsSuper):
    """Status -- part of webservice response
    includes
    statuscode -- statuscode value.
    statusDescription -- description corresponding to the statuscode
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, statuscode=None, statusDescription=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.statuscode = statuscode
        self.validate_statuscodeType(self.statuscode)
        self.statuscode_nsprefix_ = None
        self.statusDescription = statusDescription
        self.validate_statusDescriptionType(self.statusDescription)
        self.statusDescription_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Status)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Status.subclass:
            return Status.subclass(*args_, **kwargs_)
        else:
            return Status(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_statuscode(self):
        return self.statuscode
    def set_statuscode(self, statuscode):
        self.statuscode = statuscode
    def get_statusDescription(self):
        return self.statusDescription
    def set_statusDescription(self, statusDescription):
        self.statusDescription = statusDescription
    def validate_statuscodeType(self, value):
        result = True
        # Validate type statuscodeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on statuscodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_statusDescriptionType(self, value):
        result = True
        # Validate type statusDescriptionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 500:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on statusDescriptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.statuscode is not None or
            self.statusDescription is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Status', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Status')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Status':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Status')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Status', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Status'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Status', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.statuscode is not None:
            namespaceprefix_ = self.statuscode_nsprefix_ + ':' if (UseCapturedNS_ and self.statuscode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstatuscode>%s</%sstatuscode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.statuscode), input_name='statuscode')), namespaceprefix_ , eol_))
        if self.statusDescription is not None:
            namespaceprefix_ = self.statusDescription_nsprefix_ + ':' if (UseCapturedNS_ and self.statusDescription_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstatusDescription>%s</%sstatusDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.statusDescription), input_name='statusDescription')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'statuscode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'statuscode')
            value_ = self.gds_validate_string(value_, node, 'statuscode')
            self.statuscode = value_
            self.statuscode_nsprefix_ = child_.prefix
            # validate type statuscodeType
            self.validate_statuscodeType(self.statuscode)
        elif nodeName_ == 'statusDescription':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'statusDescription')
            value_ = self.gds_validate_string(value_, node, 'statusDescription')
            self.statusDescription = value_
            self.statusDescription_nsprefix_ = child_.prefix
            # validate type statusDescriptionType
            self.validate_statusDescriptionType(self.statusDescription)
# end class Status


class productKey(GeneratedsSuper):
    """productKey -- DHL product Key.
    
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
                CurrentSubclassModule_, productKey)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if productKey.subclass:
            return productKey.subclass(*args_, **kwargs_)
        else:
            return productKey(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_productKey(self, value):
        result = True
        # Validate type productKey, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='productKey', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('productKey')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'productKey':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='productKey')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='productKey', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='productKey'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='productKey', fromsubclass_=False, pretty_print=True):
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
# end class productKey


class Dimension(GeneratedsSuper):
    """Dimension -- Package dimensions (length, width, height)
    includes
    length -- length of package
    width -- width of package
    height -- height of package
    unit -- unit for all measures
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, length=None, width=None, height=None, unit='mm', gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.length = length
        self.length_nsprefix_ = None
        self.width = width
        self.width_nsprefix_ = None
        self.height = height
        self.height_nsprefix_ = None
        self.unit = unit
        self.validate_unitType(self.unit)
        self.unit_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Dimension)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Dimension.subclass:
            return Dimension.subclass(*args_, **kwargs_)
        else:
            return Dimension(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_length(self):
        return self.length
    def set_length(self, length):
        self.length = length
    def get_width(self):
        return self.width
    def set_width(self, width):
        self.width = width
    def get_height(self):
        return self.height
    def set_height(self, height):
        self.height = height
    def get_unit(self):
        return self.unit
    def set_unit(self, unit):
        self.unit = unit
    def validate_unitType(self, value):
        result = True
        # Validate type unitType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['mm', 'inch']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on unitType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) > 15:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on unitType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.length is not None or
            self.width is not None or
            self.height is not None or
            self.unit != "mm"
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Dimension', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Dimension')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Dimension':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Dimension')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Dimension', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Dimension'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Dimension', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.length is not None:
            namespaceprefix_ = self.length_nsprefix_ + ':' if (UseCapturedNS_ and self.length_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slength>%s</%slength>%s' % (namespaceprefix_ , self.gds_format_integer(self.length, input_name='length'), namespaceprefix_ , eol_))
        if self.width is not None:
            namespaceprefix_ = self.width_nsprefix_ + ':' if (UseCapturedNS_ and self.width_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%swidth>%s</%swidth>%s' % (namespaceprefix_ , self.gds_format_integer(self.width, input_name='width'), namespaceprefix_ , eol_))
        if self.height is not None:
            namespaceprefix_ = self.height_nsprefix_ + ':' if (UseCapturedNS_ and self.height_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sheight>%s</%sheight>%s' % (namespaceprefix_ , self.gds_format_integer(self.height, input_name='height'), namespaceprefix_ , eol_))
        if self.unit != "mm":
            namespaceprefix_ = self.unit_nsprefix_ + ':' if (UseCapturedNS_ and self.unit_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sunit>%s</%sunit>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.unit), input_name='unit')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'length' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'length')
            ival_ = self.gds_validate_integer(ival_, node, 'length')
            self.length = ival_
            self.length_nsprefix_ = child_.prefix
        elif nodeName_ == 'width' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'width')
            ival_ = self.gds_validate_integer(ival_, node, 'width')
            self.width = ival_
            self.width_nsprefix_ = child_.prefix
        elif nodeName_ == 'height' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'height')
            ival_ = self.gds_validate_integer(ival_, node, 'height')
            self.height = ival_
            self.height_nsprefix_ = child_.prefix
        elif nodeName_ == 'unit':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'unit')
            value_ = self.gds_validate_string(value_, node, 'unit')
            self.unit = value_
            self.unit_nsprefix_ = child_.prefix
            # validate type unitType
            self.validate_unitType(self.unit)
# end class Dimension


class TimeFrame(GeneratedsSuper):
    """TimeFrame -- Time Frame in which actions should affect
    includes
    from -- begin of timeframe
    until -- end of timeframe
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, from_=None, until=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if isinstance(from_, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(from_, '%H:%M:%S').time()
        else:
            initvalue_ = from_
        self.from_ = initvalue_
        self.from__nsprefix_ = None
        if isinstance(until, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(until, '%H:%M:%S').time()
        else:
            initvalue_ = until
        self.until = initvalue_
        self.until_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, TimeFrame)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if TimeFrame.subclass:
            return TimeFrame.subclass(*args_, **kwargs_)
        else:
            return TimeFrame(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_from(self):
        return self.from_
    def set_from(self, from_):
        self.from_ = from_
    def get_until(self):
        return self.until
    def set_until(self, until):
        self.until = until
    def _hasContent(self):
        if (
            self.from_ is not None or
            self.until is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TimeFrame', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('TimeFrame')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'TimeFrame':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='TimeFrame')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='TimeFrame', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='TimeFrame'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='TimeFrame', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.from_ is not None:
            namespaceprefix_ = self.from__nsprefix_ + ':' if (UseCapturedNS_ and self.from__nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sfrom>%s</%sfrom>%s' % (namespaceprefix_ , self.gds_format_time(self.from_, input_name='from'), namespaceprefix_ , eol_))
        if self.until is not None:
            namespaceprefix_ = self.until_nsprefix_ + ':' if (UseCapturedNS_ and self.until_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%suntil>%s</%suntil>%s' % (namespaceprefix_ , self.gds_format_time(self.until, input_name='until'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'from':
            sval_ = child_.text
            dval_ = self.gds_parse_time(sval_)
            self.from_ = dval_
            self.from_nsprefix_ = child_.prefix
        elif nodeName_ == 'until':
            sval_ = child_.text
            dval_ = self.gds_parse_time(sval_)
            self.until = dval_
            self.until_nsprefix_ = child_.prefix
# end class TimeFrame


class shipmentNumber(GeneratedsSuper):
    """shipmentNumber -- Can contain any DHL shipmentnumber.
    
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
                CurrentSubclassModule_, shipmentNumber)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if shipmentNumber.subclass:
            return shipmentNumber.subclass(*args_, **kwargs_)
        else:
            return shipmentNumber(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def validate_shipmentNumber(self, value):
        result = True
        # Validate type shipmentNumber, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (

        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='shipmentNumber', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('shipmentNumber')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'shipmentNumber':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='shipmentNumber')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='shipmentNumber', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='shipmentNumber'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='shipmentNumber', fromsubclass_=False, pretty_print=True):
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
# end class shipmentNumber


class ZipType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = "cis"
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ZipType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ZipType.subclass:
            return ZipType.subclass(*args_, **kwargs_)
        else:
            return ZipType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_valueOf_(self): return self.valueOf_
    def set_valueOf_(self, valueOf_): self.valueOf_ = valueOf_
    def validate_ZipType_impl(self, value):
        result = True
        # Validate type ZipType_impl, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 17:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ZipType_impl' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            (1 if type(self.valueOf_) in [int,float] else self.valueOf_)
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ZipType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ZipType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ZipType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ZipType')
        outfile.write('>')
        self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_, pretty_print=pretty_print)
        outfile.write(self.convert_unicode(self.valueOf_))
        outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ZipType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ZipType', fromsubclass_=False, pretty_print=True):
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
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass
# end class ZipType


GDSClassesMapping = {
    'Authentification': AuthentificationType,
    'Origin': CountryType,
    'zip': ZipType,
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
        rootTag = 'xs_string'
        rootClass = xs_string
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
        rootTag = 'xs_string'
        rootClass = xs_string
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
        rootTag = 'xs_string'
        rootClass = xs_string
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:cis="http://dhl.de/webservice/cisbase"')
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
        rootTag = 'xs_string'
        rootClass = xs_string
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from customer_interface import *\n\n')
        sys.stdout.write('import customer_interface as model_\n\n')
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
NamespaceToDefMappings_ = {'http://dhl.de/webservice/cisbase': [('countryISOType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'ST'),
                                      ('ZipType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'ST'),
                                      ('AuthentificationType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT'),
                                      ('NativeAddressType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT'),
                                      ('NativeAddressTypeNew',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT'),
                                      ('ReceiverNativeAddressType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT'),
                                      ('PickupAddressType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT'),
                                      ('DeliveryAddressType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT'),
                                      ('BankType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT'),
                                      ('NameType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT'),
                                      ('ReceiverNameType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT'),
                                      ('CommunicationType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT'),
                                      ('ContactType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT'),
                                      ('PackStationType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT'),
                                      ('PostfilialeType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT'),
                                      ('PostfilialeTypeNoCountry',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT'),
                                      ('ParcelShopType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT'),
                                      ('CustomerType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT'),
                                      ('ErrorType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT'),
                                      ('CountryType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT'),
                                      ('ShipmentNumberType',
                                       './schemas/geschaeftskundenversand-api-3.4.0-schema-cis_base.xsd',
                                       'CT')]}

__all__ = [
    "AuthentificationType",
    "BankType",
    "CommunicationType",
    "ContactType",
    "CountryType",
    "CustomerType",
    "DeliveryAddressType",
    "Dimension",
    "EKP",
    "ErrorType",
    "NameType",
    "NativeAddressType",
    "NativeAddressTypeNew",
    "PackStationType",
    "ParcelShopType",
    "PickupAddressType",
    "PostfilialeType",
    "PostfilialeTypeNoCountry",
    "ReceiverNameType",
    "ReceiverNativeAddressType",
    "ShipmentNumberType",
    "Status",
    "TimeFrame",
    "Version",
    "ZipType",
    "accountNumber",
    "accountNumberExpress",
    "airwayBill",
    "city",
    "identCode",
    "licensePlate",
    "name1",
    "name2",
    "name3",
    "note",
    "partnerID",
    "procedureID",
    "productKey",
    "province",
    "routeCode",
    "routingCode",
    "shipmentNumber",
    "streetNameCode",
    "streetNumberCode"
]
