# from django.urls import path, re_path
#
# from . import controller
# from .views import *
#
# app_name = "controller"
# urlpatterns = [
#     # The home page
#     # path('', index, name='home'),
#     path('', controller.RouteController.as_view(), name="home"),
#     re_path('.*\.*', pages, name='pages'),
# ]
from django.urls import path
from . import controller
from .views import ReportDashboardView
app_name = 'controller'

urlpatterns = [
    path('', controller.RouteController.as_view(), name="home"),
    path('login/', controller.LoginView.as_view(), name="login"),
    path('register/', controller.RegisterUserView.as_view(), name="register"),
    path('logout/', controller.LogoutView.as_view(), name="logout"),
    path("all/reports", ReportDashboardView.as_view(), name="all_reports")
]
