from django.urls import path
from .views import *

app_name = 'chorvachilik'

urlpatterns = [
    # Chorvachilik ACTUAL
    path('chorvachilik/actual/list', ChorvachilikActualList.as_view(), name="chorvachilik_actual_list"),
    path('chorvachilik/actual/create/', ChorvachilikActualCreate.as_view(), name="chorvachilik_actual_create"),
    path('chorvachilik/actual/detail/<int:pk>/', ChorvachilikActualDetail.as_view(), name="chorvachilik_actual_detail"),
    path('chorvachilik/actual/<int:pk>/delete', ChorvachilikActualDeleteView.as_view(),
         name="chorvachilik_actual_delete"),

    # chorvachilik PLAN
    path('chorvachilik/plan/list', ChorvachilikPlanList.as_view(), name="chorvachilik_plan_list"),
    path('chorvachilik/plan/create/', ChorvachilikPlanCreate.as_view(), name="chorvachilik_plan_create"),
    path('chorvachilik/plan/detail/<int:pk>/', ChorvachilikPlanDetail.as_view(), name="chorvachilik_plan_detail"),
    path('chorvachilik/plan/<int:pk>/delete', ChorvachilikPlanDeleteView.as_view(), name="chorvachilik_plan_delete"),

    # chorvachilik REPORT
    path('chorvachilik/report/dashboard', ChorvachilikReportDashboardView.as_view(),
         name="chorvachilik_report_dashboard"),
    path('chorvachilik/all/report/', ChorvachilikAllReportsView.as_view(), name="chorvachilik_all_report"),  # excel | chorvachilik_xlsx
    path('chorvachilik/report/region/<int:pk>/', ChorvachilikRegionReport.as_view(), name="chorvachilik_report_region"),
    path('chorvachilik/report/department/<int:pk>/', ChorvachilikDepartmentReport.as_view(),
         name="chorvachilik_report_department"),

    # chorvachilik INPUT
    path('chorvachilik/input/list', ChorvaInputList.as_view(), name="chorva_input_list"),
    path('chorvachilik/input/create/', ChorvaInputCreate.as_view(), name="chorva_input_create"),
    path('chorvachilik/input/detail/<int:pk>/', ChorvaInputDetail.as_view(), name="chorva_input_detail"),
    path('chorvachilik/input/<int:pk>/delete', ChorvaInputDeleteView.as_view(), name="chorva_input_delete"),

    # chorvachilik OUTPUT
    path('chorvachilik/output/list', ChorvaOutputList.as_view(), name="chorva_output_list"),
    path('chorvachilik/output/create/', ChorvaOutputCreate.as_view(), name="chorva_output_create"),
    path('chorvachilik/output/detail/<int:pk>/', ChorvaOutputDetail.as_view(), name="chorva_output_detail"),
    path('chorvachilik/output/<int:pk>/delete', ChorvaOutputDeleteView.as_view(), name="chorva_output_delete"),

    # CHORVA INPUT OUTPUT REPORT
    path("chorva/in/out/report/dashboard", ChorvaInOutDashboard.as_view(), name="chorva_in_out_report_dashboard"),
    path('chorva/in/out/all/report', ChorvaInOutAllReport.as_view(), name="chorva_in_out_all_report"),
    path('chorva/in/out/department/report/<int:pk>', ChorvaInOutDeparmentReport.as_view(),  # excel | chorva_input_output
         name="chorva_in_out_department_report"),

    # ANIMAL
    path('animal/list', AnimalList.as_view(), name="animal_list"),
    path('animal/create/', AnimalCreate.as_view(), name="animal_create"),
    path('animal/detail/<int:pk>/', AnimalDetail.as_view(), name="animal_detail"),
    path('animal/<int:pk>/delete', AnimalDeleteView.as_view(), name="animal_delete"),

    # ANIMAL CATEGORY
    path('view_animalcategory', AnimalCategoryList.as_view(), name="animal_category_list"),
    path('animal/category/create/', AnimalCategoryCreate.as_view(), name="animal_category_create"),
    path('animal/category/detail/<int:pk>/', AnimalCategoryDetail.as_view(), name="animal_category_detail"),
    path('animal/category/<int:pk>/delete', AnimalCategoryDeleteView.as_view(), name="animal_category_delete"),

    # INPUT OUTPUT CATEGORY
    path('in_out/category/list', IoCategoryList.as_view(), name="in_out_category_list"),
    path('in_out/category/create/', IoCategoryCreate.as_view(), name="in_out_category_create"),
    path('in_out/category/detail/<int:pk>/', IoCategoryDetail.as_view(), name="in_out_category_detail"),
    path('in_out/category/<int:pk>/delete', IoCategoryDeleteView.as_view(), name="in_out_category_delete"),

    # CHORVA TYPE
    path('chorva/type/list', ChorvaTypeList.as_view(), name="chorva_type_list"),
    path('chorva/type/create/', ChorvaTypeCreate.as_view(), name="chorva_type_create"),
    path('chorva/type/detail/<int:pk>/', ChorvaTypeDetail.as_view(), name="chorva_type_detail"),
    path('chorva/type/<int:pk>/delete', ChorvaTypeDeleteView.as_view(), name="chorva_type_delete"),

    # CHORVA CATEGORY ChorvaCategoryDetail
    path('chorva/category/list', ChorvaCategoryList.as_view(), name="chorva_category_list"),
    path('chorva/category/create/', ChorvaCategoryCreate.as_view(), name="chorva_category_create"),
    path('chorva/category/detail/<int:pk>/', ChorvaCategoryDetail.as_view(), name="chorva_category_detail"),
    path('chorva/category/<int:pk>/delete', ChorvaCategoryDeleteView.as_view(), name="chorva_category_delete"),

    # Generate EXCEL files
    path("chorva/report/by/animal", ChorvachilikXLSX.as_view(), name='chorvachilik_xlsx'),
    path("chorva/inp/out/report", ChorvaInputOutputXLSX.as_view(), name='chorva_input_output'),

    path('chorva/upload/file/', UploadFIleAPIView.as_view(), name="file_upload"),
    path('chorva/delete/file/<int:pk>', UploadFIleDeleteAPIView.as_view(), name="file_delete")
]
