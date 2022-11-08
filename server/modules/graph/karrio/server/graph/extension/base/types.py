import graphene
from graphene.types import generic
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_otp.plugins.otp_email import models as otp

from karrio.core.utils import DP
import karrio.server.providers.models as providers
import karrio.server.manager.models as manager
import karrio.server.tracing.models as tracing
import karrio.server.graph.models as graph
import karrio.server.user.models as auth
import karrio.server.core.models as core
import karrio.server.graph.utils as utils

User = get_user_model()


class MultiFactorType(graphene.ObjectType):
    name = graphene.String()
    confirmed = graphene.Boolean()


class UserType(utils.BaseObjectType):
    multi_factor = graphene.Field(MultiFactorType)

    class Meta:
        model = User
        fields = ("email", "full_name", "is_staff", "last_login", "date_joined")

    def resolve_multi_factor(self, info):
        device = otp.EmailDevice.objects.filter(user__id=self.id).first()

        if device is not None:
            return device.__dict__

        return device


class LogType(utils.BaseObjectType):
    data = generic.GenericScalar()
    response = generic.GenericScalar()
    query_params = generic.GenericScalar()

    class Meta:
        model = core.APILog
        exclude = (
            "errors",
            "view",
            "view_method",
        )
        interfaces = (utils.CustomNode,)

    def resolve_response(self, info):
        try:
            return DP.to_dict(self.response)
        except:
            return self.response

    def resolve_data(self, info):
        try:
            return DP.to_dict(self.data)
        except:
            return self.data

    def resolve_query_params(self, info):
        try:
            return DP.to_dict(self.query_params)
        except:
            return self.query_params


class TracingRecordType(utils.BaseObjectType):
    record = generic.GenericScalar()
    meta = generic.GenericScalar()

    class Meta:
        model = tracing.TracingRecord
        exclude = (*tracing.TracingRecord.HIDDEN_PROPS,)
        interfaces = (utils.CustomNode,)

    def resolve_record(self, info):
        try:
            return DP.to_dict(self.record)
        except:
            return self.record

    def resolve_meta(self, info):
        try:
            return DP.to_dict(self.meta)
        except:
            return self.meta


class TokenType(utils.BaseObjectType):
    class Meta:
        model = auth.Token
        exclude = ("user",)


class MessageType(graphene.ObjectType):
    carrier_name = graphene.String()
    carrier_id = graphene.String()
    message = graphene.String()
    code = graphene.String()
    details = generic.GenericScalar()


class ChargeType(graphene.ObjectType):
    name = graphene.String()
    amount = graphene.Float()
    currency = utils.CurrencyCodeEnum()


class RateType(graphene.ObjectType):
    id = graphene.String(required=True)
    carrier_name = graphene.String(required=True)
    carrier_id = graphene.String(required=True)
    currency = utils.CurrencyCodeEnum()
    transit_days = graphene.Int()
    service = graphene.String(required=True)
    discount = graphene.Float()
    base_charge = graphene.Float(required=True)
    total_charge = graphene.Float(required=True)
    duties_and_taxes = graphene.Float()
    extra_charges = graphene.List(graphene.NonNull(ChargeType), default_value=[])
    test_mode = graphene.Boolean(required=True)
    meta = generic.GenericScalar()

class CommodityType(utils.BaseObjectType):
    weight_unit = utils.WeightUnitEnum()
    origin_country = graphene.String()
    value_currency = graphene.String()
    parent_id = graphene.String()
    metadata = generic.GenericScalar()

    class Meta:
        model = manager.Commodity
        exclude = (*manager.Commodity.HIDDEN_PROPS,)

    def resolve_parent_id(self, info):
        return self.parent_id


class AddressType(utils.BaseObjectType):
    validation = generic.GenericScalar()
    country_code = utils.CountryCodeEnum(required=True)

    class Meta:
        model = manager.Address
        exclude = (*manager.Address.HIDDEN_PROPS, "template")


