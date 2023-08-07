from .models import AgricultureActual, AgriculturePlan
from ..core.filters import BaseFilter


class AgricultureActualFilter(BaseFilter):
    class Meta:
        model = AgricultureActual
        fields = ['region', 'department', 'department__name']


class FinancePlanFilter(BaseFilter):
    class Meta:
        model = AgriculturePlan
        fields = ['region', 'department', 'department__name']
