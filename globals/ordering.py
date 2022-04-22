from rest_framework.filters import OrderingFilter


class CustomOrdering(OrderingFilter):
    allowed_custom_filters = []
    fields_related = {}

    def get_ordering(self, request, queryset, view):
        self.allowed_custom_filters = getattr(view, 'allowed_custom_filters', [])
        self.fields_related = getattr(view, 'fields_related', {})
        params = request.query_params.get(self.ordering_param)
        if params:
            fields = [param.strip() for param in params.split(',')]
            ordering = [f for f in fields if f.lstrip('-') in self.allowed_custom_filters]
            if ordering:
                return ordering

        return self.get_default_ordering(view)

    def filter_queryset(self, request, queryset, view):
        order_fields = []
        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            for field in ordering:
                symbol = "-" if "-" in field else ""
                order_fields.append(symbol + self.fields_related[field.lstrip('-')])
        if order_fields:
            return queryset.order_by(*order_fields)

        return queryset
