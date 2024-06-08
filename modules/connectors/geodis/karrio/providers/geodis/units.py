from itertools import count
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class LabelType(lib.Enum):
    PDF = "P"
    PDF_themique = "T"
    Json = "J"
    EPL = "E"
    ZPL_200dpi = "Z"
    ZPL_300dpi = "Y"
    ZPL_600dpi = "W"

    ZPL = ZPL_300dpi
    PNG = PDF


class Incoterm(lib.StrEnum):
    CFR = "COST AND FREIGHT"
    CIF = "COST, INSURANCE AND FREIGHT"
    CIP = "CARRIAGE AND INSURANCE PAID TO"
    CPT = "CARRIAGE PAID TO"
    D = "CARRIAGE DUE"
    DAF = "DELIVERED AT FRONTIER"
    DAP = "DELIVERED AT PLACE"
    DAT = "DELIVERED AT TERMINAL"
    DDP = "DELIVERED DUTY PAID"
    DDU = "DELIVERED DUTY UNPAID"
    DEQ = "DELIVERED EX QUAY"
    DES = "DELIVERED EX SHIP"
    EXW = "EX WORKS"
    FAS = "FREE ALONGSIDE SHIP"
    FCA = "FREE CARRIER"
    FDC = "FRANCO DOMICILE DEDOUANE"
    FDU = "FRANCO DOMICILE NON DEDOUANE"
    FOB = "FREE ON BOARD"
    P = "CARRIAGE PAID"


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


class ConnectionConfig(lib.Enum):
    agency_code = lib.OptionEnum("agency_code")


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    geodis_EXP = "EXP"
    geodis_MES = "MES"
    geodis_express_france = "NTX"
    geodis_retour_trans_fr_messagerie_plus = "ENL"


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    geodis_web_appointment = lib.OptionEnum("RDW", bool)
    geodis_telephone_appointment = lib.OptionEnum("RDT", bool)
    geodis_pick_up_at_a_geodis_agency = lib.OptionEnum("BRT", bool)
    geodis_desired_date_of_delivery = lib.OptionEnum("DSL", bool)
    geodis_delivery_on_a_saturday_morning = lib.OptionEnum("SAT", bool)

    geodis_validate_envoi = lib.OptionEnum("validate_envoi", bool)
    geodis_no_recepisse = lib.OptionEnum("no_recepisse")
    geodis_instruction_enlevement = lib.OptionEnum("instruction_enlevement")
    geodis_date_livraison = lib.OptionEnum("date_livraison")
    geodis_heure_livraison = lib.OptionEnum("heure_livraison")
    geodis_instruction_livraison = lib.OptionEnum("instruction_livraison")

    """ Unified Option type mapping """
    saturday_delivery = geodis_delivery_on_a_saturday_morning


def shipping_options_initializer(
    options: dict,
    package_options: units.ShippingOptions = None,
) -> units.ShippingOptions:
    """
    Apply default values to the given options.
    """

    if package_options is not None:
        options.update(package_options.content)

    def items_filter(key: str) -> bool:
        return key in ["RDW" "RDT", "BRT", "DSL", "SAT"]

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


