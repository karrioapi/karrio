import karrio.schemas.canadapost.manifest as canadapost
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.canadapost.error as error
import karrio.providers.canadapost.utils as provider_utils
import karrio.providers.canadapost.units as provider_units


def parse_manifest_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ManifestDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    links = lib.find_element("link", response)

    messages = error.parse_error_response(response, settings)
    details = (
        _extract_details(links, settings, _response.ctx) if len(links) > 0 else None
    )

    return details, messages


def _extract_details(
    links: typing.List[lib.Element],
    settings: provider_utils.Settings,
    ctx: dict = None,
) -> models.ManifestDetails:
    manifest = lib.bundle_base64(ctx["files"])

    return models.ManifestDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_id,
        doc=models.ManifestDocument(manifest=manifest),
        meta=dict(
            group_ids=ctx["group_ids"],
            links=[_.get("href") for _ in links],
        ),
    )


def manifest_request(
    payload: models.ManifestRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    address = lib.to_address(payload.address)
    options = lib.units.Options(
        payload.options,
        option_type=lib.units.create_enum(
            "ManifestOptions",
            {
                "group_ids": lib.OptionEnum("group_ids", list),
                "shipments": lib.OptionEnum("shipments", lib.to_dict),
                "method_of_payment": lib.OptionEnum("method_of_payment"),
                "shipping_point_id": lib.OptionEnum("shipping_point_id"),
                "excluded_shipments": lib.OptionEnum("excluded_shipments", list),
                "detailed_manifests": lib.OptionEnum("detailed_manifests", bool),
                "cpc_pickup_indicator": lib.OptionEnum("cpc_pickup_indicator", bool),
                "requested_shipping_point": lib.OptionEnum("requested_shipping_point"),
            },
        ),
    )
    group_ids = lib.identity(
        options.group_ids.state
        or [
            *set(
                (
                    _.get("meta", {}).get("group_id")
                    for _ in (options.shipments.state or [])
                    if lib.text(_.get("meta", {}).get("group_id")) is not None
                )
            )
        ]
    )
    retrieve_shipments = len(group_ids) == 0

    request = canadapost.ShipmentTransmitSetType(
        customer_request_id=None,
        group_ids=canadapost.GroupIDListType(group_id=["[GROUP_IDS]"]),
        cpc_pickup_indicator=options.cpc_pickup_indicator.state,
        requested_shipping_point=provider_utils.format_ca_postal_code(
            options.requested_shipping_point.state or address.postal_code
        ),
        shipping_point_id=options.shipping_point_id.state,
        detailed_manifests=lib.identity(
            True
            if options.detailed_manifests.state is not False
            else options.detailed_manifests.state
        ),
        method_of_payment=(options.method_of_payment.state or "Account"),
        manifest_address=canadapost.ManifestAddressType(
            manifest_name=address.contact,
            manifest_company=address.company_name or address.contact or "N/A",
            phone_number=address.phone_number or "000 000 0000",
            address_details=canadapost.AddressDetailsType(
                address_line_1=address.address_line1,
                address_line_2=address.address_line2,
                city=address.city,
                prov_state=address.state_code,
                country_code=address.country_code,
                postal_zip_code=address.postal_code,
            ),
        ),
        customer_reference=lib.text(payload.reference, max=12),
        excluded_shipments=lib.identity(
            canadapost.ExcludedShipmentsType(
                shipment_id=options.excluded_shipments.state.slit(",")
            )
            if options.excluded_shipments.state
            else None
        ),
    )

    return lib.Serializable(
        request,
        lambda _: lib.to_xml(
            request,
            name_="transmit-set",
            namespacedef_='xmlns="http://www.canadapost.ca/ws/manifest-v8"',
        ),
        dict(
            group_ids=group_ids,
            retrieve_shipments=retrieve_shipments,
            shipment_identifiers=payload.shipment_identifiers,
        ),
    )
