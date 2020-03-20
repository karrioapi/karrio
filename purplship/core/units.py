from dataclasses import dataclass
from enum import Enum
from purplship.core.models import Insurance, COD, Notification, Parcel


@dataclass
class PackagePreset:
    width: float = None
    height: float = None
    depth: float = None
    length: float = None
    weight: float = None
    volume: float = None
    thickness: float = None
    weight_unit: str = "LB"
    dimension_unit: str = "IN"


class DimensionUnit(Enum):
    CM = "CM"
    IN = "IN"


class Dimension:
    def __init__(self, value: float, unit: DimensionUnit = DimensionUnit.CM):
        self._value = value
        self._unit = unit

    @property
    def value(self):
        return self.__getattribute__(str(self._unit.name))

    @property
    def CM(self):
        if self._unit is None or self._value is None:
            return None
        if self._unit == DimensionUnit.CM:
            return float(self._value)
        else:
            return float(self._value * 0.393701)

    @property
    def IN(self):
        if self._unit is None or self._value is None:
            return None
        if self._unit == DimensionUnit.IN:
            return float(self._value)
        else:
            return float(self._value * 2.54)


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


class PayorType(Enum):
    sender = "SENDER"
    recipient = "RECIPIENT"
    third_party = "THIRD_PARTY"


class WeightUnit(Enum):
    KG = "KG"
    LB = "LB"


class Weight:
    def __init__(self, value: float, unit: WeightUnit = WeightUnit.KG):
        self._value = value
        self._unit = unit

    @property
    def value(self):
        return self.__getattribute__(str(self._unit.name))

    @property
    def KG(self):
        if self._unit is None or self._value is None:
            return None
        if self._unit == WeightUnit.KG:
            return float(self._value)
        else:
            return float(self._value * 0.453592)

    @property
    def LB(self):
        if self._unit is None or self._value is None:
            return None
        if self._unit == WeightUnit.LB:
            return float(self._value)
        else:
            return float(self._value * 2.204620823516057)

    @property
    def OZ(self):
        if self._unit is None or self._value is None:
            return None
        if self._unit == WeightUnit.LB:
            return float(self._value * 16)
        elif self._unit == WeightUnit.KG:
            return float(self._value * 35.274)
        return None


class Dimensions:
    def __init__(self, parcel: Parcel, template: PackagePreset):
        self._parcel = parcel
        self._template = template

    @property
    def dimension_unit(self):
        return DimensionUnit[self._parcel.dimension_unit or "IN"].value

    @property
    def weight_unit(self):
        return WeightUnit[self._parcel.weight_unit or "LB"].value

    @property
    def weight(self):
        return Weight(self._parcel.weight, self.weight_unit)

    @property
    def width(self):
        return Dimension(self._parcel.width, self.dimension_unit)

    @property
    def height(self):
        return Dimension(self._parcel.height, self.dimension_unit)

    @property
    def length(self):
        return Dimension(self._parcel.length, self.dimension_unit)

    @property
    def girth(self):
        return None

    @property
    def volume(self):
        return None

    @property
    def thickness(self):
        return None


class Options:
    def __init__(self, payload: dict):
        self._payload = payload

    @property
    def has_content(self):
        return any(o for o in self._payload if o in Options.Code.__members__)

    @property
    def cash_on_delivery(self):
        if Options.Code.cash_on_delivery.name in self._payload:
            return COD(**self._payload[Options.Code.cash_on_delivery.name])
        return None

    @property
    def currency(self):
        return self._payload.get(Options.Code.currency.name)

    @property
    def insurance(self):
        if Options.Code.insurance.name in self._payload:
            return Insurance(**self._payload[Options.Code.insurance.name])
        return None

    @property
    def notification(self):
        if Options.Code.notification.name in self._payload:
            return Notification(**self._payload[Options.Code.notification.name])
        return None

    @property
    def printing(self):
        return self._payload.get(Options.Code.printing.name)

    class Code(Enum):  # TODO:: Need to be documented
        cash_on_delivery = "COD"
        currency = "currency"
        insurance = "insurance"
        notification = "notification"
        printing = "printing"


