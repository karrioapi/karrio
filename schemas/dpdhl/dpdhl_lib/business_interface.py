#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Sat Apr 22 21:02:03 2023 by generateDS.py version 2.41.3.
# Python 3.10.6 (main, Mar 10 2023, 10:55:28) [GCC 11.3.0]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './dpdhl_lib/business_interface.py')
#
# Command line arguments:
#   ./schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd
#
# Command line:
#   /home/kserver/Workspace/karrio/.venv/karrio/bin/generateDS --no-namespace-defs -o "./dpdhl_lib/business_interface.py" ./schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd
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


class PaymentTypeType(str, Enum):
    """PaymentTypeType -- Mandatory if unfree is chosen. 0= cash / 1= invoice.
    
    """
    _0='0'
    _1='1'


class activeType(str, Enum):
    """activeType -- Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType20(str, Enum):
    """activeType20 -- Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType21(str, Enum):
    """activeType21 -- Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType23(str, Enum):
    """activeType23 -- Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType25(str, Enum):
    """activeType25 -- Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType27(str, Enum):
    """activeType27 -- Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType30(str, Enum):
    """activeType30 -- Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType31(str, Enum):
    """activeType31 -- Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType32(str, Enum):
    """activeType32 -- Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType34(str, Enum):
    """activeType34 -- Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType35(str, Enum):
    """activeType35 -- Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType37(str, Enum):
    """activeType37 -- Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType39(str, Enum):
    """activeType39 -- Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType41(str, Enum):
    """activeType41 -- Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType42(str, Enum):
    """activeType42 -- Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType43(str, Enum):
    """activeType43 -- Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType44(str, Enum):
    """activeType44 --  Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType45(str, Enum):
    """activeType45 --  Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType46(str, Enum):
    """activeType46 --  Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class activeType47(str, Enum):
    """activeType47 -- Indicates, if the option is on/off
    
    """
    _0='0'
    _1='1'


class exportDocResponseTypeType(str, Enum):
    """exportDocResponseTypeType -- Dial to determine label ouput format. Must be either 'URL' or
    'B64' = Base64encoded: it is possible to request an URL for receiving
    the label as PDF stream, or to request the label as base64encoded binary
    data directly. If not defined by client, web service defaults to 'URL'.
    
    """
    URL='URL'
    B_64='B64'
    ZPL_2='ZPL2'


class exportTypeType(str, Enum):
    """exportTypeType -- Export type
    
    """
    OTHER='OTHER'
    PRESENT='PRESENT'
    COMMERCIAL_SAMPLE='COMMERCIAL_SAMPLE'
    DOCUMENT='DOCUMENT'
    RETURN_OF_GOODS='RETURN_OF_GOODS'
    COMMERCIAL_GOODS='COMMERCIAL_GOODS'


class labelResponseTypeType(str, Enum):
    """labelResponseTypeType -- Dial to determine label ouput format. Must be either 'URL' or
    'B64' = Base64encoded: it is possible to request an URL for receiving
    the label as PDF stream, or to request the label as base64encoded binary
    data directly. If not defined by client, web service defaults to 'URL'.
    
    """
    URL='URL'
    B_64='B64'
    ZPL_2='ZPL2'


class labelResponseTypeType11(str, Enum):
    """labelResponseTypeType11 -- Dial to determine label ouput format. Must be either 'URL' or
    'B64' = Base64encoded: it is possible to request an URL for receiving
    the label as PDF stream, or to request the label as base64encoded binary
    data directly. If not defined by client, web service defaults to 'URL'.
    
    """
    URL='URL'
    B_64='B64'
    ZPL_2='ZPL2'


class labelResponseTypeType4(str, Enum):
    """labelResponseTypeType4 -- Dial to determine label ouput format. Must be either 'URL' or
    'B64' = Base64encoded: it is possible to request an URL for receiving
    the label as PDF stream, or to request the label as base64encoded binary
    data directly. If not defined by client, web service defaults to 'URL'.
    
    """
    URL='URL'
    B_64='B64'
    ZPL_2='ZPL2'


class termsOfTradeType(str, Enum):
    """termsOfTradeType --
    Element provides terms of
    trades, incoterms codes:
    DDP (Delivery Duty Paid)
    DXV (Delivery Duty Paid (excl. VAT))
    DAP (formerly DDU, Delivery At Place)
    DDX (Delivery Duty Paid (excl. Duties, taxes and VAT)
    CPT (Carriage Paid To (within EU only))
    are vaild values.
    
    """
    DDP='DDP'
    DXV='DXV'
    DAP='DAP'
    DDX='DDX'
    CPT='CPT'


class typeType(str, Enum):
    """typeType --  This service defines the handling of parcels that cannot be
    delivered. There are two options: IMMEDIATE (Sending back to sender),
    ABANDONMENT (Abandonment of parcel at the hands of sender (free of charge). The
    definition of undeliverability is country-specific and depends on the
    regulations of the postal company of the receiving country. Usually, if parcels
    cannot be delivered at first try, recipients receive a notification card and can
    pick up their shipment at a local postal office. After the storage period has
    expired, the shipment will be handled according to your choosen endorsement
    option. Shipments that cannot be delivered due to address problems or active
    refusal will be either returned immediately or treated as abandoned.
    
    """
    IMMEDIATE='IMMEDIATE'
    ABANDONMENT='ABANDONMENT'


class typeType38(str, Enum):
    """typeType38 --  Timeframe of delivery, if the option is used: ValidValues are
    10001200: 10:00 until 12:00; 12001400: 12:00 until 14:00 14001600: 14:00 until
    16:00; 16001800: 16:00 until 18:00 18002000: 18:00 until 20:00; 19002100: 19:00
    until 21:00
    
    """
    _1_0001200='10001200'
    _1_2001400='12001400'
    _1_4001600='14001600'
    _1_6001800='16001800'
    _1_8002000='18002000'
    _1_9002100='19002100'


class unitType(str, Enum):
    """unitType -- unit for all measures
    
    """
    MM='mm'
    INCH='inch'


class GetVersionResponse(GeneratedsSuper):
    """GetVersionResponse -- The version of the webservice and the version of the software build.
    Version -- The version of the webservice implementation.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetVersionResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetVersionResponse.subclass:
            return GetVersionResponse.subclass(*args_, **kwargs_)
        else:
            return GetVersionResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def _hasContent(self):
        if (
            self.Version is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetVersionResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetVersionResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetVersionResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetVersionResponse')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetVersionResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetVersionResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetVersionResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
# end class GetVersionResponse


class CreateShipmentOrderRequest(GeneratedsSuper):
    """CreateShipmentOrderRequest -- The shipmentdata for creating a shipment.
    Version -- The version of the webservice implementation for which the
    requesting client is developed.
    ShipmentOrder -- ShipmentOrder is the highest parent element that contains all
    data with respect to one shipment order.
    labelResponseType -- Dial to determine label ouput format. Must be either 'URL' or
    'B64' = Base64encoded: it is possible to request an URL for receiving
    the label as PDF stream, or to request the label as base64encoded binary
    data directly. If not defined by client, web service defaults to 'URL'.
    groupProfileName -- The group profile you select defines the billing numbers you
    can use for creating shipments. To define group profiles please visit
    our business costumer portal.
    labelFormat --  In this optional section you can define the following label
    formats: A4:common label laser printing A4 plain paper; 910-300-700:
    common label laser printing 105 x 205 mm (A5 plain paper, 910-300-700);
    910-300-700-oz: common label laser printing 105 x 205 mm without
    additional barcode labels (A5 plain paper, 910-300-700); 910-300-300:
    common label laser printing 105 x 148 mm (A5 plain paper, 910-300-700);
    910-300-300-oz: common label laser printing 105 x 148 mm without
    additional barcode labels (A5 plain paper, 910-300-300); 910-300-710:
    common label laser printing 105 x 208 mm (910-300-710); 910-300-600:
    common label thermal printing 103 x 199 mm (910-300-600, 910-300-610);
    910-300-400: common label thermal printing 103 x 150 mm (910-300-400,
    910-300-410); 100x70mm: 100 x 70 mm label (only for Warenpost and
    Warenpost International);
    labelFormatRetoure --  In this optional section you can define the following label
    formats: A4:common label laser printing A4 plain paper; 910-300-700:
    common label laser printing 105 x 205 mm (a5 plain paper, 910-300-700);
    910-300-700-oz: common label laser printing 105 x 205 mm without
    additional barcode labels (A5 plain paper, 910-300-700); 910-300-300:
    common label laser printing 105 x 148 mm (A5 plain paper, 910-300-300);
    910-300-300-oz: common label laser printing 105 x 148 mm without
    additional barcode labels (A5 plain paper, 910-300-300); 910-300-710:
    common label laser printing 105 x 208 mm (910-300-710); 910-300-600:
    common label thermal printing 103 x 199 mm (910-300-600, 910-300-610);
    910-300-400: common label thermal printing 103 x 150 mm (910-300-400,
    910-300-410); 100x70mm: 100 x 70 mm label (only for Warenpost and
    Warenpost International);
    combinedPrinting -- To get a single PDF for shipping and return label select this
    option.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, ShipmentOrder=None, labelResponseType=None, groupProfileName=None, labelFormat=None, labelFormatRetoure=None, combinedPrinting=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        if ShipmentOrder is None:
            self.ShipmentOrder = []
        else:
            self.ShipmentOrder = ShipmentOrder
        self.ShipmentOrder_nsprefix_ = None
        self.labelResponseType = labelResponseType
        self.validate_labelResponseTypeType(self.labelResponseType)
        self.labelResponseType_nsprefix_ = None
        self.groupProfileName = groupProfileName
        self.validate_groupProfileNameType(self.groupProfileName)
        self.groupProfileName_nsprefix_ = None
        self.labelFormat = labelFormat
        self.validate_labelFormatType(self.labelFormat)
        self.labelFormat_nsprefix_ = None
        self.labelFormatRetoure = labelFormatRetoure
        self.validate_labelFormatRetoureType(self.labelFormatRetoure)
        self.labelFormatRetoure_nsprefix_ = None
        self.combinedPrinting = combinedPrinting
        self.validate_combinedPrintingType(self.combinedPrinting)
        self.combinedPrinting_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CreateShipmentOrderRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CreateShipmentOrderRequest.subclass:
            return CreateShipmentOrderRequest.subclass(*args_, **kwargs_)
        else:
            return CreateShipmentOrderRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_ShipmentOrder(self):
        return self.ShipmentOrder
    def set_ShipmentOrder(self, ShipmentOrder):
        self.ShipmentOrder = ShipmentOrder
    def add_ShipmentOrder(self, value):
        self.ShipmentOrder.append(value)
    def insert_ShipmentOrder_at(self, index, value):
        self.ShipmentOrder.insert(index, value)
    def replace_ShipmentOrder_at(self, index, value):
        self.ShipmentOrder[index] = value
    def get_labelResponseType(self):
        return self.labelResponseType
    def set_labelResponseType(self, labelResponseType):
        self.labelResponseType = labelResponseType
    def get_groupProfileName(self):
        return self.groupProfileName
    def set_groupProfileName(self, groupProfileName):
        self.groupProfileName = groupProfileName
    def get_labelFormat(self):
        return self.labelFormat
    def set_labelFormat(self, labelFormat):
        self.labelFormat = labelFormat
    def get_labelFormatRetoure(self):
        return self.labelFormatRetoure
    def set_labelFormatRetoure(self, labelFormatRetoure):
        self.labelFormatRetoure = labelFormatRetoure
    def get_combinedPrinting(self):
        return self.combinedPrinting
    def set_combinedPrinting(self, combinedPrinting):
        self.combinedPrinting = combinedPrinting
    def validate_labelResponseTypeType(self, value):
        result = True
        # Validate type labelResponseTypeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            value = value
            enumerations = ['URL', 'B64', 'ZPL2']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on labelResponseTypeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_groupProfileNameType(self, value):
        result = True
        # Validate type groupProfileNameType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def validate_labelFormatType(self, value):
        result = True
        # Validate type labelFormatType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def validate_labelFormatRetoureType(self, value):
        result = True
        # Validate type labelFormatRetoureType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def validate_combinedPrintingType(self, value):
        result = True
        # Validate type combinedPrintingType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def _hasContent(self):
        if (
            self.Version is not None or
            self.ShipmentOrder or
            self.labelResponseType is not None or
            self.groupProfileName is not None or
            self.labelFormat is not None or
            self.labelFormatRetoure is not None or
            self.combinedPrinting is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CreateShipmentOrderRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CreateShipmentOrderRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CreateShipmentOrderRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CreateShipmentOrderRequest')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CreateShipmentOrderRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CreateShipmentOrderRequest'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CreateShipmentOrderRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        for ShipmentOrder_ in self.ShipmentOrder:
            namespaceprefix_ = self.ShipmentOrder_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentOrder_nsprefix_) else ''
            ShipmentOrder_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentOrder', pretty_print=pretty_print)
        if self.labelResponseType is not None:
            namespaceprefix_ = self.labelResponseType_nsprefix_ + ':' if (UseCapturedNS_ and self.labelResponseType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slabelResponseType>%s</%slabelResponseType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.labelResponseType), input_name='labelResponseType')), namespaceprefix_ , eol_))
        if self.groupProfileName is not None:
            namespaceprefix_ = self.groupProfileName_nsprefix_ + ':' if (UseCapturedNS_ and self.groupProfileName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sgroupProfileName>%s</%sgroupProfileName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.groupProfileName), input_name='groupProfileName')), namespaceprefix_ , eol_))
        if self.labelFormat is not None:
            namespaceprefix_ = self.labelFormat_nsprefix_ + ':' if (UseCapturedNS_ and self.labelFormat_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slabelFormat>%s</%slabelFormat>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.labelFormat), input_name='labelFormat')), namespaceprefix_ , eol_))
        if self.labelFormatRetoure is not None:
            namespaceprefix_ = self.labelFormatRetoure_nsprefix_ + ':' if (UseCapturedNS_ and self.labelFormatRetoure_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slabelFormatRetoure>%s</%slabelFormatRetoure>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.labelFormatRetoure), input_name='labelFormatRetoure')), namespaceprefix_ , eol_))
        if self.combinedPrinting is not None:
            namespaceprefix_ = self.combinedPrinting_nsprefix_ + ':' if (UseCapturedNS_ and self.combinedPrinting_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scombinedPrinting>%s</%scombinedPrinting>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.combinedPrinting), input_name='combinedPrinting')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'ShipmentOrder':
            obj_ = ShipmentOrderType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentOrder.append(obj_)
            obj_.original_tagname_ = 'ShipmentOrder'
        elif nodeName_ == 'labelResponseType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'labelResponseType')
            value_ = self.gds_validate_string(value_, node, 'labelResponseType')
            self.labelResponseType = value_
            self.labelResponseType_nsprefix_ = child_.prefix
            # validate type labelResponseTypeType
            self.validate_labelResponseTypeType(self.labelResponseType)
        elif nodeName_ == 'groupProfileName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'groupProfileName')
            value_ = self.gds_validate_string(value_, node, 'groupProfileName')
            self.groupProfileName = value_
            self.groupProfileName_nsprefix_ = child_.prefix
            # validate type groupProfileNameType
            self.validate_groupProfileNameType(self.groupProfileName)
        elif nodeName_ == 'labelFormat':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'labelFormat')
            value_ = self.gds_validate_string(value_, node, 'labelFormat')
            self.labelFormat = value_
            self.labelFormat_nsprefix_ = child_.prefix
            # validate type labelFormatType
            self.validate_labelFormatType(self.labelFormat)
        elif nodeName_ == 'labelFormatRetoure':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'labelFormatRetoure')
            value_ = self.gds_validate_string(value_, node, 'labelFormatRetoure')
            self.labelFormatRetoure = value_
            self.labelFormatRetoure_nsprefix_ = child_.prefix
            # validate type labelFormatRetoureType
            self.validate_labelFormatRetoureType(self.labelFormatRetoure)
        elif nodeName_ == 'combinedPrinting':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'combinedPrinting')
            value_ = self.gds_validate_string(value_, node, 'combinedPrinting')
            self.combinedPrinting = value_
            self.combinedPrinting_nsprefix_ = child_.prefix
            # validate type combinedPrintingType
            self.validate_combinedPrintingType(self.combinedPrinting)
# end class CreateShipmentOrderRequest


class ValidateShipmentOrderRequest(GeneratedsSuper):
    """ValidateShipmentOrderRequest -- The shipmentdata for validating a shipment.
    Version -- The version of the webservice implementation for which the
    requesting client is developed.
    ShipmentOrder -- ShipmentOrder is the highest parent element that contains all
    data with respect to one shipment order.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, ShipmentOrder=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        if ShipmentOrder is None:
            self.ShipmentOrder = []
        else:
            self.ShipmentOrder = ShipmentOrder
        self.ShipmentOrder_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ValidateShipmentOrderRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ValidateShipmentOrderRequest.subclass:
            return ValidateShipmentOrderRequest.subclass(*args_, **kwargs_)
        else:
            return ValidateShipmentOrderRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_ShipmentOrder(self):
        return self.ShipmentOrder
    def set_ShipmentOrder(self, ShipmentOrder):
        self.ShipmentOrder = ShipmentOrder
    def add_ShipmentOrder(self, value):
        self.ShipmentOrder.append(value)
    def insert_ShipmentOrder_at(self, index, value):
        self.ShipmentOrder.insert(index, value)
    def replace_ShipmentOrder_at(self, index, value):
        self.ShipmentOrder[index] = value
    def _hasContent(self):
        if (
            self.Version is not None or
            self.ShipmentOrder
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ValidateShipmentOrderRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ValidateShipmentOrderRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ValidateShipmentOrderRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ValidateShipmentOrderRequest')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ValidateShipmentOrderRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ValidateShipmentOrderRequest'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ValidateShipmentOrderRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        for ShipmentOrder_ in self.ShipmentOrder:
            namespaceprefix_ = self.ShipmentOrder_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentOrder_nsprefix_) else ''
            ShipmentOrder_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentOrder', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'ShipmentOrder':
            obj_ = ValidateShipmentOrderType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentOrder.append(obj_)
            obj_.original_tagname_ = 'ShipmentOrder'
# end class ValidateShipmentOrderRequest


class CreateShipmentOrderResponse(GeneratedsSuper):
    """CreateShipmentOrderResponse -- The status of the operation and the shipment identifier (if available).
    Version -- The version of the webservice implementation.
    Status -- Success status after processing the overall request.
    CreationState -- The operation's success status for every single ShipmentOrder
    will be returned by one CreationState element. It is identifiable via
    SequenceNumber.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, Status=None, CreationState=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
        if CreationState is None:
            self.CreationState = []
        else:
            self.CreationState = CreationState
        self.CreationState_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CreateShipmentOrderResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CreateShipmentOrderResponse.subclass:
            return CreateShipmentOrderResponse.subclass(*args_, **kwargs_)
        else:
            return CreateShipmentOrderResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def get_CreationState(self):
        return self.CreationState
    def set_CreationState(self, CreationState):
        self.CreationState = CreationState
    def add_CreationState(self, value):
        self.CreationState.append(value)
    def insert_CreationState_at(self, index, value):
        self.CreationState.insert(index, value)
    def replace_CreationState_at(self, index, value):
        self.CreationState[index] = value
    def _hasContent(self):
        if (
            self.Version is not None or
            self.Status is not None or
            self.CreationState
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CreateShipmentOrderResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CreateShipmentOrderResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CreateShipmentOrderResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CreateShipmentOrderResponse')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CreateShipmentOrderResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CreateShipmentOrderResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CreateShipmentOrderResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            self.Status.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Status', pretty_print=pretty_print)
        for CreationState_ in self.CreationState:
            namespaceprefix_ = self.CreationState_nsprefix_ + ':' if (UseCapturedNS_ and self.CreationState_nsprefix_) else ''
            CreationState_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CreationState', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'Status':
            obj_ = Statusinformation.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Status = obj_
            obj_.original_tagname_ = 'Status'
        elif nodeName_ == 'CreationState':
            obj_ = CreationState.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CreationState.append(obj_)
            obj_.original_tagname_ = 'CreationState'
# end class CreateShipmentOrderResponse


class ValidateShipmentResponse(GeneratedsSuper):
    """ValidateShipmentResponse -- The status of the operation and the shipment identifier (if available).
    Version -- The version of the webservice implementation.
    Status -- Success status after processing the overall request.
    ValidationState -- The operation's success status for every single ShipmentOrder
    will be returned by one CreationState element. It is identifiable via
    SequenceNumber.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, Status=None, ValidationState=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
        if ValidationState is None:
            self.ValidationState = []
        else:
            self.ValidationState = ValidationState
        self.ValidationState_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ValidateShipmentResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ValidateShipmentResponse.subclass:
            return ValidateShipmentResponse.subclass(*args_, **kwargs_)
        else:
            return ValidateShipmentResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def get_ValidationState(self):
        return self.ValidationState
    def set_ValidationState(self, ValidationState):
        self.ValidationState = ValidationState
    def add_ValidationState(self, value):
        self.ValidationState.append(value)
    def insert_ValidationState_at(self, index, value):
        self.ValidationState.insert(index, value)
    def replace_ValidationState_at(self, index, value):
        self.ValidationState[index] = value
    def _hasContent(self):
        if (
            self.Version is not None or
            self.Status is not None or
            self.ValidationState
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ValidateShipmentResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ValidateShipmentResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ValidateShipmentResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ValidateShipmentResponse')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ValidateShipmentResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ValidateShipmentResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ValidateShipmentResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            self.Status.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Status', pretty_print=pretty_print)
        for ValidationState_ in self.ValidationState:
            namespaceprefix_ = self.ValidationState_nsprefix_ + ':' if (UseCapturedNS_ and self.ValidationState_nsprefix_) else ''
            ValidationState_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ValidationState', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'Status':
            obj_ = Statusinformation.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Status = obj_
            obj_.original_tagname_ = 'Status'
        elif nodeName_ == 'ValidationState':
            obj_ = ValidationState.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ValidationState.append(obj_)
            obj_.original_tagname_ = 'ValidationState'
# end class ValidateShipmentResponse


class GetLabelRequest(GeneratedsSuper):
    """GetLabelRequest -- The identifier for the shipment for which the label url is requested.
    Version -- The version of the webservice implementation for which the
    requesting client is developed.
    labelResponseType -- Dial to determine label ouput format. Must be either 'URL' or
    'B64' = Base64encoded: it is possible to request an URL for receiving
    the label as PDF stream, or to request the label as base64encoded binary
    data directly. If not defined by client, web service defaults to 'URL'.
    groupProfileName -- The group profile you select defines the billing numbers you
    can use for creating shipments. To define group profiles please visit
    our business costumer portal. The group profile defines the shipments
    you can get documents for. The shipment needs to have an account/billing
    number allocated to the group profile. To define group profiles please
    visit our business costumer portal.
    labelFormat --  In this optional section you can define the following label
    formats: A4:common label laser printing A4 plain paper; 910-300-700:
    common label laser printing 105 x 205 mm (910-300-700); 910-300-700-oz:
    common label laser printing 105 x 205 mm without additional barcode
    labels (910-300-700); 910-300-300: common label laser printing 105 x 148
    mm (910-300-700); 910-300-300-oz: common label laser printing 105 x 148
    mm without additional barcode labels (910-300-300); 910-300-710: common
    label laser printing 105 x 208 mm (910-300-710); 910-300-600: common
    label thermal printing 103 x 199 mm (910-300-600, 910-300-610);
    910-300-400: common label thermal printing 103 x 150 mm (910-300-400,
    910-300-410); 100x70mm: 100 x 70 mm label (only for Warenpost and
    Warenpost International);
    labelFormatRetoure --  In this optional section you can define the following label
    formats: A4:common label laser printing A4 plain paper; 910-300-700:
    common label laser printing 105 x 205 mm (910-300-700); 910-300-700-oz:
    common label laser printing 105 x 205 mm without additional barcode
    labels (910-300-700); 910-300-300: common label laser printing 105 x 148
    mm (910-300-700); 910-300-300-oz: common label laser printing 105 x 148
    mm without additional barcode labels (910-300-300); 910-300-710: common
    label laser printing 105 x 208 mm (910-300-710); 910-300-600: common
    label thermal printing 103 x 199 mm (910-300-600, 910-300-610);
    910-300-400: common label thermal printing 103 x 150 mm (910-300-400,
    910-300-410); 100x70mm: 100 x 70 mm label (only for Warenpost and
    Warenpost International);
    combinedPrinting -- To get a single PDF for shipping and return label select this
    option.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, shipmentNumber=None, labelResponseType=None, groupProfileName=None, labelFormat=None, labelFormatRetoure=None, combinedPrinting=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        if shipmentNumber is None:
            self.shipmentNumber = []
        else:
            self.shipmentNumber = shipmentNumber
        self.shipmentNumber_nsprefix_ = None
        self.labelResponseType = labelResponseType
        self.validate_labelResponseTypeType4(self.labelResponseType)
        self.labelResponseType_nsprefix_ = None
        self.groupProfileName = groupProfileName
        self.validate_groupProfileNameType5(self.groupProfileName)
        self.groupProfileName_nsprefix_ = None
        self.labelFormat = labelFormat
        self.validate_labelFormatType6(self.labelFormat)
        self.labelFormat_nsprefix_ = None
        self.labelFormatRetoure = labelFormatRetoure
        self.validate_labelFormatRetoureType7(self.labelFormatRetoure)
        self.labelFormatRetoure_nsprefix_ = None
        self.combinedPrinting = combinedPrinting
        self.validate_combinedPrintingType8(self.combinedPrinting)
        self.combinedPrinting_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetLabelRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetLabelRequest.subclass:
            return GetLabelRequest.subclass(*args_, **kwargs_)
        else:
            return GetLabelRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_shipmentNumber(self):
        return self.shipmentNumber
    def set_shipmentNumber(self, shipmentNumber):
        self.shipmentNumber = shipmentNumber
    def add_shipmentNumber(self, value):
        self.shipmentNumber.append(value)
    def insert_shipmentNumber_at(self, index, value):
        self.shipmentNumber.insert(index, value)
    def replace_shipmentNumber_at(self, index, value):
        self.shipmentNumber[index] = value
    def get_labelResponseType(self):
        return self.labelResponseType
    def set_labelResponseType(self, labelResponseType):
        self.labelResponseType = labelResponseType
    def get_groupProfileName(self):
        return self.groupProfileName
    def set_groupProfileName(self, groupProfileName):
        self.groupProfileName = groupProfileName
    def get_labelFormat(self):
        return self.labelFormat
    def set_labelFormat(self, labelFormat):
        self.labelFormat = labelFormat
    def get_labelFormatRetoure(self):
        return self.labelFormatRetoure
    def set_labelFormatRetoure(self, labelFormatRetoure):
        self.labelFormatRetoure = labelFormatRetoure
    def get_combinedPrinting(self):
        return self.combinedPrinting
    def set_combinedPrinting(self, combinedPrinting):
        self.combinedPrinting = combinedPrinting
    def validate_shipmentNumber(self, value):
        result = True
        # Validate type shipmentNumber, a restriction on xs:string.
        pass
        return result
    def validate_labelResponseTypeType4(self, value):
        result = True
        # Validate type labelResponseTypeType4, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            value = value
            enumerations = ['URL', 'B64', 'ZPL2']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on labelResponseTypeType4' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_groupProfileNameType5(self, value):
        result = True
        # Validate type groupProfileNameType5, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def validate_labelFormatType6(self, value):
        result = True
        # Validate type labelFormatType6, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def validate_labelFormatRetoureType7(self, value):
        result = True
        # Validate type labelFormatRetoureType7, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def validate_combinedPrintingType8(self, value):
        result = True
        # Validate type combinedPrintingType8, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def _hasContent(self):
        if (
            self.Version is not None or
            self.shipmentNumber or
            self.labelResponseType is not None or
            self.groupProfileName is not None or
            self.labelFormat is not None or
            self.labelFormatRetoure is not None or
            self.combinedPrinting is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLabelRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetLabelRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetLabelRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetLabelRequest')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetLabelRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetLabelRequest'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLabelRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        for shipmentNumber_ in self.shipmentNumber:
            namespaceprefix_ = self.shipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.shipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sshipmentNumber>%s</%sshipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(shipmentNumber_), input_name='shipmentNumber')), namespaceprefix_ , eol_))
        if self.labelResponseType is not None:
            namespaceprefix_ = self.labelResponseType_nsprefix_ + ':' if (UseCapturedNS_ and self.labelResponseType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slabelResponseType>%s</%slabelResponseType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.labelResponseType), input_name='labelResponseType')), namespaceprefix_ , eol_))
        if self.groupProfileName is not None:
            namespaceprefix_ = self.groupProfileName_nsprefix_ + ':' if (UseCapturedNS_ and self.groupProfileName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sgroupProfileName>%s</%sgroupProfileName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.groupProfileName), input_name='groupProfileName')), namespaceprefix_ , eol_))
        if self.labelFormat is not None:
            namespaceprefix_ = self.labelFormat_nsprefix_ + ':' if (UseCapturedNS_ and self.labelFormat_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slabelFormat>%s</%slabelFormat>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.labelFormat), input_name='labelFormat')), namespaceprefix_ , eol_))
        if self.labelFormatRetoure is not None:
            namespaceprefix_ = self.labelFormatRetoure_nsprefix_ + ':' if (UseCapturedNS_ and self.labelFormatRetoure_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slabelFormatRetoure>%s</%slabelFormatRetoure>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.labelFormatRetoure), input_name='labelFormatRetoure')), namespaceprefix_ , eol_))
        if self.combinedPrinting is not None:
            namespaceprefix_ = self.combinedPrinting_nsprefix_ + ':' if (UseCapturedNS_ and self.combinedPrinting_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scombinedPrinting>%s</%scombinedPrinting>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.combinedPrinting), input_name='combinedPrinting')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'shipmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'shipmentNumber')
            value_ = self.gds_validate_string(value_, node, 'shipmentNumber')
            self.shipmentNumber.append(value_)
            self.shipmentNumber_nsprefix_ = child_.prefix
            # validate type shipmentNumber
            self.validate_shipmentNumber(self.shipmentNumber[-1])
        elif nodeName_ == 'labelResponseType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'labelResponseType')
            value_ = self.gds_validate_string(value_, node, 'labelResponseType')
            self.labelResponseType = value_
            self.labelResponseType_nsprefix_ = child_.prefix
            # validate type labelResponseTypeType4
            self.validate_labelResponseTypeType4(self.labelResponseType)
        elif nodeName_ == 'groupProfileName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'groupProfileName')
            value_ = self.gds_validate_string(value_, node, 'groupProfileName')
            self.groupProfileName = value_
            self.groupProfileName_nsprefix_ = child_.prefix
            # validate type groupProfileNameType5
            self.validate_groupProfileNameType5(self.groupProfileName)
        elif nodeName_ == 'labelFormat':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'labelFormat')
            value_ = self.gds_validate_string(value_, node, 'labelFormat')
            self.labelFormat = value_
            self.labelFormat_nsprefix_ = child_.prefix
            # validate type labelFormatType6
            self.validate_labelFormatType6(self.labelFormat)
        elif nodeName_ == 'labelFormatRetoure':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'labelFormatRetoure')
            value_ = self.gds_validate_string(value_, node, 'labelFormatRetoure')
            self.labelFormatRetoure = value_
            self.labelFormatRetoure_nsprefix_ = child_.prefix
            # validate type labelFormatRetoureType7
            self.validate_labelFormatRetoureType7(self.labelFormatRetoure)
        elif nodeName_ == 'combinedPrinting':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'combinedPrinting')
            value_ = self.gds_validate_string(value_, node, 'combinedPrinting')
            self.combinedPrinting = value_
            self.combinedPrinting_nsprefix_ = child_.prefix
            # validate type combinedPrintingType8
            self.validate_combinedPrintingType8(self.combinedPrinting)
# end class GetLabelRequest


class GetLabelResponse(GeneratedsSuper):
    """GetLabelResponse -- The status of the operation and requested urls for getting the label.
    Version -- The version of the webservice implementation.
    Status -- Success status after processing the overall request.
    LabelData -- For every ShipmentNumber requested, one LabelData node is
    returned that contains the status of the label retrieval operation and
    the URL for the label (if available).
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, Status=None, LabelData=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
        if LabelData is None:
            self.LabelData = []
        else:
            self.LabelData = LabelData
        self.LabelData_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetLabelResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetLabelResponse.subclass:
            return GetLabelResponse.subclass(*args_, **kwargs_)
        else:
            return GetLabelResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def get_LabelData(self):
        return self.LabelData
    def set_LabelData(self, LabelData):
        self.LabelData = LabelData
    def add_LabelData(self, value):
        self.LabelData.append(value)
    def insert_LabelData_at(self, index, value):
        self.LabelData.insert(index, value)
    def replace_LabelData_at(self, index, value):
        self.LabelData[index] = value
    def _hasContent(self):
        if (
            self.Version is not None or
            self.Status is not None or
            self.LabelData
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLabelResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetLabelResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetLabelResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetLabelResponse')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetLabelResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetLabelResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetLabelResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            self.Status.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Status', pretty_print=pretty_print)
        for LabelData_ in self.LabelData:
            namespaceprefix_ = self.LabelData_nsprefix_ + ':' if (UseCapturedNS_ and self.LabelData_nsprefix_) else ''
            LabelData_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='LabelData', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'Status':
            obj_ = Statusinformation.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Status = obj_
            obj_.original_tagname_ = 'Status'
        elif nodeName_ == 'LabelData':
            obj_ = LabelData.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LabelData.append(obj_)
            obj_.original_tagname_ = 'LabelData'
# end class GetLabelResponse


class DoManifestRequest(GeneratedsSuper):
    """DoManifestRequest -- Manifests one ore more shipments.
    Version -- The version of the webservice implementation for which the
    requesting client is developed.
    shipmentNumber --  Contains a shipment number. Any number of a printed
    shipment not already manifested can be used. A Request can contain
    the element up to 50 times. Requests need to either contain at least
    one times shipmentNumber or allshipments. Requests cannot contain
    shipmentNumber and allShipments at the same time.
    allShipments --  Manifests all shipments. Can be used instead the element
    “
    shipmentNumber
    ”
    . The element is used without a value, e.g.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, shipmentNumber=None, allShipments=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        if shipmentNumber is None:
            self.shipmentNumber = []
        else:
            self.shipmentNumber = shipmentNumber
        self.shipmentNumber_nsprefix_ = None
        self.allShipments = allShipments
        self.allShipments_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DoManifestRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DoManifestRequest.subclass:
            return DoManifestRequest.subclass(*args_, **kwargs_)
        else:
            return DoManifestRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_shipmentNumber(self):
        return self.shipmentNumber
    def set_shipmentNumber(self, shipmentNumber):
        self.shipmentNumber = shipmentNumber
    def add_shipmentNumber(self, value):
        self.shipmentNumber.append(value)
    def insert_shipmentNumber_at(self, index, value):
        self.shipmentNumber.insert(index, value)
    def replace_shipmentNumber_at(self, index, value):
        self.shipmentNumber[index] = value
    def get_allShipments(self):
        return self.allShipments
    def set_allShipments(self, allShipments):
        self.allShipments = allShipments
    def validate_shipmentNumber(self, value):
        result = True
        # Validate type shipmentNumber, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.Version is not None or
            self.shipmentNumber or
            self.allShipments is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DoManifestRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DoManifestRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DoManifestRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DoManifestRequest')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DoManifestRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DoManifestRequest'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DoManifestRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        for shipmentNumber_ in self.shipmentNumber:
            namespaceprefix_ = self.shipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.shipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sshipmentNumber>%s</%sshipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(shipmentNumber_), input_name='shipmentNumber')), namespaceprefix_ , eol_))
        if self.allShipments is not None:
            namespaceprefix_ = self.allShipments_nsprefix_ + ':' if (UseCapturedNS_ and self.allShipments_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sallShipments>%s</%sallShipments>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.allShipments), input_name='allShipments')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'shipmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'shipmentNumber')
            value_ = self.gds_validate_string(value_, node, 'shipmentNumber')
            self.shipmentNumber.append(value_)
            self.shipmentNumber_nsprefix_ = child_.prefix
            # validate type shipmentNumber
            self.validate_shipmentNumber(self.shipmentNumber[-1])
        elif nodeName_ == 'allShipments':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'allShipments')
            value_ = self.gds_validate_string(value_, node, 'allShipments')
            self.allShipments = value_
            self.allShipments_nsprefix_ = child_.prefix
# end class DoManifestRequest


class allShipments(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, allShipments)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if allShipments.subclass:
            return allShipments.subclass(*args_, **kwargs_)
        else:
            return allShipments(*args_, **kwargs_)
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
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='allShipments', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('allShipments')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'allShipments':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='allShipments')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='allShipments', pretty_print=pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='allShipments'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='allShipments', fromsubclass_=False, pretty_print=True):
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
# end class allShipments


class DoManifestResponse(GeneratedsSuper):
    """DoManifestResponse -- The status of the operation
    Version --  The version of the webservice implementation.
    Status -- Status of the request (value of zero means, the request was
    processed without error; value greater than zero indicates that an error
    occurred).
    ManifestState -- The status of the operation for the corresponding shipment.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, Status=None, ManifestState=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
        if ManifestState is None:
            self.ManifestState = []
        else:
            self.ManifestState = ManifestState
        self.ManifestState_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DoManifestResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DoManifestResponse.subclass:
            return DoManifestResponse.subclass(*args_, **kwargs_)
        else:
            return DoManifestResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def get_ManifestState(self):
        return self.ManifestState
    def set_ManifestState(self, ManifestState):
        self.ManifestState = ManifestState
    def add_ManifestState(self, value):
        self.ManifestState.append(value)
    def insert_ManifestState_at(self, index, value):
        self.ManifestState.insert(index, value)
    def replace_ManifestState_at(self, index, value):
        self.ManifestState[index] = value
    def _hasContent(self):
        if (
            self.Version is not None or
            self.Status is not None or
            self.ManifestState
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DoManifestResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DoManifestResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DoManifestResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DoManifestResponse')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DoManifestResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DoManifestResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DoManifestResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            self.Status.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Status', pretty_print=pretty_print)
        for ManifestState_ in self.ManifestState:
            namespaceprefix_ = self.ManifestState_nsprefix_ + ':' if (UseCapturedNS_ and self.ManifestState_nsprefix_) else ''
            ManifestState_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ManifestState', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'Status':
            obj_ = Statusinformation.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Status = obj_
            obj_.original_tagname_ = 'Status'
        elif nodeName_ == 'ManifestState':
            obj_ = ManifestState.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ManifestState.append(obj_)
            obj_.original_tagname_ = 'ManifestState'
# end class DoManifestResponse


class DeleteShipmentOrderRequest(GeneratedsSuper):
    """DeleteShipmentOrderRequest --  The identifier for the shipment which should be deleted.
    Version --  The version of the webservice implementation for which the
    requesting client is developed.
    shipmentNumber --  In order to delete previously created DD shipment orders,
    ShipmentNumber. ShipmentNumber is required. This parent element inherits
    from ShipmentNumberType, therefore all following subelements are valid
    according to schema, however the web service accepts shipmentNumber
    only. Note: you can delete more than one shipment by passing multiple
    ShipmentNumber containers.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, shipmentNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        if shipmentNumber is None:
            self.shipmentNumber = []
        else:
            self.shipmentNumber = shipmentNumber
        self.shipmentNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DeleteShipmentOrderRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DeleteShipmentOrderRequest.subclass:
            return DeleteShipmentOrderRequest.subclass(*args_, **kwargs_)
        else:
            return DeleteShipmentOrderRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_shipmentNumber(self):
        return self.shipmentNumber
    def set_shipmentNumber(self, shipmentNumber):
        self.shipmentNumber = shipmentNumber
    def add_shipmentNumber(self, value):
        self.shipmentNumber.append(value)
    def insert_shipmentNumber_at(self, index, value):
        self.shipmentNumber.insert(index, value)
    def replace_shipmentNumber_at(self, index, value):
        self.shipmentNumber[index] = value
    def validate_shipmentNumber(self, value):
        result = True
        # Validate type shipmentNumber, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.Version is not None or
            self.shipmentNumber
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeleteShipmentOrderRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DeleteShipmentOrderRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DeleteShipmentOrderRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DeleteShipmentOrderRequest')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DeleteShipmentOrderRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DeleteShipmentOrderRequest'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeleteShipmentOrderRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        for shipmentNumber_ in self.shipmentNumber:
            namespaceprefix_ = self.shipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.shipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sshipmentNumber>%s</%sshipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(shipmentNumber_), input_name='shipmentNumber')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'shipmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'shipmentNumber')
            value_ = self.gds_validate_string(value_, node, 'shipmentNumber')
            self.shipmentNumber.append(value_)
            self.shipmentNumber_nsprefix_ = child_.prefix
            # validate type shipmentNumber
            self.validate_shipmentNumber(self.shipmentNumber[-1])
# end class DeleteShipmentOrderRequest


class DeleteShipmentOrderResponse(GeneratedsSuper):
    """DeleteShipmentOrderResponse -- The status of the operation.
    Version -- The version of the webservice implementation.
    Status -- Success status after processing the overall request.
    DeletionState --  For every ShipmentNumber requested, one DeletionState node
    is returned that contains the status of the respective deletion
    operation.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, Status=None, DeletionState=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
        if DeletionState is None:
            self.DeletionState = []
        else:
            self.DeletionState = DeletionState
        self.DeletionState_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DeleteShipmentOrderResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DeleteShipmentOrderResponse.subclass:
            return DeleteShipmentOrderResponse.subclass(*args_, **kwargs_)
        else:
            return DeleteShipmentOrderResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def get_DeletionState(self):
        return self.DeletionState
    def set_DeletionState(self, DeletionState):
        self.DeletionState = DeletionState
    def add_DeletionState(self, value):
        self.DeletionState.append(value)
    def insert_DeletionState_at(self, index, value):
        self.DeletionState.insert(index, value)
    def replace_DeletionState_at(self, index, value):
        self.DeletionState[index] = value
    def _hasContent(self):
        if (
            self.Version is not None or
            self.Status is not None or
            self.DeletionState
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeleteShipmentOrderResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DeleteShipmentOrderResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DeleteShipmentOrderResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DeleteShipmentOrderResponse')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DeleteShipmentOrderResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DeleteShipmentOrderResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeleteShipmentOrderResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            self.Status.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Status', pretty_print=pretty_print)
        for DeletionState_ in self.DeletionState:
            namespaceprefix_ = self.DeletionState_nsprefix_ + ':' if (UseCapturedNS_ and self.DeletionState_nsprefix_) else ''
            DeletionState_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DeletionState', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'Status':
            obj_ = Statusinformation.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Status = obj_
            obj_.original_tagname_ = 'Status'
        elif nodeName_ == 'DeletionState':
            obj_ = DeletionState.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DeletionState.append(obj_)
            obj_.original_tagname_ = 'DeletionState'
# end class DeleteShipmentOrderResponse


class GetExportDocRequest(GeneratedsSuper):
    """GetExportDocRequest --  The identifier for the shipment for which the export document url is
    requested.
    Version -- The version of the webservice implementation for which the
    requesting client is developed.
    shipmentNumber -- To request export documents, ShipmentNumber. ShipmentNumber
    is required. This parent element inherits from ShipmentNumberType,
    therefore all following subelements are valid according to schema,
    however the web service accepts shipmentNumber only.
    exportDocResponseType -- Dial to determine label ouput format. Must be either 'URL' or
    'B64' = Base64encoded: it is possible to request an URL for receiving
    the label as PDF stream, or to request the label as base64encoded binary
    data directly. If not defined by client, web service defaults to 'URL'.
    groupProfileName -- The group profile you select defines the billing numbers you
    can use for creating shipments. To define group profiles please visit
    our business costumer portal. The group profile defines the shipments
    you can get documents for. The shipment needs to have an account/billing
    number allocated to the group profile. To define group profiles please
    visit our business costumer portal.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, shipmentNumber=None, exportDocResponseType=None, groupProfileName=None, combinedPrinting=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        if shipmentNumber is None:
            self.shipmentNumber = []
        else:
            self.shipmentNumber = shipmentNumber
        self.shipmentNumber_nsprefix_ = None
        self.exportDocResponseType = exportDocResponseType
        self.validate_exportDocResponseTypeType(self.exportDocResponseType)
        self.exportDocResponseType_nsprefix_ = None
        self.groupProfileName = groupProfileName
        self.validate_groupProfileNameType9(self.groupProfileName)
        self.groupProfileName_nsprefix_ = None
        self.combinedPrinting = combinedPrinting
        self.validate_combinedPrintingType10(self.combinedPrinting)
        self.combinedPrinting_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetExportDocRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetExportDocRequest.subclass:
            return GetExportDocRequest.subclass(*args_, **kwargs_)
        else:
            return GetExportDocRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_shipmentNumber(self):
        return self.shipmentNumber
    def set_shipmentNumber(self, shipmentNumber):
        self.shipmentNumber = shipmentNumber
    def add_shipmentNumber(self, value):
        self.shipmentNumber.append(value)
    def insert_shipmentNumber_at(self, index, value):
        self.shipmentNumber.insert(index, value)
    def replace_shipmentNumber_at(self, index, value):
        self.shipmentNumber[index] = value
    def get_exportDocResponseType(self):
        return self.exportDocResponseType
    def set_exportDocResponseType(self, exportDocResponseType):
        self.exportDocResponseType = exportDocResponseType
    def get_groupProfileName(self):
        return self.groupProfileName
    def set_groupProfileName(self, groupProfileName):
        self.groupProfileName = groupProfileName
    def get_combinedPrinting(self):
        return self.combinedPrinting
    def set_combinedPrinting(self, combinedPrinting):
        self.combinedPrinting = combinedPrinting
    def validate_shipmentNumber(self, value):
        result = True
        # Validate type shipmentNumber, a restriction on xs:string.
        pass
        return result
    def validate_exportDocResponseTypeType(self, value):
        result = True
        # Validate type exportDocResponseTypeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            value = value
            enumerations = ['URL', 'B64', 'ZPL2']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on exportDocResponseTypeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_groupProfileNameType9(self, value):
        result = True
        # Validate type groupProfileNameType9, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def validate_combinedPrintingType10(self, value):
        result = True
        # Validate type combinedPrintingType10, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def _hasContent(self):
        if (
            self.Version is not None or
            self.shipmentNumber or
            self.exportDocResponseType is not None or
            self.groupProfileName is not None or
            self.combinedPrinting is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetExportDocRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetExportDocRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetExportDocRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetExportDocRequest')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetExportDocRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetExportDocRequest'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetExportDocRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        for shipmentNumber_ in self.shipmentNumber:
            namespaceprefix_ = self.shipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.shipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sshipmentNumber>%s</%sshipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(shipmentNumber_), input_name='shipmentNumber')), namespaceprefix_ , eol_))
        if self.exportDocResponseType is not None:
            namespaceprefix_ = self.exportDocResponseType_nsprefix_ + ':' if (UseCapturedNS_ and self.exportDocResponseType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sexportDocResponseType>%s</%sexportDocResponseType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.exportDocResponseType), input_name='exportDocResponseType')), namespaceprefix_ , eol_))
        if self.groupProfileName is not None:
            namespaceprefix_ = self.groupProfileName_nsprefix_ + ':' if (UseCapturedNS_ and self.groupProfileName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sgroupProfileName>%s</%sgroupProfileName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.groupProfileName), input_name='groupProfileName')), namespaceprefix_ , eol_))
        if self.combinedPrinting is not None:
            namespaceprefix_ = self.combinedPrinting_nsprefix_ + ':' if (UseCapturedNS_ and self.combinedPrinting_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scombinedPrinting>%s</%scombinedPrinting>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.combinedPrinting), input_name='combinedPrinting')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'shipmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'shipmentNumber')
            value_ = self.gds_validate_string(value_, node, 'shipmentNumber')
            self.shipmentNumber.append(value_)
            self.shipmentNumber_nsprefix_ = child_.prefix
            # validate type shipmentNumber
            self.validate_shipmentNumber(self.shipmentNumber[-1])
        elif nodeName_ == 'exportDocResponseType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'exportDocResponseType')
            value_ = self.gds_validate_string(value_, node, 'exportDocResponseType')
            self.exportDocResponseType = value_
            self.exportDocResponseType_nsprefix_ = child_.prefix
            # validate type exportDocResponseTypeType
            self.validate_exportDocResponseTypeType(self.exportDocResponseType)
        elif nodeName_ == 'groupProfileName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'groupProfileName')
            value_ = self.gds_validate_string(value_, node, 'groupProfileName')
            self.groupProfileName = value_
            self.groupProfileName_nsprefix_ = child_.prefix
            # validate type groupProfileNameType9
            self.validate_groupProfileNameType9(self.groupProfileName)
        elif nodeName_ == 'combinedPrinting':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'combinedPrinting')
            value_ = self.gds_validate_string(value_, node, 'combinedPrinting')
            self.combinedPrinting = value_
            self.combinedPrinting_nsprefix_ = child_.prefix
            # validate type combinedPrintingType10
            self.validate_combinedPrintingType10(self.combinedPrinting)
# end class GetExportDocRequest


class GetExportDocResponse(GeneratedsSuper):
    """GetExportDocResponse -- The status of the operation and requested export document.
    Version -- The version of the webservice implementation.
    Status -- Status of the request (value of zero means, the request was
    processed without error; value greater than zero indicates that an error
    occurred).
    ExportDocData -- Contains the result of the document processing: in case of no
    errors, a base64 encoded PDF is contained; also, the status of this
    particular document generation and the passed shipment number are
    returned.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, Status=None, ExportDocData=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
        if ExportDocData is None:
            self.ExportDocData = []
        else:
            self.ExportDocData = ExportDocData
        self.ExportDocData_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetExportDocResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetExportDocResponse.subclass:
            return GetExportDocResponse.subclass(*args_, **kwargs_)
        else:
            return GetExportDocResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def get_ExportDocData(self):
        return self.ExportDocData
    def set_ExportDocData(self, ExportDocData):
        self.ExportDocData = ExportDocData
    def add_ExportDocData(self, value):
        self.ExportDocData.append(value)
    def insert_ExportDocData_at(self, index, value):
        self.ExportDocData.insert(index, value)
    def replace_ExportDocData_at(self, index, value):
        self.ExportDocData[index] = value
    def _hasContent(self):
        if (
            self.Version is not None or
            self.Status is not None or
            self.ExportDocData
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetExportDocResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetExportDocResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetExportDocResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetExportDocResponse')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetExportDocResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetExportDocResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetExportDocResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            self.Status.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Status', pretty_print=pretty_print)
        for ExportDocData_ in self.ExportDocData:
            namespaceprefix_ = self.ExportDocData_nsprefix_ + ':' if (UseCapturedNS_ and self.ExportDocData_nsprefix_) else ''
            ExportDocData_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ExportDocData', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'Status':
            obj_ = Statusinformation.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Status = obj_
            obj_.original_tagname_ = 'Status'
        elif nodeName_ == 'ExportDocData':
            obj_ = ExportDocData.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ExportDocData.append(obj_)
            obj_.original_tagname_ = 'ExportDocData'
# end class GetExportDocResponse


class GetManifestRequest(GeneratedsSuper):
    """GetManifestRequest -- The request data for the manifest document
    Version -- The version of the webservice implementation for which the
    requesting client is developed.
    manifestDate -- Date in format yyyy-mm-dd
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, manifestDate=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        self.manifestDate = manifestDate
        self.manifestDate_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetManifestRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetManifestRequest.subclass:
            return GetManifestRequest.subclass(*args_, **kwargs_)
        else:
            return GetManifestRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_manifestDate(self):
        return self.manifestDate
    def set_manifestDate(self, manifestDate):
        self.manifestDate = manifestDate
    def _hasContent(self):
        if (
            self.Version is not None or
            self.manifestDate is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetManifestRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetManifestRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetManifestRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetManifestRequest')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetManifestRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetManifestRequest'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetManifestRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.manifestDate is not None:
            namespaceprefix_ = self.manifestDate_nsprefix_ + ':' if (UseCapturedNS_ and self.manifestDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smanifestDate>%s</%smanifestDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.manifestDate), input_name='manifestDate')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'manifestDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'manifestDate')
            value_ = self.gds_validate_string(value_, node, 'manifestDate')
            self.manifestDate = value_
            self.manifestDate_nsprefix_ = child_.prefix
# end class GetManifestRequest


class GetManifestResponse(GeneratedsSuper):
    """GetManifestResponse -- The status of the operation and requested export document.
    Version -- The version of the webservice implementation.
    Status -- Status of the request (value of zero means, the request was
    processed without error; value greater than zero indicates that an error
    occurred).
    manifestData -- The Base64 encoded pdf data for receiving the manifest.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, Status=None, manifestData=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
        self.manifestData = manifestData
        self.manifestData_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, GetManifestResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if GetManifestResponse.subclass:
            return GetManifestResponse.subclass(*args_, **kwargs_)
        else:
            return GetManifestResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def get_manifestData(self):
        return self.manifestData
    def set_manifestData(self, manifestData):
        self.manifestData = manifestData
    def _hasContent(self):
        if (
            self.Version is not None or
            self.Status is not None or
            self.manifestData is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetManifestResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('GetManifestResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'GetManifestResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='GetManifestResponse')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='GetManifestResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='GetManifestResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='GetManifestResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            self.Status.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Status', pretty_print=pretty_print)
        if self.manifestData is not None:
            namespaceprefix_ = self.manifestData_nsprefix_ + ':' if (UseCapturedNS_ and self.manifestData_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%smanifestData>%s</%smanifestData>%s' % (namespaceprefix_ , self.gds_format_base64(self.manifestData, input_name='manifestData'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'Status':
            obj_ = Statusinformation.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Status = obj_
            obj_.original_tagname_ = 'Status'
        elif nodeName_ == 'manifestData':
            sval_ = child_.text
            if sval_ is not None:
                try:
                    bval_ = base64.b64decode(sval_)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(child_, 'requires base64 encoded string: %s' % exp)
                bval_ = self.gds_validate_base64(bval_, node, 'manifestData')
            else:
                bval_ = None
            self.manifestData = bval_
            self.manifestData_nsprefix_ = child_.prefix
# end class GetManifestResponse


class UpdateShipmentOrderRequest(GeneratedsSuper):
    """UpdateShipmentOrderRequest -- The shipmentdata for creating a shipment.
    Version -- The version of the webservice implementation for which the
    requesting client is developed.
    shipmentNumber -- The ShipmentNumber of the shipment, which sould be updated.
    ShipmentNumber is required. This parent element inherits from
    ShipmentNumberType, therefore all following subelements are valid
    according to schema, however the web service accepts shipmentNumber
    only.
    ShipmentOrder -- ShipmentOrder contains an update of all data of the selected
    shipment order.
    labelResponseType -- Dial to determine label ouput format. Must be either 'URL' or
    'B64' = Base64encoded: it is possible to request an URL for receiving
    the label as PDF stream, or to request the label as base64encoded binary
    data directly. If not defined by client, web service defaults to 'URL'.
    groupProfileName -- The group profile you select defines the billing numbers you
    can use for creating shipments. To define group profiles please visit
    our business costumer portal.
    labelFormat --  In this optional section you can define the following label
    formats: A4:common label laser printing A4 plain paper; 910-300-700:
    common label laser printing 105 x 205 mm (910-300-700); 910-300-700-oz:
    common label laser printing 105 x 205 mm without additional barcode
    labels (910-300-700); 910-300-300: common label laser printing 105 x 148
    mm (910-300-700); 910-300-300-oz: common label laser printing 105 x 148
    mm without additional barcode labels (910-300-300); 910-300-710: common
    label laser printing 105 x 208 mm (910-300-710); 910-300-600: common
    label thermal printing 103 x 199 mm (910-300-600, 910-300-610);
    910-300-400: common label thermal printing 103 x 150 mm (910-300-400,
    910-300-410); 100x70mm: 100 x 70 mm label (only for Warenpost and
    Warenpost International);
    labelFormatRetoure --  In this optional section you can define the following label
    formats: A4:common label laser printing A4 plain paper; 910-300-700:
    common label laser printing 105 x 205 mm (910-300-700); 910-300-700-oz:
    common label laser printing 105 x 205 mm without additional barcode
    labels (910-300-700); 910-300-300: common label laser printing 105 x 148
    mm (910-300-700); 910-300-300-oz: common label laser printing 105 x 148
    mm without additional barcode labels (910-300-300); 910-300-710: common
    label laser printing 105 x 208 mm (910-300-710); 910-300-600: common
    label thermal printing 103 x 199 mm (910-300-600, 910-300-610);
    910-300-400: common label thermal printing 103 x 150 mm (910-300-400,
    910-300-410); 100x70mm: 100 x 70 mm label (only for Warenpost and
    Warenpost International);
    combinedPrinting -- To get a single PDF for shipping and return label select this
    option.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, shipmentNumber=None, ShipmentOrder=None, labelResponseType=None, groupProfileName=None, labelFormat=None, labelFormatRetoure=None, combinedPrinting=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        self.shipmentNumber = shipmentNumber
        self.validate_shipmentNumber(self.shipmentNumber)
        self.shipmentNumber_nsprefix_ = None
        self.ShipmentOrder = ShipmentOrder
        self.ShipmentOrder_nsprefix_ = None
        self.labelResponseType = labelResponseType
        self.validate_labelResponseTypeType11(self.labelResponseType)
        self.labelResponseType_nsprefix_ = None
        self.groupProfileName = groupProfileName
        self.validate_groupProfileNameType12(self.groupProfileName)
        self.groupProfileName_nsprefix_ = None
        self.labelFormat = labelFormat
        self.validate_labelFormatType13(self.labelFormat)
        self.labelFormat_nsprefix_ = None
        self.labelFormatRetoure = labelFormatRetoure
        self.validate_labelFormatRetoureType14(self.labelFormatRetoure)
        self.labelFormatRetoure_nsprefix_ = None
        self.combinedPrinting = combinedPrinting
        self.validate_combinedPrintingType15(self.combinedPrinting)
        self.combinedPrinting_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UpdateShipmentOrderRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UpdateShipmentOrderRequest.subclass:
            return UpdateShipmentOrderRequest.subclass(*args_, **kwargs_)
        else:
            return UpdateShipmentOrderRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_shipmentNumber(self):
        return self.shipmentNumber
    def set_shipmentNumber(self, shipmentNumber):
        self.shipmentNumber = shipmentNumber
    def get_ShipmentOrder(self):
        return self.ShipmentOrder
    def set_ShipmentOrder(self, ShipmentOrder):
        self.ShipmentOrder = ShipmentOrder
    def get_labelResponseType(self):
        return self.labelResponseType
    def set_labelResponseType(self, labelResponseType):
        self.labelResponseType = labelResponseType
    def get_groupProfileName(self):
        return self.groupProfileName
    def set_groupProfileName(self, groupProfileName):
        self.groupProfileName = groupProfileName
    def get_labelFormat(self):
        return self.labelFormat
    def set_labelFormat(self, labelFormat):
        self.labelFormat = labelFormat
    def get_labelFormatRetoure(self):
        return self.labelFormatRetoure
    def set_labelFormatRetoure(self, labelFormatRetoure):
        self.labelFormatRetoure = labelFormatRetoure
    def get_combinedPrinting(self):
        return self.combinedPrinting
    def set_combinedPrinting(self, combinedPrinting):
        self.combinedPrinting = combinedPrinting
    def validate_shipmentNumber(self, value):
        result = True
        # Validate type shipmentNumber, a restriction on xs:string.
        pass
        return result
    def validate_labelResponseTypeType11(self, value):
        result = True
        # Validate type labelResponseTypeType11, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            value = value
            enumerations = ['URL', 'B64', 'ZPL2']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on labelResponseTypeType11' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_groupProfileNameType12(self, value):
        result = True
        # Validate type groupProfileNameType12, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def validate_labelFormatType13(self, value):
        result = True
        # Validate type labelFormatType13, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def validate_labelFormatRetoureType14(self, value):
        result = True
        # Validate type labelFormatRetoureType14, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def validate_combinedPrintingType15(self, value):
        result = True
        # Validate type combinedPrintingType15, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def _hasContent(self):
        if (
            self.Version is not None or
            self.shipmentNumber is not None or
            self.ShipmentOrder is not None or
            self.labelResponseType is not None or
            self.groupProfileName is not None or
            self.labelFormat is not None or
            self.labelFormatRetoure is not None or
            self.combinedPrinting is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UpdateShipmentOrderRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UpdateShipmentOrderRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UpdateShipmentOrderRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UpdateShipmentOrderRequest')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UpdateShipmentOrderRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UpdateShipmentOrderRequest'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UpdateShipmentOrderRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.shipmentNumber is not None:
            namespaceprefix_ = self.shipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.shipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sshipmentNumber>%s</%sshipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.shipmentNumber), input_name='shipmentNumber')), namespaceprefix_ , eol_))
        if self.ShipmentOrder is not None:
            namespaceprefix_ = self.ShipmentOrder_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentOrder_nsprefix_) else ''
            self.ShipmentOrder.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentOrder', pretty_print=pretty_print)
        if self.labelResponseType is not None:
            namespaceprefix_ = self.labelResponseType_nsprefix_ + ':' if (UseCapturedNS_ and self.labelResponseType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slabelResponseType>%s</%slabelResponseType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.labelResponseType), input_name='labelResponseType')), namespaceprefix_ , eol_))
        if self.groupProfileName is not None:
            namespaceprefix_ = self.groupProfileName_nsprefix_ + ':' if (UseCapturedNS_ and self.groupProfileName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sgroupProfileName>%s</%sgroupProfileName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.groupProfileName), input_name='groupProfileName')), namespaceprefix_ , eol_))
        if self.labelFormat is not None:
            namespaceprefix_ = self.labelFormat_nsprefix_ + ':' if (UseCapturedNS_ and self.labelFormat_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slabelFormat>%s</%slabelFormat>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.labelFormat), input_name='labelFormat')), namespaceprefix_ , eol_))
        if self.labelFormatRetoure is not None:
            namespaceprefix_ = self.labelFormatRetoure_nsprefix_ + ':' if (UseCapturedNS_ and self.labelFormatRetoure_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slabelFormatRetoure>%s</%slabelFormatRetoure>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.labelFormatRetoure), input_name='labelFormatRetoure')), namespaceprefix_ , eol_))
        if self.combinedPrinting is not None:
            namespaceprefix_ = self.combinedPrinting_nsprefix_ + ':' if (UseCapturedNS_ and self.combinedPrinting_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scombinedPrinting>%s</%scombinedPrinting>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.combinedPrinting), input_name='combinedPrinting')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'shipmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'shipmentNumber')
            value_ = self.gds_validate_string(value_, node, 'shipmentNumber')
            self.shipmentNumber = value_
            self.shipmentNumber_nsprefix_ = child_.prefix
            # validate type shipmentNumber
            self.validate_shipmentNumber(self.shipmentNumber)
        elif nodeName_ == 'ShipmentOrder':
            obj_ = ShipmentOrderType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentOrder = obj_
            obj_.original_tagname_ = 'ShipmentOrder'
        elif nodeName_ == 'labelResponseType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'labelResponseType')
            value_ = self.gds_validate_string(value_, node, 'labelResponseType')
            self.labelResponseType = value_
            self.labelResponseType_nsprefix_ = child_.prefix
            # validate type labelResponseTypeType11
            self.validate_labelResponseTypeType11(self.labelResponseType)
        elif nodeName_ == 'groupProfileName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'groupProfileName')
            value_ = self.gds_validate_string(value_, node, 'groupProfileName')
            self.groupProfileName = value_
            self.groupProfileName_nsprefix_ = child_.prefix
            # validate type groupProfileNameType12
            self.validate_groupProfileNameType12(self.groupProfileName)
        elif nodeName_ == 'labelFormat':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'labelFormat')
            value_ = self.gds_validate_string(value_, node, 'labelFormat')
            self.labelFormat = value_
            self.labelFormat_nsprefix_ = child_.prefix
            # validate type labelFormatType13
            self.validate_labelFormatType13(self.labelFormat)
        elif nodeName_ == 'labelFormatRetoure':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'labelFormatRetoure')
            value_ = self.gds_validate_string(value_, node, 'labelFormatRetoure')
            self.labelFormatRetoure = value_
            self.labelFormatRetoure_nsprefix_ = child_.prefix
            # validate type labelFormatRetoureType14
            self.validate_labelFormatRetoureType14(self.labelFormatRetoure)
        elif nodeName_ == 'combinedPrinting':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'combinedPrinting')
            value_ = self.gds_validate_string(value_, node, 'combinedPrinting')
            self.combinedPrinting = value_
            self.combinedPrinting_nsprefix_ = child_.prefix
            # validate type combinedPrintingType15
            self.validate_combinedPrintingType15(self.combinedPrinting)
# end class UpdateShipmentOrderRequest


class UpdateShipmentOrderResponse(GeneratedsSuper):
    """UpdateShipmentOrderResponse -- The status of the operation and the shipment identifier (if available).
    Version -- The version of the webservice implementation.
    Status -- Success status after processing the overall request.
    shipmentNumber -- Can contain any DHL shipmentnumber. For successful and
    unsuccessful operations, the requested ShipmentNumber to be deleted is
    returned. This is no matter if the operation could be performed or not.
    returnShipmentNumber -- Can contain any DHL shipmentnumber. For successful and
    unsuccessful operations, the requested ShipmentNumber to be deleted is
    returned. This is no matter if the operation could be performed or not.
    LabelData -- The operation's success status for every single ShipmentOrder
    will be returned by one UpdateState element. It is identifiable via
    ShipmentNumber.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, Status=None, shipmentNumber=None, returnShipmentNumber=None, LabelData=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
        self.shipmentNumber = shipmentNumber
        self.validate_shipmentNumberType(self.shipmentNumber)
        self.shipmentNumber_nsprefix_ = None
        self.returnShipmentNumber = returnShipmentNumber
        self.validate_returnShipmentNumberType(self.returnShipmentNumber)
        self.returnShipmentNumber_nsprefix_ = None
        self.LabelData = LabelData
        self.LabelData_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, UpdateShipmentOrderResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UpdateShipmentOrderResponse.subclass:
            return UpdateShipmentOrderResponse.subclass(*args_, **kwargs_)
        else:
            return UpdateShipmentOrderResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def get_shipmentNumber(self):
        return self.shipmentNumber
    def set_shipmentNumber(self, shipmentNumber):
        self.shipmentNumber = shipmentNumber
    def get_returnShipmentNumber(self):
        return self.returnShipmentNumber
    def set_returnShipmentNumber(self, returnShipmentNumber):
        self.returnShipmentNumber = returnShipmentNumber
    def get_LabelData(self):
        return self.LabelData
    def set_LabelData(self, LabelData):
        self.LabelData = LabelData
    def validate_shipmentNumberType(self, value):
        result = True
        # Validate type shipmentNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 39:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on shipmentNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_returnShipmentNumberType(self, value):
        result = True
        # Validate type returnShipmentNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 39:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on returnShipmentNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.Version is not None or
            self.Status is not None or
            self.shipmentNumber is not None or
            self.returnShipmentNumber is not None or
            self.LabelData is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UpdateShipmentOrderResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UpdateShipmentOrderResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UpdateShipmentOrderResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UpdateShipmentOrderResponse')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='UpdateShipmentOrderResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UpdateShipmentOrderResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='UpdateShipmentOrderResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            self.Status.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Status', pretty_print=pretty_print)
        if self.shipmentNumber is not None:
            namespaceprefix_ = self.shipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.shipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sshipmentNumber>%s</%sshipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.shipmentNumber), input_name='shipmentNumber')), namespaceprefix_ , eol_))
        if self.returnShipmentNumber is not None:
            namespaceprefix_ = self.returnShipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.returnShipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sreturnShipmentNumber>%s</%sreturnShipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.returnShipmentNumber), input_name='returnShipmentNumber')), namespaceprefix_ , eol_))
        if self.LabelData is not None:
            namespaceprefix_ = self.LabelData_nsprefix_ + ':' if (UseCapturedNS_ and self.LabelData_nsprefix_) else ''
            self.LabelData.export(outfile, level, namespaceprefix_, namespacedef_='', name_='LabelData', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'Status':
            obj_ = Statusinformation.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Status = obj_
            obj_.original_tagname_ = 'Status'
        elif nodeName_ == 'shipmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'shipmentNumber')
            value_ = self.gds_validate_string(value_, node, 'shipmentNumber')
            self.shipmentNumber = value_
            self.shipmentNumber_nsprefix_ = child_.prefix
            # validate type shipmentNumberType
            self.validate_shipmentNumberType(self.shipmentNumber)
        elif nodeName_ == 'returnShipmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'returnShipmentNumber')
            value_ = self.gds_validate_string(value_, node, 'returnShipmentNumber')
            self.returnShipmentNumber = value_
            self.returnShipmentNumber_nsprefix_ = child_.prefix
            # validate type returnShipmentNumberType
            self.validate_returnShipmentNumberType(self.returnShipmentNumber)
        elif nodeName_ == 'LabelData':
            obj_ = LabelData.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LabelData = obj_
            obj_.original_tagname_ = 'LabelData'
# end class UpdateShipmentOrderResponse


class CreationState(GeneratedsSuper):
    """CreationState -- The operation's success status for every single ShipmentOrder will be
    returned by one CreationState element. It is identifiable via SequenceNumber.
    sequenceNumber -- Identifier for ShipmentOrder set by client application in
    CreateShipment request. The defined value is looped through and returned
    unchanged by the web service within the response of createShipment. The
    client can therefore assign the status information of the response to the
    correct ShipmentOrder of the request.
    shipmentNumber -- Can contain any DHL shipmentnumber. For successful and
    unsuccessful operations, the requested ShipmentNumber to be deleted is
    returned. This is no matter if the operation could be performed or not.
    returnShipmentNumber -- Can contain any DHL shipmentnumber. For successful and
    unsuccessful operations, the requested ShipmentNumber to be deleted is
    returned. This is no matter if the operation could be performed or not.
    LabelData -- For successful operations, a shipment number is created and
    returned. Depending on the invoked product.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, sequenceNumber=None, shipmentNumber=None, returnShipmentNumber=None, LabelData=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.sequenceNumber = sequenceNumber
        self.validate_SequenceNumber(self.sequenceNumber)
        self.sequenceNumber_nsprefix_ = None
        self.shipmentNumber = shipmentNumber
        self.validate_shipmentNumberType16(self.shipmentNumber)
        self.shipmentNumber_nsprefix_ = None
        self.returnShipmentNumber = returnShipmentNumber
        self.validate_returnShipmentNumberType17(self.returnShipmentNumber)
        self.returnShipmentNumber_nsprefix_ = None
        self.LabelData = LabelData
        self.LabelData_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CreationState)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CreationState.subclass:
            return CreationState.subclass(*args_, **kwargs_)
        else:
            return CreationState(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_sequenceNumber(self):
        return self.sequenceNumber
    def set_sequenceNumber(self, sequenceNumber):
        self.sequenceNumber = sequenceNumber
    def get_shipmentNumber(self):
        return self.shipmentNumber
    def set_shipmentNumber(self, shipmentNumber):
        self.shipmentNumber = shipmentNumber
    def get_returnShipmentNumber(self):
        return self.returnShipmentNumber
    def set_returnShipmentNumber(self, returnShipmentNumber):
        self.returnShipmentNumber = returnShipmentNumber
    def get_LabelData(self):
        return self.LabelData
    def set_LabelData(self, LabelData):
        self.LabelData = LabelData
    def validate_SequenceNumber(self, value):
        result = True
        # Validate type SequenceNumber, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on SequenceNumber' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_shipmentNumberType16(self, value):
        result = True
        # Validate type shipmentNumberType16, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 39:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on shipmentNumberType16' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_returnShipmentNumberType17(self, value):
        result = True
        # Validate type returnShipmentNumberType17, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 39:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on returnShipmentNumberType17' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.sequenceNumber is not None or
            self.shipmentNumber is not None or
            self.returnShipmentNumber is not None or
            self.LabelData is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CreationState', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CreationState')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CreationState':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CreationState')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CreationState', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CreationState'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CreationState', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.sequenceNumber is not None:
            namespaceprefix_ = self.sequenceNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.sequenceNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssequenceNumber>%s</%ssequenceNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.sequenceNumber), input_name='sequenceNumber')), namespaceprefix_ , eol_))
        if self.shipmentNumber is not None:
            namespaceprefix_ = self.shipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.shipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sshipmentNumber>%s</%sshipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.shipmentNumber), input_name='shipmentNumber')), namespaceprefix_ , eol_))
        if self.returnShipmentNumber is not None:
            namespaceprefix_ = self.returnShipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.returnShipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sreturnShipmentNumber>%s</%sreturnShipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.returnShipmentNumber), input_name='returnShipmentNumber')), namespaceprefix_ , eol_))
        if self.LabelData is not None:
            namespaceprefix_ = self.LabelData_nsprefix_ + ':' if (UseCapturedNS_ and self.LabelData_nsprefix_) else ''
            self.LabelData.export(outfile, level, namespaceprefix_, namespacedef_='', name_='LabelData', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'sequenceNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'sequenceNumber')
            value_ = self.gds_validate_string(value_, node, 'sequenceNumber')
            self.sequenceNumber = value_
            self.sequenceNumber_nsprefix_ = child_.prefix
            # validate type SequenceNumber
            self.validate_SequenceNumber(self.sequenceNumber)
        elif nodeName_ == 'shipmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'shipmentNumber')
            value_ = self.gds_validate_string(value_, node, 'shipmentNumber')
            self.shipmentNumber = value_
            self.shipmentNumber_nsprefix_ = child_.prefix
            # validate type shipmentNumberType16
            self.validate_shipmentNumberType16(self.shipmentNumber)
        elif nodeName_ == 'returnShipmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'returnShipmentNumber')
            value_ = self.gds_validate_string(value_, node, 'returnShipmentNumber')
            self.returnShipmentNumber = value_
            self.returnShipmentNumber_nsprefix_ = child_.prefix
            # validate type returnShipmentNumberType17
            self.validate_returnShipmentNumberType17(self.returnShipmentNumber)
        elif nodeName_ == 'LabelData':
            obj_ = LabelData.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.LabelData = obj_
            obj_.original_tagname_ = 'LabelData'
# end class CreationState


class ValidationState(GeneratedsSuper):
    """ValidationState -- The operation's success status for every single ShipmentOrder will be
    returned by one CreationState element. It is identifiable via SequenceNumber.
    sequenceNumber -- Identifier for ShipmentOrder set by client application in
    CreateShipment request. The defined value is looped through and returned
    unchanged by the web service within the response of createShipment. The
    client can therefore assign the status information of the response to the
    correct ShipmentOrder of the request.
    Status --  Success status of processing a particular shipment.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, sequenceNumber=None, Status=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.sequenceNumber = sequenceNumber
        self.validate_SequenceNumber(self.sequenceNumber)
        self.sequenceNumber_nsprefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ValidationState)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ValidationState.subclass:
            return ValidationState.subclass(*args_, **kwargs_)
        else:
            return ValidationState(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_sequenceNumber(self):
        return self.sequenceNumber
    def set_sequenceNumber(self, sequenceNumber):
        self.sequenceNumber = sequenceNumber
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def validate_SequenceNumber(self, value):
        result = True
        # Validate type SequenceNumber, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on SequenceNumber' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.sequenceNumber is not None or
            self.Status is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ValidationState', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ValidationState')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ValidationState':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ValidationState')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ValidationState', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ValidationState'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ValidationState', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.sequenceNumber is not None:
            namespaceprefix_ = self.sequenceNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.sequenceNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssequenceNumber>%s</%ssequenceNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.sequenceNumber), input_name='sequenceNumber')), namespaceprefix_ , eol_))
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            self.Status.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Status', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'sequenceNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'sequenceNumber')
            value_ = self.gds_validate_string(value_, node, 'sequenceNumber')
            self.sequenceNumber = value_
            self.sequenceNumber_nsprefix_ = child_.prefix
            # validate type SequenceNumber
            self.validate_SequenceNumber(self.sequenceNumber)
        elif nodeName_ == 'Status':
            obj_ = Statusinformation.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Status = obj_
            obj_.original_tagname_ = 'Status'
