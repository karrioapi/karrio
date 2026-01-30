import uuid
import typing
import datetime

from django.db.models import Q
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import NotFound
from karrio.server.core.logging import logger

import karrio.lib as lib
import karrio.sdk as karrio
import karrio.server.core.utils as utils
import karrio.server.core.models as core
import karrio.server.core.datatypes as datatypes
import karrio.server.core.dataunits as dataunits
import karrio.server.core.exceptions as exceptions
import karrio.server.providers.models as providers
import karrio.server.serializers as base_serializers
import karrio.server.core.serializers as serializers


class Connections:
    """
    Unified connection resolver for all connection types.

    Queries from:
    1. Carrier - User/org-owned connections
    2. BrokeredConnection - User enablement of SystemConnection
    """

    @staticmethod
    def list(context=None, **kwargs) -> typing.List[typing.Any]:
        """
        List all accessible connections (Carrier + BrokeredConnection).

        Args:
            context: Request context with user/org info
            **kwargs: Filters (test_mode, active, carrier_id, capability, etc.)

        Returns:
            Combined list of Carrier and BrokeredConnection instances.
            Both implement compatible interfaces (.carrier_id, .gateway, etc.)
        """
        list_filter = kwargs.copy()
        user_filter = core.get_access_filter(context) if context is not None else []
        test_mode = list_filter.get("test_mode") or getattr(context, "test_mode", None)
        system_only = list_filter.get("system_only") is True

        # Get user/org access ID for brokered connections
        access_id = getattr(
            getattr(context, "org" if settings.MULTI_ORGANIZATIONS else "user", None),
            "id",
            None,
        )
        creator_filter = lib.identity(
            Q(
                created_by__id=context.user.id,
                **(dict(org=None) if settings.MULTI_ORGANIZATIONS else {}),
            )
            if getattr(context, "user", None) is not None
            else Q()
        )

        # ─────────────────────────────────────────────────────────────────
        # QUERY 1: User/Org-owned CarrierConnection connections
        # ─────────────────────────────────────────────────────────────────
        carrier_queryset = providers.CarrierConnection.objects.filter(
            user_filter if len(user_filter) > 0 else Q() | creator_filter
        )

        # ─────────────────────────────────────────────────────────────────
        # QUERY 2: Brokered connections (enabled system connections)
        # ─────────────────────────────────────────────────────────────────
        if settings.MULTI_ORGANIZATIONS:
            # Insiders: Filter by org via BrokeredConnectionLink
            brokered_queryset = providers.BrokeredConnection.objects.enabled().filter(
                Q(link__org__id=access_id) if access_id else Q()
            )
        else:
            # OSS: Filter by created_by user
            brokered_queryset = providers.BrokeredConnection.objects.enabled().filter(
                Q(created_by__id=access_id) if access_id else Q()
            )

        # ─────────────────────────────────────────────────────────────────
        # APPLY COMMON FILTERS
        # ─────────────────────────────────────────────────────────────────

        # Test mode filter
        if test_mode is not None:
            carrier_queryset = carrier_queryset.filter(test_mode=test_mode)
            brokered_queryset = brokered_queryset.filter(
                system_connection__test_mode=test_mode
            )

        # Active filter
        if list_filter.get("active") is not None:
            active = False if list_filter["active"] is False else True
            carrier_queryset = carrier_queryset.filter(active=active)
            brokered_queryset = brokered_queryset.filter(
                is_enabled=active, system_connection__active=active
            )

        # Carrier ID filter - matches by id (primary key) OR carrier_id (friendly name)
        if "carrier_id" in list_filter:
            filter_value = list_filter["carrier_id"]
            carrier_queryset = carrier_queryset.filter(
                Q(id=filter_value) | Q(carrier_id=filter_value)
            )
            # Brokered: check id, user override carrier_id, or system carrier_id
            brokered_queryset = brokered_queryset.filter(
                Q(id=filter_value)
                | Q(carrier_id=filter_value)
                | Q(
                    carrier_id__isnull=True,
                    system_connection__carrier_id=filter_value,
                )
            )

        # Capability filter
        if "capability" in list_filter:
            carrier_queryset = carrier_queryset.filter(
                capabilities__icontains=list_filter["capability"]
            )
            # Brokered: check overrides first, then system
            brokered_queryset = brokered_queryset.filter(
                Q(capabilities_overrides__icontains=list_filter["capability"])
                | Q(
                    capabilities_overrides=[],
                    system_connection__capabilities__icontains=list_filter["capability"],
                )
            )

        # Metadata key filter
        if "metadata_key" in list_filter:
            carrier_queryset = carrier_queryset.filter(
                metadata__has_key=list_filter["metadata_key"]
            )
            brokered_queryset = brokered_queryset.filter(
                metadata__has_key=list_filter["metadata_key"]
            )

        # Carrier IDs filter (list) - matches by id (primary key) OR carrier_id (friendly name)
        if any(list_filter.get("carrier_ids", [])):
            ids_list = list_filter["carrier_ids"]
            carrier_queryset = carrier_queryset.filter(
                Q(id__in=ids_list) | Q(carrier_id__in=ids_list)
            )
            # Brokered: check id, user override carrier_id, or system carrier_id
            brokered_queryset = brokered_queryset.filter(
                Q(id__in=ids_list)
                | Q(carrier_id__in=ids_list)
                | Q(
                    carrier_id__isnull=True,
                    system_connection__carrier_id__in=ids_list,
                )
            )

        # Services filter
        if any(list_filter.get("services", [])):
            carrier_names = [
                name
                for name, services in dataunits.contextual_reference(context)[
                    "services"
                ].items()
                if any(
                    service in list_filter["services"] for service in services.keys()
                )
            ]
            if len(carrier_names) > 0:
                carrier_queryset = carrier_queryset.filter(carrier_code__in=carrier_names)
                brokered_queryset = brokered_queryset.filter(
                    system_connection__carrier_code__in=carrier_names
                )

        # Carrier name (carrier_code) filter
        if "carrier_name" in list_filter:
            carrier_name = list_filter["carrier_name"]
            carrier_queryset = carrier_queryset.filter(carrier_code=carrier_name)
            brokered_queryset = brokered_queryset.filter(
                system_connection__carrier_code=carrier_name
            )

        # ─────────────────────────────────────────────────────────────────
        # COMBINE RESULTS
        # ─────────────────────────────────────────────────────────────────

        if system_only:
            # Only brokered connections (system connection enablements)
            connections = list(brokered_queryset.distinct())
        else:
            # Combine both types
            carriers = list(carrier_queryset.distinct())
            brokered = list(brokered_queryset.distinct())
            connections = carriers + brokered

        # ─────────────────────────────────────────────────────────────────
        # FILTER OUT NON-EXISTENT EXTENSIONS
        # ─────────────────────────────────────────────────────────────────
        # Some connections may reference carrier extensions that no longer
        # exist (e.g., deprecated carriers like 'fedex_ws'). Filter these
        # out to prevent "Unknown provider" errors when accessing .gateway
        available_providers = set(karrio.gateway.providers.keys())
        valid_connections = []
        for conn in connections:
            if conn.ext in available_providers:
                valid_connections.append(conn)
            else:
                logger.warning(
                    "Skipping connection with non-existent extension",
                    carrier_id=conn.carrier_id,
                    extension=conn.ext,
                )
        connections = valid_connections

        # Raise error if no connections found
        if list_filter.get("raise_not_found") and len(connections) == 0:
            raise NotFound("No active carrier connection found to process the request")

        return connections

    @staticmethod
    def first(**kwargs) -> typing.Any:
        """Get first matching connection."""
        return next(iter(Connections.list(**kwargs)), None)


