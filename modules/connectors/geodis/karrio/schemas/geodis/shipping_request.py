import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class ContreRemboursementType:
    quantite: typing.Optional[float] = None
    codeUnite: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class DestinataireType:
    nom: typing.Optional[str] = None
    adresse1: typing.Optional[str] = None
    adresse2: typing.Optional[str] = None
    codePostal: typing.Optional[int] = None
    ville: typing.Optional[str] = None
    codePays: typing.Optional[str] = None
    nomContact: typing.Optional[str] = None
    email: typing.Optional[str] = None
    telFixe: typing.Optional[str] = None
    indTelMobile: typing.Optional[int] = None
    telMobile: typing.Optional[str] = None
    codePorte: typing.Optional[int] = None
    codeTiers: typing.Optional[str] = None
    noEntrepositaireAgree: typing.Optional[str] = None
    particulier: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class PieceJointeType:
    nom: typing.Optional[str] = None
    type: typing.Optional[str] = None
    contenu: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ListFactureType:
    noFacture: typing.Optional[str] = None
    montantFacture: typing.Optional[ContreRemboursementType] = jstruct.JStruct[ContreRemboursementType]
    dateFacture: typing.Optional[str] = None
    pieceJointe: typing.Optional[PieceJointeType] = jstruct.JStruct[PieceJointeType]


@attr.s(auto_attribs=True)
class InformationDouaneType:
    poidsNetTotal: typing.Optional[float] = None
    eoriExpediteur: typing.Optional[str] = None
    eoriDestinataire: typing.Optional[str] = None
    emailExpediteurDouane: typing.Optional[str] = None
    indTelExpediteurDouane: typing.Optional[str] = None
    telExpediteurDouane: typing.Optional[str] = None
    mandatRepresentation: typing.Optional[bool] = None
    listFactures: typing.Optional[typing.List[ListFactureType]] = jstruct.JList[ListFactureType]


@attr.s(auto_attribs=True)
class ListDocumentsEnvoiType:
    visibiliteDestinataire: typing.Optional[bool] = None
    pieceJointe: typing.Optional[PieceJointeType] = jstruct.JStruct[PieceJointeType]


@attr.s(auto_attribs=True)
class ListMatieresDangereusType:
    noONU: typing.Optional[str] = None
    groupeEmballage: typing.Optional[str] = None
    classeADR: typing.Optional[str] = None
    codeTypeEmballage: typing.Optional[str] = None
    nbEmballages: typing.Optional[int] = None
    nomTechnique: typing.Optional[str] = None
    codeQuantite: typing.Optional[str] = None
    poidsVolume: typing.Optional[float] = None
    dangerEnv: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class ListUmgType:
    palette: typing.Optional[bool] = None
    paletteConsignee: typing.Optional[bool] = None
    quantite: typing.Optional[int] = None
    poids: typing.Optional[float] = None
    volume: typing.Optional[float] = None
    longueurUnitaire: typing.Optional[float] = None
    largeurUnitaire: typing.Optional[float] = None
    hauteurUnitaire: typing.Optional[float] = None
    referenceColis: typing.Optional[str] = None


