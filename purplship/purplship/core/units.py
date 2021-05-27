"""Purplship universal data types and units definitions"""
import attr
import phonenumbers
from typing import List, Type, Optional, Iterator, Iterable, Tuple, Any, Union, cast
from purplship.core.utils import NF, Enum, Spec, SF
from purplship.core.models import Parcel, Address, AddressExtra
from purplship.core.errors import (
    FieldError,
    FieldErrorCode,
    MultiParcelNotSupportedError,
)


@attr.s(auto_attribs=True)
class PackagePreset:
    width: float = None
    height: float = None
    length: float = None
    weight: float = None
    volume: float = None
    weight_unit: str = "LB"
    dimension_unit: str = "IN"
    packaging_type: str = None


class LabelType(Enum):
    PDF = "PDF"
    ZPL = "ZPL"


class DocFormat(Enum):
    gif = "GIF"
    jpg = "JPG"
    pdf = "PDF"
    png = "PNG"


class PackagingUnit(Enum):
    envelope = "Small Envelope"
    pak = "Pak"
    tube = "Tube"
    pallet = "Pallet"
    small_box = "Small Box"
    medium_box = "Medium Box"
    your_packaging = "Your Packaging"


class PaymentType(Enum):
    sender = "SENDER"
    recipient = "RECIPIENT"
    third_party = "THIRD_PARTY"


class CreditCardType(Enum):
    visa = "Visa"
    mastercard = "Mastercard"
    american_express = "AmericanExpress"


class CustomsContentType(Enum):
    documents = 'DOCUMENTS'
    gift = 'GIFT'
    sample = 'SAMPLE'
    merchandise = 'MERCHANDISE'
    return_merchandise = 'RETURN_MERCHANDISE'
    other = 'OTHER'


class Incoterm(Enum):
    """universal international shipment incoterm (term of trades)"""
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
    """universal weight units"""
    KG = "KG"
    LB = "LB"


class DimensionUnit(Enum):
    """universal dimension units"""
    CM = "CM"
    IN = "IN"


class Dimension:
    """The dimension common processing helper"""
    def __init__(self, value: float, unit: Union[DimensionUnit, str] = DimensionUnit.CM, options: Type[Enum] = Enum):
        self._value = value
        self._unit = DimensionUnit[unit] if isinstance(unit, str) else unit

        # Options mapping
        measurement_options = {m.name: m.value for m in list(options)}  # type: ignore
        self._min_in = measurement_options.get('min_in')
        self._min_cm = measurement_options.get('min_cm')
        self._quant = measurement_options.get('quant')

    def __getitem__(self, item):
        return getattr(self, item)

    def _compute(self, value: float, min_value: float = None):
        below_min = min_value is not None and value < min_value
        return NF.decimal(
            value=(min_value if below_min else value),
            quant=self._quant
        )

    @property
    def unit(self) -> str:
        if self._unit is None:
            return None

        return self._unit.value

    @property
    def value(self):
        if self._unit is None or self._value is None:
            return None

        return self.__getattribute__(str(self._unit.name))

    @property
    def CM(self):
        if self._unit is None or self._value is None:
            return None
        if self._unit == DimensionUnit.IN:
            return self._compute(self._value * 2.54, self._min_cm)
        else:
            return self._compute(self._value, self._min_cm)

    @property
    def IN(self):
        if self._unit is None or self._value is None:
            return None
        if self._unit == DimensionUnit.CM:
            return self._compute(self._value / 2.54, self._min_in)
        else:
            return self._compute(self._value, self._min_in)

    @property
    def M(self):
        if self._unit is None or self._value is None:
            return None
        else:
            return self._compute(self.CM / 100)

    def map(self, options: Type[Enum]):
        return Dimension(
            value=self._value,
            unit=self._unit,
            options=options
        )


class Volume:
    """The volume common processing helper"""
    def __init__(
        self, side1: Dimension = None, side2: Dimension = None, side3: Dimension = None
    ):
        self._side1 = side1
        self._side2 = side2
        self._side3 = side3

    @property
    def value(self):
        if not any([self._side1.value, self._side2.value, self._side3.value]):
            return None

        return NF.decimal(self._side1.M * self._side2.M * self._side3.M)

    @property
    def cubic_meter(self):
        if self.value is None:
            return None
        return NF.decimal(self.value * 250)


class Girth:
    """The girth common processing helper"""
    def __init__(
        self, side1: Dimension = None, side2: Dimension = None, side3: Dimension = None
    ):
        self._side1 = side1
        self._side2 = side2
        self._side3 = side3

    @property
    def value(self):
        sides = [self._side1.CM, self._side2.CM, self._side3.CM]
        if not any(sides):
            return None

        sides.sort()
        small_side1, small_side2, _ = sides
        return NF.decimal((small_side1 + small_side2) * 2)


