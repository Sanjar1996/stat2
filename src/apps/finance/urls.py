from django.urls import path
from .views import *

app_name = 'finance'

urlpatterns = [
    # FINANCE TYPE
    path('dashboard/', FinanceDashboard.as_view(), name="finance_dashboard"),
    path('list/', FinanceTypeList.as_view(), name="finance_type_list"),
    path('create/', FinanceTypeCreate.as_view(), name="finance_type_create"),
    path('detail/<int:pk>', FinanceTypeDetail.as_view(), name="finance_type_detail"),
    path('type/<int:pk>/delete', FinanceTypeDeleteView.as_view(), name='finance_type_delete'),

    # FINANCE
    path('finance/list', FinanceList.as_view(), name="finance_list"),
    path('finance/create', FinanceCreate.as_view(), name="finance_create"),
    path('finance/detail/<int:pk>', FinanceDetail.as_view(), name="finance_detail"),
    path('finance/<int:pk>/delete', FinanceDeleteView.as_view(), name='finance_delete'),
    path('finance/actual/state/change/', ChangeFinanceActualState.as_view(), name="finance_actual_state_change"),

    # FINANCE PLAN
    path('plan/list', FinancePlanList.as_view(), name="finance_plan_list"),
    path('plan/create', FinancePlanCreate.as_view(), name="finance_plan_create"),
    path('plan/detail/<int:pk>', FinancePlanDetail.as_view(), name="finance_plan_detail"),
    path('plan/<int:pk>/delete', FinancePlanDeleteView.as_view(), name='finance_type_delete'),

    # ProductionServiceActual
    path('production/dashboard', ProductionAndPaidServiceDashboard.as_view(), name="production_dashboard"),
    path('production/actual/list', ProductionServiceActualList.as_view(), name="production_actual_list"),
    path('production/actual/create', ProductionServiceActualCreate.as_view(), name="production_actual_create"),
    path('production/actual/detail/<int:pk>', ProductionServiceActualDetail.as_view(), name="production_actual_detail"),
    path('production/actual/<int:pk>/delete', ProductionServiceActualDeleteView.as_view(), name='production_actual_delete'),

    # ProductionServicePlan
    path('production/plan/list', ProductionServicePlanList.as_view(), name="production_plan_list"),
    path('production/plan/create', ProductionServicePlanCreate.as_view(), name="production_plan_create"),
    path('production/plan/detail/<int:pk>', ProductionServicePlanDetail.as_view(), name="production_plan_detail"),
    path('production/plan/<int:pk>/delete', ProductionServicePlanDeleteView.as_view(), name='production_plan_delete'),

    # Production_Paid_Service_Report
    path('production/service/all/report', ProductServiceAllReport.as_view(), name="production_service_report"),   # excel | prod_service_by_quarter

    #EXPORT CSV
    path('export-csv', export_csv, name="export_csv"),
    path('export-exel', export_exel, name="export_exel"),

    # REPORT
    path('reports/', Report.as_view(), name="report"),  # excel | finance_general
    path('all/report/', AllReport.as_view(), name="all_report"),    # excel | finance_by_quarter
    path('profit/types/report', FinanceProfitTypesReport.as_view(), name="profit_types_report"),  # excel | finance_all_types
    path('existing/sids', ExistingSids.as_view(), name="existing_sids"),

    # Generate EXCEL files
    path("finance/report/by/quarter", FinancePlanQuarterReportXLSX.as_view(), name='finance_by_quarter'),
    path("finance/all/types/report", FinanceByTypeReportXLSX.as_view(), name='finance_all_types'),
    path("finance/general/report", FinanceGeneralReportXLSX.as_view(), name='finance_general'),
    path("prod/services/report/by/quarter", ProductionServicesReportXLSX.as_view(), name='prod_service_by_quarter'),
]


