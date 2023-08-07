from django.urls import path
from .views import *

app_name = 'report'

urlpatterns = [
    path('report/list/', ReportList.as_view(), name="report_list"),
    path('report/create/', ReportCreate.as_view(), name='report_create'),
    path('report/detail/list/', ReportDetailView.as_view(), name="report_detail_list"),
    path('report/hisobot/<int:pk>', ReportPageView.as_view(), name="hisobot"),
    path('report/value/delete/<int:pk>', ReportValueDelete.as_view(), name="report_value_delete"),
    path('query/create', CreateReportQuery.as_view(), name="query_create"),
    path('keys/list/<int:pk>', ResponseReportKeys.as_view(), name="keys_list"),
    path('create/group', CreateReportGroup.as_view(), name='create_report_group'),
    path('create/new/report', CreateNewReport.as_view(), name='create_new_report'),
    path("report/update", UpdateReport.as_view(), name="update_report"),
    #GET LISTED REPORT VALUES
    path('get/listed/values', get_listed_report_values, name='get_listed_report_values'),
    # Generate EXCEL files
    path("general/dynamic/xlsx", GeneralDynamicReportXLSX.as_view(), name='general_dynamic_xlsx'),  # test
]