class Weight:
    """The weight common processing helper"""
    def __init__(self, value: float, unit: Union[WeightUnit, str] = WeightUnit.KG, options: Type[Enum] = Enum):
        self._value = value
        self._unit = WeightUnit[unit] if isinstance(unit, str) else unit

        # Options mapping
        measurement_options = {m.name: m.value for m in list(options)}  # type: ignore
        self._min_lb = measurement_options.get('min_lb')
        self._min_kg = measurement_options.get('min_kg')
        self._min_oz = measurement_options.get('min_oz')
        self._quant = measurement_options.get('quant')

    def __getitem__(self, item):
        return getattr(self, item)

    def _compute(self, value: float, min_value: float = None) -> Optional[float]:
        below_min = min_value is not None and value < min_value
        return NF.decimal(
            value=(min_value if below_min else value),
            quant=self._quant
        )

    @property
    def unit(self) -> str:
        if self._unit is None:
            return None

        return self._unit.value

    @property
    def value(self) -> Optional[float]:
        if self._unit is None or self._value is None:
            return None

        return self.__getattribute__(str(self._unit.name))

    @property
    def KG(self) -> Optional[float]:
        if self._unit is None or self._value is None:
            return None
        if self._unit == WeightUnit.KG:
            return self._compute(self._value, self._min_kg)
        elif self._unit == WeightUnit.LB:
            return self._compute(self._value / 2.205, self._min_kg)

        return None

    @property
    def LB(self) -> Optional[float]:
        if self._unit is None or self._value is None:
            return None
        if self._unit == WeightUnit.LB:
            return self._compute(self._value, self._min_lb)
        elif self._unit == WeightUnit.KG:
            return self._compute(self._value * 2.205, self._min_lb)

        return None

    @property
    def OZ(self) -> Optional[float]:
        if self._unit is None or self._value is None:
            return None
        if self._unit == WeightUnit.LB:
            return self._compute(self._value * 16, self._min_oz)
        elif self._unit == WeightUnit.KG:
            return self._compute(self._value * 35.274, self._min_oz)

        return None

    def map(self, options: Type[Enum]):
        return Weight(
            value=self._value,
            unit=self._unit,
            options=options
        )


class Package:
    """The parcel common processing helper"""
    def __init__(self, parcel: Parcel, template: PackagePreset = None):
        self.parcel: Parcel = parcel
        self.preset: PackagePreset = template or PackagePreset()

        self._dimension_unit = (
            (self.parcel.dimension_unit or self.preset.dimension_unit)
            if any([self.parcel.height, self.parcel.width, self.parcel.length])
            else self.preset.dimension_unit
        )
        self._weight_unit = (
            self.preset.weight_unit
            if self.parcel.weight is None
            else (self.parcel.weight_unit or self.preset.weight_unit)
        )

    def _compute_dimension(self, value):
        dimension = Dimension(value, DimensionUnit[self._dimension_unit])
        if self._dimension_unit == self.dimension_unit.value:
            return dimension

        return Dimension(dimension[self.dimension_unit.value], self.dimension_unit)

    @property
    def dimension_unit(self) -> DimensionUnit:
        if self.weight_unit == WeightUnit.KG:
            return DimensionUnit.CM

        return DimensionUnit.IN

    @property
    def weight_unit(self) -> WeightUnit:
        return WeightUnit[self._weight_unit]

    @property
    def packaging_type(self):
        return self.parcel.packaging_type or self.preset.packaging_type

    @property
    def weight(self):
        return Weight(self.parcel.weight or self.preset.weight, self.weight_unit)

    @property
    def width(self):
        return self._compute_dimension(self.preset.width or self.parcel.width)

    @property
    def height(self):
        return self._compute_dimension(self.preset.height or self.parcel.height)

    @property
    def length(self):
        return self._compute_dimension(self.preset.length or self.parcel.length)

    @property
    def girth(self):
        return Girth(self.width, self.length, self.height)

    @property
    def volume(self):
        return Volume(self.width, self.length, self.height)

    @property
    def thickness(self):
        return self._compute_dimension(self.preset.thickness)

    @property
    def has_dimensions(self):
        return any(
            [
                self.length,
                self.width,
                self.height,
            ]
        )


class Packages(Iterable[Package]):
    """The parcel collection common processing helper"""
    def __init__(
        self,
        parcels: List[Parcel],
        presets: Type[Enum] = None,
        required: List[str] = None,
        max_weight: Weight = None,
    ):
        def compute_preset(parcel) -> Optional[PackagePreset]:
            if (presets is None) | (
                presets is not None and parcel.package_preset not in presets
            ):
                return None

            return presets[parcel.package_preset].value

        self._items = [Package(parcel, compute_preset(parcel)) for parcel in parcels]
        self._required = required
        self._max_weight = max_weight
        self.validate()

    def __getitem__(self, index: int) -> Package:
        return self._items[index]

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[Package]:
        return iter(self._items)

    @property
    def single(self) -> Package:
        if len(self._items) > 1:
            raise MultiParcelNotSupportedError()
        return self._items[0]

    @property
    def weight(self) -> Weight:
        unit, _ = self.compatible_units
        value = sum(pkg.weight[unit.name] for pkg in self._items if pkg.weight[unit.name] is not None)

        if value is None or not any(self._items):
            return Weight(None, None)

        return Weight(unit=unit, value=value)

    @property
    def package_type(self) -> str:
        return (
            (self._items[0].packaging_type or 'your_packaging')
            if len(self._items) == 1 else None
        )

    @property
    def compatible_units(self) -> Tuple[WeightUnit, DimensionUnit]:
        if any(self._items) and self._items[0].weight_unit == WeightUnit.KG:
            return WeightUnit.KG, DimensionUnit.CM

        return WeightUnit.LB, DimensionUnit.IN

    def validate(self, required: List[str] = None, max_weight: Weight = None):
        required = required or self._required
        max_weight = max_weight or self._max_weight

        if any(check is not None for check in [required, max_weight]):
            errors = {}
            for index, package in enumerate(self._items):
                if required is not None:
                    for field in required:
                        prop = getattr(package, field)

                        if prop is None or (hasattr(prop, "value") and prop.value is None):
                            errors.update(
                                {f"parcel[{index}].{field}": FieldErrorCode.required}
                            )

                if max_weight is not None and (package.weight.LB or 0.0) > max_weight.LB:
                    errors.update({f"parcel[{index}].weight": FieldErrorCode.exceeds})

            if any(errors.items()):
                raise FieldError(errors)

    @staticmethod
    def map(
            parcels: List[Parcel],
            presets: Type[Enum] = None,
            required: List[str] = None,
            max_weight: Weight = None) -> Union[List[Package], 'Packages']:

        return cast(Union[List[Package], Packages], Packages(parcels, presets, required, max_weight))


