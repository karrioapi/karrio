"""PurplShip Australia Post domain"""

from enum import Enum


class Service(Enum):
    AUS_LETTER_REGULAR_LARGE = "Large Letter"
    AUS_LETTER_EXPRESS_SMALL = "Express Post Small Envelope"
    AUS_PARCEL_REGULAR = "Parcel Post"
    AUS_PARCEL_REGULAR_SATCHEL_3KG = "Parcel Post Medium (3Kg) Satchel"
    AUS_PARCEL_EXPRESS = "Express Post"
    AUS_PARCEL_EXPRESS_SATCHEL_3KG = "Express Post Medium (3Kg) Satchel"


class Option(Enum):
    AUS_SERVICE_OPTION_REGISTERED_POST = "Registered Post"
    AUS_SERVICE_OPTION_COD_POSTAGE_FEES = "C.O.D - Postage & Fees"
    AUS_SERVICE_OPTION_COD_MONEY_COLLECTION = "C.O.D - Money Collection, Postage & Fees"
    AUS_SERVICE_OPTION_STANDARD = "Standard Service"
    AUS_SERVICE_OPTION_SIGNATURE_ON_DELIVERY = "Signature on Delivery"
