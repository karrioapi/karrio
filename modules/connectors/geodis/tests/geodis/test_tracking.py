import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestGEODISTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.geodis.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/zoomclient/recherche-envoi",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.geodis.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.geodis.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["1GA6DUUZQZJM"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "geodis",
            "carrier_name": "geodis",
            "delivered": True,
            "estimated_delivery": "2020-01-20",
            "events": [
                {
                    "code": "SOL/REO",
                    "date": "2020-01-17",
                    "description": "SOL/REO",
                    "location": "020037",
                    "time": "14:23 PM",
                },
                {
                    "code": "RST/SOU",
                    "date": "2020-01-17",
                    "description": "RST/SOU",
                    "location": "020037",
                    "time": "14:23 PM",
                },
                {
                    "code": "AAR/CFM",
                    "date": "2020-01-17",
                    "description": "AAR/CFM",
                    "location": "020037",
                    "time": "14:22 PM",
                },
                {
                    "code": "COM/CFM",
                    "date": "2020-01-17",
                    "description": "COM/CFM",
                    "location": "020037",
                    "time": "14:21 PM",
                },
                {
                    "code": "EXP/CFM",
                    "date": "2020-01-17",
                    "description": "EXP/CFM",
                    "location": "Rochefort (FR)",
                    "time": "14:18 PM",
                },
                {
                    "code": "PCH/CFM",
                    "date": "2020-01-17",
                    "description": "PCH/CFM",
                    "location": "Rochefort (FR)",
                    "time": "14:16 PM",
                },
                {
                    "code": "COM/CFM",
                    "date": "2020-01-17",
                    "description": "COM/CFM",
                    "location": "Rochefort (FR)",
                    "time": "14:16 PM",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://edesti.com/1G6CPLT3JB5U",
                "customer_name": "Tryphon",
                "expected_delivery": "2020-01-20",
                "package_weight": 1.0,
                "shipment_destination_country": "FR",
                "shipment_destination_postal_code": "92000",
                "shipment_origin_country": "FR",
                "shipment_origin_postal_code": "17000",
                "shipment_package_count": 1,
                "shipment_service": "Express France (NTX)",
                "shipping_date": "2020-01-17",
            },
            "meta": {
                "codeClient": "601911",
                "noRecepisse": "92211740",
                "refEdides": "1234",
                "refUniExp": 3001710324,
                "reference1": "ma-ref-1",
                "reference2": "ma-ref-2",
            },
            "status": "delivered",
            "tracking_number": "1G6CPLT3JB5U",
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "geodis",
            "carrier_name": "geodis",
            "code": "error code",
            "details": {"tracking_number": "1GA6DUUZQZJM"},
            "message": "error message",
        }
    ],
]


TrackingRequest = [{"noSuivi": "1GA6DUUZQZJM"}]