LABTEST_RATE_SHEET = [
    # weight, 1001, 1002, 1003, 1007
    (0.5, 49, 45, 53, 57),
    (1, 52, 49, 58.25, 62.33),
    (2, 56.85, 52.3, 65.52, 73.55),
    (3, 64.27, 59.45, 71.78, 84.55),
    (4, 70.92, 65.85, 77.5, 101.54),
    (5, 81.85, 76.36, 89.04, 114.52),
    (6, 86.59, 80.92, 93.86, 124.86),
    (7, 92.78, 85.65, 101.12, 136.96),
    (8, 95.04, 87.82, 108.65, 140.76),
    (9, 98.29, 90.96, 111.24, 155.3),
    (10, 99.38, 92, 113.76, 156.01),
    (11, 99.92, 92.52, 114.2, 158.89),
    (12, 100.83, 93.39, 115.23, 163.05),
    (13, 110.65, 102.85, 126.47, 177.87),
    (14, 117.14, 109.09, 137.07, 189.05),
    (15, 119.56, 111.42, 139.25, 211.16),
    (16, 130.04, 121.5, 144.96, 217.07),
    (17, 131, 122.42, 148.01, 221.99),
    (18, 133.1, 124.45, 150.56, 230.63),
    (19, 133.96, 125.27, 156.72, 240.79),
    (20, 136.25, 127.48, 157.88, 253.64),
    (21, 141.53, 132.56, 161.94, 268.15),
    (22, 142.47, 133.46, 162.8, 270.95),
    (23, 143.33, 134.29, 163.58, 271.74),
    (24, 144.1, 135.03, 164.64, 276.63),
    (25, 145.46, 136.34, 165.95, 279.38),
    (26, 179.69, 169.28, 207.52, 305.69),
    (27, 187.89, 177.17, 218.5, 313.19),
    (28, 191.51, 180.65, 219.41, 331.85),
    (29, 192.26, 181.37, 223.14, 347.95),
    (30, 193.03, 182.12, 227.02, 350),
    (31, 196.46, 185.42, 235.14, 350.23),
    (32, 197.18, 186.11, 235.78, 350.88),
    (33, 198.05, 186.95, 241.1, 358.36),
    (34, 198.82, 187.68, 243.97, 363.37),
    (35, 199.55, 188.39, 251.02, 364.93),
    (36, 200.36, 189.17, 252.83, 370.29),
    (37, 201.06, 189.84, 253.53, 376.34),
    (38, 209.95, 198.39, 259.95, 385.32),
    (39, 219.27, 207.36, 264.51, 387.14),
    (40, 220.5, 208.54, 275.76, 400.96),
    (41, 221.3, 209.31, 277.4, 403.67),
    (42, 222.24, 210.21, 279.07, 436),
    (43, 227.36, 215.14, 289.98, 452.97),
    (44, 235.77, 223.24, 297.17, 453.75),
    (45, 236.9, 224.33, 298.18, 454.39),
    (46, 238.34, 225.71, 298.96, 455.58),
    (47, 239.04, 226.38, 305.55, 474.31),
    (48, 239.78, 227.1, 310.68, 496.66),
    (49, 242.16, 229.39, 311.31, 499.19),
    (50, 245.52, 232.62, 312.11, 499.92),
    (51, 247.86, 234.87, 322.96, 501.23),
    (52, 248.18, 235.17, 323.27, 501.54),
    (53, 255.48, 242.21, 327.89, 521.4),
    (54, 255.81, 242.52, 328.22, 521.74),
    (55, 261.77, 248.25, 332, 524.7),
    (56, 262.08, 248.55, 332.31, 525.02),
    (57, 268.97, 255.18, 336.38, 525.95),
    (58, 269.28, 255.48, 336.69, 526.26),
    (59, 279.46, 265.28, 340.87, 527.17),
    (60, 279.94, 265.74, 341.34, 527.65),
    (61, 280.79, 266.55, 342.9, 528.51),
    (62, 281.26, 267, 343.36, 528.99),
    (63, 282.09, 267.81, 345.96, 552.99),
    (64, 282.52, 268.22, 346.39, 553.42),
    (65, 284.01, 269.65, 374.39, 561.44),
    (66, 284.32, 269.95, 374.7, 561.76),
    (67, 285.81, 271.38, 402.7, 569.78),
    (68, 286.34, 271.9, 403.23, 570.32),
    (69, 287.84, 273.34, 431.24, 578.35),
    (70, 288.34, 273.82, 431.74, 578.86),
]


DEFAULT_SERVICES = [
    models.ServiceLevel(
        service_name="GEODIS Express",
        service_code="geodis_EXP",
        currency="USD",
        domicile=True,
        international=True,
        zones=[
            *[
                models.ServiceZone(
                    label="1001",
                    rate=rate[1],
                    max_weight=rate[0],
                    country_codes=["BE", "FR", "DE", "IE", "IT", "LU", "NL", "MC"],
                )
                for rate in LABTEST_RATE_SHEET
            ],
            *[
                models.ServiceZone(
                    label="1002",
                    rate=rate[2],
                    max_weight=rate[0],
                    country_codes=["GB"],
                )
                for rate in LABTEST_RATE_SHEET
            ],
            *[
                models.ServiceZone(
                    label="1003",
                    rate=rate[3],
                    max_weight=rate[0],
                    country_codes=["AT", "DK", "ES", "FI", "GR", "PT", "SE"],
                )
                for rate in LABTEST_RATE_SHEET
            ],
            *[
                models.ServiceZone(
                    label="1007",
                    rate=rate[4],
                    max_weight=rate[0],
                    country_codes=[
                        "CZ",
                        "HU",
                        "LV",
                        "LT",
                        "PL",
                        "SK",
                        "SI",
                        "BG",
                        "RO",
                        "HR",
                        "EE",
                    ],
                )
                for rate in LABTEST_RATE_SHEET
            ],
        ],
        min_weight=0.5,
        max_weight=70.0,
        weight_unit=units.WeightUnit.LB,
        max_length=68.0,
        max_height=118.0,
        dimension_unit=units.DimensionUnit.CM,
        transit_days=6,
    ),
]
