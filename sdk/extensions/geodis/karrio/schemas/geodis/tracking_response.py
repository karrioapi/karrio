from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ListDisponibilite:
    jour: Optional[str] = None
    heureMatinDebut: Optional[str] = None
    heureMatinFin: Optional[str] = None
    heureApresMidiDebut: Optional[str] = None
    heureApresMidiFin: Optional[str] = None
    observations: Optional[str] = None
    serviceReception: Optional[str] = None


@s(auto_attribs=True)
class Pays:
    code: Optional[str] = None
    libelle: Optional[str] = None
    indicatifTel: Optional[str] = None
    formatTel: Optional[str] = None
    formatCodePostal: Optional[str] = None
    preInfoDestinataire: Optional[bool] = None
    controleLocalite: Optional[bool] = None
    exportControl: Optional[bool] = None
    defaut: Optional[bool] = None
    listDepartementsExclus: List[str] = []


@s(auto_attribs=True)
class Destinataire:
    type: Optional[str] = None
    code: Optional[int] = None
    nom: Optional[str] = None
    codeTiers: Optional[str] = None
    indTelephoneFixe: Optional[str] = None
    telephoneFixe: Optional[str] = None
    indTelephoneMobile: Optional[str] = None
    telephoneMobile: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[str] = None
    noVoie: Optional[str] = None
    libelleVoie: Optional[str] = None
    adresse1: Optional[str] = None
    adresse2: Optional[str] = None
    codePostal: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[Pays] = JStruct[Pays]
    codePorte: Optional[str] = None
    latitude: Optional[int] = None
    longitude: Optional[int] = None
    instructionsLivraison: Optional[str] = None
    instructionsEnlevement: Optional[str] = None
    nomContact: Optional[str] = None
    telephoneContact: Optional[str] = None
    eaDestinataire: Optional[str] = None
    typePreinfo: Optional[str] = None
    typeDestinataire: Optional[str] = None
    adresseRetour: Optional[bool] = None
    marque: Optional[str] = None
    defaut: Optional[bool] = None
    restrictionAni: Optional[bool] = None
    codeRegion: Optional[str] = None
    urlPlan: Optional[str] = None
    listDisponibilites: List[ListDisponibilite] = JList[ListDisponibilite]


@s(auto_attribs=True)
class Devise:
    code: Optional[str] = None
    libelle: Optional[str] = None
    defaut: Optional[bool] = None
    typeMontant: Optional[str] = None
    montantMax: Optional[int] = None


@s(auto_attribs=True)
class IncotermConditionLivraison:
    code: Optional[str] = None
    libelle: Optional[str] = None
    defaut: Optional[bool] = None


@s(auto_attribs=True)
class GeoLOC:
    latitude: Optional[int] = None
    longitude: Optional[int] = None


@s(auto_attribs=True)
class InfoETA:
    libelle: Optional[str] = None
    geoLocDisponible: Optional[bool] = None
    geoLocCourante: Optional[GeoLOC] = JStruct[GeoLOC]
    geoLocArrivee: Optional[GeoLOC] = JStruct[GeoLOC]


@s(auto_attribs=True)
class ListEnvoisRegroupe:
    noRecepisse: Optional[str] = None
    reference1: Optional[str] = None
    poids: Optional[int] = None
    nbColis: Optional[int] = None
    nbPalettes: Optional[int] = None


@s(auto_attribs=True)
class ListFacturesDouane:
    noFacture: Optional[str] = None
    dateDepart: Optional[str] = None
    dateDepartFrs: Optional[str] = None
    montantFacture: Optional[int] = None
    deviseFacture: Optional[str] = None
    noSequence: Optional[int] = None


@s(auto_attribs=True)
class ListImagesBordereauxLivrElement:
    typeImage: Optional[str] = None
    urlAcces: Optional[str] = None
    dateSituationJustification: Optional[str] = None
    dateSituationJustificationFrs: Optional[str] = None
    nom: Optional[str] = None
    visibleDesti: Optional[bool] = None


@s(auto_attribs=True)
class ListPointage:
    datePointage: Optional[str] = None
    datePointageFrs: Optional[str] = None
    heurePointage: Optional[str] = None
    heurePointageFrs: Optional[str] = None
    lieu: Optional[str] = None
    referenceColis: Optional[str] = None
    noPointage: Optional[str] = None
    cabTransporteur: Optional[str] = None
    cabClient: Optional[str] = None


