import django_filters


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class FilterSet(django_filters.FilterSet):
    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        data = {
            **data,
            **{
                key: (
                    ",".join(val)
                    if self.base_filters.get(key).__class__ == CharInFilter
                    else val
                )
                for key, val in data.items()
            },
        }
        super().__init__(data, queryset, request=request, prefix=prefix)