class PrinterType(Enum):
    regular = 'Regular'  # Regular
    thermal = 'Thermal'  # Thermal


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
    AD = "ANDORRA"
    AE = "UNITED ARAB EMIRATES"
    AF = "AFGHANISTAN"
    AG = "ANTIGUA"
    AI = "ANGUILLA"
    AL = "ALBANIA"
    AM = "ARMENIA"
    AN = "NETHERLANDS ANTILLES"
    AO = "ANGOLA"
    AR = "ARGENTINA"
    AS = "AMERICAN SAMOA"
    AT = "AUSTRIA"
    AU = "AUSTRALIA"
    AW = "ARUBA"
    AZ = "AZERBAIJAN"
    BA = "BOSNIA AND HERZEGOVINA"
    BB = "BARBADOS"
    BD = "BANGLADESH"
    BE = "BELGIUM"
    BF = "BURKINA FASO"
    BG = "BULGARIA"
    BH = "BAHRAIN"
    BI = "BURUNDI"
    BJ = "BENIN"
    BM = "BERMUDA"
    BN = "BRUNEI"
    BO = "BOLIVIA"
    BR = "BRAZIL"
    BS = "BAHAMAS"
    BT = "BHUTAN"
    BW = "BOTSWANA"
    BY = "BELARUS"
    BZ = "BELIZE"
    CA = "CANADA"
    CD = "CONGO, THE DEMOCRATIC REPUBLIC OF"
    CF = "CENTRAL AFRICAN REPUBLIC"
    CG = "CONGO"
    CH = "SWITZERLAND"
    CI = "COTE D IVOIRE"
    CK = "COOK ISLANDS"
    CL = "CHILE"
    CM = "CAMEROON"
    CN = "CHINA, PEOPLES REPUBLIC"
    CO = "COLOMBIA"
    CR = "COSTA RICA"
    CU = "CUBA"
    CV = "CAPE VERDE"
    CY = "CYPRUS"
    CZ = "CZECH REPUBLIC, THE"
    DE = "GERMANY"
    DJ = "DJIBOUTI"
    DK = "DENMARK"
    DM = "DOMINICA"
    DO = "DOMINICAN REPUBLIC"
    DZ = "ALGERIA"
    EC = "ECUADOR"
    EE = "ESTONIA"
    EG = "EGYPT"
    ER = "ERITREA"
    ES = "SPAIN"
    ET = "ETHIOPIA"
    FI = "FINLAND"
    FJ = "FIJI"
    FK = "FALKLAND ISLANDS"
    FM = "MICRONESIA, FEDERATED STATES OF"
    FO = "FAROE ISLANDS"
    FR = "FRANCE"
    GA = "GABON"
    GB = "UNITED KINGDOM"
    GD = "GRENADA"
    GE = "GEORGIA"
    GF = "FRENCH GUYANA"
    GG = "GUERNSEY"
    GH = "GHANA"
    GI = "GIBRALTAR"
    GL = "GREENLAND"
    GM = "GAMBIA"
    GN = "GUINEA REPUBLIC"
    GP = "GUADELOUPE"
    GQ = "GUINEA-EQUATORIAL"
    GR = "GREECE"
    GT = "GUATEMALA"
    GU = "GUAM"
    GW = "GUINEA-BISSAU"
    GY = "GUYANA (BRITISH)"
    HK = "HONG KONG"
    HN = "HONDURAS"
    HR = "CROATIA"
    HT = "HAITI"
    HU = "HUNGARY"
    IC = "CANARY ISLANDS, THE"
    ID = "INDONESIA"
    IE = "IRELAND, REPUBLIC OF"
    IL = "ISRAEL"
    IN = "INDIA"
    IQ = "IRAQ"
    IR = "IRAN (ISLAMIC REPUBLIC OF)"
    IS = "ICELAND"
    IT = "ITALY"
    JE = "JERSEY"
    JM = "JAMAICA"
    JO = "JORDAN"
    JP = "JAPAN"
    KE = "KENYA"
    KG = "KYRGYZSTAN"
    KH = "CAMBODIA"
    KI = "KIRIBATI"
    KM = "COMOROS"
    KN = "ST. KITTS"
    KP = "KOREA, THE D.P.R OF (NORTH K.)"
    KR = "KOREA, REPUBLIC OF (SOUTH K.)"
    KV = "KOSOVO"
    KW = "KUWAIT"
    KY = "CAYMAN ISLANDS"
    KZ = "KAZAKHSTAN"
    LA = "LAO PEOPLES DEMOCRATIC REPUBLIC"
    LB = "LEBANON"
    LC = "ST. LUCIA"
    LI = "LIECHTENSTEIN"
    LK = "SRI LANKA"
    LR = "LIBERIA"
    LS = "LESOTHO"
    LT = "LITHUANIA"
    LU = "LUXEMBOURG"
    LV = "LATVIA"
    LY = "LIBYA"
    MA = "MOROCCO"
    MC = "MONACO"
    MD = "MOLDOVA, REPUBLIC OF"
    ME = "MONTENEGRO, REPUBLIC OF"
    MG = "MADAGASCAR"
    MH = "MARSHALL ISLANDS"
    MK = "MACEDONIA, REPUBLIC OF"
    ML = "MALI"
    MM = "MYANMAR"
    MN = "MONGOLIA"
    MO = "MACAU"
    MP = "COMMONWEALTH NO. MARIANA ISLANDS"
    MQ = "MARTINIQUE"
    MR = "MAURITANIA"
    MS = "MONTSERRAT"
    MT = "MALTA"
    MU = "MAURITIUS"
    MV = "MALDIVES"
    MW = "MALAWI"
    MX = "MEXICO"
    MY = "MALAYSIA"
    MZ = "MOZAMBIQUE"
    NA = "NAMIBIA"
    NC = "NEW CALEDONIA"
    NE = "NIGER"
    NG = "NIGERIA"
    NI = "NICARAGUA"
    NL = "NETHERLANDS, THE"
    NO = "NORWAY"
    NP = "NEPAL"
    NR = "NAURU, REPUBLIC OF"
    NU = "NIUE"
    NZ = "NEW ZEALAND"
    OM = "OMAN"
    PA = "PANAMA"
    PE = "PERU"
    PF = "TAHITI"
    PG = "PAPUA NEW GUINEA"
    PH = "PHILIPPINES, THE"
    PK = "PAKISTAN"
    PL = "POLAND"
    PR = "PUERTO RICO"
    PT = "PORTUGAL"
    PW = "PALAU"
    PY = "PARAGUAY"
    QA = "QATAR"
    RE = "REUNION, ISLAND OF"
    RO = "ROMANIA"
    RS = "SERBIA, REPUBLIC OF"
    RU = "RUSSIAN FEDERATION, THE"
    RW = "RWANDA"
    SA = "SAUDI ARABIA"
    SB = "SOLOMON ISLANDS"
    SC = "SEYCHELLES"
    SD = "SUDAN"
    SE = "SWEDEN"
    SG = "SINGAPORE"
    SH = "SAINT HELENA"
    SI = "SLOVENIA"
    SK = "SLOVAKIA"
    SL = "SIERRA LEONE"
    SM = "SAN MARINO"
    SN = "SENEGAL"
    SO = "SOMALIA"
    SR = "SURINAME"
    SS = "SOUTH SUDAN"
    ST = "SAO TOME AND PRINCIPE"
    SV = "EL SALVADOR"
    SY = "SYRIA"
    SZ = "SWAZILAND"
    TC = "TURKS AND CAICOS ISLANDS"
    TD = "CHAD"
    TG = "TOGO"
    TH = "THAILAND"
    TJ = "TAJIKISTAN"
    TL = "TIMOR LESTE"
    TN = "TUNISIA"
    TO = "TONGA"
    TR = "TURKEY"
    TT = "TRINIDAD AND TOBAGO"
    TV = "TUVALU"
    TW = "TAIWAN"
    TZ = "TANZANIA"
    UA = "UKRAINE"
    UG = "UGANDA"
    US = "UNITED STATES OF AMERICA"
    UY = "URUGUAY"
    UZ = "UZBEKISTAN"
    VA = "VATICAN CITY STATE"
    VC = "ST. VINCENT"
    VE = "VENEZUELA"
    VG = "VIRGIN ISLANDS (BRITISH)"
    VI = "VIRGIN ISLANDS (US)"
    VN = "VIETNAM"
    VU = "VANUATU"
    WS = "SAMOA"
    XB = "BONAIRE"
    XC = "CURACAO"
    XE = "ST. EUSTATIUS"
    XM = "ST. MAARTEN"
    XN = "NEVIS"
    XS = "SOMALILAND, REP OF (NORTH SOMALIA)"
    XY = "ST. BARTHELEMY"
    YE = "YEMEN, REPUBLIC OF"
    YT = "MAYOTTE"
    ZA = "SOUTH AFRICA"
    ZM = "ZAMBIA"
    ZW = "ZIMBABWE"


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
