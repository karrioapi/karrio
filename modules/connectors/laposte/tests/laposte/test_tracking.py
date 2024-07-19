import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestLaPosteTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.laposte.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/idships/EW112720413FR?lang=fr_FR",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.laposte.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.laposte.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["EW112720413FR"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "laposte",
            "carrier_name": "laposte",
            "delivered": True,
            "estimated_delivery": "2023-03-09",
            "events": [
                {
                    "code": "DI1",
                    "date": "2023-03-09",
                    "description": "Votre colis est livré.",
                    "time": "09:38 AM",
                },
                {
                    "code": "MD2",
                    "date": "2023-03-09",
                    "description": "Votre colis est dans le site de livraison qui dessert votre adresse. Nous le préparons pour le mettre en livraison.",
                    "time": "09:01 AM",
                },
                {
                    "code": "ET1",
                    "date": "2023-03-08",
                    "description": "Votre colis est en cours d'acheminement.",
                    "time": "16:25 PM",
                },
                {
                    "code": "ET3",
                    "date": "2023-02-22",
                    "description": "Votre colis est arrivé dans le pays du destinataire.",
                    "time": "16:23 PM",
                },
                {
                    "code": "ET2",
                    "date": "2023-02-18",
                    "description": "Votre colis est prêt à partir de son territoire d’expédition. Il va être remis au transporteur pour son acheminement.",
                    "time": "12:27 PM",
                },
                {
                    "code": "ET1",
                    "date": "2023-02-18",
                    "description": "Votre colis est en transit sur nos plateformes logistiques.",
                    "time": "07:34 AM",
                },
                {
                    "code": "ET1",
                    "date": "2023-02-17",
                    "description": "Votre colis est en transit sur nos plateformes logistiques.",
                    "time": "23:13 PM",
                },
                {
                    "code": "PC1",
                    "date": "2023-02-17",
                    "description": "Votre colis a été déposé dans un point postal.",
                    "time": "14:43 PM",
                },
                {
                    "code": "DR1",
                    "date": "2023-02-17",
                    "description": "Votre Colissimo va bientôt nous être confié ! Il est en cours de préparation chez votre expéditeur.",
                    "time": "14:41 PM",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://www.laposte.fr/outils/suivre-vos-envois?code=EW112720413FR",
                "expected_delivery": "2023-03-09",
                "shipment_destination_country": "BR",
                "shipment_origin_country": "FR",
                "shipment_service": "colissimo",
                "shipping_date": "2023-02-17",
            },
            "status": "delivered",
            "tracking_number": "EW112720413FR",
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "laposte",
            "carrier_name": "laposte",
            "code": 400,
            "details": {},
            "message": "Le numéro que vous avez saisi n’est pas valide. Nous vous invitons à vérifier votre saisie, en particulier le nombre de caractères.",
        }
    ],
]


TrackingRequest = ["EW112720413FR"]

TrackingResponse = """[
    {
      "lang": "fr_FR",
      "scope": "open",
      "returnCode": 200,
      "shipment": {
        "idShip": "EW112720413FR",
        "holder": 4,
        "product": "colissimo",
        "isFinal": true,
        "deliveryDate": "2023-03-09T09:38:00+01:00",
        "entryDate": "2023-02-17T14:43:00+01:00",
        "timeline": [
          {
            "shortLabel": "Votre colis est entre nos mains.",
            "longLabel": "",
            "id": 1,
            "country": "FR",
            "status": true,
            "type": 1
          },
          {
            "shortLabel": "Il est en chemin.",
            "longLabel": "",
            "id": 2,
            "country": "BR",
            "status": true,
            "type": 1
          },
          {
            "shortLabel": "Votre colis est arrivé sur son site de livraison.",
            "longLabel": "",
            "id": 3,
            "country": "",
            "status": true,
            "type": 1
          },
          {
            "shortLabel": "Nous préparons votre colis pour sa livraison.",
            "longLabel": "",
            "id": 4,
            "country": "BR",
            "status": true,
            "type": 1
          },
          {
            "shortLabel": "Votre colis a été livré",
            "longLabel": "",
            "id": 5,
            "date": "2023-03-09T09:38:00+01:00",
            "country": "BR",
            "status": true,
            "type": 1
          }
        ],
        "event": [
          {
            "code": "DI1",
            "label": "Votre colis est livré.",
            "date": "2023-03-09T09:38:00+01:00"
          },
          {
            "code": "MD2",
            "label": "Votre colis est dans le site de livraison qui dessert votre adresse. Nous le préparons pour le mettre en livraison.",
            "date": "2023-03-09T09:01:00+01:00"
          },
          {
            "code": "ET1",
            "label": "Votre colis est en cours d'acheminement.",
            "date": "2023-03-08T16:25:00+01:00"
          },
          {
            "code": "ET3",
            "label": "Votre colis est arrivé dans le pays du destinataire.",
            "date": "2023-02-22T16:23:00+01:00"
          },
          {
            "code": "ET2",
            "label": "Votre colis est prêt à partir de son territoire d’expédition. Il va être remis au transporteur pour son acheminement.",
            "date": "2023-02-18T12:27:00+01:00"
          },
          {
            "code": "ET1",
            "label": "Votre colis est en transit sur nos plateformes logistiques.",
            "date": "2023-02-18T07:34:12+01:00"
          },
          {
            "code": "ET1",
            "label": "Votre colis est en transit sur nos plateformes logistiques.",
            "date": "2023-02-17T23:13:12+01:00"
          },
          {
            "code": "PC1",
            "label": "Votre colis a été déposé dans un point postal.",
            "date": "2023-02-17T14:43:00+01:00"
          },
          {
            "code": "DR1",
            "label": "Votre Colissimo va bientôt nous être confié ! Il est en cours de préparation chez votre expéditeur.",
            "date": "2023-02-17T14:41:00+01:00"
          }
        ],
        "contextData": {
          "deliveryChoice": {
            "deliveryChoice": 0
          },
          "originCountry": "FR",
          "arrivalCountry": "BR"
        },
        "estimDate": "2023-03-09T09:38:00+01:00",
        "url": "https://www.laposte.fr/outils/suivre-vos-envois?code=EW112720413FR"
      }
    }
]
"""

ErrorResponse = """{
  "returnCode": 400,
  "returnMessage": "Le numéro que vous avez saisi n’est pas valide. Nous vous invitons à vérifier votre saisie, en particulier le nombre de caractères.",
  "lang": "fr_FR",
  "scope": "open",
  "idShip": "WBZQ03ENZJ6BBBTEELZWITJTAGYKA19WR6OOJ6MIVZARY3OVPSX4A495YOMXBLKC"
}
"""
