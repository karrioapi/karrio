import csv
import pathlib
import karrio.lib as lib
import karrio.core.models as models

PRESET_DEFAULTS = dict(
    dimension_unit="CM",
    weight_unit="KG",
)

MeasurementOptions = lib.units.MeasurementOptionsType(
    quant=0.1,
    min_kg=0.01,
    min_in=0.01,
)


class PackagePresets(lib.Enum):
    """
    Note that dimensions are in CM and weight in KG
    """

    canadapost_mailing_box = lib.units.PackagePreset(
        **dict(width=10.2, height=15.2, length=1.0), **PRESET_DEFAULTS
    )
    canadapost_extra_small_mailing_box = lib.units.PackagePreset(
        **dict(width=14.0, height=14.0, length=14.0), **PRESET_DEFAULTS
    )
    canadapost_small_mailing_box = lib.units.PackagePreset(
        **dict(width=28.6, height=22.9, length=6.4), **PRESET_DEFAULTS
    )
    canadapost_medium_mailing_box = lib.units.PackagePreset(
        **dict(width=31.0, height=23.5, length=13.3), **PRESET_DEFAULTS
    )
    canadapost_large_mailing_box = lib.units.PackagePreset(
        **dict(width=38.1, height=30.5, length=9.5), **PRESET_DEFAULTS
    )
    canadapost_extra_large_mailing_box = lib.units.PackagePreset(
        **dict(width=40.0, height=30.5, length=21.6), **PRESET_DEFAULTS
    )
    canadapost_corrugated_small_box = lib.units.PackagePreset(
        **dict(width=42.0, height=32.0, length=32.0), **PRESET_DEFAULTS
    )
    canadapost_corrugated_medium_box = lib.units.PackagePreset(
        **dict(width=46.0, height=38.0, length=32.0), **PRESET_DEFAULTS
    )
    canadapost_corrugated_large_box = lib.units.PackagePreset(
        **dict(width=46.0, height=46.0, length=40.6), **PRESET_DEFAULTS
    )
    canadapost_xexpresspost_certified_envelope = lib.units.PackagePreset(
        **dict(width=26.0, height=15.9, weight=0.5, length=1.5), **PRESET_DEFAULTS
    )
    canadapost_xexpresspost_national_large_envelope = lib.units.PackagePreset(
        **dict(width=40.0, height=29.2, weight=1.36, length=1.5), **PRESET_DEFAULTS
    )
    canadapost_xexpresspost_regional_small_envelope = lib.units.PackagePreset(
        **dict(width=26.0, height=15.9, weight=0.5, length=1.5), **PRESET_DEFAULTS
    )
    canadapost_xexpresspost_regional_large_envelope = lib.units.PackagePreset(
        **dict(width=40.0, height=29.2, weight=1.36, length=1.5), **PRESET_DEFAULTS
    )


class LabelType(lib.Enum):
    PDF_4x6 = ("PDF", "4x6")
    PDF_8_5x11 = ("PDF", "8.5x11")
    ZPL_4x6 = ("ZPL", "4x6")

    """ Unified Label type mapping """
    PDF = PDF_4x6
    ZPL = ZPL_4x6


class PaymentType(lib.StrEnum):
    account = "Account"
    card = "CreditCard"
    supplier_account = "SupplierAccount"

    sender = account
    recipient = account
    third_party = supplier_account
    credit_card = card


class ConnectionConfig(lib.Enum):
    cost_center = lib.OptionEnum("cost_center")
    label_type = lib.OptionEnum("label_type", LabelType)
    shipping_options = lib.OptionEnum("shipping_options", list)
    shipping_services = lib.OptionEnum("shipping_services", list)
    transmit_shipment_by_default = lib.OptionEnum("transmit_shipment_by_default", bool)


class ServiceType(lib.Enum):
    canadapost_regular_parcel = "DOM.RP"
    canadapost_expedited_parcel = "DOM.EP"
    canadapost_xpresspost = "DOM.XP"
    canadapost_xpresspost_certified = "DOM.XP.CERT"
    canadapost_priority = "DOM.PC"
    canadapost_library_books = "DOM.LIB"
    canadapost_expedited_parcel_usa = "USA.EP"
    canadapost_priority_worldwide_envelope_usa = "USA.PW.ENV"
    canadapost_priority_worldwide_pak_usa = "USA.PW.PAK"
    canadapost_priority_worldwide_parcel_usa = "USA.PW.PARCEL"
    canadapost_small_packet_usa_air = "USA.SP.AIR"
    canadapost_tracked_packet_usa = "USA.TP"
    canadapost_tracked_packet_usa_lvm = "USA.TP.LVM"
    canadapost_xpresspost_usa = "USA.XP"
    canadapost_xpresspost_international = "INT.XP"
    canadapost_international_parcel_air = "INT.IP.AIR"
    canadapost_international_parcel_surface = "INT.IP.SURF"
    canadapost_priority_worldwide_envelope_intl = "INT.PW.ENV"
    canadapost_priority_worldwide_pak_intl = "INT.PW.PAK"
    canadapost_priority_worldwide_parcel_intl = "INT.PW.PARCEL"
    canadapost_small_packet_international_air = "INT.SP.AIR"
    canadapost_small_packet_international_surface = "INT.SP.SURF"
    canadapost_tracked_packet_international = "INT.TP"


class ShippingOption(lib.Enum):
    canadapost_signature = lib.OptionEnum("SO", bool, meta=dict(category="SIGNATURE"))
    canadapost_coverage = lib.OptionEnum("COV", float, meta=dict(category="INSURANCE"))
    canadapost_collect_on_delivery = lib.OptionEnum("COD", float, meta=dict(category="COD"))
    canadapost_proof_of_age_required_18 = lib.OptionEnum("PA18", bool, meta=dict(category="SIGNATURE"))
    canadapost_proof_of_age_required_19 = lib.OptionEnum("PA19", bool, meta=dict(category="SIGNATURE"))
    canadapost_card_for_pickup = lib.OptionEnum("HFP", bool, meta=dict(category="PUDO"))
    canadapost_do_not_safe_drop = lib.OptionEnum("DNS", bool, meta=dict(category="DELIVERY_OPTIONS"))
    canadapost_leave_at_door = lib.OptionEnum("LAD", bool, meta=dict(category="DELIVERY_OPTIONS"))
    canadapost_deliver_to_post_office = lib.OptionEnum("D2PO", bool, meta=dict(category="PUDO"))
    canadapost_return_at_senders_expense = lib.OptionEnum("RASE", bool, meta=dict(category="RETURN"))
    canadapost_return_to_sender = lib.OptionEnum("RTS", bool, meta=dict(category="RETURN"))
    canadapost_abandon = lib.OptionEnum("ABAN", bool)

    """ Custom Option """
    canadapost_cost_center = lib.OptionEnum("cost-centre")
    canadapost_submit_shipment = lib.OptionEnum("transmit-shipment", bool)

    """ Unified Option type mapping """
    insurance = canadapost_coverage
    cash_on_delivery = canadapost_collect_on_delivery
    signature_confirmation = canadapost_signature


