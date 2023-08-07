from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core import serializers
from django.http import HttpResponse
from django.views import generic, View
from django.views.generic import ListView
from django_filters.views import FilterView
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils.manager import ManagerM2M
from .filters import MemberFilter
from .forms import *
from .models import *
from .serializers import UserSerializer, UserInformationSerializer, DepartmentInformationSerializer, \
    RegionInformationSerializer


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            email = authenticate(email=email, password=raw_password)
            msg = 'User created'
            success = True
            return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


def report(request):
    return render(request, 'reports/report.html')


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attechment; filename=Expenses' + datetime.datetime.now() + 'csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    expenses = FinancePlan.objects.all()


class UserListView(LoginRequiredMixin, generic.ListView):
    template_name = 'accounts/users_list.html'
    model = User
    paginate_by = 10
    context_object_name = 'users'

    def get_context_data(self, *args, **kwargs):
        object_list = User.objects.exclude(status=3)
        context = super(UserListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return User.objects.exclude(status=3)


class UserCreateView(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/accounts/create/"""

    def get(self, request):
        if request.user.is_superuser:
            groups = Group.objects.all()
        else:
            groups = request.user.groups.all()
        department = serialize('json', Department.objects.filter(status=1).order_by('sort'))
        region = serialize('json', Region.objects.filter(status=1).order_by('sort'))
        regions = Region.objects.exclude(status=2).order_by('sort')
        information = serialize('json', Information.objects.filter(status=1))
        nation = serialize('json', Nation.objects.filter(status=1))
        position = serialize('json', Position.objects.filter(status=1))
        form_user = UserCreateForm()
        form_info = UserInformationForm()
        context = {
            "form_user": form_user,
            "form_info": form_info,
            "department": department,
            "region": region,
            "regions": regions,
            "groups": groups,
            "information": information,
            "nation": nation,
            "position": position,
            "get_departments_path": f'{settings.BASE_URL}/accounts/get/department/by/regions'
        }
        return render(request, 'accounts/member_create.html', context)

    def post(self, request):
        # data = request.POST
        # print("DATA.......", data)
        # 'regions': ['3', '4'], 'departments': ['16', '22', '17'],
        regions = request.POST.getlist('regions')
        departments = request.POST.getlist('departments')
        groups = request.POST.getlist('groups')
        # print("1.....", regions, type(regions))
        # print("2.....", departments, type(departments))
        # print("3.....", groups, type(groups))
        form_user = UserUpdateForm(request.POST)
        form_info = UserInformationForm(request.POST, request.FILES)
        # new_user = None
        if form_user.is_valid():
            new_user = form_user.save(commit=False)
            new_user.hash_pass = form_user.cleaned_data['password']
            new_user.set_password(form_user.cleaned_data['password'])
            new_user.save()
            if new_user and form_info.is_valid():
                data = form_info.save(commit=False)
                data.user = new_user
                ManagerM2M().save_m2m(user_pk=new_user.pk, reg=regions, dep=departments)
                ManagerM2M().save_user_perms(user_pk=new_user.pk, perms=groups)
                data.save()
            else:
                print("ERROR-1..............", form_info.errors)
        else:
            print("ERROR-2....................", form_user.errors)

        return redirect('accounts:members_list')


class UserDetailView(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/accounts/{id}detail"""
    template_name = 'accounts/user_detail.html'

    def get(self, request, account_pk):
        try:
            user = User.objects.get(pk=account_pk)
            info = _get_user_information_data(account_pk)
            ctx = {"is_user": True, "account": user, "info": info}
            return render(request, self.template_name, ctx)
        except ObjectDoesNotExist:
            ctx = {"is_user": False}
            return render(request, self.template_name, ctx)


class UserUpdateView(LoginRequiredMixin, View):
    template_name = 'accounts/user_update.html'

    def get(self, request, pk):
        selected_regions = []
        selected_departments = []
        selected_roles = []
        regions = Region.objects.exclude(status=2).order_by('sort')
        qs_user = User.objects.filter(pk=pk)
        if qs_user.exists():
            user_by_pk = User.objects.get(pk=pk)
            for role in user_by_pk.groups.all():
                selected_roles.append(role.id)
            user_regions_departments = UserDepartment.objects.filter(user=user_by_pk)
            for urd in user_regions_departments:
                for r_item in urd.regions.all():
                    selected_regions.append(r_item.id)
                for d_item in urd.departments.all():
                    selected_departments.append(d_item.id)
            if request.user.is_superuser:
                groups = Group.objects.all()
            else:
                groups = request.user.groups.all()
                # groups = user_by_pk.groups.all()
        else:
            selected_roles = []
            user_regions_departments = []
            groups = []
        # print("1......", selected_regions)
        # print("2......", selected_departments)
        # print("G......", self.request.user.user_department_set.all())
        try:
            account = User.objects.get(pk=pk)
            info = _get_user_information_data(pk)
            form_user = UserUpdateForm(initial={
                "email": account.email,
                'first_name': account.first_name,
                "last_name": account.last_name,
                "mid_name": account.mid_name,
                "temporary_work": account.temporary_work,
                "information": account.information,
                "position": account.position,
                "national": account.national,
                "department": account.department,
                'status': account.status,
                'is_active': account.is_active,
            })
            if info:
                form_info = UserInformationForm(initial={
                    "year_of_graduation": info.year_of_graduation if info.year_of_graduation else None,
                    "name_of_graduation": info.name_of_graduation,
                    "birth_date": info.birth_date,
                    "birth_place": info.birth_place,
                    "specialization": info.specialization,
                    "passport_number": info.passport_number,
                    "start_position_date": info.start_position_date,
                    "end_position_date": info.end_position_date,
                    "gender": info.gender,
                    "residence_address": info.residence_address,
                    "phone_number": info.phone_number,
                    "academic_degree": info.academic_degree,
                    "tour": info.tour,
                    "favorite_party": info.favorite_party,
                    "languages": info.languages,
                    "family_number": info.family_number,
                    "people_deputy": info.people_deputy,
                    "state_award": info.state_award,
                    "cripple": info.cripple,
                    "military_service": info.military_service,
                    "judicial": info.judicial,
                    "is_judicial": info.is_judicial,
                    "resume": info.resume
                })
            else:
                form_info = UserInformationForm()
            context = {
                "is_user": True, "selected_roles": selected_roles, "form_user": form_user,
                "form_info": form_info, "account": account,
                "groups": groups, "regions": regions, "user_departments": user_regions_departments,
                "get_departments_path": f'{settings.BASE_URL}/accounts/get/department/by/regions',
                "selected_regions_list": selected_regions, "selected_departments_list": selected_departments
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False, "incorrect_pk": pk}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        regions = request.POST.getlist('regions')
        departments = request.POST.getlist('departments')
        groups = request.POST.getlist('groups')
        # print("1......", regions, type(regions))
        # print("2......", departments, type(departments))
        # print("3......", groups, type(groups))
        try:
            user = User.objects.get(pk=pk)
            form_user = UserUpdateForm(instance=user, data=request.POST)
            user = None
            if form_user.is_valid():
                user = form_user.save(commit=False)
                user.hash_pass = form_user.cleaned_data['password']
                user.set_password(form_user.cleaned_data['password'])
                user.save()
                user_info = UserInformation.objects.filter(user=user)
                ManagerM2M().save_m2m(user_pk=user.pk, reg=regions, dep=departments)
                ManagerM2M().save_user_perms(user_pk=user.pk, perms=groups)
                if user_info:
                    form_info = UserInformationForm(instance=user_info[0], data=request.POST, files=request.FILES)
                    if form_info.is_valid():
                        data = form_info.save(commit=False)
                        data.user = user
                        data.save()
                        return redirect('accounts:members_list')
                return redirect('accounts:members_list')
            else:
                # print("UserUpdate FORM is_valid.........", form_user.errors)
                form_info = UserInformationForm()
                context = {"msg": form_user.errors, "account": user, "form_user": form_user, "form_info": form_info}
                return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            # print("UserUpdate ObjectDoesNotExist,.........", ObjectDoesNotExist)
            return render(request, self.template_name)


class UserDeleteView(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/accounts/{id}delete"""
    template_name = 'accounts/user_list.html'

    def get(self, request, pk):
        qs = User.objects.filter(pk=pk)
        print("sad", pk)
        if qs.exists() and pk > 1:
            print("sad")
            qs.update(status=3)
            return redirect('accounts:members_list')
        else:
            return redirect('accounts:members_list')


class RegionList(LoginRequiredMixin, View):
    template_name = 'regions/region_list.html'
    paginate_by = 4

    def get(self, request):
        try:
            regions = Region.objects.filter(status=1).order_by('-id')
            context = {
                "is_user": True, "regions": regions
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)


class RegionDetail(LoginRequiredMixin, View):
    template_name = 'regions/region_detail.html'
    permission_model = User

    def get(self, request, pk):
        try:
            region = Region.objects.get(pk=pk)
            form = RegionForm(initial={'name': region.name})
            context = {
                "is_user": True, "region": region, 'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            region = Region.objects.get(pk=pk)
            form = RegionForm(instance=region, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('accounts:region_list')
            else:
                return redirect('accounts:region_list')
        except ObjectDoesNotExist:
            return redirect('accounts:region_list')


class RegionCreate(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/register"""
    template_name = 'regions/region_create.html'

    def get(self, request):
        try:
            form = RegionForm()
            context = {
                "is_user": True, "form": form,
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request):
        try:
            form = RegionForm(data=request.POST)
            print(form)
            if form.is_valid():
                form.save()
                messages.success(request, "Account updated successfully!")
                return redirect('accounts:region_list')
            else:
                messages.error(request, 'Something went wrong')
                return redirect('accounts:region_list')
        except ObjectDoesNotExist:
            return redirect('accounts:region_list')


class RegionDeleteView(LoginRequiredMixin, View):
    template_name = 'regions/region_list.html'

    def get(self, request, pk):
        qs = Region.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('accounts:region_list')
        else:
            return redirect('accounts:region_list')


class DepartmentListView(LoginRequiredMixin, ListView):
    template_name = 'department/department_list.html'
    paginate_by = 10
    model = Department

    def get_context_data(self, *args, **kwargs):
        context = super(DepartmentListView, self).get_context_data(**kwargs)
        form = FilterForm()
        object_list = Department.objects.filter(status=1)
        context['form'] = form
        return context

    def get_queryset(self):
        return Department.objects.filter(status=1)


class DepartmentCreate(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/register"""
    template_name = 'department/department_create.html'

    def get(self, request):
        try:
            form = DepartmentForm()
            context = {"is_user": True, "form": form}
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request):
        try:
            form = DepartmentForm(data=request.POST)
            print(form)
            if form.is_valid():
                form.save()
                messages.success(request, "Account updated successfully!")
                return redirect('accounts:department_list')
            else:
                messages.error(request, 'Something went wrong')
                return redirect('accounts:department_list')
        except ObjectDoesNotExist:
            return redirect('accounts:department_list')


class DepartmentDetail(LoginRequiredMixin, View):
    template_name = 'department/department_detail.html'

    def get(self, request, pk):
        try:
            department = Department.objects.get(pk=pk)
            form = DepartmentForm(initial={'name': department.name, "region": department.region})
            context = {
                "is_user": True, "department": department, 'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            department = Department.objects.get(pk=pk)
            form = DepartmentForm(instance=department, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('accounts:department_list')
            else:
                return redirect('accounts:department_list')
        except ObjectDoesNotExist:
            return redirect('accounts:department_list')


class DepartmentDeleteView(LoginRequiredMixin, View):
    template_name = 'department/department_list.html'

    def get(self, request, pk):
        qs = Department.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('accounts:department_list')
        else:
            return redirect('accounts:department_list')


class PositionList(LoginRequiredMixin, View):
    template_name = 'position/position_list.html'

    def get(self, request):
        try:
            positions = Position.objects.exclude(status=2).order_by('-id')
            context = {"is_user": True, "positions": positions}
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)


class PositionDetail(LoginRequiredMixin, View):
    template_name = 'position/position_detail.html'

    def get(self, request, pk):
        try:
            position = Position.objects.get(pk=pk)
            form = PositionForm(initial={'name': position.name})
            context = {
                "is_user": True, "position": position, 'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            region = Region.objects.get(pk=pk)
            form = RegionForm(instance=region, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('accounts:region_list')
            else:
                return redirect('accounts:region_list')
        except ObjectDoesNotExist:
            return redirect('accounts:region_list')


class PositionCreate(LoginRequiredMixin, View):
    template_name = 'position/position_create.html'

    def get(self, request):
        try:
            form = PositionForm()
            context = {"is_user": True, "form": form}
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request):
        try:
            form = PositionForm(data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('accounts:position_list')
            else:
                return redirect('accounts:position_list')
        except ObjectDoesNotExist:
            return redirect('accounts:position_list')


class PositionDeleteView(LoginRequiredMixin, View):
    template_name = 'position/position_list.html'

    def get(self, request, pk):
        qs = Position.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('accounts:position_list')
        else:
            return redirect('accounts:position_list')


class NationList(LoginRequiredMixin, View):
    template_name = 'nation/nation_list.html'

    def get(self, request):
        try:
            nations = Nation.objects.exclude(status=2).order_by('-id')
            context = {
                "is_user": True, "nations": nations
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)


class NationDetail(LoginRequiredMixin, View):
    template_name = 'nation/nation_detail.html'

    def get(self, request, pk):
        try:
            nation = Nation.objects.get(pk=pk)
            form = NationForm(initial={'name': nation.name})
            context = {
                "is_user": True, "nation": nation, 'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            nation = Nation.objects.get(pk=pk)
            form = NationForm(instance=nation, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('accounts:nation_list')
            else:
                return redirect('accounts:nation_list')
        except ObjectDoesNotExist:
            return redirect('accounts:nation_list')


class NationCreate(LoginRequiredMixin, View):
    template_name = 'nation/nation_create.html'

    def get(self, request):
        try:
            form = NationForm()
            context = {
                "is_user": True, "form": form,
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request):
        try:
            form = NationForm(data=request.POST)
            if form.is_valid():
                form.save()
                form = NationForm()
                ctx = {"state": True, "form": form}
                return render(request, self.template_name, ctx)
            else:
                return redirect('accounts:nation_list')
        except ObjectDoesNotExist:
            return redirect('accounts:nation_list')


class NationDeleteView(LoginRequiredMixin, View):
    template_name = 'nation/nation_list.html'

    def get(self, request, pk):
        qs = Nation.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('accounts:nation_list')
        else:
            return redirect('accounts:nation_list')


class InformationList(LoginRequiredMixin, View):
    template_name = 'information/information_list.html'

    def get(self, request):
        try:
            information = Information.objects.exclude(status=2).order_by('-id')
            context = {
                "is_user": True, "informations": information
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)


class InformationDetail(LoginRequiredMixin, View):
    template_name = 'information/information_detail.html'

    def get(self, request, pk):
        try:
            information = Information.objects.get(pk=pk)
            form = InformationForm(initial={'name': information.name})
            context = {
                "is_user": True, "information": information, 'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            information = Information.objects.get(pk=pk)
            form = InformationForm(instance=information, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('accounts:information_list')
            else:
                return redirect('accounts:information_list')
        except ObjectDoesNotExist:
            return redirect('accounts:information_list')


class InformationCreate(LoginRequiredMixin, View):
    template_name = 'information/information_create.html'

    def get(self, request):
        try:
            form = InformationForm()
            context = {"is_user": True, "form": form}
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request):
        try:
            form = InformationForm(data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('accounts:information_list')
            else:
                return redirect('accounts:information_list')
        except ObjectDoesNotExist:
            return redirect('accounts:information_list')


class InformationDeleteView(LoginRequiredMixin, View):
    template_name = 'information/information_list.html'

    def get(self, request, pk):
        qs = Information.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('accounts:information_list')
        else:
            return redirect('accounts:information_list')


class MembersListView(LoginRequiredMixin, FilterView, ListView):
    model = User
    context_object_name = 'users'
    template_name = 'accounts/members_list.html'
    paginate_by = 15
    filterset_class = MemberFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departments = serialize('json', Department.objects.filter(status=1))
        regions = serialize('json', Region.objects.filter(status=1))
        context['department_json'] = departments
        context['region_json'] = regions
        context['department'] = self.request.GET.get('department', None)
        context['department__region'] = self.request.GET.get('department__region', None)
        context['information'] = self.request.GET.get('information', None)
        context['position'] = self.request.GET.get('position', None)
        context['national'] = self.request.GET.get('national', None)
        context['email'] = self.request.GET.get('email', None)
        context['first_name'] = self.request.GET.get('first_name', None)
        context['last_name'] = self.request.GET.get('last_name', None)
        context['is_active'] = self.request.GET.get('is_active', None)
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.exclude(status=3).order_by('-id')
        elif self.request.user.is_staff:
            return User.objects.exclude(status=3).order_by('-id')
        else:
            admin_department_list = []
            admin_user_list = []
            # print("U.....", self.request.user)
            qs_admin_user_department = UserDepartment.objects.filter(user=self.request.user)
            if qs_admin_user_department.exists():
                admin_user_department = UserDepartment.objects.get(user=self.request.user)
                for admin_department in admin_user_department.departments.all():
                    admin_department_list.append(admin_department.id)
            # admin_roles_list = []
            # for role in self.request.user.groups.all():
            #     admin_roles_list.append(role.pk)
            admin_roles = self.request.user.groups.all()
            unique_users = UserDepartment.objects.filter(
                departments__in=admin_department_list, user__groups__in=admin_roles).distinct()
            for x in unique_users:
                admin_user_list.append(x.user.pk)
            return User.objects.filter(id__in=admin_user_list).order_by('-id')


class OthersActionsList(LoginRequiredMixin, View):
    template_name = 'accounts/dashboard.html'

    def get(self, request):
        return render(request, self.template_name)


def _get_user_information_data(user=None):
    try:
        return UserInformation.objects.get(user=user)
    except:
        return None


class UserCreateAction(APIView):
    def post(self, request):
        big_data = request.data
        doublicate_users = []
        for data in big_data:
            serializer = UserSerializer(data=data)
            current_user = User.objects.filter(email=data['email'])
            if not current_user.exists():
                if serializer.is_valid(raise_exception=True):
                    user = serializer.save()
                    if user:
                        data['user'] = user
                        serilizer_two = UserInformationSerializer(data=data)
                        if serilizer_two.is_valid(raise_exception=True):
                            serilizer_two.save()
                        else:
                            pass
            else:
                doublicate_users.append(data)
                continue
        return Response({"msg": "BINGO!!!!!!!!!!!!!"})


class RegionCreteSerializer(APIView):

    def post(self, request):
        big_data = request.data
        for data in big_data:
            serializer = RegionInformationSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        return Response({"msg": True})


class DepartmentCreateSerializer(APIView):

    def post(self, request):
        big_data = request.data
        test = 1
        print(len(big_data))
        for data in big_data:
            print(test)
            serializer = DepartmentInformationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                test = test + 1
            else:
                print(serializer.errors)
        return Response({"msg": True})


class UserDepartmentView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'accounts/user_departments.html')


class GetDepartmentByRegion(View):
    """Only AJAX request call"""

    def post(self, request):
        region_list = request.POST.getlist('ids[]')
        # print("POST.....", request.POST)
        # print("region_list.....", region_list, type(region_list))
        selected_regions = []
        if region_list:
            for item in region_list:
                if item not in selected_regions:
                    selected_regions.append(int(item))
        # print("selected_regions.....", selected_regions)
        # print("********************", Department.objects.exclude(region_id__in=selected_regions, status=2).count())
        if request.is_ajax() and selected_regions:
            # print("LIST......", selected_regions)
            # departments = serializers.serialize("json", Department.objects.filter(region_id__in=[1, 5]))
            qs = Department.objects.filter(region_id__in=selected_regions)
            active_departments = qs.exclude(status=2)
            # print("********************", qs.exclude(status=2).count())
            departments = serializers.serialize("json", active_departments)
            # print("1........", Department.objects.filter(region_id__in=selected_regions))
            return HttpResponse(departments, content_type='application/json')
        else:
            # print("ELSE.........")
            return HttpResponse([], content_type='application/json')


class GetRolesByID(View):
    """Only AJAX request call"""

    def post(self, request):
        ids = request.POST.getlist('ids[]')
        selected = []
        if ids and ids not in selected:
            for item in ids:
                if item not in selected:
                    selected.append(item)
        if request.is_ajax() and selected:
            # print("LIST......", selected)
            roles = serializers.serialize("json", Group.objects.filter(id__in=selected))
            # roles = serializers.serialize("json", self.request.user.groups.all())
            return HttpResponse(roles, content_type='application/json')
        else:
            # print("ELSE.........")
            return HttpResponse([], content_type='application/json')


# role = User.objects.get(email='admin777@admin.com')
# if role.groups.exists():
#     print("1  IF.............")
# else:
#     print("1  ELSE.............")

# def remove_invalid_index(department, regions):
#     active_region = []
#     active_department = []
#     for d_index in department:
#         obj = Department.objects.get(pk=d_index)
#         for r_index in regions:
#             if obj.region.pk == r_index and r_index not in active_region:
#                 active_region.append(r_index)
#
#     for d_item in department:
#         obj = Department.objects.get(pk=d_item)
#         for a_item in active_region:
#             if obj.region.pk == a_item and a_item not in active_department:
#                 active_department.append(obj.pk)
#     return dict(reg=active_region, dep=active_department)
#
# print("1.....", remove_invalid_index(department=[17, 22, 29, 6, 10, 62, 16, 53, 110,  75, 97], regions=[4, 12, 8, 9, 5]))
