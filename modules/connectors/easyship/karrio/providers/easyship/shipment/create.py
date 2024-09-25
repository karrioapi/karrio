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
            ein=recipient.extra.get("ein"),
            vatnumber=recipient.extra.get("vat_number"),
        ),
        courierselection=easyship.CourierSelectionType(
            allowcourierfallback=options.get("allow_courier_fallback", False),
            applyshippingrules=options.get("apply_shipping_rules", True),
            listunavailablecouriers=options.get("list_unavailable_couriers", False),
            selectedcourierid=service,
        ),
        destinationaddress=easyship.AddressType(
            city=recipient.city,
            companyname=recipient.company_name,
            contactemail=recipient.email,
            contactname=recipient.person_name,
            contactphone=recipient.phone_number,
            countryalpha2=recipient.country_code,
            line1=recipient.address_line1,
            line2=recipient.address_line2,
            postalcode=recipient.postal_code,
            state=recipient.state_code,
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
        consigneetaxid=recipient.extra.get("tax_id"),
        eeireference=payload.customs.eel or payload.customs.ppa,
        incoterms=payload.incoterm,
        metadata=[easyship.Any(key=k, value=v) for k, v in payload.metadata.items()],
        insurance=easyship.InsuranceType(
            isinsured=payload.insurance.amount > 0 if payload.insurance else False,
        ),
        orderdata=easyship.OrderDataType(
            buyernotes=payload.options.get("buyer_notes"),
            buyerselectedcouriername=None,
            ordercreatedat=payload.options.get("order_date"),
            platformname=payload.options.get("platform_name"),
            platformordernumber=payload.options.get("platform_order_number"),
            ordertaglist=payload.options.get("order_tags", []),
            sellernotes=payload.options.get("seller_notes"),
        ),
        originaddress=easyship.AddressType(
            city=shipper.city,
            companyname=shipper.company_name,
            contactemail=shipper.email,
            contactname=shipper.person_name,
            contactphone=shipper.phone_number,
            countryalpha2=shipper.country_code,
            line1=shipper.address_line1,
            line2=shipper.address_line2,
            postalcode=shipper.postal_code,
            state=shipper.state_code,
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
            eori=shipper.extra.get("eori"),
            ioss=shipper.extra.get("ioss"),
            vatnumber=shipper.extra.get("vat_number"),
        ),
        shipmentrequestreturn=payload.options.get("is_return", False),
        returnaddress=easyship.AddressType(
            city=payload.return_address.city if payload.return_address else None,
            companyname=(
                payload.return_address.company_name if payload.return_address else None
            ),
            contactemail=(
                payload.return_address.email if payload.return_address else None
            ),
            contactname=(
                payload.return_address.person_name if payload.return_address else None
            ),
            contactphone=(
                payload.return_address.phone_number if payload.return_address else None
            ),
            countryalpha2=(
                payload.return_address.country_code if payload.return_address else None
            ),
            line1=(
                payload.return_address.address_line1 if payload.return_address else None
            ),
            line2=(
                payload.return_address.address_line2 if payload.return_address else None
            ),
            postalcode=(
                payload.return_address.postal_code if payload.return_address else None
            ),
            state=payload.return_address.state_code if payload.return_address else None,
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
        returnaddressid=payload.options.get("return_address_id"),
        senderaddress=easyship.AddressType(
            city=shipper.city,
            companyname=shipper.company_name,
            contactemail=shipper.email,
            contactname=shipper.person_name,
            contactphone=shipper.phone_number,
            countryalpha2=shipper.country_code,
            line1=shipper.address_line1,
            line2=shipper.address_line2,
            postalcode=shipper.postal_code,
            state=shipper.state_code,
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
        senderaddressid=payload.options.get("sender_address_id"),
        setasresidential=recipient.residential,
        shippingsettings=easyship.ShippingSettingsType(
            additionalservices=easyship.AdditionalServicesType(
                deliveryconfirmation=options.get("delivery_confirmation"),
                qrcode=options.get("qr_code"),
            ),
            b13afiling=easyship.B13AFilingType(
                option=options.get("b13a_filing_option"),
                optionexportcompliancestatement=options.get(
                    "b13a_export_compliance_statement"
                ),
                permitnumber=options.get("b13a_permit_number"),
            ),
            buylabel=True,
            buylabelsynchronous=True,
            printingoptions=easyship.PrintingOptionsType(
                commercialinvoice=options.get("commercial_invoice", True),
                format=options.get("label_format", "pdf"),
                label=options.get("label", True),
                packingslip=options.get("packing_slip", False),
                remarks=options.get("remarks"),
            ),
            units=easyship.UnitsType(
                dimensions=options.get("dimension_unit", "cm"),
                weight=options.get("weight_unit", "kg"),
            ),
        ),
        parcels=[
            easyship.ParcelType(
                box=easyship.BoxType(
                    height=parcel.height.value,
                    length=parcel.length.value,
                    weight=parcel.weight.value,
                    width=parcel.width.value,
                    slug=parcel.packaging_type or None,
                ),
                items=[
                    easyship.ItemType(
                        actualweight=item.weight.value,
                        category=item.product_id,
                        containsbatterypi966=item.contains_battery,
                        containsbatterypi967=item.contains_battery,
                        containsliquids=item.contains_liquids,
                        declaredcurrency=item.currency,
                        declaredcustomsvalue=item.value_amount,
                        description=item.description,
                        dimensions=easyship.DimensionsType(
                            height=item.height.value,
                            length=item.length.value,
                            width=item.width.value,
                        ),
                        hscode=item.hs_code,
                        origincountryalpha2=item.origin_country,
                        quantity=item.quantity,
                        sku=item.sku,
                    )
                    for item in parcel.items
                ],
                totalactualweight=parcel.weight.value,
            )
            for parcel in packages
        ],
    )

    return lib.Serializable(request, lib.to_dict)
