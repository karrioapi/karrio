import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestGEODISShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.geodis.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.geodis.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "service": "chronopost_13",
    "shipper": {
        "company_name": "Chef Royale",
        "person_name": "Jean Dupont",
        "address_line1": "28 rue du Clair Bocage",
        "city": "La Seyne-sur-mer",
        "postal_code": "83500",
        "country_code": "FR",
        "phone_number": "+330447110494",
    },
    "recipient": {
        "company_name": "HautSide",
        "person_name": "Lucas Dupont",
        "address_line1": "72 rue Reine Elisabeth",
        "city": "Menton",
        "postal_code": "06500",
        "country_code": "FR",
    },
    "parcels": [
        {
            "height": 15,
            "length": 60.0,
            "width": 30,
            "weight": 5.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        }
    ],
    "label_type": "PDF",
    "reference": "Ref. 123456",
    "options": {"shipment_date": "2022-08-16"},
}

ParsedShipmentResponse = [
    {
        "carrier_id": "geodis",
        "carrier_name": "geodis",
        "docs": {"label": ANY},
        "shipment_identifier": "2LM2095",
        "tracking_number": "2LM2095",
    },
    [],
]


ShipmentRequest = {
    "codeSaAgenceDepart": "001175",
    "codeTeosAgenceDepart": "",
    "codeClient": "020475",
    "formatImpression": "P",
    "positionPremiereEtiquette": 1,
    "codeLangue": "fr",
    "codeProduit": "ATK",
    "noRecepisse": "90148526",
    "dateDepart": "2021-12-23",
    "dateLivraison": "2021-12-24",
    "expediteur": {
        "nom": "COMPTE TEST TMA IBM/GEODIS",
        "codePays": "FR",
        "codeRegion": "95",
        "codePostal": "95300",
        "ville": "PONTOISE",
        "telephoneContact": "0102030405",
    },
    "destinataire": {
        "code": "CAS02",
        "nom": "CAS02 DSI",
        "adresse1": "13 RUE PIERRE ET MARIE CURIE",
        "adresse2": "",
        "codePays": "FR",
        "codePostal": "95135",
        "ville": "FRANCONVILLE BP150",
        "nomContact": "M. CASUAL",
        "telephoneContact": "+33601050402",
    },
    "nombreTotalUM": 3,
    "nombreTotalPalettes": 1,
    "poidsTotal": 220,
    "volumeTotal": 1.9,
    "listeUmg": [
        {
            "codeUmg": "PE",
            "poids": 150,
            "volume": 1.5,
            "numeroColis": 1,
            "cabTransporteur": "JVGTS0020000000003652",
            "cabEuropeTransporteur": "NEE000321511",
            "referenceColisClient": "CMD095-184722-X001",
            "listeArticle": [
                {"code": "BOU", "reference": "Rhum BOLOGNE", "quantite": 5},
                {"code": "BOU", "reference": "Rhum NEGRITA", "quantite": 5},
                {"code": "BOU", "reference": "Rhum ISAUTIER", "quantite": 10},
                {"code": "BOU", "reference": "Rhum SAVANNA", "quantite": 5},
                {
                    "code": "BOU",
                    "reference": "Rhum CORMAN COLLINS RHUMS",
                    "quantite": 15,
                },
            ],
        },
        {
            "codeUmg": "PC",
            "poids": 50,
            "volume": 0.3,
            "numeroColis": 2,
            "cabTransporteur": "JVGTS0020000000003653",
            "cabEuropeTransporteur": "NEE000321512",
            "referenceColisClient": "CMD095-184722-X002",
        },
        {
            "codeUmg": "PC",
            "poids": 20,
            "volume": 0.1,
            "numeroColis": 3,
            "cabTransporteur": "JVGTS0020000000003654",
            "cabEuropeTransporteur": "NEE000321513",
            "referenceColisClient": "CMD095-184722-X003",
        },
    ],
    "codeOptionLivraison": "A00",
    "reference1": "F1708-3433",
}