class Option(Enum):
    """universal shipment options (special services)"""
    currency = Spec.asValue("currency")
    insurance = Spec.asValue("insurance", float)
    cash_on_delivery = Spec.asValue("COD", float)
    label_format = Spec.asValue("label_format")
    shipment_date = Spec.asValue("shipment_date")
    label_printing = Spec.asValue("label_printing")
    declared_value = Spec.asValue("declared_value", float)
    notification_emails = Spec.asValue("notification_emails")
    signature_confirmation = Spec.asFlag("signature_confirmation")


class Options:
    """The options common processing helper"""
    def __init__(self, options: dict, option_type: Type[Enum] = Enum):
        option_values = {}
        for key, val in options.items():
            if option_type is not None and key in option_type:
                option_values[option_type[key].name] = option_type[key].value.apply(val)
            elif key in Option and key:
                option_values[key] = Option[key].value.apply(val)

        self._options = option_values

    def __getitem__(self, item):
        return self._options.get(item)

    def __getattr__(self, item):
        return self._options.get(item)

    def __contains__(self, item) -> bool:
        return item in self._options

    def __len__(self) -> int:
        return len(self._options.items())

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        return iter(self._options.items())

    @property
    def has_content(self) -> bool:
        return any(o for o in self._options)

    @property
    def cash_on_delivery(self) -> float:
        return self[Option.cash_on_delivery.name]

    @property
    def currency(self) -> str:
        return self[Option.currency.name]

    @property
    def insurance(self) -> float:
        return self[Option.insurance.name]

    @property
    def label_format(self) -> str:
        return self[Option.label_format.name]

    @property
    def label_printing(self) -> str:
        return self[Option.label_printing.name]

    @property
    def declared_value(self) -> float:
        return self[Option.declared_value.name]

    @property
    def notification_emails(self) -> str:
        return self[Option.notification_emails.name]

    @property
    def notification_email(self) -> str:
        emails = str.split(self.notification_emails or '', ',', maxsplit=1)
        return next((email for email in emails if email != ''), None)

    @property
    def shipment_date(self) -> str:
        return self[Option.shipment_date.name]

    @property
    def signature_confirmation(self) -> str:
        return self[Option.signature_confirmation.name]


class Services:
    """The services common processing helper"""
    def __init__(self, services: Iterable, service_type: Type[Enum]):
        self._services = [
            service_type[s] for s in services if s in service_type
        ]

    def __len__(self) -> int:
        return len(self._services)

    def __iter__(self) -> Iterator[Enum]:
        return iter(self._services)

    def __contains__(self, item) -> bool:
        return item in [s.name for s in self._services]

    @property
    def first(self) -> Enum:
        return next(iter(self._services), None)


class Phone:
    def __init__(self, phone_number: str = None, country_code: str = None):
        try:
            self.number = phonenumbers.parse(phone_number, country_code)
        except Exception:
            self.number = None

    @property
    def country_code(self):
        if self.number is None:
            return None

        return self.number.country_code

    @property
    def area_code(self):
        if self.number is None:
            return None

        return str(self.number.national_number)[0:3]

    @property
    def phone(self):
        if self.number is None:
            return None

        return str(self.number.national_number)[3:]


