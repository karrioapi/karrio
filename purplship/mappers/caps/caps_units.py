from enum import Enum


class CanadaPostUnit:

    class ServiceType(Enum):
        DOM_RP         =    'DOM.RP'
        DOM_EP         =    'DOM.EP'	
        DOM_XP         =    'DOM.XP'
        DOM_XP_CERT    =    'DOM.XP.CERT'
        DOM_PC         =    'DOM.PC'
        DOM_LIB        =    'DOM.LIB'
        USA_EP         =    'USA.EP'
        USA_PW_ENV     =    'USA.PW.ENV'
        USA_PW_PAK     =    'USA.PW.PAK'
        USA_PW_PARCEL  =    'USA.PW.PARCEL'
        USA_SP_AIR     =    'USA.SP.AIR'
        USA_TP         =    'USA.TP'
        USA_TP_LVM     =    'USA.TP.LVM'
        USA_XP         =    'USA.XP'
        INT_XP         =    'INT.XP'
        INT_IP_AIR     =    'INT.IP.AIR'
        INT_IP_SURF    =    'INT.IP.SURF'
        INT_PW_ENV     =    'INT.PW.ENV'
        INT_PW_PAK     =    'INT.PW.PAK'
        INT_PW_PARCEL  =    'INT.PW.PARCEL'
        INT_SP_AIR     =    'INT.SP.AIR'
        INT_SP_SURF    =    'INT.SP.SURF'
        INT_TP         =    'INT.TP'

    class OptionCode(Enum):
        Signature                       =    "SO" 
        Coverage                        =    "COV"  
        COD                             =    "COD" 
        Proof_of_Age_Required_18        =    "PA18"  
        Proof_of_Age_Required_19        =    "PA19"  
        Card_for_pickup                 =    "HFP" 
        Do_not_safe_drop                =    "DNS" 
        Leave_at_door                   =    "LAD" 
        Deliver_to_Post_Office          =    "D2PO" 