@s(auto_attribs=True)
class ListServices:
    code: Optional[str] = None
    libelle: Optional[str] = None
    statut: Optional[str] = None


@s(auto_attribs=True)
class CalendrierLivraison:
    jourDebut: Optional[str] = None
    jourDebutFrs: Optional[str] = None
    jourFin: Optional[str] = None
    jourFinFrs: Optional[str] = None
    listExceptions: List[str] = []
    listExceptionsFrs: List[str] = []
    heureLimite: Optional[str] = None
    heureLimiteFrs: Optional[str] = None
    express: Optional[bool] = None
    matinDisponible: Optional[bool] = None
    apresMidiDisponible: Optional[bool] = None
    jourLivrPrevu: Optional[str] = None
    creneauLivrPrevu: Optional[str] = None
    samediLivr: Optional[str] = None


@s(auto_attribs=True)
class InstructionClient:
    refUniExp: Optional[int] = None
    typeInstruction: Optional[str] = None
    tsSaisieInstr: Optional[str] = None
    tsSaisieInstrFrs: Optional[str] = None
    aliasSaisieInstr: Optional[str] = None
    codeMessage: Optional[str] = None
    codeProduit: Optional[str] = None
    centreTraitant: Optional[str] = None
    centreRelivraison: Optional[str] = None
    perimetreAgence: Optional[bool] = None
    calendrierLivraison: Optional[CalendrierLivraison] = JStruct[CalendrierLivraison]
    dateRetourOffice: Optional[str] = None
    adresseRelivraisonRetour: Optional[Destinataire] = JStruct[Destinataire]
    dateRelivraison: Optional[str] = None
    dateRelivraisonFrs: Optional[str] = None
    creneauRelivraison: Optional[str] = None
    annuleCrt: Optional[bool] = None
    annulePdu: Optional[bool] = None
    refClientRetour: Optional[str] = None
    listNomsPiecesJointes: List[str] = []
    uploadPjsEffectue: Optional[bool] = None
    searchText: Optional[str] = None


@s(auto_attribs=True)
class ParametrageInstruction:
    nouvelleLivraison: Optional[bool] = None
    adresseModifiable: Optional[str] = None
    porteCodee: Optional[bool] = None
    pieceJointe: Optional[str] = None
    crtAnnulable: Optional[bool] = None
    pduAnnulable: Optional[bool] = None
    retour: Optional[bool] = None
    facturation: Optional[bool] = None
    mention: Optional[str] = None
    listPaysLivraison: List[Pays] = JList[Pays]
    listPaysRetour: List[Pays] = JList[Pays]
    listDestinatairesLivraison: List[Destinataire] = JList[Destinataire]
    listExpediteursRetour: List[Destinataire] = JList[Destinataire]
    expediteurPrefere: Optional[Destinataire] = JStruct[Destinataire]


@s(auto_attribs=True)
class SuiviInstruction:
    typeInstruction: Optional[str] = None
    tsSaisieInstrFrs: Optional[str] = None
    aliasSaisieInstr: Optional[str] = None
    idSecuriseSaisieInstr: Optional[str] = None
    refClientRetour: Optional[str] = None
    adresseRelivraisonRetour: Optional[Destinataire] = JStruct[Destinataire]


@s(auto_attribs=True)
class ListEnvoisNotifications:
    tsEnvoi: Optional[str] = None
    dateEnvoi: Optional[str] = None
    dateEnvoiFrs: Optional[str] = None
    heureEnvoi: Optional[str] = None
    heureEnvoiFrs: Optional[str] = None
    typeEnvoi: Optional[str] = None
    typeNotif: Optional[str] = None
    statutEnvoi: Optional[str] = None
    emetteur: Optional[str] = None
    destinataire: Optional[str] = None
    sujet: Optional[str] = None
    contenu: Optional[str] = None
    typeDesti: Optional[str] = None


@s(auto_attribs=True)
class SuiviNotifications:
    nbEnvoisNotificationsOk: Optional[int] = None
    nbEnvoisNotificationsErr: Optional[int] = None
    listEnvoisNotificationsExpediteur: List[ListEnvoisNotifications] = JList[ListEnvoisNotifications]
    listEnvoisNotificationsDestinataire: List[ListEnvoisNotifications] = JList[ListEnvoisNotifications]


