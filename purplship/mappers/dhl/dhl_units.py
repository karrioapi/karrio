from enum import Enum


class DHLUnit:

    class Dimension(Enum):
        CM  =    "C" 
        IN  =    "I"

    class DeliveryType(Enum):
        Door_to_Door         =    "DD" 
        Door_to_Airport      =    "DA" 
        Airport_to_Airport   =    "AA"  
        Door_to_Door_C       =    "DC" 

    class DCTPackageTypeCode(Enum):
        Flyer_Smalls         =    "FLY" 
        Parcels_Conveyables  =    "COY" 
        Non_conveyables      =    "NCY" 
        Pallets              =    "PAL" 
        Double_Pallets       =    "DBL" 
        Parcels              =    "BOX"  
    
    class PackageTypeCode(Enum):
        Jumbo_Document        =    "BD"
        Jumbo_Parcel          =    "BP"
        Customer_provided     =    "CP"
        Document              =    "DC"
        DHL_Flyer             =    "DF"
        Domestic              =    "DM"
        Express_Document      =    "ED"
        DHL_Express_Envelope  =    "EE"
        Freight               =    "FR"
        Jumbo_box             =    "JB"
        Jumbo_Junior_Document =    "JD"
        Junior_jumbo_Box      =    "JJ"
        Jumbo_Junior_Parcel   =    "JP"
        Other_DHL_Packaging   =    "OD"
        Parcel                =    "PA"
        Your_packaging        =    "YP"

    class ProductCode(Enum):
        LOGISTICS_SERVICES      =    "0"
        DOMESTIC_EXPRESS_12_00  =    "1"
        # B2C                     =    "2"
        B2C                     =    "3"
        JETLINE                 =    "4"
        SPRINTLINE              =    "5"
        # EXPRESS_EASY            =    "7"
        EXPRESS_EASY            =    "8"
        EUROPACK                =    "9"
        AUTO_REVERSALS          =    "A"
        BREAKBULK_EXPRESS       =    "B"
        MEDICAL_EXPRESS         =    "C"
        EXPRESS_WORLDWIDE       =    "D"
        EXPRESS_9_00            =    "E"
        FREIGHT_WORLDWIDE       =    "F"
        DOMESTIC_ECONOMY_SELECT =    "G"
        ECONOMY_SELECT          =    "H"
        DOMESTIC_EXPRESS_9_00   =    "I"
        JUMBO_BOX               =    "J"
        EXPRESS_9_00            =    "K"
        # EXPRESS_10_30           =    "L"
        EXPRESS_10_30           =    "M"
        DOMESTIC_EXPRESS        =    "N"
        DOMESTIC_EXPRESS_10_30  =    "O"
        EXPRESS_WORLDWIDE       =    "P"
        MEDICAL_EXPRESS         =    "Q"
        GLOBALMAIL_BUSINESS     =    "R"
        SAME_DAY                =    "S"
        EXPRESS_12_00           =    "T"
        EXPRESS_WORLDWIDE       =    "U"
        EUROPACK                =    "V"
        ECONOMY_SELECT          =    "W"
        EXPRESS_ENVELOPE        =    "X"
        EXPRESS_12_00           =    "Y"
        Destination_Charges     =    "Z"

    class WeightUnit(Enum):
        KG  =     "K"
        LB  =     "L"

