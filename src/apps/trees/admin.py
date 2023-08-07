from django.contrib import admin
from .models import *


class TreeCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', "name", "status")


class TreeTypesAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "show_profit", "status")
    list_filter = ("show_profit", "name")


class TreeHeightReportAdmin(admin.ModelAdmin):
    list_display = ("tree_plan",
                    "height_0_0_2_count",
                    "height_0_2_5_count",
                    "height_0_5_1_count",
                    "height_1_1_5_count",
                    "height_1_5_2_count",
                    "height_2_count",
                    "date",
                    "region",
                    "department",
                    "status")
    list_filter = ('tree_plan', 'region__name', 'department__name')


class TreePlantAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "category", 'sort',
                    "_types", "is_show_sprouting", "is_show_seed", "is_show_sapling", "is_show_height", "status")

    list_filter = ("is_show_sprouting", "is_show_seed", "is_show_sapling", "is_show_height", "category", "types")

    search_fields = ('name',)


class SaplingAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'count', 'department', 'region', 'creator', 'plant', 'status')
    list_display_links = ('date',)


class InputAdmin(admin.ModelAdmin):
    list_display = (
        "date", "plant", "category", "donation", "buying", "new_sprout", "department", "region", "creator", "status",)
    list_display_links = ('date',)


class OutputAdmin(admin.ModelAdmin):
    list_display = (
        "date", "plant", "category", "for_the_forest", "donation", "selling", "unsuccessful",
        "place_changed", "out_of_count", "department", "region", "creator", "status")
    list_display_links = ('date',)


class LandAdmin(admin.ModelAdmin):
    list_display = ("date", "hectare", "region", "department", "categories", "creator", "status")
    list_display_links = ('date',)


class TreeContractCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    list_display_links = ("name",)


class TreeContractPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "tree_count", "date", "region", "department", )
    search_fields = ("region__name", "department__name", )
    list_display_links = ("department",)


class TreeContractAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "count", "amount", "payout", "output_tree",
                    "date", "region", "department", "status")
    list_display_links = ("category",)


admin.site.register(TreeContractCategory, TreeContractCategoryAdmin)
admin.site.register(TreeContractPlan, TreeContractPlanAdmin)
admin.site.register(TreeContract, TreeContractAdmin)

admin.site.register(LandCategory, TreeCategoryAdmin)
admin.site.register(PrepairLand, LandAdmin)
admin.site.register(PrepairLandPlan, LandAdmin)
admin.site.register(SproutInput, InputAdmin)
admin.site.register(SproutOutput, OutputAdmin)

admin.site.register(SaplingInput, InputAdmin)
admin.site.register(SaplingOutput, OutputAdmin)

admin.site.register(Sprout, SaplingAdmin)
admin.site.register(SproutPlan, SaplingAdmin)

admin.site.register(SaplingPlan, SaplingAdmin)

admin.site.register(Sapling, SaplingAdmin)
admin.site.register(TreeGroundPlanting)
admin.site.register(TreeGroundPlantingPlan)

admin.site.register(Seed, SaplingAdmin)
admin.site.register(SeedPlan, SaplingAdmin)

admin.site.register(TreeCategory, TreeCategoryAdmin)
admin.site.register(TreeTypes, TreeTypesAdmin)
admin.site.register(TreePlant, TreePlantAdmin)

admin.site.register(TreeHeightReport, TreeHeightReportAdmin)
