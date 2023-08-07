from django.urls import path
from .views import *

app_name = 'ipsgov'

urlpatterns = [
    path('pnfl/list', PnflActionListView.as_view(), name="pnfl"),

]
