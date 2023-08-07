from random import choices

from django.db import models
from ..core.models import TimestampedModel

from ..accounts.models import Department, Region

STATUSES = ((1, 'ACTIVE'), (2, 'DELETED'))

REPORT_TYPES = (
    (1, 'Moliya'),
    (2, 'Urmon-barpo'),
    (3, 'Chorvachilik'),
    (4, "Qishloq-xo'jaligi"),
    (5, "O'rmon maxsulotlari"),
    (6, 'Tanlanmagan'),
)


class ReportKind(models.IntegerChoices):
    SUMMARY = 1  # Kiritilgan reportlar yig'indisi chiqishi kerak bo'lsa
    LISTED = 2  # Xar bir kiritilgan hisobot alohida chiqishi uchun


class Report(TimestampedModel):
    name = models.CharField(max_length=264, blank=True)
    status = models.IntegerField(choices=STATUSES, default=1)
    type = models.IntegerField(choices=REPORT_TYPES, default=6)  # Bo'limlarga ajratib olish uchun
    kind = models.IntegerField(choices=ReportKind.choices, default=1)  # Report type summary or listed
    description = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'report'
        verbose_name_plural = 'Report'


class ReportGroup(models.Model):
    name = models.CharField(max_length=264, blank=True)
    status = models.IntegerField(choices=STATUSES, default=1)

    # def __int__(self):
    #     return self.id
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'report_group'
        verbose_name_plural = 'ReportGroup'


class ReportKey(models.Model):
    report = models.ForeignKey(Report, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=264, blank=True)
    query_code = models.TextField(blank=True, null=True, verbose_name="QUERY OR SQL CODE")
    status = models.IntegerField(choices=STATUSES, default=1)
    VALUE_TYPES = ((1, 'Double'), (2, 'String'), (3, "QUERY OR SQL"))
    value_type = models.IntegerField(choices=VALUE_TYPES, default=1)
    report_group_one = models.ForeignKey(ReportGroup,
                                         on_delete=models.SET_NULL,
                                         related_name="report_group_one",
                                         blank=True, null=True)
    report_group_two = models.ForeignKey(ReportGroup,
                                         on_delete=models.SET_NULL,
                                         related_name="report_group_two",
                                         blank=True, null=True)
    sort = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def report_name(self):
        return f"{self.report.name}/ Report-ID {self.report.id}"

    # def report_one(self):
    #     return f"{self.report_group_one.name[:20]}"
    #
    # def report_two(self):
    #     return f"{self.report_group_two}"

    class Meta:
        db_table = 'report_key'
        verbose_name_plural = 'ReportKey'


class ReportValue(TimestampedModel):
    date = models.DateTimeField()
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE, blank=True, null=True)
    report_key = models.ForeignKey(ReportKey, on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    double = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    string = models.CharField(max_length=264, blank=True, null=True)
    status = models.IntegerField(choices=STATUSES, default=1)

    def __int__(self):
        return self.id

    class Meta:
        db_table = 'report_value'
        verbose_name_plural = 'ReportValue'