@s(auto_attribs=True)
class ListSuivi:
    dateSuivi: Optional[str] = None
    dateSuiviFrs: Optional[str] = None
    heureSuivi: Optional[str] = None
    heureSuiviFrs: Optional[str] = None
    codeSa: Optional[str] = None
    libelleCentre: Optional[str] = None
    libelleSuivi: Optional[str] = None
    libelleCourtSuivi: Optional[str] = None
    listInformationsComplementaires: List[str] = []
    suiviNotifications: Optional[SuiviNotifications] = JStruct[SuiviNotifications]
    codeSituationJustification: Optional[str] = None
    suiviInstruction: Optional[SuiviInstruction] = JStruct[SuiviInstruction]
    instructionADonner: Optional[bool] = None
    instructionDonnee: Optional[bool] = None
    dateRetour: Optional[str] = None
    dateRetourFrs: Optional[str] = None
    compteurRebours: Optional[int] = None
    uniteRebours: Optional[str] = None
    mentionAConfirmer: Optional[str] = None
    parametrageInstruction: Optional[ParametrageInstruction] = JStruct[ParametrageInstruction]
    instructionClient: Optional[InstructionClient] = JStruct[InstructionClient]


@s(auto_attribs=True)
class PrestationCommerciale:
    codeGroupeProduits: Optional[str] = None
    codeProduit: Optional[str] = None
    codeOption: Optional[str] = None
    type: Optional[str] = None
    libelle: Optional[str] = None
    europe: Optional[bool] = None
    vinsSpiritueux: Optional[bool] = None
    pointRelais: Optional[bool] = None
    bureauRestant: Optional[bool] = None
    rdvWeb: Optional[bool] = None
    rdvTel: Optional[bool] = None
    livEtage: Optional[bool] = None
    miseLieuUtil: Optional[bool] = None
    depotage: Optional[bool] = None


@s(auto_attribs=True)
class SuiviBilanCarbone:
    emissionDisponible: Optional[bool] = None
    emissionEqc: Optional[int] = None
    emissionEqa: Optional[int] = None
    emissionPar: Optional[int] = None


@s(auto_attribs=True)
class SuiviTemperature:
    seuilMin: Optional[int] = None
    seuilMax: Optional[int] = None
    isVert: Optional[bool] = None
    isRouge: Optional[bool] = None
    isMinRouge: Optional[bool] = None
    isMaxRouge: Optional[bool] = None
    dateDernierReleve: Optional[str] = None
    dateDernierReleveTempFrs: Optional[str] = None
    heureDernierReleve: Optional[str] = None
    heureDernierReleveTempFrs: Optional[str] = None
    minimale: Optional[int] = None
    maximale: Optional[int] = None
    moyenne: Optional[int] = None
    mediane: Optional[int] = None
    nbExcursions: Optional[int] = None
    suiviNotifications: Optional[SuiviNotifications] = JStruct[SuiviNotifications]
    listMesuresTemperature: List[IncotermConditionLivraison] = JList[IncotermConditionLivraison]


@s(auto_attribs=True)
class ListTimestep:
    position: Optional[int] = None
    libelle: Optional[str] = None
    libelle2: Optional[str] = None
    actif: Optional[bool] = None
    codeSituationJustification: Optional[str] = None
    isCreneauPassage: Optional[bool] = None


@s(auto_attribs=True)
class Timeline:
    positionCourante: Optional[int] = None
    listTimesteps: List[ListTimestep] = JList[ListTimestep]


@s(auto_attribs=True)
class UniteTaxation:
    code: Optional[str] = None
    libelle: Optional[str] = None


