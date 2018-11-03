from pyups import (
    freight_ship as FShip, 
    package_ship as PShip
) 
from .interface import reduce, Tuple, List, Union, E, UPSMapperBase


class UPSMapperPartial(UPSMapperBase):

    def parse_freight_shipment_response(self, shipmentNode: 'XMLElement') -> E.ShipmentDetails:
        shipmentResponse = FShip.FreightShipResponse()
        shipmentResponse.build(shipmentNode)
        shipment = shipmentResponse.ShipmentResults
            
        return E.ShipmentDetails(
            carrier=self.client.carrier_name,
            tracking_numbers=[shipment.ShipmentNumber],
            total_charge=E.ChargeDetails(
                name="Shipment charge", 
                amount=shipment.TotalShipmentCharge.MonetaryValue,
                currency=shipment.TotalShipmentCharge.CurrencyCode
            ),
            charges=[
                E.ChargeDetails(
                    name=rate.Type.Code,
                    amount=rate.Factor.Value,
                    currency=rate.Factor.UnitOfMeasurement.Code
                ) for rate in shipment.Rate
            ],
            # shipment_date=,
            services=[shipment.Service.Code],
            documents=[image.GraphicImage for image in (shipment.Documents or [])],
            reference=E.ReferenceDetails(
                value=shipmentResponse.Response.TransactionReference.CustomerContext,
                type="CustomerContext"
            )
        )

    def parse_package_shipment_response(self, shipmentNode: 'XMLElement') -> E.ShipmentDetails:
        shipmentResponse = PShip.ShipmentResponse()
        shipmentResponse.build(shipmentNode)
        shipment = shipmentResponse.ShipmentResults

        if not shipment.NegotiatedRateCharges:
            total_charge = shipment.ShipmentCharges.TotalChargesWithTaxes or shipment.ShipmentCharges.TotalCharges
        else:
            total_charge = shipment.NegotiatedRateCharges.TotalChargesWithTaxes or shipment.NegotiatedRateCharges.TotalCharge

        return E.ShipmentDetails(
            carrier=self.client.carrier_name,
            tracking_numbers=[pkg.TrackingNumber for pkg in shipment.PackageResults],
            total_charge=E.ChargeDetails(
                name="Shipment charge", 
                amount=total_charge.MonetaryValue,
                currency=total_charge.CurrencyCode
            ),
            charges=[
                E.ChargeDetails(
                    name=charge.Code,
                    amount=charge.MonetaryValue,
                    currency=charge.CurrencyCode
                ) for charge in [
                    shipment.ShipmentCharges.TransportationCharges,
                    shipment.ShipmentCharges.ServiceOptionsCharges,
                    shipment.ShipmentCharges.BaseServiceCharge
                ] if charge is not None
            ],
            documents=[
                pkg.ShippingLabel.GraphicImage for pkg in (shipment.PackageResults or [])
            ],
            reference=E.ReferenceDetails(
                value=shipmentResponse.Response.TransactionReference.CustomerContext,
                type="CustomerContext"
            )
        )

