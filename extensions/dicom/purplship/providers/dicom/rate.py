from typing import List, Tuple, Dict
from pydicom.rate import (
    RateRequest as DicomRateRequest,
    RateResponse,
    Address,
    Parcel,
    Appointment
)
from purplship.core.models import (
    RateRequest,
    RateDetails,
    Message
)
from purplship.core.utils import (
    Serializable
)
from purplship.core.units import Packages
from purplship.providers.dicom.error import parse_error_response
from purplship.providers.dicom.utils import Settings


def parse_rate_response(response: dict, settings: Settings) -> Tuple[List[RateDetails], List[Message]]:
    pass


def create_rate_request(payload: RateRequest, settings: Settings) -> Serializable[DicomRateRequest]:
    packages = Packages(payload.parcels)

    request = DicomRateRequest(
        category="Parcel",
        paymentType="Prepaid",
        deliveryType="GRD",
        unitOfMeasurement="K",
        sender=Address(
            postalCode=payload.shipper.postal_code,
            provinceCode=payload.shipper.state_code,
            number=None,
            countryCode=payload.shipper.country_code,
            name=payload.shipper.company_name
        ),
        consignee=Address(
            postalCode=payload.recipient.postal_code,
            provinceCode=payload.recipient.state_code,
            number=None,
            countryCode=payload.recipient.country_code,
            name=payload.recipient.company_name
        ),
        parcels=[
            Parcel(
                quantity=1,
                parcelType=None,
                weight=None,
                length=None,
                depth=None,
                width=None,
                note=None,
                status=None,
                FCAClass=None,
                hazmat=None,
                requestReturnLabel=None,
                returnWaybill=None,
            )
            for pck in packages
        ],
        billing=None,
        promoCodes=[],
        surcharges=[],
        appointment=None
    )

    return Serializable(request)
