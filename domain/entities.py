from typing import List, NamedTuple
from collections import namedtuple
import json

class ContactType(NamedTuple):
    CompanyName: str = None
    PersonName: str = None
    PhoneNumber: str = None
    EMailAddress: str = None

class AddressType(NamedTuple):
    CountryCode: str
    StateOrProvince: str = None
    CountryName: str = None
    PostalCode: str = None
    City: str = None
    AddressLines: List[str] = []

class PackageType(NamedTuple):
    Width: float
    Height: float
    Lenght: float
    Weight: float
    Id: str = None
    PackagingType: str = None
    Description: str = None

class ChargesPaymentType(NamedTuple):
    Type: str
    AccountNumber: str

class InsuranceType(NamedTuple):
    Value: str
    Currency: str

def jsonify(entity): 
    return json.dumps(entity, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class Charge():
    def __init__(self, Name: str = None, Value: str = None):
        self.Name = Name
        self.Value = Value

class Quote():
    def __init__(self, Provider: str, ServiceName: str, ServiceType: str, BaseCharge: float, DutiesAndTaxes: float, TotalCharge: float, Discount: float = None, ExtraCharges: List[Charge] = []):
        self.Provider = Provider
        self.ServiceName = ServiceName
        self.ServiceType = ServiceType
        self.BaseCharge = BaseCharge
        self.DutiesAndTaxes = DutiesAndTaxes
        self.TotalCharge = TotalCharge
        self.Discount = Discount
        self.ExtraCharges = ExtraCharges

    # DeliveryTime: str = None
    # PickupTime: str = None
    # DeliveryDate: str = None
    # PickupDate: str = None
    # Code: str = None


class Error():
    def __init__(self, Message: str = None, Severity: str = None):
        self.Message = Name
        self.Severity = Value





''' Party Type definition '''
class PartyType(namedtuple("PartyType", "Address Contact")):
    def __new__(cls, Address, Contact=None):
        return super(cls, PartyType).__new__(
            cls, 
            AddressType(**Address), 
            Contact if Contact is None else ContactType(**Contact)
        )

class Party(NamedTuple):
    Address: AddressType
    Contact: ContactType = None

def createParty(**args) -> Party:
    return Party(**PartyType(**args)._asdict())




''' ShipmentDetails Type definition '''
class ShipmentDetailsType(namedtuple("ShipmentDetailsType", "Packages Insurance ChargesPayment NumberOfPackages PackagingType IsDutiable Currency TotalWeight WeightUnit DimensionUnit")):
    def __new__(cls, Packages, Insurance=None, ChargesPayment=None, NumberOfPackages=None, PackagingType=None, IsDutiable="N", Currency=None, TotalWeight=None, WeightUnit="LB", DimensionUnit="IN"):
        return super(cls, ShipmentDetailsType).__new__(
            cls,
            list(map(lambda p: PackageType(**p), Packages)),
            Insurance if Insurance is None else InsuranceType(**Insurance),
            ChargesPayment if ChargesPayment is None else ChargesPaymentType(**ChargesPayment),
            NumberOfPackages, PackagingType, IsDutiable, Currency, TotalWeight, WeightUnit, DimensionUnit
        )

class ShipmentDetails(NamedTuple):
    Packages: List[PackageType]
    Insurance: InsuranceType = None 
    ChargesPayment: ChargesPaymentType = None 
    NumberOfPackages: int = None
    PackagingType: str = None
    IsDutiable: str = "N"
    Currency: str = None
    TotalWeight: float = None
    WeightUnit: str = "LB"
    DimensionUnit: str = "IN"

def createShipmentDetails(**args) -> ShipmentDetails:
    return ShipmentDetails(**ShipmentDetailsType(**args)._asdict())




''' QuoteRequest Type definition '''
class QuoteRequestType(namedtuple("QuoteRequestType", "Shipper Recipient ShipmentDetails")):
    def __new__(cls, Shipper, Recipient, ShipmentDetails):
        return super(cls, QuoteRequestType).__new__(
            cls, 
            createParty(**Shipper), 
            createParty(**Recipient), 
            createShipmentDetails(**ShipmentDetails)
        )

class QuoteRequest(NamedTuple):
    Shipper: Party 
    Recipient: Party
    ShipmentDetails: ShipmentDetails

def createQuoteRequest(**args) -> QuoteRequest:
    return QuoteRequest(**QuoteRequestType(**args)._asdict())