class CompleteAddress:
    def __init__(self, address: Optional[Address]):
        self._address = address

    def __getattr__(self, item):
        if hasattr(self._address, item):
            return getattr(self._address, item)

        return getattr(getattr(self._address, 'extra', None), item, None)

    @property
    def country_name(self):
        return Country[self._address.country_code].value

    @property
    def address_line(self) -> str:
        return self._compute_address_line()

    @property
    def address_lines(self) -> str:
        return self._compute_address_line(join=False)

    @property
    def tax_id(self) -> Optional[str]:
        return self._address.federal_tax_id or self._address.state_tax_id

    @property
    def taxes(self) -> List[str]:
        return SF.concat_str(
            self._address.federal_tax_id, self._address.state_tax_id)

    @property
    def has_contact_info(self) -> bool:
        return any([
            self._address.company_name,
            self._address.phone_number,
            self._address.person_name,
            self._address.email,
        ])

    @property
    def has_tax_info(self) -> bool:
        return any([self._address.federal_tax_id, self._address.state_tax_id])

    def _compute_address_line(self, join: bool = True) -> Optional[str]:
        if any([self._address.address_line1, self._address.address_line2]):
            return SF.concat_str(
                self._address.address_line1,
                self._address.address_line2,
                join=join
            )

        if self._address.extra is not None:
            return SF.concat_str(
                self._address.extra.suite,
                self._address.extra.street_number,
                self._address.extra.street_name,
                self._address.extra.street_type,
                join=True
            )

        return None

    @staticmethod
    def map(address: Optional[Address]) -> Union[Address, AddressExtra, 'CompleteAddress']:
        return cast(Union[Address, AddressExtra, CompleteAddress], CompleteAddress(address))


class Currency(Enum):
    EUR = "Euro"
    AED = "UAE Dirham"
    USD = "US Dollar"
    XCD = "East Caribbean Dollar"
    AMD = "Dran"
    ANG = "Netherlands Antilles Guilder"
    AOA = "Kwanza"
    ARS = "Argentine Peso"
    AUD = "Australian Dollar"
    AWG = "Aruba Guilder"
    AZN = "Manat"
    BAM = "Convertible Marks"
    BBD = "Barbadian Dollar"
    BDT = "Taka"
    XOF = "CFA Franc West Africa"
    BGN = "Bulgarian Lev"
    BHD = "Bahraini Dinar"
    BIF = "Burundese Franc"
    BMD = "Bermudian Dollar"
    BND = "Brunei Dollar"
    BOB = "Boliviano"
    BRL = "Real"
    BSD = "Bahamian Dollar"
    BTN = "Ngultrum"
    BWP = "Pula"
    BYN = "Belarussian Ruble"
    BZD = "Belize Dollar"
    CAD = "Canadian Dollar"
    CDF = "Franc Congolais"
    XAF = "CFA Franc Central Africa"
    CHF = "Swiss Franc"
    NZD = "New Zealand Dollar"
    CLP = "New Chile Peso"
    CNY = "Yuan (Ren Min Bi)"
    COP = "Colombian Peso"
    CRC = "Costa Rican Colon"
    CUC = "Peso Convertible"
    CVE = "Cape Verde Escudo"
    CZK = "Czech Koruna"
    DJF = "Djibouti Franc"
    DKK = "Danish Krone"
    DOP = "Dominican Republic Peso"
    DZD = "Algerian Dinar"
    EGP = "Egyptian Pound"
    ERN = "Nakfa"
    ETB = "Birr"
    FJD = "Fijian Dollar"
    GBP = "Pound Sterling"
    GEL = "Georgian Lari"
    GHS = "Cedi"
    GMD = "Dalasi"
    GNF = "Guinea Franc"
    GTQ = "Quetzal"
    GYD = "Guyanan Dollar"
    HKD = "Hong Kong Dollar"
    HNL = "Lempira"
    HRK = "Croatian Kuna"
    HTG = "Gourde"
    HUF = "Forint"
    IDR = "Rupiah"
    ILS = "New Israeli Shekel"
    INR = "Indian Rupee"
    IRR = "Iranian Rial"
    ISK = "Icelandic Krona"
    JMD = "Jamaican Dollar"
    JOD = "Jordanian Dinar"
    JPY = "Yen"
    KES = "Kenyan Shilling"
    KGS = "Som"
    KHR = "Khmer Rial"
    KMF = "Comoros Franc"
    KPW = "North Korean Won"
    KRW = "Won"
    KWD = "Kuwaiti Dinar"
    KYD = "Cayman Islands Dollar"
    KZT = "Tenge"
    LAK = "Kip"
    LKR = "Sri Lankan Rupee"
    LRD = "Liberian Dollar"
    LSL = "Loti"
    LYD = "Libyan Dinar"
    MAD = "Moroccan Dirham"
    MDL = "Leu"
    MGA = "Ariary"
    MKD = "Denar"
    MMK = "Kyat"
    MNT = "Tugrik"
    MOP = "Pataca"
    MRO = "Ouguiya"
    MUR = "Mauritius Rupee"
    MVR = "Rufiyaa"
    MWK = "Kwacha"
    MXN = "Mexican Nuevo Peso"
    MYR = "Ringgit"
    MZN = "Mozambique Metical"
    NAD = "Namibian Dollar"
    XPF = "CFP Franc"
    NGN = "Naira"
    NIO = "Cordoba Oro"
    NOK = "Norwegian Krone"
    NPR = "Nepalese Rupee"
    OMR = "Omani Rial"
    PEN = "Nuevo Sol"
    PGK = "Kina"
    PHP = "Phillipines Peso"
    PKR = "Pakistani Rupee"
    PLN = "Zloty"
    PYG = "Guarani"
    QAR = "Qatar Rial"
    RON = "Leu"
    RSD = "Serbia, Dinars"
    RUB = "Russian Ruble"
    RWF = "Rwanda Franc"
    SAR = "Saudi Riyal"
    SBD = "Solomon Islands Dollar"
    SCR = "Seychelles Rupee"
    SDG = "Sudanese Pound"
    SEK = "Swedish Krona"
    SGD = "Singapore Dollar"
    SHP = "St. Helena Pound"
    SLL = "Leone"
    SOS = "Somali Shilling"
    SRD = "Suriname Dollar"
    SSP = "South Sudanese pound"
    STD = "Dobra"
    SYP = "Syrian Pound"
    SZL = "Lilangeni"
    THB = "Baht"
    TJS = "Somoni"
    TND = "Tunisian Dinar"
    TOP = "Pa'anga"
    TRY = "New Turkish Lira"
    TTD = "Trinidad and Tobago Dollar"
    TWD = "New Taiwan Dollar"
    TZS = "Tanzanian Shilling"
    UAH = "Hryvna"
    UYU = "Peso Uruguayo"
    UZS = "Sum"
    VEF = "Bolivar Fuerte"
    VND = "Dong"
    VUV = "Vanuatu Vatu"
    WST = "Tala"
    YER = "Yemeni Riyal"
    ZAR = "South African Rand"
    ZMW = "Kwacha"


