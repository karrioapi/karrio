import attr
import jstruct
import typing


@attr.s(auto_attribs=True)
class DestinataireType:
    nom: typing.Optional[str] = None
    adresse1: typing.Optional[str] = None
    adresse2: typing.Optional[str] = None
    codePostal: typing.Optional[int] = None
    ville: typing.Optional[str] = None
    codePays: typing.Optional[str] = None
    email: typing.Optional[str] = None
    telFixe: typing.Optional[str] = None
    indTelMobile: typing.Optional[int] = None
    telMobile: typing.Optional[str] = None
    nomContact: typing.Optional[str] = None
    codePorte: typing.Optional[int] = None
    codeTiers: typing.Optional[str] = None
    noEntrepositaireAgree: typing.Any = None
    particulier: typing.Optional[bool] = None


@attr.s(auto_attribs=True)
class ListRetoursEnvoisType:
    index: typing.Optional[int] = None
    horsSite: typing.Optional[bool] = None
    codeSa: typing.Optional[str] = None
    codeClient: typing.Optional[int] = None
    codeProduit: typing.Optional[str] = None
    reference1: typing.Optional[str] = None
    reference2: typing.Optional[str] = None
    dateDepartEnlevement: typing.Optional[str] = None
    destinataire: typing.Optional[DestinataireType] = jstruct.JStruct[DestinataireType]
    noRecepisse: typing.Optional[int] = None
    noSuivi: typing.Optional[str] = None
    urlSuiviDestinataire: typing.Optional[str] = None
    docEtiquette: typing.Any = None
    docBordereau: typing.Any = None
    docRecapitulatif: typing.Any = None
    msgErreurEnregistrement: typing.Any = None
    msgErreurValidation: typing.Any = None
    msgErreurSuppression: typing.Any = None
    msgErreurEtiquette: typing.Any = None
    msgErreurBordereau: typing.Any = None
    msgErreurRecapitulatif: typing.Any = None


@attr.s(auto_attribs=True)
class ContenuType:
    msgErreur: typing.Any = None
    nbEnvoisATraiter: typing.Optional[int] = None
    nbEnvoisEnregistres: typing.Optional[int] = None
    nbEnvoisValides: typing.Optional[int] = None
    nbEnvoisSupprimes: typing.Optional[int] = None
    nbAnomaliesSuppression: typing.Optional[int] = None
    nbAnomaliesEtiquette: typing.Optional[int] = None
    nbAnomaliesBordereau: typing.Optional[int] = None
    nbAnomaliesRecapitulatif: typing.Optional[int] = None
    docBordereau: typing.Any = None
    docRecapitulatif: typing.Any = None
    msgErreurBordereau: typing.Any = None
    msgErreurRecapitulatif: typing.Any = None
    listRetoursEnvois: typing.Optional[typing.List[ListRetoursEnvoisType]] = jstruct.JList[ListRetoursEnvoisType]


@attr.s(auto_attribs=True)
class CancelResponseType:
    ok: typing.Optional[bool] = None
    codeErreur: typing.Any = None
    texteErreur: typing.Any = None
    contenu: typing.Optional[ContenuType] = jstruct.JStruct[ContenuType]
