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
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **CancelShipmentPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )

        self.assertEqual(request.serialize(), CancelShipmentRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.geodis.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/wsclient/enregistrement-envois",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.geodis.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.ups.proxy.lib.request") as mock:
            mock.return_value = CancelShipmentResponse
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedShipmentCancelResponse
            )


if __name__ == "__main__":
    unittest.main()

CancelShipmentPayload = {"shipment_identifier": "1G08Q6PK6PHP"}

ShipmentPayload = {
    "service": "geodis_MES",
    "shipper": {
        "company_name": "ESPACE 2 ROCHEFORT",
        "person_name": "Mme Titi",
        "address_line1": "PLACE DU MARCHE",
        "city": "ROCHEFORT",
        "postal_code": "17300",
        "country_code": "FR",
        "phone_number": "0200000000",
        "email": "a@b.fr",
        "suite": "1789",
        "residential": False,
    },
    "recipient": {
        "company_name": "M. DESTI",
        "person_name": "M. Toto",
        "address_line1": "12 avenue du webservice",
        "address_line2": "ZA wsclient",
        "city": "PARIS 01",
        "postal_code": "75001",
        "country_code": "FR",
        "phone_number": "0100000000",
        "email": "x@y.fr",
        "suite": "1515",
    },
    "parcels": [
        {
            "width": 30,
            "weight": 1.24,
            "weight_unit": "KG",
        }
    ],
    "label_type": "ZPL_200dpi",
    "reference": "ref-1",
    "options": {
        "shipment_date": "2023-10-17",
        "geodis_web_appointment": True,
        "email_notification_to": "w@z.fr",
        "geodis_instruction_enlevement": "Entree fournisseurs",
        "geodis_instruction_livraison": "5ème sans ascenseur",
    },
}

ParsedShipmentResponse = [
    {
        "carrier_id": "geodis",
        "carrier_name": "geodis",
        "docs": {"label": ANY},
        "label_type": "ZPL_200dpi",
        "shipment_identifier": "1G0V6AFZ5TER",
        "tracking_number": "1G0V6AFZ5TER",
        "meta": {"codeProduit": "MES", "noRecepisse": "90000001"},
    },
    [],
]

ParsedShipmentCancelResponse = [
    {
        "carrier_id": "geodis",
        "carrier_name": "geodis",
        "operation": "Cancel Shipment",
        "success": True,
    },
    [],
]


ShipmentRequest = {
    "formatEtiquette": "1",
    "impressionBordereau": False,
    "impressionEtiquette": True,
    "impressionRecapitulatif": True,
    "listEnvois": [
        {
            "codeClient": "601911",
            "codeIncotermConditionLivraison": "P",
            "codeProduit": "MES",
            "codeSa": "020017",
            "dateDepartEnlevement": "2023-10-17",
            "destinataire": {
                "adresse1": "12 avenue du webservice",
                "adresse2": "ZA wsclient",
                "codePays": "FR",
                "codePorte": "1515",
                "codePostal": "75001",
                "email": "x@y.fr",
                "nom": "M. DESTI",
                "nomContact": "M. Toto",
                "particulier": False,
                "telFixe": "0100000000",
                "ville": "PARIS 01",
            },
            "emailNotificationDestinataire": "w@z.fr",
            "emailNotificationExpediteur": "a@b.fr",
            "expediteur": {
                "adresse1": "PLACE DU MARCHE",
                "codePays": "FR",
                "codePorte": "1789",
                "codePostal": "17300",
                "email": "a@b.fr",
                "nom": "ESPACE 2 ROCHEFORT",
                "nomContact": "Mme Titi",
                "particulier": False,
                "telFixe": "0200000000",
                "ville": "ROCHEFORT",
            },
            "instructionEnlevement": "Entree fournisseurs",
            "instructionLivraison": "5ème sans ascenseur",
            "listUmgs": [
                {
                    "largeurUnitaire": 30.0,
                    "palette": False,
                    "poids": 1.24,
                    "quantite": 1,
                }
            ],
            "listVinsSpiritueux": [None],
            "optionLivraison": "RDW",
            "poidsTotal": 1.24,
            "reference1": "ref-1",
            "smsNotificationDestinataire": "0200000000",
        }
    ],
    "suppressionSiEchecValidation": True,
    "typeImpressionEtiquette": "Z",
}

