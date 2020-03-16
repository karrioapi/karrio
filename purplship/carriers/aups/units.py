"""PurplShip Australia Post domain"""

from enum import Enum


class Service(Enum):
    aus_letter_regular_large = "Large Letter"
    aus_letter_express_small = "Express Post Small Envelope"
    aus_parcel_regular = "Parcel Post"
    aus_parcel_regular_satchel_3_kg = "Parcel Post Medium (3Kg) Satchel"
    aus_parcel_express = "Express Post"
    aus_parcel_express_satchel_3_kg = "Express Post Medium (3Kg) Satchel"


class Option(Enum):
    aus_service_option_registered_post = "Registered Post"
    aus_service_option_cod_postage_fees = "C.O.D - Postage & Fees"
    aus_service_option_cod_money_collection = "C.O.D - Money Collection, Postage & Fees"
    aus_service_option_standard = "Standard Service"
    aus_service_option_signature_on_delivery = "Signature on Delivery"
