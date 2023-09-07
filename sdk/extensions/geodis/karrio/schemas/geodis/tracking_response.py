from attr import s
from typing import Optional, List, Any
from jstruct import JStruct, JList


@s(auto_attribs=True)
class PaysType:
    code: Optional[str] = None
    libelle: Optional[str] = None
    indicatifTel: Optional[int] = None
    formatTel: Optional[int] = None
    formatCodePostal: Optional[int] = None
    preInfoDestinataire: Optional[bool] = None
    controleLocalite: Optional[bool] = None
    exportControl: Optional[bool] = None
    defaut: Optional[bool] = None
    listDepartementsExclus: List[int] = []


@s(auto_attribs=True)
class DestinataireType:
    type: Optional[str] = None
    code: Optional[int] = None
    nom: Optional[str] = None
    codeTiers: Optional[str] = None
    indTelephoneFixe: Optional[int] = None
    telephoneFixe: Optional[str] = None
    indTelephoneMobile: Optional[int] = None
    telephoneMobile: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[str] = None
    noVoie: Optional[str] = None
    libelleVoie: Optional[str] = None
    adresse1: Optional[str] = None
    adresse2: Optional[str] = None
    codePostal: Optional[int] = None
    ville: Optional[str] = None
    pays: Optional[PaysType] = JStruct[PaysType]
    codePorte: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    instructionsLivraison: Optional[str] = None
    instructionsEnlevement: Optional[str] = None
    nomContact: Optional[str] = None
    telephoneContact: Optional[str] = None
    eaDestinataire: Optional[str] = None
    typePreinfo: Optional[str] = None
    typeDestinataire: Optional[str] = None
    adresseRetour: Optional[str] = None
    marque: Optional[str] = None
    defaut: Optional[str] = None
    restrictionAni: Optional[str] = None
    codeRegion: Optional[int] = None
    urlPlan: Optional[str] = None
    listDisponibilites: Optional[str] = None


@s(auto_attribs=True)
class ListEnvoisRegroupeType:
    noRecepisse: Optional[str] = None
    reference1: Optional[str] = None
    poids: Optional[float] = None
    nbColis: Optional[int] = None
    nbPalettes: Optional[int] = None


@s(auto_attribs=True)
class ListPointageType:
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
class ListSuiviType:
    dateSuivi: Optional[str] = None
    dateSuiviFrs: Optional[str] = None
    heureSuivi: Optional[str] = None
    heureSuiviFrs: Optional[str] = None
    codeSa: Optional[str] = None
    libelleCentre: Optional[str] = None
    libelleSuivi: Optional[str] = None
    libelleCourtSuivi: Optional[str] = None
    listInformationsComplementaires: List[str] = []
    suiviNotifications: Optional[str] = None
    codeSituationJustification: Optional[str] = None
    suiviInstruction: Optional[str] = None
    instructionADonner: Optional[str] = None
    instructionDonnee: Optional[str] = None
    dateRetour: Optional[str] = None
    dateRetourFrs: Optional[str] = None
    compteurRebours: Optional[str] = None
    uniteRebours: Optional[str] = None
    mentionAConfirmer: Optional[str] = None
    parametrageInstruction: Optional[str] = None
    instructionClient: Optional[str] = None


@s(auto_attribs=True)
class PrestationCommercialeType:
    codeGroupeProduits: Optional[str] = None
    codeProduit: Optional[str] = None
    codeOption: Optional[str] = None
    type: Optional[str] = None
    libelle: Optional[str] = None
    europe: Optional[bool] = None
    vinsSpiritueux: Optional[str] = None
    pointRelais: Optional[str] = None
    bureauRestant: Optional[str] = None
    rdvWeb: Optional[str] = None
    rdvTel: Optional[str] = None
    livEtage: Optional[str] = None
    miseLieuUtil: Optional[str] = None
    depotage: Optional[str] = None
    defaut: Optional[str] = None


@s(auto_attribs=True)
class ListTimestepType:
    position: Optional[int] = None
    libelle: Optional[str] = None
    libelle2: Optional[str] = None
    actif: Optional[bool] = None
    codeSituationJustification: Optional[str] = None
    isCreneauPassage: Optional[str] = None


@s(auto_attribs=True)
class TimelineType:
    positionCourante: Optional[int] = None
    listTimesteps: List[ListTimestepType] = JList[ListTimestepType]


@s(auto_attribs=True)
class ContenuType:
    refUniExp: Optional[int] = None
    refUniEnl: Optional[int] = None
    noSuivi: Optional[str] = None
    codeSa: Optional[str] = None
    codeClient: Optional[str] = None
    noRecepisse: Optional[int] = None
    dateDepart: Optional[str] = None
    dateDepartFrs: Optional[str] = None
    prestationCommerciale: Optional[PrestationCommercialeType] = JStruct[PrestationCommercialeType]
    expediteur: Optional[DestinataireType] = JStruct[DestinataireType]
    destinataire: Optional[DestinataireType] = JStruct[DestinataireType]
    reference1: Optional[str] = None
    reference2: Optional[str] = None
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
    qteUniteTaxation: Optional[str] = None
    uniteTaxation: Optional[str] = None
    valeurDeclaree: Optional[str] = None
    deviseValeurDeclaree: Optional[str] = None
    contreRemboursement: Optional[str] = None
    deviseContreRemboursement: Optional[str] = None
    portDu: Optional[str] = None
    devisePortDu: Optional[str] = None
    incotermConditionLivraison: Optional[str] = None
    natureMarchandises: Optional[str] = None
    sadLivEtage: Optional[bool] = None
    sadMiseLieuUtil: Optional[bool] = None
    sadDepotage: Optional[bool] = None
    listEnvoisRegroupes: List[ListEnvoisRegroupeType] = JList[ListEnvoisRegroupeType]
    listSuivis: List[ListSuiviType] = JList[ListSuiviType]
    timeline: Optional[TimelineType] = JStruct[TimelineType]
    listReferencesColis: List[Any] = []
    listPointages: List[ListPointageType] = JList[ListPointageType]
    suiviBilanCarbone: Optional[str] = None
    suiviTemperature: Optional[str] = None
    listImagesPoc: List[Any] = []
    listImagesRecepEmarge: List[Any] = []
    listImagesBordereauxLivr: List[Any] = []
    listImagesCopilote: List[Any] = []
    listImagesMiseLieuSur: List[Any] = []
    listImagesPreuveService: List[Any] = []
    listServicesLivraison: List[Any] = []
    listServicesAdditionnels: List[Any] = []
    loginDestinataire: Optional[str] = None
    urlSuiviDestinataire: Optional[str] = None
    libelleDepart: Optional[str] = None
    libelleLivraison: Optional[str] = None
    infoETA: Optional[str] = None


@s(auto_attribs=True)
class TrackingResponseType:
    ok: Optional[bool] = None
    codeErreur: Optional[str] = None
    texteErreur: Optional[str] = None
    contenu: Optional[ContenuType] = JStruct[ContenuType]
