from django.contrib import admin
from .models import *


class ReportAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ("id", "name", "status", "type", "kind")


class ReportGroupAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ("id", "name", "status")


class ReportKeyAdmin(admin.ModelAdmin):
    search_fields = ['name', 'report_group_one.name', 'report_group_two.name']
    list_display = ("name", "id", "value_type", "report_group_one", "report_group_two", "status", "sort")


class ReportValueAdmin(admin.ModelAdmin):
    list_display = ('date', "report_id", "report_key", "department", "region", "double", "string")


admin.site.register(Report, ReportAdmin)
admin.site.register(ReportGroup, ReportGroupAdmin)
admin.site.register(ReportKey, ReportKeyAdmin)
admin.site.register(ReportValue, ReportValueAdmin)
