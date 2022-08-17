import uuid
import typing
import logging
from datetime import datetime

from django.db.models import Q
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import NotFound

import karrio
import karrio.lib as lib
import karrio.server.core.utils as utils
import karrio.server.core.models as core
import karrio.server.providers.models as providers
from karrio.server.core import (
    datatypes,
    dataunits,
    serializers,
    exceptions,
    validators,
)

logger = logging.getLogger(__name__)


class Carriers:
    @staticmethod
    def list(context=None, **kwargs) -> typing.List[providers.Carrier]:
        query: typing.Any = tuple()
        list_filter = kwargs.copy()
        user_filter = core.get_access_filter(context) if context is not None else []
        test_mode = list_filter.get("test_mode") or getattr(context, "test_mode", None)
        active_key = (
            "active_orgs__id" if settings.MULTI_ORGANIZATIONS else "active_users__id"
        )
        access_entity = getattr(
            context, "org" if settings.MULTI_ORGANIZATIONS else "user", None
        )
        access_id = getattr(access_entity, "id", None)
        system_carrier_user = (
            Q(**{"active": True, "created_by__isnull": True, active_key: access_id})
            if access_id is not None
            else Q(**{"active": True, "created_by__isnull": True})
        )
        creator_filter = (
            Q(
                created_by__id=context.user.id,
                **(dict(org=None) if settings.MULTI_ORGANIZATIONS else {}),
            )
            if getattr(context, "user", None) is not None
            else Q()
        )

        # Check if the system_only flag is not specified and there is a provided user, get the users carriers
        if (not list_filter.get("system_only")) and (len(user_filter) > 0):
            query += (user_filter | system_carrier_user | creator_filter,)
        elif list_filter.get("system_only") is True:
            query += (Q(created_by__isnull=True, active=True),)

        # Check if the test filter is specified then set it otherwise return all carriers live and test mode
        if test_mode is not None:
            query += (Q(test_mode=test_mode),)

        # Check if the active flag is specified and return all active carrier is active is not set to false
        if list_filter.get("active") is not None:
            active = False if list_filter["active"] is False else True
            carrier_is_active = Q(active=active, created_by__isnull=False)
            system_carrier_is_active = (
                system_carrier_user
                if active
                else Q(active=active, created_by__isnull=True)
            )
            query += (carrier_is_active | system_carrier_is_active,)

        # Check if a specific carrier_id is provided, to add it to the query
        if "carrier_id" in list_filter:
            query += (Q(carrier_id=list_filter["carrier_id"]),)

        # Check if a specific carrier_id is provided, to add it to the query
        if "capability" in list_filter:
            query += (Q(capabilities__contains=[list_filter["capability"]]),)

        # Check if a list of carrier_ids are provided, to add the list to the query
        if any(list_filter.get("carrier_ids", [])):
            query += (Q(carrier_id__in=list_filter["carrier_ids"]),)

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
                _queries = (
                    Q(**{f"{carrier_names[0].replace('_', '')}settings__isnull": False})
                    if carrier_names[0] in providers.MODELS.keys()
                    else Q(genericsettings__custom_carrier_name=carrier_names[0])
                )
                for carrier_name in carrier_names[1:]:
                    _queries |= (
                        Q(**{f"{carrier_name.replace('_', '')}settings__isnull": False})
                        if carrier_name in providers.MODELS.keys()
                        else Q(genericsettings__custom_carrier_name=carrier_name)
                    )

                query += (_queries,)

        if "carrier_name" in list_filter:
            carrier_name = list_filter["carrier_name"]

            if carrier_name not in providers.MODELS.keys():
                raise NotFound(
                    f"No extension installed for the carrier: '{carrier_name}'"
                )

            query += (Q(**{f"{carrier_name.replace('_', '')}settings__isnull": False}),)

        carriers = providers.Carrier.objects.filter(*query)

        # Raise an error if no carrier is found
        if list_filter.get("raise_not_found") and len(carriers) == 0:
            raise NotFound("No active carrier connection found to process the request")

        return carriers

    @staticmethod
    def first(**kwargs) -> providers.Carrier:
        return next(iter(Carriers.list(**kwargs)), None)


class Address:
    @staticmethod
    def validate(payload: dict) -> datatypes.AddressValidation:
        validation = validators.Address.validate(datatypes.Address(**payload))

        if validation.success is False:
            raise exceptions.APIException(detail=validation, code="invalid_address")

        return validation


