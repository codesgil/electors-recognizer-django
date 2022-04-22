from django_filters import rest_framework as filters
from .models import User


class UserFilter(filters.FilterSet):
    username = filters.CharFilter(lookup_expr='icontains')
    role = filters.CharFilter(lookup_expr='icontains')
    is_active = filters.BooleanFilter(lookup_expr='exact')
    p_id = filters.NumberFilter(field_name='profile__id', lookup_expr='exact')
    p_first_name = filters.CharFilter(field_name='profile__first_name', lookup_expr='icontains')
    p_last_name = filters.CharFilter(field_name='profile__last_name', lookup_expr='icontains')
    p_phone = filters.CharFilter(field_name='profile__phone', lookup_expr='icontains')
    p_email = filters.CharFilter(field_name='profile__email', lookup_expr='icontains')

    class Meta:
        model = User
        fields = {
            'id': ['exact'],
        }
