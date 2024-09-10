import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    PACKAGE = "PACKAGE"

    """ Unified Packaging type mapping """
    envelope = PACKAGE
    pak = PACKAGE
    tube = PACKAGE
    pallet = PACKAGE
    small_box = PACKAGE
    medium_box = PACKAGE
    your_packaging = PACKAGE


class ShippingCurrency(lib.StrEnum):
    RUB = "3"
    USD = "2"
    EUR = "4"
    AMD = "1"


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    letter_ordered = "88"
    letter_simple = "79"
    letter_valued = "89"
    package_ordered = "93"
    package_simple = "92"
    package_valued = "100"
    parcel_simple = "94"
    parcel_valued = "95"
    postcard_ordered = "91"
    postcard_simple = "90"
    sekogram_simple = "96"
    sprint_simple = "97"
    yes_ordered_value = "99"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    notification = lib.OptionEnum("2", bool)
    ordered_packaging = lib.OptionEnum("3", bool)
    pick_up = lib.OptionEnum("4", bool)
    postmen_delivery_value = lib.OptionEnum("5", bool)
    delivery = lib.OptionEnum("6", bool)
    international_notification = lib.OptionEnum("15", bool)
    domestic_sms = lib.OptionEnum("16", bool)
    international_sms = lib.OptionEnum("17", bool)


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """
    Apply default values to the given options.
    """
    _options = options.copy()

    if package_options is not None:
        _options.update(package_options.content)

    return units.ShippingOptions(_options, ShippingOption)


class ConnectionConfig(lib.Enum):
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)


class TrackingStatus(lib.Enum):
    on_hold = [11]
    delivered = [6]
    in_transit = [1, 2, 7, 5]
    delivery_failed = [10, 3, 4]
    delivery_delayed = [8, 9]


class ShippingCountries(lib.Enum):
    """Country codes"""

    AF = 1
    AL = 2
    DZ = 3
    AS = 4
    AD = 5
    AO = 6
    AG = 9
    AR = 10
    AM = 11
    AW = 12
    AU = 13
    AT = 14
    BS = 16
    BH = 17
    BD = 18
    BB = 19
    BY = 20
    BE = 21
    BZ = 22
    BJ = 23
    BT = 25
    BO = 26
    BA = 28
    BW = 29
    BR = 31
    VG = 33
    BG = 35
    BF = 36
    BI = 37
    CV = 38
    KH = 39
    CM = 40
    CA = 41
    KY = 42
    CF = 43
    TD = 44
    CL = 45
    CN = 46
    HK = 47
    MO = 47
    CO = 51
    KM = 52
    CG = 53
    CK = 54
    CR = 55
    HR = 56
    CU = 57
    CY = 59
    CZ = 60
    CD = 63
    DK = 64
    DJ = 65
    DM = 66
    DO = 67
    EC = 68
    EG = 69
    SV = 70
    GQ = 71
    ER = 72
    EE = 73
    ET = 74
    FJ = 77
    FI = 78
    FR = 79
    GF = 80
    PF = 81
    GA = 83
    GM = 84
    GE = 85
    DE = 86
    GH = 87
    GR = 89
    GD = 91
    GU = 93
    GT = 94
    GN = 96
    GW = 97
    GY = 98
    HT = 99
    HN = 102
    HU = 103
    IS = 104
    IN = 105
    ID = 106
    IQ = 108
    IE = 109
    IL = 111
    IT = 112
    JM = 113
    JP = 114
    JO = 116
    KZ = 117
    KE = 118
    KI = 119
    KW = 120
    KG = 121
    LV = 123
    LB = 124
    LS = 125
    LY = 127
    LI = 128
    LT = 129
    LU = 130
    MG = 131
    MW = 132
    MY = 133
    MV = 134
    ML = 135
    MT = 136
    MH = 137
    MQ = 138
    MR = 139
    MU = 140
    MX = 142
    FM = 143
    MC = 144
    MN = 145
    ME = 146
    MZ = 149
    MM = 150
    NA = 151
    NR = 152
    NP = 153
    NL = 154
    NC = 155
    NZ = 156
    NI = 157
    NE = 158
    NG = 159
    NU = 160
    MP = 162
    NO = 163
    OM = 164
    PK = 165
    PW = 166
    PA = 167
    PG = 168
    PY = 169
    PE = 170
    PH = 171
    PL = 173
    PT = 174
    PR = 175
    QA = 176
    MD = 178
    RO = 179
    RU = 180
    RW = 181
    KN = 185
    VC = 189
    WS = 190
    SM = 191
    ST = 192
    SA = 193
    SN = 194
    RS = 195
    SC = 196
    SL = 197
    SG = 198
    SK = 200
    SI = 201
    SB = 202
    SO = 203
    ZA = 204
    ES = 207
    LK = 208
    PS = 209
    SD = 210
    SR = 211
    SE = 214
    CH = 215
    SY = 216
    TJ = 217
    TH = 218
    TL = 220
    TG = 221
    TO = 223
    TT = 224
    TN = 225
    TM = 227
    TV = 229
    UG = 230
    UA = 231
    AE = 232
    GB = 233
    TZ = 234
    US = 237
    UY = 238
    UZ = 239
    VU = 240
    VE = 241
    VN = 242
    YE = 245
    ZM = 246
    ZW = 247
    BN = 252
    GP = 253
    SZ = 254
    BL = 255
    VA = 256
    KR = 257
    KP = 258
    IR = 454
    TW = 455
    TR = 456
    JE = 458
    MK = 459
    CW = 460
    BM = 464
    LA = 465
    LR = 466
    MA = 467
    LC = 468
    SS = 469
    CI = 470