class Shipments:
    @staticmethod
    def create(
        payload: dict,
        carrier: providers.Carrier = None,
        resolve_tracking_url: typing.Callable[[str, str], str] = None,
    ) -> datatypes.Shipment:
        selected_rate = next(
            (
                datatypes.Rate(**rate)
                for rate in payload.get("rates")
                if rate.get("id") == payload.get("selected_rate_id")
            ),
            None,
        )

        if selected_rate is None:
            raise NotFound("Invalid selected rate")

        carrier = carrier or Carriers.first(
            carrier_id=selected_rate.carrier_id,
            test_mode=selected_rate.test_mode,
            services=[selected_rate.service],
        )
        request = lib.to_object(
            datatypes.ShipmentRequest,
            {**lib.to_dict(payload), "service": selected_rate.service},
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
            return {
                **(parent.meta or {}),
                "rate_provider": (
                    (parent.meta or {}).get("rate_provider") or carrier.carrier_name
                ).lower(),
                "service_name": utils.upper(
                    (parent.meta or {}).get("service_name") or selected_rate.service
                ),
            }

        def process_selected_rate() -> dict:
            rate = (
                {
                    **lib.to_dict(shipment.selected_rate),
                    "id": f"rat_{uuid.uuid4().hex}",
                    "test_mode": carrier.test_mode,
                }
                if shipment.selected_rate is not None
                else lib.to_dict(selected_rate)
            )
            return {
                **rate,
                "meta": process_meta(shipment.selected_rate or selected_rate),
            }

        def process_tracking_url(rate: datatypes.Rate) -> str:
            rate_provider = (rate.get("meta") or {}).get("rate_provider")
            if (rate_provider not in providers.MODELS) and (
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
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f%z"),
                "meta": process_meta(shipment),
                "messages": messages,
            },
        )

    @staticmethod
    def cancel(
        payload: dict, carrier: providers.Carrier = None, **carrier_filters
    ) -> datatypes.ConfirmationResponse:
        carrier = carrier or Carriers.first(
            **{
                **dict(active=True, capability="shipping", raise_not_found=True),
                **carrier_filters,
            }
        )

        if carrier is None:
            raise NotFound("No active carrier connection found to process the request")

        request = karrio.Shipment.cancel(datatypes.ShipmentCancelRequest(**payload))

        # The request call is wrapped in utils.identity to simplify mocking in tests
        confirmation, messages = (
            utils.identity(lambda: request.from_(carrier.gateway).parse())
            if "cancel_shipment" in carrier.gateway.capabilities
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

    @staticmethod
    def track(
        payload: dict,
        carrier: providers.Carrier = None,
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
        results, messages = utils.identity(lambda: request.from_(carrier.gateway).parse())

        if not any(results or []) and (raise_on_error or utils.is_sdk_message(messages)):
            raise exceptions.APIException(
                detail=messages,
                status_code=status.HTTP_404_NOT_FOUND,
            )

        result = next(iter(results or []), None)
        details = result or datatypes.TrackingDetails(
            carrier_id=carrier.carrier_id,
            carrier_name=carrier.carrier_name,
            tracking_number=payload["tracking_numbers"][0],
            events=[
                datatypes.TrackingEvent(
                    date=datetime.now().strftime("%Y-%m-%d"),
                    description="Awaiting update from carrier...",
                    code="UNKNOWN",
                    time=datetime.now().strftime("%H:%M"),
                )
            ],
            delivered=False,
        )
        tracking_number = payload["tracking_numbers"][0]
        options = {
            **(payload.get("options") or {}),
            tracking_number: {
                **(details.meta or {}),
                **(payload.get("options") or {}).get(tracking_number, {}),
            },
        }

        return datatypes.TrackingResponse(
            tracking=lib.to_object(
                datatypes.Tracking,
                {
                    **lib.to_dict(details),
                    "id": f"trk_{uuid.uuid4().hex}",
                    "test_mode": carrier.test_mode,
                    "status": utils.compute_tracking_status(result).value,
                    "meta": details.meta or {},
                    "options": options,
                },
            ),
            messages=messages,
        )


class Pickups:
    @staticmethod
    def schedule(
        payload: dict, carrier: providers.Carrier = None, **carrier_filters
    ) -> datatypes.PickupResponse:
        carrier = carrier or Carriers.first(
            **{
                **dict(active=True, capability="pickup", raise_not_found=True),
                **carrier_filters,
            }
        )

        if carrier is None:
            raise NotFound("No active carrier connection found to process the request")

        request = karrio.Pickup.schedule(datatypes.PickupRequest(**lib.to_dict(payload)))

        # The request call is wrapped in utils.identity to simplify mocking in tests
        pickup, messages = utils.identity(lambda: request.from_(carrier.gateway).parse())

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
                    "id": f"pck_{uuid.uuid4().hex}",
                    "test_mode": carrier.test_mode,
                }
            ),
            messages=messages,
        )

    @staticmethod
    def update(
        payload: dict, carrier: providers.Carrier = None, **carrier_filters
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
        pickup, messages = utils.identity(lambda: request.from_(carrier.gateway).parse())

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
    def cancel(
        payload: dict, carrier: providers.Carrier = None, **carrier_filters
    ) -> datatypes.ConfirmationResponse:
        carrier = carrier or Carriers.first(
            **{
                **dict(active=True, capability="pickup", raise_not_found=True),
                **carrier_filters,
            }
        )

        if carrier is None:
            raise NotFound("No active carrier connection found to process the request")

        request = karrio.Pickup.cancel(
            datatypes.PickupCancelRequest(**lib.to_dict(payload))
        )

        # The request call is wrapped in utils.identity to simplify mocking in tests
        confirmation, messages = (
            utils.identity(lambda: request.from_(carrier.gateway).parse())
            if "cancel_shipment" in carrier.gateway.features
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


@utils.post_processing(methods=["fetch"])
class Rates:
    post_process_functions: typing.List[typing.Callable] = []

    @staticmethod
    def fetch(
        payload: dict, carriers: typing.List[providers.Carrier] = None, **carrier_filters,
    ) -> datatypes.RateResponse:
        carrier_ids = payload.get("carrier_ids", [])
        services = payload.get("services", [])
        shipper_country_code = payload["shipper"].get("country_code")
        carriers = carriers or Carriers.list(
            **{
                **dict(
                    active=True,
                    capability="rating",
                    carrier_ids=carrier_ids,
                    services=services,
                ),
                **carrier_filters,
            }
        )

        gateways = utils.filter_rate_carrier_compatible_gateways(
            carriers, carrier_ids, shipper_country_code
        )

        if len(gateways) == 0:
            raise NotFound("No active carrier connection found to process the request")

        request = karrio.Rating.fetch(lib.to_object(datatypes.RateRequest, payload))

        # The request call is wrapped in utils.identity to simplify mocking in tests
        rates, messages = utils.identity(lambda: request.from_(*gateways).parse())

        if not any(rates) and any(messages):
            raise exceptions.APIException(
                detail=messages,
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
            )

        def process_rate(rate: datatypes.Rate) -> datatypes.Rate:
            carrier = next((c for c in carriers if c.carrier_id == rate.carrier_id))
            meta = {
                **(rate.meta or {}),
                "rate_provider": (
                    (rate.meta or {}).get("rate_provider") or rate.carrier_name
                ).lower(),
                "service_name": utils.upper(
                    (rate.meta or {}).get("service_name") or rate.service
                ),
            }

            return datatypes.Rate(
                **{
                    **lib.to_dict(rate),
                    "id": f"rat_{uuid.uuid4().hex}",
                    "test_mode": carrier.test_mode,
                    "meta": {
                        **meta,
                        "carrier_connection_id": carrier.id,
                    },
                }
            )

        formated_rates: typing.List[datatypes.Rate] = sorted(
            map(process_rate, rates), key=lambda rate: rate.total_charge
        )

        return lib.to_object(
            datatypes.RateResponse, dict(rates=formated_rates, messages=messages)
        )


class Documents:

    @staticmethod
    def upload(
        payload: dict,
        carrier: providers.Carrier = None,
        **carrier_filters,
    ) -> datatypes.DocumentUploadResponse:
        carrier = carrier or Carriers.first(
            **{
                **dict(active=True, raise_not_found=True),
                **carrier_filters,
            }
        )

        if 'upload_document' not in carrier.gateway.capabilities:
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
            }
        )
