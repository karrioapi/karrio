import json
from django.db.models import Q
from import_export import resources

import karrio.lib as lib
from karrio.core.units import Packages
from karrio.server.manager import models
from karrio.server.core import serializers as core
from karrio.server.core.filters import ShipmentFilters
from karrio.server.manager.serializers import ShipmentSerializer
from karrio.server.core import datatypes as types, dataunits as units

DEFAULT_HEADERS = {
    "id": "ID",
    "created_at": "Created at",
    "tracking_number": "Tracking number",
    "status": "Status",
    "shipper_id": "Shipper ID",
    "shipper_name": "Shipper name",
    "shipper_company": "Shipper Company",
    "shipper_phone": "Shipper phone",
    "shipper_email": "Shipper email",
    "shipper_address1": "Shipper address 1",
    "shipper_address2": "Shipper address 2",
    "shipper_city": "Shipper city",
    "shipper_state": "Shipper state",
    "shipper_postal_code": "Shipper postal code",
    "shipper_country": "Shipper country",
    "shipper_residential": "Shipper residential",
    "recipient_id": "Recipient ID",
    "recipient_name": "Recipient name",
    "recipient_company": "Recipient Company",
    "recipient_phone": "Recipient phone",
    "recipient_email": "Recipient email",
    "recipient_address1": "Recipient address 1",
    "recipient_address2": "Recipient address 2",
    "recipient_city": "Recipient city",
    "recipient_state": "Recipient state",
    "recipient_postal_code": "Recipient postal code",
    "recipient_country": "Recipient country",
    "recipient_residential": "Recipient residential",
    "parcel_width": "Parcel width",
    "parcel_height": "Parcel height",
    "parcel_length": "Parcel length",
    "parcel_dimension_unit": "Parcel dimension unit",
    "parcel_weight": "Parcel weight",
    "parcel_weight_unit": "Parcel weight unit",
    "parcel_package_preset": "Parcel package preset",
    "pieces": "Number of pieces",
    "service": "Service",
    "carrier": "Carrier",
    "rate": "Rate",
    "currency": "Currency",
    "paid_by": "Payor",
    "reference": "Reference",
    "options": "Options",
}


