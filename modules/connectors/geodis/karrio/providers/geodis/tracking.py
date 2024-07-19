import karrio.schemas.geodis.tracking_request as geodis
import karrio.schemas.geodis.tracking_response as tracking
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.geodis.error as error
import karrio.providers.geodis.utils as provider_utils
import karrio.providers.geodis.units as provider_units


def parse_tracking_response(
    _responses: lib.Deserializable[typing.List[typing.Tuple[str, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _responses.deserialize()

    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(response, settings, tracking_number=_)
            for _, response in responses
        ],
        start=[],
    )
    tracking_details = [
        _extract_details(details, settings)
        for _, details in responses
        if details.get("ok") is True
    ]

    return tracking_details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    contenu = lib.to_object(tracking.TrackingResponseType, data).contenu
    delivered = any(contenu.libelleLivraison or "")
    status = (
        units.TrackingStatus.delivered.name
        if delivered
        else units.TrackingStatus.in_transit.name
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=contenu.noSuivi,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.dateSuivi),
                description=event.libelleSuivi,
                code=event.codeSituationJustification,
                time=lib.flocaltime(event.heureSuivi),
                location=event.libelleCentre,
            )
            for event in contenu.listSuivis
        ],
        estimated_delivery=lib.fdate(contenu.dateLivraisonPrevue),
        status=status,
        delivered=delivered,
        info=models.TrackingInfo(
            carrier_tracking_link=contenu.urlSuiviDestinataire,
            shipment_service=contenu.prestationCommerciale.libelle,
            expected_delivery=lib.fdate(contenu.dateLivraisonPrevue),
            shipment_package_count=contenu.nbColis,
            package_weight=contenu.poids,
            customer_name=contenu.destinataire.nom,
            shipment_origin_country=contenu.expediteur.pays.libelle,
            shipment_origin_postal_code=contenu.expediteur.codePostal,
            shipment_destination_country=contenu.destinataire.pays.libelle,
            shipment_destination_postal_code=contenu.destinataire.codePostal,
            shipping_date=lib.fdate(contenu.dateDepart),
        ),
        meta=dict(
            reference1=contenu.reference1,
            reference2=contenu.reference2,
            refEdides=contenu.refEdides,
            refUniExp=contenu.refUniExp,
            codeClient=contenu.codeClient,
            noRecepisse=contenu.noRecepisse,
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = [
        geodis.TrackingRequestType(noSuivi=tracking_number)
        for tracking_number in payload.tracking_numbers
    ]

    return lib.Serializable(request, lib.to_dict)