class ParcelType(utils.BaseObjectType):
    weight_unit = utils.WeightUnitEnum()
    dimension_unit = utils.DimensionUnitEnum()

    class Meta:
        model = manager.Parcel
        exclude = (
            *manager.Parcel.HIDDEN_PROPS,
            "template",
        )


class DutyType(graphene.ObjectType):
    paid_by = utils.PaidByEnum()
    currency = utils.CurrencyCodeEnum()
    account_number = graphene.String()
    declared_value = graphene.Float()
    bill_to = graphene.Field(AddressType)
    id = graphene.String()


class CustomsType(utils.BaseObjectType):
    content_type = utils.CustomsContentTypeEnum()
    incoterm = utils.IncotermCodeEnum()
    duty = graphene.Field(DutyType)
    options = generic.GenericScalar()

    class Meta:
        model = manager.Customs
        exclude = (*manager.Customs.HIDDEN_PROPS, "template")

    def resolve_commodities(self, info):
        return self.commodities.all()


class AddressTemplateType(utils.BaseObjectType):
    address = graphene.Field(AddressType, required=True)

    class Meta:
        model = graph.Template
        exclude = (*graph.Template.HIDDEN_PROPS, "customs", "parcel")
        filter_fields = {
            "label": ["icontains"],
            "address__address_line1": ["icontains"],
        }
        interfaces = (utils.CustomNode,)


class CustomsTemplateType(utils.BaseObjectType):
    customs = graphene.Field(CustomsType, required=True)

    class Meta:
        model = graph.Template
        exclude = (*graph.Template.HIDDEN_PROPS, "address", "parcel")
        filter_fields = {"label": ["icontains"]}
        interfaces = (utils.CustomNode,)


class ParcelTemplateType(utils.BaseObjectType):
    parcel = graphene.Field(ParcelType, required=True)

    class Meta:
        model = graph.Template
        exclude = (*graph.Template.HIDDEN_PROPS, "address", "customs")
        filter_fields = {"label": ["icontains"]}
        interfaces = (utils.CustomNode,)


class DefaultTemplatesType(graphene.ObjectType):
    default_address = graphene.Field(AddressTemplateType, required=False)
    default_customs = graphene.Field(CustomsTemplateType, required=False)
    default_parcel = graphene.Field(ParcelTemplateType, required=False)


class TrackingEventType(graphene.ObjectType):
    description = graphene.String()
    location = graphene.String()
    code = graphene.String()
    date = graphene.String()
    time = graphene.String()


class TrackerType(utils.BaseObjectType):
    carrier_id = graphene.String(required=True)
    carrier_name = graphene.String(required=True)

    events = graphene.List(graphene.NonNull(TrackingEventType), default_value=[])
    messages = graphene.List(graphene.NonNull(MessageType), default_value=[])
    status = utils.TrackerStatusEnum(required=True)
    meta = generic.GenericScalar()
    options = generic.GenericScalar()
    metadata = generic.GenericScalar()

    class Meta:
        model = manager.Tracking
        exclude = (*manager.Tracking.HIDDEN_PROPS,)
        interfaces = (utils.CustomNode,)

    def resolve_carrier_id(self, info):
        return getattr(self.tracking_carrier, "carrier_id", None)

    def resolve_carrier_name(self, info):
        return getattr(self.tracking_carrier, "carrier_name", None)


class PaymentType(graphene.ObjectType):
    paid_by = utils.PaidByEnum(required=False)
    currency = utils.CurrencyCodeEnum(required=False)
    account_number = graphene.String()
    id = graphene.String()