class Country(Enum):
    AD = "Andorra"
    AE = "United Arab Emirates"
    AF = "Afghanistan"
    AG = "Antigua"
    AI = "Anguilla"
    AL = "Albania"
    AM = "Armenia"
    AN = "Netherlands Antilles"
    AO = "Angola"
    AR = "Argentina"
    AS = "American Samoa"
    AT = "Austria"
    AU = "Australia"
    AW = "Aruba"
    AZ = "Azerbaijan"
    BA = "Bosnia And Herzegovina"
    BB = "Barbados"
    BD = "Bangladesh"
    BE = "Belgium"
    BF = "Burkina Faso"
    BG = "Bulgaria"
    BH = "Bahrain"
    BI = "Burundi"
    BJ = "Benin"
    BM = "Bermuda"
    BN = "Brunei"
    BO = "Bolivia"
    BR = "Brazil"
    BS = "Bahamas"
    BT = "Bhutan"
    BW = "Botswana"
    BY = "Belarus"
    BZ = "Belize"
    CA = "Canada"
    CD = "Congo, The Democratic Republic Of"
    CF = "Central African Republic"
    CG = "Congo"
    CH = "Switzerland"
    CI = "Cote D Ivoire"
    CK = "Cook Islands"
    CL = "Chile"
    CM = "Cameroon"
    CN = "China, Peoples Republic"
    CO = "Colombia"
    CR = "Costa Rica"
    CU = "Cuba"
    CV = "Cape Verde"
    CY = "Cyprus"
    CZ = "Czech Republic, The"
    DE = "Germany"
    DJ = "Djibouti"
    DK = "Denmark"
    DM = "Dominica"
    DO = "Dominican Republic"
    DZ = "Algeria"
    EC = "Ecuador"
    EE = "Estonia"
    EG = "Egypt"
    ER = "Eritrea"
    ES = "Spain"
    ET = "Ethiopia"
    FI = "Finland"
    FJ = "Fiji"
    FK = "Falkland Islands"
    FM = "Micronesia, Federated States Of"
    FO = "Faroe Islands"
    FR = "France"
    GA = "Gabon"
    GB = "United Kingdom"
    GD = "Grenada"
    GE = "Georgia"
    GF = "French Guyana"
    GG = "Guernsey"
    GH = "Ghana"
    GI = "Gibraltar"
    GL = "Greenland"
    GM = "Gambia"
    GN = "Guinea Republic"
    GP = "Guadeloupe"
    GQ = "Guinea-equatorial"
    GR = "Greece"
    GT = "Guatemala"
    GU = "Guam"
    GW = "Guinea-bissau"
    GY = "Guyana (british)"
    HK = "Hong Kong"
    HN = "Honduras"
    HR = "Croatia"
    HT = "Haiti"
    HU = "Hungary"
    IC = "Canary Islands, The"
    ID = "Indonesia"
    IE = "Ireland, Republic Of"
    IL = "Israel"
    IN = "India"
    IQ = "Iraq"
    IR = "Iran (islamic Republic Of)"
    IS = "Iceland"
    IT = "Italy"
    JE = "Jersey"
    JM = "Jamaica"
    JO = "Jordan"
    JP = "Japan"
    KE = "Kenya"
    KG = "Kyrgyzstan"
    KH = "Cambodia"
    KI = "Kiribati"
    KM = "Comoros"
    KN = "St. Kitts"
    KP = "Korea, The D.p.r Of (north K.)"
    KR = "Korea, Republic Of (south K.)"
    KV = "Kosovo"
    KW = "Kuwait"
    KY = "Cayman Islands"
    KZ = "Kazakhstan"
    LA = "Lao Peoples Democratic Republic"
    LB = "Lebanon"
    LC = "St. Lucia"
    LI = "Liechtenstein"
    LK = "Sri Lanka"
    LR = "Liberia"
    LS = "Lesotho"
    LT = "Lithuania"
    LU = "Luxembourg"
    LV = "Latvia"
    LY = "Libya"
    MA = "Morocco"
    MC = "Monaco"
    MD = "Moldova, Republic Of"
    ME = "Montenegro, Republic Of"
    MG = "Madagascar"
    MH = "Marshall Islands"
    MK = "Macedonia, Republic Of"
    ML = "Mali"
    MM = "Myanmar"
    MN = "Mongolia"
    MO = "Macau"
    MP = "Commonwealth No. Mariana Islands"
    MQ = "Martinique"
    MR = "Mauritania"
    MS = "Montserrat"
    MT = "Malta"
    MU = "Mauritius"
    MV = "Maldives"
    MW = "Malawi"
    MX = "Mexico"
    MY = "Malaysia"
    MZ = "Mozambique"
    NA = "Namibia"
    NC = "New Caledonia"
    NE = "Niger"
    NG = "Nigeria"
    NI = "Nicaragua"
    NL = "Netherlands, The"
    NO = "Norway"
    NP = "Nepal"
    NR = "Nauru, Republic Of"
    NU = "Niue"
    NZ = "New Zealand"
    OM = "Oman"
    PA = "Panama"
    PE = "Peru"
    PF = "Tahiti"
    PG = "Papua New Guinea"
    PH = "Philippines, The"
    PK = "Pakistan"
    PL = "Poland"
    PR = "Puerto Rico"
    PT = "Portugal"
    PW = "Palau"
    PY = "Paraguay"
    QA = "Qatar"
    RE = "Reunion, Island Of"
    RO = "Romania"
    RS = "Serbia, Republic Of"
    RU = "Russian Federation, The"
    RW = "Rwanda"
    SA = "Saudi Arabia"
    SB = "Solomon Islands"
    SC = "Seychelles"
    SD = "Sudan"
    SE = "Sweden"
    SG = "Singapore"
    SH = "Saint Helena"
    SI = "Slovenia"
    SK = "Slovakia"
    SL = "Sierra Leone"
    SM = "San Marino"
    SN = "Senegal"
    SO = "Somalia"
    SR = "Suriname"
    SS = "South Sudan"
    ST = "Sao Tome And Principe"
    SV = "El Salvador"
    SY = "Syria"
    SZ = "Swaziland"
    TC = "Turks And Caicos Islands"
    TD = "Chad"
    TG = "Togo"
    TH = "Thailand"
    TJ = "Tajikistan"
    TL = "Timor Leste"
    TN = "Tunisia"
    TO = "Tonga"
    TR = "Turkey"
    TT = "Trinidad And Tobago"
    TV = "Tuvalu"
    TW = "Taiwan"
    TZ = "Tanzania"
    UA = "Ukraine"
    UG = "Uganda"
    US = "United States"
    UY = "Uruguay"
    UZ = "Uzbekistan"
    VA = "Vatican City State"
    VC = "St. Vincent"
    VE = "Venezuela"
    VG = "British Virgin Islands"
    VI = "U.S. Virgin Islands"
    VN = "Vietnam"
    VU = "Vanuatu"
    WS = "Samoa"
    XB = "Bonaire"
    XC = "Curacao"
    XE = "St. Eustatius"
    XM = "St. Maarten"
    XN = "Nevis"
    XS = "Somaliland, Rep Of (north Somalia)"
    XY = "St. Barthelemy"
    YE = "Yemen, Republic Of"
    YT = "Mayotte"
    ZA = "South Africa"
    ZM = "Zambia"
    ZW = "Zimbabwe"