CancelShipmentRequest = {"listNosSuivis": ["1G08Q6PK6PHP"]}

ShipmentResponse = """{
    "ok": true,
    "codeErreur": null,
    "texteErreur": null,
    "contenu": {
        "msgErreur": null,
        "nbEnvoisATraiter": 1,
        "nbEnvoisEnregistres": 1,
        "nbEnvoisValides": 0,
        "nbEnvoisEtiquetes": 0,
        "nbEnvoisSupprimes": 0,
        "nbAnomaliesSuppression": 0,
        "nbAnomaliesEtiquette": 0,
        "nbAnomaliesBordereau": 0,
        "nbAnomaliesRecapitulatif": 0,
        "docEtiquette": null,
        "docBordereau": null,
        "docRecapitulatif": null,
        "msgErreurEtiquette": null,
        "msgErreurBordereau": null,
        "msgErreurRecapitulatif": null,
        "listRetoursEnvois": [
            {
                "index": 0,
                "horsSite": false,
                "codeSa": "020017",
                "codeClient": "601911",
                "codeProduit": "MES",
                "reference1": "ref-1",
                "reference2": "ref-2",
                "dateDepartEnlevement": "2023-10-17",
                "destinataire": {
                    "nom": "M. DESTI",
                    "adresse1": "12 avenue du webservice",
                    "adresse2": "ZA wsclient",
                    "codePostal": "75001",
                    "ville": "PARIS 01",
                    "codePays": "FR",
                    "email": "x@y.fr",
                    "telFixe": "0100000000",
                    "indTelMobile": "33",
                    "telMobile": "0600000000",
                    "nomContact": "M. Toto",
                    "codePorte": "1515",
                    "codeTiers": null,
                    "noEntrepositaireAgree": null,
                    "particulier": null
                },
                "noRecepisse": "90000001",
                "noSuivi": "1G0V6AFZ5TER",
                "urlSuiviDestinataire": "",
                "listRetoursUM": [
                    {
                        "numeroUM": 1,
                        "typeUM": "PC",
                        "referenceUM": "",
                        "cabGeodisUM": "",
                        "cabGeodisEuropeUM": ""
                    }
                ],
                "docEtiquette": {
                    "nom": "Etiquettes_20200319-190937.txt",
                    "type": "txt",
                    "contenu": "XlhBCl5QUjcsNyw4Xk1DWV5MUk5eRldOXkNGRCwyNF5MSDUsMTVeQ0kwXk1OWV5NVEReTUQwXlBPTl5QTU4KXkxMMTA4MApeRk8wMDAsMDAwXkdCODMwLDAwMCwzLEIsMF5GUwpeRk8xMTUsMDAwXkdCMDAwLDEyMCwzLEIsMF5GUwpeRk8zMjAsMDAwXkdCMDAwLDEyMCwzLEIsMF5GUwpeRk81NzYsMDAwXkdCMDAwLDEyMCwzLEIsMF5GUwpeRk81NzYsMDYwXkdCMjUyLDAwMCwzLEIsMF5GUwpeRk8wMDAsMTIwXkdCODMwLDAwMCwzLEIsMF5GUwpeRk8yMTYsMTIwXkdCMDAwLDI1NiwzLEIsMF5GUwpeRk81NjAsMTIwXkdCMDAwLDA1NiwzLEIsMF5GUwpeRk8wMDAsMTc2XkdCODMwLDAwMCwzLEIsMF5GUwpeRk8wMDAsMjc4XkdCMjE2LDAwMCwzLEIsMF5GUwpeRk8wMDAsMzc2XkdCODMwLDAwMCwzLEIsMF5GUwpeRk8wMDAsNDE2XkdCODMwLDAwMCwxLEIsMF5GUwpeRlggLS1ERUJVVCBJTVBSRVNTSU9OIERPTk5FRVMtLSBeRlMKXkEwTiwxMzUsMTEwXkZPMDA1LDAxM15DSTBeRkRNXkZTCl5BME4sMDkwLDA4MF5GTzA4MCwwNDdeQ0kwXkZEMl5GUwpeQTBOLDExMCwxMjBeRk8xMjAsMDMwXkNJMF5GRDJeRlMKXkEwTiwxNDAsMTMwXkZPMTgwLDAxMF5DSTBeRkQ3NV5GUwpeQTBOLDA2MCwwNzBeRk81OTAsMDEwXkNJMF5GRF5GUwpeQTBOLDA2MCwwNzBeRk81OTAsMDY4XkNJMF5GRF5GUwpeQTBOLDAyNSwwMTheRk8wMDAsMTI4XkNJMF5GRDAxNyBHRU9ESVMgUk9DSEVGT1JUXkZTCl5BME4sMDI1LDAxOF5GTzAwMCwxNTJeQ0kwXkZEVGVsOiAwODkyMDUyODI4XkZTCl5BME4sMDI1LDAxOF5GTzIyNCwxNTJeQ0kwXkZEU2hwOl5GUwpeQTBOLDA0NSwwMzBeRk8yNjAsMTM2XkNJMF5GRDkyMjE2NTAxXkZTCl5BME4sMDI1LDAxOF5GTzM3NiwxNTJeQ0kwXkZEZnJvbV5GUwpeQTBOLDA0NSwwMzBeRk80MTYsMTM2XkNJMF5GRDIwLzAzLzIwMjBeRlMKXkEwTiwwNDUsMDMwXkZPNTY4LDEzNl5DSTBeRkReRlMKXkEwTiwwMzgsMDIwXkZPMDAwLDE4MF5DSTBeRkRXRVNUQklLRV5GUwpeQTBOLDAzOCwwMjBeRk8wMDAsMjE0XkNJMF5GRDA3MDAwMDAwMDBeRlMKXkEwTiwwMzgsMDIwXkZPMDAwLDI0OF5DSTBeRkReRlMKXkEwTiwwNDUsMDM1XkZPMjI4LDE4NF5DSTBeRkRNLiBERVNUSV5GUwpeQTBOLDAzMCwwMjVeRk8yMjgsMjI0XkNJMF5GRDEyIGF2ZW51ZSBkdSB3ZWJzZXJ2aWNlXkZTCl5BME4sMDMwLDAyNV5GTzIyOCwyNTReQ0kwXkZEWkEgd3NjbGllbnReRlMKXkEwTiwwNDUsMDM1XkZPMjI4LDI4NF5DSTBeRkRGUiA3NTAwMSBQQVJJUyAwMV5GUwpeQTBOLDA0NSwwMzVeRk8yMjgsMzM2XkNJMF5GRE0uIFRvdG8gLyAwNjExMTExMTExXkZTCl5BME4sMDI1LDAxOF5GTzAwMCwyODheQ0kwXkZEVU1eRlMKXkEwTiwwMjUsMDE4XkZPMDAwLDMyMF5DSTBeRkRXR0hUXkZTCl5BME4sMDI1LDAxOF5GTzAwMCwzNTJeQ0kwXkZEVk9MXkZTCl5BME4sMDM3LDAyNV5GTzA4MCwyODReQ0kwXkZEMS8xXkZTCl5BME4sMDM3LDAyNV5GTzA4MCwzMTZeQ0kwXkZEMS4yLzEuMl5GUwpeQTBOLDAzNywwMjVeRk8wODAsMzQ4XkNJMF5GRDAuNDUvMC40NV5GUwpeQTBOLDAyNSwwMTheRk8wMDAsMzg4XkNJMF5GRFJlZiBjbHQgOl5GUwpeQTBOLDAzMCwwMjVeRk8wOTAsMzg0XkNJMF5GRHJlZi0xXkZTCl5CWTNeRk80OSw3MzJeQkNOLDE4MCxOLE4sTixBXkZOMV5GUwpeQTBOLDI0LDI0XkZPMTM4LDkyMl5DSTBeRk4yXkZTCl5GTjFeRkRKVkdUUzAwMzAxNzAwMDA2OTU5NDleRlMKXkZOMl5GREpWR1RTMDAzMDE3MDAwMDY5NTk0OV5GUwpeQlkzXkZPMjgwLDQ3MF5CQ04sMTgwLE4sTixOLEFeRk4zXkZTCl5BME4sMjQsMjReRk80MjAsNjU1XkNJMF5GTjReRlMKXkZOM15GRDJMTTIyNzVeRlMKXkZONF5GRDJMTTIyNzVeRlMKXkEwTiwwMzUsMDM1XkZPNjQwLDk4MF5DSTBeRkReRlMKXkZPMDAwLDEwMDBeR0I4NDAsMDAwLDIsQiwwXkZTCl5GTzAwMCwxMDM3XkdCODQwLDAwMCwyLEIsMF5GUwpeQTBOLDAzMiwwMjheRk8wMDUsMTAwNl5DSTBeRkRTQU5URS9FWFRFTVAvUlYgV0VCXkZTCl5GWCAtLUZJTiBJTVBSRVNTSU9OIERPTk5FRVMtLSBeRlMKXlBRMSwwLDEsWQpeWFoK"
                },
                "docBordereau": null,
                "docRecapitulatif": null,
                "msgErreurEnregistrement": null,
                "msgErreurValidation": null,
                "msgErreurSuppression": null,
                "msgErreurEtiquette": null,
                "msgErreurBordereau": null,
                "msgErreurRecapitulatif": null
            }
        ]
    }
}
"""

