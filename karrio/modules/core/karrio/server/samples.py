CARRIER_DETAILS_SAMPLE = """{
  "carrier_name": "dhl_parcel_de",
  "display_name": "DHL Parcel DE",
  "integration_status": "in-development",
  "capabilities": [
    "rating",
    "shipping",
    "tracking"
  ],
  "connection_fields": {
    "username": {
      "name": "username",
      "required": true,
      "type": "string"
    },
    "password": {
      "name": "password",
      "required": true,
      "type": "string"
    },
    "dhl_api_key": {
      "name": "dhl_api_key",
      "required": true,
      "type": "string"
    },
    "customer_number": {
      "name": "customer_number",
      "required": false,
      "type": "string"
    },
    "tracking_consumer_key": {
      "name": "tracking_consumer_key",
      "required": false,
      "type": "string"
    },
    "tracking_consumer_secret": {
      "name": "tracking_consumer_secret",
      "required": false,
      "type": "string"
    },
    "services": {
      "default": [
        {
          "active": true,
          "currency": "EUR",
          "dimension_unit": "CM",
          "domicile": true,
          "max_height": 60,
          "max_length": 120,
          "max_weight": 31.5,
          "max_width": 60,
          "metadata": {},
          "min_weight": 0.01,
          "service_code": "dhl_parcel_de_paket",
          "service_name": "DHL Paket",
          "weight_unit": "KG",
          "zones": [
            {
              "rate": 0.0
            }
          ]
        },
        {
          "active": true,
          "currency": "EUR",
          "dimension_unit": "CM",
          "domicile": false,
          "international": true,
          "max_height": 60,
          "max_length": 120,
          "max_weight": 31.5,
          "max_width": 60,
          "metadata": {},
          "min_weight": 0.01,
          "service_code": "dhl_parcel_de_paket_international",
          "service_name": "DHL Paket International",
          "weight_unit": "KG",
          "zones": [
            {
              "rate": 0.0
            }
          ]
        },
        {
          "active": true,
          "currency": "EUR",
          "dimension_unit": "CM",
          "domicile": false,
          "international": true,
          "max_height": 60,
          "max_length": 120,
          "max_weight": 31.5,
          "max_width": 60,
          "metadata": {},
          "min_weight": 0.01,
          "service_code": "dhl_parcel_de_europaket",
          "service_name": "DHL EuroPaket",
          "weight_unit": "KG",
          "zones": [
            {
              "rate": 0.0
            }
          ]
        },
        {
          "active": true,
          "currency": "EUR",
          "dimension_unit": "CM",
          "domicile": true,
          "international": false,
          "max_height": 5,
          "max_length": 35,
          "max_weight": 1,
          "max_width": 7,
          "metadata": {},
          "min_weight": 0.01,
          "service_code": "dhl_parcel_de_warenpost",
          "service_name": "DHL Warenpost",
          "weight_unit": "KG",
          "zones": [
            {
              "rate": 0.0
            }
          ]
        },
        {
          "active": true,
          "currency": "EUR",
          "dimension_unit": "CM",
          "domicile": false,
          "international": true,
          "max_height": 10,
          "max_length": 35.3,
          "max_weight": 1,
          "max_width": 9,
          "metadata": {},
          "min_weight": 0.01,
          "service_code": "dhl_parcel_de_warenpost_international",
          "service_name": "DHL Warenpost International",
          "weight_unit": "KG",
          "zones": [
            {
              "rate": 0.0
            }
          ]
        }
      ],
      "name": "services",
      "required": false,
      "type": "list"
    }
  },
  "config_fields": {
    "profile": {
      "code": "profile",
      "name": "profile",
      "required": false,
      "type": "string"
    },
    "cost_center": {
      "code": "cost_center",
      "name": "cost_center",
      "required": false,
      "type": "string"
    },
    "creation_software": {
      "code": "creation_software",
      "name": "creation_software",
      "required": false,
      "type": "string"
    },
    "shipping_options": {
      "code": "shipping_options",
      "name": "shipping_options",
      "required": false,
      "type": "list"
    },
    "shipping_services": {
      "code": "shipping_services",
      "name": "shipping_services",
      "required": false,
      "type": "list"
    },
    "language": {
      "code": "language",
      "enum": [
        "de",
        "en"
      ],
      "name": "language",
      "required": false,
      "type": "string"
    },
    "label_type": {
      "code": "label_type",
      "enum": [
        "PDF_A4",
        "ZPL2_A4",
        "PDF_910_300_700",
        "ZPL2_910_300_700",
        "PDF_910_300_700_oz",
        "ZPL2_910_300_700_oz",
        "PDF_910_300_710",
        "ZPL2_910_300_710",
        "PDF_910_300_600",
        "ZPL2_910_300_600",
        "PDF_910_300_610",
        "ZPL2_910_300_610",
        "PDF_910_300_400",
        "ZPL2_910_300_400",
        "PDF_910_300_410",
        "ZPL2_910_300_410",
        "PDF_910_300_300",
        "ZPL2_910_300_300",
        "PDF_910_300_300_oz",
        "ZPL2_910_300_300_oz"
      ],
      "name": "label_type",
      "required": false,
      "type": "string"
    }
  },
  "shipping_services": {
    "dhl_parcel_de_paket": "V01PAK",
    "dhl_parcel_de_warenpost": "V62WP",
    "dhl_parcel_de_europaket": "V54EPAK",
    "dhl_parcel_de_paket_international": "V53WPAK",
    "dhl_parcel_de_warenpost_international": "V66WPI"
  },
  "shipping_options": {
    "dhl_parcel_de_preferred_neighbour": {
      "code": "preferredNeighbour",
      "type": "string",
      "default": null
    },
    "dhl_parcel_de_preferred_location": {
      "code": "preferredLocation",
      "type": "string",
      "default": null
    },
    "dhl_parcel_de_visual_check_of_age": {
      "code": "visualCheckOfAge",
      "type": "string",
      "default": null
    },
    "dhl_parcel_de_named_person_only": {
      "code": "namedPersonOnly",
      "type": "boolean",
      "default": null
    },
    "dhl_parcel_de_signed_for_by_recipient": {
      "code": "signedForByRecipient",
      "type": "boolean",
      "default": null
    },
    "dhl_parcel_de_endorsement": {
      "code": "endorsement",
      "type": "string",
      "default": null
    },
    "dhl_parcel_de_preferred_day": {
      "code": "preferredDay",
      "type": "string",
      "default": null
    },
    "dhl_parcel_de_no_neighbour_delivery": {
      "code": "noNeighbourDelivery",
      "type": "boolean",
      "default": null
    },
    "dhl_parcel_de_additional_insurance": {
      "code": "additionalInsurance",
      "type": "float",
      "default": null
    },
    "dhl_parcel_de_bulky_goods": {
      "code": "bulkyGoods",
      "type": "boolean",
      "default": null
    },
    "dhl_parcel_de_cash_on_delivery": {
      "code": "cashOnDelivery",
      "type": "float",
      "default": null
    },
    "dhl_parcel_de_individual_sender_requirement": {
      "code": "individualSenderRequirement",
      "type": "string",
      "default": null
    },
    "dhl_parcel_de_premium": {
      "code": "premium",
      "type": "boolean",
      "default": null
    },
    "dhl_parcel_de_closest_drop_point": {
      "code": "closestDropPoint",
      "type": "boolean",
      "default": null
    },
    "dhl_parcel_de_parcel_outlet_routing": {
      "code": "parcelOutletRouting",
      "type": "string",
      "default": null
    },
    "dhl_parcel_de_postal_delivery_duty_paid": {
      "code": "postalDeliveryDutyPaid",
      "type": "boolean",
      "default": null
    }
  }
}
"""

