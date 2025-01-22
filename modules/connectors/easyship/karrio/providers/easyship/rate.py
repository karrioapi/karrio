"""Karrio Easyship rating API implementation."""

import karrio.schemas.easyship.rate_request as easyship
import karrio.schemas.easyship.rate_response as rating

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.easyship.error as error
import karrio.providers.easyship.utils as provider_utils
import karrio.providers.easyship.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    rates = [_extract_details(rate, settings) for rate in response.get("rates", [])]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    details = lib.to_object(rating.RateType, data)
    service = provider_units.ShippingServiceID.map(details.courier_id)
    courier = provider_units.ShippingCourierID.find(service.value_or_key)

    charges = [
        ("Shipment Charge", details.shipment_charge),
        ("Insurance", details.insurance_fee),
        ("Other Surcharges", getattr(details.other_surcharges, "total_fee", 0.0)),
        ("Fuel Surcharge", details.fuel_surcharge),
        ("Additional Surcharge", details.additional_services_surcharge),
        ("Import Duty Charge", details.import_duty_charge),
        ("Import Tax Charge", details.import_tax_charge),
        ("Minimum Pickup Fee", details.minimum_pickup_fee),
        ("Oversized Surcharge", details.oversized_surcharge),
        ("Provincial Sales Tax", details.provincial_sales_tax),
        ("Remote Area Surcharge", details.remote_area_surcharge),
        ("Sales Tax", details.sales_tax),
        ("Warehouse Handling Fee", details.warehouse_handling_fee),
        ("Discount", lib.failsafe(lambda: details.discount.amount)),
    ]

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.value_or_key,
        total_charge=lib.to_money(details.total_charge),
        currency=details.currency,
        transit_days=details.max_delivery_time,
        extra_charges=[
            models.ChargeDetails(
                name=name,
                amount=lib.to_money(amount),
                currency=details.currency,
            )
            for name, amount in charges
            if amount is not None and amount > 0
        ],
        meta=dict(
            rate_provider=courier.name_or_key,
            easyship_incoterms=details.incoterms,
            easyship_courier_id=details.courier_id,
            service_name=service.value or details.courier_name,
            available_handover_options=details.available_handover_options,
            value_for_money_rank=details.value_for_money_rank,
            tracking_rating=details.tracking_rating,
            min_delivery_time=details.min_delivery_time,
            max_delivery_time=details.max_delivery_time,
            delivery_time_rank=details.delivery_time_rank,
            cost_rank=details.cost_rank,
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    weight_unit, dimension_unit = packages.compatible_units
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )
    incoterms = lib.identity(
        options.easyship_incoterms.state
        or getattr(getattr(payload, "customs", None), "incoterm", None)
    )

    # map data to convert karrio model to easyship specific type
    request = easyship.RateRequestType(
        courier_selection=lib.identity(
            easyship.CourierSelectionType(
                apply_shipping_rules=lib.identity(
                    options.easyship_apply_shipping_rules.state
                    if options.easyship_apply_shipping_rules.state is not None
                    else settings.connection_config.apply_shipping_rules.state
                ),
                show_courier_logo_url=options.easyship_show_courier_logo_url.state,
            )
            if any(
                [
                    settings.connection_config.apply_shipping_rules.state,
                    options.easyship_apply_shipping_rules.state,
                    options.easyship_show_courier_logo_url.state,
                ]
            )
            else None
        ),
        destination_address=easyship.NAddressType(
            country_alpha2=recipient.country_code,
            city=recipient.city,
            company_name=lib.text(recipient.company_name or "N/A", max=22),
            contact_email=recipient.email,
            contact_name=lib.text(recipient.person_name, max=22),
            contact_phone=recipient.phone_number,
            line_1=recipient.address_line1,
            line_2=recipient.address_line2,
            postal_code=recipient.postal_code,
            state=recipient.state_code,
        ),
        incoterms=incoterms,
        insurance=easyship.InsuranceType(
            insured_amount=options.insurance.state,
            insured_currency=lib.identity(
                options.currency.state if options.insurance.state is not None else None
            ),
            is_insured=options.insurance.state is not None,
        ),
        origin_address=easyship.NAddressType(
            country_alpha2=shipper.country_code,
            city=shipper.city,
            company_name=lib.text(shipper.company_name or "N/A", max=22),
            contact_email=shipper.email,
            contact_name=lib.text(shipper.person_name, max=22),
            contact_phone=shipper.phone_number,
            line_1=shipper.address_line1,
            line_2=shipper.address_line2,
            postal_code=shipper.postal_code,
            state=shipper.state_code,
        ),
        parcels=[
            easyship.ParcelType(
                box=easyship.BoxType(
                    height=package.height.value,
                    length=package.length.value,
                    width=package.width.value,
                    slug=package.options.easyship_box_slug.state,
                ),
                items=[
                    easyship.ItemType(
                        dimensions=None,
                        declared_currency=lib.identity(
                            item.value_currency or options.currency.state or "USD"
                        ),
                        origin_country_alpha2=lib.identity(
                            item.origin_country or shipper.country_code
                        ),
                        quantity=item.quantity,
                        actual_weight=item.weight,
                        category=item.category or "bags_luggages",
                        declared_customs_value=item.value_amount,
                        description=item.description or item.title or "Item",
                        sku=item.sku or "N/A",
                        hs_code=item.hs_code or "N/A",
                        contains_liquids=item.metadata.get("contains_liquids"),
                        contains_battery_pi966=item.metadata.get(
                            "contains_battery_pi966"
                        ),
                        contains_battery_pi967=item.metadata.get(
                            "contains_battery_pi967"
                        ),
                    )
                    for item in lib.identity(
                        package.items
                        if any(package.items)
                        else [
                            models.Commodity(
                                title=lib.text(package.description, max=35),
                                description=package.description,
                                quantity=1,
                                hs_code="N/A",
                                value_amount=1.0,
                                value_currency=options.currency.state or "USD",
                                category="bags_luggages",
                            )
                        ]
                    )
                ],
                total_actual_weight=package.weight.value,
            )
            for package in packages
        ],
        shipping_settings=easyship.ShippingSettingsType(
            output_currency=options.currency.state,
            units=easyship.UnitsType(
                dimensions=provider_units.DimensionUnit.map(dimension_unit.name).value,
                weight=provider_units.WeightUnit.map(weight_unit.name).value,
            ),
        ),
    )

    return lib.Serializable(request, lib.to_dict)
