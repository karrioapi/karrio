import karrio.schemas.tge.rate_request as tge
import karrio.schemas.tge.rate_response as rating
import uuid
import typing
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.tge.error as error
import karrio.providers.tge.utils as provider_utils
import karrio.providers.tge.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[typing.List[dict]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    package_rates: typing.List[typing.Tuple[str, typing.List[models.RateDetails]]] = [
        (
            f"{_}",
            [
                _extract_details(
                    response["TollMessage"]["RateEnquiry"]["Response"],
                    settings,
                    _response.ctx,
                )
                for rate in (response if isinstance(response, list) else [response])
                if response.get("TollMessage", {})
                .get("RateEnquiry", {})
                .get("Response")
                is not None
            ],
        )
        for _, response in enumerate(responses, start=1)
    ]

    messages = error.parse_error_response(responses, settings)
    rates = lib.to_multi_piece_rates(package_rates)

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict,
) -> models.RateDetails:
    rate = lib.to_object(rating.ResponseType, data)
    service = provider_units.ShippingService.map(ctx.get("service"))
    charges = [
        (name, lib.to_money(amount["Value"]))
        for name, amount in data.items()
        if isinstance(amount, dict) and amount.get("Value") is not None
    ]

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(rate.TotalChargeAmount.Value),
        currency=units.Currency.AUD.name,
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=amount,
                currency=units.Currency.AUD.name,
            )
            for name, amount in charges
            if amount > 0
        ],
        transit_days=lib.to_int(getattr(rate.TransitTime, "Value", None)),
        meta=dict(
            service_name=service.name,
            EnquiryID=rate.EnquiryID,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    services = lib.to_services(payload.services, provider_units.ShippingService)
    options = lib.to_shipping_options(
        payload.options,
        initializer=provider_units.shipping_options_initializer,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        package_option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    service = getattr(services.first, "value", None) or "X"

    now = datetime.datetime.now()
    create_time = lib.fdatetime(now, output_format="%H:%M:%S")
    create_date = lib.fdatetime(now, output_format="%Y-%m-%dT")
    shipping_date = lib.to_date(options.shipment_date.state or now)
    pickup_date = lib.fdatetime(
        provider_utils.next_pickup_date(shipping_date), output_format="%Y-%m-%dT"
    )

    request = [
        tge.RateRequestType(
            TollMessage=tge.TollMessageType(
                Header=tge.HeaderType(
                    MessageVersion="1.0",
                    DocumentType="RateEnquiry",
                    MessageIdentifier=str(uuid.uuid4()),
                    CreateTimestamp=f"{create_date}{create_time}.000+00:00",
                    Environment="prd",
                    SourceSystemCode=(
                        settings.connection_config.source_system_code.state or "XP41"
                    ),
                    MessageSender=(
                        settings.connection_config.message_sender.state or "GOSHIPR"
                    ),
                    MessageReceiver="TOLL",
                ),
                RateEnquiry=tge.RateEnquiryType(
                    Request=tge.RequestType(
                        BusinessID=options.tge_business_id.state or "IPEC",
                        SystemFields=tge.SystemFieldsType(
                            PickupDateTime=(
                                options.pickup_datetime.state
                                or f"{pickup_date}{create_time}.000+00:00"
                            ),
                        ),
                        ShipmentService=tge.ShipmentServiceType(
                            ServiceCode=service,
                        ),
                        ShipmentFlags=tge.ShipmentFlagsType(ExtraServiceFlag="true"),
                        ShipmentFinancials=tge.ShipmentFinancialsType(
                            ExtraServicesAmount=tge.ExtraServicesAmountType(
                                Currency=options.currency.state or "AUD",
                                Value=str(
                                    lib.to_int(
                                        options.tge_extra_services_amount.state
                                        or options.declared_value.state
                                        or 10
                                    )
                                ),
                            )
                        ),
                        FreightMode=lib.identity(
                            lib.text(options.tge_freight_mode.state)
                            or lib.text(settings.connection_config.freight_mode.state)
                            or "Road"
                        ),
                        BillToParty=tge.BillToPartyType(
                            AccountCode=settings.account_code,
                        ),
                        ConsignorParty=tge.ConsignPartyType(
                            PhysicalAddress=tge.PhysicalAddressType(
                                Suburb=shipper.city,
                                StateCode=shipper.state_code,
                                PostalCode=shipper.postal_code,
                                CountryCode=shipper.country_code,
                            ),
                        ),
                        ConsigneeParty=tge.ConsignPartyType(
                            PhysicalAddress=tge.PhysicalAddressType(
                                Suburb=recipient.city,
                                StateCode=recipient.state_code,
                                PostalCode=recipient.postal_code,
                                CountryCode=recipient.country_code,
                            ),
                        ),
                        ShipmentItems=tge.ShipmentItemsType(
                            ShipmentItem=[
                                tge.ShipmentItemType(
                                    Commodity=tge.CommodityType(
                                        CommodityCode="Z",
                                        CommodityDescription="ALL FREIGHT",
                                    ),
                                    ShipmentItemTotals=tge.ShipmentItemTotalsType(
                                        ShipmentItemCount=str(len(packages)),
                                    ),
                                    Dimensions=tge.DimensionsType(
                                        Width=str(
                                            lib.to_int(
                                                package.width.map(
                                                    provider_units.MeasurementOptions
                                                ).CM
                                            )
                                        ),
                                        Length=str(
                                            lib.to_int(
                                                package.length.map(
                                                    provider_units.MeasurementOptions
                                                ).CM
                                            )
                                        ),
                                        Height=str(
                                            lib.to_int(
                                                package.height.map(
                                                    provider_units.MeasurementOptions
                                                ).CM
                                            )
                                        ),
                                        Volume=str(
                                            package.volume.map(
                                                provider_units.MeasurementOptions
                                            ).m3
                                        ),
                                        Weight=str(
                                            package.weight.map(
                                                provider_units.MeasurementOptions
                                            ).KG
                                        ),
                                    ),
                                )
                            ]
                        ),
                    )
                ),
            )
        )
        for package in packages
    ]

    return lib.Serializable(request, lib.to_dict, dict(service=service))