# Alias for backwards compatibility
Carriers = Connections


class Address:
    @staticmethod
    @utils.with_telemetry("address_validate")
    def validate(
        payload: dict,
        provider: providers.CarrierConnection = None,
        **carrier_filters,
    ) -> datatypes.AddressValidation:
        provider = provider or Carriers.first(
            **{
                **dict(active=True, raise_not_found=True),
                **carrier_filters,
            }
        )

        if "validate_address" not in provider.gateway.proxy_methods:
            raise exceptions.APIException(
                detail=f"address validation is not supported by carrier: '{provider.carrier_id}'",
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        request = karrio.Address.validate(
            lib.to_object(datatypes.AddressValidationRequest, payload)
        )

        # The request is wrapped in utils.identity to simplify mocking in tests.
        return utils.identity(lambda: request.from_(provider.gateway).parse())


class Shipments:
    @staticmethod
    @utils.with_telemetry("shipment_create")
    @utils.require_selected_rate
    def create(
        payload: dict,
        carrier: providers.CarrierConnection = None,
        selected_rate: typing.Union[datatypes.Rate, dict] = None,
        resolve_tracking_url: typing.Callable[[str, str], str] = None,
        context: base_serializers.Context = None,
        **kwargs,
    ) -> datatypes.Shipment:
        selected_rate = lib.to_object(
            datatypes.Rate,
            lib.to_dict(selected_rate),
        )
        carrier = carrier or Carriers.first(
            carrier_id=selected_rate.carrier_id,
            test_mode=selected_rate.test_mode,
            services=[selected_rate.service],
            context=context,
        )

        if carrier is None:
            raise NotFound("No active carrier connection found to process the request")

        payload = {
            **lib.to_dict(payload),
            "options": {
                **(selected_rate.meta or {}),
                **(payload.get("options") or {}),
            },
        }
        request = lib.to_object(
            datatypes.ShipmentRequest,
            {
                **lib.to_dict(payload),
                "service": selected_rate.service,
            },
        )

        # The request is wrapped in utils.identity to simplify mocking in tests.
        shipment, messages = utils.identity(
            lambda: karrio.Shipment.create(request).from_(carrier.gateway).parse()
        )

        if shipment is None:
            raise exceptions.APIException(
                detail=messages,
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
            )

        def process_meta(parent) -> dict:
            service_name = utils.upper(
                (parent.meta or {}).get("service_name") or selected_rate.service
            )
            rate_provider = (
                (parent.meta or {}).get("rate_provider") or carrier.carrier_name
            ).lower()
            # BrokeredConnection.credentials returns None (security feature)
            custom_carrier_name = (carrier.credentials or {}).get("custom_carrier_name")

            return {
                **(parent.meta or {}),
                "ext": carrier.ext,
                "carrier": rate_provider,
                "service_name": service_name,
                "rate_provider": rate_provider,  # TODO: deprecate 'rate_provider' in favor of 'carrier'
                **(
                    {"custom_carrier_name": custom_carrier_name}
                    if custom_carrier_name
                    else {}
                ),
            }

        def process_selected_rate() -> dict:
            estimated_delivery = lib.failsafe(
                lambda: (
                    getattr(shipment.selected_rate, "estimated_delivery", None)
                    or getattr(selected_rate, "estimated_delivery", None)
                )
            )
            transit_days = lib.failsafe(
                lambda: (
                    getattr(shipment.selected_rate, "transit_days", None)
                    or getattr(selected_rate, "transit_days", None)
                )
            )
            rate = lib.identity(
                {
                    **lib.to_dict(shipment.selected_rate),
                    "id": f"rat_{uuid.uuid4().hex}",
                    "test_mode": carrier.test_mode,
                    "estimated_delivery": estimated_delivery,
                    "transit_days": transit_days,
                }
                if shipment.selected_rate is not None
                else lib.to_dict(selected_rate)
            )
            return lib.to_dict(
                {
                    **rate,
                    "meta": process_meta(shipment.selected_rate or selected_rate),
                }
            )

        def process_tracking_url(rate: datatypes.Rate) -> str:
            rate_provider = (rate.get("meta") or {}).get("rate_provider")
            if (rate_provider not in dataunits.CARRIER_NAMES) and (
                (shipment.meta or {}).get("tracking_url") is not None
            ):
                return shipment.meta["tracking_url"]

            if resolve_tracking_url is not None:
                url = resolve_tracking_url(
                    shipment.tracking_number, rate_provider or rate.carrier_name
                )
                return utils.app_tracking_query_params(url, carrier)

            return ""

        def process_parcel_refs(parcels: typing.List[dict]) -> list:
            references = (shipment.meta or {}).get("tracking_numbers") or [
                shipment.tracking_number
            ]

            return [
                {
                    **lib.to_dict(parcel),
                    "reference_number": (
                        references[index]
                        if len(references) > index
                        else parcel.get("reference_number")
                    ),
                }
                for index, parcel in enumerate(parcels)
            ]

        shipment_rate = process_selected_rate()

        return lib.to_object(
            datatypes.Shipment,
            {
                "id": f"shp_{uuid.uuid4().hex}",
                **payload,
                **lib.to_dict(shipment),
                "test_mode": carrier.test_mode,
                "selected_rate": shipment_rate,
                "service": shipment_rate["service"],
                "selected_rate_id": shipment_rate["id"],
                "parcels": process_parcel_refs(payload["parcels"]),
                "tracking_url": process_tracking_url(shipment_rate),
                "status": serializers.ShipmentStatus.purchased.value,
                "created_at": datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S.%f%z"
                ),
                "meta": process_meta(shipment),
                "messages": messages,
            },
        )

    @staticmethod
    @utils.with_telemetry("shipment_cancel")
    def cancel(
        payload: dict, carrier: providers.CarrierConnection = None, **carrier_filters
    ) -> datatypes.ConfirmationResponse:
        carrier_id = lib.identity(
            dict(carrier_id=payload.pop("carrier_id"))
            if any(payload.get("carrier_id") or "")
            else {}
        )
        carrier = carrier or Carriers.first(
            **{
                **dict(active=True, capability="shipping", raise_not_found=True),
                **carrier_id,
                **carrier_filters,
            }
        )

        if carrier is None:
            raise NotFound("No active carrier connection found to process the request")

        request = karrio.Shipment.cancel(
            lib.to_object(datatypes.ShipmentCancelRequest, payload)
        )

        # The request call is wrapped in utils.identity to simplify mocking in tests
        confirmation, messages = lib.identity(
            utils.identity(lambda: request.from_(carrier.gateway).parse())
            if "cancel_shipment" in carrier.gateway.proxy_methods
            else (
                datatypes.Confirmation(
                    carrier_name=carrier.gateway.settings.carrier_name,
                    carrier_id=carrier.gateway.settings.carrier_id,
                    success=True,
                    operation="Safe cancellation allowed",
                ),
                [],
            )
        )

        if confirmation is None:
            raise exceptions.APIException(
                detail=messages,
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
            )

        return datatypes.ConfirmationResponse(
            confirmation=confirmation,
            messages=messages,
        )

    @staticmethod
    @utils.with_telemetry("tracking_fetch")
    def track(
        payload: dict,
        carrier: providers.CarrierConnection = None,
        raise_on_error: bool = True,
        **carrier_filters,
    ) -> datatypes.TrackingResponse:
        carrier = carrier or Carriers.first(
            **{
                **dict(active=True, capability="tracking", raise_not_found=True),
                **carrier_filters,
            }
        )

        if carrier is None:
            raise NotFound("No active carrier connection found to process the request")

        request = karrio.Tracking.fetch(
            lib.to_object(datatypes.TrackingRequest, payload)
        )

        # The request call is wrapped in utils.identity to simplify mocking in tests
        results, messages = utils.identity(
            lambda: request.from_(carrier.gateway).parse()
        )

        if not any(results or []) and (
            raise_on_error or utils.is_sdk_message(messages)
        ):
            raise exceptions.APIException(
                detail=messages,
                status_code=status.HTTP_404_NOT_FOUND,
            )

        result = next(iter(results or []), None)
        tracking_number = payload["tracking_numbers"][0]
        details = result or datatypes.TrackingDetails(
            carrier_id=carrier.carrier_id,
            carrier_name=carrier.carrier_name,
            tracking_number=tracking_number,
            events=[
                datatypes.TrackingEvent(
                    date=datetime.datetime.now().strftime("%Y-%m-%d"),
                    description="Awaiting update from carrier...",
                    code="UNKNOWN",
                    time=datetime.datetime.now().strftime("%H:%M"),
                )
            ],
            delivered=False,
        )
        options = {
            **(payload.get("options") or {}),
            tracking_number: {
                **(details.meta or {}),
                **(payload.get("options") or {}).get(tracking_number, {}),
            },
        }
        meta = {
            "ext": carrier.ext,
            "carrier": carrier.carrier_name,
            **(details.meta or {}),
        }
        info = {
            "carrier_tracking_link": utils.get_carrier_tracking_link(
                carrier, tracking_number
            ),
            "source": "api",
            **(lib.to_dict(details.info or {})),
            **(lib.to_dict(payload.get("info") or {})),
        }

        return datatypes.TrackingResponse(
            tracking=lib.to_object(
                datatypes.Tracking,
                {
                    **lib.to_dict(details),
                    "id": f"trk_{uuid.uuid4().hex}",
                    "test_mode": carrier.test_mode,
                    "status": utils.compute_tracking_status(result).value,
                    "options": options,
                    "meta": meta,
                    "info": info,
                },
            ),
            messages=messages,
        )


