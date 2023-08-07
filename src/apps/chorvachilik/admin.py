from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from ..chorvachilik.models import *
from .resources import AnimalResource

class ChorvachilikTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "status")


class ChorvachilikAdmin(admin.ModelAdmin):
    list_display = ("name", "parent_id",  "id", "get_type", "show_yield_area", "status",)
    list_filter = ("name", "type")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "status")


class ChorvachilikActualAdmin(admin.ModelAdmin):
    list_display = ("date", "chorvachilik", "amount", "department", "region", "creator", "chorvachilik_type", "status")


class InputOutputAdmin(admin.ModelAdmin):
    list_display = ("category", "amount", "weight", "type", "animal", "department", "region", "status", "creator")


class AnimalCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "status")


class UploadFileAdmin(admin.ModelAdmin):
    list_display = ('name', "file", "output")


class AnimalAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "status",)
    list_filter = ("category",)


class AnimalResourceAdmin(AnimalAdmin, ImportExportModelAdmin):
    list_display = ("name", "category", "status",)
    list_filter = ("category",)
    resource_class = AnimalResource


admin.site.register(AnimalCategory, AnimalCategoryAdmin)
admin.site.register(ChorvaInputOutputCategory, CategoryAdmin)
admin.site.register(Animal, AnimalResourceAdmin)
admin.site.register(ChorvaInputOutput, InputOutputAdmin)
admin.site.register(ChorvachilikActual, ChorvachilikActualAdmin)
admin.site.register(ChorvachilikPlan, ChorvachilikActualAdmin)
admin.site.register(Chorvachilik, ChorvachilikAdmin)
admin.site.register(ChorvachilikTypes, ChorvachilikTypeAdmin)
admin.site.register(UploadFile, UploadFileAdmin)
