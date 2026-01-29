import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.ups.error as error
import karrio.providers.ups.utils as provider_utils
import karrio.providers.ups.units as provider_units
import karrio.schemas.ups.pickup_request as ups
import karrio.schemas.ups.pickup_response as ups_response


def parse_pickup_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[models.PickupDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    pickup = _extract_details(response, settings) if response.get("PickupCreationResponse") else None

    return pickup, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.PickupDetails:
    response = lib.to_object(ups_response.PickupCreationResponseType, data.get("PickupCreationResponse", {}))
    rate_result = response.RateResult

    return models.PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=response.PRN,
        pickup_charge=(
            models.ChargeDetails(
                name="Pickup Charge",
                amount=lib.to_decimal(rate_result.GrandTotalOfAllCharge),
                currency=rate_result.CurrencyCode,
            )
            if rate_result and rate_result.GrandTotalOfAllCharge
            else None
        ),
        meta=dict(
            rate_type=rate_result.RateType if rate_result else None,
            weekend_service_territory=response.WeekendServiceTerritoryIndicator,
        ),
    )


def pickup_request(
    payload: models.PickupRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    # UPS only supports one-time (on-call) pickups via API
    # Daily/recurring pickups require account setup through UPS directly
    pickup_type = getattr(payload, "pickup_type", "one_time") or "one_time"
    if pickup_type not in ("one_time", None):
        raise lib.exceptions.FieldError({
            "pickup_type": f"UPS only supports 'one_time' pickups via API. Received: '{pickup_type}'. "
            "For daily/recurring pickups, please contact UPS to set up a regular pickup schedule."
        })

    address = lib.to_address(payload.address)
    packages = lib.to_packages(payload.parcels)
    options = lib.to_shipping_options(payload.options or {})
    weight = packages.weight
    weight_unit_name = weight.unit or "LB"
    weight_unit = provider_units.WeightUnit[weight_unit_name].value

    request = ups.PickupCreationRequestWrapperType(
        PickupCreationRequest=ups.PickupCreationRequestType(
            Request=ups.RequestType(
                SubVersion="2409",
                TransactionReference=ups.TransactionReferenceType(
                    CustomerContext="Pickup Request",
                ),
            ),
            RatePickupIndicator="Y",
            Shipper=(
                ups.ShipperType(
                    Account=ups.AccountType(
                        AccountNumber=settings.account_number,
                        AccountCountryCode=settings.account_country_code or address.country_code,
                    ),
                )
                if settings.account_number
                else None
            ),
            PickupDateInfo=ups.PickupDateInfoType(
                CloseTime=lib.ftime(payload.closing_time, current_format="%H:%M", output_format="%H%M") or "1800",
                ReadyTime=lib.ftime(payload.ready_time, current_format="%H:%M", output_format="%H%M") or "0800",
                PickupDate=lib.fdatetime(payload.pickup_date, current_format="%Y-%m-%d", output_format="%Y%m%d"),
            ),
            PickupAddress=ups.PickupAddressType(
                CompanyName=address.company_name or address.person_name or "N/A",
                ContactName=address.person_name or address.company_name or "N/A",
                AddressLine=address.street,
                Room=None,
                Floor=None,
                City=address.city,
                StateProvince=address.state_code,
                PostalCode=address.postal_code,
                CountryCode=address.country_code,
                ResidentialIndicator="Y" if address.residential else "N",
                PickupPoint=payload.package_location,
                Phone=ups.PhoneType(
                    Number=address.phone_number or "0000000000",
                    Extension=None,
                ),
            ),
            AlternateAddressIndicator="Y",
            PickupPiece=[
                ups.PickupPieceType(
                    ServiceCode=options.ups_pickup_service_code.state or "001",
                    Quantity=str(len(packages) or 1),
                    DestinationCountryCode=address.country_code,
                    ContainerCode="01",
                )
            ],
            TotalWeight=ups.TotalWeightType(
                Weight=str(weight[weight_unit_name] or 1.0),
                UnitOfMeasurement=weight_unit,
            ),
            OverweightIndicator="Y" if (weight.LB or 0) > 70 else "N",
            PaymentMethod="01" if settings.account_number else "00",
            SpecialInstruction=payload.instruction[:57] if payload.instruction else None,
            Notification=ups.NotificationType(
                ConfirmationEmailAddress=address.email,
            ) if address.email else None,
        ),
    )

    return lib.Serializable(request, lib.to_dict)