class Pickups:
    @staticmethod
    @utils.with_telemetry("pickup_schedule")
    def schedule(
        payload: dict, carrier: providers.CarrierConnection = None, **carrier_filters
    ) -> datatypes.PickupResponse:
        carrier = carrier or Carriers.first(
            **{
                **dict(active=True, capability="pickup", raise_not_found=True),
                **carrier_filters,
            }
        )

        if carrier is None:
            raise NotFound("No active carrier connection found to process the request")

        request = karrio.Pickup.schedule(
            datatypes.PickupRequest(**lib.to_dict(payload))
        )

        # The request call is wrapped in utils.identity to simplify mocking in tests
        pickup, messages = utils.identity(
            lambda: request.from_(carrier.gateway).parse()
        )

        if pickup is None:
            raise exceptions.APIException(
                detail=messages,
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
            )

        def process_meta(parent) -> dict:
            return {
                **(parent.meta or {}),
                "ext": carrier.ext,
            }

        return datatypes.PickupResponse(
            pickup=datatypes.Pickup(
                **{
                    **payload,
                    **lib.to_dict(pickup),
                    "id": f"pck_{uuid.uuid4().hex}",
                    "test_mode": carrier.test_mode,
                    "meta": process_meta(pickup),
                    "messages": messages,
                }
            ),
            messages=messages,
        )

    @staticmethod
    @utils.with_telemetry("pickup_update")
    def update(
        payload: dict, carrier: providers.CarrierConnection = None, **carrier_filters
    ) -> datatypes.PickupResponse:
        carrier = carrier or Carriers.first(
            **{
                **dict(active=True, capability="pickup", raise_not_found=True),
                **carrier_filters,
            }
        )

        if carrier is None:
            raise NotFound("No active carrier connection found to process the request")

        request = karrio.Pickup.update(
            datatypes.PickupUpdateRequest(**lib.to_dict(payload))
        )

        # The request call is wrapped in utils.identity to simplify mocking in tests
        pickup, messages = utils.identity(
            lambda: request.from_(carrier.gateway).parse()
        )

        if pickup is None:
            raise exceptions.APIException(
                detail=messages,
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
            )

        return datatypes.PickupResponse(
            pickup=datatypes.Pickup(
                **{
                    **payload,
                    **lib.to_dict(pickup),
                    "test_mode": carrier.test_mode,
                }
            ),
            messages=messages,
        )

    @staticmethod
    @utils.with_telemetry("pickup_cancel")
    def cancel(
        payload: dict, carrier: providers.CarrierConnection = None, **carrier_filters
    ) -> datatypes.ConfirmationResponse:
        carrier = carrier or Carriers.first(
            **{
                **dict(active=True, capability="pickup"),
                **carrier_filters,
            }
        )

        if carrier is None:
            raise NotFound("No active carrier connection found to process the request")

        request = karrio.Pickup.cancel(
            datatypes.PickupCancelRequest(**lib.to_dict(payload))
        )

        # The request call is wrapped in utils.identity to simplify mocking in tests
        confirmation, messages = lib.identity(
            utils.identity(lambda: request.from_(carrier.gateway).parse())
            if "cancel_shipment" in carrier.gateway.proxy_methods
            else (
                datatypes.Confirmation(
                    carrier_name=carrier.gateway.settings.carrier_name,
                    carrier_id=carrier.gateway.settings.carrier_id,
                    success=True,
                    operation="Safe cancellation allowed",
                ),
                [],
            )
        )

        if confirmation is None:
            raise exceptions.APIException(
                detail=messages,
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
            )

        return datatypes.ConfirmationResponse(
            confirmation=confirmation, messages=messages
        )


