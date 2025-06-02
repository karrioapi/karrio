import json
from import_export import resources

import karrio.server.serializers as serializers
import karrio.server.manager.models as manager
import karrio.server.providers.models as providers
from karrio.server.core import utils, gateway, exceptions


DEFAULT_HEADERS = {
    "id": "ID",
    "tracking_number": "Tracking Number",
    "status": "Status",
    "tracking_carrier": "Carrier",
    "options": "Options",
}


def tracker_export_resource(query_params: dict, context, data_fields: dict = None):
    queryset = manager.Tracking.access_by(context)
    field_headers = data_fields if data_fields is not None else DEFAULT_HEADERS
    _exclude = query_params.get("exclude", "").split(",")
    _fields = (
        "id",
        "tracking_number",
        "status",
        "tracking_carrier",
        "options",
    )

    class Resource(resources.ModelResource):
        class Meta:
            model = manager.Tracking
            fields = _fields
            exclude = _exclude
            export_order = [k for k in field_headers.keys() if k not in _exclude]

        def get_queryset(self):
            return queryset

        def get_export_headers(self):
            headers = super().get_export_headers()
            return [field_headers.get(k, k) for k in headers]

        if "tracking_carrier" not in _exclude:
            tracking_carrier = resources.Field()

            def dehydrate_tracking_carrier(self, row):
                carrier = getattr(row, "tracking_carrier", None)

                return getattr(carrier, "carrier_name", None)

        if "options" not in _exclude:
            options = resources.Field(default=None)

            def dehydrate_options(self, row):
                return json.loads(json.dumps(row.options))

    return Resource()


def tracker_import_resource(
    query_params: dict,
    context,
    data_fields: dict = None,
    batch_id: str = None,
    **kwargs,
):
    queryset = manager.Tracking.access_by(context)
    field_headers = data_fields if data_fields is not None else DEFAULT_HEADERS
    _exclude = query_params.get("exclude", "").split(",")
    _fields = (
        "id",
        "tracking_number",
        "status",
        "tracking_carrier",
        "options",
    )

    class Resource(resources.ModelResource):
        class Meta:
            model = manager.Tracking
            fields = _fields
            exclude = _exclude
            export_order = [k for k in field_headers.keys() if k not in _exclude]

        def get_queryset(self):
            return queryset

        def get_export_headers(self):
            headers = super().get_export_headers()
            return [field_headers.get(k, k) for k in headers]

        def init_instance(self, row=None):
            carrier_id = row.get("tracking_carrier")
            tracking_number = row.get("tracking_number")

            errors = []
            if len(tracking_number or "") == 0:
                errors.append(
                    exceptions.APIException(
                        f"A tracking number is required.",
                        code="tracking_number_required",
                    )
                )
            if carrier_id is None:
                errors.append(
                    exceptions.APIException(
                        f"No carrier connection found.",
                        code="invalid_carrier",
                    )
                )
            if any(errors):
                raise exceptions.APIExceptions(
                    errors,
                    code="invalid_row",
                )

            tracker = (
                manager.Tracking.access_by(context)
                .filter(tracking_number=tracking_number)
                .first()
            )
            carrier = providers.Carrier.objects.get(id=carrier_id).settings
            exists = getattr(tracker, "carrier_name", None) == carrier.carrier_name
            meta = {} if batch_id is None else dict(meta=dict(batch_id=batch_id))

            instance = (
                tracker
                if exists
                else manager.Tracking(
                    status="unknown",
                    test_mode=context.test_mode,
                    created_by_id=context.user.id,
                    tracking_number=tracking_number,
                    events=utils.default_tracking_event(
                        description="Awaiting update from carrier...",
                        code="UNKNOWN",
                    ),
                    **meta,
                )
            )
            return instance

        def save_instance(
            self, instance, is_create, using_transactions=True, dry_run=False
        ):
            is_create = instance.pk is None

            result = super().save_instance(
                instance,
                is_create,
                using_transactions,
                dry_run,
            )

            if is_create:
                serializers.link_org(instance, context)

            return result

        def before_import(self, dataset, using_transactions, dry_run, **kwargs):
            if dry_run:
                # Retrieve requested carriers from the database to set their id in the tracking_carrier column
                carrier_col = dataset.get_col(
                    dataset.headers.index(data_fields.get("tracking_carrier"))
                )
                carriers = {
                    carrier_name: utils.failsafe(
                        lambda: gateway.Carriers.first(
                            context=context,
                            capability="tracking",
                            carrier_name=carrier_name,
                            raise_not_found=False,
                        )
                    )
                    for carrier_name in set(carrier_col)
                }

                del dataset[data_fields.get("tracking_carrier")]
                dataset.append_col(
                    [
                        getattr(carriers.get(carrier_name), "id", None)
                        for carrier_name in carrier_col
                    ],
                    header="tracking_carrier",
                )

                # set actual fields name to headers
                dataset.headers = [
                    next(
                        (key for key, value in data_fields.items() if value == header),
                        header,
                    )
                    for header in dataset.headers
                ]

                unknown_headers = [
                    header
                    for header in dataset.headers
                    if header not in manager.Tracking.__dict__
                ]

                if any(unknown_headers):
                    raise exceptions.APIException(
                        code="unknown_headers",
                        detail=unknown_headers,
                    )

            return super().before_import(dataset, using_transactions, dry_run, **kwargs)

    return Resource()
