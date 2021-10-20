from purplship.core.utils import Enum, Flag, Spec
from purplship.core.units import PackagePreset

PRESET_DEFAULTS = dict(dimension_unit="IN", weight_unit="LB")


class PackagePresets(Flag):
    ups_small_express_box = PackagePreset(
        **dict(weight=30.0, width=13.0, height=11.0, length=2.0), **PRESET_DEFAULTS
    )
    ups_medium_express_box = PackagePreset(
        **dict(weight=30.0, width=16.0, height=11.0, length=3.0), **PRESET_DEFAULTS
    )
    ups_large_express_box = PackagePreset(
        **dict(weight=30.0, width=18.0, height=13.0, length=3.0), **PRESET_DEFAULTS
    )
    ups_express_tube = PackagePreset(
        **dict(width=38.0, height=6.0, length=6.0), **PRESET_DEFAULTS
    )
    ups_express_pak = PackagePreset(
        **dict(width=16.0, height=11.75, length=1.5), **PRESET_DEFAULTS
    )
    ups_world_document_box = PackagePreset(
        **dict(width=17.5, height=12.5, length=3.0), **PRESET_DEFAULTS
    )


class LabelType(Flag):
    PDF_6x4 = ("GIF", 6, 4)
    PDF_8x4 = ("GIF", 8, 4)
    ZPL_6x4 = ("ZPL", 6, 4)

    """ Unified Label type mapping """
    PDF = PDF_6x4
    ZPL = ZPL_6x4


class Incoterm(Enum):
    CFR = "Cost and Freight"
    CIF = "Cost Insurance and Freight"
    CIP = "Carriage and Insurance Paid"
    CPT = "Carriage Paid To"
    DAF = "Delivered at Frontier"
    DDP = "Delivery Duty Paid"
    DDU = "Delivery Duty Unpaid"
    DEQ = "Delivered Ex Quay"
    DES = "Delivered Ex Ship"
    EXW = "Ex Works"
    FAS = "Free Alongside Ship"
    FCA = "Free Carrier"
    FOB = "Free On Board"


class WeightUnit(Enum):
    KG = "KGS"
    LB = "LBS"


class PackagingType(Flag):
    ups_freight_bag = "BAG"
    ups_freight_bale = "BAL"
    ups_freight_barrel = "BAR"
    ups_freight_bundle = "BDL"
    ups_freight_bin = "BIN"
    ups_freight_box = "BOX"
    ups_freight_basket = "BSK"
    ups_freight_bunch = "BUN"
    ups_freight_cabinet = "CAB"
    ups_freight_can = "CAN"
    ups_freight_carrier = "CAR"
    ups_freight_case = "CAS"
    ups_freight_carboy = "CBY"
    ups_freight_container = "CON"
    ups_freight_crate = "CRT"
    ups_freight_cask = "CSK"
    ups_freight_carton = "CTN"
    ups_freight_cylinder = "CYL"
    ups_freight_drum = "DRM"
    ups_freight_loose = "LOO"
    ups_freight_other = "OTH"
    ups_freight_pail = "PAL"
    ups_freight_pieces = "PCS"
    ups_freight_package = "PKG"  # equivalent of user custom packaging
    ups_freight_pipe_line = "PLN"
    ups_freight_pallet = "PLT"
    ups_freight_rack = "RCK"
    ups_freight_reel = "REL"
    ups_freight_roll = "ROL"
    ups_freight_skid = "SKD"
    ups_freight_spool = "SPL"
    ups_freight_tube = "TBE"
    ups_freight_tank = "TNK"
    ups_freight_unit = "UNT"
    ups_freight_van_pack = "VPK"
    ups_freight_wrapped = "WRP"

    """ unified Packaging type mapping  """
    envelope = ups_freight_other
    pak = ups_freight_other
    tube = ups_freight_cylinder
    pallet = ups_freight_pallet
    small_box = ups_freight_box
    medium_box = ups_freight_box
    your_packaging = ups_freight_box


class ServiceCode(Enum):
    ups_freight_ltl = "308"
    ups_freight_ltl_guaranteed = "309"
    ups_freight_ltl_guaranteed_am = "334"
    ups_standard_ltl = "349"


class ServiceOption(Enum):
    ups_negotiated_rates_indicator = Spec.asFlag("NegotiatedRatesIndicator")
    ups_frs_shipment_indicator = Spec.asFlag("FRSShipmentIndicator")
    ups_rate_chart_indicator = Spec.asFlag("RateChartIndicator")
    ups_user_level_discount_indicator = Spec.asFlag("UserLevelDiscountIndicator")
    ups_saturday_delivery_indicator = Spec.asFlag("SaturdayDeliveryIndicator")
    ups_access_point_cod = Spec.asValue("AccessPointCOD", float)
    ups_deliver_to_addressee_only_indicator = Spec.asFlag(
        "DeliverToAddresseeOnlyIndicator"
    )
    ups_direct_delivery_only_indicator = Spec.asFlag("DirectDeliveryOnlyIndicator")
    ups_cod = Spec.asValue("COD", float)
    ups_delivery_confirmation = Spec.asFlag("DeliveryConfirmation")
    ups_return_of_document_indicator = Spec.asFlag("ReturnOfDocumentIndicator")
    ups_carbonneutral_indicator = Spec.asFlag("UPScarbonneutralIndicator")
    ups_certificate_of_origin_indicator = Spec.asFlag("CertificateOfOriginIndicator")
    ups_pickup_options = Spec.asFlag("PickupOptions")
    ups_delivery_options = Spec.asFlag("DeliveryOptions")
    ups_restricted_articles = Spec.asFlag("RestrictedArticles")
    ups_shipper_export_declaration_indicator = Spec.asFlag(
        "ShipperExportDeclarationIndicator"
    )
    ups_commercial_invoice_removal_indicator = Spec.asFlag(
        "CommercialInvoiceRemovalIndicator"
    )
    ups_import_control = Spec.asFlag("ImportControl")
    ups_return_service = Spec.asFlag("ReturnService")
    ups_sdl_shipment_indicator = Spec.asFlag("SDLShipmentIndicator")
    ups_epra_indicator = Spec.asFlag("EPRAIndicator")

    """ Unified Option type mapping """
    cash_on_delivery = ups_cod


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
