import karrio.lib as lib
import karrio.core.units as units


class PackagingType(lib.StrEnum):
    """Carrier specific packaging type"""

    Envelope = "Envelope"
    Pak = "Pak"
    Package = "Package"
    Pallet = "Pallet"

    """ Unified Packaging type mapping """
    envelope = Envelope
    pak = Pak
    tube = Package
    pallet = Pallet
    small_box = Package
    medium_box = Package
    your_packaging = Package


class ShippingService(lib.StrEnum):
    """Carrier specific services"""

    # fmt: off
    eshipper_aramex_economy_document_express = "5000049"
    eshipper_aramex_economy_parcel_express = "5000048"
    eshipper_aramex_priority_letter_express = "5000046"
    eshipper_aramex_priority_parcel_express = "5000047"
    eshipper_canada_post_air_parcel_intl = "5000030"
    eshipper_canada_post_expedited = "5000026"
    eshipper_canada_post_expedited_parcel_usa = "5000032"
    eshipper_canada_post_priority_courier = "5000024"
    eshipper_canada_post_regular = "5000027"
    eshipper_canada_post_small_packet = "5000033"
    eshipper_canada_post_small_packet_international_air = "5000034"
    eshipper_canada_post_small_packet_international_surface = "5000035"
    eshipper_canada_post_surface_parcel_intl = "5000031"
    eshipper_canada_post_xpress_post = "5000025"
    eshipper_canada_post_xpress_post_intl = "5000029"
    eshipper_canada_post_xpress_post_usa = "5000028"
    eshipper_canada_post_xpresspost = "5000181"
    eshipper_canpar_express_letter = "5000129"
    eshipper_canpar_express_pak = "5000130"
    eshipper_canpar_express_parcel = "5000131"
    eshipper_canpar_ground = "5000184"
    eshipper_canpar_international = "5000135"
    eshipper_canpar_select_letter = "5000126"
    eshipper_canpar_select_pak = "5000127"
    eshipper_canpar_select_parcel = "5000128"
    eshipper_canpar_usa = "5000125"
    eshipper_canpar_usa_select_letter = "5000132"
    eshipper_canpar_usa_select_pak = "5000133"
    eshipper_canpar_usa_select_parcel = "5000134"
    eshipper_cpx_canada_post = "5000454"
    eshipper_day_ross_ltl = "5000457"
    eshipper_dhl_dhl_ground = "5000022"
    eshipper_dhl_economy_select = "5000186"
    eshipper_dhl_esi_export = "5000018"
    eshipper_dhl_express_1030am = "5000016"
    eshipper_dhl_express_12pm = "5000017"
    eshipper_dhl_express_900 = "5000180"
    eshipper_dhl_express_9am = "5000014"
    eshipper_dhl_express_envelope = "5000023"
    eshipper_dhl_express_worldwide = "5000015"
    eshipper_dhl_import_express = "5000019"
    eshipper_dhl_import_express_12pm = "5000021"
    eshipper_dhl_import_express_9am = "5000020"
    eshipper_ltl_apex_v = "5000414"
    eshipper_ltl_apex_trucking = "5000120"
    eshipper_ltl_apex_trucking_v = "5000124"
    eshipper_ltl_fastfrate_rail = "5000118"
    eshipper_ltl_kindersley_expedited = "5000420"
    eshipper_ltl_kindersley_rail = "5000121"
    eshipper_ltl_kindersley_regular = "5000421"
    eshipper_ltl_kindersley_road = "5000122"
    eshipper_ltl_kingsway_road = "5000117"
    eshipper_ltl_m_o_eastbound = "5000123"
    eshipper_ltl_mo_rail = "5000116"
    eshipper_ltl_national_fastfreight_rail = "5000114"
    eshipper_ltl_national_fastfreight_road = "5000119"
    eshipper_ltl_vitran_rail = "5000112"
    eshipper_ltl_vitran_road = "5000113"
    eshipper_ltl_western_canada_rail = "5000115"
    eshipper_federal_express_2day_freight = "5000177"
    eshipper_federal_express_3day_freight = "5000178"
    eshipper_federal_express_fedex_2nd_day = "5000173"
    eshipper_federal_express_fedex_economy = "5000174"
    eshipper_federal_express_fedex_first_overnight = "5000170"
    eshipper_federal_express_fedex_ground = "5000171"
    eshipper_federal_express_fedex_ground_us = "5000183"
    eshipper_federal_express_fedex_international_priority = "8000017"
    eshipper_federal_express_fedex_international_priority_express = "8000018"
    eshipper_federal_express_fedex_intl_economy = "5000179"
    eshipper_federal_express_fedex_intl_economy_freight = "5000176"
    eshipper_federal_express_fedex_intl_priority = "8000022"
    eshipper_federal_express_fedex_intl_priority_express = "8000023"
    eshipper_federal_express_fedex_intl_priority_freight = "5000175"
    eshipper_federal_express_fedex_priority = "5000169"
    eshipper_federal_express_fedex_standard_overnight = "5000172"
    eshipper_flashbird_ground = "8000032"
    eshipper_fleet_optics_ground = "5000458"
    eshipper_project44_a_duie_pyle = "5000103"
    eshipper_project44_aaa_cooper_transportation = "5000081"
    eshipper_project44_aberdeen_express = "5000092"
    eshipper_project44_abfs = "5000111"
    eshipper_project44_averitt_express = "5000079"
    eshipper_project44_brown_transfer_company = "5000102"
    eshipper_project44_central_freight_lines = "5000066"
    eshipper_project44_central_transport = "5000085"
    eshipper_project44_chicago_suburban_express = "5000086"
    eshipper_project44_clear_lane_freight = "5000095"
    eshipper_project44_con_way_freight = "5000057"
    eshipper_project44_crosscountry_courier = "5000083"
    eshipper_project44_day_ross = "5000099"
    eshipper_project44_day_ross_v = "5000101"
    eshipper_project44_dayton_freight_lines = "5000072"
    eshipper_project44_dependable_highway_express = "5000091"
    eshipper_project44_dohrn_transfer_company = "5000078"
    eshipper_project44_dugan_truck_line = "5000076"
    eshipper_project44_estes_express_lines = "5000061"
    eshipper_project44_expedited_freight_systems = "5000077"
    eshipper_project44_fedex_freight_canada = "5000105"
    eshipper_project44_fedex_freight_east = "5000059"
    eshipper_project44_fedex_freight_national_canada = "5000107"
    eshipper_project44_fedex_freight_national_usa = "5000108"
    eshipper_project44_fedex_freight_usa = "5000106"
    eshipper_project44_fedex_national = "5000060"
    eshipper_project44_forwardair = "5000062"
    eshipper_project44_frontline_freight = "5000096"
    eshipper_project44_holland_motor_express = "5000051"
    eshipper_project44_lakeville_motor_express = "5000074"
    eshipper_project44_manitoulin_tlx_inc = "5000104"
    eshipper_project44_midwest_motor_express = "5000075"
    eshipper_project44_monroe_transportation_services = "5000087"
    eshipper_project44_n_m_transfer = "5000090"
    eshipper_project44_new_england_motor_freight = "5000064"
    eshipper_project44_new_penn_motor_express = "5000054"
    eshipper_project44_pitt_ohio = "5000071"
    eshipper_project44_polaris = "5000094"
    eshipper_project44_purolator_freight = "5000100"
    eshipper_project44_rl_carriers = "5000058"
    eshipper_project44_roadrunner_transportation_services = "5000052"
    eshipper_project44_saia_motor_freight = "5000067"
    eshipper_project44_southeastern_freight_lines = "5000082"
    eshipper_project44_southwestern_motor_transport = "5000084"
    eshipper_project44_standard_forwarding = "5000093"
    eshipper_project44_total_transportation_distribution = "5000097"
    eshipper_project44_tst_overland_express = "5000098"
    eshipper_project44_ups = "5000073"
    eshipper_project44_usf_reddaway = "5000080"
    eshipper_project44_valley_cartage = "5000089"
    eshipper_project44_vision_express_ltl = "5000065"
    eshipper_project44_ward_trucking = "5000088"
    eshipper_project44_xpo_logistics = "5000110"
    eshipper_project44_xpress_global_systems = "5000109"
    eshipper_project44_yrc = "5000053"
    eshipper_purolator_purolator_express = "5000001"
    eshipper_purolator_purolator_express_1030 = "5000003"
    eshipper_purolator_purolator_express_9am = "5000002"
    eshipper_purolator_purolator_expresscheque = "5000011"
    eshipper_purolator_purolator_ground = "5000010"
    eshipper_purolator_purolator_ground_1030 = "5000013"
    eshipper_purolator_purolator_ground_9am = "5000012"
    eshipper_purolator_puroletter = "5000004"
    eshipper_purolator_puroletter_1030 = "5000006"
    eshipper_purolator_puroletter_9am = "5000005"
    eshipper_purolator_puropak = "5000007"
    eshipper_purolator_puropak_1030 = "5000009"
    eshipper_purolator_puropak_9am = "5000008"
    eshipper_pyk_ground_advantage = "5000459"
    eshipper_pyk_priority_mail = "5000460"
    eshipper_sameday_9am_guaranteed = "5000156"
    eshipper_sameday_am_service = "5000157"
    eshipper_sameday_ground_service = "5000158"
    eshipper_sameday_h1_deliver_to_curbside = "5000159"
    eshipper_sameday_h2_delivery_to_room_of_choice = "5000160"
    eshipper_sameday_h3_delivery_packaging_removal = "5000161"
    eshipper_sameday_h4_delivery_to_curbside = "5000162"
    eshipper_sameday_h5_delivery_to_room_of_choice_2_man = "5000163"
    eshipper_sameday_h6_delivery_packaging_removal_2_man = "5000164"
    eshipper_sameday_ltl_service = "5000165"
    eshipper_sameday_pm_service = "5000166"
    eshipper_sameday_urgent_letter = "5000167"
    eshipper_sameday_urgent_pac = "5000168"
    eshipper_skip = "8000019"
    eshipper_smartepost_intl_dhl_parcel_international_direct_ngr = "8000053"
    eshipper_smartepost_intl_global_mail_business_priority = "5000137"
    eshipper_smartepost_intl_global_mail_business_standard = "5000138"
    eshipper_smartepost_intl_global_mail_packet_plus_priority = "5000139"
    eshipper_smartepost_intl_global_mail_packet_priority = "5000140"
    eshipper_smartepost_intl_global_mail_packet_standard = "5000141"
    eshipper_smartepost_intl_global_mail_parcel_direct_priority_yyz = "5000142"
    eshipper_smartepost_intl_global_mail_parcel_direct_standard_yyz = "5000143"
    eshipper_smartepost_intl_global_mail_parcel_priority = "5000144"
    eshipper_smartepost_intl_global_mail_parcel_standard = "5000145"
    eshipper_ups_expedited = "5000182"
    eshipper_ups_express = "5000036"
    eshipper_ups_express_early_am = "5000040"
    eshipper_ups_ground = "5000043"
    eshipper_ups_second_day_air_am = "5000045"
    eshipper_ups_standard = "5000039"
    eshipper_ups_three_day_select = "5000041"
    eshipper_ups_ups_saver = "5000042"
    eshipper_ups_worldwide_expedited = "5000038"
    eshipper_ups_worldwide_express = "5000037"
    eshipper_ups_worldwide_express_plus = "5000044"
    eshipper_usps_first_class_mail = "5000146"
    eshipper_usps_first_class_package_return_service = "8000002"
    eshipper_usps_library_mail = "5000147"
    eshipper_usps_media_mail = "5000148"
    eshipper_usps_parcel_select = "5000149"
    eshipper_usps_pbx = "5000154"
    eshipper_usps_pbx_lightweight = "5000155"
    eshipper_usps_priority_mail = "5000150"
    eshipper_usps_priority_mail_express = "5000151"
    eshipper_usps_priority_mail_open_and_distribute = "5000152"
    eshipper_usps_priority_mail_return_service = "8000003"
    eshipper_usps_retail_ground_formerly_standard_post = "5000153"
    # fmt: on

    @staticmethod
    def carrier(service: str) -> str:
        return next(
            (_ for _, __ in CARRIER_SERVICES.items() if service in __),
            "5000011",
        )


