"""Example: Duties & Insurance Implementation Patterns

This example demonstrates implementation patterns for:
1. Duties/Taxes Calculation (landed cost)
2. Insurance Application
"""

# =============================================================================
# DUTIES/TAXES CALCULATION IMPLEMENTATION
# =============================================================================

# === FILE: karrio/providers/[carrier]/duties.py ===

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.[carrier].error as error
import karrio.providers.[carrier].utils as provider_utils
import karrio.schemas.[carrier].duties_request as carrier_req
import karrio.schemas.[carrier].duties_response as carrier_res


def parse_duties_calculation_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.DutiesCalculationDetails, typing.List[models.Message]]:
    """Parse duties calculation response."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    details = (
        _extract_details(response, settings)
        if not any(messages)
        else None
    )
    
    return details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.DutiesCalculationDetails:
    """Extract duties calculation details."""
    result = lib.to_object(carrier_res.DutiesResponseType, data)
    
    # Extract individual charges
    charges = []
    
    # Import duty
    if hasattr(result, 'importDuty') and result.importDuty:
        charges.append(
            models.ChargeDetails(
                name="Import Duty",
                amount=lib.to_money(result.importDuty),
                currency=result.currency if hasattr(result, 'currency') else "USD",
            )
        )
    
    # VAT/GST
    if hasattr(result, 'vat') and result.vat:
        charges.append(
            models.ChargeDetails(
                name="VAT",
                amount=lib.to_money(result.vat),
                currency=result.currency if hasattr(result, 'currency') else "USD",
            )
        )
    
    # Additional taxes
    if hasattr(result, 'additionalTaxes') and result.additionalTaxes:
        for tax in result.additionalTaxes:
            charges.append(
                models.ChargeDetails(
                    name=tax.name if hasattr(tax, 'name') else "Additional Tax",
                    amount=lib.to_money(tax.amount),
                    currency=tax.currency if hasattr(tax, 'currency') else "USD",
                )
            )
    
    # Brokerage/handling fees
    if hasattr(result, 'brokerageFee') and result.brokerageFee:
        charges.append(
            models.ChargeDetails(
                name="Brokerage Fee",
                amount=lib.to_money(result.brokerageFee),
                currency=result.currency if hasattr(result, 'currency') else "USD",
            )
        )
    
    # Calculate total
    total = lib.to_money(result.totalAmount) if hasattr(result, 'totalAmount') else sum(
        c.amount for c in charges if c.amount
    )
    
    return models.DutiesCalculationDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        total_charge=total,
        currency=result.currency if hasattr(result, 'currency') else "USD",
        charges=charges,
        meta=dict(
            calculation_id=result.calculationId if hasattr(result, 'calculationId') else None,
            hs_codes_used=[
                item.hsCode for item in (result.items or [])
                if hasattr(item, 'hsCode')
            ] if hasattr(result, 'items') else None,
            landed_cost=lib.to_money(result.landedCost) if hasattr(result, 'landedCost') else None,
        ),
    )


def duties_calculation_request(
    payload: models.DutiesCalculationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create duties calculation request."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    customs = lib.to_customs_info(payload.customs)
    
    request = carrier_req.DutiesRequestType(
        # Shipment reference
        shipmentId=payload.shipment_identifier,
        # Origin
        originCountry=shipper.country_code,
        # Destination (duties apply to import country)
        destinationCountry=recipient.country_code,
        destinationPostalCode=recipient.postal_code,
        # Items for duty calculation
        items=[
            carrier_req.DutyItemType(
                description=item.description,
                hsCode=item.hs_code,
                quantity=item.quantity,
                value=item.value_amount,
                weight=item.weight,
                originCountry=item.origin_country or shipper.country_code,
                currency=item.value_currency or "USD",
            )
            for item in customs.commodities
        ],
        # Shipping charges (included in landed cost)
        shippingCost=lib.to_money(payload.shipping_charge.amount) if payload.shipping_charge else None,
        insuranceCost=lib.to_money(payload.insurance_charge.amount) if payload.insurance_charge else None,
        # Currency preference
        currency=payload.options.get("currency", "USD"),
        # Incoterm affects who pays duties
        incoterm=customs.incoterm or "DDP",
    )
    
    return lib.Serializable(request, lib.to_dict)


# === Proxy method ===
"""
def calculate_duties(self, request: lib.Serializable) -> lib.Deserializable[str]:
    response = lib.request(
        url=f"{self.settings.server_url}/v1/duties/calculate",
        data=lib.to_json(request.serialize()),
        trace=self.trace_as("json"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.settings.api_key}",
        },
    )
    return lib.Deserializable(response, lib.to_dict)
