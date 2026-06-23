"""DHL Freight shipment booking — ``sendtransportinstruction``.

Maps the karrio ``ShipmentRequest`` to/from the generated
``karrio.schemas.dhl_freight`` typed DTOs. See SPECS.md for the wire-shape
contract, the party model (billing_address → Consignor, divergent shipper →
Pickup), and the Print-API label follow-up.
"""

import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.dhl_freight.error as error
import karrio.providers.dhl_freight.units as provider_units
import karrio.providers.dhl_freight.utils as provider_utils
import karrio.schemas.dhl_freight.shipping_request as dhl_freight_req
import karrio.schemas.dhl_freight.shipping_response as dhl_freight_res


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> tuple[models.ShipmentDetails | None, list[models.Message]]:
    deserialized = _response.deserialize()
    # The proxy returns (booking, print) when the Print follow-up ran, else the
    # booking dict alone (PRD §6.3). Normalize to (booking, print_or_None).
    booking, print_doc = deserialized if isinstance(deserialized, tuple) else (deserialized, None)
    ctx = _response.ctx or {}

    messages = error.parse_error_response(booking, settings)
    has_shipment_id = booking.get("shipmentId") or booking.get("transportInstructionId")
    shipment = _extract_details(booking, print_doc, settings, ctx) if has_shipment_id else None

    return shipment, messages