@s(auto_attribs=True)
class Contenu:
    refUniExp: Optional[int] = None
    refUniEnl: Optional[int] = None
    noSuivi: Optional[str] = None
    codeSa: Optional[str] = None
    codeClient: Optional[str] = None
    noRecepisse: Optional[str] = None
    dateDepart: Optional[str] = None
    dateDepartFrs: Optional[str] = None
    prestationCommerciale: Optional[PrestationCommerciale] = JStruct[PrestationCommerciale]
    expediteur: Optional[Destinataire] = JStruct[Destinataire]
    destinataire: Optional[Destinataire] = JStruct[Destinataire]
    reference1: Optional[str] = None
    reference2: Optional[str] = None
    reference3: Optional[str] = None
    refEdides: Optional[str] = None
    dateLivraisonSouhaitee: Optional[str] = None
    dateLivraisonSouhaiteeFrs: Optional[str] = None
    dateLivraisonPrevue: Optional[str] = None
    dateLivraisonPrevueFrs: Optional[str] = None
    creneauLivraisonPrevue: Optional[str] = None
    instructionsLivraison1: Optional[str] = None
    instructionsLivraison2: Optional[str] = None
    nbColis: Optional[int] = None
    nbPalettes: Optional[int] = None
    nbPalettesConsignees: Optional[int] = None
    poids: Optional[int] = None
    volume: Optional[int] = None
    qteUniteTaxation: Optional[int] = None
    uniteTaxation: Optional[UniteTaxation] = JStruct[UniteTaxation]
    valeurDeclaree: Optional[int] = None
    deviseValeurDeclaree: Optional[Devise] = JStruct[Devise]
    contreRemboursement: Optional[int] = None
    deviseContreRemboursement: Optional[Devise] = JStruct[Devise]
    portDu: Optional[int] = None
    devisePortDu: Optional[Devise] = JStruct[Devise]
    incotermConditionLivraison: Optional[IncotermConditionLivraison] = JStruct[IncotermConditionLivraison]
    natureMarchandises: Optional[str] = None
    sadLivEtage: Optional[bool] = None
    sadMiseLieuUtil: Optional[bool] = None
    sadDepotage: Optional[bool] = None
    listEnvoisRegroupes: List[ListEnvoisRegroupe] = JList[ListEnvoisRegroupe]
    listSuivis: List[ListSuivi] = JList[ListSuivi]
    timeline: Optional[Timeline] = JStruct[Timeline]
    listReferencesColis: List[str] = []
    listPointages: List[ListPointage] = JList[ListPointage]
    suiviBilanCarbone: Optional[SuiviBilanCarbone] = JStruct[SuiviBilanCarbone]
    suiviTemperature: Optional[SuiviTemperature] = JStruct[SuiviTemperature]
    listImagesPoc: List[ListImagesBordereauxLivrElement] = JList[ListImagesBordereauxLivrElement]
    listImagesRecepEmarge: List[ListImagesBordereauxLivrElement] = JList[ListImagesBordereauxLivrElement]
    listImagesBordereauxLivr: List[ListImagesBordereauxLivrElement] = JList[ListImagesBordereauxLivrElement]
    listImagesCopilote: List[ListImagesBordereauxLivrElement] = JList[ListImagesBordereauxLivrElement]
    listImagesMiseLieuSur: List[ListImagesBordereauxLivrElement] = JList[ListImagesBordereauxLivrElement]
    listImagesPreuveService: List[ListImagesBordereauxLivrElement] = JList[ListImagesBordereauxLivrElement]
    listPjsEnvoi: List[ListImagesBordereauxLivrElement] = JList[ListImagesBordereauxLivrElement]
    listServicesLivraison: List[ListServices] = JList[ListServices]
    listServicesAdditionnels: List[ListServices] = JList[ListServices]
    loginDestinataire: Optional[str] = None
    urlSuiviDestinataire: Optional[str] = None
    libelleDepart: Optional[str] = None
    libelleLivraison: Optional[str] = None
    infoETA: Optional[InfoETA] = JStruct[InfoETA]
    swapAller: Optional[bool] = None
    refUniExpSwapAller: Optional[int] = None
    noRecepisseSwapAller: Optional[str] = None
    noSuiviSwapAller: Optional[str] = None
    swapRetour: Optional[bool] = None
    refUniExpSwapRetour: Optional[int] = None
    noRecepisseSwapRetour: Optional[str] = None
    noSuiviSwapRetour: Optional[str] = None
    controleDouane: Optional[bool] = None
    listFacturesDouane: List[ListFacturesDouane] = JList[ListFacturesDouane]


@s(auto_attribs=True)
class TrackingResponse:
    ok: Optional[bool] = None
    codeErreur: Optional[str] = None
    texteErreur: Optional[str] = None
    contenu: Optional[Contenu] = JStruct[Contenu]