"""


# =============================================================================
# INSURANCE IMPLEMENTATION
# =============================================================================

# === FILE: karrio/providers/[carrier]/insurance/__init__.py ===

from karrio.providers.[carrier].insurance.apply import (
    parse_insurance_response,
    insurance_request,
)


# === FILE: karrio/providers/[carrier]/insurance/apply.py ===

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.[carrier].error as error
import karrio.providers.[carrier].utils as provider_utils
import karrio.schemas.[carrier].insurance_request as carrier_req
import karrio.schemas.[carrier].insurance_response as carrier_res


def parse_insurance_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.InsuranceDetails, typing.List[models.Message]]:
    """Parse insurance application response."""
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    
    details = (
        _extract_details(response, settings)
        if not any(messages)
        else None
    )
    
    return details, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.InsuranceDetails:
    """Extract insurance details from response."""
    result = lib.to_object(carrier_res.InsuranceResponseType, data)
    
    # Extract fees/premiums
    fees = []
    
    # Insurance premium
    if hasattr(result, 'premium') and result.premium:
        fees.append(
            models.ChargeDetails(
                name="Insurance Premium",
                amount=lib.to_money(result.premium),
                currency=result.currency if hasattr(result, 'currency') else "USD",
            )
        )
    
    # Service fee (some providers charge separately)
    if hasattr(result, 'serviceFee') and result.serviceFee:
        fees.append(
            models.ChargeDetails(
                name="Service Fee",
                amount=lib.to_money(result.serviceFee),
                currency=result.currency if hasattr(result, 'currency') else "USD",
            )
        )
    
    return models.InsuranceDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        fees=fees,
        meta=dict(
            policy_id=result.policyId if hasattr(result, 'policyId') else None,
            policy_number=result.policyNumber if hasattr(result, 'policyNumber') else None,
            coverage_amount=lib.to_money(result.coverageAmount) if hasattr(result, 'coverageAmount') else None,
            coverage_currency=result.currency if hasattr(result, 'currency') else None,
            provider=result.provider if hasattr(result, 'provider') else None,
            terms_url=result.termsUrl if hasattr(result, 'termsUrl') else None,
            certificate_url=result.certificateUrl if hasattr(result, 'certificateUrl') else None,
        ),
    )


def insurance_request(
    payload: models.InsuranceRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    """Create insurance application request."""
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    
    # Use lib.to_packages for parcel processing if list
    package = payload.parcel
    
    request = carrier_req.InsuranceRequestType(
        # Shipment reference
        shipmentId=payload.shipment_identifier,
        # Coverage details
        coverageAmount=payload.amount,
        currency=payload.currency,
        # Origin
        originAddress=carrier_req.AddressType(
            countryCode=shipper.country_code,
            city=shipper.city,
            postalCode=shipper.postal_code,
        ),
        # Destination
        destinationAddress=carrier_req.AddressType(
            countryCode=recipient.country_code,
            city=recipient.city,
            postalCode=recipient.postal_code,
        ),
        # Package details (for risk assessment)
        packageWeight=package.weight,
        packageWeightUnit=package.weight_unit,
        packageDescription=package.description or package.content,
        # Insurance provider preference (if multiple available)
        provider=payload.provider,
        # Reference
        reference=payload.reference,
    )
    
    return lib.Serializable(request, lib.to_dict)


# === Proxy method ===
"""
def apply_insurance(self, request: lib.Serializable) -> lib.Deserializable[str]:
    response = lib.request(
        url=f"{self.settings.server_url}/v1/insurance/apply",
        data=lib.to_json(request.serialize()),
        trace=self.trace_as("json"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.settings.api_key}",
        },
    )
    return lib.Deserializable(response, lib.to_dict)
"""


# =============================================================================
# MAPPER METHODS
# =============================================================================

"""
# === FILE: karrio/mappers/[carrier]/mapper.py (duties/insurance section) ===

