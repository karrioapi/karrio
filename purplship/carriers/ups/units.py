import attr
from enum import Enum, Flag


@attr.s(auto_attribs=True)
class Template:
    width: float  # IN
    height: float  # IN
    length: float = None  # IN
    depth: float = None  # IN
    weight: float = None  # LB


class PackageTemplate(Flag):
    ups_small_express_box = Template(weight=30, width=13, height=11, length=2)
    ups_medium_express_box = Template(weight=30, width=16, height=11, length=3)
    ups_large_express_box = Template(weight=30, width=18, height=13, length=3)
    ups_express_tube = Template(width=38, height=6, length=6, depth=6)
    ups_express_pak = Template(width=16, height=11.75)
    ups_world_document_box = Template(width=17.5, height=12.5, length=3)


class WeightUnit(Enum):
    KG = "KGS"
    LB = "LBS"


class FreightPackagingType(Flag):
    bag = "BAG"
    bale = "BAL"
    barrel = "BAR"
    bundle = "BDL"
    bin = "BIN"
    box = "BOX"
    basket = "BSK"
    bunch = "BUN"
    cabinet = "CAB"
    can = "CAN"
    carrier = "CAR"
    case = "CAS"
    carboy = "CBY"
    container = "CON"
    crate = "CRT"
    cask = "CSK"
    carton = "CTN"
    cylinder = "CYL"
    drum = "DRM"
    loose = "LOO"
    other = "OTH"
    pail = "PAL"
    pieces = "PCS"
    package = "PKG"  # equivalent of user custom packaging
    pipe_line = "PLN"
    pallet = "PLT"
    rack = "RCK"
    reel = "REL"
    roll = "ROL"
    skid = "SKD"
    spool = "SPL"
    tube = "TBE"
    tank = "TNK"
    unit = "UNT"
    van_pack = "VPK"
    wrapped = "WRP"

    """ unified Packaging type mapping  """
    envelope = package
    pak = van_pack
    small_box = box
    medium_box = box
    your_packaging = package


class RatingPackagingType(Flag):
    ups_unknown = "00"
    ups_letter = "01"
    ups_package = "02"  # equivalent of user custom packaging
    ups_tube = "03"
    ups_pak = "04"
    ups_express_box = "21"
    ups_box_25_kg = "24"
    ups_box_10_kg = "25"
    ups_pallet = "30"
    ups_small_express_box = "2a"
    ups_medium_express_box = "2b"
    ups_large_express_box = "2c"

    """ unified Packaging type mapping  """
    envelope = ups_letter
    pak = ups_pak
    tube = ups_tube
    pallet = ups_pallet
    small_box = ups_small_express_box
    medium_box = ups_medium_express_box
    your_packaging = ups_package


class RatingServiceCode(Enum):
    ups_standard = "11"
    ups_worldwide_express = "07"
    ups_worldwide_expedited = "08"
    ups_worldwide_express_plus = "54"
    ups_worldwide_saver = "65"
    ups_2nd_day_air = "02"
    ups_2nd_day_air_a_m = "59"
    ups_3_day_select = "12"
    ups_ground = "03"
    ups_next_day_air = "01"
    ups_next_day_air_early = "14"
    ups_next_day_air_saver = "13"
    ups_expedited = "02"
    ups_express_saver_ca = "13"
    ups_access_point_economy = "70"
    ups_express = "01"
    ups_express_early_ca = "14"
    ups_express_saver = "65"
    ups_express_early = "54"
    ups_expedited_eu = "08"
    ups_express_eu = "07"
    ups_today_dedicated_courrier = "83"
    ups_today_express = "85"
    ups_today_express_saver = "86"
    ups_today_standard = "82"
    ups_express_plus = "54"
    ups_worldwide_express_freight = "96"
    ups_freight_ltl = "308"
    ups_freight_ltl_guaranteed = "309"
    ups_freight_ltl_guaranteed_a_m = "334"
    ups_standard_ltl = "349"


class RatingOption(Enum):
    negotiated_rates_indicator = "NegotiatedRatesIndicator"
    frs_shipment_indicator = "FRSShipmentIndicator"
    rate_chart_indicator = "RateChartIndicator"
    user_level_discount_indicator = "UserLevelDiscountIndicator"


