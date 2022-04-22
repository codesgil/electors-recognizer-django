from django_filters import rest_framework as filters
from django.db.models import Q


class Many2ManyFilters(filters.Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        values = value.split(',')
        kwargs = None
        for v in values:
            key = self.field_name + '__' + self.lookup_expr
            if not kwargs:
                kwargs = Q(**{key: v.strip()})
            else:
                kwargs |= Q(**{key: v.strip()})
        if kwargs:
            qs = qs.filter(kwargs)
        return qs
