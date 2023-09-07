from attr import s
from typing import Optional, List
from jstruct import JList, JStruct


@s(auto_attribs=True)
class DestinataireType:
    code: Optional[str] = None
    nom: Optional[str] = None
    adresse1: Optional[str] = None
    adresse2: Optional[str] = None
    codePays: Optional[str] = None
    codePostal: Optional[int] = None
    ville: Optional[str] = None
    nomContact: Optional[str] = None
    telephoneContact: Optional[str] = None


@s(auto_attribs=True)
class ExpediteurType:
    nom: Optional[str] = None
    codePays: Optional[str] = None
    codeRegion: Optional[int] = None
    codePostal: Optional[int] = None
    ville: Optional[str] = None
    telephoneContact: Optional[str] = None


@s(auto_attribs=True)
class ListeArticleType:
    code: Optional[str] = None
    reference: Optional[str] = None
    quantite: Optional[int] = None


@s(auto_attribs=True)
class ListeUmgType:
    codeUmg: Optional[str] = None
    poids: Optional[int] = None
    volume: Optional[float] = None
    numeroColis: Optional[int] = None
    cabTransporteur: Optional[str] = None
    cabEuropeTransporteur: Optional[str] = None
    referenceColisClient: Optional[str] = None
    listeArticle: List[ListeArticleType] = JList[ListeArticleType]


@s(auto_attribs=True)
class LabelRequestType:
    codeSaAgenceDepart: Optional[str] = None
    codeTeosAgenceDepart: Optional[str] = None
    codeClient: Optional[str] = None
    formatImpression: Optional[str] = None
    positionPremiereEtiquette: Optional[int] = None
    codeLangue: Optional[str] = None
    codeProduit: Optional[str] = None
    noRecepisse: Optional[int] = None
    dateDepart: Optional[str] = None
    dateLivraison: Optional[str] = None
    expediteur: Optional[ExpediteurType] = JStruct[ExpediteurType]
    destinataire: Optional[DestinataireType] = JStruct[DestinataireType]
    nombreTotalUM: Optional[int] = None
    nombreTotalPalettes: Optional[int] = None
    poidsTotal: Optional[int] = None
    volumeTotal: Optional[float] = None
    listeUmg: List[ListeUmgType] = JList[ListeUmgType]
    codeOptionLivraison: Optional[str] = None
    reference1: Optional[str] = None