# end class ValidationState


class Statusinformation(GeneratedsSuper):
    """Statusinformation -- The status information used in different situations.
    statusCode -- Overall status of the entire request: A value of zero means, the
    request was processed without error. A value greater than zero indicates
    that an error occurred. The detailed mapping and explanation of returned
    status codes is contained in the list.
    statusText -- Explanation of the statuscode. Explains what types of errors
    occurred.
    statusMessage -- Detailed explanation of errors or warnings, p.e.
    “
    Invalid postal
    code
    ”
    . This element is kept for compatibility reasons only. Please use
    “
    statusType
    ”
    und
    “
    errorMassage
    ”
    with their subelements instead.
    errorMessage --  Explains details of the error and where it occurred
    statusType -- Explains if an error or warning occurred
    warningMessage --  Explains details of the error and where it occurred
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, statusCode=None, statusText=None, statusMessage=None, errorMessage=None, statusType=None, warningMessage=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.statusCode = statusCode
        self.statusCode_nsprefix_ = None
        self.statusText = statusText
        self.statusText_nsprefix_ = None
        if statusMessage is None:
            self.statusMessage = []
        else:
            self.statusMessage = statusMessage
        self.statusMessage_nsprefix_ = None
        if errorMessage is None:
            self.errorMessage = []
        else:
            self.errorMessage = errorMessage
        self.errorMessage_nsprefix_ = None
        self.statusType = statusType
        self.statusType_nsprefix_ = None
        if warningMessage is None:
            self.warningMessage = []
        else:
            self.warningMessage = warningMessage
        self.warningMessage_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Statusinformation)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Statusinformation.subclass:
            return Statusinformation.subclass(*args_, **kwargs_)
        else:
            return Statusinformation(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_statusCode(self):
        return self.statusCode
    def set_statusCode(self, statusCode):
        self.statusCode = statusCode
    def get_statusText(self):
        return self.statusText
    def set_statusText(self, statusText):
        self.statusText = statusText
    def get_statusMessage(self):
        return self.statusMessage
    def set_statusMessage(self, statusMessage):
        self.statusMessage = statusMessage
    def add_statusMessage(self, value):
        self.statusMessage.append(value)
    def insert_statusMessage_at(self, index, value):
        self.statusMessage.insert(index, value)
    def replace_statusMessage_at(self, index, value):
        self.statusMessage[index] = value
    def get_errorMessage(self):
        return self.errorMessage
    def set_errorMessage(self, errorMessage):
        self.errorMessage = errorMessage
    def add_errorMessage(self, value):
        self.errorMessage.append(value)
    def insert_errorMessage_at(self, index, value):
        self.errorMessage.insert(index, value)
    def replace_errorMessage_at(self, index, value):
        self.errorMessage[index] = value
    def get_statusType(self):
        return self.statusType
    def set_statusType(self, statusType):
        self.statusType = statusType
    def get_warningMessage(self):
        return self.warningMessage
    def set_warningMessage(self, warningMessage):
        self.warningMessage = warningMessage
    def add_warningMessage(self, value):
        self.warningMessage.append(value)
    def insert_warningMessage_at(self, index, value):
        self.warningMessage.insert(index, value)
    def replace_warningMessage_at(self, index, value):
        self.warningMessage[index] = value
    def _hasContent(self):
        if (
            self.statusCode is not None or
            self.statusText is not None or
            self.statusMessage or
            self.errorMessage or
            self.statusType is not None or
            self.warningMessage
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Statusinformation', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Statusinformation')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Statusinformation':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Statusinformation')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Statusinformation', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Statusinformation'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Statusinformation', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.statusCode is not None:
            namespaceprefix_ = self.statusCode_nsprefix_ + ':' if (UseCapturedNS_ and self.statusCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstatusCode>%s</%sstatusCode>%s' % (namespaceprefix_ , self.gds_format_integer(self.statusCode, input_name='statusCode'), namespaceprefix_ , eol_))
        if self.statusText is not None:
            namespaceprefix_ = self.statusText_nsprefix_ + ':' if (UseCapturedNS_ and self.statusText_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstatusText>%s</%sstatusText>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.statusText), input_name='statusText')), namespaceprefix_ , eol_))
        for statusMessage_ in self.statusMessage:
            namespaceprefix_ = self.statusMessage_nsprefix_ + ':' if (UseCapturedNS_ and self.statusMessage_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstatusMessage>%s</%sstatusMessage>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(statusMessage_), input_name='statusMessage')), namespaceprefix_ , eol_))
        for errorMessage_ in self.errorMessage:
            namespaceprefix_ = self.errorMessage_nsprefix_ + ':' if (UseCapturedNS_ and self.errorMessage_nsprefix_) else ''
            errorMessage_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='errorMessage', pretty_print=pretty_print)
        if self.statusType is not None:
            namespaceprefix_ = self.statusType_nsprefix_ + ':' if (UseCapturedNS_ and self.statusType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstatusType>%s</%sstatusType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.statusType), input_name='statusType')), namespaceprefix_ , eol_))
        for warningMessage_ in self.warningMessage:
            namespaceprefix_ = self.warningMessage_nsprefix_ + ':' if (UseCapturedNS_ and self.warningMessage_nsprefix_) else ''
            warningMessage_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='warningMessage', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'statusCode' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'statusCode')
            ival_ = self.gds_validate_integer(ival_, node, 'statusCode')
            self.statusCode = ival_
            self.statusCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'statusText':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'statusText')
            value_ = self.gds_validate_string(value_, node, 'statusText')
            self.statusText = value_
            self.statusText_nsprefix_ = child_.prefix
        elif nodeName_ == 'statusMessage':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'statusMessage')
            value_ = self.gds_validate_string(value_, node, 'statusMessage')
            self.statusMessage.append(value_)
            self.statusMessage_nsprefix_ = child_.prefix
        elif nodeName_ == 'errorMessage':
            obj_ = StatusElement.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.errorMessage.append(obj_)
            obj_.original_tagname_ = 'errorMessage'
        elif nodeName_ == 'statusType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'statusType')
            value_ = self.gds_validate_string(value_, node, 'statusType')
            self.statusType = value_
            self.statusType_nsprefix_ = child_.prefix
        elif nodeName_ == 'warningMessage':
            obj_ = StatusElement.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.warningMessage.append(obj_)
            obj_.original_tagname_ = 'warningMessage'
# end class Statusinformation


class StatusElement(GeneratedsSuper):
    """statusElement -- Explanation of the statusElement and potential errors.
    statusMessage -- Explanation of the statusMessage and potential errors.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, statusElement=None, statusMessage=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.statusElement = statusElement
        self.statusElement_nsprefix_ = None
        self.statusMessage = statusMessage
        self.statusMessage_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, StatusElement)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if StatusElement.subclass:
            return StatusElement.subclass(*args_, **kwargs_)
        else:
            return StatusElement(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_statusElement(self):
        return self.statusElement
    def set_statusElement(self, statusElement):
        self.statusElement = statusElement
    def get_statusMessage(self):
        return self.statusMessage
    def set_statusMessage(self, statusMessage):
        self.statusMessage = statusMessage
    def _hasContent(self):
        if (
            self.statusElement is not None or
            self.statusMessage is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='StatusElement', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('StatusElement')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'StatusElement':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='StatusElement')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='StatusElement', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='StatusElement'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='StatusElement', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.statusElement is not None:
            namespaceprefix_ = self.statusElement_nsprefix_ + ':' if (UseCapturedNS_ and self.statusElement_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstatusElement>%s</%sstatusElement>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.statusElement), input_name='statusElement')), namespaceprefix_ , eol_))
        if self.statusMessage is not None:
            namespaceprefix_ = self.statusMessage_nsprefix_ + ':' if (UseCapturedNS_ and self.statusMessage_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sstatusMessage>%s</%sstatusMessage>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.statusMessage), input_name='statusMessage')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'statusElement':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'statusElement')
            value_ = self.gds_validate_string(value_, node, 'statusElement')
            self.statusElement = value_
            self.statusElement_nsprefix_ = child_.prefix
        elif nodeName_ == 'statusMessage':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'statusMessage')
            value_ = self.gds_validate_string(value_, node, 'statusMessage')
            self.statusMessage = value_
            self.statusMessage_nsprefix_ = child_.prefix
