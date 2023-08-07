from django.urls import path
from .views import *

urlpatterns = [
    # 1-API
    # path('get_person_dock_info_servise/', GetPersonDocInfoService.as_view(), name="get_person_dock_info_servise"),
    path('get_person_dock_info_servise/', Post_userdata_from_pinfl.as_view(), name="get_person_dock_info_servise"),
    # 2-API
    path('get_citizen_info/', GetCitizenInfoView.as_view()),  # DONE
    # 3-API
    path('get_tin_by_pass/', GetTinbyPasNumView.as_view()),  # DONE
    # 4-API
    path('get_pension_service/', GetPensionService.as_view(), name="get_pension_service"),  # DONE
    # 5-API
    path("get_pension_assng_service/", GetPensionAssngServive.as_view(), name="get_pension_assng_service"),  # DONE
    # 6-API
    path("get_pension_size_service/", GetPensionSizeService.as_view(), name="get_pension_size_service"),  # DONE
    # API 9
    path('get_divorce_info/', GetDivorceInfo.as_view(), name='divorce_info'),  # DONE
    # API 10
    path('get_death_info/', GetDeathCertInfo.as_view(), name='death_info'),  # DONE
    # API 11
    path('get_position_info/', GetPositionInfo.as_view(), name='position_info'),  # DONE
    # API 12
    path('get_position_history/', GetPositionHistoryService.as_view(), name='position_history'),  # DONE
    # API 16
    path("get_ownership_pnfl_service/", GetOwnershipPnflService.as_view(), name="ownership_pnfl_service"),  # DONE
    # 17-API
    path('check/conviction/', ObtainingCheckCertificate.as_view(), name='check_certificate'),  # DONE
    path('get/conviction/result/', GetObtainingResult.as_view(), name='get_conviction_result'),  # DONE
    # For urmon-rental project
    path('get_citizen_info/<str:tin>', GetCitizenInfoViewOld.as_view()),
    path('get_tin_by_pass/<str:passnum>', GetTinbyPasNumViewOld.as_view()),
    path('get_job_status/', Post_check_job_status.as_view()),
    path('get_userinfo/', Post_userdata_from_pinfl.as_view())


]