class CountryCurrency(Enum):
    AD = "EUR"
    AE = "AED"
    AF = "USD"
    AG = "XCD"
    AI = "XCD"
    AL = "EUR"
    AM = "AMD"
    AN = "ANG"
    AO = "AOA"
    AR = "ARS"
    AS = "USD"
    AT = "EUR"
    AU = "AUD"
    AW = "AWG"
    AZ = "AZN"
    BA = "BAM"
    BB = "BBD"
    BD = "BDT"
    BE = "EUR"
    BF = "XOF"
    BG = "BGN"
    BH = "BHD"
    BI = "BIF"
    BJ = "XOF"
    BM = "BMD"
    BN = "BND"
    BO = "BOB"
    BR = "BRL"
    BS = "BSD"
    BT = "BTN"
    BW = "BWP"
    BY = "BYN"
    BZ = "BZD"
    CA = "CAD"
    CD = "CDF"
    CF = "XAF"
    CG = "XAF"
    CH = "CHF"
    CI = "XOF"
    CK = "NZD"
    CL = "CLP"
    CM = "XAF"
    CN = "CNY"
    CO = "COP"
    CR = "CRC"
    CU = "CUC"
    CV = "CVE"
    CY = "EUR"
    CZ = "CZK"
    DE = "EUR"
    DJ = "DJF"
    DK = "DKK"
    DM = "XCD"
    DO = "DOP"
    DZ = "DZD"
    EC = "USD"
    EE = "EUR"
    EG = "EGP"
    ER = "ERN"
    ES = "EUR"
    ET = "ETB"
    FI = "EUR"
    FJ = "FJD"
    FK = "GBP"
    FM = "USD"
    FO = "DKK"
    FR = "EUR"
    GA = "XAF"
    GB = "GBP"
    GD = "XCD"
    GE = "GEL"
    GF = "EUR"
    GG = "GBP"
    GH = "GHS"
    GI = "GBP"
    GL = "DKK"
    GM = "GMD"
    GN = "GNF"
    GP = "EUR"
    GQ = "XAF"
    GR = "EUR"
    GT = "GTQ"
    GU = "USD"
    GW = "XOF"
    GY = "GYD"
    HK = "HKD"
    HN = "HNL"
    HR = "HRK"
    HT = "HTG"
    HU = "HUF"
    IC = "EUR"
    ID = "IDR"
    IE = "EUR"
    IL = "ILS"
    IN = "INR"
    IQ = "USD"
    IR = "IRR"
    IS = "ISK"
    IT = "EUR"
    JE = "GBP"
    JM = "JMD"
    JO = "JOD"
    JP = "JPY"
    KE = "KES"
    KG = "KGS"
    KH = "KHR"
    KI = "AUD"
    KM = "KMF"
    KN = "XCD"
    KP = "KPW"
    KR = "KRW"
    KV = "EUR"
    KW = "KWD"
    KY = "KYD"
    KZ = "KZT"
    LA = "LAK"
    LB = "USD"
    LC = "XCD"
    LI = "CHF"
    LK = "LKR"
    LR = "LRD"
    LS = "LSL"
    LT = "EUR"
    LU = "EUR"
    LV = "EUR"
    LY = "LYD"
    MA = "MAD"
    MC = "EUR"
    MD = "MDL"
    ME = "EUR"
    MG = "MGA"
    MH = "USD"
    MK = "MKD"
    ML = "XOF"
    MM = "MMK"
    MN = "MNT"
    MO = "MOP"
    MP = "USD"
    MQ = "EUR"
    MR = "MRO"
    MS = "XCD"
    MT = "EUR"
    MU = "MUR"
    MV = "MVR"
    MW = "MWK"
    MX = "MXN"
    MY = "MYR"
    MZ = "MZN"
    NA = "NAD"
    NC = "XPF"
    NE = "XOF"
    NG = "NGN"
    NI = "NIO"
    NL = "EUR"
    NO = "NOK"
    NP = "NPR"
    NR = "AUD"
    NU = "NZD"
    NZ = "NZD"
    OM = "OMR"
    PA = "USD"
    PE = "PEN"
    PF = "XPF"
    PG = "PGK"
    PH = "PHP"
    PK = "PKR"
    PL = "PLN"
    PR = "USD"
    PT = "EUR"
    PW = "USD"
    PY = "PYG"
    QA = "QAR"
    RE = "EUR"
    RO = "RON"
    RS = "RSD"
    RU = "RUB"
    RW = "RWF"
    SA = "SAR"
    SB = "SBD"
    SC = "SCR"
    SD = "SDG"
    SE = "SEK"
    SG = "SGD"
    SH = "SHP"
    SI = "EUR"
    SK = "EUR"
    SL = "SLL"
    SM = "EUR"
    SN = "XOF"
    SO = "SOS"
    SR = "SRD"
    SS = "SSP"
    ST = "STD"
    SV = "USD"
    SY = "SYP"
    SZ = "SZL"
    TC = "USD"
    TD = "XAF"
    TG = "XOF"
    TH = "THB"
    TJ = "TJS"
    TL = "USD"
    TN = "TND"
    TO = "TOP"
    TR = "TRY"
    TT = "TTD"
    TV = "AUD"
    TW = "TWD"
    TZ = "TZS"
    UA = "UAH"
    UG = "USD"
    US = "USD"
    UY = "UYU"
    UZ = "UZS"
    VA = "EUR"
    VC = "XCD"
    VE = "VEF"
    VG = "USD"
    VI = "USD"
    VN = "VND"
    VU = "VUV"
    WS = "WST"
    XB = "EUR"
    XC = "EUR"
    XE = "ANG"
    XM = "EUR"
    XN = "XCD"
    XS = "USD"
    XY = "ANG"
    YE = "YER"
    YT = "EUR"
    ZA = "ZAR"
    ZM = "ZMW"
    ZW = "USD"