# end class StatusElement


class PieceInformation(GeneratedsSuper):
    """PieceInformation -- Information about each piece (e.g. the generated licence plate). For
    every piece, a PieceInformation container holds the license plate number.
    PieceNumber -- For every piece a piece number is created that is of one of the
    following types (mostly licensePlate).
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PieceNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PieceNumber = PieceNumber
        self.PieceNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PieceInformation)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PieceInformation.subclass:
            return PieceInformation.subclass(*args_, **kwargs_)
        else:
            return PieceInformation(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PieceNumber(self):
        return self.PieceNumber
    def set_PieceNumber(self, PieceNumber):
        self.PieceNumber = PieceNumber
    def _hasContent(self):
        if (
            self.PieceNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PieceInformation', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PieceInformation')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PieceInformation':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PieceInformation')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PieceInformation', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PieceInformation'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PieceInformation', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PieceNumber is not None:
            namespaceprefix_ = self.PieceNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.PieceNumber_nsprefix_) else ''
            self.PieceNumber.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PieceNumber', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'PieceNumber':
            obj_ = ShipmentNumberType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PieceNumber = obj_
            obj_.original_tagname_ = 'PieceNumber'
# end class PieceInformation


class ShipmentOrderType(GeneratedsSuper):
    """ShipmentOrderType -- Data for the creation of a shipment.
    sequenceNumber -- Free field to to tag multiple shipment orders individually by
    client. Essential for later mapping of response data returned by webservice
    upon createShipment operation. Allows client to assign the shipment
    information of the response to the correct shipment order of the request.
    Shipment -- Is the core element of a ShipmentOrder. It contains all relevant
    information of the shipment.
    PrintOnlyIfCodeable -- If set to true (=1), the label will be only be printable, if the
    receiver address is valid.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, sequenceNumber=None, Shipment=None, PrintOnlyIfCodeable=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.sequenceNumber = sequenceNumber
        self.validate_SequenceNumber(self.sequenceNumber)
        self.sequenceNumber_nsprefix_ = None
        self.Shipment = Shipment
        self.Shipment_nsprefix_ = None
        self.PrintOnlyIfCodeable = PrintOnlyIfCodeable
        self.PrintOnlyIfCodeable_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentOrderType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentOrderType.subclass:
            return ShipmentOrderType.subclass(*args_, **kwargs_)
        else:
            return ShipmentOrderType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_sequenceNumber(self):
        return self.sequenceNumber
    def set_sequenceNumber(self, sequenceNumber):
        self.sequenceNumber = sequenceNumber
    def get_Shipment(self):
        return self.Shipment
    def set_Shipment(self, Shipment):
        self.Shipment = Shipment
    def get_PrintOnlyIfCodeable(self):
        return self.PrintOnlyIfCodeable
    def set_PrintOnlyIfCodeable(self, PrintOnlyIfCodeable):
        self.PrintOnlyIfCodeable = PrintOnlyIfCodeable
    def validate_SequenceNumber(self, value):
        result = True
        # Validate type SequenceNumber, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on SequenceNumber' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.sequenceNumber is not None or
            self.Shipment is not None or
            self.PrintOnlyIfCodeable is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentOrderType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentOrderType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentOrderType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentOrderType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentOrderType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentOrderType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentOrderType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.sequenceNumber is not None:
            namespaceprefix_ = self.sequenceNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.sequenceNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssequenceNumber>%s</%ssequenceNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.sequenceNumber), input_name='sequenceNumber')), namespaceprefix_ , eol_))
        if self.Shipment is not None:
            namespaceprefix_ = self.Shipment_nsprefix_ + ':' if (UseCapturedNS_ and self.Shipment_nsprefix_) else ''
            self.Shipment.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Shipment', pretty_print=pretty_print)
        if self.PrintOnlyIfCodeable is not None:
            namespaceprefix_ = self.PrintOnlyIfCodeable_nsprefix_ + ':' if (UseCapturedNS_ and self.PrintOnlyIfCodeable_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPrintOnlyIfCodeable>%s</%sPrintOnlyIfCodeable>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PrintOnlyIfCodeable), input_name='PrintOnlyIfCodeable')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'sequenceNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'sequenceNumber')
            value_ = self.gds_validate_string(value_, node, 'sequenceNumber')
            self.sequenceNumber = value_
            self.sequenceNumber_nsprefix_ = child_.prefix
            # validate type SequenceNumber
            self.validate_SequenceNumber(self.sequenceNumber)
        elif nodeName_ == 'Shipment':
            obj_ = ShipmentType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Shipment = obj_
            obj_.original_tagname_ = 'Shipment'
        elif nodeName_ == 'PrintOnlyIfCodeable':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PrintOnlyIfCodeable')
            value_ = self.gds_validate_string(value_, node, 'PrintOnlyIfCodeable')
            self.PrintOnlyIfCodeable = value_
            self.PrintOnlyIfCodeable_nsprefix_ = child_.prefix
# end class ShipmentOrderType


class ValidateShipmentOrderType(GeneratedsSuper):
    """ValidateShipmentOrderType -- Data for the creation of a shipment.
    sequenceNumber -- Free field to to tag multiple shipment orders individually by
    client. Essential for later mapping of response data returned by webservice
    upon createShipment operation. Allows client to assign the shipment
    information of the response to the correct shipment order of the request.
    Shipment -- Is the core element of a ShipmentOrder. It contains all relevant
    information of the shipment.
    PrintOnlyIfCodeable -- If set to true (=1), the label will be only be printable, if the
    receiver address is valid.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, sequenceNumber=None, Shipment=None, PrintOnlyIfCodeable=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.sequenceNumber = sequenceNumber
        self.validate_SequenceNumber(self.sequenceNumber)
        self.sequenceNumber_nsprefix_ = None
        self.Shipment = Shipment
        self.Shipment_nsprefix_ = None
        self.PrintOnlyIfCodeable = PrintOnlyIfCodeable
        self.PrintOnlyIfCodeable_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ValidateShipmentOrderType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ValidateShipmentOrderType.subclass:
            return ValidateShipmentOrderType.subclass(*args_, **kwargs_)
        else:
            return ValidateShipmentOrderType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_sequenceNumber(self):
        return self.sequenceNumber
    def set_sequenceNumber(self, sequenceNumber):
        self.sequenceNumber = sequenceNumber
    def get_Shipment(self):
        return self.Shipment
    def set_Shipment(self, Shipment):
        self.Shipment = Shipment
    def get_PrintOnlyIfCodeable(self):
        return self.PrintOnlyIfCodeable
    def set_PrintOnlyIfCodeable(self, PrintOnlyIfCodeable):
        self.PrintOnlyIfCodeable = PrintOnlyIfCodeable
    def validate_SequenceNumber(self, value):
        result = True
        # Validate type SequenceNumber, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on SequenceNumber' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.sequenceNumber is not None or
            self.Shipment is not None or
            self.PrintOnlyIfCodeable is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ValidateShipmentOrderType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ValidateShipmentOrderType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ValidateShipmentOrderType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ValidateShipmentOrderType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ValidateShipmentOrderType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ValidateShipmentOrderType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ValidateShipmentOrderType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.sequenceNumber is not None:
            namespaceprefix_ = self.sequenceNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.sequenceNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssequenceNumber>%s</%ssequenceNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.sequenceNumber), input_name='sequenceNumber')), namespaceprefix_ , eol_))
        if self.Shipment is not None:
            namespaceprefix_ = self.Shipment_nsprefix_ + ':' if (UseCapturedNS_ and self.Shipment_nsprefix_) else ''
            self.Shipment.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Shipment', pretty_print=pretty_print)
        if self.PrintOnlyIfCodeable is not None:
            namespaceprefix_ = self.PrintOnlyIfCodeable_nsprefix_ + ':' if (UseCapturedNS_ and self.PrintOnlyIfCodeable_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPrintOnlyIfCodeable>%s</%sPrintOnlyIfCodeable>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PrintOnlyIfCodeable), input_name='PrintOnlyIfCodeable')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'sequenceNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'sequenceNumber')
            value_ = self.gds_validate_string(value_, node, 'sequenceNumber')
            self.sequenceNumber = value_
            self.sequenceNumber_nsprefix_ = child_.prefix
            # validate type SequenceNumber
            self.validate_SequenceNumber(self.sequenceNumber)
        elif nodeName_ == 'Shipment':
            obj_ = ShipmentType18.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Shipment = obj_
            obj_.original_tagname_ = 'Shipment'
        elif nodeName_ == 'PrintOnlyIfCodeable':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PrintOnlyIfCodeable')
            value_ = self.gds_validate_string(value_, node, 'PrintOnlyIfCodeable')
            self.PrintOnlyIfCodeable = value_
            self.PrintOnlyIfCodeable_nsprefix_ = child_.prefix
# end class ValidateShipmentOrderType


class ShipperTypeType(GeneratedsSuper):
    """ShipperTypeType -- The data of the shipper or return receiver.
    Name -- Name of the Return Receiver
    Address -- Contains address data.
    Communication -- Information about communication.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Name=None, Address=None, Communication=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Name = Name
        self.Name_nsprefix_ = None
        self.Address = Address
        self.Address_nsprefix_ = None
        self.Communication = Communication
        self.Communication_nsprefix_ = None
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipperTypeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipperTypeType.subclass:
            return ShipperTypeType.subclass(*args_, **kwargs_)
        else:
            return ShipperTypeType(*args_, **kwargs_)
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
    def get_Communication(self):
        return self.Communication
    def set_Communication(self, Communication):
        self.Communication = Communication
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def _hasContent(self):
        if (
            self.Name is not None or
            self.Address is not None or
            self.Communication is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipperTypeType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipperTypeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipperTypeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipperTypeType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipperTypeType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipperTypeType'):
        if self.extensiontype_ is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self.extensiontype_:
                imported_ns_type_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.extensiontype_, '')
                outfile.write(' xsi:type="%s%s"' % (imported_ns_type_prefix_, self.extensiontype_))
            else:
                outfile.write(' xsi:type="%s"' % self.extensiontype_)
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipperTypeType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Name is not None:
            namespaceprefix_ = self.Name_nsprefix_ + ':' if (UseCapturedNS_ and self.Name_nsprefix_) else ''
            self.Name.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Name', pretty_print=pretty_print)
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.Communication is not None:
            namespaceprefix_ = self.Communication_nsprefix_ + ':' if (UseCapturedNS_ and self.Communication_nsprefix_) else ''
            self.Communication.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Communication', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'Name':
            obj_ = NameType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Name = obj_
            obj_.original_tagname_ = 'Name'
        elif nodeName_ == 'Address':
            obj_ = NativeAddressTypeNew.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'Communication':
            obj_ = CommunicationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Communication = obj_
            obj_.original_tagname_ = 'Communication'
# end class ShipperTypeType


class ShipperType(ShipperTypeType):
    """ShipperType -- The data of the shipper of a shipment.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = ShipperTypeType
    def __init__(self, Name=None, Address=None, Communication=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("ShipperType"), self).__init__(Name, Address, Communication,  **kwargs_)
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipperType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipperType.subclass:
            return ShipperType.subclass(*args_, **kwargs_)
        else:
            return ShipperType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def _hasContent(self):
        if (
            super(ShipperType, self)._hasContent()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipperType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipperType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipperType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipperType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipperType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipperType'):
        super(ShipperType, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipperType')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipperType', fromsubclass_=False, pretty_print=True):
        super(ShipperType, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        super(ShipperType, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        super(ShipperType, self)._buildChildren(child_, node, nodeName_, True)
        pass
# end class ShipperType


class ReceiverTypeType(GeneratedsSuper):
    """ReceiverTypeType -- The receiver data.
    Address -- The address data of the receiver.
    Packstation -- The address of the receiver is a german Packstation.
    Postfiliale -- The address of the receiver is a german Postfiliale.
    Communication -- Information about communication.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, name1=None, Address=None, Packstation=None, Postfiliale=None, Communication=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name1 = name1
        self.validate_name1(self.name1)
        self.name1_nsprefix_ = None
        self.Address = Address
        self.Address_nsprefix_ = None
        self.Packstation = Packstation
        self.Packstation_nsprefix_ = None
        self.Postfiliale = Postfiliale
        self.Postfiliale_nsprefix_ = None
        self.Communication = Communication
        self.Communication_nsprefix_ = None
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ReceiverTypeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ReceiverTypeType.subclass:
            return ReceiverTypeType.subclass(*args_, **kwargs_)
        else:
            return ReceiverTypeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_name1(self):
        return self.name1
    def set_name1(self, name1):
        self.name1 = name1
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_Packstation(self):
        return self.Packstation
    def set_Packstation(self, Packstation):
        self.Packstation = Packstation
    def get_Postfiliale(self):
        return self.Postfiliale
    def set_Postfiliale(self, Postfiliale):
        self.Postfiliale = Postfiliale
    def get_Communication(self):
        return self.Communication
    def set_Communication(self, Communication):
        self.Communication = Communication
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def validate_name1(self, value):
        result = True
        # Validate type name1, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.name1 is not None or
            self.Address is not None or
            self.Packstation is not None or
            self.Postfiliale is not None or
            self.Communication is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReceiverTypeType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ReceiverTypeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ReceiverTypeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ReceiverTypeType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ReceiverTypeType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ReceiverTypeType'):
        if self.extensiontype_ is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self.extensiontype_:
                imported_ns_type_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.extensiontype_, '')
                outfile.write(' xsi:type="%s%s"' % (imported_ns_type_prefix_, self.extensiontype_))
            else:
                outfile.write(' xsi:type="%s"' % self.extensiontype_)
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReceiverTypeType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.name1 is not None:
            namespaceprefix_ = self.name1_nsprefix_ + ':' if (UseCapturedNS_ and self.name1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sname1>%s</%sname1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.name1), input_name='name1')), namespaceprefix_ , eol_))
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.Packstation is not None:
            namespaceprefix_ = self.Packstation_nsprefix_ + ':' if (UseCapturedNS_ and self.Packstation_nsprefix_) else ''
            self.Packstation.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Packstation', pretty_print=pretty_print)
        if self.Postfiliale is not None:
            namespaceprefix_ = self.Postfiliale_nsprefix_ + ':' if (UseCapturedNS_ and self.Postfiliale_nsprefix_) else ''
            self.Postfiliale.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Postfiliale', pretty_print=pretty_print)
        if self.Communication is not None:
            namespaceprefix_ = self.Communication_nsprefix_ + ':' if (UseCapturedNS_ and self.Communication_nsprefix_) else ''
            self.Communication.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Communication', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'name1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'name1')
            value_ = self.gds_validate_string(value_, node, 'name1')
            self.name1 = value_
            self.name1_nsprefix_ = child_.prefix
            # validate type name1
            self.validate_name1(self.name1)
        elif nodeName_ == 'Address':
            obj_ = ReceiverNativeAddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'Packstation':
            obj_ = PackStationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Packstation = obj_
            obj_.original_tagname_ = 'Packstation'
        elif nodeName_ == 'Postfiliale':
            obj_ = PostfilialeTypeNoCountry.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Postfiliale = obj_
            obj_.original_tagname_ = 'Postfiliale'
        elif nodeName_ == 'Communication':
            obj_ = CommunicationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Communication = obj_
            obj_.original_tagname_ = 'Communication'
# end class ReceiverTypeType


class ReceiverType(ReceiverTypeType):
    """ReceiverType -- The receiver data of a shipment.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = ReceiverTypeType
    def __init__(self, name1=None, Address=None, Packstation=None, Postfiliale=None, Communication=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("ReceiverType"), self).__init__(name1, Address, Packstation, Postfiliale, Communication,  **kwargs_)
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ReceiverType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ReceiverType.subclass:
            return ReceiverType.subclass(*args_, **kwargs_)
        else:
            return ReceiverType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def _hasContent(self):
        if (
            super(ReceiverType, self)._hasContent()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReceiverType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ReceiverType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ReceiverType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ReceiverType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ReceiverType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ReceiverType'):
        super(ReceiverType, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ReceiverType')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReceiverType', fromsubclass_=False, pretty_print=True):
        super(ReceiverType, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        super(ReceiverType, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        super(ReceiverType, self)._buildChildren(child_, node, nodeName_, True)
        pass
# end class ReceiverType


class Ident(GeneratedsSuper):
    """Ident -- Identity data (used for ident services).
    FirstName -- First name of the person to be verified. Field length must be
    less than or equal to 30.
    LastName -- Last name of the person to be verified. Field length must be less
    than or equal to 30.
    Street -- Name of the street of registered address. Field length must be
    less than or equal to 30.
    HouseNumber -- House number of registered address. Field length must be less
    than or equal to 10.
    Postcode -- Postcode of registered address. Field length must be less than or
    equal to 15.
    City -- City of registered address. Field length must be less than or
    equal to 30.
    DateOfBirth -- Person's date of birth. Format must be yyyy-mm-dd.
    Nationality -- Person's nationality. Field length must be less than or equal to
    30.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, FirstName=None, LastName=None, Street=None, HouseNumber=None, Postcode=None, City=None, DateOfBirth=None, Nationality=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.FirstName = FirstName
        self.FirstName_nsprefix_ = None
        self.LastName = LastName
        self.LastName_nsprefix_ = None
        self.Street = Street
        self.Street_nsprefix_ = None
        self.HouseNumber = HouseNumber
        self.HouseNumber_nsprefix_ = None
        self.Postcode = Postcode
        self.Postcode_nsprefix_ = None
        self.City = City
        self.City_nsprefix_ = None
        self.DateOfBirth = DateOfBirth
        self.DateOfBirth_nsprefix_ = None
        self.Nationality = Nationality
        self.Nationality_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, Ident)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if Ident.subclass:
            return Ident.subclass(*args_, **kwargs_)
        else:
            return Ident(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_FirstName(self):
        return self.FirstName
    def set_FirstName(self, FirstName):
        self.FirstName = FirstName
    def get_LastName(self):
        return self.LastName
    def set_LastName(self, LastName):
        self.LastName = LastName
    def get_Street(self):
        return self.Street
    def set_Street(self, Street):
        self.Street = Street
    def get_HouseNumber(self):
        return self.HouseNumber
    def set_HouseNumber(self, HouseNumber):
        self.HouseNumber = HouseNumber
    def get_Postcode(self):
        return self.Postcode
    def set_Postcode(self, Postcode):
        self.Postcode = Postcode
    def get_City(self):
        return self.City
    def set_City(self, City):
        self.City = City
    def get_DateOfBirth(self):
        return self.DateOfBirth
    def set_DateOfBirth(self, DateOfBirth):
        self.DateOfBirth = DateOfBirth
    def get_Nationality(self):
        return self.Nationality
    def set_Nationality(self, Nationality):
        self.Nationality = Nationality
    def _hasContent(self):
        if (
            self.FirstName is not None or
            self.LastName is not None or
            self.Street is not None or
            self.HouseNumber is not None or
            self.Postcode is not None or
            self.City is not None or
            self.DateOfBirth is not None or
            self.Nationality is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Ident', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('Ident')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'Ident':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='Ident')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='Ident', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='Ident'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='Ident', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.FirstName is not None:
            namespaceprefix_ = self.FirstName_nsprefix_ + ':' if (UseCapturedNS_ and self.FirstName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFirstName>%s</%sFirstName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FirstName), input_name='FirstName')), namespaceprefix_ , eol_))
        if self.LastName is not None:
            namespaceprefix_ = self.LastName_nsprefix_ + ':' if (UseCapturedNS_ and self.LastName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLastName>%s</%sLastName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LastName), input_name='LastName')), namespaceprefix_ , eol_))
        if self.Street is not None:
            namespaceprefix_ = self.Street_nsprefix_ + ':' if (UseCapturedNS_ and self.Street_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStreet>%s</%sStreet>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Street), input_name='Street')), namespaceprefix_ , eol_))
        if self.HouseNumber is not None:
            namespaceprefix_ = self.HouseNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.HouseNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sHouseNumber>%s</%sHouseNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.HouseNumber), input_name='HouseNumber')), namespaceprefix_ , eol_))
        if self.Postcode is not None:
            namespaceprefix_ = self.Postcode_nsprefix_ + ':' if (UseCapturedNS_ and self.Postcode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPostcode>%s</%sPostcode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Postcode), input_name='Postcode')), namespaceprefix_ , eol_))
        if self.City is not None:
            namespaceprefix_ = self.City_nsprefix_ + ':' if (UseCapturedNS_ and self.City_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCity>%s</%sCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.City), input_name='City')), namespaceprefix_ , eol_))
        if self.DateOfBirth is not None:
            namespaceprefix_ = self.DateOfBirth_nsprefix_ + ':' if (UseCapturedNS_ and self.DateOfBirth_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDateOfBirth>%s</%sDateOfBirth>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DateOfBirth), input_name='DateOfBirth')), namespaceprefix_ , eol_))
        if self.Nationality is not None:
            namespaceprefix_ = self.Nationality_nsprefix_ + ':' if (UseCapturedNS_ and self.Nationality_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNationality>%s</%sNationality>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Nationality), input_name='Nationality')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'FirstName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FirstName')
            value_ = self.gds_validate_string(value_, node, 'FirstName')
            self.FirstName = value_
            self.FirstName_nsprefix_ = child_.prefix
        elif nodeName_ == 'LastName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LastName')
            value_ = self.gds_validate_string(value_, node, 'LastName')
            self.LastName = value_
            self.LastName_nsprefix_ = child_.prefix
        elif nodeName_ == 'Street':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Street')
            value_ = self.gds_validate_string(value_, node, 'Street')
            self.Street = value_
            self.Street_nsprefix_ = child_.prefix
        elif nodeName_ == 'HouseNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'HouseNumber')
            value_ = self.gds_validate_string(value_, node, 'HouseNumber')
            self.HouseNumber = value_
            self.HouseNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'Postcode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Postcode')
            value_ = self.gds_validate_string(value_, node, 'Postcode')
            self.Postcode = value_
            self.Postcode_nsprefix_ = child_.prefix
        elif nodeName_ == 'City':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'City')
            value_ = self.gds_validate_string(value_, node, 'City')
            self.City = value_
            self.City_nsprefix_ = child_.prefix
        elif nodeName_ == 'DateOfBirth':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DateOfBirth')
            value_ = self.gds_validate_string(value_, node, 'DateOfBirth')
            self.DateOfBirth = value_
            self.DateOfBirth_nsprefix_ = child_.prefix
        elif nodeName_ == 'Nationality':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Nationality')
            value_ = self.gds_validate_string(value_, node, 'Nationality')
            self.Nationality = value_
            self.Nationality_nsprefix_ = child_.prefix
