from karrio.server.core.serializers import *
from karrio.server.manager.serializers.address import (
    AddressSerializer,
    can_mutate_address,
)
from karrio.server.manager.serializers.commodity import (
    CommoditySerializer,
    can_mutate_commodity,
)
from karrio.server.manager.serializers.parcel import (
    ParcelSerializer,
    can_mutate_parcel,
)
from karrio.server.serializers import *

# Product is a proxy of Commodity - use the same serializer
ProductSerializer = CommoditySerializer
from karrio.server.manager.serializers.document import (
    DocumentUploadSerializer,
    can_upload_shipment_document,
)
from karrio.server.manager.serializers.manifest import (
    ManifestSerializer,
)
from karrio.server.manager.serializers.pickup import (
    PickupCancelData,
    PickupData,
    PickupUpdateData,
    can_mutate_pickup,
)
from karrio.server.manager.serializers.rate import RateSerializer
from karrio.server.manager.serializers.shipment import (
    PurchasedShipment,
    ShipmentCancelSerializer,
    ShipmentPurchaseData,
    ShipmentPurchaseSerializer,
    ShipmentRateData,
    ShipmentSerializer,
    ShipmentUpdateData,
    buy_shipment_label,
    can_mutate_shipment,
    compute_estimated_delivery,
    create_shipment_tracker,
    fetch_shipment_rates,
    reset_related_shipment_rates,
)
from karrio.server.manager.serializers.tracking import (
    TrackerEventInjectRequest,
    TrackerUpdateData,
    TrackingSerializer,
    apply_tracker_changes,
    bulk_save_trackers,
    can_mutate_tracker,
    update_shipment_tracker,
    update_tracker,
)

__all__ = [
    "ErrorResponse",
    "ErrorMessages",
    "AddressSerializer",
    "can_mutate_address",
    "ParcelSerializer",
    "can_mutate_parcel",
    "CommoditySerializer",
    "can_mutate_commodity",
    "ProductSerializer",
    "RateSerializer",
    "TrackingSerializer",
    "TrackerUpdateData",
    "TrackerEventInjectRequest",
    "update_shipment_tracker",
    "can_mutate_tracker",
    "update_tracker",
    "apply_tracker_changes",
    "bulk_save_trackers",
    "ShipmentRateData",
    "PurchasedShipment",
    "ShipmentSerializer",
    "ShipmentUpdateData",
    "ShipmentPurchaseData",
    "ShipmentPurchaseSerializer",
    "ShipmentCancelSerializer",
    "create_shipment_tracker",
    "reset_related_shipment_rates",
    "can_mutate_shipment",
    "buy_shipment_label",
    "fetch_shipment_rates",
    "compute_estimated_delivery",
    "PickupData",
    "PickupUpdateData",
    "PickupCancelData",
    "can_mutate_pickup",
    "DocumentUploadSerializer",
    "can_upload_shipment_document",
    "ManifestSerializer",
]
