from import_export import resources

from karrio.server.core import gateway
from karrio.server.core import utils, dataunits as units
from karrio.server.manager import models

DEFAULT_HEADERS = {
    "id": "id",
    "tracking_number": "tracking_number",
    "carrier": "carrier",
    "status": "status",
    "test_mode": "test_mode",
    "tracking_carrier": "tracking_carrier",
    "created_by": "created_by",
}


def tracking_resource(query_params: dict, context):
    queryset = models.Tracking.access_by(context)
    _exclude = query_params.get("exclude", "").split(",")
    _fields = (
        "id",
        "tracking_number",
        "status",
        "test_mode",
        "tracking_carrier",
        "created_by",
    )

    class Resource(resources.ModelResource):
        class Meta:
            model = models.Tracking
            fields = _fields
            exclude = _exclude
            export_order = [k for k in DEFAULT_HEADERS.keys() if k not in _exclude]

        def get_queryset(self):
            return queryset

        def get_export_headers(self):
            headers = super().get_export_headers()
            return [DEFAULT_HEADERS.get(k, k) for k in headers]

        def before_import(self, dataset, using_transactions, dry_run, **kwargs):
            # Retrieve requested carriers from the database to set their id in the tracking_carrier column
            carrier_col = dataset.get_col(dataset.headers.index("carrier"))
            carriers = {
                carrier_name: gateway.Carriers.first(
                    context=context, carrier_name=carrier_name
                )
                for carrier_name in set(carrier_col)
            }

            dataset.append_col(
                [
                    getattr(carriers.get(carrier_name), "id", None)
                    for carrier_name in carrier_col
                ],
                header="tracking_carrier",
            )

            del dataset["carrier"]

            # Set test_mode column if not defined
            if "test_mode" not in dataset.headers:
                dataset.append_col(
                    [True for _ in range(len(dataset._data))], header="test_mode"
                )

            # Set created_by (actor) column
            dataset.append_col(
                [context.user.id for _ in range(len(dataset._data))],
                header="created_by",
            )

            # Set events column
            events = utils.default_tracking_event(
                code="UNKNOWN",
                description="Tracker created awaiting carrier update",
            )
            dataset.append_col(
                [events for _ in range(len(dataset._data))],
                header="events",
            )
            print(dataset._data)
            return super().before_import(dataset, using_transactions, dry_run, **kwargs)

        if "carrier" not in _exclude:
            carrier = resources.Field()

            def dehydrate_carrier(self, row):
                carrier = getattr(row, "tracking_carrier", None)
                settings = getattr(carrier, "settings", None)
                return getattr(
                    settings,
                    "display_name",
                    units.REFERENCE_MODELS["carriers"][carrier.carrier_name],
                )

    return Resource()