def create_enum(name, values):
    return Enum(name, values)  # type: ignore


class CountryState(Enum):
    AE = create_enum(
        "State",
        {
            "AB": "Abu Dhabi",
            "AJ": "Ajman",
            "DU": "Dubai",
            "FU": "Fujairah",
            "RA": "Ras al-Khaimah",
            "SH": "Sharjah",
            "UM": "Umm al-Qaiwain",
        },
    )
    CA = create_enum(
        "State",
        {
            "AB": "Alberta",
            "BC": "British Columbia",
            "MB": "Manitoba",
            "NB": "New Brunswick",
            "NL": "Newfoundland",
            "NT": "Northwest Territories",
            "NS": "Nova Scotia",
            "NU": "Nunavut",
            "ON": "Ontario",
            "PE": "Prince Edward Island",
            "QC": "Quebec",
            "SK": "Saskatchewan",
            "YT": "Yukon",
        },
    )
    CN = create_enum(
        "State",
        {
            "anhui": "Anhui",
            "hainan": "Hainan",
            "jiangxi": "Jiangxi",
            "shanghai": "Shanghai",
            "beijing": "Beijing",
            "hebei": "Hebei",
            "jilin": "Jilin",
            "shanxi": "Shanxi",
            "chongqing": "Chongqing",
            "heilongjiang": "Heilongjiang",
            "liaoning": "Liaoning",
            "sichuan": "Sichuan",
            "fujian": "Fujian",
            "henan": "Henan",
            "nei_mongol": "Nei Mongol",
            "tianjin": "Tianjin",
            "gansu": "Gansu",
            "hubei": "Hubei",
            "qinghai": "Qinghai",
            "xinjiang": "Xinjiang",
            "guangdong": "Guangdong",
            "hunan": "Hunan",
            "shaanxi": "Shaanxi",
            "yunnan": "Yunnan",
            "guizhou": "Guizhou",
            "jiangsu": "Jiangsu",
            "shandong": "Shandong",
            "zhejiang": "Zhejiang",
        },
    )
    IN = create_enum(
        "State",
        {
            "AN": "Andaman & Nicobar (U.T)",
            "AP": "Andhra Pradesh",
            "AR": "Arunachal Pradesh",
            "AS": "Assam",
            "BR": "Bihar",
            "CG": "Chattisgarh",
            "CH": "Chandigarh (U.T.)",
            "DD": "Daman & Diu (U.T.)",
            "DL": "Delhi (U.T.)",
            "DN": "Dadra and Nagar Haveli (U.T.)",
            "GA": "Goa",
            "GJ": "Gujarat",
            "HP": "Himachal Pradesh",
            "HR": "Haryana",
            "JH": "Jharkhand",
            "JK": "Jammu & Kashmir",
            "KA": "Karnataka",
            "KL": "Kerala",
            "LD": "Lakshadweep (U.T)",
            "MH": "Maharashtra",
            "ML": "Meghalaya",
            "MN": "Manipur",
            "MP": "Madhya Pradesh",
            "MZ": "Mizoram",
            "NL": "Nagaland",
            "OR": "Orissa",
            "PB": "Punjab",
            "PY": "Puducherry (U.T.)",
            "RJ": "Rajasthan",
            "SK": "Sikkim",
            "TN": "Tamil Nadu",
            "TR": "Tripura",
            "UA": "Uttaranchal",
            "UP": "Uttar Pradesh",
            "WB": "West Bengal",
        },
    )
    MX = create_enum(
        "State",
        {
            "AG": "Aguascalientes",
            "BC": "Baja California",
            "BS": "Baja California Sur",
            "CM": "Campeche",
            "CS": "Chiapas",
            "CH": "Chihuahua",
            "CO": "Coahuila",
            "CL": "Colima",
            "DF": "Ciudad de México",
            "DG": "Durango",
            "GT": "Guanajuato",
            "GR": "Guerrero",
            "HG": "Hidalgo",
            "JA": "Jalisco",
            "EM": "Estado de México",
            "MI": "Michoacán",
            "MO": "Morelos",
            "NA": "Nayarit",
            "NL": "Nuevo León",
            "OA": "Oaxaca",
            "PU": "Puebla",
            "QE": "Querétaro",
            "QR": "Quintana Roo",
            "SL": "San Luis Potosí",
            "SI": "Sinaloa",
            "SO": "Sonora",
            "TB": "Tabasco",
            "TM": "Tamaulipas",
            "TL": "Tlaxcala",
            "VE": "Veracruz",
            "YU": "Yucatán",
            "ZA": "Zacatecas",
        },
    )
    US = create_enum(
        "State",
        {
            "AL": "Alabama",
            "AK": "Alaska",
            "AZ": "Arizona",
            "AR": "Arkansas",
            "CA": "California",
            "CO": "Colorado",
            "CT": "Connecticut",
            "DE": "Delaware",
            "DC": "District of Columbia",
            "FL": "Florida",
            "GA": "Georgia",
            "HI": "Hawaii",
            "ID": "Idaho",
            "IL": "Illinois",
            "IN": "Indiana",
            "IA": "Iowa",
            "KS": "Kansas",
            "KY": "Kentucky",
            "LA": "Louisiana",
            "ME": "Maine",
            "MD": "Maryland",
            "MA": "Massachusetts",
            "MI": "Michigan",
            "MN": "Minnesota",
            "MS": "Mississippi",
            "MO": "Missouri",
            "MT": "Montana",
            "NE": "Nebraska",
            "NV": "Nevada",
            "NH": "New Hampshire",
            "NJ": "New Jersey",
            "NM": "New Mexico",
            "NY": "New York",
            "NC": "North Carolina",
            "ND": "North Dakota",
            "OH": "Ohio",
            "OK": "Oklahoma",
            "OR": "Oregon",
            "PA": "Pennsylvania",
            "RI": "Rhode Island",
            "SC": "South Carolina",
            "SD": "South Dakota",
            "TN": "Tennessee",
            "TX": "Texas",
            "UT": "Utah",
            "VT": "Vermont",
            "VA": "Virginia",
            "WA": "Washington State",
            "WV": "West Virginia",
            "WI": "Wisconsin",
            "WY": "Wyoming",
            "PR": "Puerto Rico",
        },
    )