# Add to Mapper class:

def create_duties_calculation_request(
    self, payload: models.DutiesCalculationRequest
) -> lib.Serializable:
    return provider.duties_calculation_request(payload, self.settings)

def parse_duties_calculation_response(
    self, response: lib.Deserializable[str]
) -> typing.Tuple[models.DutiesCalculationDetails, typing.List[models.Message]]:
    return provider.parse_duties_calculation_response(response, self.settings)

def create_insurance_request(
    self, payload: models.InsuranceRequest
) -> lib.Serializable:
    return provider.insurance_request(payload, self.settings)

def parse_insurance_response(
    self, response: lib.Deserializable[str]
) -> typing.Tuple[models.InsuranceDetails, typing.List[models.Message]]:
    return provider.parse_insurance_response(response, self.settings)
"""


# =============================================================================
# PROVIDER __init__.py EXPORTS
# =============================================================================

"""
# === FILE: karrio/providers/[carrier]/__init__.py ===

# Add exports for duties and insurance:

from karrio.providers.[carrier].duties import (
    parse_duties_calculation_response,
    duties_calculation_request,
)
from karrio.providers.[carrier].insurance import (
    parse_insurance_response,
    insurance_request,
)
"""


# =============================================================================
# PLUGIN METADATA
# =============================================================================

"""
# === FILE: karrio/plugins/[carrier]/__init__.py ===

# Ensure capabilities are declared:

METADATA = metadata.PluginMetadata(
    id="carrier",
    label="Carrier Name",
    # ... other fields ...
    
    # Capabilities are auto-detected from mapper methods, but can be explicit:
    # The presence of create_duties_calculation_request enables 'duties' capability
    # The presence of create_insurance_request enables 'insurance' capability
)
"""


# =============================================================================
# TEST PATTERNS
# =============================================================================

"""
# === Duties Test ===
class TestCarrierDuties(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.DutiesRequest = models.DutiesCalculationRequest(**DutiesPayload)

    def test_create_duties_request(self):
        request = gateway.mapper.create_duties_calculation_request(self.DutiesRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), DutiesRequest)

    def test_parse_duties_response(self):
        with patch("karrio.mappers.carrier.proxy.lib.request") as mock:
            mock.return_value = DutiesResponse
            # Note: Duties uses different karrio SDK method
            parsed_response = gateway.mapper.parse_duties_calculation_response(
                lib.Deserializable(DutiesResponse, lib.to_dict)
            )
            print(f"Parsed response: {lib.to_dict(parsed_response)}")
            self.assertListEqual(lib.to_dict(parsed_response), ParsedDutiesResponse)

DutiesPayload = {
    "shipment_identifier": "SHIP123",
    "shipper": {
        "country_code": "US",
        "postal_code": "10001",
        "city": "New York",
        "state_code": "NY",
    },
    "recipient": {
        "country_code": "GB",
        "postal_code": "SW1A 1AA",
        "city": "London",
    },
    "customs": {
        "commodities": [
            {
                "description": "Electronic device",
                "hs_code": "8471.30",
                "quantity": 1,
                "value_amount": 500.00,
                "value_currency": "USD",
                "weight": 0.5,
                "origin_country": "CN",
            }
        ],
        "incoterm": "DDP",
    },
}


# === Insurance Test ===
class TestCarrierInsurance(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.InsuranceRequest = models.InsuranceRequest(**InsurancePayload)

    def test_create_insurance_request(self):
        request = gateway.mapper.create_insurance_request(self.InsuranceRequest)
        print(f"Generated request: {lib.to_dict(request.serialize())}")
        self.assertEqual(lib.to_dict(request.serialize()), InsuranceRequest)

InsurancePayload = {
    "shipment_identifier": "SHIP123",
    "amount": 1000.00,
    "currency": "USD",
    "shipper": {
        "country_code": "US",
        "city": "New York",
        "postal_code": "10001",
    },
    "recipient": {
        "country_code": "GB",
        "city": "London",
        "postal_code": "SW1A 1AA",
    },
    "parcel": {
        "weight": 2.5,
        "weight_unit": "KG",
        "description": "Electronics",
    },
}
"""
