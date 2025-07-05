import karrio.schemas.dhl_ecommerce_europe.rate_response as rating
import typing
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.dhl_ecommerce_europe.error as error
import karrio.providers.dhl_ecommerce_europe.utils as provider_utils
import karrio.providers.dhl_ecommerce_europe.units as provider_units


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    rates = [
        _extract_details(product, settings)
        for product in response.get("products", [])
    ]

    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    product = lib.to_object(rating.Product, data)
    
    # Handle totalPrice more robustly
    total_price = None
    if product.totalPrice:
        # Find TOTAL price type or use the first one
        for price_data in product.totalPrice:
            if isinstance(price_data, dict):
                if price_data.get("priceType") == "TOTAL":
                    total_price = lib.to_object(rating.TotalPrice, price_data)
                    break
            elif hasattr(price_data, 'priceType') and price_data.priceType == "TOTAL":
                total_price = price_data
                break
        
        # If no TOTAL found, use the first price
        if not total_price and product.totalPrice:
            first_price = product.totalPrice[0]
            if isinstance(first_price, dict):
                total_price = lib.to_object(rating.TotalPrice, first_price)
            else:
                total_price = first_price
    
    # Extract extra charges
    extra_charges = []
    if total_price and hasattr(total_price, 'breakdown') and total_price.breakdown:
        for charge_data in total_price.breakdown:
            if isinstance(charge_data, dict):
                charge = lib.to_object(rating.PriceBreakdown, charge_data)
            else:
                charge = charge_data
                
            extra_charges.append(models.ChargeDetails(
                name=charge.name,
                currency=charge.priceCurrency,
                amount=lib.to_money(charge.price),
            ))

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=product.productCode,
        total_charge=lib.to_money(total_price.price if total_price else 0.0),
        currency=(total_price.priceCurrency if total_price else "EUR"),
        transit_days=(
            (product.deliveryCapabilities.get('totalTransitDays') if isinstance(product.deliveryCapabilities, dict)
             else getattr(product.deliveryCapabilities, 'totalTransitDays', None))
            if product.deliveryCapabilities else None
        ),
        extra_charges=extra_charges,
        meta=dict(
            service_name=product.name,
            product_code=product.productCode,
            local_product_code=product.localProductCode,
            delivery_capabilities=(
                lib.to_dict(product.deliveryCapabilities) 
                if product.deliveryCapabilities else None
            ),
        ),
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    services = payload.services or [provider_units.ShippingService.V01PAK.name]
    
    # Use the first service for the request (DHL API typically handles one service per request)
    service_code = next(
        (provider_units.ShippingService[s].value for s in services if s in provider_units.ShippingService.__members__),
        provider_units.ShippingService.V01PAK.value
    )

    planned_shipping_date = lib.fdatetime(
        datetime.datetime.now() + datetime.timedelta(days=1),
        output_format="%Y-%m-%dT%H:%M:%S"
    )

    request = {
        "plannedShippingDateAndTime": planned_shipping_date,
        "pickup": {
            "typeCode": "business",
            "accounts": [
                {
                    "typeCode": "shipper",
                    "number": settings.account_number or "123456789",
                }
            ],
            "address": {
                "postalCode": shipper.postal_code,
                "cityName": shipper.city,
                "countryCode": shipper.country_code,
            },
        },
        "productCode": service_code,
        "accounts": [
            {
                "typeCode": "shipper",
                "number": settings.account_number or "123456789",
            }
        ],
        "customerDetails": {
            "shipperDetails": {
                "postalAddress": {
                    "postalCode": shipper.postal_code,
                    "cityName": shipper.city,
                    "countryCode": shipper.country_code,
                }
            },
            "receiverDetails": {
                "postalAddress": {
                    "postalCode": recipient.postal_code,
                    "cityName": recipient.city,
                    "countryCode": recipient.country_code,
                }
            },
        },
        "packages": [
            {
                "weight": package.weight.KG,
                "dimensions": {
                    "length": package.length.CM,
                    "width": package.width.CM,
                    "height": package.height.CM,
                },
            }
            for package in packages
        ],
    }

    return lib.Serializable(request, lib.to_dict) 
