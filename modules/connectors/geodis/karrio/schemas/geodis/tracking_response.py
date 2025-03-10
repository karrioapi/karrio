import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class PaysType:
    code: typing.Optional[str] = None
    libelle: typing.Optional[str] = None
    indicatifTel: typing.Optional[int] = None
    formatTel: typing.Optional[int] = None
    formatCodePostal: typing.Optional[int] = None
    preInfoDestinataire: typing.Optional[bool] = None
    controleLocalite: typing.Optional[bool] = None
    exportControl: typing.Optional[bool] = None
    defaut: typing.Optional[bool] = None
    listDepartementsExclus: typing.Optional[typing.List[int]] = None


@attr.s(auto_attribs=True)
class DestinataireType:
    type: typing.Optional[str] = None
    code: typing.Optional[int] = None
    nom: typing.Optional[str] = None
    codeTiers: typing.Optional[str] = None
    indTelephoneFixe: typing.Optional[int] = None
    telephoneFixe: typing.Optional[str] = None
    indTelephoneMobile: typing.Optional[int] = None
    telephoneMobile: typing.Optional[str] = None
    fax: typing.Optional[str] = None
    email: typing.Optional[str] = None
    noVoie: typing.Optional[str] = None
    libelleVoie: typing.Optional[str] = None
    adresse1: typing.Optional[str] = None
    adresse2: typing.Optional[str] = None
    codePostal: typing.Optional[int] = None
    ville: typing.Optional[str] = None
    pays: typing.Optional[PaysType] = jstruct.JStruct[PaysType]
    codePorte: typing.Optional[str] = None
    latitude: typing.Optional[str] = None
    longitude: typing.Optional[str] = None
    instructionsLivraison: typing.Optional[str] = None
    instructionsEnlevement: typing.Optional[str] = None
    nomContact: typing.Optional[str] = None
    telephoneContact: typing.Optional[str] = None
    eaDestinataire: typing.Optional[str] = None
    typePreinfo: typing.Optional[str] = None
    typeDestinataire: typing.Optional[str] = None
    adresseRetour: typing.Optional[str] = None
    marque: typing.Optional[str] = None
    defaut: typing.Optional[str] = None
    restrictionAni: typing.Optional[str] = None
    codeRegion: typing.Optional[int] = None
    urlPlan: typing.Optional[str] = None
    agenceTeos: typing.Optional[str] = None
    listDisponibilites: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class IncotermConditionLivraisonType:
    code: typing.Optional[str] = None
    libelle: typing.Optional[str] = None
    defaut: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ListSuiviType:
    dateSuivi: typing.Optional[str] = None
    dateSuiviFrs: typing.Optional[str] = None
    heureSuivi: typing.Optional[str] = None
    heureSuiviFrs: typing.Optional[str] = None
    codeSa: typing.Optional[str] = None
    libelleCentre: typing.Optional[str] = None
    libelleSuivi: typing.Optional[str] = None
    libelleCourtSuivi: typing.Optional[str] = None
    listInformationsComplementaires: typing.Optional[typing.List[str]] = None
    suiviNotifications: typing.Optional[str] = None
    codeSituationJustification: typing.Optional[str] = None
    suiviInstruction: typing.Optional[str] = None
    instructionADonner: typing.Optional[str] = None
    instructionDonnee: typing.Optional[str] = None
    dateRetour: typing.Optional[str] = None
    dateRetourFrs: typing.Optional[str] = None
    compteurRebours: typing.Optional[str] = None
    uniteRebours: typing.Optional[str] = None
    mentionAConfirmer: typing.Optional[str] = None
    parametrageInstruction: typing.Optional[str] = None
    instructionClient: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class PrestationCommercialeType:
    codeGroupeProduits: typing.Optional[str] = None
    codeProduit: typing.Optional[str] = None
    codeOption: typing.Optional[str] = None
    type: typing.Optional[str] = None
    libelle: typing.Optional[str] = None
    typeService: typing.Optional[str] = None
    sansB2C: typing.Optional[bool] = None
    europe: typing.Optional[bool] = None
    vinsSpiritueux: typing.Optional[str] = None
    pointRelais: typing.Optional[str] = None
    bureauRestant: typing.Optional[str] = None
    rdvWeb: typing.Optional[str] = None
    rdvTel: typing.Optional[str] = None
    livEtage: typing.Optional[str] = None
    miseLieuUtil: typing.Optional[str] = None
    depotage: typing.Optional[str] = None
    defaut: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class SuiviBilanCarboneType:
    emissionDisponible: typing.Optional[bool] = None
    emissionEqc: typing.Optional[str] = None
    emissionEqa: typing.Optional[str] = None
    emissionPar: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ListTimestepType:
    position: typing.Optional[int] = None
    libelle: typing.Optional[str] = None
    libelle2: typing.Optional[str] = None
    actif: typing.Optional[bool] = None
    codeSituationJustification: typing.Optional[str] = None
    isCreneauPassage: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TimelineType:
    positionCourante: typing.Optional[int] = None
    listTimesteps: typing.Optional[typing.List[ListTimestepType]] = jstruct.JList[ListTimestepType]


