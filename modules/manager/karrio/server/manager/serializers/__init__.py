from karrio.server.serializers import *
from karrio.server.core.serializers import *
from karrio.server.manager.serializers.address import (
    AddressSerializer,
    can_mutate_address,
)
from karrio.server.manager.serializers.parcel import (
    ParcelSerializer,
    can_mutate_parcel,
)
from karrio.server.manager.serializers.commodity import (
    CommoditySerializer,
    can_mutate_commodity,
)

# Product is a proxy of Commodity - use the same serializer
ProductSerializer = CommoditySerializer
from karrio.server.manager.serializers.rate import RateSerializer
from karrio.server.manager.serializers.tracking import (
    TrackingSerializer,
    TrackerUpdateData,
    TrackerEventInjectRequest,
    update_shipment_tracker,
    can_mutate_tracker,
    update_tracker,
)
from karrio.server.manager.serializers.shipment import (
    ShipmentRateData,
    PurchasedShipment,
    ShipmentSerializer,
    ShipmentUpdateData,
    ShipmentPurchaseData,
    ShipmentPurchaseSerializer,
    ShipmentCancelSerializer,
    create_shipment_tracker,
    reset_related_shipment_rates,
    can_mutate_shipment,
    buy_shipment_label,
    fetch_shipment_rates,
    compute_estimated_delivery,
)
from karrio.server.manager.serializers.pickup import (
    PickupData,
    PickupUpdateData,
    PickupCancelData,
)
from karrio.server.manager.serializers.document import (
    DocumentUploadSerializer,
    can_upload_shipment_document,
)
from karrio.server.manager.serializers.manifest import (
    ManifestSerializer,
)