class ShippingOption(lib.Enum):
    """Carrier specific options"""

    eshipper_signature_required = lib.OptionEnum("signatureRequired", bool)
    eshipper_insurance_type = lib.OptionEnum("insuranceType")
    eshipper_dangerous_goods_type = lib.OptionEnum("dangerousGoodsType", bool)
    eshipper_cod = lib.OptionEnum("cod", float)
    eshipper_is_saturday_service = lib.OptionEnum("isSaturdayService", bool)
    eshipper_hold_for_pickup_required = lib.OptionEnum("holdForPickupRequired", bool)
    eshipper_special_equipment = lib.OptionEnum("specialEquipment", bool)
    eshipper_inside_delivery = lib.OptionEnum("insideDelivery", bool)
    eshipper_delivery_appointment = lib.OptionEnum("deliveryAppointment", bool)
    eshipper_inside_pickup = lib.OptionEnum("insidePickup", bool)
    eshipper_saturday_pickup_required = lib.OptionEnum("saturdayPickupRequired", bool)
    eshipper_stackable = lib.OptionEnum("stackable", bool)

    """ Unified Option type mapping """
    cash_on_delivery = eshipper_cod
    insurance = eshipper_insurance_type
    signature_confirmation = eshipper_signature_required
    saturday_delivery = eshipper_is_saturday_service
    hold_at_location = eshipper_hold_for_pickup_required
    dangerous_good = eshipper_dangerous_goods_type


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
        return key in ShippingOption  # type: ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)


