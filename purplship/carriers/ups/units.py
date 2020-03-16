from enum import Enum, Flag


class WeightUnit(Enum):
    KG = "KGS"
    LB = "LBS"


class PackagingType(Flag):
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
    package = "PKG"
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
    sm = wrapped
    pc = pieces
    pal = pallet


class RatingPackagingType(Flag):
    unknown = "00"
    ups_letter = "01"
    package = "02"
    tube = "03"
    pak = "04"
    express_box = "21"
    box_25_kg = "24"
    box_10_kg = "25"
    pallet = "30"
    small_express_box = "2a"
    medium_express_box = "2b"
    large_express_box = "2c"

    """ unified Packaging type mapping  """
    sm = ups_letter
    box = express_box
    pc = package
    pal = pallet


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
    customer_supplied_package = "02"
    tube = "03"
    pak = "04"
    ups_express_box = "21"
    ups_25_kg_box = "24"
    ups_10_kg_box = "25"
    pallet = "30"
    small_express_box = "2a"
    medium_express_box = "2b"
    large_express_box = "2c"
    flats = "56"
    parcels = "57"
    bpm = "58"
    first_class = "59"
    priority = "60"
    machineables = "61"
    irregulars = "62"
    parcel_post = "63"
    bpm_parcel = "64"
    media_mail = "65"
    bpm_flat = "66"
    standard_flat = "67"

    """ unified Packaging type mapping  """
    sm = ups_letter
    box = ups_express_box
    pc = pak
    pal = pallet


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
