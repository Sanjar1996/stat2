from .models import Sapling, Seed, Sprout, PrepairLand, TreeGroundPlanting
from ..core.filters import BaseFilter


class SaplingActualFilter(BaseFilter):
    class Meta:
        model = Sapling
        fields = ['region', 'department', 'department__name']


class SeedActualFilter(BaseFilter):
    class Meta:
        model = Seed
        fields = ['region', 'department', 'department__name']


class SproutActualFilter(BaseFilter):
    class Meta:
        model = Sprout
        fields = ['region', 'department', 'department__name']


class PrepairLandActualFilter(BaseFilter):
    class Meta:
        model = PrepairLand
        fields = ['region', 'department', 'department__name']


class TreeGroundPlantingActualFilter(BaseFilter):
    class Meta:
        model = TreeGroundPlanting
        fields = ['region', 'department', 'department__name']
