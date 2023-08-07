from django.db import models

from ..accounts.models import Department, STATES_STATUSES, User, Region
from ..core.models import TimestampedModel

AMOUNT_TYPES = (
    (1, "PCS"),
    (2, "KG"),
    (3, "HEAD"),
    (4, "TON"),
    (5, "FAMILY"),
)
STATUS = ((1, "NEW"), (2, "CONFIRM"), (3, "DELETE"))
INPUT_OUTPUT_TYPES = ((1, "INPUT"), (2, "OUTPUT"))


class ChorvachilikTypes(TimestampedModel):
    name = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'chorvachilik_types'
        verbose_name_plural = "ChorvachilikType"


class Chorvachilik(TimestampedModel):
    name = models.CharField(max_length=128, blank=True, null=True)
    type = models.ManyToManyField(ChorvachilikTypes, related_name="chorvachilik_type", blank=True)
    show_yield_area = models.BooleanField(default=False)
    profit = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)
    parent = models.ForeignKey('self', related_name='child_chorva', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    def get_type(self):
        return " | ".join(item.name for item in self.type.all())

    class Meta:
        db_table = "chorvachilik"
        verbose_name_plural = "Chorvachilik"


class ChorvachilikPlan(TimestampedModel):
    date = models.DateField()
    chorvachilik_type = models.ForeignKey(ChorvachilikTypes, on_delete=models.CASCADE,
                                          related_name="chorvachilik_plan_type", blank=True, null=True)
    chorvachilik = models.ForeignKey(Chorvachilik, on_delete=models.CASCADE,
                                     related_name="chorvachilik_plan_chorvachilik", blank=True, null=True)
    amount = models.FloatField(blank=True, null=True, verbose_name="Amount")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="chorvachilik_plan_department")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="chorvachilik_plan_region")
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chorvachilik_plan_creator", blank=True, null=True)
    amount_type = models.IntegerField(choices=AMOUNT_TYPES, default=1)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __str__(self):
        return f'ID: {self.id}'

    class Meta:
        db_table = "chorvachilik_plan"
        verbose_name_plural = "ChorvachilikPlan"


class ChorvachilikActual(TimestampedModel):
    date = models.DateField()
    chorvachilik = models.ForeignKey(Chorvachilik, on_delete=models.CASCADE,
                                     related_name="chorvachilik_actual_chorvachilik", blank=True,
                                     null=True)
    chorvachilik_type = models.ForeignKey(ChorvachilikTypes, on_delete=models.CASCADE,
                                          related_name="chorvachilik_actual_type", blank=True,
                                          null=True)
    amount = models.FloatField(blank=True, null=True, verbose_name="Amount")
    profit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="chorvachilik_actual_department")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="chorvachilik_actual_region")
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chorvachilik_actual_creator", blank=True, null=True)
    amount_type = models.IntegerField(choices=AMOUNT_TYPES, default=1)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "chorvachilik_actual"
        verbose_name_plural = "ChorvachilikActual"


class AnimalCategory(TimestampedModel):
    name = models.CharField(max_length=120, verbose_name="Animal")
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "animal_category"
        verbose_name_plural = "AnimalCategory"


class Animal(TimestampedModel):
    name = models.CharField(max_length=120, verbose_name="Animal")
    category = models.ForeignKey(AnimalCategory, on_delete=models.CASCADE, related_name="animal_category", null=True,
                                 blank=True)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "animal"
        verbose_name_plural = "Animal"


class ChorvaInputOutputCategory(TimestampedModel):
    name = models.CharField(max_length=256, verbose_name="Kirim yoki chiqim category")
    type = models.IntegerField(choices=INPUT_OUTPUT_TYPES, default=1)
    status = models.IntegerField(choices=STATES_STATUSES, default=1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'chorva_input_output_category'
        verbose_name_plural = "ChorvaInputOutputCategory"


class ChorvaInputOutput(TimestampedModel):
    date = models.DateField()
    category = models.ForeignKey(ChorvaInputOutputCategory, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True, verbose_name="Boshi")
    weight = models.FloatField(blank=True, null=True, verbose_name="Vazni")
    type = models.IntegerField(choices=INPUT_OUTPUT_TYPES, default=1)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "chorva_input_output"
        verbose_name_plural = "ChorvaInputOutput"


class UploadFile(TimestampedModel):
    name = models.CharField(max_length=256, null=True, blank=True)
    file = models.FileField(upload_to='output/', null=True, blank=True)
    output = models.ForeignKey(ChorvaInputOutput, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.file}"

    def image_tag(self):
        from django.utils.html import mark_safe
        img = mark_safe(f"<img src='{self.file.url}' width='250' />")
        return img

    class Meta:
        db_table = "upload_file"
        verbose_name_plural = "UploadFile"
