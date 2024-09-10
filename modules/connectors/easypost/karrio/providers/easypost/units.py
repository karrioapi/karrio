import re
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models


class LabelType(lib.Enum):
    PDF = "PDF"
    ZPL = "ZPL"
    PNG = "PNG"
    EPL2 = "EPL2"


class PaymentType(lib.StrEnum):
    sender = "SENDER"
    third_party = "THIRD_PARTY"
    receiver = "RECEIVER"
    collect = "COLLECT"

    recipient = receiver


class PackagingType(lib.Enum):
    easypost_dhl_jumbo_document = "JumboDocument"
    easypost_dhl_jumbo_parcel = "JumboParcel"
    easypost_dhl_document = "Document"
    easypost_dhl_dhl_flyer = "DHLFlyer"
    easypost_dhl_domestic = "Domestic"
    easypost_dhl_express_document = "ExpressDocument"
    easypost_dhl_dhl_express_envelope = "DHLExpressEnvelop"
    easypost_dhl_jumbo_box = "JumboBox"
    easypost_dhl_jumbo_junior_document = "JumboJuniorDocume"
    easypost_dhl_junior_jumbo_box = "JuniorJumboBox"
    easypost_dhl_jumbo_junior_parcel = "JumboJuniorParcel"
    easypost_dhl_other_dhl_packaging = "OtherDHLPackaging"
    easypost_dhl_parcel = "Parcel"
    easypost_dhl_your_packaging = "YourPackaging"
    easypost_dpd_uk_parcel = "Parcel"
    easypost_dpd_uk_pallet = "Pallet"
    easypost_dpd_uk_express_pak = "ExpressPak"
    easypost_dpd_uk_freight_parcel = "FreightParcel"
    easypost_dpd_uk_freight = "Freight"
    easypost_estafeta_envelope = "ENVELOPE"
    easypost_estafeta_parcel = "PARCEL"
    easypost_fastway_parcel = "Parcel"
    easypost_fastway_a2_satchel = "A2 (Satchel)"
    easypost_fastway_a3_satchel = "A3 (Satchel)"
    easypost_fastway_a4_satchel_not_available_in_australia = (
        "A4 (Satchel, not available in Australia)"
    )
    easypost_fastway_a5_satchel_not_available_in_south_africa = (
        "A5 (Satchel, not available in South Africa)"
    )
    easypost_fastway_boxsml = "BOXSML"
    easypost_fastway_boxmed = "BOXMED"
    easypost_fastway_boxlrg = "BOXLRG"
    easypost_fedex_envelope = "FedExEnvelope"
    easypost_fedex_box = "FedExBox"
    easypost_fedex_pak = "FedExPak"
    easypost_fedex_tube = "FedExTube"
    easypost_fedex10kg_box = "FedEx10kgBox"
    easypost_fedex25kg_box = "FedEx25kgBox"
    easypost_fedex_small_box = "FedExSmallBox"
    easypost_fedex_medium_box = "FedExMediumBox"
    easypost_fedex_large_box = "FedExLargeBox"
    easypost_fedex_extra_large_box = "FedExExtraLargeBox"
    easypost_interlink_parcel = "Parcel"
    easypost_interlink_pallet = "Pallet"
    easypost_interlink_express_pak = "ExpressPak"
    easypost_interlink_freight_parcel = "FreightParcel"
    easypost_interlink_freight = "Freight"
    easypost_lasership_envelope = "Envelope"
    easypost_lasership_custom = "Custom"
    easypost_ontrac_letter = "Letter"
    easyppost_purolator_customer_packaging = "CustomerPackaging"
    easyppost_purolator_express_pack = "ExpressPack"
    easyppost_purolator_express_box = "ExpressBox"
    easyppost_purolator_express_envelope = "ExpressEnvelope"
    easyposrt_royalmail_letter = "Letter"
    easyposrt_royalmail_large_letter = "LargeLetter"
    easyposrt_royalmail_small_parcel = "SmallParcel"
    easyposrt_royalmail_medium_parcel = "MediumParcel"
    easyposrt_royalmail_parcel_for_use_with_royal_mail24_or_royal_mail48 = (
        "Parcel (for use with RoyalMail24 or RoyalMail48)"
    )
    easypost_seko_bag = "Bag"
    easypost_seko_box = "Box"
    easypost_seko_carton = "Carton"
    easypost_seko_container = "Container"
    easypost_seko_crate = "Crate"
    easypost_seko_envelope = "Envelope"
    easypost_seko_pail = "Pail"
    easypost_seko_pallet = "Pallet"
    easypost_seko_satchel = "Satchel"
    easypost_seko_tub = "Tub"
    easyport_startrack_carton = "Carton"
    easyport_startrack_pallet = "Pallet"
    easyport_startrack_satchel = "Satchel"
    easyport_startrack_bag = "Bag"
    easyport_startrack_envelope = "Envelope"
    easyport_startrack_item = "Item"
    easyport_startrack_jiffybag = "Jiffybag"
    easyport_startrack_skid = "Skid"
    easyport_tforce_parcel = "Parcel"
    easyport_tforce_letter = "Letter"
    easypost_ups_letter = "UPSLetter"
    easypost_ups_express_box = "UPSExpressBox"
    easypost_ups_25kg_box = "UPS25kgBox"
    easypost_ups_10kg_box = "UPS10kgBox"
    easypost_ups_tube = "Tube"
    easypost_ups_pak = "Pak"
    easypost_ups_small_express_box = "SmallExpressBox"
    easypost_ups_medium_express_box = "MediumExpressBox"
    easypost_ups_large_express_box = "LargeExpressBox"
    easyport_usps_card = "Card"
    easyport_usps_letter = "Letter"
    easyport_usps_flat = "Flat"
    easyport_usps_flat_rate_envelope = "FlatRateEnvelope"
    easyport_usps_flat_rate_legal_envelope = "FlatRateLegalEnvelope"
    easyport_usps_flat_rate_padded_envelope = "FlatRatePaddedEnvelope"
    easyport_usps_flat_rate_gift_card_envelope = "FlatRateGiftCardEnvelope"
    easyport_usps_flat_rate_window_envelope = "FlatRateWindowEnvelope"
    easyport_usps_flat_rate_cardboard_envelope = "FlatRateCardboardEnvelope"
    easyport_usps_small_flat_rate_envelope = "SmallFlatRateEnvelope"
    easyport_usps_parcel = "Parcel"
    easyport_usps_large_parcel = "LargeParcel"
    easyport_usps_irregular_parcel = "IrregularParcel"
    easyport_usps_soft_pack = "SoftPack"
    easyport_usps_small_flat_rate_box = "SmallFlatRateBox"
    easyport_usps_medium_flat_rate_box = "MediumFlatRateBox"
    easyport_usps_large_flat_rate_box = "LargeFlatRateBox"
    easyport_usps_large_flat_rate_box_apofpo = "LargeFlatRateBoxAPOFPO"
    easyport_usps_large_flat_rate_board_game_box = "LargeFlatRateBoardGameBox"
    easyport_usps_regional_rate_box_a = "RegionalRateBoxA"
    easyport_usps_regional_rate_box_b = "RegionalRateBoxB"
    easyport_usps_flat_tub_tray_box = "FlatTubTrayBox"
    easyport_usps_emm_tray_box = "EMMTrayBox"
    easyport_usps_full_tray_box = "FullTrayBox"
    easyport_usps_half_tray_box = "HalfTrayBox"
    easyport_usps_pmod_sack = "PMODSack"

    """ Unified Packaging type mapping """
    envelope = None
    pak = envelope
    tube = envelope
    pallet = envelope
    small_box = envelope
    medium_box = envelope
    your_packaging = envelope


