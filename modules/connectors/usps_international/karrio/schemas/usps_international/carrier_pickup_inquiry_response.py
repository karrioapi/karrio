#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Wed Apr  3 21:09:02 2024 by generateDS.py version 2.43.3.
# Python 3.10.13 (main, Mar 21 2024, 17:51:02) [GCC 9.4.0]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './karrio/schemas/usps_international/carrier_pickup_inquiry_response.py')
#
# Command line arguments:
#   ./schemas/CarrierPickupInquiryResponse.xsd
#
# Command line:
#   /workspaces/karrio/.venv/karrio/bin/generateDS --no-namespace-defs -o "./karrio/schemas/usps_international/carrier_pickup_inquiry_response.py" ./schemas/CarrierPickupInquiryResponse.xsd
#
# Current working directory (os.getcwd()):
#   usps_international
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
#
# Start data representation classes
#
class CarrierPickupInquiryResponse(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, FirstName=None, LastName=None, FirmName=None, SuiteOrApt=None, Address2=None, Urbanization=None, City=None, State=None, ZIP5=None, ZIP4=None, Phone=None, Extension=None, Package=None, EstimatedWeight=None, PackageLocation=None, SpecialInstructions=None, ConfirmationNumber=None, DayOfWeek=None, Date=None, EmailAddress=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.FirstName = FirstName
        self.FirstName_nsprefix_ = None
        self.LastName = LastName
        self.LastName_nsprefix_ = None
        self.FirmName = FirmName
        self.FirmName_nsprefix_ = None
        self.SuiteOrApt = SuiteOrApt
        self.SuiteOrApt_nsprefix_ = None
        self.Address2 = Address2
        self.Address2_nsprefix_ = None
        self.Urbanization = Urbanization
        self.Urbanization_nsprefix_ = None
        self.City = City
        self.City_nsprefix_ = None
        self.State = State
        self.State_nsprefix_ = None
        self.ZIP5 = ZIP5
        self.ZIP5_nsprefix_ = None
        self.ZIP4 = ZIP4
        self.ZIP4_nsprefix_ = None
        self.Phone = Phone
        self.Phone_nsprefix_ = None
        self.Extension = Extension
        self.Extension_nsprefix_ = None
        if Package is None:
            self.Package = []
        else:
            self.Package = Package
        self.Package_nsprefix_ = None
        self.EstimatedWeight = EstimatedWeight
        self.EstimatedWeight_nsprefix_ = None
        self.PackageLocation = PackageLocation
        self.PackageLocation_nsprefix_ = None
        self.SpecialInstructions = SpecialInstructions
        self.SpecialInstructions_nsprefix_ = None
        self.ConfirmationNumber = ConfirmationNumber
        self.ConfirmationNumber_nsprefix_ = None
        self.DayOfWeek = DayOfWeek
        self.DayOfWeek_nsprefix_ = None
        self.Date = Date
        self.Date_nsprefix_ = None
        self.EmailAddress = EmailAddress
        self.EmailAddress_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, CarrierPickupInquiryResponse)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CarrierPickupInquiryResponse.subclass:
            return CarrierPickupInquiryResponse.subclass(*args_, **kwargs_)
        else:
            return CarrierPickupInquiryResponse(*args_, **kwargs_)
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
    def get_FirmName(self):
        return self.FirmName
    def set_FirmName(self, FirmName):
        self.FirmName = FirmName
    def get_SuiteOrApt(self):
        return self.SuiteOrApt
    def set_SuiteOrApt(self, SuiteOrApt):
        self.SuiteOrApt = SuiteOrApt
    def get_Address2(self):
        return self.Address2
    def set_Address2(self, Address2):
        self.Address2 = Address2
    def get_Urbanization(self):
        return self.Urbanization
    def set_Urbanization(self, Urbanization):
        self.Urbanization = Urbanization
    def get_City(self):
        return self.City
    def set_City(self, City):
        self.City = City
    def get_State(self):
        return self.State
    def set_State(self, State):
        self.State = State
    def get_ZIP5(self):
        return self.ZIP5
    def set_ZIP5(self, ZIP5):
        self.ZIP5 = ZIP5
    def get_ZIP4(self):
        return self.ZIP4
    def set_ZIP4(self, ZIP4):
        self.ZIP4 = ZIP4
    def get_Phone(self):
        return self.Phone
    def set_Phone(self, Phone):
        self.Phone = Phone
    def get_Extension(self):
        return self.Extension
    def set_Extension(self, Extension):
        self.Extension = Extension
    def get_Package(self):
        return self.Package
    def set_Package(self, Package):
        self.Package = Package
    def add_Package(self, value):
        self.Package.append(value)
    def insert_Package_at(self, index, value):
        self.Package.insert(index, value)
    def replace_Package_at(self, index, value):
        self.Package[index] = value
    def get_EstimatedWeight(self):
        return self.EstimatedWeight
    def set_EstimatedWeight(self, EstimatedWeight):
        self.EstimatedWeight = EstimatedWeight
    def get_PackageLocation(self):
        return self.PackageLocation
    def set_PackageLocation(self, PackageLocation):
        self.PackageLocation = PackageLocation
    def get_SpecialInstructions(self):
        return self.SpecialInstructions
    def set_SpecialInstructions(self, SpecialInstructions):
        self.SpecialInstructions = SpecialInstructions
    def get_ConfirmationNumber(self):
        return self.ConfirmationNumber
    def set_ConfirmationNumber(self, ConfirmationNumber):
        self.ConfirmationNumber = ConfirmationNumber
    def get_DayOfWeek(self):
        return self.DayOfWeek
    def set_DayOfWeek(self, DayOfWeek):
        self.DayOfWeek = DayOfWeek
    def get_Date(self):
        return self.Date
    def set_Date(self, Date):
        self.Date = Date
    def get_EmailAddress(self):
        return self.EmailAddress
    def set_EmailAddress(self, EmailAddress):
        self.EmailAddress = EmailAddress
    def has__content(self):
        if (
            self.FirstName is not None or
            self.LastName is not None or
            self.FirmName is not None or
            self.SuiteOrApt is not None or
            self.Address2 is not None or
            self.Urbanization is not None or
            self.City is not None or
            self.State is not None or
            self.ZIP5 is not None or
            self.ZIP4 is not None or
            self.Phone is not None or
            self.Extension is not None or
            self.Package or
            self.EstimatedWeight is not None or
            self.PackageLocation is not None or
            self.SpecialInstructions is not None or
            self.ConfirmationNumber is not None or
            self.DayOfWeek is not None or
            self.Date is not None or
            self.EmailAddress is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CarrierPickupInquiryResponse', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CarrierPickupInquiryResponse')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CarrierPickupInquiryResponse':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CarrierPickupInquiryResponse')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='CarrierPickupInquiryResponse', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CarrierPickupInquiryResponse'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='CarrierPickupInquiryResponse', fromsubclass_=False, pretty_print=True):
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
        if self.FirmName is not None:
            namespaceprefix_ = self.FirmName_nsprefix_ + ':' if (UseCapturedNS_ and self.FirmName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFirmName>%s</%sFirmName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.FirmName), input_name='FirmName')), namespaceprefix_ , eol_))
        if self.SuiteOrApt is not None:
            namespaceprefix_ = self.SuiteOrApt_nsprefix_ + ':' if (UseCapturedNS_ and self.SuiteOrApt_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSuiteOrApt>%s</%sSuiteOrApt>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SuiteOrApt), input_name='SuiteOrApt')), namespaceprefix_ , eol_))
        if self.Address2 is not None:
            namespaceprefix_ = self.Address2_nsprefix_ + ':' if (UseCapturedNS_ and self.Address2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAddress2>%s</%sAddress2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Address2), input_name='Address2')), namespaceprefix_ , eol_))
        if self.Urbanization is not None:
            namespaceprefix_ = self.Urbanization_nsprefix_ + ':' if (UseCapturedNS_ and self.Urbanization_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sUrbanization>%s</%sUrbanization>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Urbanization), input_name='Urbanization')), namespaceprefix_ , eol_))
        if self.City is not None:
            namespaceprefix_ = self.City_nsprefix_ + ':' if (UseCapturedNS_ and self.City_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCity>%s</%sCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.City), input_name='City')), namespaceprefix_ , eol_))
        if self.State is not None:
            namespaceprefix_ = self.State_nsprefix_ + ':' if (UseCapturedNS_ and self.State_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sState>%s</%sState>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.State), input_name='State')), namespaceprefix_ , eol_))
        if self.ZIP5 is not None:
            namespaceprefix_ = self.ZIP5_nsprefix_ + ':' if (UseCapturedNS_ and self.ZIP5_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sZIP5>%s</%sZIP5>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ZIP5), input_name='ZIP5')), namespaceprefix_ , eol_))
        if self.ZIP4 is not None:
            namespaceprefix_ = self.ZIP4_nsprefix_ + ':' if (UseCapturedNS_ and self.ZIP4_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sZIP4>%s</%sZIP4>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ZIP4), input_name='ZIP4')), namespaceprefix_ , eol_))
        if self.Phone is not None:
            namespaceprefix_ = self.Phone_nsprefix_ + ':' if (UseCapturedNS_ and self.Phone_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPhone>%s</%sPhone>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Phone), input_name='Phone')), namespaceprefix_ , eol_))
        if self.Extension is not None:
            namespaceprefix_ = self.Extension_nsprefix_ + ':' if (UseCapturedNS_ and self.Extension_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExtension>%s</%sExtension>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Extension), input_name='Extension')), namespaceprefix_ , eol_))
        for Package_ in self.Package:
            namespaceprefix_ = self.Package_nsprefix_ + ':' if (UseCapturedNS_ and self.Package_nsprefix_) else ''
            Package_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='Package', pretty_print=pretty_print)
        if self.EstimatedWeight is not None:
            namespaceprefix_ = self.EstimatedWeight_nsprefix_ + ':' if (UseCapturedNS_ and self.EstimatedWeight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEstimatedWeight>%s</%sEstimatedWeight>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EstimatedWeight), input_name='EstimatedWeight')), namespaceprefix_ , eol_))
        if self.PackageLocation is not None:
            namespaceprefix_ = self.PackageLocation_nsprefix_ + ':' if (UseCapturedNS_ and self.PackageLocation_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPackageLocation>%s</%sPackageLocation>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PackageLocation), input_name='PackageLocation')), namespaceprefix_ , eol_))
        if self.SpecialInstructions is not None:
            namespaceprefix_ = self.SpecialInstructions_nsprefix_ + ':' if (UseCapturedNS_ and self.SpecialInstructions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSpecialInstructions>%s</%sSpecialInstructions>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SpecialInstructions), input_name='SpecialInstructions')), namespaceprefix_ , eol_))
        if self.ConfirmationNumber is not None:
            namespaceprefix_ = self.ConfirmationNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.ConfirmationNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sConfirmationNumber>%s</%sConfirmationNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ConfirmationNumber), input_name='ConfirmationNumber')), namespaceprefix_ , eol_))
        if self.DayOfWeek is not None:
            namespaceprefix_ = self.DayOfWeek_nsprefix_ + ':' if (UseCapturedNS_ and self.DayOfWeek_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDayOfWeek>%s</%sDayOfWeek>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DayOfWeek), input_name='DayOfWeek')), namespaceprefix_ , eol_))
        if self.Date is not None:
            namespaceprefix_ = self.Date_nsprefix_ + ':' if (UseCapturedNS_ and self.Date_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDate>%s</%sDate>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Date), input_name='Date')), namespaceprefix_ , eol_))
        if self.EmailAddress is not None:
            namespaceprefix_ = self.EmailAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.EmailAddress_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEmailAddress>%s</%sEmailAddress>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.EmailAddress), input_name='EmailAddress')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
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
        elif nodeName_ == 'FirmName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FirmName')
            value_ = self.gds_validate_string(value_, node, 'FirmName')
            self.FirmName = value_
            self.FirmName_nsprefix_ = child_.prefix
        elif nodeName_ == 'SuiteOrApt':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SuiteOrApt')
            value_ = self.gds_validate_string(value_, node, 'SuiteOrApt')
            self.SuiteOrApt = value_
            self.SuiteOrApt_nsprefix_ = child_.prefix
        elif nodeName_ == 'Address2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Address2')
            value_ = self.gds_validate_string(value_, node, 'Address2')
            self.Address2 = value_
            self.Address2_nsprefix_ = child_.prefix
        elif nodeName_ == 'Urbanization':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Urbanization')
            value_ = self.gds_validate_string(value_, node, 'Urbanization')
            self.Urbanization = value_
            self.Urbanization_nsprefix_ = child_.prefix
        elif nodeName_ == 'City':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'City')
            value_ = self.gds_validate_string(value_, node, 'City')
            self.City = value_
            self.City_nsprefix_ = child_.prefix
        elif nodeName_ == 'State':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'State')
            value_ = self.gds_validate_string(value_, node, 'State')
            self.State = value_
            self.State_nsprefix_ = child_.prefix
        elif nodeName_ == 'ZIP5':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ZIP5')
            value_ = self.gds_validate_string(value_, node, 'ZIP5')
            self.ZIP5 = value_
            self.ZIP5_nsprefix_ = child_.prefix
        elif nodeName_ == 'ZIP4':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ZIP4')
            value_ = self.gds_validate_string(value_, node, 'ZIP4')
            self.ZIP4 = value_
            self.ZIP4_nsprefix_ = child_.prefix
        elif nodeName_ == 'Phone':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Phone')
            value_ = self.gds_validate_string(value_, node, 'Phone')
            self.Phone = value_
            self.Phone_nsprefix_ = child_.prefix
        elif nodeName_ == 'Extension':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Extension')
            value_ = self.gds_validate_string(value_, node, 'Extension')
            self.Extension = value_
            self.Extension_nsprefix_ = child_.prefix
        elif nodeName_ == 'Package':
            obj_ = PackageType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Package.append(obj_)
            obj_.original_tagname_ = 'Package'
        elif nodeName_ == 'EstimatedWeight':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EstimatedWeight')
            value_ = self.gds_validate_string(value_, node, 'EstimatedWeight')
            self.EstimatedWeight = value_
            self.EstimatedWeight_nsprefix_ = child_.prefix
        elif nodeName_ == 'PackageLocation':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PackageLocation')
            value_ = self.gds_validate_string(value_, node, 'PackageLocation')
            self.PackageLocation = value_
            self.PackageLocation_nsprefix_ = child_.prefix
        elif nodeName_ == 'SpecialInstructions':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SpecialInstructions')
            value_ = self.gds_validate_string(value_, node, 'SpecialInstructions')
            self.SpecialInstructions = value_
            self.SpecialInstructions_nsprefix_ = child_.prefix
        elif nodeName_ == 'ConfirmationNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ConfirmationNumber')
            value_ = self.gds_validate_string(value_, node, 'ConfirmationNumber')
            self.ConfirmationNumber = value_
            self.ConfirmationNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'DayOfWeek':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DayOfWeek')
            value_ = self.gds_validate_string(value_, node, 'DayOfWeek')
            self.DayOfWeek = value_
            self.DayOfWeek_nsprefix_ = child_.prefix
        elif nodeName_ == 'Date':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Date')
            value_ = self.gds_validate_string(value_, node, 'Date')
            self.Date = value_
            self.Date_nsprefix_ = child_.prefix
        elif nodeName_ == 'EmailAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'EmailAddress')
            value_ = self.gds_validate_string(value_, node, 'EmailAddress')
            self.EmailAddress = value_
            self.EmailAddress_nsprefix_ = child_.prefix
