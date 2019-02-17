from enum import Enum, Flag


class PackagingType(Flag):
    Bag = "BAG"
    Bale = "BAL"
    Barrel = "BAR"
    Bundle = "BDL"
    Bin = "BIN"
    Box = "BOX"
    Basket = "BSK"
    Bunch = "BUN"
    Cabinet = "CAB"
    Can = "CAN"
    Carrier = "CAR"
    Case = "CAS"
    Carboy = "CBY"
    Container = "CON"
    Crate = "CRT"
    Cask = "CSK"
    Carton = "CTN"
    Cylinder = "CYL"
    Drum = "DRM"
    Loose = "LOO"
    Other = "OTH"
    Pail = "PAL"
    Pieces = "PCS"
    Package = "PKG"
    Pipe_Line = "PLN"
    Pallet = "PLT"
    Rack = "RCK"
    Reel = "REL"
    Roll = "ROL"
    Skid = "SKD"
    Spool = "SPL"
    Tube = "TBE"
    Tank = "TNK"
    Unit = "UNT"
    Van_Pack = "VPK"
    Wrapped = "WRP"

    """ unified Packaging type mapping  """
    SM = Wrapped
    BOX = Box
    PC = Pieces
    PAL = Pallet


class RatingPackagingType(Flag):
    UNKNOWN = "00"
    UPS_Letter = "01"
    Package = "02"
    Tube = "03"
    Pak = "04"
    Express_Box = "21"
    Box_25KG = "24"
    Box_10KG = "25"
    Pallet = "30"
    Small_Express_Box = "2a"
    Medium_Express_Box = "2b"
    Large_Express_Box = "2c"

    """ unified Packaging type mapping  """
    SM = UPS_Letter
    BOX = Express_Box
    PC = Package
    PAL = Pallet


class RatingServiceCode(Enum):
    UPS_Standard = "11"
    UPS_Worldwide_Express = "07"
    UPS_Worldwide_Expedited = "08"
    UPS_Worldwide_Express_Plus = "54"
    UPS_Worldwide_Saver = "65"
    UPS_2nd_Day_Air = "02"
    UPS_2nd_Day_Air_A_M = "59"
    UPS_3_Day_Select = "12"
    UPS_Ground = "03"
    UPS_Next_Day_Air = "01"
    UPS_Next_Day_Air_Early = "14"
    UPS_Next_Day_Air_Saver = "13"
    UPS_Expedited = "02"
    UPS_Express_Saver_CA = "13"
    UPS_Access_Point_Economy = "70"
    UPS_Express = "01"
    UPS_Express_Early_CA = "14"
    UPS_Express_Saver = "65"
    UPS_Express_Early = "54"
    UPS_Expedited_EU = "08"
    UPS_Express_EU = "07"
    UPS_Today_Dedicated_Courrier = "83"
    UPS_Today_Express = "85"
    UPS_Today_Express_Saver = "86"
    UPS_Today_Standard = "82"
    UPS_Express_Plus = "54"
    UPS_Worldwide_Express_Freight = "96"
    UPS_Freight_LTL = "308"
    UPS_Freight_LTL_Guaranteed = "309"
    UPS_Freight_LTL_Guaranteed_A_M = "334"
    UPS_Standard_LTL = "349"


class RatingOption(Enum):
    NegotiatedRatesIndicator = "NegotiatedRatesIndicator"
    FRSShipmentIndicator = "FRSShipmentIndicator"
    RateChartIndicator = "RateChartIndicator"
    UserLevelDiscountIndicator = "UserLevelDiscountIndicator"


class ShippingPackagingType(Flag):
    UPS_Letter = "01"
    Customer_Supplied_Package = "02"
    Tube = "03"
    PAK = "04"
    UPS_Express_Box = "21"
    UPS_25KG_Box = "24"
    UPS_10KG_Box = "25"
    Pallet = "30"
    Small_Express_Box = "2a"
    Medium_Express_Box = "2b"
    Large_Express_Box = "2c"
    Flats = "56"
    Parcels = "57"
    BPM = "58"
    First_Class = "59"
    Priority = "60"
    Machineables = "61"
    Irregulars = "62"
    Parcel_Post = "63"
    BPM_Parcel = "64"
    Media_Mail = "65"
    BPM_Flat = "66"
    Standard_Flat = "67"

    """ unified Packaging type mapping  """
    SM = UPS_Letter
    BOX = UPS_Express_Box
    PC = PAK
    PAL = Pallet


class ShippingServiceCode(Enum):
    UPS_Standard = "11"
    UPS_Worldwide_Expedited = "08"
    UPS_Worldwide_Express = "07"
    UPS_Worldwide_Express_Plus = "54"
    UPS_Worldwide_Saver = "65"
    UPS_2nd_Day_Air = "02"
    UPS_2nd_Day_Air_A_M = "59"
    UPS_3_Day_Select = "12"
    UPS_Expedited_Mail_Innovations = "M4"
    UPS_First_Class_Mail = "M2"
    UPS_Ground = "03"
    UPS_Next_Day_Air = "01"
    UPS_Next_Day_Air_Early = "14"
    UPS_Next_Day_Air_Saver = "13"
    UPS_Priority_Mail = "M3"
    UPS_Expedited = "02"
    UPS_Express_Saver_CA = "13"
    UPS_Access_Point_Economy = "70"
    UPS_Express = "01"
    UPS_Express_Early_CA = "14"
    UPS_Express_Saver = "65"
    UPS_Express_Early = "54"
    UPS_Expedited_EU = "08"
    UPS_Express_EU = "07"
    UPS_Express_Plus = "54"
    UPS_Today_Dedicated_Courier = "83"
    UPS_Today_Express = "85"
    UPS_Today_Express_Saver = "86"
    UPS_Today_Standard = "82"
    UPS_Worldwide_Express_Freight = "96"
    UPS_Priority_Mail_Innovations = "M5"
    UPS_Economy_Mail_Innovations = "M6"


class ServiceOption(Enum):
    SaturdayDeliveryIndicator = "SaturdayDeliveryIndicator"
    AccessPointCOD = "AccessPointCOD"
    DeliverToAddresseeOnlyIndicator = "DeliverToAddresseeOnlyIndicator"
    DirectDeliveryOnlyIndicator = "DirectDeliveryOnlyIndicator"
    COD = "COD"
    DeliveryConfirmation = "DeliveryConfirmation"
    ReturnOfDocumentIndicator = "ReturnOfDocumentIndicator"
    UPScarbonneutralIndicator = "UPScarbonneutralIndicator"
    CertificateOfOriginIndicator = "CertificateOfOriginIndicator"
    PickupOptions = "PickupOptions"
    DeliveryOptions = "DeliveryOptions"
    RestrictedArticles = "RestrictedArticles"
    ShipperExportDeclarationIndicator = "ShipperExportDeclarationIndicator"
    CommercialInvoiceRemovalIndicator = "CommercialInvoiceRemovalIndicator"
    ImportControl = "ImportControl"
    ReturnService = "ReturnService"
    SDLShipmentIndicator = "SDLShipmentIndicator"
    EPRAIndicator = "EPRAIndicator"


class WeightUnit(Enum):
    KG = "KGS"
    LB = "LBS"