TrackingResponse = """{
    "ok": true,
    "codeErreur": null,
    "texteErreur": null,
    "contenu": {
        "refUniExp": 3001710324,
        "refUniEnl": 0,
        "noSuivi": "1G6CPLT3JB5U",
        "codeSa": "020017",
        "codeClient": "601911",
        "noRecepisse": "92211740",
        "dateDepart": "2020-01-17",
        "dateDepartFrs": "17/01/2020",
        "prestationCommerciale": {
            "codeGroupeProduits": "FREXPEXP",
            "codeProduit": "NTX",
            "codeOption": "",
            "type": "EXP",
            "libelle": "Express France (NTX)",
            "typeService": null,
            "sansB2C": false,
            "europe": false,
            "vinsSpiritueux": null,
            "pointRelais": null,
            "bureauRestant": null,
            "rdvWeb": null,
            "rdvTel": null,
            "livEtage": null,
            "miseLieuUtil": null,
            "depotage": null,
            "defaut": null
        },
        "expediteur": {
            "type": "E",
            "code": 0,
            "nom": "TEST CLI",
            "codeTiers": null,
            "indTelephoneFixe": "33",
            "telephoneFixe": null,
            "indTelephoneMobile": "33",
            "telephoneMobile": null,
            "fax": null,
            "email": null,
            "noVoie": null,
            "libelleVoie": "1 RUE DE PARIS",
            "adresse1": "1 RUE DE PARIS",
            "adresse2": "BP5 - CEDEX 9",
            "codePostal": "17000",
            "ville": "LA ROCHELLE",
            "pays": {
                "code": "FR",
                "libelle": "FR",
                "indicatifTel": "33",
                "formatTel": "1111111111",
                "formatCodePostal": "11111",
                "preInfoDestinataire": true,
                "controleLocalite": false,
                "exportControl": false,
                "defaut": false,
                "listDepartementsExclus": [
                    "34",
                    "93"
                ]
            },
            "codePorte": null,
            "latitude": null,
            "longitude": null,
            "instructionsLivraison": null,
            "instructionsEnlevement": null,
            "nomContact": null,
            "telephoneContact": null,
            "eaDestinataire": null,
            "typePreinfo": null,
            "typeDestinataire": null,
            "adresseRetour": null,
            "marque": null,
            "defaut": null,
            "restrictionAni": null,
            "codeRegion": "17",
            "urlPlan": null,
            "agenceTeos": null,
            "listDisponibilites": null
        },
        "destinataire": {
            "type": "D",
            "code": 0,
            "nom": "Tryphon",
            "codeTiers": null,
            "indTelephoneFixe": "33",
            "telephoneFixe": null,
            "indTelephoneMobile": "33",
            "telephoneMobile": "0612345678",
            "fax": null,
            "email": null,
            "noVoie": null,
            "libelleVoie": "26, rue du Labrador",
            "adresse1": "26, rue du Labrador",
            "adresse2": "",
            "codePostal": "92000",
            "ville": "Bruxelles",
            "pays": {
                "code": "FR",
                "libelle": "FR",
                "indicatifTel": "33",
                "formatTel": "1111111111",
                "formatCodePostal": "11111",
                "preInfoDestinataire": true,
                "controleLocalite": false,
                "exportControl": false,
                "defaut": false,
                "listDepartementsExclus": [
                    "34",
                    "93"
                ]
            },
            "codePorte": null,
            "latitude": null,
            "longitude": null,
            "instructionsLivraison": null,
            "instructionsEnlevement": null,
            "nomContact": "TOTO",
            "telephoneContact": "0612345678",
            "eaDestinataire": null,
            "typePreinfo": null,
            "typeDestinataire": null,
            "adresseRetour": null,
            "marque": null,
            "defaut": null,
            "restrictionAni": null,
            "codeRegion": "92",
            "urlPlan": null,
            "agenceTeos": null,
            "listDisponibilites": null
        },
        "reference1": "ma-ref-1",
        "reference2": "ma-ref-2",
        "refEdides": "1234",
        "dateLivraisonSouhaitee": null,
        "dateLivraisonSouhaiteeFrs": "",
        "dateLivraisonPrevue": "2020-01-20",
        "dateLivraisonPrevueFrs": "20/01/2020",
        "creneauLivraisonPrevue": "MAT",
        "instructionsLivraison1": "",
        "instructionsLivraison2": "",
        "nbColis": 1,
        "nbPalettes": 0,
        "nbPalettesConsignees": 0,
        "poids": 1.0,
        "volume": 0.0,
        "qteUniteTaxation": null,
        "uniteTaxation": null,
        "valeurDeclaree": null,
        "deviseValeurDeclaree": null,
        "contreRemboursement": null,
        "deviseContreRemboursement": null,
        "portDu": null,
        "devisePortDu": null,
        "incotermConditionLivraison": {
            "code": "P",
            "libelle": "P",
            "defaut": null
        },
        "natureMarchandises": "",
        "sadLivEtage": false,
        "sadMiseLieuUtil": false,
        "sadDepotage": false,
        "sadSwso": false,
        "listEnvoisRegroupes": [],
        "listSuivis": [
            {
                "dateSuivi": "2020-01-17",
                "dateSuiviFrs": "17/01/2020",
                "heureSuivi": "14:23:22",
                "heureSuiviFrs": "14:23",
                "codeSa": "020037",
                "libelleCentre": "020037",
                "libelleSuivi": "SOL/REO",
                "libelleCourtSuivi": "SOL/REO",
                "listInformationsComplementaires": [],
                "suiviNotifications": null,
                "codeSituationJustification": "SOL/REO",
                "suiviInstruction": null,
                "instructionADonner": null,
                "instructionDonnee": null,
                "dateRetour": null,
                "dateRetourFrs": null,
                "compteurRebours": null,
                "uniteRebours": null,
                "mentionAConfirmer": null,
                "parametrageInstruction": null,
                "instructionClient": null
            },
            {
                "dateSuivi": "2020-01-17",
                "dateSuiviFrs": "17/01/2020",
                "heureSuivi": "14:23:02",
                "heureSuiviFrs": "14:23",
                "codeSa": "020037",
                "libelleCentre": "020037",
                "libelleSuivi": "RST/SOU",
                "libelleCourtSuivi": "RST/SOU",
                "listInformationsComplementaires": [],
                "suiviNotifications": null,
                "codeSituationJustification": "RST/SOU",
                "suiviInstruction": null,
                "instructionADonner": null,
                "instructionDonnee": null,
                "dateRetour": null,
                "dateRetourFrs": null,
                "compteurRebours": null,
                "uniteRebours": null,
                "mentionAConfirmer": null,
                "parametrageInstruction": null,
                "instructionClient": null
            },
            {
                "dateSuivi": "2020-01-17",
                "dateSuiviFrs": "17/01/2020",
                "heureSuivi": "14:22:17",
                "heureSuiviFrs": "14:22",
                "codeSa": "020037",
                "libelleCentre": "020037",
                "libelleSuivi": "AAR/CFM",
                "libelleCourtSuivi": "AAR/CFM",
                "listInformationsComplementaires": [],
                "suiviNotifications": null,
                "codeSituationJustification": "AAR/CFM",
                "suiviInstruction": null,
                "instructionADonner": null,
                "instructionDonnee": null,
                "dateRetour": null,
                "dateRetourFrs": null,
                "compteurRebours": null,
                "uniteRebours": null,
                "mentionAConfirmer": null,
                "parametrageInstruction": null,
                "instructionClient": null
            },
            {
                "dateSuivi": "2020-01-17",
                "dateSuiviFrs": "17/01/2020",
                "heureSuivi": "14:21:12",
                "heureSuiviFrs": "14:21",
                "codeSa": "020037",
                "libelleCentre": "020037",
                "libelleSuivi": "COM/CFM",
                "libelleCourtSuivi": "COM/CFM",
                "listInformationsComplementaires": [],
                "suiviNotifications": null,
                "codeSituationJustification": "COM/CFM",
                "suiviInstruction": null,
                "instructionADonner": null,
                "instructionDonnee": null,
                "dateRetour": null,
                "dateRetourFrs": null,
                "compteurRebours": null,
                "uniteRebours": null,
                "mentionAConfirmer": null,
                "parametrageInstruction": null,
                "instructionClient": null
            },
            {
                "dateSuivi": "2020-01-17",
                "dateSuiviFrs": "17/01/2020",
                "heureSuivi": "14:18:35",
                "heureSuiviFrs": "14:18",
                "codeSa": "020017",
                "libelleCentre": "Rochefort (FR)",
                "libelleSuivi": "EXP/CFM",
                "libelleCourtSuivi": "EXP/CFM",
                "listInformationsComplementaires": [],
                "suiviNotifications": null,
                "codeSituationJustification": "EXP/CFM",
                "suiviInstruction": null,
                "instructionADonner": null,
                "instructionDonnee": null,
                "dateRetour": null,
                "dateRetourFrs": null,
                "compteurRebours": null,
                "uniteRebours": null,
                "mentionAConfirmer": null,
                "parametrageInstruction": null,
                "instructionClient": null
            },
            {
                "dateSuivi": "2020-01-17",
                "dateSuiviFrs": "17/01/2020",
                "heureSuivi": "14:16:54",
                "heureSuiviFrs": "14:16",
                "codeSa": "020017",
                "libelleCentre": "Rochefort (FR)",
                "libelleSuivi": "PCH/CFM",
                "libelleCourtSuivi": "PCH/CFM",
                "listInformationsComplementaires": [],
                "suiviNotifications": null,
                "codeSituationJustification": "PCH/CFM",
                "suiviInstruction": null,
                "instructionADonner": null,
                "instructionDonnee": null,
                "dateRetour": null,
                "dateRetourFrs": null,
                "compteurRebours": null,
                "uniteRebours": null,
                "mentionAConfirmer": null,
                "parametrageInstruction": null,
                "instructionClient": null
            },
            {
                "dateSuivi": "2020-01-17",
                "dateSuiviFrs": "17/01/2020",
                "heureSuivi": "14:16:16",
                "heureSuiviFrs": "14:16",
                "codeSa": "020017",
                "libelleCentre": "Rochefort (FR)",
                "libelleSuivi": "COM/CFM",
                "libelleCourtSuivi": "COM/CFM",
                "listInformationsComplementaires": [],
                "suiviNotifications": null,
                "codeSituationJustification": "COM/CFM",
                "suiviInstruction": null,
                "instructionADonner": null,
                "instructionDonnee": null,
                "dateRetour": null,
                "dateRetourFrs": null,
                "compteurRebours": null,
                "uniteRebours": null,
                "mentionAConfirmer": null,
                "parametrageInstruction": null,
                "instructionClient": null
            }
        ],
        "timeline": {
            "positionCourante": 1,
            "listTimesteps": [
                {
                    "position": 1,
                    "libelle": "En attente de prise en charge",
                    "libelle2": null,
                    "actif": false,
                    "codeSituationJustification": null,
                    "isCreneauPassage": null
                },
                {
                    "position": 2,
                    "libelle": "En cours d'acheminement",
                    "libelle2": null,
                    "actif": false,
                    "codeSituationJustification": null,
                    "isCreneauPassage": null
                },
                {
                    "position": 3,
                    "libelle": "Mis en livraison",
                    "libelle2": null,
                    "actif": false,
                    "codeSituationJustification": null,
                    "isCreneauPassage": null
                },
                {
                    "position": 4,
                    "libelle": "Livré",
                    "libelle2": null,
                    "actif": false,
                    "codeSituationJustification": null,
                    "isCreneauPassage": null
                }
            ]
        },
        "listReferencesColis": [],
        "listPointages": [],
        "suiviBilanCarbone": {
            "emissionDisponible": false,
            "emissionEqc": null,
            "emissionEqa": null,
            "emissionPar": null
        },
        "suiviTemperature": null,
        "listImagesPoc": [],
        "listImagesRecepEmarge": [],
        "listImagesBordereauxLivr": [],
        "listImagesCopilote": [],
        "listImagesMiseLieuSur": [],
        "listImagesPreuveService": [],
        "listPjsEnvoi": [],
        "listServicesLivraison": [],
        "listServicesAdditionnels": [],
        "loginDestinataire": "02001792211740 / 92000",
        "urlSuiviDestinataire": "https://edesti.com/1G6CPLT3JB5U",
        "libelleDepart": "Départ le 17 janvier 2020",
        "libelleLivraison": "Livraison le 20 janvier 2020",
        "infoETA": null,
        "swapAller": false,
        "refUniExpSwapAller": 0,
        "noRecepisseSwapAller": "",
        "noSuiviSwapAller": "",
        "swapRetour": false,
        "refUniExpSwapRetour": 0,
        "noRecepisseSwapRetour": "",
        "noSuiviSwapRetour": "",
        "controleDouane": false,
        "listFacturesDouane": null
    }
}
"""

ErrorResponse = """{
  "ok": false,
  "codeErreur": "error code",
  "texteErreur": "error message"
}
"""