class ShippingPackagingType(Flag):
    ups_letter = "01"
    ups_customer_supplied_package = "02"
    ups_tube = "03"
    ups_pak = "04"
    ups_ups_express_box = "21"
    ups_ups_25_kg_box = "24"
    ups_ups_10_kg_box = "25"
    ups_pallet = "30"
    ups_small_express_box = "2a"
    ups_medium_express_box = "2b"
    ups_large_express_box = "2c"
    ups_flats = "56"
    ups_parcels = "57"
    ups_bpm = "58"
    ups_first_class = "59"
    ups_priority = "60"
    ups_machineables = "61"
    ups_irregulars = "62"
    ups_parcel_post = "63"
    ups_bpm_parcel = "64"
    ups_media_mail = "65"
    ups_bpm_flat = "66"
    ups_standard_flat = "67"

    """ unified Packaging type mapping  """
    envelope = ups_letter
    pak = ups_pak
    tube = ups_tube
    pallet = ups_pallet
    small_box = ups_small_express_box
    medium_box = ups_medium_express_box
    your_packaging = ups_customer_supplied_package


class ShippingServiceCode(Enum):
    ups_standard = "11"
    ups_worldwide_expedited = "08"
    ups_worldwide_express = "07"
    ups_worldwide_express_plus = "54"
    ups_worldwide_saver = "65"
    ups_2nd_day_air = "02"
    ups_2nd_day_air_a_m = "59"
    ups_3_day_select = "12"
    ups_expedited_mail_innovations = "M4"
    ups_first_class_mail = "M2"
    ups_ground = "03"
    ups_next_day_air = "01"
    ups_next_day_air_early = "14"
    ups_next_day_air_saver = "13"
    ups_priority_mail = "M3"
    ups_expedited = "02"
    ups_express_saver_ca = "13"
    ups_access_point_economy = "70"
    ups_express = "01"
    ups_express_early_ca = "14"
    ups_express_saver = "65"
    ups_express_early = "54"
    ups_expedited_eu = "08"
    ups_express_eu = "07"
    ups_express_plus = "54"
    ups_today_dedicated_courier = "83"
    ups_today_express = "85"
    ups_today_express_saver = "86"
    ups_today_standard = "82"
    ups_worldwide_express_freight = "96"
    ups_priority_mail_innovations = "M5"
    ups_economy_mail_innovations = "M6"


class ServiceOption(Enum):
    saturday_delivery_indicator = "SaturdayDeliveryIndicator"
    access_point_cod = "AccessPointCOD"
    deliver_to_addressee_only_indicator = "DeliverToAddresseeOnlyIndicator"
    direct_delivery_only_indicator = "DirectDeliveryOnlyIndicator"
    cod = "COD"
    delivery_confirmation = "DeliveryConfirmation"
    return_of_document_indicator = "ReturnOfDocumentIndicator"
    up_scarbonneutral_indicator = "UPScarbonneutralIndicator"
    certificate_of_origin_indicator = "CertificateOfOriginIndicator"
    pickup_options = "PickupOptions"
    delivery_options = "DeliveryOptions"
    restricted_articles = "RestrictedArticles"
    shipper_export_declaration_indicator = "ShipperExportDeclarationIndicator"
    commercial_invoice_removal_indicator = "CommercialInvoiceRemovalIndicator"
    import_control = "ImportControl"
    return_service = "ReturnService"
    sdl_shipment_indicator = "SDLShipmentIndicator"
    epra_indicator = "EPRAIndicator"


class FreightClass(Enum):
    ups_freight_class_50 = 50
    ups_freight_class_55 = 55
    ups_freight_class_60 = 60
    ups_freight_class_65 = 65
    ups_freight_class_70 = 70
    ups_freight_class_77_5 = 77.5
    ups_freight_class_85 = 85
    ups_freight_class_92_5 = 92.5
    ups_freight_class_100 = 100
    ups_freight_class_110 = 110
    ups_freight_class_125 = 125
    ups_freight_class_150 = 150
    ups_freight_class_175 = 175
    ups_freight_class_200 = 200
    ups_freight_class_250 = 250
    ups_freight_class_300 = 300
    ups_freight_class_400 = 400
    ups_freight_class_500 = 500
