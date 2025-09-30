import karrio.server.conf as conf
import karrio.server.user.models as models
import karrio.server.serializers as serializers


@serializers.owned_model_serializer
class TokenSerializer(serializers.Serializer):
    label = serializers.CharField(required=False)

    def create(
        self, validated_data: dict, context: serializers.Context
    ) -> models.Token:
        return models.Token.objects.create(
            user=context.user,
            test_mode=context.test_mode,
            label=validated_data.get("label") or "Default API Key",
        )

    @staticmethod
    def retrieve_token(context, org_id: str = None):
        org = getattr(context, "org", None)
        org_id = org_id or getattr(org, "id", None)

        queyset = models.Token.objects.filter(
            **{
                "test_mode": getattr(context, "test_mode", None),
                "user__id": getattr(getattr(context, "user", None), "id", None),
                **({"org__id": org_id} if org_id is not None else {}),
            }
        )

        if queyset.exists():
            return queyset.first()

        if org_id is not None and conf.settings.MULTI_ORGANIZATIONS:
            import karrio.server.orgs.models as orgs

            org = orgs.Organization.objects.get(id=org_id, users__id=context.user.id)

        ctx = serializers.Context(
            org=org,
            user=getattr(context, "user", None),
            test_mode=getattr(context, "test_mode", None),
        )

        return TokenSerializer.map(data={}, context=ctx).save().instance
