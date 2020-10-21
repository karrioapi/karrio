from functools import partial
from typing import List, cast
from django.db import models
from jsonfield import JSONField

from purpleserver.providers.models import Carrier
from purpleserver.core.models import OwnedEntity, uuid
from purpleserver.core.serializers import (
    WEIGHT_UNIT, DIMENSION_UNIT, PAYMENT_TYPES, CURRENCIES, SHIPMENT_STATUS, COUNTRIES
)


class Address(OwnedEntity):
    class Meta:
        db_table = "address"
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='adr_'), editable=False)

    postal_code = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    federal_tax_id = models.CharField(max_length=50, null=True, blank=True)
    state_tax_id = models.CharField(max_length=50, null=True, blank=True)
    person_name = models.CharField(max_length=50, null=True, blank=True)
    company_name = models.CharField(max_length=50, null=True, blank=True)
    country_code = models.CharField(max_length=20, choices=COUNTRIES)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)

    state_code = models.CharField(max_length=20, null=True, blank=True)
    suburb = models.CharField(max_length=20, null=True, blank=True)
    residential = models.BooleanField(null=True)

    address_line1 = models.CharField(max_length=100, null=True, blank=True)
    address_line2 = models.CharField(max_length=100, null=True, blank=True)


class Parcel(OwnedEntity):
    class Meta:
        db_table = "parcel"
        verbose_name = 'Parcel'
        verbose_name_plural = 'Parcels'

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='pcl_'), editable=False)

    weight = models.FloatField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    packaging_type = models.CharField(max_length=50, null=True, blank=True)
    package_preset = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    content = models.CharField(max_length=100, null=True, blank=True)
    is_document = models.BooleanField(default=False, blank=True, null=True)
    weight_unit = models.CharField(max_length=2, choices=WEIGHT_UNIT, null=True, blank=True)
    dimension_unit = models.CharField(max_length=2, choices=DIMENSION_UNIT, null=True, blank=True)


class Commodity(OwnedEntity):
    class Meta:
        db_table = "commodity"
        verbose_name = 'Commodity'
        verbose_name_plural = 'Commodities'

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='cdt_'), editable=False)

    weight = models.FloatField(blank=True, null=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    quantity = models.IntegerField(blank=True, null=True)
    sku = models.CharField(max_length=100, null=True, blank=True)
    value_amount = models.FloatField(blank=True, null=True)
    value_currency = models.CharField(max_length=3, choices=COUNTRIES, null=True, blank=True)
    origin_country = models.CharField(max_length=3, choices=CURRENCIES, null=True, blank=True)


class Payment(OwnedEntity):
    DIRECT_PROPS = ['amount', 'paid_by', 'currency', 'account_number']
    RELATIONAL_PROPS = ['contact']

    class Meta:
        db_table = "payment"
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='pyt_'), editable=False)

    amount = models.FloatField(blank=True, null=True)
    paid_by = models.CharField(max_length=20, choices=PAYMENT_TYPES, null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCIES, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    contact = models.ForeignKey('Address', on_delete=models.CASCADE, blank=True, null=True)


class Customs(OwnedEntity):
    DIRECT_PROPS = ['no_eei', 'aes', 'description', 'terms_of_trade', 'commercial_invoice']
    RELATIONAL_PROPS = ['duty', 'commodities']

    class Meta:
        db_table = "customs"
        verbose_name = 'Customs Info'
        verbose_name_plural = 'Customs Info'

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='cst_'), editable=False)

    no_eei = models.CharField(max_length=20, null=True, blank=True)
    aes = models.CharField(max_length=20, null=True, blank=True)
    description = models.CharField(max_length=20, null=True, blank=True)
    terms_of_trade = models.CharField(max_length=20)
    commercial_invoice = models.BooleanField(null=True)
    duty = models.ForeignKey('Payment', on_delete=models.CASCADE, blank=True, null=True)

    shipment_commodities = models.ManyToManyField('Commodity', blank=True)

    @property
    def commodities(self):
        return self.shipment_commodities.all()