class ShipmentType(utils.BaseObjectType):
    carrier_id = graphene.String()
    carrier_name = graphene.String()

    shipper = graphene.Field(AddressType, required=True)
    recipient = graphene.Field(AddressType, required=True)
    customs = graphene.Field(CustomsType)
    parcels = graphene.List(
        graphene.NonNull(ParcelType), required=True, default_value=[]
    )
    payment = graphene.Field(PaymentType, default_value={})

    service = graphene.String()
    services = graphene.List(
        graphene.NonNull(graphene.String), required=True, default_value=[]
    )
    carrier_ids = graphene.List(
        graphene.NonNull(graphene.String), required=True, default_value=[]
    )
    messages = graphene.List(
        graphene.NonNull(MessageType), required=True, default_value=[]
    )
    selected_rate_id = graphene.String()
    selected_rate = graphene.Field(RateType)
    rates = graphene.List(graphene.NonNull(RateType), default_value=[])

    options = generic.GenericScalar()
    meta = generic.GenericScalar()
    metadata = generic.GenericScalar(required=True, default_value={})
    tracker_id = graphene.String()

    label_type = utils.LabelTypeEnum()
    label_url = graphene.String()
    invoice_url = graphene.String()
    status = utils.ShipmentStatusEnum(required=True)
    tracker = graphene.Field(TrackerType)

    class Meta:
        model = manager.Shipment
        exclude = (*manager.Shipment.HIDDEN_PROPS,)
        interfaces = (utils.CustomNode,)

    def resolve_parcels(self, info):
        return self.parcels.all()

    def resolve_carrier_id(self, info):
        return getattr(self.selected_rate_carrier, "carrier_id", None)

    def resolve_carrier_ids(self, info):
        return getattr(self, "carrier_ids", None)

    def resolve_carrier_name(self, info):
        return getattr(self.selected_rate_carrier, "carrier_name", None)

    def resolve_tracker(self, info):
        return self.tracker


class ServiceLevelType(utils.BaseObjectType):
    class Meta:
        model = providers.ServiceLevel
        exclude = ("dhlpolandsettings_set",)
        interfaces = (utils.CustomNode,)


class LabelTemplateType(utils.BaseObjectType):
    template_type = utils.LabelTemplateTypeEnum()
    shipment_sample = generic.GenericScalar()

    class Meta:
        model = providers.LabelTemplate
        exclude = ("genericsettings",)
        interfaces = (utils.CustomNode,)


class BaseConnectionType:
    carrier_name = graphene.String(required=True)

    def resolve_carrier_name(self, info):
        return getattr(self, "settings", self).carrier_name


class SystemConnectionType(BaseConnectionType, utils.BaseObjectType):
    enabled = graphene.Boolean(required=True)

    class Meta:
        model = providers.Carrier
        fields = (
            "created_at",
            "updated_at",
            "id",
            "test_mode",
            "carrier_id",
            "carrier_name",
            "active",
            "capabilities",
        )

    def resolve_enabled(self, info):
        if hasattr(self, "active_orgs"):
            return self.active_orgs.filter(id=info.context.org.id).exists()

        return self.active_users.filter(id=info.context.user.id).exists()


class ConnectionType(graphene.Interface, BaseConnectionType):
    id = graphene.String(required=True)

    def resolve_id(self, info):
        return self.id


def CreateCarrierSettingTypes(carrier_model):
    _extra_fields: dict = dict(metadata=generic.GenericScalar(default_value={}))

    if hasattr(carrier_model, "account_country_code"):
        _extra_fields.update(account_country_code=graphene.String(required=False))

    if hasattr(carrier_model, "label_template"):
        _extra_fields.update(
            label_template=graphene.Field(LabelTemplateType),
        )

    if hasattr(carrier_model, "services"):

        def resolve_services(self, info):
            return self.services.all()

        _extra_fields.update(
            services=graphene.List(
                graphene.NonNull(ServiceLevelType), default_value=[]
            ),
            resolve_services=resolve_services,
        )

    class Meta:
        model = carrier_model
        exclude = ("carrier_ptr",)
        interfaces = (ConnectionType,)

    return type(
        carrier_model.__name__,
        (
            BaseConnectionType,
            utils.BaseObjectType,
        ),
        {"Meta": Meta, **_extra_fields},
    )


CarrierSettings = {
    f"{model.__name__.lower()}": CreateCarrierSettingTypes(model)
    for _, model in providers.MODELS.items()
}
