import karrio.schemas.nationex.shipment_request as nationex
import karrio.schemas.nationex.shipment_response as shipping
import typing
import base64
import urllib.parse
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.nationex.error as error
import karrio.providers.nationex.utils as provider_utils
import karrio.providers.nationex.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response_data = _response.deserialize()
    messages = error.parse_error_response(response_data, settings)
    shipment = (
        None
        if any(messages)
        else _extract_details(response_data, settings, _response.ctx)
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict,
) -> models.ShipmentDetails:
    shipment = lib.to_object(shipping.ShipmentResponseType, data)
    query = urllib.parse.urlencode(ctx["label"])
    label = lib.failsafe(
        lambda: lib.request(
            url=f"{settings.base_url}/Shipments/{shipment.ShipmentId}/labels?{query}",
            decoder=lambda _: lib.decode(base64.encodebytes(_)),
        )
    )

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=str(shipment.ShipmentId),
        shipment_identifier=str(shipment.ShipmentId),
        label_type=ctx["label"]["type"],
        docs=models.Documents(label=label),
        meta=dict(
            tracking_numbers=shipment.ParcelIds,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels, max_weight=units.Weight(99, "LB"))
    unit = provider_units.MeasurementUnit.map(packages.weight_unit).value
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        option_type=provider_units.ShippingOption,
    )

    request = dict(
        shipment=nationex.ShipmentRequestType(
            CustomerId=lib.to_int(settings.customer_id),
            ExpeditionDate=lib.fdate(options.shipment_date.state, "%Y-%m-%d"),
            ShipmentType=service,
            TotalParcels=len(packages),
            TotalWeight=packages.weight.value,
            ReferenceNumber=payload.reference,
            CustomBarcode=None,
            Note=options.nationex_note.state,
            BillingAccount=lib.to_int(
                getattr(payload.payment, "account_number", settings.billing_account)
            ),
            Sender=nationex.DestinationType(
                Contact=shipper.contact,
                AccountNumber=None,
                AccountName=None,
                Address1=shipper.address_line1,
                Address2=shipper.address_line2,
                PostalCode=shipper.postal_code,
                ProvinceState=shipper.state_code,
                Phone=shipper.phone_number,
                SmsNotification=None,
                EmailNotification=None,
                NoCivic=shipper.street_number,
                Suite=None,
                StreetName=shipper.street_name,
                Email=shipper.email,
            ),
            Destination=nationex.DestinationType(
                Contact=recipient.contact,
                AccountNumber=None,
                AccountName=None,
                Address1=recipient.address_line1,
                Address2=recipient.address_line2,
                PostalCode=recipient.postal_code,
                ProvinceState=recipient.state_code,
                Phone=recipient.phone_number,
                SmsNotification=options.nationex_sms_notification.state,
                EmailNotification=options.nationex_email_notification.state,
                NoCivic=recipient.street_number,
                Suite=None,
                StreetName=recipient.street_name,
                Email=recipient.email,
            ),
            Accessory=nationex.AccessoryType(
                InsuranceAmount=options.nationex_insurance_amount.state,
                FrozenProtection=options.nationex_frozen_protection.state,
                DangerousGoods=options.nationex_dangerous_goods.state,
                SNR=(
                    options.nationex_snr.state
                    if options.nationex_snr.state is not None
                    else True
                ),
            ),
            Parcels=[
                nationex.ParcelType(
                    NCV=(
                        True
                        if (
                            package.length.IN > 36
                            or package.width.IN > 36
                            or package.height.IN > 36
                            or package.weight.LB > 70
                        )
                        else False
                    ),
                    Weight=package.weight.map(provider_units.MeasurementOptions).value,
                    Dimensions=(
                        nationex.DimensionsType(
                            Length=package.length.value,
                            Width=package.width.value,
                            Height=package.height.value,
                            Cubing=lib.to_decimal(
                                (
                                    package.length.IN
                                    * package.width.IN
                                    * package.height.IN
                                )
                                / 1728
                            ),
                        )
                        if any(
                            [
                                package.length.value,
                                package.width.value,
                                package.height.value,
                            ]
                        )
                        else None
                    ),
                )
                for package in packages
            ],
            UnitsOfMeasurement=unit,
        ),
        label=dict(
            type=payload.label_type or "PDF",
            orientation="portrait",
            format="4x6",
        ),
    )

    return lib.Serializable(
        request,
        lambda _: dict(
            label=_["label"],
            shipment=lib.to_dict(_["shipment"]),
        ),
    )
