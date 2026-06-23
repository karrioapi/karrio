"""Karrio GLS Group shipment creation implementation."""

import datetime

import karrio.core.models as models
import karrio.core.units as units
import karrio.lib as lib
import karrio.providers.gls.error as error
import karrio.providers.gls.units as provider_units
import karrio.providers.gls.utils as provider_utils
import karrio.schemas.gls.shipment_request as gls_request
import karrio.schemas.gls.shipment_response as gls_response


def parse_shipment_response(
    _response: lib.Deserializable[str],
    settings: provider_utils.Settings,
) -> tuple[models.ShipmentDetails | None, list[models.Message]]:
    """Parse GLS Group shipment response."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    shipment = (
        _extract_details(response, settings, _response.ctx)
        if not any(messages) and (response.get("CreatedShipment") or {}).get("ParcelData")
        else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict = None,
) -> models.ShipmentDetails:
    """Extract shipment details from a CreatedShipment response."""
    shipment = lib.to_object(gls_response.ShipmentResponseType, data)
    created = shipment.CreatedShipment
    parcels = created.ParcelData
    print_data = created.PrintData or []

    primary_parcel = parcels[0]
    tracking_number = primary_parcel.ParcelNumber
    shipment_identifier = primary_parcel.TrackID

    labels = [pd.Data for pd in print_data if pd.Data]
    label_format = next((pd.LabelFormat for pd in print_data if pd.LabelFormat), "PDF")
    label_data = lib.bundle_base64(labels, label_format) if len(labels) > 1 else next(iter(labels), "")

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=shipment_identifier,
        label_type=label_format,
        docs=models.Documents(label=label_data),
        meta=dict(
            customer_id=created.CustomerID,
            pickup_location=created.PickupLocation,
            shipment_references=created.ShipmentReference or [],
            tracking_numbers=[p.ParcelNumber for p in parcels if p.ParcelNumber],
            track_ids=[p.TrackID for p in parcels if p.TrackID],
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create a shipment request for GLS Group API."""

    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    return_address = lib.to_address(payload.return_address or payload.shipper)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    label_format = payload.label_type or "PDF"
    shipping_date = lib.to_date(
        options.shipping_date.state or datetime.datetime.now(),
        current_format="%Y-%m-%dT%H:%M",
    )

    is_international = provider_units.is_international(shipper.country_code, recipient.country_code)
    incoterm = (payload.customs.incoterm if payload.customs else None) or "DDU" if is_international else None
    incoterm_code = lib.identity(provider_units.Incoterm.map(incoterm).value if incoterm else None)
    default_currency = lib.identity(
        options.currency.state or units.CountryCurrency.map(payload.shipper.country_code).value or "EUR"
    )

    contact_id = options.gls_contact_id.state or settings.contact_id

    shipping_date_str = lib.fdate(shipping_date, "%Y-%m-%d")

    # Customs Consignment v3 + Document Management v1 prep-upload + PUT all
    # fire inside ``proxy.upload_document`` (the carrier-side landing for the
    # unified ``flow="post_upload"`` paperless trade — see gls_paperless_trade
    # in units.py). create_shipment is just the ShipIT label POST now.

    request = gls_request.ShipmentRequestType(
        Shipment=gls_request.ShipmentType(
            Product=service.value_or_key or "PARCEL",
            IncotermCode=incoterm_code,
            Identifier=settings.connection_app_identifier,
            Middleware=provider_units.MIDDLEWARE,
            Shipper=gls_request.ShipperType(
                ContactID=contact_id,
                AlternativeShipperAddress=gls_request.AddressType(
                    Name1=shipper.company_name or shipper.person_name,
                    Name2=shipper.person_name if shipper.company_name else None,
                    Street=shipper.address_line1,
                    StreetNumber=shipper.address_line2,
                    ZIPCode=shipper.postal_code,
                    City=shipper.city,
                    CountryCode=shipper.country_code,
                    ContactPerson=shipper.person_name,
                    FixedLinePhonenumber=shipper.phone_number,
                    eMail=shipper.email,
                ),
            ),
            Consignee=gls_request.ConsigneeType(
                Address=gls_request.AddressType(
                    Name1=recipient.company_name or recipient.person_name,
                    Name2=recipient.person_name if recipient.company_name else None,
                    Street=recipient.address_line1,
                    StreetNumber=recipient.address_line2,
                    ZIPCode=recipient.postal_code,
                    City=recipient.city,
                    CountryCode=recipient.country_code,
                    ContactPerson=recipient.person_name,
                    FixedLinePhonenumber=recipient.phone_number,
                    eMail=recipient.email,
                ),
            ),
            ShipmentUnit=[
                gls_request.ShipmentUnitType(
                    Weight=package.weight.KG,
                    ShipmentUnitReference=([payload.reference] if payload.reference else None),
                    Service=[
                        *(
                            [
                                gls_request.ShipmentUnitServiceType(
                                    AddonLiability=gls_request.AddonLiabilityType(
                                        ServiceName="service_addonliability",
                                        Amount=float(options.insurance.state),
                                        Currency=default_currency,
                                    ),
                                )
                            ]
                            if options.insurance.state
                            else []
                        ),
                        *(
                            [
                                gls_request.ShipmentUnitServiceType(
                                    Cash=gls_request.AddonLiabilityType(
                                        ServiceName=options.gls_cash_service.code,
                                        Amount=float(options.cash_on_delivery.state or 0),
                                        Currency=default_currency,
                                        Reason=options.gls_cash_reason.state,
                                    ),
                                )
                            ]
                            if options.gls_cash_service.state
                            else []
                        ),
                        *(
                            [
                                gls_request.ShipmentUnitServiceType(
                                    HazardousGoods=gls_request.HazardousGoodsType(
                                        ServiceName=options.gls_hazardous_goods_service.code,
                                        HazardousGood=[
                                            gls_request.HazardousGoodType(
                                                GLSHazNo=options.gls_hazardous_goods_haz_no.state,
                                                Weight=(
                                                    float(options.gls_hazardous_goods_weight.state)
                                                    if options.gls_hazardous_goods_weight.state
                                                    else float(package.weight.KG)
                                                ),
                                            )
                                        ],
                                    ),
                                )
                            ]
                            if options.gls_hazardous_goods_service.state
                            else []
                        ),
                        *(
                            [
                                gls_request.ShipmentUnitServiceType(
                                    ExWorks=gls_request.ServiceType(
                                        ServiceName=options.gls_ex_works_service.code,
                                    ),
                                )
                            ]
                            if options.gls_ex_works_service.state
                            else []
                        ),
                        *(
                            [
                                gls_request.ShipmentUnitServiceType(
                                    LimitedQuantities=gls_request.LimitedQuantitiesType(
                                        ServiceName=options.gls_limited_quantity.code,
                                        Weight=(
                                            float(options.gls_limited_quantity_weight.state)
                                            if options.gls_limited_quantity_weight.state
                                            else None
                                        ),
                                    ),
                                )
                            ]
                            if options.gls_limited_quantity.state
                            else []
                        ),
                    ],
                )
                for package in packages
            ],
            ShipmentReference=([payload.reference] if payload.reference else None),
            ShippingDate=shipping_date_str,
            Service=[
                *(
                    gls_request.ShipmentServiceType(
                        Service=gls_request.ServiceType(ServiceName=getattr(options, key).code),
                    )
                    for key in provider_units.SHIPMENT_FLAG_OPTIONS
                    if getattr(options, key).state
                ),
                *(
                    [
                        gls_request.ShipmentServiceType(
                            Service=gls_request.ServiceType(
                                ServiceName=provider_units.time_definite_service_name(
                                    options.gls_time_definite_service.state,
                                ),
                            ),
                        )
                    ]
                    if options.gls_time_definite_service.state
                    else []
                ),
                *(
                    [
                        gls_request.ShipmentServiceType(
                            Deposit=gls_request.DepositType(
                                ServiceName=options.gls_deposit_service.code,
                                PlaceOfDeposit=options.gls_deposit_description.state,
                            ),
                        )
                    ]
                    if options.gls_deposit_service.state
                    else []
                ),
                *(
                    [
                        gls_request.ShipmentServiceType(
                            ShopDelivery=gls_request.ShopDeliveryType(
                                ServiceName=options.gls_shop_delivery.code,
                                ParcelShopID=options.gls_shop_id.state,
                            ),
                        )
                    ]
                    if (options.gls_shop_delivery.state or options.gls_shop_id.state)
                    else []
                ),
                *(
                    [
                        gls_request.ShipmentServiceType(
                            IdentPin=gls_request.IdentPinType(
                                ServiceName=options.gls_ident_pin_service.code,
                                PIN=options.gls_ident_pin.state,
                                Birthdate=options.gls_ident_pin_birthdate.state,
                            ),
                        )
                    ]
                    if options.gls_ident_pin_service.state
                    else []
                ),
                *(
                    [
                        gls_request.ShipmentServiceType(
                            Ident=gls_request.IdentType(
                                ServiceName=options.gls_ident_service.code,
                                Birthdate=options.gls_ident_birthdate.state,
                                Firstname=options.gls_ident_firstname.state,
                                Lastname=options.gls_ident_lastname.state,
                                Nationality=gls_request.NationalityType(
                                    CountryCode=options.gls_ident_nationality.state,
                                )
                                if options.gls_ident_nationality.state
                                else None,
                            ),
                        )
                    ]
                    if options.gls_ident_service.state
                    else []
                ),
                *(
                    [
                        gls_request.ShipmentServiceType(
                            DeliveryAtWork=gls_request.DeliveryAtWorkType(
                                ServiceName=options.gls_delivery_at_work_service.code,
                                RecipientName=(options.gls_dax_recipient_name.state or recipient.person_name),
                                AlternateRecipientName=options.gls_dax_alternate_recipient.state,
                                Building=options.gls_dax_building.state,
                                Floor=options.gls_dax_floor.state,
                                Room=options.gls_dax_room.state,
                                Phonenumber=recipient.phone_number,
                            ),
                        )
                    ]
                    if options.gls_delivery_at_work_service.state
                    else []
                ),
                *(
                    [
                        gls_request.ShipmentServiceType(
                            Intercompany=gls_request.ExchangeType(
                                ServiceName=options.gls_intercompany_service.code,
                                Address=gls_request.AddressType(
                                    Name1=return_address.company_name or return_address.person_name,
                                    Name2=return_address.person_name if return_address.company_name else None,
                                    Street=return_address.address_line1,
                                    StreetNumber=return_address.address_line2,
                                    ZIPCode=return_address.postal_code,
                                    City=return_address.city,
                                    CountryCode=return_address.country_code,
                                    ContactPerson=return_address.person_name,
                                    FixedLinePhonenumber=return_address.phone_number,
                                ),
                                NumberOfLabels=int(options.gls_intercompany_number_of_labels.state or 1),
                                ExpectedWeight=(
                                    float(options.gls_intercompany_expected_weight.state)
                                    if options.gls_intercompany_expected_weight.state
                                    else None
                                ),
                            ),
                        )
                    ]
                    if options.gls_intercompany_service.state
                    else []
                ),
                *(
                    [
                        gls_request.ShipmentServiceType(
                            Exchange=gls_request.ExchangeType(
                                ServiceName=options.gls_exchange_service.code,
                                Address=gls_request.AddressType(
                                    Name1=return_address.company_name or return_address.person_name,
                                    Name2=return_address.person_name if return_address.company_name else None,
                                    Street=return_address.address_line1,
                                    StreetNumber=return_address.address_line2,
                                    ZIPCode=return_address.postal_code,
                                    City=return_address.city,
                                    CountryCode=return_address.country_code,
                                    ContactPerson=return_address.person_name,
                                    FixedLinePhonenumber=return_address.phone_number,
                                ),
                                ExpectedWeight=(
                                    float(options.gls_exchange_expected_weight.state)
                                    if options.gls_exchange_expected_weight.state
                                    else None
                                ),
                            ),
                        )
                    ]
                    if options.gls_exchange_service.state
                    else []
                ),
                *(
                    [
                        gls_request.ShipmentServiceType(
                            PickAndShip=gls_request.PickAndType(
                                ServiceName=options.gls_pick_and_ship.code,
                                PickupDate=shipping_date_str,
                            ),
                        )
                    ]
                    if options.gls_pick_and_ship.state
                    else []
                ),
                *(
                    [
                        gls_request.ShipmentServiceType(
                            PickAndReturn=gls_request.PickAndType(
                                ServiceName=options.gls_pick_and_return.code,
                                PickupDate=shipping_date_str,
                            ),
                        )
                    ]
                    if options.gls_pick_and_return.state
                    else (
                        [
                            gls_request.ShipmentServiceType(
                                ShopReturn=gls_request.ShopReturnType(
                                    ServiceName=options.gls_shop_return.code,
                                    NumberOfLabels=1,
                                ),
                            )
                        ]
                        if (options.gls_shop_return.state or options.gls_return_enabled.state)
                        else []
                    )
                ),
            ],
        ),
        PrintingOptions=gls_request.PrintingOptionsType(
            ReturnLabels=gls_request.ReturnLabelsType(
                TemplateSet=settings.connection_config.template_name.state or "NONE",
                LabelFormat=label_format,
            ),
        ),
    )

    return lib.Serializable(request, lib.to_dict)
