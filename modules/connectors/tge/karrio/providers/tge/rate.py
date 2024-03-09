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
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    rates = (
        [
            _extract_details(
                response["TollMessage"]["RateEnquiry"]["Response"],
                settings,
                _response.ctx,
            )
        ]
        if response.get("TollMessage", {}).get("RateEnquiry", {}).get("Response")
        is not None
        else []
    )

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
        transit_days=getattr(rate.TransitTime, "Value", None),
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
        option_type=provider_units.ShippingOption,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        package_option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    service = getattr(services.first, "value", None)

    request = tge.RateRequestType(
        TollMessage=tge.TollMessageType(
            Header=tge.HeaderType(
                MessageVersion="1.0",
                MessageIdentifier=str(uuid.uuid4()),
                CreateTimestamp=(
                    datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
                ),
                DocumentType="RateEnquiry",
                Environment=("PRD" if not settings.test_mode else "TST"),
                SourceSystemCode=settings.channel or "XP41",
                MessageSender=settings.connection_config.app_name.state or "GOSHIPR",
                MessageReceiver="TOLL",
            ),
            RateEnquiry=tge.RateEnquiryType(
                Request=tge.RequestType(
                    BusinessID=options.tge_business_id.state,
                    SystemFields=(
                        tge.SystemFieldsType(
                            PickupDateTime=payload.pickup_datetime,
                        )
                        if options.tge_pickup_datetime.state
                        else None
                    ),
                    ShipmentService=tge.ShipmentServiceType(
                        ServiceCode=service,
                        ShipmentProductCode="",
                    ),
                    ShipmentFlags=(
                        tge.ShipmentFlagsType(
                            ExtraServiceFlag="true",
                        )
                        if options.tge_extra_service_flag.state
                        else None
                    ),
                    ShipmentFinancials=(
                        tge.ShipmentFinancialsType(
                            ExtraServicesAmount=tge.ExtraServicesAmountType(
                                Currency=options.currency.state,
                                Value=options.tge_extra_services_amount.state,
                            )
                        )
                        if options.tge_extra_services_amount.state
                        else None
                    ),
                    FreightMode=(
                        lib.text(options.tge_freight_mode.state)
                        or lib.text(settings.connection_config.freight_mode.state)
                    ),
                    BillToParty=tge.BillToPartyType(
                        AccountCode=settings.account_code.state,
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
                                    CommodityCode=(
                                        provider_units.PackagingType.map(
                                            package.packaging_type
                                        ).value
                                        or "Z"
                                    ),
                                    CommodityDescription=package.description,
                                ),
                                ShipmentItemTotals=tge.ShipmentItemTotalsType(
                                    ShipmentItemCount=len(packages),
                                ),
                                Dimensions=tge.DimensionsType(
                                    Width=package.width.map(
                                        provider_utils.MeasurementOptions
                                    ).CM,
                                    Length=package.length.map(
                                        provider_utils.MeasurementOptions
                                    ).CM,
                                    Height=package.height.map(
                                        provider_utils.MeasurementOptions
                                    ).CM,
                                    Volume=package.volume.map(
                                        provider_utils.MeasurementOptions
                                    ).cm3,
                                    Weight=package.weight.map(
                                        provider_utils.MeasurementOptions
                                    ).KG,
                                ),
                            )
                            for package in packages
                        ]
                    ),
                )
            ),
        )
    )

    return lib.Serializable(request, lib.to_dict)