def _extract_details(
    data: dict,
    print_doc: dict | None,
    settings: provider_utils.Settings,
    ctx: dict,
) -> models.ShipmentDetails:
    response = lib.to_object(dhl_freight_res.ShippingResponseType, data)
    tracking_number = str(response.shipmentId or response.transportInstructionId or "")
    piece_identifiers = [
        str(lp.licensePlate or lp.sscc or lp.pieceId or "")
        for lp in (response.licensePlates or [])
        if (lp.licensePlate or lp.sscc or lp.pieceId)
    ]
    # Base64 PDF from the Print API follow-up (when enabled + successful).
    # Field name is best-effort (unvalidated schema) — accept the common keys.
    label = (
        lib.failsafe(
            lambda: (
                (print_doc or {}).get("documents", [{}])[0].get("content")
                or (print_doc or {}).get("content")
                or (print_doc or {}).get("base64")
            )
        )
        or ""
    )

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        shipment_identifier=tracking_number,
        label_type="PDF" if label else None,
        docs=models.Documents(label=label),  # populated only via Print API — see SPECS.md
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(tracking_number),
            tracking_numbers=[tracking_number],
            shipment_identifiers=[tracking_number, *piece_identifiers],
            license_plates=piece_identifiers,
            product_code=ctx.get("product_code"),
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    # Consignor = the freight-payer / legal sender: billing_address when given,
    # else the shipper. Pickup/Delivery (physical sites) are only added when
    # they diverge from the legal parties (PRD §6.2).
    consignor = lib.to_address(payload.billing_address) if payload.billing_address else shipper
    service = provider_units.ShippingService.map(payload.service).value_or_key
    service_code = provider_units.ShippingService.map(payload.service).name
    options = lib.to_shipping_options(payload.options, initializer=provider_units.shipping_options_initializer)
    customs = lib.to_customs_info(payload.customs, option_type=provider_units.CustomsOption, weight_unit="KG")
    packages = lib.to_packages(
        payload.parcels,
        required=["weight"],
        options=payload.options,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )

    # Freight-specific cargo units (pallet places, loading meters, stackable,
    # marks) ride on parcel.options — no first-class Parcel slot (PRD §6.1).
    # ADR dangerous goods come from parcel.options OR a parcel item's metadata
    # (commodity.metadata["dangerousGoods"]) — PRD §6.4.
    piece_options = [getattr(pkg.parcel, "options", None) or {} for pkg in packages]
    piece_adr = [
        o.get("dangerousGoods")
        or next(
            (
                it.metadata["dangerousGoods"]
                for it in (pkg.parcel.items or [])
                if (it.metadata or {}).get("dangerousGoods")
            ),
            None,
        )
        for pkg, o in zip(packages, piece_options, strict=False)
    ]
    has_dangerous_goods = any(piece_adr)
    temp = options.dhl_freight_temperature_controlled.state
    insurance = options.dhl_freight_insurance.state
    cod = options.dhl_freight_cash_on_delivery.state

    # Consignor account id is mandatory; Consignee id optional. Each resolves
    # from a per-shipment option, else the connection setting (PRD §6.2).
    consignor_account = options.dhl_freight_consignor_account.state or settings.connection_account_number
    consignee_account = options.dhl_freight_consignee_account.state or settings.connection_consignee_account_number

    # payerCode.code (incoterms): customs.options → shipping option → customs.incoterm
    # → connection default. payerCode.location resolves the same way. Tax refs:
    # customs.options → shipping option (§6.6/§6.7).
    payer_code = (
        customs.options.dhl_freight_payer_code.state
        or options.dhl_freight_payer_code.state
        or customs.incoterm
        or settings.connection_config.default_payer_code.state
        or "DAP"
    )
    payer_location = (
        customs.options.dhl_freight_payer_code_location.state
        or options.dhl_freight_payer_code_location.state
        or settings.connection_config.default_payer_location.state
        or ""
    )
    uit_number = customs.options.dhl_freight_uit_number.state or options.dhl_freight_uit_number.state
    ekaer_number = customs.options.dhl_freight_ekaer_number.state or options.dhl_freight_ekaer_number.state
    sent_number = customs.options.dhl_freight_sent_number.state or options.dhl_freight_sent_number.state

    # Party specs: Consignor + Consignee (mandatory); Pickup/Delivery only when
    # the physical site diverges from the legal party (key = country+postal+city).
    def _loc(a):
        return (a.country_code, a.postal_code, a.city)

    party_specs = [
        ("Consignor", consignor, consignor_account),
        ("Consignee", recipient, consignee_account),
    ]
    if _loc(shipper) != _loc(consignor):
        party_specs.append(("Pickup", shipper, None))

    request = dhl_freight_req.ShippingRequestType(
        id="",  # DHL assigns the id; client passes empty
        productCode=service,
        pickupDate=lib.fdatetime(
            payload.options.get("shipment_date") if isinstance(payload.options, dict) else None,
            try_formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ"],
            output_format="%Y-%m-%dT%H:%M:%S.000Z",
        ),
        requestedDeliveryDate=lib.fdatetime(
            payload.options.get("requested_delivery_date") if isinstance(payload.options, dict) else None,
            try_formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ"],
            output_format="%Y-%m-%dT%H:%M:%S.000Z",
        ),
        pickupInstruction=lib.text(options.dhl_freight_pickup_instruction.state, max=512),
        deliveryInstruction=lib.text(options.dhl_freight_delivery_instruction.state, max=512),
        totalNumberOfPieces=sum(int(o.get("numberOfPieces") or 1) for o in piece_options),
        totalWeight=lib.failsafe(lambda: float(packages.weight.KG)) or 0,
        totalVolume=round(
            sum(
                lib.failsafe(
                    lambda pkg=pkg, o=o: round(
                        (pkg.length.M * pkg.width.M * pkg.height.M) * int(o.get("numberOfPieces") or 1), 3
                    )
                )
                or 0
                for pkg, o in zip(packages, piece_options, strict=False)
            ),
            3,
        ),
        totalLoadingMeters=round(sum((o.get("loadingMeters") or 0) for o in piece_options), 3),
        totalPalletPlaces=sum((o.get("palletPlaces") or 0) for o in piece_options),
        goodsDescription=lib.text(
            payload.customs.content_description
            if payload.customs is not None
            else (packages[0].parcel.description if packages else None),
            max=255,
        ),
        goodsValue=lib.failsafe(
            lambda: float(payload.customs.duty.declared_value) if payload.customs and payload.customs.duty else None
        ),
        goodsValueCurrency=lib.failsafe(
            lambda: payload.customs.duty.currency if payload.customs and payload.customs.duty else None
        )
        or "EUR",
        references=[
            dhl_freight_req.ReferenceType(qualifier=qualifier, value=value)
            for qualifier, value in (
                ("CNR", options.dhl_freight_consignor_reference.state),
                ("CNZ", options.dhl_freight_consignee_reference.state),
                ("ORD", options.dhl_freight_order_reference.state),
                ("SHP", payload.reference),
            )
            if value
        ],
        payerCode=dhl_freight_req.PayerCodeType(code=payer_code, location=payer_location),
        # Consignor (billing/sender) + Consignee mandatory; Pickup/Delivery added
        # only when the physical site diverges (party_specs, PRD §6.2). `vat` is a
        # typed PartyVAT field; the tax id goes in vatEoriSocialSecurityNumber.
        parties=[
            dhl_freight_req.PartyType(
                id=account_id,
                type=ptype,
                name=lib.text(addr.company_name or addr.person_name, max=70),
                vatEoriSocialSecurityNumber=lib.text(addr.federal_tax_id or addr.state_tax_id, max=35),
                contactName=lib.text(addr.person_name, max=70),
                address=dhl_freight_req.AddressType(
                    street=lib.text(addr.address_line1, max=70),
                    additionalAddressInfo=lib.text(addr.address_line2, max=70),
                    cityName=lib.text(addr.city, max=40),
                    postalCode=lib.text(addr.postal_code, max=10),
                    countryCode=addr.country_code,
                ),
                phone=lib.text(addr.phone_number, max=25),
                email=lib.text(addr.email, max=80),
            )
            for ptype, addr, account_id in party_specs
        ],
        additionalServices=dhl_freight_req.AdditionalServicesType(
            after12Delivery=options.dhl_freight_after_12_delivery.state,
            availablePickupTime=options.dhl_freight_available_pickup_time.state,
            availableDeliveryTime=options.dhl_freight_available_delivery_time.state,
            preAdvice=options.dhl_freight_pre_advice.state,
            timeSlotBookingPickup=options.dhl_freight_time_slot_booking_pickup.state,
            timeSlotBookingDelivery=options.dhl_freight_time_slot_booking_delivery.state,
            tailLiftLoading=options.dhl_freight_tail_lift_loading.state,
            tailLiftUnloading=options.dhl_freight_tail_lift_unloading.state,
            sideLoadingPickup=options.dhl_freight_side_loading_pickup.state,
            sideUnloadingDelivery=options.dhl_freight_side_unloading_delivery.state,
            dropOffByConsignor=options.dhl_freight_drop_off_by_consignor.state,
            temperatureControlled=lib.to_object(dhl_freight_req.TemperatureControlledType, temp) if temp else None,
            insurance=lib.to_object(dhl_freight_req.InsuranceType, insurance) if insurance else None,
            cashOnDelivery=lib.to_object(dhl_freight_req.CashOnDeliveryType, cod) if cod else None,
            dangerousGoods=(True if has_dangerous_goods else options.dhl_freight_dangerous_goods.state),
        ),
        pieces=[
            dhl_freight_req.PieceType(
                id=[lib.text(pkg.parcel.reference_number)] if pkg.parcel.reference_number else [""],
                goodsType=lib.text(pkg.parcel.description, max=70),
                packageType=provider_units.PackagingType.map(pkg.packaging_type).value_or_key,
                marksAndNumbers=lib.text(o.get("marksAndNumbers"), max=45),
                numberOfPieces=int(o.get("numberOfPieces") or 1),
                weight=lib.failsafe(lambda pkg=pkg: float(pkg.weight.KG)),
                volume=lib.failsafe(
                    lambda pkg=pkg, o=o: round(
                        (pkg.length.M * pkg.width.M * pkg.height.M) * int(o.get("numberOfPieces") or 1), 3
                    )
                ),
                loadingMeters=o.get("loadingMeters") or 0,
                palletPlaces=o.get("palletPlaces") or 0,
                width=lib.failsafe(lambda pkg=pkg: float(pkg.width.CM)),
                height=lib.failsafe(lambda pkg=pkg: float(pkg.height.CM)),
                length=lib.failsafe(lambda pkg=pkg: float(pkg.length.CM)),
                stackable=bool(o.get("stackable", True)),
                dangerousGoods=(lib.to_object(dhl_freight_req.DangerousGoodsType, adr) if adr else None),
            )
            for pkg, o, adr in zip(packages, piece_options, piece_adr, strict=False)
        ],
        additionalInformation=[
            dhl_freight_req.AdditionalInformationType(code=code, stringValue=value)
            for code, value in (
                ("UIT_NUMBER", uit_number),
                ("EKAER_NUMBER", ekaer_number),
                ("SENT_NUMBER", sent_number),
            )
            if value
        ],
    )

    return lib.Serializable(
        request,
        lib.to_dict,
        dict(
            product_code=service_code or service,
            # Print (Labelling) follow-up config — read by the proxy (PRD §6.3).
            auto_print=bool(settings.connection_config.auto_print_documents.state),
            print_document_type=settings.connection_config.print_document_type.state or "label",
        ),
    )
