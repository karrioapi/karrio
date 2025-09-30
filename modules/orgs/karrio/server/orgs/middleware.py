from django.db.models import Q


class OrganizationAccess:
    def __call__(self, context, key: str = "created_by", **kwargs):
        import karrio.server.orgs.models as orgs

        user_key = f"{key}"
        user = getattr(context, "user", context)
        user_id = getattr(user, "id", None)
        org = (
            getattr(context, "org", None)
            or orgs.Organization.objects.filter(
                users__id=user_id, is_active=True
            ).first()
        )
        org_id = getattr(org, "id", None)

        return Q(**{"org__id": org_id, "org__users__id": user_id}) | Q(
            **{user_key: user_id, "org": None}
        )
