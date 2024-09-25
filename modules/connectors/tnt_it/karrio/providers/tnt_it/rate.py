"""Karrio TNT Connect Italy rating API implementation."""

import karrio.schemas.tnt_it.rating as tnt

import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.tnt_it.error as error
import karrio.providers.tnt_it.utils as provider_utils
import karrio.providers.tnt_it.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()

    messages = error.parse_error_response(response, settings)
    rates = [_extract_details(rate, settings) for rate in response]

    return rates, messages


def _extract_details(
    data: lib.Element,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    details = None  # parse carrier rate type

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service="",  # extract service from rate
        total_charge=lib.to_money(0.0),  # extract the rate total rate cost
        currency="",  # extract the rate pricing currency
        transit_days=0,  # extract the rate transit days
        meta=dict(
            service_name="",  # extract the rate service human readable name
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    services = lib.to_services(payload.services, provider_units.ShippingService)
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    # map data to convert karrio model to tnt_it specific type
    request = tnt.Document(
        Application="MYSHP",
        Version="3.0",
        Login=tnt.LoginType(
            Customer=settings.customer,
            User=settings.username,
            Password=settings.password,
            LangID="IT",
        ),
        ApplicationFunction="priceCheck",
        Details=tnt.DetailsType(
            AccountNo=settings.account_number,
            Package=tnt.PackageType(
                Items=[
                    tnt.ItemsType(
                        ItemSeqNo=index,
                        Type=provider_units.PackagingType.map(package.packaging).value,
                        INumber=str(package.quantity),
                        IWeight=str(package.weight.KG),
                        Length=str(package.length.CM),
                        Height=str(package.height.CM),
                        Width=str(package.width.CM),
                    )
                    for index, package in enumerate(packages, start=1)
                ]
            ),
            Common=tnt.CommonType(
                ContactName=shipper.person_name,
                Service=services[0].value if services else None,
                Insurance=str(payload.insurance.amount) if payload.insurance else None,
                InsuranceCurrency=(
                    payload.insurance.currency if payload.insurance else None
                ),
                SenderReference=payload.reference,
                Payment="0",  # Assuming sender pays
                Instructions=payload.options.get("instructions"),
                SpecialGoods=(
                    "Y"
                    if any(
                        option in payload.options
                        for option in ["dangerous_goods", "dry_ice"]
                    )
                    else "N"
                ),
            ),
            Domestic=(
                tnt.DomesticType(
                    COD=(
                        tnt.CODType(
                            Amount=str(payload.payment.amount),
                            Currency=payload.payment.currency,
                            SenderComm="Y",
                            SenderRefund="N",
                        )
                        if payload.payment
                        else None
                    ),
                    OperationalOptions=tnt.OperationalOptionsType(
                        Option="1"  # Assuming default option
                    ),
                )
                if recipient.country_code == shipper.country_code
                else None
            ),
            International=(
                tnt.InternationalType(
                    GoodsValue=str(payload.customs.declared_value),
                    GoodsValueCurrency=payload.customs.declared_value_currency,
                    Priority="Y" if "priority" in payload.options else "N",
                    FDA="Y" if "fda" in payload.options else "N",
                    DryIce="Y" if "dry_ice" in payload.options else "N",
                )
                if recipient.country_code != shipper.country_code
                else None
            ),
            CheckPriceEnabled="Y",
        ),
        Shipment=tnt.ShipmentType(
            Date=payload.shipment_date.strftime("%d.%m.%Y"),
            Receiver=tnt.ReceiverType(
                Address=recipient.address_line1,
                CompanyName=recipient.company_name,
                ReceiverAccountNo=recipient.account_number,
                Town=recipient.city,
                ProvinceState=recipient.state_code,
                Postcode=recipient.postal_code,
                CountryID=recipient.country_code,
            ),
        ),
        ExtraCee="N",  # Assuming not an extra EU country
    )

    return lib.Serializable(request, lib.to_xml)
