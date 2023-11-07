from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class ContreRemboursementType:
    quantite: Optional[float] = None
    codeUnite: Optional[str] = None


@s(auto_attribs=True)
class DestinataireType:
    nom: Optional[str] = None
    adresse1: Optional[str] = None
    adresse2: Optional[str] = None
    codePostal: Optional[int] = None
    ville: Optional[str] = None
    codePays: Optional[str] = None
    nomContact: Optional[str] = None
    email: Optional[str] = None
    telFixe: Optional[str] = None
    indTelMobile: Optional[int] = None
    telMobile: Optional[str] = None
    codePorte: Optional[int] = None
    codeTiers: Optional[str] = None
    noEntrepositaireAgree: Optional[str] = None
    particulier: Optional[bool] = None


@s(auto_attribs=True)
class PieceJointeType:
    nom: Optional[str] = None
    type: Optional[str] = None
    contenu: Optional[str] = None


@s(auto_attribs=True)
class ListFactureType:
    noFacture: Optional[str] = None
    montantFacture: Optional[ContreRemboursementType] = JStruct[ContreRemboursementType]
    dateFacture: Optional[str] = None
    pieceJointe: Optional[PieceJointeType] = JStruct[PieceJointeType]


@s(auto_attribs=True)
class InformationDouaneType:
    poidsNetTotal: Optional[float] = None
    eoriExpediteur: Optional[str] = None
    eoriDestinataire: Optional[str] = None
    emailExpediteurDouane: Optional[str] = None
    indTelExpediteurDouane: Optional[str] = None
    telExpediteurDouane: Optional[str] = None
    mandatRepresentation: Optional[bool] = None
    listFactures: List[ListFactureType] = JList[ListFactureType]


@s(auto_attribs=True)
class ListDocumentsEnvoiType:
    visibiliteDestinataire: Optional[bool] = None
    pieceJointe: Optional[PieceJointeType] = JStruct[PieceJointeType]


@s(auto_attribs=True)
class ListMatieresDangereusType:
    noONU: Optional[str] = None
    groupeEmballage: Optional[str] = None
    classeADR: Optional[str] = None
    codeTypeEmballage: Optional[str] = None
    nbEmballages: Optional[int] = None
    nomTechnique: Optional[str] = None
    codeQuantite: Optional[str] = None
    poidsVolume: Optional[float] = None
    dangerEnv: Optional[bool] = None


@s(auto_attribs=True)
class ListUmgType:
    palette: Optional[bool] = None
    paletteConsignee: Optional[bool] = None
    quantite: Optional[int] = None
    poids: Optional[float] = None
    volume: Optional[float] = None
    longueurUnitaire: Optional[float] = None
    largeurUnitaire: Optional[float] = None
    hauteurUnitaire: Optional[float] = None
    referenceColis: Optional[str] = None


@s(auto_attribs=True)
class ListVinsSpiritueuxType:
    regimeFiscal: Optional[str] = None
    nbCols: Optional[int] = None
    contenance: Optional[float] = None
    volumeEnDroits: Optional[float] = None
    noTitreMvtRefAdmin: Optional[str] = None
    dureeTransport: Optional[float] = None


@s(auto_attribs=True)
class ListEnvoisType:
    noRecepisse: Optional[str] = None
    noSuivi: Optional[str] = None
    horsSite: Optional[bool] = None
    codeSa: Optional[str] = None
    codeClient: Optional[int] = None
    codeProduit: Optional[str] = None
    reference1: Optional[str] = None
    reference2: Optional[str] = None
    expediteur: Optional[DestinataireType] = JStruct[DestinataireType]
    dateDepartEnlevement: Optional[str] = None
    instructionEnlevement: Optional[str] = None
    destinataire: Optional[DestinataireType] = JStruct[DestinataireType]
    listUmgs: List[ListUmgType] = JList[ListUmgType]
    natureEnvoi: Optional[str] = None
    poidsTotal: Optional[float] = None
    volumeTotal: Optional[float] = None
    largerTotal: Optional[float] = None
    hauteurTotal: Optional[float] = None
    longueurTotal: Optional[float] = None
    uniteTaxation: Optional[ContreRemboursementType] = JStruct[ContreRemboursementType]
    animauxPlumes: Optional[bool] = None
    optionLivraison: Optional[str] = None
    codeSaBureauRestant: Optional[str] = None
    idPointRelais: Optional[str] = None
    dateLivraison: Optional[str] = None
    heureLivraison: Optional[str] = None
    instructionLivraison: Optional[str] = None
    natureMarchandise: Optional[str] = None
    valeurDeclaree: Optional[ContreRemboursementType] = JStruct[ContreRemboursementType]
    contreRemboursement: Optional[ContreRemboursementType] = JStruct[ContreRemboursementType]
    codeIncotermConditionLivraison: Optional[str] = None
    typeTva: Optional[str] = None
    sadLivToph: Optional[bool] = None
    sadSwap: Optional[bool] = None
    sadLivEtage: Optional[bool] = None
    sadMiseLieuUtil: Optional[bool] = None
    sadDepotage: Optional[bool] = None
    etage: Optional[int] = None
    emailNotificationDestinataire: Optional[str] = None
    smsNotificationDestinataire: Optional[str] = None
    emailNotificationExpediteur: Optional[str] = None
    emailConfirmationEnlevement: Optional[str] = None
    emailPriseEnChargeEnlevement: Optional[str] = None
    poidsQteLimiteeMD: Optional[float] = None
    dangerEnvQteLimiteeMD: Optional[bool] = None
    nbColisQteExcepteeMD: Optional[int] = None
    dangerEnvQteExcepteeMD: Optional[bool] = None
    listMatieresDangereuses: List[ListMatieresDangereusType] = JList[ListMatieresDangereusType]
    listVinsSpiritueux: List[ListVinsSpiritueuxType] = JList[ListVinsSpiritueuxType]
    nosUmsAEtiqueter: Optional[str] = None
    listDocumentsEnvoi: List[ListDocumentsEnvoiType] = JList[ListDocumentsEnvoiType]
    informationDouane: Optional[InformationDouaneType] = JStruct[InformationDouaneType]


@s(auto_attribs=True)
class ShippingRequestType:
    modificationParReference1: Optional[bool] = None
    impressionEtiquette: Optional[bool] = None
    typeImpressionEtiquette: Optional[str] = None
    formatEtiquette: Optional[str] = None
    validationEnvoi: Optional[bool] = None
    suppressionSiEchecValidation: Optional[bool] = None
    impressionBordereau: Optional[bool] = None
    impressionRecapitulatif: Optional[bool] = None
    listEnvois: List[ListEnvoisType] = JList[ListEnvoisType]
