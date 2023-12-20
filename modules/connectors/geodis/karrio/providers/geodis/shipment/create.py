import karrio.schemas.geodis.shipping_request as geodis
import karrio.schemas.geodis.shipping_response as shipping
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.geodis.error as error
import karrio.providers.geodis.utils as provider_utils
import karrio.providers.geodis.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = (
        error.parse_error_response(response, settings)
        if response.get("ok") is False
        else []
    )
    shipment = (
        _extract_details(response, settings, _response.ctx)
        if response.get("ok")
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict,
) -> models.ShipmentDetails:
    shipment = lib.to_object(
        shipping.ShippingResponseType, data
    ).contenu.listRetoursEnvois[0]
    label = shipment.docEtiquette.contenu

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.noSuivi,
        shipment_identifier=shipment.noSuivi,
        label_type=ctx.get("label_type", "PDF"),
        docs=models.Documents(label=label),
        meta=dict(
            carrier_tracking_link=shipment.urlSuiviDestinataire,
            noRecepisse=shipment.noRecepisse,
            codeProduit=shipment.codeProduit,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    customs = lib.to_customs_info(payload.customs)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        option_type=provider_units.ShippingOption,
    )
    label_type = provider_units.LabelType.map(payload.label_type or "PDF")

    request = geodis.ShippingRequestType(
        modificationParReference1=None,
        impressionEtiquette=True,
        typeImpressionEtiquette=label_type.value or "P",
        formatEtiquette="1",
        validationEnvoi=options.geodis_validate_envoi.state,
        suppressionSiEchecValidation=True,
        impressionBordereau=False,
        impressionRecapitulatif=True,
        listEnvois=[
            geodis.ListEnvoisType(
                noRecepisse=options.geodis_no_recepisse.state,
                noSuivi=None,
                horsSite=None,
                codeSa=settings.connection_config.agency_code.state,
                codeClient=settings.code_client,
                codeProduit=service,
                reference1=payload.reference,
                reference2=None,
                expediteur=geodis.DestinataireType(
                    nom=shipper.company_name or shipper.person_name,
                    adresse1=shipper.address_line1,
                    adresse2=shipper.address_line2,
                    codePostal=shipper.postal_code,
                    ville=shipper.city,
                    codePays=shipper.country_code,
                    nomContact=shipper.person_name,
                    email=shipper.email,
                    telFixe=shipper.phone_number,
                    indTelMobile=None,
                    telMobile=None,
                    codePorte=shipper.suite,
                    codeTiers=None,
                    noEntrepositaireAgree=None,
                    particulier=shipper.residential,
                ),
                dateDepartEnlevement=lib.fdate(options.shipment_date.state),
                instructionEnlevement=options.geodis_instruction_enlevement.state,
                destinataire=geodis.DestinataireType(
                    nom=recipient.company_name or recipient.person_name,
                    adresse1=recipient.address_line1,
                    adresse2=recipient.address_line2,
                    codePostal=recipient.postal_code,
                    ville=recipient.city,
                    codePays=recipient.country_code,
                    nomContact=recipient.person_name,
                    email=recipient.email,
                    telFixe=recipient.phone_number,
                    indTelMobile=None,
                    telMobile=None,
                    codePorte=recipient.suite,
                    codeTiers=None,
                    noEntrepositaireAgree=None,
                    particulier=recipient.residential,
                ),
                listUmgs=[
                    geodis.ListUmgType(
                        palette=(
                            package.packaging_type == units.PackagingUnit.pallet.name
                        ),
                        paletteConsignee=None,
                        quantite=1,
                        poids=package.weight.KG,
                        volume=package.volume.m3,
                        longueurUnitaire=package.length.CM,
                        largeurUnitaire=package.width.CM,
                        hauteurUnitaire=package.height.CM,
                        referenceColis=package.parcel.reference_number,
                    )
                    for package in packages
                ],
                natureEnvoi=None,
                poidsTotal=packages.weight.KG,
                volumeTotal=packages.volume.m3,
                largerTotal=None,
                hauteurTotal=None,
                longueurTotal=None,
                uniteTaxation=None,
                animauxPlumes=None,
                optionLivraison=next(
                    (
                        option.code
                        for _, option in options.items()
                        if option.state is True
                    ),
                    None,
                ),
                codeSaBureauRestant=None,
                idPointRelais=None,
                dateLivraison=options.geodis_date_livraison.state,
                heureLivraison=options.geodis_heure_livraison.state,
                instructionLivraison=options.geodis_instruction_livraison.state,
                natureMarchandise=None,
                valeurDeclaree=None,
                contreRemboursement=None,
                codeIncotermConditionLivraison=(
                    provider_units.Incoterm.map(customs.incoterm).value or "P"
                ),
                typeTva=None,
                sadLivToph=None,
                sadSwap=None,
                sadLivEtage=None,
                sadMiseLieuUtil=None,
                sadDepotage=None,
                etage=None,
                emailNotificationDestinataire=(
                    options.email_notification_to.state or recipient.email
                ),
                smsNotificationDestinataire=shipper.phone_number,
                emailNotificationExpediteur=shipper.email,
                emailConfirmationEnlevement=None,
                emailPriseEnChargeEnlevement=None,
                poidsQteLimiteeMD=None,
                dangerEnvQteLimiteeMD=None,
                nbColisQteExcepteeMD=None,
                dangerEnvQteExcepteeMD=None,
                listMatieresDangereuses=[],
                listVinsSpiritueux=None,
                nosUmsAEtiqueter=None,
                listDocumentsEnvoi=[],
                informationDouane=None,
            )
        ],
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(label_type=label_type.name or "PDF"),
    )
