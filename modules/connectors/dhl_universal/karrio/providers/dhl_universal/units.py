""" DHL Universal Native Types """
import karrio.lib as lib


class TrackingStatus(lib.Enum):
    delivered = ["delivered"]
    in_transit = ["transit"]
    delivery_failed = ["failure"]
    delivery_delayed = ["unknown"]