ShipmentResponse = """{
  "ok": true,
  "codeErreur": "string",
  "texteErreur": "string",
  "contenu": {
    "fluxEtiquettes": "JVBERi0xLjQKJeLjz9MKMyAwIG9iago8PC9Db2xvclNwYWNlL0RldmljZUdyYXkvU3VidHlwZS9JbWFnZS9IZWlnaHQgNjIvRmlsdGVyL0ZsYXRlRGVjb2RlL1R5cGUvWE9iamVjdC9EZWNvZGVQYXJtczw8L0NvbHVtbnMgMTIxL0NvbG9ycyAxL1ByZWRpY3RvciAxNS9CaXRzUGVyQ29tcG9uZW50IDE+Pi9XaWR0aCAxMjEvTGVuZ3RoIDM2L0JpdHNQZXJDb21wb25lbnQgMT4+c3RyZWFtCnjaY/h/urK3SGOuwGwRvfN+mv8bGEYFRgVGBUYFQAIA+nve3gplbmRzdHJlYW0KZW5kb2JqCjQgMCBvYmoKPDwvQ29sb3JTcGFjZS9EZXZpY2VHcmF5L1N1YnR5cGUvSW1hZ2UvSGVpZ2h0IDU3L0ZpbHRlci9GbGF0ZURlY29kZS9UeXBlL1hPYmplY3QvRGVjb2RlUGFybXM8PC9Db2x1bW5zIDIwOS9Db2xvcnMgMS9QcmVkaWN0b3IgMTUvQml0c1BlckNvbXBvbmVudCAxPj4vV2lkdGggMjA5L0xlbmd0aCA1Mi9CaXRzUGVyQ29tcG9uZW50IDE+PnN0cmVhbQp42mP4f7rKXeTpnb6JJU4+ZzuN1VLOzFxeZHXznOb/BoZRuVG5UblRuVG5UTkscgAkBUCxCmVuZHN0cmVhbQplbmRvYmoKNSAwIG9iago8PC9Db2xvclNwYWNlL0RldmljZUdyYXkvU3VidHlwZS9JbWFnZS9IZWlnaHQgMzMvRmlsdGVyL0ZsYXRlRGVjb2RlL1R5cGUvWE9iamVjdC9EZWNvZGVQYXJtczw8L0NvbHVtbnMgMjQyL0NvbG9ycyAxL1ByZWRpY3RvciAxNS9CaXRzUGVyQ29tcG9uZW50IDE+Pi9XaWR0aCAyNDIvTGVuZ3RoIDUxL0JpdHNQZXJDb21wb25lbnQgMT4+c3RyZWFtCnjaY/h/unqny8u7nb1GZicucvYWqulybDK8dOTGbMkSdZH/BxhG5UflR+VHrDwAM6AOkwplbmRzdHJlYW0KZW5kb2JqCjYgMCBvYmoKPDwvQ29sb3JTcGFjZS9EZXZpY2VHcmF5L1N1YnR5cGUvSW1hZ2UvSGVpZ2h0IDYyL0ZpbHRlci9GbGF0ZURlY29kZS9UeXBlL1hPYmplY3QvRGVjb2RlUGFybXM8PC9Db2x1bW5zIDEyMS9Db2xvcnMgMS9QcmVkaWN0b3IgMTUvQml0c1BlckNvbXBvbmVudCAxPj4vV2lkdGggMTIxL0xlbmd0aCAzNi9CaXRzUGVyQ29tcG9uZW50IDE+PnN0cmVhbQp42mP4f7qyt0hjrsBsEb3zfpr/GxhGBUYFRgVGBUACAPp73t4KZW5kc3RyZWFtCmVuZG9iago3IDAgb2JqCjw8L0NvbG9yU3BhY2UvRGV2aWNlR3JheS9TdWJ0eXBlL0ltYWdlL0hlaWdodCA1Ny9GaWx0ZXIvRmxhdGVEZWNvZGUvVHlwZS9YT2JqZWN0L0RlY29kZVBhcm1zPDwvQ29sdW1ucyAyMDkvQ29sb3JzIDEvUHJlZGljdG9yIDE1L0JpdHNQZXJDb21wb25lbnQgMT4+L1dpZHRoIDIwOS9MZW5ndGggNTIvQml0c1BlckNvbXBvbmVudCAxPj5zdHJlYW0KeNpj+H+6yl3k6Z2+iSVOPmc7jdVSzsxcXmR185zm/waGUblRuVG5UblRuVE5LHIAJAVAsQplbmRzdHJlYW0KZW5kb2JqCjggMCBvYmoKPDwvQ29sb3JTcGFjZS9EZXZpY2VHcmF5L1N1YnR5cGUvSW1hZ2UvSGVpZ2h0IDMzL0ZpbHRlci9GbGF0ZURlY29kZS9UeXBlL1hPYmplY3QvRGVjb2RlUGFybXM8PC9Db2x1bW5zIDI0Mi9Db2xvcnMgMS9QcmVkaWN0b3IgMTUvQml0c1BlckNvbXBvbmVudCAxPj4vV2lkdGggMjQyL0xlbmd0aCA1MS9CaXRzUGVyQ29tcG9uZW50IDE+PnN0cmVhbQp42mP4f7p6p8vLu529RmYnLnL2FqrpcmwyvHTkxmzJEnWR/",
    "destinataire": {
      "codePays": "FR",
      "codePostal": "95130",
      "ville": "FRANCONVILLE"
    },
    "reseau": "M",
    "priorite": "2",
    "codire": "095",
    "cabRouting": "2LM2095",
    "listeUmg": [
      {
        "codeUmg": "PE",
        "numeroColis": 1,
        "cabTransporteur": "JVGTS0020000000003652",
        "cabEuropeTransporteur": "NEE000321511",
        "referenceColisClient": "CMD095-184722-X001"
      },
      {
        "codeUmg": "PC",
        "numeroColis": 2,
        "cabTransporteur": "JVGTS0020000000003653",
        "cabEuropeTransporteur": "NEE000321512",
        "referenceColisClient": "CMD095-184722-X002"
      },
      {
        "codeUmg": "PC",
        "numeroColis": 3,
        "cabTransporteur": "JVGTS0020000000003654",
        "cabEuropeTransporteur": "NEE000321513",
        "referenceColisClient": "CMD095-184722-X003"
      }
    ],
    "direction": "TEOM2095"
  }
}
"""
