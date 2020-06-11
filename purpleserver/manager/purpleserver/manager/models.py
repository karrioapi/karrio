from functools import partial
from django.db import models
from django.contrib.postgres.fields import JSONField
from purpleserver.core.models.carrier import Carrier
from purpleserver.core.models.entity import Entity, OwnedEntity, uuid
from purpleserver.core.serializers import (
    WEIGHT_UNIT, DIMENSION_UNIT, CURRENCIES, PAYMENT_TYPES
)


class Address(OwnedEntity):
    class Meta:
        db_table = "address"
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='adr_'), editable=False)
    postal_code = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=50, blank=True)
    federal_tax_id = models.CharField(max_length=50, blank=True)
    state_tax_id = models.CharField(max_length=50, blank=True)
    person_name = models.CharField(max_length=50, blank=True)
    company_name = models.CharField(max_length=50, blank=True)
    country_code = models.CharField(max_length=3, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=50, blank=True)

    state_code = models.CharField(max_length=3, blank=True)
    suburb = models.CharField(max_length=3, blank=True)
    residential = models.BooleanField(null=True)

    address_line1 = models.CharField(max_length=100, blank=True)
    address_line2 = models.CharField(max_length=100, blank=True)


class Parcel(OwnedEntity):
    class Meta:
        db_table = "parcel"
        verbose_name = 'Parcel'
        verbose_name_plural = 'Parcels'

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='par_'), editable=False)
    weight = models.FloatField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    length = models.FloatField(blank=True, null=True)
    packaging_type = models.CharField(max_length=50, blank=True)
    package_preset = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=250, blank=True)
    content = models.CharField(max_length=100, blank=True)
    is_document = models.BooleanField(default=False)
    weight_unit = models.CharField(max_length=2, choices=WEIGHT_UNIT, blank=True)
    dimension_unit = models.CharField(max_length=2, choices=DIMENSION_UNIT, blank=True)


class Payment(Entity):
    class Meta:
        db_table = "payment"
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    paid_by = models.CharField(max_length=20, choices=PAYMENT_TYPES, blank=True)
    amount = models.FloatField(blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCIES, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    contact = models.ForeignKey('Address', on_delete=models.CASCADE, null=True)


class Document(Entity):
    class Meta:
        db_table = "document"
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    type = models.CharField(max_length=20, blank=True)
    format = models.CharField(max_length=20, blank=True)
    image = models.FileField(upload_to='uploads/')

    shipment = models.ForeignKey('Shipment', on_delete=models.CASCADE, null=True)


class Rate(Entity):
    class Meta:
        db_table = "rate"
        verbose_name = 'Rate'
        verbose_name_plural = 'Rates'

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='rat_'), editable=False)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, choices=CURRENCIES, blank=True)
    service = models.CharField(max_length=50)
    discount = models.FloatField(blank=True)
    base_charge = models.FloatField()
    total_charge = models.FloatField()
    duties_and_taxes = models.FloatField(blank=True)
    estimated_delivery = models.CharField(max_length=100, blank=True)
    extra_charges = JSONField()

    shipment = models.ForeignKey('Shipment', on_delete=models.CASCADE)


class Customs(Entity):
    class Meta:
        db_table = "customs"
        verbose_name = 'Customs Info'
        verbose_name_plural = 'Customs Info'

    no_eei = models.CharField(max_length=20, blank=True)
    aes = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=20, blank=True)
    terms_of_trade = models.CharField(max_length=20)
    duty = models.ForeignKey('Payment', on_delete=models.CASCADE, blank=True)
    commercial_invoice = models.BooleanField(null=True)
    commodities = JSONField(blank=True)
    invoice = JSONField(blank=True)


class Shipment(OwnedEntity):
    class Meta:
        db_table = "shipment"
        verbose_name = 'Shipment'
        verbose_name_plural = 'Shipments'

    id = models.CharField(max_length=50, primary_key=True, default=partial(uuid, prefix='shp_'), editable=False)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, blank=True)

    service = models.CharField(max_length=50, blank=True)
    tracking_number = models.CharField(max_length=50, blank=True)
    label = models.TextField(max_length=None, blank=True)

    shipper = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='shipper')
    recipient = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='recipient')
    parcel = models.ForeignKey('Parcel', on_delete=models.CASCADE)

    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, blank=True)
    customs = models.ForeignKey('Customs', on_delete=models.CASCADE, blank=True)
    selected_rate = models.ForeignKey('Rate', on_delete=models.CASCADE, blank=True, related_name='selected_rate')

    options = JSONField(blank=True)
