from django.db.models import Q


class CreatorAccess:
    def __call__(self, context, key: str = 'created_by', **kwargs) -> Q:
        user_key = f'{key}_id'
        user = getattr(context, 'user', user)

        return Q(**{user_key: getattr(user, 'id', None)})


class WideAccess:
    def __call__(self, *args, **kwargs) -> Q:
        return Q()


class UserToken:
    def __call__(self, context, **kwargs) -> dict:
        return dict(user=getattr(context, 'user', context))