def shipping_options_initializer(
    options: dict,
    package_options: lib.units.ShippingOptions = None,
    is_international: bool = False,
) -> lib.units.ShippingOptions:
    _options = options.copy()

    # Apply default non delivery options for if international.
    no_international_option_specified: bool = not any(
        key in _options for key in INTERNATIONAL_NON_DELIVERY_OPTION
    )

    if is_international and no_international_option_specified:
        _options.update(
            {ShippingOption.canadapost_return_at_senders_expense.name: True}
        )

    # Apply package options if specified.
    if package_options is not None:
        _options.update(package_options.content)

    # Define carrier option filter.
    def items_filter(key: str) -> bool:
        return key in ShippingOption and key not in CUSTOM_OPTIONS  # type:ignore

    return lib.units.ShippingOptions(
        _options, ShippingOption, items_filter=items_filter
    )


# Canonical Canada Post event mapping used for tracker status normalization.
# Sources:
# - Official Canada Post message/event code table:
#   https://www.canadapost-postescanada.ca/info/mc/business/productsservices/developers/messagescodetables.jsf
# - Live event payloads observed in production integrations (including padded IDs like `0100`).
#
# Mapping shape:
# - `__default__`: status when code is known and no description-specific override matches.
# - `__description_en__` / `__description_fr__`: reference labels from Canada Post docs/payloads.
# - optional description keys: explicit override for ambiguous codes.
TRACKING_STATUS_MAPPING = {
    "100": {
        "__default__": "picked_up",
        "__description_en__": "Item processed",
        "__description_fr__": "Article traité"
    },
    "102": {
        "__default__": "in_transit",
        "__description_en__": "Item processed",
        "__description_fr__": "Article traité"
    },
    "104": {
        "__default__": "picked_up",
        "__description_en__": "Item processed",
        "__description_fr__": "Article traité"
    },
    "105": {
        "__default__": "picked_up",
        "__description_en__": "Item processed",
        "__description_fr__": "Article traité"
    },
    "106": {
        "__default__": "in_transit",
        "__description_en__": "Item processed",
        "__description_fr__": "Article traité"
    },
    "107": {
        "__default__": "picked_up",
        "__description_en__": "Item processed",
        "__description_fr__": "Article traité"
    },
    "1100": {
        "__default__": "on_hold",
        "__description_en__": "Refused by Customs. Unacceptable sender info. Item being returned to sender",
        "__description_fr__": "Refusé par les Douanes. Info de l'exp. inacceptable. Article retourné à l'exp."
    },
    "113": {
        "__default__": "in_transit",
        "__description_en__": "Item arrived at partner facility",
        "__description_fr__": "L'article est arrivé à l'installation du partenaire"
    },
    "114": {
        "__default__": "in_transit",
        "__description_en__": "Item departed partner facility",
        "__description_fr__": "L'article a quitté l'installation du partenaire"
    },
    "115": {
        "__default__": "in_transit",
        "__description_en__": "Item transferred to partner",
        "__description_fr__": "Article transféré au partenaire"
    },
    "116": {
        "__default__": "in_transit",
        "__description_en__": "Item transferred to partner",
        "__description_fr__": "Article transféré au partenaire"
    },
    "117": {
        "__default__": "in_transit",
        "__description_en__": "Item on Hold.Documentation irregularity.",
        "__description_fr__": "Article retenu. Irrégularité avec le documentation"
    },
    "118": {
        "__default__": "in_transit",
        "__description_en__": "Item held. Recipient outside partner service area",
        "__description_fr__": "Article retenu. Le destinataire ne fait pas partie de la z"
    },
    "120": {
        "__default__": "in_transit",
        "__description_en__": "Item on hold. Incorrect or incomplete address",
        "__description_fr__": "Article retenu. Adresse incorrecte ou incomplète"
    },
    "1200": {
        "__default__": "on_hold",
        "__description_en__": "Expected delivery date updated",
        "__description_fr__": "Nouvelle date de livraison prévue"
    },
    "1203": {
        "__default__": "in_transit",
        "__description_en__": "Expected delivery date updated",
        "__description_fr__": "Date de livraison prévue mise à jour"
    },
    "121": {
        "__default__": "in_transit",
        "__description_en__": "Item on hold. Refused or unclaimed by recipient",
        "__description_fr__": "Article retenu. Refusé ou non réclamé par le destinataire"
    },
    "1210": {
        "__default__": "in_transit",
        "__description_en__": "Duty and taxes paid online",
        "__description_fr__": "Duty and taxes paid online"
    },
    "1214": {
        "__default__": "in_transit",
        "__description_en__": "Refund requested for duty and taxes",
        "__description_fr__": "Refund requested for duty and taxes"
    },
    "1215": {
        "__default__": "in_transit",
        "__description_en__": "Refund issued for duty and taxes",
        "__description_fr__": "Refund issued for duty and taxes"
    },
    "1216": {
        "__default__": "in_transit",
        "__description_en__": "Refund issued for duplicate payment of duty and taxes",
        "__description_fr__": "Refund issued for duplicate payment of duty and taxes"
    },
    "1220": {
        "__default__": "in_transit",
        "__description_en__": "Delivery preference - Front door",
        "__description_fr__": "Préférence de livraison - Porte d'entrée"
    },
    "1221": {
        "__default__": "in_transit",
        "__description_en__": "Delivery preference - Side door",
        "__description_fr__": "Préférence de livraison - Porte de côté"
    },
    "1223": {
        "__default__": "in_transit",
        "__description_en__": "Delivery preference - Garage",
        "__description_fr__": "Préférence de livraison - Garage"
    },
    "1224": {
        "__default__": "in_transit",
        "__description_en__": "Delivery preference - Front desk or superintendent",
        "__description_fr__": "Préférence de livraison - Réception ou surveillant"
    },
    "1225": {
        "__default__": "in_transit",
        "__description_en__": "Delivery preference - Deliver to post office",
        "__description_fr__": "Préférence de livraison - Livrer au bureau de poste"
    },
    "1230": {
        "__default__": "in_transit",
        "__description_en__": "Redirection requested by shipper",
        "__description_fr__": "Réexpédition demandée par l'expéditeur"
    },
    "1232": {
        "__default__": "in_transit",
        "__description_en__": "Redirection requested",
        "__description_fr__": "Redirection requested"
    },
    "1234": {
        "__default__": "in_transit",
        "__description_en__": "Redirection request cancelled by shipper",
        "__description_fr__": "Redirection request cancelled by shipper"
    },
    "1240": {
        "__default__": "picked_up",
        "__description_en__": "Item processed",
        "__description_fr__": "Article traité"
    },
    "1241": {
        "__default__": "in_transit",
        "__description_en__": "Item processed",
        "__description_fr__": "L'article a été redirigé"
    },
    "1244": {
        "__default__": "picked_up",
        "__description_en__": "Item processed",
        "__description_fr__": "Article traité"
    },
    "1245": {
        "__default__": "on_hold",
        "__description_en__": "Item could not be redirected",
        "__description_fr__": "L'article n'a pas pu être redirigé"
    },
    "127": {
        "__default__": "in_transit",
        "__description_en__": "Item held at customs",
        "__description_fr__": "Article retenu aux Douanes"
    },
    "130": {
        "__default__": "in_transit",
        "__description_en__": "International item released from Customs",
        "__description_fr__": "Article du régime international traité à la douane"
    },
    "1300": {
        "__default__": "pending",
        "__description_en__": "Item accepted",
        "__description_fr__": "Article accepté"
    },
    "1301": {
        "__default__": "pending",
        "__description_en__": "Item accepted at the Post Office.",
        "__description_fr__": "Article accepté au bureau de poste"
    },
    "1302": {
        "__default__": "pending",
        "__description_en__": "Item accepted at the Post Office.",
        "__description_fr__": "Article accepté au bureau de poste"
    },
    "1303": {
        "__default__": "pending",
        "__description_en__": "Return item accepted at Post Office",
        "__description_fr__": "Envoi retour accepté au bureau de poste"
    },
    "1405": {
        "__default__": "delivered",
        "__description_en__": "Delivered to automated parcel locker",
        "__description_fr__": "Delivered to automated parcel locker"
    },
    "1406": {
        "__default__": "delivered",
        "__description_en__": "Item picked up from automated parcel locker",
        "__description_fr__": "Item picked up from automated parcel locker"
    },
    "1407": {
        "__default__": "ready_for_pickup",
        "__description_en__": "Item available for pick-up",
        "__description_fr__": "Envoi disponible pour le ramassage"
    },
    "1408": {
        "__default__": "delivered",
        "__description_en__": "Delivered; Contact customer service for copy of signature",
        "__description_fr__": "Livré; appeler le service à la clientèle pour copie de la signature"
    },
    "1409": {
        "__default__": "delivered",
        "__description_en__": "Delivered; Contact customer service for copy of signature",
        "__description_fr__": "Livré; appeler le service à la clientèle pour copie de la signature"
    },
    "1410": {
        "__default__": "delivery_delayed",
        "__description_en__": "Item on hold at recipient's request",
        "__description_fr__": "Article retenu à la demande du destinataire"
    },
    "1411": {
        "__default__": "on_hold",
        "__description_en__": "Business closed for the day. Item on hold for second delivery attempt.",
        "__description_fr__": "Fermé pour la journée. Article retenu pour deuxième tentative de livraison."
    },
    "1412": {
        "L'article renvoyé à l'expéditeur est arrivé à l'installation postale.": "return_to_sender",
        "__default__": "on_hold",
        "__description_en__": "Verifying recipient's address; Possible delay",
        "__description_fr__": "Vérification de l'adresse du destinataire; délai possible"
    },
    "1414": {
        "__default__": "delivery_delayed",
        "__description_en__": "Item rescheduled for delivery next business day.",
        "__description_fr__": "La livraison de l'article est reportée au jour ouvrable suivant."
    },
    "1415": {
        "__default__": "return_to_sender",
        "__description_en__": "Item being returned to Sender. Incomplete address.",
        "__description_fr__": "Article retourné à l'expéditeur. Adresse incomplète."
    },
    "1416": {
        "__default__": "return_to_sender",
        "__description_en__": "Recipient not located at address provided. Item being returned to sender.",
        "__description_fr__": "Destinataire ne demeure pas à l'adresse indiquée. Article renvoyé à l'expéditeur"
    },
    "1417": {
        "__default__": "return_to_sender",
        "__description_en__": "Item refused by recipient. Item being returned to sender.",
        "__description_fr__": "Article refusé par le destinataire. Article retourné à l'expéditeur."
    },
    "1418": {
        "__default__": "return_to_sender",
        "__description_en__": "Item being returned to Sender. Valid proof of age identification not provided.",
        "__description_fr__": "Article retourné à l'expéditeur. Preuve d'âge valide non fournie."
    },
    "1419": {
        "__default__": "return_to_sender",
        "__description_en__": "Item was unclaimed by recipient. Item being returned to sender.",
        "__description_fr__": "Article non réclamé par le destinataire. Article retourné à l'expéditeur."
    },
    "1420": {
        "__default__": "return_to_sender",
        "__description_en__": "Item being returned to sender",
        "__description_fr__": "Article retourné à l'expéditeur"
    },
    "1421": {
        "__default__": "delivered",
        "__description_en__": "Delivered to recipient's front door",
        "__description_fr__": "Livré à la porte avant du destinataire"
    },
    "1422": {
        "__default__": "delivered",
        "__description_en__": "Delivered to recipient's side door",
        "__description_fr__": "Livré à la porte de côté du destinataire"
    },
    "1423": {
        "__default__": "delivered",
        "__description_en__": "Delivered to recipient's back door",
        "__description_fr__": "Livré à la porte arrière du destinataire"
    },
    "1424": {
        "__default__": "delivered",
        "__description_en__": "Delivered at or in recipient's garage",
        "__description_fr__": "Livré au garage du destinataire"
    },
    "1425": {
        "__default__": "delivered",
        "__description_en__": "Delivered to superintendent, security or concierge",
        "__description_fr__": "Livré au concierge/à l’agent de sécurité de l’immeuble"
    },
    "1426": {
        "__default__": "delivered",
        "__description_en__": "Delivered to recipient's parcel box",
        "__description_fr__": "Livré dans la boîte à colis du destinataire"
    },
    "1427": {
        "__default__": "delivered",
        "__description_en__": "Delivered to recipient's safe drop location",
        "__description_fr__": "Livré au lieu sûr du destinataire"
    },
    "1428": {
        "__default__": "delivered",
        "__description_en__": "Delivered to recipient's front door",
        "__description_fr__": "Livré à la porte avant du destinataire"
    },
    "1429": {
        "__default__": "delivered",
        "__description_en__": "Delivered to recipient's side door",
        "__description_fr__": "Livré à la porte de côté du destinataire"
    },
    "1430": {
        "__default__": "delivered",
        "__description_en__": "Delivered to recipient's back door",
        "__description_fr__": "Livré à la porte arrière du destinataire"
    },
    "1431": {
        "__default__": "delivered",
        "__description_en__": "Delivered at or in recipient's garage",
        "__description_fr__": "Livré au garage du destinataire"
    },
    "1432": {
        "__default__": "delivered",
        "__description_en__": "Delivered to building superintendent or security agent",
        "__description_fr__": "Livré au concierge/à l’agent de sécurité de l’immeuble"
    },
    "1433": {
        "__default__": "delivered",
        "__description_en__": "Delivered to recipient's parcel box",
        "__description_fr__": "Livré dans la boîte à colis du destinataire"
    },
    "1434": {
        "__default__": "delivered",
        "__description_en__": "Delivered to recipient's safe drop location",
        "__description_fr__": "Livré au lieu sûr du destinataire"
    },
    "1435": {
        "__default__": "ready_for_pickup",
        "__description_en__": "Notice card left indicating where and when to pick up item",
        "__description_fr__": "Un avis a été laissé pour indiquer où et quand l'article peut être ramassé"
    },
    "1436": {
        "__default__": "ready_for_pickup",
        "__description_en__": "Notice card left indicating where and when to pick up item",
        "__description_fr__": "Un avis a été laissé pour indiquer où et quand l'article peut être ramassé"
    },
    "1437": {
        "__default__": "ready_for_pickup",
        "__description_en__": "Notice card left indicating where and when to pick up item",
        "__description_fr__": "Un avis a été laissé pour indiquer où et quand l'article peut être ramassé"
    },
    "1438": {
        "__default__": "ready_for_pickup",
        "__description_en__": "Notice card left indicating where and when to pick up item",
        "__description_fr__": "Un avis a été laissé pour indiquer où et quand l'article peut être ramassé"
    },
    "1441": {
        "__default__": "delivered",
        "__description_en__": "Delivered to community mailbox or parcel locker",
        "__description_fr__": "Livré à la boîte postale communautaire ou à l'casier à colis"
    },
    "1442": {
        "__default__": "delivered",
        "__description_en__": "Delivered to community mailbox or parcel locker",
        "__description_fr__": "Livré à la boîte postale communautaire ou à l'casier à colis"
    },
    "1443": {
        "__default__": "on_hold",
        "__description_en__": "Attempted delivery. Item rescheduled for delivery next business day.",
        "__description_fr__": "Tentative de livraison. Reportée au jour ouvrable suivant."
    },
    "1444": {
        "__default__": "on_hold",
        "__description_en__": "Delivery scheduled for next business day",
        "__description_fr__": "Delivery scheduled for next business day"
    },
    "1450": {
        "__default__": "on_hold",
        "__description_en__": "Item on hold at a secure facility; contact Customer Service",
        "__description_fr__": "Envoi arrivé Centre d'envoi non distribuable. SVP communiquez Service clientèle"
    },
    "1461": {
        "__default__": "delivered",
        "__description_en__": "Delivered to your concierge or building manager",
        "__description_fr__": "Livré au concierge ou au gestionnaire de votre immeuble"
    },
    "1462": {
        "__default__": "delivered",
        "__description_en__": "Delivered to your concierge or building manager",
        "__description_fr__": "Livré au concierge ou au gestionnaire de votre immeuble"
    },
    "1463": {
        "__default__": "delivered",
        "__description_en__": "Delivered to mailroom",
        "__description_fr__": "Livré à la salle de courrier"
    },
    "1465": {
        "__default__": "delivered",
        "__description_en__": "Delivered to mailroom",
        "__description_fr__": "Livré à la salle de courrier"
    },
    "1466": {
        "__default__": "delivered",
        "__description_en__": "Delivered to mailroom",
        "__description_fr__": "Livré à la salle de courrier"
    },
    "1467": {
        "__default__": "delivered",
        "__description_en__": "Delivered to mailroom",
        "__description_fr__": "Delivered to mailroom"
    },
    "1468": {
        "__default__": "delivered",
        "__description_en__": "Delivered to mailroom",
        "__description_fr__": "Livré à la salle de courrier"
    },
    "1469": {
        "__default__": "delivered",
        "__description_en__": "Delivered to mailroom",
        "__description_fr__": "Delivered to mailroom"
    },
    "1471": {
        "__default__": "delivered",
        "__description_en__": "Delivered to recipient's delivery partner",
        "__description_fr__": "Livré au partenaire de livraison du destinataire"
    },
    "1472": {
        "__default__": "delivered",
        "__description_en__": "Delivered to recipient's delivery partner",
        "__description_fr__": "Livré au partenaire de livraison du destinataire"
    },
    "1473": {
        "__default__": "delivered",
        "__description_en__": "Delivered to mailroom",
        "__description_fr__": "Livré à la salle de courrier"
    },
    "1475": {
        "__default__": "delivered",
        "__description_en__": "Delivered to mailroom",
        "__description_fr__": "Livré à la salle de courrier"
    },
    "1476": {
        "__default__": "delivered",
        "__description_en__": "Delivered",
        "__description_fr__": "Delivered"
    },
    "1479": {
        "Tentative de renvoyer article à expéditeur. Carte laissée indiquant où ramasser": "return_to_sender",
        "Tentative de renvoyer article à expéditeur. Carte laissée indiquant où ramasser.": "return_to_sender",
        "__default__": "ready_for_pickup",
        "__description_en__": "Notice card left indicating where and when to pick up item",
        "__description_fr__": "Un avis a été laissé pour indiquer où et quand l'article peut être ramassé"
    },
    "1480": {
        "__default__": "out_for_delivery",
        "__description_en__": "Item redirected to recipient's new address",
        "__description_fr__": "Article réexpédié à la nouvelle adresse du destinataire."
    },
    "1481": {
        "__default__": "return_to_sender",
        "__description_en__": "Recipient not located at address provided. Item being returned to sender.",
        "__description_fr__": "Article refusé par le destinataire. Article retourné à l'expéditeur."
    },
    "1482": {
        "__default__": "return_to_sender",
        "__description_en__": "Item refused by recipient. Item being returned to sender.",
        "__description_fr__": "Article refusé ou non réclamé par le destinataire. Article retourné à l'exp."
    },
    "1483": {
        "__default__": "on_hold",
        "__description_en__": "Item cannot be delivered; more details to be provided",
        "__description_fr__": "Impossible livrer article tel qu'adressé; envoyé Centre d'envoi non distribuable"
    },
    "1484": {
        "__default__": "on_hold",
        "__description_en__": "Item on hold",
        "__description_fr__": "Article retenu"
    },
    "1487": {
        "__default__": "on_hold",
        "__description_en__": "Item being returned to Canadian Customs for appeal of duties",
        "__description_fr__": "Article retourné aux douanes canadiennes aux fins d'appel des droits"
    },
    "1488": {
        "__default__": "ready_for_pickup",
        "__description_en__": "Notice card left indicating where and when to pick up item",
        "__description_fr__": "Un avis a été laissé pour indiquer où et quand l'article peut être ramassé"
    },
    "1490": {
        "__default__": "out_for_delivery",
        "__description_en__": "Item redirected to recipient's new address",
        "__description_fr__": "Article réexpédié à la nouvelle adresse du destinataire"
    },
    "1491": {
        "__default__": "return_to_sender",
        "__description_en__": "Recipient not located at address provided. Item being returned to sender.",
        "__description_fr__": "Article refusé par le destinataire. Article retourné à l'expéditeur."
    },
    "1492": {
        "__default__": "return_to_sender",
        "__description_en__": "Item refused by recipient. Item being returned to sender.",
        "__description_fr__": "Article refusé ou non réclamé par le destinataire. Article retourné à l'exp."
    },
    "1493": {
        "__default__": "on_hold",
        "__description_en__": "Item cannot be delivered; more details to be provided",
        "__description_fr__": "Impossible livrer article tel qu'adressé; envoyé Centre d'envoi non distribuable"
    },
    "1494": {
        "__default__": "on_hold",
        "__description_en__": "Item on hold",
        "__description_fr__": "Article retenu"
    },
    "1495": {
        "__default__": "return_to_sender",
        "__description_en__": "Item being returned to Canadian Customs for appeal of duties",
        "__description_fr__": "Article retourné aux Douanes canadiennes aux fins d'appel des droits"
    },
    "1496": {
        "L'article a été renvoyé avec succès à l'expéditeur.": "return_to_sender",
        "__default__": "delivered",
        "__description_en__": "Delivered",
        "__description_fr__": "Livré"
    },
    "1498": {
        "L'article a été renvoyé avec succès à l'expéditeur.": "return_to_sender",
        "__default__": "delivered",
        "__description_en__": "Delivered",
        "__description_fr__": "Livré"
    },
    "150": {
        "__default__": "in_transit",
        "__description_en__": "Hold period expired; Item has been disposed of",
        "__description_fr__": "Période d'attente a expiré; Article a été éliminé"
    },
    "152": {
        "__default__": "in_transit",
        "__description_en__": "COD Payment is being issued",
        "__description_fr__": "Le paiement du CR est en cours d'exécution"
    },
    "156": {
        "__default__": "on_hold",
        "__description_en__": "Final Notice; Item will be returned to sender if not collected within 10 days",
        "__description_fr__": "Carte Avis final; renvoi à l'exp. si on ne le ramasse pas dans les dix jours"
    },
    "159": {
        "__default__": "on_hold",
        "__description_en__": "Delivery may be delayed due to extreme weather conditions",
        "__description_fr__": "Conditions météorologiques sévères à l'emplacement de livraison; article retardé"
    },
    "160": {
        "__default__": "on_hold",
        "__description_en__": "Delivery may be delayed due to public authority or demonstration",
        "__description_fr__": "Livraison retardée en raison de manifestations à cet emplacement"
    },
    "161": {
        "__default__": "on_hold",
        "__description_en__": "Delivery may be delayed due to labour disruption",
        "__description_fr__": "Interruption de travail touchant cet emplacement; article en retard"
    },
    "162": {
        "__default__": "on_hold",
        "__description_en__": "Delivery may be delayed due to transportation delay",
        "__description_fr__": "Livraison retardée en raison de délais de transport hors de notre contrôle"
    },
    "163": {
        "__default__": "on_hold",
        "__description_en__": "Delivery may be delayed due to power outage",
        "__description_fr__": "Panne d'électricité majeure touchant cet emplacement; article retardé"
    },
    "167": {
        "__default__": "return_to_sender",
        "__description_en__": "International item being returned to sender. Insufficient postage.",
        "__description_fr__": "Article international retourné à l'expéditeur. Affranchissement insuffisant."
    },
    "168": {
        "__default__": "return_to_sender",
        "__description_en__": "Item being returned to sender. Does not meet product requirements.",
        "__description_fr__": "Article int. renvoyé à l'expéditeur. Ne respecte pas les exigences du produit."
    },
    "169": {
        "__default__": "return_to_sender",
        "__description_en__": "International item being returned to sender. Incorrect or missing shipping label",
        "__description_fr__": "Article int. renvoyé à l'expéd.; étiquette d'expédition inexacte ou manquante"
    },
    "170": {
        "__default__": "picked_up",
        "__description_en__": "Item Processed",
        "__description_fr__": "Article traité"
    },
    "1701": {
        "__default__": "ready_for_pickup",
        "__description_en__": "Item available for pickup at Post Office",
        "__description_fr__": "Article peut être ramassé au bureau de poste"
    },
    "1703": {
        "Tentative de renvoyer article à expéditeur. Carte laissée indiquant où ramasser.": "on_hold",
        "__default__": "in_transit",
        "__description_en__": "Item in transit to Post Office",
        "__description_fr__": "Article en transit au bureau de poste"
    },
    "1705": {
        "__default__": "ready_for_pickup",
        "__description_en__": "Item in transit to automated parcel locker",
        "__description_fr__": "Item in transit to automated parcel locker"
    },
    "171": {
        "__default__": "in_transit",
        "__description_en__": "Verifying recipient's address; Possible delay",
        "__description_fr__": "Vérification de l'adresse du destinataire; délai possible"
    },
    "172": {
        "__default__": "on_hold",
        "__description_en__": "Item re-routed due to processing error; Possible delay",
        "__description_fr__": "Article réacheminé en raison d'une erreur de traitement; Délai possible"
    },
    "173": {
        "__default__": "on_hold",
        "__description_en__": "Customer addressing error found; attempting to correct. Possible delay",
        "__description_fr__": "Erreur d'adressage du client; tentative de correction. Délai possible"
    },
    "174": {
        "L'article renvoyé à l'expéditeur est sorti pour livraison.": "return_to_sender",
        "__default__": "out_for_delivery",
        "__description_en__": "Item out for delivery",
        "__description_fr__": "Article sorti pour livraison"
    },
    "175": {
        "__default__": "in_transit",
        "__description_en__": "Item in transit",
        "__description_fr__": "Article en transit"
    },
    "179": {
        "__default__": "in_transit",
        "__description_en__": "Item cannot be delivered; more details to be provided",
        "__description_fr__": "Envoyé au Centre d'envoi non distribuable; SVP contactez Service à la clientèle"
    },
    "181": {
        "__default__": "return_to_sender",
        "__description_en__": "Shipping label invalid. International Item being returned to sender",
        "__description_fr__": "Étiquette d'expédition invalide. Article international retourné à l'expéditeur"
    },
    "182": {
        "__default__": "return_to_sender",
        "__description_en__": "Documentation incomplete or illegible. Item being returned to sender",
        "__description_fr__": "Documentation incomplète ou illisible. Article retourné à l'expéditeur"
    },
    "183": {
        "__default__": "return_to_sender",
        "__description_en__": "Service suspended to country. Item being returned to sender",
        "__description_fr__": "Service suspendu à destination de ce pays. Article retourné à l'expéditeur"
    },
    "184": {
        "__default__": "return_to_sender",
        "__description_en__": "Itemis considered non-mailable matter. Item being returned to sender",
        "__description_fr__": "Cet article est un objet inadmissible. Il sera retourné à l'expéditeur"
    },
    "190": {
        "__default__": "in_transit",
        "__description_en__": "Retail transaction has been voided",
        "__description_fr__": "La transaction de vente au détail a été annulée"
    },
    "198": {
        "__default__": "in_transit",
        "__description_en__": "Label correction applied",
        "__description_fr__": "Correction d'étiquette appliquée"
    },
    "20": {
        "__default__": "delivered",
        "__description_en__": "Signature available",
        "__description_fr__": "Image de la signature enregistrée pour consultation en ligne"
    },
    "2001": {
        "__default__": "delivered",
        "__description_en__": "Photo available",
        "__description_fr__": "Photo disponible"
    },
    "21": {
        "__default__": "delivered",
        "__description_en__": "Signature unavailable; verbal signature.",
        "__description_fr__": "Signature unavailable; verbal signature."
    },
    "2101": {
        "__default__": "in_transit",
        "__description_en__": "Waiting for COD Remittance return",
        "__description_fr__": "En attente du retour des sommes perçues pour les envois CR."
    },
    "2300": {
        "__default__": "picked_up",
        "__description_en__": "Item picked up by Canada Post",
        "__description_fr__": "Envoi ramassé par Postes Canada"
    },
    "2407": {
        "Envoi disponible pour le ramassage": "ready_for_pickup",
        "__default__": "ready_for_pickup",
        "__description_en__": "Item available for pick-up",
        "__description_fr__": "Envoi disponible pour le ramassage par le client"
    },
    "2410": {
        "__default__": "delivery_delayed",
        "__description_en__": "Item on hold at recipient's request",
        "__description_fr__": "Article arrivé à l'installation postale. Article retenu à la demande du dest."
    },
    "2411": {
        "__default__": "on_hold",
        "__description_en__": "Business temporarily closed; item on hold",
        "__description_fr__": "Fermé pour la journée. Article retenu pour deuxième tentative de livraison."
    },
    "2412": {
        "L'article renvoyé à l'expéditeur est arrivé à l'installation postale.": "return_to_sender",
        "__default__": "on_hold",
        "__description_en__": "Verifying recipient's address; Possible delay",
        "__description_fr__": "Vérification de l'adresse du destinataire; délai possible"
    },
    "2414": {
        "__default__": "delivery_delayed",
        "__description_en__": "Item rescheduled for delivery next business day.",
        "__description_fr__": "La livraison de l'article est reportée au jour ouvrable suivant."
    },
    "2500": {
        "__default__": "picked_up",
        "__description_en__": "Item processed",
        "__description_fr__": "Article traité"
    },
    "2501": {
        "__default__": "picked_up",
        "__description_en__": "Item processed",
        "__description_fr__": "Article traité"
    },
    "2600": {
        "__default__": "return_to_sender",
        "__description_en__": "Item has been returned and is enroute to the Sender",
        "__description_fr__": "L'article a été retourné et est en route à l'Expéditeur"
    },
    "2601": {
        "__default__": "return_to_sender",
        "__description_en__": "Item is en route to Canadian Customs",
        "__description_fr__": "L'article est en route vers les douanes canadiennes"
    },
    "2802": {
        "__default__": "return_to_sender",
        "__description_en__": "International item was undeliverable. Item being returned to sender.",
        "__description_fr__": "Article international non livrable. Article retourné à l'expéditeur."
    },
    "3000": {
        "__default__": "pending",
        "__description_en__": "Electronic information submitted by shipper",
        "__description_fr__": "Les renseignements électroniques ont été soumis par l'expéditeur"
    },
    "3001": {
        "__default__": "return_to_sender",
        "__description_en__": "Item being returned to sender",
        "__description_fr__": "Article retourné à l'expéditeur"
    },
    "3002": {
        "__default__": "pending",
        "__description_en__": "Return label created",
        "__description_fr__": "Étiquette de retour créée"
    },
    "400": {
        "__default__": "in_transit",
        "__description_en__": "Item arrived",
        "__description_fr__": "Article arrivé"
    },
    "4000": {
        "__default__": "in_transit",
        "__description_en__": "International item mailed in origin country",
        "__description_fr__": "Article international expédié dans le pays d'origine"
    },
    "405": {
        "__default__": "in_transit",
        "__description_en__": "Item arrived",
        "__description_fr__": "Article arrivé"
    },
    "410": {
        "__default__": "in_transit",
        "__description_en__": "Item departed",
        "__description_fr__": "L'article est parti"
    },
    "4100": {
        "__default__": "in_transit",
        "__description_en__": "International item processed in origin country",
        "__description_fr__": "Article international traité dans le pays d'origine"
    },
    "4202": {
        "__default__": "in_transit",
        "__description_en__": "International item has left the origin country and is en route to Canada",
        "__description_fr__": "Article du régime internat. sorti du pays d'origine et en route pour le Canada"
    },
    "4310": {
        "__default__": "in_transit",
        "__description_en__": "International shipment has arrived in a foreign country",
        "__description_fr__": "Envoie du régime internationalarrivé au pays étranger"
    },
    "4311": {
        "__default__": "in_transit",
        "__description_en__": "International item has arrived in a foreign country",
        "__description_fr__": "Article du régime international arrivé au pays étranger"
    },
    "4330": {
        "__default__": "in_transit",
        "__description_en__": "Item Presented to Import Customs",
        "__description_fr__": "Article présenté à la douane pour examen"
    },
    "4400": {
        "__default__": "in_transit",
        "__description_en__": "Item has been sent to customs in the destination country",
        "__description_fr__": "Article envoyé aux douanes dans le pays de destination"
    },
    "4450": {
        "__default__": "in_transit",
        "__description_en__": "Item returned to Post from Customs",
        "__description_fr__": "Article retourné à la poste par les douanes",
        "importation refusée par les autorités douanières": "return_to_sender"
    },
    "4500": {
        "__default__": "in_transit",
        "__description_en__": "International item released from Customs to Foreign Postal Administration",
        "__description_fr__": "Article international remis par les Douanes à l'administration postale étrangère"
    },
    "4550": {
        "__default__": "in_transit",
        "__description_en__": "In Transit to Delivery Office",
        "__description_fr__": "Envoi en route vers le bureau de livraison"
    },
    "4600": {
        "__default__": "in_transit",
        "__description_en__": "Item has been received at the delivery office in the destination country",
        "__description_fr__": "Article reçu au bureau de livraison du pays de destination"
    },
    "4650": {
        "__default__": "return_to_sender",
        "__description_en__": "Item cannot be delivered; more details to be provided",
        "__description_fr__": "Impossible livrer article tel qu'adressé; envoyé Centre d'envoi non distribuable"
    },
    "4700": {
        "Article retenu": "on_hold",
        "Article retenu à la demande du destinataire": "on_hold",
        "Article réexpédié à la nouvelle adresse du destinataire.": "out_for_delivery",
        "Destinataire ne demeure pas à l'adresse indiquée. Article renvoyé à l'expéditeur": "return_to_sender",
        "Vérification de l'adresse du destinataire; délai possible": "on_hold",
        "__default__": "on_hold",
        "__description_en__": "Item on hold",
        "__description_fr__": "Article retenu"
    },
    "4900": {
        "__default__": "in_transit",
        "__description_en__": "International item has arrived at transit destination",
        "__description_fr__": "Article international arrivé au pays de transit"
    },
    "4950": {
        "__default__": "in_transit",
        "__description_en__": "International item has been forwarded onwards to destination",
        "__description_fr__": "Article international acheminé à la destination"
    },
    "500": {
        "__default__": "out_for_delivery",
        "__description_en__": "Out for delivery",
        "__description_fr__": "Sorti pour livraison"
    },
    "5201": {
        "__default__": "on_hold",
        "__description_en__": "International item released from Customs for processing by Canada Post",
        "__description_fr__": "Article international remis par les Douanes à PostesCanada"
    },
    "610": {
        "__default__": "in_transit",
        "__description_en__": "Item is with your concierge or building manager",
        "__description_fr__": "Item is with your concierge or building manager"
    },
    "611": {
        "__default__": "in_transit",
        "__description_en__": "Item is at recipient's front door",
        "__description_fr__": "Item is at recipient's front door"
    },
    "612": {
        "__default__": "in_transit",
        "__description_en__": "Item is at recipient's side door",
        "__description_fr__": "Item is at recipient's side door"
    },
    "613": {
        "__default__": "in_transit",
        "__description_en__": "Item is at or in recipient's garage",
        "__description_fr__": "Item is at or in recipient's garage"
    },
    "614": {
        "__default__": "in_transit",
        "__description_en__": "Item is at recipient's address",
        "__description_fr__": "Item is at recipient's address"
    },
    "615": {
        "__default__": "in_transit",
        "__description_en__": "Item received at recipient's address",
        "__description_fr__": "Item received at recipient's address"
    },
    "616": {
        "__default__": "in_transit",
        "__description_en__": "Item is in your community mailbox, parcel locker or apt./condo mailbox",
        "__description_fr__": "Item is in your community mailbox, parcel locker or apt./condo mailbox"
    },
    "617": {
        "__default__": "in_transit",
        "__description_en__": "Item is in recipient's mailroom",
        "__description_fr__": "Item is in recipient's mailroom"
    },
    "618": {
        "__default__": "in_transit",
        "__description_en__": "Item is in recipient's mailroom",
        "__description_fr__": "Item is in recipient's mailroom"
    },
    "619": {
        "__default__": "in_transit",
        "__description_en__": "Item is with recipient's delivery partner",
        "__description_fr__": "Item is with recipient's delivery partner"
    },
    "620": {
        "__default__": "in_transit",
        "__description_en__": "Item is in recipient's mailroom",
        "__description_fr__": "Item is in recipient's mailroom"
    },
    "621": {
        "__default__": "delivery_delayed",
        "__description_en__": "Delivery delayed to next business day",
        "__description_fr__": "Livraison reportée au prochain jour ouvrable"
    },
    "622": {
        "__default__": "delivery_delayed",
        "__description_en__": "Delivery delayed to next business day",
        "__description_fr__": "Livraison reportée au prochain jour ouvrable"
    },
    "623": {
        "__default__": "delivery_delayed",
        "__description_en__": "Delivery delayed to next business day",
        "__description_fr__": "Livraison reportée au prochain jour ouvrable"
    },
    "624": {
        "__default__": "on_hold",
        "__description_en__": "Delivery delayed to next business day",
        "__description_fr__": "Livraison reportée au prochain jour ouvrable"
    },
    "625": {
        "__default__": "delivery_delayed",
        "__description_en__": "Delivery delayed to next business day",
        "__description_fr__": "Livraison reportée au prochain jour ouvrable"
    },
    "626": {
        "__default__": "on_hold",
        "__description_en__": "Delivery delayed to next business day",
        "__description_fr__": "Delivery delayed to next business day"
    },
    "627": {
        "__default__": "delivery_delayed",
        "__description_en__": "Delivery delayed to next business day",
        "__description_fr__": "Livraison reportée au prochain jour ouvrable"
    },
    "628": {
        "__default__": "delivery_delayed",
        "__description_en__": "Delivery delayed to next business day",
        "__description_fr__": "Livraison reportée au prochain jour ouvrable"
    },
    "629": {
        "__default__": "in_transit",
        "__description_en__": "Locker pickup expired; Post office pickup details to follow",
        "__description_fr__": "Locker pickup expired; Post office pickup details to follow"
    },
    "630": {
        "__default__": "on_hold",
        "__description_en__": "Unable to deliver to locker; Post office pickup details to follow",
        "__description_fr__": "Unable to deliver to locker; Post office pickup details to follow"
    },
    "700": {
        "__default__": "in_transit",
        "__description_en__": "Unable to deliver to locker; Post office pickup details to follow",
        "__description_fr__": "Article arrivé au Canada et fut expédié au centre du traitement de courrier."
    },
    "701": {
        "__default__": "in_transit",
        "__description_en__": "Item has arrived in Canada and will be presented for review",
        "__description_fr__": "Item has arrived in Canada and will be presented for review"
    },
    "710": {
        "__default__": "in_transit",
        "__description_en__": "Item arrived in Canada damaged. Sent for further processing.",
        "__description_fr__": "Article arrivé au Canada endommagé. Envoyé pour traitement ultérieur"
    },
    "800": {
        "__default__": "in_transit",
        "__description_en__": "Item has been presented to Canada Border Services Agency for customs review.",
        "__description_fr__": "Présenté à l'Agence des services frontaliers du Canada pour dédouanement."
    },
    "804": {
        "__default__": "in_transit",
        "__description_en__": "Item in transit",
        "__description_fr__": "Article en transit"
    },
    "810": {
        "__default__": "in_transit",
        "__description_en__": "Item held by Customs",
        "__description_fr__": "Article détune par la douanes"
    },
    "815": {
        "__default__": "in_transit",
        "__description_en__": "International Item being prepared for export",
        "__description_fr__": "Article du régime international en préparation pour fins d'exportation"
    },
    "8901": {
        "__default__": "in_transit",
        "__description_en__": "If destination country is Canada, then the description is - International item being forwarded to destination country.If destination country is not Canada, then the description is - International item has transited Canada and been forwarded to destination.",
        "__description_fr__": "Article international en cours d'acheminement au pays de destination"
    },
    "900": {
        "__default__": "in_transit",
        "__description_en__": "International item released from Customs for processing by Canada Post",
        "__description_fr__": "Article international remis par les Douanes à PostesCanada"
    },
    "910": {
        "__default__": "in_transit",
        "__description_en__": "Item was released by Customs and is now with Canada Post for processing",
        "__description_fr__": "Dédouanement complété. Article fut expédié au centre du traitement de courrier."
    }
}


