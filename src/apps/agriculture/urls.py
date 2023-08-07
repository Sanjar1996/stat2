from django.urls import path
from .views import *

app_name = 'agriculture'

urlpatterns = [
    # AGRICULTURE ACTUAL
    path('agriculture/actual/list', AgricultureActualList.as_view(), name="agriculture_actual_list"),
    path('agriculture/actual/create/', AgricultureActualCreate.as_view(), name="agriculture_actual_create"),
    path('agriculture/actual/detail/<int:pk>/', AgricultureActualDetail.as_view(), name="agriculture_actual_detail"),
    path('agriculture/actual/<int:pk>/delete', AgricultureActualDeleteView.as_view(), name="agriculture_actual_delete"),
    # AGRICULTURE PLAN
    path('agriculture/plan/list', AgriculturePlanList.as_view(), name="agriculture_plan_list"),
    path('agriculture/plan/create/', AgriculturePlanCreate.as_view(), name="agriculture_plan_create"),
    path('agriculture/plan/detail/<int:pk>/', AgriculturePlanDetail.as_view(), name="agriculture_plan_detail"),
    path('agriculture/plan/<int:pk>/delete', AgriculturePlanDeleteView.as_view(), name="agriculture_plan_delete"),

    # AGRICULTURE REPORT
    path('agriculture/report/dashboard', AgricultureReportDashboardView.as_view(), name="agriculture_report_dashboard"),
    path('agriculture/report/all/', AgricultureAllReportView.as_view(), name="agriculture_report_all"),  # excel | agriculture_crops
    path('agriculture/report/region/<int:pk>/', AgricultureRegionReport.as_view(), name="agriculture_report_region"),
    path('agriculture/report/departmetn/<int:pk>/', AgricultureDepartmentReport.as_view(), name="agriculture_report_department"),
    path('only/all/report', AgricultureOnlyAllReportView.as_view(), name="only_all"),
    # Generate EXCEL files
    path("agriculture/report/by/crops", AgriculturalProductXLSX.as_view(), name='agriculture_crops'),
]
