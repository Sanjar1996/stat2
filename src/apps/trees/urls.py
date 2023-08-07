from django.urls import path
from .views import *

app_name = 'trees'

urlpatterns = [
    # Trees Plan
    path('dashboard', TreesDashboard.as_view(), name="dashboard"),
    path('action/dashboard', TreeActionDashboard.as_view(), name="action_dashboard"),

    path('list/', TreePlantList.as_view(), name="name_list"),
    path('create/', TreePlantCreate.as_view(), name="name_create"),
    path('detail/<int:pk>/', TreePlantDetail.as_view(), name="name_detail"),
    path('name/<int:pk>/delete', TreePlantDeleteView.as_view(), name='name_delete'),

    # TREE_TYPES CRUD
    path('tree/type/list/', TreeTypeList.as_view(), name="tree_type_list"),
    path('tree/type/create/', TreeTypeCreate.as_view(), name="tree_type_create"),
    path('tree/type/detail/<int:pk>/', TreeTypeDetail.as_view(), name="tree_type_detail"),
    path('tree/type/<int:pk>/delete', TreeTypeDeleteView.as_view(), name='tree_type_delete'),

    # TreeHeightReport CRUD
    path('tree/', TreeHeightReportList.as_view(), name="tree_list"),
    path('tree/create/', TreeHeightCreate.as_view(), name="tree_create"),
    path('tree/detail/<int:pk>', TreeHeightReportDetail.as_view(), name="tree_detail"),
    path('tree/<int:pk>/delete', TreeHeightReportDeleteView.as_view(), name='tree_delete'),

    # TreeHeightReport Department Info
    path('tree/height/department/<int:pk>', get_tree_height_by_department, name="tree_height_department"),

    # TreeContract CRUD
    path('tree/tree_contract/list', TreeContractList.as_view(), name="tree_contract_list"),
    path('tree/tree_contract/create/', TreeContactCreate.as_view(), name="tree_contract_create"),
    path('tree/tree_contract/detail/<int:pk>', TreeContractDetail.as_view(), name="tree_contract_detail"),
    path('tree/tree_contract/<int:pk>/delete', TreeContractDeleteView.as_view(), name='tree_contract_delete'),

    # TreeContractPlan CRUD
    path('tree/contract/action/dashboard', TreeContractActionDashboard.as_view(),
         name="tree_contract_action_dashboard"),
    path('tree/tree_contract/plan/list', TreeContractPlanList.as_view(), name="tree_contract_plan_list"),
    path('tree/tree_contract/plan/create/', TreeContactPlanCreate.as_view(), name="tree_contract_plan_create"),
    path('tree/tree_contract/plan/detail/<int:pk>', TreeContractPlanDetail.as_view(), name="tree_contract_plan_detail"),
    path('tree/tree_contract/plan/<int:pk>/delete', TreeContractPlanDeleteView.as_view(),
         name='tree_contract_plan_delete'),

    # TreeCategories
    path('category/list', TreeCategoryList.as_view(), name="category_list"),
    path('category/create/', TreeCategoryCreate.as_view(), name="category_create"),
    path('category/detail/<int:pk>', TreeCategoryDetail.as_view(), name="category_detail"),
    path('category/<int:pk>/delete', TreeCategoryDeleteView.as_view(), name='category_delete'),

    # Sapling -> Ko'chat
    path('sapling/dashboard', SaplingDashboard.as_view(), name="sapling_dashboard"),
    path('yopiq/ildizli/dashboard', YopiqIldizDashboard.as_view(), name="yopiq_ildiz_dashboard"),

    path('sapling/list', SaplingList.as_view(), name="sapling_list"),
    path('sapling/create/', SaplingCreate.as_view(), name="sapling_create"),
    path('sapling/detail/<int:pk>', SaplingDetail.as_view(), name="sapling_detail"),
    path('sapling/<int:pk>/delete', SaplingDeleteView.as_view(), name='sapling_delete'),

    # SuplingPlan -> Ko'chatPlan
    path('sapling/plan/list', SaplingPlanList.as_view(), name="sapling_plan_list"),
    path('sapling/plan/create/', SaplingPlanCreate.as_view(), name="sapling_plan_create"),
    path('sapling/plan/detail/<int:pk>', SaplingPlanDetail.as_view(), name="sapling_plan_detail"),
    path('sapling/plan/<int:pk>/delete', SaplingPlanDeleteView.as_view(), name='sapling_plan_delete'),

    # Sapling Input -> Ko'chatlar kirim
    path('sapling/input/list', SaplingInputList.as_view(), name="sapling_input_list"),
    path('sapling/input/create/', SaplingInputCreate.as_view(), name="sapling_input_create"),
    path('sapling/input/detail/<int:pk>', SaplingInputDetail.as_view(), name="sapling_input_detail"),
    path('sapling/input/<int:pk>/delete', SaplingInputDeleteView.as_view(), name='sapling_input_delete'),

    # Sapling Output -> Ko'chatlar Chiqim
    path('sapling/output/list', SaplingOutputList.as_view(), name="sapling_output_list"),
    path('sapling/output/create/', SaplingOutputCreate.as_view(), name="sapling_output_create"),
    path('sapling/output/detail/<int:pk>', SaplingOutputDetail.as_view(), name="sapling_output_detail"),
    path('sapling/output/<int:pk>/delete', SaplingOutputDeleteView.as_view(), name='sapling_output_delete'),

    # Sedd -> Urug
    path('seed/dashboard', SeedDashboard.as_view(), name="seed_dashboard"),
    path('seed/list', SeedList.as_view(), name="seed_list"),
    path('seed/create/', SeedCreate.as_view(), name="seed_create"),
    path('seed/detail/<int:pk>', SeedDetail.as_view(), name="seed_detail"),
    path('seed/<int:pk>/delete', SeedDeleteView.as_view(), name='seed_delete'),

    # SeddPlan -> UrugPlan
    path('seed/plan/list', SeedPlanList.as_view(), name="seed_plan_list"),
    path('seed/plan/create/', SeedPlanCreate.as_view(), name="seed_plan_create"),
    path('seed/plan/detail/<int:pk>', SeedPlanDetail.as_view(), name="seed_plan_detail"),
    path('seed/plan/<int:pk>/delete', SeedPlanDeleteView.as_view(), name='seed_plan_delete'),

    # PrepairLand-> URUG SEPISH
    path('land/list', PrepairLandList.as_view(), name="land_list"),
    path('land/create/', PrepairLandCreate.as_view(), name="land_create"),
    path('land/detail/<int:pk>', PrepairLandDetail.as_view(), name="land_detail"),
    path('land/<int:pk>/delete', PrepairLandDeleteView.as_view(), name='land_delete'),

    # PrepairLandPlan -> URUG SEPISH PLAN
    path('land/dashboard', PrepairLandDashboard.as_view(), name="land_dashboard"),
    path('land/plan/list', LandPlanList.as_view(), name="land_plan_list"),
    path('land/plan/create/', LandPlanCreate.as_view(), name="land_plan_create"),
    path('land/plan/detail/<int:pk>', LandPlanDetail.as_view(), name="land_plan_detail"),
    path('land/plan/<int:pk>/delete', LandPlanDeleteView.as_view(), name='land_plan_delete'),

    # SproutInput -> Nihol-Kirim
    path('sprout/input/list', SproutInputList.as_view(), name="sprout_input_list"),
    path('sprout/input/create/', SproutInputCreate.as_view(), name="sprout_input_create"),
    path('sprout/input/detail/<int:pk>', SproutInputDetail.as_view(), name="sprout_input_detail"),
    path('sprout/input/<int:pk>/delete', SproutInputDeleteView.as_view(), name='sprout_input_delete'),

    # SproutOutput -> Nihol-Chiqim
    path('sprout/output/list', SproutOutputList.as_view(), name="sprout_output_list"),
    path('sprout/output/create/', SproutOutputCreate.as_view(), name="sprout_output_create"),
    path('sprout/output/detail/<int:pk>/', SproutOutputDetail.as_view(), name="sprout_output_detail"),
    path('sprout/output/<int:pk>/delete', SproutOutputDeleteView.as_view(), name='sprout_output_delete'),

    # Sprout -> Hihol
    path('sprout/dashboard', SproutDashboard.as_view(), name="sprout_dashboard"),
    path('sprout/list', SproutList.as_view(), name="sprout_list"),
    path('sprout/create/', SproutCreate.as_view(), name="sprout_create"),
    path('sprout/detail/<int:pk>', SproutDetail.as_view(), name="sprout_detail"),
    path('sprout/<int:pk>/delete', SproutDeleteView.as_view(), name='sprout_delete'),

    # SproutPlan -> NiholPlan
    path('sprout/plan/list', SproutPlanList.as_view(), name="sprout_plan_list"),
    path('sprout/plan/create/', SproutPlanCreate.as_view(), name="sprout_plan_create"),
    path('sprout/plan/detail/<int:pk>', SproutPlanDetail.as_view(), name="sprout_plan_detail"),
    path('sprout/plan/<int:pk>/delete', SproutPlanDeleteView.as_view(), name='sprout_plan_delete'),

    # Tree-Ground-planting -> Daraxt ekish (URMON BARPO QILISH)
    # path('the_growing_plant/dashboard', TheGrowingPlanDashboard.as_view(), name="sprout_dashboard"),
    path('the_growing_plant/list', TheGrowingPlantList.as_view(), name="the_growing_plant_list"),
    path('the_growing_plant/create/', TheGrowingPlantCreate.as_view(), name="the_growing_plant_create"),
    path('the_growing_plant/detail/<int:pk>', TheGrowingPlantDetail.as_view(), name="the_growing_plant_detail"),
    path('the_growing_plant/<int:pk>/delete', TheGrowingPlantDeleteView.as_view(), name='the_growing_plant_delete'),

    # The-Ground-planting -> Daraxt ekish plan
    path('the_growing_plant/plan/list', TheGrowingPlantPlanList.as_view(), name="the_growing_plant_plan_list"),
    path('the_growing_plant/plan/create/', TheGrowingPlantPlanCreate.as_view(), name="the_growing_plant_plan_create"),
    path('the_growing_plant/plan/detail/<int:pk>', TheGrowingPlantPlanDetail.as_view(),
         name="the_growing_plant_plan_detail"),
    path('the_growing_plant/plan/<int:pk>/delete', TheGrowingPlantPlanDeleteView.as_view(),
         name='the_growing_plant_plan_delete'),
    # ========================================REPORTS=====================================#
    # Sapling  Ko'chat --> Report
    path('sapling/report', SaplingReportView.as_view(), name="sapling_report"),  # excel
    path('sapling/region/<int:pk>', SaplingRegionReportView.as_view(), name="sapling_region"),
    path('sapling/department/<int:pk>', SaplingDepartmentReportView.as_view(), name="sapling_department"),
    path('sapling/height/report', TreePlantReport.as_view(), name="sapling_height_report"),  # excel
    path('sapling/height/new/report', TreeHeightReport2.as_view(), name="tree_height_report"),
    path('tree/height/department/report/<int:pk>', TreeHeightDepartmentReport.as_view(), name='tree_height_department'),

    # Sprout Input-Output -> Report
    path('sprout/report/dashboard', SproutReportDashboard.as_view(), name="sprout_report_dashboard"),
    path('sprout/all/report', SproutRegionAllReport.as_view(), name="sprout_all_report"),
    path('sprout/department/in/out/report/<int:pk>', SproutDepartmentReport.as_view(), name="sprout_in_out_department"),

    # SPROUT PLAN REJA -> Report
    path('sprout/report', SproutReportView.as_view(), name="sprout_report"),  # excel
    path('sprout/region/<int:pk>', SproutRegionReportView.as_view(), name="sprout_region"),
    path('sprout/department/<int:pk>', SproutDepartmentReportView.as_view(), name="sprout_department"),

    # PREPAIRLAND Report
    path('land/report/dashboard', PrePairReportDashboard.as_view(), name="land_report_dashboard"),
    path('land/all/report', PrepairLandReportView.as_view(), name="land_all_report"),  # excel
    path('land/department/in/out/report/<int:pk>', PrepairLandDepartmentView.as_view(), name="land_department_detail"),

    # Daraxt ekish (URMON BARPO QILISH) -> Report
    path('the_ground/regort', TheGroundPlantingReportView.as_view(), name="the_ground_report"),  # excel

    # Sapling -> Input Output Report
    path('sapling/report/dashboard', SaplingReportDashboardView.as_view(), name="sapling_report_dashboard"),
    path('sapling/all/report', SaplingRegionAllReport.as_view(), name="sapling_all_report"),  # excel
    path('sapling/department/in/out/report/<int:pk>', SaplingDepartmentReport.as_view(),  # excel
         name="sapling_in_out_department"),
    # TreeContract --> Report
    path('tree/contract/report', TreeContractReport.as_view(), name="tree_contract_report"),
    path('tree/contract/report/department/<int:pk>', TreeContractDepartmentReport.as_view(),
         name="tree_contract_department_report"),

    # Generate EXCEL files
    path("get/height/excel", TreeHeightReportXLSX.as_view(), name='height_reports'),
    path("get/sapling/excel", SaplingPlanReportXLSX.as_view(), name='sapling_reports'),
    path("get/sprout/excel", SproutPlanReportXLSX.as_view(), name='sprout_reports'),
    path("sapling/input/output/xlsx/<int:department_pk>", SaplingInputOutputXLSX.as_view(), name='sapling_io_xlsx'),
    path("sprout/input/output/xlsx/<int:department_pk>", SproutInputOutputXLSX.as_view(), name='sprout_io_xlsx'),
    path("finance/report/by/quarter", ForestQuarterPlanReportXLSX.as_view(), name='finance_by_quarter_xlsx'),
    path("forest/report/by/year", ForestTreeGroundReportXLSX.as_view(), name='forest_report_by_year'),
    path("tree/contract/xlsx/report", TreeContractReportXLSX.as_view(), name='tree_contract_xlsx'),

    path("excel/page", DevelopmentExcelReportView.as_view(), name='development_xlsx_report'),  # test
    path("excel/file", GenerateDevelopmentXLSX.as_view(), name='get_excel_file'),  # test
]