# end class CarrierPickupInquiryResponse


class PackageType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, ServiceType=None, Count=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.ServiceType = ServiceType
        self.ServiceType_nsprefix_ = None
        self.Count = Count
        self.Count_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PackageType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PackageType.subclass:
            return PackageType.subclass(*args_, **kwargs_)
        else:
            return PackageType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_ServiceType(self):
        return self.ServiceType
    def set_ServiceType(self, ServiceType):
        self.ServiceType = ServiceType
    def get_Count(self):
        return self.Count
    def set_Count(self, Count):
        self.Count = Count
    def has__content(self):
        if (
            self.ServiceType is not None or
            self.Count is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PackageType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PackageType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PackageType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PackageType')
        if self.has__content():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PackageType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PackageType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PackageType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ServiceType is not None:
            namespaceprefix_ = self.ServiceType_nsprefix_ + ':' if (UseCapturedNS_ and self.ServiceType_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sServiceType>%s</%sServiceType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ServiceType), input_name='ServiceType')), namespaceprefix_ , eol_))
        if self.Count is not None:
            namespaceprefix_ = self.Count_nsprefix_ + ':' if (UseCapturedNS_ and self.Count_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCount>%s</%sCount>%s' % (namespaceprefix_ , self.gds_format_integer(self.Count, input_name='Count'), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ServiceType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ServiceType')
            value_ = self.gds_validate_string(value_, node, 'ServiceType')
            self.ServiceType = value_
            self.ServiceType_nsprefix_ = child_.prefix
        elif nodeName_ == 'Count' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'Count')
            ival_ = self.gds_validate_integer(ival_, node, 'Count')
            self.Count = ival_
            self.Count_nsprefix_ = child_.prefix
# end class PackageType


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
        rootTag = 'CarrierPickupInquiryResponse'
        rootClass = CarrierPickupInquiryResponse
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
        rootTag = 'CarrierPickupInquiryResponse'
        rootClass = CarrierPickupInquiryResponse
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
        rootTag = 'CarrierPickupInquiryResponse'
        rootClass = CarrierPickupInquiryResponse
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
        rootTag = 'CarrierPickupInquiryResponse'
        rootClass = CarrierPickupInquiryResponse
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from carrier_pickup_inquiry_response import *\n\n')
        sys.stdout.write('import carrier_pickup_inquiry_response as model_\n\n')
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
    "CarrierPickupInquiryResponse",
    "PackageType"
]
