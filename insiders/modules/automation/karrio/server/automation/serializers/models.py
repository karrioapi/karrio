import karrio.server.serializers as serializers
import karrio.server.automation.models as models


# -----------------------------------------------------------
# workflow related serializers
# -----------------------------------------------------------
# region


@serializers.owned_model_serializer
class WorkflowModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Workflow
        exclude = ["created_at", "updated_at", "created_by"]


@serializers.owned_model_serializer
class WorkflowConnectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorkflowConnection
        exclude = ["created_at", "updated_at", "created_by"]


@serializers.owned_model_serializer
class WorkflowActionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorkflowAction
        exclude = ["created_at", "updated_at", "created_by"]


@serializers.owned_model_serializer
class WorkflowEventModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorkflowEvent
        exclude = ["created_at", "updated_at", "created_by"]


@serializers.owned_model_serializer
class WorkflowTriggerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorkflowTrigger
        exclude = ["created_at", "updated_at", "created_by"]


# endregion


# -----------------------------------------------------------
# shipping rule related serializers
# -----------------------------------------------------------
# region


@serializers.owned_model_serializer
class ShippingRuleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShippingRule
        exclude = ["created_at", "updated_at", "created_by"]


# endregion