@utils.post_processing(methods=["fetch", "resolve"])
class Rates:
    post_process_functions: typing.List[typing.Callable] = []

    @staticmethod
    @utils.with_telemetry("rates_fetch")
    def fetch(
        payload: dict,
        carriers: typing.List[providers.CarrierConnection] = None,
        raise_on_error: bool = True,
        **carrier_filters,
    ) -> datatypes.RateResponse:
        services = payload.get("services", [])
        carrier_ids = payload.get("carrier_ids", [])
        shipper_country_code = payload["shipper"].get("country_code")
        carriers = carriers or Carriers.list(
            **{
                "active": True,
                "capability": "rating",
                "carrier_ids": carrier_ids,
                "services": services,
                **carrier_filters,
            }
        )

        gateways = utils.filter_rate_carrier_compatible_gateways(
            carriers, carrier_ids, shipper_country_code
        )

        if raise_on_error and len(gateways) == 0:
            raise NotFound("No active carrier connection found to process the request")

        request = karrio.Rating.fetch(lib.to_object(datatypes.RateRequest, payload))

        # The request call is wrapped in utils.identity to simplify mocking in tests
        rates, messages = utils.identity(lambda: request.from_(*gateways).parse())

        if raise_on_error and not any(rates) and any(messages):
            raise exceptions.APIException(
                detail=messages,
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
            )

        def process_rate(rate: datatypes.Rate) -> datatypes.Rate:
            # Use effective_carrier_id for BrokeredConnection, fall back to carrier_id for Carrier
            carrier = next(
                (c for c in carriers if getattr(c, "effective_carrier_id", c.carrier_id) == rate.carrier_id)
            )
            rate_provider = (
                (rate.meta or {}).get("rate_provider")
                or getattr(carrier, "custom_carrier_name", None)
                or rate.carrier_name
            ).lower()
            service_name = utils.upper(
                (rate.meta or {}).get("service_name") or rate.service
            )

            meta = {
                **(rate.meta or {}),
                "ext": carrier.ext,
                "carrier": rate_provider,
                "service_name": service_name,
                "rate_provider": rate_provider,  # TODO: deprecate rate_provider
                "carrier_connection_id": carrier.id,
            }

            return lib.to_object(
                datatypes.Rate,
                {
                    **lib.to_dict(rate),
                    "id": f"rat_{uuid.uuid4().hex}",
                    "test_mode": carrier.test_mode,
                    "meta": meta,
                },
            )

        formated_rates: typing.List[datatypes.Rate] = sorted(
            map(process_rate, rates), key=lambda rate: rate.total_charge
        )

        return lib.to_object(
            datatypes.RateResponse, dict(rates=formated_rates, messages=messages)
        )

    @staticmethod
    @utils.with_telemetry("rates_resolve")
    def resolve(
        payload: dict,
        carriers: typing.List[providers.CarrierConnection] = None,
        raise_on_error: bool = True,
        **carrier_filters,
    ) -> datatypes.RateResponse:
        """Resolve rates using static rate sheets only (no carrier API calls).

        Unlike fetch(), this method:
        - Uses rate sheet data (services, zones, surcharges) directly
        - Never calls carrier APIs
        - Requires carriers to have rate_sheet with services

        Args:
            payload: Rate request payload (shipper, recipient, parcels, options)
            carriers: List of carrier connections to resolve rates for
            raise_on_error: Raise exception if no rates found
            **carrier_filters: Additional filters for carrier lookup

        Returns:
            RateResponse with resolved rates
        """
        services = payload.get("services", [])
        carrier_ids = payload.get("carrier_ids", [])
        carriers = carriers or Carriers.list(
            **{
                "active": True,
                "capability": "rating",
                "carrier_ids": carrier_ids,
                "services": services,
                **carrier_filters,
            }
        )

        if raise_on_error and len(carriers) == 0:
            raise NotFound("No active carrier connection found to process the request")

        # Build carrier settings with rate sheet services
        carrier_settings = []
        carriers_with_services = []

        for carrier in carriers:
            # Get services from rate sheet or carrier defaults
            carrier_services = carrier.services
            if not carrier_services:
                continue

            carriers_with_services.append(carrier)
            # Pass carrier.data directly - it's duck-type compatible with RatingMixinProxy
            carrier_settings.append(carrier.data)

        if raise_on_error and len(carrier_settings) == 0:
            raise NotFound("No carrier with rate sheet services found to process the request")

        request = karrio.Rating.resolve(lib.to_object(datatypes.RateRequest, payload))

        # The request call is wrapped in utils.identity to simplify mocking in tests
        rates, messages = utils.identity(
            lambda: request.from_(*carrier_settings).parse()
        )

        if raise_on_error and not any(rates) and any(messages):
            raise exceptions.APIException(
                detail=messages,
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
            )

        def process_rate(rate: datatypes.Rate) -> datatypes.Rate:
            carrier = next(
                (c for c in carriers_with_services if c.carrier_id == rate.carrier_id),
                None,
            )
            if carrier is None:
                return rate

            rate_provider = (
                (rate.meta or {}).get("rate_provider")
                or getattr(carrier, "custom_carrier_name", None)
                or rate.carrier_name
            ).lower()
            service_name = utils.upper(
                (rate.meta or {}).get("service_name") or rate.service
            )

            meta = {
                **(rate.meta or {}),
                "ext": carrier.ext,
                "carrier": rate_provider,
                "service_name": service_name,
                "rate_provider": rate_provider,
                "carrier_connection_id": carrier.id,
                "rate_source": "static",
            }

            return lib.to_object(
                datatypes.Rate,
                {
                    **lib.to_dict(rate),
                    "id": f"rat_{uuid.uuid4().hex}",
                    "test_mode": carrier.test_mode,
                    "meta": meta,
                },
            )

        formated_rates: typing.List[datatypes.Rate] = sorted(
            map(process_rate, rates), key=lambda rate: rate.total_charge
        )

        return lib.to_object(
            datatypes.RateResponse, dict(rates=formated_rates, messages=messages)
        )