@attr.s(auto_attribs=True)
class ContenuType:
    refUniExp: typing.Optional[int] = None
    refUniEnl: typing.Optional[int] = None
    noSuivi: typing.Optional[str] = None
    codeSa: typing.Optional[str] = None
    codeClient: typing.Optional[int] = None
    noRecepisse: typing.Optional[int] = None
    dateDepart: typing.Optional[str] = None
    dateDepartFrs: typing.Optional[str] = None
    prestationCommerciale: typing.Optional[PrestationCommercialeType] = jstruct.JStruct[PrestationCommercialeType]
    expediteur: typing.Optional[DestinataireType] = jstruct.JStruct[DestinataireType]
    destinataire: typing.Optional[DestinataireType] = jstruct.JStruct[DestinataireType]
    reference1: typing.Optional[str] = None
    reference2: typing.Optional[str] = None
    refEdides: typing.Optional[int] = None
    dateLivraisonSouhaitee: typing.Optional[str] = None
    dateLivraisonSouhaiteeFrs: typing.Optional[str] = None
    dateLivraisonPrevue: typing.Optional[str] = None
    dateLivraisonPrevueFrs: typing.Optional[str] = None
    creneauLivraisonPrevue: typing.Optional[str] = None
    instructionsLivraison1: typing.Optional[str] = None
    instructionsLivraison2: typing.Optional[str] = None
    nbColis: typing.Optional[int] = None
    nbPalettes: typing.Optional[int] = None
    nbPalettesConsignees: typing.Optional[int] = None
    poids: typing.Optional[float] = None
    volume: typing.Optional[float] = None
    qteUniteTaxation: typing.Optional[str] = None
    uniteTaxation: typing.Optional[str] = None
    valeurDeclaree: typing.Optional[str] = None
    deviseValeurDeclaree: typing.Optional[str] = None
    contreRemboursement: typing.Optional[str] = None
    deviseContreRemboursement: typing.Optional[str] = None
    portDu: typing.Optional[str] = None
    devisePortDu: typing.Optional[str] = None
    incotermConditionLivraison: typing.Optional[IncotermConditionLivraisonType] = jstruct.JStruct[IncotermConditionLivraisonType]
    natureMarchandises: typing.Optional[str] = None
    sadLivEtage: typing.Optional[bool] = None
    sadMiseLieuUtil: typing.Optional[bool] = None
    sadDepotage: typing.Optional[bool] = None
    sadSwso: typing.Optional[bool] = None
    listEnvoisRegroupes: typing.Optional[typing.List[str]] = None
    listSuivis: typing.Optional[typing.List[ListSuiviType]] = jstruct.JList[ListSuiviType]
    timeline: typing.Optional[TimelineType] = jstruct.JStruct[TimelineType]
    listReferencesColis: typing.Optional[typing.List[str]] = None
    listPointages: typing.Optional[typing.List[str]] = None
    suiviBilanCarbone: typing.Optional[SuiviBilanCarboneType] = jstruct.JStruct[SuiviBilanCarboneType]
    suiviTemperature: typing.Optional[str] = None
    listImagesPoc: typing.Optional[typing.List[str]] = None
    listImagesRecepEmarge: typing.Optional[typing.List[str]] = None
    listImagesBordereauxLivr: typing.Optional[typing.List[str]] = None
    listImagesCopilote: typing.Optional[typing.List[str]] = None
    listImagesMiseLieuSur: typing.Optional[typing.List[str]] = None
    listImagesPreuveService: typing.Optional[typing.List[str]] = None
    listPjsEnvoi: typing.Optional[typing.List[str]] = None
    listServicesLivraison: typing.Optional[typing.List[str]] = None
    listServicesAdditionnels: typing.Optional[typing.List[str]] = None
    loginDestinataire: typing.Optional[str] = None
    urlSuiviDestinataire: typing.Optional[str] = None
    libelleDepart: typing.Optional[str] = None
    libelleLivraison: typing.Optional[str] = None
    infoETA: typing.Optional[str] = None
    swapAller: typing.Optional[bool] = None
    refUniExpSwapAller: typing.Optional[int] = None
    noRecepisseSwapAller: typing.Optional[str] = None
    noSuiviSwapAller: typing.Optional[str] = None
    swapRetour: typing.Optional[bool] = None
    refUniExpSwapRetour: typing.Optional[int] = None
    noRecepisseSwapRetour: typing.Optional[str] = None
    noSuiviSwapRetour: typing.Optional[str] = None
    controleDouane: typing.Optional[bool] = None
    listFacturesDouane: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class TrackingResponseType:
    ok: typing.Optional[bool] = None
    codeErreur: typing.Optional[str] = None
    texteErreur: typing.Optional[str] = None
    contenu: typing.Optional[ContenuType] = jstruct.JStruct[ContenuType]