# end class Ident


class ShipmentDetailsType(GeneratedsSuper):
    """ShipmentDetailsType -- Details of a shipment.
    product --  Determines the DHL Paket product to be ordered. V01PAK: DHL
    PAKET; V53WPAK: DHL PAKET International; V54EPAK: DHL Europaket; V62WP:
    Warenpost; V66WPI: Warenpost International
    customerReference -- A reference number that the client can assign for better
    association purposes. Appears on shipment label. To use the reference number
    for tracking purposes, it should be at least 8 characters long and unique
    shipmentDate -- Date of shipment should be close to current date and must not be
    in the past. Iso format required: yyyy-mm-dd.
    costCentre -- Name of a cost center. Appears on shipment label.
    returnShipmentReference -- A reference number that the client can assign for better
    association purposes. Appears on return shipment label. To use the reference
    number for tracking purposes, it should be at least 8 characters long and
    unique.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, product=None, accountNumber=None, customerReference=None, shipmentDate=None, costCentre=None, returnShipmentAccountNumber=None, returnShipmentReference=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.product = product
        self.product_nsprefix_ = None
        self.accountNumber = accountNumber
        self.validate_accountNumber(self.accountNumber)
        self.accountNumber_nsprefix_ = None
        self.customerReference = customerReference
        self.validate_customerReferenceType(self.customerReference)
        self.customerReference_nsprefix_ = None
        self.shipmentDate = shipmentDate
        self.validate_shipmentDateType(self.shipmentDate)
        self.shipmentDate_nsprefix_ = None
        self.costCentre = costCentre
        self.validate_costCentreType(self.costCentre)
        self.costCentre_nsprefix_ = None
        self.returnShipmentAccountNumber = returnShipmentAccountNumber
        self.validate_returnShipmentAccountNumberType(self.returnShipmentAccountNumber)
        self.returnShipmentAccountNumber_nsprefix_ = None
        self.returnShipmentReference = returnShipmentReference
        self.validate_returnShipmentReferenceType(self.returnShipmentReference)
        self.returnShipmentReference_nsprefix_ = None
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentDetailsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentDetailsType.subclass:
            return ShipmentDetailsType.subclass(*args_, **kwargs_)
        else:
            return ShipmentDetailsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_product(self):
        return self.product
    def set_product(self, product):
        self.product = product
    def get_accountNumber(self):
        return self.accountNumber
    def set_accountNumber(self, accountNumber):
        self.accountNumber = accountNumber
    def get_customerReference(self):
        return self.customerReference
    def set_customerReference(self, customerReference):
        self.customerReference = customerReference
    def get_shipmentDate(self):
        return self.shipmentDate
    def set_shipmentDate(self, shipmentDate):
        self.shipmentDate = shipmentDate
    def get_costCentre(self):
        return self.costCentre
    def set_costCentre(self, costCentre):
        self.costCentre = costCentre
    def get_returnShipmentAccountNumber(self):
        return self.returnShipmentAccountNumber
    def set_returnShipmentAccountNumber(self, returnShipmentAccountNumber):
        self.returnShipmentAccountNumber = returnShipmentAccountNumber
    def get_returnShipmentReference(self):
        return self.returnShipmentReference
    def set_returnShipmentReference(self, returnShipmentReference):
        self.returnShipmentReference = returnShipmentReference
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def validate_accountNumber(self, value):
        result = True
        # Validate type accountNumber, a restriction on xs:string.
        pass
        return result
    def validate_customerReferenceType(self, value):
        result = True
        # Validate type customerReferenceType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on customerReferenceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_shipmentDateType(self, value):
        result = True
        # Validate type shipmentDateType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on shipmentDateType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on shipmentDateType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_costCentreType(self, value):
        result = True
        # Validate type costCentreType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on costCentreType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_returnShipmentAccountNumberType(self, value):
        result = True
        # Validate type returnShipmentAccountNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 14:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on returnShipmentAccountNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 14:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on returnShipmentAccountNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_returnShipmentReferenceType(self, value):
        result = True
        # Validate type returnShipmentReferenceType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on returnShipmentReferenceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.product is not None or
            self.accountNumber is not None or
            self.customerReference is not None or
            self.shipmentDate is not None or
            self.costCentre is not None or
            self.returnShipmentAccountNumber is not None or
            self.returnShipmentReference is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentDetailsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentDetailsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentDetailsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentDetailsType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentDetailsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentDetailsType'):
        if self.extensiontype_ is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self.extensiontype_:
                imported_ns_type_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.extensiontype_, '')
                outfile.write(' xsi:type="%s%s"' % (imported_ns_type_prefix_, self.extensiontype_))
            else:
                outfile.write(' xsi:type="%s"' % self.extensiontype_)
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentDetailsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.product is not None:
            namespaceprefix_ = self.product_nsprefix_ + ':' if (UseCapturedNS_ and self.product_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sproduct>%s</%sproduct>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.product), input_name='product')), namespaceprefix_ , eol_))
        if self.accountNumber is not None:
            namespaceprefix_ = self.accountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.accountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saccountNumber>%s</%saccountNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.accountNumber), input_name='accountNumber')), namespaceprefix_ , eol_))
        if self.customerReference is not None:
            namespaceprefix_ = self.customerReference_nsprefix_ + ':' if (UseCapturedNS_ and self.customerReference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scustomerReference>%s</%scustomerReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.customerReference), input_name='customerReference')), namespaceprefix_ , eol_))
        if self.shipmentDate is not None:
            namespaceprefix_ = self.shipmentDate_nsprefix_ + ':' if (UseCapturedNS_ and self.shipmentDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sshipmentDate>%s</%sshipmentDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.shipmentDate), input_name='shipmentDate')), namespaceprefix_ , eol_))
        if self.costCentre is not None:
            namespaceprefix_ = self.costCentre_nsprefix_ + ':' if (UseCapturedNS_ and self.costCentre_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scostCentre>%s</%scostCentre>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.costCentre), input_name='costCentre')), namespaceprefix_ , eol_))
        if self.returnShipmentAccountNumber is not None:
            namespaceprefix_ = self.returnShipmentAccountNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.returnShipmentAccountNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sreturnShipmentAccountNumber>%s</%sreturnShipmentAccountNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.returnShipmentAccountNumber), input_name='returnShipmentAccountNumber')), namespaceprefix_ , eol_))
        if self.returnShipmentReference is not None:
            namespaceprefix_ = self.returnShipmentReference_nsprefix_ + ':' if (UseCapturedNS_ and self.returnShipmentReference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sreturnShipmentReference>%s</%sreturnShipmentReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.returnShipmentReference), input_name='returnShipmentReference')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        elif nodeName_ == 'accountNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'accountNumber')
            value_ = self.gds_validate_string(value_, node, 'accountNumber')
            self.accountNumber = value_
            self.accountNumber_nsprefix_ = child_.prefix
            # validate type accountNumber
            self.validate_accountNumber(self.accountNumber)
        elif nodeName_ == 'customerReference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'customerReference')
            value_ = self.gds_validate_string(value_, node, 'customerReference')
            self.customerReference = value_
            self.customerReference_nsprefix_ = child_.prefix
            # validate type customerReferenceType
            self.validate_customerReferenceType(self.customerReference)
        elif nodeName_ == 'shipmentDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'shipmentDate')
            value_ = self.gds_validate_string(value_, node, 'shipmentDate')
            self.shipmentDate = value_
            self.shipmentDate_nsprefix_ = child_.prefix
            # validate type shipmentDateType
            self.validate_shipmentDateType(self.shipmentDate)
        elif nodeName_ == 'costCentre':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'costCentre')
            value_ = self.gds_validate_string(value_, node, 'costCentre')
            self.costCentre = value_
            self.costCentre_nsprefix_ = child_.prefix
            # validate type costCentreType
            self.validate_costCentreType(self.costCentre)
        elif nodeName_ == 'returnShipmentAccountNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'returnShipmentAccountNumber')
            value_ = self.gds_validate_string(value_, node, 'returnShipmentAccountNumber')
            self.returnShipmentAccountNumber = value_
            self.returnShipmentAccountNumber_nsprefix_ = child_.prefix
            # validate type returnShipmentAccountNumberType
            self.validate_returnShipmentAccountNumberType(self.returnShipmentAccountNumber)
        elif nodeName_ == 'returnShipmentReference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'returnShipmentReference')
            value_ = self.gds_validate_string(value_, node, 'returnShipmentReference')
            self.returnShipmentReference = value_
            self.returnShipmentReference_nsprefix_ = child_.prefix
            # validate type returnShipmentReferenceType
            self.validate_returnShipmentReferenceType(self.returnShipmentReference)
# end class ShipmentDetailsType


class ShipmentDetailsTypeType(ShipmentDetailsType):
    """ShipmentDetailsTypeType -- Details of a shipment.
    extends the ShipmentDetailsType
    ShipmentItem -- For every parcel specified, contains weight in kg, length
    in cm, width in cm and height in cm.
    Service -- Use one dedicated Service node for each service to be
    booked with the shipment product. Add another Service node for
    booking a further service and so on. Successful booking of a
    particular service depends on account permissions and product's
    service combinatorics. I.e. not every service is allowed for every
    product, or can be combined with all other allowed services. The
    service bundles that contain all services are the following.
    Notification -- Mechanism to send notifications by email after successful
    manifesting of shipment.
    BankData -- Bank data can be provided here for different purposes.
    E.g. if COD is booked as service, bank data must be provided by DHL
    customer (mandatory server logic). The collected money will be
    transferred to specified bank account.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = ShipmentDetailsType
    def __init__(self, product=None, accountNumber=None, customerReference=None, shipmentDate=None, costCentre=None, returnShipmentAccountNumber=None, returnShipmentReference=None, ShipmentItem=None, Service=None, Notification=None, BankData=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("ShipmentDetailsTypeType"), self).__init__(product, accountNumber, customerReference, shipmentDate, costCentre, returnShipmentAccountNumber, returnShipmentReference,  **kwargs_)
        self.ShipmentItem = ShipmentItem
        self.ShipmentItem_nsprefix_ = None
        self.Service = Service
        self.Service_nsprefix_ = None
        self.Notification = Notification
        self.Notification_nsprefix_ = None
        self.BankData = BankData
        self.BankData_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentDetailsTypeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentDetailsTypeType.subclass:
            return ShipmentDetailsTypeType.subclass(*args_, **kwargs_)
        else:
            return ShipmentDetailsTypeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ShipmentItem(self):
        return self.ShipmentItem
    def set_ShipmentItem(self, ShipmentItem):
        self.ShipmentItem = ShipmentItem
    def get_Service(self):
        return self.Service
    def set_Service(self, Service):
        self.Service = Service
    def get_Notification(self):
        return self.Notification
    def set_Notification(self, Notification):
        self.Notification = Notification
    def get_BankData(self):
        return self.BankData
    def set_BankData(self, BankData):
        self.BankData = BankData
    def _hasContent(self):
        if (
            self.ShipmentItem is not None or
            self.Service is not None or
            self.Notification is not None or
            self.BankData is not None or
            super(ShipmentDetailsTypeType, self)._hasContent()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentDetailsTypeType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentDetailsTypeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentDetailsTypeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentDetailsTypeType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentDetailsTypeType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentDetailsTypeType'):
        super(ShipmentDetailsTypeType, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentDetailsTypeType')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentDetailsTypeType', fromsubclass_=False, pretty_print=True):
        super(ShipmentDetailsTypeType, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ShipmentItem is not None:
            namespaceprefix_ = self.ShipmentItem_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentItem_nsprefix_) else ''
            self.ShipmentItem.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentItem', pretty_print=pretty_print)
        if self.Service is not None:
            namespaceprefix_ = self.Service_nsprefix_ + ':' if (UseCapturedNS_ and self.Service_nsprefix_) else ''
            self.Service.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Service', pretty_print=pretty_print)
        if self.Notification is not None:
            namespaceprefix_ = self.Notification_nsprefix_ + ':' if (UseCapturedNS_ and self.Notification_nsprefix_) else ''
            self.Notification.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Notification', pretty_print=pretty_print)
        if self.BankData is not None:
            namespaceprefix_ = self.BankData_nsprefix_ + ':' if (UseCapturedNS_ and self.BankData_nsprefix_) else ''
            self.BankData.export(outfile, level, namespaceprefix_, namespacedef_='', name_='BankData', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        super(ShipmentDetailsTypeType, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ShipmentItem':
            class_obj_ = self.get_class_obj_(child_, ShipmentItemType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentItem = obj_
            obj_.original_tagname_ = 'ShipmentItem'
        elif nodeName_ == 'Service':
            obj_ = ShipmentService.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Service = obj_
            obj_.original_tagname_ = 'Service'
        elif nodeName_ == 'Notification':
            obj_ = ShipmentNotificationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Notification = obj_
            obj_.original_tagname_ = 'Notification'
        elif nodeName_ == 'BankData':
            obj_ = BankType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BankData = obj_
            obj_.original_tagname_ = 'BankData'
        super(ShipmentDetailsTypeType, self)._buildChildren(child_, node, nodeName_, True)
# end class ShipmentDetailsTypeType


class ShipmentItemType(GeneratedsSuper):
    """ShipmentItemType -- Item/Piece data.
    weightInKG -- The weight of the piece in kg
    lengthInCM -- The length of the piece in cm.
    widthInCM -- The width of the piece in cm.
    heightInCM -- The height of the piece in cm.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, weightInKG=None, lengthInCM=None, widthInCM=None, heightInCM=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.weightInKG = weightInKG
        self.validate_weightInKGType(self.weightInKG)
        self.weightInKG_nsprefix_ = None
        self.lengthInCM = lengthInCM
        self.validate_lengthInCMType(self.lengthInCM)
        self.lengthInCM_nsprefix_ = None
        self.widthInCM = widthInCM
        self.validate_widthInCMType(self.widthInCM)
        self.widthInCM_nsprefix_ = None
        self.heightInCM = heightInCM
        self.validate_heightInCMType(self.heightInCM)
        self.heightInCM_nsprefix_ = None
        self.extensiontype_ = extensiontype_
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentItemType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentItemType.subclass:
            return ShipmentItemType.subclass(*args_, **kwargs_)
        else:
            return ShipmentItemType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_weightInKG(self):
        return self.weightInKG
    def set_weightInKG(self, weightInKG):
        self.weightInKG = weightInKG
    def get_lengthInCM(self):
        return self.lengthInCM
    def set_lengthInCM(self, lengthInCM):
        self.lengthInCM = lengthInCM
    def get_widthInCM(self):
        return self.widthInCM
    def set_widthInCM(self, widthInCM):
        self.widthInCM = widthInCM
    def get_heightInCM(self):
        return self.heightInCM
    def set_heightInCM(self, heightInCM):
        self.heightInCM = heightInCM
    def get_extensiontype_(self): return self.extensiontype_
    def set_extensiontype_(self, extensiontype_): self.extensiontype_ = extensiontype_
    def validate_weightInKGType(self, value):
        result = True
        # Validate type weightInKGType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if value < 0.0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on weightInKGType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999999.99:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on weightInKGType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_lengthInCMType(self, value):
        result = True
        # Validate type lengthInCMType, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on lengthInCMType' % {"value": value, "lineno": lineno} )
                result = False
            if len(str(value)) >= 4:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on lengthInCMType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_widthInCMType(self, value):
        result = True
        # Validate type widthInCMType, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on widthInCMType' % {"value": value, "lineno": lineno} )
                result = False
            if len(str(value)) >= 4:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on widthInCMType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_heightInCMType(self, value):
        result = True
        # Validate type heightInCMType, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on heightInCMType' % {"value": value, "lineno": lineno} )
                result = False
            if len(str(value)) >= 4:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on heightInCMType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.weightInKG is not None or
            self.lengthInCM is not None or
            self.widthInCM is not None or
            self.heightInCM is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentItemType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentItemType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentItemType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentItemType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentItemType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentItemType'):
        if self.extensiontype_ is not None and 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self.extensiontype_:
                imported_ns_type_prefix_ = GenerateDSNamespaceTypePrefixes_.get(self.extensiontype_, '')
                outfile.write(' xsi:type="%s%s"' % (imported_ns_type_prefix_, self.extensiontype_))
            else:
                outfile.write(' xsi:type="%s"' % self.extensiontype_)
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentItemType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.weightInKG is not None:
            namespaceprefix_ = self.weightInKG_nsprefix_ + ':' if (UseCapturedNS_ and self.weightInKG_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sweightInKG>%s</%sweightInKG>%s' % (namespaceprefix_ , self.gds_format_decimal(self.weightInKG, input_name='weightInKG'), namespaceprefix_ , eol_))
        if self.lengthInCM is not None:
            namespaceprefix_ = self.lengthInCM_nsprefix_ + ':' if (UseCapturedNS_ and self.lengthInCM_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slengthInCM>%s</%slengthInCM>%s' % (namespaceprefix_ , self.gds_format_integer(self.lengthInCM, input_name='lengthInCM'), namespaceprefix_ , eol_))
        if self.widthInCM is not None:
            namespaceprefix_ = self.widthInCM_nsprefix_ + ':' if (UseCapturedNS_ and self.widthInCM_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%swidthInCM>%s</%swidthInCM>%s' % (namespaceprefix_ , self.gds_format_integer(self.widthInCM, input_name='widthInCM'), namespaceprefix_ , eol_))
        if self.heightInCM is not None:
            namespaceprefix_ = self.heightInCM_nsprefix_ + ':' if (UseCapturedNS_ and self.heightInCM_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sheightInCM>%s</%sheightInCM>%s' % (namespaceprefix_ , self.gds_format_integer(self.heightInCM, input_name='heightInCM'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
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
        if nodeName_ == 'weightInKG' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'weightInKG')
            fval_ = self.gds_validate_decimal(fval_, node, 'weightInKG')
            self.weightInKG = fval_
            self.weightInKG_nsprefix_ = child_.prefix
            # validate type weightInKGType
            self.validate_weightInKGType(self.weightInKG)
        elif nodeName_ == 'lengthInCM' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'lengthInCM')
            ival_ = self.gds_validate_integer(ival_, node, 'lengthInCM')
            self.lengthInCM = ival_
            self.lengthInCM_nsprefix_ = child_.prefix
            # validate type lengthInCMType
            self.validate_lengthInCMType(self.lengthInCM)
        elif nodeName_ == 'widthInCM' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'widthInCM')
            ival_ = self.gds_validate_integer(ival_, node, 'widthInCM')
            self.widthInCM = ival_
            self.widthInCM_nsprefix_ = child_.prefix
            # validate type widthInCMType
            self.validate_widthInCMType(self.widthInCM)
        elif nodeName_ == 'heightInCM' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'heightInCM')
            ival_ = self.gds_validate_integer(ival_, node, 'heightInCM')
            self.heightInCM = ival_
            self.heightInCM_nsprefix_ = child_.prefix
            # validate type heightInCMType
            self.validate_heightInCMType(self.heightInCM)
# end class ShipmentItemType


class ShipmentItemTypeType(ShipmentItemType):
    """ShipmentItemTypeType -- Item/Piece data of a shipment.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = ShipmentItemType
    def __init__(self, weightInKG=None, lengthInCM=None, widthInCM=None, heightInCM=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        super(globals().get("ShipmentItemTypeType"), self).__init__(weightInKG, lengthInCM, widthInCM, heightInCM,  **kwargs_)
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentItemTypeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentItemTypeType.subclass:
            return ShipmentItemTypeType.subclass(*args_, **kwargs_)
        else:
            return ShipmentItemTypeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def _hasContent(self):
        if (
            super(ShipmentItemTypeType, self)._hasContent()
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentItemTypeType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentItemTypeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentItemTypeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentItemTypeType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentItemTypeType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentItemTypeType'):
        super(ShipmentItemTypeType, self)._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentItemTypeType')
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentItemTypeType', fromsubclass_=False, pretty_print=True):
        super(ShipmentItemTypeType, self)._exportChildren(outfile, level, namespaceprefix_, namespacedef_, name_, True, pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        super(ShipmentItemTypeType, self)._buildAttributes(node, attrs, already_processed)
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        super(ShipmentItemTypeType, self)._buildChildren(child_, node, nodeName_, True)
        pass
# end class ShipmentItemTypeType


class ShipmentService(GeneratedsSuper):
    """ShipmentService -- GKV shipment services.
    can be
    IndividualSenderRequirement --  This service is used exclusively for shipments with special
    delivery requirements. It is not available for our regular business
    customers.
    PackagingReturn -- Service for package return. For packagingReturn you also have to
    book a return label.
    Endorsement -- Service "Endorsement". Mandatory for shipments with product DHL
    Paket International: V53WPAK
    VisualCheckOfAge -- Service visual age check
    PreferredLocation -- Service preferred location
    PreferredNeighbour -- Service preferred neighbour
    The details field should be set to the preferred neighbours name.
    PreferredDay -- Service preferred day
    NoNeighbourDelivery -- Invoke service No Neighbour Delivery.
    NamedPersonOnly -- Invoke service Named Person Only.
    ReturnReceipt -- Invoke service return receipt.
    Premium -- Premium for fast and safe delivery of international shipments.
    CashOnDelivery -- Service Cash on delivery.
    PDDP -- Postal Delivery Duty Paid Deutsche Post and sender handle import
    duties instead of consignee
    CDP -- Closest Droppoint Delivery to the droppoint closest to the
    address of the recipient of the shipment. For this kind of delivery either
    the phone number and/or the e-mail address of the receiver is mandatory. For
    shipments using DHL Paket International it is recommended that you choose
    one of the three delivery types: Economy Premium CDP Otherwise, the current
    default for the receiver country will be picked.
    Economy -- Standard delivery of international shipments For shipments using
    DHL Paket International it is recommended that you choose one of the three
    delivery types: Economy Premium CDP Otherwise, the current default for the
    receiver country will be picked.
    AdditionalInsurance -- Insure shipment with higher than standard amount.
    BulkyGoods -- Service to ship bulky goods.
    IdentCheck -- Service configuration for IdentCheck.
    ParcelOutletRouting -- Service configuration for ParcelOutletRouting. Details can be an
    email-address, if not set receiver email will be used
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, IndividualSenderRequirement=None, PackagingReturn=None, Endorsement=None, VisualCheckOfAge=None, PreferredLocation=None, PreferredNeighbour=None, PreferredDay=None, NoNeighbourDelivery=None, NamedPersonOnly=None, ReturnReceipt=None, Premium=None, CashOnDelivery=None, PDDP=None, CDP=None, Economy=None, AdditionalInsurance=None, BulkyGoods=None, IdentCheck=None, ParcelOutletRouting=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.IndividualSenderRequirement = IndividualSenderRequirement
        self.IndividualSenderRequirement_nsprefix_ = None
        self.PackagingReturn = PackagingReturn
        self.PackagingReturn_nsprefix_ = None
        self.Endorsement = Endorsement
        self.Endorsement_nsprefix_ = None
        self.VisualCheckOfAge = VisualCheckOfAge
        self.VisualCheckOfAge_nsprefix_ = None
        self.PreferredLocation = PreferredLocation
        self.PreferredLocation_nsprefix_ = None
        self.PreferredNeighbour = PreferredNeighbour
        self.PreferredNeighbour_nsprefix_ = None
        self.PreferredDay = PreferredDay
        self.PreferredDay_nsprefix_ = None
        self.NoNeighbourDelivery = NoNeighbourDelivery
        self.NoNeighbourDelivery_nsprefix_ = None
        self.NamedPersonOnly = NamedPersonOnly
        self.NamedPersonOnly_nsprefix_ = None
        self.ReturnReceipt = ReturnReceipt
        self.ReturnReceipt_nsprefix_ = None
        self.Premium = Premium
        self.Premium_nsprefix_ = None
        self.CashOnDelivery = CashOnDelivery
        self.CashOnDelivery_nsprefix_ = None
        self.PDDP = PDDP
        self.PDDP_nsprefix_ = None
        self.CDP = CDP
        self.CDP_nsprefix_ = None
        self.Economy = Economy
        self.Economy_nsprefix_ = None
        self.AdditionalInsurance = AdditionalInsurance
        self.AdditionalInsurance_nsprefix_ = None
        self.BulkyGoods = BulkyGoods
        self.BulkyGoods_nsprefix_ = None
        self.IdentCheck = IdentCheck
        self.IdentCheck_nsprefix_ = None
        self.ParcelOutletRouting = ParcelOutletRouting
        self.ParcelOutletRouting_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentService)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentService.subclass:
            return ShipmentService.subclass(*args_, **kwargs_)
        else:
            return ShipmentService(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_IndividualSenderRequirement(self):
        return self.IndividualSenderRequirement
    def set_IndividualSenderRequirement(self, IndividualSenderRequirement):
        self.IndividualSenderRequirement = IndividualSenderRequirement
    def get_PackagingReturn(self):
        return self.PackagingReturn
    def set_PackagingReturn(self, PackagingReturn):
        self.PackagingReturn = PackagingReturn
    def get_Endorsement(self):
        return self.Endorsement
    def set_Endorsement(self, Endorsement):
        self.Endorsement = Endorsement
    def get_VisualCheckOfAge(self):
        return self.VisualCheckOfAge
    def set_VisualCheckOfAge(self, VisualCheckOfAge):
        self.VisualCheckOfAge = VisualCheckOfAge
    def get_PreferredLocation(self):
        return self.PreferredLocation
    def set_PreferredLocation(self, PreferredLocation):
        self.PreferredLocation = PreferredLocation
    def get_PreferredNeighbour(self):
        return self.PreferredNeighbour
    def set_PreferredNeighbour(self, PreferredNeighbour):
        self.PreferredNeighbour = PreferredNeighbour
    def get_PreferredDay(self):
        return self.PreferredDay
    def set_PreferredDay(self, PreferredDay):
        self.PreferredDay = PreferredDay
    def get_NoNeighbourDelivery(self):
        return self.NoNeighbourDelivery
    def set_NoNeighbourDelivery(self, NoNeighbourDelivery):
        self.NoNeighbourDelivery = NoNeighbourDelivery
    def get_NamedPersonOnly(self):
        return self.NamedPersonOnly
    def set_NamedPersonOnly(self, NamedPersonOnly):
        self.NamedPersonOnly = NamedPersonOnly
    def get_ReturnReceipt(self):
        return self.ReturnReceipt
    def set_ReturnReceipt(self, ReturnReceipt):
        self.ReturnReceipt = ReturnReceipt
    def get_Premium(self):
        return self.Premium
    def set_Premium(self, Premium):
        self.Premium = Premium
    def get_CashOnDelivery(self):
        return self.CashOnDelivery
    def set_CashOnDelivery(self, CashOnDelivery):
        self.CashOnDelivery = CashOnDelivery
    def get_PDDP(self):
        return self.PDDP
    def set_PDDP(self, PDDP):
        self.PDDP = PDDP
    def get_CDP(self):
        return self.CDP
    def set_CDP(self, CDP):
        self.CDP = CDP
    def get_Economy(self):
        return self.Economy
    def set_Economy(self, Economy):
        self.Economy = Economy
    def get_AdditionalInsurance(self):
        return self.AdditionalInsurance
    def set_AdditionalInsurance(self, AdditionalInsurance):
        self.AdditionalInsurance = AdditionalInsurance
    def get_BulkyGoods(self):
        return self.BulkyGoods
    def set_BulkyGoods(self, BulkyGoods):
        self.BulkyGoods = BulkyGoods
    def get_IdentCheck(self):
        return self.IdentCheck
    def set_IdentCheck(self, IdentCheck):
        self.IdentCheck = IdentCheck
    def get_ParcelOutletRouting(self):
        return self.ParcelOutletRouting
    def set_ParcelOutletRouting(self, ParcelOutletRouting):
        self.ParcelOutletRouting = ParcelOutletRouting
    def _hasContent(self):
        if (
            self.IndividualSenderRequirement is not None or
            self.PackagingReturn is not None or
            self.Endorsement is not None or
            self.VisualCheckOfAge is not None or
            self.PreferredLocation is not None or
            self.PreferredNeighbour is not None or
            self.PreferredDay is not None or
            self.NoNeighbourDelivery is not None or
            self.NamedPersonOnly is not None or
            self.ReturnReceipt is not None or
            self.Premium is not None or
            self.CashOnDelivery is not None or
            self.PDDP is not None or
            self.CDP is not None or
            self.Economy is not None or
            self.AdditionalInsurance is not None or
            self.BulkyGoods is not None or
            self.IdentCheck is not None or
            self.ParcelOutletRouting is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentService', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentService')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentService':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentService')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentService', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentService'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentService', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.IndividualSenderRequirement is not None:
            namespaceprefix_ = self.IndividualSenderRequirement_nsprefix_ + ':' if (UseCapturedNS_ and self.IndividualSenderRequirement_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIndividualSenderRequirement>%s</%sIndividualSenderRequirement>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IndividualSenderRequirement), input_name='IndividualSenderRequirement')), namespaceprefix_ , eol_))
        if self.PackagingReturn is not None:
            namespaceprefix_ = self.PackagingReturn_nsprefix_ + ':' if (UseCapturedNS_ and self.PackagingReturn_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPackagingReturn>%s</%sPackagingReturn>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PackagingReturn), input_name='PackagingReturn')), namespaceprefix_ , eol_))
        if self.Endorsement is not None:
            namespaceprefix_ = self.Endorsement_nsprefix_ + ':' if (UseCapturedNS_ and self.Endorsement_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEndorsement>%s</%sEndorsement>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Endorsement), input_name='Endorsement')), namespaceprefix_ , eol_))
        if self.VisualCheckOfAge is not None:
            namespaceprefix_ = self.VisualCheckOfAge_nsprefix_ + ':' if (UseCapturedNS_ and self.VisualCheckOfAge_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sVisualCheckOfAge>%s</%sVisualCheckOfAge>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.VisualCheckOfAge), input_name='VisualCheckOfAge')), namespaceprefix_ , eol_))
        if self.PreferredLocation is not None:
            namespaceprefix_ = self.PreferredLocation_nsprefix_ + ':' if (UseCapturedNS_ and self.PreferredLocation_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPreferredLocation>%s</%sPreferredLocation>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PreferredLocation), input_name='PreferredLocation')), namespaceprefix_ , eol_))
        if self.PreferredNeighbour is not None:
            namespaceprefix_ = self.PreferredNeighbour_nsprefix_ + ':' if (UseCapturedNS_ and self.PreferredNeighbour_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPreferredNeighbour>%s</%sPreferredNeighbour>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PreferredNeighbour), input_name='PreferredNeighbour')), namespaceprefix_ , eol_))
        if self.PreferredDay is not None:
            namespaceprefix_ = self.PreferredDay_nsprefix_ + ':' if (UseCapturedNS_ and self.PreferredDay_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPreferredDay>%s</%sPreferredDay>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PreferredDay), input_name='PreferredDay')), namespaceprefix_ , eol_))
        if self.NoNeighbourDelivery is not None:
            namespaceprefix_ = self.NoNeighbourDelivery_nsprefix_ + ':' if (UseCapturedNS_ and self.NoNeighbourDelivery_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNoNeighbourDelivery>%s</%sNoNeighbourDelivery>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NoNeighbourDelivery), input_name='NoNeighbourDelivery')), namespaceprefix_ , eol_))
        if self.NamedPersonOnly is not None:
            namespaceprefix_ = self.NamedPersonOnly_nsprefix_ + ':' if (UseCapturedNS_ and self.NamedPersonOnly_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNamedPersonOnly>%s</%sNamedPersonOnly>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.NamedPersonOnly), input_name='NamedPersonOnly')), namespaceprefix_ , eol_))
        if self.ReturnReceipt is not None:
            namespaceprefix_ = self.ReturnReceipt_nsprefix_ + ':' if (UseCapturedNS_ and self.ReturnReceipt_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReturnReceipt>%s</%sReturnReceipt>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ReturnReceipt), input_name='ReturnReceipt')), namespaceprefix_ , eol_))
        if self.Premium is not None:
            namespaceprefix_ = self.Premium_nsprefix_ + ':' if (UseCapturedNS_ and self.Premium_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPremium>%s</%sPremium>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Premium), input_name='Premium')), namespaceprefix_ , eol_))
        if self.CashOnDelivery is not None:
            namespaceprefix_ = self.CashOnDelivery_nsprefix_ + ':' if (UseCapturedNS_ and self.CashOnDelivery_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCashOnDelivery>%s</%sCashOnDelivery>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CashOnDelivery), input_name='CashOnDelivery')), namespaceprefix_ , eol_))
        if self.PDDP is not None:
            namespaceprefix_ = self.PDDP_nsprefix_ + ':' if (UseCapturedNS_ and self.PDDP_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPDDP>%s</%sPDDP>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PDDP), input_name='PDDP')), namespaceprefix_ , eol_))
        if self.CDP is not None:
            namespaceprefix_ = self.CDP_nsprefix_ + ':' if (UseCapturedNS_ and self.CDP_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCDP>%s</%sCDP>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CDP), input_name='CDP')), namespaceprefix_ , eol_))
        if self.Economy is not None:
            namespaceprefix_ = self.Economy_nsprefix_ + ':' if (UseCapturedNS_ and self.Economy_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEconomy>%s</%sEconomy>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Economy), input_name='Economy')), namespaceprefix_ , eol_))
        if self.AdditionalInsurance is not None:
            namespaceprefix_ = self.AdditionalInsurance_nsprefix_ + ':' if (UseCapturedNS_ and self.AdditionalInsurance_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAdditionalInsurance>%s</%sAdditionalInsurance>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AdditionalInsurance), input_name='AdditionalInsurance')), namespaceprefix_ , eol_))
        if self.BulkyGoods is not None:
            namespaceprefix_ = self.BulkyGoods_nsprefix_ + ':' if (UseCapturedNS_ and self.BulkyGoods_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBulkyGoods>%s</%sBulkyGoods>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BulkyGoods), input_name='BulkyGoods')), namespaceprefix_ , eol_))
        if self.IdentCheck is not None:
            namespaceprefix_ = self.IdentCheck_nsprefix_ + ':' if (UseCapturedNS_ and self.IdentCheck_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sIdentCheck>%s</%sIdentCheck>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.IdentCheck), input_name='IdentCheck')), namespaceprefix_ , eol_))
        if self.ParcelOutletRouting is not None:
            namespaceprefix_ = self.ParcelOutletRouting_nsprefix_ + ':' if (UseCapturedNS_ and self.ParcelOutletRouting_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sParcelOutletRouting>%s</%sParcelOutletRouting>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ParcelOutletRouting), input_name='ParcelOutletRouting')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'IndividualSenderRequirement':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IndividualSenderRequirement')
            value_ = self.gds_validate_string(value_, node, 'IndividualSenderRequirement')
            self.IndividualSenderRequirement = value_
            self.IndividualSenderRequirement_nsprefix_ = child_.prefix
        elif nodeName_ == 'PackagingReturn':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PackagingReturn')
            value_ = self.gds_validate_string(value_, node, 'PackagingReturn')
            self.PackagingReturn = value_
            self.PackagingReturn_nsprefix_ = child_.prefix
        elif nodeName_ == 'Endorsement':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Endorsement')
            value_ = self.gds_validate_string(value_, node, 'Endorsement')
            self.Endorsement = value_
            self.Endorsement_nsprefix_ = child_.prefix
        elif nodeName_ == 'VisualCheckOfAge':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'VisualCheckOfAge')
            value_ = self.gds_validate_string(value_, node, 'VisualCheckOfAge')
            self.VisualCheckOfAge = value_
            self.VisualCheckOfAge_nsprefix_ = child_.prefix
        elif nodeName_ == 'PreferredLocation':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PreferredLocation')
            value_ = self.gds_validate_string(value_, node, 'PreferredLocation')
            self.PreferredLocation = value_
            self.PreferredLocation_nsprefix_ = child_.prefix
        elif nodeName_ == 'PreferredNeighbour':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PreferredNeighbour')
            value_ = self.gds_validate_string(value_, node, 'PreferredNeighbour')
            self.PreferredNeighbour = value_
            self.PreferredNeighbour_nsprefix_ = child_.prefix
        elif nodeName_ == 'PreferredDay':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PreferredDay')
            value_ = self.gds_validate_string(value_, node, 'PreferredDay')
            self.PreferredDay = value_
            self.PreferredDay_nsprefix_ = child_.prefix
        elif nodeName_ == 'NoNeighbourDelivery':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NoNeighbourDelivery')
            value_ = self.gds_validate_string(value_, node, 'NoNeighbourDelivery')
            self.NoNeighbourDelivery = value_
            self.NoNeighbourDelivery_nsprefix_ = child_.prefix
        elif nodeName_ == 'NamedPersonOnly':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'NamedPersonOnly')
            value_ = self.gds_validate_string(value_, node, 'NamedPersonOnly')
            self.NamedPersonOnly = value_
            self.NamedPersonOnly_nsprefix_ = child_.prefix
        elif nodeName_ == 'ReturnReceipt':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ReturnReceipt')
            value_ = self.gds_validate_string(value_, node, 'ReturnReceipt')
            self.ReturnReceipt = value_
            self.ReturnReceipt_nsprefix_ = child_.prefix
        elif nodeName_ == 'Premium':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Premium')
            value_ = self.gds_validate_string(value_, node, 'Premium')
            self.Premium = value_
            self.Premium_nsprefix_ = child_.prefix
        elif nodeName_ == 'CashOnDelivery':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CashOnDelivery')
            value_ = self.gds_validate_string(value_, node, 'CashOnDelivery')
            self.CashOnDelivery = value_
            self.CashOnDelivery_nsprefix_ = child_.prefix
        elif nodeName_ == 'PDDP':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PDDP')
            value_ = self.gds_validate_string(value_, node, 'PDDP')
            self.PDDP = value_
            self.PDDP_nsprefix_ = child_.prefix
        elif nodeName_ == 'CDP':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CDP')
            value_ = self.gds_validate_string(value_, node, 'CDP')
            self.CDP = value_
            self.CDP_nsprefix_ = child_.prefix
        elif nodeName_ == 'Economy':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Economy')
            value_ = self.gds_validate_string(value_, node, 'Economy')
            self.Economy = value_
            self.Economy_nsprefix_ = child_.prefix
        elif nodeName_ == 'AdditionalInsurance':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AdditionalInsurance')
            value_ = self.gds_validate_string(value_, node, 'AdditionalInsurance')
            self.AdditionalInsurance = value_
            self.AdditionalInsurance_nsprefix_ = child_.prefix
        elif nodeName_ == 'BulkyGoods':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BulkyGoods')
            value_ = self.gds_validate_string(value_, node, 'BulkyGoods')
            self.BulkyGoods = value_
            self.BulkyGoods_nsprefix_ = child_.prefix
        elif nodeName_ == 'IdentCheck':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IdentCheck')
            value_ = self.gds_validate_string(value_, node, 'IdentCheck')
            self.IdentCheck = value_
            self.IdentCheck_nsprefix_ = child_.prefix
        elif nodeName_ == 'ParcelOutletRouting':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ParcelOutletRouting')
            value_ = self.gds_validate_string(value_, node, 'ParcelOutletRouting')
            self.ParcelOutletRouting = value_
            self.ParcelOutletRouting_nsprefix_ = child_.prefix
# end class ShipmentService


class ShipmentNotificationType(GeneratedsSuper):
    """ShipmentNotificationType -- Notification type
    recipientEmailAddress -- Email address of the recipient. Mandatory if Notification is set.
    templateId -- You may choose between a standard DHL e-mail text (no ID needed)
    or configure an individual text within the section "Administration".
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, recipientEmailAddress=None, templateId=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.recipientEmailAddress = recipientEmailAddress
        self.validate_recipientEmailAddressType(self.recipientEmailAddress)
        self.recipientEmailAddress_nsprefix_ = None
        self.templateId = templateId
        self.validate_templateIdType(self.templateId)
        self.templateId_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentNotificationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentNotificationType.subclass:
            return ShipmentNotificationType.subclass(*args_, **kwargs_)
        else:
            return ShipmentNotificationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_recipientEmailAddress(self):
        return self.recipientEmailAddress
    def set_recipientEmailAddress(self, recipientEmailAddress):
        self.recipientEmailAddress = recipientEmailAddress
    def get_templateId(self):
        return self.templateId
    def set_templateId(self, templateId):
        self.templateId = templateId
    def validate_recipientEmailAddressType(self, value):
        result = True
        # Validate type recipientEmailAddressType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 70:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on recipientEmailAddressType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_templateIdType(self, value):
        result = True
        # Validate type templateIdType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on templateIdType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.recipientEmailAddress is not None or
            self.templateId is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentNotificationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentNotificationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentNotificationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentNotificationType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentNotificationType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentNotificationType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentNotificationType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.recipientEmailAddress is not None:
            namespaceprefix_ = self.recipientEmailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.recipientEmailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%srecipientEmailAddress>%s</%srecipientEmailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.recipientEmailAddress), input_name='recipientEmailAddress')), namespaceprefix_ , eol_))
        if self.templateId is not None:
            namespaceprefix_ = self.templateId_nsprefix_ + ':' if (UseCapturedNS_ and self.templateId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stemplateId>%s</%stemplateId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.templateId), input_name='templateId')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'recipientEmailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'recipientEmailAddress')
            value_ = self.gds_validate_string(value_, node, 'recipientEmailAddress')
            self.recipientEmailAddress = value_
            self.recipientEmailAddress_nsprefix_ = child_.prefix
            # validate type recipientEmailAddressType
            self.validate_recipientEmailAddressType(self.recipientEmailAddress)
        elif nodeName_ == 'templateId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'templateId')
            value_ = self.gds_validate_string(value_, node, 'templateId')
            self.templateId = value_
            self.templateId_nsprefix_ = child_.prefix
            # validate type templateIdType
            self.validate_templateIdType(self.templateId)
# end class ShipmentNotificationType


class ExportDocumentType(GeneratedsSuper):
    """ExportDocumentType -- The data of the export document for a shipment.
    invoiceNumber -- Invoice number if applicable
    exportType -- Export type
    exportTypeDescription -- Description mandatory if ExportType is OTHER.
    termsOfTrade --
    Element provides terms of
    trades, incoterms codes:
    DDP (Delivery Duty Paid)
    DXV (Delivery Duty Paid (excl. VAT))
    DAP (formerly DDU, Delivery At Place)
    DDX (Delivery Duty Paid (excl. Duties, taxes and VAT)
    CPT (Carriage Paid To (within EU only))
    are vaild values.
      
    * placeOfCommital -- PlaceOfCommital is a Locaton the shipment is handed over to DHL
    * additionalFee -- Postage costs billed in the invoice
    * customsCurrency -- CustomsCurrency refers to all stated goods / customs values as
      well as postage costs. The information has to match the currency of the
      commercial invoice or the invoice for customs purposes. ISO 4217 alpha,
      p.E.: EUR for Euro USD for US Dollar GBP for British Pound
    * permitNumber -- The permit number.
    * attestationNumber -- The attestation number.
    * addresseesCustomsReference -- The customs reference is used by customs authorities to identify
      economics operators an/or other persons involved. With the given reference,
      granted authorizations and/or relevant processes in customs clearance an/or
      taxation can be taken into account.
    * sendersCustomsReference -- The customs reference is used by customs authorities to identify
      economics operators an/or other persons involved. With the given reference,
      granted authorizations and/or relevant processes in customs clearance an/or
      taxation can be taken into account.
    * WithElectronicExportNtfctn -- Sets an electronic export notification.
    * ExportDocPosition -- One or more child elements for every position to be defined
      within the Export Document. Each one contains description, country code of
      origin, amount, net weight, customs value. Multiple positions only possible
      for shipments using DHL Paket International (V53WPAK). Shipments using DHL
      Europaket (V54EPAK) can only contain one ExportDocPosition.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, invoiceNumber=None, exportType=None, exportTypeDescription=None, termsOfTrade=None, placeOfCommital=None, additionalFee=None, customsCurrency=None, permitNumber=None, attestationNumber=None, addresseesCustomsReference=None, sendersCustomsReference=None, WithElectronicExportNtfctn=None, ExportDocPosition=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.invoiceNumber = invoiceNumber
        self.validate_invoiceNumberType(self.invoiceNumber)
        self.invoiceNumber_nsprefix_ = None
        self.exportType = exportType
        self.validate_exportTypeType(self.exportType)
        self.exportType_nsprefix_ = None
        self.exportTypeDescription = exportTypeDescription
        self.validate_exportTypeDescriptionType(self.exportTypeDescription)
        self.exportTypeDescription_nsprefix_ = None
        self.termsOfTrade = termsOfTrade
        self.validate_termsOfTradeType(self.termsOfTrade)
        self.termsOfTrade_nsprefix_ = None
        self.placeOfCommital = placeOfCommital
        self.validate_placeOfCommitalType(self.placeOfCommital)
        self.placeOfCommital_nsprefix_ = None
        self.additionalFee = additionalFee
        self.validate_additionalFeeType(self.additionalFee)
        self.additionalFee_nsprefix_ = None
        self.customsCurrency = customsCurrency
        self.validate_customsCurrencyType(self.customsCurrency)
        self.customsCurrency_nsprefix_ = None
        self.permitNumber = permitNumber
        self.validate_permitNumberType(self.permitNumber)
        self.permitNumber_nsprefix_ = None
        self.attestationNumber = attestationNumber
        self.validate_attestationNumberType(self.attestationNumber)
        self.attestationNumber_nsprefix_ = None
        self.addresseesCustomsReference = addresseesCustomsReference
        self.validate_addresseesCustomsReferenceType(self.addresseesCustomsReference)
        self.addresseesCustomsReference_nsprefix_ = None
        self.sendersCustomsReference = sendersCustomsReference
        self.validate_sendersCustomsReferenceType(self.sendersCustomsReference)
        self.sendersCustomsReference_nsprefix_ = None
        self.WithElectronicExportNtfctn = WithElectronicExportNtfctn
        self.WithElectronicExportNtfctn_nsprefix_ = None
        if ExportDocPosition is None:
            self.ExportDocPosition = []
        else:
            self.ExportDocPosition = ExportDocPosition
        self.ExportDocPosition_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ExportDocumentType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ExportDocumentType.subclass:
            return ExportDocumentType.subclass(*args_, **kwargs_)
        else:
            return ExportDocumentType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_invoiceNumber(self):
        return self.invoiceNumber
    def set_invoiceNumber(self, invoiceNumber):
        self.invoiceNumber = invoiceNumber
    def get_exportType(self):
        return self.exportType
    def set_exportType(self, exportType):
        self.exportType = exportType
    def get_exportTypeDescription(self):
        return self.exportTypeDescription
    def set_exportTypeDescription(self, exportTypeDescription):
        self.exportTypeDescription = exportTypeDescription
    def get_termsOfTrade(self):
        return self.termsOfTrade
    def set_termsOfTrade(self, termsOfTrade):
        self.termsOfTrade = termsOfTrade
    def get_placeOfCommital(self):
        return self.placeOfCommital
    def set_placeOfCommital(self, placeOfCommital):
        self.placeOfCommital = placeOfCommital
    def get_additionalFee(self):
        return self.additionalFee
    def set_additionalFee(self, additionalFee):
        self.additionalFee = additionalFee
    def get_customsCurrency(self):
        return self.customsCurrency
    def set_customsCurrency(self, customsCurrency):
        self.customsCurrency = customsCurrency
    def get_permitNumber(self):
        return self.permitNumber
    def set_permitNumber(self, permitNumber):
        self.permitNumber = permitNumber
    def get_attestationNumber(self):
        return self.attestationNumber
    def set_attestationNumber(self, attestationNumber):
        self.attestationNumber = attestationNumber
    def get_addresseesCustomsReference(self):
        return self.addresseesCustomsReference
    def set_addresseesCustomsReference(self, addresseesCustomsReference):
        self.addresseesCustomsReference = addresseesCustomsReference
    def get_sendersCustomsReference(self):
        return self.sendersCustomsReference
    def set_sendersCustomsReference(self, sendersCustomsReference):
        self.sendersCustomsReference = sendersCustomsReference
    def get_WithElectronicExportNtfctn(self):
        return self.WithElectronicExportNtfctn
    def set_WithElectronicExportNtfctn(self, WithElectronicExportNtfctn):
        self.WithElectronicExportNtfctn = WithElectronicExportNtfctn
    def get_ExportDocPosition(self):
        return self.ExportDocPosition
    def set_ExportDocPosition(self, ExportDocPosition):
        self.ExportDocPosition = ExportDocPosition
    def add_ExportDocPosition(self, value):
        self.ExportDocPosition.append(value)
    def insert_ExportDocPosition_at(self, index, value):
        self.ExportDocPosition.insert(index, value)
    def replace_ExportDocPosition_at(self, index, value):
        self.ExportDocPosition[index] = value
    def validate_invoiceNumberType(self, value):
        result = True
        # Validate type invoiceNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on invoiceNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_exportTypeType(self, value):
        result = True
        # Validate type exportTypeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            value = value
            enumerations = ['OTHER', 'PRESENT', 'COMMERCIAL_SAMPLE', 'DOCUMENT', 'RETURN_OF_GOODS', 'COMMERCIAL_GOODS']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on exportTypeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_exportTypeDescriptionType(self, value):
        result = True
        # Validate type exportTypeDescriptionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on exportTypeDescriptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on exportTypeDescriptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_termsOfTradeType(self, value):
        result = True
        # Validate type termsOfTradeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            value = value
            enumerations = ['DDP', 'DXV', 'DAP', 'DDX', 'CPT']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on termsOfTradeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on termsOfTradeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on termsOfTradeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_placeOfCommitalType(self, value):
        result = True
        # Validate type placeOfCommitalType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on placeOfCommitalType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_additionalFeeType(self, value):
        result = True
        # Validate type additionalFeeType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if value < 0.0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on additionalFeeType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999999.99:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on additionalFeeType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_customsCurrencyType(self, value):
        result = True
        # Validate type customsCurrencyType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on customsCurrencyType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_permitNumberType(self, value):
        result = True
        # Validate type permitNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on permitNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_attestationNumberType(self, value):
        result = True
        # Validate type attestationNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on attestationNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_addresseesCustomsReferenceType(self, value):
        result = True
        # Validate type addresseesCustomsReferenceType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on addresseesCustomsReferenceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_sendersCustomsReferenceType(self, value):
        result = True
        # Validate type sendersCustomsReferenceType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on sendersCustomsReferenceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.invoiceNumber is not None or
            self.exportType is not None or
            self.exportTypeDescription is not None or
            self.termsOfTrade is not None or
            self.placeOfCommital is not None or
            self.additionalFee is not None or
            self.customsCurrency is not None or
            self.permitNumber is not None or
            self.attestationNumber is not None or
            self.addresseesCustomsReference is not None or
            self.sendersCustomsReference is not None or
            self.WithElectronicExportNtfctn is not None or
            self.ExportDocPosition
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ExportDocumentType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ExportDocumentType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ExportDocumentType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ExportDocumentType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ExportDocumentType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ExportDocumentType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ExportDocumentType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.invoiceNumber is not None:
            namespaceprefix_ = self.invoiceNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.invoiceNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sinvoiceNumber>%s</%sinvoiceNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.invoiceNumber), input_name='invoiceNumber')), namespaceprefix_ , eol_))
        if self.exportType is not None:
            namespaceprefix_ = self.exportType_nsprefix_ + ':' if (UseCapturedNS_ and self.exportType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sexportType>%s</%sexportType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.exportType), input_name='exportType')), namespaceprefix_ , eol_))
        if self.exportTypeDescription is not None:
            namespaceprefix_ = self.exportTypeDescription_nsprefix_ + ':' if (UseCapturedNS_ and self.exportTypeDescription_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sexportTypeDescription>%s</%sexportTypeDescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.exportTypeDescription), input_name='exportTypeDescription')), namespaceprefix_ , eol_))
        if self.termsOfTrade is not None:
            namespaceprefix_ = self.termsOfTrade_nsprefix_ + ':' if (UseCapturedNS_ and self.termsOfTrade_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stermsOfTrade>%s</%stermsOfTrade>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.termsOfTrade), input_name='termsOfTrade')), namespaceprefix_ , eol_))
        if self.placeOfCommital is not None:
            namespaceprefix_ = self.placeOfCommital_nsprefix_ + ':' if (UseCapturedNS_ and self.placeOfCommital_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%splaceOfCommital>%s</%splaceOfCommital>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.placeOfCommital), input_name='placeOfCommital')), namespaceprefix_ , eol_))
        if self.additionalFee is not None:
            namespaceprefix_ = self.additionalFee_nsprefix_ + ':' if (UseCapturedNS_ and self.additionalFee_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sadditionalFee>%s</%sadditionalFee>%s' % (namespaceprefix_ , self.gds_format_decimal(self.additionalFee, input_name='additionalFee'), namespaceprefix_ , eol_))
        if self.customsCurrency is not None:
            namespaceprefix_ = self.customsCurrency_nsprefix_ + ':' if (UseCapturedNS_ and self.customsCurrency_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scustomsCurrency>%s</%scustomsCurrency>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.customsCurrency), input_name='customsCurrency')), namespaceprefix_ , eol_))
        if self.permitNumber is not None:
            namespaceprefix_ = self.permitNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.permitNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spermitNumber>%s</%spermitNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.permitNumber), input_name='permitNumber')), namespaceprefix_ , eol_))
        if self.attestationNumber is not None:
            namespaceprefix_ = self.attestationNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.attestationNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sattestationNumber>%s</%sattestationNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.attestationNumber), input_name='attestationNumber')), namespaceprefix_ , eol_))
        if self.addresseesCustomsReference is not None:
            namespaceprefix_ = self.addresseesCustomsReference_nsprefix_ + ':' if (UseCapturedNS_ and self.addresseesCustomsReference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saddresseesCustomsReference>%s</%saddresseesCustomsReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.addresseesCustomsReference), input_name='addresseesCustomsReference')), namespaceprefix_ , eol_))
        if self.sendersCustomsReference is not None:
            namespaceprefix_ = self.sendersCustomsReference_nsprefix_ + ':' if (UseCapturedNS_ and self.sendersCustomsReference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssendersCustomsReference>%s</%ssendersCustomsReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.sendersCustomsReference), input_name='sendersCustomsReference')), namespaceprefix_ , eol_))
        if self.WithElectronicExportNtfctn is not None:
            namespaceprefix_ = self.WithElectronicExportNtfctn_nsprefix_ + ':' if (UseCapturedNS_ and self.WithElectronicExportNtfctn_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWithElectronicExportNtfctn>%s</%sWithElectronicExportNtfctn>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.WithElectronicExportNtfctn), input_name='WithElectronicExportNtfctn')), namespaceprefix_ , eol_))
        for ExportDocPosition_ in self.ExportDocPosition:
            namespaceprefix_ = self.ExportDocPosition_nsprefix_ + ':' if (UseCapturedNS_ and self.ExportDocPosition_nsprefix_) else ''
            ExportDocPosition_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ExportDocPosition', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'invoiceNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'invoiceNumber')
            value_ = self.gds_validate_string(value_, node, 'invoiceNumber')
            self.invoiceNumber = value_
            self.invoiceNumber_nsprefix_ = child_.prefix
            # validate type invoiceNumberType
            self.validate_invoiceNumberType(self.invoiceNumber)
        elif nodeName_ == 'exportType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'exportType')
            value_ = self.gds_validate_string(value_, node, 'exportType')
            self.exportType = value_
            self.exportType_nsprefix_ = child_.prefix
            # validate type exportTypeType
            self.validate_exportTypeType(self.exportType)
        elif nodeName_ == 'exportTypeDescription':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'exportTypeDescription')
            value_ = self.gds_validate_string(value_, node, 'exportTypeDescription')
            self.exportTypeDescription = value_
            self.exportTypeDescription_nsprefix_ = child_.prefix
            # validate type exportTypeDescriptionType
            self.validate_exportTypeDescriptionType(self.exportTypeDescription)
        elif nodeName_ == 'termsOfTrade':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'termsOfTrade')
            value_ = self.gds_validate_string(value_, node, 'termsOfTrade')
            self.termsOfTrade = value_
            self.termsOfTrade_nsprefix_ = child_.prefix
            # validate type termsOfTradeType
            self.validate_termsOfTradeType(self.termsOfTrade)
        elif nodeName_ == 'placeOfCommital':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'placeOfCommital')
            value_ = self.gds_validate_string(value_, node, 'placeOfCommital')
            self.placeOfCommital = value_
            self.placeOfCommital_nsprefix_ = child_.prefix
            # validate type placeOfCommitalType
            self.validate_placeOfCommitalType(self.placeOfCommital)
        elif nodeName_ == 'additionalFee' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'additionalFee')
            fval_ = self.gds_validate_decimal(fval_, node, 'additionalFee')
            self.additionalFee = fval_
            self.additionalFee_nsprefix_ = child_.prefix
            # validate type additionalFeeType
            self.validate_additionalFeeType(self.additionalFee)
        elif nodeName_ == 'customsCurrency':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'customsCurrency')
            value_ = self.gds_validate_string(value_, node, 'customsCurrency')
            self.customsCurrency = value_
            self.customsCurrency_nsprefix_ = child_.prefix
            # validate type customsCurrencyType
            self.validate_customsCurrencyType(self.customsCurrency)
        elif nodeName_ == 'permitNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'permitNumber')
            value_ = self.gds_validate_string(value_, node, 'permitNumber')
            self.permitNumber = value_
            self.permitNumber_nsprefix_ = child_.prefix
            # validate type permitNumberType
            self.validate_permitNumberType(self.permitNumber)
        elif nodeName_ == 'attestationNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'attestationNumber')
            value_ = self.gds_validate_string(value_, node, 'attestationNumber')
            self.attestationNumber = value_
            self.attestationNumber_nsprefix_ = child_.prefix
            # validate type attestationNumberType
            self.validate_attestationNumberType(self.attestationNumber)
        elif nodeName_ == 'addresseesCustomsReference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'addresseesCustomsReference')
            value_ = self.gds_validate_string(value_, node, 'addresseesCustomsReference')
            self.addresseesCustomsReference = value_
            self.addresseesCustomsReference_nsprefix_ = child_.prefix
            # validate type addresseesCustomsReferenceType
            self.validate_addresseesCustomsReferenceType(self.addresseesCustomsReference)
        elif nodeName_ == 'sendersCustomsReference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'sendersCustomsReference')
            value_ = self.gds_validate_string(value_, node, 'sendersCustomsReference')
            self.sendersCustomsReference = value_
            self.sendersCustomsReference_nsprefix_ = child_.prefix
            # validate type sendersCustomsReferenceType
            self.validate_sendersCustomsReferenceType(self.sendersCustomsReference)
        elif nodeName_ == 'WithElectronicExportNtfctn':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'WithElectronicExportNtfctn')
            value_ = self.gds_validate_string(value_, node, 'WithElectronicExportNtfctn')
            self.WithElectronicExportNtfctn = value_
            self.WithElectronicExportNtfctn_nsprefix_ = child_.prefix
        elif nodeName_ == 'ExportDocPosition':
            obj_ = ExportDocPositionType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ExportDocPosition.append(obj_)
            obj_.original_tagname_ = 'ExportDocPosition'
# end class ExportDocumentType


class FurtherAddressesType(GeneratedsSuper):
    """FurtherAddressesType -- Further address information The following data fields from the
    cis_base-types are processed/mandatory/optional:
    -------------------------------------------------------------------------------------------------------
    Salutation (optional) : cis:NameType-
    >
    Person-
    >
    salutation Company Name 1
    (mandatory): cis:NameType-
    >
    Company-
    >
    name1 Company Name 2 (optional) :
    cis:NameType-
    >
    Company-
    >
    name2 Contact Name (mandatory):
    cis:CommunicationType-
    >
    contactPerson Street Name (mandatory):
    cis:NativeAddressType-
    >
    streetName Street Number (mandatory):
    cis:NativeAddressType-
    >
    streetNumber Add. Address (optional) :
    cis:NativeAddressType-
    >
    careOfName Postcode (mandatory):
    cis:NativeAddressType-
    >
    zip City Name (mandatory): cis:NativeAddressType-
    >
    city
    ISO Country Code (mandatory):
    cis:NativeAddressType-
    >
    Origin-
    >
    CountryType-
    >
    countryISOType Phone Number
    (mandatory): cis:CommunicationType-
    >
    phone Email Address (mandatory):
    cis:CommunicationType-
    >
    email
    DeliveryAdress -- Mandatory if further address is to be specified.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DeliveryAdress=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DeliveryAdress = DeliveryAdress
        self.DeliveryAdress_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, FurtherAddressesType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if FurtherAddressesType.subclass:
            return FurtherAddressesType.subclass(*args_, **kwargs_)
        else:
            return FurtherAddressesType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DeliveryAdress(self):
        return self.DeliveryAdress
    def set_DeliveryAdress(self, DeliveryAdress):
        self.DeliveryAdress = DeliveryAdress
    def _hasContent(self):
        if (
            self.DeliveryAdress is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FurtherAddressesType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('FurtherAddressesType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'FurtherAddressesType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='FurtherAddressesType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='FurtherAddressesType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='FurtherAddressesType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='FurtherAddressesType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DeliveryAdress is not None:
            namespaceprefix_ = self.DeliveryAdress_nsprefix_ + ':' if (UseCapturedNS_ and self.DeliveryAdress_nsprefix_) else ''
            self.DeliveryAdress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DeliveryAdress', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DeliveryAdress':
            obj_ = DeliveryAdressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DeliveryAdress = obj_
            obj_.original_tagname_ = 'DeliveryAdress'
# end class FurtherAddressesType


class LabelData(GeneratedsSuper):
    """LabelData -- The status of the getLabel operation and the url for requesting the label
    (if available).
    Status -- Success status of processing retrieval of particular shipment
    label.
    shipmentNumber -- For successful and unsuccessful operations, the requested
    ShipmentNumber of the label to be retrieved is returned. This is no matter
    if it the operation could be performed or not.
    labelUrl -- If label output format was requested as 'URL' via
    LabelResponseType, this element will be returned. It contains the URL to
    access the PDF label. This is default output format if not specified
    other by client in labelResponseType. Depending on setting in customer
    profile all labels or just the shipmentlabel.
    labelData --  Label as base64 encoded pdf data, depending on setting in
    customer profile all labels or just the shipmentlabel.
    returnLabelUrl -- If label output format was requested as 'URL' via
    LabelResponseType, this element will be returned. It contains the URL to
    access the PDF label. This is default output format if not specified
    other by client in labelResponseType. Depending on setting in customer
    profile all labels or just the returnshipmentlabel.
    returnLabelData --  Label as base64 encoded pdf data, depending on setting in
    customer profile all labels or just the returnshipmentlabel.
    exportLabelUrl -- If label output format was requested as 'URL' via
    LabelResponseType, this element will be returned. It contains the URL to
    access the PDF label. This is default output format if not specified
    other by client in labelResponseType. Depending on setting in customer
    profile all labels or just the export documents.
    exportLabelData --  Label as base64 encoded pdf data, depending on setting in
    customer profile all labels or just the export documents.
    codLabelUrl -- If label output format was requested as 'URL' via
    LabelResponseType, this element will be returned. It contains the URL to
    access the PDF label. This is default output format if not specified
    other by client in labelResponseType. Depending on setting in customer
    profile all labels or just the cod related documents.
    codLabelData --  Label as base64 encoded pdf data, depending on setting in
    customer profile all labels or just the cod related documents.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Status=None, shipmentNumber=None, labelUrl=None, labelData=None, returnLabelUrl=None, returnLabelData=None, exportLabelUrl=None, exportLabelData=None, codLabelUrl=None, codLabelData=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
        self.shipmentNumber = shipmentNumber
        self.validate_shipmentNumber(self.shipmentNumber)
        self.shipmentNumber_nsprefix_ = None
        self.labelUrl = labelUrl
        self.labelUrl_nsprefix_ = None
        self.labelData = labelData
        self.labelData_nsprefix_ = None
        self.returnLabelUrl = returnLabelUrl
        self.returnLabelUrl_nsprefix_ = None
        self.returnLabelData = returnLabelData
        self.returnLabelData_nsprefix_ = None
        self.exportLabelUrl = exportLabelUrl
        self.exportLabelUrl_nsprefix_ = None
        self.exportLabelData = exportLabelData
        self.exportLabelData_nsprefix_ = None
        self.codLabelUrl = codLabelUrl
        self.codLabelUrl_nsprefix_ = None
        self.codLabelData = codLabelData
        self.codLabelData_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, LabelData)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if LabelData.subclass:
            return LabelData.subclass(*args_, **kwargs_)
        else:
            return LabelData(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def get_shipmentNumber(self):
        return self.shipmentNumber
    def set_shipmentNumber(self, shipmentNumber):
        self.shipmentNumber = shipmentNumber
    def get_labelUrl(self):
        return self.labelUrl
    def set_labelUrl(self, labelUrl):
        self.labelUrl = labelUrl
    def get_labelData(self):
        return self.labelData
    def set_labelData(self, labelData):
        self.labelData = labelData
    def get_returnLabelUrl(self):
        return self.returnLabelUrl
    def set_returnLabelUrl(self, returnLabelUrl):
        self.returnLabelUrl = returnLabelUrl
    def get_returnLabelData(self):
        return self.returnLabelData
    def set_returnLabelData(self, returnLabelData):
        self.returnLabelData = returnLabelData
    def get_exportLabelUrl(self):
        return self.exportLabelUrl
    def set_exportLabelUrl(self, exportLabelUrl):
        self.exportLabelUrl = exportLabelUrl
    def get_exportLabelData(self):
        return self.exportLabelData
    def set_exportLabelData(self, exportLabelData):
        self.exportLabelData = exportLabelData
    def get_codLabelUrl(self):
        return self.codLabelUrl
    def set_codLabelUrl(self, codLabelUrl):
        self.codLabelUrl = codLabelUrl
    def get_codLabelData(self):
        return self.codLabelData
    def set_codLabelData(self, codLabelData):
        self.codLabelData = codLabelData
    def validate_shipmentNumber(self, value):
        result = True
        # Validate type shipmentNumber, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.Status is not None or
            self.shipmentNumber is not None or
            self.labelUrl is not None or
            self.labelData is not None or
            self.returnLabelUrl is not None or
            self.returnLabelData is not None or
            self.exportLabelUrl is not None or
            self.exportLabelData is not None or
            self.codLabelUrl is not None or
            self.codLabelData is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LabelData', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('LabelData')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'LabelData':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='LabelData')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='LabelData', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='LabelData'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='LabelData', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            self.Status.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Status', pretty_print=pretty_print)
        if self.shipmentNumber is not None:
            namespaceprefix_ = self.shipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.shipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sshipmentNumber>%s</%sshipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.shipmentNumber), input_name='shipmentNumber')), namespaceprefix_ , eol_))
        if self.labelUrl is not None:
            namespaceprefix_ = self.labelUrl_nsprefix_ + ':' if (UseCapturedNS_ and self.labelUrl_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slabelUrl>%s</%slabelUrl>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.labelUrl), input_name='labelUrl')), namespaceprefix_ , eol_))
        if self.labelData is not None:
            namespaceprefix_ = self.labelData_nsprefix_ + ':' if (UseCapturedNS_ and self.labelData_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slabelData>%s</%slabelData>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.labelData), input_name='labelData')), namespaceprefix_ , eol_))
        if self.returnLabelUrl is not None:
            namespaceprefix_ = self.returnLabelUrl_nsprefix_ + ':' if (UseCapturedNS_ and self.returnLabelUrl_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sreturnLabelUrl>%s</%sreturnLabelUrl>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.returnLabelUrl), input_name='returnLabelUrl')), namespaceprefix_ , eol_))
        if self.returnLabelData is not None:
            namespaceprefix_ = self.returnLabelData_nsprefix_ + ':' if (UseCapturedNS_ and self.returnLabelData_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sreturnLabelData>%s</%sreturnLabelData>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.returnLabelData), input_name='returnLabelData')), namespaceprefix_ , eol_))
        if self.exportLabelUrl is not None:
            namespaceprefix_ = self.exportLabelUrl_nsprefix_ + ':' if (UseCapturedNS_ and self.exportLabelUrl_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sexportLabelUrl>%s</%sexportLabelUrl>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.exportLabelUrl), input_name='exportLabelUrl')), namespaceprefix_ , eol_))
        if self.exportLabelData is not None:
            namespaceprefix_ = self.exportLabelData_nsprefix_ + ':' if (UseCapturedNS_ and self.exportLabelData_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sexportLabelData>%s</%sexportLabelData>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.exportLabelData), input_name='exportLabelData')), namespaceprefix_ , eol_))
        if self.codLabelUrl is not None:
            namespaceprefix_ = self.codLabelUrl_nsprefix_ + ':' if (UseCapturedNS_ and self.codLabelUrl_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scodLabelUrl>%s</%scodLabelUrl>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.codLabelUrl), input_name='codLabelUrl')), namespaceprefix_ , eol_))
        if self.codLabelData is not None:
            namespaceprefix_ = self.codLabelData_nsprefix_ + ':' if (UseCapturedNS_ and self.codLabelData_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scodLabelData>%s</%scodLabelData>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.codLabelData), input_name='codLabelData')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Status':
            obj_ = Statusinformation.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Status = obj_
            obj_.original_tagname_ = 'Status'
        elif nodeName_ == 'shipmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'shipmentNumber')
            value_ = self.gds_validate_string(value_, node, 'shipmentNumber')
            self.shipmentNumber = value_
            self.shipmentNumber_nsprefix_ = child_.prefix
            # validate type shipmentNumber
            self.validate_shipmentNumber(self.shipmentNumber)
        elif nodeName_ == 'labelUrl':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'labelUrl')
            value_ = self.gds_validate_string(value_, node, 'labelUrl')
            self.labelUrl = value_
            self.labelUrl_nsprefix_ = child_.prefix
        elif nodeName_ == 'labelData':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'labelData')
            value_ = self.gds_validate_string(value_, node, 'labelData')
            self.labelData = value_
            self.labelData_nsprefix_ = child_.prefix
        elif nodeName_ == 'returnLabelUrl':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'returnLabelUrl')
            value_ = self.gds_validate_string(value_, node, 'returnLabelUrl')
            self.returnLabelUrl = value_
            self.returnLabelUrl_nsprefix_ = child_.prefix
        elif nodeName_ == 'returnLabelData':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'returnLabelData')
            value_ = self.gds_validate_string(value_, node, 'returnLabelData')
            self.returnLabelData = value_
            self.returnLabelData_nsprefix_ = child_.prefix
        elif nodeName_ == 'exportLabelUrl':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'exportLabelUrl')
            value_ = self.gds_validate_string(value_, node, 'exportLabelUrl')
            self.exportLabelUrl = value_
            self.exportLabelUrl_nsprefix_ = child_.prefix
        elif nodeName_ == 'exportLabelData':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'exportLabelData')
            value_ = self.gds_validate_string(value_, node, 'exportLabelData')
            self.exportLabelData = value_
            self.exportLabelData_nsprefix_ = child_.prefix
        elif nodeName_ == 'codLabelUrl':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'codLabelUrl')
            value_ = self.gds_validate_string(value_, node, 'codLabelUrl')
            self.codLabelUrl = value_
            self.codLabelUrl_nsprefix_ = child_.prefix
        elif nodeName_ == 'codLabelData':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'codLabelData')
            value_ = self.gds_validate_string(value_, node, 'codLabelData')
            self.codLabelData = value_
            self.codLabelData_nsprefix_ = child_.prefix
# end class LabelData


class ExportDocData(GeneratedsSuper):
    """ExportDocData -- The status of the getLabel operation and the url for requesting the label
    (if available)
    shipmentNumber -- ShipmentNumber
    Status -- Status of the request (value of zero means, the request was
    processed without error; value greater than zero indicates that an error
    occurred).
    exportDocData -- Export doc as base64 encoded pdf data
    exportDocURL -- URL for downloading the Export doc as pdf
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, shipmentNumber=None, Status=None, exportDocData=None, exportDocURL=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.shipmentNumber = shipmentNumber
        self.validate_shipmentNumber(self.shipmentNumber)
        self.shipmentNumber_nsprefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
        self.exportDocData = exportDocData
        self.exportDocData_nsprefix_ = None
        self.exportDocURL = exportDocURL
        self.exportDocURL_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ExportDocData)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ExportDocData.subclass:
            return ExportDocData.subclass(*args_, **kwargs_)
        else:
            return ExportDocData(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_shipmentNumber(self):
        return self.shipmentNumber
    def set_shipmentNumber(self, shipmentNumber):
        self.shipmentNumber = shipmentNumber
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def get_exportDocData(self):
        return self.exportDocData
    def set_exportDocData(self, exportDocData):
        self.exportDocData = exportDocData
    def get_exportDocURL(self):
        return self.exportDocURL
    def set_exportDocURL(self, exportDocURL):
        self.exportDocURL = exportDocURL
    def validate_shipmentNumber(self, value):
        result = True
        # Validate type shipmentNumber, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.shipmentNumber is not None or
            self.Status is not None or
            self.exportDocData is not None or
            self.exportDocURL is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ExportDocData', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ExportDocData')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ExportDocData':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ExportDocData')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ExportDocData', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ExportDocData'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ExportDocData', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.shipmentNumber is not None:
            namespaceprefix_ = self.shipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.shipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sshipmentNumber>%s</%sshipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.shipmentNumber), input_name='shipmentNumber')), namespaceprefix_ , eol_))
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            self.Status.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Status', pretty_print=pretty_print)
        if self.exportDocData is not None:
            namespaceprefix_ = self.exportDocData_nsprefix_ + ':' if (UseCapturedNS_ and self.exportDocData_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sexportDocData>%s</%sexportDocData>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.exportDocData), input_name='exportDocData')), namespaceprefix_ , eol_))
        if self.exportDocURL is not None:
            namespaceprefix_ = self.exportDocURL_nsprefix_ + ':' if (UseCapturedNS_ and self.exportDocURL_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sexportDocURL>%s</%sexportDocURL>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.exportDocURL), input_name='exportDocURL')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
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
        elif nodeName_ == 'Status':
            obj_ = Statusinformation.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Status = obj_
            obj_.original_tagname_ = 'Status'
        elif nodeName_ == 'exportDocData':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'exportDocData')
            value_ = self.gds_validate_string(value_, node, 'exportDocData')
            self.exportDocData = value_
            self.exportDocData_nsprefix_ = child_.prefix
        elif nodeName_ == 'exportDocURL':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'exportDocURL')
            value_ = self.gds_validate_string(value_, node, 'exportDocURL')
            self.exportDocURL = value_
            self.exportDocURL_nsprefix_ = child_.prefix