class Service(lib.StrEnum):
    easypost_amazonmws_ups_rates = "UPS Rates"
    easypost_amazonmws_usps_rates = "USPS Rates"
    easypost_amazonmws_fedex_rates = "FedEx Rates"
    easypost_amazonmws_ups_labels = "UPS Labels"
    easypost_amazonmws_usps_labels = "USPS Labels"
    easypost_amazonmws_fedex_labels = "FedEx Labels"
    easypost_amazonmws_ups_tracking = "UPS Tracking"
    easypost_amazonmws_usps_tracking = "USPS Tracking"
    easypost_amazonmws_fedex_tracking = "FedEx Tracking"
    easypost_apc_parcel_connect_book_service = "parcelConnectBookService"
    easypost_apc_parcel_connect_expedited_ddp = "parcelConnectExpeditedDDP"
    easypost_apc_parcel_connect_expedited_ddu = "parcelConnectExpeditedDDU"
    easypost_apc_parcel_connect_priority_ddp = "parcelConnectPriorityDDP"
    easypost_apc_parcel_connect_priority_ddp_delcon = "parcelConnectPriorityDDPDelcon"
    easypost_apc_parcel_connect_priority_ddu = "parcelConnectPriorityDDU"
    easypost_apc_parcel_connect_priority_ddu_delcon = "parcelConnectPriorityDDUDelcon"
    easypost_apc_parcel_connect_priority_ddupqw = "parcelConnectPriorityDDUPQW"
    easypost_apc_parcel_connect_standard_ddu = "parcelConnectStandardDDU"
    easypost_apc_parcel_connect_standard_ddupqw = "parcelConnectStandardDDUPQW"
    easypost_apc_parcel_connect_packet_ddu = "parcelConnectPacketDDU"
    easypost_asendia_pmi = "PMI"
    easypost_asendia_e_packet = "ePacket"
    easypost_asendia_ipa = "IPA"
    easypost_asendia_isal = "ISAL"
    easypost_asendia_us_ads = "ADS"
    easypost_asendia_us_air_freight_inbound = "AirFreightInbound"
    easypost_asendia_us_air_freight_outbound = "AirFreightOutbound"
    easypost_asendia_us_domestic_bound_printer_matter_expedited = (
        "AsendiaDomesticBoundPrinterMatterExpedited"
    )
    easypost_asendia_us_domestic_bound_printer_matter_ground = (
        "AsendiaDomesticBoundPrinterMatterGround"
    )
    easypost_asendia_us_domestic_flats_expedited = "AsendiaDomesticFlatsExpedited"
    easypost_asendia_us_domestic_flats_ground = "AsendiaDomesticFlatsGround"
    easypost_asendia_us_domestic_parcel_ground_over1lb = (
        "AsendiaDomesticParcelGroundOver1lb"
    )
    easypost_asendia_us_domestic_parcel_ground_under1lb = (
        "AsendiaDomesticParcelGroundUnder1lb"
    )
    easypost_asendia_us_domestic_parcel_max_over1lb = "AsendiaDomesticParcelMAXOver1lb"
    easypost_asendia_us_domestic_parcel_max_under1lb = (
        "AsendiaDomesticParcelMAXUnder1lb"
    )
    easypost_asendia_us_domestic_parcel_over1lb_expedited = (
        "AsendiaDomesticParcelOver1lbExpedited"
    )
    easypost_asendia_us_domestic_parcel_under1lb_expedited = (
        "AsendiaDomesticParcelUnder1lbExpedited"
    )
    easypost_asendia_us_domestic_promo_parcel_expedited = (
        "AsendiaDomesticPromoParcelExpedited"
    )
    easypost_asendia_us_domestic_promo_parcel_ground = (
        "AsendiaDomesticPromoParcelGround"
    )
    easypost_asendia_us_bulk_freight = "BulkFreight"
    easypost_asendia_us_business_mail_canada_lettermail = "BusinessMailCanadaLettermail"
    easypost_asendia_us_business_mail_canada_lettermail_machineable = (
        "BusinessMailCanadaLettermailMachineable"
    )
    easypost_asendia_us_business_mail_economy = "BusinessMailEconomy"
    easypost_asendia_us_business_mail_economy_lp_wholesale = (
        "BusinessMailEconomyLPWholesale"
    )
    easypost_asendia_us_business_mail_economy_sp_wholesale = (
        "BusinessMailEconomySPWholesale"
    )
    easypost_asendia_us_business_mail_ipa = "BusinessMailIPA"
    easypost_asendia_us_business_mail_isal = "BusinessMailISAL"
    easypost_asendia_us_business_mail_priority = "BusinessMailPriority"
    easypost_asendia_us_business_mail_priority_lp_wholesale = (
        "BusinessMailPriorityLPWholesale"
    )
    easypost_asendia_us_business_mail_priority_sp_wholesale = (
        "BusinessMailPrioritySPWholesale"
    )
    easypost_asendia_us_marketing_mail_canada_personalized_lcp = (
        "MarketingMailCanadaPersonalizedLCP"
    )
    easypost_asendia_us_marketing_mail_canada_personalized_machineable = (
        "MarketingMailCanadaPersonalizedMachineable"
    )
    easypost_asendia_us_marketing_mail_canada_personalized_ndg = (
        "MarketingMailCanadaPersonalizedNDG"
    )
    easypost_asendia_us_marketing_mail_economy = "MarketingMailEconomy"
    easypost_asendia_us_marketing_mail_ipa = "MarketingMailIPA"
    easypost_asendia_us_marketing_mail_isal = "MarketingMailISAL"
    easypost_asendia_us_marketing_mail_priority = "MarketingMailPriority"
    easypost_asendia_us_publications_canada_lcp = "PublicationsCanadaLCP"
    easypost_asendia_us_publications_canada_ndg = "PublicationsCanadaNDG"
    easypost_asendia_us_publications_economy = "PublicationsEconomy"
    easypost_asendia_us_publications_ipa = "PublicationsIPA"
    easypost_asendia_us_publications_isal = "PublicationsISAL"
    easypost_asendia_us_publications_priority = "PublicationsPriority"
    easypost_asendia_us_epaq_elite = "ePAQElite"
    easypost_asendia_us_epaq_elite_custom = "ePAQEliteCustom"
    easypost_asendia_us_epaq_elite_dap = "ePAQEliteDAP"
    easypost_asendia_us_epaq_elite_ddp = "ePAQEliteDDP"
    easypost_asendia_us_epaq_elite_ddp_oversized = "ePAQEliteDDPOversized"
    easypost_asendia_us_epaq_elite_dpd = "ePAQEliteDPD"
    easypost_asendia_us_epaq_elite_direct_access_canada_ddp = (
        "ePAQEliteDirectAccessCanadaDDP"
    )
    easypost_asendia_us_epaq_elite_oversized = "ePAQEliteOversized"
    easypost_asendia_us_epaq_plus = "ePAQPlus"
    easypost_asendia_us_epaq_plus_custom = "ePAQPlusCustom"
    easypost_asendia_us_epaq_plus_customs_prepaid = "ePAQPlusCustomsPrepaid"
    easypost_asendia_us_epaq_plus_dap = "ePAQPlusDAP"
    easypost_asendia_us_epaq_plus_ddp = "ePAQPlusDDP"
    easypost_asendia_us_epaq_plus_economy = "ePAQPlusEconomy"
    easypost_asendia_us_epaq_plus_wholesale = "ePAQPlusWholesale"
    easypost_asendia_us_epaq_pluse_packet = "ePAQPlusePacket"
    easypost_asendia_us_epaq_pluse_packet_canada_customs_pre_paid = (
        "ePAQPlusePacketCanadaCustomsPrePaid"
    )
    easypost_asendia_us_epaq_pluse_packet_canada_ddp = "ePAQPlusePacketCanadaDDP"
    easypost_asendia_us_epaq_returns_domestic = "ePAQReturnsDomestic"
    easypost_asendia_us_epaq_returns_international = "ePAQReturnsInternational"
    easypost_asendia_us_epaq_select = "ePAQSelect"
    easypost_asendia_us_epaq_select_custom = "ePAQSelectCustom"
    easypost_asendia_us_epaq_select_customs_prepaid_by_shopper = (
        "ePAQSelectCustomsPrepaidByShopper"
    )
    easypost_asendia_us_epaq_select_dap = "ePAQSelectDAP"
    easypost_asendia_us_epaq_select_ddp = "ePAQSelectDDP"
    easypost_asendia_us_epaq_select_ddp_direct_access = "ePAQSelectDDPDirectAccess"
    easypost_asendia_us_epaq_select_direct_access = "ePAQSelectDirectAccess"
    easypost_asendia_us_epaq_select_direct_access_canada_ddp = (
        "ePAQSelectDirectAccessCanadaDDP"
    )
    easypost_asendia_us_epaq_select_economy = "ePAQSelectEconomy"
    easypost_asendia_us_epaq_select_oversized = "ePAQSelectOversized"
    easypost_asendia_us_epaq_select_oversized_ddp = "ePAQSelectOversizedDDP"
    easypost_asendia_us_epaq_select_pmei = "ePAQSelectPMEI"
    easypost_asendia_us_epaq_select_pmei_canada_customs_pre_paid = (
        "ePAQSelectPMEICanadaCustomsPrePaid"
    )
    easypost_asendia_us_epaq_select_pmeipc_postage = "ePAQSelectPMEIPCPostage"
    easypost_asendia_us_epaq_select_pmi = "ePAQSelectPMI"
    easypost_asendia_us_epaq_select_pmi_canada_customs_prepaid = (
        "ePAQSelectPMICanadaCustomsPrepaid"
    )
    easypost_asendia_us_epaq_select_pmi_canada_ddp = "ePAQSelectPMICanadaDDP"
    easypost_asendia_us_epaq_select_pmi_non_presort = "ePAQSelectPMINonPresort"
    easypost_asendia_us_epaq_select_pmipc_postage = "ePAQSelectPMIPCPostage"
    easypost_asendia_us_epaq_standard = "ePAQStandard"
    easypost_asendia_us_epaq_standard_custom = "ePAQStandardCustom"
    easypost_asendia_us_epaq_standard_economy = "ePAQStandardEconomy"
    easypost_asendia_us_epaq_standard_ipa = "ePAQStandardIPA"
    easypost_asendia_us_epaq_standard_isal = "ePAQStandardISAL"
    easypost_asendia_us_epaq_select_pmei_non_presort = "ePaqSelectPMEINonPresort"
    easypost_australiapost_express_post = "ExpressPost"
    easypost_australiapost_express_post_signature = "ExpressPostSignature"
    easypost_australiapost_parcel_post = "ParcelPost"
    easypost_australiapost_parcel_post_signature = "ParcelPostSignature"
    easypost_australiapost_parcel_post_extra = "ParcelPostExtra"
    easypost_australiapost_parcel_post_wine_plus_signature = (
        "ParcelPostWinePlusSignature"
    )
    easypost_axlehire_delivery = "AxleHireDelivery"
    easypost_better_trucks_next_day = "NEXT_DAY"
    easypost_bond_standard = "Standard"
    easypost_canadapost_regular_parcel = "RegularParcel"
    easypost_canadapost_expedited_parcel = "ExpeditedParcel"
    easypost_canadapost_xpresspost = "Xpresspost"
    easypost_canadapost_xpresspost_certified = "XpresspostCertified"
    easypost_canadapost_priority = "Priority"
    easypost_canadapost_library_books = "LibraryBooks"
    easypost_canadapost_expedited_parcel_usa = "ExpeditedParcelUSA"
    easypost_canadapost_priority_worldwide_envelope_usa = "PriorityWorldwideEnvelopeUSA"
    easypost_canadapost_priority_worldwide_pak_usa = "PriorityWorldwidePakUSA"
    easypost_canadapost_priority_worldwide_parcel_usa = "PriorityWorldwideParcelUSA"
    easypost_canadapost_small_packet_usa_air = "SmallPacketUSAAir"
    easypost_canadapost_tracked_packet_usa = "TrackedPacketUSA"
    easypost_canadapost_tracked_packet_usalvm = "TrackedPacketUSALVM"
    easypost_canadapost_xpresspost_usa = "XpresspostUSA"
    easypost_canadapost_xpresspost_international = "XpresspostInternational"
    easypost_canadapost_international_parcel_air = "InternationalParcelAir"
    easypost_canadapost_international_parcel_surface = "InternationalParcelSurface"
    easypost_canadapost_priority_worldwide_envelope_intl = (
        "PriorityWorldwideEnvelopeIntl"
    )
    easypost_canadapost_priority_worldwide_pak_intl = "PriorityWorldwidePakIntl"
    easypost_canadapost_priority_worldwide_parcel_intl = "PriorityWorldwideParcelIntl"
    easypost_canadapost_small_packet_international_air = "SmallPacketInternationalAir"
    easypost_canadapost_small_packet_international_surface = (
        "SmallPacketInternationalSurface"
    )
    easypost_canadapost_tracked_packet_international = "TrackedPacketInternational"
    easypost_canpar_ground = "Ground"
    easypost_canpar_select_letter = "SelectLetter"
    easypost_canpar_select_pak = "SelectPak"
    easypost_canpar_select = "Select"
    easypost_canpar_overnight_letter = "OvernightLetter"
    easypost_canpar_overnight_pak = "OvernightPak"
    easypost_canpar_overnight = "Overnight"
    easypost_canpar_select_usa = "SelectUSA"
    easypost_canpar_usa_pak = "USAPak"
    easypost_canpar_usa_letter = "USALetter"
    easypost_canpar_usa = "USA"
    easypost_canpar_international = "International"
    easypost_cdl_distribution = "DISTRIBUTION"
    easypost_cdl_same_day = "Same Day"
    easypost_courier_express_basic_parcel = "BASIC_PARCEL"
    easypost_couriersplease_domestic_priority_signature = "DomesticPrioritySignature"
    easypost_couriersplease_domestic_priority = "DomesticPriority"
    easypost_couriersplease_domestic_off_peak_signature = "DomesticOffPeakSignature"
    easypost_couriersplease_domestic_off_peak = "DomesticOffPeak"
    easypost_couriersplease_gold_domestic_signature = "GoldDomesticSignature"
    easypost_couriersplease_gold_domestic = "GoldDomestic"
    easypost_couriersplease_australian_city_express_signature = (
        "AustralianCityExpressSignature"
    )
    easypost_couriersplease_australian_city_express = "AustralianCityExpress"
    easypost_couriersplease_domestic_saver_signature = "DomesticSaverSignature"
    easypost_couriersplease_domestic_saver = "DomesticSaver"
    easypost_couriersplease_road_express = "RoadExpress"
    easypost_couriersplease_5_kg_satchel = "5KgSatchel"
    easypost_couriersplease_3_kg_satchel = "3KgSatchel"
    easypost_couriersplease_1_kg_satchel = "1KgSatchel"
    easypost_couriersplease_5_kg_satchel_atl = "5KgSatchelATL"
    easypost_couriersplease_3_kg_satchel_atl = "3KgSatchelATL"
    easypost_couriersplease_1_kg_satchel_atl = "1KgSatchelATL"
    easypost_couriersplease_500_gram_satchel = "500GramSatchel"
    easypost_couriersplease_500_gram_satchel_atl = "500GramSatchelATL"
    easypost_couriersplease_25_kg_parcel = "25KgParcel"
    easypost_couriersplease_10_kg_parcel = "10KgParcel"
    easypost_couriersplease_5_kg_parcel = "5KgParcel"
    easypost_couriersplease_3_kg_parcel = "3KgParcel"
    easypost_couriersplease_1_kg_parcel = "1KgParcel"
    easypost_couriersplease_500_gram_parcel = "500GramParcel"
    easypost_couriersplease_500_gram_parcel_atl = "500GramParcelATL"
    easypost_couriersplease_express_international_priority = (
        "ExpressInternationalPriority"
    )
    easypost_couriersplease_international_saver = "InternationalSaver"
    easypost_couriersplease_international_express_import = "InternationalExpressImport"
    easypost_couriersplease_domestic_tracked = "DomesticTracked"
    easypost_couriersplease_international_economy = "InternationalEconomy"
    easypost_couriersplease_international_standard = "InternationalStandard"
    easypost_couriersplease_international_express = "InternationalExpress"
    easypost_daipost_domestic_tracked = "DomesticTracked"
    easypost_daipost_international_economy = "InternationalEconomy"
    easypost_daipost_international_standard = "InternationalStandard"
    easypost_daipost_international_express = "InternationalExpress"
    easypost_deutschepost_packet_plus = "PacketPlus"
    easypost_deutschepost_uk_priority_packet_plus = "PriorityPacketPlus"
    easypost_deutschepost_uk_priority_packet = "PriorityPacket"
    easypost_deutschepost_uk_priority_packet_tracked = "PriorityPacketTracked"
    easypost_deutschepost_uk_business_mail_registered = "BusinessMailRegistered"
    easypost_deutschepost_uk_standard_packet = "StandardPacket"
    easypost_deutschepost_uk_business_mail_standard = "BusinessMailStandard"
    easypost_dhl_ecom_asia_packet = "Packet"
    easypost_dhl_ecom_asia_packet_plus = "PacketPlus"
    easypost_dhl_ecom_asia_parcel_direct = "ParcelDirect"
    easypost_dhl_ecom_asia_parcel_direct_expedited = "ParcelDirectExpedited"
    easypost_dhl_ecom_parcel_expedited = "DHLParcelExpedited"
    easypost_dhl_ecom_parcel_expedited_max = "DHLParcelExpeditedMax"
    easypost_dhl_ecom_parcel_ground = "DHLParcelGround"
    easypost_dhl_ecom_bpm_expedited = "DHLBPMExpedited"
    easypost_dhl_ecom_bpm_ground = "DHLBPMGround"
    easypost_dhl_ecom_parcel_international_direct = "DHLParcelInternationalDirect"
    easypost_dhl_ecom_parcel_international_standard = "DHLParcelInternationalStandard"
    easypost_dhl_ecom_packet_international = "DHLPacketInternational"
    easypost_dhl_ecom_parcel_international_direct_priority = (
        "DHLParcelInternationalDirectPriority"
    )
    easypost_dhl_ecom_parcel_international_direct_standard = (
        "DHLParcelInternationalDirectStandard"
    )
    easypost_dhl_express_break_bulk_economy = "BreakBulkEconomy"
    easypost_dhl_express_break_bulk_express = "BreakBulkExpress"
    easypost_dhl_express_domestic_economy_select = "DomesticEconomySelect"
    easypost_dhl_express_domestic_express = "DomesticExpress"
    easypost_dhl_express_domestic_express1030 = "DomesticExpress1030"
    easypost_dhl_express_domestic_express1200 = "DomesticExpress1200"
    easypost_dhl_express_economy_select = "EconomySelect"
    easypost_dhl_express_economy_select_non_doc = "EconomySelectNonDoc"
    easypost_dhl_express_euro_pack = "EuroPack"
    easypost_dhl_express_europack_non_doc = "EuropackNonDoc"
    easypost_dhl_express_express1030 = "Express1030"
    easypost_dhl_express_express1030_non_doc = "Express1030NonDoc"
    easypost_dhl_express_express1200_non_doc = "Express1200NonDoc"
    easypost_dhl_express_express1200 = "Express1200"
    easypost_dhl_express_express900 = "Express900"
    easypost_dhl_express_express900_non_doc = "Express900NonDoc"
    easypost_dhl_express_express_easy = "ExpressEasy"
    easypost_dhl_express_express_easy_non_doc = "ExpressEasyNonDoc"
    easypost_dhl_express_express_envelope = "ExpressEnvelope"
    easypost_dhl_express_express_worldwide = "ExpressWorldwide"
    easypost_dhl_express_express_worldwide_b2_c = "ExpressWorldwideB2C"
    easypost_dhl_express_express_worldwide_b2_c_non_doc = "ExpressWorldwideB2CNonDoc"
    easypost_dhl_express_express_worldwide_ecx = "ExpressWorldwideECX"
    easypost_dhl_express_express_worldwide_non_doc = "ExpressWorldwideNonDoc"
    easypost_dhl_express_freight_worldwide = "FreightWorldwide"
    easypost_dhl_express_globalmail_business = "GlobalmailBusiness"
    easypost_dhl_express_jet_line = "JetLine"
    easypost_dhl_express_jumbo_box = "JumboBox"
    easypost_dhl_express_logistics_services = "LogisticsServices"
    easypost_dhl_express_same_day = "SameDay"
    easypost_dhl_express_secure_line = "SecureLine"
    easypost_dhl_express_sprint_line = "SprintLine"
    easypost_dpd_classic = "DPDCLASSIC"
    easypost_dpd_8_30 = "DPD8:30"
    easypost_dpd_10_00 = "DPD10:00"
    easypost_dpd_12_00 = "DPD12:00"
    easypost_dpd_18_00 = "DPD18:00"
    easypost_dpd_express = "DPDEXPRESS"
    easypost_dpd_parcelletter = "DPDPARCELLETTER"
    easypost_dpd_parcelletterplus = "DPDPARCELLETTERPLUS"
    easypost_dpd_internationalmail = "DPDINTERNATIONALMAIL"
    easypost_dpd_uk_air_express_international_air = "AirExpressInternationalAir"
    easypost_dpd_uk_air_classic_international_air = "AirClassicInternationalAir"
    easypost_dpd_uk_parcel_sunday = "ParcelSunday"
    easypost_dpd_uk_freight_parcel_sunday = "FreightParcelSunday"
    easypost_dpd_uk_pallet_sunday = "PalletSunday"
    easypost_dpd_uk_pallet_dpd_classic = "PalletDpdClassic"
    easypost_dpd_uk_expresspak_dpd_classic = "ExpresspakDpdClassic"
    easypost_dpd_uk_expresspak_sunday = "ExpresspakSunday"
    easypost_dpd_uk_parcel_dpd_classic = "ParcelDpdClassic"
    easypost_dpd_uk_parcel_dpd_two_day = "ParcelDpdTwoDay"
    easypost_dpd_uk_parcel_dpd_next_day = "ParcelDpdNextDay"
    easypost_dpd_uk_parcel_dpd12 = "ParcelDpd12"
    easypost_dpd_uk_parcel_dpd10 = "ParcelDpd10"
    easypost_dpd_uk_parcel_return_to_shop = "ParcelReturnToShop"
    easypost_dpd_uk_parcel_saturday = "ParcelSaturday"
    easypost_dpd_uk_parcel_saturday12 = "ParcelSaturday12"
    easypost_dpd_uk_parcel_saturday10 = "ParcelSaturday10"
    easypost_dpd_uk_parcel_sunday12 = "ParcelSunday12"
    easypost_dpd_uk_freight_parcel_dpd_classic = "FreightParcelDpdClassic"
    easypost_dpd_uk_freight_parcel_sunday12 = "FreightParcelSunday12"
    easypost_dpd_uk_expresspak_dpd_next_day = "ExpresspakDpdNextDay"
    easypost_dpd_uk_expresspak_dpd12 = "ExpresspakDpd12"
    easypost_dpd_uk_expresspak_dpd10 = "ExpresspakDpd10"
    easypost_dpd_uk_expresspak_saturday = "ExpresspakSaturday"
    easypost_dpd_uk_expresspak_saturday12 = "ExpresspakSaturday12"
    easypost_dpd_uk_expresspak_saturday10 = "ExpresspakSaturday10"
    easypost_dpd_uk_expresspak_sunday12 = "ExpresspakSunday12"
    easypost_dpd_uk_pallet_sunday12 = "PalletSunday12"
    easypost_dpd_uk_pallet_dpd_two_day = "PalletDpdTwoDay"
    easypost_dpd_uk_pallet_dpd_next_day = "PalletDpdNextDay"
    easypost_dpd_uk_pallet_dpd12 = "PalletDpd12"
    easypost_dpd_uk_pallet_dpd10 = "PalletDpd10"
    easypost_dpd_uk_pallet_saturday = "PalletSaturday"
    easypost_dpd_uk_pallet_saturday12 = "PalletSaturday12"
    easypost_dpd_uk_pallet_saturday10 = "PalletSaturday10"
    easypost_dpd_uk_freight_parcel_dpd_two_day = "FreightParcelDpdTwoDay"
    easypost_dpd_uk_freight_parcel_dpd_next_day = "FreightParcelDpdNextDay"
    easypost_dpd_uk_freight_parcel_dpd12 = "FreightParcelDpd12"
    easypost_dpd_uk_freight_parcel_dpd10 = "FreightParcelDpd10"
    easypost_dpd_uk_freight_parcel_saturday = "FreightParcelSaturday"
    easypost_dpd_uk_freight_parcel_saturday12 = "FreightParcelSaturday12"
    easypost_dpd_uk_freight_parcel_saturday10 = "FreightParcelSaturday10"
    easypost_epost_courier_service_ddp = "CourierServiceDDP"
    easypost_epost_courier_service_ddu = "CourierServiceDDU"
    easypost_epost_domestic_economy_parcel = "DomesticEconomyParcel"
    easypost_epost_domestic_parcel_bpm = "DomesticParcelBPM"
    easypost_epost_domestic_priority_parcel = "DomesticPriorityParcel"
    easypost_epost_domestic_priority_parcel_bpm = "DomesticPriorityParcelBPM"
    easypost_epost_emi_service = "EMIService"
    easypost_epost_economy_parcel_service = "EconomyParcelService"
    easypost_epost_ipa_service = "IPAService"
    easypost_epost_isal_service = "ISALService"
    easypost_epost_pmi_service = "PMIService"
    easypost_epost_priority_parcel_ddp = "PriorityParcelDDP"
    easypost_epost_priority_parcel_ddu = "PriorityParcelDDU"
    easypost_epost_priority_parcel_delivery_confirmation_ddp = (
        "PriorityParcelDeliveryConfirmationDDP"
    )
    easypost_epost_priority_parcel_delivery_confirmation_ddu = (
        "PriorityParcelDeliveryConfirmationDDU"
    )
    easypost_epost_epacket_service = "ePacketService"
    easypost_estafeta_next_day_by930 = "NextDayBy930"
    easypost_estafeta_next_day_by1130 = "NextDayBy1130"
    easypost_estafeta_next_day = "NextDay"
    easypost_estafeta_ground = "Ground"
    easypost_estafeta_two_day = "TwoDay"
    easypost_estafeta_ltl = "LTL"
    easypost_fastway_parcel = "Parcel"
    easypost_fastway_satchel = "Satchel"
    easypost_fedex_ground = "FEDEX_GROUND"
    easypost_fedex_2_day = "FEDEX_2_DAY"
    easypost_fedex_2_day_am = "FEDEX_2_DAY_AM"
    easypost_fedex_express_saver = "FEDEX_EXPRESS_SAVER"
    easypost_fedex_standard_overnight = "STANDARD_OVERNIGHT"
    easypost_fedex_first_overnight = "FIRST_OVERNIGHT"
    easypost_fedex_priority_overnight = "PRIORITY_OVERNIGHT"
    easypost_fedex_international_economy = "INTERNATIONAL_ECONOMY"
    easypost_fedex_international_first = "INTERNATIONAL_FIRST"
    easypost_fedex_international_priority = "INTERNATIONAL_PRIORITY"
    easypost_fedex_ground_home_delivery = "GROUND_HOME_DELIVERY"
    easypost_fedex_crossborder_cbec = "CBEC"
    easypost_fedex_crossborder_cbecl = "CBECL"
    easypost_fedex_crossborder_cbecp = "CBECP"
    easypost_fedex_sameday_city_economy_service = "EconomyService"
    easypost_fedex_sameday_city_standard_service = "StandardService"
    easypost_fedex_sameday_city_priority_service = "PriorityService"
    easypost_fedex_sameday_city_last_mile = "LastMile"
    easypost_fedex_smart_post = "SMART_POST"
    easypost_globegistics_pmei = "PMEI"
    easypost_globegistics_pmi = "PMI"
    easypost_globegistics_ecom_domestic = "eComDomestic"
    easypost_globegistics_ecom_europe = "eComEurope"
    easypost_globegistics_ecom_express = "eComExpress"
    easypost_globegistics_ecom_extra = "eComExtra"
    easypost_globegistics_ecom_ipa = "eComIPA"
    easypost_globegistics_ecom_isal = "eComISAL"
    easypost_globegistics_ecom_pmei_duty_paid = "eComPMEIDutyPaid"
    easypost_globegistics_ecom_pmi_duty_paid = "eComPMIDutyPaid"
    easypost_globegistics_ecom_packet = "eComPacket"
    easypost_globegistics_ecom_packet_ddp = "eComPacketDDP"
    easypost_globegistics_ecom_priority = "eComPriority"
    easypost_globegistics_ecom_standard = "eComStandard"
    easypost_globegistics_ecom_tracked_ddp = "eComTrackedDDP"
    easypost_globegistics_ecom_tracked_ddu = "eComTrackedDDU"
    easypost_gso_early_priority_overnight = "EarlyPriorityOvernight"
    easypost_gso_priority_overnight = "PriorityOvernight"
    easypost_gso_california_parcel_service = "CaliforniaParcelService"
    easypost_gso_saturday_delivery_service = "SaturdayDeliveryService"
    easypost_gso_early_saturday_service = "EarlySaturdayService"
    easypost_gso_ground = "Ground"
    easypost_gso_overnight = "Overnight"
    easypost_hermes_domestic_delivery = "DomesticDelivery"
    easypost_hermes_domestic_delivery_signed = "DomesticDeliverySigned"
    easypost_hermes_international_delivery = "InternationalDelivery"
    easypost_hermes_international_delivery_signed = "InternationalDeliverySigned"
    easypost_interlink_air_classic_international_air = (
        "InterlinkAirClassicInternationalAir"
    )
    easypost_interlink_air_express_international_air = (
        "InterlinkAirExpressInternationalAir"
    )
    easypost_interlink_expresspak1_by10_30 = "InterlinkExpresspak1By10:30"
    easypost_interlink_expresspak1_by12 = "InterlinkExpresspak1By12"
    easypost_interlink_expresspak1_next_day = "InterlinkExpresspak1NextDay"
    easypost_interlink_expresspak1_saturday = "InterlinkExpresspak1Saturday"
    easypost_interlink_expresspak1_saturday_by10_30 = (
        "InterlinkExpresspak1SaturdayBy10:30"
    )
    easypost_interlink_expresspak1_saturday_by12 = "InterlinkExpresspak1SaturdayBy12"
    easypost_interlink_expresspak1_sunday = "InterlinkExpresspak1Sunday"
    easypost_interlink_expresspak1_sunday_by12 = "InterlinkExpresspak1SundayBy12"
    easypost_interlink_expresspak5_by10 = "InterlinkExpresspak5By10"
    easypost_interlink_expresspak5_by10_30 = "InterlinkExpresspak5By10:30"
    easypost_interlink_expresspak5_by12 = "InterlinkExpresspak5By12"
    easypost_interlink_expresspak5_next_day = "InterlinkExpresspak5NextDay"
    easypost_interlink_expresspak5_saturday = "InterlinkExpresspak5Saturday"
    easypost_interlink_expresspak5_saturday_by10 = "InterlinkExpresspak5SaturdayBy10"
    easypost_interlink_expresspak5_saturday_by10_30 = (
        "InterlinkExpresspak5SaturdayBy10:30"
    )
    easypost_interlink_expresspak5_saturday_by12 = "InterlinkExpresspak5SaturdayBy12"
    easypost_interlink_expresspak5_sunday = "InterlinkExpresspak5Sunday"
    easypost_interlink_expresspak5_sunday_by12 = "InterlinkExpresspak5SundayBy12"
    easypost_interlink_freight_by10 = "InterlinkFreightBy10"
    easypost_interlink_freight_by12 = "InterlinkFreightBy12"
    easypost_interlink_freight_next_day = "InterlinkFreightNextDay"
    easypost_interlink_freight_saturday = "InterlinkFreightSaturday"
    easypost_interlink_freight_saturday_by10 = "InterlinkFreightSaturdayBy10"
    easypost_interlink_freight_saturday_by12 = "InterlinkFreightSaturdayBy12"
    easypost_interlink_freight_sunday = "InterlinkFreightSunday"
    easypost_interlink_freight_sunday_by12 = "InterlinkFreightSundayBy12"
    easypost_interlink_parcel_by10 = "InterlinkParcelBy10"
    easypost_interlink_parcel_by10_30 = "InterlinkParcelBy10:30"
    easypost_interlink_parcel_by12 = "InterlinkParcelBy12"
    easypost_interlink_parcel_dpd_europe_by_road = "InterlinkParcelDpdEuropeByRoad"
    easypost_interlink_parcel_next_day = "InterlinkParcelNextDay"
    easypost_interlink_parcel_return = "InterlinkParcelReturn"
    easypost_interlink_parcel_return_to_shop = "InterlinkParcelReturnToShop"
    easypost_interlink_parcel_saturday = "InterlinkParcelSaturday"
    easypost_interlink_parcel_saturday_by10 = "InterlinkParcelSaturdayBy10"
    easypost_interlink_parcel_saturday_by10_30 = "InterlinkParcelSaturdayBy10:30"
    easypost_interlink_parcel_saturday_by12 = "InterlinkParcelSaturdayBy12"
    easypost_interlink_parcel_ship_to_shop = "InterlinkParcelShipToShop"
    easypost_interlink_parcel_sunday = "InterlinkParcelSunday"
    easypost_interlink_parcel_sunday_by12 = "InterlinkParcelSundayBy12"
    easypost_interlink_parcel_two_day = "InterlinkParcelTwoDay"
    easypost_interlink_pickup_parcel_dpd_europe_by_road = (
        "InterlinkPickupParcelDpdEuropeByRoad"
    )
    easypost_lasership_same_day = "SameDay"
    easypost_lasership_next_day = "NextDay"
    easypost_lasership_weekend = "Weekend"
    easypost_loomis_ground = "LoomisGround"
    easypost_loomis_express1800 = "LoomisExpress1800"
    easypost_loomis_express1200 = "LoomisExpress1200"
    easypost_loomis_express900 = "LoomisExpress900"
    easypost_lso_ground_early = "GroundEarly"
    easypost_lso_ground_basic = "GroundBasic"
    easypost_lso_priority_basic = "PriorityBasic"
    easypost_lso_priority_early = "PriorityEarly"
    easypost_lso_priority_saturday = "PrioritySaturday"
    easypost_lso_priority2nd_day = "Priority2ndDay"
    easypost_lso_same_day = "SameDay"
    easypost_newgistics_parcel_select = "ParcelSelect"
    easypost_newgistics_parcel_select_lightweight = "ParcelSelectLightweight"
    easypost_newgistics_ground = "Ground"
    easypost_newgistics_express = "Express"
    easypost_newgistics_first_class_mail = "FirstClassMail"
    easypost_newgistics_priority_mail = "PriorityMail"
    easypost_newgistics_bound_printed_matter = "BoundPrintedMatter"
    easypost_ontrac_sunrise = "Sunrise"
    easypost_ontrac_gold = "Gold"
    easypost_ontrac_on_trac_ground = "OnTracGround"
    easypost_ontrac_same_day = "SameDay"
    easypost_ontrac_palletized_freight = "PalletizedFreight"
    easypost_osm_first = "First"
    easypost_osm_expedited = "Expedited"
    easypost_osm_parcel_select_lightweight = "ParcelSelectLightweight"
    easypost_osm_priority = "Priority"
    easypost_osm_bpm = "BPM"
    easypost_osm_parcel_select = "ParcelSelect"
    easypost_osm_media_mail = "MediaMail"
    easypost_osm_marketing_parcel = "MarketingParcel"
    easypost_osm_marketing_parcel_tracked = "MarketingParcelTracked"
    easypost_parcll_economy_west = "Economy West"
    easypost_parcll_economy_east = "Economy East"
    easypost_parcll_economy_central = "Economy Central"
    easypost_parcll_economy_northeast = "Economy Northeast"
    easypost_parcll_economy_south = "Economy South"
    easypost_parcll_expedited_west = "Expedited West"
    easypost_parcll_expedited_northeast = "Expedited Northeast"
    easypost_parcll_regional_west = "Regional West"
    easypost_parcll_regional_east = "Regional East"
    easypost_parcll_regional_central = "Regional Central"
    easypost_parcll_regional_northeast = "Regional Northeast"
    easypost_parcll_regional_south = "Regional South"
    easypost_parcll_us_to_canada_economy_west = "US to Canada Economy West"
    easypost_parcll_us_to_canada_economy_central = "US to Canada Economy Central"
    easypost_parcll_us_to_canada_economy_northeast = "US to Canada Economy Northeast"
    easypost_parcll_us_to_europe_economy_west = "US to Europe Economy West"
    easypost_parcll_us_to_europe_economy_northeast = "US to Europe Economy Northeast"
    easypost_purolator_express = "PurolatorExpress"
    easypost_purolator_express12_pm = "PurolatorExpress12PM"
    easypost_purolator_express_pack12_pm = "PurolatorExpressPack12PM"
    easypost_purolator_express_box12_pm = "PurolatorExpressBox12PM"
    easypost_purolator_express_envelope12_pm = "PurolatorExpressEnvelope12PM"
    easypost_purolator_express1030_am = "PurolatorExpress1030AM"
    easypost_purolator_express9_am = "PurolatorExpress9AM"
    easypost_purolator_express_box = "PurolatorExpressBox"
    easypost_purolator_express_box1030_am = "PurolatorExpressBox1030AM"
    easypost_purolator_express_box9_am = "PurolatorExpressBox9AM"
    easypost_purolator_express_box_evening = "PurolatorExpressBoxEvening"
    easypost_purolator_express_box_international = "PurolatorExpressBoxInternational"
    easypost_purolator_express_box_international1030_am = (
        "PurolatorExpressBoxInternational1030AM"
    )
    easypost_purolator_express_box_international1200 = (
        "PurolatorExpressBoxInternational1200"
    )
    easypost_purolator_express_box_international9_am = (
        "PurolatorExpressBoxInternational9AM"
    )
    easypost_purolator_express_box_us = "PurolatorExpressBoxUS"
    easypost_purolator_express_box_us1030_am = "PurolatorExpressBoxUS1030AM"
    easypost_purolator_express_box_us1200 = "PurolatorExpressBoxUS1200"
    easypost_purolator_express_box_us9_am = "PurolatorExpressBoxUS9AM"
    easypost_purolator_express_envelope = "PurolatorExpressEnvelope"
    easypost_purolator_express_envelope1030_am = "PurolatorExpressEnvelope1030AM"
    easypost_purolator_express_envelope9_am = "PurolatorExpressEnvelope9AM"
    easypost_purolator_express_envelope_evening = "PurolatorExpressEnvelopeEvening"
    easypost_purolator_express_envelope_international = (
        "PurolatorExpressEnvelopeInternational"
    )
    easypost_purolator_express_envelope_international1030_am = (
        "PurolatorExpressEnvelopeInternational1030AM"
    )
    easypost_purolator_express_envelope_international1200 = (
        "PurolatorExpressEnvelopeInternational1200"
    )
    easypost_purolator_express_envelope_international9_am = (
        "PurolatorExpressEnvelopeInternational9AM"
    )
    easypost_purolator_express_envelope_us = "PurolatorExpressEnvelopeUS"
    easypost_purolator_express_envelope_us1030_am = "PurolatorExpressEnvelopeUS1030AM"
    easypost_purolator_express_envelope_us1200 = "PurolatorExpressEnvelopeUS1200"
    easypost_purolator_express_envelope_us9_am = "PurolatorExpressEnvelopeUS9AM"
    easypost_purolator_express_evening = "PurolatorExpressEvening"
    easypost_purolator_express_international = "PurolatorExpressInternational"
    easypost_purolator_express_international1030_am = (
        "PurolatorExpressInternational1030AM"
    )
    easypost_purolator_express_international1200 = "PurolatorExpressInternational1200"
    easypost_purolator_express_international9_am = "PurolatorExpressInternational9AM"
    easypost_purolator_express_pack = "PurolatorExpressPack"
    easypost_purolator_express_pack1030_am = "PurolatorExpressPack1030AM"
    easypost_purolator_express_pack9_am = "PurolatorExpressPack9AM"
    easypost_purolator_express_pack_evening = "PurolatorExpressPackEvening"
    easypost_purolator_express_pack_international = "PurolatorExpressPackInternational"
    easypost_purolator_express_pack_international1030_am = (
        "PurolatorExpressPackInternational1030AM"
    )
    easypost_purolator_express_pack_international1200 = (
        "PurolatorExpressPackInternational1200"
    )
    easypost_purolator_express_pack_international9_am = (
        "PurolatorExpressPackInternational9AM"
    )
    easypost_purolator_express_pack_us = "PurolatorExpressPackUS"
    easypost_purolator_express_pack_us1030_am = "PurolatorExpressPackUS1030AM"
    easypost_purolator_express_pack_us1200 = "PurolatorExpressPackUS1200"
    easypost_purolator_express_pack_us9_am = "PurolatorExpressPackUS9AM"
    easypost_purolator_express_us = "PurolatorExpressUS"
    easypost_purolator_express_us1030_am = "PurolatorExpressUS1030AM"
    easypost_purolator_express_us1200 = "PurolatorExpressUS1200"
    easypost_purolator_express_us9_am = "PurolatorExpressUS9AM"
    easypost_purolator_ground = "PurolatorGround"
    easypost_purolator_ground1030_am = "PurolatorGround1030AM"
    easypost_purolator_ground9_am = "PurolatorGround9AM"
    easypost_purolator_ground_distribution = "PurolatorGroundDistribution"
    easypost_purolator_ground_evening = "PurolatorGroundEvening"
    easypost_purolator_ground_regional = "PurolatorGroundRegional"
    easypost_purolator_ground_us = "PurolatorGroundUS"
    easypost_royalmail_international_signed = "InternationalSigned"
    easypost_royalmail_international_standard = "InternationalStandard"
    easypost_royalmail_international_tracked = "InternationalTracked"
    easypost_royalmail_international_tracked_and_signed = (
        "InternationalTrackedAndSigned"
    )
    easypost_royalmail_1st_class = "1stClass"
    easypost_royalmail_1st_class_signed_for = "1stClassSignedFor"
    easypost_royalmail_2nd_class = "2ndClass"
    easypost_royalmail_2nd_class_signed_for = "2ndClassSignedFor"
    easypost_royalmail_royal_mail24 = "RoyalMail24"
    easypost_royalmail_royal_mail24_signed_for = "RoyalMail24SignedFor"
    easypost_royalmail_royal_mail48 = "RoyalMail48"
    easypost_royalmail_royal_mail48_signed_for = "RoyalMail48SignedFor"
    easypost_royalmail_special_delivery_guaranteed1pm = "SpecialDeliveryGuaranteed1pm"
    easypost_royalmail_special_delivery_guaranteed9am = "SpecialDeliveryGuaranteed9am"
    easypost_royalmail_standard_letter1st_class = "StandardLetter1stClass"
    easypost_royalmail_standard_letter1st_class_signed_for = (
        "StandardLetter1stClassSignedFor"
    )
    easypost_royalmail_standard_letter2nd_class = "StandardLetter2ndClass"
    easypost_royalmail_standard_letter2nd_class_signed_for = (
        "StandardLetter2ndClassSignedFor"
    )
    easypost_royalmail_tracked24 = "Tracked24"
    easypost_royalmail_tracked24_high_volume = "Tracked24HighVolume"
    easypost_royalmail_tracked24_high_volume_signature = "Tracked24HighVolumeSignature"
    easypost_royalmail_tracked24_signature = "Tracked24Signature"
    easypost_royalmail_tracked48 = "Tracked48"
    easypost_royalmail_tracked48_high_volume = "Tracked48HighVolume"
    easypost_royalmail_tracked48_high_volume_signature = "Tracked48HighVolumeSignature"
    easypost_royalmail_tracked48_signature = "Tracked48Signature"
    easypost_seko_ecommerce_standard_tracked = "eCommerce Standard Tracked"
    easypost_seko_ecommerce_express_tracked = "eCommerce Express Tracked"
    easypost_seko_domestic_express = "Domestic Express"
    easypost_seko_domestic_standard = "Domestic Standard"
    easypost_sendle_easy = "Easy"
    easypost_sendle_pro = "Pro"
    easypost_sendle_plus = "Plus"
    easypost_sfexpress_international_standard_express_doc = (
        "International Standard Express - Doc"
    )
    easypost_sfexpress_international_standard_express_parcel = (
        "International Standard Express - Parcel"
    )
    easypost_sfexpress_international_economy_express_pilot = (
        "International Economy Express - Pilot"
    )
    easypost_sfexpress_international_economy_express_doc = (
        "International Economy Express - Doc"
    )
    easypost_speedee_delivery = "SpeeDeeDelivery"
    easypost_startrack_express = "StartrackExpress"
    easypost_startrack_premium = "StartrackPremium"
    easypost_startrack_fixed_price_premium = "StartrackFixedPricePremium"
    easypost_tforce_same_day = "SameDay"
    easypost_tforce_same_day_white_glove = "SameDayWhiteGlove"
    easypost_tforce_next_day = "NextDay"
    easypost_tforce_next_day_white_glove = "NextDayWhiteGlove"
    easypost_uds_delivery_service = "DeliveryService"
    easypost_ups_ground = "Ground"
    easypost_ups_standard = "UPSStandard"
    easypost_ups_saver = "UPSSaver"
    easypost_ups_express = "Express"
    easypost_ups_express_plus = "ExpressPlus"
    easypost_ups_expedited = "Expedited"
    easypost_ups_next_day_air = "NextDayAir"
    easypost_ups_next_day_air_saver = "NextDayAirSaver"
    easypost_ups_next_day_air_early_am = "NextDayAirEarlyAM"
    easypost_ups_2nd_day_air = "2ndDayAir"
    easypost_ups_2nd_day_air_am = "2ndDayAirAM"
    easypost_ups_3_day_select = "3DaySelect"
    easypost_ups_mail_first = "First"
    easypost_ups_mail_priority = "Priority"
    easypost_ups_mail_expedited_mail_innovations = "ExpeditedMailInnovations"
    easypost_ups_mail_priority_mail_innovations = "PriorityMailInnovations"
    easypost_ups_mail_economy_mail_innovations = "EconomyMailInnovations"
    easypost_usps_first = "First"
    easypost_usps_priority = "Priority"
    easypost_usps_express = "Express"
    easypost_usps_parcel_select = "ParcelSelect"
    easypost_usps_library_mail = "LibraryMail"
    easypost_usps_media_mail = "MediaMail"
    easypost_usps_first_class_mail_international = "FirstClassMailInternational"
    easypost_usps_first_class_package_international_service = (
        "FirstClassPackageInternationalService"
    )
    easypost_usps_priority_mail_international = "PriorityMailInternational"
    easypost_usps_express_mail_international = "ExpressMailInternational"
    easypost_veho_next_day = "nextDay"
    easypost_veho_same_day = "sameDay"

    @staticmethod
    def info(serviceName, carrier):
        rate_provider = CarrierId.map(carrier).name_or_key
        service = Service.map(serviceName)
        service_name = re.sub(
            r"((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))", r" \1", service.name_or_key
        ).replace("easypost_", "")

        return rate_provider, service.name_or_key, service_name


