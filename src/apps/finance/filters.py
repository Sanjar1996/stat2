import django_filters

from .models import Finance, FinancePlan, ProductionServiceActual
from ..core.filters import BaseFilter


class FinanceActualFilter(BaseFilter):
    amount = django_filters.CharFilter()

    class Meta:
        model = Finance
        fields = ['region', 'department', 'department__name', "amount"]


class FinancePlanFilter(BaseFilter):
    class Meta:
        model = FinancePlan
        fields = ['region', 'department', 'department__name', "amount"]


class ProductionServiceActualFilter(BaseFilter):
    class Meta:
        model = ProductionServiceActual
        fields = ['region', 'department', 'department__name']




# if request.user.is_superuser:
#     print("SUperuser")
#     regions = Region.objects.filter(status=1).order_by('sort')
#     departments = Department.objects.filter(status=1).order_by('sort')
#     self.filters['region'].extra.update(queryset=regions)
#     self.filters['department'].extra.update(queryset=departments)

# class FinancePlanFilter(django_filters.FilterSet):
#     region = django_filters.filters.ModelChoiceFilter(queryset=Region.objects.filter(status=1))
#     department = django_filters.filters.ModelChoiceFilter(queryset=Department.objects.filter(status=1))
#     department__name = django_filters.CharFilter(lookup_expr='icontains')
#     amount = django_filters.CharFilter()
#
#     class Meta:
#         model = Finance
#         fields = ['region', 'department', 'department__name', "amount"]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         request = kwargs['request']
#         if request.user.is_authenticated:
#             print("CORE.PY>>>USER>>>", request.user)
#             regions = None
#             departments = None
#             reg_and_depart = UserDepartment.objects.filter(user=self.request.user)
#             for item_objects in reg_and_depart:
#                 regions = item_objects.regions.all().order_by('sort')
#                 departments = item_objects.departments.all().order_by('sort')
#             print("LEN_REGION", len(regions))
#             print("LEN_REGION", len(departments))
#             self.filters['region'].extra.update(queryset=regions)
#             self.filters['department'].extra.update(queryset=departments)
