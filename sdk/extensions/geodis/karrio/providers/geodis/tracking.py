import geodis_lib.tracking_response as geodis
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.geodis.error as error
import karrio.providers.geodis.utils as provider_utils
import karrio.providers.geodis.units as provider_units


def parse_tracking_response(
    responses: typing.List[typing.Tuple[str, dict]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    messages: typing.List[models.Message] = sum(
        [
            error.parse_error_response(res, settings, tracking_number=number)
            for number, res in responses
            if res.get("ok") == False
        ],
        start=[],
    )
    tracking_details = [
        _extract_details(res["contenu"], settings)
        for _, res in responses
        if res.get("ok") == True
    ]

    return tracking_details, messages


def _extract_details(
    data: typing.Dict[str, typing.Any],
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    envoi = lib.to_object(geodis.Contenu, data)
    status = None
    delivered = None
    estimated_delivery = None

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=envoi.noSuivi,
        status=status,
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.dateSuivi, "%Y-%m-%d"),
                description=event.libelleSuivi,
                code=event.codeSituationJustification,
                time=lib.ftime(event.heureSuivi, "%H:%M:%S"),
                location=event.libelleCentre,
            )
            for event in envoi.listSuivis
        ],
        estimated_delivery=estimated_delivery,
        delivered=delivered,
        info=models.TrackingInfo(
            carrier_tracking_link=envoi.urlSuiviDestinataire,
            shipment_package_count=envoi.nbColis,
            package_weight=envoi.poids,
            shipment_service=lib.failsafe(
                lambda _: envoi.prestationCommerciale.libelle
            ),
            shipment_origin_country=lib.failsafe(lambda _: envoi.expediteur.pays.code),
            shipment_origin_postal_code=lib.failsafe(
                lambda _: envoi.expediteur.codePostal
            ),
            shipment_destination_country=lib.failsafe(
                lambda _: envoi.destinataire.pays.code
            ),
            shipment_destination_postal_code=lib.failsafe(
                lambda _: envoi.destinataire.codePostal
            ),
            customer_name=lib.failsafe(lambda _: envoi.destinataire.nom),
            shipping_date=lib.fdate(envoi.dateDepart, "%Y-%m-%d"),
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    request = [
        dict(
            noSuivi=number,
            refUniExp=(
                (payload.options.get(number) or {}).get("reference")
                or payload.reference
            ),
        )
        for number in payload.tracking_numbers
    ]

    return lib.Serializable(request, lib.to_dict)