class CarrierId(lib.StrEnum):
    amazon_shipping = "AmazonMws"
    apc = "APC"
    asendia = "Asendia"
    asendia_us = "Asendia USA"
    australiapost = "Australia Post"
    axlehire = "AxleHire"
    better_trucks = "Better Trucks"
    bond = "Bond"
    canadapost = "Canada Post"
    canpar = "Canpar"
    cdl = "CDL Last Mile Solutions"
    chronopost = "Chronopost"
    cloudsort = "CloudSort"
    courier_express = "Courier Express"
    courierplease = "CourierPlease"
    daipost = "Dai Post"
    deutschepost = "Deutsche Post"
    deutschepost_uk = "Deutsche Post UK"
    dhl_ecom_asia = "DHL eCommerce Asia"
    dhl_ecom = "DHL eCommerce Solutions"
    dhl_express = "DHL Express"
    dpd = "DPD"
    dpd_uk = "DPD UK"
    epost = "ePost Global"
    estafeta = "Estafeta"
    fastway = "Fastway"
    fedex = "FedEx"
    fedex_mail = "FedEx Mailview"
    fedex_sameday_city = "FedEx Same Day City"
    fedex_smartpost = "FedEx SmartPost"
    firstmile = "FirstMile"
    globegistics = "Globegistics"
    gso = "GSO"
    hermes = "Hermes"
    interlink = "Interlink Express"
    jppost = "JP Post"
    kuroneko_yamato = "Kuroneko Yamato"
    laposte = "La Poste"
    lasership = "LaserShip"
    loomis = "Loomis Express"
    lso = "LSO"
    newgistics = "Newgistics"
    ontrac = "OnTrac"
    osm = "OSM Worldwide"
    parcelforce = "Parcelforce"
    parcll = "PARCLL"
    passport = "Passport"
    postnl = "PostNL"
    purolator = "Purolator"
    royalmail = "Royal Mail"
    seko = "SEKO OmniParcel"
    sendle = "Sendle"
    sfexpress = "SF Express"
    speedee = "Spee-Dee"
    startrack = "StarTrack"
    tforce = "TForce"
    uds = "UDS"
    ups = "UPS"
    ups_iparcel = "UPS i-parcel"
    ups_mail_innovations = "UPS Mail Innovations"
    usps = "USPS"
    veho = "Veho"
    yanwen = "Yanwen"

    @staticmethod
    def to_dict():
        return {key: enum.value for key, enum in CarrierId.__members__.items()}


