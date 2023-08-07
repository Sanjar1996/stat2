from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('others/actions', OthersActionsList.as_view(), name="other_action"),
    path('login/', login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("create/", UserCreateView.as_view(), name="create"),
    # USERS
    # path('list/', UserListView.as_view(), name="users_list"),
    # MEMBERS
    path('members/list/', MembersListView.as_view(), name="members_list"),
    path('<int:pk>/update', UserUpdateView.as_view(), name='accounts_update'),
    path('<int:pk>/delete', UserDeleteView.as_view(), name='accounts_delete'),
    path('<int:account_pk>/detail', UserDetailView.as_view(), name='accounts_detail'),

    # REGIONS
    path('region/list', RegionList.as_view(), name="region_list"),
    path('region/create', RegionCreate.as_view(), name="region_create"),
    path('region/detail/<int:pk>', RegionDetail.as_view(), name="region_detail"),
    path('region/<int:pk>/delete', RegionDeleteView.as_view(), name='region_delete'),
    # DEPARTMENTS
    path('department/list', DepartmentListView.as_view(), name="department_list"),
    path('department/create', DepartmentCreate.as_view(), name="department_create"),
    path('department/detail/<int:pk>', DepartmentDetail.as_view(), name="department_detail"),
    path('department/<int:pk>/delete', DepartmentDeleteView.as_view(), name='department_delete'),
    # POSITIONS
    path('position/list', PositionList.as_view(), name="position_list"),
    path('position/create', PositionCreate.as_view(), name="position_create"),
    path('position/detail/<int:pk>', PositionDetail.as_view(), name="position_detail"),
    path('position/<int:pk>/delete', PositionDeleteView.as_view(), name='position_delete'),
    # NATIONS
    path('nation/list', NationList.as_view(), name="nation_list"),
    path('nation/create', NationCreate.as_view(), name="nation_create"),
    path('nation/detail/<int:pk>', NationDetail.as_view(), name="nation_detail"),
    path('nation/<int:pk>/delete', NationDeleteView.as_view(), name='nation_delete'),
    # information
    path('information/list', InformationList.as_view(), name="information_list"),
    path('information/create', InformationCreate.as_view(), name="information_create"),
    path('information/detail/<int:pk>', InformationDetail.as_view(), name="information_detail"),
    path('information/<int:pk>/delete', InformationDeleteView.as_view(), name='information_delete'),

    path('users/create/', UserCreateAction.as_view(), name="create_users"),
    path('region/create/', RegionCreteSerializer.as_view(), name="region_users"),
    path('department/create/', DepartmentCreateSerializer.as_view(), name="department_users"),
    path('user/deparmtnets', UserDepartmentView.as_view(), name="user_departments"),
    path('get/department/by/regions', GetDepartmentByRegion.as_view(), name='get_departments'),  # only AJAX call
    path('get/permission/by/id', GetRolesByID.as_view(), name='get_roles'),  # only AJAX call
]