# end class ExportDocData


class ManifestState(GeneratedsSuper):
    """ManifestState -- The status of a doManifest operation.
    shipmentNumber -- ShipmentNumber
    Status -- Status of the request (value of zero means, the request was
    processed without error; value greater than zero indicates that an error
    occurred).
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, shipmentNumber=None, Status=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.shipmentNumber = shipmentNumber
        self.validate_shipmentNumber(self.shipmentNumber)
        self.shipmentNumber_nsprefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ManifestState)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ManifestState.subclass:
            return ManifestState.subclass(*args_, **kwargs_)
        else:
            return ManifestState(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_shipmentNumber(self):
        return self.shipmentNumber
    def set_shipmentNumber(self, shipmentNumber):
        self.shipmentNumber = shipmentNumber
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def validate_shipmentNumber(self, value):
        result = True
        # Validate type shipmentNumber, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.shipmentNumber is not None or
            self.Status is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ManifestState', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ManifestState')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ManifestState':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ManifestState')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ManifestState', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ManifestState'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ManifestState', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.shipmentNumber is not None:
            namespaceprefix_ = self.shipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.shipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sshipmentNumber>%s</%sshipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.shipmentNumber), input_name='shipmentNumber')), namespaceprefix_ , eol_))
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            self.Status.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Status', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
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
        elif nodeName_ == 'Status':
            obj_ = Statusinformation.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Status = obj_
            obj_.original_tagname_ = 'Status'
# end class ManifestState


class DeletionState(GeneratedsSuper):
    """DeletionState -- The status of a deleteShipment operation.
    shipmentNumber -- For successful and unsuccessful operations, the requested
    ShipmentNumber to be deleted is returned. This is no matter if the operation
    could be performed or not.
    Status -- Success status of processing the deletion of particular shipment.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, shipmentNumber=None, Status=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.shipmentNumber = shipmentNumber
        self.validate_shipmentNumber(self.shipmentNumber)
        self.shipmentNumber_nsprefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DeletionState)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DeletionState.subclass:
            return DeletionState.subclass(*args_, **kwargs_)
        else:
            return DeletionState(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_shipmentNumber(self):
        return self.shipmentNumber
    def set_shipmentNumber(self, shipmentNumber):
        self.shipmentNumber = shipmentNumber
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def validate_shipmentNumber(self, value):
        result = True
        # Validate type shipmentNumber, a restriction on xs:string.
        pass
        return result
    def _hasContent(self):
        if (
            self.shipmentNumber is not None or
            self.Status is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeletionState', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DeletionState')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DeletionState':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DeletionState')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DeletionState', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DeletionState'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeletionState', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.shipmentNumber is not None:
            namespaceprefix_ = self.shipmentNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.shipmentNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sshipmentNumber>%s</%sshipmentNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.shipmentNumber), input_name='shipmentNumber')), namespaceprefix_ , eol_))
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            self.Status.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Status', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
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
        elif nodeName_ == 'Status':
            obj_ = Statusinformation.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Status = obj_
            obj_.original_tagname_ = 'Status'
