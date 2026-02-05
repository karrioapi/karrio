import django_filters
import karrio.lib as lib


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class FilterSet(django_filters.FilterSet):
    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        from django.http import QueryDict

        if isinstance(data, QueryDict):
            # REST path: QueryDict collapses lists on spread; use getlist
            # to preserve multi-value fields.
            _data = {}
            for key in data:
                base_filter = self.base_filters.get(key)
                if base_filter is not None and base_filter.__class__ == CharInFilter:
                    _data[key] = ",".join(data.getlist(key))
                elif base_filter is not None and isinstance(
                    base_filter, django_filters.MultipleChoiceFilter
                ):
                    _data[key] = data.getlist(key)
                else:
                    _data[key] = data[key]
            data = _data
        elif data is not None:
            # GraphQL path: regular dict with list values for CharInFilter
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

    def to_dict(self):
        self.form.is_valid()
        return lib.to_dict(self.form.cleaned_data)
