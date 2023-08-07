from django.db import models
from apps.accounts.models import User, Department, Region
from apps.core.models import TimestampedModel

from ..accounts.models import STATES_STATUSES

AMOUNT_TYPE = (
    (1, "Ho'jalik"),
    (2, "HUSUSIY SECTOR"),
)

STATUS = ((1, "NEW"), (2, "CONFIRM"), (3, "DELETE"))


class FinanceType(TimestampedModel):
    name = models.CharField(max_length=50, blank=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "finance_type"
        verbose_name_plural = "FinanceType"


class Finance(TimestampedModel):
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="finance_department")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="finance_region")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="finance_creator", blank=True, null=True)
    type = models.ForeignKey(FinanceType, on_delete=models.CASCADE, related_name="finance_type", blank=True, null=True)
    amount_type = models.IntegerField(choices=AMOUNT_TYPE, default=1)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)
    state = models.IntegerField(choices=STATUS, default=1)

    def __int__(self):
        return self.id

    class Meta:
        ordering = ['-id']
        db_table = "finance"
        verbose_name_plural = "Finance"


class FinancePlan(TimestampedModel):
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="finance_plan_department")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="finance_plan_region")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="finance_plan_creator", blank=True,
                                null=True)
    amount_type = models.IntegerField(choices=AMOUNT_TYPE, default=1)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "finance_plan"
        verbose_name_plural = "FinancePlan"


class ProductionServiceActual(TimestampedModel):
    date = models.DateTimeField()
    production = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    paid_service = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "production_service_actual"
        verbose_name_plural = "ProductionServiceActual"


class ProductionServicePlan(TimestampedModel):
    date = models.DateTimeField()
    production = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    paid_service = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "production_service_plan"
        verbose_name_plural = "ProductionServicePlan"