# end class DeletionState


class BookPickupRequest(GeneratedsSuper):
    """BookPickupRequest -- The data for a pickup order.
    Version -- The version of the webservice implementation for which the
    requesting client is developed.
    BookingInformation -- Contains information in further leaf elements about product,
    DHL account, pickup date and time, pickup location, amount of pieces,
    pallets, and shipments, moreover weight and volume weight, size.
    PickupAddress -- The pickup address.
    ContactOrderer -- The address and contact information of the orderer.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, BookingInformation=None, PickupAddress=None, ContactOrderer=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        self.BookingInformation = BookingInformation
        self.BookingInformation_nsprefix_ = None
        self.PickupAddress = PickupAddress
        self.PickupAddress_nsprefix_ = None
        self.ContactOrderer = ContactOrderer
        self.ContactOrderer_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, BookPickupRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BookPickupRequest.subclass:
            return BookPickupRequest.subclass(*args_, **kwargs_)
        else:
            return BookPickupRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_BookingInformation(self):
        return self.BookingInformation
    def set_BookingInformation(self, BookingInformation):
        self.BookingInformation = BookingInformation
    def get_PickupAddress(self):
        return self.PickupAddress
    def set_PickupAddress(self, PickupAddress):
        self.PickupAddress = PickupAddress
    def get_ContactOrderer(self):
        return self.ContactOrderer
    def set_ContactOrderer(self, ContactOrderer):
        self.ContactOrderer = ContactOrderer
    def _hasContent(self):
        if (
            self.Version is not None or
            self.BookingInformation is not None or
            self.PickupAddress is not None or
            self.ContactOrderer is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BookPickupRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('BookPickupRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'BookPickupRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BookPickupRequest')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='BookPickupRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='BookPickupRequest'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BookPickupRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.BookingInformation is not None:
            namespaceprefix_ = self.BookingInformation_nsprefix_ + ':' if (UseCapturedNS_ and self.BookingInformation_nsprefix_) else ''
            self.BookingInformation.export(outfile, level, namespaceprefix_, namespacedef_='', name_='BookingInformation', pretty_print=pretty_print)
        if self.PickupAddress is not None:
            namespaceprefix_ = self.PickupAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupAddress_nsprefix_) else ''
            self.PickupAddress.export(outfile, level, namespaceprefix_, namespacedef_='', name_='PickupAddress', pretty_print=pretty_print)
        if self.ContactOrderer is not None:
            namespaceprefix_ = self.ContactOrderer_nsprefix_ + ':' if (UseCapturedNS_ and self.ContactOrderer_nsprefix_) else ''
            self.ContactOrderer.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ContactOrderer', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'BookingInformation':
            obj_ = PickupBookingInformationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BookingInformation = obj_
            obj_.original_tagname_ = 'BookingInformation'
        elif nodeName_ == 'PickupAddress':
            obj_ = PickupAddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PickupAddress = obj_
            obj_.original_tagname_ = 'PickupAddress'
        elif nodeName_ == 'ContactOrderer':
            obj_ = PickupOrdererType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ContactOrderer = obj_
            obj_.original_tagname_ = 'ContactOrderer'
# end class BookPickupRequest


class BookPickupResponse(GeneratedsSuper):
    """BookPickupResponse -- The data for a pickup order.
    Version -- The version of the webservice implementation.
    Status -- Success status after processing the request.
    ConfirmationNumber -- The confirmation number of the successfully created pickup
    order. It can later be used for cancelling a pickup order. Confirmation
    number is not available for each pickup type.
    ShipmentNumber -- If available, a shipment number is returned.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, Status=None, ConfirmationNumber=None, ShipmentNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
        self.ConfirmationNumber = ConfirmationNumber
        self.ConfirmationNumber_nsprefix_ = None
        self.ShipmentNumber = ShipmentNumber
        self.ShipmentNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, BookPickupResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BookPickupResponse.subclass:
            return BookPickupResponse.subclass(*args_, **kwargs_)
        else:
            return BookPickupResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def get_ConfirmationNumber(self):
        return self.ConfirmationNumber
    def set_ConfirmationNumber(self, ConfirmationNumber):
        self.ConfirmationNumber = ConfirmationNumber
    def get_ShipmentNumber(self):
        return self.ShipmentNumber
    def set_ShipmentNumber(self, ShipmentNumber):
        self.ShipmentNumber = ShipmentNumber
    def _hasContent(self):
        if (
            self.Version is not None or
            self.Status is not None or
            self.ConfirmationNumber is not None or
            self.ShipmentNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BookPickupResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('BookPickupResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'BookPickupResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BookPickupResponse')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='BookPickupResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='BookPickupResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BookPickupResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            self.Status.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Status', pretty_print=pretty_print)
        if self.ConfirmationNumber is not None:
            namespaceprefix_ = self.ConfirmationNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ConfirmationNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sConfirmationNumber>%s</%sConfirmationNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ConfirmationNumber), input_name='ConfirmationNumber')), namespaceprefix_ , eol_))
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
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'Status':
            obj_ = Statusinformation.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Status = obj_
            obj_.original_tagname_ = 'Status'
        elif nodeName_ == 'ConfirmationNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ConfirmationNumber')
            value_ = self.gds_validate_string(value_, node, 'ConfirmationNumber')
            self.ConfirmationNumber = value_
            self.ConfirmationNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'ShipmentNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShipmentNumber')
            value_ = self.gds_validate_string(value_, node, 'ShipmentNumber')
            self.ShipmentNumber = value_
            self.ShipmentNumber_nsprefix_ = child_.prefix
# end class BookPickupResponse


class PickupDetailsType(GeneratedsSuper):
    """PickupDetailsType -- The details of a pickup order.
    PickupDate -- Pickup date in format yyyy-mm-dd. Mandatory if pickup is booked
    along with shipment order.
    ReadyByTime -- Earliest time for pickup. Format is hh:mm.
    ClosingTime -- Lates time for pickup. Format is hh:mm.
    Remark -- Remarks to be considered when pickup is done.
    PickupLocation -- Area to further detail pickup location beyond address.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, PickupDate=None, ReadyByTime=None, ClosingTime=None, Remark=None, PickupLocation=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.PickupDate = PickupDate
        self.validate_PickupDateType(self.PickupDate)
        self.PickupDate_nsprefix_ = None
        self.ReadyByTime = ReadyByTime
        self.validate_ReadyByTimeType(self.ReadyByTime)
        self.ReadyByTime_nsprefix_ = None
        self.ClosingTime = ClosingTime
        self.validate_ClosingTimeType(self.ClosingTime)
        self.ClosingTime_nsprefix_ = None
        self.Remark = Remark
        self.Remark_nsprefix_ = None
        self.PickupLocation = PickupLocation
        self.PickupLocation_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PickupDetailsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PickupDetailsType.subclass:
            return PickupDetailsType.subclass(*args_, **kwargs_)
        else:
            return PickupDetailsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_PickupDate(self):
        return self.PickupDate
    def set_PickupDate(self, PickupDate):
        self.PickupDate = PickupDate
    def get_ReadyByTime(self):
        return self.ReadyByTime
    def set_ReadyByTime(self, ReadyByTime):
        self.ReadyByTime = ReadyByTime
    def get_ClosingTime(self):
        return self.ClosingTime
    def set_ClosingTime(self, ClosingTime):
        self.ClosingTime = ClosingTime
    def get_Remark(self):
        return self.Remark
    def set_Remark(self, Remark):
        self.Remark = Remark
    def get_PickupLocation(self):
        return self.PickupLocation
    def set_PickupLocation(self, PickupLocation):
        self.PickupLocation = PickupLocation
    def validate_PickupDateType(self, value):
        result = True
        # Validate type PickupDateType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on PickupDateType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on PickupDateType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ReadyByTimeType(self, value):
        result = True
        # Validate type ReadyByTimeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ReadyByTimeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on ReadyByTimeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ClosingTimeType(self, value):
        result = True
        # Validate type ClosingTimeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ClosingTimeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on ClosingTimeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.PickupDate is not None or
            self.ReadyByTime is not None or
            self.ClosingTime is not None or
            self.Remark is not None or
            self.PickupLocation is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupDetailsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PickupDetailsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PickupDetailsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PickupDetailsType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PickupDetailsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PickupDetailsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupDetailsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PickupDate is not None:
            namespaceprefix_ = self.PickupDate_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupDate>%s</%sPickupDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupDate), input_name='PickupDate')), namespaceprefix_ , eol_))
        if self.ReadyByTime is not None:
            namespaceprefix_ = self.ReadyByTime_nsprefix_ + ':' if (UseCapturedNS_ and self.ReadyByTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReadyByTime>%s</%sReadyByTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ReadyByTime), input_name='ReadyByTime')), namespaceprefix_ , eol_))
        if self.ClosingTime is not None:
            namespaceprefix_ = self.ClosingTime_nsprefix_ + ':' if (UseCapturedNS_ and self.ClosingTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sClosingTime>%s</%sClosingTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ClosingTime), input_name='ClosingTime')), namespaceprefix_ , eol_))
        if self.Remark is not None:
            namespaceprefix_ = self.Remark_nsprefix_ + ':' if (UseCapturedNS_ and self.Remark_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRemark>%s</%sRemark>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Remark), input_name='Remark')), namespaceprefix_ , eol_))
        if self.PickupLocation is not None:
            namespaceprefix_ = self.PickupLocation_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupLocation_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupLocation>%s</%sPickupLocation>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupLocation), input_name='PickupLocation')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
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
            # validate type PickupDateType
            self.validate_PickupDateType(self.PickupDate)
        elif nodeName_ == 'ReadyByTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ReadyByTime')
            value_ = self.gds_validate_string(value_, node, 'ReadyByTime')
            self.ReadyByTime = value_
            self.ReadyByTime_nsprefix_ = child_.prefix
            # validate type ReadyByTimeType
            self.validate_ReadyByTimeType(self.ReadyByTime)
        elif nodeName_ == 'ClosingTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ClosingTime')
            value_ = self.gds_validate_string(value_, node, 'ClosingTime')
            self.ClosingTime = value_
            self.ClosingTime_nsprefix_ = child_.prefix
            # validate type ClosingTimeType
            self.validate_ClosingTimeType(self.ClosingTime)
        elif nodeName_ == 'Remark':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Remark')
            value_ = self.gds_validate_string(value_, node, 'Remark')
            self.Remark = value_
            self.Remark_nsprefix_ = child_.prefix
        elif nodeName_ == 'PickupLocation':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupLocation')
            value_ = self.gds_validate_string(value_, node, 'PickupLocation')
            self.PickupLocation = value_
            self.PickupLocation_nsprefix_ = child_.prefix
# end class PickupDetailsType


class PickupAddressType1(GeneratedsSuper):
    """PickupAddressType1 --  The pickup address. In the PickupType the following data fields are
    processed/mandatory/optional:
    ----------------------------------------------------------------------------------------------
    Company Name 1 (mandatory): cis:NameType-
    >
    Company-
    >
    name1 Contact Name
    (mandatory): cis:CommunicationType-
    >
    contactPerson Street Name (mandatory):
    cis:NativeAddressType-
    >
    streetName Street Number (mandatory):
    cis:NativeAddressType-
    >
    streetNumber Add. Address (optional) :
    cis:NativeAddressType-
    >
    careOfName Postcode (mandatory):
    cis:NativeAddressType-
    >
    zip City Name (mandatory): cis:NativeAddressType-
    >
    city
    ISO Country Code (mandatory):
    cis:NativeAddressType-
    >
    Origin-
    >
    CountryType-
    >
    countryISOType Phone Number
    (mandatory): cis:CommunicationType-
    >
    phone Email Address (mandatory):
    cis:CommunicationType-
    >
    email
    Company -- Determines whether pickup address is one of the following types.
    Address -- Data fields for pickup address.
    Communication -- Info about communication.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Company=None, Address=None, Communication=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Company = Company
        self.Company_nsprefix_ = None
        self.Address = Address
        self.Address_nsprefix_ = None
        self.Communication = Communication
        self.Communication_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PickupAddressType1)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PickupAddressType1.subclass:
            return PickupAddressType1.subclass(*args_, **kwargs_)
        else:
            return PickupAddressType1(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Company(self):
        return self.Company
    def set_Company(self, Company):
        self.Company = Company
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_Communication(self):
        return self.Communication
    def set_Communication(self, Communication):
        self.Communication = Communication
    def _hasContent(self):
        if (
            self.Company is not None or
            self.Address is not None or
            self.Communication is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupAddressType1', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PickupAddressType1')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PickupAddressType1':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PickupAddressType1')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PickupAddressType1', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PickupAddressType1'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupAddressType1', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Company is not None:
            namespaceprefix_ = self.Company_nsprefix_ + ':' if (UseCapturedNS_ and self.Company_nsprefix_) else ''
            self.Company.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Company', pretty_print=pretty_print)
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.Communication is not None:
            namespaceprefix_ = self.Communication_nsprefix_ + ':' if (UseCapturedNS_ and self.Communication_nsprefix_) else ''
            self.Communication.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Communication', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Company':
            obj_ = NameType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Company = obj_
            obj_.original_tagname_ = 'Company'
        elif nodeName_ == 'Address':
            obj_ = NativeAddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'Communication':
            obj_ = CommunicationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Communication = obj_
            obj_.original_tagname_ = 'Communication'
# end class PickupAddressType1


class PickupOrdererType(GeneratedsSuper):
    """PickupOrdererType --  Information about the pickup orderer. In the PickupOrdererType the
    following data fields are processed/mandatory/optional:
    ----------------------------------------------------------------------------------------------
    Salutation (optional) : cis:NameType-
    >
    Person-
    >
    salutation Company Name 1
    (mandatory): cis:NameType-
    >
    Company-
    >
    name1 Company Name 2 (optional) :
    cis:NameType-
    >
    Company-
    >
    name2 Contact Name (mandatory):
    cis:CommunicationType-
    >
    contactPerson Street Name (mandatory):
    cis:NativeAddressType-
    >
    streetName Street Number (mandatory):
    cis:NativeAddressType-
    >
    streetNumber Add. Address (optional) :
    cis:NativeAddressType-
    >
    careOfName Postcode (mandatory):
    cis:NativeAddressType-
    >
    zip City Name (mandatory): cis:NativeAddressType-
    >
    city
    ISO Country Code (mandatory):
    cis:NativeAddressType-
    >
    Origin-
    >
    CountryType-
    >
    countryISOType Phone Number
    (mandatory): cis:CommunicationType-
    >
    phone Email Address (mandatory):
    cis:CommunicationType-
    >
    email
    Company -- Determines whether orderer contact address is of the following
    type.
    Name3 -- Optional name appendix.
    Address -- Data fields for orderer's address.
    Communication -- Info about communication.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Company=None, Name3=None, Address=None, Communication=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Company = Company
        self.Company_nsprefix_ = None
        self.Name3 = Name3
        self.Name3_nsprefix_ = None
        self.Address = Address
        self.Address_nsprefix_ = None
        self.Communication = Communication
        self.Communication_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PickupOrdererType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PickupOrdererType.subclass:
            return PickupOrdererType.subclass(*args_, **kwargs_)
        else:
            return PickupOrdererType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Company(self):
        return self.Company
    def set_Company(self, Company):
        self.Company = Company
    def get_Name3(self):
        return self.Name3
    def set_Name3(self, Name3):
        self.Name3 = Name3
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_Communication(self):
        return self.Communication
    def set_Communication(self, Communication):
        self.Communication = Communication
    def _hasContent(self):
        if (
            self.Company is not None or
            self.Name3 is not None or
            self.Address is not None or
            self.Communication is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupOrdererType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PickupOrdererType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PickupOrdererType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PickupOrdererType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PickupOrdererType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PickupOrdererType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupOrdererType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Company is not None:
            namespaceprefix_ = self.Company_nsprefix_ + ':' if (UseCapturedNS_ and self.Company_nsprefix_) else ''
            self.Company.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Company', pretty_print=pretty_print)
        if self.Name3 is not None:
            namespaceprefix_ = self.Name3_nsprefix_ + ':' if (UseCapturedNS_ and self.Name3_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName3>%s</%sName3>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name3), input_name='Name3')), namespaceprefix_ , eol_))
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.Communication is not None:
            namespaceprefix_ = self.Communication_nsprefix_ + ':' if (UseCapturedNS_ and self.Communication_nsprefix_) else ''
            self.Communication.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Communication', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Company':
            obj_ = NameType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Company = obj_
            obj_.original_tagname_ = 'Company'
        elif nodeName_ == 'Name3':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Name3')
            value_ = self.gds_validate_string(value_, node, 'Name3')
            self.Name3 = value_
            self.Name3_nsprefix_ = child_.prefix
        elif nodeName_ == 'Address':
            obj_ = NativeAddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'Communication':
            obj_ = CommunicationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Communication = obj_
            obj_.original_tagname_ = 'Communication'
# end class PickupOrdererType


class PickupBookingInformationType(GeneratedsSuper):
    """PickupBookingInformationType -- The data of the pickup order.
    Account -- Depending on whether a DD pickup or TD pickup is invoked, this
    field contains either the 10-digit EKP number (DD pickups) or the 9-digit
    accountNumberExpress (TD pickups).
    PickupDate -- Pickup date in format yyyy-mm-dd.
    ReadyByTime -- Earliest time for pickup. Format is hh:mm.
    ClosingTime -- Lates time for pickup. Format is hh:mm.
    Remark -- Remarks to be considered when pickup is done. Mandatory if 'TDI'
    is selected.
    PickupLocation -- Area to further detail pickup location beyond address. Mandatory
    for TDN and TDI, optional for DDN and DDI.
    AmountOfPieces -- Number of pieces to be picked up.
    AmountOfPallets -- Number of pallets to be picked up.
    WeightInKG -- The weight of all shipment's pieces in kg. Field length must be
    less than or equal to 22.
    CountOfShipments -- Number of shipments to be picked up.
    TotalVolumeWeight -- The total volumetric weight of all pieces in kg. Calculated by
    piece = length x width x height in centimetres / 5000. Field length must be
    less than or equal to 22.
    MaxLengthInCM -- The maximum length in cm.
    MaxWidthInCM -- The maximum width in cm.
    MaxHeightInCM -- The maximum height in cm.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Account=None, PickupDate=None, ReadyByTime=None, ClosingTime=None, Remark=None, PickupLocation=None, AmountOfPieces=None, AmountOfPallets=None, WeightInKG=None, CountOfShipments=None, TotalVolumeWeight=None, MaxLengthInCM=None, MaxWidthInCM=None, MaxHeightInCM=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Account = Account
        self.validate_AccountType(self.Account)
        self.Account_nsprefix_ = None
        self.PickupDate = PickupDate
        self.validate_PickupDateType48(self.PickupDate)
        self.PickupDate_nsprefix_ = None
        self.ReadyByTime = ReadyByTime
        self.validate_ReadyByTimeType49(self.ReadyByTime)
        self.ReadyByTime_nsprefix_ = None
        self.ClosingTime = ClosingTime
        self.validate_ClosingTimeType50(self.ClosingTime)
        self.ClosingTime_nsprefix_ = None
        self.Remark = Remark
        self.Remark_nsprefix_ = None
        self.PickupLocation = PickupLocation
        self.PickupLocation_nsprefix_ = None
        self.AmountOfPieces = AmountOfPieces
        self.validate_AmountOfPiecesType(self.AmountOfPieces)
        self.AmountOfPieces_nsprefix_ = None
        self.AmountOfPallets = AmountOfPallets
        self.validate_AmountOfPalletsType(self.AmountOfPallets)
        self.AmountOfPallets_nsprefix_ = None
        self.WeightInKG = WeightInKG
        self.validate_WeightInKGType(self.WeightInKG)
        self.WeightInKG_nsprefix_ = None
        self.CountOfShipments = CountOfShipments
        self.validate_CountOfShipmentsType(self.CountOfShipments)
        self.CountOfShipments_nsprefix_ = None
        self.TotalVolumeWeight = TotalVolumeWeight
        self.validate_TotalVolumeWeightType(self.TotalVolumeWeight)
        self.TotalVolumeWeight_nsprefix_ = None
        self.MaxLengthInCM = MaxLengthInCM
        self.validate_MaxLengthInCMType(self.MaxLengthInCM)
        self.MaxLengthInCM_nsprefix_ = None
        self.MaxWidthInCM = MaxWidthInCM
        self.validate_MaxWidthInCMType(self.MaxWidthInCM)
        self.MaxWidthInCM_nsprefix_ = None
        self.MaxHeightInCM = MaxHeightInCM
        self.validate_MaxHeightInCMType(self.MaxHeightInCM)
        self.MaxHeightInCM_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PickupBookingInformationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PickupBookingInformationType.subclass:
            return PickupBookingInformationType.subclass(*args_, **kwargs_)
        else:
            return PickupBookingInformationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Account(self):
        return self.Account
    def set_Account(self, Account):
        self.Account = Account
    def get_PickupDate(self):
        return self.PickupDate
    def set_PickupDate(self, PickupDate):
        self.PickupDate = PickupDate
    def get_ReadyByTime(self):
        return self.ReadyByTime
    def set_ReadyByTime(self, ReadyByTime):
        self.ReadyByTime = ReadyByTime
    def get_ClosingTime(self):
        return self.ClosingTime
    def set_ClosingTime(self, ClosingTime):
        self.ClosingTime = ClosingTime
    def get_Remark(self):
        return self.Remark
    def set_Remark(self, Remark):
        self.Remark = Remark
    def get_PickupLocation(self):
        return self.PickupLocation
    def set_PickupLocation(self, PickupLocation):
        self.PickupLocation = PickupLocation
    def get_AmountOfPieces(self):
        return self.AmountOfPieces
    def set_AmountOfPieces(self, AmountOfPieces):
        self.AmountOfPieces = AmountOfPieces
    def get_AmountOfPallets(self):
        return self.AmountOfPallets
    def set_AmountOfPallets(self, AmountOfPallets):
        self.AmountOfPallets = AmountOfPallets
    def get_WeightInKG(self):
        return self.WeightInKG
    def set_WeightInKG(self, WeightInKG):
        self.WeightInKG = WeightInKG
    def get_CountOfShipments(self):
        return self.CountOfShipments
    def set_CountOfShipments(self, CountOfShipments):
        self.CountOfShipments = CountOfShipments
    def get_TotalVolumeWeight(self):
        return self.TotalVolumeWeight
    def set_TotalVolumeWeight(self, TotalVolumeWeight):
        self.TotalVolumeWeight = TotalVolumeWeight
    def get_MaxLengthInCM(self):
        return self.MaxLengthInCM
    def set_MaxLengthInCM(self, MaxLengthInCM):
        self.MaxLengthInCM = MaxLengthInCM
    def get_MaxWidthInCM(self):
        return self.MaxWidthInCM
    def set_MaxWidthInCM(self, MaxWidthInCM):
        self.MaxWidthInCM = MaxWidthInCM
    def get_MaxHeightInCM(self):
        return self.MaxHeightInCM
    def set_MaxHeightInCM(self, MaxHeightInCM):
        self.MaxHeightInCM = MaxHeightInCM
    def validate_AccountType(self, value):
        result = True
        # Validate type AccountType, a restriction on string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 14:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on AccountType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_PickupDateType48(self, value):
        result = True
        # Validate type PickupDateType48, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on PickupDateType48' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on PickupDateType48' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ReadyByTimeType49(self, value):
        result = True
        # Validate type ReadyByTimeType49, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ReadyByTimeType49' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on ReadyByTimeType49' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ClosingTimeType50(self, value):
        result = True
        # Validate type ClosingTimeType50, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ClosingTimeType50' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on ClosingTimeType50' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_AmountOfPiecesType(self, value):
        result = True
        # Validate type AmountOfPiecesType, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on AmountOfPiecesType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_AmountOfPalletsType(self, value):
        result = True
        # Validate type AmountOfPalletsType, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on AmountOfPalletsType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_WeightInKGType(self, value):
        result = True
        # Validate type WeightInKGType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if value < 0.0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on WeightInKGType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999999.99:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on WeightInKGType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_CountOfShipmentsType(self, value):
        result = True
        # Validate type CountOfShipmentsType, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if value < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on CountOfShipmentsType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_TotalVolumeWeightType(self, value):
        result = True
        # Validate type TotalVolumeWeightType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if value < 0.0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on TotalVolumeWeightType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999999.99:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on TotalVolumeWeightType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_MaxLengthInCMType(self, value):
        result = True
        # Validate type MaxLengthInCMType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if value < 0.0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on MaxLengthInCMType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999999.99:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on MaxLengthInCMType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_MaxWidthInCMType(self, value):
        result = True
        # Validate type MaxWidthInCMType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if value < 0.0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on MaxWidthInCMType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999999.99:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on MaxWidthInCMType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_MaxHeightInCMType(self, value):
        result = True
        # Validate type MaxHeightInCMType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if value < 0.0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on MaxHeightInCMType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 9999999.99:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on MaxHeightInCMType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.Account is not None or
            self.PickupDate is not None or
            self.ReadyByTime is not None or
            self.ClosingTime is not None or
            self.Remark is not None or
            self.PickupLocation is not None or
            self.AmountOfPieces is not None or
            self.AmountOfPallets is not None or
            self.WeightInKG is not None or
            self.CountOfShipments is not None or
            self.TotalVolumeWeight is not None or
            self.MaxLengthInCM is not None or
            self.MaxWidthInCM is not None or
            self.MaxHeightInCM is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupBookingInformationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PickupBookingInformationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PickupBookingInformationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PickupBookingInformationType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PickupBookingInformationType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PickupBookingInformationType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PickupBookingInformationType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Account is not None:
            namespaceprefix_ = self.Account_nsprefix_ + ':' if (UseCapturedNS_ and self.Account_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAccount>%s</%sAccount>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Account), input_name='Account')), namespaceprefix_ , eol_))
        if self.PickupDate is not None:
            namespaceprefix_ = self.PickupDate_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupDate>%s</%sPickupDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupDate), input_name='PickupDate')), namespaceprefix_ , eol_))
        if self.ReadyByTime is not None:
            namespaceprefix_ = self.ReadyByTime_nsprefix_ + ':' if (UseCapturedNS_ and self.ReadyByTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReadyByTime>%s</%sReadyByTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ReadyByTime), input_name='ReadyByTime')), namespaceprefix_ , eol_))
        if self.ClosingTime is not None:
            namespaceprefix_ = self.ClosingTime_nsprefix_ + ':' if (UseCapturedNS_ and self.ClosingTime_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sClosingTime>%s</%sClosingTime>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ClosingTime), input_name='ClosingTime')), namespaceprefix_ , eol_))
        if self.Remark is not None:
            namespaceprefix_ = self.Remark_nsprefix_ + ':' if (UseCapturedNS_ and self.Remark_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sRemark>%s</%sRemark>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Remark), input_name='Remark')), namespaceprefix_ , eol_))
        if self.PickupLocation is not None:
            namespaceprefix_ = self.PickupLocation_nsprefix_ + ':' if (UseCapturedNS_ and self.PickupLocation_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPickupLocation>%s</%sPickupLocation>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PickupLocation), input_name='PickupLocation')), namespaceprefix_ , eol_))
        if self.AmountOfPieces is not None:
            namespaceprefix_ = self.AmountOfPieces_nsprefix_ + ':' if (UseCapturedNS_ and self.AmountOfPieces_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAmountOfPieces>%s</%sAmountOfPieces>%s' % (namespaceprefix_ , self.gds_format_integer(self.AmountOfPieces, input_name='AmountOfPieces'), namespaceprefix_ , eol_))
        if self.AmountOfPallets is not None:
            namespaceprefix_ = self.AmountOfPallets_nsprefix_ + ':' if (UseCapturedNS_ and self.AmountOfPallets_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAmountOfPallets>%s</%sAmountOfPallets>%s' % (namespaceprefix_ , self.gds_format_integer(self.AmountOfPallets, input_name='AmountOfPallets'), namespaceprefix_ , eol_))
        if self.WeightInKG is not None:
            namespaceprefix_ = self.WeightInKG_nsprefix_ + ':' if (UseCapturedNS_ and self.WeightInKG_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sWeightInKG>%s</%sWeightInKG>%s' % (namespaceprefix_ , self.gds_format_decimal(self.WeightInKG, input_name='WeightInKG'), namespaceprefix_ , eol_))
        if self.CountOfShipments is not None:
            namespaceprefix_ = self.CountOfShipments_nsprefix_ + ':' if (UseCapturedNS_ and self.CountOfShipments_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountOfShipments>%s</%sCountOfShipments>%s' % (namespaceprefix_ , self.gds_format_integer(self.CountOfShipments, input_name='CountOfShipments'), namespaceprefix_ , eol_))
        if self.TotalVolumeWeight is not None:
            namespaceprefix_ = self.TotalVolumeWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.TotalVolumeWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTotalVolumeWeight>%s</%sTotalVolumeWeight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.TotalVolumeWeight, input_name='TotalVolumeWeight'), namespaceprefix_ , eol_))
        if self.MaxLengthInCM is not None:
            namespaceprefix_ = self.MaxLengthInCM_nsprefix_ + ':' if (UseCapturedNS_ and self.MaxLengthInCM_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMaxLengthInCM>%s</%sMaxLengthInCM>%s' % (namespaceprefix_ , self.gds_format_decimal(self.MaxLengthInCM, input_name='MaxLengthInCM'), namespaceprefix_ , eol_))
        if self.MaxWidthInCM is not None:
            namespaceprefix_ = self.MaxWidthInCM_nsprefix_ + ':' if (UseCapturedNS_ and self.MaxWidthInCM_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMaxWidthInCM>%s</%sMaxWidthInCM>%s' % (namespaceprefix_ , self.gds_format_decimal(self.MaxWidthInCM, input_name='MaxWidthInCM'), namespaceprefix_ , eol_))
        if self.MaxHeightInCM is not None:
            namespaceprefix_ = self.MaxHeightInCM_nsprefix_ + ':' if (UseCapturedNS_ and self.MaxHeightInCM_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sMaxHeightInCM>%s</%sMaxHeightInCM>%s' % (namespaceprefix_ , self.gds_format_decimal(self.MaxHeightInCM, input_name='MaxHeightInCM'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Account':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Account')
            value_ = self.gds_validate_string(value_, node, 'Account')
            self.Account = value_
            self.Account_nsprefix_ = child_.prefix
            # validate type AccountType
            self.validate_AccountType(self.Account)
        elif nodeName_ == 'PickupDate':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupDate')
            value_ = self.gds_validate_string(value_, node, 'PickupDate')
            self.PickupDate = value_
            self.PickupDate_nsprefix_ = child_.prefix
            # validate type PickupDateType48
            self.validate_PickupDateType48(self.PickupDate)
        elif nodeName_ == 'ReadyByTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ReadyByTime')
            value_ = self.gds_validate_string(value_, node, 'ReadyByTime')
            self.ReadyByTime = value_
            self.ReadyByTime_nsprefix_ = child_.prefix
            # validate type ReadyByTimeType49
            self.validate_ReadyByTimeType49(self.ReadyByTime)
        elif nodeName_ == 'ClosingTime':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ClosingTime')
            value_ = self.gds_validate_string(value_, node, 'ClosingTime')
            self.ClosingTime = value_
            self.ClosingTime_nsprefix_ = child_.prefix
            # validate type ClosingTimeType50
            self.validate_ClosingTimeType50(self.ClosingTime)
        elif nodeName_ == 'Remark':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Remark')
            value_ = self.gds_validate_string(value_, node, 'Remark')
            self.Remark = value_
            self.Remark_nsprefix_ = child_.prefix
        elif nodeName_ == 'PickupLocation':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PickupLocation')
            value_ = self.gds_validate_string(value_, node, 'PickupLocation')
            self.PickupLocation = value_
            self.PickupLocation_nsprefix_ = child_.prefix
        elif nodeName_ == 'AmountOfPieces' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'AmountOfPieces')
            ival_ = self.gds_validate_integer(ival_, node, 'AmountOfPieces')
            self.AmountOfPieces = ival_
            self.AmountOfPieces_nsprefix_ = child_.prefix
            # validate type AmountOfPiecesType
            self.validate_AmountOfPiecesType(self.AmountOfPieces)
        elif nodeName_ == 'AmountOfPallets' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'AmountOfPallets')
            ival_ = self.gds_validate_integer(ival_, node, 'AmountOfPallets')
            self.AmountOfPallets = ival_
            self.AmountOfPallets_nsprefix_ = child_.prefix
            # validate type AmountOfPalletsType
            self.validate_AmountOfPalletsType(self.AmountOfPallets)
        elif nodeName_ == 'WeightInKG' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'WeightInKG')
            fval_ = self.gds_validate_decimal(fval_, node, 'WeightInKG')
            self.WeightInKG = fval_
            self.WeightInKG_nsprefix_ = child_.prefix
            # validate type WeightInKGType
            self.validate_WeightInKGType(self.WeightInKG)
        elif nodeName_ == 'CountOfShipments' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'CountOfShipments')
            ival_ = self.gds_validate_integer(ival_, node, 'CountOfShipments')
            self.CountOfShipments = ival_
            self.CountOfShipments_nsprefix_ = child_.prefix
            # validate type CountOfShipmentsType
            self.validate_CountOfShipmentsType(self.CountOfShipments)
        elif nodeName_ == 'TotalVolumeWeight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'TotalVolumeWeight')
            fval_ = self.gds_validate_decimal(fval_, node, 'TotalVolumeWeight')
            self.TotalVolumeWeight = fval_
            self.TotalVolumeWeight_nsprefix_ = child_.prefix
            # validate type TotalVolumeWeightType
            self.validate_TotalVolumeWeightType(self.TotalVolumeWeight)
        elif nodeName_ == 'MaxLengthInCM' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'MaxLengthInCM')
            fval_ = self.gds_validate_decimal(fval_, node, 'MaxLengthInCM')
            self.MaxLengthInCM = fval_
            self.MaxLengthInCM_nsprefix_ = child_.prefix
            # validate type MaxLengthInCMType
            self.validate_MaxLengthInCMType(self.MaxLengthInCM)
        elif nodeName_ == 'MaxWidthInCM' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'MaxWidthInCM')
            fval_ = self.gds_validate_decimal(fval_, node, 'MaxWidthInCM')
            self.MaxWidthInCM = fval_
            self.MaxWidthInCM_nsprefix_ = child_.prefix
            # validate type MaxWidthInCMType
            self.validate_MaxWidthInCMType(self.MaxWidthInCM)
        elif nodeName_ == 'MaxHeightInCM' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'MaxHeightInCM')
            fval_ = self.gds_validate_decimal(fval_, node, 'MaxHeightInCM')
            self.MaxHeightInCM = fval_
            self.MaxHeightInCM_nsprefix_ = child_.prefix
            # validate type MaxHeightInCMType
            self.validate_MaxHeightInCMType(self.MaxHeightInCM)
