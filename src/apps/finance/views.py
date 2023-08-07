import csv
import datetime
import json
from datetime import timedelta, date
import xlwt
from django.core.serializers import serialize
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.base import View
from django_filters.views import FilterView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .filters import FinanceActualFilter, FinancePlanFilter, ProductionServiceActualFilter
from django.contrib import messages
from .forms import FinanceTypeForm, FinanceForm, FinancePlanForm, FilterForm, ProductionServiceActualForm, \
    ProductionServicePlanForm, FinanceFilterForm
from .models import *
from ..accounts.models import User, Department, Region, UserDepartment
from ..core.service import get_finance_actual_and_completed_sum, get_one_month_finance_types_income_sum, \
    get_one_month_actual_and_plan_sum, get_production_and_paid_service_data
from ..core.service import get_current_user_regions_and_departments_json, get_current_user_regions_and_departments_qs
from ..report.models import Report as Rp

month_names = [{1: 'Январ'}, {2: 'Феврал'}, {3: 'Март'}, {'4': 'Апрел'}, {'5': 'Май'}, {6: 'Июн'},
               {7: 'Июл'}, {8: 'Август'}, {9: 'Сентябр'}, {10: 'Октябр'}, {11: 'Ноябр'}, {12: 'Декабр'}]

epoch_year = date.today().year
year_start = date(epoch_year, 1, 1).strftime('%Y-%m-%d')
year_end = date(epoch_year, 12, 31).strftime('%Y-%m-%d')


class FinanceDashboard(LoginRequiredMixin, View):
    template_name = 'moliya/dashboard.html'

    def get(self, request):
        regions, departments = get_current_user_regions_and_departments_qs(request.user)
        if regions and departments:
            data = Rp.objects.filter(type=1, status=1)
            context = {"start": year_start,
                       "end": date.today().strftime('%Y-%m-%d'),
                       "data": data,
                       "current_year": date.today().year}
            context.update(get_finance_actual_and_completed_sum(request.user))
            context.update(get_one_month_actual_and_plan_sum(request.user))
            context.update(get_one_month_finance_types_income_sum(request.user))
        else:
            context = {"start": year_start,
                       "end": date.today().strftime('%Y-%m-%d'),
                       "data": [],
                       "current_year": date.today().year}
        return render(request, self.template_name, context)


class ProductionAndPaidServiceDashboard(LoginRequiredMixin, View):
    template_name = 'moliya/report/production_dashboard.html'

    def get(self, request):
        regions, departments = get_current_user_regions_and_departments_qs(request.user)
        if regions and departments:
            data = Rp.objects.filter(type=5, status=1)
            context = {"start": year_start, "end": date.today().strftime('%Y-%m-%d'),
                       "data": data, "current_year": date.today().year}
            context.update(get_production_and_paid_service_data(request.user))
        else:
            context = {"start": year_start, "end": date.today().strftime('%Y-%m-%d')}
        return render(request, self.template_name, context)


class FinanceTypeList(LoginRequiredMixin, ListView):
    template_name = 'moliya/finance_type/finance_type_list.html'
    paginate_by = 10
    model = FinanceType

    def get_context_data(self, *args, **kwargs):
        context = super(FinanceTypeList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return FinanceType.objects.exclude(status=2)


class FinanceTypeCreate(LoginRequiredMixin, View):
    template_name = 'moliya/finance_type/finance_type_create.html'

    def get(self, request):
        try:
            form = FinanceTypeForm()
            context = {"is_user": True, "form": form}
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request):
        try:
            form = FinanceTypeForm(data=request.POST)
            print(form)
            if form.is_valid():
                form.save()
                return redirect('finance:finance_type_list')
            else:
                return redirect('finance:finance_type_list')
        except ObjectDoesNotExist:
            return redirect('finance:finance_type_list')