def shipment_export_resource(query_params: dict, context, **kwargs):
    queryset = models.Shipment.access_by(context)
    _exclude = query_params.get("exclude", "").split(",")
    _fields = (
        "id",
        "tracking_number",
        "created_at",
        "status",
        "reference",
    )

    if "status" not in query_params:
        queryset = queryset.filter(
            Q(status__in=["purchased", "delivered", "shipped", "in_transit"]),
        )

    class Resource(resources.ModelResource):
        class Meta:
            model = models.Shipment
            fields = _fields
            exclude = _exclude
            export_order = [k for k in DEFAULT_HEADERS.keys() if k not in _exclude]

        def get_queryset(self):
            return ShipmentFilters(query_params, queryset).qs

        def get_export_headers(self):
            headers = super().get_export_headers()
            return [DEFAULT_HEADERS.get(k, k) for k in headers]

        @staticmethod
        def packages(row):
            parcels = core.Parcel(row.parcels, many=True).data
            return Packages([lib.to_object(types.Parcel, p) for p in parcels])

        if "service" not in _exclude:
            service = resources.Field()

            def dehydrate_service(self, row):
                rate = getattr(row, "selected_rate") or {}
                return (rate.get("meta") or {}).get("service_name") or rate.get(
                    "service"
                )

        if "carrier" not in _exclude:
            carrier = resources.Field()

            def dehydrate_carrier(self, row):
                carrier = getattr(row, "selected_rate_carrier", None)
                settings = getattr(carrier, "settings", None)
                return getattr(
                    settings, "display_name", None
                ) or units.REFERENCE_MODELS["carriers"].get(carrier.carrier_name)

        if "pieces" not in _exclude:
            pieces = resources.Field()

            def dehydrate_pieces(self, row):
                return len(row.parcels.all())

        if "rate" not in _exclude:
            rate = resources.Field()

            def dehydrate_rate(self, row):
                return (getattr(row, "selected_rate") or {}).get("total_charge", None)

        if "currency" not in _exclude:
            currency = resources.Field()

            def dehydrate_currency(self, row):
                return (getattr(row, "selected_rate") or {}).get("currency", None)

        if "paid_by" not in _exclude:
            paid_by = resources.Field()

            def dehydrate_paid_by(self, row):
                return (getattr(row, "payment") or {}).get("paid_by", None)

        if "parcel_weight" not in _exclude:
            parcel_weight = resources.Field()

            def dehydrate_parcel_weight(self, row):
                return self.packages(row).weight.value

        if "parcel_weight_unit" not in _exclude:
            parcel_weight_unit = resources.Field()

            def dehydrate_parcel_weight_unit(self, row):
                return self.packages(row).weight_unit

        if "parcel_length" not in _exclude:
            parcel_length = resources.Field()

            def dehydrate_parcel_length(self, row):
                return self.packages(row)[0].parcel.length

        if "parcel_width" not in _exclude:
            parcel_width = resources.Field()

            def dehydrate_parcel_width(self, row):
                return self.packages(row)[0].parcel.width

        if "parcel_height" not in _exclude:
            parcel_height = resources.Field()

            def dehydrate_parcel_height(self, row):
                return self.packages(row)[0].parcel.height

        if "parcel_dimension_unit" not in _exclude:
            parcel_dimension_unit = resources.Field()

            def dehydrate_parcel_dimension_unit(self, row):
                _, unit = self.packages(row).compatible_units
                return unit.value

        if "parcel_package_preset" not in _exclude:
            parcel_package_preset = resources.Field()

            def dehydrate_parcel_package_preset(self, row):
                return self.packages(row)[0].parcel.package_preset

        if "shipment_date" not in _exclude:
            shipment_date = resources.Field()

            def dehydrate_shipment_date(self, row):
                return (getattr(row, "options") or {}).get("shipment_date", None) or (
                    lib.fdate(row.created_at, "%Y-%m-%m %H:%M:%M")
                )

        if "shipper_id" not in _exclude:
            shipper_id = resources.Field()

            def dehydrate_shipper_id(self, row):
                return row.shipper.id

        if "shipper_name" not in _exclude:
            shipper_name = resources.Field()

            def dehydrate_shipper_name(self, row):
                return row.shipper.person_name

        if "shipper_company" not in _exclude:
            shipper_company = resources.Field()

            def dehydrate_shipper_company(self, row):
                return row.shipper.company_name

        if "shipper_phone" not in _exclude:
            shipper_phone = resources.Field()

            def dehydrate_shipper_phone(self, row):
                return row.shipper.phone_number

        if "shipper_email" not in _exclude:
            shipper_email = resources.Field()

            def dehydrate_shipper_email(self, row):
                return row.shipper.email

        if "shipper_address1" not in _exclude:
            shipper_address1 = resources.Field()

            def dehydrate_shipper_address1(self, row):
                return row.shipper.address_line1

        if "shipper_address2" not in _exclude:
            shipper_address2 = resources.Field()

            def dehydrate_shipper_address2(self, row):
                return row.shipper.address_line2

        if "shipper_city" not in _exclude:
            shipper_city = resources.Field()

            def dehydrate_shipper_city(self, row):
                return row.shipper.city

        if "shipper_state" not in _exclude:
            shipper_state = resources.Field()

            def dehydrate_shipper_state(self, row):
                return row.shipper.state_code

        if "shipper_postal_code" not in _exclude:
            shipper_postal_code = resources.Field()

            def dehydrate_shipper_postal_code(self, row):
                return row.shipper.postal_code

        if "shipper_country" not in _exclude:
            shipper_country = resources.Field()

            def dehydrate_shipper_country(self, row):
                return row.shipper.country_code

        if "shipper_residential" not in _exclude:
            shipper_residential = resources.Field()

            def dehydrate_shipper_residential(self, row):
                return row.shipper.residential

        if "recipient_id" not in _exclude:
            recipient_id = resources.Field()

            def dehydrate_recipient_id(self, row):
                return row.recipient.id

        if "recipient_name" not in _exclude:
            recipient_name = resources.Field()

            def dehydrate_recipient_name(self, row):
                return row.recipient.person_name

        if "recipient_company" not in _exclude:
            recipient_company = resources.Field()

            def dehydrate_recipient_company(self, row):
                return row.recipient.company_name

        if "recipient_phone" not in _exclude:
            recipient_phone = resources.Field()

            def dehydrate_recipient_phone(self, row):
                return row.recipient.phone_number

        if "recipient_email" not in _exclude:
            recipient_email = resources.Field()

            def dehydrate_recipient_email(self, row):
                return row.recipient.email

        if "recipient_address1" not in _exclude:
            recipient_address1 = resources.Field()

            def dehydrate_recipient_address1(self, row):
                return row.recipient.address_line1

        if "recipient_address2" not in _exclude:
            recipient_address2 = resources.Field()

            def dehydrate_recipient_address2(self, row):
                return row.recipient.address_line2

        if "recipient_city" not in _exclude:
            recipient_city = resources.Field()

            def dehydrate_recipient_city(self, row):
                return row.recipient.city

        if "recipient_state" not in _exclude:
            recipient_state = resources.Field()

            def dehydrate_recipient_state(self, row):
                return row.recipient.state_code

        if "recipient_postal_code" not in _exclude:
            recipient_postal_code = resources.Field()

            def dehydrate_recipient_postal_code(self, row):
                return row.recipient.postal_code

        if "recipient_country" not in _exclude:
            recipient_country = resources.Field()

            def dehydrate_recipient_country(self, row):
                return row.recipient.country_code

        if "recipient_residential" not in _exclude:
            recipient_residential = resources.Field()

            def dehydrate_recipient_residential(self, row):
                return row.recipient.residential

        if "options" not in _exclude:
            options = resources.Field()

            def dehydrate_options(self, row):
                return json.loads(json.dumps(row.options))

    return Resource()


