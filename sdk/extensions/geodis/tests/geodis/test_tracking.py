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
            "events": [
                {
                    "code": "SOL/REO",
                    "date": "2019-10-08",
                    "description": "Retour d'office",
                    "location": "Tours (FR)",
                    "time": "16:45",
                },
                {
                    "code": "RST/CAD",
                    "date": "2019-10-08",
                    "description": "Les informations communiquées dans votre contrat de transport ne permettent pas d'organiser la livraison. Des informations complémentaires nous sont nécessaires pour livrer (nom, rue, téléphone, ...).",
                    "location": "Tours (FR)",
                    "time": "16:40",
                },
                {
                    "code": "AAR/CFM",
                    "date": "2019-10-08",
                    "description": "Prise en Charge ou Arrivage Conforme",
                    "location": "Tours (FR)",
                    "time": "16:26",
                },
                {
                    "code": "EXP/CFM",
                    "date": "2019-10-08",
                    "description": "Expédié",
                    "location": "Reims (FR)",
                    "time": "16:20",
                },
                {
                    "code": "ECH/CFM",
                    "date": "2019-10-08",
                    "description": "Enlèvement réalisé",
                    "location": "Reims (FR)",
                    "time": "16:00",
                },
                {
                    "code": "EML/CFM",
                    "date": "2019-10-08",
                    "description": "Enlèvement prévu ce jour",
                    "location": "Reims (FR)",
                    "time": "15:37",
                },
                {
                    "code": "EPC/CFM",
                    "date": "2019-10-08",
                    "description": "Enlevement prevu",
                    "location": "Rochefort (FR)",
                    "time": "15:08",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://edesti.com/1GA6DUUZQZJM",
                "package_weight": 33,
                "shipment_package_count": 1,
                "shipping_date": "2019-10-08",
            },
            "tracking_number": "1GA6DUUZQZJM",
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
    "refUniExp": 1322117298,
    "refUniEnl": 1322117297,
    "noSuivi": "1GA6DUUZQZJM",
    "codeSa": "020017",
    "codeClient": "000002",
    "noRecepisse": "12971461",
    "dateDepart": "2019-10-08",
    "dateDepartFrs": "08/10/2019",
    "prestationCommerciale": {
      "codeGroupeProduits": "CALBEMES",
      "codeProduit": "ENL",
      "codeOption": "",
      "type": "MES",
      "libelle": "Retour/Trans. Fr. MessageriePlus (ENL)",
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
      "nom": "LA BOITE A PILE",
      "codeTiers": null,
      "indTelephoneFixe": "33",
      "telephoneFixe": null,
      "indTelephoneMobile": "33",
      "telephoneMobile": null,
      "fax": null,
      "email": null,
      "noVoie": null,
      "libelleVoie": "23 RUE MONSEIGNEUR BEJOT",
      "adresse1": "23 RUE MONSEIGNEUR BEJOT",
      "adresse2": null,
      "codePostal": "51100",
      "ville": "REIMS",
      "pays": {
        "code": "FR",
        "libelle": "France",
        "indicatifTel": "33",
        "formatTel": "1111111111",
        "formatCodePostal": "11111",
        "preInfoDestinataire": true,
        "controleLocalite": true,
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
      "codeRegion": "51",
      "urlPlan": null,
      "listDisponibilites": null
    },
    "destinataire": {
      "type": "D",
      "code": 0,
      "nom": "TNR REOUR CAS 1",
      "codeTiers": null,
      "indTelephoneFixe": "33",
      "telephoneFixe": null,
      "indTelephoneMobile": "33",
      "telephoneMobile": null,
      "fax": null,
      "email": null,
      "noVoie": null,
      "libelleVoie": "RUE TEST",
      "adresse1": "RUE TEST",
      "adresse2": null,
      "codePostal": "37000",
      "ville": "TOURS",
      "pays": {
        "code": "FR",
        "libelle": "France",
        "indicatifTel": "33",
        "formatTel": "1111111111",
        "formatCodePostal": "11111",
        "preInfoDestinataire": true,
        "controleLocalite": true,
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
      "codeRegion": "37",
      "urlPlan": null,
      "listDisponibilites": null
    },
    "reference1": "",
    "reference2": "",
    "refEdides": "",
    "dateLivraisonSouhaitee": null,
    "dateLivraisonSouhaiteeFrs": "",
    "dateLivraisonPrevue": null,
    "dateLivraisonPrevueFrs": "",
    "creneauLivraisonPrevue": null,
    "instructionsLivraison1": "",
    "instructionsLivraison2": "",
    "nbColis": 1,
    "nbPalettes": 0,
    "nbPalettesConsignees": 0,
    "poids": 33,
    "volume": 0,
    "qteUniteTaxation": null,
    "uniteTaxation": null,
    "valeurDeclaree": null,
    "deviseValeurDeclaree": null,
    "contreRemboursement": null,
    "deviseContreRemboursement": null,
    "portDu": null,
    "devisePortDu": null,
    "incotermConditionLivraison": null,
    "natureMarchandises": null,
    "sadLivEtage": false,
    "sadMiseLieuUtil": false,
    "sadDepotage": false,
    "listEnvoisRegroupes": [],
    "listSuivis": [
      {
        "dateSuivi": "2019-10-08",
        "dateSuiviFrs": "08/10/2019",
        "heureSuivi": "16:45:25",
        "heureSuiviFrs": "16:45",
        "codeSa": "020037",
        "libelleCentre": "Tours (FR)",
        "libelleSuivi": "Retour d'office",
        "libelleCourtSuivi": "Retour d'office",
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
        "dateSuivi": "2019-10-08",
        "dateSuiviFrs": "08/10/2019",
        "heureSuivi": "16:40:49",
        "heureSuiviFrs": "16:40",
        "codeSa": "020037",
        "libelleCentre": "Tours (FR)",
        "libelleSuivi": "Les informations communiquées dans votre contrat de transport ne permettent pas d'organiser la livraison. Des informations complémentaires nous sont nécessaires pour livrer (nom, rue, téléphone, ...).",
        "libelleCourtSuivi": "Complément d'Adresse",
        "listInformationsComplementaires": [],
        "suiviNotifications": null,
        "codeSituationJustification": "RST/CAD",
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
        "dateSuivi": "2019-10-08",
        "dateSuiviFrs": "08/10/2019",
        "heureSuivi": "16:26:00",
        "heureSuiviFrs": "16:26",
        "codeSa": "020037",
        "libelleCentre": "Tours (FR)",
        "libelleSuivi": "Prise en Charge ou Arrivage Conforme",
        "libelleCourtSuivi": "Prise en Charge ou Arrivage Conforme",
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
        "dateSuivi": "2019-10-08",
        "dateSuiviFrs": "08/10/2019",
        "heureSuivi": "16:20:11",
        "heureSuiviFrs": "16:20",
        "codeSa": "005051",
        "libelleCentre": "Reims (FR)",
        "libelleSuivi": "Expédié",
        "libelleCourtSuivi": "Expédié",
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
        "dateSuivi": "2019-10-08",
        "dateSuiviFrs": "08/10/2019",
        "heureSuivi": "16:00:00",
        "heureSuiviFrs": "16:00",
        "codeSa": "005051",
        "libelleCentre": "Reims (FR)",
        "libelleSuivi": "Enlèvement réalisé",
        "libelleCourtSuivi": null,
        "listInformationsComplementaires": [],
        "suiviNotifications": null,
        "codeSituationJustification": "ECH/CFM",
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
        "dateSuivi": "2019-10-08",
        "dateSuiviFrs": "08/10/2019",
        "heureSuivi": "15:37:58",
        "heureSuiviFrs": "15:37",
        "codeSa": "005051",
        "libelleCentre": "Reims (FR)",
        "libelleSuivi": "Enlèvement prévu ce jour",
        "libelleCourtSuivi": null,
        "listInformationsComplementaires": [],
        "suiviNotifications": null,
        "codeSituationJustification": "EML/CFM",
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
        "dateSuivi": "2019-10-08",
        "dateSuiviFrs": "08/10/2019",
        "heureSuivi": "15:08:09",
        "heureSuiviFrs": "15:08",
        "codeSa": "020017",
        "libelleCentre": "Rochefort (FR)",
        "libelleSuivi": "Enlevement prevu",
        "libelleCourtSuivi": null,
        "listInformationsComplementaires": [],
        "suiviNotifications": null,
        "codeSituationJustification": "EPC/CFM",
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
      "positionCourante": 4,
      "listTimesteps": [
        {
          "position": 1,
          "libelle": "Prise en charge",
          "libelle2": null,
          "actif": false,
          "codeSituationJustification": "ECH/CFM",
          "isCreneauPassage": null
        },
        {
          "position": 2,
          "libelle": "En cours d'acheminement",
          "libelle2": null,
          "actif": false,
          "codeSituationJustification": "AAR/CFM",
          "isCreneauPassage": null
        },
        {
          "position": 3,
          "libelle": "En attente de vos instructions",
          "libelle2": null,
          "actif": false,
          "codeSituationJustification": "RST/CAD",
          "isCreneauPassage": null
        },
        {
          "position": 4,
          "libelle": "Retour à l'expéditeur",
          "libelle2": null,
          "actif": true,
          "codeSituationJustification": "SOL/REO",
          "isCreneauPassage": null
        }
      ]
    },
    "listReferencesColis": [],
    "listPointages": [
      {
        "datePointage": "2019-10-08",
        "datePointageFrs": "08/10/2019",
        "heurePointage": "16:26:00",
        "heurePointageFrs": "16:26",
        "lieu": "Tours (FR)",
        "referenceColis": "",
        "noPointage": "000001",
        "cabTransporteur": "JVGTS0010170386551727",
        "cabClient": null
      },
      {
        "datePointage": "2019-10-08",
        "datePointageFrs": "08/10/2019",
        "heurePointage": "16:18:33",
        "heurePointageFrs": "16:18",
        "lieu": "Reims (FR)",
        "referenceColis": "",
        "noPointage": "000001",
        "cabTransporteur": "JVGTS0010170386551727",
        "cabClient": null
      },
      {
        "datePointage": "2019-10-08",
        "datePointageFrs": "08/10/2019",
        "heurePointage": "16:11:35",
        "heurePointageFrs": "16:11",
        "lieu": "Reims (FR)",
        "referenceColis": "",
        "noPointage": "000001",
        "cabTransporteur": "JVGTS0010170386551727",
        "cabClient": null
      },
      {
        "datePointage": "2019-10-08",
        "datePointageFrs": "08/10/2019",
        "heurePointage": "16:00:17",
        "heurePointageFrs": "16:00",
        "lieu": "Reims (FR)",
        "referenceColis": "",
        "noPointage": "000001",
        "cabTransporteur": "JVGTS0010170386551727",
        "cabClient": null
      }
    ],
    "suiviBilanCarbone": null,
    "suiviTemperature": null,
    "listImagesPoc": [],
    "listImagesRecepEmarge": [],
    "listImagesBordereauxLivr": [],
    "listImagesCopilote": [],
    "listImagesMiseLieuSur": [],
    "listImagesPreuveService": [],
    "listServicesLivraison": [],
    "listServicesAdditionnels": [],
    "loginDestinataire": "00505112971461 / 37000",
    "urlSuiviDestinataire": "https://edesti.com/1GA6DUUZQZJM",
    "libelleDepart": "Départ le 8 octobre 2019",
    "libelleLivraison": "Livraison selon le délai de transport contractuel",
    "infoETA": null
  }
}
"""

ErrorResponse = """{
  "ok": false,
  "codeErreur": "error code",
  "texteErreur": "error message"
}
"""
