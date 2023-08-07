from django.db import models
from ..accounts.models import STATES_STATUSES, Department, Region, User
from ..core.models import TimestampedModel
from ..trees.models import TreeTypes, TreePlant


class AgricultureActual(TimestampedModel):
    date            = models.DateTimeField()
    tree_type       = models.ForeignKey(TreeTypes, on_delete=models.CASCADE, related_name="agriculture_actual_tree_type")
    tree_plant      = models.ForeignKey(TreePlant, on_delete=models.CASCADE, related_name="agriculture_actual_plant")
    hectare         = models.FloatField(blank=True, null=True, verbose_name="Gektar hisobi")
    weight          = models.FloatField(blank=True, null=True, verbose_name="wight(tonna)")
    profit          = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    yield_area      = models.FloatField(blank=True, null=True, verbose_name="yield_area")
    show_yield_area = models.BooleanField(default=False)
    department      = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="agriculture_actual_department")
    region          = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="agriculture_actual_region")
    creator         = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="agriculture_actual_creator", blank=True, null=True)
    status          = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "agriculture_actual"
        verbose_name_plural = "AgricultureActual"


class AgriculturePlan(TimestampedModel):
    date        = models.DateTimeField()
    tree_type   = models.ForeignKey(TreeTypes, on_delete=models.CASCADE, related_name="agriculture_plan_tree_type")
    tree_plant  = models.ForeignKey(TreePlant, on_delete=models.CASCADE, related_name="agriculture_plan_plant")
    hectare     = models.FloatField(blank=True, null=True, verbose_name="Gektar hisobi")
    weight      = models.FloatField(blank=True, null=True, verbose_name="wight(tonna)")
    department  = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="agriculture_plan_department")
    region      = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="agriculture_plan_region")
    creator     = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="agriculture_plan_creator", blank=True, null=True)
    status      = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "agriculture_plan"
        verbose_name_plural = "AgriculturePlan"