def shipment_import_resource(
    query_params: dict,
    context,
    data_fields: dict = None,
    batch_id: str = None,
    **kwargs
):
    queryset = models.Shipment.access_by(context)
    field_headers = data_fields if data_fields is not None else DEFAULT_HEADERS
    _exclude = query_params.get("exclude", "").split(",")
    _fields = (
        "shipper_name",
        "shipper_company",
        "shipper_address_line1",
        "shipper_address_line2",
        "shipper_city",
        "shipper_state",
        "shipper_postal_code",
        "shipper_country",
        "shipper_residential",
        "recipient_name",
        "recipient_company",
        "recipient_address_line1",
        "recipient_address_line2",
        "recipient_city",
        "recipient_state",
        "recipient_postal_code",
        "recipient_country",
        "recipient_residential",
        "parcel_width",
        "parcel_height",
        "parcel_length",
        "parcel_dimension_unit",
        "parcel_weight",
        "parcel_weight_unit",
        "parcel_package_preset",
        "service",
        "reference",
        "options",
    )

    _Base = type(
        "ResourceFields",
        (resources.ModelResource,),
        {
            k: resources.Field(readonly=(k not in models.Shipment.__dict__))
            for k in field_headers.keys()
            if k not in _exclude
        },
    )

    class Resource(_Base, resources.ModelResource):
        class Meta:
            model = models.Shipment
            fields = _fields
            exclude = _exclude
            export_order = [k for k in field_headers.keys() if k not in _exclude]

        def get_queryset(self):
            return queryset

        def get_export_headers(self):
            headers = super().get_export_headers()
            return [field_headers.get(k, k) for k in headers]

        def init_instance(self, row=None):
            service = row.get(field_headers["service"])
            svc = {} if service is None else dict(perferred_service=service)
            batch = {} if batch_id is None else dict(batch_id=batch_id)
            options = {
                **lib.to_dict(row.get(field_headers["options"]) or "{}"),
                **svc,
            }

            data = lib.to_dict(
                dict(
                    status="draft",
                    test_mode=context.test_mode,
                    created_by_id=context.user.id,
                    meta={**svc, **batch},
                    options=options,
                    shipper=dict(
                        person_name=row.get(field_headers["shipper_name"]),
                        company_name=row.get(field_headers["shipper_company"]),
                        address_line1=row.get(field_headers["shipper_address1"]),
                        address_line2=row.get(field_headers["shipper_address2"]),
                        city=row.get(field_headers["shipper_city"]),
                        state_code=row.get(field_headers["shipper_state"]),
                        postal_code=row.get(field_headers["shipper_postal_code"]),
                        country_code=row.get(field_headers["shipper_country"]),
                        residential=row.get(field_headers["shipper_residential"]),
                    ),
                    recipient=dict(
                        person_name=row.get(field_headers["recipient_name"]),
                        company_name=row.get(field_headers["recipient_company"]),
                        address_line1=row.get(field_headers["recipient_address1"]),
                        address_line2=row.get(field_headers["recipient_address2"]),
                        city=row.get(field_headers["recipient_city"]),
                        state_code=row.get(field_headers["recipient_state"]),
                        postal_code=row.get(field_headers["recipient_postal_code"]),
                        country_code=row.get(field_headers["recipient_country"]),
                        residential=row.get(field_headers["recipient_residential"]),
                    ),
                    parcels=[
                        dict(
                            weight=row.get(field_headers["parcel_weight"]),
                            weight_unit=row.get(field_headers["parcel_weight_unit"])
                            or "KG",
                            width=row.get(field_headers["parcel_width"]),
                            height=row.get(field_headers["parcel_height"]),
                            length=row.get(field_headers["parcel_length"]),
                            dimension_unit=row.get(
                                field_headers["parcel_dimension_unit"]
                            )
                            or "CM",
                            package_preset=row.get(
                                field_headers["parcel_package_preset"]
                            ),
                        )
                    ],
                )
            )

            instance = (
                ShipmentSerializer.map(data=data, context=context)
                .save(fetch_rates=False)
                .instance
            )

            return instance

    return Resource()