# end class PickupBookingInformationType


class CancelPickupRequest(GeneratedsSuper):
    """CancelPickupRequest -- The data for cancelling a pickup order.
    Version -- The version of the webservice implementation for which the
    requesting client is developed.
    BookingConfirmationNumber -- The confirmation number of the pickup order which should be
    cancelled. Use value from pickup response attribute 'ConfirmationNumber'
    to cancel respective pickup order. Note: only one pickup can be deleted
    at a time.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, BookingConfirmationNumber=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        self.BookingConfirmationNumber = BookingConfirmationNumber
        self.BookingConfirmationNumber_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CancelPickupRequest)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CancelPickupRequest.subclass:
            return CancelPickupRequest.subclass(*args_, **kwargs_)
        else:
            return CancelPickupRequest(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_BookingConfirmationNumber(self):
        return self.BookingConfirmationNumber
    def set_BookingConfirmationNumber(self, BookingConfirmationNumber):
        self.BookingConfirmationNumber = BookingConfirmationNumber
    def _hasContent(self):
        if (
            self.Version is not None or
            self.BookingConfirmationNumber is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CancelPickupRequest', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CancelPickupRequest')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CancelPickupRequest':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CancelPickupRequest')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CancelPickupRequest', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CancelPickupRequest'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CancelPickupRequest', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.BookingConfirmationNumber is not None:
            namespaceprefix_ = self.BookingConfirmationNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.BookingConfirmationNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBookingConfirmationNumber>%s</%sBookingConfirmationNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BookingConfirmationNumber), input_name='BookingConfirmationNumber')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'BookingConfirmationNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BookingConfirmationNumber')
            value_ = self.gds_validate_string(value_, node, 'BookingConfirmationNumber')
            self.BookingConfirmationNumber = value_
            self.BookingConfirmationNumber_nsprefix_ = child_.prefix
# end class CancelPickupRequest


class CancelPickupResponse(GeneratedsSuper):
    """CancelPickupResponse -- The status of the cancel pickup operation.
    Version -- The version of the webservice implementation.
    Status -- Success status after processing the request.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, Status=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        self.Status = Status
        self.Status_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CancelPickupResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CancelPickupResponse.subclass:
            return CancelPickupResponse.subclass(*args_, **kwargs_)
        else:
            return CancelPickupResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_Status(self):
        return self.Status
    def set_Status(self, Status):
        self.Status = Status
    def _hasContent(self):
        if (
            self.Version is not None or
            self.Status is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CancelPickupResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CancelPickupResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CancelPickupResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CancelPickupResponse')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CancelPickupResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CancelPickupResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CancelPickupResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.Status is not None:
            namespaceprefix_ = self.Status_nsprefix_ + ':' if (UseCapturedNS_ and self.Status_nsprefix_) else ''
            self.Status.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Status', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'Status':
            obj_ = Statusinformation.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Status = obj_
            obj_.original_tagname_ = 'Status'
# end class CancelPickupResponse


class IdentityData(GeneratedsSuper):
    """IdentityData -- Identity data (used e.g. for ident services)
    DrivingLicense -- If driving license shall be used for verifying identity.
    IdentityCard -- If identity card shall be used for verifying identity.
    BankCard -- If a bank card shall be used for verifying identity.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, DrivingLicense=None, IdentityCard=None, BankCard=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.DrivingLicense = DrivingLicense
        self.DrivingLicense_nsprefix_ = None
        self.IdentityCard = IdentityCard
        self.IdentityCard_nsprefix_ = None
        self.BankCard = BankCard
        self.BankCard_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, IdentityData)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if IdentityData.subclass:
            return IdentityData.subclass(*args_, **kwargs_)
        else:
            return IdentityData(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_DrivingLicense(self):
        return self.DrivingLicense
    def set_DrivingLicense(self, DrivingLicense):
        self.DrivingLicense = DrivingLicense
    def get_IdentityCard(self):
        return self.IdentityCard
    def set_IdentityCard(self, IdentityCard):
        self.IdentityCard = IdentityCard
    def get_BankCard(self):
        return self.BankCard
    def set_BankCard(self, BankCard):
        self.BankCard = BankCard
    def _hasContent(self):
        if (
            self.DrivingLicense is not None or
            self.IdentityCard is not None or
            self.BankCard is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='IdentityData', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('IdentityData')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'IdentityData':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='IdentityData')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='IdentityData', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='IdentityData'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='IdentityData', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DrivingLicense is not None:
            namespaceprefix_ = self.DrivingLicense_nsprefix_ + ':' if (UseCapturedNS_ and self.DrivingLicense_nsprefix_) else ''
            self.DrivingLicense.export(outfile, level, namespaceprefix_, namespacedef_='', name_='DrivingLicense', pretty_print=pretty_print)
        if self.IdentityCard is not None:
            namespaceprefix_ = self.IdentityCard_nsprefix_ + ':' if (UseCapturedNS_ and self.IdentityCard_nsprefix_) else ''
            self.IdentityCard.export(outfile, level, namespaceprefix_, namespacedef_='', name_='IdentityCard', pretty_print=pretty_print)
        if self.BankCard is not None:
            namespaceprefix_ = self.BankCard_nsprefix_ + ':' if (UseCapturedNS_ and self.BankCard_nsprefix_) else ''
            self.BankCard.export(outfile, level, namespaceprefix_, namespacedef_='', name_='BankCard', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DrivingLicense':
            obj_ = DrivingLicenseType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DrivingLicense = obj_
            obj_.original_tagname_ = 'DrivingLicense'
        elif nodeName_ == 'IdentityCard':
            obj_ = IdentityCardType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.IdentityCard = obj_
            obj_.original_tagname_ = 'IdentityCard'
        elif nodeName_ == 'BankCard':
            obj_ = BankCardType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BankCard = obj_
            obj_.original_tagname_ = 'BankCard'
# end class IdentityData


class ReadShipmentOrderResponse(GeneratedsSuper):
    """ReadShipmentOrderResponse -- The status of the operation and the shipment identifier (if available).
    Version -- The version of the webservice implementation.
    status -- Success status after processing the overall request.
    CreationState -- The operation's success status for every single ShipmentOrder
    will be returned by one CreationState element. It is identifiable via
    SequenceNumber.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Version=None, status=None, CreationState=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Version = Version
        self.Version_nsprefix_ = None
        self.status = status
        self.status_nsprefix_ = None
        if CreationState is None:
            self.CreationState = []
        else:
            self.CreationState = CreationState
        self.CreationState_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ReadShipmentOrderResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ReadShipmentOrderResponse.subclass:
            return ReadShipmentOrderResponse.subclass(*args_, **kwargs_)
        else:
            return ReadShipmentOrderResponse(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Version(self):
        return self.Version
    def set_Version(self, Version):
        self.Version = Version
    def get_status(self):
        return self.status
    def set_status(self, status):
        self.status = status
    def get_CreationState(self):
        return self.CreationState
    def set_CreationState(self, CreationState):
        self.CreationState = CreationState
    def add_CreationState(self, value):
        self.CreationState.append(value)
    def insert_CreationState_at(self, index, value):
        self.CreationState.insert(index, value)
    def replace_CreationState_at(self, index, value):
        self.CreationState[index] = value
    def _hasContent(self):
        if (
            self.Version is not None or
            self.status is not None or
            self.CreationState
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReadShipmentOrderResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ReadShipmentOrderResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ReadShipmentOrderResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ReadShipmentOrderResponse')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ReadShipmentOrderResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ReadShipmentOrderResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReadShipmentOrderResponse', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Version is not None:
            namespaceprefix_ = self.Version_nsprefix_ + ':' if (UseCapturedNS_ and self.Version_nsprefix_) else ''
            self.Version.export(outfile, level, namespaceprefix_='bcs:', namespacedef_='', name_='Version', pretty_print=pretty_print)
        if self.status is not None:
            namespaceprefix_ = self.status_nsprefix_ + ':' if (UseCapturedNS_ and self.status_nsprefix_) else ''
            self.status.export(outfile, level, namespaceprefix_, namespacedef_='', name_='status', pretty_print=pretty_print)
        for CreationState_ in self.CreationState:
            namespaceprefix_ = self.CreationState_nsprefix_ + ':' if (UseCapturedNS_ and self.CreationState_nsprefix_) else ''
            CreationState_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='CreationState', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Version':
            obj_ = Version.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Version = obj_
            obj_.original_tagname_ = 'Version'
        elif nodeName_ == 'status':
            obj_ = Statusinformation.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.status = obj_
            obj_.original_tagname_ = 'status'
        elif nodeName_ == 'CreationState':
            obj_ = CreationState.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CreationState.append(obj_)
            obj_.original_tagname_ = 'CreationState'
# end class ReadShipmentOrderResponse


class EKP(GeneratedsSuper):
    """EKP -- First 10 digit number extract from the 14 digit DHL Account Number.
    E.g. if DHL Account Number is "5000000008 72 01" then EKP is equal to 5000000008.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='EKP', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='EKP'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='EKP', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='partnerID', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='partnerID'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='partnerID', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='procedureID', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='procedureID'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='procedureID', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='accountNumber', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='accountNumber'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='accountNumber', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='accountNumberExpress', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='accountNumberExpress'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='accountNumberExpress', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='identCode', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='identCode'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='identCode', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='licensePlate', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='licensePlate'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='licensePlate', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='airwayBill', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='airwayBill'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='airwayBill', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='routeCode', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='routeCode'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='routeCode', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='routingCode', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='routingCode'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='routingCode', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='city', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='city'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='city', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='province', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='province'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='province', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='streetNameCode', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='streetNameCode'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='streetNameCode', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='streetNumberCode', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='streetNumberCode'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='streetNumberCode', fromsubclass_=False, pretty_print=True):
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
        self.validate_majorReleaseType56(self.majorRelease)
        self.majorRelease_nsprefix_ = None
        self.minorRelease = minorRelease
        self.validate_minorReleaseType57(self.minorRelease)
        self.minorRelease_nsprefix_ = None
        self.build_ = build_
        self.validate_buildType58(self.build_)
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
    def validate_majorReleaseType56(self, value):
        result = True
        # Validate type majorReleaseType56, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on majorReleaseType56' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_minorReleaseType57(self, value):
        result = True
        # Validate type minorReleaseType57, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on minorReleaseType57' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_buildType58(self, value):
        result = True
        # Validate type buildType58, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on buildType58' % {"value" : encode_str_2_3(value), "lineno": lineno} )
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='Version', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='Version'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='Version', fromsubclass_=False, pretty_print=True):
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
            # validate type majorReleaseType56
            self.validate_majorReleaseType56(self.majorRelease)
        elif nodeName_ == 'minorRelease':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'minorRelease')
            value_ = self.gds_validate_string(value_, node, 'minorRelease')
            self.minorRelease = value_
            self.minorRelease_nsprefix_ = child_.prefix
            # validate type minorReleaseType57
            self.validate_minorReleaseType57(self.minorRelease)
        elif nodeName_ == 'build':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'build')
            value_ = self.gds_validate_string(value_, node, 'build')
            self.build_ = value_
            self.build_nsprefix_ = child_.prefix
            # validate type buildType58
            self.validate_buildType58(self.build_)
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
            pass
        return result
    def validate_signatureType(self, value):
        result = True
        # Validate type signatureType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='AuthentificationType', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='AuthentificationType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='AuthentificationType', fromsubclass_=False, pretty_print=True):
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
        self.validate_streetNameType59(self.streetName)
        self.streetName_nsprefix_ = None
        self.streetNumber = streetNumber
        self.validate_streetNumberType60(self.streetNumber)
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
    def validate_streetNameType59(self, value):
        result = True
        # Validate type streetNameType59, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetNameType59' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_streetNumberType60(self, value):
        result = True
        # Validate type streetNumberType60, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetNumberType60' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_addressAdditionType(self, value):
        result = True
        # Validate type addressAdditionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on addressAdditionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_dispatchingInformationType(self, value):
        result = True
        # Validate type dispatchingInformationType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='NativeAddressType', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='NativeAddressType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='NativeAddressType', fromsubclass_=False, pretty_print=True):
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
            # validate type streetNameType59
            self.validate_streetNameType59(self.streetName)
        elif nodeName_ == 'streetNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'streetNumber')
            value_ = self.gds_validate_string(value_, node, 'streetNumber')
            self.streetNumber = value_
            self.streetNumber_nsprefix_ = child_.prefix
            # validate type streetNumberType60
            self.validate_streetNumberType60(self.streetNumber)
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
        self.validate_streetNameType61(self.streetName)
        self.streetName_nsprefix_ = None
        self.streetNumber = streetNumber
        self.validate_streetNumberType62(self.streetNumber)
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
    def validate_streetNameType61(self, value):
        result = True
        # Validate type streetNameType61, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetNameType61' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_streetNumberType62(self, value):
        result = True
        # Validate type streetNumberType62, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetNumberType62' % {"value" : encode_str_2_3(value), "lineno": lineno} )
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='NativeAddressTypeNew', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='NativeAddressTypeNew'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='NativeAddressTypeNew', fromsubclass_=False, pretty_print=True):
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
            # validate type streetNameType61
            self.validate_streetNameType61(self.streetName)
        elif nodeName_ == 'streetNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'streetNumber')
            value_ = self.gds_validate_string(value_, node, 'streetNumber')
            self.streetNumber = value_
            self.streetNumber_nsprefix_ = child_.prefix
            # validate type streetNumberType62
            self.validate_streetNumberType62(self.streetNumber)
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
        self.validate_streetNameType63(self.streetName)
        self.streetName_nsprefix_ = None
        self.streetNumber = streetNumber
        self.validate_streetNumberType64(self.streetNumber)
        self.streetNumber_nsprefix_ = None
        if addressAddition is None:
            self.addressAddition = []
        else:
            self.addressAddition = addressAddition
        self.addressAddition_nsprefix_ = None
        self.dispatchingInformation = dispatchingInformation
        self.validate_dispatchingInformationType66(self.dispatchingInformation)
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
    def validate_streetNameType63(self, value):
        result = True
        # Validate type streetNameType63, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetNameType63' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_streetNumberType64(self, value):
        result = True
        # Validate type streetNumberType64, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetNumberType64' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_addressAdditionType65(self, value):
        result = True
        # Validate type addressAdditionType65, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on addressAdditionType65' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_dispatchingInformationType66(self, value):
        result = True
        # Validate type dispatchingInformationType66, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on dispatchingInformationType66' % {"value" : encode_str_2_3(value), "lineno": lineno} )
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='ReceiverNativeAddressType', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='ReceiverNativeAddressType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='ReceiverNativeAddressType', fromsubclass_=False, pretty_print=True):
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
            # validate type streetNameType63
            self.validate_streetNameType63(self.streetName)
        elif nodeName_ == 'streetNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'streetNumber')
            value_ = self.gds_validate_string(value_, node, 'streetNumber')
            self.streetNumber = value_
            self.streetNumber_nsprefix_ = child_.prefix
            # validate type streetNumberType64
            self.validate_streetNumberType64(self.streetNumber)
        elif nodeName_ == 'addressAddition':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'addressAddition')
            value_ = self.gds_validate_string(value_, node, 'addressAddition')
            self.addressAddition.append(value_)
            self.addressAddition_nsprefix_ = child_.prefix
            # validate type addressAdditionType65
            self.validate_addressAdditionType65(self.addressAddition[-1])
        elif nodeName_ == 'dispatchingInformation':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'dispatchingInformation')
            value_ = self.gds_validate_string(value_, node, 'dispatchingInformation')
            self.dispatchingInformation = value_
            self.dispatchingInformation_nsprefix_ = child_.prefix
            # validate type dispatchingInformationType66
            self.validate_dispatchingInformationType66(self.dispatchingInformation)
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='PickupAddressType', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='PickupAddressType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='PickupAddressType', fromsubclass_=False, pretty_print=True):
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='DeliveryAddressType', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='DeliveryAddressType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='DeliveryAddressType', fromsubclass_=False, pretty_print=True):
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
            if len(value) > 80:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on accountOwnerType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_bankNameType(self, value):
        result = True
        # Validate type bankNameType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 80:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on bankNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_ibanType(self, value):
        result = True
        # Validate type ibanType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 22:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ibanType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_note1Type(self, value):
        result = True
        # Validate type note1Type, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on note1Type' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_note2Type(self, value):
        result = True
        # Validate type note2Type, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on note2Type' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_bicType(self, value):
        result = True
        # Validate type bicType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 11:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on bicType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_accountreferenceType(self, value):
        result = True
        # Validate type accountreferenceType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='BankType', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='BankType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='BankType', fromsubclass_=False, pretty_print=True):
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='NameType', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='NameType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='NameType', fromsubclass_=False, pretty_print=True):
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='ReceiverNameType', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='ReceiverNameType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='ReceiverNameType', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='name1', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='name1'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='name1', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='name2', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='name2'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='name2', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='name3', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='name3'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='name3', fromsubclass_=False, pretty_print=True):
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
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on phoneType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_emailType(self, value):
        result = True
        # Validate type emailType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 70:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on emailType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_contactPersonType(self, value):
        result = True
        # Validate type contactPersonType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='CommunicationType', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='CommunicationType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='CommunicationType', fromsubclass_=False, pretty_print=True):
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='ContactType', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='ContactType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='ContactType', fromsubclass_=False, pretty_print=True):
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='PackStationType', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='PackStationType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='PackStationType', fromsubclass_=False, pretty_print=True):
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
        self.validate_postNumberType67(self.postNumber)
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
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on postfilialNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on postfilialNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_postNumberType67(self, value):
        result = True
        # Validate type postNumberType67, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on postNumberType67' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on postNumberType67' % {"value" : encode_str_2_3(value), "lineno": lineno} )
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='PostfilialeType', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='PostfilialeType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='PostfilialeType', fromsubclass_=False, pretty_print=True):
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
            # validate type postNumberType67
            self.validate_postNumberType67(self.postNumber)
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
        self.validate_postfilialNumberType68(self.postfilialNumber)
        self.postfilialNumber_nsprefix_ = None
        self.postNumber = postNumber
        self.validate_postNumberType69(self.postNumber)
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
    def validate_postfilialNumberType68(self, value):
        result = True
        # Validate type postfilialNumberType68, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on postfilialNumberType68' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on postfilialNumberType68' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_postNumberType69(self, value):
        result = True
        # Validate type postNumberType69, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on postNumberType69' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on postNumberType69' % {"value" : encode_str_2_3(value), "lineno": lineno} )
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='PostfilialeTypeNoCountry', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='PostfilialeTypeNoCountry'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='PostfilialeTypeNoCountry', fromsubclass_=False, pretty_print=True):
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
            # validate type postfilialNumberType68
            self.validate_postfilialNumberType68(self.postfilialNumber)
        elif nodeName_ == 'postNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'postNumber')
            value_ = self.gds_validate_string(value_, node, 'postNumber')
            self.postNumber = value_
            self.postNumber_nsprefix_ = child_.prefix
            # validate type postNumberType69
            self.validate_postNumberType69(self.postNumber)
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
        self.validate_streetNameType70(self.streetName)
        self.streetName_nsprefix_ = None
        self.streetNumber = streetNumber
        self.validate_streetNumberType71(self.streetNumber)
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
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on parcelShopNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on parcelShopNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_streetNameType70(self, value):
        result = True
        # Validate type streetNameType70, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetNameType70' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_streetNumberType71(self, value):
        result = True
        # Validate type streetNumberType71, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 5:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on streetNumberType71' % {"value" : encode_str_2_3(value), "lineno": lineno} )
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='ParcelShopType', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='ParcelShopType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='ParcelShopType', fromsubclass_=False, pretty_print=True):
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
            # validate type streetNameType70
            self.validate_streetNameType70(self.streetName)
        elif nodeName_ == 'streetNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'streetNumber')
            value_ = self.gds_validate_string(value_, node, 'streetNumber')
            self.streetNumber = value_
            self.streetNumber_nsprefix_ = child_.prefix
            # validate type streetNumberType71
            self.validate_streetNumberType71(self.streetNumber)
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
        self.vatID_nsprefix_ = "xs"
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='CustomerType', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='CustomerType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='CustomerType', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
        self.priority_nsprefix_ = "xs"
        self.code = code
        self.code_nsprefix_ = "xs"
        if isinstance(dateTime, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(dateTime, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = dateTime
        self.dateTime = initvalue_
        self.dateTime_nsprefix_ = "xs"
        self.description = description
        self.description_nsprefix_ = "xs"
        self.descriptionLong = descriptionLong
        self.descriptionLong_nsprefix_ = "xs"
        self.solution = solution
        self.solution_nsprefix_ = "xs"
        self.application = application
        self.application_nsprefix_ = "xs"
        self.module = module
        self.module_nsprefix_ = "xs"
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='ErrorType', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='ErrorType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='ErrorType', fromsubclass_=False, pretty_print=True):
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
            if len(value) > 30:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on countryType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_countryISOType(self, value):
        result = True
        # Validate type countryISOType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='CountryType', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='CountryType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='CountryType', fromsubclass_=False, pretty_print=True):
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='ShipmentNumberType', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='ShipmentNumberType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='ShipmentNumberType', fromsubclass_=False, pretty_print=True):
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
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on statuscodeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_statusDescriptionType(self, value):
        result = True
        # Validate type statusDescriptionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='Status', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='Status'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='Status', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='productKey', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='productKey'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='productKey', fromsubclass_=False, pretty_print=True):
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
        self.length_nsprefix_ = "xs"
        self.width = width
        self.width_nsprefix_ = "xs"
        self.height = height
        self.height_nsprefix_ = "xs"
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='Dimension', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='Dimension'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='Dimension', fromsubclass_=False, pretty_print=True):
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
        self.from__nsprefix_ = "xs"
        if isinstance(until, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(until, '%H:%M:%S').time()
        else:
            initvalue_ = until
        self.until = initvalue_
        self.until_nsprefix_ = "xs"
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='TimeFrame', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='TimeFrame'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='TimeFrame', fromsubclass_=False, pretty_print=True):
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
    def __init__(self, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.valueOf_ = valueOf_
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
    def export(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='shipmentNumber', pretty_print=True):
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
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='cis:', name_='shipmentNumber'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='cis:', namespacedef_='', name_='shipmentNumber', fromsubclass_=False, pretty_print=True):
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


class ShipmentType(GeneratedsSuper):
    """ShipmentType -- Is the core element of a ShipmentOrder. It contains all relevant
    information of the shipment.
    ShipmentDetails -- Contains the information of the shipment product
    code, weight and size characteristics and services to be used.
    Shipper -- Contains relevant information about the Shipper.
    ShipperReference -- Contains a reference to the Shipper data
    configured in GKP.
    Receiver -- Contains relevant information about Receiver.
    ReturnReceiver -- To be used if a return label address shall be
    generated.
    ExportDocument -- For international shipments. This section contains
    information about the exported goods relevant for customs. For
    international shipments: commercial invoice and customs
    declaration (CN23) have to be attached to the shipment. Data
    relevant for customs also has to be transferred as
    electronically.
    feederSystem -- Is only to be indicated by DHL partners
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ShipmentDetails=None, Shipper=None, ShipperReference=None, Receiver=None, ReturnReceiver=None, ExportDocument=None, feederSystem=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ShipmentDetails = ShipmentDetails
        self.ShipmentDetails_nsprefix_ = None
        self.Shipper = Shipper
        self.Shipper_nsprefix_ = None
        self.ShipperReference = ShipperReference
        self.validate_ShipperReferenceType(self.ShipperReference)
        self.ShipperReference_nsprefix_ = None
        self.Receiver = Receiver
        self.Receiver_nsprefix_ = None
        self.ReturnReceiver = ReturnReceiver
        self.ReturnReceiver_nsprefix_ = None
        self.ExportDocument = ExportDocument
        self.ExportDocument_nsprefix_ = None
        self.feederSystem = feederSystem
        self.validate_feederSystemType(self.feederSystem)
        self.feederSystem_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentType.subclass:
            return ShipmentType.subclass(*args_, **kwargs_)
        else:
            return ShipmentType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ShipmentDetails(self):
        return self.ShipmentDetails
    def set_ShipmentDetails(self, ShipmentDetails):
        self.ShipmentDetails = ShipmentDetails
    def get_Shipper(self):
        return self.Shipper
    def set_Shipper(self, Shipper):
        self.Shipper = Shipper
    def get_ShipperReference(self):
        return self.ShipperReference
    def set_ShipperReference(self, ShipperReference):
        self.ShipperReference = ShipperReference
    def get_Receiver(self):
        return self.Receiver
    def set_Receiver(self, Receiver):
        self.Receiver = Receiver
    def get_ReturnReceiver(self):
        return self.ReturnReceiver
    def set_ReturnReceiver(self, ReturnReceiver):
        self.ReturnReceiver = ReturnReceiver
    def get_ExportDocument(self):
        return self.ExportDocument
    def set_ExportDocument(self, ExportDocument):
        self.ExportDocument = ExportDocument
    def get_feederSystem(self):
        return self.feederSystem
    def set_feederSystem(self, feederSystem):
        self.feederSystem = feederSystem
    def validate_ShipperReferenceType(self, value):
        result = True
        # Validate type ShipperReferenceType, a restriction on string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ShipperReferenceType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_feederSystemType(self, value):
        result = True
        # Validate type feederSystemType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def _hasContent(self):
        if (
            self.ShipmentDetails is not None or
            self.Shipper is not None or
            self.ShipperReference is not None or
            self.Receiver is not None or
            self.ReturnReceiver is not None or
            self.ExportDocument is not None or
            self.feederSystem is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ShipmentDetails is not None:
            namespaceprefix_ = self.ShipmentDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentDetails_nsprefix_) else ''
            self.ShipmentDetails.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentDetails', pretty_print=pretty_print)
        if self.Shipper is not None:
            namespaceprefix_ = self.Shipper_nsprefix_ + ':' if (UseCapturedNS_ and self.Shipper_nsprefix_) else ''
            self.Shipper.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Shipper', pretty_print=pretty_print)
        if self.ShipperReference is not None:
            namespaceprefix_ = self.ShipperReference_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipperReference_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sShipperReference>%s</%sShipperReference>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ShipperReference), input_name='ShipperReference')), namespaceprefix_ , eol_))
        if self.Receiver is not None:
            namespaceprefix_ = self.Receiver_nsprefix_ + ':' if (UseCapturedNS_ and self.Receiver_nsprefix_) else ''
            self.Receiver.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Receiver', pretty_print=pretty_print)
        if self.ReturnReceiver is not None:
            namespaceprefix_ = self.ReturnReceiver_nsprefix_ + ':' if (UseCapturedNS_ and self.ReturnReceiver_nsprefix_) else ''
            self.ReturnReceiver.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ReturnReceiver', pretty_print=pretty_print)
        if self.ExportDocument is not None:
            namespaceprefix_ = self.ExportDocument_nsprefix_ + ':' if (UseCapturedNS_ and self.ExportDocument_nsprefix_) else ''
            self.ExportDocument.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ExportDocument', pretty_print=pretty_print)
        if self.feederSystem is not None:
            namespaceprefix_ = self.feederSystem_nsprefix_ + ':' if (UseCapturedNS_ and self.feederSystem_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sfeederSystem>%s</%sfeederSystem>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.feederSystem), input_name='feederSystem')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ShipmentDetails':
            obj_ = ShipmentDetailsTypeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentDetails = obj_
            obj_.original_tagname_ = 'ShipmentDetails'
        elif nodeName_ == 'Shipper':
            obj_ = ShipperType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Shipper = obj_
            obj_.original_tagname_ = 'Shipper'
        elif nodeName_ == 'ShipperReference':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ShipperReference')
            value_ = self.gds_validate_string(value_, node, 'ShipperReference')
            self.ShipperReference = value_
            self.ShipperReference_nsprefix_ = child_.prefix
            # validate type ShipperReferenceType
            self.validate_ShipperReferenceType(self.ShipperReference)
        elif nodeName_ == 'Receiver':
            obj_ = ReceiverType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Receiver = obj_
            obj_.original_tagname_ = 'Receiver'
        elif nodeName_ == 'ReturnReceiver':
            obj_ = ShipperType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ReturnReceiver = obj_
            obj_.original_tagname_ = 'ReturnReceiver'
        elif nodeName_ == 'ExportDocument':
            obj_ = ExportDocumentType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ExportDocument = obj_
            obj_.original_tagname_ = 'ExportDocument'
        elif nodeName_ == 'feederSystem':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'feederSystem')
            value_ = self.gds_validate_string(value_, node, 'feederSystem')
            self.feederSystem = value_
            self.feederSystem_nsprefix_ = child_.prefix
            # validate type feederSystemType
            self.validate_feederSystemType(self.feederSystem)
