"""PurplShip Australia Post domain"""
import attr
from enum import Enum, Flag


@attr.s(auto_attribs=True)
class Template:
    width: float  # CM
    height: float  # CM
    length: float = None  # CM


class PostagePackageTemplate(Flag):
    aus_letter_size_dl = Template(width=11.0, height=22.0)
    aus_letter_size_c6 = Template(width=11.4, height=16.2)
    aus_letter_size_c5 = Template(width=16.2, height=22.9)
    aus_letter_size_c4 = Template(width=32.4, height=22.9)
    aus_letter_size_b4 = Template(width=35.3, height=25.0)
    aus_parcel_type_boxed_bc = Template(width=22.0, height=16.0, length=7.7)
    aus_parcel_type_boxed_bm = Template(width=31.0, height=22.5, length=10.2)
    aus_parcel_type_boxed_bp = Template(width=40.0, height=20.0, length=18.0)
    aus_parcel_type_boxed_bt = Template(width=43.0, height=30.5, length=14.0)
    aus_parcel_type_boxed_bw = Template(width=40.5, height=30.0, length=25.5)
    aus_parcel_type_boxed_vcb = Template(width=22.0, height=14.5, length=3.5)
    aus_parcel_type_boxed_cd = Template(width=14.5, height=12.7, length=1.0)
    aus_parcel_type_boxed_toughpak = Template(width=36.3, height=21.2, length=6.5)


class PostagePackagingType(Flag):
    aus_letter_size_dl = "AUS_LETTER_SIZE_DL"
    aus_letter_size_c6 = "AUS_LETTER_SIZE_C6"
    aus_letter_size_c5 = "AUS_LETTER_SIZE_C5"
    aus_letter_size_c4 = "AUS_LETTER_SIZE_C4"
    aus_letter_size_b4 = "AUS_LETTER_SIZE_B4"
    aus_letter_size_oth = "AUS_LETTER_SIZE_OTH"
    aus_parcel_type_boxed_bc = "AUS_PARCEL_TYPE_BOXED_BC"
    aus_parcel_type_boxed_bm = "AUS_PARCEL_TYPE_BOXED_BM"
    aus_parcel_type_boxed_bp = "AUS_PARCEL_TYPE_BOXED_BP"
    aus_parcel_type_boxed_bt = "AUS_PARCEL_TYPE_BOXED_BT"
    aus_parcel_type_boxed_bw = "AUS_PARCEL_TYPE_BOXED_BW"
    aus_parcel_type_boxed_vcb = "AUS_PARCEL_TYPE_BOXED_VCB"
    aus_parcel_type_boxed_cd = "AUS_PARCEL_TYPE_BOXED_CD"
    aus_parcel_type_boxed_toughpak = "AUS_PARCEL_TYPE_BOXED_TOUGHPAK"
    aus_my_own_box = "AUS_PARCEL_TYPE_BOXED_OTH"

    """ Unified Packaging type mapping """
    # envelope = aus_envelope
    # pak = aus_satchel
    # tube = aus_item
    # pallet = aus_pallet
    # small_box = aus_bag
    # medium_box = aus_jiffy_bag
    # large_box = aus_skid_up_to_500_kg
    # your_packaging = aus_my_own_box


class PackagingType(Flag):
    aus_carton = "CTN"
    aus_pallet = "PAL"
    aus_satchel = "SAT"
    aus_bag = "BAG"
    aus_envelope = "ENV"
    aus_item = "ITM"
    aus_jiffy_bag = "JIF"
    aus_skid_up_to_500_kg = "SKI"

    """ Unified Packaging type mapping """
    envelope = aus_envelope
    pak = aus_satchel
    tube = aus_item
    pallet = aus_pallet
    small_box = aus_bag
    medium_box = aus_bag
    large_box = aus_skid_up_to_500_kg
    your_packaging = aus_carton


class ShipmentFeature(Enum):
    aus_delivery_date = "DELIVERY_DATE"
    aus_delivery_times = "DELIVERY_TIMES"
    aus_pickup_date = "PICKUP_DATE"
    aus_pickup_time = "PICKUP_TIME"
    aus_commercial_clearance = "COMMERCIAL_CLEARANCE"
    aus_identity_on_delivery = "IDENTITY_ON_DELIVERY"
    aus_print_at_depot = "PRINT_AT_DEPOT"


class PostageService(Enum):
    aus_large_letter = "AUS_LETTER_REGULAR_LARGE"
    aus_express_post_small_envelope = "AUS_LETTER_EXPRESS_SMALL"
    aus_parcel_post = "AUS_PARCEL_REGULAR"
    aus_parcel_post_medium_3_kg_satchel = "AUS_PARCEL_REGULAR_SATCHEL_3KG"
    aus_express_post = "AUS_PARCEL_EXPRESS"
    aus_express_post_medium_3_kg_satchel = "AUS_PARCEL_EXPRESS_SATCHEL_3KG"


class Option(Enum):
    aus_standard_service = "AUS_SERVICE_OPTION_STANDARD"
    aus_registered_post = "AUS_SERVICE_OPTION_REGISTERED_POST"
    aus_c_o_d_postage_fees = "AUS_SERVICE_OPTION_COD_POSTAGE_FEES"
    aus_c_o_d_money_collection_postage_fees = "AUS_SERVICE_OPTION_COD_MONEY_COLLECTION"
    aus_signature_on_delivery = "AUS_SERVICE_OPTION_SIGNATURE_ON_DELIVERY"
