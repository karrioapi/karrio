from django.db.models import Q


class OrganizationAccess:
    def __call__(self, user, **kwargs):
        return (
            Q(created_by_id=user.id) |
            Q(created_by__organizations_organization__organization_users__user_id=user.id)
        )