def normalize_tracking_event_identifier(event_identifier):
    raw = str(event_identifier or "").strip()
    if raw.isdigit():
        return str(int(raw))
    return raw


def map_tracking_status(event_identifier, event_description=None):
    normalized_event_id = normalize_tracking_event_identifier(event_identifier)
    description_mapping = TRACKING_STATUS_MAPPING.get(normalized_event_id)

    if not description_mapping:
        return "unknown"

    description = str(event_description or "")
    if description and description in description_mapping:
        return description_mapping[description]

    return description_mapping.get("__default__", "unknown")


def map_tracking_incident_reason(event_identifier):
    normalized_event_id = normalize_tracking_event_identifier(event_identifier)
    return next(
        (
            reason.name
            for reason in list(TrackingIncidentReason)
            if normalized_event_id in reason.value
        ),
        None,
    )


class TrackingIncidentReason(lib.Enum):
    """Maps Canada Post exception codes to normalized TrackingIncidentReason.

    Based on Canada Post tracking event codes.
    """
    # Carrier-caused issues
    carrier_damaged_parcel = ["119", "142", "143", "144", "145", "146", "147", "148", "149"]
    carrier_sorting_error = ["128", "129", "130", "131", "132", "133"]
    carrier_address_not_found = ["122", "123", "1413", "1440", "1485", "1486", "1489", "1490"]
    carrier_parcel_lost = ["124", "126", "151", "152", "153"]
    carrier_not_enough_time = ["155", "157", "158"]
    carrier_vehicle_issue = ["134", "135", "136", "137", "138"]

    # Consignee-caused issues
    consignee_refused = ["150", "1415", "1416"]
    consignee_business_closed = ["179", "181", "182"]
    consignee_not_available = ["183", "184", "190", "1418", "1419", "1420"]
    consignee_not_home = ["167", "168", "169", "1417"]
    consignee_incorrect_address = ["172", "173", "1482", "1483"]
    consignee_access_restricted = ["154", "180", "185", "186", "187", "188", "189"]

    # Customs-related issues
    customs_delay = ["810", "1443", "1484", "1487"]
    customs_documentation = ["117", "120", "121"]
    customs_duties_unpaid = ["125", "127", "1494"]

    # Weather/Force majeure
    weather_delay = ["159", "160", "161", "162", "163"]
    natural_disaster = ["164", "165", "166"]

    # Other issues
    unknown = []


