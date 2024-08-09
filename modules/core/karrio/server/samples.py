CARRIER_DETAILS_SAMPLE = """{
  "carrier_name": "dhl_express",
  "display_name": "DHL Express",
  "connection_fields": {
    "site_id": {
      "name": "site_id",
      "required": true,
      "type": "string"
    },
    "password": {
      "name": "password",
      "required": true,
      "type": "string"
    },
    "account_number": {
      "name": "account_number",
      "required": false,
      "type": "string"
    }
  },
  "capabilities": ["paperless", "shipping", "tracking", "rating", "pickup"],
  "config_fields": {
    "label_type": {
      "code": "label_type",
      "name": "label_type",
      "required": false,
      "type": "string"
    },
    "skip_service_filter": {
      "code": "skip_service_filter",
      "name": "skip_service_filter",
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
