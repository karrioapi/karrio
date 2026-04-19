import karrio.server.proxy.views.manifest as manifest
import karrio.server.proxy.views.pickup as pickup
import karrio.server.proxy.views.rating as rating
import karrio.server.proxy.views.shipping as shipping
import karrio.server.proxy.views.tracking as tracking
from karrio.server.proxy.router import router

# Importing these modules registers their routes on import.
REGISTERED_VIEWS = (tracking, rating, shipping, pickup, manifest)

__all__ = ["router"]
