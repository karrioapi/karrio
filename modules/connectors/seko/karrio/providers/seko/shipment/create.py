"""Karrio SEKO Logistics shipment API implementation."""

import karrio.schemas.seko.shipping_request as seko
import karrio.schemas.seko.shipping_response as shipping

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.seko.error as error
import karrio.providers.seko.utils as provider_utils
import karrio.providers.seko.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    shipment = (
        _extract_details(response, settings) if "tracking_number" in response else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    details = None  # parse carrier shipment type from "data"
    label = ""  # extract and process the shipment label to a valid base64 text
    # invoice = ""  # extract and process the shipment invoice to a valid base64 text if applies

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number="",  # extract tracking number from shipment
        shipment_identifier="",  # extract shipment identifier from shipment
        label_type="PDF",  # extract shipment label file format
        docs=models.Documents(
            label=label,  # pass label base64 text
            # invoice=invoice,  # pass invoice base64 text if applies
        ),
        meta=dict(
            # any relevent meta
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
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # map data to convert karrio model to seko specific type
    request = seko.ShippingRequestType(
        DeliveryReference=None,
        Reference2=None,
        Reference3=None,
        Origin=seko.DestinationType(
            Id=None,
            Name=None,
            Address=seko.AddressType(
                BuildingName=None,
                StreetAddress=None,
                Suburb=None,
                City=None,
                PostCode=None,
                CountryCode=None,
            ),
            ContactPerson=None,
            PhoneNumber=None,
            Email=None,
            DeliveryInstructions=None,
            RecipientTaxId=None,
            SendTrackingEmail=None,
        ),
        Destination=seko.DestinationType(
            Id=None,
            Name=None,
            Address=seko.AddressType(
                BuildingName=None,
                StreetAddress=None,
                Suburb=None,
                City=None,
                PostCode=None,
                CountryCode=None,
            ),
            ContactPerson=None,
            PhoneNumber=None,
            Email=None,
            DeliveryInstructions=None,
            RecipientTaxId=None,
            SendTrackingEmail=None,
        ),
        DangerousGoods=seko.DangerousGoodsType(
            AdditionalHandlingInfo=None,
            HazchemCode=None,
            IsRadioActive=None,
            CargoAircraftOnly=None,
            IsDGLQ=None,
            TotalQuantity=None,
            TotalKg=None,
            SignOffName=None,
            SignOffRole=None,
            LineItems=[
                seko.ItemType(
                    HarmonizedCode=None,
                    Description=None,
                    ClassOrDivision=None,
                    UNorIDNo=None,
                    PackingGroup=None,
                    SubsidaryRisk=None,
                    Packing=None,
                    PackingInstr=None,
                    Authorization=None,
                )
            ],
        ),
        Commodities=[
            seko.CommodityType(
                Description=None,
                Units=None,
                UnitValue=None,
                UnitKg=None,
                Currency=None,
                Country=None,
                IsDG=None,
                itemSKU=None,
                DangerousGoodsItem=seko.ItemType(
                    HarmonizedCode=None,
                    Description=None,
                    ClassOrDivision=None,
                    UNorIDNo=None,
                    PackingGroup=None,
                    SubsidaryRisk=None,
                    Packing=None,
                    PackingInstr=None,
                    Authorization=None,
                ),
            )
        ],
        Packages=[
            seko.PackageType(
                Height=None,
                Length=None,
                Width=None,
                Kg=None,
                Name=None,
                Type=None,
                OverLabelBarcode=None,
            )
        ],
        issignaturerequired=None,
        DutiesAndTaxesByReceiver=None,
        PrintToPrinter=None,
        IncludeLineDetails=None,
        Carrier=None,
        Service=None,
        CostCentreName=None,
        CodValue=None,
        TaxCollected=None,
        AmountCollected=None,
        TaxIds=[
            seko.TaxIDType(
                IdType=None,
                IdNumber=None,
            )
        ],
        Outputs=[],
    )

    return lib.Serializable(request, lib.to_dict)