class FinanceTypeDetail(LoginRequiredMixin, View):
    template_name = 'moliya/finance_type/finance_type_detail.html'

    def get(self, request, pk):
        try:
            f_type = FinanceType.objects.get(pk=pk)
            form = FinanceTypeForm(initial={'name': f_type.name})
            context = {"is_user": True, "finance_type": f_type, "form": form}
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            f_type = FinanceType.objects.get(pk=pk)
            form = FinanceTypeForm(instance=f_type, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('finance:finance_type_list')
            else:
                return redirect('finance:finance_type_list')
        except ObjectDoesNotExist:
            return redirect('finance:finance_type_list')


class FinanceTypeDeleteView(LoginRequiredMixin, View):
    template_name = 'moliya/finance_type/finance_type_list.html'

    def get(self, request, pk):
        qs = FinanceType.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('finance:finance_type_list')
        else:
            return redirect('finance:finance_type_list')


class FinanceList(LoginRequiredMixin, FilterView, ListView):
    model = Finance
    context_object_name = 'object_list'
    template_name = 'moliya/finance/finance_list.html'
    paginate_by = 12
    filterset_class = FinanceActualFilter

    def get_context_data(self, **kwargs):
        context = super(FinanceList, self).get_context_data(**kwargs)
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        context['department_json'] = departments
        context['region_json'] = regions
        context['department'] = self.request.GET.get('department', '')
        context['region'] = self.request.GET.get('region', '')
        context['amount'] = self.request.GET.get('amount', '')
        context['department_name'] = self.request.GET.get('department_name', '')
        return context

    def get_queryset(self):
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return Finance.objects.filter(region__in=regions, department__in=departments, status=1).order_by('-id')
        else:
            return Finance.objects.filter(status=12)


class FinanceCreate(LoginRequiredMixin, View):
    template_name = 'moliya/finance/finance_create.html'

    def get(self, request):
        amount_type = request.GET.get("type", None)
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        f = serialize('json', FinanceType.objects.exclude(status=2))
        ctx = {"regions": regions, 'departments': departments, "type": f, "amount_type": amount_type}
        return render(request, self.template_name, ctx)

    def post(self, request):
        staff_user = request.user.has_perm('finance.change_finance')
        data = request.POST
        items = json.loads(data['items'])
        check = Finance.objects.filter(department=data['department'], region=data['region'],
                                       date=datetime.datetime.strptime(data['date'], '%Y-%m-%d'),
                                       amount_type=data['amount_type'])
        valid_date = datetime.date.today() - timedelta(3)
        created_date = datetime.datetime.strptime(data['date'], '%Y-%m-%d')
        # if not check.exists() and valid_date <= created_date.date(): # voqtinchalik ochib qo'yildi
        if data:
            for i in range(len(items)):
                Finance.objects.create(
                    date=data['date'],
                    department=Department.objects.get(id=data['department']),
                    region=Region.objects.get(id=data['region']),
                    amount=float(items[i]['amount']),
                    amount_type=float(data['amount_type']),
                    type=FinanceType.objects.get(id=items[i]['type']),
                    state=2,
                    creator=self.request.user
                )
            return redirect('finance:finance_list')
        elif staff_user:
            for i in range(len(items)):
                Finance.objects.create(
                    date=data['date'],
                    department=Department.objects.get(id=data['department']),
                    region=Region.objects.get(id=data['region']),
                    amount=float(items[i]['amount']),
                    amount_type=float(data['amount_type']),
                    type=FinanceType.objects.get(id=items[i]['type']),
                    creator=self.request.user,
                    state=2,
                )
            return redirect('finance:finance_list')
        else:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            f = serialize('json', FinanceType.objects.exclude(status=2))
            ctx = {"departments": departments, "regions": regions, "type": f, "amount_type": data['amount_type']}
            return render(request, self.template_name, ctx)


class FinanceDetail(LoginRequiredMixin, View):
    template_name = 'moliya/finance/finance_detail.html'

    def get(self, request, pk):
        try:
            finance = Finance.objects.get(pk=pk)
            form = FinanceForm(initial={
                'date': finance.date,
                "amount": finance.amount,
                "department": finance.department,
                "creator": finance.creator,
                "region": finance.region,
                "type": finance.type,
                "state": finance.state})
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            context = {
                "is_user": True,
                "finance": finance,
                "data": departments,
                "region": regions,
                'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            finance = Finance.objects.get(pk=pk)
            form = FinanceForm(instance=finance, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('finance:finance_list')
            else:
                print(form.errors)
                return redirect('finance:finance_list')
        except ObjectDoesNotExist:
            return redirect('finance:finance_list')


class FinanceDeleteView(LoginRequiredMixin, View):
    template_name = 'moliya/finance/finance_list.html'

    def get(self, request, pk):
        qs = Finance.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('finance:finance_list')
        else:
            return redirect('finance:finance_list')


class FinancePlanList(LoginRequiredMixin, FilterView, ListView):
    model = FinancePlan
    context_object_name = 'object_list'
    template_name = 'moliya/finance_plan/finance_plan_list.html'
    paginate_by = 12
    filterset_class = FinancePlanFilter

    def get_context_data(self, **kwargs):
        context = super(FinancePlanList, self).get_context_data(**kwargs)
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)

        context['department_json'] = departments
        context['region_json'] = regions
        context['department'] = self.request.GET.get('department', '')
        context['region'] = self.request.GET.get('region', '')
        context['amount'] = self.request.GET.get('amount', '')
        context['department_name'] = self.request.GET.get('department_name' '')
        return context

    def get_queryset(self):
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if departments and regions:
            return FinancePlan.objects.filter(region__in=regions, department__in=departments, status=1).order_by('-id')
        else:
            return FinancePlan.objects.filter(status=44)


class FinancePlanCreate(LoginRequiredMixin, View):
    template_name = 'moliya/finance_plan/finance_plan_create.html'

    def get(self, request):
        amount_type = request.GET.get("type", None)
        reg_and_depart = UserDepartment.objects.filter(user=request.user)
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        ctx = {"departments": departments, "region": regions, "amount_type": amount_type}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        nexxt = json.loads(data['next'])
        months = generate_month_year(int(data['date']))
        items = json.loads(data['items'])
        a_type = data['amount_type']
        check = FinancePlan.objects.filter(department=data['department'],
                                           amount_type=data['amount_type'],
                                           date__year=int(data['date'])).filter(Q(status=1) | Q(status=3))
        if check.exists():
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            ctx = {"data": departments, "region": regions, "amount_type": data['amount_type']}
            return render(request, self.template_name, ctx, status=400)
        elif not check:
            for i in range(len(items)):
                if items[i]['amount']:
                    FinancePlan.objects.create(
                        date=datetime.datetime.strptime(months[i], "%Y-%m-%d"),
                        department=Department.objects.get(id=data['department']),
                        amount_type=float(data['amount_type']),
                        region=Region.objects.get(id=data['region']),
                        amount=float(items[i]['amount']),
                        creator=self.request.user
                    )
                else:
                    pass
            if nexxt:
                regions, departments = get_current_user_regions_and_departments_json(self.request.user)
                ctx = {"data": departments, "region": regions, "amount_type": data['amount_type']}
                return render(request, self.template_name, ctx, status=201)
            else:
                return redirect('finance:finance_plan_list')


class FinancePlanDetail(LoginRequiredMixin, View):
    template_name = 'moliya/finance_plan/finance_plan_detail.html'

    def get(self, request, pk):
        try:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            finance = FinancePlan.objects.get(pk=pk)
            form = FinancePlanForm(initial={
                'date': finance.date,
                "amount": finance.amount,
                "department": finance.department,
                "creator": finance.creator,
                "region": finance.region
            })
            context = {
                "is_user": True,
                "finance": finance,
                "data": departments,
                "region": regions,
                'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            finance = FinancePlan.objects.get(pk=pk)
            form = FinancePlanForm(instance=finance, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('finance:finance_plan_list')
            else:
                return redirect('finance:finance_plan_list')
        except ObjectDoesNotExist:
            return redirect('finance:finance_plan_list')


class FinancePlanDeleteView(LoginRequiredMixin, View):
    template_name = 'moliya/finance_plan/finance_plan_list.html'

    def get(self, request, pk):
        qs = FinancePlan.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('finance:finance_plan_list')
        else:
            return redirect('finance:finance_plan_list')


# PRODUCTION PAID SERVICE ACTUAL
class ProductionServiceActualList(LoginRequiredMixin, FilterView, ListView):
    model = ProductionServiceActual
    context_object_name = 'object_list'
    template_name = 'moliya/production_actual/list.html'
    paginate_by = 12
    filterset_class = ProductionServiceActualFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)

        context['department_json'] = departments
        context['region_json'] = regions
        context['department'] = self.request.GET.get('department', "")
        context['region'] = self.request.GET.get('region', "")
        context['department_name'] = self.request.GET.get('department_name', "")
        return context

    def get_queryset(self):
        return ProductionServiceActual.objects.filter(status=1).order_by('-id')


class ProductionServiceActualCreate(LoginRequiredMixin, View):
    template_name = 'moliya/production_actual/create.html'

    def get(self, request):
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        ctx = {"data": departments, "region": regions}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        items = json.loads(data['items'])
        for i in range(len(items)):
            ProductionServiceActual.objects.create(
                date=data['date'],
                department=Department.objects.get(id=data['department']),
                region=Region.objects.get(id=data['region']),
                production=int(items[i]['production']),
                paid_service=int(items[i]['paid_service']),
                creator=self.request.user
            )
        return redirect('finance:production_actual_list')


class ProductionServiceActualDetail(LoginRequiredMixin, View):
    template_name = 'moliya/production_actual/detail.html'

    def get(self, request, pk):
        try:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            production = ProductionServiceActual.objects.get(pk=pk)
            form = ProductionServiceActualForm(initial={
                'date': production.date,
                "production": production.production,
                "paid_service": production.paid_service,
                "department": production.department,
                "creator": production.creator,
                "region": production.region
            })
            context = {
                "is_user": True,
                "production": production,
                "data": departments,
                "region": regions,
                'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            production = ProductionServiceActual.objects.get(pk=pk)
            form = ProductionServiceActualForm(instance=production, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('finance:production_actual_list')
            else:
                return redirect('finance:production_actual_list')
        except ObjectDoesNotExist:
            return redirect('finance:production_actual_list')


class ProductionServiceActualDeleteView(LoginRequiredMixin, View):
    template_name = 'moliya/production_actual/list.html'

    def get(self, request, pk):
        qs = ProductionServiceActual.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('finance:production_actual_list')
        else:
            return redirect('finance:production_actual_list')


# PRODUCTION PAID SERVICE PLAN
class ProductionServicePlanList(LoginRequiredMixin, FilterView, ListView):
    model = ProductionServicePlan
    context_object_name = 'object_list'
    template_name = 'moliya/production_plan/list.html'
    paginate_by = 10
    filterset_class = FinanceActualFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        context['department_json'] = departments
        context['region_json'] = regions
        context['department'] = self.request.GET.get('department', None)
        context['region'] = self.request.GET.get('region', None)
        context['department_name'] = self.request.GET.get('department_name', None)
        return context

    def get_queryset(self):
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            return ProductionServicePlan.objects.filter(region__in=regions, department__in=departments,
                                                        status=1).order_by('-id')
        else:
            return ProductionServicePlan.objects.filter(status=44).order_by('-id')


class ProductionServicePlanCreate(LoginRequiredMixin, View):
    template_name = 'moliya/production_plan/create.html'

    def get(self, request):
        regions, departments = get_current_user_regions_and_departments_json(self.request.user)
        ctx = {"data": departments,
               "region": regions}
        return render(request, self.template_name, ctx)

    def post(self, request):
        data = request.POST
        d_id = data['department']
        check = ProductionServicePlan.objects.filter(department__id=d_id, date__year=data['date'], status=1)
        if not check.exists():
            ProductionServicePlan.objects.create(
                date=date.today(),
                department=Department.objects.get(id=data['department']),
                region=Region.objects.get(id=data['region']),
                production=data['production'],
                paid_service=data['service'],
                creator=self.request.user
            )
            return redirect('finance:production_plan_list')
        else:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            ctx = {"data": departments,
                   "region": regions}
            return render(request, self.template_name, ctx)


class ProductionServicePlanDetail(LoginRequiredMixin, View):
    template_name = 'moliya/production_plan/detail.html'
    permission_model = User

    def get(self, request, pk):
        try:
            regions, departments = get_current_user_regions_and_departments_json(self.request.user)
            production = ProductionServicePlan.objects.get(pk=pk)
            form = ProductionServicePlanForm(initial={
                'date': production.date,
                "production": production.production,
                "paid_service": production.paid_service,
                "department": production.department,
                "creator": production.creator,
                "region": production.region
            })
            context = {
                "is_user": True,
                "production": production,
                "data": departments,
                "region": regions,
                'form': form
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            context = {"is_user": False}
            return render(request, self.template_name, context)

    def post(self, request, pk):
        try:
            production = ProductionServicePlan.objects.get(pk=pk)
            form = ProductionServicePlanForm(instance=production, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('finance:production_plan_list')
            else:
                return redirect('finance:production_plan_list')
        except ObjectDoesNotExist:
            return redirect('finance:production_plan_list')


class ProductionServicePlanDeleteView(LoginRequiredMixin, View):
    template_name = 'moliya/production_plan/list.html'

    def get(self, request, pk):
        qs = ProductionServicePlan.objects.filter(pk=pk)
        if qs.exists():
            qs.update(status=2)
            return redirect('finance:production_plan_list')
        else:
            return redirect('finance:production_plan_list')


# PRODUCT SERVICE ALL REPORT 
class ProductServiceAllReport(LoginRequiredMixin, View):
    template_name = 'moliya/report/production_and_paid_service_report.html'

    def get(self, request):
        current_year = date.today().year
        start = date(current_year, 1, 1).strftime('%Y-%m-%d')
        end_date = date(current_year, 12, 31).strftime('%Y-%m-%d')
        end = self.request.GET.get('end', None)
        if not end:
            end_dateformat = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            current_month = end_dateformat.month
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = end_dateformat.strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.datetime.strptime(end, '%Y-%m-%d')
            current_month = end_dateformat.month
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = end_dateformat.strftime('%Y-%m-%d')
        form = FilterForm(initial={"start": start, "end": end})
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            actual_data = ProductionServiceActual.objects.filter(date__range=[start, end], status=1)
            plan_data = ProductionServicePlan.objects.filter(date__year=current_year, status=1)
            region_id = None,
            region_obj = None
            data = []
            x = 1
            for depart in departments:
                x = x + 1
                # PRODUCTION
                depart_prod_year_plan_query = plan_data.filter(department=depart).aggregate(Sum('production'))
                depart_prod_actual_query = actual_data.filter(department=depart).aggregate(
                    Sum('production'))
                depart_production_year_plan = _check_sum_is_none(depart_prod_year_plan_query['production__sum'])
                depart_production_actual = _check_sum_is_none(depart_prod_actual_query['production__sum'])

                # PAID SERVICE
                dapart_service_yaar_plan_query = plan_data.filter(department=depart).aggregate(Sum('paid_service'))
                depart_service_actual_query = actual_data.filter(department=depart).aggregate(
                    Sum('paid_service'))

                depart_service_year_plan = _check_sum_is_none(dapart_service_yaar_plan_query['paid_service__sum'])
                depart_service_actual = _check_sum_is_none(depart_service_actual_query['paid_service__sum'])
                # SUM PRODUCTION AND PAID SERVICE
                depart_all_year_plan = depart_production_year_plan + depart_service_year_plan
                depart_all_actual = depart_production_actual + depart_service_actual
                department_percentage = _calculate_percentage(depart_all_year_plan, depart_all_actual)
                if region_id != depart.region_id:
                    # PRODUCTION
                    region_obj = Region.objects.get(id=depart.region_id)
                    region_prod_year_plan_query = plan_data.filter(region=region_obj).aggregate(Sum('production'))
                    region_prod_actual_query = actual_data.filter(region=region_obj).aggregate(Sum('production'))
                    region_production_year_plan = _check_sum_is_none(region_prod_year_plan_query['production__sum'])
                    region_production_actual = _check_sum_is_none(region_prod_actual_query['production__sum'])
                    # PAID SERVICE
                    region_service_yaar_plan_query = plan_data.filter(region=region_obj).aggregate(Sum('paid_service'))
                    region_service_actual_query = actual_data.filter(region=region_obj).aggregate(Sum('paid_service'))
                    region_service_year_plan = _check_sum_is_none(region_service_yaar_plan_query['paid_service__sum'])
                    region_service_actual = _check_sum_is_none(region_service_actual_query['paid_service__sum'])
                    # SUM PRODUCTION AND PAID SERVICE
                    region_all_year_plan = region_production_year_plan + region_service_year_plan
                    region_all_actual = region_production_actual + region_service_actual
                    region_percentage = _calculate_percentage(region_all_year_plan, region_all_actual)
                    data.append({
                        "index": 1,
                        "region_name": region_obj.name,
                        "region_production_year_plan": region_production_year_plan,
                        "region_production_actual": region_production_actual,
                        "region_service_year_plan": region_service_year_plan,
                        "region_service_actual": region_service_actual,
                        "region_all_year_plan": region_all_year_plan,
                        "region_all_actual": region_all_actual,
                        "region_percentage": region_percentage,

                        "depart_name": depart.name,
                        "depart_production_year_plan": depart_production_year_plan,
                        "depart_production_actual": depart_production_actual,
                        "depart_service_year_plan": depart_service_year_plan,
                        "depart_service_actual": depart_service_actual,
                        "depart_all_year_plan": depart_all_year_plan,
                        "depart_all_actula": depart_all_actual,
                        "department_percentage": department_percentage
                    })
                    x = 1
                else:
                    data.append({
                        "index": x,
                        "depart_name": depart.name,
                        "depart_production_year_plan": depart_production_year_plan,
                        "depart_production_actual": depart_production_actual,
                        "depart_service_year_plan": depart_service_year_plan,
                        "depart_service_actual": depart_service_actual,
                        "depart_all_year_plan": depart_all_year_plan,
                        "depart_all_actula": depart_all_actual,
                        "department_percentage": department_percentage
                    })
                region_obj = None
                region_id = depart.region_id

            # PRODUCTION
            production_year_plan_query = plan_data.filter(department__in=departments).aggregate(Sum('production'))
            production_actual_query = actual_data.filter(department__in=departments).aggregate(Sum('production'))

            production_year_plan = _check_sum_is_none(production_year_plan_query['production__sum'])
            production_actual = _check_sum_is_none(production_actual_query['production__sum'])
            # PAID SERVICE
            service_yaar_plan_query = plan_data.filter(region__in=regions).aggregate(Sum('paid_service'))
            service_actual_query = actual_data.filter(region__in=regions).aggregate(Sum('paid_service'))

            service_year_plan = _check_sum_is_none(service_yaar_plan_query['paid_service__sum'])
            service_actual = _check_sum_is_none(service_actual_query['paid_service__sum'])
            # SUM PRODUCTION AND PAID SERVICE
            all_year_plan = production_year_plan + service_year_plan
            all_year_actual = production_actual + service_actual
            all_percentage = _calculate_percentage(all_year_plan, all_year_actual)
            result = {
                "production_year_plan": production_year_plan,
                "production_actual": production_actual,
                "service_year_plan": service_year_plan,
                "service_actual": service_actual,
                "all_year_plan": all_year_plan,
                "all_year_actual": all_year_actual,
                "all_percentage": all_percentage
            }
            ctx = {"data": data, "result": result, "form": form, "start": start, "end": end}
            return render(request, self.template_name, ctx)
        else:
            ctx = {"form": form, "start": start, "end": end}
            return render(request, self.template_name, ctx)


class ExistingSids(View):
    template_name = 'reports/mavjud_uruglar.html'

    def get(self, request):
        form = FilterForm()
        context = {"form": form}
        return render(request, self.template_name, context)


class AllReport(View):
    template_name = 'moliya/report/all_report.html'
    """Viloyatlar va ularning tashkilotlari bo'yicha yillik report"""

    def get(self, request):
        today = date.today()
        current = today.year
        this_year = date(current, 1, 1).strftime('%Y-%m-%d')
        start = self.request.GET.get('start', this_year)
        end = self.request.GET.get('end', today.strftime('%Y-%m-%d'))
        amount_type = self.request.GET.get('type', 1)
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)

        form = FinanceFilterForm(initial={"start": start, "end": end, "type": amount_type})
        if regions and departments:
            context = {}
            end_dateformat = datetime.datetime.strptime(end, '%Y-%m-%d')
            current_month = end_dateformat.month
            epoch_year = end_dateformat.year
            year_start = date(epoch_year, 1, 1).strftime('%Y-%m-%d')
            quarter_num = 0
            if current_month <= 3:
                quarter_num = 0
                context['q'] = 0
            if current_month > 3:
                quarter = round(current_month // 3)
                qoldiq = current_month % 3
                if quarter == 1:
                    if qoldiq and current_month > 3:
                        quarter_num = 3
                        context['q'] = "1-чорак"
                        context['n'] = "2"
                elif quarter == 2:
                    if qoldiq and current_month > 6:
                        quarter_num = 6
                        context['q'] = 'Ярим йиллик'
                        context['n'] = "3"
                    elif current_month == 6:
                        quarter_num = 3
                        context['q'] = '1-чорак'
                        context['n'] = "2"
                elif quarter == 3:
                    if qoldiq and current_month > 9:
                        quarter_num = 9
                        context['q'] = "9-ойлик"
                        context['n'] = "4"
                    elif current_month == 9:
                        quarter_num = 6
                        context['q'] = "Ярим ойлик"
                        context['n'] = "3"
                elif quarter == 4:
                    quarter_num = 9
                    context['q'] = "9-ойлик"
                    context['n'] = "4"

            context.update(_get_cvartal_all_data(quarter_num, start, end, amount_type, regions, departments))
            context['form'] = form
            context['end'] = end
            return render(request, self.template_name, context)
        else:
            ctx = {"year_start": start, "year_end": end, "amount_type": amount_type, "form": form}
            return render(request, self.template_name, ctx)


def _get_department_finance_plan_all_sum_only_month(current_year=None, month=None, depart=None,
                                                    amount_type=None):
    """Bu funksiya 1 oylik departmntni planni qanchaligini xisoblab olib chiqib beradi """
    result = FinancePlan.objects.filter(department=depart, amount_type=amount_type, date__year=current_year,
                                        date__month=month, status=1).aggregate(Sum('amount'))
    return _check_sum_is_none(result['amount__sum'])


def _get_department_finance_completed_all_sum_only_month(current_year=None, month=None, depart=None,
                                                         amount_type=None):
    """Bu funksiya 1 oylik bajarilgan planni qanchaligini xisoblab olib chiqib beradi """
    result = Finance.objects.filter(date__year=current_year,
                                    date__month=month,
                                    department=depart,
                                    amount_type=amount_type,
                                    state=2, status=1).aggregate(Sum('amount'))
    return _check_sum_is_none(result['amount__sum'])


def _get_year_plan_only_one_region(current_year, reg=None, amount_type=None):
    """Yillik qo'yilgan plan yigindisi region uchun"""
    result = FinancePlan.objects.filter(date__year=current_year,
                                        amount_type=amount_type,
                                        region=reg, status=1).aggregate(Sum('amount'))
    return _check_sum_is_none(result['amount__sum'])


def _get_completed_plans_off_year(current_year, reg=None, amount_type=None):
    """Yil davomida balarib bolingan planlar yigindisi region uchun"""
    result = Finance.objects.filter(date__year=current_year,
                                    amount_type=amount_type,
                                    region=reg, state=2, status=1).aggregate(Sum('amount'))
    return _check_sum_is_none(result['amount__sum'])


def _get_completed_region_of_month(current_year=None, current_month=None, reg=None):
    """
        Bu function xozirgi yil, (n) oy , va region qabul qiladi.
        Shu berilgan malumotlarga asoslangan xolda summani yigindisini qaytaradi
    """
    result = Finance.objects.filter(date__year=current_year,
                                    date__month=current_month,
                                    status=1,
                                    region=reg, state=2).aggregate(Sum('amount'))
    return _check_sum_is_none(result['amount__sum'])


def _get_plan_region_of_month(current_year=None, current_month=None, reg=None):
    """
            Bu function xozirgi yil, (n) oy , va region qabul qiladi.
            Shu berilgan malumotlarga asoslangan xolda shu (n) oyga qo'yilgan planni
             summani yigindisini qaytaradi
        """
    result = FinancePlan.objects.filter(date__year=current_year,
                                        date__month=current_month,
                                        status=1,
                                        region=reg).aggregate(Sum('amount'))
    return _check_sum_is_none(result['amount__sum'])


def _get_plan_data_in_cvartal_department(current_year=None, current_month=None, reg=None,
                                         department=None,
                                         amount_type=None):
    """ Kravtal bo'yicha qo'yilgan planlarni xisoblab qaytaradi"""
    result = FinancePlan.objects.filter(date__year=current_year,
                                        date__month__lte=current_month,
                                        region=reg,
                                        amount_type=amount_type,
                                        department=department, status=1
                                        ).aggregate(Sum('amount'))
    return _check_sum_is_none(result['amount__sum'])


def _get_completed_plan_data_in_cvartal_department(current_year=None, current_month=None,
                                                   reg=None, department=None, amount_type=None):
    """ Kravtal bo'yicha bajarilgan planlarni xisoblab qaytaradi"""
    result = Finance.objects.filter(date__year=current_year,
                                    date__month__lte=current_month,
                                    department=department,
                                    amount_type=amount_type,
                                    region=reg, status=1,
                                    state=2).aggregate(Sum('amount'))
    return _check_sum_is_none(result['amount__sum'])


def _get_region_cvartal_plan(current_year=None, current_month=None, reg=None, amount_type=None):
    result = FinancePlan.objects.filter(date__year=current_year,
                                        date__month__lte=current_month,
                                        amount_type=amount_type,
                                        status=1,
                                        region=reg).aggregate(Sum('amount'))
    return _check_sum_is_none(result['amount__sum'])


def _get_region_cvartal_actual(current_year=None, current_month=None, reg=None, amount_type=None):
    result = Finance.objects.filter(date__year=current_year,
                                    date__month__lte=current_month,
                                    amount_type=amount_type,
                                    status=1, state=2,
                                    region=reg).aggregate(Sum('amount'))
    return _check_sum_is_none(result['amount__sum'])


def _get_region_cvartal_plan_range_data(current_year=None, start_month=None, reg=None, amount_type=None):
    """Bu fucntion kelgusi kvartalga qoyilgan planni topibberadi regionlar uchun"""
    result = FinancePlan.objects.filter(date__year=current_year,
                                        date__month__range=[start_month + 1, start_month + 3],
                                        amount_type=amount_type, status=1,
                                        region=reg).aggregate(Sum('amount'))
    return _check_sum_is_none(result['amount__sum'])


def _get_department_year_completed(current_year=None, reg=None, depart=None, amount_type=None):
    result = Finance.objects.filter(date__year=current_year,
                                    department=depart,
                                    amount_type=amount_type,
                                    region=reg, state=2, status=1).aggregate(Sum('amount'))
    return _check_sum_is_none(result['amount__sum'])


def _get_department_year_plan(current_year=None, reg=None, depart=None, amount_type=None):
    result = FinancePlan.objects.filter(date__year=current_year,
                                        department=depart,
                                        amount_type=amount_type, status=1,
                                        region=reg).aggregate(Sum('amount'))
    return _check_sum_is_none(result['amount__sum'])


def _get_department_next_cvartal_plan(current_year=None, start=None,
                                      reg=None, depart=None, amount_type=None):
    """Department uchun kelgusi cvartalga qo'yilgan planni topib beradi"""
    result = FinancePlan.objects.filter(date__year=current_year,
                                        date__month__range=[start + 1, start + 3],
                                        amount_type=amount_type,
                                        department=depart,
                                        region=reg, status=1).aggregate(Sum('amount'))
    return _check_sum_is_none(result['amount__sum'])


def _get_region_month_completed__sum(current_year=None, month=None, reg=None, amount_type=None):
    result = Finance.objects.filter(date__year=current_year,
                                    date__month=month,
                                    amount_type=amount_type,
                                    region=reg, status=1, state=2).aggregate(Sum('amount'))
    return _check_sum_is_none(result['amount__sum'])


def _get_region_month_plan_sum(current_year=None, month=None, reg=None, amount_type=None):
    result = FinancePlan.objects.filter(date__year=current_year,
                                        date__month=month,
                                        amount_type=amount_type,
                                        region=reg, status=1).aggregate(Sum('amount'))
    return _check_sum_is_none(result['amount__sum'])


def _get_cvartal_all_data(quarter_num=None, year_start=None, year_end=None, amount_type=None,
                          regions=None, departments=None):
    result = []
    months = {}
    year_total_plan = 0
    year_completed_total = 0
    end_dateformat = datetime.datetime.strptime(year_end, '%Y-%m-%d')
    current_month = end_dateformat.month
    epoch_year = end_dateformat.year

    for reg in regions:
        cvartal = []
        departments_list = departments.filter(region=reg)
        for depart in departments_list:
            department_moth_data = []
            for m in range(current_month):
                month = m + 1
                if month > quarter_num:
                    department_plan = _get_department_finance_plan_all_sum_only_month(epoch_year, month, depart,
                                                                                      amount_type)
                    department_completed = _get_department_finance_completed_all_sum_only_month(epoch_year,
                                                                                                month, depart,
                                                                                                amount_type)
                    region_month_completed = _get_region_month_completed__sum(epoch_year,
                                                                              month, reg, amount_type)
                    region_month_plan = _get_region_month_plan_sum(epoch_year, month,
                                                                   reg, amount_type)
                    all_regions_month_plans = FinancePlan.objects.filter(date__year=epoch_year, date__month=month,
                                                                         amount_type=amount_type, status=1).aggregate(
                        Sum('amount'))
                    # Jamida taigda chiqishi uchun
                    all_regions_month_completed = Finance.objects.filter(date__year=epoch_year, date__month=month,
                                                                         amount_type=amount_type, state=2,
                                                                         status=1).aggregate(Sum('amount'))

                    months.update(month_names[m])
                    if month == current_month:
                        all_regions_day_completed = Finance.objects.filter(date__year=epoch_year, date=year_end,
                                                                           amount_type=amount_type, state=2,
                                                                           status=1).aggregate(Sum('amount'))
                        day_region_actual_query = Finance.objects.filter(date=year_end, status=1, state=2,
                                                                         amount_type=amount_type,
                                                                         region=reg).aggregate(Sum('amount'))
                        region_day_actual = _check_sum_is_none(day_region_actual_query['amount__sum'])
                        department_day_actual_query = Finance.objects.filter(date=year_end, status=1, state=2,
                                                                             amount_type=amount_type,
                                                                             department=depart).aggregate(Sum('amount'))
                        department_day_actual = _check_sum_is_none(department_day_actual_query['amount__sum'])

                        department_moth_data.append({
                            "current_month": True,
                            "department_day_actual": department_day_actual,
                            "region_day_actual": region_day_actual,
                            "department_plan": department_plan,
                            "department_completed": department_completed,
                            "department_percentage": _calculate_percentage(department_plan, department_completed),
                            "region_month_plan": region_month_plan,
                            "region_month_completed": region_month_completed,
                            "region_month_percentage": _calculate_percentage(region_month_plan, region_month_completed),

                            "all_regions_month_plans": _check_sum_is_none(all_regions_day_completed['amount__sum']),
                            "all_regions_month_completed": _check_sum_is_none(
                                all_regions_month_completed['amount__sum']),
                            "all_regions_month_percentage": _calculate_percentage(
                                _check_sum_is_none(all_regions_month_plans['amount__sum']),
                                _check_sum_is_none(all_regions_month_completed['amount__sum']))
                        })
                    else:
                        department_moth_data.append({
                            "department_plan": department_plan,
                            "department_completed": department_completed,
                            "department_percentage": _calculate_percentage(department_plan, department_completed),

                            "region_month_plan": region_month_plan,
                            "region_month_completed": region_month_completed,
                            "region_month_percentage": _calculate_percentage(region_month_plan, region_month_completed),

                            "all_regions_month_plans": _check_sum_is_none(all_regions_month_plans['amount__sum']),
                            "all_regions_month_completed": _check_sum_is_none(
                                all_regions_month_completed['amount__sum']),
                            "all_regions_month_percentage": _calculate_percentage(
                                _check_sum_is_none(all_regions_month_plans['amount__sum']),
                                _check_sum_is_none(all_regions_month_completed['amount__sum']))
                        })
            department_next_cvartal_plan = _get_department_next_cvartal_plan(epoch_year,
                                                                             quarter_num, reg,
                                                                             depart,
                                                                             amount_type)
            department_cvartal_plan = _get_plan_data_in_cvartal_department(epoch_year, quarter_num,
                                                                           reg,
                                                                           depart,
                                                                           amount_type)
            department_cvartal_completed = _get_completed_plan_data_in_cvartal_department(epoch_year,
                                                                                          quarter_num, reg,
                                                                                          depart, amount_type)
            department_year_plan = _get_department_year_plan(epoch_year,
                                                             reg, depart, amount_type)
            department_year_completed = _get_department_year_completed(epoch_year, reg, depart, amount_type)

            cvartal.append({
                "department_cvartal_name": depart.name,
                "department_year_plan": department_year_plan,
                "department_year_completed": department_year_completed,
                "department_year_percentage": _calculate_percentage(department_year_plan,
                                                                    department_year_completed),
                "department_cvartal_plan": department_cvartal_plan,
                "department_cvartal_completed": department_cvartal_completed,
                "department_cvartal_percentage": _calculate_percentage(department_cvartal_plan,
                                                                       department_cvartal_completed),
                "department_next_cvartal_plan": department_next_cvartal_plan,
                "department_month_data": department_moth_data
            })
        plan_year = _get_year_plan_only_one_region(epoch_year, reg, amount_type)
        year_completed_plan = _get_completed_plans_off_year(epoch_year, reg,
                                                            amount_type)

        year_total_plan += _check_sum_is_none(plan_year)
        year_completed_total += _check_sum_is_none(year_completed_plan)

        region_cvartal_plan = _get_region_cvartal_plan(epoch_year, quarter_num, reg,
                                                       amount_type)
        region_cvartal_completed = _get_region_cvartal_actual(epoch_year, quarter_num, reg,
                                                              amount_type)
        next_region_cvartal_plan = _get_region_cvartal_plan_range_data(epoch_year, quarter_num, reg,
                                                                       amount_type)
        result.append({
            "region_name": reg.name,
            "region_cvartal_plan": region_cvartal_plan,
            "region_cvartal_completed": region_cvartal_completed,
            "region_cvartal_percentage": _calculate_percentage(region_cvartal_plan, region_cvartal_completed),
            "next_region_cvartal_plan": next_region_cvartal_plan,
            "plan_year": plan_year,
            "year_completed_plan": year_completed_plan,
            "year_percentage": _calculate_percentage(plan_year, year_completed_plan),
            "year_total_plan": year_total_plan,
            "year_completed_total": year_completed_total,
            "cvartal": cvartal
        })
    all_regions_cvartal_plans = FinancePlan.objects.filter(date__year=epoch_year, date__month__lte=quarter_num,
                                                           status=1, amount_type=amount_type).aggregate(Sum('amount'))

    all_regions_cvartal_completed = Finance.objects.filter(date__year=epoch_year, date__month__lte=quarter_num,
                                                           status=1, amount_type=amount_type).aggregate(Sum('amount'))
    year_plans_all_region = FinancePlan.objects.filter(date__year=epoch_year, status=1,
                                                       amount_type=amount_type).aggregate(Sum('amount'))
    year_completed_all_region = Finance.objects.filter(date__year=epoch_year, status=1, state=2,
                                                       amount_type=amount_type).aggregate(Sum('amount'))

    regions_next_cvartal_plans = FinancePlan.objects.filter(date__year=epoch_year,
                                                            amount_type=amount_type,
                                                            date__month__range=[quarter_num + 1, quarter_num + 3],
                                                            status=1).aggregate(Sum('amount'))

    context = {
        "amount_type": int(amount_type),
        "data": result,
        "months": months,
        "plan": _check_sum_is_none(year_plans_all_region['amount__sum']),
        "completed": _check_sum_is_none(year_completed_all_region['amount__sum']),
        "percentage": _calculate_percentage(year_plans_all_region['amount__sum'],
                                            year_completed_all_region['amount__sum']),
        "all_regions_cvartal_plans": _check_sum_is_none(all_regions_cvartal_plans['amount__sum']),
        "all_regions_cvartal_completed": _check_sum_is_none(all_regions_cvartal_completed['amount__sum']),
        "all_regions_cvartal_percentage": _calculate_percentage(all_regions_cvartal_plans['amount__sum'],
                                                                all_regions_cvartal_completed['amount__sum']),
        "regions_next_cvartal_plans": _check_sum_is_none(regions_next_cvartal_plans['amount__sum']),
        "start": year_start,
        "end": year_end
    }
    return context


class Report(LoginRequiredMixin, View):
    """Yillik reja va nech foiz bajarilgani tog'risida malumot uchun"""
    template_name = 'moliya/report/index.html'

    def get(self, request):
        amount_type = self.request.GET.get('type', None)
        current_year = date.today().year
        start = date(current_year, 1, 1).strftime('%Y-%m-%d')
        end_date = date(current_year, 12, 31).strftime('%Y-%m-%d')
        end = self.request.GET.get('end', None)
        if not end:
            end_dateformat = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            current_month = end_dateformat.month
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = date.today().strftime('%Y-%m-%d')
        else:
            end_dateformat = datetime.datetime.strptime(end, '%Y-%m-%d')
            current_month = end_dateformat.month
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = end_dateformat.strftime('%Y-%m-%d')
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            context = _filter_start_date_end_date_fn(start, end, current_year, regions, departments, amount_type)
            context['form'] = FinanceFilterForm(initial={'start': start, 'end': end, "type": amount_type})
            return render(request, self.template_name, context)
        else:
            form = FinanceFilterForm(initial={'start': start, 'end': end, "type": amount_type})
            context = {"start": start, "end": end, "form": form, "amount_type": amount_type}
            return render(request, self.template_name, context)


def _check_sum_is_none(_sum=None):
    total = 0
    if _sum:
        total = _sum
        return total
    else:
        return total


def _total_percentage(arr=None):
    total = 0
    for i in arr:
        total += i['percentage']
    return total


def _calculate_percentage(plan=None, completed=None):
    """Amaldagi va bajarilgan rejani percentagesini xisoblab beradi
        1-PARAMS PLAN
        2-PARAMS AMALDA
    """
    if plan and completed:
        result = (float(completed) * 100) / float(plan)
        return round(result, 1)
    else:
        return 0


def _filter_start_date_end_date_fn(start=None, end=None, current_year=None, regions=None, departments=None,
                                   amount_type=None):
    """Agar filterda start va end bolsa shu fn filterlab datani qaytaradi"""
    result = []  # barcha regionlardan toplangan malumotlar uchun arr
    plan_total = 0  # yillik planni summasi shunga tushadi
    completed_total = 0  # bajarilgan planni summasi shunga tushadi
    plan_data = FinancePlan.objects.filter(date__year=current_year,
                                           region__in=regions, department__in=departments,
                                           amount_type=amount_type, status=1)
    actual_data = Finance.objects.filter(date__range=[start, end],
                                         region__in=regions, department__in=departments,
                                         amount_type=amount_type, status=1,
                                         state=2)
    for i in range(len(regions)):
        check_department = departments.filter(region=regions[i])
        if check_department.exists():
            child = []  # regionlarni tegishli departmentlar uchun arr
            departments_list = departments.filter(region=regions[i])
            for department in departments_list:
                amount = plan_data.filter(department=department).aggregate(Sum('amount'))
                completed = actual_data.filter(department=department).aggregate(Sum('amount'))

                child.append({
                    "region": department.name,
                    "amount": _check_sum_is_none(amount['amount__sum']),
                    "completed": _check_sum_is_none(completed['amount__sum']),
                    "percentage": _calculate_percentage(amount['amount__sum'], completed['amount__sum']),
                })
        else:
            child = []
        amount = plan_data.filter(region=regions[i], department__in=departments).aggregate(Sum('amount'))
        completed = actual_data.filter(region=regions[i], department__in=departments).aggregate(Sum('amount'))
        plan_total += _check_sum_is_none(amount['amount__sum'])
        completed_total += _check_sum_is_none(completed['amount__sum'])
        result.append({
            "region": regions[i].name,
            "amount": _check_sum_is_none(amount['amount__sum']),
            "completed": _check_sum_is_none(completed['amount__sum']),
            "percentage": _calculate_percentage(amount['amount__sum'], completed['amount__sum']),
            "child": child
        })

    total_percentage = _calculate_percentage(plan_total, completed_total)
    context = {
        "is_user": True,
        "finances": result,
        "amount_type": int(amount_type),
        "start": start,
        "end": end,
        "plan_total": plan_total,
        "completed_total": completed_total,
        "total_percentage": total_percentage
    }
    return context


# def _default_report_data_fn(regions=[], departments=None, amount_type=None):
#     """Default shu report ni qaytaradi agar vaqt boyicha filter qilinmasa"""
#     epoch_year = date.today().year
#     year_start = date(epoch_year, 1, 1)
#     year_end = date(epoch_year, 12, 31)
#     today = datetime.datetime.now()
#     result = []
#     plan_total = 0
#     completed_total = 0
#     plan_data = FinancePlan.objects.filter(date__range=[year_start, year_end],
#                                            region__in=regions, department__in=departments,
#                                            status=1, amount_type=amount_type)
#     actual_data = Finance.objects.filter(date__range=[year_start, year_end],
#                                          region__in=regions, department__in=departments,
#                                          status=1, amount_type=amount_type, state=2)
#     for i in range(len(regions)):
#         check_department = departments.filter(region=regions[i])
#         if check_department.exists():
#             child = []
#             departments_list = departments.filter(region=regions[i])
#             for department in departments_list:
#                 amount = plan_data.filter(department=department).aggregate(Sum('amount'))
#                 completed = actual_data.filter(department=department).aggregate(Sum('amount'))
#
#                 child.append({
#                     "region": department.name,
#                     "amount": _check_sum_is_none(amount['amount__sum']),
#                     "completed": _check_sum_is_none(completed['amount__sum']),
#                     "percentage": _calculate_percentage(amount['amount__sum'], completed['amount__sum']),
#                 })
#         else:
#             child = []
#         amount = plan_data.filter(region=regions[i], department__in=departments).aggregate(Sum('amount'))
#         completed = actual_data.filter(region=regions[i], department__in=departments).aggregate(Sum('amount'))
#
#         plan_total += _check_sum_is_none(amount['amount__sum'])
#         completed_total += _check_sum_is_none(completed['amount__sum'])
#         result.append({
#             "region": regions[i].name,
#             "amount": _check_sum_is_none(amount['amount__sum']),
#             "completed": _check_sum_is_none(completed['amount__sum']),
#             "percentage": _calculate_percentage(amount['amount__sum'], completed['amount__sum']),
#             "child": child
#         })
#
#     total_percentage = _calculate_percentage(plan_total, completed_total)
#     form = FilterForm(initial={'start': year_start, 'end': today})
#     context = {
#         "is_user": True,
#         "amount_type": int(amount_type),
#         "finances": result,
#         "start": year_start.strftime('%Y-%m-%d'),
#         "end": year_end.strftime('%Y-%m-%d'),
#         "form": form,
#         "plan_total": plan_total,
#         "completed_total": completed_total,
#         "total_percentage": total_percentage
#     }
#     return context


def generate_month_year(year=None):
    epoch_year = date.today().year
    year_start = date(epoch_year, 1, 1)
    result = []
    for i in range(12):
        a = date(year, i + 1, 1)
        result.append(str(a))
    return result


def get_unique_items(numbers):
    list_of_unique_numbers = []
    unique_numbers = set(numbers)
    for number in unique_numbers:
        list_of_unique_numbers.append(number)

    return list_of_unique_numbers


class FinanceProfitTypesReport(View):
    template_name = 'moliya/report/profit_types.html'
    """Viloyatlar va ularning tashkilotlari bo'yicha yillik report"""

    def get(self, request):
        data = []
        start = self.request.GET.get('start', None)
        end = self.request.GET.get('end', None)
        if not end:
            end_dateformat = datetime.datetime.strptime(year_end, '%Y-%m-%d')
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = end_dateformat
        else:
            end_dateformat = datetime.datetime.strptime(end, '%Y-%m-%d')
            current_year = end_dateformat.year
            start = date(current_year, 1, 1).strftime('%Y-%m-%d')
            end = end_dateformat.strftime('%Y-%m-%d')

        current_month = end_dateformat.month
        amount_type = self.request.GET.get('type', 1)
        finance_type_data = FinanceType.objects.filter(status=1)
        region_id = None
        region_obj = None
        result_amount_sum = 0
        result = []
        form = FinanceFilterForm(initial={"start": start, "end": end, "type": amount_type})
        regions, departments = get_current_user_regions_and_departments_qs(self.request.user)
        if regions and departments:
            finance_actual_data = Finance.objects.filter(date__range=[year_start, year_end],
                                                         amount_type=amount_type,
                                                         status=1,
                                                         state=2)
            x = 1
            for depart in departments:
                x = x + 1
                depart_child = []
                depart_amount__sum = 0
                for item in finance_type_data:
                    amount_query = finance_actual_data.filter(department=depart,
                                                              type=item).aggregate(Sum('amount'))
                    amount = _check_sum_is_none(amount_query['amount__sum'])
                    depart_amount__sum += amount
                    depart_child.append({"amount": amount})
                if region_id != depart.region_id:
                    region_obj = Region.objects.get(id=depart.region_id)
                    region_child = []
                    region_amount__sum = 0
                    for item in finance_type_data:
                        amount_query = finance_actual_data.filter(region=region_obj,
                                                                  department__in=departments,
                                                                  type=item).aggregate(Sum('amount'))
                        amount = _check_sum_is_none(amount_query['amount__sum'])
                        region_amount__sum += amount
                        region_child.append({
                            "amount": amount,
                        })
                    data.append({
                        "index": 1,
                        "region_name": region_obj.name,
                        "region_child": region_child,
                        "region_amount__sum": region_amount__sum,
                        "depart_name": depart.name,
                        "depart_child": depart_child,
                        "depart_amount__sum": depart_amount__sum
                    })
                    x = 1
                else:
                    data.append({
                        "index": x,
                        "depart_name": depart.name,
                        "depart_child": depart_child,
                        "depart_amount__sum": depart_amount__sum
                    })
                region_obj = None
                region_id = depart.region_id
            for item in finance_type_data:
                amount_query = finance_actual_data.filter(type=item, region__in=regions,
                                                          department__in=departments).aggregate(Sum("amount"))
                amount = _check_sum_is_none(amount_query['amount__sum'])
                result_amount_sum += amount
                result.append({"amount": amount})
            ctx = {"finance_type_data": finance_type_data,
                   "start": start,
                   "amount_type": int(amount_type),
                   "end": end,
                   "data": data,
                   "result": result,
                   "form": form,
                   "result_amount_sum": result_amount_sum}
            return render(request, self.template_name, ctx)
        else:
            return render(request, self.template_name)


"""Generate EXCEL reports ↓ ↓ ↓ .xlsx files"""


class FinancePlanQuarterReportXLSX(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/finance/all/report/"""

    def get(self, request):
        from ..finance.excel.quarter_finance_report import FinancePlanQuarterSheet
        start = request.GET['start']
        end = request.GET['end']
        amount_type = request.GET['amount_type']
        if start and end and len(end) == 10 and amount_type:
            xlsx = FinancePlanQuarterSheet(start=start, end=end, amount_type=amount_type, user=self.request.user.pk)
            return xlsx.generate_excel_finance_report()
        else:
            messages.error(request, "Sana noto'g'ri kiritilgan")
            return render(request, 'moliya/report/all_report.html', {})


class FinanceByTypeReportXLSX(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/finance/profit/types/report"""

    def get(self, request):
        from ..finance.excel.report_by_type import FinanceByTypeSheet
        start = request.GET['start']
        end = request.GET['end']
        amount_type = request.GET['amount_type']
        if start and end and amount_type:
            xlsx = FinanceByTypeSheet(start=start, end=end, amount_type=amount_type, user=self.request.user)
            return xlsx.generate_excel_finance_report()
        else:
            messages.error(request, "Sana noto'g'ri kiritilgan")
            return render(request, 'moliya/report/profit_types.html', {})


class FinanceGeneralReportXLSX(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/finance/reports/?"""

    def get(self, request):
        from ..finance.excel.general_finance_report import FinanceGeneralSheet
        start = request.GET['start']
        end = request.GET['end']
        amount_type = request.GET['amount_type']
        if start and end and amount_type:
            # epoch_year = datetime.datetime.strptime(start, '%Y-%m-%d').year
            xlsx = FinanceGeneralSheet(
                start=start, end=end, amount_type=amount_type, user=self.request.user.pk)
            return xlsx.generate_excel_general_finance_report()
        else:
            messages.error(request, "Sana noto'g'ri kiritilgan")
            return render(request, 'moliya/report/index.html', {})


class ProductionServicesReportXLSX(LoginRequiredMixin, View):
    """http://127.0.0.1:8000/finance/production/service/all/report?"""

    def get(self, request):
        from ..finance.excel.production_services_report import ProductionServicesSheet
        start = request.GET['start']
        end = request.GET['end']
        if start and end and len(end) == 10:
            xlsx = ProductionServicesSheet(user=self.request.user, start=start, end=end)
            return xlsx.generate_production_services_excel()
        else:
            messages.error(request, "Sana noto'g'ri kiritilgan")
            return render(request, 'moliya/report/production_and_paid_service_report.html', {})


class ChangeFinanceActualState(APIView):

    def get(self, request):
        item_id = self.request.GET.get('item', None)
        state_code = self.request.GET.get('state', None)
        if item_id and state_code:
            Finance.objects.filter(id=item_id).update(state=state_code)
        return Response({"msg": True})


def export_exel(request):
    response = HttpResponse(content_type='application/ms-exel')
    response['Content-Disposition'] = 'attachment; filename=Finance' + str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Finance')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = (['Date', 'Amount', 'Department', 'Region', 'Creator', 'Type', 'Status'])

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = FinancePlan.objects.all().values_list('date', 'amount', 'region', 'creator', 'type', 'status')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)
    return response


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=FinancePlan' + str(datetime.datetime.now()) + 'csv'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Amount', 'Department', 'Region', 'Creator', 'Type', 'Status'])

    finance_plans = FinancePlan.objects.all()
    for plan in finance_plans:
        writer.writerow([plan.date, plan.amount, plan.department, plan.region, plan.creator, plan.type, plan.status])
    return response