class Pickup(OwnedEntity):
    DIRECT_PROPS = [
        "confirmation_number", "pickup_date", "instruction", "package_location", "ready_time",
        "closing_time", "test_mode"
    ]

    class Meta:
        db_table = "pickup"
        verbose_name = 'Pickup'
        verbose_name_plural = 'Pickups'

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='pck_'), editable=False)
    confirmation_number = models.CharField(max_length=50, unique=True, blank=False)
    test_mode = models.BooleanField(null=False)
    pickup_date = models.DateField(blank=False)
    ready_time = models.CharField(max_length=5, blank=False)
    closing_time = models.CharField(max_length=5, blank=False)
    instruction = models.CharField(max_length=200, null=True, blank=True)
    package_location = models.CharField(max_length=200, null=True, blank=True)

    options = JSONField(blank=True, null=True, default={})
    address = models.ForeignKey('Address', on_delete=models.CASCADE, blank=True, null=True)

    # System Reference fields

    pickup_carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    shipments = models.ManyToManyField('Shipment', related_name='pickup_shipments')

    # Computed properties

    @property
    def carrier_id(self) -> str:
        return cast(Carrier, self.pickup_carrier).carrier_id

    @property
    def carrier_name(self) -> str:
        return cast(Carrier, self.pickup_carrier).data.carrier_name

    @property
    def parcels(self) -> List[Parcel]:
        return sum([list(shipment.parcels) for shipment in self.shipments.all()], [])

    @property
    def tracking_numbers(self) -> List[str]:
        return [shipment.tracking_number for shipment in self.shipments.all()]


class Tracking(OwnedEntity):
    class Meta:
        db_table = "tracking-status"
        verbose_name = 'Tracking Satus'
        verbose_name_plural = 'Tracking Statuses'

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='trk_'), editable=False)
    tracking_number = models.CharField(max_length=50, unique=True)
    events = JSONField(blank=True, null=True, default=[])
    test_mode = models.BooleanField(null=False)

    # System Reference fields

    tracking_carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)

    # Computed properties

    @property
    def carrier_id(self) -> str:
        return cast(Carrier, self.tracking_carrier).carrier_id

    @property
    def carrier_name(self) -> str:
        return cast(Carrier, self.tracking_carrier).data.carrier_name


class Shipment(OwnedEntity):
    DIRECT_PROPS = [
        'label', 'options', 'services', 'status', 'service', 'meta', 'shipment_rates',
        'tracking_number', 'doc_images', 'tracking_url', 'shipment_identifier', 'test_mode',
    ]
    RELATIONAL_PROPS = ['shipper', 'recipient', 'parcels', 'payment', 'customs', 'selected_rate']

    class Meta:
        db_table = "shipment"
        verbose_name = 'Shipment'
        verbose_name_plural = 'Shipments'

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='shp_'), editable=False)
    status = models.CharField(max_length=50, choices=SHIPMENT_STATUS, default=SHIPMENT_STATUS[0][0])

    recipient = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='recipient')
    shipper = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='shipper')

    tracking_number = models.CharField(max_length=50, null=True, blank=True)
    shipment_identifier = models.CharField(max_length=50, null=True, blank=True)
    label = models.TextField(max_length=None, null=True, blank=True)
    tracking_url = models.TextField(max_length=None, null=True, blank=True)
    test_mode = models.BooleanField(null=False)

    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, blank=True, null=True)
    customs = models.ForeignKey('Customs', on_delete=models.CASCADE, blank=True, null=True)

    selected_rate = JSONField(blank=True, null=True)

    options = JSONField(blank=True, null=True, default={})
    services = JSONField(blank=True, null=True, default=[])
    doc_images = JSONField(blank=True, null=True, default=[])
    meta = JSONField(blank=True, null=True, default={})

    # System Reference fields

    shipment_rates = JSONField(blank=True, null=True, default=[])
    shipment_parcels = models.ManyToManyField('Parcel', related_name='shipment_parcels')
    carriers = models.ManyToManyField(Carrier, blank=True, related_name='rating_carriers')
    selected_rate_carrier = models.ForeignKey(
        Carrier, on_delete=models.CASCADE, related_name='selected_rate_carrier', blank=True, null=True)

    # Computed properties

    @property
    def parcels(self):
        return self.shipment_parcels.all()

    @property
    def carrier_id(self) -> str:
        return cast(Carrier, self.selected_rate_carrier).carrier_id

    @property
    def carrier_name(self) -> str:
        return cast(Carrier, self.selected_rate_carrier).data.carrier_name

    @property
    def carrier_ids(self) -> List[str]:
        return [
            carrier.carrier_id for carrier in self.carriers.all()
        ]

    @property
    def selected_rate_id(self) -> str:
        return (
            cast(dict, self.selected_rate).get('id') if self.selected_rate is not None else None
        )

    @property
    def service(self) -> str:
        return (
            cast(dict, self.selected_rate).get('service') if self.selected_rate is not None else None
        )

    @property
    def rates(self) -> List[dict]:
        rates: List[dict] = []
        for stored_rate in cast(List[dict], self.shipment_rates):
            carrier = Carrier.objects.get(id=stored_rate['carrier_ref']).data
            rates.append({
                **stored_rate,
                'carrier_id': carrier.carrier_id,
                'carrier_name': carrier.carrier_name,
            })
        return rates
