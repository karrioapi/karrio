from attr import s
from typing import Optional, List
from jstruct import JStruct, JList


@s(auto_attribs=True)
class DestinataireType:
    codePays: Optional[str] = None
    codePostal: Optional[int] = None
    ville: Optional[str] = None


@s(auto_attribs=True)
class ListeUmgType:
    codeUmg: Optional[str] = None
    numeroColis: Optional[int] = None
    cabTransporteur: Optional[str] = None
    cabEuropeTransporteur: Optional[str] = None
    referenceColisClient: Optional[str] = None


@s(auto_attribs=True)
class ContenuType:
    fluxEtiquettes: Optional[str] = None
    destinataire: Optional[DestinataireType] = JStruct[DestinataireType]
    reseau: Optional[str] = None
    priorite: Optional[int] = None
    codire: Optional[str] = None
    cabRouting: Optional[str] = None
    listeUmg: List[ListeUmgType] = JList[ListeUmgType]
    direction: Optional[str] = None


@s(auto_attribs=True)
class LabelResponseType:
    ok: Optional[bool] = None
    codeErreur: Optional[str] = None
    texteErreur: Optional[str] = None
    contenu: Optional[ContenuType] = JStruct[ContenuType]