class Documents:
    @staticmethod
    @utils.with_telemetry("document_upload")
    def upload(
        payload: dict,
        carrier: providers.CarrierConnection = None,
        **carrier_filters,
    ) -> datatypes.DocumentUploadResponse:
        carrier = carrier or Carriers.first(
            **{
                **dict(active=True, raise_not_found=True),
                **carrier_filters,
            }
        )

        if "upload_document" not in carrier.gateway.proxy_methods:
            raise exceptions.APIException(
                detail=f"trade document upload is not supported by carrier: '{carrier.carrier_id}'",
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        request = karrio.Document.upload(
            lib.to_object(datatypes.DocumentUploadRequest, payload)
        )

        # The request is wrapped in utils.identity to simplify mocking in tests.
        upload, messages = utils.identity(
            lambda: request.from_(carrier.gateway).parse()
        )

        if upload is None:
            raise exceptions.APIException(
                detail=messages,
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
            )

        return lib.to_object(
            datatypes.DocumentUploadResponse,
            {
                **payload,
                **lib.to_dict(upload),
                "test_mode": carrier.test_mode,
                "id": f"sdoc_{uuid.uuid4().hex}",
                "messages": lib.to_dict(messages),
            },
        )


class Manifests:
    @staticmethod
    @utils.with_telemetry("manifest_create")
    def create(
        payload: dict, carrier: providers.CarrierConnection = None, **carrier_filters
    ) -> datatypes.ManifestResponse:
        carrier = carrier or Carriers.first(
            **{
                **dict(active=True, capability="manifest", raise_not_found=True),
                **carrier_filters,
            }
        )

        if carrier is None:
            raise NotFound("No active carrier connection found to process the request")

        request = karrio.Manifest.create(
            lib.to_object(datatypes.ManifestRequest, lib.to_dict(payload))
        )

        # The request call is wrapped in utils.identity to simplify mocking in tests
        manifest, messages = utils.identity(
            lambda: request.from_(carrier.gateway).parse()
        )

        if manifest is None:
            raise exceptions.APIException(
                detail=messages,
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
            )

        def process_meta(parent) -> dict:
            return {
                **(parent.meta or {}),
                "ext": carrier.ext,
            }

        return datatypes.ManifestResponse(
            manifest=datatypes.Manifest(
                **{
                    **payload,
                    **lib.to_dict(manifest),
                    "id": f"manf_{uuid.uuid4().hex}",
                    "test_mode": carrier.test_mode,
                    "meta": process_meta(manifest),
                    "messages": messages,
                }
            ),
            messages=messages,
        )


class Insurance:
    @staticmethod
    @utils.with_telemetry("insurance_apply")
    def apply(
        payload: dict, provider: providers.CarrierConnection = None, **provider_filters
    ) -> datatypes.InsuranceDetails:
        provider = provider or Carriers.first(
            **{
                **dict(active=True, raise_not_found=True),
                **provider_filters,
            }
        )

        if "apply_insurance" not in provider.gateway.proxy_methods:
            raise exceptions.APIException(
                detail=f"insurance application is not supported by carrier: '{provider.carrier_id}'",
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        request = karrio.Insurance.apply(
            lib.to_object(datatypes.InsuranceRequest, payload)
        )

        # The request call is wrapped in utils.identity to simplify mocking in tests
        insurance, messages = utils.identity(
            lambda: request.from_(provider.gateway).parse()
        )

        if insurance is None:
            raise exceptions.APIException(
                detail=messages,
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
            )

        def process_meta(parent) -> dict:
            return {
                **(parent.meta or {}),
                "ext": provider.ext,
            }

        return datatypes.InsuranceResponse(
            insurance=datatypes.Insurance(
                **{
                    **payload,
                    **lib.to_dict(insurance),
                    "id": f"ins_{uuid.uuid4().hex}",
                    "test_mode": provider.test_mode,
                    "meta": process_meta(insurance),
                    "messages": messages,
                }
            ),
            messages=messages,
        )


class Duties:
    @staticmethod
    @utils.with_telemetry("duties_calculate")
    def calculate(
        payload: dict,
        provider: providers.CarrierConnection = None,
        **provider_filters,
    ) -> datatypes.DutiesResponse:
        provider = provider or Carriers.first(
            **{
                **dict(active=True, raise_not_found=True),
                **provider_filters,
            }
        )

        if "calculate_duties" not in provider.gateway.proxy_methods:
            raise exceptions.APIException(
                detail=f"duties calculation is not supported by carrier: '{provider.carrier_id}'",
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        request = karrio.Duty.calculate(
            lib.to_object(datatypes.DutiesCalculationRequest, payload)
        )

        # The request is wrapped in utils.identity to simplify mocking in tests.
        duties, messages = utils.identity(
            lambda: request.from_(provider.gateway).parse()
        )

        if duties is None:
            raise exceptions.APIException(
                detail=messages,
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
            )

        return datatypes.DutiesResponse(duties=duties, messages=messages)


class Webhooks:
    @staticmethod
    @utils.with_telemetry("webhook_register")
    def register(
        payload: dict,
        carrier: providers.CarrierConnection = None,
        **carrier_filters,
    ) -> datatypes.DocumentUploadResponse:
        carrier = carrier or Carriers.first(
            **{
                **dict(active=True, raise_not_found=True),
                **carrier_filters,
            }
        )

        if "register_webhook" not in carrier.gateway.proxy_methods:
            raise exceptions.APIException(
                detail=f"webhook registration is not supported by carrier: '{carrier.carrier_id}'",
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        request = karrio.Webhook.register(
            lib.to_object(datatypes.WebhookRegistrationRequest, payload)
        )

        # The request is wrapped in utils.identity to simplify mocking in tests.
        return utils.identity(lambda: request.from_(carrier.gateway).parse())

    @staticmethod
    @utils.with_telemetry("webhook_unregister")
    def unregister(
        payload: dict,
        carrier: providers.CarrierConnection = None,
        **carrier_filters,
    ) -> datatypes.ConfirmationResponse:
        carrier = carrier or Carriers.first(
            **{
                **dict(active=True, raise_not_found=True),
                **carrier_filters,
            }
        )

        if "deregister_webhook" not in carrier.gateway.proxy_methods:
            raise exceptions.APIException(
                detail=f"webhook deregistration is not supported by carrier: '{carrier.carrier_id}'",
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        request = karrio.Webhook.deregister(
            lib.to_object(datatypes.WebhookDeregistrationRequest, payload)
        )

        # The request is wrapped in utils.identity to simplify mocking in tests.
        return utils.identity(lambda: request.from_(carrier.gateway).parse())


class Hooks:

    @staticmethod
    def create_stub_gateway(
        carrier_name: str, test_mode: bool = False
    ) -> karrio.Gateway:
        import karrio.server.core.middleware as middleware
        import karrio.server.core.config as system_config
        import django.core.cache as caching

        _context = middleware.SessionContext.get_current_request()
        _tracer = getattr(_context, "tracer", lib.Tracer())
        _cache = lib.Cache(caching.cache)
        _config = lib.SystemConfig(system_config.config)

        return karrio.gateway[carrier_name].create(
            dict(
                carrier_id=carrier_name,
                test_mode=test_mode,
            ),
            _tracer,
            _cache,
            _config,
            is_stub=True,
        )

    @staticmethod
    @utils.with_telemetry("hook_webhook_event")
    def on_webhook_event(
        payload: dict, carrier: providers.CarrierConnection = None, **carrier_filters
    ) -> typing.Tuple[datatypes.WebhookEventDetails, typing.List[datatypes.Message]]:
        carrier = carrier or Carriers.first(
            **{
                **dict(active=True, raise_not_found=True),
                **carrier_filters,
            }
        )

        if carrier is None:
            raise NotFound("No active carrier connection found to process the request")

        request = karrio.Hooks.on_webhook_event(
            lib.to_object(datatypes.RequestPayload, lib.to_dict(payload))
        )

        # The request call is wrapped in utils.identity to simplify mocking in tests
        return utils.identity(lambda: request.from_(carrier.gateway).parse())

    @staticmethod
    @utils.with_telemetry("hook_oauth_authorize")
    def on_oauth_authorize(
        payload: dict,
        carrier: providers.CarrierConnection = None,
        carrier_name: str = None,
        test_mode: bool = False,
        **kwargs,
    ) -> typing.Tuple[datatypes.OAuthAuthorizeRequest, typing.List[datatypes.Message]]:
        gateway = lib.identity(
            getattr(carrier, "gateway", None)
            or Hooks.create_stub_gateway(carrier_name, test_mode)
        )

        return utils.identity(
            lambda: karrio.Hooks.on_oauth_authorize(payload).from_(gateway).parse()
        )

    @staticmethod
    @utils.with_telemetry("hook_oauth_callback")
    def on_oauth_callback(
        payload: dict,
        carrier_name: str = None,
        test_mode: bool = False,
        carrier: providers.CarrierConnection = None,
        **kwargs,
    ) -> typing.Tuple[typing.List[typing.Dict], typing.List[datatypes.Message]]:
        gateway = lib.identity(
            getattr(carrier, "gateway", None)
            or Hooks.create_stub_gateway(carrier_name, test_mode)
        )

        return utils.identity(
            lambda: karrio.Hooks.on_oauth_callback(payload).from_(gateway).parse()
        )
