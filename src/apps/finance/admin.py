from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models import *


class LogEntryAdmin(admin.ModelAdmin):
    """
        action_time
        user
        content_type
        object_id
        object_repr
        action_flag
        change_message
    """
    list_display = ['action_time', 'user', 'content_type', 'action_flag', 'change_message', 'object_id']
    list_filter = ['change_message']


class FinanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'amount', 'department', 'region', 'creator', 'type', 'amount_type', 'status')
    list_display_links = ('date',)
    list_filter = ('date', 'department', 'type')


class FinancePlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'amount', 'department', 'region', 'creator', 'status', 'amount_type')
    list_display_links = ('date',)
    list_filter = ('department',)


class FinanceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    list_display_links = ('name',)


class Production(admin.ModelAdmin):
    list_display = ("date", "production", "paid_service", "department", "region", "creator", "status")


admin.site.register(Finance, FinanceAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(FinancePlan, FinancePlanAdmin)
admin.site.register(FinanceType, FinanceTypeAdmin)
admin.site.register(ProductionServiceActual, Production)
admin.site.register(ProductionServicePlan, Production)
