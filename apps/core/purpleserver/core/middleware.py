from django.db.models import Q


class CreatorAccess:
    def __call__(self, user, **kwargs):
        return Q(created_by_id=user.id)


class WideAccess:
    def __call__(self, *args, **kwargs):
        return Q()