CARRIER_SERICES_SAMPLE = """{
	"canadapost_regular_parcel": "DOM.RP",
	"canadapost_expedited_parcel": "DOM.EP",
	"canadapost_xpresspost": "DOM.XP",
	"canadapost_xpresspost_certified": "DOM.XP.CERT",
	"canadapost_priority": "DOM.PC",
	"canadapost_library_books": "DOM.LIB",
	"canadapost_expedited_parcel_usa": "USA.EP",
	"canadapost_priority_worldwide_envelope_usa": "USA.PW.ENV",
	"canadapost_priority_worldwide_pak_usa": "USA.PW.PAK",
	"canadapost_priority_worldwide_parcel_usa": "USA.PW.PARCEL",
	"canadapost_small_packet_usa_air": "USA.SP.AIR",
	"canadapost_tracked_packet_usa": "USA.TP",
	"canadapost_tracked_packet_usa_lvm": "USA.TP.LVM",
	"canadapost_xpresspost_usa": "USA.XP",
	"canadapost_xpresspost_international": "INT.XP",
	"canadapost_international_parcel_air": "INT.IP.AIR",
	"canadapost_international_parcel_surface": "INT.IP.SURF",
	"canadapost_priority_worldwide_envelope_intl": "INT.PW.ENV",
	"canadapost_priority_worldwide_pak_intl": "INT.PW.PAK",
	"canadapost_priority_worldwide_parcel_intl": "INT.PW.PARCEL",
	"canadapost_small_packet_international_air": "INT.SP.AIR",
	"canadapost_small_packet_international_surface": "INT.SP.SURF",
	"canadapost_tracked_packet_international": "INT.TP"
}
"""

CARRIER_OPTIONS_SAMPLE = """{
  "sendle_hide_pickup_address": {
    "code": "hide_pickup_address",
    "type": "boolean",
  },
  "sendle_first_mile_option": {
    "code": "first_mile_option",
    "type": "boolean",
  }
}
"""