from functools import partial
from django.db import models
from organizations.abstract import (
    AbstractOrganization,
    AbstractOrganizationUser,
    AbstractOrganizationOwner,
    AbstractOrganizationInvitation
)

import purpleserver.providers.models as providers
import purpleserver.pricing.models as pricing
import purpleserver.manager.models as manager
import purpleserver.events.models as events
import purpleserver.graph.models as graph
import purpleserver.core.models as core
import purpleserver.user.models as auth


class Organization(AbstractOrganization):
    id = models.CharField(max_length=50, primary_key=True, default=partial(core.uuid, prefix='org_'), editable=False)

    carriers = models.ManyToManyField(providers.Carrier, related_name="org", through='CarrierLink')
    system_carriers = models.ManyToManyField(providers.Carrier, related_name="active_orgs")

    parcels = models.ManyToManyField(manager.Parcel, related_name="org", through='ParcelLink')
    pickups = models.ManyToManyField(manager.Pickup, related_name="org", through='PickupLink')
    customs = models.ManyToManyField(manager.Customs, related_name="org", through='CustomsLink')
    trackers = models.ManyToManyField(manager.Tracking, related_name="org", through='TrackerLink')
    addresses = models.ManyToManyField(manager.Address, related_name="org", through='AddressLink')
    shipments = models.ManyToManyField(manager.Shipment, related_name="org", through='ShipmentLink')
    commodities = models.ManyToManyField(manager.Commodity, related_name="org", through='CommodityLink')

    templates = models.ManyToManyField(graph.Template, related_name="org", through='TemplateLink')

    webhooks = models.ManyToManyField(events.Webhook, related_name="org", through='WebhookLink')

    logs = models.ManyToManyField(core.APILog, related_name="org", through='LogLink')

    tokens = models.ManyToManyField(auth.Token, related_name="org", through='TokenLink')

    surcharges = models.ManyToManyField(pricing.Surcharge, related_name="org")


class OrganizationUser(AbstractOrganizationUser):

    def __str__(self):
        return f"{self.user.email} ({self.organization.name})"


class OrganizationOwner(AbstractOrganizationOwner):

    def __str__(self):
        return "{0}: {1}".format(self.organization, self.organization_user.user.email)


class OrganizationInvitation(AbstractOrganizationInvitation):
    pass


"""Models organization linking"""


class CarrierLink(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="carrier_links")
    item = models.OneToOneField(providers.Carrier, on_delete=models.CASCADE, related_name="link")


class ParcelLink(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="parcel_links")
    item = models.OneToOneField(manager.Parcel, on_delete=models.CASCADE, related_name="link")


class PickupLink(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="pickup_links")
    item = models.OneToOneField(manager.Pickup, on_delete=models.CASCADE, related_name="link")


class CustomsLink(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="custom_links")
    item = models.OneToOneField(manager.Customs, on_delete=models.CASCADE, related_name="link")


class TrackerLink(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="tracker_links")
    item = models.OneToOneField(manager.Tracking, on_delete=models.CASCADE, related_name="link")


class AddressLink(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="address_links")
    item = models.OneToOneField(manager.Address, on_delete=models.CASCADE, related_name="link")


class ShipmentLink(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="shipment_links")
    item = models.OneToOneField(manager.Shipment, on_delete=models.CASCADE, related_name="link")


class CommodityLink(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="commodity_links")
    item = models.OneToOneField(manager.Commodity, on_delete=models.CASCADE, related_name="link")


class TemplateLink(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="template_links")
    item = models.OneToOneField(graph.Template, on_delete=models.CASCADE, related_name="link")


class WebhookLink(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="webhook_links")
    item = models.OneToOneField(events.Webhook, on_delete=models.CASCADE, related_name="link")


class LogLink(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="log_links")
    item = models.OneToOneField(core.APILog, on_delete=models.CASCADE, related_name="link")


class TokenLink(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="token_links")
    item = models.OneToOneField(auth.Token, on_delete=models.CASCADE, related_name="link")
