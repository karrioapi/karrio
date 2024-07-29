"""Karrio USPS manifest API implementation."""

import karrio.schemas.usps_international.scan_form_request as usps
import karrio.schemas.usps_international.scan_form_response as manifest

import time
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.usps_international.error as error
import karrio.providers.usps_international.utils as provider_utils
import karrio.providers.usps_international.units as provider_units


def parse_manifest_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ManifestDetails, typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    details = lib.identity(
        _extract_details(response, settings)
        if response.get("SCANFormImage") is not None
        else None
    )

    return details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ManifestDetails:
    details = lib.to_object(manifest.ScanFormResponseType, data)
    image = data.get("SCANFormImage")

    return models.ManifestDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_id,
        doc=models.ManifestDocument(manifest=image),
        meta=dict(
            manifestNumber=details.SCANFormMetadata.manifestNumber,
            trackingNumbers=details.SCANFormMetadata.trackingNumbers,
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
            # fmt: off
            {
                "shipment_date": lib.OptionEnum("shipment_date"),
                "usps_ignore_bad_address": lib.OptionEnum("ignoreBadAddress", bool),
                "usps_overwrite_mailing_date": lib.OptionEnum("overwriteMailingDate", bool),
                "usps_destination_entry_facility_type": lib.OptionEnum("destinationEntryFacilityType", str),
            },
            # fmt: on
        ),
    )

    # map data to convert karrio model to usps specific type
    request = usps.ScanFormRequestType(
        form="5630",
        imageType="PDF",
        labelType="8.5x11LABEL",
        mailingDate=lib.fdate(options.shipment_date.state or time.strftime("%Y-%m-%d")),
        overwriteMailingDate=options.usps_overwrite_mailing_date.state or False,
        entryFacilityZIPCode=address.postal_code,
        destinationEntryFacilityType=lib.identity(
            options.usps_destination_entry_facility_type.state or "NONE"
        ),
        shipment=usps.ShipmentType(
            trackingNumbers=payload.shipment_identifiers,
        ),
        fromAddress=usps.FromAddressType(
            ignoreBadAddress=options.usps_ignore_bad_address.state or False,
            streetAddress=address.address_line1,
            secondaryAddress=address.address_line2,
            city=address.city,
            state=address.state,
            ZIPCode=lib.to_zip5(address.postal_code) or "",
            ZIPPlus4=lib.to_zip4(address.postal_code) or "",
            urbanization=None,
            firstName=lib.identity(
                lib.failsafe(lambda: (address.person_name or "").split(" ")[0]) or ""
            ),
            lastName=lib.failsafe(lambda: (address.person_name or "").split(" ")[1]),
            firm=address.company_name,
        ),
    )

    return lib.Serializable(request, lib.to_dict)
