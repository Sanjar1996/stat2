import django_filters

from .service import get_current_user_regions_and_departments_qs
from ..accounts.models import UserDepartment, Region, Department


class BaseFilter(django_filters.FilterSet):
    region = django_filters.filters.ModelChoiceFilter(queryset=Region.objects.all())
    department = django_filters.filters.ModelChoiceFilter(queryset=Department.objects.all())
    department__name = django_filters.CharFilter(lookup_expr='icontains')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = kwargs['request']
        if request.user.is_authenticated:
            regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
            self.filters['region'].extra.update(queryset=regions)
            self.filters['department'].extra.update(queryset=departments)
