"""Karrio Easyship shipment API implementation."""

import karrio.schemas.easyship.shipment_request as easyship
import karrio.schemas.easyship.shipment_response as shipping

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.easyship.error as error
import karrio.providers.easyship.utils as provider_utils
import karrio.providers.easyship.units as provider_units


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

    # map data to convert karrio model to easyship specific type
    request = easyship.ShipmentRequestType(
        buyerregulatoryidentifiers=easyship.BuyerRegulatoryIdentifiersType(
            ein=None,
            vatnumber=None,
        ),
        courierselection=easyship.CourierSelectionType(
            allowcourierfallback=None,
            applyshippingrules=None,
            listunavailablecouriers=None,
            selectedcourierid=None,
        ),
        destinationaddress=easyship.AddressType(
            city=None,
            companyname=None,
            contactemail=None,
            contactname=None,
            contactphone=None,
            countryalpha2=None,
            line1=None,
            line2=None,
            postalcode=None,
            state=None,
            validation=easyship.ValidationType(
                detail=None,
                status=None,
                comparison=easyship.ComparisonType(
                    changes=None,
                    post=None,
                    pre=None,
                ),
            ),
        ),
        consigneetaxid=None,
        eeireference=None,
        incoterms=None,
        metadata=[easyship.Any()],
        insurance=easyship.InsuranceType(
            isinsured=None,
        ),
        orderdata=easyship.OrderDataType(
            buyernotes=None,
            buyerselectedcouriername=None,
            ordercreatedat=None,
            platformname=None,
            platformordernumber=None,
            ordertaglist=[],
            sellernotes=None,
        ),
        originaddress=easyship.AddressType(
            city=None,
            companyname=None,
            contactemail=None,
            contactname=None,
            contactphone=None,
            countryalpha2=None,
            line1=None,
            line2=None,
            postalcode=None,
            state=None,
            validation=easyship.ValidationType(
                detail=None,
                status=None,
                comparison=easyship.ComparisonType(
                    changes=None,
                    post=None,
                    pre=None,
                ),
            ),
        ),
        regulatoryidentifiers=easyship.RegulatoryIdentifiersType(
            eori=None,
            ioss=None,
            vatnumber=None,
        ),
        shipmentrequestreturn=None,
        returnaddress=easyship.AddressType(
            city=None,
            companyname=None,
            contactemail=None,
            contactname=None,
            contactphone=None,
            countryalpha2=None,
            line1=None,
            line2=None,
            postalcode=None,
            state=None,
            validation=easyship.ValidationType(
                detail=None,
                status=None,
                comparison=easyship.ComparisonType(
                    changes=None,
                    post=None,
                    pre=None,
                ),
            ),
        ),
        returnaddressid=None,
        senderaddress=easyship.AddressType(
            city=None,
            companyname=None,
            contactemail=None,
            contactname=None,
            contactphone=None,
            countryalpha2=None,
            line1=None,
            line2=None,
            postalcode=None,
            state=None,
            validation=easyship.ValidationType(
                detail=None,
                status=None,
                comparison=easyship.ComparisonType(
                    changes=None,
                    post=None,
                    pre=None,
                ),
            ),
        ),
        senderaddressid=None,
        setasresidential=None,
        shippingsettings=easyship.ShippingSettingsType(
            additionalservices=easyship.AdditionalServicesType(
                deliveryconfirmation=None,
                qrcode=None,
            ),
            b13afiling=easyship.B13AFilingType(
                option=None,
                optionexportcompliancestatement=None,
                permitnumber=None,
            ),
            buylabel=None,
            buylabelsynchronous=None,
            printingoptions=easyship.PrintingOptionsType(
                commercialinvoice=None,
                format=None,
                label=None,
                packingslip=None,
                remarks=None,
            ),
            units=easyship.UnitsType(
                dimensions=None,
                weight=None,
            ),
        ),
        parcels=[
            easyship.ParcelType(
                box=easyship.BoxType(
                    height=None,
                    length=None,
                    weight=None,
                    width=None,
                    slug=None,
                ),
                items=[
                    easyship.ItemType(
                        actualweight=None,
                        category=easyship.Any(),
                        containsbatterypi966=None,
                        containsbatterypi967=None,
                        containsliquids=None,
                        declaredcurrency=None,
                        declaredcustomsvalue=None,
                        description=None,
                        dimensions=easyship.DimensionsType(
                            height=None,
                            length=None,
                            width=None,
                        ),
                        hscode=None,
                        origincountryalpha2=None,
                        quantity=None,
                        sku=None,
                    )
                ],
                totalactualweight=None,
            )
        ],
    )

    return lib.Serializable(request, lib.to_dict)
