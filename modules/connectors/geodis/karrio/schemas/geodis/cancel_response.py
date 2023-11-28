from attr import s
from typing import Optional, Any, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class DestinataireType:
    nom: Optional[str] = None
    adresse1: Optional[str] = None
    adresse2: Optional[str] = None
    codePostal: Optional[int] = None
    ville: Optional[str] = None
    codePays: Optional[str] = None
    email: Optional[str] = None
    telFixe: Optional[str] = None
    indTelMobile: Optional[int] = None
    telMobile: Optional[str] = None
    nomContact: Optional[str] = None
    codePorte: Optional[int] = None
    codeTiers: Optional[str] = None
    noEntrepositaireAgree: Any = None
    particulier: Optional[bool] = None


@s(auto_attribs=True)
class ListRetoursEnvoisType:
    index: Optional[int] = None
    horsSite: Optional[bool] = None
    codeSa: Optional[str] = None
    codeClient: Optional[int] = None
    codeProduit: Optional[str] = None
    reference1: Optional[str] = None
    reference2: Optional[str] = None
    dateDepartEnlevement: Optional[str] = None
    destinataire: Optional[DestinataireType] = JStruct[DestinataireType]
    noRecepisse: Optional[int] = None
    noSuivi: Optional[str] = None
    urlSuiviDestinataire: Optional[str] = None
    docEtiquette: Any = None
    docBordereau: Any = None
    docRecapitulatif: Any = None
    msgErreurEnregistrement: Any = None
    msgErreurValidation: Any = None
    msgErreurSuppression: Any = None
    msgErreurEtiquette: Any = None
    msgErreurBordereau: Any = None
    msgErreurRecapitulatif: Any = None


@s(auto_attribs=True)
class ContenuType:
    msgErreur: Any = None
    nbEnvoisATraiter: Optional[int] = None
    nbEnvoisEnregistres: Optional[int] = None
    nbEnvoisValides: Optional[int] = None
    nbEnvoisSupprimes: Optional[int] = None
    nbAnomaliesSuppression: Optional[int] = None
    nbAnomaliesEtiquette: Optional[int] = None
    nbAnomaliesBordereau: Optional[int] = None
    nbAnomaliesRecapitulatif: Optional[int] = None
    docBordereau: Any = None
    docRecapitulatif: Any = None
    msgErreurBordereau: Any = None
    msgErreurRecapitulatif: Any = None
    listRetoursEnvois: List[ListRetoursEnvoisType] = JList[ListRetoursEnvoisType]


@s(auto_attribs=True)
class CancelResponseType:
    ok: Optional[bool] = None
    codeErreur: Any = None
    texteErreur: Any = None
    contenu: Optional[ContenuType] = JStruct[ContenuType]