INTERNATIONAL_NON_DELIVERY_OPTION = [
    ShippingOption.canadapost_return_at_senders_expense.name,
    ShippingOption.canadapost_return_to_sender.name,
    ShippingOption.canadapost_abandon.name,
]

CUSTOM_OPTIONS = [
    ShippingOption.canadapost_cost_center.name,
    ShippingOption.canadapost_submit_shipment.name,
]


def load_services_from_csv() -> list:
    csv_path = pathlib.Path(__file__).resolve().parent / "services.csv"
    if not csv_path.exists():
        return []
    services_dict: dict[str, dict] = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            service_code = row["service_code"]
            karrio_service_code = ServiceType.map(service_code).name_or_key
            if karrio_service_code not in services_dict:
                services_dict[karrio_service_code] = {
                    "service_name": row["service_name"],
                    "service_code": karrio_service_code,
                    "currency": row.get("currency", "CAD"),
                    "min_weight": float(row["min_weight"]) if row.get("min_weight") else None,
                    "max_weight": float(row["max_weight"]) if row.get("max_weight") else None,
                    "max_length": float(row["max_length"]) if row.get("max_length") else None,
                    "max_width": float(row["max_width"]) if row.get("max_width") else None,
                    "max_height": float(row["max_height"]) if row.get("max_height") else None,
                    "weight_unit": "KG",
                    "dimension_unit": "CM",
                    "domicile": (row.get("domicile") or "").lower() == "true",
                    "international": True if (row.get("international") or "").lower() == "true" else None,
                    "zones": [],
                }
            country_codes = [c.strip() for c in row.get("country_codes", "").split(",") if c.strip()]
            zone = models.ServiceZone(
                label=row.get("zone_label", "Default Zone"),
                rate=float(row.get("rate", 0.0)),
                min_weight=float(row["min_weight"]) if row.get("min_weight") else None,
                max_weight=float(row["max_weight"]) if row.get("max_weight") else None,
                transit_days=int(row["transit_days"].split("-")[0]) if row.get("transit_days") and row["transit_days"].split("-")[0].isdigit() else None,
                country_codes=country_codes if country_codes else None,
            )
            services_dict[karrio_service_code]["zones"].append(zone)
    return [models.ServiceLevel(**service_data) for service_data in services_dict.values()]


DEFAULT_SERVICES = load_services_from_csv()
