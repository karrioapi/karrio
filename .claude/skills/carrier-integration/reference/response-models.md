# Response Models Reference

All unified response models from `karrio.core.models`. Every provider function must return instances of these models.

## Import

```python
from karrio.core.models import (
    RateDetails, ChargeDetails,
    TrackingDetails, TrackingEvent, TrackingInfo, Images,
    ShipmentDetails, Documents,
    PickupDetails,
    ConfirmationDetails,
    ManifestDetails, ManifestDocument,
    AddressValidationDetails,
    DocumentUploadDetails, DocumentDetails,
    Message,
)
```

## RateDetails

```python
RateDetails(
    carrier_name=settings.carrier_name,
    carrier_id=settings.carrier_id,
    service="carrier_express",           # Karrio service name (from ShippingService enum)
    total_charge=lib.to_money(25.99),
    currency="USD",
    transit_days=2,
    extra_charges=[
        ChargeDetails(name="Fuel Surcharge", amount=3.50, currency="USD"),
        ChargeDetails(name="Base Charge", amount=22.49, currency="USD"),
    ],
    meta=dict(service_name="Express Delivery"),  # Optional carrier metadata
)
```

## TrackingDetails

```python
TrackingDetails(
    carrier_name=settings.carrier_name,
    carrier_id=settings.carrier_id,
    tracking_number="1Z999AA10123456784",
    status="in_transit",                 # Normalized status code
    delivered=False,
    estimated_delivery=lib.fdate("2024-01-20"),
    events=[
        TrackingEvent(
            date=lib.fdate("2024-01-15"),
            time=lib.ftime("14:30:00"),
            description="Package in transit",
            location="New York, NY",
            code="IT",                   # Carrier-specific code
        ),
    ],
    info=TrackingInfo(
        carrier_tracking_link="https://track.carrier.com/1Z999AA10123456784",
        shipping_date=lib.fdate("2024-01-10"),
        signed_by="John Doe",
    ),
    images=Images(
        delivery_image="base64...",
        signature_image="base64...",
    ),
)
```

**Normalized tracking statuses**: `pending`, `in_transit`, `out_for_delivery`, `delivered`, `ready_for_pickup`, `delivery_failed`, `on_hold`, `unknown`

## ShipmentDetails

```python
ShipmentDetails(
    carrier_name=settings.carrier_name,
    carrier_id=settings.carrier_id,
    tracking_number="1Z999AA10123456784",
    shipment_identifier="SHIP123456",    # Carrier's shipment ID
    label_type="PDF",                    # PDF, ZPL, PNG
    docs=Documents(label="base64_encoded_label_content"),
    meta=dict(
        carrier_tracking_link="https://...",
        tracking_numbers=["1Z999..."],   # For multi-piece
    ),
)
```

## PickupDetails

```python
PickupDetails(
    carrier_name=settings.carrier_name,
    carrier_id=settings.carrier_id,
    confirmation_number="PU123456",
    pickup_date="2024-01-20",
    pickup_charge=ChargeDetails(name="Pickup", amount=5.00, currency="USD"),
    closing_time="17:00",
    ready_time="09:00",
)
```

## ConfirmationDetails (Cancel Operations)

```python
ConfirmationDetails(
    carrier_name=settings.carrier_name,
    carrier_id=settings.carrier_id,
    success=True,
    operation="Cancel Shipment",         # Or "Cancel Pickup"
)
```

## ManifestDetails

```python
ManifestDetails(
    carrier_name=settings.carrier_name,
    carrier_id=settings.carrier_id,
    doc=ManifestDocument(manifest="base64_encoded_manifest"),
    meta=dict(manifest_id="MAN123"),
)
```

## AddressValidationDetails

```python
AddressValidationDetails(
    carrier_name=settings.carrier_name,
    carrier_id=settings.carrier_id,
    success=True,
    complete_address=models.Address(
        address_line1="123 Main St",
        city="New York",
        state_code="NY",
        postal_code="10001",
        country_code="US",
    ),
)
```

## DocumentUploadDetails

```python
DocumentUploadDetails(
    carrier_name=settings.carrier_name,
    carrier_id=settings.carrier_id,
    documents=[
        DocumentDetails(
            doc_id="DOC123",
            file_name="invoice.pdf",
        ),
    ],
)
```

## Message (Errors/Warnings)

```python
Message(
    carrier_name=settings.carrier_name,
    carrier_id=settings.carrier_id,
    code="INVALID_POSTAL_CODE",
    message="The postal code format is invalid",
    level="error",           # "error", "warning", or "info"
    details={"field": "recipient.postal_code"},
)
```

## Return Type Convention

All parse functions return a tuple: `Tuple[List[ResultType], List[Message]]`

```python
def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    rates = [_extract_details(r, settings) for r in response.get("rates", [])]
    return rates, messages
```
