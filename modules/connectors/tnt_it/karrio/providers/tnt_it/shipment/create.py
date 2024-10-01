"""Karrio TNT Connect Italy shipment API implementation."""

import karrio.schemas.tnt_it.routinglabel as tnt

import typing
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.tnt_it.error as error
import karrio.providers.tnt_it.utils as provider_utils
import karrio.providers.tnt_it.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    shipment = (
        _extract_details(response, settings) if "tracking_number" in response else None
    )

    return shipment, messages


def _extract_details(
    data: lib.Element,
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
    return_address = lib.to_address(payload.return_address)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    (___, division, product) = provider_units.ShippingServiceCode.details(service)
    options = lib.to_shipping_options(
        payload.options,
        initializer=provider_units.shipping_options_initializer,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    is_international = recipient.country_code != shipper.country_code
    shipment_options = lambda _options: [
        option
        for _, option in _options.items()
        if option.state is not False and option.code in provider_units.SHIPMENT_OPTIONS
    ]

    request = tnt.shipment(
        software=tnt.softwareType(
            application="MYRTLI" if is_international else "MYRTL",
            version="1.0",
        ),
        security=tnt.securityType(
            customer=settings.customer,
            user=settings.username,
            password=settings.password,
            langId=settings.connection_config.lang_id.state or "IT",
        ),
        consignment=[
            tnt.consignmentType(
                action="I",
                internazionale="Y" if is_international else "N",
                insurance="Y" if package.options.insurance.state else "N",
                hazardous="Y" if package.options.dangerous_goods.state else "N",
                cashondeliver="Y" if package.options.cash_on_delivery.state else "N",
                codcommision="D" if package.options.cash_on_delivery.state else None,
                insurancecommision="S" if package.options.insurance.state else None,
                operationaloption=None,
                laroseDepot=package.options.larose_depot.state,
                senderAccId=settings.account_number,
                consignmentno=package.reference_number,
                consignmenttype="C" if package.reference_number else None,
                actualweight=lib.to_numeric_decimal(package.weight.KG, 5, 3),
                actualvolume=lib.to_numeric_decimal(package.dimensions.m3, 4, 3),
                totalpackages=len(packages),
                packagetype=lib.identity(
                    provider_units.PackageType.map(package.packaging).value or "C"
                ),
                division=division,
                product=product,
                vehicle=package.options.tnt_vehicle.state,
                insurancevalue=lib.to_numeric_decimal(
                    package.options.insurance.value, 11, 2
                ),
                insurancecurrency=lib.identity(
                    package.options.currency.state or "EUR"
                    if package.options.insurance.state
                    else None
                ),
                packingdesc="BOX",
                reference=package.reference_number,
                collectiondate=lib.fdatetime(
                    lib.to_next_business_datetime(
                        package.options.shipment_date.state or datetime.datetime.now(),
                        current_format="%Y-%m-%d",
                    ),
                    output_format="%Y%m%d",
                ),
                collectiontime=None,
                invoicevalue=package.options.declared_value.state,
                invoicecurrency=package.options.currency.state,
                specialinstructions=package.options.instruction.state,
                options=lib.identity(
                    tnt.optionsType(
                        option=[
                            option.code
                            for _, option in shipment_options(package.options)
                        ]
                    )
                    if any(shipment_options(package.options))
                    else None
                ),
                termsofpayment=lib.identity(
                    provider_units.PaymentType.map(payload.payment_type).value or "S"
                ),
                systemcode="RL",
                systemversion="1.0",
                codfvalue=None,
            )
            for package in packages
        ],
        hazardous="Y" if options.dangerous_goods.state else "N",
        labelType="PDF",
        FullPageLabel="Y" if options.full_page_label.state else "N",
    )

    return lib.Serializable(request, lib.to_xml)
