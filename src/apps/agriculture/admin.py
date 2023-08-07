from django.contrib import admin

from .models import *


class AgricultureAdmin(admin.ModelAdmin):
    list_display = ('date', "tree_type", "tree_plant", "hectare", "weight", "department", "region", "creator", "status",)



admin.site.register(AgricultureActual, AgricultureAdmin)
admin.site.register(AgriculturePlan, AgricultureAdmin)