CARRIER_IDS = {
    "5000001": "aramex",
    "5000002": "canadapost",
    "5000003": "canpar",
    "5000017": "day_ross",
    "5000004": "dhl_express",
    "5000011": "eshipper",
    "5000005": "fedex",
    "8000010": "flashbird",
    "56": "fleet_optics",
    "5000008": "project44",
    "5000007": "purolator",
    "5000047": "pyk",
    "5000014": "sameday",
    "5000048": "skip",
    "5000015": "smartepost_intl",
    "5000010": "ups",
    "5000013": "usps",
}

CARRIER_SERVICES = {
    "56": ["5000458", "5000458", "5000458", "5000458"],
    "5000001": [
        "5000047",
        "5000047",
        "5000046",
        "5000046",
        "5000048",
        "5000048",
        "5000049",
        "5000049",
    ],
    "5000002": [
        "5000181",
        "5000181",
        "5000181",
        "5000028",
        "5000028",
        "5000028",
        "5000029",
        "5000029",
        "5000029",
        "5000025",
        "5000025",
        "5000025",
        "5000031",
        "5000031",
        "5000031",
        "5000035",
        "5000035",
        "5000035",
        "5000034",
        "5000034",
        "5000034",
        "5000033",
        "5000033",
        "5000033",
        "5000027",
        "5000027",
        "5000027",
        "5000024",
        "5000024",
        "5000024",
        "5000032",
        "5000032",
        "5000032",
        "5000026",
        "5000026",
        "5000026",
        "5000030",
        "5000030",
        "5000030",
    ],
    "5000003": [
        "5000134",
        "5000134",
        "5000134",
        "5000133",
        "5000133",
        "5000133",
        "5000132",
        "5000132",
        "5000132",
        "5000125",
        "5000125",
        "5000125",
        "5000128",
        "5000128",
        "5000128",
        "5000127",
        "5000127",
        "5000127",
        "5000126",
        "5000126",
        "5000126",
        "5000135",
        "5000135",
        "5000135",
        "5000184",
        "5000184",
        "5000184",
        "5000131",
        "5000131",
        "5000131",
        "5000130",
        "5000130",
        "5000130",
        "5000129",
        "5000129",
        "5000129",
    ],
    "5000004": [
        "5000020",
        "5000020",
        "5000021",
        "5000021",
        "5000019",
        "5000019",
        "5000015",
        "5000015",
        "5000023",
        "5000023",
        "5000014",
        "5000014",
        "5000180",
        "5000180",
        "5000017",
        "5000017",
        "5000016",
        "5000016",
        "5000018",
        "5000018",
        "5000186",
        "5000186",
        "5000022",
        "5000022",
    ],
    "5000005": [
        "5000172",
        "5000172",
        "5000172",
        "5000169",
        "5000169",
        "5000169",
        "5000175",
        "5000175",
        "5000175",
        "8000023",
        "8000023",
        "8000023",
        "8000022",
        "8000022",
        "8000022",
        "5000176",
        "5000176",
        "5000176",
        "5000179",
        "5000179",
        "5000179",
        "8000018",
        "8000018",
        "8000018",
        "8000017",
        "8000017",
        "8000017",
        "5000183",
        "5000183",
        "5000183",
        "5000171",
        "5000171",
        "5000171",
        "5000170",
        "5000170",
        "5000170",
        "5000174",
        "5000174",
        "5000174",
        "5000173",
        "5000173",
        "5000173",
        "5000178",
        "5000178",
        "5000178",
        "5000177",
        "5000177",
        "5000177",
    ],
    "5000007": [
        "5000008",
        "5000008",
        "5000008",
        "5000009",
        "5000009",
        "5000009",
        "5000007",
        "5000007",
        "5000007",
        "5000005",
        "5000005",
        "5000005",
        "5000006",
        "5000006",
        "5000006",
        "5000004",
        "5000004",
        "5000004",
        "5000012",
        "5000012",
        "5000012",
        "5000013",
        "5000013",
        "5000013",
        "5000010",
        "5000010",
        "5000010",
        "5000011",
        "5000011",
        "5000011",
        "5000002",
        "5000002",
        "5000002",
        "5000003",
        "5000003",
        "5000003",
        "5000001",
        "5000001",
        "5000001",
    ],
    "5000008": [
        "5000056",
        "5000053",
        "5000413",
        "5000109",
        "5000110",
        "5000088",
        "5000065",
        "5000089",
        "5000080",
        "5000055",
        "5000073",
        "5000098",
        "5000097",
        "5000093",
        "5000084",
        "5000082",
        "5000067",
        "5000068",
        "5000052",
        "5000058",
        "5000100",
        "5000094",
        "5000071",
        "5000054",
        "5000063",
        "5000064",
        "5000090",
        "5000087",
        "5000075",
        "5000104",
        "5000074",
        "5000069",
        "5000051",
        "5000096",
        "5000062",
        "5000060",
        "5000106",
        "5000108",
        "5000107",
        "5000059",
        "5000070",
        "5000105",
        "5000077",
        "5000061",
        "5000076",
        "5000078",
        "5000091",
        "5000072",
        "5000101",
        "5000099",
        "5000083",
        "5000057",
        "5000095",
        "5000086",
        "5000085",
        "5000066",
        "5000102",
        "5000079",
        "5000111",
        "5000092",
        "5000081",
        "5000103",
    ],
    "5000010": [
        "5000044",
        "5000044",
        "5000044",
        "5000037",
        "5000037",
        "5000037",
        "5000038",
        "5000038",
        "5000038",
        "5000042",
        "5000042",
        "5000042",
        "5000041",
        "5000041",
        "5000041",
        "5000039",
        "5000039",
        "5000039",
        "5000045",
        "5000045",
        "5000045",
        "5000043",
        "5000043",
        "5000043",
        "5000040",
        "5000040",
        "5000040",
        "5000036",
        "5000036",
        "5000036",
        "5000182",
        "5000182",
        "5000182",
    ],
    "5000011": [
        "5000115",
        "5000113",
        "5000112",
        "5000119",
        "5000114",
        "5000116",
        "5000123",
        "5000117",
        "5000122",
        "5000421",
        "5000419",
        "5000121",
        "5000420",
        "5000118",
        "5000124",
        "5000120",
        "5000414",
    ],
    "5000013": [
        "5000153",
        "5000153",
        "8000003",
        "5000152",
        "5000152",
        "5000151",
        "5000151",
        "5000150",
        "5000150",
        "5000155",
        "5000155",
        "5000154",
        "5000154",
        "5000149",
        "5000149",
        "5000148",
        "5000148",
        "5000147",
        "5000147",
        "8000002",
        "5000146",
    ],
    "5000014": [
        "5000168",
        "5000167",
        "5000166",
        "5000165",
        "5000164",
        "5000163",
        "5000162",
        "5000161",
        "5000160",
        "5000159",
        "5000158",
        "5000157",
        "5000156",
    ],
    "5000015": [
        "5000145",
        "5000145",
        "5000145",
        "5000144",
        "5000144",
        "5000144",
        "5000143",
        "5000143",
        "5000143",
        "5000142",
        "5000142",
        "5000142",
        "5000141",
        "5000141",
        "5000141",
        "5000140",
        "5000140",
        "5000140",
        "5000139",
        "5000139",
        "5000139",
        "5000138",
        "5000138",
        "5000138",
        "5000137",
        "5000137",
        "5000137",
        "8000053",
    ],
    "5000016": ["5000454"],
    "5000017": ["5000457"],
    "5000047": ["5000460", "5000460", "5000459", "5000459"],
    "5000048": ["8000020", "8000019"],
    "8000010": ["8000032"],
}


class TrackingStatus(lib.Enum):
    on_hold = ["on_hold"]
    delivered = ["delivered"]
    in_transit = ["in_transit"]
    delivery_failed = ["delivery_failed"]
    delivery_delayed = ["delivery_delayed"]
    out_for_delivery = ["out_for_delivery"]
    ready_for_pickup = ["ready_for_pickup"]
