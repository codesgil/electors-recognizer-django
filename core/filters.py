from django_filters import rest_framework as filters

from .models import Campaign, Vote, Elector, VoteOffice


class VoteFilter(filters.FilterSet):
    e_mat = filters.CharFilter(field_name='elector__matricule', lookup_expr='iexact')
    e_name = filters.CharFilter(field_name='elector__name', lookup_expr='icontains')
    campaign = filters.NumberFilter(field_name='campaign__id', lookup_expr='exact')
    voted = filters.BooleanFilter(lookup_expr='exact')
    created = filters.DateTimeFilter(field_name='created', lookup_expr='gte')
    created_lt = filters.DateTimeFilter(field_name='created', lookup_expr='lt')
    created_gt = filters.DateTimeFilter(field_name='created', lookup_expr='gt')
    created_lte = filters.DateTimeFilter(field_name='created', lookup_expr='lte')
    created_gte = filters.DateTimeFilter(field_name='created', lookup_expr='gte')

    class Meta:
        model = Vote
        fields = {
            'id': ['exact'],
        }


class VoteOfficeFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='enabled', lookup_expr='icontains')
    enabled = filters.BooleanFilter(field_name='enabled', lookup_expr='exact')

    class Meta:
        model = VoteOffice
        fields = {
            'id': ['exact'],
        }


class CampaignFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='enabled', lookup_expr='icontains')
    enabled = filters.BooleanFilter(field_name='enabled', lookup_expr='exact')

    class Meta:
        model = Campaign
        fields = {
            'id': ['exact'],
        }


class ElectorFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    phone = filters.CharFilter(lookup_expr='icontains')
    gender = filters.CharFilter(lookup_expr='icontains')
    surname = filters.CharFilter(lookup_expr='icontains')
    birthPlace = filters.CharFilter(lookup_expr='icontains')
    birthDate = filters.DateFilter(lookup_expr='exact')
    localisation = filters.CharFilter(lookup_expr='icontains')
    matricule = filters.CharFilter(lookup_expr='iexact')
    created = filters.DateTimeFilter(field_name='created', lookup_expr='gte')
    created_lt = filters.DateTimeFilter(field_name='created', lookup_expr='lt')
    created_gt = filters.DateTimeFilter(field_name='created', lookup_expr='gt')
    created_lte = filters.DateTimeFilter(field_name='created', lookup_expr='lte')
    created_gte = filters.DateTimeFilter(field_name='created', lookup_expr='gte')

    class Meta:
        model = Elector
        fields = {
            'id': ['exact'],
        }
