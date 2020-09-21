from typing import List, Tuple
from purplship.package.mapper import Mapper as BaseMapper
from purplship.core.models import (
    ShipmentRequest,
    TrackingRequest,
    Message,
    TrackingDetails,
    RateDetails,
    RateRequest,
    ShipmentDetails,
)
from purplship.package.mappers.dicom.settings import Settings


class Mapper(BaseMapper):
    settings: Settings
