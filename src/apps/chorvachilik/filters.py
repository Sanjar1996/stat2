from .models import ChorvachilikActual, ChorvaInputOutput
from ..core.filters import BaseFilter


class ChorvachilikActualFilter(BaseFilter):
    class Meta:
        model = ChorvachilikActual
        fields = ['region', 'department', 'department__name']


class ChorvaInputOutputFilter(BaseFilter):
    class Meta:
        model = ChorvaInputOutput
        fields = ['region', 'department', 'department__name']