# end class ShipmentType


class ShipmentType18(GeneratedsSuper):
    """ShipmentType18 -- Is the core element of a ShipmentOrder. It contains all relevant
    information of the shipment.
    ShipmentDetails -- Contains the information of the shipment product
    code, weight and size characteristics and services to be used.
    Shipper -- Contains relevant information about the Shipper.
    Receiver -- Contains relevant information about Receiver.
    ReturnReceiver -- To be used if a return label address shall be
    generated.
    ExportDocument -- For international shipments. This section contains
    information about the exported goods relevant for customs. For
    international shipments: commercial invoice and customs
    declaration (CN23) have to be attached to the shipment. Data
    relevant for customs also has to be transferred as
    electronically.
    feederSystem -- Is only to be indicated by DHL partners
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ShipmentDetails=None, Shipper=None, Receiver=None, ReturnReceiver=None, ExportDocument=None, feederSystem=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ShipmentDetails = ShipmentDetails
        self.ShipmentDetails_nsprefix_ = None
        self.Shipper = Shipper
        self.Shipper_nsprefix_ = None
        self.Receiver = Receiver
        self.Receiver_nsprefix_ = None
        self.ReturnReceiver = ReturnReceiver
        self.ReturnReceiver_nsprefix_ = None
        self.ExportDocument = ExportDocument
        self.ExportDocument_nsprefix_ = None
        self.feederSystem = feederSystem
        self.validate_feederSystemType19(self.feederSystem)
        self.feederSystem_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ShipmentType18)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ShipmentType18.subclass:
            return ShipmentType18.subclass(*args_, **kwargs_)
        else:
            return ShipmentType18(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ShipmentDetails(self):
        return self.ShipmentDetails
    def set_ShipmentDetails(self, ShipmentDetails):
        self.ShipmentDetails = ShipmentDetails
    def get_Shipper(self):
        return self.Shipper
    def set_Shipper(self, Shipper):
        self.Shipper = Shipper
    def get_Receiver(self):
        return self.Receiver
    def set_Receiver(self, Receiver):
        self.Receiver = Receiver
    def get_ReturnReceiver(self):
        return self.ReturnReceiver
    def set_ReturnReceiver(self, ReturnReceiver):
        self.ReturnReceiver = ReturnReceiver
    def get_ExportDocument(self):
        return self.ExportDocument
    def set_ExportDocument(self, ExportDocument):
        self.ExportDocument = ExportDocument
    def get_feederSystem(self):
        return self.feederSystem
    def set_feederSystem(self, feederSystem):
        self.feederSystem = feederSystem
    def validate_feederSystemType19(self, value):
        result = True
        # Validate type feederSystemType19, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            pass
        return result
    def _hasContent(self):
        if (
            self.ShipmentDetails is not None or
            self.Shipper is not None or
            self.Receiver is not None or
            self.ReturnReceiver is not None or
            self.ExportDocument is not None or
            self.feederSystem is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentType18', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ShipmentType18')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ShipmentType18':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ShipmentType18')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ShipmentType18', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ShipmentType18'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ShipmentType18', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ShipmentDetails is not None:
            namespaceprefix_ = self.ShipmentDetails_nsprefix_ + ':' if (UseCapturedNS_ and self.ShipmentDetails_nsprefix_) else ''
            self.ShipmentDetails.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ShipmentDetails', pretty_print=pretty_print)
        if self.Shipper is not None:
            namespaceprefix_ = self.Shipper_nsprefix_ + ':' if (UseCapturedNS_ and self.Shipper_nsprefix_) else ''
            self.Shipper.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Shipper', pretty_print=pretty_print)
        if self.Receiver is not None:
            namespaceprefix_ = self.Receiver_nsprefix_ + ':' if (UseCapturedNS_ and self.Receiver_nsprefix_) else ''
            self.Receiver.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Receiver', pretty_print=pretty_print)
        if self.ReturnReceiver is not None:
            namespaceprefix_ = self.ReturnReceiver_nsprefix_ + ':' if (UseCapturedNS_ and self.ReturnReceiver_nsprefix_) else ''
            self.ReturnReceiver.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ReturnReceiver', pretty_print=pretty_print)
        if self.ExportDocument is not None:
            namespaceprefix_ = self.ExportDocument_nsprefix_ + ':' if (UseCapturedNS_ and self.ExportDocument_nsprefix_) else ''
            self.ExportDocument.export(outfile, level, namespaceprefix_, namespacedef_='', name_='ExportDocument', pretty_print=pretty_print)
        if self.feederSystem is not None:
            namespaceprefix_ = self.feederSystem_nsprefix_ + ':' if (UseCapturedNS_ and self.feederSystem_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sfeederSystem>%s</%sfeederSystem>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.feederSystem), input_name='feederSystem')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ShipmentDetails':
            obj_ = ShipmentDetailsTypeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ShipmentDetails = obj_
            obj_.original_tagname_ = 'ShipmentDetails'
        elif nodeName_ == 'Shipper':
            obj_ = ShipperType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Shipper = obj_
            obj_.original_tagname_ = 'Shipper'
        elif nodeName_ == 'Receiver':
            obj_ = ReceiverType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Receiver = obj_
            obj_.original_tagname_ = 'Receiver'
        elif nodeName_ == 'ReturnReceiver':
            obj_ = ShipperType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ReturnReceiver = obj_
            obj_.original_tagname_ = 'ReturnReceiver'
        elif nodeName_ == 'ExportDocument':
            obj_ = ExportDocumentType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ExportDocument = obj_
            obj_.original_tagname_ = 'ExportDocument'
        elif nodeName_ == 'feederSystem':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'feederSystem')
            value_ = self.gds_validate_string(value_, node, 'feederSystem')
            self.feederSystem = value_
            self.feederSystem_nsprefix_ = child_.prefix
            # validate type feederSystemType19
            self.validate_feederSystemType19(self.feederSystem)
# end class ShipmentType18


class IdentType(GeneratedsSuper):
    """surname -- Surname (family name) of the person for ident
    check.
    givenName -- Given name (first name) of the person for ident
    check.
    dateOfBirth -- date of birth (DOB) of the person for ident check,
    if the option is used: Date in format yyyy-mm-dd This attribute
    is only optional, if you set a minimum age
    minimumAge --  minimum age of the person for ident check ("A16"
    or "A18") This attribute is only optional, if you specify the
    date of birth
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, surname=None, givenName=None, dateOfBirth=None, minimumAge=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.surname = surname
        self.validate_surnameType(self.surname)
        self.surname_nsprefix_ = None
        self.givenName = givenName
        self.validate_givenNameType(self.givenName)
        self.givenName_nsprefix_ = None
        self.dateOfBirth = dateOfBirth
        self.validate_dateOfBirthType(self.dateOfBirth)
        self.dateOfBirth_nsprefix_ = None
        self.minimumAge = minimumAge
        self.validate_minimumAgeType(self.minimumAge)
        self.minimumAge_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, IdentType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if IdentType.subclass:
            return IdentType.subclass(*args_, **kwargs_)
        else:
            return IdentType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_surname(self):
        return self.surname
    def set_surname(self, surname):
        self.surname = surname
    def get_givenName(self):
        return self.givenName
    def set_givenName(self, givenName):
        self.givenName = givenName
    def get_dateOfBirth(self):
        return self.dateOfBirth
    def set_dateOfBirth(self, dateOfBirth):
        self.dateOfBirth = dateOfBirth
    def get_minimumAge(self):
        return self.minimumAge
    def set_minimumAge(self, minimumAge):
        self.minimumAge = minimumAge
    def validate_surnameType(self, value):
        result = True
        # Validate type surnameType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 255:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on surnameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on surnameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_givenNameType(self, value):
        result = True
        # Validate type givenNameType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 255:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on givenNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on givenNameType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_dateOfBirthType(self, value):
        result = True
        # Validate type dateOfBirthType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on dateOfBirthType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on dateOfBirthType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_minimumAgeType(self, value):
        result = True
        # Validate type minimumAgeType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 3:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on minimumAgeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on minimumAgeType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.surname is not None or
            self.givenName is not None or
            self.dateOfBirth is not None or
            self.minimumAge is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='IdentType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('IdentType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'IdentType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='IdentType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='IdentType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='IdentType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='IdentType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.surname is not None:
            namespaceprefix_ = self.surname_nsprefix_ + ':' if (UseCapturedNS_ and self.surname_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%ssurname>%s</%ssurname>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.surname), input_name='surname')), namespaceprefix_ , eol_))
        if self.givenName is not None:
            namespaceprefix_ = self.givenName_nsprefix_ + ':' if (UseCapturedNS_ and self.givenName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sgivenName>%s</%sgivenName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.givenName), input_name='givenName')), namespaceprefix_ , eol_))
        if self.dateOfBirth is not None:
            namespaceprefix_ = self.dateOfBirth_nsprefix_ + ':' if (UseCapturedNS_ and self.dateOfBirth_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdateOfBirth>%s</%sdateOfBirth>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.dateOfBirth), input_name='dateOfBirth')), namespaceprefix_ , eol_))
        if self.minimumAge is not None:
            namespaceprefix_ = self.minimumAge_nsprefix_ + ':' if (UseCapturedNS_ and self.minimumAge_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sminimumAge>%s</%sminimumAge>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.minimumAge), input_name='minimumAge')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'surname':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'surname')
            value_ = self.gds_validate_string(value_, node, 'surname')
            self.surname = value_
            self.surname_nsprefix_ = child_.prefix
            # validate type surnameType
            self.validate_surnameType(self.surname)
        elif nodeName_ == 'givenName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'givenName')
            value_ = self.gds_validate_string(value_, node, 'givenName')
            self.givenName = value_
            self.givenName_nsprefix_ = child_.prefix
            # validate type givenNameType
            self.validate_givenNameType(self.givenName)
        elif nodeName_ == 'dateOfBirth':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'dateOfBirth')
            value_ = self.gds_validate_string(value_, node, 'dateOfBirth')
            self.dateOfBirth = value_
            self.dateOfBirth_nsprefix_ = child_.prefix
            # validate type dateOfBirthType
            self.validate_dateOfBirthType(self.dateOfBirth)
        elif nodeName_ == 'minimumAge':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'minimumAge')
            value_ = self.gds_validate_string(value_, node, 'minimumAge')
            self.minimumAge = value_
            self.minimumAge_nsprefix_ = child_.prefix
            # validate type minimumAgeType
            self.validate_minimumAgeType(self.minimumAge)
# end class IdentType


class ExportDocPositionType(GeneratedsSuper):
    """ExportDocPositionType -- One or more child elements for every position to be defined
    within the Export Document. Each one contains description, country code of
    origin, amount, net weight, customs value. Multiple positions only possible
    for shipments using DHL Paket International (V53WPAK). Shipments using DHL
    Europaket (V54EPAK) can only contain one ExportDocPosition.
    description -- Description of the goods
    countryCodeOrigin -- ISO-Code (ISO 3166-2) of country the goods were
    manufactured
    customsTariffNumber -- Customs tariff number of the unit / position. If the
    service PDDP is used, customsTariffNumber is required.
    amount -- Quantity of the unit / position. Only positive values
    (
    >
    0) are allowed.
    netWeightInKG -- Net weight of the unit / position. Only positive
    values (
    >
    0) are allowed.The total net weight must not exceed
    the shipment weight
    customsValue -- Customs value amount of the unit /position. Only
    positive values (
    >
    0) are allowed.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, description=None, countryCodeOrigin=None, customsTariffNumber=None, amount=None, netWeightInKG=None, customsValue=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.description = description
        self.validate_descriptionType(self.description)
        self.description_nsprefix_ = None
        self.countryCodeOrigin = countryCodeOrigin
        self.validate_countryCodeOriginType(self.countryCodeOrigin)
        self.countryCodeOrigin_nsprefix_ = None
        self.customsTariffNumber = customsTariffNumber
        self.validate_customsTariffNumberType(self.customsTariffNumber)
        self.customsTariffNumber_nsprefix_ = None
        self.amount = amount
        self.validate_amountType(self.amount)
        self.amount_nsprefix_ = None
        self.netWeightInKG = netWeightInKG
        self.validate_netWeightInKGType(self.netWeightInKG)
        self.netWeightInKG_nsprefix_ = None
        self.customsValue = customsValue
        self.validate_customsValueType(self.customsValue)
        self.customsValue_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ExportDocPositionType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ExportDocPositionType.subclass:
            return ExportDocPositionType.subclass(*args_, **kwargs_)
        else:
            return ExportDocPositionType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_description(self):
        return self.description
    def set_description(self, description):
        self.description = description
    def get_countryCodeOrigin(self):
        return self.countryCodeOrigin
    def set_countryCodeOrigin(self, countryCodeOrigin):
        self.countryCodeOrigin = countryCodeOrigin
    def get_customsTariffNumber(self):
        return self.customsTariffNumber
    def set_customsTariffNumber(self, customsTariffNumber):
        self.customsTariffNumber = customsTariffNumber
    def get_amount(self):
        return self.amount
    def set_amount(self, amount):
        self.amount = amount
    def get_netWeightInKG(self):
        return self.netWeightInKG
    def set_netWeightInKG(self, netWeightInKG):
        self.netWeightInKG = netWeightInKG
    def get_customsValue(self):
        return self.customsValue
    def set_customsValue(self, customsValue):
        self.customsValue = customsValue
    def validate_descriptionType(self, value):
        result = True
        # Validate type descriptionType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on descriptionType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_countryCodeOriginType(self, value):
        result = True
        # Validate type countryCodeOriginType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on countryCodeOriginType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
            if len(value) < 2:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on countryCodeOriginType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_customsTariffNumberType(self, value):
        result = True
        # Validate type customsTariffNumberType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on customsTariffNumberType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_amountType(self, value):
        result = True
        # Validate type amountType, a restriction on xs:integer.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if value < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on amountType' % {"value": value, "lineno": lineno} )
                result = False
            if len(str(value)) >= 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd totalDigits restriction on amountType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_netWeightInKGType(self, value):
        result = True
        # Validate type netWeightInKGType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if value < 0.000:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on netWeightInKGType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 999999.999:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on netWeightInKGType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_customsValueType(self, value):
        result = True
        # Validate type customsValueType, a restriction on xs:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if value < 0.0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minInclusive restriction on customsValueType' % {"value": value, "lineno": lineno} )
                result = False
            if value > 999999.99:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on customsValueType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.description is not None or
            self.countryCodeOrigin is not None or
            self.customsTariffNumber is not None or
            self.amount is not None or
            self.netWeightInKG is not None or
            self.customsValue is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ExportDocPositionType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ExportDocPositionType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ExportDocPositionType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ExportDocPositionType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ExportDocPositionType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ExportDocPositionType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ExportDocPositionType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.description is not None:
            namespaceprefix_ = self.description_nsprefix_ + ':' if (UseCapturedNS_ and self.description_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sdescription>%s</%sdescription>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.description), input_name='description')), namespaceprefix_ , eol_))
        if self.countryCodeOrigin is not None:
            namespaceprefix_ = self.countryCodeOrigin_nsprefix_ + ':' if (UseCapturedNS_ and self.countryCodeOrigin_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scountryCodeOrigin>%s</%scountryCodeOrigin>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.countryCodeOrigin), input_name='countryCodeOrigin')), namespaceprefix_ , eol_))
        if self.customsTariffNumber is not None:
            namespaceprefix_ = self.customsTariffNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.customsTariffNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scustomsTariffNumber>%s</%scustomsTariffNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.customsTariffNumber), input_name='customsTariffNumber')), namespaceprefix_ , eol_))
        if self.amount is not None:
            namespaceprefix_ = self.amount_nsprefix_ + ':' if (UseCapturedNS_ and self.amount_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%samount>%s</%samount>%s' % (namespaceprefix_ , self.gds_format_integer(self.amount, input_name='amount'), namespaceprefix_ , eol_))
        if self.netWeightInKG is not None:
            namespaceprefix_ = self.netWeightInKG_nsprefix_ + ':' if (UseCapturedNS_ and self.netWeightInKG_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%snetWeightInKG>%s</%snetWeightInKG>%s' % (namespaceprefix_ , self.gds_format_decimal(self.netWeightInKG, input_name='netWeightInKG'), namespaceprefix_ , eol_))
        if self.customsValue is not None:
            namespaceprefix_ = self.customsValue_nsprefix_ + ':' if (UseCapturedNS_ and self.customsValue_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scustomsValue>%s</%scustomsValue>%s' % (namespaceprefix_ , self.gds_format_decimal(self.customsValue, input_name='customsValue'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'description':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'description')
            value_ = self.gds_validate_string(value_, node, 'description')
            self.description = value_
            self.description_nsprefix_ = child_.prefix
            # validate type descriptionType
            self.validate_descriptionType(self.description)
        elif nodeName_ == 'countryCodeOrigin':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'countryCodeOrigin')
            value_ = self.gds_validate_string(value_, node, 'countryCodeOrigin')
            self.countryCodeOrigin = value_
            self.countryCodeOrigin_nsprefix_ = child_.prefix
            # validate type countryCodeOriginType
            self.validate_countryCodeOriginType(self.countryCodeOrigin)
        elif nodeName_ == 'customsTariffNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'customsTariffNumber')
            value_ = self.gds_validate_string(value_, node, 'customsTariffNumber')
            self.customsTariffNumber = value_
            self.customsTariffNumber_nsprefix_ = child_.prefix
            # validate type customsTariffNumberType
            self.validate_customsTariffNumberType(self.customsTariffNumber)
        elif nodeName_ == 'amount' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'amount')
            ival_ = self.gds_validate_integer(ival_, node, 'amount')
            self.amount = ival_
            self.amount_nsprefix_ = child_.prefix
            # validate type amountType
            self.validate_amountType(self.amount)
        elif nodeName_ == 'netWeightInKG' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'netWeightInKG')
            fval_ = self.gds_validate_decimal(fval_, node, 'netWeightInKG')
            self.netWeightInKG = fval_
            self.netWeightInKG_nsprefix_ = child_.prefix
            # validate type netWeightInKGType
            self.validate_netWeightInKGType(self.netWeightInKG)
        elif nodeName_ == 'customsValue' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'customsValue')
            fval_ = self.gds_validate_decimal(fval_, node, 'customsValue')
            self.customsValue = fval_
            self.customsValue_nsprefix_ = child_.prefix
            # validate type customsValueType
            self.validate_customsValueType(self.customsValue)
# end class ExportDocPositionType


class DeliveryAdressType(GeneratedsSuper):
    """DeliveryAdressType -- Mandatory if further address is to be specified.
    Company -- Determines whether further address is one of the
    following types.
    Name3 -- Extra data for name extension.
    Address -- Contains address data.
    Communication -- Info about communication.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Company=None, Name3=None, Address=None, Communication=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Company = Company
        self.Company_nsprefix_ = None
        self.Name3 = Name3
        self.Name3_nsprefix_ = None
        self.Address = Address
        self.Address_nsprefix_ = None
        self.Communication = Communication
        self.Communication_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DeliveryAdressType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DeliveryAdressType.subclass:
            return DeliveryAdressType.subclass(*args_, **kwargs_)
        else:
            return DeliveryAdressType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Company(self):
        return self.Company
    def set_Company(self, Company):
        self.Company = Company
    def get_Name3(self):
        return self.Name3
    def set_Name3(self, Name3):
        self.Name3 = Name3
    def get_Address(self):
        return self.Address
    def set_Address(self, Address):
        self.Address = Address
    def get_Communication(self):
        return self.Communication
    def set_Communication(self, Communication):
        self.Communication = Communication
    def _hasContent(self):
        if (
            self.Company is not None or
            self.Name3 is not None or
            self.Address is not None or
            self.Communication is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeliveryAdressType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DeliveryAdressType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DeliveryAdressType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DeliveryAdressType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DeliveryAdressType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DeliveryAdressType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DeliveryAdressType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Company is not None:
            namespaceprefix_ = self.Company_nsprefix_ + ':' if (UseCapturedNS_ and self.Company_nsprefix_) else ''
            self.Company.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Company', pretty_print=pretty_print)
        if self.Name3 is not None:
            namespaceprefix_ = self.Name3_nsprefix_ + ':' if (UseCapturedNS_ and self.Name3_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sName3>%s</%sName3>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Name3), input_name='Name3')), namespaceprefix_ , eol_))
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print)
        if self.Communication is not None:
            namespaceprefix_ = self.Communication_nsprefix_ + ':' if (UseCapturedNS_ and self.Communication_nsprefix_) else ''
            self.Communication.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Communication', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Company':
            obj_ = NameType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Company = obj_
            obj_.original_tagname_ = 'Company'
        elif nodeName_ == 'Name3':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Name3')
            value_ = self.gds_validate_string(value_, node, 'Name3')
            self.Name3 = value_
            self.Name3_nsprefix_ = child_.prefix
        elif nodeName_ == 'Address':
            obj_ = NativeAddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'Communication':
            obj_ = CommunicationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Communication = obj_
            obj_.original_tagname_ = 'Communication'
# end class DeliveryAdressType


class DrivingLicenseType(GeneratedsSuper):
    """DrivingLicenseType -- If driving license shall be used for verifying identity.
    LicenseNumber -- ID number of the driving license. Mandatory if
    DrivingLicense is chosen as identity instrument.
    Authority -- Name of certifying authority of the driving
    license. Mandatory if DrivingLicense is chosen as identity
    instrument.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, LicenseNumber=None, Authority=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.LicenseNumber = LicenseNumber
        self.LicenseNumber_nsprefix_ = None
        self.Authority = Authority
        self.Authority_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DrivingLicenseType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DrivingLicenseType.subclass:
            return DrivingLicenseType.subclass(*args_, **kwargs_)
        else:
            return DrivingLicenseType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_LicenseNumber(self):
        return self.LicenseNumber
    def set_LicenseNumber(self, LicenseNumber):
        self.LicenseNumber = LicenseNumber
    def get_Authority(self):
        return self.Authority
    def set_Authority(self, Authority):
        self.Authority = Authority
    def _hasContent(self):
        if (
            self.LicenseNumber is not None or
            self.Authority is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DrivingLicenseType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DrivingLicenseType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DrivingLicenseType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DrivingLicenseType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DrivingLicenseType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DrivingLicenseType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DrivingLicenseType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.LicenseNumber is not None:
            namespaceprefix_ = self.LicenseNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.LicenseNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLicenseNumber>%s</%sLicenseNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LicenseNumber), input_name='LicenseNumber')), namespaceprefix_ , eol_))
        if self.Authority is not None:
            namespaceprefix_ = self.Authority_nsprefix_ + ':' if (UseCapturedNS_ and self.Authority_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAuthority>%s</%sAuthority>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Authority), input_name='Authority')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'LicenseNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LicenseNumber')
            value_ = self.gds_validate_string(value_, node, 'LicenseNumber')
            self.LicenseNumber = value_
            self.LicenseNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'Authority':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Authority')
            value_ = self.gds_validate_string(value_, node, 'Authority')
            self.Authority = value_
            self.Authority_nsprefix_ = child_.prefix
# end class DrivingLicenseType


class IdentityCardType(GeneratedsSuper):
    """IdentityCardType -- If identity card shall be used for verifying identity.
    CardNumber -- Number of the identity card. Mandatory if
    IdentityCard is chosen as identity instrument. Field length
    must be less than or equal to 20.
    CardAuthority -- Name of certifying card authority. Mandatory if
    IdentityCard is chosen as identity instrument. Field length
    must be less than or equal to 30.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CardNumber=None, CardAuthority=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CardNumber = CardNumber
        self.CardNumber_nsprefix_ = None
        self.CardAuthority = CardAuthority
        self.CardAuthority_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, IdentityCardType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if IdentityCardType.subclass:
            return IdentityCardType.subclass(*args_, **kwargs_)
        else:
            return IdentityCardType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CardNumber(self):
        return self.CardNumber
    def set_CardNumber(self, CardNumber):
        self.CardNumber = CardNumber
    def get_CardAuthority(self):
        return self.CardAuthority
    def set_CardAuthority(self, CardAuthority):
        self.CardAuthority = CardAuthority
    def _hasContent(self):
        if (
            self.CardNumber is not None or
            self.CardAuthority is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='IdentityCardType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('IdentityCardType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'IdentityCardType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='IdentityCardType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='IdentityCardType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='IdentityCardType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='IdentityCardType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CardNumber is not None:
            namespaceprefix_ = self.CardNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.CardNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCardNumber>%s</%sCardNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CardNumber), input_name='CardNumber')), namespaceprefix_ , eol_))
        if self.CardAuthority is not None:
            namespaceprefix_ = self.CardAuthority_nsprefix_ + ':' if (UseCapturedNS_ and self.CardAuthority_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCardAuthority>%s</%sCardAuthority>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CardAuthority), input_name='CardAuthority')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CardNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CardNumber')
            value_ = self.gds_validate_string(value_, node, 'CardNumber')
            self.CardNumber = value_
            self.CardNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'CardAuthority':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CardAuthority')
            value_ = self.gds_validate_string(value_, node, 'CardAuthority')
            self.CardAuthority = value_
            self.CardAuthority_nsprefix_ = child_.prefix
# end class IdentityCardType


class BankCardType(GeneratedsSuper):
    """BankCardType -- If a bank card shall be used for verifying identity.
    CardType -- Type of bank card. Mandatory if BankCard is
    chosen as identity instrument.
    CardNumber -- Number of bank card. Mandatory if BankCard is
    chosen as identity instrument.
    BankName -- Name of bank. Mandatory if BankCard is chosen as
    identity instrument.
    BankCode -- Bank code. Mandatory if BankCard is chosen as
    identity instrument.
    
    """
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, CardType=None, CardNumber=None, BankName=None, BankCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.CardType = CardType
        self.CardType_nsprefix_ = None
        self.CardNumber = CardNumber
        self.CardNumber_nsprefix_ = None
        self.BankName = BankName
        self.BankName_nsprefix_ = None
        self.BankCode = BankCode
        self.BankCode_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, BankCardType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BankCardType.subclass:
            return BankCardType.subclass(*args_, **kwargs_)
        else:
            return BankCardType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_CardType(self):
        return self.CardType
    def set_CardType(self, CardType):
        self.CardType = CardType
    def get_CardNumber(self):
        return self.CardNumber
    def set_CardNumber(self, CardNumber):
        self.CardNumber = CardNumber
    def get_BankName(self):
        return self.BankName
    def set_BankName(self, BankName):
        self.BankName = BankName
    def get_BankCode(self):
        return self.BankCode
    def set_BankCode(self, BankCode):
        self.BankCode = BankCode
    def _hasContent(self):
        if (
            self.CardType is not None or
            self.CardNumber is not None or
            self.BankName is not None or
            self.BankCode is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BankCardType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('BankCardType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'BankCardType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BankCardType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='BankCardType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='BankCardType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='BankCardType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CardType is not None:
            namespaceprefix_ = self.CardType_nsprefix_ + ':' if (UseCapturedNS_ and self.CardType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCardType>%s</%sCardType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CardType), input_name='CardType')), namespaceprefix_ , eol_))
        if self.CardNumber is not None:
            namespaceprefix_ = self.CardNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.CardNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCardNumber>%s</%sCardNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CardNumber), input_name='CardNumber')), namespaceprefix_ , eol_))
        if self.BankName is not None:
            namespaceprefix_ = self.BankName_nsprefix_ + ':' if (UseCapturedNS_ and self.BankName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBankName>%s</%sBankName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BankName), input_name='BankName')), namespaceprefix_ , eol_))
        if self.BankCode is not None:
            namespaceprefix_ = self.BankCode_nsprefix_ + ':' if (UseCapturedNS_ and self.BankCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBankCode>%s</%sBankCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BankCode), input_name='BankCode')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CardType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CardType')
            value_ = self.gds_validate_string(value_, node, 'CardType')
            self.CardType = value_
            self.CardType_nsprefix_ = child_.prefix
        elif nodeName_ == 'CardNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CardNumber')
            value_ = self.gds_validate_string(value_, node, 'CardNumber')
            self.CardNumber = value_
            self.CardNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'BankName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BankName')
            value_ = self.gds_validate_string(value_, node, 'BankName')
            self.BankName = value_
            self.BankName_nsprefix_ = child_.prefix
        elif nodeName_ == 'BankCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BankCode')
            value_ = self.gds_validate_string(value_, node, 'BankCode')
            self.BankCode = value_
            self.BankCode_nsprefix_ = child_.prefix
# end class BankCardType


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
        rootTag = 'GetVersionResponse'
        rootClass = GetVersionResponse
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
        rootTag = 'GetVersionResponse'
        rootClass = GetVersionResponse
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
        rootTag = 'GetVersionResponse'
        rootClass = GetVersionResponse
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:bcs="http://dhl.de/webservices/businesscustomershipping/3.0"')
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
        rootTag = 'GetVersionResponse'
        rootClass = GetVersionResponse
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from business_interface import *\n\n')
        sys.stdout.write('import business_interface as model_\n\n')
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
    "{http://dhl.de/webservices/businesscustomershipping/3.0}ParcelShopType": "ParcelShopType3",
    "{http://dhl.de/webservices/businesscustomershipping/3.0}PickupAddressType": "PickupAddressType1",
    "{http://dhl.de/webservices/businesscustomershipping/3.0}PostfilialeType": "PostfilialeType2",
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
                                       'CT')],
 'http://dhl.de/webservices/businesscustomershipping/3.0': [('SequenceNumber',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'ST'),
                                                            ('ShipperReferenceType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'ST'),
                                                            ('CreationState',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ValidationState',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('Statusinformation',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('StatusElement',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('PieceInformation',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ShipmentOrderType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ValidateShipmentOrderType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ShipperTypeType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ShipperType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ReceiverTypeType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ReceiverType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('Ident',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ShipmentDetailsType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ShipmentDetailsTypeType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ShipmentItemType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ShipmentItemTypeType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ShipmentService',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('Serviceconfiguration',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ServiceconfigurationDetails',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ServiceconfigurationDetailsPreferredDay',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ServiceconfigurationDetailsPreferredLocation',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ServiceconfigurationDetailsPreferredNeighbour',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ServiceconfigurationDetailsOptional',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ServiceconfigurationDetailsResponse',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ServiceconfigurationType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ServiceconfigurationEndorsement',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ServiceconfigurationISR',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ServiceconfigurationDH',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ServiceconfigurationVisualAgeCheck',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ServiceconfigurationDeliveryTimeframe',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ServiceconfigurationDateOfDelivery',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ServiceconfigurationAdditionalInsurance',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ServiceconfigurationCashOnDelivery',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ServiceconfigurationUnfree',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('PDDP',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('CDP',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('Economy',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ServiceconfigurationIC',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ShipmentNotificationType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ExportDocumentType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('FurtherAddressesType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('LabelData',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ExportDocData',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ManifestState',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('DeletionState',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('PickupDetailsType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('PickupAddressType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('PickupOrdererType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('PickupBookingInformationType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('IdentityData',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('PackstationType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('PostfilialeType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT'),
                                                            ('ParcelShopType',
                                                             './schemas/geschaeftskundenversand-api-3.4.0-schema-bcs_base.xsd',
                                                             'CT')]}

__all__ = [
    "AuthentificationType",
    "BankCardType",
    "BankType",
    "BookPickupRequest",
    "BookPickupResponse",
    "CancelPickupRequest",
    "CancelPickupResponse",
    "CommunicationType",
    "ContactType",
    "CountryType",
    "CreateShipmentOrderRequest",
    "CreateShipmentOrderResponse",
    "CreationState",
    "CustomerType",
    "DeleteShipmentOrderRequest",
    "DeleteShipmentOrderResponse",
    "DeletionState",
    "DeliveryAddressType",
    "DeliveryAdressType",
    "Dimension",
    "DoManifestRequest",
    "DoManifestResponse",
    "DrivingLicenseType",
    "EKP",
    "ErrorType",
    "ExportDocData",
    "ExportDocPositionType",
    "ExportDocumentType",
    "FurtherAddressesType",
    "GetExportDocRequest",
    "GetExportDocResponse",
    "GetLabelRequest",
    "GetLabelResponse",
    "GetManifestRequest",
    "GetManifestResponse",
    "GetVersionResponse",
    "Ident",
    "IdentType",
    "IdentityCardType",
    "IdentityData",
    "LabelData",
    "ManifestState",
    "NameType",
    "NativeAddressType",
    "NativeAddressTypeNew",
    "PackStationType",
    "ParcelShopType",
    "PickupAddressType",
    "PickupAddressType1",
    "PickupBookingInformationType",
    "PickupDetailsType",
    "PickupOrdererType",
    "PieceInformation",
    "PostfilialeType",
    "PostfilialeTypeNoCountry",
    "ReadShipmentOrderResponse",
    "ReceiverNameType",
    "ReceiverNativeAddressType",
    "ReceiverType",
    "ReceiverTypeType",
    "ShipmentDetailsType",
    "ShipmentDetailsTypeType",
    "ShipmentItemType",
    "ShipmentItemTypeType",
    "ShipmentNotificationType",
    "ShipmentNumberType",
    "ShipmentOrderType",
    "ShipmentService",
    "ShipmentType",
    "ShipmentType18",
    "ShipperType",
    "ShipperTypeType",
    "Status",
    "StatusElement",
    "Statusinformation",
    "TimeFrame",
    "UpdateShipmentOrderRequest",
    "UpdateShipmentOrderResponse",
    "ValidateShipmentOrderRequest",
    "ValidateShipmentOrderType",
    "ValidateShipmentResponse",
    "ValidationState",
    "Version",
    "ZipType",
    "accountNumber",
    "accountNumberExpress",
    "airwayBill",
    "allShipments",
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