@attr.s(auto_attribs=True)
class ListVinsSpiritueuxType:
    regimeFiscal: typing.Optional[str] = None
    nbCols: typing.Optional[int] = None
    contenance: typing.Optional[float] = None
    volumeEnDroits: typing.Optional[float] = None
    noTitreMvtRefAdmin: typing.Optional[str] = None
    dureeTransport: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class ListEnvoisType:
    noRecepisse: typing.Optional[str] = None
    noSuivi: typing.Optional[str] = None
    horsSite: typing.Optional[bool] = None
    codeSa: typing.Optional[str] = None
    codeClient: typing.Optional[int] = None
    codeProduit: typing.Optional[str] = None
    reference1: typing.Optional[str] = None
    reference2: typing.Optional[str] = None
    expediteur: typing.Optional[DestinataireType] = jstruct.JStruct[DestinataireType]
    dateDepartEnlevement: typing.Optional[str] = None
    instructionEnlevement: typing.Optional[str] = None
    destinataire: typing.Optional[DestinataireType] = jstruct.JStruct[DestinataireType]
    listUmgs: typing.Optional[typing.List[ListUmgType]] = jstruct.JList[ListUmgType]
    natureEnvoi: typing.Optional[str] = None
    poidsTotal: typing.Optional[float] = None
    volumeTotal: typing.Optional[float] = None
    largerTotal: typing.Optional[float] = None
    hauteurTotal: typing.Optional[float] = None
    longueurTotal: typing.Optional[float] = None
    uniteTaxation: typing.Optional[ContreRemboursementType] = jstruct.JStruct[ContreRemboursementType]
    animauxPlumes: typing.Optional[bool] = None
    optionLivraison: typing.Optional[str] = None
    codeSaBureauRestant: typing.Optional[str] = None
    idPointRelais: typing.Optional[str] = None
    dateLivraison: typing.Optional[str] = None
    heureLivraison: typing.Optional[str] = None
    instructionLivraison: typing.Optional[str] = None
    natureMarchandise: typing.Optional[str] = None
    valeurDeclaree: typing.Optional[ContreRemboursementType] = jstruct.JStruct[ContreRemboursementType]
    contreRemboursement: typing.Optional[ContreRemboursementType] = jstruct.JStruct[ContreRemboursementType]
    codeIncotermConditionLivraison: typing.Optional[str] = None
    typeTva: typing.Optional[str] = None
    sadLivToph: typing.Optional[bool] = None
    sadSwap: typing.Optional[bool] = None
    sadLivEtage: typing.Optional[bool] = None
    sadMiseLieuUtil: typing.Optional[bool] = None
    sadDepotage: typing.Optional[bool] = None
    etage: typing.Optional[int] = None
    emailNotificationDestinataire: typing.Optional[str] = None
    smsNotificationDestinataire: typing.Optional[str] = None
    emailNotificationExpediteur: typing.Optional[str] = None
    emailConfirmationEnlevement: typing.Optional[str] = None
    emailPriseEnChargeEnlevement: typing.Optional[str] = None
    poidsQteLimiteeMD: typing.Optional[float] = None
    dangerEnvQteLimiteeMD: typing.Optional[bool] = None
    nbColisQteExcepteeMD: typing.Optional[int] = None
    dangerEnvQteExcepteeMD: typing.Optional[bool] = None
    listMatieresDangereuses: typing.Optional[typing.List[ListMatieresDangereusType]] = jstruct.JList[ListMatieresDangereusType]
    listVinsSpiritueux: typing.Optional[typing.List[ListVinsSpiritueuxType]] = jstruct.JList[ListVinsSpiritueuxType]
    nosUmsAEtiqueter: typing.Optional[str] = None
    listDocumentsEnvoi: typing.Optional[typing.List[ListDocumentsEnvoiType]] = jstruct.JList[ListDocumentsEnvoiType]
    informationDouane: typing.Optional[InformationDouaneType] = jstruct.JStruct[InformationDouaneType]


@attr.s(auto_attribs=True)
class ShippingRequestType:
    modificationParReference1: typing.Optional[bool] = None
    impressionEtiquette: typing.Optional[bool] = None
    typeImpressionEtiquette: typing.Optional[str] = None
    formatEtiquette: typing.Optional[str] = None
    validationEnvoi: typing.Optional[bool] = None
    suppressionSiEchecValidation: typing.Optional[bool] = None
    impressionBordereau: typing.Optional[bool] = None
    impressionRecapitulatif: typing.Optional[bool] = None
    listEnvois: typing.Optional[typing.List[ListEnvoisType]] = jstruct.JList[ListEnvoisType]
