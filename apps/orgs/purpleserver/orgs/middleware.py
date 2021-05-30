from django.db.models import Q


class OrganizationAccess:
    def __call__(self, context, key: str = 'created_by', **kwargs):
        import purpleserver.orgs.models as orgs

        user_key = f'{key}__id'
        user = getattr(context, 'user', context)
        user_id = getattr(user, 'id', None)
        org = (
            getattr(context, 'org', None) or
            orgs.Organization.objects.filter(users__id=user_id, is_active=True).first()
        )
        org_id = getattr(org, 'id', None)

        return (
            Q(**{user_key: user_id, 'org__id': org_id})
            | Q(**{user_key: user_id, 'org': None})
        )