CancelShipmentResponse = """{
  "ok": true,
  "codeErreur": null,
  "texteErreur": null,
  "contenu": {
    "msgErreur": null,
    "nbEnvoisATraiter": 1,
    "nbEnvoisEnregistres": 0,
    "nbEnvoisValides": 0,
    "nbEnvoisSupprimes": 1,
    "nbAnomaliesSuppression": 0,
    "nbAnomaliesEtiquette": 0,
    "nbAnomaliesBordereau": 0,
    "nbAnomaliesRecapitulatif": 0,
    "docBordereau": null,
    "docRecapitulatif": null,
    "msgErreurBordereau": null,
    "msgErreurRecapitulatif": null,
    "listRetoursEnvois": [
      {
        "index": 0,
        "horsSite": false,
        "codeSa": "020017",
        "codeClient": "601911",
        "codeProduit": "MES",
        "reference1": "ref-1",
        "reference2": "ref-2",
        "dateDepartEnlevement": "2020-06-09",
        "destinataire": {
          "nom": "M. DESTI",
          "adresse1": "12 avenue du webservice",
          "adresse2": "ZA wsclient",
          "codePostal": "75001",
          "ville": "PARIS 01",
          "codePays": "FR",
          "email": "w@z.fr",
          "telFixe": "0100000000",
          "indTelMobile": "33",
          "telMobile": "0611111111",
          "nomContact": "M. Toto",
          "codePorte": "1515",
          "codeTiers": "",
          "noEntrepositaireAgree": null,
          "particulier": false
        },
        "noRecepisse": "90000022",
        "noSuivi": "1G08Q6PK6PHP",
        "urlSuiviDestinataire": "https://edesti.com/1G08Q6PK6PHP",
        "docEtiquette": null,
        "docBordereau": null,
        "docRecapitulatif": null,
        "msgErreurEnregistrement": null,
        "msgErreurValidation": null,
        "msgErreurSuppression": null,
        "msgErreurEtiquette": null,
        "msgErreurBordereau": null,
        "msgErreurRecapitulatif": null
      }
    ]
  }
}
"""