class ShippingOption(lib.Enum):
    easypost_additional_handling = lib.OptionEnum("additional_handling", bool)
    easypost_address_validation_level = lib.OptionEnum("address_validation_level")
    easypost_alcohol = lib.OptionEnum("alcohol", bool)
    easypost_by_drone = lib.OptionEnum("by_drone", bool)
    easypost_carbon_neutral = lib.OptionEnum("carbon_neutral", bool)
    easypost_cod_amount = lib.OptionEnum("cod_amount")
    easypost_cod_method = lib.OptionEnum("cod_method")
    easypost_cod_address_id = lib.OptionEnum("cod_address_id")
    easypost_currency = lib.OptionEnum("currency")
    easypost_delivery_confirmation = lib.OptionEnum("delivery_confirmation")
    easypost_dropoff_type = lib.OptionEnum("dropoff_type")
    easypost_dry_ice = lib.OptionEnum("dry_ice", bool)
    easypost_dry_ice_medical = lib.OptionEnum("dry_ice_medical", bool)
    easypost_dry_ice_weight = lib.OptionEnum("dry_ice_weight")
    easypost_endorsement = lib.OptionEnum("endorsement")
    easypost_freight_charge = lib.OptionEnum("freight_charge", float)
    easypost_handling_instructions = lib.OptionEnum("handling_instructions")
    easypost_hazmat = lib.OptionEnum("hazmat")
    easypost_hold_for_pickup = lib.OptionEnum("hold_for_pickup", bool)
    easypost_incoterm = lib.OptionEnum("incoterm")
    easypost_invoice_number = lib.OptionEnum("invoice_number")
    easypost_label_date = lib.OptionEnum("label_date")
    easypost_label_format = lib.OptionEnum("label_format")
    easypost_machinable = lib.OptionEnum("machinable", bool)
    easypost_payment = lib.OptionEnum("payment", dict)
    easypost_print_custom_1 = lib.OptionEnum("print_custom_1")
    easypost_print_custom_2 = lib.OptionEnum("print_custom_2")
    easypost_print_custom_3 = lib.OptionEnum("print_custom_3")
    easypost_print_custom_1_barcode = lib.OptionEnum("print_custom_1_barcode")
    easypost_print_custom_2_barcode = lib.OptionEnum("print_custom_2_barcode")
    easypost_print_custom_3_barcode = lib.OptionEnum("print_custom_3_barcode")
    easypost_print_custom_1_code = lib.OptionEnum("print_custom_1_code")
    easypost_print_custom_2_code = lib.OptionEnum("print_custom_2_code")
    easypost_print_custom_3_code = lib.OptionEnum("print_custom_3_code")
    easypost_saturday_delivery = lib.OptionEnum("saturday_delivery", bool)
    easypost_special_rates_eligibility = lib.OptionEnum("special_rates_eligibility")
    easypost_smartpost_hub = lib.OptionEnum("smartpost_hub")
    easypost_smartpost_manifest = lib.OptionEnum("smartpost_manifest")
    easypost_billing_ref = lib.OptionEnum("billing_ref")
    easypost_certified_mail = lib.OptionEnum("certified_mail", bool)
    easypost_registered_mail = lib.OptionEnum("registered_mail", bool)
    easypost_registered_mail_amount = lib.OptionEnum("registered_mail_amount", float)
    easypost_return_receipt = lib.OptionEnum("return_receipt", bool)

    """ Unified Option type mapping """
    currency = easypost_currency
    shipment_date = easypost_label_date
    cash_on_delivery = easypost_cod_amount
    saturday_delivery = easypost_saturday_delivery
    signature_confirmation = easypost_delivery_confirmation


def shipping_options_initializer(
    payload: typing.Any,
    payor: models.Address = None,
    package_options: units.Options = None,
) -> dict:
    """
    Apply default values to the given options.
    """
    options: dict = {}

    if hasattr(payload, "label_type"):
        options.update(
            easypost_label_format=LabelType.map(payload.label_type or "PDF").value,
        )

    if hasattr(payload, "customs"):
        options.update(
            easypost_invoice_number=getattr(payload.customs, "invoice", None),
        )

    if hasattr(payload, "payment"):
        options.update(
            easypost_payment=dict(
                type=units.PaymentType.map(
                    getattr(payload.payment, "paid_by", "sender")
                ).value,
                account=getattr(payload.payment, "account_number", None),
                country=getattr(payor, "country_code", None),
                postal_code=getattr(payor, "postal_code", None),
            ),
        )

    options.update(payload.options)

    if package_options is not None:
        options.update(package_options.content)

    # Define carrier option filter.
    def items_filter(key: str) -> bool:
        return key in ShippingOption  # type:ignore

    return units.ShippingOptions(options, ShippingOption, items_filter=items_filter)
