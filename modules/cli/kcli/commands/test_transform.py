#!/usr/bin/env python3
"""
Test script to verify the transform function is working correctly.
"""

import sys
from codegen import transform_content

# Sample input (dataclasses-style)
sample_input = """from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Item:
    dangerous: Optional[bool] = None
    height: Optional[int] = None
    itemCount: Optional[int] = None
    length: Optional[int] = None
    volume: Optional[float] = None
    weight: Optional[int] = None
    width: Optional[int] = None


@dataclass
class GeographicAddress:
    address1: Optional[str] = None
    address2: Optional[str] = None
    country: Optional[str] = None
    postCode: Optional[int] = None
    state: Optional[str] = None
    suburb: Optional[str] = None


@dataclass
class JobStops:
    companyName: Optional[str] = None
    contact: Optional[str] = None
    emailAddress: Optional[str] = None
    geographicAddress: Optional[GeographicAddress] = None
    phoneNumber: Optional[str] = None


@dataclass
class LabelRequest:
    bookedBy: Optional[str] = None
    account: Optional[str] = None
    instructions: Optional[str] = None
    itemCount: Optional[int] = None
    items: Optional[List[Item]] = None
    jobStopsP: Optional[JobStops] = None
    jobStopsD: Optional[JobStops] = None
    referenceNumbers: Optional[List[str]] = None
    serviceLevel: Optional[str] = None
    volume: Optional[float] = None
    weight: Optional[int] = None
"""

# Transform the sample input
transformed = transform_content(sample_input)

# Print the transformed output
print(transformed)

# Expected output will have:
# 1. import attr, import jstruct, import typing
# 2. @attr.s(auto_attribs=True) decorators
# 3. typing.Optional and typing.List annotations
# 4. jstruct.JStruct and jstruct.JList for complex types
