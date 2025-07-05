"""
Veho Tracking Request Schema based on OpenAPI spec
"""

import attr
import typing


@attr.s(auto_attribs=True)
class TrackingRequest:
    """Veho Tracking Request - for tracking by package ID or barcode"""
    
    # For tracking by package ID
    package_id: typing.Optional[str] = None
    
    # For tracking by barcode
    barcode: typing.Optional[str] = None
    
    # Optional parameter to include delivery image
    include_delivery_image: typing.Optional[bool] = False